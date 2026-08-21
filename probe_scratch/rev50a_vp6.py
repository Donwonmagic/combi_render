import numpy as np
exec(open('/home/user/combi_render/probe_scratch/rev50a_vp4.py').read().split("print(\"===========")[0])

def edge_col(ch,c,yc,half,sign,minstep=12.0):
    y0,y1=int(round(yc-half)),int(round(yc+half))
    if y0<0 or y1>=H: return None
    seg=ch[y0:y1+1,c].astype(float)
    if sign<0: seg=-seg
    n=len(seg); q=max(3,n//4)
    lo=np.median(seg[:q]); hi=np.median(seg[-q:])
    if hi-lo<minstep: return None
    t=0.5*(lo+hi); idx=np.where(seg>=t)[0]
    if len(idx)==0 or idx[0]==0: return None
    i=idx[0]; a,b=seg[i-1],seg[i]
    return y0+(i-1)+(t-a)/(b-a)

def trackH(ch,cols,y_seed,slope,half,sign,label,minstep=12.0):
    a,b=slope,y_seed-slope*cols[len(cols)//2]
    for it in range(7):
        pts=[]
        for c in cols:
            e=edge_col(ch,c,a*c+b,half,sign,minstep)
            if e is not None: pts.append((c,e))
        if len(pts)<12: print(label,"FAILED",len(pts)); return None
        xs=np.array([p[0] for p in pts],float); ys=np.array([p[1] for p in pts])
        p=np.polyfit(xs,ys,1); res=ys-np.polyval(p,xs); s=res.std()
        k=np.abs(res)<2.0*max(s,0.4); p=np.polyfit(xs[k],ys[k],1); a,b=p; half=max(3.5,half*0.72)
    print("%-30s n=%3d dy/dx=%+.5f  y@x512=%7.2f  rms=%.2f  cols %d-%d"%(
        label,int(k.sum()),p[0],p[0]*512+p[1],(ys[k]-np.polyval(p,xs[k])).std(),xs[k].min(),xs[k].max()))
    return p

print("=== FORE-AFT (bus X) horizontal lines ===")
hs=[]
p=trackH(YEL,list(range(340,740)),44.,-0.063,10,+1,"board TOP edge (bg->yellow)");  hs.append((p,"board top"))
p=trackH(Y,list(range(300,930)),524.,-0.05,9,-1,"flank cream->red belt");           hs.append((p,"belt"))
p=trackH(Y,list(range(330,900)),487.,-0.05,8,+1,"counter gold line");               hs.append((p,"gold"))
def vpH(pa,pb,tag):
    # y = a x + b
    xv=(pb[1]-pa[1])/(pa[0]-pb[0]); yv=pa[0]*xv+pa[1]
    print("   VP_X %-14s = (%9.0f, %8.0f)"%(tag,xv,yv))
    return xv,yv
for i in range(len(hs)):
    for j in range(i+1,len(hs)):
        if hs[i][0] is not None and hs[j][0] is not None:
            vpH(hs[i][0],hs[j][0],hs[i][1]+"/"+hs[j][1])
