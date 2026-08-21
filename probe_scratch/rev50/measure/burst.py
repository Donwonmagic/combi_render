import sys; sys.path.insert(0,'/home/user/combi_render/probe_scratch/rev50/measure')
import numpy as np, rays
from scipy import ndimage
from PIL import Image

def analyse(name, path, box, thrs, save=None, minpx=25):
    img=rays.load(path); x0,y0,x1,y1=box
    sub=img[y0:y1,x0:x1]
    R,G,B=sub[:,:,0],sub[:,:,1],sub[:,:,2]
    print('=== %s  box=%s ==='%(name,box))
    for t in thrs:
        M=(R-G)>t
        lab,n=ndimage.label(M)
        objs=[]
        for i in range(1,n+1):
            m=lab==i
            if m.sum()<minpx: continue
            ys,xs=np.nonzero(m)
            objs.append(dict(i=i,n=int(m.sum()),
                             x=(xs.min()+x0,xs.max()+x0),y=(ys.min()+y0,ys.max()+y0),
                             cx=xs.mean()+x0, cy=ys.mean()+y0,
                             w=xs.max()-xs.min()+1, h=ys.max()-ys.min()+1))
        objs.sort(key=lambda o:-o['n'])
        print(' thr R-G>%d : %d blobs >=%d px'%(t,len(objs),minpx))
        for o in objs[:6]:
            print('    n=%5d  bbox x %d..%d (w %d)  y %d..%d (h %d)  centroid (%.1f,%.1f)'%(
                o['n'],o['x'][0],o['x'][1],o['w'],o['y'][0],o['y'][1],o['h'],o['cx'],o['cy']))
        if save and t==thrs[len(thrs)//2]:
            vis=sub.copy(); vis[M]=[0,255,0]
            Image.fromarray(vis.astype('uint8')).resize(((x1-x0)*4,(y1-y0)*4),Image.NEAREST).save(save)
    return
