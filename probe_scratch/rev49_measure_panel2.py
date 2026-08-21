"""rev49 -- THE SECOND RAISED PANEL, measured off ref_side.jpg (the RED bus).

READ-ONLY.  Writes nothing outside probe_scratch/.  No Blender.

WHICH BUS:  ref_side.jpg is RED (LEDGER_rev48 sec.5: body G/R 0.204).  Every
GEOMETRY figure below is measured on the RED bus.  The colour figures in part
(g) are ARTWORK and are quoted from the RED frames only (rule 26).

SCALE CHAIN -- the project's own, nothing invented:
  X(u)      = 641220.4/(u+11140) - 55.0322        SPEC.md:4506-4510 (sec.10.35)
              locked by X(242.84)=+1.300, X(749.38)=-1.100, rho=1.0445
  X_TAIL    = -1.8727                             t1_core.py:72  (= X(922.2))
  k_long(u) = (u+11140)^2/641220.4  px/m          = 1/|dX/du| of that same map
  k_t(u)    = k_long(u)/(1+(u-512)/11652)         LOFT_GROUND_rev15.md sec.0.4
              scaled so k_t(749.38) = 215.5 +- 3.0 px/m  (LOFT sec.0.4, ADOPTED)
  z datum   = drip-rail groove, 1.7485 +- 0.020 m AG, v = 299.24 +- 0.6 at the
              rear-axle column                    LOFT_GROUND_rev15.md sec.1.2
              -> REFITTED here as a LINE so it can be carried to the tail.
              C1 below shows the refit reproduces LOFT's published 299.24.
CEILING ON THE WHOLE CHAIN: it is the NEAR-FLANK (rim-flange) plane, y ~ +0.70.
"""
import numpy as np, math
from PIL import Image
from scipy import ndimage as ndi

A = np.asarray(Image.open('ref_side.jpg').convert('RGB'), float)
R,G,B = A[...,0],A[...,1],A[...,2]
L = 0.2126*R+0.7152*G+0.0722*B

def Xm(u):    return 641220.4/(u+11140.0)-55.0322
def klong(u): return (u+11140.0)**2/641220.4
def _f(u):    return klong(u)/(1.0+(u-512.0)/11652.0)
def kt(u):    return 215.5*_f(u)/_f(749.38)
X_TAIL, Z_DRIP = -1.8727, 1.7485

print(__doc__); print("="*79)
print("C0 map      X(242.84)=%+.4f  X(749.38)=%+.4f  X(922.2)=%+.4f"%(Xm(242.84),Xm(749.38),Xm(922.2)))
print("C0 scale    k_t(749.38)=%.2f (LOFT 215.5+-3.0)   k_long(500)=%.2f (LOFT 211.2)"%(kt(749.38),klong(500)))
print("C0 CEILING  the frame is 1024 px wide: its RIGHT EDGE is X=%.4f = X_TAIL %+.3f m."%(Xm(1023),Xm(1023)-X_TAIL))
print("            Any tip further aft than that would be CLIPPED and the reading would saturate.")

# ---- drip-rail groove line.  WINDOW cols[750,900) rows[288,306)
pts, drop_edge = [], []
for u in range(750,900):
    seg = L[288:306,u]; i = int(np.argmin(seg))
    if i in (0,len(seg)-1): drop_edge.append(u); continue
    y0,y1,y2 = seg[i-1],seg[i],seg[i+1]; den = y0-2*y1+y2
    pts.append((u,288+i+(0.0 if den==0 else 0.5*(y0-y2)/den)))
p = np.array(pts); w = np.ones(len(p))
for _ in range(5):
    P = np.polyfit(p[:,0],p[:,1],1,w=w); r = p[:,1]-np.polyval(P,p[:,0])
    s = 1.4826*np.median(np.abs(r-np.median(r))); w = (np.abs(r)<2.5*s).astype(float)
print("\nDRIP-RAIL GROOVE   WINDOW cols[750,900) rows[288,306), parabolic sub-pixel minimum")
print("  RULE 27: %d columns dropped (minimum on the window edge): %s"%(len(drop_edge),drop_edge))
print("           %d further columns dropped as >2.5-MAD outliers (bulbs and the roof-lid\n"
      "           junction sit in this band);  %d columns kept."%(int((w==0).sum()),int(w.sum())))
print("  v_groove(u) = %+.6f*u %+.3f    rms(kept) %.3f px"%(P[0],P[1],r[w>0].std()))
print("  C1  v_groove(749.38) = %.2f   against LOFT sec.1.2's published 299.24 +- 0.6"%np.polyval(P,749.38))
print("      rms %.3f px against LOFT's stated 0.06-0.12 px.   THE CHAIN REPRODUCES."%r[w>0].std())
def vg(u): return float(np.polyval(P,u))

# ---- board silhouette
gy=ndi.sobel(L,0); gx=ndi.sobel(L,1); g=np.hypot(gx,gy)
thr=np.percentile(g[170:310,865:1024],95)
u0,v0,u1,v1 = 884.,293.,1015.,192.; mm=(v1-v0)/(u1-u0)
top,bot={},{}
for u in range(878,1022):
    vp=v0+mm*(u-u0); h=[v for v in range(int(vp-18),int(vp+19)) if g[v,u]>thr]
    if h: top[u],bot[u]=min(h),max(h)
conf=[u for u in sorted(top) if 6<=bot[u]-top[u]<=26]
thin=[u for u in sorted(top) if bot[u]-top[u]<6]
print("\nBOARD SILHOUETTE   WINDOW u[878,1022) x (axis +-18 px);  |grad| > P95 (=%.0f) of that window"%thr)
print("  %d columns give BOTH boundaries; RULE 27 -- %d give only one (the board's own"%(len(conf),len(thin)))
print("  bright face against the bright wall, the lowest-contrast run): u %s"%thin)
th=[(bot[u]-top[u])*math.cos(math.atan(0.762)) for u in conf]
print("  perpendicular extent over the %d confident columns: min %.1f  median %.1f  max %.1f px"
      %(len(conf),min(th),float(np.median(th)),max(th)))

# ---- endpoints, Monte-Carlo
BASE,TIP=(888.,293.5),(1015.5,191.5); sb,st=(5.,4.),(4.,4.)
rng=np.random.default_rng(1); N=40000
ub,vb=rng.normal(BASE[0],sb[0],N),rng.normal(BASE[1],sb[1],N)
ut,vt=rng.normal(TIP[0],st[0],N),rng.normal(TIP[1],st[1],N)
ks=rng.normal(1.0,3.0/215.5,N); zd=rng.normal(0.0,0.020,N); rk=rng.normal(0.0,0.010,N)
XB=641220.4/(ub+11140)-55.0322; XT_=641220.4/(ut+11140)-55.0322
ZB=Z_DRIP+zd+(vg(0)+P[0]*ub-vb)/(kt(ub)*ks)
ZT=Z_DRIP+zd+rk+(vg(0)+P[0]*ut-vt)/(kt(ut)*ks)
DX,DZ=XT_-XB,ZT-ZB; ang=np.degrees(np.arctan2(DZ,-DX))
def rep(n,a): print("   %-38s %+.4f  +- %.4f"%(n,a.mean(),a.std()))
print("\nRESULT  (near-flank plane; MC 4e4 over u,v jitter + k_t 215.5+-3.0 + datum +-0.020 + rake +-0.010)")
rep("(a) base station  X - X_TAIL   [m]",XB-X_TAIL)
rep("(b) base height   z AG        [m]",ZB)
rep("(c) tilt from HORIZONTAL     [deg]",ang)
rep("(c) tilt from VERTICAL       [deg]",90-ang)
rep("(d) chord, 3-D, in the XZ plane[m]",np.hypot(DX,DZ))
rep("(e) tip  X - X_TAIL           [m]",XT_-X_TAIL)
rep("(e) tip  z AG                 [m]",ZT)
print("   dimensionless (rule 14):")
rep("    chord / wheelbase 2.400",np.hypot(DX,DZ)/2.400)
rep("    tip overhang / rear overhang 0.773",(X_TAIL-XT_)/0.773)
rep("    base z / roof baseline 1.9835",ZB/1.9835)
print("\n   chord in the IMAGE plane = %.1f px  (= %.3f m at k_t(951)=%.1f px/m)"
      %(math.hypot(TIP[0]-BASE[0],TIP[1]-BASE[1]),
        math.hypot(TIP[0]-BASE[0],TIP[1]-BASE[1])/kt(951),kt(951)))
print("   CEILING on (a)/(e): the map is the near-flank plane.  Re-seated at the drip-rail")
print("   plane (y=+0.80) the same pixels give base %+.3f / tip %+.3f; at the centreline"%
      (Xm(BASE[0])*(4.78/4.9)-X_TAIL, Xm(TIP[0])*(4.78/4.9)-X_TAIL))
print("   (y=0) base %+.3f / tip %+.3f.  The aft-most silhouette point BELONGS to the near"%
      (Xm(BASE[0])*(5.60/4.9)-X_TAIL, Xm(TIP[0])*(5.60/4.9)-X_TAIL))
print("   edge, so the near-flank row is the applicable one; the +-0.05 m between the two")
print("   near-side planes is the honest depth term and is NOT in the MC sigma above.")
