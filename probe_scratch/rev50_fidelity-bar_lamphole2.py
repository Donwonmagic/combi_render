import numpy as np
from PIL import Image
im=np.asarray(Image.open('out/r49s_rear.png').convert('RGB')).astype(float)
def run(box,tag):
    y0,y1,x0,x1=box; sub=im[y0:y1,x0:x1]
    R,G,B=sub[...,0],sub[...,1],sub[...,2]
    lamp=(R>60)&(R<115)&(G<0.75*R)
    core=(R>=112)&(B>0.15*R)&(G<0.45*R)
    ysl,xsl=np.nonzero(lamp); ysc,xsc=np.nonzero(core)
    if len(xsl)==0: print(tag,'none'); return
    Wl=xsl.max()-xsl.min()+1; Hl=ysl.max()-ysl.min()+1
    print("%s lamp bbox W %d H %d  n %d"%(tag,Wl,Hl,lamp.sum()))
    if len(xsc):
        Wc=xsc.max()-xsc.min()+1; Hc=ysc.max()-ysc.min()+1
        print("   core bbox W %d H %d  n %d  ->  core/lamp W %.3f  H %.3f  areafrac %.4f"
              %(Wc,Hc,core.sum(),Wc/Wl,Hc/Hl,core.sum()/lamp.sum()))
        print("   core centre (%.1f,%.1f)  lamp centre (%.1f,%.1f)"
              %(xsc.mean()+x0,ysc.mean()+y0,xsl.mean()+x0,ysl.mean()+y0))
run((820,900,485,565),'LEFT ')
run((820,900,1035,1115),'RIGHT')
print("\nPREDICTED core/lamp diameter ratio from small_lamp's own profile = 0.181")
