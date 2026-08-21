"""rev 50 -- the same question, with a control that actually works.

TEST.  Take ref_playa_34.png, decimate it to ref_source.jpeg's 246x197 grid and
put it back to 500x400 (Lanczos both ways).  That round trip destroys exactly
the information the source copy's pixel grid cannot hold.  The residual
|real - roundtrip| is then the detail the 500 px file has and the 246 px file
cannot.  It is compared against the SAME residual computed on a deliberately
featureless crop of flat paint, which is the noise floor.

CEILING.  This measures what the SAMPLING GRID costs, not what the lens
resolved.  It cannot tell whether ref_source's extra loss (JPEG at 246 px, a
different sharpening) is worse still -- so the figures below are a LOWER bound
on what re-measuring on the 500 px file buys.
"""
import numpy as np
from PIL import Image
pla = Image.open('ref_playa_34.png').convert('L')
rt  = pla.resize((246,197), Image.LANCZOS).resize((500,400), Image.LANCZOS)
src = Image.open('ref_source.jpeg').convert('L').resize((500,400), Image.LANCZOS)
P = np.asarray(pla,float); R = np.asarray(rt,float); S = np.asarray(src,float)
CROPS = {
 "nose hardware (roundel+lamp+indicator)": (20,190,180,300),
 "the 100% Calidad burst":                 (415,110,470,170),
 "senor Tacombi script":                   (285,375,420,470),
 "flat cream roof  = NOISE FLOOR":         (200,150,330,200),
 "whole frame":                            (0,0,500,400),
}
print("%-42s %9s %9s %9s" % ("crop","grid-loss","vs floor","src resid"))
x0,y0,x1,y1 = CROPS["flat cream roof  = NOISE FLOOR"]
floor = np.abs(P-R)[y0:y1,x0:x1].mean()
for nm,(x0,y0,x1,y1) in CROPS.items():
    d  = np.abs(P-R)[y0:y1,x0:x1].mean()
    ds = np.abs(P-S)[y0:y1,x0:x1].mean()
    print("%-42s %9.2f %9.2fx %9.2f" % (nm, d, d/floor, ds))
print("\nnoise floor (flat paint) = %.2f DN" % floor)
