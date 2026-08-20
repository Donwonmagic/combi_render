#!/usr/bin/env python3
"""mark_rev45_q.py -- FOUR crops, FOUR labels, ONE question.

SPEC 10.110, rev 45.  W0 of `NEXT_CONTEXT_PROMPT_rev45.md`.

WHY THIS FILE EXISTS.  The owner has reported the same defects three times and
rev 44 answered each with a measurement, a SPEC section and a guard -- eight
sections, thirty-odd findings, every guard green -- and his verdict was
"Definitely still a lot of the same problems."  That is not a geometry finding.
It is a finding about the LOOP: the fixes and the thing he is looking at are not
the same thing, and no amount of further measuring closes that by itself.

WHAT REV 36 TAUGHT AND REV 44 FORGOT.  `mark_rev37_region3.py` records it:
rev 36's first question figure carried five mark classes and his answer was "i
don't understand what is being asked"; the second was one crop, one circle, one
sentence and produced the most valuable answer in ten revisions.  THE RULE: if
he does not understand the question, the FIGURE is the defect, not him.

SO THERE ARE NO BOXES, NO ARROWS AND NO NUMBERS ON THE IMAGE.  Each panel is a
tight crop of ONE feature, filling its own frame, with a caption naming it.
The crop IS the pointer.  Four panels because the question is *which of these*,
which needs candidates; one mark class -- the crop -- because that is the
lesson.

WHAT EACH PANEL IS, AND WHY IT IS A CANDIDATE:
  1  THE VW ON THE NOSE.  Reported "off" at rev 44 and "still doesn't look
     right" at rev 44b.  rev 44b corrected its DRAWING (SPEC 10.107: all six
     stroke ends now reach the ring; four of six had floated since rev 15).
     NOBODY HAS CHECKED WHERE THE BADGE SITS -- see W1.
  2  THE CAB DOOR'S LOWER EDGE.  Reported twice.  rev 44b gave it the forward
     lower lobe (10.106) after 10.102 had removed too much of it.
  3  "100% CALIDAD".  Reported at rev 44 and open as ledger finding 5: the
     defect is COLOUR, not position -- it renders orange where the photograph
     is red, and the source is `cal_gen.py`'s gradient.
  4  THE SIGN'S PROPS.  Reported at rev 44b; 10.108 stood them up under the
     board (lean 49 deg -> 2.5 deg).

THIS FILE READS NO PIXELS FOR A NUMBER.  It crops, it captions, it writes a PNG.
"""
import os
from PIL import Image, ImageDraw

SRC = os.environ.get("T1_MARKSRC", "out/HERO2_hero.png")
OUT = "marks/mark_rev45_q.png"

# (label, crop box in SRC pixels).  Boxes are chosen to put ONE feature in the
# middle of its own panel with enough context to place it on the vehicle.
PANELS = [
    ("1.  THE VW ON THE NOSE",            (830, 1180, 1110, 1460)),
    ("2.  THE CAB DOOR'S LOWER EDGE",     (1240, 1120, 2000, 1760)),
    ("3.  \"100% CALIDAD\"",              (2300, 700,  2600, 960)),
    ("4.  THE SIGN'S PROPS",              (1080, 540,  1880, 820)),
]
PANEL_W, PAD, CAP = 760, 26, 46


def main():
    src = Image.open(SRC).convert("RGB")
    tiles = []
    for label, box in PANELS:
        c = src.crop(box)
        h = int(c.height * PANEL_W / c.width)
        tiles.append((label, c.resize((PANEL_W, h), Image.LANCZOS)))
    rows = [tiles[0:2], tiles[2:4]]
    rh = [max(t[1].height for t in r) + CAP for r in rows]
    W = PANEL_W * 2 + PAD * 3
    H = sum(rh) + PAD * (len(rows) + 1) + 64
    im = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(im)
    d.text((PAD, 20), "Which of these still looks wrong, and what about it?",
           fill=(0, 0, 0))
    y = 56 + PAD
    for r, hh in zip(rows, rh):
        x = PAD
        for label, t in r:
            d.text((x, y), label, fill=(0, 0, 0))
            im.paste(t, (x, y + CAP - 18))
            x += PANEL_W + PAD
        y += hh + PAD
    os.makedirs("marks", exist_ok=True)
    im.save(OUT)
    print("wrote %s  (%d x %d)  from %s" % (OUT, im.width, im.height, SRC))


if __name__ == "__main__":
    main()
