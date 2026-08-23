# OPEN FINDINGS — the live register

**This is a CARRIER (`CLAUDE.md` rule 16). It is not yours to compact, prune or
summarise. Rows leave it only by being CLOSED with the measurement that closed
them, or RETIRED with the ruling that retired them — never by being dropped.**

An open-findings register existed once and was **abandoned at rev 45 with 21
rows**, and the loss went unnoticed for eleven revisions. The
standing-instructions carrier went the same way at rev 44 and took the
project's original deliverable with it (**F18** below). This file is the
register reinstated at rev 56, seeded only from findings that could be
grounded in the repository on the day it was written.

## How to use it

* **Every row carries a PROVENANCE GRADE.** That is the point of the file.
  * `MEASURED-revN` — a script in this repo printed it in revision N.
  * `RECOMPUTED-revN` — re-derived from source in revision N, agreeing with an
    earlier figure.
  * `INHERITED-revN` — carried from revision N's prose and **not re-measured
    since**. Treat every one of these as a claim, not a number.
  * `RULED-revN` — the owner decided it.
  * `CEILED` — established as far as the material allows; *"it cannot be
    recovered from what we hold"* is the result.
* **Add rows; do not renumber them.** IDs are permanent. A closed row keeps its
  ID and its number, with `CLOSED-revN` and the measurement that closed it.
* **Grade decay is a finding in itself.** An `INHERITED` row that survives three
  more revisions without being re-measured should be re-measured or downgraded
  to a claim, not quietly re-quoted.
* `verify_clone.sh` asserts this file exists, that the newest brief names it,
  and that every OPEN row carries a grade.

---

## A. THE TWO LIVE FIDELITY GATES

| ID | finding | status | figure | grade |
|---|---|---|---|---|
| **F01** | `flank_compare` worst region `Senor` below its bar | **OPEN — narrowed to the ARTWORK at rev 57** | **0.656** against a 0.75 bar on `out/r57_side.png` (0.644 at rev 56, 0.478 before rev 56's carry-law fix). See **F39** for whose defect it is | MEASURED-rev57 |
| **F02** | The flank plane's ABSOLUTE vertical scale. Three readings at one station disagree | **OPEN** | map k_h **220.45**, `k_t` **215.5**, flange-OD route **211.8** px/m. Three quantities, two equations | MEASURED-rev56, CEILED |
| **F03** | *"The render's cream mottle is the wrong SHAPE — too little fine structure, too much coarse"* | **REFUTED-rev57 AS A MOTTLE FINDING — and the diagnosis was INVERTED.** Ablated, not argued: turning the mottle **entirely off** moves the gate by **1.1–2.0 %** against a **7.7–35.0 %** gap; `MOTTLE_M` over a factor of six closes 3 points of 33; **doubling the amplitude moves the coarse row the WRONG WAY, 1.35 → 1.38**. Painted: the mottle **IS** the fine-scale term (`probe_scratch/rev57_alb_diff.png`), and the coarse cloud that dominates is not it (`probe_scratch/rev57_alb_off.png`). **DO NOT TUNE `MOTTLE_M`** | on this head 0.67 at 3 mm, 1.35 at 23.7 mm; the mottle alone is sd **0.2594 DN** of a **4.000 DN** breakup = **6.5 %** | **MEASURED-rev57** |
| **F04** | The cream's CHARACTER has the wrong sign — level-free and scale-free | **OPEN, but NOT a mottle finding either** (F03): whatever carries the sign is the same 93.5 % that F43 is about | `corr(dL*,dC*)` render **+0.216/+0.194/+0.224** on this head, photograph **+0.042/−0.106/−0.294** | MEASURED-rev57 |
| **F05** | `mottle_measure.py`'s BEAUTY arm cannot run — the cream blows out because `shader_solve._render()` builds no studio rig | **OPEN — and rev 57 PROMOTED it: it is now the BLOCKING item for the mottle, not a nicety.** The albedo arm is blind to the roughness half of the mottle by construction (F41), so the beauty arm is the only one that could ever see it | patch **100.00 %** clipped | MEASURED-rev56, re-ranked rev57 |
| **F06** | The mm axis on the `ref_rear34.jpg` cream plane is not established, and it sets F03's whole x-axis | **OPEN** | `PXM_REF = 337.0` px/m is a **bracket** (330–344) | INHERITED-rev19 |
| **F07** | The C\* base-level comparison is inadmissible as it stands — ALBEDO against OBSERVED PIXEL, SPEC §10.21's trap | **OPEN** | render 3.89 vs 21.44, ratio 0.181 — **reported, not acted on** | CEILED-rev56 |

## B. THE TOP JOB

| ID | finding | status | figure | grade |
|---|---|---|---|---|
| **F08** | **The two VW badges' STROKE WEIGHT.** The nose-badge route on `ref_workshop.jpg` was **TAKEN AT REV 57** after three revisions of deferral, and it **does not close**. Two estimators that each recover the built glyph EXACTLY from a synthetic blurred to this frame's PSF disagree by **47 points and in opposite directions** on the photograph, and each is refuted by its own painted window (threshold eats the pressing's SHADOW, best IoU 0.537 running away to width x1.80; the level-free edge fit LOCKS ONTO THE SPECULAR HIGHLIGHT). The divergence is the TARGET, not the tools: on the RING BAND of the same badge in the same frame the two agree to **0.8 %** | **OPEN — but no longer un-attempted, and no longer the top job by gate availability** | BUILT **0.20455** of the ring outer R, off the mesh, all six strokes to 0.13 % (= 0.10227 of the outer D, 28.69 mm on 280.56 mm). Frame bracket **0.14318 .. 0.23985** (**-30 % .. +17 %**): the built value is INSIDE it, so the frame does NOT refute it, but the bracket is 47 points wide against the 5.09 % it was meant to see. **NO STROKE NUMBER PUBLISHED** | **CEILED-rev57** |
| **F09** | That route's ceiling — is the GREEN vehicle's nose badge legitimate ground? | **CLOSED-rev57 — and it was never the blocker.** The frame is already load-bearing in the shipped model in **two** places, not one: the ring band (`t1_detail.py`, *"ring band / ring outer D = 0.093 +/- 0.012        adopted"*) and the glyph's own fit radius, which runs through `_BAND_FRAC = 0.028 / 0.140` and so through that same band. A third use would have been no worse. **What blocks the stroke weight is the FRAME, not the vehicle** — F08 | this probe's own 50 %-level conic: vertical D **92.728**, horizontal **63.299**, radial resid **0.2345 px**, 685 rays | **MEASURED-rev57** |

## C. THE GALLEY CLUSTER — RE-MEASURED AT REV 56, ALL FOUR REPRODUCE EXACTLY

*Carried as INHERITED-rev52 for four revisions. Re-derived off the built mesh
at rev 56; every figure reproduced, so the grade is upgraded — the numbers were
sound, they were merely unverified.*

| ID | finding | status | figure | grade |
|---|---|---|---|---|
| **F10** | The galley sits too far aft, and the offset is **NOT rigid**, so one additive constant cannot fix it | **OPEN** | ~103 mm; −0.09574 at hook u=0.13 to −0.11035 at `gal_appliance` u=0.80 → ±7.3 mm residual | INHERITED-rev52 |
| **F11** | The sixth hook lies beyond `BAYS[2]`'s own aft edge | **OPEN** | `BAYS[2]` aft edge **−0.855750**; sixth hook **−0.9070**; overshoot **51.25 mm** | **MEASURED-rev56** |
| **F12** | The hook span centre and the rail centre disagree, and one of them is wrong | **OPEN** | span centre **−0.7050** vs rail centre **−0.5980** = **107.0 mm** | **MEASURED-rev56** |
| **F13** | The six hook stations are typed literals with irregular spacing | **OPEN** | −0.907, −0.829, −0.750, −0.677, −0.572, −0.503 → gaps **78 / 79 / 73 / 105 / 69 mm** | **MEASURED-rev56** |
| **F14** | `gal_end_f` sees past its own end. Needs its OWN sight line — **do not inherit `REAR_W/2`** (rule 34: that figure belongs to the rear window, which is not what looks at it) | **OPEN** | 260.0 mm show side, 20.0 mm off side | INHERITED-rev52 |

## D. THE MODEL LIST

| ID | finding | status | figure | grade |
|---|---|---|---|---|
| **F15** | **A7 is ILLUMINATION, not dressing.** `roof_cutters()`'s aft edge is `LID_X1`, so a run of roofed body sits between the last light inlet and the tail skin, unbuilt | **OPEN** | **803 mm**. Source line is `LID_X0, LID_X1 = 0.9640, -1.0700` — **not greppable as `LID_X1 = -1.0700`** | INHERITED-rev52 |
| **F16** | A13 / A16 — the isolated star is built BELOW the burst where both red frames put it above; every flank rosette is drawn at the diameter of its **gold core** | **OPEN** | — | INHERITED-rev49 |
| **F17** | A11 / A14 — a chrome lever lying in a dish **pressed into** the skin, against a 12 mm **proud** prism | **OPEN** | — | INHERITED-rev49 |
| **F18** | **THE DIE-CUT STICKER — THE PROJECT'S ORIGINAL DELIVERABLE.** Its carrier was deleted at rev 44 and the loss was undetected for five revisions | **OPEN, and it is the oldest thing here** | — | INHERITED-rev44 |
| **F19** | The red shell carries **no edge chipping at all**, while SPEC §3 and the owner's rev-53 narrowing both require it. **Neither normal socket works**: `Normal` is dead on smooth geometry, `True Normal` counts facets | **OPEN — needs a real crease/edge-angle attribute, a revision's work** | as shipped **0.002668** on the flank, **0.000000** at the rear arch lip | MEASURED-rev55 |
| **F20** | SPEC §8's colour locks are all graded **M** = measured from `ref_source.jpeg`, a 246×197 thumbnail the record itself retired. Re-derivable on `ref_playa_34.png` at **4× the area** with no new photograph | **OPEN — report the values, do not change the constants** (W6: colour is the owner's call) | — | INHERITED-rev52 |
| **F21** | The red's hue gap cannot be split between paint and illuminant: the only near-neutral surface in the crop is there **by construction** | **OPEN** | photograph G/R **0.114** vs render **0.462** | CEILED-rev55 |
| **F22** | The vehicle's absolute roof height is **OPEN and UNMEASURED**. `H_ROOF` 1.960 was retired as a target and the model's 1.9833 is a regression baseline, not an accuracy claim | **OPEN** | — | RULED-rev22 |

## E. THE PROCESS ROWS

| ID | finding | status | figure | grade |
|---|---|---|---|---|
| **F23** | The **tail board** has zero rows in either verifier, on a part the owner has confirmed is on the vehicle | **OPEN** | — | INHERITED-rev52 |
| **F24** | Rev 48's refuted *"B stays open"* is still live in `build.py` and — **split across two lines so a flat grep misses it** — in `t1_shell.py` | **OPEN** | — | INHERITED-rev48 |
| **F25** | SPEC §0.2's two rev-4 corrections were later refuted and the refutation never landed in SPEC | **OPEN** | — | INHERITED-rev52 |
| **F26** | `flank_compare.py`'s header attributes a recovered camera position to `ref_side.jpg` that `studio.py` attributes to the **PLAYA** frame — the same three numbers, two files, two different photographs (rule 34) | **OPEN** | (−4.829, +2.222, 1.900) | **MEASURED-rev56** |
| **F27** | Five materials are still a **CONSTANT roughness**, which SPEC §3 calls the physical definition of the plastic look. Four of the five are legitimately transmissive or sealed; the list is carried so the fifth cannot hide | **OPEN, low** | 5 — amber, glass, lens, reflector, ruby | MEASURED-rev56 (`STATE.md`) |
| **F28** | The off-side flank shut line is graded **E** and is explicitly **not a correctness claim** | **OPEN, stated** | 804.9 mm over 2 pairs | MEASURED-rev56 (`STATE.md`) |

## Added at rev 57

| ID | finding | status | the number | grade |
|---|---|---|---|---|
| **F37** | **`t1_detail.py` states the nose badge's ring outer D TWICE, with two different values, about one boundary in one frame** — and neither is retracted, so nothing says which is live | **OPEN — reported, retracted in the source, not resolved** | the band comment *"outer D 91.729 px"* / *"62.705 px"* against `vw_logo_fit`'s *"vertical D 91.885 px, horizontal 63.143"* (also SPEC §10.107 via `REFERENCE_FRAMES_rev45.md`) — **0.17 %** and **0.70 %** apart. Rev 57's own fit is a third reading: **92.728 / 63.299** at radial resid **0.2345 px** | **MEASURED-rev57** |
| **F38** | **The BUILT nose ring band is wider than the frame's, and this is the FIRST built-against-frame comparison on either badge.** `verify.py` says of the other one, in its own words, *"hubcap badge is SELF-CONSISTENCY ONLY"* | **OPEN — reported, NOT changed**: it is inside the record's own declared uncertainty, and moving it moves the glyph's fit radius with it (`_BAND_FRAC = 0.028 / 0.140`) | band / ring outer D: **BUILT 0.10086** off `vw_ring`'s mesh; frame **0.09209 ± 0.00292** (threshold) and **0.09280 ± 0.00319** (gradient), 25 rays; the record's **0.0874**; adopted **0.093 ± 0.012**. Built is **+9.5 %** on this probe's reading, **+15.4 %** on the record's, and INSIDE the adopted band at the top of it | **MEASURED-rev57** |
| **F39** | **`Senor`'s deficit is in the ARTWORK ALPHA and its placement on `SCR` — not in the render, the shader or the lockup height.** Read off a table `flank_compare.py` has printed every run | **OPEN — and it is now a placement/artwork job, not a render one.** A12 remains an OWNER RULING: `senor_trace.py` calls redrawing it *"inventing ink the photograph does not show"* | `Senor` is the ONLY one of nine regions with an area outlier: **901 render px against 1261 reference px = −28.5 %**, where the other eight sit within **±5 %**. And the `tex-only` control — the texture's own alpha on the `SCR` rectangle, no render and no mask rule in it — reads **0.689** against the render column's **0.656**. `flank_compare.py`'s own sentence: *"Where it is as low as the render column, the glyph's problem is the PANEL, not the render."* | **MEASURED-rev57** |
| **F40** | The rev-55 *"the nose roundel reads as an X"* lead **dissolves at full size for the second time** | **CLOSED-rev57 — a control that finds nothing is still a result.** Recorded so a third revision does not spend itself on it | half-size hero: an X. Full-size `out/r57_hero.png`, cropped and enlarged without resampling the source: a legible **V over W** (`probe_scratch/rev57_hero_roundel.png`) | **MEASURED-rev57** |

| **F41** | **The ALBEDO arm is blind to the larger half of the mottle BY CONSTRUCTION.** The mottle drives base colour through one HueSaturation (`W_FADE_SAT` 0.88, `W_FADE_VAL` 1.04) capped at `MOTTLE_AMP` 0.55 — ~2 % of value on a near-white cream — **and** roughness (`ffac × MOTTLE_RGH_K` 0.18, up to **0.099**), which an albedo pass cannot see at all. Rev 56 woke the arm that cannot see it | **OPEN** — this is *why* F03 ablates flat; the fix is F05, not a constant | colour half measured at **1.603 DN peak-to-peak**; `t1_mats.py` asked for exactly this check beside `FADEV_CREAM` — *"its authority over the rendered cream has to be demonstrated, not assumed"* — and it had never been run | **MEASURED-rev57** |
| **F42** | **`shader_solve._render` throws away half the bits, behind a guard that cannot fire.** It asks for `color_depth = '16'` and Blender delivers (IHDR: bit depth 16, colour type 6), then reads through `Image.open(...).convert("RGBA")`, **which returns uint8** — so `a /= 65535.0 if a.max() > 255.0 else 255.0` can never take the 16-bit branch. Every measurement through `_render` is 8-bit | **OPEN — measured, retracted in the source, NOT fixed.** `_render` is a shared path; changing it moves every consumer, and doing that without re-running each is the failure the record warns about. A stdlib decoder is written and controlled | patch sd **3.9999** at 16 bits vs **4.0200** shipped (**+0.50 %**, small, and stated as small). What it destroys is the mottle: sd **0.2594** against an 8-bit quantisation floor of **1/√12 = 0.289** — **0.9 of one step**. A verifier row TESTS the downconversion rather than asserting it | **MEASURED-rev57** |
| **F43** | **What the other 93.5 % of the render's cream albedo breakup IS.** Not the mottle (F03). A coarse cloud, sd ~4.000 DN, growing monotonically with filter scale | **OPEN — this is what item B actually is, and it is where rev 58 starts** | the patch is confirmed all cream (R/G = 1.00, no red), so it is not the two-tone boundary — checked, and that hypothesis is REFUTED | **MEASURED-rev57** |

---

## CLOSED — kept with what closed them, never deleted

| ID | finding | closed by |
|---|---|---|
| **F29** | `flank_kv()` carried `k_t` by the map's FULL horizontal ratio — a 1/Z² quantity moving a 1/Z one | **CLOSED-rev56.** k_v is LINEAR in (u+B). Proved on a synthetic camera: linear exact, quadratic 4.299 % out. Ablation `T1_FC_KVQUAD=1` |
| **F30** | *"The two vertical instruments disagree by 2.3 % and one of them is out"* | **CLOSED-rev56 — WITHDRAWN.** A false premise: the horizontal scale legitimately exceeds the vertical aft of the principal column. Wheel disc W/H **1.00417 ± 0.00048** |
| **F31** | *"The render's flank lockup is short in height"* | **CLOSED-rev56 — REFUTED as a model claim.** The reference was being placed 4.3 % too tall. Rev 55's stretch vertex 1.0398 vs the instrument's 1.0428, two routes sharing no datum |
| **F32** | `lid_rail` built two objects of 0.000000000 m², exempted rather than fixed because its width was measured nowhere | **CLOSED-rev56.** Owner ruled *"narrow lip, ~as wide as it is tall"* → width **IS** `RAIL_PROUD` (0.0213 m). Sweep now 0 of 223, 0 exempt. Ablation `T1_RAILFLAT=1` |
| **F33** | `cream_rms.run()` was the dead `ref_side.jpg` path for eight revisions while the re-based measurement sat unused in the same file | **CLOSED-rev56.** `run()` reports the live spectrum; dead path kept behind `T1_CR_LEGACY=1` |
| **F34** | `mottle_measure.py`'s target was five typed literals transcribed from `spectrum()` | **CLOSED-rev56.** Derived at run time, raises rather than falling back, drift printed (0.0004 pp) |
| **F35** | `mottle_measure.py` printed five `ratio 0.00` rows off a fully saturated patch — a measurement of nothing that read as "the model has no mottle" | **CLOSED-rev56.** Refuses now, and the refusal is hoisted above the first printed number |
| **F36** | The open-findings register itself, abandoned at rev 45 with 21 rows | **CLOSED-rev56** by this file |
