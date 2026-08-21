"""
cal_gen.py -- the "100% Calidad" rear-corner decal, reproduced from the photo.

rev 8 drew a flat 24-point red star with no gradient, no bunting and type set
in a system italic. SPEC sec.10.10 lists this element as NOT STARTED, and the
brief for this pass names what is actually there. Source crop ref_side.jpg
(735,295)-(860,390), read at 8-12x.

WHAT THE PHOTOGRAPH SHOWS, MEASURED
  * one warm blob on the cream rear panel, abs x 736-835, y 306-379
    (100 x 74 px, aspect 1.35). That blob is starburst AND bunting together;
    the bunting bars sit across its top, so they share one decal panel.
  * the burst is a SPIKY sunburst -- many narrow sharp points of uneven
    length, not a regular 24-point star.
  * it carries a gradient. Sampled in bands along the upper-left -> lower-right
    axis: (240,132,130) at the red end, (245,180,148) at the orange/yellow end.
    The photograph is over-exposed here (the cream panel around it reads
    (236,229,227), i.e. nearly blown), so those are lifted; the paint is
    reconstructed saturated and the render's exposure brings it back.
  * white bold italic type, two lines, "100%" over "Calidad", set at about
    -20 degrees -- measured from the "1" at lower-left to the "%" at upper
    right, atan2(-190, 530) = -19.7 deg. Nine enclosed white counters survive
    segmentation inside the burst, largest 251 px.
  * TWO bunting bars above the type, each a thin bar with triangular pennants
    hanging BELOW it, both running roughly parallel to the type angle.
  * a small pink star to the left (SPEC sec.3).

PLACEMENT -- and why it moved
The decal's position was checked against a datum that does not depend on any
pixel-to-metre mapping: its fraction of the solid rear-corner panel. In the
photograph the panel runs x 698 (aft edge of bay 3) to x 902 (tail); the decal
occupies 18.6% to 67.2% of that span. build.py placed it at 37.3% to 84.7%.
That is 198 mm too far aft, and the ratio argument is immune to the
perspective foreshortening that makes a single linear x->X scale wrong here
(the panel measures 194.8 px/m against 211.5 px/m at mid-body).

    python3 cal_gen.py   -> tex/calidad.png
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, "tex")

AR = 1.355                       # measured 100 x 74 px
W = 2400
H = int(round(W / AR))           # 1771
SS = 3
w, h = W * SS, H * SS

# paint, reconstructed saturated -- see the exposure note above
RED = (214, 46, 30)
ORANGE = (238, 122, 22)
YELLOW = (247, 189, 46)
WHITE = (252, 250, 246)
PINK = (232, 96, 122)
# BUNT is retired with the bunting: the lines it coloured are vent slats,
# which are ~~DARK GREY~~ BODY-COLOUR sheet metal whose darkness IS its own
# self-shadow (retracted rev 47, landed here rev 49 -- see the note at the
# glyph_calidad bunting block).  Not red paint either way, which is why the
# retirement stands.  Kept as a record of what the retired feature used to
# use, and referenced by nothing.
_RETIRED_BUNT = (198, 40, 36)

ANG = math.radians(-19.7)        # measured type / bunting angle

# ------------------------------------------------------- rev 46, W1, SPEC 10.118
# THE BURST'S CENTRE, PROMOTED TO A CONSTANT, AND THE TYPE EXPRESSED AGAINST IT.
#
# The owner reported "the 100% calidad off center" and he is right.  It is NOT
# the defect rev 44 closed: that one was the decal PANEL'S PLACEMENT ON THE
# VEHICLE (Report 7, 0.180 of texture width).  This is the TYPE'S PLACEMENT
# INSIDE THE DECAL, which nobody had ever measured.  Both are true and they are
# different things.
#
# Measured on this generator's own output, before the block is rotated: the
# type's centroid sat at (0.3735, 0.6309) of the canvas while starburst()'s
# centre is (0.5050, 0.5750).  The block was 0.1315 w LEFT and 0.0559 h BELOW
# the burst it is supposed to sit on -- and it showed, with "100%" hanging off
# the burst onto bare cream and "Calidad" running off the panel's bottom edge.
#
# TYPE_SHIFT is EXACTLY that measured miss (SPEC 10.25: a constant tuned against
# another constant is expressed in terms of it).  It is not a re-tuned pair of
# absolutes -- re-run the pre-rotation centroid measurement after any glyph
# change and it re-derives.  The two lines keep their relative offset; only the
# block moves, which is what "off center" means.
#
# AND THE ROTATION CENTRE MOVES TO THE BURST'S CENTRE.  It was (0.500, 0.600) --
# near the burst's centre but not equal to it, so the -19.7 deg rotation swung
# the block off centre again by a further (+0.0148, +0.0558) even when the
# layout was right.  Rotating about the point the block is centred ON makes the
# centring EXACT and independent of ANG: a rotation fixes its own centre.
BURST_CX, BURST_CY = 0.505, 0.575

# ---------------------------------------------------------------- rev 47, W4
# THE TWO WORDS COLLIDED.  "100%" and "Calidad" shared 1110 pixels and their
# boxes overlapped by 0.0337 of the canvas height -- 14.5% of the "100%" cap
# height.  The owner reported it; rev 46 measured it and did not fix it.
#
# LINE_GAP OPENS THAT GAP, AND ITS MAGNITUDE IS NOT A MEASUREMENT.  Say so
# plainly (rule 6: an ordinal fact licenses a SIGN, never a SHAPE).  What
# ref_playa_34.png supports is that the two words are SEPARATE -- visible at
# 16x, and that is all.  A de-rotated row profile of the type inside the burst
# is a single broad smear with no trough between the words: at 4-6 px per word
# the bright/low-saturation rule that finds the type also finds the cream, the
# same failure LEDGER_rev46 sec.1 retracted a number for.  So this constant is
# the SMALLEST separation that clears the collision with a visible gap, and it
# is a placeholder for a photographed value.  PHOTOS_WANTED #1 settles it.
#
# It is expressed as a fraction of the "100%" cap height rather than of the
# canvas, so it survives a change of type size (SPEC 10.25 / rule 2).
CAP_100 = 0.228                  # "100%" size, as passed to glyph_100 below
# rev 47b: NOW MEASURED, from IMG_2073.jpeg, which he sent after seeing 0.26 and
# reporting that the words STILL did not read as two.  He was right.  The gap is
# carried as a RATIO against the same estimator run on the build, because the
# estimator has a +34% absolute bias that DIVIDES OUT of a ratio and does not
# divide out of a reading (probe_rev47_gap.py C1).  Photographed 0.244 against
# built 0.149 on the identical instrument => the photograph's gap is 1.64x the
# build's, so 0.26 * 1.64 = 0.43.  NOT MEASURED absolutely -- see probe.
# ===================== rev 48: THE RATIO ARGUMENT ABOVE IS RETRACTED ========
# It is wrong in three separate ways, and the value is KEPT anyway.  Both
# halves of that need saying.
#
# 1.  THE "+34 % ABSOLUTE BIAS" IS NOT A BIAS.  Swept over LINE_GAP 0.20..0.50
#     against cal_gen's own construction value, the estimator reads
#         LG    0.20   0.26   0.32   0.38   0.43   0.50
#         read  0.104  0.149  0.193  0.248  0.281  0.391
#         r/t   2.00   1.34   1.13   1.08   1.01   1.13
#     It is not multiplicative and not additive -- it is roughly AFFINE in
#     LINE_GAP with a NEGATIVE INTERCEPT.  A ratio rescaling assumes
#     proportionality THROUGH THE ORIGIN, and the intercept is exactly what
#     makes the 1.64x step wrong.  On clean synthetics the estimator reads
#     0.984 at every gap: there is no fixed bias to divide out.
#
# 2.  THE MECHANISM.  The estimator picks its reading angle by MAXIMISING the
#     apparent gap.  On this decal it selects -37.5 deg where ANG is -19.7.
#     Skewing two horizontally staggered words enlarges the apparent gap
#     between them, so the search rotates away from the true reading angle,
#     and it does so hardest when the gap is small.  That is the small-gap
#     inflation the record read as a fixed bias.  It is an instrument defect.
#     ==> NEXT_CONTEXT_PROMPT_rev48.md's NEW RULE 24 ("QUOTE THE RATIO, NOT
#     THE READING -- the bias divides out") has its FOUNDING CASE REFUTED.
#     The rule may still be good practice; this case does not support it.
#
# 3.  IT IS THE WRONG VEHICLE.  0.244 was measured on IMG_2073.jpeg -- the
#     GREEN bus.  He has ruled that the RED bus is the target and that ARTWORK
#     may not transfer between them, and their decals ARE different artwork
#     (spike depth 0.133 / 0.239 against 0.044).  A word gap is artwork.
#
# SO WHY IS 0.43 STILL HERE?  Because the correction is inadmissible too.
# Inverting the curve at the photographed 0.244 gives LINE_GAP 0.376 -- but
# that is still the GREEN bus's number, so substituting it swaps one
# inadmissible figure for another.  The RED bus's own decal bounds it and no
# more: both red frames are BLOWN in the highlights, the white type does not
# separate from the burst at any threshold, and a hand read of the de-rotated
# saturation profile of ref_side.jpg gives gap/cap 0.25..0.47.
#
#     0.43 IS INSIDE THAT BAND.  0.376 is too.  The red bus cannot separate
#     them, and this revision will not pretend otherwise.
#
# STATUS: TRANSFERRED FROM ANOTHER VEHICLE, ARTWORK CONFIRMED DIFFERENT,
# MAGNITUDE UNVERIFIED ON THE TARGET.  What settles it is one UNBLOWN frame
# of the red bus's decal -- ref_side.jpg already has the pixels, it does not
# have the dynamic range.
LINE_GAP = 0.43                  # of CAP_100.  TRANSFERRED, not measured on
                                 # the target vehicle; see the block above and
                                 # probe_rev47_gap.
LINE_SEP_BASE = 0.250            # rev 46's anchor separation, 0.645 - 0.395
LINE_SEP = LINE_SEP_BASE + LINE_GAP * CAP_100

# TYPE_SHIFT IS NOW DERIVED AT RUN TIME, NOT TRANSCRIBED.
# rev 46 froze TYPE_PRE_CENTROID = (0.3735, 0.6309) as a watched-print figure.
# That is correct only for rev 46's exact layout: change the gap -- which W4
# requires -- and the frozen centroid silently becomes wrong, the block slides
# off the burst, and the W1 guard fires.  The brief names this as the trap.
# Measuring the centroid of the actual laid-out type removes the trap instead
# of stepping around it, and it re-derives itself after ANY future glyph, size
# or spacing change.  SPEC 10.25: a constant tuned against another constant
# must be EXPRESSED in terms of it.
def _type_centroid(shift=(0.0, 0.0)):
    """Centroid of the two words as laid out, pre-rotation, in canvas units."""
    t = TypeMask(w, h)
    _place(t, shift)
    m = np.array(t.m) > 127
    ys, xs = np.nonzero(m)
    return (xs.mean() / w, ys.mean() / h)


def _place(t, shift):
    sx, sy = shift
    glyph_100(t, w * (0.150 + sx), h * (0.395 + sy), h * CAP_100)
    glyph_calidad(t, w * (0.180 + sx), h * (0.395 + LINE_SEP + sy), h * 0.196)


def rot(px, py, cx, cy, a):
    s, c = math.sin(a), math.cos(a)
    dx, dy = px - cx, py - cy
    return cx + dx * c - dy * s, cy + dx * s + dy * c


# ------------------------------------------------------------------ starburst
def starburst(d):
    """
    Spiky sunburst: narrow points of uneven length. The unevenness is the
    reason this does not read as a rev-8 regular star -- it is a hand-painted
    burst, so the tips wander. The sequence is fixed, not random, so the file
    is reproducible.
    """
    cx, cy = w * BURST_CX, h * BURST_CY
    RO, RI = h * 0.435, h * 0.255
    N = 27
    jitter = [0.94, 1.06, 0.88, 1.11, 0.97, 1.04, 0.91, 1.08, 1.00, 0.93,
              1.09, 0.96, 1.03, 0.89, 1.07, 0.99, 1.05, 0.92, 1.10, 0.95,
              1.02, 0.90, 1.06, 0.98, 1.04, 0.93, 1.08]
    pts = []
    for i in range(N * 2):
        a = math.pi * i / N - math.pi / 2 + math.pi / (2 * N)
        if i % 2 == 0:
            r = RO * jitter[(i // 2) % N]
        else:
            r = RI * (0.94 + 0.12 * jitter[(i // 2) % N])
        pts.append((cx + r * math.cos(a) * 1.30, cy + r * math.sin(a)))
    d.polygon(pts, fill=RED + (255,))
    return cx, cy, RO


def gradient(img, cx, cy):
    """
    Red-orange -> orange/yellow across the upper-left -> lower-right axis, the
    direction the sampled bands run in the photograph.
    """
    a = np.array(img).astype(np.float32)
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    t = ((xx - cx) * 0.62 + (yy - cy) * 0.78) / (1.35 * h)
    # ------------------------------------------------- rev 45, SPEC 10.112
    # THE BIAS WAS 0.42 AND IT THREW THE DECLARED COLOUR AWAY.
    #
    # `t` is zero AT THE BURST'S OWN CENTRE by construction -- (cx, cy) is
    # starburst()'s centre and the axis term is measured from it.  A bias of
    # 0.42 therefore started the ramp 42 % of the way along, so the core
    # evaluated to RED*0.16 + ORANGE*0.84 = (234, 110, 23).  Measured off
    # tex/calidad.png as shipped: core (237.0, 120.3, 22.0), G/R 0.508.
    # starburst() fills the whole polygon with RED = (214, 46, 30), G/R 0.215,
    # nine lines above -- AND NOTHING IN THE FINISHED TEXTURE IS THAT COLOUR
    # except the extreme upper-left corner where the clip bottoms out.  The
    # decal renders PEACH where the photograph is RED, which is what the owner
    # has reported twice.
    #
    # THE BIAS IS ZERO.  That is not a tuned number: it is the statement that
    # the gradient DEPARTS from the burst's declared colour going outward,
    # rather than starting two-thirds of the way to orange.  RED at the core,
    # ORANGE through the middle distance, YELLOW at the lower-right tips --
    # which is the direction the docstring's sampled bands actually run.
    #
    # Cross-check that needs no photograph: cal_gen's RED (214,46,30) has
    # G/R 0.215 and t1_mats' body RED sRGB(196,49,36) has G/R 0.250.  The
    # burst and the coachwork are the same red family, and at bias 0 the
    # rendered core lands there instead of 0.5.
    #
    # rev 44 ruled out two other causes BY TEST and both stay ruled out:
    # WEAR['calidad'] is not the lever (re-rendered at 0.22, core bit-
    # identical) and the material adds no cream.
    t = np.clip(t * 1.5 + 0.00, 0, 1)
    stops = np.array([RED, ORANGE, YELLOW], np.float32)
    k = t * 2.0
    i0 = np.clip(np.floor(k), 0, 1).astype(int)
    f = (k - i0)[..., None]
    col = stops[i0] * (1 - f) + stops[i0 + 1] * f
    m = a[..., 3:4] / 255.0
    a[..., :3] = a[..., :3] * (1 - m) + col * m
    return Image.fromarray(a.astype(np.uint8))


# -------------------------------------------------------------------- lettering
# Built on an L-mask so counters can be punched out. Drawing the type straight
# into the RGBA image left the 0s, the %, and a/o/d as solid slabs -- the
# counters are what make it read as type at hero scale.
class TypeMask:
    def __init__(self, wd, ht):
        self.m = Image.new("L", (wd, ht), 0)
        self.d = ImageDraw.Draw(self.m)

    def on(self, pts):
        self.d.polygon(pts, fill=255)

    def off(self, pts):
        self.d.polygon(pts, fill=0)

    def ell_on(self, box):
        self.d.ellipse(box, fill=255)

    def ell_off(self, box):
        self.d.ellipse(box, fill=0)


SL = 0.24                                  # italic slope


def _P(x, y, s, px, py):
    return (x + px * s + (1.0 - py) * SL * s, y + py * s)


def _bar(t, x, y, s, x0, x1, y0=0.0, y1=1.0, cut=False):
    q = [_P(x, y, s, x0, y0), _P(x, y, s, x1, y0),
         _P(x, y, s, x1, y1), _P(x, y, s, x0, y1)]
    (t.off if cut else t.on)(q)


def _ring(t, x, y, s, x0, x1, y0, y1, tw):
    """A bold rounded rectangle with its counter punched out."""
    t.on([_P(x, y, s, x0 + 0.05, y0), _P(x, y, s, x1 - 0.05, y0),
          _P(x, y, s, x1, y0 + 0.12), _P(x, y, s, x1, y1 - 0.12),
          _P(x, y, s, x1 - 0.05, y1), _P(x, y, s, x0 + 0.05, y1),
          _P(x, y, s, x0, y1 - 0.12), _P(x, y, s, x0, y0 + 0.12)])
    t.off([_P(x, y, s, x0 + tw + 0.03, y0 + tw), _P(x, y, s, x1 - tw - 0.03, y0 + tw),
           _P(x, y, s, x1 - tw, y0 + tw + 0.10), _P(x, y, s, x1 - tw, y1 - tw - 0.10),
           _P(x, y, s, x1 - tw - 0.03, y1 - tw), _P(x, y, s, x0 + tw + 0.03, y1 - tw),
           _P(x, y, s, x0 + tw, y1 - tw - 0.10), _P(x, y, s, x0 + tw, y0 + tw + 0.10)])


def glyph_100(t, x, y, s):
    """'100%' -- bold condensed italic, counters punched."""
    # 1: stem plus the angled flag
    _bar(t, x, y, s, 0.13, 0.32)
    t.on([_P(x, y, s, -0.04, 0.22), _P(x, y, s, 0.13, 0.02),
          _P(x, y, s, 0.13, 0.24), _P(x, y, s, 0.01, 0.36)])
    _ring(t, x, y, s, 0.42, 0.78, 0.02, 1.00, 0.13)
    _ring(t, x, y, s, 0.86, 1.22, 0.02, 1.00, 0.13)
    # %: two rings and a slash
    for ox, oy in ((1.34, 0.02), (1.62, 0.56)):
        _ring(t, x, y, s, ox, ox + 0.26, oy, oy + 0.42, 0.085)
    t.on([_P(x, y, s, 1.70, 0.00), _P(x, y, s, 1.88, 0.00),
          _P(x, y, s, 1.50, 1.02), _P(x, y, s, 1.32, 1.02)])


def glyph_calidad(t, x, y, s):
    """'Calidad' -- same idiom, x-height letters with ascenders on l and d."""
    ox = 0.0
    for ch in "Calidad":
        if ch == "C":
            t.on([_P(x, y, s, ox + 0.36, 0.02), _P(x, y, s, ox + 0.12, 0.16),
                  _P(x, y, s, ox + 0.04, 0.44), _P(x, y, s, ox + 0.04, 0.62),
                  _P(x, y, s, ox + 0.12, 0.88), _P(x, y, s, ox + 0.36, 1.02),
                  _P(x, y, s, ox + 0.36, 0.80), _P(x, y, s, ox + 0.22, 0.70),
                  _P(x, y, s, ox + 0.22, 0.34), _P(x, y, s, ox + 0.36, 0.24)])
            ox += 0.46
        elif ch == "a":
            _ring(t, x, y, s, ox + 0.02, ox + 0.34, 0.34, 1.02, 0.115)
            _bar(t, x, y, s, ox + 0.24, ox + 0.36, 0.34, 1.02)
            ox += 0.44
        elif ch == "l":
            _bar(t, x, y, s, ox + 0.02, ox + 0.16, -0.26, 1.02)
            ox += 0.26
        elif ch == "i":
            _bar(t, x, y, s, ox + 0.02, ox + 0.16, 0.34, 1.02)
            _bar(t, x, y, s, ox + 0.03, ox + 0.17, 0.06, 0.24)
            ox += 0.26
        elif ch == "d":
            _ring(t, x, y, s, ox + 0.02, ox + 0.34, 0.34, 1.02, 0.115)
            _bar(t, x, y, s, ox + 0.30, ox + 0.44, -0.26, 1.02)
            ox += 0.54
    return ox


# ------------------------------------------------------------------- bunting
# THERE IS NO BUNTING.  THE LINES ARE VENT SLATS, AND THEY ARE BODYWORK.
#
# rev 46, at the owner's instruction and in two stages.  This decal used to draw
# two red bars across the top of the burst with 15 triangular pennants hanging
# from them.  He asked for the triangles to go; nothing in any frame we hold
# shows them, and magnifying ref_playa_34.png 16x over the strip between the
# roof and the burst shows two thin STRAIGHT lines with plain cream between them
# and the burst -- no triangles, no scallop, nothing hanging.
#
# Then he named what the remaining lines are: VENT SLATS.  He is right, and the
# generator's own palette is the evidence against itself -- BUNT was (198,40,36),
# a saturated RED, and the lines in the photograph are ~~DARK GREY~~.
#
#   RETRACTED rev 47, AND LANDED IN THIS SOURCE ONLY AT REV 49.  In IMG_2073 the
#   slats are BODY COLOUR -- green, the same paint as the panel -- and read dark
#   only because each pressed slot SELF-SHADOWS.  The rev-46 reading came from a
#   frame where the shadow was all that survived.  LEDGER_rev47 sec.10c made this
#   correction and it reached verify_clone.sh:366-367 at rev 48 and NOT this file,
#   so the machine went on handing out the retracted reading for two revisions.
#   A retraction that lands in a ledger and not in the source is half a retraction.
#
# They are the
# T1's rear air-intake louvres: shadowed slots in sheet metal, not paint.  A
# louvre drawn into a decal texture is wrong three times over -- wrong colour,
# wrong material, and it cannot self-shadow or catch a highlight because it has
# no depth at all.
#
# So the whole feature is gone from the artwork rather than recoloured.
#
# AND IT LEAVES A FINDING, REPORTED RATHER THAN QUIETLY FIXED: ~~the model has NO
# REAR VENTS.  `grep -rn 'vent|louvre|slat'` over the sources returns the cab
# door's quarter-light and studio.py's lighting rig, and nothing else.~~
#
#   *** REFUTED AT REV 48.  RETRACTED IN THIS SOURCE AT REV 49. ***
#
#   THIS SENTENCE IS THE FOUNDING CASE OF RULE 1 -- "a claim in a SOURCE COMMENT
#   is not a measurement" -- AND IT WAS STILL STANDING HERE, UNANNOTATED, TWO
#   REVISIONS AFTER IT WAS REFUTED.
#
#   The model HAS had rear vent louvres since rev 16.  Measured off a real
#   T1_SUB=2 build: louvres1 / louvres-1, 560 v each, x -1.5371..-1.2419,
#   z 0.8636..1.0699, TEN slot rows at 21.111 mm pitch.  The grep quoted above
#   returns 140 hits, including t1_detail.py's own "REAR-QUARTER AIR LOUVRES".
#
#   How it propagated is the lesson.  Rev 46 was right to retire the painted
#   lines from the decal -- but those lines sat between the roof and the burst,
#   while the real louvres are on the quarter panel HALF A METRE LOWER.  Rev 46
#   concluded from retiring the PAINT that the GEOMETRY was absent, wrote that
#   conclusion HERE, and three revisions read it as machine truth.  LEDGER_rev46
#   sec.5, LEDGER_rev47 sec.10c and the rev-48 brief's JOB 2 are all wrong, and
#   all three trace to this comment.  SPEC 10.122.1; verify_clone rows 405-407.
#
#   Rev 48 then cut them as real APERTURES (they had been closed ribs on
#   unbroken metal): one hole per flank, blades spanning it, a dark bay behind.
#   Signed modulation +0.0343 -> -0.2559.
#
# Building them is bodywork geometry, not artwork, and it is not in
# the scope of a decal fix -- which remains true, and is why it was done in
# t1_detail.louvres() and not here.


STAR_N = 7
# NOT MEASURED.  The red bus's mark band is one merged 1499-px component in
# every threshold tried -- the frames are blown.  Seven is a POSE CHOICE that
# fills the measured band at the measured mark scale.  Provenance: rev 48, his
# ruling "They are actually stars that were not properly represented"; no
# count is derivable from any frame of the RED bus.

# Band and scale, measured off ref_side.jpg and expressed against the burst.
STAR_BAND_X = (-0.82, 0.82)      # of burst width, about its centre
STAR_BAND_Y = (-0.82, -0.32)     # of burst height, about its centre
STAR_R = 0.085                   # of burst radius; the isolated left-hand
                                 # mark measures 6 x 4 px against a 103 px
                                 # burst width -> 0.05..0.08.  Kept at the
                                 # rev-45 value, which is inside that band.


def _star(d, sx, sy, sr, fill, points=5, dent=0.42, phase=-math.pi / 2):
    sp = []
    for i in range(points * 2):
        a = math.pi * i / points + phase
        r = sr if i % 2 == 0 else sr * dent
        sp.append((sx + r * math.cos(a), sy + r * math.sin(a)))
    d.polygon(sp, fill=fill + (255,))


def _stars(d, cx, cy, RO):
    """The star band above the burst, plus the isolated lower-left mark.

    Positions are DERIVED from the burst's own centre and radius at draw time
    (rule 2), never typed in canvas units, so they follow the burst if it
    moves -- which is exactly what W1 had to fix once already.
    """
    bw = RO * 2.0
    r = STAR_R * RO
    # THE MEASURED BAND IS WIDER THAN THE DECAL PANEL, AND THAT IS A FINDING,
    # NOT A BUG.  +-0.82 of burst WIDTH about its centre is +-1.64 RO, and the
    # canvas holds only ~+-1.0 RO either side of the burst.  On the vehicle
    # those outermost marks are painted on the BODY, beyond this decal's own
    # rectangle; this texture physically cannot carry them.  Clamped to the
    # canvas with a margin, and the number that fell outside is REPORTED
    # rather than silently dropped -- a cap nobody logs reads as coverage.
    mx, my = w * 0.035 + r, h * 0.035 + r
    x0 = max(mx, cx + STAR_BAND_X[0] * bw)
    x1 = min(w - mx, cx + STAR_BAND_X[1] * bw)
    y0 = max(my, cy + STAR_BAND_Y[0] * bw)
    y1 = max(my, cy + STAR_BAND_Y[1] * bw)
    want = [cx + (STAR_BAND_X[0] + (STAR_BAND_X[1] - STAR_BAND_X[0])
                  * i / float(STAR_N - 1)) * bw for i in range(STAR_N)]
    outside = sum(1 for v in want if v < mx or v > w - mx)
    n = 0
    for i in range(STAR_N):
        t = i / float(STAR_N - 1)
        sx = x0 + (x1 - x0) * t
        # two staggered rows, which is how the band reads at 7x
        sy = y0 + (y1 - y0) * (0.18 if i % 2 == 0 else 0.74)
        _star(d, sx, sy, r * (1.0 if i % 2 == 0 else 0.82), PINK,
              phase=-math.pi / 2 + 0.35 * i)
        n += 1
    # the one mark that IS separately resolved: components at x 702..713,
    # y 381..391, i.e. below and LEFT of the burst.  rev 45 drew a star to the
    # left and it was the only one; it stays, moved onto its measured station,
    # clamped into the canvas on the same grounds as the band.
    _star(d, max(mx, cx - 0.92 * bw), min(h - my, cy + 0.52 * bw),
          r * 1.15, PINK)
    print("  stars: %d drawn in the band + 1 isolated; the measured band runs "
          "to +-%.2f RO and the canvas holds +-%.2f RO, so %d of the %d band "
          "positions fall OUTSIDE this decal's own rectangle and are clamped"
          % (n, abs(STAR_BAND_X[0]) * 2.0, (cx - mx) / RO, outside, STAR_N))


def main():
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy, RO = starburst(d)
    img = gradient(img, cx, cy)
    d = ImageDraw.Draw(img)

    # ------------------------------------------------ rev 48: THEY ARE STARS
    # HIS RULING, rev 48, verbatim: "They are actually stars that were not
    # properly represented."
    #
    # He was answering a marked three-way crop of this decal on the RED bus
    # (ref_side.jpg, the target vehicle), the GREEN bus (IMG_2073.jpeg) and
    # the build.  Above the burst the red bus carries a band of marks that
    # rev 45 drew as BUNTING -- two bars with triangular pennants -- and that
    # rev 46 retired at his instruction.  Rev 46 also recorded the reason as
    # "no frame we hold shows them", WHICH IS FALSE: ref_side.jpg shows them
    # plainly at 7x.  What was wrong was not their presence but their
    # IDENTITY, and only he could settle that.  They are stars.
    #
    # WHAT IS MEASURED, on ref_side.jpg, window (700,280)-(870,400), red mask
    # (R - G) > 26, watched print:
    #     the burst        x 733..836  y 306..383   ->  103 x 77 px
    #     the mark band    x 700..869  y 281..320   ->  169 x  39 px
    # Expressed against the burst, so it is dimensionless (rule 14):
    #     band x  -0.82 .. +0.82 of burst WIDTH about its centre
    #     band y  -0.82 .. -0.32 of burst HEIGHT about its centre
    # The band overlaps the burst's upper spikes, which is what the crop shows.
    #
    # WHAT IS NOT MEASURED, AND IT IS THE COUNT.  The band comes back as ONE
    # connected component of 1499 px.  Both red frames are BLOWN in the
    # highlights, so the individual stars do not separate at any threshold --
    # the same failure that stopped this revision measuring the word gap off
    # the red bus.  STAR_N is therefore a POSE CHOICE carrying NOT MEASURED in
    # its own comment, and verify_clone requires that declaration to stay, so
    # a later revision cannot quietly promote it (the LINE_GAP precedent).
    #
    # THE GREEN BUS RESOLVES THEM CLEANLY and is NOT used: he has ruled that
    # artwork may not transfer between the two vehicles, and this revision has
    # measured their decals to be different artwork (spike depth 0.133/0.239
    # against 0.044).  The green frame is admissible for GEOMETRY only.
    _stars(d, cx, cy, RO)

    # type on its own mask so the counters punch through, then rotated as one
    # block so the two lines stay parallel at the measured -19.7 degrees
    t = TypeMask(w, h)
    _pre = _type_centroid()
    TYPE_SHIFT = (BURST_CX - _pre[0], BURST_CY - _pre[1])
    print("  type: pre-rotation centroid (%.4f, %.4f) -> TYPE_SHIFT (%+.4f, %+.4f)"
          % (_pre + TYPE_SHIFT))
    _place(t, TYPE_SHIFT)
    lay = Image.merge("RGBA", (
        Image.new("L", (w, h), WHITE[0]), Image.new("L", (w, h), WHITE[1]),
        Image.new("L", (w, h), WHITE[2]), t.m))
    lay = lay.rotate(-math.degrees(ANG), resample=Image.BICUBIC,
                     center=(w * BURST_CX, h * BURST_CY))
    img = Image.alpha_composite(img, lay)

    # ------------------------------------------------- rev 46, W1: THE GUARD
    # Added in the SAME EDIT as the change it guards (SPEC 10.117 / rule 12).
    # A claim in prose is not a guard: this one MEASURES the shipped raster and
    # refuses to write a decal whose type has drifted off the burst.  It is the
    # check that did not exist for forty-five revisions, which is why "100%
    # calidad off center" survived every one of them.
    _ck = np.array(img).astype(float)
    _al = _ck[:, :, 3] / 255.0
    _wm = (_al > 0.5) & (_ck[:, :, 0] > 200) & (_ck[:, :, 1] > 195) & (_ck[:, :, 2] > 190)
    _ys, _xs = np.nonzero(_wm)
    _tc = (_xs.mean() / _ck.shape[1], _ys.mean() / _ck.shape[0])
    _off = (_tc[0] - BURST_CX, _tc[1] - BURST_CY)
    print("  guard: type centroid (%.4f, %.4f) vs burst centre (%.4f, %.4f) "
          "-> off (%+.4f, %+.4f)" % (_tc + (BURST_CX, BURST_CY) + _off))
    # 0.004 is ~10 px on the 2400-wide master: below the LANCZOS/BICUBIC
    # resampling floor, far under the 0.1167 miss this replaced.
    if abs(_off[0]) > 0.004 or abs(_off[1]) > 0.004:
        raise SystemExit(
            "cal_gen GUARD FAILED: the type is off the burst's centre by "
            "(%+.4f, %+.4f) of the decal, tolerance 0.004.  This is the defect "
            "the owner reported as \"100%% calidad off center\".  Re-derive "
            "TYPE_SHIFT from the pre-rotation centroid; do not widen the "
            "tolerance." % _off)

    img = img.resize((W, H), Image.LANCZOS)
    os.makedirs(TEX, exist_ok=True)
    img.save(os.path.join(TEX, "calidad.png"))
    Image.alpha_composite(Image.new("RGBA", (W, H), (238, 232, 220, 255)),
                          img).convert("RGB").save(
        os.path.join(TEX, "prev_calidad.png"))
    print("wrote tex/calidad.png %dx%d  AR %.3f (measured 1.355)"
          % (W, H, W / H))


if __name__ == "__main__":
    main()
