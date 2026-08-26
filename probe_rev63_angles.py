"""rev 63 -- A DIFFERENT METHOD: FIT THE SIX CONTACT ANGLES OFF THE PHOTOGRAPH.

WHY A DIFFERENT METHOD.  Every search this project has run -- rev 46's
landmarks, F103's cell-count solve, rev 62's IoU, rev 63's canonical IoU, and
rev 63's joint C6+C8+IoU fit -- optimises SCALARS SQUEEZED OUT OF THE BADGE.
F175 showed three of them can pass together on a glyph that renders as a Y, and
the chamfer test showed the workshop badge is too degraded a target to separate
a fan from a VW at all.  **The target was the problem, not the metric.**

WHAT THIS DOES INSTEAD.  It measures, on the PHOTOGRAPH, the one thing that
determines how the mark reads: **WHERE round the ring each of the six strokes
lands.**  Those six angles are a direct geometric description of the mark, they
survive foreshortening once the badge is de-squashed, and -- this is why it is
tractable -- `vw_bars` projects every terminal radially onto the band circle
with `_on_band`, so **each spine constant's ANGLE is exactly what this
measures.**  The fit is then six numbers to six numbers, not a scalar proxy.

HOW A CONTACT IS FOUND.  Sample ink on a circle just inside the ring band and
take the angular runs.  The band itself is ink at EVERY angle, so the sampling
radius must sit inboard of it; a run of ink there is a stroke crossing.

CONTROLS
  A1  the sampling circle is PAINTED on every frame before any angle is used
      (rule 8 -- five of nine wrong instruments in one revision were a mask).
  A2  the radius is SWEPT.  A single radius is a window, and a window is part
      of the measurement (rule 39).
  A3  the two independent photographs must AGREE -- the target bus's own nose
      badge and the workshop badge are different vehicles but the SAME factory
      pressing, and the pressing is geometry, which transfers (rule 11).
  A4  KILL: run it on the BUILT shipped glyph, whose answer is known from
      probe_rev63_reach.py -- it must report the two floating W arms as missing.
"""
import os
import sys

import numpy as np
import scipy.ndimage as ndi
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.join(HERE, "probe_scratch")
_fail = []


def ctl(n, ok, m):
    if not ok:
        _fail.append(n)
    print("    %-4s %s  %s" % (n, "ok  " if ok else "FAIL", m))


def desquash(im, k):
    return im.resize((int(round(im.width * k)), im.height), Image.LANCZOS)


def nolita():
    """The TARGET BUS's own nose badge.  Its own red segmentation, the same one
    probe_rev46_vw.py uses, and de-foreshortened by the crop's own aspect."""
    a = np.asarray(Image.open(os.path.join(HERE, "ref_nolita_front34.jpg"))
                   .convert("RGB")).astype(float)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    red = (R > 110) & (G < 0.60 * R) & (B < 0.60 * R)
    lab, _ = ndi.label(red)
    sub = lab[192:261, 153:194]
    ids, cnt = np.unique(sub[sub > 0], return_counts=True)
    m = (sub == ids[int(np.argmax(cnt))])
    im = Image.fromarray((m * 255).astype(np.uint8))
    return np.asarray(desquash(im, m.shape[0] / float(m.shape[1]))) > 127


def workshop():
    """The WORKSHOP badge -- a different vehicle, the SAME factory pressing.
    Geometry transfers between them; paint and artwork do not (rule 11).
    Segmentation and squash are probe_rev62_emblem.py's, F09's conic."""
    W = np.asarray(Image.open(os.path.join(HERE, "ref_workshop.jpg"))
                   .convert("RGB")).astype(float)
    sub = W.mean(axis=2)[498:599, 270:340]
    m = ndi.binary_closing(sub < 165, np.ones((3, 3)))
    im = Image.fromarray((m * 255).astype(np.uint8))
    return np.asarray(desquash(im, 92.728 / 63.299)) > 127


def runs_at(mask, frac, paint=None, title=""):
    """Angular runs of ink on the circle at `frac` of the badge radius.
    -> (list of run-centre angles, list of run widths in degrees)."""
    ys, xs = np.nonzero(mask)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    cy, cx = (y0 + y1) / 2.0, (x0 + x1) / 2.0
    ry, rx = (y1 - y0) / 2.0, (x1 - x0) / 2.0
    th = np.arange(0, 3600) / 10.0
    sy = cy - np.sin(np.radians(th)) * ry * frac
    sx = cx + np.cos(np.radians(th)) * rx * frac
    ok = ((sy >= 0) & (sy < mask.shape[0]) & (sx >= 0) & (sx < mask.shape[1]))
    v = np.zeros(len(th), bool)
    v[ok] = mask[np.round(sy[ok]).astype(int), np.round(sx[ok]).astype(int)]
    # angular runs, wrapping
    idx = np.where(v)[0]
    runs = []
    if len(idx):
        splits = np.where(np.diff(idx) > 1)[0]
        groups = np.split(idx, splits + 1)
        if len(groups) > 1 and groups[0][0] == 0 and groups[-1][-1] == len(th) - 1:
            groups[0] = np.concatenate([groups[-1], groups[0]])
            groups.pop()
        for g in groups:
            wdeg = len(g) / 10.0
            if wdeg < 4.0:
                continue
            ang = np.degrees(np.arctan2(
                np.sin(np.radians(th[g])).mean(),
                np.cos(np.radians(th[g])).mean())) % 360.0
            runs.append((float(ang), float(wdeg)))
    runs.sort()
    if paint:
        rgb = np.zeros(mask.shape + (3,), np.uint8)
        rgb[mask] = (225, 225, 225)
        for i in range(len(th)):
            yy, xx = int(round(sy[i])), int(round(sx[i]))
            if 0 <= yy < mask.shape[0] and 0 <= xx < mask.shape[1]:
                rgb[yy, xx] = (255, 40, 40) if v[i] else (40, 120, 255)
        Image.fromarray(rgb).resize((mask.shape[1] * 4, mask.shape[0] * 4),
                                    Image.NEAREST).save(
            os.path.join(SCRATCH, paint))
    return [r[0] for r in runs], [r[1] for r in runs]


if __name__ == "__main__":
    print("")
    print("  THE SIX CONTACT ANGLES, MEASURED ON THE REAL MARK")
    print("  (0 = 3 o'clock, 90 = 12 o'clock; both frames de-foreshortened)")
    print("")
    FR = 0.72
    for nm, mk, pf in (("TARGET BUS nose badge", nolita(), "rev63_ang_nolita.png"),
                       ("WORKSHOP badge", workshop(), "rev63_ang_workshop.png")):
        a, w = runs_at(mk, FR, paint=pf, title=nm)
        print("        %-24s %d strokes at %s"
              % (nm, len(a), ", ".join("%3.0f" % v for v in a)))
        print("        %-24s   widths      %s"
              % ("", ", ".join("%3.0f" % v for v in w)))
    print("")
    print("  A2 -- SWEPT, because one radius is a window (rule 39)")
    for fr in (0.62, 0.67, 0.72, 0.77, 0.82):
        a1, _ = runs_at(nolita(), fr)
        a2, _ = runs_at(workshop(), fr)
        print("        r=%.2f   target bus %d strokes   workshop %d strokes"
              % (fr, len(a1), len(a2)))
    print("")
    print("  A1 -- painted rev63_ang_nolita.png / rev63_ang_workshop.png")
    print("        (sampling circle drawn: RED where it is on ink, BLUE where")
    print("         it is on cream).  LOOK before using any angle above.")
