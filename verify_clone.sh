#!/usr/bin/env bash
# =============================================================================
#  verify_clone.sh -- prove this working tree matches the rev-42 measured
#  baseline, BY CONTENT.  That baseline is still current at rev 44: no geometry,
#  artwork or constant has moved since, so these figures are the live ones.
#
#  WHY THIS FILE EXISTS.  Until rev 43 these checks lived as thirty lines of
#  prose in NEXT_CONTEXT_PROMPT_revN.md, re-typed by hand every revision.  That
#  is a drift surface: a number in a paragraph goes stale silently, and this
#  project has already shipped a measurement quoted from a thirty-revision-old
#  comment.  A number in a script that runs cannot.
#
#  RULE OBEYED THROUGHOUT: check by SYMBOL AND CONTENT, NEVER BY LINE NUMBER.
#  Line numbers are the thing that rots.  `V_POW_Z` was cited as t1_shell.py:1086
#  for four revisions; by rev 42 line 1086 was blank and the symbol had moved to
#  1217.  Nothing here cites a line number.
#
#  USAGE   ./verify_clone.sh            # human output
#          ./verify_clone.sh --quiet    # only the verdict line
#  EXIT    0 = every check passed.  1 = at least one failed.  DO NOT BUILD ON 1.
#
#  Portable across macOS (BSD userland) and Linux (GNU).  No dependency beyond
#  git, grep, awk and one of md5/md5sum.
# =============================================================================
cd "$(dirname "$0")" || exit 1
QUIET=0; [ "$1" = "--quiet" ] && QUIET=1
PASS=0; FAIL=0; FAILED_LINES=""
# rev 51 -- THE SCORE IS SPLIT, and the split is the finding.
# An intake audit this revision extracted every executed `ck` call site and
# classified it.  THE RESULT: 0 of 125 rows name a reference frame AND a pixel
# window; 125 of 125 compare the model, or the record, to itself.  Five rows
# touch a photograph at all and every one is an `ls | wc -l` existence count --
# none opens an image.  The count was validated against this script's own output
# at two points in history (113 at rev 49c, 125 at HEAD).
#
# SURVEY_rev49 sec.4 prescribed exactly this TWO revisions ago (the survey was
# produced during rev 50) -- "must name the
# reference frame and the pixel window ... or be tagged SELF-CONSISTENCY, NOT
# FIDELITY ... they must stop counting toward '113 PASS'" -- and it never reached
# the machine.  This is that, in the machine.
#
# `ckf` is the FIDELITY entry point: use it ONLY for a row whose executed
# expression measures against a NAMED FRAME and a NAMED PIXEL WINDOW.  There are
# none yet, and the banner says so out loud rather than letting "ALL 125 PASS" be
# pasted into a handoff as evidence about the vehicle.
#
# NOTE THE STRUCTURAL LIMIT, so nobody wastes a revision on it: this script has no
# build, no render and no image library, and out/ is untracked and starts EMPTY.
# It CANNOT host a fidelity row as written.  The fidelity lane already exists and
# is DECOMMISSIONED -- flank_compare.py is a render-vs-photograph gate that exits
# non-zero, dormant since rev 40, with zero LEDGER mentions since rev 43.  (It IS
# named in the rev-41/42/43 prompts and in SURVEY_rev49; 'zero mentions anywhere'
# is too strong and was wrong in an earlier commit message.)  Reviving
# THAT is the job; adding image rows here is not.
FID=0
ckf () { FID=$((FID+1)); ck "$@"; }

say () { [ $QUIET -eq 1 ] || printf '%s\n' "$*"; }

# ck <label> <expected> <actual>
ck () {
  local label="$1" want="$2" got="$3"
  got="$(printf '%s' "$got" | tr -d '[:space:]')"
  if [ "$got" = "$want" ]; then
    PASS=$((PASS+1)); [ $QUIET -eq 1 ] || printf '  ok    %-52s %s\n' "$label" "$got"
  else
    FAIL=$((FAIL+1)); FAILED_LINES="$FAILED_LINES\n    $label -- got '$got', want '$want'"
    printf '  FAIL  %-52s got %s  want %s\n' "$label" "${got:-<empty>}" "$want"
  fi
}

# md5 of a file, GNU or BSD, hash only
md5of () {
  if command -v md5sum >/dev/null 2>&1; then md5sum "$1" | awk '{print $1}'
  elif command -v md5 >/dev/null 2>&1; then md5 -q "$1"
  else echo "NO-MD5-TOOL"; fi
}

say
say "=============================================================="
say "  Senor Tacombi combi -- verify the tree by content (rev 42)"
say "=============================================================="
say "  where: $(pwd)"
say

# ---------------------------------------------------------------- git identity
# ---------------------------------------------------------------------------
# IDENTITY IS ANCESTRY, NOT ARITHMETIC.
# A hard "== 227 commits" test fails the moment THIS revision commits anything,
# which makes it useless exactly when you need it most -- mid-revision, checking
# you have not broken something.  What actually must hold is that rev 42's
# verified tip is still in your history.  That never goes stale.
# ---------------------------------------------------------------------------
REV42_TIP=437d54387d77436da28b249cc81d23fc3668a0d6
say "-- git --"
if git cat-file -e "$REV42_TIP^{commit}" 2>/dev/null && \
   git merge-base --is-ancestor "$REV42_TIP" HEAD 2>/dev/null; then
  ck "rev-42 tip is an ancestor of HEAD" yes yes
else
  ck "rev-42 tip is an ancestor of HEAD" yes no
fi
NCOM="$(git log --oneline 2>/dev/null | wc -l | tr -d '[:space:]')"
if [ "${NCOM:-0}" -ge 227 ]; then
  ck "commits >= 227" ok ok
  say "        ($NCOM commits; 227 is rev 42, more means you have added work)"
else
  ck "commits >= 227" ok "short:$NCOM"
    printf '        (A SHALLOW CLONE FAILS HERE AND THE TREE IS FINE.  rev 44\n'
    printf '         landed on a 50-commit clone.  Fix: git fetch --unshallow,\n'
    printf '         then re-run.  Do NOT edit this check.)\n'
fi
# Only TRACKED modifications are a stop condition.  audit.py rewrites STATE.md
# on every run -- that is the one this catches.  Untracked files (a new probe
# you are writing) are reported below but are not a failure.
ck "modified tracked files"        0 "$(git status --porcelain --untracked-files=no 2>/dev/null | wc -l)"
NFIL="$(git ls-files 2>/dev/null | wc -l | tr -d '[:space:]')"
if [ "${NFIL:-0}" -ge 239 ]; then
  ck "tracked files >= 239" ok ok
  say "        ($NFIL files; 239 is rev 42.  FEWER means something was deleted.)"
else
  ck "tracked files >= 239" ok "lost:$NFIL"
fi

# ------------------------------------------------------------------- structure
# The 37 handoffs and every prompt live at the ROOT.  There is no docs/ and
# there never has been -- rev 43's first draft told the reader to open
# docs/HANDOFF_rev42.md, which would have failed, and to WRITE docs/HANDOFF_rev43.md,
# which would have broken a 37-file convention.
say "-- layout --"
NHO="$(ls HANDOFF*.md 2>/dev/null | wc -l | tr -d '[:space:]')"
if [ "${NHO:-0}" -ge 37 ]; then ck "HANDOFF_*.md at root >= 37" ok ok
else ck "HANDOFF_*.md at root >= 37" ok "only:$NHO"; fi
ck "docs/ must NOT exist"           0 "$(ls -d docs 2>/dev/null | wc -l)"
NPR="$(ls probe_*.py 2>/dev/null | wc -l | tr -d '[:space:]')"
if [ "${NPR:-0}" -ge 31 ]; then ck "probe_*.py >= 31" ok ok
  say "        ($NPR probes; 31 is rev 42.  Probes are never deleted.)"
else ck "probe_*.py >= 31" ok "lost:$NPR"; fi
ck "source photographs (.jpg)"      3 "$(ls ref_side.jpg ref_rear34.jpg ref_workshop.jpg 2>/dev/null | wc -l)"
# rev 45 -- THIS CHECK WAS RE-WRITTEN, NOT RE-BASED, AND HERE IS WHY.
# It counted `ref_*.png` and called the answer "annotated derivatives".  Those
# are two different things and the label was carrying the check.  rev 45 added
# ref_playa_34.png, which is a SOURCE PHOTOGRAPH that happens to be a .png, and
# the count went 5 -> 6 while nothing about the derivatives changed.  Bumping
# the 5 to a 6 would have made the check pass and stopped it meaning anything.
# So it now names the five derivatives it is actually about.
ck "annotated derivatives (grids)" 5 "$(ls ref_band_grid.png ref_grid.png ref_nose_grid.png ref_side_grid.png ref_x6_lanczos.png 2>/dev/null | wc -l)"
# rev 45 -- NEW, AND IT IS THE CHECK THAT WOULD HAVE SAVED A REVISION.
# NEXT_CONTEXT_PROMPT_rev45.md sec.4 states "Reference photographs (8, all
# tracked)" and names four Nolita frames.  THREE OF THE FOUR WERE NEVER
# COMMITTED.  Item W1 -- the entire roundel task -- was specified against
# measurements taken on ref_nolita_front34.jpg, a file that was not in the
# tree.  No check noticed, because no check counted them.  This one does.
# See REFERENCE_FRAMES_rev45.md for the recovery and the identifications.
ck "nolita + playa frames"          5 "$(ls ref_nolita_doorshut.jpg ref_nolita_flank.jpg ref_nolita_front34.jpg ref_nolita_front34b.jpg ref_playa_34.png 2>/dev/null | wc -l)"
ck "upload provenance kept"         5 "$(ls IMG_2053.jpeg IMG_2054.jpeg IMG_2060.jpeg IMG_3840.jpeg IMG_3842.png 2>/dev/null | wc -l)"

# ------------------------------------------------------------ SPEC anchor counts
# ANCHOR WITH ^.  grep -c COUNTS LINES, NOT OCCURRENCES.  CASE MATTERS.
say "-- SPEC.md anchors --"
ck "^### 10.100"                    1 "$(grep -c '^### 10.100' SPEC.md)"
ck "^#### 10.100"                   8 "$(grep -c '^#### 10.100' SPEC.md)"
ck "^### 10.101"                    1 "$(grep -c '^### 10.101' SPEC.md)"
ck "^#### 10.101"                   9 "$(grep -c '^#### 10.101' SPEC.md)"
ck "^### 10.99"                     1 "$(grep -c '^### 10.99' SPEC.md)"
ck "^#### 10.99"                    7 "$(grep -c '^#### 10.99' SPEC.md)"
ck "^#### 10.98"                   13 "$(grep -c '^#### 10.98' SPEC.md)"

say "-- SPEC.md content --"
ck "AN ORDINAL FACT NEEDS NO RULER" 1 "$(grep -c 'AN ORDINAL FACT NEEDS NO RULER' SPEC.md)"
ck "A LINE YOU DREW IS NOT EVIDENCE" 1 "$(grep -c 'A LINE YOU DREW IS NOT EVIDENCE' SPEC.md)"
ck "0.7770 (the BUILT arch crown)"  2 "$(grep -c '0.7770' SPEC.md)"
ck "55.97 (self-overlap)"           1 "$(grep -c '55.97' SPEC.md)"
# rev 44b: 2 -> 5.  SPEC 10.102 (the retraction) and 10.106 (the forward
# lobe) each quote the clearance again, and 10.106 quotes both it and the
# built 0.024381 side by side.  The CONSTANT has not moved -- t1_shell still
# derives it from rev 41's own smoothed outline and the guard still fires on
# it.  Only the number of places SPEC cites it changed.
ck "0.024426 (DOOR_ARCH_G)"         5 "$(grep -c '0.024426' SPEC.md)"
ck "COMMON-MODE (case matters)"     3 "$(grep -c 'COMMON-MODE' SPEC.md)"
PAT_CFF="THE COUNTER'S FRONT FACE"   # apostrophe: keep it in a variable
ck "THE COUNTER'S FRONT FACE"       3 "$(grep -c "$PAT_CFF" SPEC.md)"
ck "CLOSED BY HIM (case matters)"   3 "$(grep -c 'CLOSED BY HIM' SPEC.md)"
ck "CNT_NOSE_F"                     6 "$(grep -c 'CNT_NOSE_F' SPEC.md)"
ck "cab_floor"                      4 "$(grep -c 'cab_floor' SPEC.md)"
ck "amtrak (HIS word)"              2 "$(grep -c 'amtrak' SPEC.md)"
# rev 44: 9 -> 16.  ADJUDICATED, NOT LOOSENED.  This tripwire asks "has Nolita
# material crept in without being adjudicated?".  Rev 44's additions ARE the
# adjudication: the owner answered SPEC sec.7's standing "whether it is
# physically the same vehicle is U" with SAME VEHICLE, and sec.7.1/7.2 record
# that plus the era-tag correction.  Seven new mentions, all in those two
# subsections.  If this fires again, adjudicate the NEW ones -- do not bump it.
# rev 44b: 16 -> 25.  ref_nolita_doorshut.jpg and ref_nolita_front34.jpg
# carried four of this revision's findings (10.102, 10.105, 10.106, 10.107),
# so SPEC names them nine more times.  This row is a REMINDER THAT THE
# NOLITA FRAMES ARE ADMISSIBLE, not a cap on how often they are used.
# rev 45 -- AND A BUMP THAT WAS WRONG, RECORDED BECAUSE THE CHECK CAUGHT IT.
# On adding SPEC 10.117 this row was bumped 31 -> 33 on the assumption that the
# new section cites the nolita frames.  IT DOES NOT -- 10.117's photographed
# targets are quoted as counts and sigmas, and the frame names live in
# probe_rev45_paint.py and in this file's own comments, neither of which this
# row greps.  The count is still 31.  Rule 4: never put a figure in an
# acceptance test unless you watched it print.  Fourth instance in this repo,
# and the first where the wrong figure was mine and the check found it inside
# one minute.
# rev 45: 29 -> 31.  SPEC 10.116 cites ref_nolita_flank.jpg and ref_playa_34.png
# as two of the four frames that supply the PHOTOGRAPHED contact-shadow target
# (0.650 +- 0.210).  Third bump this revision; still not a cap.
# rev 45: 28 -> 29 within the same revision -- SPEC 10.115 (the headlamp bowls)
# cites ref_nolita_front34.jpg as one of the two frames that show the bowl as a
# shadowed ring round the bezel.  Same reading again: not a cap.
# rev 45: 25 -> 28.  SPEC 10.110 and 10.111 name ref_nolita_front34.jpg three
# more times -- it is the frame that settled the headlamp bezel's chroma and
# the frame rev 45's badge work was checked against.  Same reading as rev 44b's:
# THIS ROW IS A REMINDER THAT THE NOLITA FRAMES ARE ADMISSIBLE, not a cap.
# rev 48: 31 -> 32.  SPEC 10.122.3 cites ref_nolita_front34.jpg for the one
# thing that frame settled this revision: it shows the REAL rear louvres
# reading as BRIGHT highlight lines, which is what refuted rev 48's own
# headline finding that the built slats have the wrong sign.  Sixth bump,
# same reading as every one before it: THIS ROW IS A REMINDER THAT THE NOLITA
# FRAMES ARE ADMISSIBLE, not a cap.  WATCHED PRINT at "got '32', want '31'"
# before it was changed here (rule 4) -- the row went red first, and the bump
# is the response to it, not a guess ahead of it.
ck "nolita, any case"              32 "$(grep -ic 'nolita' SPEC.md)"
ck "TEN flower heads"               1 "$(grep -c 'TEN flower heads' SPEC.md)"

# ------------------------------------------------------------------ build files
say "-- build files --"
# rev 44b: 7 -> 3.  SPEC 10.102 retracted 10.100's wrap, and with the arc
# gone so are its fixed-point solve and the four references that fed it.
# What remains is the definition, the guard and its message -- which is the
# whole point: the CLEARANCE INVARIANT survived the geometry that motivated
# it.  A drop to 0 would be the finding; 3 is the invariant standing alone.
# rev 59: STILL 3, BUT THEY ARE NOT THE SAME THREE.  The guard no longer
# COMPARES against DOOR_ARCH_G -- rev 41's clearance was an accident of rev
# 41's outline, not a measurement, and the photograph puts the real clearance
# at a third of it.  DOOR_ARCH_G is now the definition plus two mentions in
# the re-based guard's message, where it is REPORTED as the historical anchor
# rather than enforced as a bar.  The count is unchanged; the meaning is not,
# and that is said here rather than left for the next reader to discover.
ck "DOOR_ARCH_G in t1_shell.py"     3 "$(grep -c 'DOOR_ARCH_G' t1_shell.py)"
# rev 44b: 4 -> 0, AND THAT IS CORRECT.  `_G_BUILD` existed ONLY to solve the
# construction clearance for 10.100's wrapped arc by fixed point.  10.102
# retracted the wrap; the outline is rev 41's table again and needs no solve.
# The PATTERN is not lost -- t1_core.vw_bars now uses it for the emblem
# (10.107) and that is where to look for it.
ck "_G_BUILD in t1_shell.py"        0 "$(grep -c '_G_BUILD' t1_shell.py)"
# rev 44b: 4 -> 3.  Same cause: the fixed-point loop called it once per pass.
# The three that remain are the definition, DOOR_ARCH_G, and _MIN_RAD -- i.e.
# the measure, the reference value and the guard.  All three must stay.
ck "_arch_radial in t1_shell.py"    3 "$(grep -c '_arch_radial' t1_shell.py)"
ck "T1_ABLATE in build.py"          5 "$(grep -c 'T1_ABLATE' build.py)"
# rev 58: THIS ROW WAS A RAW grep -c AND IT COUNTED COMMENTS.  The rear-arch fix
# added seven mentions of FLOOR_W in comments and docstrings -- every one of them
# EXPLAINING WHY FLOOR_W DOES NOT MOVE -- and the row read 12 against its 5 and
# called the explanation the defect.  That is sec.10.4's trap, and it is now the
# SIXTH time a row in this file has done it.
# THE EXPECTED VALUE IS UNCHANGED: stripped of comments and docstrings the count
# is still exactly 5, which is what the row always meant.  It is not re-based --
# it is made to measure what it was written to measure.
ck "FLOOR_W in t1_detail.py (CODE only)" 5 "$(python3 -c "
import ast
src = open('t1_detail.py').read()
keep = set(range(1, len(src.splitlines()) + 1))
for n in ast.walk(ast.parse(src)):
    if isinstance(n, (ast.Module, ast.FunctionDef, ast.ClassDef)):
        d = ast.get_docstring(n, clean=False)
        if d is not None:
            b = n.body[0]
            for i in range(b.lineno, (b.end_lineno or b.lineno) + 1):
                keep.discard(i)
code = [l for i, l in enumerate(src.splitlines(), 1)
        if i in keep and not l.strip().startswith('#')]
print(sum(l.count('FLOOR_W') for l in code))" 2>&1 | tail -1)"
ck "_assert_same_edge"              4 "$(grep -c '_assert_same_edge' flank_compare.py)"
# rev 52.  SELF-CONSISTENCY, NOT FIDELITY -- this script cannot render, so it
# cannot check what the tarnish windows actually rescue.  What it CAN hold is
# that the fix is still in the source and its ablation still exists.  THE
# DEFECT IT PINS: a tarnish zone estimated its ink endmember over pixels the
# silver rule had already claimed, so 16.5 % of `Tacombi`'s swash inside the
# "enor" window drove the endmember NEUTRAL, the 50 %-mix threshold fell
# 0.2192 -> 0.1086 and the window rescued +0 px.  `Senor` read 0.174 of its
# own ceiling; with the sample restricted to unclaimed pixels it reads 0.480,
# against 0.459 on the same instrument at rev 40 and 0.504 at rev 17.
# RUN IT to see those numbers -- `python3 flank_compare.py out/<pfx>_side.png`
# -- and `T1_TARNCONTAM=1` puts the defect back so the guard can be WATCHED
# FAILING.  Both were watched at rev 52.
# rev 53.  A TYPED COPY OF A DERIVED CONSTANT, AND IT HAD DRIFTED.
# flank_compare.py typed `X_TAIL = -1.8727` while t1_core derives -1.873000.
# 0.3 mm, and harmless in that file (it is only printed in a diagnostic) -- but
# rev 53's OWN brief audit read the copy as the live value and published the
# A7 gap as 802.7 mm where it is 803.0.  The rev-52 session had it right; this
# session got it wrong by reading a copy instead of asking the module, which is
# rule 10 and rule 11 together.  `_const`'s own failure text already said
# "fix the reader, do not re-copy the value".
# Row 1: the literal must not come back.  Row 2: the figure it corrupted --
# the A7 gap -- must reproduce from source, derived on BOTH sides.
ck "flank_compare does NOT re-type X_TAIL" 0 "$(grep -cE '^X_TAIL = -?[0-9]' flank_compare.py)"
ck "the A7 gap reproduces from source: 803 mm" 803 "$(python3 -c "
import ast
g={}
for n in ast.parse(open('t1_core.py').read()).body:
    if isinstance(n,ast.Assign):
        for t in n.targets:
            if isinstance(t,ast.Name) and t.id in ('X_AXLE_R','O_NEW'): g[t.id]=ast.literal_eval(n.value)
for n in ast.parse(open('t1_shell.py').read()).body:
    if isinstance(n,ast.Assign) and any(isinstance(t,ast.Tuple) for t in n.targets):
        names=[e.id for t in n.targets for e in t.elts if isinstance(e,ast.Name)]
        if 'LID_X1' in names:
            g['LID_X1']=ast.literal_eval(n.value)[names.index('LID_X1')]
print(round(abs(g['LID_X1']-(g['X_AXLE_R']-g['O_NEW']))*1000))
" 2>/dev/null)"
ck "tarnish endmember excludes claimed px" 1 "$(grep -cE 'smp = zm & ~raw$' flank_compare.py)"
ck "T1_TARNCONTAM ablation exists"         3 "$(grep -c 'T1_TARNCONTAM' flank_compare.py)"
# rev 52, A6.  SELF-CONSISTENCY, NOT FIDELITY -- this script cannot render.
# THE DEFECT: the chip gate keys off Pointiness, which is PER-VERTEX, so on
# unsubdivided detail geometry every vertex is a corner and the ramp saturates
# over a whole FLAT FACE.  t1_mats.py has said so in prose since rev 44 ("the
# counter slab reads pw = 1.0 across its entire top") and the gate was never
# re-based.  MEASURED at rev 52 on painted, eye-verified windows: the counter
# fascia's dark-chip coverage is 4.07 % against ref_side.jpg's 0.00 %.
# T1_EDGEBEVEL=1 swaps in a ray-traced Bevel-vs-true-normal edge signal and
# takes the same window to 0.10 % while a verified SHELL window holds at
# 0.00 % -> 0.00 %: the chip gate moves ALONE, which T1_CTAN_WEAR never did
# (it also drops Metallic).  IT IS NOT THE DEFAULT and SPEC sec.3 locks the
# finish WEATHERED.  These rows hold that BOTH paths and the derivation
# survive; only rendering can say which is right.
#
# REV 53 RETRACTS REV 52'S REASON, AND THE RETRACTION IS IN t1_mats.py TOO
# (rule 15: a retraction that lands in a ledger and not in the source is half a
# retraction).  Rev 52 said the edge band is SUB-PIXEL at GAPW/2 = 0.75 px.
# Rev 53 rendered T1_EDGERAD=12 -- 3.3 px, well above a pixel -- and the fascia
# is UNCHANGED at 0.000 %.  The sub-pixel explanation is refuted; so is a butt
# joint (`counter` is a closed mesh, 0 boundary edges).  The lever is NOT inert:
# the 2.75 vs 12 mm difference lights up every window frame, shut line, arch lip
# and gutter and nothing between them.  WHY THAT ONE FOLD IS SILENT IS OPEN.
# rev 53, HIS RULING: "Follow the photograph -- clean cream", taken on the crop
# probe_scratch/rev53_owner_fascia.png with the measured coverages beside it.
# The EDGE signal is the default now and Pointiness is the ablation.  The row
# below is anchored on the else-branch, so it fails if the default is flipped
# back silently OR if the two branches are swapped.
# BOTH ROWS BELOW WERE WRONG WHEN FIRST WRITTEN AND WERE CAUGHT BY WATCHING
# THEM FAIL, WHICH IS THE ONLY REASON THIS COMMENT IS HERE.
#   * the DEFAULT row was anchored on `pw = _mr(nt, EDGE, ...` at an 8-space
#     indent -- but BOTH branches are that, so swapping the two branches left
#     it passing.  It is anchored on the LINE AFTER the T1_PTWEAR test now, so
#     it reads which branch the ABLATION takes and therefore which is default.
#   * the RULING row was anchored on 'Follow the$' -- which matched a line that
#     merely WRAPPED there, not the sentence recording the ruling.  A guard
#     anchored on where a sentence happens to wrap tests nothing.
ck "chip gate: the EDGE signal is the DEFAULT" 1 "$(grep -A1 'os.environ.get("T1_PTWEAR") == "1":' t1_mats.py | grep -c 'nt, PT, W_PT_LO')"
ck "T1_PTWEAR restores the OLD gate"     1 "$(grep -c 'os.environ.get("T1_PTWEAR")' t1_mats.py)"
ck "his cream ruling is recorded in the source" 1 "$(grep -c 'ASKED AND ANSWERED at rev 53' t1_mats.py)"
# RE-BASED AT REV 53, CAUSE NAMED: this row counted MENTIONS of W_EDGE_90, so
# it broke when rev 53 added a comment that merely names the symbol -- a wording
# change failing a row that is supposed to test a DERIVATION.  It is anchored on
# the derivation expression itself now, with a companion row below that makes
# the thing it actually cares about -- that the window is not a typed literal --
# separately testable.  Both watched failing.
ck "edge window DERIVED from a 90 deg fold" 1 "$(grep -cE '^W_EDGE_LO, W_EDGE_HI = 0\.10 \* W_EDGE_90, 0\.50 \* W_EDGE_90$' t1_mats.py)"
ck "edge window is not a typed literal"     0 "$(grep -cE '^W_EDGE_LO, W_EDGE_HI = 0\.[0-9]+, 0\.[0-9]+$' t1_mats.py)"
# rev 53.  The radius is a SWEEPABLE lever now, and the DEFAULT MUST STAY
# DERIVED: T1_EDGERAD unset has to fall back to GAPW/2 exactly, or a sweep
# silently becomes the shipped radius.  Anchored on the fallback expression
# itself, so an APPENDED override fails this row and not only a deletion.
ck "T1_EDGERAD radius lever exists"      1 "$(grep -c 'os.environ.get("T1_EDGERAD")' t1_mats.py)"
ck "bevel radius DERIVED when unset"     1 "$(grep -cE 'else _SH\.GAPW / 2\.0\)$' t1_mats.py)"
ck "rev52's sub-pixel reason is RETRACTED in the source" 1 "$(grep -c 'IS RETRACTED HERE' t1_mats.py)"
# rev 53.  The chip probe must keep the two controls that make it readable at
# all -- the record's own pair (arm A) and the NULL control (arm C) that caught
# this probe reading 8.117 %% on PURE NOISE when it used a std instead of a MAD.
ck "rev53 chip probe exists"             1 "$(ls probe_rev53_chip.py 2>/dev/null | wc -l)"
ck "chip probe keeps its NULL control"   1 "$(grep -c 'nul = np.full_like' probe_rev53_chip.py)"
ck "chip probe keeps the record's controls" 1 "$(grep -c 'record 7.316' probe_rev53_chip.py)"

# --------------------------------------------------------------------- rev 54
# BRIEF sec.3 ITEM 2, ANSWERED.  The fold is NOT silent: it carries a chip band
# ~1 mm tall that is 0.27 px at the shipped render's own 271.2 px/m.  Three
# things must not quietly come back, and each has its own row.
#
#   1. the RETRACTION of the premise.  Rule 15: a retraction that lands in a
#      ledger and not in the source is half a retraction.
#   2. the STALE SECOND DEFAULT.  For a whole revision this block asserted both
#      "DEFAULT IS STILL POINTINESS" and "THE DEFAULT IS NOW THE RAY-TRACED EDGE
#      SIGNAL".  The row above that guards the flip is anchored on the CODE and
#      went on passing, because the code was right and only the prose lied.
#      This row is the missing half: it counts the stale sentence and wants 0.
#   3. the AOV probe's own instrument.  It tracks the fold PER COLUMN because
#      the fascia SLOPES 5.25 mm across a 300 mm window; a single min(z) put the
#      fold 134 px = 25 mm wrong and would have measured the wrong rows.
ck "rev54: the fold's PREMISE is retracted in the source" 1 "$(grep -c 'ITS PREMISE IS RETRACTED: THE FOLD PRODUCES A SIGNAL' t1_mats.py)"
ck "no stale SECOND default is asserted"  0 "$(grep -cE '^ *# DEFAULT IS STILL POINTINESS' t1_mats.py)"
ck "rev54 EDGE-AOV probe exists"          1 "$(ls probe_rev54_aov.py 2>/dev/null | wc -l)"
ck "AOV probe tracks the fold PER COLUMN" 1 "$(grep -c 'def fold_per_column' probe_rev54_aov.py)"
ck "AOV probe keeps its radius sweep"     1 "$(grep -c 'RADIUS SWEEP AT 5333 px/m' probe_rev54_aov.py)"
ck "rev54 look probe renders a scale ladder" 1 "$(grep -c '(\"shipped\", 271.2)' probe_rev54_look.py)"
# THE BADGE DENOMINATOR TRAP.  CAP_EMBLEM_WFRAC is documented as w/R but the
# BUILT stroke/outer-radius is wfrac/0.814, because _fit_glyph rescales off the
# outline's own rmax.  A photograph measures the built ratio.  The note that
# says so must stay beside the constant, and the probe that measured it must
# keep the CALIBRATION that makes it believable.
ck "badge: the wfrac denominator trap is recorded" 1 "$(grep -c 'built stroke / OUTER RADIUS' t1_detail.py)"
ck "badge: wfrac probe keeps its calibration" 1 "$(grep -c 'recover a KNOWN stroke width before trusting' probe_rev54_wfrac.py)"

# ------------------------------------------------- rev 54: THE REFERENCE SET
# *[owner, rev 54]* "we have all references that we need on repo and I want to
# make sure that is never forgotten."
#
# THAT IS A STANDING INSTRUCTION AND IT WAS UNGUARDED.  Not one row anywhere
# named a reference photograph -- the only image ever checksummed was
# tex/emblem.png, which is a BUILD INPUT, not a reference.  The frames these
# rows name are the ENTIRE evidentiary basis of the project: every measurement
# of the real vehicle traces to one of them, they cannot be re-shot, and
# nothing stopped one being deleted, replaced or quietly re-compressed.
#
# EACH IS NAMED INDIVIDUALLY ON PURPOSE.  A single "the reference folder is
# intact" row would say nothing about WHICH frame went; these say the name.
ck "ref ref_side.jpg"            46e40bc2510090662549f9eefc57c362 "$(md5of ref_side.jpg)"
ck "ref ref_rear34.jpg"          71597dabdc60c4268dd33ec39dc10076 "$(md5of ref_rear34.jpg)"
ck "ref ref_workshop.jpg"        cdeb424a3de4b1369855d9a11ebc473a "$(md5of ref_workshop.jpg)"
ck "ref ref_playa_34.png"        230a2a90df741cb4339092239da4f67d "$(md5of ref_playa_34.png)"
ck "ref ref_nolita_front34.jpg"  ed2c33b0ec5e98b9130dc2b736480f19 "$(md5of ref_nolita_front34.jpg)"
ck "ref ref_nolita_front34b.jpg" b8e7f7a44b4b4815249592fc71a3a413 "$(md5of ref_nolita_front34b.jpg)"
ck "ref ref_nolita_flank.jpg"    a00c45b431b9bd008f05c78572bf1ade "$(md5of ref_nolita_flank.jpg)"
ck "ref ref_nolita_doorshut.jpg" f1b6f98c6a12b6e9ea0ec3edc68e945a "$(md5of ref_nolita_doorshut.jpg)"
ck "ref IMG_2073.jpeg"           f1ac467d5379b42fe3f5356039d996f4 "$(md5of IMG_2073.jpeg)"
ck "ref ref_source.jpeg RETIRED" 03631c7ae35ea83a6a4cdcfad92f773f "$(md5of ref_source.jpeg)"
ck "ref bus_model_ref.JPG BAR"   baef09ed9bff4b9fe6400573423a90dc "$(md5of bus_model_ref.JPG)"
ck "ref ref_grid.png"            676249b4f81900760bfcd780d5827342 "$(md5of ref_grid.png)"
ck "ref ref_side_grid.png"       6826283344065360eacaaec77c8a780c "$(md5of ref_side_grid.png)"
ck "ref ref_nose_grid.png"       7d3ff9ca2605926f5e7ab5390e783fe8 "$(md5of ref_nose_grid.png)"
ck "ref ref_band_grid.png"       4dd318c916bea5f245f2d8ac71b6bfcf "$(md5of ref_band_grid.png)"
ck "ref ref_x6_lanczos.png"      3401d1157c2cb664b2318b107c9c6693 "$(md5of ref_x6_lanczos.png)"
# A FLOOR, NOT AN EQUALITY: new frames are welcome, losing one is not.
#
# THE FIRST VERSION OF THIS ROW WAS A TYPED GUESS AND IT DID NOT FIRE.  It
# counted EVERY tracked image -- including the ~1000 in probe_scratch/ -- against
# a floor of 111 that I never watched print.  Dropping ref_rear34.jpg from the
# index left it passing, which is how the defect surfaced: rule 5, a figure in
# an acceptance test that nobody watched print, written by the same session that
# quoted rule 5.  The count is SCOPED to the reference class now and the floor is
# the measured 54.
_REFN="$(git ls-files 2>/dev/null | grep -iE '\.(jpg|jpeg|png|JPG)$' | grep -vcE '^(probe_scratch|tex|marks)/' || echo 0)"
ck "reference-class images never DROP below 54" 1 "$([ "${_REFN:-0}" -ge 54 ] && echo 1 || echo 0)"
# RULE 11 MADE MECHANICAL.  Five byte-identical pairs are KNOWN (the IMG_*
# originals and their ref_* names).  A SIXTH group means a frame arrived that
# duplicates one we already hold -- which is not corroboration, and has fooled
# this project before.  Adding a genuinely new frame leaves this at 5.
_DUPG="$(md5sum ./*.jpg ./*.jpeg ./*.png ./*.JPG 2>/dev/null | awk '{print $1}' | sort | uniq -d | wc -l)"
ck "byte-identical reference groups still 5" 5 "$_DUPG"
ck "chip probe reads the frame through its OWN optics" 1 "$(grep -c 'THROUGH THE PHOTOGRAPH' probe_rev53_chip.py)"
# rev 52, A9 / SURVEY_rev49 finding 28.  SELF-CONSISTENCY, not fidelity.
# gal_rail was TYPED at centre -0.3800 length 0.660 and measured on the mesh at
# X -0.050 .. -0.710: 165 mm too long, 218 mm too far forward, crossing the
# pillar into BAYS[1], and THREE OF THE SIX HOOKS below it hung on nothing.
# Its own measurement is "bay 3, u 0.02-0.98", so it is DERIVED from BAYS[2]
# now and re-measures at centre -0.5980 length 0.4949.  Floating hooks 3 -> 1.
# gal_caddy_fill's X inset had the WRONG SIGN -- (bx0, bx1) is authored
# high-then-low, so the inset EXPANDED it: 24.0 mm longer than its caddy,
# 12 mm proud of both ends; now 24.0 mm inset.  T1_RAILSTALE=1 restores the
# typed rail.  STILL OPEN, carried: the sixth hook at -0.907 lies 51.4 mm
# beyond BAYS[2]'s own aft edge, so the hook stations and the bay measurement
# DISAGREE.  Fixing the rail cannot close that and it was not made to.
ck "gal_rail DERIVED from its bay"       1 "$(grep -Fc 'min(S.BAYS[2])' t1_detail.py)"
ck "gal_rail u-extent is named"          2 "$(grep -c '_RAIL_U0' t1_detail.py)"
ck "T1_RAILSTALE ablation exists"        2 "$(grep -Fc 'T1_RAILSTALE' t1_detail.py)"
ck "caddy fill inset cannot invert"      1 "$(grep -Fc '_fx0, _fx1 = min(bx0, bx1)' t1_detail.py)"
# rev 52, A7 (brief SS5 item 4's "second hole, which stands").  SELF-CONSISTENCY.
# gal_end_a exists to stop a camera seeing past the backdrop into unlit body
# cavity -- the comment above it says exactly that -- and it did not reach far
# enough.  MEASURED on the mesh: y -0.5000 .. +0.4000 against a rear aperture of
# +-REAR_W/2 = +-0.5200, so 120.0 mm of the SHOW side and 20.0 mm of the off
# side saw straight past it; now 0.0 mm both sides.  Confirmed by LOOKING at
# hero34r: the ablated frame shows the wall's own vertical edge inside the
# aperture, the fixed frame does not.  T1_ENDSHORT=1 restores the short wall.
# NOT FIXED and NOT the same datum: gal_end_f (the FORWARD return) reaches only
# +0.2600, i.e. 260.0 mm short of that same half-width -- but the rear window is
# not what looks at it, so it needs its own sight line established first.
# NOT FIXED either: A7's actual defect is ILLUMINATION, not dressing.
ck "gal_end_a half-width DERIVED"        1 "$(grep -Fc 'S.REAR_W / 2.0' t1_detail.py)"
ck "T1_ENDSHORT ablation exists"         2 "$(grep -Fc 'T1_ENDSHORT' t1_detail.py)"
ck "build_selectors in rev42_uv"    2 "$(grep -c 'build_selectors' probe_rev42_uv.py)"
ck "C_FOOT in rev42_uv"             7 "$(grep -c 'C_FOOT' probe_rev42_uv.py)"
ck "571.71 in rev42_uv"             1 "$(grep -c '571.71' probe_rev42_uv.py)"
ck "190 in probe_dust_scope"        4 "$(grep -c '190' probe_dust_scope.py)"

# ---- symbols that have been mis-cited by LINE NUMBER before.  Locate by name. --
say "-- symbols located by name, not by line --"
ck "V_POW_Z defined once"           1 "$(grep -c '^V_POW_Z' t1_shell.py)"
ck "V_POW defined once"             1 "$(grep -c '^V_POW ' t1_mats.py)"
ck "DOOR_H in folk_gen.py"          1 "$(grep -c '^DOOR_H' folk_gen.py)"
ck "signboard gated on T1_SIGNBOARD" 3 "$(grep -c "T1_SIGNBOARD" t1_shell.py)"
ck "lidsign IS bound in build.py"   1 "$(grep -c '\"lidsign\"' build.py)"

# ------------------------------------------------------------------- artwork
# THESE THREE WILL CHANGE when SPEC 10.100.6 / 10.101's re-bake lands -- that is
# the POINT of the re-bake, not a regression.  When it does: re-run md5, paste the
# new hashes HERE, in the SAME commit as the new artwork, and say so in the
# handoff.  Never in a separate commit -- that is how a tripwire becomes a
# rubber stamp.
say "-- textures (unchanged since rev 25; item 1 WILL move them) --"
# ALL EIGHT.  Rev 43's first cut hashed only the three the brief happened to
# mention, which left senor.png (the only image meeting SPEC 5's 3K bar) and
# calidad.png (a live work item) unprotected.  If it is artwork, it is hashed.
# ===========================================================================
# rev 60b -- SIX TEXTURE HASHES RE-BASED, AND THE CAUSE IS F93.
#
# The generators were re-run at higher resolution to meet SPEC sec.5's floor:
#     folk_gen.py   N 2048 -> 4096      swirl.png, swirl_b.png
#     folk_gen.py   NOSE_TEX 1024->3072 nose.png
#     lid_gen.py    W 2048 -> 4096      lidmural.png, lidsign.png
#     cal_gen.py    W 2400 -> 3072      calidad.png  (4096 is OOM-killed here)
#
# THE ARTWORK DID NOT CHANGE, and that was checked rather than assumed, because
# A12 makes artwork the owner's call: swirl's ink coverage is 0.0225 -> 0.0226,
# and downsampling the new 4096 tile back to 2048 differs from the old file by
# a MEDIAN of 0.00 DN with 0.3 % of pixels over 32 DN -- edges only, which is
# what resampling a sharper edge looks like.  cal_gen's own centroid guard
# ("100%% calidad off center") still passes at -0.0001.
#
# rev 60b -- SPEC sec.5's 3K FLOOR IS NOW ASSERTED.  F93.
#
# THE DEFECT THIS ROW EXISTS FOR.  Every texture below is pinned BY MD5, so any
# change to one is caught -- but nothing anywhere asserted the thing SPEC sec.5
# actually requires: that a texture is big enough for the delivery frame.  F93
# sat open for revisions reading "ONE of EIGHT meets the 3K floor" with no row
# to make it fail.  A hash pins a file to its past; it does not pin it to a
# standard.  A 3840-wide delivery frame cannot be sharper than the textures in
# it, so this is the finish line's blocker and it is now a row.
#
# emblem.png is EXEMPT AND NAMED, not silently skipped (rule 27): texgen.py
# cannot run on this machine -- load_font raises "no usable font" for all four
# candidates -- so tex/emblem.png is a tracked build input the tree cannot
# reproduce at ANY resolution.  That is F115, and the exemption dies with it.
ck "every texture meets SPEC sec.5's 3K floor (emblem exempt, F115)" OK "$(python3 -c "
from PIL import Image
import glob, os
bad = []
for f in sorted(glob.glob('tex/*.png')):
    n = os.path.basename(f)
    if n in ('emblem.png',) or n.startswith('prev_'):
        continue
    im = Image.open(f)
    if max(im.size) < 3072:
        bad.append('%s %dx%d' % (n, im.width, im.height))
print('OK' if not bad else 'UNDER 3072: ' + '; '.join(bad))" 2>&1 | tail -1)"
ck "and emblem.png is the ONLY exemption" 1 "$(python3 -c "
from PIL import Image
import glob, os
n = sum(1 for f in glob.glob('tex/*.png')
        if not os.path.basename(f).startswith('prev_')
        and max(Image.open(f).size) < 3072)
print(n)" 2>&1 | tail -1)"

ck "tex/swirl.png"   94577b44f9f4b4eab1f6fcb6d811e955 "$(md5of tex/swirl.png)"
ck "tex/swirl_b.png" eaa09315a6905d9ed9151fd4e511ed86 "$(md5of tex/swirl_b.png)"
ck "tex/nose.png"    34b3d81a74f366a6fd849612b2293e0c "$(md5of tex/nose.png)"
# rev 46, SPEC 10.120: RE-BASED because 'Senor' was very nearly invisible.
# Measured per WORD -- which nobody had done, and which dissolves the standing
# contradiction between ledger findings 19 and 30 -- Michelson against the red
# each word sits on:  Tacombi 0.4673 photographed / 0.4480 built (right), Senor
# 0.1922 photographed / 0.0711 built (2.7x too dark).  'Tacombi' was never the
# problem.  The tarnish lift is DERIVED from the photographed target, not typed.
# rev 47, SPEC 10.121: RE-BASED because the texture legitimately changed.  The
# generator no longer LANCZOS-magnifies the 271-px mask-space crop 15.11x to
# OUT_W; it crops and resizes the raster Canvas actually drew, 3252 px -> 4096,
# a 1.260x resize.  The 10-90 alpha edge width over the mean stroke width went
# 0.0924 -> 0.0062.  MASK SPACE IS BIT-IDENTICAL ACROSS THIS CHANGE -- build()
# and senor_only() hash 4a6f4e8cd0489fa1 / 82d6cf56dd660b47 before and after --
# so every mask-space figure in this project still holds.  Only the emitted
# texture moved, and this row is re-based, never relaxed.
# rev 59, F67: RE-BASED because the artwork legitimately changed -- the `n~` had
# no tilde.  senor_trace.py's baked reference was a segmentation that predates
# the tilde, the trace was fitted to it, and SPUR_PRUNE_PX had eaten what little
# survived: `_STROKES` carried only a 3 px vertical stub and a lone inscribed
# disc where the stroke belongs.  One ("ntilde", ...) stroke replaces both.
# THE CAUSE IS SEPARATELY TESTABLE, which is what licenses this re-base:
# "the tilde is DRAWN, not pruned" below counts ink in the tilde band off the
# raster (73 px before, 156 after, 186 in the reference), and "senor_trace's
# baked mask == compare_script's live mask" is the row that would have caught
# the whole thing fifty revisions ago.  Mask space is NOT bit-identical across
# this change and is not claimed to be: compare_script's `Senor` box goes
# 0.825 -> 0.889 and the whole lockup 0.942 -> 0.950, both watched printing.
# rev 61: RE-BASED AGAIN, and the cause is an OWNER RULING, not a measurement.
#   [owner, rev 61] "senor Tacombi should be clearer in the render than in that
#   photo. Well defined. I want this 3d model to look like new. Enhanced from
#   the photo"
# The `S` arrived from the chromaticity segmentation in three pieces because
# the word is TARNISHED in ref_side.jpg.  senor_trace.py reproduced those
# breaks deliberately and recorded that undoing them "is an OWNER decision,
# not this file's".  He has now made it, so the `S` is bridged and the texture
# legitimately changed.
# THE CAUSE IS SEPARATELY TESTABLE, which is what licenses this re-base: the
# row below counts the `S`'s CONNECTED COMPONENTS off the raster, so a future
# context cannot quietly undo the ruling and still pass this checksum.
# WATCHED BOTH WAYS: shipped 1 component [361 px]; T1_SENOR_BREAKS=1 gives 3
# [251, 61, 14].  IoU against the TARNISHED mask FALLS by design (Senor
# 0.8859 -> 0.8602) and MUST NOT be "repaired" -- see senor_trace.py.
# ===========================================================================
# rev 62 -- RE-BASED, AND THE CAUSE IS AN OWNER RULING, NOT A REPAIR.
#
# He was shown probe_scratch/rev62_q_senor.png -- the photograph and the render
# of the same word at the same mm/px -- and asked which finish he wanted on
# `Senor`.  Four options; he chose "Bright silver, same as Tacombi".  That
# overrides SPEC sec.3's WEATHERED lock FOR THIS WORD ONLY, and the rev-62 brief
# sec.4 had already flagged the collision and required it be surfaced to him
# rather than decided silently.  script_gen.SENOR_TARNISH = 0.0 ships it.
#
# THE COMPANION ROW, which is what makes this a re-base and not a rubber stamp
# (CLAUDE.md, "a re-base is allowed only with the cause named AND a companion
# row that makes the cause separately testable"): the row below re-runs
# script_gen with T1_SENOR_TARNISH=1 and asserts it reproduces the PRE-RULING
# texture BYTE FOR BYTE.  So the ruling is reversible, the measured TARNISH_K
# and SENOR_MICHELSON are provably still live, and this hash moved for the
# stated cause and no other.  WATCHED: the word's luma goes 117.1 -> 201.1
# against a clean silver of 210.9, and the b flag, i dot and swash zones are
# untouched.
# ===========================================================================
# ===========================================================================
# rev 62 -- THE DELIVERY PATH (T1_ALPHA).  The owner ruled the render goes on
# "different backgrounds for promotional material", so studio.py grew an RGBA
# branch.  TWO THINGS MUST STAY TRUE and neither is obvious from reading it:
#
#   1  IT IS OFF BY DEFAULT.  Every frame this project has ever judged came
#      through composite_on_white's AlphaOver onto SPEC sec.6's pure white.  If
#      T1_ALPHA ever defaults ON, every gate in this repository starts scoring
#      a transparent frame against a white-background reference and the whole
#      fidelity lane goes quietly wrong.
#   2  THE BRANCH RETURNS BEFORE THE AlphaOver, NOT AFTER.  matte_tap.__doc__
#      records the defect it exists to avoid: downstream of that node the alpha
#      is 1 everywhere and the silhouette is UNRECOVERABLE.  A branch placed one
#      node too late produces a file that HAS an alpha channel and carries no
#      information -- which is exactly the failure that went unnoticed for
#      sixty-two revisions.  This row is ORDINAL and needs no render.
# ===========================================================================
# ===========================================================================
# rev 62 -- THE EMBLEM CARRIER.  THIS ROW EXISTS BECAUSE THE PROJECT ALREADY
# LOST THIS EXACT THING ONCE.
#
# At rev 45 the correct method for the owner's top item was written down --
# "build the canonical mark and use the photograph to VERIFY" -- and it then
# survived ONLY in LEDGER_rev45.md and NEXT_CONTEXT_PROMPT_rev46.md, both
# superseded and never opened again.  Seventeen revisions kept deriving the
# glyph from a 41 px badge because no live document carried the instruction.
# That is rule 16's failure mode, and prose cannot guard against it -- a
# sentence saying "do not drop this" is exactly what got dropped.
#
# So: the file must EXIST, and the three intake doors must NAME it.  If a
# future context compacts it away, this goes red instead of the loss going
# unnoticed for seventeen revisions.
# ===========================================================================
ck "EMBLEM_HANDOFF.md exists"  1 "$(ls EMBLEM_HANDOFF.md >/dev/null 2>&1 && echo 1 || echo 0)"
# THIS ROW'S FIRST CUT WAS WRONG AND SCORED 2 ON A CORRECT TREE, twice over:
# `grep -lc` is contradictory (-c overrides -l), and it referenced
# $_LATEST_BRIEF five hundred lines BEFORE that variable is assigned, so it
# grepped an empty filename.  It finds the brief itself now.  Watched failing
# by removing the pointer from START_HERE.md, and watched passing on restore.
_EMB_BRIEF="$(ls NEXT_CONTEXT_PROMPT_rev*.md 2>/dev/null | sort -V | tail -1)"
ck "README, START_HERE and the newest brief NAME the emblem carrier" 3 \
   "$(( $(grep -q EMBLEM_HANDOFF.md README.md 2>/dev/null && echo 1 || echo 0) \
      + $(grep -q EMBLEM_HANDOFF.md START_HERE.md 2>/dev/null && echo 1 || echo 0) \
      + $(grep -q EMBLEM_HANDOFF.md "$_EMB_BRIEF" 2>/dev/null && echo 1 || echo 0) ))"
ck "the carrier still states the OWNER'S OWN sentence" 1 \
   "$(grep -c 'publicly available emblem' EMBLEM_HANDOFF.md)"
ck "T1_ALPHA defaults OFF -- the shipped path is still white" 1 \
   "$(grep -c 'os.environ.get("T1_ALPHA", "0")' studio.py)"
# NOTE ON THIS ROW, because its first cut was WRONG and passed nothing:
# `T1_ALPHA` is read TWICE in studio.py -- once in composite_on_white (the
# branch) and once in setup_render (the colour mode), and setup_render sits
# BELOW the AlphaOver.  A bare `{a=NR}` keeps overwriting and lands on the
# second one, so the row reported "no" about correct code.  It must take the
# FIRST occurrence.  Watched failing on the wrong version and on a branch moved
# below the AlphaOver by hand.
ck "the T1_ALPHA branch returns BEFORE the AlphaOver" yes \
   "$(awk '/if _alpha_delivery\(\):/{if(!a)a=NR} /lay over pure white/{if(!b)b=NR} END{print (a&&b&&a<b)?"yes":"no"}' studio.py)"
ck "deliver.py refuses a set it cannot verify" 1 \
   "$(grep -c 'PACKAGE IS NOT TRUSTWORTHY' deliver.py)"
ck "tex/senor.png"   3491b72149707950e51d6be4ca31f33f "$(md5of tex/senor.png)"
ck "T1_SENOR_TARNISH=1 restores the PRE-RULING texture byte for byte" yes \
   "$(cp tex/senor.png /tmp/_vc_senor.png 2>/dev/null; \
      T1_SENOR_TARNISH=1 python3 script_gen.py >/dev/null 2>&1; \
      if cmp -s tex/senor.png /tmp/_vc_senor_pre.png 2>/dev/null || \
         [ "$(md5of tex/senor.png)" = "adcf908f0c3c078c45f8d305d470796a" ]; \
      then echo yes; else echo no; fi; \
      cp /tmp/_vc_senor.png tex/senor.png 2>/dev/null)"
ck "the S is ONE letter, per the owner's rev-61 ruling"  1 \
   "$(python3 senor_trace.py 2>/dev/null | grep -o 'rasterised `S` components: [0-9]*' | awk '{print $NF}')"
# rev 45, SPEC 10.112: RE-BASED because the texture legitimately changed.
# cal_gen.gradient's bias was 0.42 and `t` is zero at the burst's own centre by
# construction, so the core evaluated to 84 % ORANGE and NOTHING in the shipped
# texture was the RED = (214,46,30) that starburst() fills the polygon with nine
# lines above.  Core measured off the shipped file: (237.0,120.3,22.0), G/R
# 0.508.  Bias -> 0; core now (216.6,55.1,28.2), G/R 0.255, against the body
# red's own 0.250.  The owner reported this decal twice.
# rev 46, SPEC 10.118: RE-BASED AGAIN, and again because the texture legitimately
# changed.  The owner reported "the 100% calidad off center".  The type's
# centroid sat 0.1167 w LEFT and 0.1117 h BELOW starburst()'s centre -- "100%"
# hung off the burst onto bare cream and "Calidad" ran off the panel's bottom
# edge.  cal_gen now anchors the block to BURST_CX/BURST_CY and rotates it about
# that same point, and CARRIES ITS OWN GUARD: it refuses to write a decal whose
# type is more than 0.004 off centre.  Watched fail at (-0.1099, +0.1127) on the
# rev-45 layout and at (-0.0132, +0.0134) on 12 % of the correction.
# rev 47, W4: RE-BASED because the artwork legitimately changed.  "100%" and
# "Calidad" shared 1110 pixels; they now share 0, with a clear gap of 0.0258 of
# the canvas height.  Re-based, never relaxed.
# rev 47b: RE-BASED again, and this time against a PHOTOGRAPH.  He looked at
# LINE_GAP 0.26 and said the words still did not read as two.  IMG_2073.jpeg
# arrived and shows the burst at 44x61 px instead of ref_playa_34's 23x39, and
# the words separate under a mask.  Measured as a RATIO against the same
# estimator run on the build (its +34% absolute bias divides out): photographed
# 0.244 vs built 0.149 => 1.64x, so LINE_GAP 0.26 -> 0.43.
# rev 48: RE-BASED because the artwork legitimately changed, and because HE
# settled what the marks above the burst are.  Shown a three-way crop -- the
# RED bus (ref_side.jpg, the target vehicle), the GREEN bus (IMG_2073.jpeg)
# and the build -- he ruled: "They are actually stars that were not properly
# represented."  Rev 45 drew them as BUNTING; rev 46 retired them at his
# instruction AND recorded the reason as "no frame we hold shows them", which
# ref_side.jpg refutes at 7x.  Their PRESENCE was never the error.  Their
# IDENTITY was, and only he could settle it.  Re-based, never relaxed.
ck "tex/calidad.png" 4dcde8e8df8ff32b44291189368495ad "$(md5of tex/calidad.png)"
# rev 50: RE-BASED because the TYPE legitimately changed, and the change is
# checkable independently of the checksum -- see the clamp row below, added in
# the same edit so this line cannot be re-based back without it.
# lid_gen's top-strip fit was the file's ONLY unclamped text scale.  Two
# measured quantities are in play, each word's x-run (read off ref_side.jpg)
# and the cap height (0.46 of the strip, stated at lid_gen.py:184), and a
# substitute face cannot meet both.  Unclamped, it silently sacrificed the CAP
# HEIGHT.  Measured on the texture, against the declared 0.460:
#     before   FRESH 0.421  JUICES, 0.553  GOURMET TACOS 0.386  TORTAS 0.421
#              &  0.728   <- 1.58x its own recorded measurement
#     after    the four words BIT-UNCHANGED, &  0.474  <- 1.03x
# so the clamp bit only on the glyph that was being enlarged.  The photograph
# sets the & at cap height with the rest of the line.  Re-based, never relaxed.
ck "tex/lidmural.png" 9776e6aef0114dbc209d148811b504d7 "$(md5of tex/lidmural.png)"
# COMPENSATING ROW, same edit.  A checksum re-base is only honest if the reason
# is separately testable; rev 49c set that precedent when it widened one grep
# window and added three rows in the same commit.  This one asserts the clamp
# itself, in the file's own idiom, so the texture cannot drift back silently.
# NOTE the leading `^ *` on both greps.  Without it they count MENTIONS, not
# call sites: my own comment two lines above quotes the sibling form verbatim,
# so the sibling row read 3 against a typed 2 and went red on its first run.
# Rule 4 -- never put a figure in an acceptance test unless you watched it
# print -- caught by the instrument, on the instrument's author.
ck "the header fit is CLAMPED, never enlarging" 1 \
   "$(grep -cE '^ *k = min\(1\.0, \(x1 - x0\) / wpx\)' lid_gen.py)"
# and its two siblings, which are where that idiom comes from
ck "lid_gen's sibling text fits still clamp" 2 \
   "$(grep -cE '^ *k = min\(1\.0, (wpx / tot|wid \* 0\.86 / wpx)\)' lid_gen.py)"
ck "tex/lidsign.png" 876a5e376a69dcd56ffaed7f60f13714 "$(md5of tex/lidsign.png)"
ck "tex/emblem.png"  574ba2d733353387568b412da48fd436 "$(md5of tex/emblem.png)"

# ------------------------------------------------------------------- gitignore
# ---------------------------------------------------------------------------
# VALUES, NOT JUST OCCURRENCES.
# The first cut of this script tested that a symbol EXISTS.  `grep -c '^V_POW '`
# returns 1 whether the constant reads 0.60 or 0.45 -- and section 6 item 5
# proposes moving exactly that constant.  A check that cannot see the change it
# was written to guard is not a check.
# ---------------------------------------------------------------------------
say "-- locked VALUES --"
ck "V_POW is 0.52"                  1 "$(grep -c '^V_POW = 0.52' t1_mats.py)"
ck "V_POW_Z is 0.52"                1 "$(grep -c '^V_POW_Z = 0.52' t1_shell.py)"
ck "V_POW and V_POW_Z agree"       yes "$(if [ \"$(grep -o '^V_POW = [0-9.]*' t1_mats.py | awk '{print $3}')\" = \"$(grep -o '^V_POW_Z = [0-9.]*' t1_shell.py | awk '{print $3}')\" ]; then echo yes; else echo NO; fi)"
ck "DOOR_H art datum is 1.013467"   1 "$(grep -c '1.013467 m' folk_gen.py)"
# POLARITY, not presence.  The signboard is RETIRED from the vehicle; flipping
# the default to "1" leaves the occurrence count at 3 and puts a panel he
# removed into every hero.
ck "signboard default is OFF"       1 "$(grep -c 'T1_SIGNBOARD\", \"0\"' t1_shell.py)"
# rev 46, W1.  VALUE, NOT OCCURRENCE, and the DERIVATION, not the result:
# TYPE_SHIFT must stay EXPRESSED as (burst centre - measured pre-rotation
# centroid) (SPEC 10.25).  Freezing the arithmetic result +0.1315/-0.0559 as a
# literal would pass this grep and silently decouple the type from the burst the
# next time a glyph moves.  The block must also rotate about the burst's own
# centre -- rotating about anything else swings a correctly-laid-out block back
# off centre, which is exactly what (0.500, 0.600) was doing.
ck "calidad burst centre is 0.505/0.575"  1 "$(grep -c '^BURST_CX, BURST_CY = 0.505, 0.575' cal_gen.py)"
# rev 47.  THE RATIONALE IS KEPT AND THE SHAPE IS REPLACED -- rule 5, do not
# inherit a guard's rationale along with its shape.  rev 46 satisfied "derived"
# by expressing TYPE_SHIFT against a FROZEN measured centroid,
# TYPE_PRE_CENTROID = (0.3735, 0.6309).  That is derived only for rev 46's
# spacing.  W4 had to open the gap between the two words, the pre-rotation
# centroid moved to 0.6607, and a frozen figure would have swung the block back
# off the burst -- the exact trap the rev-47 brief names.  TYPE_SHIFT is now
# COMPUTED at generation time from the centroid of the actual laid-out type, so
# it re-derives after any glyph, size or spacing change.
# THESE ROWS ARE STRICTLY STRONGER THAN THE GREP THEY REPLACE: the derivation
# must be PRESENT and the frozen literal must be GONE.  A revision that goes
# back to a typed centroid now fails on row two even if it keeps row one.
ck "calidad TYPE_SHIFT is DERIVED at run time" 1 "$(grep -c 'TYPE_SHIFT = (BURST_CX - _pre\[0\], BURST_CY - _pre\[1\])' cal_gen.py)"
ck "calidad centroid is NOT a frozen literal"  0 "$(grep -c '^TYPE_PRE_CENTROID' cal_gen.py)"
# rev 47b: THIS ROW DID ITS JOB AND WENT RED, so it is restated rather than
# deleted.  At rev 47 LINE_GAP was a placeholder and the row required it to SAY
# SO, so that nobody could quietly promote a guess into a measurement.  It was
# then promoted -- but not quietly: he sent IMG_2073.jpeg, the burst is 44x61 px
# there instead of 23x39, and probe_rev47_gap measured the gap as a RATIO
# against the same estimator run on the build.  The row now requires the
# PROVENANCE to be cited in the source, which is the same protection one step
# on: a future revision cannot retune LINE_GAP by eye without deleting a
# reference to the probe and the frame it was measured from.
# PRESENCE, not occurrence count.  A `grep -c` here is a latent false positive:
# it went red at "got 2, want 1" purely because the provenance is cited on two
# lines, which is not a defect.  A row that fires on a harmless duplicate is the
# cry-wolf failure bootstrap.sh's stranded-branch check already had to fix once.
ck "calidad LINE_GAP cites its provenance"     1 "$(grep -q 'probe_rev47_gap' cal_gen.py && echo 1 || echo 0)"
ck "calidad LINE_GAP names its frame"          1 "$(grep -q 'IMG_2073' cal_gen.py && echo 1 || echo 0)"
# rev 48: TWO MORE, because the frame it names is the WRONG VEHICLE.  He has
# ruled the RED bus is the target and that artwork may not transfer; 0.244 was
# measured on the GREEN one.  0.43 is kept because the red bus can only bound
# the gap to 0.25..0.47 and BOTH 0.43 and the corrected 0.376 sit inside that
# -- but it must keep declaring what it is, and it must keep carrying the
# retraction of the ratio argument that produced it.
ck "LINE_GAP declares it is TRANSFERRED"  1 "$(grep -q 'TRANSFERRED FROM ANOTHER VEHICLE' cal_gen.py && echo 1 || echo 0)"
ck "the +34% ratio argument stays retracted" 1 "$(grep -q 'FOUNDING CASE REFUTED' cal_gen.py && echo 1 || echo 0)"
ck "calidad type rotates about the burst" 1 "$(grep -c 'center=(w \* BURST_CX, h \* BURST_CY)' cal_gen.py)"
ck "calidad generator carries its guard"  1 "$(grep -c 'cal_gen GUARD FAILED' cal_gen.py)"
# rev 46, at the OWNER'S instruction, in two stages.  The Calidad decal drew two
# red bars with 15 triangular pennants hanging from them.  He asked for the
# triangles to go -- no frame we hold shows them -- and then named what the
# remaining lines are: VENT SLATS.  They are the T1's rear air-intake louvres,
# and cal_gen was painting them in saturated red inside a decal texture.  The
# whole feature is retired.
# rev 48 CORRECTION, and it was overdue.  This comment said the slats are
# "DARK GREY shadowed slots in sheet metal".  LEDGER_rev47.md sec.10c retracted
# that at rev 47 -- they are BODY COLOUR, and read dark only because each
# pressed slot SELF-SHADOWS -- but nobody updated this file, so the machine
# went on handing the retracted reading to every context that read it.  A
# retraction that lands in a ledger and not in the source is half a retraction
# (rule 15).
# rev 48, SECOND CORRECTION, larger.  LEDGER_rev46.md sec.5 concluded from the
# retirement of these painted lines that "THE MODEL HAS NO REAR VENTS", and
# rev 47 and this revision's brief both inherited it.  IT IS FALSE, and false
# against the BUILD: t1_detail.louvres() has built 10 pressed louvres per
# flank, 20 in all, for many revisions.  The painted bunting sat between the
# roof and the burst; the real louvres are on the quarter panel half a metre
# below.  Retiring the paint was right; concluding the geometry was missing
# chained a second error onto the first.  Guarded below.
# ABSENCE, checked three ways, because a feature that comes back halfway is
# exactly how this one survived: the function, the pennant loop, and the colour
# constant must all be gone.
ck "calidad bunting function gone"   0 "$(grep -c '^def bunting' cal_gen.py)"
# ------------------------------------------------------- rev 48: THE STARS
# The bunting stays retired -- he never asked for pennants back, he said the
# marks were always stars.  So the three absence rows above still stand AND
# the stars must be present.  Both, not either.
ck "calidad draws the star band"     1 "$(grep -qE '^def _stars' cal_gen.py && echo 1 || echo 0)"
ck "calidad stars derive from the burst" 1 "$(grep -q 'bw = RO \* 2.0' cal_gen.py && echo 1 || echo 0)"
# THE ROW THAT MATTERS.  Both red frames are BLOWN, so the mark band comes
# back as ONE merged 1499-px component and the COUNT is not derivable from the
# target vehicle at all.  STAR_N is a pose choice and must keep saying so --
# the LINE_GAP precedent, applied before the defect rather than after it.
ck "STAR_N declares itself NOT MEASURED" 1 "$(grep -A 3 '^STAR_N' cal_gen.py | grep -q 'NOT MEASURED' && echo 1 || echo 0)"
# And the clamp must keep REPORTING what it drops.  The measured band runs to
# +-1.64 RO and this decal's rectangle holds +-1.38 RO, so two band positions
# fall outside the texture entirely.  A cap nobody logs reads as coverage.
ck "the star clamp reports what it drops" 1 "$(grep -q 'fall OUTSIDE this decal' cal_gen.py && echo 1 || echo 0)"

# ---------------------------------------------------- rev 48, JOB 2 and JOB 1
# THE REAR LOUVRES EXIST.  Three documents said they did not.  These rows make
# that un-sayable again: the builder, the count and the call site must all be
# present.  PRESENCE tests, not occurrence counts -- the cry-wolf lesson above.
ck "rear louvres are BUILT geometry"      1 "$(grep -qE '^def louvres\(' t1_detail.py && echo 1 || echo 0)"
ck "rear louvre count is 10 per flank"    1 "$(grep -c '^LOUV_N = 10' t1_detail.py)"
ck "rear louvres are called from the build" 1 "$(grep -q 'louvres()' t1_detail.py && echo 1 || echo 0)"
# rev 48, the SECOND half of JOB 2 and the one that was actually open.  The
# blades were never the problem; the UNBROKEN FLANK behind them was.  A T1
# louvre is an aperture, and the fidelity bar he set (bus_model_ref.JPG) has
# modelled slots that self-shadow.  Signed modulation +0.0343 -> -0.2559 on
# probe_rev48_louv, i.e. the slats stopped catching the key and started
# shadowing themselves, which is the sign the photograph has.
ck "the louvre APERTURES are cut"    1 "$(grep -qE '^def louvre_cutters' t1_detail.py && echo 1 || echo 0)"
ck "build.py cuts the louvre apertures" 1 "$(grep -q 'louvre_cutters' build.py && echo 1 || echo 0)"
# AND THE BAY BEHIND THEM, WHICH IS NOT OPTIONAL.  Cut without it, the slots
# look straight into the lit cabin: the first render came back with BRIGHT
# WHITE BARS among the slots while every number said the change had worked.
ck "the louvre apertures are BACKED" 1 "$(grep -qE '^def louvre_backing' t1_detail.py && echo 1 || echo 0)"
ck "build.py builds the louvre bay"  1 "$(grep -q 'louvre_backing' build.py && echo 1 || echo 0)"
# The blade section must stay DERIVED from the measured pitch and the inferred
# aperture.  The authored 11.0 mm reconciled with neither, and could not show
# it while the shell was solid behind it.
ck "the blade section is DERIVED"    1 "$(grep -q 'LOUV_SECT = LOUV_PITCH - LOUV_APERTURE' t1_detail.py && echo 1 || echo 0)"
ck "LOUV_APERTURE declares itself INFERRED" 1 "$(grep -A 3 '^LOUV_APERTURE' t1_detail.py | grep -q 'INFERRED' && echo 1 || echo 0)"
# The count is not merely present, it is CONFIRMED against a photograph: 10
# slats on IMG_2073.jpeg (rows 468-582, cols 1156-1188, de-sheared s = -0.180),
# pitch 8.106 +/- 0.023 px.  That is GEOMETRY, and the owner has ruled geometry
# transfers between his two vehicles ("the geometry appears the same"), so the
# green frame is admissible here where it would not be for paint or artwork.

# THE TRUNK LID OPENS.  His newest requirement, built at rev 48.
ck "trunk lid is separated and hinged"    1 "$(grep -qE '^def split_trunk_lid' t1_shell.py && echo 1 || echo 0)"
ck "trunk lid has a LATERAL hinge"        1 "$(grep -qE '^def _hinge_y' t1_shell.py && echo 1 || echo 0)"
ck "build.py separates the trunk lid"     1 "$(grep -q 'split_trunk_lid' build.py && echo 1 || echo 0)"
# THE ROW THAT MATTERS MOST, and it is the LINE_GAP lesson applied before the
# defect rather than after it.  No frame in this project shows the trunk open,
# so any NON-ZERO TRUNK_OPEN_DEG is a POSE CHOICE and not a measurement.  This
# requires it to keep SAYING SO.  A later revision cannot quietly promote 52 deg
# into a measured angle without deleting the words that admit it is not one.
#
# RESTATED AT REV 49, NOT RELAXED (rule 5: keep the rationale, replace the
# shape).  The single row was `grep -A 3`, which assumed the declaration sits
# within three lines of the constant.  The owner then ruled the lid SHUT --
# "leave the lower bay shut, just have the back trunk window open for service"
# -- and the citation of that ruling now sits between the constant and its
# NOT-MEASURED declaration, so the row went red on a source that had become
# MORE honest, not less.  A row that fires when the thing it guards improves is
# the right row with the wrong window.
#
# WIDENING THE WINDOW ALONE WOULD BE A RELAXATION, so it does not happen alone.
# The window widens to the constant's whole comment block AND a second row is
# added requiring the shut state to keep citing the owner.  Net: strictly
# stronger.  A future revision cannot reopen the lid without either restoring a
# NOT-MEASURED declaration or deleting a reference to his words.
ck "TRUNK_OPEN_DEG declares itself NOT MEASURED" 1 "$(grep -A 30 '^TRUNK_OPEN_DEG' t1_shell.py | grep -q 'NOT MEASURED' && echo 1 || echo 0)"
ck "TRUNK_OPEN_DEG=0 cites the SHUT ruling" 1 "$(grep -A 30 '^TRUNK_OPEN_DEG' t1_shell.py | grep -q 'SHUT, BY THE OWNER' && echo 1 || echo 0)"
# And the lid must not be SWUNG at zero: _swing_open() asserts the free edge
# travels, so a shut lid run through it would fire a guard on a correct pose.
ck "a SHUT trunk lid skips the swing, not runs it at zero" 1 "$(grep -q 'abs(TRUNK_OPEN_DEG) < 1e-6' t1_shell.py && echo 1 || echo 0)"
# ---------------------------------------------------------------- THE TAIL BOARD
# rev 49e.  The photorealism survey's record audit found the tail board had ZERO
# rows in either verifier -- the project's NEWEST object, carrying the MOST pose
# choices and the LEAST measurement, entirely unguarded.  These rows exist so a
# later revision cannot quietly promote a pose choice into a measurement, and
# cannot lose the station solve that dissolved rev 49b's declared 80 mm.
ck "the tail board is built"                1 "$(grep -qE '^def tail_board' t1_shell.py && echo 1 || echo 0)"
ck "build.py raises the tail board"         1 "$(grep -q 'S.tail_board(' build.py && echo 1 || echo 0)"
# TB_WIDTH and the lateral centring cannot be measured from anything we hold --
# parallax bounds the width above and gives NO lower bound.  They must keep
# saying so.  This is the LINE_GAP lesson applied before the defect.
ck "TB_WIDTH declares itself a POSE CHOICE" 1 "$(grep -A 2 '^TB_WIDTH' t1_shell.py | grep -q 'POSE CHOICE' && echo 1 || echo 0)"
ck "TB_WIDTH keeps its parallax upper bound" 1 "$(grep -B 12 '^TB_WIDTH' t1_shell.py | grep -q '0.59' && echo 1 || echo 0)"
ck "TB_Y_CENTRE declares itself a POSE CHOICE" 1 "$(grep -A 2 '^TB_Y_CENTRE' t1_shell.py | grep -q 'POSE CHOICE' && echo 1 || echo 0)"
ck "TB_TILT_DEG states WHICH DATUM"         1 "$(grep -A 3 '^TB_TILT_DEG' t1_shell.py | grep -q 'HORIZONTAL' && echo 1 || echo 0)"
# The station is SOLVED from T1_body's own vertices at run time.  A literal here
# would go stale the moment the shell moves, and would silently re-open the
# 97 mm burial.
ck "the board station is SOLVED, not typed" 1 "$(grep -q 'station SOLVED from the skin' t1_shell.py && echo 1 || echo 0)"
ck "the board foot is guarded against the SKIN" 1 "$(grep -q 'measured roof skin at z' t1_shell.py && echo 1 || echo 0)"
# The guard rev 49b first wrote compared ZT_ALL against ZT_ALL and could never
# fire.  This row refuses the return of a self-referential foot check.
ck "the foot guard is NOT self-referential" 0 "$(grep -c '_crown = T.ZT_ALL' t1_shell.py)"

# rev 49: the lining sat 2.0 mm PROUD of the tail skin and rendered THROUGH the
# closed lid.  Invisible for a revision because the lid was open.  Guarded now.
ck "the trunk bay lining is guarded INBOARD of the skin" 1 "$(grep -q 'is PROUD of the tail skin' t1_shell.py && echo 1 || echo 0)"
# And the tail hardware must travel with the lid it is mounted on.  If a future
# edit swings the lid and leaves the handle floating in mid-air at the closed
# position, this row goes red before anyone renders it.
ck "the trunk bay is a LINING, not contents" 1 "$(grep -q 'contents NOT invented' t1_shell.py && echo 1 || echo 0)"
ck "the rear hatch opens"                 1 "$(grep -qE '^def open_rear_hatch' t1_shell.py && echo 1 || echo 0)"
ck "REAR_OPEN_DEG declares itself NOT MEASURED" 1 "$(grep -A 3 '^REAR_OPEN_DEG' t1_shell.py | grep -q 'NOT MEASURED' && echo 1 || echo 0)"
ck "the T-handle rides the trunk lid"     1 "$(grep -q 'englid_handle' build.py && echo 1 || echo 0)"
ck "the 1963 plate rides the trunk lid"   1 "$(grep -q 'plate_1963\"' build.py && echo 1 || echo 0)"
ck "calidad pennant loop gone"       0 "$(grep -c 'ay + by) / 2 + drop' cal_gen.py)"
ck "calidad BUNT colour retired"     0 "$(grep -c '^BUNT = ' cal_gen.py)"
# rev 46, W2.  The VW glyph's vertical proportions, SOLVED against the
# photograph by probe_rev46_vw.py, not typed.  VALUES, not occurrences: the
# whole point of section 6 item 5's warning is that `grep -c '^VW_APEX_Z'`
# returns 1 whether the constant reads 0.284 or 0.1250, and 0.284 is the value
# the owner reported wrong four times running.
# rev 63 -- RE-BASED, ALL SIX TOGETHER, WITH THE CAUSE NAMED.
# CAUSE: the six rev-46 values built a glyph the owner reported as an X SIX
# times.  They are replaced by the spine fitted to a CANONICAL VECTOR of the
# mark (`vw_canonical_2019.svg`, obtained at rev 63 -- the first non-photographic
# source this project has ever had), at IoU 0.7979 against it, converged with no
# parameter on a bound.  Rendered on the nose it reads as a V over a W where the
# old one read as an X: probe_scratch/rev63_emblem_ba2.png, BEFORE | AFTER.
# WHAT IT COSTS, STATED: C6 is still one cell short (6 against the photograph's
# 7) and C4/C5 go red because the landmark set no longer describes this
# topology -- EMBLEM_HANDOFF.md sec.6 predicted exactly that and says to re-read
# them, not to assume them.  C7, C6's own kill, is ALIVE here (6 -> 5), which
# F176 makes a PRECONDITION for reading C6 at all.
ck "VW_APEX_Z is 0.0538"            1 "$(grep -c '^VW_APEX_Z = 0.0538' t1_core.py)"
ck "VW_V_TIP_X is 0.3287"           1 "$(grep -c '^VW_V_TIP_X = 0.3287' t1_core.py)"
ck "VW_W_ARM_X is 1.1002"           1 "$(grep -c '^VW_W_ARM_X = 1.1002' t1_core.py)"
ck "VW_W_ARM_Z is 0.4350"           1 "$(grep -c '^VW_W_ARM_Z = 0.4350' t1_core.py)"
ck "VW_W_TROUGH_X is 0.3111"        1 "$(grep -c '^VW_W_TROUGH_X = 0.3111' t1_core.py)"
ck "VW_W_TROUGH_Z is -0.6445"       1 "$(grep -c '^VW_W_TROUGH_Z = -0.6445' t1_core.py)"
# THE COMPANION ROWS, which is what licenses the re-base above.
# 1. THE NOSE'S STROKE WEIGHT IS A SEPARATE CONSTANT FROM THE HUBCAP'S, and
#    rev 63 shipped one into the other for a whole render before the raster and
#    the render disagreeing exposed it (F178).  Neither was checked BY VALUE by
#    anything.  Both are now, so that trap cannot be re-entered silently.
# rev 66 -- RE-BASED 0.1800 -> 0.2283, WITH THE CAUSE NAMED (F204).
# CAUSE: two independent statistics that share no ruler both say the nose's
# stroke was ~24 % too thin, which is the owner's own words at rev 64 ("the
# strokes are thinner than the pressing's").  probe_rev46_vw.py's OWN L6 --
# stroke width / ring width at the SAME ROW, so the viewing angle cancels --
# read built 0.1178 against the photograph's 0.1528 and crosses it at 0.2283.
# Ink strictly inboard of the band, both sides through one function, read built
# 0.432 against 0.525 +- 0.055 and crosses at 0.2280.  THE TWO AGREE TO 0.1 %.
# L6 had been reading low since rev 46 and was never acted on because it sat
# inside a residual that was 96 % ONE BROKEN LANDMARK (F203).
ck "NOSE stroke weight is 0.2283"   1 "$(grep -c 'def vw_logo_fit(ring_r, x=2.1215, depth=0.0110, wfrac=0.2283)' t1_detail.py)"
# THE COMPANION ROWS THAT MAKE THAT RE-BASE SEPARATELY TESTABLE.
ck "and the ink fit records its ceiling" 1 "$(grep -c 'CEILING: the photographed roundel is 41 x 69 px' t1_detail.py)"
ck "L6 is quoted first, not the ink"     1 "$(grep -c 'which is why it is the one quoted first' t1_detail.py)"
ck "HUBCAP stroke weight is 0.2087" 1 "$(grep -c '^CAP_EMBLEM_WFRAC = 0.2087' t1_detail.py)"
# 2. the provenance of the new spine is ON THE REPO and is not a sentence.
ck "the canonical mark is committed" 1 "$(ls vw_canonical_2019.svg 2>/dev/null | wc -l | tr -d '[:space:]')"
ck "it is NOT named ref_*"          0 "$(ls ref_vw_canonical.svg 2>/dev/null | wc -l | tr -d '[:space:]')"
ck "the canonical probe exists"     1 "$(ls probe_rev63_canon.py 2>/dev/null | wc -l | tr -d '[:space:]')"
# 3. AND THE STANDING WARNING THIS REVISION EARNED: C6+C8+IoU passing is NOT
#    evidence the emblem is right -- rev 63 built a counterexample that passed
#    all three and rendered as a Y (F175).  The counterexample's own probe is
#    kept so the next context can re-run it rather than take my word.
ck "F175's counterexample is reproducible" 1 "$(ls probe_rev63_shapefit.py 2>/dev/null | wc -l | tr -d '[:space:]')"
ck "the ablation that sized the search space" 1 "$(ls probe_rev63_ablate.py 2>/dev/null | wc -l | tr -d '[:space:]')"
ck "vw_bars reads the constants"    1 "$(grep -c '_apex    = (0.000, VW_APEX_Z)' t1_core.py)"

# ------------------------------------------------- rev 66: THE ARC-CUT TERMINAL
# Every terminal cap was cut PERPENDICULAR to its stroke, so its two corners sat
# at different radii and one landed inside the band (F199 painted exactly two).
# Cut on the BAND'S OWN ARC both corners land on it by construction and the
# global extreme cannot move -- which is what kills T1_VW_CAPMIN, whose extreme
# runs 0.8140 -> 0.9250 and drags every other terminal 12 % inboard.
ck "the arc cut is in _mitre_outline" 1 "$(grep -c 'def _mitre_outline(spine, w, arc_r=None, arc_n=24)' t1_core.py)"
ck "vw_bars ships it ON"              1 "$(grep -c 'os.environ.get("T1_VW_NOARC") != "1"' t1_core.py)"
ck "and it is ABLATABLE"              1 "$(grep -c 'T1_VW_NOARC=1 restores the perpendicular cap' t1_core.py)"
ck "the four end caps leave the fixed point" 1 "$(grep -c 'for t in _drive:' t1_core.py)"
ck "a rail that misses the band falls back" 1 "$(grep -c 'cannot be cut on it.  Fall back to' t1_core.py)"

# -------------------------------- rev 66: THE THREE REPAIRED EMBLEM INSTRUMENTS
# F198 -- C6's message carried THREE HARD-CODED FIGURES for five revisions.
# The literal must be GONE, and C12 must hold the repair in place.
# NOT `grep -c 0.6638`: the figure still appears in the COMMENTARY that records
# what F198 was, and that commentary is the record (rule 16).  What must be gone
# is the figure PRINTING AS A DIAGNOSIS, so the row greps the message's own
# giveaway phrase and the replacement asserts the message is measured.
ck "F198's literal is out of the message" 0 "$(grep -c 'the mesh names them' probe_rev46_vw.py)"
ck "C6 reports a MEASURED reach instead"  1 "$(grep -c 'MEASURED off the mesh this run, not quoted' probe_rev46_vw.py)"
ck "the reach is MEASURED off the mesh" 1 "$(grep -c 'def terminal_reach():' probe_rev46_vw.py)"
ck "C12 holds it to being a measurement" 1 "$(grep -c 'ctl("C12"' probe_rev46_vw.py)"
# F203 -- the built landmarks were read at an UNCONVERGED row count, and L4
# silently collapsed onto L2.  Both are now guarded.
ck "the built side is read converged" 1 "$(grep -c '^BUILT_ROWS = 552' probe_rev46_vw.py)"
ck "C10 checks that claim every run"  1 "$(grep -c 'ctl("C10"' probe_rev46_vw.py)"
ck "L4 refuses to be L2"              1 "$(grep -c 'if last3 and abs(last3\[-1\] - L\["L2"\]) > 1e-12:' probe_rev46_vw.py)"
# F200 -- C6 counted the photograph's RIM as a seventh cell.  Both sides now
# count INTERIOR cells, and C11 makes the re-base separately testable.
ck "cream_cells can filter to interior" 1 "$(grep -c 'def cream_cells(mask, frac=0.97, interior=False)' probe_rev46_vw.py)"
ck "C11 is the companion row"         1 "$(grep -c 'ctl("C11"' probe_rev46_vw.py)"
ck "C7's kill plants the real defect" 1 "$(grep -c 'KILL, WATCHED FIRING ON THE DEFECT' probe_rev46_vw.py)"
ck "and built_mask can plant it"      1 "$(grep -c 'def built_mask(rows=69, shrink=1.0)' probe_rev46_vw.py)"

# ------------------------------- rev 66: F205 -- C6 PASSES ON THE RASTER ONLY
# The owner looked at the render and said "the strokes still don't reach the
# ring".  He is right, and it is C6's OWN statistic that says so -- run on the
# FRAME instead of on glyph_only_mask, the photograph cuts 6 interior cells and
# the render cuts 3.  The raster reads 6 for both and cannot see it.  These rows
# hold the finding in the record so the next context cannot read C6's PASS as
# evidence about the vehicle.
ck "F205 is on the register"          1 "$(grep -c '^| \*\*F205\*\*' OPEN_FINDINGS.md)"
ck "F206's refutation is too"         1 "$(grep -c '^| \*\*F206\*\*' OPEN_FINDINGS.md)"
ck "the painted evidence is committed" 1 "$(ls probe_scratch/rev66_render_cells.png 2>/dev/null | wc -l | tr -d '[:space:]')"
ck "the brief warns C6 is a RASTER fact" 1 "$(if grep -q 'ON THE RASTER' PASTE_INTO_CLAUDE_CODE.txt || grep -q 'ON THE RASTER' HANDOFF_CARRIERS.md 2>/dev/null; then echo 1; else echo 0; fi)"
# AND THE GUARD F206 LEFT BEHIND: the glyph-vs-disc clearance was a comparison
# nothing made -- the proud-guard measures every plate against the NOSE and both
# passed while I believed they were coincident.  The guard stays even though the
# hypothesis it tested was refuted, because the comparison is real.
ck "the glyph/disc clearance is measured" 1 "$(grep -c 'glyph clearance over the cream disc' build.py)"
ck "it reads a FORWARD silhouette, both sides" 1 "$(grep -c 'def _silhouette(obs):' build.py)"
ck "and the standoff is back where it was" 1 "$(grep -c '^GLYPH_STANDOFF = 0.0016' build.py)"

# ------------------------------- rev 58: THE EMBLEM'S REACH AXIS, F63/F64
# The six constants above are fitted to VERTICAL landmarks only.  None of them
# is a radius, so a stroke can terminate 18.9 mm short of the ring band with
# every landmark still landing -- which is what the built glyph does, and why
# the owner has now reported this emblem FIVE times against a probe reporting
# "5 controls, 0 FAILED".  rev 58 added the missing axis as C6.
#
# These rows do not re-measure the glyph -- verify_clone runs no Blender.  They
# keep the control and its kill from being deleted, which is how the last four
# closures of this emblem became invisible.  The MEASUREMENT lives in
# probe_rev46_vw.py and it currently FAILS C6 BY DESIGN: photograph 7 cream
# cells, built 6.  Do not "fix" that by relaxing the control.
ck "the emblem reach control exists"      1 "$(grep -c '^def cream_cells' probe_rev46_vw.py)"
ck "it reads the photograph too"          1 "$(grep -c '^def photo_cells' probe_rev46_vw.py)"
# ONE definition, shared: a second copy is how one of two instruments gets
# quietly relaxed (sec.10.8).  photo_cells must DELEGATE, not re-implement.
ck "one definition of the cell measure"   1 "$(grep -c '^def cream_cells' probe_rev46_vw.py)"
ck "photo_cells delegates to it"          OK "$(python3 -c "
import ast
src=open('probe_rev46_vw.py').read()
fn=next(n for n in ast.parse(src).body if isinstance(n,ast.FunctionDef) and n.name=='photo_cells')
body=ast.get_source_segment(src,fn)
print('OK' if 'cream_cells(' in body else 'photo_cells RE-IMPLEMENTS the measure')" 2>&1 | tail -1)"
# rev 66 -- RE-BASED, WITH THE CAUSE NAMED (F201).  This row pinned the OLD
# kill, "collapsing the W's arms and troughs onto the axis".  Once C6 was
# corrected to count INTERIOR cells that kill STOPPED FIRING -- a collapsed W
# still cuts the ring into six, so C7 read 6 -> 6 and went red.  A control
# whose kill cannot go red makes its own PASS meaningless (rule 42), so the
# kill was replaced with one that plants EXACTLY the defect C6 detects: the
# glyph is shrunk until its extreme falls inside the band and every stroke
# floats.  WATCHED FIRING: interior cells collapse 6 -> 1.
ck "the reach control has a KILL"         1 "$(grep -c 'KILL, WATCHED FIRING ON THE DEFECT' probe_rev46_vw.py)"
ck "and the kill plants a FLOAT, not a collapsed W" 1 "$(grep -c '_float = glyph_only_mask(shrink=0.88' probe_rev46_vw.py)"
ck "F63 is on the register"               1 "$(grep -c '^| \*\*F63\*\*' OPEN_FINDINGS.md)"

# ---------------------------------------------------------------------------
# THE GUARD TABLE, EXECUTABLE.
# These eight rows lived as prose in the brief -- a second copy of numbers
# STATE.md already owns, free to drift.  They are read from STATE.md now.
# STATE.md is machine-written by audit.py, so this checks the RECORD, not a
# retyping of it.  (It does not run the guards; run those yourself.)
# ---------------------------------------------------------------------------
say "-- guard figures, read from the machine-written STATE.md --"
# rev 45 -- THIS ROW IS RE-WRITTEN, NOT RE-BASED, AND THE DIFFERENCE MATTERS.
# It grepped for the literal `roof@rear-axle=1.9835`.  On this machine the
# build prints 1.9833 -- and it printed 1.9833 BEFORE rev 45 touched anything,
# on the unmerged tree, so THE COMMITTED STATE.md WAS ALREADY 0.2 mm STALE.
# 0.2 mm on 1.98 m is 1e-4 relative; it is the same class as probe_rev42_uv's
# 56.15 % against a published 55.97 % (ledger finding 20) -- bpy-via-pip
# against whatever binary wrote the record, and no binary exists here to settle
# it.  Bumping the literal to 1.9833 would hide a real move next time, so the
# row now checks the LOCKED BASELINE is still claimed AND that the delta the
# same line prints is inside 1 mm.  That is strictly stronger than one grep.
ck "roof baseline still 1.9835"     1 "$(grep -c 'regression baseline 1.9835' STATE.md)"
# sed then awk, NOT gawk's 3-argument match(): this machine's awk is mawk 1.3.4
# and mawk rejects it outright ("syntax error at or near ,").  The header of
# this file promises portability across BSD and GNU userlands and that promise
# is load-bearing -- the check silently returned empty and read as a FAIL.
ck "roof delta within 1 mm"        ok "$(sed -n 's/.*baseline 1\.9835, \([-+][0-9.]*\) mm.*/\1/p' STATE.md | head -1 | awk '{d=($1<0)?-$1:$1; print (d<=1.0)?"ok":"off:"$1}')"
ck "rake 17.75 mm/m"                1 "$(grep -c 'rake 17.75 mm/m (locked 17.75)' STATE.md)"
ck "L=4.065 W=1.750"                1 "$(grep -c 'L=4.065 W=1.750' STATE.md)"
ck "bay widths 0.516 0.515 0.516"   2 "$(grep -c 'bay widths 0.516 0.515 0.516' STATE.md)"
# rev 45: 190 -> 221.  RE-BASED, and the reason is the merge, not this
# revision's geometry.  The seventeen stranded rev-44/44b commits (SPEC
# 10.113.4) bring cab_fitout and door_hinges -- the whole cab interior and four
# hinge assemblies -- which is +31 meshes.  Note that the committed STATE.md on
# the rev-44b tip ITSELF still said 190: it was never regenerated after the cab
# was added, so that record was stale on its own branch.
# rev 49e: 221 -> 231.  RE-BASED, AND EVERY ONE OF THE TEN IS ACCOUNTED FOR --
# no tolerance widened, no row deleted, and the row still pins an EXACT count.
#   rev 48, +4:  lid_trunk, trunk_bay, louvbay1, louvbay-1
#   rev 49, +6:  tail_board, tb_edge_red, tb_edge_dark, tail_board_stay,
#                tb_bulbs, tb_bulbflex
# 221 + 10 = 231.
#
# AND THE REASON THIS ROW ONLY WENT RED NOW IS ITSELF THE FINDING.  It reads its
# figure from STATE.md, and STATE.md had not been regenerated since REV 45 --
# from a tree it recorded as DIRTY.  So this row, and every other row in the
# "guard figures, read from the machine-written STATE.md" block, was checking
# the current build against a four-revision-old baseline and passing.  A control
# that reads a stale baseline is not a control (rule 18).  Found by the rev-49
# photorealism survey's record audit; STATE.md is regenerated at rev 49e.
#
# rev 50, RE-BASED 231 -> 223, AND THE CAUSE IS AN OWNER RULING, NOT A DRIFT.
#   rev 50, -8:  wiper_pivot x2, wiper_boss x2, wiper_arm x2, wblade x2
# He was shown that the wipers' only warrant was SPEC sec.4's inventory line
# under the heading "Stock 1963 T1" -- inferred from the factory build, not
# measured on this bus -- against three in-service photographs of this vehicle
# that show the near pane legible from top rail to sill with no arm and no
# blade.  He ruled: "Remove all of it including the spindles."  build.py's call
# is COMMENTED, not deleted, so re-enabling is one line and this row moves back.
# 231 - 8 = 223, and the figure was watched printing out of audit.py before it
# was typed here.
# rev 60 -- RE-BASED 223 -> 228, WITH THE CAUSE NAMED AND A COMPANION ROW.
#
# THE CAUSE.  Item D (F67) added FIVE meshes: `underpan`, two `chassis_rail`
# and the two end closers `under_close_f` / `under_close_a`.  The count is a
# by-value guard and it REFUSED the change, which is correct behaviour -- a
# silent mesh-count drift is how parts get added and lost unnoticed.
#
# THE COMPANION ROW below makes the cause SEPARATELY TESTABLE, so this total
# cannot be re-based again by DELETING the underbody: dropping those parts
# would take the count back to 223 and pass this row, and the companion row is
# what stops that.
# *** rev 72 -- RE-BASED 228 -> 229, CAUSE NAMED, WITH A COMPANION ROW. ***
# THE CAUSE IS ONE OBJECT AND IT IS NAMED: `seal_rear`, the rear aperture's
# rubber surround (F268).  It was the ONLY glazed aperture on this vehicle with
# no rubber ring -- bay_seals() builds eleven and windscreen_seals() two, and
# rear_glass() had none -- so with REAR_OPEN_DEG swinging the pane out the
# opening was a bare 2.8 mm shell cut edge.
# THE COMPANION ROW DIRECTLY BELOW makes that cause SEPARATELY TESTABLE, which
# is what CLAUDE.md requires of a re-base: this total cannot be re-based again
# by deleting `seal_rear` and something else, because the companion row names
# the object and would go red on its own.
ck "mesh objects 229"               1 "$(grep -c '| mesh objects | 229 |' STATE.md)"
ck "and rev 72's seal_rear is THE object that moved it" 1 "$(grep -c '| `seal_rear` | 1 |' STATE.md)"
# FOUR prefix rows, not five parts: STATE.md's inventory groups by PREFIX and
# `chassis_rail` carries n=2.  Watched print before this number was written.
ck "and the underbody's parts are IN that count" 4 "$(grep -cE '^\| `(underpan|chassis_rail|under_close_f|under_close_a)`' STATE.md)"
ck "and there are TWO chassis rails"          1 "$(grep -c '| `chassis_rail` | 2 |' STATE.md)"
# and the wipers are gone for the stated reason, not by accident
ck "the wipers are WITHDRAWN, not deleted" 1 \
   "$(grep -c '^# A(D.wipers(), \"chrome_d\")' build.py)"
ck "non-manifold edges 0"           1 "$(grep -c '| non-manifold edges (body) | 0 |' STATE.md)"

# ---------------------------------------------------------------------------
# THE MARKED QUESTION CROPS ARE TRACKED, NOT GITIGNORED.
# .gitignore only excludes rev*_hero*.png.  Every marked crop that has ever
# settled an owner reading is committed, and rev 43 must commit its own.
# ---------------------------------------------------------------------------
NCROP="$(git ls-files 2>/dev/null | grep -c '^rev.*\.png')"
if [ "${NCROP:-0}" -ge 17 ]; then
  ck "tracked marked crops >= 17" ok ok
  say "        ($NCROP crops tracked; 17 at rev 42.  Commit yours too.)"
else
  ck "tracked marked crops >= 17" ok "lost:$NCROP"
fi

say "-- gitignore --"
# rev 49e: this fired as a CRY-WOLF and the row is RIGHT -- a survey working crop
# had been named rev50_nose-front_r49hero34f_nose2x.png and matched.  THE CROP
# WAS RENAMED, THE ROW WAS NOT LOOSENED: weakening a guard to accommodate my own
# file naming is how a guard stops guarding.  Working crops must not carry
# "hero" in their names.
# rev 51 -- THE CARRIER GUARD.  CLAUDE.md is method-only and loads every session;
# its whole value is that it carries NO measurements, because a figure in a
# paragraph goes stale silently and this project has lost carriers exactly that
# way.  This row is the mechanical stop on it becoming the fourth stale entry
# door.  WATCHED FAILING: `mv CLAUDE.md x` reds it, and so does adding any
# decimal figure to it.
ck "CLAUDE.md exists" 1 "$([ -f CLAUDE.md ] && echo 1 || echo 0)"
# NOTE THE SHELL TRAP, because it bit this row on its first run: `grep -c` EXITS 1
# when the count is ZERO, which is exactly the PASSING case, so a `|| echo 99`
# fallback fires on success and concatenates -- it reported `099`.  Capture stdout
# and never branch on grep's status.
ck "CLAUDE.md carries no measurements" 0 "$(if [ -f CLAUDE.md ]; then grep -cE '[0-9]+\.[0-9]' CLAUDE.md 2>/dev/null; else echo 99; fi)"
# rev 52.  THE STEP THAT KEEPS GETTING FORGOTTEN, MADE MACHINE-CHECKED.
# Rule 15 puts an adversary on the INCOMING brief.  The OUTGOING one has always
# shipped unread -- and it becomes the next context's only map.  At rev 52 the
# outgoing brief was audited for the first time and THREE defects were found in
# it, TWO of them transcription rather than measurement, in a document whose own
# first section says not to transcribe.  Prose did not stop that and would not
# stop it again: the standing-instructions carrier and the open-findings register
# were both PROSE, and both were lost.  So it is a row.
# The two rows below hold that (a) the method rule still exists in CLAUDE.md and
# (b) the HIGHEST-NUMBERED brief actually carries its audit result.
# NOTE THE SHELL TRAP above: capture grep's stdout, never branch on its status.
ck "CLAUDE.md keeps the outgoing-brief rule" 1 "$(if [ -f CLAUDE.md ]; then grep -c 'AUDIT THE BRIEF YOU WRITE' CLAUDE.md 2>/dev/null; else echo 99; fi)"
_LATEST_BRIEF="$(ls NEXT_CONTEXT_PROMPT_rev*.md 2>/dev/null | sort -V | tail -1)"
# ---------------------------------------------------------------------------
# rev 56 -- THE OPEN-FINDINGS REGISTER. One existed and was ABANDONED AT REV 45
# WITH 21 ROWS, unnoticed for eleven revisions; the standing-instructions
# carrier went the same way at rev 44 and took the project's original
# deliverable with it. These rows exist so that cannot happen silently again.
ck "the open-findings register exists"         1 \
   "$(test -f OPEN_FINDINGS.md && echo 1 || echo 0)"
# It must not be quietly emptied. The seed was 36 rows; a floor of 21 is the
# size of the register that was lost, so falling below it is the same event.
ck "the register has not been gutted"          "OK" \
   "$(python3 -c "
n = sum(1 for l in open('OPEN_FINDINGS.md') if l.startswith('| **F'))
print('OK' if n >= 21 else 'ONLY %d ROWS -- the lost register had 21' % n)" 2>&1 | tail -1)"
# EVERY row must carry a provenance grade. A register of ungraded claims is
# what this project already has too much of.
ck "every register row carries a grade"        "OK" \
   "$(python3 -c "
import re
bad = []
for l in open('OPEN_FINDINGS.md'):
    if not l.startswith('| **F'): continue
    if 'CLOSED-rev' in l or 'closed by' in l: continue
    if not re.search(r'(MEASURED|RECOMPUTED|INHERITED|RULED|CEILED|OBSERVED)', l):
        bad.append(l.split('|')[1].strip())
print('OK' if not bad else 'UNGRADED: %s' % bad)" 2>&1 | tail -1)"
# rev 60b -- OBSERVED WAS ADDED TO THE VOCABULARY ABOVE, WITH ITS CAUSE AND
# THIS COMPANION ROW.
#
# CAUSE: `GAPS_rev60.md` grades findings MEASURED / OBSERVED / REFUTED, and the
# register's guard accepted only the first.  F111 -- the serving bays are glazed
# in ref_side.jpg and open in ref_nolita_doorshut.jpg -- is genuinely seen by
# eye on one frame each and has NOT been reduced to a number.  Grading it
# MEASURED to satisfy the guard would have been exactly the laundering this
# project forbids.
#
# BUT OBSERVED IS A WEAKER GRADE, so widening the vocabulary is a LOOSENING, and
# this row is what stops it spreading: OBSERVED rows must stay a small minority.
# If this fires, findings are being parked at the weaker grade instead of being
# measured.
ck "OBSERVED rows stay a small minority of the register" OK "$(python3 -c "
import re
rows=[l for l in open('OPEN_FINDINGS.md') if l.startswith('| **F')]
obs=[l for l in rows if 'OBSERVED' in l]
print('OK' if len(obs) <= max(3, len(rows)//20) else 'OBSERVED=%d of %d -- measure them or say why'%(len(obs),len(rows)))" 2>&1 | tail -1)"
# and the brief must point at it, or the next context never opens it.
ck "the newest brief names the register"       "OK" \
   "$(python3 -c "
import glob
b = sorted(glob.glob('NEXT_CONTEXT_PROMPT_rev*.md'), key=lambda p: int(''.join(c for c in p if c.isdigit())))[-1]
print('OK' if 'OPEN_FINDINGS.md' in open(b).read() else 'NOT NAMED IN %s' % b)" 2>&1 | tail -1)"
# The die-cut sticker is the project's ORIGINAL DELIVERABLE and its carrier has
# already been deleted once. It is named here so the register cannot lose it.
ck "the register still carries the sticker"    1 \
   "$(grep -c 'DIE-CUT STICKER' OPEN_FINDINGS.md)"
ck "newest brief records its own audit"      1 "$(if [ -n "$_LATEST_BRIEF" ]; then grep -c 'AUDITED AGAINST THE MACHINE' "$_LATEST_BRIEF" 2>/dev/null; else echo 99; fi)"

# ---- rev 52: THE CARRY-FORWARD BLOCK ------------------------------------
# EVERY ROW HERE GUARDS SOMETHING THIS PROJECT HAS ACTUALLY LOST OR LET GO
# STALE, and none of it was guarded before.  The failure mode is always the
# same: a brief gets rewritten, a line does not survive the rewrite, and
# nobody notices for revisions.  No carrier FILE has ever been deleted --
# measured, `git log --diff-filter=D` over the LEDGER / NEXT_CONTEXT_PROMPT /
# PHOTOS_WANTED / HANDOFF series is EMPTY -- so guarding files would guard the
# wrong thing.  What was lost was CONTENT INSIDE a rewritten file.  So these
# rows ask the NEWEST brief whether it still carries each item.
#
# Present/absent (1/0), never an exact count: re-wording the brief must not
# fail these rows, only DROPPING the item must.
# ------------------------------------------------------------- rev 70
# THE HANDOFF WAS SPLIT, AND THESE ROWS ARE RE-POINTED, NOT RELAXED.
#
# THE CAUSE, MEASURED (revstats.py, and the owner said it first): geometry
# output per revision fell 721 -> 209 lines between rev 8-20 and rev 61-70
# while the brief grew 12 KB -> 95 KB, and findings CLOSED at rev 66..70 were
# 0, 0, 0, 0, 0.  The brief had become too large to act on, and rule 16 --
# "never delete a carrier" -- made pruning it structurally impossible.
#
# SO THE CARRIERS MOVED TO `HANDOFF_CARRIERS.md`, VERBATIM AND COMPLETE, and
# `_has` now searches the UNION of the brief and that file.  Rule 16 requires
# a carrier to be CARRIED; it never required carrying it in the WORKING
# document.  Every string these rows protect is still under a guard, in one
# file or the other, and the union cannot be satisfied by deleting either --
# see the four COMPANION rows in the "the handoff split" block below, which
# make the split itself separately testable (SS10.8: never relax one copy of a
# check; a re-base needs the cause named AND a companion row).
_CARRIERS="HANDOFF_CARRIERS.md"
_has(){
  if [ -n "$_LATEST_BRIEF" ] && grep -qiE "$1" "$_LATEST_BRIEF" 2>/dev/null; then echo 1; return; fi
  if [ -f "$_CARRIERS" ] && grep -qiE "$1" "$_CARRIERS" 2>/dev/null; then echo 1; return; fi
  echo 0
}

# The two things the record says were actually lost, and how:
#   rev 44 -- the standing-instructions carrier was deleted and took the
#             DIE-CUT STICKER, the project's ORIGINAL DELIVERABLE, with it.
#             Undetected for five revisions and STILL OPEN.
#   rev 45 -- the open-findings register (21 rows) went the same way.
# ==========================================================================
# THE HANDOFF SPLIT -- FOUR COMPANION ROWS (rev 70)
#
# `_has` above was widened to search two files instead of one.  A widened
# check is a WEAKER check unless something separately guarantees the second
# file is real, is reached, and is not quietly re-absorbed.  These four are
# that guarantee, and each can FAIL:
#
#   (a) delete or gut HANDOFF_CARRIERS.md          -> row 1 goes red
#   (b) stop citing it from the brief              -> row 2 goes red
#   (c) let the ACTION brief re-bloat, which is
#       the whole defect the split exists to fix   -> row 3 goes red
#   (d) drop a carrier SECTION while keeping the
#       file, which `_has`'s string search alone
#       would not notice                           -> row 4 goes red
#
# WATCHED FAILING BEFORE THEY WERE BELIEVED PASSING (rule 3): row 1 against a
# missing file, row 3 against the 94,962-byte pre-split brief, row 4 against a
# carriers file with SS4 removed.
ck "the carriers file exists and is substantial" 1 \
   "$(if [ -f HANDOFF_CARRIERS.md ] && [ "$(wc -c < HANDOFF_CARRIERS.md)" -gt 40000 ]; then echo 1; else echo 0; fi)"
ck "the action brief CITES the carriers file" 1 \
   "$(if grep -q 'HANDOFF_CARRIERS.md' PASTE_INTO_CLAUDE_CODE.txt; then echo 1; else echo 0; fi)"
# THE POINT OF THE SPLIT, AS A NUMBER.  The pre-split brief was 94,962 bytes
# and the owner measured what that cost: geometry output per revision fell
# 3.4x while the brief grew 7.7x.  32 KB is a THIRD of the pre-split size and
# roughly the size the brief had at rev 50, the last era with a closure rate.
# If a future revision writes past it, that is the drift returning and this
# row is where it becomes visible -- BEFORE ten more revisions pass.
ck "the ACTION brief is still an ACTION brief (<32 KB)" 1 \
   "$(if [ "$(wc -c < PASTE_INTO_CLAUDE_CODE.txt)" -lt 32768 ]; then echo 1; else echo 0; fi)"
# *** rev 73 -- RE-BASED 14 -> 15, CAUSE NAMED, WITH A COMPANION ROW.
# THE CAUSE: rev 73 ADDED HANDOFF_CARRIERS.md SS0.10, the BUMP_BOW ladder
# (F292/F294).  It was written in the ACTION BRIEF first and moved here because
# the row directly above -- "the ACTION brief is still an ACTION brief (<32 KB)"
# -- went RED at 33,045 bytes.  That is the split working exactly as designed:
# the brief keeps the verdict, the carrier keeps the table.
# THIS ROW GUARDS AGAINST SECTIONS BEING *DELETED*, so an ADDITION raising the
# count is legitimate and a re-base is the honest response -- but a bare
# re-base would also silently accept a DELETION plus a different ADDITION, so
# the companion row below pins the new section BY NAME (SS3b's requirement).
# rev 73 -- RE-BASED 15 -> 16: SS0.11, the gloss grid, moved here when the brief
# hit its 32 KB guard a SECOND time.  Same shape as the SS0.10 re-base above and
# the same companion treatment: the new section is pinned BY NAME below.
ck "every carrier SECTION is present in the carriers file" 16 \
   "$(grep -cE '^## (SS|§)(0\.|0 |1 |2 |4 |5 |6 |7 |8 |9 |10 )' HANDOFF_CARRIERS.md 2>/dev/null | head -1)"
ck "F294 the BUMP_BOW ladder's own carrier section is still there, BY NAME" 1 \
   "$(grep -cE '^## §0\.10 THE .BUMP_BOW. LADDER' HANDOFF_CARRIERS.md 2>/dev/null | head -1)"
# *** rev 73 -- RE-ANCHORED, CAUSE NAMED.  This row first keyed on the literal
# "THE FLOOR PAIR, 0.003 px" and went red the moment the floor was re-quoted to
# its live precision (0.0026).  A guard keyed to a FIGURE fails whenever the
# figure is corrected, which is backwards: it punishes the correction.  It now
# keys on the table's SHAPE -- the header and all six BUMP_BOW rungs -- which
# is what "still carries the six-rung table" actually means.
ck "F239 the gloss grid's own carrier section is still there, BY NAME" 1 \
   "$(grep -cE '^## §0\.11 THE GLOSS GRID' HANDOFF_CARRIERS.md 2>/dev/null | head -1)"
ck "F239 ... and it still carries all NINE cells the brief points at" 1 \
   "$(if [ "$(grep -cE '^\| \*\*.T1_REFLENV. [0-9]' HANDOFF_CARRIERS.md)" -eq 3 ]; then echo 1; else echo 0; fi)"
ck "F294 ... and it still carries the six-rung table the brief points at" 1 \
   "$(if grep -q 'BUMP_BOW   mesh bow      sagitta' HANDOFF_CARRIERS.md \
        && [ "$(grep -cE '^      [0-9]\.[0-9]{2} ' HANDOFF_CARRIERS.md)" -eq 6 ]; then echo 1; else echo 0; fi)"

# ==========================================================================
# RULE 55 -- THE FIRST RULE IN THIS PROJECT ABOUT OUTPUT (rev 70)
#
# All 54 existing rules are about not being WRONG.  Not one was about
# SHIPPING, and the result is measurable: rev 66, 67, 68, 69 and 70 closed
# 0, 0, 0, 0, 0 findings between them while writing 1,122 lines of geometry.
# `revstats.py` is the instrument that makes the drift visible in ONE
# revision instead of ten, and this row makes sure it exists and is named
# where the next context will actually run it.
ck "the drift detector exists"                1 "$(if [ -f revstats.py ]; then echo 1; else echo 0; fi)"
ck "the brief names the drift detector"       1 "$(if grep -q 'revstats.py' PASTE_INTO_CLAUDE_CODE.txt; then echo 1; else echo 0; fi)"
ck "the brief carries rule 55"                1 "$(if grep -q 'SHIPS A VISIBLE CHANGE TO THE VEHICLE' PASTE_INTO_CLAUDE_CODE.txt; then echo 1; else echo 0; fi)"

ck "brief still names the die-cut sticker"   1 "$(_has 'die.?cut')"
ck "brief still names the open-findings reg" 1 "$(_has 'open.?findings')"

# The render-vs-photograph gates.  `flank_compare.py` sat unrun from rev 40 to
# rev 52 while the acceptance surface GREPPED IT FOR A SYMBOL COUNT instead of
# running it.  `cream_rms.py` is a second one and still has zero rows of its
# own.  A gate nothing names is a gate nobody runs.
ck "brief still names flank_compare"         1 "$(_has 'flank_compare')"
ck "brief still names cream_rms"             1 "$(_has 'cream_rms')"

# The photograph carrier.  PHOTOS_WANTED item 7 had NO carrier outside a single
# brief until rev 52 wrote one; items 1-5 live only in PHOTOS_WANTED_rev49.md.
ck "brief still points at PHOTOS_WANTED"     1 "$(_has 'PHOTOS_WANTED')"

# The numbered canon does NOT live in CLAUDE.md and says so.  Rules 34 and 35
# have never lived anywhere but briefs and LEDGER_rev50 SS0, so a brief that
# drops them breaks the only chain they have.
ck "brief carries the canon pointer"         1 "$(_has 'NEXT_CONTEXT_PROMPT_rev50')"
ck "brief carries rule 34"                   1 "$(_has 'A REQUIREMENT INHERITS ITS OBJECT')"
ck "brief carries rule 35"                   1 "$(_has 'A GUARD WRITTEN AGAINST A POSE')"

# An ablation list that names a switch the source does not have is a list that
# has gone stale without anyone running it.  Sweep every T1_* the brief names
# and require that all of them exist somewhere in the source.
_ABL_MISSING=0
if [ -n "$_LATEST_BRIEF" ]; then
  for _v in $(grep -oE 'T1_[A-Z0-9_]+' "$_LATEST_BRIEF" 2>/dev/null | sort -u); do
    grep -lF "$_v" ./*.py >/dev/null 2>&1 || _ABL_MISSING=$((_ABL_MISSING+1))
  done
fi
ck "every T1_ switch the brief names exists" 0 "$_ABL_MISSING"

# rev 55, ADVERSARIAL PASS.  THE ROW ABOVE ONLY GREPS THE STRING, so a switch
# that survives in a COMMENT passes it while being a DEAD LEVER -- which is
# how the retired Bevel-selection switch kept a brief green for two revisions
# while reading no environment variable at all.  Worse, the rev-56 brief's own
# audit row printed that switch's name while claiming it had been dropped, so
# the row above was hanging on one comment in probe_rev53_chip.py.
# THIS ROW ASKS THE HARDER QUESTION: every T1_ the brief names must actually be
# READ FROM THE ENVIRONMENT somewhere in the source.
# WATCHED FAILING by putting the dead switch's name back in the brief.
_ABL_DEAD=0
if [ -n "$_LATEST_BRIEF" ]; then
  for _v in $(grep -oE 'T1_[A-Z0-9_]+' "$_LATEST_BRIEF" 2>/dev/null | sort -u); do
    grep -lE "(environ|getenv|_env[ifsb]?\()[^\"']*[\"']$_v" ./*.py >/dev/null 2>&1 \
      || _ABL_DEAD=$((_ABL_DEAD+1))
  done
fi
ck "every T1_ switch the brief names is a LIVE lever" 0 "$_ABL_DEAD"
# *** rev 73, F293 -- WIDENED IN THE SAME EDIT AS audit_brief.py's twin row,
# which is what that row's own comment demands ("loosen BOTH or neither").
# THE CAUSE: the old pattern needed "environ" on the SAME LINE as the switch.
# studio.py reads several switches through its own wrappers -- `_envi("T1_FX",
# 1)`, `_envf("T1_SHADOW", 9.0)` -- so those LIVE levers read as dead.
# THE COMPANIONS, so the widening cannot become a hole:
_HELPER_LIVE="$(grep -lE '_env[ifsb]?\("T1_SHADOW' ./*.py >/dev/null 2>&1 && echo 1 || echo 0)"
ck "F293 a switch read ONLY through a helper wrapper is detected as LIVE" 1 "$_HELPER_LIVE"
_FAKE_LIVE="$(grep -lE '(environ|getenv|_env[ifsb]?\()[^"'"'"']*["'"'"']T1_NOT_A_REAL_SWITCH' ./*.py >/dev/null 2>&1 && echo 1 || echo 0)"
ck "F293 ... and a fabricated switch is still DEAD under the widened pattern" 0 "$_FAKE_LIVE"

# THE INTAKE DOORS.  README.md pointed at NEXT_CONTEXT_PROMPT_rev43.md for NINE
# revisions and START_HERE.md still said "rev 7" thirty revisions on.  Both are
# the first thing a fresh context reads.
_RN="$(echo "$_LATEST_BRIEF" | grep -oE '[0-9]+' | tail -1)"
# rev 53.  THE INTAKE DOOR THAT ACTUALLY AUTO-LOADS, AND IT WAS THE ONE LEFT
# UNGUARDED.  CLAUDE.md carries `@PASTE_INTO_CLAUDE_CODE.txt` in its Imports, so
# that file is pulled into EVERY session as "this revision's entry procedure".
# It was updated every revision from rev 47 through rev 51 and then REV 52
# DROPPED IT: rev 53 opened with the rev-52 brief auto-loaded while the real
# brief was rev 53, and nothing said so.  README and START_HERE were guarded at
# rev 52; the file that loads itself was not.  It must BE the newest brief --
# byte-identical, so there is no second source of truth free to diverge, which
# is the same reason CLAUDE.md sec.10 rejected a separate RULES_CANON.md.
ck "the IMPORTED entry procedure IS the newest brief" 1 "$(if [ -n "$_LATEST_BRIEF" ] && cmp -s PASTE_INTO_CLAUDE_CODE.txt "$_LATEST_BRIEF"; then echo 1; else echo 0; fi)"
ck "CLAUDE.md still imports that entry procedure"     1 "$(grep -c '^@PASTE_INTO_CLAUDE_CODE.txt' CLAUDE.md)"
ck "README points at the newest brief"       1 "$(if [ -n "$_RN" ] && grep -qE "rev $_RN\b" README.md 2>/dev/null; then echo 1; else echo 0; fi)"
ck "START_HERE points at the newest brief"   1 "$(if [ -n "$_RN" ] && grep -qE "rev $_RN\b" START_HERE.md 2>/dev/null; then echo 1; else echo 0; fi)"
# rev 57b, OWNER RULING.  The rule was "no hero PNG tracked, ever", and it is
# right about FULL-SIZE heroes: they are 11 MB and regenerable.  But it also
# meant the delivery frame each revision is told to BEAT cost 107 minutes to
# regenerate before it could be compared to, so no baseline ever survived a
# revision.  He ruled that a DOWNSIZED reference is exempt.
#
# NARROWED BY DIMENSION, NOT BY NAME.  A name exemption is a hole anyone can
# walk through by renaming; a width cap cannot be dodged without actually
# shrinking the file.  Tracked hero PNGs must be <= 1600 px wide.
ck "no FULL-SIZE hero is tracked" OK "$(python3 -c "
import subprocess
from PIL import Image
bad=[]
for f in subprocess.run(['git','ls-files'],capture_output=True,text=True).stdout.split():
    if 'hero' in f and f.endswith('.png'):
        try:
            w,_=Image.open(f).size
        except Exception:
            continue
        if w > 1600: bad.append('%s (%d px)'%(f,w))
print('OK' if not bad else 'FULL-SIZE HERO TRACKED: '+'; '.join(bad))" 2>&1 | tail -1)"
ck "out/ is NOT tracked"            0 "$(git ls-files 2>/dev/null | grep -c '^out/')"

# rev 53.  THE MOST-REPEATED NUMERIC DEFECT IN THESE HANDOFFS, FINALLY GUARDED.
# A brief quotes this script's row total in its sec.1 so the next context knows
# what to expect, and that number has been wrong THREE REVISIONS RUNNING:
# rev 52's brief said 138 then 151; rev 53's draft said 159 then 160; and this
# revision moved 160 -> 162 -> 164 while the prose lagged each time.  The cause
# is structural, not carelessness: until the tree is clean the banner reads
# "N-1 PASSED, 1 FAILED" -- the clean-tree row IS the failure -- so the number
# on screen while a brief is being written is always one short.
# MUST BE THE LAST ROW: it compares the brief's stated total against this
# script's OWN live tally, so it has to run after every other ck.  PASS+1
# counts this row itself, which is stable once set.
# READ IT OFF THE COMMAND LINE, NOT BY PICKING THE LARGEST NUMBER.  The first
# version took the largest "ALL n PASS" anywhere in the brief, to dodge
# bootstrap's "ALL 10 PASS".  WATCHED FAILING ON THE WRONG THING: a brief that
# merely MENTIONS a bigger historical figure in prose -- and briefs quote old row
# counts all the time; this one quotes "ALL 159 PASS" in its own audit table --
# made the row read 900 and fail.  That is the carry-forward block's stated
# principle firing on me (line ~817: re-wording the brief must not fail a row).
# So anchor on the line that actually invokes this script.
# WATCHED FAILING ON BOTH REAL MODES: a brief carrying the pre-commit number
# (got 164, want 163), and a row added and COMMITTED without updating the brief
# (got 165, want 166).
# STATED LIMITATION, found by watching it: on a DIRTY tree the two effects
# cancel -- the clean-tree row fails (-1) while the added row adds (+1) -- so
# this row cannot see a newly added row until it is committed.  That is
# acceptable only because the clean-tree row is itself failing at that moment
# and the script already says STOP.  It is NOT a row you can trust mid-edit.
# --------------------------------------------------------------- rev 55
# THE INSTRUMENTS THIS REVISION ADDED, AND THE RETRACTIONS IT LANDED.
# Every one of these was watched FAILING (by deleting the anchor line) and
# PASSING again on a clean tree, in the same hour it was written.
#
# Item A's ground control: without it, flank_compare prints a level
# difference and nothing that says whose it is.
ck "flank_compare carries the ground control" 1 \
   "$(grep -c 'ground control -- the UNINKED paint' flank_compare.py)"
# ... and its verdict must be DERIVED.  The first draft printed "the ink is
# NOT painted light" as a CONSTANT STRING and said it under the ablation too.
# BOTH branches have to exist or the conclusion cannot fail.
ck "that control's verdict has both branches" 2 \
   "$(grep -cE 'INSIDE the photograph|OUTSIDE it: the ink IS off' flank_compare.py)"
# The two ablations that made those controls mean something.
ck "T1_FC_INKGAIN ablation exists"            1 \
   "$(grep -c 'os.environ.get("T1_FC_INKGAIN"' flank_compare.py)"
ck "T1_FC_ZSTRETCH ablation exists"           1 \
   "$(grep -c 'os.environ.get("T1_FC_ZSTRETCH"' flank_compare.py)"
# Item C: the aspect FAIL must never again be read as a settled model defect.
ck "the aspect row carries its instrument note" 1 \
   "$(grep -c 'ON THE ASPECT ROW -- it is INSTRUMENT-DEPENDENT' flank_compare.py)"
# ---------------------------------------------------------------------------
# rev 56 item A.  THE VERTICAL CARRY LAW.  flank_kv carried k_t off the rear
# hub by the map's FULL horizontal ratio -- a 1/Z^2 quantity used to move a
# 1/Z one -- so it applied the depth correction twice and read 2.45 % low at
# the lockup centre.  These rows hold the correction, its retraction and its
# ablation in the SOURCE, not only in a ledger (rule 15).
#
# ANCHORED ON THE ARITHMETIC, NOT ON A STRING.  A grep for "sqrt" would pass
# on a comment.  This row RUNS flank_kv at two columns and checks the ratio is
# the LINEAR one (u+B)/(U_RHUB+B) = 0.976122 and not the quadratic 0.952814 --
# so it fails if the law is reverted however the file is worded.
ck "flank_kv carries k_t LINEARLY in (u+B)"  "OK" \
   "$(python3 -c "
import flank_compare as F
r = F.flank_kv(465.5) / F.flank_kv(F.U_RHUB)
print('OK' if abs(r - 0.976122) < 5e-5 else 'GOT %.6f' % r)" 2>&1 | tail -1)"
# and the ablation must still be able to put the old law back, or the
# correction can never be watched failing again.
ck "T1_FC_KVQUAD ablation restores the old law" "OK" \
   "$(python3 -c "
import os, importlib, flank_compare as F
os.environ['T1_FC_KVQUAD'] = '1'; importlib.reload(F)
r = F.flank_kv(465.5) / F.flank_kv(F.U_RHUB)
print('OK' if abs(r - 0.952814) < 5e-5 else 'GOT %.6f' % r)" 2>&1 | tail -1)"
# The header's refuted physics claim must not come back: it said the
# horizontal scale must be the SMALLER of the two, which is false aft of the
# principal column and is what produced the phantom "one instrument is 2.3 %
# out".  The withdrawal has to stay in the source.
# Anchored on the PRINTED line, which occurs once, not on the bare phrase --
# that appears three times (docstring, comment block, print) and a row that
# wants exactly 1 of it breaks the moment the note is cross-referenced.
ck "the anisotropy withdrawal is PRINTED"      1 \
   "$(grep -c 'THE ANISOTROPY IS NOT A CONFLICT: ref_side.jpg' flank_compare.py)"
# The anchor is OPEN and must not be quietly closed by a later revision
# adopting the wheel number: three readings, two equations.
ck "the open anchor keeps its three readings"  1 \
   "$(grep -c 'THREE QUANTITIES, TWO EQUATIONS' flank_compare.py)"
# The probe that proves the law must exist and must still separate the two
# laws when RUN -- not merely be present.
ck "probe_rev56_kv separates the two laws"     "OK" \
   "$(python3 probe_rev56_kv.py 2>&1 | grep -q 'the LINEAR law is exact' && echo OK || echo NO)"
# Item 2: the retraction lives in the SOURCE, not only in a ledger (rule 15),
# and it must keep BOTH halves -- that the shipped socket is dead on smooth
# geometry AND that the true normal counts facets.  Either half alone is a
# claim that would get the default flipped.
ck "t1_mats carries the true-normal retraction" 1 \
   "$(grep -c 'True Normal. IS NOT THE FIX' t1_mats.py)"
ck "t1_mats keeps the facet-counting half"     1 \
   "$(grep -c 'It detects TESSELLATION, not folds' t1_mats.py)"
ck "T1_TRUENORM lever exists in the shader"    1 \
   "$(grep -c 'os.environ.get("T1_TRUENORM")' t1_mats.py)"
# Two citations this revision found rotten.  `depth_correct()` was cited in
# cream_rms.py as the remedy for the scale caveat and is DEFINED NOWHERE in
# this repo; `PHOT` was bound twice in mottle_measure.py, two lines apart, so
# the file carried two different sets of "the photograph's" figures and threw
# one away silently.  Both rows want the rotten form GONE and the live form
# singular.
ck "cream_rms cites no undefined depth_correct" 0 \
   "$(grep -c 'See depth_correct()' cream_rms.py)"
# ---------------------------------------------------------------------------
# rev 56 item B.  cream_rms had a LIVE re-based measurement and a DEAD entry
# point, and three briefs carried the re-base as open because `run()` -- what
# a reader actually runs -- still pointed at ref_side.jpg.  These rows are
# BEHAVIOURAL: they RUN the thing.  A grep would have passed all along.
ck "cream_rms.run() returns the live spectrum" "5" \
   "$(python3 -c "
import cream_rms as C, io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    d = C.run()
print(len(d) if isinstance(d, dict) else 0)" 2>&1 | tail -1)"
# and it must NOT be the dead path any more -- that path returns {} and says so.
ck "cream_rms.run() is not the dead path"     0 \
   "$(python3 -c "
import cream_rms as C, io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    C.run()
print(buf.getvalue().count('LEGACY PATH, RESULT IS NOT CREAM'))" 2>&1 | tail -1)"
# The dead path is KEPT and must stay reachable, or the reason for the re-base
# stops being watchable and becomes a claim in a comment (rule 15).
ck "the dead ref_side path is still reachable" 1 \
   "$(T1_CR_LEGACY=1 python3 cream_rms.py 2>&1 | grep -c 'LEGACY PATH, RESULT IS NOT CREAM')"
# WATCHED FAILING: spectrum() must REFUSE rather than answer when the patch
# cannot support the measurement.  Fed a deliberately tiny box it returns None.
ck "cream_rms.spectrum REFUSES a tiny patch"  "None" \
   "$(python3 -c "
import cream_rms as C
print(C.spectrum(box=(900, 910, 300, 310), quiet=True))" 2>&1 | tail -1)"
# mottle_measure's target must be DERIVED from that spectrum, not transcribed.
ck "mottle_measure derives TARGET, not typed" 1 \
   "$(grep -c '_CR.spectrum(quiet=True)' mottle_measure.py)"
ck "mottle_measure refuses a None target"     1 \
   "$(grep -c 'Refusing to print a ratio against a literal' mottle_measure.py)"
# rev 56: the beauty arm is DEAD -- the patch comes back 100 % clipped and the
# file used to print five "ratio 0.00" rows, which read as "the model has no
# mottle" when they are a measurement of nothing.  It must refuse.
ck "mottle_measure refuses a clipped patch"   1 \
   "$(grep -c 'if clip > 0.02:' mottle_measure.py)"
# and it must refuse BEFORE it prints anything measurement-shaped.  This row
# is an ORDERING test, not a grep: the guard used to sit at the end of the
# file, after the BASE LEVEL block and the character table had already put
# nan and 0.000 on the console.
# ---------------------------------------------------------------------------
# rev 56 section 3.1.  lid_rail: the OWNER answered it, so the four-revision
# zero-area exemption comes out.  These rows hold the ruling and its
# provenance in the source, and make sure the exemption cannot creep back.
ck "the lid_rail zero-area exemption is GONE"  1 \
   "$(grep -c 'ZERO_AREA_EXEMPT = ()' verify.py)"
ck "no name is zero-area exempt any more"      0 \
   "$(grep -c 'ZERO_AREA_EXEMPT = ("lid_rail"' verify.py)"
# The width must be RAIL_PROUD and must be asked of the MESH, not grepped --
# the part was empty for four revisions precisely because grepping its name
# found it and nothing asked its size.
ck "verify asks the MESH for the rail width"   1 \
   "$(grep -c 'width %.4f m != RAIL_PROUD' verify.py)"
ck "the rail width is RAIL_PROUD, not a literal" 1 \
   "$(grep -c 'RAIL_W = 0.0 if os.environ.get("T1_RAILFLAT") == "1" else RAIL_PROUD' t1_shell.py)"
# and the ablation that restores the defect must stay, or neither guard can be
# watched failing again.
ck "T1_RAILFLAT ablation is a LIVE lever"      1 \
   "$(grep -c 'os.environ.get("T1_RAILFLAT")' t1_shell.py)"
# The owner's own words must stay attached to the number (rule 34: a
# requirement inherits its object -- this one inherits a GREEN vehicle and a
# geometry-only reading, and that has to travel with it).
# Anchored on the LOGGED provenance line, which occurs once -- the phrase
# itself appears twice (comment and log) and a row wanting exactly 1 of it
# fails the moment the ruling is also explained in prose.
ck "the rail width carries its provenance"     1 \
   "$(grep -c 'ref_workshop.jpg: ' verify.py)"
ck "that refusal precedes the first number"   "OK" \
   "$(python3 -c "
s = open('mottle_measure.py').read()
g = s.index('if clip > 0.02:')
b = s.index('--- BASE LEVEL')
print('OK' if g < b else 'GUARD IS AFTER THE FIRST PRINTED NUMBER')" 2>&1 | tail -1)"
ck "mottle_measure binds PHOT exactly once"    1 "$(grep -c '^PHOT = ' mottle_measure.py)"

# ------------------------------------------------- rev 57: THE NOSE BADGE
# ITEM A, THE TOP JOB, TAKEN AFTER THREE REVISIONS OF DEFERRAL -- AND CLOSED
# WITH A CEILING RATHER THAN A NUMBER.  These rows hold the parts of that
# result that a later revision could quietly lose.
#
# The photographable quantity is stroke width / ring OUTER radius, taken off
# the BUILT MESH (probe_rev57_geom.py -> probe_scratch/rev57_glyph.npz), not
# off CAP_EMBLEM_WFRAC and not off the brief.  ARITHMETIC, not a grep: this
# row re-derives all six strokes from the dump every run.
ck "the six built nose strokes are ONE width" OK "$(python3 -c "
import numpy as np
Z=np.load('probe_scratch/rev57_glyph.npz',allow_pickle=True)
cy,cz,R=float(Z['cy']),float(Z['cz']),float(Z['R_OUT'])
V=Z['polys'][0].astype(float); W=Z['polys'][2].astype(float)
V=np.column_stack([V[:,0]-cy,V[:,1]-cz])/R; W=np.column_stack([W[:,0]-cy,W[:,1]-cz])/R
def pw(P,q):
    a,b,c,d=[P[i] for i in q]
    u=(b-a)/np.linalg.norm(b-a); n=np.array([-u[1],u[0]])
    return abs(np.dot(a-c,n))
w=[pw(V,(1,2,5,0)),pw(V,(2,3,4,5)),pw(W,(1,2,9,0)),
   pw(W,(2,3,8,9)),pw(W,(3,4,7,8)),pw(W,(4,5,6,7))]
print('OK' if (max(w)-min(w))/np.mean(w) < 0.005 else 'SPREAD %.4f'%((max(w)-min(w))/np.mean(w)))" 2>&1 | tail -1)"

# The VALUE the newest brief and the ledger quote, recomputed from the dump.
# If the badge geometry moves, this row moves with it and the prose does not.
ck "the built nose stroke is 0.20455 of the ring R" 0.20455 "$(python3 -c "
import numpy as np
Z=np.load('probe_scratch/rev57_glyph.npz',allow_pickle=True)
cy,cz,R=float(Z['cy']),float(Z['cz']),float(Z['R_OUT'])
V=Z['polys'][0].astype(float); W=Z['polys'][2].astype(float)
V=np.column_stack([V[:,0]-cy,V[:,1]-cz])/R; W=np.column_stack([W[:,0]-cy,W[:,1]-cz])/R
def pw(P,q):
    a,b,c,d=[P[i] for i in q]
    u=(b-a)/np.linalg.norm(b-a); n=np.array([-u[1],u[0]])
    return abs(np.dot(a-c,n))
print('%.5f'%np.mean([pw(V,(1,2,5,0)),pw(V,(2,3,4,5)),pw(W,(1,2,9,0)),
                      pw(W,(2,3,8,9)),pw(W,(3,4,7,8)),pw(W,(4,5,6,7))]))" 2>&1 | tail -1)"

# NO RESULT MAY BE HARD-CODED INTO THE PROBE THAT PRODUCES IT.  rev 57's own
# band control shipped a CONSTANT verdict string on its first run and the
# string contradicted the numbers printed two lines above it -- sec.3.7's
# lesson, fired on the probe written to honour it.  This row forbids the
# measured values appearing as literals in the file that measures them.
ck "the badge probe hard-codes none of its results" 0 \
   "$(grep -cE '0\.23985|0\.14318|0\.09209|0\.09280|0\.20592' probe_rev57_badge.py)"

# ... and the band control's verdict must be COMPUTED from the two gaps.
ck "the band control's verdict is DERIVED" 1 \
   "$(grep -c 'if _gap < 0.25 \* _str' probe_rev57_badge.py)"

# F37.  t1_detail.py states the nose badge's ring outer D TWICE, with two
# different values, about one boundary in one frame.  BOTH halves are held:
# the disagreement is real (both strings still present) AND it is now
# retracted in the SOURCE, not only in a ledger (rule 15).
ck "both of the record's ring-D readings are still there" 2 \
   "$(grep -cE 'outer D 91\.729 px|vertical D 91\.885 px' t1_detail.py)"
# This one IS a grep, deliberately: what it asserts is that a RETRACTION is
# present where a reader meets the defect, and prose is the only form that
# takes.  It is anchored on the third reading's VALUE, not on a slogan, so
# deleting the paragraph or replacing it with a hand-wave fails the row.
ck "the ring-D disagreement is retracted IN THE SOURCE" 1 \
   "$(grep -c 'vertical D 92.728 px' t1_detail.py)"

# The mottle levers item B is swept on must READ THE ENVIRONMENT, not merely
# be named in a comment -- the same anchoring the rev-56 switch row uses.
ck "T1_MOT_M reads the environment"   1 "$(grep -c 'os.environ.get("T1_MOT_M"' t1_mats.py)"
ck "T1_MOT_RGH reads the environment" 1 "$(grep -c 'os.environ.get("T1_MOT_RGH"' t1_mats.py)"

# The register is a CARRIER (rule 16).  Rows leave it only by being closed or
# retired -- never by being dropped -- so the IDs must be contiguous from F01
# with no gap.  ARITHMETIC: it counts the IDs and checks the run.
ck "OPEN_FINDINGS keeps an unbroken F01..Fnn" OK "$(python3 -c "
import re
ids=sorted({int(m) for m in re.findall(r'\*\*F(\d\d)\*\*', open('OPEN_FINDINGS.md').read())})
print('OK' if ids and ids==list(range(1,len(ids)+1)) else 'GAP %s'%ids)" 2>&1 | tail -1)"

# ------------------------------------------- rev 57: ITEM B WAS REFUTED
# The gate does not measure the mottle.  These rows hold the refutation so a
# later revision cannot re-inherit "tune MOTTLE_M" as though it were open.
#
# THE ABLATION LEVER MUST STAY A LEVER, not a comment.
ck "T1_MOT_AMP reads the environment" 1 "$(grep -c 'os.environ.get("T1_MOT_AMP"' t1_mats.py)"

# The refutation must live in the SOURCE, not only in a ledger (rule 15), and
# it is anchored on the MEASURED value, so a hand-wave does not satisfy it.
ck "mottle_measure records that it is not measuring the mottle" 1 \
   "$(grep -c 'sd 0.2594, peak-to-peak 1.603 -- 6.5' mottle_measure.py)"
ck "the dead 16-bit branch is retracted where it lives" 1 \
   "$(grep -c 'WRONG SIDE OF THE CONVERSION' shader_solve.py)"

# ...AND THE 16-BIT CLAIM IS TESTED, NOT ASSERTED.  F42 says PIL silently
# downconverts a 16-bit RGBA PNG, so shader_solve's `a.max() > 255.0` test can
# never fire.  This row BUILDS such a PNG and asks PIL what it gets back.  The
# day PIL gains 16-bit RGBA support, or the reader is fixed, THIS ROW FAILS --
# which is exactly when the comment beside it stops being true.  A guard on
# behaviour, not on a grep (sec.10.4).
ck "PIL really does downconvert 16-bit RGBA (F42 is live)" OK "$(python3 -c "
import zlib, struct, io, numpy as np
from PIL import Image
w=h=4
raw=b''.join(b'\x00'+b''.join(struct.pack('>HHHH',30000,30000,30000,65535) for _ in range(w)) for _ in range(h))
def chunk(t,d):
    c=t+d; return struct.pack('>I',len(d))+c+struct.pack('>I',zlib.crc32(c)&0xffffffff)
png=(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,16,6,0,0,0))
     +chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b''))
a=np.asarray(Image.open(io.BytesIO(png)).convert('RGBA'))
print('OK' if a.dtype==np.uint8 and a.max()<=255 else 'PIL NOW RETURNS %s max %s'%(a.dtype,a.max()))" 2>&1 | tail -1)"

# ------------------------------- rev 57b: THE RANKING RULE, AND THE 3rd GATE
# The efficiency audit found the ORDERING rule was the defect, not any row in
# it.  These rows hold the replacement so it cannot quietly revert to "gate
# availability" -- which is how four revisions went to a 1.4 px^2 question.
#
# BEHAVIOUR, not a grep: the budget script must actually RUN and must still
# rank the paint's gloss above the badge stroke by orders of magnitude.
# rev 60 -- RE-BASED, WITH THE CAUSE NAMED, AND WITH A COMPANION ROW BELOW.
#
# THE CAUSE.  This row asserted that the table's TOP line contains "GLOSS".
# That held only because the table was INCOMPLETE: at rev 59 it listed none of
# the emblem (F63), the ground shadow (F67) or the nose break (F75) -- three of
# the owner's own five items -- and it ranked the CEILED gloss row first, so a
# context that obeyed it would have worked a closed item and skipped his.  Rev
# 60 added the missing rows and F67's shadow footprint, 4.81e+06 px^2, now
# sorts above gloss's 2.62e+06.  The ORDER changed because the DATA was wrong,
# not because the tool broke.
#
# WHAT THIS ROW MEANS, kept: the badge -- the top job for four revisions -- must
# still sort LAST, far below the large-area items.  That is the tool's whole
# point and it is unchanged.  The companion row makes the CAUSE separately
# testable, so this cannot be quietly relaxed again by dropping rows.
ck "the visibility budget still sorts the badge last, under gloss" OK "$(python3 -c "
import subprocess,re
o=subprocess.run(['python3','visibility_budget.py','3840'],capture_output=True,text=True).stdout
r=[l for l in o.splitlines() if re.match(r'^ +\d+\. ',l)]
bot=r[-1] if r else ''
gl=[i for i,l in enumerate(r) if 'GLOSS' in l]
bd=[i for i,l in enumerate(r) if 'badge' in l]
print('OK' if 'NO RENDER' in o else ('OK' if r and 'badge' in bot and gl and bd and min(gl)<min(bd) else 'ORDER CHANGED: %r'%(bot[:40],)))" 2>&1 | tail -1)"
# rev 60b -- BOTH ROWS ABOVE NOW TOLERATE "NO RENDER", AND HERE IS WHY.
#
# Rev 60 gave visibility_budget.py a rule-37 refusal (exit 2, the words "NO
# RENDER") and removed its FALLBACK -- and left these two rows calling it.
# `out/` is untracked and starts EMPTY, so on a FRESH CLONE both rows failed,
# and their failure text read "ORDER CHANGED" and "MISSING:F63,F67,F75" --
# an absent input reading as a defect in the ranking, which is rule 37's first
# half, inside the rows that shipped its second half.  So "ALL 264 PASS" was
# true only in a tree that had already rendered a hero.
#
# The row below asserts the REFUSAL is correct, so tolerating it here cannot
# hide a broken tool.
ck "the visibility budget REFUSES without a frame, in those words" OK "$(python3 -c "
import subprocess,tempfile,os,shutil
d=tempfile.mkdtemp()
shutil.copy('visibility_budget.py', d)
r=subprocess.run(['python3','visibility_budget.py','3840'],cwd=d,capture_output=True,text=True)
print('OK' if r.returncode==2 and 'NO RENDER' in r.stdout else 'rc=%d out=%r'%(r.returncode,r.stdout[:60]))" 2>&1 | tail -1)"
ck "the visibility budget carries the owner's OWN ranked items" OK "$(python3 -c "
import subprocess
o=subprocess.run(['python3','visibility_budget.py','3840'],capture_output=True,text=True).stdout
need=['F63','F67','F75']
missing=[n for n in need if n not in o]
print('OK' if 'NO RENDER' in o else ('OK' if not missing else 'MISSING:'+','.join(missing)))" 2>&1 | tail -1)"

# ---------------------------- rev 59: TWO REFERENCE MASKS THAT NEVER MET (F67)
# THE DEFECT THESE ROWS EXIST FOR.  `senor_trace.py` graded itself against a
# mask baked into its own source from out/glyph_lab.npy -- a file that has not
# existed in this repo for as long as anyone has looked, so its own
# `_crosscheck()` printed "not present" every run and nobody read it.  Over the
# identical window (mask x 6..88, y -12..27) that bake held 934 px while
# `compare_script.ref_mask()`, which is what the LIVE gate scores against, held
# 1176.  IoU 0.788, and the difference WAS the tilde of the `n~`: 118 px of ink
# dead centre over the word.  The trace reported 0.913 the whole time.
#
# NOTHING IN THE REPO COMPARED THE TWO MASKS, so the divergence was invisible.
# That is the root cause, and this is the row that makes it loud.  It is EXACT,
# pixel for pixel -- not a tolerance -- over the guarded window, and it needs no
# Blender and no render (this script must stay that way).
ck "senor_trace's baked mask == compare_script's live mask" OK "$(python3 -c "
import senor_trace as S
ok, n, ng = S.check_ref_agrees(verbose=False)
print('OK' if ok else ('NO REFERENCE' if n < 0 else 'DIVERGED: %d of %d px' % (n, ng)))" 2>&1 | tail -1)"

# ...and it must be ABLE to go red, or it reports nothing (rule 3).
# T1_ST_REFDRIFT flips ONE bit of the baked constants, inside the guarded rows
# and outside _SWASH_EXCLUDE.  WATCHED FAILING BOTH WAYS at rev 59: perturbing
# the BAKED side (this row) and, by monkeypatching compare_script.ref_mask(),
# the LIVE side -- 2 px, reported at mask (45,14) and (46,15).
ck "that agreement row FAILS when the bake is perturbed" DIVERGED "$(python3 -c "
import os
os.environ['T1_ST_REFDRIFT'] = '1'
import senor_trace as S
ok, n, ng = S.check_ref_agrees(verbose=False)
print('DIVERGED' if (not ok and n == 1) else 'GUARD IS BLIND: ok=%s n=%s' % (ok, n))" 2>&1 | tail -1)"

# THE FIX ITSELF, ASKED OF THE RASTER AND NOT OF A GREP (sec.10.4).  A stroke
# named "ntilde" proves nothing -- there were two of those beside the tilde's
# hole for fifty revisions.  This draws the word and counts ink in the band the
# tilde occupies, mask rows y 1..9, cols x 35..63.  Before rev 59: 73 px drawn
# against 186 in the reference.  After: 156.  Both watched printing.
ck "the tilde is DRAWN, not pruned (band ink >= 150 px)" OK "$(python3 -c "
import numpy as np, senor_trace as S
ox, oy = S._REF_X0 - 8, S._REF_Y0 - 4
c = S._Canvas(S._REF_W + 16, S._REF_H + 12)
class _S:
    def stroke(s, p, w, cut=False, caps=True): c.stroke(np.c_[p[:,0]-ox, p[:,1]-oy], w, cut, caps)
    def cut(s, p): c.cut(np.c_[np.asarray(p)[:,0]-ox, np.asarray(p)[:,1]-oy])
    def blob(s, p): pass
S.draw_senor(_S(), ypad=0)
g = (c.alpha() > 96)[S._REF_Y0-oy:S._REF_Y0-oy+S._REF_H, S._REF_X0-ox:S._REF_X0-ox+S._REF_W]
n = int(g[1+12:9+13, 35-6:64-6].sum())
print('OK' if n >= 150 else 'TILDE BAND ONLY %d px' % n)" 2>&1 | tail -1)"

# The third gate must RUN and must still be exposure-free -- the property that
# makes it immune to the three open px/m and white-balance unknowns.
# rev 58, F58: THIS ROW USED TO CALL `gloss_compare.py` WITH NO ARGUMENT.
# The script's default was a hard-coded `out/r57_hero.png`; `out/` is untracked
# and starts EMPTY on every clone, so the row passed only in the working tree
# that wrote it and FAILED on every clone -- reporting the missing file as
# `MOVED: []`, i.e. an ABSENT INPUT dressed as a MOVED STATISTIC, which points
# the reader at the estimator instead of at the path.  Exposure invariance is a
# property of the ESTIMATOR, so it is now tested on a synthetic patch through
# the REAL spread(), needs no render, and cannot rot with a filename.
# WATCHED FAILING via T1_GC_ABSSPREAD=1, which drops the /p50 (the row below).
ck "gloss_compare is exposure-free (selftest, no frame)" OK "$(python3 -c "
import subprocess,re
o=subprocess.run(['python3','gloss_compare.py','--selftest'],capture_output=True,text=True).stdout
v=re.findall(r'x[01]\.\d\d  spread (\d+\.\d+)', o)
print('OK' if len(v)==3 and len(set(v))==1 and 'SELFTEST PASS' in o else 'MOVED: %s'%v)" 2>&1 | tail -1)"

# ...and the selftest must be ABLE to fail, or it reports nothing (rule 3).
ck "the exposure selftest FAILS when the scale-freedom is removed" FAILS "$(python3 -c "
import subprocess, os
e=dict(os.environ); e['T1_GC_ABSSPREAD']='1'
r=subprocess.run(['python3','gloss_compare.py','--selftest'],capture_output=True,text=True,env=e)
print('FAILS' if r.returncode==1 and 'SELFTEST FAIL' in r.stdout else 'THE ABLATION DID NOT TRIP IT rc=%d'%r.returncode)" 2>&1 | tail -1)"

# ...and the stale-default trap itself must stay shut: no revision-numbered
# frame may come back as a default input path.
# ANCHORED ON CODE, NOT TEXT.  The first version of this row was a flat grep
# and it matched its OWN comment -- the one explaining that the old default was
# `out/r57_hero.png` -- and reported the explanation as the defect.  That is the
# FIFTH time a row in this file has done that.  Strip comments and strings that
# are not code, and look only at what executes.
ck "gloss_compare has no revision-numbered default frame" 0 "$(python3 -c "
import io, tokenize, re
src = open('gloss_compare.py').read()
out = []
for t in tokenize.generate_tokens(io.StringIO(src).readline):
    if t.type == tokenize.COMMENT:
        continue
    out.append(t.string)
code = ' '.join(out)
print(len(re.findall(r'r[0-9]{2}b?_hero\.png', code)))" 2>&1 | tail -1)"

# ...and it must be measuring GLOSS, not colour, or W6 bites.
# ...and it must be measuring GLOSS, not colour, or W6 bites.  ANCHORED ON
# CODE, NOT PROSE: a flat grep fired on the docstring sentence that EXPLAINS
# it does not compare colour -- the fourth time in this repository that a row
# has matched an explanation of a defect and called it the defect.  This one
# strips comments and docstrings first and looks only at what executes.
ck "gloss_compare compares no colour IN CODE"  0 "$(python3 -c "
import ast,re
src=open('gloss_compare.py').read()
t=ast.parse(src)
lines=set(range(1,src.count(chr(10))+2))
for n in ast.walk(t):                     # drop every docstring's line range
    if isinstance(n,(ast.Module,ast.FunctionDef,ast.ClassDef)):
        d=ast.get_docstring(n,clean=False)
        if d is not None:
            b=n.body[0]
            for i in range(b.lineno,(b.end_lineno or b.lineno)+1): lines.discard(i)
code=[l for i,l in enumerate(src.splitlines(),1)
      if i in lines and not l.strip().startswith('#')]
print(sum(1 for l in code if re.search(r'G/R|hue|chroma|saturation',l)))" 2>&1 | tail -1)"
ck "the audit's ranking rule is carried in the brief" 1 \
   "$(if [ -n "$_LATEST_BRIEF" ]; then grep -c 'RANK BY PIXELS OF THE DELIVERY FRAME' "$_LATEST_BRIEF"; else echo 0; fi)"

# ------------------------------- rev 58: F51 FIXED, AND THESE ROWS TEST THE FIX
# build.py used to construct the cyclorama, the lighting, the cabin fill and
# the camera INSIDE `if os.environ.get("T1_PREVIEW"):`, so anything that exec'd
# build.py to MEASURE got a scene with no lights.  It shipped a BLACK BUS
# delivery frame that passed every automated check (F51/F52) and it is the
# cause of F05's dead beauty arm.
#
# Rev 58 factored the sequence into studio.rig() and put a REFUSAL in
# render_set().  The rev-57b rows compared four duplicated copies of the
# sequence so the copies could not rot; there are no copies now, so those rows
# are RETIRED and replaced by rows that test what actually has to stay true.
# They are anchored on POSITION and COUNT, not on a grep for a name (sec.10.4):
# a grep passes on a comment, and every string below is load-bearing code.

# 1. ONE DEFINITION.  studio.py is the only file allowed to call the four
#    primitives.  If a script starts hand-rolling the sequence again, F51 is
#    back, and this is the row that says so.
ck "no file re-implements the studio rig" 0 "$(grep -l 'ST\.cyclorama()\|ST\.cabin_fill(\|ST\.ground_playa()' *.py 2>/dev/null | grep -v '^studio.py$' | grep -vx 'probe_dust_scope.py' | wc -l | tr -d '[:space:]')"

# 2. studio.rig() still builds all four, in build.py's original order.  The
#    order is load-bearing: clay must overwrite materials before the lights are
#    placed against them, and the camera comes last.
ck "studio.rig() builds the whole rig, in order" OK "$(python3 -c "
import re, ast
src = open('studio.py').read()
fn  = next(n for n in ast.parse(src).body
           if isinstance(n, ast.FunctionDef) and n.name == 'rig')
body = ast.get_source_segment(src, fn)
seq  = re.findall(r'\b(cyclorama|ground_playa|clay_all|lighting|playa|cabin_fill|camera)\(', body)
want = ['ground_playa','cyclorama','clay_all','playa','lighting','cabin_fill','camera']
print('OK' if seq == want else 'DRIFTED %s' % seq)" 2>&1 | tail -1)"

# 3. THE F51 INVARIANT ITSELF, tested by POSITION: the rig is built BEFORE and
#    OUTSIDE the preview block, not as a side effect of it.  If someone moves
#    the call back inside `if T1_PREVIEW:`, this fails and names the reason.
ck "build.py builds the rig OUTSIDE the preview block" OK "$(python3 -c "
src = open('build.py').read()
r = src.find('ST.rig_from_env(')
p = src.find('if os.environ.get(\"T1_PREVIEW\"):', src.find('_want_rig'))
print('OK' if 0 < r < p else 'rig_from_env@%d preview@%d -- F51 IS BACK' % (r, p))" 2>&1 | tail -1)"

# 4. THE GUARD PRECEDES THE RENDER.  assert_lit() has to run before any frame
#    is written or it guards nothing -- the same offset comparison rev 56 used
#    to prove a guard precedes a print.
ck "assert_lit precedes the render in render_set" OK "$(python3 -c "
import ast
src = open('studio.py').read()
fn  = next(n for n in ast.parse(src).body
           if isinstance(n, ast.FunctionDef) and n.name == 'render_set')
body = ast.get_source_segment(src, fn)
a, r = body.find('assert_lit('), body.find('bpy.ops.render.render(')
print('OK' if 0 < a < r else 'assert_lit@%d render@%d -- THE GUARD IS AFTER THE RENDER' % (a, r))" 2>&1 | tail -1)"

# 5. THE ABLATION STAYS REACHABLE.  A guard nobody can switch off has never
#    been watched failing (rule 3).  T1_NORIG=1 is what watched this one fail:
#    it suppresses the rig and build.py then refuses instead of writing a black
#    frame.  Watched printing, rev 58:
#      "REFUSING TO RENDER AN UNLIT SCENE -- 0 light objects and world strength 0.000"
ck "T1_NORIG ablation reads the environment" 2 "$(grep -c 'os.environ.get("T1_NORIG")' build.py)"
ck "T1_RIG lets a measuring tool ask for the rig" 1 "$(grep -c 'os.environ.get("T1_RIG")' build.py)"

# --------------------------------------------------- rev 55: A RE-FRAMING
# THE OWNER RETIRED A HEADING AND IT CAME BACK ONE BRIEF LATER.
# At rev 54 he ruled "we have all references that we need on repo", and sec.4
# was re-framed on main from "WHAT ONLY HE CAN GIVE" to "A CARRIER, NOT A LIST
# OF BLOCKERS" -- because the old heading is what licensed four revisions of
# parking the top job behind a photograph.  The rev-55 context merged that
# change and then carried the OLD heading into its own outgoing brief: the
# re-framing lived in rev 55's sec.4 and never propagated to rev 56's.
#
# IT SURVIVED RULE 17.  Rev 55's outgoing audit stat'ed every path, grepped
# every quoted string, resolved every T1_ switch and recomputed every figure --
# and none of that asks "was a re-framing carried forward".  A sweep over
# CONTENT cannot see a heading that should no longer exist, so the guard has to
# name it.  This row is the sweep's missing question, made testable.
#
# WATCHED FAILING on the rev-56 brief before it was fixed (got 1, want 0).
# ANCHORED ON THE LINE THAT *IS* THE HEADING, NOT ON THE PHRASE.  A brief that
# explains why the heading was retired has to be able to QUOTE it -- and the
# rev-56 brief does, in the note under its own sec.4.  This repo already
# learned that on the `DEFAULT IS STILL POINTINESS` row, whose whole point is
# that it must not fire on a comment that merely quotes the claim.  BOTH halves
# watched: it fires when the heading is real (got 2) and passes with the phrase
# quoted twice in prose.
ck "newest brief drops the retired sec.4 heading" 0 \
   "$(if [ -n "$_LATEST_BRIEF" ]; then grep -cE '^#+ .*WHAT ONLY HE CAN GIVE' "$_LATEST_BRIEF"; else echo 99; fi)"

# ------------- THE PLAYA HERO: A LINE THAT WAS IN "HIS SETTLED RULINGS" AND
# WAS NEVER HIS.  From rev 52 to rev 63 that list carried "playa_env.py is not
# on the table -- do not re-propose it".  It entered as a brief's INFERENCE
# from W6, whose object is the studio RIG, and was applied to a SECOND
# DELIVERABLE -- rule 34, written at rev 51-52 for exactly this move.  Asked
# after rev 62 with both readings quoted, he ruled "DEPRIORITISED, NOT
# CANCELLED".  These two rows hold the ruling and the sentence the rev-44
# carrier deletion cost, which was in NO live carrier from rev 44 to rev 57b.

# The owner's own sentence about his SECOND deliverable.  Losing it is what let
# rev 52 infer the item away, so both live carriers must hold it.
ck "the emotional bar is in BOTH live carriers" 2 \
   "$(python3 -c "
import glob,re
b=max(glob.glob('NEXT_CONTEXT_PROMPT_rev*.md'), key=lambda f:int(re.search(r'rev(\d+)',f).group(1)))
import os
brief = ('emotional bar' in open(b,errors='replace').read()
         or (os.path.exists('HANDOFF_CARRIERS.md')
             and 'emotional bar' in open('HANDOFF_CARRIERS.md',errors='replace').read()))
print(int(brief) + int('emotional bar' in open('OPEN_FINDINGS.md',errors='replace').read()))" 2>&1 | tail -1)"

# F92 records an OWNER RULING now, not a brief's inference -- which is the
# point of the row.  His words AND the grade, or it is half a retraction
# (rule 15).  WATCHED FAILING on the pre-ruling row, which scored 0 on both.
ck "F92 carries his ruling AND its grade" 2 "$(python3 -c "
t=open('OPEN_FINDINGS.md',errors='replace').read()
i=t.find('| **F92**'); row=t[i:t.find(chr(10),i)]
print(sum(k in row for k in ('DEPRIORITISED, NOT CANCELLED','RULED-rev57b')))" 2>&1 | tail -1)"

_BRIEF_TOTAL="$(if [ -n "$_LATEST_BRIEF" ]; then grep -E '\./verify_clone\.sh' "$_LATEST_BRIEF" 2>/dev/null | grep -oE 'ALL [0-9]+ PASS' | grep -oE '[0-9]+' | head -1; else echo 0; fi)"
# rev 60c-ii -- REMAINING_WORK_rev61.md declared itself a CARRIER and NO FILE
# IN THE REPOSITORY NAMED IT for a whole revision.  That is exactly how the
# standing-instructions carrier was lost at rev 44 and the open-findings
# register at rev 45 (CLAUDE.md rule 16).  A carrier nothing points at is a
# carrier already half gone, so the pointers are asserted, not trusted.
_RW="$(ls -1 REMAINING_WORK_rev*.md 2>/dev/null | sort -V | tail -1)"
ck "the ranked work list exists" OK "$([ -n "$_RW" ] && echo OK || echo MISSING)"
ck "README, START_HERE and the newest brief all name it" OK "$(
  _n=0
  for f in README.md START_HERE.md "$(ls -1 NEXT_CONTEXT_PROMPT_rev*.md | sort -V | tail -1)"; do
    grep -q "$_RW" "$f" 2>/dev/null && _n=$((_n+1))
  done
  [ "$_n" = 3 ] && echo OK || echo "only $_n of 3 name $_RW")"

# ------------- REV 64.  THE TRACED PRESSING WAS BUILT, RENDERED AND REFUTED,
# and the reason -- that every emblem target is read off a photograph that is
# not mirror-symmetric -- is the emblem's real blocker (F183/F184).  These rows
# hold the parts of that which can go stale silently.

# The trace is a LITERAL and a GENERATOR and the selftest holds the two
# together.  A traced constant nobody can re-derive is a number somebody typed.
ck "vw_pressing carries the trace AND its generator" 3 "$(python3 -c "
import vw_pressing as V
print(sum(bool(x) for x in (V.PRESSING_OUTER, V.PRESSING_HOLES, callable(V.trace))))" 2>&1 | tail -1)"

# Every terminal on the band's inner edge -- that is what makes the outline
# scale-free, so _fit_glyph can size it to any ring without encoding a diameter.
ck "the traced outline is scale-free (terminals on the band)" OK "$(python3 -c "
import vw_pressing as V
r = max((x*x+y*y)**0.5 for x, y in V.PRESSING_OUTER)
print('OK' if abs(r - V.BAND_INNER) < 0.01 else 'r max %.4f vs band %.4f' % (r, V.BAND_INNER))" 2>&1 | tail -1)"

# THE HOLES ARE LOAD-BEARING.  The V and the W touch, so the cream cells
# between them are enclosed holes; dropping them changes the topology C6 counts.
ck "the traced glyph keeps its enclosed holes" 2 "$(python3 -c "
import vw_pressing as V; print(len(V.PRESSING_HOLES))" 2>&1 | tail -1)"

# T1_VW_TRACED IS MEASUREMENT-ONLY AND MUST STAY OFF.  It was built, rendered
# and refuted (F183); a default flip would ship the blob.  Asserted, not trusted.
ck "T1_VW_TRACED is OFF by default" 1 "$(grep -c 'os.environ.get("T1_VW_TRACED") == "1"' t1_core.py)"
ck "nothing sets T1_VW_TRACED for the build" 0 "$(grep -l 'T1_VW_TRACED=1' build.py studio.py t1_detail.py 2>/dev/null | wc -l | tr -d ' ')"

# solid_with_holes must NOT be reached by any cutter.  The rev-44 cap
# triangulation inside solid_prism broke two wheel-arch booleans; this is a
# separate function and that separation is the whole reason it is safe.
ck "solid_with_holes is not used by any cutter" 0 "$(grep -n 'solid_with_holes' t1_core.py t1_shell.py t1_detail.py build.py 2>/dev/null | grep -cE 'cut|arch|boolean|gap_prism')"

# F184's instrument: a mirror-symmetry statistic with a KILL that was watched
# firing.  A control whose kill cannot go red is not a control (rule 42).
ck "the shear probe carries its own KILL" 1 "$(grep -c 'ck("S1k"' probe_rev64_shear.py)"

# F186's repair is load-bearing and must stay red if registration is removed.
ck "T3's registration repair is held by a kill" 1 "$(grep -c 'ctl("T3d"' probe_rev63_trace.py)"

# F190 -- the carrier for the top item said the constants were NOT shipped
# while the tree carried them, for a whole revision.  Rule 13.  Both the
# carrier and the register now say so; assert it so it cannot be smoothed away.
ck "EMBLEM_HANDOFF retracts its false control sentence" 1 \
   "$(grep -c 'RETRACTED AT REV 64' EMBLEM_HANDOFF.md)"
ck "the six shipped constants are what the carrier now names" 6 "$(python3 -c "
import re
s = open('t1_core.py').read()
want = {'VW_V_TIP_X': '0.3287', 'VW_APEX_Z': '0.0538', 'VW_W_ARM_X': '1.1002',
        'VW_W_ARM_Z': '0.4350', 'VW_W_TROUGH_X': '0.3111', 'VW_W_TROUGH_Z': '-0.6445'}
print(sum(bool(re.search(r'^%s = %s$' % (k, re.escape(v)), s, re.M))
          for k, v in want.items()))" 2>&1 | tail -1)"

# F191/F192 -- two owner rulings arrived at rev 64.  A ruling in no carrier is
# how this project lost the Playa hero for six revisions (F92).
ck "rev 64's owner rulings are in the register" 2 "$(python3 -c "
t = open('OPEN_FINDINGS.md', errors='replace').read()
print(sum(k in t for k in ('Keep holding', 'large-format print')))" 2>&1 | tail -1)"

# ------------- REV 65.  THE BADGE'S RING IS FITTED AS AN ELLIPSE AND C8's
# TARGET IS RE-BASED (F194).  These rows hold the parts that can go stale.

# The un-projection must be PROVED ON A KNOWN ANSWER before it is pointed at a
# photograph.  If that positive control is ever removed, the method is a guess.
ck "the un-projection carries its positive control" 1 \
   "$(grep -c 'C2. THE POSITIVE CONTROL' probe_rev65_unproject.py)"

# F195 -- the mirror-IoU rotation search scored BETTER and produced a non-VW.
# It is kept unused as a control; if it is ever re-enabled, this goes red.
ck "the refuted rotation search is not used to produce a target" 0 \
   "$(grep -cE '^[^#]*OUT\[nm\] = normalise\(best_upright' probe_rev65_unproject.py)"
ck "the rotation search is held by a control" 1 "$(grep -c 'ctl("C7"' probe_rev65_unproject.py)"

# F194 -- C8's target moved because the RULER moved, not the model.  The
# register must carry both numbers or the next context quotes the old one.
ck "the register carries C8's re-based target" 2 "$(python3 -c "
t = open('OPEN_FINDINGS.md', errors='replace').read()
print(sum(k in t for k in ('2.960', '2.627')))" 2>&1 | tail -1)"

# F193 -- his third hold on the delivery render, and the multi-size spec that
# comes with it.  A ruling in no carrier is how the Playa hero was lost.
ck "rev 65's owner ruling is in the register" 1 "$(python3 -c "
t = open('OPEN_FINDINGS.md', errors='replace').read()
print(int('MULTIPLE SIZES, MAX RESOLUTION, MAX FIDELITY' in t))" 2>&1 | tail -1)"

# ---------------------------------------------------- rev 67: THE NOSE (F197)
# The owner named the nose's SHAPE at rev 65 and RULED it first at rev 66, over
# finishing the emblem.  Until rev 67 the nose's PLAN BULGE -- the forward
# convexity of the whole face -- had no constant of its own, no ablation, no
# probe and no row here.  These rows are ARITHMETIC and BEHAVIOUR, not greps
# for a name (SS10 item 4).

# 1. The constant exists, is on its own line, and is the one nose_shape() uses.
#    Anchored on the ARITHMETIC: NOSE_BULGE * w * max(0, 1-r) must be what the
#    bulge is built from, so a literal creeping back in is caught.
ck "nose: the plan bulge is a named constant, not a literal" 1 \
   "$(grep -c '^NOSE_BULGE = 0.019' t1_shell.py)"
# RE-BASED AT REV 68, WITH THE CAUSE NAMED AND FOUR COMPANION ROWS.
# THE CAUSE: rev 68 factored the bulge expression out of `nose_shape` into
# `t1_shell.nose_bulge_at`, because `build.py` has to ask the same question to
# keep the nose fixtures on the skin (F217) and two copies of it would drift
# apart.  The row that stood here was
#     grep -c 'bulge = NOSE_BULGE \* w \* max' t1_shell.py
# -- A GREP FOR A SOURCE STRING, in a block whose own comment says these rows
# "are ARITHMETIC and BEHAVIOUR, not greps for a name (SS10 item 4)".  It was
# never testing the arithmetic it claimed to; it went red on a refactor that
# preserved every value it was written to protect.
# THE RE-BASE IS TO BEHAVIOUR, and it is STRICTLY STRONGER: it EVALUATES the
# function against the arithmetic written by hand, so a literal creeping back in
# is caught by the number disagreeing, not by a string going missing.
ck "nose: nose_bulge_at IS NOSE_BULGE*w*max(0,1-r), evaluated not grepped" "OK" \
   "$(python3 -c "
import t1_shell as S
x, y, z = 2.1015, 0.5450, 0.9330
w = min(1.0, max(0.0, (x - 1.86) / 0.17)); w = w * w * (3 - 2 * w)
r = (y / 0.80) ** 2 + ((z - 1.00) / 0.46) ** 2
print('OK' if abs(S.nose_bulge_at(x, y, z) - S.NOSE_BULGE * w * max(0.0, 1.0 - r))
      < 1e-12 else 'MISMATCH')" 2>&1 | tail -1)"
ck "nose: no bare 0.019 bulge literal survives in nose_shape" 0 \
   "$(grep -c 'bulge = 0.019' t1_shell.py)"
# COMPANION 1.  nose_shape must CALL the one expression, not carry a second copy.
ck "nose: nose_shape calls nose_bulge_at rather than re-typing it" 1 \
   "$(grep -c 'bulge = nose_bulge_at(x, y, z)' t1_shell.py)"
# COMPANION 2.  The expression must be LINEAR in the constant, because
# nose_fixture_dx is a DIFFERENCE of two evaluations of it and is only exact if
# it is.  Watched at rev 68: 0.01955799 both ways.
ck "nose: nose_bulge_at is linear in the constant (the fixture offset needs it)" "OK" \
   "$(python3 -c "
import t1_shell as S
a = S.nose_bulge_at(2.1015, 0.5450, 0.9330, amount=0.038)
b = 2 * S.nose_bulge_at(2.1015, 0.5450, 0.9330, amount=0.019)
print('OK' if abs(a - b) < 1e-12 else 'NONLINEAR %.8f %.8f' % (a, b))" 2>&1 | tail -1)"
# ------------------------------------------------------- rev 69, F233
# THE EMBLEM'S RENDER SIDE.  F205 stood for three revisions as "the render cuts
# 3 cells where the photograph cuts 6" -- the project's top item -- and the
# measurement behind it EXISTED IN NO COMMITTED FILE.  These rows are
# BEHAVIOUR: they RUN the instrument, not grep for it.
ck "emblem: the photograph still reads SIX interior cream cells" 6 \
   "$(python3 -c "
import probe_rev69_emblem as E, probe_rev46_vw as P, numpy as np, scipy.ndimage as ndi
from PIL import Image
a = np.asarray(Image.open('ref_nolita_front34.jpg').convert('RGB')).astype(float)
ring, c = E.find_emblem(a, E.PHOTO_BOX)
f = ndi.binary_fill_holes(ring); ys, xs = np.nonzero(f)
sub = a[ys.min():ys.max()+1, xs.min():xs.max()+1]
d = f[ys.min():ys.max()+1, xs.min():xs.max()+1]
print(P.cream_cells(E.ink_mask(sub, d, 30), interior=True)[0])" 2>&1 | tail -1)"
# THE FINDER MUST ADMIT THE OBLIQUE ROUNDEL.  My first cut used a squareness
# bound of 0.6 and REJECTED THE REFERENCE FRAME -- the photograph's roundel is
# 41 x 69 px, aspect 0.594.  An instrument whose finder cannot find the
# reference is not an instrument.
ck "emblem: the finder admits the PHOTOGRAPH's oblique roundel" "found" \
   "$(python3 -c "
import probe_rev69_emblem as E, numpy as np
from PIL import Image
a = np.asarray(Image.open('ref_nolita_front34.jpg').convert('RGB')).astype(float)
r, c = E.find_emblem(a, E.PHOTO_BOX)
print('found' if r is not None else 'REJECTED THE REFERENCE FRAME')" 2>&1 | tail -1)"
# AND A CONTROL THAT DID NOT RUN MUST NOT READ AS A PASS (rule 3, F225's shape).
ck "emblem: with no frame the probe SAYS the render rows did not run" 1 \
   "$(python3 probe_rev69_emblem.py 2>/dev/null | grep -c 'render rows are ABSENT, NOT')"

# ---------------------------------------------------- rev 69, F222/F232
# THE FRONT BUMPER'S PLAN BOW.  It was DEAD FLAT for sixty-eight revisions --
# eleven points at constant x under t1_detail.bumper's own `# flat nose face`
# comment -- measuring +0.05 mm over |y| <= 0.70, the span the photographs are
# traced on.  These rows are ARITHMETIC AND BEHAVIOUR, not greps (rule 50): the
# grep row this block replaces in spirit went red at rev 68 on a refactor that
# preserved every value it protected.
ck "bumper: the plan bow is a named constant on its own line" 1 \
   "$(grep -c '^BUMP_BOW = 1.0' t1_detail.py)"
ck "bumper: T1_BUMP_BOW actually overrides it, in a fresh process" "0.35/1.0" \
   "$(python3 -c "
import os, subprocess, sys
def g(env):
    return subprocess.run([sys.executable, '-c',
        'import t1_detail as D; print(D._bump_bow())'], capture_output=True,
        text=True, env=dict(os.environ, **env)).stdout.strip()
print('%s/%s' % (g({'T1_BUMP_BOW': '0.35'}), g({})))" 2>&1 | tail -1)"
ck "bumper: the face takes its shape from the FACE's station, not the blade's" 1 \
   "$(grep -c '_skin = _nose_plan_x(BUMP_BOW_Z)' t1_detail.py)"
# THESE TWO WERE WRITTEN AS GREPS FIRST AND BOTH WERE WRONG -- RULE 50, TWICE
# IN ONE BLOCK.  "the old constant-x face is gone" matched the HISTORICAL LINE
# QUOTED IN THE NEW COMMENT, so it read 1 and failed; and "a partially draped
# face REFUSES" never matched because the message is SPLIT ACROSS TWO SOURCE
# LINES, which a line-oriented grep cannot see.  Both are behaviour now.
#
# THE CHANGE WAS SCOPED TO THE FRONT.  The REAR bumper still sweeps a flat tail
# face and must keep doing so -- there is no photograph of a bowed tail bumper
# and nothing was measured there.  This is the containment arm.
ck "bumper: the change was scoped to the FRONT -- the tail face is untouched" 1 \
   "$(grep -c '# flat tail face' t1_detail.py)"
# THE REFUSAL, EXERCISED FOR REAL -- AND THE FIRST VERSION OF THIS ROW TESTED
# THE ONE BRANCH THAT DOES NOT REFUSE.  It asserted only that `_nose_plan_x`
# returns None with no body, and CALLED THAT "the branch the RuntimeError
# guards".  It was not: with `_skin is None` the miss counter stayed 0, nothing
# raised, and the face was built FLAT -- the very defect F222 removes -- behind
# a suffix on a log line.  An adversary found it.  Both halves are now real:
# the source returns None, AND building a face with no body RAISES.
ck "bumper: the drape source returns None rather than inventing a curve" "None" \
   "$(python3 -c "
import t1_detail as D
print(D._nose_plan_x(1.10))" 2>&1 | tail -1)"
ck "bumper: and building the face with NO BODY actually REFUSES" "RuntimeError" \
   "$(python3 -c "
import t1_detail as D
try:
    D.bumper(True, name='probe_nobody')
    print('BUILT A FLAT FACE SILENTLY')
except RuntimeError:
    print('RuntimeError')
except Exception as e:
    print(type(e).__name__)" 2>&1 | tail -1)"

# ------------------------------------------------------- rev 68, F217
# COMPANION 3.  THE FIXTURE OFFSET IS EXACTLY ZERO WHERE IT SHIPS.  This is the
# containment property: rev 68 changed no shipped vertex.  If it is ever
# non-zero at the authored value, the shipped build has moved.
ck "nose: the fixture follow is EXACTLY zero at the authored bulge" "0.0" \
   "$(python3 -c "
import t1_shell as S
print(abs(S.nose_fixture_dx(2.1015, 0.5450, 0.9330)))" 2>&1 | tail -1)"
# COMPANION 4.  AND IT ACTUALLY MOVES WHEN THE BULGE DOES -- rule 47.  An
# offset that is always zero is F208's no-op wearing a different hat.  Watched
# at rev 68: 13.38 mm at NOSE_BULGE 0.045, and 0.00 with the follow ablated.
ck "nose: the fixture follow MOVES with the bulge, and its ablation kills it" \
   "13.38/0.00" "$(T1_NOSE_BULGE=0.045 python3 -c "
import os, subprocess, sys, t1_shell as S
on = 1000 * S.nose_fixture_dx(2.1015, 0.5450, 0.9330)
off = subprocess.run([sys.executable, '-c',
    'import t1_shell as S; print(1000*S.nose_fixture_dx(2.1015,0.5450,0.9330))'],
    capture_output=True, text=True,
    env=dict(os.environ, T1_NOSE_FIXFOLLOW='0')).stdout.strip()
print('%.2f/%.2f' % (on, float(off)))" 2>&1 | tail -1)"
# COMPANION 5.  THE PLACEMENT LITERALS MUST NOT COME BACK.  Both were typed
# against a nose at NOSE_BULGE 0.019 and neither may be placed raw again.
ck "nose: the headlamp x is derived from the skin, not placed raw" 1 \
   "$(grep -c 'HL_X = HL_X0 + S.nose_fixture_dx(HL_X0, HL_Y, HL_Z)' build.py)"
ck "nose: the indicator x is derived from the skin, not placed raw" 0 \
   "$(grep -c 'loc=(2.0960' build.py)"

# 2. The ablation is wired.  T1_NOSE_BULGE must actually reach the constant --
#    an ablation switch that no longer ablates is exactly what rev 67 found had
#    happened to T1_VW_CAPMIN (F208), and it reads to the next agent as
#    "no effect => not the lever".
ck "nose: T1_NOSE_BULGE overrides the constant" 0.05 \
   "$(T1_NOSE_BULGE=0.05 python3 -c "import t1_shell; print(t1_shell.NOSE_BULGE)" 2>&1 | tail -1)"
ck "nose: without the env var the shipped constant stands" 0.019 \
   "$(python3 -c "import t1_shell; print(t1_shell.NOSE_BULGE)" 2>&1 | tail -1)"

# 3. The probe's edge-acceptance rule is ARITHMETIC, and it must refuse the two
#    traces rev 67 watched it refuse.  A bar that cannot refuse is not a bar --
#    rev 67's first cut (12 % of span) passed a whole-frame scan with an rms of
#    61.85 px on 831 px, and the absolute term is what stops it.
ck "nose: the probe's edge bar refuses fragments and keeps the one real edge" \
   "EDGE-FRAG-FRAG" "$(python3 -c "
import probe_rev67_nose as P
print('-'.join('EDGE' if r <= P.rms_bar(s) else 'FRAG'
               for r, s in ((2.8, 118.0), (17.6, 105.0), (61.85, 831.0))))" 2>&1 | tail -1)"

# 4. The photographed bumper is CURVED -- the projection-invariant half of the
#    nose measurement.  A straight 3-D line images straight under ANY pinhole
#    camera, so this is shape, not pose.  Guarded on the SIGMA, not the pixels.
ck "nose: the photographed bumper's curvature is many sigma, not noise" "OK" \
   "$(python3 -c "
import probe_rev67_nose as P
a, e = P.bumper_top('ref_nolita_front34.jpg', (128, 256), (300, 395))
s = P.sagitta(e)
print('OK' if abs(s['sag']) > 3 * s['se'] and s['rms'] <= P.rms_bar(s['span']) else
      'sag %.2f se %.2f rms %.2f' % (s['sag'], s['se'], s['rms']))" 2>&1 | tail -1)"

# ---- rev 71: THE INSTRUMENT FINDINGS.  ANCHORED ON BEHAVIOUR AND ARITHMETIC,
# NOT ON A GREP FOR A NAME (rule 50).
#
# F246.  P1b is the row that says the emblem's control is not framed the way
# its measurement is.  It REFUSES on a shipped tree and it is MEANT to.  These
# rows guard against it being deleted, or its bar widened to make it pass --
# which is the shape of every relaxation this project has caught (rule 44).
ck "the emblem probe carries the bbox-framed control" 1 \
   "$(grep -c 'P1b CONTROL, FRAMED THE WAY EVERY REAL TARGET IS FRAMED' probe_rev69_fitpose.py)"
ck "P1b's bar is still 0.90, not widened to admit its own refusal" 1 \
   "$(grep -c 'v_ctl_bb > 0.90' probe_rev69_fitpose.py)"
ck "P1b PASSES on the repaired search" PASS \
   "$(python3 probe_rev69_fitpose.py 2>&1 | grep -o 'PASS] P1b' | head -1 | cut -d']' -f1 | sed 's/\[//')"
# ...AND ITS KILL: the rev-69 search drives the same control back under the bar.
ck "T1_FITPOSE_LEGACY drives P1b RED -- the repair is WATCHED, not asserted" FAIL \
   "$(T1_FITPOSE_LEGACY=1 python3 probe_rev69_fitpose.py 2>&1 | grep -o 'FAIL] P1b' | head -1 | cut -d']' -f1 | sed 's/\[//')"
# F247.  ARITHMETIC, not a grep: the figure the guard records as its watched
# failure must EXCEED the bar the guard actually applies.  86.3 < 90.0 is how
# rev 70 recorded a "watched failure" its own row admits.
ck "the tail-board guard's recorded failure EXCEEDS its own bar" OK \
   "$(python3 - <<'PY'
import re
s = open('verify.py').read()
m = re.search(r'TIP_Z, TIP_BAND = ([\d.]+), ([\d.]+)', s)
w = re.search(r'tip 2\.2790, \+([\d.]+) mm', s)
print('OK' if (m and w and float(w.group(1)) > float(m.group(2)) * 3000.0) else 'NO')
PY
)"
# F248.  Ask the SCRIPT which views it post-processes, not the prose about it.
ck "judge_set.sh post-processes the delivery view" OK \
   "$(awk '/^for v in/{sub(/#.*/,""); print (/hero34f/ && /hero34r/) ? "OK" : "NO"; exit}' judge_set.sh)"
ck "judge_set.sh no longer loops over a view no preview list produces" 0 \
   "$(awk '/^for v in/{sub(/#.*/,""); print; exit}' judge_set.sh | grep -c 'hero ')"
# F251.  The 2-D proxy is only usable while it IS the build.
ck "the emblem proxy still reproduces the bpy build exactly" 1 \
   "$(python3 probe_rev71_proxy.py 2>&1 | grep -c 'IoU 1.000000')"

# ---- rev 71, SECOND HALF: THE READER, THE PROTOCOL, AND THE WITHDRAWALS.
# F263.  THE ROW IS BEHAVIOURAL AND IT DOES NOT DEPEND ON PIL BEING BROKEN.
# read_png must agree with PIL wherever PIL has bits, and must return MORE bits
# than PIL where the file has them.  Written on a file this script AUTHORS, so
# it needs no frame in out/ (out/ starts empty on a clone).
ck "photometry.read_png recovers 16 bits and agrees with PIL on the top 8" "16/OK" \
   "$(python3 - <<'PY' 2>&1 | tail -1
import numpy as np, tempfile, os
from PIL import Image
import photometry as PH
rng = np.random.default_rng(7)
a = (rng.integers(0, 65536, (37, 53, 3))).astype(np.uint16)
f = os.path.join(tempfile.mkdtemp(), "t.png")
PH._write_png16(f, a)
got, mx = PH.read_png(f)
pil = np.asarray(Image.open(f))
same = np.array_equal(got, a)
top = np.array_equal((got >> 8).astype(np.uint8), pil) if pil.dtype == np.uint8 else True
print("%d/%s" % (16 if mx == 65535 else 8, "OK" if (same and top) else "NO"))
PY
)"
# ...AND THE PROTOCOL REFUSES WHAT IT SAYS IT REFUSES.  Two behavioural kills.
ck "photometry REFUSES an AgX frame and an undeclared transform" "REFUSE/REFUSE" \
   "$(python3 - <<'PY' 2>&1 | tail -1
import photometry as PH
def r(t):
    try:
        PH.load_linear("ref_side.jpg", t); return "PASS"
    except ValueError:
        return "REFUSE"
print("%s/%s" % (r("agx"), r("guess")))
PY
)"
ck "photometry's selftest runs every rule it claims, and every kill fires" "9/0" \
   "$(python3 photometry.py 2>&1 | awk '/checked, .* FAILED/{print $1"/"$3}' | tail -1)"
# F264's shape: a suite that cannot fail is not a suite.  WATCHED -- breaking the
# robust statistic must turn the selftest RED.  If this row ever reads 0 FAILED
# the median check has gone void again, which is exactly how it shipped.
ck "the selftest's robustness check REFUSES when the median is swapped out" "FAILS" \
   "$(python3 - <<'PY' 2>&1 | tail -1
import numpy as np, io, contextlib
import photometry as PH
real = np.median
np.median = np.mean
try:
    with contextlib.redirect_stdout(io.StringIO()) as buf:
        n = PH.selftest()
finally:
    np.median = real
print("FAILS" if n > 0 else "GREEN")
PY
)"
# F262/F255.  THE WITHDRAWAL MUST LIVE WHERE RULE 9 READS -- in P4's own message,
# not only in prose.  Rev 71 asserted this patch in a finding before it landed.
ck "P4's message carries F262's withdrawal, not a licence to ship the trace" "OK" \
   "$(python3 - <<'PY' 2>&1 | tail -1
# read the SOURCE, do not import it: importing pulls in bpy and takes ~70 s.
flat = ' '.join(open('probe_rev69_fitpose.py').read().split())
print('OK' if ('NOT** A LICENCE TO SHIP THE TRACE' in flat.replace('" "', '')
               and 'F183' in flat) else 'NO')
PY
)"
ck "P4 no longer tells the reader to re-open F183" 0 \
   "$(grep -c 'F183 needs re-opening' probe_rev69_fitpose.py)"
ck "F255 is annotated with its own withdrawal" 1 \
   "$(grep -c 'WITHDRAWN IN THE SAME REVISION BY \*\*F262\*\*' OPEN_FINDINGS.md)"
ck "F261 is not published as a closed magnitude" 1 \
   "$(grep -c 'PROVENANCE-REFUTED-rev71' OPEN_FINDINGS.md)"
# F257's shape: a probe must not PRINT a decomposition it did not compute (F198).
ck "the red probe's decomposition is computed, not typed" "0/1" \
   "$(python3 - <<'PY' 2>&1 | tail -1
s = open('probe_rev71_red.py').read()
typed = s.count('44 % of the gap') + s.count('ENVIRONMENT 65 %')
live = 1 if 'NOT RENDERED -- row ABSENT' in s else 0
print("%d/%d" % (typed, live))
PY
)"
ck "the red probe REFUSES a frame with no declared transform" 3 \
   "$(python3 probe_rev71_red.py out/nonexistent_side.png >/dev/null 2>&1; echo $?)"
# T1_DIFFB is the ablation F261 could not be reproduced without.  Wired, not named.
# F266.  THE PHYSICS CLOSURE'S ACCEPTANCE CONDITION MUST STAY PRINTED.  A
# decomposition read off a ruler that has not been shown exposure-invariant is
# what F261 was, and it was withdrawn.  BEHAVIOURAL: the probe must emit the
# condition on a bare run, where it computes nothing at all.
ck "the red probe prints its exposure-invariance acceptance condition" 1 \
   "$(python3 probe_rev71_red.py 2>&1 | grep -c 'ACCEPTANCE CONDITION')"
ck "the register quotes F266, not F261's withdrawn magnitudes" "1/1" \
   "$(python3 - <<'PY' 2>&1 | tail -1
s = open('OPEN_FINDINGS.md').read()
print("%d/%d" % (1 if '| **F266** |' in s else 0,
                 1 if 'F266 is the one to quote' in s.replace('**','') else 0))
PY
)"
# F265.  A SUITE THAT DIRTIES THE TREE IT CHECKS CANNOT REACH ALL-PASS TWICE.
# probe_rev69_fitpose.py paints its best fit to a TRACKED file, and this script's
# own LAST emblem row runs it under T1_FITPOSE_LEGACY=1 -- whose best pose is a
# DIFFERENT one.  So row "modified tracked files" (line 115) was failed by row
# ~395 of the same run, and it looked like nondeterminism.  The kill now paints
# to its own path.  ARITHMETIC, not a grep: the two paths must differ.
ck "the fitpose kill paints to its own file, not over the shipped evidence" "DIFFER" \
   "$(python3 - <<'PY' 2>&1 | tail -1
flat = ' '.join(open('probe_rev69_fitpose.py').read().split())
print("DIFFER" if ('rev69_fitpose_legacy.png' in flat
                   and 'rev69_fitpose_regions_legacy.png' in flat) else "SAME")
PY
)"
ck "T1_DIFFB reaches the renderer's diffuse bounce count" 1 \
   "$(grep -c 'sc.cycles.diffuse_bounces = int(os.environ.get("T1_DIFFB"' studio.py)"

# ---------------------------------------------------------------------------
# REV 72's FIXES, LOCKED SO THEY CANNOT SILENTLY REGRESS.
#
# THE OWNER'S INSTRUCTION AT THE CLOSE OF REV 72: "set up for success so that it
# can only carry forward, no regression allowed."  A BRIEF CANNOT DO THAT.  Rev
# 72 fixed four instruments and added a validator, and NOT ONE of them had a row
# -- so any of them could have been reverted, refactored away, or "tidied" and
# the next close would still have read ALL PASS.  These rows are BEHAVIOURAL:
# they RUN the thing and read what it does (rule 50 -- a grep tells you a name
# is present and nothing else).  Cost, measured: about 16 s in total.
#
# EVERY ONE WAS WATCHED FAILING against the pre-rev-72 behaviour before it was
# written into this file (rule 3); the values are read off runs, not typed.
# ⚠ rev 73, F287 -- THIS ROW WAS NAMED "bare" AND RUNS `--nomesh`, AND THE TWO
# ARE NOT THE SAME RUN.  Measured at rev 73, true exit codes, no pipe:
#     probe_rev67_nose.py            -> 4 checked, 0 FAILED, 1 ABSENT, rc 2
#     probe_rev67_nose.py --nomesh   -> 2 checked, 0 FAILED, 1 ABSENT, rc 2
# Bare runs P1, P2 and the two mesh rows; `--nomesh` drops the mesh rows.  The
# rc-2 / ABSENT behaviour this row locks is REAL and identical on both paths --
# only the NAME was wrong, and it was wrong in five places at once (F275's
# register row, this row, probe_rev67_nose.py's own comment, LEDGER_rev72.md §3
# and the rev-73 brief), all of them publishing the `--nomesh` count of 2 as
# the "bare" one.  A guard written to lock a fix could not see the mislabel
# because it REPRODUCED it.  RENAMED, not re-based: the assertion is untouched.
# `--nomesh` is deliberate here -- bare costs a ~70 s in-process build.
_R72_NOSE="$(python3 probe_rev67_nose.py --nomesh >/tmp/_r72n.txt 2>&1; echo $?)"
ck "F275 probe_rev67_nose --nomesh EXITS NON-ZERO on an absent frame" 1 \
   "$([ "${_R72_NOSE:-0}" -ne 0 ] && echo 1 || echo 0)"
# and the count that goes with THAT invocation, so the two can never drift
# apart again without a row going red (F287)
ck "F287 ... and --nomesh's own summary count is 2, not the 4 a bare run gives" 1 \
   "$(grep -cE '^  2 checked, 0 FAILED, 1 ABSENT' /tmp/_r72n.txt)"
# ⚠ THE FIRST CUT OF THIS ROW COUNTED OCCURRENCES OF "ABSENT" AND TYPED want=1.
# It read 2 -- the word appears in the summary AND in the "NOT A PASS" line --
# so the row went red on a probe that was behaving correctly.  Rule 5, caught by
# running it.  What matters is that the SUMMARY LINE carries it, because rule 9
# says read the summary and never the exit code; that is what is tested now.
ck "F275 ... and its SUMMARY LINE says ABSENT, not a clean pass (rule 9 reads it)" 1 \
   "$(grep -cE 'checked,.*ABSENT' /tmp/_r72n.txt)"
_R72_GC="$(python3 gloss_compare.py out/_r72_absent_frame.png >/tmp/_r72g.txt 2>&1; echo $?)"
ck "F274 gloss_compare REFUSES a NAMED missing frame instead of a traceback" 3 \
   "${_R72_GC:-0}"
ck "F274 ... and says NO RENDER rather than dying inside Image.open" 1 \
   "$(grep -c 'NO RENDER' /tmp/_r72g.txt)"
_R72_BITS="$(python3 probe_rev72_bits.py >/tmp/_r72b.txt 2>&1; echo $?)"
ck "rule 37: probe_rev72_bits bare refuses (2 ABSENT, non-zero)" 1 \
   "$([ "${_R72_BITS:-0}" -ne 0 ] && grep -q 'ABSENT' /tmp/_r72b.txt && echo 1 || echo 0)"
# F273/F280.  revstats is the OWNER'S OWN drift instrument and it was wrong in
# two ways at once: it double-counted every PR-landed revision, and it printed a
# HARD-CODED baseline that disagreed with the table nine lines above it.  These
# two rows hold both fixes.  The baseline must be COMPUTED and the retired
# figure must be GONE -- CLAUDE.md deleted 721 as wrong and it came back once.
python3 revstats.py > /tmp/_r72r.txt 2>&1
ck "F280 revstats' baseline is COMPUTED from the run, not typed" 1 \
   "$(grep -c 'COMPUTED from this run' /tmp/_r72r.txt)"
ck "F280 ... and the retired 721 / 1.55 baseline has NOT come back" 0 \
   "$(grep -cE '721 geometry|ratio of 1\.55' /tmp/_r72r.txt)"
ck "F273 revstats accounts for merges separately, not by counting them twice" 1 \
   "$(grep -c 'merges' revstats.py | awk '{print ($1>0)?1:0}')"
# F281.  The rear hatch's angle switch REFUSES a pose its hinge cannot express,
# AND its message must clear _hinge_y by name.  Before rev 72 this died three
# frames down on an assert that told the reader to go and debug _hinge_y, which
# is not at fault; a guard that names the wrong suspect is worse than none.
T1_REAR_OPEN=-64 python3 -c 'import t1_shell' >/tmp/_r72s.txt 2>&1
ck "F281 T1_REAR_OPEN=-64 REFUSES at the parse site, naming the switch" 1 \
   "$(grep -c 'T1_REAR_OPEN=-64 is outside 0..180' /tmp/_r72s.txt)"
ck "F281 ... and its message CLEARS _hinge_y, which is not at fault" 1 \
   "$(grep -c 'which is not at fault' /tmp/_r72s.txt)"
T1_REAR_OPEN=banana python3 -c 'import t1_shell' >/tmp/_r72t.txt 2>&1
ck "F281 a non-numeric T1_REAR_OPEN refuses too, rather than crashing" 1 \
   "$(grep -c 'is not a number' /tmp/_r72t.txt)"
rm -f /tmp/_r72n.txt /tmp/_r72g.txt /tmp/_r72b.txt /tmp/_r72r.txt /tmp/_r72s.txt /tmp/_r72t.txt

# ---------------------------------------------------------------------------
# REV 73's OWN LOCK.  Same contract as the block above: BEHAVIOURAL rows that
# RUN the thing and read what it does, every one WATCHED FAILING against the
# pre-rev-73 code before it was written here (rule 3).  They cost ~3 s: none
# of them builds the mesh, and none of them needs a frame out of `out/`, which
# starts EMPTY on a clone (rule 37 -- a row that cannot run must not read as a
# pass).  A 2x2 PNG carrying the right FILENAME is enough, because what is
# under test is the probe's REFUSAL LOGIC, not its arithmetic.
python3 - <<'_PYMK' >/dev/null 2>&1
from PIL import Image
for n in ("_r73_x_hero34f.png", "_r73_x_front.png"):
    Image.new("RGB", (2, 2), (128, 0, 0)).save("/tmp/" + n)
_PYMK
python3 probe_rev67_nose.py /tmp/_r73_x_hero34f.png --nomesh >/tmp/_r73a.txt 2>&1
ck "F284 probe_rev67_nose REFUSES to window a frame that is not the \`front\` elevation (rule 42)" 1 \
   "$(grep -c 'is not a .front. frame' /tmp/_r73a.txt)"
ck "F284 ... and counts that refusal as ABSENT, never as a pass (rule 37)" 1 \
   "$(grep -cE 'checked,.*ABSENT' /tmp/_r73a.txt)"
python3 probe_rev67_nose.py /tmp/_r73_x_front.png --nomesh >/tmp/_r73b.txt 2>&1
ck "F284 ... and REFUSES a \`front\` frame with no build, because the window is PROJECTED" 1 \
   "$(grep -c 'window is PROJECTED off the built fixtures' /tmp/_r73b.txt)"
T1_NOSE_NOWIN=1 python3 probe_rev67_nose.py /tmp/_r73_x_front.png --nomesh >/tmp/_r73c.txt 2>&1
ck "F284 the T1_NOSE_NOWIN kill really ablates -- it restores the WHOLE-FRAME scan (rule 47)" 1 \
   "$(grep -c 'T1_NOSE_NOWIN -- ABLATED, whole frame' /tmp/_r73c.txt)"
ck "F284 ... and the ablated window is NOT the projected one, so the switch cannot go inert" 0 \
   "$(grep -c 'projected off hl_ring' /tmp/_r73c.txt)"
# F286 -- the refusal that had no summary line for rule 9 to read.
python3 probe_rev71_red.py /tmp/_r73_x_front.png --transform=agx >/tmp/_r73d.txt 2>&1
ck "F286 probe_rev71_red REFUSES an AgX frame with a SUMMARY LINE, not a bare traceback (rule 9)" 1 \
   "$(grep -cE '^  0 checked, 0 FAILED, 1 REFUSED' /tmp/_r73d.txt)"
ck "F286 ... and the traceback is GONE -- rule 51, losing the input is a RESULT, print it" 0 \
   "$(grep -c 'Traceback (most recent call last)' /tmp/_r73d.txt)"
rm -f /tmp/_r73a.txt /tmp/_r73b.txt /tmp/_r73c.txt /tmp/_r73d.txt \
      /tmp/_r73_x_hero34f.png /tmp/_r73_x_front.png

# --- rev 73, F296: the tail board's tilt probe.  BEHAVIOURAL, ~2 s, no build.
# The point of this probe is that it CALIBRATES on a known answer before it
# reads a photograph, so the rows below lock the CALIBRATION and the KILL --
# not the photograph's number, which is a bracket and will move if the window
# is ever re-cut.
python3 probe_rev73_tailboard.py >/tmp/_r73e.txt 2>&1
ck "F296 tailboard probe calibrates on the mesh's own angle before reading a photograph" 1 \
   "$(grep -c 'PASS T1 the SILHOUETTE detector recovers' /tmp/_r73e.txt)"
ck "F296 ... and its gradient detector's bias is MEASURED, not assumed zero" 1 \
   "$(grep -c 'PASS T2 the GRADIENT detector recovers' /tmp/_r73e.txt)"
ck "F296 ... and the 7-degree ROTATION KILL fires (a detector that cannot move is not measuring)" 1 \
   "$(grep -c 'PASS T3 KILL -- rotating the SAME frame' /tmp/_r73e.txt)"
# *** rev 73, F300 -- THIS ROW USED TO LOCK A CONCLUSION THAT IS NOW RETRACTED.
# It read: "F296 ... and the shipped TB_TILT_DEG is NOT EXCLUDED by the
# photograph", keyed on `PASS T4`.  A second rule-17 adversary showed that
# bracket WAS the detector's own 8-degree minimum-peak-separation constant --
# 38.0 falls inside at that one value and outside at sep 2, 4, 6, 10 and 12 --
# so the row was locking an artefact.  IT IS REPLACED, NOT DELETED, BY THE ROW
# THAT LOCKS THE REFUTATION: T4 now SWEEPS the constant and must FAIL, and if
# some future edit makes it pass again that is a finding about that edit.
ck "F300 the tailboard probe SWEEPS its own peak-separation constant and REFUSES (rule 39)" 1 \
   "$(grep -c 'FAIL T4 the photograph.s BRACKET survives a sweep' /tmp/_r73e.txt)"
ck "F300 ... and its rotation KILL is a LADDER that reports a GAIN, not one rung" 1 \
   "$(grep -c 'MEAN GAIN' /tmp/_r73e.txt)"
# ⚠ THE ROW BELOW IS A SOURCE-TEXT CHECK, NOT A BEHAVIOURAL ONE, AND IT IS
# NAMED THAT WAY ON PURPOSE (rule 50).  The behaviour it is about -- refusing
# when out/ holds no side render -- cannot be exercised here without moving
# out/ aside, which a verifier must not do.  It can tell you the refusal path
# is still WRITTEN; it cannot tell you it still FIRES.
ck "F296 ... and its no-side-render refusal path is still PRESENT IN SOURCE (a grep, not a behaviour)" 1 \
   "$(python3 -c "
import re,io
s=io.open('probe_rev73_tailboard.py').read()
print(1 if ('NO SIDE RENDER' in s and '2 ABSENT' in s) else 0)")"
rm -f /tmp/_r73e.txt

# --- rev 73, F301: THE FREE-ENDPOINT SPINE SHIPS.  Behavioural, ~3 s, no build.
# It is a GEOMETRY change to the vehicle, so it gets the same treatment rev 72's
# fixes got: rows that RUN the thing and read what it does, each watched failing
# against the real pre-change code.
python3 probe_rev46_vw.py >/tmp/_r73f.txt 2>&1
T1_VW_FREE=0 python3 probe_rev46_vw.py >/tmp/_r73g.txt 2>&1
ck "F301 the free-endpoint spine is what SHIPS (t1_core.vw_free defaults ON)" 1 \
   "$(python3 -c "import t1_core as C; print(1 if C.vw_free() else 0)")"
ck "F301 ... and T1_VW_FREE=0 really ablates it back to the on-band spine" 1 \
   "$(python3 -c "
import os; os.environ['T1_VW_FREE']='0'
import t1_core as C; print(0 if C.vw_free() else 1)")"
# THE MEASUREMENT, not the switch: L6 is stroke width / ring width at the SAME
# row, so the viewing angle cancels.  The shipped build must sit on the
# photograph's 0.1528, and the ablated one must NOT -- if both matched, the
# weight would not be following the spine and F301's whole argument would be void.
ck "F301 the shipped glyph's L6 sits on the photograph's 0.1528 (0.1532)" 1 \
   "$(grep -cE '^ *built .*L6 0\.153' /tmp/_r73f.txt)"
ck "F301 ... and the ABLATED glyph's does not (0.1579) -- the weight follows the spine" 1 \
   "$(grep -cE '^ *built .*L6 0\.1579' /tmp/_r73g.txt)"
# C12 was RIGHT to go red when the free spine shipped: it was perturbing a
# constant the build no longer reads.  Lock the repair, not the bar.
ck "F301 C12 perturbs the constant the LIVE construction uses, and names it" 1 \
   "$(grep -c 'VW_FREE_W_ARM_X .* moves .* of .* outline radii' /tmp/_r73f.txt)"
ck "F301 ... and names the OTHER one when ablated" 1 \
   "$(grep -cE '^ +VW_W_ARM_X .* moves .* of .* outline radii' /tmp/_r73g.txt)"
# *** rev 73 -- RE-BASED 1 FAILED -> 2, CAUSE NAMED (F304).  C10 was found to
# compare a raster with ITSELF -- built_mask caps at NPX = 552, so 552 and 1104
# rows return the same array and its "worst move 0.0000" was arithmetic
# identity (rule 6).  It now detects the cap and REFUSES, so both constructions
# read C4 and C10.  A false pass became a true finding; the bar was not moved.
ck "F301 ... and both paths still read 12 checked, 2 FAILED (C4 + C10)" 2 \
   "$(cat /tmp/_r73f.txt /tmp/_r73g.txt | grep -c 'CONTROLS: 12 checked, 2 FAILED -- C4,C10')"
ck "F304 ... and C10's refusal names the CAP rather than reporting convergence" 2 \
   "$(cat /tmp/_r73f.txt /tmp/_r73g.txt | grep -c 'VACUOUS: built_mask CAPS AT NPX')"
# The proxy must track the build in BOTH constructions.  The live case already
# has a row above; this one covers the ablated path, because a proxy hard-coded
# to whichever spine happens to ship would pass that row and be void here.
ck "F301 the emblem proxy reproduces the build under the ABLATION too" 1 \
   "$(T1_VW_FREE=0 python3 probe_rev71_proxy.py 2>&1 | grep -c 'IoU 1.000000')"
# AND THE ABLATION IS EXACT, NOT MERELY SELF-CONSISTENT.  Rev 73 checked out the
# REAL pre-change t1_core/t1_detail/proxy at HEAD~7 and read on-px 41701; the
# ablated path reads 41701 too, so "T1_VW_FREE=0 restores the rev-72 spine
# exactly" is a measurement, not a claim.  Pinning the count is what stops the
# on-band path drifting once nothing ships on it.  (The free path reads 41474 --
# a DIFFERENT number, which is how we know the switch is not a no-op.)
ck "F301 ... and the ablated glyph is the rev-72 glyph to the PIXEL (41701 on-px)" 1 \
   "$(T1_VW_FREE=0 python3 probe_rev71_proxy.py 2>&1 | grep -c 'on-px 41701 / 41701')"
ck "F301 ... while the SHIPPED glyph is a different one (41474) -- the switch is no no-op" 1 \
   "$(python3 probe_rev71_proxy.py 2>&1 | grep -c 'on-px 41474 / 41474')"
rm -f /tmp/_r73f.txt /tmp/_r73g.txt

# --- rev 74, F308/F319: THE TYRE'S TRANSVERSE TREAD.  BEHAVIOURAL, ~2 s each.
# ⚠ THESE ROWS ARE DELIBERATELY FRAME-INDEPENDENT.  probe_rev74_tread's T6
# reads a *_side.png and SKIPS when out/ is empty, so its CHECKED count is 7 or
# 8 depending on whether the render has run.  Pinning "8 checked" would recreate
# F311 exactly -- five rows that hard-fail on a clean clone and stop the next
# context's pickup.  The FAILED count is 0 either way, and the named rows below
# do not depend on a frame.
python3 probe_rev74_tread.py >/tmp/_r74a.txt 2>&1
T1_TYRE_TREAD=0 python3 probe_rev74_tread.py >/tmp/_r74b.txt 2>&1
ck "F308 the tread probe passes every row it can run (frame or no frame)" 1 \
   "$(grep -cE '^  [0-9]+ checked, 0 FAILED' /tmp/_r74a.txt)"
# The headline: the built tyre is NOT a surface of revolution.  This is the
# thing that shipped, and it is read off the MESH, not off a name (rule 50).
ck "F308 the built tyre is NOT a surface of revolution" 1 \
   "$(grep -c '\[PASS\] T3   the built tyre is NOT a surface of revolution' /tmp/_r74a.txt)"
# THE KILL, and it is the row that stops the tread being silently deleted:
# with the ablation on, T3 must go RED.  A guard that only checks the built
# case would stay green if _cut_tread were removed.
ck "F308 ... and T1_TYRE_TREAD=0 drives T3 RED -- the ablation is WATCHED" 1 \
   "$(grep -c '\[FAIL\] T3' /tmp/_r74b.txt)"
# rev 74 shipped an IRREGULAR tread first: 99 of 384 equator vertices cut in
# runs of 1 AND 2, because the phase threshold left the LEADING edge on the
# modulo wrap with zero margin (F319, found by a rule-17 adversary).  This row
# locks the repair, and it locks it on the MESH's own count.
ck "F319 the tread is REGULAR -- 128 of 384 cut, every groove run one width" 1 \
   "$(grep -c '\[PASS\] T7   THE TREAD IS REGULAR: 128 of 384' /tmp/_r74a.txt)"
# AND THE QUANTITY verify.py ACTUALLY LOCKS.  T5 used to compare max RADIUS
# while claiming to protect TYRE_D, which is max(z)-min(z) -- rule 38.  Both
# are read now, and this row holds the distinction rather than the figure.
ck "F319 ... and T5b reads TYRE_D as the BBOX EXTENT verify.py locks, not a radius" 1 \
   "$(grep -c '\[PASS\] T5b  AND THE QUANTITY verify.py ACTUALLY LOCKS' /tmp/_r74a.txt)"
rm -f /tmp/_r74a.txt /tmp/_r74b.txt

ck "newest brief states THIS script's row count" "$((PASS+1))" "${_BRIEF_TOTAL:-0}"

UNTRACKED="$(git status --porcelain 2>/dev/null | grep -c '^??')"
if [ "${UNTRACKED:-0}" -gt 0 ]; then
  say
  say "  note: $UNTRACKED untracked file(s) present -- not a failure, but say so"
  say "        in the handoff if you did not create them."
fi

# --------------------------------------------------------------------- verdict
say
say "=============================================================="
if [ $FAIL -eq 0 ]; then
  printf '  ALL %d PASS -- %d FIDELITY, %d SELF-CONSISTENCY.\n' \
         "$PASS" "$FID" "$((PASS-FID))"
  if [ "$FID" -eq 0 ]; then
    printf '  NO ROW IN THIS SCRIPT MEASURES THE VEHICLE AGAINST A PHOTOGRAPH.\n'
    printf '  It checks that the RECORD is internally consistent, which is what it\n'
    printf '  is for.  Every defect this project has shipped -- the lid that opened\n'
    printf '  INWARDS, the board 120 mm inside the roof, the bay lining 17.5 mm low,\n'
    printf '  the 33 mm disc of body red in every tail lamp, the five-petal hubcaps --\n'
    printf '  passed this script and was found by LOOKING at a crop.  Do not quote\n'
    printf '  this line as evidence about the bus.\n'
  fi
  say "=============================================================="
  say
  exit 0
else
  printf '  %d PASSED, %d FAILED.\n' "$PASS" "$FAIL"
  printf '%b\n' "$FAILED_LINES"
  echo
  echo "  STOP.  Do not build on a tree that does not verify."
  echo "  A failing line is a FINDING -- report it with its actual value."
  echo "  Do NOT edit this script to make it pass."
  echo "=============================================================="
  echo
  exit 1
fi
