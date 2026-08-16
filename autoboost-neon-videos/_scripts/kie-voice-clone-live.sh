#!/usr/bin/env bash
# Kie/Suno singing-voice clone — LIVE mode.
#
# WHY THIS SCRIPT EXISTS
# The verification phrase returned by POST /api/v1/voice/validate expires between
# 60 s and 180 s after it becomes readable (measured 2026-08-16, see
# kie-voice-clone-STATE.md). Past that window, voice/generate is accepted with
# code 200 and then fails at polling with:
#   "Verification phrase expired or not found. Please request a new phrase."
# So the ONLY viable flow is: draw the phrase, sing it, submit — inside ~2 minutes.
#
# This script removes every second of latency on OUR side: it draws the phrase,
# prints it immediately, then WATCHES a drop directory. The instant an audio file
# lands there it converts, uploads and submits. Our own overhead is ~5 s, which
# leaves Tony the whole remaining budget.
#
# USAGE
#   1. Put a public URL of a clean a-cappella recording of Tony in SRC_URL below
#      (this is the voice to clone — 8 s of it are analysed).
#   2. Tony must be ready to record BEFORE you launch: phone in hand, quiet room.
#   3. ./kie-voice-clone-live.sh <presignedUploadUrl> <publicUrl>
#      (get the pair from blotato_create_presigned_upload_url beforehand — doing it
#      after the phrase is drawn wastes 10 s of the budget)
#   4. Read the phrase out loud to Tony the moment it prints.
#   5. Tony sings it, sends the file, you drop it in $DROP.
#
set -euo pipefail

PRESIGNED="${1:?presigned upload URL required (create it BEFORE running)}"
PUBLIC="${2:?public URL matching the presigned URL required}"
SRC_URL="${SRC_URL:-https://database.blotato.io/storage/v1/object/public/public_media/aef82d60-4167-4bf9-b043-3808d5fccdb4/cb7b1c95-692c-4c88-a7b1-c54257f41d89.mp3}"
DROP="${DROP:-/tmp/kie-drop}"
DEADLINE_S="${DEADLINE_S:-150}"   # hard stop: phrase is dead well before 180 s

export PATH="/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static:$PATH"
source /work/.kie.env
API=https://api.kie.ai/api/v1
AUTH=(-H "Authorization: Bearer $KIE_API_KEY" -H "Content-Type: application/json")

mkdir -p "$DROP"; rm -f "$DROP"/* 2>/dev/null || true
echo ">> drop directory ready: $DROP  (drop Tony's take there, any audio format)"

echo ">> drawing phrase..."
TID=$(curl -s -X POST "$API/voice/validate" "${AUTH[@]}" \
  -d "{\"voiceUrl\":\"$SRC_URL\",\"vocalStartS\":0,\"vocalEndS\":8,\"language\":\"fr\"}" \
  | grep -o '"taskId":"[^"]*' | cut -d'"' -f4)
[ -n "$TID" ] || { echo "validate failed"; exit 1; }

PHRASE=""
for i in $(seq 1 20); do
  sleep 3
  V=$(curl -s -H "Authorization: Bearer $KIE_API_KEY" "$API/voice/validate-info?taskId=$TID")
  case "$V" in
    *processing_validate_fail*) echo "task died upstream, relaunch: $V"; exit 2;;
  esac
  PHRASE=$(echo "$V" | grep -o '"validateInfo":"[^"]*' | cut -d'"' -f4)
  [ -n "$PHRASE" ] && break
done
[ -n "$PHRASE" ] || { echo "no phrase in time"; exit 1; }
READY=$(date -u +%s)

cat <<BANNER

=========================================================
  TONY CHANTE MAINTENANT (a cappella, 8-15 s) :

      $PHRASE

  Budget : ${DEADLINE_S}s a partir de maintenant.
=========================================================

BANNER

FILE=""
while [ -z "$FILE" ]; do
  ELAPSED=$(( $(date -u +%s) - READY ))
  [ "$ELAPSED" -gt "$DEADLINE_S" ] && { echo "DEADLINE BLOWN (${ELAPSED}s) — phrase is dead, relaunch"; exit 3; }
  FILE=$(find "$DROP" -type f -size +1k 2>/dev/null | head -1)
  [ -z "$FILE" ] && sleep 1
done
sleep 1   # let the copy finish
echo ">> got $FILE at t+$(( $(date -u +%s) - READY ))s"

OUT=$(mktemp -u).mp3
ffmpeg -y -hide_banner -loglevel error -i "$FILE" -ac 1 -ar 44100 -c:a libmp3lame -b:a 192k "$OUT"
curl -s -o /dev/null -X PUT "$PRESIGNED" --data-binary "@$OUT"
echo ">> uploaded at t+$(( $(date -u +%s) - READY ))s"

curl -s -X POST "$API/voice/generate" "${AUTH[@]}" \
  -d "{\"taskId\":\"$TID\",\"verifyUrl\":\"$PUBLIC\",\"voiceName\":\"Tony Payet Chant\",\"description\":\"Voix chantee de Tony Payet, FR, pop\",\"style\":\"pop\",\"singerSkillLevel\":\"intermediate\"}"
echo
echo ">> submitted at t+$(( $(date -u +%s) - READY ))s — polling"

for i in $(seq 1 30); do
  sleep 4
  RI=$(curl -s -H "Authorization: Bearer $KIE_API_KEY" "$API/voice/record-info?taskId=$TID")
  echo "   $RI"
  case "$RI" in *'"status":"success"'*|*'"status":"fail"'*) break;; esac
done
echo ">> taskId=$TID"
