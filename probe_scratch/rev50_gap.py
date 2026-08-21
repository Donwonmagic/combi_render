"""Arch-to-tyre gap at each axle, render vs ref_side.jpg.
DIMENSIONLESS on both sides: gap / tyre radius, so no px/m enters.
render: exact ortho.  ref: measured in px and divided by the frame's own
tyre radius at that wheel (front R=44.18 px free fit, rear R=29.43 px hubcap ->
rim ring 93.7 px tall => R_tyre measured directly below)."""
import numpy as np
from PIL import Image
import scipy.ndimage as nd

def col_profile(a,c,r0,r1):
    return a[r0:r1,c-1:c+2].mean(1)

print("=== RENDER (out/r49board_side.png) ===")
g=np.asarray(Image.open('out/r49board_side.png').convert('RGB'),float)
gl=g.mean(2); ppm=1600/5.90
for name,X in (("front",1.300),("rear",-1.100)):
    c=int(round(800-ppm*X))
    p=col_profile(gl,c,500,1000)
    rows=np.arange(500,1000)
    dark=p<90
    # tyre top = first dark row scanning down from z=0.9 ; arch = body/dark boundary above it
    idx=np.where(dark)[0]
    print("  %s col %d: first dark row %d (z %.4f), last dark %d"%(name,c,rows[idx[0]],(550+ppm*1.52-rows[idx[0]])/ppm,rows[idx[-1]]))
    print("     profile 610..700:", " ".join("%d:%.0f"%(500+i,p[i]) for i in range(110,200,3)))
