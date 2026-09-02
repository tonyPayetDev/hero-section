# Setup séquence Brevo — Automation Boost

## Séquence : 4 emails post-téléchargement guide

### Configuration Brevo

**Déclencheur :** Contact remplit le formulaire de téléchargement du guide
→ Tag ajouté : `guide-claude-cowork`
→ Entrée dans l'automation

---

## Les 4 emails

### Email 1 — J+0 (immédiat)
**Fichier :** `email-1-j0-guide-livraison.html`
**Objet :** `Ton guide Claude Code est là — + la 1ère astuce`
**Objet alternatif A/B :** `[Guide] Claude Cowork · livraison immédiate`
**Délai :** 0 min après déclencheur (envoi immédiat)
**Variables à remplacer :**
- `{{GUIDE_URL}}` → URL de téléchargement du PDF

---

### Email 2 — J+2
**Fichier :** `email-2-j2-workflow-scraping.html`
**Objet :** `Le workflow n8n Google Maps (+ recap email auto)`
**Objet alternatif A/B :** `Scraper Google Maps en 6 nodes n8n — workflow complet`
**Délai :** 2 jours après email 1
**Variables à remplacer :**
- `{{WORKFLOW_JSON_URL}}` → URL du fichier JSON n8n à télécharger

---

### Email 3 — J+5
**Fichier :** `email-3-j5-cas-client-horeca.html`
**Objet :** `Ce restaurant publie 22 posts/mois sans y toucher`
**Objet alternatif A/B :** `n8n + Gemini + Blotato → 22 posts/mois (cas client réel)`
**Délai :** 3 jours après email 2 (= J+5 depuis inscription)

---

### Email 4 — J+8
**Fichier :** `email-4-j8-offre-cta-stripe.html`
**Objet :** `Une automatisation qui tourne chez toi sous 7 jours.`
**Objet alternatif A/B :** `Livré sous 7 jours, ou remboursé (990€)`
**Délai :** 3 jours après email 3 (= J+8 depuis inscription)
**Offre :** « Le Déclencheur » — **990 € ferme**, prix écrit en dur dans le HTML (plus de variable).
Voir `docs/offre-automation-boost-refonte.md` pour l'échelle complète (990 € / 2 900 € / 690 €/mois).
**Variables à remplacer :**
- `{{STRIPE_PAYMENT_URL}}` → lien Stripe Checkout « Le Déclencheur — 990 € »
- `{{CALENDLY_URL}}` → lien Calendly « La carte des fuites » (30 min, gratuit)

> ⚠️ Le prix n'est **plus** paramétrable : `{{PRIX}}` et `{{PRIX_BARRE}}` n'étaient jamais
> remplacés et l'email partait sans prix. Pour changer le tarif, éditer le HTML (3 occurrences
> de `990`). Le prix barré a été supprimé volontairement — un prix barré non justifié coûte
> plus de crédibilité qu'il ne fait gagner de conversions.

---

## Variables globales Brevo (à configurer dans les paramètres)

| Variable Brevo | Valeur |
|---|---|
| `{{contact.FIRSTNAME}}` | Prénom (natif Brevo) |
| `{{unsubscribe}}` | Lien désinscription (natif Brevo) |

---

## Checklist avant activation

- [ ] Uploader le PDF guide sur le serveur ou Drive → remplacer `{{GUIDE_URL}}`
- [ ] Créer le lien Stripe « Le Déclencheur — 990 € » → remplacer `{{STRIPE_PAYMENT_URL}}`
- [ ] Créer l'événement Calendly « La carte des fuites » (30 min) → remplacer `{{CALENDLY_URL}}`
- [ ] Uploader le JSON n8n → remplacer `{{WORKFLOW_JSON_URL}}`
- [ ] Préparer le template PDF « La carte des fuites » envoyé après l'appel du palier 0
- [ ] Préparer la réponse type au mot-clé `SPRINT` (P.S. de l'email 4 → offre 2 900 €)
- [ ] Tester avec une adresse perso avant activation
- [ ] Vérifier rendu mobile (Brevo preview intégré)
- [ ] Activer SPF/DKIM sur le domaine automatisationboost.com

---

## Notes techniques HTML Brevo

- Tous les CSS sont **inline** — compatible Brevo, Gmail, Outlook
- `bgcolor` sur chaque `<td>` pour Outlook (qui ignore `background-color` CSS)
- Font stack : Arial/Helvetica uniquement — pas de Google Fonts (bloqué dans certains clients)
- Largeur fixe 600px avec max-width pour mobile
- Preheader masqué en place sur chaque email
