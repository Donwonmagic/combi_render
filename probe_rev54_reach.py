"""
probe_rev54_reach.py -- rev 54.  DO THE SIX STROKE ENDS ACTUALLY REACH THE RING?

t1_core sec."EVERY STROKE END ON THE RING" says a rev-44b fixed-point solver
puts all six terminals on the band circle.  The rev-54 hero render shows the
NOSE roundel's two V arms stopping visibly short.  One of those is wrong.

Measured off the BUILT mesh: every glyph vertex's radius as a fraction of its
own ring's OUTER radius, bucketed by angle, against the ring's own measured
inner and outer radii.  Nothing is read from a constant.
"""
import bpy, os, sys, math
import numpy as np
ROOT = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, ROOT)
src = open(os.path.join(ROOT, "build.py")).read().split('if os.environ.get("T1_SAVE")')[0]
exec(compile(src, "build.py", "exec"))
P = print

def ring_radii(objs, U, V):
    vs = []
    for o in objs:
        M = o.matrix_world
        vs += [M @ v.co for v in o.data.vertices]
    u = np.array([U[0]*p.x+U[1]*p.y+U[2]*p.z for p in vs])
    w = np.array([V[0]*p.x+V[1]*p.y+V[2]*p.z for p in vs])
    cu, cw = 0.5*(u.min()+u.max()), 0.5*(w.min()+w.max())
    r = np.hypot(u-cu, w-cw)
    return cu, cw, r.max(), r.min()

def reach(tag, glyph_objs, ring_objs, U, V):
    cu, cw, ro, ri = ring_radii(ring_objs, U, V)
    P("\n%s" % tag)
    P("  ring outer R %.6f   inner R %.6f   band = %.4f of outer"
      % (ro, ri, (ro-ri)/ro))
    pts = []
    for o in glyph_objs:
        M = o.matrix_world
        for v in o.data.vertices:
            p = M @ v.co
            x = U[0]*p.x+U[1]*p.y+U[2]*p.z - cu
            y = V[0]*p.x+V[1]*p.y+V[2]*p.z - cw
            pts.append((math.hypot(x, y)/ro, math.degrees(math.atan2(y, x)) % 360))
    P("  glyph max reach overall: %.4f of ring outer R" % max(p[0] for p in pts))
    P("  %-26s %10s %10s" % ("angular sector", "max reach", "verdict"))
    SEC = [("V left arm tip", 120, 175), ("V right arm tip", 5, 60),
           ("W left arm tip", 175, 230), ("W right arm tip", 310, 355),
           ("W left leg", 230, 265), ("W right leg", 275, 310)]
    for nm, a0, a1 in SEC:
        sel = [r for r, a in pts if a0 <= a <= a1]
        if not sel:
            P("  %-26s %10s" % (nm, "(none)")); continue
        m = max(sel)
        v = "IN THE BAND" if m >= ri/ro - 1e-4 else "SHORT by %.1f mm" % ((ri-m*ro)*1000)
        P("  %-26s %10.4f %10s" % (nm, m, v))

reach("NOSE roundel",
      [o for o in bpy.data.objects if o.name.startswith("vwbar")],
      [o for o in bpy.data.objects if o.name.startswith("vw_ring")],
      (0,1,0), (0,0,1))
_r = [o for o in bpy.data.objects if o.name.startswith("capring")][0]
import mathutils
rc = sum((o.matrix_world @ v.co for v in _r.data.vertices),
         mathutils.Vector((0,0,0))) / len(_r.data.vertices)
_g = [o for o in bpy.data.objects if o.name.startswith("capvw")
      and ((sum((o.matrix_world @ v.co for v in o.data.vertices),
                mathutils.Vector((0,0,0)))/len(o.data.vertices)) - rc).length < 0.15]
reach("HUBCAP badge (one wheel)", _g, [_r], (1,0,0), (0,0,1))
