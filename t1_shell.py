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


def headlamp_recess_cutters(hl_x, hl_y, hl_z, r_lens=0.0862):
    """rev 45 SPIKE, SPEC 10.115 -- the pressed bowl each headlamp sits in.

    FINDING 41.  There is no headlamp aperture in the nose at all.  The lamp
    assembly is fitted into unbroken sheet metal: raycast down the near lamp's
    own axis and the ray hits T1_body at 2.1116 and 2.1088 BEFORE it reaches
    hl_lens.  The reflector is therefore invisible and the lens is backed by
    body paint.

    A 1963 T1's headlamp does NOT sit in a plain hole.  The nose panel is
    DRAWN BACK into a shallow bowl and the lamp sits in it, chrome rim on the
    outer face.  Both frames show it as a shadowed ring round the bezel --
    ref_nolita_front34.jpg and ref_playa_34.png -- and that shadow is most of
    what makes a lamp read as set INTO a panel rather than stuck ON it.

    WHAT THIS ACTUALLY BUILDS, AND A DOCSTRING THAT LIED FOR ONE HOUR.
    The first draft of this comment said "a truncated cone, not a cylinder:
    mouth at the lens radius, throat at 0.62 of it".  `T.solid_prism` extrudes
    ONE outline at CONSTANT section -- it cannot make a cone -- so the code
    built a straight-sided bore while the prose claimed a taper.  That is the
    same defect class this revision found twice already (`headlamp`'s "chrome
    ring" against build.py's "brass", and `roof_lids`' "inset 160 mm" against
    an expression that reads as an outset).  Corrected here rather than in a
    later revision: THIS IS A STRAIGHT-SIDED BORE, 52 mm deep, at the lens
    radius.

    THE DEPTH AND THE SECTION ARE AUTHORED, NOT MEASURED.  No frame we hold
    resolves the bowl's section -- it is inside the bezel in every one of them.
    They are declared here, in one place, so a later measurement replaces two
    numbers and nothing else.  `PHOTOS_WANTED_rev45.md` asks for the frame.

    THE CUT IS COUPLED TO THE REFLECTOR AND THAT IS WORTH KNOWING BEFORE YOU
    TOUCH EITHER.  Before the cut the lens was backed by sheet metal, which is
    why it read as a mid-grey disc -- accidentally close to the photograph for
    the wrong reason.  Cutting the bore exposes `hl_bowl`, a metal=1.0 mirror,
    and a mirror in an unlit cavity returns the cavity.  Measured through
    `probe_rev45_nose`'s projected landmark, at the SHIPPED reflector settings:

        lens / cream         0.423  no bore  ->  0.549  bored   (photo 0.565)
        lens (R-B) / cream  +0.069  no bore  -> +0.027  bored   (photo -0.024)

    Both move toward the photograph, and the eye agrees once the render is big
    enough: bored, the aperture has a highlight, a bright arc and depth; unbored
    it is a flat dull disc.  RECORDED BECAUSE THE FIRST EYEBALL READ OF THIS
    SPIKE WAS THE OPPOSITE, taken off a 48-sample T1_SUB=1 crop, and the A/B at
    64 samples overturned it.  Rule 10 cuts both ways: a detail you cannot see
    is not a detail, and a detail you looked at badly is not looked at.

    T1_HL_BOWL=0 skips the cut and restores the un-bored arm.
    """
    obs = []
    for s in (1, -1):
        prof = []
        n = 28
        for i in range(n):                       # mouth ring, at the skin
            a = T.TAU * i / n
            prof.append((r_lens * math.cos(a), r_lens * math.sin(a)))
        mouth = T.solid_prism((hl_x + 0.010, s * hl_y, hl_z),
                              (0, s, 0), (0, 0, 1), (-1, 0, 0),
                              prof, 0.052, name=f"cut_hlbowl{s}")
        obs.append(mouth)
    return obs


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
# rev 44 -- SPEC 10.100 IS RETRACTED.  THE CAB DOOR'S BOTTOM IS A FLAT CHORD
# ABOVE THE FRONT WHEEL ARCH, NOT A WRAP AROUND IT.  SPEC 10.101.
#
# WHAT REV 42 DID.  His defect report 5 -- "the doors extend lower, around the
# wheel well" -- was turned into a construction: the door's bottom run became
# `max(ZB(x)+G, arch circle offset radially by G)`, so the door swept up and
# over the front arch and reached the rocker at both ends.  It rested on ONE
# piece of evidence: a yes/no question put to the owner over a 9x crop of
# `ref_workshop.jpg` -- "does the door's rear lower corner sweep up and over
# the front wheel arch?" -- answered YES.  That is a LEADING question answered
# off a three-quarter frame that SPEC 10.62 and 10.73 had already ruled
# inadmissible for any metric on the door plane.
#
# WHAT REFUTES IT, AND IT WAS IN THE REPO THE WHOLE TIME.  `ref_nolita_doorshut
# .jpg` is the one frame that carries the cab door's WHOLE outline, square-on,
# shut.  Three measurements off it, all by gradient, none by eye:
#
#   * THE DOOR'S BOTTOM SHUT LINE IS FLAT.  Row-gradient over the door's rear
#     half (cols 70-122) puts a 2 px dark line at ROW 239-240 and nowhere else,
#     and a column-by-column darkest-row scan holds it at row 239 continuously
#     from col 60 to col 122.  A wrap would descend ~135 mm (12 px) across that
#     span.  It does not move one pixel.
#
#   * THE REAR SHUT LINE STOPS ON IT.  Column-gradient in 8-row bands puts the
#     door's rear vertical shut line at col 124.5 (|dL| 24-37 against a floor
#     of 1-2) for rows 208 through 240, and it VANISHES below row 240 (|dL|
#     drops to 0.4-2.2, i.e. into the noise).  Under rev 42's wrap that line
#     would have to continue another 38 px down to the rocker.  It does not
#     exist there.
#
#   * THE CLEARANCE IS REV 41'S.  The wheel-well's dark top edge sits at row
#     241.5 at cols 85-94 (the crown).  Door line 239, arch lip 241.5: 2.5 px.
#     Scale from the arch's own half-width -- hub centroid col 91.0, rear foot
#     col 123 -- is 32 px = ARCH_R 0.3735 m = 85.7 px/m, so 2.5 px = 29 mm.
#     REV 41 SHIPPED 23.0-39.0 mm.  The frame lands in the middle of the band
#     that shipped, and it is scale-free in the sense that matters: the ratio
#     (door-line-to-lip) / (arch half-width) is 0.078 measured against 0.065
#     built, both read off the same two features in the same image.
#
# WHY THE OWNER'S rev-44 REPORT SAYS THE OPPOSITE OF WHAT IT LOOKS LIKE.  He
# wrote "the door does not continue on the other side of the wheel well" and
# then "the door does not continue downward behind the wheel".  Read against
# rev 42's geometry both sentences are the SAME complaint: the wrap made the
# bottom run CONCENTRIC with the arch -- offset radially by a constant G, so it
# could never diverge from it -- and a curve that never diverges from another
# reads as one thick line.  The door's bottom stopped being a line that crosses
# the wheel well and became part of the arch lip.  Measured on the 3200 px side
# render: the two ran 14.0-22.4 px apart with a spread of 8.3 px over 600 mm.
# And the rear shut line, which under the wrap ends on the arc at z 0.5385 --
# 135 mm BELOW the arch crown and 127 mm ABOVE the rocker -- terminates in mid
# panel beside the wheel, which is neither where rev 41 put it nor where the
# Nolita frame puts it.
#
# I ALSO TRIED TO FIX IT INSIDE THE WRAP, AND THE ATTEMPT IS WHAT PROVED THE
# WRAP WRONG.  Flattening the run to the arc's own crown height passed the
# clearance guard and reproduced rev 41's chord to 1 mm (0.8014 against
# 0.800-0.816) -- but it silently deleted SPEC 10.100.4's rear corner dip,
# because the arc's span reaches x = 0.9021 and the door's rear edge is at
# 0.9257, INSIDE it.  Chasing that exposed the real constraint: the arch's
# rear-most point is x = 1.3 - 0.3735 = 0.9265 and the door's rear edge is
# 0.92565, so the two coincide to 0.85 mm.  There is NO ROOM for a shut line to
# descend behind that wheel at any clearance, and every construction that tried
# either produced a 23 mm-wide 400 mm-deep tab or drove the arch clearance from
# 24.4 mm to 1.7 mm -- the exact geometry SPEC 10.1 records as collapsing the
# shell 205562 v -> 12 v.  A construction that cannot be built at any clearance
# is usually a construction that is not there, and it is not: the Nolita frame
# shows the rear shut line stopping at row 240 for the same reason.
#
# WHAT IS RESTORED.  `DOOR_GAP` -- rev 41's table, which has been sitting here
# bit-identical this whole time because rev 42 kept it as the ART DATUM.  It is
# now the cut outline again, resampled at 76 and smoothed twice, which is what
# rev 41 did, so `DOOR_GAP_S` is bit-identical to the outline that passed
# T1_SUB=2 from rev 23 to rev 41.  `_GAP41_S` and `DOOR_GAP_S` are therefore
# THE SAME LIST and that is asserted below rather than claimed here (10.45).
#
# WHAT THIS CLOSES.  Ledger finding 1 -- "the art frame: the door is 272.2 mm /
# 387.5 mm deeper than the art's outline".  It was deeper because rev 42 made
# it deeper.  The art datum and the cut outline are one table again, so the
# lobes the art would have had to grow into do not exist and there is nothing
# to draw.  `probe_rev44_doorart.py`'s C3 and C4 reproduce SPEC 10.100.4's
# published depths and crown height; they are EXPECTED TO FAIL from this
# revision and that is what a retraction looks like from the instrument side.
#
# THE GUARDS ARE KEPT, ALL THREE, and re-armed against the restored outline.
# They were written in rev 42 for the wrap, but rev 23's rule cuts both ways:
# a guard's SHAPE outlives the change that motivated it when the invariant it
# encodes is still the invariant.  Radial clearance from the arch circle is
# still what the boolean cares about; it is simply satisfied with room to
# spare now instead of exactly.
# ===========================================================================
_ARCH_CX = T.X_AXLE_F
_ARCH_CZ = arch_z(T.X_AXLE_F)
_ARCH_TOP_F = _ARCH_CZ + ARCH_R                 # kept: the crown, for messages


def _arch_radial(pt):
    """Signed clearance of a point OUTSIDE the front arch circle, in metres."""
    return math.hypot(pt[0] - _ARCH_CX, pt[1] - _ARCH_CZ) - ARCH_R


# ===========================================================================
# rev 44b -- THE FORWARD LOWER LOBE.  SPEC 10.106.  HE WAS RIGHT AGAIN.
#
# *[verbatim]* "the door curves around the FRONT of the wheel well and not the
# back.  So you removed too much door."
#
# HE IS RIGHT, AND SO IS THE FRAME.  10.102 retracted 10.100's wrap because
# `ref_nolita_doorshut.jpg` holds the bottom rail flat and stops the rear shut
# line on it.  That reading was correct -- FOR THE PART OF THE DOOR IT
# COVERED.  It was taken over cols 60-122, which is the arch and everything
# aft of it, and I then asserted flatness over the WHOLE door.  Forward of
# col 56 the same scan had already printed no line at all in that row band,
# and I read that as noise instead of as the line having gone somewhere else.
# IT HAD.  Extending the trace forward finds it 26 px lower.
#
# THE MEASUREMENT, sub-pixel, three-point parabolic on the row gradient:
#   bottom rail, over the arch (cols 70-118)      row 238.58
#   arch lip crown           (cols 70-118)        row 241.46
#   FORWARD LOWER LOBE       (cols 30-48)         row 264.58
#   body's lower edge        (cols 30-48)         row 273.50
#
# EVERY CONSTANT BELOW IS DIMENSIONLESS, so none of it depends on px/m -- and
# that matters here, because the three available scales (arch radius 105.9,
# rear rim OD 104.2, hub-to-hub wheelbase 107.4 px/m) span 3 %.
#
#   DROP   = (264.58 - 238.58) / (273.50 - 238.58) = 0.7443 of the rail's own
#            height above the body's lower edge.  Anchored to two features of
#            THE DOOR ITSELF, so it is immune to the scale question entirely.
#   RAMP   = the step's two feet, in units of the arch's own radius forward of
#            the axle: (91.1 - 56)/39.54 = 0.8877 and (91.1 - 46)/39.54 =
#            1.1406.  The ramp therefore STRADDLES THE ARCH'S FORWARD LIP,
#            which is where a door that clears a wheel would put it.
#
# AND THE RAIL ABOVE THE ARCH IS UNTOUCHED -- 2.88 px = 27 mm above the lip,
# against rev 41's shipped 23-39 mm.  10.102's finding stands where it was
# measured; this adds the part of the door it never looked at.
#
# THE ART DATUM DOES NOT MOVE.  `DOOR_GAP` stays bit-identical and keeps its
# second job (10.100.6's one good idea).  The lobe goes into the CUT outline
# only.  Nothing needs to be drawn into it: the flank's folk art is continuous
# across this panel gap in every frame we hold, so the shut line crosses the
# art rather than bounding it.
# ===========================================================================
_NRES = 76                                      # rev 41's, restored with it

DOOR_LOBE_DROP = (264.58 - 238.58) / (273.50 - 238.58)      # 0.7443
DOOR_LOBE_A = (91.1 - 56.0) / 39.54                         # 0.8877 * ARCH_R
DOOR_LOBE_B = (91.1 - 46.0) / 39.54                         # 1.1406 * ARCH_R


def _rail_z(x):
    """DOOR_GAP's own bottom rail at x, by linear interpolation."""
    rail = sorted(DOOR_GAP[-4:] + DOOR_GAP[:1])
    for i in range(len(rail) - 1):
        (xa, za), (xb, zb) = rail[i], rail[i + 1]
        if xa <= x <= xb:
            return za + (zb - za) * (x - xa) / (xb - xa)
    return rail[-1][1] if x > rail[-1][0] else rail[0][1]


_LOBE_XA = T.X_AXLE_F + DOOR_LOBE_A * ARCH_R
_LOBE_XB = T.X_AXLE_F + DOOR_LOBE_B * ARCH_R
_DOOR_X_FRONT = 1.8171
_Z_LOBE = _rail_z(_DOOR_X_FRONT) - DOOR_LOBE_DROP * (
    _rail_z(_DOOR_X_FRONT) - T.ZB(_DOOR_X_FRONT))

# The cut outline: rev 41's table with its bottom rail carried on past the
# arch's forward lip and down.  Built by SPLICING rather than by re-typing the
# table, so the two can never disagree about the seventeen points they share.
DOOR_GAP_CUT = (list(DOOR_GAP[:-3])
                + [p for p in DOOR_GAP[-3:] if p[0] < _LOBE_XA]
                + [(_LOBE_XA, _rail_z(_LOBE_XA)),
                   (_LOBE_XB, _Z_LOBE),
                   (_DOOR_X_FRONT, _Z_LOBE)])
DOOR_GAP_S = _smooth(_resample(DOOR_GAP_CUT, _NRES), 2)

# rev 41's outline smoothed exactly as rev 41 smoothed it -- the object 10.100
# built purely to READ a clearance off.  It is the reference the guard below
# is armed at, and the lobe must be no worse than it.
_GAP41_S = _smooth(_resample(DOOR_GAP, 76), 2)
DOOR_ARCH_G = min(_arch_radial(p) for p in _GAP41_S)

# The bottom run, kept as a name because probe_rev44_doorart.py and the ledger
# both address it: the rail plus the ramp plus the lobe, in x order.
_DOOR_X_REAR = 0.9084 + DOOR_REAR_DX
DOOR_BOT_RUN = sorted(p for p in DOOR_GAP_CUT if p[1] < 0.90)
assert (abs(DOOR_BOT_RUN[0][0] - _DOOR_X_REAR) < 1e-9
        and abs(DOOR_BOT_RUN[-1][0] - _DOOR_X_FRONT) < 1e-9), (
    "the bottom-run slice no longer starts and ends on the door's own two "
    "lower corners: %r" % (DOOR_BOT_RUN,))

# STRUCTURAL GUARD (SPEC sec.10.6), RE-SCOPED IN REV 42 WITH ITS NEW RATIONALE
# STATED -- rev 23's rule: DO NOT INHERIT A GUARD'S RATIONALE ALONG WITH ITS
# SHAPE.  The old guard required the outline to stay 10 mm ABOVE THE ARCH
# CROWN.  That shape was only ever a PROXY for the thing that actually
# collapsed the shell 205562 v -> 12 v at T1_SUB=2 for six revisions: the
# outline CROSSING THE ARCH LIP.  The proxy and the invariant agree again now
# that the wrap is gone, but the invariant is the one worth asserting, so the
# rev-42 form is KEPT rather than reverted with the geometry.
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
# rev 44 -- THE RAIL MUST NOT WRAP AGAIN BY ACCIDENT.
#
# RE-SCOPED IN REV 44b AND ITS RATIONALE RE-STATED (rev 23's rule).  Written
# in 10.102 as "the bottom run is FLAT across the whole door", which is what
# the frame appeared to say.  It said no such thing: it was measured over
# cols 60-122 -- the arch and everything AFT of it -- and 10.106 found the rail
# 26 px lower forward of the arch's lip.  The guard is therefore armed over
# EXACTLY THE SPAN THAT WAS MEASURED, and it is now a stronger test rather
# than a weaker one, because the span is stated instead of assumed.
#
# It still kills a re-introduced wrap: 10.100's arc descends 388 mm inside
# this span, where the measurement says 0 px of descent over 62 px of door.
_RAIL_SPAN = [p for p in DOOR_BOT_RUN if p[0] <= _LOBE_XA + 1e-9]
_BOT_SPREAD = max(p[1] for p in _RAIL_SPAN) - min(p[1] for p in _RAIL_SPAN)
assert _BOT_SPREAD < 0.030, (
    "cab-door bottom rail is not flat OVER THE ARCH: %.1f mm of descent from "
    "x %.4f to the arch's forward lip. ref_nolita_doorshut.jpg holds it flat "
    "to 1 px there (SPEC 10.106)."
    % (_BOT_SPREAD * 1000.0, _RAIL_SPAN[0][0]))

# rev 44b -- AND THE FORWARD LOBE MUST NOT SILENTLY VANISH AGAIN.  This is the
# guard 10.102 should have had: it deleted a feature that a photograph holds,
# and nothing objected.  Armed on the DIMENSIONLESS measurement, so it tests
# the thing that was measured rather than a metre value derived from a px/m
# the sources disagree about by 3 %.
_LOBE_DROP_BUILT = ((_rail_z(_DOOR_X_FRONT) - _Z_LOBE)
                    / (_rail_z(_DOOR_X_FRONT) - T.ZB(_DOOR_X_FRONT)))
assert abs(_LOBE_DROP_BUILT - DOOR_LOBE_DROP) < 1e-6, (
    "the cab door's forward lower lobe is not at its measured depth: "
    "%.4f of rail-to-sill against ref_nolita_doorshut.jpg's %.4f (SPEC 10.106)"
    % (_LOBE_DROP_BUILT, DOOR_LOBE_DROP))
assert _LOBE_DROP_BUILT > 0.50, (
    "the cab door's forward lower lobe has been flattened away: %.3f of "
    "rail-to-sill. It is 0.744 in ref_nolita_doorshut.jpg and its ABSENCE is "
    "what the owner reported at rev 44 (SPEC 10.106)." % _LOBE_DROP_BUILT)

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


# ============================================================ rev 48, JOB 1
# THE ENGINE / TRUNK LID, OPENED -- his newest requirement.
#
#     "we're going to need the trunk open like it's in service"
#
# WHAT IS MEASURED, AND WHAT IS NOT.  Stated before the constants, because
# three revisions of this project have been spent unpicking a placeholder that
# was quietly promoted to a measurement.
#
# MEASURED, and it is why this is a SEPARATION and not a rebuild:
#   the lid ALREADY EXISTS as a free-floating closed island inside T1_body.
#   engine_lid_gap() cuts a real 5.5 mm through-slot, and build.py:69 records
#   the connected-component count going 1 -> 6 "as each gap cutter frees a
#   panel".  A T1_SUB=2 build gives exactly six, and one of them is
#       7982 v   x -1.873..-1.870   y -0.467..+0.467   z 0.608..1.103
#   which is gap_prism's own outline (y +-0.470, z 0.6025..1.1025) to 3 mm.
#   WATCHED PRINT, not inferred from the source -- the brief's §9 trap about
#   the sign props is exactly this failure mode, and this went the other way.
#
# NOT MEASURED.  No frame in this project shows the trunk open:
#   * the open ANGLE.  TRUNK_OPEN_DEG carries NOT MEASURED in its own comment
#     and verify_clone.sh requires that declaration to stay present, so it
#     cannot be silently promoted (the LINE_GAP precedent, rev 47).
#   * stay-held vs counterbalanced.  NOTHING is built for it -- an invented
#     strut would be a claim, and a claim in prose is not a guard (rule 1).
#   * what the inner face carries.  Left as plain body paint.
#
# AND ONE THING THAT IS TYPE-LEVEL, NOT VEHICLE-LEVEL, SO IT IS LABELLED:
#   a T1's engine lid is TOP-hinged, the lower edge swinging aft and up.  That
#   is a property of the model of vehicle.  The owner has ruled that geometry
#   transfers between his frames -- "the geometry appears the same" -- so this
#   is admissible, but it is NOT a measurement of HIS bus and is not recorded
#   as one.
#
# WHY THIS RUNS AFTER THE RAKE SHEAR (build.py step 8b), UNLIKE roof_lids().
#   _hinge() rotates about a FORE-AFT axis, so it changes y and z and leaves
#   x alone -- which is why a roof lid can be swung before the shear and still
#   be sheared at its correct station.  A tail lid hinges about a LATERAL
#   axis and DOES move x.  Swing it first and step 8b shears it by the wrong
#   station, tilting the open lid by the rake angle for no reason.  So the
#   swing happens after the shear, in the final frame.
#
# THE FRAGILITY THIS MUST NOT DISTURB (t1_core.py:230-244): gap_englid is the
# model's most delicate boolean -- at NHALF=56 it is REJECTED at SUB=2 and
# moving the cutter in x does not fix it.  NOTHING HERE TOUCHES THE CUTTER OR
# THE OUTLINE.  The panel is separated after the fact; the boolean is
# untouched, so that failure mode cannot be reopened by this change.

TRUNK_OPEN_DEG = 52.0
# NOT MEASURED.  No frame we hold shows this lid open, so this is a POSE
# CHOICE, not a measurement, and it is written here rather than buried.  It
# is the angle at which the lid reads as open and in service without the
# lower edge fouling the rear valance.  Provenance: rev 48, JOB 1; no frame.
# If a photograph of the open tail ever arrives, this is the first thing to
# re-derive, and probe/verify_clone will still be requiring the declaration.

TRUNK_HINGE_INSET = 0.006      # the hinge sits 6 mm below the seam's top edge,
                               # inside the metal, so the lid does not lift
                               # clear of the aperture as it swings.


def _hinge_y(ob, x_hinge, z_hinge, deg):
    """Rotate a lid about a LATERAL (Y) hinge axis, in place, into world space.

    The tail-lid sibling of _hinge().  _hinge() spins in the y-z plane about a
    fore-aft axis; this spins in the x-z plane about a lateral one.  Positive
    `deg` swings the lower edge AFT (-x) and UP, which is how a T1 engine lid
    opens.  Baked into vertices, never an object transform: build.py step 8b
    asserts every mesh carries identity, and reads v.co.x as world x.

    THE SIGN WAS INVERTED ON THE FIRST CUT AND ONLY A RENDER CAUGHT IT.  The
    first version used +sin/-sin in the order that reads naturally as a
    rotation and swung the lower edge FORWARD, folding the lid down INTO the
    engine bay -- with the 1963 plate and the T-handle riding it in, so they
    hung inside the dark cavity.  `VERIFY: 0 fail, 0 warn` and all 95
    verify_clone rows passed on that build.  Nothing in this project's numbers
    could see it; one crop of one render could.  SPEC 10.105.7, and the reason
    `_open_guard` below now exists.
    """
    a = math.radians(-deg)
    ca, sa = math.cos(a), math.sin(a)
    for v in ob.data.vertices:
        x, z = v.co.x - x_hinge, v.co.z - z_hinge
        v.co.x = x_hinge + (x * ca - z * sa)
        v.co.z = z_hinge + (x * sa + z * ca)
    ob.data.update()
    T.fix_normals(ob)


def _components(me):
    """Vertex index sets of `me`'s connected components, largest first."""
    n = len(me.vertices)
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for e in me.edges:
        ra, rb = find(e.vertices[0]), find(e.vertices[1])
        if ra != rb:
            parent[rb] = ra
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)
    return sorted(groups.values(), key=len, reverse=True)


def split_trunk_lid(body, log=print):
    """Separate the already-free engine-lid island out of the shell and OPEN it.

    Returns (lid, hinge_x, hinge_z, deg) so build.py can carry the tail
    hardware -- the T-handle and the 1963 plate -- through the same swing.
    Returns (None, ...) and says why if the island is not there, rather than
    inventing one: if the boolean stopped freeing the panel that is a finding
    about the boolean, not something to paper over here.
    """
    import bmesh
    me = body.data
    # The island we want is the one that matches gap_englid's own outline.
    # Identified by GEOMETRY, never by index -- component order is not stable
    # across subdivision levels.
    want = dict(x=(-1.99, -1.80), y=(-0.52, 0.52), z=(0.50, 1.25))
    comps = _components(me)
    hit = []
    for vs in comps:
        if not (200 < len(vs) < len(me.vertices) * 0.25):
            continue
        co = [me.vertices[i].co for i in vs]
        bb = [(min(c[k] for c in co), max(c[k] for c in co)) for k in range(3)]
        if all(want[a][0] <= bb[k][0] and bb[k][1] <= want[a][1]
               for k, a in enumerate("xyz")):
            hit.append((vs, bb))
    if len(hit) != 1:
        log("!! trunk lid NOT separated: %d islands match the engine-lid "
            "outline (want exactly 1). The gap boolean may have stopped "
            "freeing the panel -- read FAILED_CUTS." % len(hit))
        return None, 0.0, 0.0, 0.0
    vs, bb = hit[0]

    keep = set(vs)
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.verts.ensure_lookup_table()
    lid_faces = [f for f in bm.faces if all(v.index in keep for v in f.verts)]

    lm = bpy.data.meshes.new("lid_trunk")
    lb = bmesh.new()
    vmap = {}
    for f in lid_faces:
        for v in f.verts:
            if v.index not in vmap:
                vmap[v.index] = lb.verts.new(v.co)
        try:
            lb.faces.new([vmap[v.index] for v in f.verts])
        except ValueError:
            pass                       # duplicate face, already added
    lb.to_mesh(lm)
    lb.free()
    lid = bpy.data.objects.new("lid_trunk", lm)
    bpy.context.collection.objects.link(lid)
    if me.materials:
        lm.materials.append(me.materials[0])

    bmesh.ops.delete(bm, geom=[bm.verts[i] for i in vs], context='VERTS')
    bm.to_mesh(me)
    bm.free()
    me.update()

    hx, hz = bb[0][1], bb[2][1] - TRUNK_HINGE_INSET

    # The lid's LOWEST vertex is the free edge -- the one that has to travel.
    # Measured before and after, so the guard tests the motion, not the code.
    # Capture the INDEX as a plain int, not the bpy struct.  _hinge_y mutates
    # the mesh and calls fix_normals, after which the struct is stale and
    # `low.index` reads garbage -- the first version of this guard died with
    # `bpy_prop_collection[-1425949424]: out of range` instead of reporting the
    # defect it was written to catch.  A guard that crashes is not a guard.
    low_i = int(min(lm.vertices, key=lambda v: v.co.z).index)
    x_before = float(lm.vertices[low_i].co.x)
    z_before = float(lm.vertices[low_i].co.z)
    _hinge_y(lid, hx, hz, TRUNK_OPEN_DEG)
    T.fix_normals(lid)
    x_after = float(lm.vertices[low_i].co.x)
    z_after = float(lm.vertices[low_i].co.z)

    # ---- THE GUARD, in the same edit as the change (rule 12), and it exists
    # because the first version of _hinge_y failed EXACTLY here while every
    # number in the project stayed green.  An open engine lid's free edge must
    # go AFT and UP.  Watched fail: with the sign inverted this prints
    #   dx +0.1946 (want negative)  dz +0.0546
    # and stops the build.  Rule 19 -- the control has been seen to fail on
    # the defect, not merely to pass on the fix.
    dx, dz = x_after - x_before, z_after - z_before
    if not (dx < -1e-4 and dz > -1e-4):
        raise AssertionError(
            "trunk lid opened the WRONG WAY: its free edge moved dx %+.4f "
            "dz %+.4f. An engine lid's free edge swings AFT (dx negative) and "
            "UP (dz non-negative). Check _hinge_y's sign -- it was inverted "
            "once already and only a render caught it." % (dx, dz))

    log("trunk lid: separated %dv, hinge (x %.4f, z %.4f) lateral, "
        "OPEN %.1f deg  [angle NOT MEASURED -- no frame shows it]"
        % (len(lm.vertices), hx, hz, TRUNK_OPEN_DEG))
    log("  free edge travelled dx %+.4f m (aft) dz %+.4f m (up) -- guard ok"
        % (dx, dz))
    return lid, hx, hz, TRUNK_OPEN_DEG


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
    # ------------------------------------------------- rev 45, SPEC 10.113
    # REV 45 FOUND THIS DEFECT INDEPENDENTLY AND ITS FIX IS DISCARDED IN FAVOUR
    # OF THE ONE BELOW, WHICH IS BETTER DERIVED.  Recorded rather than quietly
    # dropped, because the two agreeing from different directions is itself the
    # evidence.  Rev 45 measured the same thing -- both feet at y = +0.44,
    # INSIDE the roof aperture (the lid's own closed footprint, LID_Y_HINGE to
    # LID_Y_HINGE + LID_W = -0.545 .. +0.565), so each prop rose out of thin
    # air over the open hatch -- and moved the foot to LID_Y_HINGE - 0.14.
    # That is a TYPED offset.  Rev 44b's below walks roof_z outboard until it
    # stops changing and lands on the roof's OWN edge, which is a measurement
    # of the body rather than a number about it, and it moves the TIP onto the
    # lid's free edge as well.  Rev 45 kept only its Y guard, which is
    # complementary to rev 44b's lean guard: the lean catches a prop that rakes,
    # the Y catches a prop that stands on nothing.
    # rev 44b -- I READ THIS AS A SIGN ERROR AND IT IS NOT ONE.  RECORDED SO
    # IT IS NOT "FIXED" AGAIN.  `LID_X0` is 0.9640 and `LID_X1` is -1.0700 --
    # X0 IS THE LARGER -- so `LID_X1 + 0.16` and `LID_X0 - 0.16` are both
    # INSET, exactly as the comment above says.  I inverted both, and the
    # guard added below in the same edit fired on the first build:
    # "roof-lid prop at x -1.2375 is OUTSIDE the lid's own span 0.9640
    # -1.0700".  The guard was right and the change was wrong; the change is
    # reverted and the guard is kept, with its bounds written the way round
    # the constants actually are.
    # rev 44b -- THE PROPS RAKED ACROSS THE ROOF INSTEAD OF STANDING UNDER THE
    # BOARD.  SPEC 10.108.
    #
    # *[owner, verbatim]* "the props for the sign seem to meet something from
    # the sides of the sign, rather than the sign resting directly on the
    # poles."
    #
    # MEASURED on the built scene, and he is describing it exactly.  Each prop
    # ran from a foot at y +0.44 -- the SHOW side of the roof -- diagonally
    # across the whole opening to a tip at y -0.776, a horizontal travel of
    # 1.22 m against a rise of 1.00 m: a 49 degree rake.  And it met the board
    # at 0.86 of the board's width, which on a board leaning 14 degrees PAST
    # vertical is near its top edge.  A thin rod arriving at 49 degrees and
    # touching a nearly-vertical panel near its top edge does not read as a
    # prop; it reads as a stay wired to the sign's edge, which is the phrase
    # he reached for.  (The tips DO touch -- measured at 8.6 and 8.7 mm from
    # the lid's nearest vertex against a 7.5 mm rod radius, so contact was
    # never the defect.)
    #
    # TWO CHANGES, AND NEITHER NEEDS A PHOTOGRAPH.  A prop stands UNDER the
    # thing it props and meets it AT the edge that bears on it -- that is what
    # a prop is, the same class of argument as a steering wheel being normal
    # to its column (10.104.4).
    #   * the tip moves 0.86 -> 0.97 of the lid's width, i.e. onto the FREE
    #     EDGE, the edge that actually bears;
    #   * the foot moves from y +0.44 to the roof's OWN OUTBOARD EDGE, found
    #     by walking `roof_z` outboard until it stops changing rather than by
    #     typing a y.  The prop then stands at 3 degrees from vertical instead
    #     of 49, directly beneath the edge it carries.
    def _roof_edge_y(xr, y0):
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
        # zh, NOT roof_z(xs, ...).  `_hinge` rotated the lid about the roof
        # height at the lid's MIDPOINT x; using the height at the strut's own x
        # put the tip 18 mm off the panel it is supposed to carry, because the
        # roof is domed fore-and-aft.  Sharing the hinge origin makes the tip
        # land ON the lid's plane by construction rather than by luck.
        tipz = zh + w * math.sin(a) * 0.97
        footy = max(tipy, _roof_edge_y(xs, LID_Y_HINGE))
        foot = Vector((xs, footy, roof_z(xs, footy)))
        tip = Vector((xs, tipy, tipz))
        d = tip - foot
        struts.append(T.cylinder(tuple((foot + tip) / 2), tuple(d.normalized()),
                                 0.0075, d.length, seg=14,
                                 name=f"lid_strut{len(struts)}"))
    # rev 44b -- each prop must stand UNDER the board, not beside it.  Two
    # things asserted, both on the BUILT rod: it is inside the lid's own
    # x-span, and it is nearer vertical than 20 degrees.  The second is the
    # one that fires if anyone ever re-rakes it across the roof again.
    for st in struts:
        vs = [v.co for v in st.data.vertices]
        xs_ = vs[0].x
        assert (min(LID_X0, LID_X1) - 1e-9 <= xs_
                <= max(LID_X0, LID_X1) + 1e-9), (
            "roof-lid prop at x %.4f is OUTSIDE the lid's own span %.4f-%.4f, "
            "so it props nothing (SPEC 10.108)." % (xs_, LID_X0, LID_X1))
        dy = max(v.y for v in vs) - min(v.y for v in vs)
        dz = max(v.z for v in vs) - min(v.z for v in vs)
        lean = math.degrees(math.atan2(dy, dz))
        assert lean < 20.0, (
            "roof-lid prop leans %.1f deg from vertical -- it rakes across the "
            "roof instead of standing under the board (SPEC 10.108)." % lean)
    # GUARD, SAME EDIT AS THE CHANGE (rule 12).  Every prop foot must sit on
    # solid roof -- OUTSIDE the aperture's y band -- or the prop is standing in
    # the hatch again.  The band is the lid's own closed footprint.
    _y_lo, _y_hi = LID_Y_HINGE, LID_Y_HINGE + LID_W
    for _st in struts:
        _fy = min(v.co.y for v in _st.data.vertices)
        assert not (_y_lo < _fy < _y_hi), (
            "SPEC 10.113: prop foot at y=%.4f is INSIDE the roof aperture "
            "(%.4f..%.4f) -- the strut is standing on nothing"
            % (_fy, _y_lo, _y_hi))
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
