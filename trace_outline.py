"""Contour tracing for binary masks -- Moore-neighbour boundary following.

WHY IT EXISTS.  rev 63.  Every emblem attempt in this project's history has
APPROXIMATED the VW mark with a small parameter set (a 3-point V spine and a
5-point W spine, seven constants) and then fitted those constants to scalars
squeezed out of a photograph.  F175 showed three such scalars can all pass on a
glyph that renders as a Y, and a chamfer test showed the badge is too degraded a
target to separate a fan from a VW at all.  **The target was never the problem
the search could fix: a seven-parameter spine cannot BE the mark.**

So: trace the REAL PRESSING's outline off `ref_workshop.jpg` and build THAT.
The workshop badge is a different vehicle but the SAME factory pressing, and
`NEXT_CONTEXT_PROMPT_rev63` §0.1 rules explicitly on this: *"the nose roundel's
SHAPE is the factory chrome PRESSING, which is geometry and DOES transfer; only
its colour is artwork (F141)."*  Geometry transfers; paint does not (rule 11).

`selftest()` checks the tracer on shapes whose area and perimeter are known BY
CONSTRUCTION.  An instrument that has never been wrong has never been tested.
"""
import numpy as np


def _neighbours(y, x):
    return [(y - 1, x), (y - 1, x + 1), (y, x + 1), (y + 1, x + 1),
            (y + 1, x), (y + 1, x - 1), (y, x - 1), (y - 1, x - 1)]


def trace(mask):
    """-> list of closed contours, each an (N,2) float array of (y, x) in pixel
    coordinates, outermost boundary of each connected component, CCW in image
    space.  Holes are NOT traced -- the glyph strokes have none, and a silently
    dropped hole would be a defect that reads as a measurement (rule 37), so
    `has_holes()` below reports them and callers must check."""
    import scipy.ndimage as ndi
    lab, n = ndi.label(mask)
    out = []
    for k in range(1, n + 1):
        m = np.pad(lab == k, 1)
        ys, xs = np.nonzero(m)
        start = (int(ys.min()), int(xs[ys == ys.min()].min()))
        contour = [start]
        # find the first background neighbour to seed the search direction
        b = None
        for i, (ny, nx) in enumerate(_neighbours(*start)):
            if not m[ny, nx]:
                b = i
                break
        if b is None:
            continue
        cur, prev_b = start, b
        guard = 0
        while True:
            guard += 1
            if guard > 8 * m.size:
                break
            nb = _neighbours(*cur)
            found = None
            for j in range(8):
                i = (prev_b + 1 + j) % 8
                if m[nb[i]]:
                    found = i
                    break
            if found is None:
                break
            nxt = nb[found]
            prev_b = (found + 5) % 8
            if nxt == start and len(contour) > 2:
                break
            contour.append(nxt)
            cur = nxt
        out.append(np.array(contour, float) - 1.0)     # undo the pad
    return out


def trace_with_holes(mask):
    """-> list of (outer, [holes]) per connected component.

    THE FIRST VERSION OF THIS MODULE HAD ONLY `trace()`, WHICH RETURNS OUTER
    BOUNDARIES ONLY, AND probe_rev63_trace.py's T2/T3 CAUGHT IT: the VW glyph
    traces as ONE component WITH holes (the V and the W touch at the centre, so
    the cream cells between the strokes are enclosed), and filling the outer
    contour alone fills those cells too -- IoU against its own source was 0.6254,
    i.e. not a reproduction at all.  A trace that cannot reproduce its source is
    not a trace (rule 37: an instrument that cannot do the job must say so)."""
    import scipy.ndimage as ndi
    lab, n = ndi.label(mask)
    out = []
    for k in range(1, n + 1):
        comp = lab == k
        outer = trace(comp)
        if not outer:
            continue
        filled = ndi.binary_fill_holes(comp)
        holes = filled & ~comp
        hl, hn = ndi.label(holes)
        hs = []
        for j in range(1, hn + 1):
            h = hl == j
            if h.sum() < 4:
                continue
            t = trace(h)
            if t:
                hs.append(t[0])
        out.append((outer[0], hs))
    return out


def has_holes(mask):
    """True if any component encloses background -- the tracer would drop it."""
    import scipy.ndimage as ndi
    filled = ndi.binary_fill_holes(mask)
    return bool((filled & ~mask).sum())


def chaikin(p, n=3, closed=True):
    """Chaikin corner-cutting: smooths a blocky raster contour without the
    shrinkage a Gaussian would cause.  The badge is ~10 px per stroke, so a
    traced contour is a staircase; this is what turns it into a curve."""
    p = np.asarray(p, float)
    for _ in range(n):
        a = p
        b = np.roll(p, -1, axis=0) if closed else np.vstack([p[1:], p[-1]])
        p = np.empty((2 * len(a), 2))
        p[0::2] = 0.75 * a + 0.25 * b
        p[1::2] = 0.25 * a + 0.75 * b
    return p


def simplify(p, tol):
    """Douglas-Peucker on a CLOSED contour, so the mesh does not carry one
    vertex per pixel."""
    p = np.asarray(p, float)

    def dp(pts):
        if len(pts) < 3:
            return pts
        a, b = pts[0], pts[-1]
        d = b - a
        L = np.hypot(*d)
        if L < 1e-9:
            dist = np.hypot(*(pts - a).T)
        else:
            dist = np.abs(np.cross(np.tile(d, (len(pts), 1)), pts - a)) / L
        i = int(np.argmax(dist))
        if dist[i] <= tol:
            return np.array([a, b])
        return np.vstack([dp(pts[:i + 1])[:-1], dp(pts[i:])])

    half = len(p) // 2
    return np.vstack([dp(p[:half + 1])[:-1], dp(p[half:])[:-1]])


def area(p):
    x, y = p[:, 1], p[:, 0]
    return abs(float(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))) / 2.0


def perimeter(p):
    d = p - np.roll(p, -1, axis=0)
    return float(np.hypot(d[:, 0], d[:, 1]).sum())


def selftest():
    out = []
    N = 400
    yy, xx = np.mgrid[0:N, 0:N]
    c = (N - 1) / 2.0
    # 1. a disc: area pi r^2, perimeter 2 pi r -- both known by construction
    R = 150.0
    disc = ((yy - c) ** 2 + (xx - c) ** 2) <= R ** 2
    cs = trace(disc)
    out.append(("disc -> one contour", len(cs) == 1, "%d" % len(cs)))
    a, pm = area(cs[0]), perimeter(cs[0])
    out.append(("disc area", abs(a - np.pi * R ** 2) / (np.pi * R ** 2) < 0.02,
                "%.0f vs %.0f" % (a, np.pi * R ** 2)))
    # a staircase boundary overstates perimeter; Chaikin must bring it to ~2 pi R
    sm = chaikin(cs[0], 4)
    out.append(("disc perimeter after chaikin",
                abs(perimeter(sm) - 2 * np.pi * R) / (2 * np.pi * R) < 0.03,
                "raw %.0f, smoothed %.0f, true %.0f"
                % (pm, perimeter(sm), 2 * np.pi * R)))
    # 2. two separate squares -> two contours, each of known area
    sq = np.zeros((N, N), bool)
    sq[40:140, 40:140] = True
    sq[240:340, 240:340] = True
    cs = trace(sq)
    out.append(("two squares -> two contours", len(cs) == 2, "%d" % len(cs)))
    out.append(("square area", all(abs(area(k) - 100 * 100) / 10000 < 0.05
                                   for k in cs),
                ", ".join("%.0f" % area(k) for k in cs)))
    # 3. simplify must not move the shape much
    s = simplify(chaikin(trace(disc)[0], 3), 1.0)
    out.append(("simplify keeps the area",
                abs(area(s) - np.pi * R ** 2) / (np.pi * R ** 2) < 0.02,
                "%.0f vs %.0f, %d verts" % (area(s), np.pi * R ** 2, len(s))))
    # 4. a ring HAS a hole and has_holes must say so, or the tracer would
    #    silently return only its outside (rule 37).
    ring = disc & ~(((yy - c) ** 2 + (xx - c) ** 2) <= (R / 2) ** 2)
    out.append(("has_holes detects a ring", has_holes(ring), "reported"))
    out.append(("has_holes clears a disc", not has_holes(disc), "clear"))
    # 5. trace_with_holes on a RING: one component, one hole, and the annulus
    #    area is known by construction.
    twh = trace_with_holes(ring)
    ok1 = len(twh) == 1 and len(twh[0][1]) == 1
    out.append(("ring -> 1 outer + 1 hole", ok1,
                "%d comp, %d hole(s)" % (len(twh), len(twh[0][1]) if twh else 0)))
    if ok1:
        a = area(twh[0][0]) - area(twh[0][1][0])
        want = np.pi * (R ** 2 - (R / 2) ** 2)
        out.append(("annulus area from outer minus hole",
                    abs(a - want) / want < 0.03, "%.0f vs %.0f" % (a, want)))
    return out


if __name__ == "__main__":
    ok = True
    for n, g, d in selftest():
        print("   %-32s %s  %s" % (n, "ok " if g else "FAIL", d))
        ok &= g
    print("SELFTEST", "PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
