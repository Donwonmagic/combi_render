"""rev50 nose/front: fit the ellipses of the four circular apertures on
ref_workshop.jpg's nose (GREEN bus, GEOMETRY ONLY).

Method: inside a hand-declared box, classify pixels as GREEN PAINT vs NOT,
using (G-R) which separates the green paint from every aperture interior
(shadow, grey bowl, cream, background seen through).  Take the largest
connected NOT-green blob, then report its extreme horizontal and vertical
chords AND a second-moment ellipse fit.  Both are printed so a disagreement
between them is visible rather than hidden.

CEILING: the aperture outline is the boundary between painted panel and
"anything else".  Where the aperture sits at the panel's own silhouette the
blob merges with the background; the box is drawn to stop before that and
the printed blob-touches-box flags say whether it did.
"""
import numpy as np
from PIL import Image
import sys

im = np.asarray(Image.open('ref_workshop.jpg').convert('RGB')).astype(float)
GR = im[..., 1] - im[..., 0]

BOXES = {
    #  name        x0   y0   x1   y1   thr
    'near_lamp': (374, 592, 466, 672, 12),
    'far_lamp':  (212, 548, 244, 626, 12),
    'indicator': (410, 540, 448, 578, 12),
}

def blob(x0, y0, x1, y1, thr):
    sub = GR[y0:y1, x0:x1]
    m = sub < thr                      # not green paint
    # flood from the centre
    h, w = m.shape
    seed = (h // 2, w // 2)
    if not m[seed]:
        # find the nearest True to centre
        ys, xs = np.nonzero(m)
        d = (ys - seed[0]) ** 2 + (xs - seed[1]) ** 2
        seed = (ys[d.argmin()], xs[d.argmin()])
    lab = np.zeros_like(m, dtype=bool)
    stack = [seed]
    lab[seed] = True
    while stack:
        r, c = stack.pop()
        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            rr, cc = r+dr, c+dc
            if 0 <= rr < h and 0 <= cc < w and m[rr,cc] and not lab[rr,cc]:
                lab[rr,cc] = True
                stack.append((rr,cc))
    return lab

for name,(x0,y0,x1,y1,thr) in BOXES.items():
    lab = blob(x0,y0,x1,y1,thr)
    ys,xs = np.nonzero(lab)
    if len(ys)==0:
        print(name,"EMPTY"); continue
    # extreme chords
    wid = xs.max()-xs.min()+1
    hei = ys.max()-ys.min()+1
    # widest row / tallest column
    rowcount = lab.sum(axis=1); colcount = lab.sum(axis=0)
    maxrow = rowcount.max(); maxcol = colcount.max()
    # second-moment ellipse
    cy,cx = ys.mean(), xs.mean()
    myy = ((ys-cy)**2).mean(); mxx=((xs-cx)**2).mean(); mxy=((xs-cx)*(ys-cy)).mean()
    C = np.array([[mxx,mxy],[mxy,myy]])
    ev,evec = np.linalg.eigh(C)
    major = 4*np.sqrt(ev[1]); minor = 4*np.sqrt(ev[0])
    ang = np.degrees(np.arctan2(evec[1,1],evec[0,1]))
    touch = (xs.min()==0, xs.max()==x1-x0-1, ys.min()==0, ys.max()==y1-y0-1)
    print(f"{name:10s} n={len(ys):5d} bbox {wid}x{hei}  widestrow={maxrow} tallestcol={maxcol}")
    print(f"           moment major={major:.1f} minor={minor:.1f} ratio={minor/major:.3f} majang={ang:.1f} deg")
    print(f"           centre=({x0+cx:.1f},{y0+cy:.1f})  touches L/R/T/B = {touch}")
    print(f"           chord-aspect widestrow/tallestcol = {maxrow/maxcol:.3f}")
