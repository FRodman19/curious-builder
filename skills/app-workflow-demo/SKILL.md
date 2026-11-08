---
name: app-workflow-demo
description: Create faithful app workflow demos and release before/after showcases from source code, Git changes, a running app, screenshots or recordings. Reconstruct branded UI, compare changed components and demonstrate changed behavior; prototype interactions only when requested. Start with designed keyframes. Use for product behavior demonstrations, not ordinary screen capture or unrelated motion graphics.
---

# App Workflow Demo

Create reusable product demonstrations for any app: an app introduction, a specific feature, or a complete feature tour. Reuse the target product’s actual UI components, visual materials and interaction behavior. Explain cause and effect through its interface, then frame it for the intended publication. A designed reconstruction is not proof that the app performed an action.

For sharing or first use on another computer, read [portability and setup](references/portability.md). Share the whole skill folder so its sound assets and generator travel with it; check renderer dependencies and new-project UI sources separately.

## Start with the evidence and intent

Read `../VIDEO-SYSTEM-AGENTS.md` and its context when not already loaded. For animation, enter `../hyperframes/SKILL.md` as required by the video system. This skill owns workflow fidelity and the contact-sheet requirement; HyperFrames and its owning workflow supply animation/render mechanics. Reuse an existing approved brief rather than reopening discovery through another skill.

Infer from the request and project first:
- The feature, audience and one thing a viewer should understand
- Available code, live app, screenshots, recordings, approved design chapters and reusable assets
- Purpose: workflow demonstration, release-change showcase or instructional walkthrough; keep this separate from existing-feature versus proposed-feature evidence status
- Short product demo or complete workflow demo, separately from the layout choice: continuous walkthrough, feature loop, a grid of two, three or six cards, or live recording
- Camera treatment, independently of scope: whole-device/window by default; optional explicitly framed app/component details when requested or needed for readability
- Target platform and presentation: desktop window, macOS setting, mobile device frame or app-only view
- Destination, aspect ratio and whether the request stops at the contact sheet

During setup, if narration is unresolved and would help this demo, make one optional offer: “Would you like a voiceover?” Briefly distinguish no voice, installed local speech, a user-provided recording or an explicitly authorized AI voice provider, and suggest an instructional or explanatory role appropriate to the task. Read [narration.md](references/narration.md) if relevant. Preserve existing voice/no-voice choices and presets; do not repeat the offer or block otherwise authorized capture and visual work while it remains unanswered. An unanswered offer is not authorization to generate speech.

Ask only about a material gap. If “show the app” does not identify a workflow, suggest one grounded in the project and ask which feature matters. Do not make the user restate paths, brand or flows already available. A request for a live recording stays a live recording; do not silently replace it with reconstruction.

Use [evidence-and-states.md](references/evidence-and-states.md) to inspect the source. Record a compact `BRIEF.md` with source authority, app version, audience, workflow, dimensions and unresolved questions. Explicitly distinguish:

| Mode | What can be shown |
| --- | --- |
| Existing feature | Behavior supported by the target app/version, recording or other evidence |
| Screenshot-led reconstruction | Visible UI faithfully reproduced; missing transitions remain assumptions until confirmed |
| Concept | User-authorized proposed behavior; identify it as a concept on the review sheet and in exported work |
| Presentation illustration | A simplified explanation, such as a before/after wipe or feature grid; do not imply it is an app control |

A screenshot proves appearance, not what an unseen click does. A planned design chapter proves intent, not implementation. If code and selected visual reference conflict, surface the specific conflict and ask only if it affects the demonstrated action. You can prepare uncontested frames while waiting.

Faithful reconstruction is the default, not creative redesign. Reuse the supplied screens, components, icons, avatars and media; do not substitute invented app assets or controls for convenience. Missing animation may be reconstructed between evidenced states, but must not introduce unsupported behavior. Record each necessary addition or adaptation, its source gap and its purpose in the evidence table, and disclose meaningful additions with the contact sheet. Proposing a new feature requires user intent for a concept; labeling an existing-feature demo as a concept is not a way to bypass missing evidence.

## Release-change showcases

For “old versus new”, “what changed” or a shipped-release comparison, read [release-comparison.md](references/release-comparison.md) before selecting screens. Resolve both versions, classify meaningful changes, and connect selected claims to representative data and visible proof. Use matched component excerpts where they explain a difference better than another full-device shot. A release showcase can contain a complete changed workflow; it need not inventory every page or commit.

## Choose the demonstration mode

Read [modes-and-captions.md](references/modes-and-captions.md). Two modes share the same source-fidelity standard:

- **Short product demo** shows the key actions and their results with condensed waits. It can omit unrelated setup but must show the real controls and a coherent action cycle
- **Complete workflow demo** follows the selected task from beginning to end through all necessary pages, sidebars, panels, dialogs, settings, AI interactions, reviews and output. It remains a polished product demo, not a slideshow of endpoint screenshots

Use the request and existing choices to infer scope. Ask only when a material ambiguity remains; explain the practical difference rather than asking merely “short or complete?” A complete film is a finished deliverable, not automatically an exhaustive tour. Complete workflow means connected coverage of the selected task, not extra time or every unrelated feature. Length follows the information and actions; see the canonical [pacing and moving review](references/production.md#pacing-and-moving-review).

Use a clear centered page/action heading on the brand backdrop outside the phone or window. A second action-caption strip is optional; honor titles-only preferences and keep visible actions understandable. Narration and burned-in subtitles are separate choices. Choose the mode before the contact sheet. Do not treat approval of short-mode keyframes as approval to invent a complete workflow.

## Choose the camera style separately

Default to **whole-device/window mode**: keep the entire physical phone or window visible inside the safe canvas throughout its shots. Actions, scrolling and navigation move inside it; actions do not automatically trigger zooms. Size the frame generously while reserving a centered page/action heading outside it. This default also suits a conversational walkthrough.

Use **detail mode** when chosen or necessary to read a demonstrated component. Transition explicitly to a frameless app/component view, then return when context is needed. Do not enlarge a phone until half its hardware is clipped offscreen. Keep input targets and results in the detail's shared coordinate system. A requested stable whole-device tour stays whole-device; do not force a detail shot on each page.

Read [camera and mode guidance](references/modes-and-captions.md) and [heading/device framing](references/caption-and-device-framing.md). Keep consumer-facing copy focused on the page, action and benefit: no slide counters or production-method footer badges. Preserve provenance in the brief/review sidecars, with only material concept or before/after status on screen when needed to avoid misleading the viewer.

## Match the app and the publishing context

Read [app-fidelity-and-presentation.md](references/app-fidelity-and-presentation.md). Inspect the target app’s real components, fonts, colors, iconography, materials and motion. Preserve frosted/liquid glass, blur, translucency, shadows, parallax and interactive animation when they exist in the source; do not flatten them into a generic UI. Reuse source components and native motion logic where feasible, then adapt playback to deterministic rendering. A reference recording can supply the behavior and pacing; it is not permission to replace the target app’s brand with the reference app’s.

Select the presentation shell independently of the app UI: a desktop or Mac window, a phone frame for a mobile app, or a clean app-only view. Use the correct platform conventions and a compatible background, with adequate contrast and visible controls. For a polished guided showcase, use a softly blurred aurora derived from the target app’s design tokens and restrained physical depth on the outer device/window, as described in [app fidelity and presentation](references/app-fidelity-and-presentation.md#brand-aurora-depth-and-canvas-occupancy). Give the app most of the usable composition; choose a simpler background or flatter frame when fidelity, contrast or the requested style calls for it. Do not put Mac traffic-light buttons on a mobile app. Frame the video for its destination and aspect ratio without stretching or reflowing the real UI into an invented layout. Infer from the brief, source app and publishing context; ask only when the platform, fidelity or framing choice materially remains unclear. Put framing alternatives on the contact sheet when useful.

If a design system is available, inspect and reuse its tokens, components, assets and motion rules before building; record its source/version in the brief. If none exists, derive the smallest evidence-backed set from the supplied UI or references. For an explicitly requested brainstorm without existing UI, first create a coherent proposed screen and component language from the available brief/references, label new decisions, and review those screens before animating them. Do not quietly import another app’s style or pretend proposed UI is implemented.

This skill has no default Simplify Edits appearance, assets, avatar, palette, timeline, or feature set. Its case study documents the method and lessons only. For Rhydle or a new app, re-discover that app’s own UI and user flow. If a proposed app has no implementation, use its supplied or approved design system and clearly label the proposed behavior.

## First deliverable: a contact sheet

For a new direction, build actual designed keyframes and show a numbered contact sheet before full animation. This is the user’s standing review preference. Reuse existing approval for unchanged choices; a user-directed revision with authorization to produce is authorization to implement that revision. Update the affected keyframes and inspect them yourself without reopening settled choices. Ask again only when a material new choice is unresolved or the user explicitly requested another review. An explicit instruction to skip review overrides the default.

Show the initial context, action target, response/loading state, result and reversal or next step where relevant. Every demonstrated transition needs understandable before/after states. Include one full-window orienting frame and close views only where they clarify the action. For multiple independent cards, show the overview and representative states per card.

Label sheet panels outside the artwork with action, evidence status and intended motion. Show unknown behavior as an unresolved note, not a polished success. Full-size keyframe images accompany the sheet so labels and controls can be checked.

The optional [contact sheet helper](scripts/contact_sheet.py) assembles rendered PNG/JPEG keyframes without distorting them. See [production.md](references/production.md) for its input format.

Read the sheet yourself for hierarchy, word spacing, branding, clipping and workflow logic. Record the reviewed version and any later user-directed changes. Present and wait when review is still required under the rule above. A sheet cannot establish pacing: validate one representative moving segment before replicating a new camera or transition pattern, using [production.md](references/production.md#pacing-and-moving-review).

## Critique and improve the first pass

Read [the critique procedure](references/critique.md). Before presenting any contact sheet, save the first pass privately, compare the rendered work with its source, identify specific defects, revise them, and inspect the revised result. The agent supplies the first pair of eyes; the user is not the quality-control system. Only show the revised sheet after this gate passes. Share the meaningful findings briefly. Check background color, gradients and texture; animation and transition intent; text placement, hierarchy and line breaks; spacing, contrast, cropping and alignment. Include full-size and phone-size checks, especially nested light/dark surfaces. Repeat the critique on the encoded output. Do not treat a render or metadata-validation pass as proof of visual quality.

## Reconstruct the interface

After approval, load [production.md](references/production.md). Prefer this order:
1. Reuse isolated app components in a controlled fixture when feasible
2. Reconstruct the needed HTML/SVG with extracted fonts, icons, colors and assets
3. Use screenshots as faithful surfaces with explicit layer boundaries
4. Use real capture when requested or when reconstruction would lose essential behavior

Work outside production app surfaces unless product changes are requested. Use fixture data and disable mutating/network actions in copied UI. Do not trigger real sends, purchases, deletes or project edits merely to animate their appearance.

Show the screen as the user would actually see it. Keep dialogs within the canonical app shell and preserve the real page/panel layout. Establish the full app view before a closeup. Matched component excerpts are useful presentation illustrations for comparisons; preserve their source geometry and return to context when an action needs it. They do not replace necessary steps in a requested connected workflow.

Keep one coherent state model. Cursor, focus, text, status, preview, counts and timeline must describe the same state. Reproduce meaningful intermediate steps. Do not substitute a new shortcut for a difficult-to-animate real action.

For concepts, use the app’s existing component language and a plausible complete interaction. Mark proposed parts and explain assumptions in the sheet. Do not modify production code just to support a marketing concept.

## Grids and recovery flows

For a two-, three- or six-feature grid, read [grids-and-recovery.md](references/grids-and-recovery.md). Choose the card count from the user’s request and available feature evidence, not a hardcoded six-card layout. Show grid composition in the first sheet. A requested end-to-end workflow includes its connected pages, relevant chat exchanges, documented failure/recovery states and final result. Do not force every error branch into the happy path.

## Motion and delivery

Use HyperFrames with a deterministic seekable timeline by default. Preserve approved designs while adding motion. Length follows the demonstrated workflow, not an arbitrary ten-second target.

- Make each user action visible: desktop uses a readable moving pointer and click/drag feedback; mobile uses tap/press/swipe indicators. Move to the actual control, activate it, then show its response. Keep desktop pointer continuity through the workflow. For a presentation excerpt, a clearly anchored highlight or arrow can clarify the target; captions alone cannot substitute for visible interaction
- Distinguish user input from automatic or AI-driven responses. Show focus, typing and submission for a request, then the agent’s working/result state; do not invent mouse clicks for background work
- Typing starts immediately after focus; request submission leads to a brief visible working state
- Condense processing waits while preserving cause and effect; do not invent completion percentages or performance claims
- Animate the actual response continuously: dragging changes the target geometry, typing updates text, playback advances related views, and loading leads directly to its result. A moving cursor or camera does not make an unchanged UI a complete animation
- Camera moves only when they improve understanding; cursor and UI share the same transform
- Loops finish a meaningful outcome before returning to a coherent start
- Independent feature cards each complete their own understandable loop; do not replace them with one global cursor tour
- Preserve real playback speed where playback fidelity matters, separately from compressed demonstration time

For transcript/video editors, synchronize transcript, video, words, audio, ruler and playhead from one source-time model. Cuts close gaps, then the viewport may refit. Restoring/undoing must update every related view. Do not stretch media or fabricate blank timeline intervals. This is a domain-specific example, not a required layout for other apps.

Use the [production verification and pacing review](references/production.md#verification) on the encoded result. Keep technical, evidence/fidelity and editorial findings separate; a successful render does not establish all three. Report unverified behavior precisely.

For requested narration, read [narration.md](references/narration.md): inspect and capture the real screen sequence first, arrange a visual rough cut, then curate speech around what is actually shown. Generate the chosen voice and refine final timing to its measured durations; do not invent visuals to fit a prewritten script. Reuse the user’s choice of no voice, their recording, installed OS speech, a local AI model or a cloud provider. The bundled macOS helper uses installed voices without credentials, downloads or external fallback.

For requested sound effects or ambient background audio, read [local sound design](references/local-sound-design.md). The skill bundles 21 compact MP3 sound assets, an audition catalog, and an offline generator for mechanical clicks, typing, UI feedback and ambience without API keys. Inventory the real components first and distinguish mouse clicks from pops, typing from incoming AI text, and loading from success. Time effects to actual interactions, preserve intentional silence, and disclose added presentation audio. Record the audio role explicitly: silent, effects only, ambient/music plus effects, or voice-led. Effects do not automatically authorize a bed; when a longer showcase would benefit, offer that choice once unless already resolved. Use the no-voiceover mix profile when appropriate; apply an ambient onset only if a bed is selected, and duck it under speech. Audition the encoded mix and disclose any inability to listen.

Default social deliverable: H.264 MP4, yuv420p, suitable dimensions, fast-start; silent unless audio is requested. Use GIF only when requested for a compatible destination, never as the default social-video substitute. Render from the original composition or master, not a reduced-color GIF. Still keyframes remain PNGs.

Keep editable source and evidence in the working directory. Deliver only the requested clips with simple names, separate hooks if requested, and a single captions Markdown file only if requested. No publishing, site replacement or deletion of past work is implied.

## References

- [Evidence and state mapping](references/evidence-and-states.md): code, app, screenshots, recordings and concept gaps
- [Production details](references/production.md): determinism, pacing, contact-sheet manifest and verification
- [Simplify Edits case study](references/simplify-edits-case.md): how the source workflow was actually built and corrected; consult for this app or a close analogue, not as a universal theme
