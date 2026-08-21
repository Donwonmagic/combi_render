import numpy as np
from PIL import Image
A = np.asarray(Image.open('/home/user/combi_render/ref_side.jpg').convert('RGB')).astype(float)
H,W,_=A.shape
R,G,B = A[:,:,0],A[:,:,1],A[:,:,2]
Y = 0.299*R+0.587*G+0.114*B
YEL = (R+G)/2.0 - B

def edge_row(ch, r, xc, half, sign):
    """sub-pixel half-crossing of a step in ch[r, xc-half:xc+half]."""
    x0,x1 = int(round(xc-half)), int(round(xc+half))
    if x0<0 or x1>=W: return None
    seg = ch[r, x0:x1+1].astype(float)
    if sign<0: seg = -seg
    lo = np.percentile(seg[:max(3,len(seg)//4)],50)
    hi = np.percentile(seg[-max(3,len(seg)//4):],50)
    if hi-lo < 12: return None
    t = 0.5*(lo+hi)
    idx = np.where(seg>=t)[0]
    if len(idx)==0 or idx[0]==0: return None
    i = idx[0]
    a,b = seg[i-1], seg[i]
    if b==a: return None
    return x0 + (i-1) + (t-a)/(b-a)

def track(ch, rows, x_seed, slope_seed, half, sign, label, iters=6):
    xs=None
    a,b = slope_seed, x_seed - slope_seed*rows[0]
    for it in range(iters):
        pts=[]
        for r in rows:
            xc = a*r+b
            e = edge_row(ch, r, xc, half, sign)
            if e is not None: pts.append((r,e))
        if len(pts)<10: print(label,"FAILED"); return None
        ys=np.array([p[0] for p in pts]); xs=np.array([p[1] for p in pts])
        p=np.polyfit(ys,xs,1)
        res=xs-np.polyval(p,ys); s=res.std()
        k=np.abs(res)<2.0*max(s,0.4)
        p=np.polyfit(ys[k],xs[k],1)
        a,b=p; half=max(4.0, half*0.75)
    res=xs[k]-np.polyval(p,ys[k])
    print("%-34s n=%3d  slope=%+.5f  x@y150=%7.2f  rms=%.2f  yrange %d-%d"%(
        label,k.sum(),p[0],p[0]*150+p[1],res.std(),ys[k].min(),ys[k].max()))
    return p

print("### BOARD ends, outer edges (YEL step)")
pL = track(YEL, list(range(48,258)), 313.0, 0.15, 12, +1, "fore(L) outer  y48-257")
pR = track(YEL, list(range(30,262)), 741.0, 0.03, 12, -1, "aft(R) outer   y30-261")
print("### BOARD ends, INNER edges (yellow border -> dark mural)")
pLi = track(YEL, list(range(60,250)), 331.0, 0.15, 10, -1, "fore(L) inner")
pRi = track(YEL, list(range(45,250)), 725.0, 0.03, 10, +1, "aft(R) inner")

def vp(pa,pb,tag):
    yv=(pb[1]-pa[1])/(pa[0]-pb[0]); xv=pa[0]*yv+pa[1]
    print("   %-18s VP = (%8.0f, %8.0f)"%(tag,xv,yv))
    return xv,yv
vp(pL,pR,"outer pair"); vp(pLi,pRi,"inner pair"); vp(pL,pRi,"L-out/R-in")
