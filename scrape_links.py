import json
from playwright.sync_api import sync_playwright

def scrape_with_links():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://agentic-academy.fr/discover", wait_until="networkidle", timeout=30000)

        # Extraire les données complètes de chaque card
        resources = page.evaluate("""
        () => {
            const cards = document.querySelectorAll('[class*="card"]');
            const results = [];
            cards.forEach(card => {
                const title = card.querySelector('h2, h3, [class*="title"], strong, b')?.innerText?.trim();
                const desc = card.querySelector('p, [class*="desc"], [class*="body"]')?.innerText?.trim();
                const allText = card.innerText?.trim();

                // Chercher tous les liens dans la card
                const links = Array.from(card.querySelectorAll('a')).map(a => ({
                    href: a.href,
                    text: a.innerText?.trim()
                }));

                // Lien de la card elle-même
                const cardLink = card.tagName === 'A' ? card.href :
                                 card.closest('a')?.href || null;

                // Type de contenu (Article, Vidéo, etc.)
                const typeEl = card.querySelector('[class*="badge"], [class*="tag"], [class*="type"]');
                const type = typeEl?.innerText?.trim();

                // Durée si vidéo
                const durationMatch = allText?.match(/\d+m\s*\d+s/);

                results.push({
                    title: title || allText?.split('\\n')[0],
                    description: desc,
                    allText: allText,
                    cardLink,
                    links,
                    type,
                    duration: durationMatch ? durationMatch[0] : null
                });
            });
            return results;
        }
        """)

        print(f"=== {len(resources)} ressources ===\n")
        for i, r in enumerate(resources):
            print(f"--- Ressource {i+1} ---")
            print(f"Titre: {r.get('title', '')[:80]}")
            print(f"CardLink: {r.get('cardLink')}")
            print(f"Links: {r.get('links')}")
            print(f"Type: {r.get('type')} | Durée: {r.get('duration')}")
            print(f"Texte: {r.get('allText', '')[:200]}")
            print()

        # Sauvegarder en JSON
        with open("/work/resources.json", "w", encoding="utf-8") as f:
            json.dump(resources, f, ensure_ascii=False, indent=2)

        print("Sauvegardé dans /work/resources.json")
        browser.close()

if __name__ == "__main__":
    scrape_with_links()
