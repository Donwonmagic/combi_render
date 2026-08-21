import numpy as np
RIM_R=0.2198; FLANGE_AUTHORED=0.1905; S=RIM_R/FLANGE_AUTHORED
CAP_R=0.1345
barrel=[(0.0600,0.1905),(0.0640,0.1885),(0.0625,0.1820),(0.0560,0.1795),(0.0520,0.1720),
 (0.0480,0.1660),(0.0300,0.1640),(0.0080,0.1650),(-0.0080,0.1700),(-0.0200,0.1790),
 (-0.0230,0.1860),(-0.0190,0.1900),(-0.0250,0.1905),(-0.0300,0.1880),(-0.0290,0.1800),
 (-0.0180,0.1690),(-0.0060,0.1600),(0.0120,0.1560),(0.0330,0.1560),(0.0480,0.1590),
 (0.0540,0.1660),(0.0570,0.1760),(0.0560,0.1840)]
barrel=[(y,r*S) for y,r in barrel]
disc=[(0.0500,0.1600),(0.0560,0.1560),(0.0570,0.1400),(0.0520,0.1200),(0.0450,0.0900),
 (0.0430,0.0620),(0.0450,0.0400),(0.0470,0.0000)]
disc=[(y,r*S) for y,r in disc]
cap=[(0.0745,0.0000),(0.0736,0.0300),(0.0710,0.0560),(0.0664,0.0800),(0.0596,0.1010),
 (0.0502,0.1180),(0.0378,0.1288),(0.0236,0.1342),(0.0120,CAP_R)]
print("S = %.6f  RIM_R=%.4f"%(S,RIM_R))
print("barrel max y  = %.4f  (at r=%.4f)"%(max(b[0] for b in barrel),
      [r for y,r in barrel if y==max(b[0] for b in barrel)][0]))
print("cap apex y    = %.4f"%cap[0][0])
print("AS-BUILT cap apex proud of barrel max y = %.1f mm"%((cap[0][0]-max(b[0] for b in barrel))*1000))
print("disc outer radius (scaled) = %.5f   disc y range %.4f..%.4f"%(max(r for y,r in disc),
      min(y for y,r in disc),max(y for y,r in disc)))
# interpolators r -> y  (both profiles monotone-ish in r on their front faces)
dr=np.array([r for y,r in disc][::-1]); dy=np.array([y for y,r in disc][::-1])
cr=np.array([r for y,r in cap]);        cy=np.array([y for y,r in cap])
f_disc=lambda r: np.interp(r,dr,dy)
f_cap =lambda r: np.interp(r,cr,cy)
rr=np.linspace(0,CAP_R,200001)
d=f_cap(rr)-f_disc(rr)          # >0 = cap is outboard of disc
sign=np.sign(d)
idx=np.where(np.diff(sign)!=0)[0]
print("\ncrossover(s) where cap y == disc y:")
for i in idx:
    r0=rr[i]-d[i]*(rr[i+1]-rr[i])/(d[i+1]-d[i])
    print("   r = %.5f m   (%.2f mm)   cap y=%.5f disc y=%.5f"%(r0,r0*1000,f_cap(r0),f_disc(r0)))
print("\nmax disc-over-cap  (how far the cap must move OUTBOARD to clear the disc):")
k=np.argmax(-d); print("   %.4f m = %.1f mm  at r=%.4f"%(-d[k],-d[k]*1000,rr[k]))
move=-d[k]
print("   cap apex after that move = %.4f ; proud of barrel max y by %.1f mm"%(cap[0][0]+move,(cap[0][0]+move-max(b[0] for b in barrel))*1000))

print("\n--- DISHING THE DISC INSTEAD: how big is the resulting step? ---")
need=-d[k]
print("required inboard dish of the disc = %.1f mm (same magnitude)"%(need*1000))
disc_outer_r=max(r for y,r in disc); disc_outer_y=[y for y,r in disc if r==disc_outer_r][0]
br=np.array([r for y,r in barrel]); by=np.array([y for y,r in barrel])
# barrel front face only: take points with y>0.03 sorted by r
front=sorted([(r,y) for y,r in barrel if y>0.0], key=lambda t:t[0])
print("disc outer edge: r=%.4f y=%.4f -> after dish y=%.4f"%(disc_outer_r,disc_outer_y,disc_outer_y-need))
print("candidate 'cliff' measures:")
print("  barrel max y (0.0640) - dished disc outer edge      = %.1f mm"%((0.0640-(disc_outer_y-need))*1000))
print("  barrel max y (0.0640) - dished disc CENTRE           = %.1f mm"%((0.0640-(0.0470-need))*1000))
print("  rim flange y (0.0600) - dished disc CENTRE           = %.1f mm"%((0.0600-(0.0470-need))*1000))
print("  disc max y   (0.0570) - dished disc outer edge       = %.1f mm"%((0.0570-(disc_outer_y-need))*1000))
print("  the dish depth itself                                = %.1f mm"%(need*1000))
