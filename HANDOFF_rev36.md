# HANDOFF rev 36

**THE FIRST GEOMETRY CHANGE SINCE REV 30.** The over-rider bar's hoop ends now
meet the bumper. `t1_detail.py` and `verify.py` are the only build files
touched.

## 1. What rev 36 did

1. **Found that the inherited brief had lost the owner's own defect report.**
   *"the upper bar appears to also connect with the main bumper on either end.
   In the current version, there is no connection made."* is in **no** carrier
   that crosses contexts — not `SPEC.md`, not `HANDOFF_rev35.md`, not anywhere
   in `NEXT_CONTEXT_PROMPT_rev36.md`. All four checked by grep. Only memory had
   it. **The carrier that failed is the one he pastes in.**
2. **Measured the defect by ray-cast and overturned all three of rev 35's
   figures about it.** One gap, not two; **23.59 mm, not 8.1**; the "52.4 mm
   fore-aft gap" is **0.51 mm** and coplanar by construction. Rev 35 read the
   CONSTANTS, not the FUNCTION THAT CONSUMES THEM.
3. **Found two further defects in the old end that were not the gap:** a
   **tangent discontinuity** (61.2° kink off the bar, then FLATTENING to 43.4°),
   and the fact that the 0.62 sweep cap was **a numerical workaround that had
   become the shape.**
4. **Measured the real end shape scale-free** off `ref_workshop.jpg`: bend
   radius **1.35 tube diameters**, descent **69°**, both published WITH THE
   DIRECTION OF THEIR BOUND.
5. **Built it**, with `BAR_LEG_LEN` and `BAR_HALF_Y` **DERIVED**, the tip
   **FROZEN**, and `BAR_END_DROP`/`BAR_END_BACK` **RETIRED**. 23.59 → **0.02 mm**.
6. **Guarded it two-sided in `verify.py`** as SPEC 10.90, and **falsified it in
   four arms**, one of which caught the guard's own narration describing the
   opposite defect.
7. **The owner renamed a column the project has consumed since rev 32**, and
   that dissolved §10.83's five-revision question — **there are two posts and
   neither is on the centreline.**
8. **Enumerated a third estimator's preconditions and abandoned it BEFORE
   building it** — same missing feature that killed §10.89's route.

## 2. Files

| file | what |
|---|---|
| `t1_detail.py` | **BUILD FILE.** `overrider_bar()` rewritten; two constants retired, two derived, one frozen; `_blade_top_at()` added |
| `verify.py` | **BUILD FILE.** SPEC 10.90 guard, two-sided, ray-cast |
| `SPEC.md` | NEW §10.90, nine parts |
| `probe_rev36_barend.py` | the ray-cast measurement. 8 controls |
| `probe_rev36_posts.py` | the two-post test. 5 controls, incl. a falsification arm and a priced null |
| `mark_rev36_ends.py` | the question figure. 7 controls, REFUSES TO WRITE |
| `render_rev36_bumper.py` | read-only render driver; adds a view to a LOCAL COPY of `views()` and refuses if the name already exists |
| `rev36_ends.png`, `rev36_ends_plain.png`, `rev36_barend_ab.png` | the figures |

## 3. Guards, on the fresh tree

**0 fail / 0 warn at BOTH levels.** 127 objects, 186 meshes, 42 materials,
0 non-manifold, roof 1.9835/1.9833, rake 17.75, arches 0.3722/0.3732,
68564v/252749v, off flank 804.9, bay widths 0.516/0.515/0.516, `CARGO_GAP` 154.
**Every inherited figure is identical to rev 30–35's**, including the over-rider
row at **97.51 mm / 24.97 mm** — `BAR_Z` and `BAR_DIA` were deliberately not
touched.

New row: `over-rider hoop ends (SPEC 10.90, rev 36): land on bumper_f with
0.02 / 0.02 mm residual (tol 1.0, TWO-SIDED)`.

## 4. Things you must not silently undo

- **`BLADE_TOP_Z` IS NOT THE LANDING DATUM.** It is the blade's CROWN and the
  channel top slopes 2.30 mm away from it at the tube's station. Landing on it
  is a 2.32 mm gap and the guard will catch you. `BLADE_TOP_Z` itself must stay
  put — it anchors `BAR_Z` and the over-rider row.
- **`BAR_TIP_Y` IS FROZEN** and written as the old formula so the equality is
  provable. Do not replace it with a literal. `BAR_HALF_Y` follows from it and
  is DERIVED — do not turn it back into a free constant.
- **`BEND_R_RATIO` = 1.35 is a LOWER bound and `BEND_THETA` = 69° an UPPER
  bound.** They are image-space. Do not quote them as 3-D readings.
- **The two-post result is SUGGESTIVE, NOT ESTABLISHED** — 41:1 against the
  null, and it crosses the band boundary between the two available readings of
  the near post (0.73 band at 362.5, **1.23 at 365.5**). Do not promote it.
- **`u 205–208` IS A POST, NOT THE BAR'S FAR END.** Do not re-consume it under
  the old label. Rev 33's and rev 34's answers stand as readings; the label was
  wrong.
- **DO NOT OPEN A THIRD ESTIMATOR FOR THE SPAN.** §10.90.7 enumerated its
  preconditions and it fails on the same missing feature as §10.89's.
- **`probe_clean_top.py` and `probe_dust_anchor.py` are STILL deliberately
  failing.** rev 36 did not reach them either. **Four revisions now.**
- Everything `HANDOFF_rev35.md` §4 and its ancestors protect.

## 5. What rev 36 did NOT do

- **Work-list item 1 as the brief stated it** (rewrite the two degenerate
  probes) — not reached. The brief's item 1 was displaced by the owner's own
  geometry report, which the brief had lost.
- Items 2–5 — not reached.
- **No hero was shot.** `rev30_hero34f.png` is no longer a render of the current
  build: **the geometry moved.** It is superseded, not merely stale. A hero is
  now genuinely owed for the first time since rev 30.
