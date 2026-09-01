# LEDGER — rev 73

`python3 revstats.py` at close: **rev 73 — 7 commits, 0 GEOMETRY lines, 1466 doc, 583 instrument,
0 findings closed.** *(Read after the last content commit. The earlier reading in this file's own
drafting — 0 / 8 / 476 — was taken before the ledger and brief were tracked; both are true of the
moment they were run, which is exactly the ceiling below.)*

⚠ **AND THE CEILING ON THAT LINE, WHICH NO LEDGER HAS EVER STATED: IT IS MEASURED BEFORE THE
HANDOFF COMMIT AND THE HANDOFF COMMIT INVALIDATES IT.** This file and
`NEXT_CONTEXT_PROMPT_rev74.md` are ~600 lines of doc that land AFTER the figure is read, against
0 geometry. **Re-run `revstats.py` after the handoff lands if you want rev 73's true doc:geo — it
is worse than the number above, and it is unbounded above because it divides by zero geometry.**

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
that the front orthographic camera is blind to X **geometrically**. So P3's +0.45 px over 640 px is
the edge's curvature **IN ELEVATION**.

### §2c ⚠ AND REV 73's FIRST DRAFT WENT ONE STEP FURTHER THAN THAT AND WAS WRONG (F292)

It said the reading *"says NOTHING about `BUMP_BOW`"*. **A rule-17 adversary dispatched at this
revision's own outgoing brief made the distinction I had slid over: `P3w` displaces a WINDOW
ANCHOR, so it proves the WINDOW is X-blind and says nothing whatever about the TRACE — and
`T1_BUMP_BOW`, the switch that would settle it, HAD NEVER BEEN RUN.** Rule 36 unfired on the
revision's headline row.

**IT WAS RUN, WITH A FLOOR UNDER IT.** Build log: `bumper_f nose face: BUMP_BOW 0.000 … bow at
y=0 +0.00 mm` against the shipped `+21.09 mm`.

```
    shipped bow (+21.09 mm)          sagitta +0.45 px   span 640   n 340
    T1_BUMP_BOW=0  (+0.00 mm)        sagitta +0.07 px   span 627   n 314
    FLOOR, the same config twice     +0.45 -> +0.44     span 640   n 335
```

**THE ABLATION MOVES THE SAGITTA 0.38 px AGAINST A BETWEEN-RENDER FLOOR OF 0.01 px — 38×.**
It also costs 13 px of span and 26 columns.

**SO THE TRACE IS SENSITIVE TO THE BOW, AND BOTH FACTS ARE TRUE AT ONCE.** `P3w`'s `0.000e+00`
stands — the window is X-blind geometrically. What is refuted is the slide from *the window is
blind* to *the reading is blind*. **The mechanism is PHOTOMETRIC**: bowing the blade turns it
against the light, which moves the sub-pixel red/cream threshold and changes which columns carry a
detectable step at all.

⚠ **CEILING, AND IT IS THE WHOLE POINT: SHADING IS NOT A RULER.** 0.38 px is not convertible to
millimetres by anything in this tree, and one ablation at one value is **two points** — it
establishes SENSITIVITY, not a calibration and not a monotone response. **Do not read +0.45 px as a
measurement of `BUMP_BOW`. Do read it as a channel a ladder could calibrate — which is a better
position than F231's *"cannot be recovered"*, and rev 73 did not build the ladder.**

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

**AND THE TWELVE THE SIX ROWS ABOVE DO NOT COVER, CARRIED BY NAME RATHER THAN DROPPED (rule 16) —
the rule-17 adversary caught this ledger recording *"18 defects"* and carrying six.** None of these
became a register row; they are listed so a rev-74 context can find them without the transcript:

1. **`probe_rev72_bits.py`'s B4 ladder RISES (0.40 % → 1.02 %) on a fresh frame**, where the rev-73
   brief printed *"FALLS (0.46 % → 0.07 %)"* — **the opposite direction**, quoted from a row that
   fails by design and says it must not be quoted. **Carried into the rev-74 brief's §0b.**
2. **F271's headline null does not reproduce: 0.708 % on `out/r73_hero34f.png`, not the published
   0.623 %** — a move of 13 % of itself, **with no floor under it** (rule 49). ⚠ **This figure is
   in NO carrier but this line and the rev-74 brief; it names a frame here and there only.**
3. **The rev-73 brief contradicted itself on the rear pane in one document** — §2.3 *"Measured: it
   is TRANSMITTING"* against a "weakest" bullet *"THE PANE STILL RENDERS OPAQUE DARK"*. The
   adversary rendered, cropped and looked: **transmitting.** The weakness bullet is the false half.
4. **`audit_adversary.py` STILL PRINTS `ok` ON QUESTIONS WHOSE TEXT ASSERTS REFUTED STATES** — the
   overfit question quotes F255's withdrawn *"LOSES by 0.0249"*, the traced-pressing question says
   *"RENDERS AS AN UNRECOGNISABLE BLOB"* against F262's shards. **Rule 50's shape, recorded at
   rev 68, live at rev 73, and in NO register row.** Its only other home was the rev-73 brief's
   "weakest" section. **`grep -rln "UNRECOGNISABLE BLOB"`.**
5. **§2.3's G/R 0.204 was published from a SINGLE UNPAINTED PIXEL** (r645, c1050) whose 21×21
   neighbourhood spans 0.000–0.988. The conclusion is right; the number is rule-8 contraband.
6. **`probe_rev71_emblem.py`'s own comment says `~40 s` for `T1_REV71_SEARCH=AB`; it is ~13 min.**
   **Carried into the rev-74 brief's §2.2 and §4.**
7. **`probe_rev69_fitpose` P3's *"NEAR BALANCED"* is 87/212 — 2.4×**, which does not support *"the
   ink is the right AMOUNT arranged the WRONG WAY"* as strongly as F104's phrase implies.
8. **§2.5's *"TEN revisions unacted"* on F156 is hand-incremented** (five → six → seven → NINE →
   TEN, skipping eight) and derived from nothing. F156 is `MEASURED-rev62`.
9. **§0b's *"five kills"* in `photometry.py` is six** by the probe's own printed rows.
10. **§4's `probe_rev71_bulbs` comment says *"window MISPLACED"*; F250's live ceiling is DILUTION** —
    the shipped third cut was painted and looked at. **Carried into the rev-74 brief's §4.**
11. **§3 said `verify._rear_hatch` has *"three kills"*; F278 and the brief's own audit block say
    FIVE.** `--guards` exercises five. **Carried into the rev-74 brief's §4 with the live counts.**
12. **§6 under-counted the register by seven rows** — *"F268–F276 are rev 72's"* when F268–F281 and
    F283 are all `MEASURED-rev72` and F282 is `RULED-rev72`. **Among the uncounted was F283, whose
    subject is the very script §3b tells you to run.**

**THE ONE I FIRST COULD NOT REPRODUCE — AND THEN DID, AT THE CLOSE (F289b).** The adversary
re-ran `T1_REV71_SEARCH=AB` and reported the emblem's free-endpoint lever measuring positive, which
would reverse the incoming brief's *"0.0010 WORSE"*. F289 graded that `INHERITED` because rev 73 had
not reproduced it. **It was re-run to completion in this session and it agrees to four decimals:**

```
    shipped                                       fit 0.8425   indep 0.8215
    (A) CURRENT parameterisation re-searched       fit 0.8633   indep 0.8284
    (B) THE BRIEF'S PRESCRIPTION, free endpoints   fit 0.8689   indep 0.8374
```

**(B) − (A) = +0.0056 / +0.0090; (B) − shipped = +0.0264 / +0.0159. All four positive, including on
the INDEPENDENT frame.** The `INHERITED` grade is discharged.

⚠ **AND THE CEILING THAT MATTERS MORE THAN THE RESULT: NOTHING HERE WAS BUILT, RENDERED OR LOOKED
AT.** Rule 56's own counterexample — the traced pressing — scored positive on both frames by this
same instrument and renders as **disconnected shards** (F262). A silhouette IoU at ~220 px cannot
see fragmentation, and this objective still has **no legibility term**. **The emblem has a lever the
record had written off; it does not yet have a fix.**

---
## §5 THE MACHINE AT CLOSE

```
bootstrap.sh              10 PASS  (row 9 FAILED on pickup -- see §1 -- and passes after the merge)
bootstrap.sh --guards     ALL 25 PASS.  All FIVE rear-hatch kills exercised; probe_rev45_ground
                          reads 5/0, so F283's 4 -> 5 re-base holds
verify_clone.sh           read the verdict block; the row count is written LAST by
                          `audit_brief.py --fix-count` and is stated in the brief, not here --
                          a ledger that types it goes stale the moment a row is added.
                          Rev 73 added NINE ck rows and removed one (net +8) on rev 72's 392.
                          ⚠ THE FIRST DRAFT OF THIS LINE SAID "ALL 392 PASS ... +2 rows" AND
                          BOTH HALVES WERE WRONG -- caught by the rule-17 adversary
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
