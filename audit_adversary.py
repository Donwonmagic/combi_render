"""audit_adversary.py -- rule 15's half of the outgoing-brief audit.

`audit_brief.py` asks *is what the file says TRUE?* -- paths, switches, counts.
This asks the other question: *what would make it FALSE?*  They are different
instruments and rev 55 onward has required both.  The difference is that this
one RECOMPUTES the brief's headline figures from the source, the photographs
and the renders rather than checking that a string is present.

Written as a script and RUN, so the list a revision reports is what actually
executed rather than what it meant to try.  REPLACE the questions each
revision -- they are about THAT revision's claims, and a question that can no
longer fail is not a control.  Keep the shape: recompute, don't re-read.

REV 60's questions.  Rev 59's are RETIRED WITH REV 59's CLAIMS -- they asked
about the door lobes, the re-based clearance guard and the front arch, all of
which are closed and none of which can fail any more.

MOST OF THESE RECOMPUTE FROM A PHOTOGRAPH, NOT A RENDER, on purpose: rev 60's
headline numbers are photograph-side (a px/m, a cavity ratio, two chroma
ratios) and a question that needs `out/` is a question that reports the
untracked directory instead of the brief (F58, rule 37).  The three that DO
need the source read the source.

    python3 audit_adversary.py
"""
import os, re, subprocess, sys, glob
import numpy as np


def _newest(pattern):
    """Highest-numbered rev file.  LEXICAL sort is WRONG here and was: it puts
    NEXT_CONTEXT_PROMPT_rev9.md after rev61, so the question below asked
    whether rev 9's brief names the rev-61 work list.  verify_clone.sh gets
    this right with `sort -V`; this copy did not.  CLAUDE.md's own rule: find
    it with a sort that understands the number, never trust a typed name."""
    return max(glob.glob(pattern),
               key=lambda f: int(re.search(r'rev(\d+)', f).group(1)))


def _code(path):
    """Source with comments stripped.  A row about a STRING must not match its
    own explanatory comment -- that has happened FIVE times in this repository
    (brief §10.4), and it happened again here on the first run of the
    visibility_budget question below."""
    return "\n".join(l.split('#')[0] for l in open(path).read().split("\n"))

from PIL import Image

os.chdir(os.path.dirname(os.path.abspath(__file__)))
P = print
bad = []
NQ = [0]

# rev 61, CAUGHT BY AN ADVERSARY: this was HARDCODED to the INCOMING brief, so
# every question that greps `B` tested the document this revision RECEIVED and
# never the one it SHIPS -- while sec.10.5 says to run both audits on the
# outgoing brief and record what they found IN it.  `audit_brief.py` had always
# auto-detected; this one had not.  It is the newest brief now, by the same
# rule the rest of the project uses: find it with ls, never by a typed name.
BRIEF = sorted(glob.glob('NEXT_CONTEXT_PROMPT_rev*.md'),
               key=lambda f: int(re.search(r'rev(\d+)', f).group(1)))[-1]


def t(q, ok, d=""):
    NQ[0] += 1
    P("  %-5s %s" % ("ok" if ok else "BROKE", q))
    P("         %s" % d)
    if not ok:
        bad.append(q)


B = open(BRIEF).read()
P("=" * 78)
P("  audit_adversary.py -- what would make %s false?" % BRIEF)
P("=" * 78)

import t1_shell as S          # noqa: E402
import t1_core as T           # noqa: E402
import t1_detail as D_        # noqa: E402  -- constants only, no bpy calls made

# ------------------------------------------------- the underbody, from source
t("is the underbody actually BUILT, or only described in the brief?",
  hasattr(D_, "underbody") and "underpan" in open('t1_detail.py').read()
  and 'A(D.underbody(),' in open('build.py').read(),
  "t1_detail.underbody() must exist AND build.py must call it -- a function "
  "nobody calls is a paragraph")

# rev 60c -- THIS QUESTION WAS ASKING ABOUT THE WRONG QUANTITY.  It read
# `D_.UNDER_DROP < 0.151`, but rev 60b silently changed what UNDER_DROP MEANS:
# it was the visible drop (0.090) and became the pan prism's DEPTH, most of it
# buried inside the shell (0.124 now).  The question went on printing "ok"
# against a ceiling that belongs to a quantity it had stopped measuring.
# UNDER_VIS is the visible drop and is what the photograph's band bounds.
t("is the VISIBLE drop really under the 0.151 m ceiling? (UNDER_VIS, not "
  "UNDER_DROP -- rev 60b changed what UNDER_DROP means)",
  D_.UNDER_VIS < 0.151,
  "UNDER_VIS = %.4f m against a measured ceiling of 0.151 m.  If this ever "
  "exceeds it, the pan is deeper than the photograph's whole dark band, which "
  "contains the shadowed ground as well" % D_.UNDER_VIS)

# rev 60b -- THIS QUESTION WAS A LITERAL TAUTOLOGY AND IT PASSED THROUGH THE
# WORST DEFECT OF THE REVISION.  It asserted `UNDER_RAMP_W == UNDER_W` while
# t1_detail.py contains the line `UNDER_RAMP_W = UNDER_W` -- a threshold
# derived from the expression it checks (rule 6) -- and it read OK while both
# end closers were built wholly on the off side, 685 mm proud of the skin
# (rev 60c: this said 919 mm; 1.560 - 0.875 = 0.685, and 919 mm is
# reachable from no half-width this vehicle has -- it was wrong in three
# files at once).
#
# IT NOW ASKS THE MESH, via STATE.md, which audit.py writes FROM the mesh.
# A constant cannot answer a question about where a part ended up.
_ST = open('STATE.md').read()
_mY = re.search(r'full-Y \[([-0-9.]+), ([-0-9.]+)\]', _ST)
t("does the MESH still hold its lateral extent? (not the constants -- the MESH)",
  _mY is not None and abs(float(_mY.group(1)) + 1.0637) < 0.005
  and abs(float(_mY.group(2)) - 1.1500) < 0.005,
  "STATE.md full-Y %s against the baseline [-1.0637, 1.1500] set by the counter "
  "brackets and mir_head-1.  Rev 60 moved it to -1.5600 and the line was "
  "printed, logged and never read" % (_mY.groups() if _mY else "ABSENT",))

# rev 60c -- THE TWO AXES THE y QUESTION ABOVE CANNOT SEE.  An independent
# adversary reinstated rev 60's z error in full on the repaired tree and every
# check in this repository stayed green, because nothing asserted anything
# about the underbody except its NAMES and its y extent.  These ask STATE.md,
# which audit.py writes from the mesh, for verify.py's own two measurements.
_mS = re.search(r'underbody/shell fit: worst intrusion ([-+0-9.]+) mm', _ST)
t("does the underbody still MEET the shell? (the z axis rev 60b left open)",
  _mS is not None and float(_mS.group(1)) >= 5.0,
  "STATE.md's underbody/shell intrusion is %s.  It must be >= +5 mm: the pan's "
  "top has to INTRUDE into the shell, not merely reach for it.  Rev 60b set it "
  "from ZB and left -29.1 mm of open slot at the tail, because ZB is not the "
  "shell's underside" % (_mS.group(1) + " mm" if _mS else "ABSENT"))

_mP = re.search(r'underbody proudness: worst ([-+0-9.]+) mm', _ST)
t("is every underbody part still INBOARD of the skin at its own station?",
  _mP is not None and float(_mP.group(1)) <= 2.0,
  "STATE.md's worst underbody proudness is %s.  It must be <= +2 mm.  The y "
  "extent question above CANNOT see this: its bound is two fixed scalars, so a "
  "part may stand 280 mm proud on +y without moving either -- and rev 60b's "
  "aft ramp was doing exactly that, 48 mm proud, while that row read green"
  % (_mP.group(1) + " mm" if _mP else "ABSENT"))

# NOT "== HEAD": audit.py stamps the commit it ran AT, and STATE.md is then
# committed, so that form lags by one commit BY CONSTRUCTION and could never
# pass.  The real question is whether any GEOMETRY SOURCE moved after it was
# written -- that is what makes it stale.
_stc = re.search(r'\| git commit \| `([0-9a-f]+)`', _ST).group(1)
_since = subprocess.run(
    ['git', 'diff', '--name-only', _stc, 'HEAD', '--',
     'build.py', 't1_core.py', 't1_shell.py', 't1_detail.py', 't1_mats.py'],
    capture_output=True, text=True).stdout.split()
t("is STATE.md CURRENT for the geometry? (19 verify rows read it)",
  not _since,
  "STATE.md was written at %s; geometry source changed since: %s.  A stale "
  "STATE.md makes every row that reads it a claim about an older tree, and rev "
  "60 shipped it two revisions stale once already"
  % (_stc, ", ".join(_since) if _since else "nothing"))

# rev 60c-ii -- THIS QUESTION CRASHED, AND A GUARD THAT CRASHES REPORTS
# NOTHING (CLAUDE.md rule 3).  It read `D_.UNDER_RAMP`, a constant rev 60c
# SPLIT into UNDER_RAMP_F and UNDER_RAMP_A because the two ends need different
# lengths.  The rename was made and this file was not re-run, so the adversary
# died on an AttributeError PART WAY THROUGH ITS LIST -- every question below
# it silently went unasked, and the run still looked like it had produced
# output.  Both ends are asked now, by name.
t("does the AFT ramp stay clear of the vehicle's FIXED bodywork limit?",
  D_.UNDER_X1 - D_.UNDER_RAMP_A > -1.905,
  "aft ramp reaches x %.4f against the -1.905 limit that verify.py's length "
  "row enforces.  The first cut reached -2.100 and went red at +205 mm"
  % (D_.UNDER_X1 - D_.UNDER_RAMP_A))

t("does the FRONT ramp stay inboard of the front bodywork?",
  D_.UNDER_X0 + D_.UNDER_RAMP_F < 2.127,
  "front ramp reaches x %.4f against the body's own +2.127 front limit"
  % (D_.UNDER_X0 + D_.UNDER_RAMP_F))

# was a REGEX ON SOURCE that `(0.099` would have satisfied; now it compares the
# two albedos numerically, which is the thing the claim is about.
_MT = open('t1_mats.py').read()
_us = re.search(r'M\["underseal"\]\s*=\s*interior_wear\([^,]+,\s*\(([0-9.]+)', _MT)
_dk = re.search(r'M\["dark"\]\s*=\s*interior_wear\([^,]+,\s*\(([0-9.]+)', _MT)
t("is the underseal really DARKER than the interior grey it replaced?",
  _us is not None and _dk is not None
  and float(_us.group(1)) < 0.5 * float(_dk.group(1)),
  "underseal albedo %s against M['dark'] %s -- the 0.352 -> 0.219 step has no "
  "cause unless this is materially darker"
  % (_us.group(1) if _us else "ABSENT", _dk.group(1) if _dk else "ABSENT"))

# ----------------------------------------------- the guard I broke, from source
t("is V_POW's by-value pin STILL greppable, with the ablation beside it?",
  len(re.findall(r'^V_POW = 0\.52$', open('t1_mats.py').read(), re.M)) == 1
  and 'T1_VPOW' in open('t1_mats.py').read(),
  "three verify_clone rows grep '^V_POW = 0.52'.  Rev 60's first ablation cut "
  "took out all three at once; the literal must stay on its own line.  The "
  "VALUE moved 0.60 -> 0.52 at rev 61 (F135) and all three rows moved WITH it")

t("do T1_VPOW and T1_VPOWZ BOTH exist, so paint and swage can move together?",
  'T1_VPOW' in open('t1_mats.py').read()
  and 'T1_VPOWZ' in open('t1_shell.py').read(),
  "the brief tells rev 61 to sweep these; one without the other cannot keep "
  "verify.py's registration row satisfied")

# ------------------------------------------ rev 60's PHOTOGRAPH-side arithmetic
a = np.asarray(Image.open('ref_side.jpg').convert('RGB')).astype(float)
lum = a.mean(2)
col = lum[:, 350:500].mean(1)
cav, opn = col[605:650].min(), col[700:740].mean()
t("is the photographed cavity really 0.057 of open ground?",
  abs(cav / opn - 0.057) < 0.006,
  "ref_side.jpg cols 350-500: cavity floor %.1f DN, open plateau %.1f DN, "
  "ratio %.4f -- the brief says 0.057" % (cav, opn, cav / opn))

row = lum[599:604, :].mean(0)
dark = np.nonzero(row[640:830] < 40)[0]
# rev 60b: the TYRE-SPAN scale is retracted entirely -- that window was on the
# arch shadow and the kerb, not the tyre.  This now asks whether the source
# carries the RIM-FIT scale and has stopped asserting the dead one.
_TD = open('t1_detail.py').read()
t("has the dead tyre-span scale been replaced by the rim-fit one?",
  "211.6 px/m" in _TD and "hub-to-hub 507.8" in _TD
  and not re.search(r'^[^#\n]*258\.6', _TD, re.M),
  "the scale is now 211.6 px/m from a CIRCLE FIT to both cream rims "
  "(rear rms 1.11 px over 828 points), not a luminance run through the arch "
  "shadow.  If the old figure comes back, so does a 23 % error in every metric "
  "quantity taken off ref_side.jpg")

b = np.asarray(Image.open('ref_nolita_doorshut.jpg').convert('RGB')).astype(float)
ii = b[138:157, 288:315]
ee = b[183:192, 240:280]
ri = ii[..., 0].mean() / ii[..., 2].mean()
re_ = ee[..., 0].mean() / ee[..., 2].mean()
t("is the photographed interior really WARMER than its own exterior cream?",
  abs(ri - 1.357) < 0.05 and abs(re_ - 1.130) < 0.05 and ri / re_ > 1.15,
  "interior R/B %.3f, exterior R/B %.3f, ratio %.3f -- the brief claims "
  "1.357 / 1.130 / 1.201, and F99's whole case is that this ratio inverts in "
  "the render" % (ri, re_, ri / re_))

# ------------------------------------------------------- the brief's own bones
t("does the brief still CARRY §0 and §0.1, the reference-set guarantee?",
  "## §0. THE GOAL" in B and "§0.1 THE REFERENCE SET IS COMPLETE" in B,
  "rev 60 DROPPED §0 while assembling this brief and caught it only by "
  "accident.  It is a carrier (rule 16) and it holds the owner's own words "
  "about the reference set")

t("does every finding ID the gap review cites actually exist in the register?",
  all(i in open('OPEN_FINDINGS.md').read()
      for i in re.findall(r'\bF(?:9[0-9]|10[0-7])\b', open('GAPS_rev60.md').read())),
  "GAPS_rev60.md is the deliverable the owner asked for by name; a dangling "
  "ID in it is a dangling promise")

t("is every 'ALL n PASS' in the brief attached to the script that prints it?",
  all(('verify_clone' in ln or 'bootstrap' in ln or 'SELF-CONSISTENCY' in ln)
      for ln in B.splitlines() if re.search(r'ALL \d+ PASS', ln)),
  "two scripts print that phrase and a blind rewrite has corrupted this brief "
  "before")

t("does the brief promise a lever for item B that rev 60 already refuted?",
  not re.search(r'V_POW\s+needs\s+0\.345', B),
  "rev 58's 0.345 is refuted by four renders; if the brief still offers it as "
  "the fix, rev 61 will spend itself on it exactly as rev 59 did")

# ==========================================================================
# REPLACED AT REV 60c-ii FOR REV 61 (§10.5: "a question that can no longer
# fail is not a control").  The questions above are about REV 60's claims and
# most can no longer fail.  Each of these is about something that WAS wrong in
# this tree within the last revision, so each can fail again.
# ==========================================================================

t("does the ledger's ABLATED G4 still match the probe's own header?",
  "T1_NOUNDER=1   G3 0.8375   G4 0.5475" in open('probe_rev45_ground.py').read()
  and "0.5607" not in open('LEDGER_rev60.md').read(),
  "T1_NOUNDER omits the underbody ENTIRELY, so no mesh change can move this "
  "number.  0.5607 was published in five documents against a five-run mean of "
  "0.5475 (F130); if it reappears, something transcribed it back")

t("does probe_rev59_door's feet() still pass its own selftest?",
  subprocess.run(['python3', 'probe_rev59_door.py', '--selftest'],
                 capture_output=True, text=True).returncode == 0,
  "those feet are known BY CONSTRUCTION, so a failure there is the INSTRUMENT. "
  "C4/C5 went red on a door that had not moved and nothing reported it (F131)")

t("does every F-number cited by verify_clone.sh exist in the register?",
  all(("| **%s**" % f) in open('OPEN_FINDINGS.md').read()
      for f in set(re.findall(r'\bF\d{2,3}\b', open('verify_clone.sh').read()))),
  "verify_clone.sh justified its ONLY texture exemption with F115 while the "
  "register ran F1-F129 missing exactly F115 (F115).  A gate resting on a "
  "dangling citation is resting on nothing")

t("does visibility_budget.py still pick its scale frame by MTIME?",
  "getmtime" not in _code('visibility_budget.py'),
  "it takes the scale off whichever hero was rendered LAST, in an UNTRACKED "
  "directory, so the ranking that decides what counts as work depends on out/ "
  "mtimes -- 724 px/m today against 801 with a different newest frame (F132). "
  "THIS QUESTION IS EXPECTED TO FAIL UNTIL THE FRAME IS PINNED")

t("is F128's refuted SPREAD argument still marked as retracted?",
  "RETRACTED" in open('OPEN_FINDINGS.md').read().split("| **F128** |")[1][:400],
  "F128 called a 133x spread ratio DECISIVE, from two DIFFERENT instruments on "
  "the two photograph frames.  Under one consistent window the photograph's "
  "spread is the LARGER (F133).  If the mark goes, the retraction went with it")

t("is the ranked work list still named by README, START_HERE and the brief?",
  all(_rw in open(_f).read()
      for _rw in [_newest('REMAINING_WORK_rev*.md')]
      for _f in ('README.md', 'START_HERE.md',
                 _newest('NEXT_CONTEXT_PROMPT_rev*.md'))),
  "it declared itself a CARRIER and NO FILE in the repository named it for a "
  "whole revision -- which is how the standing-instructions carrier went at "
  "rev 44 and the open-findings register at rev 45 (rule 16)")

# =====================================================================
# REPLACED AT REV 61 (sec.10.5 -- a question that can no longer fail is not a
# control).  These six are about what REV 61 shipped and what it retracted.
# =====================================================================

_pn = open('probe_rev59_nose.py').read()
_i_red = _pn.find('not redm[v, ucol]')
_i_cream = _pn.find('not cream[v, ucol]')
t("does M1 still cross the lamp assembly before it looks for cream?",
  0 <= _i_red < _i_cream,
  "for two revisions M1 stopped on the headlamp's CHROME BEZEL -- bright and "
  "unsaturated, so `cream` is TRUE on it -- and returned ~1.18 lamp radii "
  "WHATEVER the paint did.  That is what refuted F106/F107 falsely.  If this "
  "walk loses its red-paint step the gate goes blind again (F134).  THIS ROW "
  "IS STRUCTURAL, NOT BEHAVIOURAL, AND THAT IS ITS CEILING: it asserts the "
  "red-paint walk appears BEFORE the cream walk, so it catches deletion and "
  "reordering but NOT a disarmed loop condition.  A first cut grepped only for "
  "the symbol and survived `while False and not redm[...]` -- watched")

t("does M1 still PRINT the bezel-ruled figure beside its lens-ruled one?",
  'BEZEL-RULED' in open('probe_rev59_nose.py').read(),
  "M1's ruler is the LENS interior; F75's bar is RIM-ruled and F75 says that "
  "1.19 conversion CANNOT BE CHECKED.  Rev 61 quoted M1's PASS as 'item B "
  "fixed' for one commit.  Without the like-for-like figure printed beside it, "
  "that misreading is one grep away from happening again (F136)")

t("is C8, the scale-stable emblem statistic, still armed and still failing?",
  'cell_elongation' in open('probe_rev46_vw.py').read()
  and 'C8' in open('probe_rev46_vw.py').read(),
  "C6 counts CELLS and F105 showed that count is not scale-stable; F139 showed "
  "its target of 7 is CONTAMINATED by a cell lying entirely inside the ring "
  "band.  C8 measures cream-cell ELONGATION -- built 1.49, a plain CROSS 1.39, "
  "photograph 3.39.  It is the only instrument that measures what the owner "
  "actually reports (F137)")

t("is C9's kill still the SYNTHETIC pair, not the W-collapse ablation?",
  '_bars' in open('probe_rev46_vw.py').read()
  and '_cross' in open('probe_rev46_vw.py').read(),
  "C9's first cut used the W-collapse ablation and moved C8 only 1.49 -> 1.56. "
  "A 0.07 margin is a coincidence waiting to happen, not a control.  The "
  "synthetic pair -- a plain cross and six parallel bars -- has an answer known "
  "BY CONSTRUCTION (1.39 and 10.71)")

t("can the owner's Senor ruling still be undone behind a passing checksum?",
  'S_bridge' in open('senor_trace.py').read()
  and 'the S is ONE letter' in open('verify_clone.sh').read(),
  "the owner ruled the word must read 'clearer than the photo, well defined'. "
  "IoU against the TARNISHED mask FALLS when the letter is restored (0.8859 -> "
  "0.8602) and MUST NOT be 'repaired'.  The checksum re-base is licensed only "
  "by the companion row that counts the S's CONNECTED COMPONENTS off the raster")

t("does judge_set.sh still exist, so photorealism is judged WITH the optics?",
  os.path.exists('judge_set.sh')
  and '--backdrop headroom' in open('judge_set.sh').read(),
  "post.py implements bloom -> CA -> vignette -> grain, defaults every gain to "
  "0.0, and the preview path never called it -- so SIXTY revisions of fidelity "
  "judgement were made on raw frames, and a photography panel scored optics "
  "1/10 on that alone.  --backdrop headroom is REQUIRED or the vignette and "
  "grain do not render at all (F146)")

# ===========================================================================
#  REV 62's QUESTIONS.  Rule 10.5: REPLACE these each revision -- a question
#  that can no longer fail is not a control.  Every one below is about a claim
#  REV 62 published, and every one can go red.
# ===========================================================================

t("does C8's target still get SWEPT, or is it a single unguarded window again?",
  os.path.exists('probe_rev62_landmarks.py')
  and 'C11' in open('probe_rev62_landmarks.py').read()
  and 'crop-window sweep' in open('probe_rev62_landmarks.py').read(),
  "cell_elongation inscribes its measuring disc in THE MASK ARRAY'S RECTANGLE, "
  "not in the badge.  At +-3 px of crop the disc escapes the roundel, the nose "
  "paint outside the ring becomes a 479 px 'cream cell' against the true "
  "cells' 215, and the target reads 1.553 against the BUILT glyph's 1.49 -- "
  "i.e. the owner's top defect reads CLOSED and nothing fires.  C1 sweeps five "
  "windows for L1-L6; this target was swept by NOTHING for two revisions "
  "(F151).  THIS ROW IS EXPECTED TO SHOW C11 FAILING -- that failure IS the "
  "finding, and if C11 ever passes without the disc being re-derived from the "
  "badge's own fitted ellipse, someone relaxed it")

t("is the point 2.27x still absent, i.e. is C8's verdict still quoted as a RANGE?",
  '1.99' in open('LEDGER_rev62.md').read()
  and 'RANGE' in open('LEDGER_rev62.md').read().upper(),
  "four documents published 'the built cells are 2.27x too round' as a POINT.  "
  "Swept over its own window and segmentation the target is 2.969..3.415, so "
  "the honest figure is 1.99x..2.27x.  If the range collapses back to a point "
  "in any outgoing document, the ceiling was dropped and only the headline "
  "survived -- which is how this project has lost figures before (F151)")

t("is the stroke-weight lever still recorded as REFUTED against C8?",
  'F152' in open('OPEN_FINDINGS.md').read()
  and 'REFUTED-rev62' in open('OPEN_FINDINGS.md').read(),
  "F102 swept T1_VW_WFRAC and called it inert -- against C6, THE COUNT.  C8 "
  "did not exist then.  Ablated against C8 it moves 1.07..1.82 and moves the "
  "WRONG WAY, and thinning to the construction's limit reaches 1.82 against "
  "3.39.  So abandoning L6 ENTIRELY cannot reach the target and L6 IS NOT THE "
  "ANSWER (F152).  If this row goes, the next context re-tries the thinning "
  "exactly as rev 62 nearly did")

t("can the owner's rev-62 Senor ruling be undone behind a passing checksum?",
  'SENOR_TARNISH' in open('script_gen.py').read()
  and 'T1_SENOR_TARNISH=1 restores' in open('verify_clone.sh').read(),
  "he was shown the figure and chose 'bright silver, same as Tacombi', which "
  "OVERRIDES SPEC sec.3's WEATHERED lock for that word (F157).  The hash "
  "re-base is licensed ONLY by the companion row asserting that "
  "T1_SENOR_TARNISH=1 reproduces the PRE-RULING texture byte for byte.  "
  "Without that row the re-base is a rubber stamp and the measured TARNISH_K "
  "and SENOR_MICHELSON are unreachable")

t("is F156's trap still flagged -- that the Senor gate row now scores a DEPARTURE?",
  'F156' in open('OPEN_FINDINGS.md').read()
  and 'DELIBERATE DEPARTURE' in open('OPEN_FINDINGS.md').read(),
  "flank_compare's `Senor` row IMPROVED -- ink 973 -> 1488 against a reference "
  "1261, of-ceiling 0.717 -> 0.751, crossing its 0.75 bar -- BY MOVING AWAY "
  "FROM THE PHOTOGRAPH, because the owner ruled a departure from it.  A "
  "revision reading that as convergence is wrong; one 'fixing' the 118 % "
  "overshoot undoes an owner ruling.  Rev 62 did NOT re-base the row and said "
  "so (F156)")

t("does probe_rev62_landmarks still LIFT its ruler rather than re-type it?",
  'ast.parse' in open('probe_rev62_landmarks.py').read()
  and 'probe_rev46_vw.py' in open('probe_rev62_landmarks.py').read(),
  "the cross-frame landmark comparison is only meaningful if both sides use "
  "the SAME definition of a landmark.  The probe lifts runs_of/transitions/"
  "landmarks/cell_elongation SOURCE TEXT out of probe_rev46_vw.py with ast at "
  "run time, and C0w asserts the lift reproduces that probe's published nolita "
  "figures to 0.00003.  If someone re-types those functions the two rulers "
  "drift silently and every delta in F153 becomes meaningless")

# ---------------------------------------------------------------------------
# REPLACED AT REV 63 (§10.5 -- a question that can no longer fail is not a
# control).  These six are about what REV 63 shipped, refuted and half-built.
# The rev-62 batch above them is the next one to replace.

t("is the emblem gate's INSUFFICIENCY still on the record, with its counterexample?",
  'F175' in open('OPEN_FINDINGS.md').read()
  and os.path.exists('probe_rev63_shapefit.py'),
  "rev 63 found constants scoring 7 cells, elongation 3.322 and IoU 0.5363 -- "
  "C6 PASS, C8 PASS, IoU up -- that render on the nose as a Y-shaped trident "
  "WORSE than the X they replaced.  If this row goes, the next context reads a "
  "green C6+C8 as evidence the emblem is right, which is exactly the mistake "
  "that has kept the owner's top item open.  The probe is kept so the "
  "refutation is REPRODUCIBLE and not just asserted (F175, rule 41)")

t("is C7 still recorded as a PRECONDITION on C6 rather than a peer of it?",
  'F176' in open('OPEN_FINDINGS.md').read()
  and 'PRECONDITION' in open('OPEN_FINDINGS.md').read(),
  "at F175's constants probe_rev46_vw.py prints '[FAIL] C7 KILL: ... moves the "
  "cell count 7 -> 7'.  A kill that cannot go red is not a control (rule 3), "
  "so C6's simultaneous PASS is worthless there.  Nobody had driven the gate "
  "into the region where its own alarm fires.  Read the kill BEFORE the pass "
  "(F176, rule 42)")

t("are the TWO stroke-weight constants still distinguished by value?",
  "NOSE stroke weight is 0.1800" in open('verify_clone.sh').read()
  and "HUBCAP stroke weight is 0.2087" in open('verify_clone.sh').read(),
  "the NOSE roundel's weight is vw_logo_fit()'s wfrac SIGNATURE DEFAULT; the "
  "HUBCAP's is CAP_EMBLEM_WFRAC; and T1_VW_WFRAC overrides the NOSE one ONLY, "
  "so every weight sweep in this project's history -- F152's included -- has "
  "been driving the nose.  Rev 63 wrote a nose-fitted value into the hubcap "
  "constant and the gate read 6 cells / 2.659 where the search had read "
  "7 / 3.322.  Neither was checked BY VALUE by anything before rev 63 (F178)")

t("is the canonical vector still marked as a DIFFERENT OBJECT, and not named ref_*?",
  os.path.exists('vw_canonical_2019.svg')
  and not os.path.exists('ref_vw_canonical.svg')
  and 'F168' in open('OPEN_FINDINGS.md').read(),
  "the 2019 redraw reads 3 cells / elongation 1.597 against the photographed "
  "badge's 7 / 3.390 AT AN IDENTICAL RASTER: its V does not touch its W and "
  "its legs stop short of the ring, and the pressing has both.  A ref_ prefix "
  "would invite the next context to treat it as a reference frame OF THE BUS, "
  "which is the exact rule-11 error it exists to document (F168)")

# RETIRED AT REV 64, IN PLACE, WITH ITS CAUSE NAMED RATHER THAN DELETED.
# This asked whether the traced-pressing route was still flagged UNFINISHED.
# Rev 64 finished it, meshed it, rendered it and REFUTED it, so the question
# can no longer mean what it meant -- and worse, its own text repeated the
# rev-63 brief's diagnosis, "the disagreement is the RING (0.508), not the
# glyph (interior 0.78)", which was NEVER IN THE PROBE and is FALSE: both
# figures were one 9 % scale error in raster() (F186).  Because the mechanical
# half of rule 15 repeated the same unbacked number, it could never have caught
# it -- which is the argument for running a REAL adversary, not this file.
# Replaced by the rev-64 batch below; the successor is "is the traced pressing
# still flagged as REFUTED and OFF?".
t("is the rev-63 trace route's FALSE ring diagnosis still retracted?",
  '0.508' not in open('PASTE_INTO_CLAUDE_CODE.txt').read()
  and 'ctl("T3b"' in open('probe_rev63_trace.py').read(),
  "The 0.508/0.78 pair was prose in three documents and in THIS FILE's own "
  "question text, and in no probe.  Measured: the ring reads 0.6758 and no "
  "concentric annulus beats it, and the glyph reproduces at 0.9496 once both "
  "sides share a ruler.  If that number returns to the brief, the next context "
  "will re-diagnose a rasteriser bug as a defect of the trace (F186, rule 38)")

t("does the construction-ablation result still stand against F137?",
  'F174' in open('OPEN_FINDINGS.md').read()
  and os.path.exists('probe_rev63_ablate.py'),
  "F137 said no spine arrangement can satisfy the photograph's cell shape.  A "
  "24000-point ablation over SEVEN spine constants AND the stroke width jointly "
  "reaches elongation 6.877 AT 7 CELLS -- twice the photograph's 3.390.  The "
  "construction was never the ceiling, so a revision that goes looking for a "
  "topology fix is spending itself on a refuted premise (F174, rule 36)")


# ===================================================================== rev 64
# The rev-63 batch above is now HISTORY -- rev 64 built its half-built route,
# rendered it and refuted it, and the "diagnosis is done: the RING (0.508)"
# that its last question repeats turned out NOT TO BE IN THE PROBE AT ALL
# (F186).  These six are about what REV 64 measured, refuted and left open.

t("is the traced pressing still flagged as REFUTED and OFF?",
  'F183' in open('OPEN_FINDINGS.md').read()
  and 'T1_VW_TRACED' in open('t1_core.py').read()
  and os.path.exists('vw_pressing.py'),
  "The rev-64 brief's TOP item was to put the traced pressing in the mesh.  It "
  "went in, it WON on cells (7 vs 6), on elongation and on IoU (0.7487 vs "
  "0.6049) -- and it RENDERS AS AN UNRECOGNISABLE BLOB.  A context that reads "
  "the table and not the crop would ship it.  T1_VW_TRACED must stay OFF")

t("do C6 and C8 still carry F184's warning?",
  os.path.exists('probe_rev64_shear.py')
  and 'F184' in open('OPEN_FINDINGS.md').read(),
  "A PURE SHEAR of the glyph already in the tree -- no constant, no spine, no "
  "shape change -- carries cells 6 -> 8 and elongation 2.388 -> 3.853.  C8's "
  "3.390 target and C6's 7 BOTH lie inside that.  Quoting either as a fidelity "
  "target without saying so is steering by a viewing angle (rule 39, rule 43)")

t("is the ring-ellipse fit still named as the emblem's close?",
  'F185' in open('OPEN_FINDINGS.md').read()
  and 'ELLIPSE' in open('PASTE_INTO_CLAUDE_CODE.txt').read().upper(),
  "The badge's ring is a CIRCLE on the real object, so its image gives the "
  "homography outright and every emblem target could be re-read on the mark "
  "instead of on a photograph of it.  Nothing in this project has ever fitted "
  "it.  Drop this and the item goes back to tuning against sheared targets")

t("does the record still say rev 63's constants SHIPPED?",
  'RETRACTED AT REV 64' in open('EMBLEM_HANDOFF.md').read(),
  "EMBLEM_HANDOFF.md is the carrier for the top item and its SS5b.2 said 'No "
  "constant in t1_core.py was changed ... and that is a control' for a whole "
  "revision while the tree carried all six.  F170 still said 'DO NOT ship'.  "
  "Rule 13 undischarged.  If that retraction is smoothed away the carrier "
  "contradicts the tree again (F190)")

t("is T3's registration repair still held by a kill?",
  'ctl("T3d"' in open('probe_rev63_trace.py').read(),
  "T3's 0.6504 was a RASTERISER defect -- the trace drawn 9.1 % too big -- not "
  "a trace defect (F186).  Registered it reads 0.9496.  T3d goes red if the "
  "registration is removed.  Without that kill the same 0.30 of IoU can be "
  "lost again and read as a defect of the trace, which is what happened once")

t("are rev 64's two owner rulings still in a live carrier?",
  all(k in open('OPEN_FINDINGS.md').read()
      for k in ('Keep holding', 'large-format print')),
  "He REAFFIRMED the delivery hold against a revision that could have shipped, "
  "and he ruled he needs LARGE-FORMAT print over the 3840 default.  A ruling "
  "in no carrier is exactly how this project lost the Playa hero for six "
  "revisions and then published the misattribution for seven more (F92, F188)")


P("-" * 78)
P("  %d asked, %d BROKE%s" % (NQ[0], len(bad),
                              ("  --  " + "; ".join(bad)) if bad else ""))
P("  A question that can no longer fail is not a control.  The last SIX were")
P("  REPLACED at rev 64 and are about what REV 64 measured, refuted and left")
P("  open; the rev-63 batch above them is the next one to replace.")
sys.exit(1 if bad else 0)


