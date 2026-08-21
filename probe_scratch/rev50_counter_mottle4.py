import numpy as np
from PIL import Image
def lum(a): return 0.2126*a[...,0]+0.7152*a[...,1]+0.0722*a[...,2]
def sat(a):
    mx=a.max(axis=-1); mn=a.min(axis=-1); return (mx-mn)/np.maximum(mx,1e-6)
rn = np.asarray(Image.open('out/r49board_side.png').convert('RGB')).astype(float)
rows=[]
for x in range(560,1290):
    col=rn[600:700,x]; rg=col[:,0]-col[:,1]
    red=(rg>60)
    # last contiguous run ending at 99
    if not red[-1]: continue
    i=99
    while i>0 and red[i-1]: i-=1
    top=600+i                      # first row of the red flank
    if top<640: continue
    rows.append(rn[top-19:top-2,x])
R=np.array(rows); L=lum(R)
print('cols',len(rows))
print('REND fascia rgb',R.reshape(-1,3).mean(axis=0).round(1),'sat %.3f'%sat(R.reshape(-1,3)).mean())
print('REND L mean %.1f sd %.2f p2/p50/p98 %.1f %.1f %.1f'%(L.mean(),L.std(),*np.percentile(L,[2,50,98])))
med=np.median(L); print('frac<med-15 %.3f <med-30 %.3f'%((L<med-15).mean(),(L<med-30).mean()))
print('col-mean sd %.2f'%L.mean(axis=1).std())
