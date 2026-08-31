// La table de montage : quel plan tombe sur quelle mesure, et comment il est traité.
//
// Elle n'est pas écrite à l'oreille. Elle est dérivée de `structure.json`,
// c'est-à-dire de la carte du morceau mesurée sur le fichier — refrain,
// couplet, break — recalée sur la boucle construite par `audio.sh`.
//
// La règle qui décide de tout, et qui vient mot pour mot de la demande :
//
//   « la music doit suivre l'avatar quand il chante »
//        → sur un bloc CHANTÉ, on ne montre que des plans où sa bouche bouge
//          (micro à la main ou gros plan qui crie). Jamais un plan de dos,
//          jamais une danseuse seule. Rien ne trahit plus vite un clip que
//          la voix qui continue pendant qu'on regarde autre chose.
//
//   « effets de saut d'écran stylé quand il ne chante pas »
//        → sur un bloc INSTRU, le montage passe au demi-temps (1,43 s au lieu
//          de 2,87 s) et le traitement `saut` prend la main.
//
// Les points d'entrée/sortie de chaque plan ont été relevés image par image
// sur les six clips (planches-contact dans work/detail/), pas devinés.

export const CLIPS = {
  c1: 'work/clips/c1--vGOyNIgEGg.mp4',   // 1280x720 — scène, foule, micro
  c2: 'work/clips/c2-slCLZzCem_I.mp4',   // 720x1280 — rue néon, orbe au doigt
  c3: 'work/clips/c3-pFzYUF-f5V8.mp4',   // 720x1280 — mimi lela, micro, scène
  c4: 'work/clips/c4-p_-_X1eZgAA.mp4',   // 720x1280 — duo qui danse (0 chant)
  c5: 'work/clips/c5-S1u-u9N5hjE.mp4',   // 720x1280 — voiture, kart au chat
  c6: 'work/clips/c6-NXfhfMCslpY.mp4',   // 720x1280 — très gros plans, orbe
};

// c1 est le seul plan large. Le recadrer en portrait au centre couperait la
// tête ou le micro selon la seconde : chaque extrait porte donc son propre
// décalage horizontal, relevé sur la grille (work/c1/grille.jpg).
export const PLANS = {
  // ---- CHANTÉ : bouche visible, micro ou cri -------------------------------
  SC1:  { clip: 'c1', t0: 2.60, t1: 4.20, cadre: { type: 'portrait16', x: 387 } },
  SC2:  { clip: 'c1', t0: 4.30, t1: 5.60, cadre: { type: 'portrait16', x: 220 } }, // le meilleur gros plan chanté des six clips
  SC3:  { clip: 'c1', t0: 8.40, t1: 9.95, cadre: { type: 'portrait16', x: 438 } },
  SC4:  { clip: 'c3', t0: 2.10, t1: 3.60 },
  SC5:  { clip: 'c3', t0: 3.90, t1: 5.00 },
  SC6:  { clip: 'c3', t0: 7.10, t1: 9.95 },
  SC7:  { clip: 'c6', t0: 1.40, t1: 3.00 },
  SC8:  { clip: 'c6', t0: 3.00, t1: 4.10 },
  SC9:  { clip: 'c2', t0: 1.30, t1: 2.50 },
  SC10: { clip: 'c2', t0: 3.40, t1: 5.50 },
  SC11: { clip: 'c2', t0: 5.50, t1: 7.40 },
  SC12: { clip: 'c2', t0: 8.90, t1: 9.95 },

  // ---- INSTRU : danse, voiture, inserts ------------------------------------
  IN1:  { clip: 'c4', t0: 0.00, t1: 2.00 },
  IN2:  { clip: 'c4', t0: 2.00, t1: 4.00 },
  IN3:  { clip: 'c4', t0: 4.80, t1: 6.90 },   // filés — le plan le plus glitchable
  IN4:  { clip: 'c4', t0: 7.00, t1: 9.95 },
  IN5:  { clip: 'c5', t0: 0.00, t1: 2.00 },
  IN6:  { clip: 'c5', t0: 2.00, t1: 3.10 },   // roue / drift
  IN7:  { clip: 'c5', t0: 3.10, t1: 5.90 },
  IN8:  { clip: 'c5', t0: 5.90, t1: 9.00 },   // le chat dans le kart — le plan qu'on retient
  IN10: { clip: 'c6', t0: 4.10, t1: 6.00 },
  IN11: { clip: 'c6', t0: 6.00, t1: 8.00 },
  IN12: { clip: 'c6', t0: 8.00, t1: 9.95 },
  IN13: { clip: 'c2', t0: 2.50, t1: 3.40 },   // macro de l'orbe — insert signature
  IN14: { clip: 'c2', t0: 7.40, t1: 8.90 },
  IN15: { clip: 'c3', t0: 0.00, t1: 2.00 },   // MIMI LELA de dos
  IN16: { clip: 'c3', t0: 5.00, t1: 7.00 },
  IN17: { clip: 'c1', t0: 0.00, t1: 2.50, cadre: { type: 'bandeau16' } },
  IN18: { clip: 'c1', t0: 5.70, t1: 7.90, cadre: { type: 'bandeau16' } },
};

// Les sections, recalées sur la boucle de audio.sh.
// La passe 2 commence à 78,88 s ; S9 enjambe volontairement la jointure et
// porte le traitement `saut` : le glitch d'image masque la couture sonore.
export const SECTIONS = [
  // L'intro est le seul bloc instrumental qui ne se coupe PAS au demi-temps :
  // le titre s'y installe, et cinq coupes en cinq secondes empêcheraient de
  // le lire. `k` force des plans de 4 à 7 demi-temps.
  { nom: 'INTRO',    t0:   0.00, t1:   5.30, chante: false, k: [4, 7],
    plans: ['IN17', 'IN13', 'IN5'] },
  { nom: 'COUPLET',  t0:   5.30, t1:   8.90, chante: true,  plans: ['SC5', 'SC1'] },
  { nom: 'PONT',     t0:   8.90, t1:  12.10, chante: false, plans: ['IN3', 'IN6'] },
  { nom: 'REFRAIN',  t0:  12.10, t1:  35.50, chante: true,
    plans: ['SC8', 'SC6', 'SC10', 'SC3', 'SC4', 'SC7', 'SC11', 'SC2'] },
  { nom: 'BREAK',    t0:  35.50, t1:  44.10, chante: false,
    plans: ['IN8', 'IN1', 'IN7', 'IN3', 'IN2', 'IN12'] },
  { nom: 'COUPLET',  t0:  44.10, t1:  50.90, chante: true,  plans: ['SC9', 'SC6', 'SC8'] },
  { nom: 'BREAK',    t0:  50.90, t1:  56.40, chante: false, plans: ['IN5', 'IN4', 'IN14', 'IN12'] },
  { nom: 'REFRAIN',  t0:  56.40, t1:  77.30, chante: true,
    plans: ['SC1', 'SC5', 'SC10', 'SC8', 'SC6', 'SC12', 'SC3'] },
  { nom: 'JOINTURE', t0:  77.30, t1:  83.15, chante: false,
    plans: ['IN6', 'IN3', 'IN15', 'IN11'] },
  { nom: 'REFRAIN',  t0:  83.15, t1: 106.55, chante: true,
    plans: ['SC11', 'SC5', 'SC3', 'SC7', 'SC6', 'SC9', 'SC1', 'SC8'] },
  { nom: 'BREAK',    t0: 106.55, t1: 115.15, chante: false,
    plans: ['IN8', 'IN2', 'IN6', 'IN4', 'IN3', 'IN7'] },
  { nom: 'COUPLET',  t0: 115.15, t1: 121.95, chante: true,  plans: ['SC4', 'SC10', 'SC5'] },
  { nom: 'BREAK',    t0: 121.95, t1: 127.45, chante: false, plans: ['IN10', 'IN1', 'IN16', 'IN8'] },
  { nom: 'FINAL',    t0: 127.45, t1: 148.35, chante: true,
    plans: ['SC8', 'SC6', 'SC3', 'SC5', 'SC11', 'SC2', 'SC12'] },
  // Deux plans et non un : la case fait 1,65 s et l'insert macro n'en dure
  // que 0,9 — le répéter tel quel poserait deux fois la même image bout à
  // bout, ce qui se lit comme un bug plutôt que comme une fin.
  { nom: 'OUTRO',    t0: 148.35, t1: 150.00, chante: false, plans: ['IN13', 'SC12'] },
];

export const BPM = 83.3;
export const BEAT = 0.7175;        // 60 / BPM, arrondi au relevé
export const MESURE = BEAT * 4;    // 2,87 s
export const DUREE = 150.0;
