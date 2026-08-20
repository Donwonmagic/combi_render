"""
cal_gen.py -- the "100% Calidad" rear-corner decal, reproduced from the photo.

rev 8 drew a flat 24-point red star with no gradient, no bunting and type set
in a system italic. SPEC sec.10.10 lists this element as NOT STARTED, and the
brief for this pass names what is actually there. Source crop ref_side.jpg
(735,295)-(860,390), read at 8-12x.

WHAT THE PHOTOGRAPH SHOWS, MEASURED
  * one warm blob on the cream rear panel, abs x 736-835, y 306-379
    (100 x 74 px, aspect 1.35). That blob is starburst AND bunting together;
    the bunting bars sit across its top, so they share one decal panel.
  * the burst is a SPIKY sunburst -- many narrow sharp points of uneven
    length, not a regular 24-point star.
  * it carries a gradient. Sampled in bands along the upper-left -> lower-right
    axis: (240,132,130) at the red end, (245,180,148) at the orange/yellow end.
    The photograph is over-exposed here (the cream panel around it reads
    (236,229,227), i.e. nearly blown), so those are lifted; the paint is
    reconstructed saturated and the render's exposure brings it back.
  * white bold italic type, two lines, "100%" over "Calidad", set at about
    -20 degrees -- measured from the "1" at lower-left to the "%" at upper
    right, atan2(-190, 530) = -19.7 deg. Nine enclosed white counters survive
    segmentation inside the burst, largest 251 px.
  * TWO bunting bars above the type, each a thin bar with triangular pennants
    hanging BELOW it, both running roughly parallel to the type angle.
  * a small pink star to the left (SPEC sec.3).

PLACEMENT -- and why it moved
The decal's position was checked against a datum that does not depend on any
pixel-to-metre mapping: its fraction of the solid rear-corner panel. In the
photograph the panel runs x 698 (aft edge of bay 3) to x 902 (tail); the decal
occupies 18.6% to 67.2% of that span. build.py placed it at 37.3% to 84.7%.
That is 198 mm too far aft, and the ratio argument is immune to the
perspective foreshortening that makes a single linear x->X scale wrong here
(the panel measures 194.8 px/m against 211.5 px/m at mid-body).

    python3 cal_gen.py   -> tex/calidad.png
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, "tex")

AR = 1.355                       # measured 100 x 74 px
W = 2400
H = int(round(W / AR))           # 1771
SS = 3
w, h = W * SS, H * SS

# paint, reconstructed saturated -- see the exposure note above
RED = (214, 46, 30)
ORANGE = (238, 122, 22)
YELLOW = (247, 189, 46)
WHITE = (252, 250, 246)
PINK = (232, 96, 122)
BUNT = (198, 40, 36)

ANG = math.radians(-19.7)        # measured type / bunting angle

# ------------------------------------------------------- rev 46, W1, SPEC 10.118
# THE BURST'S CENTRE, PROMOTED TO A CONSTANT, AND THE TYPE EXPRESSED AGAINST IT.
#
# The owner reported "the 100% calidad off center" and he is right.  It is NOT
# the defect rev 44 closed: that one was the decal PANEL'S PLACEMENT ON THE
# VEHICLE (Report 7, 0.180 of texture width).  This is the TYPE'S PLACEMENT
# INSIDE THE DECAL, which nobody had ever measured.  Both are true and they are
# different things.
#
# Measured on this generator's own output, before the block is rotated: the
# type's centroid sat at (0.3735, 0.6309) of the canvas while starburst()'s
# centre is (0.5050, 0.5750).  The block was 0.1315 w LEFT and 0.0559 h BELOW
# the burst it is supposed to sit on -- and it showed, with "100%" hanging off
# the burst onto bare cream and "Calidad" running off the panel's bottom edge.
#
# TYPE_SHIFT is EXACTLY that measured miss (SPEC 10.25: a constant tuned against
# another constant is expressed in terms of it).  It is not a re-tuned pair of
# absolutes -- re-run the pre-rotation centroid measurement after any glyph
# change and it re-derives.  The two lines keep their relative offset; only the
# block moves, which is what "off center" means.
#
# AND THE ROTATION CENTRE MOVES TO THE BURST'S CENTRE.  It was (0.500, 0.600) --
# near the burst's centre but not equal to it, so the -19.7 deg rotation swung
# the block off centre again by a further (+0.0148, +0.0558) even when the
# layout was right.  Rotating about the point the block is centred ON makes the
# centring EXACT and independent of ANG: a rotation fixes its own centre.
BURST_CX, BURST_CY = 0.505, 0.575
TYPE_PRE_CENTROID = (0.3735, 0.6309)     # watched print, rev 46, pre-rotation
TYPE_SHIFT = (BURST_CX - TYPE_PRE_CENTROID[0],
              BURST_CY - TYPE_PRE_CENTROID[1])      # (+0.1315, -0.0559)


def rot(px, py, cx, cy, a):
    s, c = math.sin(a), math.cos(a)
    dx, dy = px - cx, py - cy
    return cx + dx * c - dy * s, cy + dx * s + dy * c


# ------------------------------------------------------------------ starburst
def starburst(d):
    """
    Spiky sunburst: narrow points of uneven length. The unevenness is the
    reason this does not read as a rev-8 regular star -- it is a hand-painted
    burst, so the tips wander. The sequence is fixed, not random, so the file
    is reproducible.
    """
    cx, cy = w * BURST_CX, h * BURST_CY
    RO, RI = h * 0.435, h * 0.255
    N = 27
    jitter = [0.94, 1.06, 0.88, 1.11, 0.97, 1.04, 0.91, 1.08, 1.00, 0.93,
              1.09, 0.96, 1.03, 0.89, 1.07, 0.99, 1.05, 0.92, 1.10, 0.95,
              1.02, 0.90, 1.06, 0.98, 1.04, 0.93, 1.08]
    pts = []
    for i in range(N * 2):
        a = math.pi * i / N - math.pi / 2 + math.pi / (2 * N)
        if i % 2 == 0:
            r = RO * jitter[(i // 2) % N]
        else:
            r = RI * (0.94 + 0.12 * jitter[(i // 2) % N])
        pts.append((cx + r * math.cos(a) * 1.30, cy + r * math.sin(a)))
    d.polygon(pts, fill=RED + (255,))
    return cx, cy, RO


def gradient(img, cx, cy):
    """
    Red-orange -> orange/yellow across the upper-left -> lower-right axis, the
    direction the sampled bands run in the photograph.
    """
    a = np.array(img).astype(np.float32)
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    t = ((xx - cx) * 0.62 + (yy - cy) * 0.78) / (1.35 * h)
    # ------------------------------------------------- rev 45, SPEC 10.112
    # THE BIAS WAS 0.42 AND IT THREW THE DECLARED COLOUR AWAY.
    #
    # `t` is zero AT THE BURST'S OWN CENTRE by construction -- (cx, cy) is
    # starburst()'s centre and the axis term is measured from it.  A bias of
    # 0.42 therefore started the ramp 42 % of the way along, so the core
    # evaluated to RED*0.16 + ORANGE*0.84 = (234, 110, 23).  Measured off
    # tex/calidad.png as shipped: core (237.0, 120.3, 22.0), G/R 0.508.
    # starburst() fills the whole polygon with RED = (214, 46, 30), G/R 0.215,
    # nine lines above -- AND NOTHING IN THE FINISHED TEXTURE IS THAT COLOUR
    # except the extreme upper-left corner where the clip bottoms out.  The
    # decal renders PEACH where the photograph is RED, which is what the owner
    # has reported twice.
    #
    # THE BIAS IS ZERO.  That is not a tuned number: it is the statement that
    # the gradient DEPARTS from the burst's declared colour going outward,
    # rather than starting two-thirds of the way to orange.  RED at the core,
    # ORANGE through the middle distance, YELLOW at the lower-right tips --
    # which is the direction the docstring's sampled bands actually run.
    #
    # Cross-check that needs no photograph: cal_gen's RED (214,46,30) has
    # G/R 0.215 and t1_mats' body RED sRGB(196,49,36) has G/R 0.250.  The
    # burst and the coachwork are the same red family, and at bias 0 the
    # rendered core lands there instead of 0.5.
    #
    # rev 44 ruled out two other causes BY TEST and both stay ruled out:
    # WEAR['calidad'] is not the lever (re-rendered at 0.22, core bit-
    # identical) and the material adds no cream.
    t = np.clip(t * 1.5 + 0.00, 0, 1)
    stops = np.array([RED, ORANGE, YELLOW], np.float32)
    k = t * 2.0
    i0 = np.clip(np.floor(k), 0, 1).astype(int)
    f = (k - i0)[..., None]
    col = stops[i0] * (1 - f) + stops[i0 + 1] * f
    m = a[..., 3:4] / 255.0
    a[..., :3] = a[..., :3] * (1 - m) + col * m
    return Image.fromarray(a.astype(np.uint8))


# -------------------------------------------------------------------- lettering
# Built on an L-mask so counters can be punched out. Drawing the type straight
# into the RGBA image left the 0s, the %, and a/o/d as solid slabs -- the
# counters are what make it read as type at hero scale.
class TypeMask:
    def __init__(self, wd, ht):
        self.m = Image.new("L", (wd, ht), 0)
        self.d = ImageDraw.Draw(self.m)

    def on(self, pts):
        self.d.polygon(pts, fill=255)

    def off(self, pts):
        self.d.polygon(pts, fill=0)

    def ell_on(self, box):
        self.d.ellipse(box, fill=255)

    def ell_off(self, box):
        self.d.ellipse(box, fill=0)


SL = 0.24                                  # italic slope


def _P(x, y, s, px, py):
    return (x + px * s + (1.0 - py) * SL * s, y + py * s)


def _bar(t, x, y, s, x0, x1, y0=0.0, y1=1.0, cut=False):
    q = [_P(x, y, s, x0, y0), _P(x, y, s, x1, y0),
         _P(x, y, s, x1, y1), _P(x, y, s, x0, y1)]
    (t.off if cut else t.on)(q)


def _ring(t, x, y, s, x0, x1, y0, y1, tw):
    """A bold rounded rectangle with its counter punched out."""
    t.on([_P(x, y, s, x0 + 0.05, y0), _P(x, y, s, x1 - 0.05, y0),
          _P(x, y, s, x1, y0 + 0.12), _P(x, y, s, x1, y1 - 0.12),
          _P(x, y, s, x1 - 0.05, y1), _P(x, y, s, x0 + 0.05, y1),
          _P(x, y, s, x0, y1 - 0.12), _P(x, y, s, x0, y0 + 0.12)])
    t.off([_P(x, y, s, x0 + tw + 0.03, y0 + tw), _P(x, y, s, x1 - tw - 0.03, y0 + tw),
           _P(x, y, s, x1 - tw, y0 + tw + 0.10), _P(x, y, s, x1 - tw, y1 - tw - 0.10),
           _P(x, y, s, x1 - tw - 0.03, y1 - tw), _P(x, y, s, x0 + tw + 0.03, y1 - tw),
           _P(x, y, s, x0 + tw, y1 - tw - 0.10), _P(x, y, s, x0 + tw, y0 + tw + 0.10)])


def glyph_100(t, x, y, s):
    """'100%' -- bold condensed italic, counters punched."""
    # 1: stem plus the angled flag
    _bar(t, x, y, s, 0.13, 0.32)
    t.on([_P(x, y, s, -0.04, 0.22), _P(x, y, s, 0.13, 0.02),
          _P(x, y, s, 0.13, 0.24), _P(x, y, s, 0.01, 0.36)])
    _ring(t, x, y, s, 0.42, 0.78, 0.02, 1.00, 0.13)
    _ring(t, x, y, s, 0.86, 1.22, 0.02, 1.00, 0.13)
    # %: two rings and a slash
    for ox, oy in ((1.34, 0.02), (1.62, 0.56)):
        _ring(t, x, y, s, ox, ox + 0.26, oy, oy + 0.42, 0.085)
    t.on([_P(x, y, s, 1.70, 0.00), _P(x, y, s, 1.88, 0.00),
          _P(x, y, s, 1.50, 1.02), _P(x, y, s, 1.32, 1.02)])


def glyph_calidad(t, x, y, s):
    """'Calidad' -- same idiom, x-height letters with ascenders on l and d."""
    ox = 0.0
    for ch in "Calidad":
        if ch == "C":
            t.on([_P(x, y, s, ox + 0.36, 0.02), _P(x, y, s, ox + 0.12, 0.16),
                  _P(x, y, s, ox + 0.04, 0.44), _P(x, y, s, ox + 0.04, 0.62),
                  _P(x, y, s, ox + 0.12, 0.88), _P(x, y, s, ox + 0.36, 1.02),
                  _P(x, y, s, ox + 0.36, 0.80), _P(x, y, s, ox + 0.22, 0.70),
                  _P(x, y, s, ox + 0.22, 0.34), _P(x, y, s, ox + 0.36, 0.24)])
            ox += 0.46
        elif ch == "a":
            _ring(t, x, y, s, ox + 0.02, ox + 0.34, 0.34, 1.02, 0.115)
            _bar(t, x, y, s, ox + 0.24, ox + 0.36, 0.34, 1.02)
            ox += 0.44
        elif ch == "l":
            _bar(t, x, y, s, ox + 0.02, ox + 0.16, -0.26, 1.02)
            ox += 0.26
        elif ch == "i":
            _bar(t, x, y, s, ox + 0.02, ox + 0.16, 0.34, 1.02)
            _bar(t, x, y, s, ox + 0.03, ox + 0.17, 0.06, 0.24)
            ox += 0.26
        elif ch == "d":
            _ring(t, x, y, s, ox + 0.02, ox + 0.34, 0.34, 1.02, 0.115)
            _bar(t, x, y, s, ox + 0.30, ox + 0.44, -0.26, 1.02)
            ox += 0.54
    return ox


def bunting(d, y0, x0, x1, n, drop, fill):
    """A bar with triangular pennants hanging below it, at the measured angle."""
    tan = math.tan(-ANG)
    th = h * 0.013
    d.polygon([(x0, y0), (x1, y0 - (x1 - x0) * tan),
               (x1, y0 - (x1 - x0) * tan + th), (x0, y0 + th)], fill=fill)
    for i in range(n):
        ax = x0 + (x1 - x0) * (i + 0.10) / n
        bx = x0 + (x1 - x0) * (i + 0.80) / n
        ay = y0 - (ax - x0) * tan + th
        by = y0 - (bx - x0) * tan + th
        d.polygon([(ax, ay), (bx, by), ((ax + bx) / 2, (ay + by) / 2 + drop)],
                  fill=fill)


def main():
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy, RO = starburst(d)
    img = gradient(img, cx, cy)
    d = ImageDraw.Draw(img)

    # small pink star to the left (SPEC sec.3)
    sx, sy, sr = w * 0.075, h * 0.60, h * 0.085
    sp = []
    for i in range(10):
        a = math.pi * i / 5 - math.pi / 2
        r = sr if i % 2 == 0 else sr * 0.42
        sp.append((sx + r * math.cos(a), sy + r * math.sin(a)))
    d.polygon(sp, fill=PINK + (255,))

    # bunting: two bars across the top of the burst, pennants hanging below
    bunting(d, h * 0.150, w * 0.14, w * 0.90, 8, h * 0.058, BUNT + (255,))
    bunting(d, h * 0.290, w * 0.11, w * 0.88, 7, h * 0.055, BUNT + (255,))

    # type on its own mask so the counters punch through, then rotated as one
    # block so the two lines stay parallel at the measured -19.7 degrees
    t = TypeMask(w, h)
    sx, sy = TYPE_SHIFT
    glyph_100(t, w * (0.150 + sx), h * (0.395 + sy), h * 0.228)
    glyph_calidad(t, w * (0.180 + sx), h * (0.645 + sy), h * 0.196)
    lay = Image.merge("RGBA", (
        Image.new("L", (w, h), WHITE[0]), Image.new("L", (w, h), WHITE[1]),
        Image.new("L", (w, h), WHITE[2]), t.m))
    lay = lay.rotate(-math.degrees(ANG), resample=Image.BICUBIC,
                     center=(w * BURST_CX, h * BURST_CY))
    img = Image.alpha_composite(img, lay)

    # ------------------------------------------------- rev 46, W1: THE GUARD
    # Added in the SAME EDIT as the change it guards (SPEC 10.117 / rule 12).
    # A claim in prose is not a guard: this one MEASURES the shipped raster and
    # refuses to write a decal whose type has drifted off the burst.  It is the
    # check that did not exist for forty-five revisions, which is why "100%
    # calidad off center" survived every one of them.
    _ck = np.array(img).astype(float)
    _al = _ck[:, :, 3] / 255.0
    _wm = (_al > 0.5) & (_ck[:, :, 0] > 200) & (_ck[:, :, 1] > 195) & (_ck[:, :, 2] > 190)
    _ys, _xs = np.nonzero(_wm)
    _tc = (_xs.mean() / _ck.shape[1], _ys.mean() / _ck.shape[0])
    _off = (_tc[0] - BURST_CX, _tc[1] - BURST_CY)
    print("  guard: type centroid (%.4f, %.4f) vs burst centre (%.4f, %.4f) "
          "-> off (%+.4f, %+.4f)" % (_tc + (BURST_CX, BURST_CY) + _off))
    # 0.004 is ~10 px on the 2400-wide master: below the LANCZOS/BICUBIC
    # resampling floor, far under the 0.1167 miss this replaced.
    if abs(_off[0]) > 0.004 or abs(_off[1]) > 0.004:
        raise SystemExit(
            "cal_gen GUARD FAILED: the type is off the burst's centre by "
            "(%+.4f, %+.4f) of the decal, tolerance 0.004.  This is the defect "
            "the owner reported as \"100%% calidad off center\".  Re-derive "
            "TYPE_SHIFT from the pre-rotation centroid; do not widen the "
            "tolerance." % _off)

    img = img.resize((W, H), Image.LANCZOS)
    os.makedirs(TEX, exist_ok=True)
    img.save(os.path.join(TEX, "calidad.png"))
    Image.alpha_composite(Image.new("RGBA", (W, H), (238, 232, 220, 255)),
                          img).convert("RGB").save(
        os.path.join(TEX, "prev_calidad.png"))
    print("wrote tex/calidad.png %dx%d  AR %.3f (measured 1.355)"
          % (W, H, W / H))


if __name__ == "__main__":
    main()
