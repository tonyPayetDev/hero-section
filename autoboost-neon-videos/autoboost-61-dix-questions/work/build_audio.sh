#!/usr/bin/env bash
# Voice bed at absolute offsets + BGM ducked under the voice by sidechain + SFX on the beats.
# apad is ALWAYS bounded by atrim here — unbounded apad loops forever (paid trap).
set -e
export PATH="/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static:$PATH"
P=/work/autoboost-neon-videos/autoboost-61-dix-questions
W=$P/work; T=$W/tts/proc
SFX=/work/autoboost-neon-videos/_shared/sfx-palette/v1/assets
BGM=/work/autoboost-neon-videos/journal-ia-2026-08-17/public/assets/bgm.mp3
DUR=36.6

ffmpeg -y -v error \
 -i $T/t01.wav -i $T/t02.wav -i $T/t03.wav -i $T/t04.wav -i $T/t05.wav \
 -i $T/t06.wav -i $T/t07.wav -i $T/t08.wav -i $T/t09.wav \
 -stream_loop -1 -i $BGM \
 -i $SFX/sfx-whoosh-lat.mp3 -i $SFX/sfx-click-soft.mp3 -i $SFX/sfx-confirm.mp3 \
 -i $SFX/sfx-pop.mp3 -i $SFX/sfx-zoom.mp3 -i $SFX/sfx-impact.mp3 \
 -i $SFX/sfx-whoosh-v2.mp3 -i $SFX/sfx-chime-v2.mp3 \
 -filter_complex "\
 [0]adelay=400|400[v0];\
 [1]adelay=4130|4130[v1];\
 [2]adelay=9750|9750[v2];\
 [3]adelay=14700|14700[v3];\
 [4]adelay=17520|17520[v4];\
 [5]adelay=19200|19200[v5];\
 [6]adelay=22350|22350[v6];\
 [7]adelay=25320|25320[v7];\
 [8]adelay=30080|30080[v8];\
 [v0][v1][v2][v3][v4][v5][v6][v7][v8]amix=inputs=9:normalize=0:dropout_transition=0,\
   apad,atrim=0:$DUR,aresample=48000,volume=1.15[vox];\
 [vox]asplit=2[vox_main][vox_key];\
 [9]atrim=0:$DUR,aresample=48000,afade=t=in:st=0:d=1.2,afade=t=out:st=35.2:d=1.4[bgmraw];\
 [bgmraw][vox_key]sidechaincompress=threshold=0.03:ratio=8:attack=8:release=320,volume=0.34[bgmd];\
 [10]adelay=6900|6900,volume=0.24[s0];\
 [11]adelay=9760|9760,volume=0.20[s1];\
 [12]adelay=14300|14300,volume=0.22[s2];\
 [13]adelay=17500|17500,volume=0.22[s3];\
 [14]adelay=19200|19200,volume=0.20[s4];\
 [15]adelay=22333|22333,volume=0.30[s5];\
 [16]adelay=29367|29367,volume=0.26[s6];\
 [17]adelay=35000|35000,volume=0.22[s7];\
 [s0][s1][s2][s3][s4][s5][s6][s7]amix=inputs=8:normalize=0:dropout_transition=0,\
   apad,atrim=0:$DUR[sfxmix];\
 [vox_main][bgmd][sfxmix]amix=inputs=3:normalize=0:dropout_transition=0,\
   apad,atrim=0:$DUR,loudnorm=I=-15:TP=-1.5:LRA=11,\
   alimiter=limit=0.92:attack=5:release=60,apad,atrim=0:$DUR,aresample=48000[out]" \
 -map "[out]" -ac 2 -ar 48000 $W/final_audio.wav

# Voice-only bed — the lips gate must key off the VOICE, not the full mix.
# Keying off final_audio.wav makes BGM and SFX read as "someone is talking" and the
# gate then fires on deliberate silent beats.
ffmpeg -y -v error \
 -i $T/t01.wav -i $T/t02.wav -i $T/t03.wav -i $T/t04.wav -i $T/t05.wav \
 -i $T/t06.wav -i $T/t07.wav -i $T/t08.wav -i $T/t09.wav \
 -filter_complex "\
 [0]adelay=400|400[v0];[1]adelay=4130|4130[v1];[2]adelay=9750|9750[v2];\
 [3]adelay=14700|14700[v3];[4]adelay=17520|17520[v4];[5]adelay=19200|19200[v5];\
 [6]adelay=22350|22350[v6];[7]adelay=25320|25320[v7];[8]adelay=30080|30080[v8];\
 [v0][v1][v2][v3][v4][v5][v6][v7][v8]amix=inputs=9:normalize=0:dropout_transition=0,\
   apad,atrim=0:$DUR,aresample=48000[out]" \
 -map "[out]" -ac 1 -ar 48000 $W/voice_bed.wav

echo "final_audio: $(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 $W/final_audio.wav)"
echo "voice_bed:   $(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 $W/voice_bed.wav)"
ffmpeg -hide_banner -i $W/final_audio.wav -af "loudnorm=I=-16:TP=-1.5:print_format=summary" -f null - 2>&1 | grep -E "Input (Integrated|True Peak)"
