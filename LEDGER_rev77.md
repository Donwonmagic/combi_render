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

## §5 WHAT THE RULE-15 ADVERSARY FOUND IN THE INCOMING BRIEF — 20 DEFECTS, 6 TOP

*(This heading said **5 TOP** and its own list numbers SIX; §6 of this ledger flagged one instance and
the brief flagged the other, so the document contradicted itself twice about its own count — four,
five and six in one file. Corrected at rev 77's close, rule 13. **READ THE LIST, NOT A HEADING.**)*

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


---

## §8 WHAT REV 78 INHERITS, AND THE ONE THING IT IS OWED

**THE CONCEPT ROUND IS COMPLETE AND IN THE REPOSITORY.** Three carriers, 1.53 MB, all in
`git ls-files`: `CONCEPT_BENCH_rev77.md` (75 concepts in full), `CONCEPT_AUDIT_rev77.md` (60
adversarial verdicts across four lenses), `CONCEPT_ROUND_rev77.md` (the synthesis, the last six
amplifications, both late completeness critics). **The chain ran end to end for the first time**, and
§9.2's *"critics BEFORE the synthesis as well as after"* is satisfied in both halves.

**THE LIVE DIRECTION IS THE LOCATIONAL SERIES (F340 / F341), AND IT IS THE ONLY ITEM ON THE RANKED
LIST THE OWNER RAISED HIMSELF.** Bethesda is the hero and sets the format. The constraint is already
measured — the vehicle's hand can spell *Tacombi* and nothing else — and he has ruled on both the
lettering (draw the missing glyphs, **labelled AUTHORED**) and the artefact (**the name is the
system**, running across board, plate and table item).

⚠ **THE ONE THING REV 78 IS OWED AND DOES NOT HAVE: A PHOTOGRAPH OF AN EXISTING TACOMBI SHOPFRONT.**
All eighteen reference images in this tree are the vehicle. **Rev 76's completeness critic finding
9(d) — *"an identity system is proposed against a brand whose identity nobody has seen"* — has been
open since rev 76 and now bites directly**, because the next revision authors letterforms that will
sit above a real door. It was asked for at this close and is not yet supplied. **The work can
proceed; the ceiling is lower, and the artefact must say so.**

⚠ **AND ONE ASSUMPTION THAT IS MINE, NOT HIS, LEFT VISIBLE ON PURPOSE:** *Crystal City → El Cristal*
is the derivation I inferred from the name he gave. **He never said it.** If it is wrong, the
generator recorded in F340 is wrong and every future site name inherits the error. **Confirm it
before printing it as the system's rationale.**

**AND THE ORCHESTRATION LESSON, WHICH COST MORE THAN ANY OTHER MISTAKE THIS REVISION.** The 107-agent
round stalled three times on session limits and re-ran work on every resume — **110 audit verdicts
where 56 were needed, 42 amplify agents for 14 concepts.** The cause was mine and it is one line: the
finalist list was built by iterating an object whose insertion order depends on which screen agent
returned first, so cached results came back in a different order, ties resolved differently, prompts
changed, and the resume cache missed. **If you fan out and intend to resume, SORT YOUR WORK LIST ON A
STABLE KEY.** The owner caught the second-order consequence — that I had jumped to the synthesis on
8 of 14 amplifications — and two of the six I nearly skipped were among the only four concepts whose
danger the audit found INTACT.


---
## §9 F342 — THE ENTRY FILE WAS LYING ABOUT ITS OWN IMPORTS, AND IT COST 70 % OF EVERY PICKUP

**FOUND WHILE ANSWERING THE OWNER'S REQUEST FOR *"a healthy bit of leeway for this new context to
execute effectively"* — so the finding is a direct answer to a question he asked, not a tidy-up.**

`CLAUDE.md`'s Imports section carried, as prose rather than as a list entry:

```
    **@HANDOFF_CARRIERS.md is the OTHER HALF OF THE BRIEF and it is NOT imported -- read it when the
    action brief points you at it.**
```

**THE AT-SIGN IS HONOURED ANYWHERE ON A LINE, NOT ONLY AT COLUMN 1.** So the file that sentence
disowns was inlined into the system prompt of every session since the rev-70 split.

**MEASURED, NOT INFERRED — `wc -c`, watched printing before any of it was written down:**

```
    CLAUDE.md                    9,469
    PASTE_INTO_CLAUDE_CODE.txt  26,671
    STATE.md                    12,205
    HANDOFF_CARRIERS.md        111,863   <- the file that says it is not imported
    ------------------------------------
    auto-loaded                160,208   of which the disowned carrier is 69.8 %
    what it should have been    48,345
```

⚠ **AND THE EVIDENCE IS DIRECT RATHER THAN A CLAIM ABOUT A PARSER: THIS REVISION'S OWN SYSTEM PROMPT
CARRIES THE LINE `Contents of /home/user/combi_render/HANDOFF_CARRIERS.md (project instructions,
checked into the codebase)`.** I did not reason about it; I read it in the context I was handed.

**WHY IT MATTERS MORE THAN ITS SIZE.** The rev-70 split exists because the owner measured what a
95 KB brief cost — *"I feel that we were way more productive in the first 20 or so handoffs and I fear
we have drifted since then"* — and `HANDOFF_CARRIERS.md`'s own header announces that the split
answered him. **It did not. The split moved 111 KB out of the working document and the at-sign put
111 KB straight back into the context**, so seven revisions opened roughly 3.3× heavier than the split
intended, while the file explaining the split was the payload.

**THE FIX, AND WHAT IT DELIBERATELY DOES NOT DO.** The at-sign is removed and the paragraph now
carries why, so the sentence is true for the first time. **NOTHING WAS DELETED (rule 16):** the
carrier file is byte-unchanged, `CLAUDE.md` still names it, `PASTE_INTO_CLAUDE_CODE.txt` §6 still
points at it, and — checked, not assumed — **all 16 `verify_clone.sh` rows that guard its content read
the FILE ON DISK, never the import**, so the guard surface is exactly as strong. The one guard that
does read an import (`grep -c '^@PASTE_INTO_CLAUDE_CODE.txt' CLAUDE.md`) is anchored at column 1 and
was never involved.

**FOUR NEW ROWS, AND THE KILL WAS WATCHED (rule 3).** Row 1 counts the import construct itself; row 2
requires the carrier not to be among them; row 3 is **arithmetic over bytes computed from the files on
disk on both sides**, so neither side is a literal that can go stale (rule 5, rule 6); row 4 requires
`CLAUDE.md` to still name the carrier by filename. **Putting the at-sign back reds THREE and leaves
row 4 correctly GREEN** — printed:

```
    FAIL  CLAUDE.md imports exactly the two files its Imports section names   got 3  want 2
    FAIL  CLAUDE.md does NOT import the carrier it says it does not import    got 1  want 0
    FAIL  the auto-loaded startup set is under half what the at-sign cost     got 0  want 1
    ok    CLAUDE.md still names the carrier by filename                       1
```

**Row 4 staying green under the kill is the point of row 4: it is the row that stops this fix from
becoming rule 16's defect**, and it would have caught me had I answered the load problem by deleting
the pointer instead of the at-sign.

⚠ **THE CEILING, AND IT IS NOT SMALL.** This is a fix to the project's ERGONOMICS. **It is not
evidence about the vehicle, it closes nothing on the ranked list, and rule 55 does not count it.**
And it moves a real cost onto the next context: **that carrier used to arrive free and now must be
opened deliberately** — §2's seventeen refuted emblem rows, §4's rulings and §5's rules 34–58 are
exactly the material a context is most likely to skip and most expensive to re-derive. **The brief's
own F342 row says so in the imperative.**


---
## §10 F343 — THE TOP INSTRUMENT CANNOT BE RUN TWICE AT ONCE, AND IT FAILS BY LYING

**FOUND BY ACCIDENT, WHICH IS THE ONLY REASON IT WAS FOUND AT ALL.** I ran `./verify_clone.sh` in the
working tree while the rule-17 adversary was running it in `/tmp/cc`. My run returned:

```
    442 PASSED, 7 FAILED
      FAIL  modified tracked files                                         got 6        want 0
      FAIL  F281 a non-numeric T1_REAR_OPEN refuses too, rather than crashing  got <empty>  want 1
      FAIL  F284 probe_rev67_nose REFUSES to window a frame that is not `front`  got <empty>  want 1
      FAIL  F284 ... and counts that refusal as ABSENT, never as a pass      got <empty>  want 1
      FAIL  F284 ... and REFUSES a `front` frame with no build               got 0        want 1
      FAIL  F284 the T1_NOSE_NOWIN kill really ablates                       got 0        want 1
      FAIL  newest brief states THIS script's row count                      got 445      want 443
```

**Two of those seven are expected** — a dirty tree, and the self-referential count that
`audit_brief.py --fix-count` writes last. **The other five are a COLLISION.** The script writes and
then `rm -f`s **twenty fixed `/tmp` paths**, counted off the source:

```
    _r72b _r72g _r72n _r72r _r72s _r72t _r73a _r73b _r73c _r73d _r73e _r73f _r73g
    _r74a _r74b _r75f326   (.txt)
    _r73_x_front.png  _r73_x_hero34f.png  _vc_senor.png  _vc_senor_pre.png
```

**None is namespaced by pid, clone or run**, so two runs delete each other's evidence mid-flight and
the rows that read those files report `got <empty>` or `got 0`. **All five reds fall inside exactly
the two blocks that share those paths.**

**WHY THIS IS WORSE THAN NOISE, AND WHY IT BELONGS IN A LEDGER RATHER THAN A README.** The failure
mode is **not an error — it is a plausible red row**, which is the defect class `CLAUDE.md` names as
this project's most-repeated: *"every one produced a plausible number that would have been
published."* And the brief's own §3b instructs the reader that **a red row is a FINDING ABOUT YOUR
CHANGE**, with rule 44 making the guard the default winner. So a colliding run does not merely add
noise; **it accuses the reader's own work, and the rules then tell them to believe it.**

⚠ **AND IT IS STRUCTURALLY LIKELY, NOT A FREAK.** Rules 15 and 17 both require dispatching
adversaries; an adversary's first act is `./bootstrap.sh` and `./verify_clone.sh`; and §7.6 makes a
cold clone run it a third time. **The revision that mandates concurrent verifiers ships a verifier
that cannot be run concurrently.**

**NOT FIXED — RECORDED (rule 12, and stated rather than hidden).** The repair is source churn on the
top instrument after its last clean run, and I would be editing the script that scores my own
revision. **THE FIX IS PRESCRIBED AND CHEAP:** `_VCTMP=$(mktemp -d)`, every `/tmp/_r7*` moved under
it, `trap 'rm -rf "$_VCTMP"' EXIT`, plus one row that reds if any bare `/tmp/_` path survives in the
source — which is a row anchored on the SOURCE, not on a grep for a name (rule 50).

⚠ **CEILING, AND IT IS THE honest one: n = 1.** I observed one collision; I did not construct the
race deliberately. The five reds are consistent with the mechanism and clustered exactly where the
shared paths are, and the mechanism is **read from the source** — but it has **not been WATCHED
FAILING on a controlled pair** (rule 3). It is graded `OBSERVED-rev77`, not `MEASURED`. **Whoever
fixes it should first run two verifiers on purpose and watch these same five rows go red.**


---
## §11 THE FINAL RULE-17 AUDIT — 20 DEFECTS, 6 TOP, ALL ACTED ON

**Rule 17 says re-run the outgoing adversary after anything ships. Rev 77 shipped F342 and F343 after
the first pass, so a second adversary was dispatched at the FINAL handoff. It returned twenty more.**
Every top defect below was **re-measured by me before I acted on it** — an agent's report is not
evidence either.

### The six at top severity

1. **THE BRIEF CONTRADICTED ITSELF ON THE GAIN CLAIM, IN THE FIRST AND LAST PLACES A READER LOOKS.**
   §1 retracts *"1.8 σ"* and gives 3.86 σ on the SEM; the closing weakness list restated **"T3's GAIN
   CLAIM IS 1.8 σ"** as the brief's standing position. Confirmed: `grep -n "1.8 σ"` → lines 109 and
   355. **F322's class — an amendment reaching some sections and not others — in the brief whose §1
   boasts of catching it.** Fixed.

2. **THE GLYPH INVENTORY WAS CASE-BLIND, AND IT UNDERSTATED THE OWNER'S OWN RULING BY THREE LETTERS
   PER NAME.** `script_gen.py` holds `draw_T` (*"Capital T"*) and six LOWERCASE letterforms. Recomputed:

   ```
                                   distinct   missing CAPS            published (case-blind)
       TAQUERIA EL CRISTAL            10       9  A C E I L Q R S U    6  E L Q R S U
       TAQUERIA BUENA BETHESDITA      12      11  A B D E H I N Q R S U 8  D E H N Q R S U
   ```
   No mixed-case escape: any capitalised second word needs a capital `C`, `E` or `B`. **The owner was
   put a multiple-choice question about drawing "six to eight" glyphs for a setting that needs nine to
   eleven. HIS RULING STANDS; THE QUANTITY HE WAS GIVEN DOES NOT, and he must be told.** Fixed in the
   brief and in F340.

3. **A THIRD SHIPPED ARTEFACT WAS INVISIBLE IN BOTH HANDOFF DOCUMENTS, AND ITS OWED REGISTER ROW WAS
   LOST TO A DOUBLE-ASSIGNED ID.** `grep -c calendario` → **0** in both. `CONCEPT_ROUND_rev77.md`
   §5.0b closes *"A register row is owed; the next free ID is F341"* — **F341 was spent on the
   locational rulings.** This is **rule 16 firing twice in the revision that made F335 a headline.**
   Now **F344**, and the calendar is named in the brief.

4. **THE BRIEF PROMOTED F340 TO A "RULING" AND TO REV 78's #1 JOB; THE REGISTER SAYS IT IS NEITHER.**
   F340, verbatim: *"THE WORD IS 'maybe' — this is recorded as a DIRECTION HE FLOATED, not a ruling he
   made, and nothing should be built on it as though it were F330's kind of instruction."* The brief's
   own §6 says that file **outranks prose**. **Ranking it above F18 — which he DID fire — inverted the
   only two owner signals on the list.** Fixed: it is now *"a locational series he floated"*, and the
   brief says **RANK THEM YOURSELF.**

5. **THE FILE THE BRIEF NAMED AS *"ranks and decides"* STILL SAYS THE ROUND DID NOT FINISH, AND THE
   TWO FILES THAT CONTRADICT IT WERE NAMED NOWHERE IN THE BRIEF.** `DESIGN_PROGRAM_rev77.md` §4.2, live:
   *"STILL MISSING: 11 of 14 amplifications, the synthesis, and BOTH late completeness critics"* and
   *"no concept has been through the full chain"* — and it **has no §5**, because
   `CONCEPT_ROUND_rev77.md` §1 says *"This is §5, to append … placement is yours"* **and the placement
   was never done.** `grep` found neither `CONCEPT_AUDIT_rev77` (765 KB) nor `CONCEPT_ROUND_rev77`
   (255 KB) in the brief. **A next context following the brief literally would rank on the screen,
   which F338 says not to do.** Both are now in §6 with what they hold.

6. **`SPEC.md` §10.10 WAS QUOTED ACCURATELY AND APPLIED TO THE WRONG OBJECT — rule 34 exactly.** The
   *"hard bar"*, *"Not approximated. Not invented."* all verify. **But the sentence they govern reads
   *"Every painted element ON THIS VEHICLE"*, and its in-scope table is eight painted elements of the
   combi.** A shop sign in Bethesda is not one. **The owner's first locational question was framed on
   a requirement borrowed from another object.** The ruling may survive re-framing; the framing is now
   stated in the brief as needing to be put to him.

### The recomputations the brief's closing bullet points at

**Four published figures do not survive recomputation. Every conclusion they carry does.**

* **"60 verdicts across 14 finalists at 4 lenses"** — stated in `CONCEPT_AUDIT_rev77.md`,
  `LEDGER_rev77.md` §8 and `DESIGN_PROGRAM_rev77.md` §4.2. **14 × 4 = 56.** Counted: 60 verdict blocks
  over 14 concepts, because `BUENAS NOCHES, COMBI` carries **eight** — a residue of the resume-cache
  defect in §8. So: **56 distinct verdicts plus one concept audited twice.** The `1.85/4` headline
  double-weights it; the mean of the 14 concept means is **1.8486**. **Headline survives, stated basis
  does not.**
* **F338's Spearman ρ = +0.222** reproduces only under an arbitrary tie order; **tie-corrected it is
  +0.050.** The audit column is heavily tied (1.88×4, 1.75×4, 2.25×2, 1.62×2). **Pearson r = +0.173
  reproduces exactly.** This **strengthens** F338 — and ρ was published with no ceiling.
* **The line pass's four bare stroke counts.** §5.0b measures 2711–2716 strokes / 19468–19475 points,
  n = 5, one unchanged tree. §4's watched ablation `115 / 312` **re-runs as 116 / 312.** The ablation
  is real and large (462 → 116); **the figure is one draw.** Same defect as the calendar colophon (F344).
* **"55 of 75 food or people"** headlines `DESIGN_PROGRAM_rev77.md` §0 — and its own §3, ninety lines
  later, says *"Food or people is the SUBJECT of **21** of 75, not the 55 that claim it."* **F336's
  exact shape: a retracted figure still printed elsewhere in the same document.** This ledger's §6
  listed it among what the adversary CONFIRMED, which is true of the count and false of the claim.
* **"All 18 reference images are the vehicle"** — carried in three documents. `git ls-files` gives 22
  reference-class entries; `HANDOFF_CARRIERS.md` §0.1 gives a floor of 54 with 16 guard rows; some are
  DERIVED grids and `bus_model_ref.JPG` is a SCHOOL BUS. **The point — no photograph of a Tacombi
  shopfront exists — is true and load-bearing. The number was prose.**
* **"5,060,569 points across 250 frames"** is not re-derivable (20,234 × 250 is 2,069 short) and cannot
  be, the spike being deleted and the pass unstable. **Demoted to an anecdote in §4.**
* **`probe_rev77_t3floor.py` SILENTLY DROPS A FRAME IT CANNOT PARSE.** Six `*_side.png` on the rev-77
  tree; it printed `n = 5`. `out/fierro_side.png` yields no parseable rung, `read()` returns `None`,
  and the row is discarded with no message. **The distribution is conditioned on the ladder being
  readable, and the excluded frame is where the detector failed hardest.** Rule 37. **UNFIXED** —
  stated in the brief's §1.
* **`audit_brief.py` covers 5 of the ~9 probe counts the brief publishes.** It is a piece of the
  rule-17 half, not the half. Stated in §4.
* **`LEDGER_rev77.md` §7's revstats row was already stale** under a heading saying nothing in it is
  transcribed: `19 commits / 6804 doc` where live is `26 / 8731 / 374 instr`. The five-revision line
  `73–77: 261 geometry lines, 0 findings closed` **does** still reproduce.

### What the adversary CONFIRMED, on a genuine cold clone

**`./verify_clone.sh` on a cold clone of `f5454c7` with NO `out/`: `ALL 445 PASS`, rc = 0** — and the
brief's clause *"with an empty `out/`, SIX rows SKIP … PASS is the same either way"* verified in both
directions. The five T3 rungs, the per-rung sds, Pearson +0.173, `462 / 1453`, the seven `draw_` glyph
functions, §10.10's wording, the owner's locational quotation across three documents, the Sheet 3 ink
correction, and every probe count in §4 (`photometry` 9/0, `sheet3` 45/0, `la_rueda` 14/0, tread 8/0
with the kill reddening exactly T3 and T7, `vw` 12/2 = C4+C10, `fitpose` 5/1 = P4, proxy IoU 1.000000)
**all reproduce.** It also re-ran `sheet3_notissued.py` and `la_rueda.py` against a freshly baked line
pass and found `design_out/` **byte-identical** — stronger than this ledger had claimed for them.

### Where it said the brief OVER-CONSTRAINS — and what I cut

The owner asked for *"a healthy bit of leeway."* The adversary named six places the brief dictated a
solution where it should state a problem. **Five are now loosened:** the sticker's build order (it
said *"build the AO pass first or the sticker is line only"*, gating the project's original
deliverable on an infrastructure job the day its trigger fired — while `CONCEPT_ROUND_rev77.md` §5.2,
which the brief never named, argues for the daylight face BECAUSE it needs no occlusion); the garment
re-run (*"re-run it with three directors"* → the ceiling stated, the remedy left open); F318's
prescription (the `T1_TYRE_FILM` prohibition is earned and kept; the rest is now a suggestion, and the
brief says so, since it has been carried unchanged and undone for three revisions); T3's follow-up
rungs (*"Add a −3.0 and a −10.0. It is cheap"* → offered, not instructed); and the ranked list itself,
which now carries **"NOTHING FROM THE CONCEPT ROUND HAS BEEN SHOWN TO THE OWNER — his answer outranks
this list; getting one is a legitimate first move."** The sixth — §2.1's sequencing of the locational
series — is loosened rather than removed: the measured constraint stays, *"recovery outranks
invention"* is now *"worth weighing … your call, not this brief's."*

⚠ **AND THE BRIEF IS NOW 32,675 BYTES AGAINST A 32,768 GUARD — 93 BYTES OF HEADROOM.** Landing twenty
defects cost more than the trims recovered, even after compressing §1, §3, §5, §6, the head and the
closing block. **The next context cannot add a paragraph to that file without cutting one.** That is a
real constraint on the handoff and it is stated here rather than discovered by a red row.
