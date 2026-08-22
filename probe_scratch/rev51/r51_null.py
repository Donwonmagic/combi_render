"""REV51 A2 -- THE 5-FOLD NULL TEST.

Walk the cream annulus just OUTSIDE the cap edge and ask whether ANY 5-fold
modulation is present.  Detection floor is established by INJECTING a notch of
the size the build predicts and showing it is recovered (positive control).
"""
import numpy as np
import r51_seedfit as SF, r51_photo as PH, r51_inst as IN
from PIL import Image
R = '/home/user/combi_render/'

# ---- what the BUILD predicts, from the source literals -------------------
VC, VR, CAP_LIP, RIM = 0.118, 0.0235, 0.1370, 0.2198
def notch_halfangle(r):
    c = (r*r + VC*VC - VR*VR)/(2*r*VC)
    return float(np.degrees(np.arccos(np.clip(c, -1, 1))))

def profile(img, fit, rho_lo, rho_hi, nang=720):
    ang = np.linspace(-np.pi, np.pi, nang, endpoint=False)
    Rr = IN.ell_radius(fit, ang)
    fr = np.linspace(rho_lo, rho_hi, 9)
    xs = fit['cx'] + (Rr[:, None]*fr[None, :])*np.cos(ang)[:, None]
    ys = fit['cy'] + (Rr[:, None]*fr[None, :])*np.sin(ang)[:, None]
    V = IN.bilinear(img.mean(-1), xs, ys)
    return ang, V.mean(1)

def harmonics(ang, v, mmax=12, drop=(0, 1, 2)):
    good = np.isfinite(v)
    a, v = ang[good], v[good]
    A = {}
    for m in range(0, mmax+1):
        A[m] = 2*np.abs(np.mean(v*np.exp(-1j*m*a)))
    v0 = v.copy()
    return A

def inject(img, fit, depth, halfdeg, phase=0.31, rho=(1.00, 1.16)):
    H, W = img.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    dx = xx - fit['cx']; dy = yy - fit['cy']
    ang = np.arctan2(dy, dx)
    Rr = IN.ell_radius(fit, ang)
    rho_pix = np.hypot(dx, dy)/np.maximum(Rr, 1e-6)
    m = (rho_pix > rho[0]) & (rho_pix < rho[1])
    d = np.abs(((ang - phase) % (2*np.pi/5)) - np.pi/5)
    m &= (d > (np.pi/5 - np.radians(halfdeg)))
    out = img.copy()
    out[m] *= (1.0 - depth)
    return out

CASES = [
 ('CTRL_low34',   'out/r51b_low34.png',    (700,745,830,890), 55,60, 61,'red'),
 ('IMG_2073',     'IMG_2073.jpeg',         (670,720,810,890), 73,90, 70,'chrome'),
 ('rear34_rear',  'ref_rear34.jpg',        (690,630,840,825), 57,100,68,'red'),
 ('nolita_f34',   'ref_nolita_front34.jpg',(370,270,475,385), 44,66, 36,'red'),
 ('refside_rear', 'ref_side.jpg',          (690,540,820,680), 61,71, 54,'red'),
 ('playa_front',  'ref_playa_34.png',      (195,275,290,365), 45,47, 33,'red'),
]

print('BUILD PREDICTION: vents span r %.4f..%.4f m; cap lip r %.4f' %
      (VC-VR, VC+VR, CAP_LIP))
print('  a notch at r = %.4f m has HALF-ANGLE %.1f deg (full %.1f deg), '
      'i.e. %.0f%% of the 72 deg period'
      % (0.1390, notch_halfangle(0.1390), 2*notch_halfangle(0.1390),
         100*2*notch_halfangle(0.1390)/72))
print()
print('%-14s %8s %8s %8s %9s %9s %9s'
      % ('frame', 'A5', 'noise', 'SNR', 'A5_inj', 'SNRinj', 'floor(d)'))
for tag, fn, box, cx, cy, rg, cm in CASES:
    r = SF.run_best(R+fn, box, cx, cy, rg, capmode=cm)
    if r is None: print(tag, 'FAIL'); continue
    kf = r['cap']
    ang, v = profile(r['img'], kf, 1.03, 1.17)
    v = v/np.nanmean(v)
    A = harmonics(ang, v)
    noise = np.median([A[m] for m in (3, 4, 6, 7, 8, 9, 11)])
    snr = A[5]/noise
    # POSITIVE CONTROL: inject the notch the build predicts
    inj = inject(r['img'], kf, 0.55, notch_halfangle(0.1390))
    ang2, v2 = profile(inj, kf, 1.03, 1.17); v2 = v2/np.nanmean(v2)
    A2 = harmonics(ang2, v2)
    snr2 = A2[5]/noise
    floor = 0.55*5.0*noise/max(A2[5], 1e-9)
    print('%-14s %8.4f %8.4f %8.1f %9.4f %9.1f %9.3f'
          % (tag, A[5], noise, snr, A2[5], snr2, floor))
    Image.fromarray((np.clip(inj, 0, 1)*255).astype('uint8')).resize(
        (inj.shape[1]*5, inj.shape[0]*5), Image.LANCZOS).save('NULL_inj_%s.png' % tag)
