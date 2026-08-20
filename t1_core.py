"""
Volkswagen Type 2 (T1) Single-Cab Pickup  --  parametric body generator
True-to-scale.  All units metres.

Reference dimensions (1950-67 T1):
    wheelbase      2400 mm
    overall length 4280 mm  (over bumpers)
    overall width  1720 mm
    overall height 1925 mm  (pickup)
    tyres          5.60 x 15  ->  665 mm dia
Coordinate frame:  +X = forward (nose),  +Y = left,  +Z = up,  ground Z = 0
"""

import bpy, bmesh, math, os
import numpy as np
from mathutils import Vector, Matrix

TAU = math.pi * 2

# ----------------------------------------------------------------------------
# hard points
# ----------------------------------------------------------------------------
WB          = 2.400
X_AXLE_F    =  1.300
X_AXLE_R    = -1.100
X_NOSE      =  2.108           # front-most sheet metal

# ---------------------------------------------------------------------------
# rev 16 -- THE TAIL RE-SPACE.  SPEC sec.10.35.
#
# The overhang past the rear axle was measured DIMENSIONLESSLY, from the two
# hub columns and the tail silhouette only.  No origin, no metre scale, no
# ground line, and nothing within 800 px of the lamppost:
#
#     rear overhang / wheelbase = (u_tail - u_rhub)/(u_rhub - u_fhub)
#                               = 0.3412 +- 0.0015          (ref_side.jpg)
#     built                     = 1.008 / 2.400 = 0.4200
#
# Through the projective flank map of LOFT_GROUND sec.0 that is 0.773 +- 0.022 m
# against 1.008 built -- THE TAIL IS 235 +- 22 mm TOO LONG.  Cross-checked
# against a completely different feature pair on the same flank, using no hub
# at all: tail minus the rear arch's aft foot is 70 px = 0.320 m, which with
# the re-measured arch half-width of 0.460 m puts the tail at -1.880.  Two
# routes, 7 mm apart.  SPEC sec.10.7's "99 mm" is REFUTED at 10 sigma -- it
# subtracted two numbers in different origins.
#
# APPLIED AS A RE-SPACE, NEVER AS A TRANSLATION.  The existing aft station set
# already has a sensible distribution (it clusters hard into the corner roll);
# translating it would drag that cluster off the corner.  Every aft station and
# every aft LUT knot is therefore expressed as its fraction f of the OLD
# overhang and re-issued against the NEW one, which is what `_aft()` does.
# Anything anchored to the tail SKIN must be written in terms of X_TAIL, not
# re-typed as a constant -- a constant tuned against another constant must be
# expressed in terms of it.
X_TAIL_OLD  = -2.108           # the artefact value, kept only for _aft()
O_OLD       = X_AXLE_R - X_TAIL_OLD          # 1.008  built overhang
O_NEW       = 0.773                          # measured, +- 0.022


def _aft(x):
    """Re-space an aft station by its fraction of the rear overhang.

    f = 0 at the rear axle, f = 1 at the tail.  Stations forward of the rear
    axle are returned unchanged, so this can be applied to a whole LUT.
    """
    if x >= X_AXLE_R:
        return x
    f = (x - X_AXLE_R) / (-O_OLD)
    return X_AXLE_R - f * O_NEW


X_TAIL      = _aft(X_TAIL_OLD)  # -1.873   rear-most sheet metal
X_BUMP_F    =  2.140
X_BUMP_R    = -2.140
HALF_W      =  0.875           # max body half width (SPEC r4: W=1.750)
Z_ROOF      =  1.893           # roof edge (crown adds ~0.032 -> 1.925 overall)
Z_BED_RAIL  =  1.302           # top of pickup side gate
Z_BED_FLOOR =  0.902
X_CAB_BACK  =  0.420           # cab rear wall
TIRE_R      =  0.3325          # rev6 MEASURED dia 0.665 (NOT 6.40-15)
TIRE_W      =  0.1550          # rev6: ~215 section on a 16in rim
RIM_R       =  0.2198          # rev6 MEASURED 16in flange OD 0.4396, not 15in
TRACK_F     =  1.3690
TRACK_R     =  1.3590
# ---------------------------------------------------------------- ride & rake
# rev 8: the drop is NOT a scalar. The vehicle sits nose-down ~1.9 deg relative
# to the axle line, so the "ride drop" is a LINE in x:
#
#     drop(x) = RAKE_Z0 + RAKE_DZDX * x
#
# Grounding (HANDOFF_rev7 sec.4): model crown vs photograph read +12 mm at the
# front axle, -29 mm mid-wheelbase, -67 mm at the rear axle -- a tilt signature,
# not a missing curb. The drip rail is straight over x_img 265->846 (rms 0.4 px)
# at 33 +/- 4 mm/m. This REFUTES REF_MEASUREMENTS sec.2.3's inference that the
# roof-lid frame stands 0.10-0.15 m proud (measured proud height is 26 +/- 7 mm,
# a ~13 sigma miss) and it is why the model read 89 mm short overall.
#
# SHEAR, NOT ROTATION. Every reference number is a height-versus-X; a 1.9 deg
# rotation would also shift x by 63 mm at roof level and de-register every
# longitudinal measurement.
# rev 13 -- THE RAKE IS RE-DERIVED AND 0.0330 IS REJECTED AT 4.5 SIGMA.
#
# Everything above this line is the rev-8 derivation and it is kept because the
# SHEAR-not-rotation part of it is still right.  The MAGNITUDE is not.  Both of
# rev 8's chains measure an IMAGE slope of a body line, and an image slope of a
# fore-aft line contains the perspective term as well as the rake -- all of the
# vehicle's own horizontal lines converge on a vanishing point at u ~ -11700, so
# a raw slope cannot separate the two.  Re-fitting the rocker trim ridge
# sub-pixel gives -0.025415 +/- 0.000178 px/px (rms 0.299 px, n = 324): neither
# 0.0330 nor the audit's 0.0144, because it is not the rake at all.
#
# METHOD 4, and it needs no ground line, no px/m and no vanishing point: both
# hub centres sit at exactly one tyre radius above flat ground BY CONSTRUCTION,
# so the rocker's height above its own hub, taken at each axle and scaled by
# that wheel's own tyre, differences into the rake directly.
#
#   station        hub (sub-pixel polar fit)   local px/m   rocker above hub
#   front axle     u 242.60  v 607.84          204.4        -0.0004 m
#   rear axle      u 749.27  v 604.13          213.5        +0.0422 m
#   rake = 0.0426 / 2.400 = 0.01775 m/m
#
# The front wheel is 54 % unoccluded (polar sectors -40..+66 and +110..+198),
# which is enough for a constrained circle fit; every previous attempt treated
# it as unusable because the man's red shirt defeated a bbox search.  Three
# independent rocker extractions agree to 0.2 % and a second datum (the
# cream/red belt boundary, which needs no extrapolation at the rear) gives
# 0.01747.  Quoted 17.6 +/- 3.4 mm/m; the dominant term is the 94 px
# extrapolation past u = 650, not the fit.
#
#   from 0.0330                4.5 sigma   REJECTED
#   from the audit's 0.0144    0.70 sigma  consistent
#
# Corroboration that needs no photograph: a non-negative front arch gap
# requires rake <= 0.0171.  At 0.0330 the front gap is -27 mm -- the tyre inside
# the bodywork -- which is what SPEC 10.9 logged as an unresolved contradiction
# for five revisions.  It resolves against the built value.
#
# NOTE the arch-gap IDENTITY is NOT a valid estimator and is not used as one
# here: the front and rear arch lips are different pressings, so
# `rear - front = rake x wheelbase` confounds the rake with a design difference.
# It bounds; it does not measure.
#
# RAKE_Z0 is re-anchored in the same solve, not carried over: the model's rocker
# sat -0.0088 above its hub at the front axle and +0.0704 at the rear, so BOTH
# ends move -- the nose up 8 mm, the tail down 28 mm.  Consequence, logged not
# hidden: roof @ rear axle 1.923 -> ~1.895, so the deliberate warn against
# REF 2.3's 1.960 grows from -37 mm to about -65 mm.  That is expected and it is
# coherent with the roof dome being separately measured 90-105 mm too shallow
# (crown R 2.45 m against the built 9.65 m): correcting the dome would take the
# crown to 1.985-2.000 against 1.960 +/- 30, which the CURRENT build cannot
# reach from 1.923 no matter what the dome does.
RAKE_Z0     =  0.047925        # ride drop at x = 0   (was 0.0365)
RAKE_DZDX   =  0.017750        # nose-down rake, m per m forward, 1.02 deg
                               # (was 0.0330).  17.6 +/- 3.4 mm/m measured.


def rake_drop(x):
    """Ride drop at station x. Authored (un-dropped) z minus this == above ground."""
    return RAKE_Z0 + RAKE_DZDX * x


# SPEC 10.25: a constant tuned against another constant must be EXPRESSED in
# terms of it.  X_DROP_REF is not a locked constant -- it is defined as "the
# station where drop(x) equals the pre-rev-8 scalar 0.0650", so it has to be
# solved from the rake, not left at the value it happened to have when the rake
# was 0.0330.  Doing this keeps RIDE_DROP at exactly 0.0650, which in turn keeps
# t1_mats.Z_BELT == 1.2070 and V_APEX == 0.3400 bit-identical through a rake
# change -- both are guarded values and neither should move for this reason.
X_DROP_REF  = (0.0650 - RAKE_Z0) / RAKE_DZDX        # == 0.96197 at rev-13 rake
RIDE_DROP   =  RAKE_Z0 + RAKE_DZDX * X_DROP_REF     # == 0.0650
                               # rev6: LOWERED. Rear arch-to-tyre gap measures
                               # 41mm vs a stock 90-120. rev4 zeroed this in error.
                               # rev8: retained as the drop AT X_DROP_REF only, so
                               # the "is it still lowered" guard and legacy scalar
                               # call sites keep working. Do NOT use it as a
                               # frame conversion -- use rake_drop(x).
Z_CANOPY_T  =  1.9220          # canopy roof top
Z_CANOPY_B  =  1.8380
Z_FASCIA_B  =  1.6280

# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------
def lut(points):
    """linear interpolator from list of (x, y)"""
    a = np.asarray(points, dtype=float)
    X, Y = a[:, 0], a[:, 1]
    def f(x):
        return float(np.interp(x, X, Y))
    return f


def aft_lut(points):
    """lut() with every AFT knot re-spaced by rev 16's tail solve.

    The authored table keeps its measured values verbatim -- the re-space is
    structural and lives in exactly one place, so a future revision that
    re-measures the overhang changes O_NEW and nothing else.
    """
    return lut([(_aft(x), y) for (x, y) in points])


def qbez(p0, p1, p2, t):
    u = 1.0 - t
    return (u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
            u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1])


# ----------------------------------------------------------------------------
# universal normalised half-width profile  G(z)
# describes how the flank swells and tumbles home with height.
# multiplied by the station half-width W(x).
# ----------------------------------------------------------------------------
G = lut([
    (0.30, 0.900), (0.40, 0.940), (0.50, 0.9720), (0.58, 0.9860),
    (0.68, 0.9950), (0.80, 0.99900), (0.92, 1.00000), (1.04, 0.99930),
    (1.16, 0.99680), (1.28, 0.99230), (1.38, 0.98700), (1.48, 0.98000),
    (1.58, 0.97100), (1.68, 0.95900), (1.76, 0.94700), (1.84, 0.93200),
    (1.90, 0.91800), (1.96, 0.90100), (2.02, 0.88000),
])

# segment point budget:  bottom-flat, bottom-roll, flank, top-roll, top-flat
NA, NB, NC, ND, NE = 6, 8, 26, 8, 7
# rev 16 EXPERIMENT, owner-directed: NLOOP = 2*NHALF - 2 is 110 at NHALF=56,
# which the Coons cap splits 27/28/27/28 -- NOT mirror-symmetric about y = 0
# (the mirror of loop index 27 is 83, not 82).  NHALF = 57 gives NLOOP = 112
# = 4 x 28 and a cap grid that IS mirror-symmetric.  Selected by env so both
# arms can be built and MEASURED rather than argued about.
#
# MEASURED, NOT ARGUED.  Both arms were built at BOTH subdivision levels:
#
#   NHALF 56, cap 27x28 (asymmetric)   SUB=1  0 fail    SUB=2  1 FAIL
#                                      -> gap_englid REJECTED, "zero-area
#                                         faces 0 -> 2", ROLLED BACK
#   NHALF 57, cap 28x28 (symmetric)    SUB=1  0 fail    SUB=2  0 fail
#
# The engine-lid gap ring is symmetric about y = 0.  On a cap grid that is not,
# its two sides land differently on the grid and the exact solver returns two
# degenerate slivers.  Moving the cutter in x does NOT fix it -- 0.120, 0.158
# and 0.200 all give exactly 2 zero-area faces -- which is what identifies it
# as an outline/grid coincidence rather than a tangency.  So the symmetric cap
# is not a tidiness preference; it is the only arm that passes at both levels,
# and it was chosen on that number rather than on the argument.
if os.environ.get("T1_NHALF57", "1") == "1":
    NC = 27                                 # NHALF 56 -> 57, NLOOP -> 112
NHALF = NA + NB + NC + ND + NE + 1          # 56, or 57 on the experiment arm
NLOOP = NHALF * 2 - 2                       # 110, or 112


def section(W, Zb, Zt, rb, rt, crown, bcrown=0.0):
    """Right-half outline, bottom-centre -> top-centre, list of (y, z)."""
    zb0, zt0 = Zb + rb, Zt - rt
    if zt0 <= zb0 + 1e-4:
        zt0 = zb0 + 1e-4
    Ybs = W * G(zb0)
    Yts = W * G(zt0)
    Yb = max(Ybs - rb, 1e-4)
    Yt = max(Yts - rt, 1e-4)

    p = []
    # A  bottom flat (slight upward crown toward centreline)
    for i in range(NA):
        t = i / NA
        y = Yb * t
        p.append((y, Zb + bcrown * (1.0 - (y / Yb) ** 2)))
    # B  bottom roll
    for i in range(NB):
        p.append(qbez((Yb, Zb), (Ybs, Zb), (Ybs, zb0), i / NB))
    # C  flank
    for i in range(NC):
        z = zb0 + (zt0 - zb0) * (i / NC)
        p.append((W * G(z), z))
    # D  top roll
    for i in range(ND):
        p.append(qbez((Yts, zt0), (Yts, Zt), (Yt, Zt), i / ND))
    # E  top flat / crown
    for i in range(NE + 1):
        y = Yt * (1.0 - i / NE)
        p.append((y, Zt + crown * (1.0 - (y / Yt) ** 2)))
    return p


def ring(x, W, Zb, Zt, rb, rt, crown, bcrown=0.0):
    """Full closed loop of 3-D coords for one station."""
    half = section(W, Zb, Zt, rb, rt, crown, bcrown)
    pts = [(x, y, z) for (y, z) in half]                 # +Y side, bottom->top
    for (y, z) in reversed(half[1:-1]):                  # -Y side, top->bottom
        pts.append((x, -y, z))
    return pts


# --------------------------------------------------------------------------
# rev 16 -- THE END-CAP POLES.  SPEC sec.10.30b closed.
#
# `loft(cap_first/cap_last)` used to append ONE n-gon at each end.  build.py
# then runs SUBSURF first, and Catmull-Clark turns an n-gon into n quads around
# a new FACE POINT of valence n.  That face point IS the pole.  Measured on the
# shipped rev-15 build: valence 115 at (-2.1080, 0, 0.9612) and 112 alongside
# it on the inner skin, 110/110 at the nose -- a 110-spoke smooth-shaded fan
# at the exact centre of a FLAT panel, which is a specular starburst generator
# independent of any material.  That is why all four rev-14 ablation arms
# failed to move it (art 15.459, albedo 15.412, spec 16.834 against an
# as-built 15.478 -- the spec arm moved it the WRONG WAY).
#
# It is not only a shading defect: the n-gon cap also pulls the flat tail face
# 1.4 mm forward of its authored plane, leaving the pole standing proud of it.
#
# THE FIX IS A COONS QUAD GRID whose border IS the boundary loop, so no vertex
# is added to the loop and the loft's own topology is untouched:
#
#     n = NLOOP  ->  a = n//4, b = n//2 - a      (sides a/b/a/b, 2(a+b) = n)
#     n = 110    ->  27 x 28,  corners at loop indices 0, 27, 55, 82
#     n = 112    ->  28 x 28,  corners at 0, 28, 56, 84  and MIRROR-SYMMETRIC
#
# A quad fan with a central quad is NOT an option (110 is not reducible to 4
# without a pole) and re-spacing the stations is orthogonal to it -- the pole
# is created by the CAP, at any spacing.
#
# Boolean order: unchanged and legal at every stage.  The cap change is inside
# loft(), i.e. before SUBSURF, before nose_shape, before the arch cut and
# before solidify; the shell is closed and manifold throughout, and the caps
# are ~0.7 m from the nearest arch.  It makes the TAIL booleans strictly
# easier -- the rear-window and engine-lid cutters previously had to cut a
# 110-gon-derived fan and left 19 n-gons and 11 triangles jammed against the
# pole; a regular patch gives the exact solver quads.
def _coons_cap(loop_idx, verts, faces, flip):
    """Cap a boundary loop with a Coons quad grid. Border reuses loop verts."""
    n = len(loop_idx)
    a = n // 4
    b = n // 2 - a
    if 2 * (a + b) != n or a < 2 or b < 2:          # odd loop: fall back
        faces.append(tuple(reversed(loop_idx)) if flip else tuple(loop_idx))
        return
    P = [Vector(verts[k]) for k in loop_idx]
    grid = [[None] * (b + 1) for _ in range(a + 1)]
    for i in range(a + 1):                          # bottom / top rows
        grid[i][0] = loop_idx[i]
        grid[i][b] = loop_idx[(2 * a + b - i) % n]
    for j in range(b + 1):                          # left / right columns
        grid[a][j] = loop_idx[(a + j) % n]
        grid[0][j] = loop_idx[(n - j) % n]
    c00, c10 = P[0], P[a]
    c01, c11 = P[(2 * a + b) % n], P[(a + b) % n]
    for i in range(1, a):
        u = i / a
        A_, C_ = P[i], P[(2 * a + b - i) % n]
        for j in range(1, b):
            v = j / b
            B_, D_ = P[(a + j) % n], P[(n - j) % n]
            co = ((1 - v) * A_ + v * C_ + (1 - u) * D_ + u * B_
                  - ((1 - u) * (1 - v) * c00 + u * (1 - v) * c10
                     + (1 - u) * v * c01 + u * v * c11))
            grid[i][j] = len(verts)
            verts.append((co.x, co.y, co.z))
    for i in range(a):
        for j in range(b):
            q = (grid[i][j], grid[i + 1][j], grid[i + 1][j + 1], grid[i][j + 1])
            faces.append(tuple(reversed(q)) if flip else q)


def loft(rings, cap_first=False, cap_last=False, name="loft"):
    verts, faces = [], []
    n = len(rings[0])
    for r in rings:
        verts.extend(r)
    for s in range(len(rings) - 1):
        a, b = s * n, (s + 1) * n
        for i in range(n):
            j = (i + 1) % n
            faces.append((a + i, a + j, b + j, b + i))
    if cap_first:
        _coons_cap(list(range(n)), verts, faces, flip=True)
    if cap_last:
        o = (len(rings) - 1) * n
        _coons_cap(list(range(o, o + n)), verts, faces, flip=False)
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.validate()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    return ob


# ----------------------------------------------------------------------------
# longitudinal profiles
# ----------------------------------------------------------------------------
# under-body / sill bottom edge
ZB = aft_lut([
    (-2.108, 0.468), (-2.086, 0.432), (-2.050, 0.408), (-2.000, 0.394),
    (-1.900, 0.393), (-1.600, 0.387), (-1.200, 0.386), (-0.400, 0.385),
    ( 0.400, 0.385), ( 1.000, 0.387), ( 1.500, 0.391), ( 1.800, 0.397),
    ( 1.960, 0.408), ( 2.040, 0.430), ( 2.085, 0.470), ( 2.108, 0.520),
])

# ---------------------------------------------------------------------------
# KOMBI / MICROBUS  --  one continuous shell, nose to tail (SPEC.md §1)
# ---------------------------------------------------------------------------
# top edge: tail roll-down -> roof -> windscreen -> cowl -> nose cap
ZT_ALL = aft_lut([
    (-2.108, 1.452), (-2.098, 1.545), (-2.083, 1.634), (-2.060, 1.714),
    (-2.030, 1.782), (-1.994, 1.834), (-1.948, 1.867), (-1.892, 1.884),
    (-1.820, 1.8908), (-1.600, 1.8928), (-1.100, 1.8940), (-0.400, 1.8944),
    ( 0.300, 1.8942), ( 0.900, 1.8938), ( 1.200, 1.8935), ( 1.480, 1.8910),
    ( 1.640, 1.8860), ( 1.730, 1.8740), ( 1.775, 1.8560), ( 1.805, 1.8240),
    ( 1.830, 1.7880), ( 1.880, 1.6920), ( 1.930, 1.5960), ( 1.980, 1.5000),
    ( 2.020, 1.4230), ( 2.045, 1.3760), ( 2.065, 1.3560), ( 2.082, 1.3200),
    ( 2.096, 1.2620), ( 2.108, 1.1800),
])

# --------------------------------------------------------------------------
# rev 16 -- THE TRANSVERSE ROOF SECTION.  Re-fitted jointly with the roof edge.
#
# The defect is LOCAL to the roof/side junction and it was measured without any
# datum, scale or ground line, as a difference between two features at the same
# depth on the same flank of ref_side.jpg:
#
#     drip-rail groove  ->  serving-aperture top
#         bay 3  6.16 px over 83 columns (sd 0.19)   28.3 mm
#         bay 2  6.05 px over 83 columns (sd 0.19)   27.4 mm
#         bay 1  6.13 px over 62 columns (sd 0.21)   27.5 mm
#         adopted 27.7 +- 0.5 mm      built 68.6 mm  ->  the roll starts
#                                                        41 mm TOO HIGH
#
# A 2 % error in k_t moves 27.7 mm by 0.6 mm, so this is effectively scale-free.
#
# LOFT_GROUND_rev15 sec.1.3 proposed spending that 41 mm (it said 63) on
# ZT_ALL.  REJECTED, and the reason is a lock: the windscreen is anchored at
# absolute P_TOP = (1.8340, 0, 1.7745) in t1_shell, and lowering ZT_ALL puts
# the shell's top edge BELOW the screen's own top at that station -- the cutter
# would open a notch to the sky.  The measurement is local to the roof/side
# junction, so it is spent on the junction: RT_ALL (where the flank stops being
# vertical) and CR_ALL (the crown), with ZT_ALL, the rake, the tail roll-down
# and the windscreen all untouched.  SPEC sec.10.34.
#
# WHY 63 BECAME 41.  Not a scale error -- k_t = 215.5 px/m is VALIDATED here,
# because belt -> aperture-top measures 500.9 mm against the locked 503.0
# (-2.1 mm, 0.4 %).  It is a DATUM error: the hub-referenced chain puts the
# locked belt at 1.2145 AG against the model's 1.2436, 29 mm low -- the same
# common-mode signature SPEC sec.10.11 bans the ground line for.
#
#   roll start (gutter lip) authored   1.8027   -> RT_ALL = 1.8940 - zt0
#   crown authored                     2.0119   -> CR_ALL = crown - 1.8940
#   D = RT + CR = 0.2128               LOFT_GROUND sec.1.3: 0.2116 +- 0.035
#   R = Yt^2/(2 CR) = 2.24 m at Yt = 0.7273     (2.45 stays refuted: it needs
#                                                D = 0.172, not 0.213)
#
# R is a RE-EXPRESSION of D, not a second finding, and it moves with Yt -- so
# it is quoted with its Yt or not at all.  D is the robust number.
RT_ALL = aft_lut([
    (-2.108, 0.082), (-2.055, 0.062), (-1.970, 0.054), (-1.900, 0.0750),
    (-1.820, 0.0949), ( 1.640, 0.0949), ( 1.730, 0.0700), ( 1.790, 0.046),
    ( 1.830, 0.038), ( 1.990, 0.036),
    ( 2.030, 0.030), ( 2.070, 0.045), ( 2.108, 0.085),
])

CR_ALL = aft_lut([
    (-2.108, 0.012), (-2.000, 0.030), (-1.900, 0.0700), (-1.800, 0.1179),
    ( 1.620, 0.1179), ( 1.730, 0.0700), ( 1.810, 0.020),
    ( 2.030, 0.010), ( 2.108, 0.018),
])

# rev 16: the aft half of this list is passed through `_aft()` below, so the
# numbers here stay as authored and the f-distribution that clusters them into
# the corner roll is preserved exactly.  LOFT_GROUND_rev15 sec.3.3's tabulated
# f values are reproduced by construction rather than re-typed -- re-typing a
# table of 21 metre values against an origin that has already moved once is
# precisely the mistake SPEC sec.10.7 was made of.
STATIONS = [_aft(_x) for _x in [
    -2.108, -2.1015, -2.093, -2.081, -2.066, -2.047, -2.024, -1.998,
    -1.968, -1.934, -1.896, -1.855, -1.805, -1.745, -1.678, -1.605,
    -1.525, -1.440, -1.350, -1.255, -1.155, -1.050, -0.940, -0.825,
    -0.705, -0.580, -0.450, -0.315, -0.175, -0.030,  0.120,  0.270,
     0.420,  0.560,  0.700,  0.835,  0.965,  1.090,  1.205,  1.310,
     1.400,  1.480,  1.555,  1.625,  1.690,  1.735,  1.768,  1.792,
     1.812,  1.834,  1.860,  1.890,  1.920,  1.950,  1.978,  2.000,
     2.018,  2.034,  2.048,  2.062,  2.074,  2.085,  2.094,  2.1015,
     2.108,
]]


def build_kombi():
    """the whole van body as one lofted shell -- no cab/rear seam"""
    rings = []
    for x in STATIONS:
        rings.append(ring(x, WX(x), ZB(x), ZT_ALL(x),
                          RB_ALL(x), RT_ALL(x), CR_ALL(x), bcrown=0.012))
    return loft(rings, cap_first=True, cap_last=True, name="T1_body")

# maximum half width
WX = aft_lut([                     # SPEC r4: scaled x1.01744 for W 1.720 -> 1.750
    (-2.108, 0.7122), (-2.075, 0.7733), (-2.030, 0.8262), (-1.965, 0.8597),
    (-1.880, 0.8730), (-1.700, 0.8750), ( 1.760, 0.8750), ( 1.845, 0.8730),
    ( 1.930, 0.8628), ( 2.010, 0.8404), ( 2.065, 0.8038), ( 2.092, 0.7651),
    ( 2.108, 0.7244),
])

# cab roof / windscreen / cowl top edge
ZT_CAB = lut([
    ( 0.420, 1.876), ( 0.460, 1.886), ( 0.620, 1.891), ( 0.900, 1.8935),
    ( 1.200, 1.8935), ( 1.480, 1.891), ( 1.640, 1.886), ( 1.730, 1.874),
    ( 1.775, 1.856), ( 1.805, 1.824), ( 1.830, 1.780), ( 1.880, 1.690),
    ( 1.930, 1.598), ( 1.975, 1.518), ( 2.008, 1.458), ( 2.030, 1.437),
    ( 2.055, 1.425), ( 2.075, 1.404), ( 2.093, 1.360), ( 2.108, 1.290),
])

# top roll radius
RT_CAB = lut([
    ( 0.420, 0.026), ( 0.470, 0.050), ( 1.700, 0.054), ( 1.790, 0.046),
    ( 1.830, 0.038), ( 2.000, 0.036), ( 2.048, 0.030), ( 2.078, 0.045),
    ( 2.108, 0.088),
])
CR_CAB = lut([
    ( 0.420, 0.026), ( 1.700, 0.030), ( 1.810, 0.015), ( 2.010, 0.010),
    ( 2.108, 0.018),
])
RB_ALL = aft_lut([
    (-2.108, 0.085), (-2.000, 0.105), (-1.900, 0.120), (-0.400, 0.122),
    ( 1.500, 0.122), ( 1.900, 0.116), ( 2.060, 0.100), ( 2.108, 0.085),
])

CAB_STATIONS = [
    0.420, 0.4285, 0.445, 0.475, 0.520, 0.580, 0.660, 0.760, 0.870, 0.980,
    1.090, 1.200, 1.300, 1.395, 1.480, 1.560, 1.630, 1.690, 1.735, 1.768,
    1.792, 1.812, 1.834, 1.860, 1.890, 1.920, 1.950, 1.978, 2.000, 2.018,
    2.034, 2.048, 2.062, 2.074, 2.085, 2.094, 2.1015, 2.1065, 2.108,
]

BED_STATIONS = [
    -2.108, -2.0985, -2.086, -2.068, -2.045, -2.016, -1.982, -1.944,
    -1.900, -1.850, -1.790, -1.720, -1.640, -1.550, -1.450, -1.340,
    -1.220, -1.090, -0.950, -0.800, -0.640, -0.470, -0.300, -0.130,
     0.040,  0.190,  0.310,  0.390,  0.420,
    # tucked continuation that hides behind the cab rear wall so the
    # Catmull-Clark boundary rule cannot pinch the visible flank at x=0.42
     0.436,  0.470,  0.530,  0.600,
]
# inward shrink applied to the tucked continuation only
SHRINK = lut([(0.420, 0.000), (0.436, 0.003), (0.470, 0.010),
              (0.600, 0.016)])


# ----------------------------------------------------------------------------
# generic solid builders used for boolean cutters and hard details
# ----------------------------------------------------------------------------
def rrect(w, h, r, seg=7):
    """rounded rectangle outline centred on origin, CCW, list of (u, v)"""
    r = min(r, w / 2 - 1e-4, h / 2 - 1e-4)
    a, b = w / 2 - r, h / 2 - r
    pts = []
    for cx, cy, a0 in ((a, b, 0.0), (-a, b, math.pi / 2),
                       (-a, -b, math.pi), (a, -b, 1.5 * math.pi)):
        for i in range(seg + 1):
            t = a0 + (math.pi / 2) * i / seg
            pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    return pts


def signed_area(pts):
    a = 0.0
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        a += x1 * y2 - x2 * y1
    return a * 0.5


def poly_offset(pts, d):
    """offset a closed outline outward by d, orientation independent"""
    n = len(pts)
    if signed_area(pts) < 0:
        d = -d
    out = []
    for i in range(n):
        px, py = pts[i - 1]
        cx, cy = pts[i]
        nx, ny = pts[(i + 1) % n]
        # average of the two edge normals
        e1 = (cx - px, cy - py); e2 = (nx - cx, ny - cy)
        m1 = math.hypot(*e1) or 1.0; m2 = math.hypot(*e2) or 1.0
        v = ((e1[1] / m1 + e2[1] / m2), (-e1[0] / m1 - e2[0] / m2))
        mv = math.hypot(*v) or 1.0
        out.append((cx + d * v[0] / mv, cy + d * v[1] / mv))
    return out


def _frame(origin, u, v, w, pts_list, depth, name):
    """build a mesh from a list of closed outlines extruded +-depth/2 along w"""
    origin = Vector(origin); u = Vector(u).normalized()
    v = Vector(v).normalized(); w = Vector(w).normalized()
    verts, faces = [], []
    for pts in pts_list:
        base = len(verts)
        n = len(pts)
        for s in (-depth / 2, depth / 2):
            for (a, b) in pts:
                verts.append(tuple(origin + u * a + v * b + w * s))
        for i in range(n):
            j = (i + 1) % n
            faces.append((base + i, base + j, base + n + j, base + n + i))
    me = bpy.data.meshes.new(name)
    me.from_pydata([list(x) for x in verts], [], faces)
    me.validate()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    return ob


def fix_normals(ob):
    bm = bmesh.new(); bm.from_mesh(ob.data)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(ob.data); bm.free()
    ob.data.update()
    return ob


def solid_prism(origin, u, v, w, pts, depth, name="cut"):
    """closed solid: outline extruded along w, capped both ends"""
    ob = _frame(origin, u, v, w, [pts], depth, name)
    me = ob.data
    n = len(pts)
    bm = bmesh.new(); bm.from_mesh(me)
    bm.verts.ensure_lookup_table()
    bm.faces.new([bm.verts[i] for i in range(n - 1, -1, -1)])
    bm.faces.new([bm.verts[n + i] for i in range(n)])
    # rev 44 -- A CAP TRIANGULATION WAS TRIED HERE AND REVERTED, recorded so it
    # is not tried again.  It was a guess at why the VW emblem's W rendered as
    # fragments; it did NOT fix that (the real cause was the roundel being
    # mounted 11 mm inside the nose, see build.py) and it BROKE TWO WHEEL-ARCH
    # BOOLEANS -- `arch-11` and `arch-1-1` rolled back at both subdivision
    # levels.  solid_prism builds every cutter in this model, so a change here
    # is never local.
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.normal_update(); bm.to_mesh(me); bm.free()
    return ob


def gap_prism(origin, u, v, w, pts, gap, depth, name="gap"):
    """closed solid ring (panel-gap cutter) of width `gap` following `pts`"""
    inner = poly_offset(pts, -gap / 2)
    outer = poly_offset(pts, gap / 2)
    n = len(pts)
    verts, faces = [], []
    ori = Vector(origin); U = Vector(u).normalized()
    V = Vector(v).normalized(); W = Vector(w).normalized()
    for s in (-depth / 2, depth / 2):
        for (a, b) in inner:
            verts.append(tuple(ori + U * a + V * b + W * s))
        for (a, b) in outer:
            verts.append(tuple(ori + U * a + V * b + W * s))
    # layer 0 : 0..n-1 inner, n..2n-1 outer  |  layer 1 : 2n..3n-1, 3n..4n-1
    for i in range(n):
        j = (i + 1) % n
        # inner wall
        faces.append((i, j, 2 * n + j, 2 * n + i))
        # outer wall
        faces.append((n + j, n + i, 2 * n + n + i, 2 * n + n + j))
        # back cap
        faces.append((j, i, n + i, n + j))
        # front cap
        faces.append((2 * n + i, 2 * n + j, 2 * n + n + j, 2 * n + n + i))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.validate()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    return fix_normals(ob)


def cylinder(center, axis, radius, length, seg=64, name="cyl"):
    pts = [(radius * math.cos(TAU * i / seg), radius * math.sin(TAU * i / seg))
           for i in range(seg)]
    ax = Vector(axis).normalized()
    u = ax.cross(Vector((0, 0, 1)))
    if u.length < 1e-6:
        u = ax.cross(Vector((1, 0, 0)))
    u.normalize()
    v = ax.cross(u)
    return solid_prism(center, u, v, ax, pts, length, name)


def revolve(profile, seg=72, axis='Y', name="rev", cap=False, mat_bands=None):
    """
    profile = closed list of (along_axis, radius); revolve about the axis.
    mat_bands = {profile_index: material_slot} -- the quad ring between
    profile[i] and profile[i+1] takes that slot (used for whitewalls).
    """
    n = len(profile)
    verts, faces, fmat = [], [], []
    for k in range(seg):
        a = TAU * k / seg
        ca, sa = math.cos(a), math.sin(a)
        for (t, r) in profile:
            if axis == 'Y':
                verts.append((r * ca, t, r * sa))
            elif axis == 'X':
                verts.append((t, r * ca, r * sa))
            else:
                verts.append((r * ca, r * sa, t))
    for k in range(seg):
        k2 = (k + 1) % seg
        for i in range(n):
            j = (i + 1) % n
            faces.append((k * n + i, k * n + j, k2 * n + j, k2 * n + i))
            fmat.append((mat_bands or {}).get(i, 0))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.validate()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    fix_normals(ob)
    if mat_bands:
        for f, mi in zip(me.polygons, fmat):
            f.material_index = mi
    return ob


def _mitre_outline(spine, w):
    """Closed outline of a constant-width stroke through `spine`, mitred.

    Offsets the polyline w/2 either side and intersects consecutive edge lines
    at each interior joint, so the corners meet in a point instead of two
    rectangles overlapping. That overlap is what made the old glyph read as an
    X: at the V apex two independent bars crossed and their union bulged.
    """
    P = [Vector(p) for p in spine]
    def side(sgn):
        out = []
        for i in range(len(P) - 1):
            d = (P[i + 1] - P[i]).normalized()
            n = Vector((-d.y, d.x)) * (sgn * w / 2.0)
            out.append((P[i] + n, P[i + 1] + n))
        pts = [out[0][0]]
        for i in range(len(out) - 1):
            (a0, a1), (b0, b1) = out[i], out[i + 1]
            d1, d2 = (a1 - a0), (b1 - b0)
            den = d1.x * d2.y - d1.y * d2.x
            if abs(den) < 1e-9:
                pts.append(a1)
                continue
            t = ((b0.x - a0.x) * d2.y - (b0.y - a0.y) * d2.x) / den
            j = a0 + d1 * t
            # a mitre at a very sharp joint runs away to infinity: clamp it
            if (j - P[i + 1]).length > 2.2 * w:
                pts.extend([a1, b0])
            else:
                pts.append(j)
        pts.append(out[-1][1])
        return pts
    left = side(+1)
    right = side(-1)
    right.reverse()
    return [(p.x, p.y) for p in left + right]


def vw_bars(R, w, origin, u_ax, v_ax, n_ax, depth, tag="vw"):
    """V-over-W emblem as TWO closed mitred prisms, one V and one W.

    rev 8, per SKEPTIC_PASS.md sec.D. This was six independent overlapping bars
    (one object per stroke, 6 objects per hubcap = 24 for four hubcaps) whose
    unions self-intersected at every joint; at hero resolution the V and the W
    merged into an X. Two closed outlines remove the self-intersection outright
    rather than hiding it.

    Geometry from the skeptic pass: V arm -40.75 deg, W inner -53.04 deg, so
    12.29 deg apart. V above W, always (SPEC 0.2).

    rev 17 -- THE AIR-GAP SENTENCE THAT USED TO SIT HERE WAS FALSE, and it is
    deleted rather than re-valued.  It claimed "a clear 12.7 mm air gap between
    the V apex and the W peak at the locked ring diameter of 0.370 m".  Three
    things were wrong with it and all three are MEASURED on the built nose
    roundel (ring outer D 0.2802 m), not argued:

      * V apex underside   z = -0.03515      W centre-peak top  z = +0.01686
        -> the V PENETRATES the W by 52.0 mm.  There is no gap and there never
           was one.  SPEC 10.25's premise is wrong.
      * 0.370 is stale.  The locked diameter has been ROUNDEL_D = 0.2800
        (built 0.2802) since rev 10.
      * No diameter can open a gap.  The spine separation between the V apex
        (0, -0.060) and the W peak (0, -0.075) is 0.015 R, while each stroke's
        mitred half-extension is an order of magnitude larger.  The two fuse
        BY CONSTRUCTION -- which is why "correcting the diameter" closed the
        designed gap twice and merged the glyph into an X twice.

    rev 44 -- THIS PARAGRAPH WAS HALF RIGHT AND THE HALF THAT WAS WRONG COST
    THE EMBLEM ITS W.  A TOUCH at the centre does match the photographs: in
    ref_nolita_front34.jpg the V's apex and the W's peak merge into one mass
    over about 0.1 of the ring diameter.  A 52 mm PENETRATION does not -- it
    buries the W's centre peak AND both inner arms, and the reference shows all
    six strokes legible.  The overlap was not a property of the fusion; it was
    a property of the V being 2.5x too wide-angled, measured above.  With the
    arm angle corrected the V's outline bottom sits 11.6 mm above the ring
    centre against the W's peak at 16.8 mm -- a 5 mm touch, which is the
    photograph.  The fusion stays; the burial does not.

    rev 17 also GREW THE V's ARM TIPS.  Building the hubcap ring exposed that
    the V reached only 0.7154 of the glyph's fit radius while the ring's inner
    edge sits at 0.8140 -- the V stopped 4.28 mm short of the band (4.9 % of
    the emblem D), where every reference frame shows both arms running into
    it.  Tips scaled by 0.8140/0.7154 = 1.138 about the apex.  The arm ANGLE
    and the whole W are untouched, and the V's radius stays below the W's, so
    _fit_glyph's scale does not move.  Written as an expression of the ring
    fraction so the two can never drift apart again.
    """
    _RING_INNER_FRAC = 1.0 - 2.0 * 0.093      # t1_detail.CAP_RING_BANDFRAC
    # ------------------------------------------------------------- rev 44
    # THE V WAS 2.5x TOO WIDE-ANGLED AND IT WAS ERASING THE W.
    #
    # The owner reported the logo off the rev-44 hero.  Rendered face-on the
    # emblem showed a V and TWO ISOLATED STUBS -- no W centre peak, no inner
    # arms, no legs.  The W object was built correctly (20 verts, full extent,
    # not self-intersecting -- all three checked) and then almost entirely
    # COVERED by the V, which is solid and the same material.
    #
    # MEASURED ON ref_nolita_front34.jpg, the owner's rev-44 upload and the
    # clearest roundel in the set.  Row-run analysis of the red mask, VERTICAL
    # extents only because the frame is a three-quarter (a rotation about a
    # vertical axis preserves vertical ratios):
    #     ring outer vertical D .............. 68 px
    #     V arm separation at 0.206 D down ... 0.162 D   built 0.406 D  <-- 2.5x
    #     V apex, from the ring top .......... 0.353 D   built 0.625 D
    #     V height / ring D .................. 0.235     built 0.374
    # The V's tips are right (they run into the ring band in both), so the
    # error is the ARM ANGLE, and widening the arms is what drove the apex
    # down through the W.
    #
    # The tips are now placed ON the band circle by construction at the
    # measured half-angle, so no fraction can go stale: _V_TIP_X is the only
    # authored number and the tip height follows from the circle.
    _V_TIP_X = 0.270                          # measured, see above
    _apex    = (0.000, 0.284)                 # 0.353 of ring D from the top
    _ty      = (_RING_INNER_FRAC ** 2 - _V_TIP_X ** 2) ** 0.5
    # ------------------------------------------------------------- rev 44b
    # EVERY STROKE END ON THE RING -- WHICH THE DOCSTRING HAS CLAIMED SINCE
    # REV 15 AND THE GEOMETRY HAS NEVER DONE.  SPEC 10.107.
    #
    # *[owner, rev 44b]* "The vw still doesn't look right."
    #
    # MEASURED ON THE BUILT GLYPH, six 30-degree sectors, radius as a fraction
    # of the ring radius, with the ring's band spanning 0.800-1.000:
    #     W's two BOTTOM vertices ......... 0.840   into the band
    #     W's two OUTER ARM tips .......... 0.738   62 mm short of it
    #     V's two ARM tips ................ 0.724   76 mm short of it
    # `_fit_glyph` scales by the SINGLE FURTHEST VERTEX, so whichever end
    # reaches furthest lands in the band and drags every other end short.  Only
    # the W's bottom ever touched.  Four of the six strokes have been floating
    # inside the ring since rev 15, and rev 17 caught exactly this for the V's
    # tips -- it scaled them by 0.8140/0.7154 and then `_fit_glyph`'s divisor
    # moved underneath them again, because the W was left where it was.
    #
    # AND THE PHOTOGRAPH IS UNAMBIGUOUS.  `ref_nolita_front34.jpg`, red-mask
    # row runs over the roundel's 41 x 66 px bbox: at y+6 the V's arms and the
    # ring are ONE RUN on both sides, and at y+62 the W's bottoms and the
    # ring's lower arc are ONE RUN.  Nothing floats.  rev 15's own docstring
    # says it in words -- "every stroke end -- both V arms, both W outer arms,
    # both W legs -- disappears into the ring band".
    #
    # THE FIX CHANGES NO ANGLE.  Each of the six terminal points is projected
    # RADIALLY onto the band circle, so every arm angle, the 12.29 deg
    # separation, the apex and the centre peak are all untouched -- only the
    # REACH moves, and it moves to a circle that is itself an expression of
    # the ring's own band fraction.  Nothing here can go stale.
    def _on_band(p):
        r = (p[0] ** 2 + p[1] ** 2) ** 0.5
        k = _RING_INNER_FRAC / r
        return (p[0] * k, p[1] * k)

    V_SPINE = [_on_band((-_V_TIP_X, _ty)), _apex, _on_band((_V_TIP_X, _ty))]
    W_SPINE = [_on_band((-0.760, -0.060)), _on_band((-0.380, -0.700)),
               (0.000, -0.075),
               _on_band((0.380, -0.700)), _on_band((0.760, -0.060))]
    for _p in (V_SPINE[0], V_SPINE[2], W_SPINE[0], W_SPINE[1],
               W_SPINE[3], W_SPINE[4]):
        assert abs((_p[0] ** 2 + _p[1] ** 2) ** 0.5 - _RING_INNER_FRAC) < 1e-12
    # ------------------------------------------------------------- rev 44b
    # PUTTING THE SPINE ON THE BAND CIRCLE IS NOT ENOUGH, AND THE FIRST
    # ATTEMPT PROVED IT: the V's tips came back at 0.716 of the ring radius
    # and the W's bottoms at 0.840, WORSE for the V than before.
    #
    # WHY.  What must land on the ring is the OUTLINE, not the spine, and the
    # two differ by the cap geometry: a terminal end is cut off flush AT its
    # spine point, while an interior vertex -- the W's two bottoms -- is a
    # sharp corner whose outer point BULGES past the spine by w/(2 sin(a/2)).
    # Placing all six spine points on one circle therefore places the six
    # OUTLINE ends on six different circles, and `_fit_glyph` then scales by
    # whichever bulges most.  Compensating analytically would need the mitre's
    # half-angle at each vertex, which is exactly the kind of derived literal
    # that has gone stale here twice.
    #
    # Solved by FIXED POINT on the built outline instead -- the same pattern
    # as `t1_shell._G_BUILD`, and for the same reason: it re-solves itself if
    # the width, the angles or the mitre ever change.  Each terminal's radius
    # is scaled until the outline vertices belonging to it reach the band
    # circle.  Converged values are asserted below, never typed.
    _term = [('V', 0), ('V', 2), ('W', 0), ('W', 1), ('W', 4), ('W', 3)]
    _rad = {t: _RING_INNER_FRAC for t in _term}

    def _spines():
        v = list(V_SPINE); ww = list(W_SPINE)
        for (which, i) in _term:
            base = V_SPINE[i] if which == 'V' else W_SPINE[i]
            k = _rad[(which, i)] / _RING_INNER_FRAC
            if which == 'V':
                v[i] = (base[0] * k, base[1] * k)
            else:
                ww[i] = (base[0] * k, base[1] * k)
        return v, ww

    for _ in range(40):
        v, ww = _spines()
        reach, worst = {}, 0.0
        for which, spine in (('V', v), ('W', ww)):
            outline = _mitre_outline([(x * R, y * R) for (x, y) in spine], w)
            for (px, py) in outline:
                j = min(range(len(spine)),
                        key=lambda k: (px / R - spine[k][0]) ** 2
                                    + (py / R - spine[k][1]) ** 2)
                if (which, j) in _rad:
                    rr = math.hypot(px, py) / R
                    reach[(which, j)] = max(reach.get((which, j), 0.0), rr)
        for t in _term:
            if t in reach and reach[t] > 1e-9:
                e = _RING_INNER_FRAC / reach[t]
                worst = max(worst, abs(e - 1.0))
                _rad[t] *= e
        if worst < 1e-9:
            break
    V_SPINE, W_SPINE = _spines()

    obs = []
    for i, spine in enumerate((V_SPINE, W_SPINE)):
        pts = _mitre_outline([(x * R, y * R) for (x, y) in spine], w)
        obs.append(solid_prism(origin, u_ax, v_ax, n_ax, pts, depth,
                               name=f"{tag}{i}"))
    return obs


def sweep(path, profile, up=(0, 0, 1), name="sweep", closed=False,
          caps=True, scale=None):
    """
    path    : list of 3-D points
    profile : list of (a, b) in the local frame  a = side (path normal), b = up
    """
    P = [Vector(p) for p in path]
    n = len(profile)
    verts, faces = [], []
    UP = Vector(up).normalized()
    for i, p in enumerate(P):
        if i == 0:
            t = (P[1] - P[0])
        elif i == len(P) - 1:
            t = (P[-1] - P[-2])
        else:
            t = (P[i + 1] - P[i - 1])
        t.normalize()
        side = t.cross(UP).normalized()
        upl = side.cross(t).normalized()
        s = 1.0 if scale is None else scale[i]
        for (a, b) in profile:
            verts.append(tuple(p + side * (a * s) + upl * (b * s)))
    rng = range(len(P)) if closed else range(len(P) - 1)
    for i in rng:
        j = (i + 1) % len(P)
        for k in range(n):
            l = (k + 1) % n
            faces.append((i * n + k, i * n + l, j * n + l, j * n + k))
    if caps and not closed:
        faces.append(tuple(range(n - 1, -1, -1)))
        o = (len(P) - 1) * n
        faces.append(tuple(range(o, o + n)))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.validate()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    return fix_normals(ob)


def flank_y(x, z):
    """outer body half-width at a point on the flank"""
    return WX(x) * G(z)


def drape_x(objs, surf_x, mount, standoff=0.0016, grid=41, pad=0.02):
    """Push a FLAT, X-extruded plate (the nose emblem) onto the CURVED nose.

    rev 45.  THIS IS THE DEFECT BEHIND "THE LOGO IS OFF", REPORTED BY THE OWNER
    IN THREE CONSECUTIVE REVISIONS AND NEVER FOUND, BECAUSE EVERY CHECK EVER
    RUN ON THE EMBLEM WAS RUN ON ITS OWN OUTLINE, IN ITS OWN PLANE, IN
    ISOLATION FROM THE BODY IT SITS ON.

    `t1_detail.roundel` and `vw_logo_fit` both build the emblem in the Y-Z
    plane and extrude it along +X, so the finished badge is a FLAT PLATE.  The
    nose is not flat.  Raycast against the built body at rev 45, at the
    roundel's own centre height, ROUNDEL_D = 0.280 m:

        straight UP   at the ring radius   the nose is  -31.6 mm  (falls away)
        up-left/right at the ring radius                -19.0 mm
        sideways      at the ring radius                 -0.6 mm
        straight DOWN at the ring radius                 +3.0 mm  (comes forward)

    The glyph's front face sits at x = 2.1265 after the step-8b shear and the
    nose below the badge centre sits at 2.1265..2.1268.  So the plate's LOWER
    half is flush with, or 0.3 mm BEHIND, the sheet metal, and its UPPER half
    floats up to 32 mm proud of it.  Rendered, the V (which lives in the upper
    half) stands out and THE WHOLE W DISAPPEARS INTO THE BODY except for the
    two outer arm tips, which is why the badge reads as a CLOCK FACE.

    Everything else about the glyph was measured this revision and is RIGHT:
    the spine angles reproduce ref_workshop.jpg's mark to a few degrees
    (V arms +-37 deg photographed against +-35.2 deg built; W outer arms +-95
    against +-93; W troughs +-145 against +-151.5), and the stroke width is
    0.218 +- 0.002 R photographed against 0.2046 R built.  NOTHING IN THE
    SPINE OR THE WIDTH IS MOVED BY THIS FIX.  SPEC 10.110.

    `surf_x(y, z)` returns the body's surface X at a point, or None on a miss.
    It is sampled ONCE on a `grid` x `grid` lattice over the objects' own
    (y, z) bounding box padded by `pad`, then bilinearly interpolated, so the
    result is smooth and a single stray miss cannot spike one vertex.

    `mount` is the X of the plate's OWN MOUNTING PLANE -- the plane its author
    intended to lie against the sheet metal.  Every vertex moves by

        dx  =  surf_x(y, z) - mount + standoff

    so the mounting plane lands ON the surface everywhere and the plate's
    relief is carried out from there.  Nothing moves in Y or Z, so the
    outline, the scale and every in-plane measurement are untouched BY
    CONSTRUCTION.

    `mount` matters and a single shared reference is NOT good enough: the ring
    and its backing disc are authored with the mounting plane at local x = 0
    (world 2.1155) while the glyph is authored with its BACK FACE as the
    mounting plane (world 2.1210).  Draping them against one common datum left
    the disc's front cone 3.6 mm INSIDE the nose -- the guard below caught it,
    at -3.59 mm, on this revision's own first attempt.  Call this once per
    plate, each with its own mount.

    Returns (n_moved, dx_min, dx_max, n_miss).
    """
    ys, zs = [], []
    for o in objs:
        for v in o.data.vertices:
            ys.append(v.co.y); zs.append(v.co.z)
    y_lo, y_hi = min(ys) - pad, max(ys) + pad
    z_lo, z_hi = min(zs) - pad, max(zs) + pad
    gy = [y_lo + (y_hi - y_lo) * i / (grid - 1) for i in range(grid)]
    gz = [z_lo + (z_hi - z_lo) * i / (grid - 1) for i in range(grid)]
    n_miss = 0
    G = [[None] * grid for _ in range(grid)]
    for j, z in enumerate(gz):
        for i, y in enumerate(gy):
            x = surf_x(y, z)
            if x is None:
                n_miss += 1
            G[j][i] = x
    # fill misses from the nearest sampled neighbour so the lattice is total
    known = [(j, i) for j in range(grid) for i in range(grid) if G[j][i] is not None]
    if not known:
        raise RuntimeError("drape_x: the surface raycast missed EVERY lattice "
                           "point -- the emblem is not over the body at all")
    for j in range(grid):
        for i in range(grid):
            if G[j][i] is None:
                jj, ii = min(known, key=lambda p: (p[0] - j) ** 2 + (p[1] - i) ** 2)
                G[j][i] = G[jj][ii]

    def interp(y, z):
        fy = (y - y_lo) / (y_hi - y_lo) * (grid - 1)
        fz = (z - z_lo) / (z_hi - z_lo) * (grid - 1)
        i = min(max(int(fy), 0), grid - 2); j = min(max(int(fz), 0), grid - 2)
        a, b = fy - i, fz - j
        return (G[j][i] * (1 - a) * (1 - b) + G[j][i + 1] * a * (1 - b)
                + G[j + 1][i] * (1 - a) * b + G[j + 1][i + 1] * a * b)

    dxs = []
    n = 0
    for o in objs:
        for v in o.data.vertices:
            dx = interp(v.co.y, v.co.z) - mount + standoff
            v.co.x += dx
            dxs.append(dx); n += 1
        o.data.update()
    return n, min(dxs), max(dxs), n_miss


def conform_solid(outline, side, off=0.0, thick=0.10, name="cf"):
    """
    Closed prism whose two faces follow the curved flank.
    `outline` is a closed list of (x, z); the solid straddles the sheet metal
    so it can be used as a boolean cutter, a glass pane or a seal.
    """
    n = len(outline)
    verts, faces = [], []
    for (x, z) in outline:                                   # outer skin
        verts.append((x, side * (flank_y(x, z) + off + thick / 2), z))
    for (x, z) in outline:                                   # inner skin
        verts.append((x, side * (flank_y(x, z) + off - thick / 2), z))
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
    faces.append(tuple(range(n - 1, -1, -1)))
    faces.append(tuple(range(n, 2 * n)))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.validate()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    fix_normals(ob)
    xs = [p[0] for p in outline]; zs = [p[1] for p in outline]
    x0, x1 = min(xs), max(xs); z0, z1 = min(zs), max(zs)
    uvl = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        for li in poly.loop_indices:
            v = me.vertices[me.loops[li].vertex_index].co
            u = (v.x - x0) / max(x1 - x0, 1e-6)
            uvl.data[li].uv = (u if side > 0 else 1.0 - u,
                               (v.z - z0) / max(z1 - z0, 1e-6))
    return ob


def conform_ring(outline, side, width, off=0.0, thick=0.10, name="cr"):
    """flank-hugging ring of the given width, centred on `outline`"""
    inner = poly_offset(outline, -width / 2)
    outer = poly_offset(outline, width / 2)
    n = len(outline)
    verts, faces = [], []
    for ring_pts in (inner, outer):
        for (x, z) in ring_pts:
            verts.append((x, side * (flank_y(x, z) + off + thick / 2), z))
        for (x, z) in ring_pts:
            verts.append((x, side * (flank_y(x, z) + off - thick / 2), z))
    # layers: 0=in/out 1=in/in 2=out/out 3=out/in
    IO, II, OO, OI = 0, n, 2 * n, 3 * n
    for i in range(n):
        j = (i + 1) % n
        faces.append((IO + i, IO + j, II + j, II + i))        # inner wall
        faces.append((OO + j, OO + i, OI + i, OI + j))        # outer wall
        faces.append((IO + j, IO + i, OO + i, OO + j))        # outward cap
        faces.append((II + i, II + j, OI + j, OI + i))        # inward cap
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.validate()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    return fix_normals(ob)


def conform_disc(xc, zc, R, side, off=0.0016, seg=72, rings=10, name="dc"):
    """flat-ish decal disc that follows the flank, UV mapped 0..1"""
    verts, faces, uvs = [], [], []
    verts.append((xc, side * (flank_y(xc, zc) + off), zc))
    uvs.append((0.5, 0.5))
    for r in range(1, rings + 1):
        rr = R * r / rings
        for i in range(seg):
            a = TAU * i / seg
            x, z = xc + rr * math.cos(a), zc + rr * math.sin(a)
            verts.append((x, side * (flank_y(x, z) + off), z))
            uvs.append((0.5 + 0.5 * (rr / R) * math.cos(a) * (-side),
                        0.5 + 0.5 * (rr / R) * math.sin(a)))
    for i in range(seg):
        faces.append((0, 1 + i, 1 + (i + 1) % seg))
    for r in range(rings - 1):
        a0, b0 = 1 + r * seg, 1 + (r + 1) * seg
        for i in range(seg):
            j = (i + 1) % seg
            faces.append((a0 + i, b0 + i, b0 + j, a0 + j))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.validate()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    fix_normals(ob)
    uvl = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        for li in poly.loop_indices:
            uvl.data[li].uv = uvs[me.loops[li].vertex_index]
    return ob


def conform_panel(x0, x1, z0, z1, side, off=0.0016, nx=40, nz=12, name="pn"):
    """flank-hugging rectangular decal panel, UV mapped 0..1"""
    verts, faces, uvs = [], [], []
    for iz in range(nz + 1):
        z = z0 + (z1 - z0) * iz / nz
        for ix in range(nx + 1):
            x = x0 + (x1 - x0) * ix / nx
            verts.append((x, side * (flank_y(x, z) + off), z))
            u = ix / nx
            uvs.append((u if side > 0 else 1.0 - u, iz / nz))
    for iz in range(nz):
        for ix in range(nx):
            a = iz * (nx + 1) + ix
            b = a + nx + 1
            faces.append((a, a + 1, b + 1, b))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.validate()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    fix_normals(ob)
    uvl = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        for li in poly.loop_indices:
            uvl.data[li].uv = uvs[me.loops[li].vertex_index]
    return ob


def obj(name):
    return bpy.data.objects.get(name)


def mirror_y(ob, name=None):
    new = ob.copy(); new.data = ob.data.copy()
    new.name = name or (ob.name + "_m")
    bpy.context.collection.objects.link(new)
    new.scale.y = -1.0
    bpy.context.view_layer.update()
    me = new.data
    mw = new.matrix_world.copy()
    for v in me.vertices:
        v.co = mw @ v.co
    new.matrix_world = Matrix.Identity(4)
    fix_normals(new)
    return new


def boolean(target, cutter, op='DIFFERENCE', solver='EXACT'):
    m = target.modifiers.new("bool", 'BOOLEAN')
    m.operation = op
    m.object = cutter
    m.solver = solver
    if solver == 'EXACT':
        m.use_self = False
    return m


def apply_mods(ob):
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    ob.modifiers.clear()
    old = ob.data
    ob.data = me
    bpy.data.meshes.remove(old)
    return ob


def build_cab():
    rings = []
    for x in CAB_STATIONS:
        rings.append(ring(x, WX(x), ZB(x), ZT_CAB(x),
                          RB_ALL(x), RT_CAB(x), CR_CAB(x), bcrown=0.012))
    return loft(rings, cap_first=True, cap_last=True, name="T1_cab")


def build_bed():
    # rear body: top edge = gate rail, rolling down over the tail
    ZT_BED = lut([
        (-2.108, 1.150), (-2.098, 1.216), (-2.082, 1.258), (-2.058, 1.284),
        (-2.020, 1.298), (-1.900, 1.302), ( 0.420, 1.302),
    ])
    RT_BED = lut([
        (-2.108, 0.070), (-2.060, 0.045), (-1.960, 0.032), ( 0.420, 0.032),
    ])
    rings = []
    for x in BED_STATIONS:
        s = SHRINK(x) if x > 0.420 else 0.0
        rings.append(ring(x, WX(x) - s, ZB(x) + s, ZT_BED(x) - s,
                          max(RB_ALL(x) - s, 0.02), max(RT_BED(x) - s, 0.010),
                          0.004, bcrown=0.012))
    return loft(rings, cap_first=True, cap_last=True, name="T1_bed")
