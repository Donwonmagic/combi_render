"""REV51 A2 -- CALIBRATION of BOTH estimators on synthetics at known h, phi, D."""
import numpy as np, r51_scene as SC, r51_pipe as P, r51_emb as EM, r51_qload as QL

def scores(img):
    V = img.max(-1); ch = V - img.min(-1)
    return V - 1.6*ch, img[..., 0] - np.maximum(img[..., 1], img[..., 2]), V, ch

def outboard_hint(phi, eps, dist, f_px, W, H):
    phr = np.radians(phi); epr = np.radians(eps)
    v = np.array([np.sin(phr)*np.cos(epr), np.cos(phr), np.sin(phr)*np.sin(epr)])
    C = v*dist; fwd = -v; up = np.array([0., 0., 1.])
    right = np.cross(fwd, up); right /= np.linalg.norm(right)
    tup = np.cross(right, fwd)
    def pr(Pp):
        rel = Pp - C; z = np.dot(rel, fwd)
        return np.array([W/2 + f_px*np.dot(rel, right)/z,
                         H/2 - f_px*np.dot(rel, tup)/z])
    return pr(np.array([0., 0.05, 0.])) - pr(np.array([0., 0., 0.]))

def case(h_true, phi, dist=4.0, f_px=1900., W=560, H=560, seed=0, eps=-12.,
         noise=0.008, blur=0.9):
    dome = h_true + 0.0123
    prims, htrue, apex = SC.scene_seated(dome)
    img, m, t = SC.render(prims, phi, eps_deg=eps, dist=dist, f_px=f_px, W=W,
                          H=H, bg=0.16, seed=seed, noise=noise, blur=blur)
    cs, rs, V, ch = scores(img)
    r = P.analyze(cs, rs, (cs > 0.30) | (rs > 0.10), rs > 0.10)
    if r is None: return None
    ec, mm = EM.emblem_centre(img, r['cap'])
    hint = outboard_hint(phi, eps, dist, f_px, W, H)
    e = EM.measure_h(r['cream'], ec, hint, D_cam=dist) if ec else None
    e0 = EM.measure_h(r['cream'], ec, hint, D_cam=None) if ec else None
    ph = np.degrees(np.arccos(np.clip(r['cream']['ratio'], -1, 1)))
    hq = QL.h_from_q(r['q'], ph, 'auth')
    return dict(h_true=htrue, phi=phi, phi_hat=ph, q=r['q'], sig_q=r['sig_q'],
                h_q=hq, h_e=e['h'] if e else np.nan,
                h_e_nocorr=e0['h'] if e0 else np.nan,
                delta=e['delta_px'] if e else np.nan,
                s=e['s'] if e else np.nan, radrat=r['rad_ratio'])

if __name__ == '__main__':
    print('CALIBRATION 3 -- seated cap, authored SHAPE, dome depth = h + 12.3 mm')
    print('%7s %5s %6s | %8s %8s %7s %7s | %8s %8s %8s'
          % ('h_true','phi','D_m','phi_hat','q_obs','sig_q','radrat',
             'h_q(mm)','h_E(mm)','h_E_raw'))
    rows=[]
    for (ht, phi, D) in [(0.005,8,4.0),(0.005,25,4.0),(0.005,40,4.0),(0.005,55,4.0),(0.005,65,4.0),
                         (0.015,25,4.0),(0.015,40,4.0),(0.015,55,4.0),(0.015,65,4.0),
                         (0.040,25,4.0),(0.040,40,4.0),(0.040,55,4.0),(0.040,65,4.0),
                         (0.060,8,4.0),(0.060,25,4.0),(0.060,40,4.0),(0.060,55,4.0),(0.060,65,4.0),
                         (0.010,55,2.5),(0.010,55,12.0),(0.058,55,2.5),(0.058,55,12.0)]:
        c = case(ht, phi, dist=D, f_px=1900.*D/4.0, seed=int(ht*1e4)+phi+int(D))
        if c is None: print('%7.1f %5d  FAILED'%(ht*1000,phi)); continue
        print('%7.1f %5d %6.1f | %8.2f %8.4f %7.4f %7.4f | %+8.1f %+8.1f %+8.1f'
              %(c['h_true']*1000, phi, D, c['phi_hat'], c['q'], c['sig_q'],
                c['radrat'], c['h_q']*1000, c['h_e']*1000, c['h_e_nocorr']*1000))
        rows.append(c)
    import json
    E=[(c['h_e']-c['h_true'])*1000 for c in rows if np.isfinite(c['h_e'])]
    Q=[(c['h_q']-c['h_true'])*1000 for c in rows if np.isfinite(c['h_q']) and c['phi']>=25]
    print('\nE2 (emblem) residual over all cases : mean %+.1f mm  sd %.1f mm  n=%d'%(np.mean(E),np.std(E),len(E)))
    print('E1 (axis ratio) residual, phi>=25   : mean %+.1f mm  sd %.1f mm  n=%d'%(np.mean(Q),np.std(Q),len(Q)))
