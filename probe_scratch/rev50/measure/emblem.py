import sys; sys.path.insert(0,'/home/user/combi_render/probe_scratch/rev50/measure')
import numpy as np, rays
from PIL import Image

def centroid(path, box, mask_fn, out_png=None, scale=8):
    img=rays.load(path)
    x0,y0,x1,y1=box
    sub=img[y0:y1,x0:x1]
    M=mask_fn(sub)
    ys,xs=np.nonzero(M)
    if len(xs)<5: return None
    cx=xs.mean()+x0; cy=ys.mean()+y0
    if out_png:
        vis=sub.copy()
        vis[M]=[0,255,0]
        Image.fromarray(vis.astype('uint8')).resize(((x1-x0)*scale,(y1-y0)*scale),Image.NEAREST).save(out_png)
    return cx,cy,int(M.sum())
