# AUDIT rev 43 — the comprehensive specialist audit, run at last

**The owner asked for *"a complete and comprehensive workflow by a number of expert specialists"* and
later *"I think that we should conduct that audit workflow at some point, I believe you were one that put
it on ice."* He was right. It has now run.**

**8 dimensions across two lanes. 60 findings. Every one put to TWO adversarial refuters with DIFFERENT
LENSES — one told to reproduce it by a different method and default to REFUTED if it could not, one told
to test whether the datum is even admissible and what applying it would break. 25 of 26 agents completed;
only the final synthesis died on a session token limit, and this document is that synthesis written by hand
from the adjudicated data.**

| | |
|---|---|
| findings | **60** |
| survived both refuters | **55** |
| contested — one confirmed, one refuted | **2** |
| killed by their refuters | **3** |
| FIDELITY lane | 37 |
| DESIGN lane | 23 |

**WHAT WAS NOT AUDITED, AND IT IS A REAL LIMIT: there is no hero and no `out/` render in this tree.** The
rev-11 briefs say *"audit the rev-10 heroes as PHOTOGRAPHS"*; that was impossible. Every dimension audited
the **model source** and the **reference photographs** instead, and anything needing a rendered frame came
back NOT MEASURABLE rather than invented. Four dimensions — proportion, materials/weathering, script and
fascia — were run by hand in rev 11 and were **deliberately not redone**.


---

## 0. RETRACTION — THE HEADLINE FINDING OF THIS AUDIT IS FALSE

**"The ñ HAS NO TILDE. The word is built misspelled." IS WITHDRAWN. The tilde is there, and the
generator builds it.** The owner said so; the machine agrees with him.

**THE MEASUREMENT THAT SETTLES IT.** Connected-component analysis of both masks, run on the current
tree, no window chosen by hand:

| | detached component above the letter mass | size |
|---|---|---|
| measured photograph, `senor_trace._ref_mask()` | x 44–48, y 2–6 | **16 px** |
| generator output, `script_gen.senor_only()` | x 50–53, y 3–7 | **16 px** |

**Both masks decompose into SIX components and both contain the tilde.** `script_gen.draw_senor`
delegates entirely to `senor_trace.draw_senor`, so there is one path and it draws the mark.

**HOW THE FINDING WENT WRONG, and it is this project's most-recorded failure family.** It measured
the band **x 48–64, y −8..+2**. The photograph's tilde is at **x 44–48, y 2–6**. That window clips
the mark at **one corner** — which is exactly why the baked mask "held only 4 px" of a 16 px tilde.
On the photograph side the same window sits *above and to the right* of the tilde, over the `o`/`r`
region and the silver field; the "106 → 30 px, monotone, never vanishing" it reported is **other
letters' ink**. *A measurement window edge, not the object, decided the answer* — the same family as
the mask that dropped 14 % of the ink, the folk art column-scanned on a door swung open 49°, and the
three confident figures measured on a lamppost. **The `counter` dimension of this same audit names
that family explicitly. The `typography` dimension then fell into it.**

**AND IT EXPOSES A DEFECT IN THE HARNESS, WHICH IS MINE.** Both refuters confirmed it because **both
inherited the finder's window.** They were given different *estimators* — one an absolute-blue global
rule, one a local-median z — and told to default to REFUTED. **Neither was told to re-derive WHERE to
look.** Varying the method while holding the region of interest fixed is not independence.

> **NEW RULE, EARNED HERE: AN ADVERSARIAL VERIFIER MUST RE-DERIVE THE WINDOW, NOT ONLY THE METHOD.**
> A refuter handed the finder's region of interest can only ever re-measure the finder's mistake.
> Make the first question *"is the feature where they say it is?"*, and only then *"is the number
> right?"*

**CONSEQUENCE FOR THE REST OF THE `typography` DIMENSION.** Its other two severity-5s — *"the `e` is
not drawn as a letter"* and *"the capital S is built in three floating fragments"* — come from the
same finder, the same window family and the same pair of refuters. **They are hereby downgraded to
UNVERIFIED** and must be re-checked with the window independently re-derived before anyone acts on
them. Note that both masks decompose into **the same six components** with matching structure, which
is weak evidence *against* the fragmentation claim. **Nothing in this dimension is actionable until
it is re-run.**

**WHAT SURVIVES THIS RETRACTION.** The other seven dimensions used different finders and different
windows; they are not implicated by this specific error, but every one of their findings was verified
by the same two-lens design, so **the window-inheritance weakness applies to all of them.** Treat the
whole audit as verified against *method* variation and **not** against *window* variation until
re-run.

---

## 1. THE FINDING THAT MATTERED MOST — NOW RETRACTED, SEE SECTION 0 ABOVE

### ~~The brand name is built misspelled.~~ **WITHDRAWN — see section 0. The tilde is present in both the photograph and the generator.**

The original text is kept below because an unrecorded retraction gets re-raised.

**The ñ has no tilde.** Confirmed by both refuters, by methods sharing no step with the original or with
each other. One rebuilt the detector from scratch with an absolute-blue global rule: in the band where the
tilde belongs the photograph holds **106 → 30 ink pixels across thresholds B ≥ 12 … 32, monotone, never
vanishing**, while the baked reference mask holds **4** and the generator rasterises **1**. Area-matched at
B ≥ 32 — 950 photo px against the mask's 934 — the band still reads **30 against 4**. The second refuter
rebuilt the instrument independently, replicated its controls, and called this *"the strongest of the seven"*.

**The `branding` dimension found it separately:** the build says `Senor`, SPEC locks **`Señor`**, and §10.10
commands absolute replication.

**You rejected this script twice.** *"That script i see on the p9 hero is NOT it"* and *"there are a lot of
features that are missed or improperly displayed."* A missing tilde on the wordmark is not a subtle
shading defect — it is a spelling error on the name of the restaurant, and it has been in every hero.

Alongside it, same dimension, same severity: **the `e` is not drawn as a letter** — its bowl and eye are
gone — and **the capital S is built in three floating fragments** where the photograph is continuous.

---

## 2. SURVIVING FINDINGS, ranked

Each survived two adversarial refuters. Fix locations are **by symbol**, never by line number.


### severity 5

| dim | lane | finding | kind | fix location |
|---|---|---|---|---|
| `roof` | FID | The main lid is raked the WRONG WAY: LID_OPEN_DEG=104° leans the mural board away from the counter, the photograph leans it over the counter | ORD | t1_shell.py — LID_OPEN_DEG (and its comment), consumed by t1_shell.roof_lids via _hinge for lid_main, lid_board and the  |
| `roof` | FID | The open lid at the tail (the owner's "trunk lid", SPEC 10.26) does not exist in the model | ORD | t1_shell.py — t1_shell.roof_lids (no aft panel is emitted); build.py step 5 assigns nothing there |
| `typography` | DES | The ñ HAS NO TILDE. The word is built misspelled. | ORD | senor_trace.py :: _STROKES (no tilde branch exists); root cause upstream in the mask baked as senor_trace._REF_B64 |
| `typography` | DES | The `e` is not drawn as a letter — its bowl and its eye are gone, and the two counters that ARE built sit in the wrong glyph, an x-height too low and  | MET | senor_trace.py :: _STROKES[3..6] and _CUTS (both cuts mis-placed; no `e` bowl authored) |
| `sticker` | DES | VIEWPOINT — 18° front three-quarter from the serving side, eye height 1.55 m. The face and the flank are provably exclusive; choose the flank. | MET | NEW ASSET (does not exist): sticker_art master drawing. Data sources to draw from, by symbol: t1_shell.py :: roof_lids() |
| `sticker` | DES | OWNER QUESTION, MULTIPLE CHOICE — the cab door. Open at 49° opens a 0.306 m void that only a PERSON fills in the reference, and "nothing but the bus"  | MET | NEW ASSET: sticker_art, cab-door element. Governing symbols: t1_shell.py :: DOOR_GAP / DOOR_W / DOOR_H; folk_gen.py :: D |
| `sticker` | DES | THE FLANK IS A TRIPTYCH AND THE WORDMARK SITS IN A 1.51 m GAP WITH 63 mm OF CLEARANCE. Do not "enrich" the middle. | ORD | NEW ASSET: sticker_art, flank layout. Governing symbols: folk_gen.py :: OPEN_GOLD, BOUQ_GOLD, REAR_GOLD, DOOR_GOLD, FLAN |

### severity 4

| dim | lane | finding | kind | fix location |
|---|---|---|---|---|
| `counter` | FID | menucard0 hangs across the open mouth of serving bay 1 — 61.5% of it is over the hole | ORD | t1_detail.py :: menu_cards() — the first element of xs, the bare literal 0.9080; express it in terms of t1_shell.BAYS[0] |
| `counter` | FID | Bay 1's published contrast AND mean targets are a man in a white shirt; the fill wattage was chosen against the contaminated mean | MET | studio.py :: views(), the fill_galley block — the _gw / T1_FILLG1 default and the A/B target row in its comment; and t1_ |
| `counter` | FID | The counter carries two condiment caddies; no supplied frame shows fewer than four, and ref_side.jpg shows five | ORD | t1_detail.py :: galley_dressing(), section 7 — the gal_caddy{i} loop's two-tuple of (bx0, bx1) spans, and the 'image x 7 |
| `wheels` | FID | The tyres do not deform at the contact patch, so the whole vehicle stands 28.6 mm too high above its own ground plane — and this is the one ride-heigh | MET | build.py — step 7 wheel placement loop and step 8b `_is_wheel`/`_WHEEL_PREFIX` (a post-8b vertex deform, explicitly exem |
| `roof` | FID | The mural board mesh is 13.6 % more elongated than the texture it carries, so every flower head renders stretched along the bus | MET | t1_shell.py — t1_shell._lid_face and the roof_lids call that builds lid_board; coupled to LID_W / LID_X0 / LID_X1, which |
| `roof` | FID | The lid is built dead flat; the real lid is the cut-out roof skin and carries the roof's transverse crown | MET | t1_shell.py — t1_shell._lid_panel (the `z = 0.0` seed), which should take its section from t1_shell.roof_z at the lid's  |
| `roof` | FID | lid_rail has exactly zero surface area — the lid's perimeter rail renders as nothing, and the object-count guard passes anyway | ORD | t1_shell.py — the `for (xa, xb) in ((LID_X0, LID_X0), (LID_X1, LID_X1))` rail loop in t1_shell.roof_lids, and t1_shell._ |
| `tail` | FID | The flat tail panel is 0.996 m tall; the photograph's aft silhouette cannot be flat over more than 0.71 m | ORD | t1_core.py — the aft knots of ZT_ALL, ZB, RT_ALL and RB_ALL at the tail station (all consumed through aft_lut) |
| `tail` | FID | The "1963" plate is 74 mm too low on the engine lid, which drops the T-handle off the lid onto the apron | ORD | t1_detail.py — PLATE_Z (plate_1963 and englid_handle both inherit it through PLATE_OUTER_CZ) |
| `tail` | FID | The trunk lid at the tail, owner-stated and open in the primary frame, is not built | ORD | t1_shell.py — roof_lids (and the matching cut, alongside engine_lid_gap) |
| `optics` | FID | The festoon string is one uniform emitter and its cable emits too — 27.9% of the lit area is wire, and no lamp can differ from any other | ORD | t1_mats.build_all → M["bulb"] and t1_mats.emissive (emission chromaticity is coupled to strength: at 9.0 the blue channe |
| `typography` | DES | The capital S is built in three floating fragments, and the photograph is CONTINUOUS through all three breaks. senor_trace declined to bridge them on  | ORD | senor_trace.py :: _STROKES[0]/[1]/[2] and the WHAT THIS REPRODUCES docstring premise |
| `branding` | DES | REPORT 7 CONFIRMED — but the datum is the SUNBURST, not the texture, and texture-centring under-delivers and still misses the band | MET | cal_gen.py :: main() — the paired glyph_100(t, w*0.150, ...) and glyph_calidad(t, w*0.180, ...) origins and their h*0.22 |
| `branding` | DES | The brand mark is built as "Senor", SPEC locks "Señor", and §10.10 as written commands the misspelling | ORD | senor_trace.py :: _STROKES (the `ntilde` group) and script_gen.py :: draw_senor; SPEC.md §3's script inventory row, whic |
| `sticker` | DES | THE SACRIFICE RULE IS ALREADY MEASURED: 48 of the flank's 66 gold components carry 2.29% of the ink and every one lands under 0.40 mm. Delete all 48. | MET | NEW ASSET: sticker_art, ornament layer. Governing symbols: folk_gen.py :: COMP_TOP, COMP_HIST, FLANK_MASSES, FLANK_ROSET |
| `sticker` | DES | DIE-CUT OUTLINE — bridge the underbody with the cast shadow, and let no feature narrower than 0.159 m touch the cut line. | MET | NEW ASSET: sticker_art, cut path. Governing symbols: t1_shell.py :: roof_lids() (lid_strut), signboard() (must stay off) |
| `sticker` | DES | LINE WEIGHT AND THE DEPTH BUDGET — three strokes, a 0.15 mm floor, four contact lines, and DO NOT outline the paisley. | MET | NEW ASSET: sticker_art, line and shading system. Governing symbols: t1_mats.py :: RED, CREAM, GOLD; folk_gen.py :: the r |
| `sticker` | DES | THE SUN — it must NOT be a rayed disc. The vehicle already carries ELEVEN radial bursts, and it is the drawing's only light source. | ORD | NEW ASSET: sticker_art, sun element and global light direction. Governing symbols: lid_gen.py :: mural(), HEADS_UV, HEAD |

### severity 3

| dim | lane | finding | kind | fix location |
|---|---|---|---|---|
| `counter` | FID | The forward half of the counter is bare in the model; the standing 'CLUTTER ON THE COUNTER' instruction is answered only aft of X = -0.686 | ORD | t1_detail.py :: galley_dressing(), section 7 (counter top, show side) — it needs entries forward of gal_warmer, starting |
| `counter` | FID | The two inter-bay pillars are 109.5 and 129.5 mm; the photograph's are equal, and the model's asymmetry has the wrong sign | MET | t1_shell.py :: BAY_CX — the centre spacings 0.6250 / 0.6450 were not re-derived when BAY_W was equalised in rev 13 |
| `counter` | FID | The aperture bobble fringe is pitched 26.0 mm against 32.4 mm measured — ~13 extra balls per aperture, 39 across the three | MET | t1_detail.py :: FRINGE_PITCH (consumed by bobble_fringe via _resample_closed) |
| `wheels` | FID | The tyre is built ~150 mm in section against the 205–215 mm its own comment and REF's fitment identification require — and the constant is not even th | MET | t1_core.py:`TIRE_W` (and make `t1_detail.tyre`'s profile reference it instead of ±0.0752); SPEC.md §2 tyre row, "section |
| `wheels` | FID | folk_gen masks the folk art to a 0.747 m CIRCULAR rear arch that t1_shell stopped building in rev 16 — the two modules disagree about the shape of the | MET | folk_gen.py:`arch_top` (and its `ARCH_R`-only import) — it must call the same profile t1_shell.`rear_arch_outline` uses, |
| `wheels` | FID | The front arch aperture is 0.747 m wide against the rear's measured 0.920 m — a 23 % front-to-rear asymmetry in one side elevation, on an arch that ha | MET | t1_shell.py:`arch_cutters` front branch / a front counterpart to `ARCH_W_REAR` — but NOT before a front-arch measurement |
| `tail` | FID | The rear-quarter louvre block has twelve slots, not ten, and the built block is two slots short | ORD | t1_detail.py — LOUV_N and LOUV_Z_TOP (consumed by louvres) |
| `tail` | FID | The "1963" lettering is half size — 48 % of the plate's width photographed against 22.4 % built | MET | t1_detail.py — plate_1963 (the 0.0210 digit pitch and the 0.0110 digit width passed to _seg_bars) |
| `tail` | FID | The tail lamp is a surface of revolution; the photographed lens is a stadium, and SPEC sec.4 says oval | ORD | t1_detail.py — small_lamp (called for tail{s} in build.py; needs an elliptical or stadium section, not a revolve) |
| `tail` | FID | The engine lid is a bare sheet — the photograph's pressed relief inside the shut line is not built | ORD | t1_shell.py — engine_lid_gap (or a new pressed-relief detail in t1_detail.spec4_details) |
| `optics` | FID | post.CA_COEF puts 6.8× to 41× more lateral colour into the frame than any of the three reference photographs carry | ORD | post.py → CA_COEF (module constant), consumed by post.chromatic |
| `optics` | FID | The real matte exists in studio.py and the hero path can never use it, so every shipped frame is scaled on the heuristic mask | ORD | hero.py → main (stitch the per-strip mattes under the same row-ownership rule it already uses for the beauty strips, set |
| `typography` | DES | Letterform detail is smoothed away: the same ink laid down as fewer, fatter strokes — 20% less outline at equal area. | MET | senor_trace.py :: _chunks + BOUNDARY_SIGMA_PX; script_gen.py :: Canvas.stroke (caps=True at every chunk join) |
| `branding` | DES | cal_gen guillotines its own bunting and the burst's foot on the panel edge — 41% of the bunting and 5 of 15 pennants are simply absent | MET | cal_gen.py :: main() — the two bunting(d, h*0.150, ...) / bunting(d, h*0.290, ...) calls, and starburst()'s cy = h*0.575 |
| `branding` | DES | The build reproduces the ELEMENTS but not the SYSTEM — the same painter's red is four unreconciled numbers under three exposure conventions, and resol | ORD | cal_gen.py :: RED/ORANGE/YELLOW, lid_gen.py :: RED/ORANGE/GOLD/DARKLINE, folk_gen.py's colour classes and t1_mats :: RED |
| `sticker` | DES | COLOUR SEPARATION — the whole vehicle is ONE 70° hue wedge plus four neutrals. Seven inks printed; five if cut, and the fifth casualty is the silver s | ORD | NEW ASSET: sticker_art, colour separation sheet. Governing symbols: t1_mats.py :: RED, CREAM, GOLD; lid_gen.py :: GROUND |

### severity 2

| dim | lane | finding | kind | fix location |
|---|---|---|---|---|
| `counter` | FID | Nothing in the model stands on the counter's 315 mm tail overhang, and the four squeeze bottles that claim to are all forward of the tail | ORD | t1_detail.py :: galley_dressing(), the gal_bot{i} loop — the station list and the 'TAIL RUN' claim in its comment |
| `wheels` | FID | REF §2's front-arch numbers are traced on the swung-open cab door, not on the arch — the 0–25 mm front gap must not be used | ORD | REF_MEASUREMENTS.md §2 "Arch-to-tyre gap, FRONT"; t1_shell.py:`arch_z` docstring |
| `wheels` | FID | Ride height adjudicated: the bus IS lowered, the route is hub-referenced, and SPEC §0.2's bullet is a stale rev-4 entry that SPEC's own §2 row already | ORD | SPEC.md §0.2 — strike or annotate the "bus lowered 65 mm / 110 mm ... Stock ride height" bullet against §2's Ride height |
| `wheels` | FID | The wheel arch aperture is a bare knife edge — no rolled lip, no returned flange, no edge radius anywhere in the geometry | ORD | t1_shell.py:`arch_cutters` / t1_detail.py:`_arc_liner` — a returned lip belongs on the shell, not on the liner; alternat |
| `tail` | FID | TAIL_LAMP_OD was set from an image-height ratio across 183 px of depth with no depth correction | MET | build.py — TAIL_LAMP_OD (the 1.1627 coefficient) |
| `optics` | FID | The glazing is not clear glass: Base Color tints every transmission event, so a 6 mm 'float glass' pane loses roughly a third of the light and goes gr | ORD | t1_mats.build_all → M["glass"] (drive Base Color toward white and move any green edge tint to a Volume Absorption with a |
| `optics` | FID | Bloom is defaulted OFF on a precondition the same revision satisfied — the shipped frame carries no veiling glare at all | ORD | post.py → _FLOATS["bloom"] and the comment block above it; hero.py → main (the T1_FX=0 decision is right; the glare has  |
| `typography` | DES | The lid lettering: four of the seven glyphs are invented, they occupy 76.5% of the word, and two source comments report the invention as a reading. | MET | lid_gen.py :: front_sign (the `after` glyph list) and build.py's comment on A(sign_boards[0], "lidsign") |
| `branding` | DES | §10.10's eight-row scope table is contradicted by three later owner-settled sections of its own document, and row 7 still commissions an element the o | ORD | SPEC.md §10.10's scope table (all eight state cells, and row 7 struck); lid_gen.py module docstring section 0; build.py' |
| `branding` | DES | The pillar menu card builds three of the five design features its own generator resolved, and the missing one is unreachable in the shader graph it wa | ORD | t1_detail.py :: _gcard() — the BANDS list and the single Separate XYZ Z link that constrains it. |
| `branding` | DES | The "1963" plate digits are SEVEN-SEGMENT bars — a digital idiom the vehicle predates — on a crop that has been admissible since rev 9 | ORD | t1_detail.py :: SEG and _seg_bars(), consumed by plate_1963(). |

### severity 1

| dim | lane | finding | kind | fix location |
|---|---|---|---|---|
| `roof` | FID | t1_detail defines gutter() twice; the shadowed first copy carries the exact drip-rail formula rev 16 removed | ORD | t1_detail.py — the first `def gutter()` (in the VW-disc block), shadowed by the second |
| `optics` | FID | REFUTED at source: 'all glass reads as a mirror', 'bloom clips the whole frame', 'zero vignette, zero backdrop noise' are all dead findings | ORD | build.py → _FLAT_SHADED / A(); post.py → BACKDROP, _FLOATS, main (NO EDIT — retire these three from the standing-finding |
| `branding` | DES | Both decal panels state an aspect in a comment that their own constants do not produce | MET | build.py :: the SCR and CAL dicts and their trailing '= tex AR' comments — z1 derivable from the texture's own pixel asp |

---

## 3. CONTESTED — one refuter confirmed, one refuted. A third route is needed.


**[typography, sev 3] The whole word is bottom-heavy: the reconstruction starves the diacritic and x-height band and over-inks the baseline band. The sign never flips.**

* **REFUTED** — The finding's entire content is that a SIGN is invariant. It is not — it is an artefact of the local-median background, and I demonstrated the mechanism directly rather than merely disagreeing. First I replicated the original instrument and reproduced its numbers (z > 6 over mask x 4-92 with the split at the x-height: upper 504 / lower 495, up:lo = 1.018; the quoted baked 334/501 and built 327/497 reproduce exactly). Then I measured the instrument. The 25 px median background it subtracts is 4.68 DN in the sparse upper band and 16.06 DN in the ink-dense lower band. On the SAME baked-ink pixels, raw z is 28.4 (upper) against 30.8 (lower) — the lower band's ink is if anything stronger — and af

* **CONFIRMED** — This is the cleanest finding in the set and it replicates almost exactly. Independent rebuild, same two boxes (I used the _REF_B64 window x6–88 rather than their x4–92, which is off the mask): photo upper/lower = 502/466, 463/433, 427/391, 403/351 at th 6/8/10/12; built 327/497; baked 334/501. Built-over-photo = 0.65 / 0.71 / 0.77 / 0.81 in the UPPER band and 1.07 / 1.15 / 1.27 / 1.42 in the LOWER — always short above, always long below, at every threshold, against their 0.67/0.74/0.79 and 1.08/1.16/1.29. The result also survives despeckling (dropping every component under 5 px, which they did not test): 0.65/0.71/0.77 and 1.07/1.17/1.29. 'The built decal tracks the mask to within 2%' checks


**[typography, sev 2] senor_trace's 'NEAR-MONOLINE — nothing invented' describes a statistic that was trimmed of exactly the parts that get drawn. As authored the word carries 3–4× pen modulation sourced from mask noise.**

* **REFUTED** — Every number on the model side reproduces — and that is what kills it. Reading _STROKES column 2 directly with numpy: exactly FOUR branches (not five) have p95/p5 >= 3.0, namely [11] 0.74->2.56 (3.45), [12] 0.73->2.94 (4.05), [24] 0.79->2.68 (3.40), [25] 0.76->2.69 (3.54); S upper arc [0] median half-width 3.27 against tail [2] 1.17, ratio 2.79. All correct. But the two claims that would make this a DEFECT both fail. (a) CONCEALMENT. Pooling every point of every branch UNTRIMMED, I get half-width p5/p50/p95 = 0.98/2.22/3.42, i.e. FULL WIDTH 1.97/4.44/6.84 px — which is, to rounding, the figure senor_trace's docstring publishes two sentences after the trimmed one: 'Pooled stroke width p5/p50/

* **PARTIAL** — THE ARITHMETIC IS EXACT AND I REPRODUCE IT TO TWO DECIMALS off _STROKES column 2: [11] p5→p95 0.74→2.56 = 3.45, [12] 0.73→2.94 = 4.05, [24] 0.79→2.68 = 3.40, [25] 0.76→2.69 = 3.54, and median half-width 3.27 on _STROKES[0] against 1.17 on _STROKES[2] = 2.8× inside one glyph. No dispute on any number. THE DEFECT CLAIM DOES NOT FOLLOW, on three counts. (1) It is not the stale-comment failure mode it invokes. That failure was a figure whose qualification had been lost thirty revisions earlier; here 'Trimmed 3 px back from junctions and terminals' sits in the SAME SENTENCE as the 1.25 and the 0.32, so a reader is told exactly what was excluded. Disclosed scope is not a misrepresentation. (2) The


---

## 4. KILLED BY THEIR REFUTERS — recorded WITH REASONS

**An unrecorded refutation gets re-raised next revision.** That is how this project has wasted revisions
before, so each one is kept with the reason it died.


**[roof, sev 3] Two-sided lid artwork: exactly one of the two authored board faces is built, and the second authored texture reaches no admissible hero**

* REFUTED — The sub-facts are all true — one _lid_face call, a one-element boards list, build.py:285 assigns lid_boards[0] only, tex/lidsign.png referenced once inside the gated T1_SIGNBOARD branch, STATE.md lid_board 1 — and I verified every one. But the CONTRACT the finding rests on was retired eleven revisions before this tree. lid_gen.py's header is a rev-11 document: it states 'ref_rear34.jpg region D … is the OTHER FACE OF THAT SAME LID' and writes two textures 'for one board' on that basis. SPEC 10.28 (rev 12) records the owner reversing exactly that: asked what the cream lettered panel is, he said

* REFUTED — The 'source contract' is a stale rev-11 document that the owner overturned in rev 12, and the finding quotes it with its own hold clause removed. HANDOFF_rev11's item 1 — the very passage cited as spelling out the implementation — ends: 'Hold this until §10.26's open questions are settled — it is not yet established that the mural and the lettering are two faces of the same panel.' That condition then resolved AGAINST it, twice over: SPEC 10.26's owner-settled table assigns the cream/red-script artwork to a DIFFERENT panel from the flower mural, and 10.28 item 3 records him retiring that panel


**[roof, sev 2] No hinge hardware is built anywhere on the lid's hinge line, where the photograph shows a regular row of it**

* REFUTED — I could not reproduce the periodicity, and at magnification the feature is not there. I de-slanted the band along my own fitted board-bottom line (y = -0.014346x + 298.620) over the stated x 455-790 and took the FFT of the min-luma profile at offsets 2, 4, 6, 8 and 10 px below it: the dominant periods come out 28.0-33.6 px and 48 px (and 6.0-6.3 px at offset 10, which is the festoon bulb pitch), never the claimed 19.7 and 22.3 px. I then looked directly: at 12x over x 520-660 the band between the mural's bottom trim and the drip-rail festoon is a plain dark shadow strip with a few irregular sm

* REFUTED — I could not reproduce it, and I looked hard. Working the same band — between my own fitted mural-bottom line and the drip-rail festoon line, x 455-790, de-slanted along the bottom edge — the min-luma profile's dominant periods come out at 47.6 px and the mean-luma at 27.1 px, neither of which is 19.7 or 22.3; peak detection at prominence 8 finds 11 minima, not ~15, with spacings running 11 to 82 px, i.e. irregular. Visually, at 12x on x 460-620 and again on x 620-790, and on a per-row contrast-stretched de-slanted strip, the band shows a smooth shadow, a metallic rail and a few irregular smudg


**[optics, sev 1] ADJUDICATED, no change: the show-side serving apertures are NOT glazed — three independent signs, all one way**

* REFUTED — All three signs fail their own positive control, which is in the same photograph and which the finding never ran. The cab door in ref_side.jpg is swung open and its pane is unambiguously glazed — I proved that photometrically before using it: the same wall seen DIRECTLY beside the door reads RGB 169.8/140.7/128.0 at mean saturation 42.2, and seen THROUGH the pane reads 108.3/95.9/87.8 at saturation 22.1, i.e. darkened and desaturated by a transmitting layer. Running their three statistics on that known pane, same script, same frame, same light: (1) CHROMA — B-R = -16.0 with 16.5% of pixels blu

* REFUTED — The recommendation (do not glaze) is right; the evidence offered for it is not, and it cannot close HANDOFF_rev13 item 9. I reproduced their three bay windows to the digit — B-R -8.3 / -8.2 / -10.7, frac(B>R) 22.1 / 30.6 / 22.7 %, top-third minus bottom-third -4.4 / -15.7 / +3.0, sigma=3 high-pass sd 10.90 / 13.10 / 11.12, means 147.7 / 158.0 / 178.3, which match studio.py's own recorded photograph means exactly — and then ran the POSITIVE CONTROL they did not: the CAB DOOR GLAZING in the SAME frame, the same street, the same light, a pane that is indisputably glass. Over u[150,206] v[350,412]


---

## 5. METHOD AND CEILING, per dimension

**No self-assigned scores anywhere. Every dimension states the best its method could achieve.**


**COUNTER — counter, serving bays and galley** — *FIDELITY*  
**Ceiling:** Positions and lengths on the show flank: +-3 to +-5 mm, set by +-0.5 px half-max edge location converted through the ONE locked in-plane ruler (BAY_W = 0.5155 m read on each bay's own edges). That ruler was validated blind — it predicts the counter's forward end at image x 325.9 against an observed 326 +/- 3 — and it never leaves the flank plane, so it is untouched by SPEC 10.11's ground line, 10.62/10.73's door plane, and 10.99.6's outboard-parallax term. Counts and orderings: exact, no ruler involved. The photograph's per-bay contrast: sd to +-1.0 DN (four estimators spanning 0.18, plus +-0.9 for +-3 px window placement) — except bay 3, which is estimator-limited to +-1.5 because its sd falls 21.9 -> 18.9 across an 8 px inset sweep. Ratios of two lengths on one plane (fringe pitch/bay width, caddy height/pitch): limited only by the edge error, ~2%. HARD CEILING ON THE WHOLE REPORT: no 


**WHEELS — wheels, tyres, arches, contact shadow (+ the assigned ride-height adjudication)** — *FIDELITY*  
**Ceiling:** Every number I publish rests on one 141-px-diameter wheel in ref_side.jpg — the worst-compressed frame in the set (2.32 bits/px, DC quantiser 4, against 9.28 and 8.87 for the other two). Sub-pixel max-gradient edges there land at sd 0.34 px on a clean cream/black step (the rim flange, 357 rays) and 0.8 px on a dark-on-dark step (the tyre against the arch cavity, 140 rays). The only ruler is the tyre's own locked diameter, which itself carries SPEC's ±15 mm on 665 (±2.3 %). So the FLOOR on any hub-referenced length at that wheel is about ±0.5 px ≡ ±2.4 mm, plus 2.3 % of the length: ±2.3 mm on the 28.6 mm contact deflection, ±2.5 mm on the 372.9 mm arch-lip height, ±2.4 mm on the 40.4 mm arch gap. A perfect model would still read those numbers back at exactly that spread, and no sharper figure is obtainable from these three photographs — the two untracked thumbnails that appeared during th


**ROOF — roof, lids, mural board, menu strips** — *FIDELITY*  
**Ceiling:** The ceiling on this dimension is set by what ref_side.jpg can carry at the LID PLANE, and it is asymmetric. SIGNS, ORDERINGS, COUNTS and RATIOS on the roof are settled to the quality of my edge fits — 0.42 to 0.50 px rms over 200 to 356 samples, and my independent RANSAC reproduced lid_gen's published board corners on three of four edges to 0.1 px — so findings 1, 3, 4, 5, 6, 7 and 8 are as good as this evidence gets and would not improve with a better model. Everything ABSOLUTE on the lid is capped well short of the owner's per-measurement bar: there is no admissible px/m at the lid plane (the lid stands 130-500 mm outboard of the flank whose 212.79 px/m I measured off the 2.400 m wheelbase), the ground-line datum is barred by 10.11, ref_rear34 is suspect by 10.15, and lid_gen's own three aspect routes span 1.520 to 1.82 — so the lean magnitude cannot be tightened past [63°, 76°], the t


**TAIL — tail and rear quarter** — *FIDELITY*  
**Ceiling:** The ceiling on this dimension is set by the two photographs and by the absence of a render, not by care. Best case: (a) The plate-versus-lid offset is limited by which of the two candidate upper lines is the lid's shut line — my reading (lid height / plate height 2.944 measured against 2.972 built, 0.9 %) strongly favours the upper one, but the alternative moves the answer from 74 mm to 102 mm, so the metric cannot be tightened past +28/-0 mm systematic on about ±8 mm statistical. The ORDINAL half of it — the T-handle is 47 mm below the lid's lower shut line in the model and 26 mm above it in the photograph — is not subject to that and is as certain as the shut-line fits (residuals 0.31 and 0.44 px). (b) The louvre count is capped at a FLOOR of twelve, because the block's top trough sits 3.8 px below the counter fascia and slots above it cannot be excluded; and it presumes one dark line 


**OPTICS — glass, reflections, lighting, camera** — *FIDELITY*  
**Ceiling:** I never saw a rendered frame, so the ceiling on this dimension is hard and asymmetric. Every "model does" statement above is a read of the .py source or exact arithmetic on its constants — those are not estimates and carry no error bar (118 lamps, 28.6 mm pitch, 27.9% of lit area in the cable, 6.6 mm envelope gap, 4.9 mm cable clearance, one commit since rev 8). Every "reference shows" statement is a measurement of the supplied JPEGs, whose ceiling is set by 2×1 chroma subsampling (chroma blocks 16 luma px against a 6.00 px lamp pitch, which is why the per-lamp colour limb is barred and only the band mean survives) and by the fact that no supplied frame is of the studio scene the hero renders. What NO method here can reach is the display-referred pixel value of any hero: the source values are inputs to Cycles and then to AgX, and I could evaluate neither — rendering is barred and no OCIO


**TYPOGRAPHY — the Señor Tacombi script and lettering** — *DESIGN*  
**Ceiling:** Ceiling of the instrument, not of the work. My discriminant reads a 1024×768 JPEG in which the whole word `Senor` is about 85 × 40 px and its strokes are 3–4 px wide against a 2.07 px PSF, with 2×2 chroma subsampling underneath. That fixes what can and cannot be settled here:  SETTLED AT ESSENTIALLY FULL CONFIDENCE — presence or absence of an ink mass tens of pixels in size. The tilde is 62 px at 7.8 sigma with a matching tarnish colour and a measured bleed-floor control; the `e`'s counter shows a ring/interior contrast of 18.6 against 0.2 DN and is stable over a 5→8 threshold sweep; the three S breaks run 4.2–7.1 sigma. No plausible re-choice of segmentation rule turns any of these off.  SETTLED AS SIGN ONLY — the upper/lower band asymmetry (finding 4) and the perimeter deficit (finding 5). The direction is invariant across every threshold I swept; the magnitudes are not, and I quote th


**BRANDING — the artwork system and brand identity (SPEC §10.10, ABSOLUTE REPLICATION OF ARTWORK)** — *DESIGN*  
**Ceiling:** The best this method could reach, with a perfect model, is NOT a verdict on the rendered vehicle — it is a verdict on the artwork SOURCE and the committed TEXTURES against ref_side.jpg. Three hard ceilings bound it.  (1) THE REFERENCE. Every calidad figure rests on a blob 100 x 74 px in an over-exposed patch (the surrounding cream reads 236,229,227, nearly blown). Finding 1's reference band is 0.52 ± 0.04 of burst width and that ±0.04 IS the ceiling: I cannot resolve the lockup's position inside its burst better than about 4% of 0.43 m = 18 mm, no matter how good the model is. The 82 mm displacement clears that by 4.5x, which is why it is reportable; a 30 mm one would not have been. Finding 2's tilde test can only ever say 'this photograph does not resolve a diacritic' — it can never say the vehicle lacks one, and that gap is not closable from the supplied frames.  (2) THE MISSING TERM. 


**STICKER — the die-cut vinyl sticker (art direction specification)** — *DESIGN*  
**Ceiling:** The ceiling of this method is that it can prove SIZES AND ORDERINGS, and cannot prove BEAUTY. There is no sticker, no render, no printed proof and no drawn line anywhere in this tree — LEDGER_rev43.md CLASS 4 states it flatly: "The die-cut sticker \| §7.3 \| none — and no code, no asset, nothing on disk." So every millimetre figure above is a PROJECTION from a measured metre through a stated scale, never an observation of artwork, and I have described no render at any point because I cannot see one. What that projection can settle, and settles hard: which elements land above or below a stated size at a stated sticker scale (the 48-of-66 gold-component rule, the 0.159 m minimum cut feature, the 0.30 mm louvre pitch, the 0.58 mm menu lettering), and the orderings among them (the triptych 29.08 / 0.29 / 27.86, the eleven radial bursts, the single 70° hue wedge) — and the orderings are the s


---

## 6. WHAT THE COMPLETENESS CRITIC FOUND MISSING

**GAPS. Method: source read + `git ls-files` + grep census against the eight dimensions' scope. No render was read; nothing is quoted from one.**

**1. SURFACE WITH NO DIMENSION AT ALL — THE CAB DOOR. Sev 4.**
`grep -n hinge|swing|DOOR_OPEN t1_shell.py t1_detail.py build.py` returns **only roof-lid hits**. The model's cab door is shut: a `DOOR_GAP_S` groove plus `doorcard±/doorback±`. The photograph's door is swung ~49° and carries the largest single artwork on the vehicle (the 29.1% surface that already burned one auditor). Rev 44's item 1 *is* this door (`DOOR_H`, `z_bot(x)`, 272.2/387.5 mm of added depth) and **no dimension audited it**. Close: a `door` dimension — outline off `ref_nolita_doorshut.jpg`, art extent off `ref_side.jpg`, kept separate, **ordinal only** (10.62/10.73 bar px/m on that plane).

**2. SURFACE 2 — THE INTERIOR. Sev 4.** `galley_dressing()`'s own docstring: *"DEPTH (Y) IS NOT MEASURABLE… Y is therefore chosen, not measured."* Counter touched only bay 1's fill wattage. Nothing audits what the eye is given through three 600×396 holes — and the owner's governing sentence is an *interior* sentence. Close: present/absent inventory against the bay-3 crop, the one frame that reads inside a bay.

**3. SURFACE 3 — THE OFF (−Y) FLANK AND CARGO DOORS. Sev 2.** `t1_shell.py:713`: cargo doors and off-side windows are **both graded E and contradict each other**; ledger finding 13 (off flank 804.9 mm) never adjudicated. Sticker chose the flank, so it never faces camera — but the shell is mirrored, so errors propagate inboard. Close: declare it unaudited-by-design, in writing.

**4. HARDWARE. Sev 2.** `mirrors()`, `wipers()`, `handles()` exist in `t1_detail.py` with no dimension and no verify row.

**5. OWNER INSTRUCTION WITH NO AUDITOR.** LEDGER class 4, rows 1 and 4: SPEC §5 *"no floating or intersecting artifacts"* and *"correctly oriented, correct handedness"* decals. Rev 42 instrumented overlap and resolution only. Roof's `lid_rail` **zero-surface-area** finding is exactly a §5-bullet-1 defect found by accident — the class is live and unwatched. Close: one cheap all-object probe (zero area/volume, plus decal handedness), which would have caught `lid_rail` by construction.

**6. THE CONTACT SHADOW — CROSS-DIMENSION ORPHAN. Sev 3.** `studio.py` lines 93–111 leave `optics-6` **OPEN**: the catcher's alpha may not survive the alpha-over. Optics reported five findings, none this one. The sticker's sev-4 die-cut rule *"bridge the underbody with the cast shadow"* **rests on it**. Close: the `T1_CATCH=0` A/B is already written — one run settles whether the bridge has a shadow to use.

**7. STILL UNVERIFIED.** The **89 findings in `AUDIT_RECOVERED.md`** remain unrefuted. And ledger **finding 20**: `probe_rev42_uv` prints 56.15% against SPEC §10.101.3's 55.97% — unresolved, and `bpy` here is PyPI, not a binary, so **no area figure off this machine is canonical**.

**8. UNDER-READ PHOTOGRAPH — `ref_nolita_doorshut.jpg`.** Tracked at `a5c53b8`, 480×320, read by **0 Python files**, **3 markdown lines**. It is the *only* frame showing the door's full outline — precisely what item 1 needs — and §7 question 2 (same vehicle?) is unanswered, so its admissibility is undecided. Runner-up: `ref_workshop.jpg`, the only bare-geometry frame, anchored no dimension this round.

**PROCESS NOTE:** `out/` is **not** empty in this clone (`p_side.png` 1400×933, plus beauty/matte passes, all gitignored). The round's "no render reachable" premise was false for the flank-probe frame; dimensions may have written NOT MEASURABLE where a measurement existed. Verify before repeating that premise in rev 45.

---

## 7. HOW TO READ THIS, AND WHAT NOT TO DO

* **Surviving is not the same as applying.** Several refuters confirmed a defect and then said the
  *proposed fix* would fail. The `menucard0` finding is the clearest: the card genuinely hangs 61.5 % over
  an open aperture, and the stated one-literal fix leaves it 43.7 % over — *"the same defect symmetrically
  re-distributed"*, which the refuter names as the `80 mm standoff / 63 mm proud` failure family. **Read
  the risk field before touching anything.**
* **Nothing here has been applied. No geometry, artwork or constant moved in rev 43.**
* **Do not re-open** the over-rider, the signboard, region 3, the ten flower heads, the tyre diameter, the
  counter slab, or the Z-ladder's gate.
* **89 more findings are still unverified** in `AUDIT_RECOVERED.md`, stranded since a container restart
  killed that audit's verify phase around rev 6. They are rev 44's item 1.