"""Wheels, bright-work, lamps, counter, galley, interior."""
import bpy, bmesh, math
from mathutils import Vector, Matrix
import t1_core as T

TAU = math.pi * 2
NEW = []


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
def plank_counter(side=1):
    """cream-PAINTED slab counter cantilevered under the three serving bays
    (SPEC r4 8.5: measured saturation 0.07 - painted, not bare timber)"""
    obs = []
    X0, X1 = 0.9200, -1.3400        # SPEC r4: runs past bay 3 to the tail
    ZT = 1.3620
    y_in, y_out = 0.8450, 1.2450    # deeper slab: reference reads ~0.40 m
    nx = 40
    verts, faces = [], []
    for iy, y in enumerate((y_in, y_out)):
        for ix in range(nx + 1):
            x = X0 + (X1 - X0) * ix / nx
            verts.append((x, side * y, ZT))
            verts.append((x, side * y, ZT - 0.0850))   # thicker: 42 mm did not read
    for ix in range(nx):
        a = ix * 2
        b = a + 2
        c = (nx + 1) * 2 + ix * 2
        d = c + 2
        faces.append((a, b, d, c))                      # top
        faces.append((a + 1, c + 1, d + 1, b + 1))      # bottom
        faces.append((c, d, d + 1, c + 1))              # outer edge
        faces.append((a, a + 1, b + 1, b))              # inner edge
    n = (nx + 1) * 2
    faces.append((0, 1, n + 1, n))
    faces.append((nx * 2, n + nx * 2, n + nx * 2 + 1, nx * 2 + 1))
    me = bpy.data.meshes.new("counter")
    me.from_pydata(verts, [], faces); me.validate()
    ob = bpy.data.objects.new("counter", me)
    bpy.context.collection.objects.link(ob)
    T.fix_normals(ob)
    obs.append(ob)
    for bx in (0.780, 0.120, -0.560, -1.080):
        obs.append(T.solid_prism((bx, side * 0.9900, ZT - 0.0900),
                                 (1, 0, 0), (0, 1, 0), (0, 0, 1),
                                 T.rrect(0.048, 0.300, 0.008, seg=2),
                                 0.030, name=f"bracket{bx}"))
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

    # ---- galley backdrop behind the three serving bays
    # y = -0.480 puts it 1.34 m behind the show-side aperture and clear of
    # every existing fit-out prop (plancha reaches y = -0.46, shelves stop at
    # x = -1.38, seat back is all +Y).
    bx0 = min(min(b) for b in S.BAYS) - 0.090
    bx1 = max(max(b) for b in S.BAYS) + 0.080
    bz0, bz1 = S.Z_SILL - 0.045, S.Z_HEAD + 0.045
    pts = T.rrect(bx1 - bx0, bz1 - bz0, 0.030, seg=3)
    pts = [(u + (bx0 + bx1) / 2, v + (bz0 + bz1) / 2) for (u, v) in pts]
    obs.append(T.solid_prism((0.0, -0.480, 0.0), (1, 0, 0), (0, 0, 1),
                             (0, 1, 0), pts, 0.024, name="galley_backdrop"))
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


def wipers():
    obs = []
    for s in (1, -1):
        a = T.solid_prism((2.012, s * 0.290, 1.392), (1, 0, 0), (0, 1, 0),
                          (0, 0, 1), T.rrect(0.020, 0.300, 0.006, seg=2),
                          0.010, name=f"wblade{s}")
        obs.append(a)
        obs.append(T.cylinder((2.028, s * 0.150, 1.374), (0, 0, 1),
                              0.0085, 0.030, seg=14, name=f"wiper_pivot{s}"))
    return obs


def handles():
    obs = []
    for s in (1, -1):
        y = T.WX(1.100) * T.G(1.330)
        obs.append(T.solid_prism((1.075, s * (y + 0.012), 1.330), (1, 0, 0),
                                 (0, 0, 1), (0, s, 0),
                                 T.rrect(0.115, 0.030, 0.012, seg=3), 0.024,
                                 name=f"handle{s}"))
    return obs


# =============================================================== VW ROUNDEL
def vw_logo(R=0.1385, w=0.0275, x=2.1215, depth=0.0110):
    """V over W built from flat bars in the Y-Z plane. Never inverted."""
    segs = [
        ((-0.400,  0.560), ( 0.000, -0.060)),      # V left
        (( 0.400,  0.560), ( 0.000, -0.060)),      # V right
        ((-0.760, -0.060), (-0.380, -0.700)),      # W outer left
        ((-0.380, -0.700), ( 0.000, -0.075)),      # W inner left
        (( 0.000, -0.075), ( 0.380, -0.700)),      # W inner right
        (( 0.380, -0.700), ( 0.760, -0.060)),      # W outer right
    ]
    obs = []
    for i, (p0, p1) in enumerate(segs):
        a = Vector((p0[0] * R, p0[1] * R))
        b = Vector((p1[0] * R, p1[1] * R))
        d = b - a
        ang = math.atan2(d.y, d.x)
        pts = T.rrect(d.length + w * 0.6, w, w * 0.30, seg=3)
        pts = [(u * math.cos(ang) - v * math.sin(ang),
                u * math.sin(ang) + v * math.cos(ang)) for (u, v) in pts]
        c = (a + b) / 2
        pts = [(u + c.x, v + c.y) for (u, v) in pts]
        obs.append(T.solid_prism((x, 0, 0), (0, 1, 0), (0, 0, 1), (1, 0, 0),
                                 pts, depth, name=f"vwbar{i}"))
    return obs
