"""A minimal, CONTROLLED SVG path rasteriser -- nonzero winding, numpy scanline.

WHY THIS EXISTS.  rev 63 obtained a CANONICAL VECTOR of the VW mark (see
probe_rev63_canon.py).  This machine has no cairosvg / svglib / skia, so the
vector has to be rasterised here.  A rasteriser is an INSTRUMENT, and an
instrument that has never been wrong has never been tested (CLAUDE.md rule 4):
`selftest()` below checks it against three shapes whose answer is known BY
CONSTRUCTION -- a square, an annulus (which is the nonzero rule's whole point),
and a triangle -- and probe_rev63_canon.py refuses to publish if it fails.

Supports M L H V C S Z, absolute and relative.  No arcs: the canonical file
uses none, and a silently-ignored arc would be a defect that reads as a
measurement (rule 37).  An unsupported command RAISES.
"""
import re
import numpy as np

_TOK = re.compile(r'([MmLlHhVvCcSsZzAaQqTt])|(-?\d*\.?\d+(?:[eE][-+]?\d+)?)')


def _nums(path):
    out = []
    for m in _TOK.finditer(path):
        out.append(m.group(1) if m.group(1) else float(m.group(2)))
    return out


def flatten(path, steps=48):
    """-> list of subpaths, each a list of (x, y) vertices. Cubics flattened."""
    toks = _nums(path)
    i = 0
    subs, cur = [], []
    x = y = 0.0
    start = (0.0, 0.0)
    cmd = None
    prev_c2 = None          # for S: reflection of the previous cubic's C2

    def cubic(p0, c1, c2, p1):
        t = np.linspace(0.0, 1.0, steps + 1)[1:]
        mt = 1.0 - t
        xs = (mt**3 * p0[0] + 3 * mt**2 * t * c1[0]
              + 3 * mt * t**2 * c2[0] + t**3 * p1[0])
        ys = (mt**3 * p0[1] + 3 * mt**2 * t * c1[1]
              + 3 * mt * t**2 * c2[1] + t**3 * p1[1])
        return list(zip(xs.tolist(), ys.tolist()))

    while i < len(toks):
        t = toks[i]
        if isinstance(t, str):
            cmd = t
            i += 1
            if cmd in 'Zz':
                if cur:
                    subs.append(cur)
                cur = []
                x, y = start
                prev_c2 = None
                continue
        # implicit repeat: M/m repeats as L/l
        c = cmd
        if c == 'M' and cur:
            c = 'M'
        rel = c.islower()
        C = c.upper()
        if C == 'M':
            nx, ny = toks[i], toks[i + 1]; i += 2
            x, y = (x + nx, y + ny) if rel else (nx, ny)
            if cur:
                subs.append(cur)
            cur = [(x, y)]
            start = (x, y)
            cmd = 'l' if rel else 'L'      # subsequent pairs are lineto
            prev_c2 = None
        elif C == 'L':
            nx, ny = toks[i], toks[i + 1]; i += 2
            x, y = (x + nx, y + ny) if rel else (nx, ny)
            cur.append((x, y)); prev_c2 = None
        elif C == 'H':
            nx = toks[i]; i += 1
            x = x + nx if rel else nx
            cur.append((x, y)); prev_c2 = None
        elif C == 'V':
            ny = toks[i]; i += 1
            y = y + ny if rel else ny
            cur.append((x, y)); prev_c2 = None
        elif C == 'C':
            a, b, cc, dd, e, f = toks[i:i + 6]; i += 6
            if rel:
                c1 = (x + a, y + b); c2 = (x + cc, y + dd); p1 = (x + e, y + f)
            else:
                c1 = (a, b); c2 = (cc, dd); p1 = (e, f)
            cur += cubic((x, y), c1, c2, p1)
            prev_c2 = c2; x, y = p1
        elif C == 'S':
            cc, dd, e, f = toks[i:i + 4]; i += 4
            if rel:
                c2 = (x + cc, y + dd); p1 = (x + e, y + f)
            else:
                c2 = (cc, dd); p1 = (e, f)
            c1 = (2 * x - prev_c2[0], 2 * y - prev_c2[1]) if prev_c2 else (x, y)
            cur += cubic((x, y), c1, c2, p1)
            prev_c2 = c2; x, y = p1
        else:
            raise ValueError("svgraster: unsupported path command %r -- "
                             "refusing to rasterise silently" % c)
    if cur:
        subs.append(cur)
    return subs


def fill(subs, n, box, fill_rule='nonzero', ss=3):
    """Rasterise subpaths to an n x n boolean mask over box=(x0,y0,x1,y1).

    ss = supersampling factor per axis; the mask is the >=50 % coverage set.
    y grows DOWNWARD in SVG, and the returned array's row 0 is y0."""
    x0, y0, x1, y1 = box
    N = n * ss
    px = x0 + (np.arange(N) + 0.5) * (x1 - x0) / N
    py = y0 + (np.arange(N) + 0.5) * (y1 - y0) / N
    X = px[None, :]
    wind = np.zeros((N, N), dtype=np.int32)
    for sp in subs:
        p = np.asarray(sp, dtype=float)
        if len(p) < 3:
            continue
        if p[0][0] != p[-1][0] or p[0][1] != p[-1][1]:
            p = np.vstack([p, p[0]])
        ax, ay = p[:-1, 0], p[:-1, 1]
        bx, by = p[1:, 0], p[1:, 1]
        for j in range(len(ax)):
            yA, yB = ay[j], by[j]
            if yA == yB:
                continue
            lo, hi = (yA, yB) if yA < yB else (yB, yA)
            rows = np.where((py >= lo) & (py < hi))[0]
            if not len(rows):
                continue
            t = (py[rows] - yA) / (yB - yA)
            xc = ax[j] + t * (bx[j] - ax[j])
            step = 1 if yB > yA else -1
            wind[rows] += step * (X < xc[:, None])
    m = (wind != 0) if fill_rule == 'nonzero' else ((wind % 2) != 0)
    return (m.reshape(n, ss, n, ss).mean(axis=(1, 3)) >= 0.5)


def selftest():
    """Shapes whose answer is known BY CONSTRUCTION.  Returns (name, ok, detail).
    A rasteriser that has never been wrong has never been tested."""
    out = []
    BOX = (-0.5, -0.5, 1.5, 1.5)          # a 2 x 2 box, so area = frac * 4

    # 1. unit square via M H V H Z -- tests M, H, V, Z and the fill's edges.
    f = fill(flatten("M0 0 H1 V1 H0 Z"), 240, BOX).mean() * 4.0
    out.append(("square area", abs(f - 1.0) < 0.01, "%.4f vs 1.0000" % f))

    # 2. triangle via L -- tests sloped edges (the winding interpolation).
    f = fill(flatten("M0 0 L1 0 L0 1 Z"), 240, BOX).mean() * 4.0
    out.append(("triangle area", abs(f - 0.5) < 0.01, "%.4f vs 0.5000" % f))

    # 3. THE SAME TRIANGLE DRAWN WITH CUBICS whose control points are collinear
    #    -> each cubic IS its chord.  Tests flatten's C against a shape the L
    #    version already pinned, so a bad Bezier cannot hide.
    f = fill(flatten("M0 0 C0.33 0 0.67 0 1 0 C0.67 0.33 0.33 0.67 0 1 "
                     "C0 0.67 0 0.33 0 0 Z"), 240, BOX).mean() * 4.0
    out.append(("triangle via C", abs(f - 0.5) < 0.02, "%.4f vs 0.5000" % f))

    # 3b. S BY EQUIVALENCE, NOT BY AREA.
    #     The FIRST version of this control was WRONG and is recorded here
    #     because that is the point of a control: it drew a triangle with a
    #     trailing S and demanded area 0.5, but an S REFLECTS the previous
    #     control point, so at a corner its implied handle necessarily leaves
    #     the chord.  It read 0.5828 and the defect was the CONTROL, not the
    #     rasteriser.  S is testable only against an explicit C that is
    #     constructed to be the same curve -- here c1 of the second segment is
    #     exactly the reflection of (0.4,0.5) about (0.6,0.3).  The two masks
    #     must be IDENTICAL, pixel for pixel.
    pc = fill(flatten("M0 0 C0.2 0.5 0.4 0.5 0.6 0.3 C0.8 0.1 0.9 0.2 1 0.4 "
                      "L1 -1 L0 -1 Z"), 240, BOX)
    ps = fill(flatten("M0 0 C0.2 0.5 0.4 0.5 0.6 0.3 S0.9 0.2 1 0.4 "
                      "L1 -1 L0 -1 Z"), 240, BOX)
    d = int((pc != ps).sum())
    out.append(("S == its explicit C", d == 0, "%d pixels differ" % d))

    # 3c. AND THE EQUIVALENCE CONTROL MUST BE ABLE TO FAIL (rule 3).
    #     Perturb the S's own endpoint and the two masks must diverge.
    pw = fill(flatten("M0 0 C0.2 0.5 0.4 0.5 0.6 0.3 S0.9 0.2 1 0.6 "
                      "L1 -1 L0 -1 Z"), 240, BOX)
    dw = int((pc != pw).sum())
    out.append(("KILL: equivalence can fail", dw > 50, "%d pixels differ" % dw))

    # 4. ANNULUS BY THE NONZERO RULE -- outer ring one way, inner the OTHER.
    #    This is the control that matters: an even-odd reading, or a naive
    #    per-subpath fill, would fill the VW ring SOLID and every cream cell
    #    would vanish.  Built as explicit vertices so the control tests `fill`
    #    and not the circle-to-Bezier approximation.
    th = np.linspace(0, 2 * np.pi, 721)[:-1]
    outer = list(zip(np.cos(th), np.sin(th)))
    inner = list(zip(np.cos(-th) * 0.5, np.sin(-th) * 0.5))
    m = fill([outer, inner], 400, (-1.2, -1.2, 1.2, 1.2))
    got = m.mean() * (2.4 ** 2)
    want = np.pi * (1.0 - 0.25)
    out.append(("annulus area", abs(got - want) / want < 0.01,
                "%.4f vs %.4f" % (got, want)))
    out.append(("annulus HOLE is empty", not bool(m[200, 200]),
                "centre pixel is %s" % ("INK -- NONZERO IS BROKEN"
                                        if m[200, 200] else "hole")))
    out.append(("annulus BAND is ink", bool(m[200, 200 + int(0.75 / 2.4 * 400)]),
                "mid-band pixel"))

    # 5. AN UNSUPPORTED COMMAND MUST RAISE, NOT BE IGNORED (rule 37).
    try:
        flatten("M0 0 A1 1 0 0 1 1 1 Z")
        out.append(("arc refuses silently", False, "flatten() ACCEPTED an arc"))
    except ValueError:
        out.append(("arc RAISES", True, "unsupported command refuses"))
    return out


if __name__ == "__main__":
    ok = True
    for n, good, d in selftest():
        print("   %-24s %s   %s" % (n, "ok " if good else "FAIL", d))
        ok &= good
    print("SELFTEST", "PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
