# HANDOFF rev 21 — the owner's reading obtained, and five routes to the cream all refuted

**Guards `0 fail / 1 warn` at BOTH subdivision levels. Geometry unchanged from
rev 18/19/20 — this revision changes SPEC only.** Read `STATE.md` over any prose
here.

---

## 1. THE HEADLINE — `CREAM` IS UNCHANGED, and it is not for want of evidence

§10.55's question was answered. It did **not** unblock `CREAM`. **SPEC §10.57.**

The owner identified **N2 `(816,836,422,450)` and N3 `(868,890,426,452)` as
white paper napkins** and **M1 `(844,860,418,452)` as bare/brushed stainless** —
and refuted a second crop of mine in the process: **N1 `(784,798,420,448)` is
still straddling** a napkin and the dispenser side.

**rev 20's boxes A and B were worse than rev 20 knew.** Each straddles a napkin
face AND the grey dispenser body. That, not differential shading, is why B read
34 code values darker than A. rev 20's "the two dispensers disagree by 11 %
because they are shaded differently" is **WITHDRAWN**.

**rev 20's C / D / E are dropped on a measurement.** They are inside the galley
opening; luminance ÷ the cream's is **0.32 / 0.23 / 0.22** against the napkins'
**1.13 / 1.54 / 1.37**. A neutral cannot be 3–4× darker than the surface it
shares light with.

| route | result |
|---|---|
| **A** napkin as same-light neutral | cream hue **48.2°**, sat **0.163**, R>G. **Clean.** N1/N2/N3 clip 22/12/0 % and agree — and since clipping compresses toward neutral, that agreement is the control |
| **B** M1 stainless as neutral | **INADMISSIBLE by §10.21** — metal vs diffuse dielectric. Disagrees with A (63.7°, G>R); that is the tell |
| **C** third method: recover the locked `RED` | **FAILS.** hue **13.1–13.8°** vs locked **5.0°**. Shading explains **1.7°** of the 8.5° across 30 patches over a 4.27× luminance range |
| **§10.12 invariant** | `ref_rear34` red (G−B)/(R−B) = **0.2225 ± 0.0045** vs locked **0.0813** → **+31 sd**. **No neutral transform relates that frame to the locked constants** |
| **D** locked `RED` as the illuminant reference | **REFUTED BY ITS OWN CONTROL** — implies the white napkin is a saturated purple (hue 260–300°, sat 0.30–0.43) |
| **E** solve §10.9's `obs = albedo·E + A` | **NO PHYSICAL SOLUTION** for any napkin albedo 0.05–0.95. The red reads **95 %** of the napkin's R where 0.552 should read **65 %** — they are not under the same light |

**NEW RULE: AN ILLUMINANT REFERENCE MUST CARRY SUBSTANTIAL ALBEDO IN ALL THREE
CHANNELS.** `RED` is (0.5520, **0.0294, 0.0176**); dividing by a near-zero
channel amplifies the additive term without bound.

## 2. GUARDS — the figures I watched print

| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 1 warn** | **0 fail, 1 warn** |
| warn | roof crown @ rear axle **1.983** vs 1.960 (**+23 mm**) | **1.983** |
| rear arch lip above hub | 0.3722 → gap **39.7 mm** | same |
| front arch (control) | 0.3732 → gap **40.7 mm** | same |
| rake | **17.75 mm/m (locked 17.75)** | same |
| dome deficit / rear overhang | +0 / **0.7730** | same |
| dims | L=**4.065** W=**1.750** | same |
| cut roof hole | **68052v** | **252123v** |
| objects at `materials:` | **126** | **126** |

**185 meshes**, 42 materials, 5 constant-rough, **0 non-manifold**, three open
apertures on +Y, four shut lines 100 % open, band 1.372–1.775, bay widths
**0.516 0.515 0.516**. Identical to rev 18, 19 and 20.

## 3. WHAT CHANGED

`SPEC.md` only — §10.57, §10.58, and the change-log row. **No code, no
geometry, no constant.**

## 4. THINGS YOU MUST NOT SILENTLY UNDO — rev 20's §4, rev 19's §4 and rev 18's §4 all still stand in full

1. **`CREAM` stays (206,208,200).** Route A is clean and still must not be
   applied: the frame fails the neutral-transform test at 31 sd. Do not apply
   route A without first establishing a neutral transform for `ref_rear34`.
2. **Do NOT re-use rev 20's boxes A/B/C/D/E.** A and B straddle two materials;
   C/D/E are in the galley. Use **N3** (0 % clipped) and **N2**; **N1 is
   refuted by the owner**.
3. **`RED` is not an illuminant reference** (§10.57 route D). Its G and B
   albedos are 0.029 / 0.018.
4. **The four `audit.py` livery rows are NOT identities** (§10.58). Their
   rake-invariance is deliberate and documented at `t1_core.py:165-171`. Do not
   "fix" it.
5. Every rule from rev 20 §4 — do not raise the mottle's chroma gain; new env
   levers default to a proven no-op; `STATE.md`'s arch rows are parsed from
   verify's own line; a ray-visibility flag is not an ablation.

## 5. STILL OPEN

- **`CREAM`.** What would settle it: a same-light, **same-CLASS**, three-channel
  reference; or an established neutral transform between `ref_rear34` and the
  frame the locked constants came from. **Neither exists in the three
  photographs** — so this may need the head-on elevation, or to be accepted as
  bracketed and labelled.
- **`H_ROOF` — his call, and the answer has not arrived for FIVE revisions.**
  Recommendation unchanged from rev 20: retire it as an accuracy target, keep
  the probe as a LABELLED regression catcher at ±5 mm.
- **`COUNTERTAN`'s HUE is a cheap untouched item, separate from the pedestal
  fight**: built h 42.3° / sat 0.254 against its own docstring's cited 29–37° /
  0.33–0.39 and an independent 1266-px read of **28.4° / 0.333**. Shader-only,
  and `T1_CTAN` already exists for the A/B. The ~69 % pedestal remains
  UNIDENTIFIED; best lead is still the occlusion hypothesis (object-index pass).
- Five shut-line × aperture crossings, one on the show flank; the `t1_shell:391`
  assert still covers 1 of 4 outlines, 1 of 2 arches, 0 of 5 apertures.
  **Expect a FAIL when first armed. That is the guard working.**
- `probe_rev16.py`'s `xa` vs `xa`; **`folk_gen.py`'s four stale constants AND
  its `mm = 1000.0/211.21` at `folk_gen.py:1884`** — the banned flat px/m, still
  live in the folk-art bake frame; SPEC §10.9's table (~line 2147) still lists
  the retired rake 0.0330; **SPEC §10.3's table still lists the RETIRED red
  (196,106,36)**; `PLATE_W = 0.3300` still has no provenance.
- **NO HERO SINCE REV 16.** `CREAM` did not move, so the hero is **UNBLOCKED**
  and is now the top build item.
