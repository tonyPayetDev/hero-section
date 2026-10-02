#!/usr/bin/env bash
# FaceCam Boost - tool setup. Source it: `source .claude/skills/face-cam-boost/scripts/env.sh`
# Works on Tony's machine (system ffmpeg) and in a Claude Code cloud container,
# where ffmpeg / whisper / Chrome headless shell are missing by default.
set -u
FCB_TOOLS="${FCB_TOOLS:-${TMPDIR:-/tmp}/fcb-tools}"
mkdir -p "$FCB_TOOLS/bin"

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "[fcb] ffmpeg absent -> ffmpeg-static via npm"
  (cd "$FCB_TOOLS" && npm install --silent ffmpeg-static ffprobe-static >/dev/null 2>&1)
  ln -sf "$FCB_TOOLS/node_modules/ffmpeg-static/ffmpeg" "$FCB_TOOLS/bin/ffmpeg"
  ln -sf "$FCB_TOOLS/node_modules/ffprobe-static/bin/linux/x64/ffprobe" "$FCB_TOOLS/bin/ffprobe"
  chmod +x "$FCB_TOOLS/bin/ffmpeg" "$FCB_TOOLS/bin/ffprobe"
  export PATH="$FCB_TOOLS/bin:$PATH"
fi
export FFMPEG="$(command -v ffmpeg)" FFPROBE="$(command -v ffprobe)"

python3 -c "import faster_whisper" 2>/dev/null || { echo "[fcb] pip install faster-whisper"; pip install --quiet faster-whisper; }

# HyperFrames renders with Chrome headless shell; reuse the Playwright one when present
if [ -z "${PRODUCER_HEADLESS_SHELL_PATH:-}" ]; then
  HS=$(ls -d /opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell 2>/dev/null | head -1)
  [ -n "$HS" ] && export PRODUCER_HEADLESS_SHELL_PATH="$HS"
fi
echo "[fcb] ffmpeg=$FFMPEG"
echo "[fcb] headless shell=${PRODUCER_HEADLESS_SHELL_PATH:-auto (npx hyperframes browser ensure)}"
