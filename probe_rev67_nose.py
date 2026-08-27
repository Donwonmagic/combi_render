# probe_rev67_nose.py -- rev 67.  THE NOSE'S SECTION.  F197.
#
# WHY THIS EXISTS.  The owner named the nose's SHAPE at rev 65 -- "we still have
# work to do on the shape of the nose" -- and at rev 66, asked directly whether
# rev 67 should do the nose or finish the emblem, he chose THE NOSE.  Rev 51 had
# already held the nose against the photographs and found A FLAT NOSE by eye,
# and it was never worked.  Nothing in this tree measured it.
#
# WHAT THE EXISTING NOSE PROBE DOES *NOT* DO.  `probe_rev59_nose.py` measures
# the height of the two-tone PAINT BREAK above the headlamp.  Its own header
# says, in terms:
#     "WHICH AXES IT DOES NOT SEE (rule 36).  It sees the nose in ELEVATION
#      only.  It cannot see anything about depth or plan curvature"
# so F197 is not an inference -- the instrument disclaims the axis itself.
#
# ---------------------------------------------------------------------------
# TWO THINGS THIS PROBE LEARNED THE HARD WAY, BOTH BY PAINTING (rule 8)
# ---------------------------------------------------------------------------
# (1) A SIDE ELEVATION CANNOT SEE PLAN CURVATURE AT ALL.  In an orthographic
#     side view the silhouette at height z is max-over-y of x(y,z).  For a nose
#     that is convex in plan that is ALWAYS the centreline, whether the plan
#     bulge is 0 mm or 100 mm.  The side view therefore reports the VERTICAL
#     section and is blind to the very axis `nose_shape()`'s bulge controls.
#
# (2) AND THE RED LEADING EDGE IN A SIDE VIEW IS NOT THE CENTRELINE.  At y = 0
#     the nose is CREAM down to the V-swage apex, so the forward-most RED pixel
#     at each height sits out at |y| = y_V(z), on the two-tone break -- not at
#     the nose's forward-most point.  A "nose section" segmented on red is the
#     silhouette of the PAINT REGION.  Rev 67 wrote that measurement, painted
#     it, then asked the mesh and found the two disagreed by a factor of seven.
#     The window is part of the measurement.
#
# SO THE PLAN BULGE IS MEASURED ON THE MESH, and the photograph is asked a
# question a projection CAN answer:
#
# THE STRAIGHTNESS TEST (projection-invariant).  A straight line in 3-D images
# as a straight line under ANY pinhole camera, at any pose.  So the SIGN of a
# projected curve's sagitta is pose-free: a bumper that images as a curve is a
# curve.  The MAGNITUDE is not pose-free and is NOT compared across frames --
# see the ceiling printed in the verdict.
#
# READ THIS PROBE'S OWN SUMMARY LINE, NEVER ITS EXIT CODE (rule 9).
import sys, os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.join(HERE, "probe_scratch")

# The two RED-BUS three-quarter frames.  ref_workshop.jpg is the GREEN vehicle
# and is excluded: geometry transfers, but we are reading a painted boundary
# (the bumper's cream against the body's red), so rule 11 bites.
# ref_playa_34.png IS CARRIED AND IS EXPECTED TO REFUSE.  Its bumper is in
# shadow and has no clean cream-over-red step, so the trace catches three
# unrelated fragments -- a scrap by the roundel, a scrap on the bumper's near
# end, and a run along the bumper's lower shadow -- and fits a parabola through
# all three.  PAINTED at probe_scratch/rev67_playa_bumper.png and LOOKED AT
# (rule 8); the fit's rms of 17.6 px on a 105 px span is the giveaway.  It is
# kept in the list rather than deleted so that "only one frame carries this"
# is a row this probe PRINTS, not a sentence someone has to remember.
PHOTOS = [("ref_nolita_front34.jpg", (128, 256), (300, 395)),
          ("ref_playa_34.png",       (15, 140),  (250, 345))]

# A fitted "edge" whose scatter exceeds this is not one edge but fragments.
# A SMOOTH boundary traced sub-pixel sits within a few PIXELS of a parabola
# however long it is, so a purely FRACTIONAL bar is too loose at long spans:
# rev 67 first wrote 12 % of span and watched a whole-frame column scan of a
# three-quarter render -- rms 61.85 px, catching the counter nosing and the
# tail board as well as the bumper -- sail through it at 7.4 %.  The absolute
# term is what refuses that.  WATCHED on all three inputs this revision:
#   ref_nolita_front34.jpg  rms  2.8 px over 118 px  -> one edge
#   ref_playa_34.png        rms 17.6 px over 105 px  -> fragments
#   out/r67_hero34r.png     rms 61.9 px over 831 px  -> fragments
def rms_bar(span):
    return max(4.0, 0.03 * span)


def _masks(a):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    red = (R - 0.5 * (G + B)) > 40
    sat = a.max(axis=2) - a.min(axis=2)
    lum = a.mean(axis=2)
    cream = (sat < 50) & (lum > 120)
    return red, cream


def bumper_top(path, ucol, vrow):
    """the cream bumper's top edge where it meets the red body, per column"""
    a = np.asarray(Image.open(path).convert("RGB")).astype(float)
    red, cream = _masks(a)
    edge = []
    for u in range(*ucol):
        for v in range(*vrow):
            if v < 2 or v + 5 >= a.shape[0]:
                continue
            if red[v - 2, u] and red[v - 1, u] and cream[v:v + 5, u].all():
                edge.append((u, v)); break
    return a, edge


def sagitta(edge):
    """fit v = a + b u + c u^2 ; sagitta = the parabola's max offset from its
    own chord.  Dimensionless when divided by the chord, and ZERO for any
    straight 3-D line under any projection."""
    if len(edge) < 25:
        return None
    u = np.array([e[0] for e in edge], float)
    v = np.array([e[1] for e in edge], float)
    c2, c1, c0 = np.polyfit(u, v, 2)
    du = u.max() - u.min()
    sag = c2 * du * du / 8.0
    rms = float(np.sqrt(np.mean((v - np.polyval([c2, c1, c0], u)) ** 2)))
    # standard error of the sagitta, from the fit's own residual scatter
    try:
        cov = np.polyfit(u, v, 2, cov=True)[1]
        se = float(np.sqrt(cov[0, 0]) * du * du / 8.0)
    except Exception:
        se = float("nan")
    return dict(n=len(edge), span=float(du), sag=float(sag),
                frac=float(sag / du), rms=rms, se=se)


def paint(a, edge, out):
    ov = a.copy()
    for u, v in edge:
        ov[max(0, v - 1):v + 2, u] = [0, 120, 255]
    os.makedirs(SCRATCH, exist_ok=True)
    Image.fromarray(ov.astype("uint8")).save(out)


# --------------------------------------------------------------- the mesh
def mesh_plan_bulge():
    """x(y=0) - x(|y|=0.70) on the built nose, at four heights above ground.

    THIS IS THE NUMBER NOTHING IN THIS TREE HAD EVER MEASURED.  It is what
    `t1_shell.nose_shape`'s  bulge = 0.019 * w * max(0, 1 - r)  produces.
    T1_NOSE_BULGE scales it and is the kill (measurement-only)."""
    import bpy  # noqa
    src = open(os.path.join(HERE, "build.py")).read()
    env = os.environ.copy()
    os.environ.pop("T1_PREVIEW", None)
    cwd = os.getcwd(); os.chdir(HERE)
    try:
        exec(compile(src, "build.py", "exec"),
             {"__name__": "__main__", "__file__": "build.py"})
    finally:
        os.chdir(cwd); os.environ.clear(); os.environ.update(env)
    ob = bpy.data.objects.get("T1_body")
    if ob is None:
        return None
    mw = ob.matrix_world
    co = np.array([tuple(mw @ v.co) for v in ob.data.vertices])
    nose = co[co[:, 0] > 1.95]
    out = {}
    for z0 in (1.10, 0.95, 0.80, 0.65):
        m = np.abs(nose[:, 2] - z0) < 0.02
        s = nose[m]
        if len(s) < 20:
            continue

        def at(t):
            k = np.abs(s[:, 1] - t) < 0.03
            return float(s[k][:, 0].max()) if k.sum() else float("nan")
        out[z0] = 1000.0 * (at(0.0) - at(0.70))
    return out


def main():
    argv = [a for a in sys.argv[1:] if not a.startswith("-")]
    want_mesh = "--nomesh" not in sys.argv
    frame = argv[0] if argv else None

    checks, fails = [], []

    def ck(name, ok, detail):
        checks.append((name, ok, detail))
        if not ok:
            fails.append(name)

    # -------------------------------------------------- the photographs
    photo = {}
    for path, ucol, vrow in PHOTOS:
        p = os.path.join(HERE, path)
        if not os.path.exists(p):
            continue
        a, edge = bumper_top(p, ucol, vrow)
        s = sagitta(edge)
        photo[path] = s
        if edge:
            paint(a, edge, os.path.join(
                SCRATCH, "rev67_bumper_%s.png" % path.split(".")[0]))

    def clean(v):
        return bool(v) and v["rms"] <= rms_bar(v["span"])

    ok_named = [k for k, v in photo.items() if clean(v)]
    ck("P1 the photographed bumper's top edge is traceable AS ONE EDGE  "
       "[PAINTED to probe_scratch/rev67_bumper_*.png BEFORE any number below "
       "was read -- rule 8].  A fit whose scatter exceeds max(4 px, 3 % of "
       "span) is fragments, not an edge, and REFUSES rather than reporting a "
       "number (rule 37)",
       len(ok_named) >= 1,
       "; ".join("%s n=%d span=%.0f rms=%.1f px -> %s"
                 % (k, v["n"], v["span"], v["rms"],
                    "USED" if clean(v) else "REFUSED, not one edge")
                 for k, v in photo.items() if v)
       + "".join("; %s NO TRACE" % k for k, v in photo.items() if not v))

    for k, v in photo.items():
        if not clean(v):
            continue
        ck("P2 %s: the bumper's top edge is CURVED, not straight -- a straight "
           "3-D line images straight under ANY pinhole camera, so a sagitta "
           "many times its own standard error is SHAPE, not pose" % k,
           abs(v["sag"]) > 3.0 * v["se"] if v["se"] == v["se"] else False,
           "sagitta %+.2f px +- %.2f (%.1f sigma) over a %.0f px chord "
           "= %+.4f of chord; fit rms %.2f px"
           % (v["sag"], v["se"], abs(v["sag"]) / v["se"] if v["se"] else 0,
              v["span"], v["frac"], v["rms"]))

    # -------------------------------------------------- the render
    ren = None
    if frame and os.path.exists(frame):
        aa = np.asarray(Image.open(frame).convert("RGB")).astype(float)
        red, cream = _masks(aa)
        # find the bumper band: the widest run of columns whose topmost
        # cream-under-red transition sits in the lower half of the body
        edge = []
        for u in range(aa.shape[1]):
            for v in range(int(aa.shape[0] * 0.45), aa.shape[0] - 6):
                if red[v - 2, u] and red[v - 1, u] and cream[v:v + 5, u].all():
                    edge.append((u, v)); break
        ren = sagitta(edge)
        if edge:
            paint(aa, edge, os.path.join(SCRATCH, "rev67_bumper_render.png"))
    elif frame:
        print("NO RENDER -- %s does not exist.  out/ is untracked and starts "
              "EMPTY on a clone.  Nothing was measured." % frame)
        return 2

    if ren:
        # THE SAME GATE AS P1, AND ON A THREE-QUARTER RENDER IT REFUSES.  A
        # whole-frame column scan catches EVERY cream-under-red boundary in the
        # frame -- the counter's nosing, the tail board, the roof shoulder --
        # not the bumper alone, and fits one parabola through the lot.  Rev 67
        # watched it report sagitta +54.35 px with an rms of 61.85 px on an
        # 831 px span and did NOT publish it.  Aiming this at the render's own
        # bumper needs a nose-column window the render does not hand over, and
        # the ceiling below says the magnitude would not be comparable anyway.
        ck("P3 the RENDER's bumper top edge is traceable AS ONE EDGE by the "
           "same rule P1 uses -- and on a three-quarter frame it is NOT",
           ren["rms"] <= rms_bar(ren["span"]),
           "sagitta %+.2f px +- %.2f over %.0f px = %+.4f of chord, fit rms "
           "%.2f px = %.0f %% of span -> %s.  MAGNITUDES ARE NOT COMPARABLE "
           "ACROSS POSES (rule 43) in any case -- only the sign and the "
           "presence of curvature are"
           % (ren["sag"], ren["se"], ren["span"], ren["frac"], ren["rms"],
              100 * ren["rms"] / ren["span"],
              "one edge" if ren["rms"] <= rms_bar(ren["span"])
              else "REFUSED, fragments"))

    # -------------------------------------------------- the mesh
    bulge = None
    if want_mesh:
        try:
            bulge = mesh_plan_bulge()
        except Exception as e:                       # rule 37 -- say so
            print("NO MESH -- could not build (%s: %s).  Nothing was measured "
                  "on the mesh." % (type(e).__name__, e))
            bulge = None

    if bulge:
        vals = [v for v in bulge.values() if v == v]
        ck("M1 THE NOSE'S PLAN BULGE IS MEASURED ON THE MESH -- x(y=0) minus "
           "x(|y|=0.70), the forward convexity NO side elevation can see and "
           "NOTHING in this tree had ever measured",
           len(vals) >= 3,
           "  ".join("z=%.2f %+.1f mm" % (z, b)
                     for z, b in sorted(bulge.items())))

        # THE BARE SHELL'S OWN CONVEXITY, WATCHED PRINTING at rev 67 with
        # T1_NOSE_BULGE driven to ~0:  +6.2 / +6.2 / +6.2 / +2.4 mm.
        # SHIPPED, watched in the same session:  +19.6 / +19.6 / +20.0 / +16.3.
        # SHELL_FLOOR sits between them, so it is NOT derived from the
        # expression it checks (rule 6): one side is the loft, the other is the
        # loft PLUS nose_shape()'s constant, and the bar separates them.
        SHELL_FLOOR = 12.0
        worst = max(vals)
        ck("M2 KILL -- nose_shape()'s bulge ACTUALLY REACHES THE MESH.  With "
           "T1_NOSE_BULGE driven to 0 the same measurement reads +6.2 mm (the "
           "lofted shell's own convexity, WATCHED FIRING at rev 67), so this "
           "row goes RED on an ablated nose.  NOT A FIDELITY CLAIM -- see the "
           "ceiling below",
           worst > SHELL_FLOOR,
           "worst plan bulge %.1f mm against a floor of %.1f mm.  The shipped "
           "constant is t1_shell.NOSE_BULGE; %.1f mm of the %.1f is the "
           "constant and the rest is the loft"
           % (worst, SHELL_FLOOR, worst - 6.2, worst))

    print("=" * 78)
    print("  probe_rev67_nose -- THE NOSE'S SECTION (F197)")
    print("=" * 78)
    for name, ok, detail in checks:
        print("  %-4s %s" % ("PASS" if ok else "FAIL", name))
        print("       %s" % detail)
    print("-" * 78)
    print("  CEILING, STATED (rule 12).  The plan bulge above is the MODEL's,")
    print("  measured exactly on its own mesh.  The photograph side is a")
    print("  STRAIGHTNESS test only: it establishes that the real bumper -- and")
    print("  so the nose it follows -- IS curved in plan, which is a sign, not")
    print("  a millimetre.  Converting a projected sagitta to a plan bulge")
    print("  needs the camera, and F26's camera ambiguity is unresolved.  THE")
    print("  REAL BUS's PLAN BULGE IN MILLIMETRES CANNOT BE RECOVERED FROM WHAT")
    print("  WE HOLD BY THIS ROUTE.  That is a result, not a gap.")
    print("-" * 78)
    print("  %d checked, %d FAILED%s"
          % (len(checks), len(fails),
             ("  --  " + "; ".join(fails)) if fails else ""))
    print("=" * 78)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
