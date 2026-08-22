# Prototype: extend verify.py's _RETIRED_VALUES scan from SPEC.md to the .py sources.
# A retired literal must not appear UNMARKED (not struck ~~, not on a line that
# says stale/retired/refuted/withdrawn/WAS/DO NOT) in any tracked .py file.
import re,glob,subprocess
LITS = ["0.7273","0.507 / 0.516 / 0.526","0.0330","196, 106, 36","0.7313",
        "z = 1.402","z = 1.798","1.046 m wide"]
MARK = re.compile(r'~~|stale|STALE|RETIRED|retired|REFUTED|refuted|WITHDRAWN|withdrawn|WAS |DO NOT|NOT to be|no longer|CORRECTED')
files=[f for f in subprocess.check_output(["git","ls-files","*.py"]).decode().split()
       if not f.startswith("probe_scratch")]
hits=0
for f in files:
    if f in ("verify.py","audit.py"): continue      # they OWN the retirement table
    for i,ln in enumerate(open(f,encoding='utf-8',errors='replace'),1):
        for lit in LITS:
            if lit in ln and not MARK.search(ln):
                print("UNMARKED  %-14s %s:%d  %s" % (lit,f,i,ln.strip()[:100])); hits+=1
print("\nunmarked re-quotes of retired literals in .py sources:",hits)
