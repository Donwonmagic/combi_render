# LEDGER — rev 67

## §1 WHAT REV 67 WAS ASKED FOR, AND WHAT IT DID

The owner ruled at rev 66, asked directly whether rev 67 should do the nose or finish the
emblem: **the nose.** F197 became a RULING, not an inference, and §3 item 1 was his.

**THE NOSE NOW HAS AN INSTRUMENT. IT DID NOT BEFORE.** `probe_rev67_nose.py`,
`t1_shell.NOSE_BULGE`, the `T1_NOSE_BULGE` ablation, and SEVEN verifier rows.

**AND RULE 15's ADVERSARY WAS DISPATCHED THIS TIME** — rev 66's was run in-context and missed
what the owner caught. It came back with thirteen defects. **Five of the load-bearing ones I
re-ran myself and confirmed; they are F208–F212 and they are the most consequential thing in
this revision after the nose.**

---

## §2 THE NOSE — MEASURED FOR THE FIRST TIME (F207)

**WHAT NOTHING IN THIS TREE HAD EVER MEASURED: the nose's PLAN BULGE**, the forward convexity
of the whole face. On the mesh, `x(y=0) − x(|y|=0.70)`:

```
    SHIPPED                z=0.65 +19.6   z=0.80 +19.6   z=0.95 +20.0   z=1.10 +16.3  mm
    T1_NOSE_BULGE -> 0     z=0.65  +6.2   z=0.80  +6.2   z=0.95  +6.2   z=1.10  +2.4  mm
    so 13.4 mm of the 19.6 is nose_shape()'s constant and 6.2 mm is the LOFTED SHELL's
    own convexity -- two contributions nothing had ever separated
```

**AND THE STRUCTURAL REASON FIFTEEN REVISIONS OF "NOSE" WORK NEVER TOUCHED THIS AXIS.** In a
side elevation the silhouette at each height is **max-over-y of x**, which for a plan-convex
nose is **ALWAYS the centreline** — whether the bulge is 0 mm or 100 mm. **The axis is
invisible in a side view by construction.** `probe_rev59_nose.py` disclaims it in its own
header: *"It sees the nose in ELEVATION only. It cannot see anything about depth or plan
curvature."* F197 was never an inference.

**M2 IS A KILL AND IT WAS WATCHED FIRING.** Its floor of 12.0 mm sits BETWEEN the two watched
states (6.2 ablated, 19.6 shipped), so it is not derived from the expression it checks
(rule 6). It is **NOT a fidelity claim** and the probe says so in its own verdict block.

### §2a THE CEILING, WHICH IS THE HONEST HALF

The photograph side is a **STRAIGHTNESS TEST ONLY**, and that is a real limit, not a gap:

```
    ref_nolita_front34.jpg   bumper top edge   sagitta -2.94 px +- 0.46  over 118 px
                             = 6.4 sigma.  A straight 3-D line images STRAIGHT under ANY
                             pinhole camera, so this is SHAPE, not pose.
    ref_playa_34.png         REFUSES -- rms 17.6 px on a 105 px span, three unrelated
                             fragments, PAINTED and looked at
    out/r67_hero34r.png      REFUSES -- rms 61.85 px on 831 px, a whole-frame column scan
                             catching the counter nosing and the tail board too
```

**THE REAL BUS's PLAN BULGE IN MILLIMETRES CANNOT BE RECOVERED FROM WHAT WE HOLD BY THIS
ROUTE.** Converting a projected sagitta needs the camera and F26's ambiguity is unresolved.
**ONE frame carries the straightness test, and the probe PRINTS that rather than leaving it
in a paragraph.**

### §2b AND MY FIRST NOSE INSTRUMENT MEASURED THE PAINT, NOT THE NOSE (F213)

I traced the leading silhouette in a side elevation by segmenting on **RED** and read it as
the nose's section. **At y = 0 the nose is CREAM down to the V-swage apex**, so the
forward-most red pixel sits out on the two-tone break — it is the silhouette of the **PAINT
REGION**. Caught by painting (rule 8), then confirmed by the mesh disagreeing by a factor of
seven. **Retracted in the same revision (rule 13), and the corrected result is a real
negative:**

```
    sub-pixel quadratic fit over the whole window, sagitta of the leading edge
      MODEL out/r67_side.png    +0.24 px   (fit rms 0.72)
      ref_side.jpg              -1.21 px   (fit rms 1.30)
      ref_nolita_doorshut.jpg   -0.29 px   (fit rms 0.96)
    THE NOSE'S VERTICAL SECTION IS STRAIGHT TO WITHIN ~1 px IN ALL THREE.
    That axis does NOT distinguish them and it is NOT the defect.
```

**AND TWO FRAME FACTS WORTH CARRYING.** `ref_side.jpg` has the **CAB DOOR OPEN**, which
occludes the nose profile to a sliver; **`ref_nolita_doorshut.jpg` has it SHUT** and is the
unambiguous side elevation for nose geometry, at 107 px/m against `ref_side`'s 220. The
**indicator pod** protrudes ~14 px in the render and is visible in both photographs — it is
what settles that `ref_side`'s leading edge is the nose at all.

---

## §3 THE ADVERSARY — DISPATCHED (rule 15), AND WHAT I CONFIRMED MYSELF

**F208 — `T1_VW_CAPMIN` HAS BEEN A COMPLETE NO-OP SINCE REV 66.** Watched, fresh process per
configuration: shipped and `T1_VW_CAPMIN=1` print **identical** landmarks, identical residual
**0.0755**, identical cell sizes `[5167, 5122, 2277, 2081, 2023, 1887]`. `T1_VW_NOARC=1`
genuinely differs. F202's arc cut removed the end caps from `_drive`, which is what CAPMIN
acted on — **and F202's own register row says so**; it never reached §2 or §6.
**It voids §2 row 1 (F101, "cells 6 → 2" — today 6), §2 row 15 (F199) and F196's live text.**
**AND THE REV-67 BRIEF NAMED THE WRONG THREE ROWS AS UNSAFE:** F179 never used C6, and it
re-runs and stands. The unsafe rows are **F101, F199, F196**.

**F209 — F200 IS A RE-DISCOVERY OF F139, `MEASURED-rev61`.** F139 verbatim: *"C6's TARGET OF
7 IS CONTAMINATED, AND 7 IS TOPOLOGICALLY UNREACHABLE ANYWAY … The photograph's genuine glyph
count is 6, the same as the build."* Five revisions early, same headline, same re-base.
F200 cites neither it, nor F103 (*"7 cells IS reached"*), nor F174 (*"7 cells at 2065 of
24000 points"*). Re-run under F200's own protocol, 7 appears in 3 of 144 builds.
**F200's CONCLUSION STANDS on its photograph-side evidence alone; C6's re-base 7 → 6 is
safe.** What falls is *"the mark CANNOT make seven"* — **and with it rule 45's lesson.**
It was not an invisible target. **It was a MEASURED register row that five revisions read
past.** Rule 45 belongs to grade decay, not discovery.

**F210 — C6's REACH FIGURES ARE THE FIT TARGET RESTATED.** `1 − 0.8 × (0.028/0.140) = 0.84`
**exactly**, and `_fit_glyph`'s docstring says it lands the extreme *"exactly on target_r"*.
The 108 vertices are the arc cut's own tessellation. **WATCHED: under `T1_VW_NOARC` the same
line prints "8 of 16".** C12, the kill written one revision earlier to stop exactly this,
passes anyway — its 4 moving radii are interior mitre vertices.

**F211 — C10 PRINTS A 9.9 SENTINEL AS A LANDMARK MOVE.** Landmarks are fractions in [0,1].
`landmarks()` returns `None` at 138/184/276 rows, so nothing moved and the fallback fired.
**Watched: under NOARC the same row prints 0.2148.** C10's verdict is sound; its evidence is
false.

**F212 — F205 RE-MEASURED ON THIS REVISION'S OWN RENDER, AND IT STANDS.** Photograph **6**
interior cells; `out/r67_front.png` **4 / 3 / 2** at ink thresholds 20 / 30 / 40, stable under
crop padding 0/4/8 px. Rev 66's 3 reproduces exactly. **The emblem's render-side gate is RED.**
*(And a method note: `cream_cells`' argument is the INK, not the cream — `bg = disc & (~mask)`.
Passing the cream gave "raw 1, interior 0". Painted, looked at, corrected, no number published
from the broken window.)*

---

## §4 WHAT REV 67 GOT WRONG IN ITS OWN WORK — FOUR

1. **THE PAINT-NOT-THE-NOSE ERROR (F213), AND IT WAS THE HEADLINE MEASUREMENT.** I had a
   sagitta, a chord, sub-pixel edges and two corroborating frames before I asked what the
   window actually selected. **Rule 8 is the most-repeated defect in this project's history
   and I repeated it.** What saved it was painting, and then the mesh.
2. **AND BEFORE THAT, TWO WRONG READS OFF THE SAME EDGE.** My first leading-edge trace on
   `ref_nolita_doorshut.jpg` ran to `u = 9` — a **red object in the background** that the
   `red > 40` mask caught and that touches the bus, so connected components did not separate
   it either. My second, on `ref_side.jpg`, gave a "6.3 px forward bow" that was an artefact
   of choosing chord endpoints at two noisy single rows; the quadratic fit over all rows
   killed it. **Both found by painting, neither by reasoning.**
3. **`cream_cells` TAKES THE INK AND I PASSED THE CREAM** (F212), and got "raw 1, interior 0"
   — a number that looks like a measurement. Caught by painting the crop and then reading
   the function's own `bg = disc & (~mask)`.
4. **MY FIRST EDGE-ACCEPTANCE BAR COULD NOT REFUSE.** I wrote "rms ≤ 12 % of span" and
   watched a whole-frame column scan with **rms 61.85 px on 831 px** sail through it at 7.4 %.
   A purely fractional bar is too loose at long spans. Re-cut as `max(4 px, 3 % of span)`,
   which refuses both fragment traces and keeps the one real edge — **and that arithmetic is
   now a verifier row, so it cannot silently loosen again.**

**AND ONE THING I DID NOT GET TO.** C4 is still red at **0.0755** against a bar of 0.045 and
`T1_VW_SOLVE=1` is still sitting unrun. The nose took the revision, as it was ruled to.

---

## §5 THE MACHINE'S VERDICT AT CLOSE OF REV 67 — every one watched print

```
bootstrap.sh              ALL 10 PASS  (clone arrived SHALLOW -- the TENTH running)
verify_clone.sh           ALL 336 PASS on a clean tree.  329 -> 336, SEVEN rows ADDED,
                          NONE relaxed, NONE re-based
probe_rev67_nose.py       NEW.  5 checked, 1 FAILED -- P3, which is a REFUSAL and is
                          correct: the render's whole-frame trace is fragments
build.py T1_VERIFY=1      VERIFY: 0 fail, 0 warn at SUB=1
audit.py T1_SUB=2         VERIFY: 0 fail, 0 warn -- STATE.md regenerated, and it moved
                          ONLY in provenance.  Every vertex count and dimension identical,
                          which is the evidence the change was contained
probe_rev46_vw.py         12 checked, 1 FAILED -- C4 at 0.0755 against a bar of 0.045
F205 on the FRAME         photograph 6  |  out/r67_front.png 4 / 3 / 2 at thr 20/30/40
                          -- RED, and it is the owner's own second sentence
render                    grep -c Saved: /tmp/r67.log == 4
```

**AND THE STANDING WARNING.** Not one of those 336 rows compares the model to a photograph.
The three that do are `flank_compare`, `gloss_compare` and `probe_rev46_vw` — **and two of
the three still fail.**

---

## §6 WHAT REV 67 DID **NOT** DO

1. **C4 IS STILL RED** and the six constants were NOT re-solved. `T1_VW_SOLVE=1` unrun.
2. **F205 IS RE-CONFIRMED BUT NOT CLOSED.** The render cuts 3 cells where the photograph cuts
   6. Where the mesh and the render diverge is still not found — **and F210 now says the mesh
   half of that "contradiction" was never an independent observation.**
3. **THE NOSE IS INSTRUMENTED BUT NOT FITTED.** `NOSE_BULGE` was not moved, because the
   photograph cannot say what to move it to and a guess is what rule 12 forbids. **§7 asks
   the owner instead.**
4. F156 — seven revisions unacted. `REMAINING_WORK_rev61.md` §I — 27 rows, seven revisions.
5. `probe_rev63_shapefit.py` still reads the HUBCAP's weight where the nose ships its own.
6. Tyres, glass, the tail's barrel, the shut lines, the galley, F143's roof loudspeakers.
7. **F180 is stale and still OPEN** — it says four ring contacts; `probe_rev63_reach.py` now
   reports six.

---

## §7 THE BRANCH, MEASURED AT PICKUP AND AT CLOSE

```
AT PICKUP   clone SHALLOW -- the TENTH revision running.  bootstrap.sh unshallowed it
            to 614 commits.
            fetch --prune printed  - [deleted]  origin/claude/rev67-bootstrap-nose-jwawdm
            -- THE DESIGNATED BRANCH, before anything had been pushed to it, THE TENTH.
            HEAD 0 ahead / 0 behind origin/main.  bootstrap row 9 GREEN.
            git diff --name-only HEAD...origin/main -> EMPTY (no new photographs).
AT CLOSE    measured after the push, with `git fetch --all --prune` first -- see §8 of
            the rev-68 brief, which carries the figure.  Row 9 GREEN is the claim that
            matters: no branch carries work HEAD does not have.  THE PICKUP FIGURE IS
            NOT THE CLOSE FIGURE, and no sentence about branch state survives the hour.
```
