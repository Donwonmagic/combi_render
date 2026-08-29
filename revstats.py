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


def collect():
    log = subprocess.run(['git', 'log', '--reverse', '--pretty=%H%x09%s'],
                         capture_output=True, text=True).stdout.splitlines()
    rev_of, cur = {}, None
    for ln in log:
        h, _, s = ln.partition('\t')
        m = re.match(r'\s*rev\s*(\d+)', s)
        if m:
            cur = int(m.group(1))
        rev_of[h] = cur
    stats = collections.defaultdict(collections.Counter)
    for h, rev in rev_of.items():
        if rev is None:
            continue
        out = subprocess.run(['git', 'show', '--numstat', '--format=', '--no-renames', h],
                             capture_output=True, text=True).stdout
        for line in out.splitlines():
            p = line.split('\t')
            if len(p) != 3 or p[0] == '-':
                continue
            a, d, f = int(p[0]), int(p[1]), p[2]
            if f in GEO:
                k = 'geo'
            elif f.endswith(('.md', '.txt')):
                k = 'doc'
            elif (f.startswith(('probe_', 'audit_'))
                  or f in ('verify.py', 'verify_clone.sh', 'revstats.py')):
                k = 'inst'
            else:
                k = 'other'
            stats[rev][k] += a + d
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
    print("  BASELINE, THE ERA THE OWNER NAMED: rev 8-20 ran 721 geometry lines")
    print("  per revision at a doc:geo ratio of 1.55.  That is the bar.")
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
