"""rev 63 -- ABLATE THE CONSTRUCTION ITSELF.  Can `vw_bars` make the
photograph's cream slivers AT ANY PARAMETER, or is the topology the ceiling?

WHY THIS IS THE RIGHT QUESTION.  EMBLEM_HANDOFF.md sec.5 / the rev-63 brief
sec.2.3 candidate 1: *"The incompatibility is in the CONSTRUCTION, not the
landmarks. `vw_bars` may not be able to make a sliver at any parameter --
F137 reached 4.644 with the bar dropped, but that was six spine parameters,
not the shipped topology.  ABLATE THE CONSTRUCTION."*  Nobody has.

Every previous search here optimised something ELSE and read the shape off the
answer: F103 solved the cell COUNT, rev 62 solved IoU against a badge, rev 63's
first half solved IoU against a canonical vector.  **This one maximises the
statistic that MEASURES THE DEFECT** -- C8's cell elongation -- directly, over
SEVEN spine constants AND the stroke width jointly, and reports the CEILING.

  a ceiling reached  -> the construction can do it and the constants are the job
  a ceiling short    -> the TOPOLOGY is the defect, and no constant will fix it.
                        That is a real result and it is worth more than a guess.

CONTROLS
  A1  the objective MOVES.  An objective that cannot respond to its parameters
      is a tautology (rule 6), and this one drives a bpy mesh build through an
      env var and six setattrs -- exactly the plumbing that silently no-ops.
      Watched moving BEFORE any search result is believed.
  A2  the failure rate is REPORTED.  A search that silently discards most of
      its box is not an ablation of anything.
  A3  the ceiling is re-read at a second raster.  F152: C8's scale-stability is
      a property of the shipped point, not of the statistic.  Do not assume it.
  A4  the winner is PAINTED and must be looked at (rule 8) before it is quoted.
"""
import os
import sys
import time

import numpy as np
from PIL import Image

sys.argv = [sys.argv[0]]
import probe_rev46_vw as _vw                                   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.join(HERE, "probe_scratch")
PHOTO_E, PHOTO_N = 3.390, 7

KEYS = ("VW_V_TIP_X", "VW_APEX_Z", "VW_W_ARM_X", "VW_W_ARM_Z",
        "VW_W_TROUGH_X", "VW_W_TROUGH_Z", "VW_W_PEAK_Z")
SHIPPED = {k: float(getattr(_vw.C, k)) for k in KEYS}
SHIP_W = float(_vw.D.CAP_EMBLEM_WFRAC)

LO = np.array([0.10, -0.80, 0.20, -0.90, 0.10, -1.80, -0.80, 0.04])
HI = np.array([0.90, 0.70, 2.00, 1.60, 1.20, 0.10, 0.50, 0.40])

_fail = 0


def evaluate(x, rows=138):
    """-> (cells, elongation) or (None, None) if the construction refuses."""
    global _fail
    p = {k: float(v) for k, v in zip(KEYS, x[:7])}
    os.environ["T1_VW_WFRAC"] = "%.5f" % x[7]
    try:
        m = _vw.glyph_only_mask(rows=rows, **p)
        n, _ = _vw.cream_cells(m)
        return n, _vw.cell_elongation(m, 1.0)
    except Exception:
        _fail += 1
        return None, None
    finally:
        os.environ.pop("T1_VW_WFRAC", None)


def ctl(name, ok, msg):
    print("    %-4s %s  %s" % (name, "ok  " if ok else "FAIL", msg))
    return ok


x_ship = np.array([SHIPPED[k] for k in KEYS] + [SHIP_W])

# ------------------------------------------------------------------------- A1
print("")
print("  A1 -- DOES THE OBJECTIVE MOVE?  (rule 6: a statistic that cannot")
print("        respond to its own parameters is a tautology, and this one")
print("        drives a mesh build through an env var and seven setattrs)")
_n0, _e0 = evaluate(x_ship)
print("        shipped                         cells %d  elongation %.3f" % (_n0, _e0))
_moved = []
for i, k in enumerate(list(KEYS) + ["WFRAC"]):
    xx = x_ship.copy()
    xx[i] = LO[i] + 0.72 * (HI[i] - LO[i])
    n, e = evaluate(xx)
    if e is not None:
        _moved.append(abs(e - _e0))
        print("        %-14s -> %7.4f       cells %s  elongation %.3f"
              % (k, xx[i], n, e))
_A1 = ctl("A1", max(_moved) > 0.05,
          "the largest single-parameter move is %.3f in elongation -- the "
          "objective responds, so a search over it means something"
          % max(_moved))
if not _A1:
    print("    REFUSING TO SEARCH: the objective is inert.")
    raise SystemExit(2)

# ------------------------------------------------------------------ the sweep
NS = int(os.environ.get("T1_ABL_N", "24000"))
rng = np.random.default_rng(6303)
print("")
print("  SWEEPING THE CONSTRUCTION -- %d random points over an 8-parameter box" % NS)
print("  (7 spine constants + the stroke width).  Maximising C8's elongation,")
print("  reported BOTH unconstrained and at the photograph's own 7 cells.")
X = LO + rng.random((NS, 8)) * (HI - LO)
X[0] = x_ship
best_any = (-1.0, None, None)
best_7 = (-1.0, None, None)
hist = {}
t0 = time.time()
for i in range(NS):
    n, e = evaluate(X[i])
    if e is None:
        continue
    hist[n] = hist.get(n, 0) + 1
    if e > best_any[0]:
        best_any = (e, X[i].copy(), n)
    if n == PHOTO_N and e > best_7[0]:
        best_7 = (e, X[i].copy(), n)
print("        %d points in %.0f s;  cell-count histogram %s"
      % (NS, time.time() - t0, dict(sorted(hist.items()))))
ctl("A2", _fail < 0.25 * NS,
    "the construction REFUSED %d of %d points (%.1f %%) -- reported, because a "
    "search that silently discards its box is not an ablation"
    % (_fail, NS, 100.0 * _fail / NS))

# ------------------------------------------------------------------ refinement
from scipy.optimize import minimize                            # noqa: E402


def refine(seed, require7):
    def neg(z):
        z = np.clip(z, LO, HI)
        n, e = evaluate(z)
        if e is None:
            return 0.0
        if require7 and n != PHOTO_N:
            return -e * 0.25                # heavily penalised, not excluded
        return -e
    r = minimize(neg, seed, method="Nelder-Mead",
                 options=dict(maxiter=1200, xatol=1e-3, fatol=1e-4))
    z = np.clip(r.x, LO, HI)
    n, e = evaluate(z)
    return e, z, n


print("")
print("  REFINING the two best seeds")
_ea, _xa, _na = refine(best_any[1], False)
if best_7[1] is not None:
    _e7, _x7, _n7 = refine(best_7[1], True)
else:
    _e7, _x7, _n7 = -1.0, None, None
if _na != PHOTO_N and _e7 > 0 and _n7 == PHOTO_N:
    pass

print("")
print("  THE CONSTRUCTION'S CEILING -- what `vw_bars` CAN do, at any parameter")
print("        %-40s %-7s %s" % ("", "cells", "elongation"))
print("        %-40s %-7d %.3f" % ("shipped", _n0, _e0))
print("        %-40s %-7d %.3f" % ("best found, ANY cell count", _na, _ea))
if _x7 is not None:
    print("        %-40s %-7d %.3f" % ("best found AT 7 CELLS", _n7, _e7))
else:
    print("        %-40s %-7s %s" % ("best found AT 7 CELLS", "--", "NONE FOUND"))
print("        %-40s %-7d %.3f" % ("THE PHOTOGRAPH", PHOTO_N, PHOTO_E))

# ------------------------------------------------------------------------- A3
best_e, best_x, best_n = (_e7, _x7, _n7) if (_x7 is not None and _n7 == PHOTO_N) \
    else (_ea, _xa, _na)
print("")
print("  A3 -- THE CEILING AT A SECOND RASTER (F152: do not assume stability)")
for r in (69, 276, 552):
    n, e = evaluate(best_x, rows=r)
    print("        %-4d rows   cells %s   elongation %.3f" % (r, n, e))
_e276 = evaluate(best_x, rows=276)[1]
_e69 = evaluate(best_x, rows=69)[1]
ctl("A3", abs(_e69 - _e276) / _e276 < 0.30,
    "the winner's elongation moves %.3f -> %.3f from 69 to 276 rows (%.1f %%)"
    % (_e69, _e276, 100 * abs(_e69 - _e276) / _e276))

# ------------------------------------------------------------------------- A4
os.environ["T1_VW_WFRAC"] = "%.5f" % best_x[7]
try:
    m = _vw.glyph_only_mask(rows=276, **{k: float(v)
                                         for k, v in zip(KEYS, best_x[:7])})
finally:
    os.environ.pop("T1_VW_WFRAC", None)
import scipy.ndimage as ndi                                    # noqa: E402
n0, n1 = m.shape
yy, xx = np.mgrid[0:n0, 0:n1]
cy, cx = (n0 - 1) / 2.0, (n1 - 1) / 2.0
disc = (((yy - cy) / (n0 / 2.0)) ** 2 + ((xx - cx) / (n1 / 2.0)) ** 2) <= 0.97 ** 2
lab, k = ndi.label(disc & ~m)
rgb = np.zeros((n0, n1, 3), np.uint8)
rgb[m] = (235, 235, 235)
pal = [(215, 40, 40), (40, 170, 60), (50, 90, 230), (230, 170, 30),
       (200, 60, 200), (30, 200, 200), (250, 120, 60), (140, 140, 255)]
for i in range(1, k + 1):
    sel = lab == i
    rgb[sel] = pal[(i - 1) % len(pal)] if sel.sum() >= 0.002 * disc.sum() else (70, 70, 70)
Image.fromarray(rgb).save(os.path.join(SCRATCH, "rev63_ablate_best.png"))
print("")
print("  A4 -- PAINTED probe_scratch/rev63_ablate_best.png  -- LOOK AT IT (rule 8)")

print("")
print("  THE WINNER'S CONSTANTS")
for k_, v in zip(list(KEYS) + ["CAP_EMBLEM_WFRAC"], best_x):
    was = SHIPPED.get(k_, SHIP_W)
    print("        %-18s %8.4f  ->  %8.4f" % (k_, was, v))
_reach = best_e / PHOTO_E
print("")
print("  VERDICT: the construction reaches %.3f of the photograph's %.3f "
      "(%.0f %%)" % (best_e, PHOTO_E, 100 * _reach))
np.save(os.path.join(SCRATCH, "rev63_ablate_best.npy"), best_x)
