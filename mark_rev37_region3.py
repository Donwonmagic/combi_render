#!/usr/bin/env python3
"""mark_rev37_region3.py -- ONE crop, ONE circle, ONE sentence.

SPEC 10.92, rev 37.  Re-puts a contradiction that has stood since rev 19 between
a reading the OWNER gave and a reading SPEC settled.

  * rev 12, SPEC ~853, settled from his own answer: the counter is a "tan top,
    brass nosing on the OUTER EDGE, **body cream below**" -- i.e. the pale band
    under the nosing is the VEHICLE'S OWN belt paint, not part of the counter.
  * rev 19, shown four candidate regions and asked which were the bus's own
    painted cream, he selected ONLY region 2 and did NOT select region 3, the
    band below the brass nosing.  Memory records this as "worth re-putting to
    him, it was not chased in rev 19."  It was not chased in rev 20-36 either.

WHY THIS FIGURE IS DELIBERATELY PLAIN.  rev 36's first question figure carried
five mark classes, printed crop boxes, a coalescence column and a priced null,
and his answer was "i don't understand what is being asked."  The second attempt
was one 7x crop, one red circle and one sentence, and produced the most valuable
answer in ten revisions.  THE RULE THAT CAME OUT OF IT: if he does not understand
the question, the FIGURE is the defect, not him.  So this figure has exactly ONE
mark and that mark is a POINTER -- it points at a surface, it does not measure
one, and no number is read from inside it.

WHAT THE ANSWER CLOSES.  It decides whether `countercream` should carry the band
at all.  The band is currently painted by the COUNTER's material; if it is the
body's belt paint it belongs to `body_paint`'s cream and inherits the flank's
weathering, fade and dust -- none of which the counter's material applies.  That
is a shader-routing consequence, not a geometry one, so nothing moves on it until
he answers.  It also bears on `COUNTERTAN`'s level bracket, whose fascia arm sits
directly below this band.

NOT CLAIMED HERE: any colour statistic.  This file reads NO pixels for a number.
It crops, it draws one circle, it writes a PNG.  A sampling window would be a
different mark class and rev 36's lesson is that mixing classes is what made the
figure unanswerable.
"""
import os
from PIL import Image, ImageDraw

SRC = "ref_side.jpg"
OUT = os.environ.get("T1_OUT", "rev37_region3.png")
ZOOM = 7

# The crop.  Chosen to contain the whole counter section in one view: the tan top
# (rows 412-414), the brass nosing (416-419, SPEC 10.60's own row scan) and the
# pale band below it, with enough body above and below to place them.  PRINTED
# BELOW IN ORIGINAL-FRAME COORDINATES, per the standing rule.
CROP = (556, 396, 700, 448)          # u0, v0, u1, v1  in ref_side.jpg

# The single mark.  A POINTER at the pale band under the nosing -- region 3.
# Its centre row is chosen as the middle of the band between the nosing's lower
# edge (row 420) and where the body shadow begins; it points, it does not sample.
MARK_U, MARK_V, MARK_R = 628, 429, 9


def main():
    if not os.path.exists(SRC):
        raise SystemExit(f"{SRC} not found -- run from the repo root")
    im = Image.open(SRC).convert("RGB")
    W, H = im.size
    u0, v0, u1, v1 = CROP
    if not (0 <= u0 < u1 <= W and 0 <= v0 < v1 <= H):
        raise SystemExit("REFUSING TO WRITE: the crop box is outside the frame")
    if not (u0 < MARK_U < u1 and v0 < MARK_V < v1):
        raise SystemExit("REFUSING TO WRITE: the mark is outside its own crop -- "
                         "a figure whose mark is off the page has asked nothing")

    sub = im.crop(CROP).resize(((u1 - u0) * ZOOM, (v1 - v0) * ZOOM),
                               Image.LANCZOS)
    d = ImageDraw.Draw(sub)
    cx, cy = (MARK_U - u0) * ZOOM, (MARK_V - v0) * ZOOM
    r = MARK_R * ZOOM
    for w in (5, 4, 3):                       # one ring, drawn thick to read
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(255, 0, 0), width=w)

    sub.save(OUT)
    print(f"wrote {OUT}  {sub.size[0]}x{sub.size[1]}  ({ZOOM}x)")
    print(f"  source        : {SRC} {W}x{H}")
    print(f"  crop box      : u {u0}-{u1}, v {v0}-{v1}  (original-frame coords)")
    print(f"  the ONE mark  : a POINTER, a red circle centred at "
          f"u={MARK_U} v={MARK_V}, radius {MARK_R} px in original-frame terms")
    print(f"  it is NOT a sampling window and NO number is read from inside it")
    print(f"  for reference : SPEC 10.60 puts the counter's tan top at rows "
          f"412-414 and the brass nosing at rows 416-419 in this frame")
    print()
    print("  THE ONE SENTENCE PUT TO HIM:")
    print("    Is the pale band inside the red circle the BUS's own painted")
    print("    body, or is it part of the COUNTER?")


if __name__ == "__main__":
    main()
