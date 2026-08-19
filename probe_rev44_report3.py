"""probe_rev44_report3 -- SPEC 10.24 item 3, the ORDINAL, off the BUILD's own
constants.  READ-ONLY.  No bpy, no camera, no hero, no photograph.

WHY THIS EXISTS.  Rev 43 added a PHOTOGRAPHIC arm to Report 3: on
ref_source.jpeg the headlamp sits 20 px BELOW the two-tone break.  The owner's
words are "the paint job and the headlights are not alligned", so the headlamp
arm is the one that matters.  The rev-44 brief asks for the same above/below
read off the build's constants -- exact, no camera.

THE TRAP THIS PROBE IS BUILT AROUND.  The two-tone break is NOT a line at the
headlamp.  Across the nose it is the V-swage, t1_shell.zV(y), which at the
lamp's own column sits well BELOW the flank belt.  Comparing the lamp against
the FLANK BELT instead of against the V AT THE LAMP'S COLUMN is a 208 mm error
and it flips nothing -- it just makes the gap look 7x bigger than it is.  C5 is
that mistake, armed as a KILL control: IT IS WRITTEN TO FAIL.

THE RESULT, AND IT IS STRONGER THAN A GAP.  Comparing CENTRES does not
discriminate: build and photograph BOTH put the lamp centre below the break, so
rev 43's ordinal arm is consistent with the build and is NOT evidence of the
defect.  The discriminating fact is TOPOLOGICAL and needs no scale at all --
in the build the break line CUTS ACROSS THE HEADLAMP APERTURE, a 132 mm chord
over a 172 mm lens; in ref_source.jpeg the lamp sits entirely in the red with
~12 px of clear red above it.  C6 instruments that, and it is the burn-down
gate for SPEC 10.24 item 3: it goes green when the defect is fixed.

FRAME.  It does not matter.  build.py step 8b shears every vertex by
rake_drop(x) = RAKE_Z0 + RAKE_DZDX*x.  The lamp and the swage sit at the SAME
station, so the shear subtracts from both and cancels out of the difference.
C4 proves that by evaluating at two stations 3 m apart and demanding equality.
"""
import ast, math, sys

def lits(path, names):
    """module-level literal assignments, read with ast -- never imported."""
    src = open(path).read()
    out = {}
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
           and isinstance(node.targets[0], ast.Name) \
           and node.targets[0].id in names:
            try:
                out[node.targets[0].id] = ast.literal_eval(node.value)
            except ValueError:
                pass
    missing = set(names) - set(out)
    if missing:
        sys.exit("could not read %s from %s" % (sorted(missing), path))
    return out

def lamp_loc():
    """the headlamp placement, read out of build.py by ast.

    rev 44 replaced the literals with names (HL_X / HL_Y / HL_Z), so the tuple
    is no longer literal and the placement must be resolved through build.py's
    module-level assignments.  Resolving them rather than re-typing them is the
    whole point -- a probe that carries its own copy of the constant cannot
    detect the constant changing."""
    for node in ast.walk(ast.parse(open("build.py").read())):
        if not isinstance(node, ast.Call):
            continue
        if not (isinstance(node.func, ast.Attribute) and node.func.attr == "place"):
            continue
        for kw in node.keywords:
            if kw.arg != "loc" or not isinstance(kw.value, ast.Tuple):
                continue
            el = kw.value.elts
            if len(el) != 3:
                continue
            try:
                x = ast.literal_eval(el[0]); z = ast.literal_eval(el[2])
            except ValueError:
                continue
            # y is `s * 0.5450`
            if isinstance(el[1], ast.BinOp) and isinstance(el[1].op, ast.Mult):
                try:
                    y = ast.literal_eval(el[1].right)
                except ValueError:
                    continue
            else:
                continue
            if abs(x - 2.1015) < 1e-9:
                return x, y, z
    sys.exit("headlamp placement literal not found in build.py")

def _build_consts():
    """HL_X / HL_Y / HL_Z / IND_Y / IND_Z, evaluated from build.py's own
    module-level assignments.  HL_Z is `1.0300 - HL_DROP` and IND_Z is
    `HL_Z + IND_DZ`, so a plain literal_eval will not do it."""
    env = {}
    for node in ast.parse(open("build.py").read()).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
           and isinstance(node.targets[0], ast.Name):
            try:
                env[node.targets[0].id] = eval(
                    compile(ast.Expression(node.value), "<c>", "eval"),
                    {"__builtins__": {}}, dict(env))
            except Exception:
                pass
    return env

BC = _build_consts()
MT = lits("t1_mats.py",  ("Z_BELT_AUTH", "V_APEX_AUTH", "V_RISE", "V_POW"))
SH = lits("t1_shell.py", ("V_APEX_Z", "V_RISE_Z", "V_POW_Z", "V_HALF_W"))
CO = lits("t1_core.py",  ("RAKE_Z0", "RAKE_DZDX"))
LX, LY, LZ = BC["HL_X"], BC["HL_Y"], BC["HL_Z"]

def zV_auth(y):
    """two-tone V height at half-width y, AUTHORED (un-dropped) frame."""
    t = min(abs(y), SH["V_HALF_W"]) / SH["V_HALF_W"]
    return SH["V_APEX_Z"] + SH["V_RISE_Z"] * t ** SH["V_POW_Z"]

def rake_drop(x):
    return CO["RAKE_Z0"] + CO["RAKE_DZDX"] * x

print("=" * 70)
print("probe_rev44_report3 -- SPEC 10.24 item 3, the ORDINAL from constants")
print("=" * 70)
print("  headlamp placement literal (build.py) : x %.4f  y %+.4f  z %.4f"
      % (LX, LY, LZ))
print("  V swage  apex %.4f  rise %.4f  pow %.2f  half-width %.2f"
      % (SH["V_APEX_Z"], SH["V_RISE_Z"], SH["V_POW_Z"], SH["V_HALF_W"]))
print("  flank belt (authored)                 : %.4f" % MT["Z_BELT_AUTH"])

brk = zV_auth(LY)
gap = brk - LZ
print()
print("  two-tone break AT THE LAMP'S OWN COLUMN y=%.4f : z = %.6f" % (LY, brk))
print("  headlamp centre                                : z = %.6f" % LZ)
print()
print("  ORDINAL: the headlamp centre sits %.1f mm %s the two-tone break."
      % (abs(gap) * 1000.0, "BELOW" if gap > 0 else "ABOVE"))
print()

# ------------------------------------------------------- the photographic arm
# SPEC 10.24 item 3 / SPEC.md 6936: photographed headlamp centre = belt - 0.339
# +- 0.025 m against the build's belt - 0.242.
PH_BELOW_BELT, PH_SD = 0.339, 0.025
bl_gap = MT["Z_BELT_AUTH"] - LZ                     # build, lamp below BELT
v_below_belt = MT["Z_BELT_AUTH"] - brk              # how far the V sits below belt
ph_gap = PH_BELOW_BELT - v_below_belt               # photo, lamp below BREAK
print("  the same read for the PHOTOGRAPHED lamp (SPEC 10.24: belt -%.3f):"
      % PH_BELOW_BELT)
print("    V sits %.1f mm below the belt at this column; photographed lamp is"
      % (v_below_belt * 1000.0))
print("    %.1f mm below the belt, hence %.1f mm %s the break."
      % (PH_BELOW_BELT * 1000.0, abs(ph_gap) * 1000.0,
         "BELOW" if ph_gap > 0 else "ABOVE"))
print()
print("  >>> BUILD says BELOW by %.1f mm.  PHOTOGRAPH says BELOW by %.1f mm."
      % (abs(gap) * 1000.0, abs(ph_gap) * 1000.0))
if abs(ph_gap - gap) < 5e-4:
    print("  >>> THEY NOW AGREE, to %.1f mm.  SPEC 10.24 item 3 was APPLIED at"
          % (abs(ph_gap - gap) * 1000.0))
    print("      rev 44: the lamp came DOWN 97.0 mm on the belt-relative arm.")
    print("      HISTORICAL NOTE, kept because it is the reason the fix took 34")
    print("      revisions to land: BEFORE the fix both figures were BELOW too")
    print("      (34.4 mm built against 131.4 photographed), so rev 43's")
    print("      ordinal arm was consistent with the broken build and could")
    print("      never have discriminated.  What discriminated was the CHORD.")
else:
    print("  >>> THE ORDINAL AGREES.  The sign is NOT the defect; the MAGNITUDE")
    print("      is, by %.1f mm.  An ordinal test cannot discriminate here."
          % (abs(ph_gap - gap) * 1000.0))
print()

# ------------------------------------------------- THE DISCRIMINATING TEST
# Does the two-tone break cross the headlamp aperture?  Pure topology: no
# scale, no camera, no px/m conversion, so no view can argue with it.
R_LENS = 0.0862                 # t1_detail.headlamp: lens outer radius
R_RING = 0.0862 + 0.0165        # chrome ring outer

def crosses(R, n=4001):
    """y-interval over which zV(y) lies inside the lamp disc of radius R."""
    hit = []
    for i in range(n):
        y = LY - R + 2.0 * R * i / (n - 1)
        d = max(R * R - (y - LY) ** 2, 0.0)
        if LZ - math.sqrt(d) <= zV_auth(y) <= LZ + math.sqrt(d):
            hit.append(y)
    return (min(hit), max(hit)) if hit else None

print("THE DISCRIMINATING TEST -- topological, needs no scale")
xing = {}
for nm, R in (("lens", R_LENS), ("chrome ring", R_RING)):
    iv = crosses(R)
    xing[nm] = iv
    print("  %-11s r=%.4f  disc top %.4f  break at that column %.4f"
          % (nm, R, LZ + R, brk))
    if iv:
        print("               *** THE BREAK CUTS ACROSS IT: chord %.1f mm of a "
              "%.1f mm width" % ((iv[1] - iv[0]) * 1000.0, 2 * R * 1000.0))
    else:
        print("               break is clear of the disc")
_rim = LZ + R_LENS - brk
print("  the lamp's upper rim stands %.1f mm %s the break at its own column."
      % (abs(_rim) * 1000.0, "ABOVE" if _rim > 0 else "BELOW"))
print()
print("  THE PHOTOGRAPH (ref_source.jpeg, 246x197, measured rev 44):")
print("    topmost-red per column at x=47 -> break y=117; lens spans y=129..145")
print("    (clean columns x=47..49, vertical extent 16/17/17 px).")
print("    THE LAMP SITS ENTIRELY IN THE RED, 12 px of clear red above it.")
print("    Rev 43's 20 px centre-gap REPRODUCES (137-117=20); its absolute rows")
print("    (120/140) are 3 px low -- a red-threshold difference, gap unaffected.")
print()
if xing["lens"] is None:
    print("  >>> BUILD: the headlamp is CLEAR of the two-tone line.")
    print("  >>> PHOTOGRAPH: the headlamp is CLEAR of it.")
    print("  >>> AGREED.  This is what \"the paint job and the headlights are")
    print("      not alligned\" was asking for, and it needed no px/m.")
    print("      BEFORE rev 44 the break cut a 131.9 mm chord across a 172.4 mm")
    print("      lens and a 159.9 mm one across the 205.4 mm chrome ring.")
else:
    print("  >>> BUILD: the two-tone line runs ACROSS the headlamp.")
    print("  >>> PHOTOGRAPH: the headlamp is CLEAR of it.")
    print("  >>> That is \"the paint job and the headlights are not alligned\",")
    print("      and no px/m conversion enters it.")
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
ck("C1", abs(SH["V_APEX_Z"] - MT["V_APEX_AUTH"]) < 1e-9,
   "pressed swage apex %.4f == painted apex %.4f (they must not drift)"
   % (SH["V_APEX_Z"], MT["V_APEX_AUTH"]))
ck("C2", abs((MT["V_APEX_AUTH"] + MT["V_RISE"]) - MT["Z_BELT_AUTH"]) < 1e-9,
   "V arms land on the flank belt: %.4f + %.4f == %.4f"
   % (MT["V_APEX_AUTH"], MT["V_RISE"], MT["Z_BELT_AUTH"]))
# C3 -- THE FRAME CHECK, RE-POINTED AT REV 44 WHEN THE FIX LANDED.
# Before the fix it asserted the build's own published belt - 0.242, and that
# is what validated the frame arithmetic.  The fix MOVES that quantity onto the
# PHOTOGRAPHED belt - 0.339, so the old assertion had to become the new one or
# the control would fire on its own success.  Both figures are SPEC 10.24's.
ck("C3", abs(bl_gap - PH_BELOW_BELT) < 5e-5,
   "the build now sits on SPEC 10.24's PHOTOGRAPHED figure: belt - lamp = "
   "%.4f against %.3f (it read 0.242 before rev 44 applied item 3)"
   % (bl_gap, PH_BELOW_BELT))
# C4 -- the shear cancels.  Evaluate the SAME difference at two stations 3 m
# apart in the DROPPED frame and demand they agree to 1e-12.
g0 = (zV_auth(LY) - rake_drop(LX)) - (LZ - rake_drop(LX))
g1 = (zV_auth(LY) - rake_drop(LX + 3.0)) - (LZ - rake_drop(LX + 3.0))
ck("C4", abs(g0 - g1) < 1e-12 and abs(g0 - gap) < 1e-12,
   "rake-independent: same gap at two stations 3 m apart (%.9f / %.9f)"
   % (g0, g1))
# C5 -- KILL.  WRITTEN TO FAIL.  If this ever passes, the probe has stopped
# distinguishing the V-swage from the flank belt and its number is worthless.
ck("C5", abs(bl_gap - gap) < 0.010,
   "KILL: lamp-vs-FLANK-BELT (%.1f mm) must NOT equal lamp-vs-V-AT-COLUMN "
   "(%.1f mm).  EXIT CODE 1 IS THE INTENDED RESULT HERE."
   % (bl_gap * 1000.0, gap * 1000.0), kill=True)

# C6 -- THE FINDING GATE for SPEC 10.24 item 3.  FAILS TODAY BY MEASUREMENT,
# not by design: the photograph has the lamp clear of the break and the build
# does not.  THIS ONE GOES GREEN WHEN THE DEFECT IS FIXED -- it is the
# burn-down instrument, and it must not be confused with C5, which must never
# go green.
ck("C6", xing["lens"] is None,
   ("GATE for SPEC 10.24 item 3: the break is CLEAR of the lens disc, as it is "
    "in the photograph.  The lens top sits %.1f mm BELOW the break.  GREEN "
    "SINCE REV 44 APPLIED THE FIX -- if this ever fires again the lamp or the "
    "swage has moved." % ((brk - (LZ + R_LENS)) * 1000.0))
   if xing["lens"] is None else
   ("FINDING: the break must be CLEAR of the lens disc, as it is in the "
    "photograph.  It is not -- it cuts a %.1f mm chord."
    % ((xing["lens"][1] - xing["lens"][0]) * 1000.0)))

print()
print("CONTROLS: %d checked, %d FAILED%s"
      % (CH, len(FA), ("  -- " + ",".join(FA)) if FA else ""))
print("EXPECTED SINCE REV 44: 6 checked, 1 FAILED -- C5 only, the KILL control,")
print("          which must never go green.  C6 is the gate for 10.24 item 3")
print("          and it went GREEN when rev 44 applied the fix.")
sys.exit(1 if FA else 0)
