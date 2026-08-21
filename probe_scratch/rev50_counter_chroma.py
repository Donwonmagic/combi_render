import numpy as np
from PIL import Image
def lum(a): return 0.2126*a[...,0]+0.7152*a[...,1]+0.0722*a[...,2]
def rep(nm,a):
    a=a.reshape(-1,3); m=a.mean(axis=0)
    mx=a.max(axis=1);mn=a.min(axis=1); s=((mx-mn)/np.maximum(mx,1e-6)).mean()
    print('%-28s rgb %s  L %6.1f  sat %.3f  R-B %5.1f  sd(L) %.2f'%(nm,np.round(m,1),lum(m),s,m[0]-m[2],lum(a).std()))
ph=np.asarray(Image.open('ref_side.jpg').convert('RGB')).astype(float)
rn=np.asarray(Image.open('out/r49board_side.png').convert('RGB')).astype(float)
# PHOTO: cream flank between bay1 and bay2 pillar (x 432-453 is the card) use x 437..452 above card? use flank under bay2 y 402..? 
rep('PHOTO cream flank pillar', ph[300:320, 706:760])      # cream aft of bay3, above counter
rep('PHOTO cream flank fwd',    ph[250:300, 300:320])
rep('PHOTO counter fascia',     np.array([ph[int(round(-0.04214*x+451.1))+3:int(round(-0.04214*x+451.1))+19,x] for x in range(430,930)]))
rep('PHOTO counter top(outer)', np.array([ph[int(round(-0.04214*x+451.1))-9:int(round(-0.04214*x+451.1))-6,x] for x in range(560,930)]))
print()
# RENDER: cream flank aft of bay3 above counter x 1150..1250 y 560..600
rep('REND cream flank aft',  rn[560:600, 1150:1250])
rep('REND cream flank fwd',  rn[500:540, 640:700])
sol=(-1.76105322e-02, 6.52427054e+02)
rep('REND counter fascia', np.array([rn[int(round(sol[0]*x+sol[1]))+5:int(round(sol[0]*x+sol[1]))+21,x] for x in range(620,1240)]))
