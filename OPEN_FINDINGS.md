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
| **F01** | `flank_compare` worst region `Senor` below its bar | **OPEN** | **0.644** against a 0.75 bar (was 0.478 before rev 56's carry-law fix) | MEASURED-rev56 |
| **F02** | The flank plane's ABSOLUTE vertical scale. Three readings at one station disagree | **OPEN** | map k_h **220.45**, `k_t` **215.5**, flange-OD route **211.8** px/m. Three quantities, two equations | MEASURED-rev56, CEILED |
| **F03** | The render's cream mottle is the wrong SHAPE — too little fine structure, too much coarse | **OPEN** | ratio **0.62** at 3 mm, **1.34** at 23.7 mm | MEASURED-rev56 |
| **F04** | The mottle's CHARACTER has the wrong sign. Level-free and scale-free, so no amplitude change fixes it | **OPEN** | `corr(dL*,dC*)` render **+0.199/+0.173/+0.200**, photograph **+0.042/−0.106/−0.294** | MEASURED-rev56 |
| **F05** | `mottle_measure.py`'s BEAUTY arm cannot run — the cream blows out because `shader_solve._render()` builds no studio rig | **OPEN** (refuses rather than lying) | patch **100.00 %** clipped | MEASURED-rev56 |
| **F06** | The mm axis on the `ref_rear34.jpg` cream plane is not established, and it sets F03's whole x-axis | **OPEN** | `PXM_REF = 337.0` px/m is a **bracket** (330–344) | INHERITED-rev19 |
| **F07** | The C\* base-level comparison is inadmissible as it stands — ALBEDO against OBSERVED PIXEL, SPEC §10.21's trap | **OPEN** | render 3.89 vs 21.44, ratio 0.181 — **reported, not acted on** | CEILED-rev56 |

## B. THE TOP JOB

| ID | finding | status | figure | grade |
|---|---|---|---|---|
| **F08** | **The two VW badges' STROKE WEIGHT has never been compared to any photograph.** The live route (nose badge on `ref_workshop.jpg`) has been un-attempted at rev 54, 55 **and** 56 | **OPEN — top job** | compare against **0.25639**, not against `CAP_EMBLEM_WFRAC = 0.2087`; the two designs differ by **5.09 %** | INHERITED-rev54 |
| **F09** | That route's ceiling is unresolved: `ref_workshop.jpg` is the GREEN vehicle, and the same geometry-transfers argument already underwrites the shipped ring band. **Either both are legitimate or the ring band is grounded on the wrong vehicle** | **OPEN** | badge 91.7 px vertical D, PSF sigma 0.689 px, axis ratio **0.684** (must be de-projected) | INHERITED-rev54 |

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
