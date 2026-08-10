# HANDOFF rev 10

## THE STANDARD — read before anything else

Donald's words, unchanged and binding:

> The final product should be nearly indistinguishable from the original.
> **Any single measurement off is unacceptable.**
> We are recreating a photo realistic version of **that exact bus.**

And the reason, which sits above clinical accuracy:

> I really want this to give the person the opportunity to feel like they were
> on Playa del Carmen all those years ago. I want the owner to remember
> standing in the kombi, in this very picture that was provided.

## What rev 10 changed

Guards: **0 fail, 1 warn at BOTH subdivision levels**, warn unchanged at
`roof @ rear axle 1.923 vs spec 1.960 (-37 mm)`. HEAD `a8b6121`, clean tree.

| | rev 9 | rev 10 | measured target |
|---|---|---|---|
| script whole-lockup IoU | 0.511 | 0.942 | see caveat below |
| `Senor` IoU | 0.089 | 0.825 | was "not fitted" |
| script ink | flat (214,216,218) | mottled leaf, measured chromaticity | 5.9 % mottle |
| cab-door gold coverage | 0.0-0.2 % assumed | 29.09 % | 29.08 % |
| gold : adjacent red contrast | x1.455 | x2.050 | x2.048 |
| flank art, whitened NCC between sides | 0.175 mirrored | 0.064 | decorrelated |
| lid mural bare ground | 45.98 % | 21.96 % | 21.82 % |
| mural flower heads | 9 | 10 | 10 |
| VW roundel diameter | 0.370 | 0.280 | 0.280 +/- 0.030 |
| Playa vegetation | none | placed by inverting the reference camera | foliage:cream 0.109 vs 0.104-0.113 |

Five findings in SPEC 10.19-10.25 are the substance. Read those, not this table.

## THE CAVEAT ON 0.942 — do not quote it as a fidelity score

The glyphs are now swept along the MEASURED MEDIAL AXIS of the reference ink
mask, and `compare_script.py` scores against that same mask. So the number
means "a disc sweep reconstructs the measured ink to 0.94". It is not an
independent check. **The independent test is `flank_compare.py`** against the
photograph through the ortho camera. Run it. It was not run in rev 10 and that
is a gap.

## OPEN, ranked by how much they cost the hero

1. **The Playa hero's exposure is NOT converged.** Against the reference's own
   display luma the render reads cream 253 / red 193 / foliage 46 / ground 186
   where the reference reads **241 / 118 / 82 / 108**. The cream is clipping,
   which compresses everything under it. Two scalars (`T1_KEY_PLAYA`,
   `T1_WORLD_PLAYA`) were swept and they trade foliage against ground without
   fixing the range. The diagnosis to test next: this is a CONTRAST mismatch,
   not a level one -- the film (AgX + Punchy) is calibrated for the white
   studio, where paper white sits at linear 21.0. A scene with no white
   backdrop may need a different look, or an explicit exposure offset, rather
   than more light.
2. **No contact shadow.** `optics-6` -- the shadow dies within 11 mm of the
   tyre. In the Playa hero the vehicle reads as floating. Never applied.
3. **The nose folk art is confetti, not scrollwork.** Reported by the folk-art
   pass and not fixed: the nose front face is box-projected and samples (y, z),
   which falls in the same u-band as the cab door's flank footprint, so
   whatever is in the door's lower band appears on the nose. **Needs a separate
   nose decal or per-face UVs in `t1_mats.py`.**
4. **The rear window renders as a mirror**, not as an interior.
5. **Lid topology is NOT MEASURABLE from the three photographs.** The lettered
   cream panel's apparent aspect in `ref_rear34` is >= 1.15 and foreshortening
   can only reduce an aspect, so its true aspect is >= 1.15; the front lid
   board is 1.83 and the rear 0.67, so the lettered panel CANNOT be the rear
   board. But the flower board's footprint in `ref_side` spans bus fraction
   0.262-0.738 against the front lid's 0.275-0.750, so the MURAL is on the
   front lid. Both cannot be one face. The reading that fits every photograph:
   **the flower board is a separate signboard standing proud of the front lid,
   whose own underside is the cream lettered panel.** `t1_shell.roof_lids()`
   gives each lid exactly one board face. Ask Donald before modelling it.
6. **The lettered panel reads "La S———" and no further.** Seven merged
   downstrokes follow, which is what "anta" produces, so "La Santa" is
   consistent -- but it is a RECONSTRUCTION, not a reading, and it has been
   carried as fact for several revisions.
7. SPEC 10.24's three reverted items: bumper standoff, indicator lens depth,
   headlamp vertical position. Each needs a second derivation.
8. Still open and never skeptic-passed: `materials-5` (three serving bays share
   one reflection), `apertures-7`, the 99 mm tail length, six materials still
   reporting a constant roughness, and 10.9's rake-versus-arch-gap
   contradiction.

## Process rules that earned their place in rev 10

* **Ask what a photograph shows before measuring from it.** One question and
  two crops resolved SPEC 10.15, which had quarantined three revisions of work.
* **A rendered ratio is only an albedo ratio between two surfaces of the same
  class under the same light.** Generalises 10.12. Cost one wrong silver.
* **A constant tuned against another constant must be expressed in terms of
  it.** The VW glyph merged into an X for the second time because `vw_logo`'s
  size was absolute while the ring it sits in is driven by `ROUNDEL_D`.
* **When a finding breaks something independently locked, measure it a third
  way before choosing.** Three did in rev 10; the third method refuted the
  finding every time.
* **Check what a guard actually measures.** The script's acceptance test had
  been scoring against a reference mask missing 14 % of the ink, and two
  recorded generator defects were artefacts of it.
