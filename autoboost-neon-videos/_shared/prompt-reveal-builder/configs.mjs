// Per-video configs for the 5 "prompt reveal" videos built on real Higgsfield clips.
// Each `console` is the EXACT prompt (translated/condensed for screen), with the
// decisive keywords REDACTED — the full text is only delivered by DM.
export const CFGS = [
{
  dir: 'autoboost-56-prompt-reveal-01-regard',
  id: 'autoboost-56-prompt-reveal-01-regard',
  keyword: 'REGARD',
  mode: 'tall',
  kicker: "Ce plan n'a jamais été filmé",
  tag: '1 prompt → 1 plan cinéma',
  beat: 0.743,
  roles: ["Ce plan n'a jamais été filmé", '100% généré par IA'],
  popTimes: [0.9, 12.0],
  console: `<span class="c">// SEEDANCE 2.5 — PORTRAIT CINÉMA — 9:16 · 8s · plan-séquence</span>

<span class="m">CAMÉRA :</span> <span class="k">push-in lent et délibéré</span> vers
l'œil droit du sujet, comme si on entrait
dans son univers intérieur.

<span class="m">ACTION :</span> il retire lentement une capuche noire
à deux mains, révélant <span class="redact">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span> de la
référence, puis soutient un regard calme
et intense dans l'objectif.

<span class="m">CONTRAINTES :</span> respiration subtile et
clignements naturels <span class="o">uniquement</span>.
Aucune parole, <span class="redact">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>,
<span class="k">identité préservée</span> du début à la fin.

<span class="m">LUMIÈRE :</span> studio noir mat, <span class="redact">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
jaune et violet retenue, mouvement de
caméra réaliste.

<span class="m">FIN :</span> gros plan extrême sur l'œil,
<span class="o">l'iris remplit le cadre</span>.

<span class="c">// aucun texte, aucun logo, aucune autre personne</span>
<span class="c">// prompt complet en DM →</span> <span class="k">commente REGARD</span><span class="cursor"></span>`
},
{
  dir: 'autoboost-56-prompt-reveal-02-burger',
  id: 'autoboost-56-prompt-reveal-02-burger',
  keyword: 'BURGER',
  mode: 'tall',
  kicker: "Ce burger n'existe pas",
  tag: '0 tournage · 0 shooting',
  beat: 0.743,
  roles: ["Ce burger n'existe pas", 'Fait pour les restos'],
  console: `<span class="c">// SEEDANCE 2.5 — FOOD REEL — 9:16 · 10s · pub resto</span>

<span class="m">HOOK 0-2s :</span> plan <span class="k">macro extrême</span> du fromage
fondu qui s'étire depuis un burger gourmet
<span class="redact">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>, impact visuel immédiat.

<span class="m">2-7s :</span> coupes cinématiques rapides — bœuf
qui grésille, brioche toastée, salade
craquante, <span class="redact">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span> qui coule.

<span class="m">7-9s :</span> burger assemblé et poussé vers la
caméra, <span class="o">vapeur qui monte</span>, plan héros
qui donne faim.

<span class="m">9-10s :</span> CTA net et gras incrusté à l'écran.

<span class="m">RENDU :</span> rythme rapide, pub food premium,
textures <span class="redact">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>, physique
réaliste, <span class="k">aucun logo</span>.

<span class="c">// remplace un shooting photo à 800 €</span>
<span class="c">// prompt complet en DM →</span> <span class="k">commente BURGER</span><span class="cursor"></span>`,
  popTimes: [0.9, 11.5]
},
{
  dir: 'autoboost-56-prompt-reveal-03-shonen',
  id: 'autoboost-56-prompt-reveal-03-shonen',
  keyword: 'SHONEN',
  mode: 'tall',
  kicker: "Ce n'est pas un film",
  tag: '1 phrase → 10s de VFX',
  beat: 0.743,
  roles: ["Ce n'est pas un film", 'Découpage seconde par seconde'],
  console: `<span class="c">// SEEDANCE 2.5 — TRANSFORMATION — 9:16 · 10s · live-action anime</span>

<span class="m">RÉFÉRENCES :</span> image_1 = androïde de combat.
image_2 = jeune guerrier. <span class="k">Identité, coiffure,
vêtements et proportions préservées</span> sur les
10 secondes.

<span class="m">0.0-2.0s :</span> contre-plongée extrême, l'androïde
gît immobile sur le champ de bataille dévasté.
La poussière flotte. <span class="redact">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>

<span class="m">2.0-4.0s — LE DÉCLENCHEUR :</span> une botte entre
dans le cadre. Coupe immédiate sur le visage :
la tristesse devient rage. <span class="o">Silence anormal.</span>

<span class="m">4.0-6.0s — TRANSFORMATION :</span> il hurle. Cheveux
noirs → <span class="k">or pâle</span>, yeux <span class="k">bleu électrique</span>,
<span class="redact">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span> dans les pupilles.
Aura doré-blanc, éclairs, débris qui lévitent.

<span class="m">6.0-8.0s :</span> coupe franche en plongée verticale,
onde de choc circulaire, rotation lente.

<span class="m">8.0-10.0s :</span> plan frontal, <span class="o">bras écartés</span>,
bras mécanique gauche <span class="redact">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>.
Fin en gros plan sur les yeux.

<span class="c">// pas de sang, pas de texte, pas de logo</span>
<span class="c">// prompt complet en DM →</span> <span class="k">commente SHONEN</span><span class="cursor"></span>`,
  popTimes: [0.9, 12.5]
},
{
  dir: 'autoboost-56-prompt-reveal-04-neon',
  id: 'autoboost-56-prompt-reveal-04-neon',
  keyword: 'NEON',
  mode: 'tall',
  kicker: 'Ce clip a coûté 0 €',
  tag: '0 danseur · 0 équipe VFX',
  beat: 0.743,
  roles: ['Ce clip a coûté 0 €', '3 blocs dans le prompt'],
  console: `<span class="c">// SEEDANCE 2.5 — CLIP MUSIQUE — 9:16 · 10s · dancehall futuriste</span>

<span class="m">SUJET :</span> un chanteur charismatique interprète
un morceau dancehall face caméra. Il <span class="k">chante et
danse en même temps</span>, lèvres synchronisées,
présence scénique assumée.

<span class="m">BOULE D'ÉNERGIE :</span> une petite sphère lumineuse
<span class="o">lévite au-dessus de l'index</span>, sans jamais le
toucher, rotation lente, aura puissante,
<span class="redact">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span> au rythme de la musique.

<span class="m">CAMÉRA :</span> montage clip — gros plan visage,
macro sur la sphère, plan large chorégraphie,
contre-plongée héros, orbite fluide,
<span class="redact">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span> calé sur un temps musical.

<span class="m">STYLE :</span> techwear premium, noir + accents orange
et bleu électrique, ville de nuit néon, brume
atmosphérique, <span class="k">bitume mouillé réfléchissant</span>.

<span class="m">VERROUS :</span> même identité du début à la fin,
anatomie naturelle, <span class="redact">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>,
aucune main dupliquée.

<span class="c">// prompt complet en DM →</span> <span class="k">commente NEON</span><span class="cursor"></span>`,
  popTimes: [0.9, 12.0]
},
{
  dir: 'autoboost-56-prompt-reveal-05-combat',
  id: 'autoboost-56-prompt-reveal-05-combat',
  keyword: 'COMBAT',
  mode: 'wide',
  kicker: 'Elle réapparaît dans son dos',
  tag: '1 seule prise · 0 post-prod',
  beat: 0.743,
  roles: ['Aucun effet ajouté après', 'La règle qui change tout'],
  console: `<span class="c">// SEEDANCE 2.5 — COMBAT — 16:9 · 10s · UNE SEULE PRISE · live-action</span>

<span class="m">ADN DU COMBAT :</span> corps à corps rapide, fluide,
cinématique. Anatomie, poids, élan et réactions
d'impact <span class="k">physiquement cohérents</span>.

<span class="m">00:00-02.0 — TÉLÉPORTATION DANS LE DOS :</span>
A lance une attaque rapide. B esquive de justesse
→ au pic exact de l'attaque, B <span class="o">DISPARAÎT</span> de
devant A → <span class="o">RÉAPPARAÎT DIRECTEMENT DANS SON DOS</span>,
à très courte distance.

<span class="c">// LA RÈGLE QUI REND ÇA CRÉDIBLE :</span>
<span class="redact">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
<span class="redact">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>

<span class="m">00:02-04.5 — CONTRE :</span> B saisit le bras de A par
derrière → redirige son élan sur le côté → contre
court et contrôlé au torse → A trébuche en avant.

<span class="m">00:06.5-08.0 :</span> <span class="k">SECONDE téléportation</span>, distincte
de la première, même logique de déplacement.

<span class="m">CAMÉRA :</span> caméra épaule continue, <span class="redact">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
pendant chaque téléportation. <span class="o">AUCUNE COUPE.</span>

<span class="m">FIN :</span> différente du début. Pas de pose de
victoire, pas de boucle, coupe en plein mouvement.

<span class="c">// prompt complet en DM →</span> <span class="k">commente COMBAT</span><span class="cursor"></span>`,
  popTimes: [0.9, 12.5]
}
];
