#!/usr/bin/env node
/**
 * gen_ffmpeg.mjs <mode> <projectDir>
 *
 *   audio  -> writes work/build_audio.sh   (voice bed + sidechain-ducked BGM + SFX)
 *   pass2  -> writes work/pass2.sh         (avatar overlays + final mux)
 *
 * The filter graphs are generated from timing.json / avatar_windows.json, so the
 * number of segments, gags and avatar windows is free.
 */
import fs from 'node:fs';
import path from 'node:path';

const [, , MODE, P] = process.argv;
if (!MODE || !P) { console.error('usage: gen_ffmpeg.mjs <audio|pass2> <projectDir>'); process.exit(2); }

const W = path.join(P, 'work');
const A = path.join(P, 'public', 'assets');
const T = path.join(W, 'tts', 'proc');
const tm = JSON.parse(fs.readFileSync(path.join(W, 'timing.json'), 'utf8'));
const ed = JSON.parse(fs.readFileSync(path.join(W, 'edition.json'), 'utf8'));
const DUR = tm.duration;
const ids = ed.segments.map((s) => s.id).filter((id) => tm.start[id] !== undefined);

const HEAD = `#!/usr/bin/env bash
set -euo pipefail
export PATH="\${FFMPEG_DIR:-/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static}:$PATH"
`;

if (MODE === 'audio') {
  /* ---- 1. voice bed: every segment placed at its absolute offset ---- */
  const inputs = ids.map((id) => `-i ${T}/${id}.wav`).join(' \\\n ');
  const delays = ids.map((id, i) => `[${i}]adelay=${Math.round(tm.start[id] * 1000)}|${Math.round(tm.start[id] * 1000)}[a${i}];`).join('\\\n ');
  const mixIn = ids.map((_, i) => `[a${i}]`).join('');

  /* ---- 3. SFX: whoosh on each visual change, impacts on the countdown ---- */
  const sfx = [];
  sfx.push({ f: 'sfx-whoosh-v2.mp3', t: Math.max(0, tm.start[ids[0]] - 0.2), v: 0.16 });
  for (const s of ed.segments) {
    if (tm.start[s.id] === undefined) continue;
    if (s.role === 'brief') sfx.push({ f: 'sfx-pop.mp3', t: Math.max(0, tm.start[s.id] - 0.16), v: 0.18 });
    if (s.role === 'gag') sfx.push({ f: 'sfx-notify.mp3', t: Math.max(0, tm.start[s.id] - 0.1), v: 0.18 });
  }
  if (tm.start.cd !== undefined) {
    const step = tm.dur.cd / 3;
    for (let i = 0; i < 3; i++) sfx.push({ f: 'sfx-impact.mp3', t: tm.start.cd + 0.03 + i * step, v: 0.26 });
  }
  if (tm.start.tag !== undefined) sfx.push({ f: 'sfx-impact.mp3', t: tm.start.tag - 0.02, v: 0.30 });

  const sfxIn = sfx.map((s) => `-i ${A}/${s.f}`).join(' \\\n ');
  const sfxF = sfx.map((s, i) => `[${i + 1}]adelay=${Math.round(s.t * 1000)}|${Math.round(s.t * 1000)},volume=${s.v}[s${i}];`).join('\\\n ');
  const sfxMix = sfx.map((_, i) => `[s${i}]`).join('');

  fs.writeFileSync(path.join(W, 'build_audio.sh'), `${HEAD}
# ---------- 1) VOICE bed ----------
ffmpeg -y -v error \\
 ${inputs} \\
 -filter_complex "\\
 ${delays}\\
 ${mixIn}amix=inputs=${ids.length}:normalize=0:dropout_transition=0,\\
 apad=whole_dur=${DUR},atrim=0:${DUR},aresample=48000[v]" \\
 -map "[v]" -t ${DUR} -ac 1 -ar 48000 ${W}/voice_bed.wav

# ---------- 2) BGM looped + ducked under the voice (sidechain) ----------
ffmpeg -y -v error -stream_loop -1 -t ${DUR} -i ${A}/bgm.mp3 -i ${W}/voice_bed.wav \\
 -filter_complex "\\
 [0:a]volume=0.9,aresample=48000[bg];\\
 [1:a]aresample=48000,asplit[vc][sc];\\
 [bg][sc]sidechaincompress=threshold=0.03:ratio=8:attack=8:release=320:makeup=1[bgd];\\
 [bgd]volume=0.34[bgm];\\
 [vc]volume=1.0[voc];\\
 [voc][bgm]amix=inputs=2:normalize=0:dropout_transition=0,atrim=0:${DUR},dynaudnorm=f=250:g=7[mix]" \\
 -map "[mix]" -t ${DUR} -ac 2 -ar 48000 ${W}/bed_music.wav

# ---------- 3) SFX layer ----------
ffmpeg -y -v error \\
 -i ${W}/bed_music.wav \\
 ${sfxIn} \\
 -filter_complex "\\
 ${sfxF}\\
 [0]${sfxMix}amix=inputs=${sfx.length + 1}:normalize=0:dropout_transition=0,atrim=0:${DUR},aresample=48000,loudnorm=I=-14:TP=-1.5:LRA=11[out]" \\
 -map "[out]" -t ${DUR} -ac 2 -ar 48000 ${W}/final_audio.wav

ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 ${W}/final_audio.wav
`);
  console.error(`[gen_ffmpeg] build_audio.sh · ${ids.length} segments · ${sfx.length} SFX`);
}

if (MODE === 'pass2') {
  const wins = JSON.parse(fs.readFileSync(path.join(W, 'avatar_windows.json'), 'utf8'));
  const C = path.join(W, 'clips');
  const inputs = wins.map((w, i) => `-i ${C}/${w.id}.mp4`).join(' \\\n ');
  let chain = '';
  let prev = '[0:v]';
  wins.forEach((w, i) => {
    const out = i === wins.length - 1 ? '[vout]' : `[b${i}]`;
    chain += `[${i + 1}:v]scale=642:1146,setpts=PTS-STARTPTS+${w.in.toFixed(3)}/TB[o${i}];\\\n `;
    chain += `${prev}[o${i}]overlay=219:153:enable='between(t,${w.in.toFixed(3)},${w.out.toFixed(3)})'${out};\\\n `;
    prev = out;
  });
  chain = chain.replace(/;\\\n $/, '');

  fs.writeFileSync(path.join(W, 'pass2.sh'), `${HEAD}
BASE="\${1:-}"
[ -z "$BASE" ] && BASE=$(find ${P}/renders ${P}/public/renders -iname '*.mp4' 2>/dev/null | sort | tail -1)
[ -z "$BASE" ] && { echo "pass2: aucun rendu de base trouvé"; exit 1; }
echo "BASE=$BASE"

ffmpeg -y -v error \\
 -i "$BASE" \\
 ${inputs} \\
 -i ${W}/final_audio.wav \\
 -filter_complex "\\
 ${chain}" \\
 -map "[vout]" -map "${wins.length + 1}:a" \\
 -t ${DUR} \\
 -c:v libx264 -pix_fmt yuv420p -crf 19 -preset medium \\
 -c:a aac -b:a 192k -movflags +faststart \\
 ${P}/public/video.mp4

ffprobe -v error -show_entries format=duration -show_entries stream=codec_type,width,height -of default=nk=1 ${P}/public/video.mp4
`);

  /* avatar clip prep, cycling the reusable bank */
  const BANK = process.env.JIA_AVATAR_BANK || '/work/autoboost-neon-videos/_shared/avatar-bank/clips';
  const bank = fs.readdirSync(BANK).filter((f) => f.endsWith('.mp4')).sort();
  const roleClip = (id) => {
    if (id === 'cta') return bank.find((f) => /commente|motcle|cta/i.test(f)) || bank[bank.length - 1];
    if (id === 'intro') return bank.find((f) => /hook|frontal/i.test(f)) || bank[0];
    return bank.find((f) => /principe|explication/i.test(f)) || bank[1 % bank.length];
  };
  const lines = wins.map((w, i) => {
    const src = roleClip(w.id);
    const d = +(w.out - w.in + 0.15).toFixed(2);
    const ss = (0.4 + (i % 3) * 0.5).toFixed(2);
    return `ffmpeg -y -v error -stream_loop -1 -ss ${ss} -t ${d} -i ${BANK}/${src} -an \\
 -vf "scale=648:1152:force_original_aspect_ratio=increase,crop=648:1152,setsar=1,fps=30" \\
 -c:v libx264 -pix_fmt yuv420p -crf 18 ${C}/${w.id}.mp4`;
  }).join('\n');

  fs.writeFileSync(path.join(W, 'prep_clips.sh'), `${HEAD}
mkdir -p ${C}
${lines}
for f in ${C}/*.mp4; do echo "$(basename $f) $(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 $f)"; done
`);
  console.error(`[gen_ffmpeg] pass2.sh + prep_clips.sh · ${wins.length} fenêtres avatar`);
}
