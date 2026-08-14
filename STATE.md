# STATE — machine-written by `audit.py`. Do not hand-edit.

Every number here was measured off the mesh built in the same process that
wrote this file. If this file and any prose in the repo disagree, this file
is right. Regenerate with `T1_SUB=n blender -b --python audit.py`.

## Provenance

| | |
|---|---|
| generated | 2026-08-14 03:54:31 UTC |
| git commit | `3366d5e` |
| git subject | rev 16: handoff and the rev-17 next-context prompt |
| working tree | clean |
| blender | 4.5.3 LTS |
| subdivision | T1_SUB=1 (applied, destructive, before booleans) |
| geometry source | procedural, built this run |

## Guard result

**VERIFY: 0 fail, 1 warn** at T1_SUB=1.

> A pass here is only a pass *at this subdivision level*. The cab-door gap
> booleans passed at SUB=1 and collapsed the shell at SUB=2 for six
> revisions. Run both.

```
x range [-1.905, 2.160]   full-Y [-1.064, 1.150]
dims  L=4.065 W=1.750 roof@rear-axle=1.983 (raw resid +23 mm; dome deficit +0 mm still unmodelled) (bbox top 3.046)
rear overhang 0.7730 m = 0.3221 of the wheelbase (measured 0.773 +- 0.022 m)
measured TRACK_F=1.3713  TRACK_R=1.3613  TYRE_D=0.6650
open serving apertures on +Y: 3
roof at tail = 1.988
roof aperture: open, and solid fore / aft / both sides
shut line door+1: 100 % open
shut line door-1: 100 % open
shut line cargo: 100 % open
shut line englid: 100 % open
band 1.372-1.775 un-dropped (1.307-1.710 AG)  bay widths 0.516 0.515 0.516
VERIFY: 0 fail, 1 warn
warn  roof crown @ rear axle (dome-corrected) 1.983 vs spec 1.960 (+23 mm)
```

| | |
|---|---|
| cutters rolled back | none |
| non-manifold edges (body) | 0 |
| body faces | 60461 quad, 465 tri, 3107 ngon |

## Measured dimensions

Frame: geometry is authored un-dropped and `build.py` step 8b subtracts
`RIDE_DROP` from every vertex last, so everything below is **above ground**.
Shaders read the dropped frame, so `Z_BELT`/`V_APEX` are already AG.

| dimension | measured | SPEC | delta |
|---|---|---|---|
| overall length (ex counter) | 4.0648 | 4.2900 | -225.2 mm **OUT** |
| counter tail overhang past body | 0.2902 | — | — |
| overall width (body) | 1.7497 | 1.7500 | -0.3 mm ok |
| overall height (max, any station) | 3.0169 | 1.9600 | +1056.9 mm **OUT** |
| _(rev 8: a single scalar height is the WRONG test now that the rake is modelled — 1.960 is the maximum of a sloping line, taken at its highest station. See the three-station roof line below. §2.3's inference that the roof-lid frame stands 0.10–0.15 m proud is **refuted** at ~13σ; measured proud height is 26 ± 7 mm.)_ | | | |
| wheelbase | 2.4000 | 2.4000 | +0.0 mm ok |
| track front | 1.3690 | 1.3690 | +0.0 mm ok |
| track rear | 1.3590 | 1.3590 | +0.0 mm ok |
| tyre diameter | 0.6650 | 0.6650 | +0.0 mm ok |
| rocker to ground | 0.3175 | — | — |
| belt line @ x=0.962 (live) | 1.2070 | 1.2070 | +0.0 mm ok |
| window sill @ x=0.962 | 1.3070 | 1.3070 | +0.0 mm ok |
| window head @ x=0.962 | 1.7100 | 1.7100 | +0.0 mm ok |
| V-swage apex @ x=0.962 | 0.3400 | 0.3400 | +0.0 mm ok |

### Roof line — three stations, not one scalar

The model read 1.871 against §2.3's 1.960 for seven revisions. That is not a
missing roof-lid curb: the residual against the photograph was **+12 mm at
the front axle, −29 mm mid-wheelbase, −67 mm at the rear axle** — a tilt
signature. `Z_BELT` is a line too; see `t1_mats.z_belt(x)`.

| station | x | roof z | belt z |
|---|---|---|---|
| front axle | +1.300 | 1.9400 | 1.2010 |
| mid wheelbase | +0.100 | 0.3497 | 1.2223 |
| rear axle | -1.100 | 1.9835 | 1.2436 |

| roof line slope (measured off the mesh) | -18.1 mm/m |
| rake coefficient applied | 17.8 mm/m (1.02°) |

| stance | |
|---|---|
| ride drop @ x=0 | 47.9 mm |
| ride drop @ front axle / rear axle | 71.0 / 28.4 mm |
| arch radius − tyre radius | 41.0 mm (measured 41) |
| V_APEX + V_RISE == Z_BELT | 1.2070 == 1.2070 — held |

### Serving apertures

Measured by `verify.py` by ray-testing the shell, not by counting panes:

```
open serving apertures on +Y: 3
band 1.372-1.775 un-dropped (1.307-1.710 AG)  bay widths 0.516 0.515 0.516
```

SPEC §1.1 measured widths: 0.507 / 0.516 / 0.526 — they are **not** equal;
they grow slightly toward the tail. rev-3's three equal 0.600s are retired.

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
| mesh objects | 181 |
| vertices (all meshes) | 141503 |
| faces (all meshes) | 136243 |

| prefix | n |
|---|---|
| `capvw` | 8 |
| `gal_hook` | 6 |
| `seal_bay` | 6 |
| `bracket` | 5 |
| `cap` | 4 |
| `gal_bot` | 4 |
| `gal_botcap` | 4 |
| `rim-1` | 4 |
| `rim1` | 4 |
| `tyre` | 4 |
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
| `louvres` | 2 |
| `mir_arm` | 2 |
| `mir_head` | 2 |
| `seal_dm` | 2 |
| `seal_dv` | 2 |
| `seal_ws` | 2 |
| `tail` | 2 |
| `vwbar` | 2 |
| `wblade` | 2 |
| `wiper_arm` | 2 |
| `wiper_boss` | 2 |
| `wiper_pivot` | 2 |
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
| `lid_strut` | 1 |
| `plancha` | 1 |
| `plate` | 1 |
| `plate_digits` | 1 |
| `roof_vent` | 1 |
| `script_L` | 1 |
| `script_R` | 1 |
| `seat_back` | 1 |
| `seat_base` | 1 |
| `van_floor` | 1 |
| `vw_disc` | 1 |
| `vw_ring` | 1 |
| `wheel_rim` | 1 |

