import numpy as np
exec(open('/home/user/combi_render/probe_scratch/rev50a_vp4.py').read().split("print(\"===========")[0])

def track2(ch,rows,x_seed,slope,half,sign,label,minstep=12.0):
    a,b=slope,x_seed-slope*rows[len(rows)//2]
    for it in range(7):
        pts=[]
        for r in rows:
            e=edge_row(ch,r,a*r+b,half,sign,minstep)
            if e is not None: pts.append((r,e))
        ys=np.array([p[0] for p in pts],float); xs=np.array([p[1] for p in pts])
        p=np.polyfit(ys,xs,1); res=xs-np.polyval(p,ys); s=res.std()
        k=np.abs(res)<2.0*max(s,0.4); p=np.polyfit(ys[k],xs[k],1); a,b=p; half=max(3.5,half*0.72)
    q=np.polyfit(ys[k],xs[k],2)
    yr=ys[k]; span=yr.max()-yr.min()
    bow=q[0]*(span/2.0)**2   # sagitta of the quadratic over the fitted span
    print("%-26s n=%3d slope=%+.5f  rms=%.2f  QUAD sagitta=%+.2f px over %d rows"%(
        label,int(k.sum()),p[0],(xs[k]-np.polyval(p,ys[k])).std(),bow,span))
    return p

print("=== straightness / distortion check (quadratic sagitta) ===")
track2(Y,list(range(10,470)),52.,0.03,7,+1,"lamppost LEFT")
track2(Y,list(range(10,470)),74.,0.03,7,-1,"lamppost RIGHT")
track2(Y,list(range(8,250)),771.,0.005,8,-1,"column LEFT")
track2(YEL,list(range(48,258)),313.,0.155,12,+1,"board fore OUTER")
track2(YEL,list(range(30,262)),741.,0.057,12,-1,"board aft OUTER")

print("\n=== more verticals: background doorway / wall / bus pillars ===")
cands=[(Y,range(180,300),808.,0.01,7,+1,"dark doorway L jamb ~x808"),
       (Y,range(180,290),905.,0.01,7,-1,"dark doorway R jamb ~x905"),
       (Y,range(300,395),437.,0.01,5,+1,"bay pillar ~x437"),
       (Y,range(300,395),563.,0.01,5,+1,"bay pillar ~x563"),
       (Y,range(300,395),690.,0.01,5,+1,"bay pillar ~x690"),
       ]
for ch,rows,xs_,sl,hf,sg,lab in cands:
    try: track2(ch,list(rows),xs_,sl,hf,sg,lab,8.0)
    except Exception as e: print(lab,"fail",e)
