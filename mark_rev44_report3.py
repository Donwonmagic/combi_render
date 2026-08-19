"""mark_rev44_report3 -- the marked crop for SPEC 10.24 item 3.

Draws, on ref_source.jpeg, the two features the ordinal turns on: the topmost-
red-per-column two-tone break (the SAME detector rev 43 used), and the headlamp
lens found by desaturation.  It exists so the reader can see that the lamp sits
CLEAR of the break in the photograph -- which the build does not do.

Columns left of x=38 are NOT marked: rev 43 recorded that the break detector
returns the VW ROUNDEL there, the roundel being red too.  That exclusion is
kept and is why the marked span starts at 38.
"""
import numpy as np
from PIL import Image, ImageDraw

SRC, OUT, Z = "ref_source.jpeg", "rev44_report3_lamp.png", 8
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
red = (R > G + 40) & (R > B + 40) & (R > 90)
sat = a.max(2) - a.min(2)
lens = (sat < 40) & (a.max(2) > 90)

X0, X1, Y0, Y1 = 30, 66, 100, 160
im = Image.open(SRC).convert("RGB").crop((X0, Y0, X1, Y1))
im = im.resize((im.width * Z, im.height * Z), Image.NEAREST)
d = ImageDraw.Draw(im)

def px(x, y):
    return ((x - X0) * Z, (y - Y0) * Z)

# the break, topmost red per column, roundel columns excluded
brk = {}
for x in range(38, X1):
    col = np.nonzero(red[:, x])[0]
    col = col[col > 100]
    if len(col):
        brk[x] = int(col[0])
for x, y in brk.items():
    d.rectangle([px(x, y), (px(x, y)[0] + Z - 1, px(x, y)[1] + Z - 1)],
                fill=(0, 220, 255))
# the lens, clean columns only (42..53: 40/41 leak into the cream above)
for x in range(42, 54):
    col = np.nonzero(lens[118:154, x])[0]
    if len(col):
        d.rectangle([px(x, col.min() + 118),
                     (px(x, col.max() + 118)[0] + Z - 1,
                      px(x, col.max() + 118)[1] + Z - 1)],
                    outline=(255, 240, 0))
d.text((6, 4), "cyan = two-tone break (topmost red/col, x>=38)",
       fill=(0, 220, 255))
d.text((6, 16), "yellow = headlamp lens (desaturated), x42-53", fill=(255, 240, 0))
d.text((6, 28), "break y=117 @x47 ; lens y=129..145 -> 12 px CLEAR red between",
       fill=(255, 255, 255))
d.text((6, 40), "BUILD: the break cuts a 131.9 mm chord ACROSS the lens.",
       fill=(255, 120, 120))
im.save(OUT)
print("wrote %s  (%dx%d, %dx zoom of x%d-%d y%d-%d)"
      % (OUT, im.width, im.height, Z, X0, X1, Y0, Y1))
print("break row at x=47 : %d" % brk[47])
print("break rows x=38..53: %s" % [brk[x] for x in range(38, 54)])
