"""rev 50, THE RECORD.  Run verify._retired_value_drift's OWN table against the
ONE section it exempts by design: SPEC sec.0.2 and sec.0.2b.

WHY.  The exemption's stated reason (verify.py:348-355) is that "sec.0.2 IS the
retirement list -- it exists to name retired values".  That is true of the LEFT
half of each entry.  Each entry is "<retired reading> -- actually <correction>",
and the CORRECTION is a live assertion.  When a correction is itself later
refuted, sec.0.2 keeps publishing it and the guard is blind to that BY DESIGN.
This probe finds every occurrence and then the hits are adjudicated BY HAND --
naming a retired reading is correct behaviour, asserting a refuted correction
is not.  The probe does not decide; it lists.

CEILING.  Substring matching, exactly as the guard does.  It imports the table
from verify.py by TEXT (verify imports bpy) so the table cannot drift from the
one that ships.
"""
import re, ast
src = open("verify.py", encoding="utf-8").read()
m = re.search(r"^_RETIRED_VALUES = \((.*?)^\)\s*$", src, re.S | re.M)
body = m.group(1)
body = "\n".join(l for l in body.split("\n") if not l.strip().startswith("#"))
TAB = ast.literal_eval("(" + body + ")")
OK = ("RETIRED", "retired", "~~", "superseded", "SUPERSEDED",
      "REFUTED", "refuted", "withdrawn", "WITHDRAWN", "stale")
print("table rows: %d" % len(TAB))

lines = open("SPEC.md", encoding="utf-8").read().splitlines()
# locate sec 0.2 / 0.2b spans
spans, cur = [], None
for i, ln in enumerate(lines, 1):
    if ln.startswith("#"):
        h = ln.lstrip("#").strip()
        if h.startswith("0.2"):
            cur = [i, None, h]; spans.append(cur)
        elif cur is not None and cur[1] is None:
            lvl = len(ln) - len(ln.lstrip("#"))
            # close on any heading that is not deeper than the 0.2 heading
            cur[1] = i - 1
for s in spans:
    if s[1] is None: s[1] = len(lines)
print("sections found:", [(s[2], s[0], s[1]) for s in spans])

hits = 0
for a, b, h in spans:
    for i in range(a, b + 1):
        ln = lines[i - 1]
        if any(t in ln for t in OK):
            continue
        for lit, live, sym, sec in TAB:
            if lit in ln:
                hits += 1
                print("\nSPEC.md:%d   [%s]  literal %r" % (i, h, lit))
                print("   live now: %s  (%s, sec %s)" % (live, sym, sec))
                print("   line: %s" % ln.strip()[:150])
print("\nUNSTRUCK occurrences of a RETIRED value inside the exempted section: %d" % hits)
