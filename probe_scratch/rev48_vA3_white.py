import numpy as np
from PIL import Image
from scipy import ndimage as nd
Image.MAX_IMAGE_PIXELS=None
def show(f,box,Z,sats,mxs,out):
    im=Image.open(f).convert("RGB").crop(box)
    big=im.resize((im.width*Z,im.height*Z),Image.LANCZOS)
    a=np.asarray(big,np.float32)
    mx=a.max(2); mn=a.min(2); sat=(mx-mn)/np.maximum(mx,1)
    R,G,B=a[...,0],a[...,1],a[...,2]
    red=(R>80)&(R-G>30)
    reddil=nd.binary_dilation(red,np.ones((9,9)))
    panes=[]
    for s in sats:
        for m in mxs:
            w=(sat<s)&(mx>m)&reddil
            w=nd.binary_opening(w,np.ones((5,5)))
            lab,n=nd.label(w)
            if n:
                sz=nd.sum(w,lab,range(1,n+1))
                keep=[i+1 for i in range(n) if sz[i]>(Z*Z*2)]
                w=np.isin(lab,keep)
            panes.append((s,m,w.astype(np.uint8)*255,int(w.sum())))
    H,W=panes[0][2].shape
    can=Image.new("L",(W*len(panes)//1,H))
    for i,(s,m,img,c) in enumerate(panes):
        can.paste(Image.fromarray(img),(i*W,0)); print("  sat<%.2f mx>%d -> %d px"%(s,m,c))
    can.resize((can.width//Z*2,can.height//Z*2)).save(out)
print("ref_side")
show("ref_side.jpg",(728,300,845,392),6,[0.20],[170,200,225],"probe_scratch/rev48_vA3_w_side.png")
print("ref_rear34")
show("ref_rear34.jpg",(748,288,862,378),6,[0.20],[170,200,225],"probe_scratch/rev48_vA3_w_rear.png")
