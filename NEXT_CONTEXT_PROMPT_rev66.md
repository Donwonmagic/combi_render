# NEXT CONTEXT PROMPT — rev 66

## §0.0 DO THIS FIRST — THE WHOLE DECISION, IN TWENTY LINES

**Before you read another word, put the machine to work. It is CPU-bound and idle right now.**

```bash
cd /home/user/combi_render
./bootstrap.sh                 # the toolchain is NOT on the clone -- this builds it
nohup setsid env T1_SUB=1 T1_PREVIEW=front,side,hero,hero34r T1_PFX=r66 T1_RX=1600 T1_RY=1100 \
  T1_SAMP=96 /tmp/blender/blender -b -P build.py > /tmp/r66.log 2>&1 < /dev/null &
```

`out/` is untracked and **starts EMPTY**. **`bootstrap.sh` first**: at rev 58–62
`/tmp/blender/blender` did not exist. Then start the render, then read.
**`grep -c Saved: /tmp/r66.log` must be 4** — a backgrounded runner's exit code is the
redirect's. **USE `setsid`, NOT A BARE `nohup &`** (F173).

**AND CHECK YOUR CLONE IS THE TIP.** Rev 62, 63, 64 **and 65** all arrived **SHALLOW**. A content
check cannot detect that you are on an old commit of the same repository. **Only `git fetch
--unshallow` and the ahead/behind loop in §1 find it.** Run §1 before you trust anything.

**THEN RUN `./judge_set.sh r66`.** `post.py` implements bloom → CA → vignette → grain and the
preview path **never calls it** (F146). Judge photorealism on the `_post` set, never the raw
one. *(**ONLY `bloom` defaults to 0.0** — `ca`, `vig` and `grain` default to **1.0**. Three
documents said "every per-stage gain" until rev 64; F189a.)*

**READ `LEDGER_rev65.md` §7 AND §4 BEFORE YOU PLAN** — what rev 65 did NOT do, and the four
things it got wrong in its own work.

---
## §0.05 THIS BRIEF WAS AUDITED AGAINST THE MACHINE — AND WHERE IT IS WEAKEST

**HOW IT WAS AUDITED (rule 17).** Every figure in §0.06, §0.065 and §0.07 was RE-RUN at the
handoff commit, not transcribed. Every path resolves (`audit_brief.py` **10 checked, 0
FAILED**) and `audit_adversary.py` asks **48, 0 BROKE**. **THAT IS THE MECHANICAL HALF ONLY.**

**AND REV 65 IS THE REVISION THAT FOUND OUT WHY THAT MATTERS.** The figure this project has
quoted for the emblem's defect since rev 60 — *"r 0.6638 … floating 18.9 mm"* — **is a
string literal in a probe's message** (F198). It passed every audit, every brief, every
register row and two of my own reports, because **no script can catch a number that prints
without being measured.** **Assume this document contains another one. Go looking.**

**WHERE THIS BRIEF IS WEAKEST:** **§0's inherited gate table** and **§4**, which are the two
longest carriers and are almost entirely inherited text. Rev 64 found a seven-revision
misattribution in §4 and rev 65 found the literal above. **Start an adversary there.**

**WHAT REV 65 GOT WRONG IN ITS OWN WORK — FOUR, in `LEDGER_rev65.md` §4**, including a
rotation search that scored better and rendered as horizontal bars, and a reach clustering
that nearly published two interior vertices as floating terminals.

**`verify_clone.sh` WAS RUN ON THE ACTUAL HANDOFF COMMIT, not on the tree later.**

---
## §0.06 THE BIG ONE: THE SENTENCE THAT HAS NAMED THIS DEFECT FOR FIVE REVISIONS IS A
## STRING LITERAL — AND THE REACH, MEASURED LIVE, IS NOT WHAT IT SAYS

> *[owner, rev 65]* **"I can't believe that we can't even accomplish a publicly available
> emblem, and we still have work to do on the shape of the nose."**

**`probe_rev46_vw.py`'s C6 prints:** *"the mesh names them: the W's two outer arms, at r
0.6638 against a band inner edge of 0.7988, floating 18.9 mm"*. **THOSE THREE FIGURES ARE
HARD-CODED IN THE MESSAGE STRING.** They are rev 60's, at rev 60's constants. **Rev 63 moved
all six spine constants and the sentence did not move.** It prints identically under
`T1_VW_CAPMIN=1` while the cell count goes 6 → 2 — which is how it was caught. **F198.**

**SO THE REACH WAS MEASURED LIVE OFF THE MESH, FOR THE FIRST TIME (F199).** R=1 units,
extreme 0.8140, band inner edge 0.7752:

```
    TEN corner vertices at 0.8089 .. 0.8140  -- within 0.6 % of the extreme, PAST the band
    TWO cap corners at 80..97 % of the extreme -- a HAIR INSIDE the band's inner edge
    six more vertices under 80 %             -- INTERIOR points, NOT terminals
```

**ALL SIX TERMINALS REACH. The defect is TWO CAP CORNERS**, at the 3 and 9 o'clock strokes.
One hairline of cream merges the two cells either side, and that is C6's 6-instead-of-7.
**It is NOT "the W's two outer arms".** Painted: `probe_scratch/rev65_reach_paint.png`.

**AND EVERY KNOWN LEVER IS NOW MEASURED, NOT ARGUED:**

```
    as shipped                       6 cells   elongation 2.39
    T1_VW_CAPMIN=1                   2 cells   elongation 1.31
    T1_VW_PUREFIT=1                  6 cells   elongation 2.40
    T1_VW_CAPMIN=1 T1_VW_PUREFIT=1   6 cells   elongation 2.24   <- THE PAIR, TRIED, REFUTED
```

**CAPMIN's failure mechanism, measured:** its extreme runs **0.8140 → 0.9250**, and
`t1_detail._fit_glyph` re-normalises by the GLOBAL extreme, dragging every other terminal
12 % off the band. **And the pair the rev-58 note has called *"half of one fix"* each for
five revisions — *"the pair the rev-58 note says was never tried"* — IS NOW TRIED. Refuted.**

**WHAT IS LEFT, AND IT IS §3 ITEM 1:** cut each terminal **ON THE BAND'S ARC** instead of
perpendicular to the stroke. Both corners then land on the band by construction, **the extreme
does not move**, and `_fit_glyph` has nothing to re-normalise away. It is what a stamped mark
disappearing under a band actually is. **Nobody has written it.**

---
## §0.065 AND THE TARGETS THEMSELVES WERE WRONG — THE RING IS FITTED AS AN ELLIPSE AT LAST

**The badge is a CIRCLE on the real object.** Fitted from the second moments of the filled
badge it reproduces the region's own area to **0.05 %** and **0.11 %**; photographed axis
ratios **0.6596** and **0.5810** come out **0.9970** and **0.9994** — circles.
**Proved on a known answer first:** the built glyph (mirror IoU 0.9777), squashed 0.72 and
sheared 0.35 to 0.2369, comes back at **0.9585**.

```
                                    cells   elongation
    C6/C8 as they stand (squashed)    7        3.390
    UN-SQUASHED workshop              6        2.960
    UN-SQUASHED target bus            7        2.627
    the BUILT glyph, unchanged        6        2.388
```

**THE FAMOUS "1.42× TOO ROUND" IS 1.24×, OR 1.10× AGAINST THE TARGET BUS'S OWN BADGE** — and
the residual shear still inflates even those (F185 is NOT closed), so the true target is lower
still, **nearer what is already built**. Cells are not stably 7 either. **F194.**
**`python3 probe_rev65_unproject.py`, and LOOK at `probe_scratch/rev65_norot.png`.**

---
## §0.07 THE MACHINE'S VERDICT AT CLOSE OF REV 65 — every one watched print

```
bootstrap.sh              ALL 10 PASS
verify_clone.sh           ALL 303 PASS on a clean tree, AT THE HANDOFF COMMIT
                          <- 0 FIDELITY, 303 SELF-CONSISTENCY.  298 -> 303.  NO row relaxed.
probe_rev65_unproject.py  10 checked, 0 FAILED   -- NEW.  The ellipse fit and its POSITIVE
                          CONTROL.  C4 was RE-BASED on what the method claims, not relaxed
probe_rev64_shear.py      6 checked, 0 FAILED
probe_rev63_trace.py      ALL CONTROLS PASS
vw_pressing.py            5 checked, 0 FAILED
probe_rev46_vw.py         9 checked, 3 FAILED -- C4, C5, C6.  UNCHANGED from rev 63, and its
                          C6 MESSAGE IS STILL THE LITERAL (F198 is recorded, NOT fixed)
probe_rev63_canon.py      5 checked, 0 FAILED
probe_rev63_reach.py      ALL CONTROLS PASS
trace_outline.py          SELFTEST PASS (10);  svgraster.py SELFTEST PASS (9)
audit_brief.py            10 checked, 0 FAILED
audit_adversary.py        48 asked, 0 BROKE
flank_compare.py          FAILS.  worst region `i` at 0.687 of its own ceiling
gloss_compare.py          FAILS at 0.442 of the photograph's spread (bar 0.60)
probe_rev59_nose.py       5 checked, 0 FAILED -- AND IT DOES NOT MEASURE THE NOSE'S SECTION,
                          which is what he asked about (F197)
probe_rev59_door.py       8 checked, 1 FAILED (M3, BY DESIGN)
```

**AND THE STANDING WARNING, WHICH `verify_clone.sh` PRINTS ITSELF.** A green check is not
evidence about the vehicle. **Not one of those 303 rows compares the model to a photograph.**

---
## §0. THE GOAL, AND HOW FAR OFF IT WE ACTUALLY ARE

**CARRIED FORWARD FROM THE REV-55…64 BRIEFS. It is not mine and it is not to be dropped —
rule 16.**

**PHOTO-REALISTIC PARITY WITH THAT EXACT BUS.** Not "a convincing VW bus" — *that one*, the
red Señor Tacombi combi in the frames on this repo. **Any single measurement off is
unacceptable, per-measurement and not on average.** A model right in ninety places and wrong
in one is not 99 % done, because he will look straight at the one. **At rev 58 he did exactly
that, at the emblem, for the fifth time. At rev 61 he did it again. At rev 62 he said *"I am
sick and tired of not being able to execute a publicly available emblem."***

**AT REV 63 THE EMBLEM CHANGED AND NOW READS AS A V OVER A W ON THE NOSE. IT IS NOT RIGHT,
AND AT REV 64 IT DID NOT MOVE.** Held next to the photographs, four things are still visibly
wrong: the glyph does not fill its ring the way both photographs do, the V is too narrow, the
W's outer arms are too short, and the strokes are thinner than the pressing's. **The W's two
outer arms visibly FLOAT short of the ring — C6 measures it at 18.9 mm and you can see it in
`probe_scratch/rev64_front_emblem.png`.** What is new is that **two of the three gates that
would score a fix are now known not to mean what they were taken to mean** (§0.06).

**AND HERE IS THE HONEST DISTANCE — THE GATE TABLE, WHICH AN ADVERSARY ONCE CAUGHT A BRIEF
DROPPING.** `verify_clone.sh` ends **ALL 303 PASS**: **0 FIDELITY, 303 SELF-CONSISTENCY.**

| gate | state MEASURED at close of rev 64 |
|---|---|
| `flank_compare.py` | **runs, FAILS.** Worst region **`i` at 0.687 of its own ceiling**; the `Senor` row scores a **DELIBERATE DEPARTURE** — F156, **FOUR revisions un-re-based** |
| `gloss_compare.py` | **runs, FAILS at 0.442** (bar 0.60). Model-side lever EXHAUSTED (F60/F62) — **but F62's ceiling is DISPUTED on measurements** |
| `probe_rev46_vw.py` | **C4, C5, C6 FAIL; C7, C8 PASS — AND C6's AND C8's TARGETS ARE NOW UNDER F184.** Read §0.06 before quoting either |
| `probe_rev64_shear.py` | **NEW. 6 checked, 0 FAILED.** The reason the two above cannot decide the emblem |
| `probe_rev63_trace.py` | **ALL CONTROLS PASS.** The trace is sound; what it traced is a sheared frame (F183) |
| `probe_rev59_nose.py` | **M1 PASSES lens-ruled — AND THAT IS NOT CLOSURE (F136).** Bezel-ruled 1.550 / 1.584 against rim-ruled 1.951–2.121 |
| `mottle_measure.py` | **runs, and it is NOT measuring the mottle** — 1.1–2.0 % of it |
| `probe_rev45_ground.py` | item D's gate, `T1_NOUNDER`'s only consumer. **G4 0.3602 built / 0.5475 ablated / 0.057 photographed** |
| `probe_rev59_door.py` | `T1_DOOR_STALE`'s gate. **8 checked, 1 FAILED (M3, BY DESIGN)** |
| `cream_rms.py` | `run()` is the LIVE photograph-side cream path |
| `visibility_budget.py` | the RANKING, not a gate. **PASS IT A `.png`** — `visibility_budget.py 3840` alone falls back to globbing `out/*hero*.png` by mtime, **which IS F132's defect**, so the command printed in every brief through rev 64 reproduces the bug the sentence beside it warns against (F189) |
| everything else | self-consistency |

**AND AT REV 61 HE ADDED A STANDARD.** *"I want this 3d model to look like new. Enhanced from
the photo."* That is not the same as WEATHERED, which SPEC §3 locks. **Where the two collide,
say so and put it to him** — do not silently pick one.

### §0.1 THE REFERENCE SET IS COMPLETE, AND IT IS GUARDED FRAME BY FRAME

> *[owner, rev 54]* **"we have all references that we need on repo and I want to make sure
> that is never forgotten."**

**ONE: WHAT WE HOLD IS WHAT WE GET. STOP PARKING WORK BEHIND A PHOTOGRAPH.** Where a frame
genuinely cannot answer, the result is *"it cannot be recovered from what we hold"* — a real
result, stated with its ceiling. **Rev 61 produced four; rev 63 one; rev 64 one more**: F185,
the amount of shear in the two badge frames, which cannot be separated from shape until the
ring is fitted as an ellipse.

**TWO: THEY CANNOT BE RE-SHOT, SO THEY ARE CHECKSUMMED INDIVIDUALLY.** **16 `ck "ref …"` rows
name them one at a time** *(the "18" in the rev-63 and rev-64 briefs counted two aggregate
rows that by their own words do not name a frame — F189)*:

* **the RED target bus** — `ref_side.jpg`, `ref_rear34.jpg`, `ref_playa_34.png`,
  `ref_nolita_front34.jpg`, `ref_nolita_front34b.jpg`, `ref_nolita_flank.jpg`,
  `ref_nolita_doorshut.jpg`
* **NOT the target, geometry only** — `ref_workshop.jpg` is the **GREEN** vehicle;
  **`IMG_2073.jpeg` is ALSO the GREEN vehicle**; `bus_model_ref.JPG` is a **SCHOOL BUS**, a
  fidelity bar only. **Paint and artwork do not transfer between vehicles; geometry does
  (rule 11)** — *and the corollary rev 63 leaned on: the nose roundel's SHAPE is the factory
  chrome PRESSING, which is geometry and DOES transfer; only its colour is artwork (F141).*
  **REV 64 ADDS THE LIMIT ON THAT COROLLARY: the shape transfers, but the PROJECTION does
  not. `ref_workshop.jpg` shows the pressing obliquely (mirror IoU 0.4111) and no de-squash
  removes it (F184).**
* **AND RULE 11 APPLIES BETWEEN LIVERY STATES OF THE SAME VEHICLE**, which killed F99, F100
  and F140: `ref_nolita_front34b.jpg` has a chalkboard lid and no folk art.
* **AND IT APPLIES BETWEEN ERAS OF A TRADEMARK** — F168. `vw_canonical_2019.svg` is the mark
  as REDRAWN IN 2019 and is **a different object** from the 1955–67 pressing: 3 cells /
  elongation 1.597 against the photographed badge's 7 / 3.390 at one raster. **It is
  deliberately NOT named `ref_*`.**
* **derived/annotated** — `ref_grid.png`, `ref_side_grid.png`, `ref_nose_grid.png`,
  `ref_band_grid.png`, `ref_x6_lanczos.png` *(a 6× upsample of the RETIRED thumbnail —
  "interpolation, no new information")*
* **retired** — `ref_source.jpeg`, a 246×197 thumbnail the record itself retired
* a **floor of 54** reference-class tracked images, and **the five byte-identical pairs are
  asserted to stay five** — a sixth group means a frame arrived that duplicates one we hold,
  which is **not corroboration** and has fooled this project before.

**AND `ref_playa_34.png` IS UNDER-USED.** Rev 61 verified its white balance **neutral** on the
paving (116,119,120) and used it, not `ref_side.jpg`, to judge paint. `ref_side.jpg` and
`ref_rear34.jpg` are both globally WARM.

---
## §1 START HERE — MEASURE THE BRANCH, DO NOT TRANSCRIBE IT

```bash
git fetch --all --prune
git rev-parse --is-shallow-repository        # <- rev 62, 63 AND 64 all arrived TRUE
for b in $(git branch -r | grep -v HEAD); do
  printf "%-52s ahead %-3s behind %s\n" "$b" \
    "$(git rev-list --count origin/main..$b)" "$(git rev-list --count $b..origin/main)"
done
git diff --name-only HEAD...origin/main        # <- HIS PHOTOGRAPHS ARRIVE HERE
./bootstrap.sh          # read ROW 9, and read the "N ahead / M behind" NOTE line
./verify_clone.sh       # ALL 303 PASS -- and read its verdict block
```

**MEASURED AT REV 64 PICKUP:** the clone was **SHALLOW**; `fetch --prune` printed
`- [deleted] origin/claude/new-session-e854rn` — **the designated branch, before anything had
been pushed to it, the EIGHTH RUNNING**; HEAD was **0 ahead / 0 behind** `origin/main`; and
**row 9 FAILED** on `origin/claude/bus-model-rev57-yvrlhi`, 6 commits, **stranded since rev
57 under an owner ruling to merge it**. **IT IS NOW MERGED (F188). EXPECT THE BRANCH DELETION
AGAIN AT REV 65.**

> **AND THE LESSON THAT COST SEVEN REVISIONS: the rev-64 brief's §1 asserted rev 63 had
> measured "no branch carried work HEAD did not have". It was true when written and false
> 24 minutes later. `bootstrap.sh` row 9 outranks that sentence and every sentence like it,
> INCLUDING THIS ONE.**

**AND MEASURE IT AGAIN BEFORE YOU FINISH.** `origin/main` moved mid-revision at rev 51 and
rev 55. **At rev 64's CLOSE, HEAD was 11 ahead / 0 behind `origin/main`** — the pickup figure is
NOT the close figure, and an adversary once caught a brief shipping only the pickup one.

> **AND ONE THING THE LOOP WILL SHOW YOU THAT IS NOT A FINDING:**
> `origin/claude/bus-model-rev57-yvrlhi` still reads **6 ahead of `origin/main`** at rev 64's
> close. **It is merged into HEAD**, which is why `bootstrap.sh` row 9 — which asks about
> HEAD, not about main — is green. It goes to 0 the moment rev 64's branch reaches `main`.
> **If row 9 is RED at your pickup, that is a different branch and a real finding.**

---
## §2 THE EMBLEM — **READ `EMBLEM_HANDOFF.md` FIRST, AND READ ITS §5b.2 RETRACTION.**

> *[owner, rev 62]* **"I am sick and tired of not being able to execute a publicly available
> emblem."**

**WHAT IS IN THE TREE:** rev 63's six spine constants (`VW_V_TIP_X 0.3287`, `VW_APEX_Z
0.0538`, `VW_W_ARM_X 1.1002`, `VW_W_ARM_Z 0.4350`, `VW_W_TROUGH_X 0.3111`, `VW_W_TROUGH_Z
-0.6445`) and the NOSE's `wfrac=0.1800`. **`EMBLEM_HANDOFF.md` §5b.2 and F170 both said these
were NOT shipped, for a whole revision, in the designated carrier for this item. Retracted at
rev 64 — F190. Rule 13.**

**DO NOT re-try any of these. Every one is measured, not argued:**

```
reach            T1_VW_CAPMIN            cells 6 -> 2                       (F101)
stroke weight    T1_VW_WFRAC alone       moves the WRONG way against C8     (F152)
six-constant cell-count solve            7 cells only at residual 0.2498    (F103)
separate strokes                         rev 8 did it and got an X          (F113)
the V/W kink                             the PHOTOGRAPHS have the same kink (F138)
terminal angles off the badges           residual 0.1800, WORSE than a bad
                                         control at 0.1167                  (F141)
the workshop badge's LANDMARKS           CEILED -- scale confound           (F153)
THE CANONICAL 2019 VECTOR as a TARGET    a DIFFERENT OBJECT                 (F168)
A REACH TERM as the discriminator        the trident touches in all SIX     (F179)
"no spine can satisfy the cell shape"    REFUTED: 6.877 at 7 cells          (F174)
TRACING THE PRESSING AND MESHING IT      BUILT, RENDERED, WORSE.  It traced
  (new at rev 64 -- the rev-64 brief's   a SHEARED frame.  T1_VW_TRACED
   TOP ITEM, refuted by doing it)        exists and MUST STAY OFF      (F183)
TUNING AGAINST C6 OR C8 AS THEY STAND    their targets carry the viewing
  (new at rev 64)                        angle -- a pure shear spans both   (F184)
C8's 3.390 AS A TARGET AT ALL            un-squashed it is 2.63..2.96 and
  (new at rev 65)                        the build reads 2.388              (F194)
SEARCHING THE MARK'S VERTICAL BY         scores BETTER, renders as
  MIRROR IoU (new at rev 65)             horizontal bars.  The bus is
                                         UPRIGHT in both frames             (F195)
T1_VW_CAPMIN, ALONE OR WITH PUREFIT      2 cells alone; 6 / 2.24 together.
  (the pair, new at rev 65 -- the         THE PAIR THE REV-58 NOTE CALLED
   rev-58 note called it "never tried")   "never tried" IS NOW TRIED        (F199)
QUOTING C6's "0.6638 / 18.9 mm"          IT IS A STRING LITERAL in the
  (new at rev 65)                        message.  Measure it, do not
                                         quote it                          (F198)
```

---
## §3 THE WORK LIST FOR REV 66

> **HE IS OUT OF PATIENCE, AND HE IS RIGHT TO BE.** *"I can't believe that we can't even
> accomplish a publicly available emblem, and we still have work to do on the shape of the
> nose."* **Items 1 and 2 are his two sentences. Do them. Everything else waits.**

1. **BUILD THE ARC-CUT TERMINAL. THIS IS THE EMBLEM'S FIX AND IT IS THE ONLY ROUTE LEFT
   STANDING.** Every terminal cap is currently cut PERPENDICULAR to its stroke, so its two
   corners sit at different radii and one of them lands a hair inside the band (F199, and it
   is painted). **Cut the cap ON THE BAND'S ARC instead** — `t1_core._mitre_outline`'s
   terminal ends, in `vw_bars`. Then **both corners land on the band by construction, the
   GLOBAL EXTREME DOES NOT MOVE, and `t1_detail._fit_glyph` has nothing to re-normalise
   away** — which is exactly what kills `T1_VW_CAPMIN` (its extreme runs 0.8140 → 0.9250 and
   drags every other terminal 12 % inboard). **It is also what a stamped mark disappearing
   under a band physically IS.** Nobody has written it.
   **ACCEPTANCE, and it is not C6 alone: `probe_rev46_vw.py` C6 → 7 cells, AND the rendered
   nose crop held next to `probe_scratch/rev65_norot.png` panels 2 and 4. Rule 41 — the
   render is the arbiter, and it has refuted two winners in two revisions.**
2. **THE NOSE'S SHAPE — HE ASKED FOR IT BY NAME AND THERE IS NO INSTRUMENT FOR IT (F197).**
   `probe_rev59_nose.py` measures the lamp break's ELEVATION, not the nose's SECTION. Rev 51
   held the nose against the photographs and found **a FLAT NOSE** by eye, alongside the
   roundel's short V-arms; the V-arms became the emblem and swallowed fourteen revisions and
   **the flat nose was never worked.** The levers are `t1_shell`'s `V_POW` / `V_POWZ` /
   `V_RISE` — **move `V_POW` and `V_POWZ` TOGETHER** — and they have never been fitted to a
   photographed section. **Build the instrument first: extract the nose's silhouette from
   `ref_nolita_front34.jpg` and `ref_playa_34.png` and compare it with the mesh's own
   section. Then fit. Then render, crop, and LOOK.**
3. **REPAIR C6's MESSAGE (F198).** It is recorded, not fixed. The literal still prints
   *"the W's two outer arms, at r 0.6638 ... floating 18.9 mm"* on every run, whatever the
   glyph does. **Make it name the strokes it actually measured**, and add the kill that goes
   red if it ever stops being a measurement. Until then every quotation of it is wrong.
4. **PUT AN ADVERSARY ON THIS BRIEF (rule 15).** Rev 64's found fourteen.
5. **F156 — `flank_compare`'s `Senor` row scores a DELIBERATE DEPARTURE. FIVE revisions
   unacted.** Re-base the reference or annotate the row.
6. **FIX `probe_rev63_shapefit.py`**, which §6 tells you to run: its baseline is stale and it
   reads `CAP_EMBLEM_WFRAC`, the HUBCAP's stroke weight, where the nose ships 0.1800 —
   F178's exact trap, still unfixed. **F198 is the same disease in a different file: go and
   look for the third case before it bites.**
7. **TRIAGE `REMAINING_WORK_rev61.md` §I** — 27 rows, FIVE revisions.
8. **THE SURVIVING PANEL ITEMS**, untouched for five revisions: the glass is a flat slab
   (0.5 % sd against the photograph's 12.8 %); **the tyres have no tread, no sidewall
   lettering, and are 35 % too light — CONFIRMED BY EYE at rev 64**; the tail is a box where
   the real one is a barrel; every shut line is a 1-px ink stroke with no leading-edge
   highlight; the galley is monochrome; the counter is a floating slab.
9. **F143 — TWO LOUDSPEAKERS STAND ON THE ROOF AND ARE UNMODELLED.** 53 revisions.
10. **THE INHERITED CLUSTER** — F14 (**thirteen** revisions un-re-measured), F15, F10, F20.
11. **`delivery/READ_ME_FIRST.txt` LISTS THE MODEL'S KNOWN DEFECTS TO HIM.** It does not yet
    mention the rev-63 emblem change, F184, F194 or F197.

**RANKING NOTE — AND THE RULE IT CARRIES IS NOT DROPPED.**
**RANK BY PIXELS OF THE DELIVERY FRAME** — `python3 visibility_budget.py 3840
out/r66_hero.png` — **and PASS IT A `.png`**, or
it globs `out/` by mtime and reproduces F132. Its ceiling: pixels are not visibility, so use
it for ORDERS OF MAGNITUDE. **But he has now overridden the ranking twice in two revisions
with two sentences, and the owner outranks it — which is why items 1 and 2 above are his,
not the budget's.**

---
## §4 WHAT WAS ASKED OF HIM — A CARRIER, NOT A LIST OF BLOCKERS

> **READ §0.1 FIRST.** At rev 54 he ruled the reference set on the repo is complete. This
> section is kept in full because rule 16 forbids dropping a carrier.

**`PHOTOS_WANTED_rev52.md` is the carrier for item 7 (ONE HUBCAP, SQUARE ON AND CLOSE).**
Items **1–5** keep their full text in `PHOTOS_WANTED_rev49.md`. **He has said 1–5 are not
possible now. DO NOT RE-ASK THEM.** Item 6 was **DISSOLVED at rev 51**.

**HIS SETTLED RULINGS — DO NOT RE-OPEN OR RE-ASK ANY OF THESE.** W6 makes colour his call;
the roof strips' 0.3 m retired; the wipers withdrawn entire; the lower bay SHUT; the RED bus
is the target and paint/artwork do not transfer between vehicles; the tail board IS on the
vehicle; the marks above the burst are STARS; `lid_rail`'s width *"narrow lip, ~as wide as it
is tall"*; the roughness trade *"ship 0.250"*; the stranded rev-57b branch *"merge it,
renumber its IDs"* — **DISCHARGED AT REV 64, seven revisions late (F188)**; the studio *"keep
studio — ruling stands"* (twice); the front arch *"leave it circular"*.

> **AND ONE LINE OF THAT LIST WAS NEVER HIS — CORRECTED BY ASKING HIM, AFTER REV 62.**
> It carried *"`playa_env.py` is not on the table — do not re-propose it"* from rev 52 to
> rev 64. **That entered as a brief's INFERENCE from W6, whose object is the studio RIG, and
> was applied to a SECOND DELIVERABLE — rule 34 exactly.** Put to him as multiple choice with
> both readings quoted, he ruled the Playa hero **"DEPRIORITISED, NOT CANCELLED"** — which is
> what his own rev-43 words said before that carrier was deleted at rev 44 (**F92**).
> **The correction sat on an UNMERGED BRANCH from rev 57 to rev 64 while every brief kept
> publishing the misattribution (F188).**
>
> **WHAT IT LICENSES: NOTHING TO DO NOW.** *"Focus on the 3d model"* stands, *"keep studio"*
> stands, **no revision works the Playa hero until he opens it**, and **nothing re-proposes
> `playa_env.py` as the delivery frame** — which is also why **F57** stays recorded rather
> than fixed. What changes is that it is a LIVE agreed second deliverable carried in the
> register, and that *"the emotional bar that sits ABOVE clinical accuracy"* is back in the
> record. **Do not re-ask it; do not act on it either.**

**RULED AT REV 65 — BOTH NEW, BOTH BINDING, AND THEY SET THE WORK LIST:**

> ***"I don't think the bus is ready yet. We need the bus to be ready before investing
> seriously in the render."*** — **HIS THIRD HOLD** (rev 58, rev 64, rev 65), and this one
> was VOLUNTEERED, not asked for. It also settles what the render will be when it comes:
> **MULTIPLE SIZES, MAX RESOLUTION, MAX FIDELITY, ALL IN ONE FOLDER.** **F193.**
> **CONSEQUENCE: F192's "prove the large-format chain" drops BELOW the model defects.**
> Do not spend a revision on the pipeline.

> ***"we still have work to do on the shape of the nose."*** — **A SECOND DEFECT, AND IT IS
> NOT THE EMBLEM.** The emblem sits on the nose; he named the nose's SHAPE separately.
> **It corroborates a finding the record already held and never acted on**: rev 51 held the
> nose against the photographs and found **flush headlamps, the roundel's short V-arms, and
> A FLAT NOSE**. The V-arms became the emblem item; **the flat nose was never worked, and
> there is still no instrument for it.** **F197. It is §3 item 2.**

**RULED AT REV 64 — BOTH STILL BINDING:**

> ***"Keep holding — fix the emblem first."*** — the full delivery render. **His rev-58 gate
> is REAFFIRMED, and this time against a revision that could have shipped.** Asked with the
> crop attached, and with the plain statement that the route rev 63 nominated had been built,
> rendered and refuted. **F191. NO DELIVERY RENDER UNTIL HE SAYS SO.**

> ***"Bigger — large-format print."*** — over the pipeline's 3840×2640 default. **THE EXACT
> DIMENSION IS STILL OPEN**: the option invited him to name the medium and he did not. **Do
> NOT re-ask it cold — ask once you have something to show him.** What is settled: **3840 is
> not the target**, so the banded path must be proven larger. **F192.**
> *(And note what the question corrected: the rev-63 and rev-64 briefs both stated
> `deliver.py` "shipped a set at 2400×1650". **That figure is in no source file and no
> ledger** — `deliver.py` carries no output resolution at all. The premise was withdrawn in
> the asking. F189d.)*

**RULED AT REV 62, STILL BINDING:**

> ***"Bright silver, same as Tacombi."*** — the `Señor` word's finish. **This OVERRIDES SPEC
> §3's WEATHERED LOCK FOR THAT WORD ONLY.** SHIPPED as `script_gen.SENOR_TARNISH = 0.0`.
> `T1_SENOR_TARNISH=1` restores the pre-ruling texture byte for byte. **F157.**

> ***"It is going on different backgrounds for promotional material etc. give me everything I
> might need."*** **BUILT**: `T1_ALPHA=1` renders RGBA with the contact shadow in partial
> alpha (**F159**), and `deliver.py` packages full-frame, trimmed and SEPARATED
> vehicle/shadow layers with a plain-language `delivery/READ_ME_FIRST.txt` (**F160**).
> **It does NOT retire the rev-58 hold, which he has now reaffirmed (F191).**

> ***"this is just the render to plug into company merch with different backgrounds once i
> determine the model is done"*** — **HE DID NOT AUTHORISE THE BOUNCE CARD; "keep studio"
> stands.** Consequences in **F155**: the white backdrop is **scaffolding**, a clean matte
> matters, and **the gate is HIM determining the model is done.**

**RULED AT REV 61:** ***"senor Tacombi should be clearer in the render than in that photo.
Well defined. I want this 3d model to look like new. Enhanced from the photo."*** **It
creates a live tension with SPEC §3's WEATHERED lock — surface it, do not silently pick a
side.**

**CARRIED FROM REV 53, AND STILL IN NO OTHER DOCUMENT:** a frame showing the cream **where it
IS chipped**. Rev 54 and rev 55 both lowered its urgency — the band is 0.27 px at every scale
this project ships — but it is **not struck**, and F19 covers the MODELLING of chipping, not
the photograph request.

**AND HE VOLUNTEERED, STILL BINDING:** the emblem needs a fix, and **the full delivery render
waits until the model is right.**

**STILL WORTH HIS TIME AND NOT ASKED:** **F38** — the nose ring band at the top of its adopted
range, which interacts with the emblem *(and with F185: fitting the ring on the frame gives
this a target too)*; **F39/A3** — `Senor`'s ink deficit; and **the local bounce card** both
panels proposed independently, which is a studio change under a ruling he has given twice.

---
## §5 THE RULES — `CLAUDE.md` CARRIES THE METHOD, NOT THE NUMBERED CANON

The canon (rules 1–33) is printed in `NEXT_CONTEXT_PROMPT_rev50.md` §11. Rules 34–44 live
only in the briefs and are carried here — that is rule 16 firing on this file:

> **34. A REQUIREMENT INHERITS ITS OBJECT EXACTLY AS A RETIREMENT DOES.** Check which object
> a *"the record requires X"* sentence is about, and check the cited line exists. **F26 is
> still open. And rev 64 found rule 34's own textbook case still live in §4 for the
> thirteenth revision — see F188.**

> **35. A GUARD WRITTEN AGAINST A POSE ENCODES THAT POSE.** Ask the geometry, never the pose
> it happens to be in. **Rev 64's sibling: a VERIFY row counted "two mitred prisms per wheel"
> and went red on a glyph built as one object — the row encodes the CONSTRUCTION.**

> **36. A GATE ONLY COUNTS FOR WHAT IT CAN SEE — ABLATE THE THING YOU ARE ABOUT TO TUNE,
> FIRST.** **Rev 64 ablated the FRAME rather than the glyph, and that is what found F184.**

> **37. AN ABSENT INPUT MUST NEVER READ AS A MEASUREMENT.** A probe that cannot run must say
> **"NO RENDER"** and exit non-zero.

> **38. TWO SIDES OF A RATIO MUST SHARE A RULER, AND IF THEY CANNOT, SAY SO IN THE ROW'S OWN
> NAME.** **Rev 64 found this twice in one probe: a 9 % scale error worth 0.30 of IoU (F186),
> and a whole comparison column that broke it toward the conclusion it was used for (F187).**

> **39. A GATE'S TARGET IS AN INSTRUMENT TOO, AND MUST BE SWEPT LIKE ONE.** C6's 7 (F139),
> M1's ruler (F136), C8's window (F151) — **and now C6's AND C8's targets together, which are
> read off images that are not mirror-symmetric (F184). This is rule 39's largest instance.**

> **40. WHEN AN OWNER RULING MAKES THE MODEL DEPART FROM THE REFERENCE, THE GATE THAT SCORES
> AGAINST THAT REFERENCE STOPS MEANING WHAT IT MEANT.** **F156, and rev 62, 63 and 64 all
> failed to act on it.**

> **41. A GATE PASSING IS NOT EVIDENCE THE THING IS RIGHT. BUILD THE COUNTEREXAMPLE.** C6,
> C8 and IoU all passed on a glyph that rendered as a Y (F175). **AND AT REV 64 IT FIRED
> AGAIN, ON THE ITEM IT WAS WRITTEN ABOUT: the traced pressing won on cells, on elongation
> and on IoU, and rendered as a blob (F183). The render is the arbiter.**

> **42. A CONTROL'S KILL IS A PRECONDITION ON ITS PASS.** If the kill cannot go red at a
> point in parameter space, the control's PASS there means nothing. **C7 was dead exactly
> where C6 went green (F176). Read the kill first.**

> **43. NEW AT REV 64 — A PHOTOGRAPH IS A PROJECTION, AND A DE-SQUASH IS NOT AN
> UN-PROJECTION.** Rescaling two axes cannot undo a rotation or a shear. Before taking ANY
> shape statistic off a frame, ask what symmetry the real object has and check the frame
> still has it. **The VW mark is mirror-symmetric; both badge frames read 0.41–0.48 against
> the model's 0.9777 (F184).**

> **44. NEW AT REV 64 — WHEN A GUARD GOES RED ON YOUR OWN NEW WORK, THE GUARD IS THE DEFAULT
> WINNER.** Rev 64 graded its own register row with a word outside the register's vocabulary
> and the grade guard failed it. **The vocabulary was not widened; the row was regraded.**
> Widening a guard to admit your own output is the laundering these guards exist to stop.

---

## §6 THIS MACHINE

```
cores 4   RAM 15 GB   Blender 4.5.3 via pip install bpy   subagent concurrency 2
build  T1_SUB=1 ~20 s     render 1600x1100 96 spp ~4.5-5.5 min PER VIEW
```

**`bpy` IS A PIP MODULE HERE**, so `python3 probe_rev46_vw.py` runs in ~1.1 s without the
Blender CLI. **Check whether a probe needs `blender -b -P` before you budget minutes for it.**

```bash
./bootstrap.sh                                               # THE TOOLCHAIN IS NOT ON THE CLONE
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
./judge_set.sh r66                                           # the optics chain (F146)
python3 flank_compare.py out/r66_side.png /tmp/fc.png        # GATE 1
python3 gloss_compare.py out/r66_hero.png                    # GATE 3
python3 probe_rev59_nose.py out/r66_front.png                # READ BOTH RULERS
python3 probe_rev46_vw.py                    # THE EMBLEM GATE -- read C7 first, and read F184
python3 probe_rev64_shear.py                 # WHY C6 AND C8 CANNOT DECIDE IT -- START HERE
python3 probe_rev63_trace.py                 # ALL CONTROLS PASS.  T3 was a rasteriser defect
python3 vw_pressing.py                       # the traced pressing, held to its own source
python3 probe_rev63_canon.py                 # the canonical mark, measured
python3 probe_rev63_ablate.py                # the construction's ceiling
python3 probe_rev63_shapefit.py              # F175's counterexample -- BUT SEE SS3 ITEM 4
python3 probe_rev63_reach.py                 # contacts with the ring, and angles
python3 trace_outline.py ; python3 svgraster.py ; python3 senor_trace.py
python3 cream_rms.py                         # the LIVE photograph-side cream
python3 visibility_budget.py 3840 out/r66_hero.png   # PASS IT A .png -- see F132/F189
T1_SUB=2 /tmp/blender/blender -b -P audit.py         # rewrites STATE.md -- COMMIT FIRST
python3 audit_brief.py ; python3 audit_adversary.py  # rules 15/17, MECHANICAL half only
```

**THE GATES THE ABLATIONS EXIST TO MAKE REFUSE:**

```bash
T1_SUB=1 T1_NOUNDER=1 /tmp/blender/blender -b -P probe_rev45_ground.py  # C5 must REFUSE
T1_SUB=1 T1_PG_PAINT=1 /tmp/blender/blender -b -P probe_rev45_ground.py # paints G4's window
python3 probe_rev59_door.py out/r66_side.png        # M3 fails BY DESIGN
python3 probe_rev61.py emblem --paint               # every mode paints its window
T1_VW_TRACED=1 T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py  # F183's refutation,
                                                    # rebuildable.  IT MUST NOT SHIP
```

**ABLATION SWITCHES — all MEASUREMENT-ONLY:** **`T1_VW_TRACED` (NEW at rev 64 — builds the
traced pressing. It is REFUTED (F183); two verifier rows hold it OFF)**, `T1_VW_WFRAC`
(**F178: it overrides the NOSE's weight, `vw_logo_fit()`'s signature default — NOT
`CAP_EMBLEM_WFRAC`, which is the HUBCAP's**), `T1_VW_CAPMIN`, `T1_VW_PUREFIT`,
`T1_VW_CELLSOLVE`, `T1_VW_DUMP`, `T1_VW_RES`, `T1_VW_WSWEEP`, `T1_VNOSE_DIV`, `T1_BULB_STR`,
`T1_BULB_BASEV`, `T1_SENOR_BREAKS`, `T1_SENOR_TARNISH`, `T1_ALPHA`, `T1_NOUNDER`,
`T1_UNDER_ZBUG`, `T1_UNDER_PROUD`, `T1_UNDER_VIS`, `T1_UNDER_YBUG`, `T1_UNDERSEAL`,
`T1_VPOW`/`T1_VPOWZ` (**move them TOGETHER**), `T1_VRISE`, `T1_DOOR_STALE`, `T1_NORIG`,
`T1_RIG`, `T1_WORLD`, `T1_MOT_AMP`, `T1_GL_WRGH`, `T1_BODY_RGH`, `T1_GC_ABSSPREAD`,
`T1_GC_LOOSEMASK`, `T1_GL_TILES`, `T1_PG_PAINT`, `T1_BAREMAT`, `T1_CLAY`.

**FACTS ABOUT THIS MACHINE THAT BITE:**
* **EVERY MEASUREMENT THROUGH `shader_solve._render` IS 8-BIT (F42)**, whatever
  `color_depth` says.
* **`mottle_measure.py` names its output by `MOTTLE_AMP`**, so two runs differing only in
  `MOTTLE_M` **OVERWRITE EACH OTHER'S PNG**.
* **`probe_rev54_aov.py` and `probe_rev55_truenorm.py` write EXR into `probe_scratch/`** —
  delete them before committing and keep the PNGs.
* **`script_gen.py` IS NOT CALLED BY `build.py`.** Change it and regenerate `tex/senor.png`
  by hand, or the render silently uses the old texture.
* **`lid_gen.py` is NOT called by `build.py`** either.
* **`vw_pressing.py`'s `trace()` is NOT called by `build.py`** — the outline is a committed
  literal and the selftest is what holds it to the photograph. That is deliberate.
* **`audit.py` rewrites `STATE.md`. COMMIT FIRST** — and regenerate it after ANY geometry
  change.
* **LAUNCH LONG RENDER QUEUES WITH `setsid`, NOT A BARE `nohup &`** — F173.

**THE DELIVERY CHAIN, WHICH IS NOT THE PREVIEW CHAIN:**
```bash
T1_SUB=2 /tmp/blender/blender -b -P hq_render.py    # ONE build, 10 bands, WITH MARGIN
python3 stitch.py out/hq_hero_raw.png ...           # CHECK ITS EXIT CODE -- 2 on a seam (F49)
python3 post.py out/hq_hero_raw.png out/hq_hero.png # optics LAST, never per strip
```

**THE DELIVERY FRAME — DO NOT RUN IT. He REAFFIRMED the hold at rev 64 (F191). And he needs
LARGE FORMAT, which this chain has never been proven at (F192).**

---

## §7 THE STANDARD, IN HIS WORDS

We are recreating a photorealistic version of **that exact bus**, and **any single measurement
off is unacceptable** — per-measurement, not on average. **Ground in the reference, build,
adversarially audit, iterate.** Never build before grounding. Never call it done off
self-review. Report the measurement **with its ceiling**, never a self-assigned score. Do not
say anything is ready — say what is fixed, what is still wrong, and what you measured.

**RENDER IT, CROP IT, AND LOOK AT IT, before and after every change.** Every defect this
project has shipped passed `VERIFY: 0 fail, 0 warn` and was found by looking at a crop.
**At rev 64 the traced pressing won on every statistic the project owns and rendered as an
unrecognisable blob. One crop settled it in ten seconds.**

**When you need something from him, ask as MULTIPLE CHOICE with the reference material
attached — one crop, one mark, one sentence — and ASK IT WITH THE QUESTION TOOL.**
**And CHECK THE PREMISE FIRST: rev 64 came within one step of asking him a question built on
a figure that exists in no source file (F189d).**

---

## §8 THE OPEN-FINDINGS REGISTER — `OPEN_FINDINGS.md`

**IT IS A CARRIER (rule 16). Rows leave it only by being CLOSED with the measurement that
closed them, or RETIRED with the ruling that retired them. Never by being dropped.**

**Rev 65 added F193–F199**, of which **three are refutations** — two of work done in the same
revision — and **two are OWNER STATEMENTS**. **F198 is the one that changes what the emblem's
defect even IS: the sentence naming it was a string literal.** Rev 64 added F183–F192.

**THE POINT OF THE FILE IS THE PROVENANCE GRADE, NOT THE LIST.** An `INHERITED` row is a
claim. **GRADE DECAY IS ITSELF A FINDING.** *(And the grade vocabulary is
MEASURED / RECOMPUTED / INHERITED / RULED / CEILED / OBSERVED. **Do not widen it** — rule 44.)*

**STILL INHERITED AND OLDEST:** **F14** (`gal_end_f`'s sight lines, **rev 52 — THIRTEEN
revisions un-re-measured**), F15, F20, F10, and **F18** (the die-cut sticker, rev 44 — the
oldest live row and the project's original deliverable).

**AND `REMAINING_WORK_rev61.md` §I IS STILL NOT TRIAGED** — 27 rows, **five revisions**.

---

## §9 THE HORIZON BEYOND REV 66

**CARRIER: re-rank it, do not rewrite it, and say what moved.**

**WHAT MOVED AT REV 65.** The badge's ring was **fitted as an ellipse** for the first time in
the project's life, which **re-based C8's target from 3.390 to 2.63–2.96** and shrank the
emblem's headline defect from 1.42× to 1.10–1.24×; the reach was **measured live off the mesh
for the first time**, which showed the defect is two cap corners and **not** what the record
says; **the sentence naming that defect was found to be a string literal**; and **three more
routes were refuted**, one of them the pair the record had called "never tried" for five
revisions. **Two owner statements arrived.** **What did NOT move: the emblem itself, the
nose, and everything outside them.**

**WHAT MOVED AT REV 64.** The traced pressing was built, rendered and refuted; the reason
refuted both emblem gates with it; `bootstrap.sh` row 9 went green after seven revisions.

| horizon | the work | why |
|---|---|---|
| **next** | **THE ARC-CUT TERMINAL (§3 item 1)** | The only emblem route left standing, and the geometry asks for it |
| **next** | **THE NOSE'S SECTION (§3 item 2, F197)** | **He asked for it by name** and there is no instrument for it |
| **next** | **REPAIR C6's LITERAL (F198)** | Every quotation of it is currently wrong |
| **next** | **AN ADVERSARY ON THIS BRIEF** | Rev 64's found fourteen; rev 65 found a literal no script could |
| **near** | **F156 — the `Senor` gate row scores a DEPARTURE** | FIVE revisions unacted |
| **near** | **Fix `probe_rev63_shapefit.py`** | Stale baseline AND the hubcap's weight (F178/F189) |
| **near** | **Triage `REMAINING_WORK_rev61.md` §I** | 27 rows, five revisions |
| **near** | **Glass, tyres, the tail's barrel, the shut lines** | Untouched for five revisions |
| **near** | **F143 — the roof loudspeakers** | Unmodelled since rev 12 — 53 revisions |
| **LOWERED** | **F192 — prove the large-format chain** | **He ruled the MODEL comes first (F193).** Do not spend a revision on the pipeline |
| **then** | **F10–F14 — the galley cluster** | F14 is THIRTEEN revisions inherited |
| **CEILED** | **F153; F168; F183 the traced pressing; F195 the rotation search; F44/F60/F62 gloss; F83; F67; F142; F148** | **F62 is DISPUTED — do not quote it without testing it** |
| **standing** | **F18 — the die-cut sticker** | The original deliverable. Open since rev 44 |

---
## §10 HOW TO GROW THIS HANDOFF WITHOUT BREAKING IT

1. **The set is three files.** `LEDGER_rev<N>.md`, `NEXT_CONTEXT_PROMPT_rev<N+1>.md`, and
   **`cp` of that file over `PASTE_INTO_CLAUDE_CODE.txt` IN THE SAME COMMIT.**
2. **`README.md` and `START_HERE.md` name the newest brief BY NUMBER.** Two rows check it.
3. **THE ROW COUNT IS SELF-REFERENTIAL AND AUTOMATED.** `python3 audit_brief.py
   --fix-count`. Write it LAST. *(It reads the CLEAN-TREE total. On a dirty tree
   `verify_clone.sh`'s own row expects `PASS+1`, which undercounts by the number of earlier
   failures — that is an artefact of the dirty tree, not a defect in the count.)*
4. **ADD ROWS ANCHORED ON ARITHMETIC OR BEHAVIOUR, NOT ON A GREP.**
5. **RUN BOTH AUDITS AS SCRIPTS AND RECORD WHAT THEY FOUND *IN* THE BRIEF.** **REPLACE the
   adversary's questions each revision** — a question that can no longer fail is not a control.
6. **NEVER DELETE A CARRIER.** §0, §0.1, §4, §5, §8 and §9 are carriers.
   **`EMBLEM_HANDOFF.md`, `PANEL_rev61.md` and `REMAINING_WORK_rev61.md` are carriers too.**
7. **RANK BEFORE YOU CHOOSE** — but **the owner outranks the ranking**.
8. **NEVER RELAX ONE COPY OF A CHECK.** Rev 64 re-based `probe_rev63_trace.py`'s T3 with the
   cause named and **four** companion rows, one of which is a kill that was watched firing.
9. **DO NOT LET THE MACHINE IDLE.** Run `bootstrap.sh`, launch the render, then read.
10. **ROOM TO GROW:** new findings go in `OPEN_FINDINGS.md` with an ID and a grade.
