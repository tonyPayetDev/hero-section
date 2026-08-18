#!/usr/bin/env bash
# Avatar shots -> full-bleed 1080x1920, 30fps, NATIVE AUDIO DROPPED (-an).
# Zoom varies per shot so the 4-clip bank does not read as 4 clips.
set -e
export PATH="/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static:/home/claude/tools/node/bin:$PATH"
P=/work/autoboost-neon-videos/autoboost-61-dix-questions
W=$P/work; S=$W/src; C=$W/clips
mkdir -p $C

mk(){ local id="$1" src="$2" ss="$3" frames="$4" z="$5" yoff="$6"
 local sw sh
 sw=$(awk -v z="$z" 'BEGIN{printf "%d", int(1080*z/2)*2}')
 sh=$(awk -v z="$z" 'BEGIN{printf "%d", int(1920*z/2)*2}')
 ffmpeg -y -v error -ss $ss -i $S/$src -an -frames:v $frames \
  -vf "fps=30,scale=${sw}:${sh}:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920:(iw-1080)/2:(ih-1920)*${yoff},unsharp=5:5:0.4:5:5:0.0,setsar=1,eq=contrast=1.05:saturation=1.06" \
  -c:v libx264 -pix_fmt yuv420p -crf 17 -preset medium $C/$id.mp4; }

# id  source                        ss    frames zoom  yoff
mk S1  D1_hook_frontal.mp4          4.56  120    1.00  0.34
mk S2  D1_hook_frontal.mp4          0.45   87    1.14  0.32
mk S5  D2_insistance_doigts.mp4     5.55   84    1.06  0.33
mk S9  D4_relance_barbe.mp4         4.88  122    1.10  0.32
mk S10 D3_cta_lunettes.mp4          0.00  169    1.02  0.31

for f in S1 S2 S5 S9 S10; do
  printf "%-4s %s  %s\n" $f \
    "$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 $C/$f.mp4)" \
    "$(ffprobe -v error -select_streams v -show_entries stream=width,height,nb_frames -of csv=p=0 $C/$f.mp4)"
done
