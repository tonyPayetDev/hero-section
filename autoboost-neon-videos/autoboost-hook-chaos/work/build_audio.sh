#!/usr/bin/env bash
set -e
export PATH="/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static:$PATH"
W=/work/autoboost-neon-videos/autoboost-hook-chaos/work
T=$W/tts/proc
A=/work/autoboost-neon-videos/autoboost-hook-chaos/public/assets
DUR=34.6

# ---------- 1) VOICE bed (rien avant 10.55 s : le hook reste muet) ----------
ffmpeg -y -v error \
 -i $T/s01.wav -i $T/s02.wav -i $T/s03.wav -i $T/s04.wav -i $T/s05.wav -i $T/s06.wav \
 -filter_complex "\
 [0]adelay=10550|10550[a0];\
 [1]adelay=14600|14600[a1];\
 [2]adelay=20250|20250[a2];\
 [3]adelay=24750|24750[a3];\
 [4]adelay=26800|26800[a4];\
 [5]adelay=30200|30200[a5];\
 [a0][a1][a2][a3][a4][a5]amix=inputs=6:normalize=0:dropout_transition=0,\
 apad,atrim=0:$DUR,aresample=48000[v]" \
 -map "[v]" -ac 1 -ar 48000 $W/voice_bed.wav

# ---------- 2) BGM bouclee, duckee en sidechain, +6 dB pendant le hook ----------
ffmpeg -y -v error -stream_loop -1 -t $DUR -i $A/bgm.mp3 -i $W/voice_bed.wav \
 -filter_complex "\
 [0:a]volume=0.9,aresample=48000[bg];\
 [1:a]aresample=48000,asplit[vc][sc];\
 [bg][sc]sidechaincompress=threshold=0.03:ratio=8:attack=8:release=320:makeup=1[bgd];\
 [bgd]volume=0.34[bgl];\
 [bgl]volume=volume='if(lt(t,9.6),1.9,if(lt(t,10.5),1.9-(t-9.6)*1.0,1.0))':eval=frame[bgm];\
 [vc]volume=1.0[voc];\
 [voc][bgm]amix=inputs=2:normalize=0:dropout_transition=0,atrim=0:$DUR,dynaudnorm=f=250:g=7[mix]" \
 -map "[mix]" -ac 2 -ar 48000 $W/bed_music.wav

# ---------- 3) SFX ----------
# HOOK : whoosh 0.20 (montee du chaos) / IMPACT 2.00 (freeze) / click 5.40 / confirm 6.60
#        >>> RIEN entre 2.2 s et 3.8 s : le silence visuel est aussi sonore <<<
ffmpeg -y -v error \
 -i $W/bed_music.wav \
 -i $A/sfx-whoosh-v2.mp3 -i $A/sfx-impact.mp3 -i $A/sfx-click.mp3 -i $A/sfx-confirm.mp3 \
 -i $A/sfx-notify.mp3 -i $A/sfx-pop.mp3 -i $A/sfx-confirm.mp3 -i $A/sfx-impact.mp3 \
 -i $A/sfx-pop.mp3 -i $A/sfx-impact.mp3 \
 -filter_complex "\
 [1]adelay=200|200,volume=0.14[s1];\
 [2]adelay=2000|2000,volume=0.36[s2];\
 [3]adelay=5400|5400,volume=0.26[s3];\
 [4]adelay=6600|6600,volume=0.24[s4];\
 [5]adelay=14500|14500,volume=0.15[s5];\
 [6]adelay=22300|22300,volume=0.17[s6];\
 [7]adelay=25050|25050,volume=0.22[s7];\
 [8]adelay=28150|28150,volume=0.20[s8];\
 [9]adelay=31750|31750,volume=0.17[s9];\
 [10]adelay=33050|33050,volume=0.28[s10];\
 [0][s1][s2][s3][s4][s5][s6][s7][s8][s9][s10]amix=inputs=11:normalize=0:dropout_transition=0,atrim=0:$DUR,aresample=48000[out]" \
 -map "[out]" -ac 2 -ar 48000 $W/final_audio.wav
echo "final_audio: $(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 $W/final_audio.wav)"
