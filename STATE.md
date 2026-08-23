# STATE — machine-written by `audit.py`. Do not hand-edit.

Every number here was measured off the mesh built in the same process that
wrote this file. If this file and any prose in the repo disagree, this file
is right. Regenerate with `T1_SUB=n blender -b --python audit.py`.

## Provenance

| | |
|---|---|
| generated | 2026-08-23 04:22:24 UTC |
| git commit | `5378d78` |
| git subject | rev 57: the top job TAKEN and ceiled with a measured bracket; item B REFUTED -- the gate does not measure the mottle |
| working tree | clean |
| blender | 4.5.3 LTS |
| subdivision | T1_SUB=2 (applied, destructive, before booleans) |
| geometry source | procedural, built this run |

## Guard result

**VERIFY: 0 fail, 0 warn** at T1_SUB=2.

> A pass here is only a pass *at this subdivision level*. The cab-door gap
> booleans passed at SUB=1 and collapsed the shell at SUB=2 for six
> revisions. Run both.

```
length excludes opened lids: 4.311 with them, 4.065 without (what projects: counter, counter_nosing, counter_top, tail_board, tail_board_stay, tb_bulbflex, tb_bulbs, tb_edge_dark, tb_edge_red)
bounds EXCLUDE 9 non-bodywork part(s): counter, counter_nosing, counter_top, tail_board, tail_board_stay, tb_bulbflex, tb_bulbs, tb_edge_dark, tb_edge_red
x range [-2.151, 2.160]   full-Y [-1.064, 1.150]
dims  L=4.065 W=1.750 roof@rear-axle=1.9833 (regression baseline 1.9835, -0.2 mm; dome deficit +0 mm still unmodelled) (bbox top 3.132)
H_ROOF 1.960 is RETIRED as an accuracy target (rev 22, owner's call): its only ground-line-free support was withdrawn by SPEC 10.34. The model reads 1.9833; the real vehicle's absolute roof height is OPEN and UNMEASURED. The +23 mm warn is gone because THE TEST WAS WITHDRAWN, not because the model improved -- the mesh did not move.
rear overhang 0.7730 m = 0.3221 of the wheelbase (measured 0.773 +- 0.022 m)
measured TRACK_F=1.3713  TRACK_R=1.3613  TYRE_D=0.6650
SPEC 10.91 ban-exemption control: 2 exempt names, 4 planted near-misses all still banned
zero-area sweep: 0 of 223 meshes have zero area; 0 exempt (rev 56: lid_rail was the only exemption and it is BUILT now)
lid_rail width = RAIL_PROUD 0.0213 m (owner, rev 56, off ref_workshop.jpg: 'narrow lip, ~as wide as it is tall')
open serving apertures on +Y: 3
roof at tail = 1.988
rake 17.75 mm/m (locked 17.75); drop at x=0 47.9 mm; RIDE_DROP identity holds
rear arch lip above hub 0.3722 m (ARCH_R 0.3735) -> tyre gap 39.7 mm
front arch lip above hub 0.3732 m (ARCH_R 0.3735) -> tyre gap 40.7 mm
roof aperture: open, and solid fore / aft / both sides
shut line door+1: 100 % open
shut line door-1: 100 % open
shut line cargo: 100 % open
shut line englid: 100 % open
shut line x aperture: show flank 0.0 mm (invariant, asserted at import); off flank 804.9 mm over 2 pairs (baseline 804.9, -0.0 mm) -- off flank is graded E, NOT a correctness claim
over-rider assembly (SPEC 10.83 + 10.90 + 10.91): NOT APPLICABLE -- bar AND posts WITHDRAWN BY THE OWNER in rev 37 (SPEC 10.93); the front is a plain cream blade plus its two irons. build.py's calls are COMMENTED, NOT DELETED, and these guards stay armed for the built case. Stated, not silently skipped.
over-rider posts (SPEC 10.91): NOT APPLICABLE -- the posts were built in rev 37 and WITHDRAWN BY THE OWNER in the same revision (10.91.8); build.py's call is commented, not deleted. This guard stays armed for the 2-post case, so re-enabling that one line restores it with no change here. Stated, not silently skipped.
gap_englid is in the (y,z) TAIL frame at x=-1.7150; no flank aperture shares that surface, so a flank crossing test is NOT APPLICABLE (stated, not silently skipped)
CARGO_GAP outline samples 154 (rev 22: 28, of which 20 on the corner arcs = 5.2 % of the length)
band 1.372-1.775 un-dropped (1.307-1.710 AG)  bay widths 0.516 0.515 0.516
hubcap badge: 4 rings R 0.043429 (= CAP_EMBLEM_D/2), glyph extreme 0.043429, spread 0.00e+00 m
hubcap badge is SELF-CONSISTENCY ONLY -- CAP_EMBLEM_WFRAC has never been compared to a frame; see PHOTOS_WANTED item 7
VERIFY: 0 fail, 0 warn
```

| | |
|---|---|
| cutters rolled back | none |
| non-manifold edges (body) | 0 |
| body faces | 229493 quad, 1032 tri, 5191 ngon |

## Measured dimensions

Frame: geometry is authored un-dropped and `build.py` step 8b subtracts
`RIDE_DROP` from every vertex last, so everything below is **above ground**.
Shaders read the dropped frame, so `Z_BELT`/`V_APEX` are already AG.

| dimension | measured | SPEC | delta |
|---|---|---|---|
| overall length (ex counter) | 4.5800 | 4.0550 | +525.0 mm **OUT** |
| counter tail overhang past body | 0.0000 | — | — |
| overall width (body) | 1.7497 | 1.7500 | -0.3 mm ok |
| overall height (vehicle max, lids excluded) | 2.2268 | — *(no target: this is a max over all stations, and since rev 22 there is no roof-height target at all — H_ROOF 1.960 is RETIRED, see verify.py. Regression-caught by verify row 1a and the roof line below)* | at x = -2.401 |
| wheelbase | 2.4000 | 2.4000 | +0.0 mm ok |
| track front | 1.3690 | 1.3690 | +0.0 mm ok |
| track rear | 1.3590 | 1.3590 | +0.0 mm ok |
| tyre diameter | 0.6650 | 0.6650 | +0.0 mm ok |
| rocker to ground | 0.3177 | — | — |
| belt line @ x=0.962 (live) | 1.2070 | 1.2070 | +0.0 mm ok |
| window sill @ x=0.962 | 1.3070 | 1.3070 | +0.0 mm ok |
| window head @ x=0.962 | 1.7100 | 1.7100 | +0.0 mm ok |
| V-swage apex @ x=0.962 | 0.3400 | 0.3400 | +0.0 mm ok |

### Roof line — three stations, not one scalar

The model read 1.871 against §2.3's 1.960 for seven revisions. That is not a
missing roof-lid curb but a tilt signature — the residual varied by station,
which a scalar cannot express. `Z_BELT` is a line too; see
`t1_mats.z_belt(x)`.

_rev 18: the three residual figures that used to be quoted in this paragraph
(+12 / −29 / −67 mm) were **hand-authored, and the table below had long since
overtaken them** — this file's own header says nothing in it is typed by
hand. The live numbers are in the table; the mid-wheelbase station has no
roof over it at all because the aperture cuts the crown away there, and this
file used to publish the rocker seen through that hole as the roof height._

| station | x | roof z | belt z |
|---|---|---|---|
| front axle | +1.300 | 1.9399 *(n=184)* | 1.2010 |
| mid wheelbase | +0.100 | — *(inside the roof aperture: no roof above 1.710 m at \|y\|<0.30)* | 1.2223 |
| rear axle | -1.100 | 1.9833 *(n=230)* | 1.2436 |

| roof line slope (measured off the mesh) | -18.1 mm/m |
| rake coefficient applied | 17.8 mm/m (1.02°) |

| stance | |
|---|---|
| ride drop @ x=0 | 47.9 mm |
| ride drop @ front axle / rear axle | 71.0 / 28.4 mm |
| rear arch lip → tyre gap (MEASURED on the mesh) | 39.7 mm — SPEC §2 locks 41 ± 8 |
| front arch → tyre gap (untouched circular control) | 40.7 mm |
| V_APEX + V_RISE == Z_BELT | 1.2070 == 1.2070 — held |

### Serving apertures

Measured by `verify.py` by ray-testing the shell, not by counting panes:

```
open serving apertures on +Y: 3
band 1.372-1.775 un-dropped (1.307-1.710 AG)  bay widths 0.516 0.515 0.516
```

SPEC §1.1's taper (0.507 / 0.516 / 0.526) is **RETIRED** — it was the 100 mm
origin error of rev 13, not a real taper. The bays are EQUAL at 0.5155 m;
the measured widths are printed live in the block above, not typed here.
rev-3's three equal 0.600s are retired too, for a different reason.

## Materials

| | |
|---|---|
| datablocks built | 44 |
| bound to >=1 mesh | 42 |
| **still a CONSTANT roughness** | 5 — amber, glass, lens, reflector, ruby |

> SPEC §3 locks the finish as WEATHERED. A constant roughness is the
> physical definition of the plastic look. The only materials that may
> legitimately appear above are the transmissive ones and the sealed
> reflector.

## Object inventory

| | |
|---|---|
| mesh objects | 223 |
| vertices (all meshes) | 329920 |
| faces (all meshes) | 320641 |

| prefix | n |
|---|---|
| `capvw` | 8 |
| `gal_hook` | 6 |
| `seal_bay` | 6 |
| `bracket` | 5 |
| `cap` | 4 |
| `capring` | 4 |
| `gal_bot` | 4 |
| `gal_botcap` | 4 |
| `hinge_barrel` | 4 |
| `hinge_leaf` | 4 |
| `rim-1` | 4 |
| `rim1` | 4 |
| `tyre` | 4 |
| `wheelhouse` | 4 |
| `fringe` | 3 |
| `gal_band` | 3 |
| `gal_can_u` | 3 |
| `menucard` | 3 |
| `doorback` | 2 |
| `doorcard` | 2 |
| `gal_caddy` | 2 |
| `gal_caddy_fill` | 2 |
| `gal_can_l` | 2 |
| `gal_rack_up` | 2 |
| `gal_stack` | 2 |
| `gal_tool` | 2 |
| `glass_dm` | 2 |
| `glass_dv` | 2 |
| `glass_ws` | 2 |
| `gutter` | 2 |
| `handle` | 2 |
| `handlever` | 2 |
| `hl_bowl` | 2 |
| `hl_lens` | 2 |
| `hl_ring` | 2 |
| `lid_rail` | 2 |
| `lid_strut` | 2 |
| `louvbay` | 2 |
| `louvres` | 2 |
| `mir_arm` | 2 |
| `mir_head` | 2 |
| `seal_dm` | 2 |
| `seal_dv` | 2 |
| `seal_ws` | 2 |
| `tail` | 2 |
| `visor` | 2 |
| `vwbar` | 2 |
| `wheel_spoke` | 2 |
| `T1_body` | 1 |
| `bulb_string` | 1 |
| `bumper_f` | 1 |
| `cab_floor` | 1 |
| `calidad_L` | 1 |
| `col` | 1 |
| `counter` | 1 |
| `counter_nosing` | 1 |
| `counter_top` | 1 |
| `dash` | 1 |
| `dash_glovebox` | 1 |
| `dash_grille` | 1 |
| `dash_knob` | 1 |
| `englid_handle` | 1 |
| `fuel_flap` | 1 |
| `gal_appliance` | 1 |
| `gal_backdrop_f` | 1 |
| `gal_end_a` | 1 |
| `gal_end_f` | 1 |
| `gal_pale` | 1 |
| `gal_rack_hi` | 1 |
| `gal_rack_lo` | 1 |
| `gal_rack_shelf` | 1 |
| `gal_rail` | 1 |
| `gal_shelf_b` | 1 |
| `gal_sqbottle` | 1 |
| `gal_sqcap` | 1 |
| `gal_tube` | 1 |
| `gal_tube_ch` | 1 |
| `gal_upright` | 1 |
| `gal_warmer` | 1 |
| `gal_warmer_tap` | 1 |
| `gal_work_a` | 1 |
| `gal_worktop` | 1 |
| `gal_wrap` | 1 |
| `gal_wrap_g` | 1 |
| `galley_backdrop` | 1 |
| `galley_top` | 1 |
| `gear_knob` | 1 |
| `gear_lever` | 1 |
| `glass_bay0_R` | 1 |
| `glass_bay1_R` | 1 |
| `glass_bay2_R` | 1 |
| `glass_rear` | 1 |
| `ind-1_base` | 1 |
| `ind-1_lens` | 1 |
| `ind1_base` | 1 |
| `ind1_lens` | 1 |
| `iron-1F` | 1 |
| `iron1F` | 1 |
| `lid_board` | 1 |
| `lid_main` | 1 |
| `lid_trunk` | 1 |
| `mirror_int` | 1 |
| `mirror_stem` | 1 |
| `pedal_a` | 1 |
| `pedal_b` | 1 |
| `pedal_c` | 1 |
| `plancha` | 1 |
| `plate` | 1 |
| `plate_digits` | 1 |
| `roof_vent` | 1 |
| `script_L` | 1 |
| `script_R` | 1 |
| `seat_back` | 1 |
| `seat_back_p` | 1 |
| `seat_base` | 1 |
| `seat_base_p` | 1 |
| `seat_welt` | 1 |
| `seat_welt_p` | 1 |
| `speedo_bezel` | 1 |
| `speedo_face` | 1 |
| `speedo_glass` | 1 |
| `tail_board` | 1 |
| `tail_board_stay` | 1 |
| `tb_bulbflex` | 1 |
| `tb_bulbs` | 1 |
| `tb_edge_dark` | 1 |
| `tb_edge_red` | 1 |
| `trunk_bay` | 1 |
| `van_floor` | 1 |
| `vw_disc` | 1 |
| `vw_ring` | 1 |
| `wheel_horn` | 1 |
| `wheel_hub` | 1 |
| `wheel_rim` | 1 |

