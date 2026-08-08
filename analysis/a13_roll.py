import numpy as np, sys
sys.path.insert(0,'/home/claude/tacombi/analysis')
from util import *
im,a=load('/home/claude/tacombi/ref_side.jpg'); H,W,_=a.shape
L=lum(a)
print("=== RIGHT background wall base (wall->pavement) x 930..1020 ===")
for x in range(930,1024,10):
    col=L[540:640,x].astype(float); g=np.gradient(col); k=int(np.argmin(g))
    print(f" x={x} strongest fall @ y={540+k} g={g[k]:.3f}; vals 560..610:", " ".join(f"{L[y,x]:.2f}" for y in range(560,615,5)))
print()
print("=== LEFT background wall base x 0..60 ===")
for x in range(0,62,10):
    col=L[540:660,x].astype(float); g=np.gradient(col); k=int(np.argmin(g))
    print(f" x={x} strongest fall @ y={540+k} g={g[k]:.3f}; vals 560..650:", " ".join(f"{L[y,x]:.2f}" for y in range(560,655,10)))
print()
print("=== LEFT wall TOP edge (wall vs foliage/sky) x 0..60, y 120..200 ===")
for x in range(0,62,10):
    col=L[100:220,x].astype(float); g=np.gradient(col); k=int(np.argmax(g))
    print(f" x={x} rise @ y={100+k} g={g[k]:.3f}")
