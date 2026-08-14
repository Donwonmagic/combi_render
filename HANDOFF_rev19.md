# HANDOFF rev 19 — the cream, re-grounded on the vehicle

**Guards `0 fail / 1 warn` at BOTH subdivision levels. Geometry unchanged from
rev 18 — this revision is shader-only.** Read `STATE.md` over any prose here.

---

## 1. THE HEADLINE — two surfaces, and neither was what the code said

**Every cream number rev 17 and rev 18 recorded was measured on a DETACHED
SIGN.** `cream_rms._LID = (588, 760, 40, 190)` is the "La Santa" board.
`cream_rms.py:241` called it "the LID UNDERSIDE", and shipped this caveat with
every number: *"an INWARD-FACING panel, so its weathering is a LOWER BOUND on
the sun-exposed flank's."*

Shown a marked crop with the boxes printed, the owner identified it as **a
detached sign, separate from the bus** — his own settled reading from §10.28,
which §10.38 had silently reverted to the older §10.19/§10.26 identification.
So "lid underside" is wrong and the lower-bound inference has no basis.

**And `FadeVert` — the mechanism the map was supposed to modulate — has never
reached the flank.** Probed on the built scene:

```
OBJ T1_body -> ['T1_paint']
objects on cream -> ['vw_disc']
T1_paint FadeVert = 0.000     cream / countercream / bumpercream = 0.500
```

`body_paint()` renders cream above the break line and red below it in ONE
material. rev 14's fix reached the VW roundel disc, the bumpers, the counter,
the wheels and the hubcap whites — **and not the body shell**, which is the
surface §10.30c measured the −55 % chroma fade on.

## 2. GUARDS — the figures I watched print

| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 1 warn** | **0 fail, 1 warn** |
| warn | roof crown @ rear axle **1.983** vs 1.960 (+23 mm) | 1.983 |
| rear arch lip above hub | 0.3722 → gap **39.7 mm** | same |
| front arch (control) | 0.3732 → gap **40.7 mm** | same |
| rake | **17.75 mm/m (locked 17.75)** | same |
| dome deficit / rear overhang | +0 / **0.7730** | same |
| dims | L=**4.065** W=**1.750** | same |
| cut roof hole | **68052v** | **252123v** |
| objects at `materials:` | **126** | **126** |

**185 meshes**, 42 materials, 5 constant-rough, 0 non-manifold, three open
apertures on +Y, four shut lines 100 % open, band 1.372–1.775, bay widths
**0.516 0.515 0.516**. Identical to rev 18 — the map is shader-only.

## 3. WHAT CHANGED

`cream_rms.py` — `_LID` retired with the reason; `_BODY = (885, 968, 292, 388)`
added; `spectrum()` and `character()` added. `t1_mats.py` — `FadeRough` group
input (default 0.0), `fadev_from` on `apply_weather`, the `FADEV_MOTTLE` chain
inside `body_paint`, seven `MOTTLE_*` constants all env-overridable,
`FADEV_CREAM` exposed as `T1_FADEV`. New: `fadev_ablate.py`,
`mottle_measure.py`. `SPEC.md` §10.49–10.52 + change log.

## 4. THINGS THE NEXT CONTEXT MUST NOT SILENTLY UNDO

* **`_BODY`'s trim is measured, not cosmetic.** 10.17 % of the owner's box is
  CLIPPED (max channel ≥ 254), all in columns 860–882, plus a brass strip over
  rows 270–287. A clipped pixel carries no texture and drags a high-pass RMS
  toward zero. My first comparison was contaminated this way and read 3× where
  the truth is 2.1–2.6×. **Do not widen `_BODY` back out.**
* **The gate is GEOMETRY ONLY and that is deliberate.** Inside an
  owner-identified box a colour gate cannot add information. The old
  `sat < 0.20` is tuned to the sign's C\* 11.2 and returns **2.9 % purity** on
  the bus's own cream. Do not re-add a colour gate.
* **`character()` must be able to return None.** Its predecessor printed its
  verdict as a constant string and fired on an empty mask with `nan`
  statistics. If you add a mechanism, add a test that can reject it.
* **`fadev_from` raises rather than falling back to a scalar.** A silent
  fallback is how a map ships switched off. Keep the raise.
* **`FadeRough` defaults to 0.0** so every pre-existing material is unchanged.
  It is separate from `Fade` because `script` runs `fade = 0.5` and must not
  gain roughness. Do not merge them.
* **The mottle is multiplied by `edge`, `body_paint`'s own two-tone selector.**
  That is what makes the red exactly 0.0 **by construction** and keeps
  §10.12's locked albedo saturation 0.816 safe. Do not replace it with a
  z-threshold.
* **`MOTTLE_M` is in METRES and the noise takes OBJECT coordinates.** Generated
  is bbox-normalised; the tail has moved twice. Do not switch to Generated.
* **344.1 ± 6.7 is the PLATE plane.** The cream is on the FLANK plane at
  **337 ± 7 px/m**, bracketed by the cream rim (330) and the plate (344.1).
  It is a bracket, not a measurement — do not promote it to one.
* rev 18's §4 list still stands in full. Note that its own last bullet points
  at `HANDOFF_rev17.md` §3 for a rev-17 invariant list; **§3 there is the
  `H_ROOF` section and no such list exists** — do not read that pointer as
  meaning there are no rev-17 invariants.

## 5. STILL OPEN — with numbers

* **The map's chroma amplitude is short and the lever is bounded.** dC\* rms
  render **0.240 / 0.249 / 0.253** (flat) against the photograph's
  **0.744 / 1.015 / 1.295** (growing). `MOTTLE_AMP` 0.55 → 2.0 moved it
  0.240 → 0.241 because the fade factor clamps at 1.0 and the *modulation*
  collapses past it. The ceiling of this lever is the full `W_FADE_SAT = 0.88`
  swing, ~12 % saturation, which on the render's C\* ≈ 12 cream cannot reach
  1.3. **Next step: give the mottle its own chroma gain so the uniform fade
  keeps 0.88.** Bounded, not a sweep.
* **"The cream is 26× too uniform" is retired.** dL\* rms render
  **0.322 / 0.584 / 0.948** against **0.385 / 0.493 / 0.735** — already close,
  and *over* at coarse scale. Do not re-open it.
* **§10.52 — a FOURTH `STATE.md` phantom, not repaired.** `audit.py:156` and
  `:474` still compute `ARCH_R − TIRE_R`, so `STATE.md` publishes
  `| arch radius − tyre radius | 41.0 mm (measured 41) |` against the mesh's
  **39.7 mm**, 68 lines below the real number, with a hand-typed "(measured
  41)". One-line fix; it changes `STATE.md`, so it is recorded rather than
  slipped in.
* **`PLATE_W = 0.3300` still has no provenance.** Note rev 18's §5 states it is
  "bounded by the wheel control at < 0.1754 m" — **that bound is on
  `PLATE_OUTER_H`, not on `PLATE_W`.**
* Carried, untouched: `H_ROOF` (direct mesh probe reads **1.9835 ± 0.0007**,
  1.960's only ground-line-free support withdrawn by §10.48 — his call);
  `COUNTERTAN`'s interreflection test (**four revisions now**); the five
  shut-line × aperture crossings; the tail-lamp material slot; `Senor` at
  0.504 of its 0.782 ceiling; `SCR` +80 mm aft; `probe_rev16.py`'s `xa` vs
  `xa`; `folk_gen.py`'s four stale constants; the ~12 unverified image URLs;
  the head-on rear elevation; the flat tail-panel height.
* **No hero since rev 16.** The arch fix, rev 17's hubcap rings and now the
  mottle map are all unphotographed.

## 6. PROCESS, EARNED THIS REVISION

* **Check what a probe can physically SEE — including which SURFACE.** Six
  instances before this; two more here. The cream instrument was measuring an
  object that is not the vehicle, and it said so in its own comment.
* **A verdict printed as a constant string is not a measurement.** Give every
  mechanism a control that can reject it, and check the control itself.
* **Ablate before you believe — and then check the ablation is measuring the
  right statistic.** The luminance ablation said the map was inert. It was not:
  the lever is chromatic and the instrument was achromatic. An inert-looking
  ablation can mean the wrong estimator, not a dead constant.
* **Clipping destroys texture.** Print the clipped fraction on every patch on
  both sides of a comparison; an unclipped patch against a 10 %-clipped one is
  not a comparison.
* **An ORTHO render has an exact px/m.** Put the render side on an ortho and
  all the scale uncertainty collapses into one stated bracket on the
  photograph.
* **Verify the projection before measuring through it.** `X_TAIL` predicted
  column 1961.9 against an observed alpha edge at 1961; the wrong sign missed
  by 103 px. The script refuses above 12 px.
