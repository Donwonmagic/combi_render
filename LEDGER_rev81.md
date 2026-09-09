# LEDGER — rev 81

## THE VISIBLE CHANGE THIS REVISION SHIPS (rule 55)

**NONE TO THE VEHICLE, AND THAT IS THE OWNER'S STANDING RULING (F361).** The
model is frozen; every line of work below is DRAWING over it as an underlay,
which is what he asked for in his own words:

> *"I simply want a collection of promotional images utilizing the combi. Very
> similar to this sign, but I want to make it special, distinguished in a way."*
> → *"It's not about the pallete, it's just an example of a promotional
> product."* → *"Remember that the model is simply an underlay for the hero of
> each piece. **It should be done in different styles too.**"* → **"All."** →
> *"Continue in a cadence of build, adversarial audit, iterate, until you have
> optimized every one as far as possible."*

**THE SECOND CLAUSE RULE 55 HAS ASKED FOR SINCE REV 77 IS STILL NOT WRITTEN.**
Stated, not hidden: revs 77–81 have all shipped no geometry, and the rule's
requirement to say plainly why has been carried forward rather than answered.

⚠ **`revstats.py` CANNOT SEE THIS REVISION'S WORK AT ALL (F375).** It counts
geometry lines. Quoting it alone would misreport rev 81 as `0 / 0`.

---

## WHAT SHIPPED

**`pliego.py` — SEVENTEEN PIECES, ALL FOUR OF HIS CATEGORIES, ON THE VECTOR
ENGINE.** `69 checked, 0 FAILED`.

| category | pieces |
|---|---|
| `calle` | `aframe` `carta` `vidriera` `horario` |
| `impreso` | `cartel_a2` `cartel_a3` `postal` `tarjeta` `volante` `lealtad` |
| `mercancia` | `bolsa` `playera` `vaso` `chapa` |
| `social` | `cuadro` `historia` `cabecera` |

**⚠ THIS IS THE DELIVERABLE SET.** `design_out/promo_r80_*` (7) and
`design_out/col_r80_*` (15) are EARLIER ROUNDS on the PIL engine F382
condemned, and are superseded; **eleven names appear in all three** and nothing
said which to show him. `design_out/pliego/pl_MANIFIESTO.txt` now says it, and
records the build dpi, which was recorded nowhere.

Each piece ships an **SVG master**, a **PDF** (1 page, at its declared size to
within 0.30 mm) and a **PNG proof**, all three from the same inlined document
so they cannot drift. The three `social` pieces render at **exact pixel sizes**
— 1400×1400, 1080×1920, 2100×700.

**SUPPORTING MODULES:** `lienzo.py` (SVG master → PNG/PDF via headless
Chromium), `estilo_vec.py` (four shape-based styles + the keyline system),
`trazo.py` (mask → smooth contour, disk-cached).

---

## THE STANDARD — `ESTANDAR_rev81.json`

**WHAT "OPTIMAL" MEANS IS NOW RESEARCHED RATHER THAN ASSERTED, AND IT IS A
TRACKED FILE.** Eleven agents: seven parallel research sweeps — typography,
colour, print production, digital format specs, flagship identity structure,
food-and-hospitality sector (including what can be recovered about the REAL
Tacombi brand), and mechanical craft defects — each required to fetch real
sources and return a **mechanical test and a threshold**, not adjectives. Then
three adversarial lenses over all 83 criteria: **provenance** (is the number
traceable, or is it design folklore), **measurability** (can a program actually
run this), and **fitness** (would following this make THIS work more generic —
because the ask is a bar for DISTINCTION, and a standard that only enforces
compliance produces competent, forgettable work).

**57 criteria survived; 30 were rejected, each with its reason recorded in the
file.** ⚠ **MOST OF THE NUMBERS THE RESEARCH PRODUCED WERE STRIPPED BY THE
LENSES AS THE RESEARCHERS' OWN INVENTIONS** — a 20-brand competitor board, a
dE00 ≤ 10 boundary, "three assets per piece", a 0.5 % area floor, a 1.5 mm QR
module, 16 and 10 arcminute legibility floors. What survived is mostly
STRUCTURE, and that is the honest result rather than a disappointing one.

⚠ **THE STANDARD IS NOT A CARRIER THIS REPOSITORY'S OTHER MACHINERY READS.**
Nothing in `verify_clone.sh`, `bootstrap.sh` or `audit_brief.py` mentions it.
It is carried by this ledger and by the rows in `pliego.py` that implement it,
and by nothing else.

**What it says the suite is missing, in its own words:** a competitor board
(nothing here compares this work to anything but itself); per-piece hierarchy;
an offer surface — *his photograph is a sidewalk sign with a QR, an app callout
and two dollar figures, and not one of the seventeen has a call to action*;
corrected Spanish; a portable master; and the fact that F01/F39 and F63/F69 are
reproduced on every piece. It also states plainly that **print conformance —
TrimBox, output intent, ink limits — is table stakes, and fixing it will not
make one piece distinguished.**

---

## THE EIGHTEEN FINDINGS, F384–F409

Full rows with measurement, ceiling and grade are in **`OPEN_FINDINGS.md`**.
Grouped by what they were:

**THE DEFECT CLASS THAT KEEPS COMING BACK — a shape printed IN THE PAGE
COLOUR.** F384 (seven of eleven sheets), F391 (the wordmark, at 1.295:1 on
`carta`, outside every check), F405 (every rule, slab, frame and text run —
the adversary painted a frame in the page colour and got `0 FAILED`), F409
(`lealtad`'s eight stamp discs at 1.000:1). **Four appearances in one
revision**, after F378, `playera` and `azulejo`-at-1.00:1 in earlier ones.

**INSTRUMENTS THAT WERE GREEN ON THEIR OWN DEFECT — TEN OF THEM.** F385 (four
successive instruments for one occlusion, all printing plausible numbers),
F393 (`keylines PRINTED` passed **by 814×** with all nine strokes physically
deleted), F394 (the fourth was RENAMED, not retracted, and shipped), F397 (two
rows that cannot fail for any input), F403 (`vaso`'s bars passed a sheet with
its type ×6 running off the trim), F396 (four rows go SILENT without the
fonts). **Five were found by an adversary, not by me.**

**MEASUREMENTS I PUBLISHED THAT WERE WRONG.** F395 (the type floor's
justification, in both figures, with evidence from the instrument the same
commit retracted), F398 (a correction that published the ABLATED box), F400
(four claims wider than what was measured), F388 (the grid docstring, refuted
by the row written to prove it), F404 (two of three screen pieces the wrong
size, checked on one axis).

**REAL DESIGN WORK.** F387 (`playera`'s silhouette read as a toaster), F392
(two pairs were one design twice), F401 (the `social` category had nothing),
F406 (the gold ground MEASURED off his photograph — his disc reads 1.629:1,
mine read 1.422), F408 (the three pieces the previous commit said it had
built), F402/F409 (frames and dies inside the bands their own checks read).

---

## THE ABLATIONS, ALL WATCHED FAILING (rule 3)

| switch | reds | on |
|---|---|---|
| `T1_VEC_NOKEYLINE=1` | `ink/ground`, `keylines DIFFERENTIAL` | 9 sub-bar fills with no keyline |
| `T1_PLIEGO_OCLUIR=1` | `occlusion` | 53.3 % covered against 0.0 % |
| `T1_PLIEGO_DESBORDE=1` | `declared grounds` | hero outside the disc it declares |
| `T1_PLIEGO_MARCAPLANA=1` | `wordmark` | 1.295:1 on `carta` |
| `T1_PLIEGO_MARCOPLANO=1` | `other elements` | frame at 1.000:1 |
| `T1_PLIEGO_TIPOGRANDE=1` | `margin band`, `outer edge` | 3.016 % / 4.0094 % |

⚠ **`T1_PLIEGO_DESBORDE` WRITES A NEW TRACE TIER INTO THE TRACKED TREE** (F407,
F377's class). `git status --porcelain probe_scratch/` after any ablation.

---

## WHERE THIS IS WEAKEST, STATED RATHER THAN HIDDEN

* **NOT ONE OF THE 69 CHECKS GRADES A DRAWING**, and he has not seen any of
  this. He rejected a whole round at rev 80 with every check green.
* **`keylines DIFFERENTIAL` CATCHES A TOTAL SUPPRESSION, NOT A SUBSET.**
  Measured: with **eight of nine** keylines deleted it passes, and at a
  twentieth of their weight it passes. What would catch a subset is the
  analytic row, which this module itself calls a tautology.
* **`ink/ground`'s ANALYTIC HALF AND THE WHOLE `grid` ROW ARE TAUTOLOGIES.**
  Both say so where they print.
* **`silueta` IS BUILT AND DRAWN BY NO PIECE** — one of four vector styles on
  zero of seventeen, so `ESTILO_ES["silueta"]` names something the `colophons`
  row can never exercise. Not fixed: adding a piece to exercise a style is the
  wrong reason to add a piece.
* **THE SVG MASTERS ARE NOT PORTABLE.** Fonts are `file://` `@font-face`;
  nothing converts type to outlines. They render here and nowhere else.
* **F379 STANDS AND IS NOW MULTIPLIED BY SEVENTEEN:** the `Señor` wordmark's
  missing ink (F01/F39) and the VW glyph building as an X (F63/F69) are
  reproduced on every piece that carries them. **Fixing that means unfreezing
  the model, which is his ruling to make.**
* **`--out` DOES NOT COVER `probe_scratch/trace/`** (F407). Stated, not closed.
* **EVERY AUTHORED CONSTANT IN `pliego.py`, `estilo_vec.py` AND `lienzo.py`
  WAS TUNED BY LOOKING.**
