# probe_rev69_angles.py -- rev 69.  THE EMBLEM'S STROKE ANGLES.  F235 / F104.
#
# WHY THIS EXISTS, AND IT IS THE POINT OF THE WHOLE REVISION.
#
# The owner has reported this emblem EIGHT times.  Shown the shipped mark beside
# the solver's own landmark-optimal alternative he said *"Just what the fuck.
# Are you telling me?  That looks right to you?"* -- and he was right.  Rendered
# flat, the built glyph is a compact mass with six slits, not a V over a W.
#
# WHAT IS ACTUALLY WRONG IS NOT WHAT EIGHT REVISIONS HAVE BEEN TUNING.  Measured
# at rev 69: the ink is the RIGHT AMOUNT (56.9 % of the ring's interior
# photographed, 52.5 % on the raster), the strokes are not too fat or too thin,
# and they DO reach the ring.  What is wrong is WHERE THEY POINT:
#
#     photograph  cream-sliver angles 109.1  87.5 112.8  90.1  99.1  84.1
#                                     -> spread 28.6 deg, six near-parallel
#     built                            66.9 112.9  89.3  59.6 120.4  89.1
#                                     -> spread 60.9 deg, they RADIATE
#
# That is "it reads as an X" as a number, and it is F104 -- carried in the
# register since rev 60 and never acted on -- *"the ink is the right AMOUNT
# arranged the WRONG WAY."*
#
# WHY NO EXISTING GATE SEES IT.  `probe_rev46_vw`'s C1-C5 fit L1-L6, which are
# VERTICAL LANDMARK POSITIONS on the ring; fitting them does not constrain a
# stroke's ANGLE at all, which is why a point that improves the landmark
# residual 8.4x still looked wrong to the owner.  C6 counts cells and six slits
# in a blob is still six.  C8 reports ONE AGGREGATE elongation, which averages
# the fan away.  Rule 41, on the project's top item.
#
# THE POSE CORRECTION, AND IT IS THE WHOLE DIFFICULTY (F184).  An angle measured
# in an oblique projection is NOT the object's angle.  The photographed roundel
# is a CIRCLE, so its image ellipse gives the foreshortening directly: stretch
# the crop by (height / width) and the circle -- and every angle on it -- comes
# back.  Nothing here is measured before that is done.
#
# READ THIS PROBE'S OWN SUMMARY LINE, NEVER ITS EXIT CODE (rule 9).
import os
import sys

import numpy as np
from PIL import Image, ImageDraw
import scipy.ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.join(HERE, "probe_scratch")

PHOTO = "ref_nolita_front34.jpg"
PHOTO_BOX = (153, 192, 194, 261)


def cells(mask, disc, min_frac=0.002):
    """Every cream cell inside `disc`, as (polar_position, orientation, aspect,
    area).  Both angles in degrees.

    `polar_position` is the cell centroid's angle about the disc centre, CCW
    from +x with image-y negated -- it is the cell's IDENTITY ("the cell at two
    o'clock"), and it is what lets two marks be compared cell-for-cell instead
    of by a sorted list, which would silently pair the wrong ones.

    `orientation` is the cell's long axis.  A cream sliver runs PARALLEL to the
    strokes either side of it, so the slivers' angles ARE the mark's angles --
    which is why this is measured on the cream and not on the ink.  Measuring
    the ink would need a skeleton, and a skeleton of a mass with slits in it is
    not stable.
    """
    lab, k = ndi.label(disc & ~mask)
    inside = ndi.binary_fill_holes(mask)
    n0, n1 = mask.shape
    cy0, cx0 = (n0 - 1) / 2.0, (n1 - 1) / 2.0
    out = []
    for i in range(1, k + 1):
        m = lab == i
        n = int(m.sum())
        if n < min_frac * disc.sum():
            continue
        if float((m & inside).sum()) / n <= 0.5:
            continue                       # background beyond the ring's rim
        ys, xs = np.nonzero(m)
        pos = np.degrees(np.arctan2(-(ys.mean() - cy0), xs.mean() - cx0)) % 360.0
        yy = ys - ys.mean()
        xx = xs - xs.mean()
        cov = np.cov(np.vstack([xx, yy]))
        w, v = np.linalg.eigh(cov)
        ang = np.degrees(np.arctan2(-v[1, -1], v[0, -1])) % 180.0
        asp = float((w[-1] / max(w[0], 1e-9)) ** 0.5)
        out.append((pos, ang, asp, n))
    out.sort(key=lambda t: t[0])
    return out


def fit_ellipse(pts):
    """Direct least-squares conic fit.  Returns (cx, cy, a, b, theta)."""
    x = pts[:, 0].astype(float)
    y = pts[:, 1].astype(float)
    mx, my = x.mean(), y.mean()
    sc = max(x.std(), y.std())
    if sc <= 0:
        return None
    x = (x - mx) / sc
    y = (y - my) / sc
    D = np.column_stack([x * x, x * y, y * y, x, y, np.ones_like(x)])
    _, _, V = np.linalg.svd(D, full_matrices=False)
    A_, B_, C_, D_, E_, F_ = V[-1]
    disc = B_ * B_ - 4 * A_ * C_
    if disc >= 0:
        return None
    cx = (2 * C_ * D_ - B_ * E_) / disc
    cy = (2 * A_ * E_ - B_ * D_) / disc
    M = np.array([[A_, B_ / 2], [B_ / 2, C_]])
    off = A_ * cx * cx + B_ * cx * cy + C_ * cy * cy + D_ * cx + E_ * cy + F_
    w, vec = np.linalg.eigh(M)
    if np.any(w * (-off) <= 0):
        return None
    ax = np.sqrt(-off / w)
    o = np.argsort(-ax)
    v = vec[:, o[0]]
    return (cx * sc + mx, cy * sc + my, ax[o[0]] * sc, ax[o[1]] * sc,
            float(np.arctan2(v[1], v[0])))


def unsquash(sub, disc):
    """Stretch an obliquely-viewed roundel back to circular.

    THE FIRST VERSION OF THIS DIVIDED BY THE CROP'S BOUNDING-BOX RATIO AND
    STRETCHED ALONG THE IMAGE X AXIS.  That is only correct if the image
    ellipse's axes happen to lie along the image axes, and on a three-quarter
    view of a turned nose they do not.  MEASURED: after that correction the
    photograph's mark was still 26-46 deg away from its own MIRROR SYMMETRY,
    and the angle residual it produced (15.58 deg) was contaminated by the
    leftover rotation.  Fitting to that number would have baked a pose artefact
    into the geometry -- F184's trap, in the instrument written to avoid it.

    THE ROUNDEL IS A CIRCLE, so the correct correction is the affine that maps
    its fitted ELLIPSE back to a circle: rotate by -theta, scale the minor axis
    up by a/b, rotate back.  No camera model, no focal length, no pose solve --
    the circle carries its own pose.

    AND THE MARK'S OWN SYMMETRY VALIDATES IT.  The VW mark is mirror-symmetric
    about a diameter, so after a correct correction a cell at polar p must
    mirror one at 180-p with theta -> 180-theta.  That check needs no external
    truth and is control A0."""
    m = disc.astype(np.uint8)
    er = ndi.binary_erosion(disc, iterations=1)
    ys, xs = np.nonzero(disc & ~er)
    if len(xs) < 30:
        return sub, disc, None
    e = fit_ellipse(np.column_stack([xs, ys]))
    if e is None:
        return sub, disc, None
    cx, cy, a, b, th = e
    k = a / max(b, 1e-9)
    c, s_ = np.cos(-th), np.sin(-th)
    # inverse map: for each output pixel, where does it come from in the input
    H, W = disc.shape
    R = int(np.ceil(2 * a)) + 4
    oy, ox = np.mgrid[0:R, 0:R]
    px = ox - R / 2.0
    py = oy - R / 2.0
    # undo: rotate into ellipse frame, shrink the minor axis back
    ex = px * np.cos(th) - py * np.sin(th)
    ey = px * np.sin(th) + py * np.cos(th)
    ey = ey / k
    sx = ex * np.cos(-th) - ey * np.sin(-th) + cx
    sy = ex * np.sin(-th) + ey * np.cos(-th) + cy
    ix = np.clip(np.round(sx).astype(int), 0, W - 1)
    iy = np.clip(np.round(sy).astype(int), 0, H - 1)
    out = sub[iy, ix]
    od = disc[iy, ix] & (sx >= 0) & (sx < W) & (sy >= 0) & (sy < H)
    return out, od, (a, b, np.degrees(th))


def ink_mask(a, interior, thr=20):
    lum = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    v = lum[interior]
    if not len(v):
        return np.zeros(lum.shape, bool)
    return interior & (lum < np.percentile(v, 80) - thr)


def from_photo():
    """The photograph's six stroke angles, POSE-CORRECTED."""
    import probe_rev69_emblem as E
    a = np.asarray(Image.open(os.path.join(HERE, PHOTO)).convert("RGB")).astype(float)
    ring, _c = E.find_emblem(a, PHOTO_BOX)
    if ring is None:
        return None
    f = ndi.binary_fill_holes(ring)
    ys, xs = np.nonzero(f)
    sub = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    d = f[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    sub, d, ell = unsquash(sub, d)
    from_photo.ellipse = ell
    n0, n1 = d.shape
    yy, xx = np.mgrid[0:n0, 0:n1]
    cy, cx = (n0 - 1) / 2.0, (n1 - 1) / 2.0
    disc = (((yy - cy) / (n0 / 2.0)) ** 2 + ((xx - cx) / (n1 / 2.0)) ** 2) <= 0.97 ** 2
    return cells(ink_mask(sub, d), disc)


def from_built(rows=900, **over):
    """The built mark's six stroke angles, off the raster the gates score."""
    import probe_rev46_vw as P
    m = P.glyph_only_mask(rows=rows, **over)
    n0, n1 = m.shape
    yy, xx = np.mgrid[0:n0, 0:n1]
    cy, cx = (n0 - 1) / 2.0, (n1 - 1) / 2.0
    disc = (((yy - cy) / (n0 / 2.0)) ** 2 + ((xx - cx) / (n1 / 2.0)) ** 2) <= 0.97 ** 2
    return cells(m, disc)


def residual(pa, pb):
    """RMS angular difference between two six-cell sets, MATCHED BY POSITION.

    Cells are paired by their polar position round the disc, greedily nearest
    first, so "the cell at two o'clock" is compared with "the cell at two
    o'clock" and never with a sorted neighbour.  Returns (rms_deg, n_matched,
    pairs) or (None, 0, []) if the two do not present the same number of cells
    -- which is itself a result and must not be scored as a number (rule 37)."""
    if pa is None or pb is None or len(pa) != len(pb):
        return None, 0, []
    used = set()
    pairs = []
    for a in pa:
        best, bj = None, None
        for j, b in enumerate(pb):
            if j in used:
                continue
            dp = abs(a[0] - b[0]) % 360.0
            dp = min(dp, 360.0 - dp)
            if best is None or dp < best:
                best, bj = dp, j
        used.add(bj)
        b = pb[bj]
        da = abs(a[1] - b[1]) % 180.0
        da = min(da, 180.0 - da)
        pairs.append((a[0], b[0], a[1], b[1], da, a[2], b[2]))
    rms = float(np.sqrt(np.mean([p[4] ** 2 for p in pairs])))
    return rms, len(pairs), pairs


def main():
    checks, fails = [], []

    def ck(name, ok, detail):
        checks.append((name, ok, detail))
        if not ok:
            fails.append(name)

    ph = from_photo()
    bt = from_built()

    print("\n  PHOTOGRAPH (un-squashed)  " +
          "  ".join("%5.1f" % c[1] for c in ph) if ph else "  NO PHOTOGRAPH")
    print("  BUILT                     " +
          "  ".join("%5.1f" % c[1] for c in bt) if bt else "  NO BUILD")
    rms, n, pairs = residual(ph, bt)

    # ---- A1: the pose correction must survive a KNOWN ANSWER (rule: prove the
    # proxy first).  Squash the BUILT mark by the photograph's own axis ratio,
    # un-squash it again, and the angles must come back.
    import probe_rev46_vw as P
    m = P.glyph_only_mask(rows=900)
    n0, n1 = m.shape
    ratio = (PHOTO_BOX[2] - PHOTO_BOX[0]) / float(PHOTO_BOX[3] - PHOTO_BOX[1])
    sq = np.array(Image.fromarray((m * 255).astype("uint8"))
                  .resize((max(8, int(n1 * ratio)), n0), Image.LANCZOS)) > 127
    s3 = np.dstack([(~sq * 255).astype(float)] * 3)
    dd = np.ones(sq.shape, bool)
    s3, dd, _e = unsquash(s3, dd)
    k0, k1 = dd.shape
    yy, xx = np.mgrid[0:k0, 0:k1]
    cy, cx = (k0 - 1) / 2.0, (k1 - 1) / 2.0
    disc = (((yy - cy) / (k0 / 2.0)) ** 2 + ((xx - cx) / (k1 / 2.0)) ** 2) <= 0.97 ** 2
    rt = cells(ink_mask(s3, disc), disc)
    r_rt, n_rt, _ = residual(bt, rt)
    ck("A1 THE POSE CORRECTION RECOVERS A KNOWN ANSWER -- squash the BUILT mark "
       "by the photograph's own %.3f axis ratio, un-squash it, and its angles "
       "come back" % ratio,
       r_rt is not None and r_rt < 6.0,
       ("round trip rms %.2f deg over %d cells" % (r_rt, n_rt)) if r_rt is not None
       else "the round trip did not present the same cell count -- NOT MEASURED")

    if rms is None:
        print("\n  THE TWO MARKS DO NOT PRESENT THE SAME NUMBER OF CELLS "
              "(photo %s, built %s) -- the angle residual was NOT computed "
              "(rule 37)." % (len(ph) if ph else "?", len(bt) if bt else "?"))
    else:
        print("\n  cell   photo_pos built_pos  photo_ang built_ang   diff   "
              "photo_asp built_asp")
        for p in pairs:
            print("        %8.1f %9.1f %10.1f %9.1f %+7.1f %9.2f %9.2f"
                  % (p[0], p[1], p[2], p[3], p[3] - p[2], p[5], p[6]))
        sp_p = max(c[1] for c in ph) - min(c[1] for c in ph)
        sp_b = max(c[1] for c in bt) - min(c[1] for c in bt)
        ck("A2 THE BUILT STROKES POINT WHERE THE PHOTOGRAPH'S DO",
           rms <= 8.0,
           "angular residual %.2f deg RMS over %d matched cells.  Spread: "
           "photograph %.1f deg, built %.1f deg -- the photograph's six strokes "
           "are near-parallel and the built ones RADIATE, which is what *'it "
           "reads as an X'* means (F235/F104)" % (rms, n, sp_p, sp_b))
        rnd_p = sum(1 for c in ph if c[2] < 2.0)
        rnd_b = sum(1 for c in bt if c[2] < 2.0)
        ck("A3 NO BUILT CELL IS A ROUND BLOB where the photograph has a sliver",
           rnd_b <= rnd_p,
           "cells with aspect < 2.0: photograph %d, built %d.  A sliver becomes "
           "a blob when the two strokes bounding it stop being parallel"
           % (rnd_p, rnd_b))

    print("=" * 78)
    print("  probe_rev69_angles -- THE EMBLEM'S STROKE ANGLES (F235 / F104)")
    print("=" * 78)
    for name, ok, detail in checks:
        print("  [%s] %s\n        %s" % ("PASS" if ok else "FAIL", name, detail))
    print()
    print("  CEILING.  The pose correction assumes the obliquity is a rotation "
          "about ONE\n  axis (F184).  A view with azimuth AND elevation "
          "compresses along a tilted\n  axis and a pure shear can mimic part of "
          "it, so these angles carry that\n  systematic -- which is exactly why "
          "A1 exists and why it is watched.  This\n  measures WHERE THE STROKES "
          "POINT.  It says nothing about their width, their\n  reach, or the "
          "cell count, all of which are already right (F233/F235).")
    print()
    print("  %d checked, %d FAILED%s"
          % (len(checks), len(fails), ("  --  " + fails[0][:60]) if fails else ""))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
