"""probe_rev44_nolita_nose -- the owner's rev-44 upload, measured.  READ-ONLY.

FRAME: ref_nolita_front34.jpg, 700x467, the front three-quarter he uploaded at
rev 44.  It is the first frame in this project carrying the WHOLE nose, both
headlamps, the VW roundel and people standing on the ground.

WHAT THIS PROBE CLAIMS, AND WHAT IT REFUSES TO.

  CLAIMED -- an ORDINAL, and it is a THIRD independent arm for SPEC 10.24
  item 3, which rev 44 applied earlier today: THE HEADLAMP SITS ENTIRELY IN THE
  RED, CLEAR BELOW THE TWO-TONE BREAK.  Sign only.  No px/m enters.

  REFUSED -- the MAGNITUDE.  Two reasons, both fatal and both stated before the
  numbers rather than after:
    1. THE LAMP IS LIT.  Its bloom swamps the chrome bezel's edges, so the
       lamp's outer diameter -- the natural denominator -- cannot be measured.
       The bright core spans 34 px vertically against 28 horizontally on a part
       that is circular, which is the bloom, not the lamp.
    2. IT IS THE NOLITA LIVERY AND THE BREAK IS PAINT.  SPEC 7.1, settled with
       the owner this revision: geometry crosses livery states, livery does
       not.  The bus was repainted between Playa and Nolita.  Whether the
       Nolita paint follows the PRESSED SWAGE -- which would make it geometry
       and admissible -- IS NOT KNOWN AND IS NOW AN OWNER QUESTION.

A DETECTOR FAILURE OF MY OWN, RECORDED BECAUSE IT IS THE FIFTH THIS REVISION.
The first cut looked for "the lowest cream pixel above the lamp" and returned
y=270 for a break that is at y=228 -- because the LAMP'S OWN CHROME BEZEL is
bright and desaturated and passes any cream test.  It reported a 1 px gap where
there are 38.  sec.9: CHECK WHAT YOUR DETECTOR CAN PHYSICALLY SEE.  The fix is
to read the column profile rather than a mask.
"""
import sys
import numpy as np
from PIL import Image

F = "ref_nolita_front34.jpg"
a = np.asarray(Image.open(F).convert("RGB")).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
red = (R > G + 45) & (R > B + 45) & (R > 90)
sat = (a.max(2) - a.min(2)) / np.maximum(a.max(2), 1)
crm = (a.max(2) > 200) & (sat < 0.10)          # the cream panel: bright, FLAT

print("=" * 72)
print("probe_rev44_nolita_nose -- %s  %dx%d" % (F, W, H))
print("=" * 72)

def profile(x):
    """walk DOWN the column and return the cream->red transition, then the
    first neutral run below it (the bezel)."""
    brk = bez = None
    for y in range(120, H - 1):
        if brk is None and crm[y, x] and red[y + 1:y + 4, x].all():
            brk = y
        elif brk is not None and y > brk + 8 and sat[y, x] < 0.30 \
                and a[y, x].max() > 150 and not red[y, x]:
            bez = y
            break
    return brk, bez

print()
print("  col   break y   bezel-top y   clear red between")
rows = []
for x in range(248, 273, 4):
    b, z = profile(x)
    if b and z:
        rows.append((x, b, z, z - b))
        print("  %3d     %3d       %3d            %3d px" % (x, b, z, z - b))
gap = float(np.median([r[3] for r in rows])) if rows else -1
brk_y = float(np.median([r[1] for r in rows])) if rows else -1

# the lit core, for scale ONLY as a stated-unreliable denominator
core = (R > 215) & (G > 170) & (B < 190) & (R - B > 40)
ys, xs = np.nonzero(core[250:330, 240:280])
cd = ys.ptp() + 1 if len(ys) else -1
print()
print("  median break y = %.0f ;  median clear red = %.0f px" % (brk_y, gap))
print("  lit CORE vertical extent = %d px  (NOT the lamp diameter -- bloom)" % cd)

CH, FA = 0, []
def ck(tag, ok, msg):
    global CH, FA
    CH += 1
    if not ok:
        FA.append(tag)
    print("  [%s] %s  %s" % ("PASS" if ok else "FAIL", tag, msg))

print()
print("CONTROLS")
ck("C1", len(rows) >= 5,
   "the cream->red transition resolves on %d of 7 sampled columns" % len(rows))
ck("C2", gap > 15,
   "THE ORDINAL: %.0f px of CLEAR RED between the break and the top of the "
   "lamp assembly.  The headlamp sits entirely in the red -- a THIRD "
   "independent arm agreeing with SPEC 10.24 item 3, applied earlier this "
   "revision." % gap)
ck("C3", gap > cd * 0.5,
   "and the gap is not marginal: %.0f px against a %d px lit core, so it is "
   "comparable to the whole visible lamp.  Sign is not in doubt." % (gap, cd))
# C4 -- KILL.  This probe must NOT be read as a magnitude.
ck("C4", False,
   "KILL, WRITTEN TO FAIL: this frame must NEVER be quoted for a MAGNITUDE.  "
   "The lamp is LIT (bloom eats the bezel) and the break is PAINT in a livery "
   "state the vehicle was repainted into (SPEC 7.1).  EXIT CODE 1 IS THE "
   "INTENDED RESULT HERE.")

print()
print("CONTROLS: %d checked, %d FAILED%s"
      % (CH, len(FA), ("  -- " + ",".join(FA)) if FA else ""))
print("EXPECTED: 4 checked, 1 FAILED -- C4 is a KILL and must never go green.")
print()
print("OWNER QUESTION RAISED BY THIS FRAME: does the Nolita paint line follow")
print("the nose's PRESSED CREASE?  If it does, the break is GEOMETRY and this")
print("frame's magnitude becomes admissible -- and it wants the lamp lower")
print("still than rev 44 put it.  If the painter ignored the crease, it never")
print("will be.  Nothing in the pixels can settle that at 700 px.")
sys.exit(1 if FA else 0)
