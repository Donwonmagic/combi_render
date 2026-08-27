import os, sys, io, contextlib
HERE = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, HERE)
os.environ.setdefault("T1_SUB", "1")
os.environ["T1_VERIFY"] = "1"
import bpy
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(compile(open(os.path.join(HERE,"build.py")).read(), "build.py", "exec"),
         {"__name__": "__main__", "__file__": os.path.join(HERE,"build.py")})
log = buf.getvalue()
for L in log.split("\n"):
    s=L.strip()
    if ("bumper" in s.lower() or s.startswith("length") or "VERIFY:" in s
        or "warn" in s.lower() and "length" in s.lower() or s.startswith("dims")):
        print("LOG>", s)
def W(ob):
    m=ob.matrix_world; return [m@v.co for v in ob.data.vertices]
bmp=bpy.data.objects["bumper_f"]; body=bpy.data.objects["T1_body"]
pb,pd=W(bmp),W(body)
print("BUMP_BOW env=%s"%os.environ.get("T1_BUMP_BOW"))
print("bumper x max %.4f   shell x max %.4f   bumper - crown %+0.1f mm"%(max(c.x for c in pb),max(c.x for c in pd),1000*(max(c.x for c in pb)-max(c.x for c in pd))))
# shell x at the bumper's own dropped z, y=0
zb=0.4147
s=[c.x for c in pd if abs(c.z-zb)<0.02 and abs(c.y)<0.02]
print("shell x at bumper z %.4f, |y|<0.02 : max %.4f  (bumper inner face at y=0 = path+BUMP_OFF)"%(zb,max(s) if s else -9))
iron=[o for o in bpy.data.objects if o.name.startswith("iron")]
for o in iron:
    p=W(o); print("  %-8s x %.4f..%.4f"%(o.name,min(c.x for c in p),max(c.x for c in p)))
