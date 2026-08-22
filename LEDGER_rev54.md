# LEDGER — rev 54

Every figure below was watched printing. The runs they come from are
`probe_rev54_edge.py` (arm A, the mesh), `probe_rev54_aov.py` (arm B, the EDGE
emission AOV), `probe_rev54_look.py` (arm C, the beauty render) and
`probe_rev54_wfrac.py` / `probe_rev54_badge.py` (the badge). Re-run them and the
same numbers come back.

---

## §0. THE HEADLINE — THE QUESTION HAD A FALSE PREMISE

Brief §3 item 2 asked **"why does the counter fascia's own bottom fold produce no
edge signal?"**

**It produces one.** The fold fires at essentially the full theoretical value for a
90° fold, and it makes a chip band **one millimetre tall**. One millimetre at the
shipped side render's own **271.2 px/m** is **0.27 px**, so every instrument ever
pointed at it has integrated it away. Three revisions hunted a cause for a
silence that was never in the shader — it was in the sampling.

**And the radius lever is live at this fold too**, which is the part rev 53 could
not see: coverage rises **4.45×** from the shipped 2.75 mm to 12 mm. Rev 53 read
"unchanged at 0.000 %" and that was **a true reading and a false inference**.

---

## §1. ARM A — ASK THE MESH FIRST. TWO HYPOTHESES DIED FOR FREE

Before rendering anything, `probe_rev54_edge.py` asked the mesh.

**The code and its own comment disagree about which normal the gate uses.** The
comment says `edge = 1 - dot(bevel_normal, true_normal)`; the code links
`geo.outputs["Normal"]` — the **shading** normal. `True Normal` appears nowhere in
the tree. On a smooth-shaded mesh the shading normal is already interpolated
across a fold, which is exactly what the Bevel node approximates, so `EDGE` would
collapse to 0.

**That hypothesis is REFUTED by the mesh, and it cost no render:**

| object | polys | smooth | flat | material | Wear |
|---|---|---|---|---|---|
| `counter` | 26 | 0 | **26 — FLAT** | `countercream` | **0.7000** |
| `counter_top` | 26 | 0 | 26 — FLAT | `countertan` | 0.7000 |
| `T1_body` | 61737 | 61737 | 0 — SMOOTH | `T1_paint` | 0.5500 |

`counter` is **flat-shaded**, so its shading normal *is* its true normal.
`t1_detail.FLAT` exists for exactly this reason — its own comment says smoothing
"turns a louvre lip or **a counter corner** into a soft blob".

**The wear weight is not zero either** — `countercream` carries **0.7000**, so
`wear = hard * IN['wear']` is not starved. And the fold is real: **2 edges at
90.72–91.02° (mean 90.87°), 0.3417 m long**, on a mesh with **0 boundary edges**.

*The comment/code mismatch on `Normal` vs `True Normal` is left standing and
FLAGGED, not changed: on flat geometry the two are identical, so it is inert
here, but it is live on every smooth-shaded object the gate touches. Stated as
open — see §8.*

---

## §2. ARM B — THE EDGE VALUE AS AN EMISSION AOV, WHICH IS WHAT THE BRIEF ASKED FOR

`probe_rev54_aov.py` taps the shared `WEATHER` node group by **walking the graph**
from the Bevel node (not by node location), adds a `PROBE` output, and drives
every material's Emission from it. Materials without the group emit **blue**, so
"not measured here" can never be read as "measured zero". The walk prints what it
found before it renders:

```
Bevel -> Vector Math DOT_PRODUCT (other input: NewGeometry . Normal)
      -> Math SUBTRACT (1 - dot)  -> Map Range.003 (from 0.02929..0.14645)
      -> Math.009 MULTIPLY (craw) -> Math.010 GREATER_THAN 0.350 (hard)
```

### §2.1 THE INSTRUMENT WAS WRONG FIRST, AND THE PAINTED MASK CAUGHT IT

**The fascia SLOPES.** Measured: across a 300 mm window the fold **drops 5.25 mm**.
A single global `min(z)` over the fascia's vertices put the fold at **row 373**
while the mask's own lowest row was **239** — **134 px = 25 mm wrong**. Caught
because the probe prints both and they disagreed.

The fold is tracked **per column** off the mask now. Rev 53's arm D had already
learned this (*"NOT a fixed row band. The fascia SLOPES"*) and I re-learned it.
Rule 7: ask the geometry, never the pose.

### §2.2 THE CHAIN, MEASURED — tight crop, 0.1875 mm/px (5333 px/m)

| tap | what it is | max | frac>0 | frac>0.5 |
|---|---|---|---|---|
| `edge` | `1 - dot(bevel_n, shading_n)` | **0.28992** | 5.101 % | 0.000 % |
| `pw` | smoothstep(EDGE, 0.0293..0.1464) | 0.95673 | 4.179 % | 1.355 % |
| `cprod` | `cm * clm`, the two object-space noises | 1.00000 | 72.144 % | 19.811 % |
| `craw` | `pw * cprod` | 0.86824 | 2.260 % | 0.115 % |
| `hard` | `craw > 0.35` | 0.90625 | 0.919 % | **0.314 %** |
| `wear` | `hard * IN[wear]` | 0.63438 | 0.919 % | 0.159 % |

`EDGE` reaches **0.28992** against `W_EDGE_90 = 0.29289` — **99.0 % of the
theoretical maximum for a 90° fold.** The detector is not weak here; it is at
full scale.

### §2.3 THE BAND IS ONE MILLIMETRE TALL — the whole answer, as a profile

Bands measured **up from the per-column fold**:

| band mm | 0–1 | 1–2 | 2–3 | 3–4 | 4–6 | 6–9 | 9–12 | 12–18 |
|---|---|---|---|---|---|---|---|---|
| `hard>0.5` | **11.833 %** | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| mean `EDGE` | 0.12410 | 0.00857 | 0.00003 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

And `EDGE` in 0.25 mm bands: peak mean **0.20451 at 0.12 mm**, down to 10 % of
peak by **1.38 mm**, numerically zero past ~2.4 mm.

**1 mm at 271.2 px/m is 0.27 px. At `ref_side.jpg`'s 211.5 px/m it is 0.21 px.**

The chip population in that band: **7 blobs, 39.94 mm², median equivalent
diameter 1.916 mm, area-weighted 4.208 mm**, covering **0.3140 %** of the counter
mask.

### §2.4 THE RADIUS SWEEP — the measurement rev 53 could not make

Same window, same instrument, four Bevel radii at 5333 px/m:

| radius | EDGE reach (10 % of peak) | chip blobs | coverage |
|---|---|---|---|
| 1.00 mm | 0.625 mm | 39 | 0.0995 % |
| **2.75 mm (shipped)** | 1.375 mm | 9 | **0.3084 %** |
| 6.00 mm | 2.625 mm | 8 | 0.6769 % |
| 12.00 mm | 5.125 mm | 22 | **1.3717 %** |

Coverage per millimetre of radius: **0.0995 / 0.112 / 0.113 / 0.114** — linear.

**NOISE CONTROL, and it is built in:** the 2.75 mm case was rendered twice at
different sample counts (64 spp → **0.3140 %**, 32 spp → **0.3084 %**), so the
sampling floor on this statistic is **~1.8 %**. The 4.45× rise from 2.75 to 12 mm
is two orders of magnitude above it.

**So rev 53's `T1_EDGERAD=12` experiment moved the shader by 4.45× and its
estimator reported 0.000 % both times.** The experiment was sound; the conclusion
drawn from it — that the fold is inert — does not follow. What must clear a pixel
is not the RADIUS but the BAND, and the band is **0.43–0.63 of the radius**.

### §2.5 THE RESOLUTION LADDER

Box-averaging the linear `wear` AOV — **a model of a coarser render, not a
render, and labelled as one in the probe's own output**:

| mm/px | 0.188 | 0.563 | 0.938 | 2.063 | 3.750 | 4.688 |
|---|---|---|---|---|---|---|
| peak `wear` | 0.634 | 0.516 | 0.416 | 0.219 | **0.107** | **0.092** |

3.750 mm/px is the shipped side render (271.2 px/m → 3.687); 4.688 is
`ref_side.jpg` (211.5 px/m → 4.728).

---

## §3. ARM C — THE FALSIFIABLE TEST, AND IT PASSED

An AOV is not a render. If the band is real, a **real shader render** at fine
scale must show chips where the AOV says, and not where it does not.

`probe_rev54_look.py` renders the same window through the project's own studio
rig and `setup_render()` at four real scales. Then the four largest AOV-predicted
chip sites were cropped out of the beauty render **and four control tiles were
cropped on the same fold in columns where the AOV predicts nothing**.

**LOOKED AT** (`probe_scratch/rev54_look_chiptiles.png`, predicted first, controls
after): every one of the four predicted tiles shows a **dark ragged bite in the
cream at the fold**. Every one of the four controls is **clean**. The prediction
was made before the tiles were cut.

**And the other half** (`probe_scratch/rev54_look_ladder.png`, the same window at
0.1875 / 1.0 / 3.687 / 4.728 mm/px): by the shipped scale the chips are gone.

---

## §4. WHAT THIS DOES AND DOES NOT DO TO HIS RULING

**It does not reopen it.** He ruled *"Follow the photograph — clean cream"* and the
shipped build still reads **0.000 %** through the frame's optics. Nothing here
changes what ships or what he was shown.

**What it changes is the reason.** The cream is not clean because the gate is off
at that fold; it is clean because the gate's output is 0.27 px tall. **The build
does carry a 1 mm chip band on the fascia's bottom fold**, and any future close
view puts it on screen — at 1 mm/px the peak `wear` is still **0.416**.
`studio.views()["counter"]` is a 90 mm lens at ~6 m, i.e. roughly 1.5 mm/px on
this part. **Stated as a consequence, not acted on.**

---

## §5. THE SOURCE BLOCK ASSERTED BOTH DEFAULTS AT ONCE FOR A WHOLE REVISION

`t1_mats.py`'s chip-gate block contained, 38 lines apart:

* `# DEFAULT IS STILL POINTINESS.` — rev 52's, left behind
* `# rev 53: THE DEFAULT IS NOW THE RAY-TRACED EDGE SIGNAL.`

**And `verify_clone.sh`'s row "chip gate: the EDGE signal is the DEFAULT" passed
throughout**, because it is anchored on the CODE — and the code was right. Only
the prose lied. A guard on the code does not guard the comment beside it. The
stale sentence is retracted in place and a row now counts it and wants **0**.

---

## §6. THE BADGE — THE UNBLOCKED HALF OF THE TOP JOB

Item 1 is blocked on a photograph. This is the part that is not.

### §6.1 A PAINTED WINDOW CAUGHT MY OWN PROBE, AGAIN

The first version took every object named `capring*` and called it "the ring".
**There are four hubcaps.** The "ring" came out as a **2.486 m circle spanning the
wheelbase** with two 20 mm glyphs at the axle stations, and `w/R` read **0.01136**.
Caught in one second by looking at `probe_scratch/rev54_badge_hubcap.png` — the
red circle is the whole vehicle. Instances are clustered on the ring centroids
now, and **all four are reported so they control each other** (spread **0.00**).

### §6.2 THE CONSTANT DOES NOT DENOMINATE WHAT A PHOTOGRAPH MEASURES

`CAP_EMBLEM_WFRAC = 0.2087` is documented `# w/R as authored (0.0072 / 0.0345)`,
and 0.0345 was a real OUTER RADIUS — so the authored intent is w / R_outer. But
`vw_bars` is called with **R = 1.0** and `_fit_glyph` then rescales off the
outline's **own extreme corner**.

**CALIBRATED BEFORE IT WAS BELIEVED** (`probe_rev54_wfrac.py`): the stroke
estimator recovers a known width to **+0.33 % … +0.52 %** over w = 0.12…0.28.
And the unit glyph's `rmax` is **0.81400 at every one of those four widths**.

| | authored wfrac | built stroke / OUTER RADIUS |
|---|---|---|
| hubcap | 0.20870 | **0.25639** |
| nose (`vw_logo_fit`, the real call site) | 0.19860 | **0.24398** |

Cross-checked independently on the **built mesh** via `probe_rev54_badge.py`:
**0.25869** for the hubcap — agreeing with 0.25639 to 0.9 %, which is the
estimator's own bias. Two routes, one answer (rule 6).

**THE TRAP THIS SETS FOR REV 55:** a photograph measures the second column.
Comparing a frame against **0.2087** itself **understates by 18.6 %**. The note is
now in `t1_detail.py` beside the constant and a row holds it there.

**AND THE TWO BADGE DESIGNS DIFFER BY 5.09 %** (0.25639 vs 0.24398). Neither has
ever been compared to any frame.

*A figure I nearly published and did not: "the two glyphs differ by 25.32 % as
built". That was **my own comparison error** — the nose glyph is deliberately
fitted to 0.84 × its ring radius (`vw_logo_fit`, `_BAND_FRAC`) while the hubcap is
fitted flush, so I was dividing by two different denominators. On a common
denominator it is 5.09 %. Recorded because it was wrong for a plausible reason.*

*And `vw_logo`'s signature defaults (`R=0.1385, w=0.0275`) are **not what is
built** — the call site passes `R=1.0, w=wfrac`. I read the signature first. They
happen to agree to 4.4e-05, so nothing turned on it, but the signature is not the
call site.*

### §6.3 THE GUARD GAP, MEASURED — AND THE BRIEF OVERSTATES IT

The rev-54 brief says *"still not one row anywhere names a wheel, hub, cap, rim
or vent"*. **Measured, that is too strong:**

* `verify.py` **does** guard `TRACK_F`, `TRACK_R`, `TYRE_D` (§2, real
  `fails.append`) and the rear **arch-to-tyre gap** against SPEC §2's 41 ± 8 mm
  (§10). `STATE.md` prints all of them.
* `verify_clone.sh` row `tex/emblem.png` checksums the emblem texture.

**What genuinely had nothing** — zero occurrences in either verifier, measured:
`capvw`, `capring`, `wheel_spoke`, `wheel_rim`, `wheel_hub`, `rim1`, `rim-1`,
`wheelhouse`, `roof_vent`, `vw_disc`, `vw_ring`, `CAP_EMBLEM_D`,
`CAP_EMBLEM_WFRAC`. And `t1_detail.py:316`'s `hubcap seated:` line is a **`log`,
not a guard** — it prints four numbers and nothing fails if they drift.

`verify.py` section 13 now measures, off the mesh: the assembly's object counts;
the ring radius against `CAP_EMBLEM_D/2` **derived on both sides**; that the four
rings agree; that each cap centre sits on a hub (`z == TIRE_R`, `x` at an axle);
and that the glyph is fitted **flush** to the ring, which is what
`_fit_glyph(glyph, CAP_EMBLEM_D/2)` promises and nothing checked. Live output:

```
hubcap badge: 4 rings R 0.043429 (= CAP_EMBLEM_D/2), glyph extreme 0.043429,
spread 0.00e+00 m
hubcap badge is SELF-CONSISTENCY ONLY -- CAP_EMBLEM_WFRAC has never been
compared to a frame; see PHOTOS_WANTED item 7
```

---

## §7. GUARDS ADDED — eight rows, BOTH HALVES WATCHED ON A CLEAN TREE

`verify_clone.sh` **165 → 173**. Rule 3 says watch a guard FAIL on the defect;
rev 53's §7.2.1 added that this is necessary and **not sufficient**. Both halves
were watched for all eight:

| row | watched FAILING on | watched PASSING through |
|---|---|---|
| the fold's PREMISE is retracted | the sentence reworded away | heavy re-wording around it |
| no stale SECOND default is asserted | the rev-53 sentence put back | a comment that **quotes** it |
| rev54 EDGE-AOV probe exists | the file removed | — |
| AOV probe tracks the fold PER COLUMN | regressed to a global min | comments added above it |
| AOV probe keeps its radius sweep | the sweep header dropped | comments added |
| look probe renders a scale ladder | 271.2 changed to 300.0 | — |
| badge: the wfrac denominator trap is recorded | the figure line removed | the note reflowed |
| badge: wfrac probe keeps its calibration | the calibration removed | — |

The second row's PASS half is **live, not hypothetical**: the shipped tree
contains `# rev 54: "DEFAULT IS STILL POINTINESS" STOOD HERE AND WAS FALSE.` and
the row reads 0, because it is anchored on the line **starting** with the claim.

---

## §8. WHAT IS STILL OPEN

* **`Normal` vs `True Normal` in the chip gate.** The comment says true normal,
  the code uses the shading normal. Inert on flat geometry; **live on every
  smooth-shaded object** the gate touches, which is the whole shell. Not changed
  this revision — changing it would move the red, and the red is not what was
  asked about. **Flagged, unmeasured.**
* **The badge stroke weight against a frame.** Still the top job's open half.
  A route the brief does not list is described in the rev-55 brief §4.
* **`cream_rms.py` was NOT run at rev 54 either.** Still a dormant
  render-vs-photograph gate with zero rows in either acceptance script.
* **`flank_compare.py` was NOT re-run at rev 54** — nothing this revision touched
  the artwork it reads, and it is quoted from rev 53 as inherited, not re-measured.
* Brief §3 items 3, 4, 5, 6 and §3.1 — **untouched**.
