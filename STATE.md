# STATE — machine-written by `audit.py`. Do not hand-edit.

Every number here was measured off the mesh built in the same process that
wrote this file. If this file and any prose in the repo disagree, this file
is right. Regenerate with `T1_SUB=n blender -b --python audit.py`.

## Provenance

| | |
|---|---|
| generated | 2026-08-09 23:23:34 UTC |
| git commit | `5629786` |
| git subject | SUB=2 green for the first time; measured geometry replaces rev-3 approximations |
| working tree | **DIRTY** — this state is not committed |
| blender | 4.5.3 LTS |
| subdivision | T1_SUB=1 (applied, destructive, before booleans) |
| geometry source | procedural, built this run |

## Guard result

**VERIFY: 0 fail, 0 warn** at T1_SUB=1.

> A pass here is only a pass *at this subdivision level*. The cab-door gap
> booleans passed at SUB=1 and collapsed the shell at SUB=2 for six
> revisions. Run both.

```
x range [-2.138, 2.160]   full-Y [-1.064, 1.150]
dims  L=4.298 W=1.750 H=1.936
measured TRACK_F=1.3713  TRACK_R=1.3613  TYRE_D=0.6650
open serving apertures on +Y: 3
roof at tail = 1.856
shut line door+1: 100 % open
shut line door-1: 100 % open
shut line cargo: 100 % open
shut line englid: 100 % open
band 1.372-1.775 un-dropped (1.307-1.710 AG)  bay widths 0.507 0.516 0.525
VERIFY: 0 fail, 0 warn
```

| | |
|---|---|
| cutters rolled back | none |
| non-manifold edges (body) | 0 |
| body faces | 50390 quad, 227 tri, 2816 ngon |

## Measured dimensions

Frame: geometry is authored un-dropped and `build.py` step 8b subtracts
`RIDE_DROP` from every vertex last, so everything below is **above ground**.
Shaders read the dropped frame, so `Z_BELT`/`V_APEX` are already AG.

| dimension | measured | SPEC | delta |
|---|---|---|---|
| overall length (ex counter) | 4.2984 | 4.2900 | +8.4 mm ok |
| counter tail overhang past body | 0.2916 | — | — |
| overall width (body) | 1.7498 | 1.7500 | -0.2 mm ok |
| overall height | 1.8712 | 1.9600 | -88.8 mm **OUT** |
| _(SPEC §2 factory unladen 1.941; REF_MEASUREMENTS §2.3 measures **1.960** on the real vehicle with the lids closed — above stock despite the 65 mm lowering, implying the roof-lid frame stands proud by 0.10–0.15 m, which is not modelled)_ | | | |
| wheelbase | 2.4000 | 2.4000 | +0.0 mm ok |
| track front | 1.3690 | 1.3690 | +0.0 mm ok |
| track rear | 1.3590 | 1.3590 | +0.0 mm ok |
| tyre diameter | 0.6650 | 0.6650 | +0.0 mm ok |
| rocker to ground | 0.3207 | — | — |
| belt line (live Z_BELT) | 1.2070 | 1.2070 | +0.0 mm ok |
| window sill | 1.3070 | 1.3070 | +0.0 mm ok |
| window head | 1.7100 | 1.7100 | +0.0 mm ok |
| V-swage apex | 0.3400 | 0.3400 | +0.0 mm ok |

| stance | |
|---|---|
| ride drop applied | 65.0 mm |
| arch radius − tyre radius | 41.0 mm (measured 41) |
| V_APEX + V_RISE == Z_BELT | 1.2070 == 1.2070 — held |

### Serving apertures

Measured by `verify.py` by ray-testing the shell, not by counting panes:

```
open serving apertures on +Y: 3
band 1.372-1.775 un-dropped (1.307-1.710 AG)  bay widths 0.507 0.516 0.525
```

SPEC §1.1 measured widths: 0.507 / 0.516 / 0.526 — they are **not** equal;
they grow slightly toward the tail. rev-3's three equal 0.600s are retired.

## Materials

| | |
|---|---|
| datablocks built | 23 |
| bound to >=1 mesh | 23 |
| **still a CONSTANT roughness** | 6 — amber, brass, glass, lens, reflector, ruby |

> SPEC §3 locks the finish as WEATHERED. A constant roughness is the
> physical definition of the plastic look. The only materials that may
> legitimately appear above are the transmissive ones and the sealed
> reflector.

## Object inventory

| | |
|---|---|
| mesh objects | 147 |
| vertices (all meshes) | 126477 |
| faces (all meshes) | 120787 |

| prefix | n |
|---|---|
| `capvw` | 24 |
| `seal_bay` | 6 |
| `vwbar` | 6 |
| `bracket` | 5 |
| `cap` | 4 |
| `rim-1` | 4 |
| `rim1` | 4 |
| `tyre` | 4 |
| `fringe` | 3 |
| `menucard` | 3 |
| `doorback` | 2 |
| `doorcard` | 2 |
| `glass_dm` | 2 |
| `glass_dv` | 2 |
| `glass_ws` | 2 |
| `gutter` | 2 |
| `handle` | 2 |
| `handlever` | 2 |
| `hl_bowl` | 2 |
| `hl_lens` | 2 |
| `hl_ring` | 2 |
| `louvres` | 2 |
| `mir_arm` | 2 |
| `mir_head` | 2 |
| `ragframe` | 2 |
| `seal_dm` | 2 |
| `seal_dv` | 2 |
| `seal_ws` | 2 |
| `shelf` | 2 |
| `tail` | 2 |
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
| `dash` | 1 |
| `englid_handle` | 1 |
| `fuel_flap` | 1 |
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
| `plancha` | 1 |
| `plate` | 1 |
| `plate_digits` | 1 |
| `rag` | 1 |
| `roof_vent` | 1 |
| `script_L` | 1 |
| `script_R` | 1 |
| `seat_back` | 1 |
| `seat_base` | 1 |
| `van_floor` | 1 |
| `vw_disc` | 1 |
| `vw_ring` | 1 |
| `wheel_rim` | 1 |

