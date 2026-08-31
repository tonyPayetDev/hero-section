#!/usr/bin/env bash
# =============================================================================
#  Journal IA — rendu + publication déterministes (aucun agent dans la boucle)
#
#  usage: render-publish.sh <AAAA-MM-JJ> [options]
#
#    --no-publish   rendu seulement (pas de previsualisation, pas de Blotato)
#    --no-social    publie sur previsualisation mais ne programme pas Blotato
#    --force        refait le rendu / republie même si la route existe déjà
#    --at <ISO>     heure de programmation (défaut 03:00 UTC du jour, +2h si passé)
#
#  Sortie : dernière ligne "STATUS: OK ..." ou "STATUS: FAIL <raison>".
#  Codes  : 0 OK · 1 échec · 2 usage · 3 édition absente · 4 déjà publié (no-op)
#
#  Appelé par n8n en SSH — voir README à la fin du fichier.
# =============================================================================
set -uo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB="$SKILL_DIR/lib"

# ---------------------------------------------------------------- toolchain
export PATH="/home/claude/tools/node/bin:/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static:/home/claude/tools/chromelibs/usr/bin:$PATH"
export LD_LIBRARY_PATH="/home/claude/tools/chromelibs/lib/x86_64-linux-gnu:/home/claude/tools/chromelibs/usr/lib/x86_64-linux-gnu:${LD_LIBRARY_PATH:-}"
export FONTCONFIG_PATH="/home/claude/tools/chromelibs/etc/fonts"
export FFPROBE="$(command -v ffprobe || echo ffprobe)"

HF="${JIA_HYPERFRAMES:-/work/autoboost-neon-videos/veille-to-avatar-v3/node_modules/.bin/hyperframes}"
PREVIS_REPO="${JIA_PREVIS_REPO:-/work/previsualisation}"
PREVIS_UUID="in9lww2r6zmrxdgubz4w09iq"
PREVIS_HOST="https://previsualisation.automatisationboost.com"
VOIX_URL="${JIA_VOIX_URL:-https://assets.automatisationboost.com/voix/archiviste_ZIl7EoOf.mp3}"
TTS_URL="${JIA_TTS_URL:-https://n7n.automatisationboost.com/webhook/tts-gen}"
OUT_ROOT="${JIA_OUT_ROOT:-/work/autoboost-neon-videos}"

# ------------------------------------------------------------------- args
DATE=""; NO_PUBLISH=0; NO_SOCIAL=0; FORCE=0; AT=""
while [ $# -gt 0 ]; do
  case "$1" in
    --no-publish) NO_PUBLISH=1 ;;
    --no-social)  NO_SOCIAL=1 ;;
    --force)      FORCE=1 ;;
    --at)         shift; AT="${1:-}" ;;
    -h|--help)    sed -n '2,18p' "${BASH_SOURCE[0]}"; exit 0 ;;
    *)            [ -z "$DATE" ] && DATE="$1" || { echo "argument inconnu: $1" >&2; exit 2; } ;;
  esac
  shift
done
# Par défaut : la date de la JOURNÉE RÉUNION (UTC+4), pas la date UTC.
# Le rendu démarre à 23h00 UTC, c'est-à-dire 3h00 du matin à La Réunion le
# LENDEMAIN. `date -u +%F` renverrait la veille et ferait rejouer l'édition
# déjà publiée. La Réunion n'a pas d'heure d'été : le décalage +4h est constant.
[ -z "$DATE" ] && DATE="$(date -u -d '+4 hours' +%F)"
if ! [[ "$DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
  echo "usage: render-publish.sh <AAAA-MM-JJ> [--no-publish|--no-social|--force|--at ISO]" >&2
  echo "STATUS: FAIL date invalide"; exit 2
fi

# Créneau de publication visé : 03:00 UTC = 7h00 heure Réunion.
# Résolu par une fonction car il sert DEUX fois : à l'écriture précoce du plan
# (juste après le rendu) et à l'étape 8. S'il est déjà passé, on part au plus
# tôt — l'ancien repli « +2 heures » décalait la sortie à 9h sans rien dire.
resolve_at() {
  [ -n "$AT" ] && { echo "$AT"; return; }
  local a="${DATE}T03:00:00Z" now ts
  now=$(date -u +%s); ts=$(date -u -d "$a" +%s 2>/dev/null || echo 0)
  [ "$ts" -le "$now" ] && a=$(date -u -d '+10 minutes' +%FT%H:%M:00Z)
  echo "$a"
}

P="$OUT_ROOT/journal-ia-$DATE"
W="$P/work"
ROUTE="journal-ia-$DATE"
mkdir -p "$SKILL_DIR/logs" "$W/tts/proc" "$W/clips" "$P/public/assets" "$P/public/fonts" "$P/renders"
LOG="$SKILL_DIR/logs/$DATE-$(date -u +%H%M%S).log"

# --------------------------------------------------------------- plumbing
exec > >(tee -a "$LOG") 2>&1
step() { echo; echo "═══ [$(date -u +%H:%M:%S)] $*"; }
die()  { echo; echo "STATUS: FAIL $*"; exit "${2:-1}"; }
ok()   { echo; echo "STATUS: OK $*"; exit 0; }

LOCK="/tmp/journal-ia-$DATE.lock"
exec 9>"$LOCK"
flock -n 9 || die "un rendu du $DATE est déjà en cours ($LOCK)"

echo "Journal IA · $DATE · $(date -u +%FT%TZ) · log=$LOG"
MEM=$(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo)
echo "MemAvailable ${MEM} Mo"
[ "$MEM" -lt 1800 ] && die "mémoire insuffisante (${MEM} Mo < 1800) — rendu impossible"

# ============================================================ 1. ÉDITION
step "1/8 · récupération de l'édition"
git -C "$PREVIS_REPO" fetch --quiet origin '+refs/heads/*:refs/remotes/origin/*' 2>/dev/null || true
git -C "$PREVIS_REPO" pull --quiet --ff-only 2>/dev/null || true

MD="$PREVIS_REPO/journal-ia/$DATE.md"

# Le rendu démarre à 23h00 UTC (3h00 Réunion) mais la routine de veille cloud
# n'écrit l'édition du jour que vers 00h10-00h25 UTC — soit APRÈS. Mesuré :
#   2026-08-16 → 00:09:15Z · 2026-08-17 → 00:23:15Z · 2026-08-19 → 00:18:42Z
# On ne meurt donc plus sur une édition absente : on l'ATTEND, en refetchant.
# Sans cette attente, un déclenchement à 23h00 échouerait tous les jours.
fetch_edition() {
  [ -f "$MD" ] && return 0
  git -C "$PREVIS_REPO" fetch --quiet origin '+refs/heads/*:refs/remotes/origin/*' 2>/dev/null || true
  for BR in "origin/journal-ia-$DATE" "origin/main"; do
    if git -C "$PREVIS_REPO" cat-file -e "$BR:journal-ia/$DATE.md" 2>/dev/null; then
      mkdir -p "$PREVIS_REPO/journal-ia"
      git -C "$PREVIS_REPO" show "$BR:journal-ia/$DATE.md" > "$MD" && echo "édition récupérée depuis $BR"
      return 0
    fi
  done
  return 1
}

# Plafond d'attente : 60 min. Il DOIT rester sous l'executionTimeout de n8n
# (5400 s = 90 min), sinon n8n tue l'exécution avant que le script ait pu écrire
# sa ligne "STATUS: FAIL" — et l'alerte Telegram ne partirait jamais. Départ
# 00h30 UTC + 60 min d'attente + ~15 min de rendu/publication = 75 min < 90 min.
# Mieux vaut un échec bruyant à 01h30 qu'une exécution tuée en silence.
WAIT_MIN="${JIA_WAIT_EDITION_MIN:-60}"
if ! fetch_edition; then
  DEADLINE=$(( $(date -u +%s) + WAIT_MIN * 60 ))
  echo "édition du $DATE pas encore publiée — attente (jusqu'à ${WAIT_MIN} min, sondage toutes les 60 s)"
  until fetch_edition; do
    if [ "$(date -u +%s)" -ge "$DEADLINE" ]; then
      die "édition introuvable après ${WAIT_MIN} min d'attente : journal-ia/$DATE.md — la routine de veille n'a rien écrit" 3
    fi
    sleep 60
  done
fi
echo "édition : $MD ($(wc -c <"$MD") octets)"

# idempotence : route déjà en ligne ?
if [ "$FORCE" -eq 0 ] && [ -d "$PREVIS_REPO/$ROUTE" ] && [ -f "$PREVIS_REPO/$ROUTE/video.mp4" ]; then
  ok "route $ROUTE déjà publiée ($PREVIS_HOST/$ROUTE) — rien à refaire (--force pour rejouer)"
fi

# ============================================================ 2. PARSE
step "2/8 · parsing déterministe du script"
node "$LIB/parse_edition.mjs" "$MD" "$W/edition.json" || die "parsing de l'édition impossible"
NSEG=$(node -e 'console.log(require(process.argv[1]).segments.length)' "$W/edition.json")

# GARDE-FOU (2026-08-21) : le 21/08 est sorti en 18,9 s SANS UNE SEULE INFO.
# Le .md était complet et sourcé, mais la routine cloud avait varié l'amorce
# (`**Un.**` au lieu de `**Un — Titre.**`) et le parseur avait rendu 0 brève.
# Rien n'avait bronché : ni le rendu, ni la publication. Un journal sans brève
# n'est pas un journal — on s'arrête ici plutôt que de sortir une coquille vide.
NBREV=$(node -e 'console.log((require(process.argv[1]).briefs||[]).length)' "$W/edition.json")
if [ "${NBREV:-0}" -lt 3 ]; then
  die "édition à $NBREV brève(s) — refus de rendre. Le .md est probablement écrit dans une forme que parse_edition.mjs ne reconnaît pas : vérifier les amorces des paragraphes de « Script voix off »."
fi
step "   → $NBREV brèves reconnues"

# GARDE-FOU (2026-08-25) : le 25/08 à 03h00 UTC, le Journal est parti sur CINQ
# réseaux avec une brève intitulée « Argent) » et une autre coupée sur
# « … de Google rejoint l' ». Le 23/08 était déjà sorti avec le même défaut sans
# que personne le remarque. Le compte de brèves était bon dans les deux cas : le
# garde-fou du 21/08 ne voit pas ce genre de dégât.
# On refuse donc aussi une édition dont une brève est visiblement tronquée.
node "$LIB/check_briefs.mjs" "$W/edition.json" \
  || die "brève(s) malformée(s) — refus de rendre. Le découpage « Source — Titre » a mordu sur le corps du texte : relire les lignes signalées ci-dessus dans le .md avant de relancer."

# ============================================================ 3. VOIX
step "3/8 · voix clonée ($NSEG segments)"
gen_seg() {
  local id="$1" text="$2" f="$W/tts/$1.mp3" sig="$W/tts/$1.txt"
  # Le cache est indexé sur le TEXTE, pas sur l'id : si le script du jour change
  # (ou si un gag est reformulé), l'audio périmé doit être régénéré.
  if [ -s "$f" ] && [ "$(stat -c%s "$f")" -gt 2048 ] && [ -f "$sig" ] && [ "$(cat "$sig")" = "$text" ]; then
    echo "  = $id (cache)"; return 0
  fi
  local body; body=$(node -e 'process.stdout.write(JSON.stringify({text:process.argv[1],voixUrl:process.argv[2]}))' "$text" "$VOIX_URL")
  for att in 1 2 3; do
    curl -s -m 150 -X POST "$TTS_URL" -H "Content-Type: application/json" -d "$body" -o "$f"
    local sz; sz=$(stat -c%s "$f" 2>/dev/null || echo 0)
    [ "$sz" -gt 2048 ] && { printf '%s' "$text" > "$sig"; echo "  ✓ $id ($sz o, essai $att)"; return 0; }
    echo "  ↻ $id essai $att (${sz}o)"; sleep 3
  done
  echo "  ✗ $id"; return 1
}
export -f gen_seg 2>/dev/null || true

# NB: on attend des PID explicites. Un `wait` nu attendrait aussi le `tee` de
# la redirection globale (process substitution) et bloquerait pour toujours.
PIDS=()
while IFS=$'\t' read -r id text; do
  gen_seg "$id" "$text" &
  PIDS+=($!)
  if [ "${#PIDS[@]}" -ge "${JIA_TTS_PAR:-2}" ]; then wait "${PIDS[@]}" 2>/dev/null; PIDS=(); fi
done < <(node -e '
  const e=require(process.argv[1]);
  for(const s of e.segments) process.stdout.write(s.id+"\t"+s.text.replace(/[\t\n]/g," ")+"\n");
' "$W/edition.json")
[ "${#PIDS[@]}" -gt 0 ] && wait "${PIDS[@]}" 2>/dev/null
MISSING=$(node -e '
  const fs=require("fs"),p=process.argv[2];
  const miss=require(process.argv[1]).segments.filter(s=>{try{return fs.statSync(p+"/"+s.id+".mp3").size<2048}catch{return true}}).map(s=>s.id);
  process.stdout.write(miss.join(","));
' "$W/edition.json" "$W/tts")
[ -n "$MISSING" ] && die "génération de voix incomplète (webhook tts-gen) : $MISSING"

step "3b · traitement voix (silences coupés, atempo, normalisation)"
while IFS=$'\t' read -r id tempo; do
  ffmpeg -y -v error -i "$W/tts/$id.mp3" \
    -af "silenceremove=start_periods=1:start_silence=0.05:start_threshold=-45dB:detection=peak,areverse,silenceremove=start_periods=1:start_silence=0.08:start_threshold=-45dB:detection=peak,areverse,atempo=$tempo,dynaudnorm=f=200:g=5" \
    -ar 48000 -ac 1 "$W/tts/proc/$id.wav" || die "traitement audio KO sur $id"
done < <(node -e '
  const e=require(process.argv[1]);
  for(const s of e.segments) process.stdout.write(s.id+"\t"+(s.tempo||1.12)+"\n");
' "$W/edition.json")

# ============================================================ 4. LAYOUT
step "4/8 · calage temporel"
node "$LIB/layout.mjs" "$W/edition.json" "$W/tts/proc" "$W/timing.json" || die "calage impossible"
DUR=$(node -e 'console.log(require(process.argv[1]).duration)' "$W/timing.json")

# ============================================================ 5. COMPO
step "5/8 · composition HTML + audio + clips avatar"
cp -f "$SKILL_DIR/assets/"*.mp3 "$SKILL_DIR/assets/"*.js "$P/public/assets/" 2>/dev/null
cp -f "$SKILL_DIR/assets/fonts/"* "$P/public/fonts/" 2>/dev/null
node "$LIB/build_html.mjs" "$W/edition.json" "$W/timing.json" "$P/public/index.html" || die "génération HTML impossible"
node "$LIB/gen_ffmpeg.mjs" audio "$P" || die "génération du graphe audio impossible"
node "$LIB/gen_ffmpeg.mjs" pass2 "$P" || die "génération du graphe vidéo impossible"
bash "$W/prep_clips.sh"  || die "préparation des clips avatar KO"
bash "$W/build_audio.sh" || die "montage audio KO"

# ============================================================ 6. RENDU
step "6/8 · snapshot de contrôle"
node "$HF" snapshot "$P/public" --at 1.0 >/dev/null 2>&1 || echo "  (snapshot indisponible — on continue)"

step "6b · rendu HyperFrames (${DUR}s, ~10-20 min)"
# HyperFrames écrit dans ./renders/ RELATIF au cwd, et --out est ignoré : il faut
# se placer dans le projet, sinon le MP4 atterrit ailleurs et on ne le retrouve pas.
cd "$P" || die "projet introuvable: $P"
# la barre de progression n'écrit que des \r : sans `tr` le log devient une ligne de 170 Ko
node "$HF" render "$P/public" 2>&1 | tr '\r' '\n' | grep -vE 'Streaming frame|^\s*$' | tail -12
BASE=$(find "$P/renders" "$P/public/renders" -iname '*.mp4' -newermt '-120 min' 2>/dev/null | sort | tail -1)
[ -n "$BASE" ] || die "aucun rendu produit (voir $LOG)"
echo "rendu de base : $BASE"

step "6c · passe 2 · incrustation avatar + audio final"
bash "$W/pass2.sh" "$BASE" || die "passe 2 KO"
[ -s "$P/public/video.mp4" ] || die "video.mp4 absent après la passe 2"
VDUR=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "$P/public/video.mp4")
VMB=$(( $(stat -c%s "$P/public/video.mp4") / 1048576 ))
echo "vidéo finale : ${VDUR}s · ${VMB} Mo"

# Le plan de publication est écrit ICI, dès que la vidéo existe, et PLUS à la
# toute fin. Historique : le 19/08 le script est mort à l'étape 7 (token Coolify
# absent) avant d'avoir jamais appelé blotato.mjs — work/blotato-plan.json
# n'existait pas, les nœuds Blotato de n8n n'avaient rien à lire, et trois jours
# de Journal IA ne sont jamais sortis. Le plan ne doit dépendre de RIEN en aval.
node "$LIB/blotato.mjs" "$P/public/video.mp4" "$W/edition.json" "$(resolve_at)" --dry \
  || echo "  ⚠ plan Blotato non écrit à l'avance (l'étape 8 réessaiera)"

if [ "$NO_PUBLISH" -eq 1 ]; then
  ok "rendu seul ($P/public/video.mp4, ${VDUR}s, ${VMB} Mo) — publication désactivée (--no-publish)"
fi

# ============================================================ 7. PREVISU
step "7/8 · publication sur previsualisation ($ROUTE)"
[ -f /work/.deploy.env ] && . /work/.deploy.env

# ⚠ Ces variables NE SONT PAS dans l'environnement quand n8n appelle le script :
# `docker exec … bash -lc` ouvre un shell de login vierge, qui ne voit ni l'env de
# la session Claude Code ni ~/.bashrc. Seul /work/.deploy.env est lu — et il ne
# contient que GITHUB_TOKEN. Les anciennes gardes `: "${VAR:?msg}"` tuaient alors
# le script sur place, AVANT toute ligne « STATUS: » : n8n ne voyait aucun échec.
#
# Règle : seul le push GitHub est vital (c'est l'URL raw.githubusercontent que
# Blotato consomme). Le déploiement Coolify ne rafraîchit que le site de
# prévisualisation — il ne doit JAMAIS faire tomber la publication.
[ -n "${GITHUB_TOKEN:-}" ] || die "token GitHub absent (/work/.deploy.env) — impossible de pousser la vidéo"
PREVIS_WARN=""

R="$PREVIS_REPO"
git -C "$R" checkout -q main && git -C "$R" pull -q --ff-only || true
mkdir -p "$R/$ROUTE"
cp -f "$P/public/video.mp4" "$R/$ROUTE/video.mp4"
ffmpeg -y -v error -ss 1.5 -i "$P/public/video.mp4" -frames:v 1 -q:v 2 "$R/$ROUTE/cover.jpg" || true
node "$LIB/previs_page.mjs" "$W/edition.json" "$R/$ROUTE/index.html" "$VDUR" "$VMB" || die "page previsualisation KO"
node -e '
  const fs=require("fs"); const [f,route,label]=process.argv.slice(1);
  let h=fs.readFileSync(f,"utf8");
  if(h.includes(`href="/${route}"`)) process.exit(0);
  h=h.replace("  <ul>",`  <ul>\n    <li><a href="/${route}">\n      <span class="name">${label}</span>\n      <span class="badge">⏳ En attente</span>\n    </a></li>`);
  fs.writeFileSync(f,h);
' "$R/index.html" "$ROUTE" "Journal IA — $DATE" || true

git -C "$R" add "$ROUTE" index.html "journal-ia/$DATE.md"
git -C "$R" -c user.name="Claude" -c user.email="noreply@anthropic.com" \
  commit -q -m "feat(journal-ia): édition $DATE rendue (${VDUR}s)" || echo "  (rien à committer)"
PUSH_URL="https://${GITHUB_TOKEN}@github.com/tonyPayetDev/previsualisation.git"
git -C "$R" push -q "$PUSH_URL" HEAD:main || die "push previsualisation KO"

if [ -n "${COOLIFY_ACCESS_TOKEN:-}" ] && [ -n "${COOLIFY_BASE_URL:-}" ]; then
  curl -s -o /dev/null -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
    "${COOLIFY_BASE_URL%/}/api/v1/deploy?uuid=$PREVIS_UUID"
  echo "déploiement Coolify déclenché — attente du 200…"
  CODE=000
  for i in $(seq 1 25); do
    sleep 8
    CODE=$(curl -s -o /dev/null -w '%{http_code}' "$PREVIS_HOST/$ROUTE/?cb=$RANDOM")
    [ "$CODE" = "200" ] && break
  done
  if [ "$CODE" = "200" ]; then
    echo "✓ $PREVIS_HOST/$ROUTE — HTTP 200"
  else
    PREVIS_WARN=" · ⚠ route previsualisation non servie (HTTP $CODE)"
    echo "⚠ route $PREVIS_HOST/$ROUTE non servie (HTTP $CODE) — on continue, la vidéo est poussée sur GitHub"
  fi
else
  PREVIS_WARN=" · ⚠ deploiement Coolify non declenche (COOLIFY_ACCESS_TOKEN/COOLIFY_BASE_URL absents du shell)"
  echo "⚠ COOLIFY_ACCESS_TOKEN/COOLIFY_BASE_URL absents — déploiement previsualisation sauté."
  echo "  La vidéo est poussée sur GitHub, la programmation Blotato continue."
fi

if [ "$NO_SOCIAL" -eq 1 ]; then
  ok "route $PREVIS_HOST/$ROUTE (${VDUR}s)$PREVIS_WARN — Blotato désactivé (--no-social)"
fi

# ============================================================ 8. BLOTATO
step "8/8 · programmation Blotato (5 réseaux)"
AT="$(resolve_at)"
echo "créneau : $AT"
node "$LIB/blotato.mjs" "$P/public/video.mp4" "$W/edition.json" "$AT"
RC=$?
[ -s "$W/blotato-plan.json" ] || die "blotato-plan.json absent après blotato.mjs (rc=$RC) — n8n n'aurait rien à programmer"
case "$RC" in
  0) ok "route $PREVIS_HOST/$ROUTE (${VDUR}s)$PREVIS_WARN + 5 réseaux programmés à $AT" ;;
  3) ok "route $PREVIS_HOST/$ROUTE (${VDUR}s)$PREVIS_WARN — plan Blotato écrit dans $W/blotato-plan.json (clé API absente, planification à faire par l'appelant)" ;;
  *) die "programmation Blotato KO (rc=$RC) — la vidéo est poussée sur GitHub" ;;
esac
