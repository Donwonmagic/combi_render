import os, sys, io, contextlib
HERE = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, HERE); os.environ.setdefault("T1_SUB","1"); os.environ["T1_VERIFY"]="1"
import bpy
buf=io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(compile(open(os.path.join(HERE,"build.py")).read(),"build.py","exec"),
         {"__name__":"__main__","__file__":os.path.join(HERE,"build.py")})
for L in buf.getvalue().split("\n"):
    if "length" in L or "dims " in L or "x range" in L: print("LOG>",L.strip())
def W(o):
    m=o.matrix_world; return [m@v.co for v in o.data.vertices]
pb=W(bpy.data.objects["bumper_f"])
iron=bpy.data.objects["iron1F"]; pi=W(iron)
ixmax=max(c.x for c in pi); iy=[c.y for c in pi]
print("BOW=%s  iron1F front x %.4f  y %.4f..%.4f  z %.4f..%.4f"
      %(os.environ.get("T1_BUMP_BOW"), ixmax, min(iy),max(iy),min(c.z for c in pi),max(c.z for c in pi)))
for y0 in (0.000,0.235,0.470,0.600):
    s=[c for c in pb if abs(abs(c.y)-y0)<0.015 and 0.40<c.z<0.44]
    if s: print("   blade at |y|=%.3f (z 0.40-0.44): back(min x) %.4f  front(max x) %.4f"
                %(y0,min(c.x for c in s),max(c.x for c in s)))
s=[c for c in pb if abs(abs(c.y)-0.470)<0.015]
print("   blade at |y|=0.470 ALL z: back(min x) %.4f  ->  iron front %.4f  =>  overlap %+0.1f mm"
      %(min(c.x for c in s), ixmax, 1000*(ixmax-min(c.x for c in s))))
