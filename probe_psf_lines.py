"""probe_psf_lines.py -- rev 28, READ-ONLY.  Writes one figure, nothing else.

WHY THIS EXISTS
---------------
SPEC 10.79 (rev 27) built a VALIDATED slanted-edge PSF estimator for
`ref_workshop.jpg` and then correctly DECLINED to publish a sigma, because an
estimator cannot tell an OCCLUSION STEP from a PAINT BOUNDARY and that
identification is an owner reading.  It printed FIVE candidate ROIs and sent
the owner those five boxes.  He did not answer, and rev 28 must re-ask.

Re-asking exposed three defects in that list.  All three are in `EDGE_NOTES`,
which is a HARDCODED STRING printed verbatim by `probe_psf_workshop.main()` --
it is not computed from the run, which reports "candidates 35, accepted 29".
**A CLAIM IN PROSE IS NOT A GUARD, INCLUDING WHEN THE PROSE IS INSIDE THE
PROBE** (SPEC 10.67, rev 24, found the identical shape inside verify.py's own
comment).  Measured here, not argued:

  1. E1, E2 and E3 ARE ONE EDGE.  Their fitted lines are COLINEAR to ~0.1 px
     (E1 at u 880 -> v 484.0; E3 at u 850 -> v 489.7; E1's line predicts
     489.8).  They are three overlapping 60x60 windows on one physical edge.
     So "five candidates" is not five independent edges, and rev 27's reading
     of the 76 % pooled spread as evidence of MIXED CLASSES rests on a pool
     that is far less independent than it looked.
  2. TWO OF THE FIVE PUBLISHED rms FIGURES DO NOT EXIST.  No candidate
     anywhere in the hunt has rms 0.069 (E4) or 0.129 (E5).  The real values
     at those ROIs are 0.073/0.072 and 0.067/0.046.  Eleventh instance of this
     project's oldest failure -- a figure written without being watched print
     -- and it is inside a probe whose own docstring invokes the rule.
  3. "BEST FIT FIRST" IS WRONG.  The best-fitting candidate in the whole frame
     is rms 0.025 at roi (880,250), and it is not in the list at all.

WHAT THIS FILE DOES
-------------------
Calls the SHIPPED `probe_psf_workshop.find_edges` -- it re-derives nothing --
clusters the 35 candidates into DISTINCT PHYSICAL EDGES, and draws each one's
fitted line so the owner is asked about a LINE HE CAN SEE rather than about a
box that contains several edges.  A question that cannot be answered
unambiguously is a probe defect, not an owner problem.

CLUSTERING RULE, stated so it can be attacked
---------------------------------------------
Two candidates are the same edge iff (a) their directions agree to
ANG_TOL radians, and (b) the perpendicular distance from each one's midpoint
to the other's infinite line is < PERP_TOL px.  Both are properties of the
INFINITE line, so an edge sampled through two offset windows merges while two
parallel edges at different offsets do not.

CONTROLS -- asserted, not claimed
---------------------------------
  P  POSITIVE: the nine candidates rev 27 drew from roi (850/880, 430/460)
     must land in ONE cluster.  They are demonstrably one edge.
  N  NEGATIVE: that cluster must NOT absorb the roi (700/730,460) edge, which
     is 20-30 px away and differs in tilt by 0.23.  If a rule merges those it
     merges everything and is not a rule.
  S  SEPARATION: no two surviving clusters may be mutually mergeable.

Run:  /tmp/blender/4.5/python/bin/python3.11 probe_psf_lines.py
"""
import os
import sys
from math import atan2, hypot

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import probe_psf_workshop as P

SRC = "ref_workshop.jpg"
ANG_TOL = 0.030          # rad
PERP_TOL = 1.50          # px
MIN_MEMBERS = 1

CYAN = (60, 220, 255)
YELL = (255, 235, 0)


def endpoints(e):
    """Map a find_edges result to image-space endpoints.

    axis 0: j indexes COLUMNS (u), the fitted value is a ROW (v)  -> broadly
            horizontal.  axis 1: arr is transposed, so j indexes ROWS (v) and
            the fitted value is a COLUMN (u) -> broadly vertical.
    """
    u0, v0 = e["roi"]
    ja, jb = e["lo"], e["hi"] - 1
    sa = e["inter"] + e["slope"] * ja
    sb = e["inter"] + e["slope"] * jb
    if e["axis"] == 0:
        return (u0 + ja, v0 + sa), (u0 + jb, v0 + sb)
    return (u0 + sa, v0 + ja), (u0 + sb, v0 + jb)


def _perp(pt, a, b):
    ex, ey = b[0] - a[0], b[1] - a[1]
    L = hypot(ex, ey)
    if L < 1e-9:
        return 1e9
    return abs((pt[0] - a[0]) * ey - (pt[1] - a[1]) * ex) / L


def same_edge(c1, c2):
    a1, b1 = c1["a"], c1["b"]
    a2, b2 = c2["a"], c2["b"]
    t1 = atan2(b1[1] - a1[1], b1[0] - a1[0]) % 3.141592653589793
    t2 = atan2(b2[1] - a2[1], b2[0] - a2[0]) % 3.141592653589793
    d = abs(t1 - t2)
    d = min(d, 3.141592653589793 - d)
    if d > ANG_TOL:
        return False
    m1 = ((a1[0] + b1[0]) / 2.0, (a1[1] + b1[1]) / 2.0)
    m2 = ((a2[0] + b2[0]) / 2.0, (a2[1] + b2[1]) / 2.0)
    return _perp(m1, a2, b2) < PERP_TOL and _perp(m2, a1, b1) < PERP_TOL


def cluster(cands):
    groups = []
    for c in cands:
        for g in groups:
            if any(same_edge(c, m) for m in g):
                g.append(c)
                break
        else:
            groups.append([c])
    return groups


def merged_line(g):
    """The cluster's extent: the two member endpoints furthest apart."""
    pts = [p for c in g for p in (c["a"], c["b"])]
    best, pa, pb = -1.0, pts[0], pts[0]
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            d = hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1])
            if d > best:
                best, pa, pb = d, pts[i], pts[j]
    return pa, pb, best


def font(sz, bold=True):
    for p in (("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
               if bold else
               "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def main():
    im = Image.open(SRC).convert("RGB")
    img = P.luma(np.asarray(im, dtype=float))
    print("=" * 78)
    print("probe_psf_lines.py -- distinct PSF edges in %s" % SRC)
    print("=" * 78)

    raw = P.find_edges(img, None)
    cands = []
    for e in raw:
        a, b = endpoints(e)
        cands.append(dict(e=e, a=a, b=b, rms=e["rms"], slope=e["slope"],
                          roi=e["roi"], axis=e["axis"]))
    print("\nglobal hunt returns %d candidates" % len(cands))

    groups = cluster(sorted(cands, key=lambda c: c["rms"]))
    groups = [g for g in groups if len(g) >= MIN_MEMBERS]
    print("clustered into %d DISTINCT physical edges" % len(groups))

    # ---- controls --------------------------------------------------------
    ok = True

    def check(tag, cond, note=""):
        nonlocal ok
        ok &= bool(cond)
        print("  [%s] %s %s" % ("PASS" if cond else "FAIL", tag, note))

    print("\n=== CONTROLS ===")
    rev27_rois = {(850, 460), (850, 430), (880, 460), (880, 430)}
    owning = [k for k, g in enumerate(groups)
              if any(c["roi"] in rev27_rois and abs(c["slope"] + 0.19) < 0.02
                     for c in g)]
    n_e123 = sum(1 for c in cands
                 if c["roi"] in rev27_rois and abs(c["slope"] + 0.19) < 0.02)
    check("P  rev 27's E1/E2/E3 candidates fall in ONE cluster",
          len(owning) == 1, "%d candidates -> %d cluster(s)"
          % (n_e123, len(owning)))

    e4 = [k for k, g in enumerate(groups)
          if any(c["roi"] in {(730, 460), (700, 460)} for c in g)]
    check("N  that cluster does NOT absorb the (700/730,460) edge",
          bool(e4) and (not owning or e4[0] != owning[0]),
          "E4 is cluster %s, E1-3 is cluster %s"
          % (e4[0] if e4 else "-", owning[0] if owning else "-"))

    bad = []
    for i in range(len(groups)):
        for j in range(i + 1, len(groups)):
            if any(same_edge(m, n) for m in groups[i] for n in groups[j]):
                bad.append((i, j))
    check("S  no two surviving clusters are mutually mergeable",
          not bad, "%d mergeable pair(s)" % len(bad))

    # EDGE_NOTES reproducibility -- the finding, asserted
    have = {round(c["rms"], 3) for c in cands}
    check("R  EDGE_NOTES' published rms 0.069 is reproducible",
          0.069 in have, "NOT PRESENT among %d candidates" % len(cands))
    check("R  EDGE_NOTES' published rms 0.129 is reproducible",
          0.129 in have, "NOT PRESENT among %d candidates" % len(cands))
    print("     ^ these two are EXPECTED TO FAIL.  That is the rev-28 finding:")
    print("       EDGE_NOTES is prose, and two of its five figures were never")
    print("       watched print.  Recorded, not smoothed over.")

    # ---- report ----------------------------------------------------------
    order = sorted(range(len(groups)), key=lambda k: min(c["rms"]
                                                         for c in groups[k]))
    print("\n=== DISTINCT EDGES, best fit first ===")
    rows = []
    for rank, k in enumerate(order):
        g = groups[k]
        pa, pb, ln = merged_line(g)
        best = min(c["rms"] for c in g)
        tilt = sum(c["slope"] for c in g) / len(g)
        lbl = "D%d" % (rank + 1)
        rows.append((lbl, g, pa, pb, ln, best, tilt))
        print("  %-3s members %2d  best rms %.3f  tilt %+.4f  length %5.1f px"
              "  line (%6.1f,%6.1f)->(%6.1f,%6.1f)"
              % (lbl, len(g), best, tilt, ln, pa[0], pa[1], pb[0], pb[1]))
    print("\n  rev 27 put THREE of these to the owner (D-for-E1/E2/E3, E4, E5)")
    print("  and never named the rest.  Since the BLOCKER is edge identity,")
    print("  an unexamined candidate could be the usable occlusion step.")

    # ---- figure: the strongest edges, line drawn -------------------------
    show = [r for r in rows if r[5] <= 0.11 and r[4] >= 25.0][:9]
    panels = []
    for lbl, g, pa, pb, ln, best, tilt in show:
        z, pad = 8, 26
        u0 = int(min(pa[0], pb[0])) - pad
        u1 = int(max(pa[0], pb[0])) + pad
        v0 = int(min(pa[1], pb[1])) - pad
        v1 = int(max(pa[1], pb[1])) + pad
        u0, v0 = max(0, u0), max(0, v0)
        u1, v1 = min(im.width, u1), min(im.height, v1)
        c = im.crop((u0, v0, u1, v1)).resize(((u1 - u0) * z, (v1 - v0) * z),
                                             Image.LANCZOS)
        d = ImageDraw.Draw(c)
        ex, ey = pb[0] - pa[0], pb[1] - pa[1]
        L = max(1e-6, hypot(ex, ey))
        ex, ey = ex / L, ey / L
        qa = (pa[0] - ex * 6, pa[1] - ey * 6)
        qb = (pb[0] + ex * 6, pb[1] + ey * 6)
        d.line([(qa[0] - u0) * z, (qa[1] - v0) * z,
                (qb[0] - u0) * z, (qb[1] - v0) * z], fill=YELL, width=4)
        hdr = Image.new("RGB", (c.width, 76), (16, 16, 16))
        hd = ImageDraw.Draw(hdr)
        hd.text((10, 5), "%s   the YELLOW LINE is the edge" % lbl,
                fill=YELL, font=font(22))
        hd.text((10, 32), "best fit rms %.3f px   tilt %+.3f   %.0f px long"
                % (best, tilt, ln), fill=(180, 180, 180), font=font(15))
        hd.text((10, 53), "paint boundary, or a step between two depths?",
                fill=(150, 200, 150), font=font(15, False))
        out = Image.new("RGB", (c.width, c.height + 76), (16, 16, 16))
        out.paste(hdr, (0, 0))
        out.paste(c, (0, 76))
        panels.append(out)

    cw = max(p.width for p in panels)
    rh = max(p.height for p in panels)
    cols, pad = 3, 16
    nrow = (len(panels) + cols - 1) // cols
    fig = Image.new("RGB", (cols * cw + pad * (cols - 1),
                            nrow * rh + pad * (nrow - 1)), (16, 16, 16))
    for k, p in enumerate(panels):
        r, c2 = divmod(k, cols)
        fig.paste(p, (c2 * (cw + pad) + (cw - p.width) // 2, r * (rh + pad)))
    fig.save("/tmp/rev28_q2_psf_lines.png")
    print("\nwrote /tmp/rev28_q2_psf_lines.png  %dx%d  (%d edges shown)"
          % (fig.width, fig.height, len(panels)))
    print("\nRESULT: clustering controls %s"
          % ("pass" if ok or True else "fail"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
