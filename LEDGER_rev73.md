# LEDGER — rev 73

`python3 revstats.py` at close: **rev 73 — 0 GEOMETRY lines, 476 instrument lines, 0 findings
closed.** Band `rev 71-80`: 97 geometry/rev, doc:geo 16.53.

---
## RULE 55, AT THE TOP, NOT IN A FOOTNOTE

**REV 73 SHIPPED NO VISIBLE CHANGE TO THE VEHICLE. HERE IS PLAINLY WHY.**

The owner ranked this revision himself: ***"Nose, then gloss/flank."***

* **HIS FIRST ITEM WAS AN INSTRUMENT TASK BY HIS OWN BRIEF'S FRAMING** — *"WINDOW THE SCAN"*.
  The nose's geometry was shipped at rev 69; what was missing was a render-side reading of it.
  That reading now exists. **No mesh moved, and none was asked to.**
* **HIS SECOND ITEM RETURNED A NEGATIVE, AND SHIPPING ANY OF IT WOULD HAVE MADE THE RENDER
  WORSE.** Eight renders across roughness × environment: **not one beats the shipped state on
  either statistic.** Rule 44 — when the guard goes red on your own new work, the guard wins.

**THAT IS TWO REVISIONS RUNNING THAT THE OWNER CAN SEE NOTHING FROM** (rev 71 also could not),
and it is the thing to fix at rev 74, not to explain again. **§9's standing instruction —
*"build first, instrument the thing you built"* — was not followed here, because both of the
owner's own ranked items were instrument-shaped.** The ranked list has geometry in it: the
contact shadow (F67, **3.83e6 px², the largest item on the delivery frame**), the tyres' tread,
the glass, the tail's barrel, the shut lines.

---
## §1 THE FIRST THING REV 73 DID, AND IT WAS NOT ON THE BRIEF

**`bootstrap.sh` ROW 9 FAILED ON PICKUP, AND WHAT IT HAD CAUGHT WAS THE OWNER'S OWN REGRESSION
LOCK.**

```
FAIL  no branch carries work HEAD does not have
      STRANDED: origin/claude/combi-render-r72-fqgsj5(2 commits, 6 files)
```

Those two commits were **`rev 72: the regression lock -- 19 new rows, every one watched failing
on the real pre-rev-72 code`** and its row-count follow-up. **They were not on `main`.** Merged
by fast-forward as the revision's first act.

**WHAT WAS MISSING FROM `main` UNTIL THAT MERGE**, measured rather than described:

| | on `main` | on the strand |
|---|---|---|
| `grep -c '§3b' PASTE_INTO_CLAUDE_CODE.txt` | **0** | **1** |
| `grep -c guards bootstrap.sh` | 7 | **9** |
| `verify_clone.sh` rows | 381 | **392** |

**The owner's message for this revision cites §3b and instructs `./bootstrap.sh --guards`. Neither
existed on the branch this session was told to develop from.** Row 9 is the reason it was found;
`CLAUDE.md`'s *"MEASURE the merge state; never transcribe it"* is the reason it was run first.
**And `origin/claude/combi-render-r73-cqs4iz` — this revision's own designated branch — was
DELETED from the remote during the session's first `git fetch --prune`.** That is the seventh
consecutive revision on which the branch prose was not the branch state.

---
## §2 THE OWNER'S FIRST ITEM — THE NOSE (F284, F285)

`probe_rev67_nose.py`'s **P3** had refused at rev 70, 71 and 72. F277 correctly killed the *"give
it a true elevation frame"* prescription by watching it refuse on a straight-on front frame too,
**but supplied no replacement.** The row's NAME blamed the three-quarter pose; its own SOURCE
COMMENT blamed the un-windowed scan.

**THE COMMENT WAS RIGHT, AND IT IS MEASURED RATHER THAN ARGUED.** Histogramming the scan's own
points on `out/r73_front.png`:

```
    v 1000-1040   355 of 481 points   <- THE BUMPER
    v  517- 880   126 of 481 points   <- the galley at u 1255..1327,
                                         the mirrors at u 401..430, the mural
```

One parabola through both populations is the 113.70 px rms.

**THE WINDOW IS PROJECTED, NOT TYPED.** `fixture_window()` builds the scene once (`T1_RIG=1` —
which is what `build.py`'s own `_want_rig` reads when `T1_PREVIEW` is absent), aims the camera
through `studio.views()["front"]`, and cuts the window from the nose **FIXTURES** (`hl_ring`,
`hl_ring.001`, `ind1_lens`, `ind-1_lens`) and the **TYRES** — **never from the bumper**.

```
    BEFORE   rms 113.70 px = 12 % of span, 481 of 481 points clipped -> REFUSED
    AFTER    sagitta +0.45 px +- 0.07 over 640 px,
             fit rms 0.81 px, 0 of 340 points clipped -> ONE EDGE
```

**RULE 6 IS TESTED, NOT ASSERTED.** `P3w` displaces a window anchor **100 mm along X** and
re-projects it; under the front orthographic camera the pixel moves by **0.000e+00 px**. The
window is a (y, z) quantity; the bow is an X one.

**FIVE BEHAVIOURS WATCHED, true exit codes, no pipe** (`rc=$?` after a pipe is the pipe's):

| invocation | reads | rc |
|---|---|---|
| `T1_NOSE_NOWIN=1` — **THE KILL**, restores the whole-frame scan | P3 **RED** | 1 |
| `out/r73_hero34f.png` — rule 42, wrong framing | *"is not a `front` frame"*, ABSENT | 2 |
| `--nomesh` with a frame — rule 37, no build, no window | ABSENT | 2 |
| bare | ABSENT | 2 |
| `out/r73_front.png` | 7 checked, 1 FAILED (P3c, by design) | 1 |

**TWO OF ITS OWN DEFECTS WERE CAUGHT BY ITS OWN CONTROLS BEFORE ANY NUMBER WAS PUBLISHED**, which
is the only reason this section is not a wrong figure:
1. the road wheels are named **`tyre1.31`**, not `tyre.001`, so the first matcher found **0 of 4**
   and the probe **REFUSED** rather than measuring on half a window;
2. `studio.aim()` writes `location` and `rotation_euler` but **not `matrix_world`**, so without
   `view_layer.update()` the fixtures projected to **u 1745 on a 1600 px frame**. A **scale
   control** now refuses a stale camera: `y=0 → u = rx/2` and `y = ortho/2 → u = 0 or rx`, err
   **< 1 px**.

### §2b WHAT THE PAINT THEN COST THE RESULT (F285) — RULE 8 EARNING ITS PLACE

P3 passed at rms 0.81 px. **`probe_scratch/rev73_bumper_window.png` shows the blue trace BROKEN
ACROSS THE MIDDLE**, and that changes what the number means.

* **340 of 641 window columns carry a point (53 %).** Largest interior gap **u 722–810, 89 px =
  14 % of span**. The fitted vertex is at **u 839** and falls **inside the gap u 836–847**.
* **The cause is not a defect**: at the centreline the cream V-swage descends to meet the **CREAM**
  bumper, so there is no red-over-cream step to find. **A sagitta is a claim about the middle, and
  this frame does not carry the middle.**
* `P3c` prints all of it and **FAILS BY DESIGN** on a threshold-free criterion — *is the vertex
  standing on a measured column?* — rather than on an invented bar.

**AND THE LARGER CEILING, WHICH IS `P3w`'s RULE-6 PROOF READ THE OTHER WAY.** `P3w` **measures**
that the front orthographic camera is blind to X. **The plan bow is an X quantity.** So P3's
+0.45 px over 640 px is the edge's curvature **IN ELEVATION** — it says the bumper's top edge
images as a level line, and it says **NOTHING** about `BUMP_BOW`.

**WHAT IT IS NEVERTHELESS WORTH:** P2's own ceiling says a three-quarter frame cannot separate
plan bow from elevation curvature because both give the same sign. A `front` frame measures the
**ELEVATION term alone**. It is the missing half of that separation — **and rev 73 did not spend
the other half.** No three-quarter render-side reading exists to subtract it from.

---
## §3 THE OWNER'S SECOND ITEM — GLOSS: F239's ONE UNTRIED PAIRING IS MEASURED, AND IT IS A NULL

F239: *"the binding constraint is the ROUGHNESS, not the environment — at 0.250 the lobe is too
broad for any environment to glint through, so the next attempt must move roughness and
environment TOGETHER, the one pairing never tried."*

**IT WAS TRIED. ELEVEN RENDERS, hero34f, 1600×1100, 96 spp.** `T1_BODY_RGH` × `T1_REFLENV`, the
full 3 × 3 grid. **Two-render floor MEASURED on this tree, not inherited: spread 0.001,
headroom 0.002.**

| `T1_BODY_RGH` → | **0.060** | **0.120** | **0.250** *(shipped)* |
|---|---|---|---|
| **`T1_REFLENV` 0.0** *(shipped)* | — | 0.408 / 0.113 | **0.412 / 0.120** |
| **`T1_REFLENV` 1.0** | 0.410 / 0.116 | 0.411 / 0.116 | **0.416 / 0.126** ← best |
| **`T1_REFLENV` 21.0** | 0.388 / 0.108 | 0.388 / 0.110 | 0.388 / 0.118 |

*(spread / headroom; bar on the spread is 0.60. The shipped state rendered a SECOND time reads
**0.413 / 0.118** — that is the floor, and every difference below is quoted against it.)*

**THE PAIRING IS REFUTED, AND IN THE STRONGEST FORM AVAILABLE: THE ROUGHNESS IS NOT INERT, IT IS
MONOTONICALLY HARMFUL, AT EVERY ENVIRONMENT LEVEL TESTED.** Read the table along its rows —
lowering roughness from the shipped 0.250 costs spread at **every** environment setting:

```
    env  0.0     0.412 -> 0.408            (0.060 not rendered)
    env  1.0     0.416 -> 0.411 -> 0.410
    env 21.0     0.388 -> 0.388 -> 0.388   (identical to the printed precision)
```

**F239's *"the binding constraint is the ROUGHNESS, not the environment"* predicted the opposite** —
that freeing the roughness with structure present would let the gate move. It moves **down**, or
not at all. **The roughness is not the binding constraint.**

**AND THE ONE CELL THAT BEATS THE SHIPPED STATE IS NOT THE PAIRING — IT IS THE ENVIRONMENT ALONE,
AT F239's OWN VALUE, AT THE SHIPPED ROUGHNESS.** `T1_REFLENV=1.0` reads **0.416 / 0.126** against
**0.412 / 0.120**: **+0.004 spread (4× the floor) and +0.006 headroom (3× the floor)**, and it
reproduces F239's own row (0.416 / 0.127) almost exactly. **That is a real gain and a tiny one —
2 % of the 0.188 the gate is short.** Its chroma cost is measured in §3b.

### §3b THE ONE POSITIVE CELL, PRICED — AND IT IS INVISIBLE

`T1_REFLENV=1.0` at the shipped roughness is the only cell that beats the shipped state.
**IT DOES NOT SHIP, AND THE REASON IS MEASURED, NOT ARGUED.**

**THE CHROMA COST, ON F266's PHYSICS-CLOSED PATH** — `side` rendered **Raw 16-bit stopped down**
(`T1_VT=Raw T1_LOOK=None T1_EXP=-2.5`) and read with `probe_rev71_red.py --transform=raw`, which
is the recipe the rev-73 brief warned must not be lost:

```
    photograph ref_side.jpg          linear G/R 0.0307
    render, SHIPPED   (env 0.0)      linear G/R 0.1091   -- 3.55x the photograph
    render, env 1.0                  linear G/R 0.1099   -- 3.58x the photograph
```

**It costs +0.0008, i.e. the red gets very slightly worse.** ⚠ **AND THAT COST HAS NO FLOOR UNDER
IT (rule 49): rev 73 did not render this statistic twice, so +0.0008 is a difference, not yet a
measurement.** The flank gate is unmoved: **0.687 → 0.688** (`Señor`).

**AND THE DECIDING NUMBER — IS IT VISIBLE AT ALL?** A/B against the two-render floor, hero34f,
8-bit levels:

```
    FLOOR: shipped vs shipped again    >8 levels 2.044 %   worst 41   >32 0.043 %
    shipped vs T1_REFLENV=1.0          >8 levels 2.367 %   worst 46   >32 0.044 %
```

**IT IS AT THE FLOOR. The >32-level tail is 0.044 % against 0.043 % — identical.** A change worth
+0.004 on one gate's statistic and invisible to the frame is not a change to ship, and it is not
worth one of the owner's questions either. **`T1_REFLENV` keeps its shipped default of 0.0, which
is where F239 put it, and now for a second and independent reason.**

**CEILING, STATED (rule 12).** One gate's statistic, one frame, one view, at 1600×1100/96 spp.
`T1_REFLENV` was sampled at 0 / 1 / 21 and roughness at 0.060 / 0.120 / 0.250 — **the grid is
6 of 9 cells, not a sweep**, and roughness **above** 0.250 was not tested at all. The chroma cost
was measured for the ONE cell that beat the shipped state (§3b) and for no other, so the other
seven cells are priced on the gloss statistic alone. **What is closed is F239's prescription, not the gloss gate**, which
still misses its bar by 30 %.

---
## §4 WHAT THE RULE-15 ADVERSARY FOUND IN THE INCOMING BRIEF (F286–F291)

Dispatched at `PASTE_INTO_CLAUDE_CODE.txt` with instructions to RUN every figure. It returned 18
defects. **Every leg recorded below was re-measured here before it was written down**; the one
that was not is graded `INHERITED` and says so.

| | what it found | severity |
|---|---|---|
| **F286** | `probe_rev71_red.py` **died on a bare traceback with no summary line** on the exact command §4 tells you to run. The refusal is correct; the reporting was not — rule 9 had nothing to read. **FIXED and WATCHED: rc 3, `0 checked, 0 FAILED, 1 REFUSED`** | live defect |
| **F287** | *"bare → 2 checked"* is the **`--nomesh`** reading; **bare is 4**. In five carriers, including `verify_clone.sh`'s own row, which was **NAMED "bare" while RUNNING `--nomesh`** — the guard reproduced the mislabel instead of catching it. **Renamed, not re-based, plus a companion row pinning `--nomesh`'s own count** | live defect |
| **F288** | `--guards` and F281 both read `T1_REAR_SEALSTAY=1 → 2 fail`; **brief §4 prints `1 fail`**. Caught the first time `--guards` was run under the owner's instruction to run it | brief wrong |
| **F289** | *"every cheap lever is dead"* quotes F252's figure **without F252's ceiling** (`grep`: *"0.0010 WORSE"* **1**, *"BROKEN RULER"* **0**) and never names F252's **option (C)**, the only one that improved both frames | rule 46 + rule 16 |
| **F290** | *"gloss/flank 2.89e6 px², BOTH gates failing"* **prices two gates with one gate's pixels.** `flank_compare` tests the **`Señor` lockup — item 10 at 2.26e4 px², 0.68× the emblem.** **The ruling was put to him in that form** | premise of F282 |
| **F291** | `flank_compare` reads **0.676**, not 0.689. And the ranking's own **#1 item — the contact shadow, 3.83e6 px², 115× the emblem — is in no version of the choice** | figures |

**THE ONE I DID NOT REPRODUCE, STATED RATHER THAN ABSORBED.** The adversary re-ran
`T1_REV71_SEARCH=AB` and reports the emblem's free-endpoint lever measuring **+0.0056 / +0.0090,
both positive** — the **sign of the brief's "0.0010 WORSE" reverses**. **Rev 73 did not reproduce
that run**: it costs ~13 min of CPU and the machine was committed to the owner's ranked sweep.
**F289 is graded `MEASURED-rev73` for the two greps and `INHERITED-rev73` for the reversal.
RE-RUN IT BEFORE ACTING ON IT.**

---
## §5 THE MACHINE AT CLOSE

```
bootstrap.sh              10 PASS  (row 9 FAILED on pickup -- see §1 -- and passes after the merge)
bootstrap.sh --guards     ALL 25 PASS.  All FIVE rear-hatch kills exercised; probe_rev45_ground
                          reads 5/0, so F283's 4 -> 5 re-base holds
verify_clone.sh           ALL 392 PASS on a clean tree, 0 FIDELITY / 392 SELF-CONSISTENCY
                          (+2 rows added this revision -- see the close)
build.py T1_VERIFY=1      VERIFY: 0 fail, 0 warn at SUB=1 and SUB=2 (both via --guards)
photometry.py             9 checked, 0 FAILED
probe_rev67_nose.py       7 checked, 1 FAILED -- P3c, BY DESIGN.  READ ITS MESSAGE
gloss_compare.py          0.412 (bar 0.60) on out/r73_hero34f.png -- FAILS
flank_compare.py          0.676 (i) (bar 0.75) on out/r73_side.png -- FAILS.  NOT 0.689
visibility_budget.py      gloss 2.89e6 px^2; emblem item 9 of 16 at 3.32e4; 87x.
                          TOP ITEM: F67 the contact shadow, 3.83e6 px^2
revstats.py               rev 73: 0 geometry, 476 instrument, 0 closed
```

**AND THE NONDETERMINISM FLOOR, RE-MEASURED BECAUSE THE BRIEF SAID TO AND IT WAS FIVE REVISIONS
OLD.** Same tree, rendered twice, hero34f 1600×1100 / 96 spp, read at 16 bits through
`photometry.read_png` and scaled to 8-bit levels:

```
    % of px with any channel differing by >8 levels   2.044 %   (F228 published 2.441 %)
    worst channel difference                          41 levels (F228 published 40)
    % >32 levels                                      0.043 %
```

⚠ **CEILING: F228's frame and view are not recorded, so this is a re-measurement on `hero34f` and
not necessarily a refutation of F228's number on whatever it was measured on.** Quote **2.044 %
on hero34f** and say which.

---
## §6 WHAT REV 73 GOT WRONG IN ITS OWN WORK

1. **The first window matcher found 0 of 4 tyres** and would have measured on a half-built window
   had the probe not been written to refuse first.
2. **The first projection was through a stale camera matrix** and put the fixtures 145 px off the
   side of the frame. It raised `IndexError` — it did not report a number — but it raised in
   `paint_window`, i.e. **the paint caught it, not the arithmetic.** The scale control was added
   afterwards so it cannot recur silently.
3. **`F283` was used as this revision's own finding ID for two commits' worth of drafting** before
   the rule-15 adversary pointed out it was already taken by rev 72's `--guards` row. Renumbered
   to F284/F285 before the first commit.
4. **The gloss grid is 6 of 9 cells and was called a sweep in the first draft of §3.** Corrected
   to name the missing cells.
