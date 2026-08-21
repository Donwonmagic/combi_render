import numpy as np, colorsys
from PIL import Image
def lum(a): return 0.2126*a[...,0]+0.7152*a[...,1]+0.0722*a[...,2]
def hs(m):
    h,s,v=colorsys.rgb_to_hsv(*(m/255.0)); return h*360,s
def rep(nm,a):
    a=a.reshape(-1,3); m=a.mean(axis=0); h,s=hs(m)
    print('%-34s rgb %s L %6.1f hue %5.1f sat %.3f'%(nm,np.round(m,1),lum(m),h,s))
    return lum(m),s
r34=np.asarray(Image.open('ref_rear34.jpg').convert('RGB')).astype(float)
# locate gold nosing per column in ref_rear34 between x 620..1000 ; nosing bright gold
tops=[];fasc=[];golds=[]
for x in range(620,980,4):
    col=r34[380:520,x]
    rb=col[:,0]-col[:,2]
    g=int(np.argmax(rb))
    if rb[g]<55: continue
    y=380+g
    tops.append(r34[y-16:y-6,x]); golds.append(r34[y-1:y+2,x]); fasc.append(r34[y+5:y+15,x])
T=np.array(tops);F=np.array(fasc);G=np.array(golds)
print('ref_rear34.jpg, n cols',len(tops))
lt,st=rep(' PHOTO counter TOP (tan)',T); lf,sf=rep(' PHOTO counter FASCIA',F); lg,sg=rep(' PHOTO brass NOSING',G)
print('   top/fascia  L %.3f   sat %.3f'%(lt/lf, st/sf))
print('   gold/fascia L %.3f   sat %.3f'%(lg/lf, sg/sf))
