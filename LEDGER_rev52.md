# LEDGER rev 52 — the fidelity lane revived, and the number it was red on was the instrument

Scope of this revision: `§5 item 2` of `NEXT_CONTEXT_PROMPT_rev52.md` — *"REVIVE THE
FIDELITY LANE"*. Item 1 (the two VW badges) is untouched and still blocked on
`PHOTOS_WANTED` item 7. Items 3–7 are untouched. Read that brief's §5 for what remains.

---

## §0. WHAT WAS MEASURED, WITH ITS CEILING

`flank_compare.py` — the render-vs-photograph gate — was RUN, not grepped. It had not been
run since rev 40. On `out/r52_side.png` (1600x1100, 96 spp, T1_SUB=1, HEAD = `04ee942`):

| check | rev 40 | rev 52 as found | rev 52 after the fix below |
|---|---|---|---|
| ink area ratio | — | 0.8751 **FAIL** | **0.9446 PASS** |
| ink aspect | 2.3622 | 2.3689 FAIL | 2.3689 **FAIL, unmoved** |
| IoU vs ceiling | 0.7535 (0.877 of 0.8591) | 0.7350 | **0.7623** |
| worst region `Senor` | **0.459** | **0.174** | **0.480** |

**The gate still FAILS, 2 of 4.** It is not fixed and this revision does not claim it is.

## §1. THE RECONCILIATION THE BRIEF ASKED FOR — IT WAS NOT A TYPO AND NOT A REGRESSION

The brief carried `Senor` at **0.174** (rev 51) against **0.459** in the `LEDGER_rev44`/`rev45`
open-findings register, and said *"Reconcile them; do not assume a typo."* Both are real
readings of the same instrument in the same units. Four candidate causes were raised and
**each was killed by its own control**, in this order:

| candidate | verdict | the control that killed it |
|---|---|---|
| units — raw IoU vs fraction-of-ceiling | refuted | both ledgers say *"of its own ceiling"*; `SPEC.md` carries rev 40's raw 0.7535 separately |
| the ceiling (denominator) rose | refuted | 0.8591 (rev 40) vs 0.8592 (rev 51, implied by its own `>= 0.7303` bar). The ceiling is `iou(reference, reference shifted 1 px)` — **it never touches the render or the texture**, so it cannot move for a model change |
| `tex/senor.png` changed at rev 46/47 | refuted | alpha coverage 0.2888 -> 0.2889; the change is 0.84 % of pixels, diffuse across all 16 column bands — anti-aliasing removed, not glyph shapes moved |
| the panel `SCR` moved | refuted | byte-identical in `build.py` between rev 40 and HEAD |

**The cause is a mask selecting the wrong pixels** — this project's most-repeated defect, and
the one `CLAUDE.md` carries as a `YOU MUST`. It was found by PAINTING the four tarnish zones
onto the render and LOOKING, not by reasoning.

## §2. THE DEFECT, BY STRING

`flank_compare.py` carries the reference rule's four tarnish zones across to the render through
`LOCKUP -> SCR` and re-measures each zone's endmembers **in the render** — rev 17's fix, which
took `Senor` from 0.126 to 0.504. Each zone fitted `endmembers()` over **the whole zone**:

```
sub = crop[zm].reshape(-1, 1, 3)
```

The `"enor"` zone maps onto a render box that is **16.5 % bright silver** — the top of
`Tacombi`'s swash rides up into it. `endmembers()` splits on the redness-histogram valley, so
with silver present the valley separates SILVER from {tarnish + red} instead of tarnish from
red. Measured, per zone, in the run's own printout:

| zone | silver-rule already claimed | ink endmember | T | px rescued |
|---|---|---|---|---|
| `S` (works) | **0.0 %** | (160,108, 96) tarnish | 0.2192 | **+346** |
| `enor` | **18.6 %** | **(165,158,160) NEUTRAL** | **0.1086** | **+0** |
| `b` flag | 29.7 % | (182,172,174) neutral | 0.1105 | +2 |
| `i` dot | 35.6 % | (162,152,154) neutral | 0.1267 | +2 |

The `enor` window rescued **zero** of the **81.7 %** of itself that is genuinely tarnish.
Brightest-5 % RGB in that box is (170,166,168), matching the hijacked endmember; in the `S`
box it is (168,122,109), matching the working one. **That is the whole of the 0.459 -> 0.174.**

## §3. THE FIX, AND THE ABLATION THAT WATCHES IT FAIL

A tarnish zone exists to find ink **the silver rule could not see**, so pixels that rule has
already claimed are by construction not the population being estimated. The endmember sample
is now `smp = zm & ~raw`, falling back to the whole zone if fewer than 40 px remain.

* `T1_TARNCONTAM=1` restores the contaminated sample. **Watched:** it reproduces
  ink (165,158,160), T 0.1086, +0 px, `Senor` 0.174 exactly.
* **Untouched control:** the `S` zone is 0.0 % contaminated and is **bit-identical** before and
  after (+346 px, T 0.2192) — the change moves only contaminated zones.
* Two `verify_clone.sh` rows added, **both watched failing** (on deletion, on removal, and —
  after the first version was found to be a substring match that a suffix defeated — on append).

## §4. WHAT THE FIXED NUMBER MEANS, AND ITS CEILING

`Senor` reads **0.480 of its own 0.780 ceiling**, against **0.459** at rev 40 and **0.504** at
rev 17 — consistent, and the reconciliation closes. Its texture-only control reads **0.504** in
the same box. The gate's own decision rule is that where tex-only is **as low as** the render
column the fault is the panel and the reconstruction, not the render — 0.504 against 0.480 now
satisfies that, where 0.504 against 0.174 did not. **So the residual `Senor` failure is
open-findings row 18, *"the `Senor` reconstruction"*, exactly as rev 17 said — and the render is
not what is wrong with it.** `senor_trace.py` calls the remedy *"inventing ink the photograph
does not show"*, so this stays an OWNER RULING (brief §5 item 7, A12), not a do-now.

**CEILINGS, carried:**
* The gate's own PSF block puts the reference ink's p10 stroke at 4.0 px against a 3.98 px
  FWHM — **at the resolution limit**. There is a floor under `Senor` and `swash` that no
  threshold rule can lift, and 0.480 is not corrected for it.
* The `verify_clone.sh` rows added here are **SELF-CONSISTENCY, not fidelity**. That script
  cannot render. They hold that the fix and its ablation are still in the source; they do not
  and cannot check what the windows rescue. Only running the gate does that.
* This revision changed **an instrument, not the vehicle**. No geometry moved. `STATE.md` is
  unchanged by design.

## §5. CORRECTIONS TO THE INCOMING BRIEF (rule 15 — a retraction in a ledger only is half a retraction; these are also at the site in the source)

1. **"ONLY THE WORST-REGION NUMBER IS ROBUST" is REFUTED, and it is backwards.** The
   worst-region number was the *least* robust of the four — it was the one the contaminated
   window destroyed, moving 0.174 -> 0.480 with no change to the model. The brief reached the
   right conclusion (chase the worst region) from a wrong premise.
2. **"FAIL ink area ratio 0.8751" was the SAME defect, not a separate finding.** It PASSES at
   0.9446 once the window is fixed. Two of the brief's three FAILs were one cause.
3. **The aspect FAIL is unmoved at 2.3689** and remains what the brief says it is — a
   calibration ambiguity (`k_t` *"is known to be wrong somewhere"*), not a shape finding.
4. `flank_compare.py` *"last touched at rev 40"* — **confirmed** (`2e20da1`).
5. The guard-gap claim (*"not one `ck` row mentions a wheel, hub, cap, rim or vent"*) —
   **confirmed**; the only apparent hit is the substring "vent" inside "in**vent**ed".
6. `cream_rms.py` **is a second dormant render-vs-photograph gate** with zero rows in either
   acceptance script — the brief was right to point at it. `mark_rev45_ba.py` is **not** the
   same shape: it is a question-figure generator, not a gate. **Neither was run this revision.**
7. **NOT VERIFIED, carried forward:** `verify_clone.sh` now contains 132 `ck` lines against
   129 reported checks. The discrepancy was noticed, not chased.

---

# §6. A6 — THE CHIP GATE, RE-BASED AND MEASURED. **NOT SHIPPED AS THE DEFAULT.**

Brief §5 item 3. `LEDGER_rev51` §6 left A6 *"diagnosed, not fixed"*, and said why: *"validating a
shader change needs before/after renders at 6–15 min each."* Three full renders were run here.

## §6.1 The instrument, built and calibrated BEFORE it measured anything

Rev 51's estimator was never committed as a runnable probe, so this is a **reconstruction**, and it
was calibrated on the record's own two controls first:

| control | record | this estimator |
|---|---|---|
| flat cream + 0.5 DN noise | 0.00 % | **0.000 %** |
| flat cream + known chips | 6.58 % (true 7.6) | **7.316 % (true 7.32)** |

**CEILING:** absolute percentages are NOT comparable to rev 51's 17.06 % — different estimator,
window and erosion. Only comparisons made *through this one estimator* are meaningful, and every
comparison below is.

## §6.2 THE WINDOWS — AND FOUR OF MY OWN WERE WRONG

The class is defined **relative to each image's own cream**: the photograph's cream is warm
(R−G median 22), the render's is neutral (R−G median 2), so a fixed cut keeps only the
photograph's most neutral pixels — a ragged mask that would have excluded exactly the darker
pixels a chip statistic counts. Caught by painting it. Then, on the second pass:

* a "cab roof cream" window that was **on the white background**;
* a "nose cream" window that was **on the white background**;
* an "upper body cream" window that was **on the bulb string** — the identical defect rev 51
  recorded;
* a "cantrail" window that was **on the window glass**.

**All four read a plausible 0.00 % and would have been published as evidence of confinement.**
Every one was caught by PAINTING the selection and looking; none by reasoning. **A white studio
background passes a "bright and neutral" cream test** — that is the trap specific to this delivery
genre, and it is new to the record.

## §6.3 THE MEASUREMENT, on painted and eye-verified windows only

| window | pre-change | default after the edit | `T1_EDGEBEVEL=1` | photograph |
|---|---|---|---|---|
| counter fascia (detail geom) | dark **4.07 %** p2 −0.062 | dark 4.05 % p2 −0.062 | dark **0.10 %** p2 −0.003 | **0.00 %** p2 −0.009 |
| cab lower cream (SHELL) | 0.00 % p2 −0.003 | 0.00 % p2 −0.003 | 0.00 % p2 −0.003 | — |

**The default path is INERT:** 4.07 → 4.05 % with p2 unchanged. The whole-frame residual against
the pre-change render is salt-and-pepper — 32 006 blobs averaging 1.8 px, **median difference
0.000 DN** — i.e. Cycles sampling noise, not a structural change.

**The lever moves the chip gate ALONE**, which is what the brief said A6 never had
(`T1_CTAN_WEAR` also drops Metallic): the fascia falls 40×, the verified shell window does not move.

## §6.4 WHY IT IS NOT THE DEFAULT — THE POSITIVE CONTROL FAILED

`T1_EDGEBEVEL=1` does **not move the chips to the edges. It removes them.** Looked at, not inferred:
at 8× on the counter lip the fascia comes back clean with **no chipping at the lip either**. The
arithmetic says why, and it was predictable: the radius is `GAPW/2 = 2.75 mm`, and at the side
view's **271.2 px/m that is 0.75 px** — the edge band is **sub-pixel at every scale this project
renders**. SPEC §3 locks the finish WEATHERED, so making this the default on self-review would
trade a measured defect for an unmeasured one.

**The mechanism is right and the scale is not.** A Bevel node is mesh-density independent in
exactly the way Pointiness is not, and `edge = 1 − dot(bevel_normal, true_normal)` is **0 on a flat
face by construction**. What is missing is a radius grounded in **how big a real chip is in a
photograph** — a measurement nobody in this project has made. The window is expressed as fractions
of a 90° fold (`W_EDGE_90 = 1 − cos 45°`) so it moves with geometry, but **the 0.10 / 0.50 fractions
are chosen, not measured, and no frame has ever been compared against them.** That is the ceiling.

**OPEN, and it is an owner question, not a do-now:** the photograph's fascia reads **0.00 % dark** —
on that one surface the real vehicle is *not* chipped, so removing the chips there is closer to the
photograph than keeping them. Whether that holds across the vehicle cannot be settled from the
frames held.

## §6.5 Guards

Three `verify_clone.sh` rows, **each watched failing on the defect it exists to catch** — a silently
flipped default, a removed lever, and a typed window replacing the derivation — and passing when
restored. They are SELF-CONSISTENCY rows: that script cannot render, so it cannot check any of §6.3.

---

# §7. A9 — `gal_rail` AND `gal_caddy_fill`, MEASURED ON THE MESH AND FIXED

Brief §5 item 5. Both were confirmed by **asking the mesh**, not by reading the source.

| | built, measured | after, measured | the record's figure |
|---|---|---|---|
| `gal_rail` centre | **−0.3800** | **−0.5980** | −0.598 |
| `gal_rail` length | **0.6600** | **0.4949** | 0.495 |
| hooks hanging on nothing | **3 of 6** | **1 of 6** | survey finding 28 |
| `gal_caddy_fill` vs its caddy | **+24.0 mm PROUD both ends** | **−24.0 mm inset** | inset |

**The rail is DERIVED now, not typed.** Its own measurement is *"bay 3, u 0.02–0.98"*, so it is built
from `BAYS[2]`, which carries the 0.5155 bay width and the −0.5980 centre. As built it spanned
X −0.050 … −0.710 — running forward across the pillar into `BAYS[1]`, where a rail measured in bay 3
cannot be. `T1_RAILSTALE=1` restores the typed rail.

**`gal_caddy_fill`'s inset was inverted by authoring order.** `(bx0, bx1)` is written high-then-low
(−1.0420, −1.1550), so `bx0 + 0.012, bx1 - 0.012` *expanded* the box instead of insetting it. It now
insets from the ordered edges, so the sign cannot invert again. Its own kill test is in the same
block: the fill's top is 3 mm *below* the caddy rim, so it was always meant to sit inside.

## §7.1 CORRECTIONS TO THE RECORD

1. **The brief dropped the headline finding.** `SURVEY_rev49` finding 28 is *"[MAJOR] Three of the
   six S-hooks in bay 3 hang in mid-air"*; the rev-52 brief compressed this to the rail's length and
   station and **lost the hooks entirely**. The hooks are the visible defect; the rail is the cause.
2. **The survey's headline mis-signs it, and the brief was right to say so** — verified here at the
   site: line 280 says *"165 mm too short"*, its own body says built 0.660 against measured 0.495,
   which is 165 mm too **long**. The body is right. The brief inherited "too LONG" correctly.

## §7.2 STILL OPEN — AND FIXING THE RAIL CANNOT CLOSE IT

**The sixth hook, at X −0.907, lies 51.4 mm beyond `BAYS[2]`'s own aft edge (−0.85575).** It is
outside bay 3 altogether, so it cannot hang from a rail that is measured as *"bay 3, u 0.02–0.98"*
no matter where that rail is put. The six hook stations are six typed literals with irregular
spacing (69, 105, 73, 79, 78 mm), i.e. read off a photograph; their own span centre is **−0.705**
against the rail's measured **−0.598**. **The hook stations and the bay measurement disagree, and
one of them is wrong.** This revision did not resolve it and did not pretend to: the rail was moved
to the figure the record carries, and the residual is recorded here rather than absorbed.
