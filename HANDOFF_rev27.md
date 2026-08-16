# HANDOFF rev 27

**124 commits, clean tree. Guards 0 fail / 0 warn at BOTH subdivision levels
throughout. NO GEOMETRY MOVED. NO ARTWORK MOVED. NOTHING WAS TUNED.**

`rev25_hero34f.png` still photographs the current mesh and the current artwork.
No hero was shot and none is owed.

rev 27 opened **CLEAN** — the eighth revision running. 15 bundles crossed in ONE
`device_stage_files` call; all ten md5s recorded in memory matched; the restore
ran 59 → 67 → 71 → 75 → 81 → 87 → 93 → 96 → 101 → 105 → 107 → 115 → **120**,
clean, no divergent-branches error; **22/22 content checks exact, 8/8 ancestry**;
the three texture md5s correct including the corrected `swirl_b` `d201597e`.

---

## 1. What rev 27 did, in the order §6 of the rev-27 prompt set

### Item 1 — §10.71's wrong-material anchor. **SETTLED as far as the admissible set allows.** (§10.76)

`COUNTERTAN`, `CREAM`, `COUNTERCREAM` and `W_DUST_FAC_UP` are **UNCHANGED**.

* **The chain reproduces exactly.** `lin(202,172,127)/E` → `(0.6104, 0.52998,
  0.42647)` against the written `_UP_MEASURED = (0.6104, 0.5300, 0.4265)`,
  **3.1e-5**. rev 12's arithmetic was right.
* **The comment mislabels the gain.** "this file's CREAM (0.9676, 0.7784,
  0.4976)" is **not** `CREAM` (which is `(0.6172, 0.6308, 0.5776)`) — it is the
  **von-Kries gain itself**, `lin(203,186,146)/CREAM`, reproduced to **4.7e-5**.
  **My opening hypothesis — that the solve consumed a stale `CREAM` — was
  REFUTED by the arithmetic.** Corrected in place.
* **The live assert's three-channel agreement is a TAUTOLOGY**, spread
  **5.2e-05**: `W_DUST_COL_UP` was solved collinear with `COUNTERCREAM` and
  `_UP_MEASURED`, so it must agree whatever the numbers are. §10.71 reads that
  agreement as evidence; it is the solve restated.
* **Both source patches had NO coordinates anywhere in the repo.** Recovered
  forensically by searching `ref_rear34.jpg` for the box whose
  middle-80 %-of-L\* median **is** the recorded triple — a convention itself
  recovered, because it is what takes 2691 px to exactly **2153** and 2700 px to
  exactly **2160**.
  * flank **u 914–983, v 298–337** (69×39), trimmed n **2153**, err **0.0** —
    exact **and unique**.
  * top **u 556–656, v 397–424** (100×27), trimmed n **2160**, err **0.0** —
    exact but **NOT unique**. *Which box rev 12 used is NOT claimed.*
* **Box-independent:** the counter top is a diagonal band 15–25 px deep; the
  largest axis-aligned rectangle lying entirely on it is **1060–1512 px** across
  a swept gate, against the **2700** the patch needs. **So it straddled,
  whichever box it was** — 66–82 % tan, 8–19 % cream, 6–9 % brass, 2–4 % a tin
  can standing on the counter.
* **AND THE STRADDLE IS NOT THE EXPLANATION — my second hypothesis, refuted by
  my own control.** On a band-following clean sample, gate and erosion **swept**
  over 12 arms, the disagreement gets **WORSE**: **(−0.295, −0.320, −1.674) →
  (−0.82, −0.56, −2.19)**.
* **THE FINDING, stronger than §10.71 states:** `_UP_MEASURED` lies **OUTSIDE**
  the segment [`COUNTERTAN`, `W_DUST_COL_UP`] in all three channels. Not a
  coverage error — **there is no coverage**. E-free: observed top/flank
  **(1.056, 0.884, 0.803)** against dusty `COUNTERTAN`'s **(0.881, 0.681,
  0.461)**, B out by **74 %**.
* **NOT DECIDED, deliberately.** The de-illuminated top is **proportional to
  `CREAM`** channel-wise, so this frame cannot separate `COUNTERTAN` from
  `CREAM`; and the pair is up-facing top vs vertical flank, the mismatch §10.60
  ruled **INADMISSIBLE**. For the top to be dusty `COUNTERTAN`, `CREAM` would
  have to be ≈ sRGB(190,185,156), hue 51°/sat 0.18 — between the locked
  (206,208,200) and rev 20's read of the bus's cream (216,200,161).

### Item 2 — the residual pedestal. F90 REFUTED; three of four candidates closed. (§10.77, §10.78)

* **§10.77 — `T1_CTAN_SP=0` IS a complete specular ablation.** `probe_f90.py`,
  a purpose-made minimal scene. **SP0 == TRUE-OFF (spec 0 *and* ior 1) == bare
  DIFFUSE to six decimal places at BOTH normal and 83° grazing.** Whole specular
  = 15.834 % of the true-off arm at grazing; fraction `T1_CTAN_SP=0` fails to
  remove = **0.00 %**. **rev 26's arm 4 was COMPLETE; the residual is NOT
  specular.**
* **§10.78 — two harness controls exact to six decimals first**, then:
  `T1_WORLD=0` and `T1_GAL_LUM=0` re-run **on the residual configuration**
  (not assumed to transfer): **(6.56, 6.60, 8.51) % → (6.55, 6.58, 8.48) %**,
  the two carrying **2.64 / 2.78 / 2.91 %** between them. **REFUTED, ~97 %
  survives.**
* **`T1_CYCALB=0` IS A VACUOUS ARM.** It reproduced the shipped arm to six
  decimals in *both* albedo points, which reads as a refutation and is not:
  `ST.cyclorama()` is at `build.py:600` and the probe's `_build()` truncates
  `build.py` at **586**. Verified **empirically** — no `cyc` object, `cyc_white`
  is `None`, while 185 meshes build. **The cyclorama is excluded by ABSENCE,
  not ablation.**
* **`T1_GAL_SKY` IS A DEAD LEVER** — AST census **Store 1, Load 0**, under
  seventeen lines of "SOLVED, not chosen" commentary. Only `GAL_LUM` is read, at
  `t1_detail.py:2047`. Sixth instance of the family. **Named, not quietly
  fixed** — repairing it changes the galley lighting.
* **The scene→top bounce is the ONLY named candidate left** and has no lever.

### Item 3 — the front over-rider. First step only. (§10.79)

* A **validated** slanted-edge PSF estimator: positive control recovers σ 0.70 →
  **0.680 (2.9 %)**, 1.20 → **1.249 (4.1 %)**, 1.80 → **1.743 (3.2 %)**.
* **My first cut resampled BILINEARLY** — a triangular filter — and read 0.70 as
  **1.068 px (+52 %)**. The control caught it. Replaced with a raw-pixel
  construction that interpolates nothing.
* **My first three ROIs were rejected by the isolation test**, correctly: the
  trolley member is a **BAR**, so any window holding its step holds its other
  edge (contrast fine 40/40 columns; spread over limit in 21–40 of 40).
* **NO σ IS PUBLISHED for `ref_workshop.jpg`.** A global hunt returns five
  straight isolated candidates, boxes printed, but the estimator cannot tell an
  **occlusion step** from a **paint boundary** — rev 26's exact error. Pooling
  them gives 1.736 / 1.087 / 0.986 px, a **76 % spread**. **The probe DECLINES
  and prints why.**

---

## 2. Guard figures — every one watched print, both levels

| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 0 warn** | **0 fail, 0 warn** |
| roof crown @ rear axle | **1.9835** (baseline 1.9835, −0.0 mm) | **1.9833** (−0.2 mm) |
| rear arch lip → gap | **0.3722 → 39.7 mm** | same |
| front arch (control) | **0.3732 → 40.7 mm** | same |
| rake | **17.75 mm/m (locked 17.75)** | same |
| dome deficit / rear overhang | +0 / **0.7730** | same |
| dims | L=4.065 W=1.750 | same |
| cut roof hole | **68564v** | **252749v** |
| objects at `materials:` | **126** | **126** |
| shut line × aperture, SHOW | **0.0 mm** | **0.0 mm** |
| shut line × aperture, OFF | **804.9 mm** (baseline 804.9, −0.0) | same |
| `CARGO_GAP` samples | **154** | same |

**185 meshes; 42 materials; 5 constant-rough; 0 non-manifold; bays 0.516 0.515
0.516; band 1.372–1.775.** Identical to rev 23/24/25/26.

---

## 3. Files changed

* **`SPEC.md`** — §10.76, §10.77, §10.78, §10.79 and four change-log rows.
* **`t1_mats.py`** — the mislabelled-gain correction; the recovered crop boxes
  recorded; and a **LABELLED REGRESSION CATCHER** on the three-channel
  `COUNTERTAN`-vs-`_UP_MEASURED` residual, baseline
  **(−0.066877, −0.100324, −0.159974)**, plus a sign assert. **No constant
  changed.**
* **`probe_dust_anchor.py`** — NEW, read-only, parses `t1_mats` rather than
  re-typing it, every parse RAISES, ignores env overrides. Five asserted
  controls; falsified in five arms.
* **`probe_f90.py`** — NEW, read-only, minimal scene.
* **`probe_psf_workshop.py`** — NEW, read-only, validated estimator that
  declines.

---

## 4. Things rev 28 must NOT silently undo

`HANDOFF_rev26.md` §4, rev 25's §4, rev 24's §4, rev 23's §4, rev 22's §3, rev
21's §4, rev 20's §4, rev 19's §4 and rev 18's §4 **all still stand in full**.
Added by rev 27:

1. **The §10.76 regression catcher in `t1_mats.py` is a BASELINE, not a
   correctness claim.** It says *this disagreement has not moved*. **DO NOT
   TIGHTEN IT AND DO NOT TUNE TO IT** — driving it to zero means inventing an
   albedo. Same status as `H_ROOF_REGRESSION` and the 804.9 mm off-flank row.
2. **It must stay PER-CHANNEL.** rev 27's first cut asserted the `max`, which
   lives in B, so displacing `COUNTERTAN`'s R by +0.020 left it **silent**.
   Falsification caught it; **the cause was fixed, the band was NOT widened.**
3. **`T1_CTAN` must keep SKIPPING the new guard** — it is the A/B lever and must
   survive.
4. **Do not re-open the F90 question.** §10.77 measured it: 0.00 % left behind.
5. **Do not treat `T1_CYCALB=0` as a refutation.** It is VACUOUS in that
   harness — the cyclorama is not in the scene.
6. **Do not publish a PSF for `ref_workshop.jpg` from an unidentified edge.**
   The estimator is validated; the EDGE IDENTITY is the blocker.
7. **`probe_dust_anchor.py` parses `t1_mats` deliberately and RAISES on a failed
   parse.** Do not add a fallback — a silent fallback is how a stale constant
   ships.

---

## 5. Still open

* **§10.76 — `W_DUST_FAC_UP = 0.7313` is unsupported for the surface it is
  applied to and CANNOT be re-solved from this pair.** Blocked on `CREAM`, or on
  a same-class pair with a locked albedo ratio and differing orientations, which
  does not exist in `ref_rear34.jpg`.
* **The residual 6.6 / 6.6 / 8.5 % pedestal** — only the **scene→top bounce**
  remains (`gal_warmer`, `gal_caddy0/1`, `T1_body`). No lever; a visibility flag
  is barred by §10.56, so it needs the objects removed and the mask re-derived.
* **`GAL_SKY` is dead** — named, not fixed.
* **THE FRONT OVER-RIDER** — owner has ruled the tube and post are on the bus and
  chose *model them, tagged workshop-stage*. Blocked on the PSF edge identity,
  then a plane scale or a proof none is admissible. **This will move geometry
  and invalidate `rev25_hero34f.png`.**
* **THE FRONT BUMPER FACE IS UNMEASURED** — both catalogue values struck.
* **`CREAM`** — unchanged, needs a same-light same-CLASS three-channel reference
  that does not exist in the three photographs.
* **THE ABSOLUTE ROOF HEIGHT** — 1.960 retired, nothing replaced it.
* **THE OFF FLANK** — two contradictory E features, 804.9 mm.
* **The cab door's true top edge** — authored, unmeasurable on the admissible set.
* `PLATE_W = 0.3300` has no provenance. `probe_rev16.py:90` prints `xa` vs `xa`.
  `X_NOSE`/`X_TAIL` parsed in `folk_gen`, never LOADED.

---

## 6. Two questions outstanding with the owner

Both were sent with **printed crop boxes**, and neither blocks rev 28's other work.

1. **The counter top's surface condition** in `ref_rear34.jpg` — clean varnished
   plywood, visibly dusty, patchy, or can't tell. `W_DUST_FAC_UP` asserts **mean
   coverage 0.548**, so this bears directly on §10.76.
2. **The identity of PSF edges E1/E2/E3** in `ref_workshop.jpg` — paint boundary,
   physical step, both, or can't tell. My reading is *paint boundary*, offered
   and **not relied on**.
