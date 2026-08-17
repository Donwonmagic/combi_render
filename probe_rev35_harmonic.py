#!/usr/bin/env python3
"""
probe_rev35_harmonic.py  --  rev 35.  READ-ONLY.  No bpy.

GRADES THE TRANSVERSE-VP-BY-HARMONIC-CONJUGATE ROUTE, which SPEC 10.88.6
carries forward as "UNPUBLISHED, not refuted -- and with the cross-ratio
retired it is now the only unspent construction on this panel."

It is graded BEFORE a question is spent on it, and EVERY column it consumes is
graded, not the one under argument.  That ordering is SPEC 10.88.1's; the
reason it exists is SPEC 10.87.5, where three questions went into the wrong
term because the term that mattered had never been graded.

WHAT THE ROUTE IS.  The two headlamp centres are a pair symmetric about the
vehicle's centreline.  On the LINE joining them, the images of the two lamps
A, B and of their MIDPOINT M fix that line's vanishing point V as the harmonic
conjugate: (A, B; M, V) = -1.  A transverse VP is shared by every lateral line
on the vehicle whatever its height or depth, so V transfers into the bumper
plane WITHOUT the vehicle's yaw -- which is what killed rev 31's ARM 1.  With V
and the bar's two ends, the post's position along the bar falls out as a
scale-free fraction t of the bar's half-width, and SPEC 10.83's open claim
"the post is at the vehicle's centreline" becomes the statement t = 0.

  t = -1 at the bar's far end, 0 at its 3-D MIDPOINT, +1 at its near end.

CONTROLS
  H1  POSITIVE   the harmonic algebra is EXACT given the true midpoint
  H2  POSITIVE   the transverse VP really is shared across lateral lines at
                 different heights and depths -- the property the route rests on
  H3  KILL       THE ROUTE'S THIRD INPUT IS NOT OBSERVED.  There is no image of
                 M anywhere.  SPEC 10.86 substitutes the V-SWAGE APEX column,
                 which is a centreline point 0.625 m LOWER, at an unrecorded
                 depth, on a panel REF Sec 9 says is not planar.  Show what M's
                 column is actually constrained to, given everything known.
  H4  PRECOND    ordering and wall margins on every consumed column
  H5  PROVENANCE every consumed column must have a recorded derivation.
                 SPEC 10.88.4: "u 228 was never a measurement, which is the
                 whole complaint."
  G1..G6  LIVE per-column grading of the ROUTE, reported in the units of the
          QUANTITY (bar half-widths), NEVER in px.  SPEC 10.88's K4.
  B1..B5  WHAT SURVIVES WITHOUT THE ROUTE -- and, since rev 35's own
          adversarial audit, WHAT DOES NOT.
          B1  the SIGN of t, which is the substantive claim
          B2  KILL: the cross-ratio's COLLINEARITY precondition, which the
              build's own hoop constants VIOLATE.  This is why B1's magnitudes
              are WITHDRAWN.
          B3  KILL: the bound is NOT camera-free.  It assumes zero roll and
              zero post standoff, and rev 35 published it as consuming
              "no camera model".  That was wrong.
          B4  the margins, printed in px of post column, so the reader can see
              how little they are
          B5  scope: what the sign does and does not say
  N1, N2  NEGATIVE arms; the answer must move.

  THE RULE REV 35 EARNED BY GETTING THIS WRONG:
    CHECKING THE PRECONDITION YOU WERE WARNED ABOUT IS NOT CHECKING THE
    PRECONDITIONS.  SPEC 10.88.4 retired the cross-ratio on its ORDERING
    precondition, so H4 below checks ordering.  The cross-ratio has ANOTHER
    precondition -- collinearity -- and rev 35 did not check it until an
    adversarial audit did.  Inheriting one precondition from a previous
    revision's failure tells you nothing about the others.  Enumerate what
    the construction REQUIRES, not what last revision found.

THIS FILE REFUSES TO PRINT A RULING IF A POSITIVE CONTROL IS DOWN.
SPEC 10.88.5's rule; both rev-34 probes do the same.
"""

import math
import sys

try:
    import numpy as np
except Exception as e:                                    # pragma: no cover
    print("probe_rev35_harmonic: needs numpy:", e)
    sys.exit(2)


# ------------------------------------------------------- OBSERVED COLUMNS
# Every one carries its provenance.  H5 checks the string is not empty.
OBS = {
    "u_lamp_near": (419.0, "REF_MEASUREMENTS.md Sec 9: 'headlamp aperture "
                           "centre (419, 629)'; a second independent read in "
                           "the same file gives (418, 630)"),
    "u_lamp_far":  (236.0, ""),          # <-- deliberately empty.  See H5.
    "u_apex":      (288.8, "SPEC 10.85 / rev 31b, probe_v_apex.py: both V arms "
                           "traced and intersected, u = 288.8 +- 3 px "
                           "SYSTEMATIC (worst case 7)"),
    "u_bar_far":   (205.0, "SPEC 10.87.5 / 10.88.3, OWNER-ANSWERED TWICE: Q1 "
                           "candidate line 1 at u 205; Q1b 'at B1 or left of "
                           "it'.  Interval closed on both sides: u in (205,208]"),
    "u_bar_near":  (485.0, "SPEC 10.86 C3: hoop outer column 485.0, moving "
                           "0.0 px over a five-threshold sweep"),
    "u_post":      (365.5, "SPEC 10.86 C3: post u 355.0-376.0, centre 365.5, "
                           "right edge moving 0.5 px over five thresholds"),
}

# Per-column bands, each in the units of ITS OWN column, each with a source.
BANDS = {
    "u_lamp_near": 1.0,    # two independent reads, 418 and 419
    "u_lamp_far":  8.0,    # SEE H5.  THERE IS NO PUBLISHED BAND.  This is the
                           # probe's OWN conservative stand-in and is labelled
                           # as such every time it is used.
    "u_apex":      3.0,    # SPEC 10.85's SYSTEMATIC band
    "u_bar_far":   1.5,    # the owner's interval (205, 208] is 3 px wide
    "u_bar_near":  0.5,    # C3: 0.0 px over five thresholds, rounded up
    "u_post":      0.5,    # C3: 0.5 px over five thresholds
}

# The post's own FULL column extent, not its centre.  Used by B3.
POST_LEFT, POST_RIGHT = 355.0, 376.0

# 3-D anchors, read off the build's own constants, not retyped from prose:
#   t1_detail.py:346  D.place(o, loc=(2.1015, s * 0.5450, 1.0300))
#   t1_shell.py:1068  V_APEX_Z = 0.4050
HL_Z, V_APEX_Z = 1.0300, 0.4050

TOL_T = 0.05          # the KILL level on t, in bar half-widths


# ======================================================= HARMONIC ALGEBRA
def harmonic_conjugate(a, b, m):
    """V with (a, b; m, V) = -1.  Closed form.  None if V is at infinity."""
    den = (a + b - 2.0 * m)
    if abs(den) < 1e-12:
        return None
    return (2.0 * a * b - m * (a + b)) / den


def midpoint_from_vp(a, b, v):
    """Inverse of the above: the image of the 3-D midpoint, given the VP."""
    den = (a + b - 2.0 * v)
    if abs(den) < 1e-12:
        return None
    return (2.0 * a * b - v * (a + b)) / den


def t_along_bar(u_far, u_near, u_pt, vp):
    """u_pt's position along the bar in units of the bar's HALF-width.

    From the cross-ratio (far, near; pt, VP), the VP being the image of the
    bar's point at infinity.  t = -1 far end, 0 midpoint, +1 near end.
    """
    if vp is None:
        return None
    da, db = (u_far - u_pt), (u_near - u_pt)
    va, vb = (u_far - vp), (u_near - vp)
    if abs(db) < 1e-12 or abs(va) < 1e-12:
        return None
    r = (da / db) * (vb / va)                 # = (-1 - t) / (1 - t)
    if abs(r - 1.0) < 1e-12:
        return None
    return (1.0 + r) / (r - 1.0)


def route(c):
    """The published route, end to end.  Returns t or None."""
    vp = harmonic_conjugate(c["u_lamp_far"], c["u_lamp_near"], c["u_apex"])
    return t_along_bar(c["u_bar_far"], c["u_bar_near"], c["u_post"], vp)


def swing(fn, base, key, deltas):
    """Spread of the OUTPUT over +-delta on ONE input.

    Returns None if ANY sample is unreachable.  SPEC 10.88.5: a silently
    dropped sample is not a smaller error, it is a MISSING one.
    """
    vals = []
    for d in deltas:
        c = dict(base)
        c[key] = base[key] + d
        v = fn(c)
        if v is None or not math.isfinite(v):
            return None
        vals.append(v)
    return max(vals) - min(vals)


# ===================================================== SYNTHETIC POSITIVE
def synth_camera(az_deg=48.0, el_deg=17.0, dist=6.2, fpx=1500.0,
                 target=(2.0, 0.0, 0.85)):
    """A plausible pinhole with NO roll.  Used ONLY by H1 and H2, which are
    exactness checks on the algebra and are independent of whether this
    particular pose resembles ref_workshop.jpg."""
    az, el = math.radians(az_deg), math.radians(el_deg)
    tx, ty, tz = target
    C = np.array([tx + dist * math.cos(el) * math.cos(az),
                  ty + dist * math.cos(el) * math.sin(az),
                  tz + dist * math.sin(el)])
    fwd = np.array([tx, ty, tz]) - C
    fwd = fwd / np.linalg.norm(fwd)
    right = np.cross(fwd, np.array([0.0, 0.0, 1.0]))
    right = right / np.linalg.norm(right)
    down = np.cross(fwd, right)

    def pr(X):
        d = np.asarray(X, dtype=float) - C
        z = float(np.dot(fwd, d))
        return (600.0 + fpx * float(np.dot(right, d)) / z,
                412.0 + fpx * float(np.dot(down, d)) / z)
    pr.vp_lateral = 600.0 + fpx * float(np.dot(right, [0, 1, 0])) / \
        float(np.dot(fwd, [0, 1, 0]))
    return pr


# ==================================================================== MAIN
def main():
    results = []

    def rec(cid, ok, msg):
        results.append((cid, ok, msg))
        print("  %-4s %-4s %s" % (cid, "PASS" if ok else "FAIL", msg))

    cols = {k: v[0] for k, v in OBS.items()}
    print(__doc__.strip())

    # ------------------------------------------------------------------ H1
    print()
    print("=" * 74)
    print("H1  POSITIVE -- the harmonic algebra is EXACT given the TRUE")
    print("    midpoint.  If this fails, nothing below means anything.")
    print("=" * 74)
    pr = synth_camera()
    a = pr((2.10, -0.545, HL_Z))[0]
    b = pr((2.10, +0.545, HL_Z))[0]
    m = pr((2.10, 0.000, HL_Z))[0]
    vp_h = harmonic_conjugate(a, b, m)
    e1 = abs(vp_h - pr.vp_lateral)
    print("    lamps a %.4f  b %.4f  true midpoint m %.4f" % (a, b, m))
    rec("H1", e1 < 1e-6, "VP by harmonic conjugate %.9f vs analytic %.9f  "
                         "|err| %.2e px" % (vp_h, pr.vp_lateral, e1))

    # ------------------------------------------------------------------ H2
    print()
    print("=" * 74)
    print("H2  POSITIVE -- the transverse VP is SHARED by lateral lines at")
    print("    other heights and depths.  This is what lets V transfer into")
    print("    the bumper plane without the vehicle's yaw.")
    print("=" * 74)
    worst2 = 0.0
    for nm, (xx, zz, hy) in (("bar line", (2.1278, 0.6215, 0.600)),
                             ("belt line", (1.6000, 1.2070, 0.870)),
                             ("roof line", (0.5000, 1.9835, 0.800))):
        aa, bb = pr((xx, -hy, zz))[0], pr((xx, +hy, zz))[0]
        mm = pr((xx, 0.0, zz))[0]
        vv = harmonic_conjugate(aa, bb, mm)
        worst2 = max(worst2, abs(vv - pr.vp_lateral))
        print("    %-10s a %8.2f  b %8.2f  m %8.2f -> VP %11.5f  err %.2e"
              % (nm, aa, bb, mm, vv, abs(vv - pr.vp_lateral)))
    rec("H2", worst2 < 1e-6,
        "worst disagreement across three lateral lines %.2e px" % worst2)

    positives_ok = all(ok for cid, ok, _ in results if cid in ("H1", "H2"))

    # ------------------------------------------------------------------ H3
    print()
    print("=" * 74)
    print("H3  KILL -- THE ROUTE'S THIRD INPUT IS NOT OBSERVED.")
    print("=" * 74)
    print("    The route needs THREE columns on the headlamp line: the two")
    print("    lamps and their MIDPOINT.  Only two are observable.  There is")
    print("    no image of the midpoint anywhere in the frame, because there")
    print("    is no feature at the centre of the headlamp line.")
    print()
    print("    SPEC 10.86 supplies the third from the V-SWAGE APEX at u %.1f."
          % cols["u_apex"])
    print("    The apex is a centreline point %.3f m BELOW the headlamp line"
          % (HL_Z - V_APEX_Z))
    print("    (z %.4f against %.4f), at a depth recorded NOWHERE, on a panel"
          % (V_APEX_Z, HL_Z))
    print("    REF Sec 9 states is NOT PLANAR: 'I fitted a projection model")
    print("    and it did not close, which is itself evidence that the panel")
    print("    is not planar.'")
    print()
    print("    WHAT IS THE MIDPOINT'S COLUMN ACTUALLY CONSTRAINED TO?")
    print("    The VP of the bar must lie outside the segment [%.1f, %.1f]"
          % (cols["u_bar_far"], cols["u_bar_near"]))
    print("    and on the FAR side, because SPEC 10.86 C4 fixes the bar's")
    print("    near end as the high-u end.  So VP < %.1f.  Sweeping the VP"
          % cols["u_bar_far"])
    print("    across that whole admissible range and reading the midpoint")
    print("    of the LAMP line back out:")
    print()
    print("    %-14s %-14s %s" % ("VP", "lamp midpoint", "t (post)"))
    vp_grid = [-1e9, -5000.0, -1000.0, -300.0, -50.0, 0.0, 60.0, 111.0,
               150.0, 180.0, 200.0, 204.0]
    m_lo, m_hi, t_lo, t_hi = None, None, None, None
    unreachable = 0
    for v in vp_grid:
        mm = midpoint_from_vp(cols["u_lamp_far"], cols["u_lamp_near"], v)
        tt = t_along_bar(cols["u_bar_far"], cols["u_bar_near"],
                         cols["u_post"], v)
        if mm is None or tt is None:
            unreachable += 1
            print("    %-14s %-14s %s" % ("%.1f" % v, "UNREACHABLE", "-"))
            continue
        tag = "   <-- SPEC 10.86's published pair" if abs(v - 111.0) < 1e-9 \
            else ""
        print("    %-14.1f %-14.2f %.4f%s" % (v, mm, tt, tag))
        m_lo = mm if m_lo is None else min(m_lo, mm)
        m_hi = mm if m_hi is None else max(m_hi, mm)
        t_lo = tt if t_lo is None else min(t_lo, tt)
        t_hi = tt if t_hi is None else max(t_hi, tt)
    print()
    print("    THE LAMP MIDPOINT'S COLUMN IS FREE OVER %.1f px  [%.1f, %.1f]."
          % (m_hi - m_lo, m_lo, m_hi))
    print("    288.8 IS ONE CHOICE INSIDE THAT INTERVAL, NOT A READING OF IT.")
    print("    The corresponding t spans %.4f  [%.4f, %.4f] half-widths."
          % (t_hi - t_lo, t_lo, t_hi))
    rec("H3", (t_hi - t_lo) < TOL_T and unreachable == 0,
        "the unobserved third input leaves t free over %.4f half-widths "
        "(a KILL at %.2f)" % (t_hi - t_lo, TOL_T))

    # ------------------------------------------------------------------ H4
    print()
    print("=" * 74)
    print("H4  PRECONDITION -- ordering and WALL margins on every column.")
    print("=" * 74)
    ord_l = cols["u_lamp_far"] < cols["u_apex"] < cols["u_lamp_near"]
    m_far = cols["u_apex"] - cols["u_lamp_far"]
    m_near = cols["u_lamp_near"] - cols["u_apex"]
    print("    lamp ordering  far %.1f < mid %.1f < near %.1f : %s"
          % (cols["u_lamp_far"], cols["u_apex"], cols["u_lamp_near"],
             "holds" if ord_l else "BROKEN"))
    print("    margins to the wall %.1f px / %.1f px, against the far lamp's"
          % (m_far, m_near))
    print("    OWN STAND-IN band of +-%.1f px -> %.1fx and %.1fx."
          % (BANDS["u_lamp_far"], m_far / BANDS["u_lamp_far"],
             m_near / BANDS["u_lamp_far"]))
    print("    CONTRAST WITH THE RETIRED ROUTE: SPEC 10.88.4's strut sat")
    print("    1.5 px from its wall against a +-3.5 px residual -- 0.43x.")
    print("    THIS ROUTE DOES NOT FAIL THE WAY THE CROSS-RATIO FAILED.")
    bar_ord = cols["u_bar_far"] < cols["u_post"] < cols["u_bar_near"]
    print("    bar ordering   far %.1f < post %.1f < near %.1f : %s"
          % (cols["u_bar_far"], cols["u_post"], cols["u_bar_near"],
             "holds" if bar_ord else "BROKEN"))
    rec("H4", ord_l and bar_ord and m_far / BANDS["u_lamp_far"] > 3.0,
        "no consumed column sits against a precondition wall")

    # ------------------------------------------------------------------ H5
    print()
    print("=" * 74)
    print("H5  PROVENANCE -- every consumed column must have a recorded")
    print("    derivation.  SPEC 10.88.4: 'u 228 was never a measurement,")
    print("    which is the whole complaint.'")
    print("=" * 74)
    missing = []
    for k in ("u_lamp_far", "u_lamp_near", "u_apex", "u_bar_far",
              "u_bar_near", "u_post"):
        val, prov = OBS[k]
        print("    %-12s %8.1f   %s"
              % (k, val, "recorded" if prov.strip() else "*** NONE ***"))
        if prov.strip():
            print("                          %s" % prov)
        else:
            missing.append(k)
    print()
    print("    u_lamp_far = 236 appears in exactly two places in the whole")
    print("    tree -- SPEC 10.86's prose and HANDOFF_rev32.md -- and in")
    print("    NEITHER REF_MEASUREMENTS.md NOR ANY PROBE.  No derivation, no")
    print("    band, no threshold sweep, never asked about.")
    rec("H5", not missing, "columns with no recorded derivation: %s"
        % (", ".join(missing) if missing else "none"))

    # -------------------------------------------------------------- G1..G6
    print()
    print("=" * 74)
    print("G1..G6  LIVE PER-COLUMN GRADING OF THE ROUTE.  Reported in the")
    print("    units of the QUANTITY (bar half-widths), never in px.")
    print("    SPEC 10.88's K4: a tolerance stated in the units of the")
    print("    MEASUREMENT does not transfer between columns.")
    print("=" * 74)
    base = dict(cols)
    t_base = route(base)
    vp_base = harmonic_conjugate(base["u_lamp_far"], base["u_lamp_near"],
                                 base["u_apex"])
    print("    at the published columns: VP %.2f, t = %s half-widths"
          % (vp_base, "%.4f" % t_base if t_base is not None else "UNREACHABLE"))
    print("    (SPEC 10.86 published VP ~111 and a bumper-plane centreline")
    print("    ~266.  266 was computed with the far bar end at u ~209, which")
    print("    rev 33's and rev 34's owner answers have since REPLACED with")
    print("    u in (205, 208].  At u 205 the same construction gives %.1f."
          % midpoint_from_vp(base["u_bar_far"], base["u_bar_near"], vp_base))
    print("    The route's one published output is stale on an answered input.)")
    print()
    print("    %-13s %-10s %-12s %-12s %s"
          % ("column", "band px", "+-1 px", "+-band", "verdict"))
    g_rows = []
    for i, k in enumerate(("u_lamp_far", "u_lamp_near", "u_apex", "u_bar_far",
                           "u_bar_near", "u_post"), start=1):
        s1 = swing(route, base, k, (-1.0, 0.0, +1.0))
        sb = swing(route, base, k, (-BANDS[k], 0.0, +BANDS[k]))
        verdict = "UNREACHABLE" if sb is None else \
            ("DOMINANT" if sb > TOL_T else "ok")
        print("    %-13s %-10.1f %-12s %-12s %s"
              % (k, BANDS[k], "n/a" if s1 is None else "%.4f" % s1,
                 "n/a" if sb is None else "%.4f" % sb, verdict))
        g_rows.append((k, s1, sb))
        rec("G%d" % i, sb is not None and sb <= TOL_T,
            "%s: +-band moves t by %s"
            % (k, "n/a" if sb is None else "%.4f" % sb))
    print()
    print("    NOTE, and it is the K4 point: +-1 px buys %.4f half-widths on"
          % g_rows[0][1])
    print("    the far lamp and %.4f on the near one -- a factor of %.2f for"
          % (g_rows[1][1], g_rows[0][1] / g_rows[1][1]))
    print("    the SAME pixel move.  A px band does not transfer.")

    # -------------------------------------------------------------- B1..B3
    print()
    print("=" * 74)
    print("B1..B3  THE CAMERA-FREE BOUND -- what survives WITHOUT the route.")
    print("=" * 74)
    print("    The route above is dead on H3.  But t is not therefore")
    print("    unknown.  Sweeping the VP over its ENTIRE admissible range")
    print("    already bounded t away from 0 in the H3 table, and that bound")
    print("    consumes NO vanishing point, NO camera and NO symmetry")
    print("    assumption.  It uses only:")
    print("      (i)   the bar's two end columns,")
    print("      (ii)  the post's column,")
    print("      (iii) SPEC 10.86 C4's near/far assignment.")
    print()

    def t_bound(u_far, u_near, u_pt):
        """inf over all admissible VP (VP < u_far) of t."""
        lo = None
        for v in (-1e12, -1e9, -1e6, -1e4, -1e3, -300.0, -50.0, 0.0,
                  u_far - 100.0, u_far - 30.0, u_far - 5.0, u_far - 0.5):
            tt = t_along_bar(u_far, u_near, u_pt, v)
            if tt is None or not math.isfinite(tt):
                return None
            lo = tt if lo is None else min(lo, tt)
        return lo

    b_nom = t_bound(base["u_bar_far"], base["u_bar_near"], base["u_post"])
    print("    B1  THE SIGN.  At the published columns, the infimum over every")
    print("        admissible VP is t = %.4f > 0." % b_nom)
    print("        The orthographic limit (VP -> -infinity) is the infimum,")
    print("        and it is just the arithmetic statement that the post's")
    print("        column %.1f lies RIGHT of the bar's mid-column %.1f."
          % (base["u_post"], 0.5 * (base["u_bar_far"] + base["u_bar_near"])))
    print()
    print("        *** THE MAGNITUDE IS WITHDRAWN.  SEE B2 AND B3.  Only the")
    print("        *** SIGN of t is claimed.  rev 35 first published %.4f as"
          % b_nom)
    print("        *** a bound holding for EVERY admissible camera.  It does")
    print("        *** not, and its own probe now says so.")
    rec("B1", b_nom is not None and b_nom > 0.0,
        "SIGN ONLY: t > 0 at nominal columns (infimum %.4f, magnitude "
        "WITHDRAWN)" % b_nom)

    worst = None
    combo = None
    for df in (0.0, +3.0):                         # owner's interval (205,208]
        for dn in (-BANDS["u_bar_near"], +BANDS["u_bar_near"]):
            for up in (POST_LEFT, base["u_post"], POST_RIGHT):
                bb = t_bound(base["u_bar_far"] + df,
                             base["u_bar_near"] + dn, up)
                if bb is None:
                    worst = None
                    combo = (df, dn, up)
                    break
                if worst is None or bb < worst:
                    worst, combo = bb, (df, dn, up)
    print()
    print("        worst corner of every consumed band, INCLUDING the post's")
    print("        full column extent %.1f-%.1f rather than its centre:"
          % (POST_LEFT, POST_RIGHT))
    print("        far end %+.1f, near end %+.1f, post at %.1f -> t = %.4f"
          % (combo[0], combo[1], combo[2], worst))

    # ------------------------------------------------------------------ B2
    print()
    print("    B2  KILL -- THE COLLINEARITY PRECONDITION IS VIOLATED BY THE")
    print("        BUILD'S OWN CONSTANTS.  A cross-ratio requires its four")
    print("        points to be COLLINEAR in 3-D.  They are not.")
    dia = 0.024966
    drop, back = 2.6 * dia, 1.6 * dia
    print("        u %.1f is the HOOP's outer column.  t1_detail.py's arc,"
          % base["u_bar_near"])
    print("          x = BAR_X - BACK*(1-cos a),  z = BAR_Z - DROP*sin a,")
    print("          y = HALF_Y + 0.55*DROP*sin a,   BACK %.4f  DROP %.4f m,"
          % (back, drop))
    print("        carries the generating point up to %+.1f mm in x, %+.1f mm"
          % (-back * 1000, -drop * 1000))
    print("        in z and %+.1f mm in y off the straight axis end."
          % (0.55 * drop * 1000))
    print("        The audited generating point sits at -17.5 / -53.7 / +29.5 mm,")
    print("        INSIDE that range on all three axes.")
    print("        AND the post's column was read on rows 676-700 while the")
    print("        bar's top edge is at v 672.5 -- a DIFFERENT lateral line.")
    print("        FOUR POINTS, THREE LINES.")
    rec("B2", False,
        "collinearity VIOLATED: the audited generating point is 53.7 mm below "
        "and 17.5 mm behind the far reading's line (the arc reaches %.1f / "
        "%.1f mm)" % (drop * 1000, back * 1000))

    # ------------------------------------------------------------------ B3
    print()
    print("    B3  KILL -- THE BOUND IS NOT CAMERA-FREE, AND rev 35 PUBLISHED")
    print("        IT AS CONSUMING 'no camera model'.  Two hidden assumptions:")
    print("          (a) ZERO CAMERA ROLL.  The magnitude degrades at about")
    print("              0.00045 half-widths per degree over the pose grid and")
    print("              fails the first published figure beyond |roll| ~ 7 deg.")
    print("              Nothing in this repository establishes the roll --")
    print("              SPEC 10.86 says so itself, one section earlier, about")
    print("              a different arm: 'nothing in this repository")
    print("              establishes that' the camera is level and unrolled.")
    print("          (b) ZERO POST STANDOFF from the bar's plane.  Sensitivity")
    print("              238 px per metre; 60 mm rearward breaks the first")
    print("              published figure at the plausible pose.  t1_detail.py")
    print("              calls the standoff 'a CHOICE, not a reading'.")
    print("        THE SIGN survives to |roll| ~ 26 deg and ~139 mm of rearward")
    print("        standoff, both excluded on this frame.  THE MAGNITUDES DO NOT.")
    rec("B3", False,
        "the bound assumes zero roll and zero post standoff; only the SIGN "
        "survives")

    # ------------------------------------------------------------------ B4
    print()
    print("    B4  THE MARGINS, IN px OF POST COLUMN, so their size is visible.")
    du = 1.0
    dt = swing(lambda c: t_bound(c["u_bar_far"], c["u_bar_near"], c["u_post"]),
               base, "u_post", (-du, 0.0, +du))
    per_px = dt / (2 * du) if dt else float("nan")
    print("        d(t)/d(post column) = %.5f half-widths per px." % per_px)
    print("        nominal margin %.4f -> %.2f px of post column"
          % (b_nom, b_nom / per_px))
    print("        worst-corner    %.4f -> %.2f px of post column"
          % (worst, worst / per_px))
    print("        THAT IS NOT A BOUND, IT IS A COINCIDENCE WITH A NUMBER ON IT.")
    rec("B4", True, "margins printed in the units a reader can check")

    print()
    print("    B5  WHAT THE SIGN DOES AND DOES NOT SAY.")
    print("        SAYS: the post is on the NEAR side of the bar's 3-D")
    print("        MIDPOINT -- THE SIGN OF t AND NOTHING ELSE -- for every")
    print("        UNROLLED camera consistent with C4's near/far assignment")
    print("        and with the post standing in the bar's own plane.")
    print("        DOES NOT SAY: where the vehicle's centreline is.  'Post at")
    print("        the bar's midpoint' and 'post at the vehicle's centreline'")
    print("        are the same statement ONLY IF the bar is symmetric about")
    print("        the centreline, and SPEC 10.86 records that assumption's")
    print("        only check DISAGREEING AT 17 %.  The bar's own half-width")
    print("        constant BAR_HALF_Y is graded E, 'spans the nose as")
    print("        photographed, NOT measured'.")
    print("        AND, since the audit: it says NOTHING about the MAGNITUDE.")
    rec("B5", True, "the sign's scope is stated, not implied")

    # ------------------------------------------------------------- N1, N2
    print()
    print("=" * 74)
    print("N1, N2  NEGATIVE ARMS -- the answer must move.")
    print("=" * 74)
    bad = dict(base)
    bad["u_lamp_far"] = base["u_lamp_far"] + 40.0
    t_bad = route(bad)
    print("    N1  far lamp %.1f -> %.1f   t %.4f -> %s"
          % (base["u_lamp_far"], bad["u_lamp_far"], t_base,
             "%.4f" % t_bad if t_bad is not None else "unreachable"))
    rec("N1", t_bad is None or abs(t_bad - t_base) > TOL_T,
        "a 40 px corruption of the far lamp moves the route's answer")

    b_flip = t_bound(base["u_bar_far"], base["u_bar_near"], 300.0)
    print("    N2  post moved to u 300.0 (LEFT of the bar's mid-column %.1f):"
          % (0.5 * (base["u_bar_far"] + base["u_bar_near"])))
    print("        the sign estimate becomes t = %.4f" % b_flip)
    rec("N2", b_flip is not None and b_flip < 0.0,
        "the SIGN CHANGES when the post moves across the bar's mid-column -- "
        "it is reading the data, not asserting a sign")

    # ================================================================ RULING
    print()
    print("=" * 74)
    n_fail = sum(1 for _, ok, _ in results if not ok)
    print("CONTROLS: %d checked, %d FAILED" % (len(results), n_fail))
    print("=" * 74)
    if not positives_ok:
        print()
        print("  *** REFUSING TO PRINT A RULING: A POSITIVE CONTROL IS DOWN.")
        print("  H1 and H2 establish that the construction and the transfer")
        print("  are sound.  With either down every number above is unfounded")
        print("  and a ruling would be prose resting on nothing.")
        print("  SPEC 10.88.5's rule; both rev-34 probes do the same.")
        return 1

    dom = [k for k, s1, sb in g_rows if sb is None or sb > TOL_T]
    print()
    print("RULING -- derived from the table above, not asserted.")
    print()
    print("  1. THE ALGEBRA IS EXACT AND THE TRANSFER CLAIM HOLDS.")
    print("     H1 %.2e px, H2 %.2e px.  As with the cross-ratio, the algebra"
          % (e1, worst2))
    print("     was never the problem.")
    print()
    print("  2. THE ROUTE CANNOT CLOSE, AND NOT FOR WANT OF PRECISION.")
    print("     It consumes THREE columns on the headlamp line and only TWO")
    print("     exist.  The third is supplied by a feature %.3f m below that"
          % (HL_Z - V_APEX_Z))
    print("     line at an unrecorded depth.  Sweeping the VP over its whole")
    print("     admissible range leaves the midpoint free over %.1f px and t"
          % (m_hi - m_lo))
    print("     free over %.4f half-widths -- %.0fx the %.2f level."
          % (t_hi - t_lo, (t_hi - t_lo) / TOL_T, TOL_T))
    print("     THIS IS A PRECONDITION FAILURE, LIKE SPEC 10.88.4's, NOT A")
    print("     PRECISION SHORTFALL.  No further measurement on this frame")
    print("     repairs it, because what is missing is not accuracy but a")
    print("     FEATURE: there is nothing at the centre of the headlamp line.")
    print()
    print("  3. DOMINANT COLUMNS: %s." % (", ".join(dom) if dom else "none"))
    if missing:
        print("     AND %s HAS NO RECORDED DERIVATION ANYWHERE IN THE TREE"
              % ", ".join(m.upper() for m in missing))
        print("     -- same class as SPEC 10.88.4's u 228, found the same way.")
    print()
    print("  4. WHAT SURVIVES -- THE SIGN, AND ONLY THE SIGN.")
    print("     THE POST IS ON THE NEAR SIDE OF THE BAR'S 3-D MIDPOINT.")
    print("     It consumes no VP and no symmetry assumption, but B2 and B3")
    print("     show it DOES consume a collinearity that the build's own hoop")
    print("     constants violate, an UNROLLED camera, and a post standing in")
    print("     the bar's plane.  The sign survives all three to |roll| ~ 26")
    print("     deg and ~139 mm of standoff; the MAGNITUDES DO NOT SURVIVE AT")
    print("     ALL and are WITHDRAWN.  rev 35 published %.4f and %.4f as"
          % (b_nom, worst))
    print("     holding 'for every admissible camera'.  That was wrong, it was")
    print("     found by an adversarial audit of rev 35's own probe, and the")
    print("     figures are struck rather than quietly re-scoped.")
    print("     Whether that refutes SPEC 10.83 depends on the bar being")
    print("     symmetric about the vehicle's centreline, which is ASSUMED")
    print("     and whose only check disagrees at 17 %.  Stated, not buried.")
    print()
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
