# AUDIT rev 11 — comprehensive specialist audit against the source photographs

Three specialists so far, each read-only on the repo, each measuring the model and
the rev-11 renders against `ref_side.jpg`, `ref_rear34.jpg` and `ref_workshop.jpg`.
Full working: `measure/audit_proportion.md`, `measure/audit_weathering.md`,
`measure/audit_script.md`.

**Four dimensions run**: proportion, weathering, script, fascia. **Five remain**:
counter/galley internal contrast, wheels and contact shadow, tail, roof,
optics/glass. Briefs in `workflows/tacombi-rev11-audit.js`.

Nothing below is a self-assigned score. Every line is a measurement with a method.

---

## THE THREE THAT MATTER MOST

### 1. The script's acceptance test computes no metric. Severity 5.

`flank_compare.py` — the test SPEC calls the acceptance test for the flank script,
in Donald's own words ("render the flank, crop the script to the same framing as the
reference, and show me the two side by side at matched scale") — **contains zero
lines that compute a number.** Its entire output is:

```
script panel projects to render px x 514-817  y 668-779  (303x111)
reference ink crop (271, 99)   generated crop (303, 111)
wrote out/flank_compare.png
```

It prints two crop sizes and writes a stacked image. And all three of its framing
decisions are wrong, two of which cancel so the pair look *more* alike than they are:

* it samples the reference at y 490–588 while the ink runs 474–588 — dropping 14 %
  off the top, the whole top of `Señor`. **This is the exact defect SPEC §10.20 found
  in `compare_script.py` and fixed there. It was never fixed here.**
* it projects the render panel **un-dropped**, so it cuts 15.8 px off the bottom-front
  — the `T`'s foot.
* it resamples both to the same *width* and lets each height follow its own aspect —
  the one operation guaranteed to hide an aspect-ratio error.

**The acceptance test as written cannot detect the largest defect in the feature it
tests.** Fourth occurrence in this project of "a claim in prose is not a guard", and
the first where the guard existed but was hollow.

### 2. The script panel's aspect ratio is stale by 15.8 %. Severity 5. **FIXED.**

`build.py` `SCR = dict(..., z0=0.4453, z1=0.9177)` — 1.2784 × 0.4724 = **2.705:1**,
commented `= tex AR`. That was true of the rev-9 texture (2702 × 1000). rev 10
rebuilt the script and `tex/senor.png` is now 4096 × 1738 = **2.3567:1**. The constant
was never updated, so the lockup has been squashed 15.8 % vertically since rev 10.

Two independent derivations agree: texture aspect gives 1.2784 / 2.3567 = 0.5424 m of
height; measuring the ink off the photograph at 211.2 px/m gives 0.5440 ± 0.008 m.
Width was already right — photo 1.2784 ± 0.012 against 1.278 built, −0.4 mm — and the
x extents are confirmed at +3 / −1 mm.

Confirmed with no arithmetic on the constants at all: the best *similarity*
registration of render onto photo reaches IoU 0.627, while an *anisotropic* one
reaches **0.825 at k = 1.1575**.

**Applied: `z1` 0.9177 → 0.9896, grown upward.** Not recentred — `z0` is measured and
carries a warning, and the missing height belongs at the top, because §10.20 found the
reference ink runs 16 rows higher than the frame allowed and those rows are the top of
`Señor`. Guards re-run: 0 fail / 1 warn at both levels.

**Why nothing caught it:** `compare_script.py` scores the *texture* against the
reference mask and never looks at the panel the texture lands on. Its 0.942 was true
and irrelevant. Consequence for `Señor` in the render: 6 926 mm² of ink against the
photograph's 29 514 — **23 %** — where the mask-space score said 0.9.

### 3. Sun fade is keyed on the surface normal's Z, so the entire flank gets exactly zero. Severity 5.

`t1_mats.py:505`: `fz = MapRange(Normal.Z, 0..1)`. On a vertical flank Nz = 0, so the
fade factor is 0 everywhere it matters. The photograph has a real gradient: over the
cream corner panel X −1.60…−1.84, chroma C\* falls **14.55 → 6.53 (−55 %)** while L\*
rises 89.6 → 96.2, with **hue constant at 67–73°** — the signature of fade, not of a
colour shift. The render's same panel moves C\* 1.98 → 1.59.

*Honest caveat from the auditor:* in one open-shade frame the **cause** is not
separable from a warm ground-bounce gradient — same decay length, same hue. The
magnitude is measured; the attribution is not.

---

## PROPORTION AND STANCE — eleven findings, and two calibration corrections that move most of them

Two method results that everything else hangs on:

* **The model's origin is not mid-wheelbase.** Axles are at +1.300 / −1.100, so
  mid-wheelbase is x = **+0.100**. `REF_MEASUREMENTS.md` maps the photo as
  `X = (495.8 − u)/211.5` and calls X = 0 mid-wheelbase, but 495.8 px *is* the hub
  midpoint — so **every REF "model-frame" number is 100 mm aft of where it says.**
* **The flank's px/m drifts the opposite way from RULES §4.** Rear rim flange 46.46 px
  against front 44.2 px over identical angular sectors (ratio 0.951, so the nose is
  ~5 % farther), putting the fore-aft vanishing point at u ≈ −13 000…−20 000. **The
  tail is nearer, at ~222 px/m — not the 194.8 the rules assert.**

| # | finding | photograph | model | sev |
|---|---|---|---|---|
| P1 | **Nose-down rake 2.3× too steep** | 14.4 ± 3.1 mm/m (0.83°), from rocker slope −0.023963 ± 0.00024 over 312 px, rms 0.43, corroborated by the cream rocker trim at −0.024010 | `RAKE_DZDX = 0.0330`, mesh 34.6 mm/m — **+20 mm/m, 6σ**, 86 mm of extra tilt over the body | 4 |
| P2 | **Rear arch 143–195 mm too narrow, and the wrong curve** | 0.881–0.933 m, lip apex flat within 3 px over 367 mm, centred within 9 mm of the axle | circular cutter, 0.738 m, flat crown only 203 mm | 5 |
| P3 | **The tail is ~200 mm long, not 99** | rear overhang 0.729–0.811 m by three methods | 1.008 m. SPEC §10.7's 99 mm subtracted two numbers in **different origins** | 4 |
| P4 | **No transverse roof dome** | crown 43 px above the drip-rail gutter → **0.19 ± 0.03 m** (SPEC §10.9 independently got 35–37 px) | half-width still 0.790 at z 1.90; a **22 mm** turn-over | 4 |
| P5 | Body height 40–70 mm short | rocker→crown 1.58–1.60 m | 1.531–1.538 m | 3 |
| P6 | The crown is a straight raked line in the model, a curve in the photograph | falls ≈54 mm over x +1.20→+1.64 | falls 7.5 mm | 3 |
| P7 | **Tyres do not deflect** | loaded radius 0.302 m against unloaded 0.329 — 27 ± 9 mm of squash | rigid at 0.3325. Ride height itself is right: rocker-above-**hub** agrees to 1 mm | 3 |
| P10 | Aperture band 37 mm too tall | 0.364 m | 0.401 m | 2 |

**P9 — SPEC §10.9's rake-versus-arch-gap contradiction is RESOLVED, and it resolves
against the built rake.** The identity `rear − front = rake × wheelbase` is sound. At
the built 33 mm/m the front gap comes out at **−27 mm, which is physically
impossible**. At the measured 14.4 mm/m it is **+17 mm**, inside REF §2's independent
0–25 mm band. Rear gap re-measured at 52 mm (50–59) against the built 41; REF's 71 mm
used the loaded radius. That is strong corroboration for P1: the lower rake is the
only value at which the geometry is self-consistent.

**P4 overturns rev 10's "geometry-4 is NOT MEASURABLE".** rev 10 could not find a
datum; this pass used the drip-rail gutter at the same column, which is visible.

**P8 — RULES §4's 194.8 px/m is not a measurement.** It is 204 px of rear-corner panel
divided by the 1.047 m that panel spans *if the tail is at −2.007* — i.e. P3 restated
as a scale drift. Side effect worth its own pass: perspective predicts 2.6 % of
SPEC §10.5's 3.7 % bay-width growth, so **the three serving bays may be equal after
all.**

**NOT MEASURABLE, all four settled by one photograph:** tumblehome (a section
quantity, invisible in side elevation), the front arch (the open door is forward of
u 210 and the man occupies 210–295), absolute overall height, and the body's own belt
line (the counter occludes u 300–990). **One left-side broadside with the cab door
shut and nobody in front of the front wheel would settle all of them.**

---

## WEATHERING AND MATERIALS — the dominant CG tell, now quantified

| # | finding | photograph | model | sev |
|---|---|---|---|---|
| W1 | **The counter slab is wearing a camouflage pattern** — bare-steel chip path firing on flat panel | clean cream with a brass nosing; no chipping resolvable | residual sd rises 4.40 % at 5 px to **21.31 % at 81 px**; saturation sd 0.310 on a mean of 0.277, bimodal; largest grey blob ≈130 mm | 5 |
| W2 | **Sun fade gets zero on every vertical surface** | C\* 14.55 → 6.53 (−55 %), hue constant | fade factor identically 0 on the flank | 5 |
| W3 | **The dust film lightens where the photograph darkens** | rocker tide narrow and dark: q −13.2 % at Z 0.375, −16.4 % at 0.365; C\* 65.2 → 38.0 over the last 25 mm | Δq **+1.8 to +9.7 %** — wrong sign by 15–25 points. `W_DUST_COL` luminance 0.395 is **2.8× the red albedo's 0.139** | 4 |
| W4 | **Albedo breakup is 2–4× too weak, and cannot change chroma** | relative RMS 0.52 / 0.67 / 1.08 / 1.44 / **1.90 %** at 10/25/50/100/200 mm; panel sd 3.03 L\*; chroma spans 8.1 C\* | 0.21 / 0.28 / 0.35 / 0.42 / 0.48 %; sd **0.48 L\***; chroma spans 0.5 C\*. It is a scalar multiply, so chroma variation is impossible by construction | 4 |
| W5 | Brass nosing too pale and too blue, no albedo tarnish | B/R 0.033–0.237 light-normalised | rendered B/R 0.553; authored 0.265; brass is in no `apply_weather` group | 3 |
| W6 | Rear arch lip gets **no edge wear at all, by construction** | a local saturation minimum at the lip — S 0.932 → 0.828 over 9 mm then rising to 0.867. A pure PSF blend is monotonic; this is not | monotonic. The repo's own pointiness bake reads the lip at 0.503–0.510 against `W_PT_LO = 0.520` — it never enters the wear window at either subdivision level | 3 |

**On the nine constant-roughness materials: only one is a genuine violation** —
`gal_menucard` (`t1_detail.py:1411`), which is neither transmissive, emissive nor
sealed and skips the roughness field every other galley material gets. The others are
legitimately carved out. **The bigger number is that `WEATHER` is spliced onto only
ten materials** — `brass`, `chrome`, `steel`, `lidmural` and `lidsign` get no dust,
wear, breakup or fade at all.

**Explicitly NOT material findings** (lighting, per §10.12/§10.21): the cream's mean
L\* 92.5 against 78.7, the red's 42–46 against 100–107, the chrome, the depth of the
under-counter band. **Not supported by the photograph:** road-spray staining behind
the arches — q is +1…+4 % there. **This vehicle is washed.**

---

## THE SCRIPT AND THE CALIDAD DECAL

Calibration: projection isotropy h/v 0.9989 ± 0.010 (subpixel conic fit to the rear
hubcap ring, 180 rays); scale 211.2 ± 1.0 px/m from the locked wheelbase and
independently from the bay frame lines. Reference mask rebuilt from §10.20's rule:
9 410 px. **Ceiling for any IoU below: 0.90**, or 0.87 with 1 px of registration slop.

* **`Tacombi`'s letterforms pass at the ceiling** — x ≥ 416 gives IoU **0.873**
  against a 0.899 ceiling. **Do not touch them.**
* **`Señor` is not reproduced in the render**: photo 402 × 203 mm and 29 514 mm² of
  ink at 13.4 mm strokes; render 392 × **114** mm and **6 926 mm²** at 8.4 mm strokes,
  top 85 mm low, region IoU 0.454. Much of this is finding 2 above; re-measure after
  the panel fix before doing anything to `script_gen.py`.
* **Ink 12.5 % light** in the render after the aspect correction.
* **Mottle grain ~4× too coarse** — photo 1/e 3.75 px (17.7 mm) along the writing
  against the render's 16.0 px (67.4 mm). Direction and amplitude are right.
  **Root cause: `script_ink.md` §3's "13–16 px long axis" contradicts its own radial
  4.11 px, and the generator was tuned to the wrong one of the two.**
* **SPEC §10.16 confirmed and strengthened** — after removing a cubic illumination
  model, the ground beside the ink is within ±1.9 DN in all eight octants at every
  radius 1–12. No keyline, no drop shadow, limit ≲1 DN. **But the render has a halo
  anyway**: −12.5 DN at d = 1, isotropic, not in the texture — ambient occlusion from
  the decal panel's 1.6 mm standoff.
* **Tarnish ratios pass** (0.717/0.374/0.259 against 0.695/0.377/0.285) but the
  **warm-with-depth gradient is gone**: photo Δa\* dark−light **+14.4**, render −0.5.
* **Calidad**: 35–50 mm too far aft, 11 % too tall, ~27 spikes against ~18 ± 3 and
  26 % too regular, gradient axis rotated 32°, and **the pink star is 139 mm aft and
  178 mm low, baked into the burst texture instead of standing clear on the cream**.

---



---

## FASCIA — dimension 4, and it overturns two of SPEC §10.24's three verdicts

### The three §10.24 items, re-derived by a third method

| item | verdict | evidence |
|---|---|---|
| **bumper standoff** | **BOTH SIDES INADMISSIBLE — stays OPEN** | In `ref_side.jpg` the **lamppost occupies columns 62–79** continuously over rows 455–620, and the bumper's cream never appears left of column 77. The bumper's front face is **entirely occluded**. So `fascia.md`'s "bumper face x <= 67" *and* §10.24's "silhouette puts the bumper face at 82–91" are both reading the post and its shadow. Column 82 is the bezel's gold arc, 80 is the indicator lens, 78 is the post. **My own third method in rev 10 was measuring a lamppost.** |
| **indicator lens depth** | **REFUTED — datum error** | "41.5 mm built" is lens-proud-of-**plinth**. Against the body skin the built pod already stands **53.6 mm** proud. Scale-free third method, same frame, same station: lens blob 16 ± 2 px against the bezel arc's 50 ± 3 px = 0.320 ± 0.045 bezel diameters = **66 ± 10 mm**. Residual 12 ± 10 mm, **1.2 sigma**. Do not deepen it. |
| **headlamp vertical position** | **CONFIRMED TWICE — apply** | Method A (workshop, pure ratio, no px/m, no belt, no ground line): roundel-to-lamp separation = 0.628 ± 0.066 roundel diameters = **0.176 ± 0.019 m** against the build's 0.0928 — **83 ± 19 mm, 4.4 sigma**. Method B needs no scale at all: in the photograph the indicator aperture lies entirely **below** the two-tone break, on the coloured panel; in the build it lies entirely **above** it, on the cream. Dropping the pair 83 mm puts it 44 mm below the break, as photographed. |

The roundel's own height (belt − 0.149) is supported by both chains and **must not move** — rev 10 applied the derived half of `livery-9` and rejected its primary.

### Two severity-5 defects in rev 11's own work

* **`tex/nose.png`'s Color output was never linked.** `t1_mats.py` cleared the
  selector handoff in the *alpha* branch, which is assembled **before** the colour
  branch reads it. The nose therefore got nose.png's SHAPE and the flank tile's
  COLOUR — (0,0,0) wherever the flank tile is transparent — so it rendered as black
  marks. **Fixed in this pass; guards re-run 0 fail / 1 warn at both levels.**
* **`nose.png`'s ink is in the wrong band.** Alpha bbox v 599–689 of 1024 puts it at
  z **0.933–1.070 m AG** — the headlamp/roundel band, mostly on the cream. The red
  wedges get nothing. Measured off an orthographic render at 253.521 px/m: lower-nose
  gold **2.33 %** against the 11.44 % target, dark 3.26 % against 2.42 %, and the
  composition is **two isolated dark commas**. The rev-11 nose decal did not land.
  Fix lives in `folk_gen.py`'s nose window, not in the shader.

### And SPEC §10.25's premise is wrong

The `ROUNDEL_D` coupling is arithmetically correct and does hold. But **there has
never been a 12.7 mm air gap in this code**: the V and W spines are only 0.015 R
apart against a 0.183 R mitred apex, so the two prisms **interpenetrate 23.1 × 37.2 mm
at D = 0.280** and 30.5 × 49.2 mm at D = 0.370. Minimum vertex gap on the mesh is
0.37 mm. The render shows a fused X at both diameters. The rev-10 fix made the glyph
smaller, which made the fusion less obvious without removing it. Severity 4.

Also: **the glyph is 29 % undersized** — height/ring ⌀ 0.796 ± 0.020 photographed
against 0.565 built, with the ring itself correct. And the **V-swage arm rises about
2× too fast**: lamp station to body edge is 0.111 ± 0.015 m photographed against
0.208 built, implying `V_POW` ≈ 0.30–0.48 against the locked 0.60. Severity 3.

**Confirmed, no action:** brass bezels (rendered R−B +67/+68 against a measured +68),
blade section 0.113 against 0.110 ± 0.010, headlamp lateral 0.561 ± 0.058 against
0.545, roundel ⌀ 0.268 against 0.280 built, vent wing and wipers present.
**NOT MEASURABLE:** front plate, bumper standoff, indicator frontal outline, headlamp
lens appearance.

The origin correction (mid-wheelbase is x = +0.100) shifts **no** fascia number —
all of them are differences, ratios, or direct photograph measurements.

---

## Dimensions still to run

**Five of ten remain**: counter and galley internal contrast, wheels and contact
shadow, tail, roof, optics/glass. Briefs in `workflows/tacombi-rev11-audit.js`.


## Ordered work list

Sequenced so nothing later invalidates something earlier. Geometry in ONE rebuild,
both guards after.

0. **`nose.png`'s ink band** — the decal is drawn at z 0.933–1.070 where the target
   is the lower nose's red wedges. Cheap, and it is the difference between the nose
   having scrollwork and having two commas.
1. **Cut the roof hole** (SPEC §10.27) — unchanged as the top item.
1b. **Drop the headlamps 83 mm** — the only §10.24 item that survives an independent
   re-derivation, and it is confirmed twice, once by a test that needs no scale at
   all. Do NOT move the roundel with them.
1c. **Separate the V and W prisms.** They interpenetrate at every diameter; the
   rev-10 coupling fix made the fusion less visible without removing it.
2. **The stance batch, together, because they interact through P9's identity**: rake
   P1, rear arch P2, tail length P3, roof dome P4, body height P5, crown curve P6.
   Re-derive each once more before applying — P1 and P3 both contradict values the
   spec calls locked, and this project's rule is that such a finding needs a third
   method. P9 is that third method for P1 and it agrees.
3. **Give `flank_compare.py` an actual metric**, and fix its three framing errors,
   before touching the script again. Until then it cannot tell you whether a change
   helped.
4. **Weathering**: W2 (fade normal) and W1 (counter chip path) first — both are
   single-node fixes with severity 5. Then W3's dust sign and colour, then W4's
   breakup amplitude and its inability to move chroma.
5. Re-measure `Señor` in the render **after** the panel aspect fix, then decide
   whether `script_gen.py` needs anything.
6. Calidad: move the star out of the burst texture; correct the spike count and
   regularity.
7. Run the six remaining audit dimensions.

## What would unblock the most

**One photograph.** A left-side broadside, cab door shut, nobody in front of the front
wheel, taken square-on from as far back as the space allows. It would settle the
tumblehome, the front arch, the absolute height, the body's own belt line, and give a
clean second derivation for the rake and the tail — six open items, four of them
currently marked NOT MEASURABLE.
