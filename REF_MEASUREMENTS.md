# Tacombi (Playa del Carmen) — dimensional survey from three reference photographs

Source images (all in `/home/claude/tacombi/`):

| file | size | role |
|---|---|---|
| `ref_side.jpg` | 1024 x 768 | near-orthographic left side elevation, red livery, in service. **Primary measurement image.** |
| `ref_workshop.jpg` | 1200 x 824 | mid-conversion, green, front three-quarter. Nose geometry, bare rims, empty lamp apertures. |
| `ref_rear34.jpg` | 1200 x 824 | in service, red, rear three-quarter. Tail, counter wrap, rear wheel. |

Everything below is **measured in image pixels first**, then converted. Where a number is inferred
rather than measured it is labelled INFERRED. Where a thing cannot be resolved it says UNRESOLVED.

---

## 0. Scale, and the geometry of `ref_side.jpg`

### 0.1 Wheel centres

**Rear wheel.** The hubcap is a strongly saturated red disc. Method: HSV mask
(`h<25 or h>340`, `s>0.45`, `v>0.20`), connected-component label, hole-fill, then an algebraic
least-squares circle fit to the component boundary.

```
rear hubcap circle fit  centre = (749.60, 603.98)  R = 29.43 px  (D = 58.87 px)
boundary residual std   = 0.45 px  (n = 168 edge pixels)
```

Refined against the cream rim ring (see 0.3): rim-ring vertical extent at x = 749.6 is
y = 557.3 → 651.0 (50 % luminance crossings), midpoint **604.15** — agrees with the hubcap fit
to 0.2 px.

**REAR HUB = (749.60 ± 0.5, 604.0 ± 0.5) px**

**Front wheel.** Heavily occluded by the leaning man; only two arcs of the cream rim ring are
visible. Method: local-contrast normalisation (`L − boxblur31(L)`), sub-pixel threshold crossing
on the outer edge of each arc for every row y = 580…655 (118 edge points), then a robust
(soft-L1) circle fit.

```
free fit           centre = (242.59, 608.38)  R = 44.18 px   rms 2.37 px
extremes           left arc leftmost  (197.9, 605)
                   right arc rightmost(287.0, 607)   -> centre x = 242.45, half-width 44.6
constrained scan (cy fixed, cx & R free), rms:
  cy = 600 -> 3.85    cy = 608 -> 2.34    cy = 616 -> 3.90
  cy = 604 -> 2.85    cy = 612 -> 2.77    cy = 624 -> 6.83
```

A radial-profile template match (rear-wheel profile as template, ±38° about horizontal)
independently gives cx = 241.5–242.0 with a sharp peak (NCC 0.92, falls to 0.5 at ±4 px).

**FRONT HUB = (242.7 ± 2, 608.4 ± 3) px**

### 0.2 Two scales — and they DISAGREE

```
wheelbase in image   = 749.60 - 242.7            = 506.9 ± 2.5 px
scale from wheelbase = 506.9 px / 2.400 m        = 211.2 px/m   (4.735 mm/px)

rear tyre outside diameter (measured, see 0.3)   = 128 ± 4 px
scale from a nominal 6.40-15 tyre (0.683 m)      = 128 / 0.683  = 187.4 px/m
```

**Disagreement = 12.7 %, far outside the 5 % tolerance.**

I tested whether this is perspective and it is **not**:

* Long horizontal body lines in the image are **parallel, not convergent**. The counter's gold
  nosing (image y ≈ 420) and the rocker line (image y ≈ 595) have slopes −0.0385 and −0.0367;
  intersecting them puts the vanishing point at x ≈ −98 000 px, i.e. at infinity. A yawed
  vehicle would show measurable convergence over a 500 px baseline. It does not.
* Independent cross-checks of the wheelbase scale all agree with 211 px/m and not with 187 px/m:
  * overall length / wheelbase measured = 855/506.9 = 1.687 (stock T1 4280/2400 = 1.783 — 5 % low,
    consistent with a missing rear bumper, see §1);
  * rear overhang hub→rear panel = 170 px = 0.805 m (T1 ≈ 0.83 m);
  * front overhang hub→bumper face = 178 px = 0.841 m (T1 ≈ 0.90 m, and the bumper face is
    partly hidden behind a lamp post, see §1);
  * the leaning man measures 375 px = 1.78 m at 211 px/m (he is slightly nearer the camera, so
    his true height is a little under that — right for an adult male).

**Conclusion: the tyres on this vehicle are NOT 6.40-15.** See §8. All conversions below use
**S = 211.2 px/m (4.735 mm/px)** derived from the invariant 2.400 m wheelbase.

### 0.3 Reference frame, roll and rake — read this before using any height

Three separate "horizontal" lines were extracted and they do **not** share one slope:

```
counter gold nosing   y = 432.0 @ x=360 ... 407.5 @ x=930      slope -0.0385
visible cream/red edge y = 453.5 @ x=360 ... 435.0 @ x=900      slope -0.0385
rocker lower edge      y = 599   @ x=630 ... 590   @ x=875      slope -0.0367
drip-rail top edge     y = 304   @ x=560 ... 296   @ x=740      slope -0.0444
--- but ---
line through the two wheel centres  (242.7,608.4)->(749.6,604.0) slope -0.0087
```

Normalising the visible cream/red edge to a common station with slope −0.0385 gives
**mean y_ref = 439.45, sd 0.37 px over 32 columns** — i.e. the body lines really are straight and
really do share the −0.0385 slope. The axle line does not.

**MEASURED: the body sits nose-down by 1.71° ± 0.4° relative to the line joining the wheel
centres — 72 ± 18 mm of rake over the 2.400 m wheelbase.**

I could not eliminate "front wheels standing in a gutter" as a cause from `ref_side.jpg` alone;
the front wheel contact patch is hidden behind the man's shoe. But the front arch-to-tyre gap
(§2) is independently near zero, which supports a genuinely lowered front rather than uneven
ground. Flagged as a finding, not a certainty.

**Working frame used for every height below**

```
ground line   y_g(x) = 668.0 - 0.00868 (x - 749.6)      (parallel to the axle line)
body datum    y_ref  = y + 0.0385 (x - 749.6)           (removes the body's own line slope)
height        h      = (668.0 - y_ref) / 211.2   [metres, AT THE REAR-AXLE STATION]
model x       X      = (496.15 - x_img) / 211.2  [metres, +x forward, 0 = mid-wheelbase]
```

Because of the 1.71° rake, **every quoted height falls by 28 mm for each metre you move forward.**
E.g. the belt line is 1.207 m at the rear axle and 1.139 m at the front axle.

**Ground line.** Established at the rear contact patch by radial gradient search from the hub:
max luminance gradient at r = 63.5 px at θ = 90°, 65.5 at 80°, 68.5 at 70°, 72.5 at 60° — all
consistent with a single horizontal boundary at **y = 668.0 ± 1.5**. Cross-checked against the
background wall base (y ≈ 613) and the man's shoe (y ≈ 700): a pinhole model with camera height
≈ 1.55 m, horizon y ≈ 340, puts the wall 1.2× and the man 0.9× the bus distance — physically sane.

---

## 1. Overall length and overall height (lid closed)

### Length

```
front bumper leading face   x_img = 65 ± 8   (partly occluded by a white lamp post at x 62-80;
                                              cream bumper detectable ~3 px left of the post edge)
rearmost body point         x_img = 920 ± 5  (max x of the red lower body, rows y 480-580;
                                              the roof rear edge is at 897, the tail panel bulges aft of it)
overall (bumper face -> tail panel)  855 ± 10 px  = 4.048 ± 0.05 m
```

**There is no rear bumper.** `ref_rear34.jpg` shows the tail panel curving under into shadow with
no bumper blade; `ref_side.jpg` shows the same. Add ~0.09 m if you model one.
Stock T1 over bumpers is 4.28 m; **measured 4.05 m without a rear bumper is consistent.**

In model coordinates: front bumper face **X = +2.041 m**, tail panel **X = −2.007 m**
(the model's ±2.108 is ~70 mm longer at each end than I measure).

### Height, roof lid CLOSED

The lid IS open in `ref_side.jpg`. The **closed roofline** is the fixed roof aft of the lid
opening, unobstructed between x = 770 and x = 820 (the raised rear lid appears as the gold-edged
diagonal starting at x ≈ 883, and the flower board / front lid ends at x ≈ 745).

```
roof crown top edge   y = 252.5 (x 770-810), 253.5 (x 800), 256.5 (x 820)   [max luminance gradient]
                      -> y_ref = 254.1
ground at that station                                       = 668.0
overall height        = 413.9 px = 1.960 ± 0.03 m   (at the rear-axle station)
                                   1.892 m at the front-axle station (rake)
```

The flower board (top ≈ y 35) and the raised lid are excluded.

**This is ~30 mm MORE than a stock T1's 1.93 m even though the vehicle is lowered ~100 mm (§2).**
INFERRED: the roof-lid frame added by the conversion stands roughly **0.10–0.15 m proud of the
original roof skin**. Supporting evidence: the drip-rail / top-of-fixed-cream line measures
1.756 m, i.e. 204 mm below the crown, where a stock T1 side silhouette shows only ~120–140 mm.
Treat 0.10–0.15 m as an inference, not a measurement.

---

## 2. Ride height — VERDICT: **LOWERED**, and lowered more at the front

### Arch-to-tyre gap, REAR (measured)

Rear arch lip traced by scanning down each column for the first sustained run of non-livery pixels:

```
x:   655  660  665  670  680  690  700  710  730  750  765  780  800  820  840  853
lip: 586  564  555  548  539  532  530  527  526  525  524  525  529  537  566  590
arch meets rocker at x = 652 (front) and x = 853 (rear); mid = 752.5 (hub is at 749.6)
arch lip at the hub station        y = 525.0  -> 0.677 m above ground
tyre top   = 604.0 - 64.0          y = 540.0  -> 0.606 m above ground
ARCH-TO-TYRE GAP (rear) = 15.0 ± 2 px = 71 ± 10 mm
```

### Arch-to-tyre gap, FRONT (low confidence)

The front arch lip is only traceable ahead of the man, x = 125–190, where it is flat at
y = 546 ± 4. The rear arch's flat top extends ±45 px from its apex, so extrapolating the same
shape puts the front apex at y ≈ 540–546 at x = 242.7. The front tyre top is at
608.4 − 64.0 = 544.4.

**FRONT ARCH-TO-TYRE GAP ≈ 0–25 mm.** Confidence low (the lower front flank is in deep shadow and
the livery mask fails there) but it is independently consistent with the 72 mm of nose-down rake
measured in §0.3 — the front is effectively slammed.

### Rocker / lower body edge

```
red body lower edge  y = 599 @ x 610-650, y = 590 @ x 855-900   -> y_ref = 594.4 ± 0.5
ROCKER HEIGHT ABOVE GROUND = 73.6 px = 0.348 m  (at the rear axle; 0.280 m at the front axle)
front bumper blade: top y = 600, bottom y = 628 at x ≈ 125
   -> top    0.348 m above ground
   -> bottom 0.215 m above ground
   -> blade face height 28 px = 0.133 m  (a T1 blade is ~0.12 m -> confirms the identification
                                          and independently confirms the scale)
```

Stock T1 front bumper top is ≈ 0.46–0.48 m. **Measured 0.348 m — 110 to 130 mm low.**

### Verdict, with the arithmetic

Taking the brief's own figure of 90–120 mm of arch-to-tyre gap for a stock T1 on 683 mm tyres:

```
stock arch lip above hub = 341.5 + (90..120)   = 431..461 mm
this bus, arch lip above hub = 71 + 303        = 374 mm
  -> suspension lowered at the rear by          57..87 mm
hub centre height: this bus 0.303 m vs stock 0.3415 m
  -> a further                                  38 mm from the smaller tyres
REAR body drop vs stock                       = 95..125 mm
FRONT body drop vs stock                      = rear drop + 72 mm rake = 167..197 mm
```

**VERDICT: this bus is LOWERED, not stock. ~100–125 mm down at the rear and ~170–195 mm down at
the front, of which ~40 mm at both ends comes from non-stock small-diameter tyres and the rest
from suspension. It also carries ~1.7° of nose-down rake.** The one caveat: the rear arch gap
(71 mm) is not dramatic on its own; the strong evidence is the rake plus the low bumper plus the
tyre size.

Actual ground clearance under the chassis/engine: **UNRESOLVED** — the whole underbody is in
deep shadow in all three photographs. Use the 0.348 m rocker edge as the modelling proxy.

---

## 3. Two-tone paint break (belt line) — the model is wrong, but not by the amount you might think

There are **two** cream/red horizontal edges on this flank and they must not be confused.

### (a) The body's own two-tone break — visible on the cab door, where there is no counter

Direct pixel sampling of columns x = 130 / 150 / 170 / 190 (clear of the man):

```
x=130: window opening ends y=417 | cream 418-435 | RED from 436   (rgb 0.56,0.17,0.14)
x=150: window opening ends y=417 | cream 418-435 | RED from 436   (rgb 0.60,0.23,0.18)
x=170: window opening ends y=418 | cream 420-437 | RED from 438
x=190:                             cream 422-436 | RED from 438
```

```
cab-door break            y_ref = 413.1 ± 1.0
BODY TWO-TONE BREAK HEIGHT = 254.9 px = 1.207 ± 0.010 m above ground (rear-axle station)
cab-door window sill      y_ref = 394.3   (continuous with the serving-aperture sill, 392.0)
BREAK BELOW THE WINDOW-BAND SILL = 21.1 px = 0.100 m  ->  ** 100 mm **
```

### (b) The visible cream/red edge along the serving side — this is the counter fascia, not paint

```
mean y_ref = 439.45, sd 0.37 px (32 columns, x 340-940)
height = 1.082 ± 0.008 m above ground;  225 mm below the window sill
```

Colour evidence that (b) is the counter and not the body: the band between the gold nosing and
the red reads rgb ≈ (0.84, 0.75, 0.65) — a warm beige — while the sunlit body cream immediately
above the counter reads (0.95, 0.94, 0.96), an almost neutral white. The counter's gold nosing
sits at y_ref 416.8 (1.189 m), i.e. **within 4 px of the body break at 413.1**: the counter was
mounted right on the belt line and its fascia hangs 107 mm down over the top of the red.

### Answer for the model

* If the model's "two-tone break" is the **painted** break in the sheet metal:
  **1.207 m above ground, 100 mm below the window-band sill** — the current 16 mm is too small by
  a factor of ~6.
* If the model's "two-tone break" is meant to be the **visible** cream/red edge on the serving
  flank (which is what the photograph reads as, aft of the cab door):
  **1.082 m above ground, 225 mm below the sill**.

Note the counter is 300 mm outboard of the flank (§6); correcting the gold nosing and fascia
bottom for that parallax raises them ~16–21 mm, to 1.205 m and 1.103 m respectively. Both
corrections are inside the error band on the ground line.

---

## 4. Window band

Read from the aperture frames' outer dark outlines at 8x zoom (±3 px per reading), then
normalised with the body slope:

```
                     top y      bottom y     y_ref top   y_ref bottom
aperture 1 (x 376)   324.0      405.6        309.6       391.2
aperture 2 (x 510)   314.8      400.0        305.5       390.8
aperture 3 (x 644)   309.4      398.0        305.3       393.9
mean                                         306.8 ±2.4  392.0 ±1.7
```

```
WINDOW-BAND SILL  = (668.0 - 392.0)/211.2 = 1.307 ± 0.015 m above ground
WINDOW-BAND HEAD  = (668.0 - 306.8)/211.2 = 1.710 ± 0.020 m above ground
BAND HEIGHT       = 85.2 px               = 0.403 ± 0.020 m
```

The cab-door window sill (y_ref 394.3) is 2 px below the serving sill — **the sills are
effectively one continuous line** at 1.30 m.

---

## 5. The three serving apertures

Measured at 8x from the frames' outer dark outline (the sheet-metal cut edge) and, in brackets,
from the clear glass opening inside the beaded trim.

```
                     x_img front   x_img rear    width px    width m
aperture 1           323 (328)     430 (425)     107 (97)    0.507 (0.459)
aperture 2           455 (460)     564 (559)     109 (99)    0.516 (0.469)
aperture 3           588 (594)     699 (695)     111 (101)   0.526 (0.478)
solid cream rear
corner panel         699           920           221         1.046
```

Pillars between them: 430→455 = 25 px = 0.118 m; 564→588 = 24 px = 0.114 m.
Pillar between the cab-door shutline (x 296) and aperture 1: 27 px = 0.128 m.

### Positions, three ways

Datum for "from the front bumper" is the bumper face at x_img = 65 (± 8 px = ± 0.04 m —
this is the single largest systematic in this table). Overall length L = 855 px.

```
                        from front bumper (m)     fraction of L        MODEL x (m)
aperture 1  front            1.222                    0.302              +0.820
aperture 1  rear             1.728                    0.427              +0.313
aperture 2  front            1.847                    0.456              +0.195
aperture 2  rear             2.363                    0.584              -0.321
aperture 3  front            2.476                    0.612              -0.435
aperture 3  rear             3.002                    0.742              -0.960
rear corner panel  fwd       3.002                    0.742              -0.960
rear corner panel  aft       4.048                    1.000              -2.007
```

**Solid cream rear-corner panel = 1.046 m long = 0.258 of overall length.**

Aperture widths as a fraction of L: 0.125 / 0.127 / 0.130 — they grow very slightly rearward,
which is within the ±3 px reading error; treat them as three equal ~0.515 m openings.

Reference marks for aligning textures: the "100 % Calidad" sunburst decal spans x 718–830
(X = −1.051 → −1.581 m), y 290–350.

---

## 6. The counter

```
gold/brass nosing (outer top edge)  y_ref = 416.8 ± 0.6 (mean of 10 columns, sd 0.6)
                                    -> 1.189 m above ground (1.205 m parallax-corrected)
fascia bottom (cream -> red)        y_ref = 439.45 ± 0.37
                                    -> 1.082 m above ground (1.103 m parallax-corrected)
FASCIA / SLAB EDGE DEPTH            22.65 px = 0.107 ± 0.005 m
```

Vertical profile through the counter (x = 720, typical): white counter top to y 406, dark shadow
line 408–411, saturated gold nosing 414–420 (h ≈ 32°, s ≈ 0.86), beige fascia 422–440, red 442+.

```
LONGITUDINAL EXTENT   front end x_img = 302 ± 8   (immediately aft of the cab-door shutline at 296)
                      rear  end x_img = 986 ± 4   (last gold pixels at x = 984, none at 988)
                      length 684 px = 3.238 m
MODEL x               +0.919  ->  -2.319
```

```
OVERHANG PAST THE TAIL  986 - 920 = 66 px = 0.313 ± 0.06 m   -> YES, it overhangs
```

**OUTBOARD PROJECTION ≈ 0.30 ± 0.06 m (INFERRED).** `ref_rear34.jpg` shows the counter turning
the rear corner and running right across the tail (the gold nosing crosses the rear panel above
the "1963" plate), so the counter's rearmost surface is its outer edge offset by the projection
from the rear panel. That makes the 0.313 m rear overhang a direct proxy for the outboard
projection. `ref_workshop.jpg` corroborates the form: the shelf there is a plain slab with a
visible edge face and a boxed drop-panel below it between x 712 and 800.

Counter top is wood/tan with a brass nosing (`ref_rear34.jpg`); the fascia below the nosing is
beige. It is a full wrap: **side + rear**, not a straight side shelf.

---

## 7. Rear-quarter louvres

Detected as a stack of thin dark horizontal lines in the red rear quarter, above the rear wheel
and just below the belt line. Row-mean high-pass over x 770–840 gives dark rows at
y = 450.5, 454, 459.5, 463.5, 471.5, 481, 490 (plus one or two more that do not clear the noise
floor at this JPEG resolution).

```
COUNT            7 clear slots, probably 7-9        (moderate confidence)
BLOCK EXTENT     x 765 -> 855 (± 10)   = 90 px  = 0.426 m long
                 MODEL x  -1.273 -> -1.699
                 y 452 -> 492 (y_ref 454.0 -> 493.9) = 40 px = 0.189 m tall
HEIGHT           top slot    1.013 m above ground   (63 mm below the body belt line at 1.207 m)
                 bottom slot 0.824 m above ground
PITCH            ~5 px = 24 mm
```

The rear axle is at X = −1.200 m, so the louvre block sits from just aft of the rear hub to just
short of the rear arch's aft edge (X = −1.690). Individual slot positions are at the resolution
limit — take the block extent as reliable, the count as approximate.

---

## 8. Wheels — the white ring is the RIM, and the tyres are not stock

### The white ring is the painted rim, not a whitewall

1. Radial profile from the hub centre, rear wheel: red 0–29 px, **cream 30.5–46.2 px**, black
   beyond. The cream annulus is *inboard* of the black. A whitewall band lives on the tyre
   sidewall, i.e. *outboard* of the rim flange. The observed order is only possible if the cream
   is the wheel disc.
2. At 8x the cream annulus shows concentric steps/ridges — the dished wheel-disc profile ending
   in the flange lip — not the flat face of a whitewall.
3. A valve stem is visible crossing the cream annulus at ≈ (777, 578).
4. `ref_workshop.jpg` shows the same wheels bare, no hubcaps: white painted steel discs with
   visible ventilation slots, and the same tyre/rim proportion.

### Numbers (rear wheel, `ref_side.jpg`)

```
hubcap disc D                  58.87 px  = 0.279 m   (circle fit, resid sd 0.45 px)
rim outer (flange) D           92.31 px  = 0.437 m   (median outer radius over 72 angular bins,
                                                      45.0-47.1 px; vertical 50 % crossings give 93.7)
rim inner boundary D           61.06 px             (= the hubcap edge, consistent)
tyre outer D                   128 ± 4 px = 0.606 ± 0.019 m
   (bottom: ground contact y 668.0 -> r = 64.0;  top: luminance step at y 536-540 -> r = 64-68;
    rear flank edge at hub height x ~ 815 -> r ~ 65)

hubcap D / tyre D              = 0.460
rim outer D / tyre D           = 0.721
```

### Cross-check in the other two photographs

```
ref_workshop.jpg rear wheel (bare rim):  rim vertical extent y 581-657 = 76 px
                                         tyre bottom y 675 -> tyre D = 112 px
                                         tyre D / rim D = 1.47
ref_side.jpg                             tyre D / rim D = 128 / 92.3 = 1.39-1.45
```

**A stock 6.40-15 on a 15-inch rim gives tyre D / rim D = 683 / 405 = 1.69.** Two independent
photographs give 1.39–1.47. Whatever the rim is (14 / 15 / 16 in, flange OD 380 / 405 / 430 mm),
the tyre is a modern low-profile radial of roughly **0.59–0.63 m outside diameter**, i.e.
**50–90 mm smaller in diameter than the 1963 original**. At the wheelbase scale the rim flange
measures 0.437 m, which is closest to a 16-inch rim — but that reading carries the JPEG blur of
the flange edge, so I quote the ratio as the robust result and 0.606 m as the tyre OD to model.

For the model: hubcap = 0.46 × tyre OD; painted rim = 0.72 × tyre OD; tyre OD = 0.606 m;
tyre radius (loaded, as photographed) = 0.303 m.

---

## 9. Nose (from `ref_workshop.jpg`)

Caveat up front: this is a close, strongly-perspective three-quarter shot of a curved surface.
Lateral scale varies by more than 2:1 across the front panel (I fitted a projection model and it
did not close, which is itself evidence that the panel is not planar). Vertical *ratios* below
are solid; absolute heights are anchored to features whose absolute height I know from
`ref_side.jpg` and carry a ±0.06 m band.

### Measured positions (workshop image pixels)

```
VW roundel emblem centre        (306, 546)     D = 65 px
two-tone V apex (centreline)    (311.5, 669)   ± 4 px    <-- WRONG, see SPEC 10.85 (rev 31b)
        [CORRECTED, rev 31b: this is NOT the apex.  The V's arms have not converged at
         v=669 and the over-rider bar's top edge is at v=672.5, occluding the vertex.
         This point lies 3.98 px from the RIGHT arm and 30.75 px from the LEFT -- it is
         the RIGHT ARM'S OCCLUSION POINT AT THE BAR.  A vertex is equidistant from both.
         The arms, traced 42 rows each (rms 0.112 / 0.806 px) and intersected, cross at
         u = 288.8 +- 3 px SYSTEMATIC (band from a half-band split; a bootstrap's +-0.2
         is a false precision).  COLUMN SHIFT -22.7 px.  Only the COLUMN is published:
         the V is radiused at the tip so the crossing's ROW is not a measurement.
         Everything in this file that used 311.5 as the centreline inherits this.]   -> 104 px below the emblem centre,
                                                           i.e. 1.60 x emblem diameter
V near arm, at the headlamp x   (419, 524)
V arm at the body corner        (~520, 500), merging into the flank belt line at (590-690, 487-495)
headlamp aperture               centre (419, 629)  width 76.9 px  height 75.6 px  -> circular
indicator aperture              centre (456.6, 564.4)  width 30.6 px  height 30.0 px -> circular
front bumper blade (centreline) top y = 718, bottom y = 750
```

### Absolute heights (INFERRED, ±0.06 m)

Anchors: flank belt line = 1.207 m (measured in `ref_side.jpg`, §3a); front bumper top =
0.348 m (measured in `ref_side.jpg`, §2). Local scale on the near side of the front panel from
the headlamp aperture taken as 0.180 m -> 422 px/m.

```
V-SWAGE APEX, on the centreline      ~ 0.49 m above ground
      (49 px above the bumper top at the same image x, hence the same depth;
       centreline scale ~355 px/m -> 0.138 m above the bumper top)
V ARMS WHERE THEY MEET THE BODY CORNERS  ~ 1.05-1.08 m above ground
      (the arms run into and become the flank belt line at 1.207 m at the rear-axle station;
       at the front of the body the rake has dropped that line to ~1.13 m, and the corner
       reading sits ~20 mm below the flank line)
HEADLAMP CENTRE                      ~ 0.77 m above ground
      (105 px = 0.249 m below the V arm at its own x; that arm is ~1.02 m)
INDICATOR CENTRE                     ~ 0.93 m above ground
      = 0.155 m above the headlamp centre, 0.089 m outboard of it (37.6 px)
```

A stock-height T1 headlamp centre is ≈ 0.88 m; 0.77 m here is another ~0.11 m of lowering,
consistent with §2.

### Indicator type — what I actually see

The lens is **not fitted** in `ref_workshop.jpg` (the brief is right: the apertures are empty),
and in `ref_side.jpg` / `ref_rear34.jpg` the front panel is never presented squarely enough to
resolve a lens.

What is measurable is the **aperture**: a clean **round hole, 30.3 px, i.e. 0.398 × the headlamp
aperture ≈ 72–76 mm**, with equal width and height to within 0.6 px. There is no oval or
teardrop outline around it and no raised pod footprint. A small stub (wiring grommet or mounting
stud) protrudes at (472–477, 564–566).

So: the panel cut-out is round and ~75 mm across. That is too large for the ~48 mm base of a
1955–Aug 1961 bullet lamp, and it is not the elongated oval you would expect a fish-eye housing
to sit in. **The lens type itself is UNRESOLVED from these three photographs** — I can only give
you the hole. If you must choose, model a round-based lamp on a 75 mm aperture centred 0.155 m
above and 0.089 m outboard of the headlamp centre.

Also note: the emblem-to-headlamp size ratio measures 65 / 76.5 = 0.85, so if you model the
headlamp aperture at 0.180 m the emblem should be **0.153 m**, not the ~0.30 m sometimes quoted.

---

## 10. Other dimensionally significant things you did not ask about

1. **No rear bumper.** Confirmed in both `ref_side.jpg` and `ref_rear34.jpg`. The tail panel
   curves under into shadow with nothing below it. This is why the measured overall length is
   4.05 m rather than 4.28 m.

2. **A serving opening in the REAR face as well.** `ref_rear34.jpg` shows a large glazed opening
   in the rear panel above the tail (x 1055–1200, y 300–405 in that image) with a blender,
   bottles and a stainless work surface behind it, and the counter running across it. The bus
   serves from the side *and* the rear. A three-aperture side-only model is incomplete.

3. **Two roof lids, not one.** `ref_workshop.jpg` shows a big front/centre lid hinged at its rear
   edge, plus a smaller rear lid. In `ref_side.jpg` the front lid carries the flower board and
   the rear lid appears as the gold-edged diagonal running from (883, 292) up to (1010, 190).
   In `ref_rear34.jpg` the rear lid is up and lettered "LA SANTA…".

4. **Roof line / drip rail.** Top of the fixed cream body (drip rail / light-string line) is at
   y_ref 297.2 → **1.756 m above ground**; roof crown 1.960 m. The 0.204 m between them is
   larger than a stock T1's ~0.12–0.14 m, which is the basis for the raised-roof-frame inference
   in §1.

5. **Rear wheel arch opening**: x 652 → 853 = 201 px = **0.952 m wide**, centred at x 752.5
   (model X = −1.214 m, i.e. 14 mm aft of the rear hub). Lip apex 0.677 m above ground,
   flat-topped over x 705–800 (±0.22 m about the hub).

6. **Cab door rear shutline** at x_img 296 → model **X = +0.948 m**. The counter starts 6 px aft
   of it. The pillar between the door and aperture 1 is only 0.128 m — the conversion cut the
   openings hard up against the cab.

7. **Decorative light strings** run along the roof gutter line (visible at y ≈ 296–304,
   x 560–740, and continuing round the rear lid edge) and along the lower body at the nose
   (three bulbs at x 170–180, y 558–590). If you model these, the gutter run is at ≈ 1.75 m.

8. **The window band is not parallel to the ground** — everything on the body carries the 1.71°
   nose-down rake. If your model is built with a horizontal body datum and then simply dropped,
   it will not match the photograph; you need to pitch the body relative to the wheels (or
   accept a mismatch that grows to ~70 mm across the wheelbase).

9. **The counter's front end is aft of the cab door**, so the cab door is fully exposed and its
   two-tone break (1.207 m) is the only place the true body belt line is visible in `ref_side.jpg`.

10. **Aperture frames** are surrounded by a beaded/dotted bright trim ~5 px (24 mm) wide inside
    the cut edge, and the corners are generously rounded (radius ≈ 12 px ≈ 57 mm). There are
    printed menu strips applied to the flank at x 301–321, 431–451 and 565–587 — decals, not
    structure.

---

## Summary table (model frame: +x forward, 0 = mid-wheelbase, heights above ground at the rear axle)

| feature | model X (m) | height (m) | source / confidence |
|---|---|---|---|
| front bumper face | +2.041 | top 0.348 / bottom 0.215 | measured, ±0.04 in X |
| front hub | +1.200 | 0.303 | measured |
| cab door rear shutline | +0.948 | — | measured |
| counter front end | +0.919 | — | measured ±0.04 |
| aperture 1 | +0.820 → +0.313 | sill 1.307, head 1.710 | measured ±0.015 |
| aperture 2 | +0.195 → −0.321 | " | measured |
| aperture 3 | −0.435 → −0.960 | " | measured |
| rear arch opening | −0.738 → −1.690 | lip 0.677 | measured |
| rear hub | −1.200 | 0.303 | measured |
| louvre block | −1.273 → −1.699 | 0.824–1.013 | measured (count approximate) |
| solid rear corner panel | −0.960 → −2.007 | — | measured |
| tail panel | −2.007 | — | measured ±0.025 |
| counter rear end | −2.319 | top 1.189, bottom 1.082 | measured |
| body two-tone break | full length | 1.207 | measured on the cab door |
| roof crown (lid closed) | −1.39 (measured at) | 1.960 | measured |

Scale used throughout: **211.2 px/m in `ref_side.jpg`** (4.735 mm/px), from the 2.400 m wheelbase.

---

## Verification pass — contested claims

Independent re-derivation of claims A, B and C. Nothing below reuses a number from
§0–§10; every figure was re-measured from the pixels. Where a prior number is quoted it is
labelled *(prior)*. Methods deliberately differ from the ones that produced the claims.

### V0. Method summary

| what | method | image |
|---|---|---|
| rear hub | HSV mask of the red hubcap → hole-fill → algebraic circle fit to the boundary | `ref_side` |
| rim flange OD | 360 rays from the hub, sub-pixel 50 %-luminance crossing, then general-conic (ellipse) fit | `ref_side` |
| tyre OD | 72 rays, steepest-gradient edge, restricted to sectors where the tyre silhouettes against **deep arch shadow** (not against the ground) | `ref_side` |
| front hub | (i) x-extremes of the two visible cream rim arcs, (ii) contrast-normalised visual extremes, (iii) **wheel-arch geometry** — a body feature, wholly independent of the wheel | `ref_side` |
| rim/tyre cross-check | ellipse fit to the bare white rim + vertical luminance profile through the wheel centre | `ref_workshop`, `ref_rear34` |
| rear bumper | gamma-lifted shadow crops of the tail in all three images | all |

### V1. The front hub does **not** need the occluded circle fit

Three independent routes, one of which uses no wheel pixels at all:

```
(i)   cream rim arcs, x-extremes         leftmost 197.9   rightmost 282.5   -> centre 240.2
(ii)  same arcs on a locally contrast-normalised crop      198.0 / 289.0    -> centre 243.5
(iii) WHEEL-ARCH GEOMETRY (body feature, no wheel pixels):
        rear arch lip meets rocker at x = 654 and x = 852  -> opening 198 px, centre 753.0
        (rear hub 749.6, so the arch centre sits +3.4 px aft of the hub)
        front arch lip leaves the rocker at x = 140...150
        -> front arch centre 239...249  -> front hub 236...246
```

All three agree. **FRONT HUB = 242 ± 3 px**, i.e. the prior 242.7 was correct — it just was not
independently supported.

```
WHEELBASE          = 749.56 - 242 = 507.6 ± 3 px
SCALE  S           = 507.6 / 2.400 = 211.5 ± 1.3 px/m      (4.728 mm/px)
```

*(prior: 211.2 px/m — no material change.)*

### V2. Why the rim-flange route gives a different answer: **the rims are not 15 inch**

The rim flange edge is the crispest thing on the vehicle and it was re-measured properly:

```
rear rim flange, 360-ray sub-pixel 50 % crossing
    r = 46.48 ± 0.38 px   (n = 360, per-quadrant means 46.65 / 46.55 / 46.76 / 45.98)
    ellipse fit: semi-axes 46.86 / 46.11, axis ratio 0.984  -> circular to 1.6 %
    => RIM FLANGE OUTER D = 92.97 ± 0.8 px
```

The axis ratio 0.984 also **kills the "it's perspective" escape**: the rear wheel is presented
essentially face-on. A projective solve using the front/rear rim size ratio changes
wheelbase/flange by less than 1 %.

```
WHEELBASE / FLANGE OD = 507.6 / 92.97 = 5.46 ± 0.08
factory 15" J rim (381 + 2x17.3 = 416 mm):  2400/416 = 5.77   <- 4 sigma away
factory 16" J rim (406 + 2x17.3 = 441 mm):  2400/441 = 5.44   <- matches
```

**So the flange OD is 0.440 ± 0.008 m — a 16-inch rim, not a 15-inch one.** Route (a) of the
brief ("a 15-inch rim gives px-per-metre directly") is built on a false premise for this vehicle;
it yields 92.97/0.406 = 229 px/m, and that scale is refuted by everything else in the frame:

| test | at S = 211.5 px/m | at S = 229 px/m | factory / plausible |
|---|---|---|---|
| front overhang (hub → bumper face) | **0.849 m** | 0.784 m | 0.85–0.88 m |
| rear wheel-arch opening | **0.936 m** | 0.865 m | ~0.95 m |
| leaning man, raw height | **1.77 m** (≈1.68 m depth-corrected) | 1.64 m (≈1.55 m) | adult male |
| front bumper blade face height | **0.123 m** | 0.113 m | 0.12 m |

**S = 211.5 px/m. The prior scale was right; the prior's tyre-based cross-check was wrong
because it assumed a 15-inch rim.**

### V3. CLAIM A — REFUTED. The body is **not** shortened.

Re-measured endpoints:

```
front bumper leading face   x = 62.5 ± 2.5
   the white lamp post leans: its left edge follows x = 60.5 + 0.0514 (y - 430),
   so at bumper height it is at x = 68-69. Cream is detectable out to x = 61.9-63.0
   at y = 584-604, i.e. 5-7 px AHEAD of the post. That cream is the bumper.
rearmost red body           x = 920.7 ± 1.5
   (constant 917-921 over y = 478...574; verified on a gamma-lifted crop —
    the pale background wall behind the tail makes this a high-contrast edge)
L (bumper face -> rearmost sheet metal) = 858 ± 4 px = 4.06 ± 0.04 m
```

So the prior's **4.05 m number is confirmed as a measurement** — and it does *not* overturn the
factory dimension. Here is the closure:

```
measured front overhang  (front hub -> bumper face)   179.5 px = 0.849 m
measured rear overhang   (rear hub -> rear sheet metal)171.1 px = 0.809 m
                                                       sum      = 1.658 m
factory total overhang   = 4.280 - 2.400              = 1.880 m
                                            DEFICIT   = 0.222 m
```

The front bumper **is** fitted, so the whole deficit has to sit at the rear. Independent
measurement of exactly that quantity, in `ref_workshop` where the rear bumper *is* fitted:

```
body rear corner   x = 936    (green -> background step, rows 490/510/530/550)
bumper aftmost pt  x = 948.7
difference 12.7 px image;  the rim ellipse at that wheel gives cos(beta) = 0.347
-> 36.6 px in the wheel plane;  rim vertical D there = 71.32 px = 0.440 m
-> REAR BUMPER STANDS 0.21 - 0.23 m AFT OF THE REARMOST BODY PANEL
```

0.222 m needed, 0.21–0.23 m measured. **The vehicle is a full-length T1.**

```
OVERALL LENGTH, as photographed (no rear bumper)   4.06 ± 0.04 m
OVERALL LENGTH, factory configuration              4.28 ± 0.06 m
```

Model frame (X = (495.8 - x_img)/211.5, +x forward, 0 = mid-wheelbase):

```
front bumper face      X = +2.049 m
rearmost sheet metal   X = -2.009 m
rear bumper face IF MODELLED  X = -2.219 m   (x_img ~ 965)
```

Consequence for §6: the counter's rear end (x_img 986) overhangs the **factory bumper line** by
only 0.10 m, not the 0.31 m quoted against the bare body.

**Verdict: the body is NOT shortened; the prior scale was NOT wrong. The prior error was a
configuration mismatch — a no-rear-bumper measurement compared against an over-bumpers factory
figure, with only 0.09 m allowed for the missing bumper instead of the true 0.22 m.**

### V4. CLAIM B — half confirmed, half refuted

Radial profile through the rear wheel, `ref_side`, mean of 170 rays each normalised by its own
cream plateau (so illumination differences cancel). Transition radii from the hub centre:

```
r = 29.4    red hubcap  ->  cream            (gradient peak at r = 30.0, rise 28.5->31.5)
r = 36.5 / 39.5 / 41.0 / 42.8 / 44.0 / 45.0  concentric ridges and grooves of the wheel disc
                                             (amplitude +-8 %, no step large enough to be a
                                              rim-flange / whitewall boundary)
r = 46.4    cream  ->  black                 (50 % crossing; falls 45.25 -> 47.5)   RIM FLANGE
r = 70.3 ± 0.8  tyre -> deep arch shadow     TYRE OUTER
```

The tyre outer edge is measurable only in the sectors where the tyre silhouettes against the
**shadow inside the wheel arch** (theta 155-240 deg and 295-330 deg, 20 rays, r = 68.5-71.4,
inside L ≈ 0.10-0.15, outside L ≈ 0.04-0.05). Below the wheel every "edge" follows
r = h/sin(theta) — that is the **ground/shadow line, not the tyre**, which is where the prior
pass's 128 px came from.

```
                          ref_side          ref_workshop            ref_rear34
rim flange (px)           92.97 ± 0.8       71.32 (ellipse major)   141.44 (ellipse major)
tyre outer (px)          140.6  ± 1.6      102.1 (loaded, 2x51.06)  --- (bottom off-frame)
TYRE OD / RIM FLANGE OD   1.512 ± 0.02     1.432 loaded             cos(beta) 0.337 / 0.347
                                            ~1.48-1.50 unloaded
```

`ref_workshop` is the control: bare **white** rims, unambiguously **black-wall** tyres, so its
white/black boundary is definitely the flange. It gives the same ratio as `ref_side`, which
rules out the alternative explanation that the cream annulus in the red livery is a whitewall
band inflating the apparent rim.

```
TYRE OD / RIM FLANGE OD = 1.50 ± 0.03      (a 6.40-15 on a 15" rim would be 683/416 = 1.64-1.68)
```

* **CONFIRMED:** the tyres are **not** 6.40-15. The ratio is 1.50, not 1.64–1.68.
* **REFUTED:** the OD is **not** 0.606 m.

```
RIM FLANGE OUTER D = 92.97 / 211.5 = 0.440 ± 0.008 m   -> 16-inch rim
TYRE OUTSIDE D     = 140.6 / 211.5 = 0.665 ± 0.015 m   (6.40-15 is 0.683 — only 2.6 % more)
sidewall height    = (665 - 440)/2 = 112 mm
loaded radius      = 0.307 m  (hub y 603.9, contact y ~670 ± 2)
hubcap disc D      = 58.74 / 211.5 = 0.278 m   (an oversize aftermarket dome cap, not the
                                                ~0.25 m factory VW cap — do not use it as a ruler)
```

A 0.665 m tyre with a 112 mm sidewall on a 0.44 m rim is a **modern low-profile 16-inch fitment**
— 215/60R16 (0.664 m) or 205/65R16 (0.673 m) are exact matches. The anomaly in §8 was the
**rim**, which is one size up from stock, not the tyre, which is close to stock diameter.

**Net effect on the model:** tyre OD 0.665 m (not 0.606), rim 0.440 m (not 0.437 — unchanged in
practice), so §2's ride-height verdict weakens: the hub sits at 0.307 m vs a stock 0.3415 m, i.e.
only ~35 mm of the drop comes from the wheels, and the arch-to-tyre gap is 79 - 70.3 = 8.7 px
= **41 mm**, not 71 mm. The bus is still lowered, but the tyre-diameter contribution is smaller
than §2 assumed and the front-to-rear rake finding is untouched.

### V5. CLAIM C — CONFIRMED (in service). But the workshop bumper is real.

```
ref_side, tail, gamma-lifted (gamma 0.45):
    red body lower edge at the tail   y = 583-590 (x 857-921)
    below it, x 900-960 / y 590-670   -> clean paving, no blade, no bracket, no shadow mass
ref_rear34, rear valance, gamma-lifted:
    the rear apron rolls under to a lip at y ~ 780-790 and meets ground shadow directly.
    The only metal below the number plate is a single small chrome fitting at (1127, 737)
    — a bumper-bracket stub or lid catch, ~14 x 24 px. No blade.
ref_workshop, near rear corner, x 905-975 / y 530-615 at 16x:
    a cream BUMPER BLADE END (rounded cap, x 926-949, y 570-596) PLUS a cream TUBULAR
    OVER-RIDER GUARD above it (x 936-947, y 551-574) wrapping the corner — the same
    blade+tube assembly that is clearly visible on the front bumper in the same photograph.
    Height above the local floor 0.31-0.61 m: correct T1 rear-bumper height.
```

So: **a cream rear bumper + guard was fitted at the conversion stage and had been removed by the
time the bus was in service.** It is not hidden behind the counter — the counter fascia bottom is
at 1.08 m and the bumper would sit at 0.35–0.48 m, in clear view in both in-service photographs.
The earlier report was right about `ref_workshop`; §1/§10.1 are right about the in-service state.

```
REAR OVERHANG (rear axle -> rearmost sheet metal) = 171.1 ± 3 px = 0.809 ± 0.02 m
factory equivalent                                                 ~0.81 m
factory rear axle -> rear bumper face                              ~1.02 m
```

The rear overhang is **factory**. There is no evidence of a shortened tail.

### V6. Front indicator — it is the **fish-eye**, not a bullet

`ref_workshop` (empty apertures), luminance profiles across each hole:

```
HEADLAMP aperture   horizontal (y=628)  x 381.5 -> 454.5 = 73.0 px
                    vertical   (x=419)  y 595.2 -> 665.5 = 70.3 px      centre (418, 630)
                    (the lower half of the hole is NOT dark — it is the lit inner face of the
                     nose panel; a naive dark-blob threshold under-measures it by half)
INDICATOR aperture  horizontal (y=564)  x 442.5 -> 476.0 = 33.5 px
                    vertical   (x=457)  y 549.7 -> 578.3 = 28.6 px      centre (459.5, 564)
                    round; a small bracket/stud protrudes at (472-477, 564-566)
INDICATOR / HEADLAMP APERTURE = 0.42 ± 0.03
  -> with a 7 in / 0.178 m headlamp aperture:  INDICATOR APERTURE = 74 ± 6 mm
offset from the headlamp centre: 66 px up = 0.163 m ; 41 px outboard = >=0.10 m (foreshortened)
```

`ref_side` (in service, front lamp seen in near-profile at 16x, x 72-112 / y 458-499):

```
a raised pointed pod, red/amber, standing clear of the nose:
    tip                (79.5, 478)
    base               (96.9, 470) to (94.4, 485)
    protrusion  16.5 px = 0.078 m       base diameter  15 px = 0.071 m
    length : base ratio = 1.05
```

The fitted lamp's base (0.071 m) equals the panel aperture (0.074 m) to within the error.
A 1955–Jul 1961 **bullet** has a ~45 mm base on a ~40 mm hole and a length:base ratio near 2;
this is 71 mm on a 74 mm hole at ratio 1.05 — the stubby, wide-based profile of the
**Aug 1961-on "fish-eye" / teardrop indicator, which is correct for a 1963 T1.**

**Caveat:** in pure side elevation a fish-eye reads as a raised conical pod, which is why it is
easy to call it a bullet. Model it as a wide-based teardrop: 74 mm round base, ~78 mm forward
protrusion, centred 0.163 m above and ≥0.10 m outboard of the headlamp centre.

### V7. VW nose roundel in the red livery — **RED**, resolved

`ref_source.jpeg` (246 x 197) is the only view of the nose in the red livery. Colour statistics,
R/G ratio (chrome and cream both read ~1.0; the body red reads 2.13):

```
ref_workshop  roundel bars (chrome)   rgb (111.4, 114.4, 110.6)   R/G = 0.974   <- neutral
ref_workshop  nose white              rgb (208.1, 208.0, 187.8)   R/G = 1.001
ref_source    roundel dark strokes    rgb (135.3,  85.0,  78.5)   R/G = 1.590   <- red
ref_source    roundel light areas     rgb (207.4, 175.2, 170.6)   R/G = 1.184
ref_source    nose cream (reference)  rgb (204.9, 195.7, 193.8)   R/G = 1.047
ref_source    body red  (reference)   rgb (129.3,  60.8,  51.6)   R/G = 2.125
```

The emblem sits on the cream upper nose, ~10-20 px clear of any red paint, yet its dark strokes
run 0.55 warmer in R/G than the cream immediately around them, and there is **no neutral or
blue-ish specular highlight anywhere in the emblem** — which a polished chrome roundel in that
sunlight would certainly show (compare the workshop's 0.974).

**RESOLVED: in the red livery the nose roundel is RED (ring and monogram both), not chrome.**
The chrome emblem of the workshop stage was over-painted or replaced. Confidence moderate-high;
the only reservation is the 246 px source and its JPEG chroma subsampling.

### V8. Corrections to earlier sections

1. **§0.2 / §8** — the disagreement between the two scales was **not** evidence of small tyres.
   It was the 15-inch assumption. Rim flange 0.440 m (16 in), tyre OD 0.665 m. Scale stands at
   211.5 px/m.
2. **§1 / §10.1** — 4.05 m is a correct measurement of a bus with no rear bumper; it is **not**
   a shortened body. Factory-configuration length 4.28 m. Add a rear bumper face at
   model X = -2.219 m if you model one.
3. **§0.3** — the ground line is **y = 670 ± 2**, not 668.0 (the tyre's loaded radius is 65-67 px
   and the earlier 668 was taken at the leading edge of the contact shadow). Every height in
   §1-§7 rises by ~10 mm.
4. **§2** — arch-to-tyre gap, rear, is **41 mm** not 71 mm (the tyre is bigger than §8 assumed).
   The "lowered" verdict survives, but only ~35 mm of the drop is attributable to the wheels.
5. **§6** — the counter overhangs the *factory bumper line* by 0.10 m, not 0.31 m.
6. **§9** — the indicator is resolvable after all: fish-eye, 74 mm round aperture.
