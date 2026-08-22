import re, os, sys, collections
DOCS = ["START_HERE.md","README.md","STATE.md","SPEC.md","LEDGER_rev51.md","LEDGER_rev50.md",
        "LEDGER_rev49.md","NEXT_CONTEXT_PROMPT_rev51.md","SURVEY_rev49_photoreal.md",
        "REF_MEASUREMENTS.md","REFERENCE_FRAMES_rev45.md"]
pat = re.compile(r'\b([A-Za-z_0-9]+\.(?:py|sh|md)):(\d+)(?:\s*[-–]\s*(\d+))?')
cache={}
def lines(f):
    if f not in cache:
        try: cache[f]=open(f,encoding='utf-8',errors='replace').read().split('\n')
        except Exception: cache[f]=None
    return cache[f]
rows=[]
for d in DOCS:
    if not os.path.exists(d): continue
    for ln,txt in enumerate(open(d,encoding='utf-8',errors='replace').read().split('\n'),1):
        for m in pat.finditer(txt):
            tgt,a,b = m.group(1), int(m.group(2)), m.group(3)
            L=lines(tgt)
            if L is None: st="NOFILE"; content=""
            elif a>len(L): st="OUT_OF_RANGE(file has %d)"%len(L); content=""
            else:
                content=L[a-1]
                st="BLANK" if content.strip()=="" else "ok"
            rows.append((d,ln,m.group(0),tgt,a,st,content.strip()[:90]))
tot=len(rows)
bad=[r for r in rows if r[5]!="ok"]
print("citations scanned in live docs:",tot)
print("distinct:",len(set(r[2] for r in rows)))
c=collections.Counter(r[5].split('(')[0] for r in rows)
print(dict(c))
print()
print("=== BROKEN (blank or out of range) ===")
for r in bad:
    print("%-30s L%-6d %-28s -> %s" % (r[0],r[1],r[2],r[5]))
