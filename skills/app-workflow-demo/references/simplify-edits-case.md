# Simplify Edits case study

Inspected 2026-10-06. This is historical evidence and implementation guidance, not a blanket claim that every displayed control is present in today’s app.

Source: the Simplify Edits project (private).

## What was actually built

`hero-video-options-20261005/editor-in-motion/` contains an HTML/SVG reconstruction, not a new live screen recording. Its brief records the real 194-word transcript, a 33-proposal journal batch, original duration 70.262992 seconds, working duration about 39.15 seconds and a restored 11.02-second source passage. `model-inline.js`, `timeline-fit.js` and `word-lane.js` keep picture, transcript, words, waveform and ruler coherent. The window, fonts, mark and presenter reuse app/reference assets.

`hero-video-options-20261005/agent-workspace/` contains six independently looping feature cards. Each is a designed compact explanation, not six literal panels in the shipped app. It uses real edit data where relevant and retains local cursor/state logic. The 40-second master contains two 20-second cycles with phase offsets.

`hero-video-options-20261005/guided-walkthrough/` extends the app-window reconstruction. Read `ACTION-PROVENANCE.md` before reusing it. It distinguishes recorded take 7 and archived app 0.4.2 behavior from the later user-selected F2/D46 transcription chapter. `tighten-pacing.py` is its final documented builder, not the superseded base generator.

## Corrections that changed the method

- The first transcription shortcut was invented and rejected. Controls were traced to code/recording, then the user explicitly chose the design chapter as visual authority for transcription. Treat the chapter as a chosen design reference, not independent proof of shipped behavior
- The guided flow removed an unverified second Undo. An earlier editor film contains that action; approval of a film does not establish product capability
- Cuts initially left misleading empty timeline space. The revision closes gaps then refits the viewport; it never stretches retained footage or adds filler spans
- Word chips between video and audio derive from timestamp data and follow cuts, restore and Undo
- The before/after wipe is an explanatory presentation, not a real comparison button
- Shortened waits and immediate typing improved pacing; sample media timing stayed distinct from presentation time
- The abstract framing slide explained ratios, but the user wanted the app framing card in the animated version. Both were retained with clear roles

## How this became a carousel

`carousel-study-20261005/revision-20/` holds approved designed PNG slides and contact sheets. `common.py` measures glyph advances, tracking and line breaks. App UI uses Instrument Sans; the carousel surrounds it with approved Inter typography. These are different layers, not permission to change an app’s font.

`carousel-study-20261005/carousel-release-20261006/scripts/prepare_carousel_release.py` reuses approved headline/background designs without their demonstration panels. `crop_carousel_media.py` extracts individual 20-second feature cycles from the approved montage. `build_carousel_projects.py` embeds the editor or card footage in those layouts and authors separate simplified HTML/GSAP illustrations. Twenty independent compositions support the variants; there was no need to redesign the app for each slide.

Limits of the earlier implementation: some cropped panels were slightly resized to fixed slots and some verification used only a few frame samples. Improve future production with aspect-preserving composition, explicit action-boundary samples, actual playback inspection and visible evidence status. Do not copy a stale asset solely because it was previously approved.

## Visual and delivery decisions

The approved 1080×1350 carousel used 64px side gutters, Inter 400/500/600, heading tracking −1px and compact line steps around font size +2px. Warm white, ink and violet came from the project. Gentle white/purple/orange aurora hook alternatives were art direction choices; orange meant the actual selected light orange, not an arbitrary cream substitute. Body slides were quieter. The CTA was centered and used the site’s familiar dark rounded button.

These values are a concrete example, not a universal theme for unrelated products. Re-extract the next app’s tokens.

The first publishing pack was too complicated. Final accepted delivery used complete numbered carousel folders with their hooks included, separate hook folders and one `Captions.md`. Static slides stayed PNG. MP4 replaced GIF for social delivery. Do not reintroduce nested archive sets, per-platform text-file trees or an unsolicited publishing dashboard.
