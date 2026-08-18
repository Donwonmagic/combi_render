#!/usr/bin/env bash
# =============================================================================
#  verify_clone.sh -- prove this working tree is the rev-42 state, BY CONTENT.
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
ck "annotated derivatives (.png)"   5 "$(ls ref_*.png 2>/dev/null | wc -l)"

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
ck "0.024426 (DOOR_ARCH_G)"         2 "$(grep -c '0.024426' SPEC.md)"
ck "COMMON-MODE (case matters)"     3 "$(grep -c 'COMMON-MODE' SPEC.md)"
PAT_CFF="THE COUNTER'S FRONT FACE"   # apostrophe: keep it in a variable
ck "THE COUNTER'S FRONT FACE"       3 "$(grep -c "$PAT_CFF" SPEC.md)"
ck "CLOSED BY HIM (case matters)"   3 "$(grep -c 'CLOSED BY HIM' SPEC.md)"
ck "CNT_NOSE_F"                     6 "$(grep -c 'CNT_NOSE_F' SPEC.md)"
ck "cab_floor"                      4 "$(grep -c 'cab_floor' SPEC.md)"
ck "amtrak (HIS word)"              2 "$(grep -c 'amtrak' SPEC.md)"
ck "nolita, any case"               9 "$(grep -ic 'nolita' SPEC.md)"
ck "TEN flower heads"               1 "$(grep -c 'TEN flower heads' SPEC.md)"

# ------------------------------------------------------------------ build files
say "-- build files --"
ck "DOOR_ARCH_G in t1_shell.py"     7 "$(grep -c 'DOOR_ARCH_G' t1_shell.py)"
ck "_G_BUILD in t1_shell.py"        4 "$(grep -c '_G_BUILD' t1_shell.py)"
ck "_arch_radial in t1_shell.py"    4 "$(grep -c '_arch_radial' t1_shell.py)"
ck "T1_ABLATE in build.py"          5 "$(grep -c 'T1_ABLATE' build.py)"
ck "FLOOR_W in t1_detail.py"        5 "$(grep -c 'FLOOR_W' t1_detail.py)"
ck "_assert_same_edge"              4 "$(grep -c '_assert_same_edge' flank_compare.py)"
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
ck "tex/swirl.png"   4ee4e09edcc9afb46303c8d3858a62bf "$(md5of tex/swirl.png)"
ck "tex/swirl_b.png" d201597e1c867b6e1fbedd2c0f8ab306 "$(md5of tex/swirl_b.png)"
ck "tex/nose.png"    b31ea156c15d2d8e38ba390d9e151706 "$(md5of tex/nose.png)"
ck "tex/senor.png"   8e58ad7e9d87184591fe7cb12300e903 "$(md5of tex/senor.png)"
ck "tex/calidad.png" cc1c46c796e88e6b066d4fb2cb5cc9c2 "$(md5of tex/calidad.png)"
ck "tex/lidmural.png" 2d62159dba663c90b5ae3746383c15d1 "$(md5of tex/lidmural.png)"
ck "tex/lidsign.png" bcd3da2dbec0276fabd7d8f8ee03f27b "$(md5of tex/lidsign.png)"
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
ck "V_POW is 0.60"                  1 "$(grep -c '^V_POW = 0.60' t1_mats.py)"
ck "V_POW_Z is 0.60"                1 "$(grep -c '^V_POW_Z = 0.60' t1_shell.py)"
ck "V_POW and V_POW_Z agree"       yes "$(if [ \"$(grep -o '^V_POW = [0-9.]*' t1_mats.py | awk '{print $3}')\" = \"$(grep -o '^V_POW_Z = [0-9.]*' t1_shell.py | awk '{print $3}')\" ]; then echo yes; else echo NO; fi)"
ck "DOOR_H art datum is 1.013467"   1 "$(grep -c '1.013467 m' folk_gen.py)"
# POLARITY, not presence.  The signboard is RETIRED from the vehicle; flipping
# the default to "1" leaves the occurrence count at 3 and puts a panel he
# removed into every hero.
ck "signboard default is OFF"       1 "$(grep -c 'T1_SIGNBOARD\", \"0\"' t1_shell.py)"

# ---------------------------------------------------------------------------
# THE GUARD TABLE, EXECUTABLE.
# These eight rows lived as prose in the brief -- a second copy of numbers
# STATE.md already owns, free to drift.  They are read from STATE.md now.
# STATE.md is machine-written by audit.py, so this checks the RECORD, not a
# retyping of it.  (It does not run the guards; run those yourself.)
# ---------------------------------------------------------------------------
say "-- guard figures, read from the machine-written STATE.md --"
ck "roof @ rear axle 1.9835"        1 "$(grep -c 'roof@rear-axle=1.9835' STATE.md)"
ck "rake 17.75 mm/m"                1 "$(grep -c 'rake 17.75 mm/m (locked 17.75)' STATE.md)"
ck "L=4.065 W=1.750"                1 "$(grep -c 'L=4.065 W=1.750' STATE.md)"
ck "bay widths 0.516 0.515 0.516"   2 "$(grep -c 'bay widths 0.516 0.515 0.516' STATE.md)"
ck "mesh objects 190"               1 "$(grep -c '| mesh objects | 190 |' STATE.md)"
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
ck "heroes are NOT tracked"         0 "$(git ls-files 2>/dev/null | grep -c 'hero.*\.png')"
ck "out/ is NOT tracked"            0 "$(git ls-files 2>/dev/null | grep -c '^out/')"

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
  printf '  ALL %d PASS.  This tree is the rev-42 state.\n' "$PASS"
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
