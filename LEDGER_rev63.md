# LEDGER — rev 63

**Machine-checkable claims only. Every figure below was watched print. Where a
figure is quoted from another document rather than re-measured here, it says so.**

The revision's one subject was **the owner's top item: the nose emblem**, reported
wrong SIX times across eighteen revisions. It ends with the emblem **reading as a V
over a W on the nose** — and with the gate that has steered the item **refuted as
sufficient**, which matters more.

---

## §1 THE HEADLINE, IN ONE LINE EACH

1. **THE CANONICAL MARK WAS OBTAINED.** `EMBLEM_HANDOFF.md` §5 item 1 — *"go and get
   the specification"* — executed for the first time. `vw_canonical_2019.svg` is on the
   repo with its provenance welded into the file. **F167.**
2. **AND IT DISQUALIFIED ITSELF.** At the photograph's own 41 × 69 raster: canonical
   **3 cells / elongation 1.597 / ink 0.426** against the photographed badge's
   **7 / 3.390 / 0.606**. The 2019 redraw's V does not touch its W and its legs stop
   short of the ring; the pressing has both. **F168.**
3. **THE CONSTRUCTION WAS NEVER THE CEILING.** 24 000-point ablation over seven spine
   constants **and** the stroke width: `vw_bars` reaches **elongation 6.877 at 7 cells**,
   twice the photograph's 3.390. Eighteen revisions of "it reads as an X" was a SEARCH
   problem, not a geometry problem. **F174.**
4. **C6 AND C8 CAN BOTH GO GREEN ON A GLYPH THAT IS WORSE, AND THE COUNTEREXAMPLE WAS
   BUILT AND RENDERED.** 7 cells, elongation 3.322, IoU 0.5363 — every gate green — and
   on the nose a Y-shaped trident worse than the X. Reverted. **F175. This is the most
   important row in this ledger.**
5. **C7 — C6's OWN KILL — GOES DEAD THERE**, so C6's simultaneous pass is worthless.
   The gate contains the alarm for its own failure and nobody had driven it into the
   region where it fires. **F176.**
6. **THE EMBLEM SHIPPED, AND IT READS AS A VW.** The canonical spine plus a nose stroke
   weight set where the glyph's ink fraction matches the photograph's **0.606 exactly**.
   `probe_scratch/rev63_emblem_ba2.png` is BEFORE | AFTER on the nose.
7. **SIXTEEN NEW FINDINGS, F167–F182**, of which **five are refutations** — two of this
   revision's own proposals.

---

## §2 WHAT SHIPPED, AND WHAT IT COST

**IN `t1_core.py`** — six spine constants, re-based together:

```
                 was        now      provenance
VW_V_TIP_X       0.3806     0.3287   fitted to vw_canonical_2019.svg, IoU 0.7979,
VW_APEX_Z        0.1250     0.0538   converged, NO parameter on a bound (C27b was
VW_W_ARM_X       0.9200     1.1002   watched FAILING first, on the run before)
VW_W_ARM_Z       0.0019     0.4350
VW_W_TROUGH_X    0.4925     0.3111
VW_W_TROUGH_Z   -0.6200    -0.6445
VW_W_PEAK_Z     -0.075     -0.075    UNCHANGED
```

**IN `t1_detail.py`** — the **NOSE's** stroke weight, `vw_logo_fit()`'s signature
default, **0.1986 → 0.1800**: swept, and 0.1800 is where the built glyph's ink fraction
inside the disc reads **0.606**, the photograph's own. **`CAP_EMBLEM_WFRAC` is the
HUBCAP's weight and is UNTOUCHED at 0.2087** — see F178.

**WHAT IT COSTS, MEASURED, NOT SOFTENED:**

```
                       cells   elongation   landmark residual   C7 (C6's kill)
    before (rev 46)      6        1.485          0.0347            ALIVE
    AFTER (rev 63)       6        2.388          0.4469            ALIVE
    THE PHOTOGRAPH       7        3.390            --
```

* **C6 is still one cell short** — 6 against 7.
* **C8 passes at 2.39 against 3.39** — "1.42× too round". It passes because its bar is
  0.70 × the photograph; it is not a claim of parity.
* **C4/C5 go RED.** The landmark set no longer describes this topology.
  `EMBLEM_HANDOFF.md` §6 predicted exactly this and says to **re-read** them, not assume
  them. Done: they are red because L4 reads 0.3673 against 0.8060, i.e. the landmark is
  looking for a feature this spine does not present.
* **C7 is ALIVE (6 → 5)**, which F176 makes a precondition for reading C6 at all.

**SIX `verify_clone.sh` ROWS RE-BASED TOGETHER**, cause named in the script, plus
**SEVEN companion rows**: both stroke weights now checked BY VALUE so F178's trap cannot
be re-entered silently; the canonical mark's presence and its deliberate non-`ref_` name
asserted; and the probes behind F174's ablation and F175's counterexample asserted
present so the next context can re-run them rather than take this document's word.

---

## §3 THE INSTRUMENTS BUILT, AND THE FOUR OF THEM THAT WERE WRONG

| file | what it is |
|---|---|
| `svgraster.py` | nonzero-winding scanline SVG filler. 9 selftest shapes with known answers incl. an annulus + a kill. An unsupported path command **RAISES** (rule 37) |
| `trace_outline.py` | Moore-neighbour contour tracer, Chaikin smoothing, Douglas-Peucker. 10 selftest shapes incl. a ring whose annulus area is known by construction |
| `probe_rev63_canon.py` | the canonical mark measured through the SHIPPED statistics (lifted by `ast`), window-swept; `--fit` runs the canonical fit and VERIFIES it on the photograph |
| `probe_rev63_ablate.py` | the 24 000-point ablation of `vw_bars` itself (F174) |
| `probe_rev63_shapefit.py` | builds F175's counterexample — kept so the refutation is reproducible |
| `probe_rev63_reach.py` | contacts with the ring band, and their ANGLES (F179–F181) |
| `probe_rev63_angles.py` | the six contact angles read off both photographs — **NOT FINISHED, see §7** |
| `probe_rev63_final.py` | the search with every rev-63 term at once — produced only fans, see §7 |
| `probe_rev63_trace.py` | traces the real pressing's outline — **FAILS ITS OWN T3, see §7** |

**FOUR OF THIS REVISION'S OWN INSTRUMENTS WERE WRONG AND EVERY ONE PRINTED A PLAUSIBLE
NUMBER FIRST** (F172, F182):

1. `svgraster`'s C/S control asserted a triangle area an `S` cannot produce at a corner —
   read **0.5828 for 0.5**, and the **control** was the defect.
2. `probe_rev63_canon`'s C24 claimed *"AT AN IDENTICAL RASTER"* while printing a 276-row
   figure against the photograph's 41 × 69. Rule 38.
3. `probe_rev63_reach`'s first mask counted **arcs of the ring band's own edge** between
   cream cells — **10 contacts where the mark has 6, and 41 at 552 rows**. Caught by its
   three-raster row and confirmed by painting it. **Sixth time this project has recorded
   the mask-selects-the-wrong-pixels defect.**
4. the same probe's first KILL demanded the contact count DROP when the W's arms collapse
   onto the axis. It went **4 → 5**, and the CONTROL was the defect: `_on_band` projects
   every terminal onto the band circle by construction, so moving a spine point inboard
   changes its ANGLE, not its reach.

---

## §4 THE REFUTATIONS — FIVE, TWO OF THEM OF THIS REVISION'S OWN PROPOSALS

| # | claim | verdict |
|---|---|---|
| **F168** | the canonical 2019 vector can serve as the emblem's target | **REFUTED.** 3 cells / 1.597 against 7 / 3.390 at one ruler |
| **F170** | *(rev 63's own)* rank glyphs by IoU/elongation/cells | **AMENDED IN THE SAME REVISION** by F175 — the ranking does not track appearance |
| **F174** | *(F137's)* no spine arrangement can satisfy the photograph's cell shape | **REFUTED.** The construction reaches 6.877 at 7 cells |
| **F179** | *(rev 63's own, §5c.1 candidate 1)* a REACH term is the missing discriminator | **REFUTED.** The trident touches the ring in all SIX places |
| **F178** | `T1_VW_WFRAC` / `CAP_EMBLEM_WFRAC` are the same weight | **REFUTED.** Two constants, two objects; the env var drives the NOSE only |

---

## §5 WHAT SEPARATES A GOOD GLYPH FROM A BAD ONE — THE ONE POSITIVE RESULT (F181)

Position is the axis **C6, C8, IoU and reach are all blind to**. Contact angles at 276
rows:

```
    SHIPPED (rev 46)    4 contacts   62 118 212 328              tightest 55 deg
    rev 62 photo-fit    7 contacts   19 70 110 161 223 270 318   tightest 40 deg
    F175's TRIDENT      6 contacts   17 60 119 163 263 277       tightest 15 deg
```

The trident's two W legs converge to **15°** apart — *that convergence is the spike that
makes it read as a Y*. **A tightest-gap floor would have rejected it where every other
statistic passed it.**

**And the same instrument corroborates F63/F64 from a second independent ruler (F180):**
the rev-46 glyph touched its ring in only **four** places, with nothing near 0° or 180° —
the W's two floating outer arms, exactly where `vw_bars`' own rev-60 comment says they are.

---

## §6 THE MACHINE'S VERDICT AT CLOSE — every one watched print

```
bootstrap.sh            ALL 10 PASS
verify_clone.sh         ALL 285 PASS on a clean tree  <- 0 FIDELITY, 285 SELF-CONSISTENCY
audit.py                VERIFY: 0 fail, 0 warn at T1_SUB=2; STATE.md REGENERATED
probe_rev46_vw.py       9 checked, 3 FAILED -- C4, C5, C6.  C7 and C8 now PASS
probe_rev63_canon.py    5 checked, 0 FAILED ; --fit 11 checked, 0 FAILED
probe_rev63_ablate.py   ceiling 6.877 at 7 cells  (the construction is not the limit)
probe_rev63_reach.py    6 checked, 0 FAILED
probe_rev63_trace.py    T3 FAILS at IoU 0.6504 -- NOT FINISHED, see §7
audit_brief.py          10 checked, 0 FAILED
audit_adversary.py      36 asked, 0 BROKE
```

**AND THE STANDING WARNING `verify_clone.sh` PRINTS ITSELF:** not one of those 285 rows
compares the model to a photograph. **A green check is not evidence about the vehicle.**

---

## §7 WHAT REV 63 DID **NOT** DO — READ THIS BEFORE PLANNING REV 64

**This section is shorter than what it did, and it is the more useful one.**

1. **THE EMBLEM IS NOT RIGHT.** It reads as a VW, which it did not before. Held next to
   the two photographs (`probe_scratch/rev63_vs_real.png`) **four things are still
   visibly wrong and none is measured to a target**: the glyph does not fill its ring the
   way both photographs do; the V is too narrow; the W's outer arms are too short; the
   strokes are thinner than the pressing's.
2. **`probe_rev63_trace.py` FAILS ITS OWN T3 AND THE TRACED GLYPH IS NOT IN THE MESH.**
   This is the method most likely to close the item — trace the real pressing instead of
   approximating it with seven constants — and it is **half built**. Diagnosis is done
   and is in the probe: the disagreement is **the RING (IoU 0.508), not the glyph
   (interior IoU 0.78)**. It needs hole-aware outlines fed to `t1_core`'s existing
   outline-to-mesh builder. **Nothing about it is wired into `build.py`.**
3. **`probe_rev63_angles.py` DOES NOT YET PRODUCE A TARGET.** F181's contact-angle
   statistic separates candidates from each other but has **no photographed target**,
   because the badge's ring is not fitted on the frame. Its stroke counts are **unstable
   across sampling radii (5, 5, 7, 9, 6)** — that is a windowing defect, stated, not hidden.
4. **THE HUBCAPS WERE NEVER LOOKED AT.** The spine is shared by five objects (F69). The
   front view does not show them and **no side/hero render was inspected after the change.**
5. **NO DELIVERY RENDER.** The owner's rev-58 gate stands. He was asked for a print size
   and has not answered.
6. **NO INDEPENDENT ADVERSARY AGENT** ran on the incoming brief. Rules 15/17 were
   discharged by `audit_brief.py`, `audit_adversary.py` and the author's own pass — the
   **mechanical half only**, same gap rev 62 declared.
7. **`REMAINING_WORK_rev61.md` §I IS STILL UNTRIAGED** — 27 rows, now **three revisions**
   running. `PANEL_rev61.md` untouched.
8. **NOTHING outside the emblem was touched.** Glass, tyres, the tail's barrel, the shut
   lines, the galley, F143's roof loudspeakers, the F10–F14 cluster: all untouched.
9. **F156 was not re-based or annotated** — three revisions now.
10. **The two disputed ceilings** (specular-event census, ground shadow) were not tested.

---

## §8 THE ONE THING TO CARRY IF ONLY ONE THING IS CARRIED

> **A GATE PASSING IS NOT EVIDENCE THE THING IS RIGHT. REV 63 BUILT THE COUNTEREXAMPLE:
> C6, C8 and IoU all green, and the emblem rendered as a Y. The render is the arbiter.
> And check a control's KILL before you read its PASS — C7 was dead there.**
