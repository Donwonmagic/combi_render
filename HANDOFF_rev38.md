# HANDOFF rev 38 — his report 6 is the cab floor, not a door part

## What he reported, and what it actually was

Report 6, verbatim off `rev37_hero34f.png`: *"also there seems to be a bar
obstructing the front wheel?"*

The inherited brief identified `doorback1` and called reports 5 and 6 possibly
one fix. **Ablated and refuted.** The real object is **`cab_floor`**, seen
through a wheel arch that has **nothing behind it** — there was no wheel house
anywhere in this build. SPEC 10.96.

## What moved

| | rev 37 | rev 38 |
|---|---|---|
| objects at `materials:` | 126 | **131** |
| meshes | 185 | **190** |
| `cab_floor` width | 1.560 | **1.200** (`FLOOR_W`) |
| `van_floor` width | 1.400 | **1.200** (`FLOOR_W`) |
| wheel houses | **none** | **4** |
| `lid_strut` | 1 | **2** |
| floor↔wheel overlapping face pairs | 632 + 524 | **0** |
| interior rays through front arch | 308 | **0** |
| interior rays through rear arch | 9 | **0** |

Everything else identical: 42 materials, 5 constant-rough, **0 non-manifold**,
roof 1.9835 / 1.9833, roof hole 68564v / 252749v, rake 17.75, L=4.065 W=1.750,
arch gaps 39.7 / 40.7 mm, bays 0.516 / 0.515 / 0.516, off flank 804.9 mm,
over-rider rows **NOT APPLICABLE, stated**.

Build files touched: **`build.py`, `t1_shell.py`, `t1_detail.py`,
`probe_dust_scope.py`.** No shader, no artwork, **3/3 texture md5s unchanged**.

## The three things the next context must not lose

1. **THE HERO CAUGHT TWO DEFECTS EVERY GUARD PASSED.** The first wheel house
   was a full 360° revolve — 0 fail, 0 warn, 0 non-manifold, 0 interior rays,
   all six probe controls PASS — and the render showed a dark skirt hanging in
   mid-air below the sill. The second had a fixed outboard y and stood up to
   90 mm proud of the skin; guards passed again. **A guard tests the property
   you thought to name. Only the render tests the property you did not.**

2. **A REVISION THAT MOVES GEOMETRY MUST RE-RUN THE PROBES, NOT ONLY RE-SHOOT
   THE HERO.** rev 37 wrote the hero half of this rule and not the probe half,
   and shipped two stale probe figures in its own brief. `probe_dust_scope`'s
   mesh-count literal has now drifted **twice, in both directions** — rev 30
   (185→186) and rev 37 (186→185), each time unswept.

3. **THE BRIEF'S §6 ITEM 1 NAMED A FUNCTION THAT NEVER RUNS.** `signboard()` is
   behind `T1_SIGNBOARD=1`, not the default, and no hero may be rendered with it
   on. His report was right; the attribution was not.

## New instruments

* **`T1_ABLATE=name,name`** in `build.py`, upstream of the `T1_PREVIEW` block.
  Removes named objects before the render. **A name matching nothing RAISES**
  and writes no frame — an ablation that removes zero objects renders an
  identical frame, and "identical" is exactly the reading that would be misread
  as a finding. Default off; unset leaves the shipped path bit-identical.
* **`probe_rev38_wheelbar.py`** — ray-cast identification through the hero34f
  camera, 6 controls, all PASS.
* **`probe_rev38_floorpen.py`** — BVH overlap, floors vs wheels, on evaluated
  world-space meshes.

**27 probes now** (was 25).

## Open, in order, for rev 39

1. **Report 5 — the doors extend lower, around the wheel well.** NOT the same
   fix as report 6; the ablation refuted the shared cause. `doorback1` runs
   z 0.717→1.755, its bottom a straight line 52 mm above the tyre crown. Its
   lower boundary has never been measured; `_DOOR_TOP_AUTH` and `DOOR_H` are
   AUTHORED.
2. **Report 3 — headlamp vs two-tone**, already measured at 4.4 σ. **Do not
   move the roundel with the lamps.** It is one report about a RELATIONSHIP.
3. **Report 4 — the VW glyph.** §10.25's premise is false: a 52 mm
   interpenetration, not a 12.7 mm air gap.
4. **Report 1 / 5 — `V_POW` 0.60 against an implied 0.30–0.48.** Mirror any
   change into `t1_shell.nose_shape.zV`.
5. **Report 7 — "100% Calidad" off centre.** Determine texture-versus-panel
   first.
6. `probe_clean_top` / `probe_dust_anchor` — rewrite or retire. **SIX
   revisions.** Do not widen a tolerance.
7. Camera absolutely last.

## Still outstanding, and NOT in any other carrier

* **REGION 3 — his answer.** Re-put in rev 38, still unanswered.
* **Nolita, geometry only** (rev 15). 8 in SPEC, 0 in REF_MEASUREMENTS.
* **The GitHub migration** (rev 31c).
* **Recovered by memory sweep in rev 38, in no carrier at all:** the broadside
  render laid over `ref_side.jpg` at matched scale, which he asked for as the
  way fixes are driven; *"remember to hold up next to the actual source
  photos"*, last done in rev 16; **the die-cut vinyl sticker — the original
  deliverable**, untouched since rev 25, with its style and scene already locked
  by him; the **Playa hero**, which he deprioritised (*"let's not do playa right
  now"*) but never cancelled, and which carries his emotional bar; **NINE flower
  heads on the mural board, counted by him**, never checked against the model;
  Dimension E of the specialist audit, left incomplete; and ~12 unverified image
  URLs never seen by a vision-capable pass.
