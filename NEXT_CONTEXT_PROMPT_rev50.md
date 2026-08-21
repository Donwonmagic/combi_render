# NEXT CONTEXT PROMPT — rev 50

**Read this whole file before you touch anything.** Everything you need to start is here; everything
you need to be *correct* is in `SPEC.md` (§10.123 is this revision's), `LEDGER_rev49.md`, and
`LEDGER_rev48.md`.

---

## §0. WHAT HE SAID, AND WHAT IS LEFT

| his words | state |
|---|---|
| "100% calidad off center" | **FIXED** rev 46, guarded, guard watched fail. |
| "the vw logo wrong" | **FIXED** rev 46. |
| "señor Tacombi still isn't clearer" | **BLUR FIXED** rev 47. **CONTRAST HALF STILL OPEN.** §5 |
| "It still does not read as two separate words" | **FIXED rev 47b**, magnitude RETRACTED rev 48. Blocked on §7 item 2. |
| "the nose of the car is too flat" | **CONFIRMED, NOT FIXED, SIX REVISIONS.** Still no photographed anchor. §6 |
| "we're going to need the trunk open like it's in service" | **SUPERSEDED BY HIS OWN RULING.** See below. |
| "the main bay that should be open is the upper one" | **REV 48 OVER-READ THIS.** §2 |
| **NEW rev 49** — *"Leave the lower bay shut, just have the back trunk window open for service"* | **RULING. BUILT.** §2 |
| **NEW rev 49** — *"That was referring to a different sign. This one is part of the vehicle."* | **RULING. THE TAIL BOARD IS BUILT.** §3 |
| **NEW rev 49** — W6: chose *"re-light to match your photographs"* | **ANSWERED — then the mechanism turned out not to exist as described. RE-ASK.** §5 |
| **NEW rev 49** — photographs: *"Neither is possible right now"* | **RECORDED. STOP ASKING.** §7 |

> **RULE 29 — NEW, rev 49. A RETIREMENT INHERITS THE OBJECT IT WAS MADE ABOUT, NOT THE STATION IT WAS
> SEEN AT.** `signboard()` was retired from a crop of the **"La Santa"** sign standing on the GROUND
> BEHIND the bus. Four revisions read that as *"the raised panel at the tail is retired"* and applied
> it to a **different object at the same station**. Rev 49 REFUSED a job on the strength of it, and
> **the owner had to correct it.**

> **RULE 30 — NEW, rev 49. A FIXTURE'S FOOT MUST BE CLEAR OF THE BODY IT STANDS ON, AND SOMETHING
> MUST CHECK IT.** Nothing did. The tail board's foot sat **120 mm inside the roof**; the trunk bay's
> lining sat **2.0 mm proud of the tail skin**. Both through `VERIFY: 0 fail, 0 warn`.

---

## §1. START HERE — AND DO NOT TRANSCRIBE A BRANCH NAME OR AN AHEAD-COUNT

```bash
cd /home/user/combi_render
./bootstrap.sh            # ALL 10 PASS
./verify_clone.sh         # ALL 113 PASS   <- 113, not 110.  Four rows added at rev 49.
```

### THE BRANCH INSTRUCTION HAS NOW BEEN STALE **FOUR** REVISIONS RUNNING

Rev 47's brief named a branch with an ahead-count of 5; the real count was 1. Rev 48's named one that
was **0 ahead / 1 behind**. Rev 49's designated branch was created at `origin/main` — **0 ahead** —
while the real work sat 15 ahead on another ref. **Working where rev 49 was placed would have
discarded the whole of rev 48.**

**So this file does not name a branch. It names a MEASUREMENT.**

```bash
git fetch --all --prune
git fetch --unshallow 2>/dev/null || true      # verify_clone fails on a shallow clone
for b in $(git branch -r | grep -v HEAD); do
  printf "%-52s ahead %-3s behind %s\n" "$b" \
    "$(git rev-list --count origin/main..$b)" "$(git rev-list --count $b..origin/main)"
done
git diff --name-only HEAD...origin/main        # <- HIS PHOTOGRAPHS ARRIVE HERE
```

**Work from whichever ref that measurement shows is furthest ahead of `main` with nothing behind it.**
At the time of writing that is `claude/combi-render-rev49-sq1pvc` — **but check, do not believe this
sentence.**

**AND THE MACHINE ALREADY CATCHES THIS.** `bootstrap.sh`'s row 10 reads *"no branch carries work HEAD
does not have"*. It fired correctly at rev 49 and confirmed the correction independently. **If that
row is green you are on the right ref; if it is red, believe it over any prose including this file.**

**If your HEAD is an ANCESTOR of the furthest-ahead ref, fast-forward — nothing is lost and nothing is
merged.** Rev 49 verified that with `git merge-base --is-ancestor` before moving.

---

## §2. WHAT REV 49 BUILT AND WHAT HIS RULINGS CHANGED

### 2a. THE LOWER BAY IS SHUT. ONLY THE REAR WINDOW IS OPEN.

> *"Leave the lower bay shut, just have the back trunk window open for service."*

**This refutes an INFERENCE rev 48 made and shipped.** Rev 48 asked him which of the two rear
apertures should be open and he chose **A, the rear window**. Rev 48 then reasoned *"he called the
upper one the MAIN bay, not the ONLY one"* and kept the lower lid open too. **A choice between two
things is not a licence to keep both.** Rule 6.

`TRUNK_OPEN_DEG = 0.0` means SHUT and the swing is **skipped, not run at zero** — `_swing_open()`
asserts the free edge travels, so a shut lid put through it would fire a guard on a correct pose.
The T-handle and the plate are **no longer carried and no longer join `SWUNG`**. Length **4.065**.

**DO NOT PROPOSE REOPENING IT, and do not ask him for a photograph of the open tail: with the lid
shut, nothing in that bay shows.**

### 2b. AND CLOSING IT EXPOSED A DEFECT INVISIBLE FOR A WHOLE REVISION

```
lid_trunk   x -1.8730 .. -1.8702      the shut lid's outer face, at X_TAIL
trunk_bay   x -1.8750 .. -1.4550      the lining's face, 2.0 mm AFT of it
```

`trunk_bay()` set its origin to `x_skin − 0.002 + BAY_DEPTH*0.5`; `solid_prism` extrudes ±depth/2, so
the aft face landed **2 mm PROUD of the tail skin — the sign of the inset was inverted.** With the lid
open, nothing stood in front of it. With it shut it won the depth test across a closed panel and the
tail rendered with a **dark charcoal rectangle where the red engine lid belongs.** Guarded, and
watched fail on `T1_BAYPROUD=1`.

### 2c. THE TRUNK BAY HAD SHIPPED WITH NO MATERIAL AT ALL

`A()` only **appends** to `ASSIGN`; the loop that consumes it is step 9 at `build.py:846`, **91 lines
above** step 8c's call — the only `A()` in the file that lands after its own consumer. The bay
rendered at Blender's default grey, **1.28× the body red**. Now **0.51×**. `VERIFY` was clean and the
log line printed `len(ASSIGN)` — **appends, not assignments** — so it asserted coverage. Guarded
against the cause, watched fail on `T1_BAREMAT=1`.

---

## §3. THE TAIL BOARD — BUILT, AND WHY REV 49'S REFUSAL WAS WRONG

Rev 49 **refused** the rev-49 brief's job 1 because the source records the owner retiring that panel.
**He corrected it: "That was referring to a different sign. This one is part of the vehicle."**

**There are TWO BOARDS in `ref_rear34.jpg`.**

| | what it is | where it stands |
|---|---|---|
| **"La Santa"** | cream, **red brush script**, red star | on the **GROUND, BEHIND** the bus. This is `signboard()`. Correctly retired. |
| **the tail board** | cream face, **red rim**, amber bulbs, 38° | **ON the vehicle**, at the drip rail at the tail |

**Three pieces of physical evidence, not inference:** the base sits on the drip rail to **1 px** of the
locked fit; its bulb string is **continuous with the drip-rail run** at a pitch indistinguishable from
the vehicle's own `BULB_PITCH`; and **a power cable descends from it into the body.**

**Measured** (every figure with its ceiling in SPEC §10.123.2): base 1.747 ± 0.027 m, tilt
**38.0 ± 2.3° FROM HORIZONTAL** (*say which datum* — from vertical it is 52.0°), chord 0.711 ± 0.028 m,
bulb pitch 28 ± 2 mm, one stay.

**THE FOOT IS SOLVED, AND REV 49's OWN DECLARED 80 mm IS WITHDRAWN.** It was never a conflict between
the photograph and the geometry — the board was at the **wrong station**. The rear roof corner falls
away fast, and exactly one station satisfies both the photographed base height and the roof's own skin:

```
photographed base height           1.747 +- 0.027
roof skin at the solved station    1.7497           ->  2.7 mm
tip lands at                       2.2001
measured tip                       2.184 +- 0.030   ->  16 mm, inside the band
```

The station is **derived from `T1_body`'s own vertices at run time**, not typed, so it follows the
shell. **And the guard rev 49 first wrote for this was a TAUTOLOGY** — `z0 − _crown ≡ +0.005` by
construction — which the photorealism survey caught. The replacement measures the **built board**
against the **built skin**, and caught a further 3.7 mm on its first run.

**STILL NOT MEASURED, and NOT MEASURABLE from anything we hold:** the **width across the vehicle**
(parallax bounds it at **W ≤ 0.59 m with NO lower bound**) and the **fore-aft depth plane** — the
solved station sits 128 mm aft of the near-flank silhouette read, and the stay lands at 72.1° against
a measured 77.5°. **That is ONE unmeasurable quantity showing up twice, not two defects**, and it
closes with §7 item 1.

---

## §4. THREE ARTWORK STATES, NOT TWO VEHICLES — AND FIVE DUPLICATE FILES

**RULE 26 AS WRITTEN IS NOT SUFFICIENT.** "Check which bus" passes a Nolita reading and it is *still* a
wrong-artwork measurement.

| class | frames | carries |
|---|---|---|
| **RED, CURRENT — THE TARGET** | `ref_side.jpg`, `ref_rear34.jpg` | scrollwork, Señor Tacombi script, Calidad burst |
| **RED, AN EARLIER STATE** | the four **Nolita** frames | **plain red flank, `TACOMBI.COM`, `267 ELIZABETH STREET`, a chalkboard. NO scrollwork, NO script, NO burst.** |
| **GREEN — geometry only** | `ref_workshop.jpg`, `IMG_2073.jpeg` | a different decal entirely (spike depth 0.044 vs 0.133/0.239) |

**AND FIVE FILES ARE BYTE-IDENTICAL DUPLICATES.** `IMG_3842.png` = `ref_playa_34.png`;
`IMG_2054` = `ref_nolita_flank`; `IMG_2053` = `ref_nolita_front34b`; `IMG_2060` = `ref_nolita_front34`;
`IMG_3840` = `ref_nolita_doorshut`. **TEN distinct vehicle frames, not fifteen.** Do not count a
duplicate as corroboration.

---

## §5. W6 — THE TRADE DID NOT EXIST, THEN THE LEVER DIDN'T EITHER. **ASK HIM AGAIN.**

**He was asked for three revisions to choose between accurate paint and a clean white background.
THERE IS NO SUCH TRADE.** The background is a **compositor constant** laid under a keyed render and
renormalised to 252 DN in post. Measured, base vs `T1_CYCALB=0.30`: **max |difference| 0.000, 100.00 %
at 255.** No lighting change can reach it.

**And he retired the pure-white backdrop lock himself at rev 15** — SPEC §6 carries it struck through,
*"RETIRED, §10.69 — THE OWNER'S DECISION"*. Three revisions refused lighting changes citing it as live.

**THE SWEEP** — `probe_rev45_paint.py`, 4 controls incl. its kill, 0 FAILED every run:

| lever | P1 body red G/R | verdict |
|---|---|---|
| base | **0.455** (3.5 σ) | — |
| `T1_CYCALB` 0.76 → 0.30 | ~0.45 | **DEAD** |
| bigger softbox, **short axis** 3.5× | **0.452** | **DEAD** |
| `T1_SPEC = 0` | 0.347 | **rev 8 made this fix and REVERTED it** |
| both axes 3.5× (12× area) | 0.351 | works — but see below |
| photographed | 0.223 ± 0.066 | albedo already right (0.250) |

**Growing the source in the axis that sets the streak moves the red by 0.003.** So the both-axes gain
is **not softening** — it is the rig growing past the subject until it becomes an **enveloping dome**.
`T1_SOFTEN` does not tune the studio, it **replaces** it, and it costs 29 % of the cream's brightness.

**HE CHOSE "re-light to match your photographs" WITHOUT KNOWING THAT.** `T1_SOFTEN` defaults to **1.0**
and **nothing ships changed**. **Put it to him again with the k=1.0 and k=3.5 frames side by side and
the exposure cost stated** — that is a look decision and it is his.

---

## §6. WHAT IS STILL WRONG — WORK THIS LIST IN ORDER

*(This section is written from a 19-agent coordinated survey run at the owner's request at the close of
rev 49: twelve subsystem surveys → five adversarial refuters → a completeness critic → one ranked
synthesis. The full output is `SURVEY_rev49_photoreal.md`. **Read it before starting item 1.**)*

**PLACEHOLDER — filled below from the survey.**

---

## §7. WHAT ONLY HE CAN GIVE — AND HE HAS SAID NEITHER IS POSSIBLE NOW

Full text in `PHOTOS_WANTED_rev49.md`. **He answered at rev 49: "Neither is possible right now." STOP
ASKING** — record what each frame unblocks and work on what the frames we hold can settle.

1. **THE TAIL BOARD'S FOOTING — NEW, AND NOW THE TOP ITEM.** Closes the board's **width**, its
   **lateral position** and the **80 mm foot inconsistency** together. **`SPEC.md:937` §10.28 has
   demanded it since rev 12 and nobody ever asked him for it.**
2. **THE DECAL, DARKER — NOT CLOSER.** Five items. **Rev 49 tried to dissolve this request and failed
   its own calibration**: at `ref_side.jpg`'s exact resolution *and* 4:2:2 subsampling the estimator
   recovers a known gap to **2 % with a flat plateau**, and on the real frame it has **no plateau and
   lands 158 % off**. 60.8 % of the white lettering is clipped. **The photograph, not the method, is
   the binding constraint.**
3. **THE NOSE, SQUARE ON.** W4, six revisions.
4. **A RAKING-LIGHT FRAME OF THE LOUVRES** — the pressing depth.
5. **THE OFF SIDE — ANY FRAME AT ALL.** Every frame in the project is of the serving side.

**~~THE TAIL WITH THE ENGINE LID OPEN~~ — DROPPED.** It was item 1 for two revisions. He has ruled the
lid **shut**; with it shut, nothing in that bay shows.

---

## §8. THE THING THAT OUTRANKS EVERY ITEM ABOVE

**This project measures beautifully and its instruments keep being wrong.** Rev 46 caught five, rev 47
four, rev 48 four (three its own), **rev 49 four, and three were its own:**

* **A TAUTOLOGY PUBLISHED AS A MEASUREMENT.** Rev 49 reported that the decal's type separates from the
  burst on chroma, headlined *"of the 3007 burst pixels, ZERO have G ≥ 254"*. The mask
  `(R−G)/R > 0.22` forces `G < 198.9` **by construction**. Observed max: 198. **An algebraic identity
  about the threshold, presented as a fact about the photograph.**
* **A FOOT BURIED 120 mm INSIDE THE ROOF**, from typing a datum measured at a different station.
* **A MEASUREMENT APPLIED ACROSS DEPTH PLANES** (rule 16) — a near-flank reading used in a centreline
  build, where the source explicitly says the sign flips.
* **AND A SECOND MEASUREMENT REFUTED THE FIX**: re-seated, the stay's own triangle landed 144 mm aft
  of `X_TAIL`, in mid-air.

**AND THE RECORD WAS WRONG IN PLACES NOBODY CHECKS.** `cal_gen.py:385` still said *"the model has NO
REAR VENTS"* — **rule 1's own founding case** — two revisions after rev 48 cut real apertures.
`verify.py` called the 3.0 m bbox top *"the raised signboard"* in two places; it is `lid_main`, and
`signboard()` has been gated off since **rev 12**. SPEC §10.26's table still published *"trunk lid |
OPEN, at the tail"*. All four landed in the source at rev 49.

> **A RETRACTION THAT LANDS IN A LEDGER AND NOT IN THE SOURCE IS HALF A RETRACTION.**

---

## §9. THIS MACHINE

```
cores 4   RAM 15 GB   Blender 4.5.3 via pip install bpy
build  T1_SUB=1  ~20 s        build  T1_SUB=2  ~100 s
cal_gen ~45 s                 render 1600x1100 96 spp  ~5-9 min PER VIEW
```

```bash
/tmp/blender/blender -b -P build.py                          # T1_SUB defaults to 2
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
T1_PREVIEW=side T1_PFX=r50 T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
  /tmp/blender/blender -b -P build.py
```

**`out/` IS NOT TRACKED AND STARTS EMPTY ON A CLONE.** `probe_rev48_louv.py` hard-defaults to
`out/r48b_side.png`; with `out/` empty a bare run prints MISSING and **emits no summary line at all** —
easy to mistake for a pass. **Render before quoting any probe that reads a frame.**

**14 views, and `hero` IS one of them** — `hero34f`, **`hero`** (`studio.py:1268`), `hero34r`,
`front34`, `side`, `front`, `rear`, `detail_f`, `low34`, `topdown`, `playa`, `playa_ref`, `playa_w`,
`counter`. *Three consecutive briefs said "there is no view called `hero`".*

### ABLATION SWITCHES ADDED AT REV 49 — every one exists to WATCH A GUARD FAIL

| var | reproduces |
|---|---|
| `T1_BAREMAT=1` | the trunk bay with no material |
| `T1_TBFOOT=1` | the tail board's foot buried in the roof |
| `T1_BAYPROUD=1` | the bay lining 2 mm proud of the tail skin |
| `T1_SOFTEN=k` | the rig-replacement lighting sweep (default 1.0 = rev-48 rig exactly) |
| `T1_NOTAILBOARD=1` | stands the tail board down |

### SHELL TRAPS THAT HAVE COST REAL TIME

* **`pgrep -f "blender -b -P build.py"` MATCHES ITS OWN SHELL.** Wait on a **PID**
  (`while [ -d /proc/$P ]`), never on a pattern.
* **`read -t N </dev/null` RETURNS INSTANTLY** — rev 49 built a wait loop out of it that reported
  "waited 480 s" after waiting zero. If you need to wait, `python3 -c "import time;time.sleep(n)"`.
* **`T.solid_prism` EXTRUDES CENTRED ON ITS ORIGIN**, not forward from it — and **advancing the origin
  does not protect the inset's SIGN**, which is how rev 48's 2 mm defect shipped.
* **`verify_clone.sh` REQUIRES A CLEAN TREE.** It reports `modified tracked files` and stops. Commit
  first, then verify.

---

## §10. HOW TO USE YOUR PARALLELISM

> **DO NOT FAN OUT BLENDER.** Cycles already uses all four cores. Check
> `ps -eo pcpu,args --sort=-pcpu | head` before launching. **Run renders SEQUENTIALLY from one script
> and analyse in the foreground while they go.**

**Subagent concurrency on this box is capped at 2** (`min(16, cores−2)`). A 19-agent workflow runs in
about ten rounds. Plan for that: prefer **fewer, deeper** agents over many shallow ones, and use
`pipeline()` so verification starts as soon as each survey finishes rather than at a barrier.

**Fan out everything that is NOT a render**, and **instruct verifiers to REFUTE**. Rev 49 ran four
agents plus a 19-agent survey; **three of the four changed its conclusions**, and one of them **killed
its author's own headline finding.** That is what they are for.

**AND FINISH WHAT YOU DISPATCH.** Rev 46 closed with one outstanding and it cost a whole revision.
**Rev 49 dispatched five efforts and all five reported before its ledger was written.**

---

## §11. THE RULES. EVERY ONE WAS EARNED BY A DEFECT.

1. **A claim in prose is not a guard** — and **a claim in a SOURCE COMMENT is not a measurement.**
2. **A constant tuned against another must be EXPRESSED in terms of it — and DERIVED AT RUN TIME.**
3. **Read each probe's own summary line, never its exit code.**
4. **Never put a figure in an acceptance test unless you watched it print.**
5. **Do not inherit a guard's rationale along with its shape.**
6. **An ordinal fact licenses a SIGN, never a SHAPE.** *(Fired again at rev 49: "the MAIN bay" was
   read as a licence to keep both bays open.)*
7. **A leading question is not evidence, even when the answer is yes.**
8. **A measurement's window is part of the measurement.**
9. **A threshold trace is only valid if the feature's FAR SIDE is resolved.**
10. **A detail you cannot see is not a detail — and a detail you looked at badly is not looked at.**
11. **When a fix cannot be built at any tolerance, suspect the thing it is fixing.**
12. **Add the guard in the same edit as the change.**
13. **Inventory the frames you already hold before asking him for a new one.** *(Discharged properly
    for the first time at rev 49: TEN frames, not fifteen.)*
14. **Prefer dimensionless measurements.**
15. **Retract in the same revision you find the error** — in SPEC, **in the source**, and to him.
16. **A PART MEASURED IN ISOLATION FROM WHAT IT IS FITTED TO IS NOT MEASURED** — including from the
    DEPTH PLANE it was read in. *(Fired at rev 49, twice.)*
17. **MEASURE THE MERGE STATE; NEVER TRANSCRIBE IT.** Stale four revisions running.
18. **A CONTROL THAT IS RIGHT FOR THE WRONG REASON IS NOT A CONTROL.**
19. **A CONTROL IS NOT FINISHED WHEN IT PASSES. IT IS FINISHED WHEN YOU HAVE WATCHED IT FAIL ON THE
    DEFECT** — and **a guard that CRASHES reports nothing.**
20. **AN INSTRUMENT THAT HAS NEVER BEEN WRONG HAS NEVER BEEN TESTED.**
21. **HIS REPEAT IS A MEASUREMENT.**
22. **CALIBRATE AGAINST A KNOWN DISPLACEMENT, AT THE REAL DATA'S RESOLUTION.** *(This is what killed
    rev 49's decal finding — and it is the rule working exactly as intended.)*
23. **A HORIZONTAL OVER A HORIZONTAL AT THE SAME ROW NEEDS NO AXIS RATIO.**
24. **QUOTE THE RATIO, NOT THE READING — *founding case REFUTED at rev 48*.**
25. **CLEARANCE IS NOT LEGIBILITY.**
26. **A MEASUREMENT FROM THE WRONG VEHICLE IS NOT A MEASUREMENT** — **and rev 49 sharpened it: there
    are THREE ARTWORK STATES, not two vehicles. Check which STATE, not just which bus.**
27. **A CAP NOBODY LOGS READS AS COVERAGE** — **and rev 49 inverted it: A COUNT THAT LOGS THE WRONG
    QUANTITY READS AS COVERAGE TOO.** `len(ASSIGN)` counts appends, not assignments.
28. **RENDER IT, CROP IT, AND LOOK AT IT.** **Every headline finding at rev 46, 47, 48 and 49 came
    from looking at an image.**
29. **NEW, rev 49 — A RETIREMENT INHERITS THE OBJECT IT WAS MADE ABOUT, NOT THE STATION IT WAS SEEN
    AT.**
30. **NEW, rev 49 — A FIXTURE'S FOOT MUST BE CLEAR OF THE BODY IT STANDS ON, AND SOMETHING MUST CHECK
    IT.**

---

## §12. THE STATE OF THE MACHINE AT HANDOFF

```
bootstrap.sh      ALL 10 PASS
verify_clone.sh   ALL 113 PASS  (110 at rev 49's pickup; 4 added, 1 relabelled, NONE relaxed)
build             T1_SUB=1  VERIFY: 0 fail, 0 warn
                  length 4.065 vs spec 4.055     171 objects, 0 bare materials
probes            probe_rev45_paint   4 checked, 0 FAILED   (P1 0.455 reproduced exactly)
                  probe_rev47_gap     3 checked, 0 FAILED
                  probe_rev47_sharp   9 checked, 0 FAILED
                  probe_rev48_louv    NEEDS out/r48b_side.png -- RENDER IT FIRST
                  probe_rev46_reports PARTLY RETRACTED -- do not quote
renders           out/ is NOT TRACKED and starts EMPTY.  Re-render before any frame-reading probe.
NO DISPATCHED TASK IS OUTSTANDING.  Five efforts ran; five reported; three changed
the conclusions and one killed its author's own headline finding.
```

**`git rev-list --count origin/main..HEAD` before you start and again before you finish. And
`git diff --name-only HEAD...origin/main` — that is where his photographs arrive.**
