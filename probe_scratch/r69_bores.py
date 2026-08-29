# rev 69 -- THE HEADLAMP BORES AS A PLAN-CURVATURE INSTRUMENT.  Ground step.
#
# THE IDEA.  A T1's headlamp sits in a bowl PRESSED INTO the front panel, and
# its chrome rim lies in the panel's local TANGENT plane -- so the rim's axis is
# the panel's local NORMAL.  On a nose that is curved in plan the two rims
# therefore SPLAY apart by twice the plan slope at |y| = HL_Y.  On a nose that
# is flat in plan they are PARALLEL.
#
# WHY THIS BEATS THE BUMPER-EDGE ROUTE.  It is a DIFFERENTIAL measurement
# between two features in ONE frame, so the camera's focal length, its distance,
# its elevation and its roll are common-mode and cancel to first order.  The
# bumper sagitta needed all of them and F221 got them wrong.
#
# WHAT IT REQUIRES OF THE FRAME: both bores unoccluded.
#   ref_workshop.jpg  -- YES.  Bare shell, bores EMPTY (no lamps fitted), so the
#                        rim is a clean hole edge and not a chrome highlight.
#   IMG_2073.jpeg     -- NO.  A PALM TRUNK occludes the far side.  F223's claim
#                        that both frames show both bores is FALSE for this one.
#
# RULE 8: THE WINDOW IS PART OF THE MEASUREMENT.  Nothing here prints a number
# before the fit is painted and looked at.
import os, sys
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRATCH = os.path.join(HERE, "probe_scratch")


def fit_ellipse(pts):
    """Direct least-squares conic fit.  Returns (cx, cy, a, b, theta) or None.

    a is the SEMI-MAJOR axis, b the SEMI-MINOR, theta the major axis angle in
    image coordinates (radians, x right, y down)."""
    x = pts[:, 0].astype(float)
    y = pts[:, 1].astype(float)
    mx, my = x.mean(), y.mean()
    s = max(x.std(), y.std())
    if s <= 0:
        return None
    x = (x - mx) / s
    y = (y - my) / s
    D = np.column_stack([x * x, x * y, y * y, x, y, np.ones_like(x)])
    _, _, V = np.linalg.svd(D, full_matrices=False)
    A, B, C, Dc, E, F = V[-1]
    disc = B * B - 4 * A * C
    if disc >= 0:                      # not an ellipse
        return None
    cx = (2 * C * Dc - B * E) / disc
    cy = (2 * A * E - B * Dc) / disc
    num = 2 * (A * E * E + C * Dc * Dc + F * B * B - B * Dc * E - 4 * A * C * F)
    r1 = num / (disc * ((C - A) * np.hypot(1, B / (C - A + 1e-30)) - (A + C))) \
        if abs(C - A) > 1e-12 else None
    # robust axis extraction via the quadratic form's eigenvalues
    M = np.array([[A, B / 2], [B / 2, C]])
    off = A * cx * cx + B * cx * cy + C * cy * cy + Dc * cx + E * cy + F
    w, vec = np.linalg.eigh(M)
    if np.any(w * (-off) <= 0):
        return None
    ax = np.sqrt(-off / w)             # semi-axes along the eigenvectors
    order = np.argsort(-ax)            # major first
    a, b = ax[order[0]], ax[order[1]]
    v_major = vec[:, order[0]]
    theta = float(np.arctan2(v_major[1], v_major[0]))
    return (cx * s + mx, cy * s + my, a * s, b * s, theta)


def bore_edge(img, box, mode="bore"):
    """Sub-pixel-ish rim points of ONE bore.

    SEGMENTED ON CHROMA, NOT ON DARKNESS -- AND THAT CORRECTION WAS FORCED BY
    PAINTING THE FIRST VERSION AND LOOKING AT IT (rule 8).

    My first cut thresholded on LUMA, on the reasoning that "a hole is dark".
    It is not.  Painted, the near bore's interior is DARK IN ITS UPPER HALF AND
    LIT IN ITS LOWER HALF -- so the dark blob was a CRESCENT of shadow inside
    the bore, and the ellipse fitted to it was smaller and differently tilted
    than the aperture.  The far bore's interior is LIGHT GREY throughout, so the
    dark blob there was not the bore at all: it latched onto background above
    and left of it, and returned b/a 0.2429, a number that looked like a
    measurement.  Neither error is detectable from the number.

    WHAT ACTUALLY SEPARATES THEM: the panel is GREEN PAINT and the bore interior
    is BARE/GREY, at every interior brightness.  So the test is saturation, not
    level -- `g` above both `r` and `b` marks paint; everything else in the box
    is aperture."""
    x0, y0, x1, y1 = box
    a = np.asarray(img.convert("RGB")).astype(float)[y0:y1, x0:x1]
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    if mode == "bore":
        # green paint: g clearly above the mean of r and b.  Bore: not that.
        sig = g - 0.5 * (r + b)
        thr = 0.5 * (np.percentile(sig, 10) + np.percentile(sig, 90))
        m = sig < thr
    else:
        # the roundel is a DARK CHROME ring on CREAM -- separate on luma.  Its
        # OUTER edge is the circle we want, and hole-filling above turns the
        # ring into the filled disc it bounds.
        sig = 0.299 * r + 0.587 * g + 0.114 * b
        thr = 0.5 * (np.percentile(sig, 8) + np.percentile(sig, 92))
        m = sig < thr
    # largest connected component, 4-connected flood
    lab = np.zeros(m.shape, int)
    cur = 0
    best, bestn = None, 0
    for j in range(m.shape[0]):
        for i in range(m.shape[1]):
            if m[j, i] and lab[j, i] == 0:
                cur += 1
                stack = [(j, i)]
                lab[j, i] = cur
                n = 0
                while stack:
                    cj, ci = stack.pop()
                    n += 1
                    for dj, di in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nj, ni = cj + dj, ci + di
                        if 0 <= nj < m.shape[0] and 0 <= ni < m.shape[1] \
                                and m[nj, ni] and lab[nj, ni] == 0:
                            lab[nj, ni] = cur
                            stack.append((nj, ni))
                if n > bestn:
                    bestn, best = n, cur
    if best is None:
        return None, None
    blob = lab == best
    # FILL INTERIOR HOLES FIRST.  Painted and looked at: the near bore's
    # interior is JPEG-blocked and speckles into dozens of tiny non-blob
    # islands, every one of which contributed EDGE points to the conic fit and
    # pulled the major axis 31 deg off vertical.  Only the OUTER rim is the
    # aperture.  Flood the complement from the border; whatever the flood cannot
    # reach is interior and is filled.
    comp = ~blob
    reach = np.zeros_like(comp)
    st = [(j, i) for j in range(comp.shape[0]) for i in (0, comp.shape[1] - 1) if comp[j, i]]
    st += [(j, i) for i in range(comp.shape[1]) for j in (0, comp.shape[0] - 1) if comp[j, i]]
    for j, i in st:
        reach[j, i] = True
    st = list(st)
    while st:
        cj, ci = st.pop()
        for dj, di in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nj, ni = cj + dj, ci + di
            if 0 <= nj < comp.shape[0] and 0 <= ni < comp.shape[1] \
                    and comp[nj, ni] and not reach[nj, ni]:
                reach[nj, ni] = True
                st.append((nj, ni))
    blob = blob | (comp & ~reach)
    # boundary = blob pixels with a non-blob 4-neighbour
    pad = np.pad(blob, 1)
    edge = blob & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    ys, xs = np.nonzero(edge)
    return np.column_stack([xs + x0, ys + y0]), bestn


def main():
    frame = sys.argv[1] if len(sys.argv) > 1 else "ref_workshop.jpg"
    # boxes located BY LOOKING at probe_scratch/r69_ws_nose.png first
    BOXES = {
        # ROUNDEL first: it is the REFERENCE, not a third bore.  It is centred
        # on the vehicle's plane of symmetry, so the panel normal there is the
        # x-axis EXACTLY -- not by assumption, by symmetry.  Everything else is
        # measured as a DIFFERENCE from it, in the same frame, a few hundred
        # pixels away, so focal length, distance, elevation, roll and lens
        # distortion are common-mode.
        "ref_workshop.jpg": {"roundel": (264, 494, 350, 598),
                             "near": (376, 578, 466, 668)},
    }
    boxes = BOXES.get(os.path.basename(frame))
    if boxes is None:
        print("NO BOXES for %s -- the window must be located and LOOKED AT "
              "before anything is measured (rule 8).  Nothing measured." % frame)
        return 2
    img = Image.open(os.path.join(HERE, frame)).convert("RGB")
    paint = img.copy()
    d = ImageDraw.Draw(paint)
    out = {}
    for tag, box in boxes.items():
        pts, n = bore_edge(img, box, "roundel" if tag == "roundel" else "bore")
        d.rectangle(box, outline=(0, 200, 255), width=1)
        if pts is None or len(pts) < 12:
            print("  %-5s NO RIM FOUND in %s -- nothing measured" % (tag, box))
            continue
        for px, py in pts:
            d.point((int(px), int(py)), fill=(255, 0, 255))
        e = fit_ellipse(pts)
        if e is None:
            print("  %-5s rim found (%d px) but the conic is NOT an ellipse -- "
                  "nothing measured" % (tag, len(pts)))
            continue
        cx, cy, a, b, th = e
        out[tag] = e
        # draw the fitted ellipse
        poly = [(cx + a * np.cos(t) * np.cos(th) - b * np.sin(t) * np.sin(th),
                 cy + a * np.cos(t) * np.sin(th) + b * np.sin(t) * np.cos(th))
                for t in np.linspace(0, 2 * np.pi, 180)]
        d.line(poly + [poly[0]], fill=(0, 255, 0), width=1)
        d.line([(cx - a * np.cos(th), cy - a * np.sin(th)),
                (cx + a * np.cos(th), cy + a * np.sin(th))], fill=(255, 220, 0), width=1)
        print("  %-5s blob %5d px  rim %4d px | centre (%7.2f,%7.2f)  "
              "a %6.2f  b %6.2f  b/a %.4f  major %+6.2f deg"
              % (tag, n, len(pts), cx, cy, a, b, b / a, np.degrees(th)))
    p = os.path.join(SCRATCH, "r69_bores_%s.png" % os.path.basename(frame).split(".")[0])
    paint.save(p)
    print("  painted -> %s   LOOK AT IT BEFORE BELIEVING ANY NUMBER ABOVE" % p)
    if "roundel" in out and "near" in out:
        import math
        rr, nb = out["roundel"], out["near"]
        # b/a = cos(phi), phi = angle between the circle's own normal and the
        # viewing ray.  The roundel's normal IS the x-axis (symmetry), so the
        # DIFFERENCE is the panel's plan slope at the lamp station.
        phi_r = math.degrees(math.acos(min(1.0, rr[3] / rr[2])))
        phi_n = math.degrees(math.acos(min(1.0, nb[3] / nb[2])))
        d = phi_r - phi_n
        print("\n  ROUNDEL  b/a %.4f -> phi %5.2f deg   (its normal IS the x-axis, by symmetry)"
              % (rr[3] / rr[2], phi_r))
        print("  NEAR BORE b/a %.4f -> phi %5.2f deg   (|y| = HL_Y = 0.5450)"
              % (nb[3] / nb[2], phi_n))
        print("  PLAN SLOPE at the lamp station = %+.2f deg" % d)
        sl = math.tan(math.radians(abs(d)))
        # x(y) = x0 + B(1 - (y/0.70)^2)  ->  dx/dy = -2 B y / 0.70^2
        B = sl * 0.70 ** 2 / (2 * 0.5450)
        print("  -> B = %.1f mm  under x(y) = x0 + B(1 - (y/0.70)^2)" % (1000 * B))
        print("\n  ** NOT A RESULT YET.  This must be run on a RENDER of the model,")
        print("     whose bores are cut along (-1,0,0) and whose roundel is draped")
        print("     flat -- so the KNOWN ANSWER there is 0.00 deg.  If it does not")
        print("     read ~0 on the model, the instrument is wrong, not the bus.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
