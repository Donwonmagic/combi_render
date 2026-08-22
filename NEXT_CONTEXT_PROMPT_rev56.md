# NEXT CONTEXT PROMPT — rev 56

**Read this whole file before you touch anything.** Then `CLAUDE.md` (method only, loads every
session), then `LEDGER_rev55.md` — which is where every number below comes from — then
`SURVEY_rev49_photoreal.md` §6, still the work list.

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
./verify_clone.sh       # ALL 183 PASS -- and read what its verdict block says
```

**AT PICKUP, REV 55 MEASURED:** rev 54 **was merged**, through **PR #11** — so of the two shapes
the rev-55 brief offered, it was the first. HEAD **0 ahead / 0 behind** `origin/main`, every remote
branch **0 ahead**, `git diff --name-only HEAD...origin/main` **empty** (no photographs arrived),
`bootstrap.sh` **10/10** with row 9 passing, `verify_clone.sh` **173/173**. And `fetch --prune`
printed `- [deleted] (none) -> origin/claude/new-session-4uh2wh`, so the **designated branch's
remote copy has now been deleted a FIFTH time** in the rev-51…55 series.

**WHAT YOU WILL MEASURE IS PROBABLY NOT THAT.** Rev 55 closed with its work pushed to
`claude/new-session-4uh2wh` and **no PR opened, because none was asked for.** Expect one of two
shapes and **measure which**:

* **rev 55 was merged** → HEAD 0 ahead / 0 behind, the branch possibly deleted a sixth time.
* **rev 55 was NOT merged** → that branch carries commits `main` does not have, and
  **`bootstrap.sh` ROW 9 WILL FAIL** if you are sitting on `main`, naming it. **That failure is the
  handoff, not a defect.** Check the branch out or merge it before anything else and re-run both
  scripts from there. Do not "fix" row 9 by ignoring it.

**Either way, believe the output and not this paragraph.**

> **ROW 9, NOT ROW 10** — confirmed again at rev 55 by reading the machine's own output:
> row 8 clone depth, **row 9 "no branch carries work HEAD does not have"**, row 10 `verify_clone.sh`.

**Re-measure before you finish, too.** `origin/main` moved mid-revision at rev 51.

---

## §2. WHAT REV 55 DID

### §2.1 ITEM A IS ANSWERED, AND IT EXONERATES THE FLANK INK

The brief asked to *"measure the CREAM either side of the ink"* to separate the ink's
+41.2/+38.6/+36.3 DN from the rig's exposure. **THE QUESTION HAD A FALSE PREMISE: there is no cream
either side of that ink.** The flank lockup is silver on the **RED** body; the cream band is ~400 mm
up, above the belt line and outside both crops. One look at `probe_scratch/rev55_A_refcrop_x4.png`
settles it, and `flank_compare.py`'s own docstring had already said the ground endmember there is
`(194, 87, 74)` — red.

The control used instead is the **RED ground hugging the ink** — same panel, same paint, same local
lighting, no second registration. An annulus around **each frame's own ink** at a **matched physical
standoff**, three bands, with enclosed ground (the letter counters) dropped by a **flood fill from
the border** because ground enclosed by ink carries the silver's halo from every side.

**THE ANSWER, and it is the statistic that cancels exposure AND illuminant** — ink divided by its
own ground, in the same frame:

| | R | G | B |
|---|---|---|---|
| photograph | **0.857** | 7.045 | 17.527 |
| render | **0.867** | 1.757 | 2.048 |

**The red channel agrees to 1.1 %, against the reference ink's own R spread of 10.7 %. THE INK IS
NOT PAINTED LIGHT RELATIVE TO THE PAINT IT SITS ON — DO NOT TOUCH AN INK CONSTANT.** The raw
offsets say the same: the ground carries **171 %** of the ink's own luma offset. **Every other
flank item was blocked on this and is now unblocked.**

**WATCHED FAILING.** `T1_FC_INKGAIN` adds DN to the render's ink only, ground untouched. At +30 DN
the R ratio moves 0.867 → 1.022 and the printed verdict flips. **The ablation caught my own
instrument**: the first version printed *"the ink is NOT painted light"* as a **constant string**
and said it at 19.2 % too. Derived now.

**CEILING, AND IT IS HARD.** The red's hue gap is real and large — **G/R 0.114 in the photograph
against 0.462 in the render** — and it **cannot be split between paint and illuminant with what we
hold.** The only near-neutral surface in the crop is the silver, and `script_gen.SILVER_CHROMA` is
the photograph's own measured silver carried into the render, so its G/R agreeing on both sides is
**BY CONSTRUCTION, not evidence.** W6 makes colour his call. **Reported, NOT acted on.**

### §2.2 ITEM C — BOTH FAILING ROWS ARE ONE UNKNOWN, AND IT IS AN INSTRUMENT

The brief called them *"both measured, both model-side"*. **The second half does not hold.**

| reading of the SAME aspect difference | value | verdict at the 5 % bar |
|---|---|---|
| raw reference pixels | **+0.94 %** | PASS |
| the map's own vertical scale | **+2.86 %** | PASS |
| `k_t` (SPEC 10.34) — **the reading that is quoted** | **+5.23 %** | **FAIL** |

`flank_compare.py`'s header already said the two vertical instruments *"disagree by 2.3 % at the
hub"* and that *"one of the two instruments is 2.3 % out"* **without saying which**.

**HEIGHT, ASPECT AND AREA ARE NOT THREE WITNESSES** — `ref_area` is `(flank_mpp / flank_kv).sum()`,
so all three are reductions of the same two masks through the same instrument.

**`Senor` IS THE SAME UNKNOWN, NOT A SECOND DEFECT.** `senor_trace.py` scores **0.913 IoU** against
the measured 934 px mask, so the glyph is not in question. New ablation **`T1_FC_ZSTRETCH`**:

| stretch | 1.000 | 1.020 | 1.040 | 1.060 | 1.080 |
|---|---|---|---|---|---|
| IoU / ceiling | 0.888 | 0.910 | **0.920** | 0.910 | 0.892 |
| `Senor` of ceiling | 0.483 | — | 0.712 | **0.795** | — |

A clean parabola, vertex **1.0398**; at 1.056 the worst region becomes `i` at 0.770 and **the row
PASSES**. **One quantity — the panel's height — accounts for BOTH failing rows.**

**AND THAT OPTIMUM IS NOT INDEPENDENT EVIDENCE.** The reference mask is carried into the metric
frame by the **same `flank_kv`**, so stretching the render to overlap it improves the overlap
**circularly**. What IS independent points the other way: `tex/senor.png` was authored from the
reference's **RAW pixels** (AR 2.357 against the bbox's 2.3478) and in raw pixels the render is
+0.94 %; and the file's own physics says the **horizontal** scale must be the smaller of the two for
an oblique view of a vertical plane, and it is not (220.45 against 215.5) — so if the map is sound
then `k_t` is too small and the render may not be short at all.

**SO `SCR` WAS NOT STRETCHED.** It would encode one instrument's 2.3 % error into the geometry that
instrument exists to measure. No bar and no verdict was changed. **WHAT WOULD CLOSE THIS: one
independent vertical scale on `ref_side.jpg`'s flank plane.**

### §2.3 ITEM 2 — THE CHIP GATE IS DEAD ON THE RED SHELL, AND THE TRUE NORMAL IS NOT THE FIX

`t1_mats.py` builds `EDGE = 1 - dot(bevel_normal, geo["Normal"])` — the **shading** normal — while
its own design note says `true_normal`. Asked the mesh first: `T1_body` **61 737 polys, 100 %
smooth**; `counter` **26 polys, 0 % smooth**.

| frac > `W_EDGE_LO` | as shipped | on `True Normal` | |
|---|---|---|---|
| flank (`T1_body`) | 0.002668 | 0.134578 | 50.4× |
| rear arch lip (`T1_body`) | **0.000000** | 0.208417 | dead → alive |
| counter (FLAT, **the control**) | 0.013771 | 0.013771 | **1.00×** |

**PAINTED** (`probe_scratch/rev55_tn_flank.png`, `probe_scratch/rev55_tn_arch.png`): as shipped **the whole red
shell is BLACK** — no edge signal at any arch lip, aperture or shut line. **So the red carries no
edge chipping at all**, while SPEC §3 and his rev-53 narrowing (*"WEATHERED is NARROWED to the red
and the running gear"*) both require that it should.

**AND THEN THAT CONCLUSION WAS REFUTED BY THE NEXT MEASUREMENT.** On a smooth mesh the true normal
is **piecewise constant**, so `1 - dot(bevel_n, true_n)` fires across **every facet boundary** of a
curved panel: it detects **TESSELLATION, not folds** — the very flaw this construction exists to
escape. The direct test is the vertex count:

| frac > `W_EDGE_LO` | `T1_SUB=1` | `T1_SUB=2` (3.8× polys) | |
|---|---|---|---|
| flank, arm T | 0.134578 | 0.112530 | **−16 %** |
| arch, arm T | 0.208417 | 0.100381 | **−52 %** |
| flank, arm S | 0.002668 | 0.002675 | +0.3 % (stable) |

**A quantity that halves when you subdivide is not measuring the vehicle.** And looking settles it
(`probe_scratch/rev55_ASK_truenorm.png`): under `T1_TRUENORM=1` the trunk lid — **CREAM** — comes up
**blotched across its whole face**, against his settled *"Follow the photograph — clean cream"*.

**SO: on FLAT geometry the gate works and every rev-53/54 counter result stands. On the SMOOTH red
shell NEITHER SOCKET IS RIGHT** — `Normal` is dead, `True Normal` counts facets — **and the red's
edge wear is UNBUILT and cannot be built by changing this link.** `T1_TRUENORM=1` is the lever that
demonstrates it. **DO NOT MAKE IT THE DEFAULT.** A construction that works on both has to come off
the geometry (a real crease/edge-angle attribute) and is a revision's work.

### §2.4 REFUTED AT REV 55 / STILL REFUTED — DO NOT REBUILD THESE

* **"there is cream either side of the flank ink"** — REFUTED, §2.1.
* **"the flank ink is painted too light"** — REFUTED: 1.1 % against a 10.7 % spread, §2.1.
* **"the two `flank_compare` failures are model-side"** — REFUTED, §2.2. They are one instrument.
* **"height, aspect and area are three independent witnesses"** — REFUTED: they share `flank_kv`.
* **"the true normal is the fix for the chip gate"** — REFUTED by the subdivision test, §2.3.
* **"the nose roundel's V arms stop short"** — still refuted (rev 54). I re-made this error off a
  half-size hero crop and it dissolved at full size. **Crops generate leads, not findings.**
* Everything rev 50/51/52/53/54 refuted — all still refuted. The cap's dome depth; the m5
  "convention conflict"; the wear field does not clone; `LID_W ≤ 1.2797 m`; A7's aft wall;
  `gal_end_f` widened to `REAR_W/2`; **"ONLY THE WORST-REGION NUMBER IS ROBUST"**; the fascia fold
  is silent; the fascia is unchanged when the radius changes; the fascia's bottom edge is a butt
  joint; rev 52's sub-pixel radius claim.
* **§2b of the rev-52 brief — HIS SETTLED RULINGS — IS UNCHANGED AND STILL BINDING.** W6 (keep the
  studio rig; **a G/R shortfall on any surface is NOT a paint error**); the roof strips' 0.3 m
  retired; the wipers withdrawn entire, commented not deleted; the lower bay SHUT; the RED bus is
  the target and **paint and artwork do not transfer between vehicles**; the tail board IS on the
  vehicle; the marks above the burst are STARS. **Do not re-open or re-ask any of them.**
  `playa_env.py` is not on the table. **And rev 54's ruling stands: "Keep studio, fix the model" —
  an environment-lit hero was offered explicitly, with the gain stated, and DECLINED.**

### §2.5 REV 55 ASKED HIM NOTHING

Everything above was measurable without him. **One question was prepared and then withdrawn by its
own evidence**: `probe_scratch/rev55_ASK_truenorm.png` was built to ask whether to switch the chip
gate's normal, and the subdivision test refuted the proposal before it was put. **Do not put that
question.** The open question that IS his is §3.1.

### §2.6 THIS FILE WAS AUDITED AGAINST THE MACHINE, AND THE AUDIT FOUND SIX THINGS

Rule 17. Every file cited below was `stat`ed, every quoted string grepped, every figure recomputed
against the probes' own printouts. **What it found:**

| what the draft said | what the machine says |
|---|---|
| `verify_clone.sh` **ALL 173 PASS** (carried from rev 55's §1) | **183** — this revision added ten rows |
| rev 54's work landed through **PR #10** | **PR #11.** #10 was rev 53's. Read off `git log`, not carried |
| the ink offsets are **+41.2/+38.6/+36.3** | **+41.3/+38.6/+36.2** on this revision's own fresh render; the rev-54 figures reproduce to <0.3 DN, so they were sound |
| `Senor` is at **0.476** of its ceiling | **0.483** on the fresh render (rev 54 read 0.476). Render-to-render, not regression |
| a draft named **`T1_EDGEBEVEL`** while calling it retired | **dropped from this brief entirely.** The `every T1_ switch the brief names exists` row sweeps every `T1_*` the brief mentions, and that one survives only in a `probe_rev53_chip.py` comment. Not naming it removes the dependency instead of re-creating it — which is what the rev-55 draft did |
| §2.3 cited the arch tile **with no directory** | **that path did not resolve.** It is `probe_scratch/rev55_tn_arch.png`, and the sibling one clause earlier was already fully qualified. **THIS IS THE SAME DEFECT REV 54'S AUDIT CAUGHT** — its ladder tile, also directory-less, also beside a qualified sibling — so it is a recurring failure mode of these briefs, not a one-off. Caught only by the `stat` sweep; re-reading passed over it twice. The other **37** paths resolved. *(Bare filenames are deliberately NOT quoted in this row: a brief that prints a broken path as an example makes its own sweep fail.)* |

**FOUR OF THE SIX WERE TRANSCRIPTION OR STALE CARRY-FORWARD, NOT MEASUREMENT**, in a file whose
own §1 says not to transcribe — and **the sixth was found only by RUNNING the audit as a script**,
which is the second revision running that the `stat` sweep caught something re-reading had passed.
**Write the sweep before you write the brief.**

**VERIFIED CLEAN BY THE SAME AUDIT** — recomputed or grepped, not re-read: every file cited below
exists (a `stat` sweep over every path this brief names); `CAP_EMBLEM_WFRAC = 0.2087` is in
`t1_detail.py`; `W_EDGE_90 = 1.0 - cos(45°) = 0.29289` recomputes exactly; 0.2087/0.814 =
**0.25639** and 0.1986/0.814 = **0.24398**; `cream_rms.spectrum(_BODY)` was RUN and returns
**0.804 / 1.135 / 1.455 / 2.201 / 3.183**, which is exactly `mottle_measure.py`'s `TARGET`;
`_BODY = (885, 968, 292, 388)`; `PXM_REF = 337.0`; `T1_body` is 61 737 polys at `T1_SUB=1` and
235 716 at `T1_SUB=2`, both read off the mesh.

**THIS FILE MUST STAY BYTE-IDENTICAL TO `PASTE_INTO_CLAUDE_CODE.txt`.** `CLAUDE.md` imports that
file into every session as the entry procedure. **WHEN YOU WRITE THE REV-57 BRIEF, `cp` IT OVER
`PASTE_INTO_CLAUDE_CODE.txt` IN THE SAME COMMIT, OR `verify_clone.sh` FAILS AND NAMES THE ROW.**

---

## §3. THE WORK LIST FOR REV 56

### §3.0 START HERE — THE ORDER, AND WHY

**He ruled "keep studio, fix the model", so this is still a MODEL revision.** Rev 55 spent itself
proving that **two of the three things the rev-55 brief called model defects were instruments**.
That is worth knowing but it does not move a pixel, so rev 56 should start with the one item that
is BOTH unblocked AND has a gate.

| # | do this | why | the gate |
|---|---|---|---|
| **A** | **THE VERTICAL SCALE ON `ref_side.jpg`'s FLANK PLANE.** Establish it independently of `k_t` and of the map. | It is the **single unknown under BOTH standing `flank_compare` failures** (§2.2). Close it and the aspect row and the `Senor` row either become real defects with a known size, or go away. Nothing else on the flank list can be attributed until it is closed. | `flank_compare.py` — the aspect row stops being instrument-dependent |
| **B** | **FINISH `cream_rms` — the NARROW version.** Point `run()` at the live re-based path and give it and `mottle_measure.py` a row. See §3.2: **the re-base is mostly DONE ALREADY**, in another file. | A second fidelity number, and two live gates that nothing currently invokes. | the script's own guards — it refuses rather than lies |
| **C** | **A9 / the three holes / A13 / A16 / A11 / A14** — the inherited model list, §3.3–3.5 | unblocked, but **no gate**, so they cannot tell you whether they improved the photograph | — |

**RENDER FIRST.** `out/` starts empty. `T1_PREVIEW=side` at **1600×1100** feeds `flank_compare.py`;
**1248×858** is the 211.5 px/m scale `cream_rms.py`'s own defaults expect. Render `hero` and **LOOK
at it.**

**A WARNING ABOUT LOOKING, EARNED AGAIN AT REV 55.** I called the nose roundel an "X" off a
half-size hero and it dissolved into a proper V-over-W at full size. **Crops generate leads, not
findings.** Take the lead, paint the window, then believe the number.

### §3.1 THE ONE QUESTION THAT IS HIS — `lid_rail`

**STILL MEASURED AT ZERO AREA, STILL GUARDED, STILL DELIBERATE.** Both objects are
**0.000000000 m² with 18 of 18 faces degenerate**. `STATE.md`'s zero-area sweep reports *"2 of 223
meshes have zero area; 2 exempt and KNOWN OPEN"*. **It is exempt in `verify.py`, not fixed, because
the rail's WIDTH is measured NOWHERE.** The exemption is two-sided and cannot outlive the defect.
**Ask it as MULTIPLE CHOICE with a crop.** Carried unchanged from rev 55, which did not ask it.

### §3.2 ITEM B, CORRECTLY SCOPED — MOST OF IT IS ALREADY DONE

Three briefs have carried *"re-base `cream_rms.py` onto `ref_rear34.jpg`, open since rev 17"*.
**Measured, that is too broad:**

* The **photograph side is LIVE**. `cream_rms.spectrum(_BODY, "ref_rear34.jpg")` runs today and
  returns **0.804 / 1.135 / 1.455 / 2.201 / 3.183 %** at sigma 1/2/4/8/12 px, 7968 px, 100 %
  unclipped. `_BODY = (885, 968, 292, 388)` is the **owner-identified** bus cream.
* The **render side exists too**, in `mottle_measure.py`, which projects a model-space patch through
  an ORTHO render (px/m exact by construction) and compares at matched physical scale against a
  `TARGET` dict — **and that `TARGET` IS those five numbers** (verified at rev 55 by running
  `spectrum()` and reading them off).

**WHAT IS GENUINELY OPEN, and it is narrower:**
1. `cream_rms.run()` — what a reader runs — is still the **dead `ref_side.jpg` legacy path** that
   refuses and prints its own remedy. Point it at the live work.
2. **Neither file has a row in either verifier.** `verify_clone.sh`'s `brief still names cream_rms`
   guards that the BRIEF mentions the string — a carrier guard, not a measurement guard.
3. The **mm axis is still not established** on that plane: `PXM_REF = 337.0` px/m is a **bracket**
   (330–344), not a measurement. **Rev 55 found that the function cited as its remedy,
   `depth_correct()`, IS DEFINED NOWHERE IN THIS REPO** — corrected in place.

### §3.3 THE TOP JOB — THE TWO VW BADGES, UNCHANGED

**The DIAMETER route on `ref_side.jpg` is EXHAUSTED** (0.3474 vs the built 0.3170 — 9.6 % small but
only **1.8 sigma**; rev 51's figure, INHERITED, do not re-run it). **The open constant is the STROKE
WEIGHT**, and rev 54 established what it denominates — **compare a frame against 0.25639, not
against `CAP_EMBLEM_WFRAC = 0.2087`; comparing against 0.2087 itself understates by 18.6 %.** The
two badge DESIGNS differ by **5.09 %** and neither has ever been compared to any frame. Full text
and the four closed routes in **`PHOTOS_WANTED_rev52.md` item 7**. `verify.py` section 13 guards the
part's SELF-CONSISTENCY (six clauses, all watched failing at rev 54) but **still nothing measures
the badge against a photograph.** **NOT A DEFECT — DO NOT REBUILD:** the badge's REACH is settled
(rev 54, 720-ray profile, all six stroke ends land on the band in both badges).

### §3.4 FINISH A9, AND THE THREE HOLES REV 52 LEFT OPEN

**A9: two of four parts done; the galley is still ~103 mm too far aft. PROVENANCE, GRADED: the
per-feature deltas are INHERITED from the rev-52 brief and have NOT been re-measured at rev 52, 53,
54 or 55.** The offset is **NOT rigid** (−0.09574 at hook u=0.13 to −0.11035 at `gal_appliance`
u=0.80, so one additive constant leaves ±7.3 mm). Re-derive each X from `BAYS`, the way `gal_rail`
now is. *(The survey's ~106 mm and its +0.096..+0.113 range are both wrong.)*

**THE THREE HOLES. PROVENANCE, GRADED: the 260.0 mm and 20.0 mm sight lines are rev 52's and have
NOT been re-measured since.** The other two WERE recomputed at rev 54's audit and reproduce exactly.
* `gal_end_f` sees past by **260.0 mm** on the show side and 20.0 mm on the off side. Needs its own
  sight line established first — **do not inherit `REAR_W/2`** (rule 34: that figure belongs to the
  rear window, which is not what looks at it).
* The **sixth hook at X −0.907 lies 51.25 mm beyond `BAYS[2]`'s own aft edge (−0.855750)**. The six
  hook stations are typed literals with irregular spacing whose span centre is **−0.705** against
  the rail's measured **−0.598**. **They disagree and one of them is wrong.**
* A7's real defect: `roof_cutters()`'s aft edge is `LID_X1`, which is **not** greppable as
  `LID_X1 = -1.0700` — the source line is `LID_X0, LID_X1 = 0.9640, -1.0700` in `t1_shell.py`, so
  **803 mm of roofed body** sits between the last light inlet and the tail skin. Unbuilt. A7 is
  **ILLUMINATION, not dressing.**

### §3.5 A13 / A16 / A12, A11's SECTION, A14, AND THE CHEAP COLOUR ITEM

**A13 / A16 / A12** — the isolated star built BELOW the burst where both red frames put it above;
every flank rosette drawn at the diameter of its **gold core**; *A12 is an OWNER RULING, not a
do-now* — `senor_trace.py` calls the remedy *"inventing ink the photograph does not show"*.

**A11's SECTION, A14** — a chrome lever lying in a dish **pressed into** the skin against a 12 mm
**proud** prism; the `lid_rail` WIDTH (§3.1).

**A CHEAP UNBLOCKED ITEM, STILL NOT DONE AFTER FOUR REVISIONS:** `SPEC` §8's colour locks are all
graded **M** = *"measured by me from `ref_source.jpeg`"* — a 246×197 thumbnail the record itself
calls retired. They can be re-derived on `ref_playa_34.png` at **4× the area** with no new
photograph. **Report the re-derived values; do not change the constants without his ruling** — W6
makes colour his call. *(And `ref_playa_34.png` is byte-identical to `IMG_3842.png`; a duplicate is
not corroboration — rule 11.)* **Rev 55 gives this a reason it did not have**: the render's flank
red reads **G/R 0.462 against the photograph's 0.114**, and the split between paint and illuminant
**cannot be recovered from what we hold** (§2.1). If the colour locks are re-derived, that is the
frame to do it in.

### §3.6 THE PROCESS ROWS, STILL OPEN

The **open-findings** register abandoned at rev 45 (21 rows); the standing-instructions carrier
deleted at rev 44, which took the **die-cut sticker — the project's original deliverable** — with
it, **still open**; SPEC §0.2's two rev-4 corrections later refuted; rev 48's refuted *"B stays
open"* still live in `build.py` and, **split across two lines so a flat grep misses it**, in
`t1_shell.py`; the tail board still has **zero rows in either verifier**.

**`flank_compare.py` WAS RE-RUN AT REV 55** on a fresh `out/r55_side.png` and still fails 2 of 4 —
read its own summary line, not its exit code:

| | rev 54 | **rev 55** | |
|---|---|---|---|
| ink area ratio | 0.9425 | **0.9446** | PASS |
| ink aspect | 2.3689 | **2.3689** | **FAIL** — and see §2.2: instrument-dependent |
| IoU vs ceiling | 0.7618 | **0.7625** | PASS |
| worst region (Senor) | 0.476 | **0.483** | **FAIL** — and see §2.2: the same unknown |

The rev-54 figures reproduce to <1 %, so they were sound and the small moves are render-to-render.

### §3.7 THE HABITS THAT PAID AT REV 55

**PAINT THE WINDOW AND LOOK AT IT BEFORE IT PRODUCES A NUMBER.** Rev 55's ground control was
painted on both frames at matched mm/px before any DN was quoted, and the true-normal probe was
painted before its coverage was believed. Both survived. The one thing NOT painted first — a
half-size hero crop — produced a wrong finding within a minute.

**A CONTROL THAT CANNOT FAIL IS NOT A CONTROL.** Rev 55's true-normal probe had **no working
control on its first run** (a typed window put 418 px of counter in frame; the probe REFUSED) and
its control **FAILED on the second** (5.98 %, on a crop with 0.80 px of bevel radius). Only the
third — window derived from the mesh, **NULL ARM** for the noise floor — could support anything.
**On a ray-traced quantity, a percentage means nothing without the sampler's own spread.**

**A CONCLUSION THAT CANNOT FAIL IS NOT A MEASUREMENT.** The ground control first printed *"the ink
is NOT painted light"* as a constant string and said it under the ablation too. `cream_rms.py` had
already earned that rule and rev 55 re-earned it.

**AND CHECK WHETHER YOUR OPTIMUM IS CIRCULAR.** Rev 55 nearly published the IoU stretch optimum as
independent evidence that the lockup is short; the reference is placed by the same instrument.

---

## §4. WHAT ONLY HE CAN GIVE

**`PHOTOS_WANTED_rev52.md` is the carrier for item 7 (ONE HUBCAP, SQUARE ON AND CLOSE)**. Items
**1–5** keep their full text in `PHOTOS_WANTED_rev49.md`: the tail board's footing; the decal darker;
the nose square on; a raking-light frame of the louvres (**ONE item — the pressing depth**; the
"block length, station and V swage" expansion is a proposal, not the record); the off side, any
frame. **He has said 1–5 are not possible now. DO NOT RE-ASK THEM.** Item 6 (an obliquely-seen
wheel) was **DISSOLVED at rev 51** — struck, not outstanding.

**CARRIED FROM REV 53, still no carrier outside these briefs:** a frame showing the cream **where it
IS chipped** — any close frame of a worn edge. **Rev 54 lowered its urgency and rev 55 lowers it
again**: the band is 0.27 px at every scale this project ships, AND the gate that would place those
chips on the red is not built (§2.3). Only worth asking if a close counter view is ever wanted.

**THE ROUTE TO THE STROKE WEIGHT, AND ITS CEILING (new at rev 54, NOT attempted at 54 or 55).**
`PHOTOS_WANTED_rev52.md` item 7 closes four routes and all four are about the **hubcap** badge;
none closes the **NOSE** badge, which is the same design — the record says so and already
**transferred its RING BAND from one to the other** (`t1_detail.py`: *"ref_workshop.jpg nose badge …
= 0.0874 / 0.0995 … ring band / ring outer D = 0.093 ± 0.012 adopted"*).
* `ref_workshop.jpg` shows the nose badge at **91.7 px vertical D, PSF sigma 0.689 px** — a stroke
  of ~0.25 R is ~11 px, **resolved**. The record's crop box **(258,494,352,604)** is correct
  (verified rev 54).
* **CEILING.** (a) `ref_workshop.jpg` is the **GREEN** vehicle and his standing ruling is that
  **paint and artwork do not transfer between vehicles**. A pressed factory badge is arguably
  GEOMETRY, which rule 11 says does transfer — **but that is an argument, not a measurement, and
  the same argument already underwrites the shipped ring band.** Either both are legitimate or the
  ring band is grounded on the wrong vehicle. **Resolve that before publishing a number from it.**
  (b) The badge is **strongly oblique** — 62.7/91.7 = **0.684 axis ratio** — so it must be
  de-projected and only vertical extents are trustworthy. (c) The RED bus's own nose roundel is in
  `ref_nolita_front34.jpg` at a **41 × 66 px** bbox — the right vehicle, but a 700×467 JPEG.
* **Scoped as a revision's work, not a spare hour.** Rev 51 spent a whole revision on the diameter
  by this kind of route and reached 1.8 sigma.

---

## §5. THE RULES — `CLAUDE.md` CARRIES THE METHOD, NOT THE NUMBERED CANON

The canon (rules 1–33) is printed in `NEXT_CONTEXT_PROMPT_rev50.md` §11. **Rules 34 and 35 live only
in the rev-51…55 briefs and `LEDGER_rev50.md` §0, so they are carried here too — that is
`CLAUDE.md`'s own rule 16 firing on this file:**

> **34. A REQUIREMENT INHERITS ITS OBJECT EXACTLY AS A RETIREMENT DOES.** Before relying on any
> *"the record requires X"*, check which object the sentence is about — and check the cited line
> exists. **Rev 52 applied this deliberately**: `gal_end_f` was left alone because `REAR_W/2`
> belongs to the rear window, which is not what looks at it. **Rev 54 applied it to a photograph**:
> item 7's four closed routes are all about the HUBCAP badge and none closes the NOSE badge (§4).
> **Rev 55 applied it to a function**: `cream_rms.py` cited `depth_correct()` as its remedy and
> that function is defined NOWHERE in this repo.

> **35. A GUARD WRITTEN AGAINST A POSE ENCODES THAT POSE.** Guards that identify a part's foot or
> free edge by `min(y)` are only right while the part leans one way. Ask the geometry.
> **Rev 53 broke this and was caught by it**; **rev 54 broke it again** — a global `min(z)` for a
> fold that SLOPES, wrong by 25 mm; **rev 55 broke it a third time** — a TYPED crop window for the
> counter control that caught 418 px of it, rederived from the mesh.

> **Rule 29.3:** no finding is attributed to a cause until a control separates it. **Rule 29:** a
> retirement inherits the object it was made about. **Rule 15:** a retraction that lands in a ledger
> and not in the source is half a retraction — **rev 55's withdrawal of "the true normal is the
> fix" is in `t1_mats.py` and in the probe's own printed verdict, and two rows hold it there.**

---

## §6. THIS MACHINE

```
cores 4   RAM 15 GB   Blender 4.5.3 via pip install bpy   subagent concurrency 2
build  T1_SUB=1 ~20 s     render 1600x1100 96 spp ~4-7 min PER VIEW
```

```bash
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
T1_PREVIEW=side T1_PFX=r56 T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
  /tmp/blender/blender -b -P build.py
T1_PREVIEW=hero34r ...                                       # the REAR 3/4 -- A7 lives here
T1_SUB=2 /tmp/blender/blender -b -P audit.py                 # rewrites STATE.md -- COMMIT FIRST
python3 lid_gen.py                                           # regenerates tex/lidmural.png
python3 flank_compare.py out/r56_side.png /tmp/fc.png        # THE FIDELITY GATE.  Exits 1 today.
python3 -c "import cream_rms as C; C.spectrum()"             # the LIVE photograph-side cream
python3 probe_rev53_chip.py                                  # the chip measurement, all six arms
T1_SUB=1 T1_AOVSAMP=64  /tmp/blender/blender -b -P probe_rev54_aov.py    # the EDGE AOV + sweep
T1_SUB=1 T1_LOOKSAMP=192 /tmp/blender/blender -b -P probe_rev54_look.py  # the scale ladder
/tmp/blender/blender -b -P probe_rev54_wfrac.py              # the badge denominator, calibrated
T1_SUB=1 /tmp/blender/blender -b -P probe_rev54_badge.py     # the badge off the built mesh
T1_SUB=1 T1_TNSAMP=64 /tmp/blender/blender -b -P probe_rev55_truenorm.py  # RUN IT AT SUB=1 AND 2
```

**`out/` IS NOT TRACKED and starts empty. Render before quoting any probe that reads a frame.**
**A backgrounded runner's exit code is the WRAPPER'S, not Blender's — grep the log for `Saved:`.**
**`probe_rev54_aov.py` and `probe_rev55_truenorm.py` write EXR into `probe_scratch/` — rev 55
deleted them before committing and kept the PNGs.**

**ABLATIONS — every one exists to WATCH A GUARD FAIL.**
**NEW AT REV 55:** `T1_FC_INKGAIN` (adds DN to the RENDER's flank ink only, ground untouched — the
"artwork painted too light" case; at +30 the ink/ground R ratio moves 0.867 → 1.022 and the verdict
flips), `T1_FC_ZSTRETCH` (stretches the render's lockup mask vertically before scoring; the IoU
parabola peaks at 1.0398), and **`T1_TRUENORM`** (swaps the chip gate's dot product onto the true
normal — **a DEMONSTRATION, not a fix; see §2.3, and do not make it the default**).
Carried: `T1_PTWEAR=1` (restores the Pointiness chip gate and moves nothing else — proven by render
at rev 53: **8.795 %** under the switch against **8.826 %** when Pointiness was the default and
**0.000 %** shipped) and **`T1_EDGERAD`** (the Bevel radius in **millimetres**; unset keeps the
derived `GAPW/2`; rev 54 swept it at 1 / 2.75 / 6 / 12). Also live: `T1_TARNCONTAM=1`,
`T1_RAILSTALE=1`, `T1_ENDSHORT=1`, `T1_CAPSINK=1`, `T1_LIDDEG=104`, `T1_BAYSTALE=1`,
`T1_LAMPSINK=1`, `T1_LIDASPECT=1.2`, `T1_HANDLEHI=1`, `T1_BAREMAT=1`, `T1_TBFOOT=1`,
`T1_BAYPROUD=1`, `T1_NOBEVEL=1`, `T1_BEVEL_SAMPLES`, `T1_FC_OLDDATUM=1`.

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
shipped passed `VERIFY: 0 fail, 0 warn` and was found by looking at a crop. **Rev 55's whole item-2
result turned on this: the coverage numbers said the gate was suppressed, and only the painted
window said the red shell was BLACK — and only a LOOK at the cream lid said the obvious fix was
wrong.**

**When you need something from him, ask as MULTIPLE CHOICE with the reference material attached — one
crop, one mark, one sentence — and ASK IT WITH THE QUESTION TOOL.** He has never stood in the bus: do
not ask what the real vehicle looks like, ask what a PHOTOGRAPH shows. **Rev 55 asked him nothing** —
everything it did was measurable without him, and the one question it prepared was withdrawn by its
own evidence (§2.5). **The question that is his is §3.1, `lid_rail`.**

**`git rev-list --count origin/main..HEAD` before you start and again before you finish. And
`git diff --name-only HEAD...origin/main` — that is where his photographs arrive. EVERY session.**
