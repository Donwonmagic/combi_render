"""rev50 A2 instrument, v2.  v1 WAS WRONG and is kept in m5.py as the record of the error:
it took the last CONTIGUOUS red run from the centre outward, and the hubcap's VW emblem is a
light-coloured hole at the centre, so every ray terminated on the emblem (median r 8.25 px on a
~33 px dome) and produced a plausible m5 that was meaningless.

v2 takes the OUTERMOST red radius inside a bound that sits within the cream ring, and adds a
CONTROL WITH A CENTRAL EMBLEM that kills v1.  Controls run before any real image.
"""
import numpy as np
from PIL import Image
RED = lambda px: (px[:,0] > 85) & (px[:,1] < 0.70*px[:,0])

def prof_outer(arr, cx, cy, rmax, n=720, red=RED):
    th=np.linspace(0,2*np.pi,n,endpoint=False); rr=np.arange(1.0,rmax,0.25)
    H,W=arr.shape[:2]; out=np.full(n,np.nan)
    for i,t in enumerate(th):
        xs=cx+rr*np.cos(t); ys=cy+rr*np.sin(t)
        ok=(xs>=0)&(xs<W-1)&(ys>=0)&(ys<H-1)
        px=arr[np.clip(ys.astype(int),0,H-1),np.clip(xs.astype(int),0,W-1)].astype(float)
        g=ok&red(px); idx=np.where(g)[0]
        if len(idx): out[i]=rr[idx[-1]]
    return out

def harm(p,ms=(1,2,3,4,5,6,7)):
    p=p[~np.isnan(p)]
    if len(p)<100: return None
    n=len(p); th=np.linspace(0,2*np.pi,n,endpoint=False); mu=p.mean()
    return {m:2*abs(np.sum(p*np.exp(-1j*m*th)))/n/mu for m in ms}

def synth(petals,amp,R=32.0,size=200,emblem=0.0):
    a=np.zeros((size,size,3),np.uint8); a[:,:]=(210,205,190)
    yy,xx=np.mgrid[0:size,0:size]; c=size/2
    t=np.arctan2(yy-c,xx-c); r=np.hypot(xx-c,yy-c)
    Rl=R*(1.0+(amp*np.cos(petals*t) if petals else 0.0))
    a[r<=Rl]=(190,55,40)
    if emblem: a[r<=R*emblem]=(235,235,230)     # the light VW emblem, which killed v1
    return a

print("=== CONTROLS ===")
for name,pet,amp,emb in (("perfect circle",0,0.0,0.0),
                         ("perfect circle + EMBLEM",0,0.0,0.30),
                         ("5-petal +8%",5,0.08,0.0),
                         ("5-petal +8% + EMBLEM",5,0.08,0.30),
                         ("3-petal +8% + EMBLEM (kill)",3,0.08,0.30)):
    a=synth(pet,amp,emblem=emb); h=harm(prof_outer(a,100.0,100.0,45))
    pr=prof_outer(a,100.0,100.0,45); g=pr[~np.isnan(pr)]
    print(f"  {name:30s} r_med {np.median(g):5.2f}  " + " ".join(f"m{m}={h[m]:.4f}" for m in sorted(h)))

def hub(arr,box):
    x0,y0,x1,y1=box
    m=RED(arr[y0:y1,x0:x1].astype(float).reshape(-1,3)).reshape(y1-y0,x1-x0)
    ys,xs=np.nonzero(m); return x0+xs.mean(), y0+ys.mean(), m.sum()

print()
print("=== REAL IMAGES ===  (rmax chosen to sit inside the cream ring, stated per target)")
for label,f,box,rmax in (
    ("RENDER r50a_side REAR ","out/r50a_side.png",(1030,800,1170,940),50),
    ("RENDER r50a_side FRONT","out/r50a_side.png",(380,800,520,940),50),
    ("PHOTO  ref_side   REAR","ref_side.jpg",(715,570,785,640),40)):
    arr=np.array(Image.open(f).convert("RGB"))
    cx,cy,n=hub(arr,box); p=prof_outer(arr,cx,cy,rmax); h=harm(p); g=p[~np.isnan(p)]
    print(f"  {label} centre({cx:.1f},{cy:.1f})  rmax={rmax}")
    print(f"     r  med {np.median(g):6.2f}  p10 {np.percentile(g,10):6.2f}  p90 {np.percentile(g,90):6.2f}  max {g.max():6.2f} px")
    print("     "+" ".join(f"m{m}={h[m]:.4f}" for m in sorted(h)))
    # threshold sweep -- is m5 stable?
    for lo,k in ((75,0.75),(95,0.62),(110,0.60)):
        R2=lambda px,lo=lo,k=k:(px[:,0]>lo)&(px[:,1]<k*px[:,0])
        h2=harm(prof_outer(arr,cx,cy,rmax,red=R2))
        print(f"        thr R>{lo} G<{k}R  ->  m5={h2[5]:.4f}   (m2={h2[2]:.4f} m3={h2[3]:.4f} m4={h2[4]:.4f})")
