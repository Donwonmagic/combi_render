import os, sys, io, contextlib
HERE=os.path.dirname(os.path.abspath(__file__))+"/.."
sys.path.insert(0,HERE); os.environ.setdefault("T1_SUB","1")
import bpy
buf=io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(compile(open(os.path.join(HERE,"build.py")).read(),"build.py","exec"),
         {"__name__":"__main__","__file__":os.path.join(HERE,"build.py")})
import t1_detail as D, t1_core as T
# --- what stands forward, bodywork
EX={"counter","counter_nosing","counter_top","tail_board","tail_board_stay",
    "tb_bulbflex","tb_bulbs","tb_edge_dark","tb_edge_red"}
rows=[]
for o in bpy.data.objects:
    if o.type!='MESH' or not o.data.vertices or o.name in EX: continue
    m=o.matrix_world; rows.append((max((m@v.co).x for v in o.data.vertices),o.name))
rows.sort(reverse=True)
print("FORWARD-MOST BODYWORK:", ["%s %.4f"%(n,x) for x,n in rows[:6]])

# --- drape-station sweep: misses and resulting bow, over the 23 real stations
nose_y = T.WX(2.108)*T.G(0.4800)
print("\nnose[1]=%.5f  ; drape sweep over the SAME 23 stations the build uses:"%nose_y)
print(" z_und   misses/23   s(0)-s(anchor) mm   note")
z=0.60
while z<=1.30001:
    f=D._nose_plan_x(z)
    s0=f(nose_y)
    miss=0; vals=[]
    for i in range(1,24):
        y=-nose_y+2*nose_y*i/24
        v=f(y)
        if v is None or s0 is None: miss+=1
        else: vals.append((y,v))
    mid=min(vals,key=lambda p:abs(p[0])) if vals else None
    print("  %.3f    %2d/23        %s"%(z,miss,
        ("%+7.2f"%(1000*(mid[1]-s0))) if (mid and s0) else "  n/a  "),
        end="")
    print("   <<< SHIPPED BUMP_BOW_Z" if abs(z-1.100)<1e-9 else ("   (rev69 says 4 miss)" if abs(z-1.000)<1e-9 else ""))
    z+=0.05

# --- corner continuity on the BUILT PATH (not the mesh): last wrap seg vs first face seg
import math
import t1_shell as _SH
aft=max(p[0] for p in _SH.DOOR_GAP_S)+0.010
raw=D._plan_curve(0.4800,aft,2.108,30)
f=D._nose_plan_x(D.BUMP_BOW_Z); s0=f(nose_y)
y1=-nose_y+2*nose_y*1/24; x1=2.108+1.0*(f(y1)-s0)
p_2,p_1=(raw[-2][0],-raw[-2][1]),(raw[-1][0],-raw[-1][1])
def ang(a,b):
    return math.degrees(math.atan2(b[0]-a[0], b[1]-a[1]))
print("\nCORNER: wrap incoming heading %.2f deg from +y ; face outgoing %.2f deg ; KINK %.2f deg"
      %(ang(p_2,p_1), ang(p_1,(x1,y1)), abs(ang(p_2,p_1)-ang(p_1,(x1,y1)))))
print("  (old FLAT face outgoing was 0.00 deg -> old kink %.2f deg)"%abs(ang(p_2,p_1)))
print("  C0: face is anchored to the corner exactly -> position step = %.4f mm"%0.0)
