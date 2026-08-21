# REPORT rev 48 — LID TOPOLOGY SOURCE MAP

## **SOURCE-SIDE ONLY — NOT CONFIRMED AGAINST THE BUILD**

Every statement below was derived by reading source, grepping, git archaeology and plain
Python arithmetic on the constants. **Blender was not run. `build.py` was not run. No render
was made.** The rev-48 brief §2 and `LEDGER_rev47.md` §9 both record that two separate prior
contexts "fixed" the sign props' inset by trusting the source over the build, and both were
wrong. **Treat this document as a map of what the source SAYS, and confirm it with §F.**

Coordinate frame (`t1_core.py:12`): **+X = forward (nose), +Y = left, +Z = up, ground z = 0.**
`X_NOSE = 2.108` (`t1_core.py:26`), `X_TAIL = -1.873` (`t1_core.py:72`). Two z frames exist:
**UN-DROPPED** (authored, what every constant in `t1_shell` is written in) and **DROPPED /
above-ground**, produced by build.py step 8b (`build.py:872-882`) which subtracts
`RAKE_Z0 + RAKE_DZDX * x` from **z only** — x is never touched by the shear.

---

# A. THE COMPLETE LID INVENTORY

## A.1 Summary table

| # | part | builder | file:line | class | object name(s) in the scene | posed? |
|---|---|---|---|---|---|---|
| 1 | **main roof lid skin** | `t1_shell.roof_lids` → `_lid_panel` | `t1_shell.py:1241` / `1158` | **(a) separate geometry, posed OPEN** | `lid_main` | **yes, 104°** |
| 2 | **roof lid mural board** | `roof_lids` → `_lid_face` | `t1_shell.py:1268` / `1213` | (a) separate geometry, posed with the lid | `lid_board` | yes, 104° |
| 3 | **roof lid perimeter rails ×2** | `roof_lids` → `_rag_grid` | `t1_shell.py:1275-1278` / `1011` | (a) separate geometry, **NOT hinged** — sits on the roof | `lid_rail`, `lid_rail.001` | no (stays on roof) |
| 4 | **roof lid prop struts ×2** | `roof_lids` | `t1_shell.py:1355-1372` | (a) separate geometry | `lid_strut0`, `lid_strut1` | n/a (built in place) |
| 5 | **roof aperture cutter** | `t1_shell.roof_cutters` | `t1_shell.py:1114` | cutter, consumed | `cut_roof` (deleted after boolean) | — |
| 6 | **trunk / engine lid** | `t1_shell.engine_lid_gap` | **`t1_shell.py:994`** | **(b) boolean-cut SEAM in the body shell** | **no object of its own — a mesh island inside `T1_body`** | **NO** |
| 7 | cab door ×2 | `t1_shell.door_gaps` | `t1_shell.py:808` | (b) boolean-cut seam | mesh island inside `T1_body` | no |
| 8 | off-side cargo doors | `t1_shell.cargo_door_gaps` | `t1_shell.py:978` | (b) boolean-cut seam (+ a mid-split slab) | mesh islands inside `T1_body` | no |
| 9 | cab door hinge hardware | `t1_detail.door_hinges` | `t1_detail.py:1559` | (a) separate geometry, **decorative only** | `hinge_barrel{±1}_{0.25,0.75}`, `hinge_leaf{±1}_{…}` | no |
| 10 | fuel filler flap | `t1_detail.filler_flap` | `t1_detail.py:2195` | (a) separate geometry, **closed, proud 4 mm** | `fuel_flap` | no |
| 11 | glovebox lid | `t1_detail.cab_fitout` | `t1_detail.py:1447-1451` | (a) separate slab, closed | `dash_glovebox` (+ `dash_knob`) | no |
| 12 | roof peak vent | `t1_detail.roof_vent` | `t1_detail.py:2529` | (a) separate geometry, **explicitly "not a working flap"** (`:2531`) | `roof_vent` (joined) | no |
| 13 | engine lid T-handle | `t1_detail.englid_handle` | `t1_detail.py:2586` | (a) separate geometry mounted ON the seam panel | `englid_handle` (joined) | no |
| 14 | "1963" plate surround | `t1_detail.plate_1963` | `t1_detail.py:2421` | (a) separate geometry mounted ON the seam panel | `plate_1963` (joined) | no |
| 15 | **signboard (retired)** | `t1_shell.signboard` | `t1_shell.py:1403` | (a) separate geometry, **GATED OFF** | `sign_panel`, `sign_face`, `sign_strut` | **not built by default** |
| 16 | `ragtop()` | `t1_shell.ragtop` | `t1_shell.py:1042` | **raises RuntimeError** — dead, kept to fail loudly | — | — |

## A.2 The evidence, per class

### Class (a) — separate posable geometry: the roof lid

`t1_shell.py:1251` `main = _lid_panel(LID_X0, LID_X1, LID_W, "lid_main")` — `_lid_panel`
(`t1_shell.py:1158-1199`) creates its **own mesh and object** (`bpy.data.meshes.new(name)`,
`bpy.data.objects.new(name, me)`, `:1181-1184`), gives it a SOLIDIFY modifier
(`m.thickness = LID_T; m.offset = -1.0`, `:1194-1196`) and applies it. It is never booleaned
into `T1_body`. `build.py:302-306` collects it and assigns materials. **Separate object.**

### Class (b) — boolean-cut seam: the trunk/engine lid, and both door sets

`build.py:254`:
```
cut(body, S.door_gaps() + S.cargo_door_gaps() + S.engine_lid_gap(), "gaps", kind="gap")
```
`cut()` (`build.py:145-208`) runs a boolean **difference** of each cutter against `body`, then
`bpy.data.objects.remove(c, do_unlink=True)` (`build.py:203`). **The cutter object does not
survive the build.** There is no `A(...)` call, no material assignment and no name that reaches
the scene for `gap_englid`.

**BUT — and this is the load-bearing find — the panel inside the seam is already a separate
CONNECTED COMPONENT of `T1_body`.** `build.py:69-70`, in the boolean-guard rationale, states it
outright:

> "Connected-component count is also useless here -- it legitimately goes **1 -> 6** as each gap
> cutter frees a panel."

Six components = shell + `gap_door+1` panel + `gap_door-1` panel + `gap_cargo` panel split in two
by `gap_cargo_mid` + **`gap_englid` panel**. And the `kind="gap"` post-condition
(`build.py:191-192`) asserts `av > bv` — "gap did not free a panel". So the source claims the
trunk lid **already exists as a free-floating, 2.8 mm thick, closed mesh island inside
`T1_body`, at its closed position.** It is not "painted on"; it is a real slab that has simply
never been separated into its own object or rotated. **§F check 3 is the one that proves this.**

### Class (c) — painted only

Nothing in the lid inventory is paint-only. The roof lid's artwork (`lidmural`) and the yellow
menu strips are textures on real geometry (`lid_board`). The "lit strip lighting along the roof
lid edge" that IMG_2073 shows is **not modelled on the lid at all** — see §C.4.

## A.3 Object-name trace (what to grep for in the built scene)

* `lid_main` — `t1_shell.py:1251`, name literal passed to `_lid_panel`; `_lid_panel` does
  `bpy.data.objects.new(name, me)` at `:1183`. No rename, no join.
* `lid_board` — `t1_shell.py:1268` → `_lid_face` `:1226-1228`.
* `lid_rail`, `lid_rail.001` — `t1_shell.py:1275-1278`, a 2-iteration loop calling `_rag_grid`
  with the **same** literal `name="lid_rail"`, so Blender's `.001` suffix applies to the second.
* `lid_strut0`, `lid_strut1` — `t1_shell.py:1372`, `name=f"lid_strut{len(struts)}"`, evaluated
  **before** the append, so 0 then 1.
* `T1_body` — `build.py:280`, `body.name = "T1_body"`. **This is where the trunk lid lives.**
* `englid_handle`, `plate_1963` — `t1_detail.py:2607`, `:2504`, via `join(...)`.
* `sign_panel` / `sign_face` / `sign_strut` — `t1_shell.py:1449/1453/1462`. **Absent unless
  `T1_SIGNBOARD=1`** (`t1_shell.py:1444`), and SPEC forbids a hero with it on.
* `bulb_string` — `t1_detail.py:2333`. Drip rail, show side. Emissive.
* `audit.py:96` exploits the naming: `_LID_PARTS = tuple(o.name for o in meshes if
  o.name.startswith("lid_"))` — **anything you add named `lid_*` is automatically excluded from
  audit's vehicle-silhouette bounds.** A trunk lid named `lid_trunk*` inherits that behaviour;
  a trunk lid named `trunk_*` does **not** and will poison audit's overall-height row.

## A.4 Hinge axes, angles and pose transforms — every constant

| constant | value | file:line | meaning |
|---|---|---|---|
| `LID_X0`, `LID_X1` | `0.9640`, `-1.0700` | `t1_shell.py:1075` | roof lid fore-aft span. **X0 is the LARGER** — `t1_shell.py:1310-1318` records this being "fixed" wrongly once. |
| `LID_Y_HINGE` | `-0.5450` | `t1_shell.py:1076` | **the hinge line's y** — off side (−Y) edge of the roof opening |
| `LID_W` | `1.1100` | `t1_shell.py:1077` | hinge → free edge |
| `LID_OPEN_DEG` | `104.0` | `t1_shell.py:1078` | **the open angle**, 14° past vertical |
| `LID_T` | `0.0180` | `t1_shell.py:1079` | skin + rail thickness (SOLIDIFY) |
| `LID_PROUD` | `0.0228` | `t1_shell.py:1080` | hinge sits 22.8 mm proud of the roof (measured 26 ± 7 mm) |
| `RAIL_PROUD` | `0.0213` | `t1_shell.py:1081` | perimeter rail proud height |
| `ROOF_CUT_R` | `0.030` | `t1_shell.py:1111` | aperture corner radius |
| `SIGN_OPEN_DEG` | `82.0` | `t1_shell.py:1084` | signboard, gated off |
| `GAPW` | `0.0055` | `t1_shell.py:491` | **every** panel-gap seam width, incl. the trunk lid |
| `ENGLID_CUT_DX` | `0.158` (env `T1_ENGLID_DX`) | `t1_shell.py:855` | seam cut station, inboard of `X_TAIL` |

**The only pose transform in the whole model is `_hinge()`** (`t1_shell.py:1201-1211`):
```python
def _hinge(ob, x_unused, y_hinge, z_hinge, deg):
    a = math.radians(deg); ca, sa = math.cos(a), math.sin(a)
    for v in ob.data.vertices:
        y, z = v.co.y, v.co.z
        v.co.y = y_hinge + (y * ca - z * sa)
        v.co.z = z_hinge + (y * sa + z * ca)
```
It is a **rotation about a fore-aft (X-parallel) axis**, baked into **mesh vertices**, not the
object transform. **That is mandatory here**, not stylistic: `build.py:851-856` asserts that
every mesh in the scene carries an identity object transform, because step 8b's shear reads
`v.co.x` as world x. **A trunk lid posed with `ob.rotation_euler` will trip that assert.**

`_hinge` is called at `t1_shell.py:1252` (skin) and `:1269` (board). The rails are **not**
hinged — they stay on the roof, which is correct: they are the frame the cut skin lifted off.

Computed pose (my arithmetic on the constants, un-dropped frame):
* hinge origin `zh = roof_z(-0.053, -0.545) + LID_PROUD = 1.94599 + 0.0228 = **1.96879**`
  (`t1_shell.py:1250`)
* free edge lands at **y = −0.8135, z = 3.0458** un-dropped (**z ≈ 2.998 above ground**)
* roof aperture y band **−0.545 … +0.565**, x span **−1.070 … +0.964** (2.034 m × 1.110 m)

---

# B. `engine_lid_gap()` — WHAT IT ACTUALLY DOES

## B.1 The whole function (`t1_shell.py:994-998`)

```python
def engine_lid_gap():
    # rev 16: was -1.95, i.e. 158 mm inboard of the old tail skin.
    return [T.gap_prism((T.X_TAIL + ENGLID_CUT_DX, 0, 0), (0, 1, 0),
                        (0, 0, 1), (-1, 0, 0), ENGLID_GAP, GAPW, 0.55,
                        name="gap_englid")]
```
with (`t1_shell.py:855-857`)
```python
ENGLID_CUT_DX = float(os.environ.get("T1_ENGLID_DX", "0.158"))
ENGLID_GAP = [(u, v + 0.8700) for (u, v) in T.rrect(0.9400, 0.5000, 0.055, seg=6)]
```

## B.2 Does it make an object? **No.**

`T.gap_prism` (`t1_core.py:638-666`) builds a **closed solid ring** — inner outline offset
−GAPW/2, outer +GAPW/2, extruded, capped. It is a **cutter**. `build.py:254` feeds it to
`cut(..., kind="gap")`, which booleans it out of `body` and then destroys it
(`build.py:203`). **`gap_englid` does not exist in the finished scene.** It is not in `ASSIGN`,
gets no material, and is not in `VISIBILITY_WATCH`.

**What it leaves behind is a mesh island inside `T1_body`** (see A.2 and `build.py:69-70`).

## B.3 Exact boundary coordinates of the seam

Frame: `u = (0,1,0)` → **Y**, `v = (0,0,1)` → **Z**, `w = (-1,0,0)` → extrusion along **−X**.
Origin `(X_TAIL + 0.158, 0, 0) = (**−1.7150**, 0, 0)`; depth 0.55 ⇒ the cutter spans
**x −1.9900 … −1.4400**, i.e. it passes clean through the tail skin at x ≈ −1.873.

`ENGLID_GAP` is a rounded rectangle **0.9400 (Y) × 0.5000 (Z)**, corner radius **0.055**,
`seg=6` ⇒ **28 samples**, centred on `y = 0`, `z = 0.8700`.

| | value |
|---|---|
| **centreline outline (Y)** | **−0.4700 … +0.4700** |
| **centreline outline (Z), UN-DROPPED** | **0.6200 … 1.1200** (centre 0.8700) |
| **Z above ground** (drop at x=−1.715 is 0.017484) | **0.6025 … 1.1025** |
| outer edge of the cut (± GAPW/2 = 2.75 mm) | Y −0.47275 … +0.47275, Z 0.61725 … 1.12275 |
| corner radius | 0.055 |
| lid face area | 0.94 × 0.50 = **0.47 m²** |
| the cut plane | the tail cap, essentially planar at **x = X_TAIL = −1.8730** |

**These are the coordinates a real openable trunk lid has to be cut from.** The tail end-cap is a
Coons quad grid at station `x = −1.873` (`t1_core.py:_coons_cap`, `STATIONS[0] = _aft(-2.108) =
-1.873`, `t1_core.py:468-478`), spanning z 0.468 … 1.452 and |y| ≲ 0.70 — **the seam sits
comfortably inside the flat tail face**, well clear of the rear-window aperture
(`REAR_Z 1.4500 ± 0.1700` ⇒ z 1.28 … 1.62, `t1_shell.py:229-241`; 160 mm of solid metal between
the two) and well clear of the sill (`ZB` at the tail ≈ 0.39-0.47).

**Two features are mounted ON the seam panel and must travel with any lid that opens:**
`plate_1963` (`t1_detail.py:2421`, centre `PLATE_Z = 0.7800`, outer H `0.3300/1.9616 = 0.16823`)
and `englid_handle` (`t1_detail.py:2586`, `x = X_TAIL - 0.0004`, `z = PLATE_OUTER_CZ -
ENGLID_HANDLE_DROP`). Both sit inside z 0.62 … 1.12.

## B.4 Is there any code path, env var or flag that would open it? **NO.**

* Only one env var touches it: **`T1_ENGLID_DX`** (`t1_shell.py:855`), which moves the cut
  **station in x** — it does not open anything.
* `grep -rn "trunk" --include=*.py` returns **one** hit in modelling code: `lid_gen.py:12`, a
  prose sentence. Every other hit is `playa_env.py` / `studio.py` **palm trunks**.
* `_hinge()` is called exactly twice (`t1_shell.py:1252`, `:1269`) and once more in the gated
  `signboard()` (`:1451`, `:1455`). **Never for the tail.**
* No `T1_TRUNK*`, no `T1_ENGLID_OPEN`, nothing.

## B.5 Seam width / depth — a real recess or a shading line?

**A real 5.5 mm through-slot, not a shading line.**
* Width **`GAPW = 0.0055` = 5.5 mm** (`t1_shell.py:491`).
* It cuts **through** the 2.8 mm solidified skin (`build.py:243-247`, `sol.thickness = 0.0028`),
  because the cutter is 0.55 m deep and the skin is 2.8 mm.
* `verify.py` row 11e proves it is open by **ray-casting**: `_englid_frac`
  (`verify.py:513-542`) fires +X rays from x = −3.0 at every one of the 28 outline samples and
  counts those that get past `X_TAIL + ENGLID_CUT_DX`; the row fails below `SLOT_FRAC_MIN`
  (`verify.py:1059-1064`). Note `verify.py:521-535` records that **this row was DEAD at every
  revision up to rev 18** and printed a false "100 %" — so treat "verify says it's open" as
  reliable only from rev 18 onward.
* On top of that, `t1_mats.round_edges()` (`t1_mats.py`, called `build.py:894`) splices a Cycles
  **Bevel** node with `radius = GAPW / 2 = 2.75 mm` into every Principled BSDF — so the seam
  reads with a soft shaded fold as well as real depth. That is **shading only**; it moves no
  geometry.

## B.6 ⚠ ONE FRAGILITY THE MAIN CONTEXT MUST KNOW BEFORE TOUCHING THE TAIL

`t1_core.py:230-244`. The `gap_englid` boolean is **the single most fragile cut in the model**:

> `NHALF 56, cap 27x28 (asymmetric)  SUB=1 0 fail  SUB=2 **1 FAIL** -> gap_englid REJECTED,
> "zero-area faces 0 -> 2", ROLLED BACK` — and *"Moving the cutter in x does NOT fix it — 0.120,
> 0.158 and 0.200 all give exactly 2 zero-area faces"*.

The only reason it passes today is `T1_NHALF57=1` (default), giving a **mirror-symmetric 28×28
tail cap**. Any change to the trunk-lid outline that breaks symmetry about y = 0, or any change
to `NHALF`, can silently roll the cut back — and a rolled-back cut is reported only in
`FAILED_CUTS` (`build.py:895`). **Read the build log for `gap_englid` every time.**

---

# C. `roof_lids()` — THE WORKING EXAMPLE

## C.1 What the source does, step by step

`t1_shell.py:1241-1400`. Returns `(skins, rails, struts, boards)`.

1. **`zh = roof_z((LID_X0+LID_X1)/2, LID_Y_HINGE) + LID_PROUD`** (`:1250`).
   The hinge origin's z, taken at the lid's **midpoint x**, plus the measured proud height.
   `:1358-1364` records why the midpoint and not the strut's own station: the roof is domed
   fore-and-aft, and sharing one hinge origin makes the strut tip land on the lid's plane *by
   construction rather than by luck*.
2. **Skin**: `_lid_panel(LID_X0, LID_X1, LID_W, "lid_main")` (`:1251`, def `:1158`) — a
   41 × 23 vertex grid built **flat in the XY plane** with +Y running hinge → free edge, three
   Gaussian pressed seams `z -= 0.0028 * exp(-((yv-yc)/0.022)**2)` matching the roof ribs, a
   UVMap, then SOLIDIFY `thickness = LID_T (0.018)`, `offset = -1.0`, `use_even_offset = True`,
   applied. **Rigid — no bow sticks, no sag** (the retired canvas artefacts).
3. **Pose**: `_hinge(main, 0.0, LID_Y_HINGE, zh, LID_OPEN_DEG)` (`:1252`). Baked into vertices.
4. **Artwork board**: `_lid_face(LID_X0, LID_X1, LID_W, "lid_board", off=-(LID_T + 0.0016))`
   (`:1268`, def `:1213`) — a 3×3-vertex flat quad grid, inset 0.030, offset **−0.0196**, i.e.
   1.6 mm below the lid's **underside**. Hinged with the same call (`:1269`). `:1255-1267`
   records two prior sign errors on that offset — **read that comment before copying it.**
5. **Perimeter rails**: two calls to `_rag_grid(RAG_HW, xa, xa, RAIL_PROUD, bows=False, nx=1,
   ny=18, name="lid_rail")` at `LID_X0` and `LID_X1` (`:1274-1278`). These follow `roof_z` and
   **are not hinged** — they are the shallow frame the cut skin sat on, standing 21.3 mm proud.
6. **Struts**: see C.2.
7. **Three asserts, all on the BUILT rod**, `:1374-1399`. Copy this discipline.
8. `build.py:302-306`: `A(lid_skins,"paint")`, `A(lid_rails,"paint")`,
   `A(lid_struts,"chrome_d")`, `A(lid_boards[0],"lidmural")`.

The **aperture** is cut separately by `roof_cutters()` (`t1_shell.py:1114-1156`) from
`build.py:265`, **after** solidify, and is expressed **in terms of** `LID_X0/LID_X1/
LID_Y_HINGE/LID_W` (`:1106-1110`) so moving the lid moves the hole. `roof_cutters` also carries
the rev-16 bug note (`:1145-1152`) that `solid_prism` extrudes **±depth/2 about its origin**, so
you must pass the **midpoint**, not the low end.

## C.2 Strut geometry (`t1_shell.py:1347-1372`)

```python
def _roof_edge_y(xr, y0):                    # walk outboard until roof_z stops changing
    y = y0
    for _ in range(400):
        y2 = y - 0.002
        if abs(roof_z(xr, y2) - roof_z(xr, y)) < 1e-6:
            return y
        y = y2
    return y

for (ob, xs, deg, w) in ((main, LID_X1 + 0.16, LID_OPEN_DEG, LID_W),
                         (main, LID_X0 - 0.16, LID_OPEN_DEG, LID_W)):
    a = math.radians(deg)
    tipy = LID_Y_HINGE + w * math.cos(a) * 0.97
    tipz = zh + w * math.sin(a) * 0.97
    footy = max(tipy, _roof_edge_y(xs, LID_Y_HINGE))
    foot = Vector((xs, footy, roof_z(xs, footy)))
    tip  = Vector((xs, tipy, tipz))
    d = tip - foot
    struts.append(T.cylinder(tuple((foot + tip) / 2), tuple(d.normalized()),
                             0.0075, d.length, seg=14, name=f"lid_strut{len(struts)}"))
```
* **radius 7.5 mm, 14 segments, material `chrome_d`.**
* two struts, **inset 160 mm** from each end of the lid ⇒ x = **−0.9100** and **+0.8040**.
* the **tip** attaches at **0.97 of the lid's width** — the FREE EDGE, the edge that bears.
* the **foot** is found by **measuring the body** (`_roof_edge_y` walks `roof_z` outboard until
  it stops changing) rather than by typing a y. `:1339-1345`: *"a prop stands UNDER the thing it
  props and meets it AT the edge that bears on it"* — 3° from vertical, not 49°.

Computed from the constants (un-dropped; ± the rod radius and end caps):

| | strut0 (x = −0.9100) | strut1 (x = +0.8040) |
|---|---|---|
| foot | (−0.9100, −0.7290, 1.8941) | (0.8040, −0.7290, 1.8939) |
| tip | (−0.9100, −0.8055, 3.0135) | (0.8040, −0.8055, 3.0135) |
| length | 1.1220 | 1.1223 |
| lean from vertical | **3.91°** | **3.91°** |
| above-ground z | 1.8623 … 2.9817 | 1.8317 … 2.9513 |

### ⚠ `audit.py` §87's numbers are STALE — do not cite them as a measurement
`audit.py:87` reads *"`lid_strut0` spans z 1.8994..3.0169 and `lid_board` 1.9381..2.9920"*. That
is a **rev-18 comment**. Since it was written: rev 38 added the **second** strut
(`98f3c3d`), rev 44b moved the **tip** from 0.86 → 0.97 of the width, and rev 44b/45 moved the
**foot** from a typed `y = +0.44` to the measured roof edge (`t1_shell.py:1296-1346`). My
arithmetic on the *current* constants gives a centreline span of **1.894 … 3.014 un-dropped**
and **1.862 … 2.982 above ground** — near the comment's numbers but reconciling with neither
frame exactly. **The rev-48 brief §2 quotes this comment as evidence the roof lids are open.
They are — but get the numbers from the build, not from the comment.**

## C.3 The three guards (`t1_shell.py:1374-1399`) — copy these

1. **Inside the lid's own x-span**: `min(LID_X0,LID_X1) <= xs_ <= max(LID_X0,LID_X1)`, else
   *"props nothing (SPEC 10.108)"*. `:1319-1322` records this guard **firing on and correctly
   rejecting** an attempted "sign-error fix".
2. **Lean < 20°** from vertical, else *"it rakes across the roof instead of standing under the
   board"*.
3. **Foot outside the aperture's y band** `(LID_Y_HINGE, LID_Y_HINGE + LID_W)`, else
   *"the strut is standing on nothing"* (SPEC 10.113).

## C.4 The lit strip along the lid edge — **IT IS NOT MODELLED ON THE LID**

IMG_2073 shows lit strip lighting along the roof lid's edge. In the source:

* **`t1_detail.bulb_string()`** (`t1_detail.py:2312-2335`) is the only lit strip in the model.
  It runs along the **drip rail**, `BULB_X0 = T._aft(-1.8000)` → `BULB_X1 = 1.7000`, at
  `z = (ZT_ALL(x) - RT_ALL(x)) + 0.01512`, `y = side * (WX(x)*G(z) + 0.0180)` — i.e. on the
  **body's gutter**, on the **show (+Y) side**. `BULB_PITCH = 0.0286` (measured by FFT,
  `:2292-2300`), `BULB_R = 0.0110`. Object name **`bulb_string`**; material **`bulb`**, emissive
  `(1.000, 0.760, 0.442)` at strength 9.0 (`t1_mats.py:1880`). Shipped via
  `spec4_details` (`t1_detail.py:3234`).
* The **roof lid's free edge** ends up at **y = −0.8135** (off side, high). The bulb string is on
  the **opposite** side of the vehicle from the lid's free edge. **They are not the same feature
  and nothing in the model puts light on the lid edge.**
* SPEC sec.1/0.2 as quoted at `t1_shell.py:1055-1057` says the lid has *"a row of round bulbs
  along the free edge"*. **That is stated in the docstring and NOT BUILT.** This is a genuine
  open gap that the rev-48 record has not flagged, and IMG_2073 is now the frame for it.

## C.5 ★ THE RECIPE — a numbered procedure for building an openable trunk lid

Written to be followed against `t1_shell.py` / `build.py`, mirroring `roof_lids()`.
**Do §F first**: if check 3 shows the panel is already a free island in `T1_body`, prefer
**route A**; if not, use **route B**.

**Constants block** — put these next to `ENGLID_GAP` (`t1_shell.py:855`), expressed in terms of
the seam, never re-typed (SPEC 10.25):
```python
TRUNK_HINGE_Z  = 0.8700 + 0.5000 / 2          # == 1.1200, the seam's TOP edge, un-dropped
TRUNK_HINGE_X  = T.X_TAIL                     # the tail skin plane
TRUNK_OPEN_DEG = None   # UNMEASURED -- see sec.D / PHOTOS_WANTED_rev47 #3
TRUNK_T        = 0.0028                       # == build.py's sol.thickness; do NOT re-type
```

1. **Decide the hinge.** A T1 engine lid hinges at its **TOP** and swings **UP and AFT** about a
   **transverse (Y-parallel)** axis at `x ≈ X_TAIL`, `z = 1.1200` un-dropped (1.1025 AG).
   **This is an inference from the vehicle type, not a measurement** — `PHOTOS_WANTED_rev47.md`
   #3 lists hinge side, axis, open angle, strut-vs-counterbalance and inner-face content as all
   unmeasured. **Record it as INFERRED and say so in the docstring.**
2. **Get the panel.**
   * **Route A (preferred, if §F check 3 confirms the island).** In `build.py`, immediately
     after the `kind="gap"` cut at `:254`, separate the trunk island out of `T1_body` by loose
     parts (bmesh walk from a seed vertex inside the seam's y/z box at x ≈ X_TAIL, or
     `bpy.ops.mesh.separate(type='LOOSE')` followed by picking the part whose bbox matches
     §B.3), name it **`lid_trunk`**. This inherits the shell's true curvature, its 2.8 mm
     thickness and its UVs **for free** and leaves an exactly-matching hole. **No new outline
     constant is introduced.**
   * **Route B (fallback).** Build a fresh panel the way `_lid_panel` does, but in the **(Y,Z)
     tail frame**: a grid over `ENGLID_GAP`'s bounding box inset by `GAPW/2`, at `x = X_TAIL`,
     SOLIDIFY `thickness = 0.0028`, `offset = -1.0` (inward, matching the shell), then apply.
     Route B costs a duplicated outline and will not match the tail's crown — Route A is
     strictly better if it is available.
3. **Write a `_hinge_y()` sibling of `_hinge()`.** `_hinge` (`t1_shell.py:1201`) rotates in the
   Y–Z plane about an X-axis. A trunk lid needs the **X–Z** plane about a **Y** axis:
   ```python
   def _hinge_y(ob, x_hinge, z_hinge, deg):
       a = math.radians(deg); ca, sa = math.cos(a), math.sin(a)
       for v in ob.data.vertices:
           x, z = v.co.x, v.co.z
           v.co.x = x_hinge + (x * ca - z * sa)      # sign chosen so the lid rises AFT
           v.co.z = z_hinge + (x * sa + z * ca)
       ob.data.update(); T.fix_normals(ob)
   ```
   **Bake into vertices. Never set `ob.rotation_euler`** — `build.py:851-856` asserts identity
   object transforms and will fire.
4. **Take the lid's mounted hardware with it.** `plate_1963` (`t1_detail.py:2421`) and
   `englid_handle` (`t1_detail.py:2586`) are both inside the seam. Apply the **same**
   `_hinge_y` with the **same** arguments to both, or they will float in the hole. Both are
   built in **step 7** (`build.py:766`), i.e. after the gap cut — so the pose has to be applied
   to them there, or the whole lid assembly deferred to step 7.
5. **Give the inner face something.** The roof lid's underside is the mural (`lid_board`,
   `lidmural`). The trunk lid's inner face is **unmeasured** (`PHOTOS_WANTED_rev47.md` #3).
   Do **not** invent artwork. `dark` or `steel` with the engine-bay void behind it is the
   defensible choice; state it as inferred.
6. **Close the hole behind it.** The same reasoning as `D.wheel_houses()`
   (`t1_detail.py:1278-1291`, rev 38 / SPEC 10.96): an aperture cut clean through the skin with
   **nothing behind it** shows the interior in plain sight, and that produced a real owner defect
   report. An open trunk needs an engine-bay backing. Note `PHOTOS_WANTED_rev44.md` §3: the
   owner's press reports say the **engine was scrapped and the transmission sold** — *"whatever
   is behind that lid is not a stock engine bay and I should not model it as one."*
7. **Prop it.** Copy `roof_lids`' strut recipe verbatim in structure: `T.cylinder(midpoint,
   axis, 0.0075, length, seg=14, name="trunk_strut0")`, tip at ~0.97 of the lid's travel onto
   the **free edge**, foot on **solid body**, material `chrome_d`. Whether the real vehicle uses
   a strut or a counterbalance is **unmeasured** — if you build one, say INFERRED.
8. **Write the guards in the same edit as the change** (project rule 12 / SPEC 10.108, 10.113).
   Minimum three, all measured on the BUILT mesh:
   * the lid's hinge-edge vertices are within 1 mm of `TRUNK_HINGE_Z` (it actually pivots on its
     own hinge line);
   * the lid's free edge has cleared the tail skin by > `GAPW` (it is actually open);
   * every strut foot is **outside** the seam's y/z box projected on the tail (it is not
     standing in the hole) — the direct analogue of `t1_shell.py:1393-1399`.
9. **Name everything `lid_trunk*` / `lid_*`.** `audit.py:96` excludes `lid_*` from the vehicle
   silhouette by prefix. A raised trunk lid named anything else will re-poison audit's
   overall-height row exactly as the raised roof strut did at rev 18 (`audit.py:82-88`).
10. **Re-run `verify.py` at BOTH subdivision levels and read the log for `gap_englid`.** See
    §B.6: this cut is the model's most fragile boolean and a rollback is reported only in
    `FAILED_CUTS`. Also re-check `verify.py` row 11e (`:1059-1064`) — once the panel is removed
    from `T1_body`, `_englid_frac` will read **100 % open**, which is correct but means the row
    no longer tests what it used to. Restate it rather than delete it.

---

# D. GIT ARCHAEOLOGY

## D.1 Was an openable trunk lid ever attempted and reverted? **NO. Never.**

`git log -L :engine_lid_gap:t1_shell.py` returns the function's **complete** history — three
commits, and it has been a `gap_prism` cutter in every one of them:

| commit | change |
|---|---|
| `fae1d5d` (baseline) | born as `T.gap_prism((-1.95,0,0), …, pts, GAPW, 0.55, name="gap_englid")` |
| `5629786` | outline hoisted to the module-level `ENGLID_GAP` constant. No behaviour change. |
| `bc165ff` (rev 16) | origin re-expressed as `T.X_TAIL + ENGLID_CUT_DX` after the tail re-space |

**No commit ever created a separate trunk-lid object, a trunk hinge, a trunk strut, or a trunk
open angle.** `git log -S 'trunk' -- '*.py'` returns only `9a227cd` and `b540abd` (rev 10/11),
which is when `lid_gen.py:12`'s prose sentence was written — prose, not geometry.

`git log -S 'roof_lid'` shows the roof lid's real history: `6f73dd3` (rev 8, *"kill the canvas
ragtop; roof lids OPEN"*), `df2cb7f` (rev 11, roof topology + *"the roof hole is never cut"*),
`98f3c3d` (rev 38, *"second lid strut added"*), `48e3143` (rev 45, *"the sign props stood in the
hole"*).

## D.2 What the record says about the trunk, oldest → newest

| when | document | what it says |
|---|---|---|
| rev 10/11 | `lid_gen.py:12` | *"There are **two roof lids plus a trunk lid**."* — prose, written while the topology was still 2-lid. |
| rev 11/12 | `SPEC.md` §10.26 (line 888) / `SPEC_rev22.md:704` | Three-panel table: front lid, main/mid lid, **trunk lid — "OPEN, at the tail" in `ref_side.jpg`, "closed" in `ref_rear34.jpg`, artwork "none"**. |
| rev 12 | `SPEC.md` §10.28 (line 937) / `t1_shell.py:1403-1442` | Owner **retires the front lid**: *"I was wrong, I think it is a detached sign."* Topology becomes **ONE** roof lid + one opening. **The trunk-lid row of 10.26's table is NOT adjudicated.** |
| rev 39-43 | `NEXT_CONTEXT_PROMPT_rev39.md:194`, `rev40:190`, `rev41:194`, `rev42:212`, `rev43:731` | Owner item 8, repeated verbatim four times: *"**a TRUNK LID, separate from the roof lids, and region C is that trunk lid, OPEN**"*, each time with `grep -c trunk t1_shell.py build.py` = **0 and 0**. |
| rev 43 | `AUDIT_rev43.md:118` and `:138` | **Two independent audit dimensions** (`roof` and `tail`) reach the same finding: *"The open lid at the tail (the owner's 'trunk lid', SPEC 10.26) does not exist in the model"* / *"The trunk lid at the tail, owner-stated and open in the primary frame, is not built"*. |
| rev 43 | `LEDGER_rev43.md:100` | Finding **16** opened: *"A trunk lid, separate from the roof lids — `grep -c trunk` is 0 and 0"*. |
| rev 44 | `PHOTOS_WANTED_rev44.md:49-57` | Asks for a head-on rear. Adds: *"press reports say the **engine was scrapped and the transmission sold**, so whatever is behind that lid is not a stock engine bay."* Also raises *"the main lid being raked the wrong way — the model leans the mural board away from the counter at 104°."* |
| rev 44 | `LEDGER_rev44.md:172` | Finding 16 *"re-confirmed by running it this revision"*. |
| rev 45 | `LEDGER_rev45.md:203`, `PHOTOS_WANTED_rev45.md:80-82` | Still open; *"raised twice"*. |
| rev 46 | `NEXT_CONTEXT_PROMPT_rev46.md:362, 382` | Still open. |
| rev 47 | owner, verbatim | ***"we're going to need the trunk open like it's in service"*** — becomes a requirement, not a finding. |
| rev 47 | `PHOTOS_WANTED_rev47.md:54-64` | Names the unmeasured four: hinge side/axis, open angle, strut vs counterbalance, inner-face content. *"No frame we hold shows it open."* |
| rev 47 | `LEDGER_rev47.md:212-229`, `:376` | §5, **NOT STARTED**. *"rev 48 must confirm it against the build before believing it."* |
| rev 47 | `LEDGER_rev47.md:373-378` (§10d) | IMG_2073 arrives: *"the vehicle **in service** with the roof lids raised on visible struts/cables and **lit strip lighting along the lid edge**. **This is the pose he wants.**"* |
| rev 48 | `NEXT_CONTEXT_PROMPT_rev48.md:73-92` | JOB 1. |

## D.3 ⚑ CONTRADICTIONS IN THE RECORD

1. **`lid_gen.py:12` is STALE and it is the sentence the rev-48 brief cites.**
   It says *"There are two roof lids plus a trunk lid"* — but that same file, four lines later
   (`lid_gen.py:14-19`), says the two are **the two FACES of ONE board**, and `t1_shell.py:1244`
   states outright: *"rev 12: **was two lids**. The second panel is a separate signboard, not a
   lid … **One lid, one opening.**"* **The brief's third bullet is quoting a retired topology.**
   `lid_gen.py:12` should be corrected in the same pass as JOB 1.
2. **`SPEC.md` §10.26's table was never fully adjudicated.** §10.28 retired row 1 (the front
   lid). Rows 2 and 3 stand as written. The **trunk lid row is the only surviving claim in the
   repo that the trunk lid is OPEN in `ref_side.jpg`** — and `ref_side.jpg` is a broadside, in
   which a tail lid is at best edge-on. That claim has **never been re-measured**, and
   `SPEC.md:1707-1708` already records one instance (§10.38) of this table being silently
   re-adopted after §10.28 superseded it.
3. **"region C is that trunk lid, OPEN"** (`NEXT_CONTEXT_PROMPT_rev39.md:194` and three
   repeats) is an **owner reading of a marked crop**, not a measurement, and it has been copied
   forward verbatim through five briefs without ever being re-checked.
4. **`audit.py:87`'s strut numbers are a rev-18 snapshot** quoted by the rev-48 brief as current
   evidence — see §C.2.

---

# E. THE INDEPENDENT CHECK THE RECORD OWES

**Claim** (`LEDGER_rev47.md:71, 292-293`; `NEXT_CONTEXT_PROMPT_rev48.md:122-123, 368-370`):
> *"`bulge = 0.019` in `t1_shell.nose_shape` is the ONLY forward bulge constant in the model."*

## E.0 Which axis is "forward"? **+X.**
`t1_core.py:12`: *"+X = forward (nose)"*. `X_NOSE = +2.108` (`:26`) vs `X_TAIL = −1.873`
(`:72`). Confirmed independently by `t1_shell.py:349` (*"+x is FORWARD"*).

## E.1 VERDICT: **CONFIRMED**, with two qualifications that must be stated

**CONFIRMED**: `bulge = 0.019` at **`t1_shell.py:1499`** is the **only positive (+X, outward)
geometric displacement constant applied to the body shell anywhere in the model.**

```
1494:        if x < 1.86:
1495:            continue
1496:        w = min(1.0, max(0.0, (x - 1.86) / 0.17))
1497:        w = w * w * (3 - 2 * w)
1498:        r = ((y / 0.80) ** 2 + ((z - 1.00) / 0.46) ** 2)
1499:        bulge = 0.019 * w * max(0.0, 1.0 - r)
1500:        d = z - zV(y)
1501:        s = 0.5 * (1.0 + math.tanh(d / 0.016))
1502:        step = -0.0062 * w * (1.0 - s)
1503:        v.co = Vector((x + bulge, y, z)) + v.normal * step
```
19 mm peak, smoothstep-blended over x 1.86 → 2.03, inside an ellipse centred (y=0, z=1.00) with
half-extents 0.80 in y and 0.46 in z.

### Qualification 1 — the SAME loop carries a NEGATIVE forward-axis constant
**`step = -0.0062` (`t1_shell.py:1502`)** displaces nose vertices **−6.2 mm along their own
normal**, which on the nose's front face is very nearly −X. It is the **pressed V-swage** (a
recess), so it is not a *bulge* — but it **is** a constant that moves nose geometry along the
forward axis. If anyone reads the claim as *"the only constant that moves the nose in X"*, it is
**REFUTED by −0.0062**. Read as *"the only forward BULGE"*, **CONFIRMED**. State which reading
you mean.

### Qualification 2 — the nose's *plan curvature* is also set by the `WX` LUT
The thing the owner reported (*"the nose of the car is too flat"*) is **plan curvature**: how far
the metal stands forward as a function of y. That is set by **two** things, not one:
`bulge` (19 mm, an added dome) **and** the loft's front stations. But **`WX` displaces in Y, not
X** (see E.2), so it changes the *edge roll*, not the forward stand-off. **`bulge` really is the
only lever on forward stand-off.** The claim survives — but the fix for "too flat" is not
necessarily to raise `bulge`; it may be to add stations forward of 2.108.

## E.2 How the check was made exhaustive

1. **Every site in the modelling files that writes a vertex x.** `grep -rn "co\.x *+=|co\.x *=|
x + bulge|Vector((x +"` over `t1_shell.py t1_core.py t1_detail.py build.py` returns exactly
   **five**, and only one is on the nose:
   * `t1_shell.py:1503` — **the bulge.** ← the only nose one
   * `t1_shell.py:988` — `v.co.x += 0.2000`, the **cargo-door mid-split** cutter, off side
   * `t1_core.py:1154` — `v.co.x += dx` inside **`drape_x()`**, which drapes the **VW roundel
     plate** (a separate object) onto the nose at `standoff = 0.0016` (`build.py:733`). It moves
     an **added part**, not the shell.
   * `t1_detail.py:1287` — `v.co.x += xa`, the **wheel-house** liners' station offset
   * `build.py:538` — `v.co.x = -v.co.x`, mirroring the **tail lamp** revolve
2. **The loft cannot displace in x.** `t1_core.ring()` (`:~1290`) returns
   `pts = [(x, y, z) for (y, z) in half]` — **x is the station and is constant across the whole
   ring**. Every longitudinal LUT (`ZB :388`, `ZT_ALL :399`, `RT_ALL :450`, `CR_ALL :456`,
   `WX :490`, `G :214`) returns a **z or a y**, never an x. `bcrown=0.012` and `crown` act inside
   `section()`, in the y–z plane only. So the shell's front face is a **planar Coons cap at
   x = 2.108** (`STATIONS[-1]`, `t1_core.py:477`; `_coons_cap`, `t1_core.py:~264`).
   *Historical note worth recording:* `t1_core.py:~250` says the **retired** n-gon cap
   *"pulls the flat tail face 1.4 mm forward of its authored plane"* — that WAS a second,
   accidental forward displacement, and it was **fixed at rev 16**. It is gone.
3. **Nothing downstream moves x.** After `nose_shape` (`build.py:235`) the pipeline is: arch cut →
   solidify → apertures → gaps → roof hole → headlamp bowls → details → decals → **step 8b**.
   Step 8b (`build.py:872-882`) is `v.co.z -= (RAKE_Z0 + RAKE_DZDX * v.co.x)` — **z only**;
   `build.py:846-847` states the drop is *"a shear in x"* meaning *parameterised by* x, and
   `t1_core.py:99-101` explicitly rejects a rotation precisely because *"a 1.9 deg rotation would
   also shift x by 63 mm at roof level"*. **The model deliberately never shifts x.**
4. **No displacement modifiers or displacement shaders anywhere.**
   `grep -rn "'DISPLACE'|\"DISPLACE\"|displacement"` over the five modelling files returns
   **one** hit, `t1_detail.py:2564`, and it is the word "displacement" in a **prose comment**
   about a pixel measurement. `MT.round_edges()` (`build.py:894`, `t1_mats.round_edges`) splices
   a **Cycles Bevel node into the Normal input** — *shading normals only, no geometry*.
5. **No env var and no dead code path.** `os.environ` across the five files yields
   `T1_VENTDROP, T1_BPILLAR, T1_ENGLID_DX, T1_SIGNBOARD, T1_NHALF57, T1_GAL_SKY, T1_GAL_LUM,
   T1_SUB, T1_HL_BOWL, T1_HL_BEZEL, T1_SAVE, T1_VERIFY, T1_ABLATE, T1_PREVIEW, T1_NOBEVEL, …` —
   **none touches the nose in x.** `t1_core.build_cab()` (`:1322`) and `build_bed()` (`:1330`) are
   the pickup variants and are **never called** (`grep` for call sites: none).
6. **`t1_mats` X-gates are texture selectors, not geometry.** `t1_mats.py:1478` (`X > 1.60`) and
   `:1527` (`X < -1.60`) select which decal/paint mix a shading point gets. No displacement.

## E.3 Decoys — other occurrences of `0.019` that are NOT bulges

So the next context does not `grep 0.019` and think it found a second one:
* `t1_detail.py:1357` `COL_R = 0.019` — **steering-column radius**.
* `t1_detail.py:855` `(0.019, R + 0.0060)` — a **coordinate in a revolve profile**.
* `t1_detail.py:109` `(-0.0190, 0.1900)` — a **hubcap profile coordinate**.

## E.4 Separate parts that stand proud of the nose in +X (added geometry, not shell bulges)

Listed so they are not mistaken for bulge constants: the **VW roundel** (`build.py:733`,
`standoff = 0.0016`, guarded to stand 0.5–30 mm proud at `:750-757`), the **headlamps**
(`HL_X = 2.1015`, `build.py:219`), the **indicator pods** (`IND_DY/IND_DZ`, `build.py:442-443`),
the **front bumper** (`X_BUMP_F = 2.140`, `t1_core.py:73`).

---

# F. WHAT TO LOOK FOR IN THE BUILT SCENE — ONE PASS

**I did not run this. The main context must.** Paste into a `bpy` session on the built scene
(e.g. `T1_SAVE=x.blend` then open, or append to `build.py` before `T1_SAVE`).

```python
# ===================================================================
#  rev 48 -- LID TOPOLOGY, ONE PASS.  Read-only: it changes nothing.
# ===================================================================
import bpy, bmesh
from mathutils import Vector
import t1_shell as S, t1_core as T

P = print
def bb(ob):
    vs = [ob.matrix_world @ v.co for v in ob.data.vertices]
    lo = Vector((min(v[i] for v in vs) for i in range(3)))
    hi = Vector((max(v[i] for v in vs) for i in range(3)))
    return lo, hi

# ---------------------------------------------------------------- 1
# WHICH LID OBJECTS EXIST AT ALL.
# EXPECT: lid_main, lid_board, lid_rail, lid_rail.001, lid_strut0, lid_strut1,
#         T1_body, englid_handle, plate_1963, fuel_flap, bulb_string.
# MEANING: any name containing "trunk" or "englid" that is a PANEL (not the
#   handle) would mean a trunk lid object already exists -- it does not,
#   per the source.  Absence of lid_strut1 would mean rev 38's second strut
#   silently regressed.  Presence of sign_panel means T1_SIGNBOARD leaked on
#   and the hero is invalid (SPEC 10.28).
P("=== 1. LID-LIKE OBJECTS ===")
for o in sorted(bpy.data.objects, key=lambda o: o.name):
    if o.type != 'MESH':
        continue
    n = o.name.lower()
    if any(k in n for k in ("lid", "sign", "englid", "trunk", "flap",
                            "hinge", "vent", "plate", "bulb", "t1_body")):
        lo, hi = bb(o)
        P("  %-22s %6dv  x[%+.4f,%+.4f] y[%+.4f,%+.4f] z[%+.4f,%+.4f]"
          % (o.name, len(o.data.vertices), lo.x, hi.x, lo.y, hi.y, lo.z, hi.z))

# ---------------------------------------------------------------- 2
# THE ROOF LID IS ACTUALLY OPEN, AND THE STRUTS ARE AS THE SOURCE PREDICTS.
# EXPECT (ABOVE GROUND, i.e. after step 8b's shear):
#   lid_main   free edge near y = -0.81, top z ~ 2.98-3.00
#   lid_strut0 x = -0.9100, z ~ 1.862 .. 2.982, lean ~ 3.9 deg
#   lid_strut1 x = +0.8040, z ~ 1.832 .. 2.951, lean ~ 3.9 deg
# MEANING: if lid_main's z span is ~1.95..1.99 (flat), the lid is CLOSED and
#   the whole rev-48 premise is wrong.  If the struts lean > 20 deg the rev-44b
#   fix regressed.  Compare against audit.py:87's 1.8994..3.0169 -- that comment
#   is a REV-18 snapshot and is expected NOT to match exactly (report C.2).
P("=== 2. ROOF LID POSE (built, dropped frame) ===")
import math
for nm in ("lid_main", "lid_board", "lid_rail", "lid_rail.001",
           "lid_strut0", "lid_strut1"):
    o = bpy.data.objects.get(nm)
    if not o:
        P("  %-14s ABSENT" % nm); continue
    lo, hi = bb(o)
    P("  %-14s x[%+.4f,%+.4f] y[%+.4f,%+.4f] z[%+.4f,%+.4f]"
      % (nm, lo.x, hi.x, lo.y, hi.y, lo.z, hi.z))
    if nm.startswith("lid_strut"):
        lean = math.degrees(math.atan2(hi.y - lo.y, hi.z - lo.z))
        P("       lean from vertical %.2f deg   (guard: < 20)" % lean)

# ---------------------------------------------------------------- 3
# *** THE DECIDING CHECK ***  IS THE TRUNK LID A SEPARATE ISLAND INSIDE T1_body?
# build.py:69-70 claims the gap cutters take T1_body from 1 -> 6 connected
# components.  This counts them and prints each one's bbox.
# MEANING:
#   * >= 6 components, one of them with bbox x ~ -1.88..-1.87, y within
#     +-0.470, z within 0.60..1.11 (AG)  ->  THE TRUNK LID IS ALREADY A FREE
#     2.8 mm SLAB sitting in its hole.  Use RECIPE ROUTE A: separate by loose
#     parts, name it lid_trunk, hinge it.  No new outline constant needed.
#   * exactly 1 component  ->  the gap boolean did NOT free the panel (or was
#     rolled back).  Check the build log for "gap_englid".  Use ROUTE B.
#   * a component whose bbox matches the seam but is only a SHELL (no inner
#     face) -> the cut only reached one skin; the lid has no thickness.
P("=== 3. T1_body CONNECTED COMPONENTS  <-- THE DECIDING CHECK ===")
body = bpy.data.objects["T1_body"]
bm = bmesh.new(); bm.from_mesh(body.data)
seen, comps = set(), []
for v0 in bm.verts:
    if v0.index in seen:
        continue
    stack, comp = [v0], []
    seen.add(v0.index)
    while stack:
        v = stack.pop(); comp.append(v)
        for e in v.link_edges:
            o = e.other_vert(v)
            if o.index not in seen:
                seen.add(o.index); stack.append(o)
    comps.append(comp)
P("  T1_body has %d connected components (build.py:69 predicts 6)" % len(comps))
for c in sorted(comps, key=len, reverse=True):
    xs = [v.co.x for v in c]; ys = [v.co.y for v in c]; zs = [v.co.z for v in c]
    tag = ""
    # the trunk-lid signature: on the tail plane, inside the seam's y/z box
    if (max(xs) < -1.70 and max(abs(min(ys)), abs(max(ys))) < 0.50
            and min(zs) > 0.55 and max(zs) < 1.20):
        tag = "   <== TRUNK LID PANEL"
    P("   %7dv  x[%+.4f,%+.4f] y[%+.4f,%+.4f] z[%+.4f,%+.4f]%s"
      % (len(c), min(xs), max(xs), min(ys), max(ys), min(zs), max(zs), tag))
bm.free()

# ---------------------------------------------------------------- 4
# THE SEAM IS A REAL THROUGH-SLOT, NOT A SHADING LINE.
# Fires +X rays from behind the vehicle at every ENGLID_GAP sample.
# EXPECT: ~100% of 28 samples get past x = X_TAIL + 0.158 = -1.7150.
# MEANING: < ~90% means the gap boolean was partially rolled back.  100% AFTER
#   you separate the lid is expected and correct -- verify.py row 11e will then
#   be testing a hole, not a seam, and must be RESTATED (report C.5 step 10).
P("=== 4. SEAM OPENNESS (verify.py row 11e, re-run here) ===")
dz = -(T.RAKE_Z0 + T.RAKE_DZDX * T.X_TAIL)     # authored -> above-ground
thru = T.X_TAIL + S.ENGLID_CUT_DX
ok = 0
for (y, z) in S.ENGLID_GAP:
    hit, loc, _, _ = body.ray_cast(Vector((-3.0, y, z + dz)), Vector((1, 0, 0)))
    if (not hit) or loc.x > thru:
        ok += 1
P("  englid seam: %d/%d samples open (%.0f %%), thru-plane x=%.4f"
  % (ok, len(S.ENGLID_GAP), 100.0 * ok / len(S.ENGLID_GAP), thru))

# ---------------------------------------------------------------- 5
# WHERE THE TAIL SKIN ACTUALLY IS, AND HOW FLAT IT IS OVER THE SEAM.
# EXPECT: x ~ -1.873 everywhere inside the seam box, varying by only a few mm.
# MEANING: a flat tail face means a trunk lid can be a planar panel hinged
#   about a single Y-parallel axis.  If x varies by > ~20 mm the panel is
#   crowned and ROUTE A (separate the real island) is the only sane option.
P("=== 5. TAIL SKIN FLATNESS OVER THE SEAM ===")
xs = []
for y in (-0.44, -0.22, 0.0, 0.22, 0.44):
    for z in (0.65, 0.80, 0.95, 1.09):
        hit, loc, nor, _ = body.ray_cast(Vector((-3.0, y, z + dz)),
                                         Vector((1, 0, 0)))
        if hit:
            xs.append(loc.x)
            P("   y=%+.2f z=%+.2f -> skin x=%+.4f  n=(%.3f,%.3f,%.3f)"
              % (y, z, loc.x, nor.x, nor.y, nor.z))
if xs:
    P("  tail skin x over the seam: %.4f .. %.4f  (spread %.1f mm)"
      % (min(xs), max(xs), (max(xs) - min(xs)) * 1000))

# ---------------------------------------------------------------- 6
# WHAT IS MOUNTED ON THE LID AND MUST TRAVEL WITH IT.
# EXPECT: englid_handle and plate_1963 both inside y +-0.47, z 0.60..1.11 AG.
# MEANING: anything listed here has to receive the SAME hinge transform, or it
#   will float in the open hole.  Both are built in build.py step 7, AFTER the
#   gap cut -- so the pose must be applied there (report C.5 step 4).
P("=== 6. HARDWARE ON THE TRUNK LID PANEL ===")
for nm in ("englid_handle", "plate_1963"):
    o = bpy.data.objects.get(nm)
    if not o:
        P("  %-14s ABSENT" % nm); continue
    lo, hi = bb(o)
    inside = (hi.y < 0.48 and lo.y > -0.48 and lo.z > 0.58 and hi.z < 1.14)
    P("  %-14s x[%+.4f,%+.4f] y[%+.4f,%+.4f] z[%+.4f,%+.4f]  on-lid=%s"
      % (nm, lo.x, hi.x, lo.y, hi.y, lo.z, hi.z, inside))

# ---------------------------------------------------------------- 7
# THE LIT STRIP.  Report C.4 says the model's only lit strip is on the DRIP
# RAIL (show side, +Y), NOT on the roof lid's free edge (which is at y ~ -0.81).
# EXPECT: bulb_string y all POSITIVE, z ~ 1.85-1.90 AG.
# MEANING: if so, IMG_2073's "lit strip along the lid edge" is UNBUILT, and
#   t1_shell.py:1056's own docstring ("a row of round bulbs along the free
#   edge") is an unimplemented spec line -- a real, unlogged gap.
P("=== 7. LIT STRIP -- DRIP RAIL OR LID EDGE? ===")
o = bpy.data.objects.get("bulb_string")
if o:
    lo, hi = bb(o)
    P("  bulb_string x[%+.4f,%+.4f] y[%+.4f,%+.4f] z[%+.4f,%+.4f]"
      % (lo.x, hi.x, lo.y, hi.y, lo.z, hi.z))
    P("  -> on the LID free edge?  %s   (lid free edge is at y ~ -0.81)"
      % ("YES" if lo.y < -0.60 else "NO -- drip rail only"))
else:
    P("  bulb_string ABSENT")

# ---------------------------------------------------------------- 8
# ROLLED-BACK CUTS.  gap_englid is the most fragile boolean in the model
# (t1_core.py:230-244).  A rollback is reported ONLY here.
# MEANING: "gap_englid" in this list => the seam does not exist this run and
#   every number above about the trunk lid is meaningless.
P("=== 8. FAILED CUTS ===")
try:
    P("  " + (", ".join(FAILED_CUTS) if FAILED_CUTS else "none"))
except NameError:
    P("  (FAILED_CUTS not in scope -- read it from the build log instead)")
```

## F.1 What proves it, in one line each

| result | conclusion |
|---|---|
| Check 3 finds a component with bbox `x ≈ −1.88…−1.87, |y| ≤ 0.470, z 0.60…1.11` | **The trunk lid IS already a separate 2.8 mm slab** inside `T1_body` — only unnamed and unposed. **Route A.** |
| Check 3 finds exactly 1 component | The gap boolean did not free the panel (or rolled back). **Route B**, and read check 8. |
| Check 1 finds **no** object whose name contains `trunk` | Confirms the source: **no trunk lid object exists.** (Expected. `englid_handle` will match `englid` and is the *handle*, not the lid.) |
| Check 2 shows `lid_main` spanning z ≈ 1.95 … 3.00 | The roof lids **are** open, as the brief claims. If z spans only ~1.95 … 1.99 the premise is wrong. |
| Check 4 shows ~100 % open at 28/28 | The seam is a real through-slot, not a shading line. |
| Check 5 spread ≲ 20 mm | The tail face is planar over the seam ⇒ a single Y-parallel hinge axis at `z = 1.1025` AG works. |
| Check 7 reports "NO — drip rail only" | IMG_2073's lit lid-edge strip is **unbuilt**, and `t1_shell.py:1056` promises it. New finding. |

---

## APPENDIX — the four things about the trunk lid that are STILL UNMEASURED
(`PHOTOS_WANTED_rev47.md:54-64`; nothing found in this pass changes any of them)

1. **Hinge side and axis.** Inferred top-hinged, transverse — from the vehicle type only.
2. **Open angle.** No value exists anywhere in the repo.
3. **Strut-held or counterbalanced.** Unknown.
4. **What the inner face carries.** Unknown; and `PHOTOS_WANTED_rev44.md:57` warns the engine was
   scrapped, so it is **not** a stock engine bay.

**No frame in the repo shows the trunk open.** `IMG_2073.jpeg` is the pose reference for the
**roof** lids only (`LEDGER_rev47.md:373-378`).
