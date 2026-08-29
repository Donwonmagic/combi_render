import os,sys,io,contextlib,hashlib
HERE=os.path.dirname(os.path.abspath(__file__))+"/.."
sys.path.insert(0,HERE); os.environ.setdefault("T1_SUB","1")
import bpy
buf=io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(compile(open(os.path.join(HERE,"build.py")).read(),"build.py","exec"),
         {"__name__":"__main__","__file__":os.path.join(HERE,"build.py")})
import t1_detail as D, t1_core as T
ob=bpy.data.objects["bumper_f"]
m=ob.matrix_world
co=[tuple(round(c,6) for c in (m@v.co)) for v in ob.data.vertices]
print("BOW=%s  bumper_f verts=%d faces=%d  md5(sorted coords)=%s"
      %(os.environ.get("T1_BUMP_BOW"), len(ob.data.vertices), len(ob.data.polygons),
        hashlib.md5(repr(sorted(co)).encode()).hexdigest()[:16]))
ob2=bpy.data.objects["bumper"] if "bumper" in bpy.data.objects else None
for nm in ("bumper_r","bumper"):
    o=bpy.data.objects.get(nm)
    if o: print("   rear %s verts=%d"%(nm,len(o.data.vertices)))
# corrected station table, converting to the UN-DROPPED frame the build uses
drop=T.RAKE_Z0+T.RAKE_DZDX*2.11
ny=T.WX(2.108)*T.G(0.4800)
print("\ndrop at x=2.11 is %.4f m; build-time z is UN-DROPPED, probe runs POST-drop")
print(" z_UNDROPPED  misses/23   bow s(0)-s(corner) mm")
z=0.65
while z<=1.40001:
    f=D._nose_plan_x(z-drop); s0=f(ny); miss=0; vals=[]
    for i in range(1,24):
        y=-ny+2*ny*i/24; v=f(y)
        if v is None or s0 is None: miss+=1
        else: vals.append((y,v))
    mid=min(vals,key=lambda p:abs(p[0])) if vals else None
    tag="  <<< SHIPPED BUMP_BOW_Z=1.100" if abs(z-1.10)<1e-9 else ("  <<< rev69's rejected 1.000" if abs(z-1.00)<1e-9 else "")
    print("   %.3f       %2d/23      %s%s"%(z,miss,("%+7.2f"%(1000*(mid[1]-s0))) if (mid and s0) else "  n/a  ",tag))
    z+=0.05
