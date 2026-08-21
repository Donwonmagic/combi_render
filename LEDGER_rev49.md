# LEDGER — rev 49

**Everything this revision measured, changed, refuted, retracted and corrected.** Figures here were
watched print unless a line says otherwise. **Where this ledger and the machine disagree, the machine
is right.**

---

## §0. THE OWNER'S REPORTS AND RULINGS THIS REVISION

| his words | verdict | where |
|---|---|---|
| **NEW** *(on the tail board)* **"That was referring to a different sign. This one is part of the vehicle."** | **RULING, and it CORRECTS BOTH the record and my refusal.** Two boards in one frame; the retirement belonged to the other one. | §2 |
| **NEW** **"Leave the lower bay shut, just have the back trunk window open for service."** | **RULING. BUILT.** And it refutes an inference rev 48 shipped. | §4 |
| **NEW** *(W6)* chose **"re-light to match your photographs"** | **ANSWERED — then the mechanism turned out not to exist as described.** §5 |
| **NEW** *(photographs)* **"Neither is possible right now"** | **RECORDED.** Both stay declared NOT MEASURED; the asking stops. | §9 |

> **RULE 29 — NEW. A RETIREMENT INHERITS THE OBJECT IT WAS MADE ABOUT, NOT THE STATION IT WAS SEEN AT.**
> `signboard()` was retired from a 3× crop of the **"La Santa"** sign standing on the ground behind
> the bus. Every later document read it as *"the raised panel at the tail is retired"* and applied it
> to a **different object at the same station**. Four revisions inherited it, and rev 49 refused a
> job on the strength of it until the owner corrected it.

> **RULE 30 — NEW. A FIXTURE'S FOOT MUST BE CLEAR OF THE BODY IT STANDS ON, AND SOMETHING MUST CHECK IT.**
> Nothing in this project checked that. The tail board's foot sat **120 mm inside the roof** and the
> trunk bay's lining sat **2.0 mm proud of the tail skin**, both through `VERIFY: 0 fail, 0 warn`.

---

## §1. THE BRIEF, GRADED — IT WAS WRONG TEN TIMES, AND ITS JOB 1 WAS THE WORST OF THEM

An adversarial agent was set on `NEXT_CONTEXT_PROMPT_rev49.md` **before any work started, and this
revision did not close until it reported.** Every item was re-checked by hand against the machine.

| # | the brief says | the machine says |
|---|---|---|
| 1 | §6 item 1: build the raised tail panel, job one | **IT NEVER MENTIONS THAT THE OWNER RETIRED A PANEL AT THAT STATION.** Zero occurrences of `T1_SIGNBOARD`, `10.28`, or "detached sign". I refused it on that ground — **and the refusal was too broad, and he corrected it.** §2 |
| 2 | `out/r48ship_*.png` exist | **`out/` WAS EMPTY.** Not tracked. `probe_rev48_louv.py` hard-defaults to `out/r48b_side.png`; a bare run prints MISSING and emits **no summary line at all**. §12's "11 checked, 0 FAILED" was not a live control. |
| 3 | rule 1's founding defect is fixed | **`cal_gen.py:385` still said "the model has NO REAR VENTS"**, verbatim and unannotated, two revisions after rev 48 cut real apertures. §7 |
| 4 | two buses | **THREE ARTWORK STATES.** The four Nolita frames are the red bus with *no* scrollwork, *no* script, *no* burst. Rule 26 as written passes a Nolita reading and it is still wrong-artwork. §8 |
| 5 | fifteen reference frames | **TEN.** Five byte-identical duplicate pairs. §7 cites two of them as independent. |
| 6 | the burst is "4× `ref_playa_34`" | **8.6×** by area (7474 vs 874 px²). The 2.7× in the same sentence is right — one ratio came off an instrument, the other did not. |
| 7 | "`verify_clone`'s six louvre rows" | **NINE.** Rows 405–407 are the JOB-2-refutation rows. |
| 8 | burst "99 × 75 px" | **100 × 74** by `cal_gen.py:48`'s own constant, 101 × 74 measured. A re-typed number. |
| 9 | "11 ahead / 0 behind" | **15 ahead / 0 behind** at pickup. Self-flagged by the brief, and correct to flag. |
| 10 | §3's G/R figures | **quoted with NO WINDOW** — the brief's own rule 8. No script in the repo computes them. The classification is robust (median hue 5°/14° against 98°/100°); **the decimals are not reproducible.** |

**And the branch instruction was stale for a FOURTH consecutive revision, in the dangerous direction.**
`claude/combi-render-rev49-sq1pvc` was created at `origin/main`, **0 ahead**, while
`claude/combi-render-rev48-ypkd3o` was **15 ahead / 0 behind**. Working where I was placed would have
discarded all of rev 48. HEAD was a strict ancestor, so it fast-forwarded; nothing was lost.
**`bootstrap.sh`'s own row 10 — "no branch carries work HEAD does not have" — independently confirms
the correction.** That row is the fix rule 17 has been asking for since rev 47, and it already exists.

---

## §2. THE TAIL BOARD — AND HE CORRECTED MY REFUSAL

I refused the brief's job 1 because `t1_shell.py:1749` records the owner retiring that panel:

> *"RETIRED 2026-08-10 BY THE OWNER … 'I was wrong, I think it is a detached sign.' So it is not a
> roof lid, and **it is not on the vehicle at all**."*

**He corrected me: "That was referring to a different sign. This one is part of the vehicle."**
He is right, and `ref_rear34.jpg` shows why in one frame — **there are two boards in it.**

| | what it is | where it stands |
|---|---|---|
| **"La Santa"** | cream, **red brush script**, red star | on the **GROUND, BEHIND** the bus. This is `signboard()`. Retired, correctly. |
| **the tail board** | cream face, **red rim**, amber bulbs, 38° | **ON the vehicle**, based at the drip rail at the tail |

**THREE PIECES OF PHYSICAL EVIDENCE, not another inference.** §10.28 requires a photograph of the
board's *footing* before this is revisited. It does not need one to settle **attachment**:

1. the base sits **on the drip rail** — 1 px from the project's own locked drip-rail fit;
2. its bulb string is **continuous with the drip-rail run**, at 28 ± 2 mm against the vehicle's own
   `BULB_PITCH` 28.6 ± 1.0 mm — **one circuit**;
3. a **power cable descends from it into the body**.

**AND IT IS NOT THE ENGINE LID, refuted twice.** Rev 48 measured 11 σ. Stronger, new: the engine lid
is top-hinged at z 1.103 over a 0.50 m panel, so **no opening angle whatever** puts any part of it
above **z 1.60**; the board's tip is at **2.184**. Unreachable. And the engine-lid band is directly
visible in `ref_side.jpg`, **closed**, red, carrying the yellow swirl.

**BUILT**, with every figure carrying its ceiling — see SPEC §10.123.2. Measured: base height
**1.747 ± 0.027 m** (tightens the brief's 1.78 ± 0.07 by 2.6×), tilt **38.0 ± 2.3° from HORIZONTAL**
(*say which datum* — from vertical it is 52.0°), chord **0.711 ± 0.028 m**, bulb pitch 28 ± 2 mm,
one stay with measured endpoints. Refuted mildly: the brief's tip "~0.5 m past `X_TAIL` at z ≈ 2.26"
is **−0.408 ± 0.017** and **2.184 ± 0.030**.

**AND THE 80 mm FOOT INCONSISTENCY THIS REVISION DECLARED IS WITHDRAWN — IT DISSOLVED.** §6a.

**THE WIDTH IS NOT MEASURED AND IS NOT MEASURABLE FROM ANYTHING WE HOLD.** The board's plane contains
the lateral direction, so its width projects **only through parallax** — 33.5 px/m, and (a cross
product) **identical at base and tip, so the projected width cannot taper**. The observed silhouette
*does* taper, so it carries the board's own material and rim too. **Upper bound W ≤ 0.59 m; NO lower
bound.** That bound alone refutes a full-width board. `TB_WIDTH` and the lateral centring are declared
pose choices.

---

## §3. THE TRUNK BAY SHIPPED WITH NO MATERIAL AT ALL

```
build.py:846   for ob, key in ASSIGN:            <- the loop that APPLIES materials
build.py:937   A(S.trunk_bay(log=log), "dark")   <- appends 91 lines AFTER it ran
build.py:939   log("materials: 165 objects")     <- counted trunk_bay in the 165
```

`A()` only **appends**. Step 8c must run after step 9 because a lateral hinge moves `v.co.x` and step
8b shears on `v.co.x` — so it is **the only `A()` call in the file that lands after its own
consumer**. The bay rendered at Blender's default ~0.8-albedo grey: **1.28× the body red, 1.11× the
cream — the brightest thing on the tail**, where a T1 engine bay is a dark cavity. After: **0.51×**.

**`VERIFY: 0 fail, 0 warn`. `verify_clone` ALL 110 PASS.** And the one line that could have reported
it printed `len(ASSIGN)` — **appends, not assignments** — so it asserted coverage instead of measuring
it. **Rule 27 inverted: a count that logs the wrong quantity reads as coverage too.**

Guarded against the **cause** and watched fail on `T1_BAREMAT=1`:

```
AssertionError: objects were given a material key but never assigned one: trunk_bay
  -- an A() call landed AFTER step 9's ASSIGN loop (build.py:846)
```

**This is the same defect rev 48 fixed for the louvre apertures — light where a dark bay belongs — in
the same revision.** It was missed here only because no rev-48 frame showed the tail.

---

## §4. HIS RULING — THE LOWER BAY SHUT — AND THE 2 mm SIGN ERROR IT EXPOSED

**It refutes an inference rev 48 shipped.** Asked at rev 48 which of the two rear apertures should be
open, he chose **A, the rear window**. Rev 48 reasoned *"he called the upper one the MAIN bay, not the
ONLY one"*, kept the lower lid open too, and wrote that into §10.122.4 and into the source.
**A choice between two things is not a licence to keep both.** Rule 6.

`TRUNK_OPEN_DEG = 0.0` means SHUT and the swing is **skipped, not run at zero** — `_swing_open()`
asserts the free edge travels, so a shut lid put through it fires a guard on a correct pose. The
T-handle and the plate are **no longer carried and no longer join `SWUNG`**: they have not moved, and
registering them would exclude two parts that *are* inside the closed envelope. Rule 18, the mirror
image of rev 48's stale-`bound_box` defect. **Length returns to 4.065**, the baseline `verify_clone`
locks.

**AND CLOSING THE LID EXPOSED A DEFECT INVISIBLE FOR A WHOLE REVISION.**

```
lid_trunk   x -1.8730 .. -1.8702      the shut lid's outer face, at X_TAIL
trunk_bay   x -1.8750 .. -1.4550      the lining's face, 2.0 mm AFT of it
```

`trunk_bay()` set its origin to `x_skin − 0.002 + BAY_DEPTH*0.5`; `solid_prism` extrudes ±depth/2, so
the aft face landed **2 mm PROUD of the tail skin. The sign of the inset was inverted.** The comment
above it explains, correctly, why the origin is advanced so `BAY_DEPTH` cannot reopen rev 48's +210 mm
defect — **and that reasoning does nothing about the inset's own sign, because nothing measured the
lining's face against the skin it lines** (rule 16).

With the lid open, 2 mm past the tail read as the bay's own back wall. With it shut, the lining sat
2 mm *in front of* a closed panel and won the depth test across the whole of it: **the tail rendered
with a dark charcoal rectangle where the red engine lid belongs.** Measured, same window:
**RGB 91.1/75.4/66.7 → 106.5/72.4/61.8.** Watched fail on `T1_BAYPROUD=1`.

---

## §5. W6 — THE TRADE DID NOT EXIST, AND THEN THE LEVER DID NOT EITHER

**The owner has been asked for three revisions to choose between accurate paint and a catalogue-clean
white background. THERE IS NO SUCH TRADE.** The white background is a **compositor constant** laid
under a keyed render, then renormalised to 252 DN in `post.py`. Measured, base vs `T1_CYCALB=0.30`:

```
background mean 255.000 -> 255.000   %at255 100.00 -> 100.00   max |difference| 0.000
```

**And he retired the pure-white backdrop lock himself at rev 15** — SPEC §6 carries "composited to
pure white" struck through, *"RETIRED, §10.69 — THE OWNER'S DECISION"*. **Three revisions have since
refused lighting changes by citing it as live.**

**THE SWEEP** — `probe_rev45_paint.py`, 4 controls including its C4 kill, **0 FAILED on every run**:

| lever | P1 body red G/R | verdict |
|---|---|---|
| base (rev-48 rig) | **0.455** (3.5 σ) | — |
| `T1_CYCALB` 0.76 → 0.30 | ~0.45 (−2…5 %) | **DEAD** |
| bigger softbox, **short axis** 3.5× area | **0.452** (−0.7 %) | **DEAD** |
| `T1_SPEC = 0` | 0.347 | works — **but rev 8 made this exact fix and reverted it** |
| sources 3.5× on **both** axes (12× area) | 0.351 (1.9 σ) | works — but see below |
| photographed target | 0.223 ± 0.066 | albedo already right at 0.250 (0.4 σ) |

**The short-axis row is the one that matters, and it is a negative result about my own hypothesis.**
Growing the source 3.5× in the axis that *sets the streak* — literally "use a bigger softbox" — moves
the red by **0.003**. So the gain in the both-axes row is **not the specular being softened**; it is
the sources growing past the subject (a 56 m strip) until the rig stops being directional and becomes
an **enveloping diffuse dome**. `T1_SOFTEN` does not tune the studio, it **replaces** it — which is
also why it works, since an overcast light *is* a dome and every reference frame was taken under one.

**Default 1.0. NOTHING SHIPS CHANGED. `P1 = 0.455` at k = 1.0 reproduces rev 48 exactly, watched print.**

**`LEDGER_rev45`'s "about half the excess is the specular response to the white cyclorama and its
0.76-albedo floor" is REFUTED.** It attributes an un-decomposed lever (`T1_SPEC`, which kills the
paint's specular response to *every* white source) to the smallest of its four causes. And
`studio.py:68`'s "the floor … the single largest desaturator in the scene" appears **once in the whole
repository — in that comment** — citing a §10.9 that contains no such arm. **Rule 1.**

---

## §6. THREE DEFECTS OF MY OWN, AND ONE INSTRUMENT I PUBLISHED THAT WAS EMPTY

* **A TAUTOLOGY PUBLISHED AS A MEASUREMENT.** I reported that the decal's type separates from the
  burst on chroma, and offered as the headline statistic *"of the 3007 burst pixels, ZERO have
  G ≥ 254"*. My own mask `(R−G)/R > 0.22` forces `G < 0.78·255 = 198.9` **by construction**. Observed
  max G inside the mask: 198. **It was an algebraic identity about my threshold, not a fact about the
  photograph.** The refuter killed it; the calibration killed the conclusion with it (§9).
* **THE TAIL BOARD'S FOOT WAS BURIED 120 mm INSIDE THE ROOF.** I typed the base height as LOFT's
  drip-rail datum, which is the rail's height at *LOFT's* reference station. The rail is not level.
* **I APPLIED A MEASUREMENT ACROSS DEPTH PLANES** (rule 16). The base station is a **near-flank**
  reading and the source says so, with an explicit ±0.035 depth ceiling — at the centreline it reads
  −0.095 and *the sign flips*. I built on the centreline and used the near-flank figure.
* **AND THE STAY REFUTED MY FIX.** Re-seated to the centreline, the stay's own measured triangle lands
  **144 mm aft of `X_TAIL`, in mid-air**. A second measurement refuted the correction to the first.

**Every one of these passed `VERIFY: 0 fail, 0 warn`. Every one was found by cropping a render and
looking at it.** Rule 28 has now produced the headline finding in four consecutive revisions.

---

## §6a. THE 80 mm FOOT INCONSISTENCY DISSOLVED — AND A GUARD OF MINE WAS A TAUTOLOGY

**The photorealism survey's roof agent caught the guard I wrote at §6 being unable to fire.**

```
z0     = ZT_ALL(x0) - rake_drop(x0) + 0.005
_crown = ZT_ALL(x0) - rake_drop(x0)
```

`z0 − _crown` is **identically +0.005 by construction**, so `z0 < _crown` cannot be true in the
shipped path. It fired only because `T1_TBFOOT=1` substitutes a different `z0` — **it was testing the
escape hatch, not the construction.** Rule 20, on a guard written in the same revision that quoted
rule 20.

**AND `ZT_ALL` IS NOT THE CROWN.** It is the **roll start** — the top of the flank before the roof
curves over; `bulb_string()` uses `ZT_ALL − RT_ALL` for the drip rail, which is the tell.

```
ZT_ALL - rake_drop at the old station      1.8673
ACTUAL body top over the footprint         1.9608     <- 93 mm higher
the board's lowest vertex                            -> 97.1 mm INSIDE the roof
```

**The rewritten guard measures the BUILT BOARD against the BUILT SKIN** — two independent things, so
it cannot be satisfied by construction — and **on its first run it caught a further 3.7 mm** I had
not seen: `solid_prism` extrudes centred, so the board hangs `TB_T/2·cos(tilt)` = 8.7 mm below its
origin and my standoff was a typed 5 mm. Derived now.

**AND THEN THE INCONSISTENCY DISSOLVED.** Seating on the skin threw the tip 227 mm high; seating at
the photographed height buried the foot. **Neither was a real dilemma — the board was at the WRONG
STATION.** The rear roof corner falls away fast (1.9608 at −1.6982, 1.8607 at −1.800, **1.7497 at
−1.850**, 1.6696 at `X_TAIL`) and exactly one station satisfies both:

```
photographed base height           1.747 +- 0.027
roof skin at the solved station    1.7497            ->  2.7 mm
tip lands at                       2.2001
measured tip                       2.184 +- 0.030    ->  16 mm, inside the band
```

**Two independent heights close.** The station is **SOLVED from the skin**, not chosen, and §2's
declared 80 mm is **withdrawn**. Rule 16: both facts had been in hand for a day without being put
together.

**What remains is smaller and honest.** The stay now lands **on** the tail skin at **72.1°** against a
measured **77.5°**; its endpoints were near-flank readings and the station is solved in the build
plane, so **the −5.4° residual is the same depth-plane ambiguity as the width — one unmeasurable
quantity, not two defects.**

---

## §7. THE RECORD — FOUR HALF-RETRACTIONS LANDED IN THE SOURCE

*A retraction that lands in a ledger and not in the source is half a retraction.*

* **`cal_gen.py:385` still said "the model has NO REAR VENTS"** — **rule 1's own founding case** —
  unannotated two revisions after rev 48 cut real apertures. Annotated, with how it propagated.
* **`cal_gen.py`'s THREE "DARK GREY" slat readings**, retracted at rev 47 into `verify_clone.sh` only.
* **`verify.py` called the ~3.0 m bbox top "the raised signboard" in two places.** It is **`lid_main`**
  (3.018, which is `STATE.md`'s own 3.017); `signboard()` has been gated off since **rev 12**. A
  retired object's name living on in a live comment on the height row for 37 revisions.
* **SPEC §10.26's table** still published `| trunk lid | OPEN, at the tail |`. Annotated — the
  **fourth** instance of the failure §10.122.5 names.

---

## §8. THREE ARTWORK STATES, NOT TWO — AND FIVE DUPLICATE FILES

Measured over every reference image (chroma-gated body box, method and ceiling in the agent report):

| class | frames | body G/R | what the artwork carries |
|---|---|---|---|
| **RED, current** | `ref_side.jpg` 0.247, `ref_rear34.jpg` 0.477 | | scrollwork, Señor Tacombi script, Calidad burst |
| **RED, EARLIER STATE** | the four **Nolita** frames, 0.130–0.345 | | **plain red flank, `TACOMBI.COM`, `267 ELIZABETH STREET`, a chalkboard. No scrollwork, no script, no burst.** |
| **GREEN** | `ref_workshop.jpg` 1.314, `IMG_2073.jpeg` 1.293 | | tufted damask / plain cream |

**Rule 26 as written is not sufficient.** "Check which bus" passes a Nolita reading, and it is still a
wrong-artwork measurement. The check has to be **which artwork state**.

**And five reference files are byte-identical duplicates** — `IMG_3842.png` = `ref_playa_34.png`,
`IMG_2054` = `ref_nolita_flank`, `IMG_2053` = `ref_nolita_front34b`, `IMG_2060` = `ref_nolita_front34`,
`IMG_3840` = `ref_nolita_doorshut`. **NINE distinct vehicle frames, not fifteen** (see the correction below). Rule 13 was never
discharged.

> **CORRECTED, rev 49e — IT IS NINE, NOT TEN.** The rev-49 discharge was itself incomplete. Checksums
> find byte-identical files; they cannot see a **resized** duplicate. `ref_source.jpeg` (246 × 197) and
> `ref_playa_34.png` (500 × 400) are **the same photograph** — normalised cross-correlation **0.9768**
> after resampling to a common size, which is the JPEG-artefact floor, not a coincidence. So the
> reference set is **NINE distinct vehicle frames**. *Ceiling: correlation on a 246 × 197 thumbnail
> cannot distinguish "the same frame" from "two frames one second apart on a tripod"; the reading is
> that they are the same IMAGE, and 0.9768 will not separate those two hypotheses.*
> **And it matters beyond counting:** SPEC §8's colour locks are derived from `ref_source.jpeg`, a
> 246 × 197 thumbnail the record calls retired. They can be re-derived on `ref_playa_34.png` at **4×
> the area**, today, with no new photograph.


---

## §9. THE DECAL — MY FINDING FELL, AND TWO OF THE RECORD'S CLAIMS FELL WITH IT

**Calibrated the way rule 22 requires**, against a synthetic built at `ref_side.jpg`'s exact resolution
*and* its exact 4:2:2 JPEG subsampling, where the geometry is known by construction:

```
                        synthetic (known)         real ref_side.jpg
  gap/cap, th 0.22-0.38   0.304 ... 0.318          0.167 ... 2.25
  vs ground truth 0.3114  2% error, FLAT PLATEAU   158% error, NO PLATEAU
  spread max/min          4.4x                     13.5x
```

**A method that recovers known geometry to 2 % with a flat plateau, and swings 13.5× on the real
frame, is not measuring the real frame.** `PHOTOS_WANTED` item 2 **stands**.

**But two record claims fell:**
* *"the star band merges at every threshold"* — **false.** It merges at the one mask the record ever
  ran, `(R−G) > 26`, which reproduces 1499 px exactly. At `(R−G) > 40` it breaks into **25**
  components. The count is still unstable, so `STAR_N` stays NOT MEASURED — **the stated reason was
  wrong.**
* *"both red frames are blown"* — **false as stated.** `ref_rear34.jpg` is **4:4:4, quality ~99**, and
  only **3.77 %** clipped frame-wide. It is blown **locally at the decal** (68.7 %), not as a frame.

Also measured and worth carrying: **JPEG chroma subsampling is NOT what limits this** — forcing the
chroma to true half-resolution changes the recovered component count by one and the type area by eight
pixels. And **the real decal's type spans 0.98 of the burst width against the build's 0.77**, which is
a live artwork lead, though it comes off the same unstable mask and is **provisional**.

---

## §10. THE STATE OF THE MACHINE

> **CORRECTED, rev 50 — THREE OF THE FOUR FIGURES IN THIS BLOCK ARE CONTRADICTED BY THE MACHINE,**
> and this block is on the required reading list, so it was propagating.
> * `ALL 113 PASS` was true at rev **49c** and was never updated when rev 49e added nine more rows.
>   The clean-tree value at rev 49's tip is **122**. (Rev 50 adds two and ends at 124.)
> * `171 objects` — `audit.py` measures **231** meshes, and rev 49e's own commit re-based
>   `verify_clone`'s row from 221 to 231. The 171 and the 231 count different things and nothing in
>   the repo says which, which is the defect, not the difference.
> * `19 ahead / 0 behind` — the rev-49 tip measures **29 ahead** of `origin/main`.
> * `ALL 10 PASS` and `VERIFY: 0 fail, 0 warn` reproduce exactly.

```
bootstrap.sh      ALL 10 PASS
verify_clone.sh   ALL 113 PASS   (110 at pickup; 4 added, 1 relabelled, NONE relaxed)
build             T1_SUB=1, VERIFY: 0 fail, 0 warn
                  length 4.065 vs spec 4.055    171 objects, 0 bare materials
probes            probe_rev45_paint   4 checked, 0 FAILED   (P1 0.455 reproduced exactly)
                  probe_rev47_gap     3 checked, 0 FAILED
                  probe_rev47_sharp   9 checked, 0 FAILED
                  probe_rev48_louv    NEEDS out/r48b_side.png -- render before quoting it
renders           out/ is NOT TRACKED and starts EMPTY on a clone.  Re-render before any probe
                  that reads a frame.
branch            claude/combi-render-rev49-sq1pvc   19 ahead / 0 behind origin/main
```

**GUARDS ADDED THIS REVISION, ALL WATCHED FAILING ON THE REAL DEFECT:**

| guard | fires on | watched with |
|---|---|---|
| every `A()`-keyed object has a material | an `A()` call landing after step 9 | `T1_BAREMAT=1` |
| a fixture's foot is clear of the body | the tail board 120 mm inside the roof | `T1_TBFOOT=1` |
| the bay lining is inboard of the tail skin | the 2.0 mm inverted inset | `T1_BAYPROUD=1` |
| `_bounds()` prints every non-bodywork drop by name | silent exclusion | prints every run |

---

## §11. STILL BLOCKED ON HIM — AND HE HAS SAID NEITHER IS POSSIBLE NOW

* **The darker decal frame.** Five items. My attempt to dissolve this request **failed its own
  calibration** (§9). The request stands, and it is still the highest-value missing input.
* **The tail with the engine lid open.** *Superseded in part:* he has now ruled the lid **shut**, so
  `TRUNK_OPEN_DEG` is no longer a pose choice needing a photograph. What the frame would still settle
  is the **bay's contents** — but with the lid shut, nothing shows, so **this drops down the list**.
* **The tail board's FOOTING** — §10.28 has required it since rev 12 and nobody had asked for it. It
  is what closes the declared 80 mm inconsistency and the board's width together. **NEW, and it
  replaces item 1 in priority.**
* **W4, the nose.** Five revisions, no photographed anchor. Method 2, silhouette corner-wrap on
  `ref_workshop.jpg`, is still the live one and does not care about lighting.

---

## §12. EVERY DISPATCHED TASK RETURNED AND IS RECORDED

Four agents ran during the working phase — the **brief refuter**, the **studio-separability**
analyst, the **tail-board measurer** and the **decal refuter** — **and all four reported before this
was written.** Three of them changed the conclusions:

* the brief refuter found the retirement my refusal rested on, and the three-artwork-state finding;
* the studio analyst found the **retired backdrop lock** and predicted the cyclorama would be a dead
  lever, which my render then confirmed;
* the decal refuter **killed my own headline finding** and with it two of the record's claims;
* the tail-board measurer tightened five figures and flagged the depth-plane ceiling I then ignored.

**AND A FIFTH, LARGER EFFORT: a 19-agent coordinated survey** of what remains before photorealism,
run at the owner's request. Twelve subsystem surveys → five adversarial refuters → a completeness
critic → one ranked synthesis. **19 agents, 0 errors, ~5 hours, 1632 tool calls, 600+ working crops,
78 findings (15 blocking, 42 major, 21 minor).** Output: **`SURVEY_rev49_photoreal.md`**, 464 KB, and
`NEXT_CONTEXT_PROMPT_rev50.md` §6.

**Its headline: *"the geometry is now closer than the presentation."*** Four things unrelated to
measurement are what make every shipped frame read as a render — the vehicle barely darkens the
ground it stands on (`optics-6`, open since **rev 12**, and there is **no undercarriage at all**); its
largest surface delivers chalk where every photograph shows polished enamel; **every duplicated part
is a bit-identical clone** at the same clock angle carrying the same dirt (front-rear wheel high-pass
correlation **0.675** against a +5 px control of **−0.012**); and every specular surface has a white
void and six rectangles to reflect.

**THE ADVERSARIAL PHASE EARNED ITS KEEP: 1 CONFIRMED, 3 PARTIALLY_STANDS, 1 REFUTED.** It killed a
**blocking** finding — *"the rocker is not modelled"* — which **this session had already relayed as
confirmed after reproducing the surveyor's own error**: I grepped for an object *named* rocker. It is
built inside the loft by `t1_core.section()` and `audit.py` publishes `rocker to ground 0.3177` into
`STATE.md` on every build. **Rule 31.** It also narrowed the W4 nose claim from "a photographed handle
at last" to "the symptom made quantitative, which unblocks nothing" — **that overstatement was mine.**

**AND IT CAUGHT THREE MORE OF MY OWN DEFECTS**, all fixed this revision: the tail-board foot guard was
a **tautology** (rule 32); `verify_clone`'s `STATE.md` block had been reading a **rev-45 baseline from
a tree recorded DIRTY** for four revisions (rule 33); and rule 13's rev-49 discharge was itself
incomplete — **nine frames, not ten**, because a checksum cannot see a resized duplicate.

**The single highest-value thing it surfaced:** `playa_env.py` is **1695 lines**, every mass placed by
inverting a camera recovered from a photograph of *this* bus, **dormant since rev 10 and referenced by
no verifier and no dimension.** It is the only frame this project can compare pixel-registered against
a photograph of its own subject; it **is** the diffuse-dome rig §5 concluded is W6's only surviving
lever; and its ground is a **real lit surface**, so it closes `optics-6` and the ground finding for
free.
