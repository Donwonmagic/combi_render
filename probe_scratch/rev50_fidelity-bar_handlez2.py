import numpy as np
from PIL import Image
def col(im,x,y0,y1,w=2): return im[y0:y1, x-w:x+w+1].mean(axis=(1,2)), im[y0:y1, x-w:x+w+1].mean(axis=1)

# ---------- GREEN BUS, IMG_2073, cab door, column x=820 ----------
G=np.asarray(Image.open('IMG_2073.jpeg').convert('RGB')).astype(float)
y0,y1=440,620
lum,rgb=col(G,820,y0,y1)
gr=rgb[:,1]-rgb[:,0]
# glass bottom = last row of the dark glass before the bright cream band
bright=np.nonzero(lum>200)[0]
gb=y0+bright.min()                     # first bright cream row
brk=y0+np.nonzero(gr>25)[0].min()      # first green row
# handle: desaturated dark rows below brk
h=[y0+i for i in range(len(lum)) if (y0+i)>brk and lum[i]<125 and gr[i]<35]
print("GREEN  glass/cream boundary y=%d   white/green break y=%d   band=%d px"%(gb,brk,brk-gb))
print("       handle rows %s  centre %.1f  -> %.1f px BELOW break = %.2f band heights"
      %(h, np.mean(h), np.mean(h)-brk, (np.mean(h)-brk)/(brk-gb)))

# ---------- RENDER, r49base_side.png, cab door, column x=505 (X=+1.088) ----------
R=np.asarray(Image.open('out/r49base_side.png').convert('RGB')).astype(float)
y0,y1=560,700
lum,rgb=col(R,505,y0,y1)
rr=rgb[:,0]-rgb[:,1]
bright=np.nonzero(lum>150)[0]
gb=y0+bright.min()
brk=y0+np.nonzero(rr>40)[0].min()
print("RENDER glass/cream boundary y=%d   cream/red break y=%d   band=%d px"%(gb,brk,brk-gb))
for y in range(y0,y1):
    i=y-y0
    print("   y=%d lum %6.1f  R-G %+6.1f"%(y,lum[i],rr[i]))
