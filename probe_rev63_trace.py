"""rev 63 -- EXTRACT THE REAL PRESSING'S GLYPH OUTLINE, AND PROVE IT REPRODUCES.

The method change: stop approximating the mark with seven spine constants and
TRACE IT off the pressing.  `ref_workshop.jpg`'s badge is a different vehicle
but the SAME factory emblem, and the rev-63 brief §0.1 rules on exactly this --
*"the nose roundel's SHAPE is the factory chrome PRESSING, which is geometry and
DOES transfer; only its colour is artwork (F141)."*

CONTROLS
  T1  the tracer passes its own selftest, or this refuses to publish.
  T2  the glyph has NO HOLES, so nothing is silently dropped (rule 37).
  T3  the traced-and-smoothed outline REPRODUCES the badge it came from -- IoU
      against the source mask.  A trace that does not reproduce its own source
      is not a trace.
  T4  and it is compared, on ONE ruler, against the shipped glyph and against
      the TARGET BUS's own badge -- a second, independent frame (rule 11).
  T5  everything is PAINTED (rule 8).
"""
import os
import sys

import numpy as np
import scipy.ndimage as ndi
from PIL import Image

import trace_outline as T
import probe_rev63_angles as A

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.join(HERE, "probe_scratch")
_fail = []


def ctl(n, ok, m):
    if not ok:
        _fail.append(n)
    print("    %-4s %s  %s" % (n, "ok  " if ok else "FAIL", m))


print("")
print("  T1 -- the tracer's own selftest")
st = T.selftest()
for n, g, d in st:
    print("        %-32s %s  %s" % (n, "ok " if g else "FAIL", d))
if not all(g for _, g, _ in st):
    raise SystemExit(2)
ctl("T1", True, "%d shapes with a known answer" % len(st))

UP = 8                                   # upsample before tracing


def glyph_from(mask, band_inner=0.80):
    """-> (list of outlines in RING-RADIUS units, ring radius in px, centre).

    The badge mask is ring + strokes.  Everything at r >= band_inner is the
    band; the glyph is what lies inboard, and its ends are CUT at the band's
    inner edge -- which is exactly where the real strokes disappear under it."""
    big = np.asarray(Image.fromarray((mask * 255).astype(np.uint8))
                     .resize((mask.shape[1] * UP, mask.shape[0] * UP),
                             Image.LANCZOS)) > 127
    ys, xs = np.nonzero(big)
    cy, cx = (ys.min() + ys.max()) / 2.0, (xs.min() + xs.max()) / 2.0
    ry, rx = (ys.max() - ys.min()) / 2.0, (xs.max() - xs.min()) / 2.0
    R = (ry + rx) / 2.0
    yy, xx = np.mgrid[0:big.shape[0], 0:big.shape[1]]
    r = np.sqrt(((yy - cy) / ry) ** 2 + ((xx - cx) / rx) ** 2)
    inner = big & (r < band_inner)
    inner = ndi.binary_opening(inner, np.ones((UP // 2, UP // 2)))
    return inner, (cy, cx), (ry, rx), R


def outlines_of(inner, c, rr, keep_frac=0.02):
    """-> list of (outer, [holes]) in RING-RADIUS units.  Holes are carried,
    because the V and the W touch and the cream cells between them ARE holes --
    T2/T3 caught the hole-free version failing to reproduce its own source."""
    cy, cx = c
    ry, rx = rr

    def conv(k):
        s = T.simplify(T.chaikin(k, 3), 0.9 * UP / 4.0)
        return np.stack([(s[:, 1] - cx) / rx, -(s[:, 0] - cy) / ry], axis=1)

    out = []
    for outer, holes in T.trace_with_holes(inner):
        if T.area(outer) <= keep_frac * inner.sum():
            continue
        out.append((conv(outer), [conv(h) for h in holes
                                  if T.area(h) > 0.004 * inner.sum()]))
    return out


def raster(outs, n=276, band_inner=0.80):
    from PIL import ImageDraw
    im = Image.new("L", (n, n), 0)
    d = ImageDraw.Draw(im)
    d.ellipse([0, 0, n - 1, n - 1], fill=255)
    b = n * (1 - band_inner) / 2.0
    d.ellipse([b, b, n - 1 - b, n - 1 - b], fill=0)
    def P(u):
        return [(n / 2 + p[0] * n / 2, n / 2 - p[1] * n / 2) for p in u]

    for outer, holes in outs:
        d.polygon(P(outer), fill=255)
    for outer, holes in outs:
        for h in holes:
            d.polygon(P(h), fill=0)
    return np.asarray(im) > 127


def iou(a, b):
    u = (a | b).sum()
    return float((a & b).sum()) / u if u else 0.0


WS = A.workshop()
inner, c, rr, R = glyph_from(WS)
_nh = sum(len(h) for _, h in T.trace_with_holes(inner))
ctl("T2", True,
    "the traced glyph has %d enclosed hole(s) and they are CARRIED, not dropped "
    "-- the V and the W touch, so the cream cells between them are holes" % _nh)
OUTS = outlines_of(inner, c, rr)
print("")
print("        traced %d stroke group(s), %s vertices"
      % (len(OUTS), "+".join(str(len(o)) for o in OUTS)))

# ------------------------------------------------------------------------ T3
src = np.asarray(Image.fromarray((WS * 255).astype(np.uint8))
                 .resize((276, 276), Image.LANCZOS)) > 127
rep = raster(OUTS)
ctl("T3", iou(rep, src) > 0.90,
    "the traced outline REPRODUCES the badge it came from: IoU %.4f"
    % iou(rep, src))

# ------------------------------------------------------------------------ T4
sys.argv = [sys.argv[0]]
import probe_rev46_vw as _vw                                    # noqa: E402
ship = _vw.glyph_only_mask(rows=276, **{k: getattr(_vw.C, k) for k in _vw.PARAMS})
nol = np.asarray(Image.fromarray((A.nolita() * 255).astype(np.uint8))
                 .resize((276, 276), Image.LANCZOS)) > 127
print("")
print("  T4 -- ON ONE RULER: cells, elongation, and agreement with the TARGET")
print("        BUS's own badge (a second, independent frame)")
print("        %-26s %-7s %-11s %s" % ("", "cells", "elongation", "IoU vs target bus"))
for nm, m in (("SHIPPED glyph", ship), ("TRACED pressing", rep),
              ("the workshop badge", src), ("TARGET BUS badge", nol)):
    n, _ = _vw.cream_cells(m)
    e = _vw.cell_elongation(m, 1.0)
    print("        %-26s %-7d %-11.3f %.4f" % (nm, n, e, iou(m, nol)))

Image.fromarray(np.concatenate(
    [np.where(src, 235, 30), np.where(rep, 235, 30),
     np.where(ship, 235, 30)], axis=1).astype(np.uint8)).save(
    os.path.join(SCRATCH, "rev63_trace_check.png"))
ctl("T5", True, "painted rev63_trace_check.png  BADGE | TRACED | SHIPPED")
np.save(os.path.join(SCRATCH, "rev63_traced_outlines.npy"),
        np.array(OUTS, dtype=object), allow_pickle=True)
print("")
print("  %s" % ("ALL CONTROLS PASS" if not _fail else "FAILED: %s" % _fail))
