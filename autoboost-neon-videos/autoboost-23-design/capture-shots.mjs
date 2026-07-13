import { chromium } from "playwright";
import fs from "node:fs";

const CHROME = "/home/claude/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome";
const OUT = "shots";
fs.mkdirSync(OUT, { recursive: true });

// name -> url. Local sites are served by serve.mjs on 8081/8082/8083.
const targets = [
  { name: "21st", url: "https://21st.dev", wait: 6000 },
  { name: "ab", url: "https://automatisationboost.com", wait: 4000 },
  { name: "pizza", url: "http://localhost:8081", wait: 3000 },
  { name: "clos", url: "http://localhost:8082", wait: 3000 },
  { name: "sante", url: "http://localhost:8083", wait: 3000 },
];

const browser = await chromium.launch({
  executablePath: CHROME,
  args: ["--disable-blink-features=AutomationControlled", "--no-sandbox"],
});

const ctx = await browser.newContext({
  viewport: { width: 1600, height: 900 },
  deviceScaleFactor: 1.5,
  userAgent:
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
  locale: "fr-FR",
});
// Hide the automation flag that bot-checkpoints look for.
await ctx.addInitScript(() => {
  Object.defineProperty(navigator, "webdriver", { get: () => undefined });
});

for (const t of targets) {
  const page = await ctx.newPage();
  try {
    await page.goto(t.url, { waitUntil: "networkidle", timeout: 45000 });
    await page.waitForTimeout(t.wait);
    await page.screenshot({ path: `${OUT}/${t.name}.png` });
    const title = await page.title();
    console.log(`OK   ${t.name.padEnd(6)} ${title.slice(0, 60)}`);
  } catch (e) {
    console.log(`FAIL ${t.name.padEnd(6)} ${String(e.message).split("\n")[0].slice(0, 80)}`);
  }
  await page.close();
}

await browser.close();
