# Feature grids and recovery flows

## Two, three or six features

A grid is a presentation of independent demonstrations, not a claim that the app has a dashboard containing those cards. Keep each card’s actual controls, local pointer and state sequence together.

Choose a layout for the destination: two roomy cards side by side in a wide frame, three across or a balanced two-plus-one when that keeps controls readable, six in a 3×2 wide frame. In portrait, consider 2×3 only for a high-level overview; dense UI needs a separate full-size slide or focused reveal. Do not shrink six full app windows into illegibility merely to satisfy the count.

Before animation, show the overview plus start/action/result frames for each distinct feature. Use an explicit feature list and parameterized card count. Brand tokens and card chrome are shared, while content and action timelines are independent.

Offset loops slightly for natural activity. Choose durations by each feature’s reading/action load. A shared loop period may be useful, but padding every card with long idle holds is not. Each local sequence needs a complete result and a coherent reset. At any overview moment, important state changes should not all compete for attention; a lightly emphasized active card can guide the eye without stopping the others.

When exporting a feature separately, begin at its own start, retain the full action and outcome, and do not include cropped neighboring cards. Geometry and contrast are checked at the actual publishing size.

## Failure, chat and recovery

For a requested end-to-end example, map entry, preparation, request, review, edit and output. Use the actual connected chapters instead of inventing a generic “success” screen. Show relevant chat with natural prompt text and the supported assistant mode.

A failure must have a real documented trigger, a recoverable state, a clear next action and a visible return to the workflow. If only a proposed design defines it, label the film as a concept. Do not fabricate errors just to add drama or claim a retry succeeded with an unsupported method.

Select representative failure branches rather than making every possible failure occur in one fictional session. If necessary, show an alternate branch as a separate short segment with clear continuity. Preserve the file, selection and chosen settings when the design says they survive recovery.

Examples grounded in the Simplify Edits chapters:
- External audio mismatch keeps camera audio selected and offers another file or manual alignment. Transcription waits for the final sound choice
- Screen matching can fall back to manual selection. Choosing screen material must not silently replace the established voice source
- Unsupported motion uses a supported fallback and explains it rather than inventing a new preset
- A missing/private/short overlay follows the chapter’s recovery behavior; a hidden monitor is not the same as excluding a layer from export

A visual demonstration of waveform alignment is not proof of audible sync. If sound accuracy is claimed, listen to and inspect the actual rendered audiovisual output at meaningful points. Otherwise say the test covers UI/workflow only.
