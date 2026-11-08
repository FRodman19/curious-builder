# Evidence and state mapping

## Inspect the right product version

Check project instructions and the user-selected branch/version before tracing UI. A nearby checkout can be older than the shipped build or selected design chapter. Record the authority instead of mixing screens from different versions silently.

With source code, find:
- Relevant route/component and its visible variants
- Exact labels, menus, disabled states and handlers
- State transitions, request boundaries, approval points and result views
- Undo, restore, cancel or retry when part of the requested story
- Fonts, font weights, semantic colors, radii, shadows, icons, avatars and sample media
- Existing fixtures and demo data that preserve believable counts and durations

Inspect a running app or recorded reference for the key interaction when available. Do not treat handler names or tests as proof of what a user sees. Use the applicable browser/computer skill and its access constraints. If the app cannot run, state that limitation and use code-backed states without claiming hands-on verification.

With screenshots, identify the known viewport and screen order. Retain actual geometry and labels; reconstruct only necessary layers. Request the one missing outcome screenshot or a short explanation if the missing transition is essential. Do not invent where a button leads. With a recording, inspect frames before the action, during the response and at the result; record their timecodes and extract assets from authorized sources, not unrelated UI. Rebuild those evidenced screens faithfully rather than using the recording only as loose visual inspiration.

An approved prototype or design chapter may be the chosen visual authority even when unshipped. Keep implementation status distinct from design approval. A familiar logo does not prove integration or endorsement.

Distinguish product UI from explanatory material in design chapters. A detached timeline diagram, annotated specimen or comparison card is not evidence of an app dialog. Do not place it in an invented modal to make it fit the screen. Reproduce the documented action on the real timeline/panel; keep any explanatory inset outside the app and record it as presentation artwork in the evidence notes; use on-screen identification only when needed to avoid mistaking it for a product control. If the actual placement is unspecified, record that gap.

## Representative fixtures and capture preflight

Choose data that makes the selected claim observable. Preserve comparable business facts across versions, not necessarily identical storage structures: a new item-level workflow needs real editable items, not legacy aggregate fallbacks. Trace disabled/read-only variants, feature flags, units, filters and empty states before selecting a fixture. Record the starting state, initiating control and observable result. Mounting result screens directly can prove their appearance; it does not prove the connecting interaction.

Before bulk capture, render one representative context frame, one dense detail and one consequential action/result. Check fonts and icon glyphs, currency/unit conversion, counts, native assets, nested scroll coverage and component bounds. Prefer measured bounds from the rendered component; keep any fallback crop coordinates alongside the capture viewport so they can be reproduced. Use isolated source copies and neutral fixtures. Do not alter production behavior to make the demo work.

For release comparison, use [release-comparison.md](release-comparison.md) for version provenance and claim selection.

## Compact evidence table

Store this inside the brief or a small supporting file, not in the public post pack:

| Beat | Before | User action | Response | Result | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| Review | Proposal available | Open review | Proposal rows | Reviewable cuts | Source path/symbol, recording time or screenshot | observed / code-backed / assumed / proposed |

Use real source references, not “based on the app” for every row. Include asset paths, font weights and token origins. For conceptual UI, record which elements are existing versus proposed. File metadata or a comment can document provenance; it need not become an on-screen tag on every real demo.

For any addition, keep a compact record: frame/beat, element or transition, what the source provides, what was added or changed, why it is necessary, and whether it is a presentation device or proposed product UI. “Concept” alone is not sufficient provenance. Reused assets need a source reference, not an addition entry. Captions, pointers and camera framing belong outside product behavior; missing product controls, states and assets must remain identified gaps or explicit proposals. Disclose the meaningful additions in the review and never claim they existed in the app.

Ask a focused question when an essential row is unsupported. Example: “After selecting Transcribe, does the app open this panel automatically, or does the user choose a model first?” Do not ask a broad questionnaire when the project answers it.

## Meaningful invariants

Derive checks from the workflow, not from a universal list. Examples:
- A proposal is not shown as applied before the real approval step
- Undo returns to the appropriate prior state, not an arbitrary original screen
- A removed item remains available only if the product supports restoration
- A loading indicator does not make up a percentage, ETA or streaming capability
- Displayed counts, selected item, output file and preview agree
- A shortened timeline has contiguous retained intervals; its ruler reflects the new viewport
- A source excerpt is visibly an excerpt if it could be mistaken for the entire document

Do not silently “fix” product behavior for marketing. Simplify framing, not the action contract.

## Sensitive sample content

Use supplied demonstration material or neutral fixtures. Replace exposed credentials and private customer data. Maintain internally consistent filenames, counts and representative content. Never access unrelated private data to make a demo feel real.

## Source drawings can contradict themselves

Read the chapter register and settled decisions alongside the drawing. “Exists” in a design comparison may mean an earlier design, not a shipped implementation. A status badge, an applied result and the assistant permission mode must agree. Do not show an applied result before an Ask before apply confirmation.

When combining chapter fixtures, reconcile project/file names, selected spans, word counts, timeline rulers, playheads, preview durations and export duration. Use one explicitly recorded sample dataset. An after-state must visibly contain the change: an applied title needs a title on the canvas and its timeline item; moving an object must update its selected inspector position. A chat reply saying “done” does not demonstrate success.

Scope copied CSS or isolate components. Chapter-wide selectors such as `.row`, `.note` and `.card` can break a new chat or small feature card. Inspect the actual browser result before presenting it.
