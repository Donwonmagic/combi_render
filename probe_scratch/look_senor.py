#!/usr/bin/env python3.11
"""Composite tex/senor.png over the body red and put it beside ref_side.jpg
rows 462-598 cols 318-614 AT MATCHED MAGNIFICATION.  Argument 1 = out path,
argument 2 = label."""
import sys, numpy as np
from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS = None
out, label = sys.argv[1], sys.argv[2]
BODY = (196, 49, 36)

ref = Image.open("ref_side.jpg").convert("RGB").crop((318, 462, 614, 598))
RW, RH = ref.size                                   # 296 x 136

s = Image.open("tex/senor.png")
a = np.asarray(s.split()[-1], np.float32) / 255.0
rgb = np.asarray(s.convert("RGB"), np.float32)
bg = np.array(BODY, np.float32)
comp = (rgb * a[..., None] + bg * (1 - a[..., None])).astype(np.uint8)
built = Image.fromarray(comp)

# MATCHED MAGNIFICATION, INK TO INK.  Matching the built ink bbox to the CROP
# width is not matched magnification -- the photograph's ink does not fill its
# crop, so it silently shows the build ~9% larger and makes its edges look
# proportionally softer than they are.  Segment the photograph's own ink
# (silver = low saturation, not dark) and match bbox width to bbox width.
r = np.asarray(ref, np.float32)
mx, mn = r.max(2), r.min(2)
pink = ((mx - mn) / np.maximum(mx, 1) < 0.35) & (mx > 70)
pys, pxs = np.nonzero(pink)
pw = pxs.max() - pxs.min() + 1                       # 271 px
ys, xs = np.nonzero(a > 0.1)
bw = xs.max() - xs.min() + 1
k = pw / float(bw)
nb = built.resize((max(1, int(built.width * k)), max(1, int(built.height * k))),
                  Image.LANCZOS)
# land the built ink bbox on the photograph's ink bbox
ox = int(xs.min() * k) - pxs.min()
oy = int(ys.min() * k) - pys.min()
nb = nb.crop((ox, oy, ox + RW, oy + RH))
print("   matched ink-to-ink: photo ink %d px, built ink %d px -> x%.4f" % (pw, bw, k))

Z = 3
panel = Image.new("RGB", (RW * Z, RH * Z * 2 + 26), (24, 24, 24))
panel.paste(ref.resize((RW * Z, RH * Z), Image.NEAREST), (0, 13))
panel.paste(nb.resize((RW * Z, RH * Z), Image.NEAREST), (0, RH * Z + 26))
d = ImageDraw.Draw(panel)
d.text((6, 2), "ref_side.jpg  462-598 / 318-614  (the bar)", fill=(255, 220, 120))
d.text((6, RH * Z + 15), "BUILT tex/senor.png over body red  -- %s" % label,
       fill=(120, 220, 255))
panel.save(out)
print("wrote %s  %dx%d   built ink bbox %d px -> scaled x%.3f" % (out, panel.width, panel.height, bw, k))
