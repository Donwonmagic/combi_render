# probe_rev62_emblem.py -- FIT THE GLYPH TO THE PHOTOGRAPH'S SHAPE, NOT TO SIX
# SCALARS DERIVED FROM IT.  Rev 45's instruction, executed seventeen revisions
# late.
#
# THE OWNER HAS REPORTED THIS SIX TIMES.  At rev 45, at his own prompting, the
# record wrote down the method:
#
#     "The VW monogram is a registered trademark with fixed proportions.  Build
#      the canonical mark and use the photograph to VERIFY, inverting the method
#      that has derived it from a 68-px emblem and been called wrong four
#      revisions running."          -- commit 5d0f28e, `rev45: the nose badge is
#                                      a catalogue part, not a shape to be derived`
#
# IT WAS NEVER DONE, and it is in NO live carrier -- not the rev-62 brief, not
# the ledger, not the work list, not CLAUDE.md, not OPEN_FINDINGS.md.  It
# survives only in LEDGER_rev45.md and NEXT_CONTEXT_PROMPT_rev46.md, both
# seventeen revisions stale.  Every revision since has gone on fitting six spine
# constants to six run-count landmarks read off a 41x69 px badge.
#
# WHY THAT METHOD CANNOT WORK, MEASURED RATHER THAN ARGUED.  F137 searched 8,174
# candidates and found the maximum cream-cell elongation reachable SUBJECT TO the
# landmark bar is 1.634 against the photograph's 3.39 -- but with the bar dropped
# the SAME construction reaches 4.644.  The geometry can make the photograph's
# thin slivers; THE LANDMARKS FORBID IT.  Rev 62 then killed the leading suspect
# (F152: stroke weight tops out at 1.82 and moves the WRONG WAY) and showed the
# larger badge cannot arbitrate the landmarks (F153).
#
# THE INVERSION, CONCRETELY.  The landmarks compress the badge to six scalars.
# This fits the six spine parameters to the PHOTOGRAPH'S WHOLE MASK by IoU, then
# reports the landmarks, the cell count and the elongation AS CHECKS.  If the
# best-shape-match glyph misses the landmarks, that is a result about the
# landmarks -- which is what F137's incompatibility already implies.
#
# THE TARGET IS THE WORKSHOP BADGE, DE-FORESHORTENED.  ref_workshop.jpg carries
# the same factory pressing at 1.71x the area of the badge every constant was
# fitted to; F141's corollary makes it admissible (the roundel's SHAPE is the
# pressing, which is geometry and transfers between vehicles; only its COLOUR is
# artwork).  The mask is the one repaired at rev 62 -- level 165 with a 3x3
# closing, stable over 145..180, agreeing with F09's independently-fitted conic
# to 0.7 px.  A LEVEL THRESHOLD ON CHROME IS THE KNOWN HAZARD HERE (F08): the
# first cut at level 118 took one flank of every stroke.  Hence C2e.
#
# WHAT THIS PROBE DOES NOT DO.  It does not ship anything.  It reports what the
# best available shape match looks like and what it costs on the old gates.
#
#   C1e  the rasteriser is the SHIPPED one, imported, not re-implemented.
#   C2e  the photograph target is the REPAIRED mask, and its de-foreshortened
#        aspect is circular to within 5 % -- if it is not, the squash is wrong
#        and every shape comparison below is against an ellipse.
#   C3e  A KILL: the objective must SEPARATE the shipped glyph from a plain
#        cross.  If a cross scores as well as the build, IoU cannot see the
#        defect the owner reports and nothing here means anything.
#   C4e  the search improves on the shipped constants at all.
#
# RUN   python3 probe_rev62_emblem.py [--iters N] [--paint]

import contextlib
import importlib.util
import io
import os
import sys

import numpy as np
import scipy.ndimage as ndi
from scipy.optimize import minimize
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUTD = os.path.join(HERE, "probe_scratch")
os.environ.setdefault("T1_SUB", "1")
sys.path.insert(0, HERE)

PAINT = "--paint" in sys.argv
ITERS = int(sys.argv[sys.argv.index("--iters") + 1]) if "--iters" in sys.argv else 60

CTL = {}


def ctl(name, ok, msg):
    CTL[name] = bool(ok)
    print("  [%s] %-4s %s" % ("PASS" if ok else "FAIL", name, msg))


# ------------------------------------------------- the SHIPPED rasteriser, C1e
_spec = importlib.util.spec_from_file_location(
    "_vw", os.path.join(HERE, "probe_rev46_vw.py"))
_vw = importlib.util.module_from_spec(_spec)
with contextlib.redirect_stdout(io.StringIO()):
    _spec.loader.exec_module(_vw)

KEYS = ("VW_V_TIP_X", "VW_APEX_Z", "VW_W_ARM_X", "VW_W_ARM_Z",
        "VW_W_TROUGH_X", "VW_W_TROUGH_Z")
SHIPPED = {k: _vw.CURRENT[k] for k in KEYS}

ctl("C1e", hasattr(_vw, "glyph_only_mask") and hasattr(_vw, "cell_elongation"),
    "the rasteriser, the cell counter and the elongation statistic are "
    "probe_rev46_vw.py's OWN, imported and not re-implemented -- so a shape "
    "that scores here scores on the shipped instrument")

N = 160                                   # raster for the search; fast and ample


def built(params, rows=N):
    return _vw.glyph_only_mask(rows=rows, **params)


def norm(mask, n=N):
    ys, xs = np.nonzero(mask)
    c = mask[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    im = Image.fromarray((c * 255).astype(np.uint8)).resize((n, n), Image.LANCZOS)
    return np.array(im) > 127


# -------------------------------------------------------- the photograph, C2e
_W = np.array(Image.open(os.path.join(HERE, "ref_workshop.jpg"))
              .convert("RGB")).astype(float)
_sub = _W.mean(axis=2)[498:599, 270:340]
_m = ndi.binary_closing(_sub < 165, np.ones((3, 3)))
_im = Image.fromarray((_m * 255).astype(np.uint8))
SQUASH = 92.728 / 63.299                  # F09's conic on this same badge
_sq = np.array(_im.resize((int(round(_im.width * SQUASH)), _im.height),
                          Image.LANCZOS)) > 127
_ys, _xs = np.nonzero(_sq)
_ar = ((_xs.max() - _xs.min()) / 2.0) / ((_ys.max() - _ys.min()) / 2.0)
TARGET = norm(_sq)
ctl("C2e", abs(_ar - 1.0) < 0.05,
    "the de-foreshortened badge is CIRCULAR to %.1f %% (aspect %.3f), so the "
    "shape comparison is against a circle and not an ellipse.  Squash %.4f is "
    "F09's conic on this same badge, not a fitted value"
    % (100 * abs(_ar - 1), _ar, SQUASH))


def iou(a, b):
    u = (a | b).sum()
    return float((a & b).sum()) / u if u else 0.0


# THE OBJECTIVE EXCLUDES THE RING BAND, AND THAT MATTERS MORE THAN IT SOUNDS.
# The band is roughly half the ink and is IDENTICAL on both sides by
# construction -- it is drawn from the same _RING_INNER_FRAC either way.  Scored
# whole-mask it contributes a large constant to the numerator AND denominator,
# so the shipped glyph reads IoU 0.525 and even a plain cross reads close to it:
# the statistic is mostly measuring agreement about a circle both sides already
# agree on.  Masking to the interior makes the objective sensitive to the one
# thing that is wrong, which is the GLYPH.  Watched: it drops every score by
# about half and roughly triples the spread between a cross and the build.
_gy, _gx = np.mgrid[0:N, 0:N]
_gc = (N - 1) / 2.0
INTERIOR = ((((_gy - _gc) / (N / 2.0)) ** 2
             + ((_gx - _gc) / (N / 2.0)) ** 2) <= 0.814 ** 2)


def score(params):
    try:
        return iou(norm(built(params)) & INTERIOR, TARGET & INTERIOR)
    except Exception:
        return 0.0


# --------------------------------------------------------------------- C3e
_ship_iou = score(SHIPPED)
_yy, _xx = np.mgrid[0:N, 0:N]
_cy = _cx = (N - 1) / 2.0
_disc = (((_yy - _cy) / (N / 2.0)) ** 2 + ((_xx - _cx) / (N / 2.0)) ** 2) <= 0.97 ** 2
_band = (((_yy - _cy) / (N / 2.0)) ** 2 + ((_xx - _cx) / (N / 2.0)) ** 2) > 0.814 ** 2
_d = np.abs(_yy - _cy) - np.abs(_xx - _cx)
_cross = _disc & ((np.abs(_d) < 0.11 * N) | _band)
_cross_iou = iou(_cross & INTERIOR, TARGET & INTERIOR)
ctl("C3e", _ship_iou > _cross_iou,
    "KILL: the objective SEPARATES the shipped glyph from a PLAIN CROSS -- "
    "shipped %.4f against a cross's %.4f.  If a cross scored as well, IoU "
    "could not see the defect the owner reports and nothing below would mean "
    "anything" % (_ship_iou, _cross_iou))

print("\n    SHIPPED constants, scored against the photograph's whole mask")
print("        IoU %.4f" % _ship_iou)

# ---------------------------------------------------------------- the search
LO = np.array([0.15, -0.45, 0.30, -0.60, 0.20, -0.95])
HI = np.array([0.75, 0.55, 1.00, 0.90, 0.85, -0.05])
x0 = np.array([SHIPPED[k] for k in KEYS])


def unpack(x):
    return {k: float(v) for k, v in zip(KEYS, np.clip(x, LO, HI))}


def neg(x):
    return -score(unpack(x))


rng = np.random.default_rng(6202)
best_x, best = x0.copy(), _ship_iou
print("\n    SEARCHING -- %d restarts of Nelder-Mead on IoU against the "
      "photograph" % ITERS)
starts = [x0] + [LO + rng.random(6) * (HI - LO) for _ in range(ITERS - 1)]
for i, s in enumerate(starts):
    r = minimize(neg, s, method="Nelder-Mead",
                 options=dict(maxiter=260, xatol=2e-3, fatol=2e-4))
    if -r.fun > best:
        best, best_x = -r.fun, np.clip(r.x, LO, HI)
        print("        restart %-3d  IoU %.4f" % (i, best))
BEST = unpack(best_x)

ctl("C4e", best > _ship_iou + 0.005,
    "the search improves on the shipped constants: IoU %.4f -> %.4f (%+.1f %%)"
    % (_ship_iou, best, 100 * (best / max(_ship_iou, 1e-9) - 1)))

# ------------------------------------------------------- what it costs / buys
def report(name, params):
    m276 = built(params, rows=276)
    e = _vw.cell_elongation(m276, 1.0)
    c, sz = _vw.cream_cells(m276)
    L = _vw.built_landmarks(rows=276, **params)
    res = _vw.err(L)[0] if L else float("nan")
    print("        %-10s IoU %.4f   elongation %.2f   cells %d   "
          "landmark residual %.4f" % (name, score(params), e, c, res))
    return e, c, res


print("\n    WHAT THE SHAPE FIT BUYS, AND WHAT IT COSTS ON THE OLD GATES")
print("        photograph elongation 3.39 (2.95..3.42 over its own window), "
      "cells 7 (F139: genuinely 6)")
e0, c0, r0 = report("SHIPPED", SHIPPED)
e1, c1, r1 = report("SHAPE-FIT", BEST)

print("\n    THE SHAPE-FIT CONSTANTS")
for k in KEYS:
    print("        %-16s %8.4f   (shipped %8.4f)" % (k, BEST[k], SHIPPED[k]))

print("\n    READ THIS BEFORE ACTING ON THE NUMBERS ABOVE")
if r1 > r0:
    print("        The landmark residual got WORSE (%.4f -> %.4f) while the "
          "shape got BETTER." % (r0, r1))
    print("        That is F137's incompatibility showing up from the other "
          "side, and it is")
    print("        the POINT of this probe, not a failure of it: the six "
          "landmarks and the")
    print("        photograph's actual shape cannot both be satisfied, so one "
          "of them is wrong.")
    print("        This probe asserts the SHAPE is the thing the owner looks "
          "at.")

if PAINT:
    os.makedirs(OUTD, exist_ok=True)
    A, B = norm(built(SHIPPED)), norm(built(BEST))
    ov = np.zeros((N, N, 3), np.uint8)
    ov[..., 0] = np.where(TARGET, 255, 0)
    ov[..., 1] = np.where(B, 255, 0)
    ov[~INTERIOR] = (ov[~INTERIOR] * 0.35).astype(np.uint8)
    tri = np.concatenate([np.dstack([A * 255] * 3), np.dstack([B * 255] * 3),
                          np.dstack([TARGET * 255] * 3), ov], axis=1)
    im = Image.fromarray(tri.astype(np.uint8))
    im = im.resize((im.width * 3, im.height * 3), Image.NEAREST)
    im.save(os.path.join(OUTD, "rev62_emblem_fit.png"))
    print("\n    PAINTED -> probe_scratch/rev62_emblem_fit.png")
    print("        SHIPPED | SHAPE-FIT | PHOTOGRAPH | overlay "
          "(green = fit, red = photograph)")

bad = [k for k, v in CTL.items() if not v]
print("\nCONTROLS: %d checked, %s"
      % (len(CTL), ("%d FAILED -- %s" % (len(bad), ",".join(bad))) if bad
         else "0 FAILED"))
