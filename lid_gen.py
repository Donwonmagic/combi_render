"""Artwork for the two roof-lid boards.

rev 9. REBUILT FROM MEASUREMENT, 2026-08-10.

Everything below that carries a number was measured in the photograph's own
pixel frame, after rectifying the board out of perspective. The measurement
scripts and the annotated crops are in /home/claude/work/measure/out/ .

=============================================================================
A. THE FLOWER BOARD  (ref_side.jpg)                       -> lidmural.png
=============================================================================
Method. The board's yellow frame was traced edge by edge (per-column /
per-row scans of a hue-40-to-60 mask), four straight lines were fitted, the
interior quad was intersected out of them, and the board was rectified with a
homography onto a rectangle.  The rectangle's aspect was fixed by requiring
the flower heads -- which are 12-fold rosettes and therefore circular by
design -- to come out circular: the measured image x/y ratio of the heads is
1.029 +/- 0.07 (n = 9), so the image is stretched 2.9 % in x and the true
interior aspect is 1.5495.  Palm fronds and the man in the hatch were masked
(3.1 % of the interior) before any colour statistic was taken.

Rectified interior = 1859 x 1200 px.  Everything below is a fraction of that.

  BOARD                aspect (outer, incl. strips)     1.664
  side menu strip      0.0904 of interior width         (= 0.0765 of board W)
  top menu strip       0.0992 of interior height        (= 0.0902 of board H)
  bottom strip         NONE.  The mural runs to the bottom edge; below it is a
                       dark trim, then the roof.  rev 8 drew a yellow bottom
                       strip that is not there.

  FLOWER HEADS         TEN, not nine.  rev 8's nine missed the head behind the
                       palm fronds at (0.683, 0.268).  Centres, as fractions of
                       the interior, are in HEADS_UV below.
  head outer radius    0.0825 +/- 0.006 of interior width  (D/W = 0.165)
                       -- measured three ways: horizontal cut through the
                       cleanest head gives R = 149 px, the radial red-ring
                       profile peaks at 150 px and half-falls at 163 px.
                       rev 8 drew D = 0.141 of interior width: 15 % small.
  head ring structure  (radial hue/value profile, mean of 9 clean heads)
                       0.00-0.42 R  gold centre disc, thin orange ring at 0.38
                       0.42-0.62 R  gold scalloped ring carrying EIGHT fat pale
                                    cream petal-dots centred on 0.58 R.  Eight,
                                    not eleven: the angular V profile at the
                                    dot radius peaks every 45 deg (n = 6 heads)
                                    and eight dots are countable in out/M11.
                       0.62-0.80 R  orange scalloped ring
                       0.80-1.00 R  red scalloped ring, TWELVE lobes
                                    (median of 7 heads; 12,12,12,12,13,12 and
                                     one occluded outlier at 9)
                       centre       a small pale peace sign, at the resolution
                                    limit -- visible as a pale mark, its form
                                    is NOT independently measurable
  stems                near-vertical, orange, one per head, running to the
                       bottom edge.  Measured widths at mid-height span
                       0.010-0.020 of interior width, median 0.0145; drawn at
                       0.0154 (STEM_W_F x 1.10).
  ground fill          dense calligraphic tendrils in gold, orange AND red

  INTERIOR COLOUR, in situ, n = 2 161 104 rectified px, occluders masked.
  Classes: dark = HSV V < 0.30; then hue 345-14 red, 14-30 orange, 30-62 yellow.
      dark ground   21.82 %   mean sRGB ( 60, 32, 23)
      red           25.31 %   mean sRGB (132, 36, 22)
      orange        32.53 %   mean sRGB (145, 65, 20)
      yellow        20.33 %   mean sRGB (156,110, 30)
      interior mean sRGB (125.4, 59.7, 23.0); mean V 0.490, median V 0.537
      yellow menu strip  sRGB (165,140, 18)  hue 49.5  sat 0.91  V 0.645
      strip lettering    sRGB ( 55, 51, 19)

  THE TWO DEFECTS THIS REV FIXES, as numbers:
      dark ground   rev 8 texture 45.98 %   photograph 21.82 %  -> the board
                    was half bare.  That is the "far sparser" complaint.
      orange        rev 8 texture 17.68 %   photograph 32.53 %
      the rev-8 header claimed measured ratios of red 43 / orange 34 /
      yellow 17 among the non-dark pixels.  Re-measured independently here:
      red 32.4 / orange 41.6 / yellow 26.0.  The old numbers were wrong; they
      biased the board red, which is the other half of "darker".
      rev 8 also left the GROUND unlifted (58,26,20) while lifting the bright
      classes ~1.6x, so the dark held its photographic value while everything
      round it went to albedo -- the gaps read blacker than they should.

  ALBEDO LIFT.  The photograph is of a shaded board and carries the scene
  exposure.  A texture is an albedo.  One scalar E = 1.58 is applied to every
  measured class, chosen so the measured yellow class reaches a chrome-yellow
  enamel albedo; the RATIO structure is therefore preserved exactly and the
  absolute level is a stated assumption, not a measurement.  When the achieved
  texture is scored against the photograph the value threshold is scaled by the
  same E (dark = V < 0.30 * E = 0.474) so the comparison stays honest.

=============================================================================
B. THE LETTERED PANEL  (ref_rear34.jpg)                    -> lidsign.png
=============================================================================
rev 8 drew the words "La Santa" horizontally in DejaVu Serif Bold.  The
photograph shows nothing of the kind.  Read at 12-22x (out/L1, L4, L5, L13):

  WHAT IS LEGIBLE
    - "La", small, lower left, on its own lower baseline, about half the
      height of what follows
    - a large brush-script capital S: spiral entry at the top left, a full
      bowl, and a long descender that swings back down-LEFT and finishes in a
      taper below and before the S's own start
    - a RED FIVE-POINTED STAR, point up, sitting above and just left of the
      S's apex
    - after the S, SEVEN further script downstrokes climbing to the right at
      a steep angle, very tightly packed
  WHAT IS NOT LEGIBLE
    The seven strokes are a single merged ink mass at this resolution (the
    whole word is 80 x 99 px in a 1200 x 824 frame).  They cannot be resolved
    into individual letters.  Seven downstrokes is what "anta" would produce
    (a=2, n=2, t=1, a=2), so "La Santa" is consistent with the measurement,
    but the tail of the word is NOT INDEPENDENTLY LEGIBLE and is reconstructed,
    not read.  Do not report it as verified.

  MEASURED METRICS.  The panel was put into its own frame with an affine basis
  taken from its two traced edges: top edge y = 28 + 0.0938(x-596), left edge
  x = 590 - 0.0333(y-35).  The panel's true aspect is NOT MEASURABLE from one
  view, so all figures below are fractions of the panel, which are invariant to
  it.  A second anisotropy estimate comes from the star (a 5-point star is very
  nearly isotropic, w/h = 1.051 for a regular one; measured 12/13 px, so the
  panel's u axis is compressed 0.88 +/- 0.12) and is used only for the angles.

      word bounding box        u 0.174 - 0.519,  v 0.024 - 0.487
      baseline rise            46 - 50 deg in the panel plane
                               (dv/du = -1.460 in panel fractions)
      LETTER AXIS              6 - 7 deg from the panel's vertical.  The
                               letters stand UPRIGHT and are stepped up a
                               steeply climbing baseline.  That, not an
                               italic, is what the photograph shows: the
                               structure-tensor orientation of the ink is
                               -82 deg (n = 1000), i.e. near-vertical, while
                               the baseline runs at -46 deg.
      x-height                 0.174 of panel height  (34 px, on the first
                               letter after the S, where it is unclipped)
      capital S height         0.288 of panel height  (56 px)
      S descender below base   0.107 of panel height  (21 px)
      thick stroke width       0.021 of panel width   (5 px) = 0.22 x-height
      stroke pitch             0.0281 of panel width  (6.8 px) = 0.29 x-height
      star centre              u 0.2887, v 0.0463
      star width / height      0.0496 of W / 0.0667 of H
      "La" cap height          0.138 of panel height, i.e. 0.79 x-height,
                               its own baseline at v 0.468
      S baseline origin        u 0.2591, v 0.4099

  COLOUR.  The ink is blur-limited: the word is 80 px wide, so every ink pixel
  is mixed with the cream.  Unmixing the most-saturated 3 % (189,113,107)
  against the measured cream ground (231,220,196) at a 0.7 ink fraction gives
  the script red as (171, 67, 69); at 0.85 it gives (182, 94, 91).  The true
  enamel is redder than either because the mixing model cannot see the fully
  covered core.  Taken as (176, 46, 38), +/- 25 on G and B.  The outline is a
  dark warm brown, darkest observed pixel Y = 63, taken as (64, 42, 34).
  Cream ground measured (231, 220, 196) in situ -> (237, 227, 205) as albedo.

  THE ONE STATED DEVIATION.  At the measured position and slope the last two
  letters' tops fall 116 px (0.67 x-height) above the top boundary of the cream
  the photograph shows -- they are cut by it.  Whether that boundary is the
  panel's own edge (there is a thin yellow pinstripe on it, which argues edge)
  or the mural board occluding from behind (its edge is straight too) cannot be
  settled from one view.  The word is therefore shifted DOWN the baseline
  normal by exactly that 116 px so the letterforms come out whole.  Everything
  else is at the measured value.  SIGN_TOP_SHIFT below is that one number.

=============================================================================
D. ACHIEVED vs TARGET.  Reproduce with `python3 lid_gen.py`.
=============================================================================
  MURAL, board interior, classifier of section A, dark threshold x E:
                 achieved    photograph   delta      rev 8 texture
      dark        21.96 %      21.82 %    +0.14        45.98 %
      red         25.46 %      25.31 %    +0.15        18.20 %
      orange      32.57 %      32.53 %    +0.04        17.68 %
      yellow      20.01 %      20.33 %    -0.32        18.14 %
      mean V       0.768       0.774                    0.582
      mean sRGB  (195.8, 96.4, 42.4)  vs (198.1, 94.3, 36.3)
      flower heads    10           10                      9
      head D / Wi   0.165        0.165                   0.141

  SIGN, panel fractions, v targets carrying the stated shift:
                 achieved    photograph   delta
      word u lo    0.1856      0.1740     +0.0116
      word u hi    0.4989      0.5190     -0.0201
      S descender  0.6680      0.6376     +0.0304
      star u       0.2885      0.2887     -0.0002
      star v       0.1580      0.1623     -0.0043
      star w       0.0497      0.0496     +0.0001
      star h       0.0640      0.0667     -0.0027

=============================================================================
C. WHICH LID GETS WHICH BOARD -- NOT FIXABLE IN THIS FILE
=============================================================================
The lids open forward, so the lettered cream panel belongs on the FRONT lid's
underside.  The assignment is made outside this file:

    build.py:252   A(lid_boards[0], "lidmural")   <- lid_boards[0] is the
                   FRONT lid (t1_shell.LID_X0 = +0.964 .. LID_X1 = -1.070)
    build.py:253   A(lid_boards[1], "lidsign")    <- lid_boards[1] is the REAR
                   lid (t1_shell.LID2_X0 = -1.140 .. LID2_X1 = -1.780)

so the lettered panel is currently on the REAR lid and the mural on the FRONT
lid, which is the wrong way round.  The fix is to swap the two material names
on those two lines.  See the report; this file does not touch it, and does not
smuggle the artwork across by writing the lettering into lidmural.png, because
that would leave both file names lying.

Sizes.  lidmural.png is written at the measured board aspect 1.664.  The front
lid board in t1_shell is 2.034 m x 1.110 m = 1.832, so once build.py is
corrected the mural texture will be stretched about 10 % across the lid; that
is a geometry discrepancy in t1_shell, reported, not papered over here.
lidsign.png is written at 1.832 to suit the front lid it belongs on.
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

TEXDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tex")

# ------------------------------------------------------- measured, ref_side
BOARD_ASPECT = 1.664           # outer, incl. strips
STRIP_SIDE_F = 0.0765          # side strip width / board width
STRIP_TOP_F = 0.0902           # top strip height / board height
HEAD_R_F = 0.0825              # head outer radius / interior width
STEM_W_F = 0.0140              # stem width / interior width
N_LOBE_RED = 12                # outer scalloped ring
N_DOT = 8                      # pale petal-dots

# head centres as (u, v) fractions of the rectified interior
HEADS_UV = [
    (0.0410, 0.2871), (0.3821, 0.1477), (0.2666, 0.4367), (0.1635, 0.6124),
    (0.5157, 0.4467), (0.6827, 0.2684), (0.8148, 0.4249), (0.7504, 0.6988),
    (0.9491, 0.2616), (0.8809, 0.9035),
]
N_FLOWERS = len(HEADS_UV)      # 10, counted off the rectified board

# measured class means, in situ (see header), and the one stated albedo lift
EXPOSURE = 1.58
_INSITU = {
    "ground": (60, 32, 23),
    "red": (132, 36, 22),
    "orange": (145, 65, 20),
    "gold": (156, 110, 30),
    "strip": (165, 140, 18),
}


def _albedo(rgb, e=EXPOSURE, cap=252):
    """Lift an in-situ measurement to albedo by one scalar, hue/sat preserved."""
    v = [c * e for c in rgb]
    m = max(v)
    if m > cap:
        v = [c * cap / m for c in v]
    return tuple(int(round(c)) for c in v)


GROUND = _albedo(_INSITU["ground"])      # (95, 51, 36)
RED = _albedo(_INSITU["red"])            # (209, 57, 35)
ORANGE = _albedo(_INSITU["orange"])      # (229, 103, 32)
GOLD = _albedo(_INSITU["gold"])          # (246, 174, 47)
STRIP = _albedo(_INSITU["strip"])        # chrome yellow of the menu strips
PALE = (252, 226, 158)     # the cream petal-dots: the head's brightest ring
DISC = (250, 196, 60)      # inner gold disc
INK = (44, 40, 15)         # strip lettering, from sRGB (55,51,19) darkened
PINK = (232, 126, 132)     # pink in the torta / ceviche vignettes
GREEN = (108, 148, 62)     # garnish

# ---------------------------------------------------- measured, ref_rear34
SIGN_ASPECT = 1.832                 # front lid board 2.034 m x 1.110 m
SIGN_CREAM = (237, 227, 205)
SIGN_RED = (176, 46, 38)
SIGN_OUTLINE = (64, 42, 34)
SIGN_EDGE = (238, 190, 40)          # the yellow pinstripe on the panel edge

SIGN_BASE_UV = (0.2591, 0.4099)     # S's baseline origin, panel fractions
SIGN_SLOPE_UV = -1.460              # dv/du of the baseline, panel fractions
SIGN_XH_F = 0.174                   # x-height / panel height
SIGN_CAP_F = 0.288                  # capital S height / panel height
SIGN_DESC_F = 0.107                 # S descender below baseline / panel height
SIGN_STROKE_F = 0.0207              # thick stroke width / panel width
SIGN_PITCH_F = 0.02814              # stroke pitch / panel width
SIGN_STAR_UV = (0.2887, 0.0463)
SIGN_STAR_W_F = 0.0496              # / panel width
SIGN_STAR_H_F = 0.0667              # / panel height
SIGN_LA_UV = (0.1864, 0.4682)       # "La" baseline, left end
SIGN_LA_CAP_F = 0.138               # "La" cap height / panel height
SIGN_TOP_SHIFT = 0.116              # the one stated deviation, / panel height

W, H = 2048, int(round(2048 / BOARD_ASPECT))          # 2048 x 1231
SW, SH = 1832, int(round(1832 / SIGN_ASPECT))         # 1832 x 1000


# --------------------------------------------------------------- primitives
def _scallop(d, cx, cy, r, lobes, fill, phase=0.0, lobe=0.30):
    """A scalloped ring: `lobes` round lobes on a circle, plus the core disc.

    The photograph's rings are ROUND-lobed (out/M10_h2.png), so the lobes are
    overlapping discs, not a sinusoidal radius.
    """
    # lobe radius scaled to the lobe pitch so adjacent lobes just kiss
    rl = r * math.sin(math.pi / lobes) * lobe
    rc = r - rl
    for k in range(lobes):
        a = phase + 2 * math.pi * k / lobes
        px, py = cx + rc * math.cos(a), cy + rc * math.sin(a)
        d.ellipse([px - rl, py - rl, px + rl, py + rl], fill=fill)
    d.ellipse([cx - rc, cy - rc, cx + rc, cy + rc], fill=fill)


def _peace(d, cx, cy, r, fill):
    w = max(2, int(r * 0.22))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=fill, width=w)
    d.line([(cx, cy - r), (cx, cy + r)], fill=fill, width=w)
    for s in (-1, 1):
        d.line([(cx, cy), (cx + s * r * 0.71, cy + r * 0.71)], fill=fill,
               width=w)


def flower(d, cx, cy, R, phase=0.0):
    """One head, ring radii and lobe counts per the radial profile (header A)."""
    _scallop(d, cx, cy, R, N_LOBE_RED, RED, phase, 1.15)
    _scallop(d, cx, cy, R * 0.80, N_LOBE_RED, ORANGE, phase, 1.15)
    # ring of eight fat pale petal-dots at 0.58 R, on a gold scalloped ring
    _scallop(d, cx, cy, R * 0.62, N_DOT, GOLD, phase + math.pi / N_DOT, 1.25)
    for k in range(N_DOT):
        a = phase + math.pi / N_DOT + 2 * math.pi * k / N_DOT
        px, py = cx + R * 0.58 * math.cos(a), cy + R * 0.58 * math.sin(a)
        d.ellipse([px - R * 0.130, py - R * 0.130,
                   px + R * 0.130, py + R * 0.130], fill=PALE)
    d.ellipse([cx - R * 0.42, cy - R * 0.42, cx + R * 0.42, cy + R * 0.42],
              fill=GOLD)
    d.ellipse([cx - R * 0.38, cy - R * 0.38, cx + R * 0.38, cy + R * 0.38],
              outline=ORANGE, width=max(2, int(R * 0.045)))
    d.ellipse([cx - R * 0.34, cy - R * 0.34, cx + R * 0.34, cy + R * 0.34],
              fill=DISC)
    d.ellipse([cx - R * 0.20, cy - R * 0.20, cx + R * 0.20, cy + R * 0.20],
              fill=GOLD)
    _peace(d, cx, cy, R * 0.115, PALE)


def _ribbon(d, pts, w0, w1, fill, round_end=True):
    """A tapered stroke through a polyline: the brush model used throughout."""
    n = len(pts)
    if n < 2:
        return
    left, right = [], []
    for i in range(n):
        ax, ay = pts[i]
        bx, by = pts[min(i + 1, n - 1)]
        cx_, cy_ = pts[max(i - 1, 0)]
        dx, dy = bx - cx_, by - cy_
        L = math.hypot(dx, dy) or 1.0
        t = i / (n - 1)
        w = (w0 + (w1 - w0) * t) * 0.5
        nx, ny = -dy / L * w, dx / L * w
        left.append((ax + nx, ay + ny))
        right.append((ax - nx, ay - ny))
    d.polygon(left + right[::-1], fill=fill)
    if round_end:
        for (x, y), w in ((pts[0], w0), (pts[-1], w1)):
            r = w * 0.5
            d.ellipse([x - r, y - r, x + r, y + r], fill=fill)


def _tendril(d, x0, y0, s, fill, flip=1, turns=2.6, w0=0.22, phase=0.0):
    """Calligraphic paisley tendril: a spiral of decreasing width, rolled end."""
    n = 56
    pts, w = [], []
    for i in range(n):
        t = turns * math.pi * i / (n - 1)
        rr = s * (0.16 + 0.055 * t)
        pts.append((x0 + flip * rr * math.cos(t + phase),
                    y0 + rr * math.sin(t + phase)))
        w.append(s * w0 * (1.0 - 0.70 * i / (n - 1)))
    _ribbon(d, pts, w[0], w[-1], fill)


def _leaf(d, x, y, L, ang, fill=GOLD):
    pts = []
    for t in np.linspace(0, 2 * math.pi, 26):
        u, v = L * math.cos(t), L * 0.30 * math.sin(t)
        pts.append((x + u * math.cos(ang) - v * math.sin(ang),
                    y + u * math.sin(ang) + v * math.cos(ang)))
    d.polygon(pts, fill=fill)


def _star(d, cx, cy, rx, ry, fill=INK, rot=-math.pi / 2):
    pts = []
    for k in range(10):
        a = rot + math.pi * k / 5
        f = 1.0 if k % 2 == 0 else 0.42
        pts.append((cx + rx * f * math.cos(a), cy + ry * f * math.sin(a)))
    d.polygon(pts, fill=fill)


def _font(sz):
    """A face for the MENU-STRIP CAPS only.

    The strips carry printed-looking black slab caps, so a face is right there.
    The script on the other board loads no face at all -- see the brush model
    further down; that was rev 8's defect.
    """
    from PIL import ImageFont
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, sz)
            except Exception:
                pass
    return ImageFont.load_default()


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


# ------------------------------------------------------------------ mural
# Ground-fill density and colour split.  These are the two knobs that were
# turned until the achieved class fractions matched the photograph; the
# achieved-vs-target table is in the report and is reproduced by
# lid_gen.audit_mural().
N_TENDRIL = 395
TENDRIL_MIX = (0.32, 0.52, 0.16)   # red : orange : gold, by draw count


def mural(path=None):
    im = Image.new("RGB", (W, H), GROUND)
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(1963)

    sw = int(round(W * STRIP_SIDE_F))
    th = int(round(H * STRIP_TOP_F))
    Wi, Hi = W - 2 * sw, H - th                 # rectified interior
    ox, oy = sw, th                             # interior origin

    R = HEAD_R_F * Wi
    heads = [(ox + u * Wi, oy + v * Hi, R) for (u, v) in HEADS_UV]

    # --- stems first, orange, near-vertical, head -> bottom edge
    for (hx, hy, r) in heads:
        lean = (hx - W / 2) / (W / 2) * 0.035 * Hi
        _ribbon(d, [(hx, hy), (hx + lean * 0.5, hy + (H - hy) * 0.5),
                    (hx + lean, H)],
                STEM_W_F * Wi * 1.10, STEM_W_F * Wi * 0.95, ORANGE)

    # --- gold almond leaves off the stems
    for j, (hx, hy, r) in enumerate(heads):
        for k, f in enumerate((0.34, 0.58, 0.80)):
            yy = hy + (H - hy) * f
            s = 1 if (j + k) % 2 else -1
            _leaf(d, hx + s * r * 0.34, yy, r * 0.32, s * 0.95)

    # --- dense calligraphic tendrils, gold + orange + red, over the ground
    cols = ([RED] * int(round(TENDRIL_MIX[0] * 100))
            + [ORANGE] * int(round(TENDRIL_MIX[1] * 100))
            + [GOLD] * int(round(TENDRIL_MIX[2] * 100)))
    for i in range(N_TENDRIL):
        _tendril(d,
                 float(rng.integers(ox - int(0.05 * Wi), ox + Wi + int(0.05 * Wi))),
                 float(rng.integers(oy - int(0.02 * Hi), H)),
                 float(rng.integers(int(0.038 * Wi), int(0.082 * Wi))),
                 cols[int(rng.integers(0, len(cols)))],
                 flip=1 if rng.random() < 0.5 else -1,
                 turns=1.25 + 1.15 * rng.random(),
                 w0=0.30 + 0.16 * rng.random(),
                 phase=2 * math.pi * rng.random())

    # --- heads last, over the fill
    for i, (hx, hy, r) in enumerate(heads):
        flower(d, hx, hy, r, phase=0.21 * i)

    im = im.filter(ImageFilter.GaussianBlur(0.7))
    d = ImageDraw.Draw(im)

    # --- menu strips: left, top, right.  NO bottom strip (measured).
    d.rectangle([0, 0, sw, H], fill=STRIP)
    d.rectangle([W - sw, 0, W, H], fill=STRIP)
    d.rectangle([0, 0, W, th], fill=STRIP)
    d.rectangle([0, H - 5, W, H], fill=(52, 30, 22))     # dark bottom trim

    # top strip: one line of black slab caps between two stars, sitting
    # BETWEEN the two corner blocks (measured: the caps start clear of them)
    tw = int(W * 0.62)
    d.text((W * 0.5, th * 0.50), "FRESH JUICES,  GOURMET TACOS  &  TORTAS",
           font=_font(int(th * 0.46)), fill=INK, anchor="mm")
    _star(d, int(W * 0.5 - tw * 0.52), th // 2, th * 0.24, th * 0.24)
    _star(d, int(W * 0.5 + tw * 0.52), th // 2, th * 0.24, th * 0.24)

    # side strips: HORIZONTAL words stacked down the strip, interleaved with
    # painted food vignettes.  Measured on the rectified strip
    # (out/M12_leftstrip_rect.png): cap height 0.21 of strip width, each word
    # set to fill about 0.90 of the strip width, vignettes ~0.10 of the
    # interior height tall.  Sequence read top to bottom off both strips.
    seq = [("v", _vig_tacos), ("t", "GOURMET"), ("t", "TACOS"), ("t", "&"),
           ("t", "TORTAS"), ("v", _vig_torta), ("t", "FRESH"),
           ("v", _vig_juice), ("t", "JUICES"), ("t", "CEVICHE"),
           ("t", "TOSTADAS"), ("v", _vig_ceviche), ("t", "SHRIMP"),
           ("t", "& FISH"), ("t", "TACOS")]
    cap = sw * 0.21
    for side_x in (sw * 0.5, W - sw * 0.5):
        y = th + Hi * 0.020
        for kind, val in seq:
            if kind == "v":
                val(d, side_x, y + Hi * 0.045, sw * 0.36)
                y += Hi * 0.098
            else:
                f = _font(int(cap / 0.73))
                wpx = d.textlength(val, font=f)
                if wpx > sw * 0.90:
                    f = _font(max(8, int(cap / 0.73 * sw * 0.90 / wpx)))
                d.text((side_x, y + cap * 0.6), val, font=f, fill=INK,
                       anchor="mm")
                y += cap * 1.62
            if y > H - Hi * 0.03:
                break

    im = im.filter(ImageFilter.GaussianBlur(0.45))
    p = path or os.path.join(TEXDIR, "lidmural.png")
    im.save(p)
    return p


# ------------------------------------------------------------- brush script
# The glyph skeletons below are polylines in a normalised letter box:
#   x runs 0 -> 1 across one advance, y runs 0 at the baseline to -1 at the
#   x-height, +ve downward.  Widths are fractions of the stroke width.
# They are a brush model, not a font: no system typeface is loaded, every
# metric that scales them (x-height, cap height, stroke width, pitch, slant,
# baseline rise, descender depth) came off the photograph.

def _bez(p0, p1, p2, p3, n=40):
    out = []
    for i in range(n):
        t = i / (n - 1)
        m = 1 - t
        out.append((m ** 3 * p0[0] + 3 * m * m * t * p1[0]
                    + 3 * m * t * t * p2[0] + t ** 3 * p3[0],
                    m ** 3 * p0[1] + 3 * m * m * t * p1[1]
                    + 3 * m * t * t * p2[1] + t ** 3 * p3[1]))
    return out


def _glyph_S():
    """Capital S.  y is in CAP heights here: -1.0 is the S's own top, +0.37
    the measured descender depth (0.107 / 0.288 of the panel height).

    Shape read off out/L5_S_20x.png: a tight spiral eye at the top left, a
    full bowl, and a tail that sweeps back down-LEFT past the S's own start
    and finishes in a taper.
    """
    return [
        # entry: thin hairline sweeping right-to-left into the spiral eye
        (_bez((0.94, -0.82), (0.64, -1.04), (0.16, -1.00), (0.12, -0.74)),
         0.16, 0.60),
        # the eye closes back on itself
        (_bez((0.12, -0.74), (0.10, -0.52), (0.46, -0.50), (0.60, -0.64)),
         0.60, 0.90),
        # spine: down through the waist, thickening
        (_bez((0.60, -0.64), (0.74, -0.46), (0.36, -0.38), (0.26, -0.20)),
         0.90, 1.25),
        # lower bowl
        (_bez((0.26, -0.20), (0.18, 0.04), (0.62, 0.12), (0.80, -0.08)),
         1.25, 0.55),
        # tail: back down-LEFT, past the S's own start, tapering out.  The
        # end point is the measured descender terminal, u 0.2164 / v 0.5216.
        (_bez((0.34, -0.16), (0.16, 0.08), (-0.20, 0.11), (-0.48, 0.145)),
         1.05, 0.10),
    ]


def _glyph_a():
    return [
        (_bez((0.86, -0.86), (0.52, -1.10), (0.10, -0.86), (0.16, -0.44)),
         0.30, 0.95),
        (_bez((0.16, -0.44), (0.20, -0.06), (0.66, -0.04), (0.78, -0.34)),
         0.95, 0.70),
        (_bez((0.80, -0.94), (0.80, -0.60), (0.78, -0.28), (0.90, -0.02)),
         0.70, 1.00),
    ]


def _glyph_n():
    return [
        (_bez((0.06, -0.86), (0.10, -0.50), (0.10, -0.24), (0.14, -0.02)),
         0.85, 1.00),
        (_bez((0.10, -0.62), (0.24, -0.96), (0.66, -0.98), (0.72, -0.60)),
         0.26, 0.60),
        (_bez((0.72, -0.60), (0.74, -0.36), (0.74, -0.20), (0.80, -0.02)),
         0.60, 1.00),
    ]


def _glyph_t():
    return [
        (_bez((0.30, -1.14), (0.28, -0.84), (0.26, -0.42), (0.34, -0.02)),
         0.42, 0.95),
        (_bez((-0.06, -0.86), (0.20, -0.90), (0.50, -0.90), (0.72, -0.86)),
         0.30, 0.30),
    ]


def _glyph_L_small():
    return [
        (_bez((0.42, -1.00), (0.30, -0.66), (0.24, -0.30), (0.26, -0.02)),
         0.40, 0.85),
        (_bez((0.26, -0.02), (0.36, 0.12), (0.62, 0.10), (0.80, -0.02)),
         0.85, 0.30),
    ]


def _glyph_a_small():
    return _glyph_a()


def _draw_word(d, glyphs, origin, along, up, xh, sw_, pitch, outline_w):
    """Place glyph skeletons on a climbing baseline with an upright letter axis.

    `along` steps the pen down the baseline; `up` is the panel's own vertical
    (the measured letter axis), NOT the baseline normal -- that separation is
    the whole point of this signboard's layout.
    """
    pen = np.array(origin, float)
    al = np.array(along, float)
    uv = np.array(up, float)
    for g, adv in glyphs:
        for pts, w0, w1 in g:
            path = []
            for (gx, gy) in pts:
                p = pen + al * (gx * adv * pitch) + uv * (gy * xh)
                path.append((p[0], p[1]))
            _ribbon(d, path, sw_ * w0 + outline_w, sw_ * w1 + outline_w,
                    SIGN_OUTLINE)
        pen = pen + al * (adv * pitch)
    pen = np.array(origin, float)
    for g, adv in glyphs:
        for pts, w0, w1 in g:
            path = []
            for (gx, gy) in pts:
                p = pen + al * (gx * adv * pitch) + uv * (gy * xh)
                path.append((p[0], p[1]))
            _ribbon(d, path, max(1.0, sw_ * w0 - outline_w * 0.15),
                    max(1.0, sw_ * w1 - outline_w * 0.15), SIGN_RED)
        pen = pen + al * (adv * pitch)


def front_sign(path=None):
    """The lettered cream panel: red brush script climbing, with the red star.

    Reproduced from ref_rear34.jpg.  See header B for what is measured and
    what is not.  Nothing here loads a typeface.
    """
    im = Image.new("RGB", (SW, SH), SIGN_CREAM)
    d = ImageDraw.Draw(im)

    # the yellow pinstripe measured along the panel's top edge
    d.rectangle([0, 0, SW, int(SH * 0.010)], fill=SIGN_EDGE)

    xh = SIGN_XH_F * SH
    cap = SIGN_CAP_F * SH
    sw_ = SIGN_STROKE_F * SW
    pitch = SIGN_PITCH_F * SW
    outline_w = sw_ * 0.42

    # baseline direction in texture pixels, from the measured panel-fraction
    # slope; the letter axis is the panel's vertical, tilted by the measured
    # 6.5 deg forward slant.
    slope_px = SIGN_SLOPE_UV * SH / SW
    along = np.array([1.0, slope_px])
    along /= np.hypot(*along)
    # `up` is applied as uv * gy with gy = 0 on the baseline and -1 at the
    # x-height, so it must point DOWN-left for the letters to stand up and
    # lean forward by the measured 6.5 deg.
    slant = math.radians(6.5)
    up = np.array([-math.sin(slant), math.cos(slant)])

    shift = SIGN_TOP_SHIFT * SH        # the one stated deviation, header B
    ox = SIGN_BASE_UV[0] * SW
    oy = SIGN_BASE_UV[1] * SH + shift

    # ---- the big S, at its own (capital) scale
    s_adv = pitch * 3.05                  # S width 0.103 of panel width
    s_org = np.array([ox, oy]) - along * (s_adv * 0.42)
    _draw_word(d, [(_glyph_S(), 1.0)], tuple(s_org), along, up,
               cap, sw_ * 1.30, s_adv, outline_w * 1.30)

    # ---- the seven downstrokes after the S.  Reconstructed, not read: see B.
    after = [(_glyph_a(), 1.00), (_glyph_n(), 1.06), (_glyph_t(), 0.72),
             (_glyph_a(), 1.00)]
    start = s_org + along * (s_adv * 1.00)
    _draw_word(d, after, start, along, up, xh, sw_, pitch * 2.28, outline_w)

    # ---- "La", small, on its own lower baseline
    la_x = SIGN_LA_UV[0] * SW
    la_y = SIGN_LA_UV[1] * SH + shift
    la_xh = SIGN_LA_CAP_F * SH
    _draw_word(d, [(_glyph_L_small(), 1.0), (_glyph_a_small(), 0.95)],
               (la_x, la_y), along, up, la_xh, sw_ * 0.72, pitch * 1.55,
               outline_w * 0.72)

    # ---- the red star over the S
    st_x = SIGN_STAR_UV[0] * SW
    st_y = SIGN_STAR_UV[1] * SH + shift
    _star(d, st_x, st_y, SIGN_STAR_W_F * SW * 0.53, SIGN_STAR_H_F * SH * 0.53,
          fill=SIGN_RED)

    im = im.filter(ImageFilter.GaussianBlur(0.6))
    p = path or os.path.join(TEXDIR, "lidsign.png")
    im.save(p)
    return p


# rev 8 called this rear_sign().  The panel is on the FRONT lid (header C);
# the old name is kept so nothing outside this file breaks.
rear_sign = front_sign


# ------------------------------------------------------------------- audit
def audit_sign(path=None):
    """Score the written sign panel against the measured panel fractions.

    Targets are the ref_rear34 measurements with SIGN_TOP_SHIFT added to every
    v, since that shift is the one stated deviation (header B).  The word's
    TOP is not a target: the shift is defined by it landing on the panel edge.
    """
    from scipy import ndimage as ndi
    p = path or os.path.join(TEXDIR, "lidsign.png")
    im = Image.open(p).convert("RGB")
    a = np.asarray(im).astype(float)
    sw, sh = im.size
    lum = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    ink = lum < 170
    ink[:int(sh * 0.02)] = False           # the yellow edge pinstripe
    ys, xs = np.nonzero(ink)
    lab, n = ndi.label(ink)
    sz = ndi.sum(ink, lab, range(1, n + 1))
    star = np.argsort(sz)[::-1][2] + 1     # 3rd largest blob is the star
    sy, sx = np.nonzero(lab == star)
    got = {"u_lo": xs.min() / sw, "u_hi": xs.max() / sw,
           "v_desc": ys.max() / sh, "v_top": ys.min() / sh,
           "star_u": (sx.min() + sx.max()) / 2 / sw,
           "star_v": (sy.min() + sy.max()) / 2 / sh,
           "star_w": (sx.max() - sx.min()) / sw,
           "star_h": (sy.max() - sy.min()) / sh}
    tgt = {"u_lo": 0.174, "u_hi": 0.519,
           "v_desc": 0.5216 + SIGN_TOP_SHIFT, "v_top": float("nan"),
           "star_u": SIGN_STAR_UV[0], "star_v": SIGN_STAR_UV[1] + SIGN_TOP_SHIFT,
           "star_w": SIGN_STAR_W_F, "star_h": SIGN_STAR_H_F}
    return got, tgt


def audit_mural(path=None):
    """Score the written mural against the photograph, same classifier.

    The photograph's classes use HSV V < 0.30 for the dark ground; the texture
    is an albedo lifted by EXPOSURE, so the threshold is lifted by the same
    factor.  Returns (achieved, target) dicts of percentages.
    """
    p = path or os.path.join(TEXDIR, "lidmural.png")
    im = Image.open(p).convert("RGB")
    a = np.asarray(im).astype(float)
    hsv = np.asarray(im.convert("HSV")).astype(float)
    hh = hsv[..., 0] * 360 / 255.0
    v = hsv[..., 2] / 255.0
    sw = int(round(im.width * STRIP_SIDE_F))
    th = int(round(im.height * STRIP_TOP_F))
    sl = np.s_[th:im.height - 5, sw:im.width - sw]
    hh, v, a = hh[sl], v[sl], a[sl]
    dark = v < 0.30 * EXPOSURE
    red = (~dark) & ((hh < 14) | (hh >= 345))
    orn = (~dark) & (hh >= 14) & (hh < 30)
    yel = (~dark) & (hh >= 30) & (hh < 62)
    got = {"dark": 100 * dark.mean(), "red": 100 * red.mean(),
           "orange": 100 * orn.mean(), "yellow": 100 * yel.mean(),
           "meanV": v.mean(), "medV": float(np.median(v)),
           "meanRGB": tuple(np.round(a.reshape(-1, 3).mean(0), 1))}
    tgt = {"dark": 21.82, "red": 25.31, "orange": 32.53, "yellow": 20.33,
           "meanV": 0.490 * EXPOSURE, "medV": 0.537 * EXPOSURE,
           "meanRGB": tuple(np.round(np.array((125.4, 59.7, 23.0))
                                     * EXPOSURE, 1))}
    return got, tgt


if __name__ == "__main__":
    print(mural())
    print(front_sign())
    g, t = audit_mural()
    print("MURAL  (interior, classifier of header A, dark threshold x %.2f)"
          % EXPOSURE)
    for k in ("dark", "red", "orange", "yellow"):
        print("  %-7s achieved %5.2f %%   target %5.2f %%   d %+5.2f"
              % (k, g[k], t[k], g[k] - t[k]))
    print("  meanV   achieved %.3f       target %.3f" % (g["meanV"], t["meanV"]))
    print("  meanRGB achieved %s  target %s" % (g["meanRGB"], t["meanRGB"]))
    gs, ts = audit_sign()
    print("SIGN   (panel fractions; v targets include the stated %.3f shift)"
          % SIGN_TOP_SHIFT)
    for k in ("u_lo", "u_hi", "v_desc", "star_u", "star_v", "star_w", "star_h"):
        print("  %-7s achieved %.4f   target %.4f   d %+.4f"
              % (k, gs[k], ts[k], gs[k] - ts[k]))
    print("  v_top   achieved %.4f   (not a target: the shift is defined by it)"
          % gs["v_top"])
