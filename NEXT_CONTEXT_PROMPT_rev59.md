# NEXT CONTEXT PROMPT — rev 59

## §0.0 DO THIS FIRST — THE WHOLE DECISION, IN TWENTY LINES

**Before you read another word, put the machine to work. It is CPU-bound and idle right now.**

```bash
cd /home/user/combi_render
./bootstrap.sh                 # the toolchain is NOT on the clone -- this builds it
nohup env T1_SUB=1 T1_PREVIEW=side,hero T1_PFX=r59 T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
  /tmp/blender/blender -b -P build.py > /tmp/r59.log 2>&1 &
```

`out/` is untracked and starts empty. **`bootstrap.sh` first** — at rev 58 `/tmp/blender/blender`
did not exist and `bpy` was not importable; the script rebuilt both from nothing and returned
ALL 10 PASS. Then start the render, then read. `T1_PREVIEW` takes a LIST: `side,hero` renders both
in ONE session and pays the ~20 s scene build once. `side` feeds `flank_compare.py`, `hero` feeds
`gloss_compare.py`.

**THE OWNER RE-RANKED THIS AT REV 58 AND HIS RANKING OUTRANKS THE PIXEL BUDGET.**

> *[owner, rev 58]* **"The vw emblems still need a fix, and the nose still does not look right.
> I just want to make sure that is somewhere in the plan. We don't need to commit to a full
> render until everything is fixed right?"**

**Both halves are instructions. The emblem is item A. The delivery frame is the LAST step, not a
milestone — do not spend 106.8 minutes on it until the model is right.**

| # | do | worth | gate |
|---|---|---|---|
| **A** | **F63 — THE NOSE GLYPH BUILDS AS AN X, NOT A V OVER A W.** His FIFTH report. **GATED at rev 58 and the gate FAILS**: `probe_rev46_vw.py` C6, photograph **7** cream cells, built **6**. The W's outer arms float **18.9 mm** short of the band. **F65 lists three fixes that were tried and all failed — do not re-try them** | the emblem is dead centre on the nose and he has reported it five times | **`probe_rev46_vw.py` C6, new at rev 58, WATCHED FAILING** |
| **B** | **THE NOSE BEYOND THE EMBLEM — a LEAD, not a finding.** Recover the photograph's camera, render THAT view, and compare the cream/red boundary. Un-pose-matched crops are how rev 55's "X" dissolved twice | — | none yet; building it is the job |
| **C** | **F45 — THE GALLEY AND ROOF-APERTURE INTERIORS ARE UNTEXTURED WHITE BLOCKS**, seen through four openings, dead centre. Plainly visible in `out/r58b_hero.png` | **7.4 × 10⁵ px²** | none — build one, or accept it and say so |
| **D** | **F15 / A7** — the unlit roofed run between the last light inlet and the tail | 8.2 × 10⁵ px² | none |
| **E** | **F01/F39** — `Senor`, 28.5 % of its ink, in the ARTWORK not the render | 2.7 × 10⁴ px² | `flank_compare.py` |
| **—** | **F08 the badge STROKE WEIGHT** | **1.4 px²** | **CEILED. Do not.** Note this is NOT F63 |

**F63 AND F08 ARE DIFFERENT FINDINGS AND IT MATTERS.** F08 is the stroke's WIDTH, ceiled at rev 57
because the frame cannot resolve it — worth 1.4 px². **F63 is the glyph's SHAPE AND REACH**, which
the same frame resolves easily (7 cells against 6) and which the owner can see. Do not let F08's
ceiling talk you out of F63.

**THE RANKING RULE FROM REV 57b STILL STANDS** — rank by pixels of the delivery frame,
`python3 visibility_budget.py`; gate availability is a tie-breaker — **but the owner outranks it,
and at rev 58 he used that.** `CLAUDE.md`: *"The machine outranks the prose. The owner outranks the
record."*

---

**Now read this whole file before you CHANGE anything.** Then `CLAUDE.md`, then `LEDGER_rev58.md`
(where every number in §2 comes from), then `OPEN_FINDINGS.md`, then `AUDIT_rev57_efficiency.md`.

---

## §0. THE GOAL, AND HOW FAR OFF IT WE ACTUALLY ARE

**CARRIED FORWARD FROM THE REV-55, 56, 57 AND 58 BRIEFS. It is not mine and it is not to be
dropped — rule 16.**

**PHOTO-REALISTIC PARITY WITH THAT EXACT BUS.** Not "a convincing VW bus" — *that one*, the red
Señor Tacombi combi in the frames on this repo. **Any single measurement off is unacceptable,
per-measurement and not on average.** A model right in ninety places and wrong in one is not 99 %
done, because he will look straight at the one. **At rev 58 he did exactly that, at the emblem,
for the fifth time, while every automated check was green.**

**AND HERE IS THE HONEST DISTANCE.** `verify_clone.sh` ends **ALL 258 PASS** and its own verdict
block says what that is worth: **0 FIDELITY, 258 SELF-CONSISTENCY. Not one of those rows compares
the vehicle to a photograph.**

| gate | state at rev 58 |
|---|---|
| `flank_compare.py` | **runs, FAILS 1 of 4.** `Senor` **0.651** against a 0.75 bar. The deficit is the **artwork alpha and its placement**, not the render (F39) |
| `mottle_measure.py` | **runs, and it is NOT measuring the mottle** — 1.1–2.0 % of it. Rev 56's reading and rev 57's item B are REFUTED |
| `gloss_compare.py` | **runs, FAILS at 0.426** (bar 0.60). Mask corrected at rev 58 (F59); the model-side lever is now **exhausted** (F60/F62) |
| **`probe_rev46_vw.py`** | **NOW FAILS C6, and that is the point.** photograph 7 cream cells, built 6. It reported 0 FAILED for three revisions while the glyph was an X |
| `cream_rms.py` | `run()` is the LIVE re-based path |
| the badge STROKE WEIGHT | **CEILED-rev57.** Different finding from F63 |
| `visibility_budget.py` | the RANKING, not a gate |
| everything else | self-consistency |

**The frame reads as clay and the cause is the environment, not the shaders** — the surround is a
featureless white cyclorama, so the paint has nothing to reflect. **He was shown that, told the
cost, offered four routes, and ruled "keep studio, fix the model".** **Rev 58 MEASURED that
ceiling** (F62): this flank's specular image is white cyclorama **19.3 m** away. **Do not
re-litigate it.**

### §0.1 THE REFERENCE SET IS COMPLETE, AND IT IS GUARDED FRAME BY FRAME

> *[owner, rev 54]* **"we have all references that we need on repo and I want to make sure that is
> never forgotten."**

**ONE: WHAT WE HOLD IS WHAT WE GET. STOP PARKING WORK BEHIND A PHOTOGRAPH.** `PHOTOS_WANTED_*` is a
wish list, not a gate — carry it (rule 16, and items 1–5 are still not to be re-asked) but **do not
let it license parking an item.** Where a frame genuinely cannot answer, the result is *"it cannot
be recovered from what we hold"* — a real result, stated with its ceiling. **Rev 58 produced two:**
the residual gloss gap (F62) and the photograph's inability to resolve the V/W centre gap at 68 px.

**TWO: THEY CANNOT BE RE-SHOT, SO THEY ARE CHECKSUMMED INDIVIDUALLY.** **18 rows name them one at a
time**, so a loss says *which*:

* **the RED target bus** — `ref_side.jpg`, `ref_rear34.jpg`, `ref_playa_34.png`,
  `ref_nolita_front34.jpg`, `ref_nolita_front34b.jpg`, `ref_nolita_flank.jpg`,
  `ref_nolita_doorshut.jpg`, `IMG_2073.jpeg`
* **NOT the target, geometry only** — `ref_workshop.jpg` is the **GREEN** vehicle; `bus_model_ref.JPG`
  is a **SCHOOL BUS**, a fidelity bar only. **Paint and artwork do not transfer between vehicles;
  geometry does (rule 11).**
* **retired** — `ref_source.jpeg`, a 246×197 thumbnail the record itself retired
* **derived/annotated** — `ref_grid.png`, `ref_side_grid.png`, `ref_nose_grid.png`,
  `ref_band_grid.png`, `ref_x6_lanczos.png`
* a **floor of 54** reference-class tracked images, and **the five byte-identical pairs are asserted
  to stay five** — a sixth group means a frame arrived that duplicates one we already hold, which is
  **not corroboration** and has fooled this project before (rule 11).

---

## §1. START HERE — MEASURE THE BRANCH, DO NOT TRANSCRIBE IT

```bash
cd /home/user/combi_render
git fetch --unshallow 2>/dev/null || true
git fetch --all --prune
for b in $(git branch -r | grep -v HEAD); do
  printf "%-52s ahead %-3s behind %s\n" "$b" \
    "$(git rev-list --count origin/main..$b)" "$(git rev-list --count $b..origin/main)"
done
git diff --name-only HEAD...origin/main        # <- HIS PHOTOGRAPHS ARRIVE HERE
./bootstrap.sh          # ALL 10 PASS  -- THE BRANCH CHECK IS ROW 9
./verify_clone.sh       # ALL 258 PASS -- and read what its verdict block says
```

**AT PICKUP, REV 58 MEASURED:** rev 57 **was merged, through PR #17** — the **fourth** revision
running that the brief guessed the merge state and the machine corrected it. HEAD **0 ahead /
0 behind**, all **15** remote branches 0 ahead, `git diff --name-only HEAD...origin/main` **empty**,
`bootstrap.sh` 10/10 with row 9 passing.

**AND `fetch --prune` PRINTED `- [deleted] (none) -> origin/claude/combi-render-rev-58-lg0746`.**
That is the **EIGHTH** deletion in the rev-51…58 series and the **THIRD RUNNING** to hit the branch
the incoming brief named for the CURRENT revision, before that revision had pushed anything.
**Expect it at rev 59.**

**THE TOOLCHAIN WAS NOT ON THE CLONE AT REV 58.** `/tmp/blender/blender` did not exist and `bpy`
was not importable. `./bootstrap.sh` reproduced both and returned ALL 10 PASS; the
`pip install bpy==4.5.3` branch ran and worked. **Run bootstrap FIRST, before the render.**

> **ROW 9, NOT ROW 10** — row 8 clone depth, **row 9 "no branch carries work HEAD does not have"**,
> row 10 `verify_clone.sh`.

**RE-MEASURE BEFORE YOU FINISH, TOO.** `origin/main` moved mid-revision at rev 51 and rev 55, and
both times **row 9 was the only thing that caught it**. It did not move at rev 56, 57 or 58.

---

## §2. WHAT REV 58 DID

### §2.1 ITEM A0 — THE STUDIO RIG FACTORED, AND THE UNLIT CASE NOW REFUSES (F51)

The rig lived inside `build.py`'s `if T1_PREVIEW:`, so every tool that exec'd `build.py` to MEASURE
got an unlit scene, silently. **FIVE copies existed, not the two the record claimed** — the fifth,
`render_rev36_bumper.py`, was **incomplete** (no `cabin_fill`). All five now call `studio.rig()`.

**The duplication was the lesser half; the SILENCE was the one that bit.** `studio.assert_lit()`
refuses a scene with 0 lights and no world, from inside `render_set()`. **WATCHED FAILING** on
`T1_NORIG=1`. Emissive materials are deliberately not counted — the black bus HAD a lit bulb string.

**AND THE CONTROL IS THE LESSON.** Pre/post renders differed by max **41 DN** — which looks like a
regression. Two runs of the SAME code differ by max **41**, mean 0.469, against 0.473 old-vs-new.
**Cycles is nondeterministic at 4 spp and the refactor is inside that noise.** Without the control
this would have been published as a real change.

### §2.2 F58 — A VERIFIER ROW THAT PASSED ONLY IN THE TREE THAT WROTE IT

`ck "gloss_compare is exposure-free"` called the script with no argument; its default was a
hard-coded `out/r57_hero.png`, and **`out/` starts EMPTY on every clone**. The row passed for its
author and failed for everyone else, reporting the missing file as **`MOVED: []`** — an **ABSENT
INPUT dressed as a MOVED STATISTIC**. Fixed: exposure invariance is now a `--selftest` on a
synthetic patch through the real `spread()`. **WATCHED FAILING** via `T1_GC_ABSSPREAD=1`
(x0.70 **35.8691**, x1.00 **51.2416**, x1.40 **71.7382**, rc=1) — **and those three were typed as a
PREDICTION first and were wrong by two orders of magnitude.** Rule 5, caught by obeying rule 5.

### §2.3 ITEM A — THE GLOSS: LEVER TAKEN, CEILING MEASURED

**F59 — the gate's HEADROOM was a third artwork.** The red mask is 95.0 % body red (so the raw
rectangle's 42.9 % red fraction **overstates** it — stated because it was my first reading and it
was wrong), but 3.4 % is gold ink and it is the BRIGHT 3.4 %. Excluding it: **SPREAD +0.6 %** (the
headline is ROBUST — the ratio reads 0.3918 loose against 0.3911 tight), **HEADROOM −31.6 %**. The render's headroom is **0.090** of the photograph's,
not the 0.132 published at rev 57b. **The correction makes the deficit worse.**

**F60 — roughness is the live lever, 16× the clearcoat, and it SATURATES.** The live path is the
**WEATHER group's own `Roughness` input** (the BSDF socket is LINKED — F53), traced through
`t1_mats.py`. Ablated before tuned:

| rgh | ratio | headroom | G/R |
|---|---|---|---|
| 0.420 was shipped | 0.3911 | 0.0899 | 0.4315 |
| **0.250 ships now** | **0.4261** | **0.1458** | 0.4364 |
| 0.050 extreme | 0.4233 | 0.1408 | 0.4451 |

**OWNER RULING: "ship 0.250".** Control: the shipped constant reproduces the probe's override to
**−0.07 % / −0.51 % / +0.04 %**.

**AND THE TWO CHROMA INSTRUMENTS DISAGREE IN SIGN — reported, not picked.** The hero window says
G/R +1.1 % **away** from the photograph; `flank_compare`'s flank annulus says 0.461 → **0.423**,
−8.2 % **towards** it. Different pixels at different incidence. The +1.1 % is the pessimistic one
and it is what the owner was quoted.

**F61 / F62 — the rig arm measures the wrong thing.** Small bright sources add **FILL**: 3 × 250 W
moved the gate **backwards** (0.4261 → 0.3435). At the arm's **own shipped default** 3 × 4000 W the
panel washed out and the gate **refused** it — that default had never been run. **F62** says why,
off the shipped camera: the hero camera is at **(8.156, 5.603, 1.307)**, near flank height, and the
mirror direction **(−0.8564, +0.5155, −0.0281)** strikes the floor **19.3 m outboard**. The flank's
specular image is featureless cyclorama. **The model-side lever is exhausted at 0.4261.**

### §2.4 THE OWNER REDIRECTED — F63/F64/F65

**F63 — the glyph builds as an X**, in the project's own rasteriser. W outer arm tips reach
**0.6638** against a band inner of **0.7988** — floating **18.9 mm** on a 140.1 mm radius, while the
V's tips (0.8400) and the W's legs (0.8394) are on the band.

**F64 — why the solver could not see it:** every landmark it fits is a **VERTICAL position**; none
is a **RADIUS**. Rev 46's own *"the axis nobody checked"*, recurring on the axis rev 46 did not
check. Its vertical fit still holds (residual 0.0347 vs rev 45's 0.1167) and is **not** discarded.
**Mechanism, traced:** a cap is cut PERPENDICULAR to its stroke; `vw_bars`' fixed point drives the
**MAX** corner onto the band, leaving the other short by the cap's radial span; the W's outer arm
meets the ring at **0.12°** while travelling at **55.5°**, so that span is **0.176 R**. Then
`vw_logo_fit` re-normalises by the **GLOBAL EXTREME** — rev 44b's own mechanism, still live one
stage below where rev 44b fixed it.

**GATED — C6:** photograph **7** cream cells, built **6**. A stroke that fails to reach the ring
merges the two cells either side of it. Structural, needs no axis ratio, survives blur, and **one
function reads both frames**. **WATCHED FAILING**; its KILL moves the count **6 → 4**.

**F65 — three fixes tried, all failed, none shipped:** drive the MIN corner (6 → **4**); make
`vw_logo_fit` a pure unit conversion (6 → **4**); `VW_W_ARM_Z` 0.0019 → 0.30/0.55/0.772
(**6, 6, 6**). **The V's arms and the W's outer arms cross the same region BY CONSTRUCTION** — this
is a **re-solve of the W's spine against reach**, not a one-constant tweak. Both files are back at
HEAD.

### §2.5 REFUTED AT REV 58 / STILL REFUTED — DO NOT REBUILD THESE

* **"the glyph is a legible V over W at full size"** — **REFUTED, F63.** Rev 57 closed F40 on a
  crop; the project's own rasteriser draws an X. **F40's closure was wrong.**
* **"`probe_rev46_vw.py` clears the emblem"** — **REFUTED.** It fits one axis and is blind to the other.
* **"the clearcoat is item A's lever"** — refuted at rev 57b (F54), and now **superseded**:
  roughness is, at 16× the gloss for a fifth of the chroma cost (F60).
* **"`T1_GL_SPOT` measures the rig ceiling"** — **REFUTED, F61.** It adds fill and moves the gate
  backwards; its own default refuses.
* **"the render's headroom is 0.132 of the photograph's"** — **REFUTED, F59.** It is **0.090**;
  the rest was gold ink.
* **"the mottle is the lever"** / **"`mottle_measure`'s albedo arm is about the mottle"** — still
  refuted (rev 57).
* **"the `Senor` deficit might be the render"** — still refuted; it is the artwork.
* Everything rev 50–57 refuted — all still refuted, including the 2.3 % instrument conflict;
  `flank_kv`'s quadratic carry law; "the render's flank lockup is short in height"; `LID_W ≤ 1.2797 m`;
  A7's aft wall; `gal_end_f` widened to `REAR_W/2`.
* **§2b of the rev-52 brief — HIS SETTLED RULINGS — IS UNCHANGED AND STILL BINDING.** W6 (keep the
  studio rig; **a G/R shortfall on any surface is NOT a paint error**); the roof strips' 0.3 m
  retired; the wipers withdrawn entire, commented not deleted; the lower bay SHUT; the RED bus is
  the target and **paint and artwork do not transfer between vehicles**; the tail board IS on the
  vehicle; the marks above the burst are STARS. **Do not re-open or re-ask any of them.**
  `playa_env.py` is not on the table. **And rev 54's ruling stands: "Keep studio, fix the model".**

---

## §3. THE WORK LIST FOR REV 59

### §3.1 ITEM A IN DETAIL — THE EMBLEM, AND WHAT NOT TO RE-TRY

**Run the gate first and read its own summary line, never its exit code (rule 9):**

```bash
T1_SUB=1 /tmp/blender/blender -b -P probe_rev46_vw.py     # C6 FAILS today: photo 7, built 6
```

**DO NOT re-try F65's three.** They are recorded precisely so a revision is not spent on them again.

**WHAT THE EVIDENCE SAYS THE JOB IS.** The V's arms and the W's outer arms sweep the same region in
opposite senses, so thickening or re-radiusing either one cannot separate them. The W's spine must
be re-solved so that (a) every terminal meets the ring **radially** — its own direction of travel
equal to its angle from centre, which is a fixed point, not a constant — and (b) the vertical
landmarks L1–L6 still land. **Both axes in one objective.** `probe_rev46_vw.py` already has the
solver (`T1_VW_SOLVE=1`, coordinate descent) and now has the reach measure; **the missing piece is
putting `cream_cells` into `err()` and re-running it.** Then update the seven `verify_clone` rows
that pin the constants BY VALUE, and **LOOK at the raster before you believe any of it.**

**AND THE CONSTRAINT THAT MAY BITE:** at rev 58 no setting of the existing six parameters produced
7 cells. If the re-solve also cannot, **say so with the number** — *"the current spine family cannot
reach the photograph's topology"* is a real result and would mean the W needs a different
parameterisation, not a better search.

### §3.2 ITEM B IN DETAIL — THE NOSE, POSE-MATCHED

**This is a LEAD, not a finding, and the difference matters** — rev 55's "X" dissolved twice off
un-pose-matched crops. The job is to build the comparison, not to declare a defect from one:
recover `ref_nolita_front34.jpg`'s camera, render **that** view, and compare the cream/red boundary
and the lamp positions. `studio.py` and `flank_compare.py` both already carry recovered cameras —
and **rule 34 applies**: `flank_compare.py`'s header attributes a camera to `ref_side.jpg` that
`studio.py` attributes to the PLAYA frame (**F26, still open**). Check which frame a camera belongs
to before leaning on it.

### §3.3 ITEM C — THE UNTEXTURED INTERIORS (F45)

**7.4 × 10⁵ px², ungated, never measured, and plainly visible in `out/r58b_hero.png`.** The galley
and roof-aperture interiors read as white blocks through four openings, dead centre. Build one, or
accept it and say so with its ceiling.

### §3.4 ITEM E — THE MOTTLE GATE, AND WHAT REV 57 HANDS YOU

`mottle_measure.py`'s albedo arm is a **working instrument with a known meaning**, and **1.1–2.0 %
of what it sees is the mottle.** The remaining candidates are the paint's other spatial terms, all
in the same `apply_weather(...)` call. **Ablate them one at a time** — `dust`/`wear`/`peel` —
exactly as rev 57 ablated the mottle. `out/mottle_alb*.png` is keyed by `MOTTLE_AMP`, so **give each
ablation its own filename or it overwrites the last one.** Run at **`T1_MM_SAMP=16`**, not 64.

**AND F05 IS CHEAP NOW.** The beauty arm was dead because `shader_solve._render()` built no rig —
that was F51, **fixed at rev 58**. `studio.rig()` exists and `assert_lit()` will refuse if it is not
called. Wiring the beauty arm is now a small job, and it is the only arm that can see the
**roughness** half of the mottle (F41).

### §3.5 THE mm AXIS — STILL NOT ATTEMPTED, THREE REVISIONS RUNNING

`PXM_REF = 337.0` px/m is a **bracket** (330–344), not a measurement, and it sets the mm axis of
every render-to-photograph figure in millimetres. *(Rev 55's correction stands: `depth_correct()` is
defined NOWHERE in this repo.)* Render-against-render ablations do **not** depend on it.

### §3.6 FINISH A9, AND THE THREE HOLES REV 52 LEFT OPEN

**A9: two of four parts done; the galley is still ~103 mm too far aft. PROVENANCE, GRADED: the
per-feature deltas are INHERITED from the rev-52 brief and have NOT been re-measured at rev 52–58.**
The offset is **NOT rigid** (−0.09574 at hook u=0.13 to −0.11035 at `gal_appliance` u=0.80, so one
additive constant leaves ±7.3 mm). Re-derive each X from `BAYS`.

**THE THREE HOLES.** F11–F13 reproduce exactly. **F14's 260.0 mm and 20.0 mm sight lines are rev
52's and have NOT been re-measured since — SIX revisions, well past §8's decay rule.**
* `gal_end_f` needs its own sight line established first — **do not inherit `REAR_W/2`** (rule 34).
* The **sixth hook at X −0.907 lies 51.25 mm beyond `BAYS[2]`'s aft edge**; the hook span centre is
  **−0.7050** against the rail's **−0.5980** — **107.0 mm**. They disagree and one is wrong.
* A7's real defect: `roof_cutters()`'s aft edge is `LID_X1`, **not greppable as `LID_X1 = -1.0700`**
  — the source line is `LID_X0, LID_X1 = 0.9640, -1.0700` in `t1_shell.py`. **803 mm** of roofed
  body sits unlit between the last light inlet and the tail. A7 is **ILLUMINATION, not dressing.**

### §3.7 A13 / A16 / A12, A11's SECTION, A14, AND THE CHEAP COLOUR ITEM

**A13 / A16 / A12** — the isolated star built BELOW the burst where both red frames put it above;
every flank rosette drawn at the diameter of its **gold core**; *A12 is an OWNER RULING, not a
do-now* — `senor_trace.py` calls the remedy *"inventing ink the photograph does not show"*.

**A11's SECTION, A14** — a chrome lever lying in a dish **pressed into** the skin against a 12 mm
**proud** prism.

**A CHEAP UNBLOCKED ITEM, STILL NOT DONE AFTER SEVEN REVISIONS:** `SPEC` §8's colour locks are all
graded **M** = *"measured by me from `ref_source.jpeg`"* — a 246×197 thumbnail the record itself
calls retired. They can be re-derived on `ref_playa_34.png` at **4× the area** with no new
photograph. **Report the re-derived values; do not change the constants without his ruling** — W6
makes colour his call. *(`ref_playa_34.png` is byte-identical to `IMG_3842.png`; a duplicate is not
corroboration — rule 11.)*

### §3.8 THE PROCESS ROWS, STILL OPEN

`OPEN_FINDINGS.md` is the register — see §8; the standing-instructions carrier deleted at rev 44,
which took the **die-cut sticker — the project's original deliverable** — with it, **still open and
carried as F18**; SPEC §0.2's two rev-4 corrections later refuted; rev 48's refuted *"B stays
open"* still live in `build.py` and, **split across two lines so a flat grep misses it**, in
`t1_shell.py`; the tail board still has **zero rows in either verifier**.

### §3.9 THE HABITS THAT PAID AT REV 58

**LOOK AT THE FRAME, AND AT THE RASTER.** F63 was found by rendering the badge at the photograph's
own scale and putting the two side by side. Every number in this repo said it was fine.

**ABLATE BEFORE YOU TUNE (rule 36).** F60's sweep ran before a single constant was changed, and it
showed the lever saturates at 0.250 — so 0.050 was never shipped.

**RUN THE CONTROL BEFORE YOU CALL SOMETHING A REGRESSION.** The rig refactor "changed" the render by
41 DN. So does re-running the same code.

**PAINT THE WINDOW AND LOOK AT IT — THEN SAY SO WHEN YOUR FIRST READING WAS WRONG.** The gloss
rectangle is 42.9 % red, which looked damning; the MASK is 95.0 % red and the headline survived.
The real defect was 3.4 % of ink sitting in the p99. **Both halves are in the record.**

**WHEN AN INSTRUMENT AND THE OWNER DISAGREE, THE INSTRUMENT IS THE SUSPECT.** He has reported this
emblem five times against "0 FAILED".

---

## §4. WHAT WAS ASKED OF HIM — A CARRIER, NOT A LIST OF BLOCKERS

> **READ §0.1 FIRST.** At rev 54 he ruled that **the reference set on the repo is complete**. This
> section is kept in full because `CLAUDE.md` rule 16 forbids dropping a carrier, and because it
> records what was asked and what was refused — which is why items 1–5 must never be re-asked.
> **But it is no longer a licence to park work.**

**`PHOTOS_WANTED_rev52.md` is the carrier for item 7 (ONE HUBCAP, SQUARE ON AND CLOSE)**. Items
**1–5** keep their full text in `PHOTOS_WANTED_rev49.md`: the tail board's footing; the decal darker;
the nose square on; a raking-light frame of the louvres (**ONE item — the pressing depth**); the off
side, any frame. **He has said 1–5 are not possible now. DO NOT RE-ASK THEM.** Item 6 (an obliquely
seen wheel) was **DISSOLVED at rev 51** — struck, not outstanding.

**CARRIED FROM REV 53, still no carrier outside these briefs:** a frame showing the cream **where it
IS chipped**. Rev 54 and rev 55 both lowered its urgency; the band is 0.27 px at every scale this
project ships, and the gate that would place those chips is not built.

**ANSWERED AT REV 56 AND NOT TO BE RE-ASKED:** `lid_rail`'s width — *"narrow lip, ~as wide as it is
tall"*.

**ASKED AND ANSWERED AT REV 58:** the roughness/chroma trade — **"ship 0.250"** (F60). That is the
only thing put to him, and it was put as multiple choice with the crop attached.

**AND HE VOLUNTEERED TWO INSTRUCTIONS AT REV 58, BOTH BINDING:** the emblem needs a fix (F63, item
A), and **the full delivery render waits until the model is right.**

**STILL WORTH HIS TIME AND NOT ASKED:** **F38** — the built nose ring band sits at the top of its
adopted range (0.10086 against three frame readings at 0.087–0.093), and moving it moves the glyph's
fit radius with it, **which now interacts with F63**; and **F39** — `Senor`'s ink deficit is in the
artwork, which A12 makes his call. **Decide whether to ask. Do not simply carry them.**

---

## §5. THE RULES — `CLAUDE.md` CARRIES THE METHOD, NOT THE NUMBERED CANON

The canon (rules 1–33) is printed in `NEXT_CONTEXT_PROMPT_rev50.md` §11. **Rules 34–36 live only in
the rev-51…58 briefs and `LEDGER_rev50.md` §0, so they are carried here too — that is `CLAUDE.md`'s
own rule 16 firing on this file:**

> **34. A REQUIREMENT INHERITS ITS OBJECT EXACTLY AS A RETIREMENT DOES.** Before relying on any
> *"the record requires X"*, check which object the sentence is about — and check the cited line
> exists. **Rev 56 applied it to a CAMERA**: `flank_compare.py`'s header attributes a recovered
> camera position to `ref_side.jpg` that `studio.py` attributes to the PLAYA frame — the same three
> numbers in two places about two photographs (**F26, still open**). **Check it before any future
> work leans on that camera — item B does.**

> **35. A GUARD WRITTEN AGAINST A POSE ENCODES THAT POSE.** Guards that identify a part's foot or
> free edge by `min(y)` are only right while the part leans one way. Ask the geometry.

> **36. A GATE ONLY COUNTS FOR WHAT IT CAN SEE — ABLATE THE THING YOU ARE ABOUT TO TUNE, FIRST.**
> Earned at rev 57 and it cost that revision's item B. **Rev 58 extends it: a gate can be blind to a
> whole AXIS, not just to one constant.** `probe_rev46_vw.py` fits vertical landmarks and reported
> 0 FAILED for three revisions while the glyph was an X, because reach is a radius and every
> landmark it owns is a row (**F64**). **When you build a gate, write down which axes it does NOT
> see.**

> **37. NEW AT REV 58 — AN ABSENT INPUT MUST NEVER READ AS A MEASUREMENT.** `gloss_compare`'s
> missing default frame came back as `MOVED: []`, i.e. *"the estimator moved"*, and pointed the
> reader at the statistic instead of the path (**F58**). A probe that cannot run must say **"NO
> RENDER"** in those words and exit non-zero. **And a check whose input lives in an untracked
> directory passes only in the tree that wrote it.**

> **Rule 29.3:** no finding is attributed to a cause until a control separates it. **Rule 15:** a
> retraction that lands in a ledger and not in the source is half a retraction — **rev 58 retracted
> F47 in `t1_mats.py` itself.**

---

## §6. THIS MACHINE

```
cores 4   RAM 15 GB   Blender 4.5.3 via pip install bpy   subagent concurrency 2
build  T1_SUB=1 ~20 s     render 1600x1100 96 spp ~4.5-5.5 min PER VIEW
mottle_measure.py (albedo arm, 64 spp) ~4.8 min PER RUN -- budget ablations in fives
```

```bash
./bootstrap.sh                                               # THE TOOLCHAIN IS NOT ON THE CLONE
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
T1_PREVIEW=side,hero T1_PFX=r59 T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
  /tmp/blender/blender -b -P build.py     # BOTH views, ONE build.  It takes a LIST.
T1_RIG=1 ... /tmp/blender/blender -b -P build.py             # rev 58: build the rig WITHOUT a preview
T1_NORIG=1 ...                                               # the ABLATION -- assert_lit must REFUSE
T1_SUB=2 /tmp/blender/blender -b -P audit.py                 # rewrites STATE.md -- COMMIT FIRST
python3 lid_gen.py                                           # regenerates tex/lidmural.png
python3 flank_compare.py out/r59_side.png /tmp/fc.png        # GATE 1.  FAILS 1 of 4 today.
python3 gloss_compare.py out/r59_hero.png                    # GATE 3.  FAILS at 0.426 today.
python3 gloss_compare.py --selftest                          # exposure invariance, NO frame needed
python3 visibility_budget.py 3840                            # THE RANKING.  Run it before choosing.
T1_SUB=1 /tmp/blender/blender -b -P probe_rev46_vw.py        # ITEM A.  C6 FAILS: photo 7, built 6.
T1_SUB=1 T1_VW_SOLVE=1 /tmp/blender/blender -b -P probe_rev46_vw.py   # the solver
T1_SUB=1 T1_GL_WRGH=0.25 T1_GL_PFX=w25 T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
  /tmp/blender/blender -b -P probe_rev58_gloss.py            # ITEM A's roughness arm, changes NO source
python3 cream_rms.py                                         # the LIVE photograph-side cream
T1_SUB=1 T1_MM_ALBEDO=1 T1_MM_SAMP=16 /tmp/blender/blender -b -P mottle_measure.py  # GATE 2
#   ^ 16, NOT the default 64.  Rev 56 measured this statistic stable across 16/32/48.
python3 audit_brief.py                                       # rule 17's MECHANICAL half
python3 audit_adversary.py                                   # rule 15's adversary -- REPLACE its questions
```

**`out/` IS NOT TRACKED and starts empty. Render before quoting any probe that reads a frame.**
**A backgrounded runner's exit code is the WRAPPER'S, not Blender's — grep the log for `Saved:`.**
**`probe_rev54_aov.py` and `probe_rev55_truenorm.py` write EXR into `probe_scratch/` — delete them
before committing and keep the PNGs.**
**`mottle_measure.py`'s BEAUTY arm REFUSES (100 % clipped) — but F51 is FIXED now, so wiring it is
cheap (§3.4).**
**`mottle_measure.py` names its output by `MOTTLE_AMP`, so two runs that differ in `MOTTLE_M`
OVERWRITE EACH OTHER'S PNG.**
**EVERY MEASUREMENT THROUGH `shader_solve._render` IS 8-BIT (F42), whatever `color_depth` says.**

**THE DELIVERY FRAME — DO NOT RUN IT UNTIL THE MODEL IS RIGHT (owner, rev 58).**

```bash
T1_SUB=2 /tmp/blender/blender -b -P hq_render.py      # ONE build, 10 bands, WITH MARGIN
python3 stitch.py out/hq_hero_raw.png 0.0000,0.1000=out/hq0_hero.png ...   # DECLARED spans
#   ^^ CHECK ITS EXIT CODE.  It exits 2 on a seam and it MEANS it (F49).
python3 post.py out/hq_hero_raw.png out/hq_hero.png   # optics LAST, never per strip
```

3840×2640, 256 spp, SUB=2, **106.8 min**. `probe_scratch/rev57b_delivery_hq_hero.png` (1600 px) is
the tracked baseline; the full frame is **not** tracked and that is deliberate. The guard is
narrowed **by DIMENSION, not by name** — tracked hero PNGs must be ≤ 1600 px wide.

**ABLATIONS — every one exists to WATCH A GUARD FAIL.**
**NEW AT REV 58:** **`T1_NORIG`** (suppresses the rig; `assert_lit` must refuse — watched),
**`T1_RIG`** (build the rig without asking for a preview), **`T1_GC_ABSSPREAD`** (drops the `/p50`;
the exposure selftest must FAIL — watched), **`T1_GC_LOOSEMASK`** (restores the gloss gate's old
ink-contaminated mask), **`T1_GL_WRGH`** (the WEATHER group's roughness — item A's live lever),
**`T1_BODY_RGH`** (the shipped body roughness), **`T1_GL_DARK`** (the dark-card rig-ceiling arm —
it lands IN FRAME, which is the measurement).
Carried: `T1_GL_SPOT` (**refuted as a ceiling measure, F61**), `T1_GL_COATW`/`T1_GL_COATR`
(**refuted as a route, F54**), `T1_MOT_AMP`/`T1_MOT_M`/`T1_MOT_RGH`/`T1_MOT_DET`, `T1_FC_KVQUAD`,
`T1_RAILFLAT`, `T1_CR_LEGACY`, `T1_FC_INKGAIN`, `T1_FC_ZSTRETCH`, `T1_TRUENORM` (**a
DEMONSTRATION, not a fix**), `T1_PTWEAR`, `T1_EDGERAD`, `T1_MM_ALBEDO`, `T1_SOLVE_NODENOISE`,
`T1_TARNCONTAM`, `T1_RAILSTALE`, `T1_ENDSHORT`, `T1_CAPSINK`, `T1_LIDDEG`, `T1_BAYSTALE`,
`T1_LAMPSINK`, `T1_LIDASPECT`, `T1_HANDLEHI`, `T1_BAREMAT`, `T1_TBFOOT`, `T1_BAYPROUD`,
`T1_NOBEVEL`, `T1_BEVEL_SAMPLES`, `T1_FC_OLDDATUM`.

---

## §7. THE STANDARD, IN HIS WORDS

We are recreating a photorealistic version of **that exact bus**, and **any single measurement off is
unacceptable** — per-measurement, not on average. A model right in ninety places and wrong in one is
not 99 % done, because he will look straight at the one. **He did, at rev 58, at the emblem.**

`bus_model_ref.JPG` is a **SCHOOL BUS** and is **NOT the vehicle** — a FIDELITY BAR only. Use
`ref_workshop.jpg` the same way, and remember it has **no headlamps and no hubcaps fitted** and is
the **GREEN** vehicle (§4).

**Ground in the reference, build, adversarially audit, iterate.** Never build before grounding. Never
call it done off self-review. Report the measurement **with its ceiling**, never a self-assigned
score. Do not say anything is ready — say what is fixed, what is still wrong, and what you measured.

**RENDER IT, CROP IT, AND LOOK AT IT, before and after every change.** Every defect this project has
shipped passed `VERIFY: 0 fail, 0 warn` and was found by looking at a crop. **At rev 58 it was found
by rasterising the badge at the photograph's own scale and putting the two side by side.**

**When you need something from him, ask as MULTIPLE CHOICE with the reference material attached — one
crop, one mark, one sentence — and ASK IT WITH THE QUESTION TOOL.**

---

## §8. THE OPEN-FINDINGS REGISTER — `OPEN_FINDINGS.md`

**A register existed once and was ABANDONED AT REV 45 WITH 21 ROWS**, and nobody noticed for eleven
revisions. Rev 56 reinstated it; it carries **65 rows** now.

**IT IS A CARRIER (rule 16). Rows leave it only by being CLOSED with the measurement that closed
them, or RETIRED with the ruling that retired them. Never by being dropped.**

**THE POINT OF THE FILE IS THE PROVENANCE GRADE, NOT THE LIST.** This project's recurring failure is
**re-quoting inherited numbers as though they had been measured**. An `INHERITED` row is a claim.

**GRADE DECAY IS ITSELF A FINDING.** An `INHERITED` row that survives three more revisions without
being re-measured should be re-measured or downgraded.

**REV 58 ADDED EIGHT AND MOVED TWO.** Added: **F58** (the clone-only verifier row), **F59** (the
gate's headroom was a third artwork), **F60** (roughness, the live lever), **F61** (the rig arm
measures fill), **F62** (what the flank reflects, 19.3 m out), **F63** (the glyph is an X), **F64**
(the solver's blind axis), **F65** (three fixes that failed). Moved: **F44** partly closed,
**F51** closed.

**AND ONE CLOSURE FROM AN EARLIER REVISION IS NOW WRONG: F40** (*"the roundel reads as an X"* —
closed twice, at rev 55 and rev 57). **It was closed on a crop; the project's own rasteriser draws
an X.** F63 supersedes it.

**WHAT IS STILL INHERITED AND OLDEST:** **F14** (`gal_end_f`'s 260.0 / 20.0 mm sight lines, **rev
52 — SIX revisions un-re-measured**), F15 (A7's 803 mm, rev 52), F20 (the colour locks, rev 52),
F10 (the galley offset, rev 52), F18 (the die-cut sticker, rev 44 — **the oldest thing in the file**).

---

## §9. THE HORIZON BEYOND REV 59

**Rev 59's own order is §0.0. This section is the longer arc.** It is a CARRIER: each revision should
re-rank it, not rewrite it, and **say what moved**.

**WHAT MOVED AT REV 58.** The **owner** re-ranked the table, which no previous revision's horizon
had allowed for: the emblem was *"parked, CEILED, 1.4 px²"* under F08 and is now **item A** under
F63 — because **they are different findings** and only one of them was ceiled. Item A's gloss moved
from *"next"* to **partly closed with a measured ceiling** (F60/F62). F05 became **cheap** because
F51 was fixed.

| horizon | the work | worth | why it is in this order |
|---|---|---|---|
| **next** | **F63 — the glyph builds as an X.** Gated, failing, and his fifth report | he looks straight at it | The owner ranked it, and the owner outranks the budget |
| **next** | **the nose beyond the emblem**, pose-matched | — | A lead that needs an instrument before it needs an opinion |
| **next** | **F45 — the untextured galley and roof-aperture interiors** | 7.4 × 10⁵ px² | Bright, central, seen through four openings, pure placeholder |
| **next** | **F15 — A7.** Illumination, not dressing | 8.2 × 10⁵ px² | A large unlit region changes how the whole rear reads |
| **near** | **F01/F39 — `Senor`**, the artwork alpha and its placement | 2.7 × 10⁴ px² | Small but HARD-EDGED, so it reads louder per pixel than the table implies |
| **near** | **F43/F05/F41 — the cream's albedo texture and the beauty arm** | large area, subtle | **F05 is cheap now that F51 is fixed** |
| **near** | **F42 — the 8-bit reader.** Decoder written and controlled | — | Cheap; lifts every consumer of `_render`. Re-run them all in the same revision |
| **then** | **F10–F14 — the galley cluster.** F14 is SIX revisions INHERITED | 6.8 × 10³ px² | Re-derive each X from `BAYS` |
| **then** | **F02/F06 — the two absolute scales** | — | Every render-to-photograph figure in millimetres runs through a bracket |
| **parked** | **F08 — the badge STROKE WEIGHT. CEILED-rev57** | **1.4 px²** | **Not F63.** Needs a new frame or a pressing model |
| **later** | **F19** the red's edge wear; **F16/F17/F20/F23–F28, F37/F38** | — | Unblocked but ungated, or a decision rather than a measurement |
| **standing** | **F18 — the die-cut sticker** | — | The original deliverable. No gate, no owner ruling, open since rev 44 |

## §10. HOW TO GROW THIS HANDOFF WITHOUT BREAKING IT

1. **The set is three files.** `LEDGER_rev<N>.md`, `NEXT_CONTEXT_PROMPT_rev<N+1>.md`, and **`cp` of
   that file over `PASTE_INTO_CLAUDE_CODE.txt` IN THE SAME COMMIT.** `CLAUDE.md` imports the `.txt`
   into every session and a byte-identity row fails if you forget. *(The `HANDOFF_rev*.md` series
   ended at rev 45; do not restart it.)*
2. **`README.md` and `START_HERE.md` name the newest brief BY NUMBER.** Two rows check it.
3. **THE ROW COUNT IS SELF-REFERENTIAL — AND IT IS AUTOMATED, SO STOP HAND-EDITING IT.**
   `python3 audit_brief.py --fix-count` writes the clean-tree total into the brief AND into
   `PASTE_INTO_CLAUDE_CODE.txt`. **Every row you add changes the number the brief must state**, so
   write the count LAST and grep for the bare number afterwards, not just the phrase.
4. **ADD ROWS ANCHORED ON ARITHMETIC OR BEHAVIOUR, NOT ON A GREP.** A grep passes on a comment.
   **Rev 58 broke this and was caught by it in the same session:** a new row meant to forbid a
   revision-numbered default frame matched **its own explanatory comment** and reported the
   explanation as the defect — the **fifth** time a row in that file has done exactly that. It is
   tokenised now. **When you write a row about a string, strip comments first.**
5. **RUN BOTH AUDITS, AS SCRIPTS, AND RECORD WHAT THEY FOUND *IN* THE BRIEF.** `audit_brief.py`
   asks *"is what the file says true?"*; `audit_adversary.py` asks *"what would make it false?"*
   **REPLACE the adversary's questions each revision** — a question that can no longer fail is not
   a control.
6. **NEVER DELETE A CARRIER.** §0, §0.1, §4, §5, §8 and §9 are carriers.
7. **RANK BEFORE YOU CHOOSE** — `python3 visibility_budget.py`. **But the owner outranks it**, and
   at rev 58 he used that. If you work an item the script puts in the bottom half, say why.
8. **NEVER RELAX ONE COPY OF A CHECK.** `audit_brief.py` and `verify_clone.sh` assert some of the
   same things. **Loosen both or neither**, and when a check fails on code you just wrote, suspect
   the code first.
9. **DO NOT LET THE MACHINE IDLE.** Blender is CPU-bound and must not be fanned out. **Run
   `bootstrap.sh` first** — the toolchain was absent at rev 58 — then launch the render, then read.
10. **ROOM TO GROW:** new findings go in `OPEN_FINDINGS.md` with an ID and a grade, not into this
   file's prose. This file points AT the register.
