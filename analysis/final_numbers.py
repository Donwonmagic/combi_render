import numpy as np
S=211.21; XR=749.6; GY=668.0; MB=-0.0385; MAX_=-0.00868
X0=(242.7+749.6)/2.0
def yref(x,y): return y - MB*(x-XR)
def H(x,y): return (GY-yref(x,y))/S           # height above ground at rear-axle station
def Hg(x,y): return (GY+MAX_*(x-XR)-y)/S      # true height above ground at that x (non-body items)
def MX(x): return (X0-x)/S
def m(px): return px/S
FB=65.0; TAIL=920.0; L=TAIL-FB
def frac(x): return (x-FB)/L
print(f"scale S={S:.2f} px/m  ({1000/S:.3f} mm/px); mid-wheelbase x0={X0:.2f}")
print(f"overall length {L:.0f}px = {m(L):.3f} m")
items=[("aperture1 front",323),("aperture1 rear",430),("aperture2 front",455),("aperture2 rear",564),
       ("aperture3 front",588),("aperture3 rear",699),("rear corner panel aft edge",920),
       ("cab door rear shutline",296),("counter front end",302),("counter rear end",986),
       ("rear arch front",652),("rear arch rear",853),("louvre block front",765),("louvre block rear",855),
       ("front hub",242.7),("rear hub",749.6),("front bumper face",65),("roof rear edge",897)]
for n,x in items:
    print(f"  {n:28s} x_img={x:6.1f}  from_front={m(x-FB):6.3f} m  frac={frac(x):6.3f}  model_x={MX(x):+7.3f} m")
print()
hs=[("window head",643.5,309.4-0.0),("window sill(mean)",749.6,392.0),("body two-tone break (cab door)",749.6,413.1),
    ("counter gold nosing",749.6,416.8),("counter fascia bottom / visible cream-red",749.6,439.45),
    ("rocker bottom",749.6,594.4),("rear arch lip apex",749.6,525.0),("roof crown",749.6,254.1),
    ("drip-rail/body top",749.6,297.2),("louvre top",749.6,454.0),("louvre bottom",749.6,493.9)]
for n,x,y in hs:
    print(f"  {n:42s} yref={y:7.2f}  height={H(x,y):.4f} m")
print()
print("window band height", m(392.0-306.8))
print("break below sill (body)", m(413.1-392.0), " (visible cream/red)", m(439.45-392.0))
print("gold nosing below sill", m(416.8-392.0))
print("counter fascia depth", m(439.45-416.8))
print()
print("front bumper top height", (GY+MAX_*(125-XR)-600)/S, " bottom", (GY+MAX_*(125-XR)-628)/S)
print("tyre radius", (GY-604.0)/S, " OD", 2*(GY-604.0)/S)
print("rim outer D", 92.31/S, " hubcap D", 58.87/S)
print("hubcap/tyre", 58.87/(2*(GY-604.0)), " rim/tyre", 92.31/(2*(GY-604.0)))
print("px/m from wheelbase", (749.6-242.7)/2.400, " from 6.40-15 tyre 0.683m", (2*(GY-604.0))/0.683)
print("aperture widths m:", m(430-323), m(564-455), m(699-588))
print("pillars m:", m(455-430), m(588-564), m(323-296))
print("rear corner panel width", m(920-699), "frac", (920-699)/L)
print("counter length", m(986-302), " overhang past tail", m(986-920))
print("rear arch opening width", m(853-652), " centre x_img", (853+652)/2, "model", MX((853+652)/2))
print("louvre block: len", m(855-765), " height", m(493.9-454.0))
print("body pitch: slope diff", MB-MAX_, "=", np.degrees(np.arctan(abs(MB-MAX_))), "deg;  drop over wheelbase", m((MB-MAX_)*-506.9))
