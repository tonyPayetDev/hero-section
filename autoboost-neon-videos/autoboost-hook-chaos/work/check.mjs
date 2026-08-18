const CHROMELIBS = ['/home/claude/tools/chromelibs/usr/lib/x86_64-linux-gnu','/home/claude/tools/chromelibs/lib/x86_64-linux-gnu'].join(':');
process.env.LD_LIBRARY_PATH = CHROMELIBS + (process.env.LD_LIBRARY_PATH ? ':' + process.env.LD_LIBRARY_PATH : '');
process.env.FONTCONFIG_PATH = '/home/claude/tools/chromelibs/etc/fonts';
import pw from '/work/autoboost-neon-videos/autoboost-23-design/node_modules/playwright/index.js';
const { chromium } = pw;
const DIR='/work/autoboost-neon-videos/autoboost-hook-chaos';
const browser = await chromium.launch({ args:['--no-sandbox'] });
const page = await browser.newPage({ viewport:{width:1080,height:1920,deviceScaleFactor:1} });
const errs=[];
page.on('console', m=>{ if(m.type()==='error') errs.push('CONSOLE '+m.text()); });
page.on('pageerror', e=>errs.push('PAGEERROR '+e.message));
await page.goto('file://'+DIR+'/public/index.html', { waitUntil:'load', timeout:30000 });
await page.waitForTimeout(1200);
const ok = await page.evaluate(()=> !!(window.__timelines && window.__timelines['hookchaos']));
console.log('timeline present:', ok, '| duration:', await page.evaluate(()=> window.__timelines?.['hookchaos']?.duration?.() ?? -1));
console.log('tiles:', await page.evaluate(()=> document.querySelectorAll('.ch-tile').length));
const TS = process.argv.slice(2).map(Number);
for (const t of TS){
  await page.evaluate((tt)=>{ const tl=window.__timelines['hookchaos']; tl.pause(); tl.time(tt); }, t);
  await page.waitForTimeout(120);
  await page.screenshot({ path: `${DIR}/work/check/t_${String(t).padStart(5,'0')}.png` });
}
console.log('ERRORS:', errs.length ? errs.slice(0,10) : 'none');
await browser.close();
