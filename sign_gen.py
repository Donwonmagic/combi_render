"""
sign_gen.py -- "Senor Tacombi" side-panel signwriting.

Silver hand-painted script with a dark keyline, laid out as a two-line lockup:
a small raised "Senor" over a large "Tacombi" whose capital T is an ORNATE
SWASH built from tapered brush strokes (arcing crossbar with curled terminals,
S-curved stem, sweeping foot flourish).  See SPEC.md sec.3.
"""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from texgen import dilate_disc                       # numpy disc dilation

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, "tex")
SCRIPT_FONT = ("/root/.claude/skills/canvas-design/canvas-fonts/"
               "NothingYouCouldDo-Regular.ttf")
FALLBACK = ("/root/.claude/skills/canvas-design/canvas-fonts/"
            "IBMPlexSerif-Italic.ttf")

OUT_W, OUT_H = 4096, 890
SS = 2
W, H = OUT_W * SS, OUT_H * SS

SILVER_HI = (250, 251, 250)
SILVER_MID = (211, 213, 212)
SILVER_LO = (152, 156, 155)
KEYLINE = (46, 44, 46)


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
               (tx - 0.575, ty + 0.360 * hc) if False else
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


# ------------------------------------------------------------------- helpers
def ink_bbox(mask):
    ys, xs = np.nonzero(mask)
    return xs.min(), ys.min(), xs.max(), ys.max()


def render_text(text, font, canvas=(W, H), pos=None):
    img = Image.new("L", canvas, 0)
    d = ImageDraw.Draw(img)
    d.text(pos or (canvas[0] // 2, canvas[1] // 2), text, font=font,
           fill=255, anchor="mm")
    return np.asarray(img) > 127


def shift(mask, dx, dy):
    out = np.zeros_like(mask)
    h, w = mask.shape
    sx0, sx1 = max(0, -dx), min(w, w - dx)
    dx0, dx1 = max(0, dx), min(w, w + dx)
    sy0, sy1 = max(0, -dy), min(h, h - dy)
    dy0, dy1 = max(0, dy), min(h, h + dy)
    out[dy0:dy1, dx0:dx1] = mask[sy0:sy1, sx0:sx1]
    return out


def main():
    os.makedirs(TEX, exist_ok=True)
    fp = SCRIPT_FONT if os.path.exists(SCRIPT_FONT) else FALLBACK

    # ---- metrics: cap height per font unit --------------------------------
    REF = 200
    fref = ImageFont.truetype(fp, REF)
    capm = render_text("T", fref, (REF * 6, REF * 4), (REF * 3, REF * 2))
    cy0, _, cy1, _ = ink_bbox(capm)[1], 0, ink_bbox(capm)[3], 0
    c1 = (ink_bbox(capm)[3] - ink_bbox(capm)[1] + 1) / REF

    HC = 0.330 * H                       # cap height of the big line
    size = int(HC / c1)
    font_big = ImageFont.truetype(fp, size)
    font_sm = ImageFont.truetype(fp, int(size * 0.500))

    # ---- "acombi" (the T is drawn by hand) --------------------------------
    m_ac = render_text("acombi", font_big, (W, H), (W // 2, H // 2))
    x0, y0, x1, y1 = ink_bbox(m_ac)
    tgt_left, tgt_bottom = int(0.400 * W), int(0.870 * H)
    m_ac = shift(m_ac, tgt_left - x0, tgt_bottom - y1)
    ax0, ay0, ax1, ay1 = ink_bbox(m_ac)

    # ---- ornate swash T ---------------------------------------------------
    strokes = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(strokes)
    t_base = ay1                                  # share the baseline
    swash_T(sd, tgt_left - 0.16 * HC, t_base - HC, HC)
    m_T = np.asarray(strokes) > 127

    # ---- small raised "Senor" --------------------------------------------
    m_sn = render_text("Señor", font_sm, (W, H), (W // 2, H // 2))
    sx0, sy0, sx1, sy1 = ink_bbox(m_sn)
    m_sn = shift(m_sn, int(0.285 * W) - sx0, int(0.315 * H) - sy1)

    # ---- assemble ---------------------------------------------------------
    letters = m_ac | m_T | m_sn
    letters = dilate_disc(letters, max(1, int(0.014 * HC)))
    key = dilate_disc(letters, max(2, int(0.030 * HC)))
    shadow = dilate_disc(shift(key, int(0.020 * HC), int(0.026 * HC)),
                         int(0.010 * HC))

    arr = np.zeros((H, W, 4), np.uint8)
    arr[shadow] = (28, 12, 10, 150)
    arr[key] = KEYLINE + (255,)

    # silver: vertical gradient + a bright band across the upper third
    ys, xs = np.nonzero(letters)
    if len(ys):
        ly0, ly1 = ys.min(), ys.max()
        t = (ys - ly0) / max(1, (ly1 - ly0))
        band = np.exp(-((t - 0.26) / 0.17) ** 2)
        lo = np.array(SILVER_LO, float)
        mid = np.array(SILVER_MID, float)
        hi = np.array(SILVER_HI, float)
        col = mid[None, :] + (lo - mid)[None, :] * np.clip(
            (t - 0.55) / 0.45, 0, 1)[:, None]
        col = col + (hi - col) * band[:, None]
        # faint brush striations
        col += (np.sin(xs / 26.0) * 4 + np.cos(ys / 19.0) * 3)[:, None]
        arr[ys, xs, :3] = np.clip(col, 0, 255).astype(np.uint8)
        arr[ys, xs, 3] = 255

    img = Image.fromarray(arr, "RGBA")
    # un-premultiplied downsample to keep the keyline crisp
    out = img.resize((OUT_W, OUT_H), Image.LANCZOS)
    path = os.path.join(TEX, "senor.png")
    out.save(path)

    a = np.asarray(out)
    print("senor.png %dx%d  ink=%.4f  cap=%dpx  font=%s"
          % (out.size[0], out.size[1], (a[..., 3] > 127).mean(),
             int(HC / SS), os.path.basename(fp)))

    bg = Image.new("RGB", out.size, (152, 24, 18))
    bg.paste(out, (0, 0), out)
    bg.save(os.path.join(TEX, "prev_senor.png"))
    return path


if __name__ == "__main__":
    main()
