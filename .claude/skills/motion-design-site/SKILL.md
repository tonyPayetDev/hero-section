---
name: motion-design-site
description: Workflow Zéro Code pour construire une landing page "Motion Design à 5000$" — page d'atterrissage futuriste dark-mode avec storytelling au scroll (scrollytelling). Le cœur est la technique du flipbook canvas : une séquence d'images (JPG/PNG) synchronisée à la molette via GSAP ScrollTrigger, pas une vidéo mp4. Génère les assets par IA (images clés → vidéo IA → séquence 30 FPS), échafaude le code front-end, câble la logique scroll, puis déploie. À utiliser dès qu'on demande un site animé au scroll, une landing premium futuriste, un effet flipbook/scrollytelling, ou "un site motion design".
---

## Charte — ne pas la redéfinir ici

**Lire `/work/autoboost-neon-videos/_shared/CHARTE.md` avant toute production.**
Palette, typographie, avatar, voix, musique, CTA et pièges de rendu y sont fixés
une seule fois. Ce skill ne redéclare aucune couleur.

**Fonds animés : piocher dans `_shared/broll-abstrait/` avant d’en créer un.**
Dix motifs existent — reseau, flux, grille, planetes, workflow, constellation,
onde, circuit, spirale, tunnel. Le README du dossier dit ce que chacun signifie.
N’en dessiner un nouveau que si aucun des dix ne dit ce qu’il faut dire.

# motion-design-site — Workflow Zéro Code (site Motion Design premium)

**Input :** une direction visuelle (références Pinterest/Dribbble/Awwwards, palette, sujet du projet) — ou juste un brief.
**Output :** un dossier de site statique autonome (`index.html` + `assets/` avec la séquence d'images numérotée) où le scroll pilote une animation image-par-image façon flipbook, prêt à déployer.

**Le secret à ne jamais oublier :** l'effet scrollytelling premium **n'est pas une vidéo `<video>`**. C'est une **séquence d'images** (`001.jpg`, `002.jpg`, …) dessinée dans un `<canvas>`, dont l'index avance proportionnellement à la position du scroll. La section héro est `sticky`/`fixed` sur `100vh` et l'utilisateur "scrolle à travers" l'animation. GSAP + ScrollTrigger orchestrent tout.

---

## Vue d'ensemble — les 6 étapes

1. **Inspiration & conception** — direction visuelle claire (refs + moodboard, maquette Figma optionnelle)
2. **Créer les assets** — images clés IA → vidéo IA → **séquence d'images 30 FPS** (le cœur du flipbook)
3. **Ingénierie du prompt** — le prompt masterclass qui sépare un site basique d'un site premium
4. **Génération du code front-end** — Claude produit la base HTML/Tailwind/GSAP
5. **Assemblage dans l'IDE** — câbler le scroll aux images (méthode de l'analogie flipbook)
6. **Publication** — déployer via `coolify-deploy` (convention de ce repo)

---

## Étape 1 — Inspiration & conception

L'IA a besoin d'une direction visuelle **précise**. Ne pars pas de zéro.

- **Références :** Pinterest, Dribbble, Awwwards → moodboards, interfaces futuristes, styles visuels.
- **Maquette (optionnel) :** structure de base dans Figma pour figer les zones de texte et d'animation. Si une maquette Figma existe, on peut l'importer dans le contexte IA via le skill `figma`.

**À collecter avant de coder :** palette hex, ambiance (dark absolu, néons…), typographies, sujet de l'animation qui va défiler au scroll (produit qui tourne, caméra qui traverse une scène, morphing…).

---

## Étape 2 — Créer les assets (le vrai secret du scroll)

La transition fluide au scroll = **une séquence d'images synchronisée à la molette**, pas un `.mp4`.

### 2a. Images clés (IA image)
Génère l'**image de début** et l'**image de fin** de l'animation avec un générateur d'images IA (Seedream/seedream-v4 via WaveSpeed, Kie.ai, Midjourney…). Garde la même composition/cadrage pour que la transition soit propre.

### 2b. Animation (IA vidéo)
Anime la transition entre les deux images clés avec une IA vidéo image→image (ex. modèle **start-end** vidu sur WaveSpeed — voir la recette de boucle vidéo en mémoire). Sortie : un court `.mp4` (2–5 s suffisent : au scroll, la durée réelle importe peu, seul le nombre d'images compte).

### 2c. Conversion en séquence d'images 30 FPS — **fais-le avec ffmpeg (pas un site en ligne)**
Le guide grand public dit "cherche un outil Video to JPG sequence en ligne". **Ici c'est inutile : `ffmpeg` est déjà présent dans le sandbox** (`/home/claude/tools/ffmpeg-build/…`, voir mémoire). On produit la séquence numérotée directement :

```bash
export PATH="/home/claude/tools/ffmpeg-build/ffmpeg-7.0.2-amd64-static:$PATH"
mkdir -p assets
# Extraire à 30 FPS, nommage séquentiel 001.jpg, 002.jpg, …
ffmpeg -i animation.mp4 -vf fps=30 -q:v 2 assets/%03d.jpg
# Compter les images générées (= la valeur FRAME_COUNT à mettre dans le JS)
ls assets/*.jpg | wc -l
```

- `-vf fps=30` = 30 images découpées par seconde de vidéo.
- `%03d.jpg` = numérotation à 3 chiffres (`001.jpg`…). **Retiens le nombre total** — c'est la constante à câbler à l'étape 5.
- Vise **~60 à 150 images** : assez pour être fluide, pas trop pour ne pas plomber le poids. Sur une vidéo longue, sous-échantillonne (`fps=15`) ou coupe (`-t`).
- **Optimise le poids** (une landing ne doit pas peser 40 Mo) : redimensionne au besoin (`-vf "fps=30,scale=1600:-1"`) et garde `-q:v 2..5`.

> Pour du 100 % IA (images → cinémagraphes → vidéo), le skill `foodboost-vitrine-video` documente déjà le pipeline WaveSpeed (seedream-v4 → vidu start-end) réutilisable ici pour produire l'animation source.

---

## Étape 3 — L'ingénierie du prompt (masterclass)

C'est la différence entre un site basique et un site premium. **Sois extrêmement spécifique** : marges, couleurs hex, typographies, intégration GSAP/ScrollTrigger, ambiance globale. Adapte les valeurs à l'étape 1.

Prompt de base réutilisable (à donner à Claude pour générer le squelette) :

```
Agis en tant que développeur front-end expert (niveau Awwwards).
Crée la structure d'une landing page futuriste pour <PROJET>.

DIRECTIVES DE DESIGN :
- Thème : Dark mode absolu (#050505), accents néon (violet #8b5cf6, bleu #3b82f6).
- Typographie : 'Inter' pour le corps, 'Syne' ou 'Space Grotesk' pour les titres.
- Style : Minimaliste, Glassmorphism, bordures très subtiles (border-white/10),
  beaucoup d'espace respirable (padding massif).

COMPORTEMENT & ANIMATION :
- Tailwind CSS via CDN.
- GSAP + ScrollTrigger inclus dans le <script>.
- La section Hero DOIT être sticky/fixed sur 100vh.
- Prévois un conteneur <canvas> plein écran pour une séquence d'images pilotée au scroll
  (je fournirai les images ; laisse un TODO pour brancher le flipbook).
- Reveals au scroll (fade/slide) sur les sections suivantes via ScrollTrigger.
```

> Pour la direction design (palettes, pairings de polices, styles), le skill `ui-ux-pro-max` complète ce prompt. Pour l'API GSAP scroll, voir `gsap-scrolltrigger`.

---

## Étape 4 — Génération du code front-end

Fais générer la base par Claude à partir du prompt de l'étape 3. Sortie attendue : un `index.html` autonome (Tailwind CDN + GSAP CDN + ScrollTrigger), une section héro `sticky h-screen` contenant un `<canvas>`, puis des sections de contenu avec reveals.

- **Astuce Figma :** si une maquette existe, utilise le skill `figma` (MCP) pour importer le design dans le contexte avant de générer, au lieu de décrire à l'aveugle.
- Garde tout **inline / CDN** : le site doit rester un dossier statique déployable tel quel.

---

## Étape 5 — Assemblage : câbler le scroll aux images (méthode flipbook)

C'est ici que l'animation rencontre le code. L'analogie du **flipbook (folioscope)** force une logique de scroll fluide et sans bug. Donne à Claude ce prompt, en remplaçant `FRAME_COUNT` par le nombre réel d'images comptées à l'étape 2c :

```
On crée une animation au scroll. Traite la page comme un Flipbook (folioscope :
un carnet dont les dessins s'animent quand on fait défiler les pages).

J'ai placé FRAME_COUNT images dans 'assets/', nommées '001.jpg' à
'0FR.jpg' (padding 3 chiffres). Logique attendue :
1. Au chargement, '001.jpg' est dessinée plein écran dans un <canvas>.
2. En scrollant vers le bas, on fait défiler les pages du flipbook de façon
   synchronisée : image 2, puis 3… proportionnellement à la position du scroll.
3. En scrollant vers le haut, l'animation s'inverse (ordre décroissant).
4. Le canvas garde ses proportions et couvre tout l'écran (object-fit: cover).
Fournis le JS qui lie la position de scroll à cette séquence, via GSAP + ScrollTrigger.
```

### Squelette de référence (le pattern à obtenir)

```html
<section id="hero" class="h-[400vh] relative">   <!-- longue piste de scroll -->
  <div class="sticky top-0 h-screen w-full">
    <canvas id="seq" class="w-full h-full"></canvas>
  </div>
</section>

<script>
gsap.registerPlugin(ScrollTrigger);

const canvas = document.getElementById('seq');
const ctx = canvas.getContext('2d');
const FRAME_COUNT = 120;                    // <-- valeur réelle (ls assets/*.jpg | wc -l)
const framePath = i => `assets/${String(i + 1).padStart(3, '0')}.jpg`;

function resize() { canvas.width = innerWidth; canvas.height = innerHeight; }
addEventListener('resize', () => { resize(); render(); });
resize();

// Précharge toutes les images (indispensable pour la fluidité)
const images = [];
let loaded = 0;
for (let i = 0; i < FRAME_COUNT; i++) {
  const img = new Image();
  img.src = framePath(i);
  img.onload = () => { if (++loaded === 1) render(); };
  images[i] = img;
}

const state = { frame: 0 };

function render() {
  const img = images[state.frame];
  if (!img || !img.complete) return;
  // object-fit: cover manuel
  const cw = canvas.width, ch = canvas.height;
  const r = Math.max(cw / img.width, ch / img.height);
  const w = img.width * r, h = img.height * r;
  ctx.clearRect(0, 0, cw, ch);
  ctx.drawImage(img, (cw - w) / 2, (ch - h) / 2, w, h);
}

gsap.to(state, {
  frame: FRAME_COUNT - 1,
  snap: 'frame',
  ease: 'none',
  scrollTrigger: {
    trigger: '#hero',
    start: 'top top',
    end: 'bottom bottom',
    scrub: 0.5           // lie la molette à la séquence (inverse au scroll haut inclus)
  },
  onUpdate: render
});
</script>
```

**Points de vigilance :**
- **Précharger** toutes les images avant/pendant le scroll, sinon ça saccade.
- `scrub` (pas une valeur fixe) = c'est lui qui rend le lien scroll↔image fluide et réversible.
- `snap: 'frame'` évite d'essayer d'afficher une image fractionnaire.
- La hauteur de la piste (`h-[400vh]`) règle la "vitesse" de l'animation : plus haut = défilement plus lent.
- Teste la fluidité avec le skill `playwright-skill` (scroll + screenshots) avant de déployer.

---

## Étape 6 — Publication (déploiement)

Convention de ce repo : **on déploie sur Coolify, pas Vercel/Netlify.**

1. Vérifie que le dossier est autonome (`index.html` + `assets/` + éventuel `style.css`), poids raisonnable.
2. Déploie avec le skill **`coolify-deploy`** (push GitHub `tonyPayetDev` → app Coolify → poll `running` → HTTP 200). Il crée un `Dockerfile` nginx minimal si absent.
3. (Optionnel) publier sur la route de **prévisualisation** pour validation au téléphone — voir les conventions de prévisualisation en mémoire.
4. Lie le domaine personnalisé côté Coolify si besoin.

> Le guide grand public cite Cloudflare Pages / Vercel / Netlify — ici, préfère toujours `coolify-deploy` (compte `tonyPayetDev`, instance Coolify du repo).

---

## Checklist de fin

- [ ] Direction visuelle figée (palette hex, typos, ambiance, sujet de l'animation)
- [ ] Images clés début/fin générées, animation IA produite
- [ ] Séquence `assets/001.jpg…` extraite à 30 FPS via ffmpeg, poids optimisé, **nombre d'images noté**
- [ ] `index.html` autonome : héro `sticky h-screen` + `<canvas>`, Tailwind + GSAP/ScrollTrigger en CDN
- [ ] Flipbook câblé : préchargement, `scrub`, `object-fit: cover`, réversible au scroll haut
- [ ] Fluidité vérifiée (playwright-skill)
- [ ] Déployé via `coolify-deploy`, HTTP 200 confirmé
