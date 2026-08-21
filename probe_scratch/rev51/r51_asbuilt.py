"""REV51 A2 step 1: as-built axial geometry of the wheel, from the SOURCE STRINGS.
Pure arithmetic on the literals quoted in t1_detail.py / t1_core.py.  No Blender."""
import re

src_core   = open('t1_core.py').read()
src_detail = open('t1_detail.py').read()

def const(src, name):
    m = re.search(r'^%s\s*=\s*([0-9.\-]+)' % name, src, re.M)
    return float(m.group(1))

TIRE_R = const(src_core, 'TIRE_R')
RIM_R  = const(src_core, 'RIM_R')
CAP_R  = const(src_detail, 'CAP_R')
print('t1_core.py   TIRE_R = %.4f   -> tyre OD 2*TIRE_R = %.4f m' % (TIRE_R, 2*TIRE_R))
print('t1_core.py   RIM_R  = %.4f   -> flange OD 2*RIM_R = %.4f m' % (RIM_R, 2*RIM_R))
print('t1_detail.py CAP_R  = %.4f   -> cap    OD 2*CAP_R = %.4f m' % (CAP_R, 2*CAP_R))

# ---- rim() barrel profile, verbatim from the string in t1_detail.py -------
FLANGE_AUTHORED = 0.1905
S = RIM_R / FLANGE_AUTHORED
prof = [
    (0.0600, 0.1905), (0.0640, 0.1885), (0.0625, 0.1820),
    (0.0560, 0.1795), (0.0520, 0.1720), (0.0480, 0.1660),
    (0.0300, 0.1640), (0.0080, 0.1650), (-0.0080, 0.1700),
    (-0.0200, 0.1790), (-0.0230, 0.1860), (-0.0190, 0.1900),
    (-0.0250, 0.1905), (-0.0300, 0.1880), (-0.0290, 0.1800),
    (-0.0180, 0.1690), (-0.0060, 0.1600), (0.0120, 0.1560),
    (0.0330, 0.1560), (0.0480, 0.1590), (0.0540, 0.1660),
    (0.0570, 0.1760), (0.0560, 0.1840),
]
prof_s = [(y, r*S) for (y, r) in prof]
print('\nrim(): S = RIM_R / FLANGE_AUTHORED = %.6f' % S)
ymax_b, r_at = max(prof_s, key=lambda p: p[0])
print('rim() barrel prof   max y = %.4f  at r = %.4f  (authored r=%.4f * S)' %
      (ymax_b, r_at, r_at/S))

# ---- rim() disc profile --------------------------------------------------
disc_prof = [
    (0.0500, 0.1600), (0.0560, 0.1560), (0.0570, 0.1400),
    (0.0520, 0.1200), (0.0450, 0.0900), (0.0430, 0.0620),
    (0.0450, 0.0400), (0.0470, 0.0000),
]
disc_s = [(y, r*S) for (y, r) in disc_prof]
ymax_d, rd = max(disc_s, key=lambda p: p[0])
print('rim() disc   prof   max y = %.4f  at r = %.4f' % (ymax_d, rd))
print('   NOTE the y of disc_prof is NOT scaled by S (source: "disc_prof = [(y, r * S) ...]")')

# ---- hubcap() profile ----------------------------------------------------
R = CAP_R
cap = [
    (0.0745, 0.0000), (0.0736, 0.0300), (0.0710, 0.0560),
    (0.0664, 0.0800), (0.0596, 0.1010), (0.0502, 0.1180),
    (0.0378, 0.1288), (0.0236, 0.1342), (0.0120, R),
    (0.0040, R + 0.0025), (-0.0035, R + 0.0010), (-0.0020, R - 0.0060),
    (0.0080, R - 0.0090), (0.0220, 0.1315), (0.0362, 0.1262),
    (0.0484, 0.1155), (0.0576, 0.0988), (0.0644, 0.0780),
    (0.0690, 0.0545), (0.0716, 0.0292), (0.0725, 0.0000),
]
apex_y = max(y for y, r in cap)
cap_rmax = max(r for y, r in cap)
print('\nhubcap() apex y            = %.4f  (profile pair (0.0745, 0.0000))' % apex_y)
print('hubcap() outer r max       = %.4f  at y = %.4f'
      % (cap_rmax, [y for y, r in cap if r == cap_rmax][0]))
print('hubcap() OUTER EDGE circle : r = CAP_R = %.4f at y = %.4f  (pair "(0.0120, R)")'
      % (R, 0.0120))

# ---- tyre() outer sidewall plane ----------------------------------------
up = [
    (0.0530, 0.1905), (0.0625, 0.2020), (0.0705, 0.2220),
    (0.0728, 0.2340), (0.0745, 0.2500), (0.0752, 0.2760),
    (0.0744, 0.2905), (0.0735, 0.2980), (0.0690, 0.3110),
    (0.0640, 0.3195), (0.0578, 0.3262),
]
SHOULDER = up[-1][1]
BEAD_AUTHORED = 0.1905
_k = (SHOULDER - RIM_R) / (SHOULDER - BEAD_AUTHORED)
up_s = [(y, SHOULDER - (SHOULDER - r)*_k) for (y, r) in up]
ymax_t, rt = max(up_s, key=lambda p: p[0])
print('\ntyre() outer sidewall plane max y = %.4f at r = %.4f  (bead map k=%.5f)'
      % (ymax_t, rt, _k))
print('tyre() tread crown r (y=0)        = %.4f = TIRE_R' % TIRE_R)

# ---- wheel_assembly: is there ANY relative y offset between cap and rim? --
m = re.search(r'def wheel_assembly.*?return grp', src_detail, re.S)
print('\nwheel_assembly() body (verbatim):')
print(m.group(0))

print('\n================= AS-BUILT PROUDNESS =================')
print('cap apex y                       %+.4f m' % apex_y)
print('rim barrel front flange face y   %+.4f m' % ymax_b)
print('  -> apex PROUD of flange        %+.4f m = %+.1f mm' % (apex_y-ymax_b, 1000*(apex_y-ymax_b)))
print('tyre outer sidewall plane y      %+.4f m' % ymax_t)
print('  -> apex PROUD of tyre sidewall %+.4f m = %+.1f mm' % (apex_y-ymax_t, 1000*(apex_y-ymax_t)))
print('cap OUTER EDGE y                 %+.4f m' % 0.0120)
print('  -> cap edge BEHIND flange by   %+.4f m = %+.1f mm' % (ymax_b-0.0120, 1000*(ymax_b-0.0120)))
print('dome height (apex - own edge)    %+.4f m = %+.1f mm' % (apex_y-0.0120, 1000*(apex_y-0.0120)))
print('disc face y at r=CAP_R region: disc rises to y=%.4f at r=%.4f' % (ymax_d, rd))
