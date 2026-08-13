# HANDOFF rev 14 — 2026-08-13

> **THE STANDARD, in the owner's words, and it governs every line below.**
> The final product should be nearly indistinguishable from the original.
> **Any single measurement off is unacceptable.** We are recreating a photo
> realistic version of **that exact bus** — not a 1963 T1, not a generic
> taqueria combi. The criterion is PER-MEASUREMENT, not on average: a model
> right in ninety places and wrong in one is not 99 % done, it is wrong,
> because he will look straight at the one.
>
> And above clinical accuracy: *"I really want this to give the person the
> opportunity to feel like they were on Playa del Carmen all those years ago.
> I want the owner to remember standing in the kombi, in this very picture
> that was provided."*

`HEAD fcf6e3d`, **59 commits**, clean tree. Guards **0 fail / 1 warn at BOTH
subdivision levels**, warn unchanged.

---

## 1. Restore and verify — BY CONTENT, never by hash or commit count

```bash
git clone tacombi_history_rev9.bundle tacombi && cd tacombi
git pull ../tacombi_rev14_unified.bundle HEAD     # rev 14 unified line
git pull ../tacombi_rev14b_incremental.bundle HEAD  # THIS handoff's work
```

Then all of these must be true:

```bash
git status                              # clean
grep -c '### 10.30b' SPEC.md            # 1  — the pole finding
grep -c _isTail t1_mats.py              # non-zero — the tail gate
grep -c FadeVert t1_mats.py             # non-zero — the vertical sun fade
grep -c _FLAT_SHADED build.py           # non-zero — flat glass panes
grep -c backdrop_headroom post.py       # non-zero — the owner's A/B
ls AUDIT_rev11.md AUDIT_rev12.md        # BOTH present
```

Commit hashes and counts move whenever the handoff itself is committed. Do not
verify on them.

## 2. Both guards, and the figures I watched print

```bash
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=2 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=1 /tmp/blender/blender -b --python audit.py
```

| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 1 warn** | **0 fail, 1 warn** |
| warn | roof crown @ rear axle (dome-corrected) **1.992** vs spec 1.960 (**+32 mm**) | **1.993** (**+33 mm**) |
| dims | roof@rear-axle **1.894**, raw resid **−66 mm**, `DOME_DEFICIT` **+98 mm** unmodelled | 1.895, −65 mm, +98 mm |
| cut roof hole | **56293v** | **207383v** |

Also: `roof aperture: open, and solid fore / aft / both sides`; `TYRE_D=0.6650`;
3 open apertures on +Y; four shut lines `100 % open`; band `1.372–1.775`; bay
widths **`0.516 0.515 0.516`**; **181 meshes**; **0 non-manifold edges**;
**5 materials constant-rough**; 42 distinct materials in scene.

`cutters rolled back | none` is a **STATE.md row**, not a console print —
`audit.py:295` writes it and `build.py:522` only logs when a cut actually
failed. Do not go looking for it in the console; check STATE.md.

## 3. What rev 14 changed, each with its measurement

### 3.1 The tail gate — the flank tile no longer prints on the flat tail face

`t1_mats.py` gains a TAIL selector mirroring the nose one. Re-measured
independently of AUDIT_rev12 on `ref_rear34.jpg` rows 545–725, one gate
(hue 25–90°, S > 0.35, V > 0.45):

| region | gold | n |
|---|---|---|
| rear quarter, cols 830–940 (**positive control**) | **43.687 %** | 19 800 px |
| flat tail face, cols 965–1150 | **0.006 %** | 33 300 px |

After the change, on a 1400×1000 rear ortho, central 40 % of body width, with a
**negative control**:

| arm | gold on the flat tail face |
|---|---|
| as built | **2.129 %** |
| `T1_W_ART=0` | **2.079 %** |

**The folk art contributes 0.05 percentage points.** The ~2.1 % both arms report
is the measuring gate firing on the starburst (§3.2), not residual art. Pre-fix
the audit measured **14.30–18.11 %**. Quote the controlled difference, never the
raw 2.1 %.

Keyed on the surface **normal**, not a station — the rear quarter's normal is
not X-dominant so it keeps its real 43.7 %. `X < −1.60` exists only to exclude
the nose and could be wrong by 300 mm either way. Applied to the **alpha**: where
alpha is 0 the base colour is already body red, which is why the tail needed no
second image the way the nose did.

### 3.2 NEW, SEVERITY HIGH, NOT FIXED — the tail and nose caps are poles

A rear elevation — a view no revision had ever rendered — shows a radial
starburst across the tail. Four arms, same view, high-pass sd on a clean
100×220 patch of the engine lid:

| arm | patch mean | high-pass sd |
|---|---|---|
| as built | (109.9, 49.2, 35.3) | **15.478** |
| `T1_W_ART=0` | (109.8, 48.2, 35.2) | **15.459** |
| `T1_W_ALB=0` | (109.1, 49.0, 35.2) | **15.412** |
| `T1_SPEC=0` | (107.0, 43.9, 30.0) | **16.834** |

Not the art, not the breakup, not the specular — all three refuted, the last in
the wrong direction. Probing `T1_body`:

```
POLES: vertices with >=8 incident faces: 4
  POLE valence 115 at (-2.1080, -0.0000, +0.9612)     <- tail, outer skin
  POLE valence 112 at (-2.1052, -0.0000, +0.9611)     <- tail, inner skin
  POLE valence 110 at (+2.1224, +0.0000, +0.7729)     <- nose, outer skin
  POLE valence 110 at (+2.1252, +0.0000, +0.7727)     <- nose, inner skin
TRIS 233 total, 143 forward of x=0, 90 aft
```

A 115-triangle fan on one vertex at the exact centre of the flat tail face,
smooth-shaded. **Deliberately not fixed** — it is loft topology, the shell
carries a load-bearing boolean order and the `t1_shell.py:286` assertion that
exists because a shut line crossing an arch lip collapsed the shell 205 562 v →
12 v for six revisions. It belongs with the phase-5 loft work.

### 3.3 Sun fade reaches vertical surfaces without breaking the red lock

The fade MapRange was keyed on `Normal.Z` over 0..1 → vertical surfaces got
exactly **zero**. Measured on the cream corner panel, X −1.60…−1.84: C*
**14.55 → 6.53** (−55 %), L* 89.6 → 96.2, hue constant 67–73°; render C*
1.98 → 1.59.

A blanket fix would take **SPEC 10.12's locked red albedo saturation 0.816 to
~0.77**. So the vertical term is a NEW per-material WEATHER input `FadeVert`,
default 0.0, combined as `MAXIMUM(MapRange(Nz), FadeVert)`, switched on **only**
for `cream`, `bumpercream`, `countercream`, `wheelcream`, `capwhite` — where the
−55 % was measured, and none of which carries a locked saturation. Value
**0.50** = the diffuse view factor of a plane to a uniform hemisphere,
(1 + Nz)/2. The measured −55 % is a spatial gradient; this delivers the uniform
part only and the gradient is left open rather than faked.

### 3.4 Glass panes flat-shaded

`A()` called `shade_smooth()` unconditionally. Panes are 6 mm **solid slabs**, so
that averaged the flat face normal with the 90° rim normals all round the
perimeter. Audit measured: **88.7 %** of pane pixels change at mean |Δ| **39.18**
against a null of **4.19** — 9.4×. Not the whole defect: **81 % of the pane's
brightness is the rig**, and `gal_ceiling`'s `visible_glossy` was REFUTED as the
cause (1.87 against that 4.19 null).

### 3.5 The mural's neutral lift is the specular pedestal

Texture (127,59,23) matches the photograph (126,60,24) **to one code per
channel**; render (148,92,69). The material has no additive node — it is five
nodes. The lift is `img_paint`'s `spec = 0.42` → F0 **0.0336**, achromatic, on a
dark saturated albedo: on linear (0.2051, 0.0423, 0.0091) a neutral +0.03 moves
B ~330 %, G ~70 %, R ~16 % — exactly the observed direction. Set **0.42 → 0.16**,
overridable with `T1_MURAL_SPEC`. **First step, not a solve.** Run the three-point
solve on the **albedo pass**, not the beauty pixel.

### 3.6 Cream breakup raised, honestly not solved

`W_ALBEDO` **0.130 → 0.260**. It is not linear: the file's own calibration has
0.06 → 1.2 % albedo sd and **0.13 %** display residual, while 0.130 realises
**1.24 %** display — so most of the shipped 1.24 % comes from somewhere other
than this node. Targets are 4.22 % (SPEC 10.4) and 7.37 % (direct re-measure).
`T1_W_MAPLO` / `T1_W_MAPHI` now expose the map window, which is the other lever.
**Move one at a time.**

### 3.7 `flank_compare.py` computes a number, and the flank script FAILS

```
ink area ratio   0.8869              target 1.000 +/- 0.10   FAIL
ink aspect       2.7244 vs 2.3478    target within 5 %       FAIL  (+16.04 %)
IoU vs ceiling   0.7496              >= 0.85 x 0.8591        PASS
worst region     0.126  (Senor)      >= 0.75 of its ceiling  FAIL
```

Ceiling **0.8591 measured this run**, against AUDIT_rev11's inherited 0.87 —
agree to 0.011. Projection guard: ground plane predicted row 962.2, measured 960
(−2.2 px = −8.1 mm). All three framing errors fixed; `SCR` is parsed out of
`build.py` with `ast` so it cannot go stale; all four corners projected with
their own `rake_drop(x)`; one common frame at one mm/px, translation-only
registration so aspect cannot be absorbed.

**The aspect error is dimensionless** — no px/m error can produce it. `SCR` is
now the right shape, so the shortfall is INSIDE the panel: ink sits **+95 mm
below the panel top**. **Why the old test could not fail:** its `REF_INK` crop
was aspect **2.7374**, within **0.48 %** of the render's squashed **2.7244** — it
had cropped the photograph down to the render's own error.

`Senor` 0.099 against a 0.783 ceiling; the marks render but do not read as ink,
and the render's tarnish runs darker and warmer where the photograph's runs
cooler. Build finding, logged, **not chased**.

### 3.8 `post.py` — the backdrop A/B the owner asked for

Default is **byte-identical** to rev 13, hash-verified. Arm A corners
**255.000**, vignette **0.0000 DN**, grain sd **0.0000**, **100.0000 %** of
backdrop exactly (255,255,255). Arm B corners 246.008–246.021, vignette
**−4.7889 DN** monotone in every radial bin, grain sd 0.9009/0.9007/0.9010,
0.0007 % at 255.

```bash
python3 post.py out/<tag>_raw.png out/<tag>_A_white.png
python3 post.py out/<tag>_raw.png out/<tag>_B_headroom.png --backdrop headroom --matte out/<tag>_matte.png
```

**The hero PNG's alpha carries no information** — probed at 64×48 through the
real compositor: min 255, max 255, unique [255]. A true matte needs a File
Output tap in `studio.py`. `--matte` is plumbed and waiting. `--bloom-thr` is now
a real flag and an unrecognised `--flag` is a hard exit. CA left at 0.0011,
exposed as `--ca-coef`; verified 0.0005 gives 1.7244 px, inside the 1–2 px band.

## 4. Settled by the owner in rev 14

- **The windscreen is a SPLIT screen — two panes, centre divider.** Closes an
  AUDIT_rev12 NOT MEASURABLE item. The build already matches.
- **Backdrop:** he wants the A/B before deciding. Built; render it on a real
  hero, not the synthetic.
- **Photographs:** he instructed a comprehensive search rather than supplying
  them. See §5.

## 5. THE GREEN/RED QUESTION — put this to him before measuring any new frame

No left-side broadside and no off-side/rear view of the Playa vehicle exists on
the reachable open web. But **every colour reference for the PLAYA vehicle says
green**: Tacombi's own story page ("the original green Tacombi has since slipped
into a new lick of paint"), CNBC Jan 2023 ("1963 green VW bus"), a blogger
standing in Playa in 2012 ("a distinct lime green"). The red/cream two-tone is
consistently attached to **Nolita**.

Three readings, none excluded: (a) the red livery is the post-repaint state and
the Nolita bus is the same steel; (b) it was repainted red while still in Playa;
(c) there were two vehicles — the company timeline says two Playa locations
opened. **If (a), Nolita photographs are photographs of the same vehicle and are
the only realistic route to an off-side or rear view.** He has excluded Nolita;
that exclusion should be re-put to him with this evidence.

Blocked, not absent, and both likely to hold the needed angles: Tacombi's
Instagram retrospective post (robots-disallowed) and the brand film on YouTube
(rate-limited over six attempts). He can open either in a browser.

## 6. Ordered work list for rev 15

Metrology → shaders → post → rig → detail geometry → loft → camera last.

1. **Solve `T1_MURAL_SPEC`** onto (126,60,24) **on the albedo pass**. §3.5.
2. **Solve `W_ALBEDO`/map window** onto 4.22–7.37 % RMS at 25 mm, one lever at a
   time, measuring after each. §3.6.
3. **`COUNTERTAN`** — the §10.29 method: hold `COUNTERCREAM`, drive the
   gold-line-referenced top/fascia linear ratio onto **(0.796, 0.810, 0.633)
   ± 0.02** on dispenser-free columns; check r/g lands 1.01–1.03 and b/g 0.781.
   The hue is ~16 % too orange and does not survive at all.
4. **Glass, the rig half** — 81 % of the pane's brightness. `sample_clamp_direct`
   and `_indirect` are both 0.0; the reflected source is a 16.0 × 0.55 m
   rectangle at 511.5 W at roughness 0.022.
5. **The bloom/vignette/grain A/B on a real hero**, then his decision.
6. **Per-bay galley**: render **24.34 / 19.65 / 24.89** against photograph
   **32.23 / 24.28 / 18.11**. **Bay 2 is the defect; bay 3 already runs over.**
   No further global lift.
7. Detail geometry: cream rim (rim/tyre 0.6612 ± 0.0060 vs 0.5729, 14.7σ);
   hubcap ring + fused V/W; T-handle z only; plate frame aspect; tail lamps;
   louvre ends.
8. **The loft, jointly** — roof crown + rake (`DOME_DEFICIT` to zero, crown R
   2.45 ± 0.15 m), then the rear arch as a **flat-crowned ogee** (drop ∝
   |Δx|^3.9±0.2), then the tail LAST as a re-spaced aft station set, **and now
   the end-cap poles (§3.2) in the same pass** — they are the same loft.
9. Camera absolutely last.

**Parked deliberately:** tyre deflection (real at 23–32 mm, unauthorable in an
axisymmetric revolve, trips `TYRE_D`). **Logged not applied:** the serving bays
may be glazed — contradicts a reading he settled himself; needs a third method
or a new photograph.

## 7. Rules this revision either used or added

- **Check what a probe can physically see** — and this now applies to crops
  drawn FOR the owner. My tail-face box sat at columns 834–930 when the art's
  aft-most extent is 952, so it was entirely on the rear quarter. He answered it
  correctly; the box was wrong.
- **Ask him, then measure what he says.** He said there was art on the tail
  face. There was — in my box. The measurement, re-cut honestly, still puts the
  flat face at 0.006 %.
- **A negative control turns a number into a measurement.** `T1_W_ART=0` is what
  makes "0.05 points" mean something where "2.1 %" would have misled.
- **Do not put a figure in an acceptance test unless you watched it print.**
- **A guard can be strengthened instead of widened.**
- **When a finding breaks something independently locked, do not apply it
  blind** — `FadeVert` exists so the red lock survives the fade fix.
- Spawn 3–4 `Agent`s on **disjoint files**; this box has 2 cores and a 10-minute
  shell limit.
