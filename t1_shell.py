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


def arch_cutters():
    obs = []
    for x in (T.X_AXLE_F, T.X_AXLE_R):
        for s in (1, -1):
            obs.append(T.cylinder((x, s * 0.735, arch_z(x)), (0, 1, 0), ARCH_R,
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
DOOR_GAP = [
    (1.8171, 0.8120), (1.8080, 1.1200), (1.7960, 1.4000),
    (1.7600, 1.6280), (1.7220, 1.7620), (1.7020, 1.8020),
    (1.5200, 1.8130), (1.2800, 1.8150), (1.0800, 1.8130), (0.9680, 1.8060),
    (0.9380, 1.7000), (0.9240, 1.4000), (0.9120, 1.0000), (0.9084, 0.8160),
    (1.1000, 0.8040), (1.4000, 0.8000), (1.6500, 0.8040),
]
DOOR_GAP_S = _smooth(_resample(DOOR_GAP, 76), 2)

# STRUCTURAL GUARD (SPEC sec.10.6): a panel-gap outline must not cross the lip
# of another aperture. Checked here, at import, so a change to the rake or to
# the arch can never silently re-open the SUB=2 collapse.
_ARCH_TOP_F = arch_z(T.X_AXLE_F) + ARCH_R
_ARCH_X0, _ARCH_X1 = T.X_AXLE_F - ARCH_R, T.X_AXLE_F + ARCH_R
_over_arch = [z for (x, z) in DOOR_GAP_S if _ARCH_X0 <= x <= _ARCH_X1]
assert not _over_arch or min(_over_arch) > _ARCH_TOP_F + 0.010, (
    "cab-door shut line crosses the front wheel arch lip: outline reaches "
    "z=%.4f over the arch (x %.3f..%.3f) whose top is %.4f. This collapses the "
    "boolean at T1_SUB=2. Raise the bottom run or lower the arch."
    % (min(_over_arch), _ARCH_X0, _ARCH_X1, _ARCH_TOP_F))


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

    return [T.solid_prism((cx, cy, zlo), (1, 0, 0), (0, 1, 0), (0, 0, 1),
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

    # ---- prop strut, hinge side to free edge
    for (ob, xs, deg, w) in ((main, LID_X1 + 0.16, LID_OPEN_DEG, LID_W),):
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
