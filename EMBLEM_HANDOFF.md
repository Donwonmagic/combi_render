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

**IT WAS NEVER DONE.** And it is in **no live carrier** — not the rev-62 brief, not the
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

---

## §8 THE STANDING WARNING

**A green check here is not evidence about the badge.** `verify_clone.sh` checks that the
record is self-consistent; not one of its rows compares the emblem to a photograph. Every
defect this project has shipped passed it and was found by **looking at a crop**.

**And an instrument that has never been wrong has never been tested.** Rev 62 caught four
of its own wrong instruments on this item alone — a chrome mask that took one flank of
every stroke, two mis-specified controls, and a break-trace that followed the roundel.
Every one produced a plausible number first. **Budget for it. It is normal here.**
