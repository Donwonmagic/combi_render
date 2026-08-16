"""probe_clean_top.py -- rev 28, READ-ONLY.  SPEC 10.81.

THE OWNER HAS READ THE COUNTER TOP'S SURFACE CONDITION.

  [stated] `ref_rear34.jpg` shows the counter top as CLEAN VARNISHED PLYWOOD.

The shipped build paints that surface with a settled-dust film at **mean
coverage 0.548**, recomputed by a LIVE ASSERT at `t1_mats.py:467` on every
build, and SPEC 10.70 identified that film as **57.1/52.6/36.6 % of the
`COUNTERTAN` pedestal**.  So the reading bears directly on a modelled feature.

WHAT THIS FILE DOES, AND DELIBERATELY DOES NOT DO
-------------------------------------------------
It computes what the model predicts for a CLEAN top and compares it with what
the photograph shows, so the reading can be acted on with a number rather than
with a sentiment.  **It changes NOTHING.**  SPEC 10.76 ruled that
`W_DUST_FAC_UP` must not be repaired blind, and the owner's reading -- while it
is exactly the kind of evidence that reopens the item -- is neither of the two
things 10.76 named as sufficient (a `CREAM` reference, or a same-class
differing-orientation pair).

CONTROLS -- asserted, not claimed
---------------------------------
  H  HARNESS: the shipped chain must reproduce `_UP_MEASURED` from
     `COUNTERCREAM` at the live coverage, and must reproduce SPEC 10.76's
     published E-free triple (1.056, 0.884, 0.803).  If the harness does not
     reproduce, nothing below is readable.
  T  TAUTOLOGY: the live assert's agreement must be shown to be one -- the
     three-channel spread of the implied coverage must be ~0.
  R  REPRODUCE: 10.76's recovered patches must still return their recorded
     medians from the frame, at the recorded n.

Run:  /tmp/blender/4.5/python/bin/python3.11 probe_clean_top.py
Writes nothing.
"""
import sys

import numpy as np
from PIL import Image

from probe_dust_anchor import M          # PARSED from t1_mats, never imported
#   t1_mats imports bpy, so it cannot be imported outside Blender.  rev 27's
#   probe_dust_anchor parses it with `ast` and EVERY PARSE RAISES if a constant
#   stops being a literal or an os.environ.get default -- and it resolves the
#   DEFAULT, so this probe always describes the SHIPPED build and never the
#   caller's environment.  Re-used rather than re-implemented, so there is one
#   parser to keep honest instead of two.

FRAME = "ref_rear34.jpg"
# SPEC 10.76's forensically recovered patches, verbatim.
P_FLANK = (914, 983, 298, 337)      # u0,u1,v0,v1 -- exact and UNIQUE
P_TOP = (556, 656, 397, 424)        # exact, NOT unique -- 10.76 says so
PUB_EFREE = (1.056, 0.884, 0.803)   # SPEC 10.76's published observed top/flank
# 10.76's BAND-FOLLOWING CLEAN sample of the same surface, median sRGB.  This
# -- not the founding patch -- is what 10.76's published E-free triple is
# computed from, which my first cut of this probe got wrong.  See TAUTOLOGY 2.
CLEAN_TOP_SRGB = (208, 176, 132)


def srgb_to_lin(c):
    c = np.asarray(c, dtype=float) / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def trimmed_median(im, box):
    """10.76's convention: middle 80 % of L*, then the per-channel median."""
    u0, u1, v0, v1 = box
    a = np.asarray(im.crop((u0, v0, u1, v1)).convert("RGB"), dtype=float)
    flat = a.reshape(-1, 3)
    lin = srgb_to_lin(flat)
    Y = 0.2126 * lin[:, 0] + 0.7152 * lin[:, 1] + 0.0722 * lin[:, 2]
    lo, hi = np.percentile(Y, 10.0), np.percentile(Y, 90.0)
    keep = flat[(Y >= lo) & (Y <= hi)]
    return np.median(keep, axis=0), len(keep), len(flat)


def main():
    ok = True

    def check(tag, cond, detail=""):
        nonlocal ok
        ok = ok and bool(cond)
        print("  [%s] %-50s %s" % ("PASS" if cond else "FAIL", tag, detail))

    print("=" * 78)
    print("probe_clean_top.py -- the owner reads the counter top as CLEAN")
    print("=" * 78)

    CT = np.array(M.COUNTERTAN, dtype=float)
    CC = np.array(M.COUNTERCREAM, dtype=float)
    DU = np.array(M.W_DUST_COL_UP, dtype=float)
    UM = np.array(M._UP_MEASURED, dtype=float)
    CR = np.array(M.CREAM, dtype=float)
    f = M.W_DUST_UP_W * M.W_DUST_MOT_MEAN * M.W_DUST_FAC_UP * 1.4

    print("\n=== the shipped constants ===")
    print("  COUNTERTAN    %s   <- what the counter top CARRIES" % (tuple(CT),))
    print("  COUNTERCREAM  %s   <- what the assert anchors to" % (tuple(CC),))
    print("  W_DUST_COL_UP %s" % (tuple(DU),))
    print("  _UP_MEASURED  %s" % (tuple(UM),))
    print("  CREAM         %s" % (tuple(np.round(CR, 4)),))
    print("  live coverage f = %.6f  (t1_mats.py:467)" % f)

    # ---- H: harness -----------------------------------------------------
    print("\n=== H  HARNESS CONTROLS ===")
    pred_cc = (1.0 - f) * CC + f * DU
    check("H1 shipped chain reproduces _UP_MEASURED from COUNTERCREAM",
          np.max(np.abs(pred_cc - UM)) < 2e-3,
          "max err %.2e" % np.max(np.abs(pred_cc - UM)))
    efree_pred_cc = pred_cc / CR
    check("H2 reproduces SPEC 10.76's E-free dusty-COUNTERCREAM triple",
          np.max(np.abs(efree_pred_cc - np.array([0.989, 0.840, 0.738]))) < 2e-3,
          "%s" % (tuple(np.round(efree_pred_cc, 4)),))
    pred_ct = (1.0 - f) * CT + f * DU
    efree_pred_ct = pred_ct / CR
    check("H3 reproduces SPEC 10.76's E-free dusty-COUNTERTAN triple",
          np.max(np.abs(efree_pred_ct - np.array([0.881, 0.681, 0.461]))) < 2e-3,
          "%s" % (tuple(np.round(efree_pred_ct, 4)),))

    # ---- T: the tautology ----------------------------------------------
    imp = (UM - CC) / (DU - CC)
    print("\n=== T  the live assert's agreement is a TAUTOLOGY ===")
    print("     implied coverage per channel %s   spread %.2e"
          % (tuple(np.round(imp, 6)), float(imp.max() - imp.min())))
    check("T  three-channel spread is ~0, so the assert restates the solve",
          float(imp.max() - imp.min()) < 1e-4,
          "10.76's 5.2e-05")

    # ---- R: reproduce the patches ---------------------------------------
    im = Image.open(FRAME).convert("RGB")
    mf, nf, tf = trimmed_median(im, P_FLANK)
    mt, nt, tt = trimmed_median(im, P_TOP)
    print("\n=== R  10.76's recovered patches, re-measured from the frame ===")
    print("     flank %s  median sRGB %s  n=%d of %d (10.76: 2153)"
          % (P_FLANK, tuple(int(v) for v in mf), nf, tf))
    print("     top   %s  median sRGB %s  n=%d of %d (10.76: 2160)"
          % (P_TOP, tuple(int(v) for v in mt), nt, tt))
    check("R  the recovered patches still return 10.76's recorded n",
          nf == 2153 and nt == 2160, "%d / %d" % (nf, nt))
    efree_found = srgb_to_lin(mt) / srgb_to_lin(mf)
    efree_obs = srgb_to_lin(CLEAN_TOP_SRGB) / srgb_to_lin(mf)
    print("     E-free from the FOUNDING patch %s"
          % (tuple(np.round(efree_found, 4)),))
    print("     E-free from the CLEAN sample   %s   (10.76 published %s)"
          % (tuple(np.round(efree_obs, 4)), PUB_EFREE))
    check("R2 10.76's published E-free triple is the CLEAN sample's",
          np.max(np.abs(efree_obs - np.array(PUB_EFREE))) < 0.01,
          "max d %.4f" % np.max(np.abs(efree_obs - np.array(PUB_EFREE))))

    # ---- T2: a SECOND tautology, new in rev 28 --------------------------
    # MY OWN FIRST CUT OF THIS PROBE ASSERTED THE FOUNDING PATCH HERE AND
    # FAILED.  Checking the control's own premise -- fifth time in this project
    # -- shows the premise was mine: 10.76 computed its E-free triple from the
    # CLEAN sample, correctly.  And the reason the founding patch is the wrong
    # one to use is itself a finding.
    print("\n=== T2 A SECOND TAUTOLOGY, and it is NEW ===")
    print("     founding/flank x CREAM %s"
          % (tuple(np.round(efree_found * CR, 4)),))
    print("     _UP_MEASURED           %s" % (tuple(np.round(UM, 4)),))
    check("T2 the FOUNDING patch's E-free ratio IS _UP_MEASURED restated",
          np.max(np.abs(efree_found * CR - UM)) < 2e-3,
          "max d %.2e -- so it can NEVER disagree with the live assert"
          % np.max(np.abs(efree_found * CR - UM)))
    print("     rev 27 found ONE tautology in this chain (the three-channel")
    print("     collinearity).  This is a SECOND, in the same chain: because")
    print("     `_UP_MEASURED` was DERIVED from the founding patch through the")
    print("     von-Kries gain, that patch's own E-free ratio is the assert")
    print("     written backwards.  Any future test must use the CLEAN sample.")

    # ---- THE QUESTION: what does a CLEAN top predict? -------------------
    print("\n" + "=" * 78)
    print("THE OWNER SAYS THE TOP IS CLEAN.  WHAT DOES CLEAN PREDICT?")
    print("=" * 78)
    rows = [
        ("dusty COUNTERTAN   (SHIPPED)", pred_ct / CR),
        ("CLEAN COUNTERTAN   (f = 0)  ", CT / CR),
        ("dusty COUNTERCREAM (assert) ", pred_cc / CR),
        ("CLEAN COUNTERCREAM (f = 0)  ", CC / CR),
    ]
    print("\n  arm                            E-free top/flank        vs "
          "OBSERVED %s" % (tuple(np.round(efree_obs, 3)),))
    for lbl, v in rows:
        d = (v - efree_obs) / efree_obs * 100.0
        print("    %-30s %s   %s"
              % (lbl, tuple(np.round(v, 4)),
                 " ".join("%+6.1f %%" % x for x in d)))

    print("\n  READ THIS CAREFULLY -- the reading does NOT close the item:")
    print("    * Going CLEAN moves every channel toward the photograph, which")
    print("      is what his reading predicts and is real corroboration.")
    d_clean = (CT / CR - efree_obs) / efree_obs * 100.0
    d_dusty = (pred_ct / CR - efree_obs) / efree_obs * 100.0
    print("      worst channel |err|: dusty %.1f %% -> clean %.1f %%"
          % (np.max(np.abs(d_dusty)), np.max(np.abs(d_clean))))
    print("    * BUT f = 0 alone does NOT reconcile it.  Clean COUNTERTAN is")
    print("      still %.1f %% short in B.  Removing the dust is NECESSARY and"
          % abs(d_clean[2]))
    print("      NOT SUFFICIENT, so the residual is in COUNTERTAN or CREAM --")
    print("      exactly where 10.76 left it, now from an independent")
    print("      direction.")
    implied = efree_obs * CR
    print("    * The top albedo the photograph implies is %s"
          % (tuple(np.round(implied, 4)),))
    print("      against COUNTERTAN %s -- the gap is almost all BLUE."
          % (tuple(CT),))
    print("    * AND THE TENSION IS REAL, STATED NOT SMOOTHED: the arm that")
    print("      matches the photograph best is DUSTY COUNTERCREAM (worst")
    print("      channel %.1f %%), which is the WRONG MATERIAL for this"
          % np.max(np.abs((pred_cc / CR - efree_obs) / efree_obs * 100.0)))
    print("      surface (10.71).  Clean COUNTERCREAM is worst of all at")
    print("      %.1f %%.  So the dust IS doing real numerical work -- under an"
          % np.max(np.abs((CC / CR - efree_obs) / efree_obs * 100.0)))
    print("      anchor that is itself wrong.  10.60 rules this up-facing /")
    print("      vertical pair INADMISSIBLE, so none of it binds either way.")

    print("\n=== WHAT IS NOT DONE, AND WHY ===")
    print("  W_DUST_FAC_UP is UNCHANGED at %.4f.  SPEC 10.76 bars a blind"
          % M.W_DUST_FAC_UP)
    print("  repair, and this reading is neither of the two things it named as")
    print("  sufficient.  Setting f = 0 would also silently discard 57.1/52.6/")
    print("  36.6 %% of the pedestal SPEC 10.70 identified, and would swap one")
    print("  unsupported appearance for another -- clean COUNTERTAN does not")
    print("  match the photograph either.  The pair is still the up-facing /")
    print("  vertical mismatch 10.60 ruled INADMISSIBLE, so this frame cannot")
    print("  separate COUNTERTAN from CREAM whatever the coverage is.")
    print("\n  WHAT IT DOES CHANGE: the coverage is no longer merely")
    print("  UNSUPPORTED (10.76) -- it is CONTRADICTED BY AN OWNER READING of")
    print("  the only frame that shows the surface.  That is a stronger")
    print("  statement and it makes this the top item for rev 29.")

    print("\nRESULT: controls %s" % ("pass" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
