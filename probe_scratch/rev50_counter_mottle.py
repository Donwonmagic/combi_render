import numpy as np
from PIL import Image

def lum(a): return 0.2126*a[...,0]+0.7152*a[...,1]+0.0722*a[...,2]

ph = np.asarray(Image.open('ref_side.jpg').convert('RGB')).astype(float)
rn = np.asarray(Image.open('out/r49board_side.png').convert('RGB')).astype(float)

# PHOTO fascia: follow the band. gold-bottom -> red break, per column.
# Use measured anchors: x470 fascia 431-449 ; x600 426-444 ; x860 415-434 ; x900 413-433
# linear-ish; fit fascia top y as function of x from those four
xs=np.array([470,530,600,860,900]); tops=np.array([431,429,426,415,413])
c=np.polyfit(xs,tops,1)
print('photo fascia top(x) =',c)
rows=[]
for x in range(430,930):
    t=int(round(np.polyval(c,x)))
    rows.append(lum(ph[t+2:t+15, x]))
P=np.array(rows).T   # 13 x N
print('PHOTO fascia   mean %.1f  sd(all) %.2f  sd(column means) %.2f  n=%d'%(P.mean(),P.std(),P.mean(axis=0).std(),P.size))

# RENDER fascia: at x=700 fascia 643-665. find top per column by gold detection
def rend_band(img,x0,x1):
    out=[]
    for x in range(x0,x1):
        col=img[600:700,x]
        L=lum(col)
        # gold = strong r-b
        rb=col[:,0]-col[:,2]
        gi=int(np.argmax(rb[20:60]))+20
        t=600+gi+4
        out.append(lum(img[t:t+13,x]))
    return np.array(out).T
R=rend_band(rn,600,1150)
print('RENDER fascia  mean %.1f  sd(all) %.2f  sd(column means) %.2f  n=%d'%(R.mean(),R.std(),R.mean(axis=0).std(),R.size))

# per-column mean profiles, print a few
print('photo col-mean p5/p50/p95: %.1f %.1f %.1f'%tuple(np.percentile(P.mean(axis=0),[5,50,95])))
print('rend  col-mean p5/p50/p95: %.1f %.1f %.1f'%tuple(np.percentile(R.mean(axis=0),[5,50,95])))
print('photo pixel  p2/p50/p98: %.1f %.1f %.1f'%tuple(np.percentile(P,[2,50,98])))
print('rend  pixel  p2/p50/p98: %.1f %.1f %.1f'%tuple(np.percentile(R,[2,50,98])))

# saturation
def sat(a):
    mx=a.max(axis=-1); mn=a.min(axis=-1)
    return np.where(mx>0,(mx-mn)/np.maximum(mx,1e-6),0)
rowsP=[]
for x in range(430,930):
    t=int(round(np.polyval(c,x))); rowsP.append(ph[t+2:t+15,x])
PC=np.array(rowsP)
print('PHOTO fascia rgb mean',PC.reshape(-1,3).mean(axis=0).round(1),'sat %.3f'%sat(PC.reshape(-1,3)).mean())
rowsR=[]
for x in range(600,1150):
    col=rn[600:700,x]; rb=col[:,0]-col[:,2]; gi=int(np.argmax(rb[20:60]))+20; t=600+gi+4
    rowsR.append(rn[t:t+13,x])
RC=np.array(rowsR)
print('REND  fascia rgb mean',RC.reshape(-1,3).mean(axis=0).round(1),'sat %.3f'%sat(RC.reshape(-1,3)).mean())
