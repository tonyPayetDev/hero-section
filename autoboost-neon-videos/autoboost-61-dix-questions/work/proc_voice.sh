#!/usr/bin/env bash
# Locked v3 post-processing: trim silence head AND tail, speed up, normalise, mono 48k.
set -e
export PATH="/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static:$PATH"
W=/work/autoboost-neon-videos/autoboost-61-dix-questions/work
T=$W/tts; mkdir -p $T/proc

for id in t01 t02 t03 t04 t05 t06 t07 t08 t09; do
  case $id in
    t09) SP=1.05 ;;   # final tag breathes a little
    *)   SP=1.12 ;;
  esac
  ffmpeg -y -v error -i $T/$id.mp3 \
    -af "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05:detection=peak,\
areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05:detection=peak,areverse,\
atempo=$SP,dynaudnorm=f=200:g=5" \
    -ac 1 -ar 48000 $T/proc/$id.wav
  d=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 $T/proc/$id.wav)
  printf "%s  %6.3fs  (sp=%s)\n" $id $d $SP
done
