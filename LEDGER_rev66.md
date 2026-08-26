# LEDGER — rev 66

**Every figure below was watched printing. Nothing is transcribed.**

---

## §1 THE RESULT

**ALL THREE OF THE EMBLEM'S GATES WERE MIS-REPORTING, AND TWO OF THE THREE TARGETS WERE
UNREACHABLE BY CONSTRUCTION.** Rev 65 found that the *sentence* naming the emblem's defect
was a string literal. Rev 66 found that the *numbers* the project has been aiming at were
wrong as well:

* **C6's target of 7 cells is the photograph's RIM.** The build already matched the
  photograph. It has been red for six revisions against a count the mark cannot make.
* **C4/C5's residual was 96.4 % ONE BROKEN LANDMARK.** Corrected, the shipped constants were
  **2.8× BETTER** than rev 45 (0.2814/0.1001), where C5 was reporting them **1.6× worse**
  (0.4469/0.2814). *(All PRE-rev-66 figures, quoted together so F203 can be checked on its
  own. After F202 and F204 the probe prints 0.0755 against 0.2471 — a factor of 3.3. Two
  different states; do not mix them.)*
* **C8's target was already re-based by rev 65 (F194).**

**AND WITH THE INSTRUMENTS CORRECTED, THE REAL DEFECT WAS SITTING IN THE PROBE ALL ALONG.**
`L6` — stroke width over ring width at the same row — had read **0.1178 against the
photograph's 0.1528** since rev 46 and was never acted on, because it lived inside the
residual that was 96 % one broken landmark. **That is the owner's own sentence, *"the strokes
are thinner than the pressing's"*, as a number.**

---

## §2 THE FOUR FINDINGS, EACH MEASURED

### §2.1 F200 — C6's SEVENTH CELL IS THE RIM, NOT A CELL

`photo_cells()` labels background inside a `frac=0.97` disc that is concentric with the
**41×69 CROP BOX**. The photographed ring is **not** concentric with that box, so at one point
its outer edge falls inside the disc and a crescent of background is counted as a cream cell.

```
   the photograph's 7 cells, each tested against the RING'S OWN FILLED OUTLINE
     n= 97  100.0% inside      n=152  100.0%      n=215  100.0%
     n= 73  100.0% inside      n=115  100.0%      n= 91  100.0%
     n= 68    0.0% inside   mean r 0.932  max r 0.968   <-- THE SEVENTH
```

**Corroborated three ways, none of them an eye:**

1. **The fill test above** — six cells at 100 %, one at 0.0 %. Perfectly bimodal.
2. **The disc sweep** — the photographed RAW count runs **8, 7, 7, 8, 6, 6, 6** over
   `frac` 0.99→0.84 and settles at **6** once the disc clears the rim. The built count is
   **6 at every one**.
3. **Topology** — a V fused to a W is ONE connected figure meeting the band at **SIX** points,
   and a connected figure attached to a disc's boundary at *k* points cuts it into exactly *k*
   regions. Seven needs a seventh contact. **Over 144 builds perturbing all six spine
   constants ±50 % and the weight over 0.12–0.30 the count came out 6 in 143 and 5 in one.
   It was never once 7.**

**The built raster draws its ring out to the canvas edge and so can never produce such a cell
— the two sides were never sharing a ruler (rule 38).** Target re-based **7 → the
photograph's own INTERIOR count**, computed and not typed. **C6 PASSES, 6 = 6.**

### §2.2 F201 — AND CORRECTING C6 KILLED ITS OWN KILL (rule 42, one revision after it was written)

C7 collapsed the W's arms and troughs onto the axis and checked the count moved. Once C6
counts INTERIOR cells that **no longer fires** — a collapsed W still cuts the ring into six —
so C7 read **6 → 6** and went red. **For as long as that stood, C6's new PASS was worth
nothing.** The kill now plants exactly the defect C6 claims to detect: the glyph is shrunk
until its extreme falls **inside** the band and every stroke floats.
**WATCHED FIRING: interior cells collapse 6 → 1**, extreme driven to 0.7392 R against a band
inner edge of 0.8000 R.

### §2.3 F203 — C4/C5's RESIDUAL WAS 96.4 % ONE BROKEN LANDMARK

`landmarks()` takes **L4 = the LAST 3-run row**. When the built raster presents only ONE
3-run row, that is **the same row as L2** — so L4 reported the built V's **APEX** against the
photograph's W **TROUGHS**. Built L2 and L4 both printed **0.3673**, and **L4 printed ABOVE
L3**, which is geometrically impossible for the intended landmark.

```
   rows   L1      L2      L3      L4      residual   L4 == L2 ?
     69   0.1765  0.3676  0.4265  0.3676  0.4423     YES
    276   0.1564  0.3673  0.4145  0.3673  0.4455     YES   <- what the probe used
    552   0.1561  0.3648  0.4102  0.8657  0.1001     no
   1104   0.1561  0.3648  0.4102  0.8657  0.1001     no
   2208   0.1561  0.3648  0.4102  0.8657  0.1001     no    <- converged
```

**A 0.50 swing in L4 driven by a raster parameter that is no property of the glyph.** L4's
−0.4387 error was **96.4 % of the squared residual**. `built_mask`'s docstring has claimed
since rev 46 that *"the agreement across row counts is reported"* — **it never was, and it
does not hold.** Both halves fixed: L4 is DROPPED when it collapses (rule 37, so `err()`
penalises it as the lost landmark it is), and the built side is read at **`BUILT_ROWS = 552`**
with **new control C10** re-checking convergence on every run.

### §2.4 F204 — THE STROKE WEIGHT, BY TWO STATISTICS THAT SHARE NO RULER

```
   L6   stroke width / ring width AT THE SAME ROW -- a horizontal over a horizontal,
        so the viewing angle's cosine cancels; needs no axis ratio, no radial
        registration.  built 0.1178   photo 0.1528   crosses at wfrac 0.2283
   INK  red fraction of the disc strictly inboard of the band, both sides through
        one function.  built 0.432   photo 0.525 +- 0.055   crosses at wfrac 0.2280
```

**THE TWO AGREE TO 0.1 %.** Shipped: `vw_logo_fit`'s `wfrac` **0.1800 → 0.2283**. The
HUBCAP's `CAP_EMBLEM_WFRAC = 0.2087` is untouched — F178's trap.

**CEILING, STATED:** the photographed roundel is 41×69 px and its ring is not concentric with
its own bbox (its annulus never reads 100 % red), so the **INK** side is good to about
**±0.02 in wfrac**. **L6 does not depend on that registration, which is why it is quoted
first.**

---

## §3 WHAT SHIPPED ON THE MODEL

**F202 — THE ARC-CUT TERMINAL**, the route the rev-65 brief called *"the only one left
standing"* and which nobody had written. Each rail is trimmed where it **MEETS the band
circle** and the cap closes along the arc, so **both corners land on the band by construction
and the global extreme cannot move** — which is exactly what kills `T1_VW_CAPMIN`, whose
extreme runs 0.8140 → 0.9250 and drags every other terminal 12 % inboard.

* **Robustness SWEPT, not asserted:** 144 builds perturbing all six constants ±50 % and the
  weight 0.12–0.30 — **0 refusals, and the outline's extreme stayed at the band radius in
  every one.**
* **ON by default. `T1_VW_NOARC=1` restores the perpendicular cap exactly as it stood at rev
  65**, so the two render from one tree (rules 36 and 41).
* **IT DID NOT MOVE THE CELL COUNT (6 either way) — because F200 shows the count was never
  the discriminator.** Stated plainly: the item's stated acceptance in the rev-66 brief
  (*"C6 → 7 cells"*) **was unreachable when it was written**.

**MEASURED ON THE RENDER, WHICH IS THE ARBITER (rule 41), NOT ON THE RASTER:**

```
   ink inside the band     PHOTOGRAPH 0.510    BEFORE 0.418    AFTER 0.502
```

**The deficit closes from 18 % to 1.6 %.** Before/after crop:
`probe_scratch/rev66_emblem_ba.png`; against the photograph:
`probe_scratch/rev66_photo_before_after.png`.

**AND THE 2-D RASTER WAS VALIDATED AGAINST THE RENDER BEFORE IT WAS TRUSTED:** the raster
predicted ink 0.432 where the render reads 0.418, and their radial profiles agree to 0.02 at
every annulus. That is why a pure-2-D prototype was allowed to do the searching while Blender
had the CPU.

---

## §4 WHAT REV 66 GOT WRONG IN ITS OWN WORK — THREE

1. **I READ A GAP IN THE RENDER THAT WAS NOT IN THE GEOMETRY.** Looking at the emblem crop I
   said the stroke tips "visibly stop short of the ring, grey shows between each tip and the
   band". **The mask says they touch: one connected component at every threshold 18–38.**
   What I was reading is the ring's own shadowed inner lip. **The eye was wrong and the mask
   was right** — the same class of error rev 65 recorded, and recorded here for the same
   reason.
2. **AND I DID IT A SECOND TIME, ON THE NOTCH.** I saw a step bitten out of each V tip in the
   AFTER render and suspected the arc cut, then the drape, then subdivision. **Rasterising
   the ACTUAL MESH's front face at 1600 px shows the caps clean and both arms crossing the
   band's inner edge.** The drape log agrees — 0 lattice misses, proud range 6.96–15.10 mm,
   identical before and after. It is shading on a 95-px crop upscaled 7×, not geometry.
   **Both times the instrument beat the eye; both times I checked before publishing.**
3. **MY FIRST TWO NEW VERIFY ROWS WERE WRONG, AND ONE WAS RULE 16.** `ck "F198's literal is
   gone" 0 "$(grep -c '0.6638' ...)"` fails on the COMMENTARY that records what F198 was —
   which is the record, not the defect. Re-aimed at the message's own giveaway phrase. The
   second row grepped `OPEN_FINDINGS.md` for the same figure and would have pressured me to
   delete register text. **Dropped rather than satisfied.**

**AND ONE THING I DID NOT GET TO CHECK THE HARD WAY:** C11's first kill planted a gap in the
BAND, which `binary_fill_holes` correctly calls interior — so the kill did not reproduce the
photograph's artefact and C11 went red. Re-planted as a breach of the ring's **OUTER** edge.
**The guard failed me before I could ship it wrong (rule 44 working in my favour).**

---

## §5 NOTHING WAS PUT TO THE OWNER THIS REVISION, AND WHY

Every open question this revision raised was answerable from what is on the repo — which is
his own rev-54 ruling working as intended. **The one thing worth his eye is the before/after
crop**, and it is sent with this revision rather than held for the next.

**HIS TWO STANDING SENTENCES ARE BOTH STILL LIVE:** the emblem (worked, measured, improved,
**not finished** — C4 is still red) and **the nose's shape (F197), which is UNTOUCHED.**

---

## §6 THE MACHINE'S VERDICT AT CLOSE — every one watched print

```
bootstrap.sh              ALL 10 PASS
verify_clone.sh           320 PASSED  (1 row RE-BASED with its cause, 17 companion rows added)
probe_rev46_vw.py         12 checked, 1 FAILED -- C4 only, at 0.0755 against a bar of 0.045
                          <- WAS 9 checked, 3 FAILED (C4, C5, C6)
build.py T1_VERIFY=1      VERIFY: 0 fail, 0 warn at SUB=1
audit.py  T1_SUB=2        VERIFY: 0 fail, 0 warn -- STATE.md regenerated
probe_rev64_shear.py      6 checked, 0 FAILED
probe_rev65_unproject.py  10 checked, 0 FAILED
probe_rev63_trace.py      ALL CONTROLS PASS
probe_rev63_reach.py      ALL CONTROLS PASS
vw_pressing.py            5 checked, 0 FAILED
trace_outline.py          SELFTEST PASS ;  svgraster.py  SELFTEST PASS
probe_rev59_nose.py       5 checked, 0 FAILED -- AND IT STILL DOES NOT MEASURE THE NOSE'S
                          SECTION, which is what he asked about (F197 stands)
probe_rev59_door.py       8 checked, 1 FAILED (M3, BY DESIGN)
flank_compare.py          FAILS  -- unchanged
gloss_compare.py          FAILS at 0.441 of the photograph's spread (bar 0.60) -- unchanged
```

**AND THE STANDING WARNING. Not one of those verify rows compares the model to a photograph.**
The rows that do are `flank_compare`, `gloss_compare` and `probe_rev46_vw`, and **two of the
three still fail.**

---

## §7 WHAT REV 66 DID **NOT** DO

1. **C4 IS STILL RED — 0.0755 against a bar of 0.045.** The six spine constants were NOT
   re-solved. With L4 working the solver can see the trough landmark for the first time, and
   `T1_VW_SOLVE=1` is sitting there. **It was not run, because rule 41 says the render is the
   arbiter and a re-solve needs a render to judge it.** Remaining errors: L1 −0.0307,
   L3 −0.0239, L4 +0.0634.
2. **THE NOSE (F197) IS UNTOUCHED AND STILL UNINSTRUMENTED.** It is one of the owner's two
   sentences and it did not move. `probe_rev59_nose.py` still measures the lamp break's
   ELEVATION, not the nose's SECTION.
3. **THE VISIBLE GAP AT THE STROKE TIPS IS NOT CLOSED.** The glyph's extreme is fitted 20 %
   into the band (`1.0 − 0.8 × _BAND_FRAC`); the photograph shows the ends merging into the
   band with no gap at all. **Fitting deeper is a one-constant change that nobody has
   measured** — and rev 44 warns that fitting to the OUTER radius buries the arms, so the
   answer is somewhere between and is a MEASUREMENT, not a guess.
4. F156 — six revisions unacted. `REMAINING_WORK_rev61.md` §I — 27 rows, six revisions.
5. `probe_rev63_shapefit.py` still reads the HUBCAP's weight where the nose ships its own
   (F178's trap, brief §3 item 6) — **and F204 has now moved the nose's weight, so that probe
   is further out of date than it was.**
6. Tyres, glass, the tail's barrel, the shut lines, the galley, F143's roof loudspeakers: all
   untouched.

---

## §8 THE BRANCH, MEASURED AT PICKUP AND AT CLOSE

```
AT PICKUP   clone SHALLOW -- the NINTH revision running.  git fetch --unshallow.
            fetch --prune printed  - [deleted]  origin/claude/next-context-prompt-rev66-0rd3kg
            -- THE DESIGNATED BRANCH, before anything had been pushed to it, THE NINTH.
            HEAD 0 ahead / 0 behind origin/main.  bootstrap row 9 GREEN.
            git diff --name-only HEAD...origin/main -> EMPTY (no new photographs).
            origin/claude/bus-model-rev57-yvrlhi now reads 0 ahead, as the rev-66 brief
            predicted it would once rev 64 reached main.
AT CLOSE    measured after the push, with `git fetch --all --prune` first:
              shallow: false
              origin/claude/next-context-prompt-rev66-0rd3kg   ahead 3 / behind 0
              HEAD                                             3 ahead / 0 behind origin/main
              NO OTHER remote branch is ahead of origin/main at all.
              bootstrap.sh row 9 GREEN -- "no branch carries work HEAD does not have".
              bootstrap.sh ALL 10 PASS ;  verify_clone.sh ALL 322 PASS, clean tree.
            (The pickup figure is NOT the close figure, and an adversary once caught a
             brief shipping only the pickup one.  This citation was ALSO wrong on its
             first writing -- it pointed at the rev-67 brief's SS8, which is the
             REGISTER section, not the branch.  Rule 18: cite strings, not section
             numbers you have not re-opened.)
```

**THE ONE THING TO CARRY IF ONLY ONE THING IS CARRIED.** *A target is an instrument.* Rev 65
proved the sentence naming this defect was never measured; rev 66 found that **two of the
three numbers it was measured against could not be reached by any glyph.** Before you fit
anything to a gate, **ask what the gate's TARGET is made of, and whether the thing you are
building could ever produce it.**
