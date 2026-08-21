"""rev50 -- the VW glyph's INK-PER-ROW profile, normalised to the roundel's
own vertical extent.  Scale-free and yaw-free (the vertical axis of a circle
on a yawed panel is unforeshortened), so a render and a photograph at
different poses are directly comparable.

For each row inside the ring, count the fraction of the ROW'S OWN chord that
is glyph ink.  The V/W's crossing height shows as the minimum of that profile.
CEILING: ink is thresholded on the paint's own colour channel; the ring
itself is excluded by taking only the central 70 % of each chord, so a row's
value is ink INSIDE the ring, not ring + ink.  Rows near the top and bottom
have short chords and are noisy -- n per row is printed.
"""
import numpy as np
from PIL import Image

def prof(path, box, chan, thr, label, top, bot):
    im = np.asarray(Image.open(path).convert('RGB')).astype(float)
    x0,y0,x1,y1 = box
    if chan == 'RG': C = im[...,0]-im[...,1]     # red ink on cream
    else:            C = im[...,1]-im[...,0]
    out=[]
    for y in range(y0,y1):
        row = C[y, x0:x1]
        ink = row > thr
        if ink.sum() < 2: out.append((y,0.0,0)); continue
        l,r = np.nonzero(ink)[0][[0,-1]]
        span = r-l+1
        m = int(span*0.15)
        inner = ink[l+m:r-m+1]
        out.append((y, inner.mean() if len(inner) else 0.0, len(inner)))
    print(label)
    print("  t     ink   chord")
    for y,f,n in out:
        t = (y-top)/(bot-top)
        if 0.02 <= t <= 0.98 and n>4:
            print("  %.3f  %.3f  %3d  %s" % (t, f, n, "#"*int(f*40)))

prof('out/r49s_front.png', (735,712,865,838), 'RG', 14, 'RENDER r49s_front (head-on)', 715, 833)
prof('ref_nolita_front34.jpg', (152,188,198,248), 'RG', 40, 'PHOTO ref_nolita_front34', 190, 245)
