"""mark_rev31_q.py -- rev 31.  READ-ONLY.  Draws the owner questions for the
OVER-RIDER POST (SPEC 10.75 box C / 10.83), with every crop box printed on the
image AND on the console, every box's ROLE stated, and the photograph shown
BESIDE a render of the CURRENT BUILD.

WHY THESE TWO QUESTIONS AND NOT THE ONES THE BRIEF ASKED FOR
------------------------------------------------------------
The rev-31 brief proposed a single-view projection solve on `ref_workshop.jpg`
using the WORKSHOP's own architecture, with the bumper top at 0.348 m as the
known height, to recover the post's LATERAL position.  `probe_orb_post.py` was
built to test the first link of that chain and IT BROKE:

  the vehicle's own long "horizontal" edges DO NOT SHARE A VANISHING POINT.
  Three edges pass an rms gate -- two of them fit to rms 0.091 and 0.096 px --
  and their pairwise intersections land at u = +1529, +1284 and -5843, a spread
  of 7372 px across a 1200 px frame, and they change SIDE.

That is not a tracing failure at 0.09 px.  Those edges are genuinely not
parallel on the real vehicle: `t1_mats.z_belt(x)` makes the belt a SLOPED line
and the roof carries its own rake and crown.  So the vehicle's fore-aft
direction cannot be read off the vehicle, and the building's own lines give the
BUILDING's frame -- transferring that to the vehicle needs the vehicle's YAW,
which is one more unmeasured link the brief's framing does not carry.

AND THE THING THAT ACTUALLY BLOCKS THE POST IS UPSTREAM OF ALL OF IT.  SPEC
10.83 refuted "the post is at the centreline" by comparing the post's columns
(357-374) with the V apex at u = 311.5.  **Those two features are at different
DEPTHS** -- the apex is on the nose skin, the post stands in the bumper plane,
forward of it by a standoff 10.83 itself grades "A CHOICE, not a reading".  The
whole refutation is a 54.0 px offset, and the sign of the unpriced parallax is
UNDECIDED: the only two centreline features at different depths, the roundel
and the apex, differ by +5.5 px against REF Sec 9's own +-4 px band, 1.38 sigma.

So the two things standing between here and any progress are READINGS OF THE
PHOTOGRAPH, not calculations, and neither is one measurement can take.

BOX ROLES -- stated, per rev 28's standing requirement
------------------------------------------------------
**EVERY BOX ON THIS FIGURE IS A POINTER.  NOT ONE IS A SAMPLING WINDOW.**
No number in this revision is taken from any of them.  rev 30's S1 and S2 were
sampling windows and that was said on the figure; this revision takes no
samples, and that is said here for the same reason.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(ROOT, "ref_workshop.jpg")
RENDER = "/tmp/r31/q_raw.png"
OUT = os.path.join(ROOT, "rev31_q_post.png")

RED = (228, 26, 28)
BLU = (55, 126, 184)
GRN = (30, 140, 60)
ORA = (230, 130, 20)
INK = (20, 20, 20)
GREY = (120, 120, 120)
BG = (250, 250, 248)

# ---- crop boxes on ref_workshop.jpg, (u0, u1, v0, v1).  ALL POINTERS. ----
P_LEFT = (203, 232, 626, 702)     # Q1: the cream feature at the bar's far end
P_POST = (357, 374, 676, 700)     # Q2: SPEC 10.75 box C, the centre post
P_HOOP = (442, 490, 652, 720)     # reference: the near end, ANSWERED rev 30
P_APEX = (304, 319, 662, 676)     # reference: V apex u=311.5, REF Sec 9

VIEW = (185, 515, 600, 740)       # the photograph crop shown
RVIEW = (250, 655, 735, 900)      # the render crop shown, of q_raw 1500x1000

SCALE = 3


def font(sz, bold=True):
    p = ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
         "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    return ImageFont.truetype(p, sz) if os.path.exists(p) else \
        ImageFont.load_default()


F, FS, FT = font(26), font(19, False), font(16, False)

_MEASURE = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def wrap(text, px):
    """Greedy wrap to a pixel width, so a subtitle can never be clipped."""
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if cur and _MEASURE.textlength(t, font=FT) > px:
            out.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        out.append(cur)
    return out


def panel(im, view, scale, boxes, title, sub):
    u0, u1, v0, v1 = view
    c = im.crop((u0, v0, u1, v1))
    W, H = (u1 - u0) * scale, (v1 - v0) * scale
    c = c.resize((W, H), Image.LANCZOS)
    sub_lines = wrap(sub, W - 12)
    top = 44 + 20 * len(sub_lines)
    out = Image.new("RGB", (W + 8, H + top + 8), BG)
    out.paste(c, (4, top))
    d = ImageDraw.Draw(out)
    d.text((6, 6), title, font=F, fill=INK)
    for i, ln in enumerate(sub_lines):
        d.text((6, 40 + 20 * i), ln, font=FT, fill=GREY)
    d.rectangle([4, top, 4 + W - 1, top + H - 1], outline=(200, 200, 200))
    for (b, col, lab) in boxes:
        bu0, bu1, bv0, bv1 = b
        x0 = 4 + (bu0 - u0) * scale
        x1 = 4 + (bu1 - u0) * scale
        y0 = top + (bv0 - v0) * scale
        y1 = top + (bv1 - v0) * scale
        d.rectangle([x0, y0, x1, y1], outline=col, width=3)
        tw = d.textlength(lab, font=FS)
        x0 = min(x0, W - tw - 12)
        ty = y0 - 26 if y0 - 26 > top else y1 + 4
        d.rectangle([x0, ty, x0 + tw + 8, ty + 24], fill=col)
        d.text((x0 + 4, ty + 2), lab, font=FS, fill=(255, 255, 255))
    return out


def main():
    ph = Image.open(REF).convert("RGB")
    have = os.path.exists(RENDER)
    boxes = [
        (P_LEFT, RED, "Q1  what is this?"),
        (P_POST, BLU, "Q2  the post"),
        (P_HOOP, GRN, "near end - answered rev 30"),
        (P_APEX, ORA, "V apex u=311.5"),
    ]
    left = panel(ph, VIEW, SCALE, boxes,
                 "THE PHOTOGRAPH -- ref_workshop.jpg",
                 "crop (u,v) = (%d,%d)-(%d,%d) at x%d.   EVERY BOX IS A "
                 "POINTER.  NO BOX IS A SAMPLING WINDOW -- no number in rev 31 "
                 "is taken from any of them."
                 % (VIEW[0], VIEW[2], VIEW[1], VIEW[3], SCALE))

    if have:
        r = Image.open(RENDER).convert("RGB")
        right = panel(r, RVIEW, 2, [],
                      "THE CURRENT BUILD -- rev 30, 148 commits",
                      "hero34f 1500x1000, crop (%d,%d)-(%d,%d) at x2.  The bar "
                      "IS built (SPEC 10.83).  THE POST IS NOT."
                      % (RVIEW[0], RVIEW[2], RVIEW[1], RVIEW[3]))
    else:
        right = Image.new("RGB", (600, 400), BG)
        ImageDraw.Draw(right).text((10, 10), "*** RENDER MISSING ***",
                                   font=F, fill=RED)

    H = max(left.height, right.height)
    W = left.width + right.width + 24
    out = Image.new("RGB", (W, H + 150), BG)
    out.paste(left, (0, 0))
    out.paste(right, (left.width + 24, 0))
    d = ImageDraw.Draw(out)
    y = H + 8
    lines = [
        ("Q1  (red)  The near end of the bar turns down and back in a rounded "
         "hoop -- that is settled (green box, rev 30).  At the FAR end there is "
         "a cream feature SPEC has never recorded.  What is it?", INK),
        ("      (a) the bar's own end, turning down in a hoop -- the mirror of "
         "the green one    (b) a SECOND vertical post like the blue one", GREY),
        ("      (c) the bumper BLADE's front corner wrapping round, seen "
         "edge-on -- nothing to do with the bar    (d) can't tell", GREY),
        ("", INK),
        ("Q2  (blue)  Does the post stand in the BUMPER plane, joining bar to "
         "blade only -- or does it also run BACK to the green body panel as a "
         "mounting stay?", INK),
        ("      (a) bumper plane only    (b) it runs back to the body    "
         "(c) can't tell", GREY),
        ("", INK),
        ("Why each matters:  Q1 -- if (a), the bar's two ends bracket the post "
         "and its position becomes a SCALE-FREE FRACTION of the bar's "
         "half-width, needing no calibration, no", GREY),
        ("ground plane and no standoff.  If (c), the far end is not visible at "
         "all and that route is shut.   Q2 -- a stay running back sits at a "
         "DIFFERENT DEPTH from the bumper plane,", GREY),
        ("which is exactly the unpriced parallax that SPEC 10.83's refutation "
         "of 'the post is at the centreline' rests on.  A 'can't tell' is a "
         "result and it binds -- please say so if so.", GREY),
    ]
    for t, col in lines:
        d.text((8, y), t, font=FT, fill=col)
        y += 20
    out.save(OUT)

    print("mark_rev31_q.py -- READ-ONLY")
    print("  photo crop  : (u,v) (%d,%d)-(%d,%d) of ref_workshop.jpg at x%d"
          % (VIEW[0], VIEW[2], VIEW[1], VIEW[3], SCALE))
    print("  render crop : (%d,%d)-(%d,%d) of q_raw 1500x1000 at x2%s"
          % (RVIEW[0], RVIEW[2], RVIEW[1], RVIEW[3],
             "" if have else "   *** RENDER MISSING ***"))
    print("  BOX ROLES -- ALL FOUR ARE POINTERS.  NONE IS A SAMPLING WINDOW.")
    for nm, b in (("Q1 far-end feature", P_LEFT), ("Q2 the post", P_POST),
                  ("near hoop end (ans.)", P_HOOP), ("V apex", P_APEX)):
        print("    %-22s (u %d-%d, v %d-%d)  POINTER" % (nm, b[0], b[1],
                                                         b[2], b[3]))
    print("  wrote %s  %dx%d" % (OUT, out.width, out.height))
    return 0


if __name__ == "__main__":
    sys.exit(main())
