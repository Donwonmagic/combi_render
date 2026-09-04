"""
probe_rev77_t3floor.py -- THE EXPERIMENT F312 PRESCRIBED, RUN TO A SAMPLE SIZE
THAT CAN CARRY A CONCLUSION.

WHAT WAS OUTSTANDING.  F324 read `probe_rev73_tailboard.py`'s T3 rung on three
renders of one tree -- -7.00 / -8.50 / -6.50 -- and concluded T3's verdict is
render noise, while ALSO reporting that rev 74's frames clustered separately at
-9.00 / -9.00 / -8.75 and calling the two "DISJOINT CLUSTERS", i.e. a
BUILD-dependence on top of the scatter.  It declined to re-base the 1.5 bar
because "a bar set on n = 3 is still an invented figure (rule 5)", and the rev-77
brief's own §2.1 named the fix: "FIVE OR SIX side renders of one tree is ~30
minutes and would set a real floor (rule 49) -- THEN a bar can be set on
something WATCHED rather than invented."

THIS IS THAT.  It reads the rung off EVERY `out/*_side.png` present, by running
`probe_rev73_tailboard.py` against each one BY NAME (rule 9: read the probe's own
line, never its exit code; F316: name the frame) and parsing what it printed.
That addressing is itself new -- until rev 77 the probe took no argument, which
is the reason a distribution across frames had never been measured.

WHAT IT CANNOT DO, STATED (rule 12):
  * It reports a SPREAD, not a bar.  Choosing a replacement threshold is a
    judgement this script deliberately does not make for you.
  * Frames rendered from DIFFERENT builds are not samples of one distribution.
    It reports build provenance as UNKNOWN unless the caller says otherwise,
    because a PNG does not carry the source tree that made it -- and that is
    precisely how F324's cluster claim came to rest on frames from three
    different builds.
  * n is whatever is on disk.  `out/` is untracked and starts empty.

Run:  python3 probe_rev77_t3floor.py [frame ...]
"""
import os, re, sys, glob, subprocess, statistics

ROOT = os.path.dirname(os.path.abspath(__file__))
RUNG = re.compile(r"-7\.0 -> (-?[\d.]+)")
GAIN = re.compile(r"MEAN GAIN ([\d.]+)")
BAR = 1.5                      # T3's live bar, for reporting the split only


def read(frame):
    out = subprocess.run([sys.executable,
                          os.path.join(ROOT, "probe_rev73_tailboard.py"), frame],
                         capture_output=True, text=True).stdout
    m, g = RUNG.search(out), GAIN.search(out)
    summ = [l for l in out.splitlines() if "checked," in l]
    if not m:
        return None
    return dict(frame=os.path.basename(frame), rung=float(m.group(1)),
                gain=float(g.group(1)) if g else None,
                summary=summ[-1].strip() if summ else "")


def main(argv):
    frames = argv or sorted(f for f in glob.glob(os.path.join(ROOT, "out", "*_side.png"))
                            if "raw" not in os.path.basename(f))
    if not frames:
        print("NO SIDE RENDERS: out/ is untracked and does not exist on a clone, "
              "so nothing was measured (rule 37).  Render the brief's sec.0 queue.")
        print("0 checked, 0 FAILED, 1 ABSENT")
        return 2

    rows = [r for r in (read(f) for f in frames) if r]
    if not rows:
        print("NO T3 RUNG could be parsed from any of %d frame(s).  Nothing was "
              "measured (rule 37)." % len(frames))
        print("1 checked, 1 FAILED")
        return 2

    print("T3's DECIDING RUNG, read off each frame BY NAME (bar |miss| < %.1f):" % BAR)
    for r in rows:
        miss = abs(r["rung"] - (-7.0))
        print("   %-22s  -7.0 -> %6.2f   miss %.2f   gain %s   %s"
              % (r["frame"], r["rung"], miss,
                 ("%.3f" % r["gain"]) if r["gain"] is not None else "  n/a",
                 "PASS" if miss < BAR else "FAIL"))

    rungs = [r["rung"] for r in rows]
    gains = [r["gain"] for r in rows if r["gain"] is not None]
    npass = sum(1 for r in rows if abs(r["rung"] + 7.0) < BAR)
    print()
    print("  n = %d   range %.2f deg (%.2f .. %.2f)   mean %.3f   sd %s"
          % (len(rungs), max(rungs) - min(rungs), min(rungs), max(rungs),
             statistics.mean(rungs),
             ("%.3f" % statistics.stdev(rungs)) if len(rungs) > 1 else "n/a (n=1)"))
    if gains:
        print("  MEAN GAIN over the same frames: mean %.3f   sd %s   range %.3f"
              % (statistics.mean(gains),
                 ("%.3f" % statistics.stdev(gains)) if len(gains) > 1 else "n/a",
                 max(gains) - min(gains)))
    print("  against the live bar %.1f: %d PASS / %d FAIL" % (BAR, npass, len(rows) - npass))
    print()
    print("  CEILING (rule 12): this is a SPREAD, not a bar.  It does not choose a")
    print("  threshold, and build provenance is UNKNOWN unless you rendered these")
    print("  yourself from one tree -- a PNG does not carry the source that made it,")
    print("  which is how F324's cluster claim came to span three builds.")
    print("%d checked, 0 FAILED  --  a distribution, not a verdict" % len(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
