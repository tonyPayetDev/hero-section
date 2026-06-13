# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

```bash
npm run setup   # installs playwright + chromium (first time only)
```

## Running Scripts

Always execute from the skill directory so `require('./lib/helpers')` resolves correctly:

```bash
cd /work/.agents/skills/playwright-skill && node run.js /tmp/my-script.js
```

Three input modes:
- `node run.js /tmp/script.js` — file path
- `node run.js "await page.goto('...')"` — inline Playwright commands (auto-wrapped)
- `cat script.js | node run.js` — stdin

## Architecture

`run.js` is the universal entry point. It:
1. Auto-installs Playwright via `npm install` + `npx playwright install chromium` if missing
2. Reads code from file/arg/stdin
3. Wraps bare Playwright commands in `require('playwright')` + async IIFE boilerplate — only if no `require()` is present
4. Writes to a `.temp-execution-{timestamp}.js` file and `require()`s it
5. Cleans old temp files on startup

Scripts should be written to `/tmp/playwright-test-*.js`, never inside the skill directory.

## helpers.js API

```javascript
const helpers = require('./lib/helpers');
```

| Function | Purpose |
|----------|---------|
| `detectDevServers(extraPorts?)` | Probes localhost ports 3000/3001/5173/8080/… — call first for local testing |
| `createContext(browser, opts)` | Creates context with 1280×720 viewport + auto env headers |
| `launchBrowser(type, opts)` | Launches chromium/firefox/webkit; headless unless `HEADLESS=false` |
| `safeClick(page, sel, opts)` | Click with 3 retries + visibility wait |
| `safeType(page, sel, text, opts)` | Fill + optional `slow` mode |
| `waitForPageReady(page, opts)` | `networkidle` wait + optional selector |
| `takeScreenshot(page, name, opts)` | Saves `name-{timestamp}.png` |
| `authenticate(page, creds, sels)` | Form-based login with smart selector defaults |
| `extractTexts(page, sel)` | Returns `string[]` from matching elements |
| `extractTableData(page, sel)` | Returns `{ headers, rows }` |
| `handleCookieBanner(page, ms)` | Tries common accept selectors |
| `retryWithBackoff(fn, n, delay)` | Exponential backoff retry |
| `getExtraHeadersFromEnv()` | Reads `PW_HEADER_NAME`/`PW_HEADER_VALUE` or `PW_EXTRA_HEADERS` JSON |

## Environment Variables

| Variable | Effect |
|----------|--------|
| `HEADLESS=false` | Show browser window (default: headless) |
| `SLOW_MO=100` | Slow down actions by N ms |
| `PW_HEADER_NAME` + `PW_HEADER_VALUE` | Single extra HTTP header on all requests |
| `PW_EXTRA_HEADERS` | JSON object of multiple extra headers |

## Key Conventions

- Test scripts go in `/tmp/`, not in this directory
- `createContext()` automatically merges `PW_EXTRA_HEADERS` — prefer it over `browser.newContext()` directly
- For scripts that use raw `browser.newContext()`, use the injected `getContextOptionsWithHeaders()` helper that `run.js` injects at wrap time
- Default browser is chromium; `launchBrowser('firefox')` or `launchBrowser('webkit')` for others
- `SKILL.md` is the user-facing documentation; this file is for working on the skill internals
