"""REV51 A2 -- CALIBRATION v2.  Full pipeline, blind, on rendered synthetics
of a SEATED cap at KNOWN dome depth and KNOWN obliquity."""
import numpy as np, r51_scene as SC, r51_fwd as F, r51_pipe as P, r51_inst as IN

def scores(img):
    V = img.max(-1); mn = img.min(-1); ch = V - mn
    cream = V - 1.6*ch
    red = img[..., 0] - np.maximum(img[..., 1], img[..., 2])
    return cream, red, V, ch

CAPPROF = lambda d: SC.cap_profile_seated(d)

def one(h_true, phi, dist=4.0, f_px=1900., W=560, H=560, seed=0,
        noise=0.008, blur=0.9, eps=-12.0, shape=None):
    dome = h_true + 0.0123
    prof_fn = CAPPROF if shape is None else shape
    prims, htrue2, apex = SC.scene_seated(dome)
    if shape is not None:
        from r51_geom import revolve_profile, Disc
        prims = []
        prims += revolve_profile(SC.tyre_profile(), SC.M_TYRE)
        prims += revolve_profile(SC.barrel_profile(), SC.M_RIM)
        prims += revolve_profile(SC.disc_profile(0.0), SC.M_RIM)
        cp = shape(dome)
        prims += revolve_profile(cp, SC.M_CAP)
        apex = max(y for y, r in cp)
        prims.append(Disc(apex+0.0060, 0.0, 0.3170*SC.CAP_D/2, SC.M_EMB))
        htrue2 = apex - SC.FLANGE_FACE_Y
    img, m, t = SC.render(prims, phi, eps_deg=eps, dist=dist, f_px=f_px,
                          W=W, H=H, bg=0.16, seed=seed, noise=noise, blur=blur)
    cs, rs, V, ch = scores(img)
    face = (cs > 0.30) | (rs > 0.10)
    cap = (rs > 0.10) | ((V > 0.62) & (ch < 0.12) & (cs > 0.30) &
                         (np.abs(np.arange(W)[None, :]-W/2) < 1e9))
    cap = rs > 0.10
    r = P.analyze(cs, rs, face, cap)
    if r is None: return None
    r['h_true'] = htrue2; r['phi_true'] = phi
    # emblem centroid
    yy, xx = np.mgrid[0:H, 0:W]
    d2 = (xx-r['cap']['cx'])**2 + (yy-r['cap']['cy'])**2
    em = (V > 0.62) & (ch < 0.12) & (d2 < (0.6*r['cap']['b'])**2)
    r['emb'] = (((xx*V*em).sum()/(V*em).sum()), ((yy*V*em).sum()/(V*em).sum())) \
               if em.sum() > 8 else None
    return r

if __name__ == '__main__':
    import sys
    H_TRUE = [0.005, 0.015, 0.040, 0.060]
    PHIS = [8, 25, 40, 55, 65]
    print('CALIBRATION  (seated cap, dome depth = h + 12.3 mm)')
    print('%7s %5s | %7s %7s %7s | %8s %8s %8s | %7s'
          % ('h_true', 'phi', 'r_cream', 'cos_phi', 'phi_hat', 'q_obs',
             'h_rec', 'err_mm', 'radrat'))
    rows = []
    for ht in H_TRUE:
        for phi in PHIS:
            r = one(ht, phi, seed=int(ht*1e4)+phi)
            if r is None:
                print('%7.1f %5d   FAILED' % (ht*1000, phi)); continue
            rc = r['cream']['ratio']
            phi_hat = np.degrees(np.arccos(np.clip(rc, -1, 1)))
            d_rec = F.invert_q(r['q'], phi_hat, CAPPROF)
            h_rec = d_rec - 0.0123 if np.isfinite(d_rec) else np.nan
            print('%7.1f %5d | %7.4f %7.4f %7.2f | %8.4f %8.1f %+8.1f | %7.4f'
                  % (r['h_true']*1000, phi, rc, np.cos(np.radians(phi)), phi_hat,
                     r['q'], h_rec*1000 if np.isfinite(h_rec) else np.nan,
                     (h_rec-r['h_true'])*1000 if np.isfinite(h_rec) else np.nan,
                     r['rad_ratio']))
            rows.append((ht, phi, rc, r['q'], h_rec, r['h_true'], r['rad_ratio']))
    np.save('r51_cal2.npy', np.array(rows))
