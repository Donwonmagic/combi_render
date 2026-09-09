"""
trazo.py -- THE VECTOR LAYER.  Recovered masks become smooth closed contours.

WHY THIS EXISTS.  Asked for "more refined results", the measured answer was NOT
"clean the masks".  `estilos.py` upscales PIXEL masks with LANCZOS, so every
edge carries the capture's sampling grid, and a de-speckling pass was tried
first and REJECTED because it ate real ornament: on the cab-door scrollwork it
removed 24 of 51 components and DELETED A ROSETTE along with the crumbs.  Two
measurements set the direction instead:

  * A 1-px open/close drops the perimeter by **31.9 % (`body_red`), 30.2 %
    (`body_gold`), 25.0 % (`mural_gold`), 33.9 % (`calidad_ink`)** -- that much
    of the outline is sampling noise, not shape.  `script` drops **5.0 %**: the
    wordmark is genuinely clean and needs no help.
  * At 300 dpi the native art (**1142 x 768**) is **2.7x** short for an A3
    sheet and **5.8x** short for an A-frame panel.  The owner asked for print
    AND screen, so upscaling pixels was never going to be enough.

So the refinement is: capture at higher resolution, TRACE, simplify, smooth, and
draw from the contours.  The output is then resolution-independent -- the same
polygons rasterise at proof scale or at 300 dpi, and can be written as SVG.

⚠ CEILINGS.
  * Smoothing is a CHOICE, not a measurement.  Chaikin at 2 iterations was
    picked by looking at the result; a different count is a different drawing.
  * `rdp` epsilon and the minimum area are AUTHORED.  Set them too high and
    this module becomes the de-speckler that was rejected -- so `trace_layer`
    REPORTS what it dropped and `estilos.py` checks the drop stays small.
  * Tracing cannot invent detail the capture did not resolve.  It removes the
    grid, it does not add information.
"""
import json, math, os
import numpy as np
from PIL import Image, ImageDraw

import trace_outline as TO
from sticker import rdp, poly_area


def chaikin(pts, iters=2):
    """Corner-cutting on a CLOSED ring.  Each pass replaces every corner with
    two points at 1/4 and 3/4, which converges to a quadratic B-spline."""
    for _ in range(max(0, iters)):
        n = len(pts)
        if n < 3:
            return pts
        out = []
        for i in range(n):
            (ax, ay), (bx, by) = pts[i], pts[(i + 1) % n]
            out.append((0.75 * ax + 0.25 * bx, 0.75 * ay + 0.25 * by))
            out.append((0.25 * ax + 0.75 * bx, 0.25 * ay + 0.75 * by))
        pts = out
    return pts


# ---------------------------------------------------------------- the cache
# Tracing `sidehi` costs ~9 MINUTES per style, which makes every experiment
# unaffordable and is why the mural threshold was never tuned.  The EXPENSIVE
# half is trace + RDP; Chaikin is cheap.  So the RDP result is what is cached,
# and smoothing is applied on load -- which also keeps the cache small, because
# two Chaikin passes QUADRUPLE the point count.
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "probe_scratch", "trace")


def _key(tag, name, eps, min_area):
    return "%s__%s__e%g_a%g.json" % (tag, name, eps, min_area)


# Cache keys LOADED and keys COMPUTED, this process.
# ⚠ `--out` DOES NOT COVER THIS DIRECTORY.  `CACHE` is `probe_scratch/trace/`
# inside the repository, whatever `--out` a caller passes, so any build --
# including an ablation -- writes into the TRACKED tree.  That is F358's class,
# and the remedy the brief gives for it (`git checkout -- probe_scratch/`)
# restores modified files but leaves NEW ones untracked.  Measured: rev 81
# committed the new cache tiers for 13 of 14 pieces and missed the fourteenth,
# so a cold clone dirtied its own tree and spent ~25 minutes re-tracing `vaso`
# before printing a line.  The counters exist so a build SAYS which it did.
CARGADO = []
CALCULADO = []


def trace_cached(mask, tag, name, eps=0.9, min_area=6.0, smooth=2):
    """`trace_layer` with the trace+RDP half persisted to disk."""
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, _key(tag, name, eps, min_area))
    (CARGADO if os.path.exists(p) else CALCULADO).append(os.path.basename(p))
    if os.path.exists(p):
        raw = json.load(open(p))
        comps = [([tuple(q) for q in o], [[tuple(q) for q in h] for h in hs])
                 for o, hs in raw["comps"]]
        stats = (raw["dropped"], raw["kept"])
    else:
        comps, dropped, kept = _trace_raw(mask, eps, min_area)
        json.dump({"comps": [[[[round(x, 1), round(y, 1)] for x, y in o],
                              [[[round(x, 1), round(y, 1)] for x, y in h]
                               for h in hs]] for o, hs in comps],
                   "dropped": dropped, "kept": kept}, open(p, "w"))
        stats = (dropped, kept)
    out = [(chaikin(o, smooth), [chaikin(h, smooth) for h in hs])
           for o, hs in comps]
    return out, stats[0], stats[1]


def _trace_raw(mask, eps, min_area):
    """trace + RDP only -- no smoothing.  This is the half worth caching."""
    comps, dropped, kept = [], 0, 0
    total = float(mask.sum()) or 1.0
    for outer, holes in TO.trace_with_holes(mask):
        o = [(float(x), float(y)) for y, x in outer]
        o = rdp(o, eps)
        if len(o) < 3 or abs(poly_area(o)) < min_area:
            dropped += 1
            continue
        hs = []
        for h in holes:
            hp = rdp([(float(x), float(y)) for y, x in h], eps)
            if len(hp) >= 3 and abs(poly_area(hp)) >= min_area:
                hs.append(hp)
        comps.append((o, hs))
        kept += abs(poly_area(o)) - sum(abs(poly_area(h)) for h in hs)
    return comps, dropped, kept / total


def trace_layer(mask, eps=0.9, min_area=6.0, smooth=2):
    """A boolean mask -> [(outer, [holes])] as smoothed (x, y) rings.

    Returns (components, dropped, kept_area_frac) so the caller can PROVE the
    simplification did not eat the subject.
    """
    comps, dropped, kept = [], 0, 0
    total = float(mask.sum()) or 1.0
    for outer, holes in TO.trace_with_holes(mask):
        o = [(float(x), float(y)) for y, x in outer]
        o = rdp(o, eps)
        if len(o) < 3 or abs(poly_area(o)) < min_area:
            dropped += 1
            continue
        hs = []
        for h in holes:
            hp = [(float(x), float(y)) for y, x in h]
            hp = rdp(hp, eps)
            if len(hp) >= 3 and abs(poly_area(hp)) >= min_area:
                hs.append(chaikin(hp, smooth))
        comps.append((chaikin(o, smooth), hs))
        kept += abs(poly_area(o)) - sum(abs(poly_area(h)) for h in hs)
    return comps, dropped, kept / total


def render(comps, size, ss=2):
    """Rasterise traced components to an L mask, holes punched.  Even-odd is
    done explicitly -- outer filled, then every hole cleared -- rather than
    trusting one polygon call to know which ring is which."""
    W, H = size
    im = Image.new("L", (W * ss, H * ss), 0)
    d = ImageDraw.Draw(im)
    for outer, holes in comps:
        d.polygon([(x * ss, y * ss) for x, y in outer], fill=255)
        for h in holes:
            d.polygon([(x * ss, y * ss) for x, y in h], fill=0)
    return im.resize((W, H), Image.LANCZOS) if ss != 1 else im


def to_svg_paths(comps, scale=1.0, dx=0.0, dy=0.0, prec=2):
    """The same contours as SVG path data, so a print master is the SAME
    geometry as the proof rather than a re-derivation of it."""
    out = []
    for outer, holes in comps:
        segs = []
        for ring in [outer] + list(holes):
            pts = ["%.*f,%.*f" % (prec, dx + x * scale, prec, dy + y * scale)
                   for x, y in ring]
            segs.append("M" + "L".join(pts) + "Z")
        out.append("".join(segs))
    return out
