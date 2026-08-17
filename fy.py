import bpy,os,sys,math
try: ROOT=os.path.dirname(os.path.abspath(__file__))
except NameError: ROOT=os.getcwd()
sys.path.insert(0,ROOT)
_src=open(os.path.join(ROOT,"build.py")).read().split('if os.environ.get("T1_SAVE")')[0]
exec(compile(_src,"build.py","exec"))
import t1_core as T, t1_shell as S
import t1_detail as D
print("\n"+"="*70)
print("  flank_y around each arch rim (radius ARCH_R about the axle centre)")
print("  The liner's outboard face must sit INSIDE the smallest of these,")
print("  or it stands proud of the skin where the flank tucks in.")
print("="*70)
for xa in (T.X_AXLE_F, T.X_AXLE_R):
    zc = S.arch_z(xa)
    vals=[]
    for deg in range(-10, 191, 5):
        a=math.radians(deg)
        x = xa + S.ARCH_R*math.cos(a); z = zc + S.ARCH_R*math.sin(a)
        try: vals.append((deg, T.flank_y(x, z)))
        except Exception: pass
    lo=min(vals,key=lambda p:p[1])
    print("  axle x=%+.3f  zc=%.4f   min flank_y %.4f at %d deg   max %.4f"
          % (xa, zc, lo[1], lo[0], max(v for _,v in vals)))
    print("     %s" % "  ".join("%d:%.3f"%(d,v) for d,v in vals[::4]))
print("\n  current WH_Y_OUT = %.3f   WH_SWEEP = %.1f deg" % (D.WH_Y_OUT, D.WH_SWEEP))
print("="*70)
