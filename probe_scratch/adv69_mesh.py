import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, HERE)
os.environ.setdefault("T1_SUB", "1")
import bpy
src = open(os.path.join(HERE, "build.py")).read()
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(compile(src, "build.py", "exec"), {"__name__": "__main__", "__file__": os.path.join(HERE,"build.py")})
log = buf.getvalue()
for L in log.split("\n"):
    if "nose face" in L or "bumper plan bow" in L or "length" in L.lower()[:20]:
        print("BUILD>", L.strip())

def W(ob):
    m = ob.matrix_world
    return [m @ v.co for v in ob.data.vertices]

bmp = bpy.data.objects["bumper_f"]; body = bpy.data.objects["T1_body"]
pb, pbody = W(bmp), W(body)

def bow(pts, zlo=None, zhi=None):
    if zlo is not None: pts=[c for c in pts if zlo<=c.z<=zhi]
    if not pts: return None
    o={}
    for y0 in (0.0,0.70):
        s=[c.x for c in pts if abs(abs(c.y)-y0)<0.02]
        if not s: return None
        o[y0]=max(s)
    return 1000*(o[0.0]-o[0.70])

print("REPLICA verify bow(bumper_f) = %.2f mm" % bow(pb))
zref = 1.100-0.085
print("REPLICA verify bow(shell @ zref %.4f) = %.2f mm" % (zref, bow(pbody, zref-0.02, zref+0.02)))

# --- where do the vertices in each bin come from?
for y0 in (0.0,0.70):
    s=[c for c in pb if abs(abs(c.y)-y0)<0.02]
    s.sort(key=lambda c:-c.x)
    print("  bumper bin |y|=%.2f : n=%d  max-x %.4f at (x %.4f y %+.4f z %.4f); x range %.4f..%.4f"
          %(y0,len(s),max(c.x for c in s),s[0].x,s[0].y,s[0].z,min(c.x for c in s),max(c.x for c in s)))

# --- CROWN and overall extent
print("\nshell x max (CROWN) = %.4f   bumper_f x max = %.4f   -> bumper is %+.1f mm vs crown"
      % (max(c.x for c in pbody), max(c.x for c in pb), 1000*(max(c.x for c in pb)-max(c.x for c in pbody))))
allx=[]; ally=[]
names=[]
for ob in bpy.data.objects:
    if ob.type!='MESH' or not ob.data.vertices: continue
    p=W(ob); allx += [(c.x,ob.name) for c in p]
print("GLOBAL x max = %.4f on %s ; x min = %.4f on %s"
      % (max(allx)[0], max(allx)[1], min(allx)[0], min(allx)[1]))
tot_v=sum(len(o.data.vertices) for o in bpy.data.objects if o.type=='MESH')
tot_f=sum(len(o.data.polygons) for o in bpy.data.objects if o.type=='MESH')
n_m=len([o for o in bpy.data.objects if o.type=='MESH'])
print("mesh objects %d  vertices %d  faces %d  (STATE.md at rev68a: 228 / 331471 / 321650)"%(n_m,tot_v,tot_f))

# --- shell plan bow vs z, finely, DROPPED frame
print("\nSHELL plan bow (max-x at |y|<0.02 minus max-x at |y|-0.70|<0.02), dropped z:")
out=[]
z=0.40
while z<=1.30001:
    b=bow(pbody,z-0.02,z+0.02)
    out.append((z,b))
    print("   z_dropped %.3f (undropped ~%.3f)  bow %s"%(z, z+0.085, ("%+.2f mm"%b) if b is not None else "NONE"))
    z+=0.05
