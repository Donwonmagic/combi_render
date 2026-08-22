"""REV51 A2 -- re-derivation of the SEATING arithmetic (coordinator's claim),
and of the CROSSOVER radius, from the two profiles as strings."""
import numpy as np
import r51_scene as SC

cap  = SC.cap_profile(0.0)
disc = SC.disc_profile(0.0)
bar  = SC.barrel_profile()

# outward branch of the cap (apex -> lip): monotone decreasing y, increasing r
cap_out = cap[:10]
print('cap outward branch (y, r):')
for p in cap_out: print('   %.4f  %.4f' % p)
lip_y, lip_r = max(cap, key=lambda p: p[1])   # max r point
lip_r = max(r for y, r in cap); lip_y = [y for y, r in cap if r == lip_r][0]
apex_y = max(y for y, r in cap)
print('\ncap apex y  = %.4f' % apex_y)
print('cap lip     r = %.4f at y = %.4f' % (lip_r, lip_y))
print('DOME DEPTH apex->lip = %.4f m = %.1f mm' % (apex_y-lip_y, 1000*(apex_y-lip_y)))

# disc FRONT face y as a function of r
front = SC.disc_profile(0.0)[:8]
fr = np.array([r for y, r in front]); fy = np.array([y for y, r in front])
o = np.argsort(fr)
def disc_y(r): return float(np.interp(r, fr[o], fy[o]))
print('\ndisc front face (y, r) scaled by S=%.6f:' % SC.S)
for y, r in front: print('   %.4f  %.4f' % (y, r))
print('disc y at cap lip radius %.4f = %.4f m' % (lip_r, disc_y(lip_r)))

flange_y = max(y for y, r in bar)
print('flange front face y = %.4f' % flange_y)

seat_shift = disc_y(lip_r) - lip_y
print('\nSEAT the lip on the disc: cap must move OUT by %.4f m = %.1f mm'
      % (seat_shift, 1000*seat_shift))
print('  -> apex at y = %.4f' % (apex_y+seat_shift))
print('  -> PROUD OF FLANGE = %.4f m = %.1f mm'
      % (apex_y+seat_shift-flange_y, 1000*(apex_y+seat_shift-flange_y)))
print('  identity check: dome_depth - (flange_y - disc_at_lip) = %.1f mm'
      % (1000*((apex_y-lip_y) - (flange_y-disc_y(lip_r)))))
print('  flange_y - disc_at_lip = %.4f m = %.1f mm   <-- the +12.3 mm conversion'
      % (flange_y-disc_y(lip_r), 1000*(flange_y-disc_y(lip_r))))

# ---- crossover radius, AS BUILT (cap not seated) ------------------------
cr = np.array([r for y, r in cap_out]); cy = np.array([y for y, r in cap_out])
oo = np.argsort(cr)
def cap_y(r): return float(np.interp(r, cr[oo], cy[oo]))
rs = np.linspace(0.02, 0.1370, 20001)
d = np.array([cap_y(r)-disc_y(r) for r in rs])
sgn = np.sign(d)
k = np.where(sgn[:-1] != sgn[1:])[0]
print('\nAS BUILT crossover (cap surface == disc surface):')
for kk in k:
    r0, r1 = rs[kk], rs[kk+1]
    print('   r = %.5f m   (cap y = %.5f)' % (0.5*(r0+r1), cap_y(0.5*(r0+r1))))
print('   outboard of that radius the DISC is proud of the CAP')
print('\nVISIBLE RED EDGE, as built = the crossover, r = %.5f, y = %.5f'
      % (rs[k[-1]], cap_y(rs[k[-1]])))
print('   ratio visible_r / RIM_R = %.4f' % (rs[k[-1]]/SC.RIM_R))
print('SEATED cap: visible red edge = the LIP, r = %.4f, ratio = %.4f'
      % (lip_r, lip_r/SC.RIM_R))
print('   (intent (CAP_R+0.0025)/RIM_R = %.4f)' % ((SC.CAP_R+0.0025)/SC.RIM_R))

# ---- vents -------------------------------------------------------------
print('\nVENTS: centres 0.118*cos(a) etc, cutter radius 0.0235 (NOT scaled by S)')
print('   span r = %.4f .. %.4f   against CAP_R %.4f, cap lip %.4f'
      % (0.118-0.0235, 0.118+0.0235, SC.CAP_R, lip_r))
print('   outboard of the cap lip by %.1f mm' % (1000*(0.118+0.0235-lip_r)))
