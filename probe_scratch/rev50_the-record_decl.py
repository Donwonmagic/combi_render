"""rev 50, THE RECORD.  Every MODULE-LEVEL constant whose own comment declares
it unmeasured, and whether verify_clone.sh has a row that would notice if that
declaration were deleted.

CEILING.  This is a TEXT scan, not a semantic one.  It looks at the constant's
own line plus the 30 lines above and 6 below for one of the marker phrases, so
a constant whose declaration lives further away is missed and a constant that
merely sits under someone else's paragraph is a false positive -- each hit is
printed with the line that matched so it can be read.
"""
import re, os, sys
MARK = ("NOT MEASURED","POSE CHOICE","pose choice","INFERRED","UNMEASURED",
        "AUTHORED, NOT MEASURED","AUTHORED","authored","not measured",
        "DECLARED, not measured","chosen, not measured")
FILES = ["t1_shell.py","t1_detail.py","t1_core.py","t1_mats.py","cal_gen.py",
         "folk_gen.py","script_gen.py","studio.py","build.py","lid_gen.py"]
vc = open("verify_clone.sh").read()
rows = []
for f in FILES:
    L = open(f).read().split("\n")
    for i, ln in enumerate(L):
        m = re.match(r"^([A-Z][A-Z0-9_]{2,})\s*=\s*(.+?)(\s*#.*)?$", ln)
        if not m: continue
        name, val = m.group(1), m.group(2).strip()
        ctx = "\n".join(L[max(0,i-30):i+7])
        hit = None
        for k in MARK:
            if k in ctx:
                for j in range(max(0,i-30), min(len(L), i+7)):
                    if k in L[j]:
                        hit = (k, j+1, L[j].strip()[:96]); break
                break
        if hit is None: continue
        guarded = name in vc
        rows.append((f, i+1, name, val[:34], hit[0], hit[1], guarded, hit[2]))
print("%-13s %5s %-22s %-16s %-14s %-6s %s" % ("file","line","constant","value","marker","in_vc","matched comment"))
for r in sorted(rows, key=lambda r:(not r[6], r[0], r[1])):
    print("%-13s %5d %-22s %-16s %-14s %-6s %s" % (r[0],r[1],r[2],r[3],r[4],"YES" if r[6] else "-- NO",r[7]))
print("\ntotal %d ; with a verify_clone mention %d ; WITHOUT %d"
      % (len(rows), sum(1 for r in rows if r[6]), sum(1 for r in rows if not r[6])))
