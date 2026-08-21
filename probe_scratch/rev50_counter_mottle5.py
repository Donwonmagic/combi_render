import numpy as np
from PIL import Image
def lum(a): return 0.2126*a[...,0]+0.7152*a[...,1]+0.0722*a[...,2]
def sat(a):
    mx=a.max(axis=-1); mn=a.min(axis=-1); return (mx-mn)/np.maximum(mx,1e-6)
rn = np.asarray(Image.open('out/r49board_side.png').convert('RGB')).astype(float)
# straight-line fit of fascia band, anchored visually: at x=700 fascia 643..665
# find red-flank top at two clean x to get the slope
def redtop(x):
    col=rn[600:700,x]; rg=col[:,0]-col[:,1]; red=(rg>60)
    i=99
    while i>0 and red[i-1]: i-=1
    return 600+i
a1,a2=redtop(680),redtop(1180)
m=(a2-a1)/500.0
print('redtop 680=%d 1180=%d slope=%.4f'%(a1,a2,m))
band=[]
for x in range(620,1240):
    t=a1+m*(x-680)
    band.append(rn[int(round(t))-19:int(round(t))-3,x])
B=np.array(band)                     # cols x 16 x 3
Image.fromarray(B.transpose(1,0,2).astype(np.uint8)).resize((620*2,32),Image.NEAREST).save('probe_scratch/rev50_counter-galley_rendfascia_band.png')
L=lum(B)
print('REND fascia rgb',B.reshape(-1,3).mean(axis=0).round(1),'sat %.3f'%sat(B.reshape(-1,3)).mean())
print('REND L mean %.1f sd %.2f p2/p50/p98 %.1f %.1f %.1f'%(L.mean(),L.std(),*np.percentile(L,[2,50,98])))
med=np.median(L); print('frac<med-15 %.3f <med-30 %.3f'%((L<med-15).mean(),(L<med-30).mean()))
ph = np.asarray(Image.open('ref_side.jpg').convert('RGB')).astype(float)
xs=np.array([470,530,600,860,900]); tps=np.array([431,429,426,415,413]); c=np.polyfit(xs,tps,1)
P=np.array([ph[int(round(np.polyval(c,x)))+3:int(round(np.polyval(c,x)))+19,x] for x in range(430,930)])
Image.fromarray(P.transpose(1,0,2).astype(np.uint8)).resize((500*2,32),Image.NEAREST).save('probe_scratch/rev50_counter-galley_photofascia_band.png')
LP=lum(P); medp=np.median(LP)
print('PHOTO rgb',P.reshape(-1,3).mean(axis=0).round(1),'sat %.3f'%sat(P.reshape(-1,3)).mean())
print('PHOTO L mean %.1f sd %.2f p2/p50/p98 %.1f %.1f %.1f'%(LP.mean(),LP.std(),*np.percentile(LP,[2,50,98])))
print('PHOTO frac<med-15 %.3f <med-30 %.3f'%((LP<medp-15).mean(),(LP<medp-30).mean()))
