"""probe_rev44_lampmove -- SPEC 10.24 item 3's TRAP, ARMED.  READ-ONLY.

    /tmp/blender/blender -b --python probe_rev44_lampmove.py

SPEC:7005 states the trap in capitals: **DO NOT MOVE THE ROUNDEL WITH THE
LAMPS.**  10.24's three findings were applied together once and reverted
together once, and the lesson from that revert is that they are NOT one change.
Rev 44 applied item 3 -- the lamps came down 97.0 mm -- so from here on the
trap needs a guard rather than a warning in prose (10.45: a claim in prose is
not a guard).

WHY IT IS MEASURED OFF THE BUILT MESH AND NOT OFF THE SOURCE.  Reading the
constants proves the LITERALS did not change; it does not prove no code path
links them.  This builds the scene and reads the objects' own world Z.

WHY IT IS NOT MEASURED OFF A RENDER.  Rev 44 tried, three times, and every
pixel detector it wrote was contaminated -- a "roundel" mask that returned red
from the whole frame, a brass mask that caught the indicator, and a difference
map that lit up 7.6 % of the frame because moving two chrome reflectors changes
the bounce light everywhere.  None of them could see what they claimed to.
sec.9's rule: CHECK WHAT YOUR DETECTOR CAN PHYSICALLY SEE.
"""
import sys, os
sys.argv = [sys.argv[0]]
os.environ.pop("T1_PREVIEW", None)
import bpy

src = open("build.py").read()
g = {"__name__": "__main__", "__file__": "build.py"}
exec(compile(src, "build.py", "exec"), g)

def zc(name):
    o = bpy.data.objects.get(name)
    if o is None:
        return None
    ws = [o.matrix_world @ v.co for v in o.data.vertices]
    return sum(w.z for w in ws) / len(ws)

print()
print("=" * 70)
print("probe_rev44_lampmove -- the lamps moved, the roundel did NOT")
print("=" * 70)

names = sorted(n for n in bpy.data.objects.keys()
               if n.startswith(("hl_lens", "hl_ring", "ind", "vw_", "roundel")))
print("  objects found: %s" % ", ".join(names[:12]))
lamp = next((n for n in names if n.startswith("hl_lens")), None)
rnd = next((n for n in names if n.startswith(("vw_", "roundel"))), None)
ind = next((n for n in names if n.startswith("ind")), None)
for nm, o in (("headlamp lens", lamp), ("roundel", rnd), ("indicator", ind)):
    print("  %-14s %-22s world z = %s"
          % (nm, o or "(not found)", ("%.4f" % zc(o)) if o else "--"))

CH, FA = 0, []
def ck(tag, ok, msg):
    global CH, FA
    CH += 1
    if not ok:
        FA.append(tag)
    print("  [%s] %s  %s" % ("PASS" if ok else "FAIL", tag, msg))

# The roundel's authored centre is ROUNDEL_Z, above ground ROUNDEL_Z_AG.  The
# built mesh is DROPPED, so its world centre is ROUNDEL_Z_AG.  That is the
# number the trap protects, and it is 1.0170 at rev 41 and at rev 44 alike.
RZ_AG = 1.0170
print()
print("CONTROLS")
zr, zl = zc(rnd) if rnd else None, zc(lamp) if lamp else None
ck("C1", zr is not None and abs(zr - RZ_AG) < 0.002,
   "THE TRAP: the roundel sits at its own %.4f, untouched by item 3 "
   "(measured %s)" % (RZ_AG, ("%.4f" % zr) if zr else "not found"))
ck("C2", zl is not None and zr is not None and zl < zr,
   "the headlamp is BELOW the roundel, as the photograph has it "
   "(lamp %s, roundel %s)"
   % (("%.4f" % zl) if zl else "?", ("%.4f" % zr) if zr else "?"))
# C3 IS AN INDEPENDENT ARM AGREEING AFTER THE FACT, and that is why it is
# worth a control.  The 97.0 mm came from the BELT chain alone.  The
# roundel-ratio chain -- which was never used to derive it -- wants a
# separation of 0.1758 +- 0.0185 m and gets 0.1695, i.e. 0.34 sigma.
ck("C3", zl is not None and zr is not None and abs((zr - zl) - 0.1695) < 0.004,
   "roundel-to-lamp separation is %s m.  BEFORE rev 44 it was 0.0725 and the "
   "photograph wants 0.1758 +- 0.0185 (0.628 +- 0.066 roundel diameters); the "
   "fix closed most of that on the BELT arm alone, without ever touching the "
   "roundel." % (("%.4f" % (zr - zl)) if (zr and zl) else "?"))
ck("C4", zl is not None and ind is not None
         and abs((zc(ind) - zl) - 0.2060) < 0.004,
   "the indicator still sits 0.206 m above the lamp -- it FOLLOWED the lamp "
   "down, which the re-typed literal 1.2360 would not have done (measured %s)"
   % (("%.4f" % (zc(ind) - zl)) if (ind and zl) else "?"))

print()
print("CONTROLS: %d checked, %d FAILED%s"
      % (CH, len(FA), ("  -- " + ",".join(FA)) if FA else ""))
print("EXPECTED: 4 checked, 0 FAILED.  ALL FOUR MUST STAY GREEN.")
sys.exit(1 if FA else 0)
