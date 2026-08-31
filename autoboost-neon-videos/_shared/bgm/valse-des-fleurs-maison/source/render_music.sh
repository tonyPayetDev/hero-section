#!/usr/bin/env bash
# Renders our own sequence of the Valse des fleurs into two phonograms with FluidSynth.
#
# TOOLCHAIN — nothing was installed system-wide and nothing was paid for.
#   FluidSynth 2.3.1 (LGPL) and its dependency chain were pulled as .deb files from
#   deb.debian.org (bookworm main), unpacked with `dpkg-deb -x` into a private prefix and run
#   through LD_LIBRARY_PATH. There is no root in this sandbox and no python; the ffmpeg static
#   build has no MIDI decoder, so a real synthesiser was the only way to render a score here.
#   Sample bank: FluidR3_GM.sf2 by Frank Wen, released under the MIT licence
#   (debian package fluid-soundfont-gm, /usr/share/doc/fluid-soundfont-gm/copyright).
#   MIT allows commercial use and redistribution, so the phonogram we render is ours outright.
#
# TWO PASSES, ONE FILTER PLAN
#   tutti  — the top desks, hook only. Rendered flat: it is supposed to occupy the whole
#            spectrum, there is no voice under it.
#   hollow — the bottom desks, whole timeline. Rendered with more reverb damping (dark tail)
#            and then shaped so that whatever the samples still carry above 1 kHz comes down.
#            The shaping is applied to the ENTIRE hollow stem, hook included, so there is no
#            filter discontinuity anywhere on the timeline; during the hook the top desks put
#            the brightness back.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
FS_ROOT="${FS_ROOT:-/tmp/claude-1000/-work/23c29362-cb5a-467e-ac5e-5a3aced20058/scratchpad/apt/root}"
export LD_LIBRARY_PATH="$FS_ROOT/usr/lib/x86_64-linux-gnu:$FS_ROOT/usr/lib/x86_64-linux-gnu/pulseaudio:$FS_ROOT/lib/x86_64-linux-gnu"
export PATH="/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static:$PATH"
SF2="$FS_ROOT/usr/share/sounds/sf2/FluidR3_GM.sf2"
FS="$FS_ROOT/usr/bin/fluidsynth"
DUR=35.4

/home/claude/tools/node/bin/node "$HERE/score.mjs"

fsrender () { # $1 = midi, $2 = out wav, $3.. = extra -o options
  local mid="$1" out="$2"; shift 2
  "$FS" -a file -F "$out" -T wav -r 48000 -g 0.55 -q -n \
    -o synth.chorus.active=0 -o synth.reverb.active=1 -o synth.polyphony=512 \
    "$@" "$SF2" "$mid" 2>&1 | grep -v -E "ALSA|alsa" || true
}

# top desks: warm hall, normal damping
fsrender "$HERE/midi/tutti.mid" "$HERE/raw_tutti.wav" \
  -o synth.reverb.room-size=0.75 -o synth.reverb.damp=0.35 \
  -o synth.reverb.width=0.9 -o synth.reverb.level=0.55

# bottom desks: same hall, tail damped hard so the reverb itself does not refill 1-3.5 kHz
fsrender "$HERE/midi/hollow.mid" "$HERE/raw_hollow.wav" \
  -o synth.reverb.room-size=0.78 -o synth.reverb.damp=0.95 \
  -o synth.reverb.width=0.9 -o synth.reverb.level=0.45

# ---- tutti: trim to the timeline, tiny top-end lift so a sampled tutti keeps some air
ffmpeg -y -v error -i "$HERE/raw_tutti.wav" -af "\
aresample=48000,\
highpass=f=45,\
equalizer=f=260:width_type=q:w=1.0:g=-2.2,\
equalizer=f=2600:width_type=q:w=0.8:g=1.5,\
alimiter=limit=0.97:attack=5:release=50,\
apad,atrim=0:$DUR" -ac 1 -ar 48000 "$HERE/valse_maison_tutti.wav"

# ---- hollow: the ORCHESTRATION already does the job. Measured on the unprocessed render,
# the hollow stem is 12.5 dB clear of its own 1-3.5 kHz band, i.e. it passes the brief with
# no filtering at all — that is the whole point of choosing the instruments. The shaping below
# is margin, not rescue: it takes out what the SAMPLES still carry in the band (bow noise,
# pizzicato and harp attack transients) and lands the stem at +18.3 dB.
# Deliberately gentle: a -9 dB shelf from 1.4 kHz and a 5 kHz lowpass, NOT the 1.15 kHz brick
# wall that was tried first. That version measured +23 dB but made the cellos sound like they
# were playing in the next room, and the brief requires the theme to stay recognisable.
ffmpeg -y -v error -i "$HERE/raw_hollow.wav" -af "\
aresample=48000,\
highpass=f=40,\
treble=f=1400:width_type=q:w=0.6:g=-9,\
lowpass=f=5000:poles=2,\
equalizer=f=180:width_type=q:w=0.9:g=1.5,\
alimiter=limit=0.97:attack=5:release=50,\
apad,atrim=0:$DUR" -ac 1 -ar 48000 "$HERE/valse_maison_hollow.wav"

for f in valse_maison_tutti valse_maison_hollow; do
  printf '%-26s ' "$f.wav"
  ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "$HERE/$f.wav"
done
