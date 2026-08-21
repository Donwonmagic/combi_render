import numpy as np
from PIL import Image
def lum(a): return 0.2126*a[...,0]+0.7152*a[...,1]+0.0722*a[...,2]
def sat(a):
    mx=a.max(axis=-1); mn=a.min(axis=-1); return (mx-mn)/np.maximum(mx,1e-6)
rn = np.asarray(Image.open('out/r49board_side.png').convert('RGB')).astype(float)
rows=[]; tops=[];bots=[]
for x in range(600,1150):
    col=rn[600:700,x]
    rg=col[:,0]-col[:,1]
    # gold band: rg in 10..60 ; red flank: rg>60
    red=np.where(rg>60)[0]
    gold=np.where((rg>12)&(rg<60))[0]
    if len(red)==0 or len(gold)==0: continue
    g_end=gold[gold<red[0]].max() if (gold<red[0]).any() else None
    if g_end is None: continue
    t=600+g_end+2; b=600+red[0]-2
    if b-t<12: continue
    tops.append(t);bots.append(b)
    rows.append(rn[t:t+12,x])
R=np.array(rows)
print('n cols',len(rows),'band depth median',np.median(np.array(bots)-np.array(tops)))
L=lum(R)
print('REND fascia rgb',R.reshape(-1,3).mean(axis=0).round(1),'sat %.3f'%sat(R.reshape(-1,3)).mean())
print('REND fascia L mean %.1f sd %.2f  p2/p50/p98 %.1f %.1f %.1f'%(L.mean(),L.std(),*np.percentile(L,[2,50,98])))
print('REND col-mean sd %.2f'%L.mean(axis=1).std())
# fraction of pixels more than 15 codes below the local median
med=np.median(L)
print('frac pixels < med-15: %.3f   < med-30: %.3f'%((L<med-15).mean(),(L<med-30).mean()))
ph = np.asarray(Image.open('ref_side.jpg').convert('RGB')).astype(float)
xs=np.array([470,530,600,860,900]); tps=np.array([431,429,426,415,413]); c=np.polyfit(xs,tps,1)
rowsP=[ph[int(round(np.polyval(c,x)))+2:int(round(np.polyval(c,x)))+14,x] for x in range(430,930)]
P=np.array(rowsP); LP=lum(P)
medp=np.median(LP)
print('PHOTO frac < med-15: %.3f  < med-30: %.3f'%((LP<medp-15).mean(),(LP<medp-30).mean()))
