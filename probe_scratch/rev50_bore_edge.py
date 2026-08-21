"""rev50 -- THRESHOLD-FREE ellipse of a circular aperture.

From a seed centre, walk 72 radials outward and take the radius at which
|d/dr (G-R)| is largest (the paint/aperture edge).  Fit a conic to the 72
points by least squares and report the axes.  No threshold, so the
region-growing instability that made the near bore read 0.91..1.27 cannot
recur; the failure mode that remains is a radial that finds a stronger
gradient somewhere else (a highlight, the indicator, the silhouette), so the
per-radial residual against the fit is printed and the worst 15 % are dropped
and the fit repeated.
"""
import numpy as np
from PIL import Image
import sys

im = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float)
CH = im[...,1]-im[...,0] if sys.argv[4]=='GR' else im[...,0]-im[...,1]
cx, cy, rmax = float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[5])

def samp(x,y):
    x0,y0=int(x),int(y); fx,fy=x-x0,y-y0
    return (CH[y0,x0]*(1-fx)*(1-fy)+CH[y0,x0+1]*fx*(1-fy)
            +CH[y0+1,x0]*(1-fx)*fy+CH[y0+1,x0+1]*fx*fy)

def edge_points(cx,cy):
    pts=[]
    for i in range(96):
        a=2*np.pi*i/96; ca,sa=np.cos(a),np.sin(a)
        rs=np.arange(0.25*rmax, rmax, 0.25)
        v=np.array([samp(cx+r*ca, cy+r*sa) for r in rs])
        g=np.abs(np.diff(v))
        k=int(g.argmax())
        pts.append((cx+rs[k]*ca, cy+rs[k]*sa, a))
    return np.array(pts)

def fit_conic(P):
    x,y=P[:,0]-cx,P[:,1]-cy
    A=np.vstack([x*x, x*y, y*y, x, y]).T
    c,*_=np.linalg.lstsq(A, np.ones(len(x)), rcond=None)
    a,b,cc,d,e=c; f=-1.0
    M=np.array([[a,b/2],[b/2,cc]])
    # centre
    cen=np.linalg.solve(2*M, [-d,-e])
    val = a*cen[0]**2+b*cen[0]*cen[1]+cc*cen[1]**2+d*cen[0]+e*cen[1]+f
    ev,evec=np.linalg.eigh(M)
    ax=np.sqrt(-val/ev)
    return np.sort(2*ax), cen, np.degrees(np.arctan2(evec[1,np.argmax(-val/ev)],evec[0,np.argmax(-val/ev)]))

P=edge_points(cx,cy)
for it in range(3):
    (mn,mx),cen,ang=fit_conic(P)
    # residual
    r=np.hypot(P[:,0]-cx-cen[0],P[:,1]-cy-cen[1])
    med=np.median(r)
    keep=np.abs(r-med)<np.percentile(np.abs(r-med),85)
    print("  it%d n=%3d  axes %.1f x %.1f  ratio %.3f  major@%.0fdeg  centre (%.1f,%.1f)"
          %(it,len(P),mx,mn,mn/mx,ang,cx+cen[0],cy+cen[1]))
    P=P[keep]
