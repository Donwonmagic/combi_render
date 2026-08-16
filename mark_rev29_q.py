"""mark_rev29_q.py -- rev 29.  Draws the ONE owner question, with its crop box
printed on the image AND on the console, and with the photograph shown BESIDE
a render of the CURRENT BUILD (rev 26's lesson -- that is what turned the
over-rider from a vague question into a decisive one).

THE QUESTION
------------
`probe_dust_scope.py` established BY EXECUTION that `W_DUST_FAC_UP` is not the
counter-top constant `t1_mats.py:366`/:467 and SPEC 10.81 describe.  It is one
MULTIPLY node inside the file's ONE shared `WEATHER` node-tree, reaching
ELEVEN materials.  Setting `T1_W_DUP=0` takes ALL ELEVEN to zero, not just
`countertan`.  The largest surface it films is the ROOF: `T1_body` under
`T1_paint`, 12.3697 m^2 of up-facing area at mean coverage 0.3916.

The owner's rev-28 reading -- the counter top is CLEAN VARNISHED PLYWOOD -- is
LOCAL to one surface.  The lever is GLOBAL.  So:

    DOES `ref_rear34.jpg` SHOW THE ROOF AS DUSTY OR CLEAN?

It changes the work either way, which is why it is worth his time:
  * ROOF DUSTY  -> the global film is doing correct work and must NOT be
    zeroed; the counter needs a LOCAL fix (its own `dust` input, or its own
    constant), and `W_DUST_FAC_UP` stays where it is.
  * ROOF CLEAN  -> the whole up-face film is contradicted, not just one
    surface, and `W_DUST_FAC_UP = 0` becomes SUPPORTED for the first time --
    leaving the 34.0 % blue shortfall (SPEC 10.81) as a separate
    `COUNTERTAN`/`CREAM` problem, which it always was.

BOX ROLE, stated per rev 28's standing requirement
--------------------------------------------------
**BOX A IS A POINTER, NOT A SAMPLING WINDOW.**  No number in rev 29 is taken
from it.  It says "this surface".  It was validated before being drawn by
`probe_updust_pointer.py`, whose acceptance band has NO free parameter: box A
sits 20.6x closer in log-ratio to a box the owner ALREADY ANSWERED
(rev 28's counter pointer, 3.08 x its floor) than to SPEC 10.76's
PROVEN straddler (14.14 x).  Three thresholds were tried and the first two
were wrong; all three are recorded in that file rather than smoothed away.

The counter-top anchor is drawn too, in a DIFFERENT colour and labelled
ANSWERED, so the question carries its own scale: he can see what he already
called clean, right next to what he is being asked about.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "rev29_q1_roofdust.png")

RED = (228, 26, 28)
BLU = (55, 126, 184)
INK = (20, 20, 20)
BG = (250, 250, 248)

#  (u0, u1, v0, v1) on ref_rear34.jpg
BOX_A = (860, 930, 234, 246)          # ROOF CROWN     -- the question
BOX_ANS = (640, 680, 420, 435)        # counter top    -- rev 28, ANSWERED
VIEW = (760, 1180, 190, 300)          # photo crop for panel 1
VIEW2 = (560, 1000, 380, 470)         # photo crop for the answered anchor
# the same roof, in the render (hero34r, 1200x820)
RVIEW = (250, 790, 268, 400)


def font(sz):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


F, FS = font(21), font(16)


def strip(im, view, zoom, boxes, title, sub):
    u0, u1, v0, v1 = view
    c = im.crop((u0, v0, u1, v1))
    w, h = int((u1 - u0) * zoom), int((v1 - v0) * zoom)
    c = c.resize((w, h), Image.LANCZOS)
    pan = Image.new("RGB", (w + 24, h + 74), BG)
    pan.paste(c, (12, 62))
    d = ImageDraw.Draw(pan)
    d.text((12, 8), title, font=F, fill=INK)
    d.text((12, 36), sub, font=FS, fill=(90, 90, 90))
    for lbl, (bu0, bu1, bv0, bv1), col, note in boxes:
        x0, y0 = 12 + (bu0 - u0) * zoom, 62 + (bv0 - v0) * zoom
        x1, y1 = 12 + (bu1 - u0) * zoom, 62 + (bv1 - v0) * zoom
        for k in range(3):
            d.rectangle([x0 - k, y0 - k, x1 + k, y1 + k], outline=col)
        tw = d.textbbox((0, 0), lbl, font=F)[2]
        d.rectangle([x0 - 3, y0 - 34, x0 + tw + 11, y0 - 4], fill=col)
        d.text((x0 + 4, y0 - 31), lbl, font=F, fill=(255, 255, 255))
        d.text((x1 + 12, y0 - 2), note, font=FS, fill=col)
    d.rectangle([0, 0, pan.size[0] - 1, pan.size[1] - 1], outline=(215, 215,
                                                                   210))
    return pan


def main():
    rear = Image.open(os.path.join(ROOT, "ref_rear34.jpg")).convert("RGB")
    A = Image.open("/tmp/ab/A_hero34r.png").convert("RGB")
    B = Image.open("/tmp/ab/B_hero34r.png").convert("RGB")

    p1 = strip(rear, VIEW, 3.0,
               [("A", BOX_A, RED, "ROOF CROWN -- is this dusty or clean?")],
               "1.  THE PHOTOGRAPH -- ref_rear34.jpg, the roof aft of the "
               "opening",
               "box A is a POINTER, not a sampling window.  No number is "
               "taken from it.")
    p2 = strip(rear, VIEW2, 3.0,
               [("ANSWERED", BOX_ANS, BLU,
                 "you read this as CLEAN VARNISHED PLYWOOD (rev 28)")],
               "2.  YOUR OWN ANCHOR -- the same frame, the counter top",
               "shown so the question carries its own scale, not as a new "
               "question.")
    p3 = strip(A, RVIEW, 2.35, [],
               "3.  THE MODEL AS SHIPPED -- W_DUST_FAC_UP 0.7313",
               "the roof carries mean ochre coverage 0.3916 over 12.3697 m2 "
               "of up-facing area.")
    p4 = strip(B, RVIEW, 2.35, [],
               "4.  THE MODEL WITH THE UP-FACE FILM OFF -- T1_W_DUP=0",
               "same build, same light, same camera; ONLY the up-face dust "
               "removed.")

    ws = [p.size[0] for p in (p1, p2, p3, p4)]
    hs = [p.size[1] for p in (p1, p2, p3, p4)]
    W = max(ws) + 24
    foot = 250
    canvas = Image.new("RGB", (W, sum(hs) + 40 + foot), BG)
    y = 14
    for p in (p1, p2, p3, p4):
        canvas.paste(p, (12, y))
        y += p.size[1] + 8
    d = ImageDraw.Draw(canvas)
    y += 14
    lines = [
        ("THE QUESTION -- one, multiple choice.", F, INK),
        ("Looking at box A in panel 1: does the ROOF in ref_rear34.jpg carry "
         "a visible settled-dust film?", FS, INK),
        ("", FS, INK),
        ("  1.  CLEAN  -- the roof looks like painted cream, the way you "
         "read the counter top.", FS, INK),
        ("  2.  DUSTY  -- there is a visible ochre/grey settled film, like "
         "panel 3.", FS, INK),
        ("  3.  PARTLY -- dusty in places, clean in others.", FS, INK),
        ("  4.  CAN'T TELL from this frame.", FS, INK),
        ("", FS, INK),
        ("WHY IT MATTERS, both ways:", F, INK),
        ("  answer 2 or 3  ->  the global up-face film is doing correct work. "
         "W_DUST_FAC_UP STAYS, and the", FS, INK),
        ("                     counter gets a LOCAL fix instead.", FS, INK),
        ("  answer 1       ->  the film is contradicted on the largest "
         "surface it paints, not just on the", FS, INK),
        ("                     counter, and W_DUST_FAC_UP = 0 becomes "
         "supported for the first time.", FS, INK),
        ("", FS, INK),
        ("W_DUST_FAC_UP is ONE node in the file's ONE shared WEATHER group. "
         "It reaches ELEVEN materials:", FS, (90, 90, 90)),
        ("T1_paint, cream, bumpercream, countercream, countertan, wheelcream, "
         "capwhite, capred, roundelred,", FS, (90, 90, 90)),
        ("calidad, script.  T1_W_DUP=0 takes ALL ELEVEN to zero -- measured, "
         "not inferred.", FS, (90, 90, 90)),
    ]
    for t, f, col in lines:
        d.text((16, y), t, font=f, fill=col)
        y += (30 if f is F else 22)
    canvas.save(OUT)

    print("\nEVERY BOX, PRINTED")
    print("  %-10s %-28s %s" % ("label", "crop box (u0-u1, v0-v1)", "role"))
    print("  %-10s u %d-%d  v %d-%d      %s"
          % ("A", BOX_A[0], BOX_A[1], BOX_A[2], BOX_A[3],
             "POINTER -- the rev-29 question"))
    print("  %-10s u %d-%d  v %d-%d      %s"
          % ("ANSWERED", BOX_ANS[0], BOX_ANS[1], BOX_ANS[2], BOX_ANS[3],
             "rev 28's own pointer, already answered CLEAN"))
    print("  photo crops : panel 1 %s   panel 2 %s" % (VIEW, VIEW2))
    print("  render crop : %s of hero34r 1200x820" % (RVIEW,))
    print("\n  wrote %s  (%d x %d)" % (OUT, canvas.size[0], canvas.size[1]))
    print("\n  BOX A IS A POINTER.  No number in rev 29 is taken from it.")
    print("  Validation: probe_updust_pointer.py, 6 controls, 0 failed.")


if __name__ == "__main__":
    main()
