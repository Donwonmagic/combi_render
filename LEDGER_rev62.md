# LEDGER — rev 62

**Every figure this revision produced, with how it was obtained and what it is ceilinged by.**
Nothing here is transcribed from a paragraph. Where a number replaces an earlier one, the
earlier one is shown struck rather than deleted.

---

## §0 THE ONE-LINE SUMMARY

**Rev 62 answered the brief's ranked item 1 IN THE NEGATIVE, and found that the instrument the
question rests on has a silent failure mode.** The question was *"which of L1–L6 is wrong?"*. The
answer is **not L6** — refuted by ablation — and the workshop badge **cannot decide it**, which is
the second route that frame has failed on, for the same underlying reason both times: **the
pressing is chrome, and chrome has no flat tone to threshold.**

**And rev 62 got a RULING and shipped it.** He was shown the `Señor` figure and chose *"bright
silver, same as Tacombi"*, which overrides SPEC §3's WEATHERED lock **for that word only**.

**Rev 62 changed no geometry.** Zero files under `t1_*.py`, `build.py`, `studio.py` are touched.
`STATE.md` is therefore legitimately unchanged, and that is a CONTROL, not an omission — rev 61
shipped a stale `STATE.md` and an adversary caught it.

---

## §1 WHAT SHIPPED

| change | file | evidence |
|---|---|---|
| `SENOR_TARNISH = 0.0` — the `Señor` word renders as clean silver | `script_gen.py`, `tex/senor.png`, 2 rows in `verify_clone.sh` | **his ruling**, asked with `probe_scratch/rev62_q_senor.png`. Word luma **117.1 → 201.1** against a clean silver of **210.9**. `T1_SENOR_TARNISH=1` restores the pre-ruling texture **byte for byte** |
| `probe_rev62_landmarks.py` — the cross-frame landmark route, C8's target swept, and the stroke-weight ablation | new | §2, §3, §4 |
| `probe_rev62_senor.py` — separates SIZE from WEIGHT | new | §5 |
| F151–F155 into the register | `OPEN_FINDINGS.md` | with grades |

---

## §2 THE EMBLEM — F153. THE WORKSHOP BADGE DOES NOT DECIDE IT, AND L1 IS CORROBORATED

The brief prescribed re-deriving L1–L6 on `ref_workshop.jpg`'s badge (1.71× the area of the
50×69 source every constant was fitted to) under F141's pressing-is-geometry corollary. Taken.

**THE RULER CANNOT DRIFT.** `probe_rev62_landmarks.py` does not re-implement `runs_of()`,
`transitions()`, `landmarks()` or `cell_elongation()`. It lifts their **source text** out of
`probe_rev46_vw.py` with `ast` at run time. **C0w** proves the lift reproduces that probe's
published nolita landmarks to **0.00003**.

```
              nolita   workshop     delta
    L1        0.1940     0.1957    +0.0016     <- CORROBORATED
    L2        0.3433     0.3261    -0.0172
    L3        0.4776     0.5109    +0.0333
    L4        0.8060     0.7609    -0.0451
    L5        0.2361     0.2685    +0.0324
    L6        0.1528     0.1204    -0.0324     <- the largest, and the stroke width
```

**AND THE SCALE CONFOUND EATS A THIRD OF IT.** Resampling the workshop badge down to the nolita
badge's raster scale moves L6 **0.1204 → 0.132 ± 0.013**. At matched scale no landmark's gap
clears its own combined spread by more than ~1.5 σ. **The result is a CEILING: it cannot be
recovered from what we hold.** What *is* recovered is **L1**, agreeing to 0.0016 across two
vehicles, two segmentations and 1.71× the area.

### §2.1 MY FIRST MASK WAS WRONG, AND SO WERE TWO OF MY OWN CONTROLS

**Rule 4, and it is the whole reason §2's numbers are trustworthy.** At threshold 118 the mask
took **the left flank of every stroke and nothing else**. The pressing is chrome lit from the
right, so each stroke is a shadow flank beside a specular flank, and a low level threshold eats
one and drops the other. **That is F08's recorded failure mode arriving on a new statistic.**

It produced six plausible deltas — **L3 −0.3128, L2 −0.2554** — and every one was an artefact.
None was caught by reasoning; it was caught by painting the mask and looking at it.

* **C2w compared CROP MARGINS, not badges.** It failed on a correct mask. Withdrawn and replaced:
  it now tests the mask's vertical span against **F09's independently-fitted conic** (vertical D
  92.728 px, 685 rays), and agrees to **0.7 px** — two independently obtained quantities.
* **C3w was aimed at the workshop WALL AND FLOOR**, not the vehicle. It fired for the wrong
  reason. Re-aimed at plain nose cream and green stripe beside the badge.

The cells read **190..215** and the pressing **83..155**, so the separating level is ~165, not
~118. The repaired mask is stable in count and topology over **145..180**.

---

## §3 C8's OWN TARGET — F151. A SILENT FAILURE MODE, AND NOTHING SWEEPS IT

`cell_elongation()` takes its measuring region as an ellipse inscribed in **the mask array's
rectangle** at frac 0.97 — `n0, n1 = mask.shape` — **not in the measured badge**.

```
crop window            target
    +-0 px  (shipped)   3.390
    +-1 px              3.188
    +-2 px              2.950
    +-3 px              1.553   <- the built glyph reads 1.49
```

At ±3 px the disc escapes the roundel. The cream nose **outside** the ring becomes a **479 px**
"cream cell" against the true cells' 215, **39 % of it outside the ring's own bounding box**, and
the target collapses. **At that window C8 reports the owner's top defect CLOSED and no control
fires.** C1 sweeps six thresholds × five windows for L1–L6; this target is swept by nothing.

**THE VERDICT SURVIVES; THE CEILING DOES NOT.** Within ±2 px the target reads 3.390 / 3.188 /
2.950, and the segmentation sweep (R > 90..140, G,B < 0.50..0.70 R) gives **2.969 .. 3.415**. So
the built glyph is **1.99× .. 2.27× too round — a RANGE, not the point 2.27× that four documents
quote.**

**A HYPOTHESIS OF MINE, REFUTED BY READING THE SOURCE.** I suspected the 3.39 was inflated by the
badge's foreshortening. It is not: `cell_elongation` already corrects it with
`squash = mask.shape[0]/mask.shape[1]`. Recorded as refuted rather than dropped.

**AND A STALE FIGURE IN THE SHIPPED PROBE.** `probe_rev46_vw.py`'s own header says
*"photograph 3.33"* under a "WATCHED, all of it" banner. It prints **3.39**.

---

## §4 THE STROKE-WEIGHT LEVER — F152. RULE 36, AND IT DECIDES §2

**F102 swept `T1_VW_WFRAC` and called it inert. That was against C6, THE CELL COUNT. C8 did not
exist until rev 61**, so the lever for the landmark §2 accuses had never been tested against the
statistic that measures the defect.

```
    wfrac    elongation   cells
    0.08        1.76        5
    0.10        1.82        5      <- the construction's limit
    0.12        1.49        6      (69-row reading 1.88 -- see below)
    0.1986      1.49        6      <- SHIPPED
    0.28        1.45        6
    0.36        1.32        6
    0.44        1.07        6
```

**It moves the WRONG WAY** — thicker strokes give rounder cells — so F102's "inert" verdict was
about the count only. **Thinning to the construction's limit reaches 1.82 against 3.39, 54 % of
the way, and costs a cell.**

**SO L6 IS NOT THE ANSWER.** Abandoning the stroke-width landmark **entirely** still cannot reach
the target. Refuted by ablation, not by argument. This extends F137: the landmark bar is not what
is holding elongation down.

**AND C8's CLAIMED SCALE-STABILITY DOES NOT HOLD ACROSS THE SWEEP.** At wfrac 0.12 it reads
**1.49 at 276 rows against 1.88 at 69**. The stability C8 advertises is a property of the shipped
point, not of the statistic.

---

## §5 `Señor` — F154. THE BRIEF'S DIAGNOSIS IS HALF WRONG

The brief's item 2 says *"The deficit is letterform SIZE and WEIGHT across the whole word."* A
weight fix and a size fix are different edits.

**THE SEPARATING STATISTIC is FILL WITHIN THE GLYPH'S OWN BOUNDING BOX.** Shrink a word and it is
unchanged; thin its strokes and it falls. It is invariant to **both** scale and registration
shift, which is what makes it usable on an overlay that has been registered.

```
    region                     bbox w/h        ink    fill-in-bbox
    S + tilde (Senor)        0.833 x 0.857   0.777       1.088
    Tacombi body (control)   0.950 x 0.902   0.874       1.019
```

**NEITHER IS BELOW 1. THE WEIGHT HALF IS REFUTED** — the strokes are not thin anywhere in the
lockup; if anything they are fat for their size.

**AND MY OWN CONTROL FAILED, WHICH IS WHY THE SIZE HALF CARRIES NO MAGNITUDE.** C16 put the same
measurement on `Tacombi` and found the whole lockup renders **0.950 × 0.902**. So the deficit is
**not local to `Señor`**, and my first reading — *"`Señor` is 43 mm out of place"* — **is withdrawn
before publication**: the overlay is drawn *after* `flank_compare`'s own integer registration
shift (this run −16, −10 cells), which is the same order as the offsets I measured. Relative to
the global figure `Señor` carries an **extra 12 % in width and 5 % in height**, and that residual
is the part specific to the word.

**TWO CEILINGS, both stated in the probe before any figure:**
* only the `S` and its tilde are separable — the rest of `Señor` is **one connected component**
  with `Tacombi`'s swash. These are not the word's numbers.
* the photograph's `Señor` is tarnished and `flank_compare`'s own header says no threshold rule
  recovers it. That biases the SIZE rows toward **understating** the deficit (a lower bound, the
  safe direction) and biases the FILL row **upward** — so only *"not below 1"* is claimed from it,
  never the 9 %.

**AND ONE CLEAN RESULT FROM THE REGION TABLE.** On `out/r62_side.png`, `Señor` is the **only** one
of nine regions with a real ink deficit (973 against 1261). The other eight run **95.3–105.7 %**
of reference ink. **The whole-lockup ink ratio passing at 0.9766 is averaging over a single
localised deficit** — a gate that passes because eight regions are right.

---

## §6 THE OWNER'S RULINGS THIS REVISION

> *"Bright silver, same as Tacombi."*

Asked with `probe_scratch/rev62_q_senor.png` — the photograph and the render of the same word at
the **same mm/px**, off `flank_compare`'s own registered panels, so he did not have to take my
word for the comparison. Four options were offered, including *"match the photograph exactly"* and
*"fix the size first and re-ask"*.

**WHAT IT OVERRIDES, STATED RATHER THAN BURIED.** SPEC §3 locks the finish as WEATHERED. The
rev-62 brief §4 flagged this collision in advance and required it be **surfaced, not silently
decided**. It was surfaced and he decided. **The override is for this word only** — the b flag,
the i dot and the swash keep their measured tarnish.

**NOTHING MEASURED WAS DELETED.** `TARNISH_K` and `SENOR_MICHELSON` stay, the lift is still solved
on the `Señor` zone so the zones' K is bit-for-bit what it was, and `T1_SENOR_TARNISH=1` restores
the pre-ruling texture **byte for byte** — now a `verify_clone.sh` row, which is what makes the
hash re-base a re-base and not a rubber stamp.

> *"this is just the render to plug into company merch with different backgrounds once i
> determine the model is done"*

**HE WAS ASKED ABOUT THE BOUNCE CARD AND DID NOT AUTHORISE IT.** He answered with what the render
is FOR, which is a bigger fact than the question. **The bounce card is NOT taken** — his "keep
studio" ruling stands and he has now explained its rationale. **F155** records the consequences,
which are not small: the white backdrop is scaffolding, not the deliverable; the model will be
composited on backgrounds nobody has chosen; and the gate is **him** determining the model is
done.

---

## §7 WHAT REV 62 DID NOT DO, SAID PLAINLY

* **The emblem is not fixed.** It still reads as an X — confirmed by looking at
  `out/r62_front_post.png`, his sixth report standing. Rev 62 narrowed the question and killed a
  candidate; it did not close it.
* **`Señor`'s SIZE is not fixed.** The finish is ruled and shipped; the size deficit is measured
  and left, because C16 showed part of it is global and the magnitude is not yet separable.
* **No geometry moved.** The panel items — glass, tyres, the tail's barrel, the shut lines, the
  galley, the counter fascia, F143's roof loudspeakers — are all untouched.
* **The two disputed ceilings (§3 item 4 of the rev-62 brief) were not tested.**
* **`REMAINING_WORK_rev61.md` §I's 27 rows are still untriaged.**
* **No adversary AGENT was run.** This session was instructed not to spawn subagents, so rule 15
  and rule 17 were discharged by their **committed script halves** (`audit_brief.py`,
  `audit_adversary.py`) plus the author's own pass. **That is weaker than an independent agent and
  it is recorded as weaker.** Rev 63 should put a real adversary on this document.

---

## §8 THE GATES, MEASURED THIS REVISION

```
bootstrap.sh          ALL 10 PASS
verify_clone.sh       ALL 272 PASS on a clean tree   <- 0 FIDELITY, 272 SELF-CONSISTENCY
                      (271 at rev 61; +1 is the T1_SENOR_TARNISH companion row)
flank_compare.py      FAILS: worst region `i` 0.684 of its own ceiling
                      ink area ratio 0.9766 PASS, IoU 0.7575 PASS
                      `Senor` 973 px against 1261 -- the ONLY region with a deficit
probe_rev46_vw        9 checked, 2 FAILED -- C6 and C8
                      C8 photograph 3.39 (2.95..3.42 over its window), built 1.49
probe_rev62_landmarks 9 checked, 2 FAIL BY DESIGN -- C11 and C14 ARE the findings
probe_rev62_senor     3 checked, 1 FAILED -- C16, and it stopped an over-claim
senor_trace.py        the `S` rasterises as 1 component, per the rev-61 ruling
```

**AND THE STANDING WARNING, WHICH `verify_clone.sh` PRINTS ITSELF.** A green check is not evidence
about the vehicle. **Not one of those 272 rows compares the model to a photograph.**
