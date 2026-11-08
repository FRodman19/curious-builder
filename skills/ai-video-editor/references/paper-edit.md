# Paper Edit: Reference

The editorial blueprint step. Before touching the timeline, write the **ideal final version of the video
as text**, then trim the raw footage down to that target. The point is never "cut for cutting's sake",
it's to build the best version first and remove everything that isn't it.

Pipeline position: **after Stage 2 (Transcribe), before Stage 3 (Trim).**
Inputs: the word-level transcript (`takes_packed.md` / JSON), `script.md` if one exists, and frame reads
for delivery quality.

---

## 1. Detect mode: scripted vs unscripted

- **Scripted** (`script.md` exists): the script is the *intended* arc. Compare the transcript against it.
  Speakers often deviate on camera, treat off-script lines that land **better** than the script as wins,
  not errors.
- **Unscripted** (no script): shot live with no pre-writing. Read the transcript end-to-end and **derive
  the actual point/arc first.** The paper edit defines the structure from scratch.

Rule of thumb: no script attached -> assume unscripted.

---

## 2. Draft the paper edit (the blueprint)

Write the best version of what was said:
- strongest hook line first,
- cleanest delivery of each point,
- in the best order for the story,
- pulling the **best mix across all takes** (a topic is often shot 2-3 times).

Output a marked target transcript: each kept line tagged with the take it comes from and its source
timestamp. This feeds the EDL in Stage 3.

---

## 3. Selection rubric: which take/mix wins

Verify with **frames, not the transcript alone.** Extract JPGs across the candidate takes, read them, and
judge in this priority order:

1. **Energy**: alive, engaged, present delivery.
2. **Fluency**: no stumbles, restarts, or broken reads.
3. **Relevance**: says the thing that actually matters. Off-script-but-better beats on-script-but-flat.
4. **Continuity / framing**: eyeline, position, lighting consistent enough to splice cleanly.

Promote or demote lines based on what the frames show. Keep frame reads minimal, sample key moments,
don't read every second.

---

## 4. Three cut strategies: pick one per footage

- **Single best take**: one section nails everything -> cut just that section.
- **Best-of-each**: splice the strongest cut from each section together (watch continuity at splices).
- **Whole + light trim**: keep one take end-to-end, remove only fillers, restarts, and dead air.

Recommend ONE with reasoning tied to the transcript + frames, then **stop for approval** before cutting
(matches Plan-Mode Checkpoint 1).

---

## 5. Format-aware cutting

The cut style must match the format, decided here, applied in Stage 3:

- **Short-form (9:16)**: hook landing in the first 1-2s, aggressive jump cuts, kill ALL dead air and
  breaths, fastest viable pace.
- **Long-form (16:9)**: keep breathing room, retain setups and context, smooth pacing. Don't over-cut.
- **Tutorial**: preserve step boundaries; allow short pauses at transitions so the viewer can follow.

---

## 6. Self-review gate: watch, score, then present

Never present work unverified. After producing any output the user will look at (the cut, a render,
anything), **watch it end-to-end first**, score it **/10**, and only present if it scores **>= 8**. Below 8
is poor, diagnose what failed, fix it, re-watch, re-score. Loop until it clears the bar, then present.

Success criteria (the watch-through checklist):
1. **Audio clarity**: voice is clear; no words clipped at splices; 30ms fades present, no pops.
2. **Makes sense**: flows as one coherent piece; no orphaned references, no jarring logic jumps.
3. **Clean cuts**: every cut on a word boundary; no half-words, no mid-breath stutters.
4. **Pacing fits format**: short = tight, long = breathing room (section 5).
5. **Continuity**: no distracting jumps in framing/position at splices.
6. **Text (later stages)**: once captions/beats exist, text fully appears before it's needed and is
   never cut off mid-word.

This gate is not optional and not fully automatic: you verify your own work, and only good work reaches
the user. The user still approves each stage before the next begins, the gate is what earns that hand-off.

---

## What this step does NOT do

No motion graphics, beats, captions, or visual direction. Those come after the cut is approved, when the
user gives visual direction (Stage 4 onward).
