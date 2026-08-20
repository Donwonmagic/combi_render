# probe_rev45_paint.py -- rev 45.  THE PAINT, AGAINST HIS OWN PHOTOGRAPHS.
#
# WHAT IT IS FOR
#   Ledger finding 38 says the body red renders 3.5 sigma too pale and that the
#   cause is the studio rather than the albedo.  That measurement was made once,
#   by hand, in a scratch directory.  A finding measured once by hand is a
#   finding that will be re-litigated; this makes it repeatable and guards it.
#
# THE MEASUREMENT, AND WHY IT IS THE RIGHT SHAPE
#   Every quantity here is a paint's chroma NORMALISED TO THE CREAM IN THE SAME
#   FRAME.  That is a von-Kries normalisation and it cancels BOTH the exposure
#   and the illuminant's colour, so a render under studio strobes and a phone
#   snapshot under Mexican afternoon sun become comparable without any white
#   balance being assumed.  Rule 14: prefer dimensionless measurements.
#
#   Sample points are PROJECTED 3-D LANDMARKS, not typed crop boxes -- the same
#   technique as probe_rev45_nose, PLUS the half that probe does not have: each
#   candidate is raycast from the camera and discarded unless the ray reaches
#   IT first.  Projection is not visibility.  A body point is placed on the
#   skin by t1_core.flank_y so it follows the loft; a hubcap point off the axle
#   station and the track so it follows the wheel.
#
# WHAT IT REPORTS, and the photographed target beside each
#   P1  body red      G/R of (red / cream).   built 0.455 at rev 45's baseline
#                     against 0.223 +- 0.066 over FOUR frames -- 3.5 sigma.
#                     THE ALBEDO IS NOT THE DEFECT: t1_mats.RED is
#                     sRGB(196,49,36), G/R 0.250, which is 0.4 sigma from the
#                     photographed mean.  A five-arm ablation puts about half
#                     the excess on the white cyclorama's own specular.
#   P2  hubcap red    G/R of (cap / cream).   photographed 0.274 +- 0.096 over
#                     three frames.
#   P3  cream warmth  (R-B)/G of the cream.   photographed 0.037 +- 0.013 over
#                     the three warm frames; ref_nolita_front34 is cool indoor
#                     light and reads -0.018, and is excluded and SAID so.
#
# CONTROLS -- read THIS PROBE'S OWN SUMMARY LINE, never its exit code.
#   C1  every quantity keeps at least three candidate points that are in frame,
#       VISIBLE (the camera's ray reaches them before anything else) and
#       correctly classified.  A collapsing survivor count is itself a finding.
#   C2  the three sampled colours are distinct
#   C3  P3 cream warmth within 3 sigma of the photographed 0.037 +- 0.013
#   C4  KILL, WRITTEN TO FAIL AND EXPECTED TO FAIL FOREVER: a landmark placed
#       outboard of the flank -- open backdrop -- must be IN FRAME and must NOT
#       satisfy the
#       "this is red paint" test.  Without it, C1 and P1 are both untestable:
#       a projector returning a constant, or a sampler reading white, would
#       pass everything.
#
#   P1 AND P2 ARE REPORTED, NOT GATED, AND THAT IS DELIBERATE.  Finding 38 is
#   an OPEN question for the owner (Q6 of rev45_ba.png): softening the studio
#   would move the paint toward his photographs and would trade the
#   catalogue-clean white background he supplied as the bar.  Gating on a number
#   whose fix has not been sanctioned would turn a question into a fait
#   accompli.  When he answers, the gate goes in here.
#
# RUN
#   /tmp/blender/blender -b -P probe_rev45_paint.py
#   T1_PP_KEEP=1 keeps out/pp_hero34f.png.

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("T1_SUB", "1")
RX, RY = int(os.environ.get("T1_PP_RX", 1000)), int(os.environ.get("T1_PP_RY", 700))
os.environ["T1_PREVIEW"] = "hero34f"
os.environ["T1_PFX"] = "pp"
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

PNG = os.path.join(HERE, "out", "pp_hero34f.png")
img = np.array(Image.open(PNG).convert("RGB")).astype(float)
H, W, _ = img.shape
sc, cam = bpy.context.scene, bpy.context.scene.camera
NEAR = 1.0 if cam.location.y >= 0 else -1.0


def project(v):
    c = world_to_camera_view(sc, cam, v)
    return c.x * W, (1.0 - c.y) * H


def on_skin(x, z, out=0.010):
    """A point just proud of the flank at (x, z), on the camera's side.
    t1_core.flank_y is the loft's own half-width, so this follows the body."""
    return Vector((x, NEAR * (T.flank_y(x, z) + out), z - T.rake_drop(x)))


# A POPULATION, NOT A POINT -- and the first draft's three points were all
# wrong in a way a single point can always be wrong.  Their visibility raycasts
# came back:
#     red    first hit 'script_L'   the "Senor Tacombi" decal, 17 mm nearer
#     cream  first hit 'fringe2'    the bobble fringe, 3 mm nearer
#     cap    first hit 'cap1.31'    the cap's own rim, 36 mm nearer
# Three for three.  A flank carrying folk art, a script lockup, a decal and a
# fringe has very little clean paint left, and picking one point on it by hand
# is picking a lottery ticket.
#
# So each quantity is sampled over a GRID of candidate world points.  A
# candidate is kept only if (a) the camera's ray reaches it first and (b) the
# pixel there classifies as the material we asked for.  The reported value is
# the MEDIAN of the survivors, and the survivor count is printed -- a count
# that collapses is itself a finding.
def _grid(xs, zs, out=0.010):
    return [on_skin(x, z, out) for x in xs for z in zs]


CAND = {
    # lower flank, aft of the folk art and clear of the script's box
    "red":   _grid([-1.60, -1.45, -1.30, 0.62, 0.78, 0.94], [0.66, 0.74, 0.82, 0.90]),
    # upper body between the glazing and the drip rail
    "cream": _grid([-1.62, -1.48, 1.42, 1.58, 1.72], [1.56, 1.64, 1.72]),
}
# the hubcap's domed face, sampled across it rather than at one point
CAND["cap"] = [Vector((T.X_AXLE_F + dx,
                       NEAR * (T.TRACK_F / 2 + T.TIRE_W * 0.55),
                       T.TIRE_R + dz - T.rake_drop(T.X_AXLE_F)))
               for dx in (-0.05, -0.025, 0.0, 0.025, 0.05)
               for dz in (-0.05, -0.025, 0.0, 0.025, 0.05)]

# C4's KILL.  The first draft put it 3 m outboard of the flank and it projected
# OFF FRAME, so the control returned "<off frame>" and PASSED -- inert, the
# same defect recorded at C8 in probe_rev45_nose and C4 in probe_rev45_ground.
# Three inert kill controls in one revision.  Candidates are tried in order and
# the first IN-FRAME one is used; the control fails outright if none is.
_KILL_CANDIDATES = [on_skin(-0.35, 0.78, out=o) for o in (0.55, 0.85, 1.20, 1.60)]

KILL, PXK = None, None
for _c in _KILL_CANDIDATES:
    _u, _v = project(_c)
    if 0 <= _u < W and 0 <= _v < H:
        KILL, PXK = _c, (_u, _v)
        break


def visible(v3, tol=0.030):
    """Is this 3-D point the FIRST thing the camera meets along its own ray?

    PROJECTION IS NOT VISIBILITY, AND THE FIRST DRAFT OF THIS PROBE CONFUSED
    THEM.  world_to_camera_view maps any point to a pixel whether or not the
    point can be seen.  Every landmark this probe first chose was behind
    something -- a decal, a fringe, the cap's own rim -- and every number
    downstream was about the wrong surface.

    This is the visibility half of the landmark technique, and
    probe_rev45_nose does NOT yet have it: its landmarks are on the nose, which
    nothing overhangs, so it is correct today by luck of geometry rather than
    by test.  Recorded there.
    """
    org = cam.matrix_world.translation
    d = (v3 - org)
    d = d.normalized()
    dg = bpy.context.evaluated_depsgraph_get()
    hit, loc, _n, _i, _ob, _m = bpy.context.scene.ray_cast(dg, org + d * 1e-4, d)
    if not hit:
        return False, None
    return ((loc - v3).length <= tol), (_ob.name if _ob else None)


def patch(u, v, r=4):
    u0, v0 = int(round(u)), int(round(v))
    y0, y1 = max(v0 - r, 0), min(v0 + r + 1, H)
    x0, x1 = max(u0 - r, 0), min(u0 + r + 1, W)
    if y1 <= y0 or x1 <= x0:
        return None
    return np.median(img[y0:y1, x0:x1].reshape(-1, 3), 0)


def is_red_paint(p):
    return p is not None and (p[0] - p[1]) > 0.25 * max(p[0], 1.0) and p[0] > 40


def is_cream(p):
    return (p is not None and (p.max() - p.min()) < 0.10 * max(p.max(), 1.0)
            and 90 < p.mean() < 249)


CLASSIFY = {"red": is_red_paint, "cream": is_cream, "cap": is_red_paint}
S, NKEPT = {}, {}
for k, cands in CAND.items():
    keep = []
    for c in cands:
        u, v = project(c)
        if not (0 <= u < W and 0 <= v < H):
            continue
        ok, _ob = visible(c)
        if not ok:
            continue
        p = patch(u, v)
        if p is not None and CLASSIFY[k](p):
            keep.append(p)
    NKEPT[k] = len(keep)
    S[k] = np.median(np.array(keep), axis=0) if keep else None
    print("  %-6s %2d of %2d candidates visible AND classified -> RGB %s"
          % (k, len(keep), len(cands), S[k].round(1) if S[k] is not None else None))

ctl("C1", all(NKEPT[k] >= 3 for k in CAND),
    "every quantity keeps >= 3 candidates that are IN FRAME, VISIBLE (the "
    "camera's ray reaches them first) and correctly classified: %s"
    % ", ".join("%s %d" % (k, NKEPT[k]) for k in sorted(NKEPT)))

ctl("C2", len({tuple(S[k]) for k in CAND if S[k] is not None}) == len(CAND),
    "the %d sampled colours are distinct -- a sampler returning one constant "
    "would pass C1" % len(CAND))

cream = S["cream"]
P1 = P2 = P3 = float("nan")
if cream is not None and cream.min() > 1:
    if S["red"] is not None:
        k = S["red"] / cream
        P1 = float(k[1] / k[0])
    if S["cap"] is not None:
        k = S["cap"] / cream
        P2 = float(k[1] / k[0])
    P3 = float((cream[0] - cream[2]) / cream[1])

print("  P1 BODY RED   G/R of red/cream = %.3f   photographed 0.223 +- 0.066 "
      "(4 frames)   albedo sRGB(196,49,36) = 0.250" % P1)
print("  P2 HUBCAP RED G/R of cap/cream = %.3f   photographed 0.274 +- 0.096 "
      "(3 frames)" % P2)
print("  P3 CREAM WARM (R-B)/G          = %+.4f  photographed +0.037 +- 0.013 "
      "(3 warm frames; ref_nolita_front34 is cool indoor light at -0.018 and "
      "is excluded)" % P3)

ctl("C3", abs(P3 - 0.037) < 3 * 0.013 + 0.010,
    "P3 cream warmth %+.4f is within 3 sigma of the photographed +0.037" % P3)

kp = patch(*PXK) if PXK else None
ctl("C4", PXK is not None and not is_red_paint(kp),
    "KILL: a landmark 3 m outboard of the flank samples %s and must NOT read "
    "as red paint (a projector returning a constant would pass C1 and P1 both). "
    "It MUST be in frame: an off-frame kill passes trivially."
    % (kp.round(1) if kp is not None else "<NO IN-FRAME CANDIDATE, INERT>"))

if not os.environ.get("T1_PP_KEEP"):
    try:
        os.remove(PNG)
    except OSError:
        pass

nfail = sum(1 for v in CTL.values() if not v)
print("P1=%.3f  P2=%.3f  P3=%+.4f" % (P1, P2, P3))
print("CONTROLS: %d checked, %d FAILED%s"
      % (len(CTL), nfail,
         "" if not nfail else " -- " + ",".join(k for k, v in CTL.items() if not v)))
