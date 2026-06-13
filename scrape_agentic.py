import json
from playwright.sync_api import sync_playwright

def scrape_free_resources():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Chargement de la page...")
        page.goto("https://agentic-academy.fr/discover", wait_until="networkidle", timeout=30000)

        # Screenshot pour debug
        page.screenshot(path="/work/screen1.png")

        # Afficher le contenu visible
        content = page.content()
        print("Taille du HTML:", len(content))

        # Chercher les boutons/filtres avec "gratuit" ou "free"
        buttons = page.locator("button, a, [role='tab'], [role='button']").all()
        print(f"\n--- {len(buttons)} éléments cliquables trouvés ---")
        for btn in buttons[:30]:
            try:
                text = btn.inner_text().strip()
                if text:
                    print(f"  [{btn.get_attribute('class') or 'no-class'}] '{text}'")
            except:
                pass

        # Chercher spécifiquement "gratuit"
        print("\n--- Recherche 'gratuit' dans la page ---")
        gratuit_elements = page.locator("text=/gratuit/i").all()
        print(f"Trouvé {len(gratuit_elements)} éléments avec 'gratuit'")

        for el in gratuit_elements:
            try:
                print(f"  Tag: {el.evaluate('el => el.tagName')}, Texte: '{el.inner_text().strip()[:100]}'")
            except:
                pass

        # Cliquer sur le premier élément "gratuit" trouvé
        if gratuit_elements:
            print("\nClic sur le premier élément 'gratuit'...")
            gratuit_elements[0].click()
            page.wait_for_timeout(2000)
            page.screenshot(path="/work/screen2.png")

        # Extraire les cards/ressources
        print("\n--- Extraction des ressources ---")

        # Sélecteurs courants pour les cards
        selectors = [
            "article", ".card", "[class*='card']", "[class*='resource']",
            "[class*='item']", "li[class]", ".grid > div", ".resource"
        ]

        resources = []
        for sel in selectors:
            items = page.locator(sel).all()
            if items:
                print(f"Sélecteur '{sel}': {len(items)} éléments")
                if len(items) > 2:
                    for item in items[:20]:
                        try:
                            text = item.inner_text().strip()
                            link = item.locator("a").first.get_attribute("href") if item.locator("a").count() > 0 else None
                            if text and len(text) > 10:
                                resources.append({"text": text[:300], "link": link, "selector": sel})
                        except:
                            pass
                    if resources:
                        break

        # Afficher tout le texte visible de la page
        print("\n--- Texte complet de la page (premiers 3000 chars) ---")
        body_text = page.locator("body").inner_text()
        print(body_text[:3000])

        # Sauvegarder le HTML complet
        with open("/work/page_content.html", "w") as f:
            f.write(page.content())

        print(f"\n--- {len(resources)} ressources extraites ---")
        for r in resources:
            print(json.dumps(r, ensure_ascii=False, indent=2))

        browser.close()
        return resources

if __name__ == "__main__":
    scrape_free_resources()
