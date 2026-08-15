"""probe_cross_anatomy.py -- rev 23, READ-ONLY. Changes nothing.

WHY THIS EXISTS
rev 23's brief says: arm item 4's assert, expect it to FAIL, and fix the
GEOMETRY rather than the threshold.  That brief is a probe too (SPEC 10.43,
10.54).  Before moving any geometry to satisfy a guard, three things have to
be established, and none of them is in 10.61:

  (1) WHICH member is at fault in each pair.  "gap_cargo x bay0 = 402.0 mm"
      names a pair, not a culprit.  A guard armed without knowing whether the
      door or the bay is wrong invites moving a LOCKED constant (the serving
      bays are locked EQUAL at 0.5155 m, band 1.372-1.775) to satisfy an
      unlocked one.

  (2) WHETHER the crossing is a physical impossibility or a harmless overlap.
      The founding assert (t1_shell:451) exists for ONE reason, stated in its
      own message: a shut line crossing an ARCH LIP collapsed the boolean at
      T1_SUB=2, 205562v -> 12v.  If these six crossings do not threaten that,
      the assert's stated rationale does not transfer and a different
      rationale has to be given explicitly rather than inherited.

  (3) WHICH FLANK each crossing is on.  The +Y show flank is photographed and
      locked.  The -Y flank is not in ANY of the three photographs -- SPEC
      itself records "whether the off flank carries glazing at all" as never
      established.  A guard that fires equally on both is asserting a fact
      about geometry nobody has ever seen.

Reports the anatomy of every crossing: extents, which edge of which outline is
involved, and the separation that would be needed to clear it.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_core as T
import t1_shell as S


def _inside(pt, poly):
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


def _bay_poly(i):
    cx, cz = S.bay_centre(i)
    return [(u + cx, v + cz) for (u, v) in S.bay_outline(i)]


def ext(poly, lbl):
    xs = [p[0] for p in poly]
    zs = [p[1] for p in poly]
    print("  %-12s x %+8.4f .. %+8.4f   z %+8.4f .. %+8.4f"
          % (lbl, min(xs), max(xs), min(zs), max(zs)))
    return min(xs), max(xs), min(zs), max(zs)


def anatomy(lname, line, aname, poly):
    """Describe the inside-run: where it is, and how far it must move."""
    pts = _densify(line)
    ins = [(p, w) for p, w in pts if _inside(p, poly)]
    if not ins:
        return None
    L = sum(w for _, w in ins)
    xs = [p[0] for p, _ in ins]
    zs = [p[1] for p, _ in ins]
    ax0, ax1 = min(q[0] for q in poly), max(q[0] for q in poly)
    az0, az1 = min(q[1] for q in poly), max(q[1] for q in poly)
    # how deep past each aperture edge does the run reach?
    dx_left = max(0.0, max(xs) - ax0)
    dx_right = max(0.0, ax1 - min(xs))
    dz_bot = max(0.0, max(zs) - az0)
    dz_top = max(0.0, az1 - min(zs))
    # the cheapest escape: smallest single-axis push that empties the aperture
    esc = min(dx_left, dx_right, dz_bot, dz_top)
    which = ["+x past aperture x0", "-x past aperture x1",
             "+z past aperture z0", "-z past aperture z1"][
        [dx_left, dx_right, dz_bot, dz_top].index(esc)]
    print("    %-11s x %-9s  %7.1f mm inside" % (lname, aname, L * 1000))
    print("       run occupies x %+.4f..%+.4f   z %+.4f..%+.4f"
          % (min(xs), max(xs), min(zs), max(zs)))
    print("       aperture      x %+.4f..%+.4f   z %+.4f..%+.4f"
          % (ax0, ax1, az0, az1))
    print("       penetration: dx_left %.1f  dx_right %.1f  dz_bot %.1f  "
          "dz_top %.1f mm" % (dx_left * 1000, dx_right * 1000,
                              dz_bot * 1000, dz_top * 1000))
    print("       cheapest clearance: %.1f mm (%s)" % (esc * 1000, which))
    return L


def main():
    print("=" * 78)
    print("CROSSING ANATOMY -- rev 23 probe, READ-ONLY. Nothing is modified.")
    print("=" * 78)
    print()
    print("--- OUTLINE EXTENTS (flank frame, x aft-positive-forward, z up) ---")
    ext(S.DOOR_GAP_S, "DOOR_GAP")
    ext(S.DOOR_MAIN_S, "DOOR_MAIN")
    ext(S.DOOR_VENT_S, "DOOR_VENT")
    ext(S.CARGO_GAP, "CARGO_GAP")
    for i in range(len(S.BAYS)):
        ext(_bay_poly(i), "bay%d" % i)
    print()
    print("  band from verify: Z_SILL..Z_HEAD = %.4f .. %.4f  (height %.1f mm)"
          % (S.Z_SILL, S.Z_HEAD, (S.Z_HEAD - S.Z_SILL) * 1000))
    print("  SHOW_SIDE = %+d   OPEN_BAYS = %s" % (S.SHOW_SIDE, S.OPEN_BAYS))
    print()

    apertures = [("door_main", S.DOOR_MAIN_S), ("door_vent", S.DOOR_VENT_S)]
    for i in range(len(S.BAYS)):
        apertures.append(("bay%d" % i, _bay_poly(i)))
    flank_lines = [("gap_door+1", S.DOOR_GAP_S, +1),
                   ("gap_door-1", S.DOOR_GAP_S, -1),
                   ("gap_cargo", S.CARGO_GAP, -1)]

    print("--- ANATOMY OF EACH CROSSING ---")
    show = 0.0
    off = 0.0
    for lname, line, side in flank_lines:
        for aname, poly in apertures:
            L = anatomy(lname, line, aname, poly)
            if L:
                if side == S.SHOW_SIDE:
                    show += L
                else:
                    off += L
                print()
    print("  SHOW flank (+%d, photographed): %.1f mm" % (S.SHOW_SIDE,
                                                         show * 1000))
    print("  OFF  flank (-1, in NO photograph): %.1f mm" % (off * 1000))
    print("  total %.1f mm" % ((show + off) * 1000))
    print()
    print("=" * 78)


if __name__ == "__main__":
    main()
