#!/usr/bin/env bash
set -e
export PATH="/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static:$PATH"
B=/work/autoboost-neon-videos/_shared/avatar-bank/clips
W=/work/autoboost-neon-videos/autoboost-hook-chaos/work/clips
mkdir -p $W
mk(){ local src="$1" ss="$2" dur="$3" out="$4";
 ffmpeg -y -v error -ss $ss -t $dur -i $B/$src -an \
  -vf "scale=648:1152:force_original_aspect_ratio=increase,crop=648:1152,setsar=1,fps=30" \
  -c:v libx264 -pix_fmt yuv420p -crf 18 $W/$out; }
mk A1_hook_frontal.mp4    0.35 3.90 w1.mp4
mk B1_principe.mp4        0.60 1.80 w2.mp4
mk C2_commente_motcle.mp4 0.50 3.10 w3.mp4
for f in w1 w2 w3; do echo "$f $(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 $W/$f.mp4)"; done
