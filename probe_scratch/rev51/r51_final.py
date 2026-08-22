"""REV51 A2 -- FINAL RUN: two render controls + every candidate photograph."""
import numpy as np
import r51_photo as PH, r51_emb as EM, r51_qload as QL, r51_inst as IN

R = '/home/user/combi_render/'
BIAS_E1 = -0.0076          # calibrated mean residual of E1 (h_rec - h_true), phi>=25
SD_E1   =  0.0046

F = [
 # tag              file                     crop box              seed(cx,cy,a_h,b_v,th)   capmode  hint    emb box
 ('CTRL_side_ortho','out/r51b_side.png',   (1010,785,1190,960), (88.3,87.0,59.6,59.6,0), 'red',  (1,0),  (78,77,99,98)),
 ('CTRL_low34',     'out/r51b_low34.png',  (700,745,830,890),   (55,60,26,45,0),         'red',  (1,0),  (45,50,68,72)),
 ('IMG_2073_front', 'IMG_2073.jpeg',       (670,720,810,890),   (73,90,45,70,0),         'chrome',(1,0), (73,82,95,104)),
 ('rear34_rear',    'ref_rear34.jpg',      (695,635,835,815),   (52,95,35,68,0),         'red',  (-1,0), (18,84,40,110)),
 ('rear34_front',   'ref_rear34.jpg',      (515,500,630,660),   (50,82,20,42,0),         'red',  (-1,0), (36,72,56,96)),
 ('nolita_f34',     'ref_nolita_front34.jpg',(375,275,470,380), (39,61,26,36,0),         'red',  (-1,0), (38,53,56,73)),
 ('refside_rear',   'ref_side.jpg',        (690,540,820,680),   (61,71,54,53.5,0),       'red',  (-1,0), (50,50,72,72)),
 ('playa_front',    'ref_playa_34.png',    (205,285,275,355),   (35,37,32,33,0),         'red',  (-1,0), (29,31,48,50)),
]

def go(tag, fn, box, seed, capmode, hint, ebox, embmode=None):
    if embmode is None:
        embmode = 'dark' if capmode == 'chrome' else 'bright'
    r = PH.run(R+fn, box, None, capmode=capmode, seed=seed)
    if r is None:
        print('%-16s PIPELINE FAILED' % tag); return None
    cf, kf = r['cream'], r['cap']
    ph = np.degrees(np.arccos(np.clip(cf['ratio'], -1, 1)))
    s = cf['a']/IN.R_CREAM
    hq = QL.h_from_q(r['q'], ph, 'auth')
    hq_s = QL.h_from_q(r['q'], ph, 'sph')
    dq = max(r['sig_q'], 2e-4)
    hi = QL.h_from_q(r['q']+dq, ph, 'auth'); lo = QL.h_from_q(r['q']-dq, ph, 'auth')
    sh = abs(hi-lo)/2 if np.isfinite(hi) and np.isfinite(lo) else np.nan
    ec, mm = EM.emblem_centre(r['img'], kf, box=ebox, mode=embmode)
    e = EM.measure_h(cf, ec, hint) if ec else None
    print('== %-16s  crop%s' % (tag, box))
    print('   cream  a=%7.2f b=%7.2f  ratio=%.4f  rms=%.2f px  n=%3d'
          % (cf['a'], cf['b'], cf['ratio'], cf['rms'], cf['n']))
    print('   cap    a=%7.2f b=%7.2f  ratio=%.4f  rms=%.2f px  n=%3d'
          % (kf['a'], kf['b'], kf['ratio'], kf['rms'], kf['n']))
    print('   phi=%5.2f deg   px/m=%6.1f   RADIUS RATIO a_cap/a_cream = %.4f'
          % (ph, s, r['rad_ratio']))
    hcorr = (hq - BIAS_E1) if np.isfinite(hq) else np.nan
    print('   E1  q=%+.4f +/- %.4f  ->  h_auth=%s mm  (bias-corr %s)  h_sph=%s mm'
          % (r['q'], r['sig_q'],
             ('%+.1f' % (hq*1000)) if np.isfinite(hq) else ' n/a ',
             ('%+.1f' % (hcorr*1000)) if np.isfinite(hcorr) else ' n/a ',
             ('%+.1f' % (hq_s*1000)) if np.isfinite(hq_s) else ' n/a '))
    print('      1-sigma(stat)=%s mm   1-sigma(total, +cal sd %.1f)=%s mm'
          % (('%.1f' % (sh*1000)) if np.isfinite(sh) else 'inf', SD_E1*1000,
             ('%.1f' % (np.hypot(sh, SD_E1)*1000)) if np.isfinite(sh) else 'inf'))
    if e:
        print('   E2  emblem at (%.1f,%.1f)  delta=%+6.2f px  perp=%+6.2f px  ->  h_E=%+7.1f mm'
              % (ec[0], ec[1], e['delta_px'], e['perp_px'], e['h']*1000))
        print('       (implied dome depth = h + 12.3 mm = %+.1f mm)' % (e['h']*1000+12.3))
    else:
        print('   E2  emblem NOT FOUND')
    PH.overlay(r, 'FIN_%s.png' % tag, sc=6)
    return dict(tag=tag, ph=ph, s=s, q=r['q'], sq=r['sig_q'], hq=hq, sh=sh,
                rr=r['rad_ratio'], e=e, cf=cf, kf=kf, ec=ec)

if __name__ == '__main__':
    out = [go(*f) for f in F]
    print('\n\n%-16s %7s %8s %9s %10s %10s %9s'
          % ('frame','phi','radrat','q','h_E1(mm)','sig(mm)','h_E2(mm)'))
    for o in out:
        if o is None: continue
        print('%-16s %7.2f %8.4f %+9.4f %10s %10s %9s'
              % (o['tag'], o['ph'], o['rr'], o['q'],
                 ('%+.1f' % ((o['hq']-BIAS_E1)*1000)) if np.isfinite(o['hq']) else 'n/a',
                 ('%.1f' % (np.hypot(o['sh'], SD_E1)*1000)) if np.isfinite(o['sh']) else 'inf',
                 ('%+.1f' % (o['e']['h']*1000)) if o['e'] else 'n/a'))
