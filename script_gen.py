"""
script_gen.py -- the "Senor Tacombi" flank script, drawn as explicit outlines.

WHY THIS REPLACES THE FONT APPROACH
rev 8 shipped a system script face (NothingYouCouldDo) with a stroked swash and
stroked spirals drawn on top. Donald rejected it by name: "That script i see on
the p9 hero is NOT it." SPEC sec.10.10 makes the standard explicit -- every
painted element must be REPRODUCED from the photograph, not approximated -- and
names "a system font with flourishes bolted on" as the failure mode.

So there is no font here. Every glyph is built from primitives whose control
points were read off ref_side.jpg at 6-14x magnification, in the coordinate
frame of that photograph.

THE COORDINATE FRAME
All geometry below is in MASK SPACE: the pixel grid of ref_side.jpg offset to
(X0, Y0) = (325, 486), y increasing downward. That is deliberate -- it means a
control point in this file can be compared directly against the photograph
without a change of basis, and the acceptance test is a straight overlay.
Measured ink bounding box of the real script in this frame:

    x 5 -> 276, y 4 -> 103   (271 x 99 px, aspect 2.737)

WHAT WAS MEASURED, AND WHERE IT CAME FROM
  * ink is neutral silver, not white and not gold: median RGB (127,122,125),
    saturation 0.080, over a ground of (129,21,14).
  * the T's stem occupies x 33-60 and drops to the lowest point of the whole
    lockup at y 103; its swash ribbon runs x 6-116, entering at a rolled left
    terminal whose eye is a measured hole at (14.9, 63.1), cresting near
    x 90, and rolling clockwise over itself above the 'c' at x 96-116.
  * three spiral counters, centres (72, 72) / (112, 62) / (149, 60) for a, c
    and o. The o's counter is the one closed hole the segmentation finds:
    x 141-161, y 49-73, area 224 px in a 21x25 box -- 43% fill, which is a
    groove, not a plain bowl.
  * m spans x 166-215; b's bowl x 218-250.
  * the baseline is not level. Letter feet measured at (75,88) (112,85)
    (149,82) (190,74) (235,70) (265,58): the word arcs upward to the right.
    NOTE this fit is no longer used by anything: the m's three feet are at
    y 74.2, 67.2 and 63.3, which no single smooth baseline passes through,
    and every glyph now carries its own measured feet.

TWO CLAIMS ABOVE THAT rev 10 MEASURED AND FOUND FALSE -- kept, struck through,
because they are what the generator was built on and the next reader needs to
know they were tested rather than quietly dropped:
  * "b's counter is a tilted ellipse x 236-247, y 33-51" -- the counter is
    there, but the bowl around it is not a ring of even weight: its left stem
    is half-width 5.9-7.2 against 1.8-2.8 over the counter. An ellipse minus
    an ellipse cannot make that, and the b scored 0.362 while it tried to.
  * "i's dot is a tilted ellipse at x 248-263, y 16-31, [separate from the
    stem]" -- there is no separate dot. The mask is one connected stroke from
    (248, 20.6) to the exit terminal at (274, 39.2), with a measured 2.2
    half-width neck at (252.8, 25.3) joining head to stem.

CONSTRUCTION -- rev 10, and this is a change of method, not of numbers
Every glyph is now a union of variable-width strokes swept along its MEASURED
MEDIAL AXIS, with the half-width taken from the distance transform at every
sample.  See the block above mpath().  Nothing is placed by eye any more.

The model this replaced was "a solid bowl with a spiral GROOVE subtracted",
and it was wrong in a way that could not be fixed by moving its control
points.  The photograph does not show a disc with a trench cut in it; it shows
a RIBBON wound twice, and the counters are what the winding fails to cover.
The difference is testable and it was tested: `a` has two small counters
(x 69-74 y 65-71 and x 72-80 y 76-83), and one analytic Archimedean groove can
only ever produce one of them.  Against compare_script.py the change is
     T .706  swash .683  a .454  c .617  o .618  m .545  b .362  i .499
  -> T .981  swash .955  a .955  c .964  o .964  m .939  b .948  i .935
with the whole lockup going 0.547 -> 0.942.  Two glyphs were not merely
mis-shaped but mis-PLACED: the b's ascender leaned the wrong way and sat 30 px
right of the reference, and the a carried a 40 px stem the photograph has no
ink for at all.

Rasterised supersampled, then area-averaged down, so the edges are clean at
any output size.

    python3 script_gen.py            -> tex/senor.png
    python3 script_gen.py --compare  -> also writes the overlay against ref
    python3 script_gen.py --glyph b  -> 8x photo | ref | gen | overlay for one
                                        compare_script box, to out/glyph_b.png
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy.interpolate import CubicSpline

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, "tex")

# ---- the frame -------------------------------------------------------------
X0, Y0 = 325, 486                      # mask space origin in ref_side.jpg px
MW, MH = 290, 114                      # mask space extent BELOW y=0
INK_BBOX = (5, -12, 275, 102)          # measured ink bbox, x0 y0 x1 y1

# rev 10.  The frame used to start at mask y = 0 and the reference ink was
# believed to start there too.  It does not.  The rev-9 reference segmentation
# thresholded on saturation and silently dropped every TARNISHED pixel -- which
# is most of 'Senor', the b flag and half the i dot.  Re-segmented properly
# (SPEC 10.20) the real ink runs y 474-588 in ref_side.jpg, i.e. mask y -12 to
# +102.  The generator had never drawn the top 12 rows because nothing in the
# reference mask asked it to: the generated lockup was 99 px tall against a
# reference 114 px tall.
#
# The origin is NOT moved -- every control point in this file is expressed in
# the (325, 486) frame and moving it would invalidate all of them.  Instead the
# canvas gains a pad ABOVE y = 0 and the rasteriser translates into it, so a
# control point may now legitimately carry a negative y.
YPAD = 16                              # mask rows available above y = 0
MH_TOT = MH + YPAD

SS = 12                                # supersample factor
OUT_W = 4096                           # decal width; SPEC sec.5 wants 3K-4K


# --------------------------------------------------------------- path helpers
# rev 10: bez/poly/widths/spiral_pts/ellipse_pts and the bowl()/groove() pair
# built on them are gone.  Nothing used them once every glyph was traced, and
# groove() in particular encoded the refuted "disc minus one Archimedean
# spiral" model of the counters -- see CONSTRUCTION at the top of this file.
def resample(pts, n=400):
    d = np.r_[0.0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]
    if d[-1] <= 0:
        return pts
    u = np.linspace(0, d[-1], n)
    return np.c_[np.interp(u, d, pts[:, 0]), np.interp(u, d, pts[:, 1])]


def stroke_poly(pts, w):
    """Outline of a variable-width stroke: left side out, right side back."""
    pts = np.asarray(pts, float)
    d = np.gradient(pts, axis=0)
    L = np.hypot(d[:, 0], d[:, 1])
    L[L == 0] = 1.0
    nx, ny = -d[:, 1] / L, d[:, 0] / L
    left = pts + np.c_[nx, ny] * w[:, None]
    right = pts - np.c_[nx, ny] * w[:, None]
    return np.vstack([left, right[::-1]])


# rev 10.  MEASURED-AXIS STROKES.
#
# The glyphs below that carry a `# axis:` comment are no longer placed by eye.
# Their control points are samples of the TRUE MEDIAL AXIS of the reference ink
# mask (skimage.morphology.medial_axis on the mask upsampled x6 and Gaussian-
# filtered at sigma = 0.55 source px, exactly the pipeline senor_trace.py
# documents and validates at IoU 0.913), and the third number of each triple is
# the exact distance transform at that sample -- i.e. the measured HALF-WIDTH.
# Nothing is added to it.  Branches shorter than 3 source px are dropped as
# spurs; the half-width at a Y-junction is the inscribed radius there and is
# therefore larger than either stroke, which is geometry, not weight.
#
# This is the same instrument that produced the sec.6 modulation table in
# measure/script_ink.md, so a glyph traced this way reproduces its measured
# thick/thin ratio by construction instead of being given a hand-guessed one.
def mpath(pts, n=400):
    """Arc-length cubic spline through measured axis samples (x, y, halfwidth)."""
    p = np.asarray(pts, float)
    d = np.r_[0.0, np.cumsum(np.hypot(*np.diff(p[:, :2], axis=0).T))]
    u = np.linspace(0, d[-1], n)
    return CubicSpline(d, p[:, :2], axis=0)(u), np.interp(u, d, p[:, 2])


def mstroke(c, pts, k=1.0, cut=False, caps=True, n=400):
    """Sweep the measured half-width along the measured axis. k scales width."""
    xy, w = mpath(pts, n)
    c.stroke(xy, w * k, cut=cut, caps=caps)


# ------------------------------------------------------------------ rasteriser
class Canvas:
    def __init__(self):
        self.ink = Image.new("L", (MW * SS, MH_TOT * SS), 0)
        self.hole = Image.new("L", (MW * SS, MH_TOT * SS), 0)
        self.di = ImageDraw.Draw(self.ink)
        self.dh = ImageDraw.Draw(self.hole)

    def _fill(self, d, pts):
        # y is translated by YPAD so mask-space y may be negative
        d.polygon([(float(x) * SS, (float(y) + YPAD) * SS) for x, y in pts],
                  fill=255)

    def blob(self, pts):
        self._fill(self.di, pts)

    def cut(self, pts):
        self._fill(self.dh, pts)

    def stroke(self, pts, w, cut=False, caps=True):
        pts = resample(np.asarray(pts, float), 400)
        if np.isscalar(w):
            w = np.full(len(pts), float(w))
        else:
            w = np.asarray(w, float)
            if len(w) != len(pts):
                w = np.interp(np.linspace(0, 1, len(pts)),
                              np.linspace(0, 1, len(w)), w)
        d = self.dh if cut else self.di
        self._fill(d, stroke_poly(pts, w))
        if caps:
            for p, r in ((pts[0], w[0]), (pts[-1], w[-1])):
                d.ellipse([(p[0] - r) * SS, (p[1] + YPAD - r) * SS,
                           (p[0] + r) * SS, (p[1] + YPAD + r) * SS], fill=255)

    def alpha_box(self, k):
        """Coverage in [0,255], box-downsampled by k rather than by SS.

        SPEC 10.121 (rev 47).  THE RASTER IS DRAWN AT SS AND WAS THROWN AWAY AT
        SS.  Canvas draws at MW*SS = 3480 px across; alpha() reduced that to MW
        = 290 px, of which the ink spans 271; main() then LANCZOS-upscaled those
        271 px to OUT_W = 4096 -- a 15.11x magnification of a raster that had
        already discarded twelve times its own detail.  Every edge in the
        shipped texture was a 14.1 px ramp for that reason alone, and three
        revisions read the resulting mush as a CONTRAST fault and chased an
        amplitude number for a spatial-frequency defect.

        k = SS reproduces the historic mask space EXACTLY -- alpha() below is
        that call and nothing else, so every mask-space comparison, every
        threshold and every stored figure in this project is bit-identical
        across this change.  k = 1 returns the drawn raster untouched.
        """
        if (MW * SS) % k or (MH_TOT * SS) % k:
            raise ValueError("alpha_box: k=%d does not divide the raster" % k)
        a = np.array(self.ink, np.uint8).astype(np.float32)
        h = np.array(self.hole, np.uint8).astype(np.float32)
        m = np.clip(a - h, 0, 255)
        if k == 1:
            return m
        return m.reshape(MH_TOT * SS // k, k, MW * SS // k, k).mean(axis=(1, 3))

    def alpha(self):
        """Coverage in [0,255], MH_TOT rows.  Row i is mask-space y = i - YPAD."""
        return self.alpha_box(SS)


# ---------------------------------------------------------------- the lockup
# rev 10: the quadratic baseline() fit through six eyeballed feet is gone with
# its last caller (draw_m).  It was never a good model -- the m's own three
# feet measure y 74.2, 67.2 and 63.3, and no smooth curve through the six
# points above passes within 3 px of all three -- and every glyph now carries
# its own measured terminals instead of being hung off a shared curve.
def draw_T(c):
    """
    Capital T: a broad stem, and a ribbon swash that enters from a rolled
    terminal at the far left, sweeps right beneath 'Senor', and rolls clockwise
    over itself above the 'c'.

    rev 10.  The old construction had the right shape and the wrong dimensions.
    Three measured facts it missed:
      * the swash is far heavier than it was drawn.  Its width profile topped
        out at half-width 6.5; the reference reaches 11.1 where the ribbon runs
        into the T's stem at (39.3, 42.0), and holds 6.5-8.4 from x 68 to x 78.
        That is the sec.6 figure -- swash 3.61 thick/thin, the largest in the
        lockup -- and a 6.5 cap cannot express it.
      * the rolled tip did not roll far enough.  It stopped at x 98.6; the
        reference tail runs back left along y 16-20 all the way to x 87.7,
        where it disappears under the tarnished `r` of `Senor`.
      * the stem is not vertical and it is not where it was drawn.  Measured
        axis runs (39.2, 42.5) to (50.5, 89.2) -- an 11 px lean over the drop,
        against a drawn stem that sat at a near-constant x 46.  It was ~5 px
        right of the reference for its whole length, which is most of the T's
        missing IoU and also the 'ref-only' band at x 33-37.
      * the foot is not one wedge but two arms off (50.5, 89.5): one running
        right to a fine terminal at (69.2, 94.3), one down-left to (38.8,
        100.3).  sec.7 measures both as widening continuously into the tip
        (bulb/neck 0.86 and 0.79), which is what the profiles below do.
    """
    # --- the swash ribbon, right to left ---------------------------------
    # axis: the rolled tip above the `c`, over the crest and back along the
    # underside to the junction with the stem
    mstroke(c, [(87.7, 19.8, 4.2), (89.7, 16.8, 3.0), (92.7, 16.0, 2.0),
                (95.7, 17.7, 1.9), (98.7, 20.3, 3.4), (101.7, 18.7, 2.3),
                (104.7, 18.3, 1.7), (107.7, 18.5, 1.9), (110.7, 20.8, 2.5),
                (112.0, 23.8, 3.0), (112.0, 26.8, 3.0), (111.8, 29.8, 3.1),
                (111.0, 32.8, 4.0), (108.3, 35.8, 5.0), (105.3, 37.7, 5.8),
                (102.3, 39.2, 6.2), (99.3, 40.5, 6.0), (96.3, 41.0, 6.0),
                (93.3, 41.8, 6.1), (90.3, 41.8, 6.0), (87.3, 42.0, 6.0),
                (84.3, 42.0, 6.0), (81.3, 41.8, 6.2), (78.3, 41.3, 6.5),
                (75.3, 40.8, 6.5), (72.3, 39.7, 7.1), (68.2, 36.8, 8.2)])
    # axis: the short spur that drops off the tail where it meets `Senor`'s r
    mstroke(c, [(87.7, 20.2, 4.3), (89.3, 25.2, 2.6), (91.2, 27.2, 1.2)])
    # axis: the body, flat at y 36.2-37.7 and thickening steadily to the left
    mstroke(c, [(67.8, 36.8, 8.2), (64.8, 37.0, 7.4), (61.8, 36.7, 6.8),
                (58.8, 36.5, 6.5), (55.8, 36.2, 6.8), (52.8, 36.2, 7.3),
                (49.8, 36.8, 8.0), (46.8, 37.3, 9.0), (43.5, 37.7, 10.6)])
    # axis: the shoulder where the ribbon turns down across the stem
    mstroke(c, [(43.2, 37.8, 10.7), (40.5, 40.8, 10.8), (39.3, 42.0, 10.9)])
    # axis: the run out to the left terminal, thinning 11.0 -> 4.7
    mstroke(c, [(38.8, 42.2, 10.9), (35.8, 42.0, 9.3), (32.8, 41.8, 8.1),
                (29.8, 41.7, 7.4), (26.8, 42.3, 6.7), (23.8, 43.2, 6.4),
                (20.8, 44.3, 6.0), (17.8, 46.0, 5.4), (14.8, 47.7, 5.1),
                (11.7, 51.5, 4.8)])
    # axis: the left roll itself -- 1.2 turns anticlockwise about (16.5, 62.5),
    # wrapping the eye the segmentation finds at (14.9, 63.1)
    mstroke(c, [(11.5, 51.8, 4.6), (9.7, 54.8, 3.8), (9.2, 57.8, 3.3),
                (9.2, 60.8, 2.8), (9.8, 63.8, 2.6), (11.5, 66.8, 2.1),
                (14.3, 69.7, 2.2), (17.3, 70.8, 2.1), (20.3, 70.7, 1.8),
                (23.0, 68.8, 2.4), (24.2, 65.8, 3.8), (23.5, 62.8, 5.2),
                (21.0, 60.2, 6.0)])
    # axis: the return arm that closes the eye
    mstroke(c, [(11.8, 51.8, 4.5), (14.8, 54.8, 1.4), (17.8, 57.7, 3.0),
                (20.2, 59.5, 5.2)])

    # --- the stem --------------------------------------------------------
    # axis: down from the swash shoulder, leaning right, waisted at y 57
    mstroke(c, [(39.2, 42.5, 10.9), (39.8, 45.5, 9.5), (40.3, 48.5, 8.6),
                (40.8, 51.5, 8.1), (41.5, 54.5, 7.8), (42.3, 57.5, 7.6),
                (43.2, 60.5, 7.6), (44.0, 63.5, 7.8), (45.0, 66.2, 8.2),
                (45.5, 69.2, 7.8), (46.7, 72.2, 7.9), (47.0, 75.2, 8.2),
                (47.8, 78.2, 8.7), (48.7, 81.2, 8.9), (49.3, 84.2, 9.5),
                (50.0, 87.2, 10.2), (50.5, 89.2, 10.6)])
    # axis: foot, right arm
    mstroke(c, [(50.8, 89.5, 10.4), (53.8, 90.7, 8.4), (56.8, 92.0, 6.9),
                (59.8, 92.8, 5.3), (62.8, 94.0, 4.0), (65.8, 94.3, 2.6),
                (69.2, 94.3, 1.5)])
    # axis: foot, left arm
    mstroke(c, [(50.5, 89.5, 10.5), (48.2, 92.5, 8.3), (45.3, 95.2, 5.9),
                (42.5, 97.8, 4.1), (39.5, 99.8, 2.2), (38.8, 100.3, 1.9)])
    # axis: the two arms that rise off the stem's shoulder under `Senor`
    mstroke(c, [(47.7, 23.8, 3.6), (45.8, 26.8, 3.3), (44.2, 29.8, 5.1),
                (42.5, 32.8, 8.0), (42.3, 33.3, 8.3), (43.0, 36.3, 10.1),
                (43.2, 37.5, 10.6)])
    mstroke(c, [(36.8, 26.7, 3.0), (38.8, 29.7, 4.9), (41.7, 32.7, 7.8),
                (42.0, 33.0, 8.0)])
    mstroke(c, [(44.3, 18.5, 2.6), (46.2, 21.5, 2.3), (47.7, 23.5, 3.5)])
    # axis: the fine crossbar that runs right off the shoulder and drops into
    # the swash at (67.8, 36.5).  Half-width 1.2-2.8 -- at the resolution limit
    # of this photograph, but it is 4-6 px of real ink and it is what joins the
    # T to the swash above the `a`.
    mstroke(c, [(48.0, 23.7, 3.6), (51.0, 24.2, 2.8), (54.0, 24.8, 2.2),
                (57.0, 25.0, 1.9), (60.0, 25.5, 1.7), (63.0, 26.8, 1.2),
                (65.8, 28.7, 2.0), (67.2, 31.7, 4.1), (67.7, 34.7, 6.6),
                (67.8, 36.5, 8.0)])


def draw_a(c):
    """
    rev 10.  The `a` was a solid ellipse with a spiral trench cut out of it and
    a long right-hand stem, and it ran 20 % HEAVY at IoU 0.454.

    Two things were wrong and only one of them was weight.  The stem was
    invented: the reference has NO ink at x 84-94 between y 48 and y 72, so a
    third of the generated area sat on bare ground.  And the letter is not a
    bowl with a groove taken out of it -- it is a RIBBON wound twice, whose own
    medial axis is the spiral.  Drawing the ribbon instead of the bowl gets the
    two small counters (x 69-74 y 65-71, and x 72-80 y 76-83, ~75 px together)
    for free and in the right places, where a single analytic groove could only
    ever put one of them.

    Half-widths run 3.0-4.3 over the turns and open to 5.1-6.2 at the two
    junctions where the ribbon touches itself -- ratio 2.4, which is sec.6's
    measured figure for `a` (2.41) rather than a chosen one.
    """
    # axis: entry off the T's stem, over the top, down the right shoulder.
    # The 2.3 half-width at (54.7, 63.8) is the measured neck where the letter
    # leaves the stem -- the narrowest join in the lockup.
    mstroke(c, [(45.7, 65.7, 7.5), (48.7, 64.8, 4.8), (51.7, 64.3, 2.6),
                (54.7, 63.8, 2.3), (57.7, 63.5, 4.1), (60.7, 63.5, 6.2),
                (65.0, 61.0, 4.0), (69.0, 60.7, 3.3), (73.0, 61.5, 3.5),
                (77.0, 65.0, 3.9), (79.2, 69.0, 4.2), (79.7, 71.8, 5.1),
                (82.8, 76.2, 3.7), (84.5, 80.2, 4.0), (85.7, 82.7, 4.9)])
    # axis: round the foot and back up the left side to close the outer turn
    mstroke(c, [(85.5, 83.0, 4.8), (81.2, 86.5, 3.3), (77.2, 88.3, 3.7),
                (73.2, 87.3, 3.8), (69.7, 84.2, 3.7), (67.8, 80.2, 4.3),
                (69.7, 76.2, 4.2)])
    # axis: the inner turn -- right along the middle, then up to the entry
    mstroke(c, [(69.7, 76.0, 4.1), (71.3, 75.3, 3.5), (75.3, 73.8, 3.2),
                (79.3, 72.2, 5.0)])
    mstroke(c, [(61.0, 63.7, 6.2), (63.0, 67.7, 4.7), (66.7, 70.0, 3.4),
                (68.7, 74.0, 3.0), (69.7, 75.8, 4.2)])
    # axis: the exit that carries the foot across into the `c`.  The 2.8
    # half-width at (98.5, 80.5) is the measured neck between the two letters.
    mstroke(c, [(85.8, 83.0, 4.9), (90.5, 84.3, 5.5), (94.5, 83.5, 4.5),
                (98.5, 80.5, 2.8), (101.5, 78.4, 4.6)])


def draw_c(c):
    # bowl x 92-130, spiral counter centred (112,62)
    # rev 10.  Ribbon, not bowl-minus-groove -- see draw_o.  The `c` is a
    # single stroke that comes in low on the left, sweeps up and over, and
    # winds back INSIDE itself to a fine terminal at (120.5, 64.3), half-width
    # 1.1.  The generated aperture used to be a wedge cut out of the upper
    # right; the reference has no such wedge, it simply never closes there.
    #
    # sec.7's strongly bulbous c terminal (bulb/neck 2.55, the highest in the
    # lockup) is the roll at (115.7, 60.0) -- the last stroke below -- and its
    # 3.2 -> 1.9 half-width is measured, not styled.
    #
    # axis: the whole spiral, foot at (102.7, 77.5) out to the inner terminal
    mstroke(c, [(102.7, 77.5, 5.7), (102.3, 76.5, 5.5), (100.7, 72.5, 5.3),
                (100.0, 68.5, 5.0), (100.3, 64.5, 4.7), (101.3, 60.5, 3.9),
                (103.8, 56.5, 3.5), (107.8, 53.5, 3.1), (111.8, 52.0, 2.6),
                (115.8, 51.5, 2.5), (119.8, 52.7, 2.4), (123.2, 56.3, 1.8),
                (123.5, 60.3, 1.5), (120.5, 64.3, 1.1)])
    # axis: the foot, running left out of the `o`'s foot and round the bottom
    mstroke(c, [(135.8, 69.2, 5.8), (131.8, 71.2, 2.8), (128.3, 73.0, 3.2)])
    mstroke(c, [(128.2, 73.3, 3.2), (126.7, 77.3, 3.4), (123.0, 80.8, 3.9),
                (119.0, 82.5, 4.6), (115.0, 83.0, 5.0), (111.0, 82.7, 5.1),
                (107.0, 80.8, 5.3), (102.8, 77.8, 5.7)])
    # axis: the rolled inner terminal
    mstroke(c, [(115.7, 60.0, 3.2), (113.2, 63.3, 2.8), (114.3, 65.0, 1.9)])


def draw_o(c):
    """
    rev 10.  Same correction as `a`: the reference is a wound ribbon, and the
    counter is what the winding leaves behind, not a trench cut out of a disc.

    The docstring at the top of this file already recorded the evidence --
    "the one closed hole the segmentation finds: x 141-161, y 49-73, area
    224 px in a 21x25 box -- 43 % fill, which is a groove, not a plain bowl" --
    but the code then drew a disc and cut one analytic Archimedean spiral out
    of it, which put the open part of the counter on the wrong side.  The real
    counter is open at the UPPER LEFT (x 140-159, y 49-58) and the ink runs as
    a heavy bar across the middle at y 60.5 before winding down to a core at
    (147.7, 66.3).

    The outer ring alone carries the measured 2.92 thick/thin: half-width 2.2
    over the top at x 156-160 against 6.0-6.2 at the foot on the left.
    """
    # axis: outer ring, top half (right shoulder anticlockwise to the foot)
    mstroke(c, [(163.2, 58.2, 5.1), (162.5, 54.2, 2.8), (159.7, 50.3, 2.2),
                (155.7, 47.8, 2.2), (151.7, 46.5, 2.5), (147.7, 46.5, 2.5),
                (143.7, 47.5, 3.0), (139.7, 50.2, 3.9), (136.7, 54.2, 4.3),
                (135.7, 58.2, 5.3), (135.0, 62.2, 6.0), (135.5, 66.2, 5.6),
                (136.0, 68.8, 6.0)])
    # axis: outer ring, bottom half
    mstroke(c, [(162.5, 59.8, 5.4), (164.7, 63.8, 3.4), (164.5, 67.8, 2.7),
                (162.8, 71.8, 3.2), (159.0, 75.7, 3.3), (155.0, 77.5, 3.5),
                (151.0, 78.0, 4.0), (147.0, 77.7, 4.2), (143.0, 75.8, 4.6),
                (139.0, 72.5, 5.1), (136.2, 69.2, 6.0)])
    # axis: the heavy bar that closes the counter across the middle
    mstroke(c, [(153.7, 60.8, 5.0), (156.5, 61.2, 5.4), (158.2, 60.7, 5.0),
                (162.2, 59.7, 5.4)])
    # axis: the two inner turns winding to the core at (147.7, 66.3)
    mstroke(c, [(156.7, 61.5, 5.2), (157.2, 65.5, 2.6), (154.7, 68.8, 1.2),
                (150.7, 69.3, 1.5), (147.7, 66.5, 2.5)])
    mstroke(c, [(153.3, 60.8, 5.0), (149.3, 60.2, 2.2), (146.0, 62.7, 1.2),
                (147.5, 66.2, 2.5)])
    mstroke(c, [(153.3, 61.2, 4.8), (149.5, 64.8, 1.6), (147.8, 66.2, 2.4)])


def draw_m(c):
    """
    rev 10.  Three stems and two arches, but not the ones that were here.

    The old version put three PARALLEL stems on a 19 px pitch at x 172/191/210,
    each dropping to the fitted baseline, with symmetric arches over them.  The
    reference is not built that way and it ran 9 % heavy at IoU 0.545:
      * the stems are not parallel.  Their lean grows left to right --
        dx/dy = 0.35, 0.22 and 0.74 -- so the third is a long diagonal running
        (204.7, 45.8) to (217.7, 63.3), not a vertical at x 210.
      * the feet do not sit on one baseline.  Measured terminals are
        (169.7, 74.2), (194.0, 67.2) and (217.7, 63.3): 11 px of rise across
        the letter, and the first stem's foot hooks back down-LEFT.
      * the arches are flat, not tall, and they crest at y 44.0 and y 40.2 --
        the second is 4 px higher than the first, which is the letter's slant
        again, not a mistake.
    sec.6 measures `m` at 1.60 thick/thin, the second most monoline glyph in
    the lockup; the half-widths below run 2.2-4.8 away from the junctions,
    ratio 2.2, and the rest of the apparent 1.60 is the junction inscribed
    circles.
    """
    # axis: the thin entry carried over from the `o`
    mstroke(c, [(163.7, 43.7, 1.4), (167.7, 46.2, 3.2), (169.8, 47.3, 4.4)])
    # axis: first stem, leaning right as it falls
    mstroke(c, [(170.2, 47.7, 4.3), (170.5, 51.7, 3.5), (170.5, 55.5, 4.4),
                (173.0, 60.0, 3.1), (174.2, 64.0, 3.4), (175.0, 68.0, 4.0),
                (175.2, 68.8, 4.2)])
    # axis: its foot, which hooks back down and to the left to a fine terminal
    mstroke(c, [(175.0, 69.2, 4.2), (171.3, 72.8, 2.1), (169.7, 74.2, 1.2)])
    # axis: the link back into the `o`'s foot
    mstroke(c, [(170.2, 55.8, 4.3), (166.2, 57.3, 3.7), (163.5, 58.3, 5.0)])
    # axis: first arch -- nearly flat, crest y 43.4.
    # The last three samples are NOT medial-axis samples: the axis has a 2-3 px
    # shoulder here that the 3 px spur prune removes, so from x 177 to x 186
    # the centre and half-height are taken straight from the reference column
    # extents instead (x 180 spans y 39-47, x 182 y 38-49, x 186 y 37-...).
    # It is still measured off the same mask, one instrument coarser.
    mstroke(c, [(170.3, 47.2, 4.3), (174.0, 45.3, 2.9), (177.0, 44.5, 2.2),
                (179.5, 43.6, 3.2), (182.0, 43.4, 4.6), (186.0, 44.4, 6.1)])
    # axis: second stem and its foot
    mstroke(c, [(186.2, 45.0, 6.1), (187.5, 49.2, 4.4), (188.2, 53.2, 3.7),
                (189.2, 57.2, 3.7), (190.0, 61.2, 4.2), (190.7, 65.2, 4.8),
                (191.2, 66.0, 4.7), (194.0, 67.2, 2.7)])
    # axis: second arch (crest y 40.2) running straight on into the third stem
    mstroke(c, [(186.3, 44.6, 6.1), (190.3, 43.3, 3.3), (194.3, 41.8, 2.2),
                (198.3, 40.2, 4.0), (202.3, 41.8, 4.9), (204.7, 45.8, 4.2),
                (206.3, 49.8, 4.0), (208.3, 53.8, 4.0), (209.7, 57.8, 4.7),
                (212.3, 61.7, 5.8), (216.3, 63.3, 5.6), (217.7, 63.3, 5.6)])


def draw_b(c):
    """
    rev 10.  This glyph was in the wrong PLACE, not merely the wrong shape, and
    at IoU 0.362 it was the worst in the lockup.

    The old version drew a solid tilted ellipse for the bowl and put the
    ascender at x 224-232 leaning RIGHT as it rose, with a flag blob at
    x 232-240, y 15-21.  The reference leans the other way and starts 30 px
    further left: compare_script's own measured tarnish zone for the b flag is
    ref_side.jpg (523,487)-(555,519) = mask x 198-230, y 1-33, and
    script_ink.md sec.7 puts the flag terminal at mask (203, 9).  The colour
    layer of this file has been painting tarnish onto bare ground for nine
    revisions because the geometry was not underneath it.

    What the reference actually is (axis + distance transform, see mpath):
      * a THIN ascender, half-width 2.6-3.0, rising from the bowl shoulder at
        (229.5, 36.3) up and to the LEFT;
      * a flag at the top which is a narrow loop the photograph cannot resolve
        as two arms -- it presents as a 3-way junction at (217.6, 14.6) with
        one arm running up-left to a terminal at (203.5, 9.7) and one running
        right to a second terminal at (228.0, 12.8).  Both are drawn;
        script_ink.md sec.7 measures both (bulb 6.3 and 6.0 px).
      * a bowl that is NOT a ring of constant weight: the left stem carries
        half-width 5.9-7.2 (12-14 px) while the arc over the counter drops to
        1.8-2.8 (4-6 px).  That 3.5x is exactly the ratio sec.6 measures for
        `b`, and it is why an ellipse-minus-an-ellipse could never fit it.
    """
    # axis: bowl, thick left stem
    mstroke(c, [(229.7, 36.8, 6.4), (229.8, 40.8, 6.0), (230.8, 44.8, 6.0),
                (231.7, 48.8, 5.9), (233.3, 52.8, 6.7), (234.3, 55.2, 7.2)])
    # axis: bowl, thin arc over the counter
    mstroke(c, [(230.0, 36.3, 6.2), (233.8, 32.7, 3.7), (237.8, 30.3, 2.8),
                (241.8, 30.8, 2.2), (245.7, 33.8, 1.8), (249.2, 37.7, 3.0),
                (252.0, 39.7, 5.0)])
    # axis: bowl, right side down and round the foot
    mstroke(c, [(252.2, 40.2, 5.0), (250.7, 44.2, 2.8), (250.0, 48.2, 2.4),
                (249.0, 52.2, 2.9), (245.7, 55.8, 4.1), (241.7, 56.8, 5.0),
                (237.7, 56.2, 5.8), (234.7, 55.5, 7.0)])
    # axis: the exit that carries the foot back left into the m's last stem
    mstroke(c, [(234.3, 55.5, 7.2), (231.8, 59.5, 6.0), (228.2, 63.0, 3.8),
                (224.2, 64.8, 3.1), (220.2, 64.5, 4.3), (218.0, 63.3, 5.2)])
    # axis: the link from the m's third stem down into that exit
    mstroke(c, [(220.5, 59.3, 2.5), (218.0, 63.0, 5.2)])
    # axis: ascender -- terminal at (203.5, 9.7) through the flag junction and
    # on down into the bowl shoulder
    mstroke(c, [(203.5, 9.7, 3.0), (207.5, 12.0, 2.4), (211.5, 12.8, 3.0),
                (215.5, 14.0, 4.0), (217.7, 15.0, 4.2), (218.7, 19.0, 3.3),
                (220.3, 23.0, 2.6), (221.7, 27.0, 2.8), (224.3, 31.0, 2.9),
                (227.8, 34.8, 5.0), (229.5, 36.3, 6.2)])
    # axis: the flag's second arm, junction out to its terminal at (228.0, 12.8)
    mstroke(c, [(217.8, 14.5, 4.2), (220.0, 13.5, 3.5), (224.0, 12.5, 2.5),
                (228.0, 12.8, 2.1)])


def draw_i(c):
    """
    rev 10.  The `i` is ONE connected stroke in the reference, not a stem with
    a detached dot floating over it.

    The old version drew the dot as an isolated tilted ellipse at (255.6, 23.4)
    and started the stem 8 px below it at y 31, leaving bare ground across
    y 24-30 where the reference has a continuous 4 px neck.  It also drew the
    stem far too light: the measured half-width at the foot is 6.7 (13.4 px),
    which is the largest inscribed circle anywhere in `Tacombi` outside the T,
    and is what sec.7's "i dot, bulb 13.4" is actually pointing at.

    Measured: a fat horizontal dash from (245.8, 20.5) to (258.5, 19.7) -- the
    dot -- necking to half-width 2.2 at (252.8, 25.3), swelling to 6.7 at
    (256.0, 38.3), then the exit flourish looping right and back up to a fine
    1.8 terminal at (274.0, 39.2).  sec.7 measures that exit at bulb/neck 0.75,
    i.e. it tapers into the tip rather than bulbing, and it does so here.
    """
    # axis: the dot, which is a dash lying almost flat across the stem head
    mstroke(c, [(248.0, 20.6, 2.0), (250.5, 20.9, 3.6), (253.0, 21.0, 4.8),
                (254.5, 20.5, 4.5), (258.5, 19.7, 2.9)])
    # axis: stem -- neck at y 25, then swelling into the foot
    mstroke(c, [(253.0, 21.3, 4.6), (252.8, 25.3, 2.2), (253.5, 29.3, 3.3),
                (256.3, 32.8, 5.5), (256.2, 37.2, 6.2), (256.0, 38.3, 6.6)])
    # axis: the exit flourish
    mstroke(c, [(256.2, 38.7, 6.6), (259.0, 42.7, 5.2), (261.3, 46.7, 4.9),
                (265.0, 49.7, 5.1), (269.0, 49.3, 4.5), (272.8, 46.7, 2.4),
                (274.3, 42.7, 1.6), (274.0, 39.2, 1.8)])


# rev 10.  'Senor' is no longer drawn from eyeballed primitives.
#
# For nine revisions this word was placed by eye and excluded from fitting,
# on the recorded belief that it "is tarnished to green-black and cannot be
# segmented".  That belief was tested in rev 10 and is false: the word is
# invisible in LUMA (Michelson contrast 0.132) but obvious in CHROMATICITY --
# the red ground carries B = 6.0 +/- 3.6 DN while the word carries B = 21-81.
# Segmented properly it is 934 px of real ink (SPEC 10.20).
#
# senor_trace.py carries the reconstruction: the measured mask's medial axis,
# smoothed to 0.20 source px RMS, with the half-width taken from the Euclidean
# distance transform at every sample.  Every half-width is measured; none is
# invented.  It scores IoU 0.913 against the measured mask where the eyeballed
# version scored 0.089.
#
# The tarnish is warm brown, not green-black: darkest quartile a* +14.0 against
# lightest +6.9, a 6-sigma WARM shift.  That is applied in the RGB layer in
# main(), not here -- this function emits coverage only.
import senor_trace


def draw_senor(c):
    """Delegate to the measured reconstruction (senor_trace.draw_senor)."""
    senor_trace.draw_senor(c)

def build():
    c = Canvas()
    draw_T(c)
    draw_a(c)
    draw_c(c)
    draw_o(c)
    draw_m(c)
    draw_b(c)
    draw_i(c)
    draw_senor(c)
    return c.alpha()


def _lockup(c):
    draw_T(c); draw_a(c); draw_c(c); draw_o(c)
    draw_m(c); draw_b(c); draw_i(c); draw_senor(c)


def build_hi():
    """The lockup at the DRAWN resolution, MW*SS x MH_TOT*SS.  Same strokes as
    build(); only the reduction differs.  SPEC 10.121."""
    c = Canvas()
    _lockup(c)
    return c.alpha_box(1)


def senor_only():
    """Coverage of the 'Senor' word alone -- used as a tarnish zone mask."""
    c = Canvas()
    draw_senor(c)
    return c.alpha()


def senor_only_hi():
    """senor_only() at the drawn resolution.  The tarnish zone has to be cropped
    and resized on the SAME grid as the ink or the tarnish slides off the word."""
    c = Canvas()
    draw_senor(c)
    return c.alpha_box(1)


# ------------------------------------------------------------------- ink colour
#
# rev 10.  The generator emitted a CONSTANT (214, 216, 218) with every bit of
# shape carried in alpha.  Three things were wrong with that and all three are
# measured (SPEC 10.20, analysis in measure/script_ink.md):
#
#   1. VALUE.  The reference ink is not near-white.  Untarnished silver, taken
#      from PSF-safe stroke interiors of T/a/c/o/m, means (127.4, 124.9, 130.0)
#      -- 89 DN darker than what was being emitted.  Expressed as a ratio that
#      survives a change of exposure: the silver sits at 0.293 of the adjacent
#      cream bodywork's LINEAR luminance in ref_side.jpg (sRGB 125.8 against
#      219.1).  SILVER below is that ratio carried onto CREAM's albedo, at the
#      measured chromaticity.  T1_SILVER overrides it for calibration.
#   2. MOTTLE.  Real silver leaf is not flat.  Genuine mottle on untarnished
#      silver is 7.4 DN std against an imaging noise floor of 1.5 DN -- 5.9 %
#      relative.  It has NO dominant period (the power spectrum falls
#      monotonically), so this is filtered noise, not a pattern.  It is
#      DIRECTIONAL: correlation length 13-16 px along the stroke direction
#      against 3.5-5.0 px across (z = +6.5 at 150 deg against an isotropic null
#      run through the same mask).  The long axis lies within ~10 deg of the
#      baseline, which rises 11.6 deg -- it is brush direction.
#   3. TARNISH.  The dark material is a different material, not a darker
#      texture, and it is not spread evenly.  It is concentrated on 'Senor',
#      the b flag and ascender, the i dot, and part of the swash: per-channel
#      std runs 26-41 on b and 15-27 on the swash, against 5.9-9.0 on T/a/m.
#      And it is WARM, not green-black: darkest-quartile a* +14.0 against
#      lightest +6.9, a 6-sigma warm shift.  'Senor' median is (85, 46, 35)
#      against clean silver (126, 123, 127) -- per channel (0.675, 0.374,
#      0.276).
#
# NOT applied here, deliberately: the ~15 DN smooth gradient across the lockup.
# That is the photograph's own lighting falling across the flank; baking it in
# would light the model twice.
CREAM_LIN = (0.6172, 0.6308, 0.5776)     # t1_mats.CREAM, linear
SILVER_CHROMA = (127.4, 124.9, 130.0)    # measured sRGB of clean silver

# CORRECTION MADE WITHIN rev 10, kept visible because the reasoning is the
# trap and not the number.
#
# The first attempt read "the silver sits at 0.293 of the cream's linear
# luminance in ref_side.jpg" and set the ALBEDO to 0.293 x CREAM.  It rendered
# as dull blue-grey paint.  The error: that 0.293 is a ratio of RENDERED
# values between a near-mirror METAL and a diffuse dielectric, and those two
# do not scale together when the environment changes.  Silver leaf is dark in
# the reference BECAUSE the reference is open shade under an absorbing canopy
# with one lateral opening -- the leaf is reflecting a dark room.  Put the same
# leaf under a white studio softbox and it is bright, and that is not an error,
# it is what a photograph of the real vehicle in a white studio would show.
#
# This is the same class of mistake SPEC 10.12 already records against the
# flank saturation: "no beauty pixel of a dielectric under a white softbox
# reaches the albedo saturation".  The rule generalises -- a rendered ratio is
# only an albedo ratio between two surfaces of the SAME class under the SAME
# light.
#
# So the albedo is set from what the material IS: weathered, varnished silver
# leaf, luminance 0.66 (fresh leaf is ~0.90; this is chalked and 60 years old),
# carrying the measured chromaticity.  What the photograph DOES fix, because
# they are internal to one surface under one light, are the ratios kept below:
# the mottle amplitude, the tarnish distribution, and the 0.43 that separates
# tarnished ink from clean.
SILVER_Y = float(os.environ.get("T1_SILVER_Y", 0.66))    # linear luminance
TARNISH_K = (0.675, 0.374, 0.276)        # 'Senor' median / clean silver median
# ===================================================== rev 46, W3, SPEC 10.120
# "SENOR TACOMBI STILL ISN'T CLEARER" -- AND IT IS *SENOR* THAT ISN'T.
#
# His third report of this script.  Every prior revision measured ONE Michelson
# figure over the WHOLE script and stalled on a contradiction: the ledger's
# finding 19 says the ink is already too LIGHT against its own measured target,
# so darkening it toward that target makes legibility WORSE, and the two
# findings pull opposite ways.
#
# MEASURING THE TWO WORDS SEPARATELY DISSOLVES THE CONTRADICTION.  Michelson
# against the red each sits on:
#
#                 photographed        built rev 45
#     Tacombi     0.4673 +- 0.0009    0.4480          <- right, 4 % low
#     Senor       0.1922 +- 0.0060    0.0711          <- 2.7x TOO DARK
#
# Photographed on ref_side.jpg -- the frame the script was traced from -- over
# 6 thresholds x 4 crop windows.  'Tacombi' was never the problem.  'Senor' is
# fully tarnished by TARNISH_K and renders at a luminance of 95 against a ground
# of 79: it is not low-contrast, it is very nearly INVISIBLE.  He named the word.
#
# WHY THE LIFT IS A DECLARED DEPARTURE, AND EXACTLY HOW BIG A ONE.
# TARNISH_K is a MEASURED ratio, 'Senor' median over clean silver median, and
# the generator reproduces it faithfully: built Senor/Tacombi = 0.451 against a
# photographed 0.496.  Correcting that ratio alone is a pure fix and it is worth
# having -- but it only reaches Michelson 0.1385, still short of the
# photographed 0.1922.  THE REST IS NOT THE INK.  It is the ground: the built
# body red renders 11 % brighter relative to the ink than the photograph's
# (ground/Tacombi 0.376 built against 0.338 photographed), which is LEDGER
# FINDING W6 -- body red G/R 0.455 built against 0.223 +- 0.066 photographed,
# 3.5 sigma -- and W6 IS BLOCKED ON THE OWNER because half of it is the white
# cyclorama he supplied as the bar.
#
# So the lift is solved to land on the PHOTOGRAPHED CONTRAST 0.1922 rather than
# on the photographed ink ratio, and that over-lifts the ink to Senor/Tacombi
# 0.554 against the photographed 0.496.  THAT 0.058 IS THE DEPARTURE.  It is
# taken because he has now asked three times, it is recorded here rather than
# buried, and it has a retirement condition: WHEN W6'S PAINT IS SETTLED,
# RE-DERIVE THIS LIFT.  It will shrink, and if the red lands where the
# photograph puts it the departure goes to zero on its own.
#
# The lift is DERIVED from the target, not typed (SPEC 10.25), so it re-solves
# if the silver albedo, the mottle or the body red ever move.
SENOR_MICHELSON = 0.1922                 # ref_side.jpg, +-0.0060, 6 th x 4 windows
BODY_RED_L = 0.2126 * 196 + 0.7152 * 49 + 0.0722 * 36    # t1_mats body red sRGB
MOTTLE_REL = 0.059                       # 7.4 DN on a mean of 125.8
MOTTLE_LONG = 14.5                       # mask px, measured 13-16
MOTTLE_SHORT = 4.2                       # mask px, measured 3.5-5.0
MOTTLE_ANG = -11.6                       # deg; the baseline's rise
# tarnish patches, mask-space boxes, from the rolling-ball zones in sec.1
TARNISH_ZONES = [                        # (x0, y0, x1, y1, strength)
    (198, 1, 230, 33, 0.62),             # b flag + ascender
    (240, 11, 258, 28, 0.62),            # i dot
    (4, 26, 118, 56, 0.34),              # part of the swash
]


def _srgb_to_lin(v):
    v = np.asarray(v, float) / 255.0
    return np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)


def _lin_to_srgb(v):
    v = np.clip(np.asarray(v, float), 0, 1)
    return 255.0 * np.where(v <= 0.0031308, v * 12.92,
                            1.055 * v ** (1 / 2.4) - 0.055)


def _luma(lin):
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def silver_albedo():
    """Base colour for the ink: measured chromaticity at the measured ratio."""
    env = os.environ.get("T1_SILVER")
    if env:
        return np.array([float(t) for t in env.split(",")], float)
    chroma = _srgb_to_lin(SILVER_CHROMA)
    return _lin_to_srgb(chroma * (SILVER_Y / _luma(chroma)))


def mottle_field(h, w, px_per_mask):
    """Anisotropic filtered noise: no dominant period, brush-directional."""
    from scipy import ndimage as nd
    rng = np.random.default_rng(20260810)
    # 1/e length of a Gaussian-filtered white field is 2*sigma
    s_long = MOTTLE_LONG * px_per_mask / 2.0
    s_short = MOTTLE_SHORT * px_per_mask / 2.0
    pad = int(3 * s_long)
    n = rng.standard_normal((h + 2 * pad, w + 2 * pad)).astype(np.float32)
    # filter in the brush frame, then rotate the frame onto the baseline
    n = nd.gaussian_filter(n, sigma=(s_short, s_long), mode='reflect')
    n = nd.rotate(n, MOTTLE_ANG, reshape=False, order=1, mode='reflect')
    n = n[pad:pad + h, pad:pad + w]
    sd = n.std()
    return n / sd if sd > 0 else n


# --------------------------------------------------------------------- output
def main():
    a = build()
    np.save("/tmp/gen_alpha.npy", a)

    ys, xs = np.nonzero(a > 32)
    print("generated ink bbox  x %d-%d  y %d-%d   (%dx%d, AR %.3f)"
          % (xs.min(), xs.max(), ys.min(), ys.max(),
             xs.max() - xs.min() + 1, ys.max() - ys.min() + 1,
             (xs.max() - xs.min() + 1) / (ys.max() - ys.min() + 1)))
    print("reference  ink bbox  x %d-%d  y %d-%d   (%dx%d, AR %.3f)"
          % (INK_BBOX[0], INK_BBOX[2], INK_BBOX[1], INK_BBOX[3],
             INK_BBOX[2] - INK_BBOX[0] + 1, INK_BBOX[3] - INK_BBOX[1] + 1,
             (INK_BBOX[2] - INK_BBOX[0] + 1) / (INK_BBOX[3] - INK_BBOX[1] + 1)))

    # crop to the generated ink bbox and emit at OUT_W
    #
    # SPEC 10.121 (rev 47).  THE BBOX IS STILL FOUND IN MASK SPACE -- it must
    # be, because every stored figure, threshold and comparison in this project
    # is in mask space -- but the raster that gets CROPPED AND RESIZED is now
    # the one Canvas actually drew, at SS.  Before this, the 271-px-wide mask
    # crop was LANCZOS-magnified 15.11x to 4096; now the 3252-px-wide drawn
    # crop is resized 1.260x.  Same geometry, same bbox, same output size --
    # twelve times the real detail.
    x0, x1 = xs.min(), xs.max()
    y0, y1 = ys.min(), ys.max()
    sub = a[y0:y1 + 1, x0:x1 + 1]                    # mask space: ppm, prints
    hi = build_hi()[y0 * SS:(y1 + 1) * SS, x0 * SS:(x1 + 1) * SS]
    h = int(round(OUT_W * sub.shape[0] / sub.shape[1]))
    al = np.array(Image.fromarray(hi.astype(np.uint8))
                  .resize((OUT_W, h), Image.LANCZOS))
    print("emit: mask crop %dx%d (%.2fx to OUT_W) -> drawn crop %dx%d (%.3fx)"
          % (sub.shape[1], sub.shape[0], OUT_W / sub.shape[1],
             hi.shape[1], hi.shape[0], OUT_W / hi.shape[1]))

    # ---- ink colour: measured silver, mottled, with the tarnish where the
    #      photograph puts it.  See the block above main() for provenance.
    ppm = OUT_W / float(sub.shape[1])            # output px per mask px
    base = silver_albedo()
    rgb = np.repeat(np.repeat(base[None, None, :], h, 0), OUT_W, 1)

    # 1. mottle -- multiplicative, achromatic (measured da* = +0.20 +/- 0.24
    #    within clean silver, i.e. under 1 sigma: the mottle has no colour)
    m = 1.0 + MOTTLE_REL * mottle_field(h, OUT_W, ppm)
    rgb = rgb * m[..., None]

    # 2. tarnish.  'Senor' is fully tarnished; the b flag, the i dot and part
    #    of the swash are blotched.  Blotches are a second, coarser noise field
    #    thresholded inside the measured zones, so the tarnish reads as patches
    #    of a different material rather than as a darker paint.
    from scipy import ndimage as nd
    # SPEC 10.121: cropped and resized on the SAME grid as the ink above.
    sen = senor_only_hi()[y0 * SS:(y1 + 1) * SS, x0 * SS:(x1 + 1) * SS]
    sen = np.array(Image.fromarray(sen.astype(np.uint8))
                   .resize((OUT_W, h), Image.LANCZOS)).astype(np.float32) / 255.0
    tw = np.clip(sen * 1.15, 0, 1)               # 'Senor': full strength

    rng = np.random.default_rng(731)
    blot = nd.gaussian_filter(rng.standard_normal((h, OUT_W)).astype(np.float32),
                              sigma=2.2 * ppm, mode='reflect')
    blot = (blot - blot.mean()) / (blot.std() + 1e-9)
    for zx0, zy0, zx1, zy1, s in TARNISH_ZONES:
        gx0 = int(round((zx0 - x0) * ppm)); gx1 = int(round((zx1 - x0) * ppm))
        gy0 = int(round((zy0 - y0) * ppm)); gy1 = int(round((zy1 - y0) * ppm))
        gx0, gy0 = max(gx0, 0), max(gy0, 0)
        gx1, gy1 = min(gx1, OUT_W), min(gy1, h)
        if gx1 <= gx0 or gy1 <= gy0:
            continue
        z = np.zeros((h, OUT_W), np.float32)
        z[gy0:gy1, gx0:gx1] = 1.0
        z = nd.gaussian_filter(z, sigma=1.2 * ppm, mode='constant')
        tw = np.maximum(tw, z * s * np.clip(blot * 0.7 + 0.45, 0, 1))
    tw = np.clip(tw, 0, 1)[..., None]

    # ------------------------------------------- rev 46, W3: SOLVE THE LIFT
    # Luminance is LINEAR in the lift -- K' = K + (1-K)*lift gives
    # L(lift) = L_tarnished + lift * (L_clean - L_tarnished) -- so one solve,
    # no iteration, and it re-derives from whatever the albedo and mottle are.
    def _lum(c):
        return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]

    _K0 = np.array(TARNISH_K, float)
    _zone = (tw[..., 0] > 0.6) & (al > 96)
    if _zone.sum() > 100:
        _Lc = float(_lum(rgb)[_zone].mean())
        _Lt = float(_lum(rgb * _K0)[_zone].mean())
        _Ltar = BODY_RED_L * (1.0 + SENOR_MICHELSON) / (1.0 - SENOR_MICHELSON)
        TARNISH_LIFT = float(np.clip((_Ltar - _Lt) / max(_Lc - _Lt, 1e-6), 0.0, 1.0))
        print("  Senor lift: clean L %.1f, fully tarnished L %.1f, target L %.1f "
              "-> lift %.4f" % (_Lc, _Lt, _Ltar, TARNISH_LIFT))
    else:
        TARNISH_LIFT = 0.0
        print("  Senor lift: NO TARNISH ZONE FOUND -- lift 0")
    _K = _K0 + (1.0 - _K0) * TARNISH_LIFT
    rgb = rgb * (1.0 - tw) + rgb * _K * tw

    rgb = np.clip(rgb, 0, 255).astype(np.uint8)
    out = np.dstack([rgb, al])
    os.makedirs(TEX, exist_ok=True)
    Image.fromarray(out).save(os.path.join(TEX, "senor.png"))
    ink = al > 96
    lm = (0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2])
    clean = ink & (tw[..., 0] < 0.05)
    print("wrote tex/senor.png  %dx%d  AR %.4f" % (OUT_W, h, OUT_W / h))
    print("  base albedo sRGB %s" % np.round(base, 1))
    print("  clean-silver luma %.1f +/- %.1f  (relative std %.3f, measured 0.059)"
          % (lm[clean].mean(), lm[clean].std(),
             lm[clean].std() / max(lm[clean].mean(), 1e-9)))
    tar = ink & (tw[..., 0] > 0.6)
    if tar.sum():
        print("  tarnished luma    %.1f  (%.1f%% of ink; measured 'Senor' is "
              "0.43x clean)" % (lm[tar].mean(), 100.0 * tar.sum() / ink.sum()))
    return OUT_W / h


def glyph_sheet(name, scale=8, pad=6):
    """
    Magnified four-panel view of ONE compare_script box:
    photograph | reference ink | generated | overlay.

    This is the instrument the rev-10 pass was driven by.  Reading an IoU
    number tells you a glyph is wrong; it does not tell you whether it is the
    wrong weight, the wrong path or in the wrong place, and those need
    different fixes.  The b looked like a weight problem in the table and was
    a 30 px placement error on the sheet.
    """
    import compare_script as C
    box = dict((b[0], b[1:]) for b in C.BOXES)
    if name not in box:
        raise SystemExit("--glyph: pick one of %s" % ", ".join(sorted(box)))
    x0, y0, x1, y1 = box[name]
    G = build() > 96
    R = C.ref_mask()
    a = max(y0 + YPAD - pad, 0)
    b = min(y1 + YPAD + pad, G.shape[0])
    xa, xb = max(x0 - pad, 0), min(x1 + pad, G.shape[1])
    g, r = G[a:b, xa:xb], R[a:b, xa:xb]
    h, w = g.shape
    ph = np.array(Image.open("ref_side.jpg").convert("RGB"))
    ph = ph[C.CY0 + a:C.CY0 + a + h, X0 + xa:X0 + xa + w]
    tiles = [ph.astype(np.uint8),
             np.dstack([r * 255] * 3).astype(np.uint8),
             np.dstack([g * 255] * 3).astype(np.uint8),
             np.dstack([r * 255, g * 255, (r & g) * 255]).astype(np.uint8)]
    ox, oy = xa, a - YPAD
    out = []
    for t in tiles:
        big = np.kron(t, np.ones((scale, scale, 1), np.uint8))
        for i in range(w):                      # 10 px mask-space grid
            if (ox + i) % 10 == 0:
                big[:, i * scale] = np.maximum(big[:, i * scale], 70)
        for j in range(h):
            if (oy + j) % 10 == 0:
                big[j * scale] = np.maximum(big[j * scale], 70)
        out.append(big)
    sep = np.full((h * scale, 6, 3), 40, np.uint8)
    sheet = out[0]
    for t in out[1:]:
        sheet = np.hstack([sheet, sep, t])
    os.makedirs("out", exist_ok=True)
    p = "out/glyph_%s.png" % name.replace(" ", "_").replace("+", "")
    Image.fromarray(sheet).save(p)
    print("wrote %s   photo | ref | gen | overlay (red=ref only, green=gen "
          "only, white=both)" % p)
    print("  window mask x %d..%d  y %d..%d at %dx, grid every 10 mask px"
          % (ox, ox + w - 1, oy, oy + h - 1, scale))


if __name__ == "__main__":
    if "--glyph" in sys.argv:
        glyph_sheet(sys.argv[sys.argv.index("--glyph") + 1])
        sys.exit(0)
    ar = main()
    if "--compare" in sys.argv:
        import compare_script
        compare_script.run()
