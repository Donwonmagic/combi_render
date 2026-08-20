#!/usr/bin/env bash
# =============================================================================
#  bootstrap.sh -- rev 45.  ONE COMMAND FROM A FRESH CLONE TO A PROVEN TREE.
#
#  WHY THIS FILE EXISTS.  Every context that has picked this project up has
#  spent its first twenty minutes doing the same four things by hand, from a
#  recipe that lives in prose in START_HERE.md and has drifted twice:
#
#      1  discover that Blender is not installed and cannot be downloaded
#      2  pip install bpy
#      3  hand-build two shims at paths that eight files hard-code
#      4  discover that ./verify_clone.sh fails on a shallow clone
#
#  A recipe in a paragraph goes stale silently.  A recipe that runs cannot.
#  This is the same argument verify_clone.sh makes about itself, applied one
#  layer down -- verify_clone.sh proves the TREE, this proves the TOOLCHAIN
#  the tree needs, and then runs verify_clone.sh.
#
#  USAGE
#      ./bootstrap.sh              # toolchain + verify_clone.sh
#      ./bootstrap.sh --guards     # ... and both builds and the probes (~6 min)
#      ./bootstrap.sh --quiet      # verdict lines only
#
#  EXIT  0 = ready to work.  1 = something is wrong; DO NOT BUILD ON 1.
#
#  IT IS IDEMPOTENT.  Run it as often as you like; it reinstalls nothing that
#  is already correct, and it re-checks everything every time.
#
#  WHAT IS PROVEN AND WHAT IS NOT, STATED SO NOBODY ASSUMES THE REST.
#    PROVEN at rev 45:  `rm -rf /tmp/blender && ./bootstrap.sh` rebuilds both
#                       shims from nothing and returns ALL 10 PASS.  The argv
#                       control, the exec-not-symlink check, the clone-depth
#                       and stranded-branch rows all ran.
#    NOT EXERCISED:     the `pip install bpy==4.5.3` branch.  bpy was already
#                       installed in the container this was written in, so that
#                       arm has never executed here.  It is the one line most
#                       likely to behave differently on a fresh machine -- if it
#                       fails, the row it fails on is "bpy installed", and the
#                       fallback is START_HERE.md's venv recipe.
#
#  WHAT IT WILL NOT DO.  It will not edit any of the eight files that hard-code
#  /tmp/blender.  That constraint has held since rev 43 and it holds here.
# =============================================================================
set -uo pipefail
cd "$(dirname "$0")" || exit 1

QUIET=0; GUARDS=0
for a in "$@"; do
  case "$a" in
    --quiet)  QUIET=1 ;;
    --guards) GUARDS=1 ;;
    *) echo "bootstrap.sh: unknown option $a" >&2; exit 1 ;;
  esac
done

PASS=0; FAIL=0; FAILED_LINES=""
say () { [ $QUIET -eq 1 ] || printf '%s\n' "$*"; }
ck () {  # ck <label> <ok|message>
  local label="$1" got="$2"
  if [ "$got" = "ok" ]; then
    PASS=$((PASS+1)); [ $QUIET -eq 1 ] || printf '  ok    %-54s\n' "$label"
  else
    FAIL=$((FAIL+1)); FAILED_LINES="$FAILED_LINES\n    $label -- $got"
    printf '  FAIL  %-54s %s\n' "$label" "$got"
  fi
}

say "=============================================================="
say "  bootstrap.sh -- toolchain, then tree"
say "=============================================================="

# --------------------------------------------------------------- 1  interpreter
# bpy 4.5.3 is built for CPython 3.11 ONLY.  3.12 will resolve the pip install
# to a different bpy or fail outright, and the failure surfaces much later as an
# import error inside a build, so it is checked first and by version.
PY=""
for c in python3.11 /usr/bin/python3.11 python3; do
  if command -v "$c" >/dev/null 2>&1; then
    v="$("$c" -c 'import sys;print("%d.%d"%sys.version_info[:2])' 2>/dev/null)"
    [ "$v" = "3.11" ] && { PY="$(command -v "$c")"; break; }
  fi
done
if [ -n "$PY" ]; then ck "CPython 3.11 present ($PY)" ok
else ck "CPython 3.11 present" "NOT FOUND -- bpy 4.5.3 is 3.11-only"; fi

# --------------------------------------------------------------- 2  bpy
# download.blender.org returns 403 through this environment's proxy -- re-tested
# at rev 45, still 403, for both the tarball and the .dmg.  PyPI is the route.
if [ -n "$PY" ]; then
  if "$PY" -c 'import bpy' >/dev/null 2>&1; then
    BPYV="$("$PY" -c 'import bpy;print(bpy.app.version_string)' 2>/dev/null)"
    ck "bpy importable ($BPYV)" ok
  else
    say "  ..    installing bpy==4.5.3 (a few minutes, ~1 GB)"
    "$PY" -m pip install --quiet bpy==4.5.3 >/dev/null 2>&1
    if "$PY" -c 'import bpy' >/dev/null 2>&1
      then ck "bpy installed" ok
      else ck "bpy installed" "pip install bpy==4.5.3 FAILED"; fi
  fi
  for m in numpy PIL scipy; do
    "$PY" -c "import $m" >/dev/null 2>&1 || "$PY" -m pip install --quiet \
      "$( [ "$m" = PIL ] && echo pillow || echo "$m" )" >/dev/null 2>&1
  done
  MISS=""
  for m in numpy PIL scipy; do
    "$PY" -c "import $m" >/dev/null 2>&1 || MISS="$MISS $m"
  done
  [ -z "$MISS" ] && ck "numpy, pillow, scipy" ok || ck "numpy, pillow, scipy" "missing:$MISS"
fi

# --------------------------------------------------------------- 3  the shims
# EIGHT .py/.sh files hard-code these two paths.  Not one of them may be edited
# -- that constraint has held since rev 43.  So the paths are reproduced.
mkdir -p /tmp/blender/4.5/python/bin

if [ ! -x /tmp/blender/blender ] || ! grep -q 'BOOTSTRAP_SHIM_V1' /tmp/blender/blender 2>/dev/null; then
cat > /tmp/blender/blender <<SHIM
#!$PY
# BOOTSTRAP_SHIM_V1 -- written by bootstrap.sh.  Parses the subset of Blender's
# CLI this repo uses: -b [-P|--python] FILE [-- args].
#
# IT MUST LEAVE THE FULL COMMAND LINE IN sys.argv.  The repo uses the
# sys.argv[sys.argv.index("--")+1:] idiom in several probes; a shim that
# rewrites argv to just the script path makes those read the wrong slice.
import sys, runpy
argv = sys.argv[1:]
script = None
i = 0
while i < len(argv):
    if argv[i] == '--':
        break
    if argv[i] in ('-P', '--python'):
        i += 1
        script = argv[i] if i < len(argv) else None
    i += 1
if script is None:
    import bpy
    print("Blender", bpy.app.version_string)
    sys.exit(0)
import bpy  # noqa: F401  -- loads the embedded Blender before the script runs
sys.argv = ['/tmp/blender/blender'] + argv
runpy.run_path(script, run_name="__main__")
SHIM
chmod +x /tmp/blender/blender
fi

# THE INTERPRETER SHIM MUST exec, NOT BE A SYMLINK.  If bpy lives in a venv,
# venv resolution keys off sys.executable's own directory to find pyvenv.cfg,
# and a symlink from /tmp lands outside the venv and imports nothing.  That
# cost rev 43 a cycle.  exec is correct for a system install too, so it is
# always written this way.
cat > /tmp/blender/4.5/python/bin/python3.11 <<SHIM
#!/bin/sh
# BOOTSTRAP_SHIM_V1 -- written by bootstrap.sh.  MUST exec, never a symlink.
exec $PY "\$@"
SHIM
chmod +x /tmp/blender/4.5/python/bin/python3.11

if [ -L /tmp/blender/4.5/python/bin/python3.11 ]; then
  ck "interpreter shim execs (not a symlink)" "IT IS A SYMLINK -- see rev 43"
else
  ck "interpreter shim execs (not a symlink)" ok
fi

V="$(/tmp/blender/blender --version 2>/dev/null | head -1)"
case "$V" in
  Blender*) ck "CLI shim: $V" ok ;;
  *)        ck "CLI shim runs" "got '${V:-<empty>}'" ;;
esac
if /tmp/blender/4.5/python/bin/python3.11 -c 'import bpy,numpy,PIL' >/dev/null 2>&1
  then ck "interpreter shim imports bpy, numpy, PIL" ok
  else ck "interpreter shim imports bpy, numpy, PIL" "import failed"; fi

# A POSITIVE CONTROL ON THE ARGV IDIOM ITSELF.  Several probes are plain-Python
# and read sys.argv[sys.argv.index("--")+1:].  A shim that passes this test
# cannot silently feed them '-b'.  Without it, "the shim works" is untested.
T=$(mktemp /tmp/bootstrap_argv_XXXX.py)
cat > "$T" <<'PROBE'
import sys
print("ARGV_TAIL:" + ",".join(sys.argv[sys.argv.index("--") + 1:]))
PROBE
OUT="$(/tmp/blender/blender -b -P "$T" -- alpha beta 2>/dev/null | grep ARGV_TAIL)"
rm -f "$T"
[ "$OUT" = "ARGV_TAIL:alpha,beta" ] \
  && ck "argv tail idiom survives the shim" ok \
  || ck "argv tail idiom survives the shim" "got '${OUT:-<empty>}' want 'ARGV_TAIL:alpha,beta'"

# --------------------------------------------------------------- 4  the clone
# verify_clone.sh's `commits >= 227` row fails on a shallow clone, and the
# failure reads like a content defect.  Deepen first, then let it speak.
if [ "$(git rev-parse --is-shallow-repository 2>/dev/null)" = "true" ]; then
  say "  ..    shallow clone -- git fetch --unshallow"
  git fetch --unshallow >/dev/null 2>&1
fi
NC="$(git rev-list --count HEAD 2>/dev/null)"
[ "${NC:-0}" -ge 227 ] && ck "clone depth ($NC commits)" ok \
                       || ck "clone depth" "only $NC commits; git fetch --unshallow"

# THE RULE FROM SPEC 10.113.5, ENFORCED RATHER THAN WRITTEN DOWN.
# Seventeen commits of rev-44/44b work sat on a branch and never reached the
# mainline; the rev-45 brief was written from a tree that had them and handed
# to a context that did not.  This is eleven characters and it would have saved
# that revision an entire investigation.
git fetch --all --quiet >/dev/null 2>&1
STRANDED=""
for b in $(git branch -r --format='%(refname:short)' 2>/dev/null | grep -v HEAD); do
  n="$(git rev-list --count HEAD.."$b" 2>/dev/null)"
  [ "${n:-0}" -gt 0 ] && STRANDED="$STRANDED $b($n)"
done
[ -z "$STRANDED" ] && ck "no branch carries work HEAD does not have" ok \
  || ck "no branch carries work HEAD does not have" "STRANDED:$STRANDED -- SPEC 10.113.5"

# --------------------------------------------------------------- 5  the tree
if [ -x ./verify_clone.sh ]; then
  if ./verify_clone.sh --quiet >/dev/null 2>&1
    then ck "verify_clone.sh" ok
    else ck "verify_clone.sh" "FAILED -- run ./verify_clone.sh and read the rows"; fi
else
  ck "verify_clone.sh present and executable" "missing"
fi

# --------------------------------------------------------------- 6  the guards
if [ $GUARDS -eq 1 ]; then
  say ""
  say "-- guards (this takes about six minutes) --"
  for S in 1 2; do
    R="$(T1_SUB=$S T1_VERIFY=1 /tmp/blender/blender -b -P build.py 2>&1 | grep -c 'VERIFY: 0 fail, 0 warn')"
    [ "$R" = "1" ] && ck "T1_SUB=$S  VERIFY 0 fail 0 warn" ok \
                   || ck "T1_SUB=$S  VERIFY 0 fail 0 warn" "did not print it"
  done
  # rev 45: 7 -> 8.  RE-BASED, and the reason is that this row caught its own
  # author.  bootstrap.sh was written expecting 7 controls; SPEC 10.115 then
  # added C8 to probe_rev45_nose and the expectation was not updated, so the
  # first --guards run after that reported a FAIL that was entirely mine.  It
  # is rev 13's rule -- never put a figure in an acceptance test unless you
  # watched it print -- caught by the acceptance test itself, one turn later.
  # The count is kept rather than loosened to "0 FAILED": a control silently
  # disappearing is exactly what this row is for.
  R="$(/tmp/blender/blender -b -P probe_rev45_nose.py 2>&1 | grep 'CONTROLS:' | tail -1)"
  [ "$R" = "CONTROLS: 8 checked, 0 FAILED" ] \
    && ck "probe_rev45_nose  8/0" ok || ck "probe_rev45_nose  8/0" "got '$R'"
  R="$(/tmp/blender/blender -b -P probe_rev45_ground.py 2>&1 | grep 'CONTROLS:' | tail -1)"
  [ "$R" = "CONTROLS: 4 checked, 0 FAILED" ] \
    && ck "probe_rev45_ground  4/0" ok || ck "probe_rev45_ground  4/0" "got '$R'"
  R="$(/tmp/blender/blender -b -P probe_rev45_paint.py 2>&1 | grep 'CONTROLS:' | tail -1)"
  [ "$R" = "CONTROLS: 4 checked, 0 FAILED" ] \
    && ck "probe_rev45_paint  4/0" ok || ck "probe_rev45_paint  4/0" "got '$R'"
  R="$(/tmp/blender/blender -b -P probe_rev44_lampmove.py 2>&1 | grep 'CONTROLS:' | tail -1)"
  [ "$R" = "CONTROLS: 6 checked, 0 FAILED" ] \
    && ck "probe_rev44_lampmove  6/0" ok || ck "probe_rev44_lampmove  6/0" "got '$R'"
fi

# --------------------------------------------------------------- verdict
say ""
say "=============================================================="
if [ $FAIL -eq 0 ]; then
  printf '  ALL %d PASS.  Toolchain reproduced, tree verified.\n' "$PASS"
  [ $GUARDS -eq 1 ] || say "  (add --guards to run the builds and probes too)"
  say "=============================================================="
  exit 0
else
  printf '  %d PASSED, %d FAILED.\n' "$PASS" "$FAIL"
  printf '%b\n' "$FAILED_LINES"
  say ""
  say "  STOP.  Do not build on a toolchain that does not bootstrap."
  say "  A failing line is a FINDING -- report it with its actual value."
  say "=============================================================="
  exit 1
fi
