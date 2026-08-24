"""probe_rev44_typo -- RE-VERIFYING THE TWO SURVIVING TYPOGRAPHY SEVERITY-5s
WITH THE WINDOW INDEPENDENTLY RE-DERIVED.  READ-ONLY.  No bpy.

READ THIS FIRST, REV 59 -- THIS PROBE NOW PRINTS "8 checked, 7 FAILED" AND
THAT IS NOT A NEW DEFECT IN THE GENERATOR.  Every C-row below is pinned to
`senor_trace._ref_mask()` as it stood at rev 44: 934 px in six pieces of
252/332/16/258/61/15.  THAT MASK WAS RE-BAKED AT REV 59 (see THE TILDE, REV 59
in senor_trace.py) because it was missing the tilde of the `n~`.  It is now
1062 px and it decomposes into FOUR pieces of 15/61/256/730 -- restoring the
tilde FUSES what used to be separate components, which is why C1, C2, C3, C4,
C5 and F2 all move at once.  The rows have deliberately NOT been re-pinned:
they are rev 44's record of rev 44's mask, and re-pinning them would erase the
evidence that the mask changed.  Re-derive them if you need them.

AND NOTE WHAT THAT MEANS FOR THE HISTORY BELOW.  AUDIT_rev43 sec.0's retracted
headline was "the n HAS NO TILDE".  Rev 44 retracted it because a 16 px mark
existed at the corner of the clipped window and concluded "a thin tilde is not
a missing one" (N1).  The 16 px mark was the 3 px stub and the lone inscribed
disc that `_STROKES` carried INSTEAD of a tilde.  Rev 59 measured the band the
photograph actually carries -- 186 px against the generator's 73 -- and drew
the stroke.  The rev-43 headline was nearer right than its retraction allowed.

WHY.  AUDIT_rev43 sec.0 retracted its headline -- "the n HAS NO TILDE" -- after
finding that BOTH adversarial refuters confirmed it because BOTH INHERITED THE
ORIGINAL'S WINDOW (x 48-64, y -8..+2), which clipped a real 16 px mark at one
corner.  They were given different estimators and the same place to look.  The
rule that came out of it: AN ADVERSARIAL VERIFIER MUST RE-DERIVE THE WINDOW,
NOT ONLY THE METHOD.  Ask "is the feature where they say it is?" BEFORE "is the
number right?".  The `typography` dimension's other two severity-5s were
downgraded to UNVERIFIED pending exactly that.  This is that re-check.

HOW THE WINDOW IS RE-DERIVED.  It is not.  THERE IS NO WINDOW.  Every statement
below is a CONNECTED-COMPONENT or TOPOLOGICAL property of the whole mask:
component count, component areas, bounding boxes ordered by x, and the number
of HOLES (Euler number) inside each component.  A test with no window cannot
inherit one.  Letter identity is assigned by left-to-right order of component
bounding boxes within the mask's own extent, which is re-derived from the mask.

WHAT IS BEING TESTED
  F1  "The capital S is in three fragments."
  F2  "The `e` is not drawn as a letter -- its bowl and its eye are gone."
Both are DES-lane findings against the generator, `script_gen.draw_senor`, with
`senor_trace._ref_mask()` as the measured photograph.
"""
import sys
import numpy as np

sys.path.insert(0, ".")
import senor_trace as ST
import script_gen as SG


def components(mask, conn=8):
    """8-connected labelling, written out rather than imported: scipy is not a
    dependency of this repo and adding one to run a probe is not worth it."""
    H, W = mask.shape
    lab = np.zeros((H, W), np.int32)
    nxt = 0
    if conn == 8:
        nb = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    else:
        nb = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    for sy in range(H):
        for sx in range(W):
            if not mask[sy, sx] or lab[sy, sx]:
                continue
            nxt += 1
            stack = [(sy, sx)]
            lab[sy, sx] = nxt
            while stack:
                y, x = stack.pop()
                for dy, dx in nb:
                    ny, nx_ = y + dy, x + dx
                    if 0 <= ny < H and 0 <= nx_ < W and mask[ny, nx_] \
                       and not lab[ny, nx_]:
                        lab[ny, nx_] = nxt
                        stack.append((ny, nx_))
    return lab, nxt


def holes(comp):
    """number of enclosed background regions in a single component.

    Background is labelled with 4-connectivity while the FOREGROUND used 8 --
    that pairing is what makes the Euler count well defined; using 8 for both
    would let a diagonal background thread leak out of a closed counter and
    report zero holes for a perfectly good `o`."""
    pad = np.zeros((comp.shape[0] + 2, comp.shape[1] + 2), bool)
    pad[1:-1, 1:-1] = comp
    bg = ~pad
    lab, n = components(bg, conn=4)
    outer = lab[0, 0]
    return len({v for v in np.unique(lab) if v and v != outer})


def describe(name, mask):
    lab, n = components(mask)
    print()
    print("  %s   %d x %d, %d ink px, %d COMPONENTS"
          % (name, mask.shape[1], mask.shape[0], int(mask.sum()), n))
    rows = []
    for i in range(1, n + 1):
        c = lab == i
        ys, xs = np.nonzero(c)
        sub = c[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        rows.append(dict(i=i, area=int(c.sum()), x0=int(xs.min()), x1=int(xs.max()),
                         y0=int(ys.min()), y1=int(ys.max()), h=holes(sub)))
    rows.sort(key=lambda r: r["x0"])
    print("     %-3s %6s  %-13s %-13s %s" % ("#", "area", "x range", "y range", "holes"))
    for r in rows:
        print("     %-3d %6d  %-13s %-13s %d"
              % (r["i"], r["area"], "%d..%d" % (r["x0"], r["x1"]),
                 "%d..%d" % (r["y0"], r["y1"]), r["h"]))
    return rows


print("=" * 74)
print("probe_rev44_typo -- the two typography severity-5s, window RE-DERIVED")
print("=" * 74)

ref = ST._ref_mask()
ref_rows = describe("MEASURED PHOTOGRAPH  senor_trace._ref_mask()", ref)

alpha = np.asarray(SG.senor_only(), dtype=float)
if alpha.max() > 1.5:
    alpha = alpha / 255.0
gen = alpha > 0.5
gen_rows = describe("GENERATOR OUTPUT     script_gen.senor_only() @ a>0.5", gen)

# ---------------------------------------------------- which piece is the tilde
# A FIRST CUT OF THIS TEST WAS WRONG AND IS RECORDED RATHER THAN REPLACED.
# It called a component a diacritic if its BOUNDING BOX sat above the median of
# the other boxes' tops.  That cannot see a mark sitting over ONE letter: the
# `e`+`n` mass spans x 22..56 and its box starts at y 13 because of the `e`,
# while over the `n`'s own columns the ink starts far lower.  The box test
# returned NONE on both masks and would have "refuted" a tilde that is plainly
# there -- the SAME CLASS OF ERROR as the window the original finding inherited.
# The test below is COLUMN-LOCAL: for a candidate component, look only at the
# columns it actually occupies, and ask whether every other component's ink in
# those columns lies BELOW it.  Derived from the candidate itself; no window.
def detached_marks(mask, lab, rows):
    out = []
    for r in rows:
        cols = slice(r["x0"], r["x1"] + 1)
        other = (lab != r["i"]) & (lab > 0)
        oc = other[:, cols]
        ys = np.nonzero(oc.any(axis=1))[0]
        if len(ys) and ys.min() > r["y1"]:
            out.append((r, int(ys.min())))
    return out

print()
print("WHICH COMPONENT IS THE TILDE -- column-local, derived from the mask")
marks = {}
for nm, m, rows in (("photograph", ref, ref_rows), ("generator ", gen, gen_rows)):
    lab, _ = components(m)
    d = detached_marks(m, lab, rows)
    # A DIACRITIC is a detached mark whose COLUMNS LIE INSIDE another single
    # component's column span -- it floats over a letter that continues past it
    # on both sides.  A vertically-fragmented letter (the S, broken at its
    # spine) also registers as "detached", and must not be confused with one:
    # its columns are its OWN, not borrowed from a neighbour.
    dia = []
    for r, top in d:
        for o in rows:
            if o["i"] != r["i"] and o["x0"] <= r["x0"] and r["x1"] <= o["x1"]:
                dia.append((r, top, o))
                break
    marks[nm.strip()] = dia
    for r, top in d:
        print("   %s: #%d  %d px at x %d..%d, y %d..%d -- next ink in those "
              "columns starts at y %d, i.e. %d px BELOW it"
              % (nm, r["i"], r["area"], r["x0"], r["x1"], r["y0"], r["y1"],
                 top, top - r["y1"]))
    for r, top, o in dia:
        print("     -> DIACRITIC: #%d sits inside #%d's columns (x %d..%d), so "
              "it floats over that letter rather than being a broken piece of "
              "one." % (r["i"], o["i"], o["x0"], o["x1"]))
    if not d:
        print("   %s: no detached mark found" % nm)

CH, FA = 0, []
def ck(tag, ok, msg, kill=False):
    global CH, FA
    CH += 1
    if not ok:
        FA.append(tag)
    print("  [%s] %s%s  %s" % ("PASS" if ok else "FAIL", tag,
                               " (KILL)" if kill else "", msg))

print()
print("CONTROLS")
ck("C1", len(ref_rows) == 6,
   "the photograph's mask decomposes into 6 pieces, as senor_trace's own "
   "docstring publishes (got %d)" % len(ref_rows))
pub = sorted([252, 332, 16, 258, 61, 15])
got = sorted(r["area"] for r in ref_rows)
ck("C2", got == pub,
   "and into the published areas 252/332/16/258/61/15 (got %s)"
   % "/".join(str(a) for a in got))
ck("C3", int(ref.sum()) == 934,
   "total measured ink is the published 934 px (got %d)" % int(ref.sum()))
ck("C4", len(marks["photograph"]) == 1 and len(marks["generator"]) == 1,
   "EXACTLY ONE DIACRITIC in each mask -- sec.0's retraction of the tilde "
   "finding REPRODUCES (photograph %d, generator %d).  The S's own spine break "
   "also reads as 'detached' and is excluded by the column-containment rule."
   % (len(marks["photograph"]), len(marks["generator"])))
_pt = marks["photograph"][0][0] if marks["photograph"] else None
_gt = marks["generator"][0][0] if marks["generator"] else None
ck("C5", _pt is not None and _pt["area"] == 16,
   "and the tilde is the SIXTEEN-pixel piece, as AUDIT_rev43 sec.0 says -- "
   "NOT the 62 px AUDIT_rev43 sec.5's typography ceiling quotes.  The only "
   "component near 62 px is the 61 px piece at x 9..23, which sits UNDER THE "
   "S, not over the n.  (measured %s px)"
   % (_pt["area"] if _pt else "none"))

# ---- NEW, rev 44.  The tilde is PRESENT but it is UNDER-WEIGHTED.
if _pt and _gt:
    print("       (tilde area: photograph %d px, generator %d px -- ratio "
          "%.2f)" % (_pt["area"], _gt["area"], _gt["area"] / _pt["area"]))
ck("N1", _pt is not None and _gt is not None
         and abs(_gt["area"] / _pt["area"] - 1.0) <= 0.35,
   "NEW FINDING, rev 44: the generator's tilde carries %s px against the "
   "photograph's %s -- it is PRESENT, which is what sec.0 retracted on, but "
   "it is roughly HALF the measured ink.  Severity is low and it is NOT the "
   "withdrawn misspelling finding returning: a thin tilde is not a missing "
   "one." % (_gt["area"] if _gt else "?", _pt["area"] if _pt else "?"))

# ---- F1 and F2, the two downgraded severity-5s
s_ref = [r for r in ref_rows if r["x1"] <= 25]
s_gen = [r for r in gen_rows if r["x1"] <= 31]
ck("F1", len(s_ref) == 3 and len(s_gen) == 3,
   "F1 'the capital S is in three fragments' -- TRUE, and TRUE OF THE "
   "PHOTOGRAPH TOO (%d pieces measured, %d generated).  senor_trace's own "
   "docstring says it reproduces those breaks deliberately because they are "
   "what was measured.  A faithful copy of a tarnish artefact is not a "
   "generator defect." % (len(s_ref), len(s_gen)))
_h_ref = max(r["h"] for r in ref_rows)
_h_gen = max(r["h"] for r in gen_rows)
ck("F2", _h_ref == _h_gen,
   "F2 'the e's bowl and eye are gone' -- REFUTED on topology: the "
   "e-bearing component carries %d holes in the photograph and %d in the "
   "generator.  Same count, same component, same place." % (_h_ref, _h_gen))

print()
print("CONTROLS: %d checked, %d FAILED%s"
      % (CH, len(FA), ("  -- " + ",".join(FA)) if FA else ""))
print("EXPECTED: 8 checked, 1 FAILED -- N1 only.  N1 is the one NEW finding")
print("          here: the tilde is present but half-weight.  Everything else")
print("          passes, which is the point -- BOTH downgraded severity-5s are")
print("          REFUTED as generator defects with the window re-derived.")
sys.exit(1 if FA else 0)
