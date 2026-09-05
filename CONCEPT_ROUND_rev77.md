# THE ROUND, FINISHED — rev 77.  SYNTHESIS, THE LAST SIX AMPLIFICATIONS, AND THE TWO LATE CRITICS.

**CARRIER (rule 16), in the repository. `CONCEPT_BENCH_rev77.md` holds the 75 concepts;
`CONCEPT_AUDIT_rev77.md` holds the 60 audit verdicts; this file holds what came after them.**

**THE CHAIN IS COMPLETE: 25 directors → 75 concepts → 2 early critics → 3 screens → 14 finalists
→ 60 audit verdicts across 4 lenses → 14 amplifications → synthesis → 2 LATE critics.** §9.2 of the
rev-76 program asked for *"two completeness critics, run BEFORE the synthesis as well as after"*.
**Both halves have now run. The "after" pair had never run in this project before.**

⚠ **HOW THIS FINISHED MATTERS, AND IT IS RECORDED RATHER THAN TIDIED AWAY.** The original 107-agent
run stalled three times on session limits and, on each resume, RE-RAN work instead of replaying it:
**110 audit verdicts where 56 were needed, and 42 amplify agents for 14 concepts.** The cause was a
defect in the orchestrating script — the finalist list was built by iterating an object whose
insertion order depends on which screen agent returned first, so cached results came back in a
different order, ties resolved differently, prompts changed and the cache missed. **The last nine
agents were therefore run as a standalone job fed from data already on disk. Nothing was lost; a
great deal was repeated.** *(The first attempt at that standalone job jumped straight to the
synthesis on 8 of 14 amplifications — the owner caught it, and two of the six missing were among
the only four concepts whose danger the audit found INTACT. It was stopped and redone in order.)*

---
## §1 THE SYNTHESIS

**PLACEMENT.** This is `§5`, to append to `DESIGN_PROGRAM_rev77.md` after its existing `§4`. It supersedes `§2`'s ORDER only and says so; `§2` and `§4` are kept intact (rule 16). Full text also at `/tmp/claude-0/-home-user-combi-render/36d24290-245a-543a-b2d3-9d646e20e4c5/scratchpad/section5.md`. I did not edit the carrier myself — placement is yours, and `audit_brief.py --fix-count` must still run last.

**FIVE THINGS I MEASURED THAT ARE NEW TO THE RECORD** (all in §5.0b below, all watched printing at HEAD `959a9f8`): the 115-vs-118 lamp contradiction is settled (two different objects — photographed FFT estimate vs built count); **the line pass is not run-to-run stable in either count**, n=5 on one unchanged tree; **a shipped artefact prints one of those draws on its face without a spread** (`design_out/calendario_ano_xxii.svg`); the occlusion half is absent confirmed by grep, not assertion; and **no camera in `studio.views()` matches the sticker spec's locked viewpoint**. One register row is owed — **next free ID is F341** (F340 is highest, counted).

**TWO RETRACTIONS OF MY OWN, MADE IN-PLACE (rule 13):** after two bakes I had "strokes stable, points wobble" — the third bake read 2716 and I would have published it; and I initially counted `line_pass.py`'s SCENE-control comment as a same-view observation when it does not name its view.

---

---
## §5 THE SYNTHESIS — RANKED ON THE AUDIT, NOT THE SCREEN

**§2's table above is the SCREEN's ranking and it is kept (rule 16). This section supersedes its
ORDER and nothing else.** §2 stays because it records what the screen did; **do not build from it.**

### §5.0 WHY THE ORDER CHANGED, AND THE FOUR CEILINGS ON THE NEW ONE

**F338, `MEASURED-rev77`: over the 14 finalists the screen and the adversarial audit are essentially
uncorrelated — Pearson r = +0.173, Spearman ρ = +0.222.** `PROVECHO` screened **8.73, the highest of
all 75, and audits 1.50/4 — last of the fourteen.** Audit mean over 60 verdicts is **1.85/4**, so the
audit is harsh across the board and is not merely re-ordering a good field. `dangerIntact` is **TRUE
for only 4 of 14**: the fourth lens judged ten finalists to have had the thing that made them
dangerous sanded off.

**WHAT THAT LICENSES: rank on the audit. The screen decided what got audited and nothing more.**

⚠ **THE THREE CEILINGS F338 CARRIES, AND THEY BIND.** (a) **RANGE RESTRICTION** — the 14 were
selected BY the screen, so r is computed on the screen's own top fifth and would likely be WEAKER
over all 75; this understates the disagreement rather than overstating it. (b) **SINGLE JUDGE per
lens**, 0–4, no inter-rater check: an audit score is one opinion. (c) **n = 14.**

⚠⚠ **AND A FOURTH CEILING F338 DOES NOT CARRY, FOUND BY COUNTING THE BODIES RATHER THAN TRUSTING THE
HEADER. IT IS THE MOST IMPORTANT ONE IN THIS SECTION.**

**THE AUDIT SCORED THE PARENT CONCEPT. THE AMPLIFICATION THEN CHANGED THE OBJECT, AND IN MOST CASES
NOBODY RE-SCORED IT.** Eight of the fifteen amplified bodies carry `audit n/a` — they were never
audited after amplification. So for those eight, **ranking on the audit ranks a version of the object
that no longer exists.** `DE MANO EN MANO` was audited as a lino print of a tray crossing a brass
line and amplified into a **lithographed tin charola**; `¿TRAE SU ENVASE?` was audited as a returnable
bottle and amplified into a **jar of escabeche with a hand-painted band**. Those are not the same
objects and the 2.25 and the 1.75 do not travel with them.

**AND THE HEADER SAYS FOURTEEN AMPLIFIED CONCEPTS WHILE FIFTEEN BODIES EXIST. COUNTED, NOT
TRANSCRIBED.** The extra is `BUENAS NOCHES, COMBI`, which was **amplified TWICE** — into
`CIENTO DIECIOCHO Y UNA (118 + 1)` and into `APAGA LA LUZ`. ⚠ **DO NOT READ THAT AS AN ERROR TO TIDY
AWAY: two directors, working from one parent, independently produced a glow-vinyl die-cut sticker
whose lit elements are the serving apertures and the galley strip, whose daylight state is the shut
panel van, and which both refuse the word "asleep". That convergence is the strongest single piece of
evidence in the round**, and it is evidence about the children's line (§5.3).

**F331 COMPLIANCE, COUNTED: 6 of the 15 bodies DO NOT DECLARE A LINE** — `DE LA MANO DE`,
`CALENDARIO AÑO XXII`, `MARCA DEL COCINERO`, `MEDIA VENTANA`, `DIRECTO`, `TACOS Y`. F331 requires
every item to say which line it is in. **Where the body declares, I quote it. Where it does not, I
assign one and mark it `[ASSIGNED]` so the next context can overturn it.**

### §5.0b FIVE THINGS I MEASURED THIS SESSION THAT CHANGE WHAT MAY BE PRINTED

Every one was watched printing off live source at HEAD (`959a9f8`), not transcribed.

**1. THE PROGRAMME BRIEF'S "115 FESTOON LAMPS" AND THE CONCEPTS' "118" ARE BOTH RIGHT AND THEY ARE
DIFFERENT OBJECTS. SAY WHICH.** `t1_detail.py`'s own comment records an FFT along the string in
`ref_side.jpg`, top-5 periods 6.05–6.30 px at 211 px/m → *"pitch 28.6 +/- 1.0 mm, **~115 bulbs**"* —
that is the **PHOTOGRAPHED** estimate. The **BUILT** count is arithmetic on
`BULB_X0 = T._aft(-1.8000) = -1.6368056`, `BULB_X1 = 1.7000`, `BULB_PITCH = 0.0286`: span 3.3368056 m,
n = 117 intervals, `range(n+1)` → **118 lamps at a realised pitch of 28.5197 mm**. **Recomputed here
and both reproduce.** ⚠ **Skipping the `_aft()` call gives 123 — cite `_aft()` so the next reader can
recompute.** **Neither figure may be printed bare: an artefact says "118 built" or "~115 photographed",
never "115 lamps".**

**2. THE LINE PASS IS NOT RUN-TO-RUN STABLE, IN *BOTH* COUNTS — MEASURED, n = 5, ONE UNCHANGED TREE.**
Four bakes run this session plus the record's own figure, `line_pass.py --view side`, no source change
between them:

```
    strokes / points     2711 / 19473      this session
                         2711 / 19470      this session
                         2716 / 19475      this session   <- the STROKE count moved too
                         2711 / 19468      this session
                         2711 / 19471      the record -- the CALENDARIO body's own
                                           "--view side ... watched printing this session",
                                           and the figure the shipped SVG carries
      strokes 2711 .. 2716  (range 5)      points 19468 .. 19475  (range 7)
```

⚠ **ATTRIBUTION, STATED PRECISELY BECAUSE IT AFFECTS n: the four bakes are mine and all four are
`--view side`. The fifth is the CALENDARIO body, which names `--view side` explicitly, so all five
are one view. `line_pass.py`'s own SCENE-control comment carries the same 19471 but does NOT name its
view, so I am NOT counting it as a sixth.**

⚠ **MY OWN FIRST READING WAS WRONG AND I AM RETRACTING IT IN THE SAME SECTION (rule 13): after two
bakes I had "strokes stable at 2711, points wobble". The third bake read 2716. n = 2 was not enough
to say which half was stable, and I would have published it.** **This confirms F332's own ceiling —
*"COMPARE DRAWINGS, NOT COUNTS"* — with a number, on the shipped view.**

**3. AND A SHIPPED ARTEFACT PRINTS ONE OF THOSE DRAWS ON ITS FACE, TO FOUR SIGNIFICANT FIGURES, WITH
NO SPREAD.** `design_out/calendario_ano_xxii.svg` carries, in its colophon:
`DIBUJO: line_pass.py  2711 trazos / 19471 puntos  vista side  sub 1  pliegue …`
**The mechanism is honest and I checked it rather than assuming: `calendario.py` line 382 is a `%d`
format, not a string literal, and it reads a TRACKED cache, `probe_scratch/line_pass.json`, refusing
with a summary line if it is absent (rule 37, watched in the source). So the artefact IS reproducible
on a clone — re-running it gives a byte-identical SVG.** **The defect is narrower and it is real: the
number on its face is ONE DRAW from a distribution with a spread of 5 and 7, published as though it
were a constant.** ⚠ **THIS IS NOT A REASON TO PULL THE ARTEFACT.** The fix is one line — print
`~2711` with the observed range, or drop the counts, which carry nothing a reader can use. **A register
row is owed; the next free ID is F341** *(F340 is the highest in `OPEN_FINDINGS.md` at this commit —
counted, not transcribed)*.

**4. THE OCCLUSION HALF IS ABSENT, CONFIRMED BY GREP AND NOT BY ASSERTION.**
`grep -rln "use_pass_ambient_occlusion\|use_pass_normal\|use_pass_z" *.py` returns **nothing**.
No AO pass, no normal pass, no depth pass. **Anything in this section needing occlusion is line-only
today, and every such item says so in its own block.**

**5. NO CAMERA IN `studio.views()` MATCHES THE STICKER SPEC'S LOCKED VIEWPOINT.** `AUDIT_rev43.md`
carries **8 `sticker` rows** and the first locks *"VIEWPOINT — 18° front three-quarter from the
serving side, eye height 1.55 m. The face and the flank are provably exclusive; choose the flank."*
Azimuths computed off `studio.views()` this session, measured from the nose (+X) axis:
`side` 90.0° · `topdown` 57.8° · `hero34r` 38.4° · `detail_f` 35.4° · `hero34f` 34.7° ·
**`low34` 34.0° at camera z = 1.55 m** · `front34` 26.8° · `front`/`rear` 0.0°.
⚠ **`low34` matches the spec's 1.55 m eye height EXACTLY and I do not think that is a coincidence —
but its azimuth is 34.0°, not 18°.** ⚠ **CEILING, AND IT IS THE REASON I AM NOT PICKING: the spec row
is HARD-CUT and I cannot tell whether its 18° is measured off the nose axis or off the flank (which
would be 72° in my convention). All 8 rows survive with the DESIGN column intact and the *"Governing
symbols"* column truncated mid-name — `folk_gen.py :: D`, `folk_gen.py :: FLAN`, `lid_gen.py :: HEAD`,
`t1_mats.py :: the r`.** **The symbol lists are recoverable by grepping the named modules; the
convention is not, and it is one owner question or one painted A/B away.**

---
### §5.1 THE RANKED SHORTLIST

**Ordered by audit score, `dangerIntact` breaking ties — because the fourth lens exists precisely to
catch the sanding that hit 10 of 14, so a tie between a live risk and a sanded one is not a tie.**
Where an amplified body exists it is named and its figures are the ones quoted; **the audit score
always belongs to the PARENT** and is marked `[parent]` wherever the amplification was not re-scored.

| # | object (amplified name) | line | audit | danger | blocked on |
|---|---|---|---|---|---|
| 1 | **DE LA MANO DE** — tin charola | adult `[ASSIGNED]` | 2.25 `[parent]` | **intact** | AO pass; an illustrator |
| 2 | **DIRECTO** — the destination board | adult `[ASSIGNED]` | **2.25** | **intact** | nothing |
| 3 | **GRACIAS POR SU PREFERENCIA (1524.7)** — 16 s film | adult *(declared)* | 2.12 | false | AO pass; human geometry; an illustrator |
| 4 | **CALENDARIO AÑO XXII «YA VIENE»** | adult `[ASSIGNED]` | 1.88 | false | **SHIPPED — see below** |
| 5 | **EL TROQUEL — el lado ciego** | adult *(declared)* | 1.88 | false | depth pass |
| 6 | **MANDIL 515 · EL HUECO** — apron + 1:1 pattern | adult *(declared)* | 1.88 | false | nothing |
| 7 | **CIENTO DIECIOCHO Y UNA / APAGA LA LUZ** — glow sticker | **children** *(declared)* | 1.88 `[parent]` | false `[parent]` | nothing |
| 8 | **MARCA DEL COCINERO** — the branding die | adult `[ASSIGNED]` | 1.75 | false | the cooks' own ruling |
| 9 | **NO SE VENDE** — escabeche jar, painted band | adult *(declared)* | 1.75 `[parent]` | false `[parent]` | a −Y camera; DOHMH |
| 10 | **TACOS Y** — embroidered servilleta | adult `[ASSIGNED]` | 1.75 `[parent]` | false `[parent]` | a taller |
| 11 | **MEDIA VENTANA (HUECO No. 2, 1:2)** | adult `[ASSIGNED]` | 1.75 `[parent]` | false `[parent]` | AO pass |
| 12 | **A LA ALTURA · 118** — the instrument | adult *(declared)* | 1.75 `[parent]` | false `[parent]` | nothing |
| 13 | **MOTOR: NINGUNO — SILBATO 1:20** | **children** *(declared)* | 1.62 | **intact** | IP advice |
| 14 | **RUIDO** — six tray liners | adult *(declared)* | 1.62 | **intact** | an owner ruling |
| 15 | **PROVECHO** | adult `[ASSIGNED]` | **1.50** | false | not carried forward — see §5.4 |

---

**1 · DE LA MANO DE** — a lithographed tin **charola**, 380 × 290 mm, rolled edge, six inks; the well
deliberately **unvarnished** so the image abrades from the centre out under the plates. Rim, in
signwriter's script: `DE LA MANO DE — [cook's name] — [month, year]`. **LINE: adult `[ASSIGNED]` — a
named worker, a per-unit share and a wear record are not a child's object.**
**FIGURES:** the counter's rake — `CNT_ZT/CNT_ZB` 1.2540/1.1470 = **107.0 mm** thick, `CNT_Y_IN/OUT`
0.8450/1.1660 = **321.0 mm** plan depth, `CNT_X0` +0.9180 to `CNT_X1 = X_TAIL − CNT_OVERHANG` =
−2.1880, a **3.106 m** run; at `RAKE_DZDX` 0.017750 that is **55.1 mm of climb**, so above ground the
top runs **1189.8 → 1244.9 mm**. *(All five recomputed this session.)* Gold `CNT_NOSE_F` 0.1860 ×
107.0 = **19.90 mm in elevation.**
**RISK IT STILL CARRIES:** the image is **designed to be destroyed by its own use** and a wholesaler
may call that a defect and refuse it; and it **names and pays a worker on merchandise the company
sells**, which is a policy and not a picture — once you name one cook you have to name all of them.
**MODEL:** the rake. A counter drawn level is drawn wrong and no tape measure and no single
photograph says so. ⚠ **The parent body's "counter top 1254 mm above ground" is the AUTHORED
UN-DROPPED constant — 49–64 mm high depending on station. Corrected above; never quote a z without
its station.**
**FIRST STEP:** three lines in `studio.py` adding a `pass` camera at the forward bay, then one line
pass. ⚠ **BLOCKED for the finished object: the painted half needs an illustrator and the sampled
shadow needs the AO pass, which does not exist (§5.0b item 4).**

**2 · DIRECTO** — one hand-lettered **destination board**, 560.0 × 352.0 mm, r 40.25, on 1.5 mm
aluminium, hung on two hooks in the near pane of the actual bus's split screen. Reversible in ten
seconds; nothing rests on the glazing. The route reads terminal-biggest, and the leg the record does
not hold is set as a stop in the same hand: **`[ NO CONSTA ]`**. **LINE: adult `[ASSIGNED]` — a fixture
in a dining room, in Spanish only.**
**FIGURES:** `t1_shell.py` `WS_PANE_W, WS_PANE_H, WS_DIV, WS_R = 0.5850, 0.3770, 0.0260, 0.050`.
⚠ **CEILING THE BODY STATES AND I AM KEEPING: that constant carries NO provenance comment and is NOT
graded MEASURED. The board is sized off it, so the board inherits an ungraded number.**
**RISK IT STILL CARRIES:** a US-invested group painting a Mexican route board is a costume charge, and
`[ NO CONSTA ]` sharpens it deliberately — a route board with a hole where its papers should be,
standing in a New York room, and the people who can read it are the kitchen. The body **refuses** to
name or imply the kitchen's immigration status and says so rather than calling the refusal a fix.
**MODEL:** it takes the photograph nobody in this loop can take. `glass_ws` is a real mesh at the exact
pane transform, so the board can be stood in the windscreen and rendered without anyone flying to
Manhattan. ⚠ **The body's own withdrawal is right and I am carrying it: "the width of a windscreen" is
a tape-measurable number and the model's contribution there is ZERO.**
**FIRST STEP:** ~2 hours plus ~10 minutes of render — set the five lines as flat artwork at 560.0 ×
352.0, add `ws_board()` built off `_ws()`'s own basis, render. **Nothing blocks it.**

**3 · GRACIAS POR SU PREFERENCIA (1524.7)** — a 16 s locked-camera loop through the middle serving
aperture, machine half drawn as vector line, hand half drawn on twos; plus a 24-page flipbook.
**LINE: adult (declared).**
**FIGURES:** aperture **515.5 × 403.0, r 55, three, equal** (`BAY_W` 0.5155, `Z_SILL/Z_HEAD`
1.3720/1.7750, `BAY_R` 0.0550, `BAY_CX` 0.6720/0.0470/−0.5980 — all read this session). Menu yellow
**(172, 144, 17)**; strip ink **(72, 46, 6)**, **AUTHORED from a measured median (91, 59, 7)**.
**RISK IT STILL CARRIES:** one flat skin ink for staff and customer alike — which reads either as the
film's argument or as erasing the difference the brand trades on, **and the body does not resolve it;
it says so and puts it to the owner in those words.**
**MODEL:** it wrote the shot and **refuted the first draft of it** — `van_floor`'s top at the middle
bay is 511.2 mm AG against an aperture head at 1726.2 mm, so the head rail is **1215.0 mm above the
floor the cook stands on** and a standing adult's eye is above it. *"A camera at the cook's eye
looking out"* is impossible on this vehicle. **That is the strongest single model contribution in the
round and nothing but the mesh could have produced it.**
**FIRST STEP:** one A4 card, two sides — frame one at 1:4 of the true aperture, with the sight-line
section on the back. ⚠ **BLOCKED on three absent things and the body names all three: the AO pass, any
human geometry (229 mesh objects, no torso, arm or hand), and an illustrator.**

**4 · CALENDARIO AÑO XXII «YA VIENE»** — 480 × 680 mm header board, 12-leaf tear-off block, one ink,
the measured body red **(196, 49, 36)**. **LINE: adult `[ASSIGNED]`.**
⚠⚠ **THIS IS ALREADY SHIPPED — `design_out/calendario_ano_xxii.svg` and `.png`, and `calendario.py`
runs `14 checked, 0 FAILED` at 480 × 680 mm. DO NOT COMMISSION IT AS NEW WORK.** Re-run this session:
`scale 1 : 18.0`, `registration: drawn 4.5800 × 3.1316 m against STATE 4.5800 × 3.1320 (+0.0 / −0.4
mm)`, and **149 glyph strokes SUPPRESSED with plain discs drawn** because the mark would have printed
at 4.83 mm — the object declining to print an emblem below the size at which it can be judged, which
is the right call and is F191-consistent.
**RISK IT STILL CARRIES:** the **AÑO XXIII painted year** — the *chica de calendario* register — is
the live one and is **not** shipped; the body keeps it deliberately against two auditors' advice, with
a stated failure state. **And its colophon prints an unstable count without a spread (§5.0b item 3),
which is a one-line fix on a shipped file.**
**MODEL:** every line on the sheet. There is no photograph of this vehicle in true side orthographic
projection and there cannot be — **a true elevation can only be projected.**
**FIRST STEP:** print the shipped SVG at A3 on an office printer and put it in his hands. **Then fix
the colophon.**

**5 · EL TROQUEL — el lado ciego** — a Ø300 mm hand-carved end-grain **die** (not a medal), two faces:
obverse the show flank, reverse the **off flank that has never been photographed**, struck at the same
fidelity, with the only key on the rim. Plus a Ø55 chocolate from the OPEN pose. **LINE: adult
(declared).**
**FIGURES:** aperture 515.5 × 403.0 r55 → **30.68 × 23.99 mm at Ø300**; tyre 664.9 → 39.58; hubcap
274.0 → 16.31; badge 86.9 → 5.17 **(deleted)**; a 5.5 mm shut line → **0.327 mm at Ø300 against
0.058 mm at Ø55**, which is narrower than a fine ball-nose tool and is the arithmetic that sets the
size. `SPEC.md:138` grades the −Y flank **E (never photographed)** with two contradicting features.
**RISK IT STILL CARRIES:** it **strikes a grade-E inference in permanent material**, which is a
declared departure from *"any single measurement off is unacceptable"*; and the badges are **deleted**
from the height field, which is legally necessary on a permanent tool and visually violent.
**MODEL:** the only thing on the bench that needs a **solid**. A relief needs single-valued depth; a
photograph has none, and photogrammetry gives noise a router reproduces faithfully. **And only a model
has a blind side that can be asked to show itself.**
**FIRST STEP:** three one-line changes — `use_pass_z` on the existing `side` camera, a `side_off` view
at `loc=(0.0, −26.0, 1.52)`, and a collection exclude for `capvw`/`vw_disc`/`vw_ring`. ⚠ **`use_pass_z`
does not exist in this tree (§5.0b item 4), so this is a real if small capability job, not a flag.**

**6 · MANDIL 515 · EL HUECO** — a cross-back cook's apron with the forward serving bay **cut out of
the chest** at 1:1, bound in body red twill tape. Ships as a **1:1 cutting pattern first**, 1000 ×
1700 mm. **LINE: adult (declared).**
**FIGURES:** `bay_outline(0)` is a **live callable** returning `T.rrect(x1−x0, Z_HEAD−Z_SILL, BAY_R,
seg=8)`, so the pattern is generated, not drawn. Station **x = +0.6720 m** and never an ordinal —
`SURVEY_rev49_photoreal.md` indexes these holes both ways. `RED` (196,49,36), `CREAM` (206,208,200),
both live in `t1_mats.py`. **`probe_rev39_flank.py`: `MAN_ROWS, MAN_COLS = (420, 768), (90, 300)`** —
210 × 348 px on a 1024 × 768 frame, **9.29 %**, in an instrument whose job is to delete a man so a
flank can be scored.
**RISK IT STILL CARRIES:** **a hole in a cook's apron is a real safety reduction** and every maker will
refuse it; **cotton drill shrinks 1–3 % (an industry range, NOT measured on this cloth)** so the
aperture closes over the garment's washed life — paper carries 0.1 mm, cloth carries ±5 mm, and both
go on the pattern; and *"you are the hatch"* is on the chest of someone earning an hourly wage.
**MODEL:** **the aperture is the only shape in this record that belongs to the owner.** Volkswagen made
the van; Tacombi cut the holes. **Zero trade-dress exposure, which no other permanent object here can
say.**
**FIRST STEP:** `mandil.py` → `design_out/mandil_515_patron.svg` on `sheet.py`, which is committed and
mm-native. **An afternoon. Nothing blocks it.**

**7 · CIENTO DIECIOCHO Y UNA / APAGA LA LUZ** — a **die-cut glow-vinyl sticker**, 200 mm long
(1:20.325), printed digitally onto glow stock with the night image **knocked out to bare substrate**,
contour-cut on a plotter. **LINE: children (declared, both bodies).** **These are two independent
amplifications of one parent and they converge — see §5.0.**
**FIGURES:** **the one-emitter fact, which is the concept.** `grep -c "emit=("` over the four geometry
modules returns **0 / 0 / 1 / 0** — recomputed this session. The single hit is the galley work strip,
`emit=(1.000, 0.918, 0.790)` at `GAL_LUM 3.04`. **118 lamps at 28.5197 mm** (§5.0b item 1), and
`t1_detail.py`'s own comment says they are *"rendered as unlit pearl glass: this project has no
emissive material."* **The model has believed this object's proposition for 77 revisions: the party
lights are dark and the work light is on.**
**RISK IT STILL CARRIES:** the artefact's climax is a **closure** — strontium aluminate decays, so the
festoon goes out while the child watches and only the sun reopens it; the **daylight silhouette is a
panel van**, the vehicle before or after the conversion; and **the kitchen is lit and empty.** Both
bodies **ban the word "asleep"** and say why. ⚠ **The two disagree on one point and it is not
resolved: whether the 118 lamps glow at all, or are left in daylight ink so they visibly do not.**
**MODEL:** no photograph shows the galley from outside and none can — the flank is opaque steel. The
`side` orthographic camera can suppress it and draw the room behind.
**FIRST STEP:** ~$0. One A4 sheet of glow vinyl, a 40 mm strip, one third bare / one third at ~55 %
halftone / one third solid ink, charged and watched in the dark. **That tests the extinction ORDER,
which is the bet. If the order does not appear the concept dies on a scrap of vinyl.**

**8 · MARCA DEL COCINERO** *(was EL FIERRO)* — a **branding die issued to a person, not a store**,
whose face is the three serving apertures on two equal pillars with the counter's top edge as the
bottom rule, and the holder's chosen name beneath. **LINE: adult `[ASSIGNED]`.**
**FIGURES:** paper face at 1:20 — drawn field 89.28 × 26.05 mm, each aperture 25.77 × 20.15 mm r 2.75,
pillars 5.98 mm, **768 mm² of contact against the parent's ~3,700 mm² solid van face.**
**RISK IT STILL CARRIES, AND IT IS THE SHARPEST ON THE BENCH:** **a line cook's name goes on a
stranger's food**, which in 2026 is harassment exposure and for some workers immigration exposure.
**The body puts the question to the COOKS, not to the owner, and says that if they decline the concept
is dead and the refusal is the finding.** It also states, in the first person, that a *fierro* is a
livestock mark and that the same technology burned owners' marks into human faces in New Spain.
**MODEL:** three measurements changed the object rather than captioning it — pillars equalised, counter
nosing deleted, scale moved. ⚠ **The body RETRACTS its own parent's headline claim** — that an accurate
silhouette beats a caricature at 90 mm — as refuted by its own arithmetic. **Carry the retraction.**
**FIRST STEP:** one A4 sheet at 1200 dpi, a 4 × 3 grid of face-at-three-scales against simulated char
bleed 0.0/0.4/0.8/1.2 mm, every stroke morphologically dilated. **He looks at where the 5.98 mm
pillars fatten shut.**

**9 · NO SE VENDE** — a 250 ml jar of house escabeche carrying one **hand-painted band, ~90 × 42 mm,
of the −Y flank**, freehand in one-shot enamel by a named rotulista over a pounce transfer from the
model's own line pass. Two hundred jars, every one different. **LINE: adult (declared).**
**FIGURES:** `SPEC.md:138` — the off side is **grade E, never photographed**, and its two recorded
features contradict each other. `STATE.md` carries the flank at **804.9 mm of shut-line crossing
against 0.0 mm on the show side**, and the row's own words say that means **it has not moved**, not
that it is right. Shown the sightlines, the owner said ***"cannot tell from this crop."***
**RISK IT STILL CARRIES:** the cook is named on a permanent object — the same immigration and
retaliation exposure as item 8, with a written consent in her own language and a per-unit fee, and if
she declines **the jar prints the absence**; and **$28 for pickles that are free in the caddy** is
$112/litre on glass that says NO SE VENDE.
**MODEL:** the −Y elevation cannot be photographed, cannot be scanned, is not in the reference set, and
**is not yet drawn either — `studio.py` has no −Y camera.** That is the difference between pointing a
camera and supplying a surface.
**FIRST STEP:** one dict entry mirroring `side` at `loc=(0.0, −26.0, 1.52)`, `ortho=5.90`, plus a
**$0 phone call to NYC DOHMH** about refilling customer-owned glass, which is the only item with a
week of latency. ⚠ **The body's own struck sentence is worth keeping struck: on this side there is
nothing to correct the painter against.**

**10 · TACOS Y** — a 450 × 450 mm hand-embroidered **servilleta** carrying the bus's own **right menu
strip** at 1:1 of a 450 mm board height. **LINE: adult `[ASSIGNED]` — $58–68 hand / $32 machine
(ESTIMATE, not quoted).**
**FIGURES:** every v-run read live out of `lid_gen.py`; a 59 mm yellow band **(172,144,17)** carrying
dark ink **(72,46,6)**. ⚠ **A sequence along one axis carries NO aspect, so the board's ±0.09
uncertainty touches only the band's width — 56.8 / 59.1 / 60.8 mm across the CI. That is why this
object survives the pose problem that wrecks every square composition off the same board.**
**RISK IT STILL CARRIES:** **three lines the record cannot read are written by the taller in their own
words, and nobody approves the copy** — a real, permanent loss of brand control on a retail object.
**MODEL:** the mural survives in one oblique photograph; copy it by eye and you copy a trapezoid. The
rectification is the model's. ⚠ **CEILING: the rectification's ANGLE is a pose (`LID_OPEN_DEG`,
bracketed 68.9–90°) and it moves the board's aspect.** **Never print 1223.7 mm as a true width.**
**FIRST STEP:** `servilleta_gen.py` importing the sequence and palette from `lid_gen.py` — never
retyped — through the same `save_svg` path `la_rueda.py` uses. **~1 day, ~$15.**

**11 · MEDIA VENTANA (HUECO No. 2, 1:2)** — a two-block hand-cut relief print that **is** serving
aperture No. 2 at 1:2, trim 257.75 × 201.50 mm r 27.50, **cut out of square** because the aperture is
sheared. **LINE: adult `[ASSIGNED]` — its captions are pixel residuals.**
**FIGURES:** the view flips **outward** — 7296 rays cast through the raked opening returned sixteen
named objects, the dominant graphic fact being **a ring of 64 bobbles at 25.94 mm realised pitch**
that nobody had looked at square-on in 77 revisions. **The counter is NOT on the sheet**: `CNT_ZT` sits
**118.0 mm** below the sill, i.e. 59.0 mm below the lower edge at 1:2.
**RISK IT STILL CARRIES:** **a named worker is fully modelled and the customer is a hole**, and both
readings — the room's hierarchy, or the restaurant telling customers they are nobody — are available
and neither is defused.
**MODEL:** a true elevation, which no photograph can give; and the rake, which is invisible in every
photograph.
**FIRST STEP:** ⚠ **BLOCKED. Its own first step is "land the AO pass properly", which does not exist.**
Everything else in the concept is downstream of that.

**12 · A LA ALTURA · 118** — a fabricated **camera jig**: a 900 × 700 mm frame whose aperture is cut as
the **ground-frame parallelogram**, a 321 mm counter return with 19.9 mm of brass, and **two machined
118.0 mm spacers** between them. Output is matched pairs, one person, 11:00 and 23:00. **LINE: adult
(declared).**
**FIGURES, AND THE FINDING IS THE FIGURE:** `build.py` step 8b is a **shear in x**, not a lift, so the
aperture is a rectangle in the body frame and a **parallelogram relative to ground** — fall across its
own width **9.150 mm**, interior angles **91.017° / 88.983°**, **recomputed here and both reproduce**.
**And `Z_SILL − CNT_ZT` = 118.0 mm is RAKE-INVARIANT**, because step 8b subtracts the same drop from
both at any shared station. **Every aperture object in the pool cut the rectangle. The rectangle is
the thing that is not true.**
**RISK IT STILL CARRIES:** **printing a named line cook's shift interval on a saleable object is a
labour statement** and will be read as one; **the subject's veto is real and will lose frames**; and
⚠ **the shear may simply be invisible — 1.017° has never been looked at at 1:1 by anyone.**
**MODEL:** two facts nothing else holds — the shear (a tape rakes with the bus and reads a rectangle;
rule 43 forbids recovering it from a photograph) and the invariance. ⚠ **The body WITHDRAWS its
parent's "the model is the cutting file" as inflated, correctly: eight numbers, seven of them
tape-measurable.**
**FIRST STEP:** **~40 lines with no `bpy` import**, four sheared arcs and four lines from four
constants already in the tree. **This is the cheapest first step on the whole bench — see §5.5.**

**13 · MOTOR: NINGUNO — SILBATO 1:20** — a two-shell moulded **whistle**, 200.00 × 87.49 × 83.57 mm,
every opening moulded shut except the three serving apertures (the fingering) and the **engine-bay
louvres** (the voicing window, always open). **LINE: children (declared).**
**FIGURES:** the intervals above the first fingered note are **+490.5 and +801.7 cents** — a fourth and
a minor sixth — and **they are volume-free**: wall swept 1.0 → 4.0 mm moves them only to 484.6→499.5
and 793.5→814.3. **The chord survives; the key does not.** `LOUV_APERTURE = 0.0070` and
`LOUV_PITCH = 0.021111` confirmed in source this session.
**RISK IT STILL CARRIES:** ⚠ **`LOUV_APERTURE` is the softest number in the object and its own source
line says so — `# INFERRED, not measured -- 1.5 px`. The whole tuning stands on it, and while the
triad holds under sweep, the drone's interval swings 1073 → 1480 cents.** Plus: **a 200 mm 3-D T1 body
is the most trade-dress-exposed object the programme could make**, and the body **deletes** its
parent's moulded disclaimer as an admission rather than a shield. And **two hundred children with
whistles is a dining room nobody wants to sit in** — put back deliberately, with the measured level
owed.
**MODEL:** total, and uniquely so — a whistle's shape is its transfer function. ⚠ **The body
DISCHARGES its own stated blocker and retracts the overstatement (rule 13): `bpy.ops.wm.stl_export`
exists and wrote 132,638 triangles in 17.58 ms. It was one call, not "half a day of code".**
**FIRST STEP:** print two halves on any FDM machine and blow it. **~$40.** ⚠ **No Helmholtz
calculation predicts whether a fipple SPEAKS — only what it speaks at if it does.**

**14 · RUIDO** — **six 280 × 430 mm tray liners on 40 gsm greaseproof**, one ink each, drawn from the
archive's own people; **four printed (staff, released, paid), two never printed and never sold.**
**LINE: adult (declared, with the tension declared with it — F331's option text pairs "free/handed-to-
you" with children, and this is free and handed to you; the SUBJECT decides the line, not the
free/kept axis).**
**FIGURES:** the drawing rule is a resolution ceiling — `EL DE LA COMANDA` face **~55 × 70 px**, the
best-resolved human we hold; `LA NIÑA` head **100 × 121 px**; `EL COCINERO` ~35 px in profile. **Each
sheet carries exactly as much information as its source and not one mark more.**
**RISK IT STILL CARRIES:** distribution goes **up**, not down — tens of thousands of sheets a year;
the photographers are **unnamed and unlicensed anywhere in this repository**; and ⚠ **whether any of
these people still work there, or can be found at all, CANNOT BE RECOVERED FROM WHAT WE HOLD** — every
consent remedy in all four audits assumes findability and nothing supports it. **That gates the set.**
**MODEL:** ⚠ **the model contributes ONE constant and the body says so.** In a programme where eleven of
eleven concepts deleted the people, this one deletes the vehicle. **That asymmetry is the concept, and
it is also why this object cannot carry the programme's model-led argument.**
**FIRST STEP:** one sheet, `EL COCINERO`, ~20 sheets under **$200** — then **ask him** *"these are your
people. Which of them may we draw?"* as multiple choice. **The ruling gates everything downstream.**

**15 · PROVECHO** — **NOT CARRIED FORWARD.** Screened **8.73, first of all 75**; audits **1.50/4, last
of the fourteen**, `dangerIntact` false. **It is the single clearest instance of F338 and it is kept
visible here rather than dropped (rule 16).** ⚠ **This is not a claim the object is bad — it is a
claim that the screen's ordering carries no information about it.** If a future context wants it, it
needs re-auditing from scratch, not promoting on 8.73.

---
### §5.2 WHAT SHOULD BE BUILT FIRST — **THE DIE-CUT STICKER, AND SPECIFICALLY ITS DAYLIGHT FACE**

**F18 is the register's oldest live row (rev 44), it is the project's original deliverable, and the
owner fired its trigger at rev 77: *"YES — START IT NOW."* (F330.) Nothing on this bench outranks a
fired trigger on the original deliverable.** The three preconditions now line up and they did not
before:

1. **The line pass EXISTS** (F332) and takes `--view` through `studio.views()`, so a new viewpoint is
   one dict entry in a table that already holds thirteen.
2. **The occlusion half DOES NOT EXIST** (§5.0b item 4, confirmed by grep). **So build the half that
   is buildable and say which half it is.** The sticker's daylight face is **line and flat colour** —
   exactly the half F332 delivered. ⚠ **This is why `MI COMBI` (§2 #15) is NOT the first job despite
   being the sticker by name: its sixth ink IS the occlusion pass, so it is blocked on a capability
   nobody has built.**
3. **The spec is written, and it is written for THIS object** — 8 `sticker` rows in `AUDIT_rev43.md`
   with the DESIGN column intact: the viewpoint, the cab-door owner question, the triptych layout,
   the sacrifice rule (*"48 of the flank's 66 gold components carry 2.29 % of the ink and every one
   lands under 0.40 mm — delete all 48"*), the die-cut outline, the line-weight floor, the sun, and
   the colour separation.

**AND IT DISCHARGES §5.3 IN THE SAME EDIT.** Items 7 and 13 are the only two children's-line objects
on the bench, and item 7 **is** the die-cut sticker. **One build satisfies F330 and starts F331's
owed half.**

⚠ **THREE THINGS THAT MUST BE SETTLED BEFORE A LINE IS DRAWN, AND NONE IS EXPENSIVE.**
* **THE VIEWPOINT.** No camera matches the spec's 18° (§5.0b item 5) and **I cannot tell from the
  truncated row which convention it uses.** `low34` matches the 1.55 m eye height exactly at 34.0°.
  **Render both readings, paint them, and look — or ask him. Do not pick silently.**
* **THE CAB DOOR.** `AUDIT_rev43.md` row 2 is an explicit **OWNER QUESTION, MULTIPLE CHOICE** and it
  has never been asked. Open at 49° opens a 0.306 m void that only a PERSON fills in the reference,
  against a locked scene of *"nothing but the bus"*.
* **F330's CEILING TRAVELS WITH IT.** He was asked whether the **MODEL** is done enough, **not whether
  the EMBLEM is.** F191 and F234 stand. ⚠ **The shipped `calendario.py` shows the right reflex under
  that ceiling: it SUPPRESSED 149 glyph strokes and drew plain discs rather than print a mark at
  4.83 mm. The sticker should do the same unless a painted A/B at sticker scale says otherwise —
  and F333 (the badge traces cleanly in line) is ONE object at ONE scale in ONE view and is not
  permission.**

**SECOND, AND ONLY BECAUSE IT IS FREE: `DIRECTO` (item 2).** It is the audit's joint-first with danger
intact, it is blocked on **nothing**, and its first step is ~2 hours plus a 10-minute render. **It is
the only top-ranked item with no absent capability under it.**

---
### §5.3 THE CHILDREN'S LINE — **F331 MAKES IT HALF THE PROGRAMME AND TWO OBJECTS EXIST**

**F331 is binding: *"kids get one line, adults another."* Half the programme is owed and almost none
of it has been made.** Counted off the fifteen amplified bodies: **3 declare children (items 7 × 2 and
13), 6 declare adult, and 6 declare nothing.** Against the whole round, `THE CHILD'S EYE` slot holds
three concepts — **one register out of thirteen.**

**WHAT EXISTS AND SHOULD BE BUILT:**
* **THE GLOW STICKER (item 7).** Two independent amplifications converged on it; it needs **no absent
  capability**; its first step is a strip of vinyl and an evening; and **it is F18**. Build it.
* **THE WHISTLE (item 13).** Genuinely a children's object, `dangerIntact` **true**, and its
  export blocker is discharged. ⚠ **But it is the programme's worst trade-dress exposure and it should
  not be tooled before the IP page (§5.4).** A $40 FDM prototype needs no advice; a $6,000 tool does.

**WHAT IS MISSING, AND IT IS MOST OF THE LINE:**
* **NOTHING A CHILD READS.** The picture book the first critic named as *"the only children's object
  anyone keeps for twenty years"* is in the pool and is not in the shortlist.
* **NOTHING A CHILD DOES.** No drawing, colouring, cutting, building or collecting object survived to
  the finalists. `ARMA TU COMBI` and `DALE` exist in the bench and were not audited.
* **NO CHILD-LEGIBLE REGISTER EXISTS AT ALL.** Every shipped artefact — Sheet 3, La Rueda, the
  Calendario — is in the **deadpan-catalogue** register F331 confirms for the **adult** half.
  **The children's half has no typography, no palette, no tone and no worked example.** ⚠ **That is
  the real gap: not a missing object, a missing register.** The whistle's underside prints σ values
  and the glow sticker's backing card is explicitly figure-free — **two bodies, opposite decisions,
  no rule.** **Write the rule with the first object, and put it in a file, not a paragraph.**
* **AND ONE HONEST CONSTRAINT:** F331's own option text pairs *"free / handed across the counter"*
  with children. **`RUIDO` is free and handed across the counter and is emphatically adult.** The
  free/kept axis does not determine the line. **The SUBJECT does. Say so in the rule.**

---
### §5.4 WHAT THIS ROUND DID NOT FIX — **EXTENDS §4 ABOVE, DOES NOT REPLACE IT**

§4's seven items stand unchanged. These are additional and were found by measuring this round rather
than reading it.

1. **THE GARMENT SLOT IS THE ROUND'S ONE REAL NEGATIVE RESULT AND THE EVIDENCE UNDER IT IS WEAK.**
   It screened **best 5.07, mean 4.58 (5.07 / 4.67 / 4.00)** — **both the lowest best and the lowest
   mean of all 25 slots** — and it is the slot the rev-76 critic called *"the only genuinely premium
   object in the whole document"*. ⚠⚠ **BUT THAT IS ONE DIRECTOR'S THREE ATTEMPTS, NOT THREE
   DIRECTORS' — the round ran 25 directors at three concepts each, so a slot IS a director. A negative
   result over three tries by one person is far weaker than over three independent ones. THE RANKING
   SURVIVES; THE EVIDENTIAL WEIGHT DOES NOT.** ⚠ **AND THE SLOT IS SELF-REFUTING AS IT STANDS:
   `MANDIL 515` came out of it, audits 1.88 — joint fourth of fourteen — and is blocked on nothing.
   Re-run the slot with three directors before concluding the register is barren.**
2. **NO CONCEPT HAS BEEN THROUGH THE FULL CHAIN, AND THE AMPLIFICATIONS WERE NOT RE-AUDITED.**
   8 of 15 bodies carry `audit n/a` (§5.0). **Every ranking in §5.1 inherits that.**
3. **NOTHING HAS BEEN SHOWN TO THE OWNER.** Unchanged from §4 and still the largest single gap.
4. **THE IP PAGE IS STILL NOT DONE.** Both completeness critics led with it; it is unperformed across
   the whole programme; and this round added the worst case (item 13, a 200 mm 3-D T1 body).
   **It is cheaper than one enamel die and it gates every permanent object here.**
5. **NO COST, PRICE, MOQ OR LEAD TIME EXISTS FOR ANY OBJECT.** Critic 1's finding, unanswered. Every
   figure in §5.5 below is an **ESTIMATE** and is labelled one. **Nothing in 78 revisions of this
   repository has ever been priced.**
6. **THE OCCLUSION HALF OF THE OWNER'S OWN LOCKED STYLE SENTENCE IS NOT BUILT** — no AO, normal or
   depth pass (§5.0b item 4). **It blocks items 1, 3, 5 and 11 outright**, which is four of the top
   eleven, and it is the single highest-leverage capability job on the bench.
7. **THE LINE PASS'S COUNTS ARE NOT REPRODUCIBLE AND A SHIPPED ARTEFACT PRINTS ONE** (§5.0b items
   2–3). **A register row is owed; next free ID F341.**
8. **F331 COMPLIANCE FAILED INSIDE THE ROUND THAT RECORDED IT** — 6 of 15 bodies declare no line.
9. **THE EMBLEM IS NOT ADVANCED.** Unchanged. **0.8528 against P1b's 0.9465, no legibility term
   (rule 56), nine owner reports.** ⚠ **Two objects here decline to print it below judgeable size —
   `calendario.py` suppresses 149 glyph strokes, `EL TROQUEL` deletes the badges from its height
   field. That is the correct reflex and it is not progress on the emblem.**

---
### §5.5 THE THREE CHEAPEST THINGS HE COULD SEE FIRST

**Ordered by COST, which is not the build order in §5.2 — and that is not a contradiction: §5.2 orders
by what the owner has RULED, and he outranks the ranking. These are what could be in front of him
soonest if cost is the only question.** ⚠ **Every estimate below is machine time plus consumables. No
object in this repository has ever been quoted, and a trade estimate is not a quote (§5.4 item 5).**

**1 · THE SHEARED APERTURE AT 1:1, ON PAPER — ~1 hour, $0 plus a few sheets of A4.**
From item 12. **~40 lines with no `bpy` import**: four sheared arcs and four lines out of `BAY_W`
0.5155, `Z_HEAD − Z_SILL` 0.4030, `BAY_R` 0.0550 and `RAKE_DZDX` 0.017750. Emit an A2 sheet with the
parallelogram over the nominal rectangle in a second ink, the **9.150 mm** fall dimensioned, and the
two **118.0 mm** spacers drawn beneath the sill. Tile to A4, tape it up, hang it in a doorway with a
plumb bob, take one phone photograph. **Then ask him one multiple-choice question with option (c)
"no — it looks level to me" on it.** ⚠ **(c) kills the concept for an hour and a sheet of paper, and
that is the correct outcome if the differentiator is invisible.** **No render, no Blender, no bus, no
staff, no permission.** It is the cheapest honest test on the bench because **it tests the thing that
is actually in doubt** rather than whether he likes a drawing.

**2 · THE 1:1 APRON PATTERN SHEET — an afternoon, ~$10–20 at a plan-copy shop (ESTIMATE).**
From item 6. `mandil.py` calls `bay_outline(0)` — **a live callable, so the pattern is generated, not
drawn** — translates it by `bay_centre(0)` and emits into `sheet.Sheet(1000, 1700)` through the
committed, mm-native `sheet.py`. Two inks, 10 mm seam allowance, grain arrow, four balance notches,
and **a 100 mm calibration bar so any printer's scaling error is caught by a steel rule before cloth
is cut.** Beside it at the same 1:1, the **993 × 1645 mm** deletion rectangle from
`probe_rev39_flank.py`. ⚠ **That rectangle is an UPPER BOUND — the subject stands nearer the camera
than the scale plane — and must never be printed as a man's height.** He holds it against his own
chest and answers whether a 515 × 403 hole reads as a hatch or as a bib pocket. **Title block carries
the station `x = +0.6720 m` and never an ordinal.**

**3 · THE STICKER'S DAYLIGHT FACE AT 200 mm — ~1 day of machine time, $0 to print at home.**
From items 7 and §5.2, **and this is the one he asked for.** One new dict entry in `studio.views()`
for the spec's viewpoint (**render both conventions and look — §5.0b item 5**), one line pass at
**~26 s**, the die-cut path off the stroke cloud, three inks, the `SEÑOR TACOMBI` script in F157's
owner-ruled bright silver, **blank wheel discs**, and the 118 lamps at their realised 28.5197 mm.
Print on paper, cut it with a scalpel, and put it on the fridge. ⚠ **State on the sheet that this is
the LINE half only and that the occlusion half is unbuilt** — the owner's style sentence has two
clauses and this delivers one. **Add the glow-vinyl strip test from item 7's first step in the same
week; it costs an evening and one A4 sheet, and it decides whether the children's object is a
sticker or something else.**

**AND ONE THING THAT IS NOT AN ARTEFACT AND SHOULD RUN BESIDE ALL THREE:** ⚠ **the one page of IP
advice.** It is unperformed, both critics led with it, and it gates every permanent object in §5.1.
**It is cheaper than one tool and it is the only item here whose absence can stop the programme
rather than slow it.**

---
## §2 THE TWO LATE COMPLETENESS CRITICS, VERBATIM

**Neither was given the other's report.** Critic 3 was asked whether the synthesis obeyed its
instructions — rank on the audit, declare every item's LINE, address the children's line, avoid the
retracted pillar figure, state ceilings. Critic 4 was asked only two things: whether the
amplification sanded off the danger, and whether any of it is worth a customer's money.

### LATE CRITIC 1 — verdict

> TWO ANSWERS, BLUNTLY.
> 
> DID THE AMPLIFICATION SAND OFF THE DANGER? MIXED, AND THE FAILURES GO BOTH WAYS. Four of fifteen carry cosmetic danger and I name them: CALENDARIO ANO XXII (the shipped object carries NONE of its stated risk — every named danger belongs to ANO XXIII, which is not shipped; a risk section about a different object is the fourth lens's purest failure case), CIENTO DIECIOCHO Y UNA / APAGA LA LUZ (phosphor decay reframed as an emotional edge — that is what glow vinyl does, and manufacturing danger is the same dishonesty as sanding it, pointed the other way), MEDIA VENTANA (an interpretive ambiguity in a lino print is not a risk), and EL TROQUEL (GRADO E incuse on a rim is a confession relocated, not a danger). But the more serious problem is the opposite one: where the danger IS real it is real enough to be a kill decision, and §5.1 ranks it instead. MARCA DEL COCINERO and NO SE VENDE both put a named, plausibly undocumented worker's identity on a product sold to strangers and call an employer's ask "consent". RUIDO rests on photographers who are unlicensed anywhere in this repository and subjects whose findability its own body admits cannot be recovered from what we hold. Holding a live risk is a virtue; publishing one that can get a line cook deported is not nerve, it is negligence with good copy.
> 
> AS THE CREATIVE DIRECTOR WITH THE BUDGET. BEST BY NAME: CIENTO DIECIOCHO Y UNA / APAGA LA LUZ — zero tooling, MOQ 10, an evening's test, the impulse band, kept for years, discharges the fired trigger and opens the owed children's line in one build, and its spine (one emissive material in the whole vehicle: the party lights dark, the work light on) is the single best idea produced by all seventy-five concepts because it is true of the asset before it is true of the story. Two directors found it independently. WORST BY NAME: MARCA DEL COCINERO. Art school, cull in one pass: MEDIA VENTANA, A LA ALTURA · 118, EL TROQUEL, RUIDO, GRACIAS POR SU PREFERENCIA.
> 
> IS ANY OF IT BEAUTIFUL? One thing, and you have buried it. The side-elevation drawing on the shipped calendario is confident and alive and it is the only beautiful object this programme has made — and directly under it you have printed twenty-one rows of NO EMITIDO on a free gift, in more area than the date grid, which is at the smallest type on the sheet. That is a company telling its customers it has failed twenty-one times, on a calendar that cannot be used as a calendar. Critic 1's diagnosis reproduces exactly and you have not engaged with it: this programme only becomes beautiful at the moment it stops measuring, and it keeps treating that as a confession rather than as the finding.
> 
> AND THE OBVIOUS COMMERCIAL OBJECT YOU STILL DO NOT HAVE: all of them. No menu. No t-shirt, cap or tote. No gift card. No delivery bag or seal — your largest unbranded surface, opened at home by someone who has never seen the room. No shelf-ready retail pack. Critic 1 listed those seven by name and §5.4 lists nine gaps without one of them, while the kraft bag that would have closed the delivery surface was cut in an undocumented selection step. Which brings me to the finding that undermines the section's whole ranking: the fourteen audited concepts are NOT the screen's top fourteen. Seven of the screen's top sixteen were never audited at all, including the #2 at 8.70 and DIEZ FLORES Y MEDIA — the hule oilcloth Critic 1 named in capitals as the single best idea in the pool — while RUIDO at 5.53 was pulled in. §5.0's ceiling (a) asserts the opposite. You have ranked on the audit, correctly, on a hand-picked set, and the three most commercial and most beautiful objects in seventy-five fell through the gap without anyone writing down that they had.

**[TOP] THE FOURTEEN AUDITED ARE NOT THE SCREEN'S TOP FOURTEEN, AND §5.0's CEILING (a) STATES THE OPPOSITE. Ranking on the audit therefore deletes seven objects that never got an audit score at all — including the screen's #2 and the previous critic's single named best idea.**

* evidence: §2's top-16 vs `CONCEPT_AUDIT_rev77.md` §1's table, both counted this session. NEVER AUDITED, though inside the screen's top 16: LA TAPA (8.70, #2), EL DIA QUE LE CORTARON EL TECHO (8.50), DALE (8.40), CINCO ANTOJITOS (8.27), DIEZ FLORES Y MEDIA (8.20), GUIRNALDA (8.03), MI COMBI (8.00). AUDITED though far below it: SILBATO (7.60), GRACIAS (7.33), MANDIL 515 (7.17), 515.5x403 (7.07), RUIDO (5.53). The audit reached down to 5.53 while skipping 8.70. §5.0 says 'the 14 were selected BY the screen, so r is computed on the screen's own top fifth' — it is not; it is a hand-picked set of 14. DIEZ FLORES Y MEDIA is the hule oilcloth Critic 1 named in capitals as 'THE SINGLE BEST IDEA IN THE POOL', and it is absent from §5.1 entirely. So are the kraft bag and the lampshade. That is THREE of the six objects Critic 1 called beautiful before clever, deleted by a selection step nobody documented.
* remedy: State the real selection rule for the 14 and who applied it. Then either audit LA TAPA, DIEZ FLORES Y MEDIA, the kraft bag and MI COMBI, or say plainly in §5.1 that seven top-screen objects are excluded for want of an audit score and are NOT ranked below the fifteen. Recompute r naming the true selection. Until then no 'ranked shortlist' claim is safe.

**[TOP] THE COMMERCIAL GAP CRITIC 1 NAMED IS 100 % OPEN AND §5.4 DOES NOT LIST IT. You have fifteen objects and a taqueria still cannot buy a t-shirt, a cap, a tote, a gift card, a menu, a delivery bag or a shelf-ready retail pack from any of them.**

* evidence: Critic 1, verbatim: 'WHAT A TAQUERIA NEEDS THAT IS NOT IN THIS POOL: a gift card and its carrier; a t-shirt, a cap and a tote; THE MENU; a shelf-ready retail food pack with a barcode; and the delivery seal plus the bag someone opens at home having never seen the room — your largest unbranded surface.' Scanned §5.1's fifteen rows: not one of those seven. §5.4 lists nine gaps and this is not among them, so the round's loudest commercial finding was received and dropped. Meanwhile the kraft bag ([dream:la-combi-cerrada-2]) — one of the two objects that WOULD have closed the delivery surface, and on Critic 1's own buy list — was cut in the same selection step as finding 1. Only two of fifteen sit in the $4-25 impulse band where counter merchandise actually sells.
* remedy: Add a tenth row to §5.4 naming all seven by name so the next context inherits them. Then put ONE of them on the bench for real: the delivery bag and seal, because it is the highest-volume unbranded surface the business owns, it is cheap, it needs no capability that does not exist, and the kraft-bag concept is already written and sitting in the carrier.

**[TOP] §5.2 PUTS THE PROGRAMME'S MAXIMUM TRADE-DRESS OBJECT FIRST AND GATES IT ON NOTHING. A vinyl sticker contour-cut to the T1 silhouette is the shape sold AS the shape — precisely the exposure Critic 1 led with, and precisely the class §5.4 item 4 says is unadvised.**

* evidence: Critic 1's top finding: 'THE ENTIRE MERCHANDISE PROGRAMME IS BUILT ON A THIRD PARTY'S TRADE DRESS AND NOBODY HAS CHECKED ... three-dimensional metal objects cut to the profile — that is trade dress, not fair-use depiction.' A die-cut sticker is a two-dimensional object cut to the profile; the cut path IS the mark. §5.2's three preconditions are the line pass, the occlusion pass and the spec. IP is not one of them, and §5.2 never references §5.4 item 4. §5.4 item 4 itself says the IP page 'gates every permanent object here' and then §5.2 ships an un-gated one first. Note also that item 13's write-up already concedes 'omitting the roundel does not cure it — Volkswagen licenses toy bodies precisely because the SHAPE is the asset', so the programme holds the refutation of its own first build and did not apply it.
* remedy: Move the one page of IP advice from §5.4 item 4 into §5.2 as precondition 0, ahead of the viewpoint and the cab door. It costs less than the illustrator's first day and it is the only precondition whose answer can delete the object rather than delay it. If the answer is that the silhouette cannot be sold, the sticker becomes a giveaway rather than merchandise and the whole programme re-ranks — better to know that in week one than after tooling.

**[TOP] THE COSMETIC DANGERS, NAMED — FOUR OF THE FIFTEEN. In each the risk section describes something that cannot fail, offend, cost money or be rejected.**

* evidence: (1) CALENDARIO ANO XXII — the object is SHIPPED and carries NONE of its stated danger. Every risk named (the chica de calendario register, the pin-up format, the illustrator's refusal) belongs to ANO XXIII, which is not shipped and may never be. What shipped is a one-ink line drawing that will offend nobody. A risk section about a different object is the purest form of the defect the fourth lens exists to catch. (2) CIENTO DIECIOCHO Y UNA / APAGA LA LUZ — 'the artefact's climax is a closure ... the bus goes out while the child watches' is strontium aluminate doing what strontium aluminate does. Every glow sticker ever sold decays. Reframing a material property as an emotional edge manufactures danger where there is none, which is the same dishonesty as sanding it off, pointed the other way. (3) MEDIA VENTANA — 'a named worker is fully modelled and the customer is a hole' is an interpretive ambiguity in a lino print. Nobody has ever been harmed by an ambiguous lino print. (4) EL TROQUEL — 'strikes a grade-E inference in permanent material' is a risk to the project's epistemics, not to the business. GRADO E incuse on a rim is a confession, and the object's own §5.1 entry says the confession was deleted from both faces and moved to the edge — which is the confession relocated, not retired.
* remedy: For each of these four, either name a failure mode with a person or a dollar on the end of it, or drop the risk section to one honest line: 'this object is safe; its risk is that it is boring.' The CALENDARIO's row in particular must be rewritten to state that the shipped artefact is risk-free and that the danger is entirely deferred.

**[HIGH] THE DANGERS THAT ARE REAL ARE REAL ENOUGH TO BE KILL DECISIONS, AND §5.1 RANKS THEM INSTEAD. Two objects put a named, plausibly undocumented worker's identity onto a product sold to strangers, and both treat 'we will ask them' as consent.**

* evidence: MARCA DEL COCINERO (#8) burns a line cook's name into every plate that crosses the counter; its own risk section says 'in 2026 it is harassment exposure, and for some workers it is immigration exposure' and then resolves it as 'the question goes to the COOKS.' NO SE VENDE (#9) does the same on 200 permanent glass objects. An employer asking a worker with precarious status for permission to publish their name is not a free choice — the ask itself carries the power asymmetry, and 'if they decline the jar prints the absence' turns a refusal into copy. RUIDO (#14) adds two more that cannot be cured at all: 'the photographers are unnamed and unlicensed anywhere in this repository' and 'whether any of these people still work there, or can be found at all, CANNOT BE RECOVERED FROM WHAT WE HOLD.' Those are not risks to hold, they are conditions that make the object unmakeable.
* remedy: Kill MARCA DEL COCINERO. Move the worker-naming mechanic out of NO SE VENDE and RUIDO and replace it with the painter/illustrator credit, who is a commissioned contractor and not an employee — the power asymmetry disappears and the object survives. RUIDO's sheets 5 and 6 should not exist even as unsold artist's proofs: a proof of a real non-consenting child is exposure the moment it is photographed.

**[HIGH] §5.4 ITEM 1's COUNTER-ARGUMENT IS FALSE. MANDIL 515 DID NOT COME OUT OF THE GARMENT SLOT, so the slot's negative result stands unrefuted — and separately the audited MANDIL is a different object from the amplified one.**

* evidence: `CONCEPT_BENCH_rev77.md`: 'MANDIL 515 · screen 7.17/10 ... **id** `dream:free-3-3`' — a FREE slot that DECLARED the register 'garment', not the garment slot. The garment slot is garment-1/2/3 = LADO E, 1.02 DEG, MANDIL 812, at 5.07 / 4.67 / 4.00, and `CONCEPT_AUDIT_rev77.md` line 179 says so explicitly: 'Two aprons (garment-3 MANDIL 812, free-3-3 MANDIL 515).' §5.4 item 1's 'THE SLOT IS SELF-REFUTING AS IT STANDS: MANDIL 515 came out of it' is therefore wrong, and the finding it was meant to soften is left standing at full strength. SEPARATELY: the audited MANDIL 515 is 'a separately cut and seamed rectangle ... faced in the body red' — a SOLID PANEL. The amplified one cuts the panel out into a void. Those are opposite objects; the 1.88 does not travel with the amplification, and §5.1 quotes it as though it did.
* remedy: Correct §5.4 item 1 (rule 13) — the garment slot's negative result is UNREFUTED. And add MANDIL 515 to §5.0's list of amplifications whose audit score no longer describes the object; it currently reads 1.88 with no [parent] mark while the amplification inverted the object's defining feature.

**[HIGH] TWO SHIPPED ARTEFACTS MAKE OPPOSITE DECISIONS ON THE NINE-TIMES-REJECTED EMBLEM, 2 mm APART, WITH NO RULE — AND §5.4 ITEM 9 PRAISES ONE HALF WITHOUT NOTICING THE OTHER.**

* evidence: `calendario.py` SUPPRESSES 149 glyph strokes and draws plain discs because the mark would print at 4.83 mm. `la_rueda.py` does the opposite: it draws the badge traced — `("badge", emb_seen, K["CAP_EMBLEM_D"], 0.010)` and prints `EMBLEMA · BADGE  Ø 86.9 mm` on the card face. At the card's own stated 1:12.8 that is 6.79 mm. I opened `design_out/loteria_la_rueda.png` and the roundel is there at the hubcap centre, reading as a blobby asterisk. So the project's own shipped output prints the mark the owner has rejected nine times, at 6.79 mm, while a second shipped file declines to print it at 4.83 mm. §5.4 item 9 cites calendario and EL TROQUEL as 'the correct reflex' and does not mention that a shipped artefact went the other way.
* remedy: Write the threshold down as a number in one place both scripts read, and say what it is grounded in. Then re-run la_rueda under it. Until F191 lifts, the honest default is the calendario's: suppress and draw the disc. A programme that cannot state at what size it will print its own emblem does not have a rule, it has two accidents.

**[MEDIUM] IS ANY OF IT BEAUTIFUL? ONE THING IS, AND IT IS BURIED UNDER A LEDGER OF THE COMPANY'S OWN FAILURES. I looked at all three shipped artefacts at size before writing this.**

* evidence: `design_out/calendario_ano_xxii.png` — the side-elevation line drawing of the bus is the only genuinely beautiful thing this programme has produced: confident, alive, the counter and galley reading through the flank. It occupies about 28 % of the sheet. Directly beneath it, at similar area, sits LOS ANOS DE LA CASA — twenty-one rows reading NO EMITIDO and a header '21 DE 22 NO EMITIDOS'. Beneath THAT, at the smallest type on the sheet, is the actual twelve-month date grid. A free wall calendar whose date grid is its least legible element is not a calendar; and a company handing customers a gift that says NOT ISSUED twenty-one times is not being deadpan, it is flagellating itself in public. `design_out/loteria_la_rueda.png` is handsome and cold: a technical drawing of a wheel over a spec table reading 'MEASURED OFF THE MESH / CAP_R + 2.5 mm / 0.3170 x HUBCAP / DECLARED · BRACKET 48-84'. Loteria is a game shouted fast across a table by children and drunk adults. This cannot be shouted. `design_out/sheet3_not_issued.png` is the best-made object of the three and it is a poster about the absence of a drawing. Critic 1's diagnosis reproduces exactly: 'this programme only becomes beautiful at the exact moment it stops measuring, and it treats that as a confession rather than as the finding it is.'
* remedy: On the calendario: cut LOS ANOS DE LA CASA to one line, double the date grid, and give the drawing the top two-thirds. That is thirty minutes of work on a shipped file and it converts a self-audit into a gift. On LA RUEDA: if the deck is to be played, the spec table comes off the face and goes on the back. A loteria card is an image, not a caption with a picture above it.

**[MEDIUM] BEST AND WORST, BY NAME, AS THE PERSON WITH THE BUDGET.**

* evidence: BEST: CIENTO DIECIOCHO Y UNA / APAGA LA LUZ, the glow-vinyl die-cut sticker. It is the only object on the bench with zero tooling, MOQ 10, a first step costing one A4 sheet and an evening, and a real chance of being kept for years on a bedroom ceiling. It is the only one in the impulse band. It discharges the fired trigger (F330) and starts the owed children's line (F331) in a single build. And its central fact — one emissive material in a 229-object vehicle, the party lights dark and the work light on — is the best single idea produced by all 75 concepts, because it is true of the asset before it is true of the story. Two directors reached it independently, which is the strongest evidence in the round. Buy it. Then check the die line against counsel (finding 3).  WORST: MARCA DEL COCINERO. It is a hot iron that burns a worker's name onto a stranger's lunch, in a kitchen where some of those workers may be undocumented, sold by their employer. It requires tooling, it requires food-safe practice nobody has costed, branded tortillas are already a catalogue product, and its own body concedes the technology's history in New Spain and proceeds anyway. It is the single most likely object here to become a news story, and unlike RUIDO it ships the harm on every plate. Runner-up worst: RUIDO, for the unlicensed photographers alone.  ART SCHOOL, TO BE CULLED IN ONE PASS: MEDIA VENTANA, A LA ALTURA · 118, EL TROQUEL, RUIDO, GRACIAS POR SU PREFERENCIA. Their shared defect is Critic 1's: the idea lives in a caption, a colophon or an incuse rim line that can be cut off, and A LA ALTURA is a 900 x 700 mm birch prop that no customer will ever buy.
* remedy: Fund the sticker. Kill MARCA DEL COCINERO and RUIDO. Park MEDIA VENTANA, A LA ALTURA and GRACIAS until the occlusion pass exists, and be honest that three of the fifteen are blocked on an afternoon of Blender work nobody has scheduled in 78 revisions.

**[MEDIUM] THE PRICES IN §5.5 ARE NOT COSTS, AND TWO OBJECTS HAVE UNIT ECONOMICS THAT DO NOT CLOSE. §5.4 item 5 concedes 'no cost, price, MOQ or lead time exists for any object' and §5.5 then prints figures as though they did.**

* evidence: §5.5 quotes '~$10-20', '~$40', '$0' and '~1 hour'. Those are consumables and machine time, not landed unit cost, and no MOQ or lead time appears anywhere in §5. Worse, two objects have arithmetic that fails on inspection. NO SE VENDE: 200 jars, each carrying a freehand hand-painted band by a named rotulista, at a stated $9/unit to the painter. At even fifteen minutes a band that is fifty hours of skilled sign-painting for $1,800, i.e. $36/hour before materials — and fifteen minutes is optimistic for freehand enamel over a pounce transfer. TACOS Y: '$58-68 hand / $32 machine (ESTIMATE, not quoted)' for a hand-embroidered napkin, which Critic 1 already ruled 'cannot pay rent.' Neither carries an hours figure, so neither can be checked, and both are labelled ESTIMATE, which in this project's own vocabulary is a grade, not a licence.
* remedy: Get ONE real quote for ONE object before the next round, and put an hours line under every hand-made item. Until then §5.5's heading should read 'the three cheapest things to TRY', not 'the cheapest things he could see first' — the first is true and the second implies a cost model that does not exist.

### LATE CRITIC 2 — verdict

> NOT SOUND AS RANKED, THOUGH MOST OF WHAT IT MEASURED IS RIGHT. Taking the six questions in order.
> 
> (a) IT RANKS ON THE AUDIT — AND THE RANKING DECIDES NOTHING. The column order in §5.1 is genuinely audit-descending, and I could not find a case where a screen figure overrode an audit figure. But three defects hollow it out. The declared tiebreak (`dangerIntact`) NEVER FIRES anywhere in the table — every tie block is uniformly danger-true or uniformly danger-false — and the actual within-tie order is the screen's descending order in three blocks of four, eleven rows of fifteen, INCLUDING the tie that decides which object is #1. Second, the ranking is consumed by nothing: §5.2 orders by owner ruling, §5.5 by cost, and the audit's own #1 (`DE LA MANO DE`, 2.25, danger intact) appears in neither. Third and worst, "rank on the audit" silently deletes six of the sixteen shortlisted concepts because they have no audit score — including LA TAPA at screen 8.70, the second-highest of all 75. The document's own thesis is that the screen carries no information; it then lets the screen's selection of what got audited decide the entire field, invisibly.
> 
> (b) NO — F331 COMPLIANCE IS COUNTED WRONG IN THE SECTION THAT COUNTS IT. Every row does carry a line, which is the letter of F331 and is to the document's credit. But §5.0 says six bodies declare nothing and §5.1 stamps `[ASSIGNED]` on seven; and the body count cannot close — fifteen rows in which one row merges two bodies is sixteen bodies, against a stated fifteen, in a paragraph headed "COUNTED, NOT TRANSCRIBED".
> 
> (c) GESTURED AT, AND ITS CENTRAL FACTUAL CLAIM IS FALSE. §5.3 says the picture book "is in the pool and is not in the shortlist". It is #6 of 16 at screen 8.50, `free-5`, described in the shortlist's own words as "for the children the owner has been asking about". `DALE` (#7, 8.40) is the children's DOING object §5.3 says does not exist among finalists — correctly flagged as unaudited, but not as shortlisted. So the two highest-screening children's concepts in the round were discarded by the audit-only rule and then reported as absent. §5.3's conclusion — that what is really missing is a REGISTER, not an object — is the best paragraph in the document and survives; its premise does not.
> 
> (d) THE FORBIDDEN PAIR IS NOT PRINTED, BUT IT IS LOAD-BEARING AND UNDECLARED. No "109.5 | 129.5" string appears. But row 8's "two equal pillars … 5.98 mm" is their arithmetic mean to within 0.2 mm, its derivation is unstated, and the pair itself is recoverable in one subtraction from the `BAY_CX` constants row 3 prints on the same page. One row (`A LA ALTURA · 118`) carries an audit score citing a parent that does not exist in the audited fourteen — and §5.5 promotes it to the single cheapest action in the document. Everything else I spot-checked reproduces exactly: 118 lamps at 28.5197 mm and 123 without `_aft()`; zero AO/normal/depth passes; `WS_PANE_W` genuinely carrying no provenance comment; the counter's 3.106 m run and 55.1 mm climb; `Z_SILL − CNT_ZT` = 118.0 mm and its rake-invariance; the 9.150 mm fall and 91.017°/88.983°; `MAN_ROWS/MAN_COLS` at 9.29 %; `LOUV_APERTURE`'s own "# INFERRED, not measured" line; the tracked `probe_scratch/line_pass.json` carrying `n_strokes 2711, n_points 19471`; eight `sticker` rows in `AUDIT_rev43.md`. The measuring is good. The counting and the bookkeeping are not.
> 
> (e) IT STATES CEILINGS UNUSUALLY WELL AND THEN FAILS TO APPLY THREE OF ITS OWN. §5.0b is the strongest work here — the 115-vs-118 settlement, the line-pass instability with a retraction of its own n=2 reading, the grep-not-assertion on the occlusion half. But: it opens F341 for printing one draw as a constant and then prints whistle cents to 0.1 against a ±7-cent sweep; it cites the sticker spec's eight rows as authority and drops that spec's own ceiling paragraph, which says every millimetre in them is a projection and not an observation; and its azimuth table mixes nose and tail conventions and omits five of fourteen cameras inside the very paragraph whose subject is convention ambiguity.
> 
> (f) IT DROPPED THE ROUND'S OWN NAMED BEST IDEA AND A LIVE BLOCKER ON THE THING IT ORDERS BUILT FIRST. `DIEZ FLORES Y MEDIA` — #10, screen 8.20, danger intact, named "BEST IDEA, BY NAME" by the programme document itself AND "THE SINGLE BEST IDEA IN THE POOL, BY NAME … Fund it" by completeness critic 1 — appears nowhere in §5: not ranked, not deferred, not refused, not in §5.4. Two independent judges converged on one object, which is exactly the reasoning §5.0 uses to call the double amplification of BUENAS NOCHES "the strongest single piece of evidence in the round". And §5.2's "three things that must be settled before a line is drawn" omits `optics-6`, which `AUDIT_rev43.md:297` says the die-cut rule RESTS ON, which `studio.py:93-111` confirms is still open at HEAD, and whose test is one render that is already written.
> 
> WHAT SHOULD SURVIVE UNCHANGED: §5.0b entire (five real measurements, two retractions made in place); the refusal to promote PROVECHO on 8.73; the `[ASSIGNED]` device for undeclared lines; row 3's refutation of its own shot from `van_floor`'s top at 511.2 mm; row 12's shear arithmetic; and §5.3's diagnosis that the children's half lacks a register rather than an object.
> 
> CEILING ON THIS CRITIQUE: single reader, one pass, run against HEAD `959a9f8` only. I verified source constants, camera azimuths, the shortlist and the tie ordering by recomputation; I did NOT re-run the line pass (four bakes, ~2 minutes each), did not open the fifteen amplified bodies (I inferred the parent mapping from names and descriptions, and the `A LA ALTURA` orphan is the one inference that could be overturned by a document I could not read), and did not re-score any concept. Whether the six unaudited shortlist entries would have survived an audit is not something I can recover from what we hold — but that is the point: neither could the synthesis, and it ranked as though it could.

**[TOP] SIX OF THE SIXTEEN SHORTLISTED CONCEPTS WERE NEVER AUDITED, AND "RANK ON THE AUDIT" SILENTLY DELETES THEM. §5 never says they exist. `DESIGN_PROGRAM_rev77.md` §2's top-16 contains LA TAPA (#2, screen 8.70 — the second-highest of all 75), EL DÍA QUE LE CORTARON EL TECHO (#6, 8.50), DALE (#7, 8.40), CINCO ANTOJITOS (#9, 8.27), DIEZ FLORES Y MEDIA (#10, 8.20) and GUIRNALDA (#14, 8.03). None is among the fourteen audited. Five of the six appear NOWHERE in §5 — not in §5.1, not in §5.3, not in §5.4's "WHAT THIS ROUND DID NOT FIX". Only MI COMBI (#15) is mentioned, once, in §5.2. The synthesis's own thesis is that the screen "decided what got audited and nothing more" — so an unaudited concept is UNRANKED, not low-ranked. Treating absence of an audit as absence of merit re-imports the exact selection the section says carries no information, and does it invisibly.**

* evidence: `sed -n '78,94p' DESIGN_PROGRAM_rev77.md` prints all sixteen rows. The audited fourteen (§2 of the task, reproduced in §5.0) contain neither LA TAPA nor DIEZ FLORES Y MEDIA nor EL DÍA QUE LE CORTARON EL TECHO. §5.4 item 2 says only "8 of 15 bodies carry `audit n/a`" — a statement about amplifications, not about the six shortlisted parents that were never scored at all.
* remedy: Add a row to §5.1's table, or a named block beneath it, listing every top-16 concept with NO audit score, marked `UNRANKED — not scored, not rejected`. Then state the consequence in one line: the audit ordering is defined only over the fourteen the screen happened to pass forward, and six shortlisted objects are outside it. Either audit the six (four lenses, the same rubric) or say plainly that the programme's ranking covers 14 of 16 and which two-thirds of the danger-intact field is unexamined.

**[TOP] §5.3's LOAD-BEARING CLAIM ABOUT THE CHILDREN'S LINE IS FALSE, AND IT IS FALSIFIED BY THE DOCUMENT §5 IS BEING APPENDED TO. §5.3 writes: "NOTHING A CHILD READS. The picture book the first critic named as *'the only children's object anyone keeps for twenty years'* is in the pool and is not in the shortlist." It IS in the shortlist. It is `EL DÍA QUE LE CORTARON EL TECHO`, slot `free-5`, **#6 of 16, screen 8.50** — the sixth-highest concept in the round — and its own one-line description ends "for the children the owner has been asking about since rev". The synthesis declares the children's half empty of reading matter while the round's own shortlist carries the picture book six rows from the top. This is not a judgement call; it is a checkable statement about `DESIGN_PROGRAM_rev77.md` §2 that does not survive a grep.**

* evidence: `grep -n "CORTARON" DESIGN_PROGRAM_rev77.md` → line 84: `| 6 | **EL DÍA QUE LE CORTARON EL TECHO** | free-5 | 8.50 | yes | The true story of a green bus that could not go any further, so it stayed and fed people — for the children the owner has been asking about since rev |`. The same file's "BEST IDEA, BY NAME" paragraph (line 107) names `[dream:free-5-1] the picture book (the only children's object anyone keeps for twenty years, and it delivers F18 inside its own back board)` — same slot.
* remedy: Correct the sentence in place (rule 13) and carry the correction: the picture book is #6 at 8.50 and was NOT audited. Then re-decide §5.3 with it visible — and note the clause the synthesis dropped, that the book "delivers F18 inside its own back board", which makes it a second route to the object §5.2 orders built first. §5.3's conclusion that the children's half is a missing REGISTER may still stand; its premise that nothing exists must not.

**[TOP] §5.1 ROW 12 — `A LA ALTURA · 118` — HAS NO PARENT AMONG THE FOURTEEN AND WEARS A BORROWED AUDIT SCORE, AND §5.5 PROMOTES IT TO THE SINGLE CHEAPEST ACTION. Mapping every row to a parent exhausts the fourteen at fourteen rows: DE MANO EN MANO→1, DIRECTO→2, GRACIAS→3, CALENDARIO→4, EL TROQUEL→5, MANDIL→6, BUENAS NOCHES→7 (×2), EL FIERRO→8, ¿TRAE SU ENVASE?→9, DIEZ Y MEDIA→10 (TACOS Y — the parent is "the cloth the tortillas arrive in, embroidered"), 515.5×403→11, SILBATO→13, RUIDO→14, PROVECHO→15. Row 12 is left over. It nevertheless prints `audit 1.75 [parent]` and `danger false [parent]` — a citation to a parent that does not exist in the audited set. It is then made item 1 of §5.5, "the cheapest honest test on the bench", i.e. the most actionable recommendation in the whole document is the one row with no audit under it, inside a section whose headline is RANK ON THE AUDIT.**

* evidence: §2's fourteen audited names, matched one-to-one against §5.1's fifteen rows, leave `A LA ALTURA · 118` unmatched; `grep -n "A LA ALTURA\|ALTURA" DESIGN_PROGRAM_rev77.md CONCEPT_BENCH_rev77.md` returns no concept of that name — only two incidental `ALTURA` strings in bench captions (lines 581, 753). §5.5 heading 1: "THE SHEARED APERTURE AT 1:1, ON PAPER — ~1 hour, $0 … From item 12."
* remedy: Name row 12's parent explicitly, or strike its `[parent]` marks and label it `UNAUDITED`. Its underlying measurement — the 9.150 mm fall and the 1.017° shear, both of which I recomputed and both of which reproduce exactly from `BAY_W 0.5155` and `RAKE_DZDX 0.017750` — is sound and worth keeping in §5.5. The score is not. Say "an unaudited object with a verified measurement" and let the owner weigh it as that.

**[TOP] §5.2 LISTS "THREE THINGS THAT MUST BE SETTLED BEFORE A LINE IS DRAWN" AND OMITS A NAMED, LIVE, CHEAP BLOCKER ON THE DIE-CUT OUTLINE ITSELF. `AUDIT_rev43.md` carries it in the same file §5.2 cites for the spec: "THE CONTACT SHADOW — CROSS-DIMENSION ORPHAN. Sev 3. `studio.py` lines 93–111 leave `optics-6` OPEN … The sticker's sev-4 die-cut rule *'bridge the underbody with the cast shadow'* RESTS ON IT. Close: the `T1_CATCH=0` A/B is already written — one run settles whether the bridge has a shadow to use." `studio.py` confirms it is still open at HEAD: "So the catcher stays ON and `optics-6` stays OPEN" … "the catcher's shadow survives the alpha-over at a few code values" … "T1_CATCH=0 reproduces the A/B in one render", with `ob.is_shadow_catcher = bool(int(os.environ.get("T1_CATCH", "1")))` live. So the cut path — one of the eight spec rows §5.2 leans on — depends on an unresolved question whose test is one render, and §5.2's blocker list does not contain it.**

* evidence: `grep -n "T1_CATCH\|catch" studio.py` → lines 93, 99, 110–111, 117 as quoted; `grep -n "sticker" AUDIT_rev43.md` → line 297 for the orphan, line 144 for the die-cut row it blocks.
* remedy: Add it as a fourth precondition and run it first — it is one render and it is already written. If the catcher's shadow does not survive the alpha-over, the spec's die-cut rule has no shadow to bridge with and the cut path needs re-specifying before any line is drawn, not after.

**[HIGH] THE DECLARED TIEBREAK NEVER FIRES ANYWHERE IN THE TABLE, AND THE ACTUAL WITHIN-TIE ORDER IS THE SCREEN'S — INCLUDING THE TIE FOR FIRST PLACE. §5.1's header states: "Ordered by audit score, `dangerIntact` breaking ties — because the fourth lens exists precisely to catch the sanding that hit 10 of 14." Checked against the table: every tie block is uniformly danger-false (1.88 × 4; 1.75 × 5) or uniformly danger-true (2.25 × 2; 1.62 × 2). The tiebreak separates nothing, anywhere. What actually orders the ties is the screen: 2.25 block → 8.33, 8.17 (descending); 1.75 block → 8.5, 8.2, 8.17, 7.07 (descending); 1.62 block → 7.6, 5.53 (descending). Three of the four blocks, eleven of the fifteen rows, and the decision of which object is #1. Only the 1.88 block departs from it.**

* evidence: Recomputed: 2.25 ['DE LA MANO DE','DIRECTO'] screen [8.33, 8.17] descending TRUE; 1.88 ['CALENDARIO','TROQUEL','MANDIL','GLOW'] [8.53, 8.0, 7.17, 8.6] descending FALSE; 1.75 ['MARCA','NO SE VENDE','TACOS Y','MEDIA VENTANA','A LA ALTURA'] [8.5, 8.2, 8.17, 7.07] descending TRUE; 1.62 ['SILBATO','RUIDO'] [7.6, 5.53] descending TRUE.
* remedy: Either declare the real secondary key (it is the screen, and saying so is honest and defensible as an arbitrary stable sort) or replace it with something the audit can supply — mean of the four lens sub-scores, or lowest single lens. Delete the `dangerIntact` sentence: a tiebreak that cannot fire on this data is a claim about method that the table does not implement, which is exactly the shape §5.0b item 3 catches elsewhere.

**[HIGH] THE AUDIT RANKING IS COMPUTED, PUBLISHED, AND THEN CONSUMED BY NOTHING. §5.1 orders by audit. §5.2 orders by owner ruling ("the sticker, and specifically its daylight face" — row 7). §5.5 orders by cost (rows 12, 6, 7). Three orderings in one document, and the audit's own #1 — `DE LA MANO DE`, 2.25, danger intact, the joint-highest score in the round — appears in NEITHER action section. It is dropped on "blocked on AO pass; an illustrator", which is stated, but no section then says what to do about the top-ranked object. The owner override in §5.2 is legitimate and correctly declared ("the owner outranks the ranking"); the cost ordering in §5.5 is also declared. The defect is that after all three declarations nothing is left that the audit ranking decides.**

* evidence: §5.1 row 1 `DE LA MANO DE … 2.25 [parent] … intact`; §5.2 builds the sticker (row 7, 1.88) and DIRECTO (row 2, 2.25); §5.5's three are rows 12, 6, 7. `DE LA MANO DE` occurs in no other section of §5.
* remedy: Add one line under §5.1: what the audit order is FOR. If the answer is "it decides what gets funded once the AO pass lands", say that and put `DE LA MANO DE` at the head of a named second wave with its two blockers costed. If the answer is that owner ruling and cost decide everything actionable this revision, say that too — but then §5.0's "RANK ON THE AUDIT" is advice to a future context, not an instruction this document follows, and it should be labelled as such.

**[HIGH] THE ROUND'S OWN "BEST IDEA, BY NAME" IS ABSENT FROM §5 ENTIRELY, AND SO IS THE COMPLETENESS CRITIC'S. `DESIGN_PROGRAM_rev77.md` line 107: "BEST IDEA, BY NAME: [dream:beautiful-1] DIEZ FLORES Y MEDIA. It is the only thing here that is beautiful before it is clever … Pay the painter or commission a taller — that cost is not negotiable and it is small." Completeness critic 1 named the identical object at HIGH: "THE SINGLE BEST IDEA IN THE POOL, BY NAME: [dream:beautiful-1] DIEZ FLORES Y MEDIA … Fund it." It is #10 of the shortlist at screen 8.20 with danger intact. It appears nowhere in §5 — not ranked, not deferred, not refused, not listed in §5.4 as something the round did not fix. Two independent judges converged on one object and the synthesis is silent about it. Note also that §5.0 correctly treats the double amplification of BUENAS NOCHES as "the strongest single piece of evidence in the round" precisely BECAUSE two directors converged — the same reasoning applied here would have promoted this object, not dropped it.**

* evidence: `sed -n '88p;107p' DESIGN_PROGRAM_rev77.md`. Searching §5 for "DIEZ FLORES", "hule", "oilcloth", "tablecloth" returns nothing. Note it is a DIFFERENT object from `DIEZ Y MEDIA` (#13, free-7, the embroidered cloth), which IS carried as row 10 `TACOS Y` — the near-identical names are a trap and the synthesis never distinguishes them.
* remedy: Add it to §5.1 marked `UNAUDITED — screen 8.20, danger intact, named BEST IDEA by two independent judges`, or add it to §5.4 with the reason it was not carried. And add one line disambiguating `DIEZ FLORES Y MEDIA` (#10, beautiful, hule tablecloth) from `DIEZ Y MEDIA` (#13, free-7, embroidered servilleta) so no future context merges them.

**[HIGH] THE `[parent]` MARK — THE READER'S ONLY SIGNAL THAT A SCORE IS STALE — UNDERCOUNTS ITS OWN STATED TOTAL, SO TWO ROWS CARRY A STALE SCORE WITH NOTHING SAYING SO. §5.0 states the ceiling: "Eight of the fifteen amplified bodies carry `audit n/a` — they were never audited after amplification. So for those eight, ranking on the audit ranks a version of the object that no longer exists." §5.1 then marks `[parent]` on rows 1, 7, 9, 10, 11, 12 — six rows. Row 7 covers two bodies, giving seven. The stated eight is not reached, and the document nowhere names which bodies they are. A reader cannot tell which two of rows 2, 3, 4, 5, 6, 8, 13, 14, 15 is carrying a score for an object that no longer exists. This is the amendment-reaches-some-sections defect the project's own record names (F322's class), committed inside the section that states the ceiling.**

* evidence: §5.0: "Eight of the fifteen amplified bodies carry `audit n/a`". §5.1 table: `[parent]` appears on rows 1, 7, 9, 10, 11, 12 only. Rows 2 (2.25), 3 (2.12), 4 (1.88), 5 (1.88), 6 (1.88), 8 (1.75), 13 (1.62), 14 (1.62), 15 (1.50) are unmarked.
* remedy: List the eight by name. If the count is wrong rather than the marking, correct the count and say which. Until then no row's audit figure in §5.1 can be relied on, because the set of unreliable ones is unspecified — which makes the whole column soft, not just eight of it.

**[HIGH] THE BODY COUNT DOES NOT CLOSE, IN THE PARAGRAPH THAT SAYS "COUNTED, NOT TRANSCRIBED", AND F331 COMPLIANCE IS COUNTED WRONG TOO. §5.0: "THE HEADER SAYS FOURTEEN AMPLIFIED CONCEPTS WHILE FIFTEEN BODIES EXIST. COUNTED, NOT TRANSCRIBED. The extra is `BUENAS NOCHES, COMBI`, which was amplified TWICE." But §5.1 lists FIFTEEN ROWS in which row 7 already merges the two BUENAS NOCHES bodies — fifteen rows with one row worth two bodies is sixteen bodies, not fifteen. Separately, §5.0 lists six bodies that declare no line — "`DE LA MANO DE`, `CALENDARIO AÑO XXII`, `MARCA DEL COCINERO`, `MEDIA VENTANA`, `DIRECTO`, `TACOS Y`" — while §5.1 stamps `[ASSIGNED]` on SEVEN rows: 1, 2, 4, 8, 10, 11 and 15 (`PROVECHO` — "adult `[ASSIGNED]`"). §5.3's arithmetic "3 declare children, 6 declare adult, 6 declare nothing" = 15 only if PROVECHO is not a body; if it is, the total is 16 and the undeclared count is 7.**

* evidence: §5.1 rows 1–15 counted directly; row 7 titled "CIENTO DIECIOCHO Y UNA / APAGA LA LUZ" and described as "two independent amplifications of one parent". `[ASSIGNED]` occurs on rows 1, 2, 4, 8, 10, 11, 15.
* remedy: State the body count once, in one place, with PROVECHO's status explicit (carried body or withdrawn), and make §5.0, §5.1 and §5.3 agree. The F331 figure the next context will quote is "6 of 15 declare no line"; on the table as printed it is 7 of 16. One of the two is wrong and the register row for F331 compliance will inherit whichever ships.

**[HIGH] §5.0b ITEM 5 MIXES TWO AZIMUTH CONVENTIONS IN THE PARAGRAPH WHOSE ENTIRE SUBJECT IS A CONVENTION AMBIGUITY, AND OMITS FIVE OF FOURTEEN CAMERAS. The published list — "`side` 90.0° · `topdown` 57.8° · `hero34r` 38.4° · `detail_f` 35.4° · `hero34f` 34.7° · `low34` 34.0° · `front34` 26.8° · `front`/`rear` 0.0°" — is stated as "measured from the nose (+X) axis". Recomputing every view from `loc − tgt`: `hero34r` is **141.56°** from the nose (38.44° from the TAIL) and `rear` is **180.0°**, not 0.0°. Two of the nine entries are in the tail convention, silently, in the paragraph that says "I cannot tell whether its 18° is measured off the nose axis or off the flank". Five cameras are missing entirely: `counter` 48.41°, `hero` 34.70°, `playa` 56.94°, `playa_ref` 151.51°, `playa_w` 45.00°. And §5.2 calls it "a table that already holds thirteen" — `studio.views()` returns fourteen.**

* evidence: `python3 -c "import studio; v=studio.views()"` → 14 keys: counter, detail_f, front, front34, hero, hero34f, hero34r, low34, playa, playa_ref, playa_w, rear, side, topdown. Azimuths from `atan2(loc.y−tgt.y, loc.x−tgt.x)`: hero34r 141.56, rear 180.00, playa_w 45.00, counter 48.41, playa 56.94, hero 34.70, playa_ref 151.51.
* remedy: Reprint the full fourteen in one convention, stated. The CONCLUSION survives — nothing is at 18° or at 72° — and `low34`'s exact 1.55 m match still stands, so the finding is real and worth keeping. But it is currently presented as an exhaustive search and it is neither exhaustive nor single-convention, and a next context re-deriving it will find the discrepancy and distrust the conclusion with it.

**[HIGH] THE STICKER'S 118 LAMPS AT 200 mm FALL BELOW THE SPEC'S OWN DELETION FLOOR, AND THE DOCUMENT APPLIES A LEGIBILITY FLOOR TO THE EMBLEM AND NOT TO THEM. §5.5 item 3 prescribes "the 118 lamps at their realised 28.5197 mm" on a 200 mm sticker at 1:20.325. That is a **1.403 mm pitch**; `BULB_R = 0.0110` gives a 22 mm bulb, **1.082 mm at scale**, leaving **0.321 mm between adjacent lamps**. `AUDIT_rev43.md`'s own sacrifice rule deletes flank components because "every one lands under 0.40 mm". The gaps between the lamps are under that floor, so the string prints as one continuous bead and the 118-lamp count — which is the whole proposition of row 7, "the party lights are dark and the work light is on" — is not resolvable at the size prescribed. Meanwhile §5.2 praises `calendario.py` for suppressing 149 glyph strokes rather than print the emblem at 4.83 mm and calls it "the right reflex"; the badge at this sticker's scale is 4.28 mm, and the lamps are four times smaller than the thing that reflex refused.**

* evidence: Recomputed: 28.5197/20.325 = 1.4032 mm pitch; 22.0/20.325 = 1.0824 mm diameter; gap 0.3208 mm; 86.9/20.325 = 4.276 mm badge; string 3336.8/20.325 = 164.2 mm of a 200 mm sticker. `grep -n "sticker" AUDIT_rev43.md` line 143 for the 0.40 mm rule; line 145 for the "0.15 mm floor".
* remedy: Apply the spec's own floors to the lamp string before drawing it: either raise the sticker's scale, or draw the string as a rule with a stated lamp count in the key rather than 118 discs, or accept the bead and say the count is not readable at 200 mm. Whichever, the sheet must state it — the same reflex the document credits `calendario.py` for.

**[HIGH] ITEM 8's "TWO EQUAL PILLARS … 5.98 mm" IS THE UNDECLARED ARITHMETIC MEAN OF THE FORBIDDEN 109.5 | 129.5 PAIR, AND THE PAIR IS DERIVABLE FROM CONSTANTS ITEM 3 PRINTS ON THE SAME PAGE. §5.1 item 3 publishes `BAY_CX` 0.6720 / 0.0470 / −0.5980 and `BAY_W` 0.5155. Those give centre pitches of 625.0 and 645.0 mm and therefore pillars of **109.5 and 129.5 mm** — the pair the brief forbids. Item 8's field is built on a single pillar of 5.985 mm at 1:20, i.e. **119.7 mm**, which is the mean of 109.5 and 129.5 to within 0.2 mm. The change is named ("pillars equalised") but never quantified: the document nowhere states the pillars are unequal on the model, by how much, or that 5.98 is an average. A reader recomputing from item 3's own constants gets 5.475 and 6.475 and cannot reconstruct 5.98. Worse, the underlying contradiction is unreconciled: `t1_shell.py` labels `BAY_CX` "# measured centres" while the record holds that the photograph's pillars are EQUAL. Item 8 silently picks the photograph over a source comment that says MEASURED, and says nothing.**

* evidence: `t1_shell.py:151-152`: `BAY_W = 0.5155  # equal, measured` / `BAY_CX = (0.6720, 0.0470, -0.5980)  # measured centres`. Recomputed: pitches 625.0 / 645.0 mm; pillars 109.5 / 129.5 mm; mean 119.5 mm → 5.975 mm at 1:20; item 8's field 3×25.775 + 2×5.985 = 89.295 ≈ its printed 89.28.
* remedy: State it: "the model's pillars are unequal (the record forbids quoting the pair as a differentiator); the die regularises them to their mean, 119.5 mm, because the photograph shows them equal — a declared departure from the mesh." And open a register row on the real contradiction: `BAY_CX`'s "# measured centres" against the record's equal-pillar photograph. That is a live finding about the VEHICLE and it is worth more than the die.

**[MEDIUM] §5.2 CITES THE STICKER SPEC'S EIGHT ROWS AS AUTHORITY AND DROPS THE SPEC'S OWN CEILING PARAGRAPH, WHICH SITS IN THE SAME FILE AND SAYS EVERY MILLIMETRE IN THOSE ROWS IS A PROJECTION. §5.2's third precondition-of-confidence is "THE SPEC IS WRITTEN, AND IT IS WRITTEN FOR THIS OBJECT — 8 `sticker` rows in `AUDIT_rev43.md` with the DESIGN column intact". The row count is correct — I counted lines 121, 122, 123, 143, 144, 145, 146, 167. But `AUDIT_rev43.md:277` carries the spec's own ceiling and §5 never quotes it: "**Ceiling:** The ceiling of this method is that it can prove SIZES AND ORDERINGS, and cannot prove BEAUTY. There is no sticker, no render, no printed proof and no drawn line anywhere in this tree … So every millimetre figure above is a PROJECTION from a measured metre through a stated scale, never an observation of artwork, and I have described no render at any point because I cannot see one." In a document whose house rule is "report a measurement WITH ITS CEILING", the one artefact ordered built first cites a spec and leaves the spec's ceiling behind.**

* evidence: `grep -c "sticker" AUDIT_rev43.md` → 11 (8 table rows + prose at 276, 277, 297); `sed -n '277p' AUDIT_rev43.md` for the ceiling quoted above.
* remedy: Carry the ceiling into §5.2 verbatim. It changes what the first build is FOR: the eight rows can settle sizes and orderings on the daylight face and cannot settle whether it is any good, so the first proof is a thing to LOOK AT (rule 1), not a thing to check off against the spec.

**[MEDIUM] THE WHISTLE PUBLISHES CENTS TO ONE DECIMAL AGAINST ITS OWN ±7-CENT SWEEP — THE EXACT DEFECT §5.0b ITEM 3 CATCHES FOR THE LINE PASS, COMMITTED EIGHT ROWS LATER. Row 13: "the intervals above the first fingered note are **+490.5 and +801.7 cents**" and, in the same block, "wall swept 1.0 → 4.0 mm moves them only to 484.6→499.5 and 793.5→814.3". So the quantity has a stated spread of ~15 and ~21 cents and is printed to 0.1. §5.0b item 3's whole point is that "the number on its face is ONE DRAW from a distribution with a spread of 5 and 7, published as though it were a constant", and it opens a register row (F341) for it. The same standard is not applied here. Two smaller instances of the same shape: row 5 quotes "30.68 × 23.99 mm at Ø300" without ever stating the scale those come from (it is 1:16.8 — every one of row 5's figures reproduces at that scale and at no other, so a Ø300 disc carries a 272.6 mm drawing), and row 13's "200.00 × 87.49 × 83.57 mm" gives a body width of 1778 mm where `STATE.md` reads W = 1.7497 (1749.7 → 86.09 at 1:20.325), unexplained.**

* evidence: Row 13 as quoted. Recomputed for row 5: 515.5/30.68 = 16.80; 664.9/16.8 = 39.58 ✓ (printed 39.58); 274.0/16.8 = 16.31 ✓; 86.9/16.8 = 5.17 ✓; 5.5/16.8 = 0.327 ✓ — internally exact, scale never stated. Row 13: 1749.7/20.325 = 86.09 vs printed 87.49.
* remedy: Round the cents to the sweep (a fourth and a minor sixth, ±10 cents), state row 5's 1:16.8 and its 272.6 mm drawn field beside the Ø300 blank, and either derive row 13's 87.49 or mark it as the shell-plus-wall envelope. All three are one-line fixes and all three are the standard the document sets for itself in §5.0b.

**[MEDIUM] COMPLETENESS CRITIC 2's TOP FINDING — THAT THE PEOPLE IN SEVEN CONCEPTS ARE FABRICATED AND THE FABRICATION IS LOAD-BEARING ON EVERY CONSENT ARGUMENT — IS NEITHER DISCHARGED NOR LISTED AS UNFIXED. The critic wrote: "'Magenta puffer coat', 'back to camera', … and the headcounts 'seven real people' (people-1, packaging-2) / 'six people' (free-2-1) exist nowhere in this repository", with the remedy "Crop and paint every human region … publish the crops, count the figures". Row 14 (RUIDO) publishes exactly the kind of figure that remedy would produce — "`EL DE LA COMANDA` face ~55 × 70 px", "`LA NIÑA` head 100 × 121 px", "`EL COCINERO` ~35 px in profile" — but never says the crops were painted and looked at (rule 8), never says which frames they came from, and never states whether the critic's fabrication charge was answered or survives. §5.4 lists nine unfixed items and this is not among them. Given that row 14's entire risk case rests on who those people are, the provenance of those three pixel figures is load-bearing.**

* evidence: Critic 2 TOP finding (f) as quoted in the round's own record; §5.1 row 14's three px figures; §5.4 items 1–9 contain no entry on fabricated people. (Working crops named `s1_camisa_roja.png`, `s2_cocinero.png`, `s3_nina.png` exist in this session's scratchpad but are outside `git ls-files` — F335's rule: if it is not in `git ls-files`, it does not exist.)
* remedy: For each of the three, name the frame and the pixel window, commit the painted crop, and say in row 14 whether critic 2's charge is discharged for these three and still open for the other four concepts. If the crops cannot be committed, the figures should carry `UNPAINTED` — and §5.4 gains a tenth item.

---
## §3 THE LAST SIX AMPLIFICATIONS, IN FULL

**These six were the ones the interrupted run never reached.** Each was given its own four audit
verdicts and told not to sand off the danger; each declares which LINE it is in, as F331 requires.

### EL TROQUEL — el lado ciego  ·  LINE: adult

**REGISTER** beautiful-not-rigorous / funerary / three-dimensional / food · ADULT LINE (F331)  
**ARTEFACT** ONE DIE, TWO FACES, THREE OBJECTS OFF ONE HEIGHT FIELD.

**1. EL TROQUEL — Ø300 mm, hand-carved end-grain hardwood, the object itself.** Not a medal: the DIE. The negative, hung on a wall. Cut from a Z pass through the existing side orthographic camera, at 1:16.8 (vehicle 242.1 × 132.6 mm in a Ø276 field, 12 mm rim band). Two faces:

* **OBVERSE — EL LADO DE SERVICIO.** The show flank. Three serving apertures, MEASURED: 515.5 × 403.0 r55, three, equal. On the die at Ø300 they are 30.68 × 23.99 mm each.
* **REVERSE — EL LADO CIEGO.** The off flank. No apertures — the conversion is on one side only, so this face is still a van: two cargo-door shut lines and three windows. **SPEC grades that flank E, never photographed. Its two colliding features are BOTH grade E and CONTRADICT EACH OTHER, and shown the sightlines the owner himself answered "cannot tell from this crop." `STATE.md` carries it as a labelled regression catcher at 804.9 mm — meaning "it has not moved", explicitly NOT "it is right."**

**NOTHING IS WRITTEN ON EITHER FACE.** No caption, no confession, no `PROFUNDIDAD EXAGERADA`, no `ALTURA: SIN MEDIR`. Every word is incuse on the EDGE — 942 mm of rim, one continuous line you must rotate the object in your hands to read:

`COMPRADA VERDE · MÉXICO, D.F. · 2006 · $3,000 — LE FALTABAN TRES VENTANAS — MOTOR: NINGUNO · TRANSMISIÓN: VENDIDA — LADO DE SERVICIO: MEDIDO — LADO CIEGO: GRADO E, NUNCA FOTOGRAFIADO — SIN EMBLEMAS — 1:16.8 — HOJA 3 DE 4, NO EMITIDA`

**The die cites, as its authority, a drawing that was never issued.**

**2. EL CHOCOLATE — Ø55 mm, ~28 g, tempered dark, given with the check.** Cast from a 21-cavity polycarbonate mould at 1:94.6. Cut from the OPEN, SERVING pose — lid up, board down, 115 festoon lamps — the bus at work. Wrapper carries only the three story lines.

**3. LA MEDALLA — Ø55 struck bronze. YEAR TWO, and only if he still wants it after holding 1 and 2.** Not costed into this.

**AND THE VEHICLE ON THE PERMANENT OBJECT IS STRUCK CLOSED, AND WITH ITS BADGES DELETED.**

**A Z buffer is a single-valued height field and so is a bas-relief. That much of the original is true and it is the only thing in it that was.** Everything the four lenses attacked came from three numbers pointed at the wrong objects. Correct them and the object changes shape.

**THE PERMANENT / PERISHABLE SPLIT IS NOT A PACKAGING DECISION. IT IS THE RECORD'S OWN MEASURED/POSE DISTINCTION, GIVEN MATERIALS.**

`STATE.md` reports length two ways: **4.317 m with the lids open, 4.065 m without.** The original quoted 4065 and then struck an open tail board — the wrong vehicle for its own scale. Every open dimension on this model is a POSE: `TB_TILT_DEG = 38.0` against a photographed 28.0 (unresolved seven revisions), `REAR_OPEN_DEG = 64.0` logged NOT MEASURED, `TRUNK_OPEN_DEG` currently 0, `LID_OPEN_DEG` environment-overridable. Strike it closed and **there is not one unmeasured pose left in the object.**

So:

* **THE PERMANENT OBJECT IS THE VEHICLE CLOSED.** Not serving. Parked. Every number on it measured. This is the dead one, and it is in wood that outlives everybody.
* **THE PERISHABLE OBJECT IS THE VEHICLE OPEN.** Lid up, board down, lamps lit — at a declared pose, because a pose is allowed to be a pose for one afternoon. This is the living one, and it is eaten.

The permanence of the material is matched to the permanence of the claim. A memorial is permanent because the thing is gone; the service is perishable because it happens today and again tomorrow.

**WHY THE DIE AND NOT THE MEDAL — this removes Franklin Mint entirely.** A struck bronze medal of your own van is self-regard and the originality lens is right that it is a saturated 1970s category. A carved wooden MOULD of your van is a Mexican object with a five-hundred-year ancestry and needs no defence: the **alfeñique and pan-de-muerto moulds** of the dulcería, carved end-grain, hung in the shop, used at one date a year. That is the lineage, named. Not the Royal Mint. Not FIDEM. **A tool is not a trophy.** And the title finally means what it says.

**THE BADGES COME OUT OF THE HEIGHT FIELD.** `STATE.md`'s inventory names them: `capvw` ×8, `vw_disc`, `vw_ring`. Four hubcap badges fall in a side elevation at 86.9 mm — 5.17 mm each at Ø300 — and they are the only Volkswagen-shaped things on this face. Excluding them from the render is one collection line, and a probe can assert the height field contains zero pixels from any of those names. It clears the trade-dress exposure on a **permanent tool a cease-and-desist cannot revise.** It also makes the object worse to look at, in the right way: a vehicle with its maker's name taken off it, which is literally what a converted food truck is.

**AND WHAT GOES BACK ON IS TACOMBI'S, AT AN AUTHORED HEIGHT.** The flank's identity is paint and paint has zero depth — the feasibility lens is right and a pure Z pass gives you a VW, not this. So the relief is two layers: a MEASURED surface plus an ENGRAVED layer at one constant authored height, driven by the artwork's own alpha — the Señor script, the mural, the menu strip, the calidad burst. That is what an engraver has always done with a painted marking, and the project already has the precedent and the vocabulary for it: **the strip ink (72,46,6) is an AUTHORED darkening of a measured median (91,59,7)**, and Sheet 3's title block says so. The rim says which layer is which. The result inverts the owner-and-brand attack completely — the object now carries every Tacombi mark and no Volkswagen one.

**THE RISK IT STILL CARRIES** — **FIVE THINGS PUT BACK, NAMED, BECAUSE THE DANGER LENS SCORED THIS FALSE.**

**1. THE FUNERARY READING, STRUCTURAL INSTEAD OF CAPTIONED.** The danger lens found the thing the write-up had buried: `MOTOR: NINGUNO · TRANSMISIÓN: VENDIDA` is an epitaph, and a die is how you commemorate. The original then dressed that as a "tone question — charming or pompous." **Striking it CLOSED makes the form agree with the inscription instead of decorating it.** A food truck struck closed is a food truck not serving. It is the van, dead, parked. And it is simultaneously the only configuration in which every dimension is measured — the rigour and the bleakness point the same way for once.

**2. THE BADGES ARE DELETED AND YOU CANNOT UN-SEE IT.** Legally necessary on a permanent tool. Visually violent. A vehicle with its maker's name taken off.

**3. THE REVERSE IS THE SIDE THAT HAS NEVER BEEN PHOTOGRAPHED, STRUCK AT THE SAME FIDELITY AS THE MEASURED SIDE, AND NEITHER FACE SAYS WHICH IS WHICH.** SPEC grades it E; two of its features are both E and mutually contradictory; the owner's own words on it are *"cannot tell from this crop."* You hold a measurement and an inference at identical resolution in identical material and **the only key is on the edge.** The object makes its owner complicit in not knowing. This is not a caption about uncertainty — it is uncertainty as the subject of a face.

**4. THE CONFESSION IS DELETED FROM BOTH FACES.** Early critic 1 is right that it has become a tic and that the programme may own exactly ONE confession object — **and it already does: SHEET 3 OF 4, shipped.** So this one may not be a second. `ALTURA: SIN MEDIR` and `PROFUNDIDAD EXAGERADA · CONSTANTE DECLARADA` are struck out of this concept entirely and handed to THE UNCERTAINTY PLATE, which exists for them. What remains on the rim is a SPECIFICATION — scale, grade, exclusions, source document — in the place a medal has always carried its metal and its mint. **It costs the object something: you can no longer resolve the discomfort by reading the label.** Early critic 2's test — *name one design decision the confession CHANGED* — is answered concretely: it chose the reverse's subject. Without it the reverse is text.

**5. THE ONLY VERSION THAT IS ALIVE IS THE ONE THAT GETS EATEN.** The lid up, the board down, the 115 lamps: chocolate, on a declared pose, destroyed daily.

**AND WHAT IS NOT FIXED, STATED PLAINLY.**

* **THE TONE RISK IS REAL AND CRAFT CANNOT TOUCH IT.** He is entitled to find a carved memorial to his own van insufferable. Re-lineaging it to the dulcería lowers the odds; it does not remove them. **He sees a raking-light render at true size before a gram of anything is cut, and if he winces the concept dies there.** That is the point of the first step.
* **`LADO CIEGO · GRADO E · NUNCA FOTOGRAFIADO` IS STILL, PARTLY, A FACT ABOUT US.** The owner-and-brand lens caught the original telling a paying guest that his contractor never measured the roof, and it was right. I claim this line is different in kind — it is a fact about the photographic record of the vehicle, that no camera was ever on that side — but I will not pretend the distinction is airtight. It is on the EDGE of an object that hangs in his own room, not on a customer's wrapper. **The chocolate's wrapper carries three story lines and nothing else.**
* **STRIKING A GRADE-E INFERENCE IN PERMANENT MATERIAL IS A DELIBERATE DEPARTURE FROM "any single measurement off is unacceptable."** It is declared, it is on the rim, and it is his call — **F330's ceiling binds here: he was asked whether the MODEL is done enough for the sticker, not whether it is done enough to be carved.** This needs its own asking, as multiple choice, with the Ø300 render attached.
* **THE HEIGHT FIELD IS UNMEASURED UNTIL THE PROBE RUNS.** Nothing above is a reading. No `use_pass_z` exists in this tree.
* **THE 150 mm SLAB IS A PROPOSAL.** It may cut the counter nosing off (`STATE.md` puts non-bodywork out to y = 1.173). The probe reports what it clips, by object name, or it is not a probe.
* **THE ENGRAVED ARTWORK LAYER IS AUTHORED HEIGHT.** It has no more claim to being measured than the strip ink does. Declared, on the rim.
* **THE COSTS ARE TRADE ESTIMATES, NOT QUOTES.** Nothing in seventy-eight revisions of this repository has ever been priced. Every figure below is a number to be obtained, and saying otherwise would be the exact defect this project exists to avoid.

**WHAT THE MODEL CONTRIBUTES** — **THIS IS THE STRONGEST MODEL DEPENDENCY IN THE PROGRAMME AND IT IS THE ONE THING ONLY A SOLID CAN DO.** A relief needs DEPTH — single-valued, clean, at a resolution you choose. A photograph has none. Photogrammetry gives noise, and a CNC reproduces noise faithfully. The mesh is closed (**0 non-manifold edges**) and overwhelmingly quads (**229,489 quad, 1,040 tri, 5,186 ngon**), so the height field comes out smooth enough to cut without hand-sculpting.

But the sharper answer is the one the audit forced out:

**ONLY THE MODEL HAS A BLIND SIDE, AND ONLY A MODEL CAN BE ASKED TO SHOW IT.** No photograph in the reference set shows the off flank. The archive cannot produce that face at any price. The model can — and the model's version is graded E, is internally contradictory, and was ruled unresolvable by the owner from the only crop that bears on it. **A medal is the one form in the world with an obverse and a reverse, and this vehicle is the one subject with a measured side and a side nobody has ever seen.** The form and the subject were built for each other and the original filled the second face with text.

The three additions are all one-liners against infrastructure that already exists:

* `use_pass_z` on the existing `side` camera, 32-bit EXR. **One line. It does not exist yet — confirmed by grep, not assumed.**
* A **`-Y` side camera**, `ortho=5.90`, mirroring `studio.views()["side"]`. One dict entry.
* A **collection exclude** for `capvw`, `vw_disc`, `vw_ring` — names already in `STATE.md`'s inventory.

**And it is the SAME infrastructure the line-art keystone needs**, so it is not a cost carried by this concept alone. The engraved artwork layer consumes `line_pass.py`, which SHIPPED at rev 77 (F332) and already takes `--view side`. **It consumes nothing that does not exist: no AO pass, no normal pass, no sun lamp, no interior camera, no glTF export, no bake path.** Early critic 2's capability ledger was written to catch concepts that assume absent capability, and this one is clean against it.

**MEASURED FIGURES** — **THREE CORRECTIONS FIRST, BECAUSE THE AUDIT CHAIN INHERITED ALL THREE (rule 13, rule 34).**

**(1) `BAY_DEPTH = 0.42` IS NOT THE SERVING APERTURES. RETRACTED.** `t1_shell.py`: *"BAY_DEPTH = 0.42 # forward of the tail skin. NOT MEASURED"*, inside `def trunk_bay()` — *"A plain lining behind the engine lid, so the bay is not a void."* It is the TRUNK BAY at the TAIL, running along X, and in a side elevation it is edge-on and invisible. The original's risk (2) — *"how deep the three serving holes read … `BAY_DEPTH` is a pose choice"* — is about the wrong object, and the feasibility lens then printed `serving aperture (BAY_DEPTH 420 mm)` at the head of its decisive table. **The most-quoted number in the whole audit is attached to a part of the vehicle that is not in the picture.**

**(2) THE APERTURES ARE 1354.8 mm DEEP, NOT 420, AND THAT IS MEASURED GEOMETRY.** The Z pass looks through them into a built galley. Show flank at half of `STATE.md`'s measured body width **1.7497 → +874.85 mm**; galley backdrop `GAL_Y_BACK = −0.4800` (`t1_detail.py`, *"backdrop plane"*). **874.85 + 480.0 = 1354.8 mm.** Against `STATE.md`'s full-Y span [−1.0637, +1.1500] = **2213.7 mm**, the three holes eat **61.2 % of the entire depth budget.** That is the actual diagnosis behind "the medal is a blob" — and it is a clipping decision, not a physics limit.

**(3) THE FEASIBILITY TABLE MIXES TWO AXES.** *"wheel arch lip to tyre gap (39.7 mm) → 21.5 micron"* — the arch/tyre gap is an XZ, IN-PLANE feature. Depth compression cannot touch it. **A relief has two independent resolutions and only one of them is compressed.**

**THE TWO RESOLUTIONS, SEPARATED.**

| | Ø55 (rim 3, field Ø49) | Ø300 (rim 12, field Ø276) |
|---|---|---|
| in-plane scale | **1:94.6** | **1:16.8** |
| vehicle, closed | 43.0 × 23.5 mm | 242.1 × 132.6 mm |
| serving aperture 515.5 × 403.0 | 5.45 × 4.26 | **30.68 × 23.99** |
| tyre 664.9 | 7.03 | 39.58 |
| hubcap 274.0 | 2.90 | 16.31 |
| badge 86.9 | 0.92 | 5.17 *(deleted)* |
| **shut line 5.5 mm wide** | **0.058 mm** | **0.327 mm** |

**⚠ THE ORIGINAL'S OWN HEADLINE FIGURE DOES NOT FIT. "1:81.3, 4065 mm across a 50.0 mm relief field" ignores the vehicle's height: a 50.0 × 27.4 mm rectangle has a 56.9 mm diagonal and will not go inside a Ø55 blank, let alone inside a rim.** Corrected to 1:94.6.

**AND THAT SETTLES THE SIZE BY ARITHMETIC RATHER THAN TASTE.** A fine ball-nose tool is 250–500 µm. At Ø55 a shut line is **58 µm wide — narrower than the cutter**, so at Ø55 the flank's fine detail cannot be cut at any depth budget whatsoever. At Ø300 it is **327 µm and cuts.** *The feasibility attack is correct at Ø55 in bronze, and it is precisely the reason the object is Ø300 in wood.*

**DEPTH BUDGET, THE THREE SCHEMES.**

```
  scheme                                  RAIL_PROUD 21.3mm   shut line 5.5mm
  full span 2213.7 mm -> 1.2 mm (1:1845)       11.5 um             3.0 um
  150 mm clipped slab -> 1.2 mm (1:125)       170.4 um            44.0 um
  150 mm slab -> 8 mm, wood   (1:18.75)      1.136 mm           0.293 mm
```

**THE CLIP ALONE BUYS 14.8×, AND IT IS ONE LINE.** Clipping the height field 150 mm behind the near skin drops the apertures to the floor — they become three voids of flat shadow at full relief depth, which is what they should be — and hands the whole budget to the body. **At Ø300 in wood the naive linear map then works and no Poisson solve is needed at all.** Gradient-domain compression (Weyrich et al., SIGGRAPH 2007) stays in reserve for Ø55 only, and the probe says whether it is needed.

**CEILINGS ON ALL OF THE ABOVE.** Every depth figure is arithmetic on constants, **not a reading off a Z pass, because no Z pass exists** — `grep -rn "use_pass_z" *.py` returns nothing; the only pass anywhere is `probe_ctan_index.py`'s `use_pass_object_index`. **The V-swage's proudness in Y is in no file I can find and is NOT quoted here.** The 150 mm slab is a proposal to be measured, not a measurement. 5.5 mm for a shut line is the record's own figure (`SPEC.md`, rev-7 entry) and is one line, not a survey. Tool radii and legible-step figures are trade knowledge, not measurements off this tree.

**AND THE CAMERA IS ALREADY THERE, WHICH IS WHY THE REVERSE IS FREE.** `studio.py`: `"side": loc=(0.0, 26.0, 1.52), ortho=5.90` fits; `"front"` and `"rear"` are `ortho=3.55` and clip. The original concluded "one face only." **But the second face is not front or rear — it is the OTHER FLANK, and it is the same camera at y = −26.0 with the same `ortho_scale`, because the XZ extents are identical from either side.** Nobody noticed the reverse was already paid for.

**COST / FEASIBILITY** — **ALL FIGURES ARE TRADE ESTIMATES. NOT ONE IS A QUOTE. This repository has never priced anything and I am not going to publish a cost as though it were a measurement.**

| object | tooling | unit | MOQ | lead | status |
|---|---|---|---|---|---|
| **Ø300 hand-carved end-grain die** | **none** | **US$150–400 one-off** | **none** | 2–4 wk | **SHIPS FIRST** |
| Ø300 CNC'd MDF/plaster, bureau | none | US$60–150 | none | 3–7 d | fallback / mock |
| Ø55 polycarbonate mould, 21 cav. | US$400–900 | — | none | 3–5 wk | second |
| chocolate unit | — | ~US$0.90–1.60 landed | ~500 | — | given with check |
| Ø55 struck bronze | US$2,500–5,000 | US$8–14 | 200–500 | 4–6 mo | **YEAR TWO** |
| 3D-print bureau, Ø55 + Ø300 | none | US$20–60 | none | 2–5 d | this week |

**THE ORDER-OF-MAGNITUDE ATTACK IS ANSWERED BY DELETING THE EXPENSIVE OBJECT FROM YEAR ONE.** The original made the wall showpiece a hardened steel die and a small striking house. It is now a carved hardwood mould from a trade that has done exactly this for five centuries: **no tooling, no MOQ, no minimum, no supply chain, and it is the showpiece rather than a step toward one.** Against *"we need to finally present something"*, the deliverable is one object, in one pair of hands, at a cost below a single enamel sample.

**SELL-THROUGH, HONESTLY:** the Ø300 die is **not for sale**. It hangs in the room. The chocolate is **not sold** — it is given with the check, which is where the programme's warmth actually lives and where early critic 1's "what leaves the counter in a customer's hand" gets a real answer. **So the year-one revenue of this concept is zero and I am not going to dress it otherwise.** What it buys is a physical object of the model, on a wall, that no photograph could have produced — and a reason for a customer to turn something over in their fingers at the end of a meal.

**THE FEASIBILITY LENS'S REMEDY 1 IS ADOPTED VERBATIM AND IS THE FIRST DELIVERABLE.** `probe_rev78_relief.py`: render the side Z pass, **PAINT the mask and look at it before publishing any number from it (rule 8)**, and print the per-feature depth histogram against a declared tool radius and a declared minimum legible step, under all three compression schemes. It must report which objects the 150 mm clip removes, **by name**. It must be **WATCHED REFUSING on a flat plane and on a Z pass with the near skin clipped away (rule 3)** before any figure off it is believed. If the probe says the body is still microns after clipping, it says so in its own summary line and **the concept is re-scoped on a measurement instead of a hope, or it dies.** Half a day. No fabrication. It is the cheapest thing in the programme that can kill or save an idea.

**WHAT I CONCEDE OUTRIGHT TO THE ORIGINALITY LENS.** The technique is not a discovery and I am not claiming it: **Cignoni, Montani & Scopigno, "Computer-Assisted Generation of Bas- and High-Reliefs" (J. Graphics Tools, 1997)** founded it; **Weyrich et al., "Digital Bas-Relief from 3D Scenes" (SIGGRAPH 2007)** is the modern treatment, and the field exists precisely because naive range compression fails — which the arithmetic above independently reproduces. ArtCAM, Aspire, JewelCAD and ZBrush all ship height-field-from-3D, and mints have run scan-to-relief-to-CNC since the late 1990s. **"Render the side ortho, invert, cut" is what a sign shop does on a Tuesday, and I have removed that sentence.** Nearest existing objects, named as early critic 1 requires: **Mexican alfeñique / pan-de-muerto moulds** (carved end-grain, 18th c. onward) for the form and the lineage; **FIDEM** contemporary art-medal practice for the register; **Franklin Mint / Danbury Mint automotive series** for the trap this concept is now built to avoid. **The claim is the subject, not the method: a vehicle carved closed, badgeless, with its unphotographed side on the back.**

**FIRST SHIPPABLE STEP** — **NOTHING IS CUT THIS WEEK. HE GETS THE OBJECT ON A SCREEN AT TRUE SIZE, AND THE ARITHMETIC UNDER IT.** No printer, no bureau, no supplier, no money — this repository has never had a printer or a router and the original's "grey plastic medal in his hand inside twenty-four hours" quietly assumed both.

**DAY 1 — three one-line changes, no render queue running.**
1. `use_pass_z` on the existing `side` camera; 32-bit EXR. Confirmed absent today.
2. A `side_off` view in `studio.views()`: `loc=(0.0, -26.0, 1.52)`, `ortho=5.90` — the mirror of the `side` entry.
3. A collection exclude for `capvw`, `vw_disc`, `vw_ring`, with a build-log line naming what was dropped.

Then render both flanks **CLOSED** — `TRUNK_OPEN_DEG=0`, lids down, board stowed.

**DAY 2 — `probe_rev78_relief.py`, and it must fail before it may pass.** Paint the mask, look at it, then print the per-feature depth budget under full-span / 150 mm clip / gradient-domain, against a declared tool radius. Report by object name what the clip removes. **Watch it refuse on a flat plane and on a clipped-away skin.** Publish the numbers WITH the ceiling that the slab depth is a proposal.

**DAY 3 — THE THING HE ACTUALLY LOOKS AT.** One PDF, two pages, no words on the artefacts themselves:

* **Page 1: the Ø300 die, both faces, side by side, at true size**, rendered under raking light from the clipped height field — obverse *lado de servicio*, reverse *lado ciego* — with the incuse rim line set around the edge. He can hold a 300 mm ruler to his screen.
* **Page 2: the Ø55 chocolate**, open pose, at true size, beside its wrapper flat.

**DAY 4 — ONE QUESTION, MULTIPLE CHOICE, WITH THAT PDF ATTACHED, ASKED WITH THE QUESTION TOOL.** Not "do you like it." One crop, one mark, one sentence:

> *The back of this object is the side of the bus that no photograph we hold shows. The model's version of it is graded E, two of its features contradict each other, and when you were shown that flank you said "cannot tell from this crop." Do you want it (a) struck anyway, marked GRADO E on the edge only, (b) left a blank tool-marked field with one line of text, or (c) not made?*

**He has never stood in this vehicle and he must never be asked what the real one looks like — he is being asked what he wants a permanent object to claim.** That is a question the figures can support.

**If he answers (a) or (b), the carving brief goes out in week two** — one PDF, one STL, one rim line, to a mould-carver. **If he answers (c), the chocolate proceeds alone and the die is dead**, which is a real result and costs four days.

**HOW IT ANSWERED THE FOUR LENSES** — **FEASIBILITY — attack 1, the relief budget.** *Correct arithmetic, wrong constant, and the conclusion inverts.* `BAY_DEPTH` is the trunk-bay lining at the tail (`t1_shell.py`, `def trunk_bay`), not the apertures; the apertures are **1354.8 mm** deep to `GAL_Y_BACK = −0.4800`, which is **61.2 %** of the 2213.7 mm span and is the whole reason the body was microns. Clipping to a 150 mm slab buys **14.8×** in one line. And the table mixes axes: the 39.7 mm arch/tyre gap is IN-PLANE and is **0.488 mm at Ø55**, not 21.5 µm. **Where the attack fully binds is WIDTH, not depth: a 5.5 mm shut line is 58 µm across at Ø55 — narrower than any ball-nose tool — so it cannot be cut at Ø55 at any depth budget. That is why the object is Ø300, where it is 327 µm and everything reads under a plain linear map.** Weyrich cited and held in reserve for Ø55 only. Probe adopted verbatim, with a painted window and two watched kills.

**FEASIBILITY — attack 2, paint has zero height.** *Binds completely and is unanswerable inside a Z pass.* Answered outside it: a second, ENGRAVED layer at one constant AUTHORED height off the artwork alpha and `line_pass.py`, declared as authored on the rim, with the strip ink (72,46,6) from a measured median (91,59,7) as the record's own precedent for exactly this move. It also inverts the owner-and-brand attack that the relief deletes every Tacombi mark.

**ORIGINALITY — attack 1, a 28-year-old paper.** *Conceded entirely and cited by name* (Cignoni et al. 1997; Weyrich et al. 2007). "Render the side ortho, invert, cut" is deleted. The claim is the subject, not the method.

**ORIGINALITY — attack 2, Franklin Mint.** *Taken, and its own remedy adopted.* **Ship the die, not what the die makes**, and re-lineage from the mint to the dulcería: carved end-grain, alfeñique and pan-de-muerto, not Belgian polycarbonate as the hero. Franklin Mint is a proud portrait of a car with its badges polished; this is a van struck closed with its badges deleted. The title now means what it says.

**OWNER-AND-BRAND — attack 1, the reverse confesses about the project.** *Taken.* `ALTURA: SIN MEDIR` and `PROFUNDIDAD EXAGERADA` are struck from this concept and handed to THE UNCERTAINTY PLATE. Both faces are wordless; the rim carries a specification. The residual — `GRADO E` — is flagged in the risk section as only partly a fact about the vehicle, and it is on an object that hangs in his own room, never on a customer's wrapper.

**OWNER-AND-BRAND — attack 2, trade dress on a permanent tool.** *The strongest attack in the set and the fix is subtractive.* `capvw` ×8, `vw_disc`, `vw_ring` excluded; the badges (86.9 mm, 5.17 mm at Ø300) do not exist in the height field; `SIN EMBLEMAS` on the rim; a probe asserts it. The nose roundel was never in a side elevation — correctly excluded by camera, and now said so rather than left implied.

**OWNER-AND-BRAND — attack 3, it maximises VW and minimises Tacombi.** *Inverted by the engraved layer plus the badge deletion.* Every mark on the object is now Tacombi's and none is Volkswagen's.

**OWNER-AND-BRAND — attack 4, the tail board's unresolved pose.** *Taken, and it exposed an internal contradiction in the original: it quoted 4065 mm — `STATE.md`'s CLOSED length — while striking an open board.* **Struck closed. No unmeasured pose survives on the permanent object.** Cost stated: the mural, the board and the 115 lamps exist only in chocolate.

**OWNER-AND-BRAND — attack 5, MOQ and year two against "present something."** *Taken.* The steel die and the striking house are out of year one; a carved hardwood die has no tooling and no MOQ; the bronze medal is explicitly deferred and not costed in.

**OWNER-AND-BRAND — attack 6, F331.** *Declared: ADULT.* And declared negatively too — the chocolate is given with the check, to the person paying, and **must not be counted as the children's item. The children's line is owed a different object and this is not it.**

**DANGER — attack 1, the reverse is the safe choice.** *The best note in the set and it is now the object.* The reverse is the blind side: no apertures, cargo-door shut lines, still a van — grade E, mutually contradictory features, *"cannot tell from this crop."* Struck at identical fidelity to the measured face with nothing on either face to distinguish them.

**DANGER — attack 2, the caption converts a defect into a credential.** *Taken; the caption is deleted.* And the exaggeration is made visible instead, exactly as prescribed: the clip pushes the three apertures to full relief depth so they read as caves and the object could never be mistaken for a survey.

**DANGER — attack 3, the Z pass sees through into the galley.** *Correct, and now quantified at 1354.8 mm / 61.2 %.* The uglier answer is adopted: the taqueria's three windows become three voids of flat shadow.

**EARLY CRITIC 1 — the confession tic; one object per object; no prices.** All three taken: **SHEET 3 is the programme's one confession object and this concept stands down from being a second**; the die is the single owner of "the vehicle as a solid"; five cost lines are given with the ceiling that not one of them is a quote.

**EARLY CRITIC 2 — "name one design decision the confession CHANGED."** It chose the reverse's subject. Remove it and the reverse is text, which is what the original was.

**WHAT I COULD NOT ANSWER.** The tone risk. A man may find a carved memorial to his own delivery van insufferable, and no amount of lineage fixes that. It is why day 4 is a question and not a purchase order.

### GRACIAS POR SU PREFERENCIA (1524.7)  ·  LINE: adult

**REGISTER** Motion, hand-drawn line, room sound, and the food-and-hand-off — plus one register this project has never had in 78 revisions: HUMAN GEOMETRY. Deadpan-catalogue: the title is a Mexican receipt phrase and the parenthesis is the camera height in millimetres above ground.  
**ARTEFACT** **THE FILM.** 16 s, 2062 × 1612 px, looping. One shot, locked, from 382.2 mm inboard at 1524.7 mm above ground, 26.7 mm-equivalent lens. Delivered as a silent-safe MP4 and a ProRes master. Room sound only — plancha, a bottle cap, coins on the slab, the fringe moving. No music, no voice.

**THE MACHINE HALF**, rendered from the model as vector line and flat colour: the aperture's rounded rectangle (515.5 × 403.0, r 55, three of them and equal — this is the middle one), the 65 bobbles, the counter's true section at the sill (107.0 mm slab, 321.0 mm plan depth, standing 291.0 mm proud of the 875 mm half-width), and the gold where the edge turns down.

**THE HAND HALF**, drawn: 192 drawings, six hand-off cycles, one named illustrator.

**THE END CARD.** ONE caption in sixteen seconds, and it is a provenance ledger in the project's own grade vocabulary — MEASURED / INFERRED / AUTHORED / CONSTRUCTED — with the last line reading:

```
    SKIN   #<hex>   CONSTRUCTED — NOT RECOVERABLE FROM WHAT WE HOLD
                    chosen by <illustrator, by name>
```

**THE PHYSICAL OBJECT.** A 24-page flipbook, 90 × 60 mm, one ink, of a single hand-off. Adult line — a flipbook of hands is not a children's product because it flips, and I am not claiming the children's slot with it.

**AND ONE THING THAT SHIPS INTO THE REPOSITORY, NOT INTO THE FILM: THE COOK PROXY.** A blocked-in torso-and-forearm volume, standing on `van_floor`, at a declared height. The project's **first human geometry in 78 revisions.** It exists so the shadow across the slab is *sampled* rather than invented, and it discharges rule 55 in the same edit.

**THE OLD THESIS IS DEAD. I KILLED IT MYSELF.** "The seam between a machine-true aperture and a hand-drawn hand is the film" is PAPERMAN (2012), and then it is SPIDER-VERSE and every film after it. The originality lens was right and there is no version of that sentence worth keeping. Here is what replaces it, and it is a thing only this asset can say.

**THE CAMERA BELONGS TO THE HOLE. IT IS NOBODY'S EYE, AND THAT IS MEASURED.**

The feasibility lens proved the written camera impossible and it was right: `van_floor`'s top at the middle bay is **511.2 mm** above ground, the aperture head is **1726.2 mm**, so the head rail is **1215.0 mm above the floor the cook stands on**. Every adult eye is above that. A standing cook does not look *through* this hole — he looks *down over* it. "A locked camera at the cook's eye looking out" cannot be shot on this vehicle. Refuted, accepted, gone.

So the camera goes where the aperture's own centre is: **1524.7 mm above ground, 1013.5 mm above the cook's floor, 201.5 mm below the head rail.** That station is the cook's chest and the customer's chin. **It is the eye-height of no one who has ever stood at this window.** The film has no point-of-view character. It is not the cook looking out at customers, which is extractive, and it is not the customer looking in at staff, which is tourism. It is the hole, which has served both for years and has no opinion about either.

**AND THE STATION IS A NUMBER NOW, NOT A POSE.** The lens's third attack — that the film's spine vanishes at an undeclared distance — was exact. `CNT_ZT` sits **118.0 mm below the sill**, so the sill lip occludes the slab, and the visible slab band collapses as the camera retreats inboard. I re-derived the sweep independently and it reproduces:

```
    camera inboard of the flank plane y=0.8750     visible slab band
        0.3000 m                                       115.3 mm
        0.3500 m                                        86.0 mm
        0.3822 m   <- DECLARED STATION                  67.2 mm
        0.4000 m                                        56.8 mm
        0.4500 m                                        27.5 mm
        0.4933 m   <- THE FILM DIES HERE                 2.1 mm
```

**The station is 382.2 mm inboard, chosen because it lands the slab at exactly 67.2 mm — the bottom sixth of a 403.0 mm frame — which is what the concept always claimed and never derived.** The film has **111 mm** of travel before its own spine leaves the picture. That is the ceiling and it is printed.

**AND THE STATION IS EMPTY — I CHECKED THE MESH RATHER THAN ASSUMING.** At (x 0.0470, y 0.4928, z 1.5735) the nearest geometry in the whole tree is `gal_appliance` at **211.1 mm**. The camera fits, with room, and no one had established that. From there the hole subtends **68.0° × 55.6°** — a **26.7 mm lens on a 36 mm frame** — and the frame is the hole: **2062 × 1612 px at 4 px/mm, corner radius 220 px.**

**WHAT THE FILM IS.** Sixteen seconds, one shot, six hand-offs, drawn on twos, looping. You never see a face. **Not for consent reasons — because the geometry forbids it.** At 1524.7 mm the customer's head is above the head rail and out of frame; the cook's head is behind the camera. What crosses the picture is hands, forearms, a sleeve, paper, coins, and one wrapped thing. The vehicle wrote the shot list.

The locked camera is not a cinemagraph borrowing. **The camera is locked because the aperture is a hole in sheet metal and cannot move.** It is the subject's own property, not a style.

Across the top and down both sides hangs the bobble fringe — **65 balls per aperture, counted as loose parts in the built mesh, not read off a comment**, at 9.0 mm radius and 26.0 mm pitch. It is Tacombi-specific, it is in `ref_side.jpg`, and it is the one thing in frame that is unmistakably HIS.

Across the bottom sixth: the slab, and the gold. **And here the feasibility lens landed its cleanest hit, which I am not going to paper over.** `CNT_NOSE_F` = 0.186 ± 0.021 of the slab edge was measured on `ref_side.jpg` over 113 columns — an **OUTSIDE elevation, square-on** — and corroborated at 0.191 on `ref_rear34.jpg`. **19.9 mm is the elevation extent of the gold seen from outside. It is NOT what this camera sees.** From inside and above you are looking down onto the *crown of the roll*, which sits at 0.20h below the slab top, not at its face at 0.62h. **The apparent width of the gold from this station has never been measured and this film may not print 19.9 mm as though it had.** The projection, 7.0 mm, is INFERRED — the source says so verbatim: an elevation cannot measure a Y offset. So the gold is drawn as what it will actually be: a hard bright line where the slab's edge turns down. Better image, honest label.

**THE HANDS.** Drawn by a person, on twos, in the vehicle's palette — menu yellow **(172, 144, 17)**, the strip ink **(72, 46, 6)** which is AUTHORED from a measured median **(91, 59, 7)**, and the carried red, cream and gold. *(The old concept called (172,144,17) "strip yellow". It is the MENU yellow. Corrected here.)*

**AND THE SKIN, WHICH IS THE WHOLE POINT AND WHICH THE OLD VERSION DODGED.** See the risk section. It is printed, it is named, and it is credited.

**THE RISK IT STILL CARRIES** — **THE DANGER LENS SAID IT WAS SANDED OFF. HERE IS WHAT I PUT BACK, ITEM BY ITEM.**

**1. THE SKIN INK IS PRINTED, ON THE OBJECT, WITH A PERSON'S NAME NEXT TO IT.** The old version said there was no honest way to abstain and then abstained — six inks, none of which can draw a hand. Now the film carries **one flat skin ink, named in hex on the end card**, in the same row and the same type size as every measured colour, labelled in the project's own vocabulary: **CONSTRUCTED — NOT RECOVERABLE FROM WHAT WE HOLD**, followed by the name of the illustrator who chose it.

**And this confession CHANGES A DECISION, which is the test the completeness critic set for the forty objects that print their uncertainty as decoration.** It changes the credit block from a machine provenance list into a named human author, and it changes the hire: the illustrator is engaged as a **colour author with a credit**, not as work-for-hire hands. If the caption were removed, the fee and the credit would still have to be different. That is the difference between honesty and a caption about honesty.

**2. ONE SKIN INK FOR EVERY HAND IN THE FILM — COOK AND CUSTOMER ALIKE.** Sixteen seconds, six hand-offs, and you cannot tell staff from customer by colour. **This can be read two ways and I am not hedging it.** It can read as the film's argument — that the counter is the only thing separating the two, and it is 107.0 mm thick. It can equally read as erasure of exactly the difference the brand trades on. **That risk is not resolved. It is the decision the film makes and it should be put to the owner in those words.**

**3. NO FACES, AND THE REASON IS PUBLISHED AS GEOMETRY.** This is the piece's sharpest edge and also its most attackable. Someone will say the geometry is a convenience — that the film wanted the consent problem to go away and found a measurement that made it disappear. **They will have a point.** The answer is that the measurement came first and refuted the written camera; the no-faces rule is a consequence, not a motive. **But the reading is available and stating it here is the only defence that does not depend on being believed.**

**4. THE COOK PROXY IS THE PROJECT'S FIRST HUMAN FORM AND IT IS UNMEASURED BY CONSTRUCTION.** A repository that measures a tail board to 0.1 mm and refuses to publish a bumper bow because it cannot be recovered from the frames it holds will now contain **a guessed human body**, standing on `van_floor`, casting a real sampled shadow across a measured slab. That is genuinely uncomfortable and it is meant to be. **The seam is then IN THE RENDER — a measured machine and a guessed body sharing one occlusion pass — instead of in a caption.**

**5. THE THINGS THAT ARE STILL SIMPLY WRONG OR MISSING, NAMED.**
- **The AO pass does not exist and neither does a normal pass.** Until both are built, the shadow claim is unbuilt and the film is line-only. **Not a caveat: a blocker on the hero element.**
- **Nobody in this project has ever drawn food.** No taco exists as a mesh; the `plancha` is a bare slab that has never had anything on it. A badly drawn taco kills sixteen seconds stone dead and no measurement protects against it.
- **The money question is unresolved.** Cash crossing reads as an advertisement; no money crossing reads as fantasy. Pick one in the first drawing, not in the edit.
- **This film cannot advance the emblem.** The camera is inside looking out; the VW roundel is in no frame. **F191's hold is untouched and this does not pretend otherwise.**
- **It will not match the rest of the programme.** It is warm, and the austerity will look colder next to it.
- **THE TRADE-DRESS QUESTION IS UNANSWERED PROGRAMME-WIDE AND THIS OBJECT DOES NOT ESCAPE IT.** The film is less exposed than a printed T1 silhouette — a hole, a fringe and a gold line are not obviously a Volkswagen — but the flipbook is a saleable object and nobody has taken one page of IP advice. **That is cheaper than one day of the illustrator's time and it should happen before the hire, not before the render.**

**WHAT THE MODEL CONTRIBUTES** — **THE MODEL IS NOT SET DRESSING HERE. IT WROTE THE SHOT AND IT REFUTED THE FIRST DRAFT OF IT.**

Without the model, "a locked camera at the cook's eye looking out through the serving window" is a sentence a director writes and an illustrator draws, and it is **impossible on this vehicle** — the head rail is 1215.0 mm above the floor and the eye is above the rail. **Nothing but the mesh could have said that.** No photograph we hold shows the interior. No measurement in `SPEC.md` bounds it. It took a built floor, a built head rail and a subtraction.

Without the model, "the counter runs across the bottom sixth" is a compositional preference. With it, it is a station: **382.2 mm inboard, or the slab is 115.3 mm and the composition is wrong, or 493.3 mm and the counter, the gold and the surface the hands rest on are all gone.** The model does not decorate that decision; it is the only thing that can make it.

Without the model there is no way to know the camera **fits** — that at (0.0470, 0.4928, 1.5735) the nearest object in a 229-mesh galley is 211.1 mm away.

And the pipeline that draws it **already exists and shipped this revision**: `line_pass.py` takes `--view` and resolves it through `studio.views()`, so the interior camera is **one dict entry in a table that already holds ten**. Restricting the pass to the aperture ring, counter, nosing and fringe uses the exact route F332 established for `la_rueda` — `source_type='OBJECT'` over a joined duplicate, because `COLLECTION` is a silent no-op. **That is a precedented mechanism, not new infrastructure.**

**WHAT THE MODEL CANNOT DO, STATED WITH THE SAME FORCE.** It contributes **nothing to the hands** and it must not. It contributes nothing to the food. It cannot supply the skin. And **the occlusion it is supposed to supply does not exist yet** — no AO pass, no normal pass, no body. The old concept called the sampled shadow "the part no illustrator can fake" while the tree contained no human geometry at all. **That claim was false and it is now a costed job instead of a boast.**

**MEASURED FIGURES** — Every figure below was read off this tree at this commit, in a build I ran, not transcribed from the concept.

**THE CAMERA, AND THE ARITHMETIC THAT FORCED IT**
- `van_floor` top at the middle-bay station (x 0.047): **511.2 mm AG** (authored z 0.560, minus rake_drop(0.047) = 48.76 mm)
- aperture head **1726.2 mm AG**, sill **1323.2 mm AG**, band height **403.0 mm** (`Z_SILL/Z_HEAD` 1.3720/1.7750)
- **head rail 1215.0 mm above the cook's floor** — so a standing adult's eye is above it. THE WRITTEN CAMERA IS REFUTED.
- aperture centre **1524.7 mm AG = 1013.5 mm above that floor, 201.5 mm below the head rail.** The height of nobody.
- station **382.2 mm inboard** of the flank plane y = 0.8750, i.e. y = +0.4928
- **nearest mesh to that point in the entire tree: `gal_appliance` at 211.1 mm.** The station is empty — measured, not assumed.
- hole subtends **68.0° H × 55.6° V** → **26.7 mm on a 36 mm frame**

**THE OCCLUSION SWEEP** (`CNT_ZT` is **118.0 mm** below `Z_SILL`, so the sill lip cuts the slab)
- 0.3000 m → 115.3 mm · 0.3500 → 86.0 · **0.3822 → 67.2** · 0.4000 → 56.8 · 0.4500 → 27.5 · **0.4933 → 2.1**
- the film has **111 mm** of camera travel before its spine leaves frame

**THE APERTURE AND ITS TRIM**
- **515.5 × 403.0 mm, r 55, THREE, EQUAL** (`BAY_W` 0.5155, `BAY_CX` 0.6720 / 0.0470 / −0.5980) → 2062 × 1612 px at 4 px/mm, r = 220 px
- fringe: **65 bobbles per aperture, counted as connected components of the built `fringe1` mesh** (1732 verts, 26.6 verts/ball); `FRINGE_R` 9.0 mm, pitch 26.0 mm, inset 13.0 mm. ⚠ CEILING: radius and pitch are **INFERRED** — each ball is ~2 px in `ref_side.jpg`. The COUNT is measured off the mesh; the mesh's ball size is not.

**THE COUNTER**
- slab **107.0 mm** thick (`CNT_ZT/CNT_ZB` 1.2540/1.1470), top **1205.2 mm AG** at this station
- **321.0 mm** plan depth (`CNT_Y_IN/CNT_Y_OUT` 0.8450/1.1660), standing **291.0 mm proud** of the 875 mm half-width
- gold: `CNT_NOSE_F` **0.186 ± 0.021 of the slab edge = 19.9 mm in elevation**, measured over 113 columns of `ref_side.jpg`, corroborated at **0.191** on `ref_rear34.jpg`. ⚠ **RULE 38 CEILING, AND IT BINDS: that is an OUTSIDE ELEVATION. This camera looks down onto the roll's crown (0.20h) not its face (0.62h). The apparent gold width from this station is NOT MEASURED.** Projection 7.0 mm is INFERRED — an elevation cannot measure a Y offset.

**PALETTE** — menu yellow **(172, 144, 17)**; strip ink **(72, 46, 6)**, AUTHORED from a measured median **(91, 59, 7)**.

**WHAT IS NOT MEASURED AND CANNOT BE**
- **Skin. No measurement of any person exists in this repository.** The early completeness critic established that the humans several concepts described — the magenta puffer coat, the eater in the red shirt, "seven real people" — **are not in the record at all.** So the skin ink is not a measurement waiting to be taken. **It cannot be recovered from what we hold.**
- **The AO pass does not exist.** No normal pass either. The occlusion half of the owner's own locked style sentence is unbuilt.
- **No human geometry exists.** 229 mesh objects — `seat_back`, `seat_base`, `pedal_a`, furniture with no occupant — and no torso, arm or hand anywhere.
- Crease angle 40° in `line_pass.py` is a **POSE CHOICE**, and the module says so in its own log line.

**COST / FEASIBILITY** — **Every figure here is an ESTIMATE, not a quote. Nothing in this repository has ever carried a price and I am not going to be the first to invent one and print it as measured.**

**THE MACHINE HALF — days, not weeks, and mostly already paid for.**
- One camera entry in `studio.views()`: **one line.** The table already holds ten.
- The joined-duplicate source for the line pass: **the `la_rueda` route, already written and shipped.**
- Line pass at the new view: **~25 s a run.**
- **THE AO/NORMAL PASS: A REAL SESSION-SCALE JOB, AND IT IS THE HERO ELEMENT'S BLOCKER.** Not an afternoon. It is the unbuilt half of the owner's own locked style sentence and it gates any occlusion claim in the whole programme, not just this film.
- **THE COOK PROXY: a second session-scale job**, and the project's first human geometry.

**THE HAND HALF — this is the cost and it is a hire.**
- 16 s at 24 fps on twos = **192 drawings**; six hand-off cycles of ~32 each, plus inbetweens and clean-up.
- One illustrator, **3–4 weeks**. At a plausible NY rate of $60–110 per finished, cleaned drawing that is **≈ $11.5k–21k**, against the concept's original $8–15k. **The original estimate was low and I am raising it rather than defending it.**
- **The colour-author credit is part of the fee, not a courtesy.**

**THE FLIPBOOK.** 24 pp, 90 × 60 mm, one ink, saddle-glued. Short-run printers typically want **MOQ 250–500**; **~$2–4 landed each at 500**, i.e. **$1k–2k for the run.** It is the cheapest object in the whole bench and it exists the moment the drawings do.

**THE ORDER, AND IT IS THE POINT.** The A4 card costs one afternoon of machine time and one sitting of drawing. **The owner says yes or no to a $15–25k commitment on the strength of it, before anyone is hired.** If he says no, the total spend is one afternoon.

**AND ONE THING THAT IS NOT OPTIONAL AND COSTS ALMOST NOTHING: ONE PAGE OF IP ADVICE ON THE FLIPBOOK BEFORE THE HIRE.** The completeness critic's top finding was that the entire merchandise programme sits on a third party's trade dress and exactly one concept of fifty noticed. This film is among the least exposed objects in the pool, but "least exposed" is not "checked".

**FIRST SHIPPABLE STEP** — **ONE A4 CARD, PRINTED, TWO SIDES, IN HIS HANDS THIS WEEK. He answers it in two seconds on the front and understands it in thirty on the back.**

**FRONT — frame one of the film, at exactly 1:4 of the true aperture.**
- **128.9 × 100.8 mm** (515.5 / 4 × 403.0 / 4), **corner radius 13.75 mm**, gold line **5.0 mm**.
- The **machine half is real**: rendered through `line_pass.py` at the new interior view — one dict entry in `studio.views()`, one joined-duplicate source, ~25 s. The aperture, the 65 bobbles, the slab edge, the gold at the turn-down.
- The **hand half is one pair of hands and one wrapped item**, drawn in a single sitting, in the constructed skin ink — **with the hex printed in the margin and the illustrator's name under it.**

**BACK — the section that proves the camera, because the camera is what nearly killed this concept.**
- The sight line through the middle bay, to scale: **floor 511.2 · slab top 1205.2 · sill 1323.2 · CAMERA 1524.7 · head rail 1726.2**, all mm above ground.
- The band sweep as a table — **115.3 / 86.0 / 67.2 / 56.8 / 27.5 / 2.1 mm** — with 382.2 mm ringed and 493.3 mm marked **THE FILM DIES HERE**.
- **One sentence, set large:** *"The head rail is 1215.0 mm above the floor the cook stands on. He looks down through this hole. So the camera is not his eye — it is the hole's, at 1524.7 mm, which is nobody's."*
- One line at the foot: **SKIN — CONSTRUCTED, NOT RECOVERABLE FROM WHAT WE HOLD.**

**THE QUESTION TO ASK WITH IT, AS MULTIPLE CHOICE, ONE CROP AND ONE SENTENCE — and it is about the danger, not the drawing:** *"Every hand in this film is one flat colour, staff and customer alike. (a) Right — that is the film. (b) Wrong — staff and customers should read differently. (c) I can't tell from this card."* **Option (c) must be on it: if he cannot tell, the card is the defect, not his answer.**

**IF HE SAYS YES**, the second step is a **12-drawing flipbook of one hand-off** — a fortnight, and a physical object in his hand — while the AO pass and the cook proxy are built in parallel. **Neither of those two jobs blocks the card, and the card blocks the hire.**

**HOW IT ANSWERED THE FOUR LENSES** — **FEASIBILITY (2/4) — its four attacks were all correct and all four are now answered with numbers.**
1. *The viewpoint does not exist.* **CONCEDED ENTIRELY.** Re-derived: head rail 1215.0 mm above the floor. The cook's-eye camera is gone and the film no longer claims one. The camera is the aperture's own centre, 1524.7 mm AG, and it is named for what it is.
2. *It declares the refutable thing unmeasurable.* **CONCEDED — and the fix is structural, not verbal.** The film now declares **no camera pose at all.** The station is DERIVED from a stated requirement (slab band = the bottom sixth = 67.2 mm) and the derivation ships with its sweep, including the distance at which the film dies.
3. *The hero element vanishes at an undeclared station.* **CONCEDED.** Sweep reproduced independently, station declared at 382.2 mm, and the 111 mm of margin published as a ceiling. **I also measured what the auditor could not: the station is clear of geometry by 211.1 mm.**
4. *The 19.9 mm is from the wrong view (rule 38).* **CONCEDED, AND IT CHANGES THE DRAWING.** The film prints the FRACTION with its provenance, not the elevation depth, and states that the apparent width from this station is unmeasured. The gold is drawn as the crown of a roll seen from above.

**ORIGINALITY (2/4) — its top attack kills the old headline and I let it.**
1. *The seam thesis is Paperman and Spider-Verse.* **CONCEDED AND DELETED.** Replaced with a thesis that has no live-action or animated precedent I can name, because it depends on a measurement: **the camera occupies the one station in the transaction that belongs to neither party, and the vehicle's own dimensions forbid faces.**
2. *"Nothing moves but hands" is the cinemagraph.* **PARTLY BINDS AND I DO NOT FULLY ESCAPE IT.** What I can say honestly: nothing here is a photograph, every static element is drawn from measurement, and the camera is locked because a hole in sheet metal cannot move — that is the subject's property, not a borrowed device. **The loop remains close to the form and I am not going to pretend otherwise.**
3. *Vendor-POV is the most occupied camera in food media.* **ANSWERED BY MEASUREMENT.** Vendor-POV is the cook's eye. This is 201.5 mm below it, at a height no body's head occupies, which is why a phone cannot make this shot.
- ⚠ I **rejected** the auditor's own fix #1 (go side-orthographic). It severs the citations, but it also throws away the transaction, the hands and the reason the piece exists — and it puts the whole flank in frame, which is a different film. Stated as a rejection, not an oversight.

**OWNER-AND-BRAND (2.5/4)**
1. *A brand film with no brand in a single frame.* **LARGELY BINDS.** Two answers, both cheap: the **65 bobbles** are in frame across the top and both sides and are Tacombi-specific, confirmed in `ref_side.jpg`; and the **last beat's wrapped item carries the reproduced lettering** from `tex/senor.png`, which exists on disk and the project has already paid for. That is ONE drawing and the only printed thing in sixteen seconds. **The auditor's rule-34 reading is right: SPEC 10.10's object is "every PAINTED element on this vehicle", so hands and food are outside its scope and this is not a 10.10 violation. But its PURPOSE — "the bar is that the owner recognises HIS OWN VEHICLE" — is a real bar and the old version failed it.**
2. *The model contributes a mask, a stripe and a fringe, and the justifying claim is impossible.* **The impossible half is conceded outright — see the danger lens.** What the model genuinely contributes is now larger and is a number: the frame's entire composition is derived, not composed. A person choosing "bottom sixth" by eye would have put the camera anywhere in 300–500 mm and been wrong about the slab by up to 115 mm.

**DANGER (2/4, dangerIntact FALSE) — this is the lens I owe the most to, and its three attacks are the amplification.**
1. *The skin decision is declared unavoidable and then avoided; six inks and not one can draw a hand.* **DEAD RIGHT.** Put back — see below.
2. *The occlusion claim is FALSE; you cannot sample occlusion off a body you have not built.* **CONCEDED, AND THERE ARE TWO ABSENCES, NOT ONE: no AO pass AND no body.** I take the build option rather than striking the claim.
3. *The camera is the most political move in the bench and the concept does not know it.* **CONCEDED.** It is now the thesis rather than an unexamined default, and the reading that it hides behind geometry is owned below rather than mitigated.

### MANDIL 515 · EL HUECO  ·  LINE: adult

**REGISTER** garment — cut-and-sew, zero ink; and people. It is no longer food-and-hand-off: nothing here depicts food, and claiming that flag was part of the flag inflation the completeness critic measured (55 of 75 declared, ~21 real).  
**ARTEFACT** A cross-back cook's apron in pre-shrunk cream cotton drill with a hole cut in the chest.

The hole is the serving bay at 1:1 — 515.5 × 403.0 mm, corners r 55.0, the outline taken from `t1_shell.bay_outline(0)`, which is `T.rrect(x1−x0, Z_HEAD−Z_SILL, BAY_R, seg=8)`, eight segments a corner. Not a printed rectangle, not a faced panel: a void. It is bound in body red (196,49,36) twill tape cut on the straight grain, about 12 mm finished on the face. Through it you see the wearer's own shirt, their body, and whatever the shift has put on it.

ONE hole, not three. There is no wordmark, no roundel, no script, no print, no brass. The load goes to the shoulders on crossed straps for a structural reason — you cannot carry an apron across a chest you have removed.

The shop drawing is a second, separate artefact and it is what ships first: a 1:1 cutting pattern, 1000 × 1700 mm, out of the committed `sheet.py` (mm-native SVG/PNG, shipped rev 77). It carries the aperture path at true size with seam allowance, grain arrow and a 100 mm calibration bar, the station the shape came from — and one more rectangle, described below, which is why the sheet is that size.

The cook wears the hole.

The old version faced it in red cloth. That is the whole distance between a concept and an object: it described a hatch and delivered a bib. A serving aperture is a void; rendering it as a solid block inverts the only fact it was built on, and every auditor said so — the danger lens ("faced, seamed, closed"), the originality lens ("environmental-1 cuts it… this converts an aperture into a solid"). Cut it, and the sentence becomes true at thirty metres with nobody telling anybody anything. An apron with a hole in it is a defective apron — a protective garment with its protection removed at precisely the place protection matters — and that is the object. When a plate crosses the counter, the hole in the steel and the hole in the person are the same hole, about 300 mm apart, and one of them has a man in it.

WHY ONE HOLE AND NOT THREE, WHICH IS THE PART THAT IS NOT DECORATION. The bays are three and equal — the build ray-tests the shell and prints `open serving apertures on +Y: 3`, read back off the mesh at 0.516 / 0.515 / 0.516. The apron has one. It is the forward bay, centre station x = +0.6720 m, the one the survey's contrast section calls bay 1 and closes with this: the render's interior reads sd 24.09 against the photograph's 34.13, and the residual is at the section's own declared ceiling because *"~37 % of bay 1's photographed variance is the man standing in it."* One of the three holes has a person in it. That is the one on the apron. The finding did not get printed on the garment as a caption; it chose which hole to cut. The early critic's test — *"name one design decision the confession CHANGED"* — this is the answer, and it is the reason there is no confession to print.

AND THE SECOND RECTANGLE, WHICH THE AUDIT DID NOT HAVE. `probe_rev39_flank.py` carries, in committed source:

    # the man in the white cap and jacket occludes the lower-forward flank.  He is
    # a known occluder and the exclusion is PRICED, never quietly trimmed.
    MAN_ROWS, MAN_COLS = (420, 768), (90, 300)

210 × 348 px on a 1024 × 768 frame — 9.29 % of it, computed this session, not transcribed — and the probe prints `occluder PRICED: the man covers %.1f %% of the render silhouette`. It is a rectangle in a measuring instrument whose entire job is to delete a human being so a flank can be scored. At `ref_side.jpg`'s 211.5 px/m that rectangle is 993 × 1645 mm, which is the size of a man.

So the pattern sheet carries two rectangles at 1:1: the one you cut out of the cloth, and the one the machine cut a man out of. Same frame, same scale, side by side, both as plain outlines. The sheet is 1000 × 1700 mm and not A1 **because the man is that size** — the apron pattern would fit on A1 easily; the sheet is sized by the deletion, not by the garment. That is the second design decision a finding changed, and it is the reason this is a document about erasure rather than a document about a hatch.

The vehicle stopped so a person could stand still inside it. Seventy-seven revisions later this project has priced him out of a flank fit, masked 6.09 % of a mural board for his cap and a palm frond, thrown him away after using him as a ruler check, and thrown a child away at residuals −16.7, −16.1, −13.6 px. Every one of those was correct method. The garment is the hole they left.

**THE RISK IT STILL CARRIES** — **(1) THE COSTUME PROBLEM, AND I AM NOT SOLVING IT.** This is designed workwear referencing the clothes of people who currently wear plain white, sold in a market where workwear is bought by people who do not work. The danger lens named it and my job is to leave it live, so: it is sold, at a price a line cook can pay, and it is issued free to anyone who works a Tacombi counter. That does not remove the problem — it puts it at the till, where the buyer has to feel it. A concept that mitigates this has sanded it.

**(2) "YOU ARE THE HATCH" IS ON THE CHEST OF SOMEONE EARNING $17/HR, AND IT IS INTACT.** The proposition is that a human being is a hole in a machine. That is either tender or brutal and it is not stable — it will read one way in a magazine and the other way in a labour dispute. It is the most political object in the programme. He should be told that in one sentence before he orders any, and told that I did not soften it.

**(3) THE CLOTH CANNOT HOLD THE MEASUREMENT AND I STOPPED PRETENDING IT COULD.** The feasibility lens's attack binds completely. Cotton drill shrinks; a hole in a woven shrinks *with* it, so this aperture closes over the garment's washed life. Sanforized ranges 1–3 % — that is an **industry range, NOT measured on this cloth**, and 3 % of 515.5 is 15.5 mm. Cut-and-sew adds ±3–8 mm operator to operator before any wash. So: paper carries 0.1 mm, cloth carries ±5 mm, and both figures go on the pattern. Mitigated by mill-sponged drill and a straight-grain bound edge; **not eliminated**. The honest position is that the garment slowly closes, and I would rather say that than quote 515.5 on a substrate that cannot hold it.

**(4) A HOLE IN A COOK'S APRON IS A REAL SAFETY REDUCTION.** Splash and radiant heat reach the torso where the apron does not. Every maker will refuse this and they are not being difficult. It may be unwearable on a hot line and only wearable front-of-counter. If it must close, it closes with a red-bound flap that *opens* — a hatch is a thing that opens — and never with a solid inner panel, which is the faced version returning in disguise.

**(5) IT LEAVES A WORDMARK OFF THE HIGHEST-FREQUENCY BRAND SURFACE IN THE BUSINESS, PERMANENTLY.** Real cost, conceded, priced below.

**(6) THE FIRST PHOTOGRAPH OF A COOK WEARING IT DOES NOT EXIST AND MAY NEVER.** Filed as a want, not as a step. See below.

**(7) F191 IS UNTOUCHED.** Nothing here advances the emblem — 0.8528 against P1b's 0.9465, nine reports, and the objective still has no legibility term. Declared, not routed around.

**(8) NAMING HAZARD FOUND THIS SESSION.** The record indexes these three holes both ways — `SURVEY_rev49_photoreal.md:776` says *"bay 0 and… bay 1"* while `:874` says *"bay1 / bay2 / bay3"* for the same apertures. The pattern must therefore carry the **station**, x = +0.6720 m, and never an ordinal. If someone cuts the wrong bay this concept is about nothing.

**WHAT THE MODEL CONTRIBUTES** — Because the aperture is the only shape in this entire record that belongs to the owner.

The completeness critic's top finding was that almost every saleable object in the pool is a Volkswagen T1 silhouette or a VW roundel, and that in 77 revisions measuring a tail board to 0.1 mm there is not one line about trade dress. This object has zero. Volkswagen made the van; the conversion cut those three holes in it. 515.5 × 403.0 r55 at x = +0.6720 / +0.0470 / −0.5980 is the taqueria's own geometry, on its own vehicle, and no other van in the world has it. Nine owner rejections have gone into a mark this company may not be allowed to print; the shape it can print for free has been sitting in `t1_shell.py` the whole time.

And the shape is not read off a photograph, which is the only reason it is worth 1:1. The build ray-tests the shell — `open serving apertures on +Y: 3` — and reads back 0.516 / 0.515 / 0.516 on the mesh. The record retired a 0.507 / 0.516 / 0.526 taper **twice** as a perspective artefact, and the source comment records that perspective in fact *over-explains* it (4.4–4.5 points predicted against 3.55 measured), so if anything they narrow very slightly forward and 0.5155 is held equal because a 2 mm taper is under the floor. The pillar asymmetry is forbidden and is not used. The garment is cut on a fight the machine won, and `bay_outline(0)` is a live callable, so the pattern is generated, not drawn.

Beyond that outline the model contributes exactly two more things and I will not invent a third: the two colours, `RED = (0.5520, 0.0294, 0.0176)` = sRGB(196,49,36) and `CREAM = (0.6172, 0.6308, 0.5776)` = sRGB(206,208,200), both live in `t1_mats.py`; and the frame-space deletion rectangle from `probe_rev39_flank.py`. The tie height is not a measurement and is not claimed. Neck-strap height is not a measurement. The counter constants (`CNT_ZT/CNT_ZB` 1.2540/1.1470 = 107.0 mm thick, `CNT_Y_IN/OUT` 0.8450/1.1660 = 321.0 mm deep) are real but this object does not need them, so it does not quote them.

The occlusion half of the owner's style sentence — normal pass, AO pass — does not exist, and this is the rare artefact that does not want it. There is nothing to shade. It is a line and two flat colours, which is the half of *"vector line and flat colour, shading and occlusion sampled from the 3D asset"* that is built.

**MEASURED FIGURES** — **READ OUT OF LIVE SOURCE THIS SESSION, WITH PROVENANCE:**

- Aperture **515.5 × 403.0 mm, r 55.0**, 8 segments per corner — `t1_shell.py`: `BAY_W = 0.5155  # equal, measured`; `Z_SILL, Z_HEAD, BAY_R = 1.3720, 1.7750, 0.0550`; `bay_outline(i)` returns `T.rrect(x1 − x0, Z_HEAD − Z_SILL, BAY_R, seg=8)`.
- Bay centres **x = +0.6720 / +0.0470 / −0.5980 m** — `BAY_CX  # measured centres`. The apron uses `BAYS[0]`, x = +0.6720.
- **THREE, EQUAL** — `STATE.md`: `open serving apertures on +Y: 3` and `bay widths 0.516 0.515 0.516`, ray-tested through the shell, not counted off panes.
- The retired taper 0.507 / 0.516 / 0.526 — retired **twice**; the source records perspective *over*-explaining it, 4.4–4.5 points predicted against 3.55 measured.
- **RED (196,49,36)** = linear (0.5520, 0.0294, 0.0176); **CREAM (206,208,200)** = linear (0.6172, 0.6308, 0.5776) — `t1_mats.py`.
- Deletion rectangle **210 × 348 px = 9.29 % of a 1024 × 768 frame** — `probe_rev39_flank.py`: `MAN_ROWS, MAN_COLS = (420, 768), (90, 300)`; the percentage computed this session from the file's own dimensions, not transcribed. The probe prints `occluder PRICED: the man covers %.1f %% of the render silhouette`.
- That rectangle in metres: **993 × 1645 mm** at `ref_side.jpg`'s 211.5 px/m. ⚠ **CEILING — this is an UPPER BOUND.** The subject stands nearer the camera than the scale plane, the same ceiling `REF_MEASUREMENTS.md` states for the leaning man at 375 px / 1.78 m. It is *"about the size of a man"*, and must never be printed as his height.
- **~37 % of bay 1's photographed variance is the man standing in it** — `SPEC.md:1167`, `SURVEY_rev49_photoreal.md:874`; photographed sd 34.13 against the render's 24.09, unchanged under downsampling from 268.9 to 211.5 px/m.
- The child: residuals **−16.7, −16.1, −13.6 px** on her hair (F220). The mural mask: **6.09 %** of the board, for a palm frond and a man's cap (`lid_gen.py`).
- Counter, verified but deliberately **not used**: `CNT_ZT/CNT_ZB` 1.2540 / 1.1470 = **107.0 mm** thick; `CNT_Y_IN/OUT` 0.8450 / 1.1660 = **321.0 mm** deep.

**STATED AS NOT MEASURED:** tie height; neck-strap height; the cloth's shrinkage (1–3 % sanforized is an industry range, not a measurement of this drill); all costs below. **NOT USED:** the pillar asymmetry 109.5 | 129.5, which is forbidden and refuted on sign.

**COST / FEASIBILITY** — **THE PATTERN — the only figure here I can stand behind.** `sheet.py` exists, is committed, is mm-native and produced three artefacts at rev 77. `bay_outline(0)` is a live callable. One afternoon of scripting, no Blender, no render queue, no AO pass. Plan-copy printing of a 1000 × 1700 sheet: a few dollars.

**THE GARMENT — ESTIMATES, DECLARED AS ESTIMATES, NOT MEASUREMENTS.** The completeness critic is right that ~50 concepts carried no cost line and that the programme reaches for the six most expensive processes in merchandise. This one reaches for none of them: no print set-up, no separations to register, no enamel tooling, no die, no trademark clearance, no brass. Against the old spec I have deleted the brass hardware and the contrast facing and added one operation, the bound aperture.

- Cloth: pre-shrunk (mill-sponged) cotton drill, roughly 1.4 m per garment.
- Operations: one hole cut, one bound edge (~12 mm finished, straight grain), crossed straps, hems, one woven care/fibre/origin label — which is **legally required for a sold garment**, a point the owner-and-brand lens made correctly against the old version's *"zero legal surface"* claim. Zero *trademark* surface is the accurate phrase.
- **ESTIMATE, UNMEASURED: landed COGS US$18–28 at 50 units; RRP US$45–60; MOQ 25–50; lead time 3–5 weeks** from a small NYC or CDMX maker. These are trade-typical figures, not quotes. **One sample converts every one of them into a measurement, and until it does they should be read as guesses.**
- Sits under the critic's own US$60 ceiling. Free to anyone working a Tacombi counter.

**THE HARD PARTS, HONESTLY.** (a) Makers will refuse the hole, or quietly close it — the spec must say NO INNER PANEL in capitals, and the first sample must be inspected for exactly that. (b) The bound aperture is the only skilled operation and it is where the ±5 mm lives. (c) Grading: the hole is **fixed at 515.5 × 403.0 on every size, XS to XXL**, and the body changes around it. This is the one constraint two auditors praised and it survives untouched — and it gets worse in a way worth stating, because on a smaller wearer the hole removes a larger fraction of the person. The moment anyone scales the hole to the body it stops being a measurement and becomes a neckline. Hold it or do not make it. (d) The safety reduction in (4) above may confine it to front-of-counter, which is a real limit on the order size.

**WHAT CANNOT BE RECOVERED FROM WHAT WE HOLD:** whether this reads as a hatch or as a mistake on an actual body. No frame in this repository shows a person wearing anything with a hole in it, and no amount of measurement will settle it. That is what the 1:1 sheet is for — it is the cheapest possible way to be wrong early.

**FIRST SHIPPABLE STEP** — **IN HIS HANDS THIS WEEK, WITH NO BUS, NO COOK, NO RESTAURANT, NO PHOTOGRAPHER AND NO PERMISSION.**

The old first step asked for a staged photograph of a working cook at a service counter. The feasibility lens's attack on that binds and I am withdrawing it entirely: `PHOTOS_WANTED_rev52.md` item 7 asks for one hubcap, square on, and has sat unfulfilled for 24 revisions; items 1–5 are refused. A programme that cannot obtain a photograph of a wheel cover cannot obtain that one. It was a new photo request wearing a first-step costume.

**SHIP INSTEAD: `mandil.py` → `design_out/mandil_515_patron.svg` + `.png`.** One afternoon on infrastructure that already exists and is committed.

1. Call `t1_shell.bay_outline(0)`, translate by `bay_centre(0)`, and emit the polyline into a `sheet.Sheet(1000, 1700)` at 1:1. Two inks only: cut lines in RED sRGB(196,49,36), notation in a neutral grey.
2. Draw the aperture with a 10 mm seam allowance offset, grain arrow, four balance notches, and a 100 mm calibration bar in the margin so any printer's scaling error is caught by a ruler before cloth is cut.
3. Beside it, at the same 1:1, draw the deletion rectangle — 993 × 1645 mm, from `MAN_ROWS, MAN_COLS = (420, 768), (90, 300)` at `ref_side.jpg`'s 211.5 px/m — as a plain outline, with the source comment set in the margin verbatim: *"He is a known occluder and the exclusion is PRICED, never quietly trimmed."* **This rectangle is why the sheet is 1000 × 1700 and not A1.**
4. Title block, deadpan, in the register that is now ruled: the station `x = +0.6720 m` and never an ordinal; `515.5 × 403.0 r 55.0`, PAPER ±0.1 mm / CLOTH ±5 mm; `SHRINKAGE: NOT MEASURED ON THIS CLOTH`; the 993 × 1645 as `UPPER BOUND — the subject stands nearer the camera than the scale plane`.
5. Print it at a plan-copy shop for a few dollars, check the calibration bar with a steel rule, and hand him a rolled sheet.

He can hold it against his own chest in his own office and answer the only question that matters — does a 515 × 403 hole read as a hatch on a human body, or as a bib pocket — before anyone cuts cloth. **Then**, and only then, one sample from any maker in New York or Mexico City.

The cook-at-the-counter photograph becomes **PHOTOS_WANTED item 8, explicitly not budgeted on**, with the note that items 1–5 and 7 are all still open.

CEILING ON THE STEP: it ships a drawing, not a garment. Nobody has worn this. The shrinkage number stays unmeasured until a sample is cut and washed ten times hot — which is a real measurement this project has never made and could make for the price of a metre of drill.

**HOW IT ANSWERED THE FOUR LENSES** — **WHAT I PUT BACK, NAMED, BECAUSE THE FOURTH LENS SAYS THE DANGER WAS SANDED (it was, and it graded 1.5/4):**

1. **THE HOLE IS CUT.** The concept's central verb was "wears the hole" and the artefact said "faced, seamed, ZERO printed inks" — closed. It is now a void bound in red. The idea is in the construction, survives the label being cut out, and reads at thirty metres.
2. **THE ERASURE MOVED FROM THE PITCH INTO THE OBJECT.** The audit's sharpest hit was that the truest paragraph in the bench appeared nowhere on the garment. It still does not — and now it does not need to, because it decides **which** hole is cut (bay 1, the one that is 37 % a man) and **how big the pattern sheet is** (1000 × 1700, sized by the deletion rectangle). Two design decisions changed by findings. No caption anywhere on the cloth.
3. **THE DELETION RECTANGLE — NEW, AND NOT IN THE AUDIT.** `MAN_ROWS, MAN_COLS = (420, 768), (90, 300)`, 9.29 % of `ref_side.jpg`, a rectangle in committed source whose only job is to remove a man. Nothing in the 75-concept pool has it.
4. **THE COSTUME PROBLEM IS LEFT OPEN ON PURPOSE**, with the free-to-workers pricing offered as a sharpening rather than a fix.

**ATTACKS ANSWERED:**

*FEASIBILITY 1 (first step needs access) — BINDS. Withdrawn and replaced;* see above. *FEASIBILITY 2 (cotton cannot hold 0.1 mm) — BINDS, and it changed the object:* pre-shrunk drill, straight-grain bound edge, two carriers with two tolerances, and the closing aperture named as the garment's clock rather than hidden.

*ORIGINALITY (13 concepts on this rectangle; TRES HUECOS minus two holes) — PARTLY BINDS, and I stop claiming the rectangle as the differentiator.* What is not in the pool: a **void in a body** rather than a positive on a substrate; **one** hole chosen by a measurement; and an object that works by failing at its own function. *(environmental-1 cuts it in steel at architectural scale, where the void is filled by a wall; here it is filled by a person and the fill changes every shift.)*

*ORIGINALITY (Hedley & Bennett / Tilit house spec verbatim) — BOUND ON THE OLD SPEC, so the spec is gone.* Brass hardware: deleted. Contrast panel: deleted, there is no panel. Cross-back kept for load reasons only, stated. Prior art named as a position. **The differentiator is that neither of those companies will make this, because a hole in an apron is a manufacturing defect.**

*OWNER 1 (no F331 line) — FIXED: adult, paid/kept, deadpan-catalogue. The children's line is owed and this is not it; do not count it against that half.*

*OWNER 2 (brand subtraction) — I CONCEDE THE COST AND DECLINE THE PROPOSED FIX.* Putting the Señor Tacombi script inside the aperture turns the void back into a print carrier — the exact sanding the fourth lens forbids, arriving as a remedy. Paid differently: this **does not replace the uniform**, the script apron stays in service, and the compensating claim is that the aperture is the one mark here with no third-party trade dress in it at all.

*OWNER 3 (culled twice; idea detachable) — the bench shelved MANDIL 812 because "an object whose idea is detachable is not a designed object". A hole is not detachable.*

*OWNER 4 (ships nothing from us) — FIXED.* A generated vector file from the mesh's own outline through the committed `sheet.py`. That is line output, which is the programme's spine.

*OWNER 5 (wrong revision — F330 fired, do the sticker) — CONCEDED ON ORDER.* The sticker is rank 1 and this does not compete with it. This costs one afternoon of `sheet.py` time, no Blender, no render, and **no AO pass** — so it is the thing that can ship while the occlusion half of the style sentence gets built.

**CONSENT: CLEAN, AND SAID PLAINLY.** No archive human appears on any object. Nothing is printed. The only person in the hole is the wearer, consenting by putting it on. The bench's fabricated headcounts — "seven real people", the magenta puffer coat — are struck and not used; the audit found the record supports six, and the man in bay 1 is one man in a white cap, verified by a crop.

### A LA ALTURA · 118  ·  LINE: adult

**REGISTER** photographic — portrait and service; three-dimensional (a fabricated instrument); people. FOOD IS PRESENT BUT IT IS NOT THE SUBJECT — the people are. Adult line (F331).  
**ARTEFACT** TWO PARTS, A SPACER PAIR, AND A DECK OF PAIRS.

**THE INSTRUMENT — Part A, the frame.** 900 × 700 mm outer, 9 mm birch skins over a 6 mm rib core (torsion box, NOT solid — see cost). Aperture cut as the GROUND-FRAME parallelogram: nominal 515.5 × 403.0 mm, sides plumb, sill and head at 17.75 mm/m, 9.150 mm of fall front-to-rear across the width, interior angles 91.017° / 88.983°, corners as sheared 55 mm arcs. Faced in the flank cream, `t1_mats.CREAM` (0.6172, 0.6308, 0.5776) = sRGB (206, 208, 200) = #CED0C8. Two 3/8" threaded inserts on the back for C-stand spigots; a plumb-bob eyelet on the top edge, centred, so the line hangs in frame.

**THE INSTRUMENT — Part B, the counter edge.** A 321 mm return, 107 mm in elevation, hollow, same construction. Its outer edge carries half-hard brass across 18.6 % of that 107 mm = 19.9 mm — `CNT_NOSE_F` 0.1860, measured over 113 columns of `ref_side.jpg` at 0.182 and corroborated at 0.191 on `ref_rear34.jpg`. Faced in the COUNTER cream, `t1_mats.COUNTERCREAM` (0.7350, 0.7150, 0.6600) = sRGB (223, 220, 212) = #DFDCD4. It is not the same cream as the frame and the spec sheet says so on its face, with both source lines.

**THE SPACERS.** Two machined blocks, 118.0 mm, ground and stamped `118.0 · INVARIANTE`. They set Part B below Part A. Every other dimension on the object has an adjustment; these have none.

**THE ONE ADJUSTABLE DIMENSION, AND IT IS THE ONE WE DO NOT KNOW.** The reveal depth is a sliding sleeve behind the aperture, running 40–110 mm on an engraved scale, detented at 70. The model holds NO reveal at this aperture — the only depth in the mesh there is a 9.0 mm `conform_ring` rubber section (`t1_shell.bay_seals`, `thick=0.0090, off=-0.0030`), which is a seal, not a reveal. So the confession is not a caption in 5 pt type; it changed the object. The one thing we cannot measure is the one thing that moves, and it moves against a printed ruler. Everything else is fixed because it is known.

**THE OUTPUT.** Matched pairs, one person per pair, 11:00 and 23:00, identical camera position, no crop. Cards 96.4 × 338.3 mm — the vehicle's own pillar-card size, RE-DERIVED (see measured figures; the 94.8 mm this concept previously printed inherits a retired constant). 350 gsm uncoated, duplex. Face: the pair, 4-colour, full bleed, nothing else. Reverse: one ink — name, station, the two clock times, the interval, and `118.0 mm`. That is the entire reverse.

**WHAT IT DOES NOT DO.** It does not set brand photography policy. The previous version said "the only frame this brand is ever photographed through"; that sentence is struck. It is a camera jig, owned by the restaurant, used when the kitchen wants it, one of several frames. The moment it stops dictating, it survives a second site — which the "constant" version could not.

THE APERTURE IS NOT A RECTANGLE, AND NOBODY IN SEVENTY-FIVE CONCEPTS NOTICED.

`build.py` step 8b is not a lift. Its own comment reads "the drop is a shear in x," and it subtracts `rake_drop(x) = RAKE_Z0 + RAKE_DZDX·x` from every vertex. The serving aperture is authored as a rectangle in the body frame and then sheared. Relative to the ground the vehicle stands on, it is a PARALLELOGRAM: two plumb sides, two horizontals running downhill at 17.75 mm/m, 9.150 mm of fall across its 515.5 mm width, interior corners of 91.017° and 88.983°. The four 55 mm corner arcs are no longer circles — they depart from circular by ±0.488 mm, which is 1.84× the 0.265 mm chord error of the mesh's own eight-segment polygon.

Every aperture object in the pool — thirteen of them, at thirteen scales — cut the rectangle. The rectangle is the thing that is not true.

So: cut the parallelogram. And then note what the parallelogram gives you that the rectangle never could — A DATUM FOR FREE. The shear is vertical and depends on x alone, so the two SIDES stay plumb while the sill and head do not. Hang the frame so its sides read true against a plumb line, and the sill runs visibly downhill. Gravity is the reference. No floor, no level, no jig, no fabricator's promise; a $15 plumb bob, hanging in shot, checkable in every frame anyone ever takes through it. The rake stops being a stencilled assertion and becomes a thing you can see.

AND THE SECOND NUMBER, WHICH IS THE PIECE. `Z_SILL` 1.3720 and `CNT_ZT` 1.2540 are both authored constants, and step 8b subtracts the same drop from both at the same station — so the gap between the aperture's sill and the counter's top is 118.0 mm at EVERY station along the vehicle. It is rake-invariant. It is the only dimension on this bus that does not move.

Put a person on either side of it and 118.0 mm is the distance between a face and a hand.

Because the aperture band above ground is 1312.1–1715.1 mm at the front bay and 1334.7–1737.7 mm at the rear (station-stated, computed from the same constants), and that is standing adult head height, not counter height. The counter top is 1189.8 mm at its front end and 1244.9 mm at its tail. So the vehicle's own geometry says: your face is in the hole, their hands are 118 mm below it, and that 118 mm is the whole transaction.

THE OBJECT IS TWO PARTS AND A SPACER. The aperture frame — sheared, plumb-sided, faced in the flank cream. The counter edge — a 321 mm return, 107 mm in elevation, with 19.9 mm of brass across its top, faced in the counter cream, which is a DIFFERENT cream and the model says so. Between them, two machined spacers at 118.0 mm. Everything on this object is adjustable except the spacers. They are the argument.

THE OUTPUT IS A MATCHED PAIR, AND THIS IS WHERE THE DANGER WENT BACK IN. One camera position, one lens, one person, twice: at 11:00 and again at 23:00. Printed adjacent, same size, no crop. Twelve hours of a human being on the same brass. The reverse carries THEIR NAME, THEIR STATION AND THE INTERVAL TO THE MINUTE — 11:04 → 23:11, 12 h 07. Not the dish. Not the date. The only dimension that survives onto the card is 118.0 mm, because that is the one the two frames are about.

A programme that measures a tail board to 0.1 mm and gives the cook no name is making a statement. This one counts the hours instead of the millimetres, and publishing a line cook's shift length on a saleable object is a labour statement whether or not you intend it as one. That is the risk. It is the point.

The cook holds a veto on their own pair, after seeing both frames, up to the moment of print, and is paid the frame fee whether it prints or not. That is not a mitigation — it is what makes the danger honest instead of extractive, and it is a real, budgeted cost with a real chance of losing the best frame in the set.

AND IT IS THE ONLY OBJECT ON THE BENCH THAT CARRIES NO VOLKSWAGEN MARK. No roundel. No T1 silhouette. A sheared parallelogram, a brass strip, two creams and two spacers. Early critic 1's top finding — "the entire merchandise programme is built on a third party's trade dress and nobody has checked" — does not reach this object, by construction and at zero cost. (CEILING: that is a factual statement about what the artefact contains, not legal advice; the one page of IP advice that critic asked for is still owed on everything else.)

**THE RISK IT STILL CARRIES** — **THE DANGER I PUT BACK IS A REAL ONE AND IT CAN COST HIM.** Printing a named line cook's shift interval on a saleable object is a labour statement, and it will be read as one — favourably by some, as an admission of twelve-hour shifts by others. A screenshot of that card reverse with a hostile caption is a foreseeable outcome. I am not going to mitigate it, because mitigating it is what took this concept to 1/4 on the danger lens. What I will say is that it is the owner's decision to take, made in front of the actual card, not mine to make on his behalf in a concept document.

**THE SUBJECT'S VETO IS A REAL LOSS, NOT A COURTESY.** A cook who sees their 23:00 frame may kill the best pair in the set, after the fee is paid. That is the price of the veto being real. Budget for losing frames.

**THE SHEAR MAY BE INVISIBLE.** 9.150 mm of fall across 515.5 mm is 1.017°. I have not looked at it at 1:1 and neither has anyone else. If the eye cannot see it beside a plumb line, the entire differentiator collapses and the object is a nice window with a good spacer in it — which is precisely what the originality lens accused the previous version of being. The first step is built to find that out in an hour for nothing, and the honest answer may be no.

**THE REVEAL DEPTH IS STILL A POSE.** 70 mm is not measured, the model holds nothing but a 9.0 mm seal section there, and it cannot be recovered from what we hold. The sleeve makes that visible instead of hiding it; it does not make it known.

**THE CARD WIDTH IS UNRESOLVED, AND I FOUND THE DEFECT RATHER THAN INHERITING IT QUIETLY.** `CARD_W` is derived through the retired 0.507 bay width; on the live 0.5155 it reads 96.4 mm; the pixel measurement under both is 20.0 ± 0.5 px = ±2.4 mm, so the two are indistinguishable by the measurement that produced them. I print 96 ± 2 mm. A re-measurement of card B in `ref_side.jpg` would settle it and has not been done here.

**THE TWO CREAMS ARE NOT EQUALLY GROUNDED.** CREAM is measured. COUNTERCREAM is a SOLVED albedo whose source patches have no coordinates in this repository and were recovered forensically at rev 27, in a block that carries a correction to its own preceding paragraph. The lip's colour is the weakest figure on the object and the spec sheet says so.

**I HAVE NOT LOOKED AT ANY OF THIS RENDERED OR CUT.** No frame was rendered in this session and `out/` starts empty on a clone. Every figure above is read off source and arithmetic; none is read off a picture. Rule 1 is unsatisfied and will stay unsatisfied until the card outline is printed at 1:1 and held up — which is the entire first step, and which is why the first step is not a render.

**IP: NARROW CLAIM ONLY.** The artefact contains no Volkswagen mark and no T1 silhouette. Whether a serving-aperture proportion, a brass fraction and a cream are protectable by anyone is a question for the one page of advice early critic 1 asked for, which is still owed and which this object does not discharge for the rest of the bench.

**WHAT THE MODEL CONTRIBUTES** — THE HONEST VERSION OF THIS CLAIM IS SMALLER THAN THE ONE I INHERITED, AND IT IS STRONGER FOR BEING SMALLER.

The previous version said "the model is the cutting file, and without it this is decoration." The feasibility auditor called that inflated — eight numbers, seven of them tape-measurable on a bus the brand owns — and the auditor is right. I withdraw it.

The model supplies TWO FACTS and eight conveniences. The conveniences are real (515.5, 403.0, r 55, 107, 321, 18.6 %, 3.106 m, 55.1 mm) and a person with a tape and an afternoon could get most of them. The two facts cannot be got that way:

**ONE — THE SHEAR.** The aperture is a rectangle in the body frame and a parallelogram relative to ground. A tape held against the real vehicle measures the body frame and reads a rectangle, because the tape rakes with the bus. To find the 9.150 mm you would have to level against the ground with the vehicle at its exact stance, and then you would be measuring tyre pressure and load as much as rake. The number comes from `RAKE_DZDX` and step 8b's shear and from nowhere else in anything we hold. No photograph gives it either: a photograph of a raked vehicle from an unknown pose cannot separate the rake from the camera — that is `probe_rev64_shear`'s standing lesson, and rule 43, "a photograph is a projection, and a de-squash is not an un-projection."

**TWO — THE INVARIANCE.** That the sill-to-counter gap is 118.0 mm at EVERY station is a property of the authored frame plus a same-station subtraction. A tape gives you 118 mm once and no reason to expect it twice.

Everything else this object needs, the model happens to hold. Those two, only the model holds.

**AND WHAT THE MODEL EXPLICITLY CANNOT GIVE:** the reveal depth. There is no reveal in this mesh — `t1_shell.bay_seals` builds a 9.0 mm `conform_ring` at `off=-0.0030`, which is a rubber section and not a jamb. So 70 mm is a POSE, the sleeve moves because of it, and no photograph in the set bounds it. It cannot be recovered from what we hold.

**CAPABILITY DEPENDENCIES, DECLARED** (early critic 2's remedy). This object consumes NO render, NO line pass, NO AO pass, NO normal pass, NO sun lamp, NO interior camera, NO glTF or bake path. It needs one closed-form outline — four arcs and four lines from `BAY_W`, `Z_HEAD − Z_SILL`, `BAY_R` and `RAKE_DZDX` — written by a script with no `bpy` import. The three absent capabilities the critic named block every other concept in the shortlist. They do not touch this one. That is the reason it can be in his hands this week and most of the bench cannot.

**MEASURED FIGURES** — Every figure below was read out of source in this session, not transcribed.

**THE APERTURE.** `t1_shell.py`: `BAY_W = 0.5155` (equal, measured, THREE of them); `Z_SILL, Z_HEAD, BAY_R = 1.3720, 1.7750, 0.0550` → 403.0 mm tall, 55.0 mm radius. `BAY_CX = (0.6720, 0.0470, -0.5980)`.

**THE SHEAR — the finding.** `t1_core.py`: `RAKE_DZDX = 0.017750`, `RAKE_Z0 = 0.047925`, `rake_drop(x) = RAKE_Z0 + RAKE_DZDX*x`. `build.py` step 8b: *"the drop is a shear in x. See t1_core.rake_drop()."* Computed: fall across the aperture 515.5 × 0.017750 = **9.150 mm**; interior angles **91.017° / 88.983°**; departure of a sheared 55 mm arc from circular **±0.488 mm** (r·k/2). Wheels are exempted from the shear (`_WHEEL_PREFIX`), the aperture is not.

**THE THREE OUTLINES, ALL THREE NAMED** (feasibility attack 7). (i) the authored circular arc; (ii) the mesh's own polygon — `bay_outline` calls `T.rrect(..., seg=8)`, sagitta 55·(1−cos 5.625°) = **0.2648 mm**; (iii) the ground-frame sheared arc, **±0.488 mm** from circular. The cutting file is (iii), generated in closed form. Its deviation from (i) is 0.488 mm and from (ii) 0.4–0.7 mm depending on station. Stated rather than picked.

**ABOVE-GROUND BANDS, STATION-STATED** (early critic 2's remedy). Aperture, bay 0 (x = +0.672): 1312.1 → 1715.1 mm. Bay 1 (x = +0.047): 1323.2 → 1726.2. Bay 2 (x = −0.598): 1334.7 → 1737.7. `STATE.md`'s 1.307–1.710 is the same band at `X_DROP_REF` ≈ 0.962.

**THE COUNTER.** `t1_detail.py`: `CNT_ZT, CNT_ZB = 1.2540, 1.1470` → 107 mm. `CNT_Y_IN, CNT_Y_OUT = 0.8450, 1.1660` → 321 mm plan depth. `CNT_X0 = 0.9180`; `CNT_X1 = T.X_TAIL − CNT_OVERHANG` = −1.873 − 0.3150 = −2.188 → 3.106 m. Above ground: **1189.8 mm** at x = +0.918, **1244.9 mm** at x = −2.188, rise **55.1 mm**. `CNT_NOSE_F = 0.1860`; brass in elevation 0.1860 × 107 = **19.902 mm**, and `t1_detail` prints the same figure in its own comment: *"19.9 mm of gold in elevation."*

**THE 118.0 mm, AND WHY IT IS INVARIANT.** `Z_SILL − CNT_ZT` = 1.3720 − 1.2540 = **118.0 mm**. Both are authored constants; step 8b subtracts the same `rake_drop(x)` from both at any shared station, so the difference is unchanged by the drop. It is 118.0 mm at every station along the counter. That invariance is a property of the authored frame — a tape measure on the real vehicle returns 118 mm at one station and gives you no reason to expect it at the next.

**TWO CREAMS, BOTH WITH SOURCE LINES** (feasibility attack 3, conceded in full). `t1_mats.CREAM = (0.6172, 0.6308, 0.5776)` = sRGB (206, 208, 200) = **#CED0C8** — the flank. `t1_mats.COUNTERCREAM = (0.7350, 0.7150, 0.6600)` = sRGB (223, 220, 212) = **#DFDCD4** — the counter. The auditor's ≈#DFDCD4 was right. CEILING: COUNTERCREAM is a SOLVED albedo, not a swatch, and its own source block carries a rev-27 correction to the paragraph above it — the triple once labelled "this file's CREAM" was the von-Kries gain, not a cream. Neither source patch has coordinates in the repo; they were recovered forensically at rev 27. Say "solved," not "measured."

**⚠ A DEFECT IN THIS CONCEPT'S OWN HEADLINE FIGURE, FOUND AND RETRACTED HERE.** The card size 94.8 × 338.3 mm is `t1_detail.CARD_W, CARD_H = 0.0948, 0.3383`. `CARD_H` is sound: 70.0/83.4 × 0.403, and 0.403 is live. `CARD_W` is **not**: its source line reads `CARD_W = 20.0/107 * 0.507 = 0.0948`, and **0.507 is the RETIRED bay width.** `STATE.md`: *"SPEC §1.1's taper (0.507 / 0.516 / 0.526) is RETIRED — it was the 100 mm origin error of rev 13. The bays are EQUAL at 0.5155."* On the live scale, 20.0/107 × 0.5155 = **96.4 mm**, not 94.8. This is SPEC 10.25's own defect class — a constant tuned against a constant that later moved — living in the source. CEILING, and it matters: the underlying pixel measurement is 20.0 ± 0.5 px, which is ± 2.4 mm, so 94.8 and 96.4 are **not distinguishable by the measurement that produced either.** The honest card width is **96 ± 2 mm**. It wants a register row; I am not assigning it an ID.

**FORBIDDEN FIGURE, NOT USED:** the pillar asymmetry 109.5 | 129.5 appears nowhere in this concept. The aperture family here is founded on the THREE EQUAL holes at `BAY_W` 0.5155.

**COST / FEASIBILITY** — **MATERIALS — ESTIMATE, NOT A QUOTE.** One 2440 × 1220 sheet 12 mm birch ≈ $70; half sheet 9 mm for the skins ≈ $45; 1 L each of two matched creams ≈ $70; half-hard brass strip 19.9 × ~1100 mm ≈ $30; two machined 118.0 mm spacers, ground and stamped ≈ $60; plumb bob and line ≈ $15; food-safe two-pack seal ≈ $25. **Materials $315.** Half a day on a CNC or a router table: $0 if the owner's fabricator cuts it, ≈ $150 bought in. **Instrument all-in ≈ $315–465.** Lead time: birch, brass and paint off the shelf; CNC 3–5 working days.

**CARDS.** 500 duplex, 350 gsm uncoated, 4/1, short-run digital ≈ $180–260. MOQ 100. Lead time 5 working days. **Print COGS ≈ $0.45/card at 500.**

**THE LINE NOBODY BUDGETS, AND IT IS THE LARGEST ONE.** A per-frame fee to every person photographed, paid on release whether or not the pair prints. At $150 per person per pair and twelve pairs, **$1,800.** Landed COGS per card at 500 becomes ≈ $0.45 print + $3.60 amortised fee = **≈ $4.05.** That is the honest arithmetic and it decides the object's form: this cannot be a free counter giveaway at volume. Either it is a limited pack — six pairs, RRP $18, which sells through at a taqueria and returns roughly 2.2× COGS — or the fee is booked as marketing spend and the cards are free with an order, in which case the programme is buying twelve portraits for $1,800, which is cheap for twelve portraits. **His call; both are priced.** ESTIMATES throughout.

**TOTAL TO A REAL OBJECT PLUS A FIRST DECK: ≈ $2,300–2,500**, of which 75 % is paying people.

**THE BINDING CONSTRAINT, NAMED RATHER THAN FOOTNOTED.** The pairs need a working kitchen twice in one day, twice-daily access, and staff who agree to be named. `PHOTOS_WANTED_rev52.md` item 7 has been outstanding for twenty-four revisions for ONE phone photograph of a hubcap. Realistic: 2–6 weeks to the first pair, uncompressible, and it may not happen at all. **THE FALLBACK IS EXPLICIT: the instrument and its spec sheet ship regardless; the cards do not ship without the people, and no substitute is acceptable — not archive frames, not staged frames, not the owner's hands standing in.** If the pairs never happen, this concept delivered a $400 measuring instrument and a negative result, and that is a real result.

**WHAT IT DOES NOT NEED:** no render, no line pass, no AO or normal pass, no sun lamp, no interior camera, no bake or export path, no geometry change, no `bpy`. Four arcs, four lines and a plumb bob.

**FIRST SHIPPABLE STEP** — **ONE HOUR, NO BUDGET, NO RENDER, NO STAFF, NO KITCHEN, AND IT TESTS THE ONE THING THE CONCEPT TURNS ON.**

Write ~40 lines with no `bpy` import that emit the aperture outline in closed form from four constants already in the tree — `BAY_W` 0.5155, `Z_HEAD − Z_SILL` 0.4030, `BAY_R` 0.0550, `RAKE_DZDX` 0.017750. Four sheared arcs, four lines. Two files:

1. **`aperture_sheared.svg`** at 1:1, plus a PDF tiled to A4 for tape-together.
2. **`aperture_ab.pdf`** — one A2 page, and this is the thing that goes to him. The sheared parallelogram drawn over the nominal rectangle in a second ink, at 1:1, with the 9.150 mm of fall dimensioned, both corner angles called out (91.017° / 88.983°), the three corner outlines overlaid at 20× at one corner — circular arc, the mesh's 8-chord polygon at 0.2648 mm sagitta, the sheared arc at ±0.488 mm — and the two 118.0 mm spacers drawn to scale beneath the sill with the sentence *"sill to counter top, 118.0 mm, at every station."*

**Then tape the tiles together, hang the paper aperture from a doorway with a plumb bob against its left edge, and take one phone photograph.** Send him that photograph and the A2 sheet, and ask ONE question, multiple choice, with both attached:

> *In this photograph the two side edges are plumb and the bottom edge is not level — it falls 9.150 mm across 515.5 mm, which is the bus's own stance. Can you see it? **(a)** Yes, and it reads as wrong in a way I like. **(b)** Yes, but it reads as a badly cut hole. **(c)** No — it looks level to me.*

**(c) kills the concept for the cost of an hour and a sheet of paper**, which is the correct outcome if the differentiator is invisible, and it is a result worth having either way. **(b) says the shear needs the plumb line permanently in frame to read as intention rather than error** — which is a design instruction, not a failure. **(a) buys the wood.**

Nothing in this step needs the restaurant, a schedule, a release, a fabricator, or one minute of Blender. He can do it himself in his own doorway, and the twelve frames that follow are then his, not a shoot he has to grant someone.

**HOW IT ANSWERED THE FOUR LENSES** — **FEASIBILITY (3/4, danger intact TRUE) — its six live attacks, answered.**

*1. "The 16.0 mm tilt has no datum once the board leaves the vehicle; at 1.017° it is inside the cupping and levelling error of a 900 mm one-face-painted birch panel."* **Answered by the shear, not by argument.** The rake is not a tilt applied to a rectangle; it is INSIDE the outline. The shear is vertical and x-only, so the aperture's two sides stay plumb while its sill and head do not. Gravity is the datum, a plumb bob is the instrument, and it hangs in frame so the reader can check it. Cupping does not defeat this: a cupped panel still has two edges that either read plumb against a hanging line or do not. The auditor's premise — that signal and dominant error are the same quantity — held only while the tilt was an external claim about the whole board. It is now an internal property of the cut.

*2. "Solid birch the lip is 21.0 kg, plus 5.1 kg of board, a ~26 kg prop that cannot be held up in a doorway."* **Conceded; their arithmetic reproduces (321 × 107 × 900 mm at 680 kg/m³ = 21.0 kg).** Both parts are now torsion boxes — 9 mm skins over a 6 mm rib core — with C-stand inserts. ESTIMATE all-up ≈ 9 kg, from ply density, not a weighed part. It will be weighed before the figure is printed anywhere.

*3. "The spec names one cream; the model carries two."* **Conceded entirely and it was the sharpest catch of the four lenses.** Both are on the spec sheet with their source lines and their sRGB, and they land on different parts: #CED0C8 frame, #DFDCD4 lip. Their ≈#DFDCD4 was correct to the hex.

*4. "The seven-day kill-gate strips the lip, brass, rake and paint, so it tests whether a hole is a good frame — a question the model does not answer."* **Conceded; the gate is replaced and now tests the thesis.** The first cut IS the sheared parallelogram, in 3 mm card, and the gate is: at 1:1 with a plumb line beside it, can a person see that the sill is not level? If 9.150 mm across 515.5 mm is invisible to the eye, the differentiator is invisible and the concept dies at zero dollars, in an hour, before any wood is bought.

*5. "The critical path is a third party's live service; 6–10 weeks, uncompressible, against an impatient owner."* **Half conceded, and the halves are now separated.** Step 1 needs no service, no staff, no release and no budget (see first step). The instrument itself needs no service either. Only the PAIRS need the kitchen. If the shoot cannot be scheduled inside six weeks, the instrument and its spec sheet ship and the cards do not — and I say which half survives rather than pretending the schedule holds.

*6. "'Shot during service' conflicts with an unsealed 26 kg wooden board on a live griddle line; health code forces the compromise the concept says means failure."* **Real and now designed around.** At 9 kg on two C-stands the frame stands OUTSIDE the pass, not on the line — it is a camera jig in front of the hatch, not furniture in the kitchen. Sealed with a food-safe two-pack over the cream. No part of it crosses a food surface.

*7. "'Cut from the mesh's own outline' vs 'a true 55 mm radius' — `T.rrect` uses seg=8, two different DXFs."* **Correct, and now there are three, all named with their deviations:** authored circle; the mesh's 8-chord polygon at 0.2648 mm sagitta; the ground-frame sheared arc at ±0.488 mm. The file cut is the third.

*8. "'The model is the cutting file, and without it this is decoration' is inflated."* **Withdrawn.** Replaced by the two-facts claim above.

**ORIGINALITY (1.5/4) — the heaviest lens, and I concede the prior art it named.**

*Penn's corner (1948) and Worlds in a Small Room (1974); Avedon's white seamless; the Bechers' typology protocol; Ruscha; Nixon's Brown Sisters. And "shot through the service hatch" is the 2020–21 takeaway window and, before it, the Miami ventanita.* **All named, in the object's own documentation, per early critic 1's finding 11.** I do not contest a single one.

**BUT THE DIFFERENTIATOR IS NO LONGER THE CONSTANT-INSTRUMENT CONCEIT, SO THE PRIOR ART NO LONGER BINDS IT.** Penn's corner is two flats at an arbitrary acute angle — an INVENTED constraint, and its arbitrariness is the point. The ventanita is a real window photographed as found. Every one of those instruments is either invented or inherited. This one is neither: it is a MEASURED FALSE RECTANGLE. An object that presents as a rectangle, is not one, and is not one for a reason you can read off a vehicle's stance and check with a plumb bob. Nobody's corner is 91.017°. And no prior instrument in that list has a spacer whose only job is to hold two halves 118.0 mm apart because that is the distance between a face and a hand.

**AND I REFUSE THIS LENS'S OWN FIX 1 — "cut the aperture from the off side, the flank no photograph has ever seen" — ON MEASURED GROUNDS.** Four of them, and the last is decisive. (a) `SPEC.md`'s table grades that flank **E (never photographed)** and gives it *"twin outward-hinged cargo doors + three glazed windows"* — there is no open serving aperture on that side to cut. (b) SPEC's own §10.62 records that the two features on that flank **CONTRADICT EACH OTHER** — the windows are a mirror of the show side while the cargo door was placed independently — leaving 804.9 mm of crossing that is *"a LABELLED regression catcher… a pass means the off flank has NOT MOVED, not that it is right."* (c) Shown the sightlines with every box printed, **the owner answered "cannot tell from this crop."** (d) **`design_out/sheet3_not_issued.svg` ALREADY SHIPPED THIS REVISION AND ITS SUBJECT IS EXACTLY THAT ELEVATION.** Its docstring: *"It is NOT a body outline: no outline of that flank exists in anything we hold, and drawing a plausible one is precisely the defect this project has paid for most often. The empty field is the measurement."* Cutting a physical 1:1 object from that flank would fabricate the geometry Sheet 3 refuses to draw, and would duplicate a shipped artefact. The fix is rejected and the reasons are in the machine.

*Fix 2, "make the rake visible or cut it."* **Taken, in the form the shear allows:** the plumb line in frame and the sheared sill against it. The rake is now visible in a single still.

**OWNER-AND-BRAND (1.5/4) — its two binding attacks.**

*1. "It arrogates brand authority he never gave — a permanent brand-photography policy for an operating multi-site business. The owner's rulings run the other way every time: 'focus on the 3d model', 'keep studio — ruling stands' (twice). Rule 34's shape at the brand level."* **Fully conceded. The sentence is struck.** It is a jig the kitchen owns and uses when it wants; one of several frames; it survives a second site precisely because it claims nothing about the first.

*2. "`PHOTOS_WANTED_rev52.md` item 7 — ONE HUBCAP, SQUARE ON AND CLOSE — has stood unanswered for twenty-four revisions. `STATE.md` still reads 'hubcap badge is SELF-CONSISTENCY ONLY — CAP_EMBLEM_WFRAC has never been compared to a frame.' A concept that cannot get one hubcap frame in twenty-four revisions will not get a scheduled kitchen shoot in one."* **The strongest objection any lens raised, and it is why the first step now needs nothing from anyone but him.** One sheet of paper, in his own hands, alone. No staff, no schedule, no service, no release. If that returns nothing, the concept has cost an hour and told us something true.

*Its fix 2, "move the confession off the customer-facing card."* **Taken, and further.** The reverse now carries a person, not an epistemology. The reveal-depth confession moved onto the sleeve, where it became a mechanism instead of a caption.

**DANGER (1/4, danger intact FALSE) — this lens was right and its three attacks are the reason this concept changed most.**

*1. "The danger is quarantined in the risk section. Risk 3 names scarred hands and a black griddle; that content appears nowhere in the artefact, the shot list, or the card."* **True. WHAT I PUT BACK:** the jug blender and the anonymous forearm are deleted from the shot list. The subject is a named person, photographed twice twelve hours apart, printed adjacent at the same size. What twelve hours does to a person's hands and face is now the content of the object rather than a warning about it.

*2. "Every rule is a prohibition. An anti-styling rule with no positive obligation produces competent documentary food photography, which the concept says it would rather die than become."* **True, and the prohibitions are gone.** In their place, two positive obligations: the matched 11:00/23:00 pair from an identical camera position, and a plumb bob hanging in every frame. The plumb line does the work the no-styling rule could not — a styled frame with a plumb bob in it reads as a document and cannot pretend to be a campaign. A mechanism, not a promise.

*3. "The card reverse prints the measurement and not the person. The corner radius gets 0.1 mm of precision; the cook gets no name, no station, no hours. That is where the whole concept's politics are decided and it spent all four lines on geometry."* **The sharpest sentence in sixty audit verdicts.** The reverse now carries name, station, both clock times and the interval to the minute. One dimension survives, 118.0 mm, and only because the two frames are about it. Publishing a line cook's shift length on a saleable object is a labour statement; that is a real risk to a hospitality brand and it is not being sanded off.

*Its fix B, "stencil the frame's blindness: THIS APERTURE SHOWS 767–1170 mm ABOVE THE FLOOR. NO FACE PASSES THROUGH IT."* **CORRECTED — the figures are wrong and the conclusion inverts.** Computed from `Z_SILL`, `Z_HEAD` and `rake_drop(x)`, the aperture spans **1312.1–1715.1 mm above ground at bay 0 and 1334.7–1737.7 at bay 2.** That is standing adult head height. A face passes through it; that is nearly all that passes through it. 767–1170 mm is not the aperture — it is roughly the counter zone, and the counter top measures 1189.8–1244.9. The auditor's instinct was right and its number was not, and the true number is better for the piece: the hole frames the face, the counter carries the hands, and 118.0 mm separates them.

**PROGRAMME-LEVEL CRITICS.** IP/trade dress (critic 1, finding 1): this object carries no VW mark and no T1 silhouette — exposure zero by construction. Consent (finding 9): no human from the reference archive appears anywhere; every frame is shot new, released, and paid, with the subject holding a veto. "No food in this food programme" (finding 7): conceded and answered by pivoting off food — the subject is the people, shot during service, and the food is whatever is actually in their hands. The confession tic (finding 4 and critic 2's SUBTRACT→CONFESS finding): exactly one confession survives, and it changed a design decision — the unknown dimension is the only one that moves. Prices (finding 3): five lines, below. F331 line: declared.

### MOTOR: NINGUNO — SILBATO 1:20  ·  LINE: children

**REGISTER** sound / child / three-dimensional — a played object, not a looked-at one  
**ARTEFACT** A two-shell moulded whistle: the measured vehicle's body at 1:20, **200.00 × 87.49 × 83.57 mm**, hollow, welded along the vehicle's own belt line, given to children at the door.

It has exactly two kinds of opening, and every other opening the vehicle has is moulded SHUT — the windows, the cargo doors, the engine lid, the roof aperture, the wheel houses, all of it.

**The three serving apertures** — 515.5 × 403.0, r 55, THREE, EQUAL — at 1:20 become three holes of 25.775 × 20.150 mm, r 2.75, 512.9 mm² each. They are the fingering. They are the cut Tacombi made.

**The engine-bay louvres** — ten slots over a 377 mm run — are the voicing window, always open. They are the intake Volkswagen cut for an engine that is gone.

You do not finger it. You lay the flat of your hand across all three apertures — 63.50 mm centre to centre, one child's palm — and roll the hand open. **It rises as the hand opens.** Hand flat, it sounds through the empty engine bay alone.

No paint. No decal. No roundel, no mural, no Calidad sunburst. One name moulded in, and it is his.

**MOTOR: NINGUNO. TRANSMISSION: SOLD.** This vehicle was stripped of the most recognisable noise ever fitted to a road car. Hand a child back a combi that cannot make an engine sound and only sings — and make it sing *through the hole the engine breathed through*.

That last clause is the whole amplification, and it came from the audit. The original had a whistle with no mouthpiece anywhere on it, which the feasibility lens correctly called fatal: with all three apertures covered, the only remaining port would be an invented window, so "cover all three and it sings low" was a note set by a feature the vehicle does not have. The purity claim broke at the one feature that made it an instrument.

It does not break now. **The voicing window is the louvre bay.** On a T1 the rear-quarter louvres are the engine's cooling-air intake; `t1_detail.py` builds them as a real aperture — 10 slots, `LOUV_APERTURE` 7.0 mm, over a 377 mm run — behind which `louvre_backing()` boxes a dark cavity because, in the source's own words, *"behind a T1's rear-quarter louvres is the ENGINE BAY — shallow, unlit and boxed off from the cabin."* At 1:20 that is a **65.98 mm²** window, which is squarely inside the range a fipple is voiced through. And the windway gap falls out of the mesh too: `LOUV_PITCH` is 21.111 mm, and 21.111 / 20 = **1.056 mm**, against the 0.8–1.0 mm a craft windway is cut to. The child's lungs replace the fan.

So the signal path is the vehicle's own history: **breath in where the engine was, sound out where the engine's air came in.** MOTOR: NINGUNO stops being a caption moulded on the underside and becomes the reason the object makes a noise.

**AND THEN THE MEASUREMENT CAME BACK BETTER THAN THE IDEA.** Running the Helmholtz arithmetic this session — the feasibility lens's own first fix, *"free and it is today"*, which nobody had done — the three apertures do not give three arbitrary pitches. Above the first fingered note they give **+490 cents and +802 cents**: a perfect fourth and a minor sixth, to within 4 cents of equal temperament. Root, fourth, minor sixth is **a minor triad in second inversion**.

And here is the part that matters: **that interval structure does not depend on the cavity volume at all.** The pitch does — and the pitch is genuinely uncertain, because a 2 mm wall takes a litre of envelope down to somewhere between 776 and 894 cm³ and moves the whole scale by two semitones. But frequency ratios depend only on the ratio of port conductances, and both ports are mesh constants. Wall thickness swept 1.0 → 4.0 mm, a four-fold range: the fourth moves 484.6 → 499.5 cents, the minor sixth 793.5 → 814.3. **The chord survives; the key does not.** The vehicle's cut determines what it plays. Nothing determines what it plays it in.

That is the object. A whistle whose scale was surveyed and whose pitch cannot be.

**THE OFF SIDE IS BLANK, AND THAT IS THE SECOND HALF OF THE IDEA.** `SPEC.md` grades the −Y elevation **E (never photographed)** — the same row rev 77 built an entire A2 drafting sheet around. The three serving apertures are on the show side only; `t1_shell.py` sets `SHOW_SIDE = 1`. So the whistle is fingered on one flank because the vehicle was only ever cut on one flank, and **the other flank is left smooth and featureless** — no louvres, no fuel flap, no shut lines, no inferred cargo doors. Not mirrored, not guessed. One side is the surveyed vehicle; the other side is the absence of a photograph, moulded at 1:20 and put in a child's hand.

Every die-cast maker in the world mirrors the side they could not see. This is the first object that refuses to.

**AND IT REFUSES A NUMBER ON ITS OWN FACE.** The measured aperture pitches are 625.0 and 645.0 mm — the 109.5 | 129.5 pillar asymmetry. The programme forbids it: 0.54 σ, and the model's asymmetry has the wrong sign against a photograph whose pillars are equal. So the whistle is moulded at an **equal 31.75 mm pitch**, the asymmetry is deliberately not reproduced, and the underside says so in Spanish. A children's toy that prints the measurement it declined to copy, and its sigma, is the strangest object on this bench and I am not taking it off.

**THE UNDERSIDE**, moulded, seven lines — the danger lens asked for the provenance of the shape and not only its absences:

```
   SEÑOR TACOMBI
   515.5 × 403.0 r55 — TRES, IGUALES
   PASO 31.75 — LA ASIMETRÍA 109.5|129.5 NO SE COPIÓ (0.54σ)
   EL COSTADO SIN FOTOGRAFÍA — GRADO E
   TECHO: ALTURA NO MEDIDA
   MOTOR: NINGUNO
   1:20
```

`STATE.md`: *"H_ROOF 1.960 is RETIRED as an accuracy target… the real vehicle's absolute roof height is OPEN and UNMEASURED."* That line has sat in the machine-written record for fifty-six revisions. It has never been on anything.

**THE RISK IT STILL CARRIES** — **THE CHARGE NOBODY WROTE DOWN, AND THE DANGER LENS WAS RIGHT THAT IT WAS NEVER PICKED UP. PICKING IT UP NOW.**

A Mexican street-food working vehicle was immobilised, gutted of its engine and gearbox, parked, and turned into a restaurant. This object reproduces it as a party favour and hands it to children on their way out of that restaurant. **The taquero's tool, as a souvenir, given away by the business that stopped it working.** Set against MOTOR: NINGUNO / TRANSMISSION: SOLD, that is the most uncomfortable thing available anywhere in this programme, and it is not a risk to mitigate — it is what the object is about. Every child who takes one home takes home a vehicle that will never work again, and the only sound it has left is the one their own lungs make through the hole where the engine breathed. **It is not sad by accident. Do not let a later pass make it cute.**

**2. TRADE DRESS, AND I AM NOT PRETENDING A DESIGN MOVE CURES IT.** A 200 mm three-dimensional replica of a T1 body is the most exposed object this programme could make. Omitting the roundel does not cure it — Volkswagen licenses toy bodies precisely because the *shape* is the asset. **The moulded disclaimer is DELETED.** The danger lens was right that "EMBLEM OMITTED, NOT LICENSED BY VOLKSWAGEN" is not a shield but a permanent, dated, physical record that the maker knew there was a mark and proceeded, and the original presented that admission as prophylaxis. **CEILING, STATED: I am not counsel, and the actual exposure cannot be recovered from what we hold.** Early Critic 1's remedy stands unperformed across the whole programme — one page of IP advice before any tooling spend, cheaper than one tool — and this object should be the one that finally forces it, because it is the worst case. The blank off side and the shut openings make it demonstrably not a replica of a Volkswagen; that is a real difference and it is not a legal opinion.

**3. I REFUSED THE OWNER-AND-BRAND LENS'S CENTRAL FIX AND SAY SO.** It said: stop making a bus, re-body it as a slab carrying the three apertures. That deletes the danger entirely. MOTOR: NINGUNO is meaningless on a slab; the funerary core is the *vehicle*, and a whistle shaped like a bar of soap is a safer object about nothing. What I took instead is the half of that fix that works: **his cut is now the instrument and VW's opening is now the void.** The apertures make the notes. The engine bay makes silence into a drone. The only wordmark moulded on the object is his.

**4. CHILDREN'S PRODUCT SAFETY IS COMPULSORY, COSTS REAL MONEY, AND CAN FAIL.** CPSIA and ASTM F963 in the US, EN 71-1/2/3 in Europe. Mouth-blown toys carry a recall history for detached mouthpieces — which is an argument for the welded two-shell with no separate mouthpiece part, and not an argument that testing is optional. 200 mm of body is far too big to swallow; that is why 1:20 and not 1:43, and it does not exempt anything.

**5. TWO HUNDRED CHILDREN WITH WHISTLES IS A DINING ROOM NOBODY WANTS TO SIT IN, AND THE ORIGINAL SURRENDERED THAT POSITION. PUTTING IT BACK.** It sounds at 150–525 Hz at a child's lung pressure. Nobody has measured how loud, and that should be measured off the first print with the same discipline as everything else. Given at the door on the way *out* is a real mitigation and it is not a complete one, because children do not wait until the pavement. **A restaurant that hands out whistles has decided something about itself.** That is his decision, it should be put to him with the measured level in hand, and if he says no it is dead — correctly.

**6. A SHARED MOUTHPIECE IN A FOOD BUSINESS** is a front-of-house conversation, not a designer's. One per child, kept, never returned to a bin.

**7. THE WAGER IS WELDED SHUT.** The apertures are 25.775 × 20.150 mm, r 2.75, 512.9 mm² — the measured serving apertures at 1:20 — and **they never get a scale of their own.** The original left itself that trapdoor and the danger lens caught it. Deleted. Two outcomes, both shippable, neither negotiable: it speaks, and the packet carries the note it actually made; or it does not, and he is handed a bus that stays silent, **which is a truer object about this vehicle than one that sings.** The predicted chord does not soften this — a Helmholtz model says what a resonator sounds at, never whether a fipple speaks at all.

**8. IT IS NOT F18.** A companion to the die-cut sticker, not a substitute. It does not settle the sticker's papel-picado question, which is still his to call.

**9. IT CARRIES NO ARTWORK, AND SPEC 10.10 LOCKS ABSOLUTE REPLICATION OF ARTWORK.** No mural, no script, no Calidad sunburst, no roundel. Rule 34: that bar's object is the MODEL. This is a derivative object and it OMITS rather than redraws — and it says so in moulded type instead of cropping quietly around the mark he has rejected nine times.

**10. THE CLAIM I DELETED, BECAUSE IT WAS FALSE.** *"Every VW bus toy ever made is a caricature… the first one whose proportions were surveyed rather than remembered."* Tamiya, Schuco and Minichamps work from factory drawings and CAD under licence. Gone, along with the market argument built on it. What survives is smaller and true: **the first object of this converted vehicle, and the first object anywhere whose tuning is derived from a survey and whose surfaces carry that survey's own uncertainty grades.**

**WHAT THE MODEL CONTRIBUTES** — **TOTAL, AND UNIQUELY SO — a whistle's shape is not its decoration, it is its transfer function.** Every other object on this bench could be drawn from a good photograph and a steady hand. This one cannot: the cavity volume, the port areas, the port ratio and therefore the entire scale come out of the surveyed geometry, and there is no other survey of this vehicle in existence. Change the mesh and the object plays a different chord.

Four things the model gives that nothing else could:
- **The apertures are equal.** `BAY_W = 0.5155`, ray-tested, three, equal — with the source's own note that SPEC's 0.507 / 0.516 / 0.526 taper was retired as a 100 mm origin error. Three equal ports is what makes a three-note scale honest rather than decorative.
- **The louvre bay exists as an aperture at all**, with a boxed cavity behind it, because rev 48 stopped treating the louvres as closed ribs laid on unbroken sheet. Before that revision there was no voicing window on this vehicle to find.
- **Zero non-manifold edges on the body**, which is what lets the shell be split, hollowed, thickened and printed without repair.
- **The uncertainty grades**, which are the only reason the off side can honestly be blank and the roof line can honestly say "not measured."

**THE BLOCKER IS DISCHARGED, AND I OVERSTATED IT — RULE 13.** The concept called the missing export path *"the whole gate on this concept… half a day of code."* It is one call. `bpy.ops.wm.stl_export` exists in this Blender 4.5.3 (so do `obj_export`, `usd_export`, `ply_export` and `export_scene.gltf`); `grep` across every `.py` in the tree returns nothing that uses any of them. Run this session against the built body it wrote **6,631,984 bytes, 132,638 triangles, in 17.58 ms**, and re-reading the binary gives 200.00 × 87.49 × 83.57 mm. The tree now has an export path because someone spent ten lines on it.

The still-real infrastructure gap is elsewhere and belongs to other concepts: there is **no UV unwrap and no bake**, so nothing textured can leave this tree. This object does not care — it has no paint by design.

**MEASURED FIGURES** — **MEASURED THIS SESSION, WATCHED PRINT.**

*Off the mesh, `T1_SUB=1`:*
- Body envelope volume by ray-fill, 260 × 260 grid: **8.095524 m³** (bbox 11.698500 m³, fill 69.2 %); shell material 0.060685 m³ against `STATE`-class 0.063157 — the 4 % gap is the grid, and it is the ray-fill's own floor.
- Cavity at 1:20, envelope: **1011.9 cm³**. With a 2 mm wall: **776–894 cm³**, the span being whether the shell's 47.214 m² counts one face or two. **PUBLISH THE BAND, NOT A FIGURE.**
- STL written and re-read: **132,638 triangles, 200.00 × 87.49 × 83.57 mm.**

*Ports, from `t1_shell.py` and `t1_detail.py`:*
- Aperture at 1:20: 25.775 × 20.150 mm, r 2.750, **512.9 mm²** — the concept's own arithmetic, reproduced.
- Louvre window at 1:20: 10 × 7.0 mm × 377.0 mm run / 400 = **65.98 mm²**.
- Windway gap = `LOUV_PITCH` / 20 = **1.0556 mm**.
- Palm span, outer aperture centres: **63.50 mm**. Pitches 31.25 / 32.25 mm — **moulded equal at 31.75**.

*The scale (lumped Helmholtz, c = 343.42 m/s at 20 °C, 2 mm wall, cavity band):*

| hand | f | note |
|---|---|---|
| flat — engine bay alone | 150–161 Hz | D3 … E3 |
| one open | 308–330 Hz | D♯4 … E4 |
| two open | 409–439 Hz | G♯4 … A4 |
| open — three | 489–525 Hz | B4 … C5 |

*The intervals, which are volume-free:* **+490.5 c** (perfect fourth, 498) and **+801.7 c** (minor sixth, 800) above the first fingered note. Wall 1.0 → 4.0 mm: **484.6 → 499.5** and **793.5 → 814.3**.

*Temperature:* 331.3 + 0.606 T gives 343.42 / 352.51 m/s at 20 / 35 °C = **+45.23 cents**. The concept's 45.2 and the auditor's 45.3 both reproduce. A warm mouth runs it nearly a quarter-tone sharp. That goes on the packet.

**FOUR CEILINGS, AND THE FIRST IS THE ONE THAT BITES.**
1. **`LOUV_APERTURE` = 7.0 mm is the softest number in this object.** Its own source says *"INFERRED, not measured — 1.5 px in `ref_side.jpg`, below its resolution… the one soft number in this block."* The whole tuning stands on it. Swept 6 → 8 mm the triad holds (fourth 483–499 c, sixth 792–813 c); swept 4 → 11 mm it degrades to 465–518 and 765–840 without becoming another chord. **But the drone's interval to the fingered notes swings 1073 → 1480 cents over that range — more than a fourth. The chord is determined by the vehicle. The drone's place in it is not, and it is a 1.5-pixel inference that decides.** The object sounds its own uncertainty grade.
2. **The lumped-element model is marginal at the top.** Body / wavelength runs λ/10.7 at the drone to **λ/3.3** at three open. Below about λ/10 the arithmetic is trustworthy; at λ/3.3 the cavity starts behaving modally and the top note will run flat of prediction. The drone is the note this model can predict.
3. **No Helmholtz calculation has ever predicted whether a fipple SPEAKS** — only what it speaks at if it does. Everything above is conditional on a labium that is not yet cut.
4. **200.00 mm, not 203.3.** The concept's headline dimension was the whole vehicle including counter and tail board (4.065 m). The shell alone is 4.0000 m. Corrected off the exported STL — rule 13, and it is my own number.

**COST / FEASIBILITY** — **ESTIMATES, NOT MEASUREMENTS — except the first line, which is done.**

- **STL export: DONE, this session, 17.58 ms.** Was budgeted at half a day. `bpy.ops.wm.stl_export`, ten lines, now in the tree where nothing of the kind existed.
- Split / hollow / cut the voicing window: **half a day to one day** of mesh work. Split on `Z_BELT` 1.2070 — the vehicle's own belt line — so the weld seam is a feature and not a scar. Everything but the three apertures and the louvre bay moulded shut.
- **First prototype, FDM or resin, two halves glued: 40–150 USD for three to five bodies, days.** This is the whole gate on whether it speaks.
- 50-piece printed trial for one restaurant: order of **8–15 USD each**. Fifty whistles for the price of a night's covers.
- Injection tooling, two-shell polypropylene with ultrasonic weld: order of **6,000–12,000 USD** for the tool — higher than the original's 4,000–9,000, because "one-piece moulded" was not manufacturable and the feasibility lens was right — plus roughly **0.60–1.50 USD** a part at 2,000+. Unit economics only work in thousands.
- **Third-party children's-product lab testing: 500–1,500 USD per SKU, NOT optional.**
- **IP advice before any tooling: unpriced and unperformed, and it gates everything above the prototype.**

**MATERIAL.** The originality lens is right that barro is the deeper tradition and that generic promo plastic is the part that has been done — the Mexican clay whistle runs continuously from Teotihuacan to a mercado stall this afternoon. I take half of it. The child's edition stays food-grade polypropylene, because it has to survive a tiled floor and a dishwasher and EN 71; but **the master is commissioned from a named whistle taller** — Ocumicho, Metepec and Santa María Atzompa are the traditions the audit named, and I have contacted nobody — who cuts the voicing and the labium, which is the one part of this object that cannot be surveyed and has to be *known*. **Their name is moulded on it and they are paid.** A 366,490-face survey handing the one unsolvable feature to a hand tradition is the collision worth having; the survey cannot cut a labium and should stop pretending otherwise.

**THE THREE ARITHMETIC REFUTATIONS, ANSWERED.** The port area is 21.6 % of the bbox cross-section against an asserted ≤ 8 % target — that target was never derived, and it is now superseded by an actual frequency calculation rather than a heuristic. The 10–14 mm fingertip cannot seal a 25.775 × 20.150 mm hole — correct, and it made the object better: the flat of the hand across 63.50 mm, rolling open. And 203.3 mm was the vehicle, not the shell; the shell is 200.00 mm.

**FIRST SHIPPABLE STEP** — **TWO DAYS, AND ONE OF THEM IS ALREADY SPENT.**

**Day 0 — done this session.** The export path exists. `bpy.ops.wm.stl_export` off the evaluated `T1_body` at `global_scale = 0.05` wrote 132,638 triangles measuring **200.00 × 87.49 × 83.57 mm**, verified by re-reading the binary. That was the concept's stated gate and it is discharged.

**Day 1 — the mesh.** Split the shell on `Z_BELT` = 1.2070. Solidify to a 2 mm wall. Boolean every opening shut except the three serving apertures and the louvre bay. Cut the windway at 1.056 mm and let the taller — or, for the first print, a craft knife — place the labium at the louvre bay. **Blank the −Y flank.** Export both halves.

**Day 2 — the object.** Print on any FDM machine, glue the two halves, and blow it.

**Then hand it across his own counter and say four sentences, in this order:**
1. *Lay your whole hand flat over the three holes and blow.* That note, if it comes, is the engine bay — the only opening left that Volkswagen made, and there is nothing behind it.
2. *Now open your hand.* It should rise through a fourth and then a minor sixth. **We did not choose those intervals. The three holes he cut in the side of the bus chose them, and they come out the same whatever we make the walls out of.**
3. *Turn it over.* The underside says the roof height was never measured and that one flank was never photographed. Both are true and both are in the machine-written record.
4. *Look at the other side.* There is nothing on it, because there is no photograph of it.

**He needs no crop, no mark and no multiple choice for this one.** He finds out with his own mouth whether it speaks. If it does, we measure the note and print what it actually is, not what we predicted. **If it does not, the underside still reads 512.9 mm² and he is holding a bus that stays silent — and that is the shippable outcome too, not the failure.**

**THE ONE THING THAT MUST HAPPEN BEFORE ANY TOOL IS CUT, AND IT IS NOT A DESIGN TASK:** one page of IP advice. It has been owed across the whole programme since the first completeness critic named it, nothing has been done, and this is the object that makes it unavoidable. A prototype in his hand costs 40 USD and needs no advice. A tool costs six thousand and does.

**HOW IT ANSWERED THE FOUR LENSES** — **FEASIBILITY (1/4).** (1) No voicing on the mesh, low note set by an invented feature — **answered**: the louvre bay is the window, 65.98 mm² at 1:20, and the windway gap falls out of `LOUV_PITCH`/20 = 1.056 mm. **Conceded and named: the labium EDGE is not on the mesh and cannot be. It is the one invented feature and a taller cuts it.** (2) One-piece moulding of a closed cavity is impossible — **conceded in full**; two shells welded on the belt line. (3) Port ratio vs an ≤8 % target — **superseded** by a frequency calculation. (4) Fingertips cannot seal the holes — **conceded, and it improved the object**: the flat hand, rolling open. (5) "Half a day" for STL — **my own overstatement, retracted, and the export is written.**

**ORIGINALITY (1.5/4).** (2) "First accurate VW bus toy" — **conceded false, deleted**, with the market claim built on it. (5) Barro not plastic — **half taken**: named taller cuts the master and is credited; the child's edition stays mouldable. (1, 3, 4) Prior art density and bench duplication — **the ground moved**: the claim is no longer "an accurate bus" or "a fingered vehicle," both of which are crowded. It is that the tuning is derived from a survey and carries that survey's uncertainty. No whistle has done that, and the mechanism — two air paths, one the owner cut and one the manufacturer cut — did not exist in any of the three bench titles this was accused of fusing.

**OWNER-AND-BRAND (1/4).** (2) The disclaimer — **conceded, deleted**; it was an admission dressed as a shield. (3) Market claim — **deleted**. (1) The inversion — **answered without re-bodying**: his cut is the instrument, his wordmark is the only mark, VW's opening is the void. (4) "Stop making a bus" — **refused, with the reason stated**: it deletes the danger, which is the fourth lens's whole brief.

**DANGER (3/4) — all three sandings reversed, plus the charge that was never picked up.** Trapdoor **welded shut** (no aperture rescaling, ever). Provenance **moulded**, seven lines, not just absences. The dining-room noise **taken back off the surrender pile** and given a measurement to make. And **the taquero's tool as a party favour is now written down and is the subject.**

**PUT BACK THAT WAS NOT THERE BEFORE:** a children's toy that prints, in Spanish, the measurement it declined to copy and that measurement's sigma — 109.5 | 129.5, 0.54 σ, wrong sign, refused; and one whole flank left blank because the vehicle was never photographed from that side.

### RUIDO  ·  LINE: adult

**REGISTER** People, hand-drawn, one ink — the Posada/TGP broadside's economics on a surface that gets thrown away. ADULT LINE, declared, and the tension declared with it: F331's option text pairs "free/handed-to-you" with children, and this object is free and handed to you. It is still adult, because its subject is labour and erasure and its captions are pixel residuals. A child cannot read "−16.7, −16.1, −13.6 px." Do not let the free/kept axis decide the audience; the subject decides it.  
**ARTEFACT** RUIDO — SIX SHEETS, 280 × 430 mm, ONE INK EACH, PRINTED ON 40 gsm GREASEPROOF. They are not broadsides to hang. They are the paper the food is served on: the tray liner. You are given one, you eat off it, and it is destroyed by the meal.

Six, not eight — the count is a correction, not a trim (see SURVIVED AUDIT).

FOUR ARE PRINTED (staff; releasable; on the serving paper):
1 · EL COCINERO — white cap, profile, looking down at his work; body visible through the bay-1 glass beneath his own head. ref_side.jpg, x 355–430, rows 258–320. Caption: "37 % OF THE VARIANCE IS THE MAN." Red on cream.
2 · EL DE LA COMANDA — white shirt, white apron, an order slip held in both hands, standing at the nose beside the roundel this project has failed nine times. ref_nolita_front34.jpg, cols 0–200. The best-resolved human in the entire reference set, face ~55 × 70 px. Caption: "NOT IN THE RECORD." Black on manila.
3 · EL MESERO — back to camera, right arm up, a stack of trays on the roof rail, a white cloth over the forearm. Same frame, cols 525–585. Caption: "NOT IN THE RECORD." Black on manila.
4 · LA QUE LO ABRIÓ — the woman standing inside the freshly cut roof, hands up at the lid, the bus still green, festoon lamps already fitted. ref_workshop.jpg. Turned away; no face. Caption, set as two lines and not one: "I FIGURED OUT HOW TO CUT OPEN THE TACOMBI." / DARIO WOLOS, FOUNDER — and beneath it, same 6 pt: "THE RECORD DOES NOT NAME HER." Green on white.

TWO ARE NOT PRINTED AND NOT SOLD (customers; cannot consent). One artist's proof each, unnumbered, to the owner and to the person if she can be found:
5 · LA NIÑA — blonde, magenta puffer, at bumper height, turned to the bus. Magenta on grey. Caption: "−16.7, −16.1, −13.6 px."
6 · LA MUJER DE LA MESA — chin on her hand, waiting. ref_rear34.jpg. Caption: "UNMEASURED."

THE DRAWING RULE, which is the whole craft position: EACH SHEET CARRIES EXACTLY AS MUCH INFORMATION AS ITS SOURCE AND NOT ONE MARK MORE. I measured every head. Where the frame holds ~35 px across a face in profile, the sheet holds ~35 marks. Nothing below the pixel is drawn, so nothing is invented — which is simultaneously the answer to "you cannot trace these" and the thing that protects the people. Posture and silhouette at full confidence; the face at the record's resolution.

THE ONE MODEL CONTRIBUTION, and it is now in the right frame: a single rule of 19.90 mm of gold across the foot of every sheet — CNT_NOSE_F 0.1860 × (CNT_ZT 1.2540 − CNT_ZB 1.1470), and t1_detail.py's own comment agrees, "19.9 mm of gold in elevation." AND IT IS NOT HORIZONTAL. It falls 17.75 mm per metre — the vehicle's own rake — so the food sits on a line that leans exactly as much as the bus stands. One constant, measured, corrected.

The record deleted these people eleven times out of eleven and called them noise. Draw them back in by hand, print them on the paper the food arrives on, and let the meal delete them again — this time with the reader watching, and with the reader doing it.

The original concept was a set of prints to hang. That is the fifth display object in its own bench doing the same move, and it is the fourth or fifth artist to do archive-extraction-printed-large since 2004. What no one has done — and what only a business that took the photographs can do — is put the recovered person on a disposable food surface and let it be consumed. The erasure is not described on the object. The object performs it.

That single change answers three separate charges at once. It defeats the gallery prior art (Rafman, Wolf, Rickard, Fontcuberta, Smejkal are all extract-and-hang; none of them is eaten off). It answers the completeness critic's "there is no food in this food programme" — the food physically lands on the person. And it retires the confession tic without softening anything: the grease does what a printed admission was going to say.

It also inverts the one concept the critic called the worst in the pool. LA SERVILLETA handed you a stranger's face to wipe grease off your hands with. This hands you the person who cooked your food, on the paper his own plancha oiled. Same physical gesture, opposite speech act — and that is exactly why the split by consent has to be the FORM of the object and not a policy note appended to it. Staff are printed because the object credits their labour. Customers and the child are not printed at all, because nothing about being photographed while eating consents to being reproduced on a product.

And the frame nobody opened is now the spine of it. See MEASURED FIGURES.

**THE RISK IT STILL CARRIES** — WHAT I PUT BACK, NAMED (fourth lens).
1. THE CAPTIONS STAY VERBATIM. "37 % OF THE VARIANCE IS THE MAN" is not softened. The tone control is authorship, not temperature: the sentence is the machine's in 6 pt, the man is at full size, and the reader can see who wrote which. Softening it removes the only reason the object exists.
2. THE FOUNDER'S SENTENCE STAYS under her, attributed and dated, with the record's silence about her printed beneath. This is the dangerous option taken on purpose.
3. DISTRIBUTION GOES UP, NOT DOWN — from 200 hung prints to tens of thousands of sheets a year that people touch, stain and discard. Exposure increases.
4. THE CHILD STAYS IN THE WORK as the one sheet that is not printed and not for sale. That is a harder position than printing her or cutting her, and it is the only one that keeps her without making her a product.

WHAT IT STILL CARRIES.
LIKENESS. Even staff-only, even released, a recognisable drawn person on a commercial food surface is §50/51 territory. Releases must be written, specific to THIS use, paid, and countersigned. A person who leaves angry does not recall the sheets already in circulation.
THE PROOFS. Sheet 5 and sheet 6 exist. A photograph of an unsold proof posted online is indistinguishable from commercial use.
THE PHOTOGRAPHERS. Six frames, no named author, no licence recorded anywhere in the repository. Drawing from a photograph is a derivative work. This is unresolved and I cannot resolve it from what we hold.
TONE. Six sheets is a sequence and a sequence has a shape. If the drawings are cold the captions read as a designer sneering at his own cook. The affection has to be in the line or the object is contemptible.
THE DRAWING RULE IS UNENFORCEABLE except by the illustrator. The moment one face is "improved," the argument collapses into an invented portrait of a real person.
AND THE DEEPEST ONE: WHETHER ANY OF THESE PEOPLE STILL WORK THERE, OR CAN BE FOUND AT ALL, CANNOT BE RECOVERED FROM WHAT WE HOLD. The frames are roughly 2006–2013. Every consent remedy in all four audits assumes findability, and nothing in this repository supports it. That is a real result and it gates the whole set.
LAST: the trade-dress finding from the first completeness critic is UNTOUCHED here. Sheets 2 and 4 have a VW roundel and a T1 silhouette in frame. One page of IP advice before any print run.

**WHAT THE MODEL CONTRIBUTES** — The model contributes ONE constant and that is the honest total — there is no human geometry anywhere in this tree, no person, figure, mannequin or silhouette in any .py file, and there never will be. In a programme where eleven of eleven concepts deleted the people, this one deletes the vehicle. That asymmetry is the concept.

But the one constant is now measured properly and it earns its place. The rule across the foot of every sheet is 19.90 mm of gold — CNT_NOSE_F 0.1860 × the 107.0 mm slab, corroborated by the source's own comment — and it falls 17.75 mm per metre because the counter is raked with the vehicle. Over the counter's 3.106 m run that is 55.1 mm; the slab top stands 1.1898 m above ground at the forward end and 1.2449 m at the aft. The food sits on a line that leans exactly as much as the bus does.

That is worth more than a level rule, and it exists only because the concept's original claim was wrong. "1.2540 m above ground" is the authored, un-dropped z, and t1_core.py forbids that conversion in terms. Correcting a frame error turned a decorative constant into a fact about how this vehicle stands.

What the model CANNOT give, stated plainly: the occlusion half of the owner's own locked style sentence is not built — there is no normal pass and no AO pass — so nothing here is "cartoon with rendered depth." These sheets are hand-drawn and one-ink by intent, so that absence does not block them; but no sheet may claim the house style until that pass exists.

**MEASURED FIGURES** — EVERY FIGURE BELOW WAS MEASURED OR RECOMPUTED THIS SESSION. WINDOWS PAINTED FIRST (rule 8); the painted files are named.

THE FRAME NOBODY OPENED — THE HEADLINE FINDING.
ref_nolita_front34.jpg contains AT LEAST EIGHT PEOPLE: a man in a white apron reading an order slip at the nose; the child at the bumper; a waiter reaching a tray stack onto the roof rail; THREE COOKS IN PAPER TOQUES in the serving apertures; two women customers at right. The record's entire description of this frame's humans, in 77 revisions, is LEDGER_rev47.md:263 — "a child's head occludes the lower quarter." This is the EXIF frame and the sagitta frame; it has been measured repeatedly and never once described as a photograph of people working. Two of the six sheets come from it and neither existed in the concept.
md5 ed2c33b0ec5e98b9130dc2b736480f19 — IMG_2060.jpeg IS ref_nolita_front34.jpg, byte-identical. Not a sixth duplicate group; §0.1's five pairs hold.

THE CHILD, PAINTED — probe_scratch/r78_F220_window_painted.png, probe_scratch/r78_people_nolita_bumper_4x.png.
Hair bbox cols 225–339, rows 240–375; tighter mask 100 × 121 px. SHE IS TURNED AWAY — three-quarter rear, looking up and left at the bus. NO EYES, NO FACE. The mitigation the concept asserted in prose is now MEASURED. She and LEDGER_rev47's child are ONE child in ONE frame, not two.
493 hair pixels fall inside F220's sagitta trace window (cols 128–256, rows 300–395) — the window's right edge cuts across her. That is the 3-of-106 contamination that moved the published sagitta 43 %.

THE COOK, PAINTED — probe_scratch/r78_side_vendor_roof_6x.png. White cap, PROFILE, looking down, mural behind, festoon lamps and counter below. Body visible through the bay-1 glass beneath his own head.

EL MESERO — probe_scratch/r78_plates_12x.png. Crop 60 × 35 px at 12×: roughly SIX DARK-RIMMED METAL TRAYS, ±2. THE COUNT CANNOT BE RECOVERED FROM WHAT WE HOLD, and they are not white china. "Eight white plates" is withdrawn.

THE MODEL'S CONTRIBUTION, RECOMPUTED.
gold band = CNT_NOSE_F 0.1860 × (1.2540 − 1.1470) = 19.90 mm — corroborated by t1_detail.py's own comment.
counter run CNT_X0 +0.9180 to CNT_X1 (X_TAIL −1.873 − CNT_OVERHANG 0.3150) = −2.1880, i.e. 3.106 m.
fall over that run = 3.106 × 17.75 mm/m = 55.1 mm.
slab top ABOVE GROUND = 1.1898 m forward, 1.2449 m aft.

RESOLUTION CEILINGS, which set the drawing rule.
EL DE LA COMANDA face ~55 × 70 px — the best-resolved human we hold.
LA NIÑA head 100 × 121 px. EL COCINERO face ~35 px, profile.
ref_side.jpg is 2.32 bits/px at JPEG DC quantiser 4, against 9.28 for ref_rear34.jpg (SURVEY_rev49_photoreal.md:965) — the worst frame in the repository, and one printed sheet comes off it.

ATTRIBUTION, VERIFIED — SPEC.md:41–43. "Figured out how to cut open the Tacombi" is DARIO WOLOS's, the founder's, first person, about his own act. Confirmed live.

**COST / FEASIBILITY** — The first completeness critic's charge — "not one concept has a price, a cost, a minimum order or a lead time" — answered with ranges, and the ranges labelled.

PRINT. Greaseproof serving paper, 280 × 430 mm, one ink, 40 gsm, flexo or single-colour offset. Commodity manufacture with a very large vendor pool. MOQ 5,000–10,000 per design; roughly $0.02–0.05 landed per sheet at 10,000; one plate or cylinder charge per design at roughly $75–150; 3–4 weeks. Four printed designs at 10,000 each: roughly $1,200–3,000 all in.
ILLUSTRATION. Six drawings — four for print, two as proofs — one illustrator, about a week: $2,000–4,000.
TOTAL TO A FULL RUN: roughly $3,500–7,500. Against the bench's vitreous enamel tooling, six-unit litho and cylindrical five-colour screen, this is the cheapest route into a new register in the whole programme, and it needs no Blender time, no render, no pipeline work and no AO pass — it does not compete with the machine for the four cores.
PILOT: one design, digital or short-run riso on greaseproof, 100–200 sheets: $150–400 and about a week.
RRP: ZERO. It is consumable, and that is a commercial position rather than a dodge — the tray liner is the highest-frequency brand surface the business owns and it is currently blank paper. The critic asked for sell-through; the honest answer is that this object has none by design and pays for itself as packaging it was already buying.
CEILING ON ALL OF THE ABOVE: these are trade-typical ranges, not quotes. Nobody in this project has bought anything in 77 revisions. Get three quotes before any of these numbers is repeated.
NOT COSTED, AND IT DOMINATES: finding the people, and the fees and releases owed to them. That is a fixer, weeks, and six fees. It is also, per the originality lens, the single move with no close precedent — and it is cheaper than the letter.

**FIRST SHIPPABLE STEP** — ONE SHEET, EL COCINERO, THIS WEEK — AND IT GOES TO HIM AS A QUESTION, NOT AS A POINT BEING MADE.

The concept's original first step was LA NIÑA with "ask him nothing." Both halves are deleted. The child is the highest-exposure subject in the set and the one who cannot consent, and "ask him nothing" skips the ruling on the riskiest object in the bench — in a programme where the only two things that have gone right, F330 and F331, were both got by asking.

THE PILOT IS THE COOK. He is staff, so he is releasable and payable. He is in profile under a cap brim, so posture and silhouette carry the whole likeness and no face has to be invented at 35 px. He carries the strongest sentence in the set. And I have already cropped and looked at him: probe_scratch/r78_side_vendor_roof_6x.png.

DO THIS WEEK: one drawing, one ink, printed on actual greaseproof at 280 × 430 mm — twenty sheets, digital or riso, under $200. Then put food on one and photograph it after the meal, because the grease is half the object and no one has seen it work.

THEN ASK HIM, with the question tool, multiple choice, one crop attached and one sentence — the crop being the cook, the sheet, and the greased sheet side by side. The question is the one only he can answer and it gates everything downstream:

"THESE ARE YOUR PEOPLE. WHICH OF THEM MAY WE DRAW?"
(i) Staff only, with releases and fees, on the serving paper.
(ii) Staff, plus the customers we can find and pay.
(iii) Nobody identifiable — archetypes, no real person.
(iv) Not now.

He has never read probe_rev39_flank.py and should not be asked to care that his record called a child noise. He should be asked whether his cook may be drawn. That is a question he can answer from a photograph, which is the standing rule for asking him anything.

WHAT MUST NOT SHIP UNTIL HE RULES: nothing printed at volume, no proof of the child leaving the building, and one page of IP advice on the roundel and the T1 silhouette that appear in two of the six sheets.

**HOW IT ANSWERED THE FOUR LENSES** — FEASIBILITY (1.5/4).
(1) "The source cannot carry portraiture — face 35–60 px; you cannot trace these; the drawing must be INVENTED around a blur." BINDS, and I accept the measurement — I re-measured every head myself. I REJECT the remedy. Re-shooting with today's staff produces a staff-portrait wall: a different, safer, worse object, and precisely the sanding the fourth lens exists to stop. The point is THESE people in THESE frames, subtracted by THIS record. FIXED INSTEAD BY MAKING THE CEILING THE MEDIUM: the sheet carries exactly the source's information and not one mark more. Nothing is invented because nothing below the pixel is drawn. The under-resolution is why the record deleted them and it is now why the drawing is honest.
(2) "SHEETS 2 AND 7 ARE THE SAME MAN." CONFIRMED — I cropped it at 6× and looked. The vendor in the roof opening and the "pale band" that turned out to be a shirt are one man, his body visible through the bay-1 glass. MERGED. The set is not eight. And the replacements are not padding: EL DE LA COMANDA and EL MESERO are discoveries from a frame no critic, no lens and no revision had opened.
(3) The photographers' copyright gap is real and unanswered by anything I can measure. Named in RISK.

ORIGINALITY (1/4) — the hardest and most correct audit.
"At least the fifth concept in its own bench doing this; sheets 1,2,3,7 ARE people-1's four cards; the core move is three famous bodies of work." BINDS COMPLETELY as long as RUIDO is a display object. Every antecedent named — Rafman, Wolf, Rickard, Paglen, Fontcuberta, Smejkal — and all five bench siblings are EXTRACT AND HANG. FIXED BY CHANGING WHAT THE OBJECT IS RATHER THAN WHAT IT DEPICTS: it is now the greaseproof the food is served on. No one has printed the recovered person on a consumable and let the meal destroy them. Its bench siblings cannot follow — a card, a napkin, a print and a garment are all kept.
"The machine-caption device is the bench's engine." Half-binds. Two of six sheets now carry NO record caption, because I checked and the record has no sentence about them. Their caption is "NOT IN THE RECORD," which is a measurement I made, not the device repeated.

OWNER-AND-BRAND (1/4).
(1) "'Put it in his hand and ask him nothing' is the worst line in the concept — an artefact built to make a point to the owner about our own record." ENTIRELY RIGHT AND DELETED. It skips the ruling on the highest-consent-risk item in the bench, and its motive was an apology from us to us. Replaced with a question tool ask (see FIRST SHIPPABLE STEP).
(2) "NY Civil Rights Law §50/51; a minor; free does not help; the mitigations run backwards." BINDS. FIXED STRUCTURALLY, not by drawing style: the consent split is now the object's form. Staff printed, customers and the child never printed and never sold.
(3) "Sheet 1 is a CUSTOMER, not staff." CONFIRMED BY LOOKING — and worse than the audit said. He is not obscured: he leans on the open cab door FACE-ON TO CAMERA, fully lit. Sheet 1 had the HIGHEST likeness exposure in the set, not the lowest. CUT ENTIRELY.
(4) Lead with LA QUE LO ABRIÓ. TAKEN as a printed sheet; not taken as the pilot — see FIRST SHIPPABLE STEP for why EL COCINERO leads instead.

DANGER (3/4).
(1) "The safety argument rests on an UNPAINTED WINDOW — rule 8, this project's oldest defect. She may be facing the camera and the mitigation void. The record may hold TWO children." DISCHARGED BY PAINTING IT. One child, one frame; turned away; no face; 493 of her hair pixels inside F220's own trace window. The mitigation holds and is now measured.
(2) "Sheet 5 is a live wire — that is DARIO WOLOS's first-person sentence, printed under a woman, and the concept does not mention it." VERIFIED AT SPEC.md:41–43 AND TAKEN AS OPTION (a), THE DANGEROUS ONE. Attributed to him by name, with "THE RECORD DOES NOT NAME HER" beneath it. The transfer becomes deliberate and legible instead of accidental.

THE ONE THING NO LENS CAUGHT — the concept's SINGLE model claim was in the WRONG FRAME. "The slab top at 1.2540 m above ground" is the AUTHORED, un-dropped z. t1_core.py says so in terms: "Do NOT use it as a frame conversion -- use rake_drop(x)." Above ground the slab top RAKES 1.1898 → 1.2449 m, 55.1 mm across the counter. The counter is NOT LEVEL. Correcting it made the contribution better: the gold rule now leans.
