# probe_rev45_ground.py -- rev 45.  THE CONTACT SHADOW, MEASURED WHERE IT LIVES.
#
# `optics-6` HAS BEEN OPEN SINCE REV 12 AND HAS BEEN MEASURED THREE TIMES, EACH
# TIME SOMEWHERE THE SHADOW ISN'T.
#
#   rev 12  side ORTHO, T1_BGW=1.0: ground under the tyre 177.00 against open
#           ground 177.00 -- "the catcher contributes exactly nothing".
#   rev 17  matte tap: the alpha pool reaches 0.4980 and 19.1 % of the frame is
#           non-zero, so it is NOT nothing -- but only 0.0038 mean in the 4-30 px
#           band directly below the silhouette.  "A different symptom."
#   rev 44  no new measurement; the ledger carries rev 17's.
#
# WHAT IS WRONG WITH ALL THREE.  Two of them read a SIDE ORTHOGRAPHIC view.  In
# a side ortho the camera is level with the vehicle and the ground plane is
# edge-on, so "the band below the silhouette" is not ground at all -- it is the
# 3-4 px where the ground plane vanishes to a line.  There is no contact patch
# to see from there.  The third read a 400x300 matte where a tyre is 12 px wide.
#
# A contact shadow is a thing you look DOWN at.  So this probe measures it in
# `hero34f` -- the delivery frame, a raised three-quarter -- and it finds the
# ground by PROJECTING THE FOUR CONTACT PATCHES through the render camera
# rather than by typing a crop box.  Move a wheel and the sample follows it.
#
# WHAT IT REPORTS
#   G1  contact darkening   mean DN of the ground just in front of each
#                           CAMERA-SIDE contact patch, divided by OPEN GROUND
#                           in the same frame at the same viewing angle.  A
#                           real product render on a white sweep runs this WELL
#                           below 1.0.  Divided by the BACKDROP instead it came
#                           out above 1.0, which is nonsense -- see the code.
#   G3  under-body pool     mean DN of the ground BETWEEN the axles, under the
#                           body, over open ground.  This is what reads as
#                           "planted"; G1 is the tight contact darkening and
#                           the two move at very different rates.
#   G2  backdrop whiteness  mean DN of the far field.  SPEC sec.6 locks the
#                           backdrop to PURE WHITE and any rig change that
#                           buys a shadow by greying the sweep is REFUSED --
#                           that is exactly the trade rev 12 rejected when it
#                           tested T1_CATCH=0 and got a 166 grey with a hard
#                           horizon.
#
# CONTROLS -- read THIS PROBE'S OWN SUMMARY LINE, never its exit code.
#   C1  all four contact patches project inside the frame
#   NOTE: only the CAMERA-SIDE contacts are READ.  For the far-side wheels the
#       pixels below them are the vehicle's own underside -- see READABLE.
#   C2  the four samples are distinct -- no two annuli share a centre.  Without
#       it a projector returning one constant would pass C1 and G1 both.
#   C3  G2: the backdrop MARGINS are white -- mean AND 5th percentile, over the
#       full-height left and right edges, so a hard horizon anywhere in the
#       frame moves it.  THIS IS THE ONE THAT MUST NEVER GO AMBER: it is what
#       makes any shadow this probe reports honest rather than bought.  Its
#       first draft sampled only the top corners and passed on T1_CATCH=0's
#       horizon; see the control.
#   C4  KILL, WRITTEN TO FAIL AND EXPECTED TO FAIL FOREVER: open ground 4 m
#       off the vehicle must be IN FRAME and NOT darker than the far field.
#       Without it "there is a shadow" is untestable -- a uniformly dark frame
#       would satisfy G1.  The in-frame half is there because the first draft
#       sampled 10 m AHEAD, projected off-screen, and passed on "<no sample>".
#
# RUN
#   /tmp/blender/blender -b -P probe_rev45_ground.py
#   T1_PG_KEEP=1 keeps out/pg_hero34f.png.

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("T1_SUB", "1")
RX, RY = int(os.environ.get("T1_PG_RX", 1000)), int(os.environ.get("T1_PG_RY", 700))
os.environ["T1_PREVIEW"] = "hero34f"
os.environ["T1_PFX"] = "pg"
os.environ["T1_RX"], os.environ["T1_RY"] = str(RX), str(RY)
os.environ.setdefault("T1_SAMP", "48")

import bpy                                                   # noqa: E402
from mathutils import Vector                                 # noqa: E402
from bpy_extras.object_utils import world_to_camera_view     # noqa: E402
import runpy                                                 # noqa: E402
import numpy as np                                           # noqa: E402
from PIL import Image                                        # noqa: E402

CTL = {}


def ctl(name, ok, msg):
    CTL[name] = bool(ok)
    print("  [%s] %-4s %s" % ("PASS" if ok else "FAIL", name, msg))


G = runpy.run_path(os.path.join(HERE, "build.py"), run_name="__main__")
T = G["T"]

# The four contact patches, from the axle stations and tracks the build owns.
# Ground is z = 0 after step 8b, by construction -- RIDE_DROP is what puts it
# there -- so the patch is (x_axle, +-track/2, 0).  Nothing is typed.
PATCH = {
    "fl": Vector((T.X_AXLE_F, +T.TRACK_F / 2, 0.0)),
    "fr": Vector((T.X_AXLE_F, -T.TRACK_F / 2, 0.0)),
    "rl": Vector((T.X_AXLE_R, +T.TRACK_R / 2, 0.0)),
    "rr": Vector((T.X_AXLE_R, -T.TRACK_R / 2, 0.0)),
}
# C4's kill sample: open ground on the NEAR side, 4 m outboard of the front
# wheel.  The first two drafts put it 10 m ahead and then 4 m to the OFF side;
# both project off-screen in this framing and the control passed on "<no
# sample>", inert.  Near side is the side the camera is on.

PNG = os.path.join(HERE, "out", "pg_hero34f.png")
img = np.array(Image.open(PNG).convert("RGB")).astype(float)
H, W, _ = img.shape
sc, cam = bpy.context.scene, bpy.context.scene.camera


def project(v):
    c = world_to_camera_view(sc, cam, v)
    return c.x * W, (1.0 - c.y) * H


def ground_patch(u, v, tw, name=""):
    """Mean DN of the GROUND just in front of a contact patch.

    THE FIRST DRAFT OF THIS FUNCTION WAS AN ANNULUS AND IT WAS CONTAMINATED.
    It took a ring 1.5-4 tyre-widths around the contact point and kept
    "neutral" pixels, on the reasoning that the ground and backdrop are neutral
    and the body is not.  THE BODY IS.  The cream renders (192, 192, 188) --
    max minus min is 4, well inside any neutral threshold -- so the ring was
    sampling the vehicle's own flank and calling it ground.  It reported
    G1 = 0.8639, which is a real-looking number about the wrong pixels.

    A raised three-quarter camera sees unobstructed ground BELOW the contact
    point in screen space -- that is ground coming toward the lens.  So the
    sample is a rectangle starting half a tyre-width below the patch and
    running three tyre-widths further down, two wide.  No neutrality test is
    needed and none is applied: nothing else can be there.
    """
    # THE WINDOW IS 0.10 .. 0.85 TYRE-WIDTHS BELOW THE PATCH, AND THE FIRST
    # DRAFT'S 0.5 .. 3.5 WAS WRONG -- rule 8, a measurement's window is part of
    # the measurement.  Profiled in 0.25 TW steps out to 4.1 TW, the shipped
    # build reads
    #     fl  219 244 246 247 248 249 250 250 251 ...  against open ground 252
    #     rl  236 251 252 253 254 255 255 255 255 ...
    # so the whole contact shadow lives in the first ~0.35 TW (about 5 cm) and
    # the old window STARTED where it had already ended.  That is why G1 read
    # 0.9975 while a shadow was plainly there in the profile.
    y0 = int(v + 0.10 * tw); y1 = int(v + 0.85 * tw)
    x0 = int(u - 1.0 * tw); x1 = int(u + 1.0 * tw)
    y0, y1 = max(y0, 0), min(y1, H)
    x0, x1 = max(x0, 0), min(x1, W)
    if y1 - y0 < 4 or x1 - x0 < 4:
        return None, 0
    s = img[y0:y1, x0:x1]
    return float(s.mean()), int(s.shape[0] * s.shape[1])


# The tyre's projected width sets the annulus scale, so the sample follows the
# wheel if the wheel ever moves.  Two points one tyre-width apart, projected.
_a = project(Vector((T.X_AXLE_F, +T.TRACK_F / 2, 0.0)))
_b = project(Vector((T.X_AXLE_F, +T.TRACK_F / 2 + T.TIRE_W, 0.0)))
TW = max(((_a[0] - _b[0]) ** 2 + (_a[1] - _b[1]) ** 2) ** 0.5, 3.0)
print("  tyre width projects to %.1f px; annulus = %.1f .. %.1f px"
      % (TW, 1.5 * TW, 4.0 * TW))

# WHICH CONTACTS CAN BE READ AT ALL, and it is not all four.
# "The ground is below the contact patch in screen space" holds only for the
# wheels on the CAMERA'S OWN SIDE.  For the far-side wheels, the pixels below
# them are the vehicle's own underside -- measured, not argued: the first run
# read fl 253.81, fr 233.65, rl 254.89, rr 159.78, and 159.78 is the underbody,
# not a shadow.  Averaging all four produced G1 = 0.8844, which reads like a
# healthy contact shadow and is mostly one contaminated sample.
NEAR_SIGN = 1.0 if cam.location.y >= 0 else -1.0
READABLE = [k for k in ("fl", "fr", "rl", "rr")
            if (PATCH[k].y >= 0) == (NEAR_SIGN >= 0)]
# Candidates are tried in order and the FIRST that projects inside the frame is
# used; the chosen one is printed, so the control can never quietly go inert
# again.  A fixed point cannot work here -- the hero framing is set by
# fit_view() and moves whenever the subject's bbox does.
_FAR_CANDIDATES = [
    Vector((T.X_AXLE_F + 1.6, NEAR_SIGN * (T.TRACK_F / 2 + 1.1), 0.0)),
    Vector((T.X_AXLE_F + 0.9, NEAR_SIGN * (T.TRACK_F / 2 + 1.5), 0.0)),
    Vector((T.X_AXLE_F + 2.2, NEAR_SIGN * (T.TRACK_F / 2 + 0.6), 0.0)),
    Vector((T.X_AXLE_R - 1.2, NEAR_SIGN * (T.TRACK_R / 2 + 1.1), 0.0)),
]
FAR = _FAR_CANDIDATES[0]
FAR_NAME = "cand0"
print("  camera is on the %+.0fY side; readable contacts: %s"
      % (NEAR_SIGN, ", ".join(READABLE)))

PX = {k: project(v) for k, v in PATCH.items()}
for k, (u, v) in sorted(PX.items()):
    print("  contact %-3s -> px (%6.1f, %6.1f)" % (k, u, v))

inside = all(0 <= u < W and 0 <= v < H for u, v in PX.values())
ctl("C1", inside, "all four contact patches project inside the %dx%d frame" % (W, H))

uniq = len({(round(u), round(v)) for u, v in PX.values()})
ctl("C2", uniq == 4, "the four patches are %d distinct pixels (want 4)" % uniq)

# G2 -- THE BACKDROP, AND THE FIRST DRAFT OF THIS CONTROL WAS BLIND.
#
# It sampled the frame's top two corners only, on the reasoning that those are
# backdrop in every hero framing this project uses.  They are -- and that is
# exactly why it could not see the defect.  Run against T1_CATCH=0, which
# renders the cyclorama as a real lit surface, C3 reported "255.00, PURE WHITE"
# while the frame carried a HARD HORIZON LINE across it and a grey sweep
# filling the lower two-thirds.  The horizon sits about 18 % down; the corners
# are above it.  THE CONTROL PASSED ON THE DEFECT IT EXISTS TO CATCH -- the
# third time this revision (SPEC 10.111.2, 10.115.4).
#
# It now samples the full-height left and right margins, which cross the
# horizon wherever it falls, and it reports the 5th PERCENTILE as well as the
# mean.  A hard horizon moves the percentile long before it moves the mean.
# AND THE STATISTIC IS A STEP, NOT A LEVEL.  The second draft tested the
# margins' mean and 5th percentile against 254 and FAILED THE SHIPPED BUILD at
# 253.92 / 247.00 -- correctly, in the sense that those pixels really are below
# white, but for the wrong reason: it was catching the vehicle's OWN soft
# shadow pool reaching the left margin, which is a thing we want.  Loosening
# the threshold until the shipped build passed would have been laundering.
#
# What SPEC sec.6 forbids is a SWEEP -- a horizon, a hard edge across the
# frame.  A horizon is a STEP in the margin's vertical profile; a soft shadow
# pool and the deliberate one-code-value vignette are not.  So C3 tests the
# largest row-to-row step in the margin, and reports the level alongside it
# without gating on it.
_mw = max(int(0.07 * W), 6)
_marg = np.concatenate([img[:int(0.92 * H), 0:_mw], img[:int(0.92 * H), W - _mw:]],
                       axis=1)
# THE LEVEL AND THE STEP COME FROM DIFFERENT WINDOWS, ON PURPOSE.
# The level must be read where backdrop is the ONLY thing that can be present,
# or a deeper contact shadow -- the thing we are trying to buy -- lowers it and
# the control fires on its own success.  The upper 55 % of the margins is above
# the ground plane entirely in every hero framing this project uses.  The STEP
# is still taken over the full height, because a horizon can fall anywhere.
far = float(_marg[:int(0.55 * _marg.shape[0])].mean())
_rows = _marg.mean(axis=(1, 2))
_rows = np.convolve(_rows, np.ones(5) / 5.0, mode="valid")     # 5-row smooth
_step = float(np.abs(np.diff(_rows)).max())
far_p5 = float(np.percentile(_marg.reshape(-1, 3).mean(1), 5))
print("  G2 margins: mean %.2f  5th pct %.2f  max row-to-row STEP %.3f DN"
      % (far, far_p5, _step))

ctl("C3", _step < 1.5 and far >= 254.0,
    "G2 no horizon in the backdrop: max row step %.3f DN (< 1.5), margin mean "
    "%.2f DN (>= 254, and read in the UPPER margins where nothing but backdrop "
    "can be).  SPEC sec.6 locks the backdrop to PURE WHITE.  Watched "
    "print: shipped 0.100 / 253.92; T1_CATCH=0 22.123 / 142.49 -- a 220x step, "
    "which is the horizon rev 12 refused and rev 45 refuses again."
    % (_step, far))

# THE REFERENCE FOR G1 IS OPEN GROUND, NOT THE BACKDROP.  The first two drafts
# divided by the backdrop's mean and G1 came out at 1.0017 -- above one, which
# is nonsense for a "darkening".  The backdrop is the sweep seen edge-on and
# far away; the ground beside the vehicle is the same surface seen from the
# same angle as the contact patches.  Dividing like by like is the whole point
# of a dimensionless measure (rule 14).
#
# The candidates are tried in order and the FIRST that projects inside the
# frame is used; the chosen one is printed, so this can never quietly go inert.
# A fixed point cannot work -- the hero framing is set by fit_view() and moves
# whenever the subject's bbox does.
mk = None
for _i, _c in enumerate(_FAR_CANDIDATES):
    _u, _v = project(_c)
    if not (0 <= _u < W and 0 <= _v < H):
        continue
    _m, _n = ground_patch(_u, _v, TW, "open")
    if _m is not None:
        FAR, FAR_NAME, mk, uk, vk = _c, "cand%d" % _i, _m, _u, _v
        break
if mk is None:
    print("  OPEN-GROUND REFERENCE: none of %d candidates is in frame"
          % len(_FAR_CANDIDATES))
    OPEN = far
else:
    OPEN = mk
    print("  open-ground reference: %s at world %s -> px (%.1f, %.1f) = %.2f DN"
          % (FAR_NAME, tuple(round(t, 2) for t in FAR), uk, vk, mk))

vals = []
for k in READABLE:
    u, v = PX[k]
    m, n = ground_patch(u, v, TW, k)
    if m is not None:
        vals.append(m)
        print("  ground below %-3s  %.2f DN over %d px   (%.4f of open ground)"
              % (k, m, n, m / OPEN))
    else:
        print("  ground below %-3s  sample fell outside the frame" % k)
# A PROFILE, PRINTED, BECAUSE A WINDOW IS PART OF A MEASUREMENT (rule 8).
# The first window was 0.5 .. 3.5 tyre-widths below the contact patch -- 8 to
# 54 cm of ground -- and a contact shadow lives in the first 5.  Rather than
# pick a second window by eye, walk out from the patch and print what is there.
for k in READABLE:
    u, v = PX[k]
    prof = []
    for j in range(16):
        f0, f1 = 0.10 + 0.25 * j, 0.10 + 0.25 * (j + 1)
        y0, y1 = int(v + f0 * TW), int(v + f1 * TW)
        x0, x1 = int(u - 1.0 * TW), int(u + 1.0 * TW)
        y0, y1 = max(y0, 0), min(max(y1, y0 + 1), H)
        x0, x1 = max(x0, 0), min(x1, W)
        prof.append(float(img[y0:y1, x0:x1].mean()) if (y1 > y0 and x1 > x0) else float("nan"))
    print("  profile %-3s (0.1..4.1 TW below, 0.25 TW steps): %s"
          % (k, " ".join("%.0f" % t for t in prof)))

# G3 -- THE UNDER-BODY POOL, which is what actually reads as "planted".
# G1's window is 0.10-0.85 tyre-widths at the camera-side contacts and it
# measures the TIGHT contact darkening.  The A/B at T1_SHADOW 1.0 vs 3.2 moved
# G1 only 0.9756 -> 0.9493 while the render went from floating to planted,
# because the visible change is the BROAD pool under the body between the
# axles.  Two different things; both are reported.
_mid_u = (PX[READABLE[0]][0] + PX[READABLE[-1]][0]) / 2.0
_mid_v = (PX[READABLE[0]][1] + PX[READABLE[-1]][1]) / 2.0
_gy0, _gy1 = int(_mid_v - 1.0 * TW), int(_mid_v + 1.5 * TW)
_gx0, _gx1 = int(min(PX[k][0] for k in READABLE)), int(max(PX[k][0] for k in READABLE))
_gy0, _gy1 = max(_gy0, 0), min(_gy1, H)
_gx0, _gx1 = max(_gx0, 0), min(_gx1, W)
G3 = (float(img[_gy0:_gy1, _gx0:_gx1].mean()) / OPEN
      if (_gy1 > _gy0 and _gx1 > _gx0) else 1.0)
print("  G3 UNDER-BODY POOL = %.4f of open ground over %dx%d px"
      % (G3, _gx1 - _gx0, _gy1 - _gy0))

# ---------------------------------------------------------------------------
# G4 -- THE CAVITY FLOOR.  rev 60, F67 / item D.
#
# G3 above averages a 193 x 50 px box that is MOSTLY OPEN FLOOR, so it dilutes
# the very thing item D built: the dark band under the sill.  ON THIS PROBE'S
# OWN FRAME, ablation against built:
#
#     T1_NOUNDER=1   G3 0.8375   G4 0.5475
#     built          G3 0.7714   G4 0.2519
#
# G3 moves by 0.066, G4 by 0.296.  Every one of those four was watched print.
# (An independent window on the 1600x1100 `hero` -- a different camera and a
# different scale -- reads the same band 0.545 -> 0.219, which is why G4 is
# quoted to two figures and not three.)  Both are reported; this is the one
# that tracks the geometry.
#
# THE WINDOW IS LOCATED FROM THIS PROBE'S OWN PROJECTED CONTACT PATCHES, not
# typed: a column band about the midpoint of the two camera-side contacts,
# walked UP from the contact row.  The minimum along that walk is the cavity
# floor.  Nothing here goes stale when a camera or a constant moves.
#
# THE PHOTOGRAPH: the same profile down `ref_side.jpg` at cols 350-500 --
# between the wheels, clear of both -- reads a floor of 8.0 DN against an open
# plateau of 139.0, i.e. 0.057.  THAT IS A SUNLIT OUTDOOR FRAME AND THIS IS A
# WHITE CYCLORAMA, so it is a DIRECTION, not a bar (rule 6): the owner ruled
# "keep studio, fix the model" and a white floor under a 13 x 8.5 m softbox
# fills a 90 mm cavity from every side.  C5 is therefore armed at the
# ABLATION, which is a render-against-render test and free of that caveat.
# THE FIRST CUT OF THIS WINDOW WAS WRONG AND IT PRINTED 0.3134, WHICH IS A
# BELIEVABLE NUMBER ABOUT THE WRONG PIXELS.  It walked up from
# `min(PX[k][1])` -- the SMALLEST row among the contact patches, i.e. the
# farthest one on screen, not the ground line at mid-span -- and the band
# landed on the RED FLANK across the "Tacombi" lettering.  Its minimum was the
# dark of a letter stroke.  PAINTED AND LOOKED AT, which is the only reason it
# was caught (rule 8).
#
# THE WINDOW NOW: a column band at the mid-span of the camera-side contacts,
# from their MEAN row (the ground line under the sill) up by 2.6 tyre widths.
# The cavity and the flank are separated by CHROMA, not by height: the cavity
# is neutral, the flank is saturated red, so only near-neutral rows are
# eligible.  The silver lettering is neutral too and survives the filter --
# and it does not matter, because it is BRIGHT and this takes a MINIMUM.
_cx = int((PX[READABLE[0]][0] + PX[READABLE[-1]][0]) / 2.0)
_c0, _c1 = max(_cx - 30, 0), min(_cx + 30, W)
_grow = sum(PX[k][1] for k in READABLE) / len(READABLE)
_ctop = max(int(_grow - 2.6 * TW), 0)
_cbot = min(int(_grow - 0.10 * TW), H)
G4, _g4row = 1.0, -1
if _cbot > _ctop and _c1 > _c0:
    _rows = img[_ctop:_cbot, _c0:_c1].mean(axis=1)          # (n, 3)
    _mx = _rows.max(axis=1); _mn = _rows.min(axis=1)
    _neutral = (_mx - _mn) / np.maximum(_mx, 1.0) < 0.15
    _lum = _rows.mean(axis=1)
    if _neutral.any():
        _cand = np.where(_neutral)[0]
        _k = _cand[int(_lum[_cand].argmin())]
        G4, _g4row = float(_lum[_k]) / OPEN, _ctop + int(_k)
print("  G4 CAVITY FLOOR = %.4f of open ground (min %.1f DN at row %d, "
      "cols %d-%d)  -- photograph ref_side.jpg 0.057, a DIRECTION not a bar"
      % (G4, G4 * OPEN, _g4row, _c0, _c1))
ctl("C5", G4 < 0.45,
    "G4: there IS a cavity under the sill.  Armed at the ABLATION, which is "
    "render-against-render and so free of the studio caveat: T1_NOUNDER=1 "
    "must fail this row and the built vehicle must pass it")
if os.environ.get("T1_PG_PAINT"):
    _pi = img.copy()
    _pi[_ctop:_cbot, _c0:_c1] = 0.45 * _pi[_ctop:_cbot, _c0:_c1] + 0.55 * np.array([255, 0, 255])
    if _g4row >= 0:
        _pi[_g4row, _c0:_c1] = np.array([0, 255, 255])
    Image.fromarray(_pi.astype(np.uint8)).save(
        os.path.join(HERE, "out", "pg_g4_window.png"))
    print("  G4 window PAINTED -> out/pg_g4_window.png  (rule 8: look at it)")

G1 = (sum(vals) / len(vals) / OPEN) if vals else 1.0
print("  G1 CONTACT DARKENING = %.4f of OPEN GROUND   (1.0000 = the vehicle "
      "floats)" % G1)

kill_dark = (mk is not None) and (mk < far - 3.0)
ctl("C4", (mk is not None) and not kill_dark,
    "KILL: open ground reads %s against the backdrop's %.2f -- it must be IN "
    "FRAME (a '<no sample>' passes trivially) and NOT dark (a uniformly dark "
    "frame would satisfy G1)"
    % (("%.2f" % mk) if mk is not None else "<no sample, CONTROL IS INERT>", far))

if not os.environ.get("T1_PG_KEEP"):
    try:
        os.remove(PNG)
    except OSError:
        pass

nfail = sum(1 for v in CTL.values() if not v)
print("G1=%.4f  G2=%.2f  G3=%.4f  G4=%.4f" % (G1, far, G3, G4))
print("CONTROLS: %d checked, %d FAILED%s"
      % (len(CTL), nfail,
         "" if not nfail else " -- " + ",".join(k for k, v in CTL.items() if not v)))
