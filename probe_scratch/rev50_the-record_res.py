"""rev 50 -- IS ref_playa_34.png's EXTRA RESOLUTION REAL, or is it the same
photograph upsampled?

THE TEST.  ref_source.jpeg is 246 px wide; its Nyquist is 0.5 cycles/source-px
= 0.2460 cycles/playa-px.  If ref_playa_34.png carries real detail the source
copy cannot, its radially-averaged power spectrum must hold significant energy
ABOVE that frequency.  Control: ref_source itself upsampled to 500x400 by
Lanczos, which by construction has NO information above 0.246 c/px -- whatever
it shows there is resampling ringing, and it is the floor the real file must
beat.

CEILING.  A power spectrum cannot tell detail from JPEG/PNG noise.  So the
number reported is the RATIO of the real file's high-band energy to the
upsampled control's, on the SAME crop, and a crop of flat paint is measured
alongside a crop of the nose hardware so noise-only regions can be seen to
score near 1.
"""
import numpy as np
from PIL import Image

src = Image.open('ref_source.jpeg').convert('L')
pla = Image.open('ref_playa_34.png').convert('L')
ctl = src.resize((500, 400), Image.LANCZOS)

def band(im, box):
    a = np.asarray(im.crop(box), float)
    a = a - a.mean()
    w = np.outer(np.hanning(a.shape[0]), np.hanning(a.shape[1]))
    F = np.abs(np.fft.fftshift(np.fft.fft2(a * w)))**2
    ny, nx = a.shape
    fy = np.fft.fftshift(np.fft.fftfreq(ny))[:, None]
    fx = np.fft.fftshift(np.fft.fftfreq(nx))[None, :]
    r = np.sqrt(fy**2 + fx**2)
    lo = F[(r > 0.02) & (r <= 0.2460)].sum()
    hi = F[(r > 0.2460) & (r <= 0.48)].sum()
    return lo, hi

CROPS = {
    "nose hardware (roundel+lamp+indicator)": (20, 190, 180, 300),
    "flank folk art":                          (300, 330, 460, 440),
    "flat cream roof (near-featureless)":      (200, 150, 330, 200),
    "whole frame":                             (0, 0, 500, 400),
}
print("%-40s %10s %10s %8s" % ("crop", "hi/lo real", "hi/lo ctl", "ratio"))
for nm, box in CROPS.items():
    lo1, hi1 = band(pla, box)
    lo2, hi2 = band(ctl, box)
    r1, r2 = hi1/lo1, hi2/lo2
    print("%-40s %10.4f %10.4f %8.2fx" % (nm, r1, r2, r1/r2))
