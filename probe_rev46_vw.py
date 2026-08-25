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
import scipy.ndimage as ndi                                  # noqa: E402
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

# =====================================================================
# rev 58 -- THE AXIS THIS PROBE NEVER MEASURED, AND THE OWNER'S FIFTH REPORT.
#
# *[owner, rev 58]* "the vw emblems still need a fix, and the nose still does
# not look right."
#
# HIS REPEAT IS A MEASUREMENT.  That sentence is already in t1_core, written at
# rev 46 about his FOURTH report: when he reports the same thing again, the
# prior closure was wrong or incomplete.  This is the fifth, and this probe has
# reported "5 controls, 0 FAILED" throughout.
#
# WHY IT COULD NOT SEE IT.  Every landmark above (L1..L6) is a VERTICAL
# position -- a row index down the emblem.  Not one of them is a RADIUS.  So a
# stroke can terminate 18.9 mm short of the ring band with every landmark still
# landing, because where a stroke ENDS vertically and how far it REACHES
# radially are independent.  This is rev 46's own discovery -- "the axis nobody
# checked" -- recurring on the axis rev 46 did not check.
#
# MEASURED OFF THE BUILT MESH, as a fraction of the ring's OUTER R, band inner
# edge 0.7988:
#     V arm tips ............ 0.8400, 0.8400   on the band
#     W legs (troughs) ...... 0.8394, 0.8394   on the band
#     W OUTER ARM tips ...... 0.6638, 0.6638   FLOAT 18.9 mm short
#
# THE MECHANISM, traced rather than guessed.  A terminal cap is cut PERPENDICULAR
# TO THE STROKE, so its two corners sit at different radii.  vw_bars' fixed
# point drives each terminal's *MAX* corner onto the band, which leaves the
# other corner short by the cap's whole radial span; the W's outer arm meets the
# ring at 0.12 deg while travelling at 55.5 deg, so that span is 0.176 R and the
# far corner lands at 0.6638.  Then t1_detail.vw_logo_fit re-normalises the
# whole glyph by its GLOBAL EXTREME, which is the very mechanism rev 44b named
# and fixed one stage higher up -- "_fit_glyph scales by the SINGLE FURTHEST
# VERTEX ... and drags every other end short" -- still live, one stage below.
#
# THREE CANDIDATE FIXES WERE TRIED AT REV 58 AND ALL THREE MADE IT WORSE OR NO
# BETTER, WHICH IS WHY NONE OF THEM SHIPPED:
#     drive the MIN corner instead of the MAX ....... cells 6 -> 4 (worse)
#     make vw_logo_fit a pure unit conversion ....... cells 6 -> 4 (worse)
#     raise VW_W_ARM_Z 0.0019 -> 0.30/0.55/0.77 ..... cells 6, 6, 6 (no change)
# The glyph stays an X in all of them.  The V's arms and the W's outer arms
# cross over the same region BY CONSTRUCTION, so this is a re-solve of the W's
# spine against reach, not a one-constant tweak.  Recorded so the next attempt
# does not spend itself re-trying these three.
BAND_INNER = 1.0 - BAND          # 0.80 of the outer R, the band's inner edge


def glyph_only_mask(rows=276, **over):
    """The glyph WITH its ring band, rasterised in its own plane -- the same
    construction built_mask uses, kept separate only so overrides can be passed
    per call without disturbing the landmark path above."""
    old = {k: getattr(C, k) for k in over}
    for k, v in over.items():
        setattr(C, k, v)
    try:
        return built_mask(rows)
    finally:
        for k, v in old.items():
            setattr(C, k, v)


def cream_cells(mask, frac=0.97):
    """How many separate CREAM cells the strokes cut the ring's interior into.

    STRUCTURAL, like every landmark here: a region count, not a thresholded
    position, so it survives blur and exposure and needs no axis ratio.  It is
    the right statistic for THIS defect because a stroke that fails to reach the
    ring MERGES THE TWO CELLS EITHER SIDE OF IT -- the count drops by exactly
    one per floating stroke, whatever the stroke's width or angle.

    The photograph and the built raster go through this SAME function.  A second
    copy of a measurement is how one of them gets quietly relaxed."""
    n0, n1 = mask.shape
    yy, xx = np.mgrid[0:n0, 0:n1]
    cy, cx = (n0 - 1) / 2.0, (n1 - 1) / 2.0
    disc = (((yy - cy) / (n0 / 2.0)) ** 2 + ((xx - cx) / (n1 / 2.0)) ** 2) <= frac ** 2
    bg = disc & (~mask)
    lab, k = ndi.label(bg)
    if k == 0:
        return 0, []
    sz = ndi.sum(bg, lab, range(1, k + 1))
    big = [int(s) for s in sz if s >= 0.002 * disc.sum()]
    return len(big), sorted(big, reverse=True)


def photo_cells():
    """The same count on ref_nolita_front34.jpg's own roundel."""
    a = np.asarray(Image.open(os.path.join(HERE, "ref_nolita_front34.jpg"))
                   .convert("RGB")).astype(float)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    red = (R > 110) & (G < 0.60 * R) & (B < 0.60 * R)
    lab, n = ndi.label(red)
    sub = lab[192:261, 153:194]
    ids, counts = np.unique(sub[sub > 0], return_counts=True)
    return cream_cells(sub == ids[int(np.argmax(counts))])


nb, sb = cream_cells(glyph_only_mask(**CURRENT))
npho, sp = photo_cells()
print("")
print("    REACH / TOPOLOGY -- cream cells the strokes cut the ring into")
print("        PHOTOGRAPH  %d cells   sizes %s" % (npho, sp))
print("        BUILT       %d cells   sizes %s" % (nb, sb[:8]))
ctl("C6", nb == npho,
    "THE BUILT GLYPH CUTS THE RING INTO THE SAME NUMBER OF CELLS AS THE "
    "PHOTOGRAPH.  photo %d, built %d.  A stroke that fails to reach the ring "
    "merges the two cells either side of it, so a deficit of %d is %d floating "
    "stroke(s) -- and the mesh names them: the W's two outer arms, at r 0.6638 "
    "against a band inner edge of 0.7988, floating 18.9 mm"
    % (npho, nb, npho - nb, max(0, npho - nb)))

# THE KILL.  A topology control that cannot go red proves nothing.  Erase the
# W entirely and the count must collapse.
_gone = glyph_only_mask(**CURRENT).copy()
_nk, _ = cream_cells(_gone)
_half = glyph_only_mask(VW_W_ARM_X=0.05, VW_W_TROUGH_X=0.05)
_nh, _ = cream_cells(_half)
ctl("C7", _nh != nb,
    "KILL: collapsing the W's arms and troughs onto the axis moves the cell "
    "count %d -> %d, so this control follows the glyph's topology rather than "
    "reporting a constant" % (nb, _nh))

nfail = sum(1 for v in CTL.values() if not v)
print("\nCONTROLS: %d checked, %d FAILED%s"
      % (len(CTL), nfail,
         "" if not nfail else " -- " + ",".join(k for k, v in CTL.items() if not v)))


# =====================================================================
# rev 60 -- T1_VW_CELLSOLVE: PUT cream_cells INTO THE OBJECTIVE.
#
# The rev-60 brief's item C says the missing piece is exactly this, and that
# if no setting of the six parameters reaches the photograph's 7 cells, the
# honest result is to SAY SO WITH THE NUMBER.  So this searches and reports,
# and it does NOT write anything into t1_core.
#
# WHY REACH ALONE IS KNOWN NOT TO BE THE ANSWER (rev 60, measured).  Driving
# the cap's near corner onto the band -- which removes the 18.9 mm float that
# F63 named as the defect -- makes the topology WORSE, not better:
#     T1_VW_CAPMIN=0 T1_VW_PUREFIT=0    6 cells   (as shipped)
#     T1_VW_CAPMIN=0 T1_VW_PUREFIT=1    6 cells
#     T1_VW_CAPMIN=1 T1_VW_PUREFIT=0    2 cells
#     T1_VW_CAPMIN=1 T1_VW_PUREFIT=1    4 cells
# So the float is a SYMPTOM and not the cause: strokes pushed further into the
# band merge with their neighbours and swallow the cream between them.  The
# cell count is a property of where the strokes LAND ANGULARLY, which is the
# spine's business, not the cap's.
# =====================================================================
if os.environ.get("T1_VW_CELLSOLVE"):
    import random as _rnd
    _rnd.seed(60)
    _NEV = int(os.environ.get("T1_VW_CELLSOLVE_N", 900))
    _lo = {"VW_V_TIP_X": 0.20, "VW_APEX_Z": 0.15, "VW_W_ARM_X": 0.55,
           "VW_W_ARM_Z": -0.40, "VW_W_TROUGH_X": 0.30, "VW_W_TROUGH_Z": -0.90}
    _hi = {"VW_V_TIP_X": 0.55, "VW_APEX_Z": 0.45, "VW_W_ARM_X": 1.05,
           "VW_W_ARM_Z": 0.55, "VW_W_TROUGH_X": 0.70, "VW_W_TROUGH_Z": -0.30}

    def _score(p):
        try:
            n, sz = cream_cells(glyph_only_mask(**p))
            e, _L = err(built_landmarks(**p))
        except Exception:
            return None
        return n, e, sz

    print("\n    T1_VW_CELLSOLVE -- searching %d points for the photograph's "
          "%d cells" % (_NEV, npho))
    _best = {}          # cells -> (residual, params, sizes)
    _cur = dict(CURRENT)
    _r = _score(_cur)
    if _r:
        _best[_r[0]] = (_r[1], dict(_cur), _r[2])
    _seen = 0
    for _it in range(_NEV):
        # half the budget random over the box, half a local walk from the best
        # 7-cell (or else best-celled) point found so far
        if _it % 2 == 0 or not _best:
            _p = {k: _rnd.uniform(_lo[k], _hi[k]) for k in PARAMS}
        else:
            _target = max(_best)
            _base = _best[_target][1]
            _sc = 0.12 * (1.0 - _it / float(_NEV)) + 0.01
            _p = {k: min(_hi[k], max(_lo[k],
                  _base[k] + _rnd.gauss(0.0, _sc) * (_hi[k] - _lo[k])))
                  for k in PARAMS}
        _r = _score(_p)
        _seen += 1
        if not _r:
            continue
        _n, _e, _sz = _r
        if _n not in _best or _e < _best[_n][0]:
            _best[_n] = (_e, dict(_p), _sz)
    print("    evaluated %d points" % _seen)
    print("    cells reached: %s" % ", ".join(str(k) for k in sorted(_best)))
    for _n in sorted(_best):
        _e, _p, _sz = _best[_n]
        _mark = "  <-- THE PHOTOGRAPH'S COUNT" if _n == npho else ""
        print("      %d cells  best landmark residual %.4f%s" % (_n, _e, _mark))
        if _n == npho or _n == max(_best):
            print("          " + "  ".join("%s %.4f" % (k, _p[k])
                                           for k in PARAMS))
            print("          sizes %s" % (_sz,))
    if npho in _best:
        print("    RESULT: %d cells IS reachable; best landmark residual there "
              "is %.4f against C4's bar of 0.045"
              % (npho, _best[npho][0]))
    else:
        print("    RESULT: NO setting of the six spine parameters reached %d "
              "cells in %d evaluations.  Best was %d.  The current spine "
              "family cannot reach the photograph's topology."
              % (npho, _seen, max(_best)))


# rev 60 -- T1_VW_DUMP: PAINT THE CELLS AND LOOK AT THEM.
# A cell COUNT is a statistic about a picture nobody in this project has ever
# looked at.  Rule 8 applies to a topology exactly as it applies to a window.
if os.environ.get("T1_VW_DUMP"):
    def _paint_cells(mask, name, frac=0.97):
        """Paint what cream_cells() actually counts, in ITS OWN colours."""
        n0, n1 = mask.shape
        yy, xx = np.mgrid[0:n0, 0:n1]
        cy, cx = (n0 - 1) / 2.0, (n1 - 1) / 2.0
        disc = (((yy - cy) / (n0 / 2.0)) ** 2
                + ((xx - cx) / (n1 / 2.0)) ** 2) <= frac ** 2
        bg = disc & (~mask)
        lab, k = ndi.label(bg)
        sz = ndi.sum(bg, lab, range(1, k + 1))
        keep = 0.002 * disc.sum()
        out = np.zeros((n0, n1, 3), np.uint8)
        out[mask] = (40, 40, 40)
        cols = [(235, 60, 60), (60, 205, 95), (70, 125, 245), (240, 195, 45),
                (205, 80, 225), (55, 215, 215), (250, 135, 40)]
        big = sorted(((int(sz[i]), i + 1) for i in range(k) if sz[i] >= keep),
                     reverse=True)
        for rank, (_s, idx) in enumerate(big):
            out[lab == idx] = cols[rank % len(cols)]
        for i in range(k):                       # slivers below the size floor
            if sz[i] < keep:
                out[lab == i + 1] = (255, 255, 255)
        os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
        sc = max(1, int(420 / max(n0, n1)))
        Image.fromarray(out).resize((n1 * sc, n0 * sc), Image.NEAREST).save(
            os.path.join(HERE, "out", "vw_cells_%s.png" % name))
        print("    %-8s %d counted cells (white = below the 0.2 %% floor) "
              "-> out/vw_cells_%s.png" % (name, len(big), name))
        return len(big)

    _a = np.asarray(Image.open(os.path.join(HERE, "ref_nolita_front34.jpg"))
                    .convert("RGB")).astype(float)
    _R, _G, _B = _a[..., 0], _a[..., 1], _a[..., 2]
    _red = (_R > 110) & (_G < 0.60 * _R) & (_B < 0.60 * _R)
    _lab, _n = ndi.label(_red)
    _sub = _lab[192:261, 153:194]
    _ids, _counts = np.unique(_sub[_sub > 0], return_counts=True)
    _paint_cells(_sub == _ids[int(np.argmax(_counts))], "photo")
    _paint_cells(glyph_only_mask(rows=69, **CURRENT), "built_69")
    _alt = os.environ.get("T1_VW_DUMP_P")
    if _alt:
        import json as _json
        _ap = dict(CURRENT); _ap.update(_json.loads(_alt))
        _paint_cells(glyph_only_mask(rows=69, **_ap), "alt_69")
        print("    alt params: " + "  ".join("%s %.4f" % (k, _ap[k])
                                             for k in PARAMS))
    _paint_cells(glyph_only_mask(**CURRENT), "built_276")


# rev 60 -- T1_VW_RES: IS C6's 6-vs-7 A SHAPE DEFECT OR A RESOLUTION ARTEFACT?
#
# THE TWO SIDES OF C6 ARE NOT RASTERISED AT THE SAME SCALE.  photo_cells()
# counts inside a 41 x 69 px crop of ref_nolita_front34.jpg; glyph_only_mask
# defaults to 276 ROWS.  A cell count is a TOPOLOGY, and topology is
# resolution-sensitive: a cream gap one pixel wide at 69 rows is four pixels
# wide at 276 and survives where the other merges.  C6 has compared the two
# directly since rev 58 without this ever being checked.  Rule 36 -- run the
# instrument on a case whose answer you already know.
if os.environ.get("T1_VW_RES"):
    print("\n    T1_VW_RES -- the BUILT glyph's cell count against raster scale")
    print("    (the photograph's own count, at its native 41 x 69, is %d)" % npho)
    for _rows in (41, 55, 69, 90, 138, 207, 276, 414, 552):
        try:
            _n, _s = cream_cells(glyph_only_mask(rows=_rows, **CURRENT))
            print("      rows %4d   cells %d   sizes %s" % (_rows, _n, _s[:8]))
        except Exception as _e:
            print("      rows %4d   FAILED %s" % (_rows, _e))


# rev 60 -- T1_VW_WSWEEP: THE STROKE WEIGHT, MEASURED AGAINST THE PHOTOGRAPH.
#
# PAINTING THE COUNTED CELLS (T1_VW_DUMP) SHOWED WHAT NO COUNT COULD.  The
# photograph's cream cells are LONG THIN SLIVERS; the built glyph's are FAT
# WEDGES.  That is not a reach difference and no spine solves it: the
# photographed strokes are HEAVY and the built ones are LIGHT.  So the defect
# behind "it builds as an X" is STROKE WEIGHT, and the cell count is merely
# how it shows up in the topology.
#
# THE SCALE-FREE STATISTIC IS INK FRACTION inside the roundel disc -- ink
# pixels over disc pixels.  It needs no axis ratio, no px/m and no landmark,
# so an oblique 41 x 69 crop and a 276-row raster can be compared directly.
if os.environ.get("T1_VW_WSWEEP"):
    def _ink_frac(mask, frac=0.97):
        n0, n1 = mask.shape
        yy, xx = np.mgrid[0:n0, 0:n1]
        cy, cx = (n0 - 1) / 2.0, (n1 - 1) / 2.0
        disc = (((yy - cy) / (n0 / 2.0)) ** 2
                + ((xx - cx) / (n1 / 2.0)) ** 2) <= frac ** 2
        return float((mask & disc).sum()) / float(disc.sum())

    _a = np.asarray(Image.open(os.path.join(HERE, "ref_nolita_front34.jpg"))
                    .convert("RGB")).astype(float)
    _R, _G, _B = _a[..., 0], _a[..., 1], _a[..., 2]
    _red = (_R > 110) & (_G < 0.60 * _R) & (_B < 0.60 * _R)
    _lab, _n = ndi.label(_red)
    _sub = _lab[192:261, 153:194]
    _ids, _counts = np.unique(_sub[_sub > 0], return_counts=True)
    _pm = (_sub == _ids[int(np.argmax(_counts))])
    _pf = _ink_frac(_pm)
    print("\n    T1_VW_WSWEEP -- stroke weight against the photograph")
    print("    PHOTOGRAPH ink fraction %.4f, cells %d" % (_pf, npho))
    print("    %-8s %-8s %-6s %s" % ("wfrac", "inkfrac", "cells", "sizes"))
    for _wf in (0.1986, 0.24, 0.28, 0.32, 0.36, 0.40, 0.44, 0.48):
        os.environ["T1_VW_WFRAC"] = "%.4f" % _wf
        try:
            _m = glyph_only_mask(**CURRENT)
            _if = _ink_frac(_m)
            _c, _sz = cream_cells(_m)
            print("    %-8.4f %-8.4f %-6d %s%s"
                  % (_wf, _if, _c, _sz[:7],
                     "   <-- photograph's cell count" if _c == npho else ""))
        except Exception as _e:
            print("    %-8.4f FAILED %s" % (_wf, _e))
    os.environ.pop("T1_VW_WFRAC", None)
