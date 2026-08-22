import numpy as np, r51_scene as SC, r51_inst as IN
from r51_geom import fit_ellipse, camera_rays, cast
from PIL import Image, ImageDraw
from r51_truth import cream_score, red_score

W=H=560; dist=4.0; f=1900.
out=[]
for phi in (25,45,65):
    prims,h,apex = SC.scene_seated(SC.DOME_DEPTH_AUTHORED)
    img,m,t = SC.render(prims, phi, eps_deg=-12., dist=dist, f_px=f, W=W,H=H,
                        bg=0.16, noise=0.006, blur=0.8)
    cs=cream_score(img); rs=red_score(img)
    ys,xs=np.nonzero(cs>0.30); cx,cy=xs.mean(),ys.mean(); r0=np.sqrt(len(xs)/np.pi)
    ang=np.linspace(0,2*np.pi,720,endpoint=False)
    cf,cp = IN.fit_boundary(cs,(cx,cy),0.20*r0,1.45*r0,ang)
    kf,kp = IN.fit_boundary(rs,(cf['cx'],cf['cy']),0.05*cf['a'],1.05*cf['a'],ang)
    print('phi %2d  cream a=%.2f b=%.2f b/a=%.4f (cos=%.4f) rms=%.3f n=%d'
          %(phi,cf['a'],cf['b'],cf['b']/cf['a'],np.cos(np.radians(phi)),cf['rms'],cf['n']))
    print('        cap   a=%.2f b=%.2f b/a=%.4f rms=%.3f n=%d  DIFF=%+.4f'
          %(kf['a'],kf['b'],kf['b']/kf['a'],kf['rms'],kf['n'],kf['b']/kf['a']-cf['b']/cf['a']))
    im=Image.fromarray((img*255).astype('uint8'))
    d=ImageDraw.Draw(im)
    for p in cp: d.point((p[0],p[1]),fill=(0,255,0))
    for p in kp: d.point((p[0],p[1]),fill=(0,180,255))
    out.append(im)
o=Image.new('RGB',(W*3,H)); [o.paste(im,(i*W,0)) for i,im in enumerate(out)]
o.save('r51_diag_boundaries.png'); print('saved')
