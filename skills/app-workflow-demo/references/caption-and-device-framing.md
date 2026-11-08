# Page headings, optional captions and presentation shells

The app's design system is the default authority: typography, ink/surface colors, accent, radii and motion. Personal creator branding may govern the surrounding presentation only when requested. Never recolor the product UI to match a creator theme. If no brand is available, derive an evidence-backed neutral presentation and identify the assumption.

## Consumer-facing hierarchy

Use one clear centered page/action heading on the brand backdrop, outside the physical device/window. Keep it readable and reserve its space before fitting the whole phone. Do not stack a second caption strip when the user chose titles only. Headings identify the page or useful action, not the production method.

Keep slide/chapter counters and internal notes such as “sample”, “fictional”, “source-based”, “keyboard omitted” or “local narration” out of the consumer film. Store fixture, source, capture, voice and reconstruction provenance in the brief and review sidecars. Retain a material concept/before-after/version disclosure when needed to avoid misleading viewers; do not claim real results or live operation from a fixture. Review-sheet numbering stays outside the artwork and is not burned into the video.

## Caption placement

Honor the user’s choice of titles/page labels without an extra caption strip. When action captions are selected, use a short centered pill in a reserved area outside the app or device. Desktop defaults to below its window. For phones, choose above or below the entire physical frame, not on the screen, bezel, notch, status area, home indicator or device body. The caption must be a sibling of the device/window, not a descendant of its clipped viewport. Keep it outside camera/zoom transforms.

Use quiet solid contrast, restrained edge/shadow, the app's typeface and one plain action phrase. No decorative leading dot, generic badge icon, fake status LED, extra counter or bouncing marker. Native window controls, hardware cutouts and genuine in-app status indicators are separate and must not be removed merely because they are circular.

Size captions for their final viewing width. On a 1080px portrait export, 48–54px is a useful starting point for roughly 16–18px text when displayed at 360px. Check the actual result, not the source font size. Avoid shrinking a long caption: shorten it faithfully or wrap to two lines in a softly rounded capsule. Leave room for platform overlays and crop-safe margins. Use a restrained transition on action change without holding up the interaction.

The page/action heading provides the main guidance. Any necessary concept/version disclosure stays unobtrusive; do not add a counter or production footer. A caption must state the action actually occurring, not an unsupported success claim. On grids, captions belong to their own cards and must not obscure content.

## Frames

Start from `assets/presentation-shells/frames.css`, the reusable `android.html` fragment, and `shells.html` catalog for shell markup; set brand variables from the target app. These assets are presentation scaffolds only. Do not use their placeholder as a fabricated screen of a real product.

- Desktop/macOS: preserve the actual titlebar when present. If the supplied content is app-only, an outer Mac-style window may clarify the setting; record this as presentation chrome in the brief and do not add a second set of traffic lights to an existing Mac titlebar. Traffic-light controls are functional platform conventions, not decorative caption dots
- iPhone: illustrative rounded shell, top camera region and bottom gesture safe area; exact device details require a supplied/selected device reference
- Android: use distinct geometry and a centered, proportionate visible punch-hole; do not just relabel an iPhone or shrink its camera into a barely visible dot. The reusable shell includes a neutral 9:41 clock, signal, Wi-Fi and battery drawn as inline SVG. The neutral camera starts near 4.2% of screen width; tune `--android-camera-size` to the evidenced hardware rather than treating that size as universal. Reserve the status inset above app-only captures. Set `data-system-chrome="included"` when the capture already contains a status bar, and `data-camera-included="true"` if it also includes a punch-hole, so neither is duplicated. Use a neutral illustrative model unless an exact device is evidenced. Never replace icons with Unicode glyphs
- Mobile app content: use real mobile source screens. Never squash desktop UI into a phone or invent a mobile edition. For a frame-only draft, explicitly label placeholder UI and keep it outside the production app/demo deliverables

Use the target-brand [aurora and depth recipe](app-fidelity-and-presentation.md#brand-aurora-depth-and-canvas-occupancy) when appropriate to the requested presentation. Keep device/window depth subtle and enlarge the context within the usable canvas before adding decorative surrounding elements.

Device and screen clips are distinct: only the screen content is clipped to inner corners. Whole-device mode keeps the entire shell inside the safe canvas throughout; optional detail shots transition to frameless content. Reserve the device's full bounds before placing the heading or any caption. On portrait exports, grow the phone enough that the active UI remains legible; do not waste half the canvas on decorative backdrop. Test both the full export and a phone-width preview.

## Matched components without a frame

A phone can establish context without occupying every shot. For before/after component details, read [release-comparison.md](release-comparison.md#matched-component-shots) and adapt `assets/presentation-shells/comparison.html` and `comparison.css`. These provide stacked, side-by-side and registered specimen layouts; they do not supply product UI or timing. Preserve comparable component scale and source geometry.

## Progress is optional

Default: no horizontal progress bar below the app and no ornamental dot. Keep native video-player controls available on a watch/download page; the rule is about artwork burned into a demonstration, not suppressing useful playback controls.

If the user wants playback progress, use a thin outline just outside the window/device silhouette, in the target app's accent. A rounded-rectangle outline follows the shell; do not draw a circular loading spinner over the UI. Aim for approximately a one-pixel hairline at the intended viewing size, with no glow, dot or moving knob. Keep it optional/off by default. It must not look like the app is loading when it is only tracking the video's position.

Tie it deterministically to composition time divided by duration, resetting at the loop seam. An SVG rounded rectangle with normalized `pathLength="1"`, dash length equal to playback fraction, no fill and a non-intercepting overlay is sufficient. Offset it beyond the bezel; never cover the caption or product controls. Use a screen-reader-hidden presentation layer, and ensure seek/jump produces the right progress immediately.

## Review

Contact sheet includes desktop, iPhone or Android only as requested, with actual frame sizes and caption location visible. Self-critique first: check caption readability at phone width, device/caption non-overlap, no clipped text, enough device area, correct platform chrome, brand consistency, and no duplicated controls. Presentation changes can be previewed as disposable drafts before rerendering the full video. Frame approval does not approve an invented mobile workflow.
