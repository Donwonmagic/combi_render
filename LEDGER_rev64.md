# LEDGER — rev 64

**Every figure below was watched printing. Where a figure moved from the rev-64 brief's
value, both are given and the cause is named. Nothing here is transcribed from a document.**

---

## §1 THE ONE-LINE RESULT

**The brief's top work item was *"finish `probe_rev63_trace.py` and PUT THE TRACED PRESSING
IN THE MESH … the emblem's most likely close"*. It is finished. It is in the mesh. It was
rendered. IT IS WORSE, AND NOTHING OF IT SHIPPED — and the reason it is worse refutes both
emblem gates along with it.**

**Every emblem target this project has steered by for eighteen revisions is read off a
photograph of the badge that is NOT MIRROR-SYMMETRIC.** The mark is. The model is. The two
frames are not, and the de-squash that is supposed to correct them rescales the axes and
**never rotates**.

---

## §2 THE MACHINE AT CLOSE OF REV 64 — every one watched print

```
bootstrap.sh            ALL 10 PASS      <- row 9 GREEN for the first time in SEVEN revisions
verify_clone.sh         ALL 298 PASS on a clean tree, AT THE HANDOFF COMMIT
                        <- 0 FIDELITY, 298 SELF-CONSISTENCY.  285 -> 287 (the merge) -> 298
                           (eleven rows holding rev 64's work).  NO row was relaxed.
audit.py                0 fail, 0 warn at T1_SUB=2, 228 meshes.  STATE.md REGENERATED and
                        IDENTICAL apart from its provenance block -- THAT IS THE CONTROL:
                        T1_VW_TRACED is off, so the mesh must not have moved, and it did not
probe_rev63_trace.py    ALL CONTROLS PASS   (rev 63: FAILED T3)
probe_rev64_shear.py    6 checked, 0 FAILED  -- NEW, and it is §1's finding
vw_pressing.py          5 checked, 0 FAILED  -- NEW
probe_rev46_vw.py       9 checked, 3 FAILED -- C4, C5, C6.  UNCHANGED, and see §4
probe_rev63_canon.py    5 checked, 0 FAILED
probe_rev63_reach.py    ALL CONTROLS PASS
trace_outline.py        SELFTEST PASS (10 shapes)
svgraster.py            SELFTEST PASS (9, incl. "arc RAISES")
audit_brief.py          10 checked, 0 FAILED
audit_adversary.py      48 asked, 0 BROKE  <- 42 as inherited, which is what the brief's
                        SS0.07 states as 36 under a heading reading "every one watched
                        print".  SIX replaced at rev 64 (SS10.5) and ONE RETIRED IN PLACE:
                        its own question text repeated the false "RING (0.508)" diagnosis,
                        which is why the MECHANICAL half of rule 15 could never catch it
flank_compare.py        FAILS.  worst region `i` at 0.687 of its own ceiling (brief: 0.686)
gloss_compare.py        FAILS at 0.442 of the photograph's spread, bar 0.60 (brief: 0.426)
probe_rev59_nose.py     5 checked, 0 FAILED.  M1 PASSES lens-ruled; BEZEL-ruled 1.550 / 1.584
                        against a rim-ruled 1.951..2.121 -- F136 stands, this is NOT closure
probe_rev59_door.py     8 checked, 1 FAILED (M3, BY DESIGN)
```

> **`gloss_compare` and `flank_compare` moved because they read a DIFFERENT RENDER**, not
> because anything in the model changed. The brief's figures are rev 63's frames; these are
> `out/r64_*`. Both gates still FAIL. **A green check is not evidence about the vehicle:
> not one of those 298 rows compares the model to a photograph.**

---

## §3 WHAT REV 64 DID

### §3.1 THE STRANDED BRANCH — ROW 9 HAD BEEN RED FOR SEVEN REVISIONS (F188)

Measured at pickup, not transcribed:

```
git rev-parse --is-shallow-repository   -> TRUE          (the THIRD running)
fetch --prune  -> "- [deleted] origin/claude/new-session-e854rn"
                  the designated branch, before a byte was pushed -- the EIGHTH running
HEAD                                    -> 0 ahead / 0 behind origin/main
./bootstrap.sh row 9                    -> FAIL: STRANDED
                  origin/claude/bus-model-rev57-yvrlhi (6 commits, 5 files)
```

**The brief's §1 states rev 63 measured *"no branch carried work HEAD did not have"*. That
is FALSE at this commit**, and `bootstrap.sh` row 9 — which `CLAUDE.md` says outranks any
sentence, *including this one* — said so on the first run.

**And it was not housekeeping.** The branch carried an OWNER RULING, and the owner had
already ruled on the branch itself: *"merge it, renumber its IDs"* — a line that sat in HIS
SETTLED RULINGS in every brief from rev 57 to rev 64 **while the branch stayed unmerged**.

**What it carried: the line *"`playa_env.py` is not on the table"*, in HIS SETTLED RULINGS
from rev 52 to rev 64, WAS NEVER HIS.** It entered as a brief's INFERENCE from W6, whose
object is the studio RIG, applied to a SECOND DELIVERABLE — rule 34 exactly. Put to him
after rev 62 with both readings quoted, he ruled the Playa hero **"DEPRIORITISED, NOT
CANCELLED"**. **So the brief I was handed was publishing a misattributed owner ruling.**

"Renumber its IDs" was already discharged at rev 59 — main's F92 carries *"(was F62 on
`origin/claude/bus-model-rev57-yvrlhi`)"*. **What was still stranded was the RULING.**

Conflict resolution is stated in the merge commit rather than taken silently: five conflicts
in the entry file, HEAD (rev 64) wins on all four row counts; on the fifth — HIS SETTLED
RULINGS — HEAD's wrapping is kept, the `playa_env` sentence REMOVED, and the ruling appended.

### §3.2 THE TRACED PRESSING — BUILT, RENDERED, REFUTED (F183)

**What was built.** `vw_pressing.py` carries the factory pressing's outline traced off
`ref_workshop.jpg` — admissible because the roundel's SHAPE is the factory PRESSING, which
is geometry and DOES transfer (rule 11, F141). It is a **LITERAL and a GENERATOR**, held
together by a selftest: `trace()` re-derives it from the photograph and asserts it still
agrees with the table. **A traced constant that cannot be re-derived is a number somebody
typed.** `t1_core.solid_with_holes` caps a prism whose cross-section has holes — the V and
the W touch, so the cream cells between them are ENCLOSED HOLES, and filling them changes
the topology C6 counts.

**The gate said it was better. On ONE ruler, every figure watched printing:**

```
                          cells   elongation   IoU vs the TARGET BUS's badge
    SHIPPED glyph           6        2.388            0.6049
    TRACED pressing         7        2.534            0.7487
    the workshop badge      8        3.409            0.7789
    TARGET BUS badge        8        3.110            1.0000
```

**Seven cells where the shipped glyph reads six — C6's floating-arm defect, closed.** IoU up
0.1438, reaching **96 %** of what its own source frame scores against the target.

**AND IT RENDERS AS AN UNRECOGNISABLE JAGGED BLOB.**
`probe_scratch/rev64_emblem_ba.png`, **SHIPPED | TRACED | PHOTOGRAPH**.
**Rule 41 fired one revision after it was written, on the item it was written about.**
`T1_VW_TRACED` defaults **OFF**, is MEASUREMENT-ONLY, and two verifier rows hold it off.

### §3.3 WHY — AND THIS IS THE REVISION'S RESULT (F184, F185)

The VW mark is **mirror-symmetric about its vertical**. That is a property of the object,
not of any photograph of it. Measured, mirror IoU against the mask's own left-right flip:

```
    the BUILT glyph  (symmetric by construction)     0.9777
    the WORKSHOP badge -- what rev 63 traced         0.4111
    the TARGET BUS badge, ref_nolita_front34.jpg     0.4812
    KILL: the built glyph sheared by 0.30            0.2732
```

`probe_rev63_angles.desquash()` rescales the axes by a fitted ratio and **never rotates**,
so a three-quarter view's shear survives it. **The trace is faithful to the frame, and the
frame is not orthographic** — it traced a SHEARED VW, and face-on that is the blob.

**Then shear the BUILT glyph and change nothing else — no constant, no spine, no shape:**

```
    shear   mirror IoU   elongation   cells
     0.00     0.9777       2.388        6
     0.20     0.3574       2.809        8
     0.40     0.2716       3.400        8
     0.60     0.2294       3.853        8
    PHOTO   0.411/0.481    3.390        7
```

**C8's 3.390 target and C6's 7 BOTH lie inside the range a pure shear of the SHIPPED glyph
sweeps.** Neither gate can separate *"the glyph is the wrong shape"* from *"the frame is
oblique"*. **F175 showed the gates pass on a bad glyph; this shows their TARGETS carry the
viewing angle.** Rule 39. Painted: `probe_scratch/rev64_shear.png` — the last three panels
lean the same way and the first does not.

**CEILING, STATED, NOT AN OVERCLAIM (F185).** This does **not** show shear is the whole gap.
Mirror IoU saturates near shear 0.3 while elongation keeps climbing; at the shear that first
matches the photographs' own mirror IoU the elongation is **2.809, not 3.390**. **The badge's
ring is a CIRCLE on the real object, so its image is an ellipse whose centre, axes AND
ROTATION give the homography outright. Nothing in this project has ever fitted it.** That is
rev 65's first move and it is well-posed.

### §3.4 T3 WAS A RASTERISER DEFECT, NOT A TRACE DEFECT (F186, F187)

The brief and `LEDGER_rev63.md` §7 both say *"the disagreement is the RING (IoU 0.508), not
the glyph (interior IoU 0.78)"* and both call it *"already done and in the probe"*.
**`grep 0.508 probe_rev63_trace.py` → 0.** The decomposition existed only in prose.

Measured: `raster()` mapped the outline's [-1,1] onto the **full 276 canvas** while the
badge's own bbox is rows **11..264** — every traced point drawn **9.1 % too far out**. Rule
38. Painted at `probe_scratch/rev64_t3_diff.png`: red on one side of every stroke, green on
the other, which is what a scale error looks like and what found it.

```
    the traced GLYPH reproduces its source    0.7848 -> 0.9496
    the whole badge                           0.6412 -> 0.8050
    T3c CEILING, no tracing at all            0.9991   <- so the bar IS reachable
```

T3's OBJECT is **re-based** from "the badge" to "the glyph" — cause named, **four companion
rows**: T3b sweeps the band (no concentric annulus beats 0.6758), T3c is the ceiling, **T3d
is the KILL that goes red if registration is removed**, T3e still prints the whole-badge
figure every run. **Re-based, not relaxed, and not dropped.**

**And T4's whole column broke rule 38 in the direction that flattered the conclusion it was
used for (F187).** The brief's headline — *"the traced glyph already scores 0.7129 where the
shipped one scores 0.5367"* — was two rulers. **The real margin is +0.1438, not +0.1762.**

### §3.5 RULE 13, DISCHARGED LATE (F190)

**`EMBLEM_HANDOFF.md` is the designated carrier for the project's top item and it
contradicted the tree it describes for a whole revision.** Its §5b.2 reads *"**No constant
in `t1_core.py` was changed.** `STATE.md` is untouched, **and that is a control**"* — while
`t1_core.py` carries all six of rev 63's constants and `t1_detail.py` carries `wfrac=0.1800`.
F170's register row still said *"DO NOT ship the canonical fit"*. Both are struck through in
place with the machine's own values quoted. Found by the adversary, confirmed **against the
source, not against the file**.

### §3.6 THE ADVERSARY (F189) — rule 15, first run since rev 61

Rev 62 and rev 63 both shipped without one. It returned **fourteen findings**. Four verified
here in the source and corrected: `post.py` does **not** *"default every gain to 0.0"*
(`_FLOATS` = bloom 0.0, ca 1.0, vig 1.0, grain 1.0 — **one of four**, and the same wrong
sentence was in the brief, in F146 **and** in `judge_set.sh`'s header); `audit_adversary.py`
prints **42**, not 36; the ring/interior diagnosis is not in the probe; and **`deliver.py`
contains no output resolution at all** — the *"2400×1650"* the brief makes the **premise of a
question to the owner** appears nowhere in the code or in any ledger. **That one was caught
before the question was asked and the premise was withdrawn in the asking.**

### §3.7 THE HUBCAPS (brief §3 item 3) — LOOKED AT, AND THEY ARE FINE

The spine is shared by five objects (F69), rev 63 changed it, and nobody had looked.
Cropped off `out/r64_side.png`: both visible hubcap badges read as an intact chrome ring with
a legible V-over-W at ~30 px. **No five-petal failure.** `probe_scratch/rev64_hub_*.png`.
*(Also visible in that crop, and it is a live panel item: the tyres have no tread and no
sidewall lettering.)*

### §3.8 TWO OWNER RULINGS (F191, F192)

Asked with the question tool, multiple choice, with the crops attached.

> **"Keep holding — fix the emblem first."** — the full delivery render. **His rev-58 gate
> is REAFFIRMED, against a revision that could have shipped.**

> **"Bigger — large-format print."** — over the pipeline's 3840×2640 default. **The exact
> dimension is STILL OPEN**: the option invited him to name the medium and he did not.
> **Do not re-ask it cold.** What is settled and actionable: **3840 is not the target**, so
> `hq_render.py`'s banded path must be proven larger, and `stitch.py`'s seam check (F49,
> exit 2) has never been exercised above 3840.

---

## §4 WHAT REV 64 DID **NOT** DO — READ THIS BEFORE PLANNING REV 65

**Shorter than what it did, and the more useful one.**

1. **THE EMBLEM IS STILL NOT RIGHT, AND IT DID NOT MOVE THIS REVISION.** No constant
   changed. `probe_rev46_vw.py` still reads **9 checked, 3 FAILED — C4, C5, C6**, exactly as
   it did at rev 63's close. What changed is that **two of those three gates are now known
   not to mean what they were taken to mean** (F184).
2. **THE RING ELLIPSE IS NOT FITTED (F185).** It is the next move, it is well-posed, and
   **it is not started**. Until it is, C6's 7 and C8's 3.390 stay unusable as targets and
   F181's six contact angles still have no target.
3. **NO DELIVERY RENDER**, by his ruling — and **the large-format path is unproven**. F192.
4. **F156 was not re-based or annotated — FOUR revisions now.** `flank_compare`'s `Senor`
   row scores a deliberate departure and still scores it as a defect.
5. **`REMAINING_WORK_rev61.md` §I IS STILL UNTRIAGED — 27 rows, FOUR revisions.**
   `PANEL_rev61.md` untouched.
6. **THE ADVERSARY'S OTHER TEN FINDINGS ARE RECORDED, NOT ACTED ON** — in particular
   **`probe_rev63_shapefit.py`'s baseline is stale AND read at `CAP_EMBLEM_WFRAC`, the
   HUBCAP's weight, which is F178's exact trap and is still unfixed.** The brief tells the
   next context to run that probe.
7. **NOTHING OUTSIDE THE EMBLEM WAS TOUCHED.** Glass, tyres, the tail's barrel, the shut
   lines, the galley, F143's roof loudspeakers, the F10–F14 cluster: all untouched.
8. **The two disputed ceilings** (specular-event census, ground shadow) were not tested.
9. **`mottle_measure.py` still is not measuring the mottle.**

---

## §5 WHAT THIS REVISION GOT WRONG IN ITS OWN WORK

**Budgeted for, per `CLAUDE.md`: every recent revision has caught several of its OWN
instruments being wrong.**

1. **T4's "IoU as rev 63 read it" column carried a THIRD ruler under a SECOND one's label.**
   Once `rep` was registered, that column silently reported the registered figure for the
   traced row. Caught by reading the row against its own sentence — which is how rev 63
   caught its C24. Fixed to use the un-registered raster explicitly.
2. **My re-implementation of rev 63's raster is not byte-identical to it, and the difference
   is a second defect of rev 63's.** It reads 0.6412 where rev 63 published 0.6504: the old
   code drew the ring at centre 137.5 / radius 137.5 and the glyph at 138.0 / 138.0 — the
   ring and the strokes inside it on half-a-pixel-different frames, in one function. Stated
   in `raster.__doc__` rather than chased.
3. **I graded my own F190 `CORRECTED-rev64` and the register's grade guard went red.** That
   word is not in its vocabulary. **The vocabulary was NOT widened** — widening it to make
   my own row pass is precisely the laundering the guard's own comment says it exists to
   stop. Regraded MEASURED-rev64. Watched failing, then watched passing.
4. **I nearly asked the owner a question built on a figure that is in no source file.**
   The brief's "2400×1650" premise was withdrawn in the asking only because the adversary
   found it first.

---

## §6 THE ONE THING TO CARRY IF ONLY ONE THING IS CARRIED

**Stop measuring the emblem against a photograph of the badge until the badge's ring has
been fitted as an ELLIPSE and the frame un-projected.** Eighteen revisions of *"the built
cells are 1.42× too round"* were read off images that are not mirror-symmetric, and a pure
shear of the glyph already in the tree spans both targets. **The ring is a circle on the real
object. Fit it, and every emblem target can be re-read on the mark instead of on a
photograph of it.**

---

## §7 THE BRANCH, MEASURED AT CLOSE — NOT AT PICKUP

```
HEAD                                     11 ahead / 0 behind origin/main
origin/claude/bus-model-rev57-yvrlhi      6 ahead of origin/main -- MERGED INTO HEAD
                                          (bootstrap row 9 asks about HEAD, and is GREEN;
                                           this goes to 0 when rev 64 reaches main)
every other branch                        0 ahead
bootstrap.sh        ALL 10 PASS      at the handoff commit, clean tree
verify_clone.sh     ALL 298 PASS     at the handoff commit, clean tree
audit_brief.py      10 checked, 0 FAILED
audit_adversary.py  48 asked, 0 BROKE
```

**The pickup figure is not the close figure. `origin/main` moved mid-revision at rev 51 and
rev 55, and an adversary once caught a brief shipping only the pickup one.**

