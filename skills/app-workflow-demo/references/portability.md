# Sharing and a new-computer preflight

Share the entire `app-workflow-demo` folder, not just SKILL.md. It contains instructions, references, scripts and actual MP3 assets in `assets/ui-audio/`. Audio assets are synthesized presentation sounds; they do not depend on the original Simplify Edits project, localhost server, API key or generator cache.

Install the complete folder in the receiving assistant's supported skills directory. Refresh/restart skill discovery if needed, then invoke `app-workflow-demo` using that client's skill picker or supported skill syntax. Slash commands vary by client; a slash command is not itself an installer.

## What works without regeneration

The bundled MP3s can be auditioned and reused directly, including all 21 effects and two ambient options. Open `assets/ui-audio/index.html` locally. Generating WAV masters is optional. The 24-second ambient previews are finite tracks, not claimed seamless loops: for longer demos regenerate to duration, or crossfade repeated copies at quiet boundaries and audition the seams. Do not hard-loop MP3s with codec padding.

## What needs local tools

- Regenerate or customize sounds: Python 3 and NumPy
- Write MP3/AAC, mix existing media, inspect/encode the final video: FFmpeg/ffprobe
- Build this skill's default HTML animation: compatible HyperFrames CLI/runtime and a supported browser, plus its core/render guidance
- Render contact sheets: the helper's documented image dependencies

Check installed tools first. Do not install packages, contact an API, or change environment settings just because the skill was opened. Follow the user's setup authorization. If dependencies are missing, reuse bundled audio where possible and report the exact blocker for generation/rendering. Do not claim that every fresh computer can render a complete demo with no setup.

The referenced video-system files and HyperFrames/media skills are companion guidance, not embedded runtime packages. On a new machine, locate their installed equivalents. Missing optional audio provider tooling does not block the bundled/local audio path. If the selected renderer or its required guidance is missing, complete evidence gathering and the contact-sheet design, then identify what is needed to animate it. No paid audio provider or API key is required by this library.

## Project inputs remain separate

The skill is reusable across apps; it does not bundle the original app's code, fonts, video footage or design chapters. A new project must provide its own source UI/references and feature intent. Discover its design system and behavior, choose demo scope and camera style, review a contact sheet, then animate it faithfully. Do not reuse Simplify Edits UI merely because the sound assets came from that case study.
