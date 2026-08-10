"""Wheels, bright-work, lamps, counter, galley, interior."""
import bpy, bmesh, math, os
from mathutils import Vector, Matrix
import t1_core as T

TAU = math.pi * 2
NEW = []

# ---------------------------------------------------------------- registries
# FLAT              objects that must NOT be smooth-shaded.  build.py's A()
#                   calls shade_smooth() unconditionally, which averages the
#                   normals across a 90 deg pressed edge and turns a louvre
#                   lip or a counter corner into a soft blob.  build.py calls
#                   D.shade_fix() once, after the last A(), to undo that.
# VISIBILITY_WATCH  objects that must be reachable by a camera ray.  See
#                   visibility_fails() at the bottom of this file -- that is
#                   the guard for the defect Task 4 existed to fix.
FLAT = []
VISIBILITY_WATCH = []


def keep(o, mat=None, smooth=True):
    if smooth and o.type == 'MESH':
        o.data.shade_smooth()
    if mat:
        o["mat"] = mat
    NEW.append(o)
    return o


def place(o, loc=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
    from mathutils import Euler
    m = (Matrix.Translation(loc)
         @ Euler(rot, 'XYZ').to_matrix().to_4x4()
         @ Matrix.Diagonal(Vector(scale)).to_4x4())
    for v in o.data.vertices:
        v.co = m @ v.co
    o.data.update()
    return o


# ============================================================== WHEEL / TYRE
def tyre(name="tyre"):
    """5.60-15 bias-ply cross-section; ribbed tread"""
    R = T.TIRE_R
    # sidewall, bead -> shoulder (+Y half)
    up = [
        (0.0530, 0.1905), (0.0625, 0.2020), (0.0705, 0.2220),
        (0.0728, 0.2340),                       # 3  whitewall inner edge
        (0.0745, 0.2500), (0.0752, 0.2760),
        (0.0744, 0.2905),                       # 6  whitewall outer edge
        (0.0735, 0.2980), (0.0690, 0.3110), (0.0640, 0.3195),
        (0.0578, 0.3262),
    ]
    # crowned tread band with four circumferential grooves
    def crown(y):
        return R - 0.0042 * (abs(y) / 0.0522) ** 2
    tread = []
    for (y, d) in [(-0.0522, 0), (-0.0400, 0), (-0.0378, 1), (-0.0300, 1),
                   (-0.0278, 0), (-0.0150, 0), (-0.0128, 1), (-0.0022, 1),
                   (0.0000, 0), (0.0128, 0), (0.0150, 1), (0.0256, 1),
                   (0.0278, 0), (0.0400, 0), (0.0422, 1), (0.0500, 1),
                   (0.0522, 0)]:
        tread.append((y, crown(y) - (0.0080 if d else 0.0)))
    prof = list(up)                                   # +Y sidewall
    prof += tread[::-1]                               # tread, +Y -> -Y
    prof += [(-y, r) for (y, r) in up[::-1]]          # -Y sidewall
    prof += [(-0.0500, 0.1880), (0.0500, 0.1880)]     # inner bead
    # SPEC r4: BLACKWALL. The white ring in the reference is the painted
    # steel rim, not a whitewall band (measured: SPEC 8.1). Single slot -
    # this also removes the materials.clear() index-loss bug (old D2).
    return T.revolve(prof, seg=112, axis='Y', name=name)


def rim(name="rim"):
    """15in steel wheel: barrel + domed disc"""
    prof = [
        (0.0600, 0.1905), (0.0640, 0.1885), (0.0625, 0.1820),
        (0.0560, 0.1795), (0.0520, 0.1720), (0.0480, 0.1660),
        (0.0300, 0.1640), (0.0080, 0.1650), (-0.0080, 0.1700),
        (-0.0200, 0.1790), (-0.0230, 0.1860), (-0.0190, 0.1900),
        (-0.0250, 0.1905), (-0.0300, 0.1880), (-0.0290, 0.1800),
        (-0.0180, 0.1690), (-0.0060, 0.1600), (0.0120, 0.1560),
        (0.0330, 0.1560), (0.0480, 0.1590), (0.0540, 0.1660),
        (0.0570, 0.1760), (0.0560, 0.1840),
    ]
    barrel = T.revolve(prof, seg=96, axis='Y', name=name + "_barrel")
    # disc face (slightly dished)
    disc_prof = [
        (0.0500, 0.1600), (0.0560, 0.1560), (0.0570, 0.1400),
        (0.0520, 0.1200), (0.0450, 0.0900), (0.0430, 0.0620),
        (0.0450, 0.0400), (0.0470, 0.0000),
    ]
    verts, faces = [], []
    seg = 96
    n = len(disc_prof)
    for k in range(seg):
        a = TAU * k / seg
        ca, sa = math.cos(a), math.sin(a)
        for (y, r) in disc_prof:
            verts.append((r * ca, y, r * sa))
        for (y, r) in [(v - 0.010, r2) for (v, r2) in reversed(disc_prof)]:
            verts.append((r * ca, y, r * sa))
    m = 2 * n
    for k in range(seg):
        k2 = (k + 1) % seg
        for i in range(m):
            j = (i + 1) % m
            faces.append((k * m + i, k * m + j, k2 * m + j, k2 * m + i))
    me = bpy.data.meshes.new(name + "_disc")
    me.from_pydata(verts, [], faces); me.validate()
    disc = bpy.data.objects.new(name + "_disc", me)
    bpy.context.collection.objects.link(disc)
    T.fix_normals(disc)
    # five vent holes
    cuts = []
    for i in range(5):
        a = TAU * i / 5 + 0.31
        cuts.append(T.cylinder((0.118 * math.cos(a), 0.048,
                                0.118 * math.sin(a)),
                               (0, 1, 0), 0.0235, 0.10, seg=28,
                               name=f"vent{i}"))
    for c in cuts:
        T.boolean(disc, c)
    T.apply_mods(disc)
    for c in cuts:
        bpy.data.objects.remove(c, do_unlink=True)
    return barrel, disc


def hubcap(name="cap"):
    """large solid RED dome (SPEC rev3.2) -- not a small chrome moon cap"""
    R = 0.1345
    prof = [
        (0.0745, 0.0000), (0.0736, 0.0300), (0.0710, 0.0560),
        (0.0664, 0.0800), (0.0596, 0.1010), (0.0502, 0.1180),
        (0.0378, 0.1288), (0.0236, 0.1342), (0.0120, R),
        (0.0040, R + 0.0025), (-0.0035, R + 0.0010), (-0.0020, R - 0.0060),
        (0.0080, R - 0.0090), (0.0220, 0.1315), (0.0362, 0.1262),
        (0.0484, 0.1155), (0.0576, 0.0988), (0.0644, 0.0780),
        (0.0690, 0.0545), (0.0716, 0.0292), (0.0725, 0.0000),
    ]
    return T.revolve(prof, seg=96, axis='Y', name=name)


def cap_emblem(y, side):
    """white VW in the centre of the red dome"""
    return T.vw_bars(0.0345, 0.0072, (0.0, y + side * 0.0805, 0.0),
                     (1, 0, 0), (0, 0, 1), (0, side, 0), 0.0060,
                     tag=f"capvw{side}")


def wheel_assembly(x, y, steer=0.0):
    grp = []
    t = tyre(f"tyre_{x:.2f}_{y:.2f}")
    keep(t, "rubber")
    b, d = rim(f"rim_{x:.2f}_{y:.2f}")
    keep(b, "wheelpaint"); keep(d, "wheelpaint")
    c = hubcap(f"cap_{x:.2f}_{y:.2f}")
    keep(c, "chrome")
    s = 1 if y > 0 else -1
    for o in (t, b, d, c):
        if s < 0:
            for v in o.data.vertices:
                v.co.y = -v.co.y
            T.fix_normals(o)
        place(o, loc=(x, y, T.TIRE_R), rot=(0, 0, steer))
        grp.append(o)
    return grp


# ================================================================== BUMPERS
def _plan_curve(z, x0, x1, steps=26):
    """(x, y) of the body surface at height z, x0 -> x1"""
    g = T.G(z)
    pts = []
    for i in range(steps + 1):
        x = x0 + (x1 - x0) * i / steps
        pts.append((x, T.WX(x) * g))
    return pts


# rev 10.  Donald read the front bumper as thin.  It is not: the blade section
# measures 0.110 +/- 0.010 m against BUMP_PROFILE's 0.113, and blade/wheel
# 0.166 +/- 0.016 in two frames agreeing to 2 %.  The blade is right and stays.
# The defect is the STANDOFF -- measured >= 0.080 m from the body (0.16 m from
# the tucked skin) against 0.032 m built.  A correct blade held tight against
# the body reads thin because nothing separates it from the shell.  SPEC 10.22.
# rev 10: this was moved to 0.0555 (80 mm of standoff) on a measurement that
# said ">= 0.08 m from the body against 0.032 m built", and then moved BACK,
# because a second, independent method refutes that application.
#
# The second method: the FRONTAL SILHOUETTE of ref_side.jpg. Scanning for the
# left-most vehicle column row by row, the nose crown stands at column 78 and
# the bumper blade's front face at 82-91 -- the bumper is 4-13 px BEHIND the
# crown, i.e. 17-56 mm behind it at the nose station's 231 px/m. At 0.0555 the
# blade lands 63 mm PROUD of the crown, which no scan of the photograph
# supports and which also breaks the locked overall length (4.327 against
# 4.290 +/- TOL -- verify.py caught it, as it should have).
#
# Two independent measurements and one locked dimension now agree against the
# standoff figure AS APPLIED. Most likely the ">= 0.08 m" is measured from the
# tucked apron at bumper height, not from the forward-most nose, and the build
# offsets along the apron normal -- i.e. the two numbers use different datums.
# Reverted pending a third method. SPEC 10.24, logged OPEN not closed.
BUMP_OFF = 0.0075          # standoff so the outer face lands on x = +/-2.140

BUMP_PROFILE = [           # (outward, up)  channel section, 108 mm tall
    (0.000, 0.0560), (0.0150, 0.0532), (0.0225, 0.0430), (0.0248, 0.0210),
    (0.0230, 0.0000), (0.0248, -0.0220), (0.0225, -0.0440),
    (0.0150, -0.0540), (0.000, -0.0570), (0.000, -0.0400),
    (0.0105, -0.0360), (0.0120, 0.0360), (0.000, 0.0400),
]


def bumper(front=True, z=0.4800, name="bumper"):
    """
    Swept channel following the body plan curve.  Traversal order is chosen so
    that sweep()'s side vector (tangent x up) always points OUTBOARD:
      front:  -Y flank forward -> across the flat nose face -> +Y flank back
      rear:   +Y flank aft     -> across the flat tail face -> -Y flank forward
    """
    if front:
        raw = _plan_curve(z, 1.735, 2.108, 30)          # x increasing
        nose = raw[-1]
        seq = [(x, -y) for (x, y) in raw]
        for i in range(1, 12):                          # flat nose face
            seq.append((nose[0], -nose[1] + 2 * nose[1] * i / 12))
        seq += [(x, y) for (x, y) in reversed(raw)]
    else:
        raw = _plan_curve(z, -1.775, -2.108, 28)        # x decreasing
        tail = raw[-1]
        seq = [(x, y) for (x, y) in raw]
        for i in range(1, 12):                          # flat tail face
            seq.append((tail[0], tail[1] - 2 * tail[1] * i / 12))
        seq += [(x, -y) for (x, y) in reversed(raw)]

    n = len(seq)
    path = []
    for i, (x, y) in enumerate(seq):
        j0, j1 = max(0, i - 1), min(n - 1, i + 1)
        tg = Vector((seq[j1][0] - seq[j0][0], seq[j1][1] - seq[j0][1], 0))
        tg.normalize()
        nrm = Vector((tg.y, -tg.x, 0))                  # outboard by construction
        path.append((x + nrm.x * BUMP_OFF, y + nrm.y * BUMP_OFF, z))
    return T.sweep(path, BUMP_PROFILE, up=(0, 0, 1), name=name)


def bumper_irons(front=True):
    obs = []
    x = 2.045 if front else -2.030
    z0, z1 = 0.470, 0.585
    for s in (1, -1):
        pts = T.rrect(0.062, 0.030, 0.010, seg=3)
        obs.append(T.solid_prism((x, s * 0.470, 0.525), (0, 1, 0), (0, 0, 1),
                                 (1, 0, 0), pts, 0.150,
                                 name=f"iron{s}{'F' if front else 'R'}"))
    return obs


# =================================================================== LAMPS
def headlamp(x_off=0.0):
    """returns (chrome ring, lens, bowl) for one side; y positive"""
    R = 0.0862
    ring_prof = [
        (-0.004, R + 0.0165), (0.008, R + 0.0155), (0.019, R + 0.0060),
        (0.0235, R - 0.0060), (0.0195, R - 0.0135), (0.006, R - 0.0155),
        (-0.004, R - 0.0090),
    ]
    ring = T.revolve(ring_prof, seg=72, axis='X', name="hl_ring")
    lens_prof = [
        (0.0000, 0.0000), (0.0060, 0.0300), (0.0110, 0.0520),
        (0.0165, 0.0700), (0.0230, 0.0810), (0.0290, 0.0862),
        (0.0250, 0.0862), (0.0180, 0.0790), (0.0110, 0.0640),
        (0.0055, 0.0400), (0.0000, 0.0150),
    ]
    lens = T.revolve(lens_prof, seg=72, axis='X', name="hl_lens")
    bowl_prof = [
        (0.000, 0.0000), (-0.030, 0.0420), (-0.052, 0.0680),
        (-0.062, 0.0840), (-0.040, 0.0840), (-0.036, 0.0700),
        (-0.020, 0.0440), (0.000, 0.0180),
    ]
    bowl = T.revolve(bowl_prof, seg=64, axis='X', name="hl_bowl")
    return ring, lens, bowl


def bullet_indicator(name="ind"):
    """SPEC rev3.2: amber pod standing proud of the nose on a plinth"""
    base = T.revolve([(0.000, 0.0000), (0.000, 0.0395), (0.0140, 0.0378),
                      (0.0225, 0.0330), (0.0225, 0.0300), (0.0130, 0.0330),
                      (0.000, 0.0345)], seg=48, axis='X', name=name + "_base")
    # rev 10: a measurement pass read the lens as standing ~65 mm proud (the
    # build gives 41.5 mm of its plinth) and the lens was deepened to 87.5 mm
    # of x extent -- then reverted, for the same reason as BUMP_OFF above. The
    # frontal silhouette of ref_side.jpg puts the indicator's front face at
    # column 80 against the nose crown's 78, i.e. the pod is ~9 mm BEHIND the
    # forward-most point of the vehicle. Deepened to 0.0875 it reaches 58 mm
    # PROUD of the crown. So either the 65 mm is measured from a panel that is
    # itself set back from the crown -- in which case the fix is the pod's
    # MOUNTING STATION, not its depth -- or the 65 mm is wrong. Both are
    # geometry changes to the nose that deserve a derivation rather than a
    # guess. Reverted; SPEC 10.24, OPEN.
    lens = T.revolve([(0.0210, 0.0000), (0.0215, 0.0140), (0.0250, 0.0248),
                      (0.0320, 0.0316), (0.0420, 0.0348), (0.0530, 0.0330),
                      (0.0600, 0.0250), (0.0632, 0.0130), (0.0640, 0.0000)],
                     seg=48, axis='X', name=name + "_lens")
    return base, lens


def small_lamp(r=0.032, depth=0.026, name="lamp"):
    prof = [
        (0.000, 0.0000), (depth * 0.45, r * 0.55), (depth * 0.82, r * 0.88),
        (depth, r), (depth - 0.004, r + 0.004), (0.000, r + 0.006),
    ]
    return T.revolve(prof, seg=48, axis='X', name=name)


# ============================================================== VW  ROUNDEL
def roundel(R=0.1680):
    ring_prof = [
        (0.0000, R), (0.0100, R - 0.002), (0.0135, R - 0.012),
        (0.0120, R - 0.024), (0.0030, R - 0.028), (0.0000, R - 0.020),
    ]
    ring = T.revolve(ring_prof, seg=88, axis='X', name="vw_ring")
    disc_prof = [
        (0.0000, 0.0000), (0.0055, R - 0.030), (0.0035, R - 0.024),
        (-0.0060, R - 0.024), (-0.0060, 0.0000),
    ]
    disc = T.revolve(disc_prof, seg=88, axis='X', name="vw_disc")
    return ring, disc


# ================================================================== GUTTER
def gutter():
    prof = [(0.0000, 0.0000), (0.0135, -0.0025), (0.0160, -0.0100),
            (0.0120, -0.0155), (0.0035, -0.0140), (0.0000, -0.0090)]
    obs = []
    xs = [0.442 + (1.806 - 0.442) * (i / 40) for i in range(41)]
    for s in (1, -1):
        path = []
        for x in xs:
            zt = T.ZT_CAB(x); rt = T.RT_CAB(x)
            z = zt - rt * 0.72
            y = T.WX(x) * T.G(z)
            path.append((x, s * (y + 0.0015), z + 0.004))
        pr = [(a * -s, b) for (a, b) in prof]
        obs.append(T.sweep(path, pr, up=(0, 0, 1), name=f"gutter{s}"))
    return obs


# ============================================================ SIDE MOULDING
def moulding(z=1.372):
    prof = [(0.0000, 0.0000), (0.0075, 0.0035), (0.0090, 0.0000),
            (0.0075, -0.0035)]
    obs = []
    for s in (1, -1):
        path = []
        for i in range(37):
            x = 0.905 + (1.800 - 0.905) * i / 36
            y = T.WX(x) * T.G(z)
            path.append((x, s * (y + 0.001), z))
        pr = [(a * -s, b) for (a, b) in prof]
        obs.append(T.sweep(path, pr, up=(0, 0, 1), name=f"mould{s}"))
    return obs


# ======================================================= CANTILEVERED COUNTER
# MEASURED off ref_side.jpg and ref_rear34.jpg.  FRAME: UN-DROPPED -- these
# build in build.py step 6, before step 8b subtracts T.RIDE_DROP = 0.065 from
# every vertex.  Subtract 0.065 for above-ground.
#
#                     measured AG   un-dropped   shipped   error
#   X0 front            +0.918        +0.918      +0.920   ok
#   X1 rear             -2.323        -2.323      -1.340   983 mm SHORT
#   Z top                1.189         1.254       1.362   108 mm high
#   Z bottom             1.082         1.147       1.277   130 mm high
#   thickness            0.107         0.107       0.085   22 mm thin
#   Y outboard            --           1.166       1.245   79 mm proud
#   Y inboard             --           0.845       0.845   ok
#
# Y inboard 0.845 penetrates the flank by ~26 mm at counter height (measured
# body surface 0.8709 at x = -1.34, z = 1.200).  That is correct for a
# cantilever -- the slab is carried by the body, not butted against it.
# !! CNT_X1 INTERACTS WITH verify.py ROW 1 -- READ BEFORE "FIXING" A LENGTH FAIL
# verify._bounds() measures overall length across EVERY mesh object and skips
# only "cyc".  Before this counter existed the rear-most object was the tail
# lamp at x = -2.131, giving L = 4.291 against SPEC's 4.290 -- a 1 mm margin.
# The measured counter tail wrap reaches x = -2.323 (nosing -2.330), so
# verify reports  "length 4.490 vs spec 4.290 (+200 mm)".  That is NOT a
# geometry regression: it is the guard measuring a conversion FITTING as part
# of the vehicle.  SPEC sec.4 explicitly lists a "radiused counter tail
# OVERHANGING the body", and ref_side.jpg measures the overhang at ~0.33 m.
# The fix is one line in verify.py (see visibility_fails() at the bottom of
# this file for the exact text).  Do not shorten the counter to silence it.
CNT_X0, CNT_X1 = 0.9180, -2.4230
CNT_ZT, CNT_ZB = 1.2540, 1.1470             # 107 mm thick
CNT_Y_IN, CNT_Y_OUT = 0.8450, 1.1660        # 321 mm plan depth
# INFERRED, not measured.  ref_rear34.jpg shows the cream slab and its gold
# nosing running continuously round the rear corner and across the tail, and
# shows that the corner is radiused rather than mitred -- but the radius
# itself and the front chamfer are not measurable from the photographs.
CNT_R = 0.1500                              # tail corner radius, in plan
CNT_CH = 0.0500                             # 45 deg front outer corner chamfer
CNT_XA = CNT_X1 + CNT_R                     # -2.173  tail arc tangent point
CNT_YA = CNT_Y_OUT - CNT_R                  #  1.016  tail arc tangent point
CNT_X_IN = CNT_X1 + (CNT_Y_OUT - CNT_Y_IN)  # -2.002  tail leg inner face
CNT_BRACKETS = (0.780, 0.120, -0.560, -1.080, -1.800)


def _counter_outer(side=1, seg=8):
    """outer plan edge: front -> aft -> round the corner -> across the tail"""
    p = [(CNT_X0, CNT_Y_OUT - CNT_CH), (CNT_X0 - CNT_CH, CNT_Y_OUT),
         (CNT_XA, CNT_Y_OUT)]
    for i in range(1, seg + 1):                    # show-side corner 90->180
        a = math.radians(90 + 90 * i / seg)
        p.append((CNT_XA + CNT_R * math.cos(a), CNT_YA + CNT_R * math.sin(a)))
    p.append((CNT_X1, -CNT_YA))
    for i in range(1, seg + 1):                    # off-side corner 180->270
        a = math.radians(180 + 90 * i / seg)
        p.append((CNT_XA + CNT_R * math.cos(a), -CNT_YA + CNT_R * math.sin(a)))
    return [(x, side * y) for (x, y) in p]


def _counter_inner(side=1):
    """inner plan edge, offset from the outer by the constant 321 mm depth.
    At a corner whose radius (150 mm) is smaller than the offset the inner
    edge degenerates to a sharp corner, which is what a real offset does."""
    return [(x, side * y) for (x, y) in
            [(CNT_X0, CNT_Y_IN), (CNT_X_IN, CNT_Y_IN),
             (CNT_X_IN, -CNT_Y_IN), (CNT_XA, -CNT_Y_IN)]]


def plank_counter(side=1):
    """cream-PAINTED slab counter cantilevered under the three serving bays
    and wrapped round the rear corner and across the tail
    (SPEC r4 8.5: measured saturation 0.07 - painted, not bare timber;
     SPEC sec.4: brass edge strip on the counter lip)"""
    obs = []
    plan = _counter_outer(side) + list(reversed(_counter_inner(side)))
    ob = T.solid_prism((0.0, 0.0, (CNT_ZT + CNT_ZB) / 2),
                       (1, 0, 0), (0, 1, 0), (0, 0, 1),
                       plan, CNT_ZT - CNT_ZB, name="counter")
    obs.append(ob)
    FLAT.append(ob)

    # NB the brass nosing is NOT returned here.  build.py:116 calls this
    # through A(..., "countercream"), and A() puts everything it is handed in
    # ASSIGN, whose material loop would then paint the brass strip cream.
    # It is built in counter_nosing() and routed with a null key instead.

    # ---- brackets.  The 5th, at x = -1.80, carries the new tail overhang.
    for bx in CNT_BRACKETS:
        b = T.solid_prism((bx, side * 1.0000, CNT_ZB - 0.0200),
                          (1, 0, 0), (0, 1, 0), (0, 0, 1),
                          T.rrect(0.048, 0.300, 0.008, seg=2),
                          0.040, name=f"bracket{bx}")
        FLAT.append(b)
        obs.append(b)
    return obs


# ================================================================== GALLEY
def galley():
    """cooking fit-out visible through the serving bays"""
    obs = []
    pts = T.rrect(0.470, 2.500, 0.02, seg=3)
    obs.append(T.solid_prism((-0.300, 0.560, 1.1600), (0, 1, 0), (1, 0, 0),
                             (0, 0, 1), pts, 0.470, name="galley_top"))
    pts = T.rrect(0.560, 0.780, 0.02, seg=3)
    obs.append(T.solid_prism((0.520, -0.180, 1.1900), (0, 1, 0), (1, 0, 0),
                             (0, 0, 1), pts, 0.530, name="plancha"))
    pts = T.rrect(1.400, 2.700, 0.02, seg=3)
    obs.append(T.solid_prism((-0.500, 0.000, 0.5400), (0, 1, 0), (1, 0, 0),
                             (0, 0, 1), pts, 0.040, name="van_floor"))
    for i, x in enumerate((-1.500, -1.780)):
        obs.append(T.solid_prism((x, -0.300, 1.4200), (0, 1, 0), (1, 0, 0),
                                 (0, 0, 1), T.rrect(0.900, 0.240, 0.02, seg=2),
                                 0.030, name=f"shelf{i}"))
    return obs


# ================================================================ INTERIOR
def interior():
    obs = []
    pts = T.rrect(1.560, 0.960, 0.05, seg=4)
    obs.append(T.solid_prism((1.360, 0, 0.6400), (0, 1, 0), (1, 0, 0),
                             (0, 0, 1), pts, 0.070, name="cab_floor"))
    pts = T.rrect(0.560, 0.470, 0.05, seg=4)
    obs.append(T.solid_prism((0.980, 0.400, 0.8650), (0, 1, 0), (1, 0, 0),
                             (0, 0, 1), pts, 0.180, name="seat_base"))
    pts = T.rrect(0.560, 0.470, 0.05, seg=4)
    obs.append(T.solid_prism((0.790, 0.400, 1.1900), (0, 1, 0), (0, 0, 1),
                             (1, 0, 0), pts, 0.130, name="seat_back"))
    pts = [(-0.075, 0.0), (0.075, 0.0), (0.090, 0.115), (-0.090, 0.115)]
    obs.append(T.solid_prism((1.800, 0, 1.2450), (1, 0, 0), (0, 0, 1),
                             (0, 1, 0), pts, 1.520, name="dash"))
    w = T.revolve([(0.0, 0.0088), (0.0088, 0.0), (0.0, -0.0088),
                   (-0.0088, 0.0)], seg=56, axis='Z', name="wheel_rim")
    bm = bmesh.new(); bm.from_mesh(w.data)
    for v in bm.verts:
        r = math.hypot(v.co.x, v.co.y)
        if r > 1e-9:
            v.co.x *= (1 + 0.192 / r); v.co.y *= (1 + 0.192 / r)
    bm.to_mesh(w.data); bm.free()
    place(w, loc=(1.640, 0.372, 1.192), rot=(math.radians(72), 0, 0))
    obs.append(w)
    obs.append(T.cylinder((1.735, 0.372, 1.045), (0.30, 0, 0.95), 0.019, 0.42,
                          seg=20, name="col"))
    obs += interior_fill()
    return obs


# ------------------------------------------------------- SPEC sec.6 backing
def _clip_below(pts, zmax):
    """the part of a closed (x, z) outline at or below zmax, closed off flat"""
    out = []
    n = len(pts)
    for i in range(n):
        x0, z0 = pts[i]
        x1, z1 = pts[(i + 1) % n]
        if z0 <= zmax:
            out.append((x0, z0))
        if (z0 - zmax) * (z1 - zmax) < 0.0:
            t = (zmax - z0) / (z1 - z0)
            out.append((x0 + t * (x1 - x0), zmax))
    return out


def interior_fill():
    """Back the through-slots and the serving bays so they read as DEPTH.

    MEASURED before this existed: at the `side` ortho camera 41 of the 76
    rays sampled along the cab-door outline crossed NO surface at all -- the
    two door gaps are collinear slots through both flanks, so the bus was
    see-through along the shut line.  Separately a ray through any of the
    three open serving bays hit nothing but the off-side glass pane at
    3.83 m: three 600 x 396 mm holes with nothing behind them.

    The physically honest fix, and the one that solves both: an inner skin.
    A dark door card 20 mm inboard of the outer skin spanning the door
    outline, and a galley backdrop behind the bays.

    Runs from D.interior(), i.e. AFTER every boolean, so it cannot perturb
    the shell.  All coordinates are UN-DROPPED (build.py step 8b has not run
    yet).  The 20 mm standoff matters: T.flank_y() is wrong by -5.6...+3.9 mm
    off the flat of the flank, so anything nearer than ~10 mm can punch back
    out through the 2.8 mm skin.
    """
    import t1_shell as S
    obs = []

    # ---- cab door: card below the glass, plus a ribbon behind the shut line
    # The outline is the CENTRELINE of a 5.5 mm slot, so a card bounded by it
    # leaves the outer half of the slot open.  The ribbon (+-10 mm, 3.6x the
    # slot) covers the whole groove including the top and side runs, where the
    # card cannot reach without blocking the door glazing.
    ZCARD = 1.4400                      # just above DOOR_MAIN's 1.402-1.438
    lower = _clip_below(S.DOOR_GAP_S, ZCARD)
    for s in (1, -1):
        obs.append(T.conform_solid(lower, s, off=-0.020, thick=0.004,
                                   name=f"doorcard{s}"))
        obs.append(T.conform_ring(S.DOOR_GAP_S, s, 0.020, off=-0.020,
                                  thick=0.004, name=f"doorback{s}"))

    # ---- the galley backdrop USED to be built here, in `dark` (albedo 0.115).
    # MEASURED, ref_side.jpg, inside the cut edge of bay 3: the wall you see
    # through the aperture is sRGB (175.2, 175.3, 174.8) -- neutral to 0.003
    # HSV saturation -- against the vehicle's own cream rear-corner panel in
    # the same frame at (238, 209, 202). An 11.5 %-albedo wall 1.34 m inside an
    # unlit box cannot produce that. It has moved to galley_dressing() below,
    # where it keeps its NAME and its POSITION (both were load bearing -- see
    # verify.py row 11f) and gets a measured albedo and a light to sit under.
    return obs


# =================================================================== GUTTER
def gutter():
    prof = [(0.0000, 0.0000), (0.0135, -0.0025), (0.0160, -0.0100),
            (0.0120, -0.0155), (0.0035, -0.0140), (0.0000, -0.0090)]
    obs = []
    xs = [-1.880 + (1.806 + 1.880) * (i / 60) for i in range(61)]
    for s in (1, -1):
        path = []
        for x in xs:
            zt, rt = T.ZT_ALL(x), T.RT_ALL(x)
            z = zt - rt * 0.72
            path.append((x, s * (T.WX(x) * T.G(z) + 0.0015), z + 0.004))
        pr = [(a * -s, b) for (a, b) in prof]
        obs.append(T.sweep(path, pr, up=(0, 0, 1), name=f"gutter{s}"))
    return obs


# ==================================================================== MISC
def mirrors():
    obs = []
    for s in (1, -1):
        obs.append(T.cylinder((1.815, s * 0.905, 1.545), (0.16, s * 0.98, 0.10),
                              0.0105, 0.185, seg=18, name=f"mir_arm{s}"))
        head = T.revolve([(0.000, 0.0000), (0.014, 0.0620), (0.020, 0.0640),
                          (0.006, 0.0655), (-0.004, 0.0600),
                          (-0.004, 0.0000)], seg=44, axis='Y',
                         name=f"mir_head{s}")
        place(head, loc=(1.845, s * 1.052, 1.567), rot=(0, 0, s * -0.13))
        obs.append(head)
    return obs


# ==================================================================== WIPERS
# The shipped pair were BURIED.  Measured to 0.1 mm by an independent pass:
# the blade centre sat 17.3 mm BEHIND the windscreen plane and 8.5 mm below
# the aperture's lower edge, and every ray from either object toward every
# camera crossed exactly 2 body surfaces -- they rendered as nothing.  The
# geometry was wrong too: rrect(0.020, 0.300, 0.006) extruded along (0, 0, 1)
# is a flat plate lying in the XY plane, not a blade on a 63 deg raked screen,
# and wiper_pivot was a VERTICAL cylinder rather than a spindle normal to the
# cowl.
#
# MEASURED cowl surface (un-dropped): directly outboard of the old pivot the
# skin is at (2.0497, 0.150, 1.3852); 220 mm down-screen at y = +0.150 it is
# at (2.0520, 0.1500, 1.3868) with outward normal (0.791, 0.010, 0.612) --
# 37.7 deg from vertical, and 15.8 mm outboard of the windscreen plane.
# S.WS_N = (0.8886, 0, 0.4588).
COWL_PIVOT = (2.0500, 0.1500, 1.3860)       # un-dropped, |y|
COWL_N = (0.791, 0.010, 0.612)              # outward normal at the pivot
WIPE_LEN = 0.3000                           # blade length, along the screen
WIPE_STANDOFF = 0.0240                      # blade plane, out along WS_N
WIPE_PARK_DEG = 20.0                        # INFERRED: park lean, outboard
                                            # of screen-vertical.  Not
                                            # measurable in any reference we
                                            # hold; bottom-pivot and the
                                            # sweep direction are SPEC sec.4.


def wipers():
    """Two bottom-pivot wipers, period-correct for a 1963 T1.

    The blade is built IN the windscreen plane from S.WS_DIR / S.WS_N and
    pushed WIPE_STANDOFF out along the screen normal; the spindle is built
    along the measured cowl normal, not along +Z.  Everything here is
    registered in VISIBILITY_WATCH so visibility_fails() re-proves, off the
    built mesh, that a camera ray reaches them.
    """
    import t1_shell as S
    obs = []
    N = Vector(S.WS_N).normalized()          # out of the screen
    U = -Vector(S.WS_DIR).normalized()       # up-screen
    ph = math.radians(WIPE_PARK_DEG)
    for s in (1, -1):
        C = Vector((COWL_PIVOT[0], s * COWL_PIVOT[1], COWL_PIVOT[2]))
        Nc = Vector((COWL_N[0], s * COWL_N[1], COWL_N[2])).normalized()

        # spindle: axis along the cowl normal, 4 mm rooted / 30 mm proud
        piv = T.cylinder(tuple(C + Nc * 0.0130), tuple(Nc), 0.0090, 0.0340,
                         seg=16, name=f"wiper_pivot{s}")
        # profile deliberately does NOT close back on the axis: a
        # r=0 -> r=0 segment revolves into a ring of zero-area faces.
        boss = T.revolve([(0.0000, 0.0000), (0.0000, 0.0175),
                          (0.0060, 0.0168), (0.0085, 0.0120)],
                         seg=20, axis='X', name=f"wiper_boss{s}")
        _align_x(boss, Nc, C + Nc * 0.0015)
        obs += [piv, boss]

        # blade + arm live in the screen plane, parked leaning OUTBOARD;
        # the sweep from here is up and inboard (SPEC sec.4).
        S_AX = Vector((0.0, float(s), 0.0))          # outboard, in-plane
        d = (U * math.cos(ph) + S_AX * math.sin(ph)).normalized()
        bb = C + N * (WIPE_STANDOFF - _plane_d(C, S))
        base = bb + d * 0.0500                       # blade starts ON the glass
        tip = base + d * WIPE_LEN                    # 58 mm short of the head
        w = d.cross(N).normalized()                  # in-plane, across blade

        blade = _bar(base, tip, w, N, 0.0130, 0.0075, f"wblade{s}")
        # the arm sits 8 mm PROUD of the blade, as a real one does -- laid in
        # the same plane it was completely hidden behind the blade and the
        # spindle, which visibility_fails() caught: 0 of 24 samples reachable.
        arm = _bar(C + Nc * 0.0280,
                   bb + N * 0.0080 + d * 0.2000, w, N, 0.0075, 0.0055,
                   f"wiper_arm{s}")
        obs += [blade, arm]
        VISIBILITY_WATCH.extend([blade.name, arm.name, piv.name])
    FLAT.extend(o for o in obs if o.name.startswith(("wblade", "wiper_arm")))
    return obs


def _plane_d(p, S):
    """signed distance of p from the windscreen plane, along S.WS_N"""
    return (Vector(p) - S.WS_MID).dot(Vector(S.WS_N).normalized())


def _align_x(ob, axis, origin):
    """rotate a revolve(axis='X') so its axis points along `axis`"""
    a = Vector(axis).normalized()
    q = Vector((1.0, 0.0, 0.0)).rotation_difference(a)
    m = Matrix.Translation(origin) @ q.to_matrix().to_4x4()
    for v in ob.data.vertices:
        v.co = m @ v.co
    ob.data.update()
    return ob


def _bar(p0, p1, side_ax, up_ax, width, thick, name):
    """rectangular bar from p0 to p1, `width` across side_ax, `thick` deep"""
    c = (Vector(p0) + Vector(p1)) / 2.0
    L = (Vector(p1) - Vector(p0)).length
    ax = (Vector(p1) - Vector(p0)).normalized()
    pts = T.rrect(L, width, min(width, thick) * 0.35, seg=2)
    return T.solid_prism(tuple(c), tuple(ax), tuple(Vector(side_ax).normalized()),
                         tuple(Vector(up_ax).normalized()), pts, thick,
                         name=name)


def handles():
    """SPEC sec.4 / 2.3: ICE-PICK pull-lever cab handles.  Push-button
    handles are Dec 1963+, so the lever is the correct part for this bus."""
    obs = []
    for s in (1, -1):
        y = T.WX(1.100) * T.G(1.330)
        base = T.solid_prism((1.075, s * (y + 0.006), 1.330), (1, 0, 0),
                             (0, 0, 1), (0, s, 0),
                             T.rrect(0.115, 0.030, 0.012, seg=3), 0.012,
                             name=f"handle{s}")
        # the lever: a tapered pull standing 22 mm proud, pointed aft
        lever = T.solid_prism((1.060, s * (y + 0.018), 1.330), (1, 0, 0),
                              (0, 0, 1), (0, s, 0),
                              [(-0.048, -0.0075), (0.030, -0.0090),
                               (0.046, -0.0020), (0.046, 0.0020),
                               (0.030, 0.0090), (-0.048, 0.0075)],
                              0.018, name=f"handlever{s}")
        obs += [base, lever]
        FLAT.extend([base, lever])
        VISIBILITY_WATCH.append(lever.name)
    return obs


# =============================================================== VW ROUNDEL
def vw_logo(R=0.1385, w=0.0275, x=2.1215, depth=0.0110):
    """V over W in the Y-Z plane, as TWO closed mitred prisms. Never inverted.

    rev 8: was six independent overlapping bars, the same defect as
    t1_core.vw_bars -- SKEPTIC_PASS sec.D specifies two closed mitred prisms so
    the self-intersection is removed rather than hidden. Both call sites now
    share ONE implementation, which is why they drifted apart in the first place.
    """
    return T.vw_bars(R, w, (x, 0, 0), (0, 1, 0), (0, 0, 1), (1, 0, 0),
                     depth, tag="vwbar")


# ###########################################################################
#                       SPEC sec.4 DETAIL INVENTORY
#
# Everything below is built in build.py step 7, i.e. after solidify and after
# every boolean, so no cutter and no pipeline ordering is involved.
#
# FRAME: UN-DROPPED throughout.  build.py step 8b subtracts T.RIDE_DROP =
# 0.065 from every vertex at the very end, so above_ground = z - 0.065.
# ###########################################################################

def join(objs, name):
    """merge several meshes into one object and remove the originals.
    Keeps the object count down: 10 louvre slots per flank are one object,
    not ten, and 65 fringe balls per aperture are one object, not 65."""
    verts, faces = [], []
    for o in objs:
        base = len(verts)
        verts += [tuple(v.co) for v in o.data.vertices]
        faces += [tuple(base + i for i in p.vertices) for p in o.data.polygons]
    me = bpy.data.meshes.new(name + "_j")
    me.from_pydata(verts, [], faces)
    me.validate()
    ob = bpy.data.objects.new(name + "_j", me)
    bpy.context.collection.objects.link(ob)
    for o in objs:
        bpy.data.objects.remove(o, do_unlink=True)
    # rename only AFTER the sources are gone: joining objects whose target name
    # is already taken silently yields "<name>.001", and the caller then looks
    # up <name>, finds nothing, and the detail vanishes.  That cost the bobble
    # fringe its first build.
    ob.name = name
    ob.data.name = name
    return T.fix_normals(ob)


def shade_fix():
    """flat-shade the pressed / hard-surface details.  Call ONCE from build.py
    after the last A(), because A() force-smooths everything it touches."""
    n = 0
    for ob in FLAT:
        try:
            for p in ob.data.polygons:
                p.use_smooth = False
            ob.data.update()
            n += 1
        except ReferenceError:
            pass
    return n


def _brass(name="brass"):
    """rev 8: brass now lives in t1_mats.build_all() like every other material.

    It was defined here because build_all() had no brass key, which made it the
    last illegitimate CONSTANT-roughness material in the scene (STATE.md counted
    6; five are legitimately exempt -- the transmissive ones and the sealed
    reflector -- and this was the sixth). It now carries a roughness field.
    This shim resolves the shared datablock so the counter nosing and the plate
    surround pick up the real material rather than a private copy.
    """
    m = bpy.data.materials.get(name)
    if m:
        return m
    import t1_mats as _MT
    return _MT.tarnished(name, (0.6600, 0.4750, 0.1750), 0.255, 0.34)


# ============================================== TRUE-SURFACE CONFORMED DECAL
_DELTA = {}


def flank_delta(body, z, side=1,
                xs=(-1.60, -1.25, -0.85, -0.10, 0.40, 0.70)):
    """(measured body surface |y|) - T.flank_y(x, z), median over `xs`.

    T.flank_y() is the loft CAGE's analytic half width; the shell that gets
    rendered is the Catmull-Clark limit of that cage plus a 2.8 mm solidify,
    and below the bottom roll's tangent point (z ~ 0.508 un-dropped) the two
    part company.  MEASURED off the built mesh:

        z (un-dropped)   0.445   0.550   0.700   0.850   0.918   1.085
        surface - flank  +4.5mm  -0.2mm  -0.3mm  -0.0mm  -0.1mm  -0.0mm

    The script decal's bottom edge is at z = 0.445, so a panel placed on
    flank_y() + 1.6 mm sits 2.9 mm INSIDE the sheet metal there and the foot
    of the lockup disappears -- the same class of defect as the buried wipers.
    The error separates as WX(x) . G(z), so one median over several x samples
    is a correction in z alone; the median (not the mean) is what throws out
    the samples that fall down a shut line or through an aperture.
    """
    key = (round(z, 4), side)
    if key in _DELTA:
        return _DELTA[key]
    d = []
    for x in xs:
        ok, loc, _, _ = body.ray_cast(Vector((x, side * 3.0, z)),
                                      Vector((0.0, -side, 0.0)))
        if ok:
            e = abs(loc.y) - T.flank_y(x, z)
            if abs(e) < 0.020:                 # 20 mm: a slot or an aperture
                d.append(e)                    # reads hundreds of mm out
    d.sort()
    v = 0.0 if not d else (d[len(d) // 2] if len(d) % 2 else
                           0.5 * (d[len(d) // 2 - 1] + d[len(d) // 2]))
    _DELTA[key] = v
    return v


def conform_panel_true(body, x0, x1, z0, z1, side, off=0.0016, nx=40, nz=14,
                       name="pn"):
    """T.conform_panel(), but riding the MEASURED body surface.
    UVs identical to T.conform_panel so the texture is not mirrored."""
    verts, faces, uvs = [], [], []
    for iz in range(nz + 1):
        z = z0 + (z1 - z0) * iz / nz
        dy = flank_delta(body, z, side)
        for ix in range(nx + 1):
            x = x0 + (x1 - x0) * ix / nx
            verts.append((x, side * (T.flank_y(x, z) + dy + off), z))
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
    T.fix_normals(ob)
    uvl = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        for li in poly.loop_indices:
            uvl.data[li].uv = uvs[me.loops[li].vertex_index]
    VISIBILITY_WATCH.append(ob.name)
    return ob


# ================================================ REAR-QUARTER AIR LOUVRES
# SPEC sec.4: 10 rear-quarter air-intake louvres PER SIDE (the 10th was added
# in March 1963).  0 of the 20 existed.
#
# MEASURED on ref_side.jpg, FRAME UN-DROPPED:
#   block X            -1.285 ... -1.670   (+-0.03/0.04), length 0.385
#   10 slots, pitch    21.1 mm
#   top slot centre    1.085  (1.020 above ground)
#   bottom slot centre 0.895  (0.830 above ground)
#   slot aperture      ~7 mm  (INFERRED -- 1.5 px, below the photograph's
#                              resolution)
#
# Count: block height 0.189 / pitch 0.0210 = 9 gaps = 10 slots.  Seven slots
# at 21 mm spans 0.126 m, 60 mm short of the measured block.  At 4.5 px pitch
# the signal is under the JPEG 8x8 DCT block, so the failure mode is MERGING;
# under-counting is possible, over-counting is not.
#
# Built HORIZONTAL in the body frame.  Rake measured +3.9 deg but the peak is
# broad (+2.2 ... +4.5) and confounded by JPEG block alignment, and 0-4 deg
# nose-up is not excluded, so horizontal is the defensible choice.
LOUV_X0, LOUV_X1 = -1.2850, -1.6700
LOUV_N = 10
LOUV_Z_TOP, LOUV_Z_BOT = 1.0850, 0.8950
LOUV_PITCH = (LOUV_Z_TOP - LOUV_Z_BOT) / (LOUV_N - 1)          # 0.021111
LOUV_PROFILE = [(0.0000, 0.0000), (0.0080, -0.0020),
                (0.0080, -0.0090), (0.0000, -0.0110)]
LOUV_OFF = 0.0020                       # ride 2 mm proud of the flank


def louvres(nx=13):
    """Pressed-lip sweeps riding the flank, both flanks, 10 per side = 20.

    A sweep, not a boolean: this runs in step 7, after every cut, so the shell
    is never touched.  The 11 mm section is centred on the measured slot
    centre, so slot k sits at LOUV_Z_BOT + k . pitch +- 5.5 mm.
    T.flank_y() is accurate to 0.1 mm over z = 0.884 ... 1.091 (measured), so
    the analytic ride is safe here -- unlike the decal panel further down the
    flank, which needs flank_delta().
    """
    obs = []
    for s in (1, -1):
        parts = []
        for k in range(LOUV_N):
            z = LOUV_Z_BOT + LOUV_PITCH * k
            path = [(LOUV_X1 + (LOUV_X0 - LOUV_X1) * i / nx,
                     s * (T.WX(LOUV_X1 + (LOUV_X0 - LOUV_X1) * i / nx)
                          * T.G(z) + LOUV_OFF), z)
                    for i in range(nx + 1)]
            pr = [(a * -s, b + 0.0055) for (a, b) in LOUV_PROFILE]
            parts.append(T.sweep(path, pr, up=(0, 0, 1),
                                 name=f"louvre{s}_{k}"))
        ob = join(parts, f"louvres{s}")
        FLAT.append(ob)
        VISIBILITY_WATCH.append(ob.name)
        obs.append(ob)
    return obs


# ==================================================== FUEL FILLER FLAP (5.1)
# SPEC sec.4: fuel filler flap on the RIGHT rear quarter, immediately aft of
# the louvres.  Right = -Y = the off side.  The x station and the height are
# INFERRED -- SPEC gives no coordinate and the flap is on the side neither
# photograph shows.  Placed one flap-width aft of the louvre block, centred on
# the louvre band.
FLAP_X, FLAP_Z, FLAP_W, FLAP_H = -1.7950, 1.0100, 0.1450, 0.1450


def filler_flap():
    outline = [(u + FLAP_X, v + FLAP_Z)
               for (u, v) in T.rrect(FLAP_W, FLAP_H, 0.030, seg=5)]
    ob = T.conform_solid(outline, -1, off=0.0040, thick=0.0050,
                         name="fuel_flap")
    FLAT.append(ob)
    VISIBILITY_WATCH.append(ob.name)
    return [ob]


# ============================================= APERTURE BOBBLE FRINGE (5.2)
# SPEC sec.4 (grade R, Tacombi-specific): white bobble / ball-fringe trim
# round each serving aperture.  CONFIRMED present in ref_side.jpg -- a
# scalloped row of white balls runs round the inside edge of all three
# apertures.  Ball diameter and pitch are INFERRED (each ball is ~2 px).
FRINGE_R, FRINGE_PITCH, FRINGE_INSET = 0.0090, 0.0260, 0.0130


def _ball(verts, faces, c, r, nu=7, nv=4):
    base = len(verts)
    verts.append((c[0], c[1], c[2] + r))
    for j in range(1, nv):
        pv = math.pi * j / nv
        for i in range(nu):
            pu = TAU * i / nu
            verts.append((c[0] + r * math.sin(pv) * math.cos(pu),
                          c[1] + r * math.sin(pv) * math.sin(pu),
                          c[2] + r * math.cos(pv)))
    verts.append((c[0], c[1], c[2] - r))
    top, bot = base, len(verts) - 1
    for i in range(nu):
        faces.append((top, base + 1 + i, base + 1 + (i + 1) % nu))
    for j in range(nv - 2):
        a0 = base + 1 + j * nu
        b0 = a0 + nu
        for i in range(nu):
            k = (i + 1) % nu
            faces.append((a0 + i, b0 + i, b0 + k, a0 + k))
    a0 = base + 1 + (nv - 2) * nu
    for i in range(nu):
        faces.append((bot, a0 + (i + 1) % nu, a0 + i))


def _resample_closed(pts, pitch):
    """closed (x, z) polyline -> points at ~`pitch` spacing along it"""
    n = len(pts)
    seg = [(pts[i], pts[(i + 1) % n]) for i in range(n)]
    L = [math.dist(a, b) for (a, b) in seg]
    total = sum(L)
    m = max(4, int(round(total / pitch)))
    out, acc, k = [], 0.0, 0
    for i in range(m):
        want = total * i / m
        while k < n - 1 and acc + L[k] < want:
            acc += L[k]; k += 1
        t = 0.0 if L[k] < 1e-9 else (want - acc) / L[k]
        (ax, az), (bx, bz) = seg[k]
        out.append((ax + (bx - ax) * t, az + (bz - az) * t))
    return out


def bobble_fringe():
    """one merged mesh per aperture: the balls plus the tape they hang on"""
    import t1_shell as S
    obs = []
    for i, (xr, xf) in enumerate(S.BAYS):
        cx, cz = S.bay_centre(i)
        out = [(u + cx, v + cz) for (u, v) in S.bay_outline(i)]
        out = T.poly_offset(out, -FRINGE_INSET)
        pts = _resample_closed(out, FRINGE_PITCH)
        verts, faces = [], []
        for (x, z) in pts:
            y = S.SHOW_SIDE * (T.flank_y(x, z) + 0.0075)
            _ball(verts, faces, (x, y, z), FRINGE_R)
        me = bpy.data.meshes.new(f"fringe{i}")
        me.from_pydata(verts, [], faces); me.validate()
        ob = bpy.data.objects.new(f"fringe{i}", me)
        bpy.context.collection.objects.link(ob)
        T.fix_normals(ob)
        # the tape: a 3 mm ribbon on the rim the balls are sewn to
        tape = T.sweep([(x, S.SHOW_SIDE * (T.flank_y(x, z) + 0.0030), z)
                        for (x, z) in pts + [pts[0]]],
                       [(0.0000, 0.0060), (0.0030, 0.0060),
                        (0.0030, -0.0060), (0.0000, -0.0060)],
                       up=(0, 0, 1), name=f"fringetape{i}", caps=True)
        ob = join([ob, tape], f"fringe{i}")
        VISIBILITY_WATCH.append(ob.name)
        obs.append(ob)
    return obs


# ============================================ DRIP-RAIL BULB STRING (5.3)
# SPEC sec.4 (grade R): string of small bulbs along the drip rail.  CONFIRMED
# in ref_side.jpg -- a line of small warm bulbs runs along the rail above the
# cream band on the show side.  Pitch, bulb size and the fact that it is show
# side only are INFERRED.  Rendered as unlit pearl glass: this project has no
# emissive material and t1_mats is owned elsewhere.
BULB_X0, BULB_X1, BULB_PITCH, BULB_R = -1.8000, 1.7000, 0.1350, 0.0110


def bulb_string(side=1):
    n = int(round((BULB_X1 - BULB_X0) / BULB_PITCH))
    wire, verts, faces = [], [], []
    for i in range(n + 1):
        x = BULB_X0 + (BULB_X1 - BULB_X0) * i / n
        z = T.ZT_ALL(x) - T.RT_ALL(x) * 0.72
        y = side * (T.WX(x) * T.G(z) + 0.0180)
        wire.append((x, y, z - 0.0060))
        _ball(verts, faces, (x, y + side * 0.0020, z - 0.0245), BULB_R,
              nu=8, nv=5)
    me = bpy.data.meshes.new("bulbs")
    me.from_pydata(verts, [], faces); me.validate()
    ob = bpy.data.objects.new("bulbs", me)
    bpy.context.collection.objects.link(ob)
    T.fix_normals(ob)
    flex = T.sweep(wire, [(0.0026, 0.0026), (0.0026, -0.0026),
                          (-0.0026, -0.0026), (-0.0026, 0.0026)],
                   up=(0, 0, 1), name="bulbflex")
    ob = join([ob, flex], "bulb_string")
    VISIBILITY_WATCH.append(ob.name)
    return [ob]


# ================================================= PILLAR MENU CARDS (5.4)
# SPEC sec.4 (grade R): printed menu cards on the pillars between apertures.
# CONFIRMED in ref_side.jpg -- portrait cards with red text on each pillar.
#
# rev 11: SIZE AND HEIGHT MEASURED, and they were not "estimated off the
# aperture edges" -- they were guessed.  Card B, on the pillar between bay 1
# and bay 2, found by the column at which HSV saturation steps from the
# pillar's 0.11-0.13 to the card's 0.21-0.26 and back:
#     cols 432.0 - 452.0 (+-0.5)      rows 327.5 - 397.5 (+-0.5)
# Scaled by the local aperture band, whose two ends are both locked (bay 1
# 324.0-405.6, bay 2 314.8-400.0, linearly interpolated to the pillar station
# gives 319.4-402.8 = 83.4 px for 0.403 m) and by bay 1's width (107 px for
# 0.507 m):
#     CARD_W = 20.0/107  * 0.507 = 0.0948     was 0.0750  (+26 %)
#     CARD_H = 70.0/83.4 * 0.403 = 0.3383     was 0.3000  (+13 %)
#     centre  v = 0.5168 of the band          was the band centre exactly
#            -> z = 1.5667, i.e. 6.8 mm BELOW it
# Card centres check out against the model's pillar stations without moving
# them: measured X +0.884 / +0.256 / -0.388 against built +0.864 / +0.254 /
# -0.378, so only the card itself was wrong.
CARD_W, CARD_H, CARD_Z = 0.0948, 0.3383, 1.5667


def menu_cards():
    import t1_shell as S
    obs = []
    # pillar centres: forward of bay 0, and between the three bays
    xs = [(S.BAYS[0][1] + 0.9080) / 2.0,
          (S.BAYS[0][0] + S.BAYS[1][1]) / 2.0,
          (S.BAYS[1][0] + S.BAYS[2][1]) / 2.0]
    cz = CARD_Z
    for i, cx in enumerate(xs):
        outline = [(u + cx, v + cz)
                   for (u, v) in T.rrect(CARD_W, CARD_H, 0.005, seg=2)]
        ob = T.conform_solid(outline, S.SHOW_SIDE, off=0.0040, thick=0.0040,
                             name=f"menucard{i}")
        FLAT.append(ob)
        VISIBILITY_WATCH.append(ob.name)
        obs.append(ob)
    return obs


# ========================================== "1963" NUMBER-PLATE SURROUND (5.5)
# SPEC sec.4 (grade R): chrome number-plate surround on the engine lid reading
# "1963", EMPTY.  CONFIRMED in ref_rear34.jpg.  The digit forms are schematic
# (seven-segment bars); at the hero scale a digit is ~5 px.  FLAGGED.
PLATE_Z = 0.7800
PLATE_W, PLATE_H = 0.3300, 0.1850
SEG = {                      # a b c d e f g
    "1": "bc", "9": "abcdfg", "6": "acdefg", "3": "abcdg",
}


def _seg_bars(ch, cx, cy, w, h, t):
    """seven-segment digit -> list of (outline, ) rounded-rect outlines"""
    hw, hh = w / 2.0, h / 2.0
    G = dict(a=(cx, cy + hh, w, t), d=(cx, cy - hh, w, t), g=(cx, cy, w, t),
             f=(cx - hw, cy + hh / 2, t, h / 2), b=(cx + hw, cy + hh / 2, t, h / 2),
             e=(cx - hw, cy - hh / 2, t, h / 2), c=(cx + hw, cy - hh / 2, t, h / 2))
    out = []
    for k in SEG.get(ch, ""):
        x, y, bw, bh = G[k]
        out.append([(u + x, v + y) for (u, v) in
                    T.rrect(bw, bh, min(bw, bh) * 0.35, seg=2)])
    return out


def plate_1963(body=None):
    """chrome surround + schematic '1963' on its top rail, on the engine lid"""
    x = -2.1070                                   # measured tail skin at z 0.78
    rails = [(0.0, PLATE_Z + PLATE_H / 2 + 0.0100, PLATE_W, 0.0380),
             (0.0, PLATE_Z - PLATE_H / 2, PLATE_W, 0.0180),
             (-PLATE_W / 2 + 0.0090, PLATE_Z + 0.0050, 0.0180, PLATE_H),
             (PLATE_W / 2 - 0.0090, PLATE_Z + 0.0050, 0.0180, PLATE_H)]
    parts = []
    for i, (cy, cz, w, h) in enumerate(rails):
        parts.append(T.solid_prism((x - 0.0040, 0.0, 0.0), (0, 1, 0), (0, 0, 1),
                                   (-1, 0, 0),
                                   [(u + cy, v + cz) for (u, v) in
                                    T.rrect(w, h, min(w, h) * 0.28, seg=2)],
                                   0.0160, name=f"platerail{i}"))
    frame = join(parts, "plate_1963")
    FLAT.append(frame)
    VISIBILITY_WATCH.append(frame.name)

    dz = PLATE_Z + PLATE_H / 2 + 0.0100
    digits = []
    for i, ch in enumerate("1963"):
        cy = (i - 1.5) * 0.0210
        for j, o in enumerate(_seg_bars(ch, cy, dz, 0.0110, 0.0210, 0.0026)):
            digits.append(T.solid_prism((x - 0.0125, 0.0, 0.0), (0, 1, 0),
                                        (0, 0, 1), (-1, 0, 0), o, 0.0040,
                                        name=f"pd{i}_{j}"))
    d = join(digits, "plate_digits")
    FLAT.append(d)
    return [frame, d]


# =============================== ROOF PEAK VENT / ENGINE LID T-HANDLE (5.6)
def _surface_at(body, origin, direction):
    ok, loc, nor, _ = body.ray_cast(Vector(origin), Vector(direction))
    if not ok:
        return None, None
    return loc.copy(), nor.copy()


def roof_vent(body):
    """SPEC sec.4: roof peak vent over the windscreen.  Schematic -- a raised
    bezel with two ribs on the roof's front slope, not a working flap.
    FLAGGED as inferred: no reference we hold resolves it."""
    loc, nor = _surface_at(body, (1.8120, 0.0, 3.0), (0, 0, -1))
    if loc is None:
        return []
    u = Vector((0.0, 1.0, 0.0))
    w = nor.normalized()
    v = w.cross(u).normalized()
    o = loc + w * 0.0020
    parts = [T.solid_prism(tuple(o), tuple(u), tuple(v), tuple(w),
                           T.rrect(0.3600, 0.0620, 0.0120, seg=4), 0.0090,
                           name="roofvent")]
    for k in (-1, 1):
        parts.append(T.solid_prism(tuple(o + v * (k * 0.0150) + w * 0.0055),
                                   tuple(u), tuple(v), tuple(w),
                                   T.rrect(0.3300, 0.0060, 0.0020, seg=1),
                                   0.0060, name=f"roofvrib{k}"))
    ob = join(parts, "roof_vent")
    FLAT.append(ob)
    VISIBILITY_WATCH.append(ob.name)
    return [ob]


def englid_handle():
    """SPEC sec.4: engine lid T-handle, top centre of the lid.

    Projection held to 30.6 mm.  This is the rear-most object on the vehicle
    and verify.py row 1 measures overall length across EVERY mesh object, so
    the aft extent here is load bearing: at 43 mm proud (the first cut) it
    alone pushed L to 4.310 and raised a warn.  See the note on CNT_X1.
    """
    x = -2.1070                                   # measured tail skin at z 1.03
    z = 1.0300
    base = T.revolve([(0.0000, 0.0000), (0.0000, 0.0250), (0.0075, 0.0235),
                      (0.0100, 0.0170)], seg=24, axis='X', name="englid_esc")
    _align_x(base, Vector((-1.0, 0.0, 0.0)), Vector((x - 0.0020, 0.0, z)))
    stem = T.cylinder((x - 0.0244, 0.0, z), (-1, 0, 0), 0.0060, 0.0140,
                      seg=12, name="englid_stem")
    bar = T.solid_prism((x - 0.0276, 0.0, z), (0, 1, 0), (0, 0, 1), (-1, 0, 0),
                        T.rrect(0.0720, 0.0120, 0.0050, seg=2), 0.0060,
                        name="englid_bar")
    ob = join([base, stem, bar], "englid_handle")
    VISIBILITY_WATCH.append(ob.name)
    return [ob]


# ###########################################################################
#                    GALLEY DRESSING AND GALLEY LIGHT
#
# The three serving apertures are GLASSLESS.  Everything the eye is given at
# hero scale between z = 1.372 and 1.775 over 1.55 m of flank is whatever is
# behind them, and before this section that was one 11.5 %-albedo panel in an
# unlit box.  Measured, side ortho, inside the cut edge with a 25 mm inset:
# the render read display luma 22 / 33 / 24 against the photograph's
# 147 / 157 / 175.
#
# ------------------------------------------------------------ THE MEASUREMENT
# Method for every number below.  `ref_side.jpg`, apertures located by their
# own cut edges (REF_MEASUREMENTS sec.4/5: bay 1 x 323-430 y 324.0-405.6,
# bay 2 x 455-564 y 314.8-400.0, bay 3 x 588-699 y 309.4-398.0), then a
# feature is placed by its FRACTION (u across, v down) of that aperture and
# converted with the aperture's own locked model extents -- SPEC 10.11 and
# RULES 3/4: no ground line, no single px/m scale, and the fraction cancels
# both.  Uncertainty on a fraction read at 12x is +-0.02, i.e. +-10 mm in X
# and +-8 mm in Z.
#
#   feature                          bay  u            v            model
#   utensil rail (hook line)          3   0.02-0.98    0.055        Z 1.753
#   S-hooks on it                     3   .13 .26 .46 .60 .75 .90   X -0.503
#                                                                     -0.572
#                                                                     -0.677
#                                                                     -0.750
#                                                                     -0.829
#                                                                     -0.907
#   two hanging tools                 3   0.13, 0.26   0.05-0.46    Z 1.755-1.59
#   back-wall material change         3   0.34         -            X -0.614
#   worktop slab, front edge          3   0.12-0.52    0.685-0.760  Z 1.501-1.469
#   rack upper rail                   2   0.05-0.95    0.225        Z 1.684
#   rack shelf                        2   0.14-0.86    0.520-0.585  Z 1.565-1.539
#   wrapped item, pale                2   0.52-0.78    0.455-0.530  X -0.073..-0.207
#   wrapped item, green end           2   0.31-0.52    0.500-0.560  X +0.035..-0.073
#   red-labelled row, upper           2   0.02-0.30    0.05-0.35    X +0.185..+0.040
#   red-labelled row, lower           2   0.55-0.80    0.28-0.36    X -0.089..-0.218
#   dark appliance base               2   0.44-0.80    0.86-0.95    Z 1.428-1.392
#   pale stack on a high shelf        1   0.78-0.98    0.03-0.22    Z 1.763-1.686
#   shelf edge under it               1   0.80-0.98    0.22-0.32    Z 1.686-1.646
#
# COLOUR, same crops, mean sRGB / HSV saturation:
#   back wall aft of the seam    (175.2, 175.3, 174.8)  S 0.003  NEUTRAL
#   back wall fwd of the seam    (199.0, 185.8, 172.2)  S 0.135  warm cream
#   worktop slab                 (216.1, 209.9, 205.5)  S 0.049
#   rack rail                    (146.3, 137.0, 132.8)  S 0.092
#   dark appliance base          (116.7, 116.0, 118.2)  S 0.018
#   pale stack, bay 1            (196.4, 191.2, 197.4)  S 0.031
#   amber bottle body            (183.2, 174.3, 150.8)  S 0.177
# and for scale, in the SAME frame:
#   cream rear-corner panel      (237.8, 208.5, 202.2)  L 214.3
#   cream flank above bay 3      (218.6, 187.1, 157.2)  L 191.6
#
# The single most important number in the whole table is the one that is NOT
# an object: NOTHING inside any aperture is darker than display luma 73, and
# the 2nd percentiles are 91 / 106 / 127.  The galley is a bright room.
#
# ------------------------------------------------------------------ THE LIGHT
# The physical reason it is bright is that THE ROOF IS CUT OPEN -- the vehicle
# is a convertible taco stand and both lids stand up over the counter, so the
# galley is daylit from above through a 1.11 x 2.03 m hole.
#
# THE SHELL DOES NOT CUT THAT HOLE.  build.py step 3 issues windscreen, side,
# rear and gap cutters and no roof cutter; `t1_shell.roof_lids()` builds the
# lids as free panels floating over an UNBROKEN roof skin.  So in the model
# the galley is a sealed 2.8 mm steel box and no exterior source can reach it,
# which is why no amount of `fill_galley` outside the flank has ever fixed
# this.  That is reported, not worked around: see the handoff.
#
# Until it is cut, the opening is stood in for HERE, at the plane where it
# physically is -- `gal_ceiling` is an emissive panel at the roof line.  It is
# not a cheat light bolted to the outside of the vehicle; it is the roof
# aperture, in the right place, with the right size, radiating downward.  The
# visible practical (`gal_tube`) is the second source and it is a real fitting
# the real vehicle has to have, because it serves after dark.
#
# Both are single scalars so they can be swept without editing this file:
#     T1_GAL_SKY   roof-aperture stand-in, emissive radiance
#     T1_GAL_LUM   the practical strip light
# ###########################################################################
# SOLVED, not chosen.  Both were swept together (the ratio between them is
# held, so the two sources keep their relative parts) against the display luma
# of the three apertures measured off the side ortho at 900 x 675 with the
# same boxes used on the photograph.  Three points on the film:
#     x1.00  ->  bay 3 read 217.1        (T1_GAL_SKY 6.50, T1_GAL_LUM 22.00)
#     x0.25  ->  bay 3 read 187.6
#     x0.138 ->  bay 3 read 174.8   against the photograph's 175.0
# The middle pair fixes the film's LOCAL slope at 49.0 display codes per
# decade of scene-linear, which is worth writing down: it is not the 70 codes
# a naive AgX two-point fit through middle grey and paper white predicts, and
# the first correction overshot because of it.
GAL_SKY = float(os.environ.get("T1_GAL_SKY", 0.90))
GAL_LUM = float(os.environ.get("T1_GAL_LUM", 3.04))

# Albedos.  SPEC 10.21's rule bites here: a rendered ratio is an albedo ratio
# only between two surfaces of the SAME CLASS under the SAME LIGHT, and the
# galley wall and the exterior cream are the same class under DIFFERENT light,
# so 175/214 may NOT be turned into an albedo.  What the photograph does fix
# is the CHROMATICITY (neutral to 0.003 aft of the seam, warm cream forward of
# it) and a LOWER BOUND: interior illumination cannot exceed exterior, so a
# wall reading 0.82x the cream panel's display luma cannot have an albedo
# below the cream's.  Both are therefore set to painted-white values at or
# above the body cream's 0.735, and the chromaticity is the measured one.
GAL_WHITE = (0.7300, 0.7300, 0.7355)     # neutral, aft of the seam
GAL_CREAM = (0.7500, 0.7040, 0.6420)     # warm, forward of the seam
# Brushed 304 stainless: normal-incidence reflectance 0.55-0.60, satin.  The
# first draft ran 0.615 at roughness 0.36 and the counter-top warmer rendered
# at display 211 against the cream counter's 186 -- BRIGHTER than the paint,
# where the photograph has it at 141 against 210.  That ratio may NOT be
# transferred (SPEC 10.21: a rendered ratio is an albedo ratio only between
# surfaces of the same class, and metal against dielectric is not), so this is
# corrected to the physical figures and no further: a white studio genuinely
# does make a stainless box bright, exactly as it genuinely does desaturate
# the paint, and that is the rig's account to settle, not this one's.
GAL_STEEL = (0.5600, 0.5630, 0.5690)     # brushed stainless, not a mirror
# These three ARE legitimate albedo ratios and SPEC 10.21's rule is satisfied
# rather than violated: each is a diffuse surface measured against the galley
# back wall IN THE SAME PHOTOGRAPH, INSIDE THE SAME ROOM, under the same
# light.  Ratios are taken in LINEAR light after undoing the sRGB encoding,
# then multiplied by the wall's 0.730.
#   dark appliance base  L 116.3 / 175.2 -> lin 0.171/0.428 = 0.400 -> 0.292
#   red-labelled rows    L 139.7 / 175.2 -> 0.253/0.428 = 0.591 -> 0.431
#                        L 148.4 / 175.2 -> 0.286/0.428 = 0.668 -> 0.488
# The first draft of this section had the labelled rows at (0.42, 0.07, 0.05),
# a saturated pillar-box red with luminance 0.148.  That is what they LOOK
# like at 12x and it is not what they MEASURE: the cluster means are
# (152.9, 137.0, 127.8) and (154.7, 146.9, 144.9), HSV saturation 0.164 and
# 0.063.  They are small red marks on a pale ground, and the area mean -- the
# only thing that survives to hero scale -- is a warm mid-tone.
GAL_DARK = (0.2900, 0.2880, 0.2970)      # the appliance base, S 0.018
GAL_RED = (0.5350, 0.3600, 0.3120)
GAL_GREEN = (0.1450, 0.3050, 0.1750)
GAL_AMBER = (0.4600, 0.2650, 0.0450)
GAL_SEAM_X = -0.6140                     # measured back-wall material change

GAL_Y_BACK = -0.4800                     # backdrop plane -- UNCHANGED, see 11f
GAL_Z_TOP = 1.4285                       # dark appliance base, measured top
GAL_Z_WORK = 1.5010                      # worktop slab, measured top


def _gm(name, base, rough=0.42, metal=0.0, spec=0.5, emit=None, estr=0.0,
        rvar=0.09, nscale=160.0):
    """A galley material.  Roughness is NEVER a constant on a diffuse surface
    here: STATE.md counts constant-roughness materials as a defect class and
    calls it the physical definition of the plastic look, so every non-
    emissive material below carries a noise field on Roughness."""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*base, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Specular IOR Level"].default_value = spec
    b.inputs["Subsurface Weight"].default_value = 0.0    # verify row 6b
    if emit is not None:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = estr
    if rvar > 0.0:
        n = nt.nodes.new("ShaderNodeTexNoise")
        n.location = (-640, -220)
        n.inputs["Scale"].default_value = nscale
        n.inputs["Detail"].default_value = 4.0
        n.inputs["Roughness"].default_value = 0.55
        mr = nt.nodes.new("ShaderNodeMapRange")
        mr.location = (-400, -220)
        mr.inputs["From Min"].default_value = 0.32
        mr.inputs["From Max"].default_value = 0.68
        mr.inputs["To Min"].default_value = max(0.02, rough - rvar)
        mr.inputs["To Max"].default_value = min(0.97, rough + rvar)
        mr.clamp = True
        nt.links.new(n.outputs["Fac"], mr.inputs["Value"])
        nt.links.new(mr.outputs["Result"], b.inputs["Roughness"])
    return m


def _gcard():
    """The pillar menu card.

    MEASURED on the card between bay 1 and bay 2, ref_side.jpg (x 432-453,
    y 328-394, 20.4 x 65.7 px = 96 x 311 mm at the local 211.5 px/m):

        whole card      sRGB (225.5, 199.7, 174.5)  L 203.4  S 0.227
        cream pillar    sRGB (250.4, 238.2, 221.5)  L 239.6  S 0.116
        beside it

    So the card is 36 display codes BELOW the pillar it is stuck to and at
    almost exactly TWICE its saturation.  That pair -- darker AND warmer -- is
    the whole read at hero scale, and `capwhite` (0.890, 0.888, 0.872) can
    produce neither.  The layout is resolved at 14x and is the same on all
    three pillars: a thin red rule frames the card; a dark script logo sits in
    the top ~12 %; a red band under it; a body of small warm rows; a red band
    across the bottom ~8 %.  The individual WORDS are 1.5 px tall and are NOT
    MEASURABLE -- what is built is the band structure and the two measured
    colour statistics, not invented text.
    """
    name = "gal_menucard"
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 0.44
    b.inputs["Specular IOR Level"].default_value = 0.34
    b.inputs["Subsurface Weight"].default_value = 0.0
    tc = nt.nodes.new("ShaderNodeTexCoord"); tc.location = (-1200, 0)
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); sep.location = (-1010, 0)
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    # v runs 0 at the card foot to 1 at its head (Generated Z on a conformed
    # panel whose long axis is world Z)
    prev = None
    #  (v0,   v1,   colour)              -- bands, foot -> head
    BANDS = [(0.000, 0.075, (0.4400, 0.0900, 0.0620)),   # red footer
             (0.075, 0.760, (0.7550, 0.6350, 0.5250)),   # warm text body
             (0.760, 0.830, (0.4400, 0.0900, 0.0620)),   # red header band
             (0.830, 0.940, (0.1450, 0.1250, 0.1180)),   # dark script logo
             (0.940, 1.000, (0.8100, 0.7600, 0.6900))]   # cream head margin
    x = -820
    for (v0, v1, col) in BANDS:
        rgb = nt.nodes.new("ShaderNodeRGB"); rgb.location = (x, -260)
        rgb.outputs[0].default_value = (*col, 1)
        if prev is None:
            prev = rgb.outputs[0]
            x += 200
            continue
        gt = nt.nodes.new("ShaderNodeMath"); gt.location = (x, -80)
        gt.operation = 'GREATER_THAN'
        gt.inputs[1].default_value = v0
        nt.links.new(sep.outputs["Z"], gt.inputs[0])
        mix = nt.nodes.new("ShaderNodeMix"); mix.location = (x, 60)
        mix.data_type = 'RGBA'
        nt.links.new(gt.outputs[0], mix.inputs["Factor"])
        nt.links.new(prev, mix.inputs[6])
        nt.links.new(rgb.outputs[0], mix.inputs[7])
        prev = mix.outputs[2]
        x += 200
    # the printed rows: a fine stripe field, so the body reads as TYPE and not
    # as a flat wash at any distance the hero cameras actually stand at
    wv = nt.nodes.new("ShaderNodeMath"); wv.location = (-820, 240)
    wv.operation = 'MULTIPLY'
    wv.inputs[1].default_value = 42.0
    nt.links.new(sep.outputs["Z"], wv.inputs[0])
    wave = nt.nodes.new("ShaderNodeMath"); wave.location = (-640, 240)
    wave.operation = 'FRACT'
    nt.links.new(wv.outputs[0], wave.inputs[0])
    ink = nt.nodes.new("ShaderNodeMath"); ink.location = (-460, 240)
    ink.operation = 'GREATER_THAN'
    ink.inputs[1].default_value = 0.55
    nt.links.new(wave.outputs[0], ink.inputs[0])
    inkc = nt.nodes.new("ShaderNodeRGB"); inkc.location = (-460, 420)
    inkc.outputs[0].default_value = (0.5150, 0.2050, 0.1550, 1)
    imix = nt.nodes.new("ShaderNodeMix"); imix.location = (240, 60)
    imix.data_type = 'RGBA'
    imix.inputs["Factor"].default_value = 0.34
    fac = nt.nodes.new("ShaderNodeMath"); fac.location = (60, 240)
    fac.operation = 'MULTIPLY'
    fac.inputs[1].default_value = 0.34
    nt.links.new(ink.outputs[0], fac.inputs[0])
    nt.links.new(fac.outputs[0], imix.inputs["Factor"])
    nt.links.new(prev, imix.inputs[6])
    nt.links.new(inkc.outputs[0], imix.inputs[7])
    nt.links.new(imix.outputs[2], b.inputs["Base Color"])
    return m


def _gbox(name, x0, x1, y0, y1, z0, z1, r=0.004, seg=2):
    """axis-aligned box from two corners, outline in XZ, extruded along Y"""
    ob = T.solid_prism(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2),
                       (1, 0, 0), (0, 0, 1), (0, 1, 0),
                       T.rrect(abs(x1 - x0), abs(z1 - z0), r, seg=seg),
                       abs(y1 - y0), name=name)
    FLAT.append(ob)
    return ob


def _gcyl(name, c, axis, rad, length, seg=16, smooth=True):
    ob = T.cylinder(c, axis, rad, length, seg=seg, name=name)
    if smooth:
        ob.data.shade_smooth()
    return ob


def galley_dressing():
    """Everything the eye is given through the three serving apertures.

    Returns a flat list of objects that already carry their own materials;
    spec4_details() routes it with a None key so build.py's material loop
    leaves it alone (the same contract counter_nosing() uses).

    DEPTH (Y) IS NOT MEASURABLE.  `ref_side.jpg` is a flank elevation and
    `ref_rear34.jpg` sees the bays at a grazing angle through their own
    frames, so every feature above is located in X and Z and in NEITHER
    photograph in Y.  Y is therefore chosen, not measured, and is chosen to
    two rules: nothing crosses |y| = 0.80 (verify row 11f casts a ray at each
    bay centre and FAILS if the first hit is outboard of that), and nothing
    intersects the fit-out that is already there (galley_top occupies
    y 0.325-0.795 up to z 1.395, the plancha y -0.460-0.100 up to z 1.455).
    """
    import t1_shell as S
    obs = []
    m_white = _gm("gal_white", GAL_WHITE, rough=0.62, spec=0.32, nscale=90.0)
    m_cream = _gm("gal_cream", GAL_CREAM, rough=0.58, spec=0.34, nscale=90.0)
    m_steel = _gm("gal_steel", GAL_STEEL, rough=0.44, metal=1.0, rvar=0.11,
                  nscale=220.0)
    m_dark = _gm("gal_dark", GAL_DARK, rough=0.52, spec=0.40)
    m_red = _gm("gal_red", GAL_RED, rough=0.40, spec=0.45)
    m_green = _gm("gal_green", GAL_GREEN, rough=0.44, spec=0.42)
    m_amber = _gm("gal_amber", GAL_AMBER, rough=0.26, spec=0.55)
    m_pale = _gm("gal_pale", (0.7650, 0.7550, 0.7700), rough=0.48, spec=0.36)
    # the roof aperture t1_shell does not cut, standing in at its own plane
    m_sky = _gm("gal_sky", (0.7600, 0.7600, 0.7600), rough=0.85, spec=0.05,
                emit=(1.000, 0.988, 0.962), estr=GAL_SKY, rvar=0.0)
    # the practical.  Warm-white fluorescent, which is what a taqueria runs.
    m_tube = _gm("gal_tube", (0.8200, 0.8150, 0.7950), rough=0.30, spec=0.40,
                 emit=(1.000, 0.918, 0.790), estr=GAL_LUM, rvar=0.0)

    def A(ob, mat):
        ob.data.materials.append(mat)
        obs.append(ob)
        return ob

    X0, X1 = -1.3000, 1.0400          # galley box, fore-aft
    # ---------------------------------------------------- 1. the liner
    # The backdrop keeps its NAME and its 24 mm slab at y = -0.480 (see
    # interior_fill); it is split at the MEASURED material change.
    A(_gbox("galley_backdrop", GAL_SEAM_X, X0, GAL_Y_BACK - 0.012,
            GAL_Y_BACK + 0.012, 1.2000, 1.8950, r=0.030, seg=3), m_white)
    A(_gbox("gal_backdrop_f", GAL_SEAM_X, X1, GAL_Y_BACK - 0.012,
            GAL_Y_BACK + 0.012, 1.2000, 1.8950, r=0.030, seg=3), m_cream)
    # end returns: without them a 3/4 camera looks along the flank past the
    # ends of the backdrop into unlit body cavity
    A(_gbox("gal_end_f", X1, X1 + 0.030, -0.5000, 0.2600, 1.2000, 1.8600),
      m_cream)
    A(_gbox("gal_end_a", X0 - 0.030, X0, -0.5000, 0.4000, 1.2000, 1.8600),
      m_white)
    # ceiling: pale, and carrying the roof-aperture stand-in
    A(_gbox("gal_ceiling", X0, X1, -0.5200, 0.5400, 1.8600, 1.8780), m_sky)

    # ------------------------------------------- 2. the practical strip light
    # Tucked 20 mm under the head rail so the ortho flank and both studio 3/4
    # cameras see its LIGHT and not its filament, while the eye-height playa
    # camera looks up past the rail and sees the fitting -- which is correct,
    # a serving hatch shows you its strip light.
    A(_gbox("gal_tube_ch", 0.9000, -1.2000, -0.1900, -0.0500, 1.8020, 1.8280),
      m_steel)
    A(_gbox("gal_tube", 0.8900, -1.1900, -0.1820, -0.0580, 1.7880, 1.8020),
      m_tube)

    # ------------------------------------------------------- 3. the worktop
    # Top at the MEASURED 1.501, 32 mm slab.  It is a SHELF, not a counter,
    # and it stops at bay 3: the first draft ran it the length of the galley
    # 0.64 m deep and that is refuted by the photograph twice over -- the pale
    # slab is only present at u 0.12-0.52 OF BAY 3, and in bay 2 the field
    # below the same height reads L 170.3 at v 0.62-0.86, i.e. open lit wall
    # where a counter would have put an overhang shadow.  Rendered with the
    # long counter, bay 2 read p5 = 72.5 against the photograph's 110.8.
    A(_gbox("gal_worktop", -0.4200, -1.1800, -0.4400, -0.1800,
            GAL_Z_WORK - 0.032, GAL_Z_WORK), m_steel)
    # and the cupboard under it is set BACK from the shelf's front edge, which
    # is what lets the ceiling reach it: the photograph reads L 192.0 under
    # the slab, brighter than the wall behind the rack, so it is not in shade
    A(_gbox("gal_work_a", -0.4200, -1.1800, -0.4600, -0.2800, 1.2600,
            GAL_Z_WORK - 0.032), m_white)

    # -------------------------------------- 4. bay 3: utensil rail and tools
    rail_z, rail_y = 1.7530, -0.3600
    A(_gcyl("gal_rail", (-0.3800, rail_y, rail_z), (1, 0, 0), 0.0075, 0.660),
      m_steel)
    for hx in (-0.5030, -0.5720, -0.6770, -0.7500, -0.8290, -0.9070):
        A(_gcyl(f"gal_hook{hx:+.3f}", (hx, rail_y, rail_z - 0.0180),
                (0, 0, 1), 0.0030, 0.0360, seg=8), m_steel)
    # two long thin tools, measured hanging to v 0.45 / 0.47
    for (hx, zb, w) in ((-0.5030, 1.5940, 0.0180), (-0.5720, 1.5860, 0.0230)):
        A(_gbox(f"gal_tool{hx:+.3f}", hx - w / 2, hx + w / 2,
                rail_y - 0.014, rail_y + 0.014, zb, rail_z - 0.024, r=0.006),
          m_steel)

    # ------------------------------------------------ 5. bay 2: the tube rack
    # y is chosen, not measured (see the docstring), but it is not free: at
    # y -0.42..-0.16 the rack stood 60-320 mm off the back wall and shadowed
    # it, and bay 2 rendered at median 143.0 against the photograph's 164.1
    # while bay 3, which has no rack, sat on target.  The photograph shows no
    # such shadow -- the wall behind the rack reads L 165.4 and L 170.3 in the
    # two bands either side of it -- so the rack is carried FORWARD, toward
    # the aperture, where it shades the counter rather than the wall.
    rk_y0, rk_y1 = -0.3200, -0.0600
    for (rz, nm) in ((1.6840, "gal_rack_hi"), (1.5530, "gal_rack_lo")):
        A(_gcyl(nm, (0.2800, (rk_y0 + rk_y1) / 2, rz), (-1, 0, 0), 0.0070,
                0.680), m_steel)
    A(_gbox("gal_rack_shelf", 0.2800, -0.4000, rk_y0, rk_y1, 1.5460, 1.5530,
            r=0.003), m_steel)
    for ux in (0.2700, -0.3900):
        A(_gbox(f"gal_rack_up{ux:+.3f}", ux - 0.006, ux + 0.006,
                rk_y0 + 0.010, rk_y0 + 0.022, 1.5300, 1.6910, r=0.003),
          m_steel)
    # the wrapped item on the shelf: pale body, green end (measured X spans)
    _wy = (rk_y0 + rk_y1) / 2 - 0.020
    A(_gcyl("gal_wrap", (-0.0730, _wy, 1.5760), (-1, 0, 0), 0.0155,
            0.1340), m_pale)
    A(_gcyl("gal_wrap_g", (-0.0730, _wy, 1.5760), (1, 0, 0), 0.0125,
            0.1080), m_green)
    # The two red-labelled rows are FLAT ON THE WALL, not standing on a shelf.
    # The first draft stood them on a shelf of its own invention; the shelf is
    # not in the photograph, and it shadowed the wall it was meant to dress.
    # Flat printed matter is also what the pixels say: HSV saturation 0.164 and
    # 0.063 over the two clusters is small red marks on a pale ground, which is
    # a poster or a taped-up price list, not five red tins.
    _sy = GAL_Y_BACK + 0.012
    for i, hx in enumerate((0.1700, 0.1150, 0.0600)):
        A(_gbox(f"gal_can_u{i}", hx - 0.0225, hx + 0.0225, _sy, _sy + 0.0060,
                1.6340, 1.7550, r=0.004), m_red)
    for i, hx in enumerate((-0.1100, -0.1850)):
        A(_gbox(f"gal_can_l{i}", hx - 0.0300, hx + 0.0300, _sy, _sy + 0.0060,
                1.6300, 1.6620, r=0.004), m_red)
    # the dark appliance base, measured top 1.4285.  Its identity is NOT
    # MEASURABLE -- it is 4 px tall and reads (117, 116, 118); what is built
    # is a low dark block at the measured X span and the measured top.
    A(_gbox("gal_appliance", -0.0320, -0.2180, 0.2600, 0.5000, 1.3950,
            GAL_Z_TOP, r=0.008), m_dark)

    # ------------------------------------------ 6. bay 1: high shelf and stack
    # The forward end of bay 1 is MEASURABLY darker than the back wall and it
    # is clear of the man who works in the aft two thirds: at u 0.05-0.35 the
    # photograph reads (162.0, 145.9, 139.0) L 148.9 over Z 1.755-1.634 and
    # (135.2, 130.8, 130.6) L 131.7 over Z 1.553-1.392, against the same
    # frame's back wall at L 175.2.  That is 0.50-0.62 of the wall's
    # luminance, warm at the top and neutral at the foot.  WHAT it is is NOT
    # MEASURABLE -- a cupboard, a fridge flank, a stack of crates all fit -- so
    # what is built is a full-height mid-tone upright at the measured X span
    # and the measured reflectance ratio, and nothing is claimed about it.
    A(_gbox("gal_upright", 0.6200, 0.8300, -0.4400, -0.0600, 1.2600, 1.7800,
            r=0.010), _gm("gal_upright_m", (0.4450, 0.4020, 0.3800),
                          rough=0.56, spec=0.30, nscale=110.0))
    A(_gbox("gal_shelf_b1", 0.4700, 0.2900, -0.4200, -0.1800, 1.6740, 1.6860,
            r=0.003), m_steel)
    for i, hx in enumerate((0.4200, 0.3600)):
        A(_gbox(f"gal_stack{i}", hx - 0.0270, hx + 0.0270, -0.3900, -0.2100,
                1.6860, 1.7630 - i * 0.0180, r=0.008), m_pale)

    # ------------------------------- 7. counter top, show side (EXTERIOR props)
    # MEASURED in ref_side.jpg.  A stainless warmer stands on the counter and
    # occludes the lower right of bay 3: image x 641-698 -> X -0.686..-0.955
    # by aperture 3's own fraction, top at v -0.31 of the band, i.e. Z 1.495.
    # Its BASE is on the model counter at CNT_ZT; the photograph puts the base
    # 54 mm higher, which is the counter-height residual REF sec.6 already
    # carries (nosing 1.189-1.205 AG measured against 1.240 built) and is not
    # this section's to resolve.  The TOP is matched, because the top is what
    # the aperture read depends on and it is fixed against the locked band.
    cy0, cy1 = 0.9200, 1.1200
    A(_gbox("gal_warmer", -0.6860, -0.9550, cy0, cy1, CNT_ZT, 1.4950,
            r=0.014, seg=3), m_steel)
    A(_gcyl("gal_warmer_tap", (-0.8200, cy1, 1.3100), (0, 1, 0), 0.0170,
            0.0420, seg=12), m_steel)
    # the amber squeeze bottle standing on it -- measured Z 1.501-1.561 with a
    # pale cap over the top 18 mm
    A(_gcyl("gal_sqbottle", (-0.8400, 1.0200, 1.4980), (0, 0, 1), 0.0165,
            0.0470, seg=14), m_amber)
    A(_gcyl("gal_sqcap", (-0.8400, 1.0200, 1.5450), (0, 0, 1), 0.0105,
            0.0170, seg=12), m_pale)
    # two stainless caddies aft of it, image x 715-760, tops at v -0.53
    for i, (bx0, bx1) in enumerate(((-1.0420, -1.1550), (-1.1600, -1.2730))):
        A(_gbox(f"gal_caddy{i}", bx0, bx1, cy0 + 0.010, cy1 - 0.010,
                CNT_ZT, 1.4090, r=0.006), m_steel)
        A(_gbox(f"gal_caddy_fill{i}", bx0 + 0.012, bx1 - 0.012, cy0 + 0.024,
                cy1 - 0.024, 1.3600, 1.4060, r=0.004), m_pale)
    # ref_rear34.jpg: a rank of squeeze bottles with red and yellow caps
    # stands beside the caddies on the tail run of the counter.  Kept forward
    # of x = -2.10: verify row 1 measures overall length across every mesh
    # object except the counter itself and the margin is 17 mm.
    for i, (bx, col) in enumerate(((-1.8600, GAL_RED), (-1.9250, GAL_AMBER),
                                   (-1.9900, GAL_RED),
                                   (-2.0550, (0.5400, 0.4200, 0.0700)))):
        A(_gcyl(f"gal_bot{i}", (bx, 1.0300, CNT_ZT), (0, 0, 1), 0.0195,
                0.1350, seg=14), m_pale)
        A(_gcyl(f"gal_botcap{i}", (bx, 1.0300, CNT_ZT + 0.1350), (0, 0, 1),
                0.0120, 0.0260, seg=12),
          _gm(f"gal_cap{i}", col, rough=0.36, spec=0.45))
    return obs


# ===================================================== step-7 entry point
def spec4_details(body):
    """Everything SPEC sec.4 asks for that build.py does not already call.

    Returns [(objects, material_key or None), ...].  A None key means the
    objects carry a material built HERE and must not be re-assigned by
    build.py's material loop.
    """
    import t1_shell as S
    out = []
    out.append((louvres(), "paint"))                 # pressed body sheet metal
    out.append((counter_nosing(S.SHOW_SIDE), None))  # brass, own material
    out.append((filler_flap(), "paint"))
    out.append((bobble_fringe(), "capwhite"))
    # rev 8: the bulbs are LIT in both in-service photographs and read warm.
    # They rendered unlit pearl white for seven revisions.
    out.append((bulb_string(), "bulb"))
    # rev 11: the cards were `capwhite` (0.890, 0.888, 0.872) against a
    # measured (225.5, 199.7, 174.5) at TWICE the pillar's saturation. They
    # carry their own material now -- see _gcard().
    _cards = menu_cards()
    for _c in _cards:
        _c.data.materials.append(_gcard())
    out.append((_cards, None))
    # rev 11: everything visible through the three serving apertures
    out.append((galley_dressing(), None))
    out.append((plate_1963(), "chrome"))             # SPEC sec.4: CHROME
    out.append((roof_vent(body), "paint"))
    out.append((englid_handle(), "chrome"))
    return out


def counter_nosing(side=1):
    """SPEC sec.4: brass edge strip on the counter lip.  CONFIRMED in
    ref_rear34.jpg and ref_side.jpg -- a gold nosing runs the whole outer edge
    of the cream slab, round the rear corner and across the tail.  Section
    (7 mm proud, 34 mm deep) is INFERRED; the strip itself is not."""
    path = [(x, y, CNT_ZT) for (x, y) in _counter_outer(side)]
    prof = [(0.0000 * side, 0.0012), (0.0060 * side, -0.0020),
            (0.0070 * side, -0.0300), (0.0000 * side, -0.0340)]
    strip = T.sweep(path, prof, up=(0, 0, 1), name="counter_nosing")
    strip.data.materials.append(_brass())
    FLAT.append(strip)
    VISIBILITY_WATCH.append(strip.name)
    return [strip]


# ###########################################################################
#                          VISIBILITY ASSERTION
#
# Task 4's defect -- two wipers buried 30 mm inside the nose skin, rendering
# as nothing -- passed every guard in the project, because nothing tested
# that a detail could actually be SEEN.  This is that test, measured off the
# built mesh with the real hero camera positions.
#
# Add ONE line to verify.py, in run(), immediately before the
# 'log("  VERIFY: %d fail, %d warn" ...)' line:
#
#     fails += __import__("t1_detail").visibility_fails()
#
# A SECOND one-line change to verify.py is needed as well, for a different
# reason -- row 1 measures overall length across every mesh object, and the
# measured counter tail wrap is a fitting that overhangs the body by design
# (SPEC sec.4).  In _bounds(), widen the skip list:
#
#     if ob.type != 'MESH' or ob.name in ("cyc", "counter", "counter_nosing"):
#
# Without it verify reports 'length 4.490 vs spec 4.290 (+200 mm)'.  With it,
# both guards are 0 fail 0 warn.  See the note on CNT_X1.
# ###########################################################################
HERO_CAMS = ["hero34f", "hero34r", "front34", "low34", "detail_f"]


def _cam_locs():
    try:
        import studio as _ST
        V = _ST.views()
        return [tuple(V[k]["loc"]) for k in HERO_CAMS if k in V]
    except Exception:
        return [(9.30, 6.52, 2.90), (-8.60, 6.90, 3.10), (10.10, -5.00, 2.35),
                (9.00, 6.10, 1.30), (4.90, 2.15, 1.85)]


def _frame_dz():
    """studio's camera positions are in the RENDER frame; the mesh is only in
    that frame once build.py step 8b has run."""
    try:
        import __main__
        return 0.0 if getattr(__main__, "RIDE_DROP_APPLIED", True) \
            else -T.RIDE_DROP
    except Exception:
        return 0.0


def visibility_fails(names=None, shell="T1_body", nsample=28, log=None):
    """Fail any watched detail that NO hero camera can reach.

    The cast runs FROM the camera TOWARD each sample point, and the sample
    counts as seen only when the first thing the ray lands on is the object
    itself.  Casting the other way round -- outward from the detail -- does
    not work: the ray's first hit is then the far wall of the detail's own
    solid, which is not the body shell, so a wiper buried 30 mm inside the
    nose skin scores 100 % visible.  That false pass was measured, on this
    model, before this was turned round.

    Details legitimately hidden from one viewpoint (the off-side louvres from
    a front-left camera) are fine: the test is reachability from AT LEAST ONE
    of the hero cameras.
    """
    fails = []
    dz = _frame_dz()
    cams = [Vector((c[0], c[1], c[2] + dz)) for c in _cam_locs()]
    sc = bpy.context.scene
    dg = bpy.context.evaluated_depsgraph_get()
    for nm in (names if names is not None else VISIBILITY_WATCH):
        ob = bpy.data.objects.get(nm)
        if ob is None or ob.type != 'MESH':
            fails.append(f"visibility: '{nm}' does not exist")
            continue
        vs = [ob.matrix_world @ v.co for v in ob.data.vertices]
        step = max(1, len(vs) // nsample)
        pts = vs[::step][:nsample]
        best, best_cam, blocker = 0, "", {}
        for ci, cam in enumerate(cams):
            seen = 0
            for p in pts:
                d = (p - cam)
                dist = d.length
                d.normalize()
                r = sc.ray_cast(dg, cam, d, distance=dist + 0.010)
                if r[0] and r[4] is ob:
                    seen += 1
                elif r[0] and r[4] is not None:
                    blocker[r[4].name] = blocker.get(r[4].name, 0) + 1
            if seen > best:
                best, best_cam = seen, (HERO_CAMS[ci] if ci < len(HERO_CAMS)
                                        else str(ci))
        if best == 0:
            who = sorted(blocker.items(), key=lambda kv: -kv[1])[:3]
            fails.append(
                f"visibility: '{nm}' is INVISIBLE -- from every hero camera "
                f"({', '.join(HERO_CAMS[:len(cams)])}) the first surface the "
                f"ray lands on is never this object, for all {len(pts)} "
                f"sampled points. Occluders: "
                + ", ".join(f"{k} x{v}" for k, v in who))
        elif log:
            log(f"  visible {nm}: {best}/{len(pts)} via {best_cam}")
    return fails
