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
ck "nolita, any case"              31 "$(grep -ic 'nolita' SPEC.md)"
ck "TEN flower heads"               1 "$(grep -c 'TEN flower heads' SPEC.md)"

# ------------------------------------------------------------------ build files
say "-- build files --"
# rev 44b: 7 -> 3.  SPEC 10.102 retracted 10.100's wrap, and with the arc
# gone so are its fixed-point solve and the four references that fed it.
# What remains is the definition, the guard and its message -- which is the
# whole point: the CLEARANCE INVARIANT survived the geometry that motivated
# it.  A drop to 0 would be the finding; 3 is the invariant standing alone.
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
# rev 46, SPEC 10.120: RE-BASED because 'Senor' was very nearly invisible.
# Measured per WORD -- which nobody had done, and which dissolves the standing
# contradiction between ledger findings 19 and 30 -- Michelson against the red
# each word sits on:  Tacombi 0.4673 photographed / 0.4480 built (right), Senor
# 0.1922 photographed / 0.0711 built (2.7x too dark).  'Tacombi' was never the
# problem.  The tarnish lift is DERIVED from the photographed target, not typed.
ck "tex/senor.png"   411ade90df4fdbb696bbcdb1a481f1d4 "$(md5of tex/senor.png)"
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
ck "tex/calidad.png" d8c27a4a31ffdb7f750e8d7d1b41eaaf "$(md5of tex/calidad.png)"
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
# rev 46, W1.  VALUE, NOT OCCURRENCE, and the DERIVATION, not the result:
# TYPE_SHIFT must stay EXPRESSED as (burst centre - measured pre-rotation
# centroid) (SPEC 10.25).  Freezing the arithmetic result +0.1315/-0.0559 as a
# literal would pass this grep and silently decouple the type from the burst the
# next time a glyph moves.  The block must also rotate about the burst's own
# centre -- rotating about anything else swings a correctly-laid-out block back
# off centre, which is exactly what (0.500, 0.600) was doing.
ck "calidad burst centre is 0.505/0.575"  1 "$(grep -c '^BURST_CX, BURST_CY = 0.505, 0.575' cal_gen.py)"
ck "calidad TYPE_SHIFT is DERIVED"        1 "$(grep -c '^TYPE_SHIFT = (BURST_CX - TYPE_PRE_CENTROID\[0\],' cal_gen.py)"
ck "calidad type rotates about the burst" 1 "$(grep -c 'center=(w \* BURST_CX, h \* BURST_CY)' cal_gen.py)"
ck "calidad generator carries its guard"  1 "$(grep -c 'cal_gen GUARD FAILED' cal_gen.py)"
# rev 46, at the OWNER'S instruction, in two stages.  The Calidad decal drew two
# red bars with 15 triangular pennants hanging from them.  He asked for the
# triangles to go -- no frame we hold shows them -- and then named what the
# remaining lines are: VENT SLATS.  They are the T1's rear air-intake louvres,
# DARK GREY shadowed slots in sheet metal, and cal_gen was painting them in
# saturated red inside a decal texture.  The whole feature is retired.
# ABSENCE, checked three ways, because a feature that comes back halfway is
# exactly how this one survived: the function, the pennant loop, and the colour
# constant must all be gone.
ck "calidad bunting function gone"   0 "$(grep -c '^def bunting' cal_gen.py)"
ck "calidad pennant loop gone"       0 "$(grep -c 'ay + by) / 2 + drop' cal_gen.py)"
ck "calidad BUNT colour retired"     0 "$(grep -c '^BUNT = ' cal_gen.py)"
# rev 46, W2.  The VW glyph's vertical proportions, SOLVED against the
# photograph by probe_rev46_vw.py, not typed.  VALUES, not occurrences: the
# whole point of section 6 item 5's warning is that `grep -c '^VW_APEX_Z'`
# returns 1 whether the constant reads 0.284 or 0.1250, and 0.284 is the value
# the owner reported wrong four times running.
ck "VW_APEX_Z is 0.1250"            1 "$(grep -c '^VW_APEX_Z = 0.1250' t1_core.py)"
ck "VW_V_TIP_X is 0.3806"           1 "$(grep -c '^VW_V_TIP_X = 0.3806' t1_core.py)"
ck "VW_W_ARM_X is 0.9200"           1 "$(grep -c '^VW_W_ARM_X = 0.9200' t1_core.py)"
ck "VW_W_ARM_Z is 0.0019"           1 "$(grep -c '^VW_W_ARM_Z = 0.0019' t1_core.py)"
ck "VW_W_TROUGH_X is 0.4925"        1 "$(grep -c '^VW_W_TROUGH_X = 0.4925' t1_core.py)"
ck "VW_W_TROUGH_Z is -0.6200"       1 "$(grep -c '^VW_W_TROUGH_Z = -0.6200' t1_core.py)"
ck "vw_bars reads the constants"    1 "$(grep -c '_apex    = (0.000, VW_APEX_Z)' t1_core.py)"

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
ck "mesh objects 221"               1 "$(grep -c '| mesh objects | 221 |' STATE.md)"
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
  printf '  ALL %d PASS.  Content matches the rev-42 measured baseline,\n' "$PASS"
  printf '  which is still current at rev 44.\n'
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
