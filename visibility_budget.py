"""visibility_budget.py -- rev 57b.  RANK THE WORK BY PIXELS, NOT BY GATES.

WHY THIS EXISTS.  The rev-57 brief states the project's ranking rule in its own
words: *"Gate availability is the ranking rule -- an item with a gate outranks
an item without one, because only the gated one can tell you whether you
improved the photograph."*  That rule is why the top job for FOUR revisions was
the VW badge's stroke weight.

It is a good rule for deciding what you can TRUST.  It is the wrong rule for
deciding what to DO, because measurability and visibility are anti-correlated
here: a small isolated feature is easy to gate precisely BECAUSE it is small
and isolated, while the things that dominate a photograph -- the gloss of two
square metres of paint, an untextured interior seen through three apertures --
are large, diffuse, and hard to reduce to one number.

So this script converts every open finding into the currency the owner actually
judges in: PIXELS OF THE DELIVERY FRAME.  It is deliberately crude.  A pixel
count is not a visibility model -- a 1 px error on a hard edge can read louder
than a 10^5 px error in a soft gradient, and that caveat is printed with the
table rather than hidden.  But four orders of magnitude are not a judgement
call, and that is the range this table spans.

    python3 visibility_budget.py [frame_width_px]
"""
import sys
import numpy as np
from PIL import Image

RX = int(sys.argv[1]) if len(sys.argv) > 1 else 3840
BUS_L = 4.065                       # STATE.md, overall length ex counter

# px/m is MEASURED off a real render at a known width, not assumed from the
# camera: the subject's own bbox in a hero frame.
#
# rev 60.  THIS NAMED out/r57_hero.png, A REVISION-NUMBERED FRAME THAT NO
# LONGER EXISTS AND WILL NEVER EXIST AGAIN -- out/ is untracked and starts
# empty, and no revision since 57 has written that prefix.  So the tool ALWAYS
# took its except branch and ALWAYS reported a FALLBACK scale, while still
# printing a ranked table that reads like a measurement.  That is rule 37
# exactly: an absent input must never read as a measurement.  It now GLOBS for
# whatever hero frame the tree actually has, newest first, and REFUSES in
# those words if there is none.
import glob as _glob, os
_heroes = sorted(_glob.glob("out/*hero*.png"), key=os.path.getmtime, reverse=True)
if not _heroes:
    print("NO RENDER -- visibility_budget needs a hero frame to measure its "
          "own scale off, and out/ holds none.  Render one first:")
    print("  T1_SUB=1 T1_PREVIEW=hero T1_PFX=rNN /tmp/blender/blender -b -P build.py")
    sys.exit(2)
try:
    a = np.asarray(Image.open(_heroes[0]).convert("RGB")).astype(int)
    nw = (a.max(axis=2) < 235) | (a.max(axis=2) - a.min(axis=2) > 12)
    xs = np.nonzero(nw)[1]
    W0 = a.shape[1]
    PXM = (xs.max() - xs.min()) / BUS_L * (RX / W0)
    src = "measured off %s (%d px wide)" % (_heroes[0], W0)
except Exception as e:
    print("NO RENDER -- %s could not be read (%s)" % (_heroes[0], e))
    sys.exit(2)

print("=" * 78)
print("  VISIBILITY BUDGET at a %d px delivery frame" % RX)
print("  scale: %.0f px/m  (%.2f mm per pixel)   [%s]" % (PXM, 1000 / PXM, src))
print("=" * 78)

# (id, what, linear error in m OR None, area affected in m2 OR None, note)
ROWS = [
    ("F44", "the paint's GLOSS -- the red flank alone",
     None, 2.50 * 0.60, "measured: the photograph's red spreads 2.55x as wide"),
    ("F44", "the paint's GLOSS -- the whole cream upper body",
     None, 4.07 * 0.95, "same defect, larger surface"),
    ("F45", "galley interior reads as untextured white blocks",
     None, 3 * 0.516 * 0.40, "seen through all three serving apertures"),
    ("F45", "roof-aperture interior, same",
     None, 1.20 * 0.45, "dead centre of the hero frame"),
    ("F15", "A7 -- unlit roofed body between the last inlet and the tail",
     0.803, 0.803 * 1.60, "ILLUMINATION over a large area, not dressing"),
    ("F01/F39", "Senor -- 28.5 % of its ink missing",
     None, 0.35 * 0.12, "hard-edged silver on red: loud per pixel"),
    ("F10", "the galley sits ~103 mm too far aft",
     0.103, None, "a placement error of a visible assembly"),
    ("F03/F04", "the cream mottle's feature size MOTTLE_M",
     0.024, None, "REFUTED as the cause of the gate's disagreement"),
    ("F38", "the built nose ring band, +9.5 % on the frame",
     0.095 * 0.028, None, "inside the record's own adopted uncertainty"),
    ("F08", "the badge stroke weight -- the whole 47-point bracket",
     0.47 * 0.02869, None, "CEILED: the frame cannot resolve it"),
    ("F08", "the badge stroke weight -- the 5.09 % it was meant to settle",
     0.0509 * 0.02869, None, "**the top job for four revisions**"),
    # ------------------------------------------------------------- rev 60
    # THE TABLE OMITTED EVERY ITEM THE OWNER HIMSELF RANKED.  At rev 59 it
    # listed neither the emblem, nor the ground shadow, nor the nose break --
    # three of his five -- and put the CEILED gloss row on top, so a context
    # that followed it would have worked a closed item and skipped his.
    ("F63/F69", "the VW glyph builds as an X -- nose roundel",
     None, 3.1416 * 0.14 ** 2, "OWNER, five times.  Gated and FAILING (C6)"),
    ("F63/F69", "the same glyph on four hubcaps",
     None, 4 * 3.1416 * 0.043429 ** 2, "same defect, four more instances"),
    ("F67", "the ground shadow and the underbody",
     None, 3.54 * 0.09, "the DARK BAND itself; PARTLY CLOSED at rev 60"),
    ("F67", "the contact shadow's footprint on the ground",
     None, 4.065 * 1.75, "what makes it read planted rather than floating"),
    ("F75/F87", "the nose two-tone break, 74 mm low at the lamp",
     0.074, 1.50 * 0.074, "OWNER.  Gated and FAILING (M1).  Lever UNKNOWN"),
    ("F99", "the galley interior is 1.39x too cool relative to its cream",
     None, 3 * 0.516 * 0.40, "supersedes F45, which rev 60 REFUTED as written"),
]

print("%-10s %-52s %10s %12s" % ("id", "what", "linear px", "area px^2"))
print("-" * 90)
scored = []
for i, (fid, what, lin, area, note) in enumerate(ROWS):
    lp = lin * PXM if lin else None
    ap = area * PXM * PXM if area else None
    scored.append((ap if ap else (lp * lp if lp else 0), fid, what, lp, ap, note))
    print("%-10s %-52s %10s %12s" % (
        fid, what,
        "%.1f" % lp if lp else "-",
        "%.0f" % ap if ap else "-"))
    print("%-10s   %s" % ("", note))
print("-" * 90)
scored.sort(reverse=True)
print("RANKED BY AREA AFFECTED, largest first:")
for k, (s, fid, what, lp, ap, note) in enumerate(scored, 1):
    print("  %2d. %-10s %-52s %s" % (k, fid, what[:52],
          ("%.2e px^2" % s) if s else "-"))
top = scored[0][0]; bot = [s for s, *_ in scored if s][-1]
print()
print("  The largest item is %.0fx the smallest." % (top / bot))
print("  THE ITEM AT THE BOTTOM WAS THE TOP JOB FOR FOUR REVISIONS.")
print()
print("  CEILING ON THIS TABLE, and it is a real one: pixels are not")
print("  visibility.  A hard-edged error reads louder per pixel than a soft")
print("  one, `Senor` being the clearest case here -- it is small and it is")
print("  loud.  Use this to catch ORDERS OF MAGNITUDE, not to rank neighbours.")
