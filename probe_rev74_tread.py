#!/usr/bin/env python3
"""probe_rev74_tread.py -- rev 74.  THE TYRE'S TRANSVERSE TREAD.  F308.

WHAT THIS IS ABOUT.  `t1_detail.tyre()` returns `T.revolve(prof, seg=..., axis='Y')`.
A surface of revolution is ROTATIONALLY SYMMETRIC BY CONSTRUCTION, so the built
tyre cannot express a transverse lug however its profile is tuned -- its four
grooves are CIRCUMFERENTIAL rings.  `ref_playa_34.png` shows transverse lugs on
the front tyre's shoulder, and they are real image structure at TRUE PIXEL
RESOLUTION, not an upscaling artefact (looked at first, NEAREST, no
interpolation: probe_scratch/r74_tread_nearest.png).  That is rule 54's shape --
the quantity is not a free parameter of the model -- so it needs new
construction, not tuning.

READ THIS PROBE'S OWN SUMMARY LINE, NEVER ITS EXIT CODE (rule 9).

WHAT IT DOES **NOT** CLAIM, AND THIS IS THE CEILING (rule 12).  It does NOT
publish a lug count.  Two independent estimators on the same photograph -- a
groove PEAK COUNT and an FFT of the same angular signal -- disagree by ~30 %,
and each moves with the radius it is read at.  The tread pitch is ~3 px in a
500x400 frame.  T2 reports the BRACKET and REFUSES to name a figure inside it.
The shipped `TREAD_LUGS` is therefore a DECLARED CHOICE INSIDE A MEASURED
BRACKET, exactly as `TB_WIDTH` is, and it is labelled that way in the source.
"""
import os, sys, math

TREAD_DUTY_EXPECT = 1.0 / 3.0   # 2 of TREAD_SEG=6, and T7 MEASURES it

FAIL = []
CHECK = 0
ABSENT = 0


def row(tag, ok, msg):
    global CHECK
    CHECK += 1
    if ok is None:
        print("  [ABSENT] %-4s %s" % (tag, msg))
    else:
        print("  [%s] %-4s %s" % ("PASS" if ok else "FAIL", tag, msg))
        if not ok:
            FAIL.append(tag)


print("W1  THE TYRE'S TRANSVERSE TREAD -- photograph, then mesh.  F308.")
print("-" * 78)

# ---------------------------------------------------------------- photograph
try:
    import numpy as np
    from PIL import Image
    import scipy.ndimage as ndi
    HERE = os.path.dirname(os.path.abspath(__file__))
    a = np.asarray(Image.open(os.path.join(HERE, "ref_playa_34.png")
                              ).convert("RGB")).astype(float)
    lum = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
except Exception as e:                                    # pragma: no cover
    print("  NO PHOTOGRAPH: %s" % e)
    lum = None

# The front wheel, and the tyre band, both MEASURED off the radial profile
# along y=325 rather than assumed: red hubcap to r 11, cream rim ring 13..17,
# DARK TYRE 19..37, body beyond.  Printed by the ladder in LEDGER_rev74.md.
CX, CY = 232.0, 324.0
ARC = (150, 262)


def _band(frac, lo=18, hi=50):
    """Luminance around the tyre at `frac` of the silhouette radius."""
    ths = np.radians(np.arange(ARC[0], ARC[1], 0.2))

    def sil(th):
        rs = np.arange(lo, hi, 0.2)
        v = ndi.map_coordinates(lum, [CY - rs * np.sin(th), CX + rs * np.cos(th)],
                                order=1)
        idx = np.nonzero(v < 60)[0]
        return rs[idx[-1]] if len(idx) else np.nan

    sr = np.array([sil(t) for t in ths])
    sr = ndi.median_filter(np.where(np.isnan(sr), np.nanmedian(sr), sr), 9)
    rs = sr * frac
    v = ndi.map_coordinates(lum, [CY - rs * np.sin(ths), CX + rs * np.cos(ths)],
                            order=1)
    return ths, v, v - ndi.uniform_filter1d(v, 25, mode="nearest")


if lum is not None:
    # T1 -- IS THERE ANY TRANSVERSE STRUCTURE AT ALL?  Against a CONTROL on the
    # smooth SIDEWALL, which has no lugs.  Without this row the numbers below
    # would be indistinguishable from grain (rule 49: a difference with no
    # floor under it is not a measurement).
    _, _, tread = _band(0.91)
    _, _, wall = _band(0.62)
    ratio = tread.std() / max(wall.std(), 1e-6)
    row("T1", ratio > 1.5,
        "the SHOULDER carries transverse structure the SIDEWALL does not: "
        "rms %.2f vs %.2f levels = %.2fx (floor: the sidewall itself)"
        % (tread.std(), wall.std(), ratio))

    # T2 -- THE COUNT, AND IT REFUSES TO NAME ONE.
    ests = []
    for frac in (0.86, 0.91, 0.96):
        ths, _, res = _band(frac)
        mins = ((res[1:-1] < res[:-2]) & (res[1:-1] < res[2:])
                & (res[1:-1] < -res.std() * 0.5))
        arc = ARC[1] - ARC[0]
        ests.append(("peak", frac, mins.sum() * 360.0 / arc))
        F = np.abs(np.fft.rfft(res * np.hanning(len(res))))
        fr = np.fft.rfftfreq(len(res), d=np.radians(0.2)) * 2 * math.pi
        lo_, hi_ = np.searchsorted(fr, 20), np.searchsorted(fr, 140)
        ests.append(("fft", frac, fr[lo_ + int(np.argmax(F[lo_:hi_]))]))
    vals = [e[2] for e in ests]
    lo_v, hi_v = min(vals), max(vals)
    print("        six estimates (2 methods x 3 radii): "
          + ", ".join("%s@%.2f %.0f" % e for e in ests))
    row("T2", (hi_v / lo_v) > 1.3,
        "REFUSES to publish a lug count: the bracket is %.0f..%.0f per "
        "revolution, a %.2fx span, and the two methods disagree.  A point "
        "estimate here would be below the instrument's own noise floor "
        "(rule 42).  THE BRACKET IS THE RESULT" % (lo_v, hi_v, hi_v / lo_v))
else:
    row("T1", None, "no photograph")
    row("T2", None, "no photograph")
    ABSENT += 2

# ---------------------------------------------------------------------- mesh
try:
    import bpy                                                  # noqa: F401
    import t1_detail as D
    import t1_core as T
except Exception as e:                                          # pragma: no cover
    print("  NO MESH: %s -- the build rows below CANNOT run (rule 37)" % e)
    row("T3", None, "no mesh")
    row("T4", None, "no mesh")
    row("T5", None, "no mesh")
    ABSENT += 3
    D = None


def _crown_spread(ob):
    """Worst radius spread AT FIXED PROFILE POINT, across revolve angles.

    *** THE FIRST CUT OF THIS FUNCTION WAS WRONG AND ITS OWN T3 CAUGHT IT
    (F310, rule 3).  It pooled every crown vertex and took one spread, which
    reads the PROFILE's radial variation -- the four circumferential grooves
    (0.0080) plus the crown camber (0.0042) -- and duly returned 0.0119 m on a
    tyre that IS a surface of revolution.  A statistic that answers "is this
    rotationally symmetric?" must hold the profile point FIXED and vary ONLY
    the angle.  `revolve` emits every angle at each profile point with an
    identical y, so binning on exact y is construction-agnostic: it needs no
    knowledge of the vertex ordering or of len(profile). ***
    """
    from collections import defaultdict
    g = defaultdict(list)
    for v in ob.data.vertices:
        # NOT a re-typed 0.052: read the live constant the cut uses (F319)
        import t1_detail as _D
        if abs(v.co.y) > _D.TREAD_HALF:
            continue
        r = math.hypot(v.co.x, v.co.z)
        if r < T.TIRE_R - 0.030:            # sidewall/bead, not the crown
            continue
        g[round(v.co.y, 6)].append(r)
    worst, rmax, n = 0.0, 0.0, 0
    for _y, rs in g.items():
        n += len(rs)
        rmax = max(rmax, max(rs))
        if len(rs) > 1:
            worst = max(worst, max(rs) - min(rs))
    return worst, rmax, n, len(g)


if D is not None:
    ob = D.tyre("probe_tyre")
    spread, rmax, nv, nband = _crown_spread(ob)

    # T3 -- THE HEADLINE.  A revolve gives EXACTLY ZERO spread at fixed |y|;
    # this reads the whole crown, so the four circumferential grooves are in
    # it too and the bar is set above them.  WATCHED RED before rev 74's
    # change and GREEN after -- that is the whole of rule 3.
    row("T3", spread > 0.0015,
        "the built tyre is NOT a surface of revolution: worst radius spread "
        "AT FIXED PROFILE POINT is %.4f m, over %d crown verts in %d bands "
        "(a revolve reads 0.000000 exactly, at every band)"
        % (spread, nv, nband))

    # T4 -- THE KILL.  The ablation must put the revolve back.
    os.environ["T1_TYRE_TREAD"] = "0"
    import importlib
    importlib.reload(D)
    ob0 = D.tyre("probe_tyre_abl")
    spread0, rmax0, nv0, _ = _crown_spread(ob0)
    del os.environ["T1_TYRE_TREAD"]
    row("T4", spread0 < 1e-6,
        "KILL, WATCHED: T1_TYRE_TREAD=0 restores the surface of revolution "
        "exactly -- worst spread %.2e m over %d crown verts, against a 1e-6 bar "
        "that is the float floor of hypot(cos, sin) and 6000x under the "
        "groove depth.  A switch that "
        "did not ablate would read like the built case (rule 47)"
        % (spread0, nv0))

    # T5 -- THE LOCKED DIAMETER MUST NOT MOVE.  The grooves are cut INWARD
    # from the crown, so the tyre's maximum radius -- which verify.py locks as
    # TYRE_D 0.665 -- is the same object before and after.
    # *** T5 USED TO READ THE WRONG QUANTITY AND SAID SO IN ITS OWN MESSAGE
    # (F319).  It compared max RADIUS and concluded "the tread does NOT move
    # TYRE_D".  `verify.py` locks no radius: `_measure_wheels` sets
    # `out["TYRE_D"] = max(zs) - min(zs)`, a Z BOUNDING-BOX EXTENT, and the
    # vertex nearest the +Z pole falls in a groove, so that extent DOES move.
    # A guard must measure the quantity it names (rule 38).  It now reads BOTH.
    def _zext(o):
        zs = [v.co.z for v in o.data.vertices]
        return max(zs) - min(zs)
    ze, ze0 = _zext(ob), _zext(ob0)
    row("T5", abs(rmax - rmax0) < 1e-6,   # same float floor as T4, declared
        "the tread does not move the crown's maximum RADIUS: %.6f built vs "
        "%.6f ablated, delta %.2e m -- the grooves cut INWARD"
        % (rmax, rmax0, abs(rmax - rmax0)))
    _TOL = 0.025                          # verify.py's own tolerance on TYRE_D
    row("T5b", abs(ze - ze0) < _TOL,
        "AND THE QUANTITY verify.py ACTUALLY LOCKS -- TYRE_D = max(z)-min(z), "
        "a BBOX EXTENT, not a radius -- DOES move: %.7f built vs %.7f ablated, "
        "delta %.4f mm.  That is %.0fx inside verify.py's own TOL of %.3f m, "
        "and it is a DISCRETISATION artefact: which discrete vertex lands "
        "nearest the +Z pole, not the tyre's diameter over its lands"
        % (ze, ze0, 1000 * abs(ze - ze0), _TOL / max(abs(ze - ze0), 1e-12), _TOL))

    # T7 -- THE REALISED DUTY, MEASURED OFF THE MESH (rule 10: a claim in a
    # source comment is not a measurement).  The first cut of _cut_tread
    # shipped an IRREGULAR tread -- 99 of 384 vertices cut instead of 128, in
    # runs of 1 AND 2 -- because its phase threshold left the LEADING edge on
    # the modulo wrap with zero margin (F319).  This row would have caught it.
    import re as _re
    _ring = sorted((math.atan2(v.co.z, v.co.x), math.hypot(v.co.x, v.co.z))
                   for v in ob.data.vertices if abs(v.co.y) < 1e-9)
    _R = max(r for _, r in _ring)
    _pat = "".join("X" if r < _R - 0.001 else "." for _, r in _ring)
    # ROTATE so the string starts on a land: otherwise a groove straddling the
    # array wrap is counted as two short runs and the row reports [1, 2] on a
    # perfectly regular tread.  (My first cut of T7 did exactly that.)
    _i = _pat.find(".X")
    _pat = _pat[_i + 1:] + _pat[:_i + 1] if _i >= 0 else _pat
    _runs = sorted(set(len(m) for m in _re.findall(r"X+", _pat)))
    _cut = _pat.count("X")
    _want = len(_ring) * TREAD_DUTY_EXPECT
    row("T7", len(_runs) == 1 and abs(_cut - _want) < 2,
        "THE TREAD IS REGULAR: %d of %d equator vertices cut (expected %.0f = "
        "%d of %d segments per lug), every groove run the SAME width %s.  The "
        "shipped-then-fixed defect read 99/384 in runs of 1 AND 2"
        % (_cut, len(_ring), _want, round(TREAD_DUTY_EXPECT * 6), 6, _runs))

# ------------------------------------------------------------- render side
# T6 -- DID THE GEOMETRY REACH THE RENDER?  The BEFORE frame cannot be used
# here (it is not on disk after a rebuild), so the floor is taken from the
# ONE thing that is provable: a surface of revolution has NO angular structure
# in its silhouette, so a frame of the ABLATED tyre is a measured floor rather
# than an assumed one.  Rev 74 read it as 0.0503 px rms / dominant amplitude 4
# against 0.5286 px / amplitude 161 at exactly 64 cycles/rev on the SHIPPED
# tread (out/r74f_side.png).  The 0.4499 / 130 this comment used to call "the
# shipped" is the IRREGULAR first cut, superseded by F319 -- fixing the tread
# made the 64-cycle signal CLEANER, which is the direction it should move (F322).
#
# ⚠ TWO THINGS THIS ROW DOES **NOT** SAY.
#  (a) rule 6: recovering 64 from the pixels is NOT evidence that 64 is the
#      RIGHT count.  TREAD_LUGS is declared and the photograph brackets it at
#      48..84 (T2).  This row says the declared geometry REACHED THE FRAME.
#  (b) rule 5 / F198: the FLOOR figures in its message are RECORDED, not
#      recomputed -- see the message itself.  Do not read "measured" as
#      "measured by this row".
# NAME YOUR FRAME (F316).  An explicit argv frame wins; otherwise the
# alphabetically-last out/*_side.png, and the row PRINTS which it used -- a
# probe that silently picks a frame is how rev 74 attributed a reading to a
# frame the probe could not have read (F320(c)).
import glob
_argv = [a for a in sys.argv[1:] if a.endswith(".png")]
_side = _argv if _argv else sorted(
    glob.glob(os.path.join(HERE if 'HERE' in dir() else '.', "out", "*_side.png")))
if not _side or lum is None:
    row("T6", None, "no *_side.png in out/ -- out/ is untracked and starts "
                    "EMPTY, so the render-side row cannot run (rule 37).  It "
                    "is SKIPPED, not failed: a missing input is not a defect")
    ABSENT += 1
else:
    try:
        f = _side[-1]
        import photometry as PH
        _a, _m = PH.read_png(f)
        _a = _a[..., :3].astype(float) / _m
        _L = (0.299 * _a[..., 0] + 0.587 * _a[..., 1] + 0.114 * _a[..., 2]) * 255.0
        _sub = np.zeros(_L.shape, bool)
        _sub[780:960, 1010:1180] = True
        _red = ((_a[..., 0] > _a[..., 1] + 0.15) & (_a[..., 0] > _a[..., 2] + 0.15)
                & (_a[..., 0] > 0.25) & _sub)
        _lab, _k = ndi.label(_red)
        _sz = ndi.sum(_red, _lab, range(1, _k + 1))
        _ys, _xs = np.nonzero(_lab == int(np.argmax(_sz)) + 1)
        _cx, _cy = _xs.mean(), _ys.mean()
        _th = np.radians(np.arange(200, 340, 0.15))
        _rr = []
        for _t in _th:
            _rs = np.arange(60, 140, 0.05)
            _v = ndi.map_coordinates(_L, [_cy - _rs * np.sin(_t),
                                          _cx + _rs * np.cos(_t)], order=1)
            _d = np.nonzero(_v < 90)[0]
            _rr.append(_rs[_d[-1]] if len(_d) else np.nan)
        _rr = np.array(_rr)
        _ok = ~np.isnan(_rr)
        _r = _rr[_ok]
        _res = _r - ndi.uniform_filter1d(_r, 61, mode="nearest")
        _F = np.abs(np.fft.rfft(_res * np.hanning(len(_res))))
        _fr = (np.fft.rfftfreq(len(_res), d=np.radians(0.15)) * 2 * math.pi)
        _lo, _hi = np.searchsorted(_fr, 20), np.searchsorted(_fr, 140)
        _dom = _fr[_lo + int(np.argmax(_F[_lo:_hi]))]
        row("T6", _res.std() > 0.20 and abs(_dom - 64) < 8,
            "THE GEOMETRY REACHED THE RENDER: %s silhouette angular rms "
            "%.4f px at %.0f cycles/rev, dominant amplitude %.0f.  "
            "*** THE FLOOR IS A RECORDED READING, NOT ONE THIS ROW COMPUTES "
            "(F320): rev 74 read 0.0503 px / amplitude 4 on a frame of the "
            "ABLATED tree, which is NOT retained, so those two figures are "
            "STRING LITERALS here -- F198's shape.  This row computes only the "
            "AFTER side.  Re-derive the floor with one T1_TYRE_TREAD=0 render "
            "before quoting it. ***"
            % (os.path.basename(f), _res.std(), _dom, _F[_lo:_hi].max()))
    except Exception as _e:
        row("T6", None, "render-side row could not run: %s" % _e)
        ABSENT += 1

print("-" * 78)
print("  %d checked, %d FAILED%s%s"
      % (CHECK, len(FAIL), (", %d ABSENT" % ABSENT) if ABSENT else "",
         ("  --  " + ",".join(FAIL)) if FAIL else ""))
sys.exit(0 if not FAIL else 3)
