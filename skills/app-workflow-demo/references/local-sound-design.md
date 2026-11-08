# Optional local sound design

Use when the user asks for sound effects or background ambience in an app demo, especially without an API key. Generate audio locally with `scripts/local_audio.py`; it uses deterministic oscillators and seeded noise, no network, API, downloaded samples or generative model. Python 3 and NumPy are required. Check NumPy locally before use; do not silently add a paid provider or external service. The output is a synthesized pad, mechanical input approximations and designed UI accents, not voice narration or a hardware field recording.

For spoken guidance, use [narration.md](narration.md); the sound-effects generator below does not synthesize speech. Keep voice as an editable layer and mix against its actual measured timing.

## Select sound intentionally

Keep demos silent by default. Record the selected role in the brief: silent, effects only, ambience/music plus effects, or voice-led. Honor an explicit or existing choice. An effects request does not by itself select a music/ambient bed. If a longer showcase would benefit and the role remains open, make one grounded recommendation using the available media workflow; do not repeatedly ask or hold up independent visual work. Preserve an existing silent export. Use the target app's interaction character to tune the generator, not a universal brand sound. The skill includes actual assets, not just instructions:

- `assets/ui-audio/`: 21 compact MP3 effects, two ambient beds, playable `index.html`, and `catalog.json`
- `scripts/local_audio.py`: offline synthesis, timed event mixing and library regeneration
- WAV masters are generated into the current project on demand rather than bundled in the skill. WAV is preferred for precise editing and looping; MP3 is a convenient download/audition format and can have codec padding

Open the bundled catalog to audition sounds before choosing them. A mechanical mouse click is a short broadband switch transient with press/release. A pop is a tonal bubble/reveal accent: never substitute it for a mouse click. The mechanical files are synthesized approximations, not recordings of a specific mouse. If exact hardware realism is required, use an authorized recording or licensed source and record provenance; do not call a procedural approximation an authentic recording. Do not silently call an external sound-generation service.

## Inventory real components before assigning sounds

Read the actual workflow, UI source, design system or recording. Write an action/audio table beside the cue manifest: component, visible action, observed timestamp, chosen asset or silence, gain, start/end and reason. The library is a menu, not a requirement to add every sound to every app. Do not invent UI activity to use a sound.

| Real component or event | Asset or default | Timing rule |
| --- | --- | --- |
| Desktop button, menu item, tab | `click` | On visible mouse activation, not cursor approach |
| Press and hold or drag | `mouse_down`, `mouse_up` or quiet `drop` | At press/release separately; no repeated clicks during the hold |
| Actual double-click | `double_click` | Match both activations; use separate clicks if their interval differs from the sample |
| Text field, search, user chat prompt | `key` with modest seeded variations | Match each visible insertion, or a sparse subset at high speed; never play keyboard sounds over AI-generated text |
| Typing audition or draft | `typing` | Example burst only; do not place a fixed typing recording over unmatched text |
| Enter to submit | `enter` | At the Enter event; mouse submission uses a mouse click |
| Backspace/delete character | `backspace` | At actual character removal |
| Checkbox, radio, switch, selection | `toggle` or `click` | When selection changes; choose one, do not stack both |
| Slider, trim handle, resize, reorder | Press/release; optional `snap` | No continuous rattle; snap only at a visible snap point |
| Drag pickup/drop | `drag`, `drop` | Optional stylized object accents, distinct from physical mouse events |
| New card, badge, object reveal | `pop` | At the reveal; optional, not a generic action sound |
| Drawer, modal, moving panel, screen transition | `transition` | Align whoosh energy with movement; avoid on instant tab replacements |
| Network/job/loading state | `loading_start`, optional `loading_loop` | Start after visible work begins, only while it is pending; fade/stop exactly at success, cancellation or failure |
| Progress bar or percentage | Usually silence | Never tick for every percentage or imply a result before completion |
| Success, export saved, finished task | `complete` | Only when success/result actually appears |
| Recoverable warning or input constraint | `attention` | At warning reveal, not every frame or repeated failed drag |
| Failed request or operation | `error` | At failure state; retries return to working state and stop the error sound |
| Incoming message, toast or notification | `notification` | At arrival; no typing sounds for incoming text |
| Undo, redo or restored edit | `undo` or click only | With the actual state reversal; do not imply failure |
| Hover, focus, scrolling, cursor travel | Silence | Unless the source app has a relevant evidenced native sound |
| Media playback and audio editing | Original media audio | Preserve actual source audio; never replace it with invented audio as evidence |
| Mobile tap, swipe, long press | Usually silence or subtle designed tap | Do not use a desktop mouse switch for phone interaction; haptics are not audible recordings |
| Ambient background | `ambience` | Low continuous bed with boundary fades; independent of loading and not a substitute for action sounds |

During a drag, choose a physical press/release pair **or** a stylized pickup/drop pair. For a notification caused immediately by a click, prefer the more informative sound rather than stacking several loud accents. Cap repetitive typing gain and event density, while preserving synchrony. Loading texture is optional and especially easy to overuse; it is never a beep for each spinner rotation.

The ambient bed uses related, slowly crossfading chords, no beat or busy melody. Keep it behind the UI. Vary chord voicings, timbre or seed when appropriate; random variation on every click is distracting. Silence is useful too. Do not put a sound on mouse travel, every caption or every loading frame. Keyboard sounds may follow visible input, but use a quiet sparse subset when dense typing becomes distracting. Do not add delays or change workflow pacing to accommodate sound.

These are **editorial presentation sounds**, not evidence that the app makes these sounds. Record this distinction in the delivery/adaptations notes. Preserve authentic app audio when it is part of the demonstrated feature. Do not imply that synthesized audio came from the user’s media or a successful in-app generation.

## Generate and place

Create an events JSON from the animation's actual activation timestamps, not just scene starts:

```json
[
  {"time": 1.48, "sound": "click", "gain": 0.65},
  {"time": 4.7, "sound": "drag", "gain": 0.35},
  {"time": 12.4, "sound": "complete", "gain": 0.5}
]
```

```bash
python3 <skill-dir>/scripts/local_audio.py --out ./audio --duration 30 --events ./sound-events.json --seed 19
```

The script creates 21 stereo 48 kHz PCM WAV effects, `ambience.wav`, a combined `soundtrack.wav`, an audition sequence `preview.wav`, and a provenance/level manifest. With no events it produces a bed-only soundtrack. Pass `--no-ambience` for an effects-only mix. Each event may specify `seed` for deterministic mechanical variation. A `loading_loop` event may specify `duration`; it is repeated and faded to that exact interval. Other sounds use their natural duration. Regenerate the installed audition library with `--library --duration 24`, which also writes MP3 copies and the HTML/JSON catalog; this additionally requires local FFmpeg. Never use the catalog typing burst as a substitute for matching the actual character timestamps. Duration must match the final timeline. Set events at UI activation, with success cues at the actual visible result, not before processing finishes. Fades protect file boundaries.

For HyperFrames, place the soundtrack as a timed audio element and preserve it in the composition/rebuild source. Read `hyperframes-core` for audio timing and `hyperframes-audio` for mixing. When adding audio to an already approved silent MP4, FFmpeg can copy its video stream and encode only the new audio, preserving the visuals:

```bash
ffmpeg -i silent.mp4 -i audio/soundtrack.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -movflags +faststart -shortest with-sound.mp4
```

Check the input first: this command deliberately selects a new soundtrack and would discard existing audio. If the video already has speech or other meaningful audio, mix it rather than replace it. Use the audio skill's voice carve/ducking guidance when a bed sits under speech.

## Critique before delivery

- Check the encoded file, not just WAV sources: correct duration and channels, finite samples, no clipping, clean start/end fades and no truncated tails
- Review action timing against pointer/click/result cues; automatic processes do not get fake user clicks
- Audition the mix at normal speed, on headphones and speakers when available. Listen for harsh clicks, piercing chimes, repetitive effects, bed hum, abrupt chord changes or sounds louder than the content
- Compare sound on/off. Audio should clarify actions and support continuity without becoming the focus
- Measure levels as supporting evidence, never claim listening quality from waveform statistics alone. If playback cannot be heard by the agent, state that limitation and provide an audition preview for the user
- Deliver a simple watch/download link. Keep the generator, events and manifest in editable source; no elaborate download bundles unless requested


## Audible levels when there is no voiceover

Inspect the actual audio content first. For a demonstration with no narration or important source audio, use `--mix-profile no-voiceover`: effects are 3 dB louder and ambience 4 dB louder than the original subdued palette. These are starting gains, not a loudness guarantee. Preview them together; short mechanical transients and sustained warning tones have different perceived loudness. Avoid normalizing every sound to the same perceived volume or stacking redundant cues.

The two ambient choices are `--ambience warm` and `--ambience focus`. Each reaches its intended level after a short 0.18-second fade, avoiding the earlier four-second quiet lead-in. Keep the anti-click fade rather than abruptly switching a waveform on. Regenerate to the actual video duration; do not add a long intro or change visual pacing for the bed.

For speech, use `--mix-profile narrated` as a quieter starting point, then mix/duck and carve around the real voice using the audio guidance. A preset does not perform automatic voice ducking. If there is meaningful media audio, preserve it and balance against it even when there is no voiceover.

For every export, check the summed mix and encoded AAC/MP3 for clipping/true-peak overshoot, not just individual assets. Reduce the mix if necessary; do not blindly keep boosting. Listen at normal playback volume when possible and state when subjective audition was unavailable. Sharing details are in [portability](portability.md).


## Final mix audit

Use the actual result-state timestamp for success, not the start of a cue that still displays a preceding loading screen. Use separate press/release audio for a sustained drag. Review secondary actions inside a cue, such as adding a file before focusing a search field. Skip transition whooshes when the UI simply replaces a view without motion.

Audit the **exported** soundtrack against the generated mix, compensating only for documented codec delay. Compare event onsets within one output frame; confirm keyboard events coincide with inserted characters. Match video and audio duration, inspect integrated loudness and true peak, and confirm the final watch/download page points to that exact file. Retain editable source and update its audio so a future render reproduces the delivered mix. No-voiceover mixes may need a modest final gain after combining the layers; measure and audition, leaving headroom rather than stacking unexplained gains. Record any final gain separately from asset gains.
