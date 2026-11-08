# Production details

## Build from states

Separate semantic state from presentation time. A small state model derives every visible projection; camera and pointer animation run on the presentation timeline. A compressed wait must not rewrite media time or the meaning of an edit.

For scripted rebuilds, use a pure `draw(t)` or a seek-safe GSAP timeline registered according to the current HyperFrames contract. Set every relevant property for each state, including visibility, selected controls, input text, scroll offsets and result labels. Avoid wall clocks, uncontrolled timers, runtime network responses and unseeded randomness. Verify returning to an earlier time does not retain later state.

For actual app components, freeze asynchronous inputs through fixtures rather than importing a live authenticated backend. Keep original app assets separate from presentation chrome. For screenshot-based work, favor an honest pan/highlight or a limited layered reconstruction over invented controls.

Use [pacing and moving review](#pacing-and-moving-review) to allocate presentation time independently of product latency.

Whole-device/window mode keeps the complete frame visible throughout. If a detail view is chosen, transition to a frameless app/component view with source-correct proportions and shared pointer coordinates; do not clip half the physical phone for a closeup. Actions do not require camera zooms. Browser/video player controls should not accidentally appear over a silent product demo.

Independent feature loops can be staggered for an overview. Derive each card’s phase from a shared clock plus an offset. For individual exports, start at the action’s beginning and include its result and reset. Cropping a montage at an arbitrary time can omit the first action; a full cycle may require a rotated clip or a fresh render. Verify each crop and keep its aspect ratio; do not stretch the entire app to fill a slot.

## Contact sheet helper

The helper needs Python 3 and Pillow. It assembles already-rendered keyframes; it does not create or edit their designs. Relative image and font paths resolve against the JSON file, so a saved manifest stays portable.

```json
{
  "title": "Review cuts: workflow proposal",
  "columns": 3,
  "tile_width": 420,
  "tile_height": 300,
  "font": "assets/brand-regular.ttf",
  "frames": [
    {"file": "frames/01-start.png", "label": "01 Start", "note": "Observed · proposal ready"},
    {"file": "frames/02-review.png", "label": "02 Review", "note": "Code-backed · reveal the proposed cuts"},
    {"file": "frames/03-result.png", "label": "03 Result", "note": "Observed · applied plan, readable hold"}
  ]
}
```

```sh
python3 ~/.codex/skills/app-workflow-demo/scripts/contact_sheet.py sheet.json --output review/contact-sheet.png
```

Use tall tiles for portrait carousel artwork. Labels live outside the images. Long notes wrap; do not use them to explain unreadable artwork. Keep the original full-size frames available beside the sheet.

## Verification

Use the current HyperFrames CLI skill for supported check, snapshot and render commands; do not copy an old pinned CLI version from a case study. Check encoded media separately with ffprobe for dimensions, pixel format, frame rate and duration. Decode frames immediately before and after consequential actions and at the final hold. Review them at the final publishing size as well as full resolution.

Watch a complete encoded cycle, including the end-to-start transition if advertised as a loop. A pixel-difference test only proves something moved; it cannot prove the right button was clicked, text is readable or state is truthful. Counts and timeline projections need domain checks. Ensure source assets are bundled locally for reproducibility.

MP4 does not encode an infinite-loop playback instruction. Its repeat behavior depends on the destination player. Construct a clean cycle, but do not promise a platform will loop it.

## Embedded UI rendering

A local test exposed iframe content disappearing in the encoded MP4 even though snapshots were correct. If isolating copied app CSS, verify a short encoded sample with the real UI visible before a full render. Shadow DOM or scoped components can avoid iframe capture differences; make fonts and inherited body styles explicit when isolating them. This is a renderer compatibility check, not a reason to redesign the source UI.

## Pacing and moving review

When narration is selected, follow [narration.md](narration.md): capture and arrange the real screen sequence into a visual rough cut first, curate narration from those shots, then use measured voice durations to refine final timing. Preserve visible action order; neither the rough cut nor estimated speech duration is a final lock.

Allocate duration by what the viewer must understand: orientation, comparison, manual action, evidenced processing and result. Do not copy one scene duration across sparse and dense screens. Scroll only through content needed for the claim; a page with no relevant lower content does not need a token scroll or return-to-top. Full-page context can be brief when detail follows. A noticeable hold needs a specific reading, inspection or decision purpose.

Start input promptly after focus and show its response in order. Cursor travel around 0.25–0.5 seconds and brief click feedback can be useful starting values, not timing requirements. Compress actual waits without inventing latency, percentages or loaders. Avoid repeated zoom-settle holds and idle pointer travel. Camera movement, decorative drift or a moving cursor over unchanged endpoints cannot stand in for the changed workflow.

Before replicating a new scene/camera pattern, encode a short representative segment containing its context, detail and action/result. Review it at normal speed and destination size. Can the viewer identify what changed without pausing? Can they see the target and result without relying entirely on the caption? Adjust framing, copy and event timing before producing all scenes. Reuse this proof when the pattern is unchanged; do not add a new user approval gate for every sample.

Review the complete encoded film after assembly, including transitions and the ending. Identify any interval that adds neither information nor needed reading time. Fix those intervals in the composition rather than globally accelerating the MP4. Freeze detection can identify candidates, but neither a static frame nor pixel movement alone proves good or bad pacing. Preserve natural actions and necessary reading; duration is an outcome, not a target.

At delivery scale, test the important app text and captions as actually displayed (for example, a 1080px portrait export at 360px width). Contrast checks do not establish readable size, and DOM checks miss text baked into screenshots. Remove redundant headers and shorten copy before shrinking it. A full-device context shot need not make every label legible; the detail proving the claim does.

Keep the review conclusions distinct:
- **Technical:** encoded dimensions/audio, no missing assets, deterministic seeks and correct media playback.
- **Evidence/fidelity:** version, data and claims match sources; visible input produces the supported result; reconstruction limits disclosed.
- **Editorial:** information selection, matched comparisons, destination-size comprehension, purposeful holds and sound taste. State which portions were actually watched or heard.

## Visible input and pointer coordinates

A desktop reconstruction needs a visible pointer throughout its manual interactions, including travel, click, held drag and release. A mobile reconstruction uses touch indicators and gesture paths, not a desktop mouse. Make feedback restrained but legible at the delivered size. Match the app’s accent and motion style: use a gentle, brief click pulse and faint held-drag feedback rather than a large spotlight, bright ring, or prominent arrow by default. Let the control’s own state change carry the demonstration. Do not disappear the pointer immediately after every click or teleport it to the next target. It may rest while a loader or AI response does real work; no decorative motion is required.

Keep the pointer tip, click halo and target in the same coordinate system and camera transform. Explicitly anchor absolute overlay layers (for example `top: 0; left: 0`); an unanchored absolute element can start after the app content and be clipped outside the viewport despite correct numeric coordinates. Map the pointer to the visible control before its state changes. During a drag, the pointer and affected handle/object must move together and finish at the same location.

Verify the encoded video, not only source declarations: sample approach, contact and response for every consequential action. At publication size, a viewer must be able to tell what was activated without reading the caption. Check opacity, clipping, stacking, pointer-tip alignment and click timing. A cursor baked into preview footage is not the demo's interaction pointer. Automatic results and AI responses should remain automatic; show their initiating input rather than fabricating clicks.
