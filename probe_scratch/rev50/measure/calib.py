import sys; sys.path.insert(0,'/home/user/combi_render/probe_scratch/rev50/measure')
import numpy as np, rays, ellip, wheelfit as W, fitwheel2 as F, synth

def pipeline(V, cx, cy, rmax, excl_deg=(), frac=0.5, nit=4, dstep=0.5):
    angs=np.deg2rad(np.arange(0,360,dstep))
    OP,IP=W.edges(V,cx,cy,rmax,150.,180.,angs,0.20*rmax,0.80*rmax,0.35*rmax,rmax)
    d,_,_=F.robust_ell(OP); p,_,_=F.robust_con(IP,d)
    for it in range(nit):
        OP,IP=F.extract(V,d,p,angs,frac=frac)
        d,_,_=F.robust_ell(OP)
        ad=np.rad2deg(IP[:,2])%360; m=np.ones(len(IP),bool)
        for lo,hi in excl_deg: m&=~((ad>=lo)&(ad<=hi))
        p,kI,rI=F.robust_con(IP[m],d)
    off=np.array([p[0]-d['x0'],p[1]-d['y0']])
    ba=d['b']/d['a']; sth=np.sqrt(max(1e-9,1-ba*ba))
    return dict(a=d['a'],b=d['b'],ba=ba,ang=d['ang'],x0=d['x0'],y0=d['y0'],
                s=p[2],xi=p[0],yi=p[1],
                dmin=off@d['mindir'],dmaj=off@d['majdir'],sth=sth,
                DoverR=(off@d['mindir'])/d['a']/sth, rmsI=np.std(rI[kI]))

if __name__=='__main__':
    Rf=0.2198; Z=4.27; f=1361.
    print('CONTROL A: recover Delta, dome height H fixed 0.040, Rc=0.145, theta=49.7')
    print('  Delta_true(mm)  H(mm)  ->  b/a    s      dmin(px)  Delta_rec(mm)  err(mm)  dmaj(px)')
    for Dt in [-0.020,0.0,0.010,0.030,0.050,0.070]:
        for Hh in [0.040]:
            im,_=synth.render(49.7,Rf,0.145,Dt,Hh,Z,f)
            r=pipeline(im,130.,130.,110.)
            # sign: outboard is +x in synth -> dmin sign depends on mindir orientation
            sgn=np.sign(r['dmin']) if abs(r['dmin'])>1e-6 else 1
            Drec=r['DoverR']*Rf
            print('   %+7.1f       %5.1f      %.4f  %.4f  %+8.3f   %+8.2f     %+6.2f   %+.2f'%(
              Dt*1000,Hh*1000,r['ba'],r['s'],r['dmin'],Drec*1000,(Drec-Dt)*1000,r['dmaj']))
