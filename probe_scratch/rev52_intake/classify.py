import re, collections
src = open('verify_clone.sh').read().split('\n')
# join continuation lines
lines=[]; buf=None
for i,l in enumerate(src):
    s=l
    if buf is not None:
        buf=(buf[0], buf[1]+' '+s.strip())
        if not s.rstrip().endswith('\\'):
            lines.append(buf); buf=None
        continue
    XX|;\s*|then\s+|else\s+)ck "', s):
        if s.rstrip().endswith('\\'):
            buf=(i+1, s.strip()[:-1])
        else:
            lines.append((i+1, s.strip()))
print("raw ck call sites:", len(lines))
# dedupe if/else pairs by label
def label(t):
    m=re.search(r'ck "((?:[^"\\]|\\.)*)"', t)
    return m.group(1) if m else t
seen={}
rows=[]
for ln,t in lines:
    lab=label(t)
    if lab in seen:
        seen[lab].append((ln,t)); continue
    seen[lab]=[(ln,t)]; rows.append((ln,lab,t))
print("distinct runtime rows:", len(rows))
dupes=[k for k,v in seen.items() if len(v)>1]
print("if/else pairs collapsed:", dupes)

def cls(ln,lab,t):
    body=t
    # what file does the row's expression read?
    if re.search(r'git (cat-file|merge-base|log|status|ls-files)', body): return 'A_repo_git'
    if re.search(r'\bls\b|\bwc -l\b', body) and 'grep' not in body: return 'B_repo_layout'
    if re.search(r'md5of', body): return 'D_texture_md5'
    if 'STATE.md' in body: return 'E_state_md'
    if 'SPEC.md' in body: return 'C_spec_doc'
    if re.search(r'grep', body): return 'F_source_grep'
    return 'Z_other'
cnt=collections.Counter()
out=[]
for ln,lab,t in rows:
    c=cls(ln,lab,t); cnt[c]+=1; out.append((c,ln,lab))
for c,n in sorted(cnt.items()): print(f"{c:18s} {n}")
print()
open('probe_scratch/rev52_intake/rows.txt','w').write('\n'.join(f"{c}\t{ln}\t{lab}" for c,ln,lab in sorted(out)))
# does ANY row read an image?
img=[ (ln,lab) for ln,lab,t in rows if re.search(r'\.(png|jpe?g|JPG)\b', t)]
print("rows whose EXPRESSION mentions an image file:", len(img))
for ln,lab in img: print("   ",ln,lab)
