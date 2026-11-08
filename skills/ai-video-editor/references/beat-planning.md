# Beat Planning Reference

How to turn word-level transcript timestamps into a precise beat plan, plus the renderer composition
contract each beat HTML must satisfy.

Colors and fonts below are written as **brand tokens** (`--canvas`, `--ink`, `--accent`, `--display`,
`--body`), define them once in `design/DESIGN-GUIDELINE.md` and every beat inherits them.

---

## What Is a Beat?

A beat is a moment where a motion-graphic overlay appears. It's anchored to a specific word in the
transcript, the **anchor word**, and timed to feel like part of the speaking momentum, not slapped on
top. Good beats feel invisible. Bad beats feel like PowerPoint slides.

---

## Anchor Word Selection

**1. Payoff words**: the word that delivers the point being built toward ("works", "done", "solved",
"faster", "free", "crashed"). Place a key-claim card here. Timing: overlay starts 0.5-0.8s **before** the
anchor so it's on screen as the word lands.

**2. Topic-shift words**: the word that opens a new section ("so", "now", "but here's", "let me show
you"). Use a section intro / eyebrow beat. Timing: overlay starts **at** the anchor word (the shift is the
cue).

**3. Emphasis moments**: a stressed word the viewer should remember (louder, slower, repeated, preceded by
a rhetorical pause; the transcript JSON shows longer gaps here). Use a karaoke beat so the active-word
highlight draws attention.

### Selecting good anchors: checklist
- [ ] Does the anchor word carry meaning on its own? (avoid "and", "the", "just")
- [ ] Is it at the position where the topic actually peaks?
- [ ] Will a visual reinforcement help the viewer here?
- [ ] Is there >= 3s of clear audio after it before the next shift?
- [ ] Are consecutive beats spaced enough to avoid overcrowding?

---

## Timing Formula

```
overlay_start = anchor_word.start - reveal_duration
```
The entrance animation should **complete** exactly as the anchor word is spoken.

| Beat type          | Reveal | overlay_start                  |
|--------------------|--------|--------------------------------|
| Key-claim title    | 0.7s   | `anchor.start - 0.7`           |
| Section intro      | 0.5s   | `anchor.start` (no pre-reveal) |
| Karaoke activation | 0.15s  | `anchor.start` (sync to word)  |
| PiP facecam        | 0.8s   | `anchor.start - 0.8`           |
| Full-bleed card    | 0.6s   | `anchor.start - 0.6`           |

**Overlay duration:** hold until the current topic ends (next topic-shift word), or the next beat starts,
or a maximum of ~8s, whichever comes first. Minimum ~2.5s (the viewer needs time to read).

---

## The Renderer Composition Contract

Each beat is a self-contained HTML file with an embedded GSAP timeline that the renderer drives frame by
frame. The contract:

- Register the timeline **synchronously** on `window.__timelines` as an object: `{ main: tl }`.
- No `async/await` inside timeline setup; no `repeat: -1`; deterministic only (no `Math.random()` /
  `Date.now()`).
- Use `gsap.from()` for entrances; `gsap.to()` for exits only on the final scene.
- The karaoke / subtitle element is the **last child** in the DOM (the renderer draws in DOM order).
- Fit dynamic text to its container so it never overflows.

```html
<div id="stage">
  <!-- content layers here -->
  <div class="karaoke"><!-- last child --></div>
</div>
<script>
  const tl = gsap.timeline();
  tl.from('.eyebrow', { opacity:0, y:8,  duration:0.4, ease:'expo.out' })
    .from('.title',   { opacity:0, y:24, duration:0.7, ease:'expo.out' }, '-=0.2')
    .from('.body',    { opacity:0, y:12, duration:0.5, ease:'expo.out' }, '-=0.3');
  window.__timelines = { main: tl };   // synchronous, required
</script>
```

---

## Beat Structure: Layers (DOM order)

```
1. Background layer, var(--canvas) or a subtle texture
2. Content layer, eyebrow + title + body (stacked)
3. Accent layer, decorative line / glow / shape (optional)
4. Karaoke/subtitle layer, ALWAYS the last child in the DOM
```

Karaoke word timing:
```js
words.forEach(w => {
  const el = document.createElement('span');
  el.textContent = w.text + ' ';
  el.dataset.start = w.start; el.dataset.end = w.end;
  el.style.color = 'var(--muted)';         // inactive
  karaoke.appendChild(el);
});
function activateWord(t) {
  document.querySelectorAll('.karaoke span').forEach(s => {
    const on = t >= +s.dataset.start && t < +s.dataset.end;
    s.style.color = on ? 'var(--accent)' : 'var(--muted)';
    s.style.transform = on ? 'scale(1.05)' : 'scale(1)';
  });
}
```

---

## Placement: Above the Head Rule (mandatory for talking-head)

Motion graphics live in the top ~50% of the frame; the speaker's face/torso stays clean; captions land in
the bottom ~12%.

```
┌─────────────────────────────────────┐  y=0
│  Top-down canvas gradient            │
│  (var(--canvas) 0.96 -> 0)           │
│  [CARD A]       [CARD B]             │  cards, animated internal content
├─────────────────────────────────────┤  gradient fades
│        speaker's face + torso        │  no overlay, no blur
├─────────────────────────────────────┤
│  Caption pill (bottom ~12%)          │
└─────────────────────────────────────┘
```
- **Never** put `backdrop-filter: blur()` over the face, use a top-down canvas gradient for card contrast.
- Bottom-align internal card elements (`margin-top: auto`) so cards never have empty space.

---

## Sequential Animation Rule (when two cards share the screen)

Only ONE card animates at a time, the one tied to what's currently being said. The other **holds at its
final state** (both stay visible; only the animation state changes). Anchor entrance/exit/state-shifts to
word-level timestamps (±200ms, tighter is better). Simultaneous animation across both cards scatters
attention; sequential animation lets the eye follow the words.

---

## PiP Beat (Outro / Facecam Reveal)

Use when the speaker turns to address the camera directly.
```html
<div class="pip" style="position:absolute; bottom:80px; right:80px;
  width:320px; height:568px; border-radius:20px; overflow:hidden;
  box-shadow:0 24px 64px rgba(0,0,0,0.6); border:1px solid var(--border);">
  <!-- vertical crop of facecam -->
</div>
```
```js
gsap.from('.pip', { x:400, opacity:0, duration:0.8, ease:'expo.out' });
```

---

## Beat Count Guidelines

| Video length | Beats |
|-------------|-------|
| < 2 min     | 1-2   |
| 2-5 min     | 2-3   |
| 5-10 min    | 3-5   |
| 10-20 min   | 5-7   |
| > 20 min    | 7-10  |

Less is more. Every beat must earn its place, 3 great beats beat 8 mediocre ones.

> Want continuous, story-matched **illustrated** B-roll instead of card beats, visuals that cover a whole
> section, drawn from a library and recolored to your brand? That's the B-roll Engine (see the
> B-ROLL-ENGINE teaser in this bundle).
