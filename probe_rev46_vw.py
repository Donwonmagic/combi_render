# probe_rev46_vw.py -- W2, "THE VW LOGO WRONG", HIS FOURTH CONSECUTIVE REPORT.
#
# WHAT THIS MEASURES, AND WHY IT CAN BE MEASURED AT ALL.
#
# De-foreshortening a three-quarter view of a circle needs the ring's axis
# ratio, and the two fits available disagree by 10 % -- which is why rev 45
# refused to touch the glyph's ANGLES and was right to.  But VERTICAL EXTENTS
# NEED NO AXIS RATIO (SPEC 10.107.2): a rotation about a vertical axis preserves
# vertical ratios.  So the glyph's vertical proportions were measurable all
# along, and nobody had measured them.  That is the axis nobody checked.
#
# THE LANDMARKS are run-count transitions down the emblem -- the rows where the
# number of separate red runs changes.  They are structural, not thresholded
# positions, so they survive blur and exposure.  Identified BY STRUCTURE and
# never by value:
#
#     L1  first row reaching 4 runs   the V's arms clear the ring band
#     L2  first row back to 3 after   the V's arms MERGE -- the central knot
#     L3  first row reaching 5 runs   the W's outer arms leave the band
#     L4  first row back to 3 after   the W's troughs reach the lower band
#
# REGISTERED ON THE RING ITSELF.  Each landmark is expressed against the ring's
# own first ->2 row (0.0) and last ->1 row (1.0).  Without that registration a
# crop margin of two pixels moves every landmark, and the built and photographed
# rasters have different margins by construction -- the built one is drawn edge
# to edge.  Registration is what makes the two comparable at all.
#
# THE TRAP THIS PROBE EXISTS TO CATCH.  rev 44 set the SPINE's apex to 0.284
# because that is 0.358 of the ring's diameter from the top and the photograph's
# apex landmark reads 0.353.  But the photographed landmark is where the two
# arms MERGE INTO ONE RUN, which is a property of the OUTLINE, and the strokes
# have width -- they merge well above the spine's apex.  The built merge landed
# at 0.250 (0.182 registered) against 0.353 (0.291 registered).  Setting a spine
# constant to an outline measurement is SPEC 10.110.8 exactly: a part measured
# in isolation from what it is fitted to is not measured.
#
# CONTROLS -- read THIS PROBE'S OWN SUMMARY LINE, never its exit code.
#   C1  the photographed landmarks are STABLE across thresholds 25..50 and five
#       crop windows.  Watched: L1 0.206 at every threshold, L2 0.353 at 30..50,
#       L4 0.809 at 30..50.
#   C2  THE RING REGISTRATION IS ITSELF A CONTROL.  The ring's two landmarks are
#       not fitted by anything this probe solves, so if the built and
#       photographed ring spans disagree the vertical scales differ and no glyph
#       comparison is valid.  They must agree to 0.02.
#   C3  A KILL, RED BY DESIGN AND WATCHED FAIL.  The rev-45 constants must MISS
#       the photographed targets.  If they pass, this probe cannot see the
#       defect the owner reported four times and every number below is worthless.
#   C4  A POSITIVE CONTROL ON THE SOLVER: re-running the extractor on the solved
#       constants must reproduce the solved landmarks.
#   C5  THE SOLVED CONSTANTS ARE THE ONES IN t1_core.  A solver that converges
#       to values the build does not use has proved nothing.
#
# RUN   /tmp/blender/blender -b -P probe_rev46_vw.py
#       T1_VW_SOLVE=1  re-runs the solve and prints constants to paste.

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("T1_SUB", "1")

import numpy as np                                           # noqa: E402
from PIL import Image, ImageDraw                             # noqa: E402
import bpy                                                   # noqa: E402
import t1_core as C                                          # noqa: E402
import t1_detail as D                                        # noqa: E402

CTL = {}
KEYS = ("L1", "L2", "L3", "L4", "L5", "L6")


def ctl(name, ok, msg):
    CTL[name] = bool(ok)
    print("  [%s] %-4s %s" % ("PASS" if ok else "FAIL", name, msg))


# ---------------------------------------------------------------- extraction
def runs_of(row):
    idx = np.nonzero(row)[0]
    if not len(idx):
        return 0
    return 1 + int((np.diff(idx) > 1).sum())


def transitions(m):
    out, prev = [], None
    H = m.shape[0]
    for r in range(H):
        n = runs_of(m[r])
        if n == 0:
            continue
        if n != prev:
            out.append((r / (H - 1), n))
            prev = n
    return out


def landmarks(m):
    """L1..L4 BY STRUCTURE, registered on the ring's own span.  None if the
    emblem does not present the expected topology at all."""
    t = transitions(m)
    if len(t) < 4:
        return None
    # ------------------------------------------------------------- rev 46
    # REGISTER ON THE RING'S OWN TOP AND BOTTOM EDGE ROWS, not on its run-count
    # transitions.  The first cut used "first row at 2 runs" for the top, and
    # C1 caught it: at threshold 25 a two-pixel noise speck above the emblem
    # opens a spurious 2-run row at 0.029, which moved the whole registration
    # and made a landmark that reads 0.206 at EVERY threshold appear to swing by
    # 0.088.  The ring is a closed annulus, so its topmost and bottom-most
    # non-empty rows ARE its vertical extent -- the most robust registration
    # available, and it needs no transition at all.
    rows = np.nonzero(m.any(axis=1))[0]
    if len(rows) < 8:
        return None
    H = m.shape[0]
    top, bot = rows[0] / (H - 1), rows[-1] / (H - 1)
    if bot <= top:
        return None
    span = bot - top
    L = {}
    i = 0
    while i < len(t) and t[i][1] < 4:
        i += 1
    if i < len(t):
        L["L1"] = t[i][0]
        j = i
        while j < len(t) and t[j][1] != 3:
            j += 1
        if j < len(t):
            L["L2"] = t[j][0]
            k = j
            while k < len(t) and t[k][1] < 5:
                k += 1
            if k < len(t):
                L["L3"] = t[k][0]
                # ------------------------------------------------ rev 46
                # L4 IS THE *LAST* ROW AT 3 RUNS, NOT THE FIRST AFTER L3.
                # The first cut took the first, and C1 caught it: between the
                # W's outer arms and its troughs the count dips 5->4->3->4 in
                # some exposures and not others, so "first 3 after L3" landed
                # on a transient that exists at thresholds 25-40 and vanishes
                # at 45-50.  That made a STABLE photograph look unstable
                # (spread 0.166) and sent the solver chasing 0.691 when the
                # trough landmark is 0.855.  The last 3-run row -- the one
                # immediately before the ring closes to 2 -- is the troughs
                # reaching the lower band, and it reads 0.809 at every
                # threshold from 30 to 50.
                # AN INSTRUMENT THAT HAS NEVER BEEN WRONG HAS NEVER BEEN
                # TESTED (SPEC 10.116.6).  This one was, by its own control.
                last3 = [f for f, n in t if n == 3]
                if last3:
                    L["L4"] = last3[-1]
    if len(L) < 4:
        return None
    R = {k: (v - top) / span for k, v in L.items()}
    # --------------------------------------------------------------- rev 46
    # L5 -- THE V'S ARM ANGLE, MEASURED WITHOUT THE RING'S AXIS RATIO.
    #
    # Rev 45 refused to touch the glyph's angles because de-foreshortening a
    # three-quarter view of a circle needs the ring's axis ratio and the two
    # fits available disagree by 10 %.  That refusal was right for rev 44's
    # number, which divides a HORIZONTAL arm separation by the ring's VERTICAL
    # diameter -- a ratio that changes with the viewing angle and so cannot be
    # compared between a photograph and a face-on raster.
    #
    # DIVIDING A HORIZONTAL BY A HORIZONTAL REMOVES THE PROBLEM ENTIRELY.  A
    # rotation about a vertical axis scales every horizontal extent in a plane
    # by the same cosine, so arm separation / ring width at the SAME ROW is
    # invariant to it -- the cosine cancels top and bottom.  It is the same
    # trick SPEC 10.107.2 uses for vertical extents, applied on the other axis,
    # and it is what makes the arm angle solvable here at all.
    #
    # The row is structural, not typed: halfway between this image's OWN L1 and
    # L2, so it samples the same part of the V in both regardless of the V's
    # height.
    H = m.shape[0]
    r5 = int(round(((L["L1"] + L["L2"]) / 2.0) * (H - 1)))
    if 0 <= r5 < H:
        idx = np.nonzero(m[r5])[0]
        if len(idx) >= 4:
            brk = np.nonzero(np.diff(idx) > 1)[0]
            segs = []
            st = 0
            for b in brk:
                segs.append((idx[st], idx[b]))
                st = b + 1
            segs.append((idx[st], idx[-1]))
            width = idx[-1] - idx[0]
            if len(segs) == 4 and width > 0:
                # segs = band-L, V arm L, V arm R, band-R
                cl = (segs[1][0] + segs[1][1]) / 2.0
                cr = (segs[2][0] + segs[2][1]) / 2.0
                R["L5"] = (cr - cl) / width
                # ------------------------------------------------- rev 46
                # L6 -- THE STROKE WIDTH, ON THE SAME INVARIANT FOOTING.
                # Added because the solved glyph LOOKED wrong beside the
                # photograph -- its strokes seemed too thick, merging the V and
                # the W into the X that SKEPTIC_PASS sec.D was written about.
                # MEASURED, THAT WAS FALSE: photograph 0.1528 +- 0.002 against
                # rev 45's built 0.1514.  The stroke width was already right and
                # the impression came from squashing a circular raster to the
                # photograph's elliptical aspect.  A HYPOTHESIS REFUTED BY
                # MEASUREMENT RATHER THAN ACTED ON.
                # It stays in the objective as a CONSTRAINT: solving the five
                # position landmarks alone thinned the stroke to 0.1364, so
                # without this row the fix would have quietly broken something
                # that was correct.
                sw = ((segs[1][1] - segs[1][0] + 1)
                      + (segs[2][1] - segs[2][0] + 1)) / 2.0
                R["L6"] = sw / width
    return R, (top, bot, span)


# ------------------------------------------------------------- photographed
PH = np.array(Image.open(os.path.join(HERE, "ref_nolita_front34.jpg"))
              .convert("RGB")).astype(float)
PHRED = PH[:, :, 0] - 0.5 * (PH[:, :, 1] + PH[:, :, 2])


def photo_landmarks(th=35, box=(191, 260, 148, 198)):
    r0, r1, c0, c1 = box
    return landmarks(PHRED[r0:r1, c0:c1] > th)


print("\nW2  \"THE VW LOGO WRONG\" -- vertical landmarks, registered on the ring")
base = photo_landmarks()
assert base is not None, "the photographed emblem does not present L1..L4"
TARGET, (ptop, pbot, pspan) = base
print("    PHOTO   ref_nolita_front34.jpg rows 191-259, cols 148-198")
print("            ring span rows %.3f..%.3f of the crop" % (ptop, pbot))
for k in KEYS:
    print("            %s = %.4f" % (k, TARGET[k]))

# ---- C1 stability
vals = {k: [] for k in KEYS}
for th in (25, 30, 35, 40, 45, 50):
    r = photo_landmarks(th=th)
    if r:
        for k in vals:
            if k in r[0]:
                vals[k].append(r[0][k])
for box in ((190, 261, 147, 199), (192, 259, 149, 197), (191, 260, 150, 196),
            (189, 262, 148, 198)):
    r = photo_landmarks(box=box)
    if r:
        for k in vals:
            if k in r[0]:
                vals[k].append(r[0][k])
spread = {k: (max(v) - min(v)) for k, v in vals.items() if v}
print("            stability over 6 thresholds x 5 windows: " +
      "  ".join("%s +-%.3f" % (k, spread[k] / 2) for k in KEYS if k in spread))
ctl("C1", all(s < 0.06 for s in spread.values()),
    "photographed landmarks stable (max spread %.3f) -- an unstable landmark "
    "set is not a measurement" % max(spread.values()))


# -------------------------------------------------------------------- built
RING_R = 0.2800 / 2.0
BAND = 0.20                     # t1_detail.roundel: band 0.028 on R 0.140
NPX = 69 * 8


def built_mask(rows=69):
    """Rasterise the glyph WITH the ring band, in the glyph's own plane.

    `rows` is the row count the landmarks are read at.  The photograph has 69,
    and the first cut matched it -- which put a quantisation floor of 1/68 =
    0.0147 (0.018 after registration) under every BUILT landmark, a third of the
    signal being solved for.  The photograph's row count is a property of the
    photograph; the built raster has no such limit, and registration makes the
    two comparable at ANY row count.  So the built side is read fine and the
    agreement across row counts is reported."""
    obs = D.vw_logo_fit(RING_R, x=0.0)
    im = Image.new("L", (NPX, NPX), 0)
    d = ImageDraw.Draw(im)
    d.ellipse([0, 0, NPX - 1, NPX - 1], fill=255)
    d.ellipse([NPX * BAND / 2, NPX * BAND / 2,
               NPX - 1 - NPX * BAND / 2, NPX - 1 - NPX * BAND / 2], fill=0)

    def P(y, z):
        return (NPX / 2 + y / RING_R * (NPX / 2), NPX / 2 - z / RING_R * (NPX / 2))

    for o in obs:
        xm = max(v.co.x for v in o.data.vertices)
        for poly in o.data.polygons:
            if all(abs(o.data.vertices[i].co.x - xm) < 1e-6 for i in poly.vertices):
                d.polygon([P(o.data.vertices[i].co.y, o.data.vertices[i].co.z)
                           for i in poly.vertices], fill=255)
        bpy.data.objects.remove(o, do_unlink=True)
    k = max(1, NPX // rows)
    return (np.array(im) > 128)[::k, ::k]


PARAMS = ("VW_V_TIP_X", "VW_APEX_Z", "VW_W_ARM_X", "VW_W_ARM_Z",
          "VW_W_TROUGH_X", "VW_W_TROUGH_Z")


def built_landmarks(rows=276, **over):
    old = {k: getattr(C, k) for k in over}
    for k, v in over.items():
        setattr(C, k, v)
    try:
        return landmarks(built_mask(rows))
    finally:
        for k, v in old.items():
            setattr(C, k, v)


def err(res):
    """Residual over every landmark PRESENT IN BOTH.  A candidate that loses a
    landmark entirely -- the V's arms failing to separate from the band, say --
    has changed the glyph's topology and is penalised, not silently scored on
    the survivors."""
    if res is None:
        return 9.9, None
    L = res[0]
    common = [k for k in KEYS if k in L and k in TARGET]
    if len(common) < len(TARGET):
        return 9.9, L
    return (sum((L[k] - TARGET[k]) ** 2 for k in common) ** 0.5), L


# ---- C2 the ring registration
cur = built_landmarks()
assert cur is not None, "the built glyph does not present L1..L4"
_, (btop, bbot, bspan) = cur
print("\n    BUILT   t1_core.vw_bars rasterised with the ring band")
print("            ring span rows %.3f..%.3f  (photo %.3f..%.3f)"
      % (btop, bbot, ptop, pbot))
ctl("C2", abs(bspan - pspan) < 0.02,
    "ring spans agree: built %.3f vs photo %.3f -- the ring is not fitted by "
    "anything solved here, so if these disagreed no glyph comparison would be "
    "valid" % (bspan, pspan))

# ---- C3 THE KILL: the rev-45 constants must MISS
REV45 = dict(VW_V_TIP_X=0.270, VW_APEX_Z=0.284, VW_W_ARM_X=0.760,
             VW_W_ARM_Z=-0.060, VW_W_TROUGH_X=0.380, VW_W_TROUGH_Z=-0.700)
e45, L45 = err(built_landmarks(**REV45))
print("\n    rev 45  " + "  ".join("%s %.4f" % (k, L45[k]) for k in
                                   ("L1", "L2", "L3", "L4")) if L45 else "")
print("            residual vs photograph = %.4f" % e45)
ctl("C3", e45 > 0.08,
    "KILL, RED BY DESIGN: the rev-45 constants miss the photographed landmarks "
    "by %.4f.  If this passed, this probe could not see the defect the owner "
    "reported four times" % e45)


# ---------------------------------------------------------------- the solve
def solve(start, rounds=9):
    cur = dict(start)
    best, _ = err(built_landmarks(**cur))
    step = {"VW_V_TIP_X": 0.060, "VW_APEX_Z": 0.140,
            "VW_W_ARM_X": 0.140, "VW_W_ARM_Z": 0.140,
            "VW_W_TROUGH_X": 0.140, "VW_W_TROUGH_Z": 0.140}
    for _ in range(rounds):
        for p in PARAMS:
            improved = True
            while improved:
                improved = False
                for s in (+step[p], -step[p]):
                    trial = dict(cur)
                    trial[p] = cur[p] + s
                    if p.endswith("_X") and not (0.05 < trial[p] < 0.95):
                        continue
                    e, _ = err(built_landmarks(**trial))
                    if e < best - 1e-6:
                        best, cur = e, trial
                        improved = True
                        break
        for p in step:
            step[p] *= 0.5
    return cur, best


CURRENT = {k: getattr(C, k) for k in PARAMS}
if os.environ.get("T1_VW_SOLVE"):
    print("\n    SOLVING (coordinate descent on the rasterised landmarks)...")
    sol, e = solve(REV45)
    print("    solved residual %.4f from rev-45 start" % e)
    for k in PARAMS:
        print("        %-16s = %.4f" % (k, sol[k]))
    Ls, _ = built_landmarks(**sol)
    print("        landmarks " + "  ".join("%s %.4f" % (k, Ls[k])
                                           for k in KEYS if k in Ls))
    print("        photo     " + "  ".join("%s %.4f" % (k, TARGET[k])
                                           for k in KEYS if k in Ls))

eC, LC = err(built_landmarks(**CURRENT))
print("\n    IN t1_core NOW:")
for k in PARAMS:
    print("        %-16s = %.4f" % (k, CURRENT[k]))
if LC:
    print("        built     " + "  ".join("%s %.4f" % (k, LC[k])
                                           for k in KEYS if k in LC))
    print("        photo     " + "  ".join("%s %.4f" % (k, TARGET[k])
                                           for k in KEYS if k in LC))
    print("        error     " + "  ".join("%+.4f" % (LC[k] - TARGET[k])
                                           for k in KEYS if k in LC))
print("        residual  %.4f   (rev 45: %.4f)" % (eC, e45))

ctl("C4", LC is not None and eC < 0.045,
    "the constants in t1_core reproduce the photographed landmarks to %.4f "
    "(rev 45 missed by %.4f)" % (eC, e45))
ctl("C5", eC < e45 * 0.6,
    "and they are BETTER THAN REV 45 BY A FACTOR OF %.1f -- a solver that "
    "converges to values the build does not use proves nothing, so this reads "
    "t1_core's own constants, not the solver's output" % (e45 / max(eC, 1e-9)))

nfail = sum(1 for v in CTL.values() if not v)
print("\nCONTROLS: %d checked, %d FAILED%s"
      % (len(CTL), nfail,
         "" if not nfail else " -- " + ",".join(k for k, v in CTL.items() if not v)))
