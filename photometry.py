# photometry.py -- rev 71.  THE MEASUREMENT PROTOCOL, AS CODE RATHER THAN PROSE.
#
# WHY THIS FILE EXISTS.  Rev 71 spent most of itself finding SIX defects in its
# OWN instruments, and every one was a violation of one of four rules.  Each
# produced a plausible, publishable number; each was caught only by painting or
# by a control.  They are encoded here so the next context inherits the fix
# instead of the lesson:
#
#   1. READ IN LINEAR, AND ONLY WHERE LINEAR IS RECOVERABLE.  An 8-bit sRGB
#      channel RATIO is not a physical quantity -- gamma is non-linear, so a
#      ratio depends on absolute brightness.  Worse, inverse-sRGB does NOT undo
#      AgX.  Read through AgX, rev 71's red ratio moved with EXPOSURE and read
#      3.43x where the truth was 1.73x.
#   2. REFUSE CLIPPED DATA.  A clipped denominator cannot rise, so every ratio
#      against it reads high.  Rev 71 measured a "relight" three times and every
#      gain was the cream denominator clipping.  The relight was worth nothing.
#   3. USE A ROBUST STATISTIC.  The red's authored G albedo is 0.0294 and the
#      cream's is 0.6308 -- twenty times larger -- so a 15 % tail of contaminant
#      tiles DOUBLES the mean G while barely moving R.  Median, not mean.
#   4. PAINT THE WINDOW AND LOOK BEFORE PUBLISHING ANY NUMBER FROM IT.  Four of
#      rev 71's windows were wrong: two selected the wall and the mural behind
#      the bus, one was mostly board cream, one sat on the galley interior seen
#      through the serving apertures.  `tiles()` writes its own paint every call.
#
# AND THE FIFTH, WHICH IS NOT ABOUT PIXELS: A CONTROL MUST BE FRAMED THE WAY ITS
# MEASUREMENT IS FRAMED (F246), AND AN INSTRUMENT MAY BE BLIND TO WHAT MATTERS
# (F262: a silhouette IoU ranked a visibly shattered glyph ABOVE the shipped
# one).  No module can enforce those.  Render it, crop it, and look.
import os

import numpy as np
from PIL import Image

CLIP = 0.999
UNIFORM = 7.0 / 255.0        # per-channel sd inside a tile, in 0..1 units


def load_linear(path):
    """Return (array in 0..1, is_linear).

    A 16-bit PNG written under Blender's 'Raw' view transform is ALREADY
    scene-linear and must NOT be inverse-sRGB'd.  An 8-bit frame written under
    'Standard' carries sRGB encoding and must be.  A frame written under AgX
    cannot be linearised at all and this returns is_linear=False, so callers
    can refuse it (rule 1)."""
    im = Image.open(path)
    a = np.asarray(im).astype(float)[..., :3]
    if a.max() > 255.0:                       # 16-bit: assume Raw/linear
        return a / 65535.0, True
    a = a / 255.0
    lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    return lin, True


def clipped(a, boxes):
    """Fraction of pixels in `boxes` at or above the clip ceiling."""
    px = np.vstack([a[y0:y1, x0:x1].reshape(-1, 3) for (x0, y0, x1, y1) in boxes])
    return float((px.max(1) >= CLIP).mean())


def tiles(a, boxes, keep=None, tsz=8, step=4, paint=None, base=None):
    """Uniform tiles inside `boxes`, as a MEDIAN linear colour (rule 3).

    `keep(mean_rgb) -> bool` selects tiles.  Select by POSITION, BRIGHTNESS or
    ORDERING -- never by the quantity you are about to report, which is a
    tautology (rule 6).  `paint` writes the selection to that path so it can be
    LOOKED AT before the number is used (rule 4); `base` is the 8-bit image to
    paint onto, defaulting to a gamma of `a`.
    Returns (median_rgb, n_tiles) or (None, 0)."""
    got, marks = [], []
    for (x0, y0, x1, y1) in boxes:
        for y in range(y0, y1 - tsz, step):
            for x in range(x0, x1 - tsz, step):
                t = a[y:y + tsz, x:x + tsz].reshape(-1, 3)
                if t.std(0).max() > UNIFORM * (a.max() or 1.0):
                    continue
                m = t.mean(0)
                if keep is not None and not keep(m):
                    continue
                got.append(m)
                marks.append((x, y))
    if paint is not None and marks:
        img = base if base is not None else (np.clip(a, 0, 1) ** (1 / 2.2) * 255)
        o = np.array(img, dtype=float)[..., :3].copy()
        for (x, y) in marks:
            o[y:y + tsz, x:x + tsz] = o[y:y + tsz, x:x + tsz] * 0.4 + np.array([0, 255, 0]) * 0.6
        os.makedirs(os.path.dirname(paint) or ".", exist_ok=True)
        Image.fromarray(o.astype("uint8")).save(paint)
    if len(got) < 10:
        return None, 0
    return np.median(np.array(got), axis=0), len(got)


def ratio(a, red_boxes, cream_boxes, red_keep, cream_keep, paint_stem=None):
    """One surface against another IN THE SAME IMAGE, so the illuminant and the
    exposure cancel (probe_rev70_tyre's pattern).  REFUSES if the denominator
    is clipped (rule 2).  Returns (ratio_rgb, note)."""
    cf = clipped(a, cream_boxes)
    if cf > 0.05:
        return None, ("REFUSED: %.0f %% of the reference window is CLIPPED. A "
                      "clipped denominator cannot rise, so the ratio would read "
                      "high and the number would be exposure, not shape." % (100 * cf))
    r, nr = tiles(a, red_boxes, red_keep,
                  paint=(paint_stem + "_num.png") if paint_stem else None)
    c, nc = tiles(a, cream_boxes, cream_keep,
                  paint=(paint_stem + "_den.png") if paint_stem else None)
    if r is None or c is None:
        return None, "REFUSED: window empty (%d / %d tiles)" % (nr, nc)
    return r / c, "%d / %d tiles, clip %.1f %%" % (nr, nc, 100 * cf)


def selftest():
    """Prove the protocol on a KNOWN answer before trusting it (rule 3 of the
    project canon).  A synthetic frame with two flat patches of known linear
    value must return their exact ratio, and a clipped one must REFUSE."""
    ok = []
    a = np.zeros((120, 240, 3))
    a[:, :120] = (0.5520, 0.0294, 0.0176)          # the authored RED
    a[:, 120:] = (0.6172, 0.6308, 0.5776)          # the authored CREAM
    want = np.array([0.5520, 0.0294, 0.0176]) / np.array([0.6172, 0.6308, 0.5776])
    got, note = ratio(a, [(4, 4, 116, 116)], [(124, 4, 236, 116)],
                      lambda m: m[0] > m[1], lambda m: m[1] > 0.4)
    ok.append(("recovers a known ratio exactly",
               got is not None and np.allclose(got, want, rtol=1e-6)))
    b = a.copy(); b[:, 120:] = 1.0                  # blow the denominator out
    got2, note2 = ratio(b, [(4, 4, 116, 116)], [(124, 4, 236, 116)],
                        lambda m: m[0] > m[1], lambda m: m[1] > 0.4)
    ok.append(("REFUSES a clipped denominator", got2 is None and "CLIPPED" in note2))
    c = a.copy()
    c[:20, :120] = (0.6172, 0.6308, 0.5776)         # 17 % contaminant tiles
    got3, _ = ratio(c, [(4, 4, 116, 116)], [(124, 4, 236, 116)],
                    lambda m: m[0] > m[1], lambda m: m[1] > 0.4)
    ok.append(("a contaminant tail does NOT move the median",
               got3 is not None and abs(got3[1] - want[1]) < 0.01 * want[1]))
    for name, good in ok:
        print("  [%s] %s" % ("PASS" if good else "FAIL", name))
    n_bad = sum(1 for _, g in ok if not g)
    print("\n  %d checked, %d FAILED" % (len(ok), n_bad))
    return n_bad


if __name__ == "__main__":
    raise SystemExit(1 if selftest() else 0)
