// Render every screen state to PNG in ONE browser session.
// FONTCONFIG_PATH is mandatory here or Chromium renders text invisible (known trap).
const CHROMELIBS = [
  '/home/claude/tools/chromelibs/usr/lib/x86_64-linux-gnu',
  '/home/claude/tools/chromelibs/lib/x86_64-linux-gnu',
].join(':');
process.env.LD_LIBRARY_PATH = CHROMELIBS + (process.env.LD_LIBRARY_PATH ? ':' + process.env.LD_LIBRARY_PATH : '');
process.env.FONTCONFIG_PATH = '/home/claude/tools/chromelibs/etc/fonts';

import fs from 'node:fs';
import pw from '/work/autoboost-neon-videos/autoboost-23-design/node_modules/playwright/index.js';
const { chromium } = pw;

const W = '/work/autoboost-neon-videos/autoboost-61-dix-questions/work';
const OUT = W + '/screens';
fs.mkdirSync(OUT, { recursive: true });
const FILE = 'file://' + W + '/screens.html';

const PROMPT_LEN = 90; // characters of the typed question

const states = [];
states.push('deux_a', 'deux_b');
// typewriter: one state every 3 characters
for (let n = 0; n <= PROMPT_LEN; n += 3) states.push('prompt_' + n);
states.push('prompt_' + PROMPT_LEN);
states.push('unepar_a', 'unepar_b');
states.push('split_l', 'split_r1', 'split_r2', 'split_r3');
states.push('endcard');
for (let n = 0; n <= 7; n++) states.push('cta_' + n);

const browser = await chromium.launch({ args: ['--no-sandbox', '--force-color-profile=srgb'] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });

let done = 0;
for (const s of states) {
  const strip = s.startsWith('cta');
  if (strip) await page.setViewportSize({ width: 1080, height: 340 });
  else await page.setViewportSize({ width: 1080, height: 1920 });
  // cache-busting query param: a hash-only change is a same-document navigation,
  // so the page would never re-run render() and every shot would be identical.
  await page.goto(`${FILE}?v=${done}#${s}`, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(60);
  await page.screenshot({
    path: `${OUT}/${s}.png`,
    omitBackground: strip,        // transparent strip so it can be overlaid
    clip: strip ? { x: 0, y: 0, width: 1080, height: 340 } : undefined,
  });
  done++;
}
await browser.close();
console.log(`captured ${done} states -> ${OUT}`);
