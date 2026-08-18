#!/usr/bin/env bash
# Tony cloned-voice segments via tts-gen webhook (voixUrl MANDATORY)
export PATH="/home/claude/tools/node/bin:$PATH"
OUT=/work/autoboost-neon-videos/autoboost-hook-chaos/work/tts
mkdir -p "$OUT"
VOIX="https://assets.automatisationboost.com/voix/archiviste_ZIl7EoOf.mp3"
URL="https://n7n.automatisationboost.com/webhook/tts-gen"

gen () {
  local id="$1"; shift
  local text="$1"; shift
  local f="$OUT/$id.mp3"
  for att in 1 2 3; do
    curl -s -m 150 -X POST "$URL" \
      -H "Content-Type: application/json" \
      -d "$(node -e 'const t=process.argv[1],v=process.argv[2];process.stdout.write(JSON.stringify({text:t,voixUrl:v}))' "$text" "$VOIX")" \
      -o "$f"
    sz=$(stat -c%s "$f" 2>/dev/null || echo 0)
    if [ "$sz" -gt 1024 ]; then echo "OK $id ($sz bytes) att$att"; return 0; fi
    echo "RETRY $id att$att size=$sz"; sleep 3
  done
  echo "FAIL $id"; return 1
}

gen s01 "Pendant que tu enchaînes tes tâches à la main, mon système, lui, tourne tout seul." &
gen s02 "Chaque matin, il produit le journal I.A. du jour. Recherche, script, voix clonée, montage." &
gen s03 "Il génère des sites clients complets, et il publie sur cinq réseaux pendant que je dors." &
wait
gen s04 "Moi, je valide. C'est tout." &
gen s05 "Arrête de travailler comme une machine. Construis-en une." &
gen s06 "Commente le mot CHAOS, et je t'envoie le plan du système." &
wait
echo "=== ALL DONE ==="
ls -la "$OUT"
