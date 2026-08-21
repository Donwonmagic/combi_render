"""rev49 -- (i) THE WIDTH ACROSS THE VEHICLE.  Confirm or refute 'completely unmeasured'.

The board's plane contains the LATERAL (+Y, depth) direction -- that is what makes it
read as a near-edge-on sliver in a broadside frame at all.  So its width across the
vehicle projects ONLY through parallax: a point moved W metres away from the camera
images RADIALLY INWARD toward the principal point by roughly |p - p0| * W / D.
Only the component PERPENDICULAR to the board's own axis widens the silhouette.
"""
import math
p0=(512.,384.)                      # principal point = image centre (LOFT sec.0.2 shows
                                    # the rectification is invariant to it over +-100 px)
D=4.9                               # camera -> near flank, LOFT_GROUND_rev15 sec.1.1
BASE,TIP=(888.,293.5),(1015.5,191.5)
ax=(TIP[0]-BASE[0],TIP[1]-BASE[1]); n=math.hypot(*ax); ax=(ax[0]/n,ax[1]/n)
perp=(-ax[1],ax[0])
print(__doc__)
for nm,pt in (("base",BASE),("tip",TIP)):
    r=(p0[0]-pt[0],p0[1]-pt[1]); rn=math.hypot(*r); rh=(r[0]/rn,r[1]/rn)
    c=abs(rh[0]*perp[0]+rh[1]*perp[1])
    print("  %-5s |p-p0| = %6.1f px   perpendicular parallax = %.1f px per metre of width"
          %(nm,rn,rn/D*c))
K=(math.hypot(p0[0]-TIP[0],p0[1]-TIP[1])/D
   *abs(((p0[0]-TIP[0])/math.hypot(p0[0]-TIP[0],p0[1]-TIP[1]))*perp[0]
        +((p0[1]-TIP[1])/math.hypot(p0[0]-TIP[0],p0[1]-TIP[1]))*perp[1]))
print("\n  the coefficient is the same at both ends (%.1f px/m) -- it is a cross product,"%K)
print("  so the projected width does NOT taper along the board.  OBSERVED perpendicular")
print("  extent DOES: 19.9 px near the base, 8.4 px median, 7.2 px over the last 40 columns.")
print("  => the silhouette's thickness is NOT purely projected width.  It also carries the")
print("     board's own material thickness (t metres reads ~%.0f*t px, near face-on) and its"%(219*math.cos(math.radians(10.4))))
print("     painted border bands.  Those cannot be separated at 1024 px.")
print("\n  UPPER BOUND (the only side that is safe):  W <= max perpendicular extent / %.1f"%K)
for T,lab in ((19.9,"largest anywhere on the board"),(8.4,"median"),(7.2,"tip half")):
    print("     %-30s %4.1f px  ->  W <= %.2f m"%(lab,T,T/K))
print("  With D swept 4.4 -> 5.5 m the 19.9 px bound moves %.2f -> %.2f m."
      %(19.9/(K*4.9/4.4),19.9/(K*4.9/5.5)))
print("\n  VERDICT on 'completely unmeasured':")
print("   * ref_side.jpg CANNOT measure it -- correct.  It bounds it: W <= 0.55 +- 0.06 m,")
print("     with NO lower bound (t and the border bands can account for all 7-8 px).")
print("     That bound alone REFUTES a full-width board: the roof aperture is 1.11 m across")
print("     (t1_shell.LID_W) and the body 1.750 m; both are excluded at >2x.")
print("   * ref_rear34.jpg sees the tail obliquely, but (a) the board's far end runs off the")
print("     RIGHT FRAME EDGE at u=1199 -- checked column by column, the trim is still there")
print("     in the last column -- and (b) SPEC 10.48 admits px/m on that frame ONLY on the")
print("     PLATE plane (344.1 +- 6.7), and the plate's own frame in it reads 303 px/m across")
print("     against 386 px/m up, so the tail face is obliquely foreshortened by an unmeasured")
print("     factor.  No metre figure is admissible there and none is taken.")
print("   * IMG_2073 / ref_workshop are the GREEN bus.  Geometry transfers (rule 26), but")
print("     neither shows a raised tail board at all -- so they cannot supply it either.")
