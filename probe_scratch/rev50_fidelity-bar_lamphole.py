import numpy as np
from PIL import Image
def load(p): return np.asarray(Image.open(p).convert('RGB')).astype(float)

def analyse(path, box, tag):
    im=load(path); y0,y1,x0,x1=box; sub=im[y0:y1,x0:x1]
    R,G,B=sub[...,0],sub[...,1],sub[...,2]
    lum=sub.mean(axis=2)
    # amber lamp: warm, G/R around 0.45-0.65, moderately bright
    amber=(R>90)&(G>0.33*R)&(G<0.78*R)&(B<0.55*R)
    # body salmon red inside the lamp: much higher B/R and higher lum than amber
    red=(R>150)&(G<0.62*R)&(B>0.30*R)
    ys,xs=np.nonzero(amber)
    if len(xs)==0: print(tag,"no amber"); return
    A=amber.sum(); Ra=np.sqrt(A/np.pi)
    ys2,xs2=np.nonzero(red)
    print("%s  amber px %d (equiv R %.2f)  red-core px %d (equiv R %.2f)  ratio %.3f"
          %(tag,A,Ra,red.sum(),np.sqrt(max(red.sum(),0)/np.pi),
            np.sqrt(max(red.sum(),1)/np.pi)/Ra))
    if red.sum():
        print("    red core bbox x %d..%d y %d..%d ; amber bbox x %d..%d y %d..%d"
              %(xs2.min()+x0,xs2.max()+x0,ys2.min()+y0,ys2.max()+y0,
                xs.min()+x0,xs.max()+x0,ys.min()+y0,ys.max()+y0))
        print("    red core centroid (%.1f,%.1f)  amber centroid (%.1f,%.1f)"
              %(xs2.mean()+x0,ys2.mean()+y0,xs.mean()+x0,ys.mean()+y0))
        print("    red core W %d H %d ; amber W %d H %d ; W ratio %.3f"
              %(xs2.max()-xs2.min()+1, ys2.max()-ys2.min()+1,
                xs.max()-xs.min()+1, ys.max()-ys.min()+1,
                (xs2.max()-xs2.min()+1)/(xs.max()-xs.min()+1)))

analyse('out/r49s_rear.png',(815,905,478,572),'r49s_rear  LEFT lamp ')
analyse('out/r49s_rear.png',(815,905,1030,1124),'r49s_rear  RIGHT lamp')

# PREDICTION from the source geometry
R=1.1627*0.0  # placeholder
print("\nPREDICTION: small_lamp profile (0,0)->(0.45d,0.55r); the lamp base plane sits")
print("  4.0 mm FORWARD of X_TAIL (build.py:564 loc x = X_TAIL + 0.0040), so a flat")
print("  tail skin at X_TAIL cuts the cone at t = 0.0040 of a 0.0270 depth:")
d=0.0270
t=0.0040
frac=0.55*(t/(0.45*d))
print("  radius fraction of the lamp buried = 0.55 * (0.0040 / (0.45*0.0270)) = %.4f"%frac)
print("  -> predicted red-core diameter / lamp diameter = %.3f"%frac)
