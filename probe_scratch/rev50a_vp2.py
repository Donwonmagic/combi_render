import numpy as np
from PIL import Image
A = np.asarray(Image.open('/home/user/combi_render/ref_side.jpg').convert('RGB')).astype(float)
R,G,B = A[:,:,0],A[:,:,1],A[:,:,2]
YEL = (R+G)/2.0 - B
for r in (60,100,150,200,250,285):
    print("row",r,"L window 295..360:", " ".join("%3d"%v for v in YEL[r,295:361:2]))
print()
for r in (40,80,140,200,260):
    print("row",r,"R window 730..790:", " ".join("%3d"%v for v in YEL[r,730:791:2]))
