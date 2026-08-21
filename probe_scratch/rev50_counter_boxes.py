import numpy as np
from PIL import Image
def lum(a): return 0.2126*a[...,0]+0.7152*a[...,1]+0.0722*a[...,2]
ph=np.asarray(Image.open('ref_side.jpg').convert('RGB')).astype(float)
L=lum(ph[384:398, 700:850]).mean(axis=0)     # bright foil rows only
x=np.arange(700,850)
hi=np.percentile(L,80); lo=np.percentile(L,10); half=(hi+lo)/2
print('bright %.1f  dark %.1f  half-max %.1f'%(hi,lo,half))
b=L>half
edges=[]
for i in range(1,len(b)):
    if b[i]!=b[i-1]:
        # sub-pixel by linear interp
        t=(half-L[i-1])/(L[i]-L[i-1])
        edges.append(x[i-1]+t)
print('edges', [round(e,2) for e in edges])
runs=[(edges[i],edges[i+1]) for i in range(0,len(edges)-1,2)]
print('bright runs (box faces):')
for (a,bb) in runs:
    print('   %.2f - %.2f  width %.2f px = %.0f mm @211.9'%(a,bb,bb-a,(bb-a)/211.9*1000))
cen=[(a+bb)/2 for (a,bb) in runs]
print('centres',[round(c,1) for c in cen])
print('pitches px',[round(cen[i+1]-cen[i],2) for i in range(len(cen)-1)])
print('pitch mm  ',[round((cen[i+1]-cen[i])/211.9*1000) for i in range(len(cen)-1)])
def X(xi): return -0.686-(xi-641.0)/211.9
print('model X of the rank: %.3f .. %.3f  (211.9 px/m)'%(X(runs[0][0]),X(runs[-1][1])))
print('model X of the rank: %.3f .. %.3f  (200.0 px/m, rear-fall bound)'%(-0.686-(runs[0][0]-641)/200.,-0.686-(runs[-1][1]-641)/200.))
