"""Which physical circles do the cream and cap boundaries actually sit on?
Uses the renderer's own hit buffers -- ground truth, rim-side only."""
import numpy as np, r51_scene as SC, r51_inst as IN
from r51_geom import camera_rays, cast

def truth_of_boundary(prims, phi, dist, f_px, W, H, score_fn, thresh, rlo, rhi,
                      eps=-12.0):
    img, m, t = SC.render(prims, phi, eps_deg=eps, dist=dist, f_px=f_px,
                          W=W, H=H, bg=0.16, noise=0.0, blur=0.0)
    phr = np.radians(phi); epr = np.radians(eps)
    v = np.array([np.sin(phr)*np.cos(epr), np.cos(phr), np.sin(phr)*np.sin(epr)])
    C = v*dist
    Cc, d = camera_rays(W, H, f_px, C, (0, 0, 0))
    P = C + t[..., None]*d
    Y = P[..., 1]; R = np.sqrt(P[..., 0]**2 + P[..., 2]**2)
    sc = score_fn(img)
    ys, xs = np.nonzero((sc > thresh))
    cx, cy = xs.mean(), ys.mean()
    ang = np.linspace(0, 2*np.pi, 720, endpoint=False)
    r0 = np.sqrt(len(xs)/np.pi)
    pts = IN.outer_edge(sc, cx, cy, rlo*r0, rhi*r0, ang, thresh)
    # sample true (y,r) just INSIDE the found edge
    out = []
    for (px, py, a, rr) in pts:
        qx = cx + (rr-1.5)*np.cos(a); qy = cy + (rr-1.5)*np.sin(a)
        i, j = int(round(qy)), int(round(qx))
        if 0 <= i < H and 0 <= j < W and np.isfinite(t[i, j]):
            out.append((Y[i, j], R[i, j]))
    out = np.array(out)
    return out, pts

def cream_score(img):
    V = img.max(-1); ch = V - img.min(-1); return V - 1.6*ch
def red_score(img):
    return img[..., 0] - np.maximum(img[..., 1], img[..., 2])

if __name__ == '__main__':
    for phi in (25, 45, 65):
        prims, h, apex = SC.scene_seated(SC.DOME_DEPTH_AUTHORED)
        o, _ = truth_of_boundary(prims, phi, 4.0, 1800., 520, 520,
                                 cream_score, 0.30, 0.15, 1.35)
        print('phi %2d  CREAM boundary: r = %.4f +/- %.4f   y = %.4f +/- %.4f  (n=%d)'
              % (phi, o[:, 1].mean(), o[:, 1].std(), o[:, 0].mean(), o[:, 0].std(), len(o)))
        o2, _ = truth_of_boundary(prims, phi, 4.0, 1800., 520, 520,
                                  red_score, 0.10, 0.05, 1.30)
        print('        CAP   boundary: r = %.4f +/- %.4f   y = %.4f +/- %.4f  (n=%d)'
              % (o2[:, 1].mean(), o2[:, 1].std(), o2[:, 0].mean(), o2[:, 0].std(), len(o2)))
