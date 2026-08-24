# LEDGER — rev 60

Every figure here was watched print. Where a figure is inherited it says so.
The brief for rev 61 cites this file; the audit at close re-computed each row.

## §0 WHAT REV 60 WAS ASKED FOR, AND WHAT IT DID

The owner's instruction: **execute the whole remaining list — D, E, B, C plus
the cheap rows — in the cadence ground / build / adversarially audit / iterate,
then produce a comprehensive render-against-photograph gap review for the next
context.**

| item | outcome |
|---|---|
| **D** the ground shadow and underbody (F67) | **BUILT and PARTLY CLOSED with a measured ceiling** |
| **E** the interiors (F45) | **F45 REFUTED AS WRITTEN.** A different defect measured (F99); cause not separable; not fixed, and why |
| **B** the nose break (F75/F87) | **NOT FIXED. The remedy programme is REFUTED** — three constants swept, none moves the feature |
| **C** the emblem (F63/F69) | **NOT FIXED. Three hypotheses refuted, the CAUSE localised** to the construction |
| cheap | **F85 CLOSED.** `visibility_budget.py` repaired — it was never measuring |

**Two of the four owner items closed as REFUTATIONS rather than fixes.** That is
the honest result and every one is a number, not an opinion.

## §1 ITEM D — THE UNDERBODY (F67)

### §1.1 The defect, measured before anything was built

Vertical luminance profile, cols 930–990 of `out/r59a_hero.png` — between the
wheels, clear of both:

```
render      body 152 DN -> 131 at the lower edge (v 828) -> ground 155 rising to 224
photograph  body  63 DN -> a FORTY-ROW BAND AT 8.5 DN (v 609-648) -> ground -> 140
```

There was **no cavity at all**. Cause: `t1_mats.body_paint` drives the two-tone
off object-space z, so the shell's bottom face at `t1_core.ZB` ≈ 0.386 sits
below the belt line and was painted **body red** — sampled (159, 117, 112).

### §1.2 The scale, and an instrument of mine that was wrong

`ref_side.jpg` px/m from the **rear tyre's horizontal extent at its own hub
row**: 172 px for a locked `TYRE_D` 0.665 m → **251–284 px/m**, threshold-dependent (see the correction below).

**The wheelbase route was REFUSED at 210 px/m.** The vehicle is a few degrees
off square there, so hub-to-hub is foreshortened while the tyre's own width is
not — and the front hub cannot be fitted in that frame at all: **a person in
dark jeans stands in front of that wheel** and the first circle fit locked onto
body red *around* them, putting the centre ~100 px out. **Caught by painting
the fitted circle, not by reasoning.**

Dark band 39 px ÷ that scale = **0.137–0.155 m**, and that band contains **both** the
underbody and the shadowed ground beneath it, with no feature separating them.
So **0.137–0.155 m** is a **CEILING on the pan's drop, not its value**.

**CORRECTION, MADE IN THE SAME REVISION (rule 13).** The first cut of this
published **258.6 px/m** and **0.151 m** as exact. They are one threshold's
reading: the tyre's span runs **167 → 189 px** as the dark threshold goes
30 → 60 DN, so px/m runs **251 → 284** and the ceiling **0.155 → 0.137 m**.
`audit_adversary.py` caught it by re-measuring at a different threshold and
getting 180 px. **`UNDER_DROP` 0.090 m is below even the lowest ceiling, so the
build does not move — the precision was wrong, not the conclusion.**

### §1.3 What was built, and the result

`t1_detail.underbody()` — a notched pan, two chassis rails, an end ramp at each
end — on a new `M["underseal"]`, `UNDER_DROP = 0.090` (a stated assumption
under the measured ceiling).

| cavity floor ÷ open ground | value |
|---|---|
| render, before | **0.545** |
| render, pan on `M["dark"]` | **0.352** |
| render, pan on `M["underseal"]` | **0.219** |
| photograph `ref_side.jpg` | **0.057** |

`probe_rev45_ground.py`, its own frame, ablation against built:

```
T1_NOUNDER=1   G3 0.8375   G4 0.5475
built          G3 0.7714   G4 0.2519
```

**PARTLY CLOSED, CEILING STATED.** The residual is the ruled-in surround: a
white floor under a 13 × 8.5 m softbox fills a 90 mm cavity from every side and
the photograph is a sunlit frame over dark paving. Same ceiling as F62,
measured here for the underbody instead of the flank.

### §1.4 The guard, and two defects the guards caught

**G4** was added to `probe_rev45_ground.py`, its window located from that
probe's own projected contact patches. **C5 is armed at the ABLATION**, which is
render-against-render and so free of the studio caveat — **watched failing at
0.5475 before it was watched passing at 0.2519** (rule 3).

* **G4's first window was wrong and printed a believable 0.3134.** It walked up
  from `min(PX[k][1])` — the farthest contact patch, not the ground line at
  mid-span — and landed on the **red flank across the "Tacombi" lettering**. Its
  minimum was a letter stroke. **Painted, looked at, fixed.** The window now
  separates cavity from flank by **chroma**, not height.
* **`verify.py`'s length row caught the pan's first aft end** protruding 205 mm
  past the vehicle's fixed bodywork limit: *"length 4.260 vs spec 4.055"*. The
  skin runs to −2.108 but everything aft of **−1.905** is on a swung part, which
  `_bounds()` excludes. `UNDER_X1` is set from the guard's limit, not the skin.
* **Two crops were needed before the aft end stopped hanging in mid-air.** The
  first ramp was 1.400 wide against the pan's 1.560 and the 80 mm ledge kept its
  square face. Found by cropping the render again, at the same place.

## §2 ITEM E — F45 IS NOT REPRODUCIBLE (F98/F99/F100)

Three statistics against `ref_nolita_doorshut.jpg`, every window painted:

| statistic | render | photograph | verdict |
|---|---|---|---|
| bay interior ÷ exterior cream | **0.705** | 0.774 | render is *darker*, not brighter |
| relative std inside the bay | **0.161** | 0.060 | render is *more* varied, not flatter |
| edge density, matched 72×72 | **0.231** | 0.200 | render carries *more* edge content |

**CEILING, and it voids two of the three:** a 480 × 320 JPEG against a 1600 px
render biases std and edge density toward the render. They are quoted as
**refutations only** and never as a pass.

**What survives is CHROMA, as a ratio within one frame:**

```
R/B, bay interior     photograph 1.357   render 1.081
R/B, exterior cream   photograph 1.130   render 1.252
interior / exterior   photograph 1.201   render 0.864     net 1.39x
```

**NOT FIXED, DELIBERATELY.** Three causes fit and one frame cannot separate
them (rule 29.3): `GAL_WHITE` is *deliberately* neutral at R/B 0.993; there is
no warm interior practical (`bulb_string` IS emissive but hangs off the drip
rail, outside); or the aperture surround, which the photograph shows as smooth
gold and the render builds as white beading (**F100 — ~4 px wide in a 480 px
frame, and two attempts to window it landed on the body panel; a NEW-FRAME
item**). **W6 makes colour the owner's call**, and warming a paint constant to
absorb what may be a lighting defect is laundering.

## §3 ITEM C — THE EMBLEM (F101–F105)

### §3.1 Three refutations

| hypothesis | test | result |
|---|---|---|
| the 18.9 mm float of the W's outer arms | `T1_VW_CAPMIN` drives the cap's NEAR corner (its 0.176 R span fits the 0.200 R band) | **cells 6 → 2**; with `T1_VW_PUREFIT` **→ 4**. **WORSE** |
| the second normalisation | `T1_VW_PUREFIT` alone | **6**, no change |
| stroke weight | ink fraction, scale-free | photo **0.6062**, built **0.5903**; `T1_VW_WFRAC` 0.1986 → 0.48 leaves the count at **6 throughout** |

Rev 58 had tried the first two **separately**; rev 60 tried **the pair its own
note said was never tried**, and it fails too.

### §3.2 The solve the brief asked for

`cream_cells` into the objective, `T1_VW_CELLSOLVE`, 2000 points over the six
spine constants: **7 cells IS reached — at landmark residual 0.2498**, against
C4's bar of **0.045**, the shipped **0.0347** and rev 45's discredited **0.1167**.
And that solution's 7th cell is a **high-resolution sliver**: re-rasterised at
the photograph's own 69 rows it collapses to **6**.

### §3.3 The cause, and painting is the only reason it was found

`T1_VW_DUMP` paints exactly what `cream_cells` counts. **The photograph's cream
is seven long thin SLIVERS; the build's is four fat WEDGES plus two slivers.**
The ink is the right *amount* arranged the wrong *way*: the V's arms and the W's
outer arms **fuse into two long diagonals crossing at the centre** — the X
itself. **The fix is a different construction, not a re-solve. SCOPED, NOT BUILT.**

### §3.4 And C6 compares two rasters at different scales (F105)

`photo_cells()` counts in a 41 × 69 crop; `glyph_only_mask` defaults to 276
rows. Built count against scale: **41 → 4; 55…552 → 6**. Stable where it
matters, so C6's verdict stands — but at the photograph's own scale the built
glyph reads **4**, so **C6 understates the deficit**.

## §4 ITEM B — THE REMEDY PROGRAMME IS REFUTED (F106/F107)

`probe_rev59_nose.py` M1, pose-free, 4 controls passing: built **1.187** lamp
radii against the photographs' **1.951 … 2.127** — a **74–76 mm** rise.

Two diagnostic ablations added, read out through M1:

```
V_POW   0.15 / 0.60 / 1.20        ->  1.174 / 1.187 / 1.170 lamp radii
V_RISE  0.8670 / 0.9800           ->  1.174 / 1.165
V_POW = V_POW_Z, 0.60 / 0.30      ->  1.175 / 1.178
```

**An 8× sweep of `V_POW` moves the break by 0.004 lamp radii.** The switches
are **not inert**: the extreme arms differ over **128 421 pixels** and an
inboard column's cream boundary moves **808 → 900 px**. The change is real,
large, and concentrated at the V's **apex**, where it does nothing for the lamp.

**So rev 58's "`V_POW` needs 0.345 at the lamp" is REFUTED** — setting it to
0.345 leaves the break where it was. And the swage is ruled out with the paint.

**NOT PUBLISHED, and this is why.** An analytic two-constraint solve was built
first and predicted a break of **0.604** lamp radii where the machine measures
**1.187**. A hand-written copy of a node graph that the machine contradicts by
42 mm is not a solve. It was thrown away, not reported.

## §5 THE CHEAP ROWS

* **F85 CLOSED.** `gloss_compare.py` wrote painted tiles into tracked
  `probe_scratch/`; they go to `out/` now, `T1_GL_TILES=track` restores the old
  destination. Watched: the gate leaves the tree clean.
* **`visibility_budget.py` was never measuring.** It named `out/r57_hero.png`,
  a revision-numbered frame that cannot exist on a clone, so it **always** took
  its except branch and **always** reported a FALLBACK scale while printing a
  table that reads like a measurement (rule 37). It globs now and says
  **NO RENDER** in those words, exiting 2.
* **And its table omitted three of the owner's own five items** while ranking
  the CEILED gloss row first. Rows added for F63, F67, F75, F99. The verify row
  that pinned the old order is **re-based with the cause named plus a companion
  row** asserting the table still carries F63/F67/F75.
* **I broke a by-value guard and it caught me.** The first `T1_VPOW` cut took
  out all three `^V_POW = 0.60` rows — the three the rev-60 brief named. The
  literal is back on its own line with the override below it.

## §6 THE STATE OF THE GATES AT CLOSE

```
bootstrap.sh      AT PICKUP  9 PASSED, 1 FAILED -- row 9, STRANDED
                             origin/claude/bus-model-rev57-yvrlhi (6 commits, 16 files)
                  AT CLOSE   ALL 10 PASS, and an independent loop over every remote branch
                             finds none ahead of HEAD.  Rev 60 merged nothing, so the pickup
                             reading was probably taken against an incompletely-fetched
                             remote -- STATED AS A GUESS, not a finding (rule 29.3)
verify_clone.sh   261 PASSED, 1 FAILED at mid-revision -- the self-referential row count only
verify.py         0 fail, 0 warn at T1_SUB=1 AND T1_SUB=2
probe_rev46_vw    7 checked, 1 FAILED -- C6, photo 7 built 6.  UNCHANGED, by design
probe_rev59_nose  5 checked, 1 FAILED -- M1, 1.187 vs 1.951..2.127.  UNCHANGED
probe_rev45_ground 5 checked, 0 FAILED -- G4 0.2519 (was 0.5475 ablated)
```
