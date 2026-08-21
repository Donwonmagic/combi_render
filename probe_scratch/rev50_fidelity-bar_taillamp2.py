import numpy as np
from PIL import Image
P=np.asarray(Image.open('ref_rear34.jpg').convert('RGB')).astype(float)
sub=P[640:725, 915:975]
R,G,B=sub[...,0],sub[...,1],sub[...,2]
lum=sub.mean(axis=2); sat=(sub.max(axis=2)-sub.min(axis=2))/np.maximum(sub.max(axis=2),1)
# metal = desaturated AND bright-ish
metal=(sat<0.66)&(lum>70)
lens =(sat>0.72)&(lum<70)&(R>70)
print("metal px",metal.sum()," lens px",lens.sum())
# lens bounding box + per-row width
ys,xs=np.nonzero(lens)
print("lens bbox x %d..%d (w %d)  y %d..%d (h %d)  AR %.3f"
      %(xs.min(),xs.max(),xs.max()-xs.min()+1,ys.min(),ys.max(),ys.max()-ys.min()+1,
        (ys.max()-ys.min()+1)/(xs.max()-xs.min()+1)))
H=ys.max()-ys.min()+1; W=xs.max()-xs.min()+1
print("\nrow  width  ellipse_pred  rect_pred")
rows=[]
for y in range(ys.min(),ys.max()+1):
    w=lens[y,:].sum()
    if w==0: continue
    t=(y-(ys.min()+ys.max())/2)/(H/2.0)
    ell=W*np.sqrt(max(0.0,1-t*t))
    rows.append((y,w,ell,t))
for (y,w,ell,t) in rows: print("%3d  %5d   %6.2f   t=%+.2f"%(y,w,ell,t))
ws=np.array([r[1] for r in rows]); ell=np.array([r[2] for r in rows])
mid=[r for r in rows if abs(r[3])<0.6]
wm=np.array([r[1] for r in mid]); em=np.array([r[2] for r in mid])
print("\n|t|<0.6:  measured width mean %.2f sd %.2f   ellipse-pred mean %.2f"
      %(wm.mean(),wm.std(),em.mean()))
print("rms(measured - ellipse) over |t|<0.9 = %.2f px"
      %np.sqrt(np.mean((ws[np.abs([r[3] for r in rows])<0.9]-ell[np.abs([r[3] for r in rows])<0.9])**2)))
print("rms(measured - constant W) over |t|<0.9 = %.2f px"
      %np.sqrt(np.mean((ws[np.abs([r[3] for r in rows])<0.9]-W)**2)))
