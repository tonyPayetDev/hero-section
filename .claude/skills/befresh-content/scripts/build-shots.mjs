// Render every shot of the BeFresh x Decathlon reel as a normalized 1080x1920 @30fps clip,
// then concat them. Punch-in / ken-burns via zoompan on a 2x upscale (sharp, no black bars).
import fs from 'node:fs';
import { execFileSync } from 'node:child_process';

const cfg = JSON.parse(fs.readFileSync('src/shots.json', 'utf8'));
const FPS = cfg.fps;
const OUT = 'work/shots';
fs.mkdirSync(OUT, { recursive: true });

const sh = (args) => execFileSync('ffmpeg', args, { stdio: ['ignore', 'pipe', 'pipe'] });

let total = 0;
const list = [];

for (const s of cfg.shots) {
  const N = Math.round(s.dur * FPS);          // output frames
  const srcDur = s.dur * s.spd;               // seconds consumed from the source
  const src = cfg.sources[s.src];
  const isPhoto = s.src === 'P';

  // zoompan: input is 2160x3840, output window is (iw/zoom x ih/zoom) re-scaled to 1080x1920
  const z = `${s.z0}+(${s.z1}-${s.z0})*on/${Math.max(1, N - 1)}`;
  const x = `max(0\\,min(iw-iw/zoom\\,${s.cx}*iw-iw/zoom/2))`;
  const y = `max(0\\,min(ih-ih/zoom\\,${s.cy}*ih-ih/zoom/2))`;
  const zp = `zoompan=z='${z}':x='${x}':y='${y}':d=1:s=1080x1920:fps=${FPS}`;

  // "fresh food" grade: lift, punchier contrast, vivid fruit colours
  const GRADE = isPhoto
    ? 'eq=contrast=1.16:saturation=1.30:brightness=0.005:gamma=1.03'  // photo is hazier
    : 'eq=contrast=1.09:saturation=1.32:brightness=0.018:gamma=1.02';

  let vf, pre;
  if (isPhoto) {
    pre = ['-loop', '1', '-t', String(s.dur), '-i', src];
    vf = `scale=2160:3840:flags=lanczos,setsar=1,fps=${FPS},${zp},${GRADE},setsar=1,format=yuv420p`;
  } else {
    pre = ['-ss', String(s.ss), '-t', String(srcDur + 0.15), '-i', src];
    const speed = s.spd !== 1 ? `setpts=PTS/${s.spd},` : '';
    vf = `${speed}fps=${FPS},scale=2160:3840:flags=lanczos,setsar=1,${zp},${GRADE},setsar=1,format=yuv420p`;
  }

  const out = `${OUT}/${s.id}.mp4`;
  sh(['-v', 'error', ...pre, '-vf', vf, '-frames:v', String(N),
      '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p',
      '-r', String(FPS), '-an', out, '-y']);

  const got = execFileSync('ffprobe', ['-v', 'error', '-select_streams', 'v:0',
    '-count_frames', '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', out])
    .toString().trim();
  if (Number(got) !== N) console.warn(`  !! ${s.id}: expected ${N} frames, got ${got}`);

  console.log(`${s.id} ${String(s.dur.toFixed(2)).padStart(5)}s  z${s.z0}->${s.z1}  spd${s.spd}  ${got}f  ${s.note}`);
  list.push(`file '${s.id}.mp4'`);
  total += s.dur;
}

fs.writeFileSync(`${OUT}/list.txt`, list.join('\n') + '\n');
sh(['-v', 'error', '-f', 'concat', '-safe', '0', '-i', `${OUT}/list.txt`,
    '-c', 'copy', 'work/video-silent.mp4', '-y']);

const d = execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', 'work/video-silent.mp4']).toString().trim();
console.log(`\n${cfg.shots.length} shots | planned ${total.toFixed(2)}s | actual ${d}s | avg ${(total / cfg.shots.length).toFixed(2)}s/shot`);
