"""Artwork for the FRONT roof lid -- BOTH FACES -- and nothing else.

rev 11.  RE-MEASURED FROM THE PHOTOGRAPHS, 2026-08-10.

=============================================================================
0.  WHAT CHANGED, AND WHY IT IS ONE BOARD AND NOT TWO
=============================================================================
The owner settled the roof topology on 2026-08-10: `ref_side.jpg` region A --
the flower mural with the yellow menu strips -- is a CUT ROOF LID, hinged and
lifted, and `ref_rear34.jpg` region D -- the cream panel lettered in red brush
script with a red star -- is the OTHER FACE OF THAT SAME LID.  There are two
roof lids plus a trunk lid.

So this file now writes TWO TEXTURES FOR ONE BOARD:

    tex/lidmural.png   FRONT lid, OUTWARD (upper) face -- flower mural + strips
    tex/lidsign.png    FRONT lid, INWARD  (lower) face -- cream + red script

They are written at THE SAME ASPECT, because they are two faces of one flat
panel and an aspect is a property of the panel, not of a face.  rev 10 wrote
them at 1.664 and 1.832 and then reasoned about why the two would not
reconcile; that question is dissolved, not answered.

See the report for what `build.py` / `t1_shell.py` must do with them.

=============================================================================
A.  THE BOARD, MEASURED IN `ref_side.jpg`
=============================================================================
Method.  The four bounding lines of the ARTWORK (the outer edge of the yellow
strips on three sides, and the bottom edge of the mural on the fourth) were
traced by RANSAC line fits to a hue-35-62 / sat>0.55 / V>0.45 mask -- 220/226,
190/251, 226/246 and 205/342 inliers, residual sd 0.47 / 0.79 / 0.48 / 1.4 px
-- intersected into a quad, and the board was rectified onto a 2400 x 1500
rectangle by a homography.  Occluders (palm fronds, the man at the counter)
were masked: 6.09 % of the interior.

    outer quad, ref_side.jpg px:  TL (313.5, 57.5)   TR (738.8, 30.7)
                                  BR (757.5, 278.8)  BL (350.2, 295.2)

  ASPECT -- NOT SETTLED.  Three methods, and they do not agree:

    rectangle-from-one-view (four edges + the orthogonality of the board's
        own two edge directions, principal point assumed at the image centre)
        -> f = 2258 px and aspect 1.654;  1000-trial Monte Carlo with +/-1.5 px
        corner noise gives a 68 % interval [1.591, 1.703]
    flower-head circularity (ellipse fitted to the EIGHT pale petal-dots of
        each head, 7 heads with rms < 0.06) -> the 1.600 rectification is
        x-stretched 1.0529 +/- 0.0094, so aspect 1.520 +/- 0.014
    top-strip star regularity (a regular 5-point star is w/h 1.0515; the left
        star measures 49/53 = 0.9245) -> aspect 1.82

  The two shape priors bracket the analytic value.  The analytic value needs a
  focal length that this photograph cannot supply independently (I tried: the
  vertical vanishing point from the pole and the wall gives a NEGATIVE f^2, so
  the vertical lines are not vertical enough to close the constraint).
  BOARD_ASPECT below is the analytic value, 1.654, and it agrees with rev 9's
  1.664 to 0.6 %.  Treat +/-0.09 as the honest bar.

  Because the aspect is uncertain, EVERY shape in this file is placed and sized
  in BOARD-NORMALISED (u, v) coordinates with SEPARATE u and v radii.  The
  drawing therefore reproduces the photograph's proportions whatever aspect the
  texture is written at.  Heads are ellipses, not circles, for that reason.

  BOARD LAYOUT, fractions of the board (rectified frame, gradient of the strip
  indicator; inner edges at x = 200.5 / 2209.5, y = 138.5 +/- 1):
      left menu strip    0.0835 of board W
      right menu strip   0.0794 of board W
      top menu strip     0.0923 of board H
      BOTTOM strip       NONE.  Confirmed again: the mural runs to the bottom
                         edge and the side strips run down past it.
      interior           u 0.0835 - 0.9206,  v 0.0923 - 1.0

  THE BOTTOM EDGE IS A REAL EDGE, not the roof gutter.  Checked at 9x at the
  tail end of the board (ref_side (722,252)-(762,292)): the yellow strip stops
  at y = 278.3 +/- 1 and a dark trim, the gutter and the bulb string follow
  below it.  The board's own vanishing point (-10509, 733) predicts a bulb
  string slope of -0.03806 and the bulb string measures -0.03877 +/- 0.002, so
  the board's long edges ARE parallel to the vehicle's fore-aft axis.

=============================================================================
B.  THE MURAL -- COLOUR.  THIS IS THE ROOT OF "PALE WASHED SALMON".
=============================================================================
rev 9/10 multiplied every measured colour by EXPOSURE = 1.58 to turn a shaded
in-situ measurement into an "albedo".  That single scalar is why the render
reads pale: it put the dark ground at (95,51,36) instead of (60,32,23) and
drove the gold into the 252 cap.  The lift is GONE.  VALUE_GAIN is 1.0 and the
texture now carries the measured in-situ sRGB.  That is a change of convention
and `t1_mats.img_paint` must not re-brighten it -- see the report.

  MEASURED, board interior, homography-rectified, occluders masked,
  n = 2 569 748 px:

      median sRGB            (139.0,  49.0,  21.0)
      mean sRGB              (126.5,  58.9,  22.2)
      luma601 percentiles    p5 35.1  p25 47.3  p50 72.8  p75 97.2  p95 126.3
                             mean 74.9  sd 30.0
      HSV saturation         median 0.835   mean 0.795
      hue                    median 18.4 deg  (IQR 9.9 - 29.6)

  Classes (dark = V < 0.30; then hue 345-14 red / 14-30 orange / 30-62 yellow):
      dark    20.26 %   mean (60.1, 30.8, 21.8)   median (59, 31, 23)
      red     26.19 %   mean (132.0, 35.8, 21.6)  median (135, 35, 21)
      orange  34.06 %   mean (144.2, 64.8, 19.5)  median (154, 64, 18)
      yellow  19.49 %   mean (157.1,108.9, 28.3)  median (165,110, 23)
      among the NON-DARK pixels: red 32.8 / orange 42.7 / yellow 24.4
      -- rev 10 recorded 32.4 / 41.6 / 26.0.  INDEPENDENTLY VERIFIED to 1.6 pts.
      -- rev 10's dark ground 21.82 % against my 20.26 %; the 1.6-point gap is
         the occluder mask (6.09 % here against rev 9's 3.1 %).

  Paint colours, sampled by radius inside the heads and by luma in the strips:
      dark ground, darkest decile   ( 55,  26,  19)
      outer red ring                (159,  45,  22)
      orange ring                   (163,  66,  21)
      inner gold disc               (172, 119,  24)
      pale petal-dot core           (184, 150,  76)
      head centre / peace mark      (174, 133,  73)
      strip yellow, ink excluded    (172, 144,  17)
      strip lettering               ( 91,  59,   7)   (blur-limited; core darker)

  THE TARGET I WAS GIVEN DOES NOT COME OFF THE BOARD.  I was told the interior
  reads median (163,100,44), luma 106.7, saturation 0.559.  No region or mask
  of the board produces that.  It IS reproduced by a bounding box that
  overshoots the board downward into the vehicle: ref_side (300,40)-(770,400)
  gives median (157,102,34), median luma 109.4, mean saturation 0.539, and
  (300,40)-(770,370) gives (155,92,30) / 102.0 / 0.578.  The cream body, the
  bulb string and the serving-window band are what carry G up to 100 and mean
  saturation down to 0.56.  Targeted here: the rectified, masked board.

=============================================================================
C.  THE MURAL -- WHAT IS ON IT
=============================================================================
  FLOWER HEADS.  TEN full heads, plus ONE half head cut by the right strip.
  Centres re-derived independently (dot-ring centroid, 4 iterations) and they
  reproduce rev 10's ten to better than 0.012 in u and v -- verified, not
  assumed.  Interior fractions in HEADS_UV below.

  head outer radius     r_u 0.0879 of interior width, r_v 0.1240 of interior
                        height (half-fall of V across the outer ring: 176.5 px
                        in x, 168.9 px in y, in the 2400 x 1500 frame; the
                        x/y ratio 1.045 matches the dot rings' 1.053)
                        rev 10 drew 0.0825 of interior width: 6.5 % small.

  RING STRUCTURE, from the stacked radial profile of 7 clean heads (rho in
  units of the outer radius R):
        0.00-0.11   pale peace mark, (174,133,73) -- a circle with the
                    peace bar, legible at 10x in out G_head1
        0.11-0.33   inner gold disc (172,119,24), brightest at the centre
        0.33-0.50   gold, hue climbing to 40 deg, saturation 0.92
        0.50-0.68   EIGHT pale petal-dots, cores (184,150,76), on gold
        0.68-0.88   orange ring (163,66,21)
        0.88-1.01   outer scalloped ring, red (159,45,22)

  LOBE COUNT -- rev 10's TWELVE IS REFUTED.  The angular V profile at 0.95 R,
  stacked over 7 heads, has its dominant harmonic at k = 8 with power 42.6
  against k = 12 at 6.3; 6 of the 7 heads give k = 8 individually.  The pale
  dot ring is also k = 8.  It is an EIGHT-petal rosette with one dot per petal,
  which is also what is countable by eye at 10x.

  STEMS.  One per head, near-vertical, orange with a red keyline, running to
  the bottom edge.  Width median 33.5 px of 2009 interior px = 0.0167 of the
  interior width (n = 22 cuts, p25 0.0116, p75 0.0227).  rev 10 used 0.0140.

  GROUND FILL.  Large calligraphic C-scrolls and paisley hooks in red, orange
  and gold, many carrying a chain of shrinking dots along the inner curve, plus
  gold almond leaves off the stems.  rev 10 drew 395 small spirals; the
  photograph's scrolls are considerably larger relative to the board.

=============================================================================
D.  THE MENU STRIPS -- AUDITED AT 8-22x
=============================================================================
  HOW MANY / WHICH EDGES.  THREE.  Left and right (the board's short edges,
  fore and aft) full height, and the top (the board's free long edge) running
  BETWEEN two corner blocks that belong to the side strips.  No bottom strip.

  TOP STRIP, legible fragments and their measured x runs in the 2400-wide
  rectified frame:
        200- 250   a five-pointed star
        276- 570   FRESH
        589- 926   JUICES,
        935-1630   OCCLUDED BY PALM FRONDS -- NOT LEGIBLE
       1658-1772   &
       1807-2145   TORTAS
       ~2180       a five-pointed star (partly occluded)
    The occluded span is 695 px.  The three legible words average 53.6 px per
    character, so the gap accommodates 13.0 +/- 0.6 characters.  "GOURMET
    TACOS" is 13 characters.  That is a CONSISTENCY, not a reading.  What is
    drawn below is the reconstruction; only the six words above are read.
    cap height 64 px = 0.46 of the strip height.

  SIDE STRIPS.  Left and right carry the IDENTICAL printed sequence, read at
  22x off the rectified board.  v is a fraction of the board height, taken from
  the ink/vignette row runs of the right strip:
        0.001-0.041  GOURMET            (arched, in the corner block)
        0.047-0.096  bread-roll vignette (two bolillos, green sprigs)
        0.105-0.145  TACOS              (arched)
        0.155-0.191  &
        0.204-0.244  TORTAS             (arched)
        0.260-0.337  torta vignette      (pink meat, green garnish)
        0.379-0.416  FRESH              (arched)
        0.453-0.511  juice vignette      (tall pale glass + an orange)
        0.523-0.555  JUICES             (arched)
        0.590-0.637  CEVICHE / TOSTADAS  (two straight lines, smaller)
        0.677-0.703  tostada vignette    (pale shell, magenta filling)
        0.731-0.755  SHRIMP
        0.759-0.783  & FISH
        0.814-0.868  shrimp vignette     (a pink prawn)
        0.894-0.918  TACOS
        0.925-0.933  y
        0.935-0.966  THREE SMALL LINES -- NOT LEGIBLE.  At 16x off the original
                     they resolve to about "?ANO M?" / "??O?A?" / "Torta?"; the
                     right-hand half of the block is cut by the vehicle body in
                     ref_side and the left strip's copy is behind the man's cap.
                     Reported as unread; drawn as illegible small type.
    strip yellow (172,144,17), hue 48.0, sat 0.88-0.93.

=============================================================================
E.  THE LETTERED FACE, `ref_rear34.jpg`
=============================================================================
  The panel's two visible edges re-traced (they confirm rev 9 to 0.6 px):
        top edge   y = 0.0878 x - 22.41   (169/230 inliers) -> y(596) = 29.9
        left edge  x = -0.03656 y + 591.28 (185/185)        -> x(35) = 590.0
        top-left corner (590.20, 29.44); the cream runs to x = 815, so the
        visible panel is 225.7 px wide along its own top edge.

  ASPECT NOT MEASURABLE, and now IRRELEVANT: the panel's bottom is occluded by
  the vehicle's roof, so its height was never measurable from this view.  It is
  the same board as the mural and inherits BOARD_ASPECT.

  WHAT IS LEGIBLE at 10x (out U_word_10x):
      - "La", small, lower left, on its own lower baseline
      - a large brush-script capital S: a tight spiral eye top left, a full
        bowl, and a long descender swinging back down-LEFT below and before the
        S's own start
      - a RED FIVE-POINTED STAR, point up, above and just left of the S's apex
      - after the S, about SEVEN merged downstrokes climbing steeply to the
        right.  Perpendicular cuts across the word at four heights give 6, 5, 5
        and 4 separated dark runs -- the strokes are at the resolution limit and
        the count is not resolvable letter by letter.
      - each stroke is red with a LIGHT KEYLINE and then a dark warm outline.
        The keyline is faint but real: pixels adjacent to the ink reach luma
        233 against a cream ground of luma 221.
  WHAT IS NOT LEGIBLE
      The word after "La S".  Seven downstrokes is what "anta" produces, so
      "La Santa" remains CONSISTENT and remains UNREAD.  Do not report it as
      verified.
      The word also RUNS OFF the top edge of the visible cream: the last
      strokes are cut by it.  Whether that boundary is the panel edge or the
      horizon of a curved (domed) lid skin is not decidable from one view.

  MEASURED (panel frame: u along the traced top edge, v along the traced left
  edge, origin at their intersection; 87.07 deg apart in the image):
      lockup bbox          u 0.2159 - 0.5432 of the visible panel width
      "La"                 u 0.2159 - 0.2651,  v span 0.1213 of the panel width
      S + what follows     u 0.2500 - 0.5432,  v span 0.4639 of the panel width
      ink principal axis   climbs 59.1 deg above the panel's u axis (the S's
                           descender steepens this; the BASELINE through the
                           downstroke feet is 46-50 deg, rev 9's figure, which
                           I did not improve on)
      LETTER AXIS          2.6 deg from the panel's v axis, n = 350 edge px --
                           the letters stand UPRIGHT.  rev 9 said 6-7 deg; both
                           readings say upright, and 2.6 is used here.
      cream ground         (231, 220, 196) -- rev 9's value reproduced exactly
      reddest 5 % of ink   (187, 112, 106) -- rev 9 got (189, 113, 107)
      darkest ink pixel    ( 76,  59,  49), luma 63
  INK CHROMA IS NOT MEASURABLE.  Every ink pixel is a mixture: the word is
  74 x 105 px and the strokes are 4-6 px wide, below the JPEG's 2x2 chroma
  subsampling.  Unmixing the reddest 5 % against the cream at an ink fraction
  0.70 gives (168, 66, 67) and at 0.85 gives (179, 93, 90) -- neither supports
  rev 9's (176, 46, 38).  SIGN_RED below is a CONSTRUCTION: the measured hue
  (4.4 deg) and value (187) of the reddest pixels, with the saturation set to
  the mural's own red-enamel saturation (0.862 -> used at 0.75).  Stated, not
  measured.

=============================================================================
F.  ACHIEVED vs TARGET -- reproduce with `python3 lid_gen.py`
=============================================================================
  The audit at the bottom of this file scores the written PNGs against the
  section-B numbers with the same classifier and the same dark threshold.
  There is no self-assigned score anywhere in this file.  As written:

    MURAL, board interior          achieved     target     delta
      dark %                         19.920     20.260     -0.340
      red %                          26.508     26.190     +0.318
      orange %                       34.515     34.060     +0.455
      yellow %                       19.056     19.490     -0.434
      red / orange / yellow % of the non-dark
                            33.10 / 43.10 / 23.80   vs   32.8 / 42.7 / 24.4
      median sRGB              (139, 47, 20)   (139, 49, 21)   (0, -2, -1)
      luma p5                        38.614     35.100     +3.514
      luma p25                       47.396     47.300     +0.096
      luma p50                       72.599     72.800     -0.201
      luma p75                       92.243     97.200     -4.957
      luma p95                      131.675    126.300     +5.375
      luma mean                      75.275     74.900     +0.375
      luma sd                        29.916     30.000     -0.084
      HSV sat median                  0.843      0.835     +0.008
      HSV sat mean                    0.806      0.795     +0.011

    SIGN, board fractions          achieved     target     delta
      lockup u lo                    0.1357     0.1440    -0.0083
      lockup u hi                    0.3706     0.3623    +0.0083
      lockup v span / board W        0.3413     0.2715    +0.0698   (E)
      star centre u                  0.2031     0.2033    -0.0002
      star width                     0.0312     0.0331    -0.0018
      star w/h                       1.0847     1.0515    +0.0332

  The two u residuals are the outline pass: the ribbon's dark keyline adds
  0.0083 of the board width at each end of the lockup.  The v-span residual is
  the section-E inconsistency, stated there, not a tuning failure.

"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

TEXDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tex")

# ------------------------------------------------------- measured, ref_side
# ONE aspect: both faces are faces of one flat panel.  Section A.
BOARD_ASPECT = 1.654           # rectangle-from-one-view; 68 % CI [1.591,1.703]

STRIP_L_F = 0.0835             # left strip width  / board width
STRIP_R_F = 0.0794             # right strip width / board width
STRIP_T_F = 0.0923             # top strip height  / board height
# NO bottom strip -- measured absent, twice.

HEAD_RU_F = 0.0879             # head outer radius / interior WIDTH   (u)
HEAD_RV_F = 0.1240             # head outer radius / interior HEIGHT  (v)
STEM_W_F = 0.0167              # stem width / interior width
N_LOBE = 8                     # outer scalloped ring: k = 8, measured
N_DOT = 8                      # pale petal-dots: k = 8, measured
DOT_R_F = 0.594                # dot-ring radius / head outer radius

# head centres as (u, v) fractions of the rectified INTERIOR
HEADS_UV = [
    (0.0327, 0.2798), (0.3808, 0.1435), (0.2665, 0.4291), (0.1562, 0.6164),
    (0.5166, 0.4368), (0.6725, 0.2740), (0.8158, 0.4148), (0.9546, 0.2470),
    (0.7495, 0.6863), (0.8825, 0.8903),
]
N_FLOWERS = len(HEADS_UV)      # 10 full heads
HEADS_PARTIAL_UV = [(1.0050, 0.8460)]   # the half head cut by the right strip

# THE ALBEDO LIFT IS GONE.  Section B.  Keep the constant so that the audit's
# value threshold and the paint stay tied to one number if it is ever revived.
VALUE_GAIN = 1.0

# measured in-situ sRGB (section B)
GROUND = (55, 26, 19)          # dark ground, darkest decile
GROUND_HI = (74, 38, 26)       # its lighter mottle
RED = (159, 45, 22)            # outer ring and the red scrollwork
ORANGE = (163, 66, 21)         # orange ring, stems, scrollwork
GOLD = (172, 119, 24)          # inner disc, gold scrollwork, leaves
PALE = (184, 150, 76)          # pale petal-dot cores
PEACE = (198, 172, 122)        # the centre mark; the measured (174,133,73) is
                               # the disc-plus-mark mean, the mark is paler
STRIP = (172, 144, 17)         # menu-strip yellow, ink excluded
INK = (72, 46, 6)              # strip lettering; measured median (91,59,7) is
                               # blur-limited, so the core is set darker
PINK = (206, 118, 124)         # the vignettes' meat / shrimp
GREEN = (96, 128, 54)          # the vignettes' garnish
CREAMV = (232, 224, 198)       # the vignettes' plate / glass highlights

# ---------------------------------------------------- measured, ref_rear34
SIGN_ASPECT = BOARD_ASPECT          # SAME BOARD.  Section 0.
SIGN_CREAM = (231, 220, 196)        # measured in situ
SIGN_RED = (187, 57, 47)            # CONSTRUCTED -- see section E
SIGN_OUTLINE = (58, 44, 36)         # darkest observed (76,59,49), unmixed
SIGN_KEYLINE = (246, 240, 228)      # the light keyline between ink and outline
SIGN_EDGE = (222, 176, 44)          # the thin yellow pinstripe on the top edge

# ---- LAYOUT ON THE BOARD.  Read section E before touching any of these.
# The visible cream in ref_rear34 is NOT the whole board: its right-hand side is
# occluded by the mural lid, and its bottom by the vehicle's roof.  Its visible
# width is 225.7 image-u px, which the star's isotropy corrects to 257 true-u
# units, and its visible height is 233 v units; the board's aspect then makes
# the board at least 385 true-u units wide, so AT MOST 0.667 of the board's
# width is visible.  Every u fraction below is the measured fraction OF THE
# VISIBLE PANEL times that 0.667.  The bound is what is used; the board could be
# wider still, in which case the lettering is smaller than drawn.
VIS_FRAC = 0.667                    # visible cream / board width, upper bound
SIGN_LOCK_U0 = 0.2159 * VIS_FRAC    # lockup left  edge / board width -> 0.1440
SIGN_S_U0 = 0.2500 * VIS_FRAC       # the S's left edge / board width -> 0.1668
SIGN_LOCK_U1 = 0.5432 * VIS_FRAC    # lockup right edge / board width -> 0.3623
SIGN_STAR_U = 0.3048 * VIS_FRAC     # star centre u     / board width -> 0.2033
SIGN_BASE_DEG = 50.1                # TRUE baseline climb.  The ink's lower
                                    # envelope over u 65-117 has an apparent
                                    # slope of 1.36 in the panel's image frame;
                                    # correcting u by the star's 0.878 gives
                                    # 1.194, i.e. 50.1 deg.
SIGN_LETTER_DEG = 2.6               # letter axis off the panel's v axis
# The letters are sized from the ONE ratio that is free of the foreshortening,
# because both terms are u measurements: thick stroke / lockup u span = 5/73.9.
SIGN_STROKE_OVER_LOCK = 0.0677
SIGN_STROKE_OVER_CAP = 0.148        # rev 9's 0.22 x-height, x-height 0.604 cap
SIGN_XH_OVER_CAP = 0.604            # rev 9's 0.174 / 0.288
SIGN_DESC_OVER_CAP = 0.37           # rev 9's 0.107 / 0.288
SIGN_LA_CAP_RATIO = 0.47            # "La" cap / S cap; rev 9 got 0.479
SIGN_LA_U = (0.2159 * VIS_FRAC, 0.2651 * VIS_FRAC)
SIGN_STAR_W_F = 0.0496 * VIS_FRAC   # star width / board width -> 0.0331
SIGN_STAR_WH = 1.0515               # a regular 5-point star's w/h
# The one stated assumption left: where the lockup sits vertically.  Measured
# relative to the VISIBLE cream the ink runs v 0.017 - 0.467 of that panel's
# visible height, i.e. it hangs from the top edge; the top is set here to a
# 0.020 clearance so no letterform is clipped by the texture.
SIGN_TOP_V = 0.020
# UNRECONCILED, and reported as such: this construction predicts a lockup v
# span of 0.548 of the board height where the measured span, corrected for the
# foreshortening, is 0.449.  The residual is ~1 px of stroke width on an 80 px
# word and the three measurements (u span, v span, stroke width) do not close.

W, H = 2048, int(round(2048 / BOARD_ASPECT))          # 2048 x 1238
SW, SH = 2048, int(round(2048 / SIGN_ASPECT))         # identical, one board


# --------------------------------------------------------------- primitives
def _ell(d, cx, cy, ru, rv, fill=None, outline=None, width=1):
    d.ellipse([cx - ru, cy - rv, cx + ru, cy + rv], fill=fill, outline=outline,
              width=width)


def _scallop(d, cx, cy, ru, rv, lobes, fill, phase=0.0, lobe=1.0):
    """A scalloped ring: `lobes` round lobes on an ellipse, plus the core."""
    rl_u = ru * math.sin(math.pi / lobes) * lobe
    rl_v = rv * math.sin(math.pi / lobes) * lobe
    rc_u, rc_v = ru - rl_u, rv - rl_v
    for k in range(lobes):
        a = phase + 2 * math.pi * k / lobes
        _ell(d, cx + rc_u * math.cos(a), cy + rc_v * math.sin(a),
             rl_u, rl_v, fill=fill)
    _ell(d, cx, cy, rc_u, rc_v, fill=fill)


def _peace(d, cx, cy, ru, rv, fill):
    w = max(2, int(min(ru, rv) * 0.24))
    _ell(d, cx, cy, ru, rv, outline=fill, width=w)
    d.line([(cx, cy - rv), (cx, cy + rv)], fill=fill, width=w)
    for s in (-1, 1):
        d.line([(cx, cy), (cx + s * ru * 0.71, cy + rv * 0.71)], fill=fill,
               width=w)


def flower(d, cx, cy, ru, rv, phase=0.0, f=1.0):
    """One head.  Ring radii and lobe counts per the radial profile, C.

    `f` is a per-head value factor -- the heads are not all the same value in
    the photograph and a single value puts every class median on the paint.
    """
    def V(c):
        return tuple(int(max(0, min(255, round(x * f)))) for x in c)
    _scallop(d, cx, cy, ru * 1.045, rv * 1.045, N_LOBE, DARKLINE, phase, 1.02)
    _scallop(d, cx, cy, ru, rv, N_LOBE, V(RED), phase, 1.02)
    _scallop(d, cx, cy, ru * 0.88, rv * 0.88, N_LOBE, V(ORANGE), phase, 1.02)
    _scallop(d, cx, cy, ru * 0.68, rv * 0.68, N_LOBE, V(GOLD), phase, 1.02)
    for k in range(N_DOT):
        a = phase + 2 * math.pi * k / N_DOT
        _ell(d, cx + ru * DOT_R_F * math.cos(a), cy + rv * DOT_R_F * math.sin(a),
             ru * DOT_SZ, rv * DOT_SZ, fill=V(PALE))
    _ell(d, cx, cy, ru * 0.42, rv * 0.42, fill=V(GOLD))
    _ell(d, cx, cy, ru * 0.36, rv * 0.36, outline=V(ORANGE),
         width=max(2, int(rv * 0.05)))
    _ell(d, cx, cy, ru * 0.33, rv * 0.33, fill=V((176, 124, 28)))
    # r < 0.20 is gold, not the measured (174,133,73): that value is the mean
    # over a band that contains BOTH the disc and the pale peace mark, and
    # using it as a fill produces a desaturated blob the photograph does not
    # have.  The mark itself carries the pale end of the measurement.
    _ell(d, cx, cy, ru * 0.20, rv * 0.20, fill=V((178, 128, 34)))
    _peace(d, cx, cy, ru * 0.115, rv * 0.115, V(PEACE))


def _ribbon(d, pts, w0, w1, fill, round_end=True):
    """A tapered stroke through a polyline: the brush model used throughout."""
    n = len(pts)
    if n < 2:
        return
    left, right = [], []
    for i in range(n):
        ax, ay = pts[i]
        bx, by = pts[min(i + 1, n - 1)]
        cx_, cy_ = pts[max(i - 1, 0)]
        dx, dy = bx - cx_, by - cy_
        L = math.hypot(dx, dy) or 1.0
        t = i / (n - 1)
        w = (w0 + (w1 - w0) * t) * 0.5
        nx, ny = -dy / L * w, dx / L * w
        left.append((ax + nx, ay + ny))
        right.append((ax - nx, ay - ny))
    d.polygon(left + right[::-1], fill=fill)
    if round_end:
        for (x, y), w in ((pts[0], w0), (pts[-1], w1)):
            r = w * 0.5
            d.ellipse([x - r, y - r, x + r, y + r], fill=fill)


def _scroll(d, x0, y0, su, sv, fill, flip=1, turns=2.1, w0=0.30, phase=0.0,
            dots=False, dotfill=None):
    """A big calligraphic C-scroll / paisley hook, optionally with a dot chain.

    The photograph's ground fill is made of these at 0.10-0.25 of the interior
    height, not of confetti; see section C.
    """
    n = 60
    pts, w = [], []
    for i in range(n):
        t = turns * math.pi * i / (n - 1)
        f = 0.18 + 0.070 * t
        pts.append((x0 + flip * su * f * math.cos(t + phase),
                    y0 + sv * f * math.sin(t + phase)))
        w.append(0.5 * (su + sv) * w0 * (1.0 - 0.72 * i / (n - 1)))
    _ribbon(d, pts, w[0], w[-1], fill)
    if dots:
        for i in range(6, n - 4, 7):
            r = w[i] * 0.42
            px, py = pts[i]
            nx = px - (x0 + flip * su * 0.18 * math.cos(phase))
            ny = py - (y0 + sv * 0.18 * math.sin(phase))
            L = math.hypot(nx, ny) or 1.0
            d.ellipse([px - nx / L * w[i] * 1.15 - r,
                       py - ny / L * w[i] * 1.15 - r,
                       px - nx / L * w[i] * 1.15 + r,
                       py - ny / L * w[i] * 1.15 + r],
                      fill=dotfill or GROUND)


def _vary(col, rng, lo=None, hi=None):
    lo = VARY[0] if lo is None else lo
    hi = VARY[1] if hi is None else hi
    f = lo + (hi - lo) * float(rng.random())
    return tuple(int(max(0, min(255, round(c * f)))) for c in col)


def _leaf(d, x, y, Lu, Lv, ang, fill=GOLD):
    pts = []
    for t in np.linspace(0, 2 * math.pi, 30):
        u, v = math.cos(t), 0.30 * math.sin(t)
        pts.append((x + (Lu * u) * math.cos(ang) - (Lv * v) * math.sin(ang),
                    y + (Lu * u) * math.sin(ang) + (Lv * v) * math.cos(ang)))
    d.polygon(pts, fill=fill)


def _star(d, cx, cy, rx, ry, fill=INK, rot=-math.pi / 2):
    pts = []
    for k in range(10):
        a = rot + math.pi * k / 5
        f = 1.0 if k % 2 == 0 else 0.40
        pts.append((cx + rx * f * math.cos(a), cy + ry * f * math.sin(a)))
    d.polygon(pts, fill=fill)


def _font(sz):
    """A face for the MENU-STRIP CAPS only.  The strips are PRINTED -- the
    vignettes on them are photographs -- so a typeface is right there.  The
    brush script on the other face loads no face at all."""
    from PIL import ImageFont
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, sz)
            except Exception:
                pass
    return ImageFont.load_default()


def _arched(d, text, cx, cy, wpx, cap, fill, rise=0.16):
    """One word on a shallow upward arch -- the side strips' words are arched."""
    f = _font(max(8, int(cap / 0.72)))
    tot = sum(d.textlength(ch, font=f) for ch in text) or 1.0
    k = min(1.0, wpx / tot)                 # shrink to fit, never enlarge
    f = _font(max(6, int(cap / 0.72 * k)))
    widths = [d.textlength(ch, font=f) for ch in text]
    tot = sum(widths) or 1.0
    x = cx - tot / 2
    for ch, w in zip(text, widths):
        t = (x + w / 2 - cx) / (tot / 2 + 1e-6)
        y = cy + rise * cap * (t * t - 0.35) * 2.0
        d.text((x + w / 2, y), ch, font=f, fill=fill, anchor="mm")
        x += w


# ----------------------------------------------------------- food vignettes
def _vig_bread(d, cx, cy, su, sv):
    for k in (-0.42, 0.10, 0.55):
        d.ellipse([cx + su * (k - 0.42), cy - sv * 0.34,
                   cx + su * (k + 0.42), cy + sv * 0.34], fill=(196, 148, 74))
    for k in (-0.6, 0.0, 0.6):
        d.polygon([(cx + su * k, cy - sv * 0.62), (cx + su * (k + 0.12), cy - sv * 0.40),
                   (cx + su * (k - 0.12), cy - sv * 0.40)], fill=GREEN)


def _vig_torta(d, cx, cy, su, sv):
    d.ellipse([cx - su, cy - sv * 0.44, cx + su, cy + sv * 0.50], fill=(198, 146, 72))
    d.rectangle([cx - su * 0.88, cy - sv * 0.08, cx + su * 0.88, cy + sv * 0.24],
                fill=PINK)
    d.ellipse([cx - su * 0.95, cy - sv * 0.10, cx - su * 0.45, cy + sv * 0.30],
              fill=GREEN)
    d.ellipse([cx + su * 0.50, cy - sv * 0.12, cx + su * 1.00, cy + sv * 0.28],
              fill=GREEN)


def _vig_juice(d, cx, cy, su, sv):
    d.polygon([(cx - su * 0.46, cy - sv * 0.78), (cx + su * 0.10, cy - sv * 0.78),
               (cx + su * 0.02, cy + sv * 0.70), (cx - su * 0.36, cy + sv * 0.70)],
              fill=(214, 176, 96))
    d.rectangle([cx - su * 0.44, cy - sv * 0.76, cx + su * 0.08, cy - sv * 0.30],
                fill=CREAMV)
    d.ellipse([cx + su * 0.08, cy - sv * 0.10, cx + su * 0.98, cy + sv * 0.68],
              fill=(206, 108, 34))
    d.ellipse([cx + su * 0.30, cy - sv * 0.22, cx + su * 0.52, cy + sv * 0.02],
              fill=(120, 138, 52))


def _vig_tostada(d, cx, cy, su, sv):
    d.ellipse([cx - su, cy - sv * 0.66, cx + su, cy + sv * 0.44], fill=CREAMV)
    d.ellipse([cx - su * 0.86, cy - sv * 0.10, cx + su * 0.86, cy + sv * 0.40],
              fill=(212, 62, 148))
    d.ellipse([cx - su * 0.60, cy - sv * 0.30, cx + su * 0.30, cy + sv * 0.06],
              fill=(206, 176, 60))


def _vig_shrimp(d, cx, cy, su, sv):
    pts = []
    for t in np.linspace(-2.4, 2.4, 30):
        r = 0.62 + 0.14 * math.cos(t * 1.6)
        pts.append((cx + su * r * math.cos(t), cy + sv * r * math.sin(t)))
    _ribbon(d, pts, sv * 0.42, sv * 0.10, (222, 132, 128))
    _ribbon(d, pts[:18], sv * 0.20, sv * 0.10, (190, 70, 62))


# ------------------------------------------------------------------ mural
# The two knobs turned until the achieved class fractions matched section B.
N_SCROLL = 520
SCROLL_MIX = (0.28, 0.60, 0.12)    # red : orange : gold, by draw count
SCROLL_S = (0.075, 0.185)          # scroll size range, fraction of interior H
SCROLL_W = (0.13, 0.23)            # scroll stroke width, fraction of its size
LEAF_F = 0.30                      # almond-leaf length / head radius
N_MOTTLE = 420                     # ground mottle blobs
# Every painted form on this board carries a dark keyline; without it the
# generated ground has no intermediate values and the median runs 20 codes hot.
DARKLINE = (72, 26, 16)            # the keyline under the scrolls and leaves
DARKLINE_F = 1.62                  # its width, x the form's own
# Per-form value jitter.  Without it every red pixel is the same red and the
# class medians land on the paint value instead of on the photograph's, which
# spreads over about +/-20 codes from shading, wear and the panel's own falloff.
VARY = (0.84, 1.08)
DOT_SZ = 0.118                     # petal-dot radius / head outer radius


def mural(path=None):
    im = Image.new("RGB", (W, H), GROUND)
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(1963)

    sl = int(round(W * STRIP_L_F))
    sr = int(round(W * STRIP_R_F))
    th = int(round(H * STRIP_T_F))
    Wi, Hi = W - sl - sr, H - th                 # rectified interior
    ox, oy = sl, th

    # --- ground mottle: the dark is not flat (interior luma p1 30, p5 35)
    for i in range(N_MOTTLE):
        x = rng.integers(ox - 40, ox + Wi + 40)
        y = rng.integers(oy - 20, H)
        r = rng.integers(int(0.02 * Hi), int(0.09 * Hi))
        d.ellipse([x - r, y - r * 0.8, x + r, y + r * 0.8], fill=GROUND_HI)
    im = im.filter(ImageFilter.GaussianBlur(0.020 * Hi))
    d = ImageDraw.Draw(im)

    ru = HEAD_RU_F * Wi
    rv = HEAD_RV_F * Hi
    heads = [(ox + u * Wi, oy + v * Hi) for (u, v) in HEADS_UV]
    part = [(ox + u * Wi, oy + v * Hi) for (u, v) in HEADS_PARTIAL_UV]

    # --- the calligraphic ground fill
    cols = ([RED] * int(round(SCROLL_MIX[0] * 100))
            + [ORANGE] * int(round(SCROLL_MIX[1] * 100))
            + [GOLD] * int(round(SCROLL_MIX[2] * 100)))
    for i in range(N_SCROLL):
        c = cols[int(rng.integers(0, len(cols)))]
        sz = float(rng.uniform(*SCROLL_S)) * Hi
        x0 = float(rng.integers(ox - int(0.05 * Wi), ox + Wi + int(0.05 * Wi)))
        y0 = float(rng.integers(oy - int(0.02 * Hi), H))
        su = sz * (Wi / Hi) / BOARD_ASPECT * 1.10
        fl = 1 if rng.random() < 0.5 else -1
        tn = 0.85 + 0.95 * rng.random()
        w0 = SCROLL_W[0] + (SCROLL_W[1] - SCROLL_W[0]) * rng.random()
        ph = 2 * math.pi * rng.random()
        _scroll(d, x0, y0, su, sz, DARKLINE, flip=fl, turns=tn,
                w0=w0 * DARKLINE_F, phase=ph)
        _scroll(d, x0, y0, su, sz, _vary(c, rng), flip=fl, turns=tn, w0=w0, phase=ph,
                dots=rng.random() < 0.42,
                dotfill=GROUND if c is not GOLD else (120, 70, 20))

    # --- stems and leaves LAST but one: in the photograph the stems run
    # in FRONT of the scrollwork, not behind it
    sw_ = STEM_W_F * Wi
    for (hx, hy) in heads:
        lean = (hx - W / 2) / (W / 2) * 0.030 * Hi
        pth = [(hx, hy), (hx + lean * 0.5, hy + (H - hy) * 0.5), (hx + lean, H)]
        _ribbon(d, pth, sw_ * 1.42, sw_ * 1.26, DARKLINE)
        _ribbon(d, pth, sw_ * 1.10, sw_ * 0.98, _vary(RED, rng))
        _ribbon(d, pth, sw_ * 0.80, sw_ * 0.70, _vary(ORANGE, rng))

    # --- gold almond leaves off the stems
    for j, (hx, hy) in enumerate(heads):
        for k, f in enumerate((0.28, 0.52, 0.76)):
            yy = hy + (H - hy) * f
            s = 1 if (j + k) % 2 else -1
            _leaf(d, hx + s * ru * 0.42, yy, ru * LEAF_F * 1.24,
                  rv * LEAF_F * 1.24, s * 0.85, DARKLINE)
            _leaf(d, hx + s * ru * 0.42, yy, ru * LEAF_F, rv * LEAF_F, s * 0.85,
                  _vary(GOLD, rng))

    # --- heads last, over the fill
    for i, (hx, hy) in enumerate(heads):
        flower(d, hx, hy, ru, rv, phase=0.21 * i,
               f=VARY[0] + (VARY[1] - VARY[0]) * float(rng.random()))
    for i, (hx, hy) in enumerate(part):
        flower(d, hx, hy, ru, rv, phase=0.4,
               f=VARY[0] + (VARY[1] - VARY[0]) * float(rng.random()))

    im = im.filter(ImageFilter.GaussianBlur(0.0009 * W))
    d = ImageDraw.Draw(im)

    # ---------------------------------------------------------- menu strips
    d.rectangle([0, 0, sl, H], fill=STRIP)
    d.rectangle([W - sr, 0, W, H], fill=STRIP)
    d.rectangle([0, 0, W, th], fill=STRIP)
    d.rectangle([0, H - int(0.006 * H), W, H], fill=(46, 24, 18))   # dark trim

    # top strip.  Legible: the two stars, FRESH, JUICES, & and TORTAS, at the
    # measured x fractions.  The 695 px between JUICES, and & is occluded and
    # what is drawn there is the RECONSTRUCTION recorded in section D.
    cap_t = th * 0.46
    ft = _font(max(10, int(cap_t / 0.72)))
    for u0, u1, s in ((0.1150, 0.2375, "FRESH"), (0.2454, 0.3858, "JUICES,"),
                      (0.3896, 0.6792, "GOURMET TACOS"),
                      (0.6908, 0.7383, "&"), (0.7529, 0.8938, "TORTAS")):
        x0, x1 = u0 * W, u1 * W
        wpx = d.textlength(s, font=ft) or 1.0
        # rev 50, A16 -- CLAMPED.  This was the file's ONLY unclamped text fit.
        # Two measured quantities are in play, the word's x-run (u0..u1, read off
        # ref_side.jpg) and the cap height (0.46 of the strip, stated at line 184
        # of this file's own header).  A substitute face cannot satisfy both, and
        # the unclamped form silently sacrificed the CAP HEIGHT -- which is the
        # one of the two that is a property of the type rather than of the
        # layout.  Measured on the shipped texture before this change, against
        # the declared 0.460:  FRESH 0.421, JUICES, 0.553, GOURMET TACOS 0.386,
        # TORTAS 0.421 -- and '&' 0.728, i.e. 1.58x its own recorded measurement,
        # breaking below the baseline the caps sit on.  It is the loudest thing
        # on the board in every side and hero frame.
        # The two sibling fits in this same file already do exactly this:
        #   _arched(), line 570:  k = min(1.0, wpx / tot)   "shrink to fit, never enlarge"
        #   side strips, line 794: k = min(1.0, wid*0.86/wpx) "shrink to fit only"
        # so this is the file's own idiom, not a new policy.
        # WHAT THIS DOES NOT FIX, stated rather than hidden: the clamp only bites
        # on '&' (every other word was already being shrunk, so k < 1 for them
        # and they do not move at all).  The clamped '&' is then NARROWER than
        # its measured run -- w/cap ~0.8 against the photograph's 114/64 = 1.78 --
        # because the substitute face's ampersand is not the painted one.  That
        # residual is a TYPEFACE difference and it is not closable from here.
        k = min(1.0, (x1 - x0) / wpx)
        f = _font(max(8, int(cap_t / 0.72 * k)))
        d.text(((x0 + x1) / 2, th * 0.50), s, font=f, fill=INK, anchor="mm")
    _star(d, 0.0938 * W, th * 0.50, th * 0.22, th * 0.22)
    _star(d, 0.9083 * W, th * 0.50, th * 0.22, th * 0.22)

    # side strips: the measured sequence at the measured v fractions (D).
    seq = [
        (0.001, 0.041, "a", "GOURMET"),
        (0.047, 0.096, "v", _vig_bread),
        (0.105, 0.145, "a", "TACOS"),
        (0.155, 0.191, "a", "&"),
        (0.204, 0.244, "a", "TORTAS"),
        (0.260, 0.337, "v", _vig_torta),
        (0.379, 0.416, "a", "FRESH"),
        (0.453, 0.511, "v", _vig_juice),
        (0.523, 0.555, "a", "JUICES"),
        (0.590, 0.612, "t", "CEVICHE"),
        (0.615, 0.637, "t", "TOSTADAS"),
        (0.665, 0.710, "v", _vig_tostada),
        (0.731, 0.755, "t", "SHRIMP"),
        (0.759, 0.783, "t", "& FISH"),
        (0.808, 0.872, "v", _vig_shrimp),
        (0.894, 0.918, "t", "TACOS"),
        (0.925, 0.933, "t", "y"),
        (0.936, 0.947, "i", None),
        (0.949, 0.960, "i", None),
        (0.961, 0.970, "i", None),
    ]
    for cxs, wid in ((sl * 0.5, sl), (W - sr * 0.5, sr)):
        for v0, v1, kind, val in seq:
            y0, y1 = v0 * H, v1 * H
            yc = (y0 + y1) / 2
            if kind == "v":
                val(d, cxs, yc, wid * 0.40, (y1 - y0) * 0.5)
            elif kind == "i":
                # the three lines that are NOT LEGIBLE (section D).  Drawn as
                # unreadable small type -- irregular strokes, not words -- so
                # that nothing is invented and the block still reads as type.
                rr = np.random.default_rng(int(v0 * 10000))
                n = int(rr.integers(6, 9))
                span = wid * (0.52 + 0.24 * rr.random())
                x = cxs - span / 2
                for k in range(n):
                    bw = span / n * (0.34 + 0.42 * rr.random())
                    hh = (y1 - y0) * (0.72 + 0.28 * rr.random())
                    d.rectangle([x, y1 - hh, x + bw, y1], fill=INK)
                    x += span / n
            elif kind == "a":
                _arched(d, val, cxs, yc, wid * 0.86, (y1 - y0), INK)
            else:
                f = _font(max(8, int((y1 - y0) / 0.72)))
                wpx = d.textlength(val, font=f) or 1.0
                k = min(1.0, wid * 0.86 / wpx)       # shrink to fit only
                f = _font(max(6, int((y1 - y0) / 0.72 * k)))
                d.text((cxs, yc), val, font=f, fill=INK, anchor="mm")

    im = im.filter(ImageFilter.GaussianBlur(0.0005 * W))
    p = path or os.path.join(TEXDIR, "lidmural.png")
    im.save(p)
    return p


# ------------------------------------------------------------- brush script
# Glyph skeletons as polylines in a normalised letter box: x runs 0 -> 1 across
# one advance, y is 0 at the baseline and -1 at the x-height, +ve downward.
# A brush model, not a font: no typeface is loaded on this face.

def _bez(p0, p1, p2, p3, n=44):
    out = []
    for i in range(n):
        t = i / (n - 1)
        m = 1 - t
        out.append((m ** 3 * p0[0] + 3 * m * m * t * p1[0]
                    + 3 * m * t * t * p2[0] + t ** 3 * p3[0],
                    m ** 3 * p0[1] + 3 * m * m * t * p1[1]
                    + 3 * m * t * t * p2[1] + t ** 3 * p3[1]))
    return out


def _glyph_S():
    """Capital S, y in CAP heights.  Read off ref_rear34 at 10x: a tight spiral
    eye at the top left, a full bowl, and a tail sweeping back down-LEFT past
    the S's own start into a taper."""
    return [
        (_bez((0.96, -0.84), (0.66, -1.06), (0.16, -1.02), (0.12, -0.75)),
         0.16, 0.62),
        (_bez((0.12, -0.75), (0.10, -0.52), (0.47, -0.50), (0.61, -0.65)),
         0.62, 0.92),
        (_bez((0.61, -0.65), (0.75, -0.46), (0.36, -0.38), (0.26, -0.20)),
         0.92, 1.28),
        (_bez((0.26, -0.20), (0.18, 0.05), (0.63, 0.13), (0.81, -0.08)),
         1.28, 0.55),
        (_bez((0.34, -0.16), (0.16, 0.09), (-0.20, 0.12), (-0.50, 0.15)),
         1.06, 0.10),
    ]


def _glyph_a():
    return [
        (_bez((0.86, -0.86), (0.52, -1.10), (0.10, -0.86), (0.16, -0.44)),
         0.30, 0.95),
        (_bez((0.16, -0.44), (0.20, -0.06), (0.66, -0.04), (0.78, -0.34)),
         0.95, 0.70),
        (_bez((0.80, -0.94), (0.80, -0.60), (0.78, -0.28), (0.90, -0.02)),
         0.70, 1.00),
    ]


def _glyph_n():
    return [
        (_bez((0.06, -0.86), (0.10, -0.50), (0.10, -0.24), (0.14, -0.02)),
         0.85, 1.00),
        (_bez((0.10, -0.62), (0.24, -0.96), (0.66, -0.98), (0.72, -0.60)),
         0.26, 0.60),
        (_bez((0.72, -0.60), (0.74, -0.36), (0.74, -0.20), (0.80, -0.02)),
         0.60, 1.00),
    ]


def _glyph_t():
    return [
        (_bez((0.30, -1.16), (0.28, -0.84), (0.26, -0.42), (0.34, -0.02)),
         0.42, 0.95),
        (_bez((-0.06, -0.86), (0.20, -0.90), (0.50, -0.90), (0.72, -0.86)),
         0.30, 0.30),
    ]


def _glyph_L_small():
    return [
        (_bez((0.44, -1.02), (0.30, -0.66), (0.24, -0.30), (0.26, -0.02)),
         0.40, 0.85),
        (_bez((0.26, -0.02), (0.36, 0.12), (0.62, 0.10), (0.80, -0.02)),
         0.85, 0.30),
    ]


def _draw_word(d, glyphs, origin, along, up, xh, sw_, pitch, outline_w,
               keyline_w):
    """Place glyph skeletons on a climbing baseline with an upright letter axis.

    `along` steps the pen down the baseline; `up` is the panel's own vertical
    (the measured letter axis, 2.6 deg off it), NOT the baseline normal -- that
    separation is the whole of this signboard's layout.  Three passes: dark
    outline, light keyline, red core -- all three are visible at 10x.
    """
    for pass_w, colour in ((outline_w, SIGN_OUTLINE),
                           (keyline_w, SIGN_KEYLINE),
                           (0.0, SIGN_RED)):
        pen = np.array(origin, float)
        al = np.array(along, float)
        uv = np.array(up, float)
        for g, adv in glyphs:
            for pts, w0, w1 in g:
                path = []
                for (gx, gy) in pts:
                    p = pen + al * (gx * adv * pitch) + uv * (gy * xh)
                    path.append((p[0], p[1]))
                _ribbon(d, path, max(1.0, sw_ * w0 + pass_w),
                        max(1.0, sw_ * w1 + pass_w), colour)
            pen = pen + al * (adv * pitch)


def front_sign(path=None, mirror=None):
    """The FRONT lid's INWARD face: cream, red brush script, red star.

    Same aspect as the mural because it is the same board.  Set
    T1_LIDSIGN_MIRROR=1 (or mirror=True) to have the texture written already
    flipped in u, for the case where t1_shell gives the back face the same UV
    winding as the front -- see the report.
    """
    if mirror is None:
        mirror = os.environ.get("T1_LIDSIGN_MIRROR", "0") not in ("0", "", "no")
    im = Image.new("RGB", (SW, SH), SIGN_CREAM)
    d = ImageDraw.Draw(im)

    # the thin yellow pinstripe measured along the panel's top edge
    d.rectangle([0, 0, SW, int(SH * 0.009)], fill=SIGN_EDGE)

    # --- geometry.  Every number here is either a section-E measurement or is
    # derived from one; the vertical placement is the one stated assumption.
    base = math.radians(SIGN_BASE_DEG)
    along = np.array([math.cos(base), -math.sin(base)])
    slant = math.radians(SIGN_LETTER_DEG)
    up = np.array([-math.sin(slant), math.cos(slant)])

    lock_w = (SIGN_LOCK_U1 - SIGN_LOCK_U0) * SW          # 0.219 of the board W
    sw_ = SIGN_STROKE_OVER_LOCK * lock_w                 # foreshortening-free
    cap = sw_ / SIGN_STROKE_OVER_CAP
    xh = cap * SIGN_XH_OVER_CAP
    desc = cap * SIGN_DESC_OVER_CAP
    outline_w = sw_ * 0.62
    keyline_w = sw_ * 0.26

    # the S + the four following glyphs share one baseline run whose horizontal
    # projection is the measured (SIGN_LOCK_U1 - SIGN_S_U0)
    run = (SIGN_LOCK_U1 - SIGN_S_U0) * SW
    L = run / math.cos(base)
    s_adv = 0.235 * L
    after_adv = (1.00, 1.06, 0.72, 1.00)
    pitch2 = 0.765 * L / sum(after_adv)
    climb = run * math.tan(base)

    # vertical: hang the lockup from SIGN_TOP_V with no letterform clipped
    top = SIGN_TOP_V * SH
    s_base_y = top + climb + xh
    s_org = np.array([SIGN_S_U0 * SW, s_base_y])

    _draw_word(d, [(_glyph_S(), 1.0)], tuple(s_org), along, up,
               cap, sw_ * 1.28, s_adv, outline_w * 1.28, keyline_w * 1.28)

    # the merged downstrokes after the S.  RECONSTRUCTED, not read -- E.
    after = [(_glyph_a(), after_adv[0]), (_glyph_n(), after_adv[1]),
             (_glyph_t(), after_adv[2]), (_glyph_a(), after_adv[3])]
    start = s_org + along * s_adv
    _draw_word(d, after, tuple(start), along, up, xh, sw_, pitch2,
               outline_w, keyline_w)

    # "La", small, on its own baseline, at the measured u extent and the
    # measured cap ratio
    la_u0, la_u1 = SIGN_LA_U[0] * SW, SIGN_LA_U[1] * SW
    la_cap = cap * SIGN_LA_CAP_RATIO
    la_run = (la_u1 - la_u0)
    la_L = la_run / math.cos(base)
    la_org = (la_u0, s_base_y - (SIGN_S_U0 * SW - la_u0) * math.tan(base)
              + climb * 0.0 + la_cap * 0.62)
    _draw_word(d, [(_glyph_L_small(), 1.0), (_glyph_a(), 0.95)],
               la_org, along, up, la_cap, sw_ * 0.70, la_L / 1.95,
               outline_w * 0.70, keyline_w * 0.70)

    # the red star: measured centre u, and a regular star's w/h
    st_rx = SIGN_STAR_W_F * SW * 0.5
    st_ry = st_rx / SIGN_STAR_WH
    st_x = SIGN_STAR_U * SW
    # clearance above the S's entry stroke.  The gap between the star and the
    # S is not separately measurable at 80 px; 0.42 cap is stated, and it is
    # the smallest gap that keeps the two shapes from touching.
    st_y = s_base_y - cap * 1.56 - st_ry
    _star(d, st_x, st_y, st_rx, st_ry, fill=SIGN_RED)

    im = im.filter(ImageFilter.GaussianBlur(0.0006 * SW))
    if mirror:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    p = path or os.path.join(TEXDIR, "lidsign.png")
    im.save(p)
    return p


# rev 8 called this rear_sign().  The panel is the FRONT lid's INWARD face; the
# old name is kept so nothing outside this file breaks on import.
rear_sign = front_sign


# ------------------------------------------------------------------- audit
def audit_mural(path=None):
    """Score the written mural against the photograph, same classifier.

    Targets are the section-B measurement of the rectified, occluder-masked
    board interior.  VALUE_GAIN is 1.0, so the thresholds are the photograph's
    own; if the albedo lift is ever revived the threshold moves with it.
    """
    p = path or os.path.join(TEXDIR, "lidmural.png")
    im = Image.open(p).convert("RGB")
    a = np.asarray(im).astype(float)
    hsv = np.asarray(im.convert("HSV")).astype(float)
    hh = hsv[..., 0] * 360 / 255.0
    v = hsv[..., 2] / 255.0
    sl = int(round(im.width * STRIP_L_F))
    sr = int(round(im.width * STRIP_R_F))
    th = int(round(im.height * STRIP_T_F))
    s = np.s_[th:im.height - int(0.006 * im.height), sl:im.width - sr]
    hh, v, a = hh[s], v[s], a[s]
    px = a.reshape(-1, 3)
    lum = 0.299 * px[:, 0] + 0.587 * px[:, 1] + 0.114 * px[:, 2]
    mx, mn = px.max(1), px.min(1)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    dark = v < 0.30 * VALUE_GAIN
    red = (~dark) & ((hh < 14) | (hh >= 345))
    orn = (~dark) & (hh >= 14) & (hh < 30)
    yel = (~dark) & (hh >= 30) & (hh < 62)
    nd = float((~dark).sum())
    got = {
        "dark": 100 * dark.mean(), "red": 100 * red.mean(),
        "orange": 100 * orn.mean(), "yellow": 100 * yel.mean(),
        "nd_red": 100 * red.sum() / nd, "nd_orange": 100 * orn.sum() / nd,
        "nd_yellow": 100 * yel.sum() / nd,
        "medR": float(np.median(px[:, 0])), "medG": float(np.median(px[:, 1])),
        "medB": float(np.median(px[:, 2])),
        "p5": float(np.percentile(lum, 5)), "p25": float(np.percentile(lum, 25)),
        "p50": float(np.percentile(lum, 50)), "p75": float(np.percentile(lum, 75)),
        "p95": float(np.percentile(lum, 95)),
        "lmean": float(lum.mean()), "lsd": float(lum.std()),
        "satmed": float(np.median(sat)), "satmean": float(sat.mean()),
    }
    g = VALUE_GAIN
    tgt = {
        "dark": 20.26, "red": 26.19, "orange": 34.06, "yellow": 19.49,
        "nd_red": 32.8, "nd_orange": 42.7, "nd_yellow": 24.4,
        "medR": 139.0 * g, "medG": 49.0 * g, "medB": 21.0 * g,
        "p5": 35.1 * g, "p25": 47.3 * g, "p50": 72.8 * g, "p75": 97.2 * g,
        "p95": 126.3 * g, "lmean": 74.9 * g, "lsd": 30.0,
        "satmed": 0.835, "satmean": 0.795,
    }
    return got, tgt


def audit_sign(path=None):
    """Score the written sign face against the measured panel fractions."""
    from scipy import ndimage as ndi
    p = path or os.path.join(TEXDIR, "lidsign.png")
    im = Image.open(p).convert("RGB")
    a = np.asarray(im).astype(float)
    sw, sh = im.size
    lum = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    ink = lum < 195
    ink[:int(sh * 0.02)] = False           # the yellow edge pinstripe
    ys, xs = np.nonzero(ink)
    lab, n = ndi.label(ink)
    # the star is the component whose centroid is nearest the drawn star centre
    cen = ndi.center_of_mass(ink, lab, range(1, n + 1))
    # The star touches the S's outline at this size, so a connected-component
    # search finds the whole lockup.  Instead: seed on the TOPMOST ink pixel in
    # a column band around the drawn star's u and grow only inside a box of
    # three star-widths.  That measures the written pixels, not the intent.
    tx = SIGN_STAR_U * sw
    want = SIGN_STAR_W_F * sw
    band = np.zeros_like(ink)
    band[:, int(tx - 0.5 * want):int(tx + 0.5 * want)] = True
    by, bx = np.nonzero(ink & band)
    y0 = int(by.min())
    box = np.zeros_like(ink)
    box[y0:y0 + int(1.25 * want), int(tx - 0.62 * want):int(tx + 0.62 * want)] = True
    lab2, n2 = ndi.label(ink & box)
    seedx = int(np.median(bx[by <= y0 + 1]))
    star = lab2[y0, seedx] or 1
    sy, sx = np.nonzero(lab2 == star)
    got = {"u_lo": xs.min() / sw, "u_hi": xs.max() / sw,
           "v_lo": ys.min() / sh, "v_hi": ys.max() / sh,
           "vspan_over_W": (ys.max() - ys.min()) / sw,
           "star_u": (sx.min() + sx.max()) / 2 / sw,
           "star_w": (sx.max() - sx.min()) / sw,
           "star_wh": ((sx.max() - sx.min()) / (sy.max() - sy.min()))}
    tgt = {"u_lo": SIGN_LOCK_U0, "u_hi": SIGN_LOCK_U1,
           "v_lo": float("nan"), "v_hi": float("nan"),
           "vspan_over_W": 0.449 / BOARD_ASPECT * 1.0,
           "star_u": SIGN_STAR_U,
           "star_w": SIGN_STAR_W_F, "star_wh": SIGN_STAR_WH}
    return got, tgt


if __name__ == "__main__":
    print(mural())
    print(front_sign())
    g, t = audit_mural()
    print("\nMURAL  interior, ref_side classifier, dark V < %.3f" % (0.30 * VALUE_GAIN))
    rows = [("dark %", "dark"), ("red %", "red"), ("orange %", "orange"),
            ("yellow %", "yellow"), ("red % of non-dark", "nd_red"),
            ("orange % of non-dark", "nd_orange"),
            ("yellow % of non-dark", "nd_yellow"),
            ("median R", "medR"), ("median G", "medG"), ("median B", "medB"),
            ("luma p5", "p5"), ("luma p25", "p25"), ("luma p50", "p50"),
            ("luma p75", "p75"), ("luma p95", "p95"),
            ("luma mean", "lmean"), ("luma sd", "lsd"),
            ("HSV sat median", "satmed"), ("HSV sat mean", "satmean")]
    print("  %-22s %10s %10s %9s" % ("quantity", "achieved", "target", "delta"))
    for label, k in rows:
        print("  %-22s %10.3f %10.3f %+9.3f" % (label, g[k], t[k], g[k] - t[k]))
    gs, ts = audit_sign()
    print("\nSIGN   panel fractions")
    print("  %-22s %10s %10s %9s" % ("quantity", "achieved", "target", "delta"))
    for k in ("u_lo", "u_hi", "vspan_over_W", "star_u", "star_w", "star_wh"):
        print("  %-22s %10.4f %10.4f %+9.4f" % (k, gs[k], ts[k], gs[k] - ts[k]))
    print("  %-22s %10.4f %10s   (not a target: the vertical placement is the"
          " stated assumption)" % ("v_lo", gs["v_lo"], "--"))
    print("  %-22s %10.4f %10s" % ("v_hi", gs["v_hi"], "--"))
