# HANDOFF rev 25 — the bake frame parsed, the artwork re-baked, the hero shot

> **THE STANDARD, in the owner's words, and it governs every line below.**
> The final product should be nearly indistinguishable from the original.
> **Any single measurement off is unacceptable.** We are recreating a photo
> realistic version of **that exact bus**. The criterion is PER-MEASUREMENT.
>
> And above clinical accuracy: *"I really want this to give the person the
> opportunity to feel like they were on Playa del Carmen all those years ago.
> I want the owner to remember standing in the kombi, in this very picture
> that was provided."* — **that owner is the restaurant's owner, not Donald.
> Donald has never stood in the bus.** Ask what a PHOTOGRAPH shows; never ask
> what the vehicle looks like.

---

## 1. Arrival state — rev 25 OPENED CLEAN, sixth revision running

Thirteen bundles crossed the device bridge in **ONE `device_stage_files` call**.
All eight md5s recorded in memory matched. Restore ran
59 → 67 → 71 → 75 → 81 → 87 → 93 → 96 → 101 → 105 → **107, clean tree**, with no
divergent-branches error at any line. **20/20 content checks exact, 8/8
ancestry.** Guards on arrival **0 fail / 0 warn at both levels**, every figure
reproducing rev 24's table.

Blender 4.5.3 + pillow + scipy installed as prescribed.

## 2. Guards at the end of rev 25 — every geometry figure IDENTICAL to arrival

| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 0 warn** | **0 fail, 0 warn** |
| roof crown @ rear axle | **1.9835** (baseline 1.9835, −0.0 mm) | **1.9833** (−0.2 mm) |
| rear arch lip → gap | **0.3722 → 39.7 mm** | same |
| front arch (control) | **0.3732 → 40.7 mm** | same |
| rake | **17.75 mm/m (locked 17.75)** | same |
| dome deficit / rear overhang | +0 / **0.7730** | same |
| dims | L=4.065 W=1.750 | same |
| cut roof hole | **68564v** | **252749v** |
| objects at `materials:` | **126** | **126** |
| shut line × aperture, SHOW | **0.0 mm** | **0.0 mm** |
| shut line × aperture, OFF | **804.9 mm** (baseline 804.9, −0.0) | same |
| `CARGO_GAP` samples | **154** | same |

Also: **185 meshes**, 42 materials, 5 constant-rough, **0 non-manifold**, three
open apertures on +Y, four shut lines 100 % open, band 1.372–1.775, bay widths
**0.516 0.515 0.516**.

**NO GEOMETRY MOVED IN REV 25.** What moved is the ARTWORK — two texture files —
and SPEC/verify hygiene.

## 3. What rev 25 did

### Item 2 first, ahead of item 1 — and the re-ordering was the point

The prompt listed the hero as item 1 and `_ZB_AUTH` / the re-bake decision as
item 2. **They were inverted deliberately**: if a re-bake were owed, `tex/*.png`
would change and a hero shot first would be stale on arrival — exactly the
position rev 25 opened in. It WAS owed. The hero was shot after.

### SPEC §10.68 — the bake frame

- **`_ZB_AUTH`'s claim: magnitude CONFIRMED exactly, conclusion REFUTED.**
  76.222 mm at `x = X_TAIL`, precisely the claimed "up to 76 mm" — but **no art
  is painted anywhere aft of x = −1.40**, so ink-weighted the missing `_aft()`
  re-space is **0.0023 mm**. It is not "larger than `DOOR_X0`"; it is ~7 500×
  smaller. Two controls isolate the mechanisms (re-space 75.540 mm, dropped
  knots 20.925 mm).
- **The real `_ZB_AUTH` defect was never named: five DROPPED KNOTS**, worst at
  **+2.085 on the NOSE** — 19.477 mm peak, **3.53 %** of the primary-copy ink.
- **`DOOR_X0` dominates and is worse than recorded.** `DOOR_REAR_DX = 17.250 mm`
  exactly; the uncomputed consequence is **`DOOR_W` 1.935 % too wide**, and
  `DOOR_W` divides every u of the door art — **82.5 % of door ink displaced
  > 2 mm**, ink-weighted **6.290 mm**, **3 411 px past the true rear shut line**
  (1.44× the whole B-pillar).
- **THE CONTROL FAILED AND THAT WAS THE FINDING.** Re-baking unchanged does not
  reproduce the committed art (4.029 % / 4.261 %, max Δ 255). Determinism checked
  first (two processes, identical md5). A bisect holding the tree at rev 24 and
  swapping in only pre-rev-23 `folk_gen.py` reproduces the committed files
  **byte-identically**. **The model was wearing artwork fourteen revisions old.**
- **Fixed structurally**: a tiny bounded `_ceval` reads `t1_shell`'s constant
  GRAPH and `t1_core`'s `ZB` knots, so `DOOR_X0` is expressed in terms of
  `BAYS[0][1]` and `T1_BPILLAR` moves the ART frame with the geometry. Three more
  re-typed literals removed — **all three still agreed, so exposure, not damage**.
- **Falsification cross-confirmed from an unrelated route:** the B-pillar width
  reproducing the retired `DOOR_X0 = 0.9084` is **−0.005250 m**; §10.62
  independently derived **−0.0053** for the broken GEOMETRY. **0.050 mm apart.**
- **`_DOOR_TOP_AUTH` deliberately NOT parsed** — I wrote "within 1 mm" in my own
  comment before watching it print and the print refuted me at **4.2 mm**. Held
  at the authored 1.8140 so `DOOR_H` stays bit-identical; discrepancy carried
  forward, not absorbed.
- **After the bake:** door ink past the true shut line **3 411 → 0**; sill LUT
  error **76.222 → 0.000000 mm**; §10.10 targets held or improved (flank density
  rms 3.59→3.58 / 3.98→3.96; zone R1 −0.44→+0.29, R2 +0.58→−0.14). **Door gold
  29.09 → 28.90 against 29.08 went the WRONG way** — stated, inside the
  28.96–29.19 round-to-round spread watched printing.

### Item 1 — the hero

`rev25_hero34f.png`, **4800×3200, SUB=2, 56 samples, 20 strips, pad 48**.
**Worst seam z = 1.91** (rev 22 shipped 1.91 at the same size), all 19 seams OK,
interior row-delta mean 0.5915 sd 0.4788 DN. `post.py` run **ONCE** on the
stitched frame: `bloom=0.00`, `backdrop=headroom`. **The first frame ever to
photograph artwork that matches the model's own source.** Strip 9 was killed by
the 10-minute shell limit and its file opened clean; rather than trust that, the
**seam check adjudicated it** — row 1439 delta 0.9256, z +0.70, OK.

### SPEC §10.69 — item 3

`_RETIRED_VALUES` **5 rows → 15**. Nine defects confirmed, each against three
things; **four refuted or mislocated**. Guard fired at all 12 predicted lines,
**no false positives**, then 0.

Two are structural: **§1.1's rows defeat the guard by RE-EXPRESSION** (the
retired taper survives as edge pairs plus the 100 mm origin shift), which is this
guard's real ceiling and is now written down; and **§9 row 10 published the
INVERSE of the guard that runs** — as published it would fail every current build,
and it contradicted §2 inside the same frozen front matter.

## 4. Things the next context must NOT silently undo

`HANDOFF_rev24.md` §4, rev 23's §4, rev 22's §3, rev 21's §4, rev 20's §4,
rev 19's §4 and rev 18's §4 **all still stand in full**. Adding to them:

1. **Do not re-type any constant back into `folk_gen.py`.** Every value there is
   now parsed and the parse RAISES rather than falling back. `_ceval` is
   deliberately tiny — extend it only for node types a real definition uses.
2. **Do not "fix" `_DOOR_TOP_AUTH` to 1.8098** without measuring which is right.
   It is held at 1.8140 on purpose so `DOOR_H` is bit-identical across this bake.
3. **Do not widen `_RETIRED_VALUES`' matching or add exemption tokens.** Its
   substring ceiling is documented in §10.69; the answer to a re-expressed value
   is another ROW, not a looser rule.
4. **Do not add a `_RETIRED_VALUES` row for the ±2.145 bumper faces.** No §10
   entry retires either value; a row would assert a retirement that does not
   exist. It is an open item, not a guard.
5. **`tex/nose.png` is unchanged and must stay so** unless the nose bake itself
   is re-derived — it is independent of the flank frame.
6. The off-flank crossing baseline (804.9 mm ± 10 mm) and the `H_ROOF` regression
   band (1.9835 ± 5 mm) **must never be tightened**. Both are labelled catchers.

## 5. Still open

- **`CREAM`** — needs a same-light, same-CLASS, three-channel reference. **Does
  not exist in the three photographs.** Unchanged at (206,208,200).
- **THE ABSOLUTE ROOF HEIGHT** — 1.960 retired, nothing replaced it.
- **`COUNTERTAN`'s ~59 % pedestal** — dust, wear, fade, coat+spec, interreflection
  and occlusion all excluded. **STILL UNIDENTIFIED.** `k` is 40 % larger than
  believed — **re-derive, never carry the old secant gain.** NOT touched in rev 25.
- **THE OFF FLANK** — two mutually contradictory **E** features, 804.9 mm.
- **`_DOOR_TOP_AUTH`** — authored 1.8140 vs the outline's top-run mean 1.80980.
  **4.2 mm, NEW this revision, and neither value is measured against a photograph.**
- **Bumper faces `±2.145` (SPEC `:191`) vs `X_BUMP_F/R = ±2.140`** — a real 5 mm
  drift with **no retiring entry**. Establish which is right, then retire one.
- **`X_NOSE` and `X_TAIL` are parsed in `folk_gen` and never LOADED** — an AST
  census gives 1 Store, 0 Loads each. Harmless but it makes `_from_module` raise
  over three values nobody uses. Verified, not fixed.
- `PLATE_W = 0.3300` has no provenance. `probe_rev16.py:90` prints `xa` vs `xa`.
- Tail-lamp material slot; `Senor` at 0.504 of its 0.782 ceiling; `SCR`'s +80 mm.
  **None started in rev 25.**

## 6. Ordered work list for rev 26

1. **`COUNTERTAN`'s ~59 % pedestal** — name the next suspect and ablate it.
   Oldest undone measurement item; sixth revision on the list. **Re-derive `k`.**
2. **`_DOOR_TOP_AUTH`** — decide it with a measurement, then re-bake if it moves.
   Cheap, and it is the only thing rev 25 left half-settled.
3. **The ±2.145 / ±2.140 bumper drift** — establish which is right and retire one.
4. Tail-lamp material slot; `Senor`'s letterforms; `SCR`'s +80 mm.
5. A hero only if geometry or artwork moves again. `rev25_hero34f.png`
   photographs the current mesh AND the current artwork.
6. Camera absolutely last.

**NO DECISION IS OUTSTANDING WITH DONALD.** rev 25 asked no photograph question —
it was a measurement, bake and hygiene revision and had none a photograph could
answer. The one photograph that would move most still closes THREE things: a
head-on rear/front elevation from roof height closes `CREAM` and the absolute
roof height; a clear off-flank view closes 804.9 mm of unadjudicated crossing.
