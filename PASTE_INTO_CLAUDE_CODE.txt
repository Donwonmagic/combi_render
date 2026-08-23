# NEXT CONTEXT PROMPT — rev 57

**Read this whole file before you touch anything.** Then `CLAUDE.md` (method only, loads every
session), then `LEDGER_rev56.md` — which is where every number below comes from — then
`SURVEY_rev49_photoreal.md` §6, still the work list.

---

## §0. THE GOAL, AND HOW FAR OFF IT WE ACTUALLY ARE

**CARRIED FORWARD FROM THE REV-55 AND REV-56 BRIEFS. It is not mine and it is not to be
dropped — rule 16.**

**PHOTO-REALISTIC PARITY WITH THAT EXACT BUS.** Not "a convincing VW bus" — *that one*, the red
Señor Tacombi combi in the frames on this repo. **Any single measurement off is unacceptable,
per-measurement and not on average.** A model right in ninety places and wrong in one is not 99 %
done, because he will look straight at the one. This paragraph is first because every revision has
drifted toward whatever was measurable that week, and the goal is not "add rows".

**AND HERE IS THE HONEST DISTANCE, MEASURED AT REV 56.** `verify_clone.sh` ends **ALL 227 PASS** and
its own verdict block says what that is worth: **0 FIDELITY, 221 SELF-CONSISTENCY. Not one of those
rows compares the vehicle to a photograph.** The parity question rests on **two** scripts, and at
rev 56 **both of them run** for the first time:

| gate | state at rev 56 |
|---|---|
| `flank_compare.py` | **runs, FAILS 1 of 4** (was 2 of 4). The aspect row is CLOSED — it was an instrument, and the instrument is fixed (§2.1). The `Senor` worst-region row is still open at **0.644** against a 0.75 bar |
| `mottle_measure.py` | **RUNS, and it is a live fidelity comparison** (§2.3). Its beauty arm was DEAD — 100 % clipped, five printed `ratio 0.00` rows — and now refuses; its ALBEDO arm gives a real spectrum against the photograph |
| `cream_rms.py` | `run()` is the LIVE re-based path now, not the dead `ref_side.jpg` one |
| everything else | self-consistency |

**So parity is now measured by TWO working gates instead of one, and both have something to say.**
Adding a 222nd self-consistency row is still not progress toward the goal.

**The frame reads as clay and the cause is the environment, not the shaders** — the surround is a
featureless white cyclorama, so the paint has nothing to reflect. **He was shown that, told the cost,
offered four routes, and ruled "keep studio, fix the model".** Parity is to be won on the MODEL, with
that rig. **Do not re-litigate it.**

### §0.1 THE REFERENCE SET IS COMPLETE, AND IT IS GUARDED FRAME BY FRAME

> *[owner, rev 54]* **"we have all references that we need on repo and I want to make sure that is
> never forgotten."**

**Read that as two instructions and obey both.**

**ONE: WHAT WE HOLD IS WHAT WE GET. STOP PARKING WORK BEHIND A PHOTOGRAPH.** For five revisions the
top job has been logged as *"blocked on a photograph"*. It is not blocked; it is **hard**.
`PHOTOS_WANTED_*` is a wish list, not a gate — carry it (rule 16, and items 1–5 are still not to be
re-asked) but **do not let it license parking an item.** Rev 54 found a live route to the badge
stroke weight in frames already on this repo and did not take it; **rev 55 did not take it; REV 56
DID NOT TAKE IT EITHER, and that is rev 56's clearest omission against this instruction.** Three
revisions running. **TAKE IT** (§3.3). Where a frame genuinely cannot answer, the result is *"it
cannot be recovered from what we hold"* — a real result, stated with its ceiling. Rev 56 produced
two such results honestly: the flank plane's absolute scale (§2.2) and the front rim disc (§2.4).

**TWO: THEY CANNOT BE RE-SHOT, SO THEY ARE CHECKSUMMED INDIVIDUALLY.** **18 rows name them one at a
time**, so a loss says *which*:

* **the RED target bus** — `ref_side.jpg`, `ref_rear34.jpg`, `ref_playa_34.png`,
  `ref_nolita_front34.jpg`, `ref_nolita_front34b.jpg`, `ref_nolita_flank.jpg`,
  `ref_nolita_doorshut.jpg`, `IMG_2073.jpeg`
* **NOT the target, geometry only** — `ref_workshop.jpg` is the **GREEN** vehicle; `bus_model_ref.JPG`
  is a **SCHOOL BUS**, a fidelity bar only. **Paint and artwork do not transfer between vehicles;
  geometry does (rule 11).** Rev 56 leaned on exactly that distinction to accept the owner's
  `lid_rail` ruling off `ref_workshop.jpg` — a structural member, not a colour (§2.5).
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
./verify_clone.sh       # ALL 227 PASS -- and read what its verdict block says
```

**AT PICKUP, REV 56 MEASURED:** rev 55 **was merged**, through **PR #14 and PR #15** — **not** the
"no PR opened, because none was asked for" that the rev-56 brief predicted. **The brief was wrong
and the machine was right, which is exactly why §1 says measure.** HEAD **0 ahead / 0 behind**
`origin/main`, every remote branch **0 ahead**, `git diff --name-only HEAD...origin/main` **empty**
(no photographs arrived), `bootstrap.sh` **10/10** with row 9 passing, `verify_clone.sh` **203/203**.

**AND `fetch --prune` PRINTED `- [deleted] (none) -> origin/claude/bus-model-rev56-62lam6`.** That
is the **SIXTH** deletion in the rev-51…56 series and **the first one to hit the branch the incoming
brief named for the CURRENT revision, before that revision had pushed anything.** Expect it again.

**WHAT YOU WILL MEASURE IS PROBABLY NOT THAT.** Rev 56 closed with its work pushed to
`claude/bus-model-rev56-62lam6` and **no PR opened, because none was asked for** — which is what
rev 55 said too, and rev 55 turned out to have been merged through two PRs anyway. Expect one of two
shapes and **measure which**:

* **rev 56 was merged** → HEAD 0 ahead / 0 behind, the branch possibly deleted again.
* **rev 56 was NOT merged** → that branch carries commits `main` does not have, and
  **`bootstrap.sh` ROW 9 WILL FAIL** if you are sitting on `main`, naming it. **That failure is the
  handoff, not a defect.** Check the branch out or merge it before anything else and re-run both
  scripts from there. Do not "fix" row 9 by ignoring it.

**Either way, believe the output and not this paragraph.**

> **ROW 9, NOT ROW 10** — confirmed again at rev 56 by reading the machine's own output:
> row 8 clone depth, **row 9 "no branch carries work HEAD does not have"**, row 10 `verify_clone.sh`.

**RE-MEASURE BEFORE YOU FINISH, TOO.** `origin/main` moved mid-revision at rev 51 and again at
rev 55, and both times **row 9 was the only thing that caught it**. It did **not** move mid-revision
at rev 56 (re-checked at close: 0 ahead / 0 behind, diff empty). **Run the ahead/behind loop again
before you close, every time.**

---

## §2. WHAT REV 56 DID

### §2.1 ITEM A IS CLOSED — THE CARRY LAW WAS THE WRONG POWER

`flank_kv()` carried `k_t` off the rear hub by the map's **FULL horizontal ratio**. The horizontal
scale of a projective image of a plane falls off as **1/Z²** (distance *and* foreshortening) while
the vertical falls off as **1/Z**. So **k_v ∝ sqrt(k_h)**, i.e. **LINEAR in (u+B)** — and the shipped
law was **QUADRATIC in it**. It applied the depth correction twice.

**PROVED, not measured.** `probe_rev56_kv.py` Part 1 builds a pinhole camera where the answer is
known by construction, fits the same Möbius map to it (residual **1.5e-11 px**), and scores both
laws against the truth: **LINEAR 0.0000 %, QUADRATIC 4.299 %** worst over the wheelbase. It survives
tilt, roll, 100 mm/m tumblehome (0.002 %) and radial distortion leaving 4 px of map residual
(0.47 %), so its error is bounded by the map's own fit quality.

Worth **+2.45 %** at the lockup centre (205.3 → **210.4** px/m) and **+4.3 %** at the front hub.

**THE GATE, on `out/r56b_side.png`:**

| | rev 55 | **rev 56** | |
|---|---|---|---|
| ink area ratio | 0.9446 | **0.9669** | PASS, closer to 1.000 |
| ink aspect | **FAIL +5.23 %** | **PASS +1.85 %** | **CLOSED** |
| IoU vs ceiling | 0.7625 | 0.7506 | PASS |
| worst region (`Senor`) | 0.483 | **0.644** | **still FAIL**, bar 0.75 |

All three alternative aspect readings now agree (**+1.85 / −0.44 / +0.94 %**) where they spanned
4.3 points. **WATCHED FAILING: `T1_FC_KVQUAD=1` restores the old law and reproduces the old verdict
exactly — aspect +5.23 % FAIL, area 0.9445.**

**AND REV 55'S PARABOLA IS EXPLAINED.** Rev 55's IoU stretch optimum was **1.0398**; the instrument
correction the wheel implies at the lockup is **1.0428**. **Two routes sharing no datum agree to
0.4 %.** The reference was being placed too tall; **the model was never short.** Rev 55 refused to
stretch `SCR` and was right.

### §2.2 THE "2.3 % INSTRUMENT CONFLICT" IS WITHDRAWN — AND THE ABSOLUTE IS STILL OPEN

`flank_compare.py`'s header argued the horizontal scale must be the **smaller** of the two for an
oblique view, that it is not (220.45 against `k_t`'s 215.5), and therefore one instrument is 2.3 %
out — **without saying which. The first clause is FALSE for this geometry.** The true anisotropy is
**k_h/k_v = a2·(u+B)/(u0+B)**, which **exceeds 1 aft of the principal column**, and the rear hub is
aft of it. The old law hid this by making k_h/k_v **constant along the whole flank**.

**MEASURED.** `ref_side.jpg`'s rear wheel disc is a circle in a plane parallel to the flank, so its
imaged W/H **IS** the local anisotropy, at the very column `k_t` was taken at. Gradient-peak trace,
**1441 rays**, radial sd **0.34 px**, fitted centre **u = 749.26** against `U_RHUB` **749.38**:
**W/H = 1.00417 ± 0.00048**, shear-corrected **k_h/k_v = 1.00516**, against the shipped pair's
**1.02297** — **−1.74 %**. Calibrated by planting a known vertical squash and recovering it to
**0.2 %**; the concentric hubcap boundary was **REJECTED** at radial sd **2.13 px** (not a circle).

**ONLY THE CARRY LAW WAS APPLIED.** Re-anchoring `k_t` to the wheel (k_v(hub) **219.32** rather than
215.5) is **REPORTED AND NOT APPLIED**: it collides with SPEC §10.34's own validation of `k_t`
(belt → aperture top, −0.4 % becomes −2.2 %), and a **third** reading disagrees with both — the
traced disc is **93.09 px** across, which against `t1_core.RIM_R`'s flange OD **0.4396 m** puts k_h
at **211.8**, not the map's **220.5**.

> **THREE QUANTITIES, TWO EQUATIONS.** Which absolute is right **cannot be recovered from what we
> hold** without one more independent absolute on this plane. **The aspect row did not need it** —
> a width over a height carries only the anisotropy — but anything quoting a flank height in
> millimetres does. **This is §3.0 item A.**

### §2.3 ITEM B — A LIVE MEASUREMENT BEHIND A DEAD ENTRY POINT, AND A DEAD GATE

Three briefs carried *"re-base `cream_rms.py` onto `ref_rear34.jpg`, open since rev 17"*. **The
re-base was never the open part** — it has been written in that same file since rev 17/19. What was
dead was **`run()`**, which still pointed at `ref_side.jpg`, hit the rev-17 guard and returned `{}`.
**Eight revisions of no number from the function whose name says "run".** It reports the live
spectrum now. The dead path is kept behind **`T1_CR_LEGACY=1`** so the reason for the re-base stays
watchable. `mottle_measure.py`'s `TARGET` was five typed literals; it is **derived** from
`spectrum()` now and raises rather than falling back (drift printed every run: **0.0004 pp**).

**AND THE RENDER ARM WAS RUN FOR THE FIRST TIME AND IT WAS DEAD.** The beauty arm's patch came back
**100.00 % CLIPPED** — mean L\* exactly 100.00, C\* exactly 0.00, five printed **`ratio 0.00`** rows
that read as *"the model has no mottle at all"*. The cream renders **pure white**:
`shader_solve._render()` builds no studio rig and the file execs `build.py` without `T1_PREVIEW`.
**Looked at** — `probe_scratch/rev56_mottle_frame.png`. It refuses now, and **the refusal is hoisted
above the first printed number**; the pre-existing `too few px` guard sat at the END of the file,
after the character table had already printed `nan`. **A refusal that arrives after the numbers is
not a refusal.**

**THE SECOND GATE'S ACTUAL RESULT** (albedo arm, 3696 px, 0.00 % clipped, stable to ±0.01 across
16/32/48 samples):

| mm | target % | render % | ratio |
|---|---|---|---|
| 3.0 | 0.804 | 0.496 | **0.62** |
| 5.9 | 1.135 | 1.008 | 0.89 |
| 11.9 | 1.455 | 1.805 | 1.24 |
| 23.7 | 2.201 | 2.941 | **1.34** |
| 35.6 | 3.183 | 3.631 | 1.14 |

**The render's cream breakup is TOO WEAK AT FINE SCALE AND TOO STRONG AT COARSE SCALE — the mottle
is too coarse-grained.** A *shape* difference, so it does not wash out under the open px/m bracket.
Second, level-free: **corr(dL\*,dC\*)** is **+0.199 / +0.173 / +0.200** on the render where the
photograph goes **negative with scale** (+0.042 / −0.106 / −0.294) — the photograph's cream is
chalky sun-fade, the render's is luminance-dominated. **CEILING: the C\* base-level row (0.181) is
NOT admissible — it compares an ALBEDO against an OBSERVED PIXEL, SPEC §10.21's trap.**

### §2.4 WHAT REV 56 REFUSED TO MEASURE

* **The front rim disc.** It would have given the carry law a 500 px lever arm. Under contrast
  stretch it yields **two shadowed arcs and no recoverable outer boundary**
  (`probe_scratch/rev56_frontwheel_stretch.png`). **No number was published from it.**
* **The serving-aperture band** (top and bottom edges, a constant 403 mm apart — the ideal
  scale-free instrument). **The glass is not dark**: vertical luma profiles through all three bays
  show reflections and a white shirt. A "dark glass" rule would have selected the wrong pixels.
  **Checked before it produced a number, not after.**
* The first two wheel masks **ran to the crop border** (`probe_scratch/rev56_mask_cream.png`,
  `probe_scratch/rev56_mask_red.png`) — rule 8's defect, caught by painting the selection and looking.

### §2.5 §3.1 IS CLOSED — HE ANSWERED `lid_rail`

Both objects were **0.000000000 m²**, 18 of 18 faces degenerate: the loop ran `(LID_X0, LID_X0)` and
`_rag_grid` interpolates, so every vertex landed at one station. **Asked as multiple choice with a
marked crop** (`probe_scratch/rev56_ASK_lidrail.png`). **His answer: "Narrow lip, ~as wide as it is
tall".** So the width is **not a second free constant — it IS `RAIL_PROUD`**, and the source reads
`RAIL_PROUD`, not a literal. `ref_workshop.jpg` is the **GREEN** vehicle and this is **geometry**,
which rule 11 says transfers.

**The exemption retired itself**: rev 52 wrote it two-sided and its stale arm **FAILED** on the first
build after the width landed. **Sweep now 0 of 223, 0 exempt.** **WATCHED FAILING: `T1_RAILFLAT=1`
takes VERIFY from 0 fail to 3 fail.**

**AND THE PROBE THAT CHECKED IT WAS WRONG TWICE** — rule 4's normal rate, both would have published:
it compared a **DROPPED vertex against the AUTHORED `roof_z`** (reporting the rail 43.7 mm *below*
the roof; the residual is exactly `drop(x)`), and it used a **1e-9 tolerance on float32 vertex
storage** (reporting the aft rail poking outside its own aperture). Re-done **frame-free** by
raycasting onto the built body: **dx 0.0213 m = RAIL_PROUD**, min gap **+21.9 mm**, both rails
inside the aperture. The shipped guard's tolerance is **0.5 mm** with that reason beside it.

### §2.6 REFUTED AT REV 56 / STILL REFUTED — DO NOT REBUILD THESE

* **"the two vertical instruments disagree by 2.3 % and one of them is 2.3 % out"** — REFUTED, §2.2.
* **"for an oblique view of a vertical plane the horizontal scale must be the smaller of the two"** —
  REFUTED. True only forward of the principal column.
* **"`flank_kv` carries `k_t` correctly"** — REFUTED by construction, §2.1.
* **"the render's flank lockup is short in height"** — REFUTED as a MODEL claim, §2.1.
* **"the re-base of `cream_rms` onto `ref_rear34.jpg` is open"** — REFUTED; done since rev 17.
* **"`mottle_measure.py` compares the render against the target"** — REFUTED until rev 56.
* **"`lid_rail`'s width cannot be established"** — REFUTED; he answered it off a frame we hold.
* Everything rev 50–55 refuted — all still refuted: there is no cream either side of the flank ink;
  the flank ink is NOT painted light (1.1 % against a 10.7 % spread); height/aspect/area are not
  three witnesses; the true normal is NOT the fix for the chip gate (it counts facets — the
  subdivision test stands); the nose roundel's V arms do not stop short; the cap's dome depth; the
  m5 "convention conflict"; `LID_W ≤ 1.2797 m`; A7's aft wall; `gal_end_f` widened to `REAR_W/2`.
* **§2b of the rev-52 brief — HIS SETTLED RULINGS — IS UNCHANGED AND STILL BINDING.** W6 (keep the
  studio rig; **a G/R shortfall on any surface is NOT a paint error**); the roof strips' 0.3 m
  retired; the wipers withdrawn entire, commented not deleted; the lower bay SHUT; the RED bus is
  the target and **paint and artwork do not transfer between vehicles**; the tail board IS on the
  vehicle; the marks above the burst are STARS. **Do not re-open or re-ask any of them.**
  `playa_env.py` is not on the table. **And rev 54's ruling stands: "Keep studio, fix the model".**

### §2.7 REV 56 ASKED HIM EXACTLY ONE THING

§3.1's `lid_rail`, carried unasked since rev 52, **asked and answered** (§2.5). Nothing else needed
him. **Do not re-ask it.**

### §2.8 THIS FILE WAS AUDITED AGAINST THE MACHINE, TWICE, AND BOTH PASSES FOUND THINGS

Rule 17 (the sweep: *is what the file says true?*) and rule 15's adversary (*what would make it
false?*) are **different instruments** and rev 55 said to run both. Both were run as SCRIPTS.

**THE `stat`/grep/recompute SWEEP FOUND:**

| what the draft said | what the machine says |
|---|---|
| `verify_clone.sh` **ALL 215 PASS** | **227.** Written mid-revision and stale by SEVEN rows before the file was finished, and it took three passes to settle because the fixes the audit itself demanded each added rows. The row count row exists precisely because this keeps happening |
| the gate reads 0.9699 / 0.7509 / **0.652** | **0.9669 / 0.7506 / 0.644** on `out/r56b_side.png`, the render made AFTER the `lid_rail` geometry change. The earlier figures were from the pre-change render — render-to-render, not a regression, and the aspect row is identical to four decimals in both. **A brief must quote the render a reader will reproduce from THIS head** |
| §2.4 cited one of the two mask tiles by BARE FILENAME, with no directory | **that path did not resolve.** It is `probe_scratch/rev56_mask_red.png`, and the sibling four words earlier was already fully qualified. **THIS IS THE THIRD REVISION RUNNING FOR THIS EXACT DEFECT** — rev 54's ladder tile, rev 55's arch tile, now this: a bare filename beside a qualified sibling, caught only by the `stat` sweep and passed over by re-reading every time. The other **46** paths resolved. *(The broken form is not quoted ANYWHERE in this file, this row included. The rev-56 brief warned about exactly that — a brief that prints a bad path as an example fails its own sweep — and **the first draft of this row printed it anyway and duly failed the sweep a second time**. That is the same self-referential trap as the audit-phrase row two rows down. Naming a defect and demonstrating it are not the same act.)* |
| §6 misspelled "BEAUTY" in the one line telling the next context which arm of `mottle_measure.py` to run | caught by a spelling trap in the sweep, not by reading. **The misspelling is not reproduced in this cell** — see the row below |
| §2.8's heading was missing the phrase `verify_clone.sh`'s own `newest brief records its own audit` row greps for | that row **FAILED**. *(The phrase is deliberately not quoted in this cell: the row counts occurrences and wants exactly one, so a cell naming it makes the row fail — which is precisely what happened on the first attempt at this fix.)* The audit row was itself un-audited — the sweep I wrote checked paths, strings, switches and figures and did not check that the brief satisfies the verifier's own brief-facing rows. **Run `./verify_clone.sh` against the outgoing brief before calling the audit done; four of the five defects here were found that way, not by the sweep** |
| `README.md` and `START_HERE.md` still said **rev 56** | both point at the newest brief by number and both **FAILED** their rows. Updated |
| **THE SAME SELF-REFERENTIAL TRAP FIRED THREE TIMES IN THIS ONE FILE** | A row that documents a defect by QUOTING it re-commits the defect, because the sweep matches text and cannot tell an example from an instance. It happened with the broken path, with the phrase the audit row counts, and with the misspelling — **each time in the row written to explain that very defect, and each time only the second run of the sweep caught it.** Rev 54, 55 and 56 each recorded one instance of this and treated it as a one-off. It is not: **it is structural.** WHEN YOU DOCUMENT A DEFECT IN THIS FILE, DESCRIBE IT — DO NOT REPRODUCE IT. And run the sweep AGAIN after every fix the sweep demands |

**THE ADVERSARIAL PASS BROKE NOTHING, AND HERE IS EXACTLY WHAT IT TRIED** — written as a script and
RUN, so this list is what executed rather than what was drafted:

* *"Do the ablations actually flip what the brief says they flip?"* — `T1_FC_KVQUAD` moves
  `flank_kv(465.5)` **210.355 → 205.332 px/m**, which is the 205.3 → 210.4 the file quotes.
* *"Does every script the brief tells you to run ACTUALLY RUN?"* — `probe_rev56_kv.py` and
  `cream_rms.py` both **rc=0**, and both print the strings quoted from them.
* *"Was a BAR moved to make a row pass?"* — the diff of `flank_compare.py` across this revision
  touches **no** `*_TOL` constant. The instrument under the bar changed; the bar did not.
* *"Does `STATE.md` actually say what the brief says it says?"* — **0 of 223, 0 exempt**, and its
  own provenance header reads `working tree | clean`.
* *"Is this file byte-identical to `PASTE_INTO_CLAUDE_CODE.txt`?"* — yes, checked by comparing the
  two files rather than by remembering to `cp`.
* *"Does every `T1_*` this brief names actually READ THE ENVIRONMENT?"* — all four new ones do:
  `T1_FC_KVQUAD` (`flank_compare.py`), `T1_RAILFLAT` (`t1_shell.py`), `T1_CR_LEGACY`
  (`cream_rms.py`), `T1_MM_ALBEDO` (`mottle_measure.py`). The row that checks this is anchored on
  the environment read, not the string, so a switch surviving only in a comment fails it.
* *"Is anything claimed DONE that is not?"* — **§3.3, the top job, is claimed NOT done and is not
  done. Three revisions running.** §5 of `LEDGER_rev56.md` lists every omission on purpose.
* *"Does the aspect fix just move a bar?"* — **No.** The bar (5 %) and every threshold are
  untouched; the instrument under the bar changed, and the ablation reproduces the old verdict
  exactly. **A script was not edited to make it pass.**
* *"Is the wheel measurement circular with the map?"* — **Partly, and it is stated.** The ANISOTROPY
  is a pure ratio and map-free; converting it to an absolute k_v uses the map's `A` and `B`. The
  aspect row uses only the ratio. Said in the source and in §2.2.

**WHAT NEITHER PASS COULD BREAK, reported because a control that finds nothing is still a result:**
every path this file names resolves; `RAIL_PROUD = 0.0213` is in `t1_shell.py`;
`FLANK_A, FLANK_B, FLANK_C = 641220.4, 11140.0, 55.0322` and `K_T = 215.5` are in
`flank_compare.py`; `flank_kv(465.5)/flank_kv(749.38)` **runs** to 0.976122 (linear) and 0.952814
under the ablation; `cream_rms.spectrum(_BODY)` was RUN and returns **0.804 / 1.135 / 1.455 / 2.201
/ 3.183**; `_BODY = (885, 968, 292, 388)`; `PXM_REF = 337.0`; the zero-area sweep reads **0 of 223**
in `STATE.md`, machine-written on a clean tree.

**THIS FILE MUST STAY BYTE-IDENTICAL TO `PASTE_INTO_CLAUDE_CODE.txt`.** `CLAUDE.md` imports that
file into every session as the entry procedure. **WHEN YOU WRITE THE REV-58 BRIEF, `cp` IT OVER
`PASTE_INTO_CLAUDE_CODE.txt` IN THE SAME COMMIT, OR `verify_clone.sh` FAILS AND NAMES THE ROW.**

---

## §3. THE WORK LIST FOR REV 57

### §3.0 START HERE — THE ORDER, AND WHY

**He ruled "keep studio, fix the model", so this is still a MODEL revision.** Rev 56 fixed two
instruments and woke a second gate. **Neither moved the vehicle.** Rev 57 starts with the item that
has been deferred three revisions running.

| # | do this | why | the gate |
|---|---|---|---|
| **A** | **THE TWO VW BADGES — THE STROKE WEIGHT.** The nose-badge route on `ref_workshop.jpg`, §3.3. **Take it or close it with its ceiling.** | It is the **top job**, it is unblocked, it uses frames we hold, and it has been skipped at rev 54, 55 AND 56 | `verify.py` §13 guards self-consistency only; a frame comparison would be the FIRST fidelity row on the badge |
| **B** | **THE CREAM MOTTLE IS TOO COARSE.** §2.3 gives you a live gate and a shape defect: 0.62 at 3 mm, 1.34 at 23.7 mm, and the wrong sign of corr(dL\*,dC\*) | A second gate that RUNS and disagrees with the photograph. This is the first time the mottle map has ever been measurable | `mottle_measure.py` albedo arm |
| **C** | **`Senor`, the last failing `flank_compare` row** — 0.644 against 0.75 | The aspect row is closed, so this one is no longer downstream of the same unknown. It is now on its own | `flank_compare.py` |
| **D** | the absolute flank scale (§2.2), A9 / the three holes / A13 / A16 / A11 / A14, the colour locks | unblocked, but **no gate** | — |

**RENDER FIRST.** `out/` starts empty. `T1_PREVIEW=side` at **1600×1100** feeds `flank_compare.py`.
Render `hero` and **LOOK at it.**

**A WARNING ABOUT LOOKING.** Rev 55 called the nose roundel an "X" off a half-size hero and it
dissolved at full size. **Crops generate leads, not findings.** Take the lead, paint the window,
then believe the number.

### §3.1 THE MOTTLE — THE FIRST MEASURABLE SHADER DEFECT THIS PROJECT HAS HAD

`mottle_measure.py` now runs. `t1_mats` carries `MOTTLE_AMP` (0.550), `MOTTLE_RGH_K` (0.180) and
`MOTTLE_M` (0.0240 m). The measured mismatch is a **SHAPE** one — too little fine structure, too
much coarse — which points at `MOTTLE_M`, the feature size, rather than `MOTTLE_AMP`. **Do not tune
by eye: the gate is live, so sweep it and print the ratios.** And the character row
(corr(dL\*,dC\*) positive on the render, negative on the photograph) is **level-free and scale-free**
— it is the stronger of the two signals and no amplitude change will fix its sign.

**AND FIX THE BEAUTY ARM OR STATE WHY NOT.** It refuses today because the cream blows out;
`shader_solve._render()` builds no studio rig. Building one inside that file changes what it
measures, which is why rev 56 did not do it silently.

### §3.2 ITEM B'S REMAINING PIECE — THE mm AXIS

`PXM_REF = 337.0` px/m on that plane is a **bracket** (330–344), not a measurement, and it sets the
mm axis of the whole mottle comparison above. **Rev 56's §2.1 algebra applies to `ref_rear34.jpg`
too** — if that frame's flank can be given a projective map, the same sqrt law gives its vertical
scale. Not attempted at rev 56. *(Rev 55's correction stands: `depth_correct()` is defined NOWHERE
in this repo.)*

### §3.3 THE TOP JOB — THE TWO VW BADGES. THREE REVISIONS UN-ATTEMPTED

**The DIAMETER route on `ref_side.jpg` is EXHAUSTED** (0.3474 vs the built 0.3170 — 9.6 % small but
only **1.8 sigma**; rev 51's figure, INHERITED, do not re-run it). **The open constant is the STROKE
WEIGHT**, and rev 54 established what it denominates — **compare a frame against 0.25639, not
against `CAP_EMBLEM_WFRAC = 0.2087`; comparing against 0.2087 itself understates by 18.6 %.** The
two badge DESIGNS differ by **5.09 %** and neither has ever been compared to any frame. Full text
and the four closed routes in **`PHOTOS_WANTED_rev52.md` item 7**. **NOT A DEFECT — DO NOT REBUILD:**
the badge's REACH is settled (rev 54, 720-ray profile, all six stroke ends land on the band).

**THE ROUTE, AND ITS CEILING** (new at rev 54, un-attempted at 54, 55 **and 56**):
`PHOTOS_WANTED_rev52.md` item 7 closes four routes and **all four are about the HUBCAP badge; none
closes the NOSE badge**, which is the same design — the record says so and already **transferred its
RING BAND from one to the other** (`t1_detail.py`: *"ref_workshop.jpg nose badge … = 0.0874 / 0.0995
… ring band / ring outer D = 0.093 ± 0.012 adopted"*).
* `ref_workshop.jpg` shows the nose badge at **91.7 px vertical D, PSF sigma 0.689 px** — a stroke
  of ~0.25 R is ~11 px, **resolved**. The record's crop box **(258,494,352,604)** is correct.
* **CEILING.** (a) `ref_workshop.jpg` is the **GREEN** vehicle and paint/artwork do not transfer.
  A pressed factory badge is arguably GEOMETRY, which rule 11 says does — **but that is an argument,
  not a measurement, and the same argument already underwrites the shipped ring band. Either both
  are legitimate or the ring band is grounded on the wrong vehicle. Resolve that before publishing.**
  *(Rev 56 made the same call for `lid_rail` and made it explicitly — §2.5. That is a precedent for
  the ARGUMENT, not a substitute for making it here.)*
  (b) The badge is **strongly oblique** — 62.7/91.7 = **0.684 axis ratio** — so it must be
  de-projected and only vertical extents are trustworthy. **Rev 56's anisotropy algebra (§2.2) is
  directly applicable to that de-projection and was written for exactly this class of problem.**
  (c) The RED bus's own nose roundel is in `ref_nolita_front34.jpg` at a **41 × 66 px** bbox — the
  right vehicle, but a 700×467 JPEG.
* **Rev 51 spent a whole revision on the diameter by this kind of route and reached 1.8 sigma, so it
  is a revision's work rather than a spare hour — but that is a statement of COST, not a reason to
  defer it, and §0.1 forbids reading it as one. REV 57: TAKE IT, OR CLOSE IT WITH ITS CEILING.**

### §3.4 FINISH A9, AND THE THREE HOLES REV 52 LEFT OPEN

**A9: two of four parts done; the galley is still ~103 mm too far aft. PROVENANCE, GRADED: the
per-feature deltas are INHERITED from the rev-52 brief and have NOT been re-measured at rev 52, 53,
54, 55 or 56.** The offset is **NOT rigid** (−0.09574 at hook u=0.13 to −0.11035 at `gal_appliance`
u=0.80, so one additive constant leaves ±7.3 mm). Re-derive each X from `BAYS`, the way `gal_rail`
now is. *(The survey's ~106 mm and its +0.096..+0.113 range are both wrong.)*

**THE THREE HOLES. PROVENANCE, GRADED: the 260.0 mm and 20.0 mm sight lines are rev 52's and have
NOT been re-measured since.** The other two WERE recomputed at rev 54's audit and reproduce exactly.
* `gal_end_f` sees past by **260.0 mm** on the show side and 20.0 mm on the off side. Needs its own
  sight line established first — **do not inherit `REAR_W/2`** (rule 34: that figure belongs to the
  rear window, which is not what looks at it).
* The **sixth hook at X −0.907 lies 51.25 mm beyond `BAYS[2]`'s own aft edge (−0.855750)**. The six
  hook stations are typed literals with irregular spacing whose span centre is **−0.705** against
  the rail's measured **−0.598** — a **107.0 mm** disagreement. **They disagree and one is wrong.**
* A7's real defect: `roof_cutters()`'s aft edge is `LID_X1`, which is **not** greppable as
  `LID_X1 = -1.0700` — the source line is `LID_X0, LID_X1 = 0.9640, -1.0700` in `t1_shell.py`, so
  **803 mm of roofed body** sits between the last light inlet and the tail skin. Unbuilt. A7 is
  **ILLUMINATION, not dressing.**

### §3.5 A13 / A16 / A12, A11's SECTION, A14, AND THE CHEAP COLOUR ITEM

**A13 / A16 / A12** — the isolated star built BELOW the burst where both red frames put it above;
every flank rosette drawn at the diameter of its **gold core**; *A12 is an OWNER RULING, not a
do-now* — `senor_trace.py` calls the remedy *"inventing ink the photograph does not show"*.

**A11's SECTION, A14** — a chrome lever lying in a dish **pressed into** the skin against a 12 mm
**proud** prism. *(The `lid_rail` WIDTH that used to sit here is CLOSED — §2.5.)*

**A CHEAP UNBLOCKED ITEM, STILL NOT DONE AFTER FIVE REVISIONS:** `SPEC` §8's colour locks are all
graded **M** = *"measured by me from `ref_source.jpeg`"* — a 246×197 thumbnail the record itself
calls retired. They can be re-derived on `ref_playa_34.png` at **4× the area** with no new
photograph. **Report the re-derived values; do not change the constants without his ruling** — W6
makes colour his call. *(And `ref_playa_34.png` is byte-identical to `IMG_3842.png`; a duplicate is
not corroboration — rule 11.)* The render's flank red reads **G/R 0.462 against the photograph's
0.114**, and the split between paint and illuminant **cannot be recovered from what we hold**.

### §3.6 THE PROCESS ROWS, STILL OPEN

The **open-findings register is REINSTATED** as `OPEN_FINDINGS.md` (rev 56) — see §8; the
standing-instructions carrier deleted at rev 44, which took the **die-cut sticker — the project's
original deliverable** — with it, **still open and now carried as F18**; SPEC §0.2's two rev-4 corrections later refuted; rev 48's refuted *"B stays
open"* still live in `build.py` and, **split across two lines so a flat grep misses it**, in
`t1_shell.py`; the tail board still has **zero rows in either verifier**.

### §3.7 THE HABITS THAT PAID AT REV 56

**A DERIVED VERDICT CATCHES YOUR OWN THRESHOLD.** `probe_rev56_kv.py`'s Part 1 printed
`INCONCLUSIVE` on a run where the two laws had separated by 4.3 %, because the test compared
fractions against percentages. A constant string would have shipped the conclusion anyway.

**CALIBRATE THE ESTIMATOR BY PLANTING WHAT IT IS SUPPOSED TO FIND.** The wheel's W/H was only
believed after a known vertical squash was planted in the frame and recovered to 0.2 % — and after
a threshold-based version of the same trace was **discarded** for moving 0.9 % when its bracket
changed, which is the size of the effect.

**LET THE RESIDUAL REJECT THE WINDOW.** The hubcap boundary came back at radial sd 2.13 px and was
dropped as "not a circle" by the number, not by an opinion.

**CHECK THE WINDOW BEFORE IT PRODUCES A NUMBER, NOT AFTER.** The aperture-band route died on a
one-line luma profile showing the glass is bright. That cost a minute; believing it would have cost
the revision.

**AND ASK THE GEOMETRY IN ONE FRAME.** Both of rev 56's probe errors (§2.5) were frame or precision
errors, not modelling errors, and both produced plausible numbers.

---

## §4. WHAT WAS ASKED OF HIM — A CARRIER, NOT A LIST OF BLOCKERS

> **READ §0.1 FIRST.** At rev 54 he ruled that **the reference set on the repo is complete**. This
> section is kept in full because `CLAUDE.md` rule 16 forbids dropping a carrier, and because it
> records what was asked and what was refused — which is why items 1–5 must never be re-asked.
> **But it is no longer a licence to park work.** Nothing below blocks an item; it only says what a
> new frame would have made easier. Work every item from what we hold, or close it with
> *"it cannot be recovered from what we hold"* and its ceiling.

**`PHOTOS_WANTED_rev52.md` is the carrier for item 7 (ONE HUBCAP, SQUARE ON AND CLOSE)**. Items
**1–5** keep their full text in `PHOTOS_WANTED_rev49.md`: the tail board's footing; the decal darker;
the nose square on; a raking-light frame of the louvres (**ONE item — the pressing depth**; the
"block length, station and V swage" expansion is a proposal, not the record); the off side, any
frame. **He has said 1–5 are not possible now. DO NOT RE-ASK THEM.** Item 6 (an obliquely-seen
wheel) was **DISSOLVED at rev 51** — struck, not outstanding.

**CARRIED FROM REV 53, still no carrier outside these briefs:** a frame showing the cream **where it
IS chipped** — any close frame of a worn edge. **Rev 54 lowered its urgency and rev 55 lowered it
again**: the band is 0.27 px at every scale this project ships, AND the gate that would place those
chips on the red is not built. Only worth asking if a close counter view is ever wanted.

**ANSWERED AT REV 56 AND NOT TO BE RE-ASKED:** `lid_rail`'s width — *"narrow lip, ~as wide as it is
tall"* (§2.5). That was the only question rev 56 put to him.

---

## §5. THE RULES — `CLAUDE.md` CARRIES THE METHOD, NOT THE NUMBERED CANON

The canon (rules 1–33) is printed in `NEXT_CONTEXT_PROMPT_rev50.md` §11. **Rules 34 and 35 live only
in the rev-51…56 briefs and `LEDGER_rev50.md` §0, so they are carried here too — that is
`CLAUDE.md`'s own rule 16 firing on this file:**

> **34. A REQUIREMENT INHERITS ITS OBJECT EXACTLY AS A RETIREMENT DOES.** Before relying on any
> *"the record requires X"*, check which object the sentence is about — and check the cited line
> exists. **Rev 52 applied this deliberately**: `gal_end_f` was left alone because `REAR_W/2`
> belongs to the rear window. **Rev 54 applied it to a photograph**: item 7's four closed routes are
> all about the HUBCAP badge and none closes the NOSE badge. **Rev 55 applied it to a function**:
> `cream_rms.py` cited `depth_correct()`, which is defined NOWHERE in this repo. **Rev 56 applied it
> to a CAMERA**: `flank_compare.py`'s header attributes a recovered camera position to
> `ref_side.jpg` that `studio.py` attributes to the PLAYA frame — the same three numbers in two
> places about two photographs. **NOT resolved at rev 56; nothing rev 56 published depends on it,
> because the anisotropy was measured off the wheel rather than predicted from a pose. Check it
> before any future work leans on that camera.**

> **35. A GUARD WRITTEN AGAINST A POSE ENCODES THAT POSE.** Guards that identify a part's foot or
> free edge by `min(y)` are only right while the part leans one way. Ask the geometry.
> **Rev 53 broke this and was caught by it**; **rev 54 broke it again** — a global `min(z)` for a
> fold that SLOPES, wrong by 25 mm; **rev 55 broke it a third time** — a TYPED crop window for the
> counter control that caught 418 px of it. **Rev 56 broke its FRAME-relative cousin** — a probe
> comparing a DROPPED vertex against the AUTHORED `roof_z` and reporting a rail 43.7 mm below a roof
> it sits 21.3 mm above (§2.5).

> **Rule 29.3:** no finding is attributed to a cause until a control separates it. **Rule 29:** a
> retirement inherits the object it was made about. **Rule 15:** a retraction that lands in a ledger
> and not in the source is half a retraction — **rev 56's withdrawal of "one of the two instruments
> is 2.3 % out" is in `flank_compare.py`'s own printed block and in `flank_kv.__doc__`, and four
> rows hold it there.**

---

## §6. THIS MACHINE

```
cores 4   RAM 15 GB   Blender 4.5.3 via pip install bpy   subagent concurrency 2
build  T1_SUB=1 ~20 s     render 1600x1100 96 spp ~6 min PER VIEW
```

```bash
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
T1_PREVIEW=side T1_PFX=r57 T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
  /tmp/blender/blender -b -P build.py
T1_PREVIEW=hero34r ...                                       # the REAR 3/4 -- A7 lives here
T1_SUB=2 /tmp/blender/blender -b -P audit.py                 # rewrites STATE.md -- COMMIT FIRST
python3 lid_gen.py                                           # regenerates tex/lidmural.png
python3 flank_compare.py out/r57_side.png /tmp/fc.png        # GATE 1.  FAILS 1 of 4 today.
python3 cream_rms.py                                         # the LIVE photograph-side cream
T1_SUB=1 T1_MM_ALBEDO=1 /tmp/blender/blender -b -P mottle_measure.py   # GATE 2.  RUN THE ALBEDO ARM
python3 probe_rev56_kv.py                                    # the vertical scale, both halves
python3 probe_rev53_chip.py                                  # the chip measurement, all six arms
T1_SUB=1 T1_AOVSAMP=64  /tmp/blender/blender -b -P probe_rev54_aov.py    # the EDGE AOV + sweep
T1_SUB=1 T1_LOOKSAMP=192 /tmp/blender/blender -b -P probe_rev54_look.py  # the scale ladder
/tmp/blender/blender -b -P probe_rev54_wfrac.py              # the badge denominator, calibrated
T1_SUB=1 /tmp/blender/blender -b -P probe_rev54_badge.py     # the badge off the built mesh
T1_SUB=1 T1_TNSAMP=64 /tmp/blender/blender -b -P probe_rev55_truenorm.py  # RUN IT AT SUB=1 AND 2
```

**`out/` IS NOT TRACKED and starts empty. Render before quoting any probe that reads a frame.**
**A backgrounded runner's exit code is the WRAPPER'S, not Blender's — grep the log for `Saved:`.**
**`probe_rev54_aov.py` and `probe_rev55_truenorm.py` write EXR into `probe_scratch/` — delete them
before committing and keep the PNGs.**
**`mottle_measure.py`'s BEAUTY arm REFUSES (100 % clipped). Run it with `T1_MM_ALBEDO=1`.**

**ABLATIONS — every one exists to WATCH A GUARD FAIL.**
**NEW AT REV 56:** **`T1_FC_KVQUAD`** (restores `flank_kv`'s old QUADRATIC carry law; the aspect row
goes back to +5.23 % and FAILS), **`T1_RAILFLAT`** (restores `lid_rail`'s `xa == xb`; VERIFY goes
0 fail -> 3 fail), **`T1_CR_LEGACY`** (runs `cream_rms`'s dead `ref_side.jpg` path so the reason for
the re-base stays watchable).
Carried: `T1_FC_INKGAIN` (adds DN to the RENDER's flank ink only; at +30 the ink/ground R ratio
moves 0.867 -> 1.022 and the verdict flips), `T1_FC_ZSTRETCH` (stretches the render's lockup mask;
the IoU parabola peaks at 1.0398 -- and rev 56 explains why: see §2.1), **`T1_TRUENORM`** (swaps the
chip gate onto the true normal -- **a DEMONSTRATION, not a fix; do not make it the default**),
`T1_PTWEAR=1`, `T1_EDGERAD`, `T1_MM_ALBEDO`, `T1_TARNCONTAM=1`, `T1_RAILSTALE=1`, `T1_ENDSHORT=1`,
`T1_CAPSINK=1`, `T1_LIDDEG=104`, `T1_BAYSTALE=1`, `T1_LAMPSINK=1`, `T1_LIDASPECT=1.2`,
`T1_HANDLEHI=1`, `T1_BAREMAT=1`, `T1_TBFOOT=1`, `T1_BAYPROUD=1`, `T1_NOBEVEL=1`,
`T1_BEVEL_SAMPLES`, `T1_FC_OLDDATUM=1`.

---

## §7. THE STANDARD, IN HIS WORDS

We are recreating a photorealistic version of **that exact bus**, and **any single measurement off is
unacceptable** — per-measurement, not on average. A model right in ninety places and wrong in one is
not 99 % done, because he will look straight at the one.

`bus_model_ref.JPG` is a **SCHOOL BUS** and is **NOT the vehicle** — a FIDELITY BAR only. Use
`ref_workshop.jpg` the same way, and remember it has **no headlamps and no hubcaps fitted** and is
the **GREEN** vehicle (§4).

**Ground in the reference, build, adversarially audit, iterate.** Never build before grounding. Never
call it done off self-review. Report the measurement **with its ceiling**, never a self-assigned
score. Do not say anything is ready — say what is fixed, what is still wrong, and what you measured.

**RENDER IT, CROP IT, AND LOOK AT IT, before and after every change.** Every defect this project has
shipped passed `VERIFY: 0 fail, 0 warn` and was found by looking at a crop. **Rev 56's whole item-B
result turned on this: the ratios said 0.00 five times, and only LOOKING at the frame said the patch
was pure white.**

**When you need something from him, ask as MULTIPLE CHOICE with the reference material attached — one
crop, one mark, one sentence — and ASK IT WITH THE QUESTION TOOL.** He has never stood in the bus: do
not ask what the real vehicle looks like, ask what a PHOTOGRAPH shows. **Rev 56 asked him exactly one
thing — `lid_rail`'s width — and it closed a defect that had been exempt for four revisions.**

**`git rev-list --count origin/main..HEAD` before you start and again before you finish. And
`git diff --name-only HEAD...origin/main` — that is where his photographs arrive. EVERY session.**

---

## §8. THE OPEN-FINDINGS REGISTER — `OPEN_FINDINGS.md`

**A register existed once and was ABANDONED AT REV 45 WITH 21 ROWS, and nobody noticed for eleven
revisions.** The standing-instructions carrier went the same way at rev 44 and took the project's
original deliverable with it. Rev 56 reinstated the register as **`OPEN_FINDINGS.md`**, seeded only
from findings that could be grounded in the repository on the day it was written: **36 rows — 28
OPEN, 8 CLOSED.**

**IT IS A CARRIER (rule 16). Rows leave it only by being CLOSED with the measurement that closed
them, or RETIRED with the ruling that retired them. Never by being dropped.**

**THE POINT OF THE FILE IS THE PROVENANCE GRADE, NOT THE LIST.** Every row is marked
`MEASURED-revN` / `RECOMPUTED-revN` / `INHERITED-revN` / `RULED-revN` / `CEILED`. This project's
recurring failure is not losing numbers — it is **re-quoting inherited ones as though they had been
measured**. An `INHERITED` row is a claim. Treat it as one.

**GRADE DECAY IS ITSELF A FINDING.** An `INHERITED` row that survives three more revisions without
being re-measured should be re-measured or downgraded — not quietly re-quoted a fourth time.

**REV 56 UPGRADED FOUR ROWS BY RE-MEASURING THEM**, and reports that they were sound: the galley
cluster (F11–F13) had been carried as INHERITED-rev52 for four revisions and **every figure
reproduced exactly off the built mesh** — `BAYS[2]` aft edge **−0.855750**, sixth hook overshoot
**51.25 mm**, hook span centre **−0.7050** against the rail's **−0.5980** = **107.0 mm**, and the six
stations' irregular gaps **78 / 79 / 73 / 105 / 69 mm**. *A control that finds nothing is still a
result, and four INHERITED rows becoming MEASURED is worth more than a new row.*

**WHAT IS STILL INHERITED AND OLDEST:** F14 (`gal_end_f`'s 260.0 / 20.0 mm sight lines, rev 52),
F15 (A7's 803 mm, rev 52), F08/F09 (the badge, rev 54), F20 (the colour locks, rev 52), F18 (the
die-cut sticker, rev 44 — **the oldest thing in the file**).

---

## §9. THE HORIZON BEYOND REV 57 — WHERE THIS IS GOING

**Rev 57's own order is §3.0. This section is the longer arc, so the project stops lurching from
item to item.** It is a CARRIER too: each revision should re-rank it, not rewrite it, and say what
moved.

| horizon | the work | why it is in this order |
|---|---|---|
| **next** | **F08 — the badge stroke weight.** Take the nose-badge route or close it with its ceiling | The top job, unblocked, three revisions deferred. Nothing else on the list has been skipped that often |
| **next** | **F03/F04 — the cream mottle.** A live gate that disagrees with the photograph in SHAPE and in SIGN | The first measurable shader defect this project has ever had. `MOTTLE_M` (feature size), not `MOTTLE_AMP` |
| **near** | **F01 — `Senor`.** No longer downstream of the aspect unknown; it is on its own now | The last failing row on gate 1 |
| **near** | **F02/F06 — the two absolute scales.** Rev 56's sqrt-law algebra applies to `ref_rear34.jpg` as well as `ref_side.jpg` | Both gates quote millimetres through a bracket. Closing either lifts everything downstream |
| **then** | **F10–F14 — the galley cluster.** Now MEASURED, so it is a build job rather than a measurement one | Re-derive each X from `BAYS`; establish `gal_end_f`'s own sight line first |
| **then** | **F15 — A7.** Illumination, not dressing | 803 mm of unlit roofed body changes how the rear reads |
| **later** | **F19 — the red's edge wear.** Needs a real crease/edge-angle attribute off the geometry | A revision's work, and both obvious sockets are already refuted |
| **later** | **F16/F17/F20/F23–F28** — artwork placement, the colour locks, the process rows | Unblocked but ungated |
| **standing** | **F18 — the die-cut sticker** | The original deliverable. It has no gate and no owner ruling, and it has been open since rev 44 |

**WHAT WOULD CHANGE THIS ORDER:** a new photograph (§0.1 says none is coming), an owner ruling, or a
gate becoming available for something currently ungated. **Gate availability is the ranking rule** —
an item with a gate outranks an item without one, because only the gated one can tell you whether
you improved the photograph.

---

## §10. HOW TO GROW THIS HANDOFF WITHOUT BREAKING IT

**Written because rev 56 spent three passes fighting the mechanics rather than the work.**

1. **The set is three files.** `LEDGER_rev<N>.md` (what you did, with every number),
   `NEXT_CONTEXT_PROMPT_rev<N+1>.md` (this file), and **`cp` of that file over
   `PASTE_INTO_CLAUDE_CODE.txt` IN THE SAME COMMIT.** `CLAUDE.md` imports the `.txt` into every
   session, and a byte-identity row fails if you forget. *(The `HANDOFF_rev*.md` series ended at
   rev 45; do not restart it.)*
2. **`README.md` and `START_HERE.md` name the newest brief BY NUMBER.** Two rows check it. Update
   both when you write the brief, not after the verifier tells you.
3. **THE ROW COUNT IS SELF-REFERENTIAL AND IT WILL BITE YOU.** `verify_clone.sh` asserts the newest
   brief states the script's own total. **Every row you add changes the number the brief must
   state**, so write the count LAST, and re-run after every fix — including the fixes your own
   audit demands, which add rows of their own. Rev 56's count moved three times.
4. **ADD ROWS ANCHORED ON ARITHMETIC OR BEHAVIOUR, NOT ON A GREP.** A grep passes on a comment. Rev
   56's rows RUN `flank_kv` at two columns, RUN `cream_rms.run()`, and compare two source offsets to
   prove a guard precedes a print. The one row rev 56 wrote as a bare grep needed fixing twice
   because the phrase it counted legitimately appears more than once.
5. **RUN BOTH AUDITS, AS SCRIPTS, AND RECORD WHAT THEY FOUND *IN* THE BRIEF.** The rule-17 sweep
   asks *"is what the file says true?"*; the adversary asks *"what would make it false?"*. They are
   different instruments and they find different things — at rev 56 the sweep found a
   directory-less path and a typo, and **four of the five defects came from running
   `./verify_clone.sh` against the outgoing brief**, which neither pass thought to do until it did.
6. **NEVER DELETE A CARRIER.** §0, §0.1, §4, §5, §8 and §9 are carriers. If a section is the only
   home of something, carry it or hand it on by name. Two carriers have been lost in this project's
   history and both losses took years of context with them.
7. **ROOM TO GROW:** new findings go in `OPEN_FINDINGS.md` with an ID and a grade, not into this
   file's prose. This file points AT the register. That way the brief stays a map and the register
   becomes the memory, and neither has to be rewritten to add one fact.
