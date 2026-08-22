"""REV51 A2 -- run the instrument on the two RENDER CONTROLS and every frame."""
import numpy as np, sys
from PIL import Image
import r51_photo as PH, r51_emb as EM, r51_qload as QL, r51_inst as IN

R = '/home/user/combi_render/'

FRAMES = [
 # tag                 file                        crop box              seed pt  capmode hint  emb_mode
 ('CTRL side ortho R',  'out/r51b_side.png',   (1010,785,1190,960),  (88,87),  'red',  (+1,0), 'bright'),
 ('CTRL low34 front',   'out/r51b_low34.png',  (700,745,830,890),    (55,60),  'red',  (+1,0), 'bright'),
 ('IMG_2073 front',     'IMG_2073.jpeg',       (670,720,810,890),    (69,84),  'chrome',(+1,0),'dark'),
 ('ref_playa_34 front', 'ref_playa_34.png',    (275,255,375,355),    (48,50),  'red',  (-1,0), 'bright'),
 ('ref_rear34 rear',    'ref_rear34.jpg',      (700,640,830,800),    (55,80),  'red',  (-1,0), 'bright'),
 ('ref_rear34 front',   'ref_rear34.jpg',      (520,505,625,655),    (50,75),  'red',  (-1,0), 'bright'),
 ('ref_nolita_f34 fr',  'ref_nolita_front34.jpg',(375,278,470,378),  (45,50),  'red',  (-1,0), 'bright'),
 ('ref_side rear',      'ref_side.jpg',        (680,530,830,690),    (75,80),  'red',  (-1,0), 'bright'),
]

def go(tag, fn, box, pt, capmode, hint, embmode, clip='both', save=True):
    try:
        r = PH.run(R+fn, box, pt, capmode=capmode, clip_cap=clip)
    except Exception as e:
        print('%-20s  EXCEPTION %s' % (tag, e)); return None
    if r is None:
        print('%-20s  PIPELINE FAILED' % tag); return None
    cf, kf = r['cream'], r['cap']
    ph = np.degrees(np.arccos(np.clip(cf['ratio'], -1, 1)))
    s = cf['a']/IN.R_CREAM
    hq = {t: QL.h_from_q(r['q'], ph, t) for t in ('auth', 'sph')}
    ec, mm = EM.emblem_centre(r['img'], kf, mode=embmode)
    e = EM.measure_h(cf, ec, hint) if ec else None
    # sigma on h from sigma_q, by finite difference of the forward model
    dq = max(r['sig_q'], 1e-4)
    hi = QL.h_from_q(r['q']+dq, ph, 'auth'); lo = QL.h_from_q(max(r['q']-dq,-0.05), ph, 'auth')
    sh = abs(hi-lo)/2 if np.isfinite(hi) and np.isfinite(lo) else np.nan
    print('%-20s cream a=%6.2f b=%6.2f ratio=%.4f rms=%.2f n=%3d | phi=%5.2f  s=%6.1f px/m'
          % (tag, cf['a'], cf['b'], cf['ratio'], cf['rms'], cf['n'], ph, s))
    print('%-20s cap   a=%6.2f b=%6.2f ratio=%.4f rms=%.2f n=%3d | radrat=%.4f'
          % ('', kf['a'], kf['b'], kf['ratio'], kf['rms'], kf['n'], r['rad_ratio']))
    print('%-20s q=%+.4f +/-%.4f  ->  h_auth=%+7.1f mm  h_sph=%+7.1f mm  (stat sd %.1f mm)'
          % ('', r['q'], r['sig_q'], hq['auth']*1000 if np.isfinite(hq['auth']) else np.nan,
             hq['sph']*1000 if np.isfinite(hq['sph']) else np.nan, sh*1000 if np.isfinite(sh) else np.nan))
    if e:
        print('%-20s E2 emblem: delta=%+6.2f px  perp=%+6.2f  ->  h_E=%+7.1f mm'
              % ('', e['delta_px'], e['perp_px'], e['h']*1000))
    else:
        print('%-20s E2 emblem: NOT FOUND' % '')
    if save:
        PH.overlay(r, 'OV_%s.png' % tag.replace(' ', '_').replace('/', '_'), sc=6)
    return dict(tag=tag, r=r, phi=ph, s=s, hq=hq, sh=sh, e=e, ec=ec)

if __name__ == '__main__':
    out=[]
    for f in FRAMES:
        out.append(go(*f))
        print()
