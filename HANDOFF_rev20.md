# HANDOFF rev 20 — work item 1 refuted, §10.52 repaired, and two probes killed by their own controls

**Guards `0 fail / 1 warn` at BOTH subdivision levels. Geometry unchanged from
rev 18/19 — this revision changes one guard, one generated file, and adds
measurement levers that all default to a proven no-op.** Read `STATE.md` over
any prose here.

---

## 1. THE HEADLINE — the cream map's chroma target does not bind, and must not be chased

§6.1 of the rev-20 prompt said: give the mottle its own chroma gain, target
dC\* rms **0.744 / 1.015 / 1.295**. I built the lever, measured it, and then the
target failed a check nobody had run. **SPEC §10.54.**

**The albedo pass is DETERMINISTIC** — two runs of one arm agree to three
decimals, so the seed-to-seed null is zero and every figure below is exact.

| arm | corr(dL\*,dC\*) 5.9/11.9/23.7 mm | dL\* rms | dC\* rms |
|---|---|---|---|
| AMP 0 (ablation) | +0.265 +0.234 +0.259 | 0.337 0.608 0.968 | **0.244 0.250 0.253** |
| AMP 0.55 (shipped) | +0.216 +0.194 +0.224 | 0.345 0.618 0.981 | **0.220 0.227 0.231** |
| AMP 2.0 | +0.047 +0.057 +0.127 | 0.374 0.650 1.011 | 0.223 0.233 0.239 |
| photograph | +0.042 −0.106 −0.294 | 0.385 0.493 0.735 | 0.744 1.015 1.295 |

**(a) The dC\* triple quoted everywhere as the shipped render is the ABLATION
arm's.** §10.51, `HANDOFF_rev19` §5 and the rev-20 prompt all quote
`0.240 / 0.249 / 0.253`. That is **AMP 0**. Shipped is `0.220 / 0.227 / 0.231`.
Both endpoints reproduce §10.51 to ~0.02, so the chain is unchanged and only the
middle arm was mis-transcribed. **Eighth instance of a figure not watched print.**

**(b) Switching the map on drives dC\* DOWN** (0.244 → 0.220), not flat.

**(c) My alias hypothesis for that dip was REFUTED by its own control.** The
mottle's base octave is 1/0.024 = 41.67 and `W_N2`'s second octave is 44 — 5.3 %
apart, same object-space field, mapping in opposite senses. `MOTTLE_OFS` was
added to test it; **(0,0,0) reproduced the shipped arm to three decimals first**,
and the offset arm moved dC\* only 0.220 → 0.217. Ablating `W_FADE_VAL` drove it
further down, so the Value term is not the canceller either.

**(d) The lever IS real and IS chroma-pure.** `W_FADE_SAT` 0.88 → 0.40 gives
dC\* **0.269 / 0.314 / 0.335**, growing with scale as the photograph does, while
dL\* moves 0.345/0.618/0.981 → 0.346/0.620/0.984 — not at all.

**(e) AND THE TARGET DOES NOT BIND.** dC\* rms is an ABSOLUTE Lab statistic. The
base levels had never been printed on either side:

```
                      mean L*    mean C*
photograph _BODY        80.89      21.44     n = 7968, 0.00 % clipped
render patch            83.20       3.89     -> C* ratio 0.182
```

§10.51's "the render's C\* ≈ 12" is wrong by 3×. **L\* bases agree to 2.9 %, so
the dL\* comparison is valid — which is exactly why §10.51 correctly found dL\*
already close. The C\* bases differ 5.5×, so the dC\* comparison is not.**
Normalised: render **5.66 / 5.83 / 5.94 %** against photograph **3.47 / 4.73 /
6.04 %** — **already at or above target at every scale.** Raising the gain drives
it to 2–6× the real vehicle's.

**(f) The BEAUTY arm has been reporting zeros.** §10.51 kept it "so both are
reported". On this patch it is **clipped 100.00 %** — L\* exactly 100.00, C\*
exactly 0.00, dL\*/dC\* exactly 0.000, corr `nan`. It never could report anything.

**NEW RULE: A TARGET IS A PROBE TOO.** Print the base level of any absolute
statistic before comparing two frames through it.

## 2. GUARDS — the figures I watched print

| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 1 warn** | **0 fail, 1 warn** |
| warn | roof crown @ rear axle **1.983** vs 1.960 (**+23 mm**) | 1.983 |
| rear arch lip above hub | 0.3722 → gap **39.7 mm** | same |
| front arch (control) | 0.3732 → gap **40.7 mm** | same |
| rake | **17.75 mm/m (locked 17.75)** | same |
| dome deficit / rear overhang | +0 / **0.7730** | same |
| dims | L=**4.065** W=**1.750** | same |
| cut roof hole | **68052v** | **252123v** |
| objects at `materials:` | **126** | **126** |

**185 meshes**, 42 materials, 5 constant-rough, **0 non-manifold**, three open
apertures on +Y, four shut lines 100 % open, band 1.372–1.775, bay widths
**0.516 0.515 0.516**. Every figure identical to rev 18 and rev 19.

## 3. WHAT CHANGED

- **`audit.py`** — §10.52 repaired (§10.53). `:156` now calls
  `verify._arch_lip_z`; the `STATE.md` row is sourced from the same verify line
  that already publishes the number, as `_bayline` is. `(measured 41)` gone.
- **`shader_solve.py`** — `T1_CTAN_NOBOUNCE` (`top` / `fascia` / `top_all` /
  `fascia_all`), the interreflection arms.
- **`t1_mats.py`** — `MOTTLE_OFS` (`T1_MOT_OFS`); `T1_CTAN_DUST`,
  `T1_CTAN_WEAR`, `T1_CTAN_FADE`.
- **`mottle_measure.py`** — the base-level L\*/C\* print.
- **`SPEC.md`** — §10.53, §10.54, §10.55, §10.56 + change log.

## 4. THINGS YOU MUST NOT SILENTLY UNDO — rev 19's §4 and rev 18's §4 still stand in full

1. **Do NOT raise the mottle's chroma gain.** Normalised, the render already
   meets or exceeds the photograph at every scale (§10.54). The dC\* triple in
   §10.51 is the ablation arm's.
2. **Every new env lever defaults to a PROVEN no-op** and each was verified as
   such *before* its experimental arm was believed. Keep that order.
3. **`STATE.md`'s arch rows are parsed from `verify`'s own line.** Do not
   re-implement the measurement in `audit.py` — that is how the phantom happened.
4. **A RAY-VISIBILITY FLAG IS NOT AN ABLATION** (§10.56). Remove the ALBEDO.
5. **`CREAM` is UNCHANGED** and must stay so until a same-light neutral settles
   it (§10.55).

## 5. STILL OPEN

- **`CREAM`'s albedo is the largest open thing in the model.** Locked at sRGB
  (206,208,200), hue 75.0°, sat 0.038, **G > R**; the bus's own cream in
  `ref_rear34.jpg` reads (216,200,161), hue 41.7°, sat 0.255, **R > G**. §10.55
  records three routes and every one's weakness. **Blocked on one owner reading:**
  are boxes A `(792,838,410,458)` / B `(846,876,408,456)` white paper napkins,
  and is C `(986,1024,330,378)`, D `(1030,1074,392,424)` or E
  `(1096,1180,404,436)` bare stainless?
- **`H_ROOF`** — put to him with a recommendation, **answer not yet received.**
  Recommended: retire it as an accuracy target, keep the probe as a LABELLED
  regression catcher with a ±5 mm band, as rev 18 did for the height row. The
  warn would then disappear **because the test was withdrawn, not because the
  model improved.** Rejected: re-valuing to 1.9835 (the guard would compare the
  model to itself, and it clears a warn by tuning).
- **`COUNTERTAN`'s pedestal is UNIDENTIFIED.** Dust, wear, fade, coat+spec and
  interreflection are all excluded and together account for ~a fifth of a
  pedestal that is **~69 %** of the top's radiance. **The best open lead is the
  occlusion hypothesis** — rev 15 fixed exactly this in `solve_mural` ("isolate
  the object in the measured render, not only in the mask") and the fix was never
  applied to `solve_ctan`. The per-pixel test **cannot work at 48 samples**
  (seed-to-seed noise 21.7 % per pixel, median); it needs a much higher sample
  count or an object-index pass.
- **NOT DONE this revision, and named as such:** the shut-line × aperture
  invariant (item 5 — the assert still covers 1 of 4 outlines, 1 of 2 arches,
  0 of 5 apertures, and the five crossings are still live); the tail-lamp
  material slot; `Senor` at 0.504 of its 0.782 ceiling; `SCR` +80 mm aft;
  `probe_rev16.py`'s `xa` vs `xa`; `folk_gen.py`'s four stale constants; SPEC
  §1713's stale `RAKE_DZDX`; the ~12 unverified image URLs.
- **NO HERO SINCE REV 16 — deliberately.** The arch fix, rev 17's hubcap rings
  and rev 19's mottle are all unphotographed. Held because if `CREAM` moves, a
  hero shot now is stale on arrival. Shoot it once, after §10.55 closes.
- `PLATE_W = 0.3300` still has no provenance; rev 18's "bounded at < 0.1754 m"
  is a bound on `PLATE_OUTER_H`.

## 6. A NOTE ON THE RESTORE CHECKS

The rev-20 prompt's ten content greps and its 8-commit ancestry loop **all
passed, and neither reached the tip.** The tip was `1e9805c`, one commit past the
loop's last entry `456b201`, touching only `NEXT_CONTEXT_PROMPT_rev20.md`.
Harmless this time — but rev 18's own rule is that **both checks must reach the
tip**, and the rev-20 prompt violated it. The rev-21 prompt's checks are written
against the final commit.
