# REV 48 — THE REAR VENT PANEL, BOUNDED AND COUNTED

**Job 2, grounding pass. Measurement only. No project source was edited, no build was run,
Blender was never invoked.** Tools: python3 / numpy 1.26.4 / scipy 1.17.1 / PIL.

Everything below was watched print. Every window is stated. Scripts live in the session
scratchpad (`rev48*.py`); the three required crops are in `probe_scratch/`.

---

## 0. HEADLINE

| quantity | value | frame + window |
|---|---|---|
| **slat count** | **10** (not 6, not ~10) | `IMG_2073.jpeg`, rows 468–582, cols 1156–1188, de-sheared s = −0.180 |
| **pitch** | **8.106 ± 0.023 px** (regression); gap scatter 0.186 px = **2.3 %** | same |
| panel bounding box | x **1157 → 1186** (29 px), slat centres y **483.0 → 556.5** at x = 1170 | same |
| slats are | **horizontal on the vehicle**; the 10.2° image tilt is pure perspective | same |
| ledger's 8.02 ± 0.42 px | **CONFIRMED**, and tightened ~18× | — |
| slat **length** | **UNMEASURABLE to better than a factor of 2** — see §5 | — |

---

## 1. FRAME INVENTORY

Every image in the repo tree was opened. `REFERENCE_FRAMES_rev45.md` was read first; its
catalogue is correct and is extended here with the one column it did not have — *does this
frame show the rear vent panel, and at what size*.

| frame | native px | shows the rear vent panel? | vent panel size in that frame |
|---|---|---|---|
| **`IMG_2073.jpeg`** | 1400×933 | **YES — the only frame in which it is resolved.** 10 dark slat lines, high contrast (dip 48 grey levels on a 2.5-level noise floor, SNR ≈ 19) | **29 × 73.5 px**, pitch 8.11 px |
| **`ref_side.jpg`** | 1024×768 | **YES**, and nearly side-on (rear whitewall axis ratio 1.011) — **but the panel is in deep shade, L 30–60, and the slat dips are 2–5 grey levels against a 1.7–3.7-level noise floor (SNR ≈ 1.3).** At the detector's floor. | ≈ 70 × ≈ 48 px, apparent pitch ≈ 4.4 px, **count 10–12, not trustworthy** |
| **`ref_nolita_front34.jpg`** ( = `IMG_2060.jpeg`, md5-identical) | 700×467 | **YES, visible** — and here the louvres read as **bright highlight lines**, not dark ones (light from the other side). Confirms "pressed slot", not paint. | ≈ 14 × 17 px → implied pitch ≈ 1.7 px. **Far too small to count.** |
| `ref_workshop.jpg` | 1200×824 | **rear quarter clearly visible and SMOOTH — no louvres at all.** See §7c; this is a real discrepancy, not an occlusion | **NONE** |
| `ref_rear34.jpg` | 1200×824 | rear quarter visible below the service counter; high-pass over rows 460–590, cols 930–1090 shows no periodic texture | **NONE** |
| `ref_playa_34.png` ( = `IMG_3842.png`) | 500×400 | rear quarter visible but the fold-out shelf overhangs the panel; ~25 × 20 px of flank | not resolvable |
| `ref_nolita_front34b.jpg` ( = `IMG_2053.jpeg`) | 550×412 | rear quarter in frame, occluded by a person | not resolvable |
| `ref_nolita_flank.jpg` ( = `IMG_2054.jpeg`) | 450×450 | rear quarter behind the counter and a beer bottle | not resolvable |
| `ref_nolita_doorshut.jpg` ( = `IMG_3840.jpeg`) | 480×320 | rear quarter behind the folded-down counter | not resolvable |
| `ref_source.jpeg` | 246×197 | rear quarter ≈ 15 px wide | no |
| `ref_x6_lanczos.png` | 1476×1182 | **= `ref_source.jpeg` × 6 Lanczos** (246×6 = 1476, 197×6 = 1182). Interpolation, **no new information** | no |
| `bus_model_ref.JPG` | 2000×1125 | **YELLOW SCHOOL BUS — FIDELITY BAR ONLY.** Nothing about shape, paint or proportion taken from it. Its own louvres are modelled slots that self-shadow — that is the bar (see §7d) | n/a |
| `ref_grid.png`, `ref_band_grid.png`, `ref_nose_grid.png`, `ref_side_grid.png` | 1000–3700 px | derived grid overlays of frames already listed | no new content |
| `v6_front.png`, `v6_side.png`, `rev2*–rev4*_*.png`, `marks/*`, `probe_scratch/*` | various | renders and mark-ups, not photographs | n/a |

**Duplicates confirmed by size and content:** `IMG_2060`/`ref_nolita_front34`,
`IMG_3840`/`ref_nolita_doorshut`, `IMG_2054`/`ref_nolita_flank`, `IMG_2053`/`ref_nolita_front34b`,
`IMG_3842`/`ref_playa_34` — consistent with `REFERENCE_FRAMES_rev45.md` §2.

**Rule 13 satisfied: three frames I already hold show the panel. Only one of them can be measured.**

---

## 2. PANEL BOUNDS — bounded by structure, not by a typed box

Frame `IMG_2073.jpeg` (1400×933). All coordinates native px.

### 2.0 First: the slats' image tilt, because every window below depends on it

Window x 1156–1188, y 480–556. The de-sheared row profile's high-pass contrast was maximised
over shear s:

```
best s = -0.180   contrast 15.61
within 2% of best: s in [-0.210, -0.150]   ->   s = -0.180 +- 0.030
image tilt = 10.2 +- 1.7 deg, up to the right
```

The belt-line paint edge over the same x range has slope **−0.0683**. Two lines with different
image slopes that are parallel on the vehicle must meet at the flank's vanishing point:
they meet at **(1692, 426)** — 487 px beyond the rear corner, off-frame right, at a plausible
horizon height. **So the slats are horizontal on the vehicle**, and the 10.2° is perspective.
(Any two lines meet somewhere; what makes this evidence is that the meeting point is off-frame
in the direction the body recedes and at a horizon height consistent with the camera.)

### 2.1 TOP BOUND — the belt swage (white/green paint edge)

Sub-pixel crossing of the green/white boundary, x 1156→1204 step 2:

```
y_belt(x) = -0.0683 x + 553.78      ->   y_belt(1170) = 473.85
```

The first slat's centre is at **483.00**, i.e. **9.15 px = 1.13 pitch below the swage**.

**A candidate at y ≈ 475.0 was REJECTED, by two tests either of which could have failed:**

1. **No raw local minimum.** The 9-px high-pass reports a minimum of −16.05 there, but the raw
   de-sheared profile falls *monotonically* from L = 214.7 (y = 468) to L = 103.7 (y = 479) —
   it is the white-paint edge's ramp, not a dip. Every real slat is a genuine local minimum in
   the raw profile (checked: all 10).
2. **It runs on past the array.** Measuring dip depth along that line as a function of x:
   `x=1130: 18, 1135: 14, 1140: 29` — it is still there 27 px left of the array's left end.
   Every real slat's dip is **0** by x = 1152.

### 2.2 BOTTOM BOUND — the last slat, with a null test that had power

Last slat centre **y = 556.5**. Below it the panel is overpainted with folk-art flowers.
**Paint does not hide a slat shadow** — proven on the spot: slat 10 crosses the white/blue
painted flower and is the deepest feature in the whole profile.

| position | cols 1158–1172 (over the white flower) | verdict |
|---|---|---|
| slat 10, y = 556.5 | hp = **−62.5**, local contrast **83.6** grey levels | present |
| predicted slat 11, y = 564.6 | hp = **−4.1**, local contrast **4.7** grey levels | **absent** |
| predicted slat 12, y = 572.7 | hp = −5.4, contrast 9.4 (a flower edge) | absent |

The detector's own floor (§3, control sweep) is a dip depth of ≈ 12 grey levels: it recovers
10/10 at 12.0 and **refuses (reports 0)** at 7.2. 4.7 is far below that floor.
**There is no 11th slat. The array ends at 556.5.**

### 2.3 RIGHT BOUND — the onset of the rear corner radius

Averaging the nine "land" rows (the bright metal between slats) and scanning across x:

```
x 1157..1183   L flat at 98-102      (a flat panel, evenly lit)
x 1184         dL/dx = +6.8/px       <-- the slats stop here
x 1186..1190   L peaks at 126        (the rear-corner highlight)
x 1191..1202   L falls to 75         (the corner turning away)
x 1202..1208   the silhouette
```

Slat half-max right ends: **1184.4 ± 0.7**. Periodic-energy half-max band: **x 1158 … 1187**.
**Adopted right bound 1185.5 ± 1.5.** The array stops exactly where the corner radius begins —
that is the structural feature bounding this side.

Rear body silhouette, measured (last green column per row, rows 480–525):
`x_rear(y) = 0.1309 y + 1139.4` → 1202.6 at y = 483, **1207.5 at y = 520**.

### 2.4 LEFT BOUND — the end of the pressing; no seam is measurable

Slat half-max left ends: **1157.0 ± 1.8** (flower-free slats only: 1157.7–1158.3).
Periodic-energy half-max: 1158. **Adopted 1157.0 ± 1.8.**

**Whether a body seam or swage sits there is UNMEASURABLE**: a painted white flower covers
x 1140–1156 across rows 476–510, and yellow flowers cover the lower left from row 537. The
land-row column profile through that band peaks at L = 152 (paint), so no crease can be read.
The bound quoted is the end of the slat pressing, nothing more.

### 2.5 THE BOX

A parallelogram, because the slats are sheared −0.180 px/px in image space:

```
   corner (slat-centre)      x        y
   top-left               1157.0    485.3
   top-right              1186.0    480.1
   bottom-right           1186.0    553.6
   bottom-left            1157.0    558.8

   width  (along x)        29 px
   height (along y at constant x)   73.50 px   = 9 x pitch exactly
```

**Marked crop: `probe_scratch/rev48_vent_bound.png`** (10× nearest-neighbour, native window
x 1132–1212, y 462–586; belt line, silhouette, box, all ten slats and both rejected candidates
drawn).

**This is why rev 47's 6-in-a-50-px-crop was low.** A 50-px window at this pitch holds 6.2
slats. The panel is **73.5 px** tall. The window *was* the answer.

---

## 3. SLAT COUNT — 10, by three methods, with a control that can fail

### 3.1 The detector (frozen before the controls were run)

On a de-sheared, column-averaged profile sampled at 0.25 px:

1. `hp = p − uniform_filter(p, 8.25 px)`
2. `find_peaks(−hp, prominence ≥ 6, min separation 4 px)`
3. reject unless `hp ≤ −5` (a real darkening, not merely a relative one)
4. reject unless a **raw local minimum** of the lightly smoothed profile lies within ±1.5 px

Rules 3 and 4 exist because of the y = 475 belt-edge artefact. They are what a blank panel with
a step edge has to get past.

### 3.2 Method-by-method

| method | window | result |
|---|---|---|
| **row-profile minima**, prominence swept 3, 4, 6, 8, 10, 14 | rows 468–582, cols 1156–1188 | **10 at every threshold** — 483.00, 491.75, 499.75, 507.75, 515.75, 524.00, 532.00, 540.00, 548.00, 556.50 |
| **autocorrelation** of the high-passed profile | rows 480–558 | first four peaks at lag **8.00, 16.25, 24.25, 32.25 px** (r = 0.86, 0.76, 0.67, 0.57) |
| **FFT** of the same, parabolic-refined | 78.2 px span | peak period **8.002 px** |
| **2-D ridge count** per row (independent of the 1-D profile) | rows 470–585, cols 1150–1195 | ridge rows at 483, 492, 500, 508, 516, 524, 532, 540, 548, ~556 |

**Cross-check demanded by the brief:** panel height / pitch must equal count − 1.
`73.50 / 8.106 = 9.07` → **count 10.07**, against a direct count of **10**. Agreement to 0.07.
The two agree; there is nothing to arbitrate.

**Reported as a range with its pitch: 10 slats at 8.106 ± 0.023 px.
Given the null test in §2.2 the range is 10–10; the only frame that hints at more
(`ref_side.jpg`, 10–12) is at SNR 1.3 and is not admissible for a count.**

### 3.3 THE CONTROL — `probe_scratch/rev48_vent_control.png`

Rule 22: every control panel is **33 × 120 px — the real panel's own size** — and carries the
real panel's own measured parameters: slat depth **47.9** grey levels and FWHM **2.75 px**
(both from folding the real profile at the measured pitch), shear **−0.180**, pixel noise
**sd 2.5** (measured on flat green tiles at the panel's own luminance: 1.0–2.7 over 375 tiles),
and **JPEG quality 72**. The **same frozen detector** ran on all of them.

| control | truth | recovered | recovered pitch | |
|---|---|---|---|---|
| C1 10 slats @ 8.106 px | 10 | **10** | 8.111 | PASS |
| C2 7 slats @ 8.106 px | 7 | **7** | 8.125 | PASS |
| C3 14 slats @ 5.600 px | 14 | **14** | 5.607 | PASS |
| C4 10 slats, half contrast | 10 | **10** | 8.095 | PASS |
| C5 10 slats, quarter contrast | 10 | **10** | 8.065 | PASS |
| **C6 BLANK, no slats** | **0** | **0** | — | **PASS** |
| **C7 BLANK, 2× noise** | **0** | **0** | — | **PASS** |
| **C8 BLANK, 4× noise** | **0** | **0** | — | **PASS** |
| **C9 BLANK + vertical gradient** | **0** | **0** | — | **PASS** |
| **C10 BLANK + belt-like step edge** | **0** | **0** | — | **PASS** |

C10 is the one that matters most: it is the y = 475 artefact rebuilt on purpose, and the
detector refuses it.

**The controls could and did fail while I was building them.** An earlier version of the
raw-minimum gate rejected the real slat at y = 483 (its raw minimum is at 483.25, 0.25 px away)
and an earlier synthetic had the shear sign inverted, which made C1 return 4 of 10. Both were
found *by the control*, not by inspection of the real data.

### 3.4 THE CEILING (rule: report the ceiling)

```
contrast sweep, 10 slats, 5 seeds each
   x0.50 (depth 23.9)  -> 10,10,10,10,10
   x0.25 (depth 12.0)  -> 10,10,10,10,10
   x0.15 (depth  7.2)  ->  0, 0, 0, 0, 0     <- refuses rather than inventing
   x0.10 and below     ->  0, 0, 0, 0, 0

noise sweep, 5 seeds each
   noise x1 (sd  2.5)  BLANK 0,0,0,0,0     10-SLAT 10,10,10,10,10
   noise x2 (sd  5.0)  BLANK 0,0,0,0,0     10-SLAT 10,10,10,10,10
   noise x4 (sd 10.0)  BLANK 0,0,0,0,0     10-SLAT 10,10,10,10,10
   noise x6 (sd 15.0)  BLANK 1,1,1,1,1     10-SLAT 11,10,10,10,11   <- first hallucination
   noise x8 (sd 20.0)  BLANK 7,4,5,6,4     10-SLAT 13,11,10,10,12   <- blind
```

**The real panel sits at contrast 1.0× and noise 1×: a 4× contrast margin and a 6× noise
margin from the nearest failure.** `ref_side.jpg`'s panel, by contrast, sits at roughly
contrast 0.1× — inside the region where this detector is required to refuse.

---

## 4. PITCH — mine vs the ledger's

| source | value | scatter | window |
|---|---|---|---|
| `LEDGER_rev47.md` §10c | **8.02 ± 0.42 px** | 5 % | not stated |
| **this pass, regression over 10 slats** | **8.106 ± 0.023 px** | residual sd 0.208 px | `IMG_2073`, rows 468–582, cols 1156–1188, s = −0.180 |
| this pass, mean of the 9 gaps | 8.094 ± 0.066 (sem) | gap sd 0.186 px = **2.3 %** | same |
| this pass, FFT | 8.002 px | — | rows 480–558 |
| this pass, autocorrelation lag 1 | 8.00 px | — | rows 480–558 |

The individual gaps: `8.75, 8.00, 8.00, 8.00, 8.25, 8.00, 8.00, 8.00, 8.50`.

**VERDICT: CONFIRMED, not refuted.** 8.106 lies well inside 8.02 ± 0.42. The ledger figure was
right; this pass tightens the uncertainty by ~18× and refines the regularity from "5 % scatter"
to **2.3 %**. The pitch is now the best-determined number on this panel.

Note the ledger's 8.02 is reproduced *exactly* by the naive span/pitch on the nine slats below
483 (64.75 / 8.075) — rev 47's window very likely started at the second slat.

---

## 5. THE OTHER DIMENSIONS

### 5.1 Slat line thickness — MEASURED (vertical, so not foreshortened)

FWHM of the dip in y, cols 1163–1181, per slat: 2.90, 2.55, 2.30, 2.25, 2.35, 2.40, 2.45, 2.45,
3.55, 3.15 px.

> **FWHM = 2.63 ± 0.43 px = 0.325 ± 0.053 of the pitch.**

**Caveat that is part of the measurement:** this is the width of the **shadow**, not of the
slot's mouth. They are the same number only if the slot is an unlouvred gap. At a 1.55-px
optical blur radius the two cannot be separated here.

### 5.2 Slat length — **UNMEASURABLE to better than a factor of 2**

Raw, in `IMG_2073`: half-max ends of the flower-free slats give **left 1157.0 ± 1.8,
right 1184.4 ± 0.7, length 27.4 ± 2.2 px**; the periodic-energy half-max band gives a
width of **29 ± 2 px**.

That is a **horizontal** measurement on a flank seen at grazing incidence, so it must be
de-foreshortened. The flank's compression was measured, not assumed, from a circle in the
flank plane — the rear wheel's white sidewall:

```
IMG_2073 rear whitewall   41 x 89  px  ->  w/h = 0.461   (window x1108-1162 y638-736, thr 150)
IMG_2073 front whitewall 103 x 133 px  ->  w/h = 0.774   (window x690-800  y715-880, thr 170)
        the front figure is APPROXIMATE - the blob is clipped by the fender and the crop
   -> compression ~ (x_vp - x)^2 through those two fits x_vp = 2440; at the panel (x=1170) c = 0.437
ref_side rear whitewall   92 x 91 px   ->  w/h = 1.011      (that frame is side-on)
```

De-foreshortened, `IMG_2073` gives **slat length ≈ 63 ± 8 px = 7.7 ± 1.0 pitch**, and an array
aspect (width/height) of **0.90 ± 0.13**.

**But `ref_side.jpg` refuses to agree, and it is the frame that needs no correction.**
The two frames image the rear wheel at the **same vertical scale** (whitewall height 90 vs 91 px
— a 1 % match), so the arrays should be directly comparable, and they are not:

| | `IMG_2073` (de-foreshortened) | `ref_side` (side-on, no correction) |
|---|---|---|
| array width | 66 ± 8 px = 8.2 pitch | ≈ 70 px = 15.9 pitch |
| array height | 73.5 px = 9.07 pitch | ≈ 48 px = 10.9 pitch |
| pitch | 8.106 px | ≈ 4.4 px |
| aspect w/h | 0.90 | ≈ 1.46 |

**A factor of 1.9 in width and 1.8 in pitch, at the same image scale.** They are different
vehicles — `ref_side.jpg` is the **red** Tacombi, `IMG_2073` the **green** one — so they may
simply be different vents; or `ref_side`'s reading (SNR 1.3, at the detector's refusal floor)
may be wrong. **I cannot tell which, and I will not pick.**

> **SLAT LENGTH: UNMEASURABLE.** The only length figure that survives, because the foreshortening
> cancels between numerator and denominator (both horizontal, same rows, same depth):
>
> **slat length / (slat right end → rear silhouette) = 27.4 / 22.0 = 1.25 ± 0.13**
>
> and, as a fraction of panel width, the slats *are* the panel width — 1.00 by construction;
> the array's half-max width and the slats' half-max length agree to 1.6 px.

### 5.3 Panel position — dimensionless ratios (rule 14)

Two denominators are offered. Both are **vertical**, so neither is affected by the obliquity
that wrecks §5.2. The second is the better one for transfer because it is measured at almost
the same station as the panel.

Landmarks, all measured in `IMG_2073`:

```
belt swage (white/green paint edge)   y = -0.0683 x + 553.78    -> 473.85 at x=1170, 476.12 at x=1137
slat 1 centre                          483.00        slat 10 centre  556.50
rear wheel-arch apex                   (1137, 631 +- 5)
rear whitewall height  H_ww            90 +- 2 px
belt -> arch apex  (at x=1137)         154.9 +- 5 px  = 1.721 H_ww
rear silhouette                        x = 0.1309 y + 1139.4
```

| ratio | value |
|---|---|
| pitch / (belt → wheel-arch apex) | **0.0523 ± 0.0018** |
| (belt → slat 1) / (belt → arch apex) | **0.0591 ± 0.0030** |
| (belt → slat 10) / (belt → arch apex) | **0.534 ± 0.018** |
| array height / (belt → arch apex) | **0.475 ± 0.017** |
| pitch / H_ww (rear whitewall height) | **0.0901 ± 0.0020** |
| array height / H_ww | **0.817 ± 0.020** |
| (belt → slat 1) / H_ww | **0.102 ± 0.006** |
| (belt → slat 1) / pitch | **1.13 ± 0.05** |
| slat-line FWHM / pitch | **0.325 ± 0.053** |
| array height / pitch | **9.07** (= count − 1, exactly) |
| (right end → rear silhouette) / slat length | **0.80 ± 0.08** *(horizontal/horizontal — foreshortening cancels)* |

**Wheelbase-fraction: declined.** In this frame the front and rear wheels sit at very different
depths (front whitewall 133 px tall, rear 89 px — a depth ratio of 1.49), so an image wheelbase
is not a transferable scale. Any wheelbase ratio quoted from `IMG_2073` would be a number with a
1.5× systematic hidden inside it.

### 5.4 Horizontal or angled — MEASURED

**Horizontal on the vehicle.** Image shear −0.180 ± 0.030 px/px (10.2° ± 1.7° up to the right);
the belt swage over the same columns has slope −0.0683; the two lines meet at **(1692, 426)**,
off-frame beyond the rear corner at a plausible horizon height. Two lines that are horizontal on
a flat flank must share that point, and these do.

### 5.5 How many panels — ONE seen; a pair is UNMEASURABLE

* **On the flank in view: exactly one.** A 2× vertical high-pass of the *entire* green flank
  (x 560–1215, y 460–670) was made and looked at. The array at x 1157–1186 is the only stack of
  regular parallel dark lines anywhere on it; every other structure is folk art, the "Señor
  Tacombi" script, "BREAKFAST SPECIAL", or the door handle.
* **On the opposite flank: UNMEASURABLE.** **Every photograph in the repository has the bus's
  nose to the image left**, so every one of them shows the *same* flank. The opposite rear
  quarter is never seen. (Which physical side that is, I could not settle: the camera-handedness
  rule — nose to image-left ⇒ the vehicle's left side — says left, but the serving hatch is on
  the same flank and a kerbside serving hatch argues right. The ambiguity does not affect any
  number above, and I am not going to resolve it by assertion.)

---

## 6. WHAT I SAW — from looking at the crops, not at the numbers

**`probe_scratch/rev48_vent_raw.png`** — the panel at 8×, native window x 1145–1200, y 466–572,
unmarked. A white belt band across the top, then green, then a ladder of ten dark-green bars
sloping gently up to the right, evenly spaced, all ending at the same two vertical lines. They
are **not black**: they are a darker shade of the *same* green as the panel, which is what
LEDGER rev 47 §10c corrected and what the raw luminance confirms — the lands sit at L ≈ 101–112
and the darkest slat floor at L ≈ 45, both on green paint, with no grey or black anywhere. Each
bar is soft-edged (about two and a half pixels across) and slightly darker at its middle than at
its ends — a self-shadowing groove, not a painted stripe. A painted white flower sits over the
top-left corner of the array; yellow and white flowers cover the bottom left and bottom right.
The bars stop cleanly against a slightly brighter strip of green on the right — the corner.

**`probe_scratch/rev48_vent_bound.png`** — the same at 10× with the box, the belt line, the
silhouette, the ten detections and the two rejects drawn. The thing to look at is where the
green lines fall: **on the bars, all ten of them, without a single miss and without a spare line
in a gap.** The blue belt line lies exactly on the white/green paint edge and the top bar is
plainly *below* it with a clear band of untouched green between — you can see with your eye that
the belt edge is not one of the slats. At the bottom, the last green line lands on the last bar,
and below it the red dashed reject line crosses plain flower paint with nothing under it. The
yellow box's right edge sits where the bars stop and the corner highlight starts; its left edge
sits where they stop and a painted flower starts, which is exactly why §2.4 says the left bound
is not structural.

**`probe_scratch/rev48_vent_control.png`** — the real panel at the far left, then seven
synthetics at the *same* 33 × 120 px. Looked at side by side, the synthetics are visibly
*fainter* than the real thing — the modelled depth (47.9) is the column-averaged depth, and the
real panel's individual columns dip deeper — so the control is harder than reality, which is the
right direction for the argument. C3 (14 slats at 5.6 px) is obviously a finer ladder than C1
and the detector says so. The three blanks are, to the eye, plain grey rectangles: C6 flat, C8
visibly grainy, C10 with a white band across the top like the belt. **The detector reports zero
on all three.** That is the picture that entitles the count in §3 to be published.

---

## 7. WHAT IS STILL UNMEASURABLE, AND WHAT WOULD SETTLE IT

### 7a. The slat length / the array's true proportion — **the top gap**
Two admissible frames disagree by 2.1× (§5.2) and the frame that needs no de-foreshortening is
the one at SNR 1.3. **Wanted: the rear quarter panel photographed square on** — camera normal to
the flank, the whole panel in frame with the belt swage above it and the wheel arch below,
filling ≥ 400 px vertically. That single frame settles length, aspect, count and pitch at once
and retires this whole section.

### 7b. The slot's section and depth
The dark line's FWHM is 2.63 px, but whether that is a slot mouth, a louvre lip's shadow, or
both, cannot be separated at a 1.55-px blur radius. **Wanted: a close raking-light shot**
(sun or lamp low and along the flank) of six or so slats filling the frame — the shadow length
against the known pitch then gives the pressing depth directly.

### 7c. `ref_workshop.jpg` has no louvres, and I cannot explain it
The rear quarter in `ref_workshop.jpg` is unobstructed below the counter shelf, is at a *larger*
vertical scale than `IMG_2073`'s (a 10-slat array there would be ≈ 96 px tall at a ≈ 10.6 px
pitch — unmissable), and is **plain smooth green**, confirmed both by eye at 6× and by a
high-pass map. Either that vehicle is a different unit, or the panel was replaced during the
conversion, or the louvres postdate the shot. **Recorded, not resolved.** **Wanted: the owner's
word on whether the workshop bus and the `IMG_2073` bus are the same vehicle.**

### 7d. Whether the opposite flank carries a matching array
Never photographed (§5.5). **Wanted: one frame from the other side.** Until then the model
should not assume a mirrored pair without saying so in the source.

### 7e. Whether a body seam bounds the array on the left
Covered by paint in every available row (§2.4). Settled by the same square-on frame as 7a.

---

## 8. FILES WRITTEN

```
probe_scratch/rev48_vent_raw.png       the panel, 8x nearest-neighbour, unmarked
probe_scratch/rev48_vent_bound.png     bounding box + belt + silhouette + 10 slats + 2 rejects, 10x
probe_scratch/rev48_vent_control.png   real panel beside 7 synthetic controls and what the detector said
probe_scratch/REPORT_rev48_vents.md    this file
```

**No project source was edited. No build was run. Blender was not invoked.**
