"""rev49 -- grade EVERY CLAUSE of the brief's sentence about t1_shell.signboard().

  "signboard() will NOT do it -- wrong hinge axis (fore-aft, needs lateral),
   wrong extent (stops 93 mm short of X_TAIL), wrong presentation, and it was
   written for a different board in a different frame."

Static: no Blender.  Re-implements what signboard() would emit from the source's
own constants and the same trig `_hinge()` uses.
"""
import math, re
src = open('t1_shell.py').read()
def const(n):
    m = re.search(r"^%s\s*=\s*([-0-9.]+)"%n, src, re.M)
    if m: return float(m.group(1))
    m = re.search(r"^([A-Z0-9_,\s]*\b%s\b[A-Z0-9_,\s]*)=\s*(.+)$"%n, src, re.M)
    names=[s.strip() for s in m.group(1).split(',')]; vals=[s.strip() for s in m.group(2).split('#')[0].split(',')]
    return float(vals[names.index(n)])
SIGN_X0,SIGN_X1 = const("SIGN_X0"),const("SIGN_X1")
LID_W,LID_Y_HINGE,LID_PROUD,LID_T = const("LID_W"),const("LID_Y_HINGE"),const("LID_PROUD"),const("LID_T")
SIGN_OPEN_DEG = const("SIGN_OPEN_DEG"); LID_OPEN_DEG = const("LID_OPEN_DEG")
LID_X0,LID_X1 = const("LID_X0"),const("LID_X1")
X_TAIL = -1.8727
RIDE_DROP = 0.0650
ZH = 1.9835 + LID_PROUD          # roof baseline at the tail run + LID_PROUD

MEAS = dict(base_x=X_TAIL+0.151, base_z=1.747, tip_x=X_TAIL-0.408, tip_z=2.184,
            chord=0.711, tilt_h=38.0)

print(__doc__)
print("SOURCE CONSTANTS  SIGN_X0 %.4f  SIGN_X1 %.4f  SIGN_OPEN_DEG %.1f  LID_W %.4f"
      "  LID_Y_HINGE %.4f"%(SIGN_X0,SIGN_X1,SIGN_OPEN_DEG,LID_W,LID_Y_HINGE))
w = LID_W*0.86
a = math.radians(SIGN_OPEN_DEG)
print("                  panel width across (LID_W*0.86) = %.4f m"%w)
print()
print("CLAUSE 1  'wrong hinge axis (fore-aft, needs lateral)'")
print("  t1_shell.py:1797  signboard() calls _hinge(panel, 0.0, LID_Y_HINGE, zh, SIGN_OPEN_DEG)")
print("  t1_shell.py:1201  def _hinge(...):  '''Rotate a lid about its FORE-AFT hinge axis'''")
print("                    body moves v.co.y and v.co.z ONLY; x is untouched.")
print("  t1_shell.py:1302  _hinge_y() is the LATERAL sibling -- used by the trunk lid, NOT here.")
print("  --> the panel rotates about a line parallel to +X at y=%.3f.  VERDICT: TRUE."%LID_Y_HINGE)
print()
print("CLAUSE 2  'wrong extent (stops 93 mm short of X_TAIL)'")
print("  SIGN_X1 = %.4f ;  X_TAIL = %.4f ;  gap = %.1f mm."%(SIGN_X1,X_TAIL,(SIGN_X1-X_TAIL)*1000))
print("  build.py step 8b shears in Z only (it does not move x), and signboard() is NOT")
print("  passed through t1_core._aft(), so -1.7800 is also the BUILT station.")
print("  --> 92.7 mm, quoted as 93.  VERDICT: TRUE, and it UNDERSTATES the miss:")
print("      the measured board runs X_TAIL+0.151 -> X_TAIL-0.408.  signboard() spans")
print("      X_TAIL+0.733 -> X_TAIL+0.093.  OVERLAP WITH THE MEASURED BOARD: %.3f m of"%
      max(0.0, min(SIGN_X0,MEAS['base_x'])-max(SIGN_X1,MEAS['tip_x'])))
print("      its 0.559 m fore-aft run -- and NONE of the 0.501 m that lies aft of SIGN_X1.")
print()
print("CLAUSE 3  'wrong presentation'")
top = ZH + w*math.sin(a) - RIDE_DROP
print("  signboard() stands the panel %.1f deg from HORIZONTAL about a fore-aft axis:"%SIGN_OPEN_DEG)
print("     hinge z ~ %.3f (roof + LID_PROUD - RIDE_DROP), free edge ~ z %.3f, i.e. it rises"
      %(ZH-RIDE_DROP, top))
print("     %.3f m above the roof and leans %.1f deg PAST vertical toward the show side."
      %(w*math.sin(a), 0.0 if SIGN_OPEN_DEG<=90 else SIGN_OPEN_DEG-90))
print("  the MEASURED board lies %.1f deg from horizontal about a LATERAL axis, rises only"%MEAS['tilt_h'])
print("     %.3f m, and its tip is at z %.3f -- %.2f m BELOW signboard()'s free edge."
      %(MEAS['tip_z']-MEAS['base_z'],MEAS['tip_z'],top-MEAS['tip_z']))
print("  signboard() carries `lidsign` (LA SANTA red brush script + star, build.py:328).")
print("  It emits NO bulb string; the measured board is bulb-lined along its lower edge.")
print("  --> VERDICT: TRUE.")
print()
print("CLAUSE 4  'written for a different board in a different frame'")
print("  signboard().__doc__: 'Shown a 3x crop of this panel in ref_rear34.jpg ... a separate")
print("  signboard, not a cut roof lid', then retired by the owner as 'a detached sign' that")
print("  'happens to fall behind the combi in ref_rear34.jpg' (SPEC 10.28, re-affirmed 10.49,")
print("  re-affirmed AGAIN in SPEC 10.122.5).  That is the 'La Santa' cream + red-script board")
print("  standing at u 570-860 in ref_rear34.jpg -- a DIFFERENT OBJECT from the raised board.")
print("  --> 'different BOARD': TRUE.   'different FRAME': MISLEADING -- ref_rear34.jpg is not")
print("      a different frame from where the raised board is claimed; both boards are claimed")
print("      in it.  What separates them is that they are different objects, and one of them")
print("      is not on the vehicle at all.")
print()
print("AND THE CLAUSE THE BRIEF DOES NOT MAKE, WHICH IS THE DECISIVE ONE:")
print("  t1_shell.py:1790  if not int(os.environ.get('T1_SIGNBOARD','0')): return [],[],[]")
print("  verify_clone.sh:312 asserts that default stays OFF.  So signboard() emits NOTHING in")
print("  any shipped build: there is no 'you already built it' here even by accident.")
