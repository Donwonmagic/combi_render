import numpy as np, math
from PIL import Image
def load(p): return np.asarray(Image.open(p).convert('RGB')).astype(float)

def radprof(im,cx,cy,rmax,kR,kG,kB,n=720,step=0.20):
    out=[]
    for k in range(n):
        th=2*math.pi*k/n; last=0.0; r=2.0
        while r<rmax:
            x=int(round(cx+r*math.cos(th))); y=int(round(cy+r*math.sin(th)))
            if 0<=y<im.shape[0] and 0<=x<im.shape[1]:
                p=im[y,x]
                if p[0]>kR and p[1]<kG*p[0] and p[2]<kB*p[0]: last=r
            r+=step
        out.append(last)
    return np.array(out)

def mfold(rp):
    """normalised amplitude of each angular harmonic m of the radius profile"""
    n=len(rp); F=np.fft.rfft(rp-rp.mean())/n*2.0
    med=np.median(rp)
    return {m: abs(F[m])/med for m in range(1,11)}

# ---- POSITIVE / NEGATIVE CONTROLS on synthetic profiles ----
th=np.linspace(0,2*np.pi,720,endpoint=False)
circ=np.full(720,32.6)
lobe=32.6+2.6*np.clip(np.cos(5*th),0,None)**1     # 5 petals, +8% peak
print("CONTROL circle   m5=%.4f  (all m<=%.4f)"%(mfold(circ)[5],max(mfold(circ).values())))
print("CONTROL 5-petal  m5=%.4f  m1=%.4f m2=%.4f"%(mfold(lobe)[5],mfold(lobe)[1],mfold(lobe)[2]))

R=load('out/r51c_side.png'); P=load('ref_side.jpg')
def run(tag,im,cx,cy,rmax,ths):
    for (kR,kG,kB) in ths:
        rp=radprof(im,cx,cy,rmax,kR,kG,kB)
        h=mfold(rp)
        print("%-16s th(%3d,%.2f,%.2f) med %.2f  m5 %.4f | m1 %.4f m2 %.4f m3 %.4f m4 %.4f m6 %.4f m7 %.4f"
              %(tag,kR,kG,kB,np.median(rp),h[5],h[1],h[2],h[3],h[4],h[6],h[7]))
ths=[(85,0.70,0.70),(95,0.62,0.70),(75,0.75,0.80),(110,0.60,0.65)]
print("\nRENDER rear hub (centre 1099.2,873.9)")
run("render rear",R,1099.2,873.9,50,ths)
print("\nPHOTO ref_side rear hub (centre 749.9,603.4)")
run("photo rear",P,749.9,603.4,38,ths)
