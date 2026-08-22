# NARROWED: a retired literal counts only when it appears ADJACENT TO ITS OWN
# SYMBOL on the same line -- that is a re-quote of the retired QUANTITY, not a
# coincidental digit string.  Scope: the build modules only (not probes/marks,
# which are historical instrument records and must keep their old figures).
import re, subprocess
ROWS = [("0.7273", r"Yt"), ("0.0330", r"rake|RAKE"), ("0.7313", r"W_DUST_FAC_UP|W_DUP"),
        ("1.1100", r"LID_W")]
MARK = re.compile(r'~~|stale|STALE|RETIRED|REFUTED|WITHDRAWN|WAS |was |DO NOT|no longer|REJECTED|CORRECTED|restor')
SCOPE = ["build.py","t1_core.py","t1_shell.py","t1_detail.py","t1_mats.py","studio.py","post.py","cal_gen.py","lid_gen.py","script_gen.py","folk_gen.py","texgen.py","hero.py","sign_gen.py"]
n=0
for f in SCOPE:
    try: src=open(f,encoding='utf-8',errors='replace').read().split('\n')
    except FileNotFoundError: continue
    for i,ln in enumerate(src,1):
        for lit,sym in ROWS:
            if lit in ln and re.search(sym,ln) and not MARK.search(ln):
                print("UNMARKED RE-QUOTE  %-8s(%s)  %s:%d\n    %s" % (lit,sym,f,i,ln.strip())); n+=1
print("\nrows a narrowed guard would report:",n)
