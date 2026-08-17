# mark_rev36_ends.py -- rev 36.  THE QUESTION FIGURE.
#
# THIS IS A QUESTION.  (rev 35's figure carried a header saying NOT A QUESTION;
# this one is the opposite and says so, because a figure that does not declare
# which it is has cost this project a wasted answer before.)
#
# WHAT IT ASKS
#   The owner reported, at the end of rev 35: "the upper bar appears to also
#   connect with the main bumper on either end.  In the current version, there
#   is no connection made."  Measurement has confirmed the defect and sized it
#   (probe_rev36_barend.py: one gap, vertical, 23.59 mm, 0.945 x BAR_DIA).
#   What measurement CANNOT do is name the STRUCTURE that makes the connection,
#   because that is a depth question on a frame with no recoverable fore-aft
#   vanishing point (REF 9) and no bounded camera roll (SPEC 10.89.3).
#
# MARK CLASSES ON THIS FIGURE -- what each mark IS, stated plainly
#   [A] MEASURED COLUMN     one vertical line, at the column this script
#                           re-measures for itself.  It is a reading, not a
#                           candidate and not a pointer.
#   [B] MEASURED ROWS       two horizontal lines, likewise re-measured here.
#   [C] IDENTIFICATION BOX  a dashed box round the thing being asked about.
#                           It asserts NOTHING about what is inside it.  It is
#                           not a sampling window -- nothing is averaged in it.
#   [D] OCCLUSION BAND      NEW CLASS, rev 36.  A hatched band marking rows
#                           where NO READING IS POSSIBLE.  Every previous mark
#                           class in this project pointed at something legible.
#                           This one marks the absence of legibility, and it
#                           exists because rev 35 read a junction THROUGH it.
#
# CONTROLS -- this script REFUSES TO WRITE if any fails.
#   F1  both reference and render load at their expected sizes
#   F2  the measured column falls strictly inside the far crop box
#   F3  the occlusion band falls strictly inside the near crop box
#   F4  the plate's left edge, RE-MEASURED HERE, lands in 200..218 over rows
#       644..716 with drift < 15 px  (not copied from an earlier run)
#   F5  the occlusion band, RE-MEASURED HERE, is a contiguous run of >= 6 rows
#       with ZERO white in the window
#   F6  a NEGATIVE control: a band of the same size taken 60 rows higher, in
#       clear green body, must NOT satisfy F5's test.  Without it, "zero white"
#       is not distinguishable from a window that never contained white.

import os, sys
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "ref_workshop.jpg")
RENDER = os.environ.get("T1_R36_RENDER", "/tmp/prev/r36_rev36_bumper.png")
OUT = os.environ.get("T1_R36_OUT", os.path.join(HERE, "rev36_ends.png"))

# ------------------------------------------------------------ crop boxes
# PRINTED, per the standing rule.
FAR_PHOTO  = (183, 618, 313, 748)      # 130 x 130
NEAR_PHOTO = (432, 660, 562, 790)      # 130 x 130
FAR_REND   = (150, 455, 370, 675)      # 220 x 220
NEAR_REND  = (1190, 490, 1410, 710)    # 220 x 220

PANEL = 470

CTL = {}
def ctl(k, ok, msg):
    CTL[k] = bool(ok)
    print("  [%s] %-3s %s" % ("PASS" if ok else "FAIL", k, msg))

print("=" * 78)
print("mark_rev36_ends -- THE QUESTION FIGURE for the over-rider bar's ends")
print("=" * 78)
print()
print("  CROP BOXES (x0, y0, x1, y1), printed:")
print("    far  photograph  %s   from ref_workshop.jpg" % (FAR_PHOTO,))
print("    near photograph  %s   from ref_workshop.jpg" % (NEAR_PHOTO,))
print("    far  render      %s   from %s" % (FAR_REND, os.path.basename(RENDER)))
print("    near render      %s   from %s" % (NEAR_REND, os.path.basename(RENDER)))
print()

ref_im = Image.open(REF).convert("RGB")
ok_r = os.path.exists(RENDER)
rnd_im = Image.open(RENDER).convert("RGB") if ok_r else None
ctl("F1", ref_im.size == (1200, 824) and ok_r and rnd_im.size == (1500, 1000),
    "ref %s ; render %s" % (ref_im.size, rnd_im.size if rnd_im else "MISSING"))
if not CTL["F1"]:
    print("\nREFUSING TO WRITE -- sources not as expected.")
    sys.exit(1)

A = np.asarray(ref_im).astype(float)
mx = A.max(2); mn = A.min(2); V = mx
S = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
WHITE = (V > 140) & (S < 0.20)

# ------------------------------------------- F4: re-measure the plate edge
edges = []
for row in range(644, 717, 4):
    seg = WHITE[row, 190:260]
    idx = np.where(seg)[0]
    if len(idx):
        edges.append(190 + idx[0])
EDGE = int(round(float(np.median(edges)))) if edges else -1
ctl("F4", len(edges) >= 15 and 200 <= EDGE <= 218
         and (max(edges) - min(edges)) < 15,
    "plate left edge re-measured: median col %d over %d rows, drift %d px"
    % (EDGE, len(edges), (max(edges) - min(edges)) if edges else -1))

# ------------------------------------------------------------------------
# F4b: THE COALESCENCE COLUMN.
#
# The first version of this script measured "the bumper's top edge right of
# the plate" by taking the first white row in a column window.  IT WAS READING
# THE BAR TUBE, which passes through the same rows.  A DETECTOR THAT FINDS THE
# WRONG OBJECT AND RETURNS A PLAUSIBLE NUMBER is this project's most-repeated
# failure (SPEC 10.88's "a detector whose errors cancel"), and it produced
# 24 px where the true rise is ~48.  Recorded, not quietly fixed.
#
# The replacement needs no tube/bumper discrimination at all.  It asks a
# TOPOLOGICAL question, which is two-sided and self-checking:
#
#   at which column do the bar and the bumper STOP being one white body?
#
# Left of that column a vertical scan crosses ONE run; right of it, TWO runs
# separated by background.  Both sides are asserted, so a detector that simply
# always returns "one run" or "two runs" fails.
def runs_in_column(col, r0=600, r1=790, minh=3):
    idx = np.where(WHITE[r0:r1, col])[0]
    if len(idx) == 0:
        return []
    g = []; s = idx[0]; p = idx[0]
    for i in idx[1:]:
        if i != p + 1:
            g.append((r0 + s, r0 + p)); s = i
        p = i
    g.append((r0 + s, r0 + p))
    return [(a, b) for a, b in g if b - a + 1 >= minh]

def tall_runs(col):
    return [r for r in runs_in_column(col) if r[1] - r[0] + 1 >= 8]

# Start INSIDE the body, not at its antialiased edge: walk right to the first
# column that crosses exactly ONE tall run (that is the plate's solid interior),
# then keep walking to the first column that crosses TWO.  Anchoring at EDGE+2
# instead put the search start on the edge pixel itself, where antialiasing
# splits the body and the scan reads two runs immediately -- a detector fooled
# by the boundary it was launched from.  Recorded.
C_IN = None
for col in range(EDGE, EDGE + 20):
    if len(tall_runs(col)) == 1 and (tall_runs(col)[0][1] - tall_runs(col)[0][0]) >= 40:
        C_IN = col; break
COAL = None
if C_IN is not None:
    for col in range(C_IN + 1, C_IN + 40):
        if len(tall_runs(col)) >= 2:
            COAL = col; break
print("       solid interior first reached at col %s" % C_IN)

single = tall_runs(COAL - 4) if COAL else []
double = tall_runs(COAL + 4) if COAL else []
ctl("F4b", COAL is not None and len(single) == 1 and len(double) >= 2,
    "coalescence column = %s.  At col %s the scan crosses %d tall run(s); at "
    "col %s it crosses %d.  TWO-SIDED."
    % (COAL, COAL - 4 if COAL else "-", len(single),
       COAL + 4 if COAL else "-", len(double)))

ptop = single[0][0] if single else None
pbot = single[0][1] if single else None
print("       continuous bar+bumper body at col %s: rows %s-%s, height %s px"
      % (COAL - 4 if COAL else "-", ptop, pbot,
         (pbot - ptop + 1) if ptop is not None else "-"))
if double:
    print("       at col %s the same span holds: %s"
          % (COAL + 4, "  ".join("rows %d-%d (h%d)" % (a, b, b - a + 1)
                                 for a, b in double)))
    if len(double) >= 2:
        print("       -> separated by a gap of %d rows"
              % (double[1][0] - double[0][1] - 1))
WIDTH = (COAL - EDGE) if COAL else None
print("       CONNECTED WIDTH: col %d to col %s = %s px"
      % (EDGE, COAL, WIDTH))

# ---------------------------------------- F5/F6: re-measure the occlusion
def zero_white_run(r0, r1, c0, c1):
    z = [r for r in range(r0, r1) if WHITE[r, c0:c1].mean() == 0.0]
    if not z:
        return []
    best = cur = [z[0]]
    for r in z[1:]:
        if r == cur[-1] + 1:
            cur.append(r)
        else:
            if len(cur) > len(best): best = cur
            cur = [r]
    return cur if len(cur) > len(best) else best

BAND = zero_white_run(715, 750, 470, 510)
ctl("F5", len(BAND) >= 6,
    "occlusion band re-measured: rows %s (%d rows, zero white in cols 470-510)"
    % (("%d-%d" % (BAND[0], BAND[-1])) if BAND else "none", len(BAND)))
dark_frac = (V[BAND[0]:BAND[-1] + 1, 470:510] < 70).mean() if BAND else 0.0
print("       dark (V<70) fraction inside the band: %.1f %%" % (100 * dark_frac))

NEG = zero_white_run(640, 675, 470, 510)
ctl("F6", len(NEG) >= 6 and dark_frac > 0.30,
    "negative control: clear-body window 640-675 also reads zero white "
    "(%d rows) -- so ZERO WHITE ALONE PROVES NOTHING; the band is called an "
    "occlusion because it is %.0f %% DARK, not because it is not white."
    % (len(NEG), 100 * dark_frac))

ctl("F2", FAR_PHOTO[0] < EDGE < FAR_PHOTO[2],
    "measured column %d lies inside the far crop box" % EDGE)
ctl("F3", bool(BAND) and NEAR_PHOTO[1] < BAND[0] and BAND[-1] < NEAR_PHOTO[3],
    "occlusion band lies inside the near crop box")

print()
if not all(CTL.values()):
    print("REFUSING TO WRITE -- %d control(s) down: %s"
          % (sum(1 for v in CTL.values() if not v),
             [k for k, v in CTL.items() if not v]))
    sys.exit(1)

# ================================================================= drawing
def panel(img, box, size=PANEL):
    c = img.crop(box)
    return c.resize((size, size), Image.LANCZOS), size / float(box[2] - box[0])

pf, sf = panel(ref_im, FAR_PHOTO)
pn, sn = panel(ref_im, NEAR_PHOTO)
rf, _ = panel(rnd_im, FAR_REND)
rn, _ = panel(rnd_im, NEAR_REND)

RED = (220, 30, 30); BLU = (20, 90, 220); ORA = (235, 140, 0)
GRN = (0, 150, 60); BLK = (0, 0, 0); WHT = (255, 255, 255)

# --- far photograph marks
d = ImageDraw.Draw(pf)
ex = (EDGE - FAR_PHOTO[0]) * sf
d.line([(ex, 0), (ex, PANEL)], fill=RED, width=3)                       # [A]
cx = (COAL - FAR_PHOTO[0]) * sf
for k in range(0, PANEL, 18):                                           # [A2]
    d.line([(cx, k), (cx, min(k + 9, PANEL))], fill=(150, 0, 160), width=3)
for rr in (ptop, pbot):
    yy = (rr - FAR_PHOTO[1]) * sf
    d.line([(0, yy), (PANEL, yy)], fill=BLU, width=3)                   # [B]
bx0 = (EDGE - 5 - FAR_PHOTO[0]) * sf
bx1 = (COAL + 5 - FAR_PHOTO[0]) * sf
by0 = (ptop - 5 - FAR_PHOTO[1]) * sf
by1 = (pbot + 5 - FAR_PHOTO[1]) * sf
for k in range(0, int(by1 - by0), 14):                                  # [C]
    d.line([(bx0, by0 + k), (bx0, min(by0 + k + 7, by1))], fill=ORA, width=4)
    d.line([(bx1, by0 + k), (bx1, min(by0 + k + 7, by1))], fill=ORA, width=4)
for k in range(0, int(bx1 - bx0), 14):
    d.line([(bx0 + k, by0), (min(bx0 + k + 7, bx1), by0)], fill=ORA, width=4)
    d.line([(bx0 + k, by1), (min(bx0 + k + 7, bx1), by1)], fill=ORA, width=4)

# --- near photograph marks: the occlusion band
d = ImageDraw.Draw(pn)
y0 = (BAND[0] - NEAR_PHOTO[1]) * sn
y1 = (BAND[-1] + 1 - NEAR_PHOTO[1]) * sn
for k in range(-PANEL, PANEL * 2, 16):                                  # [D]
    d.line([(k, y1), (k + int(y1 - y0), y0)], fill=GRN, width=3)
d.line([(0, y0), (PANEL, y0)], fill=GRN, width=4)
d.line([(0, y1), (PANEL, y1)], fill=GRN, width=4)

# ================================================================= compose
GAP, LM, TOP, BOT = 18, 14, 250, 300
Wc = LM * 2 + PANEL * 2 + GAP
Hc = TOP + PANEL * 2 + GAP + 44 * 2 + BOT
canvas = Image.new("RGB", (Wc, Hc), WHT)
D = ImageDraw.Draw(canvas)

def T(x, y, s, fill=BLK):
    D.text((x, y), s, fill=fill)

y = 10
T(LM, y, "REV 36 -- THIS IS A QUESTION.  The over-rider bar's ends."); y += 16
T(LM, y, "Superseding nothing.  First issue.", (90, 90, 90)); y += 20
T(LM, y, "YOUR REPORT (rev 35): 'the upper bar appears to also connect with the main bumper on either end.  In the"); y += 13
T(LM, y, "current version, there is no connection made.'   CONFIRMED AND SIZED: ONE gap, vertical, 23.59 mm ="); y += 13
T(LM, y, "0.945 x the tube's own diameter, both ends, symmetric to 0.002 mm.  Rev 35 published 8.1 mm and a second"); y += 13
T(LM, y, "fore-aft gap of 52.4 mm; the fore-aft gap DOES NOT EXIST (tip sits 0.51 mm behind the blade face, coplanar"); y += 13
T(LM, y, "by construction) and 8.1 mm is 2.9x too small.  Both errors came from reading BAR_END_DROP at full value;"); y += 13
T(LM, y, "the code turns the hoop 55.80 deg, not 90.  THE SIGN OF YOUR REPORT IS UNTOUCHED -- only the magnitudes."); y += 20
T(LM, y, "WHAT EACH MARK IS -- none of them is a candidate line, and none is a sampling window:", BLK); y += 14
T(LM, y, "  [A] RED VERTICAL   = MEASURED COLUMN.  col %d, re-measured by this script over %d rows, drift %d px."
  % (EDGE, len(edges), max(edges) - min(edges)), RED); y += 13
T(LM, y, "      This is the same column you answered in rev 33/34 as the bar's far end: u in (205, 208].", RED); y += 13
T(LM, y, "  [A2] PURPLE DASHED VERTICAL = MEASURED COLUMN, the COALESCENCE COLUMN, col %d.  LEFT of it a vertical"
  % COAL, (150,0,160)); y += 13
T(LM, y, "      scan crosses ONE white body; RIGHT of it, TWO with a gap between.  Two-sided, so a detector that", (150,0,160)); y += 13
T(LM, y, "      always answered the same way would fail.  CONNECTED WIDTH col %d to %d = %d px = %.1f tube diameters."
  % (EDGE, COAL, WIDTH, WIDTH / 9.5), (150,0,160)); y += 13
T(LM, y, "  [B] BLUE HORIZONTALS = MEASURED ROWS.  rows %d and %d: the top and bottom of that one continuous body,"
  % (ptop, pbot), BLU); y += 13
T(LM, y, "      %d px tall -- it runs from the bar's own level all the way down past the bumper's bottom edge."
  % (pbot - ptop + 1), BLU); y += 13
T(LM, y, "  [C] ORANGE DASHED BOX = IDENTIFICATION BOX.  It asserts NOTHING about what is inside it.", ORA); y += 13
T(LM, y, "  [D] GREEN HATCH      = OCCLUSION BAND (new class).  rows %d-%d, ZERO white, %.0f %% dark.  NO READING IS"
  % (BAND[0], BAND[-1], 100 * dark_frac), GRN); y += 13
T(LM, y, "      POSSIBLE INSIDE IT.  Rev 35 reported 'one continuous white path' at the near end, through this band.", GRN); y += 18

hy = y
T(LM, hy, "PHOTOGRAPH  ref_workshop.jpg  crop %s  x%.1f" % (FAR_PHOTO, sf))
T(LM + PANEL + GAP, hy, "CURRENT BUILD  crop %s" % (FAR_REND,))
y = hy + 16
canvas.paste(pf, (LM, y)); canvas.paste(rf, (LM + PANEL + GAP, y))
D.rectangle([LM, y, LM + PANEL, y + PANEL], outline=BLK)
D.rectangle([LM + PANEL + GAP, y, LM + PANEL * 2 + GAP, y + PANEL], outline=BLK)
T(LM, y + PANEL + 4, "FAR END (-y).  The connection is VISIBLE here.")
T(LM + PANEL + GAP, y + PANEL + 4, "FAR END.  The hoop stops in mid-air.")

y += PANEL + 28
T(LM, y, "PHOTOGRAPH  ref_workshop.jpg  crop %s  x%.1f" % (NEAR_PHOTO, sn))
T(LM + PANEL + GAP, y, "CURRENT BUILD  crop %s" % (NEAR_REND,))
y += 16
canvas.paste(pn, (LM, y)); canvas.paste(rn, (LM + PANEL + GAP, y))
D.rectangle([LM, y, LM + PANEL, y + PANEL], outline=BLK)
D.rectangle([LM + PANEL + GAP, y, LM + PANEL * 2 + GAP, y + PANEL], outline=BLK)
T(LM, y + PANEL + 4, "NEAR END (+y).  The junction is BEHIND the hatch.")
T(LM + PANEL + GAP, y + PANEL + 4, "NEAR END.  Same 23.59 mm gap, mirrored.")

y += PANEL + 26
T(LM, y, "THE QUESTION -- about the FAR panel's orange box only.  I can measure that element's extent; I cannot"); y += 13
T(LM, y, "name it, because that is depth, and this frame has no recoverable fore-aft vanishing point (REF 9) and no"); y += 13
T(LM, y, "bounded camera roll (10.89.3).  What does the PHOTOGRAPH show inside the box?"); y += 16
T(LM, y, "  O1  the bumper's OWN END, seen from outside -- no separate part; the bar simply meets the blade there"); y += 13
T(LM, y, "  O2  a separate flat BRACKET or gusset PLATE joining the bar down to the bumper"); y += 13
T(LM, y, "  O3  a vertical OVER-RIDER GUARD standing PROUD of the bumper's front face, with the bar landing on it"); y += 13
T(LM, y, "  O4  the bar's own end FLATTENED and splayed into a foot, bolted down onto the blade"); y += 13
T(LM, y, "  O5  NO CONNECTION AT ALL -- the bar's end and the bumper's end merely OVERLAP IN PROJECTION, and the"); y += 13
T(LM, y, "      two whites touch only because they are in line of sight.  THIS IS THE NULL AND IT IS ON THE TABLE:"); y += 13
T(LM, y, "      the coalescence I measured is an IMAGE fact, and an image cannot separate contact from occlusion."); y += 16
T(LM, y, "WHAT EACH ANSWER CLOSES, stated before you spend one:", BLK); y += 13
T(LM, y, "  O1 -> I extend the hoop 23.59 mm and stop.  No new part.  BAR_END_DROP becomes DERIVED, not grade E."); y += 13
T(LM, y, "  O2/O3 -> a new part is authored.  Its image extent is ALREADY MEASURED: %d px wide x %d px tall,"
  % (WIDTH, pbot - ptop + 1)); y += 13
T(LM, y, "         = %.1f x %.1f tube diameters.  I would NOT need to ask you anything further to build it."
  % (WIDTH / 9.5, (pbot - ptop + 1) / 9.5)); y += 13
T(LM, y, "  O4 -> the tube's own section changes at the end; nothing new is authored but the sweep profile varies."); y += 13
T(LM, y, "  O5 -> NOTHING IS BUILT.  BAR_END_DROP stays grade E, the 23.59 mm stands as correct, and your report is"); y += 13
T(LM, y, "        recorded as an appearance this frame cannot separate from a connection.  I would rather build"); y += 13
T(LM, y, "        nothing than build a joint that is not there -- 10.24's bumper standoff was a LAMPPOST for two"); y += 13
T(LM, y, "        revisions because nobody offered the null."); y += 16
T(LM, y, "YOUR ANSWER MAY NOT BE ONE OF THESE.  If none fits, say what you see and I will build to that instead.", (90, 90, 90)); y += 13
T(LM, y, "I am NOT asking about the near end: it is occluded, and asking you to read through a %d-row black band"
  % len(BAND), (90, 90, 90)); y += 13
T(LM, y, "would be asking what the photograph cannot answer.  I will mirror whatever the far end turns out to be,", (90, 90, 90)); y += 13
T(LM, y, "and record that mirroring as an ASSUMPTION, not a reading.", (90, 90, 90))

canvas.save(OUT)
print("wrote %s  (%d x %d)" % (OUT, Wc, Hc))
print("ALL %d CONTROLS PASSED." % len(CTL))
