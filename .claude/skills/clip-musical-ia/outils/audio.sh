#!/bin/bash
# Monte la bande son : le morceau (80,8 s de fichier) devient 2 min 30 par une
# boucle musicale, pas par une répétition brute.
#
# Trois choses mesurées sur le fichier avant de couper quoi que ce soit :
#
#  1. La musique s'ARRÊTE à 78,88 s. Les 1,96 s suivantes sont du silence. Un
#     `-stream_loop -1` naïf collerait donc deux secondes de blanc au milieu
#     du clip.
#  2. Tempo dansé 83,3 BPM → beat 0,7175 s, mesure 2,87 s, et les vrais temps
#     forts tombent sur 6,40 + 2,87·k (relevé sur les pics d'énergie, pas
#     déduit d'un premier onset qui, lui, était décalé de 0,5 s).
#  3. L'intro (0 → 6 s) et le pont (8,9 → 12,1 s) sont CREUX : des fenêtres
#     entières à −44 dB. Y faire rentrer la boucle après un refrain à −12 dB
#     produit un trou qui s'entend comme « la chanson a redémarré ».
#
# D'où la rentrée à 7,835 s : c'est un demi-temps de mesure (6,40 + 2 beats),
# donc la phase du beat reste continue à la jointure — rien à rattraper au
# montage — et on repart sur le couplet en sautant la montée d'intro.
#
#   passe 1   0,000 → 78,880   morceau entier, jusqu'à sa vraie dernière note
#   passe 2   7,835 → 78,880   couplet → refrain → … → fin
#   total     149,87 s  (2 min 30)
set -e
export PATH="/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static:$PATH"
cd /work/clip-roule-kiki

FIN=78.88      # dernière note réelle du morceau
DEB2=7.835     # rentrée passe 2 — même phase de beat que FIN
XF=0.06        # fondu croisé court : le transitoire de grosse caisse le masque

ffmpeg -v error -y -i work/music.wav -t $FIN -c:a pcm_s16le work/p1.wav
ffmpeg -v error -y -i work/music.wav -ss $DEB2 -to $FIN -c:a pcm_s16le work/p2.wav

# acrossfade raccourcit le total de XF : 78,88 + 71,045 − 0,06 = 149,87 s.
ffmpeg -v error -y -i work/p1.wav -i work/p2.wav \
  -filter_complex "[0][1]acrossfade=d=$XF:c1=tri:c2=tri[m];[m]loudnorm=I=-14:TP=-1.5:LRA=11[o]" \
  -map "[o]" -ar 48000 -c:a pcm_s16le work/bande-son.wav

DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 work/bande-son.wav)
echo "bande-son.wav  ${DUR} s"
ffmpeg -v info -y -i work/bande-son.wav -af astats=metadata=1 -f null - 2>&1 \
  | grep -E "Peak level|RMS level" | head -4
