# Optional narration: capture, rough cut, speech, final sync

Use when narration is requested, already authorized, or being considered through the once-only optional setup offer. If voice is unresolved and helpful, offer no voice, installed local speech, a user-provided recording or an explicitly authorized AI provider; suggest a suitable role in the same exchange rather than starting a second questionnaire. Preserve existing decisions and continue independent visual work without waiting. Inspect the app and code, then capture and arrange the selected real screen sequence before curating narration. Write speech around the actions and outcomes actually displayed in that visual rough cut; do not narrate a guessed capability or call an unchanged feature new. Keep a compact mapping from each spoken claim to its source and intended shot. Resolve important missing evidence before recording that claim.

## Choose the speaking role

Infer the role from the request and preserve an existing choice. If unchosen and it would materially help, make one optional intake offer distinguishing:
- **Instructional:** tells the viewer which real control to use and what happens next.
- **Explanatory:** explains the meaning of the visible state or result in plain language.
- **Showcase:** briefly connects the demonstrated change to its user benefit without claiming unseen actions.

A film may combine roles deliberately. Do not reopen the question for every scene or add narration when the user selected no voice.

## Choose the voice source deliberately

Honor the user's existing choice; do not restart voice discovery or sign-in when an installed system voice was requested.

| Choice | Requirements and limits |
| --- | --- |
| No voice | Titles, visible actions and optional effects can carry the film. Do not generate narration merely because the helper exists. |
| User-provided recording | Preserve the authorized voice; measure and edit its actual audio. |
| Installed OS speech | Credential-free local synthesis using a voice already on the machine. This skill implements macOS `/usr/bin/say` only; it does not install voices or models. Expect robotic phrasing and limited pronunciation/prosody control. |
| Local AI speech model | Separate explicit choice; inspect available runtime and model first. A request for built-in speech does not authorize downloading a model or dependencies. |
| Cloud speech provider | Separate explicit choice with the provider's actual account/credentials and applicable limits. A free allowance is not the same as credential-free local speech. Never invent an unofficial keyless endpoint or silently substitute a cloud service. |

If an installed voice cannot render, report the failure and preserve independent visual work. Do not automatically download another voice or invoke an external fallback. [Apple documents voice installation separately](https://support.apple.com/en-kw/guide/mac-help/mchlp2290/mac). For an explicitly selected cloud option, verify current requirements; for example [Azure Speech pricing](https://azure.microsoft.com/en-ca/pricing/details/speech/) describes limited allowances while its [REST documentation](https://learn.microsoft.com/azure/ai-services/speech-service/rest-text-to-speech) describes authentication. Do not promise a quota or free access forever.

## Capture-led narration and final synchronization

Capture the relevant real screens/actions and arrange a visual rough cut first. Identify the input, response and result that are actually visible. Curate the speech or written transcript from that sequence rather than drafting an aspirational script and manufacturing UI to match it. For supplied recordings, use their existing sequence; for an explicitly requested concept, use the reviewed proposed sequence and retain its status.

Give each useful action/topic a concise spoken unit with its source and rough-cut shot reference. Perform a clean read-aloud pass in a conversational product-walkthrough voice: use contractions, short linked sentences, familiar words, practical examples and natural transitions. Connect the action to its useful result. Avoid a page-by-page manual recital, internal production jargon, superlatives and redundant readings of every label. Distinguish a shown state from a performed action: “The saved view shows…” is appropriate when only that state is captured, while “Tap Save…” requires the activation and response. Adjust pronunciation in the spoken text without altering product spelling on screen.

Generate or obtain the selected voice only after that visual/script pass. Measure each line's actual duration; words-per-minute estimates remain planning aids. Refine final shot timing and speech placement around those measurements while preserving action order and purposeful reading time. If a line is longer than its information warrants, shorten it rather than freezing a screen until speech ends. Re-generate and re-measure changed lines. Keep titles, actions and narration synchronized in the final encoded review; a rough cut is not an inflexible timing lock.

Mix effects and the selected bed around speech, preserve intelligibility and check the exported result. State any subjective listening limitation. No universal scene length or mandatory number of narration passes is implied.

Titles and page labels can provide the on-screen guidance when the user prefers no extra captions. Omit the additional caption strip in that case; keep necessary version/concept disclosures and visible input/result cues. A narration request does not automatically request burned-in subtitles. Neither voice nor a title substitutes for a missing demonstrated action.

## macOS installed-voice helper

`scripts/system_voice.py` requires Python 3, macOS `/usr/bin/say`, and existing `ffmpeg`/`ffprobe`. It uses safe subprocess argument lists and plain-text files, checks the installed voice list, makes no installation/download/API call and has no external fallback. Linux and Windows synthesis are not implemented by this helper.

```json
[
  {"id": "open", "text": "Open the project to review its entries.", "evidence": ["source path/symbol or observed state"]},
  {"id": "result", "text": "The updated amount appears in the total.", "evidence": ["verified result shot"]}
]
```

Use only claims supported by the target app; these sentences illustrate the input schema.

```sh
python3 <skill-dir>/scripts/system_voice.py --list-voices
python3 <skill-dir>/scripts/system_voice.py --input narration.json --out audio/voice-v1 --voice Samantha --rate 165 --normalize
```

Choose a voice from the installed list. The default `Samantha` alias resolves to an installed full name when available; if absent, generation stops. Output directories must be new or empty to preserve prior work. The helper writes one 48 kHz mono PCM WAV per line and `manifest.json` with exact text, voice, rate, evidence, measured duration and suggested cumulative starts/ends. `--gap` changes suggested spacing, not the WAV content. Adapt those starts to the storyboard instead of assuming every line must play immediately after the previous one.

`--normalize` is optional peak normalization toward −3 dBFS, capped at +6 dB gain; `--gain-db` applies an additional attenuation trim from −24 to 0 dB; it is not a guarantee of equal perceived loudness. The manifest records applied gain. Keep the voice files separate from effects and ambience for editable mixing. Inspect pronunciation, line endings, pauses and harshness; a successful WAV or level measurement proves neither natural delivery nor a good final mix.


## Reusable clean voice settings

Save an established voice/rate/mix choice as a small JSON preset and reuse it across projects when the user wants consistency. It is a starting point: brand names, language, scene density and the final mix still need checking. These are synthesis and mixing settings, not model training or fine-tuning, and cannot guarantee natural delivery from an installed robotic voice.

```json
{
  "voice": "Samantha",
  "rate": 165,
  "gap": 0.25,
  "normalize": true,
  "gain_db": -1.0,
  "pronunciation_notes": {"ProductName": "Record the preferred spoken pronunciation after audition."}
}
```

```sh
python3 <skill-dir>/scripts/system_voice.py --input narration.json --out audio/voice-v2 --preset voice-preset.json
```

Explicit CLI settings override the preset, including `--no-normalize`. Pronunciation notes are preserved in the manifest as curation notes; the helper does not silently replace words. Edit and review the actual spoken line when applying a note. Preserve source spelling separately where needed. The settings above illustrate the format, not a universal required voice or pace.
