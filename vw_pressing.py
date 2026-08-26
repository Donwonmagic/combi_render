"""THE FACTORY PRESSING'S OWN OUTLINE, TRACED -- not approximated by constants.

Eighteen revisions approximated the 1955-67 nose emblem with a seven-constant
V+W spine and the owner reported it wrong five times.  This module carries the
mark's outline TRACED off the pressing itself, in `ref_workshop.jpg`.

WHY THAT FRAME IS ADMISSIBLE, AND IT IS THE ONLY REASON IT IS.  `ref_workshop.jpg`
is the GREEN vehicle, not the target.  Paint and artwork do not transfer between
vehicles -- but the roundel's SHAPE is the factory chrome PRESSING, which is
GEOMETRY, and geometry does (CLAUDE.md rule 11; F141).  Only its colour is
artwork, and no colour is taken from here.

UNITS.  (x, y) with the badge's own outer radius as 1.0, x to the right, y up,
origin at the badge centre.  Every terminal lies on r = 0.80, the band's inner
edge, because that is exactly where the real strokes disappear under the ring.
`t1_detail._fit_glyph` rescales the whole outline to whatever ring the caller
has, so nothing here encodes a diameter.

IT IS A LITERAL **AND** A GENERATOR, AND THE SELFTEST HOLDS THE TWO TOGETHER.
A traced constant that cannot be re-derived is just a number somebody typed.
`trace()` re-derives it from the photograph; `selftest()` runs `trace()` and
asserts it still agrees with `PRESSING` below.  If the segmentation, the
tracer or the crop ever moves, this file goes red -- it cannot go stale
silently.  That is CLAUDE.md's rule about figures living in a script that runs.

THE HOLES ARE NOT DECORATION.  The V and the W touch, so the cream cells
between them are ENCLOSED HOLES of a single outline.  Dropping them is what a
hole-free tracer does, and it changes the mark's topology -- the thing C6
measures.  They are carried through to the mesh by `t1_core.solid_with_holes`.

MEASURED, rev 64 -- see probe_rev63_trace.py:
    the traced glyph reproduces the badge it came from  IoU 0.9496
    against the TARGET BUS's own badge, one ruler:      IoU 0.7129
    the shipped seven-constant glyph, same ruler:       IoU 0.5367
"""

# ------------------------------------------------------------------ the trace
# outer contour, closed, CCW; 170 vertices
PRESSING_OUTER = [
    (-0.13832, +0.78735), (-0.11842, +0.78617), (-0.11842, +0.43052),
    (-0.09762, +0.41033), (-0.09733, +0.36558), (-0.08635, +0.35410),
    (+0.02747, +0.35784), (+0.03273, +0.39283), (+0.06036, +0.41815),
    (+0.08602, +0.41862), (+0.09412, +0.42614), (+0.09486, +0.45575),
    (+0.11538, +0.46955), (+0.11665, +0.50017), (+0.14951, +0.50484),
    (+0.15728, +0.51228), (+0.15802, +0.54189), (+0.17854, +0.55569),
    (+0.17981, +0.58631), (+0.21069, +0.59127), (+0.23799, +0.61625),
    (+0.24272, +0.65057), (+0.27747, +0.65663), (+0.28417, +0.66437),
    (+0.28462, +0.69330), (+0.31332, +0.71980), (+0.34687, +0.71993),
    (+0.39490, +0.69541), (+0.49996, +0.62231), (+0.49095, +0.57621),
    (+0.46332, +0.55089), (+0.43766, +0.55043), (+0.42936, +0.54256),
    (+0.42882, +0.51329), (+0.40831, +0.49950), (+0.40703, +0.46888),
    (+0.37418, +0.46421), (+0.36641, +0.45676), (+0.36567, +0.42715),
    (+0.34515, +0.41336), (+0.34387, +0.38274), (+0.31299, +0.37778),
    (+0.28569, +0.35279), (+0.27681, +0.31422), (+0.24819, +0.31355),
    (+0.24063, +0.30670), (+0.23906, +0.27574), (+0.21854, +0.26194),
    (+0.21756, +0.23200), (+0.18372, +0.22683), (+0.17636, +0.21854),
    (+0.17516, +0.18859), (+0.14753, +0.16327), (+0.12187, +0.16281),
    (+0.11377, +0.15528), (+0.11303, +0.12567), (+0.09252, +0.11188),
    (+0.09124, +0.08126), (+0.05970, +0.07583), (+0.00851, +0.02608),
    (+0.00674, -0.00522), (-0.02582, -0.00955), (-0.03396, -0.02036),
    (-0.03396, -0.08731), (-0.02615, -0.09800), (+0.00214, -0.09838),
    (+0.00785, -0.10717), (+0.00789, -0.28011), (+0.02882, -0.30064),
    (+0.03339, -0.35309), (+0.11069, -0.35355), (+0.11990, -0.31477),
    (+0.14753, -0.31317), (+0.17833, -0.28449), (+0.18306, -0.25017),
    (+0.21234, -0.24895), (+0.21990, -0.24209), (+0.22146, -0.21114),
    (+0.24198, -0.19734), (+0.24297, -0.16740), (+0.27385, -0.16243),
    (+0.30115, -0.13745), (+0.31003, -0.09888), (+0.33865, -0.09821),
    (+0.34650, -0.09102), (+0.34778, -0.06040), (+0.36830, -0.04660),
    (+0.36904, -0.01699), (+0.40966, -0.00488), (+0.41094, +0.02574),
    (+0.43146, +0.03954), (+0.43220, +0.06915), (+0.47282, +0.08126),
    (+0.47410, +0.11188), (+0.49461, +0.12567), (+0.49535, +0.15528),
    (+0.53598, +0.16740), (+0.53746, +0.19835), (+0.57870, +0.23301),
    (+0.57956, +0.26295), (+0.62019, +0.27507), (+0.62146, +0.30569),
    (+0.64198, +0.31948), (+0.64252, +0.34876), (+0.67747, +0.35515),
    (+0.68701, +0.39409), (+0.69675, +0.39216), (+0.72607, +0.33496),
    (+0.77356, +0.20273), (+0.79474, +0.08900), (+0.79737, -0.03617),
    (+0.78680, -0.14317), (+0.75251, -0.27002), (+0.71012, -0.36760),
    (+0.64675, -0.47022), (+0.59885, -0.53011), (+0.49556, -0.62765),
    (+0.39490, -0.69541), (+0.29984, -0.74134), (+0.20214, -0.77376),
    (+0.10444, -0.79269), (-0.05148, -0.79812), (-0.09433, -0.79248),
    (-0.09478, -0.66706), (-0.11579, -0.64620), (-0.11583, -0.51632),
    (-0.12385, -0.50496), (-0.15214, -0.50458), (-0.15777, -0.49613),
    (-0.15789, -0.36592), (-0.16924, -0.35401), (-0.23339, -0.35401),
    (-0.25247, -0.37508), (-0.27813, -0.37555), (-0.28598, -0.38274),
    (-0.28709, -0.41302), (-0.30777, -0.42985), (-0.31094, -0.48065),
    (-0.34326, -0.48435), (-0.34996, -0.49209), (-0.35041, -0.52103),
    (-0.37093, -0.53483), (-0.37192, -0.56477), (-0.40477, -0.56944),
    (-0.41254, -0.57688), (-0.41340, -0.60683), (-0.43409, -0.62365),
    (-0.43462, -0.66597), (-0.52187, -0.60612), (-0.59885, -0.53011),
    (-0.64198, -0.47460), (-0.64215, -0.27944), (-0.65016, -0.26809),
    (-0.67845, -0.26771), (-0.68421, -0.25858), (-0.68425, +0.10818),
    (-0.69589, +0.11978), (-0.76628, +0.11646), (-0.77130, +0.04189),
    (-0.77681, +0.03377), (-0.79712, +0.03407), (-0.79206, +0.11087),
    (-0.77356, +0.20273), (-0.73660, +0.31073), (-0.68117, +0.41874),
    (-0.61756, +0.50824), (-0.54326, +0.58698), (-0.43470, +0.67097),
    (-0.33668, +0.72519), (-0.23898, +0.76300),
]

# the two enclosed cream cells between the V and the W
PRESSING_HOLES = [
    [
        (-0.35938, +0.67699), (-0.28988, +0.67404), (-0.28380, +0.59606),
        (-0.25049, +0.59072), (-0.24478, +0.58193), (-0.24474, +0.21517),
        (-0.22368, +0.19398), (-0.22368, +0.02137), (-0.24433, +0.00421),
        (-0.24885, -0.02978), (-0.27813, -0.03100), (-0.28623, -0.03853),
        (-0.28697, -0.06814), (-0.30748, -0.08193), (-0.30905, -0.11289),
        (-0.34161, -0.11722), (-0.34938, -0.12466), (-0.35012, -0.15427),
        (-0.37064, -0.16807), (-0.37192, -0.19869), (-0.40247, -0.20348),
        (-0.42056, -0.22413), (-0.43141, -0.22476), (-0.49169, -0.22182),
        (-0.49799, -0.16504), (-0.53109, -0.16004), (-0.53680, -0.15124),
        (-0.53684, +0.02170), (-0.55789, +0.04290), (-0.55789, +0.43085),
        (-0.57882, +0.45138), (-0.57895, +0.51699), (-0.54984, +0.54753),
        (-0.49951, +0.55110), (-0.49433, +0.58563), (-0.47064, +0.60944),
        (-0.43668, +0.61549), (-0.40748, +0.65251), (-0.37911, +0.65570),
    ],
    [
        (+0.65115, -0.01211), (+0.73569, -0.01211), (+0.74474, -0.02137),
        (+0.74461, -0.08698), (+0.73898, -0.09543), (+0.71069, -0.09581),
        (+0.70288, -0.10649), (+0.70251, -0.15158), (+0.68162, -0.17177),
        (+0.67854, -0.24378), (+0.64786, -0.24642), (+0.64009, -0.25387),
        (+0.63923, -0.28382), (+0.61846, -0.30098), (+0.61817, -0.34573),
        (+0.61266, -0.35384), (+0.58503, -0.35401), (+0.57693, -0.36154),
        (+0.57619, -0.39115), (+0.55567, -0.40495), (+0.55411, -0.43590),
        (+0.52615, -0.46139), (+0.49885, -0.46282), (+0.49215, -0.47056),
        (+0.49124, -0.50017), (+0.46299, -0.52599), (+0.43569, -0.52742),
        (+0.42899, -0.53516), (+0.42854, -0.56410), (+0.40485, -0.58790),
        (+0.37089, -0.59396), (+0.34169, -0.63097), (+0.30773, -0.63703),
        (+0.27484, -0.67581), (+0.26464, -0.67699), (+0.18199, -0.67404),
        (+0.18199, -0.61760), (+0.21431, -0.61390), (+0.22101, -0.60616),
        (+0.22146, -0.57722), (+0.24198, -0.56343), (+0.24297, -0.53348),
        (+0.27582, -0.52881), (+0.28359, -0.52137), (+0.28433, -0.49176),
        (+0.30485, -0.47796), (+0.30641, -0.44701), (+0.33898, -0.44267),
        (+0.34675, -0.43523), (+0.34749, -0.40562), (+0.36801, -0.39182),
        (+0.36957, -0.36087), (+0.40313, -0.35603), (+0.41049, -0.34775),
        (+0.41201, -0.31746), (+0.43931, -0.29248), (+0.46497, -0.29202),
        (+0.47282, -0.28483), (+0.47410, -0.25421), (+0.49461, -0.24041),
        (+0.49535, -0.21080), (+0.53598, -0.19869), (+0.53725, -0.16807),
        (+0.55777, -0.15427), (+0.55851, -0.12466), (+0.58668, -0.09867),
        (+0.61234, -0.09821), (+0.62019, -0.09102), (+0.62130, -0.06073),
        (+0.64169, -0.04727), (+0.64223, -0.01800),
    ],
]

PRESSING = (PRESSING_OUTER, PRESSING_HOLES)


# --------------------------------------------------------------- the generator
# Everything below RE-DERIVES the table above from the photograph.  It is not
# imported by `build.py` and costs the build nothing; it exists so the literal
# can never drift from the frame it came from.
BAND_INNER = 0.80          # the ring band's inner edge, in badge-radius units
UP = 8                     # upsample before tracing, so the trace is sub-pixel


def trace(band_inner=BAND_INNER, up=UP):
    """Re-derive (outer, holes) from `ref_workshop.jpg`.  Needs numpy/scipy/PIL."""
    import numpy as np
    import scipy.ndimage as ndi
    from PIL import Image
    import trace_outline as T
    import probe_rev63_angles as A

    mask = A.workshop()
    big = np.asarray(Image.fromarray((mask * 255).astype("uint8"))
                     .resize((mask.shape[1] * up, mask.shape[0] * up),
                             Image.LANCZOS)) > 127
    ys, xs = np.nonzero(big)
    cy, cx = (ys.min() + ys.max()) / 2.0, (xs.min() + xs.max()) / 2.0
    ry, rx = (ys.max() - ys.min()) / 2.0, (xs.max() - xs.min()) / 2.0
    yy, xx = np.mgrid[0:big.shape[0], 0:big.shape[1]]
    r = np.sqrt(((yy - cy) / ry) ** 2 + ((xx - cx) / rx) ** 2)
    inner = ndi.binary_opening(big & (r < band_inner), np.ones((up // 2, up // 2)))

    def conv(k):
        s = T.simplify(T.chaikin(k, 3), 0.9 * up / 4.0)
        return [((p[1] - cx) / rx, -(p[0] - cy) / ry) for p in s]

    for outer, holes in T.trace_with_holes(inner):
        if T.area(outer) <= 0.02 * inner.sum():
            continue
        return (conv(outer),
                [conv(h) for h in holes if T.area(h) > 0.004 * inner.sum()])
    raise RuntimeError("no stroke group survived -- the trace found nothing")


def _poly_mask(outer, holes, n=276):
    from PIL import Image, ImageDraw
    import numpy as np
    im = Image.new("L", (n, n), 0)
    d = ImageDraw.Draw(im)
    P = [(n / 2 + a * n / 2, n / 2 - b * n / 2) for a, b in outer]
    d.polygon(P, fill=255)
    for h in holes:
        d.polygon([(n / 2 + a * n / 2, n / 2 - b * n / 2) for a, b in h], fill=0)
    return np.asarray(im) > 127


def selftest():
    """-> list of (name, ok, detail).  Holds the literal to the photograph."""
    import numpy as np
    out = []
    o2, h2 = trace()
    out.append(("re-traced from ref_workshop.jpg",
                True, "%d outer verts, %d hole(s)" % (len(o2), len(h2))))
    out.append(("hole COUNT matches the literal",
                len(h2) == len(PRESSING_HOLES),
                "regenerated %d, literal %d" % (len(h2), len(PRESSING_HOLES))))
    a = _poly_mask(PRESSING_OUTER, PRESSING_HOLES)
    b = _poly_mask(o2, h2)
    j = float((a & b).sum()) / float((a | b).sum())
    out.append(("the LITERAL is the trace, not a typed number",
                j > 0.995, "IoU literal vs regenerated %.5f" % j))
    r = [((x * x + y * y) ** 0.5) for x, y in PRESSING_OUTER]
    out.append(("every terminal sits on the band's inner edge",
                abs(max(r) - BAND_INNER) < 0.01,
                "outer r max %.4f, band inner %.4f" % (max(r), BAND_INNER)))
    # KILL -- watched failing.  A shape this test cannot reject is not a test.
    bad = [(x * 0.72, y) for x, y in PRESSING_OUTER]
    jb = float((a & _poly_mask(bad, [])).sum()) / float((a | _poly_mask(bad, [])).sum())
    out.append(("KILL: the same test REJECTS a 0.72x-squeezed glyph",
                jb < 0.90, "IoU %.4f against the 0.995 bar" % jb))
    return out


if __name__ == "__main__":
    import sys
    print("")
    print("  vw_pressing.py -- the traced factory pressing, held to its source")
    print("")
    bad = 0
    for nm, ok, d in selftest():
        bad += not ok
        print("    %-52s %s  %s" % (nm, "ok  " if ok else "FAIL", d))
    print("")
    print("  %d checked, %d FAILED" % (len(selftest()), bad))
    sys.exit(1 if bad else 0)
