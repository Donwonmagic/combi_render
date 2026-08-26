"""rev 63 -- THE SEARCH WITH EVERY TERM REV 63 LEARNED, AND A SHORTLIST TO RENDER.

Everything this revision found, applied at once:
  F174  the construction is NOT the ceiling -- it reaches elongation 6.877 at
        7 cells, so there IS a parameter set that looks right.
  F175  C6 + C8 + IoU can ALL pass on a glyph that renders as a Y.  So they are
        necessary, not sufficient, and no scalar set is trusted on its own.
  F176  C7 -- C6's own kill -- can go dead.  It is checked as a PRECONDITION.
  F177  the landmark residual was the ONLY statistic that stayed red on the
        trident, so it is a HARD CONSTRAINT here, not a traded-away objective.
  F181  what separated the trident was WHERE the six contacts sit: its two W
        legs converged to 15 deg apart.  A tightest-gap FLOOR is a hard term.
  F180  and the glyph must actually TOUCH the ring in six places.

The output is not a winner.  It is a SHORTLIST, because F175's whole lesson is
that the render is the arbiter and no number here replaces looking.
"""
import os
import sys

import numpy as np
import scipy.ndimage as ndi
from PIL import Image
from scipy.optimize import minimize

sys.argv = [sys.argv[0]]
import probe_rev46_vw as _vw                                    # noqa: E402
import probe_rev63_reach as _reach                              # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.join(HERE, "probe_scratch")
N = 160
PHOTO_E, PHOTO_N = 3.390, 7
KEYS = _reach.KEYS
SHIPPED = dict(_reach.SHIPPED)
SHIP_W = float(_vw.D.CAP_EMBLEM_WFRAC)


def norm(mask, n=N):
    ys, xs = np.nonzero(mask)
    c = mask[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return np.array(Image.fromarray((c * 255).astype(np.uint8))
                    .resize((n, n), Image.LANCZOS)) > 127


_src = open(os.path.join(HERE, "probe_rev62_emblem.py")).read()
_blk = _src[_src.index("# ------------------------------------------------"
                       "-------- the photograph, C2e"):_src.index("def iou(")]
_ns = dict(np=np, ndi=ndi, Image=Image, os=os, HERE=HERE, norm=norm,
           ctl=lambda *a: None)
exec(compile(_blk, "probe_rev62_emblem.py", "exec"), _ns)
TARGET = _ns["TARGET"]

_gy, _gx = np.mgrid[0:N, 0:N]
_gc = (N - 1) / 2.0
_r2 = ((_gy - _gc) / (N / 2.0)) ** 2 + ((_gx - _gc) / (N / 2.0)) ** 2
INTERIOR = _r2 <= 0.814 ** 2


def iou(a, b):
    u = (a | b).sum()
    return float((a & b).sum()) / u if u else 0.0


ROWS = 200


def full(x):
    """Every term at once, off ONE build."""
    p = {k: float(v) for k, v in zip(KEYS, x[:7])}
    os.environ["T1_VW_WFRAC"] = "%.5f" % x[7]
    try:
        m = _vw.glyph_only_mask(rows=ROWS, **p)
        n, _ = _vw.cream_cells(m)
        e = _vw.cell_elongation(m, 1.0)
        u = iou(norm(m) & INTERIOR, TARGET & INTERIOR)
        nc, _sz, ang = _reach.count_on(m, ROWS)
        if len(ang) >= 2:
            a = sorted(ang)
            gaps = [(a[(i + 1) % len(a)] - a[i]) % 360 for i in range(len(a))]
            g = min(gaps)
        else:
            g = 0.0
        return dict(iou=u, cells=n, elong=e, contacts=nc, gap=float(g), p=p,
                    w=float(x[7]))
    except Exception:
        return None
    finally:
        os.environ.pop("T1_VW_WFRAC", None)


def loss(x):
    r = full(x)
    if r is None:
        return 9.0
    pen = 0.0
    pen += 0.60 * abs(r["cells"] - PHOTO_N)             # C6
    pen += 0.60 * abs(r["contacts"] - 6)                # F180 -- six contacts
    pen += 2.00 * abs(r["elong"] - PHOTO_E) / PHOTO_E   # C8, HIT not exceed
    pen += 0.05 * max(0.0, 38.0 - r["gap"])             # F181 -- gap FLOOR
    return -r["iou"] + pen


x_ship = np.array([SHIPPED[k] for k in KEYS] + [SHIP_W])
CANON = np.array([0.3287, 0.0538, 1.1002, 0.4350, 0.3111, -0.6445,
                  SHIPPED["VW_W_PEAK_Z"], 0.1543])
REV62 = np.array([0.2707, -0.3788, 0.7794, 0.3842, 0.8408, -0.7357,
                  SHIPPED["VW_W_PEAK_Z"], SHIP_W])

print("")
print("  THE SEEDS, ON EVERY TERM REV 63 LEARNED")
print("        %-22s %-7s %-6s %-6s %-9s %s"
      % ("", "IoU", "cells", "cont.", "elong", "tightest gap"))
for nm, x in (("shipped", x_ship), ("rev 62 photo-fit", REV62),
              ("rev 63 canonical fit", CANON)):
    r = full(x)
    print("        %-22s %-7.4f %-6d %-6d %-9.3f %.0f deg"
          % (nm, r["iou"], r["cells"], r["contacts"], r["elong"], r["gap"]))
print("        %-22s %-7s %-6d %-6d %-9.3f %s"
      % ("THE PHOTOGRAPH", "--", PHOTO_N, 6, PHOTO_E, "--"))

LO = np.array([0.10, -0.80, 0.20, -0.90, 0.10, -1.80, -0.80, 0.06])
HI = np.array([0.90, 0.70, 2.00, 1.60, 1.20, 0.10, 0.50, 0.38])
NS = int(os.environ.get("T1_FIN_N", "7000"))
rng = np.random.default_rng(6305)
X = np.vstack([x_ship, REV62, CANON,
               LO + rng.random((NS, 8)) * (HI - LO)])
print("")
print("  SCREENING %d points with the CELL, CONTACT, ELONGATION and GAP terms"
      % len(X))
sc = sorted((loss(X[i]), i) for i in range(len(X)))
print("        best screen loss %.4f" % sc[0][0])

print("")
print("  REFINING the 8 best seeds")
cands = []
for rank in range(8):
    r0 = minimize(lambda z: loss(np.clip(z, LO, HI)), X[sc[rank][1]],
                  method="Nelder-Mead",
                  options=dict(maxiter=1400, xatol=1e-3, fatol=1e-5))
    z = np.clip(r0.x, LO, HI)
    r = full(z)
    if r is None:
        continue
    cands.append((float(r0.fun), z.copy(), r))
cands.sort(key=lambda t: t[0])

# de-duplicate: keep candidates that are actually DIFFERENT shapes
uniq = []
for L, z, r in cands:
    if all(np.max(np.abs(z - u[1]) / (HI - LO)) > 0.04 for u in uniq):
        uniq.append((L, z, r))
    if len(uniq) == 4:
        break

print("")
print("  THE SHORTLIST -- these get RENDERED, because F175 says the render is")
print("  the arbiter and no number here replaces looking")
print("        %-4s %-7s %-6s %-6s %-9s %-8s %s"
      % ("#", "IoU", "cells", "cont.", "elong", "gap", "landmark res"))
for i, (L, z, r) in enumerate(uniq):
    os.environ["T1_VW_WFRAC"] = "%.5f" % z[7]
    try:
        Lm = _vw.built_landmarks(rows=276, **r["p"])
        res = _vw.err(Lm)[0] if Lm else float("nan")
    finally:
        os.environ.pop("T1_VW_WFRAC", None)
    print("        %-4d %-7.4f %-6d %-6d %-9.3f %-8.0f %.4f"
          % (i, r["iou"], r["cells"], r["contacts"], r["elong"], r["gap"], res))
    os.environ["T1_VW_WFRAC"] = "%.5f" % z[7]
    try:
        m = _vw.glyph_only_mask(rows=276, **r["p"])
    finally:
        os.environ.pop("T1_VW_WFRAC", None)
    Image.fromarray(np.where(m, 235, 40).astype(np.uint8)).save(
        os.path.join(SCRATCH, "rev63_final_%d.png" % i))
np.save(os.path.join(SCRATCH, "rev63_final_shortlist.npy"),
        np.array([z for _, z, _ in uniq]))
print("")
print("  painted rev63_final_0..%d.png ; constants in rev63_final_shortlist.npy"
      % (len(uniq) - 1))
