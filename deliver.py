# deliver.py -- BUILD THE PROMOTIONAL ASSET PACKAGE FROM AN RGBA RENDER SET.
#
# WHY THIS FILE EXISTS.  The owner ruled at rev 62:
#
#     "this is just the render to plug into company merch with different
#      backgrounds once i determine the model is done"
#     "It is going on different backgrounds for promotional material etc.
#      give me everything I might need"
#
# F155 recorded the consequence: THE WHITE CYCLORAMA IS SCAFFOLDING, NOT THE
# DELIVERABLE.  For sixty-two revisions every frame this project shipped had the
# backdrop baked into it by `composite_on_white`'s AlphaOver, which -- as
# `matte_tap.__doc__` records in terms -- leaves an alpha channel that is 1
# everywhere and carries no silhouette.  Those frames cannot go on a background.
#
# WHAT MAKES THIS WORK, AND IT IS NOT "TURN THE BACKGROUND OFF".  The contact
# shadow lives in PARTIAL ALPHA, not in grey pixels (see studio.composite_on_white,
# the T1_SHADOW block).  Rendered with T1_ALPHA=1 the film keeps that alpha, so
# the shadow composites CORRECTLY OVER ANY COLOUR: measured on the proof frame,
# the shadow pixels carry RGB (0.9, 0.8, 0.7) out of 255 at a mean alpha of
# 0.813, so they darken whatever is behind them instead of laying grey on it.
# Baked on white it would only ever have been right on white.
#
# THE THREE LAYERS, AND WHY THE SPLIT IS SOUND.  A designer needs the shadow
# separable -- to soften it, move it, or drop it onto a photographic background
# that has its own lighting.  The split is made on a MEASURED discriminator, not
# a guess: shadow-catcher pixels are near-black (max channel < 12/255) while the
# vehicle's are not (mean 143).  Verified on the proof frame: the two classes
# partition the footprint 37.8 / 62.2 %, the vehicle side is 97.1 % fully opaque
# and 99.99 % ONE connected component, and the shadow side has a mean luminance
# of 0.08.  C1..C4 below re-assert all of that on every frame processed, and the
# script REFUSES rather than shipping a package it cannot verify.
#
# WHAT IS DELIBERATELY *NOT* APPLIED, because the compositor must own it:
# chromatic aberration, vignette and grain.  See the T1_ALPHA branch in
# studio.py for the argument -- in short, all three are properties of the FINAL
# image, and a vignette that darkens the corners of transparency or grain that
# stops dead at the silhouette is a visible tell.
#
# BIT DEPTH, STATED BECAUSE THE RECORD HAS A FINDING ABOUT EXACTLY THIS.  The
# masters in out/ are genuine 16-bit RGBA PNGs -- IHDR bit depth 16, colour
# type 6, checked by reading the header, not by asking PIL.  This script reads
# them through PIL, which returns uint8 for 16-bit RGBA, so everything it writes
# is 8-bit.  THAT IS F42's MECHANISM ON A NEW PATH, and here it is a DELIBERATE
# CHOICE rather than F42's accident: 8-bit sRGB is what design tools expect and
# 16-bit RGBA PNG breaks several of them.  The distinction matters -- F42 is a
# measurement path silently losing precision; this is a delivery path choosing a
# format.  Do not "fix" this one by pointing it at a 16-bit decoder without
# asking the owner what his tools take.
#
# RUN   python3 deliver.py [--prefix deliv] [--outdir delivery]

import os
import sys
import zipfile

import numpy as np
import scipy.ndimage as ndi
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))

# view name -> (file stem a non-technical reader can use, one-line description)
VIEWS = {
    "hero":     ("hero_three_quarter",
                 "The hero angle. Front three-quarter, long lens, shallow depth "
                 "of field. Use this one if you only use one."),
    "hero34f":  ("front_three_quarter",
                 "Front three-quarter from higher up -- shows the nose, the "
                 "cab doors and the roof lids together."),
    "hero34r":  ("rear_three_quarter",
                 "Rear three-quarter -- the SERVING side. Shows the counter, "
                 "the open lids and the mural board."),
    "side":     ("side_elevation",
                 "Flat side elevation, near-orthographic. The signage reads "
                 "straight. Best for banners, letterheads and anything where "
                 "the vehicle sits in a strip."),
    "front":    ("front_elevation",
                 "Flat front elevation. Symmetrical -- good for centred "
                 "layouts, stickers and icons."),
    "rear":     ("rear_elevation",
                 "Flat rear elevation."),
}

ARGS = sys.argv[1:]


def _opt(name, default):
    return ARGS[ARGS.index(name) + 1] if name in ARGS else default


PFX = _opt("--prefix", "deliv")
WEB_EDGE = int(_opt("--web-edge", "1400"))
OUTDIR = os.path.join(HERE, _opt("--outdir", "delivery"))
SRC = os.path.join(HERE, "out")

CTL = {}


def ctl(name, ok, msg):
    CTL[name] = bool(ok)
    print("  [%s] %-4s %s" % ("PASS" if ok else "FAIL", name, msg))


def split(a):
    """(vehicle_rgba, shadow_rgba, stats).  The discriminator is MEASURED --
    see the header.  Shadow-catcher pixels are near-black; the vehicle's are
    not."""
    rgb, al = a[..., :3], a[..., 3] / 255.0
    lum = rgb.max(axis=2)
    foot = al > 0.002
    shadow = foot & (lum < 12)
    vehicle = foot & ~shadow

    veh = np.zeros_like(a)
    veh[..., :3] = rgb
    veh[..., 3] = np.where(vehicle, a[..., 3], 0)

    sha = np.zeros_like(a)
    sha[..., :3] = rgb                      # near-black by construction
    sha[..., 3] = np.where(shadow, a[..., 3], 0)

    lab, n = ndi.label(vehicle)
    sz = np.bincount(lab.ravel())[1:] if n else np.array([0])
    return veh, sha, dict(
        foot=int(foot.sum()), shadow=int(shadow.sum()),
        vehicle=int(vehicle.sum()),
        veh_opaque=float((al[vehicle] >= 0.996).mean()) if vehicle.any() else 0.0,
        veh_biggest=float(sz.max() / max(vehicle.sum(), 1)),
        sha_lum=float(lum[shadow].mean()) if shadow.any() else 0.0,
        veh_lum=float(lum[vehicle].mean()) if vehicle.any() else 0.0)


def trim(a):
    ys, xs = np.nonzero(a[..., 3] > 0)
    if not len(ys):
        return a, (0, 0, 0, 0)
    b = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
    return a[b[1]:b[3], b[0]:b[2]], b


def save(a, path):
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA").save(
        path, optimize=True)
    return os.path.getsize(path)


def main():
    frames = [(v, os.path.join(SRC, "%s_%s.png" % (PFX, v))) for v in VIEWS]
    have = [(v, p) for v, p in frames if os.path.exists(p)]
    missing = [v for v, p in frames if not os.path.exists(p)]
    if not have:
        print("NO RENDER: nothing matching %s_*.png in out/.  Render with "
              "T1_ALPHA=1 first (rule 37)." % PFX)
        return 2
    if missing:
        print("  NOTE: %d view(s) not yet rendered and therefore NOT in this "
              "package: %s" % (len(missing), ", ".join(missing)))

    os.makedirs(OUTDIR, exist_ok=True)
    for sub in ("full_frame", "trimmed", "layers", "web"):
        os.makedirs(os.path.join(OUTDIR, sub), exist_ok=True)

    print("\n  BUILDING THE PACKAGE -- %d view(s) from %s_*.png\n" % (len(have), PFX))
    print("  %-20s %10s %8s %8s %9s %8s"
          % ("view", "size", "footprnt", "shadow%", "veh opaq", "1 blob"))
    rows = []
    bad_alpha, bad_split = [], []
    for v, p in have:
        a = np.array(Image.open(p).convert("RGBA")).astype(float)
        al = a[..., 3]
        uniq = len(np.unique(al))
        if uniq < 16 or (al > 0.5).all():
            bad_alpha.append(v)
        veh, sha, st = split(a)
        if st["veh_opaque"] < 0.90 or st["veh_biggest"] < 0.95 \
                or st["sha_lum"] > 20 or st["veh_lum"] < 40:
            bad_split.append(v)
        stem = VIEWS[v][0]
        save(a,   os.path.join(OUTDIR, "full_frame", "combi_%s.png" % stem))
        save(veh, os.path.join(OUTDIR, "layers", "combi_%s_no_shadow.png" % stem))
        save(sha, os.path.join(OUTDIR, "layers", "combi_%s_shadow_only.png" % stem))
        ta, bb = trim(a)
        save(ta,  os.path.join(OUTDIR, "trimmed", "combi_%s.png" % stem))
        # web/ -- the same trimmed asset at WEB_EDGE px on its longest side.
        # Not a different picture, a different weight class: a 2400 px RGBA PNG
        # is ~9 MB and nobody puts that on a page.  Downscaled with LANCZOS from
        # the full-res frame rather than re-rendered, so it cannot drift from
        # the master.
        wi = Image.fromarray(np.clip(ta, 0, 255).astype(np.uint8), "RGBA")
        sc = WEB_EDGE / float(max(wi.width, wi.height))
        if sc < 1.0:
            wi = wi.resize((max(1, int(wi.width * sc)),
                            max(1, int(wi.height * sc))), Image.LANCZOS)
        wi.save(os.path.join(OUTDIR, "web", "combi_%s_web.png" % stem),
                optimize=True)
        print("  %-20s %10s %8d %7.1f%% %8.3f %8.4f"
              % (stem, "%dx%d" % (a.shape[1], a.shape[0]), st["foot"],
                 100.0 * st["shadow"] / max(st["foot"], 1),
                 st["veh_opaque"], st["veh_biggest"]))
        rows.append((v, stem, a.shape[1], a.shape[0], bb, st))

    ctl("C1", not bad_alpha,
        "every frame carries a REAL alpha channel (>=16 distinct values and "
        "not all-opaque).  This is the check that catches the sixty-two-"
        "revision defect: composite_on_white's AlphaOver leaves alpha == 1 "
        "EVERYWHERE, so a frame can have an alpha channel and no silhouette%s"
        % ("" if not bad_alpha else " -- FAILING ON: " + ", ".join(bad_alpha)))
    ctl("C2", not bad_split,
        "the vehicle/shadow split holds on every frame: vehicle >= 90 %% fully "
        "opaque and >= 95 %% ONE connected component, shadow luminance <= 20, "
        "vehicle luminance >= 40%s"
        % ("" if not bad_split else " -- FAILING ON: " + ", ".join(bad_split)))

    # C3 -- the layers must RECOMBINE to the delivered frame.  A split that
    # loses or duplicates a pixel is not a split.
    worst = 0.0
    for v, p in have:
        a = np.array(Image.open(p).convert("RGBA")).astype(float)
        veh, sha = split(a)[:2]
        recon = veh[..., 3] + sha[..., 3]
        worst = max(worst, float(np.abs(recon - a[..., 3]).max()))
    ctl("C3", worst < 0.5,
        "the two layers RECOMBINE to the delivered alpha exactly (worst "
        "disagreement %.3f of 255) -- a split that loses or duplicates a pixel "
        "is not a split" % worst)

    # C4 -- a KILL.  On a frame with NO alpha the package must refuse, not ship.
    fake = np.zeros((8, 8, 4), float); fake[..., 3] = 255
    fst = split(fake)[2]
    ctl("C4", fst["vehicle"] == 0 or fst["veh_lum"] < 40,
        "KILL: fed an opaque black frame -- what a non-T1_ALPHA render looks "
        "like once its alpha is stripped -- the split does NOT report a valid "
        "vehicle layer, so C2 would refuse it rather than ship a silhouette-"
        "less package")

    manifest(rows, missing)
    contact(rows)

    bad = [k for k, v in CTL.items() if not v]
    print("\n  CONTROLS: %d checked, %s"
          % (len(CTL), ("%d FAILED -- %s" % (len(bad), ",".join(bad))) if bad
             else "0 FAILED"))
    if bad:
        print("\n  PACKAGE IS NOT TRUSTWORTHY -- a failing row is a finding.")
        return 1
    # ONE FILE TO HAND OVER.  The package is four folders and ~50 MB; a person
    # receiving it wants one thing to download, not twenty-five.  Written LAST,
    # and only on a fully-verified package -- a zip of an unverified set is just
    # a tidier way to ship the wrong thing.
    zp = os.path.join(OUTDIR, "combi_promo_pack.zip")
    if os.path.exists(zp):
        os.remove(zp)
    n = 0
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for root, _d, fs in os.walk(OUTDIR):
            for f in sorted(fs):
                fp = os.path.join(root, f)
                if os.path.abspath(fp) == os.path.abspath(zp):
                    continue
                z.write(fp, os.path.relpath(fp, OUTDIR))
                n += 1
    print("  wrote %s  (%d files, %.1f MB)"
          % (os.path.relpath(zp, HERE), n, os.path.getsize(zp) / 1e6))

    print("\n  -> %s" % os.path.relpath(OUTDIR, HERE))
    return 0


def manifest(rows, missing):
    p = os.path.join(OUTDIR, "READ_ME_FIRST.txt")
    L = []
    A = L.append
    A("SENOR TACOMBI COMBI -- PROMOTIONAL ASSET PACKAGE")
    A("=" * 72)
    A("")
    A("Every image here has a TRANSPARENT BACKGROUND. Drop them straight onto")
    A("any colour, photograph or texture.")
    A("")
    A("WHAT IS IN EACH FOLDER")
    A("-" * 72)
    A("full_frame/   All views share one framing and one scale, so you can swap")
    A("              between them in a layout without the vehicle jumping size.")
    A("              Vehicle AND its contact shadow. START HERE.")
    A("")
    A("trimmed/      The same images cropped tight to the artwork. Easier to")
    A("              place and scale by hand. Scale is NOT consistent between")
    A("              views -- use full_frame if that matters.")
    A("")
    A("layers/       For when you want control:")
    A("                *_no_shadow.png    the vehicle alone, nothing under it")
    A("                *_shadow_only.png  the shadow alone")
    A("              Stack shadow under vehicle to rebuild the full image. Drop")
    A("              the shadow's opacity, blur it, or move it, to sit the")
    A("              vehicle on a background that has its own lighting.")
    A("")
    A("web/          The trimmed images resized for screen use -- %d px on the"
      % WEB_EDGE)
    A("              longest side, a fraction of the file size. Same picture,")
    A("              lighter. For anything going on a web page or a deck.")
    A("")
    A("contact_sheet.png   Every view on four backgrounds. Check here first.")
    A("")
    A("THE VIEWS")
    A("-" * 72)
    for v, stem, w, h, bb, st in rows:
        _fp = os.path.join(OUTDIR, "full_frame", "combi_%s.png" % stem)
        _mb = os.path.getsize(_fp) / 1e6 if os.path.exists(_fp) else 0.0
        A("%s  (%d x %d full frame, %.1f MB;  artwork occupies %d x %d of it)"
          % (stem, w, h, _mb, bb[2] - bb[0], bb[3] - bb[1]))
        for line in _wrap(VIEWS[v][1], 68):
            A("    " + line)
        A("")
    if missing:
        A("NOT INCLUDED (not rendered): %s" % ", ".join(missing))
        A("")
    A("TECHNICAL")
    A("-" * 72)
    A("Format        PNG, 8-bit RGBA, straight (un-premultiplied) alpha, sRGB.")
    A("              8-bit is deliberate -- it is what design tools expect, and")
    A("              16-bit RGBA PNG breaks in several of them. The renders")
    A("              behind these ARE 16-bit and are kept; if you ever need")
    A("              that depth for heavy grading, ask and it can be exported.")
    A("Shadow        Carried in the ALPHA channel, not painted on as grey. That")
    A("              is why it darkens a dark background correctly instead of")
    A("              laying a grey patch on it.")
    A("Not applied   Chromatic aberration, vignette and film grain are")
    A("              deliberately absent. They are properties of the FINISHED")
    A("              image -- a vignette darkening the corners of transparency,")
    A("              or grain stopping dead at the vehicle's outline, is a")
    A("              giveaway. Add them to the final composite instead.")
    A("Printing      These are sized for screen and small print. For large")
    A("              format, say so and they can be re-rendered bigger -- it is")
    A("              one command, it just takes longer.")
    A("")
    A("WHAT IS STILL WRONG WITH THE MODEL -- PLEASE READ")
    A("-" * 72)
    A("You asked for these before calling the model done, so here is the")
    A("honest state. These are known, measured, and visible at large sizes:")
    A("")
    A("  * THE VW EMBLEM ON THE NOSE READS AS AN X. This is the defect you")
    A("    have reported six times. It is still there. The nose emblem and all")
    A("    four hubcaps are affected. It is most visible in front_elevation")
    A("    and front_three_quarter.")
    A("  * The 'Senor' word is drawn too small -- roughly 0.83 x 0.86 of where")
    A("    the photograph puts it. Its FINISH is now correct (bright silver,")
    A("    per your ruling); its SIZE is not.")
    A("  * The glass is a flat slab with no real reflections. The tyres have no")
    A("    tread and no sidewall lettering. The tail is modelled as a box where")
    A("    the real one is rounded. Two loudspeakers on the roof are missing.")
    A("")
    A("If any of those would show in the piece you are making, tell me which")
    A("view you need most and it can be fixed before that one ships.")
    open(p, "w").write("\n".join(L) + "\n")
    print("\n  wrote %s" % os.path.relpath(p, HERE))


def _wrap(s, n):
    out, line = [], ""
    for w in s.split():
        if len(line) + len(w) + 1 > n:
            out.append(line); line = w
        else:
            line = (line + " " + w).strip()
    if line:
        out.append(line)
    return out


def contact(rows):
    """Every view on four backgrounds.  This is the sheet a human LOOKS at
    before the package is believed (rule 1)."""
    BGS = [(255, 255, 255), (128, 128, 128), (178, 34, 34), (18, 18, 20)]
    TH = 460
    tiles = []
    for v, stem, w, h, bb, st in rows:
        a = np.array(Image.open(os.path.join(
            OUTDIR, "full_frame", "combi_%s.png" % stem)).convert("RGBA")).astype(float)
        im = Image.fromarray(a.astype(np.uint8), "RGBA")
        sc = TH / float(im.height)
        im = im.resize((max(1, int(im.width * sc)), TH), Image.LANCZOS)
        q = np.array(im).astype(float)
        rgb, al = q[..., :3], q[..., 3:] / 255.0
        row = [ (rgb * al + np.array(b, float) * (1 - al)).astype(np.uint8)
                for b in BGS ]
        tiles.append(np.concatenate(row, axis=1))
    W = max(t.shape[1] for t in tiles)
    tiles = [np.pad(t, ((0, 0), (0, W - t.shape[1]), (0, 0)),
                    constant_values=60) for t in tiles]
    sheet = np.concatenate(tiles, axis=0)
    p = os.path.join(OUTDIR, "contact_sheet.png")
    Image.fromarray(sheet).save(p, optimize=True)
    print("  wrote %s  (%d views x white/grey/red/black)"
          % (os.path.relpath(p, HERE), len(rows)))


if __name__ == "__main__":
    sys.exit(main())
