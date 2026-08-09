# Skeptic pass over the 13 critical findings in `AUDIT_RECOVERED.md`

Run 2026-08-09. Four independent reviewers, each briefed to **refute**, each
required to re-derive every measurement by their own method rather than check
the audit's arithmetic. Reviewers were told explicitly that `REF_MEASUREMENTS.md`
outranks the audit, that the audit predates the high-resolution photographs, and
that "correcting the vehicle toward the factory catalogue" is this project's
dominant historical failure mode.

**Headline: 0 of 13 killed outright. 11 of 13 survive only with corrected
numbers — the audit was right that something was broken and wrong about how
broken, in most cases by a factor of two or more. Two findings are duplicates of
each other. Acting on the audit's numbers as written would have introduced new
errors in at least six places.**

Three defects the audit never found are larger than most of what it did find.
They are in §C.

---

## A. Verdict table

| # | Finding | Verdict | The correction |
|---|---|---|---|
| 1 | `geometry-1` belt line too high | **SURVIVES, numbers wrong** | Error is **+111 mm**, not +150. Target **1.272 model / 1.207 AG**, not the proposed 1.240 (which is 32 mm *below* the measurement). All three of its evidence lines are inadmissible — two are a **Samba** blueprint, one is the retired 246×197 thumbnail. Right conclusion, by accident. |
| 2 | `geometry-2` V-swage apex too high | **SURVIVES, error ~2× larger** | Error is **+476 mm**, not ~250. The audit's proposed 0.620 is **itself wrong by +224 mm**. Correct apex **0.405 model / 0.340 AG**. The arm exponent is also wrong: measured `V_POW ≈ 0.60` (concave), shipped 1.16 (convex). |
| 3 | `apertures-1` cab-door gaps see-through | **SURVIVES, and understates it** | Ray claim overstated (4 of 14 samples *are* blocked; defect is essentially confined to the ortho side view — 41/76 rays at `side`, 1/76 at `hero34f`). But **at `T1_SUB=2` both door-gap booleans collapse the shell 205 562 → 12 v and are rolled back**, so the production model has *no cab-door shut line at all*. See §C1. |
| 4 | `apertures-2` rollback guard too weak | **SURVIVES, numbers wrong** | Worst legitimate ratio is **0.9902** (SUB=1) / **0.9862** (SUB=2), not 0.9911/0.9875. No-op blindness is **real and worse** — a cutter entirely outside the shell passes silently. The audit's proposed face-count/coordinate digest **does not work**: EXACT re-tessellates on a true no-op (Δf = +9, ΔVolume = −3.38e−06 m³). Vertex-count equality is the only clean test. Strengthened guard designed and validated against all 44 measured (cutter, level) rows: 2 true positives, **0 false positives**. |
| 5 | `inventory-3` wipers buried in the nose skin | **SURVIVES verbatim** | Reproduces to within 0.1 mm on every quantity. Blade is 17.3 mm behind the windscreen plane, 8.5 mm below the aperture edge; every ray toward every camera crosses exactly 2 body surfaces. Orientation claims confirmed by PCA. The one finding that needed no correction. |
| 6 | `livery-2` VW roundel renders as an X | **SURVIVES, numbers wrong** | Collinearity reproduces exactly (5.93 %, 1.53° apart; joints sit *inside* the bar). "Renders black at the overlaps" is **over-sold**: 11 px of 4225, at 2 of 6 junctions, 0.26 % of the disc. Two errors nobody logged: roundel is **⌀0.336 vs SPEC 0.370** and its centre is **33 mm low**. |
| 7 | `inventory-1` louvres, 0 of 20 | **SURVIVES on the gap, REFUTED on every coordinate** | Zero louvres confirmed two ways. Audit's block is **85–130 mm too far aft and 130–150 mm too high**. Correct: x **−1.285 → −1.670**, top slot **1.085 undropped**, bottom **0.895**, pitch **21.1 mm**. Count **10** — see §B3. |
| 8 | `inventory-2` counter stops short | **SURVIVES, every number wrong** | Proposed `X1 = −2.420` is **100 mm aft of the photograph** — it applied a measured overhang to the *model's* tail instead of the *measured* tail. Correct `X1 = −2.323`. Shortfall is **0.983 m**, not 0.768. The counter is also 108 mm high, 22 mm thin, 79 mm proud, and has **no tail wrap at all**. |
| 9 | `livery-1` Calidad on frosted glass | **SURVIVES — duplicate of #10** | Merge. |
| 10 | `materials-4` Calidad still frosted glass | **SURVIVES, numbers wrong** | Same file, function, binding and fix as #9. Δ is **51.9** code values, not 62; **55.0 %** of surrounding linear reflectance, not 41 %; the "warm cast" claim is **refuted at its stated magnitude** (R−B +4.4 vs cream +2.6, a difference of 1.8, not 7.1). The two findings also **contradict each other** on mechanism — it is transmissive, and merely *reads* as an opaque plate because unlit interior sits behind it. |
| 11 | `materials-1` constant roughness everywhere | **SURVIVES, better metric** | 25 materials confirmed as 2-node constants, name for name. Material count 28 vs 22 both correct — 28 datablocks built, 22 reach a pixel, **6 orphans** (3 of which `verify.py` bans the moment anything uses them). Rendered deficit re-derived properly: real cream varies **4.22 / 7.26 / 10.54 %** RMS at 25/100/400 mm; the build gives **0.22 / 0.45 / 1.06 %** — a **10–19× deficit**. |
| 12 | `materials-2` no dust on the lower body | **SURVIVES on code, justification REFUTED** | Code claim confirmed. But "real road dust gives 15–40 % desaturation over the bottom 300 mm" is **not true of this vehicle**: in CIELAB the chroma ratio `C*/(L*+16)` is flat to ±7 % from 0.40 m to 0.92 m — the 35 % luminance fall toward the rocker is **illumination, not pigment**. Tide line is at **h ≈ 0.40 m**, so the audit's proposed `smoothstep(0.75 → 0.25)` is **~3× too tall** and would dust a band the reference shows clean. |
| 13 | `materials-3` orange peel is a no-op on bbox coords | **SURVIVES, and the audit's FIX is wrong** | Unlinked Vector socket confirmed. Feature sizes corrected (Z is 8.10 mm not 10.2 — the audit used the vehicle height, not the material's bbox). **Audit missed that `T1_paint` is on three objects**: the same node renders a **140:1** stretched peel on the drip rails. And its proposed fix — 0.5 mm features in a Bump node — **A/B's at the Monte-Carlo noise floor**: sub-pixel microstructure aliases in a Bump and belongs in Roughness. |

---

## B. Adjudications where the sources conflicted

**B1. Belt line: `sill − 100 mm` from *which* sill?**
From the measurement, not from the model's sill. `Z_BELT = 1.272`, **not 1.302**.
"Belt = sill − 100" is not a physical law; it is a restatement of two
measurements (sill 1.307, break 1.207 AG). Feeding the model's own sill into it
launders the sill's **+27 mm** error into the belt, and the relationship then
*looks* satisfied while both numbers are wrong. Set each from its own
measurement and let the 100 mm fall out as a **check**. The model's window band
is itself high: `Z_SILL` +27 mm, `Z_HEAD` +25 mm. Band *height* is fine.

**B2. The cab door in `ref_side.jpg` is OPEN, swung ~55–60° on its front hinge.**
Found by this pass; not in any prior document. Proof: door skin at the belt
spans 103 px = 0.488 m against a real T1 cab door of ~0.90 m — pure `cos θ`
foreshortening; and both door lines run at image slope **+0.065** while every
body line runs at **−0.041**. A closed panel cannot do that.
**`REF_MEASUREMENTS.md` §3(a) sampled the paint break at x = 130/150/170/190 —
entirely on the open door — then normalised 620 px back to the rear axle using
the body slope. Both steps are invalid on a rotated panel.** Its answer is
nonetheless right, because the reviewer re-derived it by a **ratio taken on the
door itself**, which is immune to the rotation (both features share one depth,
so magnification cancels): break sits **95 ± 10 mm** below the sill,
independently corroborated by a hue test showing 5 red pixels in 7072 in the
cream strip above the gold nosing. Two independent routes agree.

**B3. Louvre count: photo says 7–9, factory says 10. Take 10.**
Not deference to the catalogue — it is the only count that closes the
arithmetic. Measured block height **0.189 m** ÷ measured pitch **21.0 mm** = 9
gaps = **10 slots**. Seven slots at 21 mm spans 0.126 m, 60 mm short of the
measured block. At 4.5 px pitch the signal sits below the JPEG 8×8 DCT block, so
the failure mode is **merging** — under-counting is possible, over-counting is
not. REF's "7 clear, probably 7–9" is explicitly a lower bound. A lattice fit
recovers two sub-threshold members, taking the visible count to 10–11.
*Note:* REF §7's exact row list does not reproduce in the red channel — that
pass picked up the counter shadow edge as part of the stack. The block extent
does reproduce.

**B4. The counter "0.31 vs 0.10 m overhang" conflict is not a conflict.**
Three datums, one counter end (−2.323): past the **tail panel** (−2.007) it is
**0.316 m** — SPEC §2.3's 0.313 and the audit's 0.31 are *both correct*; past
the factory bumper **blade face** it is 0.203 m; past the **over-rider tips** it
is ≈0.10 m — SPEC §2.5's figure. §2.5 silently switched datum and called it "the
factory bumper line" without naming a face. The audit is **not** quoting a
retired number. All three are useless for modelling, because the bus has no rear
bumper. Only the absolute `X1` matters.

**B5. Sun fade is UNVERIFIABLE from the supplied photographs.**
Neither in-service photo is in direct sun — `ref_side.jpg` is open shade,
`ref_rear34.jpg` is under a palapa. SPEC §3's (206,208,200) / (196,106,36) come
from the 246×197 thumbnail, which cannot separate fade from exposure. The fade
term must be entered in SPEC as a **design value**, not a measurement. What
would settle it: one full-sun frame showing the same panel at two orientations.

---

## C. Defects found by this pass that the audit missed entirely

**C1. At `T1_SUB=2` — the production level — the cab-door shut lines do not exist.**
```
[  23.1s]   !! BOOLEAN COLLAPSE on gap_door1:  205562 -> 12v  -- ROLLED BACK
[  24.2s]   !! BOOLEAN COLLAPSE on gap_door-1: 205562 -> 12v  -- ROLLED BACK
[  30.7s]   VERIFY: 1 fail, 0 warn
```
Reproduced 4× by the reviewer and once by me — fully deterministic. So
`START_HERE.md`'s "guards green" is **true only at SUB=1**, and the audit's own
"FAILED_CUTS was empty at both levels" is false. The existing 0.6 guard catches
it; nothing reads the result.

**Cause — and the repo's `≥ 20 mm clear of roll-over` lore is REFUTED as stated.**
Causal test: rebuild at SUB=2 with the four wheel-arch cutters skipped and the
*identical* door-gap cutter at the *identical* z **succeeds** (+1214 v). The
failure is the gap's bottom run crossing the **wheel-arch aperture rim**, not
proximity to a roll-over. x-isolation puts the fatal band at [1.60, 1.75],
straddling the arch front rim at x = 1.6725. The rule was violated in *both*
directions with no failure: a bottom run 49 mm inside the sill roll works; a top
run 45 mm above the roof-roll tangent works.
**Replacement rule:** *a panel-gap outline must not cross the lip of another
aperture, and where it runs near a roll the outer-skin slope relative to the
cutter's extrusion axis must stay below `t_skin / gap_width`* (0.51 at 2.8/5.5 mm).
Measured correlate: the failure boundary sits at slope ≈ 0.5 ≈ 2.8/5.5.
**Fix:** the cab door's bottom shut line is currently at z 0.4248 undropped =
**0.3598 above ground** — wheel-centre height, running across the open arch for
745 mm of its 930 mm length. Move to **z ≥ 0.78 undropped**, which clears the
arch top (0.7710) and is the only geometrically defensible value. Tested:
0.4248 collapses, 0.4548 partially shreds, 0.56/0.78/0.80/0.83 all clean.

**C2. `audit.py` has been reporting a fabricated belt line for six revisions.**
Line 89 prints `belt line (paint break)` as a hardcoded `1.2320 − RIDE_DROP` =
**1.1670**. The actual `Z_BELT − RIDE_DROP` is **1.3210**. The literal 1.2320 is
connected to nothing in the build. It is worse than a wrong number: the
fabricated value sits *near the correct one*, so for six revisions the status
report certified precisely the dimension that was broken. This is the clearest
instance of the drift `STATE.md` exists to stop.
Other hardcoded constants masquerading as measurements in the same file:
`0.860` as body half-width when the script's own vertex dump prints 0.8749
(so "wheels sit +98.0 mm inboard" should read **+112.9**); `/ 1.72` as body
width when the measured value is 1.7498 (every glass percentage is 1.7 %
optimistic). Everything else in the file reads live values.

**C3. The "Señor Tacombi" script decal is ~1.3 m too far aft.**
`build.py:168` places it at X −0.300 … −1.900. Measured in `ref_side.jpg` the
script occupies x_img 330–600 = X **+0.784 … −0.494**. As placed it lands
squarely on the louvre block. Not in the audit's 89 findings at all.

**C4. Two more, smaller.** The model's tail panel is at −2.108 against a
measured **−2.007** and a factory-derived −2.009 — the body is **101 mm too long
at the tail**. And `audit.py`'s "nose reach"/"tail reach" rows are two stacked
bugs: `RIDE_DROP` is subtracted a second time from the *query window* (every row
interrogated 65 mm too low), and the `|y| < 0.12` filter slices the vehicle's
**centre plane**, where between z 0.65 and 1.05 there are exactly 4 vertices —
the two loft end-cap poles. So `max()` over the tail poles was printed as "nose
reach". The `or -9` fallback then hid the empty selection behind a plausible number.

---

## D. The corrected numbers, consolidated

Frame: the model is built un-dropped; `build.py` step 8b subtracts
`RIDE_DROP = 0.065` from every vertex last. `AG = above ground = model − 0.065`.

### Two-tone break and window band
| | model | AG | shipped | error |
|---|---|---|---|---|
| `Z_SILL` | **1.372** | 1.307 | 1.4020 | +27 mm |
| `Z_HEAD` | **1.775** | 1.710 | 1.7980 | +25 mm |
| `Z_BELT` | **1.272** | 1.207 | 1.3860 | **+111 mm** |
| `V_APEX` | **0.405** | 0.340 | 0.8720 | **+476 mm** |
| `V_RISE` | **0.867** | — | 0.5140 | (= `Z_BELT − V_APEX`) |
| `V_POW`  | **0.60** | — | 1.16 | profile is concave, not convex |

`V_APEX ≤ 0.396 model` is a **hard bound**, not an estimate: the cream wedge is
still 14 px wide where the bumper occludes it in `ref_workshop.jpg`, and the
bumper top measures 0.331 ± 0.020 AG. Independent of any px/m conversion.

### Serving apertures — SPEC §1.1 is measured; the code never got it
`t1_shell.BAYS = [(0.26,0.86), (−0.45,0.15), (−1.16,−0.56)]` — still rev-3's
"three evenly sized, evenly spaced", which SPEC §1.1 explicitly retires.

| edge | model | SPEC §1.1 | delta |
|---|---|---|---|
| bay 1 | +0.860 / +0.260 | **+0.820 / +0.313** | +40 / −53 mm |
| bay 2 | +0.150 / −0.450 | **+0.195 / −0.321** | −45 / −129 mm |
| bay 3 | −0.560 / −1.160 | **−0.435 / −0.960** | −125 / −200 mm |
| widths | 0.600 ×3 | **0.507 / 0.516 / 0.526** | +93 / +84 / +74 mm |

The block is 240 mm too long and its centre sits 80 mm aft.

### Louvres (new geometry)
x **−1.285 → −1.670** (±0.03/0.04) · **10 slots** · pitch **21.1 mm** ·
top slot centre **1.085 model / 1.020 AG**, bottom **0.895 / 0.830** ·
slot length 0.385 m · aperture ~7 mm (inferred, below resolution) ·
**build horizontal** in the body frame (rake measured at +3.9° but the peak is
broad, +2.2…+4.5°, and confounded by JPEG block alignment).

### Counter
| | AG | model | shipped (model) | error |
|---|---|---|---|---|
| X0 front | +0.918 | +0.918 | +0.920 | ok |
| X1 rear | **−2.323** | −2.323 | −1.340 | **983 mm short** |
| Z top | 1.189 | **1.254** | 1.362 | +108 mm |
| Z bottom | 1.082 | **1.147** | 1.277 | +130 mm |
| thickness | 0.107 | 0.107 | 0.085 | 22 mm thin |
| Y outboard | 1.166 | 1.166 | 1.245 | 79 mm proud |

Plus a tail wrap that does not exist at all: continue the outer edge aft to
(−2.173, +1.166), quarter arc R = 0.150 to (−2.323, +1.016), then across the
tail at X = −2.323. Front outer corner chamfered 45° × ~0.05.

### VW roundel
Ring **⌀0.370** (shipped 0.336) · centre **1.130 AG / 1.195 model** (shipped
1.097 AG) · glyph built as **two closed mitred prisms**, one V and one W, not
six independent bars — this removes the self-intersection outright rather than
hiding it. V arm −40.75°, W inner −53.04°: **12.29° apart**, with a clear
12.7 mm air gap between V apex and W peak. Full outlines in the reviewer's table,
transcribed into `SPEC.md` §3.1.

### Weathering — "weathered" converted from an adjective into targets
| target | measured | source |
|---|---|---|
| cream local luminance variation, 25 / 100 / 400 mm | **4.22 / 7.26 / 10.54 %** RMS | `ref_side.jpg`, imaging noise removed in quadrature |
| current build, same physical patch | 0.22 / 0.45 / 1.06 % | 10–19× deficit |
| dust tide line | knee **h = 0.40 ± 0.04 m**, full ≤ 0.30, zero by 0.48 | CIELAB `C*/(L*+16)` |
| flank above 0.40 m | **clean**, ±7 % | same |
| upward-facing dirt | **ΔL\* −8.8, ΔC\* +5.0, Δhue −6.6°** toward ochre | `ref_rear34.jpg`, counter top vs vertical cream |
| Pointiness: flat flank | 0.503, zero spread | emission bake, SUB=1 |
| Pointiness: arch lip / bumper / drip rail / counter lip | 0.552 / 0.571 / 0.591 / 0.617 | → edge-wear window **0.520 → 0.600** |

**Pointiness is mesh-density dependent — these are SUB=1 and must be re-baked
before any SUB=2 hero.**

---

## E. What this pass changes about how to proceed

1. **Do not implement the audit's numbers.** Implement the numbers in §D. Six of
   the audit's proposed fixes would have introduced fresh errors — the belt at
   1.240 (32 mm low), the apex at 0.620 (224 mm high), the counter at −2.420
   (100 mm aft), the louvre block (85–150 mm out), the dust ramp (3× too tall),
   and the orange-peel bump (aliases, buys nothing).
2. **The SUB=2 door-gap collapse (C1) outranks everything else on this list.**
   Every render the project has ever produced at production subdivision was of a
   bus with no cab-door shut line.
3. **`verify.py` needs positive assertions, not just failure reports.** Row 9
   reports `FAILED_CUTS`; a rolled-back cut leaves a *valid* mesh with a silently
   missing feature. Same gap on `calidad_L`: `verify.py:143` asserts the object
   exists and `:24` that a material of that name exists — both pass with the
   defect present.
4. **`STATE.md` must be machine-written from live values.** C2 is the proof.
