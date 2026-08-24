"""
senor_trace.py -- the word `Senor` of the flank lockup, reconstructed by
medial-axis tracing of the MEASURED ink mask.

READ `THE TILDE, REV 59` BELOW BEFORE YOU TRUST ANY NUMBER IN THIS HEADER.
Everything between `HOW THE GEOMETRY WAS DERIVED` and `ACCURACY ACHIEVED`
describes the rev-9 trace and its 934 px reference.  THAT REFERENCE WAS
MISSING THE TILDE.  It has been re-baked (1062 px), the tilde is drawn, and
the figures in `ACCURACY ACHIEVED` are superseded by the rev-59 block.

WHY THIS FILE EXISTS
`script_gen.py` draws `Tacombi` from control points read off ref_side.jpg by
eye, and it drew `Senor` the same way -- except that `Senor` is tarnished to a
warm brown-black and is nearly invisible in luma, so nobody could check the
result.  HANDOFF_rev9 sec.4.4 concluded the word "cannot be segmented", placed
it from the visual, and excluded it from IoU fitting.  It scored 0.089.

That conclusion has been refuted by measurement.  The red ground carries
B = 6.0 +- 3.6 DN while every part of `Senor` carries B = 21-81 DN, so the word
segments cleanly in chromaticity even though it is invisible in brightness.
The segmentation is documented in /home/claude/work/measure/script_ink.md sec.1
and sec.8; its output is out/script_mask.png (296x136, origin (318,462) in
ref_side.jpg) plus the per-glyph label map out/glyph_lab.npy.  `Senor` is
labels 1-5 of that map: 934 +- 110 ink px, ref_side.jpg x 331-413, y 474-513.

THE COORDINATE FRAME
Everything below is in script_gen.py MASK SPACE -- ref_side.jpg pixels offset
to (X0, Y0) = (325, 486), y increasing downward.  In that frame `Senor`
occupies

    x 6 .. 88,  y -12 .. +27          (83 x 40 px)

i.e. it extends 12 px ABOVE the old canvas top.  That is why the generated
lockup used to be 99 px tall against the reference's 114: the top third of the
`S` was never drawn at all.  draw_senor() adds `ypad` to every y it emits, so
the caller must pass ypad >= 12 for the whole word to land on the canvas.

HOW THE GEOMETRY WAS DERIVED  (no control point in this file was placed by eye
-- rev 59: still true of every coordinate, INCLUDING the tilde, whose points
are a distance-transform ridge.  What WAS chosen rather than measured is the
window the tilde was cut out of, and it was chosen by ablation with the sweep
printed -- see THE TILDE, REV 59.)
  1. Crop labels 1-5 of glyph_lab.npy -- 934 px, 6 connected components.
  2. Upsample x6 (bilinear on the indicator), Gaussian sigma = 0.55 SOURCE px
     (3.3 px at 6x), rethreshold at 0.5.  That sigma is chosen to erase the
     +-0.5 px pixel-quantisation staircase of the source mask and nothing
     coarser: it costs 0.8 % of the area (934 -> 926.8 px-equivalent) and it
     collapses the medial-axis branch count from 108 (at sigma = 0.40) to 25.
     The 108-branch version is the mask's compression noise, not a letterform.
  3. True MEDIAL AXIS (skimage.morphology.medial_axis, rng=0) with its exact
     distance map.  The morphological skeleton was tried first and rejected:
     its union-of-discs reconstruction recovers only 0.917 of the shape
     (area 881 vs 934) because thinning omits the medial branches that fill
     convex shoulders.  The true medial axis reconstructs at 0.964 / area 931.
  4. Junction-clustered graph; leaf branches shorter than 3.0 SOURCE px pruned
     iteratively, never to the point of deleting a component.
  5. Half-width = the distance transform sampled along each branch.  Nothing is
     added to it -- see NEAR-MONOLINE below.
  6. Each branch resampled to uniform arc length (0.25 source px) and fitted
     with a cubic smoothing spline.

SMOOTHING TOLERANCE -- STATED, AND WHY IT IS NOT 1.5-2 px
  Axis:  0.20 source px RMS deviation from the raw medial axis
         (0.60 px peak over all 26 branches).
  Half-width profile: 0.10 source px RMS.
  Polyline point spacing: 1.25 source px.  Coordinates rounded to 0.01 px
  (rounding to 0.01 costs 0.0001 IoU; rounding to 0.1 costs 0.006).

  The brief asked for ~1.5-2 source px, "just above the PSF".  That conflates
  two different things and I measured the difference rather than assume it.
  The 2.07 px PSF is the resolution of the BOUNDARY.  The axis is the mean of
  two boundaries and is localised better, and step 2 above has already
  low-passed the boundary.  Measured on the 13 medial-axis branches longer than
  6 px: the residual lateral roughness against an arc-length Gaussian low-pass
  is 0.062 px RMS at sigma_s = 0.5 px (range 0.050-0.070) and 0.140 px RMS at
  sigma_s = 1.0 px (range 0.109-0.159).  There is no sub-resolution wiggle left
  to remove -- the sigma = 0.55 px boundary filter already took it.  A 1.5-2 px
  tolerance is 10x that floor and it deletes real curvature: it flattens the
  `S` spine and costs 0.09 IoU overall, 0.21 on the `S` alone.  Sweep, all
  other parameters fixed (IoU at the compare_script threshold):

      axis tol (px RMS)  0.15   0.20   0.30   0.50   0.75   1.00   1.50
      peak deviation     0.60   0.60   0.60   1.02   1.61   1.81   1.81
      whole word         .913   .913   .912   .869   .840   .821   .821
      `S` alone          .913   .913   .913   .837   .759   .708   .708

  The other two smoothing knobs behave the same way -- both are set where the
  measurement puts them, not where the IoU peaks:

      spur prune (px)  1.5    2.0    3.0*   4.0    6.0
      whole word       .932   .926   .913   .913   .888
      boundary sigma   0.40   0.55*  0.70
      whole word       .935   .913   .882          (* = value used)

  sigma = 0.40 scores higher and is still wrong: at 0.40 the medial axis breaks
  into 108 branches chasing the mask's pixel staircase.  3.0 px spur pruning is
  the brief's figure and is kept; 1.5 px would buy 0.019 IoU by keeping spurs
  that are only 2-3 boundary pixels long, i.e. below the stated resolution.

COUNTERS
  The mask has exactly two enclosed holes, 10 px each, at mask-space
  x 40.4-43.7 y 12.8-15.7 and x 47.1-49.9 y 11.2-14.6.  Both are reproduced
  twice over: the medial axis loops around them, so the disc sweep leaves them
  open by construction, AND their contours are emitted as explicit c.cut()
  polygons derived the same way (upsample, smooth, spline at the same
  tolerance).  The cuts are therefore nearly redundant here -- they move the
  whole-word IoU by 0.0019 -- but they make the counters survive any later
  rescaling of the half-widths.

  One caveat on naming.  They are usually called the counters of `e` and `o`,
  and that is what they look like, but `e`, `n~` and `o` are fused into one ink
  mass here and the geodesic glyph labelling of script_ink.md sec.2 (uncertain
  by +-2-3 px at joins) puts both holes inside `n~`'s territory: they fall
  between `e`'s bbox (x 28-39) and `o`'s (x 51-66).  The data below therefore
  tags them `ntilde`, which is what was measured, not what they are called.
  At 10 px each they are at the edge of what this photograph resolves;
  script_ink.md sec.8 lists `Senor` interior detail as NOT MEASURABLE, so treat
  the counter shapes as indicative and their existence as solid.

NEAR-MONOLINE -- nothing invented
  script_ink.md sec.6 measures `Senor` as nearly monoline (S 2.06, n~ 1.50,
  e 1.05, r 1.05, o 1.00) and warns the ratios are at the quantisation limit.
  This file adds no pen modulation whatsoever: every half-width is the measured
  distance transform.  Trimmed 3 px back from junctions and terminals, the
  within-branch thick/thin ratio has median 1.25 and the within-branch width
  s.d. is 0.32 px -- monoline, as measured.  Pooled stroke width p5/p50/p95 =
  1.96 / 4.45 / 6.84 px against sec.0.1's "4-6 px in `Senor`".  The wider
  values are the inscribed circles at junctions, which is geometry, not weight.

WHAT THIS REPRODUCES, INCLUDING ITS WARTS
  The mask is a segmentation of 4-6 px strokes at a 2.07 px PSF and it arrives
  in SIX disconnected pieces (252 / 332 / 16 / 258 / 61 / 15 px).  The most
  visible break is the `S`: its spine drops below the chromaticity threshold,
  so the letter comes through as an upper C (_STROKES[0]), a detached lower
  bowl (_STROKES[1]) and a 15 px tail fragment (_STROKES[2]).  This trace
  reproduces those breaks, because they are what was measured.  They are almost
  certainly artefacts of the tarnish and not of the paint -- the real letter is
  surely continuous -- so if this ever has to look right rather than measure
  right, bridge _STROKES[0]->[1]->[2] and re-score.  Doing it now would be
  inventing ink the photograph does not show.

ACCURACY ACHIEVED  (rev 9 -- SUPERSEDED AT REV 59, see THE TILDE, REV 59)
  RETRACTED, NOT DELETED: every figure in this block is scored against the
  934 px bake that had no tilde in it.  `python3 senor_trace.py` no longer
  prints any of them.  The live figures are in the rev-59 block below.

  IoU against the 934 px measured `Senor` mask, rasterised through a faithful
  clone of script_gen.Canvas at SS=12 and thresholded the way compare_script
  does (alpha > 96):

      whole word 0.913   S 0.913   e 0.843   n~ 0.898   o 0.866   r 0.924

  (0.918 / 0.918 / 0.858 / 0.908 / 0.856 / 0.907 at a 50 % coverage threshold,
  alpha > 127; the choice of threshold is worth 0.005.)

  For scale, on this word a 1 px shift of the reference against ITSELF scores
  0.75 (x), 0.71 (y), 0.68 (diagonal) -- a cost of 0.25-0.32, against the 0.14
  quoted for the lockup as a whole.  `Senor`'s strokes are 4-6 px where
  `Tacombi`'s are 8-16, so misregistration is punished about twice as hard
  here.  The 0.6-0.75 band that was set as "what a faithful redraw scores" was
  calibrated on hand-placed control points; a medial-axis trace of a measured
  mask is a different instrument and legitimately does better.

  Read the number for what it is: this is a faithful redraw OF THE MASK, and
  the mask itself carries +-12 % area uncertainty on `Senor` and about +-1 px
  on the outline (script_ink.md sec.8).  Agreement with the mask is not the
  same as agreement with the paint.

THE TILDE, REV 59 -- THE ONE STROKE THIS FILE NEVER DREW
  THE DEFECT.  The `n~` had no tilde.  `_STROKES` carried two remnants of one
  and nothing else: a 3 px vertical stub at (45.33, 7.33)..(45.00, 10.33) and a
  lone inscribed disc at (51.67, 4.33, 1.67), which draw_senor() has a special
  branch for.  That is the signature of SPUR_PRUNE_PX = 3.0 eating a stroke
  that arrived thin and in fragments -- and the header above already records
  the source mask arriving in SIX pieces, two of them 16 and 15 px.

  WHY NOTHING CAUGHT IT.  The trace graded itself against a mask baked into
  this file from out/glyph_lab.npy, and THAT mask had no tilde either.  Two
  reference masks over the identical window, mask x 6..88 / y -12..27:

      senor_trace._ref_mask()      934 px    (what the trace was fitted to)
      compare_script.ref_mask()   1176 px    (what the live gate scores against)
      both 930, trace-only 4, live-only 246, IoU 0.788

  The trace's was a strict SUBSET.  Of the 246: 118 px the tilde, 88 px the
  Tacombi swash crossing rows 23..27 (not this trace's ink), the rest edge
  slop.  Nothing in the repo compared the two, so the trace reported 0.913
  while the owner reported he could not read the word.  check_ref_agrees()
  is that comparison, and it is now a row.

  THE INK IS REAL, AND THIS IS NOT A12.  In mask rows y 1..9, cols x 35..63
  (ref_side.jpg x 360-388, y 487-495) compare_script.ref_mask() carries 186 px
  against the pre-rev-59 generator's 73 -- less than half of it drawn.  Mean RGB
  over that rectangle is (76.1, 40.5, 34.8) against clean red 30 rows above, same
  columns, at (64.0, 13.8, 9.3): G +27 and B +26 on a red channel that is if
  anything HIGHER, which is the tarnish signature script_gen.TARNISH_K already
  documents, not a shadow.  Redness 0.279 against a red ground of
  0.604 +- 0.045 -- 7.3 sigma.  31.4 % of that rectangle passes the strict
  T_SILVER = 0.1409 rule against 10.0 % of the whole `Senor` box.  A12 forbids
  inventing ink the photograph does not show; this restores ink the photograph
  DOES show and a superseded segmentation dropped.

  ONE CORRECTION TO THE BRIEF THAT SENT ME HERE, since it will be quoted again:
  it put that band at "reference 230 px, generated 115", redness 0.290 against
  0.687 +- 0.076 (5.2 sigma), and 47.4 % / 28.0 % under T_SILVER.  Re-measured
  over the window it names, on this tree, the figures above are what print.
  THE CONCLUSION IS UNCHANGED AND IF ANYTHING STRONGER (7.3 sigma, not 5.2) --
  but the figures moved, so they are corrected here rather than transcribed.

  THE DEPARTURE, DECLARED: NO skimage.  Step 3 of HOW THE GEOMETRY WAS DERIVED
  calls skimage.morphology.medial_axis.  SKIMAGE IS NOT INSTALLED IN THIS TREE
  AND out/glyph_lab.npy IS GONE, so step 3 cannot be re-run as written and the
  tilde could not be derived the way the other 24 strokes were.  What was used
  instead, and it is a different instrument, not the same one:

      3'. scipy.ndimage.distance_transform_edt on the upsampled, sigma = 0.55
          smoothed indicator (steps 1-2 unchanged).  RIDGE = the crest of that
          transform: a pixel where E >= both neighbours along at least one of
          the four axes, closed 3x3, largest component kept.
      4'. Spine = the LONGEST GEODESIC PATH across that ridge (double Dijkstra
          on the 8-connected ridge graph).  This replaces step 4's junction
          clustering and its 3.0 px leaf prune: taking the longest path drops
          every shorter branch by construction, so the prune length is not a
          free parameter here.  It also means THIS STROKE HAS NO BRANCHES,
          which the medial axis would have given it.
      5-6 unchanged: half-width is the distance transform sampled along the
          spine, nothing added; cubic smoothing spline; 1.25 px point spacing.

  Achieved on this stroke, watched printing: spine 160 ridge px, geodesic
  length 30.85 source px, axis 0.283 px RMS / 0.740 px peak (the file's
  AXIS_TOL_RMS_PX is 0.20 / 0.60 -- THIS STROKE IS LOOSER THAN THE OTHER 24 AND
  THAT IS STATED, not smoothed away), half-width RMS 0.100 px, half-width
  p50 2.01 / p90 2.76 source px, 26 points.

  THE BAND, AND THE ABLATION THAT SET IT.  The tilde is fused to the `e`, the
  `n~` and the `o` -- one ink mass, as COUNTERS above already says -- so the
  source has to be cut out of the reference by a window.  Window mask
  x 38..64, y <= YB, largest component.  YB was ABLATED BEFORE IT WAS CHOSEN
  (rule 36), scoring the whole word against the re-baked reference:

      YB              5      6      7      8*     9     10     11
      Senor IoU     .8336  .8634  .8752  .8859  .8727  .8727  .8608
      ref-only px    150    114    101     91    102    102    116
      gen-only px     32     36     36     34     38     38     37

  Over-draw (gen-only) is FLAT across the whole sweep at 32-38 px, so this is
  not a wider stroke buying score: past YB = 8 the spine simply stops following
  the tilde and starts descending into the `n~`, and the IoU falls.  That is
  where the tilde's own ink ends.  The x limits are a plateau, not a knife
  edge: XA 36/37/38/39/40 -> .8840/.8827/.8859/.8815/.8743 and XB saturates at
  63 (.8786/.8841/.8859/.8859 for 61/62/63/64) because the ink stops there.

  THE S IS STILL BROKEN AND THAT IS DELIBERATE.  NOT TOUCHED AT REV 59 and NOT
  re-measured at rev 59 either.  WHAT THIS REPRODUCES above is the record: the
  break is what the chromaticity segmentation measured, the render shows the `S`
  in three pieces because this file draws it in three pieces, and bridging
  _STROKES[0]->[1]->[2] would be inventing ink.  It is an OWNER decision, not
  this file's.  The re-baked reference does not change it -- the rev-9 bake and
  the live mask agree across the `S` (the `S` box moved 351 -> 355 ref px).

  WHAT REV 59 DID NOT FIX, with its number.  Against the re-baked reference the
  word scores 0.8859 and 91 px of reference ink are still undrawn (34 px are
  drawn that the reference does not carry).  The 91 are SCATTERED -- no cluster
  larger than about 15 px.  The two largest are ~15 px at mask x 28..31,
  y 8..14 (the `S`-to-`e` junction) and ~14 px at x 51..55, y 8..12 (the fused
  `n~`/`o` mass).  One tilde stroke cannot reach either; they are a separate,
  unfixed deficit and they are NOT the tilde.

  ACCURACY, REV 59 (python3 senor_trace.py re-derives all of these):

      before: Senor 0.9134 against the 934 px bake  -- BUT THE BAKE WAS WRONG
      re-baked reference alone, strokes untouched:  Senor 0.8135
      with the tilde stroke:                        Senor 0.8859

      S 0.8825   e 0.7824   n~ 0.8713   o 0.8340   r 0.9144

  The first number and the third are not comparable and must not be quoted as a
  regression: the reference under them is a different mask.  0.8135 is what the
  rev-9 strokes were always worth against the ink the photograph actually
  carries; 0.9134 was the score of a trace against its own blind spot.

USE
    import senor_trace
    senor_trace.draw_senor(canvas, ypad=16)
"""
import numpy as np

# script_gen.py mask-space origin in ref_side.jpg pixels, for reference only.
X0, Y0 = 325, 486

# Measured extent of `Senor` in mask space (x0, y0, x1, y1), y down.
SENOR_BBOX = (6, -12, 88, 27)

# Derivation parameters, recorded so the trace can be regenerated.
UPSAMPLE = 6
BOUNDARY_SIGMA_PX = 0.55        # source px, Gaussian on the upsampled indicator
SPUR_PRUNE_PX = 3.0             # source px
AXIS_TOL_RMS_PX = 0.20          # source px, spline vs raw medial axis
AXIS_TOL_PEAK_PX = 0.60         # source px, worst branch
WIDTH_TOL_RMS_PX = 0.10         # source px, on the half-width profile
POINT_SPACING_PX = 1.25         # source px

# Each stroke is (glyph, array of (x, y, half_width) rows) in mask space.
# `half_width` is the measured Euclidean distance transform, in source px.
_STROKES = [
    ("S", np.array([
    (  22.33,   -4.67,  1.75),
    (  21.28,   -5.21,  2.16),
    (  20.19,   -5.62,  2.34),
    (  19.40,   -6.47,  2.37),
    (  18.80,   -7.49,  2.34),
    (  17.96,   -8.37,  2.34),
    (  16.97,   -9.01,  2.37),
    (  15.83,   -9.33,  2.45),
    (  14.70,   -9.48,  2.59),
    (  13.69,   -8.84,  2.79),
    (  12.71,   -8.19,  3.03),
    (  11.78,   -7.45,  3.29),
    (  11.32,   -6.39,  3.54),
    (  11.15,   -5.22,  3.76),
    (  10.91,   -4.06,  3.92),
    (  10.66,   -2.90,  4.02),
    (  11.01,   -1.77,  4.01),
    (  11.45,   -0.68,  3.90),
    (  12.00,    0.33,  3.72),
    (  12.75,    1.25,  3.53),
    (  13.74,    1.89,  3.40),
    (  14.68,    2.63,  3.35),
    (  15.81,    3.03,  3.37),
    (  16.92,    3.49,  3.42),
    (  18.08,    3.40,  3.45),
    (  19.15,    3.49,  3.44),
    (  20.26,    3.50,  3.36),
    (  21.37,    3.83,  3.24),
    (  22.44,    4.27,  3.07),
    (  23.38,    5.00,  2.87),
    (  24.36,    5.67,  2.64),
    (  25.33,    6.33,  2.42),
    ])),
    ("S", np.array([
    (  16.50,   14.50,  1.18),
    (  17.16,   15.51,  1.27),
    (  17.49,   16.63,  1.35),
    (  18.12,   17.64,  1.41),
    (  18.95,   18.46,  1.48),
    (  19.91,   19.19,  1.56),
    (  21.09,   19.44,  1.66),
    (  22.28,   19.62,  1.77),
    (  23.47,   19.83,  1.89),
    (  24.62,   19.83,  2.00),
    (  25.70,   19.47,  2.08),
    (  26.63,   18.70,  2.12),
    (  27.50,   17.83,  2.09),
    ])),
    ("S", np.array([
    (  23.50,   24.33,  0.70),
    (  23.50,   25.58,  1.19),
    (  24.35,   26.32,  1.52),
    (  25.51,   26.72,  1.17),
    (  26.67,   27.17,  0.71),
    ])),
    ("e", np.array([
    (  36.33,    2.50,  1.07),
    (  35.35,    3.14,  1.31),
    (  34.54,    3.96,  1.38),
    (  33.73,    4.77,  1.35),
    (  33.83,    5.93,  1.33),
    (  34.00,    7.07,  1.41),
    (  34.17,    8.21,  1.68),
    (  34.01,    9.37,  2.24),
    (  33.67,   10.50,  3.18),
    ])),
    ("e", np.array([
    (  33.67,   10.67,  3.28),
    (  33.67,   10.67,  3.28),
    ])),
    ("e", np.array([
    (  33.67,   10.67,  3.28),
    (  34.65,   11.32,  2.68),
    (  35.56,   12.06,  2.32),
    (  36.46,   12.84,  2.38),
    (  37.33,   13.67,  2.76),
    ])),
    ("e", np.array([
    (  37.33,   13.67,  2.66),
    (  37.50,   14.87,  2.83),
    (  37.69,   16.03,  2.90),
    (  38.28,   17.03,  2.90),
    (  39.25,   17.75,  2.84),
    (  40.35,   18.21,  2.75),
    (  41.56,   18.33,  2.69),
    (  42.80,   18.33,  2.71),
    (  44.00,   18.17,  2.87),
    ])),
    ("ntilde", np.array([
    (  44.67,   10.67,  2.87),
    (  43.50,   10.50,  2.49),
    (  42.38,   10.83,  2.10),
    (  41.27,   11.22,  1.77),
    (  40.14,   11.51,  1.60),
    (  39.17,   12.18,  1.65),
    (  38.18,   12.82,  2.02),
    (  37.33,   13.67,  2.79),
    ])),
    ("ntilde", np.array([
    (  45.83,   16.00,  2.64),
    (  45.28,   16.73,  2.57),
    (  44.62,   17.38,  2.68),
    (  44.17,   18.17,  3.00),
    ])),
    ("ntilde", np.array([
    (  44.17,   18.33,  2.91),
    (  44.79,   19.27,  2.33),
    (  45.34,   20.25,  2.02),
    (  45.98,   21.18,  2.12),
    (  46.50,   22.17,  2.67),
    ])),
    ("ntilde", np.array([
    (  44.83,   10.83,  2.77),
    (  45.15,   12.07,  2.01),
    (  45.33,   13.35,  1.67),
    (  45.59,   14.59,  1.85),
    (  45.83,   15.83,  2.54),
    ])),
    ("ntilde", np.array([
    (  45.17,   10.50,  2.78),
    (  46.36,   10.49,  1.75),
    (  47.40,   10.50,  1.04),
    (  48.52,   10.32,  0.71),
    (  49.64,   10.36,  0.75),
    (  50.72,   10.72,  1.08),
    (  51.57,   11.56,  1.59),
    (  52.11,   12.61,  2.16),
    (  52.50,   13.71,  2.69),
    (  52.83,   14.83,  3.08),
    ])),
    ("ntilde", np.array([
    (  52.67,   15.00,  3.00),
    (  51.69,   15.65,  2.33),
    (  50.61,   16.08,  1.87),
    (  49.47,   16.33,  1.63),
    (  48.28,   16.33,  1.65),
    (  47.13,   16.17,  1.96),
    (  46.00,   16.00,  2.58),
    ])),
    ("ntilde", np.array([
    (  46.50,   22.17,  2.67),
    (  46.50,   22.17,  2.67),
    ])),
    ("ntilde", np.array([
    (  46.67,   22.33,  2.70),
    (  47.86,   22.32,  2.48),
    (  49.00,   22.33,  2.32),
    (  50.09,   22.75,  2.21),
    (  51.12,   23.28,  2.15),
    (  52.14,   23.84,  2.11),
    (  53.13,   24.46,  2.08),
    (  54.19,   24.83,  2.03),
    (  55.28,   24.93,  1.96),
    (  56.28,   25.02,  1.86),
    (  57.43,   25.18,  1.77),
    (  58.59,   25.33,  1.69),
    (  59.72,   25.50,  1.66),
    (  60.83,   25.83,  1.70),
    ])),
    ("ntilde", np.array([
    (  52.83,   14.83,  3.11),
    (  52.83,   14.83,  3.11),
    ])),
    # ------------------------------------------------------------ REV 59
    # THE TILDE.  Derived by this file's own step 5 from the RE-BAKED
    # reference (see THE TILDE, REV 59 in the header): ridge of the
    # distance transform over the band mask x 38..64, y <= 8, spline-fitted
    # at the same tolerances as every other stroke here.  It ABSORBS the
    # 3 px vertical stub that used to sit at (45.33, 7.33)..(45.00, 10.33)
    # and the lone inscribed disc at (51.67, 4.33, 1.67) -- both were
    # remnants of a tilde that SPUR_PRUNE_PX had eaten, and both are gone
    # from the list above.  Deleting the stub costs 0.0000 IoU and deleting
    # the disc costs 0.0010; watched, both ways.
    ("ntilde", np.array([
    (  38.55,    3.47,  0.35),
    (  39.53,    3.42,  1.12),
    (  40.50,    3.78,  1.81),
    (  41.48,    4.43,  2.18),
    (  42.46,    5.24,  2.29),
    (  43.46,    6.07,  2.20),
    (  44.48,    6.80,  2.00),
    (  45.55,    7.30,  1.75),
    (  46.64,    7.49,  1.53),
    (  47.74,    7.42,  1.45),
    (  48.79,    7.13,  1.61),
    (  49.80,    6.70,  2.01),
    (  50.78,    6.16,  2.48),
    (  51.73,    5.58,  2.71),
    (  52.69,    5.00,  2.57),
    (  53.66,    4.49,  2.28),
    (  54.69,    4.10,  2.05),
    (  55.77,    3.88,  2.02),
    (  56.87,    3.89,  2.18),
    (  57.96,    4.18,  2.48),
    (  59.01,    4.73,  2.80),
    (  60.02,    5.45,  2.90),
    (  60.97,    6.26,  2.57),
    (  61.86,    7.06,  1.80),
    (  62.70,    7.78,  0.90),
    (  63.48,    8.32,  0.35),
    ])),
    ("o", np.array([
    (  59.17,    4.67,  1.72),
    (  59.38,    5.82,  1.77),
    (  59.94,    6.92,  2.10),
    (  60.49,    8.00,  2.52),
    (  61.01,    9.10,  2.82),
    (  61.01,   10.25,  2.89),
    (  61.55,   11.36,  2.82),
    (  62.31,   12.32,  2.80),
    (  63.00,   13.33,  2.98),
    ])),
    ("o", np.array([
    (  63.00,   13.33,  3.06),
    (  62.67,   14.43,  2.72),
    (  62.83,   15.59,  2.18),
    (  62.83,   16.80,  2.17),
    (  62.83,   18.00,  2.22),
    ])),
    ("o", np.array([
    (  62.83,   18.00,  2.22),
    (  62.72,   18.17,  2.15),
    (  62.83,   18.00,  2.22),
    ])),
    ("o", np.array([
    (  63.00,   13.33,  3.04),
    (  64.15,   13.17,  2.45),
    (  65.33,   13.00,  2.08),
    (  66.38,   12.86,  1.94),
    (  67.47,   13.00,  2.04),
    (  68.65,   13.17,  2.37),
    (  69.83,   13.33,  2.92),
    ])),
    ("r", np.array([
    (  72.33,    9.67,  1.77),
    (  71.56,   10.45,  1.81),
    (  70.94,   11.39,  2.05),
    (  70.47,   12.39,  2.50),
    (  69.83,   13.33,  2.95),
    ])),
    ("r", np.array([
    (  69.83,   13.33,  2.91),
    (  70.37,   14.37,  2.59),
    (  70.91,   15.44,  2.46),
    (  71.32,   16.55,  2.43),
    (  71.37,   17.61,  2.43),
    (  71.63,   18.72,  2.37),
    (  72.35,   19.68,  2.21),
    (  73.02,   20.67,  1.96),
    (  73.87,   21.55,  1.69),
    (  74.81,   22.31,  1.44),
    (  75.87,   22.87,  1.27),
    (  76.97,   23.32,  1.15),
    (  78.11,   22.92,  1.07),
    (  79.10,   22.25,  1.10),
    (  80.09,   21.58,  1.29),
    (  81.01,   20.82,  1.63),
    (  81.66,   19.83,  2.04),
    (  82.16,   18.74,  2.47),
    (  82.67,   17.67,  2.85),
    ])),
    ("r", np.array([
    (  76.33,   10.33,  0.70),
    (  77.46,   10.44,  0.90),
    (  78.41,   11.07,  1.23),
    (  79.30,   11.80,  1.34),
    (  80.12,   12.62,  1.35),
    (  80.73,   13.58,  1.38),
    (  81.20,   14.61,  1.53),
    (  81.63,   15.68,  1.84),
    (  81.92,   16.79,  2.31),
    (  82.67,   17.67,  2.99),
    ])),
    ("r", np.array([
    (  88.17,   14.33,  0.88),
    (  87.67,   15.37,  0.73),
    (  86.92,   16.25,  0.83),
    (  85.92,   16.80,  1.13),
    (  84.87,   17.19,  1.59),
    (  83.73,   17.33,  2.20),
    (  82.67,   17.67,  2.90),
    ])),
]

# Counters: closed contours subtracted from the ink.  Same derivation.
_CUTS = [
    ("ntilde", np.array([
    (  42.30,   15.67), (  42.07,   15.71), (  41.85,   15.71), (  41.64,   15.67),
    (  41.44,   15.59), (  41.25,   15.47), (  41.07,   15.33), (  40.92,   15.16),
    (  40.78,   14.97), (  40.66,   14.76), (  40.56,   14.55), (  40.49,   14.32),
    (  40.45,   14.10), (  40.43,   13.88), (  40.45,   13.67), (  40.50,   13.47),
    (  40.59,   13.29), (  40.71,   13.13), (  40.87,   12.99), (  41.08,   12.89),
    (  41.32,   12.82), (  41.60,   12.79), (  41.90,   12.78), (  42.20,   12.81),
    (  42.51,   12.88), (  42.80,   12.97), (  43.06,   13.09), (  43.29,   13.23),
    (  43.47,   13.41), (  43.60,   13.61), (  43.66,   13.83), (  43.65,   14.07),
    (  43.60,   14.32), (  43.49,   14.57), (  43.35,   14.81), (  43.17,   15.04),
    (  42.98,   15.25), (  42.76,   15.43), (  42.53,   15.57), (  42.30,   15.67),
    ])),
    ("ntilde", np.array([
    (  49.38,   14.50), (  49.17,   14.56), (  48.93,   14.58), (  48.68,   14.57),
    (  48.41,   14.51), (  48.15,   14.42), (  47.90,   14.30), (  47.67,   14.14),
    (  47.47,   13.95), (  47.31,   13.73), (  47.20,   13.49), (  47.14,   13.22),
    (  47.15,   12.93), (  47.20,   12.64), (  47.29,   12.35), (  47.42,   12.06),
    (  47.57,   11.81), (  47.74,   11.58), (  47.93,   11.39), (  48.12,   11.25),
    (  48.32,   11.17), (  48.51,   11.15), (  48.69,   11.18), (  48.88,   11.25),
    (  49.05,   11.37), (  49.21,   11.52), (  49.36,   11.71), (  49.50,   11.91),
    (  49.62,   12.14), (  49.72,   12.39), (  49.80,   12.64), (  49.87,   12.90),
    (  49.90,   13.16), (  49.92,   13.41), (  49.91,   13.65), (  49.87,   13.87),
    (  49.79,   14.07), (  49.69,   14.25), (  49.55,   14.39), (  49.38,   14.50),
    ])),
]



def _chunks(pts, w, max_turn=0.45, max_len=6.0):
    """Split a polyline into short, low-curvature runs overlapping by one point.

    script_gen.Canvas.stroke() builds a stroke outline by offsetting left and
    right and joining the two sides into ONE polygon.  On a tight curve that
    polygon self-intersects and the even-odd scanline fill punches a hole in
    the letter.  Splitting the path into runs that turn by less than ~26 deg
    keeps every polygon simple, and the round end cap that stroke() draws at
    each run boundary becomes a round join.  The union is then exactly a disc
    sweep -- which is what a distance-transform half-width means.
    """
    n = len(pts)
    if n < 2:
        return [(pts, w)]
    seg = np.diff(pts, axis=0)
    L = np.hypot(seg[:, 0], seg[:, 1])
    ang = np.arctan2(seg[:, 1], seg[:, 0])
    out, i = [], 0
    while i < n - 1:
        j, acc_len, acc_turn = i + 1, L[i], 0.0
        while j < n - 1:
            dt = (ang[j] - ang[j - 1] + np.pi) % (2 * np.pi) - np.pi
            if acc_turn + abs(dt) > max_turn or acc_len + L[j] > max_len:
                break
            acc_turn += abs(dt); acc_len += L[j]; j += 1
        out.append((pts[i:j + 1], w[i:j + 1]))
        i = j
    return out


def draw_senor(c, ypad=0):
    """Draw `Senor` into a script_gen.Canvas.

    `ypad` is added to every y coordinate.  The word reaches y = -12 in mask
    space, so ypad must be at least 12 for the top of the `S` to be drawn.
    Uses only c.stroke(pts, w) and c.cut(pts); no canvas dimension is read.
    """
    for _name, a in _STROKES:
        pts = np.c_[a[:, 0], a[:, 1] + ypad]
        w = a[:, 2]
        if len(pts) < 2:                      # a lone inscribed disc
            pts = np.vstack([pts, pts]); w = np.r_[w, w]
        for cp, cw in _chunks(pts, w):
            if len(cp) < 2:
                cp = np.vstack([cp, cp]); cw = np.r_[cw, cw]
            c.stroke(cp, cw)
    for _name, a in _CUTS:
        c.cut(np.c_[a[:, 0], a[:, 1] + ypad])


# ---------------------------------------------------------------------------
# Self-test.  Rasterises the strokes above on a bare canvas that reproduces
# script_gen.Canvas exactly (SS = 12 supersample, ink minus hole, area-average
# down) and scores IoU against the measured `Senor` mask, which is baked in
# below as packed bits so this file needs nothing at runtime.
# ---------------------------------------------------------------------------
_SS = 12

# ---------------------------------------------------------------------------
# THE REFERENCE, RE-BAKED AT REV 59 -- AND WHY IT HAD TO BE
#
# The bits below USED to be labels 1-5 of out/glyph_lab.npy, 934 px.  That file
# and the skimage install that produced it are BOTH GONE from this repo, and
# _crosscheck() had been printing "(glyph_lab.npy not present -- baked mask not
# cross-checked)" ever since, silently.  So the trace was grading itself against
# a mask nobody could reproduce, and that mask WAS MISSING THE TILDE: 118 px of
# `Senor` ink, dead centre over the `n`, that the live segmentation has and the
# baked one did not.  The trace scored 0.913 against it and the owner still
# could not read the word.
#
# NOT A12.  A12 forbids "inventing ink the photograph does not show".  This is
# the opposite: the photograph DOES show it, compare_script.ref_mask() -- the
# mask the LIVE gate scores against -- carries it, and it survives the strict
# T_SILVER rule.  This restores ink a superseded segmentation dropped.
#
# HOW THESE BITS WERE MADE, so they can be made again:
#   rows y in -12..22   compare_script.ref_mask(), window mask x 6..88,
#                       minus _SWASH_EXCLUDE below.  _rebake_ref() does exactly
#                       this and check_ref_agrees() asserts the two still agree.
#   rows y in 23..27    KEPT VERBATIM from the rev-9 bake.  The Tacombi swash
#                       runs right through those rows on its way under the word
#                       (88 px of it inside this window), it is script_gen's ink
#                       and not this trace's, and connectivity cannot separate
#                       it -- the whole lockup is ONE component of 8967 px.
#                       Those rows are therefore NOT re-baked and NOT guarded;
#                       that is the guard's declared blind spot.
# Total 1062 px against the old bake's 934.  Watched printing.
#
# _SWASH_EXCLUDE is the swash where it crosses rows -12..22 of this window.
# It was NOT placed by eye: it is script_gen's own lockup built with
# draw_senor() suppressed -- i.e. the Tacombi half, drawn from control points
# that have nothing to do with this file -- intersected with this window and
# with the complement of the rev-9 bake.  30 px, painted and looked at before
# it was adopted; 27 of them are the swash rising past the `r` at the right
# edge and 3 are isolated crossings under the word.  FOUR OF THE THIRTY ARE
# NO-OPS -- the generator's swash covers them but the photograph's mask does
# not -- so the re-bake actually removes 26.  1176 - 88 (the swash in rows
# 23..27, which is why those rows are not re-baked) - 26 = 1062.
_SWASH_EXCLUDE = (
    (86, 15), (88, 16), (87, 17), (88, 17), (86, 18), (87, 18),
    (88, 18), (47, 19), (85, 19), (86, 19), (87, 19), (88, 19),
    (84, 20), (85, 20), (86, 20), (87, 20), (88, 20), (43, 21),
    (83, 21), (84, 21), (85, 21), (86, 21), (87, 21), (88, 21),
    (54, 22), (84, 22), (85, 22), (86, 22), (87, 22), (88, 22),
)
_REBAKE_Y_MAX = 22              # rows above this are re-baked AND guarded

_REF_B64 = (
    "AeAAAAAAAAAAAAH/AAAAAAAAAAAAf/AAAAAAAAAAAB//AAAAAAAAAAAD//AAAAAAAAAAAH"
    "8/AAAAAAAAAAAf5/AAAAAAAAAAA/z/AAAAAAAAAAD/j8AAAAAAAAAAH/AAAAAAAAAAAAP+"
    "AAAAAAAAAAAAP+AAAAAAAAAAAAP/8AAAAAAAAAAAf//ABAAADAAAAAf//gPeA//gAAAAf/"
    "/g/+D//gAAAAf//j5+H//AAAAAP//Hz+P/8AAAAAAf8Hj//H4AAAAAAH4PD/+H4AAAAAAD"
    "n/H/+PwHAAAAAAf///+fgfIAAAAAf///8/B88AAAAA///n5//w8AAAAD//+Px//g8AAEAH"
    "/4cfh//A4EAcAGPw8/D/+A4YAcAgfz/+Hx+B8wA4Dg///8Hh8H/AB4Ph///4PD4P8AB//B"
    "/+Bg/HwPwAB/8B/8AA/PwfAAB/wA//gA8Ph8AAAfAAB/gAAPjwAAAAAAD/wAAP/wAAAAAA"
    "H/+AAHwAAABAAAP//wADAAAAHgAAAP/wAAAAAAPgAAAP/gAAAAAAPgAAAAGAAAAA=="
)
_REF_X0, _REF_Y0, _REF_W, _REF_H = 6, -12, 83, 40
_GLYPH_BOXES = [
    ("S", 4, -14, 32, 30),
    ("e", 26, 3, 42, 23),
    ("ntilde", 30, -1, 65, 30),
    ("o", 49, 0, 69, 23),
    ("r", 64, 6, 91, 27),
]

def _ref_mask():
    """The measured `Senor` ink, packed row-major over mask-space
    x 6..88, y -12..27.  1062 px.  Rows y <= _REBAKE_Y_MAX come from
    compare_script.ref_mask() minus _SWASH_EXCLUDE (re-baked at rev 59);
    rows below that are the rev-9 bake, kept because the Tacombi swash
    crosses them.  See THE REFERENCE, RE-BAKED AT REV 59 above.

    T1_ST_REFDRIFT=1 is the ABLATION: it flips one bit of these constants so
    that check_ref_agrees() must go red.  Watched failing, both ways."""
    import base64, os
    bits = np.unpackbits(np.frombuffer(base64.b64decode(_REF_B64), np.uint8))
    m = bits[:_REF_H * _REF_W].reshape(_REF_H, _REF_W).astype(bool)
    if os.environ.get("T1_ST_REFDRIFT"):
        m = m.copy()
        m[10, 40] = ~m[10, 40]          # mask (x, y) = (46, -2), inside the guard
    return m


def _rebake_ref():
    """Recompute the reference from the LIVE mask the gate scores against.

    This is the derivation _REF_B64 was baked from, kept runnable so the bake
    is reproducible now that out/glyph_lab.npy is gone.  Returns the same
    (_REF_H, _REF_W) array: rows y <= _REBAKE_Y_MAX from
    compare_script.ref_mask() minus _SWASH_EXCLUDE, rows below kept from the
    baked constants.  Raises rather than guessing if compare_script's window
    origin ever moves away from this file's.
    """
    import compare_script as C
    if (C.X0, C.Y0) != (X0, Y0):
        raise RuntimeError("compare_script window moved: (%d,%d) vs (%d,%d)"
                           % (C.X0, C.Y0, X0, Y0))
    live = C.ref_mask()
    r0 = _REF_Y0 + C.YPAD                        # mask y -> ref_mask() row
    sub = live[r0:r0 + _REF_H, _REF_X0:_REF_X0 + _REF_W].copy()
    for x, y in _SWASH_EXCLUDE:
        sub[y - _REF_Y0, x - _REF_X0] = False
    baked = _ref_mask()
    sub[_REBAKE_Y_MAX + 1 - _REF_Y0:, :] = baked[_REBAKE_Y_MAX + 1 - _REF_Y0:, :]
    return sub


def check_ref_agrees(verbose=True):
    """THE GUARD (rev 59).  Two reference masks over the same window silently
    disagreed for fifty revisions -- senor_trace's baked 934 px against
    compare_script's live 1176 px, IoU 0.788 -- and the difference WAS the
    missing tilde.  Nothing compared them, so nothing said so.

    This does: exact, pixel-for-pixel, over the guarded window (mask
    x 6..88, y -12..%d, minus the %d _SWASH_EXCLUDE pixels).  A divergence is
    a FINDING, not a tolerance.  Returns (ok, n_disagree, n_guarded).

    It NEEDS ref_side.jpg in the working directory.  If it cannot read it the
    answer is "NO REFERENCE", not a number (rule 37).
    """ % (_REBAKE_Y_MAX, len(_SWASH_EXCLUDE))
    try:
        live = _rebake_ref()
    except Exception as e:                       # missing frame, moved window
        if verbose:
            print("  NO REFERENCE -- cannot read the live mask: %s" % e)
        return (False, -1, -1)
    baked = _ref_mask()
    rows = slice(0, _REBAKE_Y_MAX + 1 - _REF_Y0)
    d = baked[rows] != live[rows]
    n = int(d.sum())
    guard = np.ones_like(d)
    for x, y in _SWASH_EXCLUDE:
        if y <= _REBAKE_Y_MAX:
            guard[y - _REF_Y0, x - _REF_X0] = False
    ng = int(guard.sum())
    ok = n == 0
    if verbose:
        print("  baked reference AGREES with compare_script.ref_mask(): "
              "%s (%d disagree of %d guarded px, baked %d, live %d)"
              % ("yes" if ok else "NO", n, ng, int(baked.sum()),
                 int(live.sum())))
        if not ok:
            ys, xs = np.nonzero(d)
            first = ["(%d,%d)" % (x + _REF_X0, y + _REF_Y0)
                     for x, y in list(zip(xs, ys))[:8]]
            print("  THE TWO REFERENCES HAVE DIVERGED at mask %s%s"
                  % (", ".join(first), " ..." if n > 8 else ""))
            print("  Re-bake with _rebake_ref() and say in the ledger WHY the "
                  "live mask moved -- do not relax this row.")
    return (ok, n, ng)


class _Canvas:
    """Byte-for-byte the rasterisation contract of script_gen.Canvas, plus pad."""

    def __init__(self, mw, mh):
        from PIL import Image, ImageDraw
        self.MW, self.MH = mw, mh
        self.ink = Image.new("L", (mw * _SS, mh * _SS), 0)
        self.hole = Image.new("L", (mw * _SS, mh * _SS), 0)
        self.di = ImageDraw.Draw(self.ink)
        self.dh = ImageDraw.Draw(self.hole)

    @staticmethod
    def _resample(pts, n=400):
        d = np.r_[0.0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]
        if d[-1] <= 0:
            return pts
        u = np.linspace(0, d[-1], n)
        return np.c_[np.interp(u, d, pts[:, 0]), np.interp(u, d, pts[:, 1])]

    @staticmethod
    def _outline(pts, w):
        d = np.gradient(pts, axis=0)
        L = np.hypot(d[:, 0], d[:, 1]); L[L == 0] = 1.0
        nx, ny = -d[:, 1] / L, d[:, 0] / L
        return np.vstack([pts + np.c_[nx, ny] * w[:, None],
                          (pts - np.c_[nx, ny] * w[:, None])[::-1]])

    def _fill(self, d, pts):
        d.polygon([(float(x) * _SS, float(y) * _SS) for x, y in pts], fill=255)

    def blob(self, pts):
        self._fill(self.di, pts)

    def cut(self, pts):
        self._fill(self.dh, pts)

    def stroke(self, pts, w, cut=False, caps=True):
        pts = self._resample(np.asarray(pts, float), 400)
        if np.isscalar(w):
            w = np.full(len(pts), float(w))
        else:
            w = np.asarray(w, float)
            if len(w) != len(pts):
                w = np.interp(np.linspace(0, 1, len(pts)),
                              np.linspace(0, 1, len(w)), w)
        d = self.dh if cut else self.di
        self._fill(d, self._outline(pts, w))
        if caps:
            for p, r in ((pts[0], w[0]), (pts[-1], w[-1])):
                d.ellipse([(p[0] - r) * _SS, (p[1] - r) * _SS,
                           (p[0] + r) * _SS, (p[1] + r) * _SS], fill=255)

    def alpha(self):
        a = np.array(self.ink, np.uint8).astype(np.float32)
        h = np.array(self.hole, np.uint8).astype(np.float32)
        m = np.clip(a - h, 0, 255)
        return m.reshape(self.MH, _SS, self.MW, _SS).mean(axis=(1, 3))


def _iou(a, b):
    u = (a | b).sum()
    return (a & b).sum() / u if u else 1.0


def selftest(threshold=96, verbose=True):
    """Rasterise and score against the measured mask.  Returns {region: IoU}."""
    # A bare local canvas around the word, big enough that nothing is clipped.
    ox, oy = _REF_X0 - 8, _REF_Y0 - 4           # canvas origin offset, mask space
    W, H = _REF_W + 16, _REF_H + 12
    c = _Canvas(W, H)

    class _Shift:                              # draw into the local crop
        def __init__(self, c):
            self.c = c

        def stroke(self, pts, w, cut=False, caps=True):
            self.c.stroke(np.c_[pts[:, 0] - ox, pts[:, 1] - oy], w, cut, caps)

        def cut(self, pts):
            self.c.cut(np.c_[np.asarray(pts)[:, 0] - ox,
                             np.asarray(pts)[:, 1] - oy])

        def blob(self, pts):
            self.c.blob(np.c_[np.asarray(pts)[:, 0] - ox,
                              np.asarray(pts)[:, 1] - oy])

    draw_senor(_Shift(c), ypad=0)
    G = c.alpha() > threshold

    R = np.zeros((H, W), bool)
    R[_REF_Y0 - oy:_REF_Y0 - oy + _REF_H, _REF_X0 - ox:_REF_X0 - ox + _REF_W] = \
        _ref_mask()

    res = {"Senor": _iou(G, R)}
    if verbose:
        print("  senor_trace.py -- IoU against the measured mask "
              "(alpha > %d, script_gen SS=%d)" % (threshold, _SS))
        print("  axis tol %.2f px RMS / %.2f px peak, width tol %.2f px RMS, "
              "spur prune %.1f px" % (AXIS_TOL_RMS_PX, AXIS_TOL_PEAK_PX,
                                      WIDTH_TOL_RMS_PX, SPUR_PRUNE_PX))
        print()
        print("  %-8s  %-6s %8s %8s" % ("region", "IoU", "gen px", "ref px"))
        print("  " + "-" * 34)
    for name, bx0, by0, bx1, by1 in _GLYPH_BOXES:
        sl = (slice(by0 - oy, by1 - oy), slice(bx0 - ox, bx1 - ox))
        g, r = G[sl], R[sl]
        res[name] = _iou(g, r)
        if verbose:
            print("  %-8s  %.4f %8d %8d" % (name, res[name], g.sum(), r.sum()))
    if verbose:
        print("  " + "-" * 34)
        print("  %-8s  %.4f %8d %8d" % ("Senor", res["Senor"], G.sum(), R.sum()))
        print()
        print("  strokes %d, points %d, cuts %d"
              % (len(_STROKES), sum(len(a) for _, a in _STROKES), len(_CUTS)))
        print()
        # THE GUARD RUNS HERE, not in a comment.  A green IoU against a
        # reference nobody checked is what shipped the missing tilde.
        res["ref_agrees"] = float(check_ref_agrees(verbose=True)[0])
    return res


def _crosscheck():
    """SUPERSEDED AT REV 59 by check_ref_agrees(), which is the row that runs.

    out/glyph_lab.npy has not existed in this repo for as long as anyone has
    looked, so this printed its "not present" line every single run and no
    human read it -- which is exactly how the baked mask went fifty revisions
    without being compared to anything.  It is kept, not deleted, because it is
    the only record of where the rev-9 bake came from; it is no longer the
    check.  It says NOT CROSS-CHECKED in those words and never returns a number
    when the input is absent (rule 37).
    """
    import os
    p = "/home/claude/work/measure/out/glyph_lab.npy"
    if not os.path.exists(p):
        print("  NOT CROSS-CHECKED against glyph_lab.npy -- the file is absent "
              "and has been for the life of this repo.")
        print("  (superseded: check_ref_agrees() above is the live comparison.)")
        return
    lab = np.load(p)
    ink = np.load("/home/claude/work/measure/out/ink_mask.npy")
    S = np.isin(lab, [1, 2, 3, 4, 5]) & ink
    ys, xs = np.nonzero(S)
    live = np.zeros((_REF_H, _REF_W), bool)
    live[ys + 462 - 486 - _REF_Y0, xs + 318 - 325 - _REF_X0] = True
    same = (live == _ref_mask()).all()
    print("  baked reference matches out/glyph_lab.npy labels 1-5: %s (%d px)"
          % (same, live.sum()))


if __name__ == "__main__":
    import sys
    _res = selftest()
    print()
    _crosscheck()
    # A failing guard must be a non-zero exit, not a line in a log nobody reads.
    sys.exit(0 if _res.get("ref_agrees", 0.0) == 1.0 else 1)
