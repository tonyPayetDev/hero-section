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
**Objet :** `Ton business mérite d'être automatisé.`
**Objet alternatif A/B :** `Voilà ce que je propose (places limitées)`
**Délai :** 3 jours après email 3 (= J+8 depuis inscription)
**Variables à remplacer :**
- `{{PRIX}}` → ex: 497
- `{{PRIX_BARRE}}` → ex: 797
- `{{STRIPE_PAYMENT_URL}}` → lien Stripe Checkout
- `{{CALENDLY_URL}}` → lien Calendly appel découverte

---

## Variables globales Brevo (à configurer dans les paramètres)

| Variable Brevo | Valeur |
|---|---|
| `{{contact.FIRSTNAME}}` | Prénom (natif Brevo) |
| `{{unsubscribe}}` | Lien désinscription (natif Brevo) |

---

## Checklist avant activation

- [ ] Uploader le PDF guide sur le serveur ou Drive → remplacer `{{GUIDE_URL}}`
- [ ] Créer le lien Stripe → remplacer `{{STRIPE_PAYMENT_URL}}`
- [ ] Renseigner Calendly → remplacer `{{CALENDLY_URL}}`
- [ ] Uploader le JSON n8n → remplacer `{{WORKFLOW_JSON_URL}}`
- [ ] Renseigner prix dans email 4 → `{{PRIX}}` et `{{PRIX_BARRE}}`
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
