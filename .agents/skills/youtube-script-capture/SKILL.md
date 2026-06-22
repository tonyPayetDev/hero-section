---
name: youtube-script-capture
description: Use when extracting transcript, script content, or key frame captures from a YouTube video URL. Handles subtitles, auto-generated captions, frame sampling at key moments, and structured markdown output. Works for Shorts and regular videos.
---

# YouTube Script & Capture Extractor

Extracts **transcript + key frames** from any YouTube video. Uses yt-dlp for subtitles + ffmpeg for frames. Playwright fallback for description when running on cloud IP (YouTube blocks server requests).

## Prerequisites

```bash
pip3 install yt-dlp --break-system-packages   # if not installed
ffmpeg --version                               # must be present
```

## Step 1 — Detect environment & set OUTPUT_DIR

```bash
VIDEO_URL="<URL_FOURNIE>"
VIDEO_ID=$(echo "$VIDEO_URL" | grep -oP '[?&v=|shorts/]\K[a-zA-Z0-9_-]{11}' | head -1)
OUTPUT_DIR="/tmp/yt-$VIDEO_ID"
mkdir -p "$OUTPUT_DIR"
echo "Video ID: $VIDEO_ID"
echo "Output: $OUTPUT_DIR"
```

## Step 2 — Extract transcript (subtitles)

Run this. If it fails with "Sign in to confirm", jump to **Step 2b (Playwright fallback)**.

```bash
# Try auto-generated + manual subtitles (FR priority, then EN)
yt-dlp \
  --write-auto-subs --write-subs \
  --sub-langs "fr,fr-FR,en,en-US" \
  --sub-format "vtt/srt/best" \
  --skip-download \
  --output "$OUTPUT_DIR/%(title)s.%(ext)s" \
  "$VIDEO_URL" 2>&1

# List what was downloaded
ls "$OUTPUT_DIR"/*.vtt "$OUTPUT_DIR"/*.srt 2>/dev/null
```

### Clean the VTT/SRT to readable text:

```bash
# Strip timestamps and tags from VTT
python3 << 'EOF'
import re, glob, os

for f in glob.glob('/tmp/yt-*//*.vtt') + glob.glob('/tmp/yt-*//*.srt'):
    text = open(f).read()
    # Remove VTT/SRT headers and timestamp lines
    text = re.sub(r'WEBVTT.*?\n\n', '', text, flags=re.DOTALL)
    text = re.sub(r'\d+:\d+:\d+[.,]\d+ --> \d+:\d+:\d+[.,]\d+.*\n', '', text)
    text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'<[^>]+>', '', text)  # HTML tags
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Deduplicate adjacent identical lines
    lines = text.split('\n')
    clean = []
    for l in lines:
        if not clean or l.strip() != clean[-1].strip():
            clean.append(l)
    out = f.replace('.vtt', '.txt').replace('.srt', '.txt')
    open(out, 'w').write('\n'.join(clean))
    print(f'Saved: {out}')
    print('\n'.join(clean[:20]))
EOF
```

## Step 2b — Playwright fallback (when yt-dlp blocked)

Use when running on a cloud server (YouTube blocks requests). Extracts title, description, and visible captions.

```javascript
// Write to /tmp/yt-extract-YT.js and run via playwright-skill
const { chromium } = require('playwright');
const fs = require('fs');
const VIDEO_ID = 'REPLACE_ID';
const OUTPUT_DIR = `/tmp/yt-${VIDEO_ID}`;
if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });

(async () => {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ locale: 'fr-FR' });
  const page = await ctx.newPage();

  // 1. Handle consent popup
  await page.goto(`https://www.youtube.com/watch?v=${VIDEO_ID}`, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(3000);
  const consentBtn = page.locator('button:has-text("Tout accepter"), button:has-text("Accept all")').first();
  if (await consentBtn.isVisible({ timeout: 2000 }).catch(() => false)) {
    await consentBtn.click();
    await page.waitForTimeout(2000);
    await page.goto(`https://www.youtube.com/watch?v=${VIDEO_ID}`, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(3000);
  }

  // 2. Get title
  const title = await page.$eval('meta[property="og:title"]', el => el.content).catch(() => page.title());
  console.log('=== TITRE ===\n' + title);

  // 3. Expand description
  const expandBtn = page.locator('tp-yt-paper-button#expand').first();
  if (await expandBtn.isVisible({ timeout: 2000 }).catch(() => false)) {
    await expandBtn.click({ force: true });
    await page.waitForTimeout(500);
  }
  const desc = await page.$eval('#description-inline-expander, #description', el => el.innerText).catch(() => '');
  console.log('\n=== DESCRIPTION ===\n' + desc);

  // 4. Try to get captions URL from player response
  const playerJson = await page.evaluate(() => {
    for (const s of document.querySelectorAll('script')) {
      const m = s.textContent.match(/ytInitialPlayerResponse\s*=\s*(\{.+?\});(?:var|\/\/)/s);
      if (m) return m[1];
    }
    return null;
  });

  if (playerJson) {
    const captionMatch = playerJson.match(/"baseUrl":"(https:\/\/www\.youtube\.com\/api\/timedtext[^"]+)"/);
    if (captionMatch) {
      const captionUrl = captionMatch[1].replace(/\\u0026/g, '&');
      const resp = await page.request.get(captionUrl);
      if (resp.ok()) {
        const xml = await resp.text();
        const lines = xml.match(/<text[^>]*>([^<]+)<\/text>/g) || [];
        const transcript = lines.map(l => l.replace(/<[^>]+>/g, '').replace(/&amp;/g,'&').replace(/&#39;/g,"'")).join(' ');
        console.log('\n=== TRANSCRIPT ===\n' + transcript);
        fs.writeFileSync(`${OUTPUT_DIR}/transcript.txt`, transcript);
      }
    }
  }

  // 5. Screenshot
  await page.screenshot({ path: `${OUTPUT_DIR}/page.png` });
  console.log(`\nScreenshot: ${OUTPUT_DIR}/page.png`);
  await browser.close();
})().catch(e => console.error('Error:', e.message));
```

Execute via playwright-skill:
```bash
node /work/.agents/skills/playwright-skill/run.js /tmp/yt-extract-VIDEOID.js
```

## Step 3 — Download video + extract key frames

```bash
# Download best video ≤720p (fast)
yt-dlp \
  -f "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]" \
  --merge-output-format mp4 \
  --output "$OUTPUT_DIR/video.mp4" \
  "$VIDEO_URL"

# Extract 1 frame every 3 seconds
ffmpeg -i "$OUTPUT_DIR/video.mp4" -vf "fps=1/3,scale=1280:-1" \
  "$OUTPUT_DIR/frame_%03d.jpg" -y

# OR: extract frames at specific timestamps (for short videos / Shorts)
# For a ~60s Short, extract every 5s:
for t in 0 5 10 15 20 25 30 35 40 45 50 55; do
  ffmpeg -ss $t -i "$OUTPUT_DIR/video.mp4" -frames:v 1 -q:v 2 \
    "$OUTPUT_DIR/frame_${t}s.jpg" -y 2>/dev/null
done

echo "Frames:" && ls "$OUTPUT_DIR"/*.jpg | wc -l
```

## Step 4 — Generate structured output

Write a markdown report to `$OUTPUT_DIR/report.md`:

```markdown
# YouTube Video: [TITLE]
**URL:** [URL]  
**Video ID:** [ID]

## Script / Transcript
[Paste cleaned transcript here - one paragraph per logical segment]

## Key Captures
| Frame | Timestamp | Description |
|-------|-----------|-------------|
| frame_001.jpg | 0s | [describe what's visible] |
| frame_005.jpg | 15s | [describe what's visible] |

## Key Points
- [Point 1 extracted from script]
- [Point 2]
```

## Quick reference

| Situation | Command |
|-----------|---------|
| Local machine, works normally | `yt-dlp --write-auto-subs --skip-download URL` |
| Cloud server blocked | Use Playwright Step 2b |
| Need only description | `yt-dlp --dump-json URL \| python3 -c "import sys,json; d=json.load(sys.stdin); print(d['description'])"` |
| Extract 1 frame/5s | `ffmpeg -i video.mp4 -vf fps=1/5 frame_%03d.jpg` |
| Convert VTT to text | `python3 -c "import re; print(re.sub(r'\d+:\d+.*\n|<[^>]+>|WEBVTT.*\n','',open('f.vtt').read()))"` |

## Common issues

| Error | Fix |
|-------|-----|
| `Sign in to confirm you're not a bot` | Cloud IP blocked. Use Step 2b (Playwright) or add `--cookies ~/cookies.txt` |
| `No captions found` | Video has no subtitles. Use Playwright to get description only |
| `ffmpeg: No such file` | `apt-get install ffmpeg` or `brew install ffmpeg` |
| VTT has duplicate lines | Run the dedup python3 cleaner in Step 2 |
