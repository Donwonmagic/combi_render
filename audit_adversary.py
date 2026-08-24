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
import os, re, subprocess, sys
import numpy as np
from PIL import Image

os.chdir(os.path.dirname(os.path.abspath(__file__)))
P = print
bad = []
NQ = [0]

BRIEF = 'NEXT_CONTEXT_PROMPT_rev61.md'


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

t("is UNDER_DROP really UNDER the 0.151 m ceiling the brief claims?",
  D_.UNDER_DROP < 0.151,
  "UNDER_DROP = %.4f m against a measured ceiling of 0.151 m.  If this ever "
  "exceeds it, the pan is deeper than the photograph's whole dark band, which "
  "contains the shadowed ground as well" % D_.UNDER_DROP)

t("do the end ramps really span the PAN's own width?",
  abs(D_.UNDER_RAMP_W - D_.UNDER_W) < 1e-9,
  "ramp %.4f vs pan %.4f -- the first cut made them 1.400 against 1.560 and "
  "the 80 mm ledge kept its square aft face, which is the defect the ramps "
  "were added to remove" % (D_.UNDER_RAMP_W, D_.UNDER_W))

t("does the pan stay clear of the vehicle's FIXED bodywork limit?",
  D_.UNDER_X1 - D_.UNDER_RAMP > -1.905,
  "aft ramp reaches x %.4f against the -1.905 limit that verify.py's length "
  "row enforces.  The first cut reached -2.100 and went red at +205 mm"
  % (D_.UNDER_X1 - D_.UNDER_RAMP))

t("is the underseal really DARKER than the interior grey it replaced?",
  'M["underseal"]' in open('t1_mats.py').read()
  and re.search(r'M\["underseal"\][^\n]*\(0\.0[0-9]+', open('t1_mats.py').read())
  is not None,
  "if underseal is not materially darker than M['dark'] (0.1150) the 0.352 -> "
  "0.219 step in the brief has no cause")

# ----------------------------------------------- the guard I broke, from source
t("is V_POW's by-value pin STILL greppable, with the ablation beside it?",
  len(re.findall(r'^V_POW = 0\.60$', open('t1_mats.py').read(), re.M)) == 1
  and 'T1_VPOW' in open('t1_mats.py').read(),
  "three verify_clone rows grep '^V_POW = 0.60'.  Rev 60's first ablation cut "
  "took out all three at once; the literal must stay on its own line")

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
t("is the tyre-span scale quoted as a RANGE, not one threshold's reading?",
  len(dark) > 60 and 150 < (dark.max() - dark.min()) < 195
  and "251-284" in open('t1_detail.py').read(),
  "tyre spans %d px at v=601; 0.665 m / that span is the 258.6 px/m the "
  "brief's 0.151 m ceiling rests on.  The WHEELBASE route gives 210 and is "
  "refused -- if this breaks, so does the ceiling"
  % (dark.max() - dark.min() if len(dark) else -1))

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

P("-" * 78)
P("  %d asked, %d BROKE%s" % (NQ[0], len(bad),
                              ("  --  " + "; ".join(bad)) if bad else ""))
P("  A question that can no longer fail is not a control.  REPLACE THESE")
P("  for rev 61 -- they are about rev 60's claims.")
sys.exit(1 if bad else 0)
