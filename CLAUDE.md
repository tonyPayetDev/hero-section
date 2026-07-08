# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**Monorepo** owned by Tony PAYET (`tonyPayetDev` on GitHub). Three categories of content co-exist at the root:

1. **React/Vite root app** — tutorial/reference site (`index.html`, `main.jsx`, `App.jsx`, `HeroSection.jsx`)
2. **Static client websites** — plain HTML/CSS projects (restaurants, SEO, hotels, etc.) deployed via `deploy-to-coolify`
3. **Active subprojects** with their own CLAUDE.md and tech stack:
   - `n8n-mcp-server/` — NestJS + TypeScript MCP server (see its own CLAUDE.md)
   - `snip/` — Go CLI token filter proxy (see its own CLAUDE.md)
   - `ia-dev-2026-motion/` — HyperFrames video compositions (see its own CLAUDE.md)
   - `n8n-skills/` — Claude Code skill collection for n8n workflows
   - `automationboost/` — Git submodule, marketing site

**Always check for a subdirectory-level CLAUDE.md before working in a subproject.**

## Root React App Commands

```bash
npm install          # install deps
npm run dev          # dev server on port 5173 (HMR, auto-opens browser)
npm run build        # production build → dist/
npm run preview      # preview production build locally
```

No linting or type-checking configured by default at root level.

## Deployment — deploy-to-coolify Skill

To deploy any static site subproject to Coolify:

```
/deploy-to-coolify <path-to-subproject>
```

The skill: pushes to GitHub (`tonyPayetDev`), creates/updates app in Coolify, polls until `running`, verifies HTTP 200.

- Coolify instance: `http://158.220.127.234:8000/api/v1`
- All projects deploy to `main` branch
- If no `Dockerfile` exists, the skill creates a minimal nginx one automatically
- Coolify environment UUIDs are documented in `docs/freelance-sites-mapping.md`

For **submodules** (e.g., `automationboost`): commit/push inside the submodule first, then update the parent ref.

## Architecture: Root React App

`App.jsx` renders a single `<HeroSection />`. All UI lives in `HeroSection.jsx`, which uses:
- **Framer Motion** — scroll-triggered `FadeUp`, word-by-word `SplitTitle`, animated `Counter`, cursor-following portrait
- **Tailwind CSS** — utility classes in JSX; directives in `index.css`; processed by PostCSS at build time
- **`style.css`** — legacy/global styles used by static HTML subprojects (independent of React/Tailwind)

## MCP Servers Configured

| Name | Purpose |
|---|---|
| `21st-dev-magic` | 21st.dev component registry (UI components) |
| `wordpress` | WordPress site management via MCP |
| `n8n` (env) | n8n workflow automation at `https://n7n.automatisationboost.com` |

`N8N_API_URL` and `N8N_API_KEY` are set as env in `.claude/settings.json`.

## Skills Available

Key custom skills (invoke with `/skill-name`):

| Skill | Use case |
|---|---|
| `deploy-to-coolify` | Deploy a static folder to Coolify |
| `avatar-reel` | Full avatar reel video pipeline (HyperFrames + TTS + subtitles) |
| `veille-to-video` | AI watch script → motion design video |
| `hyperframes-read-first` | **Start here** for any video/animation/motion work |
| `n8n-mcp-tools-expert` | **Start here** before using any n8n MCP tool |
| `ui-ux-pro-max` | Design system, palettes, font pairings, component styles |
| `playwright-skill` | Browser automation and UI testing |

## Custom Agents

`.claude/agents/business-orchestrator.md` — orchestrates full business analysis → dev delegation → KPI verification loop for Tony's freelance operation.

## Video Pipelines

For any video/motion work, always invoke `/hyperframes-read-first` first — it routes to the right sub-skill. Key pipeline components:
- **TTS**: WaveSpeed direct API, model `wavespeed-ai/qwen3-tts/voice-clone` (not `omnivoice`, deprecated). Fallback: n8n webhook `/webhook/tts-gen` (workflow ID `6InNNRjMJxiteEkV`)
- **Avatar**: green screen removal via `geq` filter (not `chromakey`), crop square before mask, crop from `y=0`, despill green channel to remove fringe
- **FFmpeg**: Use `-stream_loop -1 -t DUR` on input for looping (not `trim` in filter graph)
- **avatar-reel duration**: final video must be 30s–1min, never under 30s

## Telegram Notifications

A `SessionStart` hook fires a Telegram listener on every session start (configured in `.claude/settings.local.json`). This is expected behavior.

## Conventions

- Respond in French; code, commits, comments, and docs in English
- GitHub account for all deployments: `tonyPayetDev`
- No test suite at root level — manual verification via `npm run preview` or `playwright-skill`
