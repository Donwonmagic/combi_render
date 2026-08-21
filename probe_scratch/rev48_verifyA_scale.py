"""Is C1's 'BUILT at photo scale' actually at the photograph's scale?"""
import numpy as np
from PIL import Image
from scipy import ndimage as nd
Image.MAX_IMAGE_PIXELS=None
def type_mask(img,Z):
    big=img.resize((img.width*Z,img.height*Z),Image.LANCZOS)
    a=np.asarray(big.convert("RGB"),np.float32)
    R,G,B=a[...,0],a[...,1],a[...,2]
    mx=a.max(2);sat=(mx-a.min(2))/np.maximum(mx,1)
    red=(R>90)&(R-G>40)&(R-B>25)
    burst=nd.binary_fill_holes(nd.binary_closing(red,np.ones((9,9))))
    lab,n=nd.label(burst)
    if n>1: burst=lab==(int(np.argmax(nd.sum(burst,lab,range(1,n+1))))+1)
    ty=nd.binary_opening(burst&(mx>150)&(sat<0.30),np.ones((5,5)))
    return ty,burst
def bbox(m,Z):
    ys,xs=np.nonzero(m); return (xs.max()-xs.min()+1)/Z,(ys.max()-ys.min()+1)/Z
d=Image.open("tex/calidad.png").convert("RGB")
k=44/float(d.width)*3.0
small=d.resize((max(8,int(d.width*k)),max(8,int(d.height*k))),Image.LANCZOS)
print("probe's 'built at photo scale' canvas:",small.size,"  k=%.4f"%k)
ty,bu=type_mask(small,8)
print("  BUILT burst bbox  %.1f x %.1f native px   type px %d"%(bbox(bu,8)+(ty.sum(),)))
print("  BUILT type  bbox  %.1f x %.1f"%bbox(ty,8))
im=Image.open("IMG_2073.jpeg").convert("RGB").crop((1108,360,1210,445))
ty2,bu2=type_mask(im,8)
print("  PHOTO burst bbox  %.1f x %.1f native px   type px %d"%(bbox(bu2,8)+(ty2.sum(),)))
print("  PHOTO type  bbox  %.1f x %.1f"%bbox(ty2,8))
print("  scale mismatch (built burst / photo burst): w %.2fx  h %.2fx"%(
    bbox(bu,8)[0]/bbox(bu2,8)[0], bbox(bu,8)[1]/bbox(bu2,8)[1]))
# save masks side by side for eyeballing
def png(m,path):
    Image.fromarray((m*255).astype(np.uint8)).save(path)
png(ty,"probe_scratch/rev48_verifyA_mask_built.png")
png(ty2,"probe_scratch/rev48_verifyA_mask_photo.png")
