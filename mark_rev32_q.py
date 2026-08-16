"""mark_rev32_q.py -- rev 32.  Draws the TWO owner questions, each with its
crop box printed on the image AND on the console, each box's ROLE stated, and
each photograph shown BESIDE a render of the CURRENT BUILD.

Q1 -- THE BAR'S FAR END (unblocks SPEC 10.75's POST, the oldest undone item)
---------------------------------------------------------------------------
rev 32 tested two routes to the post's lateral position and MEASURED both
before spending the revision.

  Route A, the CROSS-RATIO of four collinear points in the bumper plane
  (bar far end, far strut, near post, bar near end).  Four collinear points
  carry a projective invariant, so this needs NO vanishing point, NO scale and
  NO depth -- it repairs SPEC 10.84's objection at the root, because every one
  of the four is in the SAME plane.  Under the symmetry model (ends at +-1,
  struts at +-f) the invariant is (1+f)^2 / 4f: one equation, one unknown.

  IT FAILS ON ONE TERM AND ONLY ONE.  With the far bar end at u = 209 the
  solution is f = 0.626.  Moving that one column by +15 px -- INSIDE rev 31's
  own stated ~29 px blob -- gives f = 0.820.  A 31 % swing, with the
  discriminant heading for the degenerate root f = 1.  The far end's 29 px is
  not "the stated precision" on this route; it is fatal to it.

  Route B, the transverse VP by harmonic conjugate.  Every construction of
  that VP available in this frame reduces to a difference of two nearly equal
  near/far half-widths, and my own four row-wise estimates off the V arms
  scatter over 154 px.  That propagates to about +-21 % on f.

SO THE WHOLE PROBLEM IS ONE COLUMN, and it is the one column measurement
cannot reach: rev 31 established BY HIS OWN READING that the far end is a
SUPERPOSITION of three members -- "covering the bumper, the post, and the far
end of the bar".  A superposition is not resolvable by thresholding it.

    WHERE DOES THE OVER-RIDER BAR ITSELF END, on the far side?

FIVE CANDIDATE LINES are drawn.  **THEY ARE CANDIDATE LINES, NOT SAMPLING
WINDOWS AND NOT POINTERS.**  No number in rev 32 is taken from any of them.
The number comes from whichever one he picks -- or from none of them, because
rev 31's rule stands: HIS ANSWER MAY NOT BE ONE OF THE OPTIONS.  If the bar
does not visibly terminate at all, that is an answer too and it binds.

Q2 -- SPEC 10.82's THREE UNASKED SURFACES
-----------------------------------------
rev 29 retired `W_DUST_FAC_UP` 0.7313 -> 0.0 on his reading that the ROOF in
`ref_rear34.jpg` is clean.  That lever is GLOBAL: it films eleven materials.
rev 29 named, rather than hid, that it therefore asserts more than two readings
support -- the BUMPER TOP, the RIM BARRELS and the HUB CAPS are filmed by the
same node and NOBODY HAS BEEN ASKED.  rev 30 and rev 31 both carried the item
forward without asking.

    DO THE BUMPER TOP, THE RIM BARRELS AND THE HUB CAPS CARRY DUST?

It changes the work either way:
  * ALL CLEAN  -> the global zeroing is supported on three further surfaces
    and SPEC 10.82's named gap closes.
  * ANY DUSTY  -> a global f = 0 is contradicted on that surface, and the film
    needs to become LOCAL (per-material dust input) rather than one lever.

**BOXES B1, B2 AND B3 ARE POINTERS, NOT SAMPLING WINDOWS.**  They say "this
surface".  No number is taken from them.  The two renders beside them are the
CURRENT BUILD (film OFF, shipped) and the SAME BUILD with `T1_W_DUP=0.7313`
restored -- his own scale for what the film looks like when it is on.

**STATED, NOT HIDDEN: the renders are the IN-SERVICE red/cream livery and the
photograph is the GREEN conversion stage.**  The question is about the FILM,
not the colour; the two renders differ from each other ONLY by the dust lever
(measured: max channel difference 41, 10.67 % of pixels moving by more than 2).
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT1 = os.path.join(ROOT, "rev32_q1_barend.png")
OUT2 = os.path.join(ROOT, "rev32_q2_surfaces.png")

RED = (228, 26, 28)
BLU = (55, 126, 184)
GRN = (30, 145, 70)
ORA = (255, 127, 0)
PUR = (140, 86, 190)
INK = (18, 18, 18)
BG = (250, 250, 248)

REF_W = os.path.join(ROOT, "ref_workshop.jpg")
REF_S = os.path.join(ROOT, "ref_side.jpg")

# ---------------------------------------------------------------- Q1 geometry
# crop box on ref_workshop.jpg, PRINTED to the console as well as drawn
Q1_CROP = (188, 606, 300, 706)          # u0, v0, u1, v1
Q1_ZOOM = 9
# candidate columns for the bar's far termination, in ORIGINAL frame pixels
Q1_CAND = [
    ("1", 205, RED),
    ("2", 212, ORA),
    ("3", 219, GRN),
    ("4", 228, BLU),
    ("5", 240, PUR),
]
# the two things that ARE measured, for scale, drawn on the wide strip
Q1_WIDE = (190, 640, 510, 740)
Q1_ZOOM_W = 4
POST_U0, POST_U1 = 355.0, 377.0         # MEASURED this revision, cream-run scan
BAR_NEAR_U = 487.0                      # MEASURED this revision, hoop outer

# ---------------------------------------------------------------- Q2 geometry
# POINTERS.  Validated BEFORE sending by probe_rev32_pointer.py against rev
# 29's two calibration anchors, band UNCHANGED.  B1 1.96x, B2 1.81x, B3 2.78x
# against an ANSWERED box's 3.14x and a PROVEN straddler's 13.54x.
#
# THE FRAME FOR B2/B3 IS ref_side.jpg, NOT ref_workshop.jpg, AND THAT IS A
# CORRECTION TO THE WORK LIST.  rev 29, rev 30, rev 31 and the rev-32 brief
# all say "the workshop frame shows all three".  It does not: in
# ref_workshop.jpg BOTH road wheels are BARE PAINTED RIMS WITH NO HUB CAP --
# the vehicle is at conversion stage.  The hub caps exist only in ref_side.jpg.
B1 = (262, 702, 288, 710)               # BUMPER TOP  -- ref_workshop.jpg
B2 = (708, 590, 719, 620)               # RIM FACE    -- ref_side.jpg
B3 = (756, 586, 774, 602)               # HUB CAP     -- ref_side.jpg
Q2_VIEW_A = (215, 660, 375, 740)        # ref_workshop crop, the front bumper
Q2_VIEW_B = (690, 545, 810, 665)        # ref_side crop, the rear wheel
R_CROP = (170, 405, 440, 515)           # the same hardware in the render

REND_OFF = "/tmp/q32/q32a_hero34f.png"
REND_ON = "/tmp/q32/q32b_hero34f.png"


def font(sz):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


F14, F17, F22, F28 = font(14), font(17), font(22), font(28)


def crop_zoom(im, box, z):
    u0, v0, u1, v1 = box
    c = im.crop((u0, v0, u1, v1))
    return c.resize(((u1 - u0) * z, (v1 - v0) * z), Image.LANCZOS)


def build_q1():
    im = Image.open(REF_W).convert("RGB")
    z = crop_zoom(im, Q1_CROP, Q1_ZOOM)
    zw, zh = z.size
    wide = crop_zoom(im, Q1_WIDE, Q1_ZOOM_W)
    ww, wh = wide.size

    W = max(zw, ww) + 80
    H = 150 + zh + 60 + wh + 190
    cv = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(cv)

    d.text((40, 26), "rev 32  Q1 -- WHERE DOES THE OVER-RIDER BAR END, "
                     "ON THE FAR SIDE?", INK, font=F28)
    d.text((40, 66), "The post's lateral position turns on this ONE column. "
                     "Everything else in the construction is already measured.",
           INK, font=F17)
    d.text((40, 90), "THE FIVE LINES ARE CANDIDATES, NOT SAMPLING WINDOWS AND "
                     "NOT POINTERS.  No number is taken from any of them.",
           RED, font=F17)
    d.text((40, 114), "If none of them is right, say so -- that binds, and it "
                      "is a better answer than the set.", INK, font=F17)

    x0, y0 = 40, 148
    cv.paste(z, (x0, y0))
    d.rectangle([x0 - 1, y0 - 1, x0 + zw, y0 + zh], outline=INK)
    for lab, u, col in Q1_CAND:
        px = x0 + int(round((u - Q1_CROP[0]) * Q1_ZOOM))
        d.line([px, y0, px, y0 + zh], fill=col, width=3)
        d.rectangle([px - 13, y0 + zh - 30, px + 13, y0 + zh - 2], fill=col)
        d.text((px - 6, y0 + zh - 27), lab, (255, 255, 255), font=F22)
    d.text((x0, y0 + zh + 8),
           "ref_workshop.jpg  crop box (u,v) = (%d, %d) - (%d, %d)  at x%d"
           % (Q1_CROP[0], Q1_CROP[1], Q1_CROP[2], Q1_CROP[3], Q1_ZOOM),
           INK, font=F14)

    y1 = y0 + zh + 44
    cv.paste(wide, (x0, y1))
    d.rectangle([x0 - 1, y1 - 1, x0 + ww, y1 + wh], outline=INK)
    for lab, u, col in Q1_CAND:
        px = x0 + int(round((u - Q1_WIDE[0]) * Q1_ZOOM_W))
        d.line([px, y1, px, y1 + wh], fill=col, width=2)
    pa = x0 + int(round((POST_U0 - Q1_WIDE[0]) * Q1_ZOOM_W))
    pb = x0 + int(round((POST_U1 - Q1_WIDE[0]) * Q1_ZOOM_W))
    d.rectangle([pa, y1 + 6, pb, y1 + wh - 6], outline=(0, 0, 0), width=3)
    d.text((pa - 4, y1 + wh - 26), "POST  u 355-377  MEASURED", (0, 0, 0),
           font=F14)
    pn = x0 + int(round((BAR_NEAR_U - Q1_WIDE[0]) * Q1_ZOOM_W))
    d.line([pn, y1, pn, y1 + wh], fill=(0, 0, 0), width=3)
    d.text((pn - 150, y1 + 6), "BAR NEAR END  u 487  MEASURED", (0, 0, 0),
           font=F14)
    d.text((x0, y1 + wh + 8),
           "the same bumper, wider:  crop box (u,v) = (%d, %d) - (%d, %d)  "
           "at x%d" % (Q1_WIDE[0], Q1_WIDE[1], Q1_WIDE[2], Q1_WIDE[3],
                       Q1_ZOOM_W), INK, font=F14)

    ty = y1 + wh + 36
    for ln, col in [
        ("Why this one column decides it:  with the far end at u = 209 the "
         "post lands at 0.626 of the bar's half-width;", INK),
        ("at u = 224 it lands at 0.820.  A 15 px move -- inside rev 31's own "
         "~29 px blob -- swings the answer by 31 %.", INK),
        ("rev 31 established from your reading that this end is a "
         "SUPERPOSITION of bumper + post + bar.  Thresholding cannot", INK),
        ("separate a superposition, which is why this is a question and not a "
         "measurement.", INK),
    ]:
        d.text((40, ty), ln, col, font=F17)
        ty += 24
    cv.save(OUT1)
    print("Q1 written: %s   %dx%d" % (OUT1, W, H))
    print("   crop A (u,v) = (%d,%d)-(%d,%d)  x%d   [CANDIDATE LINES]"
          % (Q1_CROP + (Q1_ZOOM,)))
    print("   crop B (u,v) = (%d,%d)-(%d,%d)  x%d   [CANDIDATE LINES]"
          % (Q1_WIDE + (Q1_ZOOM_W,)))
    for lab, u, _ in Q1_CAND:
        print("     candidate %s : u = %d" % (lab, u))


def build_q2():
    imw = Image.open(REF_W).convert("RGB")
    ims = Image.open(REF_S).convert("RGB")
    a = Image.open(REND_OFF).convert("RGB")
    b = Image.open(REND_ON).convert("RGB")

    pa = crop_zoom(imw, Q2_VIEW_A, 6)
    pb = crop_zoom(ims, Q2_VIEW_B, 6)
    ra = crop_zoom(a, R_CROP, 4)
    rb = crop_zoom(b, R_CROP, 4)

    W = max(pa.size[0] + pb.size[0] + 120, ra.size[0] * 2 + 120)
    H = 190 + max(pa.size[1], pb.size[1]) + 90 + ra.size[1] + 210
    cv = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(cv)

    d.text((40, 26), "rev 32  Q2 -- DO THESE THREE SURFACES CARRY DUST?",
           INK, font=F28)
    d.text((40, 66), "SPEC 10.82's named gap.  You told rev 29 the ROOF is "
                     "clean, and that retired ONE GLOBAL lever that films "
                     "eleven materials.", INK, font=F17)
    d.text((40, 90), "These three are filmed by the same node -- 0.751 m2 of "
                     "up-face area between them -- and have never been asked "
                     "about.", INK, font=F17)
    d.text((40, 114), "B1, B2 AND B3 ARE POINTERS, NOT SAMPLING WINDOWS.  They "
                      "say 'this surface'.  No number is taken from them.",
           RED, font=F17)
    d.text((40, 138), "CORRECTION: the workshop frame does NOT show hub caps -- "
                      "both wheels there are bare painted rims.  B2 and B3 are "
                      "on ref_side.jpg.", (150, 60, 10), font=F17)

    def mark(box, view, z, ox, oy, col, lab, below=True):
        u0, v0, u1, v1 = box
        x0 = ox + (u0 - view[0]) * z
        y0 = oy + (v0 - view[1]) * z
        x1 = ox + (u1 - view[0]) * z
        y1 = oy + (v1 - view[1]) * z
        d.rectangle([x0, y0, x1, y1], outline=col, width=3)
        d.text((x0 - 4, (y1 + 6) if below else (y0 - 24)), lab, col, font=F17)

    x0, y0 = 40, 176
    cv.paste(pa, (x0, y0))
    d.rectangle([x0 - 1, y0 - 1, x0 + pa.size[0], y0 + pa.size[1]], outline=INK)
    mark(B1, Q2_VIEW_A, 6, x0, y0, RED, "B1  BUMPER TOP")
    d.text((x0, y0 + pa.size[1] + 30),
           "ref_workshop.jpg  crop (u,v) = (%d,%d)-(%d,%d) x6" % Q2_VIEW_A,
           INK, font=F14)

    x1 = x0 + pa.size[0] + 40
    cv.paste(pb, (x1, y0))
    d.rectangle([x1 - 1, y0 - 1, x1 + pb.size[0], y0 + pb.size[1]], outline=INK)
    mark(B2, Q2_VIEW_B, 6, x1, y0, BLU, "B2  RIM FACE")
    mark(B3, Q2_VIEW_B, 6, x1, y0, GRN, "B3  HUB CAP", below=False)
    d.text((x1, y0 + pb.size[1] + 30),
           "ref_side.jpg  crop (u,v) = (%d,%d)-(%d,%d) x6" % Q2_VIEW_B,
           INK, font=F14)

    y1 = y0 + max(pa.size[1], pb.size[1]) + 82
    cv.paste(ra, (x0, y1))
    d.rectangle([x0 - 1, y1 - 1, x0 + ra.size[0], y1 + ra.size[1]], outline=INK)
    d.text((x0, y1 + ra.size[1] + 8),
           "CURRENT BUILD -- film OFF (shipped, W_DUST_FAC_UP = 0.0)",
           INK, font=F17)
    x2 = x0 + ra.size[0] + 40
    cv.paste(rb, (x2, y1))
    d.rectangle([x2 - 1, y1 - 1, x2 + rb.size[0], y1 + rb.size[1]], outline=INK)
    d.text((x2, y1 + rb.size[1] + 8),
           "SAME BUILD -- film ON (T1_W_DUP = 0.7313, rev 29's retired value)",
           INK, font=F17)

    ty = y1 + ra.size[1] + 46
    for ln in [
        "The two renders differ ONLY by the dust lever.  Over this crop: mean "
        "|difference| 2.0 code values, max 40, 21 % of pixels moving.",
        "STATED, NOT HIDDEN: the renders are the in-service red/cream livery, "
        "the left photograph is the green conversion stage.",
        "The question is about the FILM, not the colour.  If a surface is dusty "
        "in a way neither render shows, say that -- it binds.",
        "Each pointer was validated before sending (probe_rev32_pointer.py): "
        "B1 1.96x, B2 1.81x, B3 2.78x, against a box you ALREADY answered at "
        "3.14x",
        "and a PROVEN straddler at 13.54x.  My first B3 failed at 8.77x and was "
        "moved, not excused -- 7 of 8 cap boxes fail, because the cap is a dome "
        "in shadow.",
    ]:
        d.text((40, ty), ln, INK, font=F17)
        ty += 24
    cv.save(OUT2)
    print("Q2 written: %s   %dx%d" % (OUT2, W, H))
    for nm, bx, fr in (("B1 BUMPER TOP", B1, "ref_workshop.jpg"),
                       ("B2 RIM FACE", B2, "ref_side.jpg"),
                       ("B3 HUB CAP", B3, "ref_side.jpg")):
        print("   POINTER %-14s (u,v) = (%d,%d)-(%d,%d)  on %s"
              % ((nm,) + bx + (fr,)))
    print("   photo crop A (u,v) = (%d,%d)-(%d,%d) x6  ref_workshop.jpg"
          % Q2_VIEW_A)
    print("   photo crop B (u,v) = (%d,%d)-(%d,%d) x6  ref_side.jpg"
          % Q2_VIEW_B)
    print("   render crop  (u,v) = (%d,%d)-(%d,%d) x4  on 900x600 hero34f"
          % R_CROP)


if __name__ == "__main__":
    build_q1()
    build_q2()
