import numpy as np
from PIL import Image
G=np.asarray(Image.open('IMG_2073.jpeg').convert('RGB')).astype(float)
print("IMG_2073 (GREEN bus -- these are GEOMETRY quantities: handle station, belt, sill)")
# column scan across the cab door around the handle x~810
for x in (790,800,810,820,830,840):
    col=G[500:640,x]
    R,Gc,B=col[:,0],col[:,1],col[:,2]
    lum=col.mean(axis=1)
    grn=(Gc-R)   # green paint: G > R ; white: G ~ R
    out=[]
    for i in range(1,len(col)-1):
        pass
    # find the white->green break: first row (from top) where G-R rises above 12
    br=None
    for i in range(len(col)):
        if grn[i]>12 and grn[i+1]>12 and grn[i+2]>12: br=500+i; break
    # window sill: the bottom of the dark glass above -- first row from top where lum>140
    sl=None
    for i in range(len(col)):
        if lum[i]>140 and lum[i+1]>140: sl=500+i; break
    # handle: bright chrome (lum high, low sat) inside the green
    hs=[500+i for i in range(len(col)) if grn[i]<6 and lum[i]>110 and (500+i)>(br or 0)]
    print(" x=%d  sill(top of body colour) y=%s   white/green break y=%s   chrome rows in green %s"
          %(x,sl,br,hs[:12]))
