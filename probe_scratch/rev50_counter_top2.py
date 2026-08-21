import numpy as np, colorsys
from PIL import Image
def lum(a): return 0.2126*a[...,0]+0.7152*a[...,1]+0.0722*a[...,2]
def hs(m):
    h,s,v=colorsys.rgb_to_hsv(*(m/255.0)); return h*360,s
def rep(nm,a):
    a=a.reshape(-1,3); m=a.mean(axis=0); h,s=hs(m)
    print('%-32s rgb %s L %6.1f hue %5.1f sat %.3f'%(nm,np.round(m,1),lum(m),h,s)); return lum(m),s
rn=np.asarray(Image.open('out/r49s_counter.png').convert('RGB')).astype(float)
tops=[];fasc=[];golds=[];ys=[]
for x in range(1250,1560,2):
    col=rn[500:700,x]
    rb=col[:,0]-col[:,2]
    rg=col[:,0]-col[:,1]
    m=(rg<45)
    rbm=np.where(m,rb,-999)
    g=int(np.argmax(rbm))
    if rbm[g]<25: continue
    y=500+g; ys.append((x,y))
    tops.append(rn[y-14:y-4,x]); golds.append(rn[y-1:y+2,x]); fasc.append(rn[y+5:y+15,x])
print('n',len(tops), ys[:3], ys[-3:])
T=np.array(tops);F=np.array(fasc);G=np.array(golds)
lt,st=rep(' REND counter TOP',T); lf,sf=rep(' REND counter FASCIA',F); lg,sg=rep(' REND brass NOSING',G)
print('   top/fascia  L %.3f  sat %.3f'%(lt/lf,st/sf))
print('   gold/fascia L %.3f  sat %.3f'%(lg/lf,sg/sf))
# mark the sampled rows on an image
im=Image.open('out/r49s_counter.png').convert('RGB'); a=np.asarray(im).copy()
for (x,y) in ys:
    a[y-14:y-4,x]=[0,255,0]; a[y+5:y+15,x]=[0,0,255]; a[y-1:y+2,x]=[255,0,255]
Image.fromarray(a[480:700,1200:1600]).resize((400*2,220*2),Image.NEAREST).save('probe_scratch/rev50_counter-galley_topsample_marked.png')
