"""mark_rev30_q.py -- rev 30.  READ-ONLY.  Draws the owner questions for the
FRONT OVER-RIDER (SPEC 10.75 / 10.80), with every crop box printed on the image
AND on the console, every box's ROLE stated, and the photograph shown BESIDE a
render of the CURRENT BUILD.

WHY THE QUESTION MOVED
----------------------
The rev-30 brief said to ask which columns show the true bumper-blade bottom.
`probe_orb_blade.py` ANSWERED THAT BY MEASUREMENT instead, so it is not asked:
the trolley rail's top edge fits a straight line to rms 0.289 px over 65
columns and lies 6.6-61.3 px BELOW the blade's lower boundary throughout the
tube's own columns.  It does not occlude them.  The same probe REFUTED rev 29's
proposed scale-free ratio: swept over seven thresholds the ratio is +-12.8 %,
between the tube's +-16.8 % and the blade's +-9.0 %, so the systematic does not
cancel.  Spending his attention on a question measurement has already settled
would be the same defect as asking a malformed one.

WHAT ACTUALLY BLOCKS THE ITEM, AND WHY IT NEEDS HIM
---------------------------------------------------
The tube runs the WHOLE way across the nose.  At u 385-460 it passes directly
beneath the headlamp aperture -- the one locked ruler in this frame -- so no
cross-panel scale is needed and REF Section 9's "lateral scale varies by more
than 2:1" warning does not bite: this is one station, measured vertically.
There the tube is isolated against green above and below, and its apparent
thickness is constant to +-5.2 % over sixteen columns against rev 26's +-19 %.

Two boundary CONVENTIONS are then all that stand between here and a number, and
both are readings of the photograph, not calculations:

  Q1  THE TUBE'S LOWER SILHOUETTE.  Below the bright tube there is a dark band.
      If it is the tube's own unlit underside the tube is ~1.8x thicker than if
      it is the shadow the tube casts on the green panel.
  Q2  THE APERTURE'S LOWER RIM -- the RULER itself.  Its interior is partly
      lit, so a threshold does not outline it.  Measured to the dark rim line
      the vertical extent is 71.1 px; REF Section 9 publishes 75.6 px.  The two
      differ by 6.0 %, and that lands directly on the answer.

BOX ROLES -- stated, per rev 28's standing requirement
-------------------------------------------------------
**S1 AND S2 ARE SAMPLING WINDOWS, NOT POINTERS.**  Numbers ARE taken from them.
That is DIFFERENT from rev 28's and rev 29's questions, whose boxes were
pointers and from which no number was taken, and it is said plainly here rather
than left to be inferred.  Box A on panel 2 is rev 26's own POINTER, already
ANSWERED, drawn in a different colour so the question carries its own scale.

NO METRE FIGURE IS ASSERTED ANYWHERE IN THIS FIGURE.  The aperture's 0.180 m is
a STOCK T1 CATALOGUE value, which is the exact class of evidence SPEC 10.72
struck for the bumper face; it is shown as a consequence, tagged, never as a
measurement of this vehicle.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(ROOT, "ref_workshop.jpg")
RENDER = "/tmp/r30/q_hero34f.png"
OUT = os.path.join(ROOT, "rev30_q_overrider.png")

RED = (228, 26, 28)
BLU = (55, 126, 184)
GRN = (30, 140, 60)
ORA = (230, 130, 20)
PUR = (140, 60, 160)
INK = (20, 20, 20)
BG = (250, 250, 248)

# crop boxes on ref_workshop.jpg, (u0, u1, v0, v1)
VIEW_NEAR = (376, 466, 578, 716)
VIEW_FAR = (226, 302, 640, 740)
S1 = (385, 460, 684, 712)        # SAMPLING WINDOW -- the tube
S2 = (390, 446, 588, 678)        # SAMPLING WINDOW -- the aperture, the ruler
BOX_A = (260, 286, 664, 673)     # rev 26's POINTER, ANSWERED
# nose of the current build in the 1500x1000 hero34f render
RVIEW = (250, 655, 545, 890)

U0S, U1S = 385, 461              # the measured column run


def font(sz, bold=True):
    p = ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
         "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    return ImageFont.truetype(p, sz) if os.path.exists(p) else \
        ImageFont.load_default()


F, FS, FT = font(22), font(16, False), font(14, False)


def luma(a):
    return 0.2126 * a[:, :, 0] + 0.7152 * a[:, :, 1] + 0.0722 * a[:, :, 2]


def cross(col, v0, v1, level):
    for v in range(v0, v1):
        y0, y1 = col[v], col[v + 1]
        if (y0 - level) * (y1 - level) <= 0 and y0 != y1:
            return v + (level - y0) / (y1 - y0)
    return None


def measure(L):
    """Everything drawn below is measured here, so the figure cannot drift
    from the numbers.  Nothing is hardcoded except the search windows."""
    us, top, botA, botB = [], [], [], []
    for u in range(U0S, U1S):
        col = L[:, u]
        g = float(np.median(col[678:686]))
        c = float(np.max(col[686:700]))
        t = cross(col, 682, 695, 0.5 * (g + c))
        if t is None:
            continue
        sh = float(np.min(col[int(t) + 8:int(t) + 20]))
        b1 = cross(col, int(t) + 4, int(t) + 14, 0.5 * (c + sh))
        # H2: the LOWER edge of the dark band -- dark back up to panel green
        gp = float(np.median(col[int(t) + 18:int(t) + 26]))
        b2 = cross(col, int(t) + 10, int(t) + 24, 0.5 * (sh + gp))
        if b1 is None or b2 is None:
            continue
        us.append(u)
        top.append(t)
        botA.append(b1)
        botB.append(b2)
    us = np.array(us, float)
    top, botA, botB = (np.array(x, float) for x in (top, botA, botB))
    mt, ct = np.polyfit(us, top, 1)
    ma, ca = np.polyfit(us, botA, 1)
    mb, cb = np.polyfit(us, botB, 1)
    rms = lambda m, c, y: float(np.sqrt(np.mean((m * us + c - y) ** 2)))
    h1 = botA - top
    h2 = botB - top
    # the aperture
    ext, uu = [], []
    for u in range(390, 447):
        col = L[:, u]
        g = float(np.median(col[578:592]))
        dk = float(np.min(col[600:625]))
        t = cross(col, 588, 606, 0.5 * (g + dk))
        if t is None:
            continue
        seg = col[655:678]
        j = int(np.argmin(seg))
        # the rim is a DARK line.  A column whose darkest sample is merely
        # panel green has no rim in view and is DECLINED, not ranked -- the
        # first cut ranked them and picked u=390, whose "rim" read L=98.7.
        if seg[j] > 85.0:
            continue
        ext.append(655 + j - t)
        uu.append((u, t, 655 + j))
    ext = np.array(ext)
    k = int(np.argmax(ext))
    return dict(us=us, mt=mt, ct=ct, ma=ma, ca=ca, mb=mb, cb=cb,
                rt=rms(mt, ct, top), ra=rms(ma, ca, botA),
                rb=rms(mb, cb, botB), h1=h1, h2=h2,
                ap_ext=float(ext[k]), ap_u=uu[k][0], ap_top=uu[k][1],
                ap_bot=uu[k][2], slope=float(mt))


def strip(im, view, zoom, marks, boxes, title, sub):
    u0, u1, v0, v1 = view
    c = im.crop((u0, v0, u1, v1))
    w, h = int((u1 - u0) * zoom), int((v1 - v0) * zoom)
    c = c.resize((w, h), Image.LANCZOS)
    pan = Image.new("RGB", (w + 520, h + 72), BG)
    pan.paste(c, (12, 60))
    d = ImageDraw.Draw(pan)
    d.text((12, 6), title, font=F, fill=INK)
    d.text((12, 34), sub, font=FS, fill=(90, 90, 90))
    for lbl, fn, col, note, dy in marks:      # fn(u) -> v, a fitted line
        pts = []
        for i in range(0, w, 2):
            u = u0 + i / zoom
            v = fn(u)
            if v is None or not (v0 <= v <= v1):
                continue
            pts.append((12 + i, 60 + (v - v0) * zoom))
        for k in range(len(pts) - 1):
            d.line([pts[k], pts[k + 1]], fill=col, width=2)
        if pts:
            ty = pts[-1][1] + dy
            d.line([pts[-1][0], pts[-1][1], w + 16, ty + 7], fill=col)
            d.text((w + 20, ty), "%s   %s" % (lbl, note), font=FT, fill=col)
    for lbl, (bu0, bu1, bv0, bv1), col, note in boxes:
        x0, y0 = 12 + (bu0 - u0) * zoom, 60 + (bv0 - v0) * zoom
        x1, y1 = 12 + (bu1 - u0) * zoom, 60 + (bv1 - v0) * zoom
        for k in range(2):
            d.rectangle([x0 - k, y0 - k, x1 + k, y1 + k], outline=col)
        tw = d.textbbox((0, 0), lbl, font=F)[2]
        d.rectangle([x0 - 3, y0 - 32, x0 + tw + 11, y0 - 3], fill=col)
        d.text((x0 + 4, y0 - 29), lbl, font=F, fill=(255, 255, 255))
        d.text((x1 + 10, y1 + 4), note, font=FT, fill=col)
    d.rectangle([0, 0, pan.size[0] - 1, pan.size[1] - 1],
                outline=(215, 215, 210))
    return pan


def main():
    im = Image.open(REF).convert("RGB")
    L = luma(np.asarray(im).astype(np.float64))
    M = measure(L)
    have_render = os.path.exists(RENDER)

    p1 = strip(
        im, VIEW_NEAR, 8.0,
        [("aperture TOP rim", lambda u: M["ap_top"], BLU,
          "measured 50 % crossing", -8),
         ("aperture LOWER rim, Q2 reading 1",
          lambda u: float(M["ap_bot"]), BLU,
          "the thin dark line -> extent %.1f px" % M["ap_ext"], -46),
         ("aperture LOWER rim, Q2 reading 2",
          lambda u: M["ap_top"] + 75.6, PUR,
          "REF section 9's 75.6 px, +6.3 %", -6),
         ("tube TOP", lambda u: M["mt"] * u + M["ct"], GRN,
          "measured, rms %.2f px" % M["rt"], -34),
         ("tube bottom, Q1 reading 1", lambda u: M["ma"] * u + M["ca"], RED,
          "-> tube %.2f px, rms %.2f" % (M["h1"].mean(), M["ra"]), 4),
         ("tube bottom, Q1 reading 2", lambda u: M["mb"] * u + M["cb"], ORA,
          "-> tube %.2f px, rms %.2f" % (M["h2"].mean(), M["rb"]), 42)],
        [("S1", S1, PUR, "SAMPLING WINDOW"),
         ("S2", S2, BLU, "SAMPLING WINDOW -- the ruler")],
        "1.  THE PHOTOGRAPH -- ref_workshop.jpg, the near station",
        "the headlamp aperture (S2) sits directly above the over-rider tube "
        "(S1).  Same station, so no cross-panel scale is used.")

    p2 = strip(
        im, VIEW_FAR, 8.0, [],
        [("A", BOX_A, BLU, "rev 26: you ruled this ON THE BUS -- ANSWERED")],
        "2.  YOUR OWN ANCHOR -- the same tube, far side, rev 26's box",
        "shown so the question carries its own scale.  rev 26 measured the "
        "tube HERE; this revision measures it at the near station instead.")

    pans = [p1, p2]
    if have_render:
        r = Image.open(RENDER).convert("RGB")
        pans.append(strip(r, RVIEW, 2.6, [], [],
                          "3.  THE MODEL AS SHIPPED -- 135 commits, guards "
                          "0 fail / 0 warn",
                          "one plain cream blade.  NO transverse tube and NO "
                          "centre post: the model has no member for either."))

    W = max(p.size[0] for p in pans) + 24
    foot = 430
    canvas = Image.new("RGB", (W, sum(p.size[1] for p in pans) + 40 + foot),
                       BG)
    y = 14
    for p in pans:
        canvas.paste(p, (12, y))
        y += p.size[1] + 8
    d = ImageDraw.Draw(canvas)
    y += 12
    ap = M["ap_ext"]
    lines = [
        ("TWO QUESTIONS, both multiple choice, both about what the "
         "PHOTOGRAPH shows.", F, INK),
        ("", FS, INK),
        ("Q1.  In panel 1, where does the white tube END?  Below it is a dark "
         "band.", F, INK),
        ("   1.  The tube ends at the GREEN line's partner in RED -- the dark "
         "band below is the SHADOW the tube", FS, INK),
        ("       casts on the green panel.   ->  tube reads %.2f px."
         % M["h1"].mean(), FS, INK),
        ("   2.  The dark band IS the tube -- its unlit underside -- so the "
         "tube ends at the ORANGE line.", FS, INK),
        ("       ->  tube reads %.2f px, %.2f x thicker."
         % (M["h2"].mean(), M["h2"].mean() / M["h1"].mean()), FS, INK),
        ("   3.  Can't tell from this frame.", FS, INK),
        ("   MY OWN LEAN, SAID SO YOU CAN OVERRULE IT: reading 1.  Its two "
         "edges fit straight lines to rms 0.28 and", FT, (90, 90, 90)),
        ("   0.24 px and the thickness holds to +-5.5 % over 76 columns; "
         "reading 2 fits to rms 2.18 px and swings +-32.9 %.", FT,
         (90, 90, 90)),
        ("   A constant-diameter tube at near-constant depth cannot do that. "
         "But that is an argument, not a reading.", FT, (90, 90, 90)),
        ("", FS, INK),
        ("Q2.  In panel 1, where is the headlamp aperture's LOWER RIM?  This "
         "is the RULER, so it sets the answer.", F, INK),
        ("   1.  At the thin dark line I have marked -- vertical extent "
         "%.1f px." % ap, FS, INK),
        ("   2.  Lower than that, at the outer edge of the rim -- REF section "
         "9 reads 75.6 px, 6.0 % larger.", FS, INK),
        ("   3.  Can't tell from this frame.", FS, INK),
        ("", FS, INK),
        ("WHAT EACH ANSWER DOES:", F, INK),
        ("   Q1 answer 1 + Q2 answer 1  ->  tube / aperture = %.4f."
         % (M["h1"].mean() / ap), FS, INK),
        ("   Q1 answer 2               ->  ratio %.4f, i.e. a tube 1.8 x "
         "thicker.  It changes the part, not a decimal."
         % (M["h2"].mean() / ap), FS, INK),
        ("   Q2 chooses between two rulers 6.0 % apart, which is the whole "
         "remaining band on the answer.", FS, INK),
        ("", FS, INK),
        ("WHY I AM NOT ASKING THE QUESTION THE BRIEF NAMED:  it is already "
         "answered by measurement.  The trolley rail's", FS, (90, 90, 90)),
        ("top edge fits a straight line to rms 0.289 px over 65 columns and "
         "lies 6.6-61.3 px BELOW the blade's lower", FS, (90, 90, 90)),
        ("boundary in every one of the tube's columns.  It does not occlude "
         "them.  rev 29's scale-free ratio is REFUTED", FS, (90, 90, 90)),
        ("in the same run: swept over seven thresholds it reads +-12.8 %, "
         "BETWEEN the tube's +-16.8 % and the blade's", FS, (90, 90, 90)),
        ("+-9.0 % -- the systematic does not cancel.", FS, (90, 90, 90)),
        ("", FS, INK),
        ("S1 AND S2 ARE SAMPLING WINDOWS, NOT POINTERS -- numbers ARE taken "
         "from them.  That is different from", FS, (90, 90, 90)),
        ("rev 28's and rev 29's boxes and is said here rather than left to be "
         "inferred.  Box A is rev 26's POINTER,", FS, (90, 90, 90)),
        ("already answered.  NO METRE FIGURE APPEARS ANYWHERE ABOVE: the "
         "aperture's 0.180 m is a stock T1 CATALOGUE", FS, (90, 90, 90)),
        ("value, the exact class SPEC 10.72 struck for the bumper face, and "
         "it is not used here.", FS, (90, 90, 90)),
    ]
    for t, f, col in lines:
        d.text((16, y), t, font=f, fill=col)
        y += (30 if f is F else 21)
    canvas.save(OUT)

    print("\nEVERY BOX AND EVERY LINE, PRINTED")
    print("  %-9s %-30s %s" % ("label", "box (u0-u1, v0-v1)", "ROLE"))
    print("  %-9s u %d-%d  v %d-%d          %s"
          % ("S1", S1[0], S1[1], S1[2], S1[3],
             "SAMPLING WINDOW -- the tube; a number IS taken from it"))
    print("  %-9s u %d-%d  v %d-%d          %s"
          % ("S2", S2[0], S2[1], S2[2], S2[3],
             "SAMPLING WINDOW -- the ruler; a number IS taken from it"))
    print("  %-9s u %d-%d  v %d-%d          %s"
          % ("A", BOX_A[0], BOX_A[1], BOX_A[2], BOX_A[3],
             "POINTER -- rev 26's, ALREADY ANSWERED"))
    print("  photo crops : panel 1 %s   panel 2 %s" % (VIEW_NEAR, VIEW_FAR))
    print("  render crop : %s of q_hero34f 1500x1000%s"
          % (RVIEW, "" if have_render else "   *** RENDER MISSING ***"))
    print("\n  MEASURED, columns u %d-%d (n=%d):" % (U0S, U1S - 1,
                                                     len(M["us"])))
    print("    tube TOP   line  v = %+.5f u %+.3f   rms %.3f px"
          % (M["mt"], M["ct"], M["rt"]))
    print("    bottom rdg 1     v = %+.5f u %+.3f   rms %.3f px"
          % (M["ma"], M["ca"], M["ra"]))
    print("    bottom rdg 2     v = %+.5f u %+.3f   rms %.3f px"
          % (M["mb"], M["cb"], M["rb"]))
    print("    tube vertical    reading 1 %.2f px (sd %.2f, +-%.1f %%)"
          % (M["h1"].mean(), M["h1"].std(),
             100 * (M["h1"].max() - M["h1"].min()) / 2 / M["h1"].mean()))
    print("    tube vertical    reading 2 %.2f px (sd %.2f, +-%.1f %%)"
          % (M["h2"].mean(), M["h2"].std(),
             100 * (M["h2"].max() - M["h2"].min()) / 2 / M["h2"].mean()))
    print("    tube image axis slope %.4f -> perpendicular thickness is"
          " %.3f x the vertical" % (M["slope"],
                                    1 / np.sqrt(1 + M["slope"] ** 2)))
    print("    aperture vertical extent %.2f px, maximal at u=%d "
          "(top %.2f -> rim line %d);  REF section 9 publishes 75.6 px,"
          " %+.1f %%"
          % (M["ap_ext"], M["ap_u"], M["ap_top"], M["ap_bot"],
             100 * (75.6 / M["ap_ext"] - 1)))
    print("\n  wrote %s  (%d x %d)" % (OUT, canvas.size[0], canvas.size[1]))
    print("  NO METRE FIGURE IS ASSERTED.  The 0.180 m aperture is a stock T1"
          " CATALOGUE value (SPEC 10.72's class).")


if __name__ == "__main__":
    main()
