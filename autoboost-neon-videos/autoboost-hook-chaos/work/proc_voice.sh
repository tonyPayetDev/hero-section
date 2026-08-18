#!/usr/bin/env bash
set -e
export PATH="/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static:$PATH"
cd /work/autoboost-neon-videos/autoboost-hook-chaos/work/tts
mkdir -p proc
proc () {
  local id="$1"; local tempo="$2"
  ffmpeg -y -v error -i "$id.mp3" \
    -af "silenceremove=start_periods=1:start_silence=0.05:start_threshold=-45dB:detection=peak,areverse,silenceremove=start_periods=1:start_silence=0.08:start_threshold=-45dB:detection=peak,areverse,atempo=$tempo,dynaudnorm=f=200:g=5" \
    -ar 48000 -ac 1 "proc/$id.wav"
}
for i in 01 02 03 04; do proc s$i 1.12; done
proc s05 1.06
proc s06 1.08
for i in 01 02 03 04 05 06; do d=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 proc/s$i.wav); echo "s$i $d"; done
