"""audit_adversary.py -- rule 15's half of the outgoing-brief audit.

`audit_brief.py` asks *is what the file says TRUE?* -- paths, switches, counts.
This asks the other question: *what would make it FALSE?*  They are different
instruments and rev 55 onward has required both.  The difference is that this
one RECOMPUTES the brief's headline figures from the renders and the source
rather than checking that a string is present.

Written as a script and RUN, so the list a revision reports is what actually
executed rather than what it meant to try.  REPLACE the questions each
revision -- they are about THAT revision's claims, and a question that can no
longer fail is not a control.  Keep the shape: recompute, don't re-read.

    python3 audit_adversary.py
"""
import os, re, subprocess, math
import numpy as np
from PIL import Image
import scipy.ndimage as ndi
os.chdir('/home/user/combi_render')
P=print; bad=[]
def t(q, ok, d=""):
    P("  %-5s %s" % ("ok" if ok else "BROKE", q)); P("         %s" % d)
    if not ok: bad.append(q)
B=open('NEXT_CONTEXT_PROMPT_rev58.md').read()

# 1. the headline ablation, recomputed from the two renders, not from prose
def gl(f):
    a=np.asarray(Image.open(f).convert('RGB')).astype(float)[610:790,520:1060]
    R,G,Bl=a[...,0],a[...,1],a[...,2]; L=0.2126*R+0.7152*G+0.0722*Bl
    m=(R>G*1.35)&(R>Bl*1.35)&(L>25)
    m=ndi.binary_erosion(ndi.binary_opening(m,np.ones((5,5))),np.ones((5,5)))
    p5,p50,p95=np.percentile(L[m],[5,50,95])
    return (p95-p5)/p50, (G[m]/np.maximum(R[m],1)).mean()
s0,c0=gl('out/g0_hero.png'); s1,c1=gl('out/g1_hero.png')
sp,cp=gl('ref_nolita_front34.jpg') if False else (1.192,0.114)
t("does the clearcoat really buy only +0.5 % of spread?",
  abs((s1/sp)-(s0/sp)) < 0.01,
  "recomputed: %.3f -> %.3f of the photograph's" % (s0/sp, s1/sp))
t("does it really cost ~18 % of the red's saturation?",
  c1 > c0*1.15, "G/R %.4f -> %.4f  (%+.1f %%)" % (c0,c1,100*(c1/c0-1)))

# 2. is the gloss statistic exposure-free, as the brief claims?
o=subprocess.run(['python3','gloss_compare.py'],capture_output=True,text=True).stdout
v=re.findall(r'x[01]\.\d\d  spread (\d\.\d+)', o)
t("is gloss_compare exposure-free?", len(v)==3 and len(set(v))==1, "0.70x/1.00x/1.40x -> %s"%v)

# 3. does the budget still rank gloss top and the badge bottom?
o2=subprocess.run(['python3','visibility_budget.py','3840'],capture_output=True,text=True).stdout
rows=[l for l in o2.splitlines() if re.match(r'^ +\d+\. ',l)]
t("does the budget still rank gloss over the badge?",
  'GLOSS' in rows[0] and 'badge' in rows[-1], "top %r / bottom %r"%(rows[0][6:46],rows[-1][6:46]))

# 4. F51: is the rig really only inside build.py's preview block?
bp=open('build.py').read()
i=bp.index('if os.environ.get("T1_PREVIEW")')
t("F51: is ST.lighting ONLY inside the preview block?",
  bp.count('ST.lighting(')==1 and bp.index('ST.lighting(')>i,
  "ST.lighting appears %d time(s); preview block starts at char %d, call at %d"
  %(bp.count('ST.lighting('), i, bp.index('ST.lighting(')))

# 5. F53: is Roughness really linked?  (read the probe's own last output)
g0=open('/tmp/claude-0/-home-user-combi-render/2aef52fe-c3ce-545a-b0a9-403bc2d5249e/scratchpad/gl_g0.log').read()
t("F53: did the probe really report Roughness LINKED?",
  'INERT for: Roughness' in g0, "the probe's own line, from its first run")

# 6. is the delivery frame lit and seam-free, as claimed?
a=np.asarray(Image.open('out/hq_hero.png').convert('RGB')).astype(float)
nz=a[a.max(axis=2)<250]
hq=open('/tmp/claude-0/-home-user-combi-render/2aef52fe-c3ce-545a-b0a9-403bc2d5249e/scratchpad/hq3.log').read()
t("is the shipped delivery frame lit AND seam-free?",
  nz.mean()>120 and 'no seam detectable' in hq and 'STITCH rc=0' in hq,
  "non-backdrop mean %.1f; stitch rc=0; worst seam z = %s"
  % (nz.mean(), re.search(r'worst seam z = ([\d.]+)',hq).group(1)))

# 7. did rev 57b change any MODEL code?
d=subprocess.run(['git','diff','5378d78..HEAD','--','t1_core.py','t1_shell.py','t1_detail.py',
                  't1_mats.py','build.py','studio.py','lid_gen.py','script_gen.py'],
                 capture_output=True,text=True).stdout
code=[l for l in d.splitlines() if l.startswith(('+','-')) and not l.startswith(('+++','---'))
      and not re.match(r'^[+-]\s*#',l) and l.strip() not in ('+','-')]
t("did rev 57/57b change any MODEL code?", not code,
  "non-comment +/- lines across all eight model files since rev 56: %d"%len(code))

# 8. no bar was moved to make anything pass
d2=subprocess.run(['git','diff','5378d78..HEAD','--','flank_compare.py','verify.py','mottle_measure.py'],
                  capture_output=True,text=True).stdout
t("was any threshold moved?", '_TOL' not in d2 and 'REGION_IOU_FRAC' not in d2 and 'BAR =' not in d2,
  "no *_TOL, no REGION_IOU_FRAC, no BAR in the diff of the three gate files")

# 9. does the brief promise a baseline image that is not in the clone?
tracked=set(subprocess.run(['git','ls-files'],capture_output=True,text=True).stdout.split())
promised=[p for p in re.findall(r'`(probe_scratch/[A-Za-z0-9_.-]+\.png)`', B) if p not in tracked]
t("does the brief cite any probe tile that is not tracked?", not promised, "unresolved: %s"%promised)

# 10. is anything claimed CLOSED that is still open?
of=open('OPEN_FINDINGS.md').read()
t("is item A claimed solved anywhere?",
  'F44' in of and 'OPEN' in of[of.index('| **F44**'):of.index('| **F44**')+400],
  "F44 is still OPEN; F54 closes only the CLEARCOAT ROUTE, not the item")

P(); P("  %d tried, %d BROKE%s"%(10,len(bad),("  -> "+"; ".join(bad)) if bad else ""))
