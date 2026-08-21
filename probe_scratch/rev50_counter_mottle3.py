import numpy as np
from PIL import Image
def lum(a): return 0.2126*a[...,0]+0.7152*a[...,1]+0.0722*a[...,2]
def sat(a):
    mx=a.max(axis=-1); mn=a.min(axis=-1); return (mx-mn)/np.maximum(mx,1e-6)
rn = np.asarray(Image.open('out/r49board_side.png').convert('RGB')).astype(float)
rows=[]; depths=[]
for x in range(600,1150):
    col=rn[600:700,x]; rg=col[:,0]-col[:,1]
    gold=np.where((rg>12)&(rg<45))[0]
    if len(gold)==0: continue
    g=gold.max()                      # bottom of the gold roll
    below=np.where(rg[g+1:]>60)[0]
    if len(below)==0: continue
    b=g+1+below[0]
    if b-g<15: continue
    depths.append(b-g)
    rows.append(rn[600+g+3:600+g+15,x])
R=np.array(rows); L=lum(R)
print('cols',len(rows),'fascia depth px median',np.median(depths))
print('REND fascia rgb',R.reshape(-1,3).mean(axis=0).round(1),'sat %.3f'%sat(R.reshape(-1,3)).mean())
print('REND L mean %.1f sd %.2f  p2/p50/p98 %.1f %.1f %.1f'%(L.mean(),L.std(),*np.percentile(L,[2,50,98])))
med=np.median(L); print('REND frac<med-15 %.3f  <med-30 %.3f'%((L<med-15).mean(),(L<med-30).mean()))
ph = np.asarray(Image.open('ref_side.jpg').convert('RGB')).astype(float)
xs=np.array([470,530,600,860,900]); tps=np.array([431,429,426,415,413]); c=np.polyfit(xs,tps,1)
P=np.array([ph[int(round(np.polyval(c,x)))+2:int(round(np.polyval(c,x)))+14,x] for x in range(430,930)])
LP=lum(P); medp=np.median(LP)
print('PHOTO rgb',P.reshape(-1,3).mean(axis=0).round(1),'sat %.3f'%sat(P.reshape(-1,3)).mean())
print('PHOTO L mean %.1f sd %.2f p2/p50/p98 %.1f %.1f %.1f'%(LP.mean(),LP.std(),*np.percentile(LP,[2,50,98])))
print('PHOTO frac<med-15 %.3f  <med-30 %.3f'%((LP<medp-15).mean(),(LP<medp-30).mean()))
