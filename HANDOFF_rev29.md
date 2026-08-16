# HANDOFF rev 29 — 2026-08-16

**Commits: see §7. Clean tree. Guards 0 fail / 0 warn at BOTH subdivision
levels.**
**NO GEOMETRY MOVED. NO ARTWORK MOVED. ONE CONSTANT WAS RETIRED.**

> The standard, in the owner's words: *"The final product should be nearly
> indistinguishable from the original. **Any single measurement off is
> unacceptable.**"* The criterion is PER-MEASUREMENT. And above clinical
> accuracy: *"I really want this to give the person the opportunity to feel
> like they were on Playa del Carmen all those years ago."* **That owner is
> the restaurant's owner, not Donald.**

---

## 1. How rev 29 opened

**NOT CLEAN — the same environmental failure rev 28 hit, and Step 0 caught it.**
`get_device_info` returned `connectedFolders: []`. The first
`device_request_folder_access` **timed out unanswered**; the second was granted.
Step 0 of the rev-29 prompt is what made this cost minutes instead of the hour
it cost rev 28. **Keep it as Step 0.**

Once granted:
- **SEVENTEEN bundles crossed in ONE `device_stage_files` call.**
- Restore 59 → (fetch b14) → 67 → 71 → 75 → 81 → 87 → 93 → 96 → 101 → 105 →
  107 → 115 → 120 → 126 → **130, clean**, no divergent-branches error. Every
  intermediate count hit its expected value exactly.
- **19/19 content checks exact, 8/8 ancestry**, three texture md5s correct
  (`swirl.png` `4ee4e09e`, `swirl_b.png` `d201597e`, `nose.png` `b31ea156`).
- Guards on arrival **0 fail / 0 warn at both levels**, every figure in the
  rev-29 prompt's §2 table reproduced.
- Blender 4.5.3 + pillow 12.3.0 + scipy 1.17.1.

---

## 2. §10.82 — `W_DUST_FAC_UP` IS A GLOBAL LEVER, AND IT IS NOW RETIRED

### The scope, by EXECUTION not by reading

`t1_mats.py:366` and its live assert both describe `W_DUST_FAC_UP` as *"mean
coverage 0.548 **on the counter top**"*. **It is one MULTIPLY node inside the
file's ONE shared `WEATHER` node-tree, reaching ELEVEN materials.**
`probe_dust_scope.py` (NEW, read-only, 8 asserted controls):

| | |
|---|---|
| distinct `WEATHER` node-trees in the file | **1** — the lever is global BY STRUCTURE |
| materials reached | **11** — `T1_paint`, `cream`, `bumpercream`, `countercream`, `countertan`, `wheelcream`, `capwhite`, `capred`, `roundelred`, `calidad`, `script` |
| mean coverage | **0.3916** at `dust=1.0`, **0.5483** at `dust=1.4` |
| total filmed up-face area | **6.3354 m²** |
| of which `countertan` | **0.8645 m² = 13.6 %** |
| largest single surface | **`T1_body` / `T1_paint`, 12.3697 m² — THE ROOF** |
| falsification arm `T1_W_DUP=0` | **all ELEVEN rows go to 0.0000** |

### The owner reading

> [stated] **The ROOF in `ref_rear34.jpg` is CLEAN.**

Asked as multiple choice, with the crop box **printed**, the box stated to be a
**POINTER**, the photograph shown **BESIDE a render of the current build** with
the film ON and OFF, and rev 28's already-answered counter-top box drawn
alongside in a different colour as his own scale. `rev29_q1_roofdust.png`.

**This is what SPEC 10.81 was missing.** 10.81 barred a blind `f = 0` because
the counter reading is LOCAL. The roof reading contradicts the film on **86.4 %
of the area it paints**.

### The retirement — a DERIVATION retired, not a constant tuned

`W_DUST_FAC_UP` **0.7313 → 0.0**.

- **The old derivation assert is RETIRED, NOT WIDENED.** At `f = 0` it misses by
  **0.2335**, a hundredfold: it compares a clean top with a measurement of a
  dirty one. SPEC 10.59's shape — the owner withdrew the target.
- **Replaced by a narrower assert that CAN fail** (`_f_up == 0.0`) plus a
  road-film-untouched assert. **FALSIFIED IN SEVEN ARMS, every one watched.**
- **SPEC 10.76's catcher DELIBERATELY RE-BASELINED** to
  **(−0.023400, −0.037000, −0.120500)**, band UNCHANGED at 2e-3. At `f = 0` the
  residual is exactly `COUNTERTAN − _UP_MEASURED`, so **the catcher is now
  STRONGER** — no dust term stands between the two constants it watches.
- **Two `_RETIRED_VALUES` rows**, `0.7313` and `mean coverage 0.548`.

### Two defects in my own probe, and three wrong thresholds

1. **C1 failed at 9.34e-09; the premise was mine** (sixth instance). The node
   socket is **float32**, so the shader's dust is `1.3999999761581421` and the
   shipped coverage is **0.54825560066326251** against the assert's
   **0.54825560999999989**. Irrelevant at 1.7e-08 relative — **but a figure
   nobody had watched.**
2. **My first area estimator was wrong**, caught by *"two rows agreeing exactly
   are a bug until checked"*: `counter` and `counter_top` both read **7.2332 m²**
   on a 1.750 m body. `counter_top` is a concave U-gon wrapping the tail; a fan
   of `|cross|` cannot cancel overlap. Now Newell, **and the retired method is
   PRICED at +50.0 %** on a synthetic U-gon of analytic area 6.
3. **Three straddle thresholds of mine were wrong before one was right.** The
   final band has **NO FREE PARAMETER**: it is calibrated against a PROVEN
   straddler (14.14 × its floor) and a box the owner **had already answered**
   (3.08 ×). The roof pointer reads **3.30 ×** — 20.6 × closer to the answered
   anchor than to the straddle.

---

## 3. What rev 29 did NOT do — named, not hidden

- **The FRONT OVER-RIDER (§10.75, §10.80) was NOT ATTEMPTED.** It is still the
  oldest undone item. The PSF blocker is cleared; what remains is **a scale on
  the nose/bumper plane, or a proof that none is admissible.**
  **rev 29's one contribution to it is negative and worth carrying:**
  REF §9's **422 px/m** is a *local* scale on the NEAR SIDE of the front panel,
  anchored on the headlamp aperture at 0.180 m, and REF states in the same
  breath that *lateral scale varies by more than 2:1 across the front panel and
  a fitted projection model did not close*. The over-rider tube sits at
  `u 260–286`, the headlamp at `u 419` — far apart laterally, on a panel whose
  lateral scale is explicitly not usable. **The most promising untried route is
  a scale-free RATIO at the same station**: the tube's vertical thickness
  against the **bumper blade's face height in the same columns** (REF §2:
  0.133 m at S = 211.2; V2: 0.123 m at S = 211.5; stock T1 ≈ 0.12 m — an 8 %
  spread that must be carried). That needs an owner reading first, because rev
  26 found the trolley occludes the blade's lower edge in 5 of 8 columns.
- **The residual 6.6/6.6/8.5 % pedestal — NOT STARTED.** Note it is now
  measured on a build whose dust film is gone; **§10.70's arms must be re-run
  before any of its percentages are quoted again.**
- **NO HERO WAS SHOT, AND ONE IS OWED.**

---

## 4. Things you must not silently undo

`HANDOFF_rev28.md` §4, and rev 27's §4, rev 26's §4, rev 25's §4, rev 24's §4,
rev 23's §4, rev 22's §3, rev 21's §4, rev 20's §4, rev 19's §4 and rev 18's §4
**all still stand in full**, except where §10.82 explicitly retires them.
Added by rev 29:

- **`W_DUST_FAC_UP = 0.0` is a RETIREMENT ON TWO OWNER READINGS, not a tune.**
  Restoring 0.7313 in source FIRES an assert. To render the retired arm use
  **`T1_W_DUP=0.7313`**, which is deliberately still supported.
- **The SPEC 10.76 catcher's new baseline (−0.023400, −0.037000, −0.120500) is
  a DELIBERATE re-baseline after a deliberate change. Do NOT tighten it, do NOT
  tune to it, and do NOT restore the rev-26 figure** — that figure is
  unreachable by construction now.
- **Both `_RETIRED_VALUES` rows must stay.** `0.7313` and `mean coverage 0.548`
  are the same retirement in two forms; a substring guard needs both.
- **`rev25_hero34f.png` NO LONGER PHOTOGRAPHS THE CURRENT BUILD.** Geometry and
  artwork are unchanged, but the shading moved on eleven materials.
- **The bumper top, the rim barrels and the hub caps are filmed by the same
  node and NOBODY HAS BEEN ASKED about them.** The retirement asserts more than
  two readings strictly support. If a frame ever shows them, ask.
- **`probe_updust_pointer.py`'s band has NO FREE PARAMETER on purpose.** Do not
  replace it with a fixed percentage — three fixed percentages were tried and
  all three were wrong.

---

## 5. Still open

- **THE FRONT OVER-RIDER** — see §3. Blocked on a plane scale or a proof.
- **`COUNTERTAN` / `CREAM`.** Retiring the film did NOT fix it: a clean top is
  still **34.0 % short in B**. `CREAM` still needs a same-light, same-CLASS,
  three-channel reference that does not exist in the three photographs.
- **The residual pedestal — the scene→top bounce.** Re-run §10.70's arms first.
- **THE FRONT BUMPER FACE IS UNMEASURED** — both catalogue values struck.
- **THE ABSOLUTE ROOF HEIGHT. THE OFF FLANK, 804.9 mm.**
- The cab door's true top edge — authored; unmeasurable.
- `GAL_SKY` is a dead lever. `PLATE_W = 0.3300` has no provenance.
  `probe_rev16.py:90` prints `xa` vs `xa`.
- **D1/D4/D8 unmeasurable**; D1 misses the monotone threshold by 0.0002.
  **Do not widen it to collect D1.**

---

## 6. Process rules earned in rev 29

- **COMMIT BEFORE FALSIFYING.** A `git checkout <file>` used to undo a
  falsification arm destroyed unrelated uncommitted work **TWICE** — once on
  `t1_mats.py`, and then on `SPEC.md` **twenty minutes after I had written the
  rule into SPEC itself.** Both recovered, both recorded. *Writing a rule down
  is not the same as having it.*
- **A THRESHOLD IS A PROBE TOO.** Three of mine were wrong. The one that is
  right has no free parameter because it is calibrated against a box the owner
  had already successfully answered.
- **CALIBRATE AGAINST AN ANSWERED QUESTION.** The strongest available control
  on "can this be answered" is a box that was answered.
- **A NUMBER COMPUTED ONE WAY IS NOT A NUMBER COMPUTED ANOTHER WAY.** rev 28's
  0.0 %/0.6 % and this file's 5.4 % are the same box under different
  statistics; comparing them is the carried-forward-figure trap.
- **CHECK WHICH SECTION A GUARD CAN SEE.** My first falsification of the two new
  retirement rows did not fire and **the guard was right** — I appended inside a
  §10 body, which it deliberately does not scan.
- **CHECK THE LEVER REACHES ONLY WHAT YOU THINK** — seventh instance, and this
  time it converted a barred repair into a supported one.

---

## 7. Deliverables

`tacombi_rev29_incremental.bundle` (applies onto the rev-28 tip),
`tacombi_rev29_tree.tar.gz`, `SPEC_rev29.md`, `STATE_rev29.md`,
`HANDOFF_rev29.md`, `NEXT_CONTEXT_PROMPT_rev30.md`, plus the question figure
`rev29_q1_roofdust.png`.

**A HERO IS OWED.** `rev25_hero34f.png` is now stale for shading.
