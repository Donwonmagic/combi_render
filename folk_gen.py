"""Flank folk art -- `tex/swirl.png` (show side) and `tex/swirl_b.png` (off side).

rev 10.  REBUILT against `/home/claude/work/measure/folk_door.md`, which
re-measured the cab door in the DOOR'S OWN PLANE (the door is swung open ~49
deg in `ref_side.jpg`, so every earlier column-scan of "body x" over the door
was sampling the wrong surface).

What that measurement changed
-----------------------------
    quantity                       old generator / SPEC 10.9   folk_door.md
    cab-door gold coverage         0.0 - 0.2 %                 29.08 % +/- 2
    gold / red luma ratio          not controlled              2.048  (core)
    cream rosettes                 "scattered densely", 26     3.90 %, 10 of them
    rosette diameter               random 0.017-0.032 of tile  median 0.072 of
                                                               door width
    dark-brown outline on the door 9 commas scattered over it  0.48 % (<= 2 %)
                                                               -- it is NOT a
                                                               door feature
    dark-brown outline elsewhere   -                           lower nose 2.42 %,
                                                               rear quarter (a
                                                               28 mm stroke
                                                               resolves there)
    gold across the door           flat                        42 % at u < 0.25
                                                               -> 5 % at u > 0.75
    forward flank "bare"           0.0 - 0.2 %                 0.7 - 3.3 %

The old tile was a MOTIF FIELD: motifs at random positions in tile space, with
`t1_mats.body_paint` deciding where they landed on the body via a MapRange
density mask on object X.  That cannot reproduce the measurement, for two
reasons that are structural, not tuning:

  * the mask modulates ALPHA only.  It cannot put dark-brown ink on the lower
    nose and the rear quarter and keep it off the cab door -- that is a
    per-class, per-station statement.
  * the mask is a threshold on a noise field.  It cannot deliver a 42 % -> 5 %
    ramp across a 0.94 m door.

So this generator is now BODY-STATION AWARE.  It knows the object-space -> tile
mapping that `t1_mats.body_paint` applies and paints each motif at the body
station the measurement puts it at.  Density-vs-x and class-vs-x are baked into
the tile.  See MAPPING CONTRACT below -- if those numbers move in t1_mats.py,
this file must be re-run with them.

MAPPING CONTRACT  (t1_mats.body_paint, the `mp` Mapping node + `swirl` BOX)
---------------------------------------------------------------------------
    tile_co   = MAP_LOC + MAP_SCALE * object_position         (Mapping, POINT)
    flank (normal +/-Y) samples (tile_co.x, tile_co.z)        (BOX projection)
    Blender mirrors u on ONE of the two Y faces, which is audit finding
    materials-14 -- the off flank is the show flank mirrored.  See SIDES below.

    u = U0 + SGN * MAP_SCALE * x      v = MAP_LOC[2] + MAP_SCALE * z
    1 texel = 1.878 mm on the body;  the tile period is 3.846 m.

SIDES
-----
`studio.views()` puts hero34f at y = +8.55 (the reference-photo angle, so +Y is
the show flank, the one `ref_side.jpg` shows) and front34 at y = -6.60.  Both
flanks are therefore in the hero set, which is why materials-14 matters.

This file writes TWO tiles with genuinely different compositions, both obeying
the measured statistics:

    tex/swirl.png    show side (+Y), authored for u = 0.815 - 0.26 x
    tex/swirl_b.png  off  side (-Y), authored for u = 0.185 + 0.26 x

`t1_mats.py` must be changed to select between them -- see the block comment at
the bottom of this file.  Until it is, only swirl.png is read and the off side
keeps materials-14.

Verification (run this file; every number is measured with numpy, in BODY
coordinates, by sampling the tile the way the shader samples it):
  * cab door -- class fractions and the 20-bin / 10-bin gold profiles of sec.5
  * lower nose -- sec.10's 11.44 % gold / 2.42 % dark over its own wedge
  * flank -- sec.11's gold/(red+gold) in the report's own X bins
  * contrast -- the tile composited over t1_mats.RED in linear light, Rec.709
    luma on sRGB codes, gold core / cream core / dark core against sec.7;
    and the same tile through the UNPATCHED body_paint, which shows the
    contrast target is blocked there, not here
  * materials-14 -- both tiles sampled onto the same body grid and correlated
    over every shift and both parities, raw and after removing each side's own
    local density (which the two sides are supposed to share)

What is NOT measured, and is flagged as such wherever it is used
----------------------------------------------------------------
  * rear-quarter DARK and CREAM percentages.  folk_door.md gives a dark figure
    for the lower nose (2.42 %) and says a 28 mm dark stroke resolves on the
    rear quarter, but no rear-quarter area fraction.  REAR_DARK / REAR_CREAM
    below are extrapolations from the same painter's hand and are printed with
    the word "extrapolated" against them.
  * the gold density profile DOWN the panel is measured on the door only
    (sec.5).  It is reused as the shape for the rest of the flank.
  * the strip below the cab-door shut line has no measurement of its own; it is
    carried at the near-bare mid-flank rate.
  * rosette internal structure is below the photograph's resolution on the door
    (8-11 px).  sec.4 says to take it from the rear quarter at (890, 545), and
    that is what the rosette() sub-structure is: cream pearl ring, cream
    scalloped ring, gold disc, dark centre.  At 1.878 mm/texel the smallest
    measured rosette (0.031 of door width = 28 mm) resolves to 15 texels, so
    its dark centre is ~2 texels across -- present but at the limit.

Palette
-------
folk_door.md sec.6 is explicit that its sRGB medians are PHOTOGRAPH values, not
albedo.  What is transferable is the CONTRAST, sec.7: gold core reads 2.048x
the adjacent red in luma (Rec.709 weights on sRGB code values), cream 2.348x,
pure dark ink 0.49x.  So the measured chromaticities are kept and their
luminances are solved so that, composited over this project's own measured
livery red (t1_mats.RED), those three ratios come out exactly.
"""
import math
import os
import re
import numpy as np
from PIL import Image, ImageDraw

try:
    from scipy import ndimage
except ImportError:                                   # colour-bleed pass only
    ndimage = None

HERE = os.path.dirname(os.path.abspath(__file__))
TEXDIR = os.path.join(HERE, "tex")

# ===========================================================================
# 1.  MAPPING CONTRACT -- must match t1_mats.body_paint
# ===========================================================================
MAP_LOC = (0.185, 0.410, 0.263)      # Mapping node Location
MAP_SCALE = 0.26                     # Mapping node Scale (uniform)
N = 2048                             # tile size
SS = 3                               # supersample factor (0.626 mm sub-texel)
TILE = N * SS
PPM = MAP_SCALE * TILE               # sub-texels per metre = 1597.4

# u = U0 + SGN * MAP_SCALE * x
SIDES = {
    # name        U0                  SGN   file
    "show": (1.0 - MAP_LOC[0], -1.0, "swirl.png"),
    "off":  (MAP_LOC[0],       +1.0, "swirl_b.png"),
}


def check_mapping_contract():
    """Read t1_mats.py (never write it) and warn if the mapping has drifted."""
    p = os.path.join(HERE, "t1_mats.py")
    try:
        src = open(p).read()
    except OSError:
        return
    i = src.find("def body_paint(")
    j = src.find("\ndef ", i + 1) if i >= 0 else -1
    src = src[i:j] if i >= 0 else src
    loc = re.search(r'mp\.inputs\["Location"\]\.default_value\s*=\s*\(([^)]*)\)', src)
    sca = re.search(r'mp\.inputs\["Scale"\]\.default_value\s*=\s*\(([^)]*)\)', src)
    bad = []
    if loc:
        got = tuple(float(t) for t in loc.group(1).split(","))
        if max(abs(a - b) for a, b in zip(got, MAP_LOC)) > 1e-6:
            bad.append("Location %s != MAP_LOC %s" % (got, MAP_LOC))
    if sca:
        got = float(sca.group(1).split(",")[0])
        if abs(got - MAP_SCALE) > 1e-6:
            bad.append("Scale %.4f != MAP_SCALE %.4f" % (got, MAP_SCALE))
    for b in bad:
        print("  !! MAPPING CONTRACT BROKEN: %s -- the baked art will land at "
              "the wrong body station. Update the constants here and re-run."
              % b)


# ===========================================================================
# 2.  BODY GEOMETRY -- read off t1_core.py / t1_shell.py, never imported
#     (importing them needs bpy).  Object-space z == height above ground:
#     step 8b shears the shell by rake_drop(x) = RAKE_Z0 + RAKE_DZDX * x.
# ===========================================================================
RAKE_Z0, RAKE_DZDX = 0.0365, 0.0330          # t1_core.py:56-57
Z_BELT0 = 1.2355                             # t1_mats.py:130
X_NOSE, X_TAIL = 2.108, -2.108               # t1_core.py:26-27

# cab-door shut line, t1_shell.DOOR_GAP (authored z, un-sheared)
DOOR_X0, DOOR_X1 = 0.9084, 1.8171            # latch (aft) .. hinge (fwd)
DOOR_W = DOOR_X1 - DOOR_X0                   # 0.9087 m  (measured 0.94)
_DOOR_BOT_AUTH = [(0.9084, 0.8160), (1.1000, 0.8040), (1.4000, 0.8000),
                  (1.6500, 0.8040), (1.8171, 0.8120)]
_DOOR_TOP_AUTH = 1.8140                      # top rail of the shut line
# rocker / sill bottom, t1_core.ZB (authored z)
_ZB_AUTH = [(-2.108, 0.468), (-2.000, 0.394), (-1.600, 0.387), (-0.400, 0.385),
            (0.400, 0.385), (1.000, 0.387), (1.500, 0.391), (1.800, 0.397),
            (1.960, 0.408), (2.040, 0.430), (2.108, 0.520)]
# the flank proper: outside this the body wraps to the +/-X faces of the box
# projection and a (x, z) authored motif is not what gets sampled.
FLANK_X0, FLANK_X1 = -2.000, 2.030
# no flank op may reach x < XART_LO: at MAP_SCALE 0.26 that wraps onto the
# cab door's hinge edge (x = -2.029 is the same texel as x = +1.817).
XART_LO, XART_HI = -2.026, 2.028


def _lut(tab, x):
    xs = [t[0] for t in tab]
    ys = [t[1] for t in tab]
    return float(np.interp(x, xs, ys))


def rake_drop(x):
    return RAKE_Z0 + RAKE_DZDX * x


def belt_z(x):
    """cream/red break line in object space (t1_mats: Z_BELT0 - RAKE*x)."""
    return Z_BELT0 - RAKE_DZDX * x


def sill_z(x):
    return _lut(_ZB_AUTH, x) - rake_drop(x)


def door_bot_z(x):
    return _lut(_DOOR_BOT_AUTH, x) - rake_drop(x)


DOOR_H = ((_DOOR_TOP_AUTH - rake_drop(1.36)) - door_bot_z(1.36))   # ~1.017 m


def panel_top(x):
    """top of the paintable red field."""
    return belt_z(x)


def panel_bot(x):
    if DOOR_X0 <= x <= DOOR_X1:
        return door_bot_z(x)
    return sill_z(x)


# ===========================================================================
# 3.  MEASURED TARGETS -- folk_door.md
# ===========================================================================
DOOR_GOLD = 29.08          # sec.3, % of the painted panel
DOOR_CREAM = 3.90
DOOR_DARK = 0.50           # 0.48 measured, bounded <= 2
BELT_MARGIN = 0.052        # sec.5: top tenth of the panel only 4.5 % gold

# sec.5, gold % per bin ACROSS the door, u = 0 (hinge) -> 1 (latch)
DOOR_U_PROFILE = np.array([
    45.4, 53.3, 48.9, 33.2, 29.4, 40.8, 33.4, 46.6, 43.5, 38.6,
    53.1, 36.3, 20.7, 6.4, 20.2, 4.7, 3.1, 8.6, 2.2, 7.0])
# sec.5, gold % per bin DOWN the panel, belt -> bottom
DOOR_V_PROFILE = np.array([
    4.5, 17.7, 20.1, 41.1, 42.0, 37.2, 43.3, 29.2, 34.7, 15.7])

# sec.9 motif map.  u = 0 at the hinge (front) edge, v over the WHOLE door with
# the belt at 0.5058;  d = equivalent-area diameter as a fraction of door width.
BELT_V = 0.5058
# sec.9's `d` is the HORIZONTAL extent as a fraction of door width -- the one
# sec.2 calls exact (vertical mm carry the 5.3 % rectification stretch, which
# is also why the equivalent-area diameters in sec.4 run ~11 % larger).  Their
# median is 0.0718, the figure sec.4 reports.
ROSETTES = [                                     # (u, v, d)
    (0.422, 0.554, 0.0479), (0.585, 0.636, 0.1106), (0.103, 0.780, 0.0766),
    (0.408, 0.824, 0.1138), (0.865, 0.913, 0.0670), (0.196, 0.922, 0.0809),
    (0.552, 0.929, 0.1191), (0.371, 0.935, 0.0628), (0.716, 0.942, 0.0596),
    (0.065, 0.979, 0.0309)]
CURLS = [                                        # (u, v, su, sv)  sec.9
    (0.529, 0.918, 0.172, 0.117), (0.354, 0.925, 0.106, 0.082),
    (0.869, 0.911, 0.096, 0.090), (0.725, 0.944, 0.068, 0.050)]
EDGE_E = (0.988, 0.593, 0.031, 0.095)
DARK_1 = (0.020, 0.591, 0.028, 0.073)

# sec.11 corrected coverage-vs-X scan.  gold % of (red+gold) painted flank.
# `arch` marks bins the report says are unreliable -- the rear wheel arch eats
# the sampling band there and strips out the low, dense part of the panel, so
# those bins are LOWER BOUNDS, not measurements.  The X -1.34 bin (6.33 %) is
# the artefact the report names explicitly and is discarded outright.
FLANK_SCAN = [   # (X centre, gold %, reliable?)
    (+0.739, 2.41, True), (+0.550, 3.28, True), (+0.361, 2.49, True),
    (+0.171, 1.27, True), (-0.019, 1.16, True), (-0.208, 1.20, True),
    (-0.397, 0.72, True), (-0.587, 2.12, True),
    (-0.776, 8.18, False), (-0.965, 19.18, False), (-1.155, 20.13, False),
    (-1.344, 6.33, None), (-1.534, 11.94, False), (-1.723, 19.12, True),
    (-1.912, 39.81, True)]

# The density model.  Monotone-ish envelope: every reliable bin is hit, every
# arch-affected bin is treated as a lower bound, the -1.34 artefact is dropped.
# Forward of the door the lower nose (sec.10) is 11.44 % gold / 2.42 % dark.
NOSE_GOLD, NOSE_DARK = 11.44, 2.42
FLANK_DENSITY = [           # (x, gold % of the local painted band)
    (2.108, 11.4), (1.900, 11.4), (1.840, 7.0),
    (1.8171, 29.1),                              # <- the door, sec.3
    (0.9084, 29.1),
    (0.860, 3.2), (0.739, 2.41), (0.550, 3.28), (0.361, 2.49), (0.171, 1.27),
    (-0.019, 1.16), (-0.208, 1.20), (-0.397, 0.72), (-0.587, 2.12),
    (-0.776, 9.5), (-0.965, 19.6), (-1.155, 20.3), (-1.344, 20.3),
    (-1.534, 20.2), (-1.723, 19.4), (-1.912, 39.8), (-2.108, 42.0)]
# rear quarter carries the heavy dark curlwork (sec.8: a 28 mm dark stroke
# resolves there).  folk_door.md gives NO rear-quarter dark %, only the lower
# nose's 2.42 %; this is an extrapolation from the same painter's hand and is
# reported as such.
REAR_DARK = 3.0
REAR_CREAM = 4.0


def flank_density(x):
    xs = [t[0] for t in FLANK_DENSITY][::-1]
    ys = [t[1] for t in FLANK_DENSITY][::-1]
    return float(np.interp(x, xs, ys))


def v_profile(pv):
    """gold density multiplier down the panel, pv = 0 at the belt, 1 at the
    bottom.  Measured on the door (sec.5); used as the shape everywhere,
    which is an assumption -- the report measures it on the door only."""
    c = (np.arange(10) + 0.5) / 10.0
    return float(np.interp(pv, c, DOOR_V_PROFILE / DOOR_V_PROFILE.mean()))


def u_profile(ud):
    c = (np.arange(20) + 0.5) / 20.0
    return float(np.interp(ud, c, DOOR_U_PROFILE / DOOR_U_PROFILE.mean()))


# ===========================================================================
# 4.  PALETTE -- chromaticity measured (sec.6), luminance solved for the
#     contrast ratios of sec.7 against this project's own livery red.
# ===========================================================================
RED_LIN = np.array([0.5520, 0.0294, 0.0176])      # t1_mats.RED
LUMA_W = np.array([0.2126, 0.7152, 0.0722])       # Rec.709 on sRGB CODE values


def lin_to_srgb(a):
    a = np.clip(a, 0.0, 1.0)
    return np.where(a <= 0.0031308, a * 12.92, 1.055 * a ** (1 / 2.4) - 0.055)


def srgb_to_lin(a):
    a = np.clip(np.asarray(a, float), 0.0, 1.0)
    return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)


def code_luma(lin):
    return float(np.dot(lin_to_srgb(np.asarray(lin, float)) * 255.0, LUMA_W))


RED_LUMA = code_luma(RED_LIN)                     # 78.3


def _solve_luma(srgb255, target):
    """scale a measured chromaticity in LINEAR light until its sRGB-code luma
    equals `target`."""
    base = srgb_to_lin(np.asarray(srgb255, float) / 255.0)
    lo, hi = 1e-4, 40.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if code_luma(base * mid) < target:
            lo = mid
        else:
            hi = mid
    return base * (0.5 * (lo + hi))


# class ids used in the label raster
NONE, GOLD, GOLDS, CREAM, DARK = 0, 1, 2, 3, 4
GOLD_CLASSES = (GOLD, GOLDS)

PAL = {
    GOLD:  _solve_luma((194, 146, 6), 2.048 * RED_LUMA),    # sec.7 gold core
    GOLDS: _solve_luma((194, 146, 6), 2.048 * RED_LUMA * 0.88),  # shaded side
    CREAM: _solve_luma((198, 164, 105), 2.348 * RED_LUMA),  # sec.7 rosette
    DARK:  _solve_luma((75, 17, 13), 0.490 * RED_LUMA),     # sec.7 pure ink
}


# ===========================================================================
# 5.  RASTERISER.  Ops are authored in BODY metres (x, z) and drawn through the
#     mapping contract, three times (u-1, u, u+1) so the tile wraps.
# ===========================================================================
class Pen:
    def __init__(self, side, view=None):
        self.U0, self.SGN, _ = SIDES[side]
        # view = (col0, row0, w, h) in sub-texels; None = the whole tile
        self.view = view or (0, 0, TILE, TILE)

    def px(self, x, z):
        u = self.U0 + self.SGN * MAP_SCALE * x
        v = MAP_LOC[2] + MAP_SCALE * z
        return u * TILE - self.view[0], (1.0 - v) * TILE - self.view[1]

    def m(self, d):
        return d * PPM


def _tangents(pts):
    n = len(pts)
    t = []
    for i in range(n):
        a = pts[max(i - 1, 0)]
        b = pts[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        t.append((dx / L, dy / L))
    return t


def _stroke_poly(pts, w0, w1, bias=0.0):
    """offset polygon for a tapered stroke through `pts` (already in px)."""
    n = len(pts)
    tg = _tangents(pts)
    left, right = [], []
    for i, (px, py) in enumerate(pts):
        f = i / (n - 1) if n > 1 else 0.0
        w = (w0 + (w1 - w0) * f) * 0.5
        tx, ty = tg[i]
        nx, ny = -ty, tx
        left.append((px + nx * w, py + ny * w))
        right.append((px - nx * w * (1.0 - bias), py - ny * w * (1.0 - bias)))
    return left + right[::-1]


class Raster:
    """label image + the op list that produced it."""

    def __init__(self, pen):
        self.pen = pen
        self.ops = []

    # -- authoring (body metres) -------------------------------------------
    def stroke(self, cls, pts_xz, w0, w1=None, bias=0.0, cap=True):
        self.ops.append(("stroke", cls, list(pts_xz), w0,
                         w0 if w1 is None else w1, bias, cap))

    def disc(self, cls, x, z, r):
        self.ops.append(("disc", cls, x, z, r))

    def poly(self, cls, pts_xz):
        self.ops.append(("poly", cls, list(pts_xz)))

    # -- rasterising --------------------------------------------------------
    def render(self, ops=None):
        pen = self.pen
        w, h = pen.view[2], pen.view[3]
        im = Image.new("L", (w, h), NONE)
        d = ImageDraw.Draw(im)
        for shift in (-TILE, 0, TILE):
            for op in (self.ops if ops is None else ops):
                self._draw(d, op, shift)
        return im

    def _draw(self, d, op, shift):
        pen = self.pen
        kind = op[0]
        if kind == "stroke":
            _, cls, pts, w0, w1, bias, cap = op
            P = [pen.px(x, z) for (x, z) in pts]
            P = [(p[0] + shift, p[1]) for p in P]
            if len(P) < 2:
                return
            a, b = pen.m(w0), pen.m(w1)
            if max(a, b) < 0.7:
                return
            d.polygon(_stroke_poly(P, a, b, bias), fill=cls)
            if cap:
                for (px, py), r in ((P[0], a / 2), (P[-1], b / 2)):
                    if r > 0.4:
                        d.ellipse([px - r, py - r, px + r, py + r], fill=cls)
        elif kind == "disc":
            _, cls, x, z, r = op
            px, py = pen.px(x, z)
            px += shift
            R = pen.m(r)
            if R < 0.35:
                return
            d.ellipse([px - R, py - R, px + R, py + R], fill=cls)
        elif kind == "poly":
            _, cls, pts = op
            P = [pen.px(x, z) for (x, z) in pts]
            d.polygon([(p[0] + shift, p[1]) for p in P], fill=cls)


# ===========================================================================
# 6.  MOTIF VOCABULARY.  Everything is authored in body metres.
# ===========================================================================
def spiral(cx, cz, r0, r1, turns, phase, chir=1, n=64, squash=1.0):
    """logarithmic-ish scroll centreline, body metres."""
    pts = []
    for i in range(n):
        f = i / (n - 1)
        t = phase + chir * turns * 2 * math.pi * f
        r = r0 * (r1 / r0) ** f
        pts.append((cx + r * math.cos(t), cz + r * math.sin(t) * squash))
    return pts


def arc(x0, z0, x1, z1, bow, n=32):
    """a bowed line from (x0,z0) to (x1,z1); bow is the sagitta in metres."""
    dx, dz = x1 - x0, z1 - z0
    L = math.hypot(dx, dz) or 1.0
    nx, nz = -dz / L, dx / L
    pts = []
    for i in range(n):
        f = i / (n - 1)
        s = math.sin(math.pi * f) * bow
        pts.append((x0 + dx * f + nx * s, z0 + dz * f + nz * s))
    return pts


def acanthus_scroll(R, cx, cz, size, chir=1, phase=0.0, w=0.055,
                    eyes=(0.30, 0.62), shade=True, dark=0.0):
    """A fat gold C-scroll with rolled end and two inner eye curls -- the
    dominant element of the vocabulary.  `dark` > 0 lays a dark keyline under
    it (rear quarter / lower nose only)."""
    # 0.60 turns from full radius down to a third of it, with the stroke
    # tapering to a fifth: a C-scroll with a rolled end, not a filled disc.
    main = spiral(cx, cz, size, size * 0.34, 0.60, phase, chir)
    if dark > 0:
        R.stroke(DARK, main, w + 2 * dark, w * 0.22 + 2 * dark)
    if shade:
        sh = [(x, z - w * 0.26) for (x, z) in main]
        R.stroke(GOLDS, sh, w * 1.06, w * 0.26)
    R.stroke(GOLD, main, w, w * 0.22)
    # the rolled tip: a short tight coil carrying on from the scroll's end
    tipx, tipz = main[-1]
    roll = spiral(tipx + chir * size * 0.10 * math.cos(phase + 3.4),
                  tipz + size * 0.10 * math.sin(phase + 3.4),
                  size * 0.12, size * 0.03, 0.70, phase + 3.4, chir)
    R.stroke(GOLD, roll, w * 0.30, w * 0.10)
    for f in eyes:
        i = int(f * (len(main) - 1))
        ex, ez = main[i]
        e = spiral(ex, ez, size * 0.34, size * 0.07, 0.66, phase + 2.2, -chir)
        R.stroke(GOLD, e, w * 0.38, w * 0.11)
    return main


def leaf(R, x0, z0, x1, z1, bow, w, cls=GOLD, dark=0.0):
    """a tapered acanthus leaf / tendril."""
    p = arc(x0, z0, x1, z1, bow)
    if dark > 0:
        R.stroke(DARK, p, w + 2 * dark, 2 * dark)
    R.stroke(cls, p, w, w * 0.10)
    return p


def curl(R, cx, cz, size, chir=1, phase=0.0, w=0.030, dark=0.0):
    p = spiral(cx, cz, size * 0.92, size * 0.12, 0.85, phase, chir)
    if dark > 0:
        R.stroke(DARK, p, w + 2 * dark, w * 0.25 + 2 * dark)
    R.stroke(GOLD, p, w, w * 0.25)
    return p


# rosette: outer ring of cream pearls, cream scalloped mid-ring, gold disc,
# DARK CENTRE.  folk_door.md sec.4 -- the door rosettes are 8-11 px in the
# photograph so this sub-structure is taken from the same painter's rosettes on
# the rear quarter at (890, 545), as the report instructs.
# geometry solved so cream / (pi R^2) = ROS_CREAM_FRAC, which is what turns the
# measured 10-rosette disc area into the measured 3.90 % cream.
ROS_PEARLS = 12
ROS_PEARL_R = 0.152        # x R
ROS_PEARL_AT = 0.845       # x R
ROS_MID_IN, ROS_MID_OUT = 0.442, 0.5218
ROS_GOLD_R = 0.400
ROS_DARK_R = 0.155


def rosette(R, cx, cz, d, phase=0.0):
    r = d * 0.5
    for k in range(ROS_PEARLS):
        a = phase + 2 * math.pi * k / ROS_PEARLS
        R.disc(CREAM, cx + r * ROS_PEARL_AT * math.cos(a),
               cz + r * ROS_PEARL_AT * math.sin(a), r * ROS_PEARL_R)
    R.disc(CREAM, cx, cz, r * ROS_MID_OUT)
    R.disc(NONE, cx, cz, r * ROS_MID_IN)
    R.disc(GOLD, cx, cz, r * ROS_GOLD_R)
    R.disc(DARK, cx, cz, r * ROS_DARK_R)


# ===========================================================================
# 7.  CAB DOOR.  Authored in door-local metres:  a = across from the HINGE
#     (front, +x) edge, b = down from the belt.
# ===========================================================================
def door_xz(a, b):
    x = DOOR_X1 - a
    return x, belt_z(x) - b


def door_pv(u, v):
    """motif-map (u, v) from folk_door.md sec.9 -> door-local metres."""
    a = u * DOOR_W
    pv = (v - BELT_V) / (1.0 - BELT_V)
    x = DOOR_X1 - a
    return a, (belt_z(x) - panel_bot(x)) * pv


def build_door(R, rng, variant=0, ws=1.0):
    """G1 / ACANTHUS-MAIN -- one continuous stroke system spanning u 0.000-0.813
    and the full panel height, 86 % of the component gold area -- plus the four
    detached bottom-row curls G2-G5 and the latch-edge sliver G6.
    `variant` re-composes the same inventory for the other flank; `ws` is the
    global stroke-width scale the door solver sets."""
    A = DOOR_W

    def S(a, b):
        return door_xz(a, b)

    if variant == 0:
        acanthus_scroll(R, *S(0.115 * A, 0.300), 0.150, chir=+1, phase=1.05,
                        w=0.064 * ws)
        acanthus_scroll(R, *S(0.070 * A, 0.372), 0.098, chir=-1, phase=3.6,
                        w=0.048 * ws)
        stem = arc(*S(0.055 * A, 0.395), *S(0.395 * A, 0.125), -0.055)
        R.stroke(GOLDS, [(x, z - 0.010) for (x, z) in stem], 0.052 * ws,
                 0.020 * ws)
        R.stroke(GOLD, stem, 0.045 * ws, 0.017 * ws)
        curl(R, *S(0.325 * A, 0.185), 0.070, chir=-1, phase=0.4, w=0.034 * ws)
        curl(R, *S(0.395 * A, 0.310), 0.074, chir=+1, phase=2.5, w=0.036 * ws)
        acanthus_scroll(R, *S(0.520 * A, 0.250), 0.118, chir=-1, phase=2.0,
                        w=0.052 * ws)
        leaf(R, *S(0.470 * A, 0.390), *S(0.610 * A, 0.110), 0.045, 0.034 * ws)
        tail = arc(*S(0.600 * A, 0.235), *S(0.800 * A, 0.412), 0.052)
        R.stroke(GOLDS, [(x, z - 0.006) for (x, z) in tail], 0.030 * ws,
                 0.008 * ws)
        R.stroke(GOLD, tail, 0.025 * ws, 0.007 * ws)
        curl(R, *S(0.788 * A, 0.398), 0.036, chir=+1, phase=1.4, w=0.014 * ws)
        leaf(R, *S(0.360 * A, 0.230), *S(0.455 * A, 0.360), 0.026, 0.030 * ws)
        leaf(R, *S(0.240 * A, 0.155), *S(0.062 * A, 0.140), -0.030, 0.028 * ws)
        leaf(R, *S(0.150 * A, 0.410), *S(0.330 * A, 0.425), 0.028, 0.030 * ws)
        leaf(R, *S(0.430 * A, 0.410), *S(0.560 * A, 0.395), 0.024, 0.024 * ws)
    else:
        acanthus_scroll(R, *S(0.118 * A, 0.325), 0.152, chir=-1, phase=2.3,
                        w=0.064 * ws)
        acanthus_scroll(R, *S(0.196 * A, 0.170), 0.094, chir=+1, phase=0.6,
                        w=0.046 * ws)
        stem = arc(*S(0.070 * A, 0.140), *S(0.380 * A, 0.390), 0.058)
        R.stroke(GOLDS, [(x, z - 0.010) for (x, z) in stem], 0.052 * ws,
                 0.020 * ws)
        R.stroke(GOLD, stem, 0.045 * ws, 0.017 * ws)
        curl(R, *S(0.350 * A, 0.145), 0.072, chir=+1, phase=2.9, w=0.036 * ws)
        curl(R, *S(0.300 * A, 0.395), 0.068, chir=-1, phase=1.1, w=0.032 * ws)
        acanthus_scroll(R, *S(0.545 * A, 0.300), 0.122, chir=+1, phase=4.1,
                        w=0.052 * ws)
        leaf(R, *S(0.480 * A, 0.115), *S(0.625 * A, 0.395), -0.048, 0.034 * ws)
        tail = arc(*S(0.615 * A, 0.355), *S(0.802 * A, 0.155), -0.048)
        R.stroke(GOLDS, [(x, z - 0.006) for (x, z) in tail], 0.030 * ws,
                 0.008 * ws)
        R.stroke(GOLD, tail, 0.025 * ws, 0.007 * ws)
        curl(R, *S(0.792 * A, 0.168), 0.034, chir=-1, phase=3.3, w=0.014 * ws)
        leaf(R, *S(0.365 * A, 0.340), *S(0.458 * A, 0.215), -0.026, 0.030 * ws)
        leaf(R, *S(0.230 * A, 0.415), *S(0.058 * A, 0.398), 0.030, 0.028 * ws)
        leaf(R, *S(0.170 * A, 0.135), *S(0.340 * A, 0.120), -0.026, 0.030 * ws)
        leaf(R, *S(0.440 * A, 0.130), *S(0.570 * A, 0.145), -0.022, 0.024 * ws)

    for i, (u, v, su, sv) in enumerate(CURLS):          # G2..G5, bottom row
        uu = u if variant == 0 else min(0.94, 1.04 - u)
        a, b = door_pv(uu, v)
        curl(R, *S(a, b), 0.42 * su * A, chir=(1 if (i + variant) % 2 else -1),
             phase=1.7 * i + 0.6 * variant, w=0.26 * su * A * ws)
    u, v, su, sv = EDGE_E                                # G6, latch-edge sliver
    uu = u if variant == 0 else 0.012
    a, b = door_pv(uu, v)
    h = sv * DOOR_H
    R.stroke(GOLD, arc(*S(a, b - 0.5 * h), *S(a, b + 0.5 * h), 0.006),
             0.024 * ws, 0.018 * ws)


def door_dark(R, variant=0):
    """DARK-1, and nothing else.  folk_door.md sec.8: vertical luma transects
    across gold->red boundaries ON THE DOOR show NO undershoot below the red --
    the gold falls to red and stops.  There is no dark keyline on this panel;
    the heavy dark curlwork is a rear-quarter and lower-nose feature."""
    u, v, su, sv = DARK_1
    uu = u if variant == 0 else 0.975
    a, b = door_pv(uu, v)
    h = sv * DOOR_H
    R.stroke(DARK, arc(*door_xz(a, b - 0.5 * h), *door_xz(a, b + 0.5 * h),
                       0.004), su * DOOR_W * 0.90, su * DOOR_W * 0.70)


def door_rosettes(R, rng, variant=0):
    """10 rosettes at the measured diameters, six of them in the bottom row at
    v 0.91-0.98 (sec.4).  Cream ring, gold sub-disc, DARK CENTRE."""
    out = []
    for (u, v, d) in ROSETTES:
        if variant == 0:
            uu, vv = u, v
        else:
            # same inventory, different hand: reverse the u order and jitter
            # inside the measured band, so the two flanks do not rhyme
            uu = float(np.clip(1.0 - u + rng.normal(0, 0.030), 0.03, 0.97))
            vv = float(np.clip(v + rng.normal(0, 0.010), BELT_V + 0.03, 0.992))
        a, b = door_pv(uu, vv)
        rosette(R, *door_xz(a, b), d * DOOR_W, phase=rng.random() * 0.5)
        out.append((uu, vv, d))
    return out


# ===========================================================================
# 8.  REST OF THE FLANK
#
#     TEXTURE-WRAP COLLISION.  The tile period is 1/MAP_SCALE = 3.846 m and the
#     flank is 4.01 m long, so body station x and station x - 3.846 SHARE
#     TEXELS.  Concretely x >= +1.866 is the same paint as x <= -1.980: the
#     lower nose and the rear-most quarter cannot be authored independently
#     under a single object-space box projection.  They are therefore authored
#     ONCE, with the nose's own band (z 0.470-0.700, sec.10) carrying the nose
#     composition and the rear bouquet kept above and below it.  The fix is a
#     MAP_SCALE change in t1_mats.py -- see the note at the bottom of this file.
# ===========================================================================
SHARE_X = FLANK_X0 + 1.0 / MAP_SCALE          # +1.866
NOSE_Z0, NOSE_Z1 = 0.470, 0.700               # sec.10 wedge, above the bumper


def full_band(x):
    """the whole painted red field -- the band sec.11's scan measures over."""
    return panel_top(x), panel_bot(x)


def band(x):
    """where art may be PLACED: the same field less the measured 52 mm bare
    margin the painter left under the belt (sec.5)."""
    return panel_top(x) - BELT_MARGIN, panel_bot(x)


def rocker_band(x):
    """strip below the cab-door shut line.  folk_door.md gives no separate
    figure for it; carried at the near-bare mid-flank rate."""
    return door_bot_z(x) - 0.010, sill_z(x)


def nose_band(x):
    return NOSE_Z1, NOSE_Z0


def build_nose(R, rng, variant=0, gs=1.0, ds=1.0):
    """Lower nose, sec.10: ONE bold yellow hook and ONE bold dark-brown
    comma/leaf on plain red -- sparser and larger-stroked than the door, and
    unlike the door it carries resolved heavy dark curlwork.  The wedge sec.10
    measures is only ~0.039 m2, so 11.44 % gold is ~4500 mm2 of stroke and
    2.42 % dark is ~940 mm2: two motifs, not a field."""
    zc = 0.5 * (NOSE_Z0 + NOSE_Z1)
    sgn = 1 if variant == 0 else -1
    R.stroke(DARK, spiral(1.906, zc + 0.045, 0.040, 0.012, 0.46,
                          2.4 + variant, -sgn), 0.026 * ds, 0.008 * ds)
    acanthus_scroll(R, 1.948, zc - 0.008, 0.062, chir=sgn, phase=0.7 + variant,
                    w=0.030 * gs, eyes=(0.45,), shade=False)


def build_rear(R, rng, variant=0, ws=1.0):
    """Rear-quarter bouquet.  sec.8: this is where the heavy dark-brown
    curlwork lives -- a 28 mm dark stroke resolves here and nowhere on the
    door.  Kept clear of the nose band inside the shared strip, and clear of
    x < -2.02 (which would wrap onto the cab door's hinge edge)."""
    dk = 0.013                                   # keyline half-width -> 26 mm
    sgn = 1 if variant == 0 else -1
    t, b = band(-1.90)
    # dominant paisley of the rear-most panel, sitting ABOVE the nose band
    acanthus_scroll(R, -1.900, NOSE_Z1 + 0.175, 0.108, chir=sgn,
                    phase=1.3 + variant, w=0.082 * ws, dark=dk)
    acanthus_scroll(R, -1.860, NOSE_Z1 + 0.400, 0.086, chir=-sgn, phase=3.4,
                    w=0.058 * ws, dark=dk)
    leaf(R, -1.98, t - 0.09, -1.83, t - 0.05, 0.05 * sgn, 0.044 * ws)
    for i, cx in enumerate((-1.56, -1.36, -1.16, -0.99)):
        t2, b2 = band(cx)
        m2 = 0.5 * (t2 + b2)
        acanthus_scroll(R, cx, m2 + 0.05 * (1 if i % 2 else -1),
                        0.150 - 0.008 * i, chir=sgn * (1 if i % 2 else -1),
                        phase=0.8 + 1.9 * i + variant, w=0.060 * ws,
                        dark=dk if i == 0 else 0.0)


def rear_rosettes(R, rng, variant=0, scale=1.0):
    """folk_door.md does NOT measure cream on the rear quarter -- sec.4 only
    says the same painter's rosettes are legible there at ~18 px.  This is an
    extrapolation at REAR_CREAM %, flagged as such in the report."""
    x = -1.985
    while x < -0.86:
        dens = flank_density(x) / 40.0
        if rng.random() < 0.85 * dens * scale:
            t, b = band(x)
            z = b + (t - b) * float(np.clip(rng.beta(2.0, 2.0), 0.06, 0.94))
            d = float(rng.uniform(0.048, 0.098))
            shared = FLANK_X0 <= x <= FLANK_X1 - 1.0 / MAP_SCALE
            if not (shared and NOSE_Z0 - 0.02 - d < z < NOSE_Z1 + 0.02 + d):
                rosette(R, x, z, d, phase=rng.random())
        x += 0.030


# ------------------------------------------------------- filler candidates
def _cands(seed, key, x0, x1, zf, n=34, smin=0.024, smax=0.060, big=1.0):
    """A fixed pool of small curls / tendrils for one cell.  Drawn once, so a
    budget that goes up or down changes only HOW MANY are used, which is what
    makes the density solvers converge."""
    rng = np.random.default_rng([seed] + list(key))
    out = []
    for _ in range(n):
        f = float(rng.random())
        s = float(rng.uniform(smin, smax)) * big
        out.append(dict(x=x0 + (x1 - x0) * float(rng.random()),
                        f=f, s=s, w=s * float(rng.uniform(0.34, 0.54)),
                        ch=1 if rng.random() < 0.5 else -1,
                        ph=float(rng.random()) * 6.283,
                        kind=float(rng.random()), ang=float(rng.random()) * 6.283))
    return out, zf


def _draw_cands(R, pool, zf, k, dark=0.0):
    for c in pool[:int(max(0, round(k)))]:
        x = float(np.clip(c["x"], XART_LO + c["s"], XART_HI - c["s"]))
        c = dict(c, x=x)
        z = zf(c["x"], c["f"])
        if c["kind"] < 0.55:
            curl(R, c["x"], z, c["s"], chir=c["ch"], phase=c["ph"], w=c["w"],
                 dark=dark)
        else:
            s, a = c["s"], c["ang"]
            leaf(R, c["x"] - s * math.cos(a), z - s * 0.75 * math.sin(a),
                 c["x"] + s * math.cos(a), z + s * 0.75 * math.sin(a),
                 s * 0.45 * c["ch"], c["w"], dark=dark)


# ===========================================================================
# 9.  BODY-SPACE SAMPLING.  Every number reported below is read off the tile
#     the way the shader reads it: through the mapping contract, on a grid in
#     BODY coordinates -- not by looking at texels in tile space.
# ===========================================================================
def look(lab, pen, X, Z, wrap=True):
    px, py = pen.px(X, Z)
    c = px.astype(np.int64)
    r = py.astype(np.int64)
    if wrap:
        c = np.mod(c, TILE)
        r = np.mod(r, TILE)
    else:
        c = np.clip(c, 0, lab.shape[1] - 1)
        r = np.clip(r, 0, lab.shape[0] - 1)
    return lab[r, c]


def door_grid(nu=440, nv=240):
    ud = (np.arange(nu) + 0.5) / nu                 # 0 = hinge
    pv = (np.arange(nv) + 0.5) / nv                 # 0 = belt
    UD, PV = np.meshgrid(ud, pv)
    X = DOOR_X1 - UD * DOOR_W
    ZT = Z_BELT0 - RAKE_DZDX * X
    ZB = np.interp(X, [t[0] for t in _DOOR_BOT_AUTH],
                   [t[1] for t in _DOOR_BOT_AUTH]) - RAKE_Z0 - RAKE_DZDX * X
    return X, ZT - PV * (ZT - ZB), UD, PV


def band_grid(x0, x1, nx, nz, bandfn):
    xs = x0 + (x1 - x0) * (np.arange(nx) + 0.5) / nx
    fz = (np.arange(nz) + 0.5) / nz
    X, F = np.meshgrid(xs, fz)
    T = np.array([bandfn(x)[0] for x in xs])[None, :]
    B = np.array([bandfn(x)[1] for x in xs])[None, :]
    return X, B + (T - B) * F


def classify(v):
    return (((v == GOLD) | (v == GOLDS)), v == CREAM, v == DARK)


def frac(lab, pen, X, Z, wrap=True):
    g, c, d = classify(look(lab, pen, X, Z, wrap))
    n = float(X.size)
    return 100 * g.sum() / n, 100 * c.sum() / n, 100 * d.sum() / n


# ===========================================================================
# 10.  SOLVERS.  Closed loop: render, measure in body space, adjust, repeat.
# ===========================================================================
def solve_door(side, seed, variant, verbose=True):
    view = door_view(side)
    pen = Pen(side, view)
    X, Z, UD, PV = door_grid()
    ub = np.clip((UD * 20).astype(int), 0, 19)
    vb = np.clip((PV * 10).astype(int), 0, 9)
    cell = [[(ub == i) & (vb == j) for j in range(10)] for i in range(20)]
    T2 = np.clip(np.outer(DOOR_U_PROFILE, DOOR_V_PROFILE) / DOOR_GOLD, 0, 92.0)

    over = Raster(Pen(side))
    door_dark(over, variant)
    door_rosettes(over, np.random.default_rng(seed + 7), variant)

    def base(ws):
        R = Raster(Pen(side))
        build_door(R, np.random.default_rng(seed), variant, ws)
        return R.ops

    def gold_of(ops):
        R = Raster(pen)
        R.ops = ops
        lab = np.asarray(R.render(), dtype=np.uint8)
        g, c, d = classify(look(lab, pen, X, Z, wrap=False))
        return g, lab

    # 1) global stroke-width scale so the ACANTHUS MASS alone lands at ~68 % of
    #    the measured coverage, leaving the rest for the curl filler
    lo, hi = 0.45, 1.35
    for _ in range(7):
        ws = 0.5 * (lo + hi)
        g, _ = gold_of(base(ws) + over.ops)
        if 100.0 * g.mean() < 0.68 * DOOR_GOLD:
            lo = ws
        else:
            hi = ws
    ws = 0.5 * (lo + hi)
    if verbose:
        print("      acanthus width scale %.3f" % ws)
    under = base(ws)

    # 2) per-cell filler against the max-entropy 2-D target
    pools = {}
    for i in range(20):
        for j in range(10):
            a0, a1 = DOOR_W * i / 20.0, DOOR_W * (i + 1) / 20.0
            j0, j1 = j / 10.0, (j + 1) / 10.0

            def zf(x, f, j0=j0, j1=j1):
                zt, zb = belt_z(x), panel_bot(x)
                return zt - (j0 + (j1 - j0) * f) * (zt - zb)
            pools[(i, j)] = _cands(seed, [i, j], DOOR_X1 - a1, DOOR_X1 - a0,
                                   zf, n=64, smin=0.013, smax=0.040)
    # Controller.  The SHAPE is set by a per-cell residual against the
    # max-entropy 2-D target; the LEVEL is then set by bisecting one global
    # scalar on the whole budget, which is monotone and therefore cannot
    # ratchet the way a clipped per-cell integrator does.
    def draw(nb):
        Rf = Raster(Pen(side))
        for i in range(20):
            for j in range(10):
                p, zf = pools[(i, j)]
                _draw_cands(Rf, p, zf, nb[i, j])
        return under + Rf.ops + over.ops

    def stats(ops):
        g, _ = gold_of(ops)
        A2 = np.array([[100.0 * g[cell[i][j]].mean() for j in range(10)]
                       for i in range(20)])
        uu = np.array([100.0 * g[ub == i].mean() for i in range(20)])
        vv = np.array([100.0 * g[vb == j].mean() for j in range(10)])
        return 100.0 * g.mean(), A2, uu, vv

    Tn = T2 * (DOOR_GOLD / T2.mean())
    K = 0.030                            # motifs per percentage-point of gap
    nbud = np.zeros((20, 10))
    ops = draw(nbud)
    tot, A2, uu, vv = stats(ops)
    best, bops = None, ops
    for rnd in range(7):
        raw = np.maximum(0.0, nbud + K * (Tn - A2))
        if raw.sum() <= 0:
            break
        lo, hi = 0.0, 4.0                                  # global level solve
        for _ in range(9):
            lam = 0.5 * (lo + hi)
            t2_, _a, _u, _v = stats(draw(raw * lam))
            if t2_ < DOOR_GOLD:
                lo = lam
            else:
                hi = lam
        nbud = raw * (0.5 * (lo + hi))
        ops = draw(nbud)
        tot, A2, uu, vv = stats(ops)
        urms = float(np.sqrt(((uu - DOOR_U_PROFILE) ** 2).mean()))
        vrms = float(np.sqrt(((vv - DOOR_V_PROFILE) ** 2).mean()))
        cost = abs(tot - DOOR_GOLD) * 3.0 + urms + vrms
        if best is None or cost < best:
            best, bops = cost, ops
        if verbose:
            print("      round %d  gold %6.2f %%  u-rms %5.2f  v-rms %5.2f"
                  % (rnd, tot, urms, vrms))
    return bops


def solve_flank(side, seed, variant, door_ops, verbose=True):
    """Same closed loop for the rest of the flank: hit FLANK_DENSITY(x), which
    is folk_door.md sec.11's corrected scan with the wheel-arch bins treated as
    lower bounds and the X -1.34 artefact discarded.

    Bins forward of x 1.83 are NOT solved: their texels are the rear-most
    quarter's (see the wrap note in section 8) and are authored there, with the
    nose's own z-window (0.470-0.700) left free for the nose composition."""
    pen = Pen(side)
    NB = 56
    edges = np.linspace(FLANK_X0, FLANK_X1, NB + 1)
    Xs, Zs, tgt, live, pools = [], [], [], [], []
    SH_R0, SH_R1 = FLANK_X0, FLANK_X1 - 1.0 / MAP_SCALE      # the shared strip
    for i in range(NB):
        x0, x1 = edges[i], edges[i + 1]
        xc = 0.5 * (x0 + x1)
        indoor = DOOR_X0 - 0.02 < xc < DOOR_X1 + 0.02
        bf = rocker_band if indoor else full_band
        shared = SH_R0 <= xc <= SH_R1
        X, Z = band_grid(x0, x1, 12, 110, bf)
        Xs.append(X)
        Zs.append(Z)
        t = 1.6 if indoor else flank_density(xc)
        tgt.append(t)
        live.append(xc < 1.83)

        def zf(x, f, indoor=indoor, shared=shared):
            tt, bb = (rocker_band if indoor else band)(x)
            if not shared:
                return bb + (tt - bb) * (1.0 - f ** 1.35)
            lo, hi = NOSE_Z0 - 0.018, NOSE_Z1 + 0.018     # leave the nose band
            span = (tt - bb) - (hi - lo)                  # to the nose motifs
            val = bb + span * (1.0 - f ** 1.35)
            return val if val < lo else val + (hi - lo)
        sparse = t < 6.0
        # a motif may not reach past XART_LO, which wraps onto the door
        smax = min(0.030 if sparse else 0.070, max(0.034, x0 - XART_LO))
        pools.append(_cands(seed + 5, [i], x0, x1, zf, n=180,
                            smin=min(0.012 if sparse else 0.026, smax * 0.55),
                            smax=smax))
    tgt = np.array(tgt)
    live = np.array(live)

    def anchors(ws, gs=1.0, ds=1.0):
        R = Raster(Pen(side))
        rng = np.random.default_rng(seed + 31)
        build_nose(R, rng, variant, gs, ds)
        build_rear(R, rng, variant, ws)
        return R.ops

    def rosettes_of(cs):
        R = Raster(Pen(side))
        rear_rosettes(R, np.random.default_rng(seed + 91), variant, cs)
        return R.ops

    def render(ops):
        R = Raster(pen)
        R.ops = ops
        return np.asarray(R.render(), dtype=np.uint8)

    def profile(lab):
        return np.array([frac(lab, pen, Xs[i], Zs[i])[0] for i in range(NB)])

    Xn, Zn = band_grid(1.870, 2.020, 60, 170, nose_band)
    Xc, Zc = band_grid(-2.000, -1.700, 60, 200, full_band)

    def bisect(f, lo, hi, n=7):
        for _ in range(n):
            m = 0.5 * (lo + hi)
            if f(m):
                lo = m
            else:
                hi = m
        return 0.5 * (lo + hi)

    # 1) global width scale on the rear bouquet, so the anchors alone sit under
    #    the target everywhere -- the per-bin filler can only ADD.
    rear = (edges[:-1] > -2.0) & (edges[:-1] < -0.90)
    ws = bisect(lambda m: profile(render(door_ops + anchors(m)))[rear].mean()
                < 0.52 * tgt[rear].mean(), 0.40, 1.30, 6)
    # 2) the two lower-nose motifs, against sec.10's 11.44 % / 2.42 %
    gs = bisect(lambda m: frac(render(door_ops + anchors(ws, m)), pen,
                               Xn, Zn)[0] < NOSE_GOLD, 0.20, 2.2, 8)
    ds = bisect(lambda m: frac(render(door_ops + anchors(ws, gs, m)), pen,
                               Xn, Zn)[2] < NOSE_DARK, 0.05, 2.0, 8)
    anc = anchors(ws, gs, ds)
    if verbose:
        print("      scales: rear bouquet %.3f  nose gold %.3f  nose dark %.3f"
              % (ws, gs, ds))

    # 4) per-bin filler.  Each bin's target is independent, so a damped
    #    proportional controller is enough; motif spill between bins is a
    #    smoothing operator and does not destabilise it.
    nbud = np.zeros(NB)
    K = 0.30
    best, bops, blab = None, None, None
    for it in range(30):
        Rf = Raster(Pen(side))
        for i in range(NB):
            if live[i]:
                p, zf = pools[i]
                _draw_cands(Rf, p, zf, nbud[i])
        ops = door_ops + anc + Rf.ops
        lab = render(ops)
        got = profile(lab)
        err = (got - tgt)[live]
        rms = float(np.sqrt((err ** 2).mean()))
        if best is None or rms < best:
            best, bops, blab = rms, ops, lab
        if verbose and it % 4 == 0:
            print("      iter %2d  flank rms %5.2f  max %5.2f"
                  % (it, rms, float(np.abs(err).max())))
        nbud = np.maximum(0.0, nbud + 0.55 * K * (tgt - got))
    if verbose:
        print("      best flank rms %.2f %% (over %d live bins)"
              % (best, int(live.sum())))
    # 5) rear-quarter rosettes LAST, so the filler cannot overdraw them
    #    (extrapolated target -- folk_door.md measures no rear cream)
    cs = bisect(lambda m: frac(render(bops + rosettes_of(m)), pen,
                               Xc, Zc)[1] < REAR_CREAM, 0.10, 4.0, 8)
    bops = bops + rosettes_of(cs)
    if verbose:
        print("      rear rosette scale %.3f" % cs)
    return bops, render(bops)


def make(path=None, side="show", seed=196301, variant=0, verbose=True):
    check_mapping_contract()
    if verbose:
        print("  [%s] cab door -- folk_door.md sec.3/sec.5" % side)
    dops = solve_door(side, seed, variant, verbose)
    if verbose:
        print("  [%s] flank -- folk_door.md sec.11 corrected scan" % side)
    ops, lab = solve_flank(side, seed, variant, dops, verbose)
    rgba, alpha, W = resolve(lab)
    p = path or os.path.join(TEXDIR, SIDES[side][2])
    Image.fromarray(rgba, "RGBA").save(p)
    if verbose:
        print("  [%s] %d ops -> %s" % (side, len(ops), p))
    return dict(path=p, ops=ops, lab=lab, alpha=alpha, W=W, side=side)


def class_weights(lab):
    """area-exact per-class coverage of every output texel (SS x SS block)."""
    out = {}
    a = np.asarray(lab, dtype=np.uint8)
    for c in (GOLD, GOLDS, CREAM, DARK):
        out[c] = ((a == c).reshape(N, SS, N, SS)
                  .sum(axis=(1, 3), dtype=np.int32) / float(SS * SS))
    return out


def resolve(lab):
    """label raster -> (sRGB uint8, alpha, per-class texel weights)."""
    W = class_weights(lab)
    alpha = sum(W.values())
    acc = np.zeros((N, N, 3), np.float32)
    for c, col in PAL.items():
        acc += W[c][..., None] * col.astype(np.float32)
    rgb = np.where(alpha[..., None] > 1e-6,
                   acc / np.maximum(alpha, 1e-6)[..., None], 0.0)
    # bleed ink colour into the transparent ground so bilinear filtering in the
    # shader cannot pull a dark fringe out of empty texels
    if ndimage is not None:
        m = (alpha > 1e-6).astype(np.float32)
        for _ in range(5):
            w = ndimage.uniform_filter(m, 9)
            for k in range(3):
                sm = ndimage.uniform_filter(rgb[..., k] * m, 9)
                rgb[..., k] = np.where(m > 0.5, rgb[..., k],
                                       sm / np.maximum(w, 1e-6))
            m = (w > 1e-6).astype(np.float32)
    else:
        rgb = np.where(alpha[..., None] > 1e-6, rgb,
                       PAL[GOLD].astype(np.float32))
    out = np.zeros((N, N, 4), np.uint8)
    out[..., :3] = np.clip(lin_to_srgb(rgb) * 255.0 + 0.5, 0, 255).astype(np.uint8)
    out[..., 3] = np.clip(alpha * 255.0 + 0.5, 0, 255).astype(np.uint8)
    return out, alpha, W


def door_view(side):
    """sub-texel bbox of the cab-door painted panel for this side."""
    pen = Pen(side)
    xs = np.linspace(DOOR_X0, DOOR_X1, 9)
    pts = [pen.px(x, panel_top(x)) for x in xs] + \
          [pen.px(x, panel_bot(x)) for x in xs]
    c0 = int(math.floor(min(p[0] for p in pts))) - 2
    c1 = int(math.ceil(max(p[0] for p in pts))) + 2
    r0 = int(math.floor(min(p[1] for p in pts))) - 2
    r1 = int(math.ceil(max(p[1] for p in pts))) + 2
    return c0, r0, c1 - c0, r1 - r0


# ===========================================================================
# 11.  REPORT
# ===========================================================================
def contrast(res):
    """Composite the tile over t1_mats.RED in LINEAR light -- exactly what the
    Mix node in body_paint does -- and measure Rec.709 luma on sRGB codes."""
    a = np.asarray(Image.open(res["path"])).astype(np.float64) / 255.0
    lin = srgb_to_lin(a[..., :3])
    al = a[..., 3:4]
    comp = lin * al + RED_LIN[None, None, :] * (1.0 - al)
    luma = (lin_to_srgb(comp) * 255.0) @ LUMA_W
    W, alpha = res["W"], res["alpha"]
    out = {}
    for nm, sel in (("gold core", W[GOLD] >= 0.995),
                    ("gold whole class", (W[GOLD] + W[GOLDS]) > 0.5),
                    ("cream core", W[CREAM] >= 0.995),
                    ("dark core", W[DARK] >= 0.995)):
        out[nm] = (float(np.median(luma[sel])) if sel.sum() else float("nan"),
                   int(sel.sum()))
    out["red"] = (RED_LUMA, int((alpha < 0.002).sum()))
    return out


def contrast_through_shader(res, w_art=0.30, sat=2.45, val=0.94):
    """What the tile would read as THROUGH THE CURRENT UNPATCHED body_paint:
    Hue/Saturation(Sat 2.45, Val 0.94) on the colour, then Mix over RED at
    alpha * W_ART.  This is the measurement that shows the contrast target is
    unreachable without the t1_mats.py changes listed at the bottom of this
    file -- reported next to the corrected path, not instead of it."""
    a = np.asarray(Image.open(res["path"])).astype(np.float64) / 255.0
    lin = srgb_to_lin(a[..., :3])
    mx = lin.max(axis=2)
    mn = lin.min(axis=2)
    v = mx
    sv = np.where(mx > 1e-9, (mx - mn) / np.maximum(mx, 1e-9), 0.0)
    # hue, then rebuild with S' = clip(S*sat), V' = V*val   (Blender HSV node)
    with np.errstate(invalid="ignore", divide="ignore"):
        d = np.maximum(mx - mn, 1e-12)
        r, g, b = lin[..., 0], lin[..., 1], lin[..., 2]
        h = np.where(mx == r, (g - b) / d % 6,
                     np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) / 6.0
    h = np.where(sv < 1e-9, 0.0, h)
    S = np.clip(sv * sat, 0, 1)
    V = np.clip(v * val, 0, 1)
    i = np.floor(h * 6.0) % 6
    f = h * 6.0 - np.floor(h * 6.0)
    pp, qq, tt = V * (1 - S), V * (1 - S * f), V * (1 - S * (1 - f))
    out = np.zeros_like(lin)
    for k, (rr, gg, bb) in enumerate(((V, tt, pp), (qq, V, pp), (pp, V, tt),
                                      (pp, qq, V), (tt, pp, V), (V, pp, qq))):
        m = (i == k)
        out[..., 0] = np.where(m, rr, out[..., 0])
        out[..., 1] = np.where(m, gg, out[..., 1])
        out[..., 2] = np.where(m, bb, out[..., 2])
    al = a[..., 3:4] * w_art
    comp = out * al + RED_LIN[None, None, :] * (1 - al)
    luma = (lin_to_srgb(comp) * 255.0) @ LUMA_W
    W = res["W"]
    res2 = {}
    for nm, sel in (("gold core", W[GOLD] >= 0.995),
                    ("cream core", W[CREAM] >= 0.995),
                    ("dark core", W[DARK] >= 0.995)):
        res2[nm] = float(np.median(luma[sel])) if sel.sum() else float("nan")
    return res2


def demirror_check(res_show, res_off):
    """Audit materials-14 asks one specific question: is the off flank the show
    flank mirrored?  Sample BOTH tiles the way the body samples them, on the
    same body grid, and correlate over every shift and both parities.

    Two correlations are reported.  The RAW one is dominated by the density
    envelope, which the two sides are *supposed* to share -- both flanks must
    obey the same measured coverage-vs-x.  The WHITENED one subtracts each
    map's own local density (a 0.30 m boxcar along the body) and so answers the
    question that actually matters: is it the same DRAWING?"""
    xs = np.linspace(FLANK_X0, FLANK_X1, 1024)
    fs = np.linspace(0.01, 0.99, 192)
    X, F = np.meshgrid(xs, fs)
    T = np.array([full_band(x)[0] for x in xs])[None, :]
    B = np.array([full_band(x)[1] for x in xs])[None, :]
    Z = B + (T - B) * F

    def bodymap(lab, side):
        return (look(lab, Pen(side), X, Z) != NONE).astype(np.float32)

    def whiten(M):
        k = max(3, int(0.30 / (xs[1] - xs[0])) | 1)          # 0.30 m boxcar
        if ndimage is None:
            return M - M.mean()
        return M - ndimage.uniform_filter1d(M, k, axis=1, mode="wrap")

    A = bodymap(res_show["lab"], "show")
    Bo = bodymap(res_off["lab"], "off")
    C = bodymap(res_show["lab"], "off")      # what the UNPATCHED shader does

    def ncc(P, Q):
        p, q = P - P.mean(), Q - Q.mean()
        n = float(np.sqrt((p * p).sum() * (q * q).sum()))
        if not n:
            return 0.0
        r = np.fft.irfft2(np.fft.rfft2(p) * np.conj(np.fft.rfft2(q)), p.shape)
        return float(r.max() / n)

    wA, wB, wC = whiten(A), whiten(Bo), whiten(C)
    return {
        "TWO tiles  raw   unflipped / mirrored":
            (round(ncc(A, Bo), 4), round(ncc(A, Bo[:, ::-1]), 4)),
        "TWO tiles  whitened  unflipped / mirrored":
            (round(ncc(wA, wB), 4), round(ncc(wA, wB[:, ::-1]), 4)),
        "ONE tile   raw   unflipped / mirrored":
            (round(ncc(A, C), 4), round(ncc(A, C[:, ::-1]), 4)),
        "ONE tile   whitened  unflipped / mirrored":
            (round(ncc(wA, wC), 4), round(ncc(wA, wC[:, ::-1]), 4)),
        "ink coverage over the flank, show / off (%)":
            (round(float(100 * A.mean()), 2), round(float(100 * Bo.mean()), 2)),
    }


def report(out):
    for side in ("show", "off"):
        r = out[side]
        lab, pen = r["lab"], Pen(side)
        X, Z, UD, PV = door_grid()
        g, c, d = classify(look(lab, pen, X, Z))
        ub = np.clip((UD * 20).astype(int), 0, 19)
        vb = np.clip((PV * 10).astype(int), 0, 9)
        uu = np.array([100.0 * g[ub == i].mean() for i in range(20)])
        vv = np.array([100.0 * g[vb == j].mean() for j in range(10)])
        gg, cc, dd = 100 * g.mean(), 100 * c.mean(), 100 * d.mean()

        print("\n  =================== %s FLANK ===================" % side.upper())
        print("  CAB DOOR PANEL                     target   achieved")
        for nm, t, a in (("gold / painted panel   %", DOOR_GOLD, gg),
                         ("cream rosettes         %", DOOR_CREAM, cc),
                         ("dark-brown ink         %", DOOR_DARK, dd),
                         ("red ground             %", 66.54,
                          100 - gg - cc - dd)):
            print("    %-30s %8.2f %10.2f" % (nm, t, a))
        print("    gold across the door, 20 bins, hinge -> latch")
        print("      target " + " ".join("%4.1f" % v for v in DOOR_U_PROFILE))
        print("      got    " + " ".join("%4.1f" % v for v in uu))
        print("      u<0.25  target 42.1  got %5.1f      "
              "u>0.75  target  5.1  got %5.1f       "
              "rms %.1f, r = %.2f"
              % (uu[:5].mean(), uu[15:].mean(),
                 float(np.sqrt(((uu - DOOR_U_PROFILE) ** 2).mean())),
                 float(np.corrcoef(uu, DOOR_U_PROFILE)[0, 1])))
        print("    gold down the panel, 10 bins, belt -> bottom")
        print("      target " + " ".join("%4.1f" % v for v in DOOR_V_PROFILE))
        print("      got    " + " ".join("%4.1f" % v for v in vv))
        print("      rms %.1f, r = %.2f"
              % (float(np.sqrt(((vv - DOOR_V_PROFILE) ** 2).mean())),
                 float(np.corrcoef(vv, DOOR_V_PROFILE)[0, 1])))

        Xn, Zn = band_grid(1.870, 2.020, 60, 160, nose_band)
        gn, cn, dn = frac(lab, pen, Xn, Zn)
        print("  LOWER NOSE (sec.10)                target   achieved")
        print("    %-30s %8.2f %10.2f" % ("gold                   %",
                                          NOSE_GOLD, gn))
        print("    %-30s %8.2f %10.2f" % ("dark-brown ink         %",
                                          NOSE_DARK, dn))

        print("  FLANK SCAN, sec.11 quantity gold / (red + gold)")
        print("    %8s %8s %8s   %s" % ("X", "target", "got", "status"))
        for xc, tv, rel in FLANK_SCAN:
            Xb, Zb = band_grid(xc - 0.095, xc + 0.095, 40, 200, full_band)
            gb, cb, db = frac(lab, pen, Xb, Zb)
            note = {True: "measured", False: "arch-affected: lower bound",
                    None: "arch artefact -- discarded"}[rel]
            print("    %8.3f %8.2f %8.2f   %s"
                  % (xc, tv, 100.0 * gb / max(100.0 - cb - db, 1e-6), note))
        Xr, Zr = band_grid(-2.000, -1.700, 60, 200, full_band)
        gr, cr, dr = frac(lab, pen, Xr, Zr)
        print("    rear quarter: dark %.2f %% (extrapolated target %.1f), "
              "cream %.2f %% (extrapolated target %.1f)"
              % (dr, REAR_DARK, cr, REAR_CREAM))

        print("  CONTRAST over t1_mats.RED (adjacent-red luma %.2f)" % RED_LUMA)
        ct = contrast(r)
        for nm, t in (("gold core", 2.048), ("gold whole class", 1.840),
                      ("cream core", 2.348), ("dark core", 0.490)):
            lu, n = ct[nm]
            print("    %-20s target x%.3f    got %6.2f = x%.3f   (n = %d)"
                  % (nm, t, lu, lu / RED_LUMA, n))
        cs2 = contrast_through_shader(r)
        print("  the same tile THROUGH THE UNPATCHED t1_mats.body_paint "
              "(W_ART 0.30, HueSat 2.45/0.94):")
        for nm, t in (("gold core", 2.048), ("cream core", 2.348),
                      ("dark core", 0.490)):
            print("    %-20s target x%.3f    got %6.2f = x%.3f   <- BLOCKED"
                  % (nm, t, cs2[nm], cs2[nm] / RED_LUMA))

    print("\n  ============ materials-14: are the flanks the same art? ========")
    for k, v in demirror_check(out["show"], out["off"]).items():
        print("    %-42s %s" % (k, v if isinstance(v, tuple) else "%.4f" % v))


def main():
    print("folk_gen rev10  --  built against measure/folk_door.md")
    print("  tile %d px, ss %d, 1 texel = %.3f mm on the body, period %.3f m"
          % (N, SS, 1000.0 / (N * MAP_SCALE), 1.0 / MAP_SCALE))
    print("  palette solved for the sec.7 contrast ratios against t1_mats.RED "
          "(luma %.2f):" % RED_LUMA)
    for k, nm in ((GOLD, "gold"), (GOLDS, "gold shade"), (CREAM, "cream"),
                  (DARK, "dark")):
        s = tuple(int(v) for v in np.round(lin_to_srgb(PAL[k]) * 255))
        print("      %-11s sRGB %-16s luma %6.2f   x red = %.3f"
              % (nm, s, code_luma(PAL[k]), code_luma(PAL[k]) / RED_LUMA))
    out = {}
    for side, seed, variant in (("show", 196301, 0), ("off", 771963, 1)):
        out[side] = make(side=side, seed=seed, variant=variant)
    report(out)
    return out


# ===========================================================================
# 12.  WHAT MUST CHANGE IN t1_mats.py  (not edited here -- other work is live
#      in that file).  Every line number is against the tree this was written
#      on.  Without (a) and (b) the art CANNOT reach the measured contrast: at
#      W_ART 0.30 the densest possible gold composites to x2.15 the red only if
#      the ink is pure white, and the Hue/Saturation node clamps every class to
#      full saturation, which turns the cream rosettes orange.
#
#   (a) t1_mats.py:175   W_ART = float(os.environ.get("T1_W_ART", 0.30))
#                     -> W_ART = float(os.environ.get("T1_W_ART", 1.00))
#       The folk art is painted, not glazed.  0.30 is a 30 % opacity ceiling.
#
#   (b) t1_mats.py:893 and :894  the Hue/Saturation node on the swirl colour
#           hs.inputs["Saturation"].default_value = 2.45   -> 1.0
#           hs.inputs["Value"].default_value      = 0.94   -> 1.0
#       2.45 clamps S to 1.0 for gold, cream AND dark: the cream rosettes
#       (198,164,105) come out fully saturated orange and the dark brown loses
#       its blue channel.  The tile is now authored at the correct colours.
#
#   (c) t1_mats.py:846-878  the density mask (fx, fx2, bz/belt/beltw, clut,
#       thr, keep) is now REDUNDANT and must be bypassed: at line 879 replace
#           amask = _math(nt, 'MULTIPLY', swirl.outputs["Alpha"], keep, ...)
#       with a direct link from swirl.outputs["Alpha"].  Density-vs-x, the
#       42 %->5 % ramp across the door, the 52 mm bare belt margin and the
#       per-class split are all baked into the tile now, measured in body
#       coordinates.  Leaving the mask in place multiplies the measured
#       profile by a second, wrong one.
#       If the mask is kept instead, its corrected numbers are:
#           fx  (rear lobe)   0.05 at X -0.30  ->  1.00 at X -2.05 stays, but
#                             the plateau is 20 % from X -0.97 to -1.72 and the
#                             rise to 40 % happens only aft of -1.75;
#           fx2 (door lobe)   inputs[1] 0.55 -> 0.90, inputs[2] 1.75 -> 1.83,
#                             inputs[3] 0.05 -> 0.03, inputs[4] 0.60 -> 1.00.
#           The old fx2 topped out at 0.60 of the tile alpha over a lobe that
#           began at X +0.55 -- i.e. it put its maximum on the flank BEHIND the
#           door and never reached the door's own coverage.
#
#   (d) materials-14, the de-mirroring.  Blender's BOX projection samples the
#       two Y faces at u and 1-u, so one tile can only ever give two mirrored
#       flanks.  Add a per-side selector (sign of Position.Y is unambiguous;
#       the normal is not, on a crowned flank):
#           sep.Y -> Math GREATER_THAN 0.0            -> `sideY`
#           swirl_b = _img(nt, "swirl_b.png", ...)     same Vector as swirl
#           MixRGB(sideY, swirl_b.Color, swirl.Color) -> hs.Color
#           Math MIX / Mix float(sideY, swirl_b.Alpha, swirl.Alpha) -> amask
#       and make the vector explicit rather than relying on the box flip:
#           u = 0.815 - 0.26*X on +Y, u = 0.185 + 0.26*X on -Y, v = 0.263+0.26*Z
#       (SeparateXYZ -> Math -> CombineXYZ -> projection='FLAT').  That is the
#       convention the two tiles here are authored for.  Also drop
#       projection_blend 0.32 -> 0.10 (t1_mats.py:826): at 0.32 the nose corner
#       cross-fades two unrelated regions of the tile.
#
#   (e) OPTIONAL, removes the nose/tail texture-wrap collision documented in
#       section 8: t1_mats.py:823 Scale 0.2600 -> 0.2280 and :815 Location
#       0.185 -> 0.500 (x only).  Period becomes 4.386 m > the 4.01 m flank, so
#       the lower nose and the rear-most quarter stop sharing texels.  MAP_LOC
#       and MAP_SCALE at the top of this file must be changed to match and the
#       generator re-run -- it self-checks and warns if they diverge.
# ===========================================================================

if __name__ == "__main__":
    main()
