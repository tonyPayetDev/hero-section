// Genere des b-rolls abstraits animes, en boucle, aux couleurs de la marque.
// Reutilisables sur toutes les videos : c'est le point de reutilisabilite
// demande par Tony. Rendus en canvas puis assembles par ffmpeg.
//
// Palette reelle du site : jaune #eab308, violet #8b5cf6, fond #0a0a0f.
import pw from '/work/autoboost-neon-videos/autoboost-23-design/node_modules/playwright/index.js';
const { chromium } = pw;
import fs from 'fs';

process.env.LD_LIBRARY_PATH = [
  '/home/claude/tools/chromelibs/usr/lib/x86_64-linux-gnu',
  '/home/claude/tools/chromelibs/lib/x86_64-linux-gnu',
].join(':') + (process.env.LD_LIBRARY_PATH ? ':' + process.env.LD_LIBRARY_PATH : '');
process.env.FONTCONFIG_PATH = '/home/claude/tools/chromelibs/etc/fonts';

const BASE = '/work/autoboost-neon-videos/_shared/broll-abstrait';
const FRAMES = 240;                     // 8 s a 30 fps
const W = +(process.env.BW || 1920), H = +(process.env.BH || 1080);
const SUF = process.env.BSUF || "";     // "" = paysage, "-9x16" = vertical

// Chaque scene expose draw(ctx, p) ou p va de 0 a 1 : boucle parfaite garantie
// tant que draw(0) == draw(1). On s'appuie sur sin/cos de 2*PI*p.
const SCENES = {
  // Reseau qui respire — pour tout ce qui parle de graphe, de structure, de liens
  reseau: `
    const N=90, R=[];
    for(let i=0;i<N;i++){const a=i*2.399963;const r=Math.sqrt(i/N)*Math.min(${W},${H})*0.44;
      R.push({bx:${W}/2+Math.cos(a)*r, by:${H}/2+Math.sin(a)*r, ph:Math.random()*6.283, sp:0.6+Math.random()*0.9});}
    draw=(x,p)=>{
      x.fillStyle='#0a0a0f';x.fillRect(0,0,${W},${H});
      const T=p*6.283185;
      const P=R.map(n=>({x:n.bx+Math.cos(T*n.sp+n.ph)*17, y:n.by+Math.sin(T*n.sp*1.3+n.ph)*17}));
      x.lineWidth=1.1;
      for(let i=0;i<N;i++)for(let j=i+1;j<N;j++){
        const dx=P[j].x-P[i].x,dy=P[j].y-P[i].y,d=Math.hypot(dx,dy);
        if(d<175){const a=(1-d/175)*0.30;
          x.strokeStyle='rgba(234,179,8,'+a.toFixed(3)+')';
          x.beginPath();x.moveTo(P[i].x,P[i].y);x.lineTo(P[j].x,P[j].y);x.stroke();}}
      P.forEach((q,i)=>{const pu=0.5+0.5*Math.sin(T*1.7+R[i].ph);
        const r=2.2+pu*3.4;
        x.fillStyle= i%7===0 ? 'rgba(139,92,246,'+(0.55+pu*0.45).toFixed(3)+')'
                             : 'rgba(234,179,8,'+(0.40+pu*0.5).toFixed(3)+')';
        x.beginPath();x.arc(q.x,q.y,r,0,6.284);x.fill();});
    };`,

  // Flux de particules — pour tout ce qui parle de tokens, de cout, de lecture
  flux: `
    const N=420, R=[];
    for(let i=0;i<N;i++)R.push({y:Math.random()*${H}, o:Math.random(), v:0.35+Math.random()*0.9,
      l:40+Math.random()*190, w:Math.random()<0.14?2.1:1.0, vi:Math.random()<0.18});
    draw=(x,p)=>{
      x.fillStyle='#0a0a0f';x.fillRect(0,0,${W},${H});
      R.forEach(s=>{
        const t=(s.o+p*s.v)%1;
        const px=t*(${W}+s.l)-s.l;
        const g=x.createLinearGradient(px,0,px+s.l,0);
        const c= s.vi ? '139,92,246' : '234,179,8';
        g.addColorStop(0,'rgba('+c+',0)');
        g.addColorStop(0.55,'rgba('+c+',0.42)');
        g.addColorStop(1,'rgba('+c+',0)');
        x.strokeStyle=g;x.lineWidth=s.w;
        x.beginPath();x.moveTo(px,s.y);x.lineTo(px+s.l,s.y);x.stroke();});
    };`,

  // Grille en perspective qui defile — pour le depot, l'arborescence, l'echelle
  grille: `
    draw=(x,p)=>{
      x.fillStyle='#0a0a0f';x.fillRect(0,0,${W},${H});
      const hz=${H}*0.4;
      x.lineWidth=1;
      for(let i=-26;i<=26;i++){
        const gx=${W}/2+i*${W}*0.072;
        x.strokeStyle='rgba(234,179,8,0.15)';
        x.beginPath();x.moveTo(gx,${H});x.lineTo(${W}/2+i*${W}*0.0057,hz);x.stroke();}
      for(let k=0;k<22;k++){
        const t=((k+p)%22)/22;
        const y=hz+Math.pow(t,2.6)*(${H}-hz);
        const a=Math.min(0.34,Math.pow(t,1.5)*0.5);
        x.strokeStyle='rgba(139,92,246,'+a.toFixed(3)+')';
        x.beginPath();x.moveTo(0,y);x.lineTo(${W},y);x.stroke();}
      const g=x.createLinearGradient(0,hz-130,0,hz+150);
      g.addColorStop(0,'rgba(10,10,15,1)');g.addColorStop(1,'rgba(10,10,15,0)');
      x.fillStyle=g;x.fillRect(0,hz-130,${W},280);
    };`,
};

const browser = await chromium.launch({ args: ['--no-sandbox'] });
for (const [name, code] of Object.entries(SCENES)) {
  const dir = `${BASE}/${name}${SUF}`;
  fs.mkdirSync(dir, { recursive: true });
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  await page.setContent(`<!DOCTYPE html><html><head><meta charset="UTF-8">
    <style>*{margin:0;padding:0}body{background:#0a0a0f;overflow:hidden}canvas{display:block}</style>
    </head><body><canvas id="c" width="${W}" height="${H}"></canvas>
    <script>const X=document.getElementById('c').getContext('2d');let draw;${code}
    window.__f=(p)=>draw(X,p);</script></body></html>`);
  for (let i = 0; i < FRAMES; i++) {
    await page.evaluate((p) => window.__f(p), i / FRAMES);
    await page.screenshot({ path: `${dir}/f${String(i).padStart(4, '0')}.png` });
  }
  await page.close();
  console.log(`  ${name}${SUF} : ${FRAMES} frames`);
}
await browser.close();
