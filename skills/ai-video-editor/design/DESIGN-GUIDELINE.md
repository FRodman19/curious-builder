# Design Guideline: Neutral Starter

This is a **brand-agnostic** starter. It carries the craft rules that make motion graphics read cleanly,
using **tokens** instead of a fixed identity. Drop in your own colors and fonts once, here, and every beat
inherits them. The craft rules (placement, one accent per composition, animation-is-the-explanation,
caption style, the identity gate) are worth keeping as-is regardless of brand.

> For best output, define your brand below before building. Bland tokens = bland video.

---

## Brand tokens: fill these in

```css
:root {
  /* Surfaces */
  --canvas:  #FAFAF8;   /* main background (or a dark value if you run dark) */
  --surface: #F2F1EC;   /* card / panel background */
  --border:  #E2E1DD;   /* borders, dividers */

  /* Text */
  --ink:     #0C0D0C;   /* primary text on light surfaces */
  --head:    #E8E8E5;   /* primary text on dark surfaces (never pure #FFFFFF) */
  --body:    #52544F;   /* secondary / body text */
  --muted:   #8A8C87;   /* inactive karaoke, supporting text */

  /* Accent, ONE highlight color, used sparingly */
  --accent:  #EF6D28;   /* swap for your brand accent */

  /* Semantic (leave as-is unless your brand overrides) */
  --succ: #4CAF50;  --err: #EF5350;  --warn: #F59E0B;

  /* Fonts */
  --display: 'Playfair Display', Georgia, serif;  /* titles / key claims, an editorial display face */
  --body-font: 'Inter', system-ui, sans-serif;    /* body / captions / karaoke, a clean sans */
}
```

- **`--accent`** is your single highlight. One anchor per composition, never decorative, never two accent
  moments fighting for the eye.
- **`--display`** is for anything the viewer must remember (titles, key claims). Pick a face with
  personality, an editorial serif reads more premium than a system sans.
- **`--body-font`** is for anything the viewer must read fast (labels, captions, karaoke). Pick a clean,
  high-legibility sans.
- These example values are placeholders: replace them with your brand.

---

## Type scale (motion graphics, 1080p)

| Role              | Font          | Weight | Size     | Color        |
|-------------------|---------------|--------|----------|--------------|
| Eyebrow label     | `--body-font` | 500    | 18-22px  | `--accent`   |
| Main title        | `--display`   | 700    | 56-80px  | `--ink`/`--head` |
| Sub-title         | `--display`   | 400    | 32-44px  | `--ink`/`--head` |
| Body / caption    | `--body-font` | 400    | 20-28px  | `--body`     |
| Karaoke active    | `--body-font` | 700    | 28-36px  | `--accent`   |
| Karaoke inactive  | `--body-font` | 400    | 28-36px  | `--muted`    |

Rules: display font for memory, body font for speed. Always fit caption/karaoke text to its container so it
can't overflow. No hero text smaller than ~48px.

---

## Motion defaults

```js
gsap.defaults({ ease: 'expo.out' });        // entrances: fast settle, premium not snappy
gsap.to(el, { ease: 'power2.in', duration: 0.4 });  // exits: final scene only
```

| Motion type   | Duration |
|---------------|----------|
| Title reveal  | 0.6-0.9s |
| Eyebrow fade  | 0.4s     |
| Karaoke word  | 0.15s    |
| Card wipe     | 0.5s     |
| PiP entrance  | 0.7s     |

**Aesthetic principle, animation IS the explanation.** The moving content inside a card carries the
meaning; the card is a quiet frame around it. Lean toward mechanics that *demonstrate* the concept (a task
tree building, a list checking off, a cursor clicking, an idea bubble popping) rather than static text +
icon "slideshow" cards. Motion should feel weighted, not floaty.

---

## Captions

White text + a dark backdrop pill (`rgba(12,13,12,0.42)`) + a heavy text-shadow. **Not** white pills with
dark text. This reads on any footage, light or dark.

---

## Visual Identity Gate: checklist (run before approving any beat)

- [ ] Background is `var(--canvas)`, a deliberate brand surface, not an accidental one.
- [ ] Text uses `--ink` on light / `--head` on dark, never pure white `#FFFFFF` (feels cheap).
- [ ] `--accent` used **at most once** per composition, as the focal anchor.
- [ ] Title font is your `--display` face, not a system-serif fallback (a common silent failure, check
      the rendered frame).
- [ ] Body / captions use `--body-font`.
- [ ] Caption style is white text + dark backdrop pill + heavy shadow.
- [ ] For talking-head: graphics sit ABOVE the face (top ~50%), never on the face.
- [ ] No `backdrop-filter: blur()` over a face, use a top-down canvas gradient instead.
- [ ] When two cards co-exist, only the one tied to the current spoken word animates; the other holds at
      final state.
- [ ] Animation mechanics tie to the spoken concept (not text-heavy slideshow cards).
- [ ] No `repeat: -1`; all timelines synchronous; entrances use `gsap.from()`.
- [ ] Dynamic text fitted to its container.
- [ ] **Frame-check pass run**, extracted JPGs at key timestamps, read each, fixed issues before approval.

---

## What NOT to do

1. **No pure white** (`#FFFFFF`), use `--canvas` for backgrounds and `--head` on dark surfaces.
2. **No gradient text**: keep text solid; gradients only for subtle background glows/washes.
3. **No system sans for titles**: a title in a fallback font undermines the whole identity.
4. **No second accent**: one highlight color as the anchor; everything else is neutral.
5. **No busy layouts**: max ~3 typographic elements per beat.
6. **No card-heavy slideshow beats**: if a card is just static text + icon, redesign it with an active
   animation that demonstrates the concept.
7. **No blur on faces**: ever.
8. **No overlays on the face or shoulders**: graphics live in the top ~50%.
9. **No simultaneous card animations** when two cards share the screen.
10. **No "claim done"** until the frame-check pass has run on the render.
