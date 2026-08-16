"""
mark_rev33_q1.py -- rev 33.  READ-ONLY.  Rebuilds rev 32's Q1 figure with its
arithmetic CORRECTED and its unusable options LABELLED.

WHY THIS FILE EXISTS.  rev 32's `rev32_q1_barend.png` carries two defects in
the block that tells the owner why the column matters.  Neither changes the
verdict (the cross-ratio route is dead either way, C5) but the figure is the
artifact he is being asked to act on, so it is a PROBE and it was checked.

  DEFECT 1 -- A PLANTED VALUE QUOTED AS A MEASUREMENT.
  The figure says "with the far end at u = 209 the post lands at 0.626".
  0.626 is `f_true` in probe_orb_xratio.py's P1b -- a value PLANTED on a
  SYNTHETIC projective map u(t) = (vp*t + p)/(t + q) to grade the estimator's
  conditioning.  It is not a reading of this vehicle.  The LIVE value at
  u = 209, from C5's own columns, is 0.6160.

  DEFECT 2 -- A SECOND NUMBER THAT DOES NOT REPRODUCE.
  The figure says "at u = 224 it lands at 0.820", a 31 % swing.  Running C5's
  own machinery at u = 224 gives 0.7943.  0.820 is produced by neither the
  synthetic map nor the live columns.  C5's published swing is 28 %, over
  203 -> 221, and that is the figure of record.

  DEFECT 3 -- TWO OF THE FIVE OPTIONS CANNOT BE CONSUMED.
  C5 fixes `strut_u = 228.0` and declares ORDER BROKEN for any far end at or
  beyond it: the far end would be inboard of the strut.  Candidate line 4 sits
  at u = 228 and line 5 at u = 240.  BOTH ARE UNANSWERABLE BY THE ROUTE THE
  QUESTION EXISTS TO FEED.  They are NOT removed -- they are legitimate
  readings of the photograph and rev 32 already ruled that "none of them"
  binds.  They are LABELLED, so that choosing one is a decision to close the
  route rather than an answer that quietly evaporates.

SELF-CHECK.  This script does not hard-code a single f.  It recomputes every
one from C5's own constants at draw time, and it re-derives three of C5's
printed rows (203, 209, 215, 221) as a positive control before drawing.  If
the control fails it REFUSES TO WRITE THE FIGURE.  rev 32's lesson: a number
written into a question is a number nobody re-reads.

CEILING, STATED.  This corrects the figure's ARITHMETIC and its OPTION
LABELLING.  It does not improve the underlying measurement by one pixel, it
does not revive the route, and it does not make the question closeable -- see
the pre-commitment printed at the end, which is on the record BEFORE any
answer arrives.
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT1 = os.path.join(ROOT, "rev33_q1_barend.png")
REF_W = os.path.join(ROOT, "ref_workshop.jpg")

RED = (228, 26, 28)
BLU = (55, 126, 184)
GRN = (30, 145, 70)
ORA = (255, 127, 0)
PUR = (140, 86, 190)
INK = (18, 18, 18)
BG = (250, 250, 248)
GREY = (110, 110, 110)

# ---- geometry, IDENTICAL to rev 32's so the two figures are comparable ----
Q1_CROP = (188, 606, 300, 706)
Q1_ZOOM = 9
Q1_CAND = [("1", 205, RED), ("2", 212, ORA), ("3", 219, GRN),
           ("4", 228, BLU), ("5", 240, PUR)]
Q1_WIDE = (190, 640, 510, 740)
Q1_ZOOM_W = 4
POST_U0, POST_U1 = 355.0, 377.0
BAR_NEAR_U = 487.0

# ---- C5's own constants, copied from probe_orb_xratio.py -----------------
POST_U = 0.5 * (POST_U0 + POST_U1)      # 366.0 from the figure's own pair
POST_U_C5 = 365.5                       # C3's measured centre, what C5 uses
HOOP_U = 485.0                          # C3's measured hoop outer
STRUT_U = 228.0                         # C5's far strut

# C5's printed rows, for the positive control
C5_PUBLISHED = {203.0: 0.5780, 209.0: 0.6160, 215.0: 0.6661, 221.0: 0.7390}

# the published go / no-go, from P1b.  NOT recomputed here, quoted as levels.
GONOGO = "dU <= 4 px closes (6.2 % on f); dU >= 8 px does not (14.3 %)"


def xratio(a, b, c, d):
    return ((a - c) * (b - d)) / ((a - d) * (b - c))


def f_from_X(X):
    """X = (1+f)^2 / 4f  ->  f^2 + (2 - 4X) f + 1 = 0, small (physical) root."""
    b = 2.0 - 4.0 * X
    disc = b * b - 4.0
    if disc < 0.0:
        return None
    return (-b - math.sqrt(disc)) / 2.0


def f_at(u):
    """f for a far-end column u, through C5's machinery.  None if unusable."""
    if u >= STRUT_U:
        return None
    return f_from_X(xratio(float(u), STRUT_U, POST_U_C5, HOOP_U))


def font(sz):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


F13, F14, F17, F22, F28 = font(13), font(14), font(17), font(22), font(28)


def crop_zoom(im, box, z):
    u0, v0, u1, v1 = box
    return im.crop((u0, v0, u1, v1)).resize(((u1 - u0) * z, (v1 - v0) * z),
                                            Image.LANCZOS)


def positive_control():
    """Re-derive C5's OWN printed rows.  Refuse to draw if they do not match."""
    print("--- POSITIVE CONTROL: re-derive C5's printed rows -------------")
    worst = 0.0
    for u, want in sorted(C5_PUBLISHED.items()):
        got = f_at(u)
        d = abs(got - want)
        worst = max(worst, d)
        print("    u %6.1f   published %.4f   recomputed %.4f   d %.5f  %s"
              % (u, want, got, d, "ok" if d < 5e-4 else "MISMATCH"))
    ok = worst < 5e-4
    print("    worst deviation %.2e over %d rows -- %s"
          % (worst, len(C5_PUBLISHED), "PASS" if ok else "FAIL"))
    if not ok:
        print("\n    REFUSING TO WRITE THE FIGURE.  This script's estimator no")
        print("    longer reproduces the probe it claims to correct, so any")
        print("    number it drew would be unsourced.")
        sys.exit(1)
    return worst


def build():
    worst = positive_control()

    print("\n--- f AT EVERY CANDIDATE LINE, recomputed at draw time ---------")
    rows = []
    for lab, u, col in Q1_CAND:
        f = f_at(u)
        rows.append((lab, u, col, f))
        if f is None:
            print("    line %s  u %3d   ORDER BROKEN -- at/beyond the strut at "
                  "u %.0f; the route has NO ANSWER here" % (lab, u, STRUT_U))
        else:
            print("    line %s  u %3d   f = %.4f" % (lab, u, f))

    usable = [r for r in rows if r[3] is not None]
    fs = [r[3] for r in usable]
    swing = 100.0 * (max(fs) - min(fs)) / min(fs)
    print("    usable lines: %d of %d.  f spans %.4f - %.4f = %.1f %% swing"
          % (len(usable), len(rows), min(fs), max(fs), swing))
    print("    the three usable lines are 7 px apart; the published go/no-go "
          "is\n      %s" % GONOGO)

    im = Image.open(REF_W).convert("RGB")
    z = crop_zoom(im, Q1_CROP, Q1_ZOOM)
    zw, zh = z.size
    wide = crop_zoom(im, Q1_WIDE, Q1_ZOOM_W)
    ww, wh = wide.size

    W = max(zw, ww) + 80
    H = 175 + zh + 60 + wh + 470
    cv = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(cv)

    d.text((40, 24), "rev 33  Q1 -- WHERE DOES THE OVER-RIDER BAR END, ON THE "
                     "FAR SIDE?", INK, font=F28)
    d.text((40, 62), "Same question as rev 32, same crops, same five lines.  "
                     "THE ARITHMETIC UNDER IT WAS WRONG AND IS CORRECTED.",
           RED, font=F17)
    d.text((40, 86), "THE FIVE LINES ARE CANDIDATES -- not sampling windows, "
                     "not pointers.  No number is taken from any of them.",
           INK, font=F17)
    d.text((40, 110), "If none of them is right, say so -- that binds, and it "
                      "is a better answer than the set.", INK, font=F17)
    d.text((40, 134), "LINES 4 AND 5 ARE MARKED GREY: they are legitimate "
                      "readings, but the route cannot consume them.  See below.",
           GREY, font=F17)

    x0, y0 = 40, 172
    cv.paste(z, (x0, y0))
    d.rectangle([x0 - 1, y0 - 1, x0 + zw, y0 + zh], outline=INK)
    for lab, u, col, f in rows:
        px = x0 + int(round((u - Q1_CROP[0]) * Q1_ZOOM))
        dead = f is None
        draw_col = GREY if dead else col
        d.line([px, y0, px, y0 + zh], fill=draw_col, width=3)
        d.rectangle([px - 13, y0 + zh - 30, px + 13, y0 + zh - 2],
                    fill=draw_col)
        d.text((px - 6, y0 + zh - 27), lab, (255, 255, 255), font=F22)
        tag = "NO ANSWER" if dead else "f %.3f" % f
        tw = d.textlength(tag, font=F14)
        d.rectangle([px - tw / 2 - 5, y0 + 4, px + tw / 2 + 5, y0 + 26],
                    fill=(255, 255, 255), outline=draw_col)
        d.text((px - tw / 2, y0 + 6), tag, draw_col, font=F14)
    d.text((x0, y0 + zh + 8),
           "ref_workshop.jpg  crop box (u,v) = (%d, %d) - (%d, %d)  at x%d"
           % (Q1_CROP + (Q1_ZOOM,)), INK, font=F14)

    y1 = y0 + zh + 44
    cv.paste(wide, (x0, y1))
    d.rectangle([x0 - 1, y1 - 1, x0 + ww, y1 + wh], outline=INK)
    for lab, u, col, f in rows:
        px = x0 + int(round((u - Q1_WIDE[0]) * Q1_ZOOM_W))
        d.line([px, y1, px, y1 + wh], fill=(GREY if f is None else col),
               width=2)
    pa = x0 + int(round((POST_U0 - Q1_WIDE[0]) * Q1_ZOOM_W))
    pb = x0 + int(round((POST_U1 - Q1_WIDE[0]) * Q1_ZOOM_W))
    d.rectangle([pa, y1 + 6, pb, y1 + wh - 6], outline=(0, 0, 0), width=3)
    d.text((pa - 4, y1 + wh - 26), "POST  u 355-377  MEASURED", (0, 0, 0),
           font=F14)
    pn = x0 + int(round((BAR_NEAR_U - Q1_WIDE[0]) * Q1_ZOOM_W))
    d.line([pn, y1, pn, y1 + wh], fill=(0, 0, 0), width=3)
    d.text((pn - 155, y1 + 6), "BAR NEAR END  u 487  MEASURED", (0, 0, 0),
           font=F14)
    d.text((x0, y1 + wh + 8),
           "the same bumper, wider:  crop box (u,v) = (%d, %d) - (%d, %d)  at "
           "x%d" % (Q1_WIDE + (Q1_ZOOM_W,)), INK, font=F14)

    ty = y1 + wh + 36
    lines = [
        ("WHAT REV 32's FIGURE SAID, AND WHY IT WAS WRONG:", RED),
        ("  it said \"at u = 209 the post lands at 0.626\".  0.626 is a value "
         "PLANTED on a SYNTHETIC map to grade the", INK),
        ("  estimator -- not a reading of this vehicle.  The live value at "
         "u = 209 is 0.616.  It also said u = 224 gives", INK),
        ("  0.820; C5's own machinery gives 0.794.  The swing of record is "
         "28 %, over u 203-221, not 31 %.", INK),
        ("", INK),
        ("WHAT EACH ANSWER ACTUALLY YIELDS (recomputed above the lines, not "
         "typed):", INK),
        ("  line 1  u 205 -> f %.3f      line 2  u 212 -> f %.3f      "
         "line 3  u 219 -> f %.3f"
         % (rows[0][3], rows[1][3], rows[2][3]), INK),
        ("  line 4  u 228  and  line 5  u 240 -> NO ANSWER.  C5 fixes the far "
         "strut at u 228 and both sit at or beyond it,", GREY),
        ("  so the far end would be inboard of the strut and the cross-ratio "
         "has no physical root.  Choosing 4 or 5 is a", GREY),
        ("  decision to CLOSE the route -- which is a real answer, and it "
         "binds.  It is not a number.", GREY),
        ("", INK),
        ("WHAT I EXPECT, ON THE RECORD BEFORE YOU ANSWER:", RED),
        ("  the three usable lines are 7 px apart and span %.1f %% in f.  The "
         "published levels are" % swing, INK),
        ("  %s." % GONOGO, INK),
        ("  So naming ONE line still leaves ~7 px of residual and the route "
         "does NOT close.  I am not asking this expecting", INK),
        ("  to build the post from it.  I am asking because if the end is at "
         "line 4 or 5 the route is closed for good, and", INK),
        ("  because your reading is the only thing that can tighten it below "
         "the line spacing.  A square-on frame of the", INK),
        ("  FRONT of the vehicle would collapse the whole problem and is worth "
         "more than any answer to this question.", INK),
    ]
    for ln, col in lines:
        d.text((40, ty), ln, col, font=F17)
        ty += 23

    cv.save(OUT1)
    print("\nQ1 written: %s   %dx%d" % (OUT1, W, H))
    print("   crop A (u,v) = (%d,%d)-(%d,%d)  x%d   [CANDIDATE LINES]"
          % (Q1_CROP + (Q1_ZOOM,)))
    print("   crop B (u,v) = (%d,%d)-(%d,%d)  x%d   [CANDIDATE LINES]"
          % (Q1_WIDE + (Q1_ZOOM_W,)))
    print("   positive control worst deviation %.2e" % worst)


if __name__ == "__main__":
    build()
