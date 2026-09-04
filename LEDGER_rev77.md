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

## §5 THE MACHINE AT CLOSE

*(filled in at close — every figure watched printing, none transcribed)*
