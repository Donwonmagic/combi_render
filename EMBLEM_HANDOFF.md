# THE EMBLEM — A HANDOFF

**This file exists because the owner has reported the same defect SIX TIMES across
eighteen revisions, and because the reason it has never been fixed is now known and is
embarrassing. It is a CARRIER (`CLAUDE.md` rule 16). It is not yours to compact or
summarise. If you close this item, close it here with the measurement that closed it.**

> *[owner, rev 62]* **"I am sick and tired of not being able to execute a publicly
> available emblem."**

He is right, and that sentence is the whole finding.

---

## §1 THE ONE THING TO UNDERSTAND BEFORE YOU TOUCH ANYTHING

**THE VW ROUNDEL IS A PUBLISHED, SPECIFIED, REGISTERED TRADEMARK. THIS PROJECT HAS SPENT
EIGHTEEN REVISIONS TRYING TO REVERSE-ENGINEER IT FROM A 41 × 69 PIXEL PHOTOGRAPH.**

That is the error. Not a wrong constant — the *method*. Everything below is downstream
of it.

**AND THE PROJECT ALREADY KNEW.** At rev 45, at the owner's own prompting, commit
`5d0f28e` — *"rev45: the nose badge is a catalogue part, not a shape to be derived"* —
wrote it down in terms:

> *"The VW monogram is a registered trademark with fixed proportions. **Build the
> canonical mark and use the photograph to VERIFY, inverting the method that has derived
> it from a 68-px emblem and been called wrong four revisions running.**"*

**AT REV 63 IT WAS DONE — AND THE MARK THAT CAME BACK DISQUALIFIED ITSELF. READ §5b
BEFORE §5, because §5 item 1 is now partly ANSWERED and partly SHARPENED.**

**IT WAS NEVER DONE BEFORE REV 63.** And it was in **no live carrier** — not the rev-62 brief, not the
ledger, not the work list, not `CLAUDE.md`, not `OPEN_FINDINGS.md`. It survives only in
`LEDGER_rev45.md` and `NEXT_CONTEXT_PROMPT_rev46.md`, both long superseded and never
opened. **That is the carrier-loss mechanism rule 16 exists to prevent, and it cost this
project seventeen revisions on its owner's top item.** This file is named by
`README.md`, `START_HERE.md` and the newest brief specifically so it cannot happen again.

**REV 62 DID NOT FIX IT EITHER, AND SHOULD SAY SO PLAINLY.** What rev 62 did was fit the
glyph to a *bigger, better* photograph with a *better* objective. **That is the same
error in nicer clothes.** It produced the best glyph this project has made — see §4 — and
it is still a derivation, and it is still 25 % short.

---

## §2 WHAT HE HAS ACTUALLY SAID, ALL SIX TIMES

| rev | his words |
|---|---|
| 44 | *"The vw still doesn't look right."* |
| 46 | *"the vw logo wrong"* — the vertical proportions |
| 51 | reported again; the badge's SCALE measured, built ~10 % small at 1.8 σ, **not decisive** |
| 58 | reported again — the fifth time |
| 61 | reported again — the sixth time |
| 62 | *"the badges still aren't correct"*; *"I am sick and tired of not being able to execute a publicly available emblem."* |

**AND IT IS ON FIVE OBJECTS (F69)** — the nose roundel and all four hubcaps. Fixing the
construction fixes all five; they share `t1_core.vw_bars`.

---

## §3 REFUTED. DO NOT RE-TRY ANY OF THESE.

Every row is measured, not argued. Re-trying one is how this project loses a revision.

```
reach              T1_VW_CAPMIN                 cells 6 -> 2                    F101
stroke weight      T1_VW_WFRAC -> 0.48          cells 6 at EVERY value          F102
six-constant cell-count solve                   7 cells only at residual 0.2498 F103
separate strokes                                rev 8 did it and got an X       F113
the V/W kink                                    photographs have the SAME kink  F138
terminal angles off the badges                  BUILT IT: residual 0.1800,
                                                WORSE than a deliberately-bad
                                                control at 0.1167               F141
STROKE WEIGHT AGAINST C8   (new at rev 62)      moves the WRONG WAY; thinning
                                                to the limit reaches 1.82 vs
                                                3.39 and costs a cell           F152
THE WORKSHOP BADGE'S LANDMARKS (new at rev 62)  CEILED -- a third of the gap is
                                                raster scale; nothing clears
                                                ~1.5 sigma at matched scale     F153
THE CANONICAL 2019 VECTOR AS A TARGET           OBTAINED IT, MEASURED IT, and it
  (new at rev 63)                               is a DIFFERENT OBJECT: 3 cells /
                                                1.597 against the photograph's
                                                7 / 3.390 at ONE ruler          F168
FITTING TO THAT VECTOR                          BUILT IT: elongation 2.316 / 6
  (new at rev 63)                               cells, WORSE than rev 62's own
                                                photo-fit at 2.529 / 7          F170
```

**AND TWO ROUTES THROUGH `ref_workshop.jpg` HAVE NOW FAILED FOR THE SAME REASON** (F141,
F153): **the pressing is chrome, and chrome has no flat tone to threshold.** Before
proposing a third route through that frame, say how it avoids that.

---

## §4 WHAT REV 62 ESTABLISHED, AND THE PICTURE THAT SHOULD HAVE BEEN MADE AT REV 45

**LOOK AT `probe_scratch/rev62_emblem_ab.png` FIRST.** BUILT | PHOTOGRAPH | overlay, at
the same scale, the workshop badge de-foreshortened by F09's conic. **Ours is an X. The
photograph is a V over a W.** The difference is topological and angular, not a constant
that wants nudging — which is why eighteen revisions of nudging did nothing. Nobody had
ever put the two side by side.

**THE SHAPE FIT — `probe_rev62_emblem.py`.** Fits the six spine constants to the
photograph's WHOLE MASK by IoU on the glyph interior, instead of to six scalars extracted
from it. The rasteriser, the cell counter and the elongation statistic are
`probe_rev46_vw.py`'s own, imported, so a score here is a score on the shipped instrument.

```
                      interior IoU   elongation   cream cells   landmark residual
shipped                   0.4061         1.49          6              0.0347
rev-62 shape fit          0.5402         2.56          7            off-scale
the photograph                --         3.39          7                --
a plain cross             0.3174         1.39         --                --
```

**THE SEARCH CONVERGED AND WAS NOT CLIPPED** — the first run left `VW_W_TROUGH_X` pinned
exactly on its bound, which is shipping the bound rather than the fit; the bounds were
widened and re-run and **no parameter is on a bound**.

```
VW_V_TIP_X       0.2707   (shipped 0.3806)   the V narrows
VW_APEX_Z       -0.3788   (shipped 0.1250)   its apex drops well below centre
VW_W_ARM_X       0.7794   (shipped 0.9200)
VW_W_ARM_Z       0.3842   (shipped 0.0019)   the W's outer arms RISE off the 3-and-9
                                             o'clock line toward the top
VW_W_TROUGH_X    0.8408   (shipped 0.4925)   its troughs spread outboard
VW_W_TROUGH_Z   -0.7357   (shipped -0.6200)
```

**THE CAUSE OF THE X, IN ONE LINE:** the W's outer arms leave the ring at **±89.9°** —
dead horizontal, 3 and 9 o'clock — and cross a wide V. Near-horizontal arms crossing a
wide V *is* an X. Raise the arms and narrow the V and it becomes a VW.

**THREE THINGS REV 62 BROKE, THAT YOU INHERIT AS FACTS:**

* **F151 — C8's photograph target has a SILENT FAILURE MODE.** `cell_elongation`
  inscribes its measuring disc in the **mask array's rectangle**, not in the badge. Widen
  the crop 3 px and the disc escapes the roundel, the nose paint outside the ring becomes
  a 479 px "cream cell", and the target reads **1.553** — indistinguishable from the built
  1.49. **At that window the gate reports the owner's top defect CLOSED and nothing
  fires.** Within ±2 px it reads 3.390 / 3.188 / 2.950 and the segmentation sweep gives
  2.969 .. 3.415, so **the built glyph is 1.99× .. 2.27× too round — a RANGE. Four
  documents quote the point 2.27×. Stop.**
* **F152 — the stroke-weight lever is dead**, and F102's "inert" verdict was about the
  cell COUNT only; C8 did not exist then.
* **`probe_rev46_vw.py`'s own header says *"photograph 3.33"* under a "WATCHED" banner and
  the probe prints 3.39.** Small, but it is a figure in a comment that has gone stale.

---

## §5b WHAT REV 63 DID — THE SPECIFICATION WAS FETCHED, AND IT IS THE WRONG ERA

**THE FIRST MOVE OF §5 WAS MADE.** A canonical vector of the mark was obtained and is
committed as **`vw_canonical_2019.svg`**, with its provenance welded into the file as an
XML comment so the two can never be separated. **It deliberately does NOT carry the `ref_`
prefix**, because it is not a reference frame of the target vehicle and a `ref_` name would
invite the exact rule-11 error this section exists to record.

**WHAT IS REACHABLE FROM THIS ENVIRONMENT, MEASURED, NOT GUESSED.** `upload.wikimedia.org`,
`commons.wikimedia.org`, `en.wikipedia.org`, `cdn.jsdelivr.net`, `unpkg.com` and
`creativebloq.com` are all refused by the network egress proxy — 403 on CONNECT, watched.
**`raw.githubusercontent.com` and `registry.npmjs.org` are reachable**, and that is where
the mark came from. **Do not re-run the blocked hosts; do start from the reachable two.**

**AND IT IS THE WRONG MARK — THIS IS THE RESULT, AND IT IS RULE 11 IN ITS PUREST FORM.**
Measured through `probe_rev46_vw.py`'s OWN `cream_cells()` and `cell_elongation()`, lifted
by `ast`, **with both sides at the photograph's own 41 × 69 raster and squash 69/41**:

```
                              cells   elongation   ink fraction
    PHOTOGRAPHED badge          7        3.390        0.606
    canonical 2019 vector       3        1.597        0.426
```

**TWO FEATURES THE 2019 REDRAW DROPPED ACCOUNT FOR THE WHOLE DIFFERENCE, AND BOTH WERE
FOUND BY PAINTING EACH CREAM CELL ALONE AND LOOKING — none by reasoning about it:**
**its V does not touch its W, and its legs stop short of the ring. The pressing has both.**
See `probe_scratch/rev63_canon_cell_each.png`, which is that paint.

The reading is window-stable (1.589 .. 1.591 over ±0..3 px) and scale-stable (1.597 at 69
rows, 1.590 at 552), so it is the **mark's** property and not the crop's — which is what
rule 39 demands and what C8's own photograph target fails.

**SO: A 2019 REDRAW IS NOT A SOURCE FOR A 1955–67 PRESSING. What is still worth fetching is
a PRE-2019 vector, an official specification, or an orthographic photograph of the pressing
itself.** Note for whoever tries: **`simple-icons` had no Volkswagen icon at all before the
rebrand** — checked back to 1.16.0 (2019-09-23) — so that particular well is dry.

### §5b.1 WHAT IT *DID* BUY, AND IT IS THE STRONGEST LEAD ON THIS ITEM (F169)

**Rev 63 fitted the six spine constants to the canonical vector — JOINTLY WITH THE STROKE
WIDTH, which §5 item 3 records as never searched — and the fit AGREES WITH REV 62's
PHOTOGRAPH FIT ON THE DIRECTION OF THE FIX.** The two were fitted to different objects, one
of which contains no photographic content at all. **That is the first independent
corroboration this item has ever had.**

```
                    shipped   rev 62 (photo)   rev 63 (canonical)   agree?
VW_V_TIP_X          0.3806       0.2707             0.3287          YES -- both NARROW the V
VW_APEX_Z           0.1250      -0.3788             0.0538          yes -- both lower the apex
VW_W_ARM_X          0.9200       0.7794             1.1002          (only the ratio matters)
VW_W_ARM_Z          0.0019       0.3842             0.4350          YES -- both RAISE the arms,
                                                                    and by a similar amount
VW_W_TROUGH_X       0.4925       0.8408             0.3111          NO -- not corroborated
VW_W_TROUGH_Z      -0.6200      -0.7357            -0.6445          yes -- both lower slightly
stroke width        0.2087       (not searched)     0.1543          thinner, as F152's sweep
```

**§4's stated cause — *"Raise the arms and narrow the V and it becomes a VW"* — is
CORROBORATED.** And the fit's own raster, painted at
`probe_scratch/rev63_canonfit_cells.png`, **is a legible V over a W. It is not an X.**

### §5b.2 AND IT IS *NOT* TO BE SHIPPED — MEASURED, NOT ARGUED (F170)

**On the photograph's own statistics the canonical fit lands FURTHER AWAY than rev 62's fit
already did.** All read through the same path at 276 rows, **rev 62's constants re-run here
rather than transcribed** (rule 38):

```
                          cells   elongation   landmark residual
    shipped                 6        1.485          0.0317
    rev 62 photo-fit        7        2.529          9.9000
    rev 63 canonical fit    6        2.316          0.4394
    THE PHOTOGRAPH          7        3.390            --
```

**REV 62's PHOTOGRAPH FIT REMAINS THE BEST GLYPH THIS PROJECT HAS MADE, and it is still
short.** The canonical fit converged at IoU 0.7979 against its own target (from the shipped
glyph's 0.4301) **with no parameter on a bound — after the first run pinned two and was
re-run on widened bounds, watched failing as C27b**, which is rev 62's same correction.

**§6 BELOW STILL GOVERNS AND NONE OF IT WAS DONE AT REV 63:** nothing was rendered on the
nose with new constants, the six `verify_clone.sh` rows were not re-based, and the hubcaps
were not checked. **No constant in `t1_core.py` was changed. `STATE.md` is untouched, and
that is a control: rev 63 edited zero files under `t1_*.py` / `build.py` / `studio.py`.**

**ONE MORE, SMALL BUT IT IS IN THIS FILE (F171): §4 above quotes rev 62's fit as elongation
2.56. Re-run on this ruler it prints 2.529.** Recorded rather than silently corrected.

---

## §5c THE GATE IS NOT SUFFICIENT — REV 63 BUILT THE COUNTEREXAMPLE AND RENDERED IT

**READ THIS BEFORE §5, AND BEFORE RUNNING ANY SEARCH. IT CHANGES WHAT "BETTER" MEANS
ON THIS ITEM.**

**1. THE CONSTRUCTION IS NOT THE CEILING (F174).** §2.3 candidate 1 — *"ablate the
construction"* — is done. `probe_rev63_ablate.py` swept **24000 points over seven spine
constants AND the stroke width jointly**, and `vw_bars` reaches **elongation 6.877 at 7
cells, twice the photograph's 3.390**. The objective was watched moving first, and the
10.9 % refusal rate is reported. **Eighteen revisions of "it reads as an X" were a SEARCH
problem, not a geometry problem.** Do not spend another revision looking for a topology fix.

**2. BUT RANGE IS NOT FIDELITY.** That 6.877 point is a degenerate crown of parallel
slivers — `probe_scratch/rev63_ablate_best.png`. It is not a VW. **The target is 3.390,
not "as high as possible", and any objective that maximises C8 will walk straight into
this.**

**3. AND HERE IS THE ONE THAT MATTERS (F175). C6 AND C8 CAN BOTH GO GREEN ON A GLYPH THAT
IS VISIBLY WORSE.** `probe_rev63_shapefit.py` implements §5 item 4's own prescription —
IoU jointly with the elongation and cell-count statistics — and finds constants that score:

```
                        IoU      cells   elongation   landmark residual
    shipped            0.4172      6        1.485          0.0317
    rev 63 joint fit   0.5363      7        3.322          0.2135
    THE PHOTOGRAPH        --       7        3.390            --
```

**C6 PASSES (7 = 7). C8 PASSES ("1.02x too round"). IoU improves. And rendered on the nose
it is a Y-shaped trident, WORSE than the X it replaced.** Look at
`probe_scratch/rev63_emblem_ba.png` — BEFORE | AFTER — before you believe any number in
this file. **The constants were REVERTED. Nothing shipped.**

**4. THE GATE CONTAINS THE ALARM FOR ITS OWN FAILURE, AND IT FIRED (F176).** At those
constants `probe_rev46_vw.py` prints **`[FAIL] C7 KILL: collapsing the W's arms and troughs
onto the axis moves the cell count 7 -> 7`**. A kill that cannot fail is not a control
(rule 3), so **C6's simultaneous PASS is worthless there**. Nobody had ever driven the gate
into the region where its own kill dies. **Read C7 as a PRECONDITION on C6: C7 red means
C6's pass means nothing.**

**5. THE LANDMARK RESIDUAL WAS THE ONLY STATISTIC THAT STAYED RED, AND IT WAS RIGHT
(F177).** C4 failed at 0.2135 against the shipped 0.0347 while every shape statistic
improved. That is ONE counterexample and it does not rehabilitate L1–L6 — F137 and F139
stand — but **it inverts the presumption, and §5 item 5's "retire them" option should not
be taken on the current evidence.**

**6. AND A TRAP IN THE SOURCE THAT COST ONE MISLEADING RENDER (F178). THERE ARE TWO STROKE-
WEIGHT CONSTANTS.** The **NOSE** roundel's weight is `vw_logo_fit()`'s `wfrac` **signature
default, 0.1986**. The **HUBCAP's** is `CAP_EMBLEM_WFRAC`, **0.2087**. **`T1_VW_WFRAC`
overrides the NOSE one only** — so every weight sweep in this project's history, F152's
included, has been driving the nose. Rev 63 wrote a nose-fitted value into
`CAP_EMBLEM_WFRAC` and the gate promptly read 6 cells / 2.659 where the search had read
7 / 3.322. **Check which constant before you touch either.**

### §5c.1 SO WHAT IS THE NEXT OBJECTIVE, CONCRETELY

Not another statistic on the face-on raster. **The three we have are jointly satisfiable by
a wrong glyph, which is now measured.** What is missing is a term that would have rejected
the trident, and rev 63 did not build it. The candidates, NOT measured:

1. **A REACH term measured on the BUILT MESH, not the raster.** In the AFTER crop the
   stroke ends visibly stop short of the ring while the raster says 7 cells. `STATE.md`
   already carries a wheel-house reach idiom that does this kind of thing properly.
2. **Judge on the RENDER.** One orthographic front render per candidate is minutes, not
   milliseconds, so it cannot go inside a 24000-point sweep — but it can gate the top ten.
3. **Keep the landmark residual as a HARD CONSTRAINT rather than an objective**, per F177.

---

## §5 WHAT TO DO NEXT — AND THE OPPORTUNITY IS DELIBERATELY LEFT OPEN

**THE FIRST MOVE IS NOT A SEARCH. IT IS TO GO AND GET THE SPECIFICATION.**

The mark is public. Its proportions are published. This project has never once tried to
obtain them — every revision has re-derived them from pixels. **That is the opportunity,
and it is why this item is still open.**

Ranked, with what each buys and what it costs:

1. **OBTAIN THE CANONICAL MARK AND BUILD IT.** Vector outlines, an official brand
   specification, the pressing's part geometry (`241853601A`, Type 2 front emblem,
   1955–1967), or a clean high-resolution orthographic photograph of *any* example of the
   same pressing — the mark is identical on every one, which is the whole point of a
   trademark. **Then use `probe_rev62_emblem.py`'s IoU and C8 to VERIFY, not to fit.**
   Rev 62's fitted constants become the *floor* the canonical mark must beat.
   *If it cannot be obtained in this environment, say so as a result and say what was
   tried — that is a real finding and it is worth more than another search.*
2. **SHIP §4's CONSTANTS AS AN INTERIM.** They are measured, converged, unclipped, and
   they take the glyph from an X to a V-over-W on the owner's own eye. **This was NOT
   shipped at rev 62** — see §6 for exactly why and for what shipping costs.
3. **EXTEND THE SEARCH TO THE STROKE WIDTH.** `CAP_EMBLEM_WFRAC` was held fixed. F152
   says weight alone cannot reach the target, but weight *jointly with* the spine has
   never been searched, and the fit is 25 % short.
4. **THE OBJECTIVE IS NOT FULLY DISCRIMINATING, AND THIS IS A REAL OPENING.** Parameter
   sets that look quite different score within **0.0007** of each other. A better
   objective — a distance transform, a chamfer, a shape context, or IoU jointly with the
   elongation and cell-count statistics — would likely find a better optimum than IoU on
   its own.
5. **RE-DERIVE L1–L6, OR RETIRE THEM.** F137 proved the landmarks and the photograph's
   cell shape are incompatible; F139 proved one of their targets is contaminated; rev 62
   proved L6 is not the culprit and the second badge cannot arbitrate. **They are a
   compression of the badge into six scalars and they may simply be the wrong
   representation.** Retiring them is a legitimate outcome and would need saying out loud.

---

## §6 WHAT SHIPPING §4's CONSTANTS COSTS — READ BEFORE YOU DO IT

Rev 62 deliberately did not ship them, and the reasons are not "it was out of time":

* **It is 25 % short of the photograph** (elongation 2.56 against 3.39). It is an
  improvement, not a fix, and it must be described that way to the owner. He has been
  told something was fixed before and found it was not.
* **The L1..L4 topology is no longer presented**, so the landmark residual goes
  off-scale. That is F137's incompatibility arriving from the other side and is the
  EXPECTED outcome — but `probe_rev46_vw.py`'s C4/C5 will change character and must be
  re-read, not assumed.
* **Six `verify_clone.sh` rows check these constants BY VALUE**, at
  `ck "VW_APEX_Z is 0.1250"` and its five siblings. Changing the constants means
  **re-basing all six together with the cause named and a companion row** —
  `CLAUDE.md`: *"NEVER RELAX ONE COPY OF A CHECK"*, and rev 61 moved three `V_POW` rows
  together for exactly this reason.
* **RENDER IT AND LOOK AT IT ON THE NOSE BEFORE CALLING IT ANYTHING.** A glyph that
  scores well in a face-on rasteriser still has to survive being a *pressed, lit object
  on a curved panel*. Rev 45 already found the badge was *"a flat plate on a curved
  nose"*. **rule 1, and it is the rule this project breaks most often.**
* **It changes all five objects** — nose roundel and four hubcaps (F69). Check the
  hubcaps, not just the nose.

---

## §7 THE INSTRUMENTS, AND HOW TO RUN THEM

```bash
python3 probe_rev46_vw.py                 # 1.1 s -- the shipped gate.  C6 and C8 FAIL
python3 probe_rev62_emblem.py --paint     # the shape fit.  --iters N for more restarts
python3 probe_rev62_landmarks.py --paint  # the cross-frame landmark route + C8's window
python3 probe_rev63_canon.py             # NEW at rev 63 -- the canonical mark, measured
python3 probe_rev63_canon.py --fit       # ...and fitted, then VERIFIED on the photograph
python3 svgraster.py                     # its rasteriser's OWN selftest, 9 known shapes
python3 probe_rev63_ablate.py            # NEW -- ABLATES vw_bars.  ~20 min, 24000 pts
python3 probe_rev63_shapefit.py          # NEW -- the joint fit.  BUILDS F175's counterexample
T1_VW_DUMP=1 python3 probe_rev46_vw.py    # paints the cream cells.  LOOK at them
T1_VW_WFRAC=0.14 python3 probe_rev46_vw.py   # the stroke-weight ablation (F152)
```

**`bpy` is a pip module here, so these run WITHOUT the Blender CLI** — `probe_rev46_vw.py`
is 1.1 s, which is what makes a thousand-evaluation search affordable. Check whether a
probe needs `blender -b -P` before budgeting minutes for it.

**THE CONSTANTS LIVE IN `t1_core.py`**, immediately above `def vw_bars(`:
`VW_V_TIP_X`, `VW_APEX_Z`, `VW_W_ARM_X`, `VW_W_ARM_Z`, `VW_W_TROUGH_X`,
`VW_W_TROUGH_Z`, `VW_W_PEAK_Z`. `vw_bars` builds a 3-point V spine and a 5-point W spine
and projects every terminal radially onto the band circle with `_on_band`, so
`VW_W_ARM_X` and `VW_W_ARM_Z` matter **only through their ratio** — they set an angle,
not a position.

**THE EVIDENCE CROPS**, all committed:
`probe_scratch/rev62_emblem_ab.png` (built | photograph | overlay — start here),
`rev62_emblem_fit.png` (shipped | fit | photograph | overlay),
`rev62_c8_window.png` (C8's disc escaping the badge — F151's mechanism),
`rev62_mask_workshop.png`, `rev62_thsweep.png` (the repaired chrome mask).

**NEW AT REV 63**, all committed: `probe_scratch/rev63_three_marks.png`
(**PHOTOGRAPH | BUILT | CANONICAL, start here**), `rev63_photo_vs_canon_41x69.png` (the two
at ONE raster — the picture F168 is about), `rev63_canon_cell_each.png` (each canonical
cream cell alone; this is the paint that found the V/W gap and the short legs),
`rev63_canonfit_cells.png` (the canonical fit — a legible V over W),
`rev63_front_emblem.png` (the SHIPPED emblem cropped off `out/r63_front.png`, where the V's
arm tips visibly float short of the ring).

---

## §8 THE STANDING WARNING

**A green check here is not evidence about the badge.** `verify_clone.sh` checks that the
record is self-consistent; not one of its rows compares the emblem to a photograph. Every
defect this project has shipped passed it and was found by **looking at a crop**.

**And an instrument that has never been wrong has never been tested.** Rev 62 caught four
of its own wrong instruments on this item alone — a chrome mask that took one flank of
every stroke, two mis-specified controls, and a break-trace that followed the roundel.
Every one produced a plausible number first. **Budget for it. It is normal here.**
