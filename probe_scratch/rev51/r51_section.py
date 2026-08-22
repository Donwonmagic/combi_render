"""rev 51 -- the hubcap/rim SECTION, drawn from the two authored profiles in
t1_detail.py. This is a PICTURE OF THE SOURCE, not a measurement."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np

S = 0.2198/0.1905
cap = [(0.0745,0.0000),(0.0736,0.0300),(0.0710,0.0560),(0.0664,0.0800),(0.0596,0.1010),
       (0.0502,0.1180),(0.0378,0.1288),(0.0236,0.1342),(0.0120,0.1345),(0.0040,0.1370)]
disc= [(0.0470,0.0000),(0.0450,0.0400),(0.0430,0.0620),(0.0450,0.0900),(0.0520,0.1200),
       (0.0570,0.1400),(0.0560,0.1560),(0.0500,0.1600)]
disc= [(y, r*S) for (y,r) in disc]
barrel=[(0.0600,0.1905),(0.0640,0.1885),(0.0625,0.1820),(0.0560,0.1795),(0.0520,0.1720),
        (0.0480,0.1660),(0.0300,0.1640),(0.0080,0.1650)]
barrel=[(y, r*S) for (y,r) in barrel]

W,H = 1560, 900
PX = 4200.0
OX, OY = 150, 700
im = Image.new('RGB',(W,H),(255,255,255)); d = ImageDraw.Draw(im)
def P(r,y): return (OX + r*PX, OY - y*PX)
def f(sz, bold=False):
    n = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/"+n, sz)
    except: return ImageFont.load_default()
F, FB, FS = f(17), f(19, True), f(15)

d.text((30, 22), "THE HUBCAP SECTION, drawn from the two profiles in t1_detail.py", fill=(0,0,0), font=f(22, True))
d.text((30, 50), "A picture of the source. Nothing is measured here.", fill=(90,90,90), font=F)

# --- axes
d.line([P(0,0), P(0.238,0)], fill=(205,205,205), width=1)
d.line([P(0,-0.004), P(0,0.150)], fill=(205,205,205), width=1)
for rr in (0.05,0.10,0.15,0.20):
    d.line([P(rr,-0.0035), P(rr,0.0035)], fill=(170,170,170))
    d.text((P(rr,0)[0]-20, P(rr,0)[1]+9), "%.2f"%rr, fill=(130,130,130), font=FS)
d.text((P(0.043,0)[0], P(0.043,0)[1]+34), "radius r, metres  ->", fill=(130,130,130), font=FS)
d.text((OX-118, 118), "outboard y", fill=(130,130,130), font=FS)

# --- the three surfaces
d.line([P(r,y) for (y,r) in disc],   fill=(214,150,38), width=6)
d.line([P(r,y) for (y,r) in barrel], fill=(150,150,150), width=6)
d.line([P(r,y) for (y,r) in cap],    fill=(198,42,38),   width=6)
d.text((P(0.012,0.0790)[0], P(0.012,0.0790)[1]-26), "hubcap()  -- RED cap", fill=(198,42,38), font=FB)
d.text((P(0.030,0.0430)[0], P(0.030,0.0430)[1]+12), "rim()'s disc_prof -- CREAM disc", fill=(190,132,30), font=FB)
d.text((P(0.196,0.0180)[0]-40, P(0.196,0.0180)[1]), "barrel", fill=(140,140,140), font=F)

# --- crossover marker
XR = 0.11973
yc = float(np.interp(XR, [c[1] for c in cap], [c[0] for c in cap]))
cxp = P(XR,yc)
d.ellipse([cxp[0]-9, cxp[1]-9, cxp[0]+9, cxp[1]+9], outline=(0,0,0), width=3)
# callout into the empty upper-left
bx, by = 300, 120
d.line([cxp, (bx+250, by+96)], fill=(0,0,0), width=2)
d.rectangle([bx-12, by-10, bx+700, by+104], outline=(0,0,0), width=2, fill=(252,252,252))
d.text((bx, by),      "CROSSOVER   r = 0.11973 m", fill=(0,0,0), font=FB)
d.text((bx, by+26),   "Outboard of here the CREAM DISC is in front of the RED CAP.", fill=(0,0,0), font=F)
d.text((bx, by+48),   "The five vent holes are cut through the disc across this radius,", fill=(0,0,0), font=F)
d.text((bx, by+70),   "so each looks THROUGH the cream onto red  ->  FIVE RED PETALS.", fill=(0,0,0), font=F)

# --- vent spans, drawn just under the profiles, clear of the axis labels
yv1, yv2 = 0.0175, 0.0075
d.line([P(0.0945,yv1), P(0.1345,yv1)], fill=(168,52,150), width=7)
d.text((P(0.0945,yv1)[0]-292, P(0.0945,yv1)[1]-10), "vent span UNDER the cap", fill=(168,52,150), font=F)
d.line([P(0.1345,yv2), P(0.1415,yv2)], fill=(25,25,25), width=7)
d.line([P(0.1380,yv2), (P(0.1380,yv2)[0]+150, P(0.1380,yv2)[1]+92)], fill=(25,25,25), width=2)
d.text((P(0.1380,yv2)[0]+156, P(0.1380,yv2)[1]+84),
       "7.0 mm of vent OUTSIDE the cap  ->  five DARK NOTCHES", fill=(25,25,25), font=F)
d.text((P(0.1380,yv2)[0]+156, P(0.1380,yv2)[1]+106),
       "(known and accepted in rim()'s own comment)", fill=(90,90,90), font=FS)

# --- the two depths that decide the fix, right-hand side, well separated
fy = 0.0640
d.line([P(0.196,fy), P(0.234,fy)], fill=(120,120,120), width=2)
d.text((P(0.208,fy)[0], P(0.208,fy)[1]+7), "flange face  y = 0.0640", fill=(110,110,110), font=FS)
d.line([P(0.150,0.0745), P(0.234,0.0745)], fill=(198,42,38), width=2)
d.text((P(0.208,0.0745)[0], P(0.208,0.0745)[1]-24), "cap apex  y = 0.0745", fill=(198,42,38), font=FS)
d.line([P(0.2015,fy), P(0.2015,0.0745)], fill=(0,0,0), width=4)
d.text((P(0.2015,0.0693)[0]-292, P(0.2015,0.0693)[1]-11), "10.5 mm proud, AS BUILT", fill=(0,0,0), font=FB)

# --- footer
d.line([(30, 800), (W-30, 800)], fill=(210,210,210), width=1)
d.text((30, 816), "DOME DEPTH, apex to lip = 70.5 mm.  A hubcap must seat its lip on the wheel, and seating it forces:", fill=(0,0,0), font=FB)
d.text((30, 842), "proud = dome_depth - (flange_y - disc_at_lip) = 70.5 - (64.0 - 51.7) = 58.2 mm", fill=(0,0,0), font=f(18, True))
d.text((30, 866), "So ~58 mm proud is not a consequence of choosing one fix -- it is forced by the cap's own section.  CAP_R is a RADIUS and does not bound the depth.", fill=(70,70,70), font=FS)
im.save('probe_scratch/rev51/FIG_hubcap_section.png')
print("wrote", im.size)
