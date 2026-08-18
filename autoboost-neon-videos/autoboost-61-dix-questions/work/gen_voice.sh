#!/usr/bin/env bash
# 10 QUESTIONS — cloned-voice segments via tts-gen webhook (voixUrl mandatory,
# without it the OpenAI branch is dead). Consent for the clone is standing.
export PATH="/home/claude/tools/node/bin:$PATH"
OUT=/work/autoboost-neon-videos/autoboost-61-dix-questions/work/tts
mkdir -p "$OUT"
VOIX="https://assets.automatisationboost.com/voix/archiviste_ZIl7EoOf.mp3"
URL="https://n7n.automatisationboost.com/webhook/tts-gen"

gen () {
  local id="$1"; shift
  local text="$1"; shift
  local f="$OUT/$id.mp3"
  for att in 1 2 3; do
    curl -s -m 180 -X POST "$URL" -H "Content-Type: application/json" \
      -d "$(node -e 'process.stdout.write(JSON.stringify({text:process.argv[1],voixUrl:process.argv[2]}))' "$text" "$VOIX")" -o "$f"
    sz=$(stat -c%s "$f" 2>/dev/null || echo 0)
    if [ "$sz" -gt 1024 ]; then echo "OK $id ($sz bytes) att$att"; return 0; fi
    echo "RETRY $id att$att size=$sz"; sleep 3
  done
  echo "FAIL $id"; return 1
}

gen t01 "Écoute bien. Tu crois te connaître. Tu te racontes la même histoire depuis des années." &
gen t02 "Tu vas aller sur Claude. Et tu vas le tester deux fois. Sur un Claude vide. Et sur celui qui a déjà toutes tes conversations." &
gen t03 "Tu lui demandes ça, en dix questions. Que pourrais-tu me demander sur moi-même pour révéler quelque chose que moi-même j'ignore ?" &
wait
gen t04 "Et tu précises. Une par une. Pas toutes à la fois." &
gen t05 "C'est ce détail qui change tout." &
gen t06 "Le Claude vide te pose des questions intelligentes. Et froides." &
wait
gen t07 "Celui qui te connaît te pose la question que tu évites depuis six mois." &
gen t08 "Tu vas être choqué. Tu vas être bluffé par les questions. Tu vas découvrir comment tu es." &
gen t09 "C'est indéniable. Irréfutable. Commente MIROIR, je t'envoie les dix questions." &
wait
echo "=== DONE ==="; ls -la "$OUT"/t0*.mp3
