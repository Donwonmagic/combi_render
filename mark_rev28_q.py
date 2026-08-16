"""mark_rev28_q.py -- rev 28, READ-ONLY on the references.

Re-asks the TWO questions rev 27 sent and never got answered, with EVERY crop
box printed on the image and to the console.

A crop I draw for him is a probe too.  Sixteen recorded instances
(SPEC 10.43 / 10.49 / 10.57 / 10.60 / 10.75 / 10.76).  rev 26's first draft put
box A on the green body ABOVE the tube it pointed at; rev 23's first draft
straddled the A-pillar.  Both were thrown away rather than sent.

BOX ROLE, stated per rev 28's standing requirement:
  Q1 boxes are POINTERS.  No number is taken from them.  The counter top is a
  DIAGONAL band 15-25 px deep, so SPEC 10.76 proved that any axis-aligned
  rectangle large enough to sample it must straddle -- the largest clean one is
  1060-1512 px against the 2700 that patch needed.  These are deliberately
  small and local, and their straddle indicator is printed anyway.
  Q2 boxes are the PSF estimator's own SAMPLING WINDOWS (probe_psf_workshop.py
  EDGE_NOTES, verbatim).  In this figure they serve as pointers to the edge
  inside each.  They are reproduced UNCHANGED so his answer maps 1:1 onto the
  probe's ROIs.

Both questions ask what a PHOTOGRAPH SHOWS.  Neither asks what the vehicle
looks like -- he has never stood in it.
"""
import os
from PIL import Image, ImageDraw, ImageFont

REAR = "ref_rear34.jpg"        # DC quantiser 1, 9.28 bits/px (SPEC 10.38)
WORK = "ref_workshop.jpg"      # DC quantiser 1, 8.87 bits/px (SPEC 10.38)

# ---------------------------------------------------------------- Q1 ------
# Counter top, ref_rear34.jpg.  Kept NARROW so each lies along the band rather
# than across it.  Clear of: the tin can and shaker (u < 640), the brass
# nosing on the outer edge, and the cream fascia above.
Q1_VIEW = (540, 380, 800, 500)
Q1_BOXES = [
    ("P1", (640, 420, 680, 435), "counter top, mid-run"),
    ("P2", (720, 445, 760, 465), "counter top, nearer the tail"),
]

# ---------------------------------------------------------------- Q2 ------
# VERBATIM from probe_psf_workshop.EDGE_NOTES.  Do not redraw these.
Q2_VIEW = (700, 220, 1000, 560)
Q2_BOXES = [
    ("E1", (880, 460, 940, 520), "fit rms 0.055 px  tilt -0.193   <- best fit"),
    ("E2", (880, 430, 940, 490), "fit rms 0.055 px  tilt -0.193"),
    ("E3", (850, 460, 910, 520), "fit rms 0.058 px  tilt -0.192"),
    ("E4", (730, 460, 790, 520), "fit rms 0.069 px  tilt +0.037"),
    ("E5", (850, 250, 910, 310), "fit rms 0.129 px  tilt +0.020"),
]

RED = (255, 45, 45)
CYAN = (60, 220, 255)


def font(sz, bold=True):
    for p in (("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
               if bold else
               "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def straddle(im, box):
    """Straddle INDICATOR, and it is deliberately TWO numbers.

    A raw luma spread cannot tell a straddle from an illumination gradient --
    and the counter top has a real gradient, so the raw number reads high with
    no contamination at all.  So: fit a PLANE in (u, v) by least squares and
    report the residual spread as well.  A gradient is absorbed by the plane;
    a material step is not.  This is the check-the-control-itself rule applied
    to a figure caption.

    Returns (raw_pct, resid_pct, median, lo, hi).  NOT a class test.
    """
    x0, y0, x1, y1 = box
    px = im.crop(box).convert("RGB").load()
    w, h = x1 - x0, y1 - y0
    pts = []
    for j in range(h):
        for i in range(w):
            r, g, b = px[i, j]
            pts.append((i, j, 0.2126 * r + 0.7152 * g + 0.0722 * b))
    n = len(pts)
    # least-squares plane  L = a*i + b*j + c   (normal equations, 3x3)
    Sii = sum(p[0] * p[0] for p in pts); Sij = sum(p[0] * p[1] for p in pts)
    Sjj = sum(p[1] * p[1] for p in pts); Si = sum(p[0] for p in pts)
    Sj = sum(p[1] for p in pts)
    Sli = sum(p[0] * p[2] for p in pts); Slj = sum(p[1] * p[2] for p in pts)
    Sl = sum(p[2] for p in pts)
    A = [[Sii, Sij, Si], [Sij, Sjj, Sj], [Si, Sj, float(n)]]
    y = [Sli, Slj, Sl]
    for k in range(3):                                   # Gaussian elimination
        pv = max(range(k, 3), key=lambda r: abs(A[r][k]))
        A[k], A[pv] = A[pv], A[k]; y[k], y[pv] = y[pv], y[k]
        for r in range(k + 1, 3):
            f = A[r][k] / A[k][k]
            for c in range(k, 3):
                A[r][c] -= f * A[k][c]
            y[r] -= f * y[k]
    co = [0.0, 0.0, 0.0]
    for k in (2, 1, 0):
        co[k] = (y[k] - sum(A[k][c] * co[c] for c in range(k + 1, 3))) / A[k][k]

    lum = sorted(p[2] for p in pts)
    med = lum[len(lum) // 2]
    raw = 100.0 * sum(1 for v in lum if abs(v - med) > 15) / n
    res = [p[2] - (co[0] * p[0] + co[1] * p[1] + co[2]) for p in pts]
    rpc = 100.0 * sum(1 for v in res if abs(v) > 15) / n
    return raw, rpc, med, lum[0], lum[-1]


def panel(im, view, boxes, title, sub, src, zoom, colour=RED, notes=()):
    x0, y0, x1, y1 = view
    c = im.crop(view).resize(((x1 - x0) * zoom, (y1 - y0) * zoom),
                             Image.LANCZOS)
    d = ImageDraw.Draw(c)
    fs = font(16)
    for lbl, (bx0, by0, bx1, by1), _what in boxes:
        r = [(bx0 - x0) * zoom, (by0 - y0) * zoom,
             (bx1 - x0) * zoom, (by1 - y0) * zoom]
        d.rectangle(r, outline=colour, width=3)
        txt = "%s  (%d,%d)-(%d,%d)" % (lbl, bx0, by0, bx1, by1)
        w = int(d.textlength(txt, font=fs)) + 12
        ty = max(0, r[1] - 23)
        d.rectangle([r[0], ty, r[0] + w, ty + 22], fill=colour)
        d.text((r[0] + 6, ty + 2), txt, fill=(0, 0, 0), font=fs)
    bh = 62 + 19 * len(notes)
    band = Image.new("RGB", (c.width, bh), (16, 16, 16))
    bd = ImageDraw.Draw(band)
    bd.text((12, 7), title, fill=(255, 255, 255), font=font(23))
    bd.text((12, 36), sub, fill=(180, 180, 180), font=fs)
    for k, n in enumerate(notes):
        bd.text((12, 57 + 19 * k), n, fill=(130, 190, 130), font=font(14, False))
    bd.text((c.width - 330, 36),
            "%s   view (%d,%d)-(%d,%d)  x%d" % (src, x0, y0, x1, y1, zoom),
            fill=(120, 120, 120), font=font(14, False))
    out = Image.new("RGB", (c.width, c.height + bh), (16, 16, 16))
    out.paste(band, (0, 0))
    out.paste(c, (0, bh))
    return out


def stack(panels, pad=14):
    w = max(p.width for p in panels)
    h = sum(p.height for p in panels) + pad * (len(panels) - 1)
    fig = Image.new("RGB", (w, h), (16, 16, 16))
    y = 0
    for p in panels:
        fig.paste(p, ((w - p.width) // 2, y))
        y += p.height + pad
    return fig


def grid(panels, cols, pad=14):
    cw = max(p.width for p in panels)
    rh = max(p.height for p in panels)
    rows = (len(panels) + cols - 1) // cols
    fig = Image.new("RGB", (cols * cw + pad * (cols - 1),
                            rows * rh + pad * (rows - 1)), (16, 16, 16))
    for k, p in enumerate(panels):
        r, c = divmod(k, cols)
        fig.paste(p, (c * (cw + pad) + (cw - p.width) // 2,
                      r * (rh + pad)))
    return fig


def main():
    rear = Image.open(REAR).convert("RGB")
    work = Image.open(WORK).convert("RGB")
    print("sources: %s %dx%d   %s %dx%d"
          % (REAR, rear.width, rear.height, WORK, work.width, work.height))

    # ---- Q1 -------------------------------------------------------------
    p1 = panel(rear, Q1_VIEW, Q1_BOXES,
               "Q1  -  the COUNTER TOP's surface condition",
               "Clean varnished plywood / visibly dusty / patchy / can't tell?",
               REAR, 6,
               notes=("BOXES ARE POINTERS -- no number is taken from them.",
                      "W_DUST_FAC_UP asserts mean dust coverage 0.548 on this "
                      "surface (t1_mats.py:441)."))
    p1b = panel(rear, (620, 400, 800, 490), [], "",
                "the same top, larger and closer -- no boxes, just the surface",
                REAR, 8)
    stack([p1, p1b]).save("/tmp/rev28_q1_countertop.png")

    # ---- Q2 -------------------------------------------------------------
    ctx = panel(work, Q2_VIEW, Q2_BOXES,
                "Q2  -  where the five candidate PSF edges sit",
                "context: all five, on the workshop frame",
                WORK, 4, colour=CYAN,
                notes=("BOXES ARE THE ESTIMATOR'S OWN SAMPLING WINDOWS, "
                       "reproduced UNCHANGED from probe_psf_workshop.py.",))
    zooms = []
    for lbl, b, what in Q2_BOXES:
        v = (b[0] - 30, b[1] - 30, b[2] + 30, b[3] + 30)
        zooms.append(panel(work, v, [(lbl, b, what)],
                           "%s  -  paint boundary, or physical step?" % lbl,
                           what, WORK, 7, colour=CYAN))
    g = grid(zooms, 3)
    W = max(ctx.width, g.width)
    fig = Image.new("RGB", (W, ctx.height + 18 + g.height), (16, 16, 16))
    fig.paste(ctx, ((W - ctx.width) // 2, 0))
    fig.paste(g, ((W - g.width) // 2, ctx.height + 18))
    fig.save("/tmp/rev28_q2_psf_edges.png")
    print("  Q2 figure %dx%d" % (fig.width, fig.height))

    # ---- every box, printed ---------------------------------------------
    print("\nEVERY BOX, PRINTED")
    print("Q1  ref_rear34.jpg 1200x824  -- POINTERS")
    for lbl, b, what in Q1_BOXES:
        raw, res, med, lo, hi = straddle(rear, b)
        print("  %-3s (%4d,%4d)-(%4d,%4d)  %-28s  raw spread %5.1f %%  "
              "PLANE-REMOVED %5.1f %%  luma med %.0f  range %.0f-%.0f"
              % (lbl, b[0], b[1], b[2], b[3], what, raw, res, med, lo, hi))
    print("      (raw counts the top's real illumination gradient; the "
          "plane-removed figure is the straddle test)")
    # POSITIVE CONTROL.  SPEC 10.76 PROVED this box straddles -- it is the
    # forensically recovered founding patch for _UP_MEASURED, 66-82 % tan,
    # 8-19 % cream, 6-9 % brass nosing.  If the plane-removed indicator does
    # not fire here it is not an instrument and the P1/P2 figures mean nothing.
    craw, cres, cmed, clo, chi = straddle(rear, (556, 397, 656, 424))
    print("  %-3s (%4d,%4d)-(%4d,%4d)  %-28s  raw spread %5.1f %%  "
          "PLANE-REMOVED %5.1f %%  luma med %.0f  range %.0f-%.0f"
          % ("C+", 556, 397, 656, 424, "SPEC 10.76 founding patch",
             craw, cres, cmed, clo, chi))
    ok = cres > max(0.5, 3.0 * max(straddle(rear, b)[1] for _l, b, _w
                                   in Q1_BOXES))
    print("      POSITIVE CONTROL %s -- the proven-straddling patch reads "
          "%.1f %% plane-removed against P1/P2's %s"
          % ("FIRES" if ok else "DID NOT FIRE (indicator is not usable)", cres,
             " / ".join("%.1f %%" % straddle(rear, b)[1]
                        for _l, b, _w in Q1_BOXES)))
    print("Q2  ref_workshop.jpg 1200x824  -- SAMPLING WINDOWS (verbatim)")
    for lbl, b, what in Q2_BOXES:
        print("  %-3s (%4d,%4d)-(%4d,%4d)  %s" % (lbl, b[0], b[1], b[2], b[3],
                                                  what))
    print("\nwrote /tmp/rev28_q1_countertop.png and "
          "/tmp/rev28_q2_psf_edges.png")


if __name__ == "__main__":
    main()
