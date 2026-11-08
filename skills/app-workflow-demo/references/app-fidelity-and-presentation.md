# Target app fidelity and presentation

Use this reference for any app, platform or publishing format. The output is designed product content grounded in the app, not necessarily a literal screen recording.

## Inputs and authority

Start from the user’s intent and available evidence: a local codebase, running app, component library, screenshots, recorded interaction, approved designs or a reference app. Infer the specific task and takeaway. Inspect both appearance and behavior. A screenshot cannot establish unseen behavior, and a beautiful invented animation cannot establish an existing capability.

A supplied screen recording may be used to reconstruct the demonstrated steps, remove dead waiting time and create a better-framed product presentation. Preserve important states and timing dependencies. If the reference is another app, clarify whether the user wants that app demonstrated or wants its presentation approach applied to their own product; do not silently blend identities or imply ownership.

For a new or unbuilt app, use approved components and design assets to propose a coherent workflow. Label the concept. If the key interaction lacks evidence or a product decision, ask a focused question while preparing the supported parts.

## Inspect more than color

Record the visible design language needed for this feature:

- Typography, hierarchy, density, spacing, icon assets, radii and elevation
- Light/dark mode and the actual colors of nested surfaces
- Frosted or liquid glass: opacity, blur, tint, backdrop, highlight and edge treatment
- Platform chrome, navigation, side panels, context menus, dialogs and selection states
- Scroll, parallax, focus, hover and active states where relevant
- Native motion: easing, spring response, timing, transforms and transitions

Reuse working components and styles when practical. Keep fixture data and side effects isolated. Preserve relevant source GSAP, CSS, spring or other motion semantics when making them seekable for the renderer. HyperFrames is the presentation/rendering tool, not a license to restyle the target app. If exact material reproduction is unsupported, disclose the limitation and choose a faithful capture or approved approximation rather than silently replacing it.

## App surface and outer presentation are separate

**macOS app:** use its actual window/titlebar and control positions. A macOS-like desktop backdrop or supplied wallpaper can support the composition. Avoid duplicating traffic-light controls when already present. Do not expose a real personal desktop, notifications or files just to provide atmosphere.

**Other desktop app:** preserve the correct operating-system and app conventions. A desktop window or app-only crop may be more faithful than a Mac mockup.

**Mobile app:** use the target platform, orientation and screen proportions. Keep the entire phone visible in whole-device mode. A restrained frame and appropriate background can make it publishable. Respect safe areas, status/navigation regions, corner clipping and gesture controls. When a capture omits OS chrome, use a neutral Android clock/signal/Wi-Fi/battery bar and a centered proportionate punch-hole from the reusable shell; do not duplicate captured chrome or use Unicode icon substitutes. Do not invent a device-specific notch or hardware branding when the device is unknown; use a neutral phone frame or ask if the exact hardware matters. Demonstrate taps and swipes, not an unexplained desktop mouse cursor.

**Web app:** preserve browser chrome only when it helps establish context. Hide unrelated tabs and personal data. Keep the actual responsive layout at the chosen viewport.

**App-only/detail:** explicitly transition to frameless content when a selected detail needs more room. Use a considered background, margins and a centered heading; do not leave a half-clipped phone around the content.

Presentation backgrounds should suit the target app and audience, including light, dark, softly textured or brand-derived gradients. Do not force a texture, orange glow, glass card or decorative parallax into every project. Real app glass requires a meaningful backdrop to look correct; verify transparency and contrast in the encoded output.

## Brand aurora, depth and canvas occupancy

For a polished guided showcase, build the presentation backdrop from the target app's actual design system: its base surface, primary/accent hues and compatible neutral ink. A softly blurred aurora can add atmosphere while remaining subordinate to the product. Use broad low-contrast color fields and a calm center behind important controls; do not import another app's palette or make every product orange. When no brand tokens exist, derive restrained colors from the supplied UI and record that choice. Respect explicit solid-background or screen-recording requests. If an aurora reduces contrast, misrepresents the app's material, or competes with dense UI, reduce it or use a simpler surface.

Start with `.demo-stage--aurora` in `assets/presentation-shells/frames.css`. Set `--paper`, `--aurora-a`, `--aurora-b` and optionally `--aurora-c` from the target brand; tune `--aurora-opacity` and `--aurora-blur` after rendered inspection. Blur only the decorative layer, not the app, labels or captions. Keep ambient movement optional and deterministic; it must not conceal static or incomplete product behavior.

Use `.presentation-depth` on the outer phone or desktop window for restrained contact/diffuse shadows and edge highlights. This is presentation depth, not a redesign of product cards or evidence that the native app has 3D UI. Preserve actual hardware conventions and avoid unreadable perspective tilt, exaggerated bevels, floating screen fragments or duplicate titlebars. A framed reveal can have depth while the reading/action view remains straight-on. A frameless component pair can use minimal separation shadows without becoming an invented app dialog.

Give the device or window the largest area compatible with its true proportions, caption safe area and visible controls. Remove redundant headings and excess margins before shrinking UI. Derive context size from the available safe rectangle rather than a fixed pixel width; the supplied `--stage-gutter` is a layout starting point. Portrait comparisons can retain both full phones or explicitly transition to larger frameless matched details when that treatment is selected. Do not stretch the phones or sacrifice caption legibility to fill every pixel. Confirm occupancy visually at the final feed width: the app should be the subject, not a small object surrounded by decorative background.

## Aspect ratio and destination

Choose the output dimensions from the destination and viewer task. Landscape often gives a desktop workflow room; portrait can suit a phone app or social post; square or 4:5 can suit a feature card. These are starting points, not universal platform rules. Check current platform specifications when making specific publishing-compatibility claims.

Do not stretch a landscape interface into portrait. Preserve its true viewport and either fit it inside the frame, use deliberate closeups, or create a separate portrait composition with an honest cropped view. Full workflow demos need orienting wide views as well as detail. Captions remain outside the app, readable at the intended viewing size.

For multiple destinations, produce deliberate variants only when requested. Use the same verified state sequence, adapting camera/framing and captions to each format. Do not multiply outputs by every ratio or device automatically.

## Review before animation

The contact sheet should establish app identity, device/platform, outer background, aspect ratio, readable full-window context, useful closeups and caption placement. Inspect first at full resolution, then at the size someone will actually see in a feed. Critique material accuracy, text, motion plans, cropping, device proportions and background contrast before showing it to the user.

## Example intents

- “Show this Rhydle feature for a social post” → inspect Rhydle’s feature and design system, select short or complete mode as needed, then present a destination-sized contact sheet
- “Recreate this app recording as a polished feature demo” → map the recorded states, reuse supported real components or faithful screenshot layers, condense idle time and frame for publication
- “Show how this planned mobile feature could work” → use approved app assets, design the complete proposed interaction, label it a concept and review it in a phone composition
- “Tour this Blender task from setup to export” → preserve the actual Blender version, workspace, object mode, panels and operators; use complete mode when requested and do not replace required operations with visual shortcuts
