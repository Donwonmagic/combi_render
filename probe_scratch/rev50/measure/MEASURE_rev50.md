# rev 50 MEASUREMENT PASS — the hubcap's proudness, the artwork census, two corroborations

Scratch: `probe_scratch/rev50/measure/`. No tracked file touched, no render run, no commit.
Every crop referenced below is on disk at the path given, and every one was **looked at**,
not only computed on.

---

# TASK 1 — HOW PROUD IS THE HUBCAP?

## 1.0 THE ANSWER, FIRST

**The hubcap's emblem/apex stands ~ +45 mm PROUD of the rim-flange lip plane
(range +40 to +52 mm).  The build ships +20.5 mm (emblem plate) / +14.5 mm (dome apex).
Candidate (a) as written — the full 49.7 mm outboard move — lands at +70 mm (emblem)
/ +60 mm (apex) and OVERSHOOTS by about 20 mm.**

So neither posted option is right as stated:

| quantity (relative to the flange-lip plane, + = outboard) | build now | option (a) full 49.7 mm | **photographs** |
|---|---|---|---|
| emblem plate | +20.5 mm | +70.2 mm | **+45 ± 5 mm** |
| dome apex | +14.5 mm | +60.2 mm | **+39 ± 5 mm** (apex = emblem − 6 mm, build's own plate offset) |
| visible cap-edge circle | −12.1 mm | −6.3 mm | **−10 to −35 mm** (poorly constrained; see 1.4) |
| visible cap D / flange D | 0.5447 rendered (0.6233 intended) | — | **0.633 – 0.667** |

**Recommended move: cap outboard by +24 mm (17 → 30 mm), not 49.7 mm.**
That alone is not sufficient: at +24 mm the cap's own max-radius rim (y = 0.0040 + 0.024
= 0.0280) would sit ~24 mm *behind* the disc surface at the same radius (disc y ≈ 0.0517
at r = 0.137), so the disc would occlude it again from some radius outward.  The disc
must be dished about **18 mm deeper at r ≈ 0.137 m** at the same time, so that the cream
annulus runs as a single smooth ~18° cone from the cap's edge (y ≈ 0.034) out to the
flange lip (y = 0.060).  That is a smooth cone over an 83 mm radial run — **not** a step,
so the "≈55 mm step in a cream annulus the photographs show smooth" objection does not
apply to a dish of this depth.  The photographs positively require such a cone: in every
frame the cream annulus is visibly *wider on the outboard side than the inboard side*,
which is the signature of a dished disc with a recessed cap edge (see 1.4 and the
synthetic in `S_dished.png`).

## 1.1 WHAT WAS MEASURED, AND WHY THIS OBSERVABLE

The decisive observable is **the VW emblem**, not the cap outline.

The emblem is a disc centred on the axle sitting at (or within millimetres of) the dome's
apex.  Under an oblique view its image is displaced from the flange circle's ellipse
centre, along the ellipse's minor axis, by

    d = h · sin(theta) · (a_px / R_flange)          h = axial proudness, a_px = flange semi-major

so `h = d / (a_px · sin theta) · 0.2198 m`, with `sin theta = sqrt(1 − (b/a)²)` read off the
same flange ellipse.  One feature, one number, no dome-shape assumption, and the sign is
anchored by physics: the apex is by construction the most outboard point of a convex cap,
so the emblem MUST be displaced outboard of the cap's own base ellipse.  That gives an
independent per-frame determination of which image direction is "outboard" — and it agreed
with the scene geometry in every frame (see 1.3).

## 1.2 CALIBRATION — the estimator recovers a known answer

**Control E1 — the render, whose truth is in the source.**
`out/r50a_hero34f.png`, front wheel.  `t1_detail.py`: `CAP_EMBLEM_PLANE = 0.0805`, plate
thickness 0.0060; rim barrel profile reaches its maximum radius (0.2198) at y = 0.0600.
So truth = **+20.5 mm** (plate mid-plane), **+23.5 mm** (plate front face), **+14.5 mm** (apex).

Window: flange ellipse fitted from 720 rays, adaptive per-ray 50 % level, robust-clipped —
`a = 55.772, b = 31.657, b/a = 0.5676, centre (745.74, 861.00), rms 0.15 px, n = 490`.
Emblem mask: saturation `S < thr`, `max(RGB) > 120`, box (740,847)–(758,877).

| thr | emblem centroid | d_out (px) | d_major (px) | h recovered |
|---|---|---|---|---|
| 0.28 | (750.24, 862.38) | +4.66 | +0.65 | **+22.3 mm** |
| 0.35 | (750.42, 862.67) | +4.89 | +0.91 | **+23.4 mm** |
| 0.42 | (750.84, 863.12) | +5.37 | +1.28 | **+25.7 mm** |

Truth +20.5 / +23.5 → **recovered to within +1.5 to +3 mm, threshold-stable, with the
cross-axis residual `d_major` ≤ 1.3 px.**  Mask images: `J_render_0.28.png`,
`J_render_0.35.png`, `J_render_0.42.png`.  **PASS.**  I subtract a +2.5 mm bias from the
photographic numbers below.

**Control E2 — the same render for the cap-edge estimator.**
Truth: the render's visible red boundary is the inter-vent crossing at r = 0.1200,
y = 0.0479 ⇒ Δ = −12.1 mm, and D-ratio = 0.1200/0.2198 = 0.546.
Recovered: `Δ = −11.5 mm`, `s = 0.547` (frac 0.35).  **PASS to ~1 mm and ~0.001.**

**Control S — synthetic perspective wheels** (`synth.py`, analytic cone + spherical cap,
4× supersampled, σ = 1 px blur).  `control_dished.py`, `control_H.py`.
Dished disc (cone from the cap edge at y = Δ out to the flange lip at y = 0), spherical
cap of base radius Rc, height H, full perspective at distance Z:

```
 theta  Z(m)   D_true(mm)   b/a_rec  s_rec   D_rec(mm)   err(mm)
  49.7  4.24     -60.0      0.6469  0.6526   -55.38      +4.62
  49.7  4.24     -45.0      0.6473  0.6547   -40.53      +4.47
  49.7  4.24     -33.0      0.6473  0.6557   -28.63      +4.37
  49.7  4.24     -20.0      0.6473  0.6571   -15.74      +4.26
  49.7  4.24      +0.0      0.6473  0.6591    +4.16      +4.16
  49.7  4.24     +20.0      0.6473  0.6611   +24.26      +4.26
```
Slope 1.000; the whole error is a pure perspective offset, **bias ≈ +18.5/Z mm**
(+6.2 at Z = 3 m, +4.4 at 4.24 m, +2.6 at 7 m), essentially independent of theta (40–60°),
of the cap radius (0.130–0.160), and of dome height for H ≤ 70 mm.  At H = 90 mm the dome's
limb enters and the bias grows to +11 … +14 mm — flagged, and not the regime here.
**PASS.**

**A control that FAILED and is reported as such.**  My first dished synthetic built the
cone as a stack of 120 flat annuli.  Its risers were never rendered, so background leaked
through on the outboard side and the estimator returned −18 mm for a true −33 mm.  The
analytic-cone rewrite fixed it.  If I had stopped at the staircase version I would have
published a number that was 45 % low.  (`bhjc640z2.output` holds the failed table.)

## 1.3 THE OUTBOARD DIRECTION — determined three independent ways per frame

A sign error here inverts the answer, so it was pinned three ways.

1. **Scene geometry.** IMG_2073 and ref_playa_34: nose near-left, tail far-right (front
   flange 70.1 px vs rear ~44 px) ⇒ visible flank normal has +X ⇒ **outboard = image RIGHT**.
   ref_rear34: tail near-right, nose far-left ⇒ **outboard = image LEFT**.
2. **The tyre, in IMG_2073.**  The tyre solid is symmetric about the wheel's centre plane,
   so its projected outline is centred on that plane, while the flange-lip circle sits
   ≈ 60 mm outboard of it.  Predicted black band at the flange centre height (y = 810):
   39 px on the inboard side and ~10 px on the outboard side if outboard = right; the
   reverse if outboard = left.  **Measured: 44.5 px of black on the LEFT (x 651 → 695.5),
   ≲ 25 px on the right.**  Outboard = RIGHT.  Decisive (9.9 px cannot become 44.5).
3. **Physics.**  In every frame the emblem is displaced from the *cap's own base-ellipse
   centre* in exactly the direction I call outboard: IMG_2073 +18.9 px, ref_playa_34
   +7.0 px, ref_rear34 −16.9 px (image-left).  A convex dome's apex cannot be inboard of
   its base plane, so this fixes the sign frame-by-frame with no scene reasoning at all —
   and it agrees with (1) in all three, including the frame where the image direction flips.

## 1.4 THE MEASUREMENTS

### (A) Emblem / apex proudness — the headline

**ref_playa_34.png, front wheel (RED bus, CURRENT artwork — the target vehicle & state).**
Flange: `a = 32.775, b = 19.329, b/a = 0.5897 (theta 53.9°), centre (232.50, 325.40),
rms 0.21 px, n = 699 rays`.  Scale 149.1 px/m; **1 px = 8.30 mm** of proudness.
Emblem mask `S < thr`, `max(RGB) > 90`, box (233,318)–(242,336); mask image `J_playa_0.32.png`
(verified by eye: clean, no ring contamination).

| thr | centroid | d_out (px) | d_major (px) | h |
|---|---|---|---|---|
| 0.26 | (238.42, 326.15) | +5.96 | −0.38 | **+49.5 mm** |
| 0.32 | (238.46, 326.85) | +6.13 | +0.29 | **+50.9 mm** |
| 0.40 | (238.40, 327.02) | +6.10 | +0.48 | **+50.7 mm** |

After the render-calibrated −2.5 mm: **h = +47.7 mm**.

**ref_rear34.jpg, rear wheel (RED bus, CURRENT artwork).**
Flange: `a = 70.707, b = 24.152, b/a = 0.3416 (theta 70.0°), centre (753.0, 731.4),
rms 0.65 px`.  Scale 321.7 px/m; **1 px = 3.31 mm**.  Outboard = image LEFT.
Emblem mask box (737,718)–(747,749) — the box starts at x = 737 specifically to exclude the
flange's cream ring, which at this wheel's vertical centre never reaches past x ≈ 736
(verified on the `C/g/R` segmentation printed in the log and on `I_rear34_zone.png`).

| thr | centroid | d_out (px) | d_major (px) | h |
|---|---|---|---|---|
| 0.26 | (739.58, 732.42) | +13.45 | +0.49 | **+44.5 mm** |
| 0.32 | (739.67, 732.38) | +13.35 | +0.46 | **+44.2 mm** |
| 0.40 | (739.64, 732.58) | +13.40 | +0.66 | **+44.3 mm** |

A second, independent route on the same frame — the emblem's *inboard* edge alone, which is
a clean cream/red step at x = 743.5 at y = 731, with the emblem's radius taken from its
unforeshortened (vertical) semi-extent of 14 px: `0.03031 = y_e·0.9398 − 0.04352·0.3416`
⇒ **y_e = +48.1 mm**.  Two routes, +44 and +48.
After the −2.5 mm bias: **h = +42 to +45 mm**.

**Combined: h = +45 mm, +40 to +52 mm.**  d_major (the cross-axis residual, which must be
zero for a feature centred on the axle) is ≤ 0.7 px in both frames — a strong internal check.

**Known systematic, direction stated:** near the limb the dome's surface foreshortens
violently, so the emblem's outboard half is compressed in the image and its centroid is
pulled **inboard**.  h above is therefore, if anything, a *lower* bound.

**What I could NOT measure here.**
- *IMG_2073 (green bus, chrome cap).*  There is a warm circular emblem at ≈ (755.6, 817.5)
  which would give h ≈ +57 mm, but no colour or luminance mask isolates it: every threshold
  I tried returns `d_major = +17 … +19 px`, i.e. the blob's centre is 17 px off the wheel's
  own vertical — the mask is grabbing chrome reflections, not the badge.  **The estimator
  fails its own cross-axis test on this frame and the number is withheld.**
  Crops looked at: `H_2073_emblem.png`, `H_2073_emblem2.png`.
- *ref_side.jpg.*  `b/a = 0.9848` ⇒ sin theta = 0.174 ⇒ **1 px = 27.1 mm**, and at that
  eccentricity the fitted minor-axis *direction* is not determined (it comes out nearly
  perpendicular to the radial direction from the principal point, which the off-axis
  perspective would demand).  **ref_side constrains proudness not at all**, exactly as the
  brief anticipated.  It is used below only for the in-plane ratio.
- *ref_nolita_flank.jpg.*  The wheel is partly cut by the valance and only ~34 px in
  semi-major; the fit is unstable across thresholds (`s` = 0.686 / 0.787 / 0.836,
  `d_major` = −1.8 / −4.0 / −5.0 px).  **NOT MEASURABLE.**
- *IMG_2073 rear wheel.*  rms 3.0–4.1 px and a recovered `b/a` of 0.71–0.76 against a
  hand-measured 0.45 — the fit is not finding the ellipse (arch and shadow).
  **NOT MEASURABLE.**  Its cross-section by hand (chrome displaced toward the bus's front =
  inboard, cream wider outboard) corroborates the sign only.

### (B) Cap-edge depth Δ (plane of the visible red/cream boundary vs the flange-lip plane)

Method: fit the flange ellipse from the cream→tyre step (adaptive per-ray level, robust
clip), then fit the cap boundary with **axis ratio and orientation locked to the flange's**
(both circles are coaxial, so their ellipses are similar) leaving only centre and scale
free; Δ from the centre offset along the minor axis, minus the +18.5/Z mm perspective bias.

| frame | a_px | b/a | frac | s (=cap D/flange D) | d_minor (px) | Δ_rec | bias | **Δ** | inner-fit rms |
|---|---|---|---|---|---|---|---|---|---|
| IMG_2073 front | 70.14 | 0.6470 | 0.35 | 0.6559 | −7.174 | −29.4 mm | +4.4 | **−34 mm** | 0.95 px |
| IMG_2073 front | 70.14 | 0.6470 | 0.50 | 0.6672 | −7.166 | −29.5 mm | +4.4 | **−34 mm** | 0.88 px |
| IMG_2073 front | — | — | 0.65 | 0.7528 | −10.96 | — | — | **REJECTED** | 2.21 px |
| ref_playa_34 front | 32.78 | 0.5897 | 0.35 | 0.6343 | −1.142 | −9.5 mm | +3.7 | **−13 mm** | 0.36 px |
| ref_playa_34 front | — | — | 0.50/0.65 | 0.74/0.76 | — | — | — | **REJECTED** | 1.7 / 1.2 px |
| ref_side rear | 46.85 | 0.9848 | 0.35 | 0.6329 | +0.062 | +1.7 mm | — | **+2 ± 27 mm/px** | 0.17 px |
| ref_rear34 rear | 70.71 | 0.3416 | — | 0.658 (vertical extent) | inboard edge only | — | — | **−11 mm** (assumes Rc = 0.145) | — |
| RENDER (control) | 55.77 | 0.5676 | 0.35 | 0.5471 | −2.319 | −11.5 mm | ~+2 | **−12 mm** (truth −12.1) | 2.48 px* |

\* the render's boundary is a five-petal outline, not a circle, which is exactly why its rms is 2.5 px.

**Δ is NOT well determined: it lies somewhere in [−35, −10] mm.**  The frames that disagree
most (IMG_2073 at −34 vs ref_playa/ref_rear34 at −11 to −13) are different vehicles with
visibly different caps (chrome moon vs painted red dome).  The IMG_2073 number is the only
one from a two-sided fit at a resolution where the signal (7.2 px) is far above the residual
(0.9 px); the ref_playa signal is 1.1 px and the frac-0.5 run diverged when only the fit's
*bootstrap* was changed, so I grade it LOW CONFIDENCE.
Implied dome height (apex − edge) = 55 to 80 mm against the built 70.5 mm — **consistent**,
which is why the recommended fix moves the cap as a rigid body and re-dishes the disc under
it rather than reshaping the dome.

### (C) Visible red-dome D / rim-flange D, on the UNFORESHORTENED (major) axis

| frame | ratio | window / note |
|---|---|---|
| ref_side.jpg rear | **0.633** | frac 0.35, inner rms 0.17 px; frac 0.50/0.65 rejected (rms 2.1/2.0) |
| ref_playa_34 front | **0.634** | frac 0.35, inner rms 0.36 px |
| ref_rear34 rear | **0.658** | red region's vertical extent y 687→780 against a = 70.71 |
| IMG_2073 front | **0.656 / 0.667** | frac 0.35 / 0.50, inner rms 0.95 / 0.88 px |
| render (control) | **0.547** | truth 0.546 — CONTROL PASSES |

**Photographs: 0.633 – 0.667.  Red bus alone: 0.633 – 0.658.**  The record's 0.6446 sits in
the middle of the red-bus band and is confirmed.  The build's intent 0.6233 is at or just
below the bottom of the band; the render's delivered 0.5447 is 0.09–0.12 low.
**Ceiling:** all of these are the *visible* boundary; if any occlusion by the disc remains,
the built CAP_R and the measured ratio are not the same quantity.

### (D) Is the cream annulus unbroken? — YES, in every frame that resolves it

| frame / wheel | crop looked at | magnification | annulus radial width | verdict |
|---|---|---|---|---|
| ref_side.jpg rear | `L_side_wheel.png` box (690,545)–(810,660) | 7× | 30 → 46 px | **UNBROKEN**, smooth, one shallow concentric groove, no notches |
| ref_playa_34 front | `D_playa_frontwheel.png` box (195,275)–(280,370) | 8× | 21 → 33 px | **UNBROKEN** |
| ref_rear34 rear | `E_rear34_wheel.png` box (700,640)–(830,790) | 5× | 46 → 71 px | **UNBROKEN** |
| IMG_2073 front | `B_2073_frontwheel.png` box (640,700)–(850,920) | 4× | 46 → 70 px | **UNBROKEN** |
| **RENDER** front | `C_render_frontwheel.png` box (690,770)–(830,900) | 6× | 30 → 56 px | **BROKEN** — five dark crescents at the cap edge |

The build cuts five vents at r 0.0945–0.1415 m, i.e. r/R_flange 0.430–0.644.  They show in
the render only because the visible cap stops at 0.545.  **But even at the intended ratio
they are marginal:** 0.644 versus a measured cap edge of 0.633–0.658 means the vents end
*exactly at* the cap's rim, and against ref_side's 0.633 they would still show.
**Recommendation: move the vents in to r ≤ 0.60 R_flange (0.132 m) or delete them.**

### (E) Tyre valve stem — VISIBLE, and it is a real feature to model

| frame | image position | r / R_flange | r (m) | clock position (wheel frame) | crop |
|---|---|---|---|---|---|
| IMG_2073 front | (730.5, 861.5) | **0.754** | 0.166 | ≈ 6 o'clock (3.5° off) | `L_2073_valve.png` box (715,845)–(750,875), 16× |
| ref_side rear | (780.4, 581) | **0.83** | 0.182 | ≈ 1:30 | `L_side_wheel.png`, 7× |
| ref_playa_34 front | (218, 313.5) | 0.90 | 0.197 | ≈ 10:30 | candidate only, **not confirmed** |

A dark stub with a visibly thicker cap, ~19 mm of protrusion in IMG_2073, sitting in the
**cream annulus outside the hubcap**, at r ≈ 0.75–0.83 R_flange (0.165–0.182 m).  The build
has no valve stem.  Clock position is random (the wheel turns) — model it at a fixed radius
of ≈ 0.79 R_flange and a free angle.

## 1.5 WHAT WOULD MAKE TASK 1 WRONG (ceilings)

- **The emblem is assumed centred on the axle and at the apex.**  If it is a decal placed
  off-centre, h is meaningless.  Three frames of two vehicles and two opposite image
  directions all agreeing, plus `d_major` ≤ 0.7 px, make that implausible but not impossible.
- **The flange-lip plane is taken as the white/tyre boundary**, i.e. the rim's maximum
  radius, y = 0.0600 in the build.  If the paint runs over onto the flange's outer face the
  reference plane shifts by a few mm and every h shifts with it.
- **The perspective bias correction uses Z**, which I estimated only to ± a factor
  (IMG_2073: f ≈ 1352 px and Z ≈ 4.2 m from the front/rear obliquity difference, versus
  f ≈ 982 px, Z ≈ 3.1 m from the wheel-size ratio and a 2.40 m wheelbase — the two disagree
  and I did not resolve it).  The whole span Z ∈ [3, 7] moves h by only ±2 mm, so this is
  not load-bearing, but it IS unresolved.
- **The green bus's cap may not be the red bus's cap.**  Geometry transfers between
  vehicles by the project's rule, but a chrome moon cap and a painted deep dome are
  plausibly different parts.  The headline h rests on the two RED, current-artwork frames.
- **ref_playa_34's front wheel is steered** by ~2–4° (its theta is 53.9° while the rear
  wheel, further from the principal point and so necessarily *more* oblique, measures 51.7°).
  This does not bias Δ or h — the axle is still the ellipse's minor axis — but it does mean
  the frame's obliquity is not the body's.

---

# TASK 2 — HOW MANY ARTWORK STATES ARE THERE REALLY?

## 2.0 File identity first (md5, whole file)

| file | size | md5[:12] | identity |
|---|---|---|---|
| ref_playa_34.png | 500×400 | 230a2a90df74 | **=** IMG_3842.png (byte-identical) |
| ref_nolita_flank.jpg | 450×450 | a00c45b431b9 | **=** IMG_2054.jpeg |
| ref_nolita_front34.jpg | 700×467 | ed2c33b0ec5e | **=** IMG_2060.jpeg |
| ref_nolita_front34b.jpg | 550×412 | b8e7f7a44b4b | **=** IMG_2053.jpeg |
| ref_nolita_doorshut.jpg | 480×320 | f1b6f98c6a12 | **=** IMG_3840.jpeg |
| ref_source.jpeg | 246×197 | 03631c7ae35e | re-encoded downscale of ref_playa_34, not a distinct view |

Five byte-identical duplicates, exactly as the brief states.  Nine distinct views.

## 2.1 THE CLASSIFICATION TABLE

`P` present, `A` absent, `?` present in frame but not resolvable at this scale/angle.

| | **ref_side** | **ref_rear34** | **ref_playa_34** | **nolita_flank** | **nolita_front34** | **nolita_front34b** | **nolita_doorshut** | **ref_workshop** | **IMG_2073** |
|---|---|---|---|---|---|---|---|---|---|
| vehicle colour | RED | RED | RED | RED | RED | RED | RED | **GREEN** | **GREEN** |
| flank scrollwork (yellow/ochre) | **P** | **P** | **P** | A | A | A | A | **A** | **P** |
| "Señor Tacombi" script | **P** | **P** | **P** | A | A | A | A | **P** | **P** |
| "100 % Calidad" burst | **P** | **P** | **P** | A | A | A | A | **A** | **P** |
| isolated star(s) | **P** (1, above-left of burst) | **P** (1, above-left) | **P** (1, above-left) | A | A | A | A | **A** | **P** (several small, around the burst) |
| TACOMBI.COM lettering | A | A | A | **P** (flank, below window) | **P** (small, flank) | ? | **P** (counter fascia, green/red) | A | A |
| 267 ELIZABETH STREET / NUEVA YORK | A | A | A | **P** | ? | ? | **P** (+ "Gracias por su Preferencia") | A | A |
| drip-rail bulb string | **P** (lit, along the gutter) | ? | **P** (around apertures; gutter not resolved) | **P** | **P** (lit, orange) | **P** (lit, continuous strip) | ? (ceiling string is not on the vehicle) | **P** (orange bulbs on the lid rim) | **P** (on the lid rim) |
| raised roof lid | **P** | **P** | **P** | ? | **P** | **P** | **P** | **P** | **P** |
| …and what is on its face | orange/yellow **floral mural**, header board "★ FRESH JUICES, GOURMET TACOS & TORTAS ★", side rails of menu items | same **floral mural** (seen from the rear) | floral/patterned (small in frame) | not visible | plain/reverse side to camera | **chalkboard menu** + "TACOMBI / NUEVA YORK / PLAYA DEL CARMEN", "BIENVENIDOS" rails | **chalkboard** "TACOS DE HOY", "TACOMBI" header, "…DA NOLITA ★" | **plain cream, bare** (white ribbed underside, nothing on it) | **tufted/upholstered cream panel with green medallions**, scalloped green carved border |
| mirrors | **P** (door-frame mirror) | not in view | **P** (round A-pillar mirror) | ? | **P** | ? | not in view | **P** (both sides) | **P** (white door mirror) |
| wipers (arm+blade vs bare spindle) | not in view | not in view | ? | ? | **none visible** | **none visible** | not in view | **none visible** | ? |
| bobble fringe | **A** | **A** | **A** — the "fringe" around the apertures is a **bulb string**, not bobbles (`S_playa_windows.png`, 6×) | A | A | A | A | A | A |
| bulb-lined board at the tail | **P** (raised board, right of frame) | **P** (raised tail lid, upper right) | **P** (small board at the tail) | not in view | not in view | ? | **P** (raised board, right) | **A** (a second plain lid, no bulbs) | **P** (white board, right) |
| headlamp bores | fitted | not in view | fitted (brass/chrome rim) | fitted | fitted, **lit** | fitted | not in view | **BARE HOLES — no lamps** | fitted |
| painted flank boards | — | — | — | — | — | — | — | — | **"TACOS" (orange) and "BREAKFAST SPECIAL" (red)** beside the louvres |

## 2.2 HOW MANY DISTINCT STATES

**FOUR, not three.  The record undercounts, and the audit that says so is right.**

- **G1 — `ref_workshop.jpg`** (GREEN, in build).  Script only.  No scrollwork, no burst, no
  stars, no boards.  Bare headlamp bores.  Plain cream lid with nothing on its face.  No
  tail board.  Bulbs already fitted to the lid rim.
- **G2 — `IMG_2073.jpeg`** (GREEN, in service).  Script **+ scrollwork + "100 % Calidad"
  burst + stars + "TACOS"/"BREAKFAST SPECIAL" flank boards**, headlamps fitted, tufted
  medallion-patterned lid with a scalloped green border, tail board.
  **G1 and G2 are not the same artwork state and must never be pooled.**
- **B — the four nolita frames** (`_flank`, `_front34`, `_front34b`, `_doorshut`) (RED,
  New York).  Plain red flank; TACOMBI.COM and 267 ELIZABETH STREET / NUEVA YORK lettering;
  **no scrollwork, no script, no burst, no star**; chalkboard lid.
  These four are **one** state: the only differences between them are the chalk menu text,
  which door or lid is open, and the ambient bulb strings — operational, not artwork.
- **C — `ref_side.jpg`, `ref_rear34.jpg`, `ref_playa_34.png`** (RED, current).  Scrollwork
  + script + burst + isolated star + bulb strings + floral mural lid + bulb-lined tail board.

## 2.3 ADMISSIBILITY

- **Artwork measurements of the target vehicle: ONLY `ref_side.jpg`, `ref_rear34.jpg`,
  `ref_playa_34.png` (and its duplicates IMG_3842.png / ref_source.jpeg).**  Three views.
- **`ref_nolita_*` (4 frames): geometry only** for the current build.  They are a genuine
  earlier state of the *same* vehicle, so they are admissible for bodywork, apertures,
  hardware and for the era-B lettering itself — never for state-C artwork.
- **`ref_workshop.jpg`, `IMG_2073.jpeg`: geometry only.**  IMG_2073 is the dangerous one:
  it carries a script, a scrollwork field, a burst and stars that *look* like the target's
  and are not.  Any decal measured off IMG_2073 is measured off the wrong vehicle.
- **`bus_model_ref.JPG`: nothing** — school bus, fidelity bar only.

---

# TASK 3 — TWO CHEAP CORROBORATIONS

## 3(a) Does the lid's support rod pass IN FRONT of the painted face?

**YES, in both frames.  I tried to refute it and could not.**

- **IMG_2073** — `P_2073_lid.png`, box (560,30)–(900,330), **3×**.  A white rod runs from
  the upper left down to the lower right and crosses the tufted cream/green-medallion lid
  face as an unbroken bright line over about 240 crop-px (≈ 80 image-px) of pattern, from
  crop (280,560) to (380,800).  It occludes the medallions; nothing occludes it.
  **CERTAINTY: HIGH.**  A second rod near the top right does disappear behind the green
  frame's top edge — so the rods are not *all* in front of everything, and that is the
  detail that makes the first one credible rather than a misread of a highlight.
- **ref_rear34** — `P_rear34_lid.png`, box (800,0)–(1200,200), **3×**.  A thin pale rod runs
  from upper right to lower left, crosses the yellow border and continues unbroken across
  the dark orange/yellow floral mural for the full width of the crop.
  **CERTAINTY: HIGH.**

The change (lid leaning over the counter rather than away from it) is **corroborated**.

## 3(b) The isolated star relative to the "100 % Calidad" burst

Segmentation: `R − G > thr` on the raw pixels, `scipy.ndimage.label`, blobs ≥ 25 px.
Positions are bounding-box centres; sizes are bounding-box widths/heights.  Sign convention:
image −x = LEFT, image −y = ABOVE.

**ref_side.jpg** (near-broadside — the reliable frame), box (695,295)–(850,385):

| thr (R−G) | burst bbox (merged) | star bbox | Δx / burst-W | Δy / burst-H | star W / burst W | star H / burst H |
|---|---|---|---|---|---|---|
| 40 | x 735–835 (W 101), y 306–380 (H 75) | x 710–727 (W 18), y 305–319 (H 15) | **−0.658** | **−0.413** | 0.178 | 0.200 |
| 60 | x 736–835 (W 100), y 306–379 (H 74) | x 711–726 (W 16), y 306–318 (H 13) | **−0.670** | **−0.412** | 0.160 | 0.176 |
| 80 | x 737–834 (W 98), y 307–377 (H 71) | x 712–724 (W 13), y 306–318 (H 13) | **−0.689** | **−0.423** | 0.133 | 0.183 |

**Star centre = (−0.67 ± 0.02) burst-widths, (−0.42 ± 0.01) burst-heights — ABOVE and LEFT.**
Stable to 3 % over a 2× threshold sweep.  Crop looked at: `Q_side_burst.png` (6×);
mask `Q_side_mask.png`.

**ref_rear34.jpg** (rear ¾, burst foreshorted horizontally and partly overlapped by the
scrollwork below), box (745,270)–(880,400):

| thr | burst bbox | star bbox | Δx / W | Δy / H | star W / burst W |
|---|---|---|---|---|---|
| 35 | x 776–839 (W 64), y 298–363 (H 66) | x 766–780 (W 15), y 283–299 (H 17) | −0.539 | −0.598 | 0.234 |
| 50 | x 776–838 (W 63), y 301–352 (H 52) | x 767–779 (W 13), y 284–298 (H 15) | −0.540 | −0.683 | 0.206 |
| 70 | x 780–837 (W 58), y 302–340 (H 39) | x 769–777 (W 9),  y 285–297 (H 13) | −0.612 | −0.769 | 0.155 |

**ABOVE-LEFT, confirmed.**  The *magnitudes* here are NOT stable (Δy/H drifts from −0.60 to
−0.77) because the burst's lower spikes fade into the scrollwork and its measured height
collapses with threshold.  **ref_rear34 corroborates the direction and nothing more.**
Correcting ref_rear34's horizontal foreshortening by the burst's own aspect
(64/55 vs ref_side's 101/75) gives −0.62 burst-widths — consistent with ref_side's −0.67.

**Against the build** (`cal_gen.py` lines 492–493):
```
_star(d, max(mx, cx - 0.92 * bw), min(h - my, cy + 0.52 * bw), r * 1.15, PINK)
```
i.e. **−0.92 burst-widths in x and +0.52 burst-widths in y (BELOW)**, radius
`0.085 · 1.15 · RO` ⇒ star width / burst width = **0.098**.

| | build | photograph (ref_side) | correction |
|---|---|---|---|
| x offset | −0.92 burst-W | **−0.67 ± 0.02** burst-W | move RIGHT by 0.25 burst-W |
| y offset | **+0.52** burst-W (below) | **−0.42 ± 0.01** burst-H (above) | **sign error** — move up by ≈ 0.9 burst-heights |
| star W / burst W | 0.098 | **0.13 – 0.18** (best 0.16) | **enlarge ×1.4 – ×1.8** |

**The record's "about 2.4× larger" is too big.**  My sweep gives ×1.36 (thr 80) to ×1.82
(thr 40); the low-threshold value is the least eroded and therefore the fairest, so ×1.7–1.8
is the defensible upper end and ×1.6 the central value.  The **position** finding —
above-left, not below-left — is confirmed and is the larger error by far.

---

# APPENDIX — crops looked at, and code

Crops (all under `probe_scratch/rev50/measure/`):
`A_2073_full.png`, `A_playa_full.png`, `B_2073_frontwheel.png`, `B_2073_rearwheel.png`,
`C_render34f.png`, `C_render_frontwheel.png`, `D_playa_frontwheel.png`,
`E_rear34_full.png`, `E_rear34_wheel.png`, `F_rear34_emblem.png`, `G_render_emblem.png`,
`G_render_emb2_*.png`, `H_2073_emblem.png`, `H_2073_emblem2.png`, `H_playa_emblem.png`,
`I_rear34_zone.png`, `I_rear34_emb_*.png`, `J_render_*.png`, `J_playa_*.png`,
`K_nolita_flank.png`, `L_2073_valve.png`, `L_side_wheel.png`, `M_side.png`,
`M_workshop.png`, `N_nolita_f34.png`, `N_nolita_f34b.png`, `N_nolita_door.png`,
`P_2073_lid.png`, `P_rear34_lid.png`, `Q_side_burst.png`, `Q_side_mask.png`,
`Q_rear34_burst.png`, `Q_rear34_mask.png`, `S_demo.png`, `S_dished.png`,
`S_playa_front.png`, `S_playa_windows.png`, `S_side_front.png`, `S_side_roof.png`.

Code: `crop.py`, `ellip.py` (conic fit; control: recovers a=46.0/b=30.0/centre to 0.06 px
under 0.4 px noise, and to 0.1 px on a 60 % arc), `rays.py`, `wheelfit.py`, `fitwheel2.py`,
`frame.py` (per-frame adaptive-level fitter), `emblem.py`, `emb_run.py`, `burst.py`,
`synth.py` (perspective wheel renderer: flat and analytic-cone dished variants),
`control_dished.py`, `control_H.py`, `calib.py`, `go2073f.py`, `run2073f.py`.
