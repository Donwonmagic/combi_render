import numpy as np, math
SENSOR_W=36.0; RES=(1600,1100)
def cam(loc,tgt,lens):
    loc=np.array(loc,float); tgt=np.array(tgt,float)
    f=(tgt-loc); f/=np.linalg.norm(f)
    up=np.array([0,0,1.0])
    r=np.cross(f,up); r/=np.linalg.norm(r)
    u=np.cross(r,f)
    return loc,f,r,u
def proj(P,loc,f,r,u,lens):
    v=np.array(P,float)-loc
    z=v.dot(f)
    if z<=0: return None
    xs=v.dot(r)/z*lens/(SENSOR_W/2)      # -1..1 across width
    ys=v.dot(u)/z*lens/(SENSOR_W/2)
    px=(xs+1)/2*RES[0]
    py=(1-ys*RES[0]/RES[1])/2*RES[1]
    return px,py
# lid geometry
LID_X0,LID_X1=0.9640,-1.0700; LID_Y_HINGE=-0.5450; LID_W=1.1100
zh=2.006
for deg in (104.0,76.0,68.0,82.0):
    a=math.radians(deg)
    fy=LID_Y_HINGE+LID_W*math.cos(a); fz=zh+LID_W*math.sin(a)
    print("alpha=%5.1f  free edge y=%+.4f z=%.4f"%(deg,fy,fz))
    for name,(loc,tgt,lens) in {"counter":((3.40,5.20,1.98),(-0.55,0.75,1.26),90),
                                "playa":((3.15,5.75,1.60),(-0.30,0.45,1.40),42)}.items():
        L,f,r,u=cam(loc,tgt,lens)
        pts={"hinge fore":(LID_X0,LID_Y_HINGE,zh),"hinge aft":(LID_X1,LID_Y_HINGE,zh),
             "free fore":(LID_X0,fy,fz),"free aft":(LID_X1,fy,fz)}
        out=[]
        for k,P in pts.items():
            q=proj(P,L,f,r,u,lens)
            out.append("%s(%.0f,%.0f)"%(k,q[0],q[1]) if q else k+"BEHIND")
        print("   %-8s %s"%(name," ".join(out)))
print("frame is 0..1600 x 0..1100")
