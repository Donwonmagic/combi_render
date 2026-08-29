# probe_rev69_emblem.py -- rev 69.  THE EMBLEM, MEASURED ON THE RENDER.
#
# WHY THIS EXISTS.  The owner has reported this emblem SEVEN times, most
# recently as *"The strokes still don't reach the ring."*  The gate that scores
# it, `probe_rev46_vw.py`'s C6, reads a RASTER built from the constants and
# passes 6 = 6.  The RENDER disagrees -- rev 67 measured photograph 6 against
# render 4 / 3 / 2 -- and THAT MEASUREMENT EXISTED IN NO COMMITTED FILE.  A gate
# passing on a proxy while the delivered pixels fail is rule 41, on the
# project's top item.  This is the missing instrument.
#
# THE CONTRADICTION IT WAS WRITTEN TO RESOLVE, and it is sharp:
#
#     probe_rev46_vw.terminal_reach()   every terminal at EXACTLY 0.8400 R
#     t1_core._RING_INNER_FRAC          the band's inner edge at 0.8000 R
#     => the strokes should OVERLAP the band by 0.04 R, i.e. they must touch
#
#     the RENDER                        the V's arms stop around 0.6 R, with
#                                       cream all round them, and the glyph is
#                                       a SEPARATE connected component from the
#                                       ring -- in the photograph they are ONE
#
# Both cannot be true of the same object.  F210 already found that the "mesh
# says 0.8400" half is not an independent observation -- `_on_band` DRIVES the
# terminals to exactly that number, so it is the fit target restated.  So the
# render is asked instead, in pixels, with no constant taken on trust.
#
# EVERYTHING HERE IS MEASURED IN THE IMAGE, and every window is PAINTED before
# a number is printed (rule 8).  READ THIS PROBE'S OWN SUMMARY LINE, NEVER ITS
# EXIT CODE (rule 9).
import os
import sys

import numpy as np
from PIL import Image, ImageDraw
import scipy.ndimage as ndi

# rev 67's own ink ladder, in levels below the disc's cream.  Its published
# figures (photograph 6, render 4 / 3 / 2) were taken at 20 / 30 / 40.
THR = 30

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.join(HERE, "probe_scratch")

# The photograph's own roundel window, taken VERBATIM from
# `probe_rev46_vw.photo_cells` so the two sides cannot drift apart (rule 38).
PHOTO = "ref_nolita_front34.jpg"
PHOTO_BOX = (153, 192, 194, 261)          # x0, y0, x1, y1


def red_mask(a):
    """The photograph's own red test, taken VERBATIM from
    `probe_rev46_vw.photo_cells`.  USED ONLY TO FIND THE RING, never to measure
    the strokes -- see `ink_mask` for why."""
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    return (R > 110) & (G < 0.60 * R) & (B < 0.60 * R)


def ink_mask(a, interior, thr):
    """The strokes, as INK AGAINST THIS IMAGE'S OWN CREAM.

    AND THE REASON THIS IS NOT `red_mask` IS A DEFECT I BUILT AND MEASURED.
    Segmenting the render with the photograph's red test looked like the
    strictest possible "same ruler" (rule 38).  It is not: the render's strokes
    are a DARKER, LESS SATURATED red than the photograph's, so that test caught
    only their brightest parts and shattered the glyph into fragments.  The
    probe then reported "19 red components" and called it "the glyph floats
    free of its ring" -- a topological claim that was really a threshold
    artefact.  Painted and looked at; caught there, not in the number.

    What transfers between two images of the same object under different light
    is INK RELATIVE TO THE CREAM IT SITS ON.  The cream level is estimated per
    image from the interior's own bright mode, and `thr` is the same ladder rev
    67 used on this defect (20 / 30 / 40 levels), so its figures are
    reproducible from this file for the first time."""
    lum = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    vals = lum[interior]
    if not len(vals):
        return np.zeros(lum.shape, bool)
    cream = np.percentile(vals, 80)          # the disc's own cream
    return interior & (lum < cream - thr)


def find_emblem(a, box=None):
    """Locate the roundel RING in a frame.  Returns (mask_of_ring, (cx, cy)).

    NOT A FIXED WINDOW.  Rev 69 learned the hard way that the previews AUTO-FRAME
    -- `studio.fit_view` centres the subject and fills 0.92 of the frame from
    `subject_bbox()`, so ANY change to the vehicle's extent moves every feature
    in the image.  A hard-coded crop would silently measure the wrong pixels the
    first time somebody touched the geometry.

    So the ring is FOUND: among the red connected components, the roundel is the
    one that is nearly square in bbox, of plausible size, and -- the part that
    actually discriminates -- ENCLOSES A HOLE.  The body's red panels are large
    and solid; only the ring is an annulus."""
    red = red_mask(a)
    if box is not None:
        m = np.zeros(red.shape, bool)
        m[box[1]:box[3], box[0]:box[2]] = True
        red = red & m
    lab, n = ndi.label(red)
    best = None
    for i in range(1, n + 1):
        c = lab == i
        ys, xs = np.nonzero(c)
        if len(xs) < 200:
            continue
        w, h = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
        # THE PHOTOGRAPH'S ROUNDEL IS OBLIQUE: 41 x 69 px, aspect 0.594.  My
        # first cut used 0.6 and REJECTED IT -- the reference frame failed the
        # instrument's own finder.  A roundel seen from a three-quarter view is
        # a squashed ellipse and the bound has to admit one.
        if not (0.45 < w / float(h) < 2.2):
            continue
        # an annulus: filling it adds a lot of area
        filled = ndi.binary_fill_holes(c)
        hole = filled.sum() - c.sum()
        if hole < 0.4 * c.sum():
            continue
        if best is None or c.sum() > best[1].sum():
            best = (i, c, filled)
    if best is None:
        return None, None
    _, ring, filled = best
    ys, xs = np.nonzero(filled)
    return ring, (xs.mean(), ys.mean())


def radial_profile(mask, c, n_ang=720):
    """For each of `n_ang` rays from `c`, the radii at which `mask` is true.

    Returns a list of (angle, r_min, r_max) for rays that hit the mask at all.
    Angles are image-frame, measured CCW from +x with y DOWN negated so the
    result reads like a clock face."""
    cx, cy = c
    H, W = mask.shape
    rmax = int(min(cx, cy, W - cx, H - cy))
    out = []
    for k in range(n_ang):
        th = 2 * np.pi * k / n_ang
        dx, dy = np.cos(th), -np.sin(th)
        rr = np.arange(1.0, rmax, 0.5)
        xs = np.clip((cx + dx * rr).astype(int), 0, W - 1)
        ys = np.clip((cy + dy * rr).astype(int), 0, H - 1)
        hit = mask[ys, xs]
        if not hit.any():
            continue
        idx = np.nonzero(hit)[0]
        out.append((th, rr[idx[0]], rr[idx[-1]]))
    return out


def measure(path, tag, paint_to):
    """The whole measurement for ONE image.  Returns a dict, or None.

    STRUCTURED AROUND `cream_cells`, THE PROJECT'S OWN STATISTIC, AND MY FIRST
    CUT WAS NOT.  I tried to separate the RING from the GLYPH and measure the
    gap between them.  On the photograph that is impossible BY THE VERY FACT
    BEING MEASURED: there the strokes touch the ring, so they are ONE connected
    component, and "the ring" swallowed the glyph -- the probe reported a ring
    inner radius of 1.0 px and a reach of 28.0.  The separation cannot be a
    PRECONDITION of an instrument whose question is whether the separation
    exists.

    `cream_cells` needs no separation: it counts how many CREAM regions the ink
    cuts the disc into.  A stroke that fails to reach the ring merges the two
    cells either side of it, so the count drops by exactly one per floating
    stroke -- whatever the stroke's width, angle or colour.  The photograph
    makes SIX.  Both sides go through THE SAME FUNCTION, imported, not copied.
    """
    import probe_rev46_vw as _P                 # the real cream_cells
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(float)
    box = PHOTO_BOX if os.path.basename(path) == PHOTO else None
    ring, c = find_emblem(a, box)
    if ring is None:
        print("  %-10s NO ROUNDEL FOUND in %s -- nothing measured (rule 37)"
              % (tag, os.path.basename(path)))
        return None
    filled = ndi.binary_fill_holes(ring)
    ys, xs = np.nonzero(filled)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    sub = a[y0:y1, x0:x1]
    disc = filled[y0:y1, x0:x1]

    ladder, inks = {}, {}
    for t in (20, 30, 40):
        ink = ink_mask(sub, disc, t)
        inks[t] = ink
        n_raw, _ = _P.cream_cells(ink, interior=False)
        n_int, _ = _P.cream_cells(ink, interior=True)
        ladder[t] = (n_raw, n_int)

    d = dict(tag=tag, ladder=ladder, wh=(x1 - x0, y1 - y0),
             ink_frac=float(inks[THR].sum()) / max(1, disc.sum()))

    # ---- PAINT IT, BEFORE ANY NUMBER IS BELIEVED (rule 8)
    base = (np.asarray(im.convert("L")).astype(int) // 2 + 90)[y0:y1, x0:x1]
    ov = np.dstack([base] * 3)
    ov[inks[THR]] = [255, 0, 255]
    p = Image.fromarray(ov.astype("uint8"))
    S = max(1, 420 // max(p.width, p.height))
    p = p.resize((p.width * S, p.height * S), Image.NEAREST)
    dr = ImageDraw.Draw(p)
    dr.text((4, 3), "%s  magenta = INK at thr %d" % (tag, THR), fill=(255, 255, 0))
    p.save(paint_to)
    print("  %-10s roundel %d x %d px | ink %.1f %% of the disc | "
          "CREAM CELLS (raw/interior) at thr 20/30/40: %s"
          % (tag, x1 - x0, y1 - y0, 100 * d["ink_frac"],
             "  ".join("%d/%d" % ladder[t] for t in (20, 30, 40))))
    print("             painted -> %s" % paint_to)
    return d


def main():
    frame = sys.argv[1] if len(sys.argv) > 1 else None
    checks, fails = [], []

    def ck(name, ok, detail):
        checks.append((name, ok, detail))
        if not ok:
            fails.append(name)

    ph = measure(os.path.join(HERE, PHOTO), "PHOTOGRAPH",
                 os.path.join(SCRATCH, "rev69_emblem_photo.png"))
    rn = None
    if frame is None:
        print("\nNO FRAME GIVEN -- the RENDER rows DID NOT RUN.  Pass one, e.g. "
              "`python3 probe_rev69_emblem.py out/r70_front.png`.  The "
              "photograph row above stands; the render rows are ABSENT, NOT "
              "PASSED (rule 3).")
    elif not os.path.exists(frame):
        print("\nNO RENDER -- %s does not exist.  out/ is untracked and starts "
              "EMPTY on a clone.  Nothing was measured." % frame)
        return 2
    else:
        rn = measure(frame, "RENDER", os.path.join(SCRATCH, "rev69_emblem_render.png"))

    print()
    if ph:
        ck("E1 the PHOTOGRAPH cuts its disc into SIX cream cells -- the "
           "statistic the whole gate rests on",
           ph["ladder"][30][1] == 6,
           "interior cells at thr 20/30/40: %s (raw %s)"
           % ("/".join(str(ph["ladder"][t][1]) for t in (20, 30, 40)),
              "/".join(str(ph["ladder"][t][0]) for t in (20, 30, 40))))
    if rn and ph:
        want = ph["ladder"][30][1]
        got = rn["ladder"][30][1]
        ck("E2 THE RENDER cuts its disc into as many cells as the PHOTOGRAPH, "
           "by the SAME function on ink measured against each image's OWN cream",
           got == want,
           "render %s against the photograph's %s (interior, thr 20/30/40).  "
           "EVERY CELL SHORT IS A STROKE THAT FAILED TO REACH THE RING -- the "
           "count drops by exactly one per floating stroke.  This is the "
           "owner's *'the strokes still don't reach the ring'*, and it is the "
           "row `probe_rev46_vw`'s C6 CANNOT see, because C6 reads a raster "
           "built from the constants and passes 6 = 6 (F205, rule 41)"
           % ("/".join(str(rn["ladder"][t][1]) for t in (20, 30, 40)),
              "/".join(str(ph["ladder"][t][1]) for t in (20, 30, 40))))
    print("=" * 78)
    print("  probe_rev69_emblem -- THE EMBLEM, ON THE RENDER (F205)")
    print("=" * 78)
    for name, ok, detail in checks:
        print("  [%s] %s\n        %s" % ("PASS" if ok else "FAIL", name, detail))
    print()
    print("  CEILING.  The photograph is 41 x 69 px and OBLIQUE; the render is "
          "head-on and\n  ~120 px.  A CELL COUNT IS A REGION COUNT, so it "
          "survives blur, exposure and\n  foreshortening -- which is why this "
          "project chose it -- but it is NOT a\n  fidelity claim about stroke "
          "WIDTH, ANGLE or POSITION, and it cannot say WHICH\n  stroke floats, "
          "only how many do.  The ink threshold is measured against each\n  "
          "image's OWN cream, so the two sides never share an absolute level.")
    print()
    print("  %d checked, %d FAILED%s"
          % (len(checks), len(fails), ("  --  " + fails[0]) if fails else ""))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
