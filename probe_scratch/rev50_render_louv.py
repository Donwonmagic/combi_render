"""Render-side louvre block: extent, pitch, count, dark duty cycle.
Projection PARSED from studio.views()['side'] (ortho, exact) -- no landmark hunting."""
import numpy as np, ast, sys
from PIL import Image
import scipy.ndimage as nd
def view(want='side'):
    tree=ast.parse(open('studio.py').read())
    for n in ast.walk(tree):
        if isinstance(n,ast.FunctionDef) and n.name=='views':
            for s in ast.walk(n):
                if isinstance(s,ast.Return) and isinstance(s.value,ast.Dict):
                    for k,v in zip(s.value.keys,s.value.values):
                        if getattr(k,'value',None)==want:
                            return {kw.arg:ast.literal_eval(kw.value) for kw in v.keywords}
    sys.exit('no side view')
V=view(); RX,RY=1600,1100
ppm=RX/V['ortho']; cz=V['tgt'][2]
def X2px(X): return RX/2 - ppm*X
def Z2py(Z): return RY/2 + ppm*cz - ppm*Z
def px2X(p): return (RX/2-p)/ppm
def py2Z(p): return (RY/2+ppm*cz-p)/ppm
print("ortho %.3f  ppm %.4f px/m  cz %.3f"%(V['ortho'],ppm,cz))
im=np.asarray(Image.open('out/r49board_side.png').convert('RGB'),float); lum=im.mean(2)
hp=lum-nd.uniform_filter1d(lum,9,axis=0)
# vertical profile at several columns
for c0,c1 in [(1150,1156),(1170,1176),(1195,1201)]:
    p=hp[665:740,c0:c1].mean(1)
    lo=[665+i for i in range(1,len(p)-1) if p[i]<p[i-1] and p[i]<=p[i+1] and p[i]<-3]
    print("cols %d-%d  minima rows %s"%(c0,c1,lo))
    if len(lo)>1:
        d=np.diff(lo); print("     n=%d  pitch %.3f px = %.2f mm  (built LOUV_PITCH 21.111)"%(len(lo),d.mean(),1000*d.mean()/ppm))
    # duty cycle: fraction of rows with p<0 inside the block
    a,b=lo[0],lo[-1]
    seg=p[a-665:b-665+1]
    print("     dark duty (profile<0) %.3f over rows %d-%d"%((seg<0).mean(),a,b))
    print("     z top slot %.4f  z bottom slot %.4f  span %.4f"%(py2Z(lo[0]),py2Z(lo[-1]),py2Z(lo[0])-py2Z(lo[-1])))
# horizontal extent at the darkest rows
print()
for r in range(670,732):
    row=hp[r,1100:1260]
    idx=np.where(row<-6)[0]
    if len(idx)>5:
        print("row %d  dark cols %d..%d   X %+.4f .. %+.4f  len %.4f"%(r,1100+idx[0],1100+idx[-1],
              px2X(1100+idx[0]),px2X(1100+idx[-1]),px2X(1100+idx[0])-px2X(1100+idx[-1])))
