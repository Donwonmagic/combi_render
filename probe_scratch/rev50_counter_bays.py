import numpy as np
from PIL import Image
def lum(a): return 0.2126*a[...,0]+0.7152*a[...,1]+0.0722*a[...,2]
rn=np.asarray(Image.open('out/r49board_side.png').convert('RGB')).astype(float)
ph=np.asarray(Image.open('ref_side.jpg').convert('RGB')).astype(float)
S=268.9
def ix(X): return 800.7 - S*X
# vertical anchor: counter top edge.  gold top at x=700 is row 637 -> that is CNT_ZT=1.254
# check with the slab bottom 1.147 -> 637 + 0.107*S = 637+28.8 = 665.8 (measured 666) OK
def iy(Z): return 637.0 + S*(1.2540 - Z)
BAYS=[(0.6720,0.5155),(0.0470,0.5155),(-0.5980,0.5155)]
print('render aperture boxes (5%% inset):')
res=[]
for i,(cx,w) in enumerate(BAYS):
    x0=ix(cx+w/2); x1=ix(cx-w/2); y0=iy(1.7750); y1=iy(1.3720)
    dx=(x1-x0)*0.05; dy=(y1-y0)*0.05
    a=rn[int(y0+dy):int(y1-dy), int(x0+dx):int(x1-dx)]
    L=lum(a); res.append(L)
    print(' bay%d img x %d-%d y %d-%d  L mean %.1f sd %.2f p5 %.1f p50 %.1f p95 %.1f'%(
        i+1,x0,x1,y0,y1,L.mean(),L.std(),*np.percentile(L,[5,50,95])))
PB=[(323,430,324.0,405.6),(455,564,314.8,400.0),(588,699,309.4,398.0)]
print('photo aperture boxes (5%% inset):')
for i,(x0,x1,y0,y1) in enumerate(PB):
    dx=(x1-x0)*0.05; dy=(y1-y0)*0.05
    a=ph[int(y0+dy):int(y1-dy), int(x0+dx):int(x1-dx)]
    L=lum(a)
    print(' bay%d L mean %.1f sd %.2f p5 %.1f p50 %.1f p95 %.1f'%(i+1,L.mean(),L.std(),*np.percentile(L,[5,50,95])))
# save side-by-side crops
for i,(cx,w) in enumerate(BAYS):
    x0=int(ix(cx+w/2)); x1=int(ix(cx-w/2)); y0=int(iy(1.7750)); y1=int(iy(1.3720))
    Image.fromarray(rn[y0:y1,x0:x1].astype(np.uint8)).resize(((x1-x0)*3,(y1-y0)*3),Image.LANCZOS).save(f'probe_scratch/rev50_counter-galley_rendbay{i+1}.png')
for i,(x0,x1,y0,y1) in enumerate(PB):
    Image.fromarray(ph[int(y0):int(y1),x0:x1].astype(np.uint8)).resize(((x1-x0)*4,int(y1-y0)*4),Image.LANCZOS).save(f'probe_scratch/rev50_counter-galley_photobay{i+1}.png')
