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
