# Critique, revise, verify

This is a required internal gate BEFORE the user sees a contact sheet, not a closing checklist. The agent reviews and fixes the first pass itself. Do not knowingly send an unreadable or broken sheet to the user for them to catch.

1. Save the first pass separately before changing it
2. Inspect the actual rendered contact sheet, every full-size frame and the intended phone-size view
3. Compare app frames against the source UI or approved design at the same viewport
4. Record concrete defects with frame/slide IDs, evidence, viewer consequence and the planned fix
5. Fix them and inspect the same views again
6. Only after visible defects are fixed, present the revised work and a short honest critique. Show before/after only when useful; do not make the user inspect every failed draft

Do not self-award a score or call something premium because it rendered. A successful metadata check is not design validation. A still-sheet approval does not excuse render defects. Repeat this critique on the encoded result.

## Fidelity

A workflow demo shows the actual screen the user would see. Preserve app chrome, page structure, panel positions, active tools, dialogs in context and the controls that drive the next action. Keep the whole device/window visible in whole-frame mode. Chosen details transition to frameless content instead of clipping the hardware. Do not replace required workflow steps with floating marketing cards. A release comparison or carousel may use matched component excerpts as presentation illustrations; preserve source geometry and context needed to understand the claim.

For unbuilt features, match the approved design assets and identify the film as a concept. If a chapter only describes a state without drawing the full screen, reconstruct that state inside its canonical app shell and identify the adaptation. Never describe such a reconstruction as an exact recording of implemented software.

## Message and visual review

Read each slide without the accompanying explanation. Does the second hook add a concrete problem? Does the picture support the heading? Is each action understandable? Can a person see the primary content at phone size?

Check explicit foreground and background colors on every nested surface, particularly light cards on dark slides. Check line breaks, letter spacing, clipping, text inside components, overlong chat rows, empty space and contrast. Reusing a source does not guarantee its CSS will remain correct after extraction.

For motion, inspect immediately before a click, immediately after, after loading, after application, and at the loop seam. Pointer, preview, transcript, timeline, inspector and result text must all agree. A success message with an unchanged canvas is a failure.

## Useful critique format

| Frame | What failed | Why it matters | Revision | Verified evidence |
|---|---|---|---|---|
| Slide 02 | Light text inherited onto a white card | The problem is unreadable | Explicit dark text or a dark card with light text | Full-size and phone-size screenshots |
| Demo recovery | Detached specimen card | Viewer cannot understand where it opens | Dialog inside the app window | Compared with chapter shell |

Keep this report outside the user’s publishing folder. Share the few meaningful findings in plain language. If something remains unverified, say what is missing rather than implying it passed.

## First-eye checklist before presentation

- Background and texture support the subject, stay subtle, and do not degrade legibility
- Gradient hues come from the target brand; no arbitrary decorative palette
- Headings, body text, labels, icons and CTAs align and remain readable at destination size
- No accidental gaps, awkward wraps, stretched UI, unexplained empty space, or tiny key controls
- Static artwork reads without movement; proposed animation has a clear start, action and result
- Before full rendering, verify initial/result keyframes and transition plans. After animation exists, play it at normal speed and inspect loading, click timing, typing, cursor movement, zoom anchoring and loop seams
- Camera treatment matches the brief: whole-device shots keep all hardware in frame; optional details are explicitly frameless and keep targets/results visible; no automatic action zooms
- The centered page/action heading stays outside the device and readable at feed width; no duplicate caption strip when titles-only was selected. No slide counters or internal production badges. Android status icons and punch-hole are visible, proportional and not duplicated from the capture
- Design-system tokens, assets and motion remain faithful; proposed design decisions are explicitly identified
- At delivered size, manual actions visibly show desktop pointer travel/click/drag or mobile tap/swipe, aligned with the real target and its response. Check approach, contact and result in the encoded video; source code containing a cursor is not proof it renders
- No missing assets, frozen videos, unintended controls, offscreen pointers, stale state or visual effects hiding the feature
- Text and UI state match the source evidence and the same sample dataset

Do not mark this gate passed from source inspection alone. Inspect the rendered output. Fix known defects without another permission request. If missing evidence prevents faithful work, surface that specific gap rather than polishing an invented interaction.

## Motion and destination review

Use the single [pacing and moving review procedure](production.md#pacing-and-moving-review) for the representative sample and complete encoded film. For a release showcase, cross-check selected claims against the [release inventory](release-comparison.md): a beautiful screen is not proof of a changed interaction. Separate technical, fidelity and editorial findings, and record actual viewing/listening limitations.
