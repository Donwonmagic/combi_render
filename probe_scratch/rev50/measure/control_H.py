import sys; sys.path.insert(0,'/home/user/combi_render/probe_scratch/rev50/measure')
import numpy as np, synth
from control_dished import pipe
Rf=0.2198; th=49.7; Z=4.24; f=319.*Z
print('CONTROL C -- sensitivity to dome height H and cap radius Rc.  theta=49.7 Z=4.24')
print('  Rc      H(mm)  D_true  b/a    s_rec   D_rec(mm)  err(mm)')
for Rc in [0.130,0.145,0.160]:
    for H in [0.020,0.045,0.070,0.090]:
        for Dt in [-0.033]:
            im=synth.render_cone(th,Rf,Rc,Dt,H,Z,f)
            r=pipe(im,th,Z,f,Rc)
            print('  %.3f  %5.1f  %+6.1f  %.4f %.4f  %+9.2f  %+7.2f'%(Rc,H*1000,Dt*1000,r[1],r[2],r[0]*1000,(r[0]-Dt)*1000))
