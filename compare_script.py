"""
compare_script.py -- the acceptance test for the flank script.

Donald's terms, verbatim: "render the flank, crop the script to the same
framing as the reference, and show me the two side by side at matched scale.
If the letterform skeleton, the swash path and the spiral counters do not line
up, it is not done."

This is the mask-space half of that: generated outline against the photograph's
ink, in the same coordinate frame, same scale, no alignment fudge. It reports
IoU over the whole lockup and per glyph box, so a glyph that has drifted shows
up as a number rather than as an impression.

An IoU in the 0.6-0.75 band is what a faithful redraw of a 271 px source scores
-- the photograph's own edges are two JPEG-blurred pixels wide, so 1.0 is not
reachable and chasing it would mean reproducing compression noise.
"""
import numpy as np
from PIL import Image
from scipy import ndimage as nd

X0, Y0, MW, MH = 325, 486, 290, 114
YPAD = 16                      # script_gen.Canvas pads this many rows above y=0

# rev 10 -- THE REFERENCE MASK WAS WRONG, AND IT WAS WRONG IN THE DIRECTION
# THAT FLATTERED THE GENERATOR.
#
# The old rule was `sat < 0.36 & 55 < max < 228`.  That finds untarnished
# silver and nothing else.  It therefore dropped 'Senor' almost entirely, the
# b flag, and half the i dot -- 1 212 px, 14 % of the real ink -- and the
# generator was then fitted to what was left.  Two consequences that showed up
# as "defects" in the generator and were not:
#   * 'Senor' scored 0.089 and was written off as unfittable.
#   * The lockup was recorded as running "8 % heavy" (8 609 gen against 7 982
#     ref).  Against the true 9 129 px it runs 6 % LIGHT.  Thinning it, as the
#     rev-9 handoff prescribed, would have made it worse.
#
# The rule below is the measured one (measure/script_ink.md sec.1).  It is not a
# tuned threshold: T is the redness of a 50 %-area optical mix of the ink and
# ground endmembers, mixed in LINEAR light and re-encoded -- the locus where a
# pixel is half covered by paint.  The mapping is strongly non-linear because
# of the gamma encoding (25 % coverage already sits at r = 0.275), so a naive
# midpoint would be badly wrong.  Tarnished ink is a different endmember with
# its own 50 %-mix threshold, so the four measured tarnish zones each get their
# own T.  Reproduces 9 129 px +/- 3 %.
def _redness(im):
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    return (R - 0.5 * (G + B)) / np.maximum(R + G + B, 1e-6)


T_SILVER = 0.1409              # 50 % mix of (125.0,122.8,126.9) and (140.9,15.0,5.8)
TARNISH = [                    # (x0, y0, x1, y1, T) in ref_side.jpg pixels
    (325, 469, 355, 492, 0.541),   # S of Senor
    (359, 488, 428, 519, 0.522),   # enor
    (523, 487, 555, 519, 0.558),   # b flag + ascender
    (565, 497, 583, 514, 0.562),   # i dot
]

LOCKUP = (331, 474, 600, 588)  # measured whole-lockup bbox in ref_side.jpg px

# Comparison window: the full measured ink, not the old clipped one.
CY0 = Y0 - YPAD                # 470
CMH = MH + YPAD                # 130


def ref_mask():
    im = np.array(Image.open("ref_side.jpg").convert("RGB")).astype(np.float64)
    r = _redness(im)
    ink = r < T_SILVER
    for x0, y0, x1, y1, T in TARNISH:
        z = np.zeros_like(ink)
        z[y0:y1, x0:x1] = True
        ink |= z & (r < T)
    ink = nd.binary_closing(ink, np.ones((2, 2)))
    ink = nd.binary_opening(ink, nd.generate_binary_structure(2, 1))
    # the measured lockup extent -- outside it is other flank art, the counter
    # and the man's hand, all of which the measurement pass rejected by hand
    keep = np.zeros_like(ink)
    keep[LOCKUP[1]:LOCKUP[3] + 1, LOCKUP[0]:LOCKUP[2] + 1] = True
    ink &= keep
    lab, n = nd.label(ink)
    if n:
        sz = nd.sum(ink, lab, range(1, n + 1))
        ink = np.isin(lab, 1 + np.nonzero(sz >= 12)[0])
    return ink[CY0:CY0 + CMH, X0:X0 + MW]


BOXES = [
    ("T stem+foot", 30, 26, 64, 106),
    ("swash", 4, 14, 118, 52),
    ("a", 52, 44, 96, 94),
    ("c", 90, 40, 132, 90),
    ("o", 128, 38, 168, 86),
    ("m", 164, 30, 220, 80),
    ("b", 216, 2, 252, 74),
    ("i", 244, 12, 280, 62),
    ("Senor", 4, -13, 92, 28),
]


def iou(a, b):
    u = (a | b).sum()
    return (a & b).sum() / u if u else 1.0


def run(gen=None):
    if gen is None:
        gen = np.load("/tmp/gen_alpha.npy")
    G = gen > 96
    R = ref_mask()
    print("\n  %-14s  IoU    gen px   ref px" % "region")
    print("  " + "-" * 42)
    for name, x0, y0, x1, y1 in BOXES:
        a, b = y0 + YPAD, y1 + YPAD
        g, r = G[a:b, x0:x1], R[a:b, x0:x1]
        print("  %-14s  %.3f  %6d   %6d" % (name, iou(g, r), g.sum(), r.sum()))
    print("  " + "-" * 42)
    print("  %-14s  %.3f  %6d   %6d" % ("WHOLE LOCKUP", iou(G, R),
                                        G.sum(), R.sum()))

    # side-by-side + overlay, at 6x
    S = 6
    def up(m, col):
        a = np.kron(m.astype(np.uint8), np.ones((S, S), np.uint8))
        return np.dstack([a * c for c in col]).astype(np.uint8)

    ov = np.zeros((CMH * S, MW * S, 3), np.uint8)
    ov[..., 0] = np.kron(R.astype(np.uint8) * 255, np.ones((S, S), np.uint8))
    ov[..., 1] = np.kron(G.astype(np.uint8) * 255, np.ones((S, S), np.uint8))
    ov[..., 2] = np.kron((R & G).astype(np.uint8) * 255,
                         np.ones((S, S), np.uint8))
    pad = np.zeros((8, MW * S, 3), np.uint8)
    stack = np.vstack([up(R, (1, 1, 1)) * 255 // 255 * 255 if False else
                       up(R, (255, 255, 255)), pad, up(G, (255, 255, 255)),
                       pad, ov])
    Image.fromarray(stack).save("out/script_compare.png")
    print("\n  wrote out/script_compare.png")
    print("  panels: reference ink | generated | overlay "
          "(red=ref only, green=gen only, white=both)")


if __name__ == "__main__":
    run()
