"""Slot COUNT and pitch on the GREEN bus, IMG_2073.jpeg (geometry transfers; owner ruling).
A count is projectively invariant -- it needs no scale at all."""
import numpy as np
from PIL import Image
import scipy.ndimage as nd
im=np.asarray(Image.open('IMG_2073.jpeg').convert('RGB'),float)
lum=im.mean(2)
hp=lum-nd.uniform_filter1d(lum,7,axis=0)
print("shape",im.shape)
# block roughly x 1158..1188, y 480..550 (from the x10 crop, origin 1130,460)
for c0,c1 in [(1160,1166),(1166,1172),(1172,1178),(1155,1185)]:
    p=hp[470:560,c0:c1].mean(1)
    print("\ncols %d-%d"%(c0,c1))
    for i,v in enumerate(p):
        print("   row %d %+7.2f %s"%(470+i,v,("-"*int(-v)) if v<0 else "+"*int(v)))
