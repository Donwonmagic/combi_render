import sys; sys.path.insert(0,'/home/user/combi_render/probe_scratch/rev50/measure')
import numpy as np, rays, ellip, wheelfit as W, synth
Rf=0.2198
def pipe(im,th,Z,f,Rc):
    ap=f*Rf/Z; bp=ap*np.cos(np.deg2rad(th)); WW=im.shape[0]
    angs=np.deg2rad(np.arange(0,360,0.5))
    OP,IP=W.edges(im,WW/2,WW/2,1.35*ap,150.,170.,angs, 10, 0.9*ap, 0.55*bp, 1.35*ap)
    if IP.ndim<2 or OP.ndim<2: return None
    dO=ellip.decode(ellip.fit_ellipse(OP[:,0],OP[:,1]))
    dI=ellip.decode(ellip.fit_ellipse(IP[:,0],IP[:,1]))
    dx=(np.array([dI['x0']-dO['x0'],dI['y0']-dO['y0']])@dO['mindir'])
    # force mindir to point +x (outboard in the synthetic)
    if dO['mindir'][0]<0: dx=-dx
    ba=dO['b']/dO['a']; sth=np.sqrt(1-ba*ba)
    return dx/dO['a']*Rf/sth, ba, dI['a']/dO['a'], dx
if __name__=='__main__':
    print('CONTROL B -- DISHED disc, recessed cap.  Rf=0.2198  Rc=0.145  Nann=120')
    print(' theta  Z(m)   H(mm)  D_true(mm)  b/a_rec  s_rec  dx_px   D_rec(mm)   err(mm)')
    for th,Z in [(49.7,4.24),(49.7,3.0),(49.7,7.0),(60.,4.24),(40.,4.24)]:
        f=319.*Z if th==49.7 else 319.*Z
        for H in [0.045]:
            for Dt in [-0.060,-0.045,-0.033,-0.020,0.0,+0.020]:
                im=synth.render_cone(th,Rf,0.145,Dt,H,Z,f)
                r=pipe(im,th,Z,f,0.145)
                if r is None: print('  FAIL'); continue
                print(' %5.1f %5.2f %6.1f  %+9.1f    %.4f  %.4f %+7.3f  %+9.2f  %+8.2f'%(
                    th,Z,H*1000,Dt*1000,r[1],r[2],r[3],r[0]*1000,(r[0]-Dt)*1000))
        print()
