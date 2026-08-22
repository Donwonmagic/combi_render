"""REV51 A2 -- final numbers."""
import numpy as np, json
import r51_seedfit as SF, r51_photo as PH, r51_emb as EM, r51_qload as QL, r51_inst as IN
R = '/home/user/combi_render/'
BIAS, SD = -0.0076, 0.0046

C = [
 ('CTRL_side_ortho', 'out/r51b_side.png',      (1010,785,1190,960), 88.3, 87.0, 59.6,'red',   (1,0)),
 ('CTRL_low34',      'out/r51b_low34.png',     (700,745,830,890),   55,  60,   61,  'red',   (1,0)),
 ('IMG_2073',        'IMG_2073.jpeg',          (670,720,810,890),   73,  90,   70,  'chrome',(1,0)),
 ('rear34_rear',     'ref_rear34.jpg',         (690,630,840,825),   57, 100,   68,  'red',   (-1,0)),
 ('rear34_front',    'ref_rear34.jpg',         (510,495,635,670),   55,  87,   42,  'red',   (-1,0)),
 ('nolita_f34',      'ref_nolita_front34.jpg', (370,270,475,385),   44,  66,   36,  'red',   (-1,0)),
 ('refside_rear',    'ref_side.jpg',           (690,540,820,680),   61,  71,   54,  'red',   (-1,0)),
 ('playa_front',     'ref_playa_34.png',       (195,275,290,365),   45,  47,   33,  'red',   (-1,0)),
]
out = []
for tag, fn, box, cx, cy, rg, cm, hint in C:
    r = SF.run_best(R+fn, box, cx, cy, rg, capmode=cm)
    if r is None:
        print('%-16s FAIL' % tag); continue
    c, k = r['cream'], r['cap']
    ph = float(np.degrees(np.arccos(np.clip(c['ratio'], -1, 1))))
    s = c['a']/IN.R_CREAM
    h = QL.h_from_q(r['q'], ph, 'auth')
    hs = QL.h_from_q(r['q'], ph, 'sph')
    dq = max(r['sig_q'], 2e-4)
    hi = QL.h_from_q(r['q']+dq, ph, 'auth'); lo = QL.h_from_q(max(r['q']-dq, -0.06), ph, 'auth')
    sh = abs(hi-lo)/2 if np.isfinite(hi) and np.isfinite(lo) else np.nan
    ec, mm = EM.emblem_centre(r['img'], k, mode=('dark' if cm == 'chrome' else 'bright'))
    e = EM.measure_h(c, ec, hint) if ec else None
    o = dict(tag=tag, seed=r['seedmode'], phi=ph, s=s, q=r['q'], sq=r['sig_q'],
             rr=r['rad_ratio'], crms=c['rms'], krms=k['rms'], cn=c['n'], kn=k['n'],
             ca=c['a'], cb=c['b'], ka=k['a'], kb=k['b'],
             h=h, hs=hs, sh=sh, hE=(e['h'] if e else np.nan),
             dE=(e['delta_px'] if e else np.nan), pE=(e['perp_px'] if e else np.nan))
    out.append(o); PH.overlay(r, 'ANS_%s.png' % tag, sc=6)
    print('%-16s seed=%-4s phi=%5.2f  px/m=%6.1f  rms c/k = %.2f/%.2f  n %3d/%3d'
          % (tag, r['seedmode'], ph, s, c['rms'], k['rms'], c['n'], k['n']))
    print('%16s  radrat=%.4f   q=%+.4f+/-%.4f   h_auth=%s  h_sph=%s  sig=%s   h_E2=%s  (perp %s px)'
          % ('', r['rad_ratio'], r['q'], r['sig_q'],
             ('%+.1f' % ((h-BIAS)*1000)) if np.isfinite(h) else '  n/a',
             ('%+.1f' % ((hs-BIAS)*1000)) if np.isfinite(hs) else '  n/a',
             ('%.1f' % (sh*1000)) if np.isfinite(sh) else ' inf',
             ('%+.1f' % (e['h']*1000)) if e else ' n/a',
             ('%+.1f' % e['perp_px']) if e else '  - '))
json.dump([{k: (None if (isinstance(v, float) and not np.isfinite(v)) else v)
            for k, v in o.items()} for o in out], open('r51_answer.json', 'w'), indent=1)

# ---- single-dome-depth fit across the oblique red-cap frames --------------
print('\n--- GLOBAL FIT: one dome depth explaining all frames? ---')
use = [o for o in out if o['tag'] not in ('CTRL_side_ortho', 'CTRL_low34')]
def chi2(d):
    t = 0.0
    for o in use:
        qm = QL.q_of('auth', d, o['phi'])
        t += ((o['q']-qm)/max(o['sq'], 0.002))**2
    return t
ds = np.linspace(0.005, 0.150, 400)
cs_ = np.array([chi2(d) for d in ds])
b = ds[int(np.argmin(cs_))]
print('best dome depth %.1f mm  -> h = %.1f mm   chi2=%.1f on %d frames (dof %d)'
      % (b*1000, (b-0.0123)*1000, cs_.min(), len(use), len(use)-1))
for o in use:
    qm = QL.q_of('auth', b, o['phi'])
    print('   %-14s phi=%5.2f  q_obs=%+.4f  q_model=%+.4f  resid=%+.4f (%.1f sigma)'
          % (o['tag'], o['phi'], o['q'], qm, o['q']-qm, (o['q']-qm)/max(o['sq'], 0.002)))
