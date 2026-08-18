# Gate commentaire → DM auto (MCP Blotato)

Câblage : quand quelqu'un commente le **mot-clé** sous la vidéo Prompt Reveal, il reçoit
le **prompt complet en DM** — automatiquement. Compte **Automation Boost, `accountId 54617`**.

> Règle d'or : le mot-clé de la vidéo (carte CTA `{{KEYWORD}}`) **doit être identique** au trigger
> de l'automation. Un écart = personne ne reçoit rien.

---

## 1. Vérifier le compte

```
blotato_list_accounts
```
Confirmer que le compte Automation Boost (`accountId 54617`) est bien listé et connecté
(la plateforme cible : Instagram et/ou TikTok selon où la vidéo est postée). Noter l'`id`
exact renvoyé — c'est lui qu'on passe aux appels suivants.

---

## 2. Créer l'automation commentaire → DM

```
blotato_create_automation
```
Paramètres visés (adapter aux noms exacts renvoyés par le schéma de l'outil au moment de l'appel) :

- **account** : `54617` (Automation Boost).
- **trigger** : commentaire contenant le mot-clé, en **matching insensible à la casse** et sur
  le **mot entier** (éviter qu'un mot plus long contenant le mot-clé déclenche à tort).
- **action** : envoyer un DM à l'auteur du commentaire.
- **message** : le message DM type ci-dessous, prompt complet inclus.
- **(optionnel)** répondre publiquement au commentaire (« Regarde tes DMs 📩 ») pour la preuve sociale.

### Message DM type

```
Yes ! 🔥 Voici le prompt complet "Ultra Instinct" utilisé dans la vidéo 👇

<<< COLLER ICI LE PROMPT COMPLET (assets/example-prompt-ultra-instinct.txt) >>>

Images de référence + réglages : dans le fichier.
Si tu le testes, envoie-moi ton rendu ici, je te fais un retour 💪
— Automation Boost
```

> Le DM contient le **prompt COMPLET** (celui qui était volontairement coupé/verrouillé dans la vidéo)
> + les 2 URLs d'images de réf. C'est toute la valeur promise par le CTA.

---

## 3. Garde-fou anti-doublon (obligatoire)

Un même utilisateur peut commenter plusieurs fois → ne l'envoyer **qu'une fois**.

- Préférer l'option native « une réponse par utilisateur » de l'automation si le schéma l'expose.
- Sinon, tenir un registre local des `authorId`/`username` déjà servis et filtrer avant l'envoi :

```
blotato_list_automation_runs     # historique des déclenchements de l'automation
blotato_list_comments            # commentaires reçus sur le post
```
Croiser `author` des runs déjà envoyés ; ne pas renvoyer à un auteur déjà présent.
Journaliser chaque envoi (username + timestamp) dans un fichier local pour audit.

---

## 4. Amorcer / tester

- Poster un commentaire de contrôle avec le mot-clé pour valider le flux :
  ```
  blotato_post_comment
  ```
- Vérifier le déclenchement et le contenu du DM :
  ```
  blotato_list_automation_runs
  ```
- Confirmer que le DM reçu contient bien le prompt **entier** (pas la version tronquée de la vidéo).

---

## Checklist gate

- [ ] `accountId 54617` connecté (`blotato_list_accounts`).
- [ ] Mot-clé automation == mot-clé carte CTA de la vidéo (exact, insensible à la casse, mot entier).
- [ ] DM contient le prompt COMPLET + les 2 URLs d'images de réf.
- [ ] Garde-fou anti-doublon actif (1 DM / utilisateur).
- [ ] Test de contrôle passé (`blotato_post_comment` → `blotato_list_automation_runs` → DM reçu).
- [ ] Journal des envois tenu (username + timestamp).

---

### Outils MCP Blotato utilisés
`blotato_list_accounts` · `blotato_create_automation` · `blotato_list_automation_runs` · `blotato_post_comment`
(complément possible : `blotato_list_comments`, `blotato_update_automation`, `blotato_send_message`)
