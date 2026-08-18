#!/usr/bin/env bash
export PATH="/home/claude/tools/node/bin:/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static:/home/claude/tools/chromelibs/usr/bin:$PATH"
export LD_LIBRARY_PATH="/home/claude/tools/chromelibs/lib/x86_64-linux-gnu:/home/claude/tools/chromelibs/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH"
export FONTCONFIG_PATH="/home/claude/tools/chromelibs/etc/fonts"
P=/work/autoboost-neon-videos/autoboost-hook-chaos
HF=/work/autoboost-neon-videos/veille-to-avatar-v3/node_modules/.bin/hyperframes
cd $P
echo "RENDER START $(date +%H:%M:%S)"
node "$HF" render public 2>&1 | tail -30
echo "RENDER EXIT ${PIPESTATUS[0]} $(date +%H:%M:%S)"
find $P -iname "*.mp4" -newermt "-30 min" 2>/dev/null
