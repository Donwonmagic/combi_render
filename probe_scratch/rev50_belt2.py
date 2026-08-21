"""The cream/red break along the WHOLE flank: ref_side.jpg vs the shipped side render,
same estimator (redness gradient, sub-pixel), both in metres above ground.
REF instruments: SPEC 10.35 map (u->x) + SPEC 10.34 k_t carried; hub datum z=TIRE_R.
RENDER: exact ortho from studio.views()['side'].
"""
import numpy as np, ast, sys
from PIL import Image
import scipy.ndimage as nd
A,B,C=641220.4,11140.0,55.0322; KT=215.5; U_RHUB=749.38
fX=lambda u: A/(np.asarray(u,float)+B)-C
fu=lambda x: A/(np.asarray(x,float)+C)-B
mpp=lambda u: A/(np.asarray(u,float)+B)**2
kv=lambda u: KT*mpp(U_RHUB)/mpp(u)
vhub=lambda u: 604.0-0.0087*(np.asarray(u,float)-749.6)
zref=lambda u,v: 0.3325+(vhub(u)-v)/kv(u)
def view(want='side'):
    for n in ast.walk(ast.parse(open('studio.py').read())):
        if isinstance(n,ast.FunctionDef) and n.name=='views':
            for s in ast.walk(n):
                if isinstance(s,ast.Return) and isinstance(s.value,ast.Dict):
                    for k,v in zip(s.value.keys,s.value.values):
                        if getattr(k,'value',None)==want:
                            return {kw.arg:ast.literal_eval(kw.value) for kw in v.keywords}
V=view(); RX,RY=1600,1100; ppm=RX/V['ortho']; cz=V['tgt'][2]
X2px=lambda X: RX/2-ppm*X
py2Z=lambda p: RY/2+ppm*cz-p
def redness(a):
    R,G,Bb=a[...,0],a[...,1],a[...,2]
    return (R-0.5*(G+Bb))/(R+G+Bb+1e-6)
def edge(rd,u,r0,r1,mg):
    s=nd.gaussian_filter1d(rd[r0:r1,u],1.0); g=np.gradient(s); i=int(np.argmax(g))
    if g[i]<mg: return None
    a,b=max(0,i-2),min(len(g),i+3); w=np.clip(g[a:b],0,None)
    if w.sum()<=0: return None
    return r0+(np.arange(a,b)*w).sum()/w.sum()
ref=np.asarray(Image.open('ref_side.jpg').convert('RGB'),float); rr=redness(ref)
gen=np.asarray(Image.open('out/r49board_side.png').convert('RGB'),float); rg=redness(gen)
print("   X(m)    ref u   z_ref     gen px   z_gen    gen-ref (mm)")
for X in np.arange(1.10,-1.95,-0.10):
    u=int(round(float(fu(X))))
    # ref window: 1.30 .. 0.95 m above ground
    v0=int(vhub(u)-(1.32-0.3325)*kv(u)); v1=int(vhub(u)-(0.95-0.3325)*kv(u))
    vr=edge(rr,u,v0,v1,0.004)
    px=int(round(X2px(X)))
    p0=int(RY/2+ppm*cz-ppm*1.32); p1=int(RY/2+ppm*cz-ppm*0.95)
    vg=edge(rg,px,p0,p1,0.004)
    zr=float(zref(u,vr)) if vr else float('nan')
    zg=float(py2Z(vg)/ppm) if vg else float('nan')
    zg=(RY/2+ppm*cz-vg)/ppm if vg else float('nan')
    print("%+7.2f  %6d  %7.4f   %6.1f   %7.4f   %+8.1f"%(X,u,zr,vg if vg else -1,zg,(zg-zr)*1000))
