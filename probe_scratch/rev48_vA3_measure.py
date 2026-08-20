import numpy as np, sys
from PIL import Image
from scipy import ndimage as nd
Image.MAX_IMAGE_PIXELS=None

def burstbox(f, box, rg=40, rb=25, R0=90):
    im = Image.open(f).convert("RGB").crop(box)
    a = np.asarray(im, np.float32)
    R,G,B = a[...,0],a[...,1],a[...,2]
    red = (R>R0)&(R-G>rg)&(R-B>rb)
    burst = nd.binary_fill_holes(nd.binary_closing(red, np.ones((5,5))))
    lab,n = nd.label(burst)
    if n==0: return None
    sizes = nd.sum(burst, lab, range(1,n+1))
    k = int(np.argmax(sizes))+1
    m = lab==k
    ys,xs = np.nonzero(m)
    return (f, box, xs.min()+box[0], xs.max()+box[0], ys.min()+box[1], ys.max()+box[1],
            xs.max()-xs.min()+1, ys.max()-ys.min()+1, int(m.sum()))

for f,box in [("ref_rear34.jpg",(700,230,920,430)),
              ("ref_side.jpg",(700,260,880,410)),
              ("IMG_2073.jpeg",(1108,360,1210,445)),
              ("ref_playa_34.png",(0,0,500,400)),
              ("ref_workshop.jpg",(0,0,1200,824))]:
    r = burstbox(f,box)
    if r: print("%-18s bbox x %d-%d y %d-%d   size %d x %d px   area %d" % (r[0],r[2],r[3],r[4],r[5],r[6],r[7],r[8]))
