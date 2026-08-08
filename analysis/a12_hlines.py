import numpy as np, sys
sys.path.insert(0,'/home/claude/tacombi/analysis')
from util import *
im,a=load('/home/claude/tacombi/ref_side.jpg'); H,W,_=a.shape
h,s,v=hsv(a); L=lum(a)
# Drip-rail / roof-opening dark line above the cream band: find the dark line minimum per column
print("=== dark line under the raised lid (roof opening rim) 250..320 ===")
for x in range(200,790,25):
    col=L[250:330,x]; k=int(np.argmin(col))
    print(f" x={x} darkmin@{250+k} L={col[k]:.3f}")
print()
print("=== cream roof/gutter band TOP edge (bright cream starts) ===")
for x in range(140,780,20):
    col=L[255:340,x].astype(float)
    # find last strong rising edge into cream (>0.72)
    idx=np.nonzero(col>0.72)[0]
    print(f" x={x} first_cream_y={255+idx[0] if len(idx) else None}")
