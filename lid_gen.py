"""Artwork for the two roof-lid boards.

rev 8. The lids are cut roof skin, hinged, shown OPEN, and their undersides are
the vehicle's signage -- the thing that makes it a taqueria rather than a bus.

Everything here is sized and coloured off ref_side.jpg / ref_rear34.jpg, not
invented. Measured on the board interior (excluding the menu strips), n=70400:

    hue 0-18   (red)     43.0 %   mean sRGB (113, 37, 22)
    hue 18-35  (orange)  34.0 %   mean sRGB (132, 68, 20)
    hue 35-55  (yellow)  17.0 %   mean sRGB (140,105, 28)
    dark ground          24.9 %   mean sRGB ( 58, 33, 22)
    overall             hue 33.8  sat 0.78  val 0.48
    menu strip          sRGB (159,127, 46)  hue 47.6 sat 0.72 val 0.62

Those are IN-SITU values off a shaded photograph, so they carry the scene's
exposure. What is transferred here is the RATIO structure -- ground:flower:strip
and the hue split -- with the absolute level set for an albedo map. Painted
board, matte, not emissive.
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

TEXDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tex")

# albedo, sRGB 0-255. The photograph's board sits at val 0.48 under shade; as an
# albedo the same paint reads roughly 1.8x that, held below 0.85 so nothing
# clips in the render.
GROUND = (74, 34, 24)          # dark red-brown between the flowers
PETAL_O = (238, 132, 26)       # orange petal ring
PETAL_Y = (250, 196, 44)       # yellow inner ring
CENTRE = (252, 232, 150)       # pale centre
STEM = (236, 170, 30)          # stem / scroll gold
SCROLL = (208, 58, 26)         # red scrollwork
STRIP = (238, 196, 60)         # yellow menu strip
STRIP_INK = (86, 30, 16)       # menu lettering

W, H = 2048, 1024


def _font(sz):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, sz)
            except Exception:
                pass
    return ImageFont.load_default()


def _flower(d, cx, cy, r, petals=8, phase=0.0):
    """Concentric-ring daisy, the motif that repeats across the board."""
    for k in range(petals):
        a = phase + 2 * math.pi * k / petals
        px, py = cx + r * 0.62 * math.cos(a), cy + r * 0.62 * math.sin(a)
        d.ellipse([px - r * 0.42, py - r * 0.42, px + r * 0.42, py + r * 0.42],
                  fill=PETAL_O)
    d.ellipse([cx - r * 0.66, cy - r * 0.66, cx + r * 0.66, cy + r * 0.66],
              fill=PETAL_Y)
    for k in range(petals):
        a = phase + 2 * math.pi * k / petals + math.pi / petals
        px, py = cx + r * 0.40 * math.cos(a), cy + r * 0.40 * math.sin(a)
        d.ellipse([px - r * 0.20, py - r * 0.20, px + r * 0.20, py + r * 0.20],
                  fill=PETAL_O)
    d.ellipse([cx - r * 0.26, cy - r * 0.26, cx + r * 0.26, cy + r * 0.26],
              fill=CENTRE)


def _scroll(d, x0, y0, s, flip=1):
    """One curl of the folk-art scrollwork that fills between the stems."""
    pts = []
    for t in np.linspace(0, 3.2 * math.pi, 90):
        rr = s * (0.10 + 0.030 * t)
        pts.append((x0 + flip * rr * math.cos(t), y0 + rr * math.sin(t)))
    d.line(pts, fill=SCROLL, width=max(2, int(s * 0.06)), joint="curve")


def mural(path=None):
    """The big front/centre lid: flowers on stems, yellow menu strips both edges."""
    im = Image.new("RGB", (W, H), GROUND)
    d = ImageDraw.Draw(im)

    strip_w = int(W * 0.098)          # measured off ref_side.jpg
    top_h = int(H * 0.088)
    rng = np.random.default_rng(1963)

    x_lo, x_hi = strip_w + 60, W - strip_w - 60
    xs = np.linspace(x_lo, x_hi, 9)

    # --- stems, rising from the bottom edge, slightly splayed
    for i, x in enumerate(xs):
        lean = (x - W / 2) / (W / 2) * 48
        d.line([(x, H), (x + lean, H * 0.26)], fill=STEM,
               width=int(17 + 6 * rng.random()))

    # --- red scrollwork. The reference measures 43 % of the board interior in
    # hue 0-18 deg, so the curls are not an accent -- they carry the ground.
    for i, x in enumerate(xs):
        for yy, ss in ((H * 0.80, 150), (H * 0.44, 132)):
            _scroll(d, x + (34 if i % 2 else -34) + rng.integers(-16, 16),
                    yy + rng.integers(-26, 26), ss, flip=1 if i % 2 else -1)
    for i in range(13):                      # fill the gaps between the stems
        _scroll(d, rng.integers(x_lo, x_hi), rng.integers(int(top_h + 40), H - 30),
                rng.integers(70, 120), flip=1 if i % 2 else -1)

    # --- flowers. Alternate a red-petalled and an orange-petalled variant:
    # the reference board is red-dominant, not the uniform orange a single
    # palette gives.
    def bloom(cx, cy, r, i):
        if i % 3:
            _flower(d, cx, cy, r, petals=8, phase=0.21 * i)
        else:
            for k in range(8):               # red outer ring
                a = 0.21 * i + 2 * math.pi * k / 8
                px, py = cx + r * 0.62 * math.cos(a), cy + r * 0.62 * math.sin(a)
                d.ellipse([px - r * 0.44, py - r * 0.44,
                           px + r * 0.44, py + r * 0.44], fill=SCROLL)
            d.ellipse([cx - r * 0.62, cy - r * 0.62, cx + r * 0.62, cy + r * 0.62],
                      fill=PETAL_O)
            d.ellipse([cx - r * 0.36, cy - r * 0.36, cx + r * 0.36, cy + r * 0.36],
                      fill=PETAL_Y)
            d.ellipse([cx - r * 0.15, cy - r * 0.15, cx + r * 0.15, cy + r * 0.15],
                      fill=CENTRE)

    for i, x in enumerate(xs):
        lean = (x - W / 2) / (W / 2) * 48
        bloom(x + lean * 0.30, H * 0.28 + (36 if i % 2 else -20),
              128 + 18 * ((i * 5) % 3), i)
    mid = xs[:-1] + (xs[1] - xs[0]) / 2
    for i, x in enumerate(mid):
        bloom(x, H * 0.62 + (28 if i % 2 else -24), 106, i + 1)

    im = im.filter(ImageFilter.GaussianBlur(0.6))
    d = ImageDraw.Draw(im)

    # --- yellow menu strips down both long edges, and across the top
    d.rectangle([0, 0, strip_w, H], fill=STRIP)
    d.rectangle([W - strip_w, 0, W, H], fill=STRIP)
    d.rectangle([0, 0, W, top_h], fill=STRIP)

    def diamond(cx, cy, r):
        d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)],
                  fill=STRIP_INK)

    f_top = _font(int(H * 0.052))
    d.text((W * 0.5, top_h * 0.50), "FRESH JUICES  ·  GOURMET TACOS  &  TORTAS",
           font=f_top, fill=STRIP_INK, anchor="mm")
    diamond(int(W * 0.055), top_h // 2, int(top_h * 0.20))
    diamond(int(W * 0.945), top_h // 2, int(top_h * 0.20))

    f_side = _font(int(H * 0.034))
    items = ["TACOS", "&", "TORTAS", "FRESH", "JUICES", "SHRIMP", "& FISH"]
    for side_x in (strip_w * 0.5, W - strip_w * 0.5):
        y = top_h + H * 0.075
        for it in items:
            d.text((side_x, y), it, font=f_side, fill=STRIP_INK, anchor="mm")
            y += H * 0.122

    im = im.filter(ImageFilter.GaussianBlur(0.4))
    p = path or os.path.join(TEXDIR, "lidmural.png")
    im.save(p)
    return p


def rear_sign(path=None):
    """The smaller aft lid: cream board lettered in red script."""
    im = Image.new("RGB", (1024, 512), (226, 222, 208))
    d = ImageDraw.Draw(im)
    d.rectangle([12, 12, 1011, 499], outline=(206, 198, 180), width=5)
    f = _font(150)
    d.text((512, 232), "La Santa", font=f, fill=(176, 38, 28), anchor="mm")
    f2 = _font(52)
    d.text((512, 350), "T A C O M B I", font=f2, fill=(176, 38, 28), anchor="mm")
    im = im.filter(ImageFilter.GaussianBlur(0.5))
    p = path or os.path.join(TEXDIR, "lidsign.png")
    im.save(p)
    return p


if __name__ == "__main__":
    print(mural())
    print(rear_sign())
