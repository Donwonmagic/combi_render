"""ATTACK: proper conic (ellipse) fits to the roundel and the near headlamp
aperture on ref_workshop.jpg, with a threshold sweep, so the two are compared
as ELLIPSES (axis ratio + tilt) and not as bounding boxes.  A bounding box
inflates a TILTED ellipse toward 1:1 and the two features are tilted by
different amounts, so bbox-aspect is not the right comparand.
"""
import numpy as np, math
from PIL import Image
from scipy import ndimage

im = np.asarray(Image.open('ref_workshop.jpg').convert('RGB')).astype(float)
GR = im[...,1]-im[...,0]
L  = im.mean(-1)

def blob_from(mask, seed):
    lab,_ = ndimage.label(mask)
    i = lab[seed]
    if i==0: return None
    return lab==i

def fit_ellipse(ys, xs):
    """direct least-squares conic on the boundary points"""
    x = xs-xs.mean(); y = ys-ys.mean()
    D = np.stack([x*x, x*y, y*y, x, y, np.ones_like(x)],1)
    _,_,V = np.linalg.svd(D, full_matrices=False)
    a,b,c,d,e,f = V[-1]
    M = np.array([[a,b/2],[b/2,c]])
    ev,evec = np.linalg.eigh(M)
    if (ev<=0).any() and (ev>=0).any(): return None
    # centre
    cen = np.linalg.solve(2*M, [-d,-e])
    k = a*cen[0]**2 + b*cen[0]*cen[1] + c*cen[1]**2 + d*cen[0] + e*cen[1] + f
    axes = np.sqrt(-k/ev)
    order = np.argsort(axes)[::-1]
    major, minor = axes[order[0]], axes[order[1]]
    vmaj = evec[:,order[0]]
    ang = math.degrees(math.atan2(vmaj[1], vmaj[0])) % 180
    return minor/major, major, minor, ang, (cen[0]+xs.mean(), cen[1]+ys.mean())

def report(name, box, chan, thr_list, sense):
    x0,y0,x1,y1 = box
    print(f"--- {name}  window x{x0}..{x1} y{y0}..{y1}")
    for thr in thr_list:
        sub = chan[y0:y1, x0:x1]
        m = (sub < thr) if sense=='lt' else (sub > thr)
        seedy, seedx = (y1-y0)//2, (x1-x0)//2
        if not m[seedy,seedx]:
            ys_,xs_ = np.nonzero(m)
            if len(ys_)==0: print(f"  thr {thr}: empty"); continue
            d=(ys_-seedy)**2+(xs_-seedx)**2; k=d.argmin(); seedy,seedx=ys_[k],xs_[k]
        bl = blob_from(m,(seedy,seedx))
        bl = ndimage.binary_fill_holes(bl)
        ys,xs = np.nonzero(bl)
        touch = (xs.min()==0 or xs.max()==x1-x0-1 or ys.min()==0 or ys.max()==y1-y0-1)
        er = ndimage.binary_erosion(bl)
        by,bx = np.nonzero(bl & ~er)
        fe = fit_ellipse(by.astype(float), bx.astype(float))
        w = xs.max()-xs.min()+1; h = ys.max()-ys.min()+1
        s = f"  thr {thr:6.1f}  n={bl.sum():5d}  bbox {w}x{h} = {w/h:.3f}"
        if fe: s += f"   ELLIPSE ratio={fe[0]:.3f} maj={fe[1]*2:.1f} min={fe[2]*2:.1f} majang={fe[3]:.1f}deg"
        if touch: s += "  <<TOUCHES BOX"
        print(s)

# roundel: chrome ring on cream -> use luminance-difference from the cream field.
# cream is bright; the ring is darker.  Threshold on L.
report("ROUNDEL (dark ring on cream)", (270,494,346,600), L, [150,160,170,180,190], 'lt')
# near lamp aperture: not-green
report("NEAR LAMP APERTURE (not-green)", (372,584,466,676), GR, [4,8,12,16,20], 'lt')
