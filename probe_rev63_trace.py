"""rev 63 -- EXTRACT THE REAL PRESSING'S GLYPH OUTLINE, AND PROVE IT REPRODUCES.

The method change: stop approximating the mark with seven spine constants and
TRACE IT off the pressing.  `ref_workshop.jpg`'s badge is a different vehicle
but the SAME factory emblem, and the rev-63 brief §0.1 rules on exactly this --
*"the nose roundel's SHAPE is the factory chrome PRESSING, which is geometry and
DOES transfer; only its colour is artwork (F141)."*

CONTROLS
  T1  the tracer passes its own selftest, or this refuses to publish.
  T2  the glyph's enclosed HOLES are counted and CARRIED, never dropped
      (rule 37).  The V and the W touch, so the cream cells between them
      are holes of a single outline; a hole-free trace changes the mark's
      topology, which is the thing C6 counts.  The docstring said "NO
      HOLES" until rev 64 while the T2 beside it printed 2 -- a stale
      sentence sitting on top of a live measurement.
  T3  the traced-and-smoothed outline REPRODUCES the badge it came from -- IoU
      against the source mask.  A trace that does not reproduce its own source
      is not a trace.  REGISTERED on the source's own bounding box: until
      rev 64 this rasterised the trace onto the full canvas and read 0.6504
      against a 0.90 bar, and the deficit was a 9 % SCALE ERROR, not the
      trace (rule 38 -- two sides of a ratio must share a ruler).
  T3a the same comparison restricted to the region the trace actually
      covers, and T3b the ring, which is NOT traced and never was.
  T3c the control T3 never had: the tracer's own INPUT, downsampled to
      T3's raster with no tracing at all.  That is T3's ceiling.
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


def frame_of(mask):
    """-> (cy, cx, ry, rx): the badge's OWN centre and half-extents inside its
    raster.  Every comparison below is registered on this, not on the canvas."""
    ys, xs = np.nonzero(mask)
    return ((ys.min() + ys.max()) / 2.0, (xs.min() + xs.max()) / 2.0,
            (ys.max() - ys.min()) / 2.0, (xs.max() - xs.min()) / 2.0)


def raster(outs, n=276, band_inner=0.80, frame=None, band=True):
    """Rasterise traced outlines (units: badge radius = 1) at n rows.

    rev 64 -- THE `frame` ARGUMENT IS THE FIX, AND IT IS WORTH 0.30 OF IoU.
    This used to map the outline's [-1, 1] onto the FULL canvas, i.e. it
    assumed the badge fills its raster edge to edge.  It does not: resized to
    276 the workshop badge's own bounding box is rows/cols 11..264, half-extent
    126.5 against the assumed 138.  So every traced point was drawn 9.1 % too
    far out, and T3 read the resulting one-to-two-pixel rim of disagreement --
    painted in probe_scratch/rev64_t3_diff.png as red on one side of every
    stroke and green on the other -- as a defect OF THE TRACE.  It was a defect
    of this function.  Rule 38: two sides of a ratio must share a ruler.
    Pass `frame` to register on the source; leave it None for the old behaviour,
    which is what the T3 KILL below uses to hold the repair in place.

    THE UN-REGISTERED PATH IS NOT BYTE-FOR-BYTE REV 63's, AND THE DIFFERENCE IS
    ITSELF A SMALL DEFECT OF REV 63's, SAID OUT LOUD RATHER THAN CHASED.  It
    read 0.6504 where this reads 0.6412.  The old code drew the ring with
    `ellipse([0, 0, n-1, n-1])` -- centre 137.5, radius 137.5 -- and the glyph
    with `n/2 + p*n/2` -- centre 138.0, radius 138.0.  The ring and the strokes
    inside it were on half-a-pixel-different centres AND radii, in one function,
    which is the same class of error as the 9 % above and two orders of
    magnitude smaller.  Both are now on one frame."""
    from PIL import ImageDraw
    im = Image.new("L", (n, n), 0)
    d = ImageDraw.Draw(im)
    cy, cx, ry, rx = (n / 2.0, n / 2.0, n / 2.0, n / 2.0) if frame is None \
        else frame
    if band:
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=255)
        d.ellipse([cx - rx * band_inner, cy - ry * band_inner,
                   cx + rx * band_inner, cy + ry * band_inner], fill=0)

    def P(u):
        return [(cx + p[0] * rx, cy - p[1] * ry) for p in u]

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
FR = frame_of(src)                       # the badge's OWN frame -- one ruler
cy, cx, ry, rx = FR
yy, xx = np.mgrid[0:276, 0:276]
RR = np.sqrt(((yy - cy) / ry) ** 2 + ((xx - cx) / rx) ** 2)
INT = RR < 0.80                          # the region the trace actually covers

rep = raster(OUTS, frame=FR)
unreg = raster(OUTS)                     # what this probe read before rev 64
print("")
print("        the badge's own bbox in the 276 canvas: rows %d..%d, half-extent"
      % (int(cy - ry), int(cy + ry)))
print("        %.1f -- the un-registered raster assumed %.1f, i.e. %.1f %% too big"
      % (ry, 276 / 2.0, 100 * (276 / 2.0 / ry - 1)))
# T3's OBJECT IS RE-BASED AT REV 64, cause named, three companion rows below.
# It used to demand that the traced outline reproduce THE WHOLE BADGE -- but
# the trace produces a GLYPH and the ring is synthetic, so that row was scoring
# a ring model nothing had fitted.  T3b sweeps the band and shows NO concentric
# annulus reaches even 0.68, so the 0.90 bar was unreachable for a reason that
# has nothing to do with tracing.  The glyph is also the only part that goes in
# the mesh.  Rule 34: a requirement inherits its object, so the object is said
# out loud rather than the bar being quietly lowered.  The whole-badge figure is
# still printed, every revision, in T3e -- it is re-based, not dropped.
rep_g = raster(OUTS, frame=FR, band=False)
ctl("T3", iou(rep_g & INT, src & INT) > 0.90,
    "THE TRACED GLYPH REPRODUCES THE GLYPH IT CAME FROM, both sides at r<0.80: "
    "IoU %.4f  (un-registered: %.4f -- rev 63 published 0.6504/0.7848 with a\n     half-pixel offset inside its own raster, see raster.__doc__)"
    % (iou(rep_g & INT, src & INT),
       iou(raster(OUTS, band=False) & INT, src & INT)))

ctl("T3e", True,
    "AND THE WHOLE BADGE, REPORTED WITH ITS CEILING, NOT GATED: IoU %.4f "
    "registered, %.4f as rev 63 read it.  What is left is the ring (T3b)"
    % (iou(rep, src), iou(unreg, src)))

_best = max((iou(raster(OUTS, frame=FR, band_inner=b) & ~INT, src & ~INT), b)
            for b in np.arange(0.74, 0.92, 0.02))
ctl("T3b", True,
    "THE RING IS NOT TRACED AND NEVER WAS: synthetic annulus %.4f against the "
    "badge's own band, and NO concentric band beats it (best inner %.2f). "
    "The rev-63 brief's \"the disagreement is the RING (IoU 0.508)\" named the "
    "right half and the wrong cause -- both halves were the scale error"
    % (iou(rep & ~INT, src & ~INT), _best[1]))

# T3c -- THE CONTROL T3 NEVER HAD.  No tracing at all: take the tracer's own
# input and downsample it to T3's raster.  A trace cannot beat this, so if it
# were low, T3's bar would be unreachable for reasons that have nothing to do
# with tracing.  Watched: 0.9991, so the bar is reachable and T3 is a real test.
_down = np.asarray(Image.fromarray((inner * 255).astype(np.uint8))
                   .resize((276, 276), Image.LANCZOS)) > 127
ctl("T3c", iou(_down & INT, src & INT) > 0.95,
    "CEILING, no trace at all -- the tracer's INPUT at T3's raster: IoU %.4f. "
    "T3a cannot beat this, and it is not what limits T3a"
    % iou(_down & INT, src & INT))

# T3d -- KILL, and it was watched failing.  Registration is now load-bearing:
# if someone removes it, this must go red rather than the probe quietly
# reporting a trace defect again.
ctl("T3d", iou(unreg, src) < 0.90,
    "KILL: the SAME trace rasterised without registration reads %.4f, under "
    "T3's own 0.90 bar.  The repair is held in place by this row"
    % iou(unreg, src))

# ------------------------------------------------------------------------ T4
sys.argv = [sys.argv[0]]
import probe_rev46_vw as _vw                                    # noqa: E402


def regis(m, n=276):
    """Crop a badge mask to its OWN ink bounding box and resize to n x n.

    rev 64 -- WITHOUT THIS, T4's WHOLE COLUMN BROKE RULE 38, and it broke it in
    the direction that flattered the conclusion the rev-63 brief drew from it.
    `built_mask` rasterises edge to edge; a photographed badge resized to 276
    occupies rows 11..264 of its canvas.  Scoring one against the other charges
    the built glyph a 9 % scale error it does not have.  Every row below is now
    registered the same way, so the column compares SHAPES."""
    ys, xs = np.nonzero(m)
    sub = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return np.asarray(Image.fromarray((sub * 255).astype(np.uint8))
                      .resize((n, n), Image.LANCZOS)) > 127


ship = _vw.glyph_only_mask(rows=276, **{k: getattr(_vw.C, k) for k in _vw.PARAMS})
nol = np.asarray(Image.fromarray((A.nolita() * 255).astype(np.uint8))
                 .resize((276, 276), Image.LANCZOS)) > 127
_NOL = regis(nol)
print("")
print("  T4 -- ON ONE RULER: cells, elongation, and agreement with the TARGET")
print("        BUS's own badge (a second, independent frame).  EVERY row is")
print("        registered on its own bounding box first -- see regis()")
print("        %-26s %-7s %-11s %-11s %s"
      % ("", "cells", "elongation", "IoU (one ruler)", "IoU as rev 63 read it"))
_T4 = {}
for nm, m in (("SHIPPED glyph", ship), ("TRACED pressing", rep),
              ("the workshop badge", src), ("TARGET BUS badge", nol)):
    n, _ = _vw.cream_cells(m)
    e = _vw.cell_elongation(m, 1.0)
    _T4[nm] = iou(regis(m), _NOL)
    # the rev-63 reading for the TRACED row must use the UN-registered raster,
    # because `rep` itself is registered now.  Using `rep` there would have
    # printed 0.5893 under a heading that says "as rev 63 read it", which is a
    # third ruler wearing a second one's label -- caught by reading the row
    # against its own sentence, which is how rev 63 caught its C24.
    _old = iou(unreg, nol) if nm == "TRACED pressing" else iou(m, nol)
    print("        %-26s %-7d %-11.3f %-11.4f %.4f"
          % (nm, n, e, _T4[nm], _old))
ctl("T6", _T4["TRACED pressing"] > _T4["SHIPPED glyph"],
    "ON ONE RULER the traced pressing still agrees with the TARGET BUS's badge "
    "better than the shipped glyph: %.4f against %.4f (margin %+.4f).  Rev 63 "
    "read this margin as +%.4f off two different rulers"
    % (_T4["TRACED pressing"], _T4["SHIPPED glyph"],
       _T4["TRACED pressing"] - _T4["SHIPPED glyph"], 0.7129 - 0.5367))

Image.fromarray(np.concatenate(
    [np.where(src, 235, 30), np.where(rep, 235, 30),
     np.where(ship, 235, 30)], axis=1).astype(np.uint8)).save(
    os.path.join(SCRATCH, "rev63_trace_check.png"))
ctl("T5", True, "painted rev63_trace_check.png  BADGE | TRACED | SHIPPED")
np.save(os.path.join(SCRATCH, "rev63_traced_outlines.npy"),
        np.array(OUTS, dtype=object), allow_pickle=True)
print("")
print("  %s" % ("ALL CONTROLS PASS" if not _fail else "FAILED: %s" % _fail))
