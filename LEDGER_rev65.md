# LEDGER — rev 65

**Every figure below was watched printing. Nothing is transcribed.**

---

## §1 THE RESULT, AND IT IS NOT A COMFORTABLE ONE

**THE EMBLEM HAS BEEN STEERED FOR FIVE REVISIONS BY A SENTENCE THAT IS A STRING LITERAL.**

`probe_rev46_vw.py`'s C6 prints *"the mesh names them: the W's two outer arms, at r 0.6638
against a band inner edge of 0.7988, floating 18.9 mm"*. **Those three figures are hard-coded
into the message.** They are rev 60's, measured at rev 60's constants. **Rev 63 changed all six
spine constants and the sentence did not move.** It printed identically under
`T1_VW_CAPMIN=1` while the cell count went 6 → 2 — which is how it was caught.

It has been quoted as a live measurement by the rev-61 through rev-65 briefs, by
`EMBLEM_HANDOFF.md`, by `OPEN_FINDINGS.md`, and **by me, twice, in the revision that found
it.** **F198.**

---

## §2 SO THE REACH WAS MEASURED LIVE, OFF THE MESH, FOR THE FIRST TIME (F199)

Every outline vertex of the built glyph, R=1 units, extreme 0.8140, band inner edge 0.7752:

```
    TEN corner vertices at 0.8089 .. 0.8140   -- within 0.6 % of the extreme,
                                                 PAST the band's inner edge
    TWO cap corners at 80..97 % of the extreme -- a HAIR INSIDE the band
    six more vertices below 80 %              -- INTERIOR points, not terminals
```

**ALL SIX TERMINALS REACH. The defect is TWO CAP CORNERS**, at the 3 and 9 o'clock strokes,
landing just inside the band's inner edge. One hairline of cream merges the two cells either
side of it, and that is C6's 6-instead-of-7. **It is NOT "the W's two outer arms".**

**AND I NEARLY PUBLISHED THIS WRONG TOO.** My first clustering of those same vertices read two
terminals at 0.4656 — 57 % — and named them the W's bottoms. **The paint showed they are
INTERIOR vertices caught by my own 0.45 radius threshold.** `probe_scratch/rev65_reach_paint.png`,
every vertex coloured by reach with the band drawn to scale. Rule 8, on my own instrument,
in the same hour I wrote F198 about someone else's.

### §2.1 WHY EVERY KNOWN LEVER FAILS — ALSO MEASURED, NOT ARGUED

```
    as shipped                       6 cells   elongation 2.39
    T1_VW_CAPMIN=1                   2 cells   elongation 1.31
    T1_VW_PUREFIT=1                  6 cells   elongation 2.40
    T1_VW_CAPMIN=1 T1_VW_PUREFIT=1   6 cells   elongation 2.24   <- THE PAIR, TRIED
```

**CAPMIN's failure mechanism, measured:** its extreme runs **0.8140 → 0.9250**, and
`t1_detail._fit_glyph` re-normalises by the GLOBAL extreme — so every other terminal is
dragged 12 % off the band. That is the 2 cells.

**AND THE PAIR THE REV-58 NOTE HAS CALLED *"half of one fix"* EACH FOR FIVE REVISIONS —
`T1_VW_CAPMIN=1 T1_VW_PUREFIT=1`, *"the pair the rev-58 note says was never tried"* — IS NOW
TRIED. 6 cells / 2.24. REFUTED.**

---

## §3 THE BADGE'S RING IS FITTED AS AN ELLIPSE AT LAST, AND IT SHRINKS THE DEFECT (F194)

F185's close. **Nothing in this project had ever fitted it.**

The badge is a **circle on the real object**, so its image is an ellipse. Fitted from the
SECOND MOMENTS of the filled badge — every interior pixel voting, not a ragged rim — it
reproduces the region's own area to **0.05 %** and **0.11 %**.

```
    photographed axis ratio    0.6596 (workshop)   0.5810 (target bus)
    un-squashed                0.9970              0.9994    <- it comes out a CIRCLE
```

**PROVED ON A KNOWN ANSWER FIRST:** the built glyph, mirror IoU **0.9777**, squashed 0.72 and
sheared 0.35 to **0.2369**, comes back at **0.9585**.

**WHAT THE TARGETS BECOME — read on the MARK instead of on a photograph of it:**

```
                                    cells   elongation
    C6/C8 as they stand (squashed)    7        3.390
    UN-SQUASHED workshop              6        2.960
    UN-SQUASHED target bus            7        2.627
    the BUILT glyph, unchanged        6        2.388
```

**THE FAMOUS "1.42× TOO ROUND" IS 1.24×, OR 1.10× AGAINST THE TARGET BUS'S OWN BADGE.** And
the residual SHEAR still inflates even those (F185's ceiling is not closed), so the true
target is lower still — **NEARER what is already built.** Cells are not stably 7 either:
un-squashed, the workshop badge reads **6**, the same as the build.

**EIGHTEEN REVISIONS CHASED A CELL-SHAPE DEFICIT THAT IS MOSTLY AN ARTEFACT OF THE RULER.**

---

## §4 WHAT REV 65 GOT WRONG IN ITS OWN WORK — FOUR, AND ONE IS THE SAME CLASS AS F198

1. **The rotation search (F195).** After un-squashing, the first cut searched rotation for
   maximum mirror IoU. **It lifted the score 0.4143 → 0.6922 and turned a legible VW into
   horizontal bars**, picking −55.0° and −81.5°. A circle is mirror-symmetric about EVERY
   axis, so the ring scores the same at every rotation and only the glyph breaks the tie.
   **And the question was never open: the bus is UPRIGHT in both frames.** Rule 41, one
   revision after it fired on the traced pressing. Kept unused as C7's control.
2. **The positive control's first run failed and the failure was mine.** The projected glyph
   was CLIPPED by its own canvas (`glyph_only_mask` rasterises rows 0..275 of a 276 canvas,
   so any shear clips it), and `unproject` returned the badge at native scale — radius 47 in
   a 276 canvas — where `cell_elongation` reads **exactly 1.000**, a degenerate value I had
   already printed. `pad()` and `normalise()` fix both. **Same family as F186.**
3. **The reach clustering (§2 above).** Nearly published two terminals "floating at 57 %"
   that were interior vertices caught by my own threshold.
4. **I misread a painted panel.** I looked at `rev65_capmin.png` and said CAPMIN "reads as a
   VW with ~7 cells"; counting components at four disc fractions gave **2 at every one**.
   **The eye was wrong and the count was right** — recorded because this project usually
   records the reverse.

**AND C4 WAS RE-BASED ON WHAT THE METHOD CLAIMS, NOT RELAXED.** It first gated *"mirror
symmetry must come back"* and the nolita frame failed at +0.034 against a +0.05 bar. **The bar
was not lowered (rule 44).** The ellipse gives 5 of a homography's 8 degrees of freedom, so
un-squashing removes the SQUASH and cannot remove the SHEAR — that was never the claim. What
IS claimed is checkable exactly and is now the assertion: **the badge must come out a circle.**

---

## §5 TWO OWNER STATEMENTS, BOTH BINDING

> **"I don't think the bus is ready yet. We need the bus to be ready before investing
> seriously in the render."** — **F193, his THIRD hold** (rev 58, rev 64, now). It also fixes
> what the render will be: **MULTIPLE SIZES, MAX RESOLUTION, MAX FIDELITY, ONE FOLDER.**
> **So F192's "prove the large-format chain" drops BELOW the model defects.**

> **"we still have work to do on the shape of the nose."** — **F197, AND IT IS A SECOND
> DEFECT, NOT THE EMBLEM.** The emblem sits on the nose; he named the nose's SHAPE separately.
> **It corroborates a finding the record already held and never acted on:** when the nose was
> last held against the photographs (rev 51) it found **three defects by eye — flush
> headlamps, the roundel's short V-arms, and A FLAT NOSE.** The V-arms became the emblem item
> and swallowed fourteen revisions. **The flat nose was never worked, and there is no
> instrument for it** — `probe_rev59_nose.py` measures the lamp break's ELEVATION, not the
> nose's SECTION.

---

## §6 THE MACHINE AT CLOSE OF REV 65

```
bootstrap.sh              ALL 10 PASS
verify_clone.sh           ALL 303 PASS on a clean tree  <- 0 FIDELITY, 303 SELF-CONSISTENCY
probe_rev65_unproject.py  10 checked, 0 FAILED   -- NEW
probe_rev64_shear.py      6 checked, 0 FAILED
probe_rev63_trace.py      ALL CONTROLS PASS
vw_pressing.py            5 checked, 0 FAILED
probe_rev46_vw.py         9 checked, 3 FAILED -- C4, C5, C6.  UNCHANGED
audit_brief.py            10 checked, 0 FAILED
audit_adversary.py        48 asked, 0 BROKE
```

**Not one of those 303 rows compares the model to a photograph.**

---

## §7 WHAT REV 65 DID **NOT** DO

1. **THE EMBLEM STILL IS NOT FIXED.** No constant changed. `probe_rev46_vw.py` reads exactly
   what it read at rev 63's close. **What changed is that the defect is now correctly named
   and correctly sized, and three more routes are refuted.**
2. **The one fix the geometry asks for is NOT built** — cutting each terminal on the band's
   arc. §2.1 says why it is the right one; nobody has written it.
3. **THE NOSE (F197) IS UNTOUCHED AND UNINSTRUMENTED.**
4. F156 — five revisions unacted. `REMAINING_WORK_rev61.md` §I — 27 rows, five revisions.
5. Tyres, glass, the tail's barrel, the shut lines, the galley, F143's roof loudspeakers:
   all untouched.
6. **`probe_rev46_vw.py`'s C6 message is NOT yet repaired** — F198 is recorded, not fixed.
   The literal still prints.

---

## §8 THE BRANCH, MEASURED AT CLOSE

```
HEAD                                   17 ahead / 0 behind origin/main
origin/claude/bus-model-rev57-yvrlhi    6 ahead of origin/main -- MERGED INTO HEAD at rev 64
                                        (bootstrap row 9 asks about HEAD; it is GREEN)
bootstrap.sh        ALL 10 PASS    at the handoff commit, clean tree
verify_clone.sh     ALL 303 PASS   at the handoff commit, clean tree
audit_brief.py      10 checked, 0 FAILED
audit_adversary.py  48 asked, 0 BROKE
NEXT_CONTEXT_PROMPT_rev66.md is byte-identical to PASTE_INTO_CLAUDE_CODE.txt (§10.1)
```

**THE ONE THING TO CARRY IF ONLY ONE THING IS CARRIED.** *Measure the defect before you fix
it, and check the measurement is a measurement.* This project spent five revisions aiming at
a number that was typed into a message string. **`grep` for the figures your brief quotes,
and if they are not inside an expression, they are not measurements.**
