import numpy as np
from PIL import Image
def lum(a): return 0.2126*a[...,0]+0.7152*a[...,1]+0.0722*a[...,2]
rnI=Image.open('out/r49board_side.png').convert('RGB')
rn=np.asarray(rnI).astype(float)
ph=np.asarray(Image.open('ref_side.jpg').convert('RGB')).astype(float)
S=268.9; PS=211.5
k=PS/S
small=rnI.resize((int(rnI.width*k),int(rnI.height*k)),Image.LANCZOS)
rs=np.asarray(small).astype(float)
def ix(X): return (800.7 - S*X)*k
def iy(Z): return (637.0 + S*(1.2540 - Z))*k
BAYS=[(0.6720,0.5155),(0.0470,0.5155),(-0.5980,0.5155)]
print('RENDER downsampled to the photo\'s 211.5 px/m:')
for i,(cx,w) in enumerate(BAYS):
    x0=ix(cx+w/2); x1=ix(cx-w/2); y0=iy(1.7750); y1=iy(1.3720)
    dx=(x1-x0)*0.05; dy=(y1-y0)*0.05
    L=lum(rs[int(y0+dy):int(y1-dy), int(x0+dx):int(x1-dx)])
    print('  bay%d %dx%d px  L mean %.1f sd %.2f p5 %.1f p95 %.1f'%(i+1,L.shape[1],L.shape[0],L.mean(),L.std(),*np.percentile(L,[5,95])))
PB=[(323,430,324.0,405.6),(455,564,314.8,400.0),(588,699,309.4,398.0)]
print('PHOTO:')
for i,(x0,x1,y0,y1) in enumerate(PB):
    dx=(x1-x0)*0.05; dy=(y1-y0)*0.05
    L=lum(ph[int(y0+dy):int(y1-dy), int(x0+dx):int(x1-dx)])
    print('  bay%d %dx%d px  L mean %.1f sd %.2f p5 %.1f p95 %.1f'%(i+1,L.shape[1],L.shape[0],L.mean(),L.std(),*np.percentile(L,[5,95])))
