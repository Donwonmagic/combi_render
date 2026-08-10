"""Artwork for the two roof-lid boards.

rev 8. The lids are cut roof skin, hinged, shown OPEN, and the main lid's
underside is the vehicle's signboard -- the thing that makes it a taqueria
rather than a bus, and the emotional centre of any hero render of it.

REPRODUCTION, NOT RECONSTRUCTION (rev 8b). The first pass derived a plausible
board from measured palette ratios. Donald's brief -- he wants the owner to
remember standing in this vehicle -- makes that not good enough: a generic
flower pattern does not trigger a memory, the actual board does. So the design
below is read off `ref_side.jpg` at 4x magnification, element by element.

The mural occupies ~450 x 270 px in the reference. That is enough to read the
DESIGN -- ring structure, motif vocabulary, wording, layout, palette -- and
nowhere near enough to resample as a texture. So it is redrawn at 2048 x 1024
from what the photograph shows, not traced.

WHAT THE PHOTOGRAPH SHOWS, and what the first pass got wrong:

  flower head   11 scalloped lobes in concentric rings --
                red -> orange -> a ring of fat pale-cream lobes -> gold ring ->
                pale disc -> and a small PEACE SIGN at the centre of many.
                (first pass: 8 crude ellipses, 3 rings, no cream lobe ring,
                no centre motif)
  stems         thick VERMILLION-ORANGE, straight, near-full height
                (first pass: thin gold)
  leaves        small pale-gold ALMOND leaves angled off the stems
                (first pass: absent)
  ground fill   dense CALLIGRAPHIC PAISLEY tendrils in gold AND red, thick
                TAPERED strokes with rolled ends, covering nearly all the
                ground (first pass: thin constant-width spirals, sparse --
                which is why it read as scribble rather than signwriting)
  ground        very dark maroon-brown, barely visible through the fill
  border        yellow frame on ALL FOUR sides, black condensed slab caps,
                five-pointed star separators, and painted FOOD VIGNETTES
                between the text blocks -- a torta with pink filling, a glass
                of juice with a fruit slice, a ceviche tostada with pink
                shrimp, a plate of tacos
                (first pass: three sides, text only, no vignettes)

Measured on the board interior, n = 70400, excluding the strips:
    hue 0-18  (red)    43.0 %   mean sRGB (113, 37, 22)
    hue 18-35 (orange) 34.0 %   mean sRGB (132, 68, 20)
    hue 35-55 (yellow) 17.0 %   mean sRGB (140,105, 28)
    dark ground        24.9 %   mean sRGB ( 58, 33, 22)
    menu strip         sRGB (159,127, 46)  hue 47.6 sat 0.72 val 0.62
Those are in-situ values off a shaded photograph and carry the scene exposure;
what transfers is the RATIO structure, with the absolute level set for albedo.
Painted board, matte. NOT emissive -- the warm read is the scene light.
"""
import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

TEXDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tex")

# albedo, sRGB 0-255
GROUND = (58, 26, 20)          # dark maroon-brown behind the fill
RED = (214, 48, 24)            # outer petal ring, red paisley
ORANGE = (240, 122, 26)        # second ring, stems
GOLD = (247, 186, 38)          # gold ring, gold paisley, leaves
PALE = (253, 232, 176)         # the fat cream lobe ring
DISC = (250, 206, 74)          # inner disc
STRIP = (243, 201, 52)         # yellow menu strip
INK = (36, 22, 14)             # lettering
PINK = (232, 126, 132)         # the pink in the torta / ceviche vignettes
GREEN = (108, 148, 62)         # garnish

W, H = 2048, 1024
N_FLOWERS = 9                  # counted off ref_side.jpg by Donald


def _font(sz):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, sz)
            except Exception:
                pass
    return ImageFont.load_default()


# --------------------------------------------------------------- primitives
def _scallop(d, cx, cy, r, lobes, fill, phase=0.0, lobe=0.42):
    """A scalloped ring: `lobes` overlapping discs on a circle, plus the core."""
    for k in range(lobes):
        a = phase + 2 * math.pi * k / lobes
        px, py = cx + r * math.cos(a), cy + r * math.sin(a)
        d.ellipse([px - r * lobe, py - r * lobe, px + r * lobe, py + r * lobe],
                  fill=fill)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)


def _peace(d, cx, cy, r, fill):
    """The centre motif. Many heads on the real board carry one."""
    wdt = max(2, int(r * 0.18))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=fill, width=wdt)
    d.line([(cx, cy - r), (cx, cy + r)], fill=fill, width=wdt)
    for sgn in (-1, 1):
        d.line([(cx, cy), (cx + sgn * r * 0.71, cy + r * 0.71)],
               fill=fill, width=wdt)


def flower(d, cx, cy, R, phase=0.0, peace=True):
    """One head: concentric scalloped rings + centre, per ref_side.jpg at 4x."""
    lobes = 11
    _scallop(d, cx, cy, R * 0.92, lobes, RED, phase)
    _scallop(d, cx, cy, R * 0.74, lobes, ORANGE, phase)
    _scallop(d, cx, cy, R * 0.54, lobes, PALE, phase)      # fat cream lobes
    for rr, col in ((0.45, ORANGE), (0.37, GOLD), (0.29, DISC)):
        d.ellipse([cx - R * rr, cy - R * rr, cx + R * rr, cy + R * rr], fill=col)
    if peace:
        _peace(d, cx, cy, R * 0.185, PALE)


def _taper_curl(d, x0, y0, s, fill, flip=1, turns=2.4, w0=0.20):
    """A calligraphic paisley tendril: a spiral of DECREASING width, rolled end."""
    n = 64
    pts, wid = [], []
    for i in range(n):
        t = turns * math.pi * i / (n - 1)
        rr = s * (0.16 + 0.052 * t)
        pts.append((x0 + flip * rr * math.cos(t), y0 + rr * math.sin(t)))
        wid.append(s * w0 * (1.0 - 0.72 * i / (n - 1)))
    left, right = [], []
    for i in range(n - 1):
        ax, ay = pts[i]
        bx, by = pts[i + 1]
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L * wid[i] / 2, dx / L * wid[i] / 2
        left.append((ax + nx, ay + ny))
        right.append((ax - nx, ay - ny))
    d.polygon(left + right[::-1], fill=fill)
    ex, ey = pts[-1]
    w = max(1.0, wid[-1])
    d.ellipse([ex - w, ey - w, ex + w, ey + w], fill=fill)


def _leaf(d, x, y, L, ang, fill=GOLD):
    """Pale-gold almond leaf on a stem."""
    pts = []
    for t in np.linspace(0, 2 * math.pi, 26):
        u, v = L * math.cos(t), L * 0.30 * math.sin(t)
        pts.append((x + u * math.cos(ang) - v * math.sin(ang),
                    y + u * math.sin(ang) + v * math.cos(ang)))
    d.polygon(pts, fill=fill)


# ----------------------------------------------------------- food vignettes
def _vig_torta(d, cx, cy, s):
    d.ellipse([cx - s, cy - s * 0.42, cx + s, cy + s * 0.52], fill=(214, 158, 78))
    d.rectangle([cx - s * 0.86, cy - s * 0.06, cx + s * 0.86, cy + s * 0.20],
                fill=PINK)
    d.ellipse([cx - s * 0.55, cy + s * 0.10, cx + s * 0.30, cy + s * 0.34],
              fill=GREEN)


def _vig_juice(d, cx, cy, s):
    d.polygon([(cx - s * 0.42, cy - s * 0.72), (cx + s * 0.42, cy - s * 0.72),
               (cx + s * 0.30, cy + s * 0.66), (cx - s * 0.30, cy + s * 0.66)],
              fill=(246, 168, 44))
    d.ellipse([cx + s * 0.06, cy - s * 0.20, cx + s * 0.96, cy + s * 0.62],
              fill=(238, 128, 36))
    d.ellipse([cx + s * 0.24, cy - s * 0.02, cx + s * 0.78, cy + s * 0.44],
              fill=(250, 196, 96))


def _vig_ceviche(d, cx, cy, s):
    d.ellipse([cx - s, cy - s * 0.30, cx + s, cy + s * 0.42], fill=(238, 206, 130))
    d.ellipse([cx - s * 0.70, cy - s * 0.26, cx + s * 0.70, cy + s * 0.14],
              fill=GREEN)
    for k in (-0.36, 0.02, 0.40):
        d.ellipse([cx + s * (k - 0.20), cy - s * 0.24,
                   cx + s * (k + 0.22), cy + s * 0.06], fill=PINK)


def _vig_tacos(d, cx, cy, s):
    for k in (-0.46, 0.0, 0.46):
        d.ellipse([cx + s * (k - 0.34), cy - s * 0.34,
                   cx + s * (k + 0.34), cy + s * 0.34], fill=(232, 178, 66))
    d.ellipse([cx - s * 0.30, cy + s * 0.10, cx + s * 0.40, cy + s * 0.40],
              fill=GREEN)


def _star(d, cx, cy, r, fill=INK):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + math.pi * k / 5
        rr = r if k % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill)


# ------------------------------------------------------------------- boards
def mural(path=None):
    im = Image.new("RGB", (W, H), GROUND)
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(1963)

    strip_w = int(W * 0.098)
    top_h = int(H * 0.090)
    bot_h = int(H * 0.030)
    x_lo, x_hi = strip_w + 40, W - strip_w - 40
    y_top, y_bot = top_h, H - bot_h

    # --- NINE heads: five upper, four staggered below
    xs_up = np.linspace(x_lo + 120, x_hi - 120, 5)
    xs_lo = np.linspace(x_lo + 285, x_hi - 285, 4)
    # Heads sized so DARK GROUND AND PAISLEY SHOW BETWEEN THEM. The previous
    # pass had them touching, which turned the board into a flower pattern; on
    # the real board the tendril fill is as much of the read as the flowers.
    heads = [(x, y_top + (H * 0.245 if i % 2 else H * 0.175), 112 + 8 * (i % 3))
             for i, x in enumerate(xs_up)]
    heads += [(x, y_top + (H * 0.585 if i % 2 else H * 0.515), 100)
              for i, x in enumerate(xs_lo)]
    assert len(heads) == N_FLOWERS

    # --- stems first: thick vermillion-orange, running to the bottom
    for (hx, hy, R) in heads:
        d.line([(hx, hy), (hx + (hx - W / 2) / (W / 2) * 26, y_bot)],
               fill=ORANGE, width=int(R * 0.150))

    # --- leaves on the stems
    for j, (hx, hy, R) in enumerate(heads):
        for k, f in enumerate((0.42, 0.66, 0.88)):
            yy = hy + (y_bot - hy) * f
            sgn = 1 if (j + k) % 2 else -1
            _leaf(d, hx + sgn * R * 0.30, yy, R * 0.30, sgn * 0.95)

    # --- dense calligraphic paisley, gold and red, filling the ground
    for i in range(120):
        _taper_curl(d, rng.integers(x_lo - 30, x_hi + 30),
                    rng.integers(y_top + 25, y_bot - 15),
                    rng.integers(40, 96), GOLD if i % 2 else RED,
                    flip=1 if i % 3 else -1,
                    turns=2.4 + 1.4 * rng.random(), w0=0.15)

    # --- heads last, over the fill
    for i, (hx, hy, R) in enumerate(heads):
        flower(d, hx, hy, R, phase=0.19 * i, peace=(i % 2 == 0))

    im = im.filter(ImageFilter.GaussianBlur(0.7))
    d = ImageDraw.Draw(im)

    # --- yellow frame, ALL FOUR sides
    d.rectangle([0, 0, strip_w, H], fill=STRIP)
    d.rectangle([W - strip_w, 0, W, H], fill=STRIP)
    d.rectangle([0, 0, W, top_h], fill=STRIP)
    d.rectangle([0, H - bot_h, W, H], fill=STRIP)

    # --- top strip: stars + slab caps + corner vignettes
    d.text((W * 0.5, top_h * 0.52), "FRESH JUICES,  GOURMET TACOS  &  TORTAS",
           font=_font(int(H * 0.044)), fill=INK, anchor="mm")
    _star(d, int(W * 0.148), top_h // 2, int(top_h * 0.24))
    _star(d, int(W * 0.852), top_h // 2, int(top_h * 0.24))
    _vig_tacos(d, strip_w // 2, top_h + int(H * 0.055), strip_w * 0.32)
    _vig_tacos(d, W - strip_w // 2, top_h + int(H * 0.055), strip_w * 0.32)

    # --- side strips: stacked wording interleaved with painted food
    f_s, f_s2 = _font(int(H * 0.036)), _font(int(H * 0.028))
    seq = [("t", "TACOS"), ("t", "&"), ("t", "TORTAS"),
           ("v", _vig_torta), ("t", "FRESH"), ("v", _vig_juice),
           ("t", "JUICES"), ("s", "CEVICHE"), ("s", "TOSTADAS"),
           ("v", _vig_ceviche), ("t", "SHRIMP"), ("s", "& FISH"), ("t", "TACOS")]
    for side_x in (strip_w * 0.5, W - strip_w * 0.5):
        y = top_h + H * 0.115
        for kind, val in seq:
            if kind == "v":
                val(d, side_x, y + H * 0.006, strip_w * 0.32)
                y += H * 0.086
            else:
                d.text((side_x, y), val, font=(f_s if kind == "t" else f_s2),
                       fill=INK, anchor="mm")
                y += H * 0.056

    im = im.filter(ImageFilter.GaussianBlur(0.45))
    p = path or os.path.join(TEXDIR, "lidmural.png")
    im.save(p)
    return p


def rear_sign(path=None):
    """The smaller aft lid. ref_rear34.jpg: up and lettered 'LA SANTA...'."""
    im = Image.new("RGB", (1024, 512), (228, 224, 210))
    d = ImageDraw.Draw(im)
    d.rectangle([10, 10, 1013, 501], outline=(203, 195, 176), width=6)
    d.text((512, 214), "La Santa", font=_font(158), fill=(178, 40, 28),
           anchor="mm")
    d.text((512, 336), "T A C O M B I", font=_font(54), fill=(178, 40, 28),
           anchor="mm")
    _star(d, 250, 336, 16, (178, 40, 28))
    _star(d, 774, 336, 16, (178, 40, 28))
    im = im.filter(ImageFilter.GaussianBlur(0.5))
    p = path or os.path.join(TEXDIR, "lidsign.png")
    im.save(p)
    return p


if __name__ == "__main__":
    print(mural())
    print(rear_sign())
