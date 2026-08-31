// Refuse une édition dont une brève est visiblement tronquée ou mal découpée.
//
// POURQUOI CE FICHIER EXISTE
// Le 2026-08-25 à 03h00 UTC, le Journal est parti sur cinq réseaux avec une
// brève intitulée « Argent) » et une autre coupée sur « … de Google rejoint l' ».
// La cause (un regex qui franchissait le `**` fermant) est corrigée dans
// parse_edition.mjs. Ce garde-fou-ci couvre la CLASSE du problème : une brève
// malformée ne doit plus jamais atteindre la publication, quelle qu'en soit la
// cause. Le 2026-08-23 était déjà sorti avec le même défaut sans que personne
// le voie.
//
// Il ne juge pas le fond — seulement des signes de troncature mécaniques,
// vérifiables, et sans faux positif sur les éditions correctes.
import fs from 'node:fs';

const OUT = process.argv[2];
if (!OUT) { console.error('usage: check_briefs.mjs <edition.json>'); process.exit(2); }
const ed = JSON.parse(fs.readFileSync(OUT, 'utf8'));

/* Mots qui ne peuvent pas terminer un titre : la phrase continuait. */
const FIN_IMPOSSIBLE = /(?:\b(?:de|du|des|le|la|les|un|une|et|ou|à|au|aux|en|dans|sur|pour|par|avec|que|qui|dont|vers|chez)|['’])\s*$/i;

const soucis = [];
for (const b of ed.briefs || []) {
  const source = (b.source || '').trim();
  const titre = (b.title || '').trim();

  /* Parenthèses déséquilibrées = le découpage a coupé au milieu d'une
     parenthèse. C'est la signature exacte de « (gisement D — Argent) ».
     On teste la source et le titre SÉPARÉMENT : concaténés, la parenthèse
     ouverte de l'un compense la fermante de l'autre et le défaut disparaît
     — le cas « Argent) » passait au travers. */
  for (const [nom, txt] of [['la source', source], ['le titre', titre]]) {
    const o = (txt.match(/\(/g) || []).length;
    const f = (txt.match(/\)/g) || []).length;
    if (o !== f) {
      soucis.push(`brève ${b.n} : parenthèses déséquilibrées dans ${nom} (${o} ouvrante(s), ${f} fermante(s)) — « ${txt.slice(0, 70)} »`);
    }
  }

  /* Titre qui s'arrête sur un mot outil ou une apostrophe : phrase coupée. */
  if (FIN_IMPOSSIBLE.test(titre)) {
    soucis.push(`brève ${b.n} : titre coupé en pleine phrase — « …${titre.slice(-46)} »`);
  }

  /* Pas de règle sur la longueur du titre : « xAI — Grok 4.6 » (édition du
     16/08) est parfaitement valide et une règle « moins de 12 caractères »
     la rejetait. Un fragment court comme « Argent) » se reconnaît à sa
     parenthèse orpheline, pas à sa taille. Un garde-fou qui crie sur du bon
     travail finit par être ignoré — et ne protège alors plus de rien. */

  /* Une source n'est pas une phrase. Vide est légitime (parse_edition la
     reconstruit) ; longue et ponctuée ne l'est pas. */
  if (source.length > 40 || /[.!?](\s|$)/.test(source)) {
    soucis.push(`brève ${b.n} : la source contient du texte de corps — « ${source.slice(0, 70)} »`);
  }
}

if (soucis.length) {
  console.error(`[check] ${soucis.length} brève(s) malformée(s) :`);
  soucis.forEach((s) => console.error(`  ✗ ${s}`));
  process.exit(1);
}
console.error(`[check] ${(ed.briefs || []).length} brèves, aucune tronquée`);
