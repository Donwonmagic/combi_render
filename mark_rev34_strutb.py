"""
mark_rev34_strutb.py -- rev 34, Q1b.  READ-ONLY.  Writes ONE figure.

WHY THERE IS A Q1b.  [stated, rev 34] Q1: the far strut is at S1 or S2 --
LEFT of the hard-coded 228.  That is the LEFTMOST GROUP of the offered set,
and rev 33's rule says an endpoint answer leaves the interval open on that
side and must be bounded before it is consumed.

BUT THE LEFT SIDE HERE IS NOT OPEN THE WAY REV 33's WAS, AND SAYING SO IS
PART OF THE QUESTION.  The cross-ratio requires far_end < strut < post <
hoop.  With the far end answered at u = 205, every column at or left of 205
is FORBIDDEN BY THE ESTIMATOR'S OWN ORDER -- not by a set boundary I chose.
S1 sits 7 px from that wall.  In rev 33's Q1 the leftmost option had
unbounded reach and 20 px of it moved f by 17.8 %; here there is nowhere for
the answer to run to.

WHAT IS STILL OPEN is the 15 px between the wall and S2, and it is wide:
f runs 0.9296 at u 205.5 down to 0.6594 at u 220.

WHAT THE MARKS ARE.  FOUR CANDIDATE LINES inside the interval he named,
plus the ORDERING WALL drawn as a wall and labelled as one -- the wall is
NOT a candidate and the figure says so.

STILL TRUE, AND STILL PRINTED: no answer to this closes the post
(probe_rev34_levels.py, K5).  Closing needs +-1.5 px; a 4 px split of this
interval returns about +-2 px -> 6.6-7.1 % on the strut alone, on top of the
far end's 7.5 %.

POSITIVE CONTROL GATES THE WRITE, as in Q1: re-derive C5's four published
rows or refuse to write.  Every f is recomputed at draw time.
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "rev34_q_strutb.png")
REF_W = os.path.join(ROOT, "ref_workshop.jpg")

RED = (228, 26, 28)
INK = (18, 18, 18)
BG = (250, 250, 248)
NEW = (0, 130, 180)
GREY = (120, 120, 120)
AMB = (200, 120, 0)
WALL = (120, 20, 140)

POST_U, HOOP_U = 365.5, 485.0
FAR_U = 205.0
STRUT_HARD = 228.0
C5_PUBLISHED = {203.0: 0.5780, 209.0: 0.6160, 215.0: 0.6661, 221.0: 0.7390}

# FOUR candidate lines inside the interval he named, closing BOTH its ends
CAND = [("B1", 208), ("B2", 212), ("B3", 216), ("B4", 220)]

CROP = (198, 630, 274, 708)
ZOOM = 14


def xratio(a, b, c, d):
    return ((a - c) * (b - d)) / ((a - d) * (b - c))


def f_from_X(X):
    b = 2.0 - 4.0 * X
    disc = b * b - 4.0
    return None if disc < 0.0 else (-b - math.sqrt(disc)) / 2.0


def f_at_strut(s):
    return None if FAR_U >= s else f_from_X(xratio(FAR_U, float(s), POST_U,
                                                   HOOP_U))


def f_at_far(u, strut=STRUT_HARD):
    return None if u >= strut else f_from_X(xratio(float(u), float(strut),
                                                   POST_U, HOOP_U))


def font(sz):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


F13, F15, F18, F26 = font(13), font(15), font(18), font(26)


def build():
    print("=" * 74)
    print("mark_rev34_strutb.py -- Q1b, bounding the side he named.")
    print("=" * 74)
    print("\n--- POSITIVE CONTROL (GATES THE WRITE) -------------------------")
    worst = 0.0
    for u in sorted(C5_PUBLISHED):
        got = f_at_far(u)
        dv = abs(got - C5_PUBLISHED[u]) if got is not None else 9e9
        worst = max(worst, dv)
        print("    far end %6.1f -> f %.6f   published %.4f   delta %.2e"
              % (u, got, C5_PUBLISHED[u], dv))
    if worst >= 1e-3:
        print("\n  *** POSITIVE CONTROL FAILED -- REFUSING TO WRITE %s"
              % os.path.basename(OUT))
        return 1
    print("    worst deviation %.2e -- [PASS], the figure may be drawn."
          % worst)

    print("\n--- THE ORDERING WALL, which is NOT a choice I made -------------")
    print("    the cross-ratio needs far_end < strut.  far end = %.0f" % FAR_U)
    for s in (204.0, 205.0, 205.5, 206.0):
        v = f_at_strut(s)
        print("    u %6.1f -> %s"
              % (s, "ORDER BROKEN" if v is None else "f %.4f" % v))

    print("\n--- THE FOUR CANDIDATE LINES, f RECOMPUTED AT DRAW TIME --------")
    f_hard = f_at_strut(STRUT_HARD)
    print("    %4s %8s %10s %14s" % ("line", "u", "f", "vs 228"))
    drawn = []
    for lab, u in CAND:
        f = f_at_strut(u)
        drawn.append((lab, u, f))
        print("    %4s %8d %10.4f %13.1f %%"
              % (lab, u, f, 100.0 * (f - f_hard) / f_hard))
    span = 100.0 * (drawn[0][2] - drawn[-1][2]) / drawn[-1][2]
    print("    the offered interval spans %.1f %% in f." % span)

    im = Image.open(REF_W).convert("RGB")
    u0, v0, u1, v1 = CROP
    z = im.crop(CROP).resize(((u1 - u0) * ZOOM, (v1 - v0) * ZOOM),
                             Image.LANCZOS)

    HEAD = [("rev 34  Q1b -- YOU SAID LEFT OF 228. CLOSING THAT SIDE.",
             F26, INK, 36),
            ("[stated] Q1: the far strut is at S1 or S2, LEFT of the "
             "hard-coded 228. That is the leftmost group, so it gets a "
             "bounded follow-up before I use it.", F15, INK, 22),
            ("AND THIS LEFT SIDE IS NOT OPEN THE WAY REV 33's WAS. The "
             "cross-ratio requires far end < strut. With the far end at "
             "u 205, everything at or left of 205", F15, AMB, 22),
            ("is FORBIDDEN BY THE ESTIMATOR'S OWN ORDER -- not by a set "
             "boundary I chose. The wall is drawn below and it is NOT a "
             "candidate.", F15, AMB, 30),
            ("STILL TRUE: NO ANSWER TO THIS CLOSES THE POST (K5). Closing "
             "needs +-1.5 px; a 4 px split of this interval returns about "
             "+-2 px.", F18, RED, 30),
            ("What is still open is the 15 px between the wall and B4, and "
             "it is wide: f runs 0.930 at u 205.5 down to 0.659 at u 220.",
             F15, INK, 22)]
    FOOT = [("WHAT I AM ASKING: at the bar-axis row, is the strut's column "
             "AT one of these four lines, or LEFT of B1 (between the wall "
             "and 208)?", F18, INK),
            ("\"Between two of them\" and \"can't tell\" are both results "
             "and both bind. Your answer may still be none of these.",
             F15, INK),
            ("crop box printed below. Every f recomputed at draw time; the "
             "figure refused to write unless it first reproduced C5's four "
             "rows (worst %.2e)." % worst, F13, GREY)]

    tmpd = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    wmax = max([tmpd.textbbox((0, 0), t, font=fo)[2] for t, fo, _, _ in HEAD]
               + [tmpd.textbbox((0, 0), t, font=fo)[2] for t, fo, _ in FOOT])
    head_h = 26 + sum(g for _, _, _, g in HEAD)
    x0, y0 = 40, head_h + 34
    W = max(x0 + z.width + 40, x0 + wmax + 40)
    H = y0 + z.height + 190
    cv = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(cv)
    ty = 26
    for t, fo, col, g in HEAD:
        d.text((40, ty), t, col, fo)
        ty += g

    cv.paste(z, (x0, y0))
    d.rectangle([x0 - 1, y0 - 1, x0 + z.width, y0 + z.height], outline=GREY)

    pw = x0 + int(round((FAR_U - CROP[0]) * ZOOM))
    if x0 <= pw <= x0 + z.width:
        d.line([(pw, y0), (pw, y0 + z.height)], fill=WALL, width=5)

    for lab, u, f in drawn:
        px = x0 + int(round((u - CROP[0]) * ZOOM))
        d.line([(px, y0), (px, y0 + z.height)], fill=NEW, width=3)
        d.text((px - 11, y0 - 26), lab, NEW, F18)
        d.text((px - 24, y0 + z.height + 6), "u %d" % u, NEW, F15)
        d.text((px - 28, y0 + z.height + 26), "f %.3f" % f, INK, F13)

    # The wall LABEL is drawn LAST, after the candidate lines, so nothing can
    # be drawn across it.  Two earlier drafts of this figure had the label
    # crossed -- first by the B1..B4 tags at the head, then by the lines
    # themselves.  Both caught by cropping the PNG and looking at it.
    if x0 <= pw <= x0 + z.width:
        wl = "ORDERING WALL  u 205  -- NOT a candidate, and not my choice"
        ly = y0 + z.height - 34
        lb = d.textbbox((pw + 10, ly), wl, font=F15)
        d.rectangle([lb[0] - 5, lb[1] - 4, lb[2] + 5, lb[3] + 4], fill=BG,
                    outline=WALL)
        d.text((pw + 10, ly), wl, WALL, F15)

    d.text((x0, y0 + z.height + 52),
           "ref_workshop.jpg   CROP BOX (u,v) = (%d, %d) - (%d, %d)   at x%d"
           "   [CANDIDATE LINES + one ORDERING WALL]" % (CROP + (ZOOM,)),
           INK, F15)
    d.text((x0, y0 + z.height + 74),
           "the hard-coded 228 is OFF THIS CROP to the right -- your Q1 "
           "answer already excluded it, and it is not offered again.",
           GREY, F13)

    fy = H - 96
    for t, fo, col in FOOT:
        d.text((40, fy), t, col, fo)
        fy += 26

    cv.save(OUT)
    print("\n    wrote %s  (%d x %d)" % (os.path.basename(OUT), W, H))
    print("    crop (u,v) = (%d,%d)-(%d,%d)  x%d  [CANDIDATE LINES + WALL]"
          % (CROP + (ZOOM,)))
    return 0


if __name__ == "__main__":
    sys.exit(build())
