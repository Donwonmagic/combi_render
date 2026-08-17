#!/usr/bin/env python3
"""
mark_rev35_bound.py  --  rev 35.  READ-ONLY.  Writes rev35_bound.png.

THIS FIGURE IS NOT A QUESTION.  NO ANSWER IS SOUGHT AND NONE SHOULD BE GIVEN.
It is a RESULT figure: it shows, on the photograph, the four columns behind
probe_rev35_harmonic.py's camera-free bound, so the claim can be checked by
eye against the frame it was read from.

That makes it a FIFTH mark class in this project, and the class is named on
the figure itself, as rev 30 through rev 34 each named theirs:

    rev 30   SAMPLING WINDOWS   -- numbers were taken from inside them
    rev 31   POINTERS           -- no number taken; they only point
    rev 32-34 CANDIDATE LINES   -- a set to choose from
    rev 34   ORDERING WALL      -- a hard bound, explicitly not a choice
    rev 35   MEASURED COLUMNS + ONE DERIVED MEAN   -- nothing to choose.
             Three are readings already in the record; the fourth is
             arithmetic on two of them and marks no feature at all.

THE RIGHT-HAND PANEL IS A DIFFERENT CAMERA.  It is the current build, shown
so the bar and the missing post can be seen on the model beside the frame.
NO COLUMN CORRESPONDENCE BETWEEN THE PANELS IS IMPLIED OR DRAWN.

CONTROLS -- the figure REFUSES TO WRITE if any fails (SPEC 10.87.4's rule,
kept by both rev-34 figures):
  C1  the drawn mid-column is RE-DERIVED here, not copied from the probe
  C2  the drawn post column lies inside its published extent 355.0-376.0
  C3  the ordering far < mid < post < near holds as drawn
  C4  every string that will be drawn is MEASURED before the canvas is sized
      (SPEC 10.88.5: rev 34's Q1 figure clipped its header because the canvas
      was sized off one text block while three were drawn)
"""

import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except Exception as e:                                    # pragma: no cover
    print("mark_rev35_bound: needs pillow:", e)
    sys.exit(2)

REF = "ref_workshop.jpg"
RENDER = os.environ.get("T1_PREVIEW_PNG", "/tmp/prev/pv_hero34f.png")
OUT = "rev35_bound.png"

CROP = (180, 615, 525, 745)          # PRINTED on the figure and on stdout
Z = 3                                # integer zoom, NEAREST, so no resampling
                                     # can move an edge

U_BAR_FAR = 205.0     # OWNER-ANSWERED twice (SPEC 10.87.5, 10.88.3)
U_BAR_NEAR = 485.0    # SPEC 10.86 C3, 0.0 px over five thresholds
U_POST = 365.5        # SPEC 10.86 C3, extent 355.0-376.0, centre 365.5
POST_LO, POST_HI = 355.0, 376.0


def font(sz):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, sz)
            except Exception:
                pass
    return ImageFont.load_default()


def main():
    fails = []

    # ---------------------------------------------------------- C1, C2, C3
    u_mid = 0.5 * (U_BAR_FAR + U_BAR_NEAR)          # RE-DERIVED HERE
    print("C1  mid-column re-derived here: (%.1f + %.1f)/2 = %.1f"
          % (U_BAR_FAR, U_BAR_NEAR, u_mid))
    if abs(u_mid - 345.0) > 1e-9:
        fails.append("C1 mid-column re-derivation disagrees with 345.0")

    print("C2  post column %.1f inside its published extent [%.1f, %.1f]: %s"
          % (U_POST, POST_LO, POST_HI,
             "yes" if POST_LO <= U_POST <= POST_HI else "NO"))
    if not (POST_LO <= U_POST <= POST_HI):
        fails.append("C2 post column outside its published extent")

    order = U_BAR_FAR < u_mid < U_POST < U_BAR_NEAR
    print("C3  ordering %.1f < %.1f < %.1f < %.1f : %s"
          % (U_BAR_FAR, u_mid, U_POST, U_BAR_NEAR, "holds" if order else "BROKEN"))
    if not order:
        fails.append("C3 ordering broken")

    for p in (REF, RENDER):
        if not os.path.exists(p):
            fails.append("missing input %s" % p)
    if fails:
        print()
        print("*** REFUSING TO WRITE: %s" % "; ".join(fails))
        return 1

    # --------------------------------------------------------------- build
    ref = Image.open(REF).convert("RGB")
    left = ref.crop(CROP).resize(((CROP[2] - CROP[0]) * Z,
                                  (CROP[3] - CROP[1]) * Z), Image.NEAREST)
    LW, LH = left.size

    ren = Image.open(RENDER).convert("RGB")
    RH = LH
    RW = int(ren.width * RH / ren.height)
    right = ren.resize((RW, RH), Image.LANCZOS)

    f_hd, f_bd, f_sm = font(26), font(17), font(14)

    head = ("rev 35 -- THE SIGN OF THE OVER-RIDER POST'S OFFSET. "
            "NOT A QUESTION.")
    sub = ("Marks are MEASURED COLUMNS plus ONE DERIVED MEAN. Nothing here is "
           "a candidate, a pointer, a sampling window or a wall.  "
           "SUPERSEDES the first issue of this figure.")
    body = [
        "photograph  ref_workshop.jpg   CROP BOX (u0,v0,u1,v1) = %s   zoom x%d NEAREST"
        % (str(CROP), Z),
        "",
        "  A  u %.1f   BAR, FAR END        OWNER-ANSWERED TWICE, interval closed on both sides: u in (205, 208]"
        % U_BAR_FAR,
        "  M  u %.1f   BAR, MID-COLUMN     DERIVED, NOT A FEATURE: the arithmetic mean (%.1f + %.1f)/2. Nothing stands here."
        % (u_mid, U_BAR_FAR, U_BAR_NEAR),
        "  P  u %.1f   THE POST            MEASURED, SPEC 10.86 C3: extent %.1f-%.1f, right edge moving 0.5 px over five thresholds"
        % (U_POST, POST_LO, POST_HI),
        "  B  u %.1f   BAR, NEAR END       MEASURED, SPEC 10.86 C3: 0.0 px over five thresholds"
        % U_BAR_NEAR,
        "",
        "THE ARITHMETIC, PRINTED SO IT CAN BE CHECKED:",
        "  P - M = %.1f - %.1f = %+.1f px.  The post lies RIGHT of the bar's mid-column."
        % (U_POST, u_mid, U_POST - u_mid),
        "  Under perspective the image of the bar's 3-D MIDPOINT lies at or LEFT of M (it equals M only in the",
        "  orthographic limit), because the far end recedes -- SPEC 10.86 C4 fixes the near end as the high-u end.",
        "  Therefore the post is on the NEAR side of the bar's 3-D midpoint.  THE SIGN, AND ONLY THE SIGN.",
        "",
        "MAGNITUDES WITHDRAWN.  rev 35 first published t >= 0.1464 (nominal) and t >= 0.0595 (worst corner) as",
        "holding 'for every admissible camera'.  ITS OWN ADVERSARIAL AUDIT REFUTED THAT, and the figures are",
        "STRUCK rather than quietly re-scoped.  Two preconditions the cross-ratio needs were never checked:",
        "  (a) COLLINEARITY.  u 485 is the HOOP's outer column; t1_detail.py's arc puts the point that generates",
        "      it 53.7 mm below and 17.5 mm behind the far reading's line.  The post's column was read on rows",
        "      676-700 while the bar's top edge is v 672.5.  FOUR POINTS, THREE LINES.",
        "  (b) ZERO CAMERA ROLL and ZERO POST STANDOFF -- neither established anywhere in the repository.",
        "The SIGN survives to |roll| ~ 26 deg and ~139 mm of rearward standoff, both excluded on this frame.",
        "",
        "WHAT IT DOES NOT SAY:  where the vehicle's CENTRELINE is.  'At the bar's midpoint' and 'at the vehicle's",
        "centreline' are the same statement only if the bar is symmetric about the centreline -- SPEC 10.86 records",
        "that assumption's only check DISAGREEING AT 17 %, and BAR_HALF_Y is graded E, 'not measured'.",
        "",
        "right panel: the current build, T1_SUB=1 T1_SAMP=24, 900x600.  A DIFFERENT CAMERA.  No column",
        "correspondence between the panels is implied or drawn.  The post is absent because it is not built.",
    ]

    # ------------------------------------------------------------------ C4
    probe = Image.new("RGB", (10, 10))
    dp = ImageDraw.Draw(probe)
    need_w = 0
    for s, ft in ([(head, f_hd), (sub, f_bd)] + [(b, f_sm) for b in body]):
        if s:
            need_w = max(need_w, dp.textbbox((0, 0), s, font=ft)[2])
    PAD = 18
    W = max(LW + RW + PAD * 3, int(need_w) + PAD * 2)
    text_h = 44 + 30 + sum(20 for _ in body) + 20
    H = 44 + 30 + LH + PAD * 2 + text_h
    print("C4  widest drawn string %d px; canvas sized to %d px (panels need %d)"
          % (need_w, W, LW + RW + PAD * 3))
    if W < need_w + PAD * 2:
        print("*** REFUSING TO WRITE: C4 canvas narrower than a drawn string")
        return 1

    im = Image.new("RGB", (W, H), (250, 250, 248))
    d = ImageDraw.Draw(im)
    d.text((PAD, 12), head, font=f_hd, fill=(140, 0, 0))
    d.text((PAD, 46), sub, font=f_bd, fill=(0, 0, 0))

    y0 = 78
    im.paste(left, (PAD, y0))
    im.paste(right, (PAD * 2 + LW, y0))
    d.rectangle([PAD - 1, y0 - 1, PAD + LW, y0 + LH], outline=(0, 0, 0))
    d.rectangle([PAD * 2 + LW - 1, y0 - 1, PAD * 2 + LW + RW, y0 + LH],
                outline=(0, 0, 0))

    marks = [("A", U_BAR_FAR, (0, 90, 220)),
             ("M", u_mid, (200, 120, 0)),
             ("P", U_POST, (200, 0, 0)),
             ("B", U_BAR_NEAR, (0, 90, 220))]
    for tag, u, col in marks:
        x = PAD + int(round((u - CROP[0]) * Z))
        dash = (tag == "M")
        yy = y0
        while yy < y0 + LH:
            seg = 7 if dash else LH
            d.line([(x, yy), (x, min(yy + seg, y0 + LH))], fill=col, width=2)
            yy += seg * 2 if dash else LH
        bb = d.textbbox((0, 0), tag, font=f_bd)
        d.rectangle([x - 9, y0 + LH + 2, x + 9, y0 + LH + 6 + bb[3]],
                    fill=(255, 255, 255), outline=col)
        d.text((x - bb[2] // 2, y0 + LH + 4), tag, font=f_bd, fill=col)

    ty = y0 + LH + 30
    d.text((PAD, ty), body[0], font=f_sm, fill=(60, 60, 60))
    ty += 24
    for b in body[1:]:
        colr = (0, 0, 0)
        if b.startswith("THE ARITHMETIC") or b.startswith("WHAT IT DOES NOT"):
            colr = (140, 0, 0)
        elif b.strip().startswith("t >="):
            colr = (0, 100, 0)
        d.text((PAD, ty), b, font=f_sm, fill=colr)
        ty += 20

    im.save(OUT)
    print()
    print("wrote %s  (%d x %d)" % (OUT, W, H))
    print("CROP BOX: %s   zoom x%d NEAREST" % (str(CROP), Z))
    return 0


if __name__ == "__main__":
    sys.exit(main())
