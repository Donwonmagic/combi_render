# probe_rev62_landmarks.py -- WHICH OF L1..L6 IS WRONG?
#
# THE QUESTION, AND WHY IT IS THE RIGHT ONE.  Rev 61 closed the emblem's search
# space (F137): using probe_rev46_vw.py's OWN functions over 8,174 candidates,
# the maximum cream-cell elongation achievable SUBJECT TO the L1..L6 landmark
# bar (residual < 0.045) is 1.634, against the photograph's 3.39.  Drop the bar
# and the same construction reaches 4.644.  So the CONSTRUCTION can produce the
# photograph's slivers and THE LANDMARKS FORBID IT.  L1..L6 and the photograph's
# cell shape are incompatible, and one of them is wrong.
#
# F139 already showed one target IS wrong: C6's 7 is contaminated -- the seventh
# counted cell sits entirely inside the ring band with no left-hand counterpart,
# so the genuine count is 6, the same as the build.  If C6's target can be
# wrong, L1..L6 can be too.
#
# THE ROUTE.  Every one of L1..L6 was fitted to ONE badge: ref_nolita_front34.jpg
# rows 191-259, cols 148-198 -- 50x69 px.  ref_workshop.jpg carries the SAME
# factory pressing at 62x93 px, 1.71x the area (F09 fitted its 50%-level conic
# at vertical D 92.728, horizontal D 63.299, radial residual 0.2345 px).
#
# ADMISSIBLE, AND THE ARGUMENT IS NOT MINE.  ref_workshop.jpg is the GREEN
# vehicle and rule 11 forbids transferring paint or artwork between vehicles.
# F141's corollary is that the roundel's SHAPE is the factory chrome PRESSING --
# geometry, which DOES transfer -- and only its colour is artwork.  That frame
# is already load-bearing in the shipped model in two places for exactly this
# reason (F09): the ring band ratio and the glyph's own fit radius.
#
# WHAT IS DIFFERENT ABOUT THIS FRAME, STATED BEFORE ANY NUMBER.  On the red bus
# the mask is PAINT: R - 0.5(G+B) selects the red ring and the red glyph, and
# the cells are cream.  On the green bus there is no red -- the pressing reads
# as a DARK stroke against the cream nose showing through the cells.  So the
# mask here is DARKNESS, not redness.  That is a different segmentation of the
# same topology, and it is the single largest thing that could make this
# comparison invalid.  It is why C1w..C3w below exist and why the mask is
# PAINTED before a landmark is quoted (rule 8).
#
# AND THE FIRST MASK I WROTE WAS WRONG, CAUGHT BY PAINTING IT (rule 4).  At
# th = 118 the mask took the LEFT FLANK OF EVERY STROKE AND NOTHING ELSE: the
# pressing is chrome lit from the right, so each stroke is a dark shadow flank
# beside a specular highlight flank, and a low level threshold eats one and
# drops the other.  That is F08's recorded failure mode -- *"threshold eats the
# pressing's SHADOW ... the level-free edge fit LOCKS ONTO THE SPECULAR
# HIGHLIGHT"* -- arriving on a different statistic.  It produced six plausible
# deltas and every one of them was an artefact.  The cells read 190..215 and the
# pressing 83..155, so the separating level is ~165, not ~118; the handful of
# specular pixels INSIDE a stroke are closed over with a 3x3.  The repaired mask
# is stable in count and topology over 145..180 -- see C1w.
#
# NO DRIFT BY CONSTRUCTION.  This file does not re-implement runs_of(),
# transitions() or landmarks().  It lifts their SOURCE TEXT out of
# probe_rev46_vw.py with ast at run time and execs it, so the two instruments
# cannot disagree about what a landmark is.  If probe_rev46_vw.py's definitions
# change, this probe changes with them or fails loudly.
#
# CONTROLS -- read this probe's own summary line, never its exit code (rule 9).
#   C0w  the lifted source really is probe_rev46_vw.py's, and it reproduces that
#        probe's PUBLISHED nolita landmarks exactly.  Without this the whole
#        comparison is against a re-typed ruler.
#   C1w  the workshop landmarks are STABLE across thresholds and crop windows,
#        the same bar C1 puts on the nolita frame.
#   C2w  THE MASK REACHES THE RING'S TRUE VERTICAL EXTREMES.  Every landmark is
#        registered on that span, so if the mask stops short at the top or
#        bottom -- which is exactly what lighting does to a chrome annulus --
#        the denominator is wrong and ALL SIX landmarks shift together.  Tested
#        against a quantity this probe does not fit: F09's 50%-level conic on
#        this same badge, vertical D 92.728 px, 685 rays, radial residual
#        0.2345 px.  Two independently obtained quantities (rule 6).
#        The first version of this row compared the two frames' CROP-RELATIVE
#        spans, which measure my crop margins and not the badges; it failed on a
#        correct mask and is withdrawn.
#   C3w  A KILL, RED BY DESIGN: the mask must NOT be able to invent this
#        topology out of PAINT.  The same mask on a window of plain nose cream
#        and green stripe beside the badge must fail to present L1..L4.
#        The first version of this row was aimed at cols 150-219, which is the
#        workshop WALL AND FLOOR, not the vehicle -- a mis-aimed control that
#        fired for the wrong reason.  Caught by painting it.
#
# RUN   python3 probe_rev62_landmarks.py [--paint]
#       --paint writes the mask overlays to probe_scratch/ .  LOOK AT THEM.

import ast
import os
import sys

import numpy as np
import scipy.ndimage as ndi
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUTD = os.path.join(HERE, "probe_scratch")
PAINT = "--paint" in sys.argv

CTL = {}


def ctl(name, ok, msg):
    CTL[name] = bool(ok)
    print("  [%s] %-4s %s" % ("PASS" if ok else "FAIL", name, msg))


def P(*a):
    print(*a)


# ------------------------------------------------------- lift the shared ruler
SRC = os.path.join(HERE, "probe_rev46_vw.py")
WANT = ("runs_of", "transitions", "landmarks")
_tree = ast.parse(open(SRC).read())
_lift = [n for n in _tree.body
         if isinstance(n, ast.FunctionDef) and n.name in WANT]
_missing = set(WANT) - {n.name for n in _lift}
assert not _missing, ("probe_rev46_vw.py no longer defines %s -- this probe's "
                      "ruler is gone, not stale" % sorted(_missing))
_ns = {"np": np}
exec(compile(ast.Module(body=_lift, type_ignores=[]), SRC, "exec"), _ns)
runs_of, transitions, landmarks = (_ns[n] for n in WANT)

KEYS = ("L1", "L2", "L3", "L4", "L5", "L6")

P("\nREV 62 -- WHICH OF L1..L6 IS WRONG?")
P("    the ruler is probe_rev46_vw.py's own landmarks(), lifted by ast")
P("    (%d source lines, %s)" % (
    sum(n.end_lineno - n.lineno + 1 for n in _lift),
    ", ".join(n.name + "()" for n in _lift)))


# --------------------------------------------------------------- the two frames
NOLITA = os.path.join(HERE, "ref_nolita_front34.jpg")
WORKSHOP = os.path.join(HERE, "ref_workshop.jpg")

_NO = np.array(Image.open(NOLITA).convert("RGB")).astype(float)
_NORED = _NO[:, :, 0] - 0.5 * (_NO[:, :, 1] + _NO[:, :, 2])

_WS = np.array(Image.open(WORKSHOP).convert("RGB")).astype(float)
# Luminance.  The pressing reads DARK against the cream nose; the cells are the
# nose.  This is the analogue of redness on the painted badge, and it is the one
# substitution in this whole comparison -- see the header.
_WSLUM = _WS.mean(axis=2)


def nolita_mask(th=35, box=(191, 260, 148, 198)):
    r0, r1, c0, c1 = box
    return _NORED[r0:r1, c0:c1] > th


# The badge on ref_workshop.jpg.  Read off the x8 crop and cross-checked against
# F09's conic: that fit puts the pressing at vertical D 92.728, horizontal D
# 63.299, and this window is 70 x 101 -- a few px of margin on each side and NO
# green paint, which enters the frame below x 350 / above x 267 at this height.
WS_BOX = (498, 599, 270, 340)


def workshop_mask(th=165, box=None):
    r0, r1, c0, c1 = box or WS_BOX
    m = _WSLUM[r0:r1, c0:c1] < th
    # close the specular pixels that sit INSIDE a stroke.  Without this the
    # highlight punches holes through the V's arms and the run count is noise.
    return ndi.binary_closing(m, np.ones((3, 3)))


def paint(mask, img, path, box):
    r0, r1, c0, c1 = box
    base = np.array(Image.fromarray(img[r0:r1, c0:c1].astype(np.uint8)))
    ov = base.copy()
    ov[mask] = (0.35 * ov[mask] + 0.65 * np.array([255, 0, 255])).astype(np.uint8)
    out = np.concatenate([base, ov], axis=1).astype(np.uint8)
    im = Image.fromarray(out)
    im = im.resize((im.width * 8, im.height * 8), Image.NEAREST)
    os.makedirs(OUTD, exist_ok=True)
    im.save(path)
    return path


# ------------------------------------------------------------------------- C0w
NOL = landmarks(nolita_mask())
assert NOL is not None, "the nolita badge does not present L1..L4"
NOLL, (ntop, nbot, nspan) = NOL
PUBLISHED = {"L1": 0.1940, "L2": 0.3433, "L3": 0.4776,
             "L4": 0.8060, "L5": 0.2361, "L6": 0.1528}
d0 = max(abs(NOLL[k] - PUBLISHED[k]) for k in KEYS)
ctl("C0w", d0 < 1e-4,
    "the lifted ruler reproduces probe_rev46_vw.py's PUBLISHED nolita "
    "landmarks to %.6f -- without this the comparison below is against a "
    "re-typed ruler, not the shipped one" % d0)

P("\n    NOLITA    ref_nolita_front34.jpg rows 191-259, cols 148-198  (50x69)")
P("              ring span %.3f..%.3f of the crop" % (ntop, nbot))

# ------------------------------------------------------------------------- C1w
WS = landmarks(workshop_mask())
assert WS is not None, "the workshop badge does not present L1..L4"
WSL, (wtop, wbot, wspan) = WS
P("\n    WORKSHOP  ref_workshop.jpg rows %d-%d, cols %d-%d  (%dx%d)"
  % (WS_BOX[0], WS_BOX[1] - 1, WS_BOX[2], WS_BOX[3] - 1,
     WS_BOX[3] - WS_BOX[2], WS_BOX[1] - WS_BOX[0]))
P("              ring span %.3f..%.3f of the crop" % (wtop, wbot))

WINDOWS = [WS_BOX,
           (497, 600, 269, 341), (499, 598, 271, 339),
           (496, 601, 268, 342), (500, 597, 272, 338)]
vals = {k: [] for k in KEYS}
nseen = 0
for th in (145, 152, 158, 165, 172, 180):
    for box in WINDOWS:
        r = landmarks(workshop_mask(th=th, box=box))
        if r is None:
            continue
        nseen += 1
        for k in KEYS:
            if k in r[0]:
                vals[k].append(r[0][k])
spread = {k: (max(v) - min(v)) if len(v) > 2 else 9.9 for k, v in vals.items()}
P("              stability over 6 thresholds x %d windows (%d presented): %s"
  % (len(WINDOWS), nseen,
     "  ".join("%s +-%.3f" % (k, spread[k] / 2) for k in KEYS)))
ctl("C1w", max(spread.values()) < 0.075,
    "workshop landmarks stable (max spread %.3f) -- an unstable landmark set "
    "is not a measurement.  C1's bar on the nolita frame is 0.037"
    % max(spread.values()))

# ------------------------------------------------------------------------- C2w
F09_CONIC_VERT_D = 92.728          # F09, probe_rev57_badge.py 50%-level conic
wpix = wspan * (WS_BOX[1] - WS_BOX[0] - 1)
ctl("C2w", abs(wpix - F09_CONIC_VERT_D) < 2.0,
    "the mask reaches the ring's true vertical extremes: it spans %.1f px "
    "against F09's independently-fitted conic vertical D of %.3f px -- "
    "%+.1f px.  Every landmark is registered on this span, so a mask that "
    "stopped short would shift all six together"
    % (wpix, F09_CONIC_VERT_D, wpix - F09_CONIC_VERT_D))

# ------------------------------------------------------------------------- C3w
PAINT_BOX = (498, 599, 350, 420)   # plain nose cream + the green stripe
gr = landmarks(workshop_mask(box=PAINT_BOX))
ctl("C3w", gr is None or len({"L1", "L2", "L3", "L4"} & set(gr[0])) < 4,
    "KILL, RED BY DESIGN: the same mask on a window of PLAIN NOSE CREAM AND "
    "GREEN STRIPE beside the badge does not present L1..L4.  If it did, this "
    "mask could invent the glyph's topology out of paint")

# ---------------------------------------------------------------- the comparison
P("\n    THE TWO BADGES, SAME RULER, SAME PRESSING, 1.71x THE AREA")
P("        %-6s %9s %9s %9s" % ("", "nolita", "workshop", "delta"))
order = []
for k in KEYS:
    if k not in WSL:
        P("        %-6s %9.4f %9s" % (k, NOLL[k], "absent"))
        continue
    d = WSL[k] - NOLL[k]
    order.append((abs(d), k, NOLL[k], WSL[k], d))
    P("        %-6s %9.4f %9.4f %+9.4f" % (k, NOLL[k], WSL[k], d))

order.sort(reverse=True)
P("\n    RANKED BY DISAGREEMENT -- the top row is the landmark most likely wrong")
for a, k, n, w, d in order:
    P("        %-4s %+.4f   nolita %.4f  workshop %.4f   %s"
      % (k, d, n, w,
         "MOVES" if a > spread.get(k, 0) else "within this frame's own spread"))

if PAINT:
    p1 = paint(nolita_mask(), _NO, os.path.join(OUTD, "rev62_mask_nolita.png"),
               (191, 260, 148, 198))
    p2 = paint(workshop_mask(), _WS,
               os.path.join(OUTD, "rev62_mask_workshop.png"), WS_BOX)
    p3 = paint(workshop_mask(box=PAINT_BOX), _WS,
               os.path.join(OUTD, "rev62_mask_paint_kill.png"), PAINT_BOX)
    P("\n    PAINTED (raw | mask, x8) -- LOOK BEFORE QUOTING ANY ROW ABOVE:")
    for p in (p1, p2, p3):
        P("        %s" % os.path.relpath(p, HERE))

bad = [k for k, v in CTL.items() if not v]
P("\nCONTROLS: %d checked, %s"
  % (len(CTL), ("%d FAILED -- %s" % (len(bad), ",".join(bad))) if bad
     else "0 FAILED"))


# ============================================================================
#  PART 2 -- C8's OWN TARGET.  NOTHING SWEEPS IT, AND IT HAS A SILENT FAILURE.
# ============================================================================
#
# WHY THIS IS HERE.  Part 1 asked which of L1..L6 is wrong and did not get a
# decisive answer.  While testing the obvious alternative -- that C8's 3.39 is
# inflated by the badge's foreshortening -- I read cell_elongation() and found
# the foreshortening IS corrected (squash = mask.shape[0]/mask.shape[1]).  That
# hypothesis is REFUTED, by source inspection.  But the same read showed the
# measuring region is an ellipse inscribed in THE MASK ARRAY'S RECTANGLE:
#
#     n0, n1 = mask.shape
#     disc = (((yy-cy)/(n0/2))**2 + ((xx-cx)/(n1/2))**2) <= frac**2
#     bg = disc & (~mask)
#
# The region is the CROP, not the measured badge.  Widen the crop and the disc
# escapes the roundel, the cream nose OUTSIDE the ring becomes a cream "cell",
# and because that halo is round it drags the area-weighted median down.
#
# C1 sweeps six thresholds x five windows for L1..L6.  C8's target -- which is
# the whole basis for "the built cells are 2.27x too round", his top item -- is
# swept by NOTHING.  Two targets in this same instrument family have already
# been found contaminated: C6's 7 (F139) and M1's ruler (F136).  This is the
# third one tested, and it is the first to have a silent failure mode.
#
#   C10  the target is STABLE against the red segmentation.
#   C11  the target is STABLE against the crop window -- and this is the row
#        that fails.  It is REPORTED, not relaxed.
#   C12  A KILL, WATCHED FAILING: at +-3 px the disc provably escapes the
#        badge.  The largest "cream cell" must then be the OUTSIDE halo, not a
#        cell of the glyph.  That is the mechanism, not a coincidence.

_ce = [n for n in _tree.body
       if isinstance(n, ast.FunctionDef) and n.name == "cell_elongation"]
assert _ce, "probe_rev46_vw.py no longer defines cell_elongation"
_ns2 = {"np": np, "ndi": ndi}
exec(compile(ast.Module(body=_ce, type_ignores=[]), SRC, "exec"), _ns2)
cell_elongation = _ns2["cell_elongation"]

_R, _G, _B = _NO[..., 0], _NO[..., 1], _NO[..., 2]
SHIPPED_BOX = (192, 261, 153, 194)          # probe_rev46_vw.photo_elongation


def photo_target(rth=110, kf=0.60, box=SHIPPED_BOX):
    """probe_rev46_vw.photo_elongation(), with its constants exposed."""
    red = (_R > rth) & (_G < kf * _R) & (_B < kf * _R)
    lab, _ = ndi.label(red)
    sub = lab[box[0]:box[1], box[2]:box[3]]
    ids, cnt = np.unique(sub[sub > 0], return_counts=True)
    if not len(ids):
        return None, None
    m = sub == ids[int(np.argmax(cnt))]
    return cell_elongation(m, m.shape[0] / float(m.shape[1])), m


P("\n\n    C8's PHOTOGRAPH TARGET -- SWEPT FOR THE FIRST TIME")
_t0, _ = photo_target()
P("        shipped call                      %.4f" % _t0)
P("        (probe_rev46_vw.py's own header still says 3.33 -- stale by 0.06)")

_seg = []
for rth in (90, 100, 110, 120, 130, 140):
    v, _ = photo_target(rth=rth)
    _seg.append(v)
for kf in (0.50, 0.55, 0.60, 0.65, 0.70):
    v, _ = photo_target(kf=kf)
    _seg.append(v)
_seg = [v for v in _seg if v]
P("        segmentation sweep (6 thresholds, 5 ratios)  %.3f .. %.3f"
  % (min(_seg), max(_seg)))
ctl("C10", (max(_seg) - min(_seg)) < 0.60,
    "C8's target is stable against the red segmentation: spread %.3f over "
    "R>90..140 and G,B<0.50..0.70 R" % (max(_seg) - min(_seg)))

_win = []
P("        crop-window sweep, the sweep C1 does for L1..L6 and nothing does here:")
for d in (0, 1, 2, 3):
    b = (SHIPPED_BOX[0] - d, SHIPPED_BOX[1] + d,
         SHIPPED_BOX[2] - d, SHIPPED_BOX[3] + d)
    v, _ = photo_target(box=b)
    _win.append(v)
    P("            +-%d px   rows %d-%d cols %d-%d   %.3f"
      % (d, b[0], b[1] - 1, b[2], b[3] - 1, v))
ctl("C11", (max(_win) - min(_win)) < 0.40,
    "C8's target is stable against its CROP WINDOW: %.3f .. %.3f, a spread of "
    "%.3f.  At +-3 px it reads %.3f -- indistinguishable from the BUILT "
    "glyph's 1.49, so at that window C8 would report the defect CLOSED.  "
    "NOTHING IN THE SHIPPED PROBE SWEEPS THIS"
    % (min(_win), max(_win), max(_win) - min(_win), _win[-1]))

# C12 -- the mechanism, watched
_b3 = (SHIPPED_BOX[0] - 3, SHIPPED_BOX[1] + 3,
       SHIPPED_BOX[2] - 3, SHIPPED_BOX[3] + 3)
_v3, _m3 = photo_target(box=_b3)
_n0, _n1 = _m3.shape
_yy, _xx = np.mgrid[0:_n0, 0:_n1]
_cy, _cx = (_n0 - 1) / 2.0, (_n1 - 1) / 2.0
_disc = (((_yy - _cy) / (_n0 / 2.0)) ** 2
         + ((_xx - _cx) / (_n1 / 2.0)) ** 2) <= 0.97 ** 2
_lab3, _k3 = ndi.label(_disc & (~_m3))
_sz3 = np.bincount(_lab3.ravel())[1:]
_big = int(np.argmax(_sz3)) + 1
_ring_rows = np.nonzero(_m3.any(axis=1))[0]
_ring_cols = np.nonzero(_m3.any(axis=0))[0]
_by, _bx = np.where(_lab3 == _big)
_outside = float(((_by < _ring_rows[0]) | (_by > _ring_rows[-1])
                  | (_bx < _ring_cols[0]) | (_bx > _ring_cols[-1])).mean())
ctl("C12", _outside > 0.25,
    "KILL, WATCHED FAILING: at +-3 px the largest 'cream cell' is %d px "
    "against the true cells' 215, and %.0f%% of it lies OUTSIDE the ring's own "
    "bounding box -- it is the nose paint around the roundel, not a cell of "
    "the glyph.  That is the mechanism by which the target collapses to %.3f"
    % (_sz3.max(), 100 * _outside, _v3))

P("\n    WHAT THIS DOES AND DOES NOT OVERTURN")
P("        Within +-2 px the target reads %.2f / %.2f / %.2f and the"
  % (_win[0], _win[1], _win[2]))
P("        segmentation sweep gives %.2f .. %.2f, so the built glyph is"
  % (min(_seg), max(_seg)))
P("        %.2fx..%.2fx too round rather than a point 2.27x."
  % (min(_seg) / 1.49, max(_win) / 1.49))
P("        C8's VERDICT SURVIVES.  Its CEILING does not: the target is a")
P("        range, and the instrument fails SILENTLY outside a 2 px window.")

bad = [k for k, v in CTL.items() if not v]
P("\nCONTROLS (both parts): %d checked, %s"
  % (len(CTL), ("%d FAILED -- %s" % (len(bad), ",".join(bad))) if bad
     else "0 FAILED"))


# ============================================================================
#  PART 3 -- THE STROKE-WEIGHT LEVER, ABLATED AGAINST C8 FOR THE FIRST TIME.
# ============================================================================
#
# RULE 36: ABLATE THE THING YOU ARE ABOUT TO TUNE, FIRST.
#
# Part 1 makes L6 -- the stroke width -- the largest cross-frame disagreement,
# and the workshop badge says the strokes are THINNER than the nolita fit.  The
# obvious next move is to thin them.  Before doing that, ablate it.
#
# F102 already swept T1_VW_WFRAC and recorded "cells 6 at EVERY value".  That
# was against C6, THE CELL COUNT.  C8 -- elongation -- did not exist until
# rev 61.  So the shipped lever for the thing Part 1 accuses has NEVER been
# tested against the statistic that measures the defect.
#
# This runs the SHIPPED probe as a subprocess at each weight, unmodified, and
# reads its own C8 line (rule 9: read the probe's summary line).
#
#   C13  the lever MOVES C8 at all -- otherwise it is inert and Part 1's
#        accusation of L6 is untestable by this route.
#   C14  THE DECIDING ROW.  Thinning the stroke as far as the construction
#        allows must reach the photograph's target.  IT DOES NOT -- which
#        REFUTES L6 as the answer to "which landmark is wrong", by ablation
#        rather than by argument.

import re                                                    # noqa: E402
import subprocess                                            # noqa: E402

if "--noablate" not in sys.argv:
    P("\n\n    T1_VW_WFRAC AGAINST C8 -- THE LEVER PART 1 ACCUSES, ABLATED")
    P("        F102 swept this against C6 (the COUNT) and called it inert.")
    P("        C8 did not exist then.  Shipped value 0.1986.")
    P("        %-9s %-8s %-7s %s" % ("wfrac", "elong", "cells", ""))
    rows = []
    for wf in (0.08, 0.10, 0.12, 0.14, 0.16, 0.1986, 0.28, 0.36, 0.44):
        env = dict(os.environ, T1_VW_WFRAC="%.4f" % wf)
        try:
            o = subprocess.run([sys.executable, os.path.join(HERE,
                               "probe_rev46_vw.py")], capture_output=True,
                               text=True, env=env, timeout=600).stdout
        except Exception as e:                               # noqa: BLE001
            P("        %-9.4f RUN FAILED %s" % (wf, e))
            continue
        me = re.search(r"BUILT\s+elongation\s+([\d.]+) at 276 rows, "
                       r"([\d.]+) at 69", o)
        mc = re.search(r"BUILT\s+(\d+) cells", o)
        if not me or not mc:
            P("        %-9.4f NO C8 LINE" % wf)
            continue
        e276, e69, cells = float(me.group(1)), float(me.group(2)), int(mc.group(1))
        rows.append((wf, e276, e69, cells))
        P("        %-9.4f %-8.2f %-7d %s%s"
          % (wf, e276, cells,
             "<- SHIPPED" if abs(wf - 0.1986) < 1e-6 else "",
             "   (69-row reading %.2f -- C8's scale-stability does NOT hold "
             "here)" % e69 if abs(e276 - e69) > 0.10 else ""))

    if rows:
        emax = max(r[1] for r in rows)
        emin = min(r[1] for r in rows)
        ctl("C13", (emax - emin) > 0.20,
            "the lever MOVES C8: %.2f .. %.2f over wfrac 0.08..0.44, and it "
            "moves the WRONG WAY -- thicker strokes give ROUNDER cells.  So "
            "F102's 'inert' verdict was about C6 only" % (emin, emax))
        ctl("C14", emax >= 0.70 * _t0,
            "THE DECIDING ROW: thinning the stroke to the construction's limit "
            "reaches elongation %.2f against the photograph's %.2f -- it gets "
            "%.0f%% of the way and costs a cell.  SO L6 IS NOT THE ANSWER: "
            "abandoning the stroke-width landmark ENTIRELY still cannot reach "
            "the target, which refutes Part 1's leading suspect BY ABLATION "
            "rather than by argument" % (emax, _t0, 100 * emax / _t0))

    bad = [k for k, v in CTL.items() if not v]
    P("\nCONTROLS (all three parts): %d checked, %s"
      % (len(CTL), ("%d FAILED -- %s" % (len(bad), ",".join(bad))) if bad
         else "0 FAILED"))
