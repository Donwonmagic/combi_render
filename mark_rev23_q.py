"""mark_rev23_q.py -- rev 23, READ-ONLY on the references.

Draws the rev-23 owner questions with EVERY crop box printed on the image and
to the console.  A crop I draw for him is a probe too -- thirteen recorded
instances (SPEC 10.43 / 10.49 / 10.57 / 10.60), and the FIRST draft of this
very file straddled the A-pillar and the windscreen aperture with box D.
That draft was thrown away rather than sent.  Fourteenth instance.

Both questions ask what a PHOTOGRAPH SHOWS.  Neither asks what the vehicle
looks like -- he has never stood in it.

Frame: ref_workshop.jpg -- DC quantiser 1 / 8.87 bits/px (SPEC 10.38), and
the ONLY frame in which the cab door is CLOSED, which is the only state in
which a cab-door shut line is observable at all.
"""
import os
from PIL import Image, ImageDraw, ImageFont

SRC = "ref_workshop.jpg"

# Q1 -- the three near-side openings.  Boxes follow each OPENING's own glass
# area, kept off the white pillars either side so no box spans two materials.
Q1_VIEW = (688, 320, 900, 462)
Q1_BOXES = [
    ("1", (706, 358, 734, 430), "sightline through the LEFT opening"),
    ("2", (752, 356, 786, 424), "sightline through the MIDDLE opening"),
    ("3", (820, 354, 852, 422), "sightline through the RIGHT opening"),
]

# Q2 -- the cab door only.  The forward edge of the DOOR GLASS and the door's
# own top rail.  Deliberately clear of the A-pillar and of the windscreen
# aperture, which is what the discarded draft got wrong.
Q2_VIEW = (500, 330, 600, 420)
Q2_BOXES = [
    ("4", (521, 356, 545, 392), "forward end of the door glass"),
    ("5", (548, 350, 588, 364), "the door's top rail"),
]


def font(sz, bold=True):
    for p in (("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
               if bold else
               "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def panel(im, view, boxes, title, sub, zoom):
    x0, y0, x1, y1 = view
    c = im.crop(view).resize(((x1 - x0) * zoom, (y1 - y0) * zoom),
                             Image.LANCZOS)
    d = ImageDraw.Draw(c)
    fs = font(17)
    for lbl, (bx0, by0, bx1, by1), what in boxes:
        r = [(bx0 - x0) * zoom, (by0 - y0) * zoom,
             (bx1 - x0) * zoom, (by1 - y0) * zoom]
        d.rectangle(r, outline=(255, 45, 45), width=4)
        txt = "%s  (%d,%d)-(%d,%d)" % (lbl, bx0, by0, bx1, by1)
        w = int(d.textlength(txt, font=fs)) + 12
        ty = max(0, r[1] - 25)
        d.rectangle([r[0], ty, r[0] + w, ty + 24], fill=(255, 45, 45))
        d.text((r[0] + 6, ty + 3), txt, fill=(255, 255, 255), font=fs)
    band = Image.new("RGB", (c.width, 78), (16, 16, 16))
    bd = ImageDraw.Draw(band)
    bd.text((12, 8), title, fill=(255, 255, 255), font=font(23))
    bd.text((12, 38), sub, fill=(175, 175, 175), font=fs)
    bd.text((12, 57), "ref_workshop.jpg   view (%d,%d)-(%d,%d)   zoom x%d"
            % (x0, y0, x1, y1, zoom), fill=(130, 130, 130), font=font(15,
                                                                     False))
    out = Image.new("RGB", (c.width, c.height + 78), (16, 16, 16))
    out.paste(band, (0, 0))
    out.paste(c, (0, 78))
    return out


def main():
    im = Image.open(SRC).convert("RGB")
    print("source %s  %dx%d" % (SRC, im.width, im.height))
    p1 = panel(im, Q1_VIEW, Q1_BOXES,
               "Q1  -  looking THROUGH the near-side openings",
               "In each box: is there a FAR-SIDE OPENING, or panel/interior?",
               6)
    p2 = panel(im, Q2_VIEW, Q2_BOXES,
               "Q2  -  the cab door glass, forward end",
               "Is the door glass DIVIDED into a small vent + a main pane?", 9)
    W = max(p1.width, p2.width)
    fig = Image.new("RGB", (W, p1.height + p2.height + 14), (16, 16, 16))
    fig.paste(p1, ((W - p1.width) // 2, 0))
    fig.paste(p2, ((W - p2.width) // 2, p1.height + 14))
    fig.save("/tmp/rev23_questions.png")
    print("wrote /tmp/rev23_questions.png  %dx%d" % (fig.width, fig.height))
    print()
    print("EVERY BOX, PRINTED (pixel coords in ref_workshop.jpg, 1200x824):")
    for lbl, b, what in Q1_BOXES + Q2_BOXES:
        print("  %s  (%4d,%4d)-(%4d,%4d)   %s"
              % (lbl, b[0], b[1], b[2], b[3], what))


if __name__ == "__main__":
    main()
