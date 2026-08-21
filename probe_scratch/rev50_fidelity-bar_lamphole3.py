import numpy as np
from PIL import Image
im=np.asarray(Image.open('out/r49s_rear.png').convert('RGB')).astype(float)
sub=im[800:930, 460:600]
R,G,B=sub[...,0],sub[...,1],sub[...,2]
lum=sub.mean(axis=2)
print("distinct tones in the box (rounded):")
# print a coarse map
sym=np.full(sub.shape[:2],'.',dtype='<U1')
sym[(R>60)&(R<112)&(G<0.75*R)]='a'        # amber lamp
sym[(R>=112)&(G<0.45*R)&(B>0.15*R)]='#'   # bright red core
sym[(R>140)&(G<0.42*R)]='r'               # body paint
for y in range(0,130,2):
    print("%3d "%(800+y)+''.join(sym[y,::2]))
