# LeadFlow Video Factory - Design Spec

**Date:** June 13, 2026  
**Author:** Claude Code  
**Project:** Automated Video Generation System for n8n Niche  

---

## 1. Project Overview

**Objective:** Build a fully automated video production system that generates 2 short-form videos per day (15-30 seconds) on n8n/automation topics and publishes them across TikTok, YouTube Shorts, and Instagram Reels.

**Success Criteria:**
- Generate 2 videos/day consistently (60/month, 730/year)
- Maintain quality (viewable, engaging, accurate)
- Auto-publish across 3 platforms
- Track analytics for content optimization
- Zero manual intervention (fully automated)

**Timeline Goal:** Launch within 2 weeks with MVP, expand features after 3 months

---

## 2. Content Strategy

### 2.1 Content Mix (Rotation)
Three content types rotate daily:

| Type | Format | Example | Duration |
|------|--------|---------|----------|
| **Hacks** | Problem → Solution | "Save 5 hours with this n8n trigger" | 15-20s |
| **Use Cases** | Situation → Workflow demo | "Automate your email nurturing with n8n" | 20-30s |
| **Fails** | Wrong way vs Right way | "Everyone does this wrong in n8n" | 15-25s |

**Rotation:** Hack → Use Case → Fail → Repeat  
**Daily Output:** 2 videos/day = 1 Hack + 1 Use Case OR Fail combo

### 2.2 Script Templates
Pre-built templates for each type in Supabase:
- 30+ Hack templates
- 30+ Use Case templates  
- 20+ Fail/Comparison templates

Templates contain placeholders for:
- Main tip/workflow name
- Benefit (time saved, $ saved, complexity reduced)
- Call-to-action (subscribe, check bio, learn more)

---

## 3. System Architecture

### 3.1 Component Overview

```
┌─────────────────────────────────────────────────────┐
│                  DAILY FLOW (2x/day)                │
├─────────────────────────────────────────────────────┤
│                                                     │
│  [1] Script Generator (Claude AI)                  │
│      ├─ Selects template by rotation               │
│      ├─ Fills in n8n tip/workflow                  │
│      └─ Returns: Title + Script + Metadata         │
│           ↓                                         │
│  [2] Video Generator (Remotion)                    │
│      ├─ Takes script                               │
│      ├─ Renders with B-roll, text, music          │
│      └─ Returns: MP4 (TikTok/Shorts/Reels format)  │
│           ↓                                         │
│  [3] Publisher (n8n Automation)                    │
│      ├─ TikTok upload                              │
│      ├─ YouTube Shorts upload                      │
│      ├─ Instagram Reels upload                     │
│      └─ Returns: Video IDs + URLs                  │
│           ↓                                         │
│  [4] Analytics Logger (Supabase)                   │
│      └─ Stores video metadata + URLs               │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 3.2 Core Components

**Component 1: Script Generator**
- Tool: Claude API (claude-opus or claude-sonnet)
- Input: Content type (hack/usecase/fail), Supabase template
- Output: { title, script_text, hook, cta, duration_estimate, metadata }
- Latency: ~2 seconds per script
- Runs: 2x/day (6 AM + 3 PM UTC)

**Component 2: Video Generator (Remotion + Hyperframe)**
- **Remotion:** React-based video structure
  - Input: Script JSON + template design
  - Output: Video base with text, B-roll, music overlay
  - Latency: ~15 seconds
  - Handles: Layout, text placement, timing, audio sync
  
- **Hyperframe:** Motion design & animations
  - Input: Remotion output + animation specs
  - Transforms: Adds smooth transitions, text animations, visual effects
  - Latency: ~15 seconds
  - Handles: Entrance animations, transitions between clips, text reveals, scale/rotation effects
  
- **Final Output:** MP4 file (1080p, optimized for short-form)
- **Total latency:** ~30 seconds per video
- **Formats:** TikTok (1080x1920), YouTube Shorts (1080x1920), Instagram (1080x1350)

**Component 3: Publisher**
- Tool: n8n automation workflow
- Input: MP4 + metadata (title, captions, hashtags)
- Integrations: TikTok API, YouTube Data API, Instagram Graph API
- Output: Published video links + IDs
- Scheduling: Optimal post times per platform
- Features: Auto-hashtags, caption generation, thumbnail selection

**Component 4: Analytics**
- Tool: Supabase (PostgreSQL) + simple dashboard
- Tracks: Views, likes, comments, shares per video
- Metrics: Engagement rate, view duration, type performance
- Updates: Every 24 hours via API polling

---

## 4. Data Schema (Supabase)

### 4.1 Tables

**templates** (templates for script generation)
```
- id (UUID)
- type ('hack' | 'usecase' | 'fail')
- template_text (TEXT) — has {PLACEHOLDER} markers
- category (TEXT) — 'productivity', 'integration', 'advanced'
- example_output (TEXT) — sample filled-in script
- created_at
```

**scripts** (generated scripts)
```
- id (UUID)
- template_id (FK → templates)
- title (TEXT)
- script_text (TEXT)
- cta (TEXT)
- duration_estimate (INT) — seconds
- metadata (JSONB) — {hook, benefit, keywords}
- created_at
```

**videos** (generated videos)
```
- id (UUID)
- script_id (FK → scripts)
- file_path (TEXT) — local or S3 path
- duration (INT) — actual duration in seconds
- format (TEXT) — 'tiktok', 'youtube', 'instagram'
- created_at
```

**published_videos** (tracking published content)
```
- id (UUID)
- video_id (FK → videos)
- platform ('tiktok' | 'youtube' | 'instagram')
- platform_video_id (TEXT) — native ID from platform
- url (TEXT)
- published_at
- views (INT) — last synced count
- likes (INT)
- comments (INT)
- shares (INT)
- updated_at
```

---

## 5. Implementation Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| Script Gen | Claude API | Generate n8n tips based on templates |
| Video Base | Remotion | Render MP4 structure with text, B-roll, audio |
| Motion Design | Hyperframe | Add smooth animations, transitions, visual effects |
| Publishing | n8n | Multi-platform upload automation |
| Storage | Supabase (PostgreSQL) | Script templates, video metadata, analytics |
| B-roll Library | Local MP4s / Stock footage API | Background videos for Remotion |
| Music | Royalty-free API (Epidemic Sound, AudioJungle) | Background music per video type |
| Orchestration | n8n or Supabase Cron | Daily trigger at 6 AM + 3 PM |

---

## 6. Workflow: Daily Execution

### 6.1 Morning Run (6 AM UTC)
1. **n8n trigger** → calls Claude API
2. **Claude generates** Script #1 (e.g., Hack)
3. **Remotion renders** Video #1 base (text, B-roll, audio)
4. **Hyperframe applies** motion design & animations
5. **n8n publishes** to TikTok, YouTube, Instagram
6. **Supabase logs** video metadata + URLs

### 6.2 Afternoon Run (3 PM UTC)
1. Same flow for Script #2 (e.g., Use Case or Fail)

### 6.3 Nightly Analytics Sync (11 PM UTC)
1. **n8n polls** TikTok/YouTube/Instagram APIs
2. **Updates** view counts, likes, comments
3. **Stores** in `published_videos` table

---

## 7. Error Handling & Fallbacks

| Failure | Handling |
|---------|----------|
| Claude API timeout | Retry 3x with exponential backoff; use cached template if all fail |
| Remotion render failure | Log error, notify via Slack, skip that day's video |
| Upload to platform fails | Retry 2x; if fails, queue for manual retry next day |
| Analytics API down | Skip sync; retry next cycle |

**Monitoring:** Simple dashboard showing daily success/failure rate + last 30 days of videos

---

## 8. Quality Assurance

### 8.1 Script Quality
- Claude output must pass: word count check, hook strength, CTA clarity
- Manual review of first 10 scripts before auto-approval

### 8.2 Video Quality
- Remotion must output: valid MP4, duration 15-30s, text readable
- Aspect ratio correct for each platform
- No obvious visual glitches

### 8.3 Publishing Quality
- Must reach published state on all 3 platforms within 2 hours
- Captions/hashtags must match metadata
- Analytics must sync within 24 hours

---

## 9. Scalability & Future Features

### 9.1 Phase 1 (MVP - Week 1-2)
- ✅ 2 videos/day on TikTok + YouTube Shorts only
- ✅ 3 content types in rotation
- ✅ Basic analytics dashboard

### 9.2 Phase 2 (Week 3-4)
- Add Instagram Reels
- Add email notifications (daily digest)
- Improve B-roll library (50+ videos)

### 9.3 Phase 3 (Month 2-3)
- A/B test script templates
- Add trending hashtag integration
- Subscriber-only content tier

### 9.4 Phase 4+ (Monetization ready)
- Sell script templates on Gumroad
- Launch automation course
- Build community workspace

---

## 10. Success Metrics (First 90 Days)

| Metric | Target | Baseline |
|--------|--------|----------|
| Videos published | 180 (2/day × 90) | 0 |
| Total views | 50K+ | 0 |
| Average views/video | 280+ | 0 |
| Engagement rate | 3%+ | 0 |
| Subscriber growth | 500+ | 0 |

---

## 11. Dependencies & Setup

### Required:
- Claude API key (OpenAI)
- Remotion installed + React environment
- n8n instance (cloud or self-hosted)
- Supabase project (PostgreSQL)
- TikTok Creator API access
- YouTube Data API v3 key
- Instagram Graph API access

### Optional:
- Slack integration (error alerts)
- Vercel (Remotion hosting)
- S3 (video storage)

---

## 12. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Platform API rate limits | Videos don't publish | Implement smart queuing, spread uploads across 1 hour |
| Claude costs scale | Budget overrun | Cache templates, batch requests, set monthly budget limit |
| B-roll copyright | Takedown notices | Use only licensed/royalty-free content |
| Low initial engagement | Discouragement | Expected for first 2-4 weeks; optimize based on analytics |
| Remotion rendering fails consistently | No videos | Test locally first; use fallback render engine (FFmpeg) |

---

## 13. File Structure

```
/work/leadflow-video-factory/
├── src/
│   ├── claude/
│   │   └── script-generator.ts     (Claude API wrapper)
│   ├── remotion/
│   │   ├── TipVideo.tsx            (Remotion base structure)
│   │   ├── UseCase.tsx
│   │   └── FailVideo.tsx
│   ├── hyperframe/
│   │   ├── animations/
│   │   │   ├── textReveal.ts       (Text animation presets)
│   │   │   ├── transitions.ts      (Transition effects)
│   │   │   └── entrance.ts         (Entrance animations)
│   │   └── apply-motion.ts         (Hyperframe integration)
│   ├── n8n/
│   │   └── workflows/
│   │       ├── daily-publish.json  (n8n workflow)
│   │       └── analytics-sync.json
│   ├── supabase/
│   │   └── migrations/
│   │       └── 001_init_schema.sql
│   └── utils/
│       ├── config.ts               (API keys, constants)
│       └── logger.ts
├── public/
│   ├── broll/
│   │   ├── hack-1.mp4
│   │   ├── usecase-1.mp4
│   │   └── ... (50+ videos)
│   └── music/
│       ├── upbeat.mp3
│       └── ... (10+ tracks)
├── docs/
│   └── superpowers/
│       └── specs/
│           └── 2026-06-13-leadflow-video-factory-design.md (this file)
├── package.json
├── .env.example
└── README.md
```

---

## 14. Next Steps After Approval

1. **Write Implementation Plan** (writing-plans skill)
2. **Set up repo structure & dependencies**
3. **Build Claude script generator**
4. **Build Remotion video components**
5. **Build n8n publishing workflow**
6. **Test end-to-end (1 video cycle)**
7. **Deploy & launch**

---

**Design Status:** ✅ READY FOR REVIEW & APPROVAL
