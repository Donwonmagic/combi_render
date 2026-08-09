"""
Kombi shell features: windscreen, cab door glazing, serving bays, rear glass,
panel gaps, wheel arches, closed ragtop.  Geometry follows SPEC.md rev 3.
"""
import bpy, bmesh, math
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
DOOR_VENT = [
    (1.6060, 1.4300), (1.7420, 1.4180), (1.7560, 1.4460), (1.7160, 1.7700),
    (1.6900, 1.7880), (1.6060, 1.7860),
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
BAYS = [(0.3130, 0.8200), (-0.3210, 0.1950), (-0.9600, -0.4350)]
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
    return T.solid_prism((-2.20, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0),
                         pts, 0.40, name="cut_rear")


def rear_glass():
    pts = T.rrect(REAR_W - 0.008, REAR_H - 0.008, 0.060, seg=8)
    pts = [(u, v + REAR_Z) for (u, v) in pts]
    return T.solid_prism((-2.0880, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0),
                         pts, 0.006, name="glass_rear")


# --------------------------------------------------------------- wheel arch
ARCH_R = 0.3735                      # rev6: TIRE_R 0.3325 + measured 41 mm
ARCH_Z = T.TIRE_R + T.RIDE_DROP      # concentric with the tyre after the drop


def arch_cutters():
    obs = []
    for x in (T.X_AXLE_F, T.X_AXLE_R):
        for s in (1, -1):
            obs.append(T.cylinder((x, s * 0.735, ARCH_Z), (0, 1, 0), ARCH_R,
                                  0.62, seg=80, name=f"arch{x:.0f}{s}"))
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
# The bottom run now sits at z 0.7800-0.7920 un-dropped (0.715-0.727 above
# ground), clearing the front arch aperture top ARCH_Z + ARCH_R = 0.7710 by
# 9-21 mm.  That is also where a real T1 cab door bottom sits: just proud of
# the front arch crown, with the fixed step panel below it.
DOOR_GAP = [
    (1.8171, 0.7920), (1.8080, 1.1200), (1.7960, 1.4000),
    (1.7600, 1.6280), (1.7220, 1.7620), (1.7020, 1.8020),
    (1.5200, 1.8130), (1.2800, 1.8150), (1.0800, 1.8130), (0.9680, 1.8060),
    (0.9380, 1.7000), (0.9240, 1.4000), (0.9120, 1.0000), (0.9084, 0.7960),
    (1.1000, 0.7840), (1.4000, 0.7800), (1.6500, 0.7840),
]
DOOR_GAP_S = _smooth(_resample(DOOR_GAP, 76), 2)


def door_gaps():
    return [T.gap_prism((0, s * 0.64, 0), (1, 0, 0), (0, 0, 1), (0, s, 0),
                        DOOR_GAP_S, GAPW, 0.48, name=f"gap_door{s}")
            for s in (1, -1)]


# off-side cargo doors, (x, z); tail engine lid, (y, z).  Module level so
# verify.py can assert positively that the shut lines exist in the geometry.
CARGO_GAP = [(u + 0.2000, v + 1.1380)
             for (u, v) in T.rrect(1.3600, 1.4100, 0.045, seg=6)]
ENGLID_GAP = [(u, v + 0.8700)
              for (u, v) in T.rrect(0.9400, 0.5000, 0.055, seg=6)]


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
    return [T.gap_prism((-1.95, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0),
                        ENGLID_GAP, GAPW, 0.55, name="gap_englid")]


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
    """intact folding roof, shown CLOSED: canvas panel + steel frame"""
    canvas = _rag_grid(RAG_HW - 0.028, RAG_X0 - 0.028, RAG_X1 + 0.028, 0.0075)
    frame = []
    m = 0.026
    for (yy0, yy1, xx0, xx1) in (
            (RAG_HW - m, RAG_HW + m, RAG_X0 + m, RAG_X1 - m),
            (-RAG_HW - m, -RAG_HW + m, RAG_X0 + m, RAG_X1 - m)):
        frame.append(_rag_grid((yy1 - yy0) / 2, xx0, xx1, 0.0060, bows=False,
                               nx=48, ny=3, name="ragframe"))
        for v in frame[-1].data.vertices:
            v.co.y += (yy0 + yy1) / 2
        frame[-1].data.update()
    for xc in (RAG_X0, RAG_X1):
        g = _rag_grid(RAG_HW + m, xc, xc, 0.0060, bows=False, nx=1, ny=24,
                      name="ragframe")
        bpy.data.objects.remove(g, do_unlink=True)
    return canvas, frame


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
