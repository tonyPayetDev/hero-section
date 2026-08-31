#!/bin/sh
# B-roll « je suis réel » — time-lapse rapide à partir des vraies vidéos de Tony.
#
# Trois plans du 19 août 2026, remis dans l'ordre de la journée :
#   14 h 11 plage · 14 h 11 sous les arbres · 17 h 48 le port à l'heure dorée.
# L'arc de la journée fait le montage tout seul, il n'y a rien à inventer.
#
# Deux versions, parce qu'elles ne servent pas au même endroit :
#   reel-9x16.mp4  — pleine hauteur, à insérer dans une vidéo verticale
#   reel-16x9.mp4  — format d'origine, pour un montage paysage
#
# Pas de musique ici : c'est un ASSET. La musique se pose au montage final,
# sinon elle se superpose à celle de la vidéo hôte.
set -e
export PATH=/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static:$PATH
D=/work/autoboost-neon-videos/_shared/broll-reel
S=$D/source
W=$D/work
mkdir -p "$W"

VITESSE="${VITESSE:-4}"        # 4× → 18,92 s deviennent 4,7 s

# --- 1. Chaque plan accéléré, recadré, et légèrement relevé --------------------
# Le grade reste discret : ces images doivent avoir l'air vraies, pas retouchées.
# C'est tout l'intérêt du plan — s'il ressemble à une banque d'images, il ne
# prouve plus rien.
n=0
: > "$W/liste-9x16.txt"
: > "$W/liste-16x9.txt"
for f in "$S"/*.mp4; do
  n=$((n + 1))
  BASE=$(printf "%02d" "$n")

  # 9:16 — recadrage vertical centré, remonté d'un huitième pour garder
  # l'horizon et le ciel plutôt que le sable au premier plan.
  ffmpeg -nostdin -y -v error -i "$f" \
    -filter_complex "[0:v]setpts=PTS/${VITESSE},fps=30,\
crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920,setsar=1,\
eq=saturation=1.06:contrast=1.03,unsharp=3:3:0.4[v]" \
    -map "[v]" -an -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -r 30 \
    "$W/${BASE}-9x16.mp4"
  echo "file '$W/${BASE}-9x16.mp4'" >> "$W/liste-9x16.txt"

  ffmpeg -nostdin -y -v error -i "$f" \
    -filter_complex "[0:v]setpts=PTS/${VITESSE},fps=30,scale=1920:1080,setsar=1,\
eq=saturation=1.06:contrast=1.03,unsharp=3:3:0.4[v]" \
    -map "[v]" -an -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -r 30 \
    "$W/${BASE}-16x9.mp4"
  echo "file '$W/${BASE}-16x9.mp4'" >> "$W/liste-16x9.txt"

  echo "  plan $BASE  $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$W/${BASE}-9x16.mp4")s"
done

# --- 2. Assemblage ------------------------------------------------------------
for R in 9x16 16x9; do
  ffmpeg -nostdin -y -v error -f concat -safe 0 -i "$W/liste-$R.txt" \
    -c copy "$D/reel-$R.mp4"
  echo "  reel-$R : $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$D/reel-$R.mp4")s · $(du -h "$D/reel-$R.mp4" | cut -f1)"
done
