# LEDGER — rev 74

## RULE 55, AT THE TOP, WHERE IT BELONGS

**REV 74 SHIPPED GEOMETRY: THE TYRE'S TRANSVERSE TREAD (F308).** `t1_detail.tyre()` returned
`T.revolve(...)` — **rotationally symmetric by construction**, so its four grooves are
CIRCUMFERENTIAL rings and the transverse lugs the photograph shows were **not a free parameter of
the model at all**. That is rule 54's shape for the second time in this project's history. Sixty-four
grooves are now cut INWARD from the crown; `T1_TYRE_TREAD=0` restores the rev-73 tyre exactly.

`python3 revstats.py` — run it for the live row; at the time of writing rev 73 reads
`73 | 123 geometry | 0 closed`.

**AND THE HONEST SIZE OF IT, STATED HERE RATHER THAN IN A FOOTNOTE (rule 12), INCLUDING A READING
I MADE AND THEN REFUTED MYSELF.**

**THE PIXEL-DIFFERENCE STATISTIC IS A FLAT NULL, AND IT IS A NULL EVEN LOCALLY.** Whole frame,
hero34f: change `2.038 %` of pixels >8 levels against a two-render floor of `2.045 %` — **1.00×**.
I then reasoned the statistic was saturated by a whole-frame average and painted the difference
(`probe_scratch/r74_tread_diff.png`), which shows **two bright annular rings at the wheels** — and
recorded that as localisation confirmed. **THAT WAS WRONG AND THE BOX-LOCAL FLOOR REFUTED IT.**
Measured per box, change against a second render of the SAME tree:

```
    front wheel              change 4.418 %   FLOOR 4.372 %   1.01x
    rear wheel               change 1.923 %   FLOOR 1.847 %   1.04x
    body (control, no tyre)  change 7.941 %   FLOOR 7.900 %   1.01x
```

**The rings are a NOISE feature — high-contrast wheel edges are where sampling noise lives — and
they appear in the floor too.** Rule 49, and I published the interpretation one step before the
measurement that kills it.

**WHAT DOES SEE IT IS A STRUCTURAL STATISTIC, AND ITS FLOOR IS MEASURED RATHER THAN ASSUMED.** The
rev-73 tyre is a *provable* surface of revolution, so any angular structure in its rendered
silhouette is raster noise. Tracing the rear tyre's silhouette in the `side` frame:

```
    BEFORE (a revolve -- THIS IS THE FLOOR)   rms 0.0503 px   dominant amplitude   4
    AFTER  (64 lugs)                          rms 0.4499 px   dominant amplitude 130
                                                              at exactly 64 cycles/rev
```

**8.9× the floor on rms, 32× on amplitude, and the render recovers the lug count from PIXELS.**
`probe_rev74_tread.py`'s **T6** carries it. ⚠ **AND WHAT T6 DOES NOT SAY (rule 6): recovering 64 is
NOT evidence that 64 is RIGHT** — it says the declared geometry reached the frame. The photograph
brackets the count at 48..84 and that is still open. **Looking agrees**: the silhouette went from a
smooth curve to a visibly serrated one (`probe_scratch/r74_tyre_BEFORE.png` / `r74_tyre_AFTER.png`,
and `r74_tread_ab.png` on the delivery view). **Preview frames are 1600 px; the delivery frame is
3840, where the lugs are 2.4× larger.**

---

## §1 THE OWNER'S RULING, WHICH WAS THIS REVISION'S TOP ITEM

He ruled the emblem's contested stroke weight, shown `probe_scratch/rev74_weight_ask.png`:

> ***"I can't tell them apart — stop tuning the weight."***

**`VW_FREE_WFRAC` STAYS AT 0.2205 AND THE WEIGHT IS RECORDED AS *UNRESOLVED*, NOT SETTLED (F314).**
He did not pick a ruler and was explicit he could not, so **F302 and F303 both stand**. What is
closed is tuning further against these two candidates. **It does not withdraw the emblem** — still
his ninth report, F191 and F234 still stand — and it supersedes §2.2's instruction to re-implement
F204's ink-strictly-inboard statistic *for the purpose of* settling 0.2205.

**THE FIGURE HE WAS SHOWN HAD TO BE REBUILT FIRST, AND THAT IS A FINDING (F313).** The brief pointed
at `rev73_emblem_free_ab.png`. It captions its middle panel **`SHIPPED wfrac 0.2283`** — but
`t1_core.VW_FREE_WFRAC` is **0.2205** and `verify_clone.sh` pins the shipped glyph at 41474 on-px,
which is what 0.2205 builds. **The panel labelled "shipped" was not the shipped build**; the crop
predates rev 73's own ship by hours. Worse, its three panels **did not share a projection** — an
oblique photograph beside two head-on masks, which is F184's trap and rule 43.

**AND A CONFOUND IN MY OWN REBUILD, CAUGHT BEFORE IT REACHED HIM (F315).** Fitting each candidate to
its *own* best pose — correct for SCORING — put a solid arc down the ring's outer rim that is the
two homographies disagreeing, not stroke weight. **XOR 226 px / 7.20 % of the ink per-pose against
89 px / 2.83 % through one pose**, the latter agreeing with the head-on **2.91 %**. More than half
the apparent disagreement was pose. **A pose-free objective is the right way to SCORE two
constructions and the wrong way to PICTURE their difference.**

Reproduced en route, and the brief's figures stand: **A 0.8528 fit / 0.8276 indep; B 0.8657 /
0.8364; B − A = +0.0129 / +0.0088.** Built L6 at 0.2205 is **0.1532** against the photograph's
**0.1528**; at 0.20429 it is **0.1412**. Both rulers are real and they genuinely disagree.

---

## §2 WHAT ELSE WAS MEASURED, INCLUDING TWO NULLS

**F309 — F143's ROOF LOUDSPEAKERS ARE A POSE, NOT GEOMETRY, AND THE RECORD CARRIED THEM AS AN
UNMODELLED OBJECT FOR 57 REVISIONS.** The identification is right: `ref_rear34.jpg` at 8× resolves a
white cabinet, black baffle, a woofer with a visible surround and a tweeter. **But three frames of
the same vehicle show the roof BARE** — decisively `ref_playa_34.png`, **the same location** as
`ref_rear34.jpg` (same walls, same folk-art panels, same paving), plus `ref_nolita_flank.jpg` and
`ref_nolita_front34.jpg`. Painted side by side: `probe_scratch/r74_F143_grounding.png`. **Building it
would plant removable event gear permanently into every delivery frame**, the same class as
`REAR_OPEN_DEG`'s unmeasured pose. ⚠ **And half its corroboration does not survive either: F143's
second frame is not an independent sighting** — that crop sits where the propped mural board, its
frame, its bulb string and the roof all overlap.

**F308b — THE LUG COUNT CANNOT BE RECOVERED FROM WHAT WE HOLD, AND THE PROBE REFUSES TO PUBLISH
ONE.** Six estimates, two independent methods × three radii: **peak 55 / fft 64 / peak 61 / fft 74 /
peak 48 / fft 84** — a **48..84 bracket, 1.73×**, the two methods disagreeing by ~30 % and each
moving with the radius. The pitch is ~3 px in a 500×400 frame. **So `TREAD_LUGS = 64` has exactly the
standing of `TB_WIDTH`'s "POSE CHOICE, NOT MEASURED"** and is labelled that way above the constant.
**What is measured is the KIND.**

---

## §3 THE INSTRUMENTS THAT WERE WRONG — INCLUDING MINE

**F310 — MY OWN HEADLINE ROW WAS WRONG FIRST TIME AND THE WATCHED-FAILURE STEP CAUGHT IT.**
`probe_rev74_tread.py`'s T3 asks *"is the tyre a surface of revolution?"*. Its first cut pooled every
crown vertex and took one spread — which reads the **PROFILE's** radial variation (four 0.0080
grooves plus 0.0042 of camber) and returned a confident **PASS at 0.0119 m on a tyre that IS a
revolve**. Fixed by binning on exact `y`, where `revolve` puts every angle at one profile point:
it then read **0.000000 m** and went red on the real defect. **Caught by running the row BEFORE the
change and expecting it to fail** — not by reasoning. Written after the build it would have passed
for the wrong reason and guarded nothing.

**F311 — `verify_clone.sh` FAILS SIX ROWS ON A CLEAN CLONE, SO `bootstrap.sh` STOPS AT PICKUP.**
Measured before anything was touched: `bootstrap.sh` **9 PASSED, 1 FAILED**; `verify_clone.sh`
**417 PASSED, 6 FAILED**. Five are one cause — the `F296`/`F300` rows run
`probe_rev73_tailboard.py`, which needs a `*_side.png` in `out/`, and **`out/` is untracked and
starts EMPTY**, so the probe correctly refuses (rule 37) and every grep returns 0. The sixth is
`$((PASS+1))` and can only agree once the other five are green. **This is F307's shape one level up
and F307 did not see it.** **RECORDED, NOT PATCHED** — the repair is a re-base of five rows and needs
the cause named plus companion rows.

**F312 — A WATCHED KILL IS RED WHERE THE BRIEF SAYS ONLY ITS SWEEP ROW FAILS.**
`probe_rev73_tailboard.py` reads **5 checked, 2 FAILED — T3, T4**, not 1. T3 is the rotation KILL,
bar `< 1.5`, and the −7.0 → −8.75 rung is **1.75**. **Cause not established and it cannot be from
what is on disk**: no source moved, so it is a property of the frame — but rev 73's own side frame is
gone with `out/`, and **T3's bar has no floor under it** (rule 49). Two `side` renders of one tree
would settle it.

**F316 / F316b — THE RULE-15 ADVERSARY RETURNED EIGHTEEN DEFECTS.** The most consequential:
**`probe_rev67_nose.py out/r74_front.png` reads `7 checked, 0 FAILED` and P3c PASSES**, where §2.3
and §4 both say it fails BY DESIGN with a mechanism attached. **Verified independently.** The outcome
is frame-dependent and the brief names no frame — and a context told "P3c fails by design" will wave
through a genuinely red P3c. **And `audit_brief.py`'s regex `^python3 (\S+\.py)\s+#` cannot match any
command line carrying a frame argument**, so F306's headline fix is structurally blind to the largest
instance of the class it was built for. The remaining defects are carried verbatim in **F316b**.

---

## §4 WHAT THIS REVISION DID **NOT** DO

* It did **not** re-open the nose, the gloss grid, the `BUMP_BOW` ladder or the recess.
* It did **not** re-quote `0.623 %` and did not re-read the gates at 16 bits.
* It did **not** fix F311 or F312 — both are recorded with what would settle them.
* It did **not** measure the tread's depth or duty; both are declared, and a closer tyre frame is
  the obvious `PHOTOS_WANTED` item this project has never had.
