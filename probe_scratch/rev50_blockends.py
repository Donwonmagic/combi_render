"""Louvre block FORWARD and AFT ends, ref_side.jpg vs the side render.
Same estimator both sides: vertical high-pass (9-tap boxcar detrend), then for each
strong slot row take the longest run of columns below a FRACTIONAL threshold of that
row's own minimum -- dimensionless in amplitude, so paint/exposure cancel (rule 24).
The reading is repeated over a FAMILY of rows and thresholds; the spread IS the ceiling.
REF x from SPEC 10.35 flank map (validated to 1.5 mm at u=852, past this block).
GEN x from studio.views()['side'] ortho, exact."""
import numpy as np, ast, sys
from PIL import Image
import scipy.ndimage as nd
A,B,C=641220.4,11140.0,55.0322
fX=lambda u: A/(np.asarray(u,float)+B)-C
def view(want='side'):
    for n in ast.walk(ast.parse(open('studio.py').read())):
        if isinstance(n,ast.FunctionDef) and n.name=='views':
            for s in ast.walk(n):
                if isinstance(s,ast.Return) and isinstance(s.value,ast.Dict):
                    for k,v in zip(s.value.keys,s.value.values):
                        if getattr(k,'value',None)==want:
                            return {kw.arg:ast.literal_eval(kw.value) for kw in v.keywords}
V=view(); ppm=1600/V['ortho']
gX=lambda p: (800.0-p)/ppm

def runs(hp,r,c0,c1,frac):
    row=hp[r,c0:c1]
    t=frac*row.min()
    m=row<=t
    best=(0,0,0)
    i=0
    while i<len(m):
        if m[i]:
            j=i
            while j+1<len(m) and m[j+1]: j+=1
            if j-i>best[0]-1: best=(j-i+1,i,j)
            i=j+1
        else: i+=1
    return c0+best[1], c0+best[2], best[0]

def report(tag,img,rows,c0,c1,tox):
    a=np.asarray(Image.open(img).convert('RGB'),float).mean(2)
    hp=a-nd.uniform_filter1d(a,9,axis=0)
    X0s,X1s=[],[]
    for r in rows:
        for f in (0.35,0.45,0.55,0.65):
            u0,u1,n=runs(hp,r,c0,c1,f)
            if n<10: continue
            X0s.append(tox(u0)); X1s.append(tox(u1))
    X0s=np.array(X0s); X1s=np.array(X1s)
    print("%-9s n=%d  fwd end %+.4f +- %.4f   aft end %+.4f +- %.4f   length %.4f +- %.4f"
          %(tag,len(X0s),X0s.mean(),X0s.std(),X1s.mean(),X1s.std(),
            (X0s-X1s).mean(),(X0s-X1s).std()))
    return X0s.mean(),X1s.mean()

# REF: the six best-resolved slot rows (rows where the line is unambiguous by eye)
report("ref_side",'ref_side.jpg',[471,472,480,481,489,490],740,880,lambda u: float(fX(u)))
# also the upper, weaker rows
report("ref upper",'ref_side.jpg',[445,450,454,459,463],740,880,lambda u: float(fX(u)))
# GEN: interior slot rows only (skip the aperture-edge bands)
report("render",'out/r49board_side.png',[677,683,689,694,700,706,712,717],1090,1270,gX)
print("\nbuilt (t1_detail LOUV_X0/X1 through T._aft): -1.2419 .. -1.5371, length 0.2952")
print("source header claim (t1_detail.py:2124): -1.285 .. -1.670, length 0.385 +-0.03/0.04")
