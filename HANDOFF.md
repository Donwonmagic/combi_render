# TACOMBI COMBI — COMPLETE HANDOFF
**Read `SPEC.md` first. It is authoritative. This file explains the machine.**

Target: a maximum-fidelity, true-to-scale 3D model of the **Playa del Carmen
Tacombi combi** (1963 VW Type 2 T1 Kombi converted to a taqueria), rendered as
white-studio hero stills. Donald's standing process: **ground → build →
adversarial audit → iterate**, and never declare done off self-review.

---

## 1. Where the build actually is

Geometry is correct in silhouette and passes every regression guard. Livery,
brightwork and lighting are mid-refinement. **Nothing here is finished.**

Last verified build (`T1_SUB=1`, `verify.py` → 0 fail, 0 warn):

| Measure | Value | Spec |
|---|---|---|
| Overall length over bumpers | 4.2806 | 4.280 |
| Body width | 1.7198 | 1.720 |
| Overall height | 1.8262 | 1.940 − 0.110 drop |
| Rocker to ground | 0.2757 (15.1 % of H) | lowered bus |
| Arch-to-tyre gap | 35.5 mm | tight, lowered |
| Windscreen vertical rise | 0.335 (18.3 % of H) | ~18.5 % on a real T1 |
| Belt line | 1.122 (61.4 % of H) | — |
| Body shell | 0 non-manifold edges | watertight |
| Body faces | 49 289 quad / 262 tri / 2 876 ngon | ngons are boolean fallout |

---

## 2. Environment

```
Blender 4.5.3 LTS at /home/claude/blender/blender     (NOT on PATH)
Project                /home/claude/tacombi
2 CPU cores, 7 GB RAM  -> Cycles CPU only. No GPU, no EEVEE.
```

Render cost on this box: ~15 s per 700×480 @16 samples; a 2400×1600 @256
sample hero is roughly 35–60 min. **Always background long renders**
(`nohup … &`) — the shell times out at 2 minutes.

---

## 3. Module map

| File | Role |
|---|---|
| `SPEC.md` | **Authoritative.** Locked dimensions, livery, config, regression list |
| `SPEC_AUDIT.md` | Element-by-element read of the reference, confidence-graded |
| `t1_core.py` | Parametric engine: section/loft, profile LUTs, `build_kombi()`, boolean + sweep + revolve + conform helpers |
| `t1_shell.py` | Openings: windscreen, cab glazing, serving bays, rear glass, arches, panel gaps, ragtop, nose V-swage |
| `t1_detail.py` | Wheels, tyres, hubcaps, bumpers, lamps, gutter, mirrors, wipers, handles, counter, galley, interior |
| `t1_mats.py` | All materials. Body paint is fully procedural (no UV unwrap of the shell) |
| `studio.py` | Shadow-catcher ground, softbox rig, camera presets, render driver |
| `build.py` | Master driver — the pipeline order below |
| `verify.py` | Regression guard, asserts SPEC §6 |
| `audit.py` | Measured provenance + silhouette metrics. **Run this before claiming anything** |
| `texgen.py` | Folk-art swirl tile, emblem, generic signboard |
| `sign_gen.py` | "Señor Tacombi" silver script with the hand-drawn ornate swash T |

Textures in `tex/`: `swirl.png` 2048² seamless folk art (29.9 % ink),
`senor.png` 4096×890 silver script, `calidad.png` 2048×1400,
`emblem.png` 1024². `estilo.png` / `fascia.png` are **dead** (retired wording).

---

## 4. How the body is built — and why the order matters

The shell is **one continuous lofted surface, nose to tail**. Earlier builds
lofted the cab and the rear separately and the seam was visible; do not go back.

`t1_core.section()` builds a closed ring from a **universal normalised
half-width profile `G(z)`** multiplied by a per-station half-width `WX(x)`,
with independent bottom-roll and top-roll radii and a roof crown. Because
`y = WX(x)·G(z)` does not depend on the section's top, sections at different
heights share an identical flank curve — that is what makes seamless joins
possible.

Longitudinal shape lives in LUTs in `t1_core.py`: `ZB` (sill), `ZT_ALL`
(tail roll → roof → windscreen → cowl → nose), `WX`, `RT_ALL`, `CR_ALL`,
`RB_ALL`, and `STATIONS` (65 stations, dense at the nose and the screen).

### Pipeline order in `build.py` — three hard-won constraints

1. **Subsurf is applied destructively before any boolean.** Level 2 gives
   ~113 k verts.
2. **Wheel arches are cut while the shell is still a closed solid.** The
   cylinder's inboard cap becomes the wheel-well tub for free. Cutting them
   after solidify leaves the underbody open.
3. **Everything else is cut *after* solidify.** Post-solidify the shell is a
   2.8 mm skin, so a cutter's inner cap lands in the hollow and creates no
   stray faces. Cutting apertures before solidify produced box-shaped recesses
   behind every window.

`cut()` applies **one cutter at a time**, and if a boolean drops the vert count
below 60 % it **rolls the mesh back** and records the failure. This exists
because a single tangent cutter silently shredded the shell from 202 k to 9 k
verts and still passed a naive check. **Do not remove this guard.**

### Known boolean fragility
The EXACT solver fails where a cutter wall runs near-tangent to the shell. The
door gap's top run sat 1.5 mm below the roof roll and destroyed the mesh at
subsurf 2 while working fine at subsurf 1. Keep gap outlines ≥ 20 mm clear of
roll-over regions.

---

## 5. Materials — how the livery works

`t1_mats.body_paint()` is **object-space procedural**, so colour boundaries are
resolution-independent and need no UV unwrap:

- Cream above / red below a break surface: belt line `Z_BELT` on the flanks,
  blended by a smoothstep on X into the **T1 V-swage**
  `zV(y) = V_APEX + V_RISE·(|y|/0.86)^V_POW` across the nose.
- Folk art is `swirl.png` **box-projected** in object space, masked to the red.
- **Density grading** (SPEC §3): a Map Range on X × a Gaussian band on Z gives
  a density field; that field sets a spatially varying threshold on a
  low-frequency noise, so whole motifs drop out toward the tail rather than
  fading. Dense on the nose, trailing along the belt, sparse at the tail.

Decals use `conform_panel` / `conform_solid` / `conform_disc` in `t1_core.py`,
which generate flank-hugging geometry (`y = WX(x)·G(z) + offset`) with UVs, so
artwork sits on the curved flank without floating or clipping.

**Mirroring rule that has bitten twice:** a decal's `u` must run bow-to-stern
in *screen* space on each side. `conform_panel` uses
`u if side > 0 else 1 − u`; `conform_solid` currently uses the opposite and is
**wrong** (see defect D1).

---

## 6. Open defects, ranked — start here

| # | Defect | Evidence | Root cause / fix |
|---|---|---|---|
| **D1** | "100 % CALIDAD" decal is **mirrored** | `v6_side.png`, rear bay | `conform_solid` UV builds `u` from `min(x)`, which is the *rear*. Flip to `1 − u` for `side > 0` in `t1_core.conform_solid` |
| **D2** | **Whitewalls do not render** — tyres read solid black | `v6_side.png` | `revolve(mat_bands={3:1,4:1,5:1})` sets `material_index` *after* `fix_normals()` rebuilds the mesh through bmesh. Set indices inside the bmesh pass, or re-verify slot order at runtime |
| **D3** | **Backdrop renders grey (0.686), not white** | corner-pixel probe in `studio.render_set` | Shadow catcher is not taking effect, or the compositor isn't running. Check `ob.is_shadow_catcher` survives, `scene.render.use_compositing`, and that `film_transparent` is still True at render time. Until fixed, every hero still has a grey background |
| **D4** | Three serving bays render **flat black** | `v6_side.png` | Nothing lit behind them. Add a dim interior fill light and lighter galley materials so the openings read as depth, not holes |
| **D5** | Front bumper reads thin and detached | `v6_front.png` | `BUMP_OFF = 0.0075` hugs the plan curve but the blade needs a deeper section and a visible mounting iron; also verify it wraps to the corners |
| **D6** | Roof-to-windscreen transition too bulbous | `v6_side.png` | Tighten `RT_ALL` around x 1.73–1.83 and add stations |
| **D7** | Paint reads pink/salmon, not deep tomato red | all renders | AgX + Punchy desaturates. Either deepen `RED` further or test `view_transform='Standard'` with the key pulled down |
| **D8** | V-swage arms meet the body corner at a height that doesn't line up with the belt line | `v6_front.png` | `V_APEX + V_RISE` must equal `Z_BELT` exactly at `y = 0.86`. Currently 0.818 + 0.414 = 1.232 = `Z_BELT` ✔ — but re-check after any belt change |
| **D9** | Missing detail inventory | — | number plates, fuel filler, rear vents, engine-lid handle, tyre sidewall lettering, hub detail behind the cap |
| **D10** | 2 876 n-gons on the shell | `audit.py` | Boolean fallout. Harmless for rendering, but fails the "crisp topology" bar if the mesh is ever delivered |

---

## 7. Reference readings — locked, do not re-litigate

Confirmed by Donald against the photograph:

- Body: **Kombi van**, full height to the tail. *Not* a pickup with a canopy.
- Roof: **intact**, folding ragtop modelled **closed**.
- Show side: **three evenly sized, evenly spaced serving openings**, then a
  **fourth rear pane frosted with "100 % CALIDAD"**.
- **Cantilevered timber plank counter** under the serving openings.
- Script: **"Señor Tacombi"**, **silver**, ornate **swash capital T**.
- Wheels: **whitewall tyres**, **solid red domed hubcaps** with a **white VW**.
- Bumpers sit **low** relative to the wheel.
- Indicators **poke out proud** of the nose above the headlamps.
- VW nose emblem: **painted cream**, V above W, never inverted.
- Bus **sits noticeably lower** than stock.
- Finish: **clean restoration** gloss, not weathered patina.

Retired misreadings live in SPEC §0.1 — treat any reappearance as a regression.

---

## 8. Commands

```bash
cd /home/claude/tacombi
B=/home/claude/blender/blender

# fast build + regression guard (~15 s)
T1_SUB=1 T1_VERIFY=1 $B -b --python build.py

# measured provenance + silhouette metrics — run before claiming anything
T1_SUB=1 $B -b --python audit.py

# quick look
T1_SUB=1 T1_PREVIEW=side,front,hero34f T1_SAMP=16 T1_KEY=0.9 \
  T1_RX=760 T1_RY=520 T1_PFX=v7 $B -b --python build.py

# clay, to judge form without shading
T1_SUB=1 T1_CLAY=1 T1_PREVIEW=hero34f T1_SAMP=10 T1_PFX=clay $B -b --python build.py

# final (background it)
T1_SUB=2 T1_PREVIEW=hero34f,hero34r,front34,side,front,rear,detail_f,low34 \
  T1_SAMP=256 T1_KEY=0.9 T1_RX=2400 T1_RY=1600 T1_PFX=final \
  nohup $B -b --python build.py > final.log 2>&1 &

# regenerate artwork
python3 texgen.py          # swirl / emblem
python3 sign_gen.py        # Señor Tacombi silver script
```

Env vars: `T1_SUB` subdiv, `T1_SAMP` samples, `T1_KEY` light scale,
`T1_RX/RY` resolution, `T1_PFX` filename prefix, `T1_PREVIEW` comma-separated
view names, `T1_CLAY`, `T1_VERIFY`, `T1_SAVE`, `T1_OUT`, `T1_VT`/`T1_LOOK`
colour management, `T1_EXP` exposure.

Camera presets in `studio.views()`: `hero34f` (the reference angle),
`hero34r`, `front34`, `side`/`front`/`rear` (ortho), `detail_f`, `low34`,
`topdown`.

---

## 9. Suggested order of work

1. **D3 first** — every hero still is unusable until the background is white.
2. D1, D2 — cheap, visible, and both are livery-accuracy defects.
3. D4, D5, D6 — form and read.
4. D7 — colour, once the background is correct (grey backdrop is skewing the
   perceived hue).
5. D9 — detail inventory sweep against the photograph.
6. Then a genuine **adversarial audit**: spawn an independent reviewer against
   `SPEC.md` + `audit.py` output + the renders, and act on what it finds.
   Self-review has already missed a shredded mesh and two mirrored decals.

---

## 10. Process notes worth keeping

- The pickup-vs-Kombi error cost roughly half a day. It happened because the
  build started from a low-resolution reference without checking prior project
  context. **Read memory and prior context before modelling.**
- `verify.py` was written after the fact and immediately caught two real
  regressions. Extend it whenever a new invariant is agreed.
- `audit.py` reports numbers instead of adjectives. Donald has explicitly
  rejected self-reported scores; report the measurement against the reference.
