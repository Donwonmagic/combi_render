"""playa_env.py -- procedural vegetation and set dressing for the Playa scene.

SELF-CONTAINED. Imports nothing from this project. One entry point:

    import playa_env; playa_env.build(seed=0)   ->  dict of counts

Every number in this file is traceable to /home/claude/work/measure/playa_env.md
(the measurement of ref_rear34.jpg). Section references below are to that report.

WHAT THIS MODULE DELIBERATELY DOES NOT DO  (all four are measured absences)
--------------------------------------------------------------------------
  * no lamps of any kind -- no sun, no dapple gobo, no HDRI sun     (report S3.6)
  * no volumetric fog / no world volume: airlight bound dY < 0.004  (report S6)
  * no papel picado / bunting: the top-of-frame band is a continuous
    polychrome FLOWERING mass, 55.1 % green / 13.4 % crimson /
    5.5 % cream florets, jagged interpenetrating lower edge         (report S4.1)
  * no orange grade: brightest vs darkest ground in the whole frame is
    da* -0.6, db* +2.4 -- the shadows are WARMER, not bluer          (report S3.5)

THE ONE NUMBER THAT DECIDES WHETHER THIS READS
----------------------------------------------
Foliage median linear luminance must land at 0.104-0.113 x the cream
bodywork's median (report S2.2 / S7.1).  In L* that is a 52.1 unit gap
(foliage L* 32.7 against cream L* 84.8).  FOLIAGE_GAIN below is the single
scalar that sets it; it was tuned by rendering and measuring, not guessed --
see the header note on FOLIAGE_GAIN for the achieved figure.

GEOMETRY / WORLD FRAME
----------------------
Project frame: bus centred on the origin, nose +X, tail -X, counter (left)
flank +Y, Z up, ground z = 0, roof 1.923 m.

The reference photograph's camera is recovered here (REF_CAM / REF_AXIS_DEG)
from the report's own pose solve: rear-wheel ellipse minor/major 0.348 puts the
view ray 20.37 deg off the bus's long axis, the hub sits at image x 753.2 with
Z = 3.84 m, f = 1200 px.  That gives camera (-4.83, +2.22, 1.90) with the
optical axis 13.1 deg off the bus axis -- and it is confirmed by an
independent feature the solve never saw: it predicts the bus's far (nose) top
corner at image x = 554.6, and the report reads the cream lid panel as
beginning at x = 555.

Every mass in report S1 is then placed by inverting (image column, depth Z)
back to world XY through that camera, so the eleven masses sit at their
MEASURED depths and heights.  Beyond the measured wedge the same planting
vocabulary is continued around the terrace so that any hero camera has a close
green wall behind the vehicle rather than an empty pale plain.
"""

import math
import random

import bpy
import numpy as np
from mathutils import Vector

# --------------------------------------------------------------------------
# tuning
# --------------------------------------------------------------------------

PREFIX = "pl_"                 # everything this module makes is named pl_*

#: Single scalar on every foliage albedo.  TUNED BY MEASUREMENT, not guessed.
#: Measured in the standalone rig /home/claude/work/measure/veg_test.py, which
#: builds a cream box at the bus's 4.30 x 1.75 x 1.92 m and lights the scene
#: per report S3 (one large low lateral area source, dark absorbing surround),
#: then takes medians of scene-linear luminance over geometric masks.
#: The rig it was tuned on reproduces the report's OWN surface measurements as
#: an independent check: one 8.5 x 5.0 m area light at azimuth 89 deg,
#: elevation 10 deg, 9.5 m out, 306 W; a uniform world at 0.30; a dark canopy
#: disc (r 11.6 m at z 7.5) and palapa roof, all camera-invisible.  That rig
#: renders the same cream at flank : 72-deg-fascia = 4.00 : 1 (report 3.95) and
#: up-facing : 72-deg-fascia = 1.91 : 1 (report 1.87), and puts the up-facing
#: cream at 0.787 where the report reads 0.772 -- a surface never fitted to.
#:
#: ACHIEVED, seed 0, 640 x 439, 32 samples, medians of scene-linear luminance
#: taken through geometric object-ID masks (measure/veg_test.py):
#:   foliage (all green incl. lawn) : cream median = 0.1093  target 0.104-0.113
#:   canopy only                    : cream median = 0.1074  report  0.1083
#:   grass                          : cream median = 0.1598  report  0.159
#:   foliage L* p5/25/50/75/95 = 18.5 / 25.8 / 32.2 / 41.0 / 57.0
#:              report          13.8 / 24.2 / 32.7 / 43.8 / 65.1
#:   L* gap cream - foliage    = 52.6                report  52.1
#: The resulting canopy albedo is luminance 0.117 -- a real leaf, not a number
#: bent to fit.
FOLIAGE_GAIN = 1.681

#: The lawn is measured separately and sits higher than the canopy: report
#: S2.1 gives grass median Y 0.1041 against foliage 0.0742, i.e. grass : cream
#: = 0.159 where the canopy is 0.113.  Tuned the same way, by measurement.
#: Achieved grass : cream = 0.1598 (report 0.159).
GRASS_GAIN = 1.15

ROOF = 1.923                   # bus roof height, the scale datum (report S0.1)

# ---- the reference photograph's camera, recovered from report S0 -----------
REF_F_PX = 1200.0              # focal length in px for the 1200 x 824 crop
REF_W_PX, REF_H_PX = 1200.0, 824.0
REF_HORIZON_ROW = 230.0        # report S0.2
REF_CAM = (-4.829, 2.222, 1.90)
REF_AXIS_DEG = -13.09          # optical-axis azimuth in the XY plane

# ---- the measured lawn / terrace boundary (report S1 layer table, S5) ------
# Traced at image (520, 598) and (400, 618); inverted through the camera those
# are world (1.30, 1.22) and (1.12, 1.85).  Half-plane form n.p = d.
EDGE_N = (0.9614, 0.2752)
EDGE_D = 1.585

# Beyond the measured wedge the planting belt starts here (m from bus centre).
BELT_R_IN = 9.6
BELT_R_OUT = 17.5

# Report S1 layer table: "Z 3.8 - 6.0 m  paved terrace, tables, chairs (no
# planting)" and "Z 5.9 m  lawn near edge".  So nothing green stands within
# 5.9 m of the reference viewpoint, in any direction -- that is the terrace.
TERRACE_R = 5.90

# Camera stations that must stay clear of planting, plus their sightlines to
# the vehicle.  These are studio.py's two "playa" views; hardcoded rather than
# imported so this module never depends on a file another process is editing.
KEEPOUT_CAMS = ((3.15, 5.75), (6.40, 6.90), (-4.829, 2.222))
KEEPOUT_R = 2.10               # clear disc around each station
SIGHTLINE_R = 1.55             # clear corridor from each station to the bus


# --------------------------------------------------------------------------
# colour helpers -- every target below is a MEASURED sRGB median from the report
# --------------------------------------------------------------------------

def _lin(srgb8):
    """8-bit sRGB -> linear float triple."""
    o = []
    for c in srgb8:
        c = c / 255.0
        o.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(o)


def _scale(rgb, k):
    return tuple(min(1.0, c * k) for c in rgb)


def _lum(rgb):
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]


# Measured medians (report S1 table, S4, S5).  These are RENDERED APPEARANCES,
# not albedos; the albedo is appearance / (how much light that class receives),
# which for the foliage is what FOLIAGE_GAIN carries.
C_CANOPY      = (70, 80, 37)     # P3 feather-palm canopy   L* 32.4  C* 24.2
C_CANE        = (59, 70, 36)     # P4 cane palm             L* 28.1  C* 20.0
C_PADDLE      = (95, 116, 42)    # P5 Musa/Heliconia paddle L* 45.6  C* 38
C_UNDERSTOREY = (60, 69, 18)     # P8 dark shrub layer      L* 27.6  C* 27.6
C_GRASS       = (78, 96, 36)     # P7 lawn                  L* 38.6  C* 29.6
C_GRASS_GAP   = (38, 44, 22)     # the shadowed inter-blade gap (grass Y p5)
C_AGAVE       = (75, 83, 42)     # P6 strap-leaf rosette    L* 33.8  C* 25.1
C_BANDGREEN   = (82, 107, 39)    # P9 band, green fraction  L* 42.9  C* 33.0
C_CRIMSON     = (158, 86, 63)    # P9 band, flower heads    L* 45.4  C* 34.8
C_FLORET      = (178, 170, 145)  # P9 band, cream florets   L* 69.7  C* 16.3
C_SHADEFLOOR  = (30, 34, 20)     # the canopy's shadow floor: report S6 measures
#                                  it CONSTANT with depth, Y p5 0.0141-0.0190
C_TRUNK       = (106, 87, 67)    # P1 palm trunk  C* 13.7 -- near neutral (S7.3)
C_STEM_RINGED = (105, 97, 70)    # P2 ringed stem
C_CANE_STEM   = (126, 108, 62)   # slim tan/olive canes
C_TIMBER      = (77, 67, 29)     # fence lower rail, weathered
C_TIMBER_MOSS = (76, 85, 47)     # fence upper rail, overgrown
C_POST_DARK   = (58, 32, 25)     # the one dark fence post
C_SIGN_FRAME  = (208, 177, 111)  # ochre, C* 30.9, beaded rails
C_SIGN_HEAD   = (193, 173, 89)   # header field, C* 41.8
C_SIGN_FIELD  = (216, 206, 194)  # white field, L* 83.4
C_SIGN_INK    = (70, 62, 50)     # lettering -- warm dark grey, NOT black
C_LAMINATE    = (195, 167, 112)  # table top
C_ALU         = (154, 145, 129)  # table edge band, C* 10.7
C_VINYL       = (195, 110, 68)   # chair vinyl, C* 43.8
C_CHROME      = (207, 199, 186)  # chair frame
C_STAINLESS   = (204, 197, 184)  # napkin dispenser
C_GINGHAM_G   = (143, 173, 127)  # cloth green squares
C_GINGHAM_W   = (175, 199, 164)  # cloth "white" squares -- NOT white (S4.4)
C_OXBLOOD     = (89, 38, 33)     # palapa painted panel
C_SCROLL      = (161, 142, 116)  # its cream scrollwork
C_BOARD_GREEN = (59, 124, 67)    # green painted board, C* 43.8 -- man-made
C_POLESCREEN  = (126, 90, 48)    # rustic vertical-pole screen
C_PENDANT     = (160, 164, 154)  # spun metal dome, C* 6.6
C_MINT        = (168, 196, 178)  # the rolled mat / coiled hose by the trunk

#: Non-foliage classes.  Their measured sRGB medians are appearances, not
#: albedos, so they need dividing by however much light that class actually
#: receives.  Anchored on the report's own unclipped pair: cream of albedo
#: Y 0.624 reads 0.412 where it is turned 72 deg from the opening and 1.67
#: where it faces it, so appearance / albedo runs 0.66 to 2.7 across the set.
#: The dressed props sit in the palapa's own light, between those two, hence
#: 0.80.  This scalar cannot move the foliage measurement -- the leaf, flower,
#: floret, shadow-floor and lawn-gap materials are all on FOLIAGE_GAIN.
DRESS_GAIN = 0.80


# --------------------------------------------------------------------------
# scene plumbing
# --------------------------------------------------------------------------

_COLL = None
_RNG = None
_NPR = None
_COUNT = None
_MESHPOLY = 0        # unique polygons actually created
_EVALPOLY = 0        # polygons after instancing


def _purge():
    """Remove only what a previous build() made.  Never touches anything else."""
    for ob in [o for o in bpy.data.objects if o.name.startswith(PREFIX)]:
        bpy.data.objects.remove(ob, do_unlink=True)
    for db in (bpy.data.meshes, bpy.data.curves, bpy.data.materials,
               bpy.data.node_groups):
        for d in [x for x in db if x.name.startswith(PREFIX)]:
            try:
                db.remove(d, do_unlink=True)
            except Exception:
                pass
    for c in [c for c in bpy.data.collections if c.name.startswith(PREFIX)]:
        try:
            bpy.data.collections.remove(c)
        except Exception:
            pass


def _new_coll():
    c = bpy.data.collections.new(PREFIX + "env")
    bpy.context.scene.collection.children.link(c)
    return c


def _mesh(name, verts, faces, smooth=True):
    global _MESHPOLY
    me = bpy.data.meshes.new(PREFIX + "msh_" + name)
    me.from_pydata([tuple(v) for v in verts], [], [tuple(f) for f in faces])
    me.validate(verbose=False)
    me.update()
    if smooth and len(me.polygons):
        try:
            me.shade_smooth()
        except Exception:
            for p in me.polygons:
                p.use_smooth = True
    _MESHPOLY += len(me.polygons)
    return me


def _poly_area(me):
    return float(sum(p.area for p in me.polygons))


def _put(name, me, loc=(0, 0, 0), rot=(0, 0, 0), scale=1.0, cls=None):
    global _EVALPOLY
    ob = bpy.data.objects.new(PREFIX + name, me)
    ob.location = loc
    ob.rotation_euler = rot
    ob.scale = (scale, scale, scale) if isinstance(scale, (int, float)) else scale
    _COLL.objects.link(ob)
    _EVALPOLY += len(me.polygons)
    if cls:
        _COUNT[cls] = _COUNT.get(cls, 0) + 1
    return ob


# --------------------------------------------------------------------------
# materials
# --------------------------------------------------------------------------

def _base_mat(name):
    m = bpy.data.materials.new(PREFIX + "mat_" + name)
    m.use_nodes = True
    nt = m.node_tree
    return m, nt, nt.nodes["Principled BSDF"], nt.nodes["Material Output"]


def _varied_colour(nt, rgb, spread=0.34, noise_scale=5.5):
    """Per-instance and per-leaf value variation around `rgb`.

    Report S2.1: the foliage is not one value -- L* p5/p50/p95 = 13.8/32.7/65.1.
    Most of that spread comes from the lighting and self-shadowing, but a canopy
    of identically-coloured leaves still reads as plastic, so a little albedo
    variation is carried per instance (Object Info -> Random) and per leaf
    (object-space noise).
    """
    dark = _scale(rgb, 1.0 - spread)
    lite = _scale(rgb, 1.0 + spread)
    oi = nt.nodes.new("ShaderNodeObjectInfo")
    m1 = nt.nodes.new("ShaderNodeMix")
    m1.data_type = 'RGBA'
    m1.inputs[6].default_value = (*dark, 1.0)
    m1.inputs[7].default_value = (*lite, 1.0)
    nt.links.new(oi.outputs["Random"], m1.inputs[0])

    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = noise_scale
    nz.inputs["Detail"].default_value = 3.0
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    m2 = nt.nodes.new("ShaderNodeMix")
    m2.data_type = 'RGBA'
    m2.inputs[0].default_value = 0.55
    nt.links.new(nz.outputs["Fac"], m2.inputs[0])
    nt.links.new(m1.outputs[2], m2.inputs[6])
    mul = nt.nodes.new("ShaderNodeVectorMath")  # the leaf-to-leaf light end
    mul.operation = 'MULTIPLY'
    mul.inputs[1].default_value = (1.34, 1.34, 1.34)
    nt.links.new(m1.outputs[2], mul.inputs[0])
    nt.links.new(mul.outputs[0], m2.inputs[7])
    return m2.outputs[2]


def _leaf_mat(name, srgb, gain=None, rough=0.42, translucency=0.09, spread=0.44,
              noise_scale=5.5, sheen=0.26):
    """A leaf: dielectric, barely glossy, a little light through it.

    Translucency AND specular are both kept low on purpose.  Measured against
    report S2.1 the first build of this shader landed its median correctly but
    its p95 at L* 90 against a measured 65: a glossy leaf catching a large low
    source is the mechanism by which CG foliage escapes its value band at the
    top end even when the median is right.  Wide rough, weak sheen, little
    transmission -- S7.1: "Do not lift the foliage to see the detail".
    """
    gain = FOLIAGE_GAIN if gain is None else gain
    rgb = _scale(_lin(srgb), gain)
    m, nt, b, out = _base_mat(name)
    col = _varied_colour(nt, rgb, spread, noise_scale)
    nt.links.new(col, b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = rough
    if "Specular IOR Level" in b.inputs:
        b.inputs["Specular IOR Level"].default_value = sheen
    tr = nt.nodes.new("ShaderNodeBsdfTranslucent")
    tr.inputs["Color"].default_value = (*_scale(rgb, 1.25), 1.0)
    mx = nt.nodes.new("ShaderNodeMixShader")
    mx.inputs[0].default_value = translucency
    nt.links.new(b.outputs[0], mx.inputs[1])
    nt.links.new(tr.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs["Surface"])
    return m


def _matte(name, srgb, gain=DRESS_GAIN, rough=0.72, spec=0.28, bump=0.0,
           bump_scale=40.0, metallic=0.0, coat=0.0):
    m, nt, b, out = _base_mat(name)
    b.inputs["Base Color"].default_value = (*_scale(_lin(srgb), gain), 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metallic
    if "Specular IOR Level" in b.inputs:
        b.inputs["Specular IOR Level"].default_value = spec
    if coat and "Coat Weight" in b.inputs:
        b.inputs["Coat Weight"].default_value = coat
    if bump:
        nz = nt.nodes.new("ShaderNodeTexNoise")
        nz.inputs["Scale"].default_value = bump_scale
        nz.inputs["Detail"].default_value = 8.0
        bp = nt.nodes.new("ShaderNodeBump")
        bp.inputs["Strength"].default_value = bump
        nt.links.new(nz.outputs["Fac"], bp.inputs["Height"])
        nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m


def _trunk_mat(name, srgb, rings=0.0, ring_scale=26.0):
    """Palm trunk.  Report S7.3: C* 13.7 -- almost neutral warm grey.  A stock
    bark shader gives C* 30+ and it is the first thing that reads as CG."""
    m, nt, b, out = _base_mat(name)
    base = _scale(_lin(srgb), DRESS_GAIN)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    # diagonal fibre grain (report S1, P1) -- stretched noise
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (3.2, 3.2, 0.32)
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 5.0
    nz.inputs["Detail"].default_value = 7.0
    nt.links.new(mp.outputs["Vector"], nz.inputs["Vector"])
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = 'RGBA'
    mix.inputs[6].default_value = (*_scale(base, 0.66), 1.0)
    mix.inputs[7].default_value = (*_scale(base, 1.24), 1.0)
    nt.links.new(nz.outputs["Fac"], mix.inputs[0])
    nt.links.new(mix.outputs[2], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.80
    if "Specular IOR Level" in b.inputs:
        b.inputs["Specular IOR Level"].default_value = 0.22
    # transverse leaf-scar rings
    bump_src = nz.outputs["Fac"]
    if rings:
        sep = nt.nodes.new("ShaderNodeSeparateXYZ")
        nt.links.new(tc.outputs["Object"], sep.inputs[0])
        wv = nt.nodes.new("ShaderNodeMath")
        wv.operation = 'MULTIPLY'
        wv.inputs[1].default_value = ring_scale
        nt.links.new(sep.outputs["Z"], wv.inputs[0])
        sn = nt.nodes.new("ShaderNodeMath")
        sn.operation = 'SINE'
        nt.links.new(wv.outputs[0], sn.inputs[0])
        ad = nt.nodes.new("ShaderNodeMath")
        ad.operation = 'MULTIPLY_ADD'
        ad.inputs[1].default_value = rings
        ad.inputs[2].default_value = 0.5
        nt.links.new(sn.outputs[0], ad.inputs[0])
        mixb = nt.nodes.new("ShaderNodeMix")
        mixb.data_type = 'FLOAT'
        mixb.inputs[0].default_value = 0.55
        nt.links.new(nz.outputs["Fac"], mixb.inputs[2])
        nt.links.new(ad.outputs[0], mixb.inputs[3])
        bump_src = mixb.outputs[0]
    bp = nt.nodes.new("ShaderNodeBump")
    bp.inputs["Strength"].default_value = 0.34
    nt.links.new(bump_src, bp.inputs["Height"])
    nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m


def _grass_mat(name):
    """Blade colour, but with the dark bottom end the report insists on:
    grass Y p5 = 0.0225 against p50 0.104 -- the shadowed inter-blade gap is
    60 % of the pixel mass (report S2.1, S6)."""
    return _leaf_mat(name, C_GRASS, gain=FOLIAGE_GAIN * GRASS_GAIN, rough=0.46,
                     translucency=0.12, spread=0.50, noise_scale=1.6, sheen=0.20)


# --------------------------------------------------------------------------
# primitive builders (numpy -> from_pydata; no ops, no modifiers stack needed)
# --------------------------------------------------------------------------

def _tube(p0, p1, r0, r1, sides=7, twist=0.0):
    """Tapering tube between two points.  Returns (verts, faces)."""
    p0 = np.asarray(p0, float)
    p1 = np.asarray(p1, float)
    ax = p1 - p0
    L = np.linalg.norm(ax)
    if L < 1e-9:
        return [], []
    ax = ax / L
    up = np.array([0.0, 0.0, 1.0])
    if abs(np.dot(ax, up)) > 0.95:
        up = np.array([1.0, 0.0, 0.0])
    s = np.cross(ax, up)
    s /= np.linalg.norm(s)
    t = np.cross(ax, s)
    a = np.linspace(0, 2 * math.pi, sides, endpoint=False)
    ring0 = p0 + r0 * (np.outer(np.cos(a), s) + np.outer(np.sin(a), t))
    ring1 = p1 + r1 * (np.outer(np.cos(a + twist), s) + np.outer(np.sin(a + twist), t))
    v = np.vstack([ring0, ring1])
    f = [(i, (i + 1) % sides, sides + (i + 1) % sides, sides + i)
         for i in range(sides)]
    return v, f


def _curved_stem(pts, radii, sides=7):
    """Swept tube through a polyline."""
    pts = np.asarray(pts, float)
    n = len(pts)
    up = np.array([0.0, 0.0, 1.0])
    V, F = [], []
    a = np.linspace(0, 2 * math.pi, sides, endpoint=False)
    for i in range(n):
        if i == 0:
            ax = pts[1] - pts[0]
        elif i == n - 1:
            ax = pts[-1] - pts[-2]
        else:
            ax = pts[i + 1] - pts[i - 1]
        ax = ax / (np.linalg.norm(ax) + 1e-12)
        u = up if abs(np.dot(ax, up)) < 0.95 else np.array([1.0, 0.0, 0.0])
        s = np.cross(ax, u)
        s /= np.linalg.norm(s) + 1e-12
        t = np.cross(ax, s)
        ring = pts[i] + radii[i] * (np.outer(np.cos(a), s) + np.outer(np.sin(a), t))
        V.append(ring)
    V = np.vstack(V)
    for i in range(n - 1):
        for j in range(sides):
            k = (j + 1) % sides
            F.append((i * sides + j, i * sides + k,
                      (i + 1) * sides + k, (i + 1) * sides + j))
    return V, F


def _leaflet(P, d, up, along, length, width, curl):
    """One pinnate leaflet: 1 quad + 1 tri, 5 verts.  Cheapest thing that still
    has a silhouette and a fold."""
    M = P + d * length * 0.55 + up * curl * 0.45
    T = P + d * length + up * curl
    w0 = along * (width * 0.5)
    w1 = along * (width * 0.34)
    v = [P - w0, P + w0, M - w1, M + w1, T]
    f = [(0, 1, 3, 2), (2, 3, 4)]
    return v, f


def _frond(L=2.55, nleaf=26, droop=0.60, leaf_frac=0.20, sweep=0.42,
           fold=0.55, rachis_r=0.020, narrow=1.0, rng=None):
    """A pinnate (feather) palm frond lying along +X, arching down.

    Leaflets 2-4 px wide at Z 10 m in the reference (report S1) -- i.e. of order
    20-35 mm.  `narrow` squeezes them for the cane palm (P4, lanceolate).
    """
    rng = rng or random
    ns = 26
    t = np.linspace(0.0, 1.0, ns)
    pts = np.stack([L * t, np.zeros(ns), -droop * t ** 2.1], 1)
    rad = rachis_r * (1.0 - 0.85 * t) + 0.0015
    V, F = _curved_stem(pts, rad, sides=5)
    V = [np.asarray(x) for x in V]
    F = [tuple(f) for f in F]
    up = np.array([0.0, 0.0, 1.0])
    for i in range(nleaf):
        u = 0.10 + 0.90 * (i + 0.5) / nleaf
        P = np.array([L * u, 0.0, -droop * u ** 2.1])
        tang = np.array([1.0, 0.0, -2.1 * droop * u ** 1.1])
        tang /= np.linalg.norm(tang)
        # bell length profile, tips shorter
        ln = leaf_frac * L * (math.sin(math.pi * min(1.0, u ** 0.82)) ** 0.55)
        ln *= (0.86 + 0.28 * rng.random())
        wd = 0.030 * L * narrow * (0.8 + 0.4 * rng.random())
        for sgn in (+1.0, -1.0):
            side = np.array([0.0, sgn, 0.0])
            d = side + tang * sweep - up * fold
            d /= np.linalg.norm(d)
            vv, ff = _leaflet(P, d, up, tang, ln, wd,
                              -0.30 * ln * (0.6 + 0.8 * rng.random()))
            off = len(V)
            V.extend(vv)
            F.extend([tuple(k + off for k in f) for f in ff])
    return V, F


def _crown_mesh(name, nfrond=13, L=2.55, tilt_lo=8.0, tilt_hi=48.0, rng=None,
                narrow=1.0, leaf_frac=0.20, droop=0.60):
    """A whole palm crown as ONE mesh so it can be instanced.  Origin at the
    crown centre, +Z up."""
    rng = rng or random
    V, F = [], []
    az0 = rng.random() * 360.0
    for i in range(nfrond):
        az = math.radians(az0 + 360.0 * i / nfrond + rng.uniform(-9, 9))
        el = math.radians(rng.uniform(tilt_lo, tilt_hi))
        vv, ff = _frond(L=L * rng.uniform(0.82, 1.12), droop=droop,
                        narrow=narrow, leaf_frac=leaf_frac, rng=rng)
        ca, sa, ce, se = math.cos(az), math.sin(az), math.cos(el), math.sin(el)
        Rz = np.array([[ca, -sa, 0], [sa, ca, 0], [0, 0, 1]])
        Ry = np.array([[ce, 0, se], [0, 1, 0], [-se, 0, ce]])
        R = Rz @ Ry
        off = len(V)
        V.extend([R @ np.asarray(v) for v in vv])
        F.extend([tuple(k + off for k in f) for f in ff])
    return _mesh(name, V, F)


def _paddle_mesh(name, L=1.15, W=0.46, arch=0.34, fold=0.30, tears=3, rng=None):
    """Musa / Heliconia paddle blade.  Report S1 P5a-c: entire margin, strong
    midrib, the chroma peak of the whole planting (C* 34-45)."""
    rng = rng or random
    nu, nv = 7, 13
    us = np.linspace(-1, 1, nu)
    vs = np.linspace(0, 1, nv)
    V = []
    for v in vs:
        wid = W * (math.sin(math.pi * max(1e-3, v) ** 0.72) ** 0.62)
        for u in us:
            x = L * v
            y = u * wid * 0.5
            z = -arch * v ** 1.8 - fold * abs(u) * wid * 0.5
            V.append((x, y, z))
    F = []
    torn = set()
    for _ in range(tears):
        r = rng.randrange(2, nv - 2)
        s = rng.choice((0, nu - 2))
        torn.add((r, s))
        torn.add((r, s + (1 if s == 0 else -1)))
    for j in range(nv - 1):
        for i in range(nu - 1):
            if (j, i) in torn:
                continue
            a = j * nu + i
            F.append((a, a + 1, a + nu + 1, a + nu))
    # short petiole
    pv, pf = _tube((-0.16 * L, 0, 0.03), (0, 0, 0), 0.016, 0.011, sides=5)
    off = len(V)
    V.extend([tuple(p) for p in pv])
    F.extend([tuple(k + off for k in f) for f in pf])
    return _mesh(name, V, F)


def _strap_mesh(name, n=21, L=0.98, W=0.075, rng=None):
    """Agave / bromeliad rosette (report S1 P6): long narrow arching strap
    leaves with a pale central rib.  Rosette measured 1.5 x 1.06 m."""
    rng = rng or random
    V, F = [], []
    for i in range(n):
        az = math.radians(360.0 * i / n + rng.uniform(-8, 8))
        el = math.radians(rng.uniform(24, 74))
        ll = L * rng.uniform(0.72, 1.15)
        ns = 7
        t = np.linspace(0, 1, ns)
        # arching: rises then falls away
        rr = ll * t
        # rises at the leaf's own elevation, then arches away and falls
        zz = ll * (math.sin(el) * t - 0.62 * t ** 2.4)
        xy = rr * math.cos(el)
        wid = W * (1.0 - 0.92 * t ** 1.6) + 0.004
        off = len(V)
        for k in range(ns):
            cx = xy[k] * math.cos(az)
            cy = xy[k] * math.sin(az)
            px = -math.sin(az) * wid[k]
            py = math.cos(az) * wid[k]
            crease = -0.30 * wid[k]
            V.append((cx - px, cy - py, zz[k]))
            V.append((cx, cy, zz[k] + crease))
            V.append((cx + px, cy + py, zz[k]))
        for k in range(ns - 1):
            a = off + k * 3
            F.append((a, a + 1, a + 4, a + 3))
            F.append((a + 1, a + 2, a + 5, a + 4))
    return _mesh(name, V, F)


def _leafpuff_mesh(name, n=34, r=0.30, leaf=0.11, wide=0.055, rng=None,
                   flat=1.0):
    """A cluster of small ovate leaves on a squashed hemisphere -- the unit of
    the shrub layer and of the flowering band's green fraction."""
    rng = rng or random
    V, F = [], []
    up = np.array([0.0, 0.0, 1.0])
    for _ in range(n):
        th = math.acos(1 - rng.random() * 1.55)
        ph = rng.random() * 2 * math.pi
        d = np.array([math.sin(th) * math.cos(ph),
                      math.sin(th) * math.sin(ph),
                      math.cos(th) * flat])
        d /= np.linalg.norm(d)
        P = d * r * rng.uniform(0.55, 1.0)
        along = np.cross(d, up)
        if np.linalg.norm(along) < 1e-6:
            along = np.array([1.0, 0.0, 0.0])
        along /= np.linalg.norm(along)
        ll = leaf * rng.uniform(0.7, 1.3)
        ww = wide * rng.uniform(0.7, 1.3)
        M = P + d * ll * 0.5
        T = P + d * ll
        off = len(V)
        V.extend([P - along * ww * 0.30, P + along * ww * 0.30,
                  M - along * ww * 0.5, M + along * ww * 0.5, T])
        F.extend([(off, off + 1, off + 3, off + 2), (off + 2, off + 3, off + 4)])
    return _mesh(name, V, F)


def _twigcluster_mesh(name, n=7, r=0.30, rng=None):
    """Tan stems / grey-blue sprays -- the 26 % remainder of the flowering
    band (report S4.1).  Without it the band reads as flowers glued to leaves
    rather than as a climbing mass with woody structure."""
    rng = rng or random
    V, F = [], []
    for _ in range(n):
        a = rng.random() * 2 * math.pi
        e = rng.uniform(-0.9, 0.9)
        d = np.array([math.cos(a), math.sin(a), e])
        d /= np.linalg.norm(d)
        P = np.array([rng.uniform(-r, r), rng.uniform(-r, r),
                      rng.uniform(-r * 0.6, r * 0.6)]) * 0.5
        ln = r * rng.uniform(0.8, 1.9)
        mid = P + d * ln * 0.5 + np.array([0, 0, -0.10 * ln])
        vv, ff = _curved_stem([P, mid, P + d * ln],
                              [0.008, 0.006, 0.0035], sides=4)
        off = len(V)
        V.extend([tuple(p) for p in vv])
        F.extend([tuple(k + off for k in f) for f in ff])
    return _mesh(name, V, F)


def _flowerhead_mesh(name, n=11, r=0.085, rng=None):
    """Crimson flower head -- a little rosette of bracts (report S4.1: median
    sRGB 158,86,63, C* 34.8, 13.4 % of the band)."""
    rng = rng or random
    V, F = [], []
    for i in range(n):
        az = math.radians(360.0 * i / n + rng.uniform(-14, 14))
        el = math.radians(rng.uniform(12, 78))
        d = np.array([math.cos(az) * math.cos(el), math.sin(az) * math.cos(el),
                      math.sin(el)])
        s = np.array([-math.sin(az), math.cos(az), 0.0])
        ll = r * rng.uniform(0.75, 1.25)
        off = len(V)
        V.extend([(0, 0, 0), tuple(d * ll * 0.5 - s * r * 0.42),
                  tuple(d * ll), tuple(d * ll * 0.5 + s * r * 0.42)])
        F.append((off, off + 1, off + 2, off + 3))
    return _mesh(name, V, F)


def _floretspray_mesh(name, n=30, r=0.090, rng=None):
    """Cream floret spray, 5.5 % of the band."""
    rng = rng or random
    V, F = [], []
    for _ in range(n):
        th = math.acos(1 - rng.random() * 2.0)
        ph = rng.random() * 2 * math.pi
        c = np.array([math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph),
                      math.cos(th)]) * r * rng.uniform(0.3, 1.0)
        s = 0.013 * rng.uniform(0.7, 1.4)
        off = len(V)
        V.extend([tuple(c + np.array(o) * s) for o in
                  ((-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0))])
        F.append((off, off + 1, off + 2, off + 3))
    return _mesh(name, V, F)


def _blade_tile_mesh(name, size=1.9, n=1500, h=0.075, rng=None):
    """A tile of lawn blades, built as ONE mesh and instanced over the lawn.

    Report S6 is explicit: the near/far grass gradient must come from grass
    geometry and self-shadowing, not from a fog volume.
    """
    rng = rng or random
    V, F = [], []
    for _ in range(n):
        x = rng.uniform(-size / 2, size / 2)
        y = rng.uniform(-size / 2, size / 2)
        az = rng.random() * 2 * math.pi
        d = np.array([math.cos(az), math.sin(az), 0.0])
        ll = h * rng.uniform(0.55, 1.55)
        lean = rng.uniform(0.25, 0.85)
        w = 0.0035 * rng.uniform(0.7, 1.3)
        s = np.array([-math.sin(az), math.cos(az), 0.0]) * w
        P = np.array([x, y, 0.0])
        p1 = P + d * (ll * lean * 0.30) + np.array([0, 0, ll * 0.52])
        p2 = P + d * (ll * lean * 0.72) + np.array([0, 0, ll * 0.86])
        p3 = P + d * (ll * lean) + np.array([0, 0, ll])
        off = len(V)
        V.extend([tuple(P - s), tuple(P + s),
                  tuple(p1 - s * 0.8), tuple(p1 + s * 0.8),
                  tuple(p2 - s * 0.5), tuple(p2 + s * 0.5),
                  tuple(p3)])
        F.extend([(off, off + 1, off + 3, off + 2),
                  (off + 2, off + 3, off + 5, off + 4),
                  (off + 4, off + 5, off + 6)])
    return _mesh(name, V, F, smooth=False)


# --------------------------------------------------------------------------
# where planting is allowed
# --------------------------------------------------------------------------

def _edge_d(x, y):
    return EDGE_N[0] * x + EDGE_N[1] * y


def _planted(x, y, margin=0.0):
    """True where planting may stand.

    Two regions, unioned:
      * beyond the MEASURED lawn edge (report S1/S5) -- the wedge the reference
        photograph actually shows, nose-and-counter side;
      * beyond BELT_R_IN in every other direction, so that a camera anywhere on
        the terrace still has a green wall behind the vehicle.
    Minus the paved terrace, the camera stations and their sightlines.
    """
    r = math.hypot(x, y)
    if r < 2.60:                       # never inside/next to the vehicle
        return False
    if math.hypot(x - REF_CAM[0], y - REF_CAM[1]) < TERRACE_R:
        return False                   # the paved terrace (report S1)
    inside = (_edge_d(x, y) > EDGE_D + margin) or (r > BELT_R_IN + margin)
    if not inside or r > BELT_R_OUT:
        return False
    # A negative margin is used to let ground cover run a little INTO the
    # planting boundary; it must never be allowed to shrink the camera
    # clearances, or the lawn plane ends up a metre in front of the lens.
    cm = max(margin, 0.0)
    for cx, cy in KEEPOUT_CAMS:
        if math.hypot(x - cx, y - cy) < KEEPOUT_R + cm:
            return False
        # Clear corridor from the station to the vehicle -- but ONLY through the
        # extrapolated belt.  Two of studio.py's playa stations stand inside the
        # wedge the reference photograph actually measured; cutting 3 m tunnels
        # through THAT to accommodate them would delete the measurement, so the
        # measured wedge wins and only the belt gets carved.
        if r <= BELT_R_IN:
            continue
        vx, vy = -cx, -cy
        L2 = vx * vx + vy * vy
        t = ((x - cx) * vx + (y - cy) * vy) / L2
        if 0.0 < t < 1.0:
            px, py = cx + t * vx, cy + t * vy
            if math.hypot(x - px, y - py) < SIGHTLINE_R + cm:
                return False
    return True


def _scatter(n, rmin, rmax, azlo=0.0, azhi=360.0, margin=0.0, tries=60):
    """Poisson-ish rejection scatter inside the planted region."""
    out = []
    for _ in range(n):
        for _ in range(tries):
            a = math.radians(_RNG.uniform(azlo, azhi))
            r = math.sqrt(_RNG.uniform(rmin ** 2, rmax ** 2))
            x, y = r * math.cos(a), r * math.sin(a)
            if _planted(x, y, margin):
                out.append((x, y))
                break
    return out


# --------------------------------------------------------------------------
# the eleven measured masses
# --------------------------------------------------------------------------

def _ref_world(ximg, Z):
    """Invert (image column, depth) through the reference camera -> world XY."""
    u = math.atan((ximg - REF_W_PX * 0.5) / REF_F_PX)
    phi = math.radians(REF_AXIS_DEG) - u
    d = Z / math.cos(u)
    return (REF_CAM[0] + d * math.cos(phi), REF_CAM[1] + d * math.sin(phi))


# (name, image column, depth Z m) -> world XY, straight off report S1.
MASS_XY = {
    "P1":  _ref_world(318, 5.90),    # main palm, clear trunk >= 3.03 m
    "P2":  _ref_world(140, 10.50),   # slender ringed stem, top >= 3.83 m
    "P3":  _ref_world(170, 10.00),   # feather-palm canopy, top ~ 3.6 m
    "P4":  _ref_world(460, 13.00),   # cane clumping palm, top ~ 4.1 m
    "P5a": _ref_world(378, 10.50),   # paddle leaf 2.86 -> 2.23 m
    "P5b": _ref_world(193, 11.00),   # paddle leaf 2.27 -> 1.65 m
    "P5c": _ref_world(401, 9.00),    # paddle leaf 1.30 -> 0.93 m
    "P6":  _ref_world(226, 10.10),   # agave rosette, top 1.06 m
    "P8":  _ref_world(385, 12.30),   # dark understorey shrub, 0.67 m
    "P9L": _ref_world(0, 7.50),      # flowering band, left end
    "P9R": _ref_world(790, 7.50),    # flowering band, occluded at x 790
}


def _palm(name, xy, trunk_h, dia, crown_meshes, trunk_mat, ringed=False,
          lean=0.0, crown_scale=1.0, cls="palm"):
    x, y = xy
    az = _RNG.uniform(0, 2 * math.pi)
    tip = (x + lean * math.cos(az), y + lean * math.sin(az), trunk_h)
    ns = 9
    t = np.linspace(0, 1, ns)
    pts = np.stack([x + lean * math.cos(az) * t ** 1.7,
                    y + lean * math.sin(az) * t ** 1.7,
                    trunk_h * t], 1)
    # report S1 P1: the trunk does NOT taper over 0.38 -> 2.74 m above ground
    rad = np.full(ns, dia * 0.5)
    rad[0] *= 1.22                       # slight basal flare only
    rad[-1] *= 0.92
    V, F = _curved_stem(pts, rad, sides=9)
    me = _mesh(name + "_trunk", V, F)
    me.materials.append(trunk_mat)
    ob = _put(name + "_trunk", me, cls="trunk")
    cm = _RNG.choice(crown_meshes)
    _put(name + "_crown", cm, loc=tip, scale=crown_scale,
         rot=(0, 0, _RNG.uniform(0, 6.28)), cls=cls)
    return ob


def _cane_clump(name, xy, h, mesh_pool, cane_mat, ncane=13, cls="cane_palm"):
    """P4: many slim tan/olive canes with narrow lanceolate leaflets --
    Chamaedorea seifrizii / Dypsis lutescens habit (report S1)."""
    x, y = xy
    V, F = [], []
    tips = []
    for i in range(ncane):
        a = _RNG.uniform(0, 2 * math.pi)
        rr = _RNG.uniform(0.06, 0.62)
        hh = h * _RNG.uniform(0.55, 1.0)
        bx, by = x + rr * math.cos(a), y + rr * math.sin(a)
        lean = _RNG.uniform(0.05, 0.40)
        la = _RNG.uniform(0, 2 * math.pi)
        ns = 7
        t = np.linspace(0, 1, ns)
        pts = np.stack([bx + lean * math.cos(la) * t ** 1.9,
                        by + lean * math.sin(la) * t ** 1.9, hh * t], 1)
        rad = 0.021 * (1.0 - 0.35 * t) + 0.004
        vv, ff = _curved_stem(pts, rad, sides=5)
        off = len(V)
        V.extend([tuple(v) for v in vv])
        F.extend([tuple(k + off for k in f) for f in ff])
        tips.append((pts[-1], hh))
    me = _mesh(name + "_canes", V, F)
    me.materials.append(cane_mat)
    _put(name + "_canes", me, cls="trunk")
    for p, hh in tips:
        _put(name + "_crown", _RNG.choice(mesh_pool),
             loc=tuple(p), scale=0.34 * (hh / h) + 0.20,
             rot=(0, 0, _RNG.uniform(0, 6.28)), cls=cls)


# --------------------------------------------------------------------------
# build
# --------------------------------------------------------------------------

def build(seed=0):
    """Construct the Playa vegetation and set dressing in the current scene.

    Safe to call twice: it first removes only objects/data it named pl_*.
    Adds no lamps, no world volume, no bunting.  Returns a count dict.
    """
    global _COLL, _RNG, _NPR, _COUNT, _MESHPOLY, _EVALPOLY
    _purge()
    _RNG = random.Random(seed)
    _NPR = np.random.default_rng(seed)
    _COUNT = {}
    _MESHPOLY = 0
    _EVALPOLY = 0
    _COLL = _new_coll()
    R = _RNG

    # ---------------------------------------------------------------- mats
    m_canopy = _leaf_mat("leaf_canopy", C_CANOPY, rough=0.42, translucency=0.09)
    m_cane_l = _leaf_mat("leaf_cane", C_CANE, rough=0.42, translucency=0.08,
                         spread=0.40)
    m_paddle = _leaf_mat("leaf_paddle", C_PADDLE, rough=0.36, translucency=0.13,
                         spread=0.30, noise_scale=2.4, sheen=0.32)
    m_under = _leaf_mat("leaf_understorey", C_UNDERSTOREY, rough=0.48,
                        translucency=0.05, spread=0.44, sheen=0.14)
    m_agave = _leaf_mat("leaf_agave", C_AGAVE, rough=0.38, translucency=0.05,
                        spread=0.30, sheen=0.30)
    m_grass = _grass_mat("grass")
    m_gap = _matte("grass_gap", C_GRASS_GAP, gain=FOLIAGE_GAIN * 1.9 * GRASS_GAIN,
                   rough=0.88,
                   spec=0.05, bump=0.22, bump_scale=13.0)
    m_bandg = _leaf_mat("band_green", C_BANDGREEN, rough=0.42, translucency=0.11,
                        spread=0.40, sheen=0.24)
    m_crimson = _matte("band_crimson", C_CRIMSON, gain=FOLIAGE_GAIN * 1.55,
                       rough=0.48, spec=0.22)
    m_floret = _matte("band_floret", C_FLORET, gain=FOLIAGE_GAIN * 1.35,
                      rough=0.55, spec=0.20)
    m_trunk = _trunk_mat("trunk_palm", C_TRUNK)
    m_stemring = _trunk_mat("stem_ringed", C_STEM_RINGED, rings=0.55,
                            ring_scale=95.0)
    m_cane_s = _trunk_mat("cane_stem", C_CANE_STEM)
    m_timber = _matte("timber", C_TIMBER, rough=0.86, spec=0.14, bump=0.30,
                      bump_scale=55.0)
    m_timb_m = _matte("timber_mossy", C_TIMBER_MOSS, rough=0.88, spec=0.10,
                      bump=0.30, bump_scale=55.0)
    m_postdk = _matte("post_dark", C_POST_DARK, rough=0.90, spec=0.10)
    m_frame = _matte("sign_frame", C_SIGN_FRAME, rough=0.55, spec=0.30)
    m_head = _matte("sign_header", C_SIGN_HEAD, rough=0.58, spec=0.28)
    m_field = _matte("sign_field", C_SIGN_FIELD, rough=0.62, spec=0.26)
    m_ink = _matte("sign_ink", C_SIGN_INK, rough=0.70, spec=0.16)
    m_lam = _matte("laminate", C_LAMINATE, rough=0.28, spec=0.42, coat=0.25)
    m_alu = _matte("alu_band", C_ALU, rough=0.30, spec=0.5, metallic=0.85)
    m_vinyl = _matte("vinyl", C_VINYL, rough=0.34, spec=0.45, coat=0.20)
    m_chrome = _matte("chrome", C_CHROME, rough=0.13, spec=0.5, metallic=1.0)
    m_steel = _matte("stainless", C_STAINLESS, rough=0.26, spec=0.5,
                     metallic=0.9)
    m_ging = _gingham_mat("gingham")
    m_oxb = _matte("oxblood", C_OXBLOOD, rough=0.66, spec=0.22)
    m_scroll = _matte("scrollwork", C_SCROLL, rough=0.62, spec=0.24)
    m_board = _matte("board_green", C_BOARD_GREEN, rough=0.60, spec=0.26)
    m_pole = _matte("pole_screen", C_POLESCREEN, rough=0.88, spec=0.12,
                    bump=0.26, bump_scale=48.0)
    m_pend = _matte("pendant", C_PENDANT, rough=0.16, spec=0.5, metallic=0.92)
    m_mint = _matte("mat_roll", C_MINT, rough=0.72, spec=0.18, bump=0.5,
                    bump_scale=170.0)

    # --------------------------------------------------- instanceable meshes
    crowns_big = [_crown_mesh("crown_big%d" % i, nfrond=R.randint(15, 19),
                              L=2.75, rng=R) for i in range(3)]
    crowns_mid = [_crown_mesh("crown_mid%d" % i, nfrond=R.randint(12, 16),
                              L=2.05, rng=R, droop=0.66) for i in range(3)]
    crowns_cane = [_crown_mesh("crown_cane%d" % i, nfrond=R.randint(9, 13),
                               L=1.15, narrow=0.55, leaf_frac=0.26,
                               droop=0.42, rng=R) for i in range(3)]
    for m in crowns_big + crowns_mid:
        m.materials.append(m_canopy)
    for m in crowns_cane:
        m.materials.append(m_cane_l)

    paddles = []
    for i in range(3):
        me = _paddle_mesh("paddle%d" % i, L=1.05 + 0.22 * i, W=0.40 + 0.07 * i,
                          rng=R)
        me.materials.append(m_paddle)
        paddles.append(me)

    straps = []
    for i in range(2):
        me = _strap_mesh("agave%d" % i, n=19 + 4 * i, L=0.95 + 0.10 * i, rng=R)
        me.materials.append(m_agave)
        straps.append(me)

    puffs_under = []
    for i in range(3):
        me = _leafpuff_mesh("shrub%d" % i, n=30 + 6 * i, r=0.28, leaf=0.10,
                            rng=R, flat=0.72)
        me.materials.append(m_under)
        puffs_under.append(me)

    puffs_band = []
    for i in range(3):
        me = _leafpuff_mesh("bandleaf%d" % i, n=32, r=0.26, leaf=0.105,
                            wide=0.058, rng=R, flat=0.9)
        me.materials.append(m_bandg)
        puffs_band.append(me)

    heads = []
    for i in range(2):
        me = _flowerhead_mesh("flowerhead%d" % i, n=11, r=0.085, rng=R)
        me.materials.append(m_crimson)
        heads.append(me)

    florets = []
    for i in range(2):
        me = _floretspray_mesh("floret%d" % i, n=30, r=0.090, rng=R)
        me.materials.append(m_floret)
        florets.append(me)

    twigs = []
    for i in range(2):
        me = _twigcluster_mesh("twig%d" % i, n=8, r=0.30, rng=R)
        me.materials.append(m_cane_s)
        twigs.append(me)

    tiles = []
    for i in range(4):
        me = _blade_tile_mesh("grasstile%d" % i, size=1.90, n=1450, h=0.078,
                              rng=R)
        me.materials.append(m_grass)
        tiles.append(me)

    # ------------------------------------------------------------ the lawn
    _lawn_base(m_gap)
    ng = _lawn_blades(tiles)

    # ------------------------------------------- P1: the main palm + its sign
    # 0.245 +- 0.020 m diameter, non-tapering, >= 3.03 m of clear trunk running
    # off the top of the frame (report S1, S7.3).
    _palm("P1_palm", MASS_XY["P1"], 4.85, 0.245, crowns_big, m_trunk,
          lean=0.10, crown_scale=1.12)
    _sign_on_trunk(MASS_XY["P1"], m_frame, m_head, m_field, m_ink)
    _rolled_mat(MASS_XY["P1"], m_mint)

    # ---------------------------------------------- P2: slender ringed stem
    _palm("P2_stem", MASS_XY["P2"], 5.30, 0.21, crowns_mid, m_stemring,
          lean=0.16, crown_scale=0.95)

    # ------------------------------------------- P3: feather-palm frond wall
    # top ~ 3.6 m AG = 1.88 x roof.  Built as three crowns clustered so the
    # canopy reads as a mass rather than as one plant.
    px, py = MASS_XY["P3"]
    for k, (dx, dy, h) in enumerate(((0, 0, 3.55), (-0.9, 0.7, 3.15),
                                     (1.0, -0.5, 3.75), (-1.9, -0.3, 3.30),
                                     (2.0, 0.9, 3.60), (0.4, 1.6, 3.05))):
        _palm("P3_palm%d" % k, (px + dx, py + dy), h - 0.35, 0.17,
              crowns_mid, m_trunk, lean=0.22, crown_scale=0.90)

    # ------------------------------------------------ P4: cane clumping palm
    _cane_clump("P4_clump", MASS_XY["P4"], 4.10, crowns_cane, m_cane_s,
                ncane=15)
    # a second clump beside it so the far screen closes
    _cane_clump("P4_clump_b", (MASS_XY["P4"][0] - 1.5, MASS_XY["P4"][1] + 1.4),
                3.60, crowns_cane, m_cane_s, ncane=11)

    # ------------------------------------------------- P5a-c: paddle leaves
    # measured tops: 2.86, 2.27, 1.30 m AG, blades falling ~0.6 m.
    _paddle_plant("P5a", MASS_XY["P5a"], 2.86, paddles, m_cane_s, nleaf=7)
    _paddle_plant("P5b", MASS_XY["P5b"], 2.27, paddles, m_cane_s, nleaf=6)
    _paddle_plant("P5c", MASS_XY["P5c"], 1.30, paddles, m_cane_s, nleaf=5,
                  scale=0.72)

    # -------------------------------------------------------- P6: the agave
    # rosette 1.5 x 1.06 m at Z = 10 m; top of mass 1.06 m AG.
    _put("P6_agave", straps[0], loc=(MASS_XY["P6"][0], MASS_XY["P6"][1], 0.06),
         rot=(0, 0, R.uniform(0, 6.28)), scale=1.06, cls="agave")
    _put("P6_agave_b", straps[1],
         loc=(MASS_XY["P6"][0] - 0.85, MASS_XY["P6"][1] + 0.45, 0.04),
         rot=(0, 0, R.uniform(0, 6.28)), scale=0.80, cls="agave")

    # ------------------------------------------ P8: dark understorey shrubs
    # 0.67 m high (0.35 x roof) at Z 11-14 m; a band, not a plant.
    sx, sy = MASS_XY["P8"]
    nsh = 0
    for _ in range(210):
        x = sx + R.uniform(-3.4, 3.4)
        y = sy + R.uniform(-2.6, 2.6)
        if not _planted(x, y):
            continue
        _put("P8_shrub", R.choice(puffs_under),
             loc=(x, y, R.uniform(0.20, 0.52)), scale=R.uniform(0.75, 1.45),
             rot=(R.uniform(-0.3, 0.3), R.uniform(-0.3, 0.3),
                  R.uniform(0, 6.28)), cls="shrub")
        nsh += 1

    # ------------------------------------------------ P9: the flowering band
    band = _flowering_band(puffs_band, heads, florets, twigs, m_cane_s)

    # ------------------------------------ fence, edging, palapa, furniture
    _fence(m_timber, m_timb_m, m_postdk)
    _bed_edging(m_timber)
    _palapa_corner(m_oxb, m_scroll, m_board, m_pole, m_pend)
    _furniture(m_lam, m_alu, m_vinyl, m_chrome, m_steel, m_ging)

    # ------------------------------------------- the wrap-around green wall
    _belt(crowns_big, crowns_mid, crowns_cane, paddles, straps, puffs_under,
          puffs_band, heads, florets, m_trunk, m_cane_s, m_stemring)
    m_deep = _matte("shadefloor", C_SHADEFLOOR, gain=FOLIAGE_GAIN * 2.2,
                    rough=0.92, spec=0.04)
    deep_puffs = []
    for i in range(2):
        me = _leafpuff_mesh("deepmass%d" % i, n=26, r=0.42, leaf=0.19,
                            wide=0.10, rng=R, flat=0.85)
        me.materials.append(m_deep)
        deep_puffs.append(me)
    _backdrop(m_deep, deep_puffs, m_under)

    _COUNT["_unique_polygons"] = _MESHPOLY
    _COUNT["_instanced_polygons"] = _EVALPOLY
    _COUNT["_objects"] = len([o for o in bpy.data.objects
                              if o.name.startswith(PREFIX)])
    _COUNT["_grass_blades"] = ng * 1450
    _COUNT["_band_fractions"] = band
    _COUNT["_foliage_gain"] = FOLIAGE_GAIN
    return _COUNT


# --------------------------------------------------------------------------
# pieces
# --------------------------------------------------------------------------

def _gingham_mat(name):
    """25 mm green gingham.  Report S4.4: the "white" squares are sRGB
    (175,199,164), L* 77.2, a* -15.5 -- rendered white they punch a hole in the
    foreground."""
    m, nt, b, out = _base_mat(name)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    ck = nt.nodes.new("ShaderNodeTexChecker")
    ck.inputs["Scale"].default_value = 40.0            # ~25 mm on a 1 m cloth
    ck.inputs["Color1"].default_value = (*_scale(_lin(C_GINGHAM_G), DRESS_GAIN), 1)
    ck.inputs["Color2"].default_value = (*_scale(_lin(C_GINGHAM_W), DRESS_GAIN), 1)
    nt.links.new(tc.outputs["Object"], ck.inputs["Vector"])
    nt.links.new(ck.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.80
    if "Specular IOR Level" in b.inputs:
        b.inputs["Specular IOR Level"].default_value = 0.18
    return m


def _lawn_base(mat):
    """The dark ground the blades stand in.  Report S2.1: grass Y p5 = 0.0225 --
    the inter-blade gap is the bottom of the value range and 60 % of the mass."""
    R = 24.0
    na, nr = 168, 74
    V = []
    for j in range(nr + 1):
        rr = 2.2 + (R - 2.2) * (j / nr) ** 1.35
        for i in range(na):
            a = 2 * math.pi * i / na
            V.append((rr * math.cos(a), rr * math.sin(a),
                      0.004 + 0.012 * math.sin(3.1 * a + 0.7 * rr)))
    F = []
    for j in range(nr):
        rr = 2.2 + (R - 2.2) * ((j + 0.5) / nr) ** 1.35
        for i in range(na):
            k = (i + 1) % na
            a = 2 * math.pi * (i + 0.5) / na
            if not _planted(rr * math.cos(a), rr * math.sin(a), margin=-0.9):
                continue
            F.append((j * na + i, j * na + k, (j + 1) * na + k, (j + 1) * na + i))
    me = _mesh("lawn_base", V, F, smooth=False)
    me.materials.append(mat)
    _put("lawn_base", me, cls="lawn")


def _lawn_blades(tiles):
    """Instanced blade tiles.  Dense where the reference shows lawn, thinning
    with distance -- the far lawn is carried by the base and by the planting."""
    n = 0
    step = 1.72                       # tiles overlap slightly: no seams
    for gx in np.arange(-16.0, 16.01, step):
        for gy in np.arange(-16.0, 16.01, step):
            x = gx + _RNG.uniform(-0.24, 0.24)
            y = gy + _RNG.uniform(-0.24, 0.24)
            if not _planted(x, y, margin=-0.5):
                continue
            r = math.hypot(x, y)
            if r > 13.5 and _RNG.random() > 0.45:
                continue
            _put("grass", _RNG.choice(tiles), loc=(x, y, 0.006),
                 rot=(0, 0, _RNG.choice((0, 1.5708, 3.1416, 4.7124))),
                 scale=(1.0, 1.0, _RNG.uniform(0.8, 1.25)), cls="grass_tile")
            n += 1
    return n


def _paddle_plant(name, xy, top, meshes, stem_mat, nleaf=6, scale=1.0):
    """Musa / Heliconia: a short pseudostem with blades whose tips fall about
    0.6 m below the top of the mass (report S1 P5a: 2.86 -> 2.23 m)."""
    x, y = xy
    R = _RNG
    ph = max(0.25, top * 0.42)
    V, F = _tube((x, y, 0), (x, y, ph), 0.085, 0.055, sides=8)
    me = _mesh(name + "_stem", V, F)
    me.materials.append(stem_mat)
    _put(name + "_stem", me, cls="trunk")
    for i in range(nleaf):
        az = R.uniform(0, 2 * math.pi)
        el = R.uniform(-0.10, 0.62)
        h = ph + (top - ph) * R.uniform(0.35, 1.0)
        _put(name + "_leaf", R.choice(meshes), loc=(x, y, h),
             rot=(R.uniform(-0.25, 0.25), -el, az),
             scale=scale * R.uniform(0.85, 1.20), cls="paddle_leaf")


def _flowering_band(puffs, heads, florets, twigs, stem_mat):
    """Report S4.1.  A continuous polychrome flowering mass, NOT bunting.

    Placement: the band was measured at constant depth Z = 6-9 m from the
    reference camera spanning image x 0 -> 790, lower edge 3.2 m AG (1.65 x
    roof), top off-frame.  Inverting that gives an arc about the reference
    camera at r ~ 7.5-8.4 m, which in world runs along X ~ 2.7 from Y = +4.0 to
    Y = -0.8, and continues where the vehicle occludes it.

    Composition is set by MEAN PROJECTED AREA, not by instance count:
    green 55.1 : crimson 13.4 : cream 5.5 : tan stems 26.0, the four classes the
    report measures, which between them account for all of the band's pixels
    (the mass is continuous -- there are no gaps to give away, S4.1 evidence 2).
    A randomly oriented flat element projects to half its polygon area; a
    randomly oriented tube to a quarter of its surface area, so the twigs carry
    their own factor.
    """
    R = _RNG
    cx, cy = REF_CAM[0], REF_CAM[1]
    a0, a1 = math.radians(-24.0), math.radians(15.5)
    ag = _poly_area(puffs[0]) * 0.5
    ah = _poly_area(heads[0]) * 0.5
    af = _poly_area(florets[0]) * 0.5
    aw = _poly_area(twigs[0]) * 0.25

    slots = []
    for _ in range(1400):
        a = R.uniform(a0, a1)
        rr = R.uniform(7.1, 8.6)
        x = cx + rr * math.cos(a) + R.uniform(-0.35, 0.35)
        y = cy + rr * math.sin(a) + R.uniform(-0.35, 0.35)
        # jagged lower edge that interpenetrates the fronds in front (S4.1)
        z = 3.20 + R.random() ** 0.7 * 1.35 - 0.34 * R.random() ** 2
        slots.append((x, y, z))
    # continue the band round the belt so other cameras see it too
    for _ in range(900):
        a = R.uniform(0, 2 * math.pi)
        rr = R.uniform(BELT_R_IN + 0.8, BELT_R_IN + 3.4)
        x, y = rr * math.cos(a), rr * math.sin(a)
        if not _planted(x, y):
            continue
        slots.append((x, y, 3.20 + R.random() ** 0.7 * 1.30))

    # counts from area fractions
    tot = len(slots)
    wg, wh, wf, ww = 55.1, 13.4, 5.5, 26.0
    unit = tot / ((wg / ag) + (wh / ah) + (wf / af) + (ww / aw))
    ng = int(round(unit * wg / ag))
    nh = int(round(unit * wh / ah))
    nf = int(round(unit * wf / af))
    nw = int(round(unit * ww / aw))
    R.shuffle(slots)
    i = 0
    for _ in range(min(ng, len(slots) - i)):
        x, y, z = slots[i]; i += 1
        _put("P9_leaf", R.choice(puffs), loc=(x, y, z),
             scale=R.uniform(0.75, 1.35),
             rot=(R.uniform(0, 6.28), R.uniform(0, 6.28), R.uniform(0, 6.28)),
             cls="band_foliage")
    for _ in range(min(nh, len(slots) - i)):
        x, y, z = slots[i]; i += 1
        _put("P9_flower", R.choice(heads), loc=(x, y, z),
             scale=R.uniform(0.7, 1.5),
             rot=(R.uniform(0, 6.28), R.uniform(0, 6.28), R.uniform(0, 6.28)),
             cls="band_crimson")
    for _ in range(min(nf, len(slots) - i)):
        x, y, z = slots[i]; i += 1
        _put("P9_floret", R.choice(florets), loc=(x, y, z),
             scale=R.uniform(0.7, 1.4),
             rot=(R.uniform(0, 6.28), R.uniform(0, 6.28), R.uniform(0, 6.28)),
             cls="band_floret")
    for _ in range(min(nw, len(slots) - i)):
        x, y, z = slots[i]; i += 1
        _put("P9_twig", R.choice(twigs), loc=(x, y, z),
             scale=R.uniform(0.7, 1.5),
             rot=(R.uniform(0, 6.28), R.uniform(0, 6.28), R.uniform(0, 6.28)),
             cls="band_stems")
    A = (ng * ag, nh * ah, nf * af, nw * aw)
    S = sum(A)
    return dict(green=round(100.0 * A[0] / S, 1),
                crimson=round(100.0 * A[1] / S, 1),
                floret=round(100.0 * A[2] / S, 1),
                tan_stems=round(100.0 * A[3] / S, 1),
                target="55.1 / 13.4 / 5.5 / 26.0",
                n=(ng, nh, nf, nw))


def _fence(m_low, m_up, m_post):
    """Report S4.5.  Two rustic timber rails at Z ~ 7.0 m: upper 0.97 m AG,
    lower 0.21-0.45 m, plus one dark post.  The upper rail is heavily
    overgrown, hence its own mossy colour."""
    R = _RNG
    a, b = _ref_world(150, 7.0), _ref_world(560, 7.0)
    ax, ay = a
    bx, by = b
    # extend a little past both traced ends
    dx, dy = bx - ax, by - ay
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    ax, ay = ax - ux * 1.4, ay - uy * 1.4
    bx, by = bx + ux * 2.2, by + uy * 2.2
    for zz, mat, nm, sag in ((0.97, m_up, "upper", 0.045),
                             (0.33, m_low, "lower", 0.030)):
        ns = 14
        t = np.linspace(0, 1, ns)
        pts = np.stack([ax + (bx - ax) * t, ay + (by - ay) * t,
                        zz - sag * np.sin(math.pi * t) +
                        0.012 * np.sin(7 * t)], 1)
        rad = np.full(ns, 0.042) * (0.85 + 0.3 * np.sin(4.3 * t))
        V, F = _curved_stem(pts, rad, sides=6)
        me = _mesh("fence_" + nm, V, F)
        me.materials.append(mat)
        _put("fence_" + nm, me, cls="fence")
    # posts
    for f in (0.06, 0.34, 0.62, 0.90):
        px, py = ax + (bx - ax) * f, ay + (by - ay) * f
        h = 1.12 + R.uniform(-0.06, 0.06)
        V, F = _tube((px, py, 0), (px + R.uniform(-.03, .03),
                                   py + R.uniform(-.03, .03), h),
                     0.055, 0.048, sides=6)
        me = _mesh("fence_post", V, F)
        me.materials.append(m_post if f > 0.55 else m_low)
        _put("fence_post", me, cls="fence")


def _bed_edging(mat):
    """Report S1 layer table: low rustic timber edging 0.30-0.45 m high at
    Z 6.0-6.6 m, i.e. just beyond the 0.14 m mulch step at the lawn edge."""
    R = _RNG
    pts = [_ref_world(x, 6.0 + 0.6 * (x / 700.0)) for x in
           range(60, 760, 44)]
    for i in range(len(pts) - 1):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        h = R.uniform(0.30, 0.45)
        V, F = _tube((x0, y0, 0.02), (x1, y1, 0.02), 0.052, 0.048, sides=5)
        v2, f2 = _tube(((x0 + x1) / 2, (y0 + y1) / 2, 0),
                       ((x0 + x1) / 2, (y0 + y1) / 2, h), 0.045, 0.040, sides=5)
        off = len(V)
        V = list(V) + [tuple(p) for p in v2]
        F = list(F) + [tuple(k + off for k in f) for f in f2]
        me = _mesh("edging", V, F)
        me.materials.append(mat)
        _put("edging", me, cls="edging")


def _sign_on_trunk(xy, m_frame, m_head, m_field, m_ink):
    """Report S4.3 / S7.3.  0.554 x 0.534 m outer frame, centre 1.85 m AG --
    standing eye level.  Ochre frame with a beaded run on all four rails, ochre
    header over a white field, four lines of 60 mm caps in warm dark grey.
    The only typography in the environment.  Plumb to ~0.5 deg.
    """
    x, y = xy
    R = _RNG
    # face the sign at the reference camera (that is how it was measured)
    ang = math.atan2(REF_CAM[1] - y, REF_CAM[0] - x)
    nx, ny = math.cos(ang), math.sin(ang)
    off = 0.245 * 0.5 + 0.012            # clear of the trunk surface
    cz = 1.85
    W, H = 0.554, 0.534
    FW, FH = 0.461, 0.446

    def panel(nm, w, h, dz, depth, mat, dy=0.0):
        hw, hh = w / 2, h / 2
        # local axes: u across (perpendicular to the trunk normal), v = up
        ux, uy = -ny, nx
        px = x + nx * (off + depth) + ux * dy
        py = y + ny * (off + depth) + uy * dy
        V = [(px - ux * hw, py - uy * hw, cz + dz - hh),
             (px + ux * hw, py + uy * hw, cz + dz - hh),
             (px + ux * hw, py + uy * hw, cz + dz + hh),
             (px - ux * hw, py - uy * hw, cz + dz + hh)]
        me = _mesh(nm, V, [(0, 1, 2, 3)], smooth=False)
        me.materials.append(mat)
        return _put(nm, me, cls="sign")

    panel("sign_frame", W, H, 0.0, 0.000, m_frame)
    # header 38 % of the field, white field the lower 62 %
    hh = FH * 0.38
    panel("sign_header", FW, hh, (FH - hh) / 2, 0.006, m_head)
    panel("sign_field", FW, FH - hh, -hh / 2, 0.006, m_field)
    # beaded/dotted run along all four rails
    V, F = [], []
    ux, uy = -ny, nx
    for (u, v) in ([(t, H / 2 - 0.018) for t in np.arange(-W / 2 + .02, W / 2, .034)] +
                   [(t, -H / 2 + 0.018) for t in np.arange(-W / 2 + .02, W / 2, .034)] +
                   [(W / 2 - 0.018, t) for t in np.arange(-H / 2 + .04, H / 2 - .03, .034)] +
                   [(-W / 2 + 0.018, t) for t in np.arange(-H / 2 + .04, H / 2 - .03, .034)]):
        cx = x + nx * (off + 0.004) + ux * u
        cy = y + ny * (off + 0.004) + uy * v
        s = 0.007
        o = len(V)
        V.extend([(cx - ux * s, cy - uy * s, cz + v - s),
                  (cx + ux * s, cy + uy * s, cz + v - s),
                  (cx + ux * s, cy + uy * s, cz + v + s),
                  (cx - ux * s, cy - uy * s, cz + v + s)])
        F.append((o, o + 1, o + 2, o + 3))
    me = _mesh("sign_beads", V, F, smooth=False)
    me.materials.append(m_ink)
    _put("sign_beads", me, cls="sign")

    # the lettering: FAVOR DE / ORDENAR / Y PAGAR / AQUI, 60 mm caps
    # four lines of 60 mm caps filling the white field, which is the lower 62 %
    # of a 0.446 m field centred at 1.85 m: y 237-288 px in the reference, a
    # 62.5 mm line pitch (report S4.3)
    lines = ("FAVOR DE", "ORDENAR", "Y PAGAR", "AQUI")
    base = (cz - FH / 2) + (FH - hh) / 2 + 1.5 * 0.0625
    for i, txt in enumerate(lines):
        cu = bpy.data.curves.new(PREFIX + "txt_%d" % i, type='FONT')
        cu.body = txt
        cu.size = 0.060                       # measured capital height
        cu.align_x = 'CENTER'
        cu.align_y = 'CENTER'
        cu.extrude = 0.0006
        ob = bpy.data.objects.new(PREFIX + "sign_text", cu)
        cu.materials.append(m_ink)
        ob.location = (x + nx * (off + 0.011), y + ny * (off + 0.011),
                       base - i * 0.0625)
        ob.rotation_euler = (math.pi / 2, 0, ang + math.pi / 2)
        _COLL.objects.link(ob)
        _COUNT["sign_text"] = _COUNT.get("sign_text", 0) + 1


def _rolled_mat(xy, mat):
    """Report S1: a pale mint-green, finely transverse-ribbed cylinder,
    ~0.13 x 0.39 m, leaning against the trunk.  NOT IDENTIFIABLE as a plant --
    a rolled mat or a coiled hose.  It is in the reference, so it is here."""
    x, y = xy
    ang = math.atan2(REF_CAM[1] - y, REF_CAM[0] - x) + 0.5
    bx, by = x + 0.19 * math.cos(ang), y + 0.19 * math.sin(ang)
    V, F = _tube((bx, by, 0.01), (x + 0.055 * math.cos(ang),
                                  y + 0.055 * math.sin(ang), 0.39),
                 0.066, 0.062, sides=10)
    me = _mesh("rolled_mat", V, F)
    me.materials.append(mat)
    _put("rolled_mat", me, cls="prop")


def _palapa_corner(m_oxb, m_scroll, m_board, m_pole, m_pend):
    """Report S4.2.  The top-left corner of the reference frame: an oxblood
    painted panel with cream scrollwork and a scalloped bead fringe, a spun
    metal pendant below it, a green painted board behind, and a rustic
    vertical-pole screen in the deep background.

    Placed on the palapa's own structure just left of the reference camera's
    axis and above eye level.  Depths in S4.2 are explicitly NOT MEASURABLE, so
    these sit at the nearest depth the frame allows and are kept small.
    """
    R = _RNG
    # panel: image x 0-100, y 15-128 -> put it on the palapa post line, close.
    px, py = _ref_world(40, 3.30)
    ang = math.atan2(REF_CAM[1] - py, REF_CAM[0] - px)
    ux, uy = -math.sin(ang), math.cos(ang)

    def board(nm, w, h, cz, mat, back=0.0, dy=0.0):
        hw, hh = w / 2, h / 2
        cx = px + math.cos(ang) * back + ux * dy
        cy = py + math.sin(ang) * back + uy * dy
        V = [(cx - ux * hw, cy - uy * hw, cz - hh),
             (cx + ux * hw, cy + uy * hw, cz - hh),
             (cx + ux * hw, cy + uy * hw, cz + hh),
             (cx - ux * hw, cy - uy * hw, cz + hh)]
        me = _mesh(nm, V, [(0, 1, 2, 3)], smooth=False)
        me.materials.append(mat)
        return _put(nm, me, cls="palapa")

    board("palapa_panel", 0.62, 0.66, 2.72, m_oxb)
    board("palapa_scroll", 0.44, 0.30, 2.80, m_scroll, back=-0.012)
    # scalloped cream bead fringe along the lower edge
    V, F = [], []
    for t in np.arange(-0.29, 0.30, 0.036):
        cx = px + ux * t
        cy = py + uy * t
        s = 0.016
        o = len(V)
        V.extend([(cx - ux * s, cy - uy * s, 2.39),
                  (cx + ux * s, cy + uy * s, 2.39),
                  (cx + ux * s, cy + uy * s, 2.39 - 0.030),
                  (cx - ux * s, cy - uy * s, 2.39 - 0.030)])
        F.append((o, o + 1, o + 2, o + 3))
    me = _mesh("palapa_fringe", V, F, smooth=False)
    me.materials.append(m_scroll)
    _put("palapa_fringe", me, cls="palapa")
    board("palapa_board_green", 0.55, 0.24, 2.19, m_board, back=0.55)

    # pendant: spun-metal dome, apex about 0.33 m below the panel
    dx = px + math.cos(ang) * 0.10
    dy2 = py + math.sin(ang) * 0.10
    ns = 7
    t = np.linspace(0, 1, ns)
    pts = np.stack([np.full(ns, dx), np.full(ns, dy2), 2.36 - 0.20 * t], 1)
    rad = 0.02 + 0.20 * np.sin(np.pi * 0.5 * t) ** 1.5
    V, F = _curved_stem(pts, rad, sides=14)
    me = _mesh("pendant", V, F)
    me.materials.append(m_pend)
    _put("pendant", me, cls="palapa")
    V, F = _tube((dx, dy2, 2.40), (dx, dy2, 2.95), 0.008, 0.008, sides=5)
    me = _mesh("pendant_rod", V, F)
    me.materials.append(m_pend)
    _put("pendant_rod", me, cls="palapa")

    # rustic vertical-pole screen in the deep background (image x 20-95, y 196-262)
    sx, sy = _ref_world(60, 9.0)
    ang2 = math.atan2(REF_CAM[1] - sy, REF_CAM[0] - sx)
    u2x, u2y = -math.sin(ang2), math.cos(ang2)
    V, F = [], []
    for t in np.arange(-1.3, 1.31, 0.085):
        cx = sx + u2x * t + R.uniform(-0.01, 0.01)
        cy = sy + u2y * t + R.uniform(-0.01, 0.01)
        h = R.uniform(1.35, 1.75)
        vv, ff = _tube((cx, cy, 0), (cx, cy, h), 0.032, 0.028, sides=5)
        o = len(V)
        V.extend([tuple(p) for p in vv])
        F.extend([tuple(k + o for k in f) for f in ff])
    me = _mesh("pole_screen", V, F)
    me.materials.append(m_pole)
    _put("pole_screen", me, cls="palapa")


def _furniture(m_lam, m_alu, m_vinyl, m_chrome, m_steel, m_ging):
    """Report S4.4 / S7.4.  Two tables at the measured depths with 0.85 m tops,
    55 mm brushed-aluminium edge bands, low-back diner chairs in burnt-orange
    vinyl on chrome tube, a stainless napkin box per table, and a 25 mm green
    gingham skirt on the near table only.

    These occupy the bottom-left third of the reference frame at Z 3.8-5.0 m and
    are what makes it read as a place where you sat down.
    """
    R = _RNG
    tables = [(_ref_world(380, 4.86), 0.75, True),
              (_ref_world(250, 4.39), 0.75, False)]

    def box(nm, c, size, mat, rot=0.0, smooth=False):
        sx, sy, sz = (s / 2 for s in size)
        pts = [(-sx, -sy, -sz), (sx, -sy, -sz), (sx, sy, -sz), (-sx, sy, -sz),
               (-sx, -sy, sz), (sx, -sy, sz), (sx, sy, sz), (-sx, sy, sz)]
        ca, sa = math.cos(rot), math.sin(rot)
        V = [(c[0] + p[0] * ca - p[1] * sa, c[1] + p[0] * sa + p[1] * ca,
              c[2] + p[2]) for p in pts]
        F = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5),
             (2, 3, 7, 6), (3, 0, 4, 7)]
        me = _mesh(nm, V, F, smooth=smooth)
        me.materials.append(mat)
        return _put(nm, me, cls="furniture")

    for k, ((tx, ty), th, skirt) in enumerate(tables):
        rot = math.atan2(ty - REF_CAM[1], tx - REF_CAM[0]) + R.uniform(-.2, .2)
        box("table%d_top" % k, (tx, ty, th), (0.85, 0.60, 0.030), m_lam, rot)
        box("table%d_band" % k, (tx, ty, th - 0.028), (0.855, 0.605, 0.055),
            m_alu, rot)
        V, F = _tube((tx, ty, 0), (tx, ty, th - 0.06), 0.035, 0.030, sides=8)
        me = _mesh("table%d_leg" % k, V, F)
        me.materials.append(m_chrome)
        _put("table%d_leg" % k, me, cls="furniture")
        box("table%d_foot" % k, (tx, ty, 0.012), (0.44, 0.44, 0.024), m_chrome,
            rot)
        box("table%d_napkins" % k, (tx + 0.18, ty - 0.10, th + 0.075),
            (0.11, 0.09, 0.12), m_steel, rot)
        if skirt:
            # skirt only, on the near table (report S4.4)
            hw, hd, hh = 0.455, 0.325, 0.62
            ca, sa = math.cos(rot), math.sin(rot)
            corners = [(-hw, -hd), (hw, -hd), (hw, hd), (-hw, hd)]
            V, F = [], []
            for i in range(4):
                a = corners[i]
                b = corners[(i + 1) % 4]
                for (p, q) in ((a, b),):
                    o = len(V)
                    for (u, v) in (p, q):
                        px = tx + u * ca - v * sa
                        py = ty + u * sa + v * ca
                        V.append((px, py, th - 0.02))
                        V.append((px * 1.004, py * 1.004, th - 0.02 - hh))
                    F.append((o, o + 2, o + 3, o + 1))
            me = _mesh("table%d_cloth" % k, V, F, smooth=False)
            me.materials.append(m_ging)
            _put("table%d_cloth" % k, me, cls="furniture")
        # two chairs per table, chair back top 0.71 m above the floor
        for s in (-1, 1):
            ang = rot + (0 if s > 0 else math.pi) + R.uniform(-.25, .25)
            cxx = tx + math.cos(ang) * 0.72
            cyy = ty + math.sin(ang) * 0.72
            box("chair%d_seat" % k, (cxx, cyy, 0.44), (0.42, 0.42, 0.055),
                m_vinyl, ang)
            bx = cxx + math.cos(ang) * 0.19
            by = cyy + math.sin(ang) * 0.19
            box("chair%d_back" % k, (bx, by, 0.63), (0.40, 0.07, 0.20),
                m_vinyl, ang)
            for (ox, oy) in ((-0.17, -0.17), (0.17, -0.17), (0.17, 0.17),
                             (-0.17, 0.17)):
                ca2, sa2 = math.cos(ang), math.sin(ang)
                lx = cxx + ox * ca2 - oy * sa2
                ly = cyy + ox * sa2 + oy * ca2
                V, F = _tube((lx, ly, 0), (lx, ly, 0.42), 0.014, 0.013, sides=5)
                me = _mesh("chair%d_leg" % k, V, F)
                me.materials.append(m_chrome)
                _put("chair%d_leg" % k, me, cls="furniture")


def _backdrop(mat, puffs, dark_mat):
    """What is behind the last plant.

    Report S3.7: THERE IS NO SKY IN FRAME.  Report S6: the canopy's shadow
    floor is CONSTANT with depth at Y p5 = 0.0141 - 0.0190, i.e. about 0.024 x
    the cream -- the deep garden behind the leaves never gets lighter.  Without
    something at that value the world shows through every gap in the canopy and
    the plants silhouette against it; that single failure will undo the value
    work no matter what the median says, and it is what a hero built on a sky
    world would do.

    The shell is CAMERA-ONLY: it is invisible to diffuse, glossy, transmission
    and shadow rays, so it fills gaps for the lens and contributes exactly
    nothing to the lighting solution.  The puffs just inside it are ordinary
    geometry and do light normally, so the transition is not a flat wall.
    """
    R, TOP, N = 23.0, 13.0, 72
    V, F = [], []
    for i in range(N):
        a = 2 * math.pi * i / N
        V.append((R * math.cos(a), R * math.sin(a), -0.5))
        V.append((R * math.cos(a), R * math.sin(a), TOP))
    for i in range(N):
        j = (i + 1) % N
        F.append((2 * i, 2 * i + 1, 2 * j + 1, 2 * j))     # normals inward
    me = _mesh("backdrop_shell", V, F, smooth=False)
    me.materials.append(mat)
    ob = _put("backdrop_shell", me, cls="backdrop")
    for a in ("visible_diffuse", "visible_glossy", "visible_transmission",
              "visible_volume_scatter", "visible_shadow"):
        if hasattr(ob, a):
            setattr(ob, a, False)
    # a broken fringe of very dark foliage in front of it
    Rn = _RNG
    for _ in range(300):
        a = Rn.uniform(0, 2 * math.pi)
        r = Rn.uniform(17.0, 21.5)
        _put("backdrop_mass", Rn.choice(puffs),
             loc=(r * math.cos(a), r * math.sin(a), Rn.uniform(0.6, 7.4)),
             scale=Rn.uniform(1.6, 3.4),
             rot=(Rn.uniform(0, 6.28), Rn.uniform(0, 6.28),
                  Rn.uniform(0, 6.28)), cls="backdrop")


def _belt(crowns_big, crowns_mid, crowns_cane, paddles, straps, puffs_under,
          puffs_band, heads, florets, m_trunk, m_cane_s, m_stemring):
    """Continue the measured planting vocabulary around the terrace.

    The reference frames one wedge of a garden.  Nothing in the report says the
    planting stops where the frame does -- S1 records masses running off every
    edge - and a hero from any other azimuth needs the same wall behind the
    vehicle.  Values, heights and species are the measured ones; only the
    positions are extrapolated, and they are all beyond BELT_R_IN so they can
    never intrude on the measured near field.
    """
    R = _RNG
    # tall palms
    for (x, y) in _scatter(26, BELT_R_IN, BELT_R_OUT, margin=0.6):
        h = R.uniform(3.4, 6.2)
        _palm("belt_palm", (x, y), h, R.uniform(0.16, 0.26),
              crowns_big if h > 4.6 else crowns_mid,
              m_trunk if R.random() < 0.7 else m_stemring,
              lean=R.uniform(0, 0.35), crown_scale=R.uniform(0.75, 1.25))
    # cane clumps -- the standard Riviera-Maya screening palm (report S1 P4)
    for (x, y) in _scatter(16, BELT_R_IN, BELT_R_OUT - 2.0, margin=0.5):
        _cane_clump("belt_clump", (x, y), R.uniform(2.8, 4.3), crowns_cane,
                    m_cane_s, ncane=R.randint(7, 13))
    # paddle leaves -- the chroma peak, so they are used sparingly
    for (x, y) in _scatter(14, BELT_R_IN, BELT_R_OUT - 3.0, margin=0.4):
        _paddle_plant("belt_paddle", (x, y), R.uniform(1.4, 2.9), paddles,
                      m_cane_s, nleaf=R.randint(4, 7),
                      scale=R.uniform(0.8, 1.15))
    # agaves at the front of the belt
    for (x, y) in _scatter(10, BELT_R_IN - 0.4, BELT_R_IN + 2.6, margin=0.3):
        _put("belt_agave", R.choice(straps), loc=(x, y, 0.05),
             rot=(0, 0, R.uniform(0, 6.28)), scale=R.uniform(0.7, 1.1),
             cls="agave")
    # understorey: the dark bottom of the value range, 60 % of the pixel mass
    for (x, y) in _scatter(560, BELT_R_IN - 0.8, BELT_R_OUT, margin=0.0):
        _put("belt_shrub", R.choice(puffs_under),
             loc=(x, y, R.uniform(0.18, 0.75)), scale=R.uniform(0.7, 1.7),
             rot=(R.uniform(-0.3, 0.3), R.uniform(-0.3, 0.3),
                  R.uniform(0, 6.28)), cls="shrub")
    # a mid-height green mass to close the gap between shrub and canopy
    for (x, y) in _scatter(360, BELT_R_IN - 0.4, BELT_R_OUT, margin=0.0):
        _put("belt_mass", R.choice(puffs_band),
             loc=(x, y, R.uniform(0.9, 2.6)), scale=R.uniform(0.9, 1.9),
             rot=(R.uniform(0, 6.28), R.uniform(0, 6.28), R.uniform(0, 6.28)),
             cls="shrub")
