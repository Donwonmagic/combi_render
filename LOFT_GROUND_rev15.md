# LOFT_GROUND_rev15 — measurements to ground the joint re-loft

**Status: MEASURE-ONLY.** No repo file was edited. This document is the only file created
in the repo. Build state reproduced first, unchanged:

```
T1_SUB=1 T1_VERIFY=1 blender -b --python build.py
  dims  L=4.298 W=1.750 roof@rear-axle=1.894 (raw resid -66 mm; dome deficit +98 mm still unmodelled)
  roof at tail = 1.903
  VERIFY: 0 fail, 1 warn
    warn  roof crown @ rear axle (dome-corrected) 1.992 vs spec 1.960 (+32 mm)
```

Every number below carries its method, its crop box, its uncertainty, and whether it is
INDEPENDENT or shares a chain with the others. Read §0 first: it is the calibration that
three of the four parts hang from, and it refutes an inherited claim.

---

## 0. THE FLANK CAMERA MODEL — established, cross-checked three ways, and it refutes REF §0.2

### 0.1 What was measured

| quantity | value | method | crop box | rms |
|---|---|---|---|---|
| rear hub centre | **u 749.38, v 604.38** | sub-pixel chord-midpoint + chord-width circle fit on the white rim-flange OD | cols[695,805) rows[588,650) | 0.14 px |
| rear rim flange OD | **92.50 px** | same fit, ×2 | same | 0.14 px |
| front hub centre | **u 242.84, v 607.0 ± 2** | identical method, only the two unoccluded arcs | cols[190,300) rows[595,650) | 2.40 px |
| front rim flange OD | **88.56 px** | same | same | 2.40 px |

The two rims are the **same physical object at two depths**, so their ratio is a pure
transverse-scale ratio, free of any metre calibration:

**ρ = k_t(rear)/k_t(front) = 46.251/44.282 = 1.0445 ± 0.020**

(the ±0.020 is the front fit's radius uncertainty; the rear contributes nothing.)

### 0.2 The 1-D projective rectification

Along the flank, with c(s) = 1/k_t(s) linear in arc length and X(s) = (u−u₀)·c(s) linear
in s, three constraints fix the map exactly: u(front hub), u(rear hub), and ρ. It is
**invariant to the principal point** — verified numerically over u₀ ∈ [412, 612], the
answers move by 0.0 mm. Implied vanishing point:

**u_vp = −11 140** (i.e. the flank IS convergent).

### 0.3 Three independent confirmations, and one refutation

| prediction of the map | this work | inherited value | verdict |
|---|---|---|---|
| local longitudinal px/m at mid-body (u≈500) | **211.2** | "~211 mid-body" (RULES §4 / brief) | ✔ |
| local longitudinal px/m at the tail panel (u≈921) | **226.9 ± 8** | "225 ± 3" (brief; refutes RULES §4's 194.8 in sign) | ✔ |
| vanishing point | **u_vp = −11 140** | rev 13: u ≈ −11 700 | ✔ (5 %) |
| vanishing point | **u_vp = −11 140** | **REF §0.2: x ≈ −98 000, "parallel, not convergent"** | **REFUTED** |

> **REFUTED: `REF_MEASUREMENTS` §0.2's finding that the flank shows no measurable
> perspective convergence.** It was obtained by intersecting two body lines whose slopes
> (−0.0385, −0.0367) differ by less than their own noise. The rim-radius route is direct
> and gives a VP eight times nearer. Consequence: **REF's single S = 211.2 px/m is wrong
> by −4 % at the tail and +4 % at the nose**, and every inherited longitudinal metre value
> taken at the extremities inherits that.

### 0.4 The absolute vertical scale at the rear wheel

The transverse (vertical) scale follows from the longitudinal one and the VP without
needing the focal length:

  k_t(u) = k_long(u) / [1 + (u−u₀)/|u_vp−u₀|]  →  k_t(749.38) = 220.5/1.0204 = 216.1

Cross-check, fully independent of the above: the arch-to-tyre gap at the crown is
80.29 px minus the locked tyre radius in px; forcing that to SPEC §10.29's independently
re-measured **41.0 ± 3.5 mm** gives k_t = 214.9 ± 2.0.

**k_t(rear hub) = 215.5 ± 3.0 px/m** (adopted throughout).

Two further corroborations fall out at once:
* rear arch lip above the hub at the crown = 80.29 px = **0.3726 ± 0.0052 m** against the
  built `ARCH_R = 0.3735`. **The built arch RADIUS at the crown is right to 1 mm** — only
  its width is wrong (§2).
* the ground line under the rear wheel is at **v = 676.0 ± 0.6** (hub v 604.38 plus
  0.3325 × 215.5). REF §0.3 put it at 670 ± 2; SPEC §10.11 inferred ≈ 683 from three
  features landing low. **Both were partly right and §10.11's open question closes: the
  datum is ~6 px low AND the scale is ~2 % low, and the two errors partly cancel.**
  This does not license using the ground line — the cancellation is station-dependent.

**CHAIN NOTE.** §2 (arch width), §3 (tail) and §4 (roof heights) all use this calibration.
They are NOT mutually independent. §2's exponent/flatness, §2's crown-centring, and §5
(the poles) do not use it and ARE independent.

---

## 1. PART A — ROOF CROWN + RAKE, JOINTLY

### 1.1 The one frame everyone has been using for the dome cannot deliver it — proof

`ref_side.jpg`'s roof band is not merely short; the two features being differenced are at
**different depths**. The drip rail is at y ≈ +0.816 m (near flank); the crown is at
y ≈ 0. At Z ≈ 4.9 m that is a **14–20 % scale difference between the two ends of the
measurement**, and correcting it needs the camera height H.

`ref_side.jpg` does not determine H. The two hub rows would fix the horizon — both hubs
sit at exactly one tyre radius above flat ground by construction — but they put it at
**v ≈ 725, below the hubs themselves**, which is physically impossible for a camera that
is plainly looking down on the counter. (Either the street cambers ~20 mm across the
wheelbase, or the front hub row is wrong by 4 px; `ref_side.jpg` cannot separate them.)

> **REFUTED as a method, not merely as a number: SPEC §10.29's "crown-minus-drip-rail at
> the same column in `ref_side.jpg` gives 0.188 ± 0.015 m".** The quantity it measures is
> a difference of two heights read at two depths with one scale. The stated ±0.015 does
> not contain the 14–20 % depth systematic, and the systematic's sign cannot be pinned
> without H. **Do not re-use that route.**

The `ref_workshop.jpg` lid route has a different, equally unstated problem. The lid's
forward cut edge is a plane arc, but the lid is **raised**, so its plane is tilted by the
opening angle. Under projection the chord is preserved and the sagitta foreshortens by
cos θ, so **R scales as 1/cos θ**. At a plausible 50–60° of lid opening that is a factor
of **1.4–2.0**, not ±6 %. I also could not re-trace that edge: the red studs, the vertical
support pole crossing it at u ≈ 440, and the workshop lights behind it defeated a
sub-pixel scan (line rms 17 px, circle rms 15 px — no usable fit).

> **The quoted "R = 2.45 ± 0.15 m" therefore has no admissible provenance in front of me.**
> Its ±0.15 is not credible from either of its two stated routes.

### 1.2 What IS measurable: the roof line at the rear axle, hub-referenced

At the rear-axle column the hub is the datum, so no horizon and no ground line is needed:
a vertical pixel difference at one column divides straight by k_t.

| feature | v | crop box | height above ground |
|---|---|---|---|
| drip-rail groove (gutter) | **299.24 ± 0.6** | cols[700,900) rows[288,306), parabolic minimum, line fit over 85–135 columns, **rms 0.06–0.12 px** | **1.7485 ± 0.020 m** |
| roof silhouette, fixed skin | **257.2 ± 1.5** | cols[766,816) rows[242,272), half-max rising edge | **1.9435 ± 0.024 m** |
| roof silhouette incl. a proud strip over u 750–816 | 253.21 ± 1.2 | same | 1.9621 ± 0.023 m |

The proud strip is 4.0 ± 1.5 px ≈ **19 ± 7 mm** above the skin either side of it and is
almost certainly the roof-opening coaming (it is inside REF §1's "unobstructed" window
770–820, and matches SPEC §10.9's independently measured "26 ± 7 mm proud").

**INDEPENDENT CONFIRMATION OF 1.960 WITHOUT THE GROUND LINE.** The silhouette-including-
strip height is **1.962 ± 0.023 m** against REF §1's ground-line-derived **1.960 ± 0.03**.
Agreement to 2 mm by a route that shares nothing with it. **1.960 survives**, which is
worth saying explicitly because REF §1 derived it from `ground = 668.0`, exactly the datum
SPEC §10.11 banned.

**NEW, AND IT REVERSES THE SIGN OF HALF THE PROBLEM.** The built gutter at the rear axle
is 1.8116 m AG (`ZT_ALL(−1.100) = 1.894`, minus `RT_ALL = 0.054`, minus
`rake_drop(−1.100) = 0.0284`). Measured: **1.7485 ± 0.020**.

> **The model's roof EDGE is 63 ± 20 mm TOO HIGH at the rear axle**, at the same time as
> its CROWN is 66 mm too low. Nobody has measured the edge before; the whole −66 mm has
> been attributed to the missing dome. It is not. It is **+63 mm of roof line and
> +130 mm of missing dome, partly cancelling.**

### 1.3 THE CLOSURE TEST — the system is over-determined and DOES NOT CLOSE at R = 2.45 m

All at the rear-axle station, all as heights above ground:

```
  gutter (measured, hub-referenced)                    1.7485 ± 0.020
  roof silhouette, fixed skin (measured)               1.9435 ± 0.024   -> crown >= this
  crown target (REF §1, and confirmed in 1.2)          1.960  ± 0.030
  dome, as built  (RT_ALL 0.054 + CR_ALL 0.032)        0.0860           -> R = 9.06 m
```

With the model's own section parametrisation (crown parabola of half-width
Yt = 0.7615 m, so crown parameter = Yt²/2R, and gutter-to-crown D = RT_ALL + crown param):

(the "crown AG" column is **measured gutter 1.7485 + D**, i.e. what the crown would be if
the roof line were corrected to the photograph and only the dome varied. It is therefore
not the same as the current build's 1.894, which sits on a roof line 63 mm too high.)

| assumed R | crown parameter | D | crown AG | vs 1.960 |
|---|---|---|---|---|
| 9.06 (as built) | 0.0320 | 0.0860 | 1.8345 | −126 mm |
| **2.45** (backlog target) | 0.1183 | 0.1723 | **1.9208** | **−39 mm** |
| 2.30 | 0.1261 | 0.1801 | 1.9285 | −31 mm |
| 2.00 | 0.1450 | 0.1990 | 1.9474 | −13 mm |
| **1.84** | 0.1576 | 0.2116 | **1.9600** | **0** |
| 1.60 | 0.1812 | 0.2352 | 1.9837 | +24 mm |

**Two independent constraints both reject 2.45 m in the same direction:**

1. **Crown ≥ silhouette.** The measured fixed-skin silhouette is 1.9435 ± 0.024. R = 2.45
   predicts a crown of 1.9208 — **below the measured silhouette**, which is impossible.
   R must be **≤ 2.06 m** for the crown to clear its own silhouette (≤ 1.82 m if the
   proud strip is roof skin after all).
2. **Crown = 1.960.** Requires D = 0.2115 → **R = 1.84 m**.

> **ANSWER TO THE BRIEF'S QUESTION: NO. crown = 1.960, rake = 17.75 mm/m and
> R = 2.45 ± 0.15 m are NOT mutually satisfiable.** With the gutter measured at
> 1.7485 ± 0.020, R = 2.45 lands the crown 39 ± 30 mm short of 1.960 *and* 23 ± 30 mm
> below the roof's own photographed silhouette. The over-determination resolves only if R
> comes down.

**THE JOINT SOLUTION I would re-loft to** (drives `DOME_DEFICIT` to zero by construction):

```
  transverse crown radius        R      = 1.84  ± 0.30 m     (NOT 2.45 ± 0.15)
  crown parameter  CR_ALL(roof)         = 0.1576 (was 0.0320)
  gutter-to-crown  D                    = 0.2116 (was 0.0860)   deficit +126 mm, not +98
  roof line        ZT_ALL(-1.100)       = 1.8309 authored (was 1.8940)   -63 mm
  rake             RAKE_DZDX            = 0.017750  UNCHANGED
  => crown @ rear axle                  = 1.9600 m AG    residual 0 mm
```

**The rake never entered this station's closure** — the guarded quantity is at the rear
axle, and I measured the real roof line at the rear axle. So the coupling the brief warns
about ("the rake and the roof dome pull the same way") is real *for the rest of the roof*
but is **not** what is breaking the rear-axle guard. What is breaking it is a roof line
that has never been measured at all.

### 1.4 What I could NOT measure, honestly

* **A transverse crown radius from any frame, directly.** `ref_side.jpg` is disqualified
  by §1.1. `ref_workshop.jpg`'s lid carries an unrecoverable tilt factor of 1.4–2.0 and I
  could not even trace its edge. `ref_rear34.jpg` shows the roof from above with real
  elevation — but between the near drip rail and the roof opening there are only ~13 px of
  roof skin at u ≈ 720, and aft of the opening the surface is a specular highlight with no
  traceable far edge. **The R = 1.84 ± 0.30 m above is INFERRED from two heights at one
  station plus the model's own section parametrisation, not measured as a curvature.**
  It is only as good as the assumption that the roof section is a single parabola of
  half-width 0.7615 m. If the real section is flatter in the middle and tighter at the
  shoulder — which a T1 roof is — the *central* radius will be larger than 1.84 and the
  shoulder tighter, at the same total D. **D = 0.2116 ± 0.035 m is the robust number;
  R = 1.84 is a re-expression of it, not a second finding.**
* **A second roof-line station.** The front roof is visible only over u 150–310; the
  front hub row is uncertain by ±3 px (±14 mm) and the horizon is not recoverable, so a
  two-station roof line would carry ±20 mm of pure datum error on a quantity of interest
  of 40 mm. Not attempted. **The rake is not re-derived here and nothing here disagrees
  with 17.75 mm/m.**
* I explicitly did **not** convert any body-line image slope into a rake. For the record,
  the gutter's image slope is **−0.0436 ± 0.0006 px/px over 128 columns (rms 0.09 px)**;
  fed through the calibrated camera it implies a camera height of 0.30 m, which is absurd.
  That is a fourth demonstration that an image slope of a fore-aft line is not a rake.

---

## 2. PART B — THE REAR ARCH AS A FLAT-CROWNED OGEE

### 2.1 The trace

Sub-pixel lip trace on the **R channel** (the red body plateau R ≈ 165–195 falls to R ≈ 10–20
in the arch interior in 2–3 px; the gold pinstripe on the lip is intermittent and was not
used as the edge). Crop **cols[640,872) rows[505,604)**, first sustained R < 35 run of 5,
then half-max falling crossing in a ±7-row window. 185 of 232 columns traced; 6 outliers
(dark folk-art specks at u 657, 758–761, 844–845) rejected by a 9-wide median filter.
Vertical arc flanks traced separately by rows: **rows[540,606) cols[625,712) and
cols[795,882)**.

### 2.2 A circle is refuted, overwhelmingly

| model fitted over the full traced lip | rms |
|---|---|
| circle | **11.41 mm** |
| symmetric power law, best window | 2.7–4.2 mm |
| superellipse (|Δx|/a)ⁿ + ((h−drop)/h)ⁿ = 1 | **2.67 mm** |

### 2.3 The exponent — CONFIRMED but NOT scale-free, and that matters

Fitted in the metric, de-sloped **body** frame (image rows corrected by the −0.0385 px/px
body-line slope, which brings the two arch feet from 10.4 px apart to 2.8 px apart —
an independent validation of the de-slope):

| half-window | n | exponent | rms |
|---|---|---|---|
| ±0.249 m | 107 | 3.52 ± 0.08 | 0.82 mm |
| ±0.299 m | 129 | 3.50 ± 0.06 | 1.26 mm |
| **±0.349 m** | 151 | **3.83 ± 0.07** | 2.32 mm |
| ±0.399 m | 173 | 4.28 ± 0.05 | 2.84 mm |
| ±0.449 m | 179 | 4.28 ± 0.05 | 2.84 mm |

> **rev 13's "drop ∝ |Δx|^3.9 ± 0.2" is CONFIRMED — at a ±0.35 m window, where I get
> 3.83 ± 0.07. But the exponent is window-dependent, running 3.5 → 4.3 over plausible
> windows, so 3.9 is not a property of the arch; it is a property of a choice of window.**
> Do not implement a single power law and expect it to reproduce both the crown and the
> feet. Implement the superellipse or the table.

**Recommended single-formula fit** (full traced lip, n = 169, **rms 2.67 mm**):

```
  (|x - x_c| / a)^n  +  ((h - drop)/h)^n  =  1
     x_c = -1.088 ± 0.008 m      a = 0.44 ... 0.48 m      n = 3.50 ± 0.11
```
(a and h trade off against each other over the traced span; use the **directly measured**
width of §2.5 rather than the fitted a.)

**Normalised profile table — assumption-free, use this if in doubt.** Δx as a fraction of
the half-width, drop as a fraction of crown-to-foot:

| Δx/a | −0.90 | −0.80 | −0.70 | −0.60 | −0.50 | −0.40 | −0.30 | −0.20 | −0.10 | 0 |
|---|---|---|---|---|---|---|---|---|---|---|
| drop | 0.583 | 0.370 | 0.246 | 0.156 | 0.117 | 0.090 | 0.078 | 0.074 | 0.068 | 0.060 |

| Δx/a | +0.10 | +0.20 | +0.30 | +0.40 | +0.50 | +0.60 | +0.70 | +0.80 | +0.90 | +0.95 |
|---|---|---|---|---|---|---|---|---|---|---|
| drop | 0.014 | 0.057 | 0.058 | 0.076 | 0.101 | 0.146 | 0.217 | 0.354 | 0.593 | 0.754 |

### 2.4 Crown flatness and centring — INDEPENDENT of §0's calibration

The lip's crown, de-sloped:

| within | span |
|---|---|
| 1.2 mm | 164 mm |
| 2.5 mm | 209 mm |
| **4.6 mm** | **313 mm** |
| 9.3 mm | 377 mm |

> rev 13's "crown flat within 4.7 mm over 337 mm" is **CONFIRMED** (4.6 mm over 313 mm).

**Centring.** The symmetric power-law fit puts the crown centre at
**u = 749.4 ± 0.2** against the rear hub at **u = 749.38 ± 0.05**. Both are image
columns, so this is a ratio-free comparison that uses no scale at all:

> **The rear arch is centred on the rear axle to within 0.2 px ≈ 1 mm.** AUDIT_rev11's
> "centred within 9 mm" is confirmed and tightened by an order of magnitude.
> `ARCH_R`'s concentricity with the wheel is right; only the profile and the width are wrong.

### 2.5 The width — settled, and rev 13's 1.026 m is refuted

Feet of the lip, where it meets the rocker: **u 652.4 ± 0.5** (forward) and
**u 851.0–853.1** (aft, short extrapolation from the last traced row). Chord
**199.5 ± 2.5 px**.

| route | width |
|---|---|
| projective map of §0 (correct) | **0.905 m** |
| linear 211.1 px/m (no perspective) | 0.946 m |
| rear rim flange as a local horizontal ruler, rim OD 0.4396 | 0.949 m |

The spread is entirely the choice of map; §0.3 says the projective one is right, so the
linear routes are upper bounds.

> **REAR ARCH WIDTH = 0.92 ± 0.03 m.**
> Dimensionless form, immune to every scale question: **width / rear rim flange OD =
> 2.158 ± 0.027.**
> Built: **0.747 m → the arch is 175 ± 30 mm too narrow.**

| inherited claim | verdict |
|---|---|
| AUDIT_rev11 "0.881–0.933, 143–195 mm too narrow" | **CONFIRMED**, mine sits inside it |
| AUDIT_rev12 "independent floor 0.875 m" | **CONFIRMED** |
| REF §589 "−0.738 → −1.690" = 0.952 m, and after rule 6's +100 mm it centres at −1.114 | **CONFIRMED** (and this is a fourth independent confirmation of the 100 mm origin correction) |
| rev 13 wheels pass "**1.026 ± 0.035**" | **REFUTED at 3.4 σ** |

### 2.6 One more thing that falls out

Lip height above the hub at the crown = **0.3726 ± 0.0052 m** against the built
`ARCH_R = 0.3735`. **The radius is right; the shape is not.** The correct change is
exactly what NEXT_CONTEXT_rev13 said: change the *profile*, not the radius — hold the
crown height, widen to 0.92 m, and use the §2.3 profile.

---

## 3. PART C — THE TAIL, RE-DERIVED FROM SCRATCH, DIMENSIONLESSLY

Every inherited tail number was discarded. Nothing below touches the nose, the front
bumper, or **columns 62–79** (the lamppost); nothing below subtracts two numbers in
different origins. The only datum is the two hub columns.

### 3.1 The measurement

Rearmost sheet metal, `ref_side.jpg`, redness edge, **crop cols[880,965) rows[470,600)**,
108 rows traced, silhouette flat to ±1.0 px over rows 474–552:

**u_tail = 922.2 ± 0.6** (maximum at v = 525).

Rows 450–462 return u 941–955 — that is **orange graffiti on the background wall**, not
the vehicle, and it is the trap that would inflate the overhang by 130 mm. Rejected.

### 3.2 The result, as a fraction of a named datum

> **DATUM: the wheelbase, 2.400 m, between the two hub columns (both LOCKED).**
>
> **rear overhang / wheelbase = (u_tail − u_rhub)/(u_rhub − u_fhub) = 0.3412 ± 0.0015**
>
> This number is raw image geometry. It contains no origin, no scale and no ground line.

Converted:

| map | overhang past the rear axle |
|---|---|
| **projective (§0, correct)** | **0.773 ± 0.022 m** |
| linear 211.1 px/m | 0.818 m |
| **model `X_TAIL` − `X_AXLE_R`** | **1.008 m** |

> **THE TAIL IS 235 ± 22 mm TOO LONG.**
> Sanity: the linear route gives 0.818, reproducing AUDIT_rev12's 0.813 ± 0.013 to 5 mm —
> so my chain and theirs agree where they use the same map, and the extra 45 mm is the
> perspective correction they did not apply. AUDIT_rev12's "plausibly 250–300 mm" is at
> the top of my band; 300 mm would need ρ ≈ 1.09, which the rims exclude.
> **The "99 mm tail" of SPEC §10.7 is REFUTED outright** (10 σ).

Cross-check with a completely different pair of features, both on the near flank, no hub:
the arch's aft foot is at u 852; tail − arch-aft-foot = 70 px = **0.32 m**. With the
measured arch (half-width 0.46 m about the axle), that puts the tail at
x = −1.100 − 0.46 − 0.32 = **−1.88 m**, against the model's −2.108. Independent, and it
agrees to 8 mm.

### 3.3 The aft station set a re-loft should use

**DATUM: O = x(rear axle) − x(tail) = 0.773 ± 0.022 m** (was 1.008).
Express every aft station as f = (x + 1.100)/(−O). The current station set already has a
sensible f-distribution (it clusters hard into the corner roll); **re-space it, do not
translate it**:

| f (keep) | 0.0546 | 0.1538 | 0.2480 | 0.3373 | 0.4216 | 0.5010 | 0.5734 | 0.6399 | 0.6994 | 0.7490 | 0.7897 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| current x | −1.155 | −1.255 | −1.350 | −1.440 | −1.525 | −1.605 | −1.678 | −1.745 | −1.805 | −1.855 | −1.896 |
| **new x** | **−1.142** | **−1.219** | **−1.292** | **−1.361** | **−1.426** | **−1.487** | **−1.543** | **−1.595** | **−1.641** | **−1.679** | **−1.710** |

| f (keep) | 0.8274 | 0.8611 | 0.8909 | 0.9167 | 0.9395 | 0.9583 | 0.9732 | 0.9851 | 0.9936 | 1.0000 |
|---|---|---|---|---|---|---|---|---|---|---|
| current x | −1.934 | −1.968 | −1.998 | −2.024 | −2.047 | −2.066 | −2.081 | −2.093 | −2.1015 | −2.108 |
| **new x** | **−1.740** | **−1.766** | **−1.789** | **−1.809** | **−1.826** | **−1.841** | **−1.852** | **−1.862** | **−1.868** | **−1.873** |

Everything keyed to `X_TAIL` moves with it: `ZB`, `ZT_ALL`, `RT_ALL`, `CR_ALL`, `WX`,
`RB_ALL` all have knots at −2.108/−2.1015/−2.093/… and each must be re-spaced by the same
f, not clipped. **Note the consequence AUDIT_rev12 flagged and it gets worse, not better:
with the arch also widening to 0.92 m, the arch's aft foot lands at x = −1.56 and the aft
skin at −1.873 — only 313 mm apart, against 418 mm today.**

### 3.4 Two things about the tail I could NOT settle

* **The height of the flat tail panel.** The counter fascia occludes rows 400–470, exactly
  where the panel's upper end is. The silhouette is flat to ±1 px over rows 474–552 (0.36 m)
  and has certainly rolled by row 396. So the flat panel is between **0.36 and 0.72 m**
  tall against the model's **1.02 m** — probably too tall, but I will not put a number on it.
  Resolving it needs a rear view with the counter out of the way.
* **Whether the silhouette is the near rear corner or the centreline.** Under the §0 camera
  the extreme-u point on the tail is on the NEAR side (larger y projects further right), so
  the near-flank map is the right one and the residual bias is small — but I have not
  bounded it. It is of order the tail's own half-width taper and I estimate < 15 mm.

---

## 4. PART D — THE END-CAP POLES

**Fully INDEPENDENT of every image measurement above. Mesh-derived, so certain.**

### 4.1 The mechanism, found

`t1_core.loft(..., cap_first=True, cap_last=True)` appends **one 110-gon** at each end
(`NLOOP = 2·NHALF − 2 = 110`). `build.py` then runs `SUBSURF` **before** everything else.
Catmull–Clark turns an n-gon into n quads around a new **face point of valence n**. That
face point is the pole. Solidify duplicates it; the tail booleans then add a few faces
around it.

Probed on the shipped build (`T1_SUB=1`, `T1_body` 56 293 v / 52 313 f):

| pole | valence | face mix | spoke length min/med/max | fan area | max normal spread | smooth |
|---|---|---|---|---|---|---|
| tail outer (−2.1080, 0, 0.9612) | **115** | 11 tri / 85 quad / 19 ngon | 0.146 / 0.468 / **0.562 m** | **0.4597 m²** | 8.5° | yes |
| tail inner (−2.1052, 0, 0.9611) | 112 | 14 / 78 / 20 | same | 0.4597 m² | 8.8° | yes |
| nose outer (2.1252, 0, 0.7727) | 110 | 0 / 110 / 0 | 0.250 / 0.552 / 0.580 m | 0.6501 m² | 8.7° | yes |
| nose inner (2.1224, 0, 0.7729) | 110 | 0 / 110 / 0 | same | 0.6505 m² | 8.7° | yes |

The pole's location is **exactly** the raw cap centroid minus the ride drop:
cap centroid (−2.1080, 0, 0.9717); `rake_drop(−2.108) = 0.010508`; 0.9717 − 0.0105 =
**0.9612**. Confirms the mechanism to 0.1 mm.

### 4.2 It is not only a shading defect — there is a 1.4 mm geometric spike

Comparing the raw loft + SUBSURF(1) with the same rings capped by an explicit quad grid:

| | shipped n-gon cap | grid cap |
|---|---|---|
| tail centreline surface x over z 0.53–1.42 | **−2.1066** | **−2.1080** (flat) |
| tail-most vertex | −2.10800 **at z = 0.9717 only** | −2.10800 over the whole panel |
| valence histogram (whole shell) | 4:28160, 3:220, **110:2** | 4:34202, **3:8**, no pole |
| non-manifold edges | 0 | **0** |
| verts | 28 382 | 34 210 |

> **The flat tail face is pulled 1.4 mm forward of its authored plane by the subdivision,
> and the pole is left standing 1.4 mm proud of it** — a 0.2°-half-angle cone at the exact
> centre of a flat panel, smooth-shaded across 110–115 spokes. That is a specular
> starburst generator independent of any material, which is exactly why the four ablation
> arms (art 15.459, albedo 15.412, spec 16.834 vs as-built 15.478) all failed to move it.

### 4.3 SPECIFICATION — what to build instead

**Use a grid cap. Not a quad-fan-with-a-central-quad (110 is not reducible to 4 without a
pole), and not a re-spaced station set (station spacing is orthogonal to this defect —
the pole is created by the *cap*, at any spacing).**

```
In t1_core.loft(), replace each `cap_*` n-gon with an (a x b) Coons quad grid whose
border IS the boundary loop:

  n = NLOOP = 110  ->  a = 27, b = 28   (sides 27/28/27/28, opposite sides equal)
  corners at loop indices 0, 27, 55, 82
  interior points by bilinear Coons interpolation of the four border curves
  faces: a*b = 756 quads per cap (+702 new verts per cap)

Verified result: max valence 4 everywhere, exactly 8 valence-3 verts (the 4 corners
of each cap), 0 non-manifold edges, tail face flat at x = -2.1080.
```

**Strongly recommended at the same time:** make `NHALF = 57` so `NLOOP = 112 = 4x28`, and
put the corners at 0/28/56/84. Then the cap grid is **mirror-symmetric about y = 0**, which
the 27/28 split is not (the mirror of index 27 is 83, not 82). This changes every ring in
the shell, so it belongs in the same re-loft and nowhere else.

**WHAT IT DOES TO THE BOOLEAN ORDER — the part that must not be missed:**

1. **Order is unchanged and every stage stays legal.** The cap change is inside `loft()`,
   i.e. before SUBSURF, before `nose_shape`, before the arch cut, before solidify. The
   shell is closed and manifold at every stage (measured: 0 non-manifold edges after
   SUBSURF). **The arch boolean — the one cut made while the shell is a closed solid —
   is unaffected; the caps are 0.7 m from the nearest arch.**
2. **It makes the tail booleans strictly easier.** Today the rear-window and engine-lid
   cutters have to cut a single 110-gon-derived fan, and they leave **19 n-gons and 11
   triangles jammed against the pole**. A quad grid gives the exact solver a regular
   patch. Expect *fewer* degenerate faces, not more.
3. **THE TAIL SKIN MOVES 1.4 mm AFT and two chrome details are anchored to its OLD
   position.** `t1_detail.plate_1963` and `t1_detail.englid_handle` are both placed at
   `x = -2.1070` with the comment *"measured tail skin at z 0.78 / z 1.03"* — i.e. they
   were fitted to the **artefact** surface at −2.1066. After the fix the skin is at
   −2.1080 and those two parts sit **1.0 mm inside it**. Move both to −2.1084 or aft, or
   re-derive them from `X_TAIL`. `tail` (the lamp) at −2.1040 keeps clearance but its gap
   changes from 2.6 to 4.0 mm. **This interacts with Part C: after the tail re-space,
   `X_TAIL` becomes −1.873 and all three must be re-anchored anyway. Do D and C in one
   change.**
4. **Cost.** +5 828 v on the raw shell (+20.5 %) at SUB=1, roughly ×4 that at SUB=2. The
   guards must be re-read at **both** subdivision levels, per the standing rule about
   `t1_shell.py:286`.
5. `shade_smooth()` on the body can stay. With no pole and a flat cap there is nothing for
   it to fan.

---

## 5. INDEPENDENCE LEDGER — do not count these twice

| finding | shares a chain with |
|---|---|
| §0 camera model (ρ, u_vp, k_t) | — (root of the chain) |
| §1.2 gutter 1.7485 / silhouette 1.9435 | §0 k_t |
| §1.3 R = 1.84, D = 0.2116, roof line −63 mm | §1.2, hence §0. **`D` and `R` are ONE finding restated, not two.** |
| §2.3 exponent, §2.4 flatness, §2.4 centring | **INDEPENDENT of §0** (affine-invariant / column-only) |
| §2.5 arch width 0.92 m | §0 |
| §2.6 lip height 0.3726 m | §0 k_t — and it is the *same* k_t that was partly calibrated against the arch-to-tyre gap, so treat §2.6 as a **consistency check, not a measurement** |
| §3.2 overhang 0.773 m | §0 |
| §3.2 arch-foot-to-tail cross-check | §0 for the metre value; **independent of the hub datum** |
| §4 all | **fully INDEPENDENT** (mesh only) |
| §0.4 ground line at v = 676 | §0 k_t + the locked tyre OD |

Also, explicitly: **the +130 mm dome deficit of §1.3 and the −63 mm roof line of §1.2 are
NOT two defects.** They are the two halves of one two-parameter fit to two measurements
(gutter, crown). Reported together, applied together, or not at all.

---

## 6. THE ONE PHOTOGRAPH I WOULD ASK FOR

**A head-on rear elevation (or front elevation) of the vehicle, taken from a tripod at
roof height or above, with the counter and the lids clear of the roof line.**

It is the single frame that unblocks the most:
* it gives the transverse roof section **directly** — the crown radius stops being an
  inference from two heights plus an assumed parabola (§1.4), and `DOME_DEFICIT` can be
  driven to zero against a measurement rather than against an identity;
* it gives the roof half-width `Yt`, which every R above is proportional to the square of;
* it shows the full tail panel, which `ref_rear34.jpg` cuts off at the frame edge and
  `ref_side.jpg` sees only in silhouette — settling §3.4's flat-panel height;
* and being head-on, one frame carries no fore-aft perspective term at all, so it is the
  only way to break the depth/scale degeneracy that disqualified `ref_side.jpg` for the
  roof in §1.1.
