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
two-tone V apex (centreline)    (311.5, 669)   ± 4 px   -> 104 px below the emblem centre,
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
