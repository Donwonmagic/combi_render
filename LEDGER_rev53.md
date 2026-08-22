# LEDGER — rev 53

Every figure below was watched printing. The single run they are quoted from is
`probe_rev53_chip.py`; re-run it and the same numbers come back.

---

## §0. THE HEADLINE

Brief §4 item 2 asked for one number: **how big a chip is in a photograph.**

**There are no chips to size, and that is not a resolution artefact.** The frames
we hold would have shown the render's own chip population and they show nothing.
The measurement that item 2 wanted cannot be made — but the measurement that
*replaces* it is stronger, because it bounds the answer instead of guessing it.

**HE THEN RULED ON IT** (§5), so the cream is no longer an open question.

---

## §1. WHAT THE RADIUS ACTUALLY IS — THE BRIEF'S QUESTION WAS SLIGHTLY THE WRONG ONE

In `t1_mats.py` the gate is `edge = 1 - dot(bevel_normal, true_normal)` — grep
`_dot.operation = 'DOT_PRODUCT'`. That is non-zero **only within about one bevel
radius of a fold**. So the Bevel radius is **not a chip diameter**; it is the
**half-width of the wear band along an edge**. Grounding it needs two things
from a photograph, and item 2 named only the second:

1. the **width of the chipped band along a fold** — this sets the radius;
2. the **size of one chip** — this bounds (1) from below.

**Neither is recoverable, because the vehicle's cream is not chipped.**

---

## §2. THE INSTRUMENT, AND WHY IT IS NOT REV 52'S

`LEDGER_rev52` §6.3 compared the render's fascia at **4.07 %** with the
photograph's **0.00 %**. Those two numbers were not measured on a common footing:
the render is **271.2 px/m** and `ref_side.jpg` is **211.5**, so a fixed 9 px
local-median radius is a **different physical size in each**.

This probe puts each render **through the photograph's own optics** first —
blurred to the measured PSF, decimated to 4.728 mm/px, given the frame's own
0.99 DN noise — and only then reads it with the same estimator.

Calibrated on the record's own two controls **before** touching a frame:

| control | record | this estimator |
|---|---|---|
| flat cream + 0.5 DN noise | 0.00 % | **0.000 %** |
| flat cream + known chips | 7.316 % (true 7.32) | **7.329 % (true 7.33)** |

Frame constants, measured here: scale **211.5 px/m → 4.728 mm/px**; **PSF sigma
0.735 px** (n=110 columns, FWHM 1.73 px = 8.2 mm) on the fascia's bottom edge.
*Ceiling, stated: the rear hubcap is at x=750.5 but the FRONT hub is behind the
leaning man, so the wheelbase span is a **consistency check** here, not an
independent re-derivation. The scale is the record's.*

---

## §3. WHAT THE PHOTOGRAPHS SAY

| window | frame | px | noise DN | dark |
|---|---|---|---|---|
| counter fascia, tracked per column | `ref_side.jpg` | 4861 | 0.99 | **0.165 %** |
| tail cream below the nosing | `ref_rear34.jpg` | 4952 | 1.48 | **0.000 %** |
| counter fascia, mid | `ref_rear34.jpg` | 3011 | 0.99 | **0.266 %** |

The `ref_side` fascia's 0.165 % is **8 pixels in 4861, in 4 blobs, 3 of them
single pixels** — JPEG noise. The fascia window is 18.3 px tall = **87 mm**
against the record's ~94 mm, which is how we know it is on the right object.

**Robust across the estimator's own constants**, so the headline is not a
tuning artefact: 0.391 / 0.165 / 0.123 / 0.082 % at thresholds 8/12/16/20 DN,
and 0.021 / 0.165 / 0.288 % at median radii 5/9/15 px.

### §3.1 THE DETECTION FLOOR — each size against its OWN null control

| chip dia | true cov | NULL, no chips | with chips |
|---|---|---|---|
| 4 mm | 5.00 % | 0.000 % | 0.316 % |
| **6 mm** | 5.00 % | 0.000 % | **3.055 %** |
| 10 mm | 5.01 % | 0.000 % | 7.059 % |
| 20 mm | 5.03 % | 0.000 % | 6.684 % |
| 40 mm | 5.21 % | 0.000 % | 6.031 % |

**The render's own chips are 18.9 mm area-weighted and 20.3 DN deep.** A synthetic
at that size and depth reads ~3.5 %; the render through the same optics reads
**2.589 %**. The photograph reads **0.165 %**. So the render's chip population is
**excluded by the photograph at roughly 16x** — the frame would have shown it.

> **CEILING, AND IT IS A REAL LIMIT.** Swept against chip DEPTH, the floor moves:
> at −20 DN a 6 mm chip reads 0.008 % and is **invisible**; only ≥10 mm clears
> 0.165 %. At −10 DN nothing at any size clears it. **So this excludes the
> render's population, NOT fine faint scuffing.** A chip through to primer is far
> darker than 20 DN, so the conclusion holds for chips; it does not hold for
> light scuffing, and this probe cannot see that.

> **SECOND CEILING, inherited and still true:** a local-median dark-pixel count is
> structurally blind to large-cell, low-contrast **MOTTLE**. A 40 mm band-pass
> mottle statistic was attempted here and **WITHDRAWN, not published**: on a long
> thin band it reads the lighting gradient (the photograph's fascia is unevenly
> lit, the render's studio-uniform), not mottle. Recorded so it is not re-tried blind.

---

## §4. THE WEAR-BAND PROFILE — THE DEFECT AS A SHAPE, NOT A SCALAR

Dark coverage in 6 mm bands measured **up from the fascia's bottom fold**:

| | 0–6 | 6–12 | 12–18 | 18–24 | 24–30 | 30–36 | 36–42 mm |
|---|---|---|---|---|---|---|---|
| `ref_side.jpg` **photograph** | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| Pointiness gate | 6.12 | 1.22 | 4.12 | 7.68 | 11.02 | 11.92 | **14.03** |
| edge signal, 2.75 mm | 1.34 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| edge signal, 12 mm | 1.34 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

**The default's wear is HEAVIEST FARTHEST FROM THE FOLD.** That is the Pointiness
saturation defect stated as a shape: it puts the most wear where a real edge chip
cannot be. A single coverage number never showed that.

*The edge signal's 1.34 % is **12 pixels**, 10 of them shared between the two
radii at x 1299–1307 — one fixed geometric feature, not radius-dependent
chipping. Painted and looked at.*

### §4.1 REV 52'S EXPLANATION IS RETRACTED — in the source, not only here

Rev 52 said the Bevel gate looks empty because `GAPW/2 = 2.75 mm` is **0.75 px**
and therefore **sub-pixel at every scale this project renders**.

* **REFUTED.** `T1_EDGERAD=12` is **3.3 px** at 271.2 px/m, well above a pixel,
  and the fascia is **unchanged at 0.000 %**.
* **A butt joint is refuted too** — asked of the mesh: `counter` is a **closed
  mesh with 0 boundary edges**.
* **The lever is not inert.** The 2.75 mm vs 12 mm difference image lights up
  **every window frame, shut line, arch lip and gutter and nothing between them**
  — 53 004 px differ by >6 DN. The gate works and is edge-confined as designed.
* **WHY THAT ONE FOLD IS SILENT IS OPEN.** Stated as open, not guessed.

The retraction is in `t1_mats.py` (grep `IS RETRACTED HERE`) and in
`verify_clone.sh`, and a row holds it there — rule 15.

---

## §5. HIS RULING, AND WHAT SHIPPED

Asked as multiple choice on `probe_scratch/rev53_owner_fascia.png` — photograph,
as-built and re-based, **all three at the same 4.728 mm/px** — with the measured
coverages beside them. He answered:

> **"Follow the photograph — clean cream."**

So **the ray-traced edge signal is the DEFAULT now** and `T1_PTWEAR=1` restores
Pointiness. `SPEC` §3's WEATHERED lock is **narrowed to the red and the running
gear**; the cream follows the frame.

| | own px/m | through the frame's optics |
|---|---|---|
| Pointiness (was default) | 8.826 % | **2.589 %** |
| edge signal, 2.75 mm | 0.000 % | **0.000 %** |
| edge signal, 12 mm | 0.000 % | **0.000 %** |
| **the SHIPPED build** | 0.000 % | **0.000 %** |
| `ref_side.jpg` | — | **0.165 %** |

**The shipped build reproduces the 2.75 mm case exactly**, which is a control on
the flip rather than a restatement of it.

**AND THE CHANGE IS CREAM-ONLY, WHICH IS THE SCOPE HE RULED ON.** A red flank
window in the same two renders: **0.527 % → 0.537 %**, unmoved. The red lives on
the subdivided shell, where Pointiness never saturated.

**AND THE ABLATION IS PROVEN END-TO-END, NOT ASSERTED.** A row that greps for a lever only shows the
string is there. Rendered:

| | counter fascia, render's own scale |
|---|---|
| `r53base` — Pointiness, when it was the default | **8.826 %** |
| `r53ptw` — `T1_PTWEAR=1`, restoring it | **8.795 %** |
| `r53final` — the shipped default | **0.000 %** |

The 0.031 pp between the first two is Cycles sampling noise between two renders, not a difference in
the gate. **The lever restores what it claims to restore.**

**`T1_PTWEAR` DID NOT EXIST UNTIL THIS REVISION, THOUGH THE SOURCE SAID IT DID.**
`t1_mats.py` has claimed since rev 52 that *"T1_PTWEAR=1 restores the Pointiness
gate and moves NOTHING ELSE"*; the string appeared in **no other line of the
source**. Rev 52 named a lever it never built. It is built now. Rule 10: a claim
in a source comment is not a lever.

---

## §6. MY OWN INSTRUMENTS — SEVEN WRONG, EVERY ONE CAUGHT BY A CONTROL OR BY PAINTING

Not one was caught by reasoning about it.

| what was wrong | what it read | how it was caught |
|---|---|---|
| the floor used the window's raw high-pass **STD** (8.57 DN, outlier-driven) instead of its **MAD** (0.99) | the **null control read 8.117 % on PURE NOISE** — every "detection" in that pass was noise | the null control |
| window on the **MENU CARD** | **12.014 %** — printed text counted as chips | painted it |
| window on the **bulb-string shadow** | 0.000 % | painted it |
| window on the **window chrome** | 1.089 % | painted it |
| window on the **tail/wall highlight** | 0.000 %, noise 0.49 DN (implausibly smooth) | painted it |
| window on the **white wall behind the bumper** | 2.668 % | painted it |
| the **trap check** that should have caught the wall one | passed | its own box was on the **LEFT wall only** — a trap check is a window too |
| the bracket-column filter had its **SIGN BACKWARDS** | dropped nothing | a bracket is cream, so the red detector finds red **below** it and the column comes out **TALLER**, not shorter — rule 35's shape |
| excluding bracket columns was not enough | 8.75 % in the edge band | the survivors sat on the bracket **SHOULDERS**, in the columns beside an excluded one |

**Five of the six windows first tried were contaminated. Only the counter fascia
survived on `ref_side.jpg`.** That is the same rate the last two revisions
recorded, and the same cause every time.

### §6.1 AND TWO OF MY OWN GUARDS DID NOT FIRE WHEN FIRST WATCHED

Both were written, asserted in a comment to catch a specific defect, and **did
not**. Caught only by watching them fail:

* **"the EDGE signal is the DEFAULT"** was anchored on `pw = _mr(nt, EDGE, ...`
  at an 8-space indent — but **both branches are that**, so swapping the two
  branches left it passing. Its own comment claimed it caught a swap. It did not.
  Re-anchored on the line **after** the `T1_PTWEAR` test.
* **"his cream ruling is recorded"** was anchored on `Follow the$` — which matched
  a line that merely **WRAPPED** there, not the sentence recording the ruling.
  **A guard anchored on where a sentence happens to wrap tests nothing.**

---

## §7. GUARDS ADDED — nine rows, EVERY ONE WATCHED FAILING

`verify_clone.sh` **151 → 164** across the revision. Watched failing on: a silently flipped default;
**an APPENDED override after the derived fallback** (not merely a deletion —
§4.2's stated failure mode); a removed radius lever; a removed `T1_PTWEAR`; a
dropped null control; an un-retracted retraction; a typed literal replacing the
derived edge window; a dropped ruling.

**One rev-52 row was RE-BASED, cause named and companion added** (`CLAUDE.md`
allows this only on those terms): *"edge window DERIVED from a 90 deg fold"*
counted **mentions** of `W_EDGE_90`, so it broke when this revision added a
comment that merely names the symbol — a wording change failing a row meant to
test a **derivation**. It is anchored on the derivation expression now, with a
companion row *"edge window is not a typed literal"* making the thing it actually
cares about separately testable. Both watched failing.

---

## §7.1 A TYPED COPY THAT HAD DRIFTED — AND MY OWN AUDIT CERTIFIED IT

Caught only because the **rev-52 session's report was re-checked against the machine** instead of
being read. It said the A7 gap reproduces off a live `X_TAIL = -1.8730`; rev 53's audit "verified"
802.7 mm off **−1.8727**. **Rev 52 was right.**

`t1_core.py` writes `X_TAIL = _aft(X_TAIL_OLD)` — a **call**, evaluating to **−1.873000**.
`flank_compare.py` carried a **typed copy** at −1.8727, drifted 0.3 mm, harmless in that file (it is
only printed in a diagnostic) but read as live by this revision's brief audit and published in its
**"verified clean" list**. An audit that certifies a stale value is worse than no audit.

Fixed in the tree's own idiom (`folk_gen.py` already derives it as `X_AXLE_R - O_NEW`, which equals
`_aft(X_TAIL_OLD)` exactly because f = 1 at the tail). Two rows, three drift routes watched failing —
re-typing the literal, drifting `O_NEW` (the silent case), drifting `LID_X1`.

**`verify_clone.sh` 162 → 164.**

---

## §8. WHAT IS STILL OPEN

* **Why the counter fascia's own bottom fold produces no edge signal at any
  radius.** Sub-pixel refuted, butt joint refuted, lever proven live. Open.
* **Item 2's original question is unanswerable from the frames held** and will
  stay so until a frame shows chipping. `PHOTOS_WANTED_rev52.md` item 7 (one
  hubcap, square on and close) would also serve this.
* **Mottle** — see §3's second ceiling. The statistic attempted here was withdrawn.
* **`cream_rms.py` was NOT run at rev 53 either.** Still a dormant
  render-vs-photograph gate with zero rows in either acceptance script.
* Everything the rev-53 brief §4 lists as items 1, 3, 4, 5, 6 — **untouched**.
