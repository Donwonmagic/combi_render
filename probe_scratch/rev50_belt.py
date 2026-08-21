"""rev50 -- the cream/red break line in ref_side.jpg, column by column, in metres
above ground, against t1_mats.z_belt(x).
INSTRUMENTS: SPEC 10.35 flank map (u->x), SPEC 10.34 k_t carried (px/m vertical),
datum = REAR HUB (749.60, 604.0) at z = TIRE_R = 0.3325 BY CONSTRUCTION (t1_core:80,
build.py:360 "centre at exactly TIRE_R, contact patch on z=0").
CEILING: k_t carries +-2.3% (the two calibrated instruments disagree at the hub,
flank_compare.py:226) -> +-2.3% of the LEVER (v_hub - v)/kv, i.e. +-20 mm at a
0.9 m lever.  Hub row +-0.5 px = +-2.3 mm.  Edge fit noise printed per column.
"""
import numpy as np, ast, sys
from PIL import Image
import scipy.ndimage as nd
A,B,C = 641220.4, 11140.0, 55.0322
KT=215.5; U_RHUB=749.38
def fX(u): return A/(np.asarray(u,float)+B)-C
def mpp(u): return A/(np.asarray(u,float)+B)**2
def kv(u): return KT*mpp(U_RHUB)/mpp(u)
def vhub(u): return 604.0-0.0087*(np.asarray(u,float)-749.6)
def zref(u,v): return 0.3325+(vhub(u)-v)/kv(u)

# --- model belt, PARSED not typed -------------------------------------------
src=open('t1_mats.py').read()
def const(name,txt):
    for n in ast.parse(txt).body:
        if isinstance(n,ast.Assign) and any(getattr(t,'id','')==name for t in n.targets):
            try: return ast.literal_eval(n.value)
            except Exception: return None
    return None
Z_BELT_AUTH=const('Z_BELT_AUTH',src); V_APEX_AUTH=const('V_APEX_AUTH',src)
tsrc=open('t1_core.py').read()
RAKE_Z0=const('RAKE_Z0',tsrc); RAKE_DZDX=const('RAKE_DZDX',tsrc); TIRE_R=const('TIRE_R',tsrc)
Z_BELT0=Z_BELT_AUTH-RAKE_Z0
def z_belt(x): return Z_BELT0-RAKE_DZDX*np.asarray(x,float)
print("parsed: Z_BELT_AUTH %.4f RAKE_Z0 %.6f RAKE_DZDX %.6f TIRE_R %.4f -> Z_BELT0 %.5f"
      %(Z_BELT_AUTH,RAKE_Z0,RAKE_DZDX,TIRE_R,Z_BELT0))

im=np.asarray(Image.open('ref_side.jpg').convert('RGB'),float)
R,G,Bc=im[...,0],im[...,1],im[...,2]
red=(R-0.5*(G+Bc))/(R+G+Bc+1e-6)      # redness; cream low, red high
lum=im.mean(2)

def break_row(u,r0,r1):
    s=nd.gaussian_filter1d(red[r0:r1,u],1.0)
    g=np.gradient(s)
    i=int(np.argmax(g))
    if g[i]<0.004: return None,g[i]
    a,b=max(0,i-2),min(len(g),i+3)
    w=np.clip(g[a:b],0,None)
    if w.sum()<=0: return None,g[i]
    return r0+(np.arange(a,b)*w).sum()/w.sum(), g[i]

print("\n  u      x(m)    v_break   z_meas   z_belt(x)   diff(mm)  grad")
for u in range(120,960,10):
    x=float(fX(u))
    # search window: model belt +-0.18 m around expected row
    zb=float(z_belt(x))
    v_exp=float(vhub(u)-(zb-TIRE_R)*kv(u))
    r0,r1=int(v_exp-45),int(v_exp+45)
    if r0<0 or r1>im.shape[0]: continue
    v,g=break_row(u,r0,r1)
    if v is None: 
        print("%4d %+7.3f      --                                  (weak %.4f)"%(u,x,g)); continue
    z=float(zref(u,v))
    print("%4d %+7.3f   %7.2f  %7.4f  %7.4f  %+8.1f   %.4f"%(u,x,v,z,zb,(z-zb)*1000,g))
