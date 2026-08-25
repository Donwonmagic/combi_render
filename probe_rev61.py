#!/usr/bin/env python3
"""probe_rev61.py -- the four instruments rev 61 published figures from.

WHY THIS FILE EXISTS.  An independent adversary auditing rev 61's outgoing
handoff found that FOUR of its headline results rested on instruments that were
never committed: the 8,174-candidate emblem solve, the cream's low-frequency
blotch, the T1_WORLD mirror/paint trade, and the bulb saturation ratio.  In a
project whose rule 8 is "a measurement's window is part of the measurement" and
whose rule 4 is "every instrument is wrong at least once", a figure whose
instrument cannot be re-run, re-windowed or ablated is a CLAIM, not a
measurement.  All four are here now.

EVERY MODE PAINTS ITS WINDOW.  Pass --paint and look at out/p61_*.png BEFORE
quoting any number this file prints.  Rev 61 threw away ELEVEN painted windows,
every one of which produced a plausible number first -- one landed on a child's
hair, one on the white background, one read the RIDE DROP as a 70 mm defect.

READ THIS PROBE'S OWN SUMMARY LINES, NEVER ITS EXIT CODE (rule 9).

    python3 probe_rev61.py emblem [--budget SECONDS]
    python3 probe_rev61.py blotch  [--paint]
    python3 probe_rev61.py world   [--paint]
    python3 probe_rev61.py bulb    [--paint]
"""
import sys, os, io, time, random, contextlib
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
OUT = os.path.join(HERE, "out")


def _need(path):
    if not os.path.exists(path):
        print("  NO RENDER: %s -- render before quoting this probe (rule 37)" % path)
        sys.exit(2)
    return path


def _paint(img, mask, box, name):
    """Write the selection as an overlay.  Rule 8: painted BEFORE the number."""
    o = np.asarray(img.convert("RGB")).copy()
    y0, y1, x0, x1 = box
    sub = o[y0:y1, x0:x1]
    sub[mask] = [0, 255, 0]
    o[y0:y1, x0:x1] = sub
    os.makedirs(OUT, exist_ok=True)
    Image.fromarray(o).save(os.path.join(OUT, "p61_%s.png" % name))
    print("     painted window -> out/p61_%s.png   LOOK AT IT" % name)


# ---------------------------------------------------------------- 1. EMBLEM
def emblem(budget=420.0):
    """Max cream-cell elongation subject to C4's OWN landmark bar.

    THE RESULT THIS PRODUCED: 1.634 against a photographed 3.39, over 8,174
    candidates -- i.e. the landmark set L1-L6 and the photograph's cell shape
    are INCOMPATIBLE.  Dropping the constraint reaches 4.644, so the
    CONSTRUCTION can make slivers and the LANDMARKS forbid it.

    It uses probe_rev46_vw's OWN functions -- err, built_landmarks,
    glyph_only_mask, cell_elongation -- never a second copy of them, because a
    second copy of a measurement is how one of them gets quietly relaxed.
    `bpy` is a pip module here, so this runs in plain python3 at ~0.02 s per
    candidate; it does NOT need the Blender CLI.
    """
    with contextlib.redirect_stdout(io.StringIO()):
        import probe_rev46_vw as P
    base = dict(P.CURRENT)
    keys = list(base)

    def ev(prm):
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                e, lc = P.err(P.built_landmarks(**prm))
                if lc is None:
                    return None
                m = P.glyph_only_mask(**prm)
                return e, P.cell_elongation(m, 1.0), P.cream_cells(m)[0]
        except Exception:
            return None

    b = ev(base)
    print("  probe_rev61 emblem -- max C8 elongation under C4's own bar")
    print("     baseline   residual %.4f  elongation %.3f  cells %d" % b)
    span = {"VW_V_TIP_X": .18, "VW_APEX_Z": .10, "VW_W_ARM_X": .20,
            "VW_W_ARM_Z": .35, "VW_W_TROUGH_X": .18, "VW_W_TROUGH_Z": .18}
    for label, constrained in (("CONSTRAINED (residual < 0.045, cells == 6)", True),
                               ("UNCONSTRAINED (cells == 6 only)", False)):
        random.seed(7)
        best = (b[0], b[1], b[2], dict(base))
        pool, n, t0 = [dict(base)], 0, time.time()
        while time.time() - t0 < budget / 2.0:
            seed = random.choice(pool)
            prm = {k: seed[k] + random.gauss(0, span[k] * .30) for k in keys}
            r = ev(prm)
            n += 1
            if not r:
                continue
            e, el, cells = r
            if cells == 6 and el > best[1] and (e < 0.045 or not constrained):
                best = (e, el, cells, prm)
                pool.append(prm)
                pool = pool[-12:]
        print("     %-42s %d candidates  BEST elongation %.3f (residual %.4f)"
              % (label, n, best[1], best[0]))
    print("     photograph 3.39.  A PLAIN CROSS reads 1.39.")
    print("  emblem: the CONSTRAINED ceiling is the finding -- if it is far below")
    print("          3.39 then L1-L6 and the photograph's cell shape disagree.")


# ---------------------------------------------------------------- 2. BLOTCH
_BLOTCH = {  # frame -> (box, lum floor, low-pass sigma, roundel vertical D)
    "photo":  ("ref_playa_34.png", (175, 215, 60, 135), 130, 2.0, 27),
    "render": (None,               (625, 700, 600, 1010), 120, 9.3, 125),
}


def _cream(img, box, lo):
    a = np.asarray(img.convert("RGB")).astype(float)
    y0, y1, x0, x1 = box
    w = a[y0:y1, x0:x1]
    lum = w.mean(2)
    sat = (w.max(2) - w.min(2)) / np.maximum(w.max(2), 1)
    m = (lum > lo) & (sat < 0.22)
    m = ndi.binary_erosion(m, np.ones((5, 5)))
    lab, n = ndi.label(m)
    if n == 0:
        return lum, m
    sz = ndi.sum(m, lab, range(1, n + 1))
    return lum, lab == int(np.argmax(sz)) + 1


def blotch(frame=None, paint=False):
    """Low-frequency blotch of the NOSE CREAM, matched by the roundel's scale.

    (p95-p05)/mean of the low-passed cream.  Rev 61 measured photograph 7.8 %,
    render 11.8 %, and then ABLATED: T1_MOT_AMP 0.55 -> 0.30 -> 0.00 gives
    11.8 -> 11.9 -> 11.9 %.  At AMP = 0 the mottle texture is GONE and the
    number does not move, so the blotch is the SHADING GRADIENT on the curved
    nose panel, not the mottle (F147).

    ITS CEILING, AND IT IS REAL: the ablation clears the render-to-render noise
    floor by only ~0.06 DN in the mean on the cream.  Two settings-identical
    renders differ by 0.35 DN mean-abs on that window.  The conclusion needs a
    REPEAT, not a single run -- rev 60c's own lesson (G4 was published as
    0.360 +- 0.002 from five runs, with "a variant is not a repeat" spelled out).
    """
    frame = frame or os.path.join(OUT, "r61f_front.png")
    rows = []
    for tag, (path, box, lo, sigma, _rd) in _BLOTCH.items():
        p = _need(path if path else frame)
        im = Image.open(p)
        lum, m = _cream(im, box, lo)
        if m.sum() < 200:
            print("  %s: SELECTION TOO SMALL (%d px) -- window is wrong" % (tag, m.sum()))
            continue
        f = lum.copy()
        f[~m] = lum[m].mean()
        v = ndi.gaussian_filter(f, sigma)[m]
        r = (np.percentile(v, 95) - np.percentile(v, 5)) / v.mean()
        print("  %-7s %-22s n %6d  mean %6.1f  sigma %4.1f  BLOTCH %5.1f %%"
              % (tag, os.path.basename(p), m.sum(), lum[m].mean(), sigma, r * 100))
        if paint:
            _paint(im, m, box, "blotch_" + tag)
        rows.append(r)
    if len(rows) == 2:
        print("  blotch: render / photograph = %.2fx" % (rows[1] / rows[0]))


# ----------------------------------------------------------------- 3. WORLD
def world(paint=False):
    """The T1_WORLD trade: what brightening the world costs the paint.

    Windows are FIXED here so the trade is re-measurable: the mirror head and
    the nose red on studio.py's "front" camera.  Rev 61 measured, across
    T1_WORLD 0.05 / 0.30 / 1.00: mirror 100.2 / 132.1 / 169.6 DN, nose-red
    saturation 0.459 / 0.430 / 0.377, cream 140.2 / 150.9 / 170.7 (F148).

    THE POINT: the shipped 0.05 gives the HIGHEST red saturation of the three,
    and the render's red is already below every reference -- so raising the
    world costs the paint more than it gains the metal.  An adversary
    reproduced the DIRECTION and the RATIO on a different red window
    (0.749 -> 0.611, 1.226x against this window's 1.218x).
    """
    frames = [(v, os.path.join(OUT, "w%s_front.png" % v)) for v in ("0.05", "0.30", "1.00")]
    print("  probe_rev61 world -- T1_WORLD's cost to the paint")
    print("     T1_WORLD   mirror DN   nose-red sRGB          red sat   cream DN")
    for v, p in frames:
        if not os.path.exists(p):
            print("     %s      NO RENDER %s" % (v, os.path.basename(p)))
            continue
        im = Image.open(p)
        a = np.asarray(im.convert("RGB")).astype(float)
        mh = a[530:585, 320:355].reshape(-1, 3)
        dark = mh[mh.mean(1) < 200]                 # exclude the white backdrop
        red = a[880:930, 640:760].reshape(-1, 3)
        s = (red.max(1) - red.min(1)) / np.maximum(red.max(1), 1)
        cr = a[625:700, 600:1010].reshape(-1, 3)
        print("      %s      %6.1f    %s   %.3f    %.1f"
              % (v, dark.mean(), red.mean(0).round(0), s.mean(), cr.mean()))
        if paint and v == "0.05":
            box = (530, 585, 320, 355)
            sub = a[box[0]:box[1], box[2]:box[3]]
            _paint(im, sub.mean(2) < 200, box, "world_mirror")


# ------------------------------------------------------------------ 4. BULB
def bulb(paint=False):
    """The festoon bulbs' saturation against their OWN adjacent cream.

    Scale-, exposure- and white-balance-free.  Rev 61 measured ref_side.jpg
    4.96, ref_rear34.jpg's aft coaming rail 3.82, render 1.40 -- the render
    2.8-3.6x short, corroborated on two independent scenes (F144).  Then BOTH
    levers were ablated and BOTH failed: T1_BULB_STR=60 moves it 1.40 -> 0.88
    (WORSE -- the bead clips toward white and clipped pixels are neutral) and
    T1_BULB_BASEV=0.30 moves it 1.40 -> 1.50 (nothing).

    THE WINDOWS MATTER MORE THAN USUAL HERE.  A first ref_rear34 window
    swallowed the MURAL LID and returned a believable 4.48 against the true
    3.82.  The rail window is restricted to a band within 7 px of the coaming
    centreline for exactly that reason.
    """
    def sat(p):
        mx = p.max(-1).astype(float)
        mn = p.min(-1).astype(float)
        return np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)

    print("  probe_rev61 bulb -- bead saturation / its OWN adjacent cream")
    specs = [("ref_side.jpg",  (299, 309, 430, 690), (321, 329, 430, 690)),
             (os.path.join(OUT, "r61f_side.png"),
                              (485, 493, 600, 1200), (508, 516, 600, 1200))]
    for path, bb, cb in specs:
        if not os.path.exists(path):
            print("     NO RENDER %s" % os.path.basename(path))
            continue
        im = Image.open(path)
        a = np.asarray(im.convert("RGB")).astype(float)
        w = a[bb[0]:bb[1], bb[2]:bb[3]]
        s = sat(w)
        sel = s >= np.percentile(s, 70)
        b = w[sel]
        c = a[cb[0]:cb[1], cb[2]:cb[3]].reshape(-1, 3)
        sb, sc = sat(b).mean(), sat(c).mean()
        print("     %-22s bulb %s sat %.3f | cream sat %.3f | RATIO %.2f"
              % (os.path.basename(path), b.mean(0).round(0), sb, sc, sb / sc))
        if paint:
            _paint(im, sel, bb, "bulb_" + os.path.basename(path).split(".")[0])
    print("     ref_rear34.jpg's aft coaming rail read 3.82 on a band within 7 px")
    print("     of the rail centreline; an unrestricted window swallowed the MURAL")
    print("     LID and returned a believable 4.48.  Paint it before you trust it.")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    pn = "--paint" in sys.argv
    if mode == "emblem":
        bg = 420.0
        if "--budget" in sys.argv:
            bg = float(sys.argv[sys.argv.index("--budget") + 1])
        emblem(bg)
    elif mode == "blotch":
        blotch(paint=pn)
    elif mode == "world":
        world(paint=pn)
    elif mode == "bulb":
        bulb(paint=pn)
    else:
        print(__doc__)
        sys.exit(2)
