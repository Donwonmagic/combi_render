# LEDGER — rev 77

## ⚠ RULE 55, AT THE TOP, WHERE IT BELONGS

**REV 77 SHIPPED NO VEHICLE GEOMETRY, AND SAYS SO HERE RATHER THAN IN A FOOTNOTE.**
`revstats.py` is the instrument; run it, do not read this sentence for the figure.

**What it did ship is TWO FINISHED ARTEFACTS THE OWNER CAN LOOK AT, and the capability
underneath them:**

| shipped | what it is |
|---|---|
| `design_out/sheet3_not_issued.svg` / `.png` | **SHEET 3 OF 4 — OFF SIDE ELEVATION (−Y) — NOT ISSUED.** A2, 1:10, one ink. Its subject is the one elevation `SPEC.md` grades **E**. |
| `design_out/loteria_la_rueda.svg` / `.png` | **CARD ZERO of EL COMBI · LA LOTERÍA — `LA RUEDA`.** 90 × 140 mm, one ink, drawn through the line pass. |
| `line_pass.py` | **THE LINE PASS. It did not exist before this revision.** Grease Pencil Line Art → polylines → SVG. |
| `sheet.py` | The drafting primitive layer both artefacts are drawn with: ONE primitive list, TWO backends (SVG master, PNG proof), so they cannot drift. |

**THE HONEST READING OF RULE 55.** Its letter is *"a visible change to the vehicle"*, and the
vehicle did not move. Its purpose is *"the owner cannot see a revision that only measures"*, and
that purpose is met twice over. **The redirect at rev 76 makes the letter and the purpose come
apart, and this is the first revision where that happens — so it is stated, not quietly
reinterpreted.** A future context should decide whether rule 55 needs a second clause for the
design programme, and should not assume this ledger settled it.

---

## §1 THE OWNER RULED TWICE, AND ONE OF THEM UNBLOCKS THE OLDEST THING IN THE REGISTER

Both were put as multiple choice with the reference material attached, using the question tool, as
`CLAUDE.md` requires. Both are recorded in `OPEN_FINDINGS.md`, which outranks this file.

**F330 — F18's TRIGGER IS FIRED.** *"Is the model done enough to start the sticker, or not yet?"* →
***"Yes — start it now."*** The die-cut sticker has been the register's oldest live row since
rev 44, it is the project's original deliverable, and the rev-76 completeness critic named this as
the single question that unblocks the most (its finding 12). **It is now a live build item.**

⚠ **ITS CEILING, RECORDED WITH IT: he was asked whether the MODEL is done enough, not whether the
EMBLEM is.** He did not withdraw F191 and was not asked to. The asker's reasoning — that a die-cut
sticker at 60–80 mm cannot resolve the roundel — was offered in the option text and is NOT a ruling
he made.

**F331 — THE AUDIENCE IS SPLIT DELIBERATELY.** *"Kids get one line, adults another."* The
deadpan-catalogue register is **CONFIRMED for the adult half and is no longer a drift to be
corrected** — but it is now HALF the programme and a children's line of equal standing is owed.
**Every future shortlist must say which line each item is in.**

⚠ **WHAT F331 DOES NOT SETTLE: the critic's finding 4 — NO FOOD, NO PEOPLE, in a programme for a
taqueria — is untouched and stays open.** The option that carried it was not chosen, but he was
choosing an AUDIENCE; do not read a refusal into an unchosen option.

---

## §2 SESSION A — `SHEET 3 OF 4 : NOT ISSUED`

**EVERY FIGURE ON THE SHEET IS READ OUT OF `STATE.md` AND `SPEC.md` AT DRAW TIME — 40 of them.**
Nothing is typed into the drawing. When the model moves, the sheet moves.

**WATCHED REFUSING (rule 3), before any file was written:** a regex that could not find the
mid-wheelbase belt station printed `39 checked, 1 FAILED -- nothing was drawn (rule 37)`.

**WHAT IS DRAWN IS ONLY WHAT TRANSFERS.** Measured off the mesh AND symmetric about the centre
plane — ground, hub stations, tyre circles, arch lips, the three roof stations, the three belt
stations, the rocker. **There is no body outline, because none exists in anything we hold**, and
the sheet's own key says so: *"ABSENT — no outline of this flank exists in anything we hold.
Drawing a plausible one is the defect this project has paid for most often."*

**IT PRINTS ITS OWN DISAGREEMENTS.** Three different overall lengths under three different
exclusions, and the dimensions table's `+525.0 mm` still OUT.

**TWO DEFECTS IN `sheet.py` WERE WATCHED AND FIXED**, both in the rotated-text path: the first cut
silently dropped the rotated label entirely, and the SVG and PNG backends disagreed by 180° on the
sign of the rotation (SVG rotates clockwise on screen, PIL rotates the image counter-clockwise).

---

## §3 SESSION B — THE LINE PASS, AND CARD ZERO

**THE KEYSTONE EXISTS.** `DESIGN_PROGRAM_rev76.md` §5 item 1 called it *"the keystone and it does
not exist"*. It exists. It delivers the first half of the owner's own recovered style ruling —
*"vector line and flat colour, shading and occlusion sampled from the 3D asset"*.

⚠ **THE SECOND HALF IS NOT BUILT. There is still no normal pass and no AO pass.** The line
programme is half built and the built half is the line. Do not let a later document round this up.

**FOUR DEFECTS MEASURED IN THE NEW INSTRUMENT — see F332. The one that matters:**

```
    source_type = SCENE       strokes span x -2.420 .. +2.160   19471 points
    source_type = COLLECTION  strokes span x -2.420 .. +2.128    5933 points   <- 7 wheel objects
    source_type = OBJECT      strokes span x +0.968 .. +1.632    1331 points
```

**`COLLECTION` IS A SILENT NO-OP: FEWER POINTS OVER AN UNFILTERED WINDOW.** The tyre is 0.665 m and
the window it actually drew is 4.55 m. **AND THE COUNT LOOKED RIGHT** — 2845 strokes for the whole
scene falling to 718 for "the wheel" is exactly what a working filter would print. **It was caught
by DRAWING the 718 strokes and looking at them: they render a complete bus, roof, windows, both
arches.** Rule 1 and rule 8, on the revision's own new instrument, on its first day.

**CARD ZERO — `LA RUEDA`.** The badge is TRACED, point for point off the line pass. The rings are
**MEASURED, NOT TRACED**: they are creases on a surface nearly tangent to the view, occlusion
flickers along them, and no chaining setting repairs it (`0.001 / 0.01 / 0.05` → `461 / 337 / 182`
strokes, longest run `88 / 102 / 156` points). So every stroke point's radius about the axle is
histogrammed and the peaks are drawn as true circles — **which converts a broken trace into a
measurement**, the only move available.

**CHECKED AGAINST FOUR INDEPENDENTLY OBTAINED QUANTITIES (rule 6)**, parsed from source at draw
time and never derived from the line pass:

```
    tyre     line pass 664.1 mm   source 664.9 mm   -0.8 mm
    hubcap   line pass 273.8 mm   source 274.0 mm   -0.2 mm
    badge    line pass  87.4 mm   source  86.9 mm   +0.5 mm
    rim OD   line pass 440.2 mm   source 439.6 mm   +0.6 mm
```

**WATCHED REFUSING:** fed the contour-ablated pass, all four go OUT at −250.2 / +89.9 / −16.1 /
−24.9 mm, `14 checked, 4 FAILED`, and nothing is drawn.

⚠ **AND ONE OBSERVATION THAT BEARS ON F191, RECORDED AT ITS TRUE STRENGTH AND NO MORE: THE VW BADGE
TRACES CLEANLY AND IS LEGIBLE IN LINE.** It is a raised plate seen square-on, so its contour is a
true silhouette. **The mark the owner has reported wrong NINE times in photoreal renders is not
wrong in line.** That is an observation about ONE object at ONE scale in ONE view. **It is not a
claim that the emblem is fixed. F191 and F234 both stand.**

---

## §4 WHAT I GOT WRONG IN THIS REVISION

*(This section is mandatory here and is written before the closing audits, not after.)*

1. **I wrote a wheel-object filter that split names on `"."`** — `tyre1.31` → `tyre1`, `cap1.31` →
   `cap1` — so it matched **2 of 11 objects** and would have drawn a rim with no tyre and no
   hubcap. Caught by PRINTING the window (rule 8) and reading it.
2. **I baked 250 identical frames.** `lineart_bake_strokes()` covers the whole scene frame range;
   the first spike wrote **5,060,569 points in 220 s** to obtain the 20,234 it needed. The same
   bake now takes **2.3 s**.
3. **I converted camera-normalised coordinates to metres wrongly, by the frame aspect.**
   `ortho_scale` spans the LONG axis only. The first cut read the tyre at **966 mm against its
   measured 664.9**. Caught by the card's own source cross-check REFUSING — which is what a rule-6
   check is for, and the first time in this revision that a guard caught me rather than the reverse.
4. **I published `1:10` in `sheet3_notissued.py`'s summary line as a string literal** while the
   script drew at a different scale, in a project whose first rule is that a figure in a paragraph
   goes stale silently. It is derived now.
5. **I let three text blocks collide** on two different artefacts and only found them by rendering
   and looking — twice on the sheet, twice on the card. Rule 1 earned its keep four times in one
   session on layout alone.

---

## §5 WHAT THE RULE-15 ADVERSARY FOUND IN THE INCOMING BRIEF — 20 DEFECTS, 5 TOP

**AND ONE OF THEM WAS IN AN ARTEFACT I HAD ALREADY SHIPPED.** `sheet3_notissued.py`'s title block
printed `1 -- (72,46,6) ON (206,208,200), BOTH MEASURED`. `lid_gen.py` says
`INK = (72, 46, 6)  # strip lettering; measured median (91,59,7) is blur-limited, so the core is set
darker`. **The ink is an AUTHORED darkening of a measured median, on a sheet whose entire subject is
evidence grading.** Fixed in the same revision (rule 13); both figures are now parsed and both printed.
**The stock's provenance was checked and does hold** — `t1_mats.py` carries `# measured (206,208,200) sRGB`.

**AND THE SAME PASS MADE THE SHEET BETTER, because the repository already held stronger material than
the sheet was using.** `SPEC.md` says the two off-side features **CONTRADICT each other** — the windows
mirror the show flank because `side_cutters` loops `s in (1,-1)` while the cargo door was placed
independently — and that, shown the sightlines with every box printed, **the owner answered *"cannot
tell from this crop"***. His own reading of that elevation is now the largest sentence in the sheet's
empty field. The grade wording was wrong too: **E is *"Expert inference — not observed"*; *"(never
photographed)"* is that row's annotation, not the grade's definition.**

**THE OTHER TOP FOUR, ALL VERIFIED INDEPENDENTLY BEFORE BEING RECORDED:**

1. **`DESIGN_PROGRAM_rev76.md` §0 retracts `109.5 | 129.5` and its §3 still prints it, word for word,
   in the *"measured figures in solid ink"* class, 122 lines later.** F322's class.
2. **`AUDIT_rev43.md` already refutes the pillar thesis harder than the retraction does** — *"the
   photograph's are equal, and the model's asymmetry has the wrong sign"*, with the cause named — and
   `grep -c "109.5" OPEN_FINDINGS.md` is **0**. It has never been in a register. **F336.**
3. **The retraction's own sigma is wrong.** Asymmetry is `2c₁ − c₀ − c₂`, so σ = 0.015·√6 = **36.7 mm
   → 0.54 σ**, not the published 0.67. Conclusion strengthens; the figure was wrong in the direction
   that overstates the effect.
4. **The 78-concept bench's bodies are gone (F335)** — the program declared itself their only home and
   pointed at an agent scratch path that was never tracked and no longer exists on this disk.
5. **The evidence for the keystone claim was void.** `grep -rln "freestyle|gpencil|use_pass_|cryptomatte"
   --include=*.py .` is a BASIC-regex grep, so the pipes are literal; it would have printed *"finds
   nothing"* on a tree full of gpencil. **The claim was true; the evidence was not.** Rule 50.

**AND WHAT IT CONFIRMED, which is worth as much:** the spine quote is **real and verbatim** in
`NEXT_CONTEXT_PROMPT_rev39.md` §7 and absent from every carrier since — the single most important
sentence in the programme survives; `post.py` really does destroy alpha; `deliver.py` really does
write its whole package before it refuses; there really is no 3D export path; the ortho arithmetic is
right and `side` really does fit.

---

## §6 WHAT THE RULE-17 ADVERSARY FOUND IN THE BRIEF I WROTE — 15 DEFECTS, 4 TOP

**AND THREE OF THEM WERE WRONG CLAIMS OF MINE THAT CHANGE A CONCLUSION. All re-derived independently
before being accepted — an adversary is not taken at face value either.**

1. ***"the row is strictly HARDER to pass"* IS FALSE, AND IT IS THE SENTENCE THAT LICENSED THE T3
   RE-BASE UNDER RULE 44.** Run over rev 77's own five ladders: **OLD passes 2 of 5, NEW passes 5 of
   5. Three flip FAIL→PASS and none flips back.** The conditions are **INCOMPARABLE, not ordered** —
   `(−7→−9.00, +3→+2.50, +5→+4.00, +7→+6.00, +10→+9.00)` fails OLD and passes NEW; `(−7→−6.00,
   +3→+4.40, …)` passes OLD and fails NEW. **On this tree the change is a NET LOOSENING.** The
   re-base stands on the measurement — the ungated rung IS below its own noise — but not on that
   word. **Retracted in the probe, the verifier, the register and the brief.**
2. **THE `1.8 σ` GAIN FIGURE WAS WRONG THREE WAYS AND I HAD WITHDRAWN A LIVE FINDING ON IT.**
   Arithmetically it is **1.727**, not 1.8. **And it is the wrong statistic**: the departure of a
   MEAN from 1.000 is scaled by the SEM, `0.033506/√5 = 0.01498`, giving **3.86 σ**. **And it was
   contaminated by the very rung this revision declared unusable** — excluding −7.0 the gains read
   mean **0.8955**, departure **0.1045**, **3.13 σ on the sd and 7.00 on the SEM.** **So the
   sub-unity gain IS established on this tree and my "do not quote it" was an unjustified
   withdrawal. Restored.**
3. **THE F324 RETRACTION NEVER REACHED `OPEN_FINDINGS.md` OR `verify_clone.sh` — WHICH IS REV 75's
   OWN TOP DEFECT, REPEATED TWO REVISIONS LATER.** F324's row still published *"TWO DISJOINT
   CLUSTERS"* and *"a TREE- OR BUILD-DEPENDENCE"* at `MEASURED-rev75` with no rev-77 annotation, and
   `verify_clone.sh` — the file I was editing — still carried *"SO THIS ROW IS A COIN FLIP"* twenty-five
   lines above my own new companion block. **`HANDOFF_CARRIERS.md` §11 records rev 75 writing "my own
   corrections had reached the prose carriers and stopped short of `OPEN_FINDINGS.md`". Same defect,
   same two file classes.** Both corrected.
4. **§4 SAID FIVE ROWS SKIP; THE GUARD I RE-BASED IN THE SAME REVISION DEMANDS SIX.** Carried forward
   from rev 76 without re-deriving it, contradicting my own new row.

**AND FOUR TRANSCRIPTION DEFECTS, WHICH IS THE CLASS RULE 17 EXISTS FOR:** *"three directors were
aimed at cut-and-sew"* — **it was ONE director, three concepts**, and the negative result is
correspondingly weaker; **5.07 is that slot's BEST, not its mean (4.58)**; *"rev 77 re-based TWO
rows"* — **it was three**; and *"20 defects, 5 TOP"* where my own ledger lists **six**.

**AND ONE IT CONFIRMED THAT MATTERS: every one of the nine probe readings the brief publishes
reproduces**, as do all five T3 rungs, the per-rung sds, the four `LA RUEDA` cross-check deltas, the
concept-round counts (75 / 25 / 13 / 32 % / 55-of-75 / 510 KB), and every carrier-string guard.
**F328's trap was not sprung.**

---

## §7 THE MACHINE AT CLOSE

*(every figure below was watched printing in this session; none is transcribed)*

```
  verify_clone.sh         ALL 445 PASS -- 0 FIDELITY, 445 SELF-CONSISTENCY
                          on the MERGED tree, five side frames in out/
  bootstrap.sh            ALL 10 PASS  on a COLD CLONE at 73e8780, no out/ at all
                          (it read 9 PASSED / 1 FAILED before F337's repair -- that
                           is what the repair was for, and it is the whole reason
                           the cold clone is the LAST act and not the first)
  build.py T1_VERIFY=1    VERIFY: 0 fail, 0 warn  at T1_SUB=2, via audit.py
  STATE.md                REGENERATED, and it moved THREE LINES, all provenance:
                          generated / git commit / git subject.  Not one measured
                          figure changed.  That is the evidence this revision
                          carried no geometry, and it is why rule 55 is at the top
  photometry.py           9 checked, 0 FAILED
  audit_brief.py          14 checked, 0 FAILED
  audit_adversary.py      61 asked, 0 BROKE
  revstats.py             rev 77: 19 commits, 0 geometry, 6804 doc, 369 instr,
                          0 CLOSED.  "LAST FIVE REVISIONS (73-77): 261 geometry
                          lines, 0 findings closed."
  sheet3_notissued.py     45 checked, 0 FAILED
  la_rueda.py             14 checked, 0 FAILED
  line_pass.py            side/front wheel: 462 strokes / 1453 points
                          T1_LINE_NOCONTOUR=1 -> 115 / 312   (the watched kill)
  probe_rev73_tailboard   5 checked, 1 FAILED -- T4 only, BY DESIGN, on every one
                          of the five rev-77 side frames.  T3 no longer flips
  probe_rev77_t3floor     n = 5, range 2.50 deg, sd 1.282, 2 PASS / 3 FAIL
```

⚠ **AND THE ROW THAT MATTERS MOST HERE IS `revstats.py`'s LAST COLUMN: 0 FINDINGS CLOSED, FOR THE
FIFTH REVISION RUNNING.** Rev 77 refuted, superseded, corrected and retracted — F324's clusters,
F335's own conclusion, two of my own claims in F334, and the pillar thesis's scope — **but it RETIRED
nothing.** The brief's §3 heading was changed from *"WHAT REV 77 CLOSED"* to *"WHAT REV 77 SETTLED"*
for exactly this reason: **the instrument and the heading disagreed, and the instrument was right.**

⚠ **`audit_adversary.py` READS 61 ASKED / 0 BROKE AND THAT IS NOT ENTIRELY GOOD NEWS.** Its own output
says *"The rev-63 batch is still the oldest and is the next one to replace"* — `HANDOFF_CARRIERS.md`
§10.5 requires the adversary's questions to be REPLACED each revision, *"a question that can no longer
fail is not a control"*, and **rev 77 replaced none.** Ten revisions unacted. Recorded here rather
than left for the next rule-17 pass to find.

⚠ **AND F329 FIRED AS PREDICTED: running the closing instruments repainted tracked files under
`probe_scratch/`.** `git status --porcelain` went dirty, `git checkout -- probe_scratch/` restored it
to 0. **That is the documented side effect of a probe sweep, not a change — but a context that
committed without looking would have shipped it.**
