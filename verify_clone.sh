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
# (it also drops Metallic).  IT IS NOT THE DEFAULT: its positive control
# FAILED -- GAPW/2 is 0.75 px at 271.2 px/m, so the edge band is sub-pixel and
# the chips are REMOVED rather than moved to the edges, and SPEC sec.3 locks
# the finish WEATHERED.  These rows hold that BOTH paths and the derivation
# survive; only rendering can say which is right.
ck "chip gate: Pointiness still DEFAULT" 1 "$(grep -cE 'pw = _mr\(nt, PT, W_PT_LO' t1_mats.py)"
ck "T1_EDGEBEVEL lever exists"           2 "$(grep -c 'T1_EDGEBEVEL' t1_mats.py)"
ck "edge window DERIVED from a 90 deg fold" 2 "$(grep -c 'W_EDGE_90' t1_mats.py)"
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
# rev 47, SPEC 10.121: RE-BASED because the texture legitimately changed.  The
# generator no longer LANCZOS-magnifies the 271-px mask-space crop 15.11x to
# OUT_W; it crops and resizes the raster Canvas actually drew, 3252 px -> 4096,
# a 1.260x resize.  The 10-90 alpha edge width over the mean stroke width went
# 0.0924 -> 0.0062.  MASK SPACE IS BIT-IDENTICAL ACROSS THIS CHANGE -- build()
# and senor_only() hash 4a6f4e8cd0489fa1 / 82d6cf56dd660b47 before and after --
# so every mask-space figure in this project still holds.  Only the emitted
# texture moved, and this row is re-based, never relaxed.
ck "tex/senor.png"   92ff38554d61947528904e113cf657f0 "$(md5of tex/senor.png)"
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
ck "tex/calidad.png" ffefd297a529adc9f2b0a319107429b1 "$(md5of tex/calidad.png)"
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
ck "tex/lidmural.png" 39f523a3127c0fdc72aec6bd567e1c85 "$(md5of tex/lidmural.png)"
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
ck "mesh objects 223"               1 "$(grep -c '| mesh objects | 223 |' STATE.md)"
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
