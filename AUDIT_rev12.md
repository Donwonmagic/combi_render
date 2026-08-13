# AUDIT rev 12 — the five remaining dimensions

**Read-only audit.** Nothing in this repo was edited except this file and `measure/`
and `out/`. No build file was touched, by me or by any subagent. Where a finding
proposes a change, the change is written down and **not applied**.

| | |
|---|---|
| line audited | rev-12 line, HEAD `c8f66fe`, clean tree |
| restored from | `tacombi_history_rev9.bundle` + `tacombi_rev12_incremental.bundle` |
| blender | 4.5.3 LTS (67807e1800cc) |
| guards, `T1_SUB=1` | **VERIFY: 0 fail, 1 warn** — `roof @ rear axle 1.923 vs spec 1.960 (-37 mm)` |
| guards, `T1_SUB=2` | **VERIFY: 0 fail, 1 warn** — same warn |
| roof hole | `cut roof hole: 56446v` (SUB=1) / `207959v` (SUB=2); `roof aperture: open, and solid fore / aft / both sides` |
| dimensions covered | A counter+galley · B wheels+ground contact · C tail+rear quarter · D roof · E optics+glass+camera |
| already covered by `AUDIT_rev11.md` and not redone | proportion · weathering · script · fascia |

One deviation from the brief, stated plainly: the restored line has **47** commits
reachable, not 46. The rev-9 bundle restores 34 commits where the rev-9 handoff
documents 30 — the same benign `.gitignore`/handoff-prose drift already logged at
rev 8. The tree, the file set and both guard runs are otherwise exactly as
specified.

---

## 0. The branch divergence — neither audit-line fix is on this line

Both confirmed absent. **Not applied.** They belong to the build context.

| fix | state on the rev-12 line |
|---|---|
| `build.py:421` `SCR = dict(x0=0.784, x1=-0.494, z0=0.4453, z1=0.9177)  # 2.705:1 = tex AR` | **stale.** Still `0.9177`; should be `0.9896`. The script lockup is squashed 15.8 % vertically in every render from this line. |
| `t1_mats.py:1206` `_NOSE_SEL[0] = None` | **present.** It sits inside the alpha branch that begins at line 1198. The colour branch that reads `_NOSE_SEL[0]` is at line 1251 — *after*. It therefore takes its `else` path and the nose gets the decal's alpha with the flank tile's colour. **The nose in this line renders as black marks.** |

`AUDIT_rev11.md` has been copied into the repo root as a reference document,
untracked. The branches are not merged.

---

## How to read the verdicts

Every finding at severity 4 or 5 was put to a second agent whose instruction was
to **refute** it, defaulting to refuted if it could not independently reproduce
the number. Six of those refutation passes ran. Their verdicts are binding on
this report, and several of them overturned the specialist.

| tag | meaning |
|---|---|
| **CONFIRMED** | an independent second measurement reproduced it |
| **PARTIALLY CONFIRMED** | the defect is real, a stated limb of the argument is not |
| **REFUTED** | see §3. Do not raise it again without new evidence |
| **UNVERIFIED** | severity ≤ 3, or no second pass ran. Measure again before acting |

No score appears anywhere in this document. Every number is a measurement
against a named photograph or against the built mesh, with its method and its
uncertainty.

---

# 1. WHERE IT STANDS

## A — Counter and galley

`materials-5` is **dead and can be closed**. Bay-pair peak normalised
cross-correlation in `out/p_side.png` is **+0.157 / +0.281 / +0.148**, against a
positive control that reads +0.517 at a 0.5 shared fraction and +1.000 at 1.0,
and against the *photograph's own* bay-to-bay null of +0.332 / −0.135 / +0.194.
High-passed, render +0.138/+0.166/+0.137 against photograph +0.106/+0.127/+0.166 —
statistically indistinguishable. One duplicated emitter footprint would read
≥ +0.5. The roof hole fixed it.

The **brass nosing correction was applied, not merely explained**. Mesh: 19.5 mm
on a 107.1 mm slab edge = **0.182**, against a photographic 0.1865 ± 0.0107
(se 0.0011) over 86 columns — **0.05 σ**. The counter edge depth
(0.1142 ± 0.0031 m flank-plane against 0.1070 built, ≤ 2.3 σ) and the tan top's
presence and plan position also verify.

The three **menu cards** are correct in count, station, height (0.3383 built
against 0.3385 measured, 0.06 %), colour offset and all five band boundaries.
Their printed text is **not invented** — it is a stripe field, and the reference
resolves ~1.5 px per word, so the build is right to decline. Card width is
6.6 % short and the stripe pitch is ~2.2× too fine.

The **aperture surround** is right in construction and colour. Its "small bulbs"
are **refuted** — the ring elements read L 236 against flank cream at 215, a
ratio of 1.10; a lit filament against daylit cream reads 3–10×. They are fabric
bobbles, as SPEC §4 says. Pitch is 16 % tight.

Galley contrast, on matched windows, two independent locations of the same six
windows:

| bay | photo sd (specialist) | photo sd (verifier) | render sd | status |
|---|---|---|---|---|
| 1 | 32.76 ± 1.75 | 32.76 ± 1.75 | 15.1–15.3 ± 1.3 | dominated by the man — see §3 |
| 2 | 23.62 ± 1.01 | **23.90 ± 1.05** | **13.52 ± 0.40** | **the real defect, 9.2 σ** |
| 3 | 21.81 ± 1.28 | **18.43 ± 1.43** | **20.27 ± 2.22** | render already *exceeds* the photograph |

`COUNTERTAN`'s **hue does not match the measurement its own docstring cites**:
built hue 42.3°, saturation 0.254; `t1_detail.py:1996-2000` quotes hue 29–37,
saturation 0.33–0.39; an independent read over 1266 px gives hue 28.4°,
saturation 0.333. Its *level* remains bracketed and is NOT MEASURABLE (§4).

## B — Wheels, tyres, arches, ground contact

**The vehicle does not float, and `optics-6` as written is measuring the wrong
frame.** This is the most consequential correction in the audit. The founding
reading — "the ground reads 255.00 at every row from 3 px below the contact patch
outward, the catcher writes identically zero alpha" — was taken in
`studio.views()["side"]`, an **orthographic** camera whose view direction is
exactly (0,−1,0) against a cyclorama that *is* the plane z = 0. The ground is
exactly edge-on and occupies two antialias rows. Both the specialist and the
verifier reproduced this: rows 962 (min 209) and 963 (min 251), then 255.00 at
every column. The companion reading "177.00 under the tyre against 177.00 open
ground" is likewise the bare backdrop — AgX+Punchy maps linear 1.0 to display
176.56, measured twice at ≤ 0.5 DN agreement.

In the **shipped hero**, measured by the verifier from its own probe geometry:
the darkest ground pixel beside the near front tyre reads **150/255**, and the
ground returns to white over **≈ 0.84–1.7 m**. There is a real, soft, roughly
metre-scale contact shadow in the delivered frame.

What *is* true is the mechanism, reproduced independently end to end: the
catcher writes α 0.674–0.930 at 20 mm from contact (verifier's own EXR, with
`cyc.is_shadow_catcher = False` as a control giving α ≡ 1.0000, which proves the
sub-unity values are shadow and not coverage); `bg_white_level()` = 24.87;
AgX's slope at the backdrop level is **0.90 code values per linear unit against
66 at linear 0.5–1.0**; and `post.bloom(thr=0.72)` on a display-referred frame
adds a uniform **+0.16 linear** veil. Those four limbs are confirmed. The
conclusion drawn from them was not.

The **rim** is the wheel's error, and the hubcap is not:

| ratio | specialist | verifier | built | gap |
|---|---|---|---|---|
| rim / tyre | 0.6472 ± 0.0095 | **0.6612 ± 0.0060** | 0.5729 | **+0.088, 14.7 σ** |
| hubcap / tyre | 0.4115 ± 0.0065 | **0.4136 ± 0.0045** | 0.4120 | +0.0016, 0.35 σ — correct |

An ellipse fit to the cream ring gives semi-axis ratio 0.9844, so no obliquity
correction is needed; per-octant radii spread 0.71 px with no upper/lower split,
so the detector does not change feature between arcs. The implied rim OD is
**0.4397 m** — which lands **0.1 mm** from `t1_core.py:37 RIM_R = 0.2198`
("rev6 MEASURED 16in flange OD 0.4396"), a constant that `grep` shows is
**referenced by nothing in the repo**. The measurement was taken six revisions
ago and the geometry never consumed it.

The **stance question is settled in favour of the build.** The one measurement
free of a ground line — arch lip radius minus tyre radius, both from the hub
centre — gives **36 ± 5 mm** against the built 41.0 mm, **1.0 σ**. The vehicle
is lowered and 41 mm is right. All four contact patches are coplanar at
`zmin = +0.000000`, and `arch_z(x) = TIRE_R + rake_drop(x)` keeps the arch
concentric at both axles despite the 79.4 / 0.2 mm differential drop.

## C — Tail and rear quarter

`ref_rear34.jpg`'s near end was worked at 5–20× Lanczos.

**The build paints gold folk art across the flat tail face. The photograph has
none.** Zero gold pixels in 35 991, and the zero is gate-independent: the
specialist's gate gives 0, `v > 0` gives 0, `s > 0 ∧ v > 0` gives 0, hue widened
to 25–90° with no gates gives 0. Only hue 20–100° with no gates at all finds 12 px
(0.03 %). The face is **not in shadow** — its own value median is 0.494, p10 0.420 —
and the identical gate on the rear quarter in the same rows returns **20.94 %**,
so the instrument works. The art terminates at x = 952 ± 5, which is
independently the intersection of the flank and tail branches of the cream/red
edge at x 952.3.

The **apron** is right: no rear bumper, no blade, no irons, no gap; a specular
ridge 8–12 px (≈26 mm) above the silhouette edge over x 990–1050 is a tight roll
catching light. `bumper_r` is commented out at `build.py:300-301` and absent from
the inventory.

The **heavy dark-brown curlwork** lives on the rear quarter, as recorded, and its
**colour and stroke weight are correct**: measured ink median RGB (88, 21, 14),
eroded core (78, 16, 11), against `folk_gen.py:548`'s (75, 17, 13) — 13/4/2 DN
across the channels, inside JPEG noise; stroke width 28 ± 4 mm against a ~26 mm
lineage. Its *area fraction* is not a well-posed measurement — 2.4 %, 4.21 %,
0.14 % and 12.46 % are four different gates on the same ink, and `folk_gen.py`
already says so. Mass count is the substantive difference: **13 measured against
5 authored**.

`STATE.md`'s two counter rows are **measuring the wrong objects**.
`audit.py:308` excludes `counter` and `counter_nosing` from "body" but not
`counter_top`, whose x runs to −2.4230. So:

* "overall length (ex counter) 4.5830 … +293.0 mm **OUT**" is
  `ind-1_lens (+2.1600) − counter_top (−2.4230)`. The true length excluding the
  whole counter is **4.2984** — inside SPEC's 4.290 ± 0.025.
* "counter tail overhang past body 0.0070" is the nosing standing 7 mm proud of
  the slab. The real overhang past the tail skin is **0.322 m**.

## D — Roof

Owner-settled items **verified in the build**: one opening only, with the roof
solid at X ≥ +1.060 ± 0.035 and open at X ≤ +0.442 ± 0.044 in `ref_rear34.jpg`
(the built `LID_X0 = +0.964` lies inside that bracket); the "La Santa" panel
detached — no `sign_panel`/`sign_face`/`sign_strut` object exists unless
`T1_SIGNBOARD=1`, which is not the default, so **no shipped render contains the
invented word**; the lid hinged fore-aft and opening sideways.

The **mural's geometry is right and should not be touched**. Petal count k = 8 is
the top harmonic on 5 of 8 clean heads with a summed spectrum peaking at
k8 = 9.44 against k12 = 4.31. Head diameter 0.171 ± 0.005 of the board interior
against a built 0.1758 — 0.9 σ. Three menu strips, no bottom strip, confirmed as
two L-shaped components meeting across the top. Ten heads are present; the owner's
nine is the count of unobscured heads, and the tenth at ≈(583,118) is behind a
palm frond. The bulb-string slope cross-check holds: −0.040 ± 0.011 measured
against −0.03453 built, 0.5 σ.

The **mural's texture is right and its render is not.** This is settled by area
means, not by class fractions:

| | area mean sRGB | b-chromaticity |
|---|---|---|
| `ref_side.jpg` board interior | (126, 60, 24) | 0.1129 |
| `tex/lidmural.png` interior | **(127, 59, 23)** | 0.1101 |
| render | **(148, 92, 69)** | 0.2227 |

The texture matches the photograph to **one sRGB code in every channel**. The
render is displaced +21 R / +33 G / +46 B *away* from the texture's own area
mean and toward neutral. Minification cannot do that — averaging can only pull a
render's mean *toward* the texture's area mean. So there is a near-neutral
additive lift, and the texture is the one thing that is right.

`gal_ceiling` is a **2.034 × 1.110 m opaque slab spanning 100 % of the opening
footprint**, sitting 44.9–46.9 mm below the roof crown, with `visible_camera =
False` and `visible_diffuse / glossy / transmission / volume_scatter / shadow` all
True.

## E — Optics, glass and camera

**One mechanism accounts for most of what reads as CG in this frame.**
`post.main` runs on an already display-referred stitched PNG:
`srgb_to_lin → bloom → chromatic → vignette → lin_to_srgb → grain`. `srgb_to_lin`
puts paper white at linear **1.0**; `post.bloom` computes
`m = clip((lum−0.72)/0.28, 0, 1)`, which is **1.0 for every white pixel**, and the
frame is 70.3 % pure white. The whole frame is lifted to 1.16 linear and clipped.

I verified the three consequences myself, directly on `out/rev12_hero_studio.png`:

| | designed | measured |
|---|---|---|
| vignette, strength 0.055, `r**2.2` | corner ×0.945 → display 250.6 | backdrop **254.9968 → 255.0000** across r/rmax 0.125→1.000; all four 40×40 corners exactly **255.000**; total falloff **0.00 ± 0.01** |
| grain, σ = 0.0042 | ~1.07 code values | backdrop high-pass sd **0.0000 in all three channels**, both sample boxes; **99.51 %** of backdrop pixels exactly (255,255,255) |
| edge halation | symmetric about an edge | veil **+0.0589 linear** on 159 047 subject pixels within 20 px of white, **0.000** on the white side — a one-sided *inward* glow around the whole 2 198-px-wide silhouette |

And 91.1 % of the bloom landing on the speculars is the subject's **own** energy,
so suppressing only the backdrop's contribution would not fix them — the
threshold itself is wrong for a display-referred input.

**The glass is the second mechanism.** Coefficient of variation inside the
aperture — scale-free, so it survives the exposure difference between open shade
and a studio rig:

| aperture | CV | against the photograph's 0.24 |
|---|---|---|
| `ref_side.jpg` cab door glazing (the standard) | 0.24 | — |
| rear pane with the glass **removed** | 0.38 | 1.6× |
| rear pane **as built** | **1.22** | **5.1×** |
| hero cab door glass | 0.70 | 2.9× |
| hero windscreen | **1.34** | **5.6×** |

A six-way ablation on the rear pane, with a render-to-render null of 4.19 mean
|Δlum| established by re-rendering the nominal configuration:

* **the interior is modelled and lit** — deleting the glass gives a coherent
  interior at mean 38.0 with 2.9× less spread and p95 52.9 against 145.8. The
  glass does not hide a black box; it overwrites a working one.
* **81 % of the pane's brightness is the light rig** — removing the rig drops the
  mean from 34.05 to 6.54.
* **`gal_ceiling`'s `visible_glossy` is refuted as the cause here** — turning it
  off moves the pane by 1.87, *below* the 4.19 null.
* **the panes are smooth-shaded** — forcing flat shading changes 88.7 % of the
  pane's pixels at mean |Δ| 39.18, **9.4× the null**. A planar pane with
  interpolated normals reflects a warped image of the room. That is a first-order
  CG tell and it is present.

The **framing**, verified by my own measurement of the shipped hero: subject bbox
cols 177–2375, rows 264–1781; **lead room 177 px (5.9 %) on the nose side,
trailing space 624 px (20.8 %)**; headroom 264 px (13.2 %); tonal centroid at
0.437 W / 0.543 H.

---

# 2. WHAT DOES NOT MATCH

Ranked by what a viewer meets first at hero scale. Every entry states the
measured gap, where the fix lives, and what applying it endangers. **None is
applied.**

### 1. `post.bloom` clips the whole frame — sev 5 — CONFIRMED (two independent reproductions)
70.3 % of the hero is above the bloom threshold, so a +0.16 linear veil goes on
everything and clips. It destroys the vignette outright (0.00 of a designed 4.4
code values), destroys the grain (0.0000 sd), puts a one-sided inward glow around
the entire silhouette, and flattens every specular above 240 (a 250-on-255 patch
loses 100 %, 240 loses 56–60 %). It is also what makes the real contact shadow
look shorter than it is.
**Fix:** `post.py:52-58` — threshold on the excess over the backdrop level, or
pass a matte. `post.py:106-117` ordering.
**Risk:** changes every shipped frame's highlight rendering at once and
invalidates any tuning done downstream of it. Coordinate with item 8. No
geometry, no boolean, no `verify.py` exposure.

### 2. Gold folk art painted across the flat tail face — sev 5 — CONFIRMED
Photograph **0.00 %** gold in 35 991 px, gate-independent, on a face that is not
in shadow, with a positive control at 20.94 % on the rear quarter. Render
**14.30 %** (verifier, background excluded) to **18.11 %** (central half of the
flat face). Mechanism: `t1_mats.py:1105` `projection='BOX'` — on the tail
|Nx| ≈ 1 so the flank tile samples on (y, z) and tiles, the identical failure
`t1_mats.py:1236-1250` documents and fixes for the nose.
**Fix:** a tail selector mirroring `_NOSE_SEL`, in `t1_mats.body_paint`.
**Risk:** three traps. (i) `_NOSE_SEL[0] = None` at line 1206 means the colour
branch takes its `else` path — a tail selector written in the same pattern lands
in the same dead branch. (ii) `_facex = GREATER_THAN(|Nx|, 0.70)` is true on the
tail as well as the nose, so a tail gate must also key on X < −1.60 or the nose
decal leaks aft. (iii) **The rear quarter has 20.9 % real gold** — a blunt
"no art aft of x = −1.6" would strip it and repeat the folk-art-coverage error.

### 3. All the glass reads as a mirror — sev 5 — UNVERIFIED (internally controlled ablation)
Rear pane CV **1.22 against the photograph's 0.24 (+408 %)**; windscreen 1.34
(+458 %). The interior is modelled and lit and is being overwritten by the rig's
specular. The panes are smooth-shaded, so the reflection is warped — 9.4× the
render-to-render null.
**Fix:** `t1_mats.py:459-467, 508-509` (glass roughness / specular IOR level /
transmission weight) and `use_smooth = False` on every polygon carrying `glass`
where the panes are created. Separately, the interior needs its own practical to
transmit toward, not the rig.
**Risk:** flat-shading is mesh data, not the loft — `verify.py` unaffected.
Raising transmission puts the galley bays through the glass and collides with
the bay work in item 12.

### 4. The lid is built flat — sev 5 — CONFIRMED, and larger than claimed; but see the caveat
Specialist 85 ± 25 mm; verifier **122 ± 16 mm**, from a stronger derivation. The
bow is proven real by an internal control: the lid's *longitudinal* bulb edge,
same detector, same image radius, near-identical chord, fits a straight line at
rms 0.51 px with max deviation 1.33 px, while the transverse edge deviates
23.08 px — **17× more bow on one than the other**, which no lens model explains.
It reproduces from the **panel silhouette alone** (line rms 7.90 vs quadratic
2.77, F(1,462) = 3313), so the "bulbs are hardware in a mid-conversion frame"
objection does not bite. The recovered sagitta vector lies along the panel normal
to a dot product of 0.998–1.000, so it is a crown and not a curved cut line.
Built: `t1_shell.py:476 _lid_panel` sets z = 0.0; `roof_z` crowns only
15.3–16.5 mm.
**CAVEAT THAT MUST TRAVEL WITH THIS:** a circular arc consistent with
`AUDIT_rev11`'s already-reported roof dome (0.19 ± 0.03 m off the drip-rail
gutter) implies ~79 mm over the central 1.110 m. **This may be a re-derivation of
that finding rather than a new one. Do not count it twice.**
**Fix:** *not* `_lid_panel` alone. Crowning only the lid leaves the closed lid
standing 70–106 mm proud of the roof on the centreline. It has to be
`t1_core.G(z)` with `_lid_panel` driven from `roof_z`.
**Risk: the highest in this report along with item 17.** `G(z)` is the shell
loft — the wheel arches are cut while the shell is a **closed solid** and would
move; every post-solidify aperture boolean moves; every UV shifts; the drip rail,
belt and gutter re-seat. `_roof_cutter` sizes its prism from
`min/max(roof_z) − 0.030 / + 0.060` and asserts `zlo > Z_HEAD + 0.020` — a
+100 mm crown blows through the 60 mm headroom. The roof cutter's own two-sided
guard already threw three false FAILs on its first run. And it interacts with the
rake: see item 5.

### 5. The rake and the roof warn pull the same way and must be re-fitted together — sev 4 — UNVERIFIED
`AUDIT_rev11`'s rake finding (14.4 ± 3.1 mm/m against 33.0 built) propagated
through `rake_drop(x)` at `X_AXLE_R`:

| pivot held | roof @ rear axle | residual vs 1.960 |
|---|---|---|
| built, 33.0 mm/m | 1.9225 | −37 mm (the current warn) |
| x = 0 held, slope → 14.4 | 1.9022 | **−58 mm** |
| `X_DROP_REF` held, slope → 14.4 | 1.8862 | **−74 mm** |

`verify.py` fails at 40 mm. **Applying the rake correction alone takes the guard
from warn to FAIL.** Conversely item 4's missing crown, added with the drip rail
held, raises `roof @ rear axle` by ~68 mm to ~1.99 — overshooting 1.960 by +30 mm.
**Fix:** `t1_core.G(z)` tail plus `t1_core.RAKE_DZDX`, re-fitted jointly against
`verify.py:36 H_ROOF`.
**Risk:** do not change the rake and the dome in the same commit without a plan
to attribute the residual, and do not change either alone.

### 6. The mural renders washed out — sev 5 — PARTIALLY CONFIRMED
The class-fraction statistic the specialist led with (dark 31.8 % → 2.9 %) is
contaminated: the mural renders at 8.2× minification, which destroys a dark tail
regardless of illumination. The **area-mean test settles it** — see §1 D. The
render's mean is displaced +21/+33/+46 *away* from the texture's own area mean,
which averaging cannot do.
**Fix:** shader side only — the `lidmural` material's specular/coat in
`t1_mats.py`, or the studio key's incidence on the lid. **Not `lid_gen.py`, not
`texgen.py`, not `tex/lidmural.png`** — the texture is measurably correct and
regenerating it would break the one thing that is right.
**Risk:** SPEC §10.9 locked the flank's beauty saturation as an outcome of the
rig, not a target, and refuted three suspects by measurement. Measure any change
on the **albedo**, not on the beauty pixel.

### 7. The cream rim is ~59 mm small and the blackwall ~29 % too deep — sev 5 — CONFIRMED, understated
See §1 B. rim/tyre **0.6612 ± 0.0060 against 0.5729 built, 14.7 σ**;
hubcap/tyre correct at 0.35 σ, so the rim is the odd one out. Cross-validated on
`ref_rear34.jpg` (hubcap/cream 0.614 vs 0.625 — 1.8 % apart). The cream's radial
shading *reverses* between r 32–37 and r 38–46, which requires two
differently-oriented surfaces — a dished disc plus a flaring flange.
**Residual doubt that changes the fix:** at 1024×768 a flange lip and a
whitewall's outer paint line look alike, and `t1_detail.tyre()` still carries
disabled whitewall vertices at r 0.2340/0.2905. Neither matches my measured
0.2195 m, which argues for the flange — but it is not formally excluded.
**Fix:** vertex tables in `t1_detail.rim()` and `t1_detail.tyre()`;
`t1_core.RIM_R` should then drive the geometry instead of being dead.
**Risk:** the bead and flange are coupled at r = 0.1880/0.1905 — enlarging the
rim alone opens a 25 mm gap all the way round, at the near front wheel, which is
the DoF focus point. The sidewall must be re-lofted in the same edit. **Do not
scale the hubcap.** `TIRE_R` does not change, so `verify.py`'s arch guard and
`TYRE_D` are unaffected.

### 8. Zero vignette, zero backdrop noise — sev 4 — CONFIRMED (measured by me directly)
Numbers in §1 E. A 4.9-megapixel field with **exactly zero variance** in all
three channels, 99.51 % of it exactly (255,255,255), with zero falloff to the
corners, is the cheapest CG tell in the frame and it covers 70 % of it. The noise
that *does* exist is render sampling noise at 6.9–7.9 in the dark glass — loudest
exactly where a viewer looks to check whether an image is real.
**Fix:** `post.py:93-103` needs a floor that does not scale to zero at white;
`post.py:81-90` needs to run where it can still do something.
**Risk:** grain on the backdrop contradicts SPEC §6's pure-white lock and
**must be agreed with the owner before anyone does it**. Raising samples for the
dark glass multiplies the six-strip render time.

### 9. The tail lamps are ~2× short and the wrong hue — sev 5 — PARTIALLY CONFIRMED
Height **0.151 ± 0.018 m** (verifier) / 0.159 ± 0.010 (specialist) against
**0.103 m** built — 1.9–2.2× short. The vertical extent is immune to horizontal
foreshortening, and the lamp is as tall as or taller than the whole plate frame
in the photograph while the build makes it 46 % of it.
Hue: lens **21.7°** by 20×20 block means (which annihilate 2×2 chroma
subsampling, so the JPEG attack fails), against adjacent body paint at
**12.4°** in the same frame under the same light. The lens is **8.5–13.4°
warmer** than the paint; built `ruby` at **0.9°** is *cooler* than it. The sign
survives any white-balance argument. `t1_mats.py:1433`'s existing `amber`
(hue 21.1°) would match.
**What falls:** the "oval, AR 1.60" claim is **not established** — an image AR of
1.46–1.60 is what a circle shows at local foreshortening 0.63–0.69, and the only
clean probe (a folk-art flower at w/h = 1.000) is a single blob. The "12.6° off
vertical" limb is **refuted** — the ellipse fit latched onto the gold swirl. The
width-ratio limb is **inadmissible**: it compares the lamp on the corner radius
against the plate on the flat face.
**Fix:** `build.py:334-338`; `t1_detail.small_lamp` is `T.revolve` and cannot
make an oval. Change the material to `amber` first — that half is free.
**Risk:** the lamp sits at x −2.1310, **23 mm aft of the body skin**, and
`verify.py` row 1 measures overall length across every mesh object. Grow it in
y/z, never fore-aft. A flat oval across the corner radius will float at one end
unless re-anchored by ray-cast.

### 10. The bulbs do not read as tungsten — sev 4 — UNVERIFIED
The luminance ratio is right (rendered 1.301 against 1.217–1.35 photographed).
Two things are not. Colour: core R−B **+12.9** against the photograph's **+64 to
+69**, on a surround already at +6.6 — so the render's bulb is only 6.3 warmer
than the cream it sits on. Gap **−51 ± 6, ≈ 8.5 σ**. And variance: **sd 0.66
code values across all 22 bulbs**. The photograph shows one bulb at ratio 1.35
and one at **0.87** in the same frame — a dead lamp beside a lit one.
**Fix:** the `bulb` material's emission colour, plus per-instance jitter and one
deliberately dead lamp.
**Risk:** warmer bulbs warm every adjacent cream surface by bounce, which touches
the galley work. Per-instance jitter touches the instancing item 11 audits.

### 11. Drip-rail bulb pitch is 4.7× too coarse — sev 4 — CONFIRMED
**28.8 ± 2.0 mm** measured against **134.62 mm** built (mesh: 27 bulbs, 20.9 mm
balls). FFT 6.15 px, autocorrelation 6.25 px, comb fits 5.895 / 5.940 / 6.335 px
at three stations, second harmonic at 3.08 px carrying 37 % of the fundamental —
the signature of round blobs at duty ~0.46.
**The JPEG-artefact control passes cleanly.** `ref_side.jpg` is SOF0 with 2×1
subsampling, so chroma blocks are 16 luma px. Measured power at 16.00 px = 279,
at 8.00 px = 226, at **6.15 px = 562**. The same comb fit on plain cream body at
four offsets returns 9.3–10.0 px at 2.2–3.1 DN contrast against 6.65 DN on the
rail. A second photograph at a different scale gives ≈29 mm independently.
**Fix:** `t1_detail.BULB_PITCH` / `BULB_R`.
**Risk:** 27 → ~106 instances on a string running the full flank, rendered at
3000×2000. At 29 mm pitch with ~13 mm bulbs the string is nearly continuous at
hero scale, so a shader may be cheaper than geometry. Downstream of every
boolean; no `verify.py` exposure.

### 12. Bay 2's galley contrast — sev 4 — CONFIRMED (but not as originally framed)
**Bay 2 is the defect: photo sd 23.90 ± 1.05 against render 13.52 ± 0.40, 9.2 σ,
and there is no man in bay 2.** Bay 1's apparent 8.1 σ gap is mostly the man
(§3). Bay 3's render at 20.27 already **exceeds** the photograph's 18.43 — so any
*global* galley-contrast lift makes bay 3 worse to fix bay 2.
**Fix:** `studio.py:154, 241` `fill_galley`. Its own comment records that it was
placed when "the galley is a closed 2.8 mm box lit only by EXTERIOR sources" — it
sits at y +2.35, outboard of the show flank, raking in horizontally. The source
that should light the galley is now the real roof hole.
**Risk:** `fill_galley` is `10.2 * key` in `lighting()` and a bare `10.2` in
`playa()`, so a change moves both rigs and every hero. A harder source through
the roof hole puts cast shadows on the counter top and the flank, and SPEC §10.4
locks the flank above 0.40 m clean to ±7 % — a budget item 18 shows is already
spent.

### 13. The model shows an 18 mm red strip along the whole counter — sev 4 — CONFIRMED (all four attacks failed)
`z_belt(x)` and the counter-top plane both carry the same `RAKE_DZDX`, so
`Z_BELT0 = 1.2355` sits **exactly 18.0 mm** above `CNT_ZT − rake_drop(x)` at
every station. Measured empirically in `out/p_side.png` on **47 of 61 columns**
from x +0.80 to −1.44: a red run 13.8 ± 1.6 mm of hard core, bottom +1.6 ± 1.0 mm
above the analytic counter plane, top −2.6 ± 1.2 mm below the analytic belt
plane, at (208,132,123), **R−G = 76** — paint, not shadow. In the photograph the
eight rows above the per-column brass top across 30 columns give **R−G 20–43**
everywhere. The gate fires on true body red under the counter at all six test
columns, so it is not a detection failure; the x 700/800 exclusion is honest
(steam table and dispensers); the brass-top location reproduces to 1 px.
**Fix — and this is the important part.** Do **not** move `Z_BELT0`:
`V_APEX0 + V_RISE == Z_BELT0` is an asserted identity and `Z_BELT @ x=0.864 =
1.2070` is a locked `STATE.md` row, and the break is photographically visible and
*correct* forward of the counter. Do **not** move `CNT_ZT`: SPEC §10.5 lock, and
`CNT_NOSE_F` is a *fraction* of the slab edge so it would silently thicken the
brass nosing by 17 %. **Clamp the shader break to
`min(z_belt(x), counter_top(x))` over x ∈ [`CNT_X1`, `CNT_X0`] in `t1_mats.py`.**
Shader-only, no geometry, no lock touched.

### 14. The hero is framed backwards — sev 4 — CONFIRMED (measured by me directly)
Lead room **5.9 %** on the nose side against **20.8 %** trailing — a 1 : 3.53
inversion where convention gives the larger margin to the direction of travel.
The nose sits 177 px from the frame edge, inside the margin a photographer would
leave even for a static subject. Tonal centroid at 0.437 W / 0.543 H, near
neither third. *This is the one item judged against professional practice rather
than the source photographs, and it is flagged as such.*
**Fix:** the `hero34f` camera target in `studio.py`.
**Risk:** **do this last.** `hero.py` renders six stitched strips; moving the
camera re-cuts every strip boundary, re-runs SPEC §10.14's seam handling, changes
the DoF geometry, and **invalidates every measurement in this report that is
expressed in hero pixel coordinates.**

### 15. The T-handle is on the wrong side of the plate — sev 4 — CONFIRMED
Photograph: a chrome object **205 mm below** the plate centre (specialist
197 ± 15, 0.5 σ), aligned with the plate centre to 2.7 px on a 99 px baseline.
Above the plate, over x 985–1200 × y 540–628: **max L = 95, zero pixels with
S < 0.45 ∧ L > 70**, examined stretched. Built at z 1.0631 against a plate centre
at 0.8232 — **240 mm above**. Projected into the photograph, the built handle
lands at y 564–577, where the photograph shows a **shut line** (V 74 against a
local mean of 102). The identification of the object below does not need to
succeed: the build's handle location is measured to be empty red paint.
**Fix:** `t1_detail.py:1289` z. **Do not change its x** — it is the rearmost
object in the scene at −2.1384 and `verify.py` row 1 measures length across every
mesh; the docstring records it alone raising a warn at 43 mm proud.
**Open, and it cuts both ways:** projecting the tail face's width forward puts the
vehicle centreline at u ≈ 1222 ± 30, off the right edge of frame — so the plate
may genuinely be mounted off-centre, which the build does not model either.

### 16. The "1963" plate frame is too tall for its width — sev 4 — CONFIRMED
Image AR **1.674 ± 0.05** (verifier, saturation-crossing classifier) against the
specialist's 1.71 ± 0.04 — 0.6 σ, from a completely different classifier. The
built outer AR is **1.4765**. **At c = 1 the built frame is already 13 % too
tall, and c < 1 is guaranteed**, so the scale-free limb is unbreakable.
De-foreshortened over the admissible range: **+31 % to +66 %**. Rails: measured
top 22 ± 4 mm and bottom 23 ± 3 mm against built 38 mm and 18 mm. The surround is
empty in both, correctly. *Note: the specialist's "c ≤ 0.96" upper bound is
geometrically impossible; every VP candidate caps c at 0.78–0.89.*
**Fix:** `t1_detail.py:1196, 1219-1222`.
**Risk:** the digits are positioned off `PLATE_Z + PLATE_H/2`, so they move; the
top rail shrinking 38 → ~22 mm will no longer fit 21 mm digits, which must be
rescaled in the same edit. And item 9's height ratio uses this frame as its
denominator — **do not apply 9's ratio evidence and 16 together without
recomputing 9's denominator.**

### 17. The tail is 195–300 mm too long — sev 4 — CONFIRMED on its primary limb; two supporting arguments inadmissible
Specialist −201.0 mm; verifier **−195 ± 13 mm** orthographic, from its own hub
fit (rear rim circle fit (749.37, 607.11), R 44.67, sd 2.38, n = 88), its own
silhouette (rearmost body pixel **921.5 ± 1.5** by sub-pixel saturation crossing)
and its own mesh probe. Stated as an overhang past the rear axle, rule 6's
+100 mm conversion **cancels entirely**: photo 0.813 ± 0.013 m against model
1.0080 m. Four independent tests put the fore-aft VP on the nose side, confirming
the tail is nearer, and under a finite VP the cross-ratio gives 0.751 / 0.727 /
0.673 m — so **0.813 is an upper bound and the gap is plausibly 250–300 mm.**
**Two limbs are struck out and must not be repeated:** the "nose right to 0.7 mm"
agreement and the overall-length cross-check both take their front endpoint from
`x_img = 65 ± 8` — **that is the lamppost**, columns 62–79. Both inadmissible.
Neither is load-bearing; the tail claim rests only on the rear hub, the tail
silhouette and the shared wheelbase.
**Risk — the highest in this report.** It is a loft change and it endangers most
of the load-bearing order. The aft station set must be **re-spaced, not
translated**. The rear arch spans −0.738 → −1.690; at the new tail it is
**217 mm** from the aft skin instead of 418 mm — and the arch boolean is the one
cut made while the shell is a closed solid. Every post-solidify aperture is
positioned in absolute x. Every tail detail (`plate_1963` −2.1070,
`englid_handle` −2.1384, `tail` −2.1040) is left floating in air. Step 8b's shear
changes the drop at the tail by 6.6 mm, perturbing every locked height there.
And the counter's rear end already overhangs by 111 mm; after the fix it
overhangs by **312 mm**, which must be adjudicated, not absorbed.
**Do not apply this as a translation. Apply it last, with the counter, and
re-verify at both subdivision levels.**

### 18. Counter fascia speckle ~5× — sev 3 (downgraded) — PARTIALLY CONFIRMED
The specialist's 8.7× is inflated: their render box is **58.4 % body red and
12.4 % gold folk-art**, only 26.9 % cream. Properly relocating the fascia per
column and matching scale gives **4.06 %** (p25 3.09, p75 4.75) against the
photograph's **0.78 %** (p25 0.62, p75 1.58) — **≈ 5×**, still far above the
~0.5 % JPEG/optics floor. Re-encoding the scale-matched render at JPEG q88 4:2:0
gives 4.04 %, so compression does not explain it; native scale gives 3.61 %, so
the downsample does not either.
**Risk:** `AUDIT_rev11` found sun fade is keyed on Normal.Z and gives every
vertical surface exactly zero — so whatever streaks this vertical fascia is a
*different* node, and turning down a global weathering amount would strip wanted
weathering off the horizontals. **And do not tune against the 7.24 % figure or
its box** — it is 58 % body red, and a fix driven by it would flatten folk-art
and grime the photograph *does* have.

### 19. The louvre block is ~100 mm too far aft and 57 mm too long — sev 3 — UNVERIFIED
Pitch is right (20.7 ± 0.6 mm against 21.1 built, 0.7 σ) and the slot heights are
right. The block's ends are not: measured forward end **−1.193 ± 0.030** against
built −1.2850, aft **−1.520 ± 0.035** against −1.6700; length 0.328 ± 0.020
against 0.385. The build used `REF_MEASUREMENTS`' numbers **without rule 6's
+100 mm conversion** — REF's own corrected forward end (−1.173) agrees with the
measurement. Slot count 11 certain against 10 built. Rake measures **−0.5° ± 0.6°**,
which **vindicates the build's horizontal call** and refutes the "+3.9°" in its
own comment at ~3 σ. Profiles were de-skewed by a fitted +0.030 ± 0.010 px/px
first; without that the pattern phase-flips over 40 px, which is why `a21` and
`a22` lost the block ends.
**Risk:** `T.flank_y()` is stated accurate to 0.1 mm only over z 0.884–1.091, and
an 11th slot at 1.1063 leaves that band with only 2 mm of `LOUV_OFF` — the sweep
can sink into the flank. `fuel_flap` is anchored to the block and moves with it.

### 20. The hubcap emblem has no ring, and its VW is fused — sev 4 — UNVERIFIED (mesh-derived, so the fusion is certain)
The photographed emblem is a cream **ring** enclosing the V-over-W at
**0.323 ± 0.018 of the cap diameter**, stroke 0.026–0.034 of it, legible in the
raw pixel dump and confirmed as an ellipse-projected ring in `ref_rear34.jpg`.
`t1_detail.cap_emblem()` returns two prisms and nothing else; the only ring
objects in the scene are the nose roundel's.
Separately, from the mesh: the hubcap's V and W overlap by **13.05 mm on a
52.41 mm glyph — 24.9 %** (nose: 38.02 on 158.26 = 24.0 %). Closed form:
`overlap = R·(1.885·(w/R) − 0.015)`, zero only at w/R = 0.00796; the hubcap runs
0.2087 and the nose 0.1986. Predicted 13.06 and 37.7 mm against a mesh 13.05 and
38.02. **The docstring's "clear 12.7 mm air gap" is arithmetically impossible at
any plausible bar width** — this confirms `AUDIT_rev11` and shows the hubcap is
the worse of the two in relative terms.
**Honest limit:** the *fact* of the overlap is certain from the mesh; the correct
spine geometry is **not measurable** — the reference emblem is 19 px across.
**Risk:** `vw_bars` is shared by the nose roundel and all four hubcaps; a spine
change moves both, and they use different `w/R`. Tie the cap glyph to its ring the
way `build.py:382` ties the nose glyph to `ROUNDEL_D`, or it will drift again.

### 21. The rear arch was not applied, and its shape is wrong — sev 4 — UNVERIFIED
**Answer to the yes/no: NO.** `ARCH_R = 0.3735` is unchanged and the mesh gives a
0.747 m aperture. Independent floor from a livery mask: **0.875 m**, consistent
with `AUDIT_rev11`'s 0.881–0.933. Gap −128 to −186 mm.
New: the built arch is a circle **concentric with the wheel**, so its gap is
41.0 mm at every angle; the photograph gives **34–38 mm at the crown and
109–121 mm at ±60°**. The arch flares and the build does not.
**Risk:** the arches are cut **before** solidify, while the shell is a closed
solid — the only cut in the pipeline with that property. Widening also moves
`_ARCH_TOP_F`, guarded by an assertion at `t1_shell.py:286` that exists because a
shut line crossing the arch lip **collapsed the shell from 205 562 v to 12 v at
SUB=2** for six revisions. Re-verify at SUB=2, not only SUB=1. It also interacts
with item 17 — after a tail fix the rear arch is 217 mm from the aft skin.

### 22. The tyres do not deflect — sev 3 (downgraded from 5) — PARTIALLY CONFIRMED
The phenomenon is real and survived every attack: the boundary above it is
tyre-dark only between x ≈ 712 and 788 and reads L 45–77 outside, the pavement
below reads 97–128, and the dark disc's chord at y 665–666 implies R = 70.2–70.9
about the same centre — a ~70 px circle truncated at y ≈ 668.5.
The **magnitude falls**: **23 ± 4 mm**, not 35 ± 6. The specialist's fixed
L-band mask (0.070–0.215) is a different edge criterion on every background — it
expands the tyre against the dark arch cavity and shrinks it against the bright
pavement, and both errors inflate the deflection by about 2 px. The claimed
"flat to ±0.35 px" is also not defensible: a 1.4 px systematic bow is measurable
along the same span. And the standing 27 ± 9 mm figure is **not independent** —
it shares the photograph, the red-dome centre and the ground line.
**Risk, and it is why this is not a quick win.** `t1_detail.tyre()` is
`T.revolve(..., axis='Y')` — axisymmetric, so a contact flat **cannot be authored
in the profile at all**. It needs a post-placement vertex deformation on the 24
wheel parts, which step 8b already skips, so a new step would have to run after
8b and be explicitly exempted from it — a new ordering constraint in the most
load-bearing part of the pipeline. Worse: `verify._measure_wheels()` derives
`TYRE_D` as max(z) − min(z) and `audit.py:322` checks it against 0.665 ± 0.015. A
23 mm flat gives 0.642 and **trips that guard**, taking `verify.py` off 0 fail.
The guard would have to change in the same edit.

### 23. Glazing on the off flank that may not belong there — sev 4 if confirmed — NOT MEASURABLE (see §4)
`glass_bay0_R / 1_R / 2_R` are three specular panes on −Y, opposite the three
confirmed-glassless serving apertures on +Y. In a front-3/4 render they carry
sd 28–31 against the surrounding cream's 9.6 — **3× the local contrast**,
reading as bright specular slabs. If the off side is "solid cream sheet metal" as
the owner described the +Y side, these are glass in a wall with no aperture,
which is worse than glazed apertures.

### 24. Two `STATE.md` rows measure the wrong objects — sev 4 — UNVERIFIED (code-derived, certain)
See §1 C. `audit.py:308`'s exclusion tuple omits `counter_top`.
**Fix:** add `"counter_top"`, or filter on `o.name.startswith("counter")`.
**Risk:** none to geometry — but it will *remove* a standing "OUT" from
`STATE.md`, which will read as a regression fix to anyone who does not read the
diff. And item 17 couples to it: `CNT_X1` was deliberately set against the
model's *wrong* tail, so a correct overhang metric and a tail fix must land
together.

### 25. Smaller confirmed gaps — sev 2–3, all UNVERIFIED
* **Engine-lid shut lines.** The photograph resolves **two** parallel horizontal
  lines across the whole visible tail, at z 1.062 ± 0.020 and z 1.015 ± 0.020,
  separated by 46 ± 4 mm. The build has one, at z 1.153 — **+91 mm too high** —
  and the second is absent entirely. `GAPW = 5.5 mm` is **not refuted**; the dark
  line's FWHM is 4–5 px ≈ 11 mm, below what the photograph can resolve. Prefer a
  swept crease to a second cutter — the gap booleans run after solidify and
  collapsed the shell at SUB=2 for six revisions.
* **Plate legend.** The source resolves **four light masses at 36 ± 4 mm pitch**
  over a 0.152 m span, with **no glyph topology at ×20** — no closed counters, no
  stroke junctions. The build renders a seven-segment typeface at 21 mm pitch
  over 0.0656 m. Under the absolute-replication requirement, rendering a specific
  legible typeface where the source resolves an illegible smear is itself the
  finding. Span is 2.3× too narrow; digit *height* matches.
* **Rear glazing.** `ref_rear34.jpg` shows **two** apertures in the rear panel —
  a glazed window with a 17 ± 3 mm seal whose bottom edge sits at z ≈ 1.835, and
  a separate open serving aperture below it with the galley visible through.
  The build has one, glazed, at z 1.3163–1.6485 — i.e. at the *serving*
  aperture's height. There is no `seal_rear` in the inventory. The seal's colour
  is measured and it is **not black**: RGB 83.6/74.5/50.8 at saturation 0.41
  (lower run), 129.0/103.1/61.7 at 0.56 (upper) — chalked, sun-bleached rubber.
* **One strut of two; no hinge hardware at all.** `ref_rear34.jpg` shows two pale
  posts on the opening's off-side lip at model X ≈ −0.08 and −0.78 with a bright
  rod between them. The 182-object inventory contains no hinge; the lid is hinged
  by a coordinate transform. `lid_rail` exists only at the two ends, not down the
  free edge where the workshop frame shows a continuous rail.
* **`lid_board` is inset 30 mm on all four sides**, framing the mural in body
  paint. At 11× the photograph's yellow strip runs to a single 1.6–2.0 px line
  and then to background — artwork-to-edge gap **0 ± 11 mm**. *This also answers
  the open "skin or carried board" question: no board is carried proud — no edge
  thickness, no shadow line, no plane break. The build's flush board is not
  contradicted; the inset is.* At inset 0 the decal z-fights at grazing angles,
  and it must follow item 4's curvature — the two are coupled.
* **An unmodelled cream box stands on the roof** at the opening's forward end,
  X +1.00 → +0.44, 0.35–0.45 m tall, with two dark circular faces. Nothing is
  modelled there. It also occludes the opening's forward station (§4).
* **`lid_gen.py:954` draws literal `a`,`n`,`t`,`a` glyphs** after the legible
  "La S". The panel reads "La S" and no further; `lid_gen.py`'s own text says
  *"'La Santa' remains CONSISTENT and remains UNREAD. Do not report it as
  verified."* Currently dark — `t1_shell.signboard()` returns empty unless
  `T1_SIGNBOARD=1` — so **no shipped render contains the invention**. But
  `tex/lidsign.png` is committed with it baked in. Latent, sev 4 if re-enabled.
* **The rear-quarter curlwork is drawn as 5 masses; 13 are measured** (carrying
  92 % of the ink). Colour and stroke weight are correct — do not touch those.
* **Bobble fringe pitch 26.1–26.8 mm built against 31.1 ± 1.0 mm measured**
  (−16 %), 17 balls per bay against 13–14. Menu-card stripe pitch 8.1 mm built
  against 19 ± 5 mm measured (~2.2× too fine, aliasing to a grey wash at render
  scale); card width −6.6 %.
* **`COUNTERTAN` hue** built at 42.3° / sat 0.254 against its own cited 29–37° /
  0.33–0.39 and an independent 28.4° / 0.333.
* **The hubcap dome renders pale pink** — saturation ratio to the body red in the
  same frame 0.354 (hero) and 0.446 (ortho) against **0.899** photographed.
  Flagged as a **lead, not a settled measurement**: a dome and a flat flank are
  the same material class but not the same geometry. An A/B at `capred` roughness
  0.165 vs ~0.28 would settle it.
* **Chromatic aberration ~2–4× too strong.** The model is *correct in kind* — a
  true per-channel radial scale about the optical centre, not a smear. But
  `0.0011 × r` puts **3.96 px of R–B separation at the corner** of a 3000 px
  frame where a good 78 mm prime gives 1–2 px. `corr(R−B, radial luminance
  gradient) = −0.885` over 10 422 outer-field edge pixels confirms the mechanism
  is present and coherent.
* **The studio's only contact shadow rides on a Blender default.** All seven
  softboxes carry `is_shadow_catcher = True`; a freshly created LIGHT object
  defaults to True in 4.5.3 while a MESH defaults to False, and the RNA default
  is False. Nothing in the repo sets it — the only assignment anywhere is
  `studio.py:100` on the cyclorama. Clearing it on the lights takes ground alpha
  from mean 0.1070 to 0.0036, with **98.85 % of ground pixels going to exactly
  zero**. **This is a hazard note, not a fix request**: set it explicitly, with a
  comment, so the behaviour is chosen. Setting it *False* deletes the shadow.

---

# 3. DO NOT RE-OPEN

Each of these fell to an independent second measurement. They will be raised
again if this section is not read.

### `optics-6` as written — "the vehicle floats, the catcher writes no alpha"
**Both founding measurements are inadmissible.** They were taken in an
orthographic view where the ground plane is exactly edge-on. The shipped hero has
a contact shadow reaching **150/255** and covering roughly a metre of ground.
The *mechanism* limbs survive and are item 1 above; the conclusion does not.
Do not "fix the floating vehicle" — there is no floating vehicle to fix.
And do not re-propose `T1_CATCH=0`: already refuted, and now explained — it works
by moving the sweep off the alpha path onto a surface at linear ≈0.8 where the
curve still has slope, at the cost of defect D3 and SPEC §6.

### Bay 1's galley contrast, and the "achievable ceiling"
The rev-12 ceiling of ~23 **is** an arithmetic error — that limb stands
(`38.0 × 0.6358 = 24.2` applies a variance fraction as an sd fraction). But the
replacement ceiling of 29.4–32.6 is worse, and the reason is decisive:
**the man in the hatch is wearing a white shirt.** Every mask offered caught skin
only. At column x = 400 the profile is bright 167–198 / dark arm 101–143 / bright
157–212 — an arm in front of a torso — and **98.9 % of the 370 pixels in bay 1
above 210 DN lie at x ≥ 364**, on that torso. Masking arm, hand and torso
(81.7 % of the window) gives **sd 18.50 ± 2.02**; iid-resample inpaint 18.48;
mirrored-strip inpaint 18.76. That is **below the ~23 the finding attacks.**
Bay 1's render at 15.1 is then ~1.7 σ short, not 8.1 σ. Chasing bay 1 to sd ≈ 30
would be a ~60 % over-correction.
Also: the rev-12 window overhangs the aperture by 5 rows top and 4 bottom; clipped
to the interior, its "man-free forward third" drops from 28.61 to **20.91** — the
28.6 was aperture-frame contrast (dark cut edge plus bright bead), not galley.
And **bay 3's photo sd does not reproduce** — 18.43 ± 1.43, not 21.81; the render
at 20.27 already exceeds it.
**What survives: bay 2, at 9.2 σ, with no man in it.**

### Large bulbs around the lid perimeter (D4a)
**Refuted.** Its primary dataset is `ref_workshop.jpg`, a mid-conversion frame,
and bulbs are hardware — barred. Its claimed in-service corroboration in
`ref_rear34.jpg` fails on a scale-free test: that rail's dominant along-axis
period is 6.82 px with 4–5 px dots, ≈38 bulbs on the run, **7.6× more bulbs than
the workshop edge of the same panel**. It is the fine drip-rail string (item 11),
not ten 55 mm lamps. The lid's other visible perimeter in service is a painted
yellow menu border. **No in-service frame shows large perimeter bulbs anywhere.**
Adding them would put large wrong hardware on the most visible edge of the hero,
from a barred source — the exact shape of the `livery-9` failure.

### The tail lamp's oval shape and its 12.6° tilt
The **size and the hue survive** (item 9). The **oval does not**: an image AR of
1.46–1.60 is exactly what a circle shows at local foreshortening 0.63–0.69, and
the only clean foreshortening probe is a single folk-art flower. The **tilt is
refuted** — the ellipse fit latched onto the gold swirl on the left and drifted
its centre by 15 px. The **width ratio (0.428 vs 0.312) is inadmissible** — it
compares a lamp on the corner radius against a plate on the flat face.

### The tail-length finding's nose agreement and its overall-length cross-check
Both take their front endpoint from `ref_side.jpg` `x_img = 65 ± 8`. **That is
the lamppost** (columns 62–79). "Right to 0.7 mm" is an agreement with a
lamppost. Neither is load-bearing, and the tail claim stands without them — but
they must not be repeated as evidence. This is the third time this post has
produced a confident wrong number.

### `materials-5`
**Closed.** Settled with a number and a positive control — see §1 A. Remove it
from the open list.

### "Small bulbs around each serving aperture"
**Refuted.** Ring elements read L 236 against flank cream at 215 — a ratio of
1.10 where a lit filament against daylit cream reads 3–10×. They are fabric
bobbles.

### The louvre block's "+3.9° rake"
**Refuted at ~3 σ.** Measured **−0.5° ± 0.6°** in the body frame after de-skew.
The build's horizontal call is right; the comment is wrong.

### `gal_ceiling`'s `visible_glossy` as the cause of the mirrored rear window
**Refuted for the rear pane specifically.** Turning it off moves the pane by mean
1.87 code values, *below* the 4.19 render-to-render null. `gal_ceiling` is still
a light blocker (item in §2/§5) — but it is not what the rear window is
mirroring. That is the rig.

### Step 8b invalidating `gal_ceiling`'s 45 mm standoff
**Refuted.** The shear is applied identically to every non-wheel mesh, so a
same-x z difference is preserved exactly. The standoff is real: 44.9–46.9 mm.

### The claim that `gal_ceiling`'s effect is inside the noise
**Refuted.** A seed-paired four-render noise floor gives 0.1–1.7 DN (median 0.48)
in the window band, against a deletion effect of +30 to +36 DN locally. The
effect is 5–100 σ above the floor. *But note the honest caveat in §5: deleting
removes the blocker* and *the emitter the bays were tuned against, and
`t1_detail.py:1670-1690` already prescribes exactly this fix. D3 is true and is
not news.*

---

# 4. NOT MEASURABLE

Marked as such deliberately. No number was invented for any of these.

| # | quantity | why | what would settle it |
|---|---|---|---|
| 1 | **The off (−Y) flank — everything, including whether `glass_bay*_R` should exist** | No photograph shows the off side. `ref_side` and `ref_rear34` are both the serving flank; `ref_workshop` is nose-on and mid-conversion. | **Any in-service frame of the off side.** One photograph closes item 23 outright. Failing that, an owner statement in the same terms he used for the +Y side. |
| 2 | **The counter's outboard projection** (built 294 mm proud) | `ref_side.jpg` is an elevation and the counter-top/flank boundary carries **no step** — saturation ramps monotonically with max \|dS/dy\| = 0.070 against 0.32 at the gold band's own edge. It is a bounce-light ramp, not an edge. | A camera-pose solve on `ref_rear34.jpg` (it has both vanishing directions and the tail's locked 1.750 m width for cross-vehicle scale). Or any frame showing the counter's front end face. |
| 3 | **`COUNTERTAN`'s level** (still bracketed −16 %/+15 %) | The tie-break needs a same-light, same-class, **horizontal**, unclipped reference. The only candidate — the napkin dispensers standing on the counter — **clips**: 22.5 % of the top face and 34.6 % of the front face at ≥ 248. In `ref_rear34` the cream flank clips at 37.7 % and the fascia at 50.6 %. | A frame of the counter with a grey card or any known-reflectance surface lying **on** the counter top, exposed so nothing clips. |
| 4 | **Whether the windscreen is split or one-piece** | The cab door is open 49° across the relevant columns of `ref_side.jpg`; a column scan does not isolate a centre divider. The build has two panes. | **`ref_workshop.jpg` at the screen aperture** — that frame shows the bare aperture with no hardware, so a divider or its absence is unambiguous. A crop is prepared at `measure/e_ws_screen.png`. **Do not settle this from the VW catalogue.** |
| 5 | **Lens haze on `amber`, `ruby`, `lens`, `reflector`** — i.e. whether their constant roughness is a defect | Not measured. Reasoned only, and reasoning is not evidence here. | `ref_rear34.jpg` at the amber lamp: specular-peak ÷ diffuse-body ratio, radially from lens centre to rim. Flat ⇒ constant roughness defensible; rising at the rim ⇒ not. Crop at `measure/e_ref_tail_zoom.png`. |
| 6 | **The roof opening's forward station** | `ref_rear34.jpg` is the only frame with roof elevation, and the unmodelled roof box (§2/25) occupies image x 592–635 — precisely the forward end. Bracketed only to X ∈ [+0.44, +1.06]; `LID_X0 = +0.964` is consistent but unconfirmed. | An elevated view from the **off** side, or a rear three-quarter from ~2 m higher. |
| 7 | **The engine lid's width, its left/right shut lines, the rear-lamp count, the plate's lateral position, the far half of the tail face** | All beyond `ref_rear34.jpg`'s right frame edge at x 1200, or not separable from the body's corner tangent at x 981. | **A square-on rear elevation**, or any rear three-quarter from the off side. |
| 8 | **The front wheel — arch crown gap, aperture width, lip section, tyre deflection** | The man covers 33 % of the front-wheel window and his red shirt defeats a red-livery mask on principle; columns 214–234 return no livery pixel at all. `ref_workshop.jpg` shows the arch unoccluded but the vehicle is on a cradle, unloaded — a different stance. | A left broadside with nobody in front of the front wheel. |
| 9 | **Whether the wheel's cream annulus is a rim flange or a wide whitewall band** | At 1024×768 a flange lip and a whitewall's outer paint line look alike. The shading reversal favours the flange but does not settle it. **This changes the fix for item 7** — flange means re-loft; whitewall means a painted band. | A close-up of either wheel taken normal to the wheel plane. |
| 10 | **The correct VW spine geometry** (item 20) | The reference emblem is 19 px across. The *fact* of the overlap is certain from the mesh; the correct proportions are not recoverable. | Any close frame of a hubcap, or of the nose roundel at ≥ 4× present scale. |
| 11 | **Menu-card printed text; plate legend glyphs; drip-rail bulb diameter; tail-lamp bezel section; shut-line gap width; apron roll radius; fuel flap (it is on the −Y side)** | All at or below the photographs' resolution limit — 1.5 px per word, no glyph topology at ×20, 2–3 px in a 4:2:2 JPEG, 2–3 px of blown chrome, FWHM ≥ 11 mm, underside in shadow, wrong side of the vehicle. | Close frames of each; the drip rail needs > 600 px/m. **The build is right to decline to invent these — except the plate legend, where it does not decline.** |
| 12 | **Whether item 4's crown is lid-specific or the already-reported roof-dome deficit** | No photograph shows this vehicle with the lid **closed**. | A frame with the lid closed, showing the roof in transverse elevation. |

### The one photograph that would pay for itself

Unchanged from `AUDIT_rev11`, and this pass adds to its list rather than
shortening it: **a left-side broadside, cab door shut, nobody in front of the
front wheel, square-on from as far back as the space allows.** It settles
tumblehome, the front arch, absolute height, the belt line, a clean second
derivation of the rake and the tail, the whole front wheel (items 21, 22), and
the rim-versus-whitewall question that decides how item 7 is fixed.

This pass identifies a **second** photograph worth almost as much:
**a square-on rear elevation, or any rear three-quarter taken from the off
side.** It settles the engine lid's width and shut lines, the rear-lamp count,
the plate's lateral position, the far half of the tail face, the roof opening's
forward station, the hinge count, and — critically — **whether the off flank
carries glazing at all**, which is the only thing standing between item 23 and a
verdict.

Asking for those two photographs is worth more than any amount of further
inference on this project.

---

# 5. THE ORDERED WORK LIST

Sequenced so that nothing later invalidates something earlier. The ordering rule
used: **metrology before pixels, shaders before compositing, compositing before
lighting, lighting before detail geometry, detail geometry before the loft, and
the camera absolutely last** — because every measurement in §2 that is expressed
in hero pixel coordinates dies the moment the camera moves.

**Phase 0 — metrology and the branch, before anything is measured again**
1. Merge the two audit-line fixes (`SCR z1` → 0.9896; delete `_NOSE_SEL[0] = None`
   at `t1_mats.py:1206`). Nothing downstream is trustworthy while the nose renders
   as black marks and the script is squashed 15.8 %.
2. `audit.py:308` — add `counter_top` to the exclusion. Two `STATE.md` rows are
   currently false, one of them a phantom 293 mm failure (item 24).
3. `studio._softbox` — set `is_shadow_catcher` explicitly with a comment. Behaviour
   unchanged; it stops the studio's only contact shadow riding on a default.
4. Close `materials-5` in the SPEC open list. Record that `optics-6` as written is
   inadmissible and why.

**Phase 1 — shader and material only, no geometry, no rig**
5. Tail selector to stop the flank tile printing on the tail face (item 2). Highest
   visible-defect-per-line-of-code in the report. Watch all three traps.
6. `ruby` → `amber` on the tail lamps (item 9, the free half).
7. Clamp the two-tone break to `min(z_belt(x), counter_top(x))` over the counter's
   span (item 13). Shader-only; touches no lock.
8. The `lidmural` additive lift (item 6). Measure on the albedo, not the beauty pixel.
9. `bulb` emission colour + per-instance jitter + one dead lamp (item 10).
10. `COUNTERTAN` hue to its own cited measurement (item 25). Level stays bracketed.
11. Glass: transmission up, specular IOR level down, and **flat-shade the panes**
    (item 3). Do this before the rig work — it changes what the rig has to do.

**Phase 2 — compositing and post, after every shader change**
12. `post.bloom`'s threshold, for display-referred input (item 1). This is the
    single biggest change to how the hero reads, and it re-values every pixel
    measurement taken before it.
13. Then the vignette (item 8) — it cannot be evaluated until 12 lands.
14. Then the grain floor (item 8) — **put the backdrop question to the owner
    first**; grain on the sweep is a change to SPEC §6's pure-white lock.
15. Halve the CA coefficient to ≈0.0005 (item 25).

**Phase 3 — lighting and the rig**
16. Delete `gal_ceiling` and re-solve `GAL_SKY` / `GAL_LUM` / `fill_galley`
    **in one commit**. A partial application blows the bay levels past their
    photographically-solved targets by +20–30 % locally.
17. Re-aim `fill_galley` to light through the real roof hole, targeting **bay 2
    only** (item 12). Bay 3 already exceeds the photograph; bay 1's remaining gap
    is ~1.7 σ. Re-measure all three after, and re-shoot the hero and all three
    ortho probes together or the audit trail decouples.

**Phase 4 — detail geometry, all downstream of every boolean**
18. Rim and tyre re-loft together (item 7). Do not scale the hubcap.
    **Settle the flange-versus-whitewall question first (§4 #9)** — it decides
    which fix is right.
19. Hubcap ring + tie the glyph radius to it; then the shared `vw_bars` spines
    (item 20), accepting that the spine proportions are not measurable.
20. Plate frame height and rails, with the digits rescaled in the same edit
    (item 16). **Then** recompute item 9's height ratio against the new denominator.
21. T-handle z (item 15). Change z only; never x.
22. Tail lamp geometry (item 9) — y/z only, re-anchored by ray-cast.
23. Louvre block ends and slot count (item 19); `fuel_flap` follows.
24. Drip-rail bulb pitch (item 11) — consider a shader over 106 instances.
25. `lid_board` inset → 0 (item 25). **Hold this until phase 5** if item 4 is
    going ahead — a flat decal on a crowned skin floats up to 122 mm at the centre.
26. Second lid strut, hinge hardware, the free-edge rail, the roof box (item 25).
27. Plate legend → four soft raised masses at 36 mm pitch, not a typeface (item 25).
28. Rear glazing: raise the window, add the second aperture and a rear seal in the
    measured warm-brown (item 25). Verify at **both** subdivision levels.
29. Engine-lid shut line down 91 mm; second line as a swept crease, not a cutter
    (item 25).

**Phase 5 — the loft. One at a time, each with a full two-level verify.**
30. **Roof crown + rake, re-fitted jointly** (items 4 and 5). Neither is safe
    alone: the rake alone takes the guard from warn to FAIL; the crown alone
    overshoots by +30 mm. Before starting, settle whether item 4 is a
    re-derivation of the existing roof-dome finding — **do not apply it twice.**
31. Rear arch width and profile (item 21). Cut before solidify, on the closed
    solid, past an assertion that exists because this collapsed the shell at SUB=2
    for six revisions.
32. **Tail length, last** (item 17), as a re-spaced aft station set — never a
    translation — with `CNT_X1`, `plate_1963`, `englid_handle` and the tail lamps
    moving in the same commit, and the counter overhang adjudicated rather than
    absorbed. After it lands, item 31's rear arch sits 217 mm from the aft skin
    instead of 418 — so 31 must be re-verified after 32 even though it ran first.

**Phase 6 — the camera, after everything**
33. Re-frame `hero34f` for lead room (item 14). Consider f/11–f/16 for a product
    hero rather than f/8 focused on the front arch. This re-cuts every strip
    boundary and invalidates every hero-pixel measurement in this report — which
    is exactly why it goes last.

**Not on this list, deliberately:** tyre deflection (item 22). It is real at
23 ± 4 mm, but it cannot be authored in an axisymmetric revolve, it needs a new
pipeline step after 8b with its own exemption, and it trips `audit.py:322`'s
`TYRE_D` guard — which would have to change in the same edit. That is a coupled
change of exactly the kind this project's history warns about, for a 23 mm
effect. Park it until the loft work in phase 5 is finished and stable.

---

## Working files

Everything this audit produced lives in `measure/` (probe scripts, crops,
overlays, per-agent working files under `a_*`, `b*`, `c/`, `d_*`, `e_*`, `v1_*`,
`v2/`, `v3_*`, `v4_*`) and `out/` (renders, gitignored). `measure/AUDIT_RULES.md`
carries the brief every agent was held to. `AUDIT_rev11.md` sits at the repo root
as an untracked reference. **Only this file is committed.**
