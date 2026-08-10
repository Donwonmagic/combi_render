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

import bpy, bmesh, math
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
X_TAIL      = -2.108           # rear-most sheet metal
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
RAKE_Z0     =  0.0365          # ride drop at x = 0
RAKE_DZDX   =  0.0330          # nose-down rake, m per m forward (+/- 0.0040)
                               # 0.0302 from the belt, 0.0367 from the drip rail
X_DROP_REF  =  0.8636          # station where drop(x) == the pre-rev-8 scalar


def rake_drop(x):
    """Ride drop at station x. Authored (un-dropped) z minus this == above ground."""
    return RAKE_Z0 + RAKE_DZDX * x


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
NHALF = NA + NB + NC + ND + NE + 1          # 56
NLOOP = NHALF * 2 - 2                       # 110


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
        faces.append(tuple(range(n - 1, -1, -1)))
    if cap_last:
        o = (len(rings) - 1) * n
        faces.append(tuple(range(o, o + n)))
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
ZB = lut([
    (-2.108, 0.468), (-2.086, 0.432), (-2.050, 0.408), (-2.000, 0.394),
    (-1.900, 0.393), (-1.600, 0.387), (-1.200, 0.386), (-0.400, 0.385),
    ( 0.400, 0.385), ( 1.000, 0.387), ( 1.500, 0.391), ( 1.800, 0.397),
    ( 1.960, 0.408), ( 2.040, 0.430), ( 2.085, 0.470), ( 2.108, 0.520),
])

# ---------------------------------------------------------------------------
# KOMBI / MICROBUS  --  one continuous shell, nose to tail (SPEC.md §1)
# ---------------------------------------------------------------------------
# top edge: tail roll-down -> roof -> windscreen -> cowl -> nose cap
ZT_ALL = lut([
    (-2.108, 1.452), (-2.098, 1.545), (-2.083, 1.634), (-2.060, 1.714),
    (-2.030, 1.782), (-1.994, 1.834), (-1.948, 1.867), (-1.892, 1.884),
    (-1.820, 1.8908), (-1.600, 1.8928), (-1.100, 1.8940), (-0.400, 1.8944),
    ( 0.300, 1.8942), ( 0.900, 1.8938), ( 1.200, 1.8935), ( 1.480, 1.8910),
    ( 1.640, 1.8860), ( 1.730, 1.8740), ( 1.775, 1.8560), ( 1.805, 1.8240),
    ( 1.830, 1.7880), ( 1.880, 1.6920), ( 1.930, 1.5960), ( 1.980, 1.5000),
    ( 2.020, 1.4230), ( 2.045, 1.3760), ( 2.065, 1.3560), ( 2.082, 1.3200),
    ( 2.096, 1.2620), ( 2.108, 1.1800),
])

RT_ALL = lut([
    (-2.108, 0.082), (-2.055, 0.062), (-1.970, 0.054), (-1.860, 0.052),
    ( 1.700, 0.054), ( 1.790, 0.046), ( 1.830, 0.038), ( 1.990, 0.036),
    ( 2.030, 0.030), ( 2.070, 0.045), ( 2.108, 0.085),
])

CR_ALL = lut([
    (-2.108, 0.012), (-2.000, 0.020), (-1.860, 0.028), ( 1.700, 0.032),
    ( 1.810, 0.015), ( 2.030, 0.010), ( 2.108, 0.018),
])

STATIONS = [
    -2.108, -2.1015, -2.093, -2.081, -2.066, -2.047, -2.024, -1.998,
    -1.968, -1.934, -1.896, -1.855, -1.805, -1.745, -1.678, -1.605,
    -1.525, -1.440, -1.350, -1.255, -1.155, -1.050, -0.940, -0.825,
    -0.705, -0.580, -0.450, -0.315, -0.175, -0.030,  0.120,  0.270,
     0.420,  0.560,  0.700,  0.835,  0.965,  1.090,  1.205,  1.310,
     1.400,  1.480,  1.555,  1.625,  1.690,  1.735,  1.768,  1.792,
     1.812,  1.834,  1.860,  1.890,  1.920,  1.950,  1.978,  2.000,
     2.018,  2.034,  2.048,  2.062,  2.074,  2.085,  2.094,  2.1015,
     2.108,
]


def build_kombi():
    """the whole van body as one lofted shell -- no cab/rear seam"""
    rings = []
    for x in STATIONS:
        rings.append(ring(x, WX(x), ZB(x), ZT_ALL(x),
                          RB_ALL(x), RT_ALL(x), CR_ALL(x), bcrown=0.012))
    return loft(rings, cap_first=True, cap_last=True, name="T1_body")

# maximum half width
WX = lut([                     # SPEC r4: scaled x1.01744 for W 1.720 -> 1.750
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
RB_ALL = lut([
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
    12.29 deg apart, with a clear 12.7 mm air gap between the V apex and the W
    peak at the locked ring diameter of 0.370 m. V above W, always (SPEC 0.2).
    """
    V_SPINE = [(-0.400, 0.560), (0.000, -0.060), (0.400, 0.560)]
    W_SPINE = [(-0.760, -0.060), (-0.380, -0.700), (0.000, -0.075),
               (0.380, -0.700), (0.760, -0.060)]
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
