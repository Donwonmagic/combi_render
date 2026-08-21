import numpy as np
from PIL import Image
def lum(a): return 0.2126*a[...,0]+0.7152*a[...,1]+0.0722*a[...,2]
rn=np.asarray(Image.open('out/r49board_side.png').convert('RGB')).astype(float)
sol=(-1.76105322e-02, 6.52427054e+02)
B=np.array([rn[int(round(sol[0]*x+sol[1]))+5:int(round(sol[0]*x+sol[1]))+21,x] for x in range(620,1240)])
L=lum(B)              # cols x rows
base=np.percentile(L,90)
for th in (8,15,25,40):
    print('  render fascia: frac of area more than %d codes below the clean (p90) tone: %.3f'%(th,(L<base-th).mean()))
print('  clean tone p90 = %.1f ; area sampled %.2f m x %.2f m'%(base, 620/268.9, 16/268.9))
# blotch scale: 1-D autocorrelation of the column-mean deficit
d=base-L.mean(axis=1); d=d-d.mean()
ac=np.correlate(d,d,'full')[len(d)-1:]; ac/=ac[0]
half=np.argmax(ac<0.5)
print('  chip-field autocorrelation half-width along the counter: %d px = %.0f mm'%(half, half/268.9*1000))
# counter TOP, r49s_counter.png
rc=np.asarray(Image.open('out/r49s_counter.png').convert('RGB')).astype(float)
tops=[]
for x in range(1250,1560,1):
    col=rc[500:700,x]; rb=col[:,0]-col[:,2]; rg=col[:,0]-col[:,1]
    rbm=np.where(rg<45,rb,-999); g=int(np.argmax(rbm))
    if rbm[g]<25: continue
    tops.append(lum(rc[500+g-16:500+g-4,x]))
T=np.array(tops); bt=np.percentile(T,90)
print('  render counter TOP (r49s_counter): p90 %.1f ; frac >15 below %.3f ; >30 below %.3f ; sd %.2f'%(bt,(T<bt-15).mean(),(T<bt-30).mean(),T.std()))
# photo counter TOP band, ref_rear34
r34=np.asarray(Image.open('ref_rear34.jpg').convert('RGB')).astype(float)
pt=[]
for x in range(620,980):
    col=r34[380:520,x]; rb=col[:,0]-col[:,2]; g=int(np.argmax(rb))
    if rb[g]<55: continue
    pt.append(lum(r34[380+g-16:380+g-4,x]))
P=np.array(pt); bp=np.percentile(P,90)
print('  photo  counter TOP (ref_rear34): p90 %.1f ; frac >15 below %.3f ; >30 below %.3f ; sd %.2f'%(bp,(P<bp-15).mean(),(P<bp-30).mean(),P.std()))
