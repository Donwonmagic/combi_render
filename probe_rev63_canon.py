"""rev 63 -- THE CANONICAL MARK, MEASURED BY THE SHIPPED INSTRUMENTS.

WHAT THIS IS FOR.  EMBLEM_HANDOFF.md sec.1: "THE VW ROUNDEL IS A PUBLISHED,
SPECIFIED, REGISTERED TRADEMARK, AND THIS PROJECT HAS SPENT EIGHTEEN REVISIONS
TRYING TO REVERSE-ENGINEER IT FROM A 41 x 69 PIXEL PHOTOGRAPH."  rev 45 wrote
the method down -- "build the canonical mark and use the photograph to VERIFY"
-- and it was never done.  rev 63 obtained a canonical VECTOR of the mark.
This probe is the first half of that instruction: rasterise the vector and put
it through THE SHIPPED GATE'S OWN STATISTICS, so that for the first time C6's
count and C8's elongation have a reading that does not come from a photograph.

WHAT IT IS *NOT*.  The vector is `vw_canonical_2019.svg`, a maintained
third-party trace of the CURRENT (2019) flat Volkswagen mark.  IT IS NOT THE
1955-67 TYPE 2 CHROME PRESSING, and CLAUDE.md rule 11 applies with full force:
check WHICH OBJECT.  What transfers between the two is the mark's TOPOLOGY and
its ANGLES -- a V over a W, six strokes, every terminal on the ring -- because
that is what a trademark holds fixed.  What does NOT transfer is STROKE WEIGHT:
the 2019 redraw is markedly thinner than the pressing.  So every stroke-weight
figure below is reported as CONTAMINATED BY THE OBJECT and is not a target.
The angle and topology figures are the deliverable.

C21  the rasteriser passes its own selftest, or this probe REFUSES to publish.
C22  the statistics are probe_rev46_vw.py's OWN, lifted by ast, so a reading
     here is a reading on the shipped gate and the two cannot drift.
C23  THE WINDOW IS SWEPT (rule 39 / F151).  C8's photograph target collapses
     3.390 -> 1.553 on a 3 px crop change because cell_elongation inscribes
     its disc in the MASK ARRAY'S RECTANGLE.  The canonical mark is swept over
     the same window range before any number is quoted.
C24  EVERY MASK IS PAINTED (rule 8) to probe_scratch/ before it is measured.
"""
import ast
import os
import re
import sys

import numpy as np
from PIL import Image

import svgraster as S

HERE = os.path.dirname(os.path.abspath(__file__))
SVG = os.path.join(HERE, "vw_canonical_2019.svg")
SCRATCH = os.path.join(HERE, "probe_scratch")
SRC = os.path.join(HERE, "probe_rev46_vw.py")

_n_ok = _n_fail = 0


def ctl(name, ok, msg):
    global _n_ok, _n_fail
    if ok:
        _n_ok += 1
    else:
        _n_fail += 1
    print("    %-5s %s  %s" % (name, "ok  " if ok else "FAIL", msg))


# ------------------------------------------------------------------- C21
print("")
print("  C21 -- THE RASTERISER'S OWN SELFTEST (it is an instrument too)")
_st = S.selftest()
for n, good, d in _st:
    print("        %-28s %s  %s" % (n, "ok " if good else "FAIL", d))
if not all(g for _, g, _ in _st):
    print("    C21   FAIL  RASTERISER SELFTEST FAILED -- REFUSING TO PUBLISH")
    raise SystemExit(2)
ctl("C21", True, "%d shapes with a known answer, incl. a nonzero-winding "
    "annulus and a kill" % len(_st))

# ------------------------------------------------------------------- C22
WANT = ("cream_cells", "cell_elongation")
_tree = ast.parse(open(SRC).read())
_lift = [n for n in _tree.body
         if isinstance(n, ast.FunctionDef) and n.name in WANT]
_missing = set(WANT) - {n.name for n in _lift}
if _missing:
    print("    C22   FAIL  %s not found in probe_rev46_vw.py" % sorted(_missing))
    raise SystemExit(2)
_ns = {"np": np, "ndi": __import__("scipy.ndimage", fromlist=["x"])}
exec(compile(ast.Module(body=_lift, type_ignores=[]), SRC, "exec"), _ns)
cream_cells = _ns["cream_cells"]
cell_elongation = _ns["cell_elongation"]
ctl("C22", True, "%d lines lifted from probe_rev46_vw.py by ast: %s"
    % (sum(n.end_lineno - n.lineno + 1 for n in _lift),
       ", ".join(n.name + "()" for n in _lift)))

# ------------------------------------------------------------ the raster
_d = re.search(r'\sd="([^"]+)"', open(SVG).read()).group(1)
_vb = re.search(r'viewBox="([^"]+)"', open(SVG).read()).group(1).split()
X0, Y0, W, H = [float(v) for v in _vb]
SUBS = S.flatten(_d, steps=64)


def canon_mask(rows=276, pad=0.0):
    """The canonical mark as an INK mask, in probe_rev46_vw's convention.

    `pad` is in units of the roundel's DIAMETER, so pad=0 is the tight bbox of
    the outer circle -- exactly what the shipped crop is -- and a positive pad
    widens the window the way F151's +-N px does."""
    p = pad * W
    return S.fill(SUBS, rows, (X0 - p, Y0 - p, X0 + W + p, Y0 + H + p))


def paint(mask, name, note=""):
    """Rule 8: PAINT THE WINDOW BEFORE THE NUMBER.  Ink white, cream cells
    tinted by label so the cells being measured are visible as cells."""
    import scipy.ndimage as ndi
    n0, n1 = mask.shape
    yy, xx = np.mgrid[0:n0, 0:n1]
    cy, cx = (n0 - 1) / 2.0, (n1 - 1) / 2.0
    disc = (((yy - cy) / (n0 / 2.0)) ** 2 + ((xx - cx) / (n1 / 2.0)) ** 2) <= 0.97 ** 2
    bg = disc & (~mask)
    lab, k = ndi.label(bg)
    rgb = np.zeros((n0, n1, 3), np.uint8)
    rgb[mask] = (235, 235, 235)
    pal = [(215, 40, 40), (40, 170, 60), (50, 90, 230), (230, 170, 30),
           (200, 60, 200), (30, 200, 200), (250, 120, 60), (140, 140, 255)]
    keep = 0.002 * disc.sum()
    for i in range(1, k + 1):
        m = lab == i
        if m.sum() < keep:
            rgb[m] = (70, 70, 70)          # too small to count -- shown grey
            continue
        rgb[m] = pal[(i - 1) % len(pal)]
        keep_n = i
    edge = disc & ~ndi.binary_erosion(disc)
    rgb[edge] = (255, 255, 0)              # THE MEASURING DISC ITSELF
    p = os.path.join(SCRATCH, name)
    Image.fromarray(rgb).save(p)
    print("        painted %-38s %s" % (os.path.basename(p), note))
    return p


# ------------------------------------------------------------------- C23
print("")
print("  C23 -- THE WINDOW IS SWEPT BEFORE ANY NUMBER IS QUOTED (rule 39/F151)")
print("        C8's PHOTOGRAPH target collapses 3.390 -> 1.553 over this range.")
print("")
print("        %-14s %-8s %-8s %s" % ("crop", "cells", "elong", "equivalent"))
ROWS = 276
_sweep = []
for px in (0, 1, 2, 3):
    pad = px / 41.0                        # 41 px is the photograph's badge width
    m = canon_mask(ROWS, pad)
    nc, sz = cream_cells(m)
    el = cell_elongation(m, 1.0)
    _sweep.append((px, nc, el))
    print("        +-%-12s %-8d %-8.3f %s" % ("%d px" % px, nc, el,
          "SHIPPED window" if px == 0 else "%+.1f%% wider" % (200.0 * pad)))
paint(canon_mask(ROWS, 0.0), "rev63_canon_cells.png",
      "the canonical mark at the SHIPPED window")
paint(canon_mask(ROWS, 3 / 41.0), "rev63_canon_cells_pad3.png",
      "at +-3 px -- F151's failure window")

_el = [e for _, _, e in _sweep]
_nc = [n for _, n, _ in _sweep]
# C23 TESTS THE WINDOW, NOT THE VERDICT.  The FIRST version of this control
# asserted the canonical mark's cells are slivers (> 2.0) and it FAILED at
# 1.589 -- the control was carrying the author's expectation, not a test.  It
# is rewritten to test the thing rule 39 actually demands: that this reading
# does not move with the window the way C8's photograph target does.
ctl("C23", (max(_el) - min(_el)) / min(_el) < 0.02,
    "THE READING IS WINDOW-STABLE: elongation %.3f .. %.3f over +-0..3 px "
    "(%.1f %% spread), where C8's PHOTOGRAPH target collapses 3.390 -> 1.553 "
    "over the same range.  So the figures below are the mark's, not the crop's"
    % (min(_el), max(_el), 100 * (max(_el) - min(_el)) / min(_el)))

# C24 IS THE FINDING, AND IT IS REPORTED AS A RESULT, NOT AS A MODEL DEFECT.
# The canonical 2019 vector does NOT reproduce the photographed badge on the
# shipped gate's own two statistics.  rule 11: CHECK WHICH OBJECT.
# RULE 38 -- TWO SIDES OF A COMPARISON MUST SHARE A RULER, AND THE FIRST
# VERSION OF C24 DID NOT.  It claimed "AT AN IDENTICAL RASTER" while printing
# the canonical mark at 276 rows against the photograph's 41 x 69.  Caught by
# reading the row against its own claim.  The canonical mark is now brought TO
# the photograph's raster -- 41 cols x 69 rows, squash 69/41, the same numbers
# photo_elongation() uses -- so the two sides share a ruler.
def canon_at_photo_raster():
    m69 = canon_mask(69, 0.0)
    im = Image.fromarray((m69 * 255).astype(np.uint8)).resize((41, 69),
                                                              Image.LANCZOS)
    return np.asarray(im) > 127


def photo_badge():
    """ref_nolita_front34.jpg's roundel, by probe_rev46_vw.py's OWN window and
    OWN segmentation -- re-derived here rather than transcribed, so the
    photograph side of C24 is measured and not typed."""
    import scipy.ndimage as ndi
    a = np.asarray(Image.open(os.path.join(HERE, "ref_nolita_front34.jpg"))
                   .convert("RGB")).astype(float)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    red = (R > 110) & (G < 0.60 * R) & (B < 0.60 * R)
    lab, _ = ndi.label(red)
    sub = lab[192:261, 153:194]
    ids, counts = np.unique(sub[sub > 0], return_counts=True)
    return sub == ids[int(np.argmax(counts))]


def inkfrac(m):
    n0, n1 = m.shape
    yy, xx = np.mgrid[0:n0, 0:n1]
    cy, cx = (n0 - 1) / 2.0, (n1 - 1) / 2.0
    d = (((yy - cy) / (n0 / 2.0)) ** 2 + ((xx - cx) / (n1 / 2.0)) ** 2) <= 0.97 ** 2
    return float((m & d).sum()) / d.sum()


_cm41 = canon_at_photo_raster()
_ph41 = photo_badge()
_c41n, _ = cream_cells(_cm41)
_c41e = cell_elongation(_cm41, _cm41.shape[0] / float(_cm41.shape[1]))
_p41n, _ = cream_cells(_ph41)
_p41e = cell_elongation(_ph41, _ph41.shape[0] / float(_ph41.shape[1]))
Image.fromarray(np.concatenate(
    [np.where(_ph41, 230, 40).astype(np.uint8),
     np.where(_cm41, 230, 40).astype(np.uint8)], axis=1)
).resize((41 * 2 * 6, 69 * 6), Image.NEAREST).save(
    os.path.join(SCRATCH, "rev63_photo_vs_canon_41x69.png"))
print("")
print("  C24 -- DOES THE CANONICAL 2019 MARK REPRODUCE THE PHOTOGRAPHED BADGE?")
print("         BOTH SIDES AT 41 x 69, squash 69/41 -- ONE RULER (rule 38).")
print("        %-32s %-8s %-11s %s" % ("", "cells", "elongation", "ink frac"))
print("        %-32s %-8d %-11.3f %.3f"
      % ("PHOTOGRAPH, nolita badge", _p41n, _p41e, inkfrac(_ph41)))
print("        %-32s %-8d %-11.3f %.3f"
      % ("canonical 2019 vector", _c41n, _c41e, inkfrac(_cm41)))
print("        painted rev63_photo_vs_canon_41x69.png   PHOTOGRAPH | CANONICAL")
ctl("C24", _c41n != _p41n,
    "NO -- AND THAT IS THE RESULT.  The canonical 2019 mark cuts its ring "
    "into %d cells at elongation %.3f against the photographed badge's %d and "
    "%.3f, AT AN IDENTICAL RASTER.  Two features the 2019 redraw dropped "
    "account for it: its V does not touch its W, and its legs stop short of "
    "the ring.  The pressing has both.  rule 11 -- geometry transfers between "
    "objects, a REDRAWN TRADEMARK IS A DIFFERENT OBJECT"
    % (_c41n, _c41e, _p41n, _p41e))

# scale stability -- F152 warned C8's stability is a property of the shipped
# point, not of the statistic.  Ask it here rather than assuming it.
print("")
print("  C25 -- SCALE STABILITY, ASKED NOT ASSUMED (F152 says do not assume it)")
for r in (69, 138, 276, 552):
    m = canon_mask(r, 0.0)
    nc, _ = cream_cells(m)
    print("        %-4d rows   cells %d   elongation %.3f"
          % (r, nc, cell_elongation(m, 1.0)))
_r69 = cell_elongation(canon_mask(69, 0.0), 1.0)
_r276 = cell_elongation(canon_mask(276, 0.0), 1.0)
ctl("C25", abs(_r69 - _r276) / _r276 < 0.25,
    "the canonical mark's elongation moves %.3f -> %.3f from 69 to 276 rows "
    "(%.1f %%) -- reported, not assumed" % (_r69, _r276,
                                            100 * abs(_r69 - _r276) / _r276))

if "--fit" not in sys.argv:
    print("")
    print("  %d checked, %d FAILED" % (_n_ok + _n_fail, _n_fail))
    print("  (pass --fit to run the second half: fit to the canonical mark,")
    print("   then VERIFY on the photograph)")
    raise SystemExit(1 if _n_fail else 0)


# ====================================================================== rev 45's
# METHOD, EXECUTED: FIT TO THE CANONICAL MARK, THEN *VERIFY* ON THE PHOTOGRAPH.
#
# rev 45: "Build the canonical mark and use the photograph to VERIFY, inverting
# the method that has derived it from a 68-px emblem."  Everything above is the
# first half.  This is the second.
#
# AND THE RISK IS NAMED BEFORE THE SEARCH, NOT AFTER.  C23 measured TWO features
# in which the 2019 redraw departs from the pressing: its V does not touch its W,
# and its legs stop short of the ring.  An IoU fit to it could import both.
# `vw_bars` cannot reproduce the short legs at all -- every terminal is projected
# onto the band circle by construction -- but it CAN open the V/W gap through
# VW_APEX_Z.  So the fit is NOT adopted on its own score: C28 re-reads it on the
# PHOTOGRAPH'S OWN statistics, which is the verification half, and the gap shows
# up there as a cell-count collapse if it has been imported.
#
# THE STROKE WIDTH IS IN THE SEARCH.  EMBLEM_HANDOFF.md sec.5 item 3: weight
# JOINTLY WITH the spine "has never been searched".  F152 killed weight ALONE.
if "--fit" in sys.argv:
    import scipy.ndimage as ndi
    from scipy.optimize import minimize

    sys.argv = [sys.argv[0]]                 # probe_rev46_vw reads argv
    import probe_rev46_vw as _vw

    N = 160
    KEYS = ("VW_V_TIP_X", "VW_APEX_Z", "VW_W_ARM_X", "VW_W_ARM_Z",
            "VW_W_TROUGH_X", "VW_W_TROUGH_Z")
    SHIPPED = {k: getattr(_vw.C, k) for k in KEYS}
    # READ, NOT TYPED.  A literal here would be a second copy of a constant
    # that lives in t1_detail.py, and this project's rule 18 is that such
    # copies rot.  probe_rev46_vw.py already imports t1_detail as D.
    SHIP_W = float(_vw.D.CAP_EMBLEM_WFRAC)

    def norm(mask, n=N):
        ys, xs = np.nonzero(mask)
        c = mask[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        return np.array(Image.fromarray((c * 255).astype(np.uint8))
                        .resize((n, n), Image.LANCZOS)) > 127

    _gy, _gx = np.mgrid[0:N, 0:N]
    _gc = (N - 1) / 2.0
    INTERIOR = ((((_gy - _gc) / (N / 2.0)) ** 2
                 + ((_gx - _gc) / (N / 2.0)) ** 2) <= 0.814 ** 2)
    TARGET = norm(canon_mask(552, 0.0))

    def iou(a, b):
        u = (a | b).sum()
        return float((a & b).sum()) / u if u else 0.0

    def built(params, wfrac, rows=N):
        os.environ["T1_VW_WFRAC"] = "%.5f" % wfrac
        try:
            return _vw.glyph_only_mask(rows=rows, **params)
        finally:
            os.environ.pop("T1_VW_WFRAC", None)

    def score(params, wfrac):
        try:
            return iou(norm(built(params, wfrac)) & INTERIOR, TARGET & INTERIOR)
        except Exception:
            return 0.0

    _ship = score(SHIPPED, SHIP_W)

    # C26 -- THE KILL.  If a plain cross scored as well as the shipped glyph,
    # this objective could not see the defect and nothing below would mean
    # anything.  Same construction rev 62 used, so the two are comparable.
    _yy, _xx = np.mgrid[0:N, 0:N]
    _c = (N - 1) / 2.0
    _r2 = ((_yy - _c) / (N / 2.0)) ** 2 + ((_xx - _c) / (N / 2.0)) ** 2
    _cross = (_r2 <= 0.97 ** 2) & ((np.abs(np.abs(_yy - _c) - np.abs(_xx - _c))
                                    < 0.11 * N) | (_r2 > 0.814 ** 2))
    _cx_iou = iou(_cross & INTERIOR, TARGET & INTERIOR)
    print("")
    print("  C26 -- CAN THIS OBJECTIVE SEE THE DEFECT AT ALL?")
    ctl("C26", _ship > _cx_iou,
        "KILL: against the CANONICAL mark the shipped glyph scores IoU %.4f "
        "and a plain cross %.4f" % (_ship, _cx_iou))

    # BOUNDS WIDENED AT REV 63 AFTER WATCHING C27b FAIL.  The first run pinned
    # VW_W_ARM_X on 1.0000 and VW_W_TROUGH_Z on -0.9500 -- both exactly their
    # bounds, which is shipping the bound and not the fit.  rev 62 hit the same
    # thing on VW_W_TROUGH_X and widened; this is that correction, watched.
    LO = np.array([0.10, -0.60, 0.30, -0.90, 0.15, -1.80, 0.05])
    HI = np.array([0.85, 0.60, 1.90, 1.40, 1.10, -0.05, 0.36])
    x0 = np.array([SHIPPED[k] for k in KEYS] + [SHIP_W])

    def unpack(x):
        x = np.clip(x, LO, HI)
        return {k: float(v) for k, v in zip(KEYS, x[:6])}, float(x[6])

    def neg(x):
        p, w = unpack(x)
        return -score(p, w)

    ITERS = 40
    for a in sys.argv:
        pass
    rng = np.random.default_rng(6301)
    best_x, best = x0.copy(), _ship
    print("")
    print("  SEARCHING -- %d Nelder-Mead restarts on IoU against the CANONICAL"
          % ITERS)
    print("  mark, over the SIX spine constants AND the stroke width jointly.")
    starts = [x0] + [LO + rng.random(7) * (HI - LO) for _ in range(ITERS - 1)]
    for i, s in enumerate(starts):
        r = minimize(neg, s, method="Nelder-Mead",
                     options=dict(maxiter=300, xatol=2e-3, fatol=2e-4))
        if -r.fun > best:
            best, best_x = -r.fun, np.clip(r.x, LO, HI)
            print("        restart %-3d  IoU %.4f" % (i, best))
    BEST_P, BEST_W = unpack(best_x)
    _onbound = [k for k, v, lo, hi in zip(list(KEYS) + ["WFRAC"], best_x, LO, HI)
                if abs(v - lo) < 1e-6 or abs(v - hi) < 1e-6]
    ctl("C27", best > _ship + 0.005,
        "the joint spine+weight search improves on the shipped constants "
        "against the canonical mark: IoU %.4f -> %.4f (%+.1f %%)"
        % (_ship, best, 100 * (best / max(_ship, 1e-9) - 1)))
    ctl("C27b", not _onbound,
        "NO PARAMETER IS ON A BOUND -- shipping a bound is shipping the bound, "
        "not the fit.  %s" % ("clear" if not _onbound else "ON BOUND: %s"
                              % _onbound))

    # ------------------------------------------------------ C28, THE VERIFY
    print("")
    print("  C28 -- AND NOW THE VERIFICATION HALF: read the canonical fit on")
    print("         THE PHOTOGRAPH'S OWN STATISTICS.  This is where an imported")
    print("         2019 feature (the V/W gap) would show as a cell collapse.")
    print("")
    print("        %-26s %-8s %-8s %-10s" % ("", "cells", "elong", "landmark res"))

    def read(name, params, wfrac):
        m = built(params, wfrac, rows=276)
        c, _ = cream_cells(m)
        e = cell_elongation(m, 1.0)
        try:
            os.environ["T1_VW_WFRAC"] = "%.5f" % wfrac
            L = _vw.built_landmarks(rows=276, **params)
            res = _vw.err(L)[0] if L else float("nan")
        finally:
            os.environ.pop("T1_VW_WFRAC", None)
        print("        %-26s %-8d %-8.3f %-10.4f" % (name, c, e, res))
        return c, e, res

    # REV 62's OWN FIT, RE-READ ON THIS RULER (rule 38).  EMBLEM_HANDOFF.md
    # sec.4 reports it as elongation 2.56 / 7 cells, but that figure came off
    # rev 62's path.  Quoting it beside rev 63's would be comparing two rulers,
    # which is the defect F136 cost this project a revision on.  So rev 62's
    # SIX CONSTANTS are re-run through the SAME read() below and whatever they
    # print here is what is quoted -- transcribed from EMBLEM_HANDOFF.md sec.4,
    # which is the only carrier holding them.
    REV62 = dict(VW_V_TIP_X=0.2707, VW_APEX_Z=-0.3788, VW_W_ARM_X=0.7794,
                 VW_W_ARM_Z=0.3842, VW_W_TROUGH_X=0.8408, VW_W_TROUGH_Z=-0.7357)
    _sc, _se, _sr = read("shipped", SHIPPED, SHIP_W)
    _rc, _re, _rr = read("rev 62 photo-fit", REV62, SHIP_W)
    _bc, _be, _br = read("canonical fit (rev 63)", BEST_P, BEST_W)
    print("        %-26s %-8d %-8.3f %-10s" % ("THE PHOTOGRAPH", 7, 3.390, "--"))
    print("        %-26s %-8d %-8.3f %-10s"
          % ("the canonical mark", _sweep[0][1], _sweep[0][2], "--"))
    print("")
    print("        stroke width  shipped %.4f  ->  fitted %.4f" % (SHIP_W, BEST_W))
    for k in KEYS:
        print("        %-16s %8.4f  ->  %8.4f" % (k, SHIPPED[k], BEST_P[k]))

    paint(built(BEST_P, BEST_W, rows=276), "rev63_canonfit_cells.png",
          "THE CANONICAL FIT's cream cells")
    ctl("C28", _be > _se,
        "the canonical fit's cells are %s elongated than the shipped glyph's "
        "(%.3f vs %.3f) against the photograph's 3.390"
        % ("MORE" if _be > _se else "LESS", _be, _se))
    ctl("C30", True,
        "REV 62's PHOTO-FIT AND REV 63's CANONICAL FIT, ON ONE RULER: "
        "elongation %.3f vs %.3f, cells %d vs %d, against the photograph's "
        "3.390 and 7.  %s -- and the two were fitted to DIFFERENT OBJECTS "
        "(rev 62 to ref_workshop.jpg's badge, rev 63 to the 2019 vector)"
        % (_re, _be, _rc, _bc,
           "rev 62's is closer to the photograph" if _re > _be
           else "rev 63's is closer to the photograph"))
    ctl("C29", _bc >= _sc,
        "and it does not LOSE cells to an imported V/W gap: %d -> %d against "
        "the photograph's 7" % (_sc, _bc))

    print("")
    print("  %d checked, %d FAILED" % (_n_ok + _n_fail, _n_fail))
    raise SystemExit(1 if _n_fail else 0)
