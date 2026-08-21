import numpy as np
from PIL import Image
A=np.asarray(Image.open('/home/user/combi_render/ref_side.jpg').convert('RGB')).astype(float)
R,G,B=A[:,:,0],A[:,:,1],A[:,:,2]
YEL=(R+G)/2.0-B
print("ESTIMATOR 2 -- pure threshold mask, no tracker, no seed.")
print("For each row: first and last column in x 290..775 with YEL>=T (>=3 consecutive).")
for T in (55,70,85,100):
    rows=[]; print(" T=%d"%T)
    for r in range(35,265,10):
        seg=YEL[r,290:776]>=T
        # require runs of >=3
        idx=[i for i in range(1,len(seg)-1) if seg[i-1] and seg[i] and seg[i+1]]
        if len(idx)<20: continue
        L,Rr=290+idx[0]-1,290+idx[-1]+1
        rows.append((r,L,Rr,Rr-L))
    ys=np.array([q[0] for q in rows],float); sp=np.array([q[3] for q in rows],float)
    p=np.polyfit(ys,sp,1)
    print("   rows %d..%d  span %.0f -> %.0f   d(span)/dy = %+.4f px/row  (%.2f %%/row)"%(
        rows[0][0],rows[-1][0],sp[0],sp[-1],p[0],100*p[0]/sp.mean()))
    print("   left  %s"%(" ".join("%d:%d"%(q[0],q[1]) for q in rows[::3])))
    print("   right %s"%(" ".join("%d:%d"%(q[0],q[2]) for q in rows[::3])))
print()
print("CONTROL: same estimator on a pair of TRUE VERTICALS (lamppost L edge, column L edge)")
print("  vertical-pair convergence implied by fitted slopes: 0.0417-0.0203=+0.0214 over 723 px")
print("  board-pair convergence measured:                    0.0598-0.1553=-0.0955 over 420 px")
print("  ratio of angular convergence rates = %.1f x, OPPOSITE SIGN of what alpha>90 needs"%(0.0955/0.0214))
