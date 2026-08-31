#!/usr/bin/env python3
# revstats.py -- rev 70.  THE DRIFT DETECTOR.
#
# THE OWNER SAW THIS BEFORE ANY INSTRUMENT DID:
#
#   [owner, rev 70] "I feel that we were way more productive in the first 20
#   or so handoffs and I fear we have drifted since then."
#
# He is right, and this is the measurement.  For every revision it buckets the
# lines changed into GEOMETRY (the vehicle), DOC (prose about the vehicle) and
# INSTRUMENT (machinery that checks the vehicle), and it counts the findings
# the register records as CLOSED, REFUTED or RETRACTED that revision.
#
# WHY IT EXISTS.  All 54 rules in this project's canon are about not being
# WRONG; not one was about SHIPPING.  The drift that produced took TEN
# revisions to become visible, and only because the owner said so.  A number
# printed every revision makes it visible in ONE.
#
# READ THE SUMMARY LINE, NEVER THE EXIT CODE (rule 9).
import collections
import re
import subprocess
import sys

GEO = ('t1_core.py', 't1_shell.py', 't1_detail.py', 't1_mats.py', 'build.py',
       'studio.py', 'lid_gen.py', 'script_gen.py', 'vw_pressing.py')


def _bucket(f):
    """One place, so the merge path and the ordinary path cannot disagree."""
    if f in GEO:
        return 'geo'
    if f.endswith(('.md', '.txt')):
        return 'doc'
    if (f.startswith(('probe_', 'audit_'))
            or f in ('verify.py', 'verify_clone.sh', 'revstats.py')):
        return 'inst'
    return 'other'


def collect():
    # *** rev 72 -- MERGE COMMITS WERE COUNTED, AND THEY DOUBLE EVERY BRANCH. ***
    #
    # `git show --numstat <merge>` emits the merge's diff against its FIRST
    # PARENT, which for a PR merge is the ENTIRE BRANCH again -- every line the
    # branch's own commits already contributed.  So every revision landed by PR
    # was counted TWICE.  Measured at rev 72: rev 71 read 176 geometry lines,
    # and excluding merges it reads 88.  Exactly 2x, which is the signature.
    #
    # THIS MATTERS BECAUSE THIS SCRIPT IS THE OWNER'S OWN DRIFT INSTRUMENT.  He
    # said "we were way more productive in the first 20 or so handoffs and I
    # fear we have drifted since then", the project answered with this script,
    # and three documents quote it.  An instrument that doubles its numerator
    # understates the drift it exists to show -- and the honest doc:geo for
    # rev 71 is WORSE than any figure published for it (see LEDGER_rev72).
    #
    # AN INSTRUMENT THAT HAS NEVER BEEN WRONG HAS NEVER BEEN TESTED (CLAUDE.md).
    # Found by an adversary dispatched at the rev-72 brief under rule 15.
    log = subprocess.run(['git', 'log', '--reverse', '--pretty=%H%x09%P%x09%s'],
                         capture_output=True, text=True).stdout.splitlines()
    rev_of, parents_of, cur = {}, {}, None
    for ln in log:
        h, _, rest = ln.partition('\t')
        par, _, s = rest.partition('\t')
        m = re.match(r'\s*rev\s*(\d+)', s)
        if m:
            cur = int(m.group(1))
        rev_of[h] = cur
        parents_of[h] = par.split()
    merges = 0
    stats = collections.defaultdict(collections.Counter)
    for h, rev in rev_of.items():
        if rev is None:
            continue
        # *** rev 72b -- SKIPPING MERGES OUTRIGHT UNDER-COUNTED, AND THE FIRST
        # FIX'S OWN COMMENT STATED A FALSEHOOD. ***
        # It said a merge's first-parent diff is "the ENTIRE BRANCH again --
        # every line the branch's own commits already contributed."  That is
        # true of MOST merges and FALSE of any merge with a CONFLICT: the
        # resolution is content present in NO parent.  A rule-17 adversary found
        # four such merges here, the largest (`c430b5f`, rev 45) carrying 239
        # geometry and 1848 doc lines that `continue` threw away.
        # THE CORRECT INSTRUMENT IS `--cc`, WHICH REPORTS EXACTLY THE CONTENT
        # THAT DIFFERS FROM ALL PARENTS -- neither double-counting the branch
        # nor discarding the resolution.
        _merge = len(parents_of.get(h, [])) > 1
        if _merge:
            merges += 1
            stats[rev]['merges'] += 1
        if _merge:
            # ⚠ `--cc` HAS NO EFFECT ON `--numstat` -- GIT IGNORES IT SILENTLY.
            # Measured at rev 72b: `git show --cc --numstat 0de5fd2` and the
            # same command without `--cc` both emit 39 identical rows, i.e. the
            # FULL first-parent diff.  So the obvious fix for the undercount
            # fails without saying so, which is rule 58's shape in git rather
            # than in PIL.  The combined diff has to be read as a PATCH.
            # In combined-diff format a line beginning `++` is content present
            # in NO parent -- exactly the merge RESOLUTION, which is real work
            # that belongs to the revision that did it.
            pat = subprocess.run(
                ['git', 'show', '--cc', '--format=', '--no-renames', h],
                capture_output=True, text=True, errors='replace').stdout
            f = None
            for line in pat.splitlines():
                if line.startswith('+++ '):
                    f = line[4:].strip()
                    f = f[2:] if f.startswith(('a/', 'b/')) else f
                elif line.startswith('--- ') or line.startswith('@@'):
                    continue
                elif f and line.startswith('++'):
                    stats[rev][_bucket(f)] += 1
            continue
        out = subprocess.run(
            ['git', 'show', '--numstat', '--format=', '--no-renames', h],
            capture_output=True, text=True).stdout
        for line in out.splitlines():
            p = line.split('\t')
            if len(p) != 3 or p[0] == '-':
                continue
            a, d, f = int(p[0]), int(p[1]), p[2]
            stats[rev][_bucket(f)] += a + d
        stats[rev]['commits'] += 1
    return stats


def closures():
    try:
        t = open('OPEN_FINDINGS.md', errors='replace').read()
    except OSError:
        return {}
    c = collections.Counter()
    for kind, rev in re.findall(r'(CLOSED|REFUTED|RETRACTED)-rev(\d+)', t):
        c[int(rev)] += 1
    return c


def main():
    st, cl = collect(), closures()
    revs = sorted(st)
    if not revs:
        print("  NO REVISIONS FOUND -- nothing measured (rule 37)")
        return 1

    print("=" * 78)
    print("  revstats.py -- OUTPUT PER REVISION.  Is the project building, or")
    print("                 describing the building?")
    print("=" * 78)
    print("  band        revs   GEOMETRY/rev   DOC/rev   INSTR/rev   doc:geo   closed")
    bands = [(8, 20), (21, 35), (36, 50), (51, 60), (61, 70), (71, 80), (81, 99)]
    for lo, hi in bands:
        inb = [r for r in revs if lo <= r <= hi]
        if not inb:
            continue
        g = sum(st[r]['geo'] for r in inb)
        d = sum(st[r]['doc'] for r in inb)
        i = sum(st[r]['inst'] for r in inb)
        c = sum(cl.get(r, 0) for r in inb)
        n = len(inb)
        print("  rev %2d-%2d    %2d      %6d       %6d      %5d     %6.2f    %3d"
              % (lo, hi, n, g // n, d // n, i // n, (d / g if g else 0), c))

    print()
    print("  THE LAST TEN REVISIONS, ONE ROW EACH")
    print("  rev   commits   geometry   doc   instrument   findings closed")
    for r in revs[-10:]:
        v = st[r]
        print("  %-4d  %5d    %7d  %6d   %8d   %8d"
              % (r, v['commits'], v['geo'], v['doc'], v['inst'], cl.get(r, 0)))

    last5 = revs[-5:]
    g5 = sum(st[r]['geo'] for r in last5)
    c5 = sum(cl.get(r, 0) for r in last5)
    print()
    # *** rev 72b -- THIS BASELINE WAS HARD-CODED AND DISAGREED WITH THE TABLE
    # PRINTED NINE LINES ABOVE IT, IN THE SAME OUTPUT. ***
    # It said "721 geometry lines ... doc:geo 1.55" while the band table read
    # 718 and 1.40 off the live repository.  `CLAUDE.md` had already deleted 721
    # as wrong, and rev 72's own F273 edit to this file left the stale figure in
    # place and CALLED IT "the bar".  A script that contradicts itself in one
    # screen is not an instrument.  COMPUTED NOW, from the same numbers as the
    # table, so it cannot drift again.  Found by the rule-17 adversary.
    _bl = [r for r in revs if 8 <= r <= 20]
    if _bl:
        _bg = sum(st[r]['geo'] for r in _bl)
        _bd = sum(st[r]['doc'] for r in _bl)
        print("  BASELINE, THE ERA THE OWNER NAMED: rev 8-20 ran %d geometry"
              % (_bg // len(_bl)))
        print("  lines per revision at a doc:geo ratio of %.2f.  That is the bar."
              % (_bd / _bg if _bg else 0))
        print("  (COMPUTED from this run, not typed -- the figure that used to be")
        print("   printed here was 721 / 1.55 and disagreed with the table above.)")
    else:
        print("  BASELINE UNAVAILABLE: no rev 8-20 commits in this clone's history")
        print("  (a shallow clone?).  Not a measurement -- say so, do not guess.")
    print()
    print("  LAST FIVE REVISIONS (%s): %d geometry lines, %d findings closed."
          % ("-".join(str(x) for x in (last5[0], last5[-1])), g5, c5))
    if c5 == 0:
        print("  *** ZERO CLOSURES IN FIVE REVISIONS. Rule 55: a revision ships a")
        print("  *** visible change to the vehicle, or says PLAINLY why it could not.")
    print()
    print("  CEILING ON THIS INSTRUMENT, AND IT IS REAL: lines changed is a PROXY for")
    print("  work, not a measure of it -- a one-line constant can be a revision's whole")
    print("  result (F238 was one default), and a large refactor can be worth nothing.")
    print("  The CLOSED column is the harder currency.  Read them together, and never")
    print("  quote the line counts as productivity on their own.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
