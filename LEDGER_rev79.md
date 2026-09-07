# LEDGER — rev 79

## RULE 55, AT THE TOP, AS THE RULE REQUIRES

**REV 79 SHIPPED NO VEHICLE GEOMETRY, AND THIS TIME THAT IS NOT A CONFESSION —
IT IS THE OWNER'S STANDING RULING.** `revstats.py` prints
**`LAST FIVE REVISIONS (75-79): 16 geometry lines, 4 findings closed`**. The
geometry column reads `0` for the fourth revision running, and at rev 79 the
owner was asked directly whether that was a problem and ruled that it is not:
**FREEZE THE MODEL, DRAW FROM IT (F361)**.

**THE ZERO-CLOSURE RUN IS BROKEN. Rev 79 closed FOUR: F354, F360, F363, F364.** The
run was rev 72 through rev 78, seven revisions, every one `0`.

⚠ **AND THE CLOSURE FIGURE IS ITSELF A REV-79 FINDING. `revstats.py` PRINTED
`3` FOR TWO FINDINGS** because it counted occurrences of the string
`CLOSED-rev79` rather than distinct rows, and this revision had written one row
that graded itself twice. It is fixed (F363), and the `3` above is the fixed
count of three genuinely distinct rows. **The number this ledger leads with is
the number the defect would have inflated.**

---
## §1 WHAT THE OWNER RULED, AND IT IS THE BIGGER OF THE TWO

### F361 — the second half of his rev-78 sentence, answered at last

At rev 78 he said: *"Oh god that looks terrible. I'm worried we're too
committed to the model rather than the combi itself."* The first half became
F346 (draw it, model as underlay). **The second half — whether the PROJECT is
too committed — was recorded as unanswered and stayed that way for a revision.**

Put to him as multiple choice with the measurement attached: revs 76, 77 and 78
each shipped **0** lines of vehicle geometry, and F18 waited **34 revisions**
behind *"build it after the model is done"*. He chose **FREEZE THE MODEL, DRAW
FROM IT** over *"keep building the model"*, over *"stop model work outright"*,
and over *"split it and tell me the cost each revision"*.

⚠⚠ **WHAT IT DOES NOT DO, AND THE OPTION SAID SO ON ITS FACE BEFORE HE PICKED
IT: IT DOES NOT WITHDRAW F191.** *"Keep holding — fix the emblem first"* still
stands. **F318 and the other open geometry rows are DE-RANKED, NOT ANSWERED.**
And it does not retire rule 55 — a revision still owes a visible change or a
plain statement of why not. **This is the second clause rev 77 and rev 78 both
said was owed and neither settled.**

### F362 — he bought a concept, and ordered its open question drawn both ways

4.5 MB of concept material across revs 76–77, and **not one item had ever been
shown to him.** Shown the audit's top-ranked object, he chose **"Build it — and
show me both lamp readings."**

---
## §2 WHAT WAS BUILT — `apaga.py`, and what LOOKING cost it

`design_out/apaga_r79_side.png` / `.svg`, three panels off one `side` capture:
**DÍA** (the shut panel van), **NOCHE lectura A** (the festoon lamps glow),
**NOCHE lectura B** (they stay in daylight ink and visibly do not).

**THE SPINE REPRODUCES EXACTLY.** `grep -c "emit=("` over the four geometry
modules returns **0 / 0 / 1 / 0** — recomputed this revision — the single hit
being `gal_tube`, `emit=(1.000, 0.918, 0.790)` at `GAL_LUM 3.04`. One emissive
material in a 229-object vehicle.

⚠⚠ **AND THE MEASUREMENT THAT CHANGED THE OBJECT, MADE BEFORE ANY INK:
`gal_tube` IS ZERO PIXELS ON BOTH CAPTURES** — 0 of 566 208 art px at az 72,
0 of 561 033 at az 90. The strip sits under the roof header and a waist-height
serving hatch does not show it. **So what is drawn is the room it lights, not
the lamp.** That is a departure from the concept body, declared on the sheet
and in F362. **The concept's published *"FIRST STEP: ~$0, one A4 sheet and an
evening"* is the VINYL EXTINCTION TEST and does not cover this drawing, which
needed a capture that did not exist until this revision.**

### FOUR OF THIS REVISION'S OWN INSTRUMENTS WERE WRONG. NONE WAS FOUND BY REASONING,
### AND THE FOURTH WAS FOUND ONLY BECAUSE AN ADVERSARY WAS DISPATCHED AT MY OWN BRIEF.

1. **THE DAYLIGHT PANEL WAS A FLAT RED SLAB.** One silhouette in one ink. **All
   twelve checks were green on it.** Found by cropping the proof and looking
   (rule 1). Fixed by painting through the material index in the authored
   palette — which is F346's ruling in one sentence.
2. **THE FALL-THROUGH PAINTED THE BODY NEAR-BLACK.** `T1_paint` is unassigned
   by NAME, and the first loop defaulted every unassigned material to the dark
   ink — so the combi's own paint. Fixed by using `classify()`'s MEASURED
   albedo family (rule 10: ask the mesh).
3. ⚠⚠ **THE SHUT-APERTURE RESIDUAL WAS A TAUTOLOGY.** It read
   `(~shut) & fill(galley)`, and `shut` is built FROM `galley`, so it was zero
   **by construction**. It printed `0 px` and could never print anything else.
   **That is rev 78's own S1 defect arriving by a different door, on the
   revision that read rev 78's ledger.** Rebuilt off the bay GLAZING's own
   component boxes — two independently obtained quantities (rule 6) — and it
   now reads **1075 px, 0.1916 % of art**.

4. ⚠⚠ **AND THE RESIDUAL GUARD WAS WRONG A SECOND TIME, WHICH THE FIRST DRAFT
   OF THIS LEDGER PUBLISHED AS A RESULT. F364, RETRACTED HERE (rule 13), FOUND
   BY THE RULE-17 ADVERSARY.** Having escaped the tautology, v2 defined the
   opening from the `glass` material — and **the three serving apertures are
   UNGLAZED** (`STATE.md`: *"open serving apertures on +Y: 3"*), so the window
   overlapped the galley by **ZERO pixels** and was measuring the CAB WINDOWS.
   **The `1075 px of counter shelf in bays 1 and 2` this ledger printed was 759
   `rubber`, 232 `bulb` and 84 `chrome_dull`** — and the `bulb` share is the
   object's OWN INTENDED DRAWING counted as a defect. **A number published off
   a mask nobody painted: rule 8, the defect this project calls its most
   repeated, committed on the revision that quoted the rule.**

**THE FIX, AND WHAT LOOKING FINALLY SHOWED.** v3 takes the opening from the
**BAY SEAL RING** (`rubber` components ≥ 40×40) — independent of the galley and
of `shut`, and it demonstrably covers the bays: three seal components enclose
**11 728 / 10 457 / 9 550** galley px, the fourth being the cab window at **0**.
The mask is now **PAINTED every run** to `probe_scratch/apaga_resid.png`.
Looking at that painting showed two more things no check had: the seal ring
itself was being counted as leakage (2751 px — the frame is not something
showing *through* the frame), and the true leak was the counter shelf at the
foot of bays 1 and 2, **which is what the original prose said and the original
window could not see.** With the seal-ring pass shutting it, **the daylight
panel is now the panel van.**

⚠⚠ **AND A8's GREEN IS STILL NOT EVIDENCE — THE THIRD TAUTOLOGY IN ONE GUARD.**
The seal-ring pass now shuts exactly the set A8 measures, so `n_resid` is 0 on
the normal path BY CONSTRUCTION. **All of its discriminating power is in the
ablation:** `T1_APAGA_NOSHUT=1` reads **52 643 px (9.3832 %)** and REDS. That
is stated in the source, on the artefact's colophon, and in F364.
⚠ **`verify_clone.sh` does not run it (F355's class); it is watched by hand,
and `--out` is mandatory or the ablated sheet overwrites the shipped one.**

⚠ **THE SCALE IS NOT THE CONCEPT'S.** The drawn silhouette measures
**234.06 × 156.86 mm**, not 200 mm. The concept's 200 mm is the BODY
(4.065 m / 20.325); the drawing includes the counter and the OPEN tail board.
**1:23.79 would put the whole silhouette at 200 mm — the owner's call, not the
script's, and it is stated rather than silently rescaled.**

---
## §3 THE THREE CLOSURES

| | |
|---|---|
| **F360** | Rev 78 retracted the *"truncated spec row"* claim in its prose and **not in the module that WRITES it**, so the false sentence survived in **six** tracked files, four machine-written and shipped. Its own §8 said four places were corrected; measured, **two** were. Generator fixed at both sites, the four files re-emitted through the source's own serialisers. **A companion row is WATCHED FAILING on the real defect.** ⚠ **Its own first draft quoted the forbidden phrase in its explanatory comment, so it redded on a clean tree — caught by RUNNING it. The needle is now assembled at run time from two pieces.** |
| **F354** | `probe_rev77_t3floor.py`'s `0 FAILED` was a string literal. `FAILED` now counts **frames that could not be parsed** — explicitly NOT the rung, which F334 deliberately un-gated — and the same edit ends the silent drop beside it. **Watched: `2 checked, 1 FAILED`, the dropped frame NAMED, rc 1.** |
| **F363** | `revstats.py` counted closure STRINGS, not findings. **It printed `3` for two.** Now distinct IDs per revision. ⚠ **It corrects a published historical figure: rev 71 reads `1`, not the `2` the brief and `CLAUDE.md` both print. The 72–78 zero run is UNAFFECTED — zero cannot be inflated — so only the flattering numbers were ever suspect.** |

---
## §4 THE MACHINE AT THE CLOSE

`bootstrap.sh` **ALL 10 PASS** at pickup, row 9 clean. Probes, read by their own
summary lines (rule 9), all as the incoming brief predicts:

```
sticker.py --selftest          6 checked, 0 FAILED
apaga.py --selftest            7 checked, 0 FAILED     NEW
apaga.py --tag side           13 checked, 0 FAILED     NEW
probe_rev73_tailboard          5 checked, 1 FAILED  -- T4 only
probe_rev74_tread              8 checked, 0 FAILED
  T1_TYRE_TREAD=0              8 checked, 2 FAILED  -- T3, T7  (the kill)
probe_rev46_vw                12 checked, 2 FAILED  -- C4, C10
probe_rev69_fitpose            5 checked, 1 FAILED  -- P4 only
probe_rev71_proxy              IoU 1.000000
probe_rev77_t3floor            1 checked, 0 FAILED     (its verdict is real now)
```

⚠ **THE §0 RENDER QUEUE DIED AT THREE FRAMES OF FOUR.** `front`, `side` and
`hero34f` landed; `hero34r` was cut off at sample 9/96 **with no error in the
log** — the process was simply gone. Not diagnosed. **Anything wanting
`out/r79_hero34r.png` has no frame, and `visibility_budget.py` was therefore
not run this revision.** Stated, not skipped.

---
## §4b ⚠⚠ THE OWNER REJECTED THE FIRST NIGHT PANELS. F366.

*"That's not a product."* Three words, on an artefact with **all fourteen checks
green**. He was right, and **this is the second time in two revisions he has
caught a proof that no instrument in this tree could** — rev 78's was *"Oh god
that looks terrible."* **In neither case did a number move.** Rule 2 says a
green check is not evidence about the vehicle. These two say it is not evidence
about the DRAWING either, and that is now a pattern rather than an anecdote.

Four causes, all found by looking (rule 1):
1. **The line pass was computed, discarded and never reused.** The strokes the
   daylight panel drops as "kitchen" are exactly the ones the night panel
   needs. **388 are now knocked out of the glow** — a glow sticker's drawing is
   made by what is PRINTED OVER the substrate, not by colour, so without them
   twenty-odd adjacent objects merge into slabs.
2. **The glow was one flat value.** The AO pass already measured where a single
   strip fails to reach and it was thrown away. Two tiers now, **MEASURED**
   placement at the 45th AO percentile, AUTHORED step.
3. ⚠⚠ **THE STICKER LIT THE CAB.** `glass` was in the glow set, and because the
   serving bays are UNGLAZED that material is **only** the cab door window and
   quarter light. **The two biggest shapes in the picture were the cab glowing,
   in the one drawing whose entire proposition is that the work light is on and
   everything else is dark. The artefact contradicted its own concept.**
4. **Every panel was laid out at CAPTURE size, not artwork size** — each night
   panel a vast black rectangle with the art filling under a fifth of it.

**And two things the sheet did not have at all:** a **DIE LINE** — a die-cut
sticker with no cut path is a picture of a product — and any tie between the
three panels. The cut is now on all three, faint on the dark ones, because the
cut edge is physically there in both states. **It closes to ONE component with
zero thin features left after the bridge.**

---
## §5 WHERE THIS REVISION IS WEAKEST

* **NOTHING IN THIS TREE CAN GRADE THE STICKER, and that is still true of the
  new one.** The 13 checks measure self-consistency. **No check compares either
  artefact to a photograph of a printed sticker; none exists.**
* **A8's GREEN IS ARITHMETIC, NOT EVIDENCE** (F364). Only its ablation discriminates.
* **THE OWNER HAS NOW REJECTED A PROOF IN EACH OF THE LAST TWO REVISIONS**, both
  times on artefacts that passed every check written for them (F346, F366).
  **Nothing in this tree can grade a drawing, and that is not a gap a check can
  close.**
* **FOUR OF MY OWN INSTRUMENTS WERE WRONG**, and the worst was caught by an
  adversary, not by me — after I had already published its number.
* **THE SCALE DISAGREES WITH THE CONCEPT** (234 mm against 200 mm) and only he
  can settle which object he is buying.
* **THE FOURTH FRAME NEVER RENDERED** and the cause is unknown.
* **EVERY AUTHORED CONSTANT IN `apaga.py` WAS CHOSEN BY LOOKING** — the glow
  ink, the night ground, `VOID_FRAC`, `SIMPLIFY_MM`, `LINE_MIN_MM`. They are
  printed on the sheet. A different context would choose differently.
* **F191 STANDS, F318 IS STILL OPEN** for a fifth revision, and F361 de-ranked
  them rather than answering them.
* **THE `nose` CAPTURE'S 200.0° HUE WEDGE IS STILL UNEXPLAINED (F353).**
* **HIS THREE OLDER QUESTIONS ARE STILL UNANSWERED**: the cab door (F352,
  unrecoverable from the record), the earlier cartoon version of the wheels
  (not in this repository), and a photograph of a real Tacombi shopfront.
