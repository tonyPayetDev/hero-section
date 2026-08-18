#!/usr/bin/env bash
set -e
export PATH="/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static:$PATH"
P=/work/autoboost-neon-videos/autoboost-hook-chaos
W=$P/work; C=$W/clips
BASE="$1"
[ -z "$BASE" ] && BASE=$(find $P -iname "*.mp4" -not -name "video.mp4" | sort | tail -1)
echo "BASE=$BASE"
ffprobe -v error -show_entries format=duration:stream=width,height -of default=nk=1 "$BASE" | head -4
ffmpeg -y -v error \
 -i "$BASE" \
 -i $C/w1.mp4 -i $C/w2.mp4 -i $C/w3.mp4 \
 -i $W/final_audio.wav \
 -filter_complex "\
 [1:v]scale=642:1146,setpts=PTS-STARTPTS+10.30/TB[o1];\
 [0:v][o1]overlay=219:153:enable='between(t,10.30,14.23)'[b1];\
 [2:v]scale=642:1146,setpts=PTS-STARTPTS+24.50/TB[o2];\
 [b1][o2]overlay=219:153:enable='between(t,24.50,26.37)'[b2];\
 [3:v]scale=642:1146,setpts=PTS-STARTPTS+29.85/TB[o3];\
 [b2][o3]overlay=219:153:enable='between(t,29.85,32.98)'[vout]" \
 -map "[vout]" -map "4:a" -t 34.6 \
 -c:v libx264 -pix_fmt yuv420p -crf 19 -preset medium \
 -c:a aac -b:a 192k -movflags +faststart \
 $P/public/video.mp4
echo "=== DONE ==="
ffprobe -v error -show_entries format=duration -show_entries stream=codec_type,width,height -of default=nk=1 $P/public/video.mp4
