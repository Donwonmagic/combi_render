# LEDGER — rev 78

**RULE 55, AT THE TOP, AS IT REQUIRES.**
**THE VEHICLE DID NOT MOVE. `revstats.py` reads rev 78 as `0 geometry lines`, and
`74–78: 138 geometry lines, 0 findings closed`.** What shipped is the project's
ORIGINAL DELIVERABLE — the die-cut sticker, F18, open since rev 44 — as a thing the
owner can look at, plus the capability under it. He has looked at it twice.

**Every figure below was read from a script that ran. Where a figure is a POSE or an
AUTHORED choice it says so. Nothing here is a fidelity claim.**

---
## §1 WHAT THE OWNER RULED, MID-REVISION, AND IT CHANGED THE WHOLE BUILD

He was sent the first proof. His words, verbatim:

> **"Oh god that looks terrible. I'm worried we're too committed to the model rather
> than the combi itself."**

Put four options as multiple choice, he chose **DRAW IT, MODEL AS UNDERLAY**. **F346.**

**HE WAS RIGHT, AND THE DIAGNOSIS WAS BETTER THAN MINE.** The first pipeline clustered
the *rendered albedo* into seven inks and drew all **2091** line strokes. That albedo is
DELIBERATELY WEATHERED — `SPEC` §3 locks the finish as weathered, correctly, for the
photoreal render — so the clustering spent its inks on grime and the bus came out
mud-coloured. And the galley is twenty-odd separate objects, every one of which got its
own outline, so **the drawing rendered its own kitchen through the serving apertures.**

The rebuild asks the model only **where** things are, which it knows exactly through the
material index, and an **authored palette** decides what each prints in. The three paints
are the project's MEASURED constants (`t1_mats.RED / CREAM / GOLD`); what is authored is
the ASSIGNMENT, not the ink. Every `gal_*` collapses to ONE dark void. **Line count
2091 → 190.**

⚠ **THE SECOND HALF OF HIS SENTENCE IS NOT ANSWERED BY THIS ARTEFACT AND MUST NOT BE
TREATED AS IF IT WERE.** Whether the PROJECT is too committed to the model is a question
about the project. F18 waiting **34 revisions** behind *"build it after the model is
done"* is evidence for him, not against. A future context should not read F345 as
closing that.

---
## §2 WHAT SHIPPED

| file | what it is |
|---|---|
| `design_out/sticker_r78_flank.svg` / `.png` | **THE ARTEFACT.** 18° read off the FLANK (72° azimuth) — the reading the spec's own table argues for |
| `design_out/sticker_r78_nose.svg` / `.png` | the other reading of the same truncated row, drawn so he can choose by looking |
| `sticker_pass.py` | the 3D capture: material-index map, albedo, alpha, the light term, the AO pass, and the line pass baked **through the same camera** |
| `sticker.py` | the drawing and its checks — **37 checked, 1 FAILED**, and the failure is F353, a finding about the spec row |
| `sheet.py` | gains `area()` (filled polygon, with holes) and per-primitive colour. **TWO of the three rev-77 artefacts re-emit BYTE-IDENTICAL** — `sheet3_notissued.py` (45/0) and `calendario.py` (14/0), both watched. ⚠ **THE THIRD, `la_rueda.py`, NEEDS `probe_scratch/rueda.json`, WHICH IS UNTRACKED — so on a clone it cannot be checked at all, and NO `verify_clone.sh` ROW BINDS ANY OF THIS.** The first draft said "the three … which is checked, not assumed"; two of three were, and a companion row is owed (§3b) |
| `line_pass.py` | gains an explicit-camera bake path |

**THE OCCLUSION HALF OF THE OWNER'S LOCKED STYLE SENTENCE NOW EXISTS.** The rev-77 brief
said *"no normal pass, no AO pass"* and the rule-15 adversary confirmed it against the
whole tree. `sticker_pass.py` enables Cycles' AO pass and the shading term
(Combined ÷ DiffCol). Both are drawn. **If the AO pass is unavailable the capture
records `ao: false` and `sticker.py` REFUSES to draw an occlusion layer rather than
passing the shading term off as one** (rule 37).

---
## §3 THE INSTRUMENTS THAT WERE WRONG, AND HOW EACH WAS CAUGHT

**Rule 4 says budget for this; it is normal here. Rev 78 found SIX of its own, and NOT ONE
was found by reasoning about the code.** ⚠ **COUNTED FROM THE TABLE BELOW, not asserted:
FOUR by looking at a picture, ONE by an ablation (`T1_STK_NOHOLES`, after three wrong causes
had been eliminated), ONE by a fabricated-mask selftest.** The first draft of this sentence
said "five by looking and one by selftest" and disagreed with its own table — this project's
record names *"four, five and six in one document"* as a defect class, and the rule-17
adversary caught it here (rule 13).

| # | the defect | what it printed while wrong | how it was caught |
|---|---|---|---|
| 1 | material classification read `Base Color.default_value`, the UNCONNECTED default on the **22 of 45** materials that LINK that socket — `T1_paint`, the body red, among them | `ink_red` nearly EMPTY on a bus that is mostly red, with *"5 family masks, 99.99 % of the silhouette covered, 0 px of overlap"* | **PAINTING THE MASKS AND LOOKING** (rule 8). One second. **F351** |
| 2 | Blender 4.x's default **AgX view transform** applied to the DATA passes on the way out | an ORANGE bus and a TAN mural, with **all 32 checks passing** | looking at the proof. **F351** |
| 3 | `sheet.py`'s `tint` mixes toward the **STOCK**, so shading drawn at tint 0.34 paints **opaque pale grey** over the artwork | a grey halo round the bus, a grey wash over the roof and apertures, and a band covering the lower half of the wordmark | looking — **after misdiagnosing the same symptom twice**. **F350** |
| 4 | the die-cut opening (r ≈ 19 px) was masking the **ARTWORK**; the spec's 0.159 m rule governs the **CUT LINE** only | the SEÑOR TACOMBI wordmark as an unreadable blob; most of the paisley gone | painting the `script` mask: **12 864 px of perfectly legible, correctly foreshortened wordmark.** Nothing was too fine. **F349** |
| 5 | `holes_of` treated every OTHER ink's region as a hole | **pure-white blotches** — bare stock, a colour in none of the seven inks — across the flank, mural and roof | the `T1_STK_NOHOLES` ablation, after **three wrong causes were eliminated first**, one of which cost a render |
| 6 | the die-cut instrument, wrong **five ways at once** (closing before opening; broken idempotence; components counted after the bleed so the guard could never red; the bridge leaving thin slivers; an O(n·k²) opening too slow to run) | — | a **fabricated mask whose answers are known by construction**, now committed as `sticker.py --selftest` |

⚠ **DEFECT 4 IS THE ONE TO READ TWICE.** I misdiagnosed it as *"the lockup is too fine to
resolve at 1:70"*, then as *"the despeckle filter is eating it"*, and had already begun
fitting `script_gen.build_hi()` over it as a stencil workaround. **The stencil was the
wrong answer to a question that was a bug.** Painting one mask settled it.

---
## §4 THE MEASUREMENTS THIS REVISION ADDS

**THE SCALE, RECOVERED RATHER THAN GIVEN (F347).** The surviving spec never states the
sticker's scale; it states consequences of one. `t1_detail.LOUV_PITCH` is **0.021111 m**,
IMPORTED not transcribed, and printed at the spec's stated 0.30 mm that is **1:70.37**.
Two independently obtained quantities — one from the audit document, one from the source
— so the recovery is not a tautology (rule 6). **It cross-checks:** at that scale the
spec's 0.159 m minimum cut feature lands at **2.259 mm**, a real die-cutter's minimum,
and its 0.40 mm sacrifice threshold is **28.1 mm** on the vehicle.
⚠ **CEILING, MEASURED NOT ASSUMED: a 78 mm lens is not orthographic, so 1:70 holds
exactly only at the vehicle's centre depth. Across the bounding box the scale spreads
44.4 %.** It is printed on every run. "1:70" is nominal.

**THE COLOUR-SEPARATION CLAIM DOES NOT SURVIVE (F353).** `AUDIT_rev43.md` asserts the
vehicle is *"ONE 70° hue wedge plus four neutrals"*. **MEASURED: 89.6°** over all 24
chromatic materials, **89.2°** over the 16 holding ≥ 0.1 % of chromatic area. `C4` is
left RED rather than re-based, because **it is a finding about the spec row, not about
the drawing.** ⚠ Both figures are reported with the excluded materials NAMED; reporting
only the flattering one would be the defect. ⚠ The red/gold classification margin is as
thin as **0.18°** on one material — the split is REPORTED, not settled. ⚠ The `nose`
capture measures **200.0°** on the same asset, a wrap-around artefact of a different
visible material set, and that is **unexplained**. Do not quote either without its capture.

**THE ABLATIONS, WATCHED FAILING (rule 3).** `T1_STK_NOBRIDGE=1` reds **D1** (3 pieces,
not 1). `T1_STK_NOOPEN=1` reds **D14** (197 px still thinner than the rule) and the 5 px
test aerial survives. `T1_STK_NOHOLES=1` is kept because it is what identified defect 5.
`sticker.py --selftest` runs all of it in ~2 s and is run on every invocation.

---
## §5 WHAT THE RULE-15 ADVERSARY FOUND IN THE INCOMING BRIEF

It ran read-only and returned **14 defects** plus a long confirmed list. ⚠ **EIGHT of the
fourteen have register rows (F352–F359); SIX ARE UNLOCATED. An earlier draft of this ledger
said "all carried" — withdrawn (rule 13, and rule 16 on the revision that made rule 16 a
headline).** It also **hit
F357 live** — `audit_brief.py` shells `verify_clone.sh` internally, a FOURTH runner
F343's row does not name — and had to abort.

**The four that change what a context should do:** the sticker's locked VIEWPOINT is
absent from the brief entirely (**F348**); `audit_brief.py` as a hidden verifier runner
(**F357**); **seven owner-graded rows in no carrier at all** — `F56` `F91` `F93` `F94`
`F164` `F166` `F259` (**F356**); and `la_rueda.py` / `calendario.py` overwriting tracked
files that F329's stated remedy does not reach (**F358**).

**Also: `probe_rev77_t3floor.py`'s `0 FAILED` is a STRING LITERAL** and that probe cannot
report a failure (**F354**); **the line pass is not guarded by `verify_clone.sh`** at all
(**F355**); F18's own pointer to its spec is to the wrong section and two of the eight
rows are cut mid-sentence, one of them an **unrecoverable OWNER QUESTION about the cab
door** (**F352**); and three brief figures do not recompute (**F359**).

**WHAT IT CONFIRMED, which matters as much:** the fired/floated distinction is the
register's own words and not the brief's gloss; **F191 stands and was not withdrawn**;
the case-exact glyph inventory is right to the letter; the *"no AO pass anywhere"* claim
was true; the style sentence is genuinely his, from `NEXT_CONTEXT_PROMPT_rev39.md` §7;
`bootstrap.sh` row **9** is row 9; and §1's T3 arithmetic recomputes.

---
## §6 WHERE THIS REVISION IS WEAKEST, STATED

* **THE OWNER HAS SEEN IT TWICE AND CALLED THE FIRST VERSION TERRIBLE.** The second is
  better by his own redirect, not by any measurement. **There is no instrument in this
  tree that can tell you whether the sticker is good**, and none of the 37 checks tries.
* **NOT ONE CHECK COMPARES IT TO A PHOTOGRAPH OF A PRINTED STICKER.** None exists.
* **HIS WHEELS SENTENCE CANNOT BE HONOURED.** *"I like how the wheels were drawn in the
  earlier cartoon version"* — that version is still not in this repository. The artefact
  says so on its own face. **Still owed by him.**
* **THE VIEWPOINT IS UNANSWERED (F348).** Both readings are drawn and sent; he has not
  chosen. **No document may quote 18° as measured.**
* **THE CAB-DOOR OWNER QUESTION IS UNRECOVERABLE (F352)** and has never been put to him.
* **`sheet.py`'s TINT TRAP IS STILL THERE** for the next caller (F350). Rev 78 worked
  around it in `sticker.py` rather than fixing the module.
* **THE SHEET IS A POSE IN ONE MORE WAY:** `DESPECKLE_MM`, `ALBEDO_BLUR_MM`,
  `SHADE_BLUR_MM`, `SHADE_MULT`, `AO_MULT`, `LINE_MIN_MM` and `BLEED_MM` are all AUTHORED
  constants. ⚠ **The first draft of this line claimed they were "labelled AUTHORED on the
  artefact". THEY WERE NOT — they were reported at run time only, and the sheet's AUTHORED
  line named four ELEMENTS, not one constant. The rule-17 adversary extracted the SVG's six
  text nodes and showed it. The colophon now prints all seven** (rule 13). They are still
  **tuned by looking, and a different context would tune them differently and get a
  different sticker.**
* **A PHOTOGRAPH OF A REAL TACOMBI SHOPFRONT OR SIGN IS STILL OWED AND STILL NOT SUPPLIED**
  (asked at rev 77's close). Every reference in this tree is the vehicle.

---
## §7 WHAT THE RULE-17 ADVERSARY FOUND IN THE BRIEF **I** WROTE

**29 findings. Nine change what rev 79 should do; all nine are fixed, and the fixes are
recorded in `NEXT_CONTEXT_PROMPT_rev78.md` §8 so the next context knows this file was
tested and where it was weak.**

**THE TWO THAT MATTER MOST WERE BOTH SELF-INFLICTED IRONIES:**

**`F345` was not a row.** It had been appended to F344's line with no newline — one
3465-character line carrying two findings — so the register's own table could not render
the project's oldest live row. **F344 is the row about a finding that lost its register
row.** One newline.

**THE VIEWPOINT ROW IS NOT TRUNCATED, AND I SPENT AN OWNER QUESTION ON SOMETHING THE RECORD
ANSWERS.** I wrote that `AUDIT_rev43.md`'s VIEWPOINT row was hard-cut and its disambiguating
sentence lost. **MEASURED: its DESIGN cell is 142 characters and ends in a full stop** —
*"…The face and the flank are provably exclusive; choose the flank."* What is hard-cut at
120 is a DIFFERENT COLUMN on all eight rows, the trailing symbol list. Only rows 2 and 8
end mid-thought. **So the face/flank question was already settled in the record, in favour
of the flank, and the A/B I sent the owner asked him something he did not need to answer.**
The claim was wrong in the brief, in F348, in `sticker_pass.py`'s docstring **and on the
shipped artefact's own colophon** — all four are corrected. ⚠ **`CONCEPT_ROUND_rev77.md`
§5.0b item 5 carries the same error and was almost certainly where I inherited it.**

**AND ONE GUARD OF THE 37 COULD NEVER HAVE FIRED.** `sticker.py`'s S1 asserted the identity
that DEFINES the recovered scale — residual exactly 0.0. Rule 6, in the revision whose own
ledger quotes rule 6. Replaced with a comparison against `STATE.md`'s overall length
(65.1 mm at 1:70.37, a quantity the recovery does not use) and **watched failing at 10× and
¹⁄₁₀× the scale**.

**Eight published figures did not recompute** and are corrected or withdrawn: the closure
run (five per the script, **seven** in truth, not six); *"2091"* strokes (the captures read
2103 and 1719); *"2104"*; *"153 characters"* (149 and 150); *"three untouched concepts"*
(two — the third is the sticker this revision built); *"14 findings all carried"* (eight);
the *"wrap-around artefact"* explanation of the nose capture's 200° (`_arc()` IS wrap-safe,
so the span is real and remains **unexplained**); and the 0.18° classification margin quoted
without the **0.1 % of chromatic area** that sizes it.

⚠ **AND WHAT IT COULD NOT CHECK, WHICH IS THE REAL CEILING ON THIS AUDIT:** it did not run
`verify_clone.sh`, `audit_brief.py`, Blender, `sticker_pass.py` or `la_rueda.py`. So the 449
total, `--fix-count`'s behaviour, the three `T1_STK_*` ablations **against a real capture**
rather than the fabricated mask, and the third leg of the byte-identity claim are unverified
by it — and **no verifier row binds any of them.**
