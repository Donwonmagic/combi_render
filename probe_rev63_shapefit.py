"""rev 63 -- THE FIT EMBLEM_HANDOFF.md sec.5 ITEM 4 ASKS FOR, AND NOBODY BUILT.

sec.5 item 4: *"THE OBJECTIVE IS NOT FULLY DISCRIMINATING, AND THIS IS A REAL
OPENING.  Parameter sets that look quite different score within 0.0007 of each
other.  A better objective -- a distance transform, a chamfer, a shape context,
or IoU JOINTLY WITH THE ELONGATION AND CELL-COUNT STATISTICS -- would likely
find a better optimum than IoU on its own."*  This is that objective.

AND IT EXISTS BECAUSE THE ABLATION SAID IT WOULD WORK.  probe_rev63_ablate.py
answered sec.2.3 candidate 1: `vw_bars` reaches elongation 6.877 at 7 cells,
**twice** the photograph's 3.390.  So the construction is NOT the ceiling and
the topology is not the defect -- but MAXIMISING elongation produces a
degenerate crown of parallel slivers (painted, looked at, and it is not a VW).
Range is not fidelity.  The target is 3.390, not "as high as possible".

THE OBJECTIVE, therefore, is three things at once and none of them alone:
    maximise   IoU against the de-foreshortened workshop badge  (SHAPE)
    hit        elongation 3.390, not exceed it                  (C8's defect)
    require    7 cream cells                                    (C6's topology)

THE PHOTOGRAPH SIDE IS LIFTED FROM probe_rev62_emblem.py BY SOURCE SLICE, not
re-implemented -- a second copy of a target is how one of them gets quietly
relaxed, and F09's conic squash lives in that block.

CONTROLS
  S1  the lifted target is CIRCULAR to within 5 % -- rev 62's own C2e, re-run.
  S2  KILL: the objective separates the shipped glyph from a plain cross.
  S3  no parameter on a bound.
  S4  the winner is PAINTED, and read at 276 rows on the SHIPPED statistics.
"""
import os
import re
import sys
import time

import numpy as np
import scipy.ndimage as ndi
from PIL import Image
from scipy.optimize import minimize

sys.argv = [sys.argv[0]]
import probe_rev46_vw as _vw                                    # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.join(HERE, "probe_scratch")
N = 160
PHOTO_E, PHOTO_N = 3.390, 7

KEYS = ("VW_V_TIP_X", "VW_APEX_Z", "VW_W_ARM_X", "VW_W_ARM_Z",
        "VW_W_TROUGH_X", "VW_W_TROUGH_Z", "VW_W_PEAK_Z")
SHIPPED = {k: float(getattr(_vw.C, k)) for k in KEYS}
SHIP_W = float(_vw.D.CAP_EMBLEM_WFRAC)

_ctl_fail = []


def ctl(name, ok, msg):
    if not ok:
        _ctl_fail.append(name)
    print("    %-4s %s  %s" % (name, "ok  " if ok else "FAIL", msg))


def norm(mask, n=N):
    ys, xs = np.nonzero(mask)
    c = mask[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return np.array(Image.fromarray((c * 255).astype(np.uint8))
                    .resize((n, n), Image.LANCZOS)) > 127


# ---------------------------------------------------------------- THE TARGET
# LIFTED BY SOURCE SLICE from probe_rev62_emblem.py, between its own two
# markers, so F09's conic squash and the badge window cannot drift from rev 62's.
_src = open(os.path.join(HERE, "probe_rev62_emblem.py")).read()
_a = _src.index("# -------------------------------------------------------- the photograph, C2e")
_b = _src.index("def iou(")
_block = _src[_a:_b]
assert "SQUASH" in _block and "TARGET = norm(" in _block, \
    "probe_rev62_emblem.py's target block has moved -- REFUSING to guess"
_ns = dict(np=np, ndi=ndi, Image=Image, os=os, HERE=HERE, norm=norm, ctl=ctl)
print("")
print("  S1 -- THE PHOTOGRAPH SIDE, LIFTED (%d lines of probe_rev62_emblem.py)"
      % _block.count("\n"))
exec(compile(_block, "probe_rev62_emblem.py", "exec"), _ns)
TARGET = _ns["TARGET"]
SQUASH = _ns["SQUASH"]

_gy, _gx = np.mgrid[0:N, 0:N]
_gc = (N - 1) / 2.0
_r2 = ((_gy - _gc) / (N / 2.0)) ** 2 + ((_gx - _gc) / (N / 2.0)) ** 2
INTERIOR = _r2 <= 0.814 ** 2


def iou(a, b):
    u = (a | b).sum()
    return float((a & b).sum()) / u if u else 0.0


_fail = 0


def evaluate(x, rows=N):
    """One build -> (IoU, cells, elongation).  All three off the SAME mask."""
    global _fail
    p = {k: float(v) for k, v in zip(KEYS, x[:7])}
    os.environ["T1_VW_WFRAC"] = "%.5f" % x[7]
    try:
        m = _vw.glyph_only_mask(rows=rows, **p)
        n, _ = _vw.cream_cells(m)
        e = _vw.cell_elongation(m, 1.0)
        return iou(norm(m) & INTERIOR, TARGET & INTERIOR), n, e
    except Exception:
        _fail += 1
        return None, None, None
    finally:
        os.environ.pop("T1_VW_WFRAC", None)


def loss(x):
    u, n, e = evaluate(x)
    if u is None:
        return 5.0
    return (-u
            + 2.0 * abs(e - PHOTO_E) / PHOTO_E        # HIT 3.390, not exceed it
            + 0.5 * abs(n - PHOTO_N))                 # and cut 7 cells


x_ship = np.array([SHIPPED[k] for k in KEYS] + [SHIP_W])
_u0, _n0, _e0 = evaluate(x_ship)

# ------------------------------------------------------------------------- S2
_cross = (_r2 <= 0.97 ** 2) & (
    (np.abs(np.abs(_gy - _gc) - np.abs(_gx - _gc)) < 0.11 * N) | (_r2 > 0.814 ** 2))
_ucross = iou(_cross & INTERIOR, TARGET & INTERIOR)
print("")
ctl("S2", _u0 > _ucross,
    "KILL: the shipped glyph scores IoU %.4f against the badge and a plain "
    "cross %.4f -- the shape term can see the defect" % (_u0, _ucross))
print("        shipped: IoU %.4f  cells %d  elongation %.3f  loss %.4f"
      % (_u0, _n0, _e0, loss(x_ship)))

LO = np.array([0.10, -0.80, 0.20, -0.90, 0.10, -1.80, -0.80, 0.04])
HI = np.array([0.90, 0.70, 2.00, 1.60, 1.20, 0.10, 0.50, 0.40])

NS = int(os.environ.get("T1_FIT_N", "9000"))
rng = np.random.default_rng(6304)
print("")
print("  SCREENING %d random points on the JOINT objective" % NS)
X = LO + rng.random((NS, 8)) * (HI - LO)
X[0] = x_ship
t0 = time.time()
scored = []
for i in range(NS):
    scored.append((loss(X[i]), i))
scored.sort()
print("        %d points in %.0f s; best screen loss %.4f (shipped %.4f); "
      "construction refused %d (%.1f %%)"
      % (NS, time.time() - t0, scored[0][0], loss(x_ship), _fail,
         100.0 * _fail / NS))

print("")
print("  REFINING the 6 best seeds")
best = (loss(x_ship), x_ship.copy())
for rank in range(6):
    seed = X[scored[rank][1]]
    r = minimize(lambda z: loss(np.clip(z, LO, HI)), seed, method="Nelder-Mead",
                 options=dict(maxiter=1500, xatol=1e-3, fatol=1e-5))
    z = np.clip(r.x, LO, HI)
    if r.fun < best[0]:
        best = (float(r.fun), z.copy())
        u, n, e = evaluate(z)
        print("        seed %d  loss %.4f   IoU %.4f  cells %d  elongation %.3f"
              % (rank, r.fun, u, n, e))
BEST = best[1]

_onb = [k for k, v, lo, hi in zip(list(KEYS) + ["WFRAC"], BEST, LO, HI)
        if abs(v - lo) < 1e-6 or abs(v - hi) < 1e-6]
ctl("S3", not _onb, "no parameter on a bound  %s"
    % ("clear" if not _onb else "ON BOUND: %s" % _onb))

# ------------------------------------------------------------------------- S4
print("")
print("  S4 -- READ AT 276 ROWS ON THE SHIPPED STATISTICS")
print("        %-28s %-7s %-8s %-11s %s"
      % ("", "IoU", "cells", "elongation", "landmark res"))


def read(name, x):
    u, n, e = evaluate(x, rows=276)
    os.environ["T1_VW_WFRAC"] = "%.5f" % x[7]
    try:
        L = _vw.built_landmarks(rows=276,
                                **{k: float(v) for k, v in zip(KEYS, x[:7])})
        res = _vw.err(L)[0] if L else float("nan")
    finally:
        os.environ.pop("T1_VW_WFRAC", None)
    print("        %-28s %-7.4f %-8d %-11.3f %.4f" % (name, u, n, e, res))
    return u, n, e, res


read("shipped", x_ship)
_u, _n, _e, _res = read("rev 63 JOINT fit", BEST)
print("        %-28s %-7s %-8d %-11.3f %s" % ("THE PHOTOGRAPH", "--", PHOTO_N,
                                              PHOTO_E, "--"))

os.environ["T1_VW_WFRAC"] = "%.5f" % BEST[7]
try:
    m = _vw.glyph_only_mask(rows=276, **{k: float(v)
                                         for k, v in zip(KEYS, BEST[:7])})
finally:
    os.environ.pop("T1_VW_WFRAC", None)
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
Image.fromarray(rgb).save(os.path.join(SCRATCH, "rev63_shapefit_cells.png"))
Image.fromarray((np.where(m, 235, 40)).astype(np.uint8)).save(
    os.path.join(SCRATCH, "rev63_shapefit_glyph.png"))
print("        painted rev63_shapefit_cells.png and rev63_shapefit_glyph.png")

print("")
print("  THE FITTED CONSTANTS")
for k_, v in zip(list(KEYS) + ["CAP_EMBLEM_WFRAC"], BEST):
    print("        %-18s %8.4f  ->  %9.6f" % (k_, SHIPPED.get(k_, SHIP_W), v))
np.save(os.path.join(SCRATCH, "rev63_shapefit_best.npy"), BEST)
print("")
print("  %s" % ("ALL CONTROLS PASS" if not _ctl_fail
                else "FAILED: %s" % _ctl_fail))
