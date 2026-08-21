import numpy as np
# ANALYTIC: where does the wheel disc surface cross OUTBOARD of the hubcap dome?
RIM_R=0.2198; FLANGE_AUTHORED=0.1905; S=RIM_R/FLANGE_AUTHORED
disc=[(0.0500,0.1600),(0.0560,0.1560),(0.0570,0.1400),(0.0520,0.1200),
      (0.0450,0.0900),(0.0430,0.0620),(0.0450,0.0400),(0.0470,0.0000)]
disc=[(y,r*S) for (y,r) in disc]
CAP_R=0.1345
cap=[(0.0745,0.0000),(0.0736,0.0300),(0.0710,0.0560),(0.0664,0.0800),
     (0.0596,0.1010),(0.0502,0.1180),(0.0378,0.1288),(0.0236,0.1342),
     (0.0120,CAP_R),(0.0040,CAP_R+0.0025)]
def yat(prof,r):
    rs=[p[1] for p in prof]; ys=[p[0] for p in prof]
    o=np.argsort(rs); rs=np.array(rs)[o]; ys=np.array(ys)[o]
    if r<rs[0] or r>rs[-1]: return None
    return float(np.interp(r,rs,ys))
print("S=%.4f  disc radii after scale: %s"%(S,[round(p[1],4) for p in disc]))
print(" r(m)   disc_y   cap_y   disc-cap(mm)")
cross=None
for r in np.arange(0.090,0.1500,0.0020):
    dy=yat(disc,r); cy=yat(cap,r)
    if dy is None or cy is None: continue
    d=(dy-cy)*1000
    print("  %.4f  %.4f  %.4f  %+7.2f"%(r,dy,cy,d))
    if cross is None and d>0: cross=r
print("\nDISC FIRST STANDS PROUD OF THE CAP AT r ~ %.4f m"%cross)
print("visible dome radius / built CAP_R = %.4f"%(cross/CAP_R))
print("vent hole annulus: centre r 0.118, hole R 0.0235 -> r 0.0945 .. 0.1415")
print("so through each hole the cap shows out to min(0.1415, cap edge 0.1370) = 0.1370")
