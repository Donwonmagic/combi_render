# HANDOFF rev 16 — THE LOFT

**Scheduled last across four revisions so nothing after it could invalidate what
came before. Done in one rebuild. Guards re-run at both subdivision levels.**

Verify by CONTENT, never by hash or commit count.

---

## 0. Guards, and the figures I watched print

| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 1 warn** | **0 fail, 1 warn** |
| warn | roof crown @ rear axle (dome-corrected) **1.983** vs spec 1.960 (**+23 mm**) | **1.983** (**+23 mm**) |
| `DOME_DEFICIT` | **0** (was +98 mm) | **0** |
| rear overhang | **0.7730 m** = 0.3221 of the wheelbase (measured 0.773 ± 0.022) | **0.7730** |
| dims | L=4.065 W=1.750 | L=4.065 W=1.750 |
| cut roof hole | **68088v** | **252335v** |
| body faces | 60461 quad / 465 tri / 3107 ngon | 240338 / 1108 / 4434 |
| non-manifold edges | **0** | **0** |

Also unchanged and printed every run: `roof aperture: open, and solid fore / aft
/ both sides`; `TYRE_D=0.6650`; 3 open apertures on +Y; **four shut lines
100 % open**; band `1.372–1.775`; **bay widths `0.516 0.515 0.516`**; **181
meshes**; **5 materials constant-rough**; **42 distinct materials**;
`cutters rolled back | none` (a STATE.md row, not a console print).

**The warn changed meaning.** It is no longer "the dome is unmodelled". The dome
is modelled; the crown now lands 23 mm ABOVE `SPEC H_ROOF = 1.960` instead of
66 mm below its own gutter. See §1 for why `H_ROOF` was not touched.

---

## 1. Part A — the roof section, and a rejected instruction

`NEXT_CONTEXT_rev16` §6.1 and `LOFT_GROUND` §1.3 both say **drop `ZT_ALL` by
63 mm**. I did not, and this is the one place I departed from the brief.

**It breaks two locks.** The drip rail sits 65–69 mm above the serving-aperture
top (`band …–1.775`, guarded); a 63 mm drop leaves **2 mm** of metal there. And
the windscreen is anchored at absolute `P_TOP = (1.8340, 0, 1.7745)`; dropping
`ZT_ALL` puts the shell's top edge 35–57 mm **below** the screen's own top, so
the cutter opens a notch to the sky.

**Third method, datum-free** — two features at one depth on one flank,
differenced at the same column:

| | measured | built |
|---|---|---|
| drip-rail groove → bay 3 aperture top | 6.16 px / 83 cols / sd 0.19 → **28.3 mm** | 68.6 |
| → bay 2 | 6.05 px / 83 cols / sd 0.19 → **27.4 mm** | 68.6 |
| → bay 1 | 6.13 px / 62 cols / sd 0.21 → **27.5 mm** | 68.6 |
| adopted | **27.7 ± 0.5 mm** | 68.6 → **−41 mm** |

**The aperture band is not the error.** Against the locked belt:
`belt → aperture top = 500.9 mm` measured vs **503.0 built, −2.1 mm**;
`belt → drip rail = 529.7` vs 568.0, **−38.3 mm**.

**The hub route's extra 22 mm is a datum error, not a scale error.** `k_t = 215.5`
is *validated* by belt→aperture agreeing to 0.4 %; the same hub chain puts the
locked belt 29 mm low. Same signature §10.11 bans the ground line for.

**Applied**

```
  RT_ALL (roof)  0.054 -> 0.0949      CR_ALL (roof)  0.032 -> 0.1179
  D = RT + CR          = 0.2128       LOFT_GROUND: 0.2116 +- 0.035
  Yt 0.7273   R = Yt^2/(2 CR) = 2.24 m   (quote R with its Yt or not at all)
  ZT_ALL / RAKE_DZDX / P_TOP  UNTOUCHED       DOME_DEFICIT -> 0
```

Built mesh measures back: drip-rail lip − aperture top = **+27.0 mm**.

**Two `LOFT_GROUND` §1.2 numbers, checked.** Its drip rail **reproduced exactly**
(my fit `v = −0.04409u + 332.301`, n=83, rms **0.067 px**, v = 299.26 at the rear
axle vs their 299.24 ± 0.6). Its roof silhouette **not reproduced**: scanning the
top edge, it is flat at **252.1–253.6 over u[755,815]**, so their "fixed skin
257.2" is 4.7 px low and their "proud strip 253.21" is the roof itself. **Their
coaming/proud-strip reading is withdrawn.** `D` survives regardless.

**`H_ROOF` was NOT changed to clear the warn.** If you re-open it: REF §1 derived
1.960 from `ground = 668.0`, the datum §10.11 bans; the belt-anchored chain here
puts the crown at **1.981**. That is the owner's call, not mine.

---

## 2. Part B — the rear arch

Ogee from `t1_shell._ARCH_PROFILE`, the **assumption-free normalised table**, not
the exponent (window-dependent 3.50–4.28, so 3.9 ± 0.2 is a property of a window
choice). The trace's small left/right difference is kept, not averaged.

```
  ARCH_W_REAR  0.747 -> 0.920 m   (measured 0.92 +- 0.03; width / rim OD 2.158)
  ARCH_R       0.3735  HELD       (lip above hub measures 0.3726 +- 0.0052)
  crown centre rear axle          (confirmed to 0.2 px ~ 1 mm, column-only)
```

**The front arch is left circular.** Never measured — a man stands in front of it
— and widening it brings the lip within 57 mm of the cab-door shut line's bottom
run, the geometry that collapsed the shell for six revisions.

**Carry forward:** the arch's aft foot is now at x = −1.560 and the aft skin at
−1.873, **313 mm apart against 418 before.** `LOFT_GROUND` §3.3 predicted this
gets worse; it is the thing most likely to constrain a future tail change.

---

## 3. Part C — the tail, re-spaced

```
  rear overhang / wheelbase = 0.3412 +- 0.0015   IMAGE      (0.4200 built)
  -> 0.773 +- 0.022 m through the projective map (1.008 built)
  X_TAIL  -2.108 -> -1.873          235 +- 22 mm too long
```

**The map, written out and validated before use.** Rebuilt from `LOFT_GROUND`
§0's own three constraints:

```
  X(u) = 641220.4/(u + 11140) - 55.0322
  X(242.84) = +1.3000   X(749.38) = -1.1000   rho = 1.0445 (measured 1.0445)
  X(922.2)  = -1.8727                          the tail
  X(852)    = -1.5615   vs -1.560 predicted by the measured arch half-width
```

**1.5 mm**, on a feature pair sharing no datum with the tail.

**Applied through `t1_core._aft(x)`**, which carries every aft station and LUT
knot by its own fraction f. `ZB`, `ZT_ALL`, `RT_ALL`, `CR_ALL`, `WX`, `RB_ALL`,
`STATIONS` all go through it, so §3.3's f-table is reproduced **by construction**
rather than re-typed.

**Everything anchored to the old tail skin moved with it** — tail lamps,
`plate_1963`, `englid_handle`, fuel flap, louvres, counter (as a preserved
0.315 m *overhang*), counter brackets, drip-rail sweep, bulb-string aft end,
galley bottles, rear-window cutter and glass, engine-lid gap. Left alone the
lamps became the rear-most objects by 258 mm and **verify row 1 would have kept
passing on a phantom** — the `counter_top` failure shape again.

**`SPEC["L"]` stops being the VW catalogue 4.290.** It is now
`4.290 − (O_OLD − O_NEW)`, an expression so it cannot go stale, and it is
labelled a regression catcher because its forward end `X_NOSE` has never been
measured (lamppost). **A new verify row guards the rear overhang itself** — the
guard strengthened, not widened.

---

## 4. Part D — the poles, §10.30b CLOSED

Coons quad-grid caps whose border IS the boundary loop, so the loop gains no
vertex and the loft's topology is untouched. `a = n//4, b = n//2 − a`.

**The NHALF decision was made on a guard result.** Both arms, both levels:

| arm | SUB=1 | SUB=2 |
|---|---|---|
| NHALF 56, cap 27×28 (asymmetric) | 0 fail | **1 FAIL** — `gap_englid`, "zero-area faces 0 → 2", rolled back |
| **NHALF 57, cap 28×28 (symmetric)** | **0 fail** | **0 fail** |

The engine-lid gap ring is symmetric about y = 0; on an asymmetric cap grid its
two sides land differently and the exact solver returns two slivers. **Moving the
cutter does not fix it** — `T1_ENGLID_DX` 0.120 / 0.158 / 0.200 all give exactly
2 zero-area faces, which is what makes it an outline/grid coincidence rather than
a tangency. Revert with `T1_NHALF57=0` if ever needed.

**Measured, with a negative control in the same frame.** Rear ortho, 1200×800,
32 samples, high-pass σ=8 px, red paint only, 3 px erosion:

| patch | rev 15 | rev 16 |
|---|---|---|
| lower-LEFT corner (335,682,432,764) — the fan | **3.015** | **1.609 (−47 %)** |
| lower-RIGHT corner (784,682,878,764) — **control** | 1.596 | 1.592 (−0.3 %) |

Residual 1.609 is within 1 % of the control. **Do not compare to rev 14's
15.478** — different render, different crop; this is an internally controlled
A/B, not a continuation of that number.

Topology: **max valence 115 → 6**, valence > 4 **53 → 14**, non-manifold **0**.

---

## 5. Two latent bugs this exposed, both fixed

1. **`t1_shell.roof_cutters` passed `zlo` as `T.solid_prism`'s origin**, but
   `solid_prism` extrudes ±depth/2 **about** its origin (`t1_core._frame`). At
   the old `CR_ALL = 0.032` the crown was shallow enough that the half-height
   prism still cleared the roof by 6 mm — it worked by luck for four revisions.
   At 0.1179 it stops 18 mm short and the galley went back to sealed steel.
   Caught by `verify` 11d2.
2. **Every tail-anchored detail was a re-typed constant**, and the tail lamps in
   particular would have kept `verify` row 1 green on a phantom.

---

## 6. What rev 16 did NOT do

- **`SPEC H_ROOF` not changed.** The warn is reported, not tuned away.
- **The front arch not widened.** Unmeasured, and it endangers the shut line.
- **The flat tail-panel HEIGHT not changed.** `LOFT_GROUND` §3.4 bounds it at
  0.36–0.72 m against 1.02 built but would not put a number on it, and the
  counter occludes exactly that band. Needs the head-on rear elevation.
- **No camera change, no hero re-frame**, per the standing order that the camera
  is absolutely last.
- **§6.5's list untouched**: the cream detail map, `COUNTERTAN`'s
  interreflection test, the real matte, the hubcap ring, the tail-lamp material
  slot. All still open exactly as rev 15 left them.

## 7. The photograph search

Owner chose "search and proceed in parallel". A bounded open-web pass found
**nothing at rank 1–4** — no head-on rear or front elevation, and no
transverse-roof silhouette, for either the Playa or the Nolita vehicle. It did
recover ~12 unverified direct image URLs (`/home/claude/search_findings.md` in
the session; not in the repo) and one useful identity corroboration:
trufflepig.com's 2013 Nolita-opening post captions a bus photo *"The bus is in
pretty good shape for travelling over 5500 km to get to NYC"* — textual support
that the Nolita bus is the same physical vehicle relocated from Playa.
Instagram, Facebook, Pinterest, Alamy, Wikimedia and web.archive.org were
**blocked, not absent**. The tool cannot look at images, so the candidate URLs
remain unjudged; a vision-capable pass over that specific list is the logical
next step and is cheap.
