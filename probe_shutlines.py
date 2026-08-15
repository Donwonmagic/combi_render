"""probe_shutlines.py -- rev 22, READ-ONLY.

Enumerate every SHUT LINE x APERTURE and SHUT LINE x ARCH crossing, with a
measured arc length rather than a yes/no, so item 4's guard can be armed
against a number somebody watched print.

WHY THIS IS A PROBE AND NOT THE GUARD
SPEC 10.45 found the only existing structural assert (t1_shell.py:451) covers
1 of 4 shut lines, 1 of 2 arches and 0 of 5 apertures.  rev 18/19/20/21 all
carried "five crossings, 1209 mm total, one on the show flank" forward as a
CLAIM.  Before generalising the assert, the claim has to be reproduced, and
each crossing has to be attributed to a specific pair -- otherwise the guard
gets armed against a total nobody can decompose.

WHAT A NAIVE VERSION WOULD GET WRONG, and why this one is built the way it is:

  (1) FRAMES.  DOOR_GAP and CARGO_GAP are (x, z).  ENGLID_GAP is (y, z), on
      the TAIL.  Comparing englid to a flank aperture in one loop would
      manufacture crossings out of a coordinate mismatch.  englid is reported
      SEPARATELY and explicitly, never silently skipped.

  (2) SIDES.  The serving apertures are cut on BOTH flanks by side_cutters(),
      but the three serving BAYS are only OPEN on +Y (SHOW_SIDE); on -Y they
      carry glass.  gap_cargo is on -Y only, gap_door on both.  A test that
      ignores the side reports the cargo line crossing a +Y serving hatch,
      which is on the other side of the vehicle.

  (3) THE STATISTIC.  "Do the polygons intersect" is a bit; what the geometry
      cares about is HOW MUCH shut line lies inside an aperture.  This walks
      the outline at ~1 mm and sums the arc length of the samples that fall
      inside, so the answer is in millimetres and can be compared revision to
      revision.

  (4) IT MUST BE ABLE TO SAY NO.  A probe that cannot answer must return None,
      not an endpoint (SPEC 10.45).  The point-in-polygon test is exercised
      against a known-outside control before any result is believed.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_core as T
import t1_shell as S


def _inside(pt, poly):
    """Ray-crossing point-in-polygon. Returns a bool, never a guess."""
    x, z = pt
    n = len(poly)
    c = False
    j = n - 1
    for i in range(n):
        xi, zi = poly[i]
        xj, zj = poly[j]
        if ((zi > z) != (zj > z)) and \
           (x < (xj - xi) * (z - zi) / ((zj - zi) or 1e-30) + xi):
            c = not c
        j = i
    return c


def _densify(poly, step=0.001):
    """Resample a closed outline to ~`step` spacing, carrying segment length."""
    out = []
    n = len(poly)
    for i in range(n):
        x0, z0 = poly[i]
        x1, z1 = poly[(i + 1) % n]
        seg = math.hypot(x1 - x0, z1 - z0)
        k = max(1, int(math.ceil(seg / step)))
        for t in range(k):
            f = t / k
            out.append(((x0 + (x1 - x0) * f, z0 + (z1 - z0) * f), seg / k))
    return out


def _arc_inside(line, poly):
    """Metres of `line` that fall strictly inside `poly`."""
    return sum(w for p, w in _densify(line) if _inside(p, poly))


def _bay_poly(i):
    cx, cz = S.bay_centre(i)
    return [(u + cx, v + cz) for (u, v) in S.bay_outline(i)]


def main():
    print("=" * 78)
    print("SHUT LINE x APERTURE / ARCH CROSSINGS -- rev 22 probe, READ-ONLY")
    print("=" * 78)

    # ---- CONTROL FIRST (SPEC 10.55: build the control, prove it, then test).
    sq = [(0.0, 0.0), (0.1, 0.0), (0.1, 0.1), (0.0, 0.1)]
    assert _inside((0.05, 0.05), sq) and not _inside((0.5, 0.5), sq), \
        "point-in-polygon control FAILED -- no result below is admissible"
    ctrl_far = [(9.0, 9.0), (9.1, 9.0), (9.1, 9.1), (9.0, 9.1)]
    ctrl = _arc_inside(S.DOOR_GAP_S, ctrl_far)
    print("control: point-in-polygon ok; door line vs a far-away box = "
          "%.4f m (must be 0.0000)" % ctrl)
    assert ctrl == 0.0
    print()

    # ---- the five apertures, per flank, in the (x, z) flank frame.
    apertures = [("door_main", S.DOOR_MAIN_S), ("door_vent", S.DOOR_VENT_S)]
    for i in range(len(S.BAYS)):
        apertures.append(("bay%d" % i, _bay_poly(i)))

    # ---- the shut lines that live in the FLANK frame, with the side each is
    #      actually cut on.  englid is (y, z) on the tail and is handled below.
    flank_lines = [("gap_door+1", S.DOOR_GAP_S, +1),
                   ("gap_door-1", S.DOOR_GAP_S, -1),
                   ("gap_cargo", S.CARGO_GAP, -1)]

    total = 0.0
    hits = 0
    print("--- SHUT LINE x APERTURE (same flank only) ---")
    for lname, line, side in flank_lines:
        for aname, poly in apertures:
            open_here = True
            if aname.startswith("bay"):
                i = int(aname[3:])
                open_here = (side == S.SHOW_SIDE and i in S.OPEN_BAYS)
            L = _arc_inside(line, poly)
            if L > 1e-9:
                hits += 1
                total += L
                print("  %-11s x %-9s side %+d  %7.1f mm INSIDE   "
                      "(aperture %s)"
                      % (lname, aname, side, L * 1000,
                         "OPEN - real hole" if open_here else "glazed"))
    print("  -> %d crossings, %.1f mm total" % (hits, total * 1000))
    print()

    # ---- arches.  The existing assert covers exactly one of these four pairs.
    print("--- SHUT LINE x ARCH LIP ---")
    for lname, line, side in flank_lines:
        for arch, xa in (("front", T.X_AXLE_F), ("rear", T.X_AXLE_R)):
            top = S.arch_z(xa) + S.ARCH_R
            x0, x1 = xa - S.ARCH_R, xa + S.ARCH_R
            over = [z for (x, z) in line if x0 <= x <= x1]
            if not over:
                print("  %-11s x %-5s arch  side %+d  outline does not span "
                      "the arch station -- no test possible (None)"
                      % (lname, arch, side))
                continue
            m = min(over)
            print("  %-11s x %-5s arch  side %+d  lowest z over arch %.4f vs "
                  "lip %.4f  -> %+7.1f mm %s"
                  % (lname, arch, side, m, top, (m - top) * 1000,
                     "CLEAR" if m > top + 0.010 else "** CROSSES / <10 mm **"))
    print()

    # ---- englid, stated rather than skipped.
    print("--- gap_englid ---")
    zs = [z for (_, z) in S.ENGLID_GAP]
    ys = [y for (y, _) in S.ENGLID_GAP]
    print("  ENGLID_GAP is in the (y, z) TAIL frame: y %.3f..%.3f  z %.3f..%.3f"
          % (min(ys), max(ys), min(zs), max(zs)))
    print("  It is cut on the tail face at x = X_TAIL + ENGLID_CUT_DX = %.4f."
          % (T.X_TAIL + S.ENGLID_CUT_DX))
    print("  No flank aperture shares that surface, so a flank crossing test "
          "is NOT APPLICABLE here -- reported, not silently skipped.")
    print()

    # ---- CARGO_GAP's sampling, the second half of item 4.
    print("--- CARGO_GAP sample distribution (SPEC 10.45's second finding) ---")
    pts = S.CARGO_GAP
    n = len(pts)
    xs = [p[0] for p in pts]
    zs = [p[1] for p in pts]
    x0, x1, z0, z1 = min(xs), max(xs), min(zs), max(zs)
    r = 0.045
    corner = sum(1 for (x, z) in pts
                 if (min(abs(x - x0), abs(x - x1)) < r and
                     min(abs(z - z0), abs(z - z1)) < r))
    print("  %d samples; %d lie on the four corner arcs = %.1f %% of the "
          "outline's points" % (n, corner, 100.0 * corner / n))
    print("  straight runs therefore carry %d samples" % (n - corner))
    print()
    print("=" * 78)
    print("This probe CHANGES NOTHING. It is the grounding for arming the")
    print("generalised assert. Expect the assert to FAIL when first armed --")
    print("that is the guard working; fix the geometry, never the threshold.")
    print("=" * 78)


if __name__ == "__main__":
    main()
