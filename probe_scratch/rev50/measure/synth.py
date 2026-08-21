"""Synthetic oblique wheel: black tyre disc, cream annulus, dome cap.
Perspective camera. Renders at a chosen pixel scale so the pipeline sees the
same sampling as the photographs."""
import numpy as np

def render(theta_deg, Rf, Rc, Delta, H, Z, f_px, W=260, Hh=260, ss=4,
           y_annulus=0.0, cream_rin=0.0, tyre_R=1.52, blur=1.0, cream=245., chrome=95.,
           tyre=55., rng=None):
    th=np.deg2rad(theta_deg)
    ax=np.array([np.sin(th),0.,-np.cos(th)])          # outboard axis
    e1=np.array([0.,1.,0.]); e1=e1-ax*(e1@ax); e1/=np.linalg.norm(e1)
    e2=np.cross(ax,e1)
    C =np.array([0.,0.,Z])                            # flange-plane centre
    # supersampled image grid centred on the projection of C
    cx0=f_px*C[0]/C[2]; cy0=f_px*C[1]/C[2]
    xs=(np.arange(W*ss)+0.5)/ss - W/2 + cx0
    ys=(np.arange(Hh*ss)+0.5)/ss - Hh/2 + cy0
    X,Y=np.meshgrid(xs,ys)
    d=np.stack([X/f_px, Y/f_px, np.ones_like(X)],-1)
    d/=np.linalg.norm(d,axis=-1,keepdims=True)
    img=np.full(X.shape, np.nan)
    tmin=np.full(X.shape, np.inf)

    def plane_hit(y_off, rin, rout, val):
        P=C+ax*y_off
        den=d@ax
        t=((P)@ax)/np.where(np.abs(den)<1e-9,1e-9,den)
        Q=d*t[...,None]
        v=Q-P
        r=np.hypot(v@e1, v@e2)
        m=(t>0)&(r>=rin)&(r<=rout)&(t<tmin)
        img[m]=val; tmin[m]=t[m]

    # tyre (big black disc) sits at the flange plane, behind everything
    plane_hit(0.0, Rf, tyre_R*Rf, tyre)
    # cream annulus, in the flange plane (y_annulus offset allowed)
    plane_hit(y_annulus, cream_rin, Rf, cream)
    # dome: spherical cap, base radius Rc at axial offset Delta, height H
    if H>1e-6:
        Rs=(Rc*Rc+H*H)/(2*H)
        Sc=C+ax*(Delta+H-Rs)
        oc=-Sc
        b=2*(d@oc); c=(oc*oc).sum()-Rs*Rs
        disc=b*b-4*c
        ok=disc>0
        sq=np.sqrt(np.where(ok,disc,0))
        for t in [(-b-sq)/2, (-b+sq)/2]:
            Q=d*t[...,None]
            hgt=(Q-C)@ax
            m=ok&(t>0)&(hgt>=Delta)&(hgt<=Delta+H+1e-9)&(t<tmin)
            img[m]=chrome; tmin[m]=t[m]
    else:
        plane_hit(Delta, 0.0, Rc, chrome)
    img=np.where(np.isnan(img),20.,img)
    # box-downsample
    img=img.reshape(Hh,ss,W,ss).mean(axis=(1,3))
    if blur>0:
        from scipy.ndimage import gaussian_filter
        img=gaussian_filter(img,blur)
    if rng is not None:
        img=img+rng.normal(0,2.0,img.shape)
    return img, (W/2, Hh/2)      # image, centre-of-flange pixel (approx)


def render_dished(theta_deg, Rf, Rc, Delta, H, Z, f_px, W=300, Hh=300, ss=4,
                  tyre_R=1.513, blur=1.0, cream=245., chrome=95., tyre=55.,
                  Nann=120, rng=None):
    """Realistic wheel: conical (dished) cream disc from (Rc,Delta) to (Rf,0),
    spherical cap of base radius Rc, height H, sitting at y=Delta.
    Delta<0 = cap edge recessed INBOARD of the flange-lip plane."""
    th=np.deg2rad(theta_deg)
    ax=np.array([np.sin(th),0.,-np.cos(th)])
    e1=np.array([0.,1.,0.]); e1=e1-ax*(e1@ax); e1/=np.linalg.norm(e1)
    e2=np.cross(ax,e1)
    C =np.array([0.,0.,Z])
    cx0=f_px*C[0]/C[2]; cy0=f_px*C[1]/C[2]
    xs=(np.arange(W*ss)+0.5)/ss - W/2 + cx0
    ys=(np.arange(Hh*ss)+0.5)/ss - Hh/2 + cy0
    X,Y=np.meshgrid(xs,ys)
    d=np.stack([X/f_px, Y/f_px, np.ones_like(X)],-1)
    d/=np.linalg.norm(d,axis=-1,keepdims=True)
    img=np.full(X.shape, np.nan); tmin=np.full(X.shape, np.inf)
    def plane_hit(y_off, rin, rout, val):
        P=C+ax*y_off
        den=d@ax
        t=(P@ax)/np.where(np.abs(den)<1e-9,1e-9,den)
        Q=d*t[...,None]; v=Q-P
        r=np.hypot(v@e1, v@e2)
        m=(t>0)&(r>=rin)&(r<=rout)&(t<tmin)
        img[m]=val; tmin[m]=t[m]
    plane_hit(0.0, Rf, tyre_R*Rf, tyre)                # tyre
    # dished cream cone, inner->outer, as a stack of annuli
    edges=np.linspace(Rc, Rf, Nann+1)
    for i in range(Nann):
        r0,r1=edges[i],edges[i+1]
        rm=0.5*(r0+r1)
        yv=Delta*(Rf-rm)/(Rf-Rc)
        plane_hit(yv, r0, r1, cream)
    plane_hit(Delta, 0.0, Rc, cream)                   # centre pan (behind cap)
    Rs=(Rc*Rc+H*H)/(2*H)
    Sc=C+ax*(Delta+H-Rs)
    oc=-Sc; bq=2*(d@oc); cq=(oc*oc).sum()-Rs*Rs
    disc=bq*bq-4*cq; ok=disc>0; sq=np.sqrt(np.where(ok,disc,0))
    for t in [(-bq-sq)/2, (-bq+sq)/2]:
        Q=d*t[...,None]; hgt=(Q-C)@ax
        m=ok&(t>0)&(hgt>=Delta-1e-9)&(hgt<=Delta+H+1e-9)&(t<tmin)
        img[m]=chrome; tmin[m]=t[m]
    img=np.where(np.isnan(img),20.,img)
    img=img.reshape(Hh,ss,W,ss).mean(axis=(1,3))
    if blur>0:
        from scipy.ndimage import gaussian_filter
        img=gaussian_filter(img,blur)
    if rng is not None: img=img+rng.normal(0,2.0,img.shape)
    return img


def render_cone(theta_deg, Rf, Rc, Delta, H, Z, f_px, W=300, Hh=300, ss=4,
                tyre_R=1.513, blur=1.0, cream=245., chrome=95., tyre=55.,
                rng=None):
    """Analytic conical dished disc + spherical cap.  Delta<0 = cap recessed."""
    th=np.deg2rad(theta_deg)
    ax=np.array([np.sin(th),0.,-np.cos(th)])
    e1=np.array([0.,1.,0.]); e1=e1-ax*(e1@ax); e1/=np.linalg.norm(e1)
    e2=np.cross(ax,e1)
    C =np.array([0.,0.,Z])
    cx0=f_px*C[0]/C[2]; cy0=f_px*C[1]/C[2]
    xs=(np.arange(W*ss)+0.5)/ss - W/2 + cx0
    ys=(np.arange(Hh*ss)+0.5)/ss - Hh/2 + cy0
    X,Y=np.meshgrid(xs,ys)
    d=np.stack([X/f_px, Y/f_px, np.ones_like(X)],-1)
    d/=np.linalg.norm(d,axis=-1,keepdims=True)
    img=np.full(X.shape, np.nan); tmin=np.full(X.shape, np.inf)
    def put(t, m, val):
        mm=m&(t<tmin)&(t>0)
        img[mm]=val; tmin[mm]=t[mm]
    def plane_hit(y_off, rin, rout, val):
        P=C+ax*y_off
        den=d@ax
        t=(P@ax)/np.where(np.abs(den)<1e-9,1e-9,den)
        Q=d*t[...,None]; v=Q-P
        r=np.hypot(v@e1, v@e2)
        put(t,(r>=rin)&(r<=rout),val)
    plane_hit(0.0, Rf, tyre_R*Rf, tyre)
    if abs(Delta)<1e-6:
        plane_hit(0.0, 0.0, Rf, cream)
    else:
        al=d@ax; be=C@ax; ga=d@C; de=(C*C).sum()
        m=(Rf-Rc)/Delta
        A=1-al*al*(1+m*m)
        B=-2*ga+2*al*be*(1+m*m)+2*Rf*m*al
        C0=de-be*be-Rf*Rf-2*Rf*m*be-m*m*be*be
        disc=B*B-4*A*C0; ok=disc>0
        sq=np.sqrt(np.where(ok,disc,0))
        ylo,yhi=min(0.,Delta),max(0.,Delta)
        for t in [(-B-sq)/(2*A),(-B+sq)/(2*A)]:
            yv=al*t-be
            put(t, ok&(yv>=ylo-1e-9)&(yv<=yhi+1e-9), cream)
        plane_hit(Delta, 0.0, Rc, cream)      # flat centre pan behind the cap
    Rs=(Rc*Rc+H*H)/(2*H)
    Sc=C+ax*(Delta+H-Rs)
    oc=-Sc; bq=2*(d@oc); cq=(oc*oc).sum()-Rs*Rs
    dq=bq*bq-4*cq; ok=dq>0; sq=np.sqrt(np.where(ok,dq,0))
    for t in [(-bq-sq)/2,(-bq+sq)/2]:
        Q=d*t[...,None]; hgt=(Q-C)@ax
        put(t, ok&(hgt>=Delta-1e-9)&(hgt<=Delta+H+1e-9), chrome)
    img=np.where(np.isnan(img),20.,img)
    img=img.reshape(Hh,ss,W,ss).mean(axis=(1,3))
    if blur>0:
        from scipy.ndimage import gaussian_filter
        img=gaussian_filter(img,blur)
    if rng is not None: img=img+rng.normal(0,2.0,img.shape)
    return img
