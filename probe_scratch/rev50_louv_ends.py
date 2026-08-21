import numpy as np
from PIL import Image
import scipy.ndimage as nd
A,B,C = 641220.4, 11140.0, 55.0322
def fX(u): return A/(np.asarray(u,float)+B)-C
im=np.asarray(Image.open('ref_side.jpg').convert('RGB'),float); lum=im.mean(2)
hp = lum - nd.uniform_filter1d(lum,9,axis=0)      # vertical high-pass
for r in (445,454,463,471,472,481,490):
    p=hp[r,740:880]
    print("row %d:"%r)
    print("   "," ".join("%d:%+.0f"%(740+i,v) for i,v in enumerate(p)))
    print()
