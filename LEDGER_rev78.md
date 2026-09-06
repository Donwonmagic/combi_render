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
| `sheet.py` | gains `area()` (filled polygon, with holes) and per-primitive colour. **The three rev-77 artefacts re-emit BYTE-IDENTICAL**, which is checked, not assumed |
| `line_pass.py` | gains an explicit-camera bake path |

**THE OCCLUSION HALF OF THE OWNER'S LOCKED STYLE SENTENCE NOW EXISTS.** The rev-77 brief
said *"no normal pass, no AO pass"* and the rule-15 adversary confirmed it against the
whole tree. `sticker_pass.py` enables Cycles' AO pass and the shading term
(Combined ÷ DiffCol). Both are drawn. **If the AO pass is unavailable the capture
records `ao: false` and `sticker.py` REFUSES to draw an occlusion layer rather than
passing the shading term off as one** (rule 37).

---
## §3 THE INSTRUMENTS THAT WERE WRONG, AND HOW EACH WAS CAUGHT

**Rule 4 says budget for this; it is normal here. Rev 78 found SIX of its own, and NOT
ONE was found by reasoning about the code.** Five were found by looking at a picture and
one by a fabricated-mask selftest.

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

It ran read-only and returned **14 defects** plus a long confirmed list. It also **hit
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
  constants. They are reported on every run and labelled AUTHORED on the artefact, but
  **they were tuned by looking, and a different context would tune them differently.**
* **A PHOTOGRAPH OF A REAL TACOMBI SHOPFRONT OR SIGN IS STILL OWED AND STILL NOT SUPPLIED**
  (asked at rev 77's close). Every reference in this tree is the vehicle.
