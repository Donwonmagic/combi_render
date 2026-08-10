"""
script_gen.py -- the "Senor Tacombi" flank script, drawn as explicit outlines.

WHY THIS REPLACES THE FONT APPROACH
rev 8 shipped a system script face (NothingYouCouldDo) with a stroked swash and
stroked spirals drawn on top. Donald rejected it by name: "That script i see on
the p9 hero is NOT it." SPEC sec.10.10 makes the standard explicit -- every
painted element must be REPRODUCED from the photograph, not approximated -- and
names "a system font with flourishes bolted on" as the failure mode.

So there is no font here. Every glyph is built from primitives whose control
points were read off ref_side.jpg at 6-14x magnification, in the coordinate
frame of that photograph.

THE COORDINATE FRAME
All geometry below is in MASK SPACE: the pixel grid of ref_side.jpg offset to
(X0, Y0) = (325, 486), y increasing downward. That is deliberate -- it means a
control point in this file can be compared directly against the photograph
without a change of basis, and the acceptance test is a straight overlay.
Measured ink bounding box of the real script in this frame:

    x 5 -> 276, y 4 -> 103   (271 x 99 px, aspect 2.737)

WHAT WAS MEASURED, AND WHERE IT CAME FROM
  * ink is neutral silver, not white and not gold: median RGB (127,122,125),
    saturation 0.080, over a ground of (129,21,14).
  * the T's stem occupies x 33-60 and drops to the lowest point of the whole
    lockup at y 103; its swash ribbon runs x 6-116, entering at a rolled left
    terminal whose eye is a measured hole at (14.9, 63.1), cresting near
    x 90, and rolling clockwise over itself above the 'c' at x 96-116.
  * three spiral counters, centres (72, 72) / (112, 62) / (149, 60) for a, c
    and o. The o's counter is the one closed hole the segmentation finds:
    x 141-161, y 49-73, area 224 px in a 21x25 box -- 43% fill, which is a
    groove, not a plain bowl.
  * m spans x 166-215; b's bowl x 218-250 with a tilted counter measured at
    x 236-247, y 33-51; i's dot is a tilted ellipse at x 248-263, y 16-31.
  * the baseline is not level. Letter feet measured at (75,88) (112,85)
    (149,82) (190,74) (235,70) (265,58): the word arcs upward to the right.

CONSTRUCTION
Glyphs are unions of variable-width strokes and solid blobs, minus counter
shapes. A spiral counter is a GROOVE subtracted from a solid bowl -- that is
what the photograph shows: silver outside, a red spiral channel wound inward,
a silver core left in the middle. Rasterised supersampled, then area-averaged
down, so the edges are clean at any output size.

    python3 script_gen.py            -> tex/senor.png
    python3 script_gen.py --compare  -> also writes the overlay against ref
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy.interpolate import CubicSpline

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, "tex")

# ---- the frame -------------------------------------------------------------
X0, Y0 = 325, 486                      # mask space origin in ref_side.jpg px
MW, MH = 290, 114                      # mask space extent
INK_BBOX = (5, 4, 276, 103)            # measured ink bbox, x0 y0 x1 y1

SS = 12                                # supersample factor
OUT_W = 4096                           # decal width; SPEC sec.5 wants 3K-4K


# --------------------------------------------------------------- path helpers
def bez(p0, p1, p2, p3, n=60):
    t = np.linspace(0, 1, n)[:, None]
    return ((1 - t) ** 3 * np.array(p0) + 3 * (1 - t) ** 2 * t * np.array(p1)
            + 3 * (1 - t) * t ** 2 * np.array(p2) + t ** 3 * np.array(p3))


def poly(*segs):
    """Concatenate bezier segments into one dense polyline."""
    out = [segs[0]]
    for s in segs[1:]:
        out.append(s[1:])
    return np.vstack(out)


def resample(pts, n=400):
    d = np.r_[0.0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]
    if d[-1] <= 0:
        return pts
    u = np.linspace(0, d[-1], n)
    return np.c_[np.interp(u, d, pts[:, 0]), np.interp(u, d, pts[:, 1])]


def widths(n, keys):
    """Piecewise-linear half-width profile. keys = [(t, w), ...] with t in 0..1."""
    t = np.array([k[0] for k in keys])
    w = np.array([k[1] for k in keys])
    return np.interp(np.linspace(0, 1, n), t, w)


def stroke_poly(pts, w):
    """Outline of a variable-width stroke: left side out, right side back."""
    pts = np.asarray(pts, float)
    d = np.gradient(pts, axis=0)
    L = np.hypot(d[:, 0], d[:, 1])
    L[L == 0] = 1.0
    nx, ny = -d[:, 1] / L, d[:, 0] / L
    left = pts + np.c_[nx, ny] * w[:, None]
    right = pts - np.c_[nx, ny] * w[:, None]
    return np.vstack([left, right[::-1]])


def spiral_pts(cx, cy, r0, r1, turns, phase=0.0, hand=1.0, n=400):
    t = np.linspace(0, 1, n)
    th = phase + hand * turns * 2 * np.pi * t
    r = r0 + (r1 - r0) * t
    return np.c_[cx + r * np.cos(th), cy + r * np.sin(th)]


def ellipse_pts(cx, cy, rx, ry, rot=0.0, n=180):
    t = np.linspace(0, 2 * np.pi, n)
    x, y = rx * np.cos(t), ry * np.sin(t)
    c, s = np.cos(rot), np.sin(rot)
    return np.c_[cx + x * c - y * s, cy + x * s + y * c]


# ------------------------------------------------------------------ rasteriser
class Canvas:
    def __init__(self):
        self.ink = Image.new("L", (MW * SS, MH * SS), 0)
        self.hole = Image.new("L", (MW * SS, MH * SS), 0)
        self.di = ImageDraw.Draw(self.ink)
        self.dh = ImageDraw.Draw(self.hole)

    def _fill(self, d, pts):
        d.polygon([(float(x) * SS, float(y) * SS) for x, y in pts], fill=255)

    def blob(self, pts):
        self._fill(self.di, pts)

    def cut(self, pts):
        self._fill(self.dh, pts)

    def stroke(self, pts, w, cut=False, caps=True):
        pts = resample(np.asarray(pts, float), 400)
        if np.isscalar(w):
            w = np.full(len(pts), float(w))
        else:
            w = np.asarray(w, float)
            if len(w) != len(pts):
                w = np.interp(np.linspace(0, 1, len(pts)),
                              np.linspace(0, 1, len(w)), w)
        d = self.dh if cut else self.di
        self._fill(d, stroke_poly(pts, w))
        if caps:
            for p, r in ((pts[0], w[0]), (pts[-1], w[-1])):
                d.ellipse([(p[0] - r) * SS, (p[1] - r) * SS,
                           (p[0] + r) * SS, (p[1] + r) * SS], fill=255)

    def alpha(self):
        a = np.array(self.ink, np.uint8).astype(np.float32)
        h = np.array(self.hole, np.uint8).astype(np.float32)
        m = np.clip(a - h, 0, 255)
        m = m.reshape(MH, SS, MW, SS).mean(axis=(1, 3))
        return m


# ---------------------------------------------------------------- the lockup
def baseline(x):
    """Feet measured at (75,88) (112,85) (149,82) (190,74) (235,70) (265,58)."""
    return np.polyval(BL, x)


BL = np.polyfit([75, 112, 149, 190, 235, 265],
                [88, 85, 82, 74, 70, 58], 2)


def draw_T(c):
    """
    Capital T: a broad stem, and a ribbon swash that enters from a rolled
    terminal at the far left, sweeps right beneath 'Senor', and rolls clockwise
    over itself above the 'c'.
    """
    # --- the swash ribbon -----------------------------------------------
    # Every point below is measured off ref_side.jpg by taking the longest
    # contiguous ink run in each column. The ribbon is an ARCH, not a rise:
    # centre y 42.2 at x 30, cresting at 36.2 near x 57, falling back to 41.5
    # by x 90. An earlier pass drew it climbing monotonically and was 10 px
    # high at the right end.
    #
    # Left terminal: a 0.80-turn spiral about (17, 59), radius 21.4 -> 11.7,
    # wrapping the eye the segmentation finds at (14.9, 63.1). Three ink runs
    # at x 16-20 -- outer arm, inner arm, and the return -- are what fix the
    # turn count.
    lead = spiral_pts(18.4, 60.6, 21.4, 11.7, 0.80, phase=-0.90, hand=-1.0,
                      n=200)[::-1]
    xs = [30.3, 38.0, 46.0, 57.0, 66.0, 74.0, 82.0, 90.0, 98.0, 105.0]
    ys = [44.0, 41.8, 40.0, 38.0, 39.8, 42.0, 42.8, 43.3, 42.2, 39.8]
    cs = CubicSpline(xs, ys)
    gx = np.linspace(xs[0], xs[-1], 220)
    body = np.c_[gx, cs(gx)]
    # the fold: the ribbon turns up at x~108, over at x~112, and the tip runs
    # back LEFT along y 17-21 to x 99 (measured as a separate run at x 98-108)
    fold = poly(
        bez((105.0, 39.8), (109.0, 36.8), (111.6, 32.8), (112.4, 28.2)),
        bez((112.4, 28.2), (113.0, 24.0), (110.8, 21.2), (106.8, 20.4)),
        bez((106.8, 20.4), (103.4, 19.8), (100.6, 20.2), (98.6, 21.0)),
    )
    path = np.vstack([lead, body[1:], fold[1:]])
    w = widths(400,
               [(0.00, 3.9), (0.06, 4.6), (0.14, 5.3), (0.26, 5.9),
                (0.34, 6.5), (0.46, 6.0), (0.58, 5.6), (0.70, 5.4),
                (0.80, 5.3), (0.88, 4.8), (0.93, 3.6), (0.97, 2.1),
                (1.00, 1.2)])
    c.stroke(path, w)

    # --- the stem -------------------------------------------------------
    stem = poly(
        bez((46.2, 34.0), (46.8, 49.0), (46.2, 64.0), (45.6, 80.0)),
        bez((45.6, 80.0), (45.2, 88.0), (45.8, 94.0), (47.8, 98.6)),
    )
    c.stroke(stem, widths(400, [(0.0, 9.6), (0.30, 8.6), (0.62, 7.9),
                                (0.86, 7.2), (1.0, 5.6)]))
    # the foot flares forward into a small wedge, measured x 33-62 at y 100-103
    c.blob(poly(
        bez((37.4, 94.4), (39.4, 98.8), (45.4, 100.4), (53.4, 100.0)),
        bez((53.4, 100.0), (59.4, 99.4), (61.4, 97.0), (60.0, 93.8)),
        bez((60.0, 93.8), (51.4, 92.2), (43.4, 92.2), (37.4, 94.4)),
    ))


def bowl(c, cx, cy, rx, ry, rot=0.0):
    c.blob(ellipse_pts(cx, cy, rx, ry, rot))


def groove(c, cx, cy, r0, r1, turns, phase, hand, w):
    """A spiral counter: a channel of ground colour wound into a solid bowl."""
    c.stroke(spiral_pts(cx, cy, r0, r1, turns, phase, hand, 420), w, cut=True)


def draw_a(c):
    # bowl x 55-92, foot y 88; spiral counter centred (72,72)
    bowl(c, 71.6, 76.4, 18.2, 18.0, rot=-0.10)
    groove(c, 71.6, 77.2, 2.8, 12.2, 1.15, phase=-0.30, hand=1.0,
           w=widths(420, [(0.0, 1.8), (0.5, 2.5), (1.0, 3.1)]))
    # the a's right stem, dropping to the baseline with a small exit
    c.stroke(poly(bez((89.0, 59.0), (91.6, 70.0), (91.6, 82.0), (90.2, 90.0)),
                  bez((90.2, 90.0), (89.6, 93.6), (91.0, 95.4), (94.4, 95.0))),
             widths(400, [(0.0, 5.4), (0.55, 5.0), (0.86, 3.9), (1.0, 2.4)]))


def draw_c(c):
    # bowl x 92-130, spiral counter centred (112,62)
    bowl(c, 114.0, 68.4, 18.6, 18.8, rot=-0.06)
    groove(c, 114.2, 67.8, 3.0, 12.8, 1.20, phase=-0.15, hand=1.0,
           w=widths(420, [(0.0, 1.9), (0.5, 2.7), (1.0, 3.3)]))
    # the c's aperture: a wedge opening to the upper right
    c.cut(poly(bez((127.6, 48.0), (132.4, 50.6), (134.0, 55.0), (132.6, 59.0)),
               bez((132.6, 59.0), (137.6, 56.4), (138.8, 45.0), (134.4, 43.4)),
               bez((134.4, 43.4), (130.8, 43.4), (128.4, 45.4), (127.6, 48.0))))


def draw_o(c):
    # the one measured closed counter: hole x 141-161, y 49-73, centre (149,60)
    bowl(c, 150.6, 63.4, 19.4, 19.8, rot=-0.05)
    groove(c, 151.2, 62.6, 2.6, 11.8, 1.18, phase=0.60, hand=1.0,
           w=widths(420, [(0.0, 1.9), (0.5, 2.6), (1.0, 3.2)]))


def draw_m(c):
    """Three stems, two arches, narrow slot counters with rounded tops."""
    top = 48.0
    for i, x in enumerate((172.0, 191.0, 210.0)):
        f = baseline(x) + 0.5
        c.stroke(poly(bez((x, top + 2 - i * 1.2), (x + 0.6, (top + f) / 2),
                          (x + 0.4, f - 6), (x + 1.0, f))),
                 widths(400, [(0.0, 3.8), (0.6, 3.6), (1.0, 3.4)]))
    for x0, x1, rise in ((172.0, 191.0, 9.5), (191.0, 210.0, 10.5)):
        c.stroke(poly(bez((x0 - 0.4, top + 4), (x0 + 3, top - rise + 3),
                          (x1 - 3, top - rise + 0.5), (x1 + 0.2, top + 1.5))),
                 widths(400, [(0.0, 3.8), (0.5, 4.3), (1.0, 3.9)]))
    c.stroke(poly(bez((211.0, 66.0), (213.0, 70.0), (216.0, 71.4), (219.0, 70.4))),
             widths(400, [(0.0, 4.0), (1.0, 2.2)]))


def draw_b(c):
    # bowl x 218-250; counter measured x 236-247, y 33-51 (tilted)
    bowl(c, 234.8, 52.4, 15.8, 17.6, rot=-0.30)
    c.cut(ellipse_pts(238.4, 47.0, 6.8, 10.2, rot=-0.42))
    # thin ascender with a small flag -- the high-contrast stroke of the lockup
    c.stroke(poly(bez((223.6, 43.0), (226.0, 33.4), (228.8, 24.6), (232.4, 17.6))),
             widths(400, [(0.0, 4.4), (0.35, 2.6), (0.72, 1.9), (1.0, 1.4)]))
    c.blob(poly(bez((232.4, 18.0), (236.0, 15.4), (239.2, 16.0), (239.8, 18.6)),
                bez((239.8, 18.6), (236.8, 19.8), (234.0, 20.6), (231.6, 20.8)),
                bez((231.6, 20.8), (231.0, 19.6), (231.4, 18.7), (232.4, 18.0))))


def draw_i(c):
    # stem, then the exit flourish sweeping up to the right
    c.stroke(poly(bez((252.0, 31.0), (253.6, 39.4), (254.4, 46.8), (256.6, 51.6)),
                  bez((256.6, 51.6), (260.0, 57.4), (266.0, 56.4), (269.6, 50.6)),
                  bez((269.6, 50.6), (272.6, 46.0), (274.0, 41.4), (274.4, 37.2))),
             widths(400, [(0.0, 4.8), (0.35, 4.6), (0.62, 3.6),
                          (0.84, 2.4), (1.0, 1.5)]))
    # the dot: a tilted ellipse, measured x 248-263, y 16-31
    c.blob(ellipse_pts(255.6, 23.4, 7.4, 4.0, rot=-0.52))


SENOR = [
    # "Senor", small, raised upper-left, sitting above the swash ribbon.
    # Measured extent x 12-100, y 2-27. Rounded, fat, on a shallow arc.
    ("S", 13.0, 14.2, 7.2),
    ("e", 27.5, 14.8, 6.8),
    ("n", 41.5, 13.8, 6.9),
    ("o", 55.5, 12.6, 6.8),
    ("r", 69.5, 11.4, 6.4),
]


def draw_senor(c):
    """
    'Senor' in the same fat rounded idiom, at ~0.38 of the Tacombi x-height.
    Built from the same primitives -- bowls with cut counters and short
    strokes -- so the two words read as one hand.
    """
    def O(cx, cy, s, rot=0.0):
        bowl(c, cx, cy, 0.56 * s, 0.54 * s, rot)
        c.cut(ellipse_pts(cx, cy, 0.17 * s, 0.16 * s, rot))

    for ch, x, y, s in SENOR:
        if ch == "S":
            c.stroke(poly(bez((x + 4.0, y - 4.6), (x - 0.4, y - 6.4),
                              (x - 4.0, y - 3.4), (x - 1.4, y - 0.6)),
                          bez((x - 1.4, y - 0.6), (x + 2.2, y + 2.2),
                              (x + 4.6, y + 3.6), (x + 1.2, y + 5.2)),
                          bez((x + 1.2, y + 5.2), (x - 2.0, y + 6.2),
                              (x - 4.4, y + 4.6), (x - 4.6, y + 2.6))),
                     widths(400, [(0.0, 2.2), (0.3, 3.3), (0.6, 3.4),
                                  (1.0, 2.3)]))
        elif ch == "e":
            bowl(c, x, y, 0.54 * s, 0.50 * s)
            c.cut(ellipse_pts(x + 0.2, y - 1.0, 0.23 * s, 0.15 * s))
            c.cut(poly(bez((x + 0.6, y + 0.9), (x + 2.4, y + 1.4),
                           (x + 3.6, y + 2.6), (x + 4.4, y + 4.2)),
                       bez((x + 4.4, y + 4.2), (x + 2.0, y + 4.4),
                           (x + 0.4, y + 3.2), (x + 0.6, y + 0.9))))
        elif ch == "n":
            for dx in (-2.7, 2.7):
                c.stroke(poly(bez((x + dx, y - 2.0), (x + dx, y + 1.0),
                                  (x + dx, y + 2.4), (x + dx, y + 3.8))), 2.7)
            c.stroke(poly(bez((x - 2.9, y - 1.8), (x - 1.7, y - 5.0),
                              (x + 1.7, y - 5.0), (x + 2.9, y - 1.8))), 2.7)
            # the tilde
            c.stroke(poly(bez((x - 3.8, y - 8.0), (x - 1.6, y - 10.2),
                              (x + 1.2, y - 7.0), (x + 3.6, y - 8.8))), 1.7)
        elif ch == "o":
            O(x, y, s)
        elif ch == "r":
            c.stroke(poly(bez((x - 2.4, y - 2.8), (x - 2.6, y + 0.6),
                              (x - 2.4, y + 2.2), (x - 2.2, y + 3.8))), 2.7)
            c.stroke(poly(bez((x - 2.6, y - 1.8), (x - 0.8, y - 4.6),
                              (x + 2.0, y - 4.4), (x + 3.2, y - 2.4))),
                     widths(400, [(0.0, 2.6), (1.0, 1.8)]))


def build():
    c = Canvas()
    draw_T(c)
    draw_a(c)
    draw_c(c)
    draw_o(c)
    draw_m(c)
    draw_b(c)
    draw_i(c)
    draw_senor(c)
    return c.alpha()


# --------------------------------------------------------------------- output
def main():
    a = build()
    np.save("/tmp/gen_alpha.npy", a)

    ys, xs = np.nonzero(a > 32)
    print("generated ink bbox  x %d-%d  y %d-%d   (%dx%d, AR %.3f)"
          % (xs.min(), xs.max(), ys.min(), ys.max(),
             xs.max() - xs.min() + 1, ys.max() - ys.min() + 1,
             (xs.max() - xs.min() + 1) / (ys.max() - ys.min() + 1)))
    print("reference  ink bbox  x %d-%d  y %d-%d   (%dx%d, AR %.3f)"
          % (INK_BBOX[0], INK_BBOX[2], INK_BBOX[1], INK_BBOX[3],
             INK_BBOX[2] - INK_BBOX[0] + 1, INK_BBOX[3] - INK_BBOX[1] + 1,
             (INK_BBOX[2] - INK_BBOX[0] + 1) / (INK_BBOX[3] - INK_BBOX[1] + 1)))

    # crop to the generated ink bbox and emit at OUT_W
    sub = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h = int(round(OUT_W * sub.shape[0] / sub.shape[1]))
    al = np.array(Image.fromarray(sub.astype(np.uint8))
                  .resize((OUT_W, h), Image.LANCZOS))
    # silver: neutral, value keyed to the measured ink, with a dark keyline
    # implied by the alpha edge rather than painted in.
    rgb = np.zeros((h, OUT_W, 3), np.uint8)
    rgb[..., 0], rgb[..., 1], rgb[..., 2] = 214, 216, 218
    out = np.dstack([rgb, al])
    os.makedirs(TEX, exist_ok=True)
    Image.fromarray(out).save(os.path.join(TEX, "senor.png"))
    print("wrote tex/senor.png  %dx%d  AR %.4f" % (OUT_W, h, OUT_W / h))
    return OUT_W / h


if __name__ == "__main__":
    ar = main()
    if "--compare" in sys.argv:
        import compare_script
        compare_script.run()
