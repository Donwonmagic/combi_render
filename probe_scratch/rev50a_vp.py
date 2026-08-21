import numpy as np
from PIL import Image
im = Image.open('/home/user/combi_render/ref_side.jpg').convert('RGB')
A = np.asarray(im).astype(float)
H,W,_ = A.shape
R,G,B = A[:,:,0],A[:,:,1],A[:,:,2]
Y = 0.299*R+0.587*G+0.114*B
# "yellowness": yellow board border is high R,G low B
YEL = (R+G)/2.0 - B

def subpix_edge(row, x0, x1, sign, chan):
    """find max |gradient| of chan along row in [x0,x1]; sign=+1 rising, -1 falling.
    returns parabola-refined x of extremum of signed gradient*sign."""
    seg = chan[row, x0:x1+1]
    g = np.gradient(seg)*sign
    i = int(np.argmax(g))
    if i<=0 or i>=len(g)-1: return None, g[i]
    a,b,c = g[i-1],g[i],g[i+1]
    d = (a-c)/(2*(a-2*b+c)) if (a-2*b+c)!=0 else 0.0
    if abs(d)>1: d=0.0
    return x0+i+d, b

def fit(rows, xlo_fn, xhi_fn, sign, chan, label):
    xs,ys,st=[],[],[]
    for r in rows:
        x0,x1 = int(xlo_fn(r)), int(xhi_fn(r))
        x,s = subpix_edge(r,x0,x1,sign,chan)
        if x is None: continue
        xs.append(x); ys.append(r); st.append(s)
    xs=np.array(xs); ys=np.array(ys); st=np.array(st)
    # robust: 2 rounds of 2.5-sigma clipping about a linear fit
    keep=np.ones(len(xs),bool)
    for _ in range(4):
        p=np.polyfit(ys[keep],xs[keep],1)
        res=xs-np.polyval(p,ys)
        s=res[keep].std()
        keep=np.abs(res)<2.5*max(s,0.3)
    p=np.polyfit(ys[keep],xs[keep],1)
    rms=(xs[keep]-np.polyval(p,ys[keep])).std()
    print("%-28s n=%3d/%3d  slope dx/dy=%+.5f  x0=%8.2f  rms=%.2f px"%(label,keep.sum(),len(xs),p[0],p[1],rms))
    return p, ys[keep], xs[keep]

print("=== BOARD END EDGES (outer edge of the yellow border) ===")
# left/fore end: background (palm/wall, darker or whiter) -> yellow.  use YEL rising
pL,_,_ = fit(range(50,292), lambda r: 300+0.14*(r-50)-14, lambda r: 300+0.14*(r-50)+14, +1, YEL, "L(fore) outer, YEL rise")
pR,_,_ = fit(range(32,278),  lambda r: 760+0.06*(r-32)-14, lambda r: 760+0.06*(r-32)+14, -1, YEL, "R(aft) outer, YEL fall")
def vp(pa,pb):
    # x = a1 y + b1 ; x = a2 y + b2  -> y = (b2-b1)/(a1-a2)
    yv=(pb[1]-pa[1])/(pa[0]-pb[0]); return yv, pa[0]*yv+pa[1]
yv,xv = vp(pL,pR); print("   -> VP_board  y=%.0f  x=%.0f   (image is %dx%d)"%(yv,xv,W,H))
