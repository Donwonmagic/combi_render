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

# ===========================================================================
# rev 59 -- THE RAMP IS THE RIGHT SIZE AND IN THE WRONG PLACE.  probe_rev59_door.
#
# THE TWO STALE CONSTANTS, AND WHY EACH IS WRONG.  rev 44b wrote the feet as
# (91.1 - 56.0) / 39.54 and (91.1 - 46.0) / 39.54.  The FEET are right --
# re-traced at rev 59 to 56.069 and 46.741, ramp rms 0.112 px.  The other two
# numbers are not:
#   * 91.1 is the WHEEL HUB column.  The datum these are used against is
#     `_ARCH_CX`, the ARCH's centre.  Fitted on the lip they are 9.83 px apart
#     in this frame, which is rule 34 exactly -- a requirement inherits its
#     object, and this one changed object silently.
#   * 39.54 px is not the arch's radius in that image.  It is ARCH_R * 105.9,
#     a scale obtained by ASSUMING the radius it is then used to measure.
#     Fitted directly the radius is 37.28 px.
#
# BOTH ARE NOW MEASURED, IN ONE FRAME, IN THE FLANK PLANE.  The door line and
# the arch lip are both on the flank, so this ratio carries NO px/m and NO
# parallax term -- which is why it is stated without the +-4 % floor the rev-59
# brief attached to it.  That floor came from mixing the flank plane (the
# crown) with the wheel plane (the hub); nothing here does.
#
# THE CONTROL, and it is the reason to believe the number.  The identical
# pixel code run on the SIDE RENDER -- whose front arch is a circle of ARCH_R
# about X_AXLE_F by construction -- recovers ARCH_R to -0.05 %, the arch
# centre to 0.17 px, and the built DOOR_LOBE_A / DOOR_LOBE_B to -0.22 % and
# +1.30 % end to end.  And the ramp's WIDTH in the photograph comes back at
# 0.2502 of R against the built 0.2529, -1.07 %: the step is the right SIZE.
# Only its POSITION is wrong, and BOTH feet move by the same amount -- 66.5 mm
# and 67.5 mm -- which is a translation, not a re-shaping.
#
# NOT 95 mm.  The rev-59 brief section 3.10 says ~95 mm, from A = 41.50 px.
# Measured here A is 38.66 px vertically and the fitted R is 37.28 px; the
# render control recovers A to +1.7 % and R to -0.05 %, so the ruler is the
# smaller one.  Retracted in the brief and the register in the same revision.
# ===========================================================================
_DS_ARCH_CX = 82.53          # ref_nolita_doorshut.jpg, arch lip circle fit
_DS_ARCH_R  = 37.28          # px, same fit, rms 0.437 px over n=54
_DS_FOOT_A  = 56.069         # aft foot of the ramp, tracked walk
_DS_FOOT_B  = 46.741         # forward foot
DOOR_LOBE_A = (_DS_ARCH_CX - _DS_FOOT_A) / _DS_ARCH_R       # 0.7096 * ARCH_R
DOOR_LOBE_B = (_DS_ARCH_CX - _DS_FOOT_B) / _DS_ARCH_R       # 0.9598 * ARCH_R
if os.environ.get("T1_DOOR_STALE"):
    # THE ABLATION.  rev 44b's two constants, put back verbatim.  The rev-59
    # clearance guard below must REFUSE them -- that is how it was watched
    # failing, and a guard that has not been watched fail reports nothing.
    DOOR_LOBE_A, DOOR_LOBE_B = (91.1 - 56.0) / 39.54, (91.1 - 46.0) / 39.54


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

# rev 59 -- RE-BASED, WITH THE CAUSE NAMED, AND THE PROXY DEMOTED.
#
# THE CAUSE.  Both thresholds below were REGRESSION BASELINES armed at rev 41's
# own clearance, never at a measured one.  rev 41 happened to clear the arch by
# 0.0244 m = 0.0653 * ARCH_R, and that accident became the bar.  Traced on
# ref_nolita_doorshut.jpg by probe_rev59_door, THE REAL VEHICLE'S OWN MINIMUM
# CLEARANCE between its cab-door shut line and its front arch lip is
# 0.844 px = 0.0226 * ARCH_R = 8.4 mm -- about a THIRD of what rev 41 demanded.
# So the old bar was not a physical limit; it forbade the vehicle.
#
# AND THE RATIONALE IT INHERITED IS ALREADY REFUTED IN THIS REPO.  The message
# blamed the 205562 v -> 12 v collapse.  SPEC 10.62 says of exactly that
# rationale: "That does not transfer: all six crossings were live at SUB=2 with
# zero non-manifold edges."
#
# THE COMPANION TEST, so the cause is separately testable rather than re-proxied
# (CLAUDE.md's condition for a re-base).  The collapse is a TOPOLOGY event and
# verify.py already tests it DIRECTLY, at both subdivision levels and with no
# threshold to tune: "no boolean may have rolled back" and the non-manifold edge
# count on the shell.  Those rows are what catch the failure this assert was
# only ever a proxy for.  This assert is therefore re-armed as what it can
# actually see -- A FIDELITY TEST against the photographed clearance.
#
# ABLATION: T1_DOOR_STALE=1 restores rev 44b's lobes and this guard must REFUSE.
_ARCH_G_PHOTO = 0.0226               # probe_rev59_door, ref_nolita_doorshut.jpg
assert abs(_MIN_RAD / ARCH_R - _ARCH_G_PHOTO) < 0.030, (
    "cab-door shut line does not clear the front arch the way the photograph "
    "does: built %.4f m = %.4f of ARCH_R, photograph %.4f of ARCH_R "
    "(probe_rev59_door, ref_nolita_doorshut.jpg). For scale, rev 41's "
    "accidental clearance -- the bar this guard used to inherit -- was "
    "%.4f m = %.4f of ARCH_R, about three times what the vehicle has."
    % (_MIN_RAD, _MIN_RAD / ARCH_R, _ARCH_G_PHOTO,
       DOOR_ARCH_G,
       DOOR_ARCH_G / ARCH_R))
assert _MIN_RAD > 0.004, (
    "cab-door shut line within 4 mm of the front wheel arch lip (%.4f m). The "
    "photograph reads 8.4 mm; below 4 mm the two features are not separable in "
    "any frame we hold and the boolean has no material to work in." % _MIN_RAD)
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

# rev 59 -- AND THE SAME INVARIANT ON THE OUTLINE THAT ACTUALLY CUTS.
#
# The guard above is armed on FOUR raw table points, because DOOR_GAP simply has
# no more between the door's rear corner and the ramp.  Four points cannot see a
# sag between them, and the object the boolean uses is not that table -- it is
# DOOR_GAP_S, resampled to 76 and smoothed twice.  So the same invariant is armed
# again, densely, on the smoothed outline.
#
# THE SPAN IS STATED RATHER THAN ASSUMED, which is the whole lesson of 10.102 ->
# 10.106: both END CORNERS are excluded by 60 mm, because the outline turns UP at
# the rear corner (z 0.8700 against the rail's 0.8007 -- reading it as rail sag
# reports 76.7 mm of descent that is not there) and DOWN into the ramp at the
# forward one.  What is left is rail and only rail.
#
# rev 59 measured the photograph's own rail over the same feature: flat to
# 0.81 px = 8 mm across cols 70-123 of ref_nolita_doorshut.jpg.
_RAIL_DENSE = [q for q in DOOR_GAP_S
               if q[1] < 0.90 and _DOOR_X_REAR + 0.060 <= q[0] <= _LOBE_XA - 0.060]
_DENSE_SPREAD = max(q[1] for q in _RAIL_DENSE) - min(q[1] for q in _RAIL_DENSE)
assert len(_RAIL_DENSE) >= 10, (
    "the dense bottom-rail span has collapsed to %d point(s) -- moving _LOBE_XA "
    "aft has eaten the span this guard covers, which is exactly the silent "
    "weakening rev 59 was warned about." % len(_RAIL_DENSE))
assert _DENSE_SPREAD < 0.030, (
    "cab-door bottom rail is not flat on the outline that CUTS: %.1f mm of "
    "descent over x %.4f .. %.4f (%d samples of DOOR_GAP_S). The photograph "
    "holds it flat to 8 mm over the same feature."
    % (_DENSE_SPREAD * 1000.0, _RAIL_DENSE[0][0], _RAIL_DENSE[-1][0],
       len(_RAIL_DENSE)))

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
# LID_W is DERIVED below, immediately after LID_OPEN_DEG, because it depends on it.
# rev 50 -- SURVEY_rev49 finding 49 ("LID_W is too narrow; the joint solve gives
# W = 1.40-1.49 m") IS REFUTED, on this shell's own arithmetic.  THE REFUTATION
# STANDS.  ITS FIGURES DO NOT, AND THE OWNER HAS SINCE CLOSED ITS LAST CLAUSE --
# rev 51.  Struck through rather than deleted, per the wipers/over-rider
# convention, so the propagation stays visible:
#   ~~the roof spans y -0.7273 .. +0.7273 and the aperture starts at the hinge,
#   y = -0.5450, so W <= 0.7273 + 0.5450 = 1.2723 m OR THE HOLE RUNS OFF THE ROOF.
#   At W = 1.45 the aperture would end at y = +0.905, i.e. 178 mm PAST the roof
#   edge.~~
#   *** THOSE THREE NUMBERS COME FROM THE RECORD'S STALE Yt = 0.7273.  THE
#   MACHINE WALKS ITS OWN ROOF AND DISAGREES.  Watched print, this revision,
#   from the assert 80 lines below under T1_LIDASPECT=1.2:
#       "the roof reaches only y=0.7347 at the lid station, so W <= 1.2797 m"
#       "LID_W = 1.7469 m runs the roof aperture 467.2 mm PAST the roof edge"
#   so at W = 1.45 the overrun is 1.45 - 1.2797 = 170.3 mm, NOT 178.  LEDGER_rev50
#   sec.3 already said to quote the machine's walk and not the record's Yt; that
#   correction reached the ledger and NOT this block, which is the half-retraction
#   shape this project keeps finding.  DO NOT re-derive from 0.7273. ***
#   The finding's own hard floor, W >= 1.19 m, is admissible only in the last
#   90 mm of the corrected range.
# WHAT SURVIVES:
#   the photographed aspect is scale-free -- L / (W sin a) = 1.713 measured on
#   ref_side.jpg against a built L = 2.034 -- so W*sin(a) = 1.1874 m.  With
#   W <= 1.2797 that forces sin(a) >= 0.9279, i.e. a in [68.1, 90) once the taper
#   fixes a < 90.  76.0 satisfies it.  THAT is what still holds.
# AND WHAT NO LONGER SURVIVES -- THE OWNER CLOSED IT AT REV 50:
#   ~~any W in [1.187, 1.272] leaves a SHOW-SIDE surviving roof strip of only
#   0.000-0.085 m in plan, against the owner's settled "roughly 0.3 m each side"
#   ... THAT IS AN OWNER QUESTION (rev 50 C3), NOT A CONSTANT TO TUNE.  W is left
#   at 1.1100 deliberately: moving it moves the roof aperture, which is his.~~
#   *** HE ANSWERED rev 50 C3: "Retire the number."  The 0.3 m is GONE from the
#   record, so there is no longer any inconsistency between the photographed lid
#   aspect and a roof-strip ruling -- there is no roof-strip ruling.  And LID_W is
#   no longer "left at 1.1100": it is DERIVED below, at 1.2237 m.  Every clause
#   above was live and unannotated until rev 51 and would have re-opened a
#   question he has closed.  Do not re-ask it (rule 34: check WHICH object, and
#   check the cited line still exists). ***
# rev 50, A1 -- CORRECTED FROM 104.0.  THE SIGN WAS WRONG AND THE COMMENT SAID
# SO FOR SIX REVISIONS.  `_hinge` maps the free edge to
# y = LID_Y_HINGE + LID_W*cos(a), so a > 90 puts it on the OFF side of the
# hinge.  At 104.0 it landed at y = -0.8135 -- 87 mm OUTBOARD of the off-side
# roof edge (Yt = 0.7347 -- a THIRD site that published the record's stale
# 0.7273 until rev 51; the machine walks 0.7347, see the assert below) and
# 1.63 m from the counter -- i.e. leaning AWAY from the counter, the exact
# opposite of this line's own comment and of SPEC 135.
# NOTE for anyone sweeping 0.7273: the remaining occurrence in this file, in
# the prop-strut guard's rationale ("the foot is at y +0.7273"), is a NARRATIVE
# OBSERVATION of where a foot landed at a DIFFERENT station, not a roof
# constant. Yt varies with x. Do not "correct" it.
# Raised at AUDIT_rev43:117 and unfixed since.
#
# WHY 76.0 AND NOT 61-78 ANYWHERE:  sin(76) - sin(104) = 0.0 EXACTLY, so this
# change moves NO z dimension of the lid, no bbox row, no roof-cutter extent and
# no strut length -- it flips the lean and nothing else.  Every other candidate
# angle would also change the projected width, which is a SEPARATE and still
# open question (see the bound below), and changing two things at once is how
# this project loses a revision.
#
# 76.0 is inside BOTH admissible windows:
#   * the photographed taper solve, 61-78 deg (SURVEY_rev49 finding 5: the
#     board's span shrinks -5.3 +- 0.6 % top-to-bottom in ref_side.jpg over
#     4 row windows, so the TOP is nearer the show side); corroborated with no
#     measurement at all -- the support rod passes IN FRONT of the painted face
#     in ref_rear34.jpg and IMG_2073.
#   * the roof's own width, 68.9-90 deg.  See the LID_W note below.
#
# The mural still faces the SHOW side: the face is built at z = off (negative)
# in the hinge frame, so its normal (0,0,-1) maps to (dy,dz) = (+sin a, -cos a)
# = (+0.970, -0.242) -- toward the counter and slightly DOWN, i.e. an awning.
# At 104 it was (+0.970, +0.242), toward the counter and UP.
LID_OPEN_DEG = float(os.environ.get("T1_LIDDEG", 76.0))

# ---------------------------------------------------------------- LID_W, rev 50
# WAS 1.1100, TYPED.  NOW DERIVED, AND ONLY BECAUSE THE OWNER RETIRED THE THING
# THAT WAS HOLDING IT.  His settled "roughly 0.3 m of roof each side" was the
# only constraint keeping the lid this narrow; put to him at rev 50 with all
# three readings he ruled *"Retire the number."*  See the roof-aperture block.
#
# THE MEASUREMENT IS SCALE-FREE AND NEEDS NO CAMERA MODEL.  In ref_side.jpg the
# yellow board rectangle's aspect is 418/244 = 1.713 (top edge fitted over 178
# columns at 0.35 px rms; bottom edge read at six clean column stations, all
# agreeing within 3 px).  The board's own length is LID_X0 - LID_X1, so
#     W * sin(a) = (LID_X0 - LID_X1) / 1.713
# and W follows from whatever a is.  Expressed that way, not as a number, so the
# two cannot drift apart (rule 2): change the opening angle and the width
# follows, which is the whole point -- they are one measurement, not two.
#
# CEILING, stated.  The fragile input is the bottom edge, which could not be
# fitted (rms 16.3 px) because the vendor and the roof occlude it, so it is six
# hand-read stations.  The survey's own refutation bounds that: five px of
# systematic error moves the aspect to 1.749 and the width by ~25 mm, and the
# SIGN does not turn over until the height is wrong by 28 px, which six readings
# agreeing within 3 px exclude.  Take W as +- 0.03 m.
# AND IT IS STILL NOT A FREE PARAMETER: the aperture starts at the hinge and the
# roof is only Yt half-wide, so W is hard-bounded above by Yt - LID_Y_HINGE.
# That bound is what refuted SURVEY_rev49 finding 49's W = 1.40-1.49 m, which
# would have run the hole 170.3 mm off the roof (1.45 - 1.2797, on the machine's
# own walk; the 178 mm published here until rev 51 used the record's stale
# Yt = 0.7273 -- the SAME stale figure the block above carried).  The assert below is that bound,
# and it is the reason this is a derivation and not a guess.
# T1_LIDASPECT overrides the measured aspect so the roof bound below can be
# WATCHED FAILING (rule 19).  T1_LIDASPECT=1.2 gives W = 1.747 m, which is
# past the roof edge and reports by how much.
LID_ASPECT = float(os.environ.get("T1_LIDASPECT", 1.7130))   # MEASURED, ref_side.jpg
LID_W = (LID_X0 - LID_X1) / LID_ASPECT / math.sin(math.radians(LID_OPEN_DEG))

def _lid_w_bound():
    """The roof's own half-width at the lid station, walked off the body.

    Deliberately a FUNCTION and not a constant: it is evaluated after the roof
    profile is known, so it is a measurement of the shell rather than a number
    about it.  Returns Yt at the lid's mid station.
    """
    x = (LID_X0 + LID_X1) * 0.5
    zt = T.ZT_ALL(x) - T.rake_drop(x)
    return T.WX(x) * T.G(zt - T.RT_ALL(x)) - T.RT_ALL(x)


_LID_W_MAX = _lid_w_bound() - LID_Y_HINGE
assert LID_W <= _LID_W_MAX + 1e-9, (
    "LID_W = %.4f m runs the roof aperture %.1f mm PAST the roof edge: the "
    "aperture starts at the hinge (y=%.4f) and the roof reaches only y=%.4f at "
    "the lid station, so W <= %.4f m.  This is the bound that refutes "
    "SURVEY_rev49 finding 49's W = 1.40-1.49 m."
    % (LID_W, (LID_W - _LID_W_MAX) * 1000, LID_Y_HINGE,
       _lid_w_bound(), _LID_W_MAX))
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
#   * a strip of roof survives on BOTH sides -- ~~roughly 0.3 m on the off side
#     where the lid hinges, roughly 0.3 m on the show side~~ carrying the bulb
#     string along the drip rail.  ~~The 1.11 m transverse width stands.~~
#
# *** rev 50 -- THE 0.3 m IS RETIRED BY THE OWNER, AND THE 1.11 m WITH IT. ***
#
# It was put to him with all three readings, because his own number had come to
# disagree with a measurement.  The build gave 0.162 / 0.182 m in PLAN and
# 0.286 / 0.306 m as ARC from the aperture edge to the drip rail; it passed only
# on the second reading, and that re-expression happened AFTER the first one
# failed, which is rule 29.2.  Separately, ref_side.jpg's scale-free lid aspect
# demands a lid so wide that the show-side strip falls to 0-85 mm in plan under
# either reading.  His ruling: *"Retire the number."*
#
# THE STRIPS STILL EXIST -- he is retiring the FIGURE, not the feature, and the
# show-side one still has to carry the bulb string along the drip rail.  What is
# gone is 0.3 m as an acceptance value, and with it the only thing that was
# holding LID_W at 1.1100.  See the LID_W block above: the width is now derived
# from the photographed aspect, bounded by the roof's own half-width.
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


def _decal_aspect_guard(ob, tol=0.010, filename="lidmural.png"):
    """The mural decal quad must carry tex/lidmural.png at its authored aspect.

    rev 59, ITEM 1's guard, added in the SAME edit as the fix.

    TWO INDEPENDENTLY OBTAINED QUANTITIES, so it is not a tautology (rule 6):
      * the aspect of the quad AS BUILT, measured off `ob`'s own vertices --
        not recomputed from LID_X0/LID_X1/LID_W, which is what the call site
        already knows;
      * the aspect of the IMAGE FILE, read out of the PNG's IHDR on disk --
        `lid_gen.py` authors that file and nothing here can influence it.

    A stretched decal is invisible to every existing check: the panel is the
    right size, the material is bound, the texture is not stale, and VERIFY
    reads 0 fail.  It is only visible as distortion of the printed artwork.

    WATCH IT FAIL:  T1_LIDINSET=0.030 restores the rev-8..58 inset and this
    must refuse (built 1.6963 against the file's 1.6543, +2.54 %).

    An ABSENT texture is reported as "NO TEXTURE" and is NOT a pass (rule 37).
    """
    import struct
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "tex", filename)
    if not os.path.exists(path):
        print("_decal_aspect_guard: NO TEXTURE at %s -- NOT CHECKED, and this "
              "is an absent input, not a pass" % path)
        return None
    with open(path, "rb") as fh:
        head = fh.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        print("_decal_aspect_guard: %s is not a PNG IHDR -- NOT CHECKED"
              % filename)
        return None
    iw, ih = struct.unpack(">II", head[16:24])
    co = [v.co for v in ob.data.vertices]
    # ASK THE MESH, not the pose or the constants (rule 35): the quad's own
    # two edge lengths, taken as the bbox spans in the frame it was built in.
    bl = max(c.x for c in co) - min(c.x for c in co)
    bw = max(c.y for c in co) - min(c.y for c in co)
    built, authored = bl / bw, iw / float(ih)
    err = built / authored - 1.0
    print("decal aspect: built %.4f (%.4f x %.4f m) vs %s %d x %d = %.4f "
          "-> %+.2f %%" % (built, bl, bw, filename, iw, ih, authored,
                           err * 100.0))
    assert abs(err) <= tol, (
        "SPEC/rev 59 item 1: the mural decal quad is %.4f but tex/%s is "
        "authored %d x %d = %.4f, so the printed image is stretched %+.2f %% "
        "along the vehicle (tolerance %.1f %%).  lid_gen.py traces the OUTER "
        "edge of the yellow strips as the board boundary; a border inset here "
        "makes the two files disagree about what that edge means."
        % (built, filename, iw, ih, authored, err * 100.0, tol * 100.0))
    return err


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
#   which is gap_prism's own outline (y +-0.470, z 0.6200..1.1200) to 3 mm.
#   (that z pair was published 0.6025..1.1025 for several revisions -- rrect is CENTRED, so the centre is the +0.8700 literal.  rev-50 corr.)
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

TRUNK_OPEN_DEG = 0.0
# *** SHUT, BY THE OWNER'S RULING AT REV 49. ***
#
#     "Leave the lower bay shut, just have the back trunk window open for
#      service."
#
# THIS REFUTES AN INFERENCE REV 48 MADE AND SHIPPED.  Asked at rev 48 which of
# the two rear apertures should be open -- with both marked by projection on a
# straight rear view -- he chose A, the rear window.  Rev 48 then reasoned that
# "he called the upper one the MAIN bay, not the ONLY one", kept the lower lid
# open too, and recorded that reading in SPEC 10.122.4 and in this file.  He has
# now said plainly that only the window is open.  THE INFERENCE WAS THE DEFECT:
# a choice between two things is not a licence to keep both.  Rule 6 -- an
# ordinal fact ("the MAIN bay") licenses a SIGN, never a SHAPE.
#
# 0.0 MEANS SHUT AND THE SWING IS SKIPPED ENTIRELY, not run at zero: the
# direction guard in _swing_open() asserts the free edge actually travels, so
# calling it with 0.0 would fire it.  The panel is still SEPARATED and named --
# the shut line already existed as gap_englid, so a closed free panel is
# geometrically identical to the un-separated body and costs nothing, and it
# keeps the capability one constant away.
#
# IF IT IS EVER REOPENED THE ANGLE IS **NOT MEASURED** -- no frame we hold
# shows this lid open, so any non-zero value here is a POSE CHOICE, not a
# measurement.  The previous pose choice was 52.0.  It is
# the angle at which the lid reads as open and in service without the
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


# ----------------------------------------------------- rev 48, JOB 1b
# THE REAR HATCH, OPENED.  His correction, after seeing the trunk lid open:
#
#     "the main bay that should be open is the upper one"
#
# Asked with both apertures marked on a straight rear view of the build -- A
# the rear window (z 1.284..1.616, built as `glass_rear`), B the engine lid
# (z 0.603..1.103, opened above).  He chose A.  His earlier standing request,
# "we're going to need the trunk open like it's in service", is NOT withdrawn
# by that -- he said the upper one is the MAIN bay, not the only one -- so B
# stays open and A is added.
#
# WHAT IS BUILT.  `glass_rear` is a 6 mm glazed pane sitting 20 mm inboard of
# the tail skin, in an aperture `rear_cutter()` has always cut.  The aperture
# is therefore already there; only the pane was closing it.  So this is the
# same shape of job as the trunk lid -- swing what is already a separate part,
# do not model anything new -- and it uses the SAME guard.
#
# WHAT IS NOT MEASURED, and it is more than for the trunk:
#   * the ANGLE.  Same status as TRUNK_OPEN_DEG: no frame shows it.
#   * WHETHER THE PANE IS THE HINGED PART AT ALL.  On a stock T1 the rear
#     window is fixed glass.  On this converted vehicle `ref_rear34.jpg` shows
#     the rear window still reading as GLAZED with the large open serving
#     aperture BELOW it on the flank -- so hinging the pane is HIS INSTRUCTION
#     applied to the part that occupies that station, not a reading of a
#     photograph.  Recorded plainly so the next revision can undo it cheaply
#     if a frame of the open tail contradicts it.

REAR_OPEN_DEG = 64.0
# NOT MEASURED.  A pose choice, like TRUNK_OPEN_DEG, and guarded to keep
# saying so.  Wider than the trunk's 52 deg because this pane swings up over
# the roof line where nothing fouls it, and because a serving hatch is propped
# clear of the people under it.  Provenance: rev 48 JOB 1b, his instruction;
# no frame.


# ------------------------------------------------------- rev 48, the TRUNK BAY
# With the engine lid open the aperture showed a flat black void, which is the
# most visible defect in the whole tail.  He was asked how to leave it and
# chose "fill it as a service bay", then said "I trust your judgement."
#
# WHAT IS BUILT: a LINING -- floor, back, two sides, roof -- so the opening
# reads as a compartment rather than a hole cut in a shell.
#
# WHAT IS DELIBERATELY NOT BUILT: its CONTENTS.  No frame in this project
# shows the trunk open at all, `PHOTOS_WANTED_rev44` records that "the engine
# was scrapped and the transmission sold", and so what is in there is unknown.
# Crates, a gas bottle and service kit would be invention -- exactly the class
# of detail this project refuses without a photograph, and exactly what was
# said to him when the option was offered.  Judgement exercised, and stated:
# THE VOID IS FIXED, THE CONTENTS ARE NOT INVENTED.  One frame of the open
# tail turns this from a lining into a measurement.
#
# Sized off the aperture itself, never typed: gap_prism's outline is
# y +-0.470, z 0.6200..1.1200 above ground, so the lining is inset one skin
#   (that z pair was published 0.6025..1.1025 for several revisions -- rrect is CENTRED, so the centre is the +0.8700 literal.  rev-50 corr.)
# thickness inside that and runs forward BAY_DEPTH from the tail cap.

BAY_DEPTH = 0.42                 # forward of the tail skin.  NOT MEASURED --
                                 # deep enough that the back is not visible
                                 # through the aperture at any camera in
                                 # studio.views(), which is the only property
                                 # it needs to have.
BAY_INSET = 0.010                # inside the cut edge, so no z-fighting with
                                 # the aperture's own returned rim.


def trunk_bay(log=print):
    """A plain lining behind the engine lid, so the bay is not a void.

    Runs in step 8c AFTER the shear, like the lids, so it lands in the final
    frame without being sheared twice.
    """
    BAY_INSET_X = 0.0020        # how far INBOARD of the tail skin the lining
                                # sits.  POSITIVE = inside.  It was applied
                                # with the wrong sign until rev 49; see below.
    # rev 50 -- THESE WERE THREE TYPED LITERALS AND ONE OF THEM WAS STALE BY
    # 17.5 mm.  They are now DERIVED FROM ENGLID_GAP AT RUN TIME (rule 2): this
    # object LINES that aperture, so its extents are that aperture's extents
    # inset by one skin, and typing them lets the two drift.  They had drifted.
    #
    # `T.rrect(w, h, r)` is "centred on origin" by its own docstring, so
    # ENGLID_GAP = rrect(0.9400, 0.5000, ...) offset by v + 0.8700 spans
    #     y +-0.4700   z 0.6200 .. 1.1200
    # The repository published z 0.6025 .. 1.1025 in FOUR places -- same height
    # (0.5000 exactly), centre 0.8525 against the built 0.8700, i.e. stale by
    # 17.5 mm from an earlier value of that +0.8700 literal.  Three of the four
    # are comments.  THE FOURTH WAS THIS LINE, live code, so the lining was
    # actually built 17.5 mm below the aperture it lines.
    # This is the third defect found in trunk_bay() in two revisions (rev 49
    # found the missing material and the inverted 2 mm inset); all three are the
    # same shape -- a number about another object, typed instead of derived.
    _gy = [u for (u, v) in ENGLID_GAP]
    _gz = [v for (u, v) in ENGLID_GAP]
    y = max(_gy) - BAY_INSET
    z0, z1 = min(_gz) + BAY_INSET, max(_gz) - BAY_INSET
    if os.environ.get("T1_BAYSTALE"):
        # rev-50 ablation (rule 19): restore the typed 0.6025..1.1025 pair this
        # line carried until rev 50, so the guard below can be WATCHED FAILING
        # on the real 17.5 mm defect.  It moves the LINING ONLY -- the guard's
        # reference stays ENGLID_GAP, or it would move with it and prove nothing.
        z0, z1 = 0.6025 + BAY_INSET, 1.1025 - BAY_INSET
    # GUARD, SAME EDIT AS THE CHANGE (rule 12).  The lining must sit INSIDE the
    # aperture on all four sides, by exactly one inset.  Compares the BUILT
    # extents against ENGLID_GAP's own, which is two independently obtained
    # quantities and not one expression checked against itself (rule 32).
    x_skin = T.X_TAIL
    pts = T.rrect((z1 - z0), (2 * y), 0.030, seg=6)
    pts = [(u + (z0 + z1) * 0.5, v) for (u, v) in pts]      # (z, y) frame
    # T.solid_prism EXTRUDES CENTRED ON ITS ORIGIN, not forward from it.
    # Measured, watched print: origin x -1.875 with depth 0.42 produced a bay
    # spanning -2.085..-1.665, i.e. +-depth/2 -- so half of it stood PROUD of
    # the tail skin and the length row went red at +190 mm.  The origin is
    # therefore advanced by half the depth, expressed in terms of it rather
    # than typed, so changing BAY_DEPTH cannot reopen the same defect.
    # *** rev 49: THE SIGN OF THIS INSET WAS INVERTED, AND IT SHIPPED. ***
    #
    # It read `x_skin - 0.002 + BAY_DEPTH * 0.5`.  solid_prism extrudes +-depth/2
    # about its origin, so the aft face landed at x_skin - 0.002 -- 2.0 mm
    # PROUD OF THE TAIL SKIN, not 2 mm inside it.  The comment above says the
    # origin is advanced "so changing BAY_DEPTH cannot reopen the same defect",
    # and it does prevent that one; it does not prevent the inset's own sign
    # being wrong, and nothing measured the face against the skin it lines.
    #
    # IT WAS INVISIBLE FOR A WHOLE REVISION BECAUSE THE LID WAS OPEN.  Nothing
    # stood in front of the lining, so 2 mm of it poking past the tail read as
    # the bay's own back wall.  The owner's rev-49 ruling -- "leave the lower
    # bay shut" -- put the lid back, and the lining then sat 2 mm IN FRONT of a
    # closed panel and won the depth test across the whole of it: the tail
    # rendered with a DARK CHARCOAL rectangle where the red engine lid belongs.
    # VERIFY 0 fail / 0 warn, verify_clone ALL 110 PASS, and one crop showed it.
    # Rule 28, and rule 16 -- a part measured in isolation from what it is
    # fitted to is not measured.
    # T1_BAYPROUD=1 restores the inverted sign so the guard below can be
    # watched failing on the real defect (rule 19).
    _ins = -BAY_INSET_X if os.environ.get("T1_BAYPROUD") else BAY_INSET_X
    ob = T.solid_prism((x_skin + _ins + BAY_DEPTH * 0.5, 0, 0),
                       (0, 0, 1), (0, 1, 0),
                       (1, 0, 0), pts, BAY_DEPTH, name="trunk_bay")
    # THE GUARD, IN THE SAME EDIT (rule 12), against the CAUSE: the lining must
    # lie entirely INBOARD of the tail skin, whatever BAY_DEPTH or the inset do.
    # rev 50 GUARD -- THE LINING'S OWN FACE AGAINST THE APERTURE IT LINES.
    # MY FIRST VERSION OF THIS WAS A TAUTOLOGY AND I CAUGHT IT BY READING IT
    # BACK, NOT BY RUNNING IT: it asserted `(z0 - min(ENGLID_GAP.z)) == BAY_INSET`
    # two lines after setting `z0 = min(ENGLID_GAP.z) + BAY_INSET`.  Identically
    # true by construction, rule 32, in the same edit that cites rule 32.
    # This one reads the BUILT PRISM'S OWN VERTICES against ENGLID_GAP -- two
    # independently obtained quantities -- so it also covers the rrect mapping,
    # the (z,y) frame swap, solid_prism's centred extrusion and any transform.
    # WATCHED FAIL on T1_BAYSTALE=1, which restores the 0.6025..1.1025 literals
    # this line was built from until rev 50 and reports the 17.5 mm.
    _bz = [(ob.matrix_world @ v.co).z for v in ob.data.vertices]
    _by = [(ob.matrix_world @ v.co).y for v in ob.data.vertices]
    for _nm, _got, _want in (("z lower", min(_bz), min(_gz) + BAY_INSET),
                             ("z upper", max(_bz), max(_gz) - BAY_INSET),
                             ("y half", max(_by), max(_gy) - BAY_INSET)):
        if abs(_got - _want) > 5e-4:
            raise AssertionError(
                "trunk bay lining's %s is %.4f, %.1f mm from the ENGLID_GAP "
                "aperture it lines inset by BAY_INSET (%.4f).  The lining and "
                "the aperture must not be typed independently -- they drifted "
                "17.5 mm before rev 50 derived one from the other."
                % (_nm, _got, (_got - _want) * 1000, _want))
    _aft_face = min((ob.matrix_world @ v.co).x for v in ob.data.vertices)
    if _aft_face < x_skin + 1e-6:
        raise AssertionError(
            "trunk bay lining is PROUD of the tail skin: its aft face is at "
            "x %.4f against a skin at x %.4f (%.1f mm outside).  With the lid "
            "shut this renders THROUGH the closed panel."
            % (_aft_face, x_skin, (x_skin - _aft_face) * 1000))
    log("trunk bay: lining %.3f m deep, y +-%.3f, z %.4f..%.4f  "
        "[a LINING -- contents NOT invented, no frame shows them]%s"
        % (BAY_DEPTH, y, z0, z1,
           "  -- UNSEEN while TRUNK_OPEN_DEG is 0 (the owner's rev-49 ruling); "
           "KEPT because the compartment is real and reopening it is one "
           "constant away" if abs(TRUNK_OPEN_DEG) < 1e-6 else ""))
    return ob


# ===========================================================================
# rev 49 -- THE TAIL BOARD.  SPEC 10.123.
#
# WHAT IT IS.  A thin bulb-lined board standing off the aft end of the drip
# rail and leaning back over the tail.  Both RED frames carry it; both GREEN
# frames carry one at the same station (geometry corroboration only -- no
# figure and no colour was taken off a green frame, rule 26).
#
# THE OWNER SETTLED ITS IDENTITY, rev 49: "That was referring to a different
# sign. This one is part of the vehicle."  He is right, and the frames prove
# it rather than merely permitting it:
#   * the board's base sits ON the drip rail -- 1 px from the project's own
#     locked drip-rail fit;
#   * its bulb string is CONTINUOUS with the drip-rail bulb run.  One circuit.
#   * a power cable descends from it into the body.
# A sign standing on the ground behind the bus does none of those.
#
# WHAT IT IS NOT, AND WHY THAT MATTERED FOR FOUR REVISIONS.
#   * NOT signboard().  That is the "La Santa" CREAM + RED BRUSH SCRIPT board
#     which stands on the GROUND BEHIND the bus in ref_rear34.jpg, retired by
#     the owner 2026-08-10 (SPEC 10.28, re-affirmed 10.49 and 10.122.5).  Two
#     different objects in the SAME frame; the record conflated them, and the
#     rev-49 brief inherited the conflation and then contradicted it.
#     signboard() also could not do this: fore-aft hinge (_hinge, :1201) where
#     this needs lateral, SIGN_X1 = -1.7800 stops 92.7 mm short of X_TAIL, and
#     it overlaps only 0.058 m of this board's 0.559 m fore-aft run.
#   * NOT the engine lid.  Refuted twice over.  Rev 48 measured the base at
#     11 sigma from ENGLID_GAP's z 0.6200..1.1200.  Stronger, rev 49: the
#   (that z pair was published 0.6025..1.1025 for several revisions -- rrect is CENTRED, so the centre is the +0.8700 literal.  rev-50 corr.)
#     engine lid is top-hinged at z 1.103 over a 0.50 m panel, so NO opening
#     angle puts any part of it above z 1.60.  This board's TIP is at 2.184.
#     Unreachable, at any angle.  And the engine-lid band is directly visible
#     in ref_side.jpg, CLOSED, red, carrying the yellow swirl.
#
# EVERY NUMBER, AND WHERE IT CAME FROM.  Measured on ref_side.jpg (RED) through
# the project's own scale chain (SPEC 10.35's X(u) map + LOFT_GROUND_rev15
# sec.0.4's k_t, renormalised and C0-checked against X(242.84)=+1.3000,
# X(749.38)=-1.1000, X(922.2)=X_TAIL).  Uncertainties are Monte-Carlo over
# endpoint jitter, k_t 215.5+-3.0 and the datum +-0.020.
TB_TILT_DEG = 38.0        # MEASURED +-2.3, FROM HORIZONTAL.  Say which datum:
                          # from VERTICAL this is 52.0, and the rev-49 brief's
                          # bare "39 degrees" does not state which it meant.
TB_CHORD    = 0.7110      # MEASURED +-0.028, in the vehicle's XZ plane.
                          # The IMAGE-PLANE chord is 0.745 m; reading it with a
                          # single px/m over-reads by 4.8 % because the map's x
                          # and z scales differ at that station.
TB_T        = 0.0220      # NOT MEASURED.  Board thickness is at the frame's
                          # blur floor and cannot be separated from the painted
                          # border bands at 1024 px.  A pose choice.
TB_BORDER   = 0.0210      # the red edge band, 4-5 px at ~215 px/m.  ARTWORK,
                          # and RED-frame only.
# THE WIDTH ACROSS THE VEHICLE IS NOT MEASURED, AND IT IS NOT MEASURABLE FROM
# ANYTHING WE HOLD.  The board's plane contains the lateral direction, so its
# width projects ONLY through parallax -- 33.5 px per metre, and (being a cross
# product) IDENTICAL at base and tip, so the projected width cannot taper.  The
# observed silhouette DOES taper (19.9 px at the base, 7.2 over the last 40
# columns), so the thickness carries the board's own material and border too,
# and the two cannot be separated at this resolution.
#   UPPER BOUND, admissible:  W <= 19.9/33.5 = 0.59 m.
#   LOWER BOUND:              NONE.  7 px of the tip half is fully accounted
#                             for by a 30 mm board plus a border.
# That bound alone REFUTES a full-width board: the roof aperture is 1.11 m
# across and the body 1.750 m, both excluded by more than 2x.  ref_rear34.jpg
# cannot close it -- the candidate free edge runs off the frame at u=1199, and
# SPEC 10.48 admits px/m there only on the plate plane.
TB_WIDTH    = 0.5500      # POSE CHOICE, NOT MEASURED.  Inside the 0.59 bound.
# The lateral CENTRING is a pose choice too: a broadside frame cannot see it.
TB_Y_CENTRE = 0.0000      # POSE CHOICE, NOT MEASURED.


def tail_board(log=print):
    """The bulb-lined board at the tail.  Runs in step 8c, after the shear.

    AFTER THE SHEAR, DELIBERATELY.  Every figure above was measured off a
    photograph of the vehicle in its own raked stance, and the drip-rail datum
    z = 1.7485 is quoted ABOVE GROUND.  So they are final-frame coordinates and
    the board must be placed in the final frame, exactly as the lids and
    trunk_bay are.  Placed before step 8b it would be sheared a second time.
    """
    a = math.radians(TB_TILT_DEG)
    # THE BASE STATION IS DERIVED, NOT TYPED (rule 2).  Measured X_TAIL+0.151
    # +-0.022; t1_detail.gutter() ends at T._aft(-1.880) = X_TAIL+0.1745.  They
    # agree to 24 mm, inside the measurement's own +-0.022 stat and +-0.035
    # depth-plane uncertainty -- so the board is hung on the gutter's own aft
    # end and moves with it, rather than carrying a literal that would go stale
    # the moment the gutter is re-spaced.
    # THE BASE: WHAT IS MEASURED, WHAT IS NOT, AND THE ONE INCONSISTENCY THAT
    # THE FRAMES WE HOLD CANNOT RESOLVE.  Read this before moving it.
    #
    # THREE READINGS, AND THEY DO NOT ALL CLOSE:
    #  (1) the board's near lower corner sits ON the drip-rail line -- 1 px from
    #      cream_rms.py:91's locked fit (predicted v 293.1 at u 890, reads 294);
    #  (2) the station is X_TAIL + 0.151 +- 0.022 IN THE NEAR-FLANK PLANE, and
    #      that carries a +-0.035 DEPTH ceiling: at the drip-rail plane it is
    #      +0.193, AT THE CENTRELINE IT IS -0.095 -- the sign flips;
    #  (3) the stay's own triangle -- top 0.13 m up the chord, 77-78 deg, landing
    #      z 1.578 on the tail skin -- closes only for a base NEAR the roof's
    #      rear corner.  Re-seated to the centreline it lands 144 mm AFT of
    #      X_TAIL, in mid-air.  So (3) refutes the centreline re-seating of (2).
    #
    # AND (1) AND (3) TOGETHER STILL DO NOT CLOSE.  A board based at RAIL height
    # and spanning laterally is buried in the roof, because the crown at this
    # station is 1.8851 against a rail at 1.8052 -- 80 mm of roof over the
    # inboard span.  The near-edge read and a clear foot are 80 mm apart and
    # nothing we hold separates them: the frames are broadside, so the near edge
    # is all they see, and whether the foot is bracketed, stepped or sits aft of
    # the roof corner is exactly the FOOTING detail SPEC 10.28 has required a
    # photograph for since rev 12.
    #
    # SO THE BOARD IS BUILT STANDING CLEAR ON THE ROOF AT THE REAR CORNER, and
    # the 80 mm is DECLARED rather than hidden.  That choice is the one that
    # makes the stay's measured triangle land on the body (X_TAIL + 0.153
    # against a measured +0.106) and keeps the foot out of the sheet metal.
    # The alternative -- honouring the near-edge read exactly -- buries it.
    # BOTH numbers are recorded so the next context re-seats rather than
    # re-measures, and neither is presented as settled.
    TB_BASE_DX_NEARFLANK  = +0.1510     # MEASURED, near-flank plane, +-0.022
    TB_BASE_DX_CENTRELINE = -0.0950     # the same measurement re-seated; REFUTED
                                        # by the stay triangle, kept as a record
    TB_BASE_Z_NEAREDGE    = 1.7470      # MEASURED +-0.027, the near lower corner
    # *** rev 49c -- THE 80 mm FOOT INCONSISTENCY DISSOLVES.  It was never a
    # conflict between the photograph and the geometry; the board was at the
    # WRONG STATION. ***
    #
    # The station is now SOLVED, not chosen: it is the station where the roof's
    # own skin is at the photographed base height.  Both facts were already in
    # hand and nobody had put them together (rule 16 -- a part measured in
    # isolation from what it is fitted to is not measured):
    #
    #     photographed base height           1.747 +- 0.027   (near lower corner,
    #                                                          on the drip-rail
    #                                                          line, 1 px fit)
    #     roof skin at x = -1.8500           1.7497
    #                                        -> AGREE TO 2.7 mm
    #
    # and the chord then lands the tip at z 2.200 against a measured
    # 2.184 +- 0.030 -- 16 mm, inside the band.  TWO INDEPENDENT HEIGHTS CLOSE.
    #
    # The previous cut put the base at the gutter's aft end (-1.6982), 175 mm
    # forward of X_TAIL, where the roof is still 1.9608 -- so seating it on the
    # skin threw the tip 227 mm high, and seating it at the photographed height
    # buried the foot 97 mm.  Neither was a real dilemma.  The rear roof corner
    # falls away fast: 1.9608 at -1.6982, 1.8607 at -1.800, 1.7497 at -1.850,
    # 1.6696 at X_TAIL.  There is exactly one station that satisfies both.
    #
    # WHAT IS STILL NOT MEASURED is the FORE-AFT DEPTH PLANE (the solved station
    # sits 128 mm aft of the near-flank silhouette read) and the WIDTH.  Those
    # are the same unmeasurable quantity the parallax argument identifies, and
    # they close with the same photograph.  The HEIGHT chain no longer needs one.
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
        if _n:
            log("  station solve: %d of 61 candidate stations had no skin over "
                "the footprint and were DROPPED" % _n)
    if _bx is None:                       # body absent -- say so, do not guess
        _bx, _bs = T._aft(-1.8800), None
        log("  !! tail board: T1_body absent, falling back to the gutter's aft "
            "end -- the station is NOT solved")
    else:
        log("  station SOLVED from the skin: x %.4f (X_TAIL %+.3f), roof there "
            "%.4f against a photographed base %.4f -- %.1f mm"
            % (_bx, _bx - T.X_TAIL, _bs, TB_BASE_Z_NEAREDGE, _bd * 1000))
    x0 = _bx
    # THE FOOT IS SEATED ON THE ACTUAL BODY MESH, NOT ON A PROFILE FUNCTION.
    #
    # *** rev 49b: THE FIRST CUT USED THE WRONG SURFACE, AND THE GUARD WRITTEN
    # TO CATCH THAT COMPARED AGAINST THE SAME WRONG SURFACE, SO IT COULD NEVER
    # NOTICE. ***
    #
    # It read  z0 = ZT_ALL(x0) - rake_drop(x0) + 0.005  and then guarded with
    # _crown = ZT_ALL(x0) - rake_drop(x0), so z0 - _crown was IDENTICALLY
    # +0.005 BY CONSTRUCTION and `z0 < _crown` could not fire in the shipped
    # path.  It only ever fired because T1_TBFOOT=1 substitutes a different z0
    # -- so it was testing the escape hatch, not the construction.  Rule 20: an
    # instrument that has never been wrong has never been tested, and this one
    # was written in the same revision that quoted the rule.
    #
    # AND ZT_ALL IS NOT THE CROWN.  It is the ROLL START -- the top of the flank
    # before the roof curves over; t1_detail.bulb_string() uses ZT_ALL - RT_ALL
    # for the drip rail, which is the tell.  Measured on a real T1_SUB=1 build:
    #     ZT_ALL(x0) - rake_drop(x0)                 = 1.8673
    #     ACTUAL body top over the board's footprint = 1.9608   <- 93 mm higher
    # so the board's lowest vertex sat 97.1 mm INSIDE the roof, and the render
    # showed a board growing out of solid sheet metal.
    #
    # THE FIX IS TO STOP ASKING A FUNCTION AND MEASURE THE THING IT IS FITTED TO
    # (rule 16).  The seat is the maximum z of T1_body's own vertices over the
    # board's own footprint, in the final frame, which cannot be wrong about the
    # skin because it IS the skin.
    _seat = _bs
    if _seat is None:                     # body absent -- say so, do not guess
        _seat = T.ZT_ALL(x0) - T.rake_drop(x0)
        log("  !! tail board: T1_body absent, seating on ZT_ALL -- NOT the skin")
    # THE STANDOFF IS DERIVED FROM THE BOARD'S OWN SECTION, NOT TYPED.
    # T.solid_prism extrudes CENTRED on its origin, so the board hangs
    # TB_T/2 * cos(tilt) BELOW z0 along its own normal.  A typed 5 mm standoff
    # left the foot 3.7 mm inside the skin -- caught by the new guard below on
    # its first run, which is the whole point of measuring the built thing
    # against the built skin instead of a function against itself.
    _hang = TB_T * 0.5 * math.cos(a)
    z0 = _seat + _hang + 0.0040        # 4 mm of daylight under the lowest corner
    # T1_TBFOOT=1 restores the ORIGINAL buried value so the guard below can be
    # watched failing on the real defect rather than on an injected one.
    if os.environ.get("T1_TBFOOT"):
        z0 = T.ZT_ALL(x0) - T.rake_drop(x0) + 0.0050
    u = (-math.cos(a), 0.0, math.sin(a))          # up the chord, aft and up
    v = (0.0, 1.0, 0.0)                           # across the vehicle
    w = (-math.sin(a), 0.0, -math.cos(a))         # the board's own normal
    pts = T.rrect(TB_CHORD, TB_WIDTH, 0.012, seg=4)
    pts = [(uu + TB_CHORD * 0.5, vv) for (uu, vv) in pts]   # run from the base
    board = T.solid_prism((x0, TB_Y_CENTRE, z0), u, v, w, pts, TB_T,
                          name="tail_board")
    NOT_BODYWORK.add(board.name)      # on the vehicle; not its sheet metal
    # *** rev 51 -- THIS COMMENT USED TO CLAIM THE OPPOSITE OF THE TRUTH. ***
    # It read: "It measures the BUILT BOARD against the BUILT SKIN -- two
    # independent things -- so it cannot be satisfied by construction the way its
    # predecessor was."  That is FALSE, and in the same direction as the rev-49b
    # guard it was written to replace.  z0 = _seat + _hang + 0.0040, and
    # T.solid_prism extrudes centred along w while T.rrect returns exact extremes
    # with pts shifted so min u = 0, so the board's lowest vertex is IDENTICALLY
    # z0 - _hang = _seat + 0.0040, whatever _seat is.  `_lo < _seat` therefore
    # CANNOT FIRE in the shipped path, and the log prints "+4.0 mm clear" on
    # every build because 4.0 mm is what was typed two lines up, not what was
    # measured.  Rule 32, third occurrence on this one guard.  The owner's own
    # rev-51 brief already says so ("pinned at exactly +4.0 mm by construction");
    # the SOURCE said the reverse until now.
    #
    # WHAT IT ACTUALLY IS: a CONSTRUCTION-CONSISTENCY check.  Kept, because it
    # still catches a z0 that is not built from _seat at all -- which is what
    # T1_TBFOOT=1 substitutes, and why that ablation fires.  Relabelled, not
    # deleted (rule 5: keep the rationale, correct the shape).
    _lo = min((board.matrix_world @ vv.co).z for vv in board.data.vertices)
    if _lo < _seat - 1e-6:
        raise AssertionError(
            "tail board foot is BURIED: its lowest vertex is at z %.4f against a "
            "measured roof skin at z %.4f over its own footprint -- %.1f mm inside "
            "the body.  A fixture's foot must be clear of the body it stands on."
            % (_lo, _seat, (_seat - _lo) * 1000))
    log("  foot: lowest vertex z %.4f on a MEASURED skin seat of %.4f "
        "(+%.1f mm clear -- CONSTRUCTION-CONSISTENCY, pinned by z0's own +4.0 mm; "
        "NOT a free-running clearance)" % (_lo, _seat, (_lo - _seat) * 1000))
    # *** rev 51 -- I TRIED TO ADD A FREE-RUNNING CHECK HERE AND IT FAILED ITS
    # OWN CONTROL.  RECORDED, NOT SHIPPED, AND THE REASON IS USEFUL. ***
    # The guard above cannot police _seat itself, and _seat is exactly what was
    # wrong at rev 49b.  So I cross-checked the mesh read against what looked like
    # an independent analytic route to the same surface --
    #     _seat_analytic = roof_z(x0, TB_Y_CENTRE) - T.rake_drop(x0)
    # -- with a 20 mm subdivision/solidify budget.  IT FIRED ON THE CLEAN BUILD:
    #     mesh 1.7497  vs  roof_z analytic 1.6391   -- 110.6 mm apart
    # and the instrument is what is wrong, not the build.  x0 = -1.8530 is 20 mm
    # from X_TAIL, INSIDE THE TAIL ROLL-DOWN, and roof_z (zt + cr*(1-(y/Yt)^2)) is
    # the main-run crown formula -- it does not describe the surface where the
    # body turns down over the tail.  ZT_ALL is worse there still (1.6227).
    # LEDGER_rev49 sec.6a's own walk of the skin agrees with the MESH and not with
    # either formula: "1.9608 at -1.6982, 1.8607 at -1.800, 1.7497 at -1.850,
    # 1.6696 at X_TAIL".
    #
    # SO THE HONEST STATEMENT IS: at the board's station there is NO analytic route
    # to cross-check _seat against.  Reading it off the body mesh is not merely the
    # better choice, it is the ONLY correct one -- which is also the deeper reason
    # rev 49b went wrong, and a warning to anyone who tries to "tidy" this into a
    # profile function.  I did NOT widen the tolerance to make my check pass; the
    # check is withdrawn.  (Rule 4: an instrument that fails its control is not
    # evidence.  Rule 19: watch it fail -- it failed, on the wrong thing.)
    tip = (x0 + u[0] * TB_CHORD, TB_Y_CENTRE, z0 + u[2] * TB_CHORD)
    log("tail board: base x %.4f (SOLVED from the skin) z %.4f (standing CLEAR on "
        "the roof AND at the photographed base height -- rev 49b's 80 mm "
        "inconsistency DISSOLVED, it was a wrong station), %.1f deg from "
        "HORIZONTAL, chord %.3f m -> tip x %.4f z %.4f"
        % (x0, z0, TB_TILT_DEG, TB_CHORD, tip[0], tip[2]))
    log("  width %.3f m and lateral centring are POSE CHOICES -- NOT MEASURED; "
        "parallax bounds the width at <= 0.590 m and gives NO lower bound"
        % TB_WIDTH)
    return board, (x0, z0), tip


def tail_board_edge(base, log=print):
    """The board's painted rim band.  MEASURED as artwork, RED frame only.

    WHAT WAS MEASURED, on ref_side.jpg at 8x, 11-16 samples per band:
        over the TIP half   a saturated RED band, (210,55,55), 4-5 px
        over the BASE half  a cool near-black, (85,76,88), B > R
        immediately below the red, a warm near-black (69,40,40), ~5 px
    At ~215 px/m a 4-5 px band is TB_BORDER = 21 mm.

    WHY IT IS BUILT ON THE RIM.  The board is seen almost edge-on in every
    frame we hold, so the "boundary band" the measurement found IS the board's
    own rim -- that is what an edge-on panel presents.  Building it as a face
    border instead would be a claim about a face no frame resolves.

    THE COLOURS ARE CEILINGS, NOT MATCHES.  ref_side.jpg is clipped: the bulbs
    read (255,251,99) and the roof cream (255,243,232), BOTH R-clipped.  The
    board's own cream at (227,220,198) is NOT clipped and is usable; the red
    band sits between them and cannot be separated from its own highlight.  So
    the existing capred / interior_dark materials are used rather than new ones
    mixed to a clipped sample.  Rule 26: nothing here came off a green frame.

    WHICH LONG EDGE.  The bulbs are on the lower / near (show-side) edge, so
    this is the other one.  That much the frame does settle.
    """
    a = math.radians(TB_TILT_DEG)
    ey = TB_Y_CENTRE - TB_WIDTH * 0.5           # the far / upper long edge
    u = (-math.cos(a), 0.0, math.sin(a))
    out = []
    for name, t0, t1, tag in (("tb_edge_red", 0.5, 1.0, "RED, tip half"),
                              ("tb_edge_dark", 0.0, 0.5, "near-black, base half")):
        mid = (t0 + t1) * 0.5
        cx = base[0] + u[0] * TB_CHORD * mid
        cz = base[1] + u[2] * TB_CHORD * mid
        pts = T.rrect(TB_CHORD * (t1 - t0), TB_T + 0.004, 0.004, seg=3)
        ob = T.solid_prism((cx, ey, cz), u, (0.0, 0.0, 0.0) if False else
                           (-math.sin(a), 0.0, -math.cos(a)),
                           (0.0, 1.0, 0.0), pts, TB_BORDER, name=name)
        NOT_BODYWORK.add(ob.name)
        out.append((ob, tag))
    log("  rim band %.0f mm: RED over the tip half, near-black over the base "
        "half  [ARTWORK, ref_side.jpg only; colours are CLIPPED-frame ceilings]"
        % (TB_BORDER * 1000))
    return out


def tail_board_stay(base, log=print):
    """The single stay under the board.  MEASURED, and its TYPE is not.

    ONE, and only one is visible, and every figure here is expressed AGAINST
    THE BOARD rather than as a station, so it re-seats with the board's own
    depth ambiguity instead of going stale the moment the board moves (rule 2).
    What was measured on ref_side.jpg:

        top      about 0.13 m UP THE CHORD from the base
        landing  z 1.578, on the tail skin below the roof line
        angle    77-78 deg from horizontal, running down and FORWARD
        length   0.247 m visible

    ITS APPARENT DIAMETER IS 1-4 px (median 2) = 9 +- 7 mm, WHICH IS THE
    FRAME'S BLUR FLOOR.  A rod, a wire and the bulb string's own power cable
    cannot be separated there, and it FADES rather than terminating, so the
    landing point is where contrast is lost, not necessarily the foot.  It is
    built as a slender rod and that choice is DECLARED, not measured.  In
    IMG_2073 (GREEN -- geometry only) the member at this station is a
    substantial white PROP: corroboration that something structural is there,
    and NOT evidence for this vehicle's type.

    A SECOND STAY ON THE OFF SIDE WOULD BE INVISIBLE IN EVERY FRAME WE HOLD.
    None is built, because building one would be a claim.
    """
    a = math.radians(TB_TILT_DEG)
    up = 0.1300                                   # MEASURED, up the chord
    xa = base[0] - math.cos(a) * up
    za = base[1] + math.sin(a) * up - math.cos(a) * TB_T * 0.5   # its lower face
    ang = math.radians(77.5)                      # MEASURED 77-78 deg
    # THE LANDING IS MEASURED AT z 1.578 ON THE TAIL SKIN -- but that reading
    # belongs to a base at the near-edge height, and this board stands clear on
    # the roof (see tail_board()).  Run at the measured ANGLE and stop
    # *** rev 50: THE "80 mm" THAT USED TO STAND IN THAT SENTENCE IS WITHDRAWN
    # AND IS REMOVED HERE.  It was withdrawn at rev 49d and in SPEC 10.123.2a,
    # and rev 49d's commit says it "withdrew the declared 80 mm across the
    # record, not just the source" -- but this site was missed, and it was the
    # ONLY surviving one that stood as LIVE JUSTIFICATION rather than as record
    # (the mentions at :1602-1620 sit inside the block that ends "THE 80 mm FOOT
    # INCONSISTENCY DISSOLVES", so they read as history).  The built clearance is
    # `z0 = _seat + _hang + 0.0040`, i.e. 4.0 mm under the lowest corner -- the
    # withdrawn figure was 20x the real one, and it was the FIRST stated reason
    # in a comment block a future context reads to decide whether to re-seat this
    # stay.  Exactly the half-retraction shape rev 49's own ledger headlined. ***
    # where the rod MEETS THE ROOF, rather than driving it to a z that is now
    # inside the sheet metal.  A stay that ends inside the body is the same
    # class of defect as a foot that starts inside it.
    # THE LANDING IS THE TAIL SKIN, AND THE ANGLE IS WHAT IT COSTS.
    #
    # The measured stay runs 0.13 m up the chord, DOWN AND FORWARD at 77-78 deg,
    # to z 1.578 on the tail skin.  With the base SOLVED at X_TAIL+0.020 the
    # top sits 82 mm AFT of X_TAIL, and a 77.5 deg rod from there gains only
    # 57 mm of forward reach -- it stops short and HANGS IN MID-AIR.  Driving it
    # at the measured angle produced exactly that.
    #
    # THE TWO READINGS ARE IN DIFFERENT DEPTH PLANES (rule 16): the stay's
    # endpoints were read in the NEAR-FLANK plane, the station is solved in the
    # plane the board is built in.  Mixing them is the same error that put the
    # foot 97 mm inside the roof.  So the LANDING -- a hard geometric fact, the
    # rod ends ON the vehicle -- is honoured, and the ANGLE comes out and is
    # REPORTED against the measurement rather than forced to match it.
    zb = 1.5780                                   # MEASURED landing height
    xb = T.X_TAIL                                 # the tail skin
    _got = math.degrees(math.atan2(za - zb, abs(xb - xa)))
    r = 0.0045                       # 9 mm dia, the median of the blur-floor read
    wire = [(xa, TB_Y_CENTRE, za), (xb, TB_Y_CENTRE, zb)]
    ob = T.sweep(wire, [(r, r), (r, -r), (-r, -r), (-r, r)],
                 up=(0, 0, 1), name="tail_board_stay")
    NOT_BODYWORK.add(ob.name)
    log("  stay: (%.4f, %.3f) -> (%.4f, %.3f) ON THE TAIL SKIN, %.1f deg against a "
        "MEASURED %.1f (%+.1f) -- the residual is the SAME depth-plane ambiguity "
        "as the width, not a second defect; len %.3f m, dia %.0f mm [top DERIVED "
        "%.3f m up the chord; ROD vs WIRE NOT RESOLVED -- blur floor]"
        % (xa, za, xb, zb, _got, math.degrees(ang), _got - math.degrees(ang),
           math.hypot(xb - xa, zb - za), r * 2000, up))
    return ob


def tail_board_bulbs(base, tip, log=print):
    """The bulb string on the board's lower/show-side long edge.

    THE PITCH IS MEASURED AND THE COUNT IS NOT.  Along the board's edge the
    resolved bulbs give 6.15 +- 0.4 px = 28 +- 2 mm, which is statistically
    INDISTINGUISHABLE from the vehicle's own measured BULB_PITCH (28.6 +- 1.0
    mm) -- one circuit, one spacing, which is itself part of why this board is
    on the vehicle.  So the pitch is TAKEN FROM t1_detail.BULB_PITCH rather
    than retyped (rule 2), and the count falls out of it.

    ONLY SIX BULBS ACTUALLY RESOLVE.  An FFT along the edge returns no 6-px
    component -- the string is at the JPEG 4:2:0 Nyquist floor over most of its
    length.  The positive control is the vehicle's own rail string, where the
    same estimator returns 6.31 and 6.64 px against t1_detail sec.5.3's
    published 6.05-6.30.  So the count below is DERIVED from a measured pitch,
    and is NOT an observed count.  Rule 27: it prints what it derived.
    """
    import t1_detail as D
    n = int(round(TB_CHORD / D.BULB_PITCH))
    verts, faces, wire = [], [], []
    a = math.radians(TB_TILT_DEG)
    ey = TB_Y_CENTRE + TB_WIDTH * 0.5 + 0.004      # the show-side long edge
    for i in range(n + 1):
        t = i / n
        x = base[0] - math.cos(a) * TB_CHORD * t
        z = base[1] + math.sin(a) * TB_CHORD * t
        # hung just below the board's lower edge, on its own normal
        wire.append((x + math.sin(a) * 0.010, ey, z + math.cos(a) * 0.010))
        D._ball(verts, faces,
                (x + math.sin(a) * 0.020, ey, z + math.cos(a) * 0.020),
                D.BULB_R, nu=8, nv=5)
    me = bpy.data.meshes.new("tb_bulbs")
    me.from_pydata(verts, [], faces); me.validate()
    ob = bpy.data.objects.new("tb_bulbs", me)
    bpy.context.collection.objects.link(ob)
    T.fix_normals(ob)
    flex = T.sweep(wire, [(0.0026, 0.0026), (0.0026, -0.0026),
                          (-0.0026, -0.0026), (-0.0026, 0.0026)],
                   up=(0, 0, 1), name="tb_bulbflex")
    NOT_BODYWORK.update((ob.name, flex.name))
    log("  bulbs: %d DERIVED from BULB_PITCH %.4f m over a %.3f m chord "
        "[pitch MEASURED 28+-2 mm; COUNT NOT OBSERVED -- only 6 resolve]"
        % (n + 1, D.BULB_PITCH, TB_CHORD))
    return [ob, flex]


def open_rear_hatch(log=print):
    """Swing the glazed rear pane up and aft, so the upper bay stands open.

    Runs in build.py step 8c, AFTER the rake shear, for the same reason the
    trunk lid does: a lateral hinge moves v.co.x and step 8b shears on
    v.co.x.  Returns (hinge_x, hinge_z, deg) so anything mounted on the pane
    could be carried through the identical call.  Nothing is, today.
    """
    ob = bpy.data.objects.get("glass_rear")
    if ob is None:
        log("!! rear hatch NOT opened: glass_rear absent")
        return None
    co = [v.co for v in ob.data.vertices]
    hx = max(c.x for c in co)          # the pane's aft face, its hinge line
    hz = max(c.z for c in co)          # top-hinged, like the trunk lid
    _swing_open(ob, hx, hz, REAR_OPEN_DEG, "rear hatch", log=log)
    log("rear hatch: glass_rear hinged (x %.4f, z %.4f) lateral, OPEN %.1f deg"
        "  [angle NOT MEASURED -- no frame shows it]" % (hx, hz, REAR_OPEN_DEG))
    return hx, hz, REAR_OPEN_DEG


# Every part that has been swung out of the vehicle's closed envelope.
# Populated at run time by _swing_open() and by build.py's carried hardware, so
# verify.py can exclude them WITHOUT an enumerated list -- audit.py:96's stated
# reason for excluding lids by prefix rather than by name.  A list goes stale
# the moment somebody hangs a new part on a lid; this cannot.
SWUNG = set()

# Every part that is ON the vehicle but is NOT BODYWORK, and projects beyond
# the body's own envelope.  rev 49.
#
# WHY THIS EXISTS.  verify._bounds() excluded such parts with a HARD-CODED
# TUPLE -- ("cyc", "counter", "counter_nosing", "counter_top") -- while the
# same function's docstring argues at length that an enumerated list is the
# wrong shape because "a list goes stale the moment somebody hangs a new part
# on a lid".  It was right, and it went stale the moment rev 49 hung the tail
# board off the drip rail: the length row went red at +370 mm on a vehicle
# whose sheet metal had not moved.  Rule 5 -- do not inherit a guard's
# rationale along with its shape; here the rationale was sound and the shape
# contradicted it.
#
# The vehicle's SPEC length (4.055 m) is a measurement of its BODY.  A serving
# counter and a sign board are on the vehicle and are not its bodywork, in
# exactly the sense that an open lid is not its height.  Parts register
# themselves here; nothing enumerates them.
#
# AND WHAT IS DROPPED IS PRINTED, EVERY RUN (rule 27).  A cap nobody logs
# reads as coverage.
NOT_BODYWORK = set()


def _swing_open(ob, hx, hz, deg, what, log=print):
    """Swing a top-hinged tail panel open, and PROVE it went the right way.

    Shared by the trunk lid and the rear hatch so the two cannot drift apart:
    a guard that is written twice is a guard that gets fixed once.

    The panel's LOWEST vertex is its free edge -- the one that has to travel.
    Measured before and after, so this tests the MOTION, not the code.

    Capture the INDEX as a plain int, not the bpy struct.  _hinge_y mutates the
    mesh and calls fix_normals, after which the struct is stale and `.index`
    reads garbage -- the first version of this guard died with
    `bpy_prop_collection[-1425949424]: out of range` instead of reporting the
    defect it was written to catch.  A guard that crashes is not a guard.

    WATCHED FAIL (rule 19), sign inverted, run and read:
        AssertionError: trunk lid opened the WRONG WAY: its free edge moved
        dx +0.3850 dz +0.1878
    and the build stops.  The first draft of this comment GUESSED
    "dx +0.1946 dz +0.0546" from arithmetic instead of running it -- wrong on
    both figures.  Rule 4: never put a figure in an acceptance test unless you
    watched it print.  This one is watched.
    """
    me = ob.data
    low_i = int(min(me.vertices, key=lambda v: v.co.z).index)
    x0, z0 = float(me.vertices[low_i].co.x), float(me.vertices[low_i].co.z)
    _hinge_y(ob, hx, hz, deg)
    T.fix_normals(ob)
    dx = float(me.vertices[low_i].co.x) - x0
    dz = float(me.vertices[low_i].co.z) - z0
    if not (dx < -1e-4 and dz > -1e-4):
        raise AssertionError(
            "%s opened the WRONG WAY: its free edge moved dx %+.4f dz %+.4f. "
            "A top-hinged tail panel's free edge swings AFT (dx negative) and "
            "UP (dz non-negative). Check _hinge_y's sign -- it was inverted "
            "once already and only a render caught it." % (what, dx, dz))
    SWUNG.add(ob.name)
    log("  %s free edge travelled dx %+.4f m (aft) dz %+.4f m (up) -- guard ok"
        % (what, dx, dz))
    return dx, dz


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
    #
    # SKIPPED WHEN SHUT, not run at zero.  _swing_open() asserts the free edge
    # actually travelled (dx aft, dz up); at 0 deg nothing moves and the guard
    # would fire on a lid that is correctly closed.  A guard must fire on the
    # DEFECT, not on a legitimate pose.
    if abs(TRUNK_OPEN_DEG) < 1e-6:
        log("trunk lid: separated %dv, hinge (x %.4f, z %.4f) lateral, "
            "**SHUT** -- the owner's ruling at rev 49: \"leave the lower bay "
            "shut, just have the back trunk window open for service\".  Rev 48 "
            "inferred the opposite from \"the MAIN bay\" and shipped it."
            % (len(lm.vertices), hx, hz))
        return lid, hx, hz, 0.0
    _swing_open(lid, hx, hz, TRUNK_OPEN_DEG, "trunk lid", log=log)

    log("trunk lid: separated %dv, hinge (x %.4f, z %.4f) lateral, "
        "OPEN %.1f deg  [angle NOT MEASURED -- no frame shows it]"
        % (len(lm.vertices), hx, hz, TRUNK_OPEN_DEG))
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

    # GUARD, SAME EDIT AS THE CHANGE (rule 12) -- rev 50, A1.
    # THE BOARD MUST LEAN OVER THE COUNTER.  Measured on the BUILT panel, not on
    # LID_OPEN_DEG, so it tests the shipped geometry and not the constant that
    # produced it (rule 32): the free edge is the panel vertex furthest from the
    # hinge in y, and it must lie on the SHOW side (+y) of the hinge.
    # WATCHED FAIL on T1_LIDDEG=104 -- the pre-rev-50 pose -- which reports
    #   "the mural lid leans AWAY from the counter: free edge at y=-0.8135,
    #    0.2685 m on the OFF side of the hinge at y=-0.5450"
    # The free edge is the panel's TOPMOST vertex: the lid rotates up about a
    # fore-aft axis, so whichever end is highest is the end away from the hinge.
    # Its y is the whole of the observable -- ref_side.jpg's taper says the TOP
    # of the board is nearer the SHOW side, so this vertex's y must exceed the
    # hinge's.  Reading z to find it and y to test it means the guard cannot be
    # satisfied by the same expression that positioned it.
    _top = max(main.data.vertices, key=lambda v: v.co.z)
    assert _top.co.y > LID_Y_HINGE + 0.010, (
        "SPEC 10.135 / AUDIT_rev43:117: the mural lid leans AWAY from the "
        "counter -- its free edge is at y=%.4f, %.4f m on the OFF side of the "
        "hinge at y=%.4f.  ref_side.jpg's board tapers -5.3 +- 0.6 %% "
        "top-to-bottom, so the TOP is nearer the show side, and in "
        "ref_rear34.jpg and IMG_2073 the stay passes IN FRONT of the painted "
        "face.  LID_OPEN_DEG must be < 90."
        % (_top.co.y, LID_Y_HINGE - _top.co.y, LID_Y_HINGE))

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
    # rev 59, ITEM 1 -- THE 30 mm INSET IS DROPPED AT THIS CALL SITE ONLY.
    # `_lid_face`'s DEFAULT stays 0.030 because `signboard()` shares it; this
    # is a call-site override, not a change of the function's contract.
    #
    # THE TWO FILES DISAGREED ABOUT WHAT THE TEXTURE'S BORDER MEANS.
    # `lid_gen.py` traces the OUTER EDGE OF THE YELLOW STRIPS as the board
    # boundary, i.e. the image already runs to the panel edge; this call then
    # treated that same edge as 30 mm INBOARD of the panel.  The 30 mm was
    # applied on all four sides of a 2.0340 x 1.2237 m panel -- 1.47 % of the
    # length but 2.45 % of the width -- so it did two things at once:
    #   * a bare-cream border all round that ref_side.jpg does not have
    #     (a thin specular lip on the top and right edges only, <= 0.4 % of
    #     the board's height at 6 columns, against 3.7 % rendered);
    #   * it STRETCHED the printed image along the vehicle.  Decal quad
    #     1.9740 x 1.1637, aspect 1.6963, against tex/lidmural.png's authored
    #     2048 x 1238 = 1.6543 -> +2.54 % along X.  At inset 0.0 the quad is
    #     2.0340 x 1.2237 = 1.6621 and the residual stretch is +0.47 %.
    # Both figures recomputed from LID_X0/LID_X1/LID_ASPECT/LID_OPEN_DEG here,
    # not transcribed.
    #
    # THE BOARD'S SIZE IS A SEPARATE, OPEN FINDING AND IS NOT TOUCHED HERE:
    # LID_W, LID_X0, LID_X1 and LID_ASPECT are all unchanged.
    #
    # T1_LIDINSET restores the old value so the border can be WATCHED coming
    # back -- the ablation for this item.
    _LID_INSET = float(os.environ.get("T1_LIDINSET", 0.0))
    b = _lid_face(LID_X0, LID_X1, LID_W, "lid_board",
                  inset=_LID_INSET, off=-(LID_T + 0.0016))
    _decal_aspect_guard(b)
    _hinge(b, 0.0, LID_Y_HINGE, zh, LID_OPEN_DEG)
    boards.append(b)

    # perimeter rail: the shallow frame the skin sits on, standing PROUD of the
    # roof by the measured 26 +/- 7 mm. ref_workshop.jpg shows the open lid is
    # the cut-out roof skin on a rail, not a box.
    # rev 56 -- THIS BUILT TWO EMPTY OBJECTS FOR FOUR REVISIONS.  The loop ran
    # (LID_X0, LID_X0) and (LID_X1, LID_X1), and _rag_grid interpolates
    # x = x0 + (x1-x0)*ix/nx, so x0 == x1 put every vertex at ONE station:
    # both objects measured 0.000000000 m2 with 18 of 18 faces degenerate and
    # a bbox dx of exactly 0.000000.  The rail the comment above describes was
    # in no render.  Grepping for the object name found it -- it was built, it
    # was just empty, which is rule 10 exactly.
    #
    # It was left EXEMPT rather than fixed because the rail's WIDTH was
    # measured nowhere and inventing one puts a visible member on the roof at
    # a size no photograph supports.
    #
    # THE OWNER RULED IT, rev 56, off the marked crop of ref_workshop.jpg
    # (probe_scratch/rev56_ASK_lidrail.png -- the aft end of the roof opening,
    # multiple choice): "Narrow lip, ~as wide as it is tall".  So the width IS
    # the proud height, and it is not a second free constant -- it is
    # RAIL_PROUD itself, which is why this reads RAIL_PROUD and not a literal.
    # ref_workshop.jpg is the GREEN vehicle: this is GEOMETRY, which rule 11
    # says transfers, and no paint or artwork is taken from it.
    #
    # Both rails run INBOARD of the opening's own edges -- the frame the skin
    # sits ON, so it cannot poke out past the aperture it closes.
    # T1_RAILFLAT=1 restores the rev-52..55 defect (xa == xb, zero area) so
    # the new width guard and the zero-area sweep can both be WATCHED FAILING
    # on the thing they exist to catch.
    RAIL_W = 0.0 if os.environ.get("T1_RAILFLAT") == "1" else RAIL_PROUD
    for (xa, xb) in ((LID_X0 - RAIL_W, LID_X0), (LID_X1, LID_X1 + RAIL_W)):
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
    # rev 50, A1 -- AND THE FOOT HAD TO MOVE WITH THE LEAN.  This is recorded at
    # length because it re-opens ground rev 44b settled ON THE OWNER'S WORDS, and
    # the next context must be able to see exactly what was and was not re-opened.
    #
    # With LID_OPEN_DEG corrected from 104 to 76 the free edge moves from
    # y = -0.8135 (beyond the OFF-side roof edge, where a near-vertical prop
    # could stand under it) to y = -0.2765, which is INSIDE the roof aperture
    # (-0.5450 .. +0.5650).  A prop dropped straight down from there stands on
    # the open hatch, and rev 45's own guard below says so and fires.  So the
    # foot must sit on one of the two surviving roof strips, and the prop rakes.
    #
    # WHICH STRIP: the SHOW side.  In ref_rear34.jpg (RED, target, current
    # artwork) and IMG_2073.jpeg (GREEN -- geometry, so it transfers) the support
    # rod passes IN FRONT OF the painted face, i.e. between the camera and the
    # board, and both cameras are on the show side.  A rod in front of the face
    # has its foot on the show side.  This needs no scale and no camera model.
    #
    # WHAT THIS DOES NOT RE-OPEN.  The owner's rev-37/44b complaint, verbatim,
    # was *"the props for the sign seem to meet something from the SIDES of the
    # sign, rather than the sign resting directly on the poles."*  Rev 44b
    # diagnosed that correctly as a TIP problem -- the tip met the board at 0.86
    # of its width, near its top edge -- and fixed it by moving the tip to 0.97,
    # onto the FREE EDGE, the edge that actually bears.  THAT FIX IS KEPT
    # UNCHANGED below.  What rev 44b also did, on its own initiative and not on
    # his instruction, was move the FOOT outboard so the rod stood at 3 deg from
    # vertical; that was only possible because the board was leaning the wrong
    # way, and it is what is being undone here.  The rod still meets the board at
    # the bearing edge, which is what he asked for.
    def _roof_edge_y(xr, y0, step):
        """Walk roof_z along y until it stops changing -- the roof's OWN edge.

        `step` is signed, so this finds the OFF-side edge (negative) or the
        SHOW-side edge (positive).  Measured off the body rather than typed.
        """
        y = y0
        for _ in range(600):
            y2 = y + step
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
        # rev 50: the foot goes on whichever surviving roof strip the board
        # LEANS OVER, walked out to the roof's own edge.  a < 90 -> the free
        # edge is on the show side of the hinge -> show-side strip, walking +y
        # from the aperture's show edge.  a > 90 (the pre-rev-50 pose) -> the
        # off-side strip, walking -y from the hinge, which is what rev 44b did.
        # DERIVED FROM THE POSE, not typed, so the foot follows the angle.
        if math.cos(a) > 0.0:
            footy = _roof_edge_y(xs, LID_Y_HINGE + w, +0.002)
        else:
            footy = max(tipy, _roof_edge_y(xs, LID_Y_HINGE, -0.002))
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
        # rev 50 -- THIS GUARD IS RE-SCOPED, NOT RELAXED, AND HERE IS WHY.
        #
        # rev 44b wrote `lean < 20.0` to catch a prop that "rakes across the roof
        # instead of standing under the board".  It was a PROXY.  The owner's
        # actual words were about WHERE THE PROP MEETS THE BOARD -- "they meet
        # something from the SIDES of the sign, rather than the sign resting
        # directly on the poles" -- and the thing that fixed that was moving the
        # TIP to 0.97 of the width, onto the bearing edge.  The lean was only
        # ever small because the board was leaning the WRONG WAY (a = 104), which
        # put its free edge outboard of the roof where a vertical rod could stand.
        # With the lean corrected to a = 76 the free edge sits over the open
        # aperture, so no admissible prop can be near-vertical: `lean < 20` and
        # rev 45's foot-outside-the-aperture guard became jointly unsatisfiable.
        # A guard that cannot be satisfied by any correct build is not a guard.
        #
        # MY FIRST ATTEMPT AT THIS REPLACEMENT WAS ITSELF A TAUTOLOGY AND THE
        # BUILD CAUGHT IT.  I derived a bound `_lean_max` from the ROD'S OWN
        # min/max y and z and then compared the rod's lean to it -- one
        # expression checked against itself, rule 32, in the same edit that
        # cites rule 32.  It aborted with "leans 42.2 deg, past the 5.3 deg its
        # own foot and tip allow", because with the foot now on the show side
        # `min(v.y)` is the TIP end, not the foot.  Recorded rather than quietly
        # replaced: it is the fourth instrument defect this project has caught in
        # its own guard-writing in five revisions.
        #
        # WHAT REPLACES IT READS THE BUILT BODY, not the rod's own extents.
        # (1) THE FOOT MUST BE ON THE SIDE THE BOARD LEANS TOWARD.  This is what
        #     actually forbids "raking across the roof", and it reproduces rev
        #     44b's catch exactly: at a = 104 the free edge was at y -0.8135, the
        #     OFF side of the hinge, while the offending foot was at y +0.44, the
        #     show side -- opposite sides, so this fires.
        _free_y = LID_Y_HINGE + w * math.cos(a)
        _foot_v = min(vs, key=lambda v: v.z)
        _tip_v = max(vs, key=lambda v: v.z)
        assert ((_foot_v.y - LID_Y_HINGE) * (_free_y - LID_Y_HINGE)) > 0.0, (
            "roof-lid prop foot at y=%.4f is on the OPPOSITE side of the hinge "
            "(y=%.4f) from the board's free edge (y=%.4f) -- it reaches across "
            "the opening instead of carrying the board (SPEC 10.108, owner rev "
            "37/44b)." % (_foot_v.y, LID_Y_HINGE, _free_y))
        # (2) THE ROD MUST NOT PASS THROUGH THE ROOF.  Sampled along the built
        #     rod against `roof_z`, i.e. the rod against the body it stands on --
        #     two independently obtained quantities.  This is the physical
        #     content of "does not rake across the roof", and unlike a lean
        #     threshold it stays correct at any opening angle.
        _f = Vector((_foot_v.x, _foot_v.y, _foot_v.z))
        _t = Vector((_tip_v.x, _tip_v.y, _tip_v.z))
        for _i in range(1, 20):
            _p = _f + (_t - _f) * (_i / 20.0)
            assert _p.z > roof_z(_p.x, _p.y) - 0.0075, (
                "roof-lid prop passes THROUGH the roof at (%.3f, %.3f, %.3f): "
                "roof is at z=%.4f there (SPEC 10.108, re-scoped rev 50)."
                % (_p.x, _p.y, _p.z, roof_z(_p.x, _p.y)))
        # THE TIP MUST BEAR ON THE FREE EDGE.  This is the owner's rev-37/44b
        # ruling expressed directly instead of through the lean proxy.
        _free = Vector((xs_, LID_Y_HINGE + w * math.cos(a),
                        zh + w * math.sin(a)))
        _miss = (Vector((_tip_v.x, _tip_v.y, _tip_v.z)) - _free).length
        assert _miss < 0.045, (
            "roof-lid prop tip misses the board's FREE EDGE by %.1f mm -- the "
            "board is not resting on the pole (owner, rev 37/44b)." % (_miss * 1e3))
    # GUARD, SAME EDIT AS THE CHANGE (rule 12).  Every prop foot must sit on
    # solid roof -- OUTSIDE the aperture's y band -- or the prop is standing in
    # the hatch again.  The band is the lid's own closed footprint.
    #
    # rev 50 -- ITS RATIONALE IS KEPT AND ITS SHAPE IS CORRECTED (rule 5).
    # It identified the foot as `min(v.co.y)`, which is the foot ONLY while the
    # prop stands on the OFF side, i.e. only while the board leans the wrong way.
    # With a = 76 the foot is at y +0.7273 and the TIP is the minimum y (-0.2899),
    # so the guard read the tip as the foot and aborted on a correct build:
    #   "prop foot at y=-0.2899 is INSIDE the roof aperture (-0.5450..0.5650)"
    # A foot is the LOWEST point of a rod, which is true at any opening angle, so
    # that is what it now reads.  The test itself -- foot outside the aperture's
    # y band -- is unchanged, and it still fires on the rev-45 defect it was
    # written for (a foot at y +0.44 with the aperture -0.545..+0.565).
    _y_lo, _y_hi = LID_Y_HINGE, LID_Y_HINGE + LID_W
    for _st in struts:
        _fv = min(_st.data.vertices, key=lambda v: v.co.z)
        _fy = _fv.co.y
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
V_POW_Z = 0.52
# rev 60 -- T1_VPOWZ, the PRESSED SWAGE's half of the T1_VPOW ablation.  The
# literal above stays on its own line: verify_clone.sh greps `^V_POW_Z = 0.52`
# (0.52 since rev 61 -- F77 fitted the exponent POSE-INVARIANTLY on three
# frames at 0.517 / 0.521 / 0.531, with a render control recovering 0.600 to
# +/-0.02.  The old 0.60 was refuted only behind a BROKEN gate; see F135.)
# and t1_mats' V_POW is pinned to agree with it.  Set BOTH env vars to the same
# value to move paint and swage together and keep verify.py's registration row
# satisfied; set one alone and that row must FAIL, which is the point.
if os.environ.get("T1_VPOWZ"):
    V_POW_Z = float(os.environ["T1_VPOWZ"])           # == t1_mats.V_POW.  < 1: the profile is CONCAVE.
V_HALF_W = 0.86

# ------------------------------------------------------------- rev 67, F207
# THE NOSE'S PLAN BULGE -- the forward convexity of the vehicle's whole face,
# and until rev 67 it had never been measured, ablated or guarded.  It is the
# ONE constant that answers the owner's *"we still have work to do on the shape
# of the nose"* (F197) and rev 51's FLAT NOSE found by eye.
#
# It stays on its own line as a bare literal so a verifier row can grep
# `^NOSE_BULGE = 0.019`.  T1_NOSE_BULGE scales it and is MEASUREMENT-ONLY: it
# is `probe_rev67_nose.py`'s kill, and setting it to 0 must collapse the plan
# bulge M1 reports.  A control is finished when you have WATCHED IT FAIL.
#
# WHY A SIDE ELEVATION CANNOT CHECK THIS.  In a side view the silhouette at
# each height is max-over-y of x, which for a plan-convex nose is ALWAYS the
# centreline -- whether this constant is 0.019 or 0.0.  The axis is invisible
# there by construction, which is why fifteen revisions of nose work never
# touched it.
NOSE_BULGE = 0.019
if os.environ.get("T1_NOSE_BULGE"):
    NOSE_BULGE = float(os.environ["T1_NOSE_BULGE"])


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
        bulge = NOSE_BULGE * w * max(0.0, 1.0 - r)
        d = z - zV(y)
        s = 0.5 * (1.0 + math.tanh(d / 0.016))
        step = -0.0062 * w * (1.0 - s)
        v.co = Vector((x + bulge, y, z)) + v.normal * step
    bm.to_mesh(me); bm.free()
    me.update()
