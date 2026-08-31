import fs from 'fs';
import path from 'path';
import { CFGS } from './configs.mjs';
import { buildHtml } from './build-lib.mjs';

const ROOT = '/work/autoboost-neon-videos';
const DUR = {
  'autoboost-56-prompt-reveal-01-regard': 27.3,
  'autoboost-56-prompt-reveal-02-burger': 28.0,
  'autoboost-56-prompt-reveal-03-shonen': 27.8,
  'autoboost-56-prompt-reveal-04-neon': 25.3,
  'autoboost-56-prompt-reveal-05-combat': 27.5,
};

for (const cfg of CFGS) {
  cfg.dur = DUR[cfg.dir];
  const out = path.join(ROOT, cfg.dir, 'public', 'index.html');
  fs.writeFileSync(out, buildHtml(cfg));
  const sh = `#!/usr/bin/env bash
export PATH="/home/claude/tools/node/bin:/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static:/home/claude/tools/chromelibs/usr/bin:$PATH"
export LD_LIBRARY_PATH="/home/claude/tools/chromelibs/lib/x86_64-linux-gnu:/home/claude/tools/chromelibs/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH"
export FONTCONFIG_PATH="/home/claude/tools/chromelibs/etc/fonts"
HF="/work/autoboost-neon-videos/autoboost-seedance-tuto/node_modules/.bin/hyperframes"
cd ${ROOT}/${cfg.dir}
echo "RENDER START ${cfg.dir} $(date +%H:%M:%S)"
node "$HF" render public 2>&1
echo "RENDER EXIT $? $(date +%H:%M:%S)"
`;
  fs.writeFileSync(path.join(ROOT, cfg.dir, 'render.sh'), sh, { mode: 0o755 });
  console.log('OK', cfg.dir, cfg.dur + 's', cfg.keyword);
}
