"""audit_brief.py -- rule 17's sweep and rule 15's adversary, as ONE SCRIPT.

Rev 54, 55 and 56 each wrote this by hand, ran it, threw it away, and the next
revision re-committed the same defects.  Rev 56's own brief records the shape:
*"a bare filename beside a qualified sibling, caught only by the `stat` sweep
and passed over by re-reading every time"* -- THREE REVISIONS RUNNING.  A sweep
that is rewritten every revision is not an instrument, it is a habit, and this
project's whole method says the difference matters.  So it lives here now.

    python3 audit_brief.py [brief.md]        # default: the highest-numbered one

WHAT IT ASKS
  1. does every path the brief names RESOLVE?           (rev 54/55/56's defect)
  2. does every `T1_*` it names READ THE ENVIRONMENT,   (a switch surviving
     rather than merely appear in a comment?             only in a comment)
  3. does every script it tells you to run EXIST?
  4. is it byte-identical to PASTE_INTO_CLAUDE_CODE.txt?
  5. does it state verify_clone.sh's OWN row count?
  6. do README.md and START_HERE.md name THIS brief by number?
  7. the SELF-REFERENTIAL TRAP: a row that documents a defect by QUOTING it
     re-commits the defect.  Rev 54, 55 and 56 each hit this and each recorded
     it as a one-off; the rev-57 brief says it is STRUCTURAL.  So the sweep
     checks the traps that have actually fired here.

IT DOES NOT CHECK THAT THE NUMBERS ARE TRUE.  Only the revision that measured
them can do that, which is why the ledger exists and why rule 17 says
RECOMPUTE.  What this removes is the mechanical half, so the reading half gets
the attention.
"""
import os, re, sys, glob, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
briefs = sorted(glob.glob(os.path.join(ROOT, "NEXT_CONTEXT_PROMPT_rev*.md")),
                key=lambda p: int(re.search(r"rev(\d+)", p).group(1)))
_args = [a for a in sys.argv[1:] if not a.startswith("--")]
BRIEF = _args[0] if _args else briefs[-1]
N = int(re.search(r"rev(\d+)", os.path.basename(BRIEF)).group(1))
TXT = open(BRIEF).read()

# ------------------------------------------------------------------ rev 70
# THE HANDOFF WAS SPLIT, AND THIS SWEEP FOLLOWS THE CONTENT.
#
# The carriers moved out of the brief into HANDOFF_CARRIERS.md (the cause is
# measured in revstats.py: geometry per revision fell 721 -> 209 while the
# brief grew 12 KB -> 95 KB).  If this file kept sweeping only the brief, then
# every path, switch and script name in the carriers would silently STOP being
# audited the moment it moved -- the split would buy legibility by giving up
# coverage, which is exactly the trade this project must not make.
#
# So the path / T1_* / script sweeps below run over the UNION.  `TXT` is the
# ACTION brief alone, because the rows that are ABOUT the brief -- its own
# audit record, its row count, its size -- must stay pointed at the brief.
CARRIERS = os.path.join(ROOT, "HANDOFF_CARRIERS.md")
BOTH = TXT + ("\n" + open(CARRIERS).read() if os.path.exists(CARRIERS) else "")
if not os.path.exists(CARRIERS):
    print("  !! HANDOFF_CARRIERS.md IS MISSING -- the carriers are unaudited, and "
          "that is a FINDING, not a pass")
fails = []


_NCK = 0


def ck(label, ok, detail=""):
    # rev 60c-ii -- THE TOTAL IS COUNTED HERE, NOT TYPED AT THE BOTTOM.  It was
    # the literal `7 + 2` while this file ran ten ck rows, so it printed
    # "9 checked" and a row could be added, removed or skipped without the
    # number ever moving.  Same defect class as F129 in the sibling script,
    # and the register wrote the general rule down while this copy kept it:
    # a script that reports per-item results must make a PARTIAL RUN VISIBLE.
    global _NCK
    _NCK += 1
    print("  %-4s %-52s %s" % ("ok" if ok else "FAIL", label, detail))
    if not ok:
        fails.append(label)


print("=" * 78)
print("  audit_brief.py -- %s" % os.path.basename(BRIEF))
print("=" * 78)

# ---------------------------------------------------------------- 1. paths
# The FIRST run of this sweep failed on eleven "paths" that are not paths --
# `REAR_W/2`, `0.1986/0.814`, `origin/main`, `git`, and the TEMPLATE names
# `LEDGER_rev<N>.md` and `HANDOFF_rev*.md`.  A sweep that cries wolf on a
# quotient gets ignored, which is worse than not having one.  So a path must
# END in a known extension, and must carry no glob or placeholder.
_PATH = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_./-]*\.(py|sh|md|txt|png|jpg|jpeg|JPG|npz)$")
paths = set()
for m in re.finditer(r"`([^`\n]+)`", BOTH):
    t = m.group(1).strip().split()[0].rstrip(".,;:)")
    if any(c in t for c in "<>*?$") or t.startswith(("http", "-")):
        continue
    if _PATH.fullmatch(t):
        paths.add(t)
# EXISTING IS NOT ENOUGH -- IT MUST BE IN THE REPOSITORY.  The rev-57 sweep
# passed a tile that `.gitignore` silently excluded (`rev*_hero*.png`): the
# path resolved on the machine that wrote the brief and would NOT resolve on
# a clone, which is the only place the brief is ever read.  A sweep that
# checks the working tree instead of the repo cannot see that, and this one
# could not until it did.
_tracked = set(subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True,
                              text=True).stdout.split())
bad = sorted(p for p in paths
             if not os.path.exists(os.path.join(ROOT, p)) or p not in _tracked)
# a path may legitimately name something this revision creates in out/, which
# is untracked and starts empty -- say so rather than failing on it.
#
# rev 62 EXTENDS THIS TO delivery/, WITH THE CAUSE NAMED.  deliver.py writes the
# owner's promotional asset package there, and it is untracked for exactly the
# reason out/ is: it is ~100 MB of generated RGBA PNGs regenerated from the
# renders by one command.  A repository is not an asset store.  THE EXEMPTION IS
# BY PREFIX AND IS NOT A BLANKET PASS -- a path anywhere else in the tree still
# has to resolve, and the exempted ones are PRINTED, not silently dropped.
_GEN = ("out/", "delivery/")
outp = [p for p in bad if p.startswith(_GEN)]
bad = [p for p in bad if not p.startswith(_GEN)]
ck("every path the brief names resolves", not bad,
   "%d checked, %d unresolved%s" % (len(paths), len(bad),
                                    ("  " + " ".join(bad)) if bad else ""))
if outp:
    print("       (%d in out/ or delivery/, both untracked and both starting "
          "empty: %s)"
          % (len(outp), " ".join(outp)))

# --------------------------------------------------------- 2. T1_* switches
sw = sorted(set(re.findall(r"\bT1_[A-Z0-9_]+\b", BOTH)))
srcs = {p: open(os.path.join(ROOT, p)).read()
        for p in os.listdir(ROOT) if p.endswith((".py", ".sh"))}
# THIS MUST MATCH verify_clone.sh's OWN ROW, IDIOM FOR IDIOM.  Rev 57b
# loosened it here and not there, and the result was this tool reporting green
# while the repository's verifier failed on the same two switches -- two
# instruments disagreeing because one had been relaxed to fit new code.  The
# fix belonged in the new code.  If this ever needs loosening again, loosen
# BOTH or neither.
# *** rev 73, F293 -- WIDENED, WITH THE CAUSE NAMED, AND WIDENED IN
# verify_clone.sh IN THE SAME EDIT, WHICH IS WHAT THE PARAGRAPH ABOVE DEMANDS.
# THE CAUSE: this pattern only sees a switch read through `os.environ` or
# `os.getenv` LITERALLY.  studio.py reads several of its switches through its
# own thin wrappers -- `_envi("T1_FX", 1)` and `_envf("T1_SHADOW", 9.0)` -- so
# those switches are LIVE LEVERS that this row called dead.  Watched at rev 73:
# naming T1_FX and T1_SHADOW in the brief turned this row red on two switches
# that both work.  That is rule 50 in BOTH directions -- a regex told us a name
# was absent when the behaviour was present.
# THE COMPANION ROWS BELOW make the cause separately testable, so this widening
# cannot silently become a hole: one pins a helper-read switch as LIVE, one
# pins a fabricated switch as DEAD.
_ACCESS = r"(environ(\.get)?\[?\(?|getenv\(|_env[ifsb]?\()[\"']%s"
dead = []
for s_ in sw:
    if not any(re.search(_ACCESS % s_, t) for t in srcs.values()):
        dead.append(s_)

ck("every T1_* the brief names READS THE ENVIRONMENT", not dead,
   "%d named, %d not an env read%s" % (len(sw), len(dead),
                                       ("  " + " ".join(dead)) if dead else ""))

# F293's companion rows.  A widening that nothing tests is a hole.
_live = any(re.search(_ACCESS % "T1_SHADOW", t) for t in srcs.values())
ck("F293 a switch read ONLY through a helper wrapper counts as LIVE",
   _live, "T1_SHADOW is read as `_envf(\"T1_SHADOW\", 9.0)` in studio.py and "
          "nowhere as os.environ -- detected: %s" % _live)
_fake = any(re.search(_ACCESS % "T1_NOT_A_REAL_SWITCH", t) for t in srcs.values())
ck("F293 ... and the widened pattern still calls a fabricated switch DEAD",
   not _fake, "T1_NOT_A_REAL_SWITCH detected as live: %s (must be False)" % _fake)

# ---------------------------------------------- rev 73, F306: BOTH HALVES
# "ALL n PASS -- 0 FIDELITY, n SELF-CONSISTENCY".  The two figures are the same
# quantity and a mismatch is a transcription defect, not a measurement.
# the two halves are often split across a line break and a `#` continuation,
# which is exactly how the mismatch hid: match across it, bounded.
# ANCHOR ON `FIDELITY`, which is the token that actually joins the pair.  A
# looser window matched "ALL 25 PASS" (the --guards line) against the NEXT
# line's SELF-CONSISTENCY figure and reported a mismatch between two unrelated
# numbers -- a false red is as bad as a false green (rule 50, both directions).
_halves = re.findall(r"ALL (\d+) PASS\s*--\s*0 FIDELITY,\s*(\d+)"
                     r"[\s\S]{0,12}?SELF-CONSISTENCY", TXT)
_bad_half = [(a, b) for a, b in _halves if a != b]
ck("F306 the verifier's two verdict halves state the SAME number", not _bad_half,
   "%d verdict line(s) checked%s" % (len(_halves),
    "" if not _bad_half else "; MISMATCHED: " + ", ".join(
        "ALL %s PASS vs %s SELF-CONSISTENCY" % t for t in _bad_half)))

# ------------------------------------------- rev 73, F306: THE EXPECTED-OUTPUT
# MAP MUST MATCH WHAT THE PROBES ACTUALLY PRINT.
#
# THIS IS THE DEFECT CLASS THREE CONSECUTIVE RULE-17 ADVERSARIES KEPT FINDING,
# and it kept recurring because nothing MECHANICAL checked it: sec 4 is the map a
# next context reads as "what this should say" (rule 9), and every figure in it
# was hand-carried.  At rev 73 it said probe_rev73_tailboard reads "5 checked,
# 0 FAILED" while it read 1 FAILED, and said probe_rev69_fitpose's P2 fails
# after the ship had made it pass.  RUN THE CHEAP ONES AND COMPARE.
# Only probes that need NO frame argument are run -- a frame lives in out/,
# which starts empty, and a row that cannot run must not read as a pass.
_claims = re.findall(
    r"^python3 (\S+\.py)\s+#[^\n]*?(\d+) checked, (\d+) FAILED",
    TXT, re.M)
_probe_bad, _probe_ran = [], 0
for _sc, _wc, _wf in _claims:
    if not os.path.exists(os.path.join(ROOT, _sc)):
        continue
    try:
        _o = subprocess.run([sys.executable, _sc], cwd=ROOT,
                            capture_output=True, text=True, timeout=300).stdout
    except Exception as _e:
        _probe_bad.append("%s DID NOT RUN (%s)" % (_sc, type(_e).__name__))
        continue
    _m = re.findall(r"(\d+) checked, (\d+) FAILED", _o)
    if not _m:
        _probe_bad.append("%s printed no summary line" % _sc)
        continue
    _probe_ran += 1
    _gc, _gf = _m[-1]
    if (_gc, _gf) != (_wc, _wf):
        _probe_bad.append("%s: brief says %s checked/%s FAILED, live says "
                          "%s/%s" % (_sc, _wc, _wf, _gc, _gf))
ck("F306 every probe the brief gives an expected count for still prints it",
   not _probe_bad,
   "%d claim(s) found, %d run%s" % (len(_claims), _probe_ran,
    "" if not _probe_bad else ";  " + ";  ".join(_probe_bad)))

# ------------------------------------------------------------- 3. runnables
runs = sorted(set(re.findall(r"-P (\w+\.py)", BOTH))
              | set(re.findall(r"python3 (\w+\.py)", BOTH)))
miss = [r for r in runs if not os.path.exists(os.path.join(ROOT, r))]
ck("every script the brief says to run exists", not miss,
   "%d named%s" % (len(runs), ("  MISSING " + " ".join(miss)) if miss else ""))

# --------------------------------------------------------- 4. byte identity
pst = os.path.join(ROOT, "PASTE_INTO_CLAUDE_CODE.txt")
same = os.path.exists(pst) and open(pst, "rb").read() == open(BRIEF, "rb").read()
ck("byte-identical to PASTE_INTO_CLAUDE_CODE.txt", same,
   "compared, not remembered")

# ------------------------------------------------------------ 5. row count
try:
    tot = subprocess.run(["./verify_clone.sh"], cwd=ROOT, capture_output=True,
                         text=True, timeout=900).stdout
    # verify_clone prints "ALL n PASS" only when nothing failed; on a dirty
    # tree it prints "n PASSED, m FAILED" instead.  The FIRST run of this
    # sweep reported "script says None" for exactly that reason and looked
    # like a brief defect.  Read both forms.
    real = re.search(r"ALL (\d+) PASS", tot)
    if real is None:
        m2 = re.search(r"(\d+) PASSED, (\d+) FAILED", tot)
        real = int(m2.group(1)) + int(m2.group(2)) if m2 else None
    else:
        real = int(real.group(1))
except Exception:
    real = None
# ------------------------------------------------------------- rev 58 FIX
# THIS USED TO TAKE THE FIRST "ALL n PASS" IN THE BRIEF, AND IT CORRUPTED THE
# BRIEF IT WAS WRITTEN TO REPAIR.
#
# TWO scripts in this repository print that phrase: verify_clone.sh (ALL 258
# PASS) and bootstrap.sh (ALL 10 PASS), and the brief quotes bootstrap's FIRST.
# So `stated` read 10, and --fix-count then blind-replaced every occurrence of
# the string "ALL 10 PASS" -- rewriting all THREE of the brief's bootstrap
# references to 258 and leaving verify_clone's own count untouched.  It then
# reported the row as PASSING, because the corrupted text matched.
#
# Watched, rev 58: "--fix-count: rewrote 10 -> 258", three bootstrap lines
# wrong, verify's two still at 257, and a green row over the top of it.
#
# The count is now bound to verify_clone BY CONTEXT rather than by position,
# and the rewrite is line-targeted.  If the brief does not make the attribution
# unambiguous, this REFUSES rather than guessing -- a number this file cannot
# identify is not a number it may rewrite.
def _stated_rows(txt):
    """The row count the brief attributes to VERIFY_CLONE, and its line numbers.

    A line counts as verify_clone's if it names verify_clone, or if it is the
    SELF-CONSISTENCY sentence, which is about verify_clone by construction.
    Lines naming bootstrap are excluded explicitly."""
    hits = []
    for i, ln in enumerate(txt.splitlines()):
        m = re.search(r"ALL (\d+) PASS", ln)
        if not m:
            continue
        if "bootstrap" in ln:
            continue
        if "verify_clone" in ln or "SELF-CONSISTENCY" in ln:
            hits.append((i, int(m.group(1))))
    # The SELF-CONSISTENCY sentence carries the same number WITHOUT the
    # "ALL n PASS" wrapper, on its own line -- rev 54, 55, 56 and 57 each
    # re-committed a defect inside the very row written to explain it, and at
    # rev 58 this function left that line at 999 while fixing the two beside
    # it.  It is about verify_clone by construction, so it is collected too.
    if hits:
        _n = hits[0][1]
        for i, ln in enumerate(txt.splitlines()):
            if re.search(r"\b%d SELF-CONSISTENCY" % _n, ln) and \
               not any(i == j for j, _ in hits):
                hits.append((i, _n))
    return hits


_hits = _stated_rows(TXT)
_vals = sorted({v for _, v in _hits})
if len(_vals) == 1:
    stated = _vals[0]
elif not _vals:
    stated = None
else:
    stated = None
    print("  !! the brief states MORE THAN ONE verify_clone row count %s -- "
          "REFUSING to rewrite any of them" % _vals)
# THE ROW COUNT IS SELF-REFERENTIAL AND IT HAS COST THREE EDIT CYCLES IN EACH
# OF THE LAST TWO REVISIONS: every fix the audit demands adds a row, which
# changes the number the brief must state, which is another edit and another
# `cp`.  --fix-count writes it, so the ritual costs one command instead of
# three rounds.  It writes the CLEAN-TREE total (a dirty tree costs one
# passing row), which is the number the brief must carry.
# *** rev 73, F306 -- NORMALISE THE SECOND HALF UNCONDITIONALLY.
# The block below only runs when the TOTAL changed, and it rewrites the lines
# _stated_rows attributes to verify_clone.  The SELF-CONSISTENCY figure lives on
# the NEXT line (a `#` continuation), so whenever the total happened to be
# already correct the stale half survived -- which is exactly the state rev 73
# shipped twice.  Fix the pair first, then the total.
if real is not None and "--fix-count" in sys.argv:
    _t = open(BRIEF).read()
    _t2 = re.sub(r"(ALL )(\d+)( PASS\s*--\s*0 FIDELITY,\s*)(\d+)",
                 lambda m: m.group(1) + str(real) + m.group(3) + str(real), _t)
    if _t2 != _t:
        open(BRIEF, "w").write(_t2)
        open(pst, "w").write(_t2)
        print("  --fix-count: normalised the verdict PAIR to %d/%d" % (real, real))

if real is not None and real != stated and "--fix-count" in sys.argv:
    import glob as _g
    # LINE-TARGETED.  A blind string replace hits bootstrap's "ALL 10 PASS"
    # too -- that is exactly what corrupted the rev-59 brief.  Only lines this
    # file has ATTRIBUTED to verify_clone are rewritten.
    _lines = open(BRIEF).read().splitlines(keepends=True)
    # *** rev 73, F306 -- REWRITE BOTH HALVES, NOT JUST THE FIRST.
    # The second sub keyed on the OLD total, so whenever the two halves had
    # already drifted apart it matched nothing and left the stale one behind --
    # and this row then PASSED, because it only ever compared the first figure.
    # HANDOFF_CARRIERS.md sec 0 records the same defect at rev 69 ("351 PASS ...
    # 342 SELF-CONSISTENCY") with the rule beside it: "The two halves must
    # always be the SAME number."  It recurred at rev 73 twice.  Keying the
    # SELF-CONSISTENCY sub on ANY integer is what stops it recurring a third
    # time; the row below then checks the invariant rather than trusting it.
    for _i, _ in _stated_rows("".join(_lines)):
        _lines[_i] = re.sub(r"ALL \d+ PASS", "ALL %d PASS" % real, _lines[_i])
        _lines[_i] = re.sub(r"\d+ SELF-CONSISTENCY",
                            "%d SELF-CONSISTENCY" % real, _lines[_i])
    t = "".join(_lines)
    open(BRIEF, "w").write(t)
    open(pst, "w").write(t)
    print("  --fix-count: rewrote %d -> %d in the brief AND in %s"
          % (stated, real, os.path.basename(pst)))
    stated = real
ck("brief states verify_clone.sh's own row count", real is not None and real == stated,
   "brief says %s, script says %s%s" % (stated, real,
   "" if real == stated else "   [re-run with --fix-count to write it]"))

# ------------------------------------------------- 6. README / START_HERE
for f in ("README.md", "START_HERE.md"):
    t = open(os.path.join(ROOT, f)).read()
    ck("%s names rev %d" % (f, N), ("rev %d" % N) in t)

# --------------------------------------------- 7. the self-referential traps
# Each of these has FIRED in this repo, in the row written to explain it.
trap_ok = True
# (a) a bare filename beside a qualified sibling
tiles = re.findall(r"`(rev\d+_[A-Za-z0-9_]+\.png)`", BOTH)
if tiles:
    trap_ok = False
ck("no probe tile is named without its directory", trap_ok,
   "found %s" % (" ".join(tiles) if tiles else "none"))
# (b) the audit row's own phrase must appear exactly once
ph = "newest brief records its own audit"
ck("the audit-row phrase appears at most once", TXT.count(ph) <= 1,
   "%d occurrence(s)" % TXT.count(ph))
# (c) the retired sec.4 heading must not come back as a heading
ck("the retired sec.4 heading is not a heading",
   not re.search(r"(?m)^#+ .*WHAT ONLY HE CAN GIVE", TXT))

print("-" * 78)
print("  %d checked, %d FAILED%s"
      % (_NCK, len(fails), ("  ->  " + "; ".join(fails)) if fails else ""))
print("  This is the MECHANICAL half of rule 17.  The other half -- RECOMPUTE")
print("  every figure -- is the revision's own job and no script can do it.")
sys.exit(1 if fails else 0)
