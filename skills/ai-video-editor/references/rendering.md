# Rendering: speed, quality, resolution

Two renders happen in this pipeline. Both encode video, and both are slow for the same reason if you let
them: CPU encoding. This is how to make them fast without losing quality.

| Render | Tool | What it does |
|--------|------|--------------|
| **Cut** | ffmpeg | Trims + concats the picture cut, composites subtitles, loudnorm |
| **Motion graphics** | HTML renderer (headless Chrome + ffmpeg) | Screenshots each frame of the HTML/GSAP composition, encodes to video |

---

## Resolution policy (the crisp-output rule)

**Match the footage, never below 1080p, up to 4K.** Crisp masters, but honest ones: no fake-4K upscaling
of 1080p footage, and never a sub-1080p final.

| Stage | Resolution |
|-------|-----------|
| Draft (cut-point checks) | 720p |
| Preview (QC, motion preview) | 1080p |
| Final, cut | source resolution, floored at 1080p, capped at 4K |
| Final, motion | match the footage (4K source -> 4K preset; 1080p source -> native 1080p) |
| Editor handoff (`.otio`) | references the **original** footage -> full source res |

Iterate on proxies; render the high-res master once, at the end. 4K is ~4x the pixels of 1080p, so the
hardware encode + parallel workers are what keep a crisp 4K master fast.

---

## Fix 1: hardware encoding (the cut render)

Prefer a hardware encoder over `libx264` (on Apple Silicon: `h264_videotoolbox`), typically several times
faster at visually equivalent quality. Notes:
- Hardware encoders are bitrate-driven (no CRF): scale bitrate to resolution (e.g. ~12M at 1080p, ~48M at
  4K).
- Match output fps to the source; don't hard-pin fps or non-24 footage will judder.
- Use a draft pass while iterating cut points; the full pass only once.
- Force software (`libx264` + CRF) only if you need CRF-exact output or hit a hardware quirk.

> If your ffmpeg is built without `libass`, the `subtitles` filter won't exist and burned-in SRTs are
> skipped, that's fine, since captions live in the renderer's karaoke layer. Install an ffmpeg with
> `--enable-libass` only if you actually need burned captions.

---

## Fix 2: the motion-render flags

The HTML renderer seeks a headless-Chrome timeline and screenshots **every frame**, then pipes to ffmpeg.
Levers (HyperFrames flag names shown; adapt to your renderer):
- `--gpu` -> hardware encode. Great for previews. On finals it's bitrate-driven and **mutually exclusive
  with `--crf`**, so a max-quality final is either `--crf 18` (CPU) or `--gpu --video-bitrate 12M`
  (hardware, faster, slightly softer).
- `--workers auto` -> multiple Chrome instances capture frames in parallel (~4 is often the sweet spot;
  each worker uses meaningful RAM). Benchmark once and record the best number.
- `--quality draft` for previews, `--quality high` for finals.
- `-f 25` -> match the footage; higher fps scales render time linearly.
- Speed for previews comes from **draft quality**, not a lower resolution, most renderers only
  supersample *up* to presets, they can't downscale for speed.

---

## Quality: the source-frame extraction fix

If your motion render sometimes looks softer than you expect, it's usually not the engine. It's how the
renderer decodes the **embedded source video** (facecam or screen recording) while capturing frames:

- Default `auto` = **JPEG** -> the source footage is re-compressed lossily during capture, softening faces
  and mushing crisp UI / type edges.
- `--video-frame-format png` extracts those source frames **losslessly**. (Alpha sources already extract
  as PNG.)

Put `--video-frame-format png` on **finals** (and always on screencasts). Combined with a good final
encode (`--crf 18` on CPU, or `--video-bitrate 12M` on GPU) it closes the gap, without switching engines.
Keep JPEG for drafts: faster, smaller, fine for review.

> This flag governs *source-video* extraction, not the HTML composition's own frames (those are Chrome
> screenshots). Since these videos are facecam + graphics, the source-video path is exactly what softens,
> so this is the lever that matters.

---

## One clip per graphic (editor handoff)

To hand each motion graphic to the editor as its own resizable clip, render each beat **natively at its own
duration** into a transparent ProRes 4444 MOV: build a throwaway one-beat mini-project whose root duration
equals the beat's `data-duration`, render it as a transparent MOV, and write an `overlays.json` your
timeline exporter turns into V2/V3 overlay tracks over the V1 cut. Output is exactly the beat's length, no
trim, no timing drift. Each beat is a separate headless-Chrome render, so a handoff export takes a few
minutes; it's a one-time step.

> ⚠️ Pin a known-good renderer version for the overlay step. Some newer builds of the HTML renderer have
> regressed transparent-overlay rendering, pin rather than always taking the latest.

---

## Speed checklist (per render)

- Cut render: hardware encode; use a draft pass while iterating cut points.
- Motion preview: `--quality draft --gpu --workers auto`.
- Motion final: `--quality high --gpu --workers auto --video-frame-format png -f 25`.
- Confirm the worker count once with a benchmark.
- Don't render final resolution while iterating, draft/preview first, final only after approval.
