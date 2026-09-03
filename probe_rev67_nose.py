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


def exif_focal(path):
    """The frame's OWN focal length, in PIXELS, from its EXIF.

    ------------------------------------------------------------------ F219
    NOTHING IN THIS TREE HAD EVER READ EXIF -- `grep -rniE
    "getexif|_getexif|exifread|piexif|ExifTags"` over every .py and .sh
    returned ZERO -- and the record published the OPPOSITE for five
    revisions: `SURVEY_rev49_photoreal.md` says "the focal length of a camera
    nobody recorded" and "no focal length, no camera distance, no px/m".

    TWO of the seven target-bus frames carry their own intrinsics:
        ref_nolita_front34.jpg   SONY DSC-RX100  f 10.4 mm, 35mm-equiv 28,
                                 700x467 = 3:2 UNCROPPED, zoom ratio 1.0
        ref_nolita_doorshut.jpg  Canon EOS 5D Mark II  f 24.0 mm, 480x320
    Returns None when the frame carries nothing, which is the honest answer
    for the other five.
    """
    try:
        from PIL import ExifTags
        im = Image.open(path)
        ex = im.getexif()
        d = {ExifTags.TAGS.get(k, k): v for k, v in ex.items()}
        try:
            d.update({ExifTags.TAGS.get(k, k): v
                      for k, v in ex.get_ifd(0x8769).items()})
        except Exception:
            pass
        w = im.size[0]
        f35 = d.get("FocalLengthIn35mmFilm")
        if f35:
            return float(f35) / 36.0 * w, d.get("Model", "?"), float(f35)
    except Exception:
        pass
    return None


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


def sagitta(edge, clip=8.0):
    """fit v = a + b u + c u^2 ; sagitta = the parabola's max offset from its
    own chord.  Dimensionless when divided by the chord, and ZERO for any
    straight 3-D line under any projection.

    ------------------------------------------------------------------ F220
    ONE PASS OF OUTLIER REJECTION, AND IT IS NOT COSMETIC.  Rev 67 published
    "-2.94 px +- 0.46 over a 118 px chord, 6.4 sigma" from this function and
    THREE of its 106 points were ON A CHILD'S HAIR -- residuals -16.7, -16.1,
    -13.6 px, RGB (205,165,157), (204,172,161), (193,166,149).  Dropping them
    moves the headline 43 % and its stated error 5.1x:
        as published  -2.94 +- 0.46  rms 2.78   6.4 sigma
        cleaned       -2.05 +- 0.09  rms 0.55  21.9 sigma
    AND RULE 48's BAR, WRITTEN THIS SAME REVISION TO REFUSE EXACTLY THIS,
    PASSED IT: max(4 px, 3 % of 118) = 4.00 against an rms of 2.78.  A bar
    that cannot refuse contamination worth 43 % of the answer is not a bar
    (rule 3).  `n_clipped` is REPORTED so the rejection can never be silent.
    """
    if len(edge) < 25:
        return None
    u = np.array([e[0] for e in edge], float)
    v = np.array([e[1] for e in edge], float)
    c2, c1, c0 = np.polyfit(u, v, 2)
    n0, span0 = len(u), float(u.max() - u.min())
    keep = np.abs(v - np.polyval([c2, c1, c0], u)) < clip
    n_clipped = int((~keep).sum())
    if keep.sum() >= 25 and n_clipped:
        u, v = u[keep], v[keep]
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
    # ---------------------------------------------------------------- F220b
    # AND THE REJECTION PASS MUST NOT BE ABLE TO RESCUE A FRAGMENT TRACE.
    # Watched immediately after F220's clip was added: `ref_playa_34.png`, whose
    # refusal is CORRECT and was confirmed independently, went from rms 17.6 to
    # rms 0.2 and PASSED -- the clip had eaten the fragments and fitted a clean
    # parabola to one surviving scrap, with the span collapsing 105 -> 51 px.
    # A rejection that turns a right refusal into a wrong pass is worse than no
    # rejection at all.  So the ORIGINAL n and span are what the caller judges.
    rescued = (n_clipped > 0.10 * n0) or (du < 0.70 * span0)
    return dict(n=int(len(u)), n0=n0, n_clipped=n_clipped, span=float(du),
                span0=span0, rescued=bool(rescued),
                sag=float(sag), frac=float(sag / du), rms=rms, se=se)


def paint(a, edge, out):
    ov = a.copy()
    for u, v in edge:
        ov[max(0, v - 1):v + 2, u] = [0, 120, 255]
    os.makedirs(SCRATCH, exist_ok=True)
    Image.fromarray(ov.astype("uint8")).save(out)


# --------------------------------------------------------------- the mesh
# ============================================================ rev 73, F284
# THE BUILD, ONCE, SHARED BY THE MESH ROW AND P3's WINDOW.
#
# Before rev 73 the build lived inside mesh_plan_bulge().  P3's window is
# projected through the SAME build, so the two rows cannot disagree about
# which vehicle they are describing.
_BPY = None


def _build_scene():
    """exec build.py once in this process; return the bpy module.

    T1_RIG=1 is what build.py's own `_want_rig` reads when T1_PREVIEW is
    absent.  WITHOUT IT THERE IS NO CAMERA IN THE SCENE and no window can be
    projected -- build.py's line is
        _want_rig = (os.environ.get("T1_PREVIEW") or os.environ.get("T1_RIG"))
    """
    global _BPY
    if _BPY is not None:
        return _BPY
    import bpy  # noqa
    src = open(os.path.join(HERE, "build.py")).read()
    env = os.environ.copy()
    os.environ.pop("T1_PREVIEW", None)
    os.environ["T1_RIG"] = "1"
    cwd = os.getcwd(); os.chdir(HERE)
    try:
        exec(compile(src, "build.py", "exec"),
             {"__name__": "__main__", "__file__": "build.py"})
    finally:
        os.chdir(cwd); os.environ.clear(); os.environ.update(env)
    _BPY = bpy
    return bpy


# The objects the window is cut from.  NOT the bumper, and NOT the body.
#   hl_ring / ind*_lens -- the nose FIXTURES.  build.py stands them at FIXED
#     lateral stations (`HL_Y = 0.5450`, `IND_Y = HL_Y + IND_DY`) and only
#     their X follows the skin (`HL_X = HL_X0 + S.nose_fixture_dx(...)`).
#   tyre -- the ground line.
_FIX_PREFIX = ("hl_ring", "ind1_lens", "ind-1_lens")
_GROUND_PREFIX = ("tyre",)


def _obs(bpy, base):
    """every MESH whose name starts with `base`.

    NOT `base` + "." -- rev 73 wrote that first and found 4 fixtures and ZERO
    tyres, because the road wheels are named `tyre1.31` / `tyre-1.1-1`, not
    `tyre.001`.  The probe REFUSED rather than measuring on a half-built
    window (rule 37), which is how the naming was caught.  `wheel_rim`,
    `wheel_hub`, `wheel_spoke*` are the STEERING wheel and are not matched."""
    return [o for o in bpy.data.objects
            if o.type == "MESH" and o.name.startswith(base)]


def _project(bpy, sc, cam, obs, rx, ry):
    from bpy_extras.object_utils import world_to_camera_view
    uv = []
    for o in obs:
        mw = o.matrix_world
        for v in o.data.vertices:
            c = world_to_camera_view(sc, cam, mw @ v.co)
            uv.append((c.x * rx, (1.0 - c.y) * ry))
    return np.array(uv, float)


def fixture_window(rx, ry):
    """(ucol, vrow) for the FRONT elevation, projected from the nose FIXTURES
    and the TYRES -- never from the bumper.

    ------------------------------------------------------------ RULE 6, F284
    THE QUANTITY P3 MEASURES IS A CURVATURE -- the sagitta of the rendered
    cream-under-red boundary.  Nothing this function reads can express one.
    `front` is ORTHOGRAPHIC down the X axis (studio.views()["front"] is
    `loc=(26.0, 0.0, 1.52), tgt=(0.0, 0.0, 1.52), ortho=3.55`), so a point's
    column is a function of y alone and its row of z alone, and X -- the axis
    the ENTIRE plan bow lives on -- does not reach the image at all.
    That is not an argument, it is `win["xblind"]`: the same vertex is
    projected again displaced 100 mm in X and the two pixels are compared.
    P3w prints the disagreement and REFUSES if it is not zero.

    ------------------------------------------------------------ RULE 8, F284
    The window is PAINTED, with the points it selected, BEFORE any number is
    read from it -- probe_scratch/rev73_bumper_window.png.
    """
    bpy = _build_scene()
    sc = bpy.context.scene
    cam = sc.camera
    if cam is None:
        return None, "NO CAMERA in the built scene (T1_RIG did not take)"
    import studio as ST
    V = ST.views()["front"]
    ST.aim(cam, V["loc"], V["tgt"], V.get("lens"), V.get("ortho"),
           V.get("focus"), V.get("fstop"))
    sc.render.resolution_x, sc.render.resolution_y = int(rx), int(ry)
    sc.render.resolution_percentage = 100
    # ---------------------------------------------------------------- rev 73
    # aim() writes cam.location and cam.rotation_euler.  matrix_world is
    # DERIVED and is not recomputed until the depsgraph runs, so without this
    # line world_to_camera_view projects through the camera's PREVIOUS pose.
    # Watched at rev 73: the four nose fixtures came back at u 1745 on a
    # 1600 px frame -- off the side of the image -- and the paint call raised
    # IndexError.  It raised; it did not report a number.  The scale control
    # below is what makes that a MEASUREMENT rather than a lucky crash.
    bpy.context.view_layer.update()
    if cam.data.type != "ORTHO":
        return None, ("the front camera is %s, not ORTHO -- this window's "
                      "whole rule-6 argument is the orthographic X-blindness"
                      % cam.data.type)

    # --- THE SCALE CONTROL.  Two points whose pixels are known from the view
    # table alone, checked BEFORE anything is read off the projection.  The
    # centreline must land mid-frame and the ortho half-width at the edge.
    # This is what refuses a stale camera matrix, a wrong sensor_fit or a
    # resolution set after the fact -- none of which announce themselves.
    import mathutils
    from bpy_extras.object_utils import world_to_camera_view as _w2c
    zc = float(V["tgt"][2])
    o_scale = float(V["ortho"])
    c_mid = _w2c(sc, cam, mathutils.Vector((0.0, 0.0, zc)))
    c_edge = _w2c(sc, cam, mathutils.Vector((0.0, o_scale / 2.0, zc)))
    u_mid, u_edge = c_mid.x * rx, c_edge.x * rx
    scale_err = max(abs(u_mid - rx / 2.0), min(abs(u_edge), abs(u_edge - rx)))
    if not (scale_err < 1.0):
        return None, ("the front projection FAILS its own scale control -- "
                      "y=0 lands at u %.1f (want %.1f) and y=%.3f at u %.1f "
                      "(want 0 or %d), err %.1f px.  Nothing was measured."
                      % (u_mid, rx / 2.0, o_scale / 2.0, u_edge, int(rx),
                         scale_err))

    fix, ground = [], []
    for b in _FIX_PREFIX:
        fix += _obs(bpy, b)
    for b in _GROUND_PREFIX:
        ground += _obs(bpy, b)
    if len(fix) < 4 or len(ground) < 4:
        return None, ("expected 4 nose fixtures and 4 tyres, found %d and %d "
                      "-- the window's anchors are not in this build"
                      % (len(fix), len(ground)))

    pf = _project(bpy, sc, cam, fix, rx, ry)
    pg = _project(bpy, sc, cam, ground, rx, ry)

    # --- the rule-6 proof, RUN rather than asserted -------------------------
    from bpy_extras.object_utils import world_to_camera_view
    import mathutils
    o = fix[0]
    w0 = o.matrix_world @ o.data.vertices[0].co
    c0 = world_to_camera_view(sc, cam, w0)
    c1 = world_to_camera_view(sc, cam, w0 + mathutils.Vector((0.100, 0.0, 0.0)))
    xblind = max(abs(c0.x - c1.x) * rx, abs(c0.y - c1.y) * ry)

    u0, u1 = float(pf[:, 0].min()), float(pf[:, 0].max())
    v0 = float(pf[:, 1].max())            # the LOWEST fixture pixel
    v1 = float(pg[:, 1].max())            # the ground line, off the tyres
    # ---------------------------------------------------------------- rev 73
    # THE WINDOW IS THE PROJECTED BAND *INTERSECTED WITH THE FRAME*, and the
    # clamping is REPORTED, never silent.  Measured at rev 73: the tyres'
    # ground line projects to v 1235 on a 1100 px frame -- `front` is
    # ortho 3.55 across 1600 px, so it spans 2.441 m of height centred on
    # z 1.52 and its lower edge is z 0.300.  THE GROUND IS NOT IN THIS FRAME.
    # That does not weaken the window: the scan takes the FIRST red-over-cream
    # step below the fixtures, so the lower bound only stops a runaway.
    raw = (u0, u1, v0, v1)
    u0, u1 = max(0.0, u0), min(float(rx), u1)
    v0, v1 = max(0.0, v0), min(float(ry), v1)
    if not (u0 < u1 and v0 < v1):
        return None, ("the projected window u %.1f..%.1f v %.1f..%.1f does "
                      "not intersect the %dx%d frame.  Nothing was measured."
                      % (raw[0], raw[1], raw[2], raw[3], int(rx), int(ry)))
    clamped = tuple(round(a - b, 1) for a, b in
                    zip((u0, u1, v0, v1), raw))
    return dict(ucol=(int(np.floor(u0)), int(np.ceil(u1)) + 1),
                vrow=(int(np.floor(v0)), int(np.ceil(v1)) + 1),
                xblind=float(xblind), n_fix=len(fix), n_ground=len(ground),
                scale_err=float(scale_err), clamped=clamped, raw=raw,
                fix_names=sorted(o.name for o in fix),
                ground_names=sorted(o.name for o in ground)), None


def bumper_edge(a, red, cream, ucol, vrow):
    """the topmost red-over-cream step per column, INSIDE the window.
    Character for character the rule P1 uses on the photograph."""
    edge = []
    for u in range(max(0, ucol[0]), min(a.shape[1], ucol[1])):
        for v in range(max(2, vrow[0]), min(a.shape[0] - 6, vrow[1])):
            if red[v - 2, u] and red[v - 1, u] and cream[v:v + 5, u].all():
                edge.append((u, v)); break
    return edge


def coverage(edge, ucol):
    """what fraction of the window's columns the edge actually occupies, the
    largest INTERIOR gap, and whether the fitted parabola's vertex is
    SUPPORTED by data or extrapolated across a hole.

    ------------------------------------------------------------ RULE 8, F285
    THE PAINT IS WHY THIS FUNCTION EXISTS.  P3's window passed, its rms was
    0.81 px, and probe_scratch/rev73_bumper_window.png showed the blue trace
    BROKEN ACROSS THE MIDDLE.  Measured: 340 of 641 columns carry a point, and
    the biggest holes are u 722..810 (89 px) and u 658..720 (63 px) -- either
    side of the window's own centre column, 800.  The cause is not a defect:
    at the centreline the cream V-swage descends to meet the CREAM bumper, so
    there is no red-over-cream step to find.  A SAGITTA IS A STATEMENT ABOUT
    THE MIDDLE, and the middle is exactly what this frame does not carry."""
    if not edge:
        return None
    u = np.array([e[0] for e in edge], int)
    v = np.array([e[1] for e in edge], float)
    lo, hi = int(u.min()), int(u.max())
    have = np.zeros(hi - lo + 1, bool)
    have[u - lo] = True
    gaps, start = [], None
    for i, ok in enumerate(have):
        if not ok and start is None:
            start = i
        if ok and start is not None:
            gaps.append((start + lo, i - 1 + lo)); start = None
    big = max(gaps, key=lambda g: g[1] - g[0]) if gaps else None
    c2, c1, _ = np.polyfit(u.astype(float), v, 2)
    vx = (-c1 / (2 * c2)) if c2 else float("nan")
    supported = bool(lo <= vx <= hi and have[int(round(vx)) - lo]) \
        if (vx == vx and lo <= vx <= hi) else False
    span = float(hi - lo) or 1.0
    holder = [g for g in gaps if g[0] <= vx <= g[1]] if vx == vx else []
    return dict(vx_gap=(holder[0] if holder else None),
                n_cols=int(have.sum()), n_win=int(ucol[1] - ucol[0]),
                n_span=int(hi - lo + 1), frac=float(have.sum()) / (hi - lo + 1),
                big=big, big_px=(big[1] - big[0] + 1) if big else 0,
                big_frac=((big[1] - big[0] + 1) / span) if big else 0.0,
                vx=float(vx), supported=supported)


def paint_window(a, edge, win, out):
    """RULE 8.  The window in GREEN, the points it selected in BLUE."""
    ov = a.copy()
    if win:
        (u0, u1), (v0, v1) = win["ucol"], win["vrow"]
        u0 = int(min(max(0, u0), a.shape[1] - 1))
        v0 = int(min(max(0, v0), a.shape[0] - 1))
        u1 = int(min(max(u0 + 1, u1), a.shape[1] - 1))
        v1 = int(min(max(v0 + 1, v1), a.shape[0] - 1))
        for v in (v0, v1):
            ov[v, u0:u1] = [0, 255, 0]
        for u in (u0, u1):
            ov[v0:v1, u] = [0, 255, 0]
    for u, v in edge:
        ov[max(0, v - 1):v + 2, u] = [0, 120, 255]
    os.makedirs(SCRATCH, exist_ok=True)
    Image.fromarray(np.clip(ov, 0, 255).astype("uint8")).save(out)


def mesh_plan_bulge():
    """x(y=0) - x(|y|=0.70) on the built nose, at four heights above ground.

    THIS IS THE NUMBER NOTHING IN THIS TREE HAD EVER MEASURED.  It is what
    `t1_shell.nose_shape`'s  bulge = 0.019 * w * max(0, 1 - r)  produces.
    T1_NOSE_BULGE scales it and is the kill (measurement-only)."""
    bpy = _build_scene()
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
    nowin = os.environ.get("T1_NOSE_NOWIN") == "1"
    frame = argv[0] if argv else None

    checks, fails, absent = [], [], []

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
        return (bool(v) and v["rms"] <= rms_bar(v["span"])
                and not v["rescued"])

    ok_named = [k for k, v in photo.items() if clean(v)]
    ck("P1 the photographed bumper's top edge is traceable AS ONE EDGE  "
       "[PAINTED to probe_scratch/rev67_bumper_*.png BEFORE any number below "
       "was read -- rule 8].  A fit whose scatter exceeds max(4 px, 3 % of "
       "span) is fragments, not an edge, and REFUSES rather than reporting a "
       "number (rule 37)",
       len(ok_named) >= 1,
       "; ".join("%s n=%d/%d span=%.0f/%.0f rms=%.1f px -> %s"
                 % (k, v["n"], v["n0"], v["span"], v["span0"], v["rms"],
                    "USED" if clean(v)
                    else ("REFUSED, the clip RESCUED it" if v["rescued"]
                          else "REFUSED, not one edge"))
                 for k, v in photo.items() if v)
       + "".join("; %s NO TRACE" % k for k, v in photo.items() if not v))

    for k, v in photo.items():
        if not clean(v):
            continue
        ck("P2 %s: the bumper's top edge IS NOT A STRAIGHT 3-D LINE -- a "
           "straight line images straight under ANY pinhole camera, so a "
           "sagitta many times its own standard error is SHAPE, not pose.  "
           "*** AND THAT IS ALL IT LICENSES (F220).  It does NOT say the nose "
           "is curved IN PLAN: a plan-FLAT bumper whose top edge sweeps up at "
           "its ends is curved in ELEVATION and gives the same sign.  This "
           "frame does not separate the two, and rev 67 first published the "
           "conclusion as though it did ***" % k,
           abs(v["sag"]) > 3.0 * v["se"] if v["se"] == v["se"] else False,
           "sagitta %+.2f px +- %.2f (%.1f sigma) over a %.0f px chord "
           "= %+.4f of chord; fit rms %.2f px"
           % (v["sag"], v["se"], abs(v["sag"]) / v["se"] if v["se"] else 0,
              v["span"], v["frac"], v["rms"]))

    # -------------------------------------------------- the render
    # ======================================================== rev 73, F284
    # P3 IS WINDOWED NOW, AND THE WINDOW IS PROJECTED, NOT TYPED.
    #
    # Rev 70, 71 and 72 all recorded this row refusing and none of them fixed
    # the cause.  Rev 72 established what the cause is NOT: it is not the
    # three-quarter pose.  Given `out/r72_front.png`, the straight-on FRONT
    # preview, the un-windowed scan still read fit rms 113.22 px = 12 % of
    # span with 475 of 476 points clipped (F277).  The row's own NAME blamed
    # the pose; its own SOURCE COMMENT blamed the un-windowed scan.  MEASURED
    # at rev 73 on out/r73_front.png, by histogramming the scan's own points:
    #     v 1000-1040   355 of 481 points   <- THE BUMPER
    #     v  517- 880   126 of 481 points   <- the galley at u 1255..1327,
    #                                          the mirrors at u 401..430,
    #                                          the mural, the roof shoulder
    # One parabola through both populations is what the 113.70 px rms is.
    # THE COMMENT WAS RIGHT.
    #
    # The window is cut from the nose FIXTURES and the TYRES and never from
    # the bumper -- see fixture_window()'s rule-6 and rule-8 blocks.
    ren = None
    win = None
    win_why = None
    if frame and os.path.exists(frame):
        aa = np.asarray(Image.open(frame).convert("RGB")).astype(float)
        red, cream = _masks(aa)
        ry, rx = aa.shape[0], aa.shape[1]
        # ---------------------------------------------------------- rule 42
        # A CONTROL MUST BE FRAMED THE WAY ITS MEASUREMENT IS FRAMED.  This
        # window is the FRONT elevation's and no other view's.  Handed a
        # hero34f the projection would be silently wrong, so refuse by name
        # rather than measure.
        base = os.path.basename(frame)
        if not base.endswith("_front.png"):
            win_why = ("%s is not a `front` frame.  This window is projected "
                       "through studio.views()['front'] and is valid for that "
                       "elevation ONLY (rule 42)." % base)
        elif nowin:
            # ------------------------------------------- THE KILL, rule 3/36
            # T1_NOSE_NOWIN=1 restores the PRE-REV-73 whole-frame scan.  P3
            # must go RED.  Watched at rev 73 on out/r73_front.png:
            #   windowed  rms   0.81 px over 640 px, 0 of 340 points clipped
            #                   -> ONE EDGE, PASSES
            #   T1_NOSE_NOWIN=1 rms 113.70 px over 926 px, 481 of 481 points
            #                   clipped -> REFUSED
            # *** THE FIRST CUT OF THIS COMMENT READ "rms 2.09 px over 620 px"
            # AND THAT FIGURE WAS NEVER PRINTED BY ANYTHING.  It was typed into
            # the patch BEFORE the windowed run existed and never re-read
            # afterwards, so it disagreed with the number this same revision
            # published in five other places.  RULE 5: never put a figure in an
            # acceptance test unless you watched it print.  Caught by the
            # rule-17 adversary dispatched at rev 73's own outgoing brief. ***
            win = dict(ucol=(0, aa.shape[1]),
                       vrow=(int(aa.shape[0] * 0.45), aa.shape[0]),
                       xblind=float("nan"), n_fix=0, n_ground=0,
                       fix_names=["T1_NOSE_NOWIN -- NO WINDOW"])
        elif not want_mesh:
            win_why = ("--nomesh was given.  The window is PROJECTED off the "
                       "built fixtures, so without the build there is no "
                       "window and nothing may be read (rule 37).")
        else:
            win, win_why = fixture_window(rx, ry)

        if win:
            edge = bumper_edge(aa, red, cream, win["ucol"], win["vrow"])
            ren = sagitta(edge)
            # ---------------------------------------------------- rev 73, F297
            # THE PAINT ONLY OVERWRITES THE COMMITTED ARTEFACT FOR A REAL FRAME
            # OUT OF out/.  Rev 73's own new verify_clone rows run this probe on
            # a 2x2 SYNTHETIC png to exercise the refusal paths, and the first
            # cut of them repainted probe_scratch/rev73_bumper_window.png with
            # that 2x2 test image -- so `./verify_clone.sh` left the tree DIRTY
            # and the NEXT run failed its own "modified tracked files" row.
            # A verifier that dirties the tree it verifies fails the run after
            # the one you are looking at, which is the worst kind of flake.
            _real = os.path.dirname(os.path.abspath(frame)) == \
                os.path.join(HERE, "out")
            _out = os.path.join(SCRATCH, "rev73_bumper_window.png") if _real \
                else os.path.join("/tmp", "rev73_bumper_window_scratch.png")
            paint_window(aa, edge, win, _out)
            print("  P3 window %s  u %d..%d  v %d..%d  from %s"
                  % ("(T1_NOSE_NOWIN -- ABLATED, whole frame)" if nowin
                     else "projected off " + ", ".join(win["fix_names"])
                          + " + " + ", ".join(win.get("ground_names", [])),
                     win["ucol"][0], win["ucol"][1],
                     win["vrow"][0], win["vrow"][1],
                     "the ablation" if nowin else "the built scene"))
            if win.get("raw") and any(win.get("clamped", ())):
                print("     clamped to the frame by (u0 %+.1f, u1 %+.1f, "
                      "v0 %+.1f, v1 %+.1f) px from the projected "
                      "u %.1f..%.1f v %.1f..%.1f -- stated, not silent"
                      % (win["clamped"] + win["raw"]))
            print("     PAINTED -> %s -- LOOK AT IT (rule 8).  %d columns "
                  "selected." % (_out, len(edge)))
        else:
            print("  P3 WINDOW NOT AVAILABLE -- %s" % win_why)
            absent.append("P3 (the RENDER's bumper edge) -- %s"
                          % win_why.split(".")[0])
    elif frame:
        print("NO RENDER -- %s does not exist.  out/ is untracked and starts "
              "EMPTY on a clone.  Nothing was measured." % frame)
        return 2
    else:
        # ------------------------------------------------------- rev 68, F225
        # A CONTROL THAT DID NOT RUN MUST NOT READ AS A CLEAN PASS.  RULE 3.
        #
        # This branch did not exist.  Invoked with NO ARGUMENT -- which is how
        # every brief through rev 68 prints this probe, and how §6's run list
        # does not print it at all -- `ren` stayed None, P3 never executed, and
        # the probe reported "4 checked, 0 FAILED" and EXIT 0.  Meanwhile the
        # rev-68 brief's §0.07 publishes "5 checked, 1 FAILED -- P3", and §0.05
        # holds that row up as the proof its outgoing audit works.  The row is
        # obtainable ONLY with a frame argument the brief never gives.  Watched
        # at rev 68, true exit codes, no pipe:
        #     probe_rev67_nose.py                   -> 4 checked, 0 FAILED, rc 0
        #     probe_rev67_nose.py out/r68_front.png -> 5 checked, 1 FAILED, rc 1
        # The refusal below covers the wrong-file case; nothing covered the
        # no-argument case, which is the one that actually gets typed.
        # *** rev 72 -- THE MESSAGE WAS RIGHT AND THE VERDICT WAS STILL GREEN. ***
        # Rev 68 added the refusal TEXT above; rev 70 and rev 71 both recorded
        # that the probe still "prints a GREEN summary and exits 0 while its
        # first line refuses", and neither fixed it.  A reader obeying rule 9 --
        # read the SUMMARY line, never the exit code -- was handed
        # "4 checked, 0 FAILED".  Rule 37: an absent input must never read as a
        # measurement.  The absence is now COUNTED and carried into the summary
        # and the exit code.  Watched at rev 72:
        #     bare                    -> "2 checked, 0 FAILED, 1 ABSENT", rc 2
        #     out/r72_front.png       -> the P3 row runs and REFUSES, rc 1
        # *** rev 73, F287 -- THAT FIRST LINE IS THE `--nomesh` READING, NOT
        # THE BARE ONE, AND IT WAS COPIED INTO FIVE CARRIERS.  Re-measured at
        # rev 73, true exit codes, no pipe:
        #     bare            -> "4 checked, 0 FAILED, 1 ABSENT", rc 2
        #     --nomesh        -> "2 checked, 0 FAILED, 1 ABSENT", rc 2
        # Bare runs P1, P2 and the two mesh rows; --nomesh drops the mesh
        # rows.  The rc-2 / ABSENT FIX IS REAL on both paths -- only the count
        # attributed to "bare" was wrong.  verify_clone.sh's row was NAMED
        # "bare" while RUNNING --nomesh, so the guard reproduced the mislabel
        # instead of catching it; it is renamed and has a companion row now. ***
        # *** THIS MESSAGE USED TO HARDCODE `out/r72_front.png` (F321).  That
        # prefix went stale two revisions later, and `out/` is untracked and
        # starts EMPTY on a clone, so the example it told the reader to run
        # resolved to NOTHING.  A probe that names a frame must name one that
        # exists: it now offers whatever `out/` actually holds, and falls back
        # to naming the SOURCE of the prefix rather than a guess at its value.
        # Same class as F320(c); found by the rule-15 adversary. ***
        import glob as _g
        _have = sorted(_g.glob(os.path.join(HERE, "out", "*_front.png")))
        _eg = ("out/%s" % os.path.basename(_have[-1]) if _have
               else "out/<the T1_PFX you rendered>_front.png  (out/ is empty "
                    "here -- run the brief's SS0 render first)")
        print("NO FRAME GIVEN -- P3 (the RENDER's bumper edge) DID NOT RUN.  "
              "Pass a frame, e.g. `python3 probe_rev67_nose.py %s`.  "
              "The photograph and mesh rows below stand; "
              "the render row is ABSENT, not passed." % _eg)
        absent.append("P3 (the RENDER's bumper edge) -- no frame given")

    if win and not nowin:
        # ---------------------------------------------------- P3w, rule 6
        # THE WINDOW CANNOT SEE THE THING P3 MEASURES, AND THIS IS THE TEST
        # RATHER THAN THE CLAIM.  Displace a fixture vertex 100 mm along X --
        # the axis the whole plan bow lives on -- and re-project it.  Under the
        # front ORTHOGRAPHIC camera the pixel must not move at all.
        ck("P3w the window is BLIND to the axis the bow lives on -- a 100 mm "
           "X displacement of a window anchor moves its pixel by 0",
           win["xblind"] == win["xblind"] and win["xblind"] < 1e-6,
           "100 mm in X moves the anchor's pixel by %.3e px, over a window "
           "u %d..%d / v %d..%d cut from %d fixtures + %d tyres.  The bow is "
           "an X quantity; this window is a (y, z) one (rule 6)."
           % (win["xblind"], win["ucol"][0], win["ucol"][1],
              win["vrow"][0], win["vrow"][1], win["n_fix"], win["n_ground"]))

    cov = coverage(edge, win["ucol"]) if (win and ren) else None
    if cov:
        # --------------------------------------------------- P3c, rule 8/12
        # THE COVERAGE ROW.  It does not invent a bar; it asks a
        # threshold-free question -- is the parabola's VERTEX standing on a
        # measured column, or is its magnitude extrapolated across a hole?
        # A sagitta is a claim about the middle.
        ck("P3c the sagitta's VERTEX stands on a measured column rather than "
           "being extrapolated across a hole in the trace",
           cov["supported"],
           "%d of %d window columns carry a point (%.0f %% of the traced "
           "span); largest interior gap %s = %d px = %.0f %% of span; the "
           "fitted vertex is at u %.0f and is %s.  *** THE CAUSE IS NOT A "
           "DEFECT: at the centreline the cream V-swage descends to meet the "
           "CREAM bumper, so there is no red-over-cream step to find there. "
           "It is a PROPERTY OF THIS FRAME, and it is why the magnitude below "
           "is quoted with this row attached (rule 12). ***"
           % (cov["n_cols"], cov["n_win"], 100 * cov["frac"],
              ("u %d..%d" % cov["big"]) if cov["big"] else "none",
              cov["big_px"], 100 * cov["big_frac"], cov["vx"],
              "SUPPORTED" if cov["supported"] else
              ("IN THE GAP u %d..%d -- the sagitta's MAGNITUDE is an "
               "extrapolation and must not be read as shape"
               % cov["vx_gap"]) if cov["vx_gap"] else
              "OUTSIDE the traced span -- the sagitta's MAGNITUDE is an "
              "extrapolation and must not be read as shape"))

    if ren:
        # THE SAME GATE AS P1.  Before rev 73 this scanned the WHOLE FRAME and
        # caught every cream-under-red boundary in it -- the galley, the
        # mirrors, the mural -- and fitted one parabola through the lot.  Rev
        # 67 watched it report sagitta +54.35 px with an rms of 61.85 px on an
        # 831 px span and did NOT publish it; rev 72 watched the same failure
        # on a straight-on FRONT frame and correctly refused the pose
        # explanation (F277).  The window is projected now (F284).
        ck("P3 the RENDER's bumper top edge traces AS ONE EDGE by the same "
           "rule P1 uses, inside a window projected from the nose FIXTURES "
           "and the TYRES -- never from the bumper",
           ren["rms"] <= rms_bar(ren["span"]) and not ren["rescued"],
           "sagitta %+.2f px +- %.2f over %.0f px (pre-clip %.0f px, %d of %d "
           "points clipped) = %+.4f of chord, fit rms %.2f px = %.0f %% of "
           "span -> %s.  MAGNITUDES ARE NOT COMPARABLE "
           "ACROSS POSES (rule 43) in any case -- only the sign and the "
           "presence of curvature are"
           % (ren["sag"], ren["se"], ren["span"], ren["span0"],
              ren["n_clipped"], ren["n0"], ren["frac"], ren["rms"],
              100 * ren["rms"] / ren["span"],
              "one edge" if (ren["rms"] <= rms_bar(ren["span"])
                             and not ren["rescued"])
              else ("REFUSED, the clip RESCUED it" if ren["rescued"]
                    else "REFUSED, fragments")))

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
    print("  measured exactly on its own mesh.")
    print()
    print("  *** AND THE CEILING REV 73 OWES ON ITS OWN NEW ROW (F284).  P3 IS")
    print("  A READING OF THE RENDER'S BUMPER EDGE -- THE FIRST THIS PROJECT")
    print("  HAS HAD -- AND ON A `front` FRAME IT CANNOT SEE THE PLAN BOW.")
    print("  P3w does not merely permit that statement, it MEASURES it: a")
    print("  100 mm displacement along X moves a window anchor's pixel by 0.")
    print("  The plan bow is an X quantity.  The same orthographic")
    print("  X-blindness that makes this window safe under rule 6 makes the")
    print("  FRAME blind to the bow GEOMETRICALLY.  P3's +0.45 px over 640 px")
    print("  is therefore the edge's curvature IN ELEVATION.")
    print()
    print("  *** AND THE FIRST DRAFT OF THIS BLOCK WENT ONE STEP FURTHER AND")
    print("  WAS WRONG (F292).  It said the reading 'says NOTHING about")
    print("  BUMP_BOW'.  A rule-17 adversary pointed out that P3w displaces a")
    print("  WINDOW ANCHOR, so it proves the WINDOW is X-blind and says")
    print("  nothing about the TRACE -- and that T1_BUMP_BOW, the switch that")
    print("  would settle it, had never been run (rule 36).  IT WAS RUN:")
    print("      shipped bow (+21.09 mm)  sagitta +0.45 px  span 640  n 340")
    print("      T1_BUMP_BOW=0 (+0.00 mm) sagitta +0.07 px  span 627  n 314")
    print("      FLOOR, same config twice  +0.45 -> +0.44   span 640  n 335")
    print("  The ablation moves the sagitta by 0.38 px against a between-render")
    print("  floor of 0.01 px -- 38x.  THE TRACE IS SENSITIVE TO THE BOW.  Not")
    print("  geometrically -- P3w's 0.000e+00 stands -- but PHOTOMETRICALLY:")
    print("  bowing the blade turns it against the light, which moves the")
    print("  sub-pixel red/cream threshold and changes which columns carry a")
    print("  detectable step at all (26 columns of span, 26 points).  So a")
    print("  `front` frame DOES carry bow information; it carries it through")
    print("  SHADING, which is not a geometric ruler and must not be read as")
    print("  one until something calibrates it. ***")
    print("  WHAT THAT IS WORTH, AND IT IS NOT NOTHING: P2's own ceiling says")
    print("  a three-quarter frame cannot separate plan bow from elevation")
    print("  curvature because both give the same sign.  A `front` frame")
    print("  measures the ELEVATION term ALONE.  It is the missing half of")
    print("  that separation, and this revision did not spend it -- no")
    print("  three-quarter render-side reading exists to subtract it from.")
    print()
    print("  *** THE CEILING REV 67 FIRST PUBLISHED HERE IS REFUTED, IN THE")
    print("  SAME REVISION THAT WROTE IT (F219/F221).  It read: 'converting a")
    print("  projected sagitta needs the camera, and F26's camera ambiguity is")
    print("  unresolved, so the real bus's plan bulge CANNOT BE RECOVERED FROM")
    print("  WHAT WE HOLD'.  Three things were wrong with it:")
    print("    1. THE FRAME CARRIES ITS OWN INTRINSICS.  ref_nolita_front34.jpg")
    print("       is a SONY DSC-RX100, f 10.4 mm, 35mm-equiv 28, 3:2 UNCROPPED")
    e = exif_focal(os.path.join(HERE, "ref_nolita_front34.jpg"))
    if e:
        print("       -> f = %.1f px, read live from EXIF just now" % e[0])
    print("       NOTHING in this tree had ever read EXIF, and the record said")
    print("       'the focal length of a camera nobody recorded' for FIVE revs.")
    print("    2. F26 IS NOT ABOUT THIS FRAME.  Its row is an ATTRIBUTION")
    print("       defect over ref_side.jpg and ref_playa_34.png.  Citing it to")
    print("       block a third frame is rule 34, inside the revision whose own")
    print("       brief carries rule 34.")
    print("    3. AND A METRIC ROUTE EXISTS AND WAS RUN: forward-modelling the")
    print("       bumper's plan profile through a camera built from the EXIF")
    print("       focal and the two hubcap centroids gives B ~ 40 mm, bracketed")
    print("       20-55 mm by lens distortion measured in-frame.  THE SHIPPED")
    print("       NOSE IS 19.6 mm -- at or below the bottom of that range. ***")
    print()
    print("  WHAT IS STILL TRUE: this probe does not implement that route, and")
    print("  the camera failed its own painted validation (belt line 18 px out),")
    print("  so 40 mm is BRACKETED, not validated.  One straight-edge across the")
    print("  two front bumper corners, photographed against a ruler, would")
    print("  settle it outright with no camera model at all.")
    print("-" * 78)
    print("  %d checked, %d FAILED%s%s"
          % (len(checks), len(fails),
             (", %d ABSENT" % len(absent)) if absent else "",
             ("  --  " + "; ".join(fails + absent)) if (fails or absent) else ""))
    if absent and not fails:
        print("  ⚠ NOT A PASS.  %d row(s) did not run.  A probe that could not "
              "measure has not measured (rule 37)." % len(absent))
    print("=" * 78)
    return 1 if fails else (2 if absent else 0)


if __name__ == "__main__":
    sys.exit(main())
