"""rev 50 -- SPEC 8.4 again, this time honouring its own word MINIMA, and with
a much wider window search.  Statistic: for each column in the range take the
MINIMUM luminance over the row band, then average those minima across columns.
Also tried: plain mean, and the per-column median.
"""
import numpy as np
from PIL import Image
S = np.asarray(Image.open('ref_source.jpeg').convert('RGB'), float).mean(2)
P = np.asarray(Image.open('ref_playa_34.png').convert('RGB'), float).mean(2)
BANDS=[(137,158),(163,180),(185,202),(205,228)]
TGT=[61.6,71.6,106.4]
def stat(img,y0,y1,a,b,kind):
    blk=img[y0:y1, a:b+1]
    if kind=='min': return blk.min(axis=0).mean()
    if kind=='mean': return blk.mean()
    if kind=='med': return np.median(blk,axis=0).mean()
for kind in ('min','mean','med'):
    best=None
    for y0 in range(0, S.shape[0]-3):
        for hh in range(3, 45):
            y1=y0+hh
            if y1>S.shape[0]: break
            v=[stat(S,y0,y1,a,b,kind) for a,b in BANDS]
            err=sum(abs(v[i]-TGT[i]) for i in range(3))+max(0,178-v[3])+max(0,v[3]-204)
            if best is None or err<best[0]: best=(err,y0,y1,v)
    err,y0,y1,v=best
    print("%-5s best rows %3d..%3d -> %6.1f %6.1f %6.1f  bright %6.1f   err %.1f"
          %(kind,y0,y1,v[0],v[1],v[2],v[3],err))
