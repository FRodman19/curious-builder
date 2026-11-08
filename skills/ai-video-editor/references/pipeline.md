# Full Pipeline Reference: 9 Stages

The detailed working document for every stage. `SKILL.md` summarizes each stage; come here for exact
commands, hard rules, and decision trees.

Notation: `{PROJECT_ROOT}` is wherever you keep video projects; `{stem}` is the source filename without
extension. `--display / --body / --accent / --ink / --canvas` are your brand tokens (see
`design/DESIGN-GUIDELINE.md`).

---

## Stage 1: INGEST

**Goal:** Understand the raw file and set up the project folder.

```bash
ffprobe -v quiet -print_format json -show_streams -show_format {input_file}
```

Record: duration, resolution, frame rate, audio codec + sample rate, file size.

Detect the video type from context or filename:
- "short", "reel", "tiktok" -> `short-form`
- "screen recording", "screencast", "demo on screen" -> `howto-screencast` (facecam PiP over a screen
  recording, two sources)
- "tutorial", "how to", "step by step" -> `tutorial`
- everything else -> `youtube-long` (default)

Create the project folder:
```
{PROJECT_ROOT}/{project-name}/
├── raw/          <- one source (facecam) normally; howto-screencast has facecam.mp4 + screen.mp4
├── transcripts/
├── edl/
├── clips/
├── beats/
├── renders/
├── screenshots/
├── exports/      <- editor handoff (Stage 7.5)
```

Write `project.md` (date, video type, source filename, ffprobe summary, session goals).

---

## Stage 2: TRANSCRIBE

**Goal:** Word-level timestamp JSON. Cache it, never re-run.

Use any transcription source that returns **per-word start/end times** (e.g. an ElevenLabs Scribe-style
API). Cache the result to `transcripts/{stem}.json`, then optionally pack it into a human-readable
`takes_packed.md` for review.

Hard rules:
- Never re-transcribe if `{stem}.json` exists.
- Never transcribe audio that was already clipped/edited: always transcribe from `raw/`.

`takes_packed.md` format:
```
[TAKE 1-0:00:00 -> 0:12:34]
word word word [hesitation] word word
...
```

> ⚙️ Companion tool: the full system uses a turnkey transcribe helper that wraps the API + caching +
> packing. It's not in this bundle, the mechanism above (word-level JSON, cached) is all the pipeline
> needs. If you'd like my ready-made helper, just ask.

---

## Stage 3: TRIM

**Goal:** Generate an edit decision list (EDL) that removes filler, mistakes, and dead air. Get approval
before rendering.

### 3a: Propose trim strategy
From the transcript, identify: filler ("um", "uh", "like", "you know", pauses >0.8s), retakes (keep the
cleaner one), off-topic tangents, dead air at start/end. Present as a numbered list with time saved and an
estimated final duration. **Confirm before proceeding.**

### 3b: Generate EDL
```json
{
  "input": "raw/{filename}",
  "clips": [
    { "start": 0.000, "end": 14.820 },
    { "start": 15.210, "end": 22.440 }
  ],
  "audio_fade_ms": 30
}
```
Hard rules:
- Every cut point lands on a **word boundary** from the transcript JSON.
- 30ms audio fade on every cut (prevents pops).
- Never cut mid-phoneme, check the preceding word's `end` and the next word's `start`.

### 3c: Render clips
Cut and concatenate with ffmpeg to `clips/final.mp4` (the trimmed video, no overlays). Use hardware
encoding where available (e.g. Apple VideoToolbox `h264_videotoolbox`) for speed; match output fps to the
source (don't hard-pin fps or you'll judder non-24 footage). Use a draft/proxy pass while iterating on cut
points, a full pass once approved.

> ⚙️ Companion tool: the full system has a `render.py` that does EDL -> cut with auto hardware detection,
> loudnorm, and draft/preview modes. It's not in this bundle, ffmpeg does all of this. Ask me if you want
> the ready-made helper.

---

## Stage 3.7: TRANSITIONS (optional)

**Goal:** a small, deliberate set of transitions at **section breaks only**, never every cut, on the
locked picture cut, **before** audio-enhance and motion graphics.

**Why here:** transitions re-render from the EDL + raw sources, so running them after audio-enhance would
discard the enhanced audio.

**Flow:** read the section boundaries + transcript -> propose one transition per major boundary, matched to
the moment (fade/dissolve for soft shifts, wipe/smooth for energetic pivots, zoom/push-in for reveals) ->
**get approval** -> apply (ffmpeg `xfade` or your transition engine) -> `clips/final_fx.mp4`. Frame-check
each transition midpoint before showing the user. Section breaks only.

---

## Stage 4: BEAT PLAN

**Goal:** decide which moments get motion-graphic overlays, what they show, and when they start.

Read the transcript JSON to identify **anchor words** (rules in `references/beat-planning.md`). Propose a
beat-plan table:
```
Beat 1: "The hook"
  Anchor word: "broke" at 0:08.3
  Overlay starts: 0:07.7 (0.6s before anchor)
  Overlay ends:   0:12.0
  Composition: title card + karaoke
Beat 2: "The fix"
  Anchor word: "fixed" at 4:22.1
  ...
```
**Confirm the beat plan before building.** Allow adjustments (add/remove beats, change anchor words, adjust
timing, change content).

---

## Stage 5: BUILD

**Goal:** one HTML composition per beat. Build beats **in parallel**.

For each beat, spawn a separate sub-agent:
```
Task: Build beat {N} for project {name}
Beat spec: {beat plan entry}
Output file: beats/beat-{N:02d}.html
Design rules: design/DESIGN-GUIDELINE.md
Renderer contract: window.__timelines must be defined synchronously
```
Each sub-agent must:
1. Read `design/DESIGN-GUIDELINE.md` (tokens, component patterns).
2. Read its beat spec.
3. Produce a self-contained HTML file with embedded GSAP.
4. Export `window.__timelines` synchronously.
5. Fit dynamic text to its container (no overflow).
6. Use `gsap.from()` for entrances (not `gsap.to()` on init).

Renderer hard rules:
- No `repeat: -1` on any timeline.
- No `async/await` inside `window.__timelines` initialization.
- Timelines are synchronous and defined by the time the DOM is ready.
- `window.__timelines` is an object: `{ main: gsapTimeline... }`.

-> Full composition contract: `references/beat-planning.md`.

---

## Stage 6: ASSEMBLE

**Goal:** wire beats into `index.html`, validate, screenshot, frame-check.

### 6a: Wire index.html
```html
<composition src="beat-01.html" data-start="7.7" data-duration="4.3"></composition>
```
Set correct `data-start` / `data-duration` on each.

### 6b: Validate
Lint the compositions and capture screenshots (with HyperFrames: `npx hyperframes lint` /
`npx hyperframes inspect --output screenshots/`). Look for text overflow, missing fonts, color mismatches
vs. the design guideline.

### 6c: Visual identity gate
Cross-check each screenshot against the checklist in `design/DESIGN-GUIDELINE.md`.

### 6d: Frame-check pass (mandatory before render approval)
Extract JPGs at key beat moments + state-change points and **read each one yourself**:
```bash
for t in <timestamps spanning the video>; do
  ffmpeg -loglevel error -ss "$t" -i renders/preview.mp4 -frames:v 1 -q:v 3 -y "screenshots/check-t${t}.jpg"
done
```
Check for: typos, text overflow / cropped icons / missing elements, wrong colors or font fallbacks
(a display serif silently falling back to a system serif is a common one), anything on the face or below
safe zones, and sync (does the active animation match what's being said at that timestamp?). Fix and
re-render before sharing. This is the cheapest place to catch issues.

---

## Stage 7: RENDER

**Goal:** preview for approval, then final.

The renderer screenshots a headless-Chrome timeline frame-by-frame, then encodes. Speed levers: parallel
workers, hardware encode, and draft quality for previews.

### Preview (fast)
```bash
npx hyperframes render beats/index.html --quality draft --gpu --workers auto -f 25 --output renders/preview.mp4
```
Present to the user. **Must approve before final.**

### Final (quality)
```bash
npx hyperframes render beats/index.html --quality high --workers auto --video-frame-format png -f 25 --crf 18 --output renders/final.mp4
```
- Match the frame rate to the footage (`-f`).
- `--video-frame-format png` extracts the embedded source video **losslessly** (default JPEG softens
  faces / UI). Put it on finals and always on screencasts.
- Resolution: **match the footage, floor 1080p, up to 4K.** Never render a final below 1080p; don't
  fake-upscale 1080p to 4K. For 4K source add the 4K resolution preset and keep GPU + workers on.
- `--gpu` (hardware encode) is bitrate-driven and **mutually exclusive with `--crf`**, pick `--crf 18`
  for max quality or `--gpu --video-bitrate 12M` for speed.

-> Full rationale: `references/rendering.md`.

---

## Stage 7.5: EDITOR HANDOFF (optional)

**Goal:** emit an editable *timeline* so the cut opens in DaVinci Resolve (primary) or CapCut (secondary).
Bonus export, the Stage 7 MP4 is unchanged.

Turn `edl/edl.json` into:
- `exports/resolve/{project}.otio`: **DaVinci imports OTIO natively** (Media Pool -> Timelines -> Import
  -> OTIO). Every cut is a live, trimmable clip referencing the original footage. Even free Resolve opens
  it.
- `exports/capcut/{project}.fcpxml`: **best-effort** for CapCut (limited importer; duplicate the project
  first).

**Why OTIO for Resolve, FCPXML for CapCut:** Resolve reads OTIO natively; OTIO->FCPXML breaks in Resolve,
so never feed it FCPXML. FCPXML is only for CapCut, which can't read OTIO.

**Motion graphics as separate, adjustable clips (one clip per graphic):** render each beat as its own
**transparent ProRes 4444 .mov**: at its own native duration, so every graphic lands on its own track,
movable / resizable / retimable in the editor (text edits still go back to the renderer). Build a
throwaway one-beat mini-project whose root duration equals the beat's `data-duration`, render it as a
transparent MOV (full-cover beats render opaque; card/lower-third beats render with alpha), then write an
`overlays.json` your timeline exporter turns into V2/V3 overlay tracks over the V1 cut.

> ⚙️ Companion tools: the full system ships `export_timeline.py` (EDL -> OTIO/FCPXML) and
> `render_overlays.py` (per-beat transparent MOVs). Neither is in this bundle. The mechanism is standard,
> OpenTimelineIO writes OTIO/FCPXML; the renderer produces the transparent MOVs. Ask me if you want my
> ready-made scripts.
>
> ⚠️ Renderer version: newer builds of the HTML renderer have regressed transparent-overlay rendering.
> Pin a known-good version for the overlay step rather than always taking the latest.

---

## Stage 8: TRAIN (optional)

**Goal:** capture what worked so the next video starts with better defaults. After the user approves the
final render: copy `beats/*.html` into a `successes/{YYYY-MM-DD}/` folder, save the beat plan + prompts,
and note the new success pattern for that video type.

> ⚙️ Companion tool: the full system also runs an automatic self-critique step that scores each finished
> render against a benchmark and mines reusable style lessons for future videos. That part isn't in this
> bundle, ask me if you want it.

---

## Stage 9: THUMBNAIL (optional)

**Goal:** a static thumbnail rendered AFTER the video is approved.

### 9a: Extract a pre-overlay base frame
Pick a frame from the version BEFORE motion graphics were rendered in. Choose a moment of expression
(hands raised, mouth open, full gesture).
```bash
ffmpeg -i renders/final-preoverlay.mp4 -ss 44.0 -vframes 1 thumbnail/thumb_clean.jpg
```

### 9b: Build the thumbnail composition
Create `thumbnail/index.html`. A reliable layout: base image (saturate ~0.55, brightness ~0.68) + dark
overlay -> short pill badge (1-2 words) -> big headline with one accent word in your display font ->
accent divider -> subline -> a row of small step cards (icon + number, no text labels) -> accent CTA.

### 9c: Render and iterate
Render, show the user, iterate (v2, v3...) until approved.

Hard rules:
- Describe the aspect ratio precisely (e.g. **9:16** or **16:9**), not "vertical"/"portrait".
- Base frame must come from a **pre-overlay** video (no double-layered motion graphics).
- Never blur the base image: use saturate + brightness + a dark overlay instead.

---

## Cross-Stage Hard Rules

1. **Never re-transcribe**: if `transcripts/{stem}.json` exists, use it.
2. **Always cut on word boundaries**: from the transcript JSON `end`/`start`.
3. **30ms audio fade on every cut**: prevents pops.
4. **Subtitles last in the DOM**: karaoke/subtitle elements are the last child (the renderer draws in DOM
   order).
5. **Confirm before rendering**: Stage 3 trim and Stage 4 beat plan both require confirmation.
6. **Parallel Stage 5 builds**: all beat sub-agents at once, not serially.
7. **No `repeat: -1`**: infinite GSAP loops break the capture engine.
8. **Entrance only**: `gsap.from()` on enter, `gsap.to()` exits only on the final scene.
9. **Synchronous timelines**: `window.__timelines` defined synchronously in `<script>`.
10. **Raw folder is sacred**: never modify, move, or re-encode files in `raw/`.
