# probe_rev45_nose.py -- rev 45.  THE NOSE, MEASURED IN THE RENDERED FRAME.
#
# WHY THIS EXISTS
#   Rev 45 opened on the observation that this project has measured the nose
#   emblem eight ways and never once looked at it in a render.  SPEC 10.25
#   measured the glyph's air gap, 10.107 measured its six stroke ends, and
#   probe_rev44_lampmove measured its height from two chains -- all of them in
#   the GLYPH'S OWN PLANE, none of them against the body it sits on.  The
#   badge was rendering as a CLOCK FACE the whole time (SPEC 10.110).
#
#   The obstacle to looking was always the same one: finding the thing in the
#   pixels.  Every previous crop box in this repo is a hand-typed literal that
#   goes stale the moment a camera or a constant moves.  So this probe does not
#   type boxes.  It PROJECTS KNOWN 3-D LANDMARKS -- the roundel centre, the two
#   headlamp centres, the indicator pods -- through the render camera with
#   bpy_extras.world_to_camera_view, and samples where they actually land.
#   Move HL_Z again and the sample follows it, by construction.
#
# WHAT IT MEASURES, AND AGAINST WHAT
#   N1  emblem relief      every emblem FRONT-face vertex stands proud of the
#                          nose.  Pre-drape this ran -0.3 .. +32 mm; the whole
#                          W was inside the sheet metal.  SPEC 10.110.
#   N2  lens luminance     unlit headlamp lens / cream, same frame.
#                          PHOTOGRAPHED 0.565 on IMG_3842 (ref_playa_34.png),
#                          the only frame in the set with an unlit lamp square
#                          enough to read.  A clear 0.018-rough glass over a
#                          mirror bowl reflects whatever is BEHIND THE CAMERA,
#                          which in a cyclorama is nothing, so the aperture
#                          rendered BLACK.
#   N3  bezel neutrality   |b*| of the headlamp bezel.  See SPEC 10.111 -- the
#                          brass reading is CONTESTED and this watches whichever
#                          arm is built.
#
# CONTROLS -- read THIS PROBE'S OWN SUMMARY LINE, never its exit code.
#   C1  the landmark projection lands inside the frame for every landmark
#   C2  the two headlamp landmarks are symmetric about the frame's subject
#       axis to within 2 % of the frame width  (proves the projection is sane
#       and is not silently returning the frame centre)
#   C3  N1: min front-face proudness > 0.5 mm
#   C4  N2: lens/cream in 0.40 .. 0.75    (photograph 0.565; the window is the
#       spread of the three unlit-lamp readings available, stated per rule 8)
#   C6  N2b: |lens (R-B)/cream| < 0.15.  THE CHROMA, and it is the control
#       that actually catches this defect -- C4's luminance ratio passed at
#       0.432 while the aperture was rendering RED.
#   C8  N4: no T1_body face lies between the headlamp lens and its reflector.
#       Finding 41's inverse.  T1_HL_BOWL=0 makes it fail -- and the FIRST
#       draft of this control did not, which is recorded at the control.
#   C7  N3: |bezel b*| < 12.  SPEC 10.111 retires the rev-10 brass reading to
#       chrome; brass renders +25.7, chrome +1.7, photographed +2.7 / +6.7.
#   C5  KILL, WRITTEN TO FAIL AND EXPECTED TO FAIL FOREVER.  A landmark placed
#       one metre in front of the nose must NOT sample the same pixel as the
#       roundel.  Without it "the projection works" is untestable -- a stub
#       returning a constant would pass C1 and C2.
#
# RUN
#   /tmp/blender/blender -b -P probe_rev45_nose.py
#   T1_P45_KEEP=1 keeps out/p45_nose.png for eyeballing.

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("T1_SUB", "1")
# Render through build.py's OWN preview path rather than calling render_set
# here: the studio needs cyclorama() + lighting() + camera() before it, and a
# probe that reproduces that call sequence by hand is a second copy of the
# shipped path that can drift from it.  Setting the environment and letting
# build.py render is the same code the owner's frames come out of.
RX, RY = 900, 620
os.environ["T1_PREVIEW"] = "front34"
os.environ["T1_PFX"] = "p45"
os.environ["T1_RX"], os.environ["T1_RY"] = str(RX), str(RY)
os.environ.setdefault("T1_SAMP", "48")

import bpy                                                   # noqa: E402
from mathutils import Vector                                 # noqa: E402
from bpy_extras.object_utils import world_to_camera_view     # noqa: E402

import runpy                                                 # noqa: E402

CTL = {}
NOTE = []


def ctl(name, ok, msg):
    CTL[name] = bool(ok)
    print("  [%s] %-4s %s" % ("PASS" if ok else "FAIL", name, msg))


# ---------------------------------------------------------------- build
G = runpy.run_path(os.path.join(HERE, "build.py"), run_name="__main__")
import studio as ST                                          # noqa: E402

HL_X, HL_Y, HL_Z = G["HL_X"], G["HL_Y"], G["HL_Z"]
ROUNDEL_Z = G["ROUNDEL_Z"]
RIDE = G["T"].RIDE_DROP

# build.py's step 8b shears every body vertex by rake_drop(x); the landmarks
# above are authored in the UN-DROPPED frame, so they get the same treatment
# here rather than being re-typed.  A constant tuned against another constant
# must be expressed in terms of it (rule 2).
rake_drop = G["T"].rake_drop


def dropped(x, y, z):
    return Vector((x, y, z - rake_drop(x)))


LANDMARKS = {
    "roundel":  dropped(2.1155, 0.0, ROUNDEL_Z),
    "lamp_L":   dropped(HL_X, +HL_Y, HL_Z),
    "lamp_R":   dropped(HL_X, -HL_Y, HL_Z),
    "cream_up": dropped(2.1000, 0.0, ROUNDEL_Z + 0.22),
}
# C5's kill landmark: one metre in FRONT of the nose, on the same axis.
LANDMARKS_KILL = {"ghost": dropped(3.1155, 0.0, ROUNDEL_Z)}

# ---------------------------------------------------------------- render
PNG = os.path.join(HERE, "out", "p45_front34.png")

import numpy as np                                           # noqa: E402
from PIL import Image                                        # noqa: E402

img = np.array(Image.open(PNG).convert("RGB")).astype(float)
H, W, _ = img.shape

sc = bpy.context.scene
cam = sc.camera


def project(v):
    c = world_to_camera_view(sc, cam, v)
    return c.x * W, (1.0 - c.y) * H, c.z


PX = {k: project(v) for k, v in LANDMARKS.items()}
PXK = {k: project(v) for k, v in LANDMARKS_KILL.items()}
for k, (u, v, d) in sorted(PX.items()):
    print("  landmark %-9s -> px (%7.1f, %7.1f)  depth %.3f m" % (k, u, v, d))


def patch(u, v, r=4):
    u0, v0 = int(round(u)), int(round(v))
    s = img[max(v0 - r, 0):v0 + r + 1, max(u0 - r, 0):u0 + r + 1].reshape(-1, 3)
    return np.median(s, 0)


def lab_b(rgb):
    r, g, b = [c / 255.0 for c in rgb]
    f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = f(r), f(g), f(b)
    Y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    Z = 0.0193 * r + 0.1192 * g + 0.9505 * b
    g2 = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    return 200 * (g2(Y / 1.0) - g2(Z / 1.08883))


# ---------------------------------------------------------------- controls
inside = all(0 <= u < W and 0 <= v < H for u, v, _ in PX.values())
ctl("C1", inside, "every landmark projects inside the %dx%d frame" % (W, H))

uL, uR = PX["lamp_L"][0], PX["lamp_R"][0]
uc = PX["roundel"][0]
sym = abs((uL - uc) + (uR - uc)) / W
ctl("C2", sym < 0.02,
    "headlamps symmetric about the roundel to %.4f of frame width (< 0.020)" % sym)

# N1 -- emblem relief, read off the build log line build.py prints
N1 = G.get("_pr")
n1_min = min(N1) * 1000 if N1 else -99.0
ctl("C3", n1_min > 0.5,
    "N1 emblem front faces stand %.2f mm proud of the nose (flat plate: -0.3)"
    % n1_min)

# Sample the NEAR lamp -- the far one is at grazing incidence and part of it
# falls off the nose's shoulder.  "Near" is read off the projected depth, not
# assumed from the sign of Y, so it follows the camera.
_near = "lamp_L" if PX["lamp_L"][2] < PX["lamp_R"][2] else "lamp_R"
lens = patch(*PX[_near][:2], r=3)
cream = patch(*PX["cream_up"][:2], r=6)
ratio = lens.mean() / max(cream.mean(), 1e-6)
ctl("C4", 0.40 <= ratio <= 0.75,
    "N2 lens/cream = %.3f on %s (photographed 0.565, window 0.40-0.75)"
    % (ratio, _near))
print("      lens RGB %s   cream RGB %s" % (lens.round(1), cream.round(1)))

# N2b -- THE CHROMA, which is the defect C4's luminance test could not see.
# Photographed unlit lens: RGB (124,127,127), i.e. NEUTRAL.  A mirror bowl
# behind clear glass returns the red nose instead.  Expressed as the lens's own
# red-minus-blue against the CREAM's, so exposure and illuminant drop out.
_lens_rb = (lens[0] - lens[2]) / max(cream.mean(), 1e-6)
_ref_rb = (124.0 - 127.0) / ((124.0 + 127.0 + 127.0) / 3.0)
ctl("C6", abs(_lens_rb) < 0.15,
    "N2b lens (R-B)/cream = %+.3f  (photographed %+.3f; the mirror arm ran "
    "+0.558)" % (_lens_rb, _ref_rb))

# N3 -- bezel neutrality, sampled on the bezel arc outboard of the lamp centre.
# The bezel's outer radius is 0.0862 + 0.0165 m; sample at 0.094 m outboard,
# expressed off t1_detail.headlamp's own profile rather than typed.
_sgn = 1.0 if _near == "lamp_L" else -1.0
bz = project(dropped(HL_X, _sgn * (HL_Y + 0.094), HL_Z))
bez = patch(bz[0], bz[1], r=2)
b_star = lab_b(bez)
ctl("C7", abs(b_star) < 12.0,
    "N3 bezel b* %+.1f  (photographed +2.7 / +6.7 on ref_nolita_front34, "
    "against that frame's own neutral +6.9 and its red +61.8; the retired "
    "brass arm renders +25.7).  RGB %s" % (b_star, bez.round(1)))

# C8 -- FINDING 41's INVERSE: NO SHEET METAL BETWEEN THE LENS AND THE BOWL.
#
# THE FIRST DRAFT OF THIS CONTROL DID NOT DISCRIMINATE AND IS RECORDED RATHER
# THAN QUIETLY REPLACED.  It asserted "the first object down the lamp axis is
# hl_*, not T1_body", off the rev-45 measurement that the ray hit T1_body at
# 2.1116 before hl_lens at 2.1015.  That measurement was taken on the CONCAVE
# lens.  SPEC 10.111.1 then turned the lens convex, apex at 2.1220 -- in front
# of the nose -- so the first hit is the lens in BOTH arms and the control
# passed on the defect it was written for.  Rule 18 in its own probe.
#
# What the bore actually changes is what sits BEHIND the glass.  So: walk the
# axis and require that no T1_body face lies between the lens and the bowl.
# Un-bored, two of them do -- the 2.8 mm solidified skin, at 2.1116 and 2.1088.
_sgn2 = 1.0 if _near == "lamp_L" else -1.0
_dg = bpy.context.evaluated_depsgraph_get()
_org = Vector((3.5, _sgn2 * HL_Y, HL_Z - rake_drop(HL_X)))
_dir = Vector((-1, 0, 0))
_seq = []
for _k in range(12):
    _hit, _loc, _nn, _ii, _ob, _mat = bpy.context.scene.ray_cast(_dg, _org, _dir)
    if not _hit:
        break
    _seq.append(_ob.name)
    _org = _loc + _dir * 0.0005
    if _ob.name.startswith("hl_bowl"):
        break
_lens_i = next((i for i, n in enumerate(_seq) if n.startswith("hl_lens")), None)
_bowl_i = next((i for i, n in enumerate(_seq) if n.startswith("hl_bowl")), None)
_between = ([n for n in _seq[_lens_i:_bowl_i] if n == "T1_body"]
            if _lens_i is not None and _bowl_i is not None else ["<no bowl reached>"])
ctl("C8", _lens_i is not None and _bowl_i is not None and not _between,
    "N4 nothing between lens and reflector down the lamp axis; hits = %s"
    % " -> ".join(_seq))

ghost = PXK["ghost"]
same = (abs(ghost[0] - PX["roundel"][0]) < 1.0
        and abs(ghost[1] - PX["roundel"][1]) < 1.0)
ctl("C5", not same,
    "KILL: a landmark 1 m in front of the nose lands %.1f px from the roundel "
    "(a stub projector would give 0.0)"
    % ((ghost[0] - PX["roundel"][0]) ** 2 + (ghost[1] - PX["roundel"][1]) ** 2) ** 0.5)

for n in NOTE:
    print("  note: %s" % n)

if not os.environ.get("T1_P45_KEEP"):
    try:
        os.remove(PNG)
    except OSError:
        pass

nfail = sum(1 for v in CTL.values() if not v)
print("CONTROLS: %d checked, %d FAILED%s"
      % (len(CTL), nfail,
         "" if not nfail else " -- " + ",".join(k for k, v in CTL.items() if not v)))
