#!/usr/bin/env bash
# Extrait la piste audio d'une vidéo, puis en sépare la voix et l'instrumental.
#
# Deux sorties distinctes, parce qu'elles servent à deux choses :
#   audio.wav        — la bande complète, pour l'analyse (BPM, structure)
#   instrumental.mp3 — la musique seule, quand il faut la reposer sous une
#                      autre voix. C'est la sortie qu'on utilise pour refaire
#                      une vidéo « dans le même style » sans garder la voix
#                      de quelqu'un d'autre.
set -euo pipefail
export PATH="/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static:/home/claude/tools/node/bin:$PATH"

VIDEO="${1:?usage: extraire.sh <video.mp4> [dossier-sortie]}"
OUT="${2:-$(dirname "$VIDEO")/musique}"
mkdir -p "$OUT"

echo "── source ──"
ffprobe -v error -show_entries format=duration \
  -show_entries stream=codec_type,codec_name,sample_rate,channels \
  -of default=nw=1 "$VIDEO"

# 48 kHz mono : c'est la cadence attendue par l'analyse plus bas, et le mono
# évite qu'une différence de phase entre canaux fausse la mesure d'énergie.
ffmpeg -v error -y -i "$VIDEO" -vn -ac 1 -ar 48000 -c:a pcm_s16le "$OUT/audio.wav"
echo "  audio.wav : $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT/audio.wav")s"

# Isolation voix / instrumental via WaveSpeed. Le modèle rend DEUX pistes ;
# celle qui nous intéresse est l'instrumental.
CLE=$(grep -oE '[A-Za-z0-9_-]{20,}' /work/.wavespeed.env | head -1)
if [ -z "$CLE" ]; then echo "  ⚠️  pas de clé WaveSpeed, isolation sautée"; exit 0; fi

# Le modèle attend une URL : on téléverse d'abord le fichier.
URL=$(curl -s -X POST "https://api.wavespeed.ai/api/v3/media/upload/binary" \
  -H "Authorization: Bearer $CLE" -F "file=@$OUT/audio.wav" \
  | node -e 'let b="";process.stdin.on("data",d=>b+=d).on("end",()=>{try{const j=JSON.parse(b);console.log(j.data?.download_url||"")}catch(e){console.log("")}})')
if [ -z "$URL" ]; then echo "  ⚠️  téléversement échoué, isolation sautée"; exit 0; fi

node "$(dirname "$0")/isoler.mjs" "$URL" "$OUT"
