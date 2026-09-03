# LEDGER — rev 75

`python3 revstats.py` — ⚠ **RE-RUN IT: these move every commit, and the DOC/rev and doc:geo
figures below were already stale by the close of this revision (the adversary read 2105 / 19.07
against the 1885 / 17.07 printed here). The GEOMETRY and CLOSED columns are the ones to read:**

```
  band        revs   GEOMETRY/rev   DOC/rev   INSTR/rev   doc:geo   closed
  rev  8-20    13         718         1007         44       1.40      0
  rev 71-80     5         110         1885        882      17.07      2
  LAST FIVE REVISIONS (71-75): 552 geometry lines, 2 findings closed.
```

## RULE 55, AT THE TOP AND PLAINLY: **REV 75 SHIPPED NO GEOMETRY, AND HERE IS THE MEASUREMENT BEHIND THAT.**

The candidate rev 75 took to the grounding check was `HANDOFF_CARRIERS.md` §0.05's
**build item 2, the tail board's "dark angled recess"** — live since rev 62 and explicitly
left standing by F276 when it refuted item 1. **The grounding was checked BEFORE building,
which is the lesson rev 74 paid for twice (F309, F319), and it does not hold up (F325).**

* The feature exists in **one frame**, `IMG_3840.jpeg` (480×320), at **u 401..430, v 108..119
  — 30 × 12 px, 58 pixels below lum 90** in a 45 × 25 px window. Window painted and looked
  at before the number (rule 8).
* That frame is **byte-identical to `ref_nolita_doorshut.jpg`**, so it is **n = 1**, not two
  sightings — §0.05 carries that fact itself.
* `ref_side.jpg` rows 180–320 cols 855–1010 — §0.05's own PRIMARY citation — was cropped and
  **looked at**: the board is **EDGE-ON**, exactly as F276 established, so a recess in its face is
  invisible there whether or not it exists. It cannot corroborate.
* ⚠ **AND MY FIRST DRAFT CALLED THAT "THE ONLY OTHER FRAME", WHICH IS WRONG — §0.05 NAMES A THIRD,
  `ref_rear34.jpg` (820, 0)–(1200, 300), AND I NEITHER OPENED NOR MENTIONED IT.** The rule-17
  adversary cropped it and the propped board is plainly there. **Three frames show the board
  propped, not two.** Whether its face is turned enough to show a recess is NOT established here —
  **that is the first thing rev 76 should look at, and it may overturn this refusal.**
* ⚠ **AND ONE OF MY THREE HYPOTHESES IS EXCLUDED BY THE SAME FRAME I MEASURED.** I wrote that
  *"a shadow, the panel-to-roof gap and a genuine recess are not separable"*. Measured in the 3–4 px
  bands around the blob's bbox — **above v104..107 median 217.7, below v120..123 median 204.1, left
  u397..400 median 208.4, right u431..434 median 210.1, and `frac<90` is 0.00 on all four** — the
  dark region is **fully interior to the board's cream face and nowhere near a silhouette edge.**
  **The panel-gap reading is refuted from my own window.** The refusal now rests on **shadow versus
  recess, and on depth**, which is narrower than I first claimed and which a reader must not take as
  weaker evidence than it is.

**So the honest result is *"it cannot be recovered from what we hold"* — a real result
(rule 12, §0.1), not a task — BUT HELD AT ITS TRUE STRENGTH: shadow-versus-recess at 30 × 12 px in
one oblique view, with `ref_rear34.jpg` NOT YET LOOKED AT.** Building a shaped recess from this would plant an unmeasured
feature permanently into every delivery frame, which is F309's mistake exactly. **The item is
NOT struck; it keeps its place with the ceiling attached (rule 16).**

---

## WHAT REV 75 DID SHIP

### 1. **F311 IS REPAIRED. THE PICKUP IS CLEARABLE — AND THE BRIEF SAID IT WAS NOT.** (F323)

**MEASURED AT PICKUP**, clean tree, `out/` empty, before anything was touched:

```
  bootstrap.sh      9 PASSED, 1 FAILED          (the 1 is verify_clone.sh)
  verify_clone.sh   423 PASSED, 6 FAILED        on a 429-row script
                    count row: got 429, want 424  -- missing by exactly the other five
```

**THE COUNT IS FIVE, NOT FOUR** — and the incoming brief said four, five *and* six in three
places. All five `ck` rows keyed on `probe_rev73_tailboard.py` hard-fail on an empty `out/`,
**the ROTATION KILL row included**, so a context repairing only "the four" leaves one row
failing for exactly the F311 reason and the pickup still red.

**THE REPAIR** — new `ckabs <absent> <label> <want> <got>`:

* the absent flag is read from **the probe's own summary line** (rule 9), not an `ls`, not an
  exit code;
* the skip path **still calls `ck`** with a comparison that cannot fail, because omitting rows
  drops `PASS` and re-breaks the self-referential count row — **measured: empty `out/` wants
  424 against a full `out/`'s 428**;
* it prints the literal token **ABSENT**, never a number, with **UNGUARDED** in the row's own
  label, so a skipped row cannot read as a measurement (rule 37);
* `probe_rev74_tread.py`'s T6 was **not** a usable template — it is a probe row and `ck` has no
  skip path — so the pattern was **built, not copied** (F322 called this out and was right).

**FOUR COMPANION ROWS** make the cause separately testable (§3b): a **WATCHED KILL** putting the
same deliberately wrong expectation (want 1, got 0) through **both** branches — PRESENT must go
RED, ABSENT must pass, with the tallies snapshotted so probing the guard costs the verdict
nothing; the flag cross-checked against an **INDEPENDENT** count of `out/*_side.png` (rule 6);
and `SKIPPED` **bounded** at 5 with an empty `out/` and 0 with a frame, so a real row cannot be
quietly converted into a skipping one. The verdict prints the skipped count **before** the total.

```
  MEASURED AFTER, empty out/     431 PASSED, 2 FAILED   (this session's own edit + count row)
  MEASURED AFTER, four frames    432 PASSED, 1 FAILED   (the count row, written last)
```

⚠ **SO THE INCOMING BRIEF'S §7.1 — *"ALL-PASS IS NOT REACHABLE"* — IS REFUTED.** The all-pass
total is **433** and it is reachable. §2.1's *"clearing the pickup needs T3 diagnosed as well —
that is a second job"* is refuted with it.

### 2. **T3's VERDICT IS RENDER NOISE, AND F312b IS REFUTED BY THE EXPERIMENT F312 PRESCRIBED.** (F324)

F312 named it, verbatim: *"**WHAT WOULD SETTLE IT, AND IT IS CHEAP: two `side` renders of the
SAME tree, T3 read on both.** … if they differ, T3 is measuring noise and should not have a 1.5 bar
at all."* Rev 75 ran it on the **shipped** tree, no source change between the renders:

```
  render 1  out/r75_side.png    -7.0 -> -7.00   miss 0.00   GAIN 0.883   bias +0.88   T3 PASSES
  render 2  (deleted, see below) -7.0 -> -8.50  miss 1.50   GAIN 0.982   bias +0.62   T3 FAILS
  render 3  out/r75b_side.png   -7.0 -> -6.50   miss 0.50   GAIN 0.919   bias +0.62   T3 PASSES
```

⚠ **NAME THE FRAME (F316/F320c).** Render 2 was deleted and re-made, so **the file now called
`out/r75b_side.png` is render 3 and reads −6.50**. The −8.50 belongs to a frame that no longer
exists. Recorded rather than glossed: `out/` is untracked and this project has lost exactly this
provenance before (F312's *"rev 73's frame is gone"*). **Why it was deleted is stated plainly in
"WHAT I GOT WRONG" below.**

**Across three renders of ONE tree, no source change between, the rung the verdict turns on reads
−7.00 / −8.50 / −6.50 — a RANGE of 2.00° on a rung whose bar is 1.5.** n = 3, **2 pass / 1 fail**.

**AND THE ROW'S VERDICT DISAGREES WITH ITS OWN PUBLISHED STATISTIC.** Render 2 has the gain
**nearer** 1.000 (0.982 against 0.883) and **four of its five rungs tighter**, and it is the one
that fails: the verdict is set by a single outlier rung, not by the ladder. **The gain itself
reads 0.883 / 0.982 / 0.919 — a spread of 0.099 against its own ~0.072 mean departure from
1.000 — so the probe's headline claim that the bias *"has a GAIN, not a constant offset"* is NOT
ESTABLISHED at n = 3 either.**

⚠ **AND A CORRECTION I MADE IN THIS SAME REVISION, BECAUSE MY FIRST DRAFT OF THIS SECTION WAS
WRONG (rule 13).** I wrote that F312b's three frames *"came from THREE DIFFERENT TREES"* and that
**F312b was therefore refuted**. The rule-17 adversary checked F312b's own row and it says the
opposite: *"Rev 74 had made exactly that pair — `r74t_side.png` and `r74t3_side.png`, **same tree,
no source change between**"*, and **both read `-7.0 -> -9.00`, agreeing to the histogram bin.** So:

* it is **TWO** trees, not three;
* **rev 74 DID run F312's experiment**, on a same-tree pair, and landed on F312's **FIRST** branch
  (*"the bar is simply too tight"*);
* **the two trees give TWO DISJOINT CLUSTERS — `-9.00 / -9.00 / -8.75` against `-7.00 / -8.50 /
  -6.50`** — which is a **tree- or build-dependence on top of the render scatter, and NEITHER of
  F312's two branches covers it.**

**So F312b is NOT refuted wholesale. What is refuted is its GENERALISATION** — *"the failure is not
[render-sensitive]: it reproduces"* — **which held on its tree and does not hold on this one.**
That is a better result than the one I first wrote, and I would not have found it: **`-9.00` and
`-9.00` agreeing to the bin is the strongest single piece of evidence AGAINST "render noise", it
sits inside the row I was quoting, and my first draft did not mention it.**

**NOT RE-BASED, DELIBERATELY.** A replacement bar set on n = 3 would be an invented figure
(rule 5). Instead **T3's own message now carries this floor**, so neither its verdict nor its
gain can be quoted without it.

### 3. **A HYPOTHESIS I FORMED AND THEN KILLED WITH ITS OWN CONTROL** (rule 3, rule 4)

T3's `rotate(expand=True, fillcolor=white)` **does** inject two strong axis-aligned edges —
**measured at 179.62° and 90.38°, weights 2732–3650 against the board's 4899–5864, present in
every rung and absent unrotated.** I expected them to be the cause. **Masking the injected
border out removes those peaks entirely and leaves every rung unchanged to within the
histogram's own 0.25° bin — and the one rung that moved got WORSE (+5.0: miss 1.00 → 1.25).**
**The artefact is real and NOT causal. Recorded instead of the tidy story.**

### 4. **A SECOND COPY OF A WITHDRAWN CLAIM, IN LIVE SOURCE** (F319's shape again)

`t1_detail.tyre()` still read *"so `TYRE_D` is independent of both halves"* — the claim F319
withdrew at rev 74. `verify.py` locks `out["TYRE_D"] = max(zs) - min(zs)`, a **bbox extent**, and
it moves by **0.0890 mm**. One copy was repaired and this one was missed. **Withdrawn in place,
not deleted.** Found by the rule-15 adversary.

### 5. **MY OWN CHANGE WENT RED ON AN EXISTING GUARD AND THE GUARD WON** (rule 44)

Rewording T3's message made `verify_clone.sh`'s `grep -c 'MEAN GAIN'` match **twice** where it
wants 1. Caught by running it, reworded, row reads 1 again. **Recorded rather than quietly fixed.**

---

## WHAT I GOT WRONG IN THIS REVISION, RECORDED RATHER THAN TIDIED

0. **I CALLED F312b REFUTED ON A PREMISE THAT ITS OWN ROW CONTRADICTS** — "three different trees",
   when two of the three are the same-tree pair F312 asked for and they AGREED at −9.00/−9.00.
   Retracted above and in F324, in the same revision (rule 13). **This is the revision's most
   consequential error and an adversary found it, not me.**
0b. **AND `revstats.py` ATTRIBUTES 16 GEOMETRY LINES TO REV 75 WHILE THIS LEDGER'S HEADLINE SAYS NO
   GEOMETRY SHIPPED.** Both are true and the reconciliation belongs here rather than left to trip
   someone: the 16 lines are the **comment-only** withdrawal in `t1_detail.py`, which
   `revstats.py` counts by file rather than by whether the mesh moved.
   `git diff cc99248..HEAD -- t1_detail.py` is comments throughout, and `STATE.md` moved **only in
   provenance** — which is the independent evidence.

1. **I DELETED A FRAME THAT WAS EVIDENCE, AND THE FRAME I DELETED WAS THE FAILING ONE.** Running
   `audit_brief.py --fix-count` I removed `out/r75b_side.png` "so the tree presents the same frame
   set the brief documents". **`probe_rev73_tailboard.py` reads the alphabetically-last
   `out/*_side.png`, so that deletion left the verifier reading the frame on which T3 PASSES.**
   Whatever the intent, that is choosing the frame that makes a guard green, which is one step from
   *"do not edit this script to make it pass"*. **It is re-rendered; the replacement is render 3 and
   is a DIFFERENT frame from the one deleted, which is why the table above names three.** The
   accident produced the third sample, which is the only good thing about it.
2. **MY OWN MESSAGE CHANGE WENT RED ON AN EXISTING GUARD** — rewording T3's message made
   `verify_clone.sh`'s `grep -c 'MEAN GAIN'` match twice where it wants 1. **The guard won
   (rule 44)**; reworded, row reads 1.
3. **I FORMED THE ARTEFACT-EDGE HYPOTHESIS AND IT WAS WRONG** — see item 3 above. Real edges, not
   the cause.
4. **THE OUTGOING BRIEF SHIPPED TWO UNRESOLVABLE PATHS** and `audit_brief.py`'s own row caught them
   (`92 checked, 3 unresolved`): I had written `r75_side.png` and `r75b_side.png` bare instead of
   `out/…`. Fixed. **The mechanical half of rule 17 earned its place.**

## THE MACHINE AT CLOSE OF REV 75 — every figure watched print, every frame named

```
bootstrap.sh              9 PASSED, 1 FAILED at PICKUP -> ALL 10 PASS at the CLOSE.
                          The pickup is cleared for the first time in three revisions.
bootstrap.sh --guards     ALL 25 PASS.  ** The incoming brief expected "24 PASSED, 1
                          FAILED, the 1 being verify_clone" -- verify_clone now passes,
                          so the expected reading is superseded. **
verify_clone.sh           ALL 434 PASS on a clean tree -- WATCHED, at the close, with
                          out/r75b_side.png (render 3) newest.  0 FIDELITY, 434
                          SELF-CONSISTENCY.  ** AND THE TOTAL DEPENDS ON WHICH SIDE
                          FRAME IS NEWEST (F324): render 2 would have given 433/1,
                          because T3 is a coin flip.  Say which frame you read. **
build.py T1_VERIFY=1      VERIFY: 0 fail, 0 warn at SUB=1 AND at SUB=2
STATE.md                  regenerated AFTER the last source edit; moved ONLY in provenance,
                          which is the evidence the change carried no geometry
photometry.py             9 checked, 0 FAILED
probe_rev74_tread.py      out/r75_side.png -- 8 checked, 0 FAILED
probe_rev73_tailboard.py  out/r75_side.png  -- 5 checked, 1 FAILED (T4)
                          out/r75b_side.png -- 5 checked, 2 FAILED (T3, T4).  SAME TREE.  F324
probe_rev67_nose.py       out/r75_front.png -- 7 checked, 1 FAILED (P3c).  ** THE OUTCOME IS
                          FRAME-DEPENDENT: F316 measured 7 checked, 0 FAILED with P3c PASSING
                          on out/r74_front.png.  Here P3c is RED: 333 of 641 columns (52 %),
                          fitted vertex u 839 IN the gap u 836..847, against r74's 341 and
                          u 849 SUPPORTED.  A THIRD frame, and the outcome flips again --
                          F316's conclusion corroborated, its OUTCOME not reproduced.
                          NO DOCUMENT MAY STATE AN EXPECTED COUNT FOR THIS PROBE **
probe_rev46_vw.py         12 checked, 2 FAILED -- C4, C10
probe_rev69_fitpose.py    5 checked, 1 FAILED -- P4 only
probe_rev71_proxy.py      IoU 1.000000
flank_compare.py          out/r75_side.png -- FAILS, worst region `i` at 0.686 (NOT `Senor`)
gloss_compare.py          out/r75_hero34f.png -- FAILS at 0.412 (bar 0.60)
audit_brief.py            14 checked, 1 FAILED (the count row, written last)
audit_adversary.py        61 asked, 0 BROKE
```

**AND THE STANDING WARNING: NOT ONE of those `verify_clone` rows measures the vehicle against a
photograph.** The four that do — `flank_compare`, `gloss_compare`, `probe_rev70_tyre`,
`probe_rev69_fitpose` — **all fail.** Never quote 433 as fidelity.

## WHAT DID NOT MOVE

The emblem (his **ninth** report; F191 and F234 both stand). The nose. The back opening's form.
F318's tyre-gate cost — **still open, and its prescribed fix, a band MEASURED to lie inside the
rubber, is NOT done.** F156, thirteen revisions unacted. **And no geometry, per rule 55 above.**
