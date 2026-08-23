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
fails = []


def ck(label, ok, detail=""):
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
for m in re.finditer(r"`([^`\n]+)`", TXT):
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
outp = [p for p in bad if p.startswith("out/")]
bad = [p for p in bad if not p.startswith("out/")]
ck("every path the brief names resolves", not bad,
   "%d checked, %d unresolved%s" % (len(paths), len(bad),
                                    ("  " + " ".join(bad)) if bad else ""))
if outp:
    print("       (%d in out/, which is untracked and starts empty: %s)"
          % (len(outp), " ".join(outp)))

# --------------------------------------------------------- 2. T1_* switches
sw = sorted(set(re.findall(r"\bT1_[A-Z0-9_]+\b", TXT)))
srcs = {p: open(os.path.join(ROOT, p)).read()
        for p in os.listdir(ROOT) if p.endswith((".py", ".sh"))}
# THIS MUST MATCH verify_clone.sh's OWN ROW, IDIOM FOR IDIOM.  Rev 57b
# loosened it here and not there, and the result was this tool reporting green
# while the repository's verifier failed on the same two switches -- two
# instruments disagreeing because one had been relaxed to fit new code.  The
# fix belonged in the new code.  If this ever needs loosening again, loosen
# BOTH or neither.
dead = []
for s_ in sw:
    if not any(re.search(r"(environ(\.get)?\[?\(?[\"']%s|getenv\([\"']%s)" % (s_, s_), t)
               for t in srcs.values()):
        dead.append(s_)

ck("every T1_* the brief names READS THE ENVIRONMENT", not dead,
   "%d named, %d not an env read%s" % (len(sw), len(dead),
                                       ("  " + " ".join(dead)) if dead else ""))

# ------------------------------------------------------------- 3. runnables
runs = sorted(set(re.findall(r"-P (\w+\.py)", TXT))
              | set(re.findall(r"python3 (\w+\.py)", TXT)))
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
stated = re.search(r"ALL (\d+) PASS", TXT)
stated = int(stated.group(1)) if stated else None
# THE ROW COUNT IS SELF-REFERENTIAL AND IT HAS COST THREE EDIT CYCLES IN EACH
# OF THE LAST TWO REVISIONS: every fix the audit demands adds a row, which
# changes the number the brief must state, which is another edit and another
# `cp`.  --fix-count writes it, so the ritual costs one command instead of
# three rounds.  It writes the CLEAN-TREE total (a dirty tree costs one
# passing row), which is the number the brief must carry.
if real is not None and real != stated and "--fix-count" in sys.argv:
    import glob as _g
    t = open(BRIEF).read().replace("ALL %d PASS" % stated, "ALL %d PASS" % real) \
                          .replace("%d SELF-CONSISTENCY" % stated,
                                   "%d SELF-CONSISTENCY" % real)
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
tiles = re.findall(r"`(rev\d+_[A-Za-z0-9_]+\.png)`", TXT)
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
      % (7 + 2, len(fails), ("  ->  " + "; ".join(fails)) if fails else ""))
print("  This is the MECHANICAL half of rule 17.  The other half -- RECOMPUTE")
print("  every figure -- is the revision's own job and no script can do it.")
sys.exit(1 if fails else 0)
