# LEDGER — rev 79

## RULE 55, AT THE TOP, AS THE RULE REQUIRES

**REV 79 SHIPPED NO VEHICLE GEOMETRY, AND THIS TIME THAT IS NOT A CONFESSION —
IT IS THE OWNER'S STANDING RULING.** `revstats.py` prints
**`LAST FIVE REVISIONS (75-79): 16 geometry lines, 3 findings closed`**. The
geometry column reads `0` for the fourth revision running, and at rev 79 the
owner was asked directly whether that was a problem and ruled that it is not:
**FREEZE THE MODEL, DRAW FROM IT (F361)**.

**THE ZERO-CLOSURE RUN IS BROKEN. Rev 79 closed THREE: F354, F360, F363.** The
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

### THREE OF THIS REVISION'S OWN INSTRUMENTS WERE WRONG. NONE WAS FOUND BY REASONING.

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

**AND THE DEFECT I DID NOT FIX, NAMED RATHER THAN ITERATED AT A FOURTH TIME:**
those 1075 px are the counter shelf (`chrome_dull`, identified by SAMPLING THE
PROOF, not guessed) showing through bays 1 and 2. Three attempts failed — by
name, by palette slot, by bbox containment — because the component runs the
length of the flank and no single aperture box contains it. **It is printed on
the sheet. The daylight state is not perfectly the panel van the concept asks
for, and the artefact says so.**

**A8 IS WATCHED FAILING**, which is the only reason it may be quoted:
`T1_APAGA_NOSHUT=1` takes the residual from 1075 px to **18 075 px (3.2217 %)**
and the row REDS. ⚠ **`verify_clone.sh` does not run it (F355's class); it is
watched by hand.**

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
## §5 WHERE THIS REVISION IS WEAKEST

* **NOTHING IN THIS TREE CAN GRADE THE STICKER, and that is still true of the
  new one.** The 13 checks measure self-consistency. **No check compares either
  artefact to a photograph of a printed sticker; none exists.**
* **THE COUNTER SHELF STILL SHOWS THROUGH TWO BAYS** (1075 px). Named, not fixed.
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
