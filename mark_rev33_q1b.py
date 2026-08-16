"""
mark_rev33_q1b.py -- rev 33.  READ-ONLY.  THE BOUNDED FOLLOW-UP.

WHY THERE IS A SECOND Q1.  The owner answered Q1 with CANDIDATE LINE 1,
u = 205 -- the LEFTMOST member of the offered set.  probe_rev33_barend.py's
A4 and A5 both FAIL on that: an endpoint answer leaves the interval OPEN on
that side, and 20 px of reach to the left moves f by 17.8 %.  The set's left
boundary at 205 was chosen by rev 32, not by the photograph.

So this figure does the one thing that converts an open interval into a
closed one: it puts marks on the side the first set never reached, and asks
a BOUNDED question.  If he says the end is AT line 1 and not left of it, the
left side closes and the route's residual is the line spacing alone.

THE MARKS ARE CANDIDATE LINES, the same third class rev 32 introduced --
neither sampling windows nor pointers.  No number is taken from any of them.
Line 1 (u 205) is redrawn in its ORIGINAL COLOUR AND LABEL so the two figures
can be laid side by side without re-indexing anything.

CEILING, STATED.  This cannot resolve the superposition rev 31 identified and
does not try to.  It can only establish whether the answered column is a
BOUND or an INTERIOR reading.  Even a perfect answer here leaves criterion
(1) -- the line-spacing residual, which straddles the published closing level
depending on how the answer is read.  A square-on frame of the FRONT is still
worth more than any answer to this figure.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "rev33_q1b_leftbound.png")
REF_W = os.path.join(ROOT, "ref_workshop.jpg")

RED = (228, 26, 28)
INK = (18, 18, 18)
BG = (250, 250, 248)
NEW = (0, 130, 180)

CROP = (170, 606, 300, 706)     # WIDENED LEFT from rev 32's 188 -- stated
ZOOM = 9
WIDE = (172, 640, 510, 740)
ZOOM_W = 4

# the NEW candidates, all LEFT of the answered column
LEFT_CAND = [("L1", 185), ("L2", 190), ("L3", 195), ("L4", 200)]
ANSWERED = 205

POST_U, HOOP_U, STRUT_U = 365.5, 485.0, 228.0
POST_U0, POST_U1, BAR_NEAR_U = 355.0, 377.0, 487.0


def xratio(a, b, c, d):
    return ((a - c) * (b - d)) / ((a - d) * (b - c))


def f_at(u):
    X = xratio(float(u), STRUT_U, POST_U, HOOP_U)
    b = 2.0 - 4.0 * X
    disc = b * b - 4.0
    return None if disc < 0 else (-b - math.sqrt(disc)) / 2.0


def font(sz):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


F14, F17, F22, F28 = font(14), font(17), font(22), font(28)


def crop_zoom(im, box, z):
    u0, v0, u1, v1 = box
    return im.crop((u0, v0, u1, v1)).resize(((u1 - u0) * z, (v1 - v0) * z),
                                            Image.LANCZOS)


def build():
    f_ans = f_at(ANSWERED)
    print("--- the answered column, for reference ---")
    print("    u %d -> f %.4f" % (ANSWERED, f_ans))
    print("--- the NEW candidates, all LEFT of it ---")
    rows = []
    for lab, u in LEFT_CAND:
        f = f_at(u)
        rows.append((lab, u, f))
        print("    %s  u %3d -> f %.4f   (%+.1f %% vs the answered column)"
              % (lab, u, f, 100.0 * (f - f_ans) / f_ans))

    im = Image.open(REF_W).convert("RGB")
    z = crop_zoom(im, CROP, ZOOM)
    zw, zh = z.size
    wide = crop_zoom(im, WIDE, ZOOM_W)
    ww, wh = wide.size

    W = max(zw, ww) + 80
    H = 185 + zh + 60 + wh + 300
    cv = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(cv)

    d.text((40, 24), "rev 33  Q1b -- IS THE BAR'S FAR END *AT* LINE 1, OR "
                     "LEFT OF IT?", INK, font=F28)
    d.text((40, 62), "You answered line 1, u = 205 -- the LEFTMOST option I "
                     "offered.  That is the one answer my set could not "
                     "bracket:", RED, font=F17)
    d.text((40, 86), "nothing in it excludes an end further left, and 20 px "
                     "of reach there moves the answer by 17.8 %.", RED,
           font=F17)
    d.text((40, 112), "SO THIS FIGURE ONLY ADDS MARKS ON THE SIDE THE FIRST "
                      "SET NEVER REACHED.  The crop is widened left to u = "
                      "170.", INK, font=F17)
    d.text((40, 136), "BLUE L1-L4 ARE CANDIDATE LINES -- not sampling "
                      "windows, not pointers.  RED 1 is your answer, "
                      "unchanged.", INK, font=F17)

    x0, y0 = 40, 172
    cv.paste(z, (x0, y0))
    d.rectangle([x0 - 1, y0 - 1, x0 + zw, y0 + zh], outline=INK)

    def tag(px, text, col, tier=0):
        """Tiered vertically: at 5 px spacing and x9 the boxes would collide."""
        ty0 = y0 + 4 + tier * 26
        tw = d.textlength(text, font=F14)
        d.rectangle([px - tw / 2 - 5, ty0, px + tw / 2 + 5, ty0 + 22],
                    fill=(255, 255, 255), outline=col)
        d.text((px - tw / 2, ty0 + 2), text, col, font=F14)

    for i, (lab, u, f) in enumerate(rows):
        px = x0 + int(round((u - CROP[0]) * ZOOM))
        d.line([px, y0, px, y0 + zh], fill=NEW, width=3)
        d.rectangle([px - 15, y0 + zh - 30, px + 15, y0 + zh - 2], fill=NEW)
        d.text((px - 13, y0 + zh - 27), lab, (255, 255, 255), font=F22)
        tag(px, "%s  f %.3f" % (lab, f), NEW, tier=i)
    pa = x0 + int(round((ANSWERED - CROP[0]) * ZOOM))
    d.line([pa, y0, pa, y0 + zh], fill=RED, width=4)
    d.rectangle([pa - 13, y0 + zh - 30, pa + 13, y0 + zh - 2], fill=RED)
    d.text((pa - 6, y0 + zh - 27), "1", (255, 255, 255), font=F22)
    tag(pa, "1  f %.3f  YOUR ANSWER" % f_ans, RED, tier=len(rows))
    d.text((x0, y0 + zh + 8),
           "ref_workshop.jpg  crop box (u,v) = (%d, %d) - (%d, %d)  at x%d   "
           "-- WIDENED LEFT from rev 32's u0 = 188" % (CROP + (ZOOM,)),
           INK, font=F14)

    y1 = y0 + zh + 44
    cv.paste(wide, (x0, y1))
    d.rectangle([x0 - 1, y1 - 1, x0 + ww, y1 + wh], outline=INK)
    for lab, u, f in rows:
        px = x0 + int(round((u - WIDE[0]) * ZOOM_W))
        d.line([px, y1, px, y1 + wh], fill=NEW, width=2)
    pa2 = x0 + int(round((ANSWERED - WIDE[0]) * ZOOM_W))
    d.line([pa2, y1, pa2, y1 + wh], fill=RED, width=3)
    qa = x0 + int(round((POST_U0 - WIDE[0]) * ZOOM_W))
    qb = x0 + int(round((POST_U1 - WIDE[0]) * ZOOM_W))
    d.rectangle([qa, y1 + 6, qb, y1 + wh - 6], outline=(0, 0, 0), width=3)
    d.text((qa - 4, y1 + wh - 26), "POST  u 355-377  MEASURED", (0, 0, 0),
           font=F14)
    pn = x0 + int(round((BAR_NEAR_U - WIDE[0]) * ZOOM_W))
    d.line([pn, y1, pn, y1 + wh], fill=(0, 0, 0), width=3)
    d.text((pn - 155, y1 + 6), "BAR NEAR END  u 487  MEASURED", (0, 0, 0),
           font=F14)
    d.text((x0, y1 + wh + 8),
           "the same bumper, wider:  crop box (u,v) = (%d, %d) - (%d, %d)  at "
           "x%d" % (WIDE + (ZOOM_W,)), INK, font=F14)

    ty = y1 + wh + 36
    lines = [
        ("WHAT EACH ANSWER YIELDS (recomputed at draw time, not typed):",
         INK),
        ("  L1 u 185 -> f %.3f     L2 u 190 -> f %.3f     L3 u 195 -> f %.3f"
         "     L4 u 200 -> f %.3f"
         % (rows[0][2], rows[1][2], rows[2][2], rows[3][2]), NEW),
        ("  your line 1  u 205 -> f %.3f" % f_ans, RED),
        ("", INK),
        ("THE ONLY ANSWER THAT HELPS IS A BOUND:", RED),
        ("  \"it is AT line 1, not left of it\" closes the open side and the "
         "residual becomes the line spacing alone.", INK),
        ("  \"it is at L1-L4\" moves the number and re-opens the question one "
         "step further left -- say it anyway if it is true.", INK),
        ("  \"I cannot tell from this frame\" is a real answer and it BINDS: "
         "the cross-ratio route closes for good, and the", INK),
        ("  post waits for a square-on frame of the FRONT rather than being "
         "built on a number this frame cannot support.", INK),
        ("", INK),
        ("CEILING, STATED: even a perfect answer here leaves the line-spacing "
         "residual, which straddles the published", INK),
        ("closing level depending on how it is read.  This figure closes ONE "
         "of the two open sides, not the question.", INK),
    ]
    for ln, col in lines:
        d.text((40, ty), ln, col, font=F17)
        ty += 23

    cv.save(OUT)
    print("\nQ1b written: %s   %dx%d" % (OUT, W, H))
    print("   crop A (u,v) = (%d,%d)-(%d,%d)  x%d   [CANDIDATE LINES]"
          % (CROP + (ZOOM,)))
    print("   crop B (u,v) = (%d,%d)-(%d,%d)  x%d   [CANDIDATE LINES]"
          % (WIDE + (ZOOM_W,)))


if __name__ == "__main__":
    build()
