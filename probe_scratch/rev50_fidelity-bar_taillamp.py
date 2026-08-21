import numpy as np
from PIL import Image
P=np.asarray(Image.open('ref_rear34.jpg').convert('RGB')).astype(float)
# tail lamp in ref_rear34: crop box from the x4 crop -> orig x 880+185/4..880+345/4, y 500+600/4..500+855/4
x0,x1 = 880+185//4, 880+345//4
y0,y1 = 500+600//4, 500+855//4
print("lamp box", x0,x1,y0,y1)
sub=P[y0-6:y1+6, x0-8:x1+8]
Image.fromarray(sub.astype('uint8')).resize(((x1-x0+16)*12,(y1-y0+12)*12), Image.NEAREST).save('probe_scratch/rev50_fidelity-bar_ref_taillamp_x12.png')
# horizontal scan through the lamp centre
cy=(y0+y1)//2
row=P[cy, x0-14:x1+14]
for i,p in enumerate(row):
    lum=p.mean(); sat=(p.max()-p.min())/max(p.max(),1)
    print("x=%4d  R%3d G%3d B%3d  lum %5.1f  sat %.2f"%(x0-14+i,p[0],p[1],p[2],lum,sat))
