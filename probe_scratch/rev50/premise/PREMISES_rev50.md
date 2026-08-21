# REV 50 — PREMISE VERIFICATION OF THE "DO NOW" LIST

Tree: `claude/combi-render-setup-dkgwme` @ `868c72d` (rev 49g). Nothing tracked was
modified. No Blender was run. Every line number below is HEAD's, read with
`sed -n`, and every number is recomputed by hand from the literals quoted.

**One structural fact that governs the whole report.** The only source file that
changed after the survey landed (`5b28472`) is *none* — `git diff --name-only
5b28472 HEAD` returns three markdown/text files only. Going back further, the only
`.py` that changed between the roof-lids agent's tree (`ae526d7`) and HEAD is
`t1_shell.py`, and only in `tail_board()` / `tail_board_stay()` (`git diff --stat
ae526d7 HEAD -- '*.py'` → `t1_shell.py | 171 ++++---`). So **exactly one A-list
premise can have gone stale by a later commit, and it is the tail board's.**
Everything else I verified by reading HEAD directly.


> ### ⚠ CONCURRENCY NOTE — READ THIS FIRST
>
> **This report is against `HEAD` = `868c72d`. Every line number and every literal
> quoted below was checked against `git show HEAD:<file>` after the fact and matches.**
>
> While I was working, another agent began writing rev-50 fixes into the **working
> tree**. At the time I finished, `git status --porcelain` showed `M lid_gen.py` and
> `M t1_shell.py` (uncommitted). Those edits implement **A1** (`LID_OPEN_DEG`
> `104.0` → `float(os.environ.get("T1_LIDDEG", 76.0))`, plus a new built-panel lean
> guard and a signed `_roof_edge_y` that re-foots the props on the SHOW side) and
> **A16's `&` clamp** in `lid_gen.py`. I did not touch them and I did not read them
> as evidence.
>
> Two consequences for whoever reads this:
> 1. **A1's premise is verified against HEAD and is TRUE there.** The working tree
>    already carries a candidate fix. My §2 A1 guard analysis — that a bare
>    `LID_OPEN_DEG` change trips the rev-45 Y-guard and that a show-side stay trips
>    the rev-44b lean guard — is exactly the problem that working-tree diff is
>    solving, and it appears to solve it by re-footing the prop rather than by
>    relaxing either guard. That is the right shape.
> 2. **`verify_clone.sh`'s `ALL 122 PASS` was obtained on a CLEAN tree**, before
>    those edits landed (row `verify_clone.sh:86` is `ck "modified tracked files" 0`,
>    and it passed). It will now report that row red until the edits are committed.
>

---

## 1. THE TABLE

| item | premise as written | verdict | the machine's actual value |
|---|---|---|---|
| **A1** | `LID_OPEN_DEG = 104.0` tips the lid away from the counter | **HOLDS** | `t1_shell.py:1078` = `104.0`. Free edge y = **−0.81353**, roof edge Yt = **0.72726** → **86.3 mm outboard** |
| **A1b** | `LID_W = 1.110` too narrow (needs ≥1.19 m) | **HOLDS (source half)** | `t1_shell.py:1077` = `1.1100`; `W·sinα` = 1.077 m |
| **A1c** | the rev-44b lean guard forbids the corrected geometry | **HOLDS — and it is worse than stated** | `assert lean < 20.0` at **t1_shell.py:2234**. Photographed stay = **36.4–42.9°**. AND the rev-45 Y-guard at **2243** fires first on any α<90° |
| **A2** | disc crosses in front of cap at r ≈ 0.120 | **HOLDS** | crossover recomputed **r = 0.11973 m** → visible **Ø239.5 mm** vs built **Ø274.0 mm**, ratio **0.8739** |
| **A2b** | `CAP_R` is LOCKED | **HOLDS** | `t1_detail.py:165` `CAP_R = 0.1345 … Do not touch.` |
| **A3a** | four wheels placed with no rotation about the axle | **HOLDS** | `build.py:360` `D.place(o, loc=(x, s*tr/2, T.TIRE_R))` — no `rot=` |
| **A3b** | WEATHER/MOTTLE fed **Object** coords ⇒ the wear field clones too | **FALSE (mechanism refuted)** | `place()` **bakes** into vertices; `build.py:858` + assert `:867` prove every mesh carries an **identity transform**, so Object coords **are world coords**. Four wheels sample four different points of the field |
| **A3c** | `MOTTLE_OFS` exists as a declared no-op and is half the fix | **PARTIAL** | exists, `t1_mats.py:662` default `"0,0,0"`; but it is **module-global**, applied inside **`body_paint()` only** (`t1_mats.py:1424-1432`) — it never touches `capred`/`wheelcream`/`tyre` |
| **A8a** | handle 46.8 mm below the lid's lower shut line | **HOLDS** | handle z = **0.573219**, `ENGLID_GAP` lower line z = **0.620000** → **−46.78 mm** (below) |
| **A10b** | `small_lamp()` starts on the axis; placed 4.0 mm inside the skin | **HOLDS** | `t1_detail.py:921-926` first point `(0.000, 0.0000)`; `build.py:564` `x = T.X_TAIL + 0.0040` → **18.11 %** of the lamp radius buried = **Ø33.2 mm** red disc |
| **A10c** | lamp z above `PLATE_OUTER_CZ` | **HOLDS** | `build.py:564` z = **0.8250**, `PLATE_OUTER_CZ` = **0.787544** → **+37.46 mm ABOVE** (= +0.2226 plate heights) |
| **A9** | every galley feature ~106 mm too far aft | **HOLDS, but the offset is NOT rigid** | per-feature **−0.0957 … −0.1103 m**; REF map reproduced to **0.4–1.3 mm** on all six S-hooks |
| **A9b** | finding 28 (`gal_rail`) is separate | **HOLDS — and its headline mis-signs the length** | rail spans **−0.050 … −0.710**; aftmost hook **−0.907**; centre **+0.218 m** forward; length **0.660 vs 0.495 = 165 mm too LONG, not short** |
| **A9c** | finding 29 (`gal_caddy_fill` sign) is separate | **HOLDS** | `t1_detail.py:3325-3326`: fill spans **−1.0300…−1.1670** (137 mm) inside a **113 mm** caddy |
| **A11** | handle z = 1.330 twice vs `Z_BELT_AUTH` 1.2720 | **HOLDS (three occurrences, not two)** | `t1_detail.py:1864, 1865, 1870`; `t1_mats.py:144` = `1.2720`; offset **+58.0 mm**, station-independent |
| **A14a** | both `lid_rail` objects zero-area | **HOLDS** | `t1_shell.py:2122-2124` `xa == xb`, `nx=1`; `_rag_grid` `t1_shell.py:1016` `x = x0 + (x1 - x0) * ix / nx` |
| **A14b** | `gutter()` defined twice | **HOLDS** | `t1_detail.py:944` and `:1717`; `build.py:403` binds the later |
| **A14c** | `moulding()` called by nothing | **HOLDS** | `grep -rn moulding --include=*.py .` → **one hit**, its own `def` at `t1_detail.py:962` |
| **A19a** | headlamps + indicators placed with zero rotation | **HOLDS** | `build.py:506`, `:520`, `:521` — no `rot=` on any of the five parts |
| **A19b** | headlamp bore axis is +X both sides | **HOLDS** | `t1_shell.py:466-469` extrude direction `(-1, 0, 0)`, plane `(0,s,0)×(0,0,1)` |
| **A19c** | `IND_X` is the bare literal 2.0960 typed twice | **HOLDS** | `build.py:520` and `:521`; no `IND_X` symbol exists anywhere |
| **A18a** | `hero.py:112` sets `T1_FX=0`; studio gates the shadow on it; post has none | **HOLDS** | `hero.py:112` `"T1_FX": "0"`; `studio.py:762` `on = optics and _envi("T1_FX", 1)`; `studio.py:823` `if on and _sh > 1.0:`; `grep -n shadow post.py` → **nothing** |
| **A18b** | `bg_white_level` returns 24.87 and it clips | **HOLDS / render-dependent** | `studio.py:721-723` returns **24.87** for AgX+Punchy. The clip itself is a render measurement I could not repeat |
| **A18c** | the DIRECT path carries the shadow | **HOLDS** | `build.py` never sets `T1_FX`; the default in `_envi("T1_FX", 1)` is **1**. Defect is latent on the strip path only |
| **A5a** | body finish literals; Coat Roughness 10× out of family | **HOLDS** | `t1_mats.py:1694` Rough **0.420**, `:1699-1700` Spec IOR `T1_SPEC` default **0.50**, `:1701` Coat Weight **0.02**, `:1702` Coat Roughness **0.300**; `simple()` `t1_mats.py:714` hard-sets **0.030** for all **nine** coated materials. Repeated verbatim for `calidad` at `:1778-1783` |
| **A6a** | both WEATHER gates saturate at Pointiness = 1.0 | **HOLDS** | `t1_mats.py:962` `_mr(PT, 0.520, 0.600, 0, 1)` → 1.0; `:974` `_mr(pw, 0.80, 1.00, 0, 1)` → 1.0 |
| **A6b** | `apply_weather` links Metallic only when wear > 0 | **HOLDS** | `t1_mats.py:1143-1144` |
| **A6c** | `T1_CTAN_WEAR` exists; `WEAR['countertan'] = 0.7` | **HOLDS** | `t1_mats.py:1980-1981`; `t1_mats.py:681` |
| **A7** | `gal_end_a` at x −1.300 vs `X_TAIL` −1.873; 573 mm undressed | **HOLDS — and there is a second hole nobody named** | `t1_detail.py:3089` `X0 = -1.3000`; `:3101`; `X_TAIL = -1.873` → **573.0 mm**. `gal_end_a` spans y **−0.500…+0.400** against a rear aperture of **±0.520** — **120 mm of the aperture's show side sees past the end wall entirely** |
| **TAIL BOARD FOOT** | survey finding 6: foot buried 63–75 mm, guard is a tautology | **PREMISE FALSE — already fixed at rev 49d** | `_crown = T.ZT_ALL` is **gone** (`grep -c` = 0 at `39f3301` onward); station solved from `T1_body` vertices at `t1_shell.py:1651-1663` |
| **verify_clone rows** | "ALL 113 PASS" | **FALSE — it is 122** | I ran it: `ALL 122 PASS`, exit 0. Brief §1 says 113, brief §12 says 122 — the brief contradicts itself |
| **verify_clone "none relaxed"** | no row was relaxed | **PARTIAL** | one grep window widened `-A 3` → `-A 30`; the commit that did it **says so** and adds three compensating rows |

---

## 2. THE DETAIL

### A1 — the mural lid's rake, and whether it can be fixed at all

`t1_shell.py:1075-1078`:

```
LID_X0, LID_X1 = 0.9640, -1.0700       # main lid opening, fore-aft
LID_Y_HINGE = -0.5450                  # off-side edge of the opening
LID_W = 1.1100                         # across, hinge -> free edge
LID_OPEN_DEG = 104.0                   # past vertical, leaning over the counter
```

The swing sign. `_hinge` (`t1_shell.py:1201-1208`):

```
v.co.y = y_hinge + (y * ca - z * sa)
v.co.z = z_hinge + (y * sa + z * ca)
```

`_lid_face` / `_lid_panel` build the panel in the hinge frame with **y running
0 → w** (`t1_shell.py:1216-1217`, `yv = inset + (w - 2*inset)*iy/ny`), so the free
edge is at local y = `LID_W` and lands at

    y_free = −0.5450 + 1.1100·cos(104°) = **−0.813533**

I recomputed `Yt` at the lid's mid-station x = −0.0530 from `t1_core`'s own LUTs
(`ZT_ALL`, `RT_ALL`, `WX`, `G`, all re-typed into `probe_scratch/rev50/premise/prof.py`):
**Yt = 0.727261**. So the free edge is **86.3 mm outboard of the off-side roof
edge**, on the far side from the counter. The comment on line 1078 and SPEC §135
say the opposite. Premise holds exactly as written.

**`LID_W`.** `t1_shell.py:1077` is still `1.1100`. `W·sinα = 1.1100·sin104° =
1.07715 m` against finding 49's floor of `≥1.187 m`. The *source* half of the
premise holds; the photographic half is finding 49's own image measurement, which
I did not re-derive (see §5).

**THE GUARD QUESTION — and this is the load-bearing part of A1.**
Two guards sit downstream of `LID_OPEN_DEG`, not one:

* `t1_shell.py:2234` — rev-44b: `assert lean < 20.0`
* `t1_shell.py:2243` — rev-45/SPEC 10.113: `assert not (_y_lo < _fy < _y_hi)`
  with `_y_lo, _y_hi = LID_Y_HINGE, LID_Y_HINGE + LID_W` (line 2240)

The foot is `footy = max(tipy, _roof_edge_y(xs, LID_Y_HINGE))` (`t1_shell.py:2213`),
and `_roof_edge_y` walks in **−y** only. I simulated both guards by hand against the
real `roof_z`:

| α | tip y | foot y | lean | foot inside aperture? | photographed-stay lean (foot on show-side roof edge y=+0.7263) |
|---|---|---|---|---|---|
| **104° (built)** | −0.8055 | −0.7290 | **3.91°** | no | 53.8° |
| 78° | −0.3211 | **−0.3211** | 0.00° | **YES → 2243 FIRES** | **42.9° → 2234 FIRES** |
| 70° | −0.1767 | **−0.1767** | 0.00° | **YES → 2243 FIRES** | **39.7° → 2234 FIRES** |
| 61° | −0.0230 | **−0.0230** | 0.00° | **YES → 2243 FIRES** | **36.4° → 2234 FIRES** |

**Answer to the question asked: yes, and by two guards, not one.**
Changing `LID_OPEN_DEG` *alone* to anything under 90° makes `max()` pick `tipy`, the
prop becomes a vertical rod standing in mid-air over the open hatch, and the rev-45
Y-guard aborts the build. Re-footing the props on the show-side roof edge — which is
what finding 48 says the photographs show — puts the lean at **36–43°** and the
rev-44b guard aborts the build. **A1 cannot be shipped without touching the props
and both guards in the same edit.** The already-right list explicitly blesses both
guards ("both do what they say"), so this is a rule-5 job: keep each rationale,
replace each shape.

*Ceiling:* I could not verify the **photographic** basis for α = 61–78° (the −5.3 %
taper) or for `LID_W ≥ 1.19 m`; both are image measurements on `ref_side.jpg` and
re-deriving them needs the frame, not the source.

---

### A2 — the hubcap five-petal flower

Both profiles, read verbatim.

`rim()`, `t1_detail.py:103-104`: `FLANGE_AUTHORED = 0.1905`; `S = T.RIM_R /
FLANGE_AUTHORED`. `T.RIM_R = 0.2198` (`t1_core.py:82`) → **S = 1.153806**.

Disc, `t1_detail.py:118-122` then `:123` `disc_prof = [(y, r * S) for (y, r) in
disc_prof]` — **radius scaled, `y` untouched**:

```
(0.0500, 0.1600), (0.0560, 0.1560), (0.0570, 0.1400),
(0.0520, 0.1200), (0.0450, 0.0900), (0.0430, 0.0620),
(0.0450, 0.0400), (0.0470, 0.0000)
```

Cap, `t1_detail.py:175-183`, a separate `T.revolve`, **no S anywhere**:

```
(0.0745, 0.0000), … (0.0378, 0.1288), (0.0236, 0.1342), (0.0120, R),
(0.0040, R + 0.0025), …
```

Interpolating both and solving `disc(r) − cap(r) = 0` myself:

```
r=0.1180  disc 0.04786  cap 0.05020  → -2.34 mm
r=0.1197  disc 0.04821  cap 0.04825  →  0.00 mm   <-- crossover
r=0.1200  disc 0.04827  cap 0.04790  → +0.36 mm
r=0.1288  disc 0.05005  cap 0.03780  → +12.25 mm
r=0.1370  disc 0.05171  cap 0.00400  → +47.71 mm
```

**Crossover r = 0.119731 m.** Visible Ø **239.5 mm** against a built cap Ø
**274.0 mm** (`CAP_D = 2*(CAP_R+0.0025)`), ratio **0.8739**. This reproduces
finding 7's 0.1197 to 0.03 mm and finding 12's 0.1200 to 0.3 mm, from the source
alone. Premise holds.

`CAP_R` at `t1_detail.py:165`: `0.1345  # hubcap dome radius.  LOCKED: hubcap D /
tyre D measures 0.4134 against 0.4211 built … Do not touch.` — confirmed LOCKED,
and the already-right list independently confirms it ("Do not shrink or grow
CAP_R").

**Which surface must move.** Not the cap's radius. The two revolves are placed at
the *same* y-origin (`build.py:360` places every wheel part with the same `loc`), and
the disc's **axial** coordinates were never scaled while its radii were. The peak
interference is **47.71 mm at r = 0.1370** (the cap's outer lip). So the fix is a
**relative axial offset between the two revolves** — move the disc face inboard, or
seat the cap outboard, by ≥47.7 mm at the lip. Note that scaling the disc's `y` by
`S` as well would make it **worse** (0.0482 → 0.0556 at the crossover): the missing
`S` is not the fix, it is only the symptom's origin.

*Ceiling:* the m=5 harmonic figures (render 0.050–0.056 vs photo 0.012–0.022) are
render measurements I could not repeat.

---

### A3 — the clone class, and the one half of it that is not true

**The geometry half: HOLDS.** `build.py:346-360`:

```
for (x, tr) in ((T.X_AXLE_F, T.TRACK_F), (T.X_AXLE_R, T.TRACK_R)):
    for s in (1, -1):
        …
            D.place(o, loc=(x, s * tr / 2, T.TIRE_R))
```

No `rot=`. All four hubcaps, all four sets of five vent holes and all four VW
glyphs are at the identical clock angle. `build.py:869-873` explicitly exempts the
wheels from the step-8b shear so this is the final pose.

**The materials half: FALSE AS STATED, and this matters for the fix.**
The critic's stated mechanism is "`WEATHER`, `MOTTLE` and the dust noises are all
fed **Object** coordinates … so every duplicate carries a bit-identical wear field."
Three source facts kill it:

1. `place()` (`t1_detail.py:31-39`) **bakes** the transform into `v.co`. It does not
   set an object transform.
2. `build.py:858-859` states it and `build.py:862-868` **asserts** it:
   > *"verified that all 147 meshes carry an identity transform at this point
   > (`D.place()` bakes into mesh data), so local == world … it is asserted rather
   > than assumed"*
   with `assert not _bad, "step 8b shears on v.co.x, which is only world x while
   every mesh has an identity transform."`
3. Therefore **Object texture coordinates == world coordinates** for every mesh in
   the scene. The front wheel sits at x = +1.300 and the rear at x = −1.100 — 2.400 m
   apart in a field whose largest feature is `W_CLUST_SCALE = 7.0` (143 mm). They
   sample **different** noise. The same holds for the ±y pair, which is additionally
   mirrored in y before placement (`build.py:355-357`).

And `MOTTLE` is not even in play: `MOTTLE_OFS`'s only consumer is inside
**`body_paint()`** (`t1_mats.py:1424-1432`, function begins at `:1349`), i.e. the
`T1_paint` material. The wheels carry `tyre` / `wheelcream` / `capred` / `capwhite`
(`build.py:348-351`). `MOTTLE_OFS` cannot be "the second line of the fix" for the
wheels — it never reaches them.

**`MOTTLE_OFS` itself: PARTIAL.** It exists, `t1_mats.py:662-663`:
```
MOTTLE_OFS    = tuple(float(v) for v in
                      os.environ.get("T1_MOT_OFS", "0,0,0").split(","))
```
It is a **module-level** constant baked once into one shared node tree, so it is a
global field shift, not a per-instance seed. Turning it into one requires a material
copy per instance.

**So what is the observed 0.90 correlation?** Almost certainly the geometry: the
critic's own caption names "the five vent notches, the VW glyph, the dome's specular
streak" — all identical geometry under identical lighting. I cannot separate the
geometric and material contributions without rendering (see §5).

**THE FULL CLASS — every place two or more instances of one builder differ only by
a sign or a translation.** All confirmed by reading each site:

| parts | site | rotation varies? |
|---|---|---|
| 4 × tyre, rim_barrel, rim_disc, hubcap, cap_emblem | `build.py:346-360` | **no** |
| 2 × headlamp ring / lens / bowl | `build.py:466`, `:506` | **no** |
| 2 × bullet indicator base + lens | `build.py:520-521` | **no** |
| 2 × tail lamp | `build.py:564` | **no** |
| 2 × headlamp recess bore | `t1_shell.py:463-473` | **no** (axis `(-1,0,0)` both) |
| 4 × cab door hinge (barrel + leaf) | `t1_detail.py:1576-1588` | mirror only |
| 2 × lid prop strut | `t1_shell.py:2203-2219` | same rod, x only |
| 8 × bay/door seal ring | `t1_shell.py:217-225` | mirror only |
| 2 × windscreen pane, 2 × ws seal | `t1_shell.py:24-30`, `:43` | mirror only |
| 2 × side glass | `t1_shell.py:192` | mirror only |
| 2 × gutter run | `t1_detail.py:1724` | mirror only |
| 2 × wiper (pivot/boss/arm/blade) | `t1_detail.py:1795` | mirror only |
| 2 × cab door handle + lever | `t1_detail.py:1863-1876` | mirror only |
| 2 × bumper iron | `t1_detail.py:466` | mirror only |
| 2 × over-rider post | `t1_detail.py:837` | mirror only |
| 2 × 13 louvre blades + cutters + backing | `t1_detail.py:2241`, `:2274`, `:2295` | mirror only |
| 4 × wheel-house liner | `t1_detail.py:1277-1289` | mirror only |
| 2 × door card + door back | `t1_detail.py:1699-1707` | mirror only |
| bulb-string repeats | `t1_detail.py:2443` | pitch only |
| tail-board bulb repeats | `t1_shell.py:1864-1890` | pitch only |
| 2 × mirror arm + head | `t1_detail.py:1743-1750` | **has `rot=(0,0,s*-0.13)`** — the only one that rotates |
| 6 × S-hook, 2 × caddy | `t1_detail.py:3159-3161`, `:3322` | translation only |

---

### A8 / A10 — tail hardware

**(a) The handle.** `t1_shell.py:856-857`:
```
ENGLID_GAP = [(u, v + 0.8700)
              for (u, v) in T.rrect(0.9400, 0.5000, 0.055, seg=6)]
```
so the shut-line outline runs z **0.6200 … 1.1200** (`0.8700 ∓ 0.5000/2`), and with
`GAPW = 0.0055` (`t1_shell.py:491`) the lid's own lower cut edge is at
**0.617250**.

`t1_detail.py:2714`: `ENGLID_HANDLE_DROP = 1.274 * PLATE_OUTER_H`;
`t1_detail.py:2729`: `z = PLATE_OUTER_CZ - ENGLID_HANDLE_DROP`.

Recomputed from `PLATE_Z = 0.7800`, `PLATE_W = 0.3300`, `PLATE_ASPECT = 1.9616`
(`t1_detail.py:2515-2531`):

```
PLATE_OUTER_H  = 0.168230
PLATE_OUTER_CZ = 0.787544
DROP           = 0.214325
handle z       = 0.573219
```

**Handle sits 46.78 mm BELOW the lower shut line** (49.5 mm below the lid panel's own
lower edge at 0.617250). Sign: **negative — outside the lid, on the fixed body.**
Premise holds to 0.02 mm of the survey's 46.8 mm.

Note the already-right list says the handle's placement *relative to the plate* is
correct and must not be touched — so this is an argument about `ENGLID_GAP`'s
`+0.8700`, not about `ENGLID_HANDLE_DROP`.

**(b) The lamp bore.** `t1_detail.py:920-926`:
```
def small_lamp(r=0.032, depth=0.026, name="lamp"):
    prof = [
        (0.000, 0.0000), (depth * 0.45, r * 0.55), (depth * 0.82, r * 0.88),
        (depth, r), (depth - 0.004, r + 0.004), (0.000, r + 0.006),
    ]
```
It starts **on the axis**. `build.py:546` calls it with `r = TAIL_LAMP_OD/2 - 0.006 =
0.091801`, `depth = 0.0270`. `build.py:564`:
`D.place(tl, loc=(T.X_TAIL + 0.0040, s * 0.6200, 0.8250))` — the base plane is
**4.0 mm inboard** of the tail skin at `X_TAIL`.

Buried fraction of radius on that profile's first segment:
`0.55 · (0.0040 / (0.45·0.0270)) = **0.18107**` → a **16.62 mm radius / Ø33.2 mm**
disc of body red at the exact lens centre, **3.3 % of the lens area**. Premise holds
(the survey's 0.181 reproduced exactly).

**(c) Lamp z.** `build.py:564` z = **0.8250** (bare literal) against
`PLATE_OUTER_CZ = 0.787544` → **+37.46 mm ABOVE**, i.e. **+0.2226 plate heights**.
Premise holds; the sign is the one the finding claims.

---

### A9 — the galley's aft offset, and the two things that must not be double-counted

`t1_shell.py:151-153`: `BAY_W = 0.5155`, `BAY_CX = (0.6720, 0.0470, -0.5980)` →
`BAYS = [(0.4143,0.9298), (-0.2107,0.3047), (-0.8558,-0.3402)]`.

The six bay-3 S-hooks at `t1_detail.py:3159`:
`-0.5030, -0.5720, -0.6770, -0.7500, -0.8290, -0.9070`.

| u | built X | corrected `BAYS[2]` | Δ | retired REF map `(495.8−u)/211.5` | Δ |
|---|---|---|---|---|---|
| 0.13 | −0.5030 | −0.4073 | **−0.0957** | −0.5042 | +0.0012 |
| 0.26 | −0.5720 | −0.4743 | **−0.0977** | −0.5724 | +0.0004 |
| 0.46 | −0.6770 | −0.5774 | **−0.0996** | −0.6774 | +0.0004 |
| 0.60 | −0.7500 | −0.6496 | **−0.1004** | −0.7508 | +0.0008 |
| 0.75 | −0.8290 | −0.7269 | **−0.1021** | −0.8296 | +0.0006 |
| 0.90 | −0.9070 | −0.8042 | **−0.1028** | −0.9083 | +0.0013 |

Two more, from the same source lines:

* `gal_appliance` (`t1_detail.py:3208`) built **−0.0320 … −0.2180**; corrected
  (u 0.44–0.80 of `BAYS[1]`) **+0.0779 … −0.1077** → **Δ −0.1099 / −0.1103**.
* `gal_warmer` (`t1_detail.py:3311`) built **−0.6860 … −0.9550**; the retired map
  puts image x 641/698 at **−0.68653 / −0.95604** — a **0.5 / 0.4 mm** match.
  Corrected: **−0.5863 / −0.8511** → **Δ −0.0997 / −0.1039**.
* `GAL_SEAM_X = -0.6140` (`t1_detail.py:2880`) — sits on the retired map at
  u = 625.66 px.

**So: the premise holds, but the offset is NOT rigid.** It runs **−0.0957 to
−0.1103 m** across the sample, for two reasons the source itself states at
`t1_shell.py:126-140`: (1) rev 13's translation was per-bay, not global — the old
centres were `+0.5665 / −0.0630 / −0.6975` and the new are `+0.6720 / +0.0470 /
−0.5980`, i.e. **+0.1055 / +0.1100 / +0.0995**; (2) the retired map's implied bay
width is **0.5248 m** against `BAY_W = 0.5155` (**+1.8 %**), which spreads the offset
by ~7 mm inside each bay. **A single additive constant will leave ±8 mm on the
table**; re-deriving each X from `BAYS[i]` (which is what the header at
`t1_detail.py:2757-2764` already claims is being done) will not.

**Finding 28, `gal_rail` — SEPARATE, and its headline mis-signs the length.**
`t1_detail.py:3157`: `_gcyl("gal_rail", (-0.3800, rail_y, rail_z), (1,0,0), 0.0075,
0.660)`. `t1_core._frame` (`:595`) extrudes `±depth/2` about the origin, so the rail
spans **−0.050 … −0.710**. Against the measured rail (u 0.02–0.98 of `BAYS[2]`):
centre **−0.598**, length **0.495**.

* centre off by **+0.218 m forward** — that is **twice** the 106 mm, so it is not the
  same defect and must not be corrected twice;
* length **0.660 vs 0.495 = 165 mm too LONG.** The survey's headline says "165 mm too
  short"; the magnitude is right, the **direction is inverted**. The survey's own body
  text states the two numbers correctly. **Do not shorten by 165 mm from the wrong
  end.**
* the three aft hooks at −0.750 / −0.829 / −0.907 hang **40 / 119 / 197 mm** beyond
  the rail's aft end at −0.710. Confirmed.
* the forward end at −0.050 is inside `BAYS[1] = (−0.2107, 0.3047)` — the rail
  crosses the pillar into bay 2. Confirmed.

**Finding 29, `gal_caddy_fill` — SEPARATE.** `t1_detail.py:3322-3326`:
```
for i, (bx0, bx1) in enumerate(((-1.0420, -1.1550), (-1.1600, -1.2730))):
    A(_gbox(f"gal_caddy{i}",      bx0,         bx1,         cy0+0.010, cy1-0.010, …))
    A(_gbox(f"gal_caddy_fill{i}", bx0 + 0.012, bx1 - 0.012, cy0+0.024, cy1-0.024, …))
```
`bx0 > bx1` (both negative), so `bx0+0.012` moves the **forward** end further forward
and `bx1−0.012` the **aft** end further aft. fill0 spans **−1.0300 … −1.1670**
(137 mm) inside a caddy of **−1.0420 … −1.1550** (113 mm) — **12 mm proud at both
ends**. fill1 spans **−1.1480 … −1.2850**, and its forward face at −1.1480 is
**7.0 mm inside caddy0's solid** (caddy0 ends at −1.1550). The `cy` pair on the same
call insets correctly (`cy0 < cy1`). Confirmed exactly. This is a sign error at one
station and is orthogonal to the 106 mm.

---

### A11 — the cab door handle

`t1_detail.py:1859-1878`, verbatim:
```
def handles():
    for s in (1, -1):
        y = T.WX(1.100) * T.G(1.330)
        base = T.solid_prism((1.075, s * (y + 0.006), 1.330), …
        lever = T.solid_prism((1.060, s * (y + 0.018), 1.330), …
```
`1.330` appears at lines **1864, 1865 and 1870** — three occurrences, not two (line
1864 is the flank-half-width lookup at the same z). `grep -rn "1\.330\b" --include=*.py .`
returns **only those three lines in the whole repository.** No citation anywhere.

`t1_mats.py:144`: `Z_BELT_AUTH = 1.2720   # un-dropped, geometry frame`.

Both are un-dropped geometry-frame z, and both carry the same `rake_drop(x)`, so the
offset is **exactly +58.0 mm** and is station-independent (checked at x = 1.060,
1.075, 1.088 — 58.0 mm at all three). The handle is above the belt; both reference
vehicles carry it below. Premise holds.

---

### A14 — three dead things

**Zero-area rails.** `t1_shell.py:2122-2124`:
```
for (xa, xb) in ((LID_X0, LID_X0), (LID_X1, LID_X1)):
    r = _rag_grid(RAG_HW, xa, xb, RAIL_PROUD, bows=False, nx=1, ny=18,
                  name="lid_rail")
```
`_rag_grid` begins at `t1_shell.py:1011`; its x is `t1_shell.py:1016`:
`x = x0 + (x1 - x0) * ix / nx`. With `x0 == x1` this is `x0` for **both** `ix = 0`
and `ix = 1`, so columns 0 and 1 are coincident and **all 18 quads per rail have zero
area**. `me.validate()` (`:1030`) strips faces with repeated *indices*, not repeated
*positions*, so the objects survive and are assigned "paint". `grep -n _rag_grid
t1_shell.py` returns exactly two lines — the def and this one call. Premise holds.
`grep -n "zero.area\|degenerate\|calc_area" verify.py verify_clone.sh` returns
**nothing**, so neither verifier can see it.

**Double `gutter()`.** `grep -n '^def gutter' t1_detail.py` → **944** and **1717**.
`build.py:403` `A(D.gutter(), "paint")` binds the **later** one (Python keeps the
last definition). Premise holds.

**Dead `moulding()`.** `grep -rn "moulding" --include=*.py .` returns **exactly one
line**: `t1_detail.py:962:def moulding(z=1.372):`. It is called by nothing, and by
nothing in `verify.py` or `verify_clone.sh` either. Premise holds.

---

### A19 — zero rotation on the front lighting

`build.py:506`:
```
for o, k in ((ring, _BEZEL), (lens, "lens"), (bowl, "reflector")):
    D.place(o, loc=(HL_X, s * HL_Y, HL_Z)); A(o, k)
```
`build.py:520-521`:
```
D.place(ibase, loc=(2.0960, s * IND_Y, IND_Z)); A(ibase, "chrome")
D.place(ilens, loc=(2.0960, s * IND_Y, IND_Z)); A(ilens, "amber")
```
No `rot=` on any of the five parts. `2.0960` is a **bare literal typed twice**; there
is no `IND_X` symbol anywhere in the repository. Premise holds.

`headlamp_recess_cutters`, `t1_shell.py:463-473`:
```
for s in (1, -1):
    …
    mouth = T.solid_prism((hl_x + 0.010, s * hl_y, hl_z),
                          (0, s, 0), (0, 0, 1), (-1, 0, 0),
                          prof, 0.052, name=f"cut_hlbowl{s}")
```
The extrusion direction is `(-1, 0, 0)` for **both** signs — the bore axis is the
vehicle X axis on both sides. Premise holds. (The docstring at `:435-436` also states
plainly "THIS IS A STRAIGHT-SIDED BORE, 52 mm deep, **at the lens radius**", which
independently confirms A19's third clause.)

---

### A18 — contact shadow, vignette, grain

Four source checks, all confirmed:

* `hero.py:112` — `"T1_SUB": a.sub, "T1_PREVIEW": a.view, "T1_FX": "0",`
* `studio.py:762` — `on = optics and _envi("T1_FX", 1)`
* `studio.py:823` — `if on and _sh > 1.0:` (the survey cites 825; the whole
  floor/power/SetAlpha subgraph is inside this block)
* `post.py` — `grep -n shadow post.py` returns **nothing**. `main()` (`post.py:441-465`)
  runs `backdrop_headroom → bloom → chromatic → vignette → grain`. No shadow stage.

`bg_white_level` (`studio.py:702-723`):
```
    if vt == 'AgX' and 'Punchy' in look:
        lvl = 24.87
    return float(os.environ.get("T1_BGW", lvl))
```
returns **24.87**, exactly as claimed. Its own comment at `:713-715` records that
linear 21.0 maps to display **253** under this look, so 24.87 was chosen to reach 255
— which is the definition of sitting at or past the clip. `studio.py:941` sets the
vignette at `amt = T1_VIG · 0.055` and `:964` the grain at `amt = T1_GRAIN · 0.016`,
both applied where paper white is 24.87 linear — the grain is **0.13 % of white**.
I cannot confirm the *delivered* 0.000 / 0.0000 without rendering (§5).

**THE DIRECT PATH DOES CARRY THE SHADOW.** `grep -rn T1_FX *.py` shows `build.py`
never sets it; `_envi("T1_FX", 1)` defaults to **1**. Only `hero.py`, `flank_compare.py`
and two probes force it to 0. Everything in `out/` comes off `build.py`'s direct
path, so it carries the whole optics chain — and the already-right list measured it
there at **0.8866** against SPEC 10.116.5's declared 0.8729. **The A18 defect is
latent, on the `hero.py` strip path only.** That is exactly what the brief says, and
it means A18's headline ("the delivered frames have NO contact shadow") is true of
the *stitched* deliverable and **false of every frame currently in `out/`**.

---

### A5 / A6 — materials

**(a)** `t1_mats.py:1694-1702`, verbatim:
```
bsdf.inputs["Roughness"].default_value = 0.420
bsdf.inputs["Metallic"].default_value = 0.0
bsdf.inputs["Specular IOR Level"].default_value = float(
    os.environ.get("T1_SPEC", 0.50))
bsdf.inputs["Coat Weight"].default_value = 0.02
bsdf.inputs["Coat Roughness"].default_value = 0.300
```
`simple()`'s coat branch, `t1_mats.py:712-714`:
```
if coat:
    b.inputs["Coat Weight"].default_value = coat
    b.inputs["Coat Roughness"].default_value = 0.030
```
**Nine** materials go through it with `coat > 0` (`t1_mats.py:1790, 1792, 1794, 1796,
1800, 1808, 1816, 1825, 1827`): `cream`, `wheelcream`, `bumpercream`, `roundelred`,
`countercream`, `countertan`, `glass`, `capred`, `capwhite`. Every one gets **0.030**;
`T1_paint` gets **0.300** — **10×**. The same three literals are repeated verbatim for
`calidad` at `t1_mats.py:1778-1783`. `grep` finds no `T1_ROUGH` / `T1_COAT` /
`T1_COATRG` anywhere. Premise holds.

**(b)** `t1_mats.py:962` — `pw = _mr(nt, PT, W_PT_LO, W_PT_HI, 0.0, 1.0, …, smooth=True)`
with `W_PT_LO, W_PT_HI = 0.520, 0.600` (`t1_mats.py:243`). At `Pointiness = 1.0`,
`pw = 1.0`. `t1_mats.py:974` — `deep = _mr(nt, pw, W_STEEL_LO, W_STEEL_HI, 0.0, 1.0,
…, smooth=True)` with `0.80, 1.00` (`t1_mats.py:260`). At `pw = 1.0`, `deep = 1.0`.
**Both gates saturate**, exactly as claimed; the chip mask collapses to
`cm·clm > W_CHIP_CUT = 0.35` (`t1_mats.py:246`, `:972`) — object-space noise with no
edge selectivity. Premise holds.

`apply_weather`, `t1_mats.py:1143-1144`:
```
    if wear > 0.0:
        nt.links.new(g.outputs[3], b.inputs["Metallic"])
```
Confirmed, at the exact lines cited.

**(c)** `t1_mats.py:1979-1982`:
```
    _CTAN_WEAR = float(os.environ.get("T1_CTAN_WEAR",
                                      WEAR[M["countertan"].name]))
    apply_weather(M["countertan"], dust=_CTAN_DUST, wear=_CTAN_WEAR, …)
```
and `t1_mats.py:681`: `WEAR = dict(bumpercream=1.0, wheelcream=0.8,
countercream=0.7, countertan=0.7, …)`. Both confirmed.

---

### A7 — the rear serving aperture

`t1_detail.py:3089`: `X0, X1 = -1.3000, 1.0400          # galley box, fore-aft`
`t1_detail.py:3101-3102`:
```
A(_gbox("gal_end_a", X0 - 0.030, X0, -0.5000, 0.4000, 1.2000, 1.8600),
  m_white)
```
`X_TAIL = T._aft(-2.108) = -1.100 - 0.773 = **-1.873000**` (`t1_core.py:60-70`).
Gap = **573.0 mm**. Premise holds.

**Nothing dresses or lights it.** Verified by reading, not grepping:
* `gal_ceiling` is deleted and nothing replaces it — `t1_detail.py:3103-3127`,
  ending `del _ceil`. The stated light source is *daylight through the roof opening*.
* The roof opening runs `LID_X0…LID_X1 = 0.9640…-1.0700` (`t1_shell.py:1075`), so it
  **stops 803 mm forward of the tail** — no daylight reaches x < −1.070 at all.
* `trunk_bay` (`t1_shell.py:1439-1500`) does line x −1.873…−1.453 — but at
  **z 0.6025…1.1025**, i.e. the *engine* bay, well below the rear aperture at
  `REAR_Z = 1.4500 ± 0.1700` (`t1_shell.py:230`), and it is behind a lid the owner
  ruled **shut**.
* `interior_fill()` (`t1_detail.py:1669-1713`) builds only door cards and door backs;
  the galley backdrop moved out of it and ends at `X0 = -1.3000`.

**AND A SECOND HOLE THE SURVEY DID NOT NAME.** `gal_end_a` spans y **−0.5000 …
+0.4000**, while the rear aperture is `REAR_W = 1.0400` wide, i.e. **±0.5200**. So
**120 mm of the aperture's show-side width and 20 mm of its off-side width look
straight past the end wall** into unlit body cavity, regardless of how the 573 mm is
dressed. Any fix that only extends `gal_end_a` aft will leave those two strips black.

---

## 3. ITEMS ALREADY FIXED — DO NOT RE-FIX

**Only one item on the A-list / cross-check list is already fixed, and it is the one
the record contradicts itself about.**

1. **Survey finding 6 — the tail board's buried foot and the tautological guard.
   FIXED at rev 49d (`39f3301`).** The finding's two quoted lines no longer exist:
   `grep -c "_crown = T.ZT_ALL" t1_shell.py` returns **1** at `d8275da`, `05a31b9`,
   `5adf8e7`, `ae526d7` and **0** at `39f3301` and every commit after. The roof-lids
   agent read a tree at or before `ae526d7`. **The synthesis's A23 "resolve the
   contradiction BEFORE touching it" is discharged by this report: there is no
   contradiction left, only a stale finding.** Full adjudication in §4.

2. Two the brief already flags: finding 15 (rev-50 plan is an empty placeholder /
   survey untracked) and finding 42 (STATE.md last written at rev 45). Both false.

3. **Not fixed, but not a defect either — A18's headline.** "The delivered frames
   have NO contact shadow at all" is **true of the `hero.py` stitched strip path and
   false of everything in `out/`**, because `build.py` never sets `T1_FX` and
   `_envi("T1_FX", 1)` defaults to 1. Anyone who "fixes" this by re-tuning
   `T1_SHADOW` will be tuning a gain that already delivers 0.8866 against a declared
   0.8729. The fix is one line in `hero.py`, not in `studio.py`.

4. **Not fixed, but the stated mechanism is wrong — A3's material half.** See §2.
   The wear field does **not** clone. Implementing "a per-instance `MOTTLE_OFS`" would
   be work against a non-defect, and `MOTTLE_OFS` does not reach the wheel materials
   at all.

5. **Not fixed, but mis-signed — finding 28's `gal_rail` length.** The rail is
   **165 mm too LONG**, not short.

I found **no other** A-item that has already been fixed. Every other premise I was
asked to test reads in HEAD exactly as the survey describes it.

---

## 4. THE TAIL BOARD FOOT — ADJUDICATION

**The question:** is the current guard still a tautology, and is the station solved
or typed?

**THE STATION IS SOLVED FROM `T1_body`'s OWN VERTICES AT RUN TIME.**
`t1_shell.py:1649-1667`, verbatim:

```python
    _bx, _bs, _bd = None, None, 1e9
    _b0 = bpy.data.objects.get("T1_body")
    if _b0 is not None:
        _m0 = _b0.matrix_world
        _wv = [_m0 @ vv.co for vv in _b0.data.vertices]
        _n = 0
        for _i in range(61):
            _xc = T.X_TAIL + 0.300 * _i / 60.0
            _sel = [w.z for w in _wv if abs(w.x - _xc) < 0.030
                    and abs(w.y - TB_Y_CENTRE) <= TB_WIDTH * 0.5]
            if not _sel:
                _n += 1
                continue
            _sz = max(_sel)
            if abs(_sz - TB_BASE_Z_NEAREDGE) < _bd:
                _bd, _bx, _bs = abs(_sz - TB_BASE_Z_NEAREDGE), _xc, _sz
```

It sweeps 61 stations over `X_TAIL … X_TAIL+0.300` at 5 mm spacing, takes the **max z
of the body mesh's world-space vertices over the board's own footprint** at each, and
picks the station whose skin height is nearest the photographed base
`TB_BASE_Z_NEAREDGE = 1.7470`. It logs the residual (`"station SOLVED from the skin:
… %.1f mm"`) and it has an explicit no-body fallback that **says so** rather than
guessing (`t1_shell.py:1670-1673`). **Nothing is typed.** Brief §3 is correct on this point.

I reproduced the downstream chain by hand and it lands where the brief says:
`_hang = TB_T·0.5·cos(38°) = 0.0086681`; `z0 = _seat + _hang + 0.0040`; with
`_seat ≈ 1.7497` → `z0 ≈ 1.76237`; tip z `= z0 + sin(38°)·0.7110 = **2.20010**`
against a measured 2.184 ± 0.030. Both closures reproduce.

**THE GUARD.** `t1_shell.py:1730-1738`:

```python
    _lo = min((board.matrix_world @ vv.co).z for vv in board.data.vertices)
    if _lo < _seat - 1e-6:
        raise AssertionError(
            "tail board foot is BURIED: its lowest vertex is at z %.4f against a "
            "measured roof skin at z %.4f over its own footprint -- %.1f mm inside "
            "the body. …")
```

**Verdict: it is NOT the old tautology, and it is not a free-running clearance
measurement either. Both halves need saying.**

*Why it is not the old tautology.* The old form was
`z0 = ZT_ALL(x0) − rake_drop(x0) + 0.005` guarded by `z0 < ZT_ALL(x0) − rake_drop(x0)`
— two evaluations of **one expression**, and that expression named the **wrong
surface** (`ZT_ALL` is the roll start, not the crown). The new form reads **two
different meshes**: `_seat` from `T1_body`'s vertices, `_lo` from `tail_board`'s
vertices, both through `matrix_world`. It **has** fired on a real defect: the source
records at `t1_shell.py:1707-1712` that a typed 5 mm standoff left the foot 3.7 mm
inside the skin and *"caught by the new guard below on its first run"*. The old form
could not have caught that at any tolerance.

*Why it is still not independent.* Trace the arithmetic. `z0` is **derived from
`_seat`**. The board is `T.rrect(TB_CHORD, TB_WIDTH, 0.012, seg=4)` shifted by
`+TB_CHORD·0.5` (`t1_shell.py:1722-1723` (HEAD)) so its outline's minimum `u` is **exactly
0** (`rrect`'s corner arc at `t = π` returns `−a − r = −w/2`), and `T._frame`
(`t1_core.py:592-596`) extrudes `±depth/2` about the origin along
`w = (−sin a, 0, −cos a)`. So

    min z  =  z0 + 0·sin(a) − (TB_T/2)·cos(a)  =  z0 − _hang  =  _seat + 0.00400

**identically**, and `matrix_world` is the identity (no `place()` is called on the
board; `build.py:973` just links it). So in the shipped path the guard's margin is
pinned at **exactly +4.0 mm by construction**, and it can never fire on a change to
the standoff, to the seat, or to the skin.

What it *can* fire on is a mismatch between `_hang`'s model of the board and the
board's actual section: a change to `TB_T`, to the tilt, to the `+TB_CHORD·0.5`
shift, to `solid_prism`'s extrusion convention, or the appearance of any object-level
transform. That is a real and useful class — it is the class that was caught — but it
is a **construction-consistency** check, not a clearance measurement.

**So, adjudicating the three documents:**

| document | claim | verdict |
|---|---|---|
| survey finding 6 | foot buried 63–75 mm; guard is a tautology | **STALE.** Both lines it quotes were deleted at `39f3301` |
| already-right list | height chain closes at 2.7 mm; station derived at run time; do not re-open | **CORRECT.** Reproduced by hand |
| synthesis A23 | resolve the contradiction before touching it | **DISCHARGED.** There is no live contradiction |
| brief §3 | rev 49d re-solved the station and rewrote the guard to compare built board against built skin | **CORRECT in every particular**, though "compares two independently obtained quantities" understates the residual: it compares two mesh reads whose difference is fixed at +4.0 mm by the construction of `z0` |

**Do not re-open the tail board's foot.** The one thing left is housekeeping the
already-right list already named: the stale sentence at **`t1_shell.py:1827-1829`**,
inside `tail_board_stay`'s comment — *"that reading belongs to a base at the near-edge
height, and this board stands **80 mm** clear on the roof (see `tail_board()`)"* —
still cites the withdrawn 80 mm as live justification. (The four other "80 mm"
mentions in `t1_shell.py` at 1602, 1603, 1610 and 1620 are inside the deliberately
kept historical block that ends with "*rev 49c — THE 80 mm FOOT INCONSISTENCY
DISSOLVES*", so they read as record, not as claim. Line 1828 does not.)

---

## 5. `verify_clone.sh` — THE ROW COUNT

**I ran it.** Output, verbatim:

```
  ALL 122 PASS.  Content matches the rev-42 measured baseline,
  which is still current at rev 44.
```
exit 0.

**Where 113 came from, and why it is stale rather than wrong.** The history:

| commit | rev | executed rows | what changed |
|---|---|---|---|
| `40dd87e` | 48 | **110** | — |
| `5adf8e7` | 49c | **113** | +3 new rows, 1 window widened, 1 relabelled |
| `e19b46f` | 49e | **122** | +9 tail-board rows, all additive |
| `7b12ca8` | 49e | **122** | 1 baseline re-based (`mesh objects 221 → 231`) |

(`grep -c "ck "` gives 113 / 116 / 125 / 125; three of those occurrences are the two
branches of an if/else pair plus the `ck ()` definition and its usage comment, so the
executed count is three lower at every commit.)

`5adf8e7`'s own commit message ends *"verify_clone.sh ALL 113 PASS."* — **so the
brief's §1 was written at rev 49c and never updated when 49e added nine more rows.**
The brief's §12 says 122. **§12 is right, §1 is stale.**

**Was anything relaxed?** Three modified rows, from `git diff 40dd87e HEAD -- verify_clone.sh`:

1. `"build.py opens the trunk lid"` → `"build.py separates the trunk lid"` — the test
   is byte-identical (`grep -q 'split_trunk_lid' build.py`). **Pure relabel.**
2. `"TRUNK_OPEN_DEG declares itself NOT MEASURED"` — window widened from
   `grep -A 3 '^TRUNK_OPEN_DEG'` to `grep -A 30`. **This is a widening**, and the
   commit that made it says so in its own words: *"WIDENING THE WINDOW ALONE WOULD BE
   A RELAXATION, SO IT DOES NOT HAPPEN ALONE"*, and adds three rows in the same edit
   (`TRUNK_OPEN_DEG=0 cites the SHUT ruling`, `a SHUT trunk lid skips the swing`,
   `the trunk bay lining is guarded INBOARD of the skin`). The row had gone red
   *because the source improved* — the owner's ruling was cited between the constant
   and its declaration.
3. `"mesh objects 221"` → `"mesh objects 231"` — a **documented re-base** of a
   baseline count, `7b12ca8` (*"re-base mesh objects 221 → 231, every one
   accounted"*).

The other **twelve** rows are net-new and every one is a real content test (they
grep for a symbol, a declaration string, or a count). **`ck "the foot guard is NOT
self-referential" 0 "$(grep -c '_crown = T.ZT_ALL' t1_shell.py)"` is the strongest of
them: a row that refuses the return of the tautology.**

**Verdict: "ALL 113 PASS" is FALSE (it is 122). "NONE were relaxed" is
SUBSTANTIVELY TRUE — the net is strictly stronger — but LITERALLY one row's grep
window was widened, and the record is honest about it.** No threshold on any numeric
row was widened; no row was deleted.

---

## 6. WHAT I COULD NOT CHECK, AND WHY

Every ceiling below is a hard boundary of this pass, not a hedge.

1. **Every image measurement in the survey.** I did not open a single reference
   photograph or render. So the following remain on the survey's authority alone,
   not mine: A1's −5.3 % taper and α = 61–78°; A1b's `W·sinα ≥ 1.187 m`; A2's m=5
   harmonic (render 0.050–0.056 vs photo 0.012–0.022); A3's HF correlation 0.675–0.9;
   A8's pixel chain (seam y 962.5, handle y 984); A10's lens-centre-below-plate
   reading; A11's render/photograph handle rows; A13/A16's texture measurements;
   A18's "57 % bit-exact white" and the vignette/grain deliveries of 0.000/0.0000.
2. **Nothing was rendered.** The brief forbids it and a render queue holds all four
   cores. So I could not (a) confirm that `bg_white_level`'s 24.87 clips to 255 in
   the delivered frame, (b) separate the geometric from the material contribution to
   the wheel-vs-wheel correlation, which is the crux of A3, or (c) watch any guard
   fail. My A1 guard table is an arithmetic simulation of the guard expressions, not
   an observed abort.
3. **Blender was not run, so I could not confirm two mesh-level facts:** that Cycles
   drops the zero-area `lid_rail` faces rather than rendering them as something, and
   that `me.validate()` really leaves them in place (I verified only that it strips
   duplicate *indices*, which is Blender's documented behaviour, not that it does so
   here).
4. **`prof.py` is a re-typing of `t1_core`'s LUTs**, not an import (importing
   `t1_core` needs `bpy`). I transcribed `G`, `ZT_ALL`, `RT_ALL`, `CR_ALL`, `WX`,
   `_aft`, `rake_drop` and `roof_z` by hand. A transcription error would move `Yt`
   and the `_roof_edge_y` walk. As a check, my `Yt(-0.053) = 0.727261` reproduces
   `t1_core.py:449`'s own published `Yt = 0.7273`, and my `X_TAIL = −1.873000`
   reproduces `t1_core.py:71`'s comment exactly.
5. **A9's corrected stations use the survey's own `u` fractions** (0.13/0.26/0.46/
   0.60/0.75/0.90 for the hooks, 0.44–0.80 for `gal_appliance`, image x 641–698 for
   `gal_warmer`). Those fractions are the survey's readings off `ref_side.jpg`, not
   mine. What I verified independently is that (a) every built X reproduces the
   retired `(495.8−u)/211.5` map to 0.4–1.3 mm, and (b) the per-bay centre shifts at
   `t1_shell.py:121-136` are +0.1055 / +0.1100 / +0.0995 — and those two facts alone
   establish the finding without needing the `u` values.
6. **I did not audit the survey's remaining findings** — only the bodies of 3, 4, 5,
   6, 7, 8, 10, 11, 12, 13, 19, 22, 28, 29, 30, 35, 37, 38, 47, 48, 49, 58, 60, 72,
   the completeness critic's §1.2, and the ALREADY RIGHT section in full. Findings
   I did not read could carry their own staleness.
7. **A18's `bg_white_level` clip.** The constant is confirmed; the *consequence* is
   an AgX-Punchy transfer-curve question I cannot answer without either the OCIO
   config or a render.
