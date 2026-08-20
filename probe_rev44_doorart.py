"""probe_rev44_doorart -- ITEM 1 / SPEC 10.100: WHAT ACTUALLY MAPS THE DOOR
ART'S v-COORDINATE, and why the owner's answer cannot be reached by moving
DOOR_H or by re-pointing one parse.  READ-ONLY.  bpy only because t1_shell
imports it.

THE OWNER'S ANSWER, GIVEN REV 44: the art KEEPS ITS DRAWN SCALE and EXTENDS
further down to reach the door's bottom edge.  It does NOT stretch.

FOUR THINGS THE RECORD HAS WRONG, all checkable here.

1. `DOOR_H` DOES NOT DIVIDE ANYTHING, AND IT DOES NOT MAP THE ART'S v AT ALL.
   It has exactly TWO read sites, folk_gen.py:1274 and :1287, both
   `h = sv * DOOR_H` -- a MULTIPLIER turning a normalised motif height into
   metres for TWO motifs (EDGE_E's latch sliver, DARK_1).  SPEC 10.100.6 AND
   t1_shell.py:546 both say it "divides every v-coordinate of the door art".
   Both are wrong; the code is right.  The rev-44 brief caught the SPEC one and
   called it a multiplier -- correct -- but missed that the same sentence sits
   in the code, and missed that DOOR_H is not the v-map either way.

2. THE v-MAP IS `door_pv`, AND IT ALREADY DRIVES OFF THE DOOR'S OWN OUTLINE
   PER STATION:  z = (belt_z(x) - panel_bot(x)) * (v-BELT_V)/(1-BELT_V), and
   panel_bot(x) == door_bot_z(x) inside the door span.  So "drive the art's
   extent from the door's own outline, z_bot(x)" is ALREADY WHAT HAPPENS.
   Nothing needs building for that.

3. AND THAT IS THE PROBLEM.  `door_pv` is PROPORTIONAL -- it normalises over
   the panel height -- so deepening the panel SCALES every motif.  The obvious
   one-line fix, re-pointing the art's outline at the wrapped outline, delivers
   a STRETCH: precisely the option the owner did NOT choose.  The lever the
   record is looking for does not exist yet.

4. THE ADDED DEPTH IS NOT A UNIFORM DEEPENING AND NO SCALAR CAN DESCRIBE IT.
   SPEC 10.100.4's own z_bot reproduces here to 0.1 mm: 272.2 mm at the rear
   corner, 387.5 mm at the front -- but only 1.8 mm over the front wheel arch,
   because the new bottom is an ARC that rises to z 0.8033 at the crown.  The
   brief says a scalar DOOR_H "is right at one corner and 115 mm wrong at the
   other".  It is worse than that: it is ~270-390 mm wrong at the corners and
   ~2 mm wrong in the middle.  What the art must gain is TWO LOBES at the
   corners, not a band across the bottom.

THE SPLIT THAT CAUSES ALL OF THIS: the art is framed on `DOOR_GAP` (17 pts,
rev 41's, held bit-identical as the ART DATUM) while the shell is cut by
`DOOR_GAP_S` / `DOOR_BOT_RUN` (the wrapped outline).

ESTIMATOR NOTE, because a first cut of this probe got it wrong and published
252/380 mm.  `DOOR_GAP_S` is the WHOLE door perimeter -- top rail, bottom rail
and both vertical edges -- so "lowest z near x" picks up the VERTICAL EDGES at
the corners and returns a number that is neither outline.  The bottom rail is
`t1_shell.DOOR_BOT_RUN` (61 pts) and that is what is used here.  Those wrong
figures are recorded rather than quietly replaced (sec.9 of the rev-44 brief).
"""
import ast, re, sys
import numpy as np
import folk_gen as F
import t1_shell as S

print("=" * 72)
print("probe_rev44_doorart -- the door art's v-map, and the owner's answer")
print("=" * 72)

# ------------------------------------------------- 1. DOOR_H's real read sites
src = open("folk_gen.py").read()
lines = src.splitlines()
sites = sorted({n.lineno for n in ast.walk(ast.parse(src))
                if isinstance(n, ast.Name) and n.id == "DOOR_H"
                and isinstance(n.ctx, ast.Load)})
print()
print("1. DOOR_H's READ SITES IN folk_gen.py")
for ln in sites:
    print("     :%-5d %s" % (ln, lines[ln - 1].strip()))
mult = all("* DOOR_H" in lines[ln - 1] for ln in sites)
print("   every read site MULTIPLIES: %s        DOOR_H = %.6f m"
      % (mult, F.DOOR_H))
# NB: must be matched ACROSS lines and anchored to DOOR_H itself.  A first cut
# keyed on "divides every" + "DOOR_H" anywhere on the line and false-positived
# on SPEC.md:3254, where the phrase belongs to DOOR_W.
_PAT = re.compile(r"DOOR_H`?[^.]{0,60}?divides every\s+v-coordinate")
prose = []
for fn in ("SPEC.md", "t1_shell.py", "folk_gen.py"):
    txt = open(fn).read()
    for m in _PAT.finditer(txt):
        prose.append((fn, txt[:m.start()].count("\n") + 1))
print("   prose still saying 'divides every v-coordinate': %s"
      % (", ".join("%s:%d" % p for p in prose) or "none"))

# ------------------------------------------ 2. the v-map, and its shape
print()
print("2. THE v-MAP IS door_pv, AND IT IS PROPORTIONAL")
print("     z = (belt_z(x) - panel_bot(x)) * (v - BELT_V)/(1 - BELT_V),"
      "  BELT_V = %.4f" % F.BELT_V)

_r = sorted(S.DOOR_BOT_RUN)
_rx = np.array([p[0] for p in _r]); _rz = np.array([p[1] for p in _r])
def new_bot(x):
    """SPEC 10.100.4's z_bot, in the art's DROPPED frame."""
    return float(np.interp(x, _rx, _rz)) - F.rake_drop(x)

X_CROWN = 1.36
STATIONS = (("rear corner  (DOOR_X0)", F.DOOR_X0),
            ("arch crown            ", X_CROWN),
            ("front corner (DOOR_X1)", F.DOOR_X1))
print()
print("3. THE ART OUTLINE vs THE OUTLINE THAT ACTUALLY CUTS")
print("     art datum  DOOR_GAP     %3d pts (rev 41's, bit-identical)"
      % len(S.DOOR_GAP))
print("     bottom run DOOR_BOT_RUN %3d pts (SPEC 10.100.4's z_bot)"
      % len(S.DOOR_BOT_RUN))
dep = {}
for nm, x in STATIONS:
    a, g = F.panel_bot(x), new_bot(x)
    dep[nm] = (a - g) * 1000.0
    print("     %s x=%.4f : art %.4f  new %.4f  DEEPER BY %6.1f mm"
          % (nm, x, a, g, dep[nm]))
print("     -> the added depth is TWO CORNER LOBES, not a band: %.1f mm and"
      % dep["rear corner  (DOOR_X0)"])
print("        %.1f mm at the corners against %.1f mm over the arch crown."
      % (dep["front corner (DOOR_X1)"], dep["arch crown            "]))

print()
print("4. WHAT THE ONE-LINE RE-POINT WOULD DO -- IT STRETCHES")
for nm, x in STATIONS:
    h0 = F.belt_z(x) - F.panel_bot(x)
    h1 = F.belt_z(x) - new_bot(x)
    print("     %s : panel height %.4f -> %.4f  = x%.4f (%+.1f %% on every "
          "motif at this station)" % (nm, h0, h1, h1 / h0, (h1 / h0 - 1) * 100))
print()
print("   >>> AND THE STRETCH IS NOT EVEN UNIFORM ALONG THE DOOR, so a re-point")
print("       does not merely scale the art -- it SHEARS it, hardest at the")
print("       corners and not at all over the arch.")
print()
print("   >>> SUPERSEDED rev 44, SPEC 10.102 -- THE WRAP IS RETRACTED, so the")
print("       two corner lobes below do not exist and there is nothing to draw.")
print("       The paragraph is LEFT PRINTING as a dated record of the rev-43")
print("       state; the depths above now read 0.0 mm, which is the retraction")
print("       showing through the instrument rather than being asserted at it.")
print()
print("   >>> [rev 43] THE OWNER CHOSE 'EXTEND AT DRAWN SCALE'.  door_pv must become")
print("       BELT-ANCHORED AND METRIC, and the inventory must GROW to fill")
print("       two corner lobes.  That is a drawing job, not a constant change")
print("       and not a re-point.")
print()

CH, FA = 0, []
def ck(tag, ok, msg, kill=False):
    global CH, FA
    CH += 1
    if not ok:
        FA.append(tag)
    print("  [%s] %s%s  %s" % ("PASS" if ok else "FAIL", tag,
                               " (KILL)" if kill else "", msg))

print("CONTROLS")
ck("C1", mult and len(sites) == 2,
   "DOOR_H has exactly 2 read sites and both MULTIPLY (found %d)" % len(sites))
ck("C2", abs(F.DOOR_H - 1.013467) < 5e-7,
   "DOOR_H reproduces its published 1.013467 m (%.6f)" % F.DOOR_H)
# C3 and C4 -- RED BY DESIGN FROM REV 44.  They reproduce SPEC 10.100.4's
# published corner depths and crown height, and SPEC 10.102 RETRACTED the shape
# those figures describe: the cab door does not wrap the front wheel arch, and
# rev 41's flat chord is restored.  They are LEFT ARMED AND LEFT FAILING rather
# than deleted or re-pointed at the new numbers.  A retraction that quietly
# re-points its own instrument is not a retraction -- and if anything ever
# re-introduces the wrap, these two go GREEN and say so in one line.
ck("C3", abs(dep["rear corner  (DOOR_X0)"] - 272.2) < 0.2
       and abs(dep["front corner (DOOR_X1)"] - 387.5) < 0.2,
   "RED BY DESIGN (SPEC 10.102): reproduces the RETRACTED 10.100.4 depths "
   "272.2 / 387.5 mm.  Reads %.1f / %.1f mm.  FAIL IS THE INTENDED RESULT."
   % (dep["rear corner  (DOOR_X0)"], dep["front corner (DOOR_X1)"]))
ck("C4", abs(max(p[1] for p in S.DOOR_BOT_RUN) - 0.8033) < 5e-4,
   "RED BY DESIGN (SPEC 10.102): reproduces the RETRACTED 10.100.4 crown "
   "height 0.8033.  Reads %.4f.  FAIL IS THE INTENDED RESULT."
   % max(p[1] for p in S.DOOR_BOT_RUN))
# C5 -- THE FINDING, armed as a KILL.  If door_pv were belt-anchored and
# metric, re-pointing the outline would leave a given v at the SAME depth below
# the belt.  It does not, and the difference IS the unwanted stretch.
V = 0.90
def depth(x, bot):
    return (F.belt_z(x) - bot(x)) * (V - F.BELT_V) / (1 - F.BELT_V)
d_now = depth(F.DOOR_X1, F.panel_bot)
d_new = depth(F.DOOR_X1, new_bot)
print("       (v=%.2f at the front corner: %.1f mm below the belt now, "
      "%.1f mm after a re-point)" % (V, d_now * 1000, d_new * 1000))
ck("C5", abs(d_now - d_new) < 1e-4,
   "KILL: a re-point must NOT move a fixed v, or the map is a STRETCH. "
   "It moves it %.1f mm. EXIT CODE 1 IS THE INTENDED RESULT HERE -- it is "
   "the finding." % ((d_new - d_now) * 1000), kill=True)
ck("C6", all(d > 0 for d in dep.values()),
   "the cut outline is BELOW the art outline at every station measured")

print()
print("CONTROLS: %d checked, %d FAILED%s"
      % (CH, len(FA), ("  -- " + ",".join(FA)) if FA else ""))
print("EXPECTED, rev 42-43: 6 checked, 1 FAILED (C5, the finding, a KILL).")
print("EXPECTED, rev 44 on: 6 checked, 3 FAILED -- C3,C4,C6.  C3 and C4 are RED")
print("  BY DESIGN: SPEC 10.102 retracted the shape they measure.  C6 follows")
print("  them -- with the wrap gone the cut outline IS the art outline, so it")
print("  is no longer BELOW it at any station.")
print()
print("  AND C5 HAS FLIPPED TO PASS, WHICH IS THE POINT.  It was armed as a")
print("  KILL on the rev-43 finding that re-pointing the art's v-map would")
print("  STRETCH the art; it now reads 0.0 mm because there is nothing left to")
print("  re-point.  THAT IS LEDGER FINDING 1 CLOSING, INSTRUMENTED: the art")
print("  datum and the cut outline are one table again.  C1 and C2 are the")
print("  live controls and both still PASS.")
sys.exit(1 if FA else 0)
