"""
sign_gen.py -- "Senor Tacombi" side-panel signwriting.

Silver hand-painted script with a dark keyline and a drop shadow, laid out as
a two-line lockup: a small raised "Senor" over a large "Tacombi" whose capital
T is an ORNATE SWASH built from tapered brush strokes (arcing crossbar with
curled terminals, S-curved stem, sweeping foot flourish), with decorative
SPIRALS set inside the counters of a / c / o / m / b.  See SPEC.md sec.3.

FRAME / FIT.  This file is the texture half of a two-part fit; the other half
is the decal panel in build.py step 8.

    MEASURED in ref_side.jpg the lockup occupies
        X  +0.784 ... -0.494   (1.278 m)
        Z   0.445 ...  0.918   un-dropped   (0.380 ... 0.853 above ground)
        ->  aspect ratio 1.278 / 0.473 = 2.7019

    The shipped senor.png was 4096 x 890 (4.602:1) with an alpha bounding box
    of only 1838 x 716 -- the ink filled 44.9 % of the panel's width and
    80.4 % of its height, so a panel sized to the measured lockup rendered
    a script 0.574 m wide instead of 1.278 m, and 0.4 m too high.  The fix
    is HERE, not in the panel: the image is now cropped tight to its own ink
    and emitted at exactly the measured aspect ratio, so "panel extent" and
    "ink extent" are the same rectangle.  OUT_AR below and the SCR dict in
    build.py must agree; if you change one, change the other.
"""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from texgen import dilate_disc                       # numpy disc dilation

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, "tex")

# The font roots differ between the build box and the render box; probe all of
# them rather than hard-coding one and silently falling through to a serif.
FONT_ROOTS = [
    "/root/.claude/skills/canvas-design/canvas-fonts",
    os.path.expanduser("~/.claude/skills/canvas-design/canvas-fonts"),
    "/sessions/dazzling-sharp-cori/mnt/.claude/skills/canvas-design/canvas-fonts",
    os.path.join(HERE, "fonts"),
]
SCRIPT_FONT = "NothingYouCouldDo-Regular.ttf"
FALLBACK = "IBMPlexSerif-Italic.ttf"

# ---- output ---------------------------------------------------------------
# measured panel 1.278 m x 0.473 m
OUT_AR = 1.278 / 0.473                                # 2.70190...
OUT_H = 1000
OUT_W = int(round(OUT_H * OUT_AR))                    # 2702, AR 2.7020

# ---- working canvas -------------------------------------------------------
# generous margin on every side so the keyline and the drop shadow are never
# clipped; the whole thing is cropped to the ink bounding box at the end, so
# the canvas size only sets the supersampling ratio (~1.6x here).
W, H = 5600, 2400
HC = 700.0                    # cap height of the big line, working px
AC_LEFT = 0.28 * W            # pen x of "acombi"
BASE_Y = 0.78 * H             # baseline of the big line
SEN_LEFT_HC = -1.604          # "Senor" pen x, in cap heights from AC_LEFT
SEN_GAP_HC = 0.682            # start value; solved for OUT_AR in main()
SMALL_RATIO = 0.500           # "Senor" size / "Tacombi" size

KEY_HC = 0.030                # keyline dilation, in cap heights
THICK_HC = 0.014              # stroke fattening
SHADOW_DX_HC, SHADOW_DY_HC = 0.020, 0.026

SILVER_HI = (250, 251, 250)
SILVER_MID = (211, 213, 212)
SILVER_LO = (152, 156, 155)
KEYLINE = (46, 44, 46)

TAU = math.pi * 2


def font_path(fname):
    for r in FONT_ROOTS:
        p = os.path.join(r, fname)
        try:
            if os.path.exists(p):
                return p
        except OSError:
            continue
    return None


# --------------------------------------------------------------------- strokes
def bez(p0, p1, p2, p3, n):
    t = np.linspace(0.0, 1.0, n)[:, None]
    u = 1.0 - t
    P = (u ** 3 * np.array(p0) + 3 * u ** 2 * t * np.array(p1)
         + 3 * u * t ** 2 * np.array(p2) + t ** 3 * np.array(p3))
    return P


def taper(n, keys):
    """radius profile: keys = [(t, r), ...] interpolated over 0..1"""
    t = np.linspace(0.0, 1.0, n)
    kt = np.array([k[0] for k in keys])
    kr = np.array([k[1] for k in keys])
    return np.interp(t, kt, kr)


def brush(drw, pts, radii):
    for (x, y), r in zip(pts, radii):
        if r < 0.45:
            r = 0.45
        drw.ellipse((x - r, y - r, x + r, y + r), fill=255)


def curve(drw, p0, p1, p2, p3, keys, hc):
    n = 520
    pts = bez(p0, p1, p2, p3, n)
    brush(drw, pts, taper(n, keys) * hc)
    return pts


# ----------------------------------------------------------------- swash "T"
def swash_T(drw, tx, ty, hc):
    """
    tx, ty = top-left anchor of the letter cell; hc = cap height.
    Stem descends from ty to ty+hc.
    """
    # 1. crossbar -- long arc, thick in the belly, hairline terminals
    curve(drw, (tx - 0.66 * hc, ty + 0.150 * hc),
               (tx - 0.20 * hc, ty - 0.085 * hc),
               (tx + 0.60 * hc, ty - 0.120 * hc),
               (tx + 1.22 * hc, ty + 0.045 * hc),
          [(0.00, 0.012), (0.14, 0.048), (0.38, 0.082), (0.62, 0.070),
           (0.85, 0.030), (1.00, 0.010)], hc)

    # 2. left terminal -- curls down and back on itself
    curve(drw, (tx - 0.66 * hc, ty + 0.150 * hc),
               (tx - 0.99 * hc, ty + 0.190 * hc),
               (tx - 1.03 * hc, ty + 0.500 * hc),
               (tx - 0.76 * hc, ty + 0.530 * hc),
          [(0.00, 0.012), (0.35, 0.030), (0.72, 0.024), (1.00, 0.009)], hc)
    curve(drw, (tx - 0.76 * hc, ty + 0.530 * hc),
               (tx - 0.58 * hc, ty + 0.545 * hc),
               (tx - 0.58 * hc, ty + 0.360 * hc),
               (tx - 0.74 * hc, ty + 0.345 * hc),
          [(0.00, 0.009), (0.45, 0.014), (1.00, 0.004)], hc)

    # 3. right terminal -- sweeps out, lifts, hooks back
    curve(drw, (tx + 1.22 * hc, ty + 0.045 * hc),
               (tx + 1.66 * hc, ty - 0.075 * hc),
               (tx + 1.92 * hc, ty + 0.195 * hc),
               (tx + 1.63 * hc, ty + 0.315 * hc),
          [(0.00, 0.010), (0.30, 0.030), (0.66, 0.026), (1.00, 0.007)], hc)
    curve(drw, (tx + 1.63 * hc, ty + 0.315 * hc),
               (tx + 1.45 * hc, ty + 0.360 * hc),
               (tx + 1.44 * hc, ty + 0.190 * hc),
               (tx + 1.60 * hc, ty + 0.170 * hc),
          [(0.00, 0.007), (0.5, 0.012), (1.00, 0.003)], hc)

    # 4. stem -- slight S, heavy at the shoulder, tapering to the foot
    curve(drw, (tx + 0.035 * hc, ty - 0.070 * hc),
               (tx + 0.085 * hc, ty + 0.320 * hc),
               (tx - 0.030 * hc, ty + 0.700 * hc),
               (tx - 0.105 * hc, ty + 0.990 * hc),
          [(0.00, 0.088), (0.28, 0.084), (0.62, 0.062), (0.88, 0.034),
           (1.00, 0.016)], hc)

    # 5. foot flourish -- sweeps left under the word and flicks up
    curve(drw, (tx - 0.105 * hc, ty + 0.990 * hc),
               (tx - 0.46 * hc, ty + 1.135 * hc),
               (tx - 1.00 * hc, ty + 1.045 * hc),
               (tx - 1.12 * hc, ty + 0.795 * hc),
          [(0.00, 0.016), (0.30, 0.030), (0.66, 0.024), (1.00, 0.007)], hc)
    curve(drw, (tx - 1.12 * hc, ty + 0.795 * hc),
               (tx - 1.20 * hc, ty + 0.640 * hc),
               (tx - 1.02 * hc, ty + 0.600 * hc),
               (tx - 0.94 * hc, ty + 0.690 * hc),
          [(0.00, 0.007), (0.5, 0.011), (1.00, 0.003)], hc)


# ------------------------------------------------------------ counter spirals
def spiral(drw, cx, cy, R, turns=2.15, hand=1.0, phase=0.0):
    """decorative curl: an Archimedean spiral run from a hairline eye outward"""
    n = 460
    t = np.linspace(0.0, 1.0, n)
    th = phase + TAU * turns * t * hand
    r = R * (0.05 + 0.95 * t)
    pts = np.stack([cx + r * np.cos(th), cy + r * np.sin(th)], 1)
    rad = R * (0.055 + 0.115 * t)
    brush(drw, pts, rad)


def chamfer_dt(free):
    """
    Distance (px) from every free pixel to the nearest occupied pixel.
    Two-pass 3x3 chamfer with weights (1, sqrt2): max error ~4 %, which is
    far inside the margin the spiral sizing already carries.  numpy only --
    texgen's contract for this project is PIL + numpy, no scipy.
    """
    A, B = 1.0, math.sqrt(2.0)
    INF = 1e8
    d = np.where(free, INF, 0.0)
    h, w = d.shape
    for y in range(1, h):
        row, prev = d[y], d[y - 1]
        np.minimum(row[1:], prev[:-1] + B, out=row[1:])
        np.minimum(row, prev + A, out=row)
        np.minimum(row[:-1], prev[1:] + B, out=row[:-1])
        for x in range(1, w):                       # left-to-right causal pass
            if row[x] > row[x - 1] + A:
                row[x] = row[x - 1] + A
    for y in range(h - 2, -1, -1):
        row, nxt = d[y], d[y + 1]
        np.minimum(row[:-1], nxt[1:] + B, out=row[:-1])
        np.minimum(row, nxt + A, out=row)
        np.minimum(row[1:], nxt[:-1] + B, out=row[1:])
        for x in range(w - 2, -1, -1):
            if row[x] > row[x + 1] + A:
                row[x] = row[x + 1] + A
    return d


PAD = 110          # px of context round a search window, >= any spiral radius


def counter_spirals(body, boxes, key_r):
    """
    body   : bool mask of the painted letter strokes (already fattened)
    boxes  : [(x0, x1, y0, y1, hand), ...] one search window per letter, in
             absolute canvas px; these are the letter's OWN ink bounding box
             inset, not its advance box -- this face leans, so the advance box
             misses the bowl by a third of a letter width.
    Returns a bool mask of curls, each guaranteed to clear the letter -- and
    its keyline -- by construction.  Sized off the widest free disc that fits
    inside the window, so a tight counter gets a smaller curl and an
    impossible one gets none.
    """
    h, w = body.shape
    img = Image.new("L", (w, h), 0)
    drw = ImageDraw.Draw(img)
    placed = []
    for (x0, x1, y0, y1, hand) in boxes:
        x0, x1 = int(max(0, x0)), int(min(w, x1))
        y0, y1 = int(max(0, y0)), int(min(h, y1))
        if x1 - x0 < 8 or y1 - y0 < 8:
            continue
        # distance transform over a PADDED window so ink just outside the
        # search rect still pushes the curl away; argmax over the rect only.
        px0, px1 = max(0, x0 - PAD), min(w, x1 + PAD)
        py0, py1 = max(0, y0 - PAD), min(h, y1 + PAD)
        d = chamfer_dt(~body[py0:py1, px0:px1])
        mask = np.zeros_like(d, dtype=bool)
        mask[y0 - py0:y1 - py0, x0 - px0:x1 - px0] = True
        d = np.where(mask, d, 0.0)
        iy, ix = np.unravel_index(np.argmax(d), d.shape)
        clear = float(d[iy, ix]) - key_r - 3.0        # keyline eats into it
        if clear < 14.0:
            continue
        R = 0.56 * clear
        cx, cy = px0 + ix, py0 + iy
        spiral(drw, cx, cy, R, hand=hand,
               phase=TAU * (0.13 + 0.37 * len(placed)))
        placed.append((cx, cy, R, float(d[iy, ix])))
    return (np.asarray(img) > 127), placed


# ------------------------------------------------------------------- helpers
def ink_bbox(mask):
    ys, xs = np.nonzero(mask)
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def shift(mask, dx, dy):
    out = np.zeros_like(mask)
    h, w = mask.shape
    sx0, sx1 = max(0, -dx), min(w, w - dx)
    dx0, dx1 = max(0, dx), min(w, w + dx)
    sy0, sy1 = max(0, -dy), min(h, h - dy)
    dy0, dy1 = max(0, dy), min(h, h + dy)
    out[dy0:dy1, dx0:dx1] = mask[sy0:sy1, sx0:sx1]
    return out


def _draw_text(text, font, xy, anchor):
    img = Image.new("L", (W, H), 0)
    ImageDraw.Draw(img).text(xy, text, font=font, fill=255, anchor=anchor)
    return np.asarray(img) > 127


# ------------------------------------------------------------------ compose
def compose(sen_gap_hc, fp, want_spirals=True):
    """Draw the whole lockup.  Returns (rgba_uint8, alpha_mask, info)."""
    ref = 200
    fref = ImageFont.truetype(fp, ref)
    tb = _draw_text("T", fref, (ref * 3, ref * 2), "mm")
    bx = ink_bbox(tb)
    cap_per_unit = (bx[3] - bx[1] + 1) / ref

    size = int(round(HC / cap_per_unit))
    font_big = ImageFont.truetype(fp, size)
    font_sm = ImageFont.truetype(fp, int(round(size * SMALL_RATIO)))
    meas = ImageDraw.Draw(Image.new("L", (8, 8), 0))

    # ---- "acombi" (the T is drawn by hand), pen on the baseline -----------
    word = "acombi"
    m_ac = _draw_text(word, font_big, (AC_LEFT, BASE_Y), "ls")
    base_y = ink_bbox(m_ac)[3]                       # no descenders in "acombi"

    # x-height band, measured off an "o" set on the same baseline
    m_o = _draw_text("o", font_big, (AC_LEFT, BASE_Y), "ls")
    ob = ink_bbox(m_o)
    xh_top, xh_bot = ob[1], ob[3]

    # ---- ornate swash T ---------------------------------------------------
    strokes = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(strokes)
    swash_T(sd, AC_LEFT - 0.16 * HC, base_y - HC, HC)
    m_T = np.asarray(strokes) > 127

    # ---- small raised "Senor" --------------------------------------------
    # drawn well inside the canvas first, then shifted -- setting it straight
    # at the target with anchor "ls" clipped the whole word off the top edge
    # and left two stray fragments behind.
    m_sn = _draw_text("Señor", font_sm, (0.10 * W, 0.55 * H), "ls")
    sb = ink_bbox(m_sn)
    sen_left = AC_LEFT + SEN_LEFT_HC * HC
    sen_bottom = (base_y - HC) - sen_gap_hc * HC
    m_sn = shift(m_sn, int(round(sen_left - sb[0])),
                 int(round(sen_bottom - sb[3])))

    # ---- assemble ---------------------------------------------------------
    thick = max(1, int(round(THICK_HC * HC)))
    key_r = max(2, int(round(KEY_HC * HC)))
    body = dilate_disc(m_ac | m_T | m_sn, thick)

    curls = np.zeros_like(body)
    placed = []
    if want_spirals:
        boxes, adv0 = [], 0.0
        xh = xh_bot - xh_top
        for i, ch in enumerate(word):
            adv1 = meas.textlength(word[:i + 1], font=font_big)
            if ch in "acomb":
                # the glyph's real ink box: set the single letter alone at the
                # pen position it occupies in the word.
                gm = _draw_text(ch, font_big, (AC_LEFT + adv0, BASE_Y), "ls")
                gb = ink_bbox(gm)
                gw, gh = gb[2] - gb[0], gb[3] - gb[1]
                boxes.append((gb[0] + 0.11 * gw, gb[2] - 0.11 * gw,
                              max(gb[1], xh_top) + 0.08 * xh,
                              min(gb[3], xh_bot) - 0.22 * xh,
                              1.0 if i % 2 == 0 else -1.0))
            adv0 = adv1
        curls, placed = counter_spirals(body, boxes, key_r)

    letters = body | curls
    # the keyline and the shadow follow the LETTERS only -- a hairline
    # ornament inside a counter is drawn straight onto the ground, which is
    # how a signwriter does it and which stops the keylines closing the
    # counter up into a dark blob.
    key = dilate_disc(body, key_r)
    shadow = dilate_disc(shift(key, int(SHADOW_DX_HC * HC),
                               int(SHADOW_DY_HC * HC)),
                         max(1, int(0.010 * HC)))

    arr = np.zeros((H, W, 4), np.uint8)
    arr[shadow] = (28, 12, 10, 150)
    arr[key] = KEYLINE + (255,)

    ys, xs = np.nonzero(letters)
    ly0, ly1 = ys.min(), ys.max()
    t = (ys - ly0) / max(1, (ly1 - ly0))
    band = np.exp(-((t - 0.26) / 0.17) ** 2)
    lo = np.array(SILVER_LO, float)
    mid = np.array(SILVER_MID, float)
    hi = np.array(SILVER_HI, float)
    col = mid[None, :] + (lo - mid)[None, :] * np.clip(
        (t - 0.55) / 0.45, 0, 1)[:, None]
    col = col + (hi - col) * band[:, None]
    col += (np.sin(xs / 26.0) * 4 + np.cos(ys / 19.0) * 3)[:, None]
    arr[ys, xs, :3] = np.clip(col, 0, 255).astype(np.uint8)
    arr[ys, xs, 3] = 255

    alpha = arr[..., 3] > 127
    info = dict(size=size, key_r=key_r, spirals=placed,
                cap_px=HC, base_y=base_y)
    return arr, alpha, info


def main():
    os.makedirs(TEX, exist_ok=True)
    fp = font_path(SCRIPT_FONT) or font_path(FALLBACK)
    if fp is None:
        raise SystemExit("sign_gen: no usable font found in %s" % FONT_ROOTS)

    # ---- solve the "Senor" raise for the measured aspect ratio ------------
    # The ink WIDTH is set by "Senor"'s S on the left and "acombi"'s i on the
    # right, neither of which moves with the raise; the ink HEIGHT moves with
    # it 1:1.  So the relation is exactly linear and one probe pass fixes it
    # -- no search, no distortion of any letterform.
    gap = SEN_GAP_HC
    arr, alpha, info = compose(gap, fp, want_spirals=False)
    x0, y0, x1, y1 = ink_bbox(alpha)
    w0, h0 = x1 - x0 + 1, y1 - y0 + 1
    h_want = w0 / OUT_AR
    gap = gap + (h_want - h0) / HC
    print("  solve: probe %d x %d (AR %.4f) -> raise %.4f -> %.4f cap heights"
          % (w0, h0, w0 / h0, SEN_GAP_HC, gap))

    arr, alpha, info = compose(gap, fp)
    x0, y0, x1, y1 = ink_bbox(alpha)
    w1, h1 = x1 - x0 + 1, y1 - y0 + 1
    print("  built: %d x %d  AR %.4f  (target %.4f, %+.2f %%)"
          % (w1, h1, w1 / h1, OUT_AR, 100.0 * (w1 / h1 / OUT_AR - 1.0)))
    for (cx, cy, R, d) in info["spirals"]:
        print("    spiral at (%d, %d)  R=%.0f px  clearance=%.0f px"
              % (cx, cy, R, d))

    # ---- crop tight to the ink, emit at exactly OUT_AR --------------------
    img = Image.fromarray(arr, "RGBA").crop((x0, y0, x1 + 1, y1 + 1))
    out = img.resize((OUT_W, OUT_H), Image.LANCZOS)
    path = os.path.join(TEX, "senor.png")
    out.save(path)

    a = np.asarray(out)
    m = a[..., 3] > 127
    bx = ink_bbox(m)
    print("senor.png %dx%d  AR %.4f  ink=%.4f  alpha bbox %s "
          "(margins L%d T%d R%d B%d px)  cap=%dpx  font=%s"
          % (out.size[0], out.size[1], out.size[0] / out.size[1], m.mean(),
             bx, bx[0], bx[1], OUT_W - 1 - bx[2], OUT_H - 1 - bx[3],
             int(round(HC * OUT_W / max(1, w1))), os.path.basename(fp)))

    bg = Image.new("RGB", out.size, (152, 24, 18))
    bg.paste(out, (0, 0), out)
    bg.save(os.path.join(TEX, "prev_senor.png"))
    return path


if __name__ == "__main__":
    main()
