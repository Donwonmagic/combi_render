"""REV51 A2 -- E2, the SHAPE-INDEPENDENT estimator.

The hubcap's emblem sits on the crown, ON THE AXLE AXIS.  Its image position
is therefore the projection of a single 3-D point at axial height y_emb.  Its
offset from the cream-ring ellipse centre along the minor axis is
    Delta_px = (y_emb - Y_CREAM) * sin(phi) * (px/m)
and NOTHING about the dome's shape enters.  That is the whole point.
"""
import numpy as np
import r51_inst as IN

Y_CREAM  = 0.0585      # axial plane of the cream/tyre boundary  (+/- 0.0055)
Y_FLANGE = 0.0640
EMB_PROUD = 0.0060     # emblem plate above the crown, as built

def emblem_centre(img, capfit, box=None, mode='bright'):
    """centroid of the emblem blob inside the cap.
    box = (x0,y0,x1,y1) in crop pixels, generous; None -> central 55% of cap."""
    H, W = img.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    ct, st = np.cos(-capfit['theta']), np.sin(-capfit['theta'])
    u = ct*(xx-capfit['cx']) - st*(yy-capfit['cy'])
    v = st*(xx-capfit['cx']) + ct*(yy-capfit['cy'])
    inside = (u/capfit['a'])**2 + (v/capfit['b'])**2
    reg = inside < 0.55**2
    if box is not None:
        reg &= (xx >= box[0]) & (xx <= box[2]) & (yy >= box[1]) & (yy <= box[3])
    if reg.sum() < 12:
        return None, None
    V = img.mean(-1)
    med = np.median(V[reg])
    if mode == 'bright':
        d = np.clip(V - med, 0, None)
    else:
        d = np.clip(med - V, 0, None)
    thr = np.percentile(d[reg], 88)
    m = reg & (d > thr)
    if m.sum() < 8:
        return None, None
    w = d*m
    return (float((xx*w).sum()/w.sum()), float((yy*w).sum()/w.sum())), m

def measure_h(creamfit, emb_xy, outboard_hint, R_CREAM=IN.R_CREAM,
              y_cream=Y_CREAM, emb_proud=EMB_PROUD, D_cam=None):
    ratio = creamfit['b']/creamfit['a']
    phi = np.arccos(np.clip(ratio, -1, 1))
    s = creamfit['a']/R_CREAM                       # px per metre
    th = creamfit['theta']
    t = np.array([-np.sin(th), np.cos(th)])          # minor axis
    if np.dot(t, np.asarray(outboard_hint, float)) < 0:
        t = -t
    d = np.array([emb_xy[0]-creamfit['cx'], emb_xy[1]-creamfit['cy']])
    delta = float(np.dot(d, t))
    perp = float(np.dot(d, np.array([np.cos(th), np.sin(th)])))
    sp = np.sin(phi)
    dy = delta/(sp*s) if sp > 1e-6 else np.nan
    # perspective: the ellipse centre of a tilted circle of radius R at range D
    # is displaced from the projected circle centre by ~ R^2 sin(phi)cos(phi)/D
    corr = 0.0
    if D_cam:
        corr = (R_CREAM**2/D_cam)*np.cos(phi)
    h = dy + corr + (y_cream - Y_FLANGE) - emb_proud
    return dict(phi_deg=float(np.degrees(phi)), s=float(s), delta_px=delta,
                perp_px=perp, dy=float(dy), corr=float(corr), h=float(h))
