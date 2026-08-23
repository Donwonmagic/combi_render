# LEDGER rev 56 — the flank's vertical scale, and three dead instruments

Every number here was printed by a script in this repository. Where a figure is
inherited it says so. Where something could not be established it says that
instead of guessing.

---

## §0. WHAT THIS REVISION CHANGED, IN ONE TABLE

| | before | after |
|---|---|---|
| `flank_compare.py` | **FAILS 2 of 4** | **FAILS 1 of 4** |
| `mottle_measure.py` | never run; beauty arm prints five `ratio 0.00` rows | **RUNS**; beauty arm REFUSES, albedo arm gives a real spectrum |
| `cream_rms.run()` | dead `ref_side.jpg` path, returns `{}` | the live re-based spectrum |
| zero-area meshes | 2 of 223, 2 exempt | **0 of 223, 0 exempt** |
| `verify_clone.sh` | 203 rows | **221 rows** |

Two of those are fidelity gates. The brief's §0 says making a second gate run
is the progress that counts, and that is what §2 and §3 below are.

---

## §1. PICKUP, MEASURED

Rev 55 **was merged**, through **PR #14 and PR #15** — *not* "no PR opened,
because none was asked for", which is what the rev-56 brief predicted. Believe
the output, not the paragraph.

* HEAD `claude/bus-model-rev56-62lam6` **0 ahead / 0 behind** `origin/main`
* every remote branch **0 ahead**; `main` 199 behind
* `git diff --name-only HEAD...origin/main` **empty** — no photographs arrived
* `bootstrap.sh` **ALL 10 PASS**, row 9 (`no branch carries work HEAD does not
  have`) passing. **Row 9, not row 10** — confirmed again off the machine's
  own output.
* `verify_clone.sh` **ALL 203 PASS**
* `git fetch --prune` printed
  `- [deleted] (none) -> origin/claude/bus-model-rev56-62lam6`, so **this
  revision's own designated branch had already been deleted remotely before
  the revision started** — the sixth deletion in the rev-51…56 series, and the
  first to hit the branch the incoming brief named for the current revision.

---

## §2. ITEM A — THE VERTICAL SCALE. THE CARRY LAW WAS THE WRONG POWER

The brief asked for one independent vertical scale on `ref_side.jpg`'s flank
plane, and said both standing `flank_compare` failures sit under it.

### §2.1 The answer, and it is a proof rather than a measurement

`flank_kv()` carried `k_t` off the rear hub by the map's **full horizontal
ratio**. For a projective image of a vertical plane with a level camera the
depth along the optical axis is **affine in x**, so

```
k_v = f / Zc                    vertical  -> 1/Z
k_h = a1^2 * A / Zc^2           horizontal -> 1/Z^2   (distance AND foreshortening)
```

The horizontal scale falls off as the **square** of the depth and the vertical
as the first power, so **k_v is proportional to sqrt(k_h)**. Through the map's
own `u + B = A/(x + C)` that makes k_v **LINEAR in (u+B)**. The shipped law was
**QUADRATIC in (u+B)** — it applied the depth correction twice.

**Watched on a synthetic camera where the answer is known by construction**
(`probe_rev56_kv.py` Part 1 — a pinhole camera, the same Möbius map fitted to
it to 1.5e-11 px, both laws scored against the truth):

| x | u | TRUE k_v | LINEAR | QUADRATIC |
|---|---|---|---|---|
| +1.300 | 330.87 | 208.491 | **208.491** | 199.529 |
| +0.700 | 454.86 | 210.756 | **210.756** | 203.887 |
| 0.000 | 602.97 | 213.462 | **213.462** | 209.156 |
| −0.500 | 711.11 | 215.437 | **215.437** | 213.045 |
| −1.100 | 843.55 | 217.857 | **217.857** | 217.857 |

worst error over the wheelbase: **LINEAR 0.0000 %, QUADRATIC 4.299 %**.

**The verdict is derived, and it caught its own threshold.** The first version
compared fractions against percentages and printed `INCONCLUSIVE` on a run
where the laws had separated by 4.3 %. A constant string would have shipped.

**Error budget, by ablation.** The linear law survives camera tilt (3°, 8°),
roll (2°, 6°), 100 mm/m of tumblehome (0.002 %) and radial distortion severe
enough to leave 4 px of map residual (0.47 %). So its error is bounded by the
map's own fit quality, which is sub-pixel.

Worth **+2.45 %** at the lockup centre (205.3 → 210.4 px/m) and **+4.3 %** at
the front hub.

### §2.2 "One of the two instruments is 2.3 % out" is WITHDRAWN

`flank_compare.py`'s header argued that for an oblique view of a vertical plane
the horizontal scale must be the **smaller** of the two, that it is not
(220.45 against `k_t`'s 215.5), and therefore that one instrument is 2.3 % out
— without saying which. **The first clause is false for this geometry.** The
true anisotropy is

```
k_h / k_v = a2 * (u + B) / (u0 + B)
```

which **exceeds 1 wherever the column is aft of the principal point**, and the
rear hub is. The old law hid this by making `k_h/k_v` **constant along the
whole flank**, which no projective image of a plane does.

**Measured, not argued.** `ref_side.jpg`'s rear wheel disc is a circle in a
plane parallel to the flank, so its imaged W/H **is** the local anisotropy —
depth cancels in a ratio, and it sits at the very column `k_t` was taken at.

* gradient-peak radial trace, **1441 rays**, radial sd **0.34 px**
* fitted centre **u = 749.26**, against `U_RHUB` = **749.38**
* **W/H = 1.00417 ± 0.00048** (spread over five search brackets)
* shear-corrected (the drip rail's own −0.04409 image slope) → **k_h/k_v = 1.00516**
* the shipped pair implies **1.02297**. They differ by **−1.74 %**.

**Calibrated before it was believed:** a known vertical squash was planted in
the frame and recovered to **0.2 %**. **A window was rejected:** the concentric
red hubcap boundary returned radial **sd 2.13 px** — it is not a circle, and
the residual said so rather than a person deciding it looked wrong.

**And the first two masks ran to the crop border** — plain colour rules on the
wheel crop caught the body red above and the road below
(`probe_scratch/rev56_mask_cream.png`, `rev56_mask_red.png`). That is rule 8's
defect, caught by painting the selection and looking at it.

### §2.3 What was APPLIED and what was only REPORTED

**Applied:** the carry law only. It is a proof about the map's *shape* and it
does not touch the anchor.

**Reported, not applied:** re-anchoring `k_t` to the wheel, which would put
k_v(hub) at **219.32** rather than 215.5. It collides with SPEC §10.34's own
validation of `k_t` — belt → aperture top reads 500.9 mm measured against
503.0 built, **−0.4 %**, and under the wheel anchor that becomes **−2.2 %**.

**And a third reading disagrees with both.** The traced disc is **93.09 px**
across; against `t1_core.RIM_R`'s flange OD of **0.4396 m** that puts k_h at
**211.8**, not the map's **220.5**.

> **THREE QUANTITIES, TWO EQUATIONS. Which absolute is right CANNOT BE
> RECOVERED FROM WHAT WE HOLD** without one more independent absolute on this
> plane. That is a result, not a deferral.

**The aspect row does not need that absolute** — it is a width over a height,
so only the *anisotropy* at the lockup enters and neither absolute survives
into it. That is why the carry law settles the row while the anchor stays open.

### §2.4 The gate, before and after, on a fresh 1600×1100 render

| | before | after | |
|---|---|---|---|
| ink area ratio | 0.9445 | **0.9669** | PASS, and closer to 1.000 |
| ink aspect | 2.3689 vs 2.2512, **+5.23 %** | 2.3689 vs 2.3259, **+1.85 %** | **FAIL → PASS** |
| IoU vs ceiling | 0.7617 | 0.7506 | PASS |
| worst region (`Senor`) | 0.478 | **0.644** | still FAIL, bar 0.75 |

Quoted off `out/r56b_side.png`, rendered **after** the `lid_rail` geometry
change, so the figures are the ones a reader reproduces from this HEAD. The
run before that change read 0.9699 / 0.7509 / 0.652 on the same three rows —
**render-to-render, not a regression**, and the aspect row is identical to four
decimal places in both.

All three alternative aspect readings now **agree** — +1.85 / −0.44 / +0.94 %
— where they spanned 4.3 points before.

**WATCHED FAILING.** `T1_FC_KVQUAD=1` restores the old law and reproduces the
old verdict exactly: aspect **+5.23 % FAIL**, area **0.9445**.

### §2.5 Rev 55's stretch parabola is explained, and rev 55 was right

Rev 55 measured an IoU stretch optimum at **1.0398** and refused to stretch
`SCR`, on the grounds that the optimum was circular. The instrument correction
the wheel implies at the lockup is **1.0428**. **Two routes sharing no datum
— mask overlap on one side, a traced circle and the map's shape on the other —
agree to 0.4 %.** The reference was being placed too tall. **The model was not
short.** Rev 55's refusal was correct and is now explained rather than merely
vindicated.

### §2.6 What the front wheel could NOT do

The obvious second leg — the front rim disc, for the carry law over a 500 px
lever arm — **was refused**. Under contrast stretch it yields two shadowed
arcs and no recoverable outer boundary
(`probe_scratch/rev56_frontwheel_stretch.png`), and identifying those arcs with
the rear disc's outer boundary is exactly the unverified window this project
has been burned by. **No number was published from it.**

The **serving-aperture band** route was also dropped, and for a better reason:
the glass is not dark. Vertical luma profiles through all three bays show the
apertures full of reflections and a white shirt, so a "dark glass" rule would
have selected the wrong pixels in a measurement whose whole point was a
constant 403 mm. **Checked before it produced a number.**

---

## §3. ITEM B — A LIVE MEASUREMENT BEHIND A DEAD ENTRY POINT, AND A DEAD GATE

### §3.1 The re-base was never the open part

Three briefs carried *"re-base `cream_rms.py` onto `ref_rear34.jpg`, open since
rev 17"*. The re-based measurement **has been written in that same file since
rev 17/19 and returns a real spectrum today**. What was open was `run()` — what
a reader actually runs — which still pointed at `ref_side.jpg`, hit the rev-17
hard guard, printed `LEGACY PATH, RESULT IS NOT CREAM` and returned `{}`.
**Eight revisions of no number from the function whose name says "run".**

`run()` now reports the live path: **0.804 / 1.135 / 1.455 / 2.201 / 3.183 %**
at sigma 1/2/4/8/12 px on the owner-identified `_BODY` patch (7968 px, 100 %
unclipped), plus `character()`'s derived verdict, plus the render arm's command.

**No colour-gated render arm was added, deliberately.** A colour gate on a
render of the surface whose colour is under test is circular. `run()` refuses
and names the real arm rather than producing a second number that would look
like corroboration.

The dead path is **kept** behind `T1_CR_LEGACY=1`: it is what demonstrates why
the re-base was necessary.

`mottle_measure.py`'s `TARGET` was five typed literals — a transcription of
`spectrum()`'s output. It is **derived** now, and raises rather than falling
back if that call refuses. Drift against the literals is printed every run:
**0.0004 pp**.

### §3.2 The render arm was RUN for the first time and it was DEAD

`mottle_measure.py` has existed since rev 19 and **nothing ever invoked it**.
Run end to end, the beauty arm came back with its patch **100.00 % CLIPPED** —
mean L\* exactly 100.00, mean C\* exactly 0.00, every high-pass RMS 0.000, every
ratio **0.00**. The cream band renders **pure white**:
`shader_solve._render()` builds no studio rig and the file execs `build.py`
without `T1_PREVIEW`, so nothing sets the exposure the cream was balanced for.

**Looked at, not inferred** — `probe_scratch/rev56_mottle_frame.png` is the
frame with the patch drawn on it and the whole cream band is blown flat.

Five printed `ratio 0.00` rows read as *"the model has no mottle at all"*. They
were a measurement of nothing. **It refuses now**, and the refusal is **hoisted
to before the first printed number** — the existing `too few px` guard sat at
the very END of the file, after the BASE LEVEL block and the character table
had already put `nan` and `0.000` on the console. **A refusal that arrives
after the numbers is not a refusal.**

### §3.3 THE SECOND GATE NOW RUNS

Albedo arm, 3696 px, **0.00 % clipped**, stable to ±0.01 across 16 / 32 / 48
samples so it is not sampler-driven:

| mm | target % | render % | ratio |
|---|---|---|---|
| 3.0 | 0.804 | 0.496 | **0.62** |
| 5.9 | 1.135 | 1.008 | 0.89 |
| 11.9 | 1.455 | 1.805 | 1.24 |
| 23.7 | 2.201 | 2.941 | **1.34** |
| 35.6 | 3.183 | 3.631 | 1.14 |

**The render's cream breakup is too weak at fine scale and too strong at coarse
scale — the model's mottle is too coarse-grained.** That is a *shape*
difference, not a level one, so it does not wash out under the open px/m
bracket.

**A second, level-free difference.** `corr(dL*,dC*)` on the render is
**+0.199 / +0.173 / +0.200** at 5.9 / 11.9 / 23.7 mm, where the photograph goes
**negative with scale** (+0.042 / −0.106 / −0.294). The photograph's cream is
chalky sun-fade — patches oxidised lighter **and** less chromatic — and the
render's is luminance-dominated with chroma weakly co-varying. Being a
correlation it carries no scale and no exposure.

**CEILING, STATED.** The C\* base-level row (render 3.89 against 21.44, ratio
0.181) is **not admissible as it stands**: it compares an **albedo** against an
**observed pixel**, which is SPEC §10.21's trap. Reported, not acted on.

**NOT FIXED, and said so:** making the beauty arm live means building the
studio rig inside that file, which changes what it measures. Rev 57's job.

### §3.4 Still open, unchanged

The **mm axis** on that plane. `PXM_REF = 337.0` px/m is a bracket (330–344),
not a measurement. Untouched this revision.

---

## §4. §3.1 OF THE BRIEF — `lid_rail` WAS ASKED AND ANSWERED

Both objects measured **0.000000000 m²** with 18 of 18 faces degenerate: the
loop ran `(LID_X0, LID_X0)` and `(LID_X1, LID_X1)` and `_rag_grid` interpolates
`x = x0 + (x1-x0)*ix/nx`, so every vertex landed at one station. The rail the
source describes was **in no render**.

**Asked as multiple choice with a marked crop** of `ref_workshop.jpg`
(`probe_scratch/rev56_ASK_lidrail.png`, the aft end of the roof opening with
the lid propped). **The owner's answer: "Narrow lip, ~as wide as it is tall".**

So the width is **not a second free constant — it IS `RAIL_PROUD`**, and the
source reads `RAIL_PROUD` rather than a literal. `ref_workshop.jpg` is the
**GREEN** vehicle: this is **geometry**, which rule 11 says transfers, and no
paint or artwork is taken from it.

**The exemption retired itself.** Rev 52 wrote it two-sided so it could not
outlive the defect, and on the first build after the width landed the stale arm
**FAILED and named both objects**. Removed. The sweep now reads **0 of 223 with
0 exempt**, so a future zero-area part has nowhere to hide.

**WATCHED FAILING:** `T1_RAILFLAT=1` restores `xa == xb` and VERIFY goes
0 fail → **3 fail** (the zero-area sweep, now a hard fail, plus the width guard
on each object).

### §4.1 MY OWN PROBE WAS WRONG TWICE, WHICH IS THE NORMAL RATE HERE

Rule 4 says budget for it. Both errors would have produced a plausible
published number.

1. **It compared a DROPPED vertex against the AUTHORED `roof_z`** and reported
   the rail **43.7 mm BELOW the roof**. Different frames: `build.py` step 8b
   shears every vertex by `RIDE_DROP` after authoring and `roof_z` returns the
   un-dropped surface, so the residual is exactly `drop(x)` — 64.8 mm at the
   fore rail, 29.1 mm at the aft one, which is what the two readings were.
2. **It used a 1e-9 tolerance on float32 vertex storage** and reported the aft
   rail poking outside its own aperture. It does not.

Re-done **frame-free** — raycast down onto the built body — it reads
**dx 0.0213 m = RAIL_PROUD**, minimum gap **+21.9 mm** above the built roof
skin, both rails inside the aperture x-range. The tolerance in the shipped
guard is **0.5 mm**, with that reason written next to it.

---

## §5. WHAT THIS REVISION DID **NOT** DO

Stated plainly, because a brief that only lists wins is a brief that gets
believed.

* **§3.3, the two VW badges — the top job — WAS NOT TOUCHED.** The nose-badge
  stroke-weight route off `ref_workshop.jpg` is now **three revisions
  un-attempted** (54, 55, 56). §0.1 forbids reading its cost as a reason to
  defer it, and this revision deferred it anyway. **It is rev 57's first
  item after the anchor.**
* **A9 / the three holes / A13 / A16 / A11 / A14** — untouched.
* **SPEC §8's colour locks** — untouched, still graded **M** off a retired
  246×197 thumbnail.
* **The process rows** — the open-findings register, the die-cut sticker
  carrier, the tail board's zero verifier rows — all untouched.
* `flank_compare`'s **worst-region row still FAILS** at 0.644 against a 0.75
  bar. It improved from 0.478 but it is not closed, and the residual is
  localised: the overlay shows `Senor` as reference-only red at the top-left
  while `Tacombi` now overlaps almost entirely.

---

## §6. REFUTED THIS REVISION — DO NOT REBUILD THESE

* **"the two vertical instruments disagree by 2.3 % and one of them is out"** —
  REFUTED. They differ by the anisotropy they *should* differ by; the residual
  is 1.74 %, and the phantom came from a false premise about which scale must
  be smaller.
* **"for an oblique view of a vertical plane the horizontal scale must be the
  smaller of the two"** — REFUTED. True only forward of the principal column.
* **"`flank_kv` carries `k_t` correctly"** — REFUTED, and by construction.
* **"the render's flank lockup is short in height"** — REFUTED as a *model*
  claim. The reference was placed 4.3 % too tall.
* **"the re-base of `cream_rms` onto `ref_rear34.jpg` is open"** — REFUTED. It
  has been done since rev 17; the entry point was what was dead.
* **"`mottle_measure.py` compares the render against the target"** — REFUTED
  until this revision: its beauty arm measured a saturated patch and printed
  five zeros.
* **"`lid_rail`'s width cannot be established"** — REFUTED. The owner answered
  it from a frame already on the repo.

Everything rev 50–55 refuted is **still refuted**, including §2b of the rev-52
brief (his settled rulings), which is unchanged and still binding.
