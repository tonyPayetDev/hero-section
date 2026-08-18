---
name: etat
description: >
  Affiche l'état réel du business en un coup d'œil : demandes ouvertes (TASKLOG),
  rendus vidéo en cours, vidéos planifiées (Blotato), déploiements Coolify, santé des
  workflows n8n, sites en ligne, travail git non commité. Utilise ce skill dès que
  Tony demande où en sont les choses : « c'est fini ? », « c'est ok ? », « ça va ? »,
  « la suite ? », « les vidéos sont planifiées ? », « c'est déployé ? », « /etat »,
  ou toute demande de statut / avancement. Répond à la place d'une re-vérification manuelle.
---

# /etat — tableau de bord unique

But : supprimer la taxe « c'est fini ? ». Une commande = une réponse factuelle, sourcée,
sur tout ce qui tourne. ~8 % des messages de Tony sont des vérifications de statut :
ce skill y répond en une passe au lieu de rescanner à la main.

## Procédure

1. **Lancer le moteur local** (sources : TASKLOG, Coolify, n8n, /proc, domaines, git) :
   ```bash
   export PATH="/home/claude/tools/node/bin:$PATH"
   node /work/.claude/skills/etat/status.mjs
   ```
   Il imprime déjà un digest compact. Ne pas re-scanner ces sources à la main.

2. **Vidéos planifiées (Blotato, via MCP)** — le moteur ne couvre pas Blotato (pas de
   token local). Appeler `blotato_list_schedules` (serveur Reseaux) pour compter les posts
   à venir et donner les 3 prochaines dates/plateformes. C'est LA réponse à
   « combien de vidéos planifiées ? » / « les vidéos foodboost sont programmées ? ».
   Si le MCP Reseaux est déconnecté, le dire en une ligne et continuer.

3. **Synthétiser en français**, court et scannable, dans cet ordre de priorité :
   - ✅ **Ce qui est fait / en ligne** (domaines 200, apps running, MP4 récents produits)
   - ⏳ **Ce qui tourne** (rendus actifs)
   - 🗓️ **Ce qui est planifié** (prochaines vidéos Blotato)
   - ⚠️ **Ce qui casse** (workflows n8n en erreur, apps non-running qui comptent, sites down)
   - 📋 **Demandes ouvertes des dernières 48h** (pas les 517 historiques — juste le récent)

   Terminer par UNE recommandation d'action si quelque chose casse, sinon « rien ne bloque ».

## Clôturer les tâches faites (fermer la boucle)

Le TASKLOG accumule les demandes mais rien n'est jamais coché → le total gonfle (500+).
Quand une tâche est vérifiée comme faite, la clôturer pour que le compteur « 48h » reste vrai :
```bash
node /work/.claude/skills/etat/close.mjs "motif du texte" --apply          # [x] fait
node /work/.claude/skills/etat/close.mjs "motif" --state '~' --apply        # [~] partiel
node /work/.claude/skills/etat/close.mjs "motif" --state '!' --apply        # [!] abandonné
```
Sans `--apply` c'est un dry-run (montre ce qui serait clôturé). Proposer la clôture à Tony
quand une demande listée est manifestement terminée ; ne pas clôturer à l'aveugle.

## Notes

- Tout est best-effort : une API qui tombe n'empêche pas le reste de s'afficher.
- Tokens lus depuis l'env (`COOLIFY_ACCESS_TOKEN`, `COOLIFY_BASE_URL`, `N8N_API_URL`,
  `N8N_API_KEY`) — déjà présents via `.claude/settings.json`.
- Les workflows IG « Auto-DM » et « Réponse auto commentaires » remontent souvent en erreur
  car ils pollent sans commentaire à traiter : vérifier que c'est bien ça avant d'alerter.
- Rapide (~quelques secondes). Sûr en lecture seule sauf `close.mjs --apply`.
