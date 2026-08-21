import numpy as np
from PIL import Image
A = np.asarray(Image.open('/home/user/combi_render/ref_side.jpg').convert('RGB')).astype(float)
H,W,_=A.shape
R,G,B = A[:,:,0],A[:,:,1],A[:,:,2]
Y = 0.299*R+0.587*G+0.114*B
YEL = (R+G)/2.0 - B

def edge_row(ch,r,xc,half,sign,minstep=12.0):
    x0,x1=int(round(xc-half)),int(round(xc+half))
    if x0<0 or x1>=W: return None
    seg=ch[r,x0:x1+1].astype(float)
    if sign<0: seg=-seg
    n=len(seg); q=max(3,n//4)
    lo=np.median(seg[:q]); hi=np.median(seg[-q:])
    if hi-lo<minstep: return None
    t=0.5*(lo+hi)
    idx=np.where(seg>=t)[0]
    if len(idx)==0 or idx[0]==0: return None
    i=idx[0]; a,b=seg[i-1],seg[i]
    if b==a: return None
    return x0+(i-1)+(t-a)/(b-a)

def track(ch,rows,x_seed,slope,half,sign,label,minstep=12.0,verbose=True):
    a,b=slope,x_seed-slope*rows[len(rows)//2]
    b=x_seed-slope*rows[len(rows)//2]
    for it in range(7):
        pts=[]
        for r in rows:
            e=edge_row(ch,r,a*r+b,half,sign,minstep)
            if e is not None: pts.append((r,e))
        if len(pts)<12: 
            if verbose: print(label,"FAILED n=%d"%len(pts))
            return None,None,None
        ys=np.array([p[0] for p in pts],float); xs=np.array([p[1] for p in pts])
        p=np.polyfit(ys,xs,1); res=xs-np.polyval(p,ys); s=res.std()
        k=np.abs(res)<2.0*max(s,0.4)
        p=np.polyfit(ys[k],xs[k],1); a,b=p; half=max(3.5,half*0.72)
    res=xs[k]-np.polyval(p,ys[k])
    if verbose:
        print("%-30s n=%3d slope=%+.5f  x@y150=%7.2f  rms=%.2f  rows %d-%d"%(
            label,int(k.sum()),p[0],p[0]*150+p[1],res.std(),ys[k].min(),ys[k].max()))
    return p,ys[k],xs[k]

print("=========== BOARD END EDGES, ref_side.jpg (RED target, GEOMETRY) ===========")
pLo,_,_=track(YEL,list(range(48,258)),313.,0.155,12,+1,"fore OUTER")
pRo,_,_=track(YEL,list(range(30,262)),741.,0.057,12,-1,"aft  OUTER")
pLi,_,_=track(YEL,list(range(60,250)),362.,0.155,9,-1,"fore INNER (yel->mural)")
pRi,_,_=track(YEL,list(range(45,250)),713.,0.057,9,+1,"aft  INNER (mural->yel)")
print("  fore strip width @y150 = %.1f px ; aft strip width @y150 = %.1f px"%(
      (pLi[0]*150+pLi[1])-(pLo[0]*150+pLo[1]), (pRo[0]*150+pRo[1])-(pRi[0]*150+pRi[1])))

def vp(pa,pb,tag):
    yv=(pb[1]-pa[1])/(pa[0]-pb[0]); xv=pa[0]*yv+pa[1]
    print("   VP %-16s = (%7.0f, %8.0f)   taper d(span)/dy = %+.5f"%(tag,xv,yv,pb[0]-pa[0]))
    return xv,yv
vp(pLo,pRo,"OUTER pair"); vp(pLi,pRi,"INNER pair")

print("\n--- sub-window stability of the two OUTER edges ---")
for lo,hi in ((48,150),(150,258),(60,200),(90,240)):
    a,_,_=track(YEL,list(range(lo,hi)),0.155*((lo+hi)/2)+306,0.155,12,+1,"  fore %d-%d"%(lo,hi))
    c,_,_=track(YEL,list(range(max(lo,32),hi)),0.057*((lo+hi)/2)+739,0.057,12,-1,"  aft  %d-%d"%(lo,hi))
    if a is not None and c is not None:
        print("      -> taper %+0.5f   VP_y %8.0f"%(c[0]-a[0],(c[1]-a[1])/(a[0]-c[0])))

print("\n=========== TRUE-VERTICAL CONTROLS IN THE SAME FRAME ===========")
V=[]
def addv(p,x,lab):
    if p is None: return
    V.append((p,lab))
# lamppost, both edges (orig x ~50-75, y 0..470)
p,_,_=track(Y,list(range(10,470)),52.,0.03,7,+1,"lamppost LEFT edge"); addv(p,52,"post L")
p,_,_=track(Y,list(range(10,470)),74.,0.03,7,-1,"lamppost RIGHT edge"); addv(p,74,"post R")
# concrete column behind bus right (orig x 770..802, y 5..250)
p,_,_=track(Y,list(range(8,250)),771.,0.005,8,-1,"column LEFT edge"); addv(p,771,"col L")
p,_,_=track(Y,list(range(8,250)),802.,0.005,8,+1,"column RIGHT edge"); addv(p,802,"col R")
