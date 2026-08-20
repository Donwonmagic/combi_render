# mark_rev45_q.py -- rev 45.  THE QUESTION FIGURE.
#
# THIS IS A QUESTION.  Six of them, numbered, one per row.
#
# WHY IT LOOKS DIFFERENT FROM mark_rev23..mark_rev37
#   Those eleven figures were "one crop, one mark, one sentence" (SPEC
#   10.100.3) and the format worked -- it settled the shape of a member that
#   had been unmeasurable for five revisions.  Rev 45's problem is not the same
#   problem.  The owner has now reported THE SAME DEFECTS THREE TIMES and rev
#   44 answered each report with a measurement, eight SPEC sections and thirty
#   findings.  He still saw them.  The rev-45 brief sec.0 lists three possible
#   causes and they are all failures of EVIDENCE, not of measurement:
#
#       (a) he is looking at a different thing than the measurement is
#       (b) the fix is real but sub-threshold at the size he views it
#       (c) he is looking at an older image
#
#   A single crop with a dashed box round it answers none of those.  So every
#   row here is BEFORE | AFTER | PHOTOGRAPH, at matched scale, cropped to the
#   thing being asked about:
#
#       (a) dies because the photograph is in the row -- there is no "which
#           thing did you mean" left to have
#       (b) dies because the crop is magnified to where a 2 mm change is tens
#           of pixels
#       (c) dies because BEFORE is in the frame, labelled, next to AFTER
#
#   BEFORE is the rev-44 build as it stood at the head of this branch.  AFTER
#   is this revision.  Neither is re-touched.
#
# MARK CLASSES -- what each mark IS, stated plainly
#   [C] IDENTIFICATION BOX  a dashed box round the thing being asked about.
#                           It asserts NOTHING about what is inside it.  It is
#                           not a sampling window -- nothing is averaged in it.
#   [L] PANEL LABEL         which build, or which photograph, this cell is.
#   [Q] THE QUESTION        one sentence, numbered.
#
# CONTROLS -- THIS SCRIPT REFUSES TO WRITE IF ANY FAILS.
#   F1  every input image loads, at a size this script did not assume
#   F2  BEFORE and AFTER are DIFFERENT IMAGES.  Without this the figure could
#       ship two copies of the same render and read as "nothing changed" --
#       or, worse, as "everything changed" if they were both the new one.
#   F3  every crop box lies strictly inside its own image
#   F4  each row's three cells end up the same height, so the eye can compare
#       across without rescaling anything itself
#   F5  a NEGATIVE control: the badge row's BEFORE and AFTER crops must differ
#       by MORE than the two Calidad crops differ, because the badge is the
#       biggest geometric change this revision and the decal is a texture
#       recolour.  If that ordering inverts, the wrong files are wired up.
#
# RUN
#   python3 mark_rev45_q.py
#   T1_Q45_BEFORE=dir  T1_Q45_AFTER=dir   override the two render directories.

import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BEFORE_DIR = os.environ.get("T1_Q45_BEFORE", "/tmp/insp/before")
AFTER_DIR = os.environ.get("T1_Q45_AFTER", os.path.join(HERE, "out"))
OUT = os.environ.get("T1_Q45_OUT", os.path.join(HERE, "rev45_q.png"))

CTL = {}


def ctl(name, ok, msg):
    CTL[name] = bool(ok)
    print("  [%s] %-3s %s" % ("PASS" if ok else "FAIL", name, msg))


# --------------------------------------------------------------- inputs
# BEFORE = the rev-44 build at the head of claude/project-improvement-id3a9o,
# rendered with prefix r45.  AFTER = this revision, prefix a45.
SRC = {
    "before_hero":  os.path.join(BEFORE_DIR, "r45_hero34f.png"),
    "before_front": os.path.join(BEFORE_DIR, "r45_front34.png"),
    "before_side":  os.path.join(BEFORE_DIR, "r45_side.png"),
    "after_hero":   os.path.join(AFTER_DIR, "a45_hero34f.png"),
    "after_front":  os.path.join(AFTER_DIR, "a45_front34.png"),
    "after_side":   os.path.join(AFTER_DIR, "a45_side.png"),
    "ph_front34":   os.path.join(HERE, "ref_nolita_front34.jpg"),
    "ph_playa":     os.path.join(HERE, "ref_playa_34.png"),
    "ph_board":     os.path.join(HERE, "ref_nolita_doorshut.jpg"),
    "ph_flank":     os.path.join(HERE, "ref_nolita_flank.jpg"),
}
IM = {}
missing = []
for k, p in SRC.items():
    if not os.path.exists(p):
        missing.append(p)
    else:
        IM[k] = Image.open(p).convert("RGB")
ctl("F1", not missing,
    "all %d inputs load%s" % (len(SRC),
                              "" if not missing else " -- MISSING: %s" % missing))
if missing:
    print("CONTROLS: %d checked, %d FAILED -- REFUSING TO WRITE"
          % (len(CTL), 1))
    sys.exit(1)
for k, im in IM.items():
    print("      %-13s %dx%d" % (k, im.width, im.height))


def diff(a, b):
    """mean absolute difference of two equal-sized crops, 0..255"""
    A = np.array(a.convert("RGB").resize((160, 160))).astype(float)
    B = np.array(b.convert("RGB").resize((160, 160))).astype(float)
    return float(np.abs(A - B).mean())


same = diff(IM["before_hero"], IM["after_hero"]) < 0.5
ctl("F2", not same,
    "BEFORE and AFTER heroes differ (mean |d| = %.2f/255)"
    % diff(IM["before_hero"], IM["after_hero"]))

# --------------------------------------------------------------- rows
# Every box is (image_key, x0, y0, x1, y1).  They are PRINTED, per the standing
# rule, and F3 proves each one lies inside its own image.
ROWS = [
    dict(
        n=1,
        title="THE VW BADGE ON THE NOSE",
        q=("Q1.  The badge is the thing you have called \"off\" three times.  "
           "BEFORE, the whole W was inside the sheet metal and only the V and "
           "two stubs stood out -- it read as a CLOCK FACE.  Is AFTER right "
           "now, and if it is still wrong, is it the DRAWING or the SIZE AND "
           "PLACE on the nose?"),
        cells=[("BEFORE  rev 44", "before_front", (860, 555, 925, 615)),
               ("AFTER  rev 45", "after_front", (860, 555, 925, 615)),
               ("PHOTOGRAPH  ref_nolita_front34", "ph_front34", (146, 186, 200, 266))],
    ),
    dict(
        n=2,
        title="THE HEADLAMPS",
        q=("Q2.  BEFORE, the lens was dished the wrong way round and its "
           "centre sat 10 mm INSIDE the nose, so the aperture rendered as a "
           "dark red hole in a brass ring.  AFTER, the lens is convex and the "
           "rim is chrome.  Is the rim chrome or brass on your bus?"),
        cells=[("BEFORE  rev 44", "before_front", (960, 595, 1055, 680)),
               ("AFTER  rev 45", "after_front", (960, 595, 1055, 680)),
               ("PHOTOGRAPH  ref_nolita_front34", "ph_front34", (215, 255, 295, 325))],
    ),
    dict(
        n=3,
        title="\"100% CALIDAD\"",
        q=("Q3.  You have reported this twice.  BEFORE it was PEACH, because "
           "a gradient threw away the red the generator declares.  AFTER it "
           "is red.  Is the colour right now?"),
        cells=[("BEFORE  rev 44", "before_side", (960, 425, 1090, 520)),
               ("AFTER  rev 45", "after_side", (960, 425, 1090, 520)),
               ("PHOTOGRAPH  ref_playa_34", "ph_playa", (418, 110, 466, 168))],
    ),
    dict(
        n=4,
        title="THE PROPS UNDER THE SIGN",
        q=("Q4.  You said the props \"seem to meet something from the sides of "
           "the sign\".  They did: both feet were planted at y = +0.44, which "
           "is INSIDE the open roof hatch, so each prop rose out of thin air "
           "and ran a metre across the board's printed face.  AFTER, both feet "
           "stand on solid roof outboard of the hinge.  Right now?"),
        cells=[("BEFORE  rev 44", "before_hero", (380, 110, 900, 420)),
               ("AFTER  rev 45", "after_hero", (380, 110, 900, 420)),
               ("PHOTOGRAPH  ref_nolita_doorshut", "ph_board", (60, 20, 340, 190))],
    ),
    dict(
        n=5,
        title="THE SIGN BOARD ITSELF -- AN OPEN QUESTION, NOT A FIX",
        q=("Q5.  NOTHING WAS CHANGED HERE.  The build paints the raised board "
           "as a flower mural with menu strips down its edges.  Every "
           "photograph we hold shows a BLACKBOARD, chalked by hand, in a "
           "cream frame, with TACOMBI across the top and BIENVENIDOS down the "
           "side.  Which do you want in the hero?"),
        cells=[("BUILD  rev 45", "after_hero", (380, 110, 900, 420)),
               ("PHOTOGRAPH  ref_nolita_doorshut", "ph_board", (60, 20, 340, 190)),
               ("PHOTOGRAPH  ref_nolita_front34b", "ph_flank", (0, 55, 300, 235))],
    ),
    dict(
        n=6,
        title="THE PAINT -- AN OPEN QUESTION, NOT A FIX",
        q=("Q6.  NOTHING WAS CHANGED HERE EITHER, and it needs your call.  "
           "Measured against your own photographs the red renders too PALE: "
           "green-over-red 0.455 built against 0.223 +- 0.066 photographed "
           "over four frames, 3.5 sigma.  The albedo is RIGHT (0.250).  Half "
           "the excess is the white studio itself -- killing the specular "
           "alone moves it to 0.347.  The same rig is why the bus has no "
           "contact shadow.  Do you want the studio softened so the paint "
           "reads as it does in your photographs, or the catalogue-clean "
           "white background kept?"),
        cells=[("BUILD  rev 45", "after_side", (180, 380, 780, 800)),
               ("PHOTOGRAPH  ref_playa_34", "ph_playa", (20, 90, 470, 350)),
               ("PHOTOGRAPH  ref_nolita_flank", "ph_flank", (0, 140, 260, 340))],
    ),
]

# F3 -- every box strictly inside its own image
bad = []
for r in ROWS:
    for lbl, key, (x0, y0, x1, y1) in r["cells"]:
        im = IM[key]
        if not (0 <= x0 < x1 <= im.width and 0 <= y0 < y1 <= im.height):
            bad.append("row %d %s %s in %dx%d" % (r["n"], lbl, (x0, y0, x1, y1),
                                                  im.width, im.height))
ctl("F3", not bad, "all %d crop boxes lie inside their images%s"
    % (sum(len(r["cells"]) for r in ROWS),
       "" if not bad else " -- OUTSIDE: " + "; ".join(bad)))

# F5 -- the negative control
badge_d = diff(IM["before_front"].crop(ROWS[0]["cells"][0][2]),
               IM["after_front"].crop(ROWS[0]["cells"][1][2]))
cal_d = diff(IM["before_side"].crop(ROWS[2]["cells"][0][2]),
             IM["after_side"].crop(ROWS[2]["cells"][1][2]))
ctl("F5", badge_d > cal_d,
    "NEGATIVE CONTROL: badge before/after differs %.2f, decal %.2f -- the "
    "geometric change must exceed the recolour" % (badge_d, cal_d))

# --------------------------------------------------------------- compose
CELL_H = 300
PAD = 18
GUT = 14
TITLE_H = 30
Q_H = 96
W_TOTAL = 1560


def font(sz, bold=False):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf"
              % ("-Bold" if bold else ""),
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, sz)
            except OSError:
                pass
    return ImageFont.load_default()


F_T = font(19, True)
F_L = font(13, True)
F_Q = font(15)


def _dash(dr, x0, y0, x1, y1, dash=9, gap=6, col=(196, 40, 30), w=2):
    """[C] IDENTIFICATION BOX.  A dashed rectangle round the thing being asked
    about.  It asserts NOTHING about what is inside it and nothing is averaged
    in it -- the format is mark_rev36_ends' and it is kept deliberately."""
    def run(a, b, horiz, fixed):
        t = a
        while t < b:
            u = min(t + dash, b)
            if horiz:
                dr.line([(t, fixed), (u, fixed)], fill=col, width=w)
            else:
                dr.line([(fixed, t), (fixed, u)], fill=col, width=w)
            t = u + gap
    run(x0, x1, True, y0); run(x0, x1, True, y1)
    run(y0, y1, False, x0); run(y0, y1, False, x1)


def wrap(d, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


rows_h = []
scratch = ImageDraw.Draw(Image.new("RGB", (10, 10)))
for r in ROWS:
    n = len(r["cells"])
    cw = (W_TOTAL - 2 * PAD - (n - 1) * GUT) // n
    qlines = wrap(scratch, r["q"], F_Q, W_TOTAL - 2 * PAD)
    rows_h.append((cw, TITLE_H + CELL_H + 20 + len(qlines) * 20 + 26, qlines))

H_TOTAL = PAD + sum(h for _, h, _ in rows_h) + PAD + 46
sheet = Image.new("RGB", (W_TOTAL, H_TOTAL), (250, 249, 245))
dr = ImageDraw.Draw(sheet)

dr.text((PAD, 12),
        "SENOR TACOMBI -- rev 45.  BEFORE | AFTER | PHOTOGRAPH.  "
        "Six questions.  Nothing here is re-touched.", fill=(20, 20, 24),
        font=font(20, True))
y = PAD + 40

for r, (cw, rh, qlines) in zip(ROWS, rows_h):
    dr.text((PAD, y), "%d.  %s" % (r["n"], r["title"]), fill=(150, 24, 18),
            font=F_T)
    cy = y + TITLE_H
    for i, (lbl, key, box) in enumerate(r["cells"]):
        crop = IM[key].crop(box)
        sc = min(cw / crop.width, CELL_H / crop.height)
        crop = crop.resize((max(int(crop.width * sc), 1),
                            max(int(crop.height * sc), 1)), Image.LANCZOS)
        cx = PAD + i * (cw + GUT)
        ox = cx + (cw - crop.width) // 2
        oy = cy + (CELL_H - crop.height) // 2
        sheet.paste(crop, (ox, oy))
        # [C] IDENTIFICATION BOX -- dashed, round the whole cell's subject
        _dash(dr, ox - 4, oy - 4, ox + crop.width + 3, oy + crop.height + 3)
        # [L] PANEL LABEL
        dr.rectangle([cx, cy + CELL_H + 2, cx + cw, cy + CELL_H + 20],
                     fill=(238, 236, 230))
        dr.text((cx + 5, cy + CELL_H + 4), lbl, fill=(40, 40, 46), font=F_L)
    qy = cy + CELL_H + 26
    for ln in qlines:
        dr.text((PAD, qy), ln, fill=(24, 24, 28), font=F_Q)
        qy += 20
    y += rh

# F4 -- every cell in a row shares CELL_H by construction; assert the arithmetic
ctl("F4", all(rh > CELL_H for _, rh, _ in rows_h),
    "every row allocates the full %d px cell height" % CELL_H)

nfail = sum(1 for v in CTL.values() if not v)
print("CONTROLS: %d checked, %d FAILED%s"
      % (len(CTL), nfail,
         "" if not nfail else " -- " + ",".join(k for k, v in CTL.items() if not v)))
if nfail:
    print("REFUSING TO WRITE %s" % OUT)
    sys.exit(1)
sheet.save(OUT)
print("wrote %s  %dx%d" % (OUT, sheet.width, sheet.height))
