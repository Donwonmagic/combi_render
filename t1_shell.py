"""
Kombi shell features: windscreen, cab door glazing, serving bays, rear glass,
panel gaps, wheel arches, closed ragtop.  Geometry follows SPEC.md rev 3.
"""
import bpy, bmesh, math, os
import numpy as np
from mathutils import Vector
import t1_core as T

# ============================================================== WINDSCREEN
P_TOP = Vector((1.8340, 0.0, 1.7745))
P_BOT = Vector((2.0400, 0.0, 1.3755))
WS_DIR = (P_BOT - P_TOP).normalized()
WS_MID = (P_TOP + P_BOT) * 0.5
WS_N = Vector((-WS_DIR.z, 0.0, WS_DIR.x))
if WS_N.x < 0:
    WS_N = -WS_N

WS_PANE_W, WS_PANE_H, WS_DIV, WS_R = 0.5850, 0.3770, 0.0260, 0.050


def _ws(pane_w, pane_h, depth, off, tag):
    obs = []
    for s in (1, -1):
        yc = s * (WS_DIV + WS_PANE_W / 2)
        pts = T.rrect(pane_w, pane_h, WS_R, seg=8)
        o = WS_MID + Vector((0, yc, 0)) + WS_N * off
        obs.append(T.solid_prism(o, (0, 1, 0), tuple(-WS_DIR), tuple(WS_N),
                                 pts, depth, name=f"{tag}{s}"))
    return obs


def windscreen_cutters():
    return _ws(WS_PANE_W, WS_PANE_H, 0.10, 0.0, "cut_ws")


def windscreen_glass():
    return _ws(WS_PANE_W - 0.006, WS_PANE_H - 0.006, 0.006, -0.012, "glass_ws")


def windscreen_seals():
    obs = []
    for s in (1, -1):
        yc = s * (WS_DIV + WS_PANE_W / 2)
        pts = T.rrect(WS_PANE_W + 0.0125, WS_PANE_H + 0.0125, WS_R, seg=8)
        inn = T.rrect(WS_PANE_W - 0.0055, WS_PANE_H - 0.0055, WS_R, seg=8)
        o = WS_MID + Vector((0, yc, 0)) - WS_N * 0.004
        outer = T.solid_prism(o, (0, 1, 0), tuple(-WS_DIR), tuple(WS_N),
                              pts, 0.0090, name=f"seal_ws{s}")
        cut = T.solid_prism(o, (0, 1, 0), tuple(-WS_DIR), tuple(WS_N),
                            inn, 0.10, name=f"sealcut{s}")
        T.boolean(outer, cut); T.apply_mods(outer)
        bpy.data.objects.remove(cut, do_unlink=True)
        obs.append(outer)
    return obs


# ============================================ CAB DOOR GLAZING (main + vent)
# FRAME: UN-DROPPED.  These build cutter/pane geometry in build.py steps 1-4,
# i.e. before step 8b subtracts T.RIDE_DROP from every vertex.  A feature
# authored at z here ends up at z - 0.065 above ground.
#   Z_SILL 1.372 -> 1.307 above ground
#   Z_HEAD 1.775 -> 1.710 above ground
Z_SILL, Z_HEAD, BAY_R = 1.3720, 1.7750, 0.0550

DOOR_MAIN = [
    (1.0000, 1.4380), (1.0180, 1.4120), (1.4200, 1.4020), (1.5480, 1.4060),
    (1.5720, 1.4300), (1.5720, 1.7640), (1.5480, 1.7900), (1.1000, 1.7960),
    (1.0100, 1.7880), (0.9940, 1.7560),
]
# rev 23.  VENT_TOP_DROP -- the vent's top edge was 20.7 mm ABOVE the cab
# door's own top shut line, so the vent hole broke the door's boundary and the
# door could not open.  That is a TOPOLOGICAL defect, not a livery one: an
# aperture cut in a panel cannot extend past that panel's own outline, and
# establishing it needs no photograph and no scale.  See SPEC sec.10.62.
#
# WHICH MEMBER MOVED, and why:  the owner confirmed from ref_workshop.jpg that
# the door glass IS divided into a vent plus a main pane, so the vent stays.
# He could NOT resolve whether its top edge reaches the door's top rail, so the
# door's top-front corner -- which IS legible in that frame -- was left alone
# and the vent's top edge was dropped instead.  The DROP IS AUTHORED, not
# measured: it is the smallest value that satisfies the invariant with the
# stated clearance.  The vent's true top edge is OPEN and UNMEASURED.
# T1_VENTDROP defaults to the shipped value (a proven no-op) and exists so the
# assert can be FALSIFIED: setting it to 0 restores the rev-22 geometry exactly
# and the show-flank assert must fire on door_vent.
VENT_TOP_DROP = float(os.environ.get("T1_VENTDROP", "0.0280"))
DOOR_VENT = [
    (1.6060, 1.4300), (1.7420, 1.4180), (1.7560, 1.4460),
    (1.7160, 1.7700 - VENT_TOP_DROP),
    (1.6900, 1.7880 - VENT_TOP_DROP), (1.6060, 1.7860 - VENT_TOP_DROP),
]


def _smooth(pts, iters=3):
    p = list(pts)
    for _ in range(iters):
        n = len(p)
        p = [((p[i - 1][0] + 2 * p[i][0] + p[(i + 1) % n][0]) / 4,
              (p[i - 1][1] + 2 * p[i][1] + p[(i + 1) % n][1]) / 4)
             for i in range(n)]
    return p


def _resample(pts, n):
    a = np.array(pts + [pts[0]], dtype=float)
    d = np.concatenate([[0], np.cumsum(np.hypot(np.diff(a[:, 0]),
                                                np.diff(a[:, 1])))])
    t = np.linspace(0, d[-1], n, endpoint=False)
    return list(zip(np.interp(t, d, a[:, 0]), np.interp(t, d, a[:, 1])))


DOOR_MAIN_S = _smooth(_resample(DOOR_MAIN, 88), 4)
DOOR_VENT_S = _smooth(_resample(DOOR_VENT, 56), 3)


# ====================================================== SIDE SERVING BAYS
# SPEC rev3 sec.1.1 -- three open serving hatches then a frosted rear bay
# SPEC sec.1.1 retires rev-3's "three evenly sized, evenly spaced" bays.
# MEASURED edges off the reference photographs, tuples are (rear, front) to
# match bay_outline()'s x1 - x0:
#   bay 0  front +0.820  rear +0.313   width 0.507
#   bay 1  front +0.195  rear -0.321   width 0.516
#   bay 2  front -0.435  rear -0.960   width 0.525
# The bays grow slightly toward the tail; they are NOT equal.
# rev 13.  TWO corrections, both measured, and the first explains a 100 mm error
# that also turned up independently in the tail length.
#
# (1) POSITION.  All three bays sat 105 mm too far AFT, as a pure translation --
#     the widths and the spacings were right.  `REF_MEASUREMENTS`'s "MODEL x"
#     column maps the photograph as X = (495.8 - u)/211.5 and calls X = 0
#     mid-wheelbase.  But 495.8 px IS the hub midpoint, and this model's axles
#     are at +1.300 / -1.100, so its mid-wheelbase is x = +0.100.  Every REF
#     model-frame number is 100 mm aft of where it says.  Measured bay centres,
#     from six sub-pixel cut edges anchored by ratio to the two hubs (which are
#     both locked by the 2.400 m wheelbase): +0.672 / +0.047 / -0.598 +/- 0.015.
#
# (2) WIDTH.  The bays are EQUAL.  SPEC 10.5's 0.507 / 0.516 / 0.525 is
#     perspective, not geometry: three exactly equal 0.5155 m bays project to
#     106.76 / 109.12 / 111.52 px against a measured 107.23 / 109.13 / 111.04 --
#     residuals +0.47 / +0.01 / -0.48 px.  Under the corrected homography the
#     measured widths are 0.5177 / 0.5155 / 0.5132, spread 0.36 % of the mean.
#     Perspective in fact over-explains the taper (4.4-4.5 points predicted
#     against 3.55 measured), so if anything they narrow very slightly forward.
#     Held equal: a 2 mm taper is below the measurement floor and inventing one
#     is how 10.5's version got here.
#
# STATE.md's "SPEC 1.1 measured widths 0.507/0.516/0.526 -- they are NOT equal"
# is therefore retired.  rev-3's three equal 0.600s stay retired; the width is
# 0.5155, not 0.600.
BAY_W = 0.5155                                   # equal, measured
BAY_CX = (0.6720, 0.0470, -0.5980)               # measured centres
BAYS = [(cx - BAY_W / 2.0, cx + BAY_W / 2.0) for cx in BAY_CX]
OPEN_BAYS = (0, 1, 2)          # +Y show side: all three glass removed
# SPEC r4: there is NO fourth bay. Aft of bay 3 is solid sheet metal carrying
# the "100% Calidad" decal (measured: SPEC 8.4). Re-adding a bay is a regression.
SHOW_SIDE = 1                  # +Y


def bay_outline(i):
    x0, x1 = BAYS[i]
    return T.rrect(x1 - x0, Z_HEAD - Z_SILL, BAY_R, seg=8)


def bay_centre(i):
    x0, x1 = BAYS[i]
    return ((x0 + x1) / 2, (Z_SILL + Z_HEAD) / 2)


def _flat_cut(outline, cx, cz, side, depth=0.30, y=0.80, name="c"):
    pts = [(u + cx, v + cz) for (u, v) in outline]
    return T.solid_prism((0, side * y, 0), (1, 0, 0), (0, 0, 1),
                         (0, side, 0), pts, depth, name=name)


def side_cutters():
    """all glazing apertures in both flanks"""
    obs = []
    for s in (1, -1):
        obs.append(_flat_cut(DOOR_MAIN_S, 0, 0, s, name=f"cut_dm{s}"))
        obs.append(_flat_cut(DOOR_VENT_S, 0, 0, s, name=f"cut_dv{s}"))
        for i in range(len(BAYS)):
            cx, cz = bay_centre(i)
            obs.append(_flat_cut(bay_outline(i), cx, cz, s,
                                 name=f"cut_bay{i}{s}"))
    return obs


def side_glass():
    """glass panes; the three show-side serving bays get none"""
    obs = []
    for s in (1, -1):
        obs.append(T.conform_solid(T.poly_offset(DOOR_MAIN_S, -0.004), s,
                                   off=-0.010, thick=0.006,
                                   name=f"glass_dm{s}"))
        obs.append(T.conform_solid(T.poly_offset(DOOR_VENT_S, -0.004), s,
                                   off=-0.010, thick=0.006,
                                   name=f"glass_dv{s}"))
        for i in range(len(BAYS)):
            if s == SHOW_SIDE and i in OPEN_BAYS:
                continue                       # serving hatch: no glass
            cx, cz = bay_centre(i)
            out = [(u + cx, v + cz) for (u, v) in bay_outline(i)]
            g = T.conform_solid(T.poly_offset(out, -0.004), s, off=-0.010,
                                thick=0.006, name=f"glass_bay{i}_{'L' if s > 0 else 'R'}")
            obs.append(g)
    return obs


# SPEC r4: calidad_pane() DELETED. The decal is applied to sheet metal by
# a conform_panel in build.py, not to a glass pane. See SPEC 0.2 and 8.4.


def bay_seals():
    """rubber surrounds in every aperture"""
    obs = []
    for s in (1, -1):
        for outline, tag in ((DOOR_MAIN_S, "dm"), (DOOR_VENT_S, "dv")):
            obs.append(T.conform_ring(outline, s, 0.0075, off=-0.0030,
                                      thick=0.0090, name=f"seal_{tag}{s}"))
        for i in range(len(BAYS)):
            cx, cz = bay_centre(i)
            out = [(u + cx, v + cz) for (u, v) in bay_outline(i)]
            obs.append(T.conform_ring(out, s, 0.0075, off=-0.0030, thick=0.0090,
                                      name=f"seal_bay{i}{s}"))
    return obs


# ============================================================ REAR GLAZING
REAR_W, REAR_H, REAR_Z = 1.0400, 0.3400, 1.4500


def rear_cutter():
    pts = T.rrect(REAR_W, REAR_H, 0.060, seg=8)
    pts = [(u, v + REAR_Z) for (u, v) in pts]
    # rev 16: anchored to the tail skin, not to a constant.  The tail
    # re-space moved X_TAIL -2.108 -> -1.873 and this cutter stayed at -2.20,
    # so it sat entirely BEHIND the vehicle and was rolled back -- caught by
    # verify's rolled-back-cuts row, not by prose.
    return T.solid_prism((T.X_TAIL - 0.092, 0, 0), (0, 1, 0), (0, 0, 1),
                         (-1, 0, 0), pts, 0.40, name="cut_rear")


def rear_glass():
    pts = T.rrect(REAR_W - 0.008, REAR_H - 0.008, 0.060, seg=8)
    pts = [(u, v + REAR_Z) for (u, v) in pts]
    # rev 16: 20.0 mm inboard of the tail skin, as authored (-2.0880 against
    # the old X_TAIL of -2.1080), now expressed in terms of it.
    return T.solid_prism((T.X_TAIL + 0.0200, 0, 0), (0, 1, 0), (0, 0, 1),
                         (-1, 0, 0), pts, 0.006, name="glass_rear")


# --------------------------------------------------------------- wheel arch
ARCH_R = 0.3735                      # rev6: TIRE_R 0.3325 + measured 41 mm


def arch_z(x):
    """Authored z of the arch centre at axle station x.

    rev 8: was the scalar `T.TIRE_R + T.RIDE_DROP`. Step 8b now shears rather
    than dropping, so this has to track rake_drop(x) for the arch to stay
    concentric with its own wheel.

    OPEN INCONSISTENCY -- see SPEC sec.10.7. If the rake is suspension-derived
    then the arches should NOT stay concentric: the front arch would sit
    rake*wheelbase = 0.0330 * 2.400 = 79 mm lower relative to its wheel than
    the rear does. But the rear arch gap MEASURES ~30 mm off ref_side.jpg
    (arch lip y 524 +/- 2 against a tyre top computed at 532.3 from the rim
    fit, 211.5 px/m), and SPEC sec.2 locks it at 41 mm. Either way,
    front = rear - 79 mm is NEGATIVE, i.e. the tyre inside the bodywork.
    Two measurements off the real vehicle contradict each other.

    Held concentric because that is the only option which keeps both measured
    numbers and produces no impossible geometry. Resolving it needs a
    photograph with an UNOCCLUDED front wheel -- in ref_side.jpg a man stands
    directly in front of it, and every attempt to measure the front arch here
    locked onto his red shirt instead.
    """
    return T.TIRE_R + T.rake_drop(x)


ARCH_Z = arch_z(T.X_AXLE_R)          # back-compat scalar; prefer arch_z(x)


# ---------------------------------------------- rev 16: the REAR arch is not
# a circle.  LOFT_GROUND_rev15 sec.2 traced the lip sub-pixel on the R channel
# (185 of 232 columns) and fitted it four ways:
#
#     circle                                rms 11.41 mm
#     symmetric power law, best window      rms  2.7-4.2 mm
#     superellipse                          rms  2.67 mm
#
# so a circle is refuted overwhelmingly.  The EXPONENT is NOT used here: it is
# window-dependent (3.50 at +-0.249 m, 4.28 at +-0.449 m), so 3.9 +- 0.2 is a
# property of a choice of window, not of the arch.  The assumption-free
# normalised profile TABLE is used instead, exactly as NEXT_CONTEXT sec.6.2
# instructs.  Delta-x as a fraction of the half-width, drop as a fraction of
# crown-to-foot; the |t| = 1.0 end point is the foot by definition.
#
# Two things about the rear arch are already RIGHT and must not move:
#   * lip height above the hub at the crown 0.3726 +- 0.0052 m against the
#     built ARCH_R = 0.3735 -- the RADIUS is right, the SHAPE is not;
#   * the crown is centred on the rear axle to 0.2 px ~ 1 mm (column-only
#     comparison, no scale at all).
# What is wrong is the WIDTH: 0.92 +- 0.03 m measured (dimensionless form
# width / rear rim flange OD = 2.158 +- 0.027) against 2*ARCH_R = 0.747 built.
#
# The FRONT arch is left circular on purpose.  It was never measured -- a man
# stands directly in front of it in ref_side.jpg and every attempt to trace it
# has locked onto his red shirt -- and widening it would bring the arch lip to
# within 57 mm of the cab-door shut line's bottom run, which is the exact
# geometry that collapsed the shell 205562 v -> 12 v for six revisions
# (see the assert below and SPEC sec.10.1).
ARCH_W_REAR = 0.920                  # LOFT_GROUND sec.2.5, +- 0.03 m
#
# rev 18 -- THREE COUPLED CORRECTIONS, APPLIED TOGETHER BECAUSE ANY ONE OF THEM
# ALONE LANDS THE OTHER TWO WRONG.  See AUDIT_rev18_loft.md sections 3, 4 and 5.
#
# (a) THE CROWN WAS DOUBLE-COUNTED.  rear_arch_outline evaluates
#     z = ARCH_R - h*_arch_drop(t), and the raw table's smallest drop is 0.057,
#     never 0.  But ARCH_R *is* the measured crown lip height -- SPEC 10.37 and
#     the comment 14 lines above both say it is HELD, and LOFT_GROUND sec.2.6
#     instructs "hold the crown height, widen to 0.92 m, and use the sec.2.3
#     profile".  Subtracting a crown drop from the crown itself put the lip
#     20.9 mm low at the axle and the tyre gap at 20.1 mm against SPEC sec.2's
#     locked 41 +- 8.  MEASURED on the built mesh at 20.2 mm, and the FRONT
#     arch -- untouched, still circular -- reads ARCH_R to 0.3 mm in the same
#     run as the positive control.  The table is now normalised so its MINIMUM
#     is zero, which makes the highest point of the built lip exactly ARCH_R.
#     That is what "hold the crown height" means, expressed rather than asserted.
#
# (b) THE (0.10, 0.014) ENTRY IS NOT A MEASUREMENT.  Re-traced in rev 18:
#     reproducing LOFT_GROUND sec.2.1's own +-7-row half-max method DOES
#     reproduce a 4.5 px spike, but the raw pixels put the lip edge on row
#     524->525 at EVERY column across it -- the window straddles a dark
#     folk-art speck 5 px above the lip and locks onto the band.  Re-anchored
#     on the edge the lip reads 371.4 / 370.9 / 371.4 / 372.1 / 372.3 /
#     372.1 mm: FLAT.  And through LOFT_GROUND sec.0's own map, dx/a = +0.10
#     is u = 759.53 -- inside the band sec.2.1's text says it REJECTED
#     ("dark folk-art specks at u 657, 758-761, 844-845").  The 9-wide median
#     filter sec.2.1 announces was never propagated into the sec.2.3 table.
#     Independent corroboration needing no re-trace: sec.2.4 says the crown is
#     flat within 1.2 mm over 164 mm, a span containing this station, and
#     0.046 x h = 16.0 mm is 13x that.  Replaced by the median of its
#     neighbours, 0.0585, which is what the announced filter would have given.
#
# (c) THE SIGN CONVENTION WAS MIRRORED.  SPEC 10.37 and the note below assert
#     the table is stated forward at -0.90 and aft at +0.90.  rear_arch_outline
#     emits (t*a, ...) and solid_prism is passed u = (1,0,0), and +x is FORWARD
#     in t1_core -- so t = +0.90 was landing forward.  Settled empirically, not
#     by argument: LOFT_GROUND sec.0's map is X(u) = 641220.4/(u+11140) -
#     55.0322, so increasing u runs AFT, and the anomalous +0.10 station lands
#     at u 759.5 inside the AFT rejected band.  +dx is aft.  The lookup below
#     is negated, which keeps the outline's traversal order (and therefore the
#     prism's winding) untouched while putting each drop on its own side.
#
# WHAT THIS DOES NOT DO: it does not touch ARCH_R, ARCH_W_REAR, the front arch,
# or any station.  Only the profile's normalisation, one outlier, and a sign.
_ARCH_PROFILE = [                    # (delta-x / half-width, drop / crown-to-foot)
    (-1.00, 1.000), (-0.95, 0.754), (-0.90, 0.583), (-0.80, 0.370),
    (-0.70, 0.246), (-0.60, 0.156), (-0.50, 0.117), (-0.40, 0.090),
    (-0.30, 0.078), (-0.20, 0.074), (-0.10, 0.068), ( 0.00, 0.060),
    ( 0.10, 0.0585), ( 0.20, 0.057), ( 0.30, 0.058), ( 0.40, 0.076),
    ( 0.50, 0.101), ( 0.60, 0.146), ( 0.70, 0.217), ( 0.80, 0.354),
    ( 0.90, 0.593), ( 0.95, 0.754), ( 1.00, 1.000),
]
# The table is stated for the forward half at -0.90 and the aft half at +0.90
# with 0.583 / 0.593 -- it is a TRACE, not a symmetric model, and the small
# left/right difference is kept rather than averaged away.  The -0.95 point is
# mirrored from +0.95, which the trace reached and the forward side did not.
_ARCH_T = [p[0] for p in _ARCH_PROFILE]
_ARCH_D0 = [p[1] for p in _ARCH_PROFILE]
# (a): re-base so the crown drop is ZERO and the foot is still exactly 1.000.
# Both end conditions of rear_arch_outline are preserved by construction --
# t = 0 gives z = ARCH_R, t = +-1 gives z = z_foot -- so this changes the SHAPE
# between them and neither endpoint.  Written as an expression of the table, not
# as a second table, so re-tracing the profile cannot leave the re-basing stale.
_ARCH_DMIN = min(_ARCH_D0)
_ARCH_D = [(d - _ARCH_DMIN) / (1.0 - _ARCH_DMIN) for d in _ARCH_D0]
assert abs(min(_ARCH_D)) < 1e-12 and abs(max(_ARCH_D) - 1.0) < 1e-12


def _arch_drop(t):
    """drop as a fraction of crown-to-foot, at delta-x/half-width = t

    rev 18 (c): t is NEGATED because the table's +dx is AFT while this
    module's +x is forward.  See the block above -- established from the
    projective flank map, not from the convention SPEC 10.37 asserts.
    """
    return float(np.interp(-t, _ARCH_T, _ARCH_D))


def rear_arch_outline(x_axle, n=96, floor=-0.400):
    """Closed (dx, dz) outline of the rear arch cutter, about (x_axle, arch_z).

    dz is measured from the AXLE CENTRE, so the crown sits at +ARCH_R and the
    concentricity that ref_side.jpg confirms to ~1 mm is structural here rather
    than a comment.
    """
    a = ARCH_W_REAR / 2.0
    z_foot = T.ZB(x_axle) - arch_z(x_axle)       # rocker underside, axle frame
    h = ARCH_R - z_foot                          # crown-to-foot
    pts = []
    for i in range(n + 1):
        t = -1.0 + 2.0 * i / n
        pts.append((t * a, ARCH_R - h * _arch_drop(t)))
    pts.append(( a, floor))
    pts.append((-a, floor))
    return pts


def arch_cutters():
    obs = []
    for s in (1, -1):
        obs.append(T.cylinder((T.X_AXLE_F, s * 0.735, arch_z(T.X_AXLE_F)),
                              (0, 1, 0), ARCH_R, 0.62, seg=80,
                              name=f"arch{T.X_AXLE_F:.0f}{s}"))
    pts = rear_arch_outline(T.X_AXLE_R)
    for s in (1, -1):
        obs.append(T.solid_prism((T.X_AXLE_R, s * 0.735, arch_z(T.X_AXLE_R)),
                                 (1, 0, 0), (0, 0, 1), (0, 1, 0),
                                 pts, 0.62, name=f"arch{T.X_AXLE_R:.0f}{s}"))
    return obs


# ---------------------------------------------------------------- panel gaps
GAPW = 0.0055

# CAB DOOR SHUT LINE -- frame: UN-DROPPED (cut in build.py step 3, before the
# ride-height drop).  Subtract T.RIDE_DROP for the above-ground height.
#
# The bottom run used to sit at z 0.4240-0.4360 un-dropped = 0.359 above
# ground.  That is wheel-centre height, and it ran straight across the OPEN
# front wheel arch for 745 mm of its 930 mm length (arch aperture x
# 0.9265...1.6735).  There is no sheet metal there at all, so there was no
# shut line to cut -- and at T1_SUB=2 the boolean collapsed the shell from
# 205562 v to 12 v and was rolled back, shipping a production model with no
# cab-door shut line.  Measured correlate of the failure: the outer-skin slope
# relative to the cutter's extrusion axis exceeds t_skin / gap_width =
# 2.8/5.5 = 0.51 across the arch lip.  Tested at SUB=2: z 0.4248 collapses,
# 0.4548 shreds (8490 v), 0.56 / 0.78 / 0.80 / 0.83 all clean.
#
# rev 7 put the bottom run at z 0.7800-0.7920 un-dropped, clearing a front arch
# aperture top of ARCH_Z + ARCH_R = 0.7710 by 9-21 mm.
#
# rev 8 BREAKS THAT CLEARANCE: step 8b now shears instead of dropping, so the
# front arch is authored at rake_drop(1.300) = 0.0794 rather than RIDE_DROP =
# 0.0650 -- 14.4 mm higher. The front arch top moves 0.7710 -> 0.7854 and the
# old 0.7800 bottom run would sit 5.4 mm BELOW it, crossing the arch lip: the
# exact condition that collapsed the shell 205562 v -> 12 v at SUB=2 for six
# revisions. The bottom run is therefore lifted 20 mm to 0.8000-0.8160
# (clearance 14.6-30.6 mm). 0.80 is one of the values tested clean at SUB=2.
# The assert below makes this structural rather than a comment.
# rev 23.  THE B-PILLAR HAD NEGATIVE WIDTH.  The cab door's REAR shut line ran
# 5.2 mm INSIDE serving bay 0's forward edge, so bay 0 straddled the door's own
# boundary: part of the aperture was in the door and part in the body, and the
# door could not open.  Topological, provable without any photograph, and
# nothing in the repo had ever looked (SPEC sec.10.62).
#
# WHICH MEMBER MOVED:  bay 0's edges are LOCKED -- the three bays are equal at
# 0.5155 m (sec.10.29) and the band Z_SILL..Z_HEAD is guarded every revision.
# The door's rear-run x carries NO provenance anywhere in the repo.  So the
# DOOR moves, and it moves as a whole so the door's rear edge stays a single
# straight lean rather than gaining a jog inside the window band.
#
# DOOR_REAR_DX is EXPRESSED IN TERMS OF THE LOCKED BAY, never as a bare number,
# so re-measuring the bays can never leave this outline asserting a stale
# clearance (sec.10.25's rule -- the rule that merged the VW glyph into an X
# twice when it was ignored).
#
# B_PILLAR IS AUTHORED, NOT MEASURED.  It is the minimum clearance that makes
# the topology valid.  ref_workshop.jpg shows the pillar between the cab door
# and the first side window is visibly WIDER than the pillars between the three
# side windows, but that frame is a three-quarter view with a projective flank
# map and no admissible px/m on the door plane, so no number was taken from it.
# THE B-PILLAR'S TRUE WIDTH IS OPEN AND UNMEASURED.
#
# T1_BPILLAR exists so the assert below can be FALSIFIED by anyone, not just
# asserted to work.  It defaults to the shipped value and that default is a
# proven no-op (rev 20's pattern).  Setting it negative re-creates the exact
# rev-22 defect and the show-flank assert must fire.
B_PILLAR = float(os.environ.get("T1_BPILLAR", "0.0120"))
_DOOR_REAR_X0 = 0.9245                      # smoothed rear run's min x, rev 22
DOOR_REAR_DX = (BAYS[0][1] + B_PILLAR) - _DOOR_REAR_X0
DOOR_GAP = [
    (1.8171, 0.8120), (1.8080, 1.1200), (1.7960, 1.4000),
    (1.7600, 1.6280), (1.7220, 1.7620), (1.7020, 1.8020),
    (1.5200, 1.8130), (1.2800, 1.8150), (1.0800, 1.8130),
    (0.9680 + DOOR_REAR_DX, 1.8060),
    (0.9380 + DOOR_REAR_DX, 1.7000), (0.9240 + DOOR_REAR_DX, 1.4000),
    (0.9120 + DOOR_REAR_DX, 1.0000), (0.9084 + DOOR_REAR_DX, 0.8160),
    (1.1000, 0.8040), (1.4000, 0.8000), (1.6500, 0.8040),
]
# ===========================================================================
# rev 42 -- HIS DEFECT REPORT 5: "the doors extend lower, around the wheel
# well".  SPEC 10.100.
#
# WHAT WAS WRONG.  The table above cuts the cab door's bottom as a STRAIGHT
# CHORD ACROSS THE TOP OF THE FRONT WHEEL ARCH, z 0.8000-0.8160 un-dropped,
# 23.0-39.0 mm above the arch crown -- whose BUILT value is
# arch_z(X_AXLE_F) + ARCH_R = 0.4035 + 0.3735 = 0.7770, WATCHED PRINT.  The
# smoothed rev-41 outline's minimum over the arch's x-span is 0.8006, 23.6 mm.
# Every revision from rev 7 to rev 41 shipped that chord.
#
# MY FIRST DRAFT OF THIS COMMENT SAID 0.7854 AND 14.6-30.6 mm.  0.7854 is the
# rev-8 COMMENT forty lines above ("the front arch top moves 0.7710 -> 0.7854")
# and it has been STALE SINCE REV 13, which re-derived the rake 33.0 -> 17.75
# mm/m and moved arch_z with it.  I quoted the comment instead of the value the
# build prints -- SPEC 10's own trap, reproduced inside the repair.  THE
# GEOMETRY IS UNAFFECTED: everything below calls arch_z(T.X_AXLE_F) live and
# never touches the literal.  The rev-8 comment is left where it is because it
# is a dated record of a rev-8 state; this note is what stops it being read as
# a current one.
#
# HIS TWO READINGS, rev 42, off `ref_workshop.jpg` -- the ONLY frame with the
# cab door SHUT.  Shown one 9x crop with three marks (the shut line; the height
# of the arch crown; the body's lower edge):
#   * "the door extends down to the side rocker it looks like"  -- his hedge is
#     kept, deliberately, because he wrote it;
#   * asked whether the door's rear lower corner sweeps UP AND OVER the front
#     wheel arch so that the arch's front lip is part of the door: YES.
#
# WHY THAT IS ADMISSIBLE HERE.  sec.10.62 and sec.10.73 establish that NO
# supplied frame carries both a closed cab door and an admissible px/m on the
# door plane, so no METRIC may be taken from that frame.  Nothing metric is.
# What was measured before he was asked is ORDINAL, and an ordinal fact needs
# no scale: the door's front shut line fits x = -0.03467 v + 512.233 over 49
# rows (ridge scores rising to 93) and runs CONTINUOUSLY from the belt down to
# the body's lower edge at v = 712, which is ~91 px BELOW the arch crown at
# v ~= 621.  The build put the door's bottom ABOVE the crown.  THE SIGN WAS
# WRONG, and a sign does not need a ruler.
#
# NOT ONE NEW CONSTANT IS INVENTED.  The new bottom is:
#   * the build's OWN arch circle -- centre (X_AXLE_F, arch_z(X_AXLE_F)),
#     radius ARCH_R, all locked and all guarded elsewhere;
#   * the build's OWN rocker -- `t1_core.ZB`, the under-body / sill bottom edge;
#   * a clearance G READ OFF THE REV-41 OUTLINE ITSELF: the minimum radial
#     distance rev 41's own smoothed DOOR_GAP_S kept from that circle.  So the
#     new outline is NOWHERE CLOSER to the arch than the outline that has been
#     passing T1_SUB=2 since rev 23.  That is asserted below, not claimed here
#     -- sec.10.45's rule, a claim in prose is not a guard.
#
# WHAT IS **NOT** CHANGED, AND IT IS NAMED RATHER THAN ABSORBED.  `DOOR_GAP`
# above is left BIT-IDENTICAL and keeps its second job: it is the ART DATUM.
# `folk_gen` parses it for DOOR_X0 / DOOR_X1 / DOOR_W and for `_DOOR_BOT_AUTH`,
# which `panel_bot(x)` returns inside the door span and which `door_pv` then
# normalises every v-coordinate of the door art over.
# CORRECTED rev 44: `DOOR_H` DIVIDES NOTHING and is NOT the v-map.  Its only
# two read sites, folk_gen.py:1274 and :1287, are both `h = sv * DOOR_H` and
# both MULTIPLY.  `door_pv` is the v-map and it is PROPORTIONAL, so re-pointing
# the parse STRETCHES the art instead of extending it.  probe_rev44_doorart.py.
# Re-pointing that parse at the wrapped outline would move DOOR_H by ~390 mm
# and force a re-bake of the flank textures -- a SECOND lever in the same
# revision, which is exactly what rev 25 refused to pull when it held
# `_DOOR_TOP_AUTH` at 1.8140 "so DOOR_H stays bit-identical and only one lever
# moves".  Same call, same reason.  THE ART FRAME IS THEREFORE STILL REV 41's
# AND THAT IS AN OPEN ITEM, not a solved one: the door is now ~390 mm deeper at
# its rear lower corner than the frame the art was baked into.  The three
# texture md5s are unchanged this revision BY CONSTRUCTION.
# ===========================================================================
_ARCH_CX = T.X_AXLE_F
_ARCH_CZ = arch_z(T.X_AXLE_F)
_ARCH_TOP_F = _ARCH_CZ + ARCH_R                 # kept: the crown, for messages


def _arch_radial(pt):
    """Signed clearance of a point OUTSIDE the front arch circle, in metres."""
    return math.hypot(pt[0] - _ARCH_CX, pt[1] - _ARCH_CZ) - ARCH_R


# rev 41's outline, smoothed exactly as rev 41 smoothed it, purely to read its
# own minimum clearance off it.  It is not used to cut anything.
_GAP41_S = _smooth(_resample(DOOR_GAP, 76), 2)
DOOR_ARCH_G = min(_arch_radial(p) for p in _GAP41_S)


def _door_bot_z(x, g):
    """The door's lower shut line at clearance `g`: the rocker, lifted over
    the arch."""
    z = T.ZB(x) + g
    dx = x - _ARCH_CX
    ra = ARCH_R + g
    if abs(dx) < ra:
        z = max(z, _ARCH_CZ + math.sqrt(ra * ra - dx * dx))
    return z


_DOOR_X_REAR = 0.9084 + DOOR_REAR_DX
_DOOR_X_FRONT = 1.8171
_NBOT = 61
_BOT_XS = [_DOOR_X_REAR + (_DOOR_X_FRONT - _DOOR_X_REAR) * i / (_NBOT - 1)
           for i in range(_NBOT)]
_NRES = 200


def _build_gap(g):
    run = [(x, _door_bot_z(x, g)) for x in _BOT_XS]
    cut = DOOR_GAP[:-3] + run
    return run, cut, _smooth(_resample(cut, _NRES), 2)


# THE RESAMPLE AND THE TWO SMOOTHING PASSES PULL AN ARC INWARD, and the guard
# below caught exactly that on the first run: built at DOOR_ARCH_G the smoothed
# outline came back at 0.0225 m against rev 41's 0.0244 m -- 1.9 mm CLOSER to
# the arch than what shipped.  The fix is not to relax the guard by 1.9 mm; it
# is to build the arc at whatever construction clearance makes the SMOOTHED
# outline land on DOOR_ARCH_G.  Solved here by fixed point, so it re-solves
# itself if _NRES, _NBOT or the smoothing ever change.  Converged value is
# printed by audit.py, never typed.
_G_BUILD = DOOR_ARCH_G
for _ in range(24):
    _r, _c, _sm = _build_gap(_G_BUILD)
    _err = DOOR_ARCH_G - min(_arch_radial(p) for p in _sm)
    if abs(_err) < 2e-5:
        break
    _G_BUILD += _err
DOOR_BOT_RUN, DOOR_GAP_CUT, DOOR_GAP_S = _build_gap(_G_BUILD)

# STRUCTURAL GUARD (SPEC sec.10.6), RE-SCOPED IN REV 42 WITH ITS NEW RATIONALE
# STATED -- rev 23's rule: DO NOT INHERIT A GUARD'S RATIONALE ALONG WITH ITS
# SHAPE.  The old guard required the outline to stay 10 mm ABOVE THE ARCH
# CROWN.  That shape was only ever a PROXY for the thing that actually
# collapsed the shell 205562 v -> 12 v at T1_SUB=2 for six revisions: the
# outline CROSSING THE ARCH LIP.  A door that wraps the arch violates the proxy
# while satisfying the invariant, so the guard is rewritten as the invariant it
# always meant -- a RADIAL clearance from the arch circle -- and it is armed at
# the clearance REV 41's OWN OUTLINE KEPT, so it can only be satisfied by being
# no worse than what shipped, never by a number chosen today.
_MIN_RAD = min(_arch_radial(p) for p in DOOR_GAP_S)
assert _MIN_RAD >= DOOR_ARCH_G - 5e-4, (
    "cab-door shut line is CLOSER to the front wheel arch than rev 41's was: "
    "min radial clearance %.4f m against rev 41's %.4f m. That is the "
    "condition that collapsed the boolean at T1_SUB=2 for six revisions."
    % (_MIN_RAD, DOOR_ARCH_G))
assert _MIN_RAD > 0.010, (
    "cab-door shut line within 10 mm of the front wheel arch lip (%.4f m)."
    % _MIN_RAD)
# and it must still not fall through the body's own lower edge
_MIN_SILL = min(z - T.ZB(x) for (x, z) in DOOR_GAP_S)
assert _MIN_SILL > 0.005, (
    "cab-door shut line reaches the body's lower edge: closest approach %.4f m"
    % _MIN_SILL)


def door_gaps():
    return [T.gap_prism((0, s * 0.64, 0), (1, 0, 0), (0, 0, 1), (0, s, 0),
                        DOOR_GAP_S, GAPW, 0.48, name=f"gap_door{s}")
            for s in (1, -1)]


# off-side cargo doors, (x, z); tail engine lid, (y, z).  Module level so
# verify.py can assert positively that the shut lines exist in the geometry.
def _seg_samples(pts, step=0.040):
    """Insert samples along any segment longer than `step`, closed outline.

    rev 23.  T.rrect(seg=6) emits 4*(seg+1) = 28 points and EVERY ONE of them
    is on a corner arc -- the four straight runs get only their two tangent
    endpoints.  SPEC sec.10.45 recorded that as "28 samples, all on the corner
    arcs = 5.2 % of the outline"; sec.10.61 sharpened it to "71.4 % of the
    samples are spent on 5.2 % of the length, leaving 94.8 % of the length with
    8 samples".  verify's shut-line row samples THIS list, so 94.8 % of the
    cargo door's shut line was never probed at all.

    This does not change the OUTLINE -- the inserted points are collinear with
    the segment they subdivide, so the cut geometry is identical.  It changes
    only how densely the guard can see it.  The no-op is asserted below.
    """
    out = []
    n = len(pts)
    for i in range(n):
        x0, z0 = pts[i]
        x1, z1 = pts[(i + 1) % n]
        out.append((x0, z0))
        d = math.hypot(x1 - x0, z1 - z0)
        if d > step:
            k = int(d // step)
            for j in range(1, k + 1):
                f = j / (k + 1.0)
                out.append((x0 + (x1 - x0) * f, z0 + (z1 - z0) * f))
    return out


_CARGO_RAW = [(u + 0.2000, v + 1.1380)
              for (u, v) in T.rrect(1.3600, 1.4100, 0.045, seg=6)]
CARGO_GAP = _seg_samples(_CARGO_RAW)
# The densification must be a pure no-op on the SHAPE.  Signed area is the
# statistic that would move if an inserted point were off the segment, so it is
# the one checked -- a control, not a comment (SPEC sec.10.50).
assert abs(T.signed_area(CARGO_GAP) - T.signed_area(_CARGO_RAW)) < 1e-9, (
    "CARGO_GAP densification changed the outline's area: %.12f vs %.12f"
    % (T.signed_area(CARGO_GAP), T.signed_area(_CARGO_RAW)))
ENGLID_CUT_DX = float(os.environ.get("T1_ENGLID_DX", "0.158"))
ENGLID_GAP = [(u, v + 0.8700)
              for (u, v) in T.rrect(0.9400, 0.5000, 0.055, seg=6)]


# =================================== SHUT LINE x APERTURE -- rev 23, SPEC 10.62
# THE INVARIANT, and it is NOT the one the arch assert above enforces.
#
# The arch assert exists for one stated reason: a shut line crossing an ARCH LIP
# collapsed the shell 205562 v -> 12 v at SUB=2.  That rationale does NOT
# transfer here and was deliberately not inherited -- all six crossings rev 22
# measured were live at SUB=2 with ZERO non-manifold edges, so they do not
# threaten the boolean at all.
#
# The rationale here is TOPOLOGICAL and needs no photograph, no scale and no
# datum: an aperture cut in a panel cannot extend past that panel's own
# boundary.  If it does, part of the hole is in the door and part is in the
# body, and the door cannot open.  That is true of any vehicle ever built, so
# it does not depend on which one this is -- which matters, because 87.7 % of
# rev 22's measured crossings were on the -Y flank, and SPEC's own source table
# grades that whole flank "E (never photographed)".
#
# WHAT THIS GUARD WILL AND WILL NOT ASSERT:
#   SHOW flank (+Y):  both members are photographed geometry, graded S/M.  The
#     invariant is asserted at ZERO.  rev 23 fixed the two crossings that were
#     live here (sec.10.62) rather than widening anything.
#   OFF flank (-Y):  the cargo doors AND the three off-side windows are BOTH
#     graded E and they contradict each other -- the windows are a mirror of the
#     show side (side_cutters loops s in (1,-1)) and the cargo door was placed
#     independently.  No photograph adjudicates: asked directly what the frame
#     shows through the near openings, the owner answered "cannot tell from this
#     crop".  So this half is a LABELLED REGRESSION CATCHER at a watched
#     baseline, exactly as rev 22 did for H_ROOF, and it is NOT evidence the
#     off flank is right.  DO NOT tighten it to zero by moving geometry nobody
#     has ever seen; the fix is a photograph, not a number.
OFF_CROSS_BASELINE = 0.8049       # m, WATCHED PRINT rev 23, both SUB levels
OFF_CROSS_BAND = 0.0100           # m.  Never widen -- see above.


def _pt_in_poly(pt, poly):
    x, z = pt
    n = len(poly)
    c = False
    j = n - 1
    for i in range(n):
        xi, zi = poly[i]
        xj, zj = poly[j]
        if ((zi > z) != (zj > z)) and \
           (x < (xj - xi) * (z - zi) / ((zj - zi) or 1e-30) + xi):
            c = not c
        j = i
    return c


def _arc_inside(line, poly, step=0.001):
    """Metres of the closed outline `line` lying strictly inside `poly`."""
    tot = 0.0
    n = len(line)
    for i in range(n):
        x0, z0 = line[i]
        x1, z1 = line[(i + 1) % n]
        seg = math.hypot(x1 - x0, z1 - z0)
        k = max(1, int(math.ceil(seg / step)))
        w = seg / k
        for t in range(k):
            f = t / k
            if _pt_in_poly((x0 + (x1 - x0) * f, z0 + (z1 - z0) * f), poly):
                tot += w
    return tot


def shutline_aperture_crossings():
    """Every shut line x aperture crossing, per flank, in metres.

    Returns a list of (line_name, aperture_name, side, arc_m, graded_E).
    ENGLID_GAP is in the (y, z) TAIL frame and shares no surface with a flank
    aperture, so it is NOT looped in -- doing so would manufacture crossings
    out of a coordinate mismatch.  It is reported separately by verify.
    """
    aps = [("door_main", DOOR_MAIN_S), ("door_vent", DOOR_VENT_S)]
    for i in range(len(BAYS)):
        cx, cz = bay_centre(i)
        aps.append(("bay%d" % i, [(u + cx, v + cz) for (u, v) in
                                  bay_outline(i)]))
    lines = [("gap_door+1", DOOR_GAP_S, +1), ("gap_door-1", DOOR_GAP_S, -1),
             ("gap_cargo", CARGO_GAP, -1)]
    out = []
    for lname, line, side in lines:
        for aname, poly in aps:
            L = _arc_inside(line, poly)
            if L > 1e-9:
                # graded E: anything on the flank no photograph covers.
                out.append((lname, aname, side, L, side != SHOW_SIDE))
    return out


# The SHOW-flank half is asserted at import, like the arch guard, so a change
# to a bay or to the door outline can never silently re-open it.  A control
# runs first: the test must be able to SEE a crossing, or a clean result below
# means nothing (SPEC sec.10.50 -- a verdict that cannot fail is not a test).
#
# NOTE ON THE NEGATIVE CONTROL, because the first one I wrote was WRONG and the
# failure was MINE, not the geometry's (SPEC sec.10.55's rule, second instance
# this revision).  The first draft asserted "an outline is not inside ITSELF".
# That is ill-posed: every sample then lies exactly ON the boundary, where a
# ray-crossing test is undefined and returns whatever the rounding decides.  It
# fired immediately.  The control below is a DISJOINT box instead, where the
# answer is unambiguous -- which is what a negative control has to be.
_ctrl_far = [(9.0, 9.0), (9.1, 9.0), (9.1, 9.1), (9.0, 9.1)]
assert _arc_inside(DOOR_GAP_S, _ctrl_far) == 0.0, \
    "crossing control: a disjoint box must contain 0.0 m of the outline"
_ctrl_box = [(0.6, 1.45), (1.4, 1.45), (1.4, 1.60), (0.6, 1.60)]
assert _arc_inside(DOOR_GAP_S, _ctrl_box) > 0.01, \
    "crossing control FAILED: the probe cannot see a crossing it is straddling"
_show_cross = [c for c in shutline_aperture_crossings() if c[2] == SHOW_SIDE]
assert not _show_cross, (
    "SHOW-flank aperture straddles a shut line: %s. Part of the hole is in the "
    "panel and part in the body, so the panel cannot open. Both members here "
    "are PHOTOGRAPHED geometry -- fix the outline, never this assert."
    % ", ".join("%s x %s = %.1f mm" % (c[0], c[1], c[3] * 1000)
                for c in _show_cross))


def cargo_door_gaps():
    """double side-loading doors, off side only"""
    obs = []
    pts = CARGO_GAP
    obs.append(T.gap_prism((0, -0.64, 0), (1, 0, 0), (0, 0, 1), (0, -1, 0),
                           pts, GAPW, 0.48, name="gap_cargo"))
    obs.append(T.solid_prism((0, -0.64, 0), (1, 0, 0), (0, 0, 1), (0, -1, 0),
                             T.rrect(GAPW * 1.3, 1.4100, 0.0012, seg=2),
                             0.48, name="gap_cargo_mid"))
    for v in obs[-1].data.vertices:
        v.co.x += 0.2000
        v.co.z += 1.1380
    obs[-1].data.update()
    return obs


def engine_lid_gap():
    # rev 16: was -1.95, i.e. 158 mm inboard of the old tail skin.
    return [T.gap_prism((T.X_TAIL + ENGLID_CUT_DX, 0, 0), (0, 1, 0),
                        (0, 0, 1), (-1, 0, 0), ENGLID_GAP, GAPW, 0.55,
                        name="gap_englid")]


# ------------------------------------------------------------- closed ragtop
RAG_X0, RAG_X1, RAG_HW = 1.4800, -1.5200, 0.5450


def roof_z(x, y):
    zt, rt, cr = T.ZT_ALL(x), T.RT_ALL(x), T.CR_ALL(x)
    Yt = max(T.WX(x) * T.G(zt - rt) - rt, 1e-3)
    return zt + cr * (1.0 - min(abs(y) / Yt, 1.0) ** 2)


def _rag_grid(hw, x0, x1, off, bows=True, nx=64, ny=18, name="rag"):
    verts, faces, uvs = [], [], []
    for iy in range(ny + 1):
        y = -hw + 2 * hw * iy / ny
        for ix in range(nx + 1):
            x = x0 + (x1 - x0) * ix / nx
            z = roof_z(x, y) + off
            if bows:
                for bx in (1.10, 0.44, -0.24, -0.92, -1.44):
                    z += 0.0075 * math.exp(-((x - bx) / 0.030) ** 2)
                z -= 0.0035 * (1 - (y / hw) ** 2) ** 2
            verts.append((x, y, z))
            uvs.append((ix / nx, iy / ny))
    for iy in range(ny):
        for ix in range(nx):
            a = iy * (nx + 1) + ix
            b = a + nx + 1
            faces.append((a, a + 1, b + 1, b))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.validate()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    T.fix_normals(ob)
    uvl = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        for li in poly.loop_indices:
            uvl.data[li].uv = uvs[me.loops[li].vertex_index]
    return ob


def ragtop():
    """RETIRED rev 8. Kept only so an old call site fails loudly, not silently."""
    raise RuntimeError(
        "t1_shell.ragtop() built a folding CANVAS ragtop with five Gaussian bow "
        "sticks and a sailcloth sag term, skinned 'canvas' and framed "
        "'chrome_dull'. SPEC sec.0.2 retired that reading in rev 4 -- the roof is "
        "CUT INTO RIGID HINGED STEEL LIDS -- and it shipped anyway for three "
        "revisions because verify.py only banned the retired materials someone "
        "remembered to list. Use roof_lids().")


# --------------------------------------------------------------- roof lids
# SPEC sec.1 + sec.0.2: the steel roof is CUT into rigid hinged lids. Donald's
# reference notes, settled off the high-resolution photographs: "the steel roof
# is CUT into rigid hinged lids that swing up as an awning/signboard, with a row
# of round bulbs along the free edge and flowers plus yellow menu strips painted
# on the underside. A second smaller lid sits behind the main one."
#
# Modelled OPEN (locked 2026-08-10). Both in-service photographs show the lids
# up; no photograph shows the vehicle closed. rev 7's "modelled CLOSED" was
# written while the roof was still believed to be canvas.
#
# Geometry, measured off ref_side.jpg at 211.5 px/m:
#   main lid   ~1.97 m fore-aft x ~1.11 m across, bottom edge on the roof line
#   rear lid   smaller, aft, lettered "LA SANTA..." (ref_rear34.jpg)
# The main lid hinges on a FORE-AFT axis at the off-side edge of the roof
# opening and swings up and over toward the show side, so its underside -- the
# flower mural with the yellow menu strips -- faces the counter. That is the one
# arrangement which reproduces all three photographs: broadside mural in
# ref_side.jpg, foreshortened mural top-right in ref_rear34.jpg, and the
# cut-out skin on a shallow perimeter rail in ref_workshop.jpg.
#
# RAG_X0 = +1.4800 is CONTRADICTED -- the cab roof dome is unbroken to X=+0.964.
LID_X0, LID_X1 = 0.9640, -1.0700       # main lid opening, fore-aft
LID_Y_HINGE = -0.5450                  # off-side edge of the opening
LID_W = 1.1100                         # across, hinge -> free edge
LID_OPEN_DEG = 104.0                   # past vertical, leaning over the counter
LID_T = 0.0180                         # skin + rail thickness
LID_PROUD = 0.0228                     # 26 +/- 7 mm measured proud height
RAIL_PROUD = 0.0213

SIGN_X0, SIGN_X1 = -1.1400, -1.7800    # the separate signboard -- NOT a lid
SIGN_OPEN_DEG = 82.0
LID2_X0, LID2_X1 = SIGN_X0, SIGN_X1    # back-compat aliases, do not use
LID2_OPEN_DEG = SIGN_OPEN_DEG


# ------------------------------------------------------------ roof aperture
# SPEC sec.10.28, settled WITH THE OWNER 2026-08-10 from marked crops of both
# in-service frames, before anything was measured from them:
#   * ONE opening only, under the flower-mural lid.  Solid roof forward of it
#     over the cab, and solid roof aft of it all the way to the tail.
#   * a strip of roof survives on BOTH sides -- roughly 0.3 m on the off side
#     where the lid hinges, roughly 0.3 m on the show side carrying the bulb
#     string along the drip rail.  The 1.11 m transverse width stands.
#
# Why this had to be ASKED rather than measured: ref_side.jpg puts the camera
# at roof height, so the roof plane is edge-on and the surviving strip between
# the lid's base and the near drip rail is ~13 px tall -- no transverse number
# taken off that frame is worth anything.  ref_rear34.jpg is the only frame
# with any elevation on the roof; it shows maroon interior through the opening,
# which is the first direct sight of the inside of the hole in any frame, but
# it shows neither end of it.
#
# The opening IS the main lid's own footprint -- the lid is the piece of skin
# that was cut out of it -- so it is expressed in terms of LID_X0 / LID_X1 /
# LID_Y_HINGE / LID_W and NOT as four fresh constants.  SPEC sec.10.25: a
# constant tuned against another constant must be expressed IN TERMS of it, or
# correcting one silently breaks the other.  Moving the lid moves the hole.
ROOF_CUT_R = 0.030                     # corner radius of the cut-out


def roof_cutters():
    """The single roof aperture the main lid was cut from.

    A rectangle in PLAN, extruded straight down through the roof skin -- which
    is what a cut-out in a curved roof is.  Issued from build.py step 3, i.e.
    AFTER solidify and in the UN-DROPPED frame, like every other aperture.
    Only the wheel arches are cut while the shell is still a closed solid, and
    that pipeline order is load-bearing (SPEC sec.10.1).

    Until rev 11, build.py issued NO roof cutter at all: the lids floated over
    an unbroken roof skin, so the galley was a sealed 2.8 mm steel box that no
    exterior source could physically reach.  That is why the black serving bays
    survived six revisions of light tuning -- the light had nowhere to enter.
    """
    x0, x1 = min(LID_X0, LID_X1), max(LID_X0, LID_X1)
    y0, y1 = LID_Y_HINGE, LID_Y_HINGE + LID_W
    cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    pts = T.rrect(x1 - x0, y1 - y0, ROOF_CUT_R, seg=6)

    # span the crown over the WHOLE opening, then clear it top and bottom. The
    # roof is doubly curved, so one station's z is not enough.
    zs = [roof_z(x0 + (x1 - x0) * i / 24.0, y0 + (y1 - y0) * j / 12.0)
          for i in range(25) for j in range(13)]
    zlo, zhi = min(zs) - 0.030, max(zs) + 0.060

    # the prism must not reach down into the window band; if it ever did, the
    # roof cutter would take the header rail with it.
    assert zlo > Z_HEAD + 0.020, (
        "roof cutter bottom z=%.4f is within 20 mm of the window head %.4f -- "
        "it would cut the header rail, not the roof" % (zlo, Z_HEAD))

    # rev 16 BUG FIX, exposed by the re-fitted crown.  T.solid_prism extrudes
    # +-depth/2 about its ORIGIN (t1_core._frame), so passing `zlo` as the
    # origin put the prism's top at zlo + (zhi-zlo)/2, i.e. only halfway up the
    # span it was computed to cover.  At the old CR_ALL = 0.032 the crown was
    # so shallow that the prism still cleared the roof by 6 mm and the cut
    # worked by luck; at CR_ALL = 0.1179 it stops 18 mm short and the aperture
    # centre goes back to being sealed steel -- caught by verify 11d2, which is
    # exactly the failure that guard was written for.
    return [T.solid_prism((cx, cy, (zlo + zhi) / 2.0),
                          (1, 0, 0), (0, 1, 0), (0, 0, 1),
                          pts, zhi - zlo, name="cut_roof")]


def _lid_panel(x0, x1, w, name, seams=3):
    """A rigid, flat, rectangular lid panel in the hinge frame.

    Built flat in the XY plane with +Y running hinge -> free edge, then rotated
    about the hinge by the caller. Rigid: NO bow sticks and NO sag term -- those
    were the canvas artefacts. Pressed seams run fore-aft, matching the roof
    skin ribs visible in ref_workshop.jpg.
    """
    nx, ny = 40, 22
    verts, faces, uvs = [], [], []
    for iy in range(ny + 1):
        yv = w * iy / ny
        for ix in range(nx + 1):
            xv = x0 + (x1 - x0) * ix / nx
            z = 0.0
            for k in range(1, seams + 1):
                yc = w * k / (seams + 1)
                z -= 0.0028 * math.exp(-((yv - yc) / 0.022) ** 2)
            verts.append((xv, yv, z))
            uvs.append((ix / nx, iy / ny))
    for iy in range(ny):
        for ix in range(nx):
            a = iy * (nx + 1) + ix
            b = a + nx + 1
            faces.append((a, a + 1, b + 1, b))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.validate()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    uvl = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        for li in poly.loop_indices:
            uvl.data[li].uv = uvs[me.loops[li].vertex_index]
    m = ob.modifiers.new("sol", 'SOLIDIFY')
    m.thickness = LID_T
    m.offset = -1.0
    m.use_even_offset = True
    T.apply_mods(ob)
    T.fix_normals(ob)
    return ob


def _hinge(ob, x_unused, y_hinge, z_hinge, deg):
    """Rotate a lid about its fore-aft hinge axis, in place, into world space."""
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    for v in ob.data.vertices:
        y, z = v.co.y, v.co.z
        v.co.y = y_hinge + (y * ca - z * sa)
        v.co.z = z_hinge + (y * sa + z * ca)
    ob.data.update()
    T.fix_normals(ob)


def _lid_face(x0, x1, w, name, inset=0.030, off=0.0):
    """A flat single-quad-grid panel in the hinge frame, for the mural decal."""
    nx, ny = 2, 2
    verts, faces, uvs = [], [], []
    for iy in range(ny + 1):
        yv = inset + (w - 2 * inset) * iy / ny
        for ix in range(nx + 1):
            xv = (x0 - inset) + ((x1 + inset) - (x0 - inset)) * ix / nx
            verts.append((xv, yv, off))
            uvs.append((ix / nx, iy / ny))
    for iy in range(ny):
        for ix in range(nx):
            a = iy * (nx + 1) + ix
            b = a + nx + 1
            faces.append((a, a + 1, b + 1, b))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.validate()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    uvl = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        for li in poly.loop_indices:
            uvl.data[li].uv = uvs[me.loops[li].vertex_index]
    T.fix_normals(ob)
    return ob


def roof_lids():
    """The ONE cut roof lid, OPEN. Returns (skins, rails, struts, boards).

    rev 12: was two lids. The second panel is a separate signboard, not a lid
    (SPEC sec.10.28, owner's reading) -- see signboard(). One lid, one opening.
    """
    skins, rails, struts, boards = [], [], [], []

    # ---- main lid
    zh = roof_z((LID_X0 + LID_X1) / 2, LID_Y_HINGE) + LID_PROUD
    main = _lid_panel(LID_X0, LID_X1, LID_W, "lid_main")
    _hinge(main, 0.0, LID_Y_HINGE, zh, LID_OPEN_DEG)
    skins.append(main)

    # the flower mural + yellow menu strips, on the lid's UNDERSIDE -- which,
    # with the lid swung over, is the face presented to the counter. This is the
    # single most recognisable thing about the vehicle.
    # off is NEGATIVE: the mural is on the lid's UNDERSIDE. With the lid swung
    # to 104 deg the underside normal maps to +Y, i.e. it faces the show side and
    # the counter, which is the whole point of the board. At +0.0016 it sat on
    # the outer skin and faced the off side -- the first probe rendered two blank
    # grey slabs.
    # rev 11: off was -0.0016 and that is 1.6 mm INSIDE the skin, not on its
    # underside.  _lid_panel solidifies with offset = -1.0, so the skin occupies
    # z in [-LID_T, 0]; a board at -0.0016 sits just under the UPPER face, and
    # _lid_panel's pressed seams dip to -0.0028 and poke through the decal
    # plane.  The underside is at -LID_T.
    b = _lid_face(LID_X0, LID_X1, LID_W, "lid_board", off=-(LID_T + 0.0016))
    _hinge(b, 0.0, LID_Y_HINGE, zh, LID_OPEN_DEG)
    boards.append(b)

    # perimeter rail: the shallow frame the skin sits on, standing PROUD of the
    # roof by the measured 26 +/- 7 mm. ref_workshop.jpg shows the open lid is
    # the cut-out roof skin on a rail, not a box.
    for (xa, xb) in ((LID_X0, LID_X0), (LID_X1, LID_X1)):
        r = _rag_grid(RAG_HW, xa, xb, RAIL_PROUD, bows=False, nx=1, ny=18,
                      name="lid_rail")
        rails.append(r)

    # ---- prop struts, hinge side to free edge.  TWO, one near each END of the
    # lid, inset 160 mm.
    #
    # OWNER READING, rev 37, off `rev37_hero34f.png`, verbatim: "we there are
    # two bars propping up the art sign on either side, not one".  A COUNT --
    # the cheapest class of observation there is, needing no scale, no px/m and
    # no camera model.  Until rev 38 this loop ran over a ONE-ELEMENT tuple and
    # built `lid_strut0` alone.
    #
    # NOTE FOR ANY LATER CONTEXT: `NEXT_CONTEXT_PROMPT_rev38.md` sec.6 item 1
    # attributed this to `t1_shell.signboard()`'s single `sign_strut`.  That is
    # the WRONG OBJECT: signboard() is gated behind T1_SIGNBOARD=1, is not the
    # default, and SPEC forbids rendering a hero with it on -- so no
    # `sign_strut` exists in any shipped frame.  The strut he can see is
    # `lid_strut0`, from here.  The report was right; the attribution was not.
    # x is symmetric about the lid's own ends: LID_X1 + 0.16 and LID_X0 - 0.16.
    for (ob, xs, deg, w) in ((main, LID_X1 + 0.16, LID_OPEN_DEG, LID_W),
                             (main, LID_X0 - 0.16, LID_OPEN_DEG, LID_W)):
        a = math.radians(deg)
        tipy = LID_Y_HINGE + w * math.cos(a) * 0.86
        tipz = (roof_z(xs, LID_Y_HINGE) + LID_PROUD) + w * math.sin(a) * 0.86
        foot = Vector((xs, 0.44, roof_z(xs, 0.44)))
        tip = Vector((xs, tipy, tipz))
        d = tip - foot
        struts.append(T.cylinder(tuple((foot + tip) / 2), tuple(d.normalized()),
                                 0.0075, d.length, seg=14,
                                 name=f"lid_strut{len(struts)}"))
    return skins, rails, struts, boards


def signboard():
    """The separate cream signboard, lettered in red brush script with a red star.

    OWNER READING, 2026-08-10, SPEC sec.10.28.  Shown a 3x crop of this panel in
    ref_rear34.jpg and asked what it is, Donald answered: **a separate
    signboard, not a cut roof lid.**

    That is a topology change, not a dressing change.  Up to rev 11 this panel
    was `lid_rear` -- a second hinged LID, which implies a second opening under
    it.  It is not a lid, so there is no opening under it, and roof_cutters()
    issues exactly one cutter.  Donald's answer to the same question set says
    the roof is solid forward of the main opening and solid aft of it to the
    tail, which is consistent: a signboard stands on solid roof.

    RETIRED 2026-08-10 BY THE OWNER, and this is the second correction to the
    same panel in one session -- both from him, both after being shown a crop.

    Asked where it stands, he answered: "I think it is something separate from
    our render focus", and then, unprompted, corrected his own earlier reading:
    **"I was wrong, I think it is a detached sign."**

    So it is not a roof lid, and it is not on the vehicle at all.  It is a
    detached sign that happens to fall behind the combi in ref_rear34.jpg.  The
    build emits NOTHING here by default.

    What this retires, in order:
      rev 8-9   `lid_rear`, a second hinged LID, which implied a second roof
                opening that build.py never cut.
      rev 12a   a roof-mounted SIGNBOARD, which implied solid roof carrying it.
      rev 12b   nothing.  It is not part of this vehicle.

    That is also why it was never visible in ref_side.jpg -- not "folded flat",
    which is what I had reasoned; simply not there.  A large blank white slab
    standing over the tail in every broadside render was the visible symptom,
    and it has no counterpart anywhere in ref_side.jpg.

    The geometry is kept, gated, rather than deleted: the panel and its measured
    proportions cost real work and the owner has now changed his reading of this
    one panel three times.  T1_SIGNBOARD=1 restores it.  It is deliberately NOT
    the default, and no hero should be rendered with it on.
    """
    if not int(os.environ.get("T1_SIGNBOARD", "0")):
        return [], [], []
    skins, boards, struts = [], [], []
    w = LID_W * 0.86
    zh = roof_z((SIGN_X0 + SIGN_X1) / 2, LID_Y_HINGE) + LID_PROUD

    panel = _lid_panel(SIGN_X0, SIGN_X1, w, "sign_panel")
    _hinge(panel, 0.0, LID_Y_HINGE, zh, SIGN_OPEN_DEG)
    skins.append(panel)

    face = _lid_face(SIGN_X0, SIGN_X1, w, "sign_face", off=-(LID_T + 0.0016))
    _hinge(face, 0.0, LID_Y_HINGE, zh, SIGN_OPEN_DEG)
    boards.append(face)

    xs = SIGN_X1 + 0.12
    a = math.radians(SIGN_OPEN_DEG)
    tipy = LID_Y_HINGE + w * math.cos(a) * 0.86
    tipz = (roof_z(xs, LID_Y_HINGE) + LID_PROUD) + w * math.sin(a) * 0.86
    foot = Vector((xs, 0.44, roof_z(xs, 0.44)))
    tip = Vector((xs, tipy, tipz))
    d = tip - foot
    struts.append(T.cylinder(tuple((foot + tip) / 2), tuple(d.normalized()),
                             0.0075, d.length, seg=14, name="sign_strut"))
    return skins, boards, struts


# ------------------------------------------------------- nose bulge + V swage
# The PRESSED swage, UN-DROPPED.  These MUST mirror t1_mats.V_APEX / V_RISE /
# V_POW, which drive the PAINTED break and are in the DROPPED (above-ground)
# frame, offset by T.RIDE_DROP.  verify.py asserts the registration; if the
# two drift apart the pressed crease and the two-tone line separate by the
# difference, which is exactly the 65 mm mistake this frame invites.
V_APEX_Z = 0.4050        # t1_mats.V_APEX 0.340 above ground + RIDE_DROP 0.065
V_RISE_Z = 0.8670        # == t1_mats.V_RISE
V_POW_Z = 0.60           # == t1_mats.V_POW.  < 1: the profile is CONCAVE.
V_HALF_W = 0.86


def zV(y):
    """height of the two-tone V at half-width y, UN-DROPPED"""
    return V_APEX_Z + V_RISE_Z * (min(abs(y), V_HALF_W) / V_HALF_W) ** V_POW_Z


def nose_shape(ob):
    me = ob.data
    bm = bmesh.new(); bm.from_mesh(me)
    bm.normal_update()

    for v in bm.verts:
        x, y, z = v.co
        if x < 1.86:
            continue
        w = min(1.0, max(0.0, (x - 1.86) / 0.17))
        w = w * w * (3 - 2 * w)
        r = ((y / 0.80) ** 2 + ((z - 1.00) / 0.46) ** 2)
        bulge = 0.019 * w * max(0.0, 1.0 - r)
        d = z - zV(y)
        s = 0.5 * (1.0 + math.tanh(d / 0.016))
        step = -0.0062 * w * (1.0 - s)
        v.co = Vector((x + bulge, y, z)) + v.normal * step
    bm.to_mesh(me); bm.free()
    me.update()
