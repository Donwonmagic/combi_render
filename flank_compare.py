"""
flank_compare.py -- the acceptance test Donald set for the flank script, in his
words: "render the flank, crop the script to the same framing as the reference,
and show me the two side by side at matched scale."

Not a self-review. The render is cropped by GEOMETRY, not by eye: the script
panel's model extents (build.py SCR) are projected through the known
orthographic camera, so the crop is the same rectangle the decal occupies -- no
hunting for a framing that flatters it. Both panels are then resampled to the
same width so the comparison is at matched scale.

    python3 flank_compare.py out/r9_side.png out/flank_compare.png
"""
import sys

import numpy as np
from PIL import Image, ImageDraw

# camera: studio.views()["side"] -- orthographic, 5.90 m wide, aimed at
# (0, 0, 1.52) from +Y. Model +X runs to image LEFT in this projection.
ORTHO_W = 5.90
CAM_X, CAM_Z = 0.0, 1.52

# build.py SCR after the rev 9 rebuild
SCR = dict(x0=0.784, x1=-0.494, z0=0.4476, z1=0.9154)

REF_CROP = (325, 486, 606, 594)          # ref_side.jpg, the script + margin
REF_INK = (5, 4, 276, 103)               # measured ink bbox inside that crop


def project(img_w, img_h):
    """Model (x, z) -> pixel. Ortho, so it is linear."""
    ppm = img_w / ORTHO_W

    def f(x, z):
        return (img_w * 0.5 - (x - CAM_X) * ppm,
                img_h * 0.5 - (z - CAM_Z) * ppm)
    return f


def main():
    src, out = sys.argv[1], sys.argv[2]
    im = Image.open(src).convert("RGB")
    W, H = im.size
    f = project(W, H)
    # SCR x0 is the FRONT (larger x) -> smaller pixel x
    xa, ya = f(SCR["x0"], SCR["z1"])
    xb, yb = f(SCR["x1"], SCR["z0"])
    x0, x1 = int(round(min(xa, xb))), int(round(max(xa, xb)))
    y0, y1 = int(round(min(ya, yb))), int(round(max(ya, yb)))
    print("script panel projects to render px x %d-%d  y %d-%d  (%dx%d)"
          % (x0, x1, y0, y1, x1 - x0, y1 - y0))

    gen = im.crop((x0, y0, x1, y1))

    ref_full = Image.open("ref_side.jpg").convert("RGB").crop(REF_CROP)
    ref = ref_full.crop(REF_INK)         # the ink bbox = what SCR represents
    print("reference ink crop %s   generated crop %s" % (ref.size, gen.size))

    # matched scale: both to the same width, heights follow their own aspect
    TW = 1500
    r = ref.resize((TW, int(round(TW * ref.size[1] / ref.size[0]))),
                   Image.LANCZOS)
    g = gen.resize((TW, int(round(TW * gen.size[1] / gen.size[0]))),
                   Image.LANCZOS)
    pad, lab = 14, 34
    canvas = Image.new("RGB", (TW, r.size[1] + g.size[1] + pad + lab * 2),
                       (26, 26, 28))
    d = ImageDraw.Draw(canvas)
    d.text((8, 8), "REFERENCE  ref_side.jpg  (300,470)-(620,570) region, ink bbox",
           fill=(235, 235, 235))
    canvas.paste(r, (0, lab))
    d.text((8, lab + r.size[1] + pad - 24),
           "RENDERED  rev 9 script_gen.py, same panel, matched scale",
           fill=(235, 235, 235))
    canvas.paste(g, (0, lab + r.size[1] + pad + lab - 24))
    canvas.save(out)
    print("wrote %s" % out)


if __name__ == "__main__":
    main()
