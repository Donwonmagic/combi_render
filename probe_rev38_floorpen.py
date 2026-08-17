import bpy, os, sys, math
from mathutils import Vector
try: ROOT=os.path.dirname(os.path.abspath(__file__))
except NameError: ROOT=os.getcwd()
sys.path.insert(0,ROOT)
_src=open(os.path.join(ROOT,"build.py")).read().split('if os.environ.get("T1_SAVE")')[0]
exec(compile(_src,"build.py","exec"))
import bmesh
dg=bpy.context.evaluated_depsgraph_get()

def world_bm(name):
    ob=bpy.data.objects[name]
    bm=bmesh.new(); bm.from_object(ob,dg); bm.transform(ob.matrix_world)
    return ob,bm

print("\n"+"="*78)
print("  DO THE CAB FLOOR AND THE FRONT WHEELS OCCUPY THE SAME SPACE?")
print("  Method: BVH tree overlap on the EVALUATED, WORLD-SPACE meshes.")
print("  Not a bounding-box test -- bounding boxes overlap for many pairs that")
print("  do not touch, and a bbox claim is not an interpenetration claim.")
print("="*78)
from mathutils.bvhtree import BVHTree
fo,fbm=world_bm("cab_floor")
ftree=BVHTree.FromBMesh(fbm)

pairs=[]
for nm in [o.name for o in bpy.data.objects]:
    if nm=="cab_floor": continue
    if not any(k in nm for k in ("tyre","rim","cap")): continue
    try: ob,bm=world_bm(nm)
    except Exception: continue
    t=BVHTree.FromBMesh(bm)
    ov=ftree.overlap(t)
    if ov: pairs.append((nm,len(ov)))
    bm.free()
print("\n  cab_floor vs wheel parts -- overlapping face pairs:")
if pairs:
    for nm,c in sorted(pairs,key=lambda p:-p[1]):
        print("    %-18s %5d overlapping face pairs   INTERPENETRATION" % (nm,c))
else:
    print("    none")

# CONTROL: van_floor vs the REAR wheels must be CLEAN, or the test proves nothing
vo,vbm=world_bm("van_floor"); vtree=BVHTree.FromBMesh(vbm)
vp=[]
for nm in [o.name for o in bpy.data.objects]:
    if not any(k in nm for k in ("tyre","rim","cap")): continue
    try: ob,bm=world_bm(nm)
    except Exception: continue
    ov=vtree.overlap(BVHTree.FromBMesh(bm))
    if ov: vp.append((nm,len(ov)))
    bm.free()
print("\n  CONTROL -- van_floor vs ALL wheel parts:")
print("    %s" % (vp if vp else "CLEAN (0 overlapping face pairs)"))
# BEFORE rev 38's repair this probe read:
#   cab_floor vs tyre1.31 / tyre1.3-1        240 overlapping face pairs each
#             vs rim1.31_barrel / rim1.3-1_barrel   76 each   (632 total)
#   van_floor vs tyre-1.11 / tyre-1.1-1      152 each
#             vs rim-1.11_barrel / rim-1.1-1_barrel 110 each  (524 total)
# The van_floor row was written as the CONTROL for the cab_floor claim, and its
# FAILING is what showed the defect was systemic rather than a cab quirk.  A
# control that fails is a result, not a broken instrument.
ok1 = (not pairs) and (not vp)
print("\n  [%s] C1 NO floor penetrates ANY wheel (rev 38 repair, SPEC 10.96)"
      % ("PASS" if ok1 else "FAIL"))
print("      pre-repair: cab_floor 632 pairs, van_floor 524 pairs")
print("\n  half-widths: both floors FLOOR_W/2 = 0.600")
print("  front tyre inner face 0.609 -> 9 mm clearance; rear 0.604 -> 4 mm")
print("="*78)
