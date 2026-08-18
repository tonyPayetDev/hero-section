#!/usr/bin/env bash
# Concat the 11 shots -> overlay the fake comment field on the CTA -> burn captions -> mux audio.
# FONTCONFIG_PATH is mandatory or libass renders nothing.
set -e
export PATH="/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static:/home/claude/tools/node/bin:$PATH"
export FONTCONFIG_PATH="/home/claude/tools/chromelibs/etc/fonts"
P=/work/autoboost-neon-videos/autoboost-61-dix-questions
W=$P/work; C=$W/clips; S=$W/screens
mkdir -p $P/public

SEGS="S1 S2 S3 S4 S5 S6 S7 S8 S9 S10 S11"

IN=""; CAT=""; N=0
for id in $SEGS; do IN="$IN -i $C/$id.mp4"; CAT="$CAT[$N:v]"; N=$((N+1)); done

# fake comment field: MIROIR typed letter by letter, keyed to the spoken CTA
# state  from    to
CTA_T="0:30.60:31.90 1:31.90:32.04 2:32.04:32.18 3:32.18:32.32 4:32.32:32.46 5:32.46:32.60 6:32.60:33.40 7:33.40:35.00"
for spec in $CTA_T; do n=${spec%%:*}; IN="$IN -i $S/cta_$n.png"; done

FC="${CAT}concat=n=$N:v=1:a=0[cat]"
prev="cat"; k=$N; i=0
for spec in $CTA_T; do
  a=$(echo $spec | cut -d: -f2); b=$(echo $spec | cut -d: -f3)
  FC="$FC;[$prev][$k:v]overlay=0:1150:enable='between(t,$a,$b)'[o$i]"
  prev="o$i"; k=$((k+1)); i=$((i+1))
done
FC="$FC;[$prev]subtitles=filename=$W/captions.ass:fontsdir=$W/fonts[vout]"

ffmpeg -y -v error $IN -i $W/final_audio.wav \
 -filter_complex "$FC" \
 -map "[vout]" -map "$k:a" \
 -c:v libx264 -pix_fmt yuv420p -crf 19 -preset medium -r 30 \
 -c:a aac -b:a 192k -movflags +faststart \
 $P/public/video.mp4

echo "=== DONE ==="
ffprobe -v error -show_entries format=duration -show_entries stream=codec_type,width,height,nb_frames,r_frame_rate -of default=nk=0 $P/public/video.mp4
ls -la $P/public/video.mp4
