# Release comparison: evidence to story

Use for a release-change showcase, redesign comparison or “what changed since the live version”. Purpose is separate from length, camera style and evidence status. A useful comparison explains selected changes and their consequences; a complete film does not imply every commit or screen.

## Establish the two authorities

Resolve the baseline from the user's confirmed release, store/build evidence or release metadata. A latest Git tag is not proof of the currently published store build. Record version/build, commit and the authority connecting them; qualify unresolved mappings rather than guessing. For the new version, record the commit plus relevant uncommitted files or a preserved patch/source snapshot. Do not compare a clean commit while silently omitting the local refinements the user asked to show.

Inspect available local Git history/diffs first. Use accessible GitHub releases and PRs to understand intent or resolve provenance where useful; trace important claims into changed components, handlers and state. PR titles are candidate leads, not proof that behavior shipped. Screenshots can support appearance comparisons but cannot establish unseen interactions. No additional remote access is necessary when the needed evidence already exists locally.

Keep production sources intact. Record a compact manifest with source references, viewport, fixture inputs, asset locations and reconstruction limits so another session can resume without rediscovering the entire repo.

## Select claims before screens

Inventory meaningful changes, grouped by visual structure, interaction/navigation, data behavior, user-visible fix and infrastructure. Read enough surrounding code to distinguish a new capability from a new way to reach an existing one. Select the changes that support the audience's takeaway; use show, recap or omit decisions rather than allocating equal screen time to every modified page.

Use one compact table in the brief or storyboard:

| Claim | Old → new evidence | Viewer benefit | Representative scenario/data | Proof and scene | Decision / confidence |
| --- | --- | --- | --- | --- | --- |
| Revise one item | Source symbols or observed states on both versions | Correct a mistake without recreating the record | Same underlying amount; current data includes actual editable items | Select row → edit → updated row/total; scene ID | show / code-backed and fixture-observed |

The example is a schema, not a feature to invent. Each selected claim needs visible proof or an explicitly source-backed recap. Distinguish “demonstrated” from “mentioned”. Record a short reason for important omissions; do not turn infrastructure changes into fabricated UI. If an action existed before, name the specific change in access, layout or outcome instead of calling the capability new.

## Choose representative data and behavior

Keep facts comparable across versions: amounts, period, counts and selected object, but use each version's correct data model. A legacy fallback may hide the new behavior even when it renders without errors. Trace read-only rows, missing item records, flags and migration states before choosing the hero example. Include legacy compatibility only when it is the intended story.

Prefer a small action/result cycle for a behavioral change: real initiating control, intermediate response, next step and visible outcome. Use controlled fixtures or isolated app components; record which handlers were exercised and which states were directly mounted. A fixture-observed local interaction does not prove a live backend or store build. Apply the [capture preflight](evidence-and-states.md#representative-fixtures-and-capture-preflight) before bulk capture.

## Matched component shots

Use a treatment that fits the evidence and destination:

1. Establish whole-page location and version context.
2. Isolate the corresponding old/new component at comparable scale and with matched facts.
3. Reveal the meaningful visual difference using a paired view or registered replacement.
4. If the claim is behavioral, return to enough app context to show the initiating input and result.

A device frame is optional per shot. For a simultaneous portrait comparison, place Before above After: keep both whole phones visible for context; if a detail view is chosen, explicitly transition both to matched frameless app/component crops. Do not obtain detail by clipping the physical phones offscreen. Preserve both versions throughout when that is the requested comparison, with comparable scale and data; do not leave one as a tiny unreadable reference. Stacked specimens or a registered old/new replacement are alternatives when simultaneity is not required. Side-by-side works when both remain legible. A “registered” replacement aligns the same semantic region; it does not stretch differently sized components into identical geometry. Label versions outside the source UI. Preserve source typography, controls and proportions, and include surrounding context needed to identify the specimen.

Adapt `assets/presentation-shells/comparison.html` and `comparison.css` for layout. Supply real captures or extracted components and explicit crop/bounds data; these assets are not product mockups or a ready-timed video. Animate the shared wrapper for camera movement and the specimen layers for a comparison reveal. Before/after wipes and editorial morphs are presentation devices, not evidence of native app animation. Avoid morphing one action into another if that implies unsupported product behavior.

Alternate context, comparison and action only as the information requires. Do not impose the same scene pattern or number of zooms on every change. See [pacing and moving review](production.md#pacing-and-moving-review).

## Review the release story

At destination size and normal speed, can the viewer identify the old problem, the concrete change and its benefit? Check that selected claims map to the delivered shots, old/new data are comparable, actions are supported and “new” labels are true. Preserve uncertainties in the production notes. Source-backed fixes without visible proof may be recapped briefly; never count them as demonstrated interactions.

When asked to improve and rerun an existing demo, preserve its video, brief and skill version when available. Compare claim coverage, legibility, necessary action/result steps, pacing and correction effort. Record measured durations and limits; do not invent efficiency percentages from render time or treat one improved example as a general benchmark win.
