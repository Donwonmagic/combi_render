import numpy as np
from PIL import Image
def lum(a): return 0.2126*a[...,0]+0.7152*a[...,1]+0.0722*a[...,2]
def sat(a):
    mx=a.max(axis=-1); mn=a.min(axis=-1); return (mx-mn)/np.maximum(mx,1e-6)
rn = np.asarray(Image.open('out/r49board_side.png').convert('RGB')).astype(float)
gy=[]
xs=list(range(620,1240))
for x in xs:
    w=rn[615:680,x]
    rb=w[:,0]-w[:,2]
    # gold roll: r-b large but not red (r-g small)
    m=(w[:,0]-w[:,1])<40
    rb=np.where(m,rb,-999)
    gy.append(615+int(np.argmax(rb)))
gy=np.array(gy,float)
# robust line fit
A=np.vstack([np.array(xs),np.ones(len(xs))]).T
for _ in range(5):
    sol,*_=np.linalg.lstsq(A,gy,rcond=None)
    r=gy-A@sol
    keep=np.abs(r)<4
    A2=A[keep];gy2=gy[keep]
    sol,*_=np.linalg.lstsq(A2,gy2,rcond=None)
print('gold line',sol, 'inliers',keep.sum())
band=[];gold=[]
for i,x in enumerate(xs):
    t=int(round(sol[0]*x+sol[1]))
    gold.append(rn[t-2:t+3,x])
    band.append(rn[t+5:t+21,x])
B=np.array(band);G=np.array(gold)
Image.fromarray(B.transpose(1,0,2).astype(np.uint8)).resize((620*2,48),Image.NEAREST).save('probe_scratch/rev50_counter-galley_rendfascia_band.png')
L=lum(B)
print('REND fascia rgb',B.reshape(-1,3).mean(axis=0).round(1),'sat %.3f'%sat(B.reshape(-1,3)).mean())
print('REND L mean %.1f sd %.2f p2/p50/p98 %.1f %.1f %.1f'%(L.mean(),L.std(),*np.percentile(L,[2,50,98])))
med=np.median(L); print('REND frac<med-15 %.3f <med-30 %.3f'%((L<med-15).mean(),(L<med-30).mean()))
LG=lum(G)
print('REND gold rgb',G.reshape(-1,3).mean(axis=0).round(1),'sat %.3f'%sat(G.reshape(-1,3)).mean(),'L %.1f  gold/fascia %.3f'%(LG.mean(),LG.mean()/L.mean()))
