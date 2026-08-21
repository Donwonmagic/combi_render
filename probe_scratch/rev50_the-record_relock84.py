"""rev 50 -- SPEC section 8.4 re-run on both copies of the SAME photograph.

SPEC 8.4 gives COLUMN ranges (px x 137-158, 163-180, 185-202, 205-228) and a
"window band" but NO ROW RANGE.  That missing row range is the point: the
window is not stated, so the reader must guess it.  Below, the row band is
SEARCHED on ref_source.jpeg for the band that best reproduces SPEC's own
published luminances, and the band that wins is then SCALED to ref_playa_34.
CEILING: a searched window is weaker evidence than a stated one.  This probe
does not claim to recover SPEC's band -- it claims the band was never written
down, and it prints the spread over plausible bands so the reader can see how
much that costs.
"""
import numpy as np
from PIL import Image

S = np.asarray(Image.open('ref_source.jpeg').convert('RGB'), float).mean(2)
P = np.asarray(Image.open('ref_playa_34.png').convert('RGB'), float).mean(2)
sx, sy = 500/246., 400/197.
BANDS = [(137,158),(163,180),(185,202),(205,228)]
SPEC_LUM = [61.6, 71.6, 106.4, "178-204"]

print("ref_source.jpeg   rows searched 40..110, height 8..24")
best=None
for y0 in range(40,111,2):
    for hh in (8,12,16,20,24):
        y1=y0+hh
        if y1 > S.shape[0]: continue
        v=[S[y0:y1, a:b+1].mean() for a,b in BANDS]
        err=abs(v[0]-61.6)+abs(v[1]-71.6)+abs(v[2]-106.4)+max(0, 178-v[3])+max(0, v[3]-204)
        if best is None or err<best[0]: best=(err,y0,y1,v)
err,y0,y1,v = best
print("  best row band %d..%d  ->  %.1f / %.1f / %.1f  and bright %.1f   (SPEC 61.6/71.6/106.4, 178-204)  total abs err %.1f"
      % (y0,y1,v[0],v[1],v[2],v[3],err))
print("  SPREAD over all searched bands (how much the unstated window is worth):")
allv=[]
for yy in range(40,111,2):
    for hh in (8,12,16,20,24):
        if yy+hh> S.shape[0]: continue
        allv.append([S[yy:yy+hh, a:b+1].mean() for a,b in BANDS])
allv=np.array(allv)
for i,(a,b) in enumerate(BANDS):
    print("    x %3d-%3d  lum min %.1f  max %.1f  (SPEC %s)" % (a,b,allv[:,i].min(),allv[:,i].max(),SPEC_LUM[i]))

py0,py1 = int(round(y0*sy)), int(round(y1*sy))
print("\nref_playa_34.png  same band scaled -> rows %d..%d, columns scaled by %.4f" % (py0,py1,sx))
pv=[P[py0:py1, int(round(a*sx)):int(round(b*sx))+1].mean() for a,b in BANDS]
print("  ->  %.1f / %.1f / %.1f  and bright %.1f" % tuple(pv))
