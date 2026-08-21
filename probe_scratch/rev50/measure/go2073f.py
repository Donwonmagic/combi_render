import sys; sys.path.insert(0,'/home/user/combi_render/probe_scratch/rev50/measure')
import numpy as np, rays, ellip, wheelfit as W, fitwheel2 as F

def run(path, cx, cy, rmax, excl_deg, label, frac_list=(0.35,0.5,0.65)):
    img=rays.load(path); V=img.max(2)
    angs=np.deg2rad(np.arange(0,360,0.5))
    # bootstrap with fixed thresholds
    OP,IP=W.edges(V,cx,cy,rmax,155.,215.,angs,0.20*rmax,0.75*rmax,0.35*rmax,rmax)
    d,_,_=F.robust_ell(OP)
    p,_,_=F.robust_con(IP,d)
    for it in range(3):
        OP,IP=F.extract(V,d,p,angs,frac=0.5)
        d,_,_=F.robust_ell(OP)
        p,_,_=F.robust_con(IP,d)
    print('=== %s ==='%label)
    out=[]
    for frac in frac_list:
        OP,IP=F.extract(V,d,p,angs,frac=frac)
        dd,kO,rO=F.robust_ell(OP)
        ang_deg=np.rad2deg(IP[:,2])%360
        m=np.ones(len(IP),bool)
        for lo,hi in excl_deg: m &= ~((ang_deg>=lo)&(ang_deg<=hi))
        pp,kI,rI=F.robust_con(IP[m],dd)
        off=np.array([pp[0]-dd['x0'],pp[1]-dd['y0']])
        dmin=off@dd['mindir']; dmaj=off@dd['majdir']
        ba=dd['b']/dd['a']; sth=np.sqrt(max(1e-9,1-ba*ba))
        print(' frac=%.2f  OUT a=%.3f b=%.3f b/a=%.4f c=(%.3f,%.3f) rms=%.2f n=%d | IN s=%.4f c=(%.3f,%.3f) rms=%.2f n=%d/%d | d_minor=%+.3f d_major=%+.3f | Delta/R_f=%.4f'%(
            frac, dd['a'],dd['b'],ba,dd['x0'],dd['y0'],np.std(rO[kO]),kO.sum(),
            pp[2],pp[0],pp[1],np.std(rI[kI]),kI.sum(),len(kI),dmin,dmaj, dmin/dd['a']/sth))
        out.append((frac,dd,pp,dmin,dmaj))
    return out

run('/home/user/combi_render/IMG_2073.jpeg',744.,811.,85,[(195,290)],'IMG_2073 FRONT wheel')
