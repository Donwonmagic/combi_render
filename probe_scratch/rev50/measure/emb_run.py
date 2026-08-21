import sys; sys.path.insert(0,'/home/user/combi_render/probe_scratch/rev50/measure')
import numpy as np, rays
from PIL import Image

def run(name, path, box, flange, mindir, outboard_sign, a_px, ba, thrs, mode='cream',
        vmin=90., save=None):
    """flange=(x0,y0); mindir=(mx,my); outboard_sign=+1 if outboard is +mindir.
       returns proudness in mm for each threshold."""
    img=rays.load(path); mn=img.min(2); mx=img.max(2)
    S=np.where(mx>0,(mx-mn)/np.maximum(mx,1),0)
    x0,y0,x1,y1=box
    sub=img[y0:y1,x0:x1]; Ssub=S[y0:y1,x0:x1]; Msub=mx[y0:y1,x0:x1]
    sth=np.sqrt(max(1e-9,1-ba*ba)); scale=a_px/0.2198
    md=np.array(mindir,float); md/=np.linalg.norm(md)
    maj=np.array([-md[1],md[0]])
    print('%s   sin(theta)=%.4f  scale=%.1f px/m  1 px = %.2f mm of proudness'%(
        name,sth,scale,1000/(scale*sth)))
    out=[]
    for t in thrs:
        M=(Ssub<t)&(Msub>vmin) if mode=='cream' else (Ssub>t)&(Msub>vmin)
        ys,xs=np.nonzero(M)
        if len(xs)<5: print('   thr %.2f : too few px'%t); continue
        cx=xs.mean()+x0; cy=ys.mean()+y0
        bx=(xs.min()+xs.max())/2+x0; by=(ys.min()+ys.max())/2+y0
        for lab,(px,py) in [('centroid',(cx,cy)),('bbox-mid',(bx,by))]:
            off=np.array([px-flange[0],py-flange[1]])
            d=(off@md)*outboard_sign; dm=off@maj
            h=d/(a_px*sth)*219.8
            print('   thr %.2f  %-9s (%.2f,%.2f) n=%d  d_out=%+.2f px  d_major=%+.2f px  ->  h = %+.1f mm'%(
                t,lab,px,py,int(M.sum()),d,dm,h))
            if lab=='centroid': out.append(h)
        if save:
            vis=sub.copy(); vis[M]=[0,255,0]
            Image.fromarray(vis.astype('uint8')).resize(((x1-x0)*14,(y1-y0)*14),Image.NEAREST).save(save%t)
    return out
