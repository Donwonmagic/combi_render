"""Per-frame wheel measurement: flange-lip ellipse + cap-edge ellipse,
adaptive per-ray levels, threshold sweep, outboard-signed axial offset."""
import sys; sys.path.insert(0,'/home/user/combi_render/probe_scratch/rev50/measure')
import numpy as np, rays, ellip, wheelfit as W
from scipy.optimize import least_squares

def ell_r(a,b,ang,th):
    ca,sa=np.cos(th),np.sin(th); c,s=np.cos(ang),np.sin(ang)
    u=(c*ca+s*sa)/a; v=(-s*ca+c*sa)/b
    return 1/np.hypot(u,v)


def ray_ell(ox,oy,th,x0,y0,A,B,ang):
    """positive-r intersection of ray (ox,oy)+r*(cos,sin) with ellipse
       centred (x0,y0), semi-axes A,B, rotated by ang."""
    c,sn=np.cos(ang),np.sin(ang)
    dx,dy=np.cos(th),np.sin(th)
    ex,ey=ox-x0,oy-y0
    u0=( c*ex+sn*ey)/A; v0=(-sn*ex+c*ey)/B
    ud=( c*dx+sn*dy)/A; vd=(-sn*dx+c*dy)/B
    a=ud*ud+vd*vd; b=2*(u0*ud+v0*vd); cc=u0*u0+v0*v0-1
    disc=b*b-4*a*cc
    if disc<0: return None
    r=(-b+np.sqrt(disc))/(2*a)
    return r if r>0 else None

def cross_last(r,v,level,lo,hi,rising):
    m=(r>=lo)&(r<=hi); rr=r[m]; vv=v[m]
    if rr.size<3: return None
    s=np.sign(vv-level); idx=np.where(np.diff(s)!=0)[0]
    good=[i for i in idx if (vv[i+1]>vv[i])==rising]
    if not good: return None
    i=good[-1]
    v0,v1=vv[i],vv[i+1]; t=(level-v0)/(v1-v0+1e-12)
    return rr[i]+t*(rr[i+1]-rr[i])

def measure(path, cx, cy, R0, ratio0=0.65, chan_out='V', chan_in='V',
            excl_out=(), excl_in=(), fracs=(0.35,0.5,0.65), dstep=0.5,
            step=0.15, nit=4, minc_out=35., minc_in=35., verbose=True,
            tyre_ratio=1.513, ba0=0.6):
    img=rays.load(path)
    CH={'V':img.max(2),'m':img.min(2),'G':img[:,:,1],'B':img[:,:,2],
        'L':img.mean(2)}
    Co=CH[chan_out]; Ci=CH[chan_in]
    angs=np.deg2rad(np.arange(0,360,dstep))
    # bootstrap
    a,b,ang,x0,y0=R0,R0*0.7,0.0,cx,cy
    s=ratio0; xi,yi=cx,cy
    out=[]
    for frac in fracs:
        a,b,ang,x0,y0=R0,R0*ba0,np.pi/2,cx,cy; s=ratio0; xi,yi=cx,cy
        for it in range(nit):
            OP=[];IP=[]
            for th in angs:
                Ro=ell_r(a,b,ang,th)
                # OUTER: cream -> tyre, falling
                r,v=rays.ray_profile(Co,x0,y0,th,Ro*1.9,step)
                Rin=ray_ell(x0,y0,th,xi,yi,a*s,b*s,ang)
                lo_c=(Rin*1.10+1.0) if Rin is not None else Ro*0.72
                cream=v[(r>lo_c)&(r<Ro*0.94)]
                tyre =v[(r>Ro*1.18)&(r<Ro*1.55)]
                if cream.size>3 and tyre.size>3:
                    Pc=np.median(cream); Pt=np.percentile(tyre,25)
                    if Pc-Pt>minc_out:
                        lev=Pt+frac*(Pc-Pt)
                        ro=rays.subpix_cross(r,v,lev,Ro*0.88,Ro*1.18,rising=False)
                        if ro is not None:
                            OP.append((x0+ro*np.cos(th),y0+ro*np.sin(th),np.rad2deg(th)%360))
                # INNER: cap -> cream, rising (take OUTERMOST crossing)
                Ri=ell_r(a*s,b*s,ang,th)
                Rout=ray_ell(xi,yi,th,x0,y0,a,b,ang)
                if Rout is None: continue
                r2,v2=rays.ray_profile(Ci,xi,yi,th,Rout*1.10,step)
                cap  =v2[(r2>Ri*0.30)&(r2<Ri*0.80)]
                crm  =v2[(r2>Ri*1.14+1.0)&(r2<Rout*0.94)]
                if cap.size>3 and crm.size>3:
                    Pk=np.median(cap); Pr=np.median(crm)
                    if Pr-Pk>minc_in:
                        lev2=Pk+frac*(Pr-Pk)
                        ri=cross_last(r2,v2,lev2,Ri*0.80,Ri*1.25,rising=True)
                        if ri is not None:
                            IP.append((xi+ri*np.cos(th),yi+ri*np.sin(th),np.rad2deg(th)%360))
            OP=np.array(OP); IP=np.array(IP)
            if OP.ndim<2 or IP.ndim<2:
                print('    frac %.2f iter %d: no edges (OP %s IP %s)'%(frac,it,OP.shape,IP.shape)); OP=None; break
            mo=np.ones(len(OP),bool)
            for lo,hi in excl_out: mo&=~((OP[:,2]>=lo)&(OP[:,2]<=hi))
            mi=np.ones(len(IP),bool)
            for lo,hi in excl_in: mi&=~((IP[:,2]>=lo)&(IP[:,2]<=hi))
            dO,kO,rO=robust_ell(OP[mo])
            a,b,ang,x0,y0=dO['a'],dO['b'],dO['ang'],dO['x0'],dO['y0']
            p,kI,rI=robust_con(IP[mi],dO)
            xi,yi,s=p
        if OP is None: continue
        mind=np.array([-np.sin(ang),np.cos(ang)]); majd=np.array([np.cos(ang),np.sin(ang)])
        off=np.array([xi-x0,yi-y0])
        ba=b/a; sth=np.sqrt(max(1e-9,1-ba*ba))
        out.append(dict(frac=frac,a=a,b=b,ba=ba,ang=ang,x0=x0,y0=y0,s=s,xi=xi,yi=yi,
                        dmin=off@mind,dmaj=off@majd,mindir=mind,sth=sth,
                        nO=int(kO.sum()),nI=int(kI.sum()),
                        rmsO=float(np.std(rO[kO])),rmsI=float(np.std(rI[kI])),
                        DoverRf=(off@mind)/a/sth))
        if verbose:
            o=out[-1]
            print('  frac %.2f | flange a=%.3f b=%.3f b/a=%.4f c=(%.2f,%.2f) rms=%.2f n=%d'
                  ' | cap s=%.4f c=(%.2f,%.2f) rms=%.2f n=%d | d_minor=%+.3f px d_major=%+.3f'
                  ' | Delta/Rf=%+.4f  mindir=(%+.3f,%+.3f)'%(
                  frac,o['a'],o['b'],o['ba'],o['x0'],o['y0'],o['rmsO'],o['nO'],
                  o['s'],o['xi'],o['yi'],o['rmsI'],o['nI'],o['dmin'],o['dmaj'],
                  o['DoverRf'],mind[0],mind[1]))
    return out

def robust_ell(P,niter=8,kap=2.5,floor=0.8):
    pts=P[:,:2]; keep=np.ones(len(pts),bool)
    for _ in range(niter):
        d=ellip.decode(ellip.fit_ellipse(pts[keep,0],pts[keep,1]))
        r=W.ell_pt_dist(pts,d['x0'],d['y0'],d['a'],d['b'],d['ang'])*d['a']
        sd=np.std(r[keep]); keep=np.abs(r)<max(floor,kap*sd)
    return d,keep,r

def robust_con(P,dO,niter=8,kap=2.5,floor=0.8):
    pts=P[:,:2]; keep=np.ones(len(pts),bool); p=[dO['x0'],dO['y0'],0.65]
    for _ in range(niter):
        p,f=W.constrained_fit(pts[keep],dO['a'],dO['b'],dO['ang'],p[0],p[1])
        r=W.ell_pt_dist(pts,p[0],p[1],p[2]*dO['a'],p[2]*dO['b'],dO['ang'])*p[2]*dO['a']
        sd=np.std(r[keep]); keep=np.abs(r)<max(floor,kap*sd)
    return p,keep,r
