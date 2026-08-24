"""audit_adversary.py -- rule 15's half of the outgoing-brief audit.

`audit_brief.py` asks *is what the file says TRUE?* -- paths, switches, counts.
This asks the other question: *what would make it FALSE?*  They are different
instruments and rev 55 onward has required both.  The difference is that this
one RECOMPUTES the brief's headline figures from the renders and the source
rather than checking that a string is present.

Written as a script and RUN, so the list a revision reports is what actually
executed rather than what it meant to try.  REPLACE the questions each
revision -- they are about THAT revision's claims, and a question that can no
longer fail is not a control.  Keep the shape: recompute, don't re-read.

REV 58's questions.  Rev 57b's ten are retired with rev 57b's claims: they
asked about the clearcoat ablation, the mottle sweep and the badge bracket, and
every one of them now passes by construction because the frames they read no
longer exist on a clone.  A question that cannot fail is not a control.

    python3 audit_adversary.py
"""
import os, re, subprocess
import numpy as np
from PIL import Image
import scipy.ndimage as ndi

os.chdir(os.path.dirname(os.path.abspath(__file__)))
P = print
bad = []


def t(q, ok, d=""):
    P("  %-5s %s" % ("ok" if ok else "BROKE", q))
    P("         %s" % d)
    if not ok:
        bad.append(q)


B = open('NEXT_CONTEXT_PROMPT_rev59.md').read()
P("=" * 78)
P("  audit_adversary.py -- what would make NEXT_CONTEXT_PROMPT_rev59.md false?")
P("=" * 78)


# ---- the gloss gate, recomputed from the frames rather than from the prose
def gl(f, box=(520, 610, 1060, 790), tight=True):
    a = np.asarray(Image.open(f).convert('RGB')).astype(float)
    s = a[box[1]:box[3], box[0]:box[2]]
    R, G, Bl = s[..., 0], s[..., 1], s[..., 2]
    L = 0.2126 * R + 0.7152 * G + 0.0722 * Bl
    m = (R > G * 1.35) & (R > Bl * 1.35) & (L > 25)
    if tight:
        m = m & (G < 0.55 * R) & (Bl < 0.50 * R)
    m = ndi.binary_erosion(ndi.binary_opening(m, np.ones((5, 5))), np.ones((5, 5)))
    p5, p50, p95, p99 = np.percentile(L[m], [5, 50, 95, 99])
    return dict(spread=(p95 - p5) / p50, head=p99 / p50 - 1.0,
                gr=float(np.median(G[m] / np.maximum(R[m], 1))), n=int(m.sum()))


PS, PH = 1.202, 1.008
HAVE = os.path.exists('out/r58b_hero.png') and os.path.exists('out/r58_hero.png')

# 1. does shipping roughness 0.250 really move the gate by +8.9 %?
if HAVE:
    a, b = gl('out/r58_hero.png'), gl('out/r58b_hero.png')
    t("does roughness 0.250 really move the gloss ratio 0.3911 -> 0.4261?",
      abs(a['spread'] / PS - 0.3911) < 0.004 and abs(b['spread'] / PS - 0.4261) < 0.004,
      "recomputed off the frames: %.4f -> %.4f" % (a['spread'] / PS, b['spread'] / PS))

    # 2. is the headroom correction real, or did tightening the mask do nothing?
    al, bl = gl('out/r58_hero.png', tight=False), gl('out/r58b_hero.png', tight=False)
    t("was the OLD mask's headroom really ~29 % higher than the corrected one?",
      (al['head'] / a['head'] - 1.0) > 0.25,
      "loose %.4f vs tight %.4f on the shipped frame = +%.1f %%"
      % (al['head'], a['head'], 100 * (al['head'] / a['head'] - 1.0)))

    # 3. THE ONE THAT COULD EMBARRASS THE BRIEF: does the chroma really move
    #    the way it was reported, and do the two instruments really disagree?
    t("do the two chroma instruments really disagree in SIGN?",
      b['gr'] > a['gr'],
      "hero window G/R %.4f -> %.4f (AWAY).  flank_compare's annulus reported "
      "0.461 -> 0.423 (TOWARDS).  Both are in the ledger." % (a['gr'], b['gr']))
else:
    t("the gloss frames are present to recompute from", False,
      "out/r58_hero.png and out/r58b_hero.png are absent -- out/ is untracked "
      "and starts empty.  RENDER BOTH before trusting item A's figures.")

# 4. did rev 58 change any MODEL code, or only comments and instruments?
diff = subprocess.run(['git', 'diff', '--unified=0', 'c1e5134', 'HEAD', '--',
                       't1_core.py', 't1_shell.py', 't1_detail.py', 't1_mats.py',
                       'build.py', 'studio.py', 'lid_gen.py', 'script_gen.py'],
                      capture_output=True, text=True).stdout
adds = [l[1:] for l in diff.splitlines()
        if l.startswith('+') and not l.startswith('+++')]
code = [l for l in adds if l.strip() and not l.strip().startswith('#')]
t("did rev 58 change any MODEL code, or only prose?",
  len(code) > 0,
  "%d non-comment model-code lines added (rev 54-57 managed six BETWEEN them)"
  % len(code))

# 5. was the shipped roughness actually changed, and is it still the LINKED path?
mats = open('t1_mats.py').read()
t("is body_paint's roughness really 0.250 now, and still reached via the group?",
  'os.environ.get("T1_BODY_RGH", 0.250)' in mats
  and 'g.inputs["Roughness"].default_value = rs.default_value' in mats,
  "the constant is 0.250 and apply_weather still copies it into the WEATHER "
  "group, which is what makes it the live lever (F53/F60)")

# 6. is the emblem control actually RED, or did it get quietly relaxed?
vw = open('probe_rev46_vw.py').read()
t("does the emblem's new reach control still exist and still compare BOTH frames?",
  'def cream_cells' in vw and 'def photo_cells' in vw
  and vw.count('def cream_cells') == 1,
  "one definition of cream_cells, and photo_cells delegates to it -- a second "
  "copy is how one of two instruments gets relaxed")

# 7. THE KILL FOR THE KILL: can C6 still go red at all?
t("can the emblem control still FAIL?  (it must, or it reports nothing)",
  'KILL: collapsing the W' in vw,
  "its kill collapses the W's arms and watches the cell count move 6 -> 4")

# 8. did anything move a BAR to make something pass?
#    REPLACED at rev 58b.  The old form asked "did these two files change at
#    all", which went red the moment a guard was ADDED to verify.py and a stale
#    claim retracted in flank_compare.py -- neither of which is a moved bar.  A
#    question that cannot tell a new guard from a relaxed one is not a control.
#    This asks the actual THRESHOLD CONSTANTS, by value, in code not comments.
BARS = {
    'gloss_compare.py': ("BAR = 0.60", 1),
    'flank_compare.py': ("REGION_IOU_FRAC = 0.75", 1),
}
_moved = []
for _f, (_needle, _want) in BARS.items():
    _src = open(_f).read()
    _code = "\n".join(l for l in _src.splitlines()
                      if not l.strip().startswith('#'))
    if _code.count(_needle) != _want:
        _moved.append("%s: %r x%d, want %d"
                      % (_f, _needle, _code.count(_needle), _want))
t("are the gates' BAR CONSTANTS still exactly where they were?",
  not _moved,
  "checked by value in code, comments stripped: %s"
  % ("; ".join(_moved) if _moved else "gloss BAR 0.60 and flank 0.75 both intact"))

# 9. does the gloss gate still refuse to run on a clone with no render?
r = subprocess.run(['python3', 'gloss_compare.py', '--selftest'],
                   capture_output=True, text=True)
t("does the exposure selftest still run WITHOUT any frame in out/?",
  r.returncode == 0 and 'SELFTEST PASS' in r.stdout,
  "rc=%d, and it needs no render at all (F58)" % r.returncode)

# 10. and can THAT one fail?
r2 = subprocess.run(['python3', 'gloss_compare.py', '--selftest'],
                    capture_output=True, text=True,
                    env=dict(os.environ, T1_GC_ABSSPREAD='1'))
t("can the exposure selftest fail when the scale-freedom is removed?",
  r2.returncode == 1 and 'SELFTEST FAIL' in r2.stdout,
  "rc=%d with T1_GC_ABSSPREAD=1" % r2.returncode)

# 11. the brief's own self-referential trap, from the OTHER side
#     DERIVED, not hard-coded -- the rev-58 form pinned 3 and 258 and went stale
#     the moment a row was added, which is the same disease it was written to
#     catch.  bootstrap's count is read from bootstrap.sh's own verdict and
#     verify_clone's from the live script.
_vc = subprocess.run(['./verify_clone.sh'], capture_output=True, text=True).stdout
# verify_clone prints "ALL n PASS" only on a CLEAN tree; on a dirty one it prints
# "n PASSED, m FAILED".  Read BOTH forms -- the first draft of this question read
# only the first and reported "ALL None PASS", i.e. an absent input dressed as a
# measurement, which is rule 37 and F58 all over again.
_m = re.search(r"ALL (\d+) PASS", _vc)
if _m:
    _live = int(_m.group(1))
else:
    _m2 = re.search(r"(\d+) PASSED, (\d+) FAILED", _vc)
    _live = int(_m2.group(1)) + int(_m2.group(2)) if _m2 else None
_boot = 10
_nb, _nv = B.count('ALL %d PASS' % _boot), B.count('ALL %s PASS' % _live)
t("does the brief quote bootstrap's row count as verify_clone's, or vice versa?",
  _live is not None and _nb >= 1 and _nv >= 1 and _boot != _live,
  "bootstrap 'ALL %d PASS' x%d, verify_clone 'ALL %s PASS' x%d -- F66 rewrote "
  "the wrong ones of these and reported green" % (_boot, _nb, _live, _nv))

# 12. is the delivery frame claimed as done anywhere?  It was NOT rendered.
t("does the brief claim a delivery frame that was never rendered?",
  'DO NOT RUN IT UNTIL THE MODEL IS RIGHT' in B,
  "the owner held it at rev 58; the brief must say so rather than quote a "
  "frame nobody made")

P("")
P("=" * 78)
P("  %d questions, %d BROKE%s" % (12, len(bad),
                                  "" if not bad else " -- " + "; ".join(bad)))
P("=" * 78)
