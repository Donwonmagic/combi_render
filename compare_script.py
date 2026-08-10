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

BOXES = [
    ("T stem+foot", 30, 26, 64, 106),
    ("swash", 4, 14, 118, 52),
    ("a", 52, 44, 96, 94),
    ("c", 90, 40, 132, 90),
    ("o", 128, 38, 168, 86),
    ("m", 164, 30, 220, 80),
    ("b", 216, 2, 252, 74),
    ("i", 244, 12, 280, 62),
    ("Senor", 8, 0, 104, 30),
]


def ref_mask():
    im = np.array(Image.open("ref_side.jpg").convert("RGB")).astype(np.float64)
    w = im[Y0:Y0 + MH, X0:X0 + MW]
    mx, mn = w.max(axis=2), w.min(axis=2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
    ink = (sat < 0.36) & (mx > 55) & (mx < 228)
    return nd.binary_closing(ink, np.ones((2, 2)))


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
        g, r = G[y0:y1, x0:x1], R[y0:y1, x0:x1]
        print("  %-14s  %.3f  %6d   %6d" % (name, iou(g, r), g.sum(), r.sum()))
    print("  " + "-" * 42)
    print("  %-14s  %.3f  %6d   %6d" % ("WHOLE LOCKUP", iou(G, R),
                                        G.sum(), R.sum()))

    # side-by-side + overlay, at 6x
    S = 6
    def up(m, col):
        a = np.kron(m.astype(np.uint8), np.ones((S, S), np.uint8))
        return np.dstack([a * c for c in col]).astype(np.uint8)

    ov = np.zeros((MH * S, MW * S, 3), np.uint8)
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
