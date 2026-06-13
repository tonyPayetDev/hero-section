import os

BASE = "/work/automationboost/ressources"

CSS = """background:#0a0a0a;border:1px solid var(--border);border-radius:var(--radius);padding:16px 20px;font-family:monospace;font-size:14px;color:#a3e635;margin:16px 0;overflow-x:auto;white-space:pre"""

SHARED_CSS = """
    .res-page{padding:120px 0 80px}.breadcrumb{font-size:13px;color:var(--text-muted);margin-bottom:32px}.breadcrumb a{color:var(--gold);text-decoration:none}.breadcrumb span{margin:0 8px}.page-badge-art{display:inline-flex;align-items:center;gap:6px;background:rgba(99,102,241,.15);border:1px solid rgba(99,102,241,.25);color:#818cf8;font-size:11px;font-weight:700;padding:4px 12px;border-radius:4px;letter-spacing:.06em;text-transform:uppercase;margin-bottom:20px}.page-badge-vid{display:inline-flex;align-items:center;gap:6px;background:rgba(234,179,8,.12);border:1px solid rgba(234,179,8,.25);color:var(--gold);font-size:11px;font-weight:700;padding:4px 12px;border-radius:4px;letter-spacing:.06em;text-transform:uppercase;margin-bottom:20px}.page-title{font-size:clamp(1.8rem,4vw,2.8rem);font-family:'Orbitron',sans-serif;font-weight:900;margin-bottom:16px;line-height:1.2}.page-title span{color:var(--gold)}.page-meta{display:flex;align-items:center;gap:16px;font-size:13px;color:var(--text-muted);margin-bottom:48px}.divider{width:60px;height:2px;background:var(--gold);margin:40px 0}.content-block{max-width:720px}.content-block h2{font-family:'Orbitron',sans-serif;font-size:1.2rem;font-weight:700;color:var(--text);margin:40px 0 16px}.content-block p{color:var(--text-light);line-height:1.8;margin-bottom:16px}.content-block ul{color:var(--text-light);line-height:1.9;padding-left:20px;margin-bottom:16px}.content-block ul li{margin-bottom:6px}.tip-box{background:var(--bg-card);border:1px solid rgba(234,179,8,.2);border-left:3px solid var(--gold);border-radius:var(--radius);padding:20px 24px;margin:24px 0}.tip-box .tip-label{font-size:11px;font-weight:700;color:var(--gold);text-transform:uppercase;letter-spacing:.06em;margin-bottom:8px}.tip-box p{color:var(--text-light);margin:0;font-size:15px}.code-block{background:#0a0a0a;border:1px solid var(--border);border-radius:var(--radius);padding:16px 20px;font-family:monospace;font-size:14px;color:#a3e635;margin:16px 0;overflow-x:auto;white-space:pre}.source-cta{display:inline-flex;align-items:center;gap:10px;background:var(--gold);color:#000;font-family:'Orbitron',sans-serif;font-size:13px;font-weight:700;padding:14px 28px;border-radius:var(--radius);text-decoration:none;margin-top:40px;transition:all .2s}.source-cta:hover{background:var(--gold-dark);transform:translateY(-2px)}.nav-back{display:inline-flex;align-items:center;gap:8px;color:var(--text-muted);font-size:14px;text-decoration:none;margin-top:60px;transition:color .2s}.nav-back:hover{color:var(--gold)}
"""

def page(filename, title, meta_desc, badge_type, badge_label, h1, meta_tags, body_html, source_url, source_label, breadcrumb_label):
    badge_class = "page-badge-vid" if badge_type == "video" else "page-badge-art"
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} – AutomationBoost</title>
  <meta name="description" content="{meta_desc}" />
  <link rel="stylesheet" href="../assets/css/style.css" />
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%23eab308'/><text x='50%25' y='54%25' dominant-baseline='middle' text-anchor='middle' font-size='18' font-family='Arial' fill='%23000'>⚡</text></svg>" />
  <style>{SHARED_CSS}</style>
</head>
<body>
<nav id="navbar">
  <div class="nav-inner">
    <a href="/" class="logo"><div class="logo-icon">⚡</div><span class="logo-text">Automation<span>Boost</span></span></a>
    <a href="../ressources.html" style="color:var(--gold);font-size:14px;font-weight:600;text-decoration:none;font-family:'Rajdhani',sans-serif;">← Ressources</a>
  </div>
</nav>
<section class="res-page">
  <div class="container">
    <div class="breadcrumb"><a href="../ressources.html">Ressources</a><span>/</span>{breadcrumb_label}</div>
    <div class="{badge_class}">{badge_label}</div>
    <h1 class="page-title">{h1}</h1>
    <div class="page-meta">{meta_tags}</div>
    <div class="content-block">
{body_html}
      <a href="{source_url}" target="_blank" rel="noopener" class="source-cta">{source_label}</a>
    </div>
    <a href="../ressources.html" class="nav-back">← Retour aux ressources</a>
  </div>
</section>
<script>const navbar=document.getElementById('navbar');window.addEventListener('scroll',()=>navbar.classList.toggle('scrolled',window.scrollY>20));</script>
</body>
</html>"""
    path = os.path.join(BASE, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ {filename}")


# ── PAGE 3 : 3 techniques tokens ──────────────────────────────────────────────
page(
    "reduire-cout-tokens.html",
    "3 Astuces pour Réduire la Facture Claude",
    "Réduisez votre consommation de tokens de 80% avec 3 réglages simples dans Claude Code.",
    "article", "◈ Article",
    "Diviser sa facture Claude par <span>5</span>",
    "<span>Claude Code</span><span>·</span><span>Optimisation</span><span>·</span><span>Niveau débutant</span>",
    """      <p>Claude Code facture à la consommation de tokens. Chaque ligne de contexte envoyée au modèle coûte. Par défaut, les réglages sont généreux — pratique pour débuter, coûteux à l'usage intensif. Trois ajustements simples suffisent à diviser ta facture par 5 sans sacrifier la qualité.</p>
      <div style="width:60px;height:2px;background:var(--gold);margin:40px 0"></div>
      <h2>Réglage 1 — Choisir le bon modèle avec /model</h2>
      <p>Par défaut, Claude Code utilise le modèle le plus puissant (Opus). Pour les tâches simples — génération de tests, refactoring basique, questions de syntaxe — un modèle plus léger fait exactement le même travail pour 5 à 10 fois moins cher.</p>
      <div class="code-block">/model claude-haiku-4-5   # tâches simples, rapides et économiques
/model claude-sonnet-4-5  # équilibre puissance/coût pour la plupart des tâches
/model claude-opus-4      # réservé aux problèmes complexes uniquement</div>
      <p>La stratégie gagnante : Haiku pour les tâches répétitives, Sonnet pour le travail quotidien, Opus seulement quand les autres modèles bloquent.</p>
      <h2>Réglage 2 — Activer le RTK (Relevant Token Keeping)</h2>
      <p>Le RTK est un mécanisme qui tronque intelligemment le contexte en gardant uniquement les parties pertinentes pour ta requête. Au lieu d'envoyer tout l'historique de la conversation, Claude ne reçoit que ce dont il a besoin.</p>
      <div class="tip-box"><div class="tip-label">💡 Impact concret</div><p>Sur des sessions longues (1h+), le RTK peut réduire de 60 à 70% le nombre de tokens envoyés. C'est là que se font les vraies économies.</p></div>
      <h2>Réglage 3 — Un CLAUDE.md bien structuré</h2>
      <p>Un CLAUDE.md verbeux avec 500 lignes de contexte est lu intégralement à chaque requête. Un CLAUDE.md compact et ciblé (50-100 lignes essentielles) fait le même travail pour 80% moins de tokens de contexte.</p>
      <ul>
        <li>Supprimer les explications que Claude comprend déjà nativement</li>
        <li>Remplacer les paragraphes par des listes à puces concises</li>
        <li>Ne garder que les règles non-évidentes spécifiques à ton projet</li>
      </ul>
      <div class="tip-box"><div class="tip-label">⚡ Combinaison gagnante</div><p>Ces trois réglages ensemble peuvent réduire ta consommation de 80%. Sur un usage intensif de 100€/mois, ça te ramène à 20€ avec exactement les mêmes résultats.</p></div>""",
    "https://agentic-academy.fr/discover/watch/1a68fb77-c191-48a7-b44d-32201b276f59",
    "◈ Lire l'article original",
    "3 Astuces pour Réduire la Facture"
)

# ── PAGE 4 : 127 sous-agents ──────────────────────────────────────────────────
page(
    "127-sous-agents.html",
    "127 Sous-Agents Spécialisés pour Claude Code",
    "Une bibliothèque de 127 agents IA prêts à l'emploi pour automatiser chaque étape de votre workflow de développement.",
    "video", "▶ Vidéo · 1m 38s",
    "<span>127</span> sous-agents prêts à l'emploi",
    "<span>Claude Code</span><span>·</span><span>Agents IA</span><span>·</span><span>Niveau intermédiaire</span>",
    """      <p>Le repo <strong style="color:var(--text)">awesome-claude-code-subagents</strong> de VoltAgent recense 127 sous-agents spécialisés, prêts à brancher dans Claude Code. Chaque agent est une instruction système optimisée pour une tâche précise — debug, tests, documentation, sécurité, performance...</p>
      <div style="width:60px;height:2px;background:var(--gold);margin:40px 0"></div>
      <h2>C'est quoi un sous-agent Claude Code ?</h2>
      <p>Un sous-agent est une instance de Claude configurée avec un rôle et des instructions spécifiques. Au lieu de demander à un modèle généraliste de tout faire, tu dispatches les tâches vers des agents experts dans leur domaine.</p>
      <p>Résultat : chaque tâche est traitée par un agent qui connaît exactement les meilleures pratiques pour ce type de problème, sans polluer le contexte avec des instructions sans rapport.</p>
      <h2>Exemples d'agents disponibles</h2>
      <ul>
        <li><strong style="color:var(--text)">security-auditor</strong> — analyse ton code pour les vulnérabilités OWASP</li>
        <li><strong style="color:var(--text)">test-writer</strong> — génère des tests unitaires et d'intégration complets</li>
        <li><strong style="color:var(--text)">performance-optimizer</strong> — identifie et corrige les bottlenecks</li>
        <li><strong style="color:var(--text)">documentation-writer</strong> — crée la doc technique depuis le code</li>
        <li><strong style="color:var(--text)">code-reviewer</strong> — fait une revue de code senior sur tes PRs</li>
        <li><strong style="color:var(--text)">refactoring-agent</strong> — restructure le code sans changer le comportement</li>
      </ul>
      <h2>Comment les utiliser</h2>
      <div class="code-block"># Cloner le repo
git clone https://github.com/VoltAgent/awesome-claude-code-subagents

# Copier un agent dans ton projet
cp awesome-claude-code-subagents/security-auditor.md .claude/agents/

# L'appeler dans Claude Code
/agent security-auditor "Audite le dossier src/auth/"</div>
      <div class="tip-box"><div class="tip-label">💡 Stratégie recommandée</div><p>N'installe pas les 127 d'un coup. Commence par 3-4 agents pour les tâches que tu répètes le plus souvent. Ajoute-en au fur et à mesure de tes besoins.</p></div>
      <div class="tip-box"><div class="tip-label">⚡ Conseil pro</div><p>Tu peux créer tes propres agents en t'inspirant de ceux du repo. Le pattern est simple : un nom, un rôle, des instructions précises, des exemples de sorties attendues.</p></div>""",
    "https://agentic-academy.fr/discover/watch/1e1b9de8-58e7-4c6e-8621-ac7659eb3598",
    "▶ Voir la vidéo originale (1m 38s)",
    "127 Sous-Agents Spécialisés"
)

# ── PAGE 5 : 5 couches mémoire ────────────────────────────────────────────────
page(
    "5-couches-memoire.html",
    "Les 5 Couches Mémoire de Claude Code",
    "Donnez une mémoire persistante à Claude Code avec ce système de 5 fichiers pour des sessions continues et efficaces.",
    "article", "◈ Article",
    "Donner une <span>mémoire persistante</span> à Claude Code",
    "<span>Claude Code</span><span>·</span><span>Mémoire & Contexte</span><span>·</span><span>Niveau avancé</span>",
    """      <p>Claude Code n'a pas de mémoire native entre les sessions. Chaque nouvelle conversation repart de zéro. Le système des 5 couches mémoire de Thariq (@trq212) résout ce problème avec une architecture simple : 5 fichiers Markdown qui reconstituent le contexte automatiquement à chaque session.</p>
      <div style="width:60px;height:2px;background:var(--gold);margin:40px 0"></div>
      <h2>Pourquoi la mémoire est cruciale</h2>
      <p>Sans mémoire structurée, tu passes les 5-10 premières minutes de chaque session à réexpliquer le contexte : qui tu es, ce que tu construis, quelles décisions ont déjà été prises. Sur un projet long, c'est une perte massive de temps et de tokens.</p>
      <h2>Les 5 couches du système</h2>
      <ul>
        <li><strong style="color:var(--text)">Couche 1 — user.md</strong> : qui tu es, tes préférences, ton style de travail</li>
        <li><strong style="color:var(--text)">Couche 2 — project.md</strong> : contexte du projet, stack, objectifs, contraintes</li>
        <li><strong style="color:var(--text)">Couche 3 — decisions.md</strong> : toutes les décisions techniques prises et pourquoi</li>
        <li><strong style="color:var(--text)">Couche 4 — progress.md</strong> : état d'avancement, tâches en cours, prochaines étapes</li>
        <li><strong style="color:var(--text)">Couche 5 — feedback.md</strong> : ce qui a bien fonctionné, les erreurs à éviter</li>
      </ul>
      <div class="tip-box"><div class="tip-label">💡 Setup automatique</div><p>Le système de Thariq inclut un script d'initialisation qui crée les 5 fichiers et les remplit avec tes informations en une seule commande. Claude les lit automatiquement au démarrage de chaque session via le CLAUDE.md.</p></div>
      <h2>Comment l'intégrer dans ton CLAUDE.md</h2>
      <div class="code-block"># Dans ton CLAUDE.md
## Mémoire du projet
Lis ces fichiers au début de chaque session :
- .claude/memory/user.md
- .claude/memory/project.md
- .claude/memory/decisions.md
- .claude/memory/progress.md
- .claude/memory/feedback.md

Après chaque session, mets à jour progress.md avec ce qui a été fait.</div>
      <h2>Résultats concrets</h2>
      <ul>
        <li>Zéro réexplication de contexte en début de session</li>
        <li>Claude connaît les décisions passées et ne les remet pas en question inutilement</li>
        <li>Continuité parfaite sur des projets de plusieurs semaines</li>
        <li>Économie de 20-30% de tokens par session</li>
      </ul>
      <div class="tip-box"><div class="tip-label">⚡ Conseil pro</div><p>Demande à Claude de mettre à jour progress.md en fin de session. En une phrase : "Résume ce qu'on a fait aujourd'hui et mets à jour progress.md". Tu auras toujours un journal de bord à jour.</p></div>""",
    "https://agentic-academy.fr/discover/watch/bb479a61-a7ea-46bc-8659-1ec408ddf3e9",
    "◈ Lire l'article original",
    "Les 5 Couches Mémoire"
)

# ── PAGE 6 : DeerFlow ─────────────────────────────────────────────────────────
page(
    "guide-deerflow.html",
    "Guide DeerFlow – L'IA Multi-Agents de ByteDance",
    "Installez et utilisez DeerFlow, le framework open source multi-agents de ByteDance, pour automatiser recherche et rapports.",
    "article", "◈ Article",
    "DeerFlow — automatiser avec des <span>agents en parallèle</span>",
    "<span>Agents IA</span><span>·</span><span>Open Source</span><span>·</span><span>Niveau intermédiaire</span>",
    """      <p><strong style="color:var(--text)">DeerFlow</strong> est le framework multi-agents open source développé par ByteDance. Contrairement aux outils qui utilisent un seul modèle séquentiellement, DeerFlow orchestre plusieurs agents spécialisés en parallèle : un cherche des informations, un autre les analyse, un troisième rédige le rapport — tout simultanément.</p>
      <div style="width:60px;height:2px;background:var(--gold);margin:40px 0"></div>
      <h2>Ce que DeerFlow peut faire</h2>
      <ul>
        <li>Recherche web approfondie avec synthèse automatique</li>
        <li>Génération de rapports structurés de 10-50 pages</li>
        <li>Création de présentations slides depuis un sujet</li>
        <li>Analyse de marchés et veille concurrentielle automatisée</li>
        <li>Génération et exécution de code avec feedback en boucle</li>
      </ul>
      <h2>Installation en 10 minutes</h2>
      <div class="code-block"># Cloner le repo
git clone https://github.com/bytedance/deer-flow
cd deer-flow

# Installer les dépendances
pip install -r requirements.txt

# Configurer ta clé API
cp .env.example .env
# Éditer .env avec ta clé Anthropic ou OpenAI

# Lancer DeerFlow
python main.py</div>
      <div class="tip-box"><div class="tip-label">💡 Compatible avec Claude</div><p>DeerFlow fonctionne nativement avec l'API Anthropic. Configure simplement ta clé dans le .env et les agents utiliseront Claude pour toutes les tâches de raisonnement.</p></div>
      <h2>Exemple d'utilisation</h2>
      <div class="code-block"># Demander un rapport de marché complet
python main.py --task "Analyse le marché de l'automatisation IA en France en 2025 :
acteurs principaux, taille du marché, tendances, opportunités.
Produis un rapport de 20 pages avec sources."</div>
      <p>DeerFlow va lancer automatiquement plusieurs agents : un pour la recherche web, un pour l'analyse des données trouvées, un pour la rédaction. Le rapport final est compilé en quelques minutes.</p>
      <h2>Cas d'usage concrets</h2>
      <ul>
        <li><strong style="color:var(--text)">Freelances</strong> : génèrer des études de marché pour tes clients en quelques minutes</li>
        <li><strong style="color:var(--text)">Content creators</strong> : automatiser la recherche documentaire avant d'écrire</li>
        <li><strong style="color:var(--text)">Startups</strong> : veille concurrentielle automatique hebdomadaire</li>
      </ul>
      <div class="tip-box"><div class="tip-label">⚡ Conseil pro</div><p>DeerFlow est open source — tu peux créer tes propres agents spécialisés et les intégrer dans le pipeline. C'est là que l'outil devient vraiment puissant pour des cas d'usage métier spécifiques.</p></div>""",
    "https://agentic-academy.fr/discover/watch/17dfc56d-beb6-4a11-a60a-0d48049406d9",
    "◈ Lire l'article original",
    "Guide DeerFlow"
)

# ── PAGE 7 : Playwright ───────────────────────────────────────────────────────
page(
    "claude-playwright.html",
    "Donner un Navigateur à Claude Code avec Playwright",
    "Connectez Playwright à Claude Code pour scraper, remplir des formulaires et extraire des données sans toucher au contexte.",
    "article", "◈ Article",
    "Claude Code + <span>Playwright</span> = navigateur IA",
    "<span>Claude Code</span><span>·</span><span>Automatisation Web</span><span>·</span><span>Niveau intermédiaire</span>",
    """      <p>Par défaut, Claude Code ne peut pas naviguer sur internet. Il travaille avec ce que tu lui fournis. En connectant <strong style="color:var(--text)">Playwright</strong> — le framework de navigation headless de Microsoft — Claude devient capable d'ouvrir des pages, cliquer sur des éléments, remplir des formulaires et extraire des données en temps réel.</p>
      <div style="width:60px;height:2px;background:var(--gold);margin:40px 0"></div>
      <h2>Ce que ça change concrètement</h2>
      <ul>
        <li>Scraper n'importe quelle page, même rendue en JavaScript</li>
        <li>Automatiser des formulaires de connexion et de saisie</li>
        <li>Prendre des screenshots pour vérifier des interfaces</li>
        <li>Extraire des données structurées depuis des sites dynamiques</li>
        <li>Tester des flows utilisateur complets automatiquement</li>
      </ul>
      <h2>Installation du MCP Playwright</h2>
      <div class="code-block"># Dans ton projet Claude Code
claude mcp add playwright

# Ou manuellement dans .claude/settings.json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}</div>
      <div class="tip-box"><div class="tip-label">💡 Zéro gaspillage de contexte</div><p>L'avantage de passer par MCP plutôt que de coller du HTML dans le chat : le contenu de la page n'entre jamais dans la fenêtre de contexte de Claude. Seulement les données que tu lui demandes d'extraire.</p></div>
      <h2>Exemples de prompts avec Playwright actif</h2>
      <div class="code-block">"Va sur https://example.com, trouve tous les prix des produits
et retourne-les sous forme de tableau JSON"</div>
      <div class="code-block">"Connecte-toi sur mon dashboard (email: X, mot de passe: Y),
navigue vers les rapports du mois dernier et télécharge le CSV"</div>
      <div class="code-block">"Prends un screenshot de ma landing page sur mobile
et dis-moi ce qui pose problème côté UX"</div>
      <h2>Limitations à connaître</h2>
      <ul>
        <li>Certains sites bloquent les navigateurs headless (Cloudflare bot protection)</li>
        <li>Les captchas nécessitent une intervention manuelle</li>
        <li>Les sessions sont temporaires — pas de cookies persistants entre les runs</li>
      </ul>
      <div class="tip-box"><div class="tip-label">⚡ Conseil pro</div><p>Combine Playwright avec un sous-agent dédié au scraping. L'agent sait déjà gérer les sélecteurs CSS, les délais d'attente et les erreurs réseau — tu n'as pas à l'expliquer à chaque fois.</p></div>""",
    "https://agentic-academy.fr/discover/watch/578a098b-aa7c-4202-9bd6-ccb4bae341b2",
    "◈ Lire l'article original",
    "Claude Code + Playwright"
)

# ── PAGE 8 : PDF en Markdown ──────────────────────────────────────────────────
page(
    "pdf-vers-markdown.html",
    "Convertir vos PDF en Markdown Avant de les Envoyer à Claude",
    "Économisez des tokens et améliorez la compréhension de Claude en convertissant vos PDF en Markdown avant de les envoyer.",
    "article", "◈ Article",
    "PDF → <span>Markdown</span> : économisez 3x de tokens",
    "<span>Claude</span><span>·</span><span>Optimisation</span><span>·</span><span>Niveau débutant</span>",
    """      <p>Envoyer un PDF directement à Claude est intuitif mais inefficace. Claude doit interpréter la mise en page, les colonnes, les en-têtes, les pieds de page — du bruit qui consomme des tokens sans apporter de valeur. En convertissant d'abord en Markdown, tu envoies uniquement le contenu utile.</p>
      <div style="width:60px;height:2px;background:var(--gold);margin:40px 0"></div>
      <h2>Pourquoi les PDF coûtent cher en tokens</h2>
      <p>Un PDF de 10 pages envoyé directement peut consommer 8 000 à 15 000 tokens selon sa mise en page. Le même contenu en Markdown propre tourne autour de 2 000 à 4 000 tokens. Sur des documents techniques longs, la différence est énorme.</p>
      <p>De plus, le Markdown est le format natif de Claude. Il le comprend mieux, extrait l'information plus précisément et génère des réponses plus pertinentes.</p>
      <h2>Outils pour convertir</h2>
      <ul>
        <li><strong style="color:var(--text)">marker</strong> (Python) — le plus précis pour les PDFs complexes avec tableaux</li>
        <li><strong style="color:var(--text)">pymupdf4llm</strong> — rapide, optimisé spécifiquement pour les LLMs</li>
        <li><strong style="color:var(--text)">pdf2md</strong> — simple et efficace pour les PDFs textuels</li>
        <li><strong style="color:var(--text)">pandoc</strong> — couteau suisse, converti depuis/vers beaucoup de formats</li>
      </ul>
      <h2>Installation et usage rapide</h2>
      <div class="code-block"># Installer pymupdf4llm (recommandé pour Claude)
pip install pymupdf4llm

# Convertir un PDF
python -c "import pymupdf4llm; print(pymupdf4llm.to_markdown('document.pdf'))" > document.md

# Envoyer le Markdown à Claude
claude "Résume ce document" --file document.md</div>
      <div class="tip-box"><div class="tip-label">💡 Pour les PDFs avec images</div><p>Si ton PDF contient des graphiques ou schémas importants, utilise marker qui préserve les images et les convertit en références Markdown. Les autres outils ignorent les images.</p></div>
      <h2>Aller plus loin : automatiser le pipeline</h2>
      <div class="code-block"># Script bash pour convertir tous les PDFs d'un dossier
for pdf in *.pdf; do
    python -c "import pymupdf4llm; \
    content = pymupdf4llm.to_markdown('$pdf'); \
    open('${pdf%.pdf}.md', 'w').write(content)"
    echo "✓ Converti: $pdf"
done</div>
      <div class="tip-box"><div class="tip-label">⚡ Conseil pro</div><p>Ajoute une étape de nettoyage après la conversion : supprime les numéros de page, les en-têtes répétitifs et les références bibliographiques si elles ne t'intéressent pas. Ça réduit encore 20-30% du contenu.</p></div>""",
    "https://agentic-academy.fr/discover/watch/6aba0044-708b-4851-9837-8b586610ff22",
    "◈ Lire l'article original",
    "PDF → Markdown"
)

# ── PAGE 9 : Computer Use ─────────────────────────────────────────────────────
page(
    "claude-computer-use.html",
    "Guide Claude Computer Use + Dispatch",
    "Pilotez votre Mac à distance avec Claude Computer Use et Dispatch depuis n'importe quel appareil.",
    "article", "◈ Article",
    "Contrôler son Mac avec <span>Claude</span> depuis son téléphone",
    "<span>Claude</span><span>·</span><span>Computer Use</span><span>·</span><span>Niveau avancé</span>",
    """      <p><strong style="color:var(--text)">Computer Use</strong> est la fonctionnalité d'Anthropic qui permet à Claude de voir ton écran et de contrôler ta souris et ton clavier. Couplé à <strong style="color:var(--text)">Dispatch</strong>, tu peux piloter ton Mac depuis ton téléphone comme si tu étais devant lui.</p>
      <div style="width:60px;height:2px;background:var(--gold);margin:40px 0"></div>
      <h2>Ce que ça permet de faire</h2>
      <ul>
        <li>Déclencher des tâches longues sur ton Mac depuis ton mobile pendant tes déplacements</li>
        <li>Automatiser des applications qui n'ont pas d'API (logiciels legacy, outils desktop)</li>
        <li>Faire exécuter des workflows complexes à Claude pendant que tu fais autre chose</li>
        <li>Déléguer la navigation dans des interfaces graphiques complexes</li>
      </ul>
      <h2>Setup en 2 minutes</h2>
      <div class="code-block"># 1. Installer Claude pour Mac
# Télécharger depuis claude.ai/download

# 2. Activer Computer Use dans les paramètres
# Préférences > Fonctionnalités avancées > Computer Use

# 3. Installer Dispatch
npm install -g @dispatch-ai/cli

# 4. Configurer la connexion
dispatch init --claude</div>
      <div class="tip-box"><div class="tip-label">💡 Sécurité</div><p>Computer Use a accès complet à ton écran et tes entrées. Active-le uniquement pour les tâches spécifiques que tu lui demandes, et surveille ce qu'il fait la première fois pour chaque nouveau type de tâche.</p></div>
      <h2>Exemples de tâches déléguées</h2>
      <div class="code-block"># Depuis ton téléphone via Dispatch :
"Ouvre Figma, exporte toutes les frames de la page 'Mobile'
en PNG 2x et mets-les dans le dossier Desktop/exports"</div>
      <div class="code-block">"Lance la compilation du projet, surveille les erreurs
et envoie-moi un résumé par message quand c'est terminé"</div>
      <h2>Limitations actuelles</h2>
      <ul>
        <li>Latence de quelques secondes entre chaque action (pas du temps réel)</li>
        <li>Claude peut se tromper sur des éléments UI très petits ou non standard</li>
        <li>Nécessite que ton Mac soit allumé et connecté</li>
      </ul>
      <div class="tip-box"><div class="tip-label">⚡ Conseil pro</div><p>Pour les tâches répétitives, crée un script Dispatch que tu peux lancer en un mot depuis ton téléphone. Tu gagnes du temps et Claude fait moins d'erreurs sur des séquences qu'il a déjà exécutées.</p></div>""",
    "https://agentic-academy.fr/discover/watch/4aead526-0376-4dc3-9303-90af6a8145bb",
    "◈ Lire l'article original",
    "Claude Computer Use + Dispatch"
)

# ── PAGE 10 : 6 plugins ───────────────────────────────────────────────────────
page(
    "6-plugins-claude-code.html",
    "Les 6 Plugins Essentiels de Claude Code",
    "Les 6 extensions indispensables pour décupler les capacités de Claude Code, avec les liens directs pour les installer.",
    "article", "◈ Article",
    "Les <span>6 plugins</span> qui changent tout dans Claude Code",
    "<span>Claude Code</span><span>·</span><span>Plugins & Extensions</span><span>·</span><span>Niveau débutant</span>",
    """      <p>Claude Code devient beaucoup plus puissant avec les bons plugins. Ces 6 extensions sont celles qui ont le plus d'impact sur la productivité quotidienne — certaines ajoutent des capacités, d'autres améliorent le workflow ou réduisent les coûts.</p>
      <div style="width:60px;height:2px;background:var(--gold);margin:40px 0"></div>
      <h2>Plugin 1 — Context7 (Documentation live)</h2>
      <p>Donne à Claude accès à la documentation officielle et à jour de n'importe quelle librairie. Fini les hallucinations sur des APIs qui ont changé depuis le training.</p>
      <div class="code-block">claude mcp add context7</div>
      <h2>Plugin 2 — Playwright (Navigation web)</h2>
      <p>Connecte un navigateur headless à Claude. Il peut naviguer, scraper, tester des interfaces et prendre des screenshots.</p>
      <div class="code-block">claude mcp add playwright</div>
      <h2>Plugin 3 — 21st.dev (Composants UI)</h2>
      <p>Bibliothèque de composants générés par IA. Claude y accède pour créer des interfaces modernes plutôt que de tout coder from scratch.</p>
      <div class="code-block">claude mcp add 21st-dev</div>
      <h2>Plugin 4 — Sequential Thinking (Raisonnement)</h2>
      <p>Force Claude à décomposer les problèmes complexes étape par étape avant d'agir. Réduit les erreurs sur les tâches à plusieurs étapes.</p>
      <div class="code-block">claude mcp add sequential-thinking</div>
      <h2>Plugin 5 — Filesystem (Accès fichiers étendu)</h2>
      <p>Donne à Claude un accès sécurisé et configurable à certains dossiers de ton système, au-delà du répertoire de travail courant.</p>
      <div class="code-block">claude mcp add filesystem --path ~/Documents --path ~/Projects</div>
      <h2>Plugin 6 — Memory (Mémoire persistante)</h2>
      <p>Stocke des informations importantes entre les sessions. Claude peut noter des décisions, des préférences, des contextes et les retrouver plus tard.</p>
      <div class="code-block">claude mcp add memory</div>
      <div class="tip-box"><div class="tip-label">💡 Ordre d'installation recommandé</div><p>Commence par Context7 et Sequential Thinking — ils améliorent immédiatement la qualité des réponses sans configuration. Puis Playwright si tu fais du web scraping, 21st.dev si tu crées des interfaces.</p></div>
      <div class="tip-box"><div class="tip-label">⚡ Conseil pro</div><p>Chaque plugin activé consomme un peu de contexte système. Si tu travailles sur des tâches simples, désactive les plugins que tu n'utilises pas pour maximiser la fenêtre de contexte disponible pour ton code.</p></div>""",
    "https://agentic-academy.fr/discover/watch/8962b93c-db03-4fec-8d7e-fd8aab97be7a",
    "◈ Lire l'article original",
    "Les 6 Plugins Claude Code"
)

# ── PAGE 11 : Cloner un site ──────────────────────────────────────────────────
page(
    "cloner-site-claude.html",
    "Cloner N'importe Quel Site avec Claude Code",
    "Technique complète pour cloner n'importe quel site en moins de 10 minutes avec Claude Code et une extension Chrome.",
    "video", "▶ Vidéo · 2m 05s",
    "Cloner n'importe quel site en <span>10 minutes</span>",
    "<span>Claude Code</span><span>·</span><span>Web Cloning</span><span>·</span><span>Niveau débutant</span>",
    """      <p>Recréer un site existant pixel-perfect prenait des heures. Avec Claude Code et l'extension Chrome dédiée, tu le fais en 5 à 10 minutes. Claude voit le site, analyse sa structure visuelle et son code, puis le recrée dans ton stack tech de choix.</p>
      <div style="width:60px;height:2px;background:var(--gold);margin:40px 0"></div>
      <h2>Ce dont tu as besoin</h2>
      <ul>
        <li><strong style="color:var(--text)">Claude Code</strong> — l'outil CLI d'Anthropic</li>
        <li><strong style="color:var(--text)">Extension Chrome Claude</strong> — pour que Claude voit ton navigateur</li>
        <li><strong style="color:var(--text)">Le skill ai-website-cloner-template</strong> — les instructions spécialisées pour le cloning</li>
      </ul>
      <h2>Setup en 3 étapes</h2>
      <div class="code-block"># Étape 1 : Installer le skill de cloning
# Dans Claude Code, colle le lien du skill et demande-lui de l'installer

# Étape 2 : Installer l'extension Chrome Claude
# Télécharger depuis le Chrome Web Store : "Claude for Chrome"
# Se connecter avec ton compte Anthropic

# Étape 3 : Lancer Claude avec accès au navigateur
claude --chrome</div>
      <h2>Cloner un site</h2>
      <div class="code-block"># Une fois Claude lancé avec --chrome :
/clone-website https://example.com

# Claude va :
# 1. Ouvrir le site dans Chrome
# 2. Analyser le design, la structure, les composants
# 3. Générer le code HTML/CSS/JS équivalent
# 4. Adapter selon ton stack si tu précises (React, Vue, etc.)</div>
      <div class="tip-box"><div class="tip-label">💡 Cas d'usage principaux</div><p>Ce n'est pas fait pour copier des sites illégalement. C'est utile pour recréer ton propre design dans un nouveau stack, s'inspirer d'une mise en page pour un projet client, ou créer des maquettes rapides à partir de références visuelles.</p></div>
      <h2>Personnalisation après cloning</h2>
      <p>Une fois le clone généré, Claude peut modifier n'importe quel aspect :</p>
      <div class="code-block">"Remplace la palette de couleurs par du noir/or cyberpunk"
"Adapte ce composant hero pour qu'il soit responsive mobile"
"Ajoute une section pricing avec 3 colonnes sous la hero section"</div>
      <div class="tip-box"><div class="tip-label">⚡ Conseil pro</div><p>Clone d'abord en HTML/CSS vanilla, puis demande à Claude de migrer vers ton framework. C'est plus fiable que de demander directement du React depuis un site complexe.</p></div>""",
    "https://agentic-academy.fr/discover/watch/d6a76753-470f-4440-b54f-bb9bd20381a7",
    "▶ Voir la vidéo originale (2m 05s)",
    "Cloner un Site avec Claude"
)

# ── PAGE 12 : Redesigner une pièce ───────────────────────────────────────────
page(
    "redesigner-piece-claude.html",
    "Redesigner une Pièce en 30 Secondes avec Claude",
    "Claude Code + Nano Banana pour générer des visualisations photoréalistes de redesign d'intérieur en quelques secondes.",
    "article", "◈ Article",
    "Transformer une pièce en <span>30 secondes</span> avec Claude",
    "<span>Claude Code</span><span>·</span><span>Design & Créativité</span><span>·</span><span>Niveau débutant</span>",
    """      <p>Visualiser un projet de décoration avant de l'entreprendre était réservé aux architectes d'intérieur avec des outils professionnels. Claude Code + <strong style="color:var(--text)">Nano Banana</strong> rend ça accessible en 30 secondes, depuis une simple photo de ta pièce.</p>
      <div style="width:60px;height:2px;background:var(--gold);margin:40px 0"></div>
      <h2>Comment ça fonctionne</h2>
      <p>Nano Banana est un outil de génération d'images spécialisé dans le design d'intérieur. Connecté à Claude Code via MCP, il permet à Claude de générer des visualisations photoréalistes directement depuis tes descriptions ou des photos existantes.</p>
      <ul>
        <li>Prendre une photo de ta pièce actuelle</li>
        <li>Décrire à Claude le style que tu veux (scandinave, industriel, minimaliste...)</li>
        <li>Claude génère plusieurs variantes photoréalistes en quelques secondes</li>
        <li>Itérer en affinant la description jusqu'au résultat souhaité</li>
      </ul>
      <h2>Installation du setup</h2>
      <div class="code-block"># Ajouter le MCP Nano Banana
claude mcp add nano-banana

# Ou configurer manuellement dans .claude/settings.json
{
  "mcpServers": {
    "nano-banana": {
      "command": "npx",
      "args": ["nano-banana-mcp"]
    }
  }
}</div>
      <div class="tip-box"><div class="tip-label">💡 Prompts efficaces pour la déco</div><p>Sois précis sur le style, les matériaux et la lumière. "Salon style japandi avec bois clair, plantes vertes, canapé gris anthracite, lumière naturelle dorée" donne de bien meilleurs résultats que "salon moderne".</p></div>
      <h2>Exemples de transformations</h2>
      <div class="code-block">"Transforme cette chambre en style bohème :
murs blancs cassés, rideaux lin naturel, tapis berbère,
plantes suspendues, éclairage chaud ambiant"</div>
      <div class="code-block">"Redesigne ce salon en loft industriel new-yorkais :
béton brut, métal noir, brique apparente, mobilier vintage,
spots directionnels"</div>
      <h2>Applications pratiques</h2>
      <ul>
        <li>Visualiser un projet avant d'acheter des meubles</li>
        <li>Présenter des options à un client pour un projet de rénovation</li>
        <li>Tester différents styles sans engagement</li>
        <li>Créer du contenu visuel pour un compte déco Instagram</li>
      </ul>
      <div class="tip-box"><div class="tip-label">⚡ Conseil pro</div><p>Génère 4-5 variantes en changeant un seul élément à la fois (couleur des murs, type de mobilier, éclairage). C'est plus efficace que de tout changer d'un coup pour trouver ce qui fonctionne.</p></div>""",
    "https://agentic-academy.fr/discover/watch/5b69f28a-4255-451b-a23b-c18c2102fb45",
    "◈ Lire l'article original",
    "Redesigner une Pièce"
)

# ── PAGE 13 : Anti-flatterie ──────────────────────────────────────────────────
page(
    "instruction-anti-flatterie.html",
    "L'Instruction Anti-Flatterie pour Claude",
    "Un prompt système pour rendre Claude honnête, direct et utile — sans les réponses complaisantes par défaut.",
    "article", "◈ Article",
    "Rendre Claude <span>honnête</span> et direct",
    "<span>Claude</span><span>·</span><span>Prompting</span><span>·</span><span>Niveau débutant</span>",
    """      <p>Par défaut, Claude a tendance à être poli, encourageant et à souligner les aspects positifs de ce que tu lui montres. C'est agréable socialement, mais contre-productif quand tu as besoin de retours francs sur ton code, ton business plan ou ton contenu. L'instruction anti-flatterie corrige ça.</p>
      <div style="width:60px;height:2px;background:var(--gold);margin:40px 0"></div>
      <h2>Le problème de la flatterie par défaut</h2>
      <p>Quand tu demandes à Claude "qu'est-ce que tu penses de mon idée ?", sa réponse par défaut commence souvent par "C'est une excellente idée !" avant de nuancer. Cette validation réflexe te fait rater les vrais problèmes que Claude a identifiés mais hésite à mettre en avant.</p>
      <p>Le même phénomène avec le code : "Ce code a l'air bien structuré, cependant..." — tu veux d'abord savoir ce qui ne va pas, pas une validation.</p>
      <h2>L'instruction à coller dans tes préférences</h2>
      <div class="code-block">Ne commence jamais tes réponses par une validation ou un compliment.
Va directement au sujet sans "C'est une excellente idée", "Bien sûr !" ou
équivalents. Si je montre du code ou une idée, dis-moi d'abord ce qui
ne fonctionne pas ou pourrait être amélioré, puis ce qui est bien.
Sois direct et honnête même si c'est inconfortable.
Si quelque chose est fondamentalement mauvais, dis-le clairement.
Je préfère une critique utile à une validation creuse.</div>
      <h2>Où la coller</h2>
      <ul>
        <li><strong style="color:var(--text)">Claude.ai</strong> : Paramètres > Préférences personnalisées > Instructions système</li>
        <li><strong style="color:var(--text)">Claude Code</strong> : Dans ton <code style="color:var(--gold)">~/.claude/CLAUDE.md</code> global</li>
        <li><strong style="color:var(--text)">API</strong> : Dans le champ <code style="color:var(--gold)">system</code> de tes appels</li>
      </ul>
      <div class="tip-box"><div class="tip-label">💡 Résultat concret</div><p>Avec cette instruction, quand tu montres un business plan à Claude, il commence par "Le modèle de revenus présente trois problèmes structurels..." — exactement ce dont tu as besoin pour améliorer.</p></div>
      <h2>Variantes selon le contexte</h2>
      <div class="code-block"># Version pour la revue de code
"Quand tu analyses du code, commence par les bugs critiques,
puis les problèmes de performance, puis le style. Ne mentionne
les points positifs qu'en dernier si le temps le permet."</div>
      <div class="code-block"># Version pour le contenu
"Évalue mon contenu comme un éditeur exigeant. Ce qui est
banal, redondant ou faible doit être dit clairement en premier."</div>
      <div class="tip-box"><div class="tip-label">⚡ Conseil pro</div><p>Cette instruction ne rend pas Claude agressif ou décourageant — elle le rend simplement honnête. Il reste bienveillant, mais prioritise l'utilité sur le confort social.</p></div>""",
    "https://agentic-academy.fr/discover/watch/5104daf0-57a0-4185-ae3b-2f40401b4905",
    "◈ Lire l'article original",
    "L'Instruction Anti-Flatterie"
)

# ── PAGE 14 : Remotion ────────────────────────────────────────────────────────
page(
    "claude-remotion-videos.html",
    "Créer des Vidéos Pro avec Claude Code et Remotion",
    "Automatisez la production vidéo avec Claude et Remotion — démos, pubs et reels générés par code sans logiciel de montage.",
    "article", "◈ Article",
    "Produire des vidéos pro avec <span>Claude + Remotion</span>",
    "<span>Claude Code</span><span>·</span><span>Vidéo & Contenu</span><span>·</span><span>Niveau avancé</span>",
    """      <p><strong style="color:var(--text)">Remotion</strong> est un framework qui permet de créer des vidéos avec du code React. Couplé à Claude Code, tu décris la vidéo que tu veux et Claude génère tout le code Remotion pour la produire — animations, timing, assets, exports — sans toucher à un logiciel de montage.</p>
      <div style="width:60px;height:2px;background:var(--gold);margin:40px 0"></div>
      <h2>Pourquoi c'est puissant</h2>
      <ul>
        <li>Vidéos 100% reproductibles et versionnées dans Git</li>
        <li>Changements programmatiques : modifier la couleur ou le texte de 100 scènes en une ligne</li>
        <li>Templates réutilisables pour du contenu en série</li>
        <li>Export en haute qualité sans abonnement logiciel</li>
        <li>Intégration dans des pipelines CI/CD pour de la vidéo automatisée</li>
      </ul>
      <h2>Installation</h2>
      <div class="code-block"># Créer un projet Remotion
npx create-video@latest my-video
cd my-video
npm install

# Lancer le player de prévisualisation
npm start</div>
      <h2>Exemple de prompt pour Claude</h2>
      <div class="code-block">"Crée une vidéo Remotion de 30 secondes pour présenter
mon SaaS AutomationBoost :
- 0-5s : Logo animé avec effet glitch sur fond noir
- 5-15s : 3 features défilantes avec icônes et texte
- 15-25s : Témoignage client avec avatar et citation
- 25-30s : CTA avec URL et bouton pulsant
Style : cyberpunk, palette or/noir, font Orbitron"</div>
      <div class="tip-box"><div class="tip-label">💡 Cas d'usage concrets</div><p>Démos produit pour Product Hunt, vidéos d'onboarding in-app, reels LinkedIn automatisés depuis des données, vidéos de changelog après chaque release.</p></div>
      <h2>Automatiser la production en série</h2>
      <div class="code-block"># Générer 30 reels différents depuis un JSON de données
const episodes = require('./episodes.json');
episodes.forEach(ep => {
  renderMedia({
    composition: 'EpisodeTemplate',
    inputProps: ep,
    outputLocation: `out/episode-${ep.id}.mp4`
  });
});</div>
      <div class="tip-box"><div class="tip-label">⚡ Conseil pro</div><p>Commence par un template simple (texte + logo + animation entrée/sortie), valide que le rendu te plaît, puis demande à Claude de l'enrichir progressivement. Évite de tout générer d'un coup sur une vidéo complexe.</p></div>""",
    "https://agentic-academy.fr/discover/watch/3ebf6540-2e48-4c9c-a7ab-b16119b67731",
    "◈ Lire l'article original",
    "Claude Code + Remotion"
)

# ── PAGE 15 : RuFlo ───────────────────────────────────────────────────────────
page(
    "ruflo-stack.html",
    "RuFlo Stack – Claude Code en Armée d'Agents",
    "Installez RuFlo pour orchestrer 100+ agents spécialisés directement dans Claude Code et traiter des tâches complexes.",
    "article", "◈ Article",
    "<span>RuFlo</span> — orchestrer 100+ agents dans Claude Code",
    "<span>Claude Code</span><span>·</span><span>Orchestration</span><span>·</span><span>Niveau avancé</span>",
    """      <p><strong style="color:var(--text)">RuFlo</strong> est un stack d'orchestration qui transforme Claude Code en coordinateur d'agents. Au lieu d'un seul modèle qui fait tout séquentiellement, RuFlo dispatche les tâches vers des agents spécialisés qui travaillent en parallèle, avec un agent orchestrateur qui consolide les résultats.</p>
      <div style="width:60px;height:2px;background:var(--gold);margin:40px 0"></div>
      <h2>La différence avec un usage classique</h2>
      <p>Sans RuFlo : tu poses une question complexe à Claude, il répond de son mieux en faisant tout lui-même, dans la limite de sa fenêtre de contexte.</p>
      <p>Avec RuFlo : l'orchestrateur décompose la tâche, dispatche vers des agents spécialisés (un chercheur, un analyste, un rédacteur, un vérificateur), consolide les résultats. Chaque agent est optimisé pour sa sous-tâche.</p>
      <h2>Installation</h2>
      <div class="code-block"># Cloner le stack RuFlo
git clone https://github.com/ruflo-ai/ruflo-stack
cd ruflo-stack

# Installer les dépendances
npm install

# Configurer les agents
cp agents.example.json agents.json
# Éditer agents.json pour activer les agents dont tu as besoin

# Connecter à Claude Code
claude mcp add ruflo --config ./agents.json</div>
      <div class="tip-box"><div class="tip-label">💡 Quand utiliser RuFlo</div><p>RuFlo est utile quand tes tâches dépassent régulièrement la fenêtre de contexte d'une session, ou quand tu veux paralléliser plusieurs analyses indépendantes sur le même problème.</p></div>
      <h2>Exemple d'orchestration</h2>
      <div class="code-block">"Analyse mon codebase et produis un rapport complet :
- Agent sécurité : vulnerabilités et CVEs
- Agent performance : bottlenecks et optimisations
- Agent qualité : dette technique et duplications
- Agent documentation : écarts entre code et docs
Synthèse finale avec priorités d'action"</div>
      <p>RuFlo lance les 4 agents simultanément, chacun avec son propre contexte optimisé pour sa spécialité, puis l'orchestrateur rédige la synthèse à partir de leurs rapports.</p>
      <h2>Agents disponibles dans le stack</h2>
      <ul>
        <li>Security Auditor, Performance Analyzer, Code Quality Checker</li>
        <li>Documentation Auditor, Test Coverage Analyzer</li>
        <li>Architecture Reviewer, Dependency Auditor</li>
        <li>Et 90+ autres agents spécialisés</li>
      </ul>
      <div class="tip-box"><div class="tip-label">⚡ Conseil pro</div><p>Commence avec 3-4 agents sur des tâches que tu répètes souvent. Une fois que tu comprends le pattern d'orchestration, créer tes propres agents personnalisés devient naturel.</p></div>""",
    "https://agentic-academy.fr/discover/watch/f1c18325-936a-4df2-aa8f-3c98e06ade6b",
    "◈ Lire l'article original",
    "RuFlo Stack"
)

# ── PAGE 16 : 1000 skills ─────────────────────────────────────────────────────
page(
    "1000-skills-claude-code.html",
    "+1 000 Skills pour Claude Code en Une Commande",
    "Débloquez plus de 1000 compétences dans Claude Code avec une seule commande — détection automatique du bon skill.",
    "article", "◈ Article",
    "+1 000 compétences en <span>une commande</span>",
    "<span>Claude Code</span><span>·</span><span>Skills & Plugins</span><span>·</span><span>Niveau débutant</span>",
    """      <p>Les skills Claude Code sont des instructions spécialisées qui améliorent drastiquement la qualité des réponses sur des domaines spécifiques. Au lieu d'en installer un par un, cette technique te donne accès à plus de 1 000 skills d'un coup, avec une détection automatique de celui à utiliser selon ta demande.</p>
      <div style="width:60px;height:2px;background:var(--gold);margin:40px 0"></div>
      <h2>Comment fonctionnent les skills</h2>
      <p>Un skill est un fichier Markdown qui contient des instructions précises pour Claude sur comment aborder un type de tâche spécifique. Par exemple, le skill "TDD" lui enseigne à toujours écrire les tests avant le code. Le skill "debugging" lui impose une méthode systématique d'analyse.</p>
      <p>Sans skills, Claude improvise selon ses données d'entraînement. Avec les bons skills, il suit des processus éprouvés par des praticiens experts.</p>
      <h2>La commande unique</h2>
      <div class="code-block"># Dans Claude Code, tape cette commande :
/install-superpowers

# Claude va :
# 1. Télécharger le registry complet des skills communautaires
# 2. Les organiser dans .claude/skills/
# 3. Configurer la détection automatique dans ton CLAUDE.md
# 4. Te confirmer les 1000+ skills disponibles</div>
      <div class="tip-box"><div class="tip-label">💡 Détection automatique</div><p>Après installation, Claude détecte quel skill est pertinent pour chaque demande. Si tu lui demandes de "debugger un bug", il active automatiquement le skill systematic-debugging. Tu n'as rien à faire.</p></div>
      <h2>Catégories de skills disponibles</h2>
      <ul>
        <li><strong style="color:var(--text)">Développement</strong> : TDD, debugging, code review, refactoring, sécurité</li>
        <li><strong style="color:var(--text)">Architecture</strong> : design patterns, microservices, API design</li>
        <li><strong style="color:var(--text)">DevOps</strong> : CI/CD, Docker, Kubernetes, monitoring</li>
        <li><strong style="color:var(--text)">Productivité</strong> : brainstorming, planification, rédaction technique</li>
        <li><strong style="color:var(--text)">Domaines métier</strong> : e-commerce, SaaS, marketing, finance</li>
      </ul>
      <h2>Activer un skill manuellement</h2>
      <div class="code-block"># Si tu veux forcer un skill spécifique :
/skill tdd "Implémente la feature de panier d'achat"

/skill code-reviewer "Revue de ce fichier avant le merge"

/skill brainstorming "Nouvelles features pour mon SaaS"</div>
      <div class="tip-box"><div class="tip-label">⚡ Conseil pro</div><p>Après quelques semaines, identifie les 5-10 skills que tu utilises le plus. Ouvre ces fichiers dans <code style="color:var(--gold)">.claude/skills/</code> et personnalise-les selon ton contexte — les principes généraux deviennent des instructions taillées pour ton projet.</p></div>""",
    "https://agentic-academy.fr/discover/watch/e4581d1f-6247-42ce-80f2-1242447e4159",
    "◈ Lire l'article original",
    "+1 000 Skills en Une Commande"
)

print("\n✅ Toutes les pages générées !")
