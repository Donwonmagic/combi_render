"""probe_rev44_vpow -- REPORT 1, the "amtrak train" nose.  READ-ONLY.  No bpy.

HIS WORDS: "the front nose is shaped inaccurately... more like the front of an
amtrak train than a vw bus".  SPEC 10.24-family, ledger finding 6.

THE STATE OF IT: `V_POW` is LOCKED at 0.60 (SPEC 10.2).  The rev-11 audit
measured the V-swage arm rising ~2x too fast -- "lamp station to body edge
0.111 +- 0.015 m photographed against 0.208 built" -- and SPEC records that as
"implying V_POW = 0.30-0.48".  MEASURED AT REV 11, NEVER APPLIED.

WHAT THIS PROBE DOES.  It does NOT re-measure the photograph; it has no new
frame to measure (the owner's rev-44 batch contained no usable front view, and
this environment cannot fetch images).  It does four things that need no new
evidence at all:

  1. REPRODUCES the built 0.208 from the constants, which validates the frame.
  2. INVERTS the published 0.111 +- 0.015 for V_POW, and checks SPEC's own
     stated range against that inversion.
  3. PRICES THE INTERACTION WITH REPORT 3, which rev 44 has just fixed.
     Lowering V_POW RAISES the break at the lamp's column, so it moves the very
     clearance probe_rev44_report3 C6 now guards.  A fix that silently re-breaks
     a fix from the same revision is exactly how this project has been burned.
  4. CHECKS THE HARD BOUND.  SPEC 10.2: "V_APEX <= 0.396 above ground is a HARD
     BOUND, not an estimate" -- the cream wedge is still 14 px wide where the
     bumper occludes it.  V_POW does not move V_APEX, so the bound must remain
     satisfied; C4 states that rather than assuming it.

NOTHING IS APPLIED HERE.  10.24's own lesson is that a single-chain claim which
moves the FACE of the vehicle deserves a second derivation first, and this one
moves the whole nose.  One chain exists.
"""
import ast, math, sys

def lits(path, names):
    out = {}
    for n in ast.parse(open(path).read()).body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 \
           and isinstance(n.targets[0], ast.Name) and n.targets[0].id in names:
            try:
                out[n.targets[0].id] = ast.literal_eval(n.value)
            except ValueError:
                pass
    miss = set(names) - set(out)
    if miss:
        sys.exit("could not read %s from %s" % (sorted(miss), path))
    return out

SH = lits("t1_shell.py", ("V_APEX_Z", "V_RISE_Z", "V_POW_Z", "V_HALF_W"))
MT = lits("t1_mats.py",  ("Z_BELT_AUTH", "V_APEX_AUTH", "V_RISE", "V_POW"))
BC = {}
for n in ast.parse(open("build.py").read()).body:
    if isinstance(n, ast.Assign) and len(n.targets) == 1 \
       and isinstance(n.targets[0], ast.Name):
        try:
            BC[n.targets[0].id] = eval(compile(ast.Expression(n.value), "<c>",
                                               "eval"), {"__builtins__": {}}, dict(BC))
        except Exception:
            pass
LY, LZ = BC["HL_Y"], BC["HL_Z"]
R_LENS = 0.0862

def zV(y, p):
    t = min(abs(y), SH["V_HALF_W"]) / SH["V_HALF_W"]
    return SH["V_APEX_Z"] + SH["V_RISE_Z"] * t ** p

def rise(p):
    """the published quantity: lamp station to body edge."""
    return zV(SH["V_HALF_W"], p) - zV(LY, p)

def solve(target):
    """V_POW giving that rise.  Closed form: 1-(y/W)^p = target/V_RISE."""
    k = 1.0 - target / SH["V_RISE_Z"]
    return math.log(k) / math.log(LY / SH["V_HALF_W"])

print("=" * 72)
print('probe_rev44_vpow -- REPORT 1, the "amtrak train" nose')
print("=" * 72)
print()
print("  V_POW built            %.2f          V_APEX %.4f  V_RISE %.4f"
      % (SH["V_POW_Z"], SH["V_APEX_Z"], SH["V_RISE_Z"]))
print("  lamp column y = %.4f   body edge y = %.2f" % (LY, SH["V_HALF_W"]))
print()
print("  RISE from the lamp station to the body edge")
print("    built  @ V_POW %.2f : %.4f m   (SPEC 10.24-family publishes 0.208)"
      % (SH["V_POW_Z"], rise(SH["V_POW_Z"])))
PH, PS = 0.111, 0.015
print("    photographed        : %.3f +- %.3f m  -- rev-11 audit, ONE chain"
      % (PH, PS))
print("    the build is %.2fx too steep." % (rise(SH["V_POW_Z"]) / PH))
print()
p_mid, p_lo, p_hi = solve(PH), solve(PH + PS), solve(PH - PS)
print("  INVERTING THAT FOR V_POW")
print("    0.111        -> V_POW = %.4f" % p_mid)
print("    0.111 +0.015 -> V_POW = %.4f      (a BIGGER rise wants a BIGGER p)"
      % p_lo)
print("    0.111 -0.015 -> V_POW = %.4f" % p_hi)
print("    so the photograph implies V_POW = %.3f  (%.3f .. %.3f)"
      % (p_mid, min(p_lo, p_hi), max(p_lo, p_hi)))
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
ck("C1", abs(rise(SH["V_POW_Z"]) - 0.208) < 5e-4,
   "the built rise reproduces SPEC's published 0.208 (%.4f) -- the frame is "
   "right and the quantity is the one SPEC means" % rise(SH["V_POW_Z"]))
ck("C2", abs(SH["V_POW_Z"] - MT["V_POW"]) < 1e-9,
   "pressed swage V_POW_Z == painted V_POW (%.2f) -- they must never drift, "
   "SPEC 10.2" % SH["V_POW_Z"])
# C3 -- SPEC's OWN STATED RANGE against the inversion of its OWN numbers.
lo, hi = min(p_lo, p_hi), max(p_lo, p_hi)
ck("C3", lo <= 0.30 and hi >= 0.48,
   "SPEC states the measurement implies 'V_POW = 0.30-0.48'.  Inverting SPEC's "
   "OWN 0.111 +- 0.015 gives %.3f-%.3f.  The upper end 0.48 DOES NOT FOLLOW "
   "from the published figure -- it needs 0.111+0.048, over 3 sigma out.  "
   "SPEC's range is not reproducible from SPEC's own numbers."
   % (lo, hi))
# C4 -- the hard bound is untouched by p, and that is worth stating
ck("C4", (SH["V_APEX_Z"] - 0.0650) <= 0.396 + 1e-9,
   "the HARD BOUND holds and V_POW cannot move it: V_APEX above ground is "
   "%.4f against the bound 0.396 (bumper occlusion, ref_workshop.jpg).  "
   "Re-fitting V_POW is safe with respect to it."
   % (SH["V_APEX_Z"] - 0.0650))
# C5 -- THE INTERACTION.  Does a lower V_POW re-break Report 3?
clr_now = zV(LY, SH["V_POW_Z"]) - (LZ + R_LENS)
clr_new = zV(LY, p_mid) - (LZ + R_LENS)
print("       (headlamp clearance under the break: %.1f mm at V_POW %.2f, "
      "%.1f mm at %.3f)"
      % (clr_now * 1000, SH["V_POW_Z"], clr_new * 1000, p_mid))
ck("C5", clr_new > 0.010,
   "REPORT 3 SURVIVES: re-fitting V_POW to %.3f RAISES the break at the lamp's "
   "column, so the clearance rev 44 just won goes %.1f -> %.1f mm.  It does "
   "not re-break probe_rev44_report3 C6."
   % (p_mid, clr_now * 1000, clr_new * 1000))
# C6 -- and the other direction: this is why the two must be ordered
ck("C6", clr_new > clr_now,
   "and the ORDER was lucky, not clever: V_POW moves the same break Report 3 "
   "is measured against.  Had it moved the other way, applying Report 3 first "
   "would have had to be re-derived.  ANY FUTURE V_POW CHANGE MUST RE-RUN "
   "probe_rev44_report3.")

print()
print("CONTROLS: %d checked, %d FAILED%s"
      % (CH, len(FA), ("  -- " + ",".join(FA)) if FA else ""))
print("EXPECTED: 6 checked, 1 FAILED -- C3 only.  C3 is a FINDING against SPEC's")
print("          published range, not against the model.  NOTHING IS APPLIED.")
sys.exit(1 if FA else 0)
