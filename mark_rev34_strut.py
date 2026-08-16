"""
mark_rev34_strut.py -- rev 34.  READ-ONLY.  Writes ONE figure.

THE QUESTION: where does the over-rider bar's FAR STRUT sit?

It is the last ungraded column in the cross-ratio.  C3 measured the post
(365.5) and the hoop (485.0).  P1b graded the far end.  The FAR STRUT at
u = 228 has never been measured, never been graded and never been asked
about -- it is hard-coded in probe_orb_xratio.py's C5 and that probe's own
print calls it '(blob)'.

WHAT THE MARKS ARE.  FIVE CANDIDATE LINES, the third mark class -- neither
POINTERS (rev 31) nor SAMPLING WINDOWS (rev 30).  A candidate line is an
OFFER: "is the feature at this column?"  It asserts nothing.  They are
placed SYMMETRICALLY about the hard-coded 228 so that an endpoint answer is
informative, per rev 33's rule that an endpoint answer is an open interval.

STATED BEFORE THE QUESTION IS ASKED -- probe_rev34_levels.py, K5:
    NO ANSWER TO THIS QUESTION CLOSES THE POST.
    Closing needs the strut pinned to about +-1.5 px.  The best a
    candidate-line set at this spacing can return is +-4 px.  The gap is
    not close and it is not arguable.
WHAT THE ANSWER DOES BUY is stated on the figure: it converts the last
hard-coded column in the estimator into a measured value with an interval.

POSITIVE CONTROL, AND IT GATES THE WRITE.  Before drawing, re-derive C5's
four published rows from this file's own arithmetic.  If any row deviates
by more than 1e-3 the figure REFUSES TO WRITE.  rev 33's rule: a number
written into a question is a number nobody re-reads -- so every `f` on this
figure is recomputed at draw time from the columns, and none is typed.

CEILING, STATED ON THE FIGURE.  The strut is not a line.  It is a WEDGE
whose width changes with height, so "its column" is undefined until a ROW
is named.  The row that matters is where it meets the BAR'S OWN AXIS,
because the cross-ratio requires the four points COLLINEAR in the bumper
plane.  The figure says this and marks that junction.
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "rev34_q_strut.png")
REF_W = os.path.join(ROOT, "ref_workshop.jpg")
RENDER = os.path.join(ROOT, "out", "rev34strut_raw.png")

RED = (228, 26, 28)
INK = (18, 18, 18)
BG = (250, 250, 248)
NEW = (0, 130, 180)
GREY = (120, 120, 120)
AMB = (200, 120, 0)

# ---- the LIVE columns.  NOT typed as results anywhere below. -------------
POST_U, HOOP_U = 365.5, 485.0
FAR_U = 205.0            # [stated, rev 33] Q1 + Q1b
STRUT_HARD = 228.0       # what C5 has been assuming, on no support

# C5's four published rows -- the positive control that GATES THE WRITE
C5_PUBLISHED = {203.0: 0.5780, 209.0: 0.6160, 215.0: 0.6661, 221.0: 0.7390}

# FIVE CANDIDATE LINES, symmetric about the hard-coded 228
CAND = [("S1", 212), ("S2", 220), ("S3", 228), ("S4", 236), ("S5", 244)]

CROP = (175, 620, 290, 730)      # the strut, at x9
ZOOM = 9
WIDE = (160, 600, 520, 760)      # the same bumper, wider, at x3
ZOOM_W = 3
RCROP = (150, 400, 370, 520)     # the BUILD, same assembly, at x4
RZOOM = 4


def xratio(a, b, c, d):
    return ((a - c) * (b - d)) / ((a - d) * (b - c))


def f_from_X(X):
    b = 2.0 - 4.0 * X
    disc = b * b - 4.0
    return None if disc < 0.0 else (-b - math.sqrt(disc)) / 2.0


def f_at_strut(s, far=FAR_U):
    """f recomputed AT DRAW TIME from the columns.  Never a typed literal."""
    if far >= s:
        return None
    return f_from_X(xratio(float(far), float(s), POST_U, HOOP_U))


def f_at_far(u, strut=STRUT_HARD):
    if u >= strut:
        return None
    return f_from_X(xratio(float(u), float(strut), POST_U, HOOP_U))


def font(sz):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


F13, F15, F18, F21, F26 = font(13), font(15), font(18), font(21), font(26)


def crop_zoom(im, box, z):
    u0, v0, u1, v1 = box
    return im.crop((u0, v0, u1, v1)).resize(((u1 - u0) * z, (v1 - v0) * z),
                                            Image.LANCZOS)


def positive_control():
    """Re-derive C5's four published rows.  Returns (ok, worst, rows)."""
    worst, rows = 0.0, []
    for u in sorted(C5_PUBLISHED):
        got = f_at_far(u)
        d = abs(got - C5_PUBLISHED[u]) if got is not None else 9e9
        worst = max(worst, d)
        rows.append((u, got, C5_PUBLISHED[u], d))
    return worst < 1e-3, worst, rows


def build():
    print("=" * 74)
    print("mark_rev34_strut.py -- the FAR STRUT question.  READ-ONLY.")
    print("=" * 74)

    # ---- the gate ------------------------------------------------------
    print("\n--- POSITIVE CONTROL (GATES THE WRITE) -------------------------")
    print("    re-derive C5's four published rows from this file's own")
    print("    arithmetic.  If this fails, NO FIGURE IS WRITTEN.")
    ok, worst, rows = positive_control()
    for u, got, pub, d in rows:
        print("    far end %6.1f -> f %.6f   published %.4f   delta %.2e"
              % (u, got, pub, d))
    print("    worst deviation %.2e over %d rows" % (worst, len(rows)))
    if not ok:
        print("\n  *** POSITIVE CONTROL FAILED -- REFUSING TO WRITE %s"
              % os.path.basename(OUT))
        print("  *** A figure whose own arithmetic no longer reproduces the")
        print("  *** published rows is not evidence.  Nothing was written.")
        return 1
    print("    [PASS] control holds -- the figure may be drawn.")

    # ---- the candidate columns, f recomputed at draw time ---------------
    print("\n--- THE FIVE CANDIDATE LINES, f RECOMPUTED AT DRAW TIME --------")
    f_hard = f_at_strut(STRUT_HARD)
    print("    far end held at u = %.0f  [stated, rev 33]" % FAR_U)
    print("    %4s %8s %10s %14s" % ("line", "u", "f", "vs u = 228"))
    drawn = []
    for lab, u in CAND:
        f = f_at_strut(u)
        drawn.append((lab, u, f))
        print("    %4s %8d %10.4f %13.1f %%"
              % (lab, u, f, 100.0 * (f - f_hard) / f_hard))
    span = 100.0 * (max(d[2] for d in drawn) - min(d[2] for d in drawn)) \
        / min(d[2] for d in drawn)
    print("    the offered set spans %.1f %% in f." % span)

    # ---- draw ------------------------------------------------------------
    im = Image.open(REF_W).convert("RGB")
    z = crop_zoom(im, CROP, ZOOM)
    wide = crop_zoom(im, WIDE, ZOOM_W)
    rnd = Image.open(RENDER).convert("RGB")
    rz = crop_zoom(rnd, RCROP, RZOOM)

    # ---- lay the header out by MEASURING it, never by assuming it fits.
    #      rev 33 shipped two figures with clipped text and colliding tags,
    #      caught only by cropping and viewing them.  This sizes the canvas
    #      from the drawn extents instead.
    HEAD = [("rev 34  Q1 -- WHERE DOES THE OVER-RIDER BAR'S FAR STRUT SIT?",
             F26, INK, 36),
            ("The FIVE marks below are CANDIDATE LINES -- an OFFER, not a "
             "claim. Neither POINTERS (rev 31) nor SAMPLING WINDOWS "
             "(rev 30).", F15, INK, 22),
            ("Placed SYMMETRICALLY about the hard-coded u = 228 so an "
             "endpoint answer is informative. YOUR ANSWER MAY BE NONE OF "
             "THEM.", F15, INK, 30),
            ("SAID BEFORE ASKING (probe_rev34_levels.py, K5):  NO ANSWER TO "
             "THIS CLOSES THE POST.", F18, RED, 24),
            ("Closing needs the strut pinned to about +-1.5 px; this set "
             "returns +-4 px at best.", F15, INK, 22),
            ("WHAT THE ANSWER DOES BUY: it turns the last hard-coded column "
             "in the estimator -- C5's own print calls it '(blob)' -- into a "
             "measured value with an interval.", F15, INK, 22),
            ("The post stays UNBUILT either way.", F15, INK, 30),
            ("CEILING: the strut is NOT a line. It is a WEDGE whose width "
             "changes with height, so its column is undefined until a ROW is "
             "named.", F15, AMB, 22),
            ("The row that matters is where it meets THE BAR'S OWN AXIS -- "
             "the cross-ratio needs the four points collinear in the bumper "
             "plane.", F15, AMB, 22)]
    FOOT = [("WHAT I AM ASKING: at the row where the bar's axis crosses it, "
             "which candidate line lands on the strut? Above and below that "
             "row it is wider.", F18, INK),
            ("\"CAN'T TELL\" IS A RESULT AND IT BINDS (rev 30). So is \"none "
             "of these\" (rev 31, twice). Either answer is more use to me "
             "than a guess.", F15, INK),
            ("The offered set spans %.1f %% in f. Nothing here is a build "
             "value and the post is not being built off your answer." % span,
             F13, GREY)]
    CAPS = [("THE CURRENT BUILD, same assembly, same 3/4 front view   crop "
             "(x,y) = (%d, %d) - (%d, %d) at x%d of a 900x600 T1_SAMP=24 "
             "preview" % (RCROP + (RZOOM,)), F15),
            ("the figure REFUSED TO WRITE unless it first reproduced C5's "
             "four published rows; worst deviation this run %.2e." % worst,
             F13),
            ("every f above is RECOMPUTED AT DRAW TIME from the columns "
             "(far end %.0f, post %.1f, hoop %.1f) -- none is typed."
             % (FAR_U, POST_U, HOOP_U), F13)]
    # Measure EVERY string that will be drawn, not just the header -- rev 33
    # clipped a figure by sizing the canvas off one block and drawing three.
    tmpd = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    head_w = max([tmpd.textbbox((0, 0), t, font=fo)[2]
                  for t, fo, _, _ in HEAD]
                 + [tmpd.textbbox((0, 0), t, font=fo)[2]
                    for t, fo, _ in FOOT]
                 + [tmpd.textbbox((0, 0), t, font=fo)[2] for t, fo in CAPS])
    head_h = 26 + sum(gap for _, _, _, gap in HEAD)

    x0 = 40
    y0 = head_h + 34            # 34 px of clearance for the S1..S5 tags
    W = max(x0 + z.width + 40, x0 + wide.width + 40,
            x0 + rz.width + 40, x0 + head_w + 40)
    y1 = y0 + z.height + 132
    y2 = y1 + wide.height + 118
    H = y2 + rz.height + 196
    cv = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(cv)

    ty = 26
    for t, fo, col, gap in HEAD:
        d.text((40, ty), t, col, fo)
        ty += gap

    cv.paste(z, (x0, y0))
    d.rectangle([x0 - 1, y0 - 1, x0 + z.width, y0 + z.height], outline=GREY)

    for lab, u, f in drawn:
        px = x0 + int(round((u - CROP[0]) * ZOOM))
        if not (x0 <= px <= x0 + z.width):
            continue
        d.line([(px, y0), (px, y0 + z.height)], fill=NEW, width=3)
        d.text((px - 11, y0 - 24), lab, NEW, F18)
        d.text((px - 26, y0 + z.height + 6), "u %d" % u, NEW, F15)
        d.text((px - 30, y0 + z.height + 26), "f %.3f" % f, INK, F13)
    ph = x0 + int(round((STRUT_HARD - CROP[0]) * ZOOM))
    d.line([(ph, y0), (ph, y0 + 40)], fill=RED, width=3)
    lab = "hard-coded 228 (no support)"
    lb = d.textbbox((ph + 9, y0 + 6), lab, font=F15)
    d.rectangle([lb[0] - 4, lb[1] - 3, lb[2] + 4, lb[3] + 3], fill=BG,
                outline=RED)
    d.text((ph + 9, y0 + 6), lab, RED, F15)

    d.text((x0, y0 + z.height + 52),
           "ref_workshop.jpg   CROP BOX (u,v) = (%d, %d) - (%d, %d)   at x%d"
           "   [CANDIDATE LINES]" % (CROP + (ZOOM,)), INK, F15)
    d.text((x0, y0 + z.height + 74),
           "every f above is RECOMPUTED AT DRAW TIME from the columns "
           "(far end %.0f, post %.1f, hoop %.1f) -- none is typed."
           % (FAR_U, POST_U, HOOP_U), GREY, F13)
    d.text((x0, y0 + z.height + 94),
           "the figure REFUSED TO WRITE unless it first reproduced C5's four "
           "published rows; worst deviation this run %.2e." % worst,
           GREY, F13)

    cv.paste(wide, (x0, y1))
    d.rectangle([x0 - 1, y1 - 1, x0 + wide.width, y1 + wide.height],
                outline=GREY)
    for lab, u, f in drawn:
        px = x0 + int(round((u - WIDE[0]) * ZOOM_W))
        d.line([(px, y1), (px, y1 + 22)], fill=NEW, width=2)
        d.text((px - 9, y1 + 24), lab, NEW, F13)
    pp = x0 + int(round((POST_U - WIDE[0]) * ZOOM_W))
    d.line([(pp, y1), (pp, y1 + wide.height)], fill=(20, 150, 60), width=2)
    d.text((pp + 6, y1 + wide.height - 30), "the POST, u 365.5 (C3, measured)",
           (20, 150, 60), F13)
    d.text((x0, y1 + wide.height + 8),
           "the same bumper, wider:  CROP BOX (u,v) = (%d, %d) - (%d, %d)  at "
           "x%d   [CANDIDATE LINES]" % (WIDE + (ZOOM_W,)), INK, F15)
    d.text((x0, y1 + wide.height + 30),
           "for scale: the POST is the vertical the bar's near end lands on, "
           "and it IS measured. The strut is its far-side counterpart and is "
           "NOT.", GREY, F13)

    cv.paste(rz, (x0, y2))
    d.rectangle([x0 - 1, y2 - 1, x0 + rz.width, y2 + rz.height], outline=GREY)
    d.text((x0, y2 + rz.height + 8),
           "THE CURRENT BUILD, same assembly, same 3/4 front view   "
           "crop (x,y) = (%d, %d) - (%d, %d) at x%d of a 900x600 "
           "T1_SAMP=24 preview" % (RCROP + (RZOOM,)), INK, F15)
    d.text((x0, y2 + rz.height + 30),
           "The over-rider BAR is built (SPEC 10.83, workshop-stage). "
           "NEITHER the post NOR the far strut is built -- that is what the "
           "render is here to show.", GREY, F13)
    d.text((x0, y2 + rz.height + 52),
           "173 commits, guards 0 fail / 0 warn at both subdivision levels. "
           "No geometry has moved since rev 30.", GREY, F13)

    fy = H - 96
    for t, fo, col in FOOT:
        d.text((40, fy), t, col, fo)
        fy += 26

    cv.save(OUT)
    print("\n    wrote %s  (%d x %d)" % (os.path.basename(OUT), W, H))
    print("    crop A (u,v) = (%d,%d)-(%d,%d)  x%d   [CANDIDATE LINES]"
          % (CROP + (ZOOM,)))
    print("    crop B (u,v) = (%d,%d)-(%d,%d)  x%d   [CANDIDATE LINES]"
          % (WIDE + (ZOOM_W,)))
    print("    render (x,y) = (%d,%d)-(%d,%d)  x%d" % (RCROP + (RZOOM,)))
    return 0


if __name__ == "__main__":
    sys.exit(build())
