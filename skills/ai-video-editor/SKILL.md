---
name: ai-video-editor
description: An AI video production pipeline that turns a raw talking-head recording into a polished,
  motion-graphics video. Use whenever you want to edit a video, trim filler words or mistakes, cut a
  recording down from a transcript, add motion graphics / overlays / captions / beats, produce a YouTube
  video, or make a short-form clip. Trigger phrases include "let's edit this", "trim this video",
  "add motion graphics", "I filmed something", "raw video ready", "make this look good", "produce this
  clip", "edit my recording", "add captions", "add beats", "I have raw footage".
  Handles the full pipeline: word-accurate transcription -> smart filler trimming -> beat planning ->
  HTML + GSAP motion graphics -> parallel beat building -> verified render. Optionally exports the
  finished cut as an editable DaVinci Resolve / CapCut timeline for manual tweaks.
---

# ai-video-editor

An end-to-end video production pipeline. Raw recording in -> polished, motion-graphics video out.
Built on three ideas: **cut from the transcript**, **plan before you build**, and **animation is the
explanation**.

> **One line:** it plans the edit first, then asks for (or generates) a word-level transcript, cuts the
> video down from that transcript, builds motion graphics timed to the words, and renders the finished
> video, with an optional editable-timeline export.

---

## What you need

- **ffmpeg**: cutting, concatenating, frame extraction, encode.
- **A word-level transcription source**: any service that returns per-word start/end timestamps
  (e.g. an ElevenLabs Scribe-style API). The pipeline is built around word-accurate timing.
- **An HTML/GSAP -> video renderer**: this build uses **HyperFrames** (`npx hyperframes`), which
  screenshots a headless-Chrome timeline frame-by-frame and encodes to video. Any renderer that runs an
  HTML composition with a GSAP timeline works; the composition contract is described in
  `references/beat-planning.md`.
- **(Optional) A design guideline**: `design/DESIGN-GUIDELINE.md` is a neutral starter. For best
  results, drop in your own brand tokens (colors + fonts); the graphics inherit them. See "Bring your
  own brand" below.

> ⚙️ **Companion tools, not included in this share.** The full production system this skill came from
> uses several private companion tools: a turnkey transcription + cut helper, an illustration/B-roll
> library with automatic recoloring, and a self-learning step that critiques each finished render to
> improve the next one. **Those are not part of this package.** Where a stage relies on one it's flagged,
> so you know what's doing the heavy lifting, message me if you want it. The pipeline below is fully
> workable with the public tools listed above; the companion tools just make it turnkey.

---

## Bring your own brand

This skill ships **without a brand identity on purpose**, so it looks like *your* channel, not someone
else's. `design/DESIGN-GUIDELINE.md` defines craft rules (placement, motion, captions, contrast) using
**tokens**: not fixed colors or fonts:

```
--canvas   your background
--ink      your primary text
--accent   your single highlight color
--display  your title font
--body     your body / caption font
```

Fill those in once with your brand and every beat inherits them. The craft principles (above-the-head
placement, one accent per composition, animation-is-the-explanation, the caption style, the frame-check
gate) are brand-agnostic and worth keeping as-is.

---

## Plan Mode Checkpoints (mandatory two-step)

This pipeline plans at **two moments** in every video. Don't skip either, they are where quality is won.

### Checkpoint 1: Session start (before any execution)
When the user says "let's edit this" / "I filmed something" / hands over raw footage:
1. **Enter plan mode immediately.** Don't run ffprobe, don't transcribe, don't touch files yet.
2. Ask clarifying questions: video type (short / tutorial / long), aspect ratio, project name, hook
   angle, anything ambiguous in the recording.
3. Produce a plan: how the cut will go, the trim strategy at a high level, the visual direction, and the
   approximate beat count.
4. **Get approval on the plan.** Only then begin Stages 1-3.

### Checkpoint 2: After the rough cut is approved, before motion graphics
After ingest -> transcribe -> paper-edit -> trim land and the user has signed off on the cut:
1. **Re-enter plan mode** before any beat HTML is written.
2. Walk through the beat plan: anchor words, timestamps, composition type per beat, and what the moving
   mechanic *is* for each beat.
3. **Get approval on the beat plan.** Only then start Stage 5 (parallel beat builds).

### When to just act (skip plan mode)
- Inside a stage the user already approved (running the render, generating screenshots, frame-checks).
- Mechanical follow-ups: "extract a thumbnail frame", "re-render with bt709 color".
- Single named fixes ("fix the typo on beat-02").

### Why this matters
- The rough cut is a **destructive boundary**, after audio enhancement, re-cuts get expensive. Lock the
  cut before that wall.
- Motion graphics are N beats x creative judgment each. Course-correcting mid-build wastes a parallel
  sub-agent run. Lock the beats before Stage 5.

---

## Model selection by stage (if your runner supports it)

Default to a mid-tier model for ~80% of the pipeline. Escalate to your strongest model only at the two
**judgment** stages, the surgical cut/paper-edit and the beat plan. Drop to a fast/cheap model for
mechanical stages (ingest, transcribe, render, file copies). Reading extracted frames burns tokens fast,
stay off your largest-context model during frame-read passes.

---

## Session Start

At the start of every session:

1. **Check for an existing project**: if `project.md` exists in the project folder, read it for context.
2. **Detect the video type** from filename, content, or an explicit statement:
   - `short-form`: "tiktok", "reel", "short", "60 seconds", "vertical".
   - `howto-screencast`: "screen recording", "screencast", "demo on screen" (two sources: facecam +
     screen, composited as a framed PiP over the screen recording).
   - `tutorial`: "how to", "step by step", "walkthrough" (talking-head teaching, no screen capture).
   - `youtube-long`: everything else (default).
3. **Load your design guideline** (`design/DESIGN-GUIDELINE.md`) and, if you keep a folder of approved
   past beats, scan it for reusable HTML.

---

## The 8-Stage Pipeline

### Stage 1: INGEST
Run `ffprobe` on the source to get duration, resolution, frame rate. Create the project folder with all
subdirectories (`raw/`, `transcripts/`, `edl/`, `clips/`, `beats/`, `renders/`, `screenshots/`,
`exports/`). Write `project.md` with the session info.
-> `references/pipeline.md` Stage 1.

### Stage 2: TRANSCRIBE
Get a word-level transcript from your transcription source and **cache it** to `transcripts/{stem}.json`.
Never re-run if the file exists. Always transcribe from the **raw** file, never from an already-cut clip.
-> `references/pipeline.md` Stage 2.

### Stage 2.5: PAPER EDIT
Before cutting, build the target. Detect **scripted vs unscripted** (a `script.md` = scripted). Scripted
-> diff transcript vs script, keeping off-script-but-better lines. Unscripted -> derive the video's real
point/arc from the transcript first. Then write the ideal final version as a marked target transcript
(best mix across takes), frame-verify the candidate takes (energy -> fluency -> relevance -> continuity),
and pick a cut strategy. **Get confirmation** before cutting. Never cut for cutting's sake.
-> `references/paper-edit.md`.

### Stage 3: TRIM
Cut the footage **down** to the approved paper edit. Confirm fillers / retakes / dead air, apply the cut
style for the format (short = tight/jump-cut, long = breathing room, tutorial = clear step boundaries).
Generate `edl/edl.json` (all cuts on word boundaries, 30ms audio fades) and render `clips/final.mp4`.
-> `references/pipeline.md` Stage 3.

### Stage 3.7: TRANSITIONS (optional)
After the picture cut is locked, and **before** audio-enhance + motion graphics, add a *small, deliberate*
set of transitions at section breaks only, never every cut. Propose one per major boundary matched to the
moment (fade/dissolve for soft shifts, wipe/zoom for energetic pivots), get approval, then apply.
-> `references/pipeline.md` Stage 3.7.

### Stage 4: BEAT PLAN
Read the transcript JSON to identify **anchor words** (payoff words, topic-shift words, emphasis moments).
Propose a beat-plan table: anchor word + timestamp + composition type. **Get confirmation.** Allow
adjustments before building.
-> `references/beat-planning.md`.

### Stage 5: BUILD
Spawn **one sub-agent per beat, in parallel**, all beats build simultaneously. Each sub-agent reads the
design guideline, the beat spec, and the renderer contract, and produces `beats/beat-NN.html`. Each file
uses `gsap.from()` for entrances, defines `window.__timelines` synchronously, and puts the
karaoke/subtitle element **last** in the DOM.
-> `references/pipeline.md` Stage 5 + `references/beat-planning.md`.

### Stage 6: ASSEMBLE
Wire all beats into `beats/index.html` with correct `data-start` / `data-duration`. Lint and screenshot
the compositions. Review each screenshot against the Visual Identity Gate in `design/DESIGN-GUIDELINE.md`.
Then run the **frame-check pass**, extract JPGs at key timestamps, read each one, fix typos / overflow /
missing elements / wrong fonts before render approval.
-> `references/pipeline.md` Stage 6.

### Stage 7: RENDER
Preview render (fast: draft quality + GPU + parallel workers) -> show the user -> **get approval** -> final
render (high quality, lossless source-frame extraction, matched frame rate, floor 1080p up to 4K). Iterate
on proxies; render the high-res master once, at the end.
-> `references/pipeline.md` Stage 7 + `references/rendering.md`.

### Stage 7.5: EDITOR HANDOFF (optional)
Bonus export, the rendered MP4 is unchanged. Turn `edl/edl.json` into an editable timeline: an `.otio`
(DaVinci Resolve imports it natively, even the free version) and a best-effort `.fcpxml` (CapCut). Cuts
land as live clips referencing the original footage; motion graphics come in as movable transparent
overlay clips (text edits stay in the renderer). Run on request or after final render.
-> `references/pipeline.md` Stage 7.5.

> ⚙️ Companion tool: the turnkey `transcript -> cut -> editable-timeline` helper scripts aren't in this
> bundle. The mechanism is standard (word-level JSON + ffmpeg + an OTIO/FCPXML writer such as
> OpenTimelineIO), and if you'd rather have my ready-made scripts for it, just ask.

### Stage 8: TRAIN (optional)
After the user approves the final render, capture what worked: copy the approved beats into a `successes/`
folder, save the beat plan + prompts, and note the pattern so the next video starts with better defaults.
> ⚙️ Companion tool: the full system also runs an automatic self-critique step that scores each finished
> render against a benchmark and mines reusable style lessons. That part isn't in this bundle, message me
> if you want it.

### Stage 9: THUMBNAIL (optional, post-render)
Extract a **pre-overlay** frame (before motion graphics were rendered in), build a thumbnail composition,
render it, and iterate with the user until approved.
-> `references/pipeline.md` Stage 9.

---

## Beat Building Contract (Sub-agents)

When spawning Stage 5 sub-agents, each agent receives:

```
Build beat {N} for project {name}:
- Beat spec: {anchor word, timestamp, composition type}
- Output: beats/beat-{NN}.html
- Must read: design/DESIGN-GUIDELINE.md
- Must follow: window.__timelines synchronous contract
- Karaoke (if present) must be the LAST child in the DOM
- Use gsap.from() for all entrances
- No repeat:-1 on any timeline
- Fit dynamic text to its container (no overflow)
```

---

## Hard Rules (Non-Negotiable)

1. Never re-transcribe, `transcripts/{stem}.json` is cached forever.
2. All cuts land on word boundaries from the transcript JSON.
3. 30ms audio fade on every cut point, no exceptions.
4. Karaoke / subtitle elements are always the last child in the DOM.
5. Confirm with the user before rendering (Stage 3 trim + Stage 4 beat plan).
6. Stage 5 beats build in parallel, never serial.
7. No `repeat: -1` in any GSAP timeline.
8. `gsap.from()` for entrances; `gsap.to()` exits only on the final scene.
9. `window.__timelines` must be defined synchronously in `<script>`.
10. The raw folder is sacred, never modify files in `raw/`.
11. Self-review before presenting, watch any output end-to-end, score it /10 against the success
    criteria, and only present at >=8. Below 8: diagnose, fix, re-watch.
12. Transitions only at section changes, never every cut; run them before audio-enhance.

---

## Reference Files

| File | Contents |
|------|----------|
| `references/pipeline.md` | Full Stage 1-9 with commands, hard rules, decision trees |
| `references/paper-edit.md` | Stage 2.5, scripted/unscripted detection, paper-edit blueprint, take-selection rubric, three cut strategies, format-aware cutting |
| `references/beat-planning.md` | Anchor-word selection, timing formula, the renderer composition contract, beat HTML patterns |
| `references/rendering.md` | Render speed, quality (lossless source extraction), resolution policy, editor-handoff overlays |
| `design/DESIGN-GUIDELINE.md` | Neutral design system (tokens, not a fixed brand) + the Visual Identity Gate |
