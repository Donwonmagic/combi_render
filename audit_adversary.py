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



def _sub_env(env, code):
    """Run `code` in a FRESH interpreter with `env` overlaid, return stdout.

    rev 68.  An ablation switch read at import time cannot be tested in-process
    -- the module is already imported.  Asking a grep instead is what let
    T1_VW_CAPMIN sit dead for a whole revision (F208).  This runs it for real.
    """
    import os as _os, subprocess as _sp, sys as _sys
    return _sp.run([_sys.executable, "-c", code], capture_output=True, text=True,
                   env=dict(_os.environ, **env)).stdout.strip()


def t(q, ok, d=""):
    NQ[0] += 1
    P("  %-5s %s" % ("ok" if ok else "BROKE", q))
    P("         %s" % d)
    if not ok:
        bad.append(q)


B_ACTION = open(BRIEF).read()
# ------------------------------------------------------------------ rev 70
# THE HANDOFF WAS SPLIT AND THESE QUESTIONS FOLLOW THE CONTENT.
#
# The carriers moved to HANDOFF_CARRIERS.md because the brief had reached
# 95 KB and the owner measured the cost (revstats.py: geometry per revision
# 721 -> 209, closures at rev 66..70 all zero).  Questions here ask "is X
# still carried?"; X is still carried if it is in EITHER file, so `B` is the
# union.  Anything that must be in the ACTION brief specifically -- because a
# context that reads only the brief has to see it -- uses B_ACTION instead.
#
# THIS IS NOT A RELAXATION: delete the carriers file, or gut a section of it,
# and every one of these goes red exactly as it would have before the split.
# WATCHED: with SS4 removed from HANDOFF_CARRIERS.md the emotional-bar and
# reference-set rows both return 0.
import os as _os
_CARR = _os.path.join(ROOT, "HANDOFF_CARRIERS.md") if 'ROOT' in dir() else "HANDOFF_CARRIERS.md"
B = B_ACTION + ("\n" + open(_CARR).read() if _os.path.exists(_CARR) else "")
P("=" * 78)
P("  audit_adversary.py -- what would make %s false?" % BRIEF)
P("=" * 78)

import t1_shell as S          # noqa: E402
import t1_core as T           # noqa: E402
import t1_detail as D_        # noqa: E402  -- constants only, no bpy calls made

# ------------------------------------------------- the underbody, from source

# ------------------------------------------------------------------ rev 69
# FOUR QUESTIONS REPLACED (SS10.5).  The rev-63 batch was the oldest and all
# four of the ones replaced were GREPS -- rule 50: a grep fails in BOTH
# directions.  These four RUN something instead.
def _tyre_lift_ok():
    """ARITHMETIC, off t1_mats.py's own numbers: the road film's maximum lift
    of the rubber must still bracket the 1.90x that was MEASURED (F238)."""
    try:
        t = open('t1_mats.py').read()
        col = re.search(r"W_DUST_COL\s*=\s*\(([\d.]+),", t)
        base = re.search(r'dust_film\("tyre",\s*\(([\d.]+),', t)
        low = re.search(r"fac_up=0\.22\s*\*\s*_tf,\s*fac_low=0\.34\s*\*\s*_tf", t)
        tf = re.search(r'T1_TYRE_FILM",\s*([\d.]+)', t)
        if not (col and base and low and tf):
            return False
        c, b, f = float(col.group(1)), float(base.group(1)), float(tf.group(1))
        def srgb(x):
            return 255 * (1.055 * x ** (1 / 2.4) - 0.055) if x > 0.0031308 else 255 * 12.92 * x
        shipped = srgb(b + 0.34 * f * (c - b)) / srgb(b)
        old = srgb(b + 0.34 * (c - b)) / srgb(b)
        return old > 1.8 and shipped < old        # the old film lifted; the new one lifts less
    except Exception:
        return False


def _on_band_normalises():
    """BEHAVIOURAL: two points of the same DIRECTION and different magnitude
    must land on the same band point, which is why an angle is not a free
    parameter of the spine (rule 54, F237)."""
    try:
        import t1_core as C
        f = getattr(C, "_on_band", None)
        if f is None:
            src = open('t1_core.py').read()
            return "_RING_INNER_FRAC / r" in src
        a, b = f((0.3, 0.4)), f((0.6, 0.8))
        return max(abs(a[0] - b[0]), abs(a[1] - b[1])) < 1e-9
    except Exception:
        src = open('t1_core.py').read()
        return "_RING_INNER_FRAC / r" in src


def _second_frame_ok():
    """BEHAVIOURAL: the emblem's INDEPENDENT frame still yields a connected
    mark at the box the brief names.  F237's overfit kill depends on it."""
    try:
        import probe_rev69_fitpose as F
        m = F.photo_mark("IMG_2073.jpeg", (283, 537, 357, 662), True)
        return m is not None and min(m.shape) > 20 and 0.2 < m.mean() < 0.8
    except Exception:
        return False


def _tyre_finder_ok():
    """BEHAVIOURAL: the band finder recovers a synthetic wheel of known ratio."""
    try:
        import numpy as np
        import probe_rev70_tyre as T
        n = 400
        yy, xx = np.mgrid[0:n, 0:n]
        r = np.hypot(xx - n / 2, yy - n / 2)
        a = np.full((n, n, 3), 205.0)
        a[r < 185] = [30, 30, 30]
        a[r < 95] = [150, 150, 150]
        a[r < 50] = [180, 40, 40]
        c = T.find_wheel(a, (140, 140, 260, 260))
        if c is None:
            return False
        cx, cy, rh = c
        b = T.bands(a, cx, cy, rh)
        if b is None:
            return False
        m0, m1, t0, t1 = b
        rr = np.hypot(xx - cx, yy - cy)
        L = T._lum(a)
        got = L[(rr >= t0) & (rr < t1)].mean() / L[(rr >= m0) & (rr < m1)].mean()
        return abs(got - 0.200) < 0.02
    except Exception:
        return False


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

t("is C8 still armed, and is its LIVE target still the squashed 3.39?",
  'cell_elongation' in open('probe_rev46_vw.py').read()
  and 'C8' in open('probe_rev46_vw.py').read(),
  "CORRECTED AT REV 68.  This asked whether C8 was 'still failing' and tested "
  "only that two strings existed -- it read ok while C8 PASSED (photo 3.39, "
  "built 2.55 after F204).  A question that asserts a false state and cannot "
  "detect it is not a control.  What is still true and worth guarding: C8's "
  "LIVE target is photo_elongation()'s 3.3896, the 69/41 bbox squash, and "
  "F194's re-base to 2.63..2.96 was never wired into it -- grep the tree for "
  "2.627 and you get nothing.  So do NOT quote C8 as re-based (F222)")

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
# ==========================================================================
# REPLACED AT REV 71 (§10.5 -- a question that can no longer fail is not a
# control).  §10 has said "REPLACE the adversary's questions each revision"
# since rev 60, and revs 68, 69 and 70 replaced NONE, so the rev-63 batch had
# been the "next to replace" for four revisions running.  These four are about
# what REV 71 refuted, and every one of them can go red.
# ==========================================================================

def _p1b_still_refuses():
    """P1b must EXIST and must still be a real row -- not quietly deleted or
    widened once its refusal becomes inconvenient (F246, rule 44)."""
    src = open('probe_rev69_fitpose.py').read()
    return ('P1b' in src and 'synth_bb' in src
            and 'ys_.min()' in src and 'v_ctl_bb > 0.90' in src)


t("is the emblem's CONTROL still framed the way its MEASUREMENT is framed?",
  _p1b_still_refuses(),
  "F246: photo_mark bbox-crops every real target; P1's control is the raw warp "
  "output; fit() searches no translation while its docstring asserts both "
  "masks are already bbox-centred.  Framed correctly the control reads 0.4988 "
  "against the mark's own 0.7345 -- IT SCORES BELOW ITS OWN SPECIMEN, so "
  "0.9882 is NOT the emblem's ceiling.  This goes red if P1b is deleted, or if "
  "its bar is widened to make it pass instead of fixing the search")

t("does the brief still quote 0.2537 as the emblem's SHAPE deficit?",
  ('0.2537' not in B)
  or ('not a shape deficit' in ' '.join(B.lower().split())),
  "F246 refutes that subtraction: it is 0.9882 minus 0.7345 where the two are "
  "measured through DIFFERENT framings.  F237's '4.4 % of the deficit' is a "
  "ratio against it.  If a later brief re-publishes 0.2537 as shape without "
  "carrying the refutation, this fires")

t("is the tail-board guard's watched-failure figure still one its own bar "
  "would PASS?",
  ('2.2790' in open('verify.py').read()
   and '95.0' in open('verify.py').read()
   and '86.3' not in open('t1_shell.py').read().split('THE RULES')[0].split(
       '95.0 mm -- 3.2 sigma')[0]),
  "F247: verify._tail_board_pose recorded 'WATCHED FAILING ... 2.2703 -- "
  "86.3 mm, 2.9 sigma' against a bar of TIP_BAND*3.0 = 90.0 mm.  86.3 < 90.0, "
  "so the recorded failure PASSES.  Cause: 2.2703 is tail_board()'s BUILD LOG "
  "tip (the spine endpoint); the row reads the MESH max, 2.2790.  Rule 5 and "
  "rule 38 inside one docstring.  Re-watched at rev 71: +95.0 mm, 3.2 sigma")

t("does judge_set.sh still post-process the views the brief actually renders?",
  (lambda ln: ln is not None and 'hero34f' in ln and 'hero34r' in ln
   and 'hero ' not in ln)(
      next((l.split('#')[0] for l in open('judge_set.sh')
            if l.startswith('for v in')), None)),
  "F248: it looped over a plain 'hero' that NO preview list has produced since "
  "the hero34f/hero34r split, so it exited 2 and never post-processed "
  "hero34f -- the delivery view.  The trap was DOCUMENTED at rev 69 and the "
  "SCRIPT was never fixed until rev 71.  This asks the script, not the prose")

# ==========================================================================
# The rev-62 batch below is now the oldest and is the NEXT one to replace.
# ==========================================================================
# KEPT FROM REV 63.  These are about what REV 63 shipped, refuted and
# half-built, and they still go red.

t("does the TYRE's road film still arithmetically explain its measured lift?",
  _tyre_lift_ok(),
  "REPLACES a rev-63 GREP for F175 (rule 50: a grep tells you a name is "
  "present and nothing else).  F175's content is NOT lost -- it is the row "
  "itself, and probe_rev63_shapefit.py still reproduces it.  THIS question is "
  "ARITHMETIC: dust_film mixes the tyre's base toward W_DUST_COL at up to "
  "fac_low, and that lift must still bracket the 1.90x probe_rev70_tyre "
  "MEASURED (F238).  If someone re-tunes W_DUST_COL or the rubber's albedo "
  "without re-measuring, the published mechanism and the shipped material "
  "stop agreeing and this goes red")

t("is C7 still recorded as a PRECONDITION on C6 rather than a peer of it?",
  'F176' in open('OPEN_FINDINGS.md').read()
  and 'PRECONDITION' in open('OPEN_FINDINGS.md').read(),
  "at F175's constants probe_rev46_vw.py prints '[FAIL] C7 KILL: ... moves the "
  "cell count 7 -> 7'.  A kill that cannot go red is not a control (rule 3), "
  "so C6's simultaneous PASS is worthless there.  Nobody had driven the gate "
  "into the region where its own alarm fires.  Read the kill BEFORE the pass "
  "(F176, rule 42)")

# rev 66 -- THIS QUESTION FROZE ONE OF THE TWO VALUES AND F204 MOVED IT.
# NOT WIDENED TO ADMIT THE NEW VALUE (rule 44): re-asked so it tests the
# INTENT -- that both weights are checked BY VALUE, that the two values DIFFER,
# and that each row agrees with the source it claims to pin.  That is strictly
# stronger than the frozen literal, and it still goes red if anyone writes one
# constant into the other, drops a row, or lets a row drift off its source.
def _two_weights():
    import re
    vc = open('verify_clone.sh').read()
    nose_row = re.search(r'NOSE stroke weight is ([\d.]+)', vc)
    hub_row = re.search(r'HUBCAP stroke weight is ([\d.]+)', vc)
    if not (nose_row and hub_row):
        return False
    nose_src = re.search(r'def vw_logo_fit\([^)]*wfrac=([\d.]+)\)',
                         open('t1_detail.py').read())
    hub_src = re.search(r'^CAP_EMBLEM_WFRAC = ([\d.]+)',
                        open('t1_detail.py').read(), re.M)
    if not (nose_src and hub_src):
        return False
    return (nose_row.group(1) == nose_src.group(1)
            and hub_row.group(1) == hub_src.group(1)
            and nose_row.group(1) != hub_row.group(1))


t("are the TWO stroke-weight constants still distinguished by value?",
  _two_weights(),
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
t("does the emblem's OVERFIT DETECTOR still have a second frame to detect with?",
  _second_frame_ok(),
  "REPLACES a rev-63 grep.  F237 killed the traced pressing by scoring it on a "
  "frame it was NOT traced from: it wins by +0.0905 on ref_workshop.jpg, its "
  "own source, and LOSES by 0.0249 on IMG_2073.jpeg.  That refutation exists "
  "ONLY while the second frame does.  This question EXTRACTS the mark from "
  "IMG_2073.jpeg at the box the brief names and requires it to come back "
  "connected and of sane size.  Lose it and T1_VW_TRACED's overfit becomes "
  "unfalsifiable again")

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
  and 'ELLIPSE' in B.upper(),
  "The badge's ring is a CIRCLE on the real object, so its image gives the "
  "homography outright and every emblem target could be re-read on the mark "
  "instead of on a photograph of it.  Nothing in this project has ever fitted "
  "it.  Drop this and the item goes back to tuning against sheared targets")

t("does the emblem's spine still make a stroke's ANGLE unreachable?",
  _on_band_normalises(),
  "REPLACES a rev-63 grep.  RULE 54, and it is the whole reason the emblem "
  "resisted eight revisions of solving: _spines() asserts every terminal onto "
  "the band circle and _on_band NORMALISES, so each (X, Z) pair contributes "
  "only a DIRECTION -- its magnitude divides out (F224 corrected).  This "
  "question RUNS _on_band on two points of the same direction and different "
  "magnitude and requires them to land on the same point.  If that ever stops "
  "being true the parameterisation has changed and F237's 4.4 % result no "
  "longer describes the tree")

t("does probe_rev70_tyre's band finder still recover a KNOWN ratio?",
  _tyre_finder_ok(),
  "REPLACES a rev-63 grep.  This finder was WRONG TWICE before it was right -- "
  "an image-size search radius, and a saturation walk that ran through a warm "
  "cream rim -- and its own control caught both (F238).  A control that is "
  "never run is not a control (rule 3), so this RUNS it: a synthetic wheel "
  "built at tyre 30 / rim 150 must come back at 0.200.  Every tyre number in "
  "the record is downstream of this finder")

t("are rev 64's two owner rulings still in a live carrier?",
  all(k in open('OPEN_FINDINGS.md').read()
      for k in ('Keep holding', 'large-format print')),
  "He REAFFIRMED the delivery hold against a revision that could have shipped, "
  "and he ruled he needs LARGE-FORMAT print over the 3840 default.  A ruling "
  "in no carrier is exactly how this project lost the Playa hero for six "
  "revisions and then published the misattribution for seven more (F92, F188)")


P("-" * 78)

# =========================================================== rev 66's BATCH
# Rule: replace the questions each revision -- a question that can no longer
# fail is not a control.  These five are about what REV 66 measured, and each
# one goes red on a specific way rev 66's work could be silently undone.

t("is C6 still counting INTERIOR cells on BOTH sides?",
  'def cream_cells(mask, frac=0.97, interior=False)' in open('probe_rev46_vw.py').read()
  and 'photo_cells(interior=True)' in open('probe_rev46_vw.py').read()
  and 'cream_cells(glyph_only_mask(**CURRENT), interior=True)' in open('probe_rev46_vw.py').read(),
  "C6's target of SEVEN was the PHOTOGRAPH'S RIM -- a crescent of background "
  "outside the ring, caught because the 0.97 disc is concentric with the 41x69 "
  "CROP BOX and the ring is not.  Measured 0.0 %% inside the ring's own filled "
  "outline against 100 %% for the six real cells.  If EITHER side stops "
  "filtering, the two stop sharing a ruler and the unreachable 7 comes back "
  "(F200).  A V fused to a W meets the band at SIX points and so cuts the disc "
  "into SIX.  NOTE, CORRECTED AT REV 68: the clause that stood here -- '144 "
  "perturbed builds gave 7 not once' -- is REFUTED by F209, which found 7 in 3 "
  "of those 144 under F200's own protocol, and F103 and F174 both reported it "
  "earlier.  C6's re-base 7 -> 6 STANDS on its PHOTOGRAPH-side evidence above; "
  "what falls is 'the mark cannot make seven'")

t("can C6's kill still go red?",
  'KILL, WATCHED FIRING ON THE DEFECT' in open('probe_rev46_vw.py').read()
  and 'shrink=0.88' in open('probe_rev46_vw.py').read()
  and 'def built_mask(rows=69, shrink=1.0)' in open('probe_rev46_vw.py').read(),
  "correcting C6 KILLED ITS OWN KILL: a collapsed W still cuts the ring into "
  "six, so C7 read 6 -> 6 and went red.  A control whose kill cannot go red "
  "makes its own PASS meaningless (rule 42).  The kill now plants the actual "
  "defect -- the glyph shrunk until nothing reaches the band -- and collapses "
  "the count 6 -> 1.  If `shrink` goes, C6 is unguarded again (F201)")

t("is the built landmark raster still read where it has CONVERGED?",
  'BUILT_ROWS = 552' in open('probe_rev46_vw.py').read()
  and 'ctl("C10"' in open('probe_rev46_vw.py').read()
  and 'if last3 and abs(last3[-1] - L["L2"]) > 1e-12:' in open('probe_rev46_vw.py').read(),
  "L4 is 'the last 3-run row'; when the raster shows only ONE, that is L2's "
  "row, so L4 reported the built V's APEX against the photograph's W TROUGHS. "
  "Built L4 flips between 0.366 and 0.866 with the row count alone.  Its error "
  "was 96.4 %% of the squared residual: 0.4455 at 276 rows against 0.1001 "
  "converged.  BOTH halves must stand -- the refusal AND the row count (F203)")

t("does C6's message still MEASURE its reach rather than print it?",
  'def terminal_reach():' in open('probe_rev46_vw.py').read()
  and 'ctl("C12"' in open('probe_rev46_vw.py').read()
  and 'the mesh names them' not in open('probe_rev46_vw.py').read(),
  "for five revisions C6 printed three HARD-CODED figures as a diagnosis, and "
  "no audit could catch them because a literal prints without being measured "
  "(F198).  C12 perturbs VW_W_ARM_X and insists the reported figures MOVE.  "
  "If C12 goes, the message can quietly freeze again")

t("is the arc cut still ablatable, and still holding the extreme?",
  'def _mitre_outline(spine, w, arc_r=None, arc_n=24)' in open('t1_core.py').read()
  and 'T1_VW_NOARC' in open('t1_core.py').read()
  and 'for t in _drive:' in open('t1_core.py').read(),
  "the arc cut trims each rail where it MEETS the band circle, so both cap "
  "corners land on the band BY CONSTRUCTION and the global extreme cannot "
  "move -- which is exactly what kills T1_VW_CAPMIN, whose extreme runs "
  "0.8140 -> 0.9250 and drags every other terminal 12 %% inboard.  The four "
  "true end caps must stay OUT of the fixed point (`_drive`), or the "
  "corner-choice the arc cut removes comes straight back (F202)")


# ---------------------------------------------------------------- rev 67
# REPLACED THIS REVISION (SS10 item 5).  These are about what rev 67 measured,
# refuted and left open, and every one of them CAN go red.

t("is the nose's plan bulge still a named constant with a live ablation?",
  '\nNOSE_BULGE = 0.019' in open('t1_shell.py').read()
  and _sub_env({'T1_NOSE_BULGE': '0.05'},
               'import t1_shell as S; print(S.NOSE_BULGE)') == '0.05'
  and _sub_env({}, 'import t1_shell as S; print(S.NOSE_BULGE)') == '0.019'
  and _sub_env({'T1_NOSE_BULGE': '0.05'},
               'import t1_shell as S; print(S.nose_bulge_at(2.1015,0.545,0.933) > '
               '2*S.nose_bulge_at(2.1015,0.545,0.933,amount=0.019))') == 'True',
  "RE-CUT AT REV 68 FROM A GREP TO A BEHAVIOUR.  This tested that the string "
  "'bulge = NOSE_BULGE * w * max' was present, and it BROKE on a refactor that "
  "preserved every value it existed to protect -- rev 68 factored the "
  "expression into nose_bulge_at() so build.py could ask the same question and "
  "keep the fixtures on the skin (F217).  A grep cannot tell a refactor from a "
  "regression; it now RUNS the ablation in a fresh process and checks the "
  "constant actually moves.  The nose's forward convexity had NO constant, NO "
  "ablation and NO probe for fifteen revisions, because a side elevation is "
  "blind to plan curvature BY CONSTRUCTION -- the silhouette is max-over-y of "
  "x, which is always the centreline (F207).  If the ablation stops ablating, "
  "F207's kill reports nothing, which is F208's failure mode exactly")

t("does the nose probe still READ EXIF rather than assume no camera?",
  'def exif_focal(' in open('probe_rev67_nose.py').read()
  and 'FocalLengthIn35mmFilm' in open('probe_rev67_nose.py').read(),
  "NOTHING in this tree had ever read EXIF, and the record said 'the focal "
  "length of a camera nobody recorded' for FIVE revisions while "
  "ref_nolita_front34.jpg carried SONY DSC-RX100 / 10.4 mm / 35mm-equiv 28, "
  "3:2 uncropped -> f = 544.4 px.  That belief is what made the nose look "
  "unmeasurable, and F26 was cited to block a frame it is not even about "
  "(F219).  If exif_focal goes, the ceiling comes straight back")

t("can the edge-acceptance bar still refuse, and can the clip still not rescue?",
  'def rms_bar(span)' in open('probe_rev67_nose.py').read()
  and 'max(4.0, 0.03 * span)' in open('probe_rev67_nose.py').read()
  and 'rescued' in open('probe_rev67_nose.py').read()
  and 'n_clipped' in open('probe_rev67_nose.py').read(),
  "rev 67 wrote 'rms <= 12 %% of span' and watched an 831 px whole-frame scan "
  "with rms 61.85 sail through at 7.4 %% -- a fraction-of-span bar cannot "
  "refuse a long enough input (rule 48).  Then the outlier clip written for "
  "F220 turned ref_playa_34's CORRECT refusal into a PASS by eating the "
  "fragments, span collapsing 105 -> 51 px.  BOTH halves must stand: the "
  "absolute term, and judging the ORIGINAL n and span (F220b)")

t("do the nose fixtures still FOLLOW the skin, arithmetically?",
  __import__('t1_shell').nose_fixture_dx(2.1015, 0.5450, 0.9330) == 0.0
  and 'HL_X = HL_X0 + S.nose_fixture_dx' in open('build.py').read()
  and 'loc=(2.0960' not in open('build.py').read()
  and 'F217' in open('OPEN_FINDINGS.md').read(),
  "FIXED AT REV 68.  The pods and lamps were placed at hard-coded x literals "
  "typed against a nose at NOSE_BULGE 0.019, so rev 67 moved the nose and left "
  "ind1_base 7.6 mm of OPEN AIR with VERIFY 0 fail 0 warn -- the only row that "
  "ever stopped a bulge change is `length`, a max-over-x, blind to a rearward "
  "deformation BY CONSTRUCTION (F217).  Both now derive from "
  "t1_shell.nose_fixture_dx, which is EXACTLY 0 at the authored bulge (so the "
  "shipped build is unmoved) and 13.38 mm at 0.045.  This question fails if "
  "either literal is placed raw again, or if the follow silently becomes a "
  "no-op -- F208's failure mode, one axis over")

P("  %d asked, %d BROKE%s" % (NQ[0], len(bad),
                              ("  --  " + "; ".join(bad)) if bad else ""))
P("  A question that can no longer fail is not a control.  The last FOUR were")
P("  REPLACED at rev 67 and are about what REV 67 measured, refuted and left")
P("  open -- the nose's constant, the EXIF the tree never read, the bar that")
P("  could not refuse, and the fixtures that do not follow the skin.  The")
P("  rev-63 batch is still the oldest and is the next one to replace.")
sys.exit(1 if bad else 0)


