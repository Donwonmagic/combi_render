"""Flank folk art -- `tex/swirl.png`.

rev 8b, part of the art reproduction pass Donald scoped to four pieces: the
mural, THE PAISLEY, the "Senor Tacombi" script and the "100% Calidad" decal.

The previous tile was measured (by the AUDIT_RECOVERED triage) as
**one flat gold**: 0.0 % of texels in hue 0-25 deg, 89 % in hue 25-45,
median (234,172,27), pale texels 0.75 %. The real signwriting is not one
colour and not one motif. Read off `ref_rear34.jpg` and `ref_side.jpg` at 4-5x,
the vocabulary is FOUR things:

  1. big GOLD ACANTHUS SCROLLS -- thick tapered strokes that curl, with rolled
     ends and small inner "eye" curls. One large paisley/comma dominates each
     rear quarter, with tendrils growing off it.
  2. thin GOLD TENDRILS branching from the scrolls, hairline-tapered.
  3. ROSETTES -- concentric-ring daisies ~10-12 lobes, an orange/red outer
     ring, a ring of pale cream dots, a gold centre. Scattered densely.
  4. DARK-BROWN COMMA PAISLEYS with a cluster of dots inside them. These read
     almost black against the red and they are what the old tile missed
     entirely -- they are the reason the reference reads as signwriting with
     depth rather than as a gold decal.

Measured over the flank folk-art region of `ref_rear34.jpg` (n = 19760):

    gold / yellow  13.1 %   mean sRGB (195,161, 39)
    orange         51.1 %   mean sRGB (141, 96, 61)
    red            35.5 %   mean sRGB (162, 64, 36)
    dark            10.2 %  mean sRGB ( 45, 35, 26)   <- the dark commas
    pale             3.5 %  mean sRGB (218,196,169)   <- cream rosette rings

Note the orange/red fractions are dominated by the BODY colour showing through
between motifs; what this generator has to match is the motif palette and the
coverage, not those two percentages. Alpha carries the coverage.

Output is RGBA with a transparent ground, drawn at 2x and downsampled so the
stroke edges stay clean where the flank curves away.
"""
import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

TEXDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tex")

N = 2048
SS = 2                                   # supersample

GOLD = (243, 196, 44, 255)               # the acanthus scrolls and tendrils
GOLD_D = (208, 150, 26, 255)             # shaded side of a scroll
ROSE_O = (226, 96, 34, 255)              # rosette outer ring
ROSE_P = (238, 216, 178, 255)            # rosette cream dot ring
ROSE_C = (246, 198, 62, 255)             # rosette centre
DARK = (58, 40, 28, 255)                 # the dark-brown commas


def _stroke(d, pts, w0, w1, fill):
    """Tapered stroke through pts, width w0 -> w1, with a rounded start."""
    n = len(pts)
    left, right = [], []
    for i in range(n - 1):
        ax, ay = pts[i]
        bx, by = pts[i + 1]
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy) or 1.0
        w = w0 + (w1 - w0) * i / (n - 1)
        nx, ny = -dy / L * w / 2, dx / L * w / 2
        left.append((ax + nx, ay + ny))
        right.append((ax - nx, ay - ny))
    d.polygon(left + right[::-1], fill=fill)
    d.ellipse([pts[0][0] - w0 / 2, pts[0][1] - w0 / 2,
               pts[0][0] + w0 / 2, pts[0][1] + w0 / 2], fill=fill)


def _curl(cx, cy, s, turns=2.3, flip=1, phase=0.0, grow=0.052):
    pts = []
    n = 70
    for i in range(n):
        t = phase + turns * math.pi * i / (n - 1)
        r = s * (0.15 + grow * t)
        pts.append((cx + flip * r * math.cos(t), cy + r * math.sin(t)))
    return pts


def acanthus(d, cx, cy, s, flip=1, phase=0.0):
    """A big gold scroll: main curl, a shade pass, and two inner eye curls."""
    main = _curl(cx, cy, s, turns=2.5, flip=flip, phase=phase)
    _stroke(d, main, s * 0.30, s * 0.045, GOLD_D)
    main2 = [(x, y - s * 0.030) for (x, y) in main]
    _stroke(d, main2, s * 0.26, s * 0.035, GOLD)
    for f, ss in ((0.34, 0.34), (0.62, 0.26)):
        i = int(f * (len(main) - 1))
        ex, ey = main[i]
        eye = _curl(ex, ey, s * ss, turns=1.7, flip=-flip, phase=phase + 1.1)
        _stroke(d, eye, s * 0.10, s * 0.02, GOLD)


def tendril(d, cx, cy, s, flip=1, phase=0.0):
    _stroke(d, _curl(cx, cy, s, turns=2.9, flip=flip, phase=phase),
            s * 0.085, s * 0.014, GOLD)


def rosette(d, cx, cy, R):
    """Concentric-ring daisy: orange outer, cream dot ring, gold centre."""
    lobes = 11
    for k in range(lobes):
        a = 2 * math.pi * k / lobes
        px, py = cx + R * 0.70 * math.cos(a), cy + R * 0.70 * math.sin(a)
        d.ellipse([px - R * 0.34, py - R * 0.34, px + R * 0.34, py + R * 0.34],
                  fill=ROSE_O)
    d.ellipse([cx - R * 0.74, cy - R * 0.74, cx + R * 0.74, cy + R * 0.74],
              fill=ROSE_O)
    for k in range(lobes):
        a = 2 * math.pi * k / lobes + math.pi / lobes
        px, py = cx + R * 0.46 * math.cos(a), cy + R * 0.46 * math.sin(a)
        d.ellipse([px - R * 0.15, py - R * 0.15, px + R * 0.15, py + R * 0.15],
                  fill=ROSE_P)
    d.ellipse([cx - R * 0.30, cy - R * 0.30, cx + R * 0.30, cy + R * 0.30],
              fill=ROSE_C)


def dark_comma(d, cx, cy, s, flip=1, phase=0.0):
    """Dark-brown comma paisley with a cluster of dots inside it."""
    pts = _curl(cx, cy, s, turns=1.35, flip=flip, phase=phase, grow=0.075)
    _stroke(d, pts, s * 0.46, s * 0.05, DARK)
    hx, hy = pts[2]
    for (ux, uy) in ((-0.10, -0.10), (0.10, -0.04), (0.00, 0.12)):
        d.ellipse([hx + s * (ux - 0.055), hy + s * (uy - 0.055),
                   hx + s * (ux + 0.055), hy + s * (uy + 0.055)],
                  fill=(24, 16, 12, 255))


def make(path=None):
    n = N * SS
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(1963)

    # --- one dominant paisley cluster, as on the real rear quarter, plus
    #     supporting scrolls. Placed rather than tiled: the density mask in
    #     t1_mats decides where this lands on the body.
    acanthus(d, n * 0.30, n * 0.34, n * 0.185, flip=1, phase=0.2)
    acanthus(d, n * 0.72, n * 0.30, n * 0.150, flip=-1, phase=0.9)
    acanthus(d, n * 0.52, n * 0.72, n * 0.165, flip=1, phase=2.1)
    acanthus(d, n * 0.13, n * 0.80, n * 0.115, flip=-1, phase=1.4)

    for i in range(16):
        tendril(d, rng.integers(int(n * 0.05), int(n * 0.95)),
                rng.integers(int(n * 0.05), int(n * 0.95)),
                rng.integers(int(n * 0.045), int(n * 0.090)),
                flip=1 if i % 2 else -1, phase=rng.random() * 3.0)

    for i in range(9):
        dark_comma(d, rng.integers(int(n * 0.08), int(n * 0.92)),
                   rng.integers(int(n * 0.08), int(n * 0.92)),
                   rng.integers(int(n * 0.045), int(n * 0.080)),
                   flip=1 if i % 2 else -1, phase=rng.random() * 2.0)

    for i in range(26):
        rosette(d, rng.integers(int(n * 0.04), int(n * 0.96)),
                rng.integers(int(n * 0.04), int(n * 0.96)),
                rng.integers(int(n * 0.017), int(n * 0.032)))

    im = im.resize((N, N), Image.LANCZOS)
    im = im.filter(ImageFilter.GaussianBlur(0.4))
    p = path or os.path.join(TEXDIR, "swirl.png")
    im.save(p)
    return p


if __name__ == "__main__":
    print(make())
