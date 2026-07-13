import { chromium } from "playwright";
import fs from "node:fs";

const CHROME = "/home/claude/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome";
fs.mkdirSync("shots", { recursive: true });

const targets = [
  { name: "superpowers", url: "https://github.com/obra/superpowers" },
  { name: "skills", url: "https://github.com/anthropics/skills" },
  { name: "claude-mem", url: "https://github.com/thedotmack/claude-mem" },
];

const browser = await chromium.launch({
  executablePath: CHROME,
  args: ["--disable-blink-features=AutomationControlled", "--no-sandbox"],
});
const ctx = await browser.newContext({
  viewport: { width: 1600, height: 900 },
  deviceScaleFactor: 1.5,
  colorScheme: "dark",
  userAgent:
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
});

for (const t of targets) {
  const page = await ctx.newPage();
  try {
    await page.goto(t.url, { waitUntil: "networkidle", timeout: 45000 });
    await page.waitForTimeout(2500);
    await page.screenshot({ path: `shots/${t.name}.png` });
    console.log(`OK   ${t.name.padEnd(12)} ${(await page.title()).slice(0, 60)}`);
  } catch (e) {
    console.log(`FAIL ${t.name.padEnd(12)} ${String(e.message).split("\n")[0].slice(0, 70)}`);
  }
  await page.close();
}
await browser.close();
