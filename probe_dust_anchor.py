"""probe_dust_anchor.py -- READ-ONLY.  SPEC 10.76, rev 27.

Settles SPEC 10.71: `W_DUST_FAC_UP = 0.7313` is solved against `COUNTERCREAM`
on a surface that carries `COUNTERTAN`.

This script BUILDS NOTHING and CHANGES NOTHING.  It needs no Blender -- it is
pure arithmetic on `t1_mats`' own constants plus `ref_rear34.jpg`.  Run it with
Blender's python (it needs pillow + numpy):

    /tmp/blender/4.5/python/bin/python3.11 probe_dust_anchor.py

WHAT IT ASSERTS RATHER THAN CLAIMS IN PROSE
-------------------------------------------
Every load-bearing statement below is an `assert`, per SPEC 10.67's rule that a
claim in prose is not a guard -- including when the prose is inside the guard.

  C1 HARNESS   the recorded chain reproduces `_UP_MEASURED` from the recorded
               patch triples, to < 1e-4.  If this fails, nothing else here
               means anything.
  C2 MISLABEL  `t1_mats.py`'s comment "this file's CREAM (0.9676, 0.7784,
               0.4976)" is NOT `CREAM`.  It is the von-Kries GAIN,
               lin(flank patch) / CREAM.  Asserted both ways.
  C3 TAUTOLOGY the live assert's three-channel agreement is a CONSTRUCTION,
               not a check: `W_DUST_COL_UP` is collinear with COUNTERCREAM and
               `_UP_MEASURED` by design, so the coverage solve must agree in
               all three channels whatever the numbers are.
  C4 GEOMETRY  no axis-aligned rectangle of 2700 px lies entirely on the
               counter top in `ref_rear34.jpg`.  Hence the patch straddled,
               whichever box rev 12 used.
  C5 UNREACHED on a clean band-following sample, with the class gate and the
               edge erosion SWEPT rather than picked, `_UP_MEASURED`'s surface
               is not reachable from `COUNTERTAN` by ANY coverage f in [0, 1] --
               every arm returns f < 0 in all three channels.

WHAT IT DOES **NOT** CLAIM -- printed at the end so it cannot be misread
-----------------------------------------------------------------------
  * WHICH box rev 12 used.  Several distinct boxes reproduce the recorded
    median exactly.  The geometric result C4 is box-INDEPENDENT and is the
    only thing claimed.
  * That `COUNTERTAN` is wrong, or that `CREAM` is wrong.  The de-illuminated
    top is PROPORTIONAL to `CREAM` channel-wise, and `CREAM` is this project's
    largest open constant (rev 20/21, five routes refuted).  This frame cannot
    separate the two.
  * That the top and the flank share a light.  They are up-facing vs vertical
    -- exactly the orientation mismatch SPEC 10.60 ruled INADMISSIBLE when it
    struck `COUNTERTAN`'s cab-roof arm at 22 % bluer.  UNTESTED here.
  * Any repair.  SPEC 10.71 says do not repair it blind; this probe does not.
"""

import ast
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
FRAME = os.path.join(HERE, "ref_rear34.jpg")
SRC = os.path.join(HERE, "t1_mats.py")


class _Consts(object):
    """Constants PARSED out of `t1_mats.py`, never re-typed here.

    `t1_mats` imports `bpy`, so it cannot be imported outside Blender -- and
    re-typing its constants into this file is the exact defect SPEC 10.63 and
    10.68 were about.  So they are parsed, and **every parse RAISES** if the
    name is missing or is no longer a literal.  An `os.environ.get(name, d)`
    wrapper resolves to its DEFAULT `d`, so this probe always describes the
    shipped build and never the caller's environment.
    """

    def __init__(self, path, names):
        tree = ast.parse(open(path).read())
        found = {}
        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id in names and t.id not in found:
                    found[t.id] = self._value(t.id, node.value)
        missing = [n for n in names if n not in found]
        if missing:
            raise RuntimeError("t1_mats.py no longer defines %r at module level "
                               "-- this probe must be re-grounded, not patched"
                               % (missing,))
        self.__dict__.update(found)

    @staticmethod
    def _value(name, node):
        try:
            return ast.literal_eval(node)
        except (ValueError, TypeError, SyntaxError):
            pass
        # float(os.environ.get("T1_X", <default>))  ->  <default>
        n = node
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "float":
            n = n.args[0]
        if isinstance(n, ast.Call) and getattr(n.func, "attr", None) == "get" \
                and len(n.args) == 2:
            return float(ast.literal_eval(n.args[1]))
        raise RuntimeError("t1_mats.%s is no longer a parseable literal or an "
                           "os.environ.get default -- re-ground this probe"
                           % name)


M = _Consts(SRC, ["CREAM", "COUNTERCREAM", "COUNTERTAN", "W_DUST_COL_UP",
                  "_UP_MEASURED", "W_DUST_UP_W", "W_DUST_MOT_MEAN",
                  "W_DUST_FAC_UP"])

# The two patches as t1_mats.py records them -- mean sRGB and post-trim count.
# NEITHER has coordinates anywhere in the repo; see the recovery below.
REC_TOP = (202.0, 172.0, 127.0)      # "counter top (upward, cream paint)" n=2160
REC_FLK = (203.0, 186.0, 146.0)      # "cream flank rear quarter (side)"   n=2153
REC_N_TOP, REC_N_FLK = 2160, 2153
COMMENT_TRIPLE = (0.9676, 0.7784, 0.4976)   # what the comment calls "CREAM"


def lin(v):
    v = v / 255.0
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4


def lin_arr(x):
    v = np.asarray(x, dtype=np.float64) / 255.0
    return np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)


def lstar_arr(rgb255):
    l = lin_arr(rgb255)
    y = 0.2126 * l[..., 0] + 0.7152 * l[..., 1] + 0.0722 * l[..., 2]
    return np.where(y > (6 / 29.) ** 3,
                    116.0 * np.cbrt(np.maximum(y, 1e-12)) - 16.0,
                    116.0 * (y / (3 * (6 / 29.) ** 2) + 4 / 29.) - 16.0)


def trimmed_median(px):
    """Median over the middle 80 % of L* -- the convention the comment names.

    Recovered, not assumed: it is what takes 2691 px to exactly 2153 and
    2700 px to exactly 2160, the two counts the comment records.
    """
    px = np.asarray(px, dtype=np.float64).reshape(-1, 3)
    L = lstar_arr(px)
    lo, hi = np.percentile(L, [10, 90])
    k = (L >= lo) & (L <= hi)
    return np.median(px[k], axis=0), int(k.sum())


def coverage(base, dust, target):
    """f solving base + f*(dust - base) = target, per channel."""
    return [(m - b) / (d - b) for b, d, m in zip(base, dust, target)]


def main():
    ok = True

    def check(tag, cond, detail=""):
        nonlocal ok
        ok = ok and bool(cond)
        print("  [%s] %-52s %s" % ("PASS" if cond else "FAIL", tag, detail))

    print(__doc__.split("WHAT IT ASSERTS")[0].strip().splitlines()[0])
    print("\n=== constants read live out of t1_mats ===")
    print("  CREAM         %s" % (M.CREAM,))
    print("  COUNTERCREAM  %s" % (M.COUNTERCREAM,))
    print("  COUNTERTAN    %s" % (M.COUNTERTAN,))
    print("  W_DUST_COL_UP %s" % (M.W_DUST_COL_UP,))
    print("  _UP_MEASURED  %s" % (M._UP_MEASURED,))
    print("  W_DUST_FAC_UP %.4f" % M.W_DUST_FAC_UP)

    # ---------------------------------------------------------------- C1/C2
    print("\n=== C1 harness, C2 mislabel ===")
    E = tuple(lin(c) / k for c, k in zip(REC_FLK, M.CREAM))
    check("C2  comment triple == von-Kries gain lin(flank)/CREAM",
          max(abs(a - b) for a, b in zip(E, COMMENT_TRIPLE)) < 1e-4,
          "gain %s" % (tuple(round(v, 5) for v in E),))
    check("C2  comment triple is NOT CREAM",
          max(abs(a - b) for a, b in zip(M.CREAM, COMMENT_TRIPLE)) > 0.05,
          "CREAM %s" % (M.CREAM,))
    de = tuple(lin(c) / e for c, e in zip(REC_TOP, E))
    check("C1  lin(top patch)/gain reproduces _UP_MEASURED",
          max(abs(a - b) for a, b in zip(de, M._UP_MEASURED)) < 1e-4,
          "%s" % (tuple(round(v, 5) for v in de),))

    # ------------------------------------------------------------------ C3
    print("\n=== C3 the live assert's agreement is a TAUTOLOGY ===")
    f_live = M.W_DUST_UP_W * M.W_DUST_MOT_MEAN * M.W_DUST_FAC_UP * 1.4
    fC = coverage(M.COUNTERCREAM, M.W_DUST_COL_UP, M._UP_MEASURED)
    fT = coverage(M.COUNTERTAN, M.W_DUST_COL_UP, M._UP_MEASURED)
    print("    live f_up = 0.85*0.630*W_DUST_FAC_UP*1.4 = %.6f" % f_live)
    print("    f | COUNTERCREAM  %s   spread %.6f" %
          (tuple(round(v, 4) for v in fC), max(fC) - min(fC)))
    print("    f | COUNTERTAN    %s   spread %.4f" %
          (tuple(round(v, 4) for v in fT), max(fT) - min(fT)))
    check("C3  COUNTERCREAM solve reproduces the live coverage",
          abs(np.mean(fC) - f_live) < 2e-3)
    check("C3  and it agrees in 3 channels BY CONSTRUCTION (collinear)",
          max(fC) - min(fC) < 1e-3,
          "spread %.1e -- this is the solve restated, not a check"
          % (max(fC) - min(fC)))
    # PER CHANNEL, not the max.  rev 27's first cut of the twin guard in
    # t1_mats.py asserted only the max; falsification showed the max lives in
    # B, so an R-channel move left it silent.  Cause fixed, band not widened.
    resid = tuple(M.COUNTERTAN[i] + f_live *
                  (M.W_DUST_COL_UP[i] - M.COUNTERTAN[i]) - M._UP_MEASURED[i]
                  for i in range(3))
    baseline = (-0.066877, -0.100324, -0.159974)
    check("C3  COUNTERTAN residual triple matches the rev-26 baseline",
          max(abs(r - b) for r, b in zip(resid, baseline)) < 2e-3,
          "%s" % (tuple(round(v, 6) for v in resid),))
    check("C3  and it is NEGATIVE in all three channels (outside the segment)",
          all(r < 0 for r in resid))

    if not os.path.exists(FRAME):
        print("\n  %s not present -- C4/C5 SKIPPED (declined, not passed)" % FRAME)
        print("\nRESULT: %s (C4/C5 not run)" % ("pass" if ok else "FAIL"))
        return 0 if ok else 1

    a = np.asarray(Image.open(FRAME).convert("RGB")).astype(np.float64)
    H, W, _ = a.shape
    mx, mn = a.max(axis=2), a.min(axis=2)
    S = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-9), 0.0)
    warm = (a[:, :, 0] >= a[:, :, 1]) & (a[:, :, 1] >= a[:, :, 2])

    # ------------------------------------------------------------------ C4
    print("\n=== C4 no clean 2700 px rectangle exists on the counter top ===")
    print("    (largest-rectangle-in-histogram over the tan class, gate SWEPT)")
    worst = 0
    for slo, shi in ((0.24, 0.54), (0.26, 0.52), (0.28, 0.50), (0.30, 0.48)):
        TAN = warm & (S >= slo) & (S < shi) & (mx > 120) & (mx < 250)
        sub = TAN[370:460, 500:720].astype(np.uint8)
        h, w = sub.shape
        heights = np.zeros(w, dtype=int)
        best = 0
        for i in range(h):
            heights = np.where(sub[i] > 0, heights + 1, 0)
            st = []
            for j in range(w + 1):
                cur = heights[j] if j < w else 0
                start = j
                while st and st[-1][1] >= cur:
                    idx, hh = st.pop()
                    best = max(best, hh * (j - idx))
                    start = idx
                st.append((start, cur))
        worst = max(worst, best)
        print("      gate [%.2f,%.2f)  largest clean rectangle %5d px  "
              "(patch needs 2700 -> %.2fx too big)" % (slo, shi, best, 2700.0 / best))
    check("C4  largest clean rectangle < 2700 px in EVERY gate arm",
          worst < 2700, "worst-case largest = %d px" % worst)

    # ------------------------------------------------------------------ C5
    print("\n=== C5 clean band-following sample, gate and erosion SWEPT ===")
    print("      gate        erode    n    median sRGB      f | COUNTERTAN")
    allneg = True
    n_arms = 0
    for slo, shi in ((0.24, 0.54), (0.26, 0.52), (0.28, 0.50), (0.30, 0.48)):
        TAN = warm & (S >= slo) & (S < shi) & (mx > 120) & (mx < 250)
        for er in (2, 3, 4):
            px = []
            for u in range(520, 700):
                col = TAN[380:452, u]
                best, cur, st = (0, None), 0, 0
                for i, v in enumerate(col):
                    if v:
                        if cur == 0:
                            st = i
                        cur += 1
                        if cur > best[0]:
                            best = (cur, st)
                    else:
                        cur = 0
                if best[0] < 2 * er + 4:
                    continue
                v0 = 380 + best[1] + er
                v1 = 380 + best[1] + best[0] - er
                px.extend(a[v0:v1, u])
            if len(px) < 200:
                continue
            med, n = trimmed_median(px)
            d = tuple(lin(c) / e for c, e in zip(med, E))
            f = coverage(M.COUNTERTAN, M.W_DUST_COL_UP, d)
            n_arms += 1
            allneg = allneg and max(f) < 0.0
            print("      [%.2f,%.2f)    %d   %5d  (%3d,%3d,%3d)   %s"
                  % (slo, shi, er, n, med[0], med[1], med[2],
                     tuple(round(v, 3) for v in f)))
    check("C5  every swept arm gives f < 0 in ALL THREE channels",
          allneg and n_arms >= 8,
          "%d arms; no physical coverage reaches the observed top from "
          "COUNTERTAN" % n_arms)

    # E-free statement -- no de-illumination, so no CREAM dependence
    print("\n=== E-FREE: same frame, same light, no de-illumination ===")
    top = np.array([lin(c) for c in (208.0, 176.0, 132.0)])   # clean band median
    flk = np.array([lin(c) for c in REC_FLK])
    r = top / flk
    for tag, base in (("dusty COUNTERTAN  ", M.COUNTERTAN),
                      ("dusty COUNTERCREAM", M.COUNTERCREAM)):
        pred = tuple((b + f_live * (d - b)) / c
                     for b, d, c in zip(base, M.W_DUST_COL_UP, M.CREAM))
        print("    observed top/flank %s   %s predicts %s"
              % (tuple(round(v, 4) for v in r), tag,
                 tuple(round(v, 4) for v in pred)))

    print("\n--- NOT CLAIMED ---")
    for line in ("which box rev 12 used -- several reproduce the median exactly;"
                 " C4 is box-independent",
                 "that COUNTERTAN is wrong, or that CREAM is wrong -- the "
                 "de-illuminated top is PROPORTIONAL to CREAM",
                 "that the up-facing top and the vertical flank share a light "
                 "-- SPEC 10.60's inadmissible pair, UNTESTED here",
                 "any repair.  SPEC 10.71 says do not repair it blind."):
        print("    * " + line)

    print("\nRESULT: %s" % ("all controls pass" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
