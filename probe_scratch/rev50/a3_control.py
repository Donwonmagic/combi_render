"""rev50 -- THE CONTROL A3 NEVER HAD.

SURVEY_rev49 finding "every duplicated part is a bit-identical clone" rests on a
front-vs-rear wheel high-pass correlation of 0.675-0.708 against a +5 px control
of -0.012, and concludes the WEAR FIELD clones because WEATHER/MOTTLE are fed
Object coordinates.

That statistic cannot separate two hypotheses:
  H1  the TEXTURE clones (the accusation)
  H2  the GEOMETRY is identical -- both wheels are the same revolve at the same
      clock angle, so their images correlate whatever the texture does.
The critic tried to control for this by restricting to the "tyre annulus, which
carries no azimuthally-varying geometry".  That is exactly backwards: geometry
with no azimuthal variation is IDENTICAL at both wheels, so it correlates
perfectly and DOMINATES the statistic.  Rule 29.3: no finding is attributed to a
cause until a control separates it from the other candidates.

THIS SEPARATES THEM.  Resample each wheel into polar (r, theta) about its own hub
and subtract the theta-MEAN at each radius.  That removes every rotationally
symmetric contribution -- the tread grooves, the rim bands, the dome shading,
the vignette -- and leaves only azimuthal content: the vent notches, the VW
glyph, and the wear texture.  Restricted to the TYRE ANNULUS there is no vent
and no glyph, so what is left is texture and render noise alone.

  H1 predicts the annulus residuals still correlate strongly.
  H2 predicts they do not.
"""
import numpy as np
from PIL import Image

PPM = 271.1864                     # side ortho, studio.views()["side"]
def polar(a, cx, cy, r0, r1, nr=90, nt=720):
    H, W = a.shape[:2]
    rr = np.linspace(r0, r1, nr); tt = np.linspace(0, 2*np.pi, nt, endpoint=False)
    R, T = np.meshgrid(rr, tt, indexing="ij")
    xs = np.clip((cx + R*np.cos(T)).astype(int), 0, W-1)
    ys = np.clip((cy + R*np.sin(T)).astype(int), 0, H-1)
    return a[ys, xs]

def resid(p):
    """remove the theta-mean at each radius: kills all rotationally symmetric content"""
    return p - p.mean(axis=1, keepdims=True)

def corr(x, y):
    x = x.ravel() - x.mean(); y = y.ravel() - y.mean()
    d = np.sqrt((x*x).sum() * (y*y).sum())
    return float((x*y).sum()/d) if d > 0 else np.nan

img = np.array(Image.open("out/r50a_side.png").convert("RGB")).astype(float)
lum = img @ np.array([0.2126, 0.7152, 0.0722])

# hub centres: derived from the red dome centroid, not typed
def hub(box):
    x0,y0,x1,y1 = box
    s = img[y0:y1, x0:x1]
    m = (s[:,:,0] > 85) & (s[:,:,1] < 0.70*s[:,:,0])
    ys,xs = np.nonzero(m); return x0+xs.mean(), y0+ys.mean()
FR = hub((380,800,520,940)); RE = hub((1030,800,1170,940))
print(f"front hub {FR[0]:.1f},{FR[1]:.1f}   rear hub {RE[0]:.1f},{RE[1]:.1f}   "
      f"separation {abs(RE[0]-FR[0])/PPM:.4f} m (wheelbase 2.400)")

BANDS = {"tyre annulus (no vent, no glyph)": (0.2400*PPM, 0.3100*PPM),
         "cream rim ring": (0.1500*PPM, 0.2100*PPM),
         "hubcap dome": (0.0300*PPM, 0.1100*PPM)}
print()
print(f"{'band':36} {'RAW corr':>9} {'POLAR-RESIDUAL corr':>21}")
for name,(r0,r1) in BANDS.items():
    pf = polar(lum, *FR, r0, r1); pr = polar(lum, *RE, r0, r1)
    print(f"{name:36} {corr(pf,pr):9.3f} {corr(resid(pf),resid(pr)):21.3f}")

print()
print("CONTROLS")
r0,r1 = BANDS["tyre annulus (no vent, no glyph)"]
pf = polar(lum, *FR, r0, r1); pr = polar(lum, *RE, r0, r1)
rf, rr_ = resid(pf), resid(pr)
print(f"  {'front vs ITSELF rotated 37 deg':44} {corr(rf, np.roll(rf, 74, axis=1)):7.3f}   (expect ~0 if the residual is real azimuthal structure)")
print(f"  {'front vs ITSELF (identity)':44} {corr(rf, rf):7.3f}   (expect 1.000 -- the instrument's ceiling)")
print(f"  {'front vs rear, RAW, shifted +5 px in x':44} "
      f"{corr(polar(lum,FR[0]+5,FR[1],r0,r1), pr):7.3f}   (the survey's own decorrelation control)")
noise = np.random.default_rng(0).normal(0,1,rf.shape)
print(f"  {'front residual vs white noise':44} {corr(rf, noise):7.3f}   (expect ~0)")

# ---------------------------------------------------------------------------
# THE ABOVE FAILED ITS OWN CONTROLS AND IS KEPT AS THE RECORD OF THE FAILURE.
# "front vs itself rotated 37 deg" returned 0.629 where a residual made of fine
# azimuthal structure must return ~0, and the survey's +5 px decorrelation
# control returned 0.914 against their -0.012.  Cause: removing the theta-MEAN
# kills only the m=0 term.  Everything smooth in theta -- the key falloff across
# the wheel, the arch shadow, the tyre's own limb shading -- survives, dominates
# the variance, and correlates with anything similarly smooth, including itself
# rotated.  A residual is not a high-pass.
#
# v2 HIGH-PASSES ALONG THETA before correlating, which is what the survey's 9 px
# box did in image space.  The rotation control is the arbiter.
from scipy.ndimage import uniform_filter1d

def hp(p, k=9):
    """high-pass along theta only: p minus its own running mean over k samples"""
    return p - uniform_filter1d(p, size=k, axis=1, mode="wrap")

print()
print("=== v2: HIGH-PASSED ALONG THETA ===")
for k in (9, 21):
    print(f"  --- theta box = {k} samples ({k*360/720:.1f} deg) ---")
    r0, r1 = BANDS["tyre annulus (no vent, no glyph)"]
    pf = polar(lum, *FR, r0, r1); pr = polar(lum, *RE, r0, r1)
    hf, hr = hp(pf, k), hp(pr, k)
    c_self_rot = corr(hf, np.roll(hf, 74, axis=1))
    print(f"    CONTROL front vs itself rotated 37 deg : {c_self_rot:7.3f}  <- must be ~0 or the instrument is void")
    if abs(c_self_rot) > 0.15:
        print("    -> STILL FAILING ITS CONTROL.  Not reporting a number from it.")
        continue
    print(f"    CONTROL front vs white noise           : {corr(hf, np.random.default_rng(1).normal(0,1,hf.shape)):7.3f}")
    for name,(a0,a1) in BANDS.items():
        pf2 = hp(polar(lum,*FR,a0,a1), k); pr2 = hp(polar(lum,*RE,a0,a1), k)
        print(f"    {name:36} front vs rear: {corr(pf2, pr2):7.3f}")
