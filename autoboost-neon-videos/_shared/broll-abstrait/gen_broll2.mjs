// Banque de fonds animés — 7 nouveaux motifs, mêmes couleurs de marque.
// Jaune #eab308, violet #8b5cf6, fond #0a0a0f. Aucun vert.
//
// Chaque scène expose draw(ctx, p) avec p de 0 à 1. La boucle est parfaite
// tant que draw(0) == draw(1) : on n'utilise donc que sin/cos de 2*PI*p et des
// modulos sur p, jamais un compteur qui avance.
import pw from '/work/autoboost-neon-videos/autoboost-23-design/node_modules/playwright/index.js';
const { chromium } = pw;
import fs from 'fs';

process.env.LD_LIBRARY_PATH = [
  '/home/claude/tools/chromelibs/usr/lib/x86_64-linux-gnu',
  '/home/claude/tools/chromelibs/lib/x86_64-linux-gnu',
].join(':') + (process.env.LD_LIBRARY_PATH ? ':' + process.env.LD_LIBRARY_PATH : '');
process.env.FONTCONFIG_PATH = '/home/claude/tools/chromelibs/etc/fonts';

const BASE = '/work/autoboost-neon-videos/_shared/broll-abstrait';
const FRAMES = 240;                     // 8 s à 30 fps
const W = +(process.env.BW || 1920), H = +(process.env.BH || 1080);
const SUF = process.env.BSUF || '';     // '' = paysage, '-9x16' = vertical

const J = '234,179,8', V = '139,92,246';

const SCENES = {
  // 04 — Planètes en orbite. Pour tout ce qui parle d'écosystème, de gravité,
  // de « tout tourne autour de ». Demandé explicitement par Tony.
  planetes: `
    const N=7,O=[];
    for(let i=0;i<N;i++)O.push({r:120+i*98, sp:(i%2?1:-1)*(1+i*0.22), ph:i*0.9,
      rad:5+((i*3)%9), vi:i%3===0, tilt:0.34+i*0.05});
    draw=(x,p)=>{
      x.fillStyle='#0a0a0f';x.fillRect(0,0,${W},${H});
      const cx=${W}/2, cy=${H}/2, T=p*6.283185;
      O.forEach(o=>{
        x.strokeStyle='rgba(${J},0.10)';x.lineWidth=1;
        x.beginPath();x.ellipse(cx,cy,o.r,o.r*o.tilt,0,0,6.284);x.stroke();
      });
      // le soleil : halo net, pas un dégradé mou
      x.fillStyle='rgba(${J},0.95)';x.beginPath();x.arc(cx,cy,17,0,6.284);x.fill();
      x.strokeStyle='rgba(${J},0.28)';x.lineWidth=2;
      x.beginPath();x.arc(cx,cy,30,0,6.284);x.stroke();
      O.forEach(o=>{
        const a=T*o.sp+o.ph;
        const px=cx+Math.cos(a)*o.r, py=cy+Math.sin(a)*o.r*o.tilt;
        x.strokeStyle='rgba('+(o.vi?'${V}':'${J}')+',0.22)';x.lineWidth=1.2;
        x.beginPath();x.moveTo(cx,cy);x.lineTo(px,py);x.stroke();
        x.fillStyle='rgba('+(o.vi?'${V}':'${J}')+',0.92)';
        x.beginPath();x.arc(px,py,o.rad,0,6.284);x.fill();
        // une lune sur les planètes violettes
        if(o.vi){const b=a*3.1;
          x.fillStyle='rgba(${J},0.8)';
          x.beginPath();x.arc(px+Math.cos(b)*(o.rad+13),py+Math.sin(b)*(o.rad+13),2.4,0,6.284);x.fill();}
      });
    };`,

  // 05 — Workflow : des nœuds reliés dont les liaisons se tracent une par une,
  // puis un jeton parcourt le chemin. Le motif le plus proche de ce que fait n8n.
  workflow: `
    const NODES=[[0.14,0.5],[0.34,0.26],[0.34,0.74],[0.56,0.5],[0.76,0.28],[0.76,0.72],[0.92,0.5]];
    const EDGES=[[0,1],[0,2],[1,3],[2,3],[3,4],[3,5],[4,6],[5,6]];
    draw=(x,p)=>{
      x.fillStyle='#0a0a0f';x.fillRect(0,0,${W},${H});
      const P=NODES.map(n=>[n[0]*${W},n[1]*${H}]);
      EDGES.forEach((e,i)=>{
        // chaque liaison se trace sur sa propre fenêtre de temps, puis reste
        const t0=i/EDGES.length*0.55, t=Math.max(0,Math.min(1,(p-t0)/0.22));
        if(t<=0) return;
        const a=P[e[0]],b=P[e[1]];
        const mx=(a[0]+b[0])/2;
        x.strokeStyle='rgba(${J},0.5)';x.lineWidth=2;
        x.beginPath();x.moveTo(a[0],a[1]);
        x.bezierCurveTo(mx,a[1],mx,b[1],a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t);
        x.stroke();
      });
      // le jeton qui circule, une fois la structure posée
      if(p>0.6){
        const q=(p-0.6)/0.4;
        const seq=[0,1,3,4,6];
        const seg=Math.min(seq.length-2,Math.floor(q*(seq.length-1)));
        const lo=(q*(seq.length-1))-seg;
        const a=P[seq[seg]],b=P[seq[seg+1]];
        x.fillStyle='rgba(${V},1)';
        x.beginPath();x.arc(a[0]+(b[0]-a[0])*lo,a[1]+(b[1]-a[1])*lo,7,0,6.284);x.fill();
      }
      P.forEach((n,i)=>{
        const on=p>i/NODES.length*0.55;
        x.fillStyle=on?'rgba(${J},0.95)':'rgba(${J},0.2)';
        x.beginPath();x.arc(n[0],n[1],on?11:7,0,6.284);x.fill();
        if(on){x.strokeStyle='rgba(${V},0.55)';x.lineWidth=1.5;
          x.beginPath();x.arc(n[0],n[1],18,0,6.284);x.stroke();}
      });
    };`,

  // 06 — Constellation : des points se relient en figure puis se dispersent.
  // Pour « les pièces s'assemblent », la révélation d'un système.
  constellation: `
    const N=54,S=[];
    for(let i=0;i<N;i++){const a=i*2.399963,r=Math.sqrt(i/N);
      S.push({tx:0.5+Math.cos(a)*r*0.34, ty:0.5+Math.sin(a)*r*0.34,
        fx:Math.random(), fy:Math.random(), s:1.6+Math.random()*2.6, vi:i%6===0});}
    draw=(x,p)=>{
      x.fillStyle='#0a0a0f';x.fillRect(0,0,${W},${H});
      // aller-retour : rassemblement puis dispersion, boucle fermée
      const k=(1-Math.cos(p*6.283185))/2;
      const P=S.map(s=>[(s.fx+(s.tx-s.fx)*k)*${W},(s.fy+(s.ty-s.fy)*k)*${H}]);
      x.lineWidth=1;
      for(let i=0;i<N;i++)for(let j=i+1;j<N;j++){
        const dx=P[j][0]-P[i][0],dy=P[j][1]-P[i][1],d=Math.hypot(dx,dy);
        if(d<150){x.strokeStyle='rgba(${J},'+((1-d/150)*0.30*k).toFixed(3)+')';
          x.beginPath();x.moveTo(P[i][0],P[i][1]);x.lineTo(P[j][0],P[j][1]);x.stroke();}
      }
      P.forEach((q,i)=>{x.fillStyle=S[i].vi?'rgba(${V},'+(0.4+0.6*k).toFixed(2)+')':'rgba(${J},'+(0.35+0.6*k).toFixed(2)+')';
        x.beginPath();x.arc(q[0],q[1],S[i].s,0,6.284);x.fill();});
    };`,

  // 07 — Ondes concentriques. Pour la portée, la diffusion, « ça se propage ».
  onde: `
    draw=(x,p)=>{
      x.fillStyle='#0a0a0f';x.fillRect(0,0,${W},${H});
      const cx=${W}/2, cy=${H}/2, MAX=Math.hypot(${W},${H})/2;
      for(let k=0;k<9;k++){
        const t=((p+k/9)%1);
        const r=t*MAX;
        const a=Math.max(0,(1-t)*0.42);
        x.strokeStyle=(k%3===0?'rgba(${V},':'rgba(${J},')+a.toFixed(3)+')';
        x.lineWidth=2.2-t*1.4;
        x.beginPath();x.arc(cx,cy,r,0,6.284);x.stroke();
      }
      x.fillStyle='rgba(${J},0.9)';x.beginPath();x.arc(cx,cy,9,0,6.284);x.fill();
    };`,

  // 08 — Circuit imprimé : des pistes orthogonales qui s'allument par tronçon.
  // Pour tout ce qui parle d'infrastructure, de « sous le capot ».
  circuit: `
    const L=[];const G=64;
    for(let i=0;i<26;i++){
      let x0=Math.floor(Math.random()*(${W}/G))*G, y0=Math.floor(Math.random()*(${H}/G))*G;
      const pts=[[x0,y0]];
      for(let s=0;s<5;s++){
        if(Math.random()<0.5) x0+=(Math.random()<0.5?-1:1)*G*(1+Math.floor(Math.random()*3));
        else y0+=(Math.random()<0.5?-1:1)*G*(1+Math.floor(Math.random()*3));
        pts.push([x0,y0]);
      }
      L.push({pts, off:Math.random(), vi:i%5===0});
    }
    draw=(x,p)=>{
      x.fillStyle='#0a0a0f';x.fillRect(0,0,${W},${H});
      x.lineCap='round';
      L.forEach(l=>{
        const t=(p+l.off)%1;
        const glow=Math.max(0,1-Math.abs(t-0.5)*2.6);
        x.strokeStyle=(l.vi?'rgba(${V},':'rgba(${J},')+(0.07+glow*0.55).toFixed(3)+')';
        x.lineWidth=1.4+glow*2.2;
        x.beginPath();x.moveTo(l.pts[0][0],l.pts[0][1]);
        l.pts.slice(1).forEach(q=>x.lineTo(q[0],q[1]));
        x.stroke();
        l.pts.forEach(q=>{x.fillStyle=(l.vi?'rgba(${V},':'rgba(${J},')+(0.1+glow*0.6).toFixed(3)+')';
          x.beginPath();x.arc(q[0],q[1],2.6+glow*2,0,6.284);x.fill();});
      });
    };`,

  // 09 — Spirale de points. Pour la montée en puissance, l'accumulation.
  spirale: `
    const N=260;
    draw=(x,p)=>{
      x.fillStyle='#0a0a0f';x.fillRect(0,0,${W},${H});
      const cx=${W}/2, cy=${H}/2, T=p*6.283185;
      for(let i=0;i<N;i++){
        const f=i/N;
        const a=f*15.5+T;
        const r=f*Math.min(${W},${H})*0.46;
        const px=cx+Math.cos(a)*r, py=cy+Math.sin(a)*r;
        const s=1+f*4.2;
        x.fillStyle=(i%9===0?'rgba(${V},':'rgba(${J},')+(0.15+f*0.7).toFixed(3)+')';
        x.beginPath();x.arc(px,py,s,0,6.284);x.fill();
      }
    };`,

  // 10 — Tunnel : des cadres qui foncent vers le spectateur. Pour l'avancée,
  // le « on entre dedans », les transitions de fin.
  tunnel: `
    draw=(x,p)=>{
      x.fillStyle='#0a0a0f';x.fillRect(0,0,${W},${H});
      const cx=${W}/2, cy=${H}/2;
      for(let k=13;k>=0;k--){
        const t=((p+k/14)%1);
        const z=Math.pow(t,2.2);
        const w=z*${W}*1.5, h=z*${H}*1.5;
        const a=Math.max(0,(1-t)*0.5);
        x.strokeStyle=(k%4===0?'rgba(${V},':'rgba(${J},')+a.toFixed(3)+')';
        x.lineWidth=1+z*2.4;
        x.strokeRect(cx-w/2,cy-h/2,w,h);
      }
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
