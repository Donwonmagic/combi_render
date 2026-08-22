"""
probe_rev54_reach.py -- rev 54.  DO THE SIX STROKE ENDS REACH THE RING BAND?

FIRST VERSION WAS WRONG AND IS REPLACED, NOT PATCHED.  It bucketed glyph
vertices into six HAND-CHOSEN angular sectors and returned 0.8394 for the W's
left arm tip and 0.5537 for its mirror.  A glyph that is symmetric by
construction cannot do that, so the sectors were the defect.  Rule 8: a
measurement's window is part of the measurement, and I had guessed it.

This version lets the DATA place the terminals: it builds a 720-ray angular
reach profile (max glyph radius per 0.5 deg), finds its local maxima, and
reports those.  Six peaks are expected and the count is printed, not assumed.
The profile and the ring's own measured band are PAINTED so the window can be
looked at before it produces a number.
"""
import bpy, os, sys, math
import numpy as np
from PIL import Image, ImageDraw
ROOT = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, ROOT)
OUTD = os.path.join(ROOT, "probe_scratch")
src = open(os.path.join(ROOT, "build.py")).read().split('if os.environ.get("T1_SAVE")')[0]
exec(compile(src, "build.py", "exec"))
import mathutils
P = print

def proj(objs, U, V):
    out = []
    for o in objs:
        M = o.matrix_world
        for v in o.data.vertices:
            p = M @ v.co
            out.append((U[0]*p.x+U[1]*p.y+U[2]*p.z, V[0]*p.x+V[1]*p.y+V[2]*p.z))
    return out

def analyse(tag, glyph, ring, U, V, NR=720):
    rp = proj(ring, U, V); gp = proj(glyph, U, V)
    cu = 0.5*(min(p[0] for p in rp)+max(p[0] for p in rp))
    cw = 0.5*(min(p[1] for p in rp)+max(p[1] for p in rp))
    rr = [math.hypot(u-cu, w-cw) for u, w in rp]
    RO, RI = max(rr), min(rr)
    P("\n=== %s ===" % tag)
    P("  ring outer R %.6f m   inner R %.6f m   band %.4f of outer"
      % (RO, RI, (RO-RI)/RO))
    prof = np.zeros(NR)
    for u, w in gp:
        du, dw = u-cu, w-cw
        a = int((math.degrees(math.atan2(dw, du)) % 360) / 360.0 * NR) % NR
        prof[a] = max(prof[a], math.hypot(du, dw)/RO)
    # peaks: strict local maxima of the filled profile, min separation 20 deg
    f = prof.copy()
    for i in range(NR):                       # fill empty rays from neighbours
        if f[i] == 0:
            f[i] = max(f[(i-1) % NR], f[(i+1) % NR])
    idx = [i for i in range(NR)
           if f[i] >= f[(i-1) % NR] and f[i] >= f[(i+1) % NR] and f[i] > 0.3]
    peaks = []
    for i in sorted(idx, key=lambda k: -f[k]):
        if all(min(abs(i-j), NR-abs(i-j)) > NR*20/360 for j in peaks):
            peaks.append(i)
    peaks.sort()
    P("  angular reach profile: %d local maxima found (six stroke ends expected)"
      % len(peaks))
    band = RI/RO
    P("  %-10s %10s %10s   %s" % ("angle deg", "reach", "band at", "verdict"))
    for i in peaks:
        m = f[i]
        v = "IN THE BAND" if m >= band - 1e-4 else "SHORT by %5.1f mm" % ((RI-m*RO)*1000)
        P("  %-10.1f %10.4f %10.4f   %s" % (i*360.0/NR, m, band, v))
    # PAINT IT
    PX = 900; S = PX/(2*RO*1.12)
    img = Image.new("RGB", (PX, PX), (0, 0, 0)); dr = ImageDraw.Draw(img)
    def xy(u, w): return ((u-cu)*S + PX/2, PX/2 - (w-cw)*S)
    for o in ring:
        M = o.matrix_world
        for p in o.data.polygons:
            vs = [M @ o.data.vertices[i].co for i in p.vertices]
            dr.polygon([xy(U[0]*q.x+U[1]*q.y+U[2]*q.z, V[0]*q.x+V[1]*q.y+V[2]*q.z)
                        for q in vs], fill=(90, 90, 110))
    for o in glyph:
        M = o.matrix_world
        for p in o.data.polygons:
            vs = [M @ o.data.vertices[i].co for i in p.vertices]
            dr.polygon([xy(U[0]*q.x+U[1]*q.y+U[2]*q.z, V[0]*q.x+V[1]*q.y+V[2]*q.z)
                        for q in vs], fill=(235, 235, 235))
    for R, col in ((RO, (255, 0, 0)), (RI, (255, 180, 0))):
        dr.ellipse([PX/2-R*S, PX/2-R*S, PX/2+R*S, PX/2+R*S], outline=col, width=2)
    for i in peaks:
        a = math.radians(i*360.0/NR); m = f[i]*RO
        dr.line([PX/2, PX/2, PX/2+m*S*math.cos(a), PX/2-m*S*math.sin(a)],
                fill=(0, 220, 255), width=2)
    img.save(os.path.join(OUTD, "rev54_reach_%s.png" % tag))
    P("  painted -> probe_scratch/rev54_reach_%s.png" % tag)
    P("     red = ring OUTER, amber = ring INNER (band edge), cyan = each peak's reach")
    return peaks, f, band

analyse("nose", [o for o in bpy.data.objects if o.name.startswith("vwbar")],
        [o for o in bpy.data.objects if o.name.startswith("vw_ring")], (0,1,0), (0,0,1))
_r = [o for o in bpy.data.objects if o.name.startswith("capring")][0]
rc = sum((_r.matrix_world @ v.co for v in _r.data.vertices), mathutils.Vector((0,0,0)))/len(_r.data.vertices)
_g = [o for o in bpy.data.objects if o.name.startswith("capvw")
      and ((sum((o.matrix_world @ v.co for v in o.data.vertices), mathutils.Vector((0,0,0)))/len(o.data.vertices))-rc).length < 0.15]
analyse("hubcap", _g, [_r], (1,0,0), (0,0,1))
