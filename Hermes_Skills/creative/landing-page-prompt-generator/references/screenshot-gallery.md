# Rendering screenshots & a thumbnail gallery

Used by Step 4 of the landing-page-prompt-generator skill when the user wants to *see*
built pages, or when generating a gallery of many pages.

## Why this exists
Text-only tiles in a gallery are useless — the user explicitly asked for real page
thumbnails. Render each page to a PNG and tile those images.

## Method (proven end-to-end this session)
Do NOT install a driver. Playwright's Chromium is already on disk:
`~/AppData/Local/ms-playwright/chromium-*/chrome-win64/chrome.exe`
(find it: `ls ~/AppData/Local/ms-playwright/chromium-*/chrome-win64/chrome.exe`).

```bash
CHROME="C:/Users/Kreuz/AppData/Local/ms-playwright/chromium-1228/chrome-win64/chrome.exe"
mkdir -p "C:/Users/Kreuz/landing-pages/thumbs"
"$CHROME" --headless --no-sandbox --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=1200,900 \
  --screenshot="C:/Users/Kreuz/landing-pages/thumbs/<slug>.png" \
  "http://127.0.0.1:8140/<slug>/index.html"
```

## CRITICAL path gotcha
Native Windows binaries (chrome.exe) do NOT get MSYS path translation. Passing
`/c/Users/...` to chrome.exe fails with "cannot find the path specified". You MUST
pass Windows-style paths — `C:/Users/...` — to the executable AND as the
`--screenshot` argument, even though bash itself tolerates either. (This burned the
first attempt; switching to `C:/...` fixed it instantly.)

## After capture
- Validate each file: PNG magic bytes are `\x89PNG` (first 4 bytes). Reject otherwise.
- Gallery `index.html` pattern:
  ```html
  <a class="card" href="<slug>/index.html">
    <div class="shot"><img src="thumbs/<slug>.png" loading="lazy"></div>
    <div class="meta"><span class="n">01 · Tag</span><h2>Name</h2><p>Concept</p></div>
  </a>
  ```
  CSS: `.shot{aspect-ratio:4/3; overflow:hidden}` and
  `.shot img{width:100%;height:100%;object-fit:cover;object-position:top center}`
  (top-center shows the hero). Hover zoom + card lift is a nice touch.
- For a mid-page shot instead of the hero, add `--virtual-time-budget=2000` and scroll
  via CDP, or just capture the hero (usually representative enough).

## Delegation pitfall (batch builds)
When building MANY pages, do NOT hand all of them to one subagent and trust its
self-report. Subagents hit iteration/API-timeout caps (~90s per call) and silently
drop files — one batch of 9 lost 3 pages (only 6 written; the subagent claimed success).
Mitigations, in order of reliability:
1. Build ONE file at a time, validate with `scripts/validate_html.py`, then move on.
2. Or split into small parallel batches (3 each), then **RE-CHECK DISK** (`ls` the
   target dir) rather than trusting the summary — a truncated/dead subagent lies.
3. If a batch truncates, re-dispatch the missing slugs as a tight single-task agent
   with "write ONE file, validate, then continue" instructions.
