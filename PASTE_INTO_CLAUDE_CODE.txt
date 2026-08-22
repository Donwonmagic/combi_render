# NEXT CONTEXT PROMPT — rev 54

**Read this whole file before you touch anything.** Then `CLAUDE.md` (method only, loads every
session), then `LEDGER_rev53.md` — which is where every number below comes from — then
`SURVEY_rev49_photoreal.md` §6, still the work list.

---

## §1. START HERE — MEASURE THE BRANCH, DO NOT TRANSCRIBE IT

```bash
cd /home/user/combi_render
git fetch --unshallow 2>/dev/null || true
git fetch --all --prune
for b in $(git branch -r | grep -v HEAD); do
  printf "%-52s ahead %-3s behind %s\n" "$b" \
    "$(git rev-list --count origin/main..$b)" "$(git rev-list --count $b..origin/main)"
done
git diff --name-only HEAD...origin/main        # <- HIS PHOTOGRAPHS ARRIVE HERE
./bootstrap.sh          # ALL 10 PASS  -- THE BRANCH CHECK IS ROW 9
./verify_clone.sh       # ALL 162 PASS -- and read what its verdict block says
```

**THE DESIGNATED BRANCH'S REMOTE COPY WAS DELETED AGAIN AT REV 53** — `fetch --prune` printed
`- [deleted] (none) -> origin/claude/youthful-hamilton-yqrzs5`, the **third revision running**
(rev 51, rev 52, rev 53). HEAD measured **0 ahead / 0 behind** `origin/main`, every remote branch
measured **0 ahead**, and rev 52's work had landed in `main` through **PR #9**. MEASURED at pickup,
not transcribed. **Expect this shape a fourth time and measure it.**

> **ROW 9, NOT ROW 10** — confirmed again at rev 53 by reading the machine's own output:
> row 8 clone depth, **row 9 "no branch carries work HEAD does not have"**, row 10 `verify_clone.sh`.

**Re-measure before you finish, too.** `origin/main` moved mid-revision at rev 51.

---

## §2. WHAT REV 53 DID

### §2.1 A6 IS CLOSED BY AN OWNER RULING, AND THE MEASUREMENT THAT GOT THERE IS THE POINT

Brief §4 item 2 asked for one number — **how big a chip is in a photograph**. The answer is that
**there are no chips to size**, and the detection floor shows that is *not* a resolution artefact.

**THE INSTRUMENT IS NOT REV 52'S.** The render is **271.2 px/m** and `ref_side.jpg` is **211.5**, so
a fixed 9 px local-median radius is a **different physical size in each** — rev 52's raw
4.07 % vs 0.00 % comparison mismatched them. Every render is now put **through the photograph's own
optics** (blurred to the measured PSF sigma **0.735 px**, decimated to **4.728 mm/px**, given the
frame's own **0.99 DN** noise) before the same estimator reads it. Calibrated on `LEDGER_rev52`
§6.1's own two controls first: **0.000 %** on flat cream + noise, **7.329 %** against a true 7.33 %.

| | own px/m | through the frame's optics |
|---|---|---|
| Pointiness (was the default) | 8.826 % | **2.589 %** |
| edge signal, GAPW/2 = 2.75 mm | 0.000 % | **0.000 %** |
| edge signal, `T1_EDGERAD=12` | 0.000 % | **0.000 %** |
| **the SHIPPED build** | 0.000 % | **0.000 %** |
| `ref_side.jpg` **photograph** | — | **0.165 %** |

**AND AS A PROFILE** — dark coverage in 6 mm bands measured **up from the fascia's bottom fold**,
which is what a wear band actually *is*:

| | 0–6 | 6–12 | 12–18 | 18–24 | 24–30 | 30–36 | 36–42 mm |
|---|---|---|---|---|---|---|---|
| **photograph** | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| Pointiness | 6.12 | 1.22 | 4.12 | 7.68 | 11.02 | 11.92 | **14.03** |

**The old default's wear was HEAVIEST FARTHEST FROM THE FOLD** — it put the most wear where a real
edge chip cannot be. A single coverage number never showed that; the profile does.

**HE RULED**, on `probe_scratch/rev53_owner_fascia.png` (photograph / as-built / re-based, **all
three at the same 4.728 mm/px**, coverages beside them): ***"Follow the photograph — clean cream."***
So the **ray-traced edge signal is the DEFAULT now**, `T1_PTWEAR=1` restores Pointiness, and
`SPEC` §3's WEATHERED lock is **narrowed to the red and the running gear**.
**The change is CREAM-ONLY** — a red flank window reads **0.527 % → 0.537 %**, unmoved.

### §2.2 REFUTED AT REV 53 — DO NOT REBUILD THESE

* **"the Bevel gate looks empty because GAPW/2 = 0.75 px is SUB-PIXEL."** Rev 52's explanation,
  **REFUTED**: `T1_EDGERAD=12` is **3.25 px**, well above a pixel, and the fascia is **unchanged at
  0.000 %**. The retraction is in `t1_mats.py` (grep `IS RETRACTED HERE`) and guarded.
* **"the fascia's bottom edge is a butt joint between objects."** My own hypothesis, **REFUTED by
  the mesh**: `counter` is a **closed mesh with 0 boundary edges**.
* **"the gate is inert."** No — the 2.75 mm vs 12 mm difference image lights up **every window
  frame, shut line, arch lip and gutter and nothing between them** (53 004 px differ by >6 DN).
* **"ONLY THE WORST-REGION NUMBER IS ROBUST"** (rev 52) and everything rev 50/51 refuted — all still
  refuted. The cap's dome depth; the m5 "convention conflict"; the wear field does not clone;
  `LID_W ≤ 1.2797 m`; A7's aft wall; `gal_end_f` widened to `REAR_W/2`.
* **§2b of the rev-52 brief — HIS SETTLED RULINGS — IS UNCHANGED AND STILL BINDING.** W6 (keep the
  studio rig; **a G/R shortfall on any surface is NOT a paint error**); the roof strips' 0.3 m
  retired; the wipers withdrawn entire, commented not deleted; the lower bay SHUT; the RED bus is
  the target and **paint and artwork do not transfer between vehicles**; the tail board IS on the
  vehicle; the marks above the burst are STARS. **Do not re-open or re-ask any of them.**
  `playa_env.py` is not on the table.

### §2.3 THIS FILE WAS AUDITED AGAINST THE MACHINE, AND THE AUDIT FOUND FOUR THINGS

Rule 17. Every file cited below was opened, every quoted string grepped, every figure recomputed
against `probe_rev53_chip.py`'s own printout and against the source. **What it found:**

| what the draft said | what the machine says |
|---|---|
| `verify_clone.sh` **ALL 151 PASS** (carried from rev 53's own §1) | **159** — this revision added nine rows and re-based one |
| the edge-signal rows read **0.913 % / 1.094 %** through the optics | **0.000 % / 0.000 %** — those were from a run BEFORE the bracket-column fix, i.e. the exact transcribe-an-old-run defect §1 warns about |
| the brief named `T1_EDGEBEVEL` in its ablation list | **that switch no longer exists** — it became the default and was replaced by `T1_PTWEAR`. The `every T1_ switch the brief names exists` row would have failed |
| "the detection floor is 6 mm" stated flat | **6 mm at 5 % coverage AND ≥30 DN depth.** At −20 DN a 6 mm chip is invisible. The ceiling is not optional |
| `LID_X1 = -1.0700` cited as a greppable string | **it is not one** — the source line is `LID_X0, LID_X1 = 0.9640, -1.0700`. Rule 18's exact defect, inherited from the rev-53 brief and corrected here |
| *"`T1_EDGEBEVEL` is GONE"* | gone from the **shader**; it survives in one `probe_rev53_chip.py` comment as history — and that mention is what keeps the ablation-sweep row green while this brief names it |
| `T1_EDGERAD=12` is **3.3 px** | **3.25 px** (12 × 271.2 / 1000), recomputed |
| `verify_clone.sh` **ALL 159 PASS** | **160.** Caught only by running it on a CLEAN tree at the very end — before the commit the clean-tree row itself fails, so the banner reads "159 PASSED, 1 FAILED" and 159 is the number that gets transcribed. **Run it clean before you quote its total.** `LEDGER_rev53` §7 carried the same 159 and is corrected too |

| the brief said nothing about `PASTE_INTO_CLAUDE_CODE.txt` | **it was a byte-identical copy of the rev-52 brief** — see §2.4. The most important intake door in the repo, and the audit found it only by asking what `CLAUDE.md` actually imports |

**All nine are corrected above.** Five of the nine were **transcription**, not measurement, in a
document whose own §1 says not to transcribe.

**VERIFIED CLEAN BY THE SAME AUDIT** — recomputed or grepped, not re-read: all 22 cited files exist;
`CAP_EMBLEM_WFRAC = 0.2087` is in `t1_detail.py`; `T1_PTWEAR` and `T1_EDGERAD` are real levers in
`t1_mats.py`; **`BAYS[2]`'s aft edge recomputes to exactly −0.855750 and the sixth hook to 51.25 mm
beyond it**; `X_TAIL = -1.8727` against `LID_X1 = -1.0700` gives **802.7 mm**, so the 803 stands;
1000/211.5 = **4.728 mm/px**; 2.589/0.165 = **15.7x**; `STATE.md`'s zero-area row is present; and
**PR #9** is confirmed in the log.

### §2.4 THE INTAKE DOOR THAT AUTO-LOADS WAS TWO REVISIONS STALE, AND NOTHING GUARDED IT

`CLAUDE.md`'s Imports carry **`@PASTE_INTO_CLAUDE_CODE.txt`**, so that file is pulled into **every
session** as *"this revision's entry procedure"*. Measured at the end of rev 53: it was a
**byte-identical copy of the rev-52 brief**.

It was updated every revision from rev 47 through rev 51 and **rev 52 dropped it** — so rev 53 opened
with the rev-52 brief auto-loaded while the real brief was rev 53, and nothing said so. Rev 52
guarded `README` and `START_HERE`, **the two intake doors a human has to choose to open, and missed
the one that opens itself.**

**Now guarded by two rows**, both watched failing — on the previous brief left in place (rev 52's
actual defect) and on a **one-character drift**: `the IMPORTED entry procedure IS the newest brief`
and `CLAUDE.md still imports that entry procedure`. **It must stay byte-identical to the newest
brief**, so there is no second source of truth free to diverge — the same reason the rev-52 brief
§10 rejected a separate `RULES_CANON.md`.

**SO: WHEN YOU WRITE THE REV-55 BRIEF, `cp` IT OVER `PASTE_INTO_CLAUDE_CODE.txt` IN THE SAME COMMIT,
OR `verify_clone.sh` FAILS AND NAMES THE ROW.**

---

## §3. THE WORK LIST FOR REV 54

**Item 1 is blocked on a photograph. Items 2–4 are not.**

**1. THE TWO VW BADGES — HIS REPORT AT REV 51, STILL THE TOP JOB, STILL BLOCKED.**
Untouched at rev 52 and rev 53. **PROVENANCE, GRADED: every figure in this item is INHERITED from
rev 51 / rev 15 and has NOT been re-measured since.** The DIAMETER route on `ref_side.jpg` is
**EXHAUSTED** (0.3474 vs the built 0.3170 — 9.6 % small but only **1.8 sigma**). **The untouched
constant is the STROKE WEIGHT**, `CAP_EMBLEM_WFRAC = 0.2087` **in `t1_detail.py`**, whose own comment
says it kept its w/R from the rev-14 emblem that rev 15 found at 7.0 sigma and resized. **No frame
has ever been compared against it.** Full text and the four closed routes in
**`PHOTOS_WANTED_rev52.md` item 7**.
**AND THE GUARD GAP ON THIS PART IS STILL TOTAL** — after three revisions of adding rows, **still not
one row anywhere names a wheel, hub, cap, rim or vent.** Verified again at rev 53: the only
apparent hit is "vent" inside "in**vent**ed".

**2. WHY DOES THE COUNTER FASCIA'S OWN BOTTOM FOLD PRODUCE NO EDGE SIGNAL?**
Rev 53 left this open **and it is the one thing that would let the radius be grounded at all**.
Sub-pixel is refuted, a butt joint is refuted, and the lever is proven live on every *other* edge.
The next step is cheap and is **not another guess**: render the `EDGE` value itself as an emission
AOV and look at where it is non-zero. If it is zero at that fold the geometry is the cause; if it is
non-zero then `cm * clm` and `W_CHIP_CUT` are starving it. **One render answers it.**

**3. FINISH A9. Two of its four parts are done; the galley is still ~103 mm too far aft.**
**PROVENANCE, GRADED: the per-feature deltas are INHERITED from the rev-52 brief and have NOT been
re-measured at rev 52 or rev 53.** The offset is **NOT rigid** (−0.09574 at hook u=0.13 to −0.11035
at `gal_appliance` u=0.80, so one additive constant leaves ±7.3 mm). Re-derive each X from `BAYS`,
the way `gal_rail` now is. *(The survey's ~106 mm and its +0.096..+0.113 range are both wrong.)*

**4. THE THREE HOLES REV 52 LEFT OPEN, all cheap to reach.**
**PROVENANCE, GRADED: the 260.0 mm and 20.0 mm sight lines are rev 52's and were NOT re-measured at
rev 53.** The other two figures in this item WERE recomputed at rev 53's audit and reproduce exactly
(see §2.3).
* `gal_end_f` sees past by **260.0 mm** on the show side and 20.0 mm on the off side. Needs its own
  sight line established first — **do not inherit `REAR_W/2`** (rule 34: that figure belongs to the
  rear window, which is not what looks at it).
* The **sixth hook at X −0.907 lies 51.25 mm beyond `BAYS[2]`'s own aft edge (−0.855750)**. The six
  hook stations are typed literals with irregular spacing whose span centre is **−0.705** against the
  rail's measured **−0.598**. **They disagree and one of them is wrong.**
* A7's real defect: `roof_cutters()`'s aft edge is `LID_X1`, which is **not** greppable as `LID_X1 = -1.0700` — the source line is `LID_X0, LID_X1 = 0.9640, -1.0700` in `t1_shell.py`, so **803 mm of roofed body**
  sits between the last light inlet and the tail skin. Unbuilt. A7 is **ILLUMINATION, not dressing**.

**5. A13 / A16 / A12** — the isolated star built BELOW the burst where both red frames put it above;
every flank rosette drawn at the diameter of its **gold core**; *A12 is an OWNER RULING, not a
do-now* — `senor_trace.py` calls the remedy *"inventing ink the photograph does not show"*.

**6. A11's SECTION, A14** — a chrome lever lying in a dish **pressed into** the skin against a 12 mm
**proud** prism; the `lid_rail` WIDTH (§3.1).

**A CHEAP UNBLOCKED ITEM, STILL NOT DONE AFTER TWO REVISIONS:** `SPEC` §8's colour locks are all
graded **M** = *"measured by me from `ref_source.jpeg`"* — a 246×197 thumbnail the record itself
calls retired. They can be re-derived on `ref_playa_34.png` at **4× the area** with no new
photograph. **Report the re-derived values; do not change the constants without his ruling** — W6
makes colour his call.

**THE PROCESS ROWS, still open:** the **open-findings** register abandoned at rev 45 (21 rows); the
standing-instructions carrier deleted at rev 44, which took the **die-cut sticker — the project's
original deliverable** — with it, **still open**; SPEC §0.2's two rev-4 corrections later refuted;
rev 48's refuted *"B stays open"* still live in `build.py` and, **split across two lines so a flat
grep misses it**, in `t1_shell.py`; the tail board still has **zero rows in either verifier**.
**AND `cream_rms.py` IS STILL A DORMANT RENDER-VS-PHOTOGRAPH GATE with zero rows in either
acceptance script. It was NOT run at rev 52 and NOT run at rev 53.** **`flank_compare.py` WAS re-run at rev 53**, on the
shipped render, and **still fails 2 of 4** — read its own summary line, not its exit code:
`ink area ratio 0.9417 PASS`, `ink aspect 2.3689 FAIL`, `IoU 0.7608 PASS`,
`worst region 0.471 (Senor) FAIL`. **`Senor` is 0.471 now, not the 0.479 rev 52 measured** — the
same instrument on a different render, so do not read the drop as a regression in the artwork.

### §3.1 `lid_rail` — STILL MEASURED AT ZERO AREA, STILL GUARDED, STILL DELIBERATE

Both objects are **0.000000000 m² with 18 of 18 faces degenerate**. `STATE.md`'s zero-area sweep
still reports *"2 of 223 meshes have zero area; 2 exempt and KNOWN OPEN"*. **It is exempt in
`verify.py`, not fixed, because the rail's WIDTH is measured NOWHERE.** The exemption is two-sided
and cannot outlive the defect. **This is an owner question.**

### §3.2 THE HABIT THAT PAID AT REV 53, NINE TIMES

**PAINT THE WINDOW AND LOOK AT IT BEFORE IT PRODUCES A NUMBER.** Rev 53 caught **seven of its own
windows or masks** this way — the **MENU CARD** (read **12.014 %**: printed text counted as chips),
the bulb-string shadow, the window chrome, the tail/wall highlight, the white wall behind the
bumper, and a **trap check whose own box covered the LEFT wall only** — *a trap check is a window
too*. It also caught a bracket filter with its **SIGN BACKWARDS** (a bracket is cream, so the red
detector finds red BELOW it and the column comes out **TALLER**, not shorter — rule 35's shape), and
found that excluding the bracket columns was not enough because the survivors sat on the bracket
**SHOULDERS**, in the columns beside an excluded one.

**AND A NULL CONTROL CAUGHT THE WORST ONE.** The detection floor first used the window's raw
high-pass **STD** (8.57 DN, outlier-driven) instead of its **MAD** (0.99). The null then read
**8.117 % on PURE NOISE** — every "detection" in that pass was noise. **Give every threshold
statistic a null control at the real noise, or it will report noise as signal.**

**AND TWO OF REV 53'S OWN GUARDS DID NOT FIRE WHEN FIRST WATCHED.** One was anchored on a line that
appears in **both branches** of an if/else, so swapping the branches left it passing — while its own
comment claimed it caught exactly that. The other was anchored on `Follow the$`, which matched a line
that merely **WRAPPED** there. **A guard anchored on where a sentence happens to wrap tests nothing.**
Both were caught only by watching them fail, which is why rule 3 exists.

---

## §4. WHAT ONLY HE CAN GIVE

**`PHOTOS_WANTED_rev52.md` is the carrier for item 7 (ONE HUBCAP, SQUARE ON AND CLOSE)**. Items
**1–5** keep their full text in `PHOTOS_WANTED_rev49.md`: the tail board's footing; the decal darker;
the nose square on; a raking-light frame of the louvres (**ONE item — the pressing depth**; the
"block length, station and V swage" expansion is a proposal, not the record); the off side, any
frame. **He has said 1–5 are not possible now. DO NOT RE-ASK THEM.** Item 6 (an obliquely-seen wheel)
was **DISSOLVED at rev 51** — struck, not outstanding.

**NEW AT REV 53, and it has no carrier outside this brief yet:** a frame showing the cream **where it
IS chipped** — any close frame of a worn edge — would let the Bevel radius be grounded on a real wear
band instead of on nothing. It is **not** urgent now that he has ruled "clean cream", but it is the
only thing that would reopen §3 item 2's other half.

---

## §5. THE RULES — `CLAUDE.md` CARRIES THE METHOD, NOT THE NUMBERED CANON

The canon (rules 1–33) is printed in `NEXT_CONTEXT_PROMPT_rev50.md` §11. **Rules 34 and 35 live only
in the rev-51/52/53 briefs and `LEDGER_rev50.md` §0, so they are carried here too — that is
`CLAUDE.md`'s own rule 16 firing on this file:**

> **34. A REQUIREMENT INHERITS ITS OBJECT EXACTLY AS A RETIREMENT DOES.** Before relying on any
> *"the record requires X"*, check which object the sentence is about — and check the cited line
> exists. **Rev 52 applied this deliberately**: `gal_end_f` was left alone because `REAR_W/2` belongs
> to the rear window, which is not what looks at it.

> **35. A GUARD WRITTEN AGAINST A POSE ENCODES THAT POSE.** Guards that identify a part's foot or
> free edge by `min(y)` are only right while the part leans one way. Ask the geometry.
> **Rev 53 broke this and was caught by it**: a filter assumed a bracket would make a column
> *shorter*; the machine says a cream bracket makes it *taller*.

> **Rule 29.3:** no finding is attributed to a cause until a control separates it. **Rule 29:** a
> retirement inherits the object it was made about. **Rule 15:** a retraction that lands in a ledger
> and not in the source is half a retraction — **rev 53's retraction of rev 52's sub-pixel claim is
> in `t1_mats.py`, not only in `LEDGER_rev53.md`, and a row holds it there.**

---

## §6. THIS MACHINE

```
cores 4   RAM 15 GB   Blender 4.5.3 via pip install bpy   subagent concurrency 2
build  T1_SUB=1 ~19 s     render 1600x1100 96 spp ~4-7 min PER VIEW
```

```bash
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
T1_PREVIEW=side T1_PFX=r54 T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
  /tmp/blender/blender -b -P build.py
T1_PREVIEW=hero34r ...                                       # the REAR 3/4 -- A7 lives here
T1_SUB=2 /tmp/blender/blender -b -P audit.py                 # rewrites STATE.md -- COMMIT FIRST
python3 lid_gen.py                                           # regenerates tex/lidmural.png
python3 flank_compare.py out/r54_side.png /tmp/fc.png        # THE FIDELITY GATE.  Exits 1 today.
python3 probe_rev53_chip.py                                  # the chip measurement, all six arms
```

**`out/` IS NOT TRACKED and starts empty. Render before quoting any probe that reads a frame.**
**A backgrounded runner's exit code is the WRAPPER'S, not Blender's — grep the log for `Saved:`.**

**ABLATIONS — every one exists to WATCH A GUARD FAIL.** New at rev 53: **`T1_PTWEAR=1`** (restores
the Pointiness chip gate and moves nothing else — **rev 52 claimed this switch existed; it did not,
and rev 53 built it**) and **`T1_EDGERAD`** (the Bevel radius in **millimetres**; unset keeps the
derived `GAPW/2`). Carried from before: `T1_TARNCONTAM=1`, `T1_RAILSTALE=1`, `T1_ENDSHORT=1`,
`T1_CAPSINK=1`, `T1_LIDDEG=104`, `T1_BAYSTALE=1`, `T1_LAMPSINK=1`, `T1_LIDASPECT=1.2`,
`T1_HANDLEHI=1`, `T1_BAREMAT=1`, `T1_TBFOOT=1`, `T1_BAYPROUD=1`.
*`T1_EDGEBEVEL` is **gone from the shader** — it became the default at rev 53. Do not cite it as a
lever. It survives on purpose in one comment in `probe_rev53_chip.py`, recording that r53base /
r53bev / r53bev12 were rendered before the ruling; that mention is also what keeps the
`every T1_ switch the brief names exists` row satisfied while this brief still names it.*

---

## §7. THE STANDARD, IN HIS WORDS

We are recreating a photorealistic version of **that exact bus**, and **any single measurement off is
unacceptable** — per-measurement, not on average. A model right in ninety places and wrong in one is
not 99 % done, because he will look straight at the one.

`bus_model_ref.JPG` is a **SCHOOL BUS** and is **NOT the vehicle** — a FIDELITY BAR only. Use
`ref_workshop.jpg` the same way, and remember it has **no headlamps and no hubcaps fitted**.

**Ground in the reference, build, adversarially audit, iterate.** Never build before grounding. Never
call it done off self-review. Report the measurement **with its ceiling**, never a self-assigned
score. Do not say anything is ready — say what is fixed, what is still wrong, and what you measured.

**RENDER IT, CROP IT, AND LOOK AT IT, before and after every change.** Every defect this project has
shipped passed `VERIFY: 0 fail, 0 warn` and was found by looking at a crop.

**When you need something from him, ask as MULTIPLE CHOICE with the reference material attached — one
crop, one mark, one sentence — and ASK IT WITH THE QUESTION TOOL.** He has never stood in the bus: do
not ask what the real vehicle looks like, ask what a PHOTOGRAPH shows. **Rev 53's whole A6 result
turned on one such question, and the crop had all three states at the same mm/px so he could compare
them by eye.**

**`git rev-list --count origin/main..HEAD` before you start and again before you finish. And
`git diff --name-only HEAD...origin/main` — that is where his photographs arrive. EVERY session.**
