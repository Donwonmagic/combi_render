# NEXT CONTEXT PROMPT — rev 49

**Read this whole file before you touch anything.** Everything you need to start is here; everything
you need to be *correct* is in `SPEC.md` (which now actually contains §10.118–§10.122 — rev 48 had to
write four of them, see §8), `LEDGER_rev48.md`, and `LEDGER_rev47.md`.

---

## §0. WHAT HE SAID, AND WHAT IS LEFT

| his words | state |
|---|---|
| "100% calidad off center" | **FIXED** rev 46, guarded, guard watched fail. |
| "the vw logo wrong" | **FIXED** rev 46. Residual 0.1167 → 0.0347. |
| "señor Tacombi still isn't clearer" | **BLUR FIXED** rev 47. **CONTRAST HALF STILL OPEN, gated on W6.** |
| "It still does not read as two separate words" | **FIXED rev 47b — but its magnitude is now RETRACTED.** §4. |
| "the nose of the car is too flat" | **CONFIRMED, NOT FIXED, still no photographed anchor.** §6. |
| "we're going to need the trunk open like it's in service" | **BUILT rev 48.** §2. |
| "the main bay that should be open is the upper one" | **BUILT rev 48.** Both rear bays open. §2. |
| "The geometry appears the same" | **RULING.** Geometry transfers between his two vehicles. §3. |
| *(chose)* **the RED bus is the target** | **RULING.** Paint and artwork do NOT transfer. §3. |
| "They are actually stars that were not properly represented" | **BUILT rev 48.** §5. |
| "fill it as a service bay" + "I trust your judgement" | **LINED, contents NOT invented.** §2c. |
| "the lettering looks off as well" | **STILL OPEN**, and §7 says exactly which photograph unblocks it. |

> **RULE 26 — NEW, rev 48. A MEASUREMENT FROM THE WRONG VEHICLE IS NOT A MEASUREMENT.**
> The reference set contains **two** Señor Tacombi T1s. Rev 47 measured a decal dimension on the
> green one and applied it to a model of the red one, and no document flagged it. **Before quoting
> any figure, check which bus it came off, and whether the quantity is geometry (transfers) or paint
> and artwork (does not).**

---

## §1. START HERE — AND DO NOT TRANSCRIBE A BRANCH NAME OR AN AHEAD-COUNT

```bash
cd /home/user/combi_render
./bootstrap.sh            # ALL 10 PASS
./verify_clone.sh         # ALL 110 PASS
```

### THE BRANCH INSTRUCTION HAS BEEN STALE THREE REVISIONS RUNNING

Rev 47's brief named a branch and an ahead-count of 5; the real count was 1. Rev 48's brief named
`claude/combi-render-rev46-t8vhpm`; that branch was **0 ahead / 1 behind `main`**, and obeying it
would have discarded the whole of rev 47 — twelve commits including two owner uploads.

**So this file does not name a branch to check out. It names a MEASUREMENT.**

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
At the time of writing that is `claude/combi-render-rev48-ypkd3o`, 11 ahead / 0 behind — **but check,
do not believe this sentence.** He pushes photographs straight to `main` from the web UI, mid-revision,
without saying so. **Re-run the diff at the start of every session, not once.**

If `verify_clone` fails on **`commits >= 227 → got short:NNN`**, that is a shallow clone and the
script says so. `git fetch --unshallow`, re-run. **Do not edit the script.**

---

## §2. WHAT REV 48 BUILT

### 2a. Both rear bays open

```
    trunk lid  separated 2200v (SUB=1) / 7982v (SUB=2), hinge lateral, OPEN 52 deg
    rear hatch glass_rear hinged lateral, OPEN 64 deg
    free edges  dx -0.3850 / -0.2985 m aft,  dz +0.1878 / +0.1865 m up
```

**The trunk lid was never a seam.** `T1_body` has **six** connected components and one of them is
`gap_prism`'s outline to 3 mm — the panel has been free since the gap boolean was written.
`build.py:69` said so all along. Rev 48 separated, named and hinged it; nothing was modelled.

**Both angles are POSE CHOICES**, declared `NOT MEASURED` in the source and guarded. No frame in this
project shows either lid open. **§7 item 1 is the frame that replaces them with measurements.**

### 2b. It opened INWARD first, and only a render caught it

`VERIFY: 0 fail, 0 warn`. `verify_clone` ALL 95 PASS. The log said *"separated 2200v … OPEN 52.0
deg"*. Every number green, and the lid was folded into the engine bay with the 1963 plate and the
T-handle hanging inside the cavity. **One crop showed it in a second.**

`_swing_open()` now guards direction, is shared by both lids, and has been **watched fail** on the
inverted sign. **Read §9 before you build anything.**

### 2c. The rear louvres became APERTURES

They had been **closed ribs on unbroken metal** since rev 16 — `louvres()` says so itself: *"A sweep,
not a boolean … the shell is never touched."* One hole per flank now spans the block, the blades
span the hole, and a shallow dark bay sits behind. **Signed modulation +0.0343 → −0.2559**: they
stopped catching the key and started shadowing themselves, which is the sign the photograph has.

**AND THE FIRST CUT WAS VISIBLY WRONG WHILE EVERY NUMBER SAID IT HAD WORKED.** The modulation went
the right way at the first attempt and `VERIFY` was clean; the *render* came back with **bright white
bars among the slots** — cabin light shining out through the new holes. Rule 28, fired on a change
made in the same revision that wrote rule 28.

**A constant that could not be wrong until the shell was cut:** the blade section was 11.0 mm, but a
21.11 mm pitch and a ~7 mm inferred aperture require **14.1 mm**. It never showed, because the "slot"
was solid metal. Now `LOUV_SECT = LOUV_PITCH − LOUV_APERTURE`.

### 2d. The bay is LINED and its contents are NOT invented

He chose "fill it as a service bay" and then said "I trust your judgement". The void is fixed; crates
and a gas bottle are not there, because no frame shows them. **Do not add them without §7 item 1.**

---

## §3. THERE ARE TWO VEHICLES — AND THIS IS THE MOST IMPORTANT THING IN THIS FILE

| | body G/R | |
|---|---|---|
| `ref_side.jpg`, `ref_rear34.jpg` | 0.204, 0.269 | **RED — THE TARGET** |
| `IMG_2073.jpeg`, `ref_workshop.jpg` | 1.378, 1.304 | GREEN — geometry only |

0.20 against 1.38 is not white balance. **His rulings: the red bus is the target; geometry transfers
between them; paint and artwork do not.**

**What that already cost.** `LINE_GAP` was set from the green bus's decal (§4). Three of rev 47's
four decal "defects" were green-bus readings, and on the red bus **the build was already right for
two of them** — its few long broad spikes and its single left-hand star match `ref_side.jpg`. The two
decals are measurably different artwork: spike depth **0.133 / 0.239** against **0.044**.

**W5 IS DISSOLVED, NOT ANSWERED.** The rev-48 brief said "every frame shows a hand-chalked
blackboard". `ref_side.jpg` — the frame the mural was measured from at rev 11 — shows the flower
mural with yellow menu strips, exactly as built. **It was never a defect. Do not raise it again.**

---

## §4. `LINE_GAP` — RETRACTED, KEPT, AND WHY BOTH

`probe_rev47_gap.py` carried `built_truth = 0.111` as a **frozen literal** commented "from cal_gen".
It was typed, and it was the value for `LINE_GAP = 0.26`. The probe reported **1 FAILED** while the
brief and ledger both reported 0.

**The failure pointed the wrong way.** At 0.43 the estimator reads 0.281 against a construction
0.2776 — **1.2 % error, its best operating point.** C1 was failing *because the instrument had become
right*: **it passed when the estimator was 34 % wrong and failed when it was 1 % right.**

**The "+34 % bias" is not a bias.** Swept 0.20→0.50 the read/truth ratio runs **2.00, 1.34, 1.13,
1.08, 1.01, 1.13** — affine with a negative intercept. On clean synthetics it reads 0.984 everywhere.
**The mechanism:** the estimator picks its reading angle by *maximising the apparent gap*, selecting
−37.5° on a decal set at −19.7°. Skewing staggered words enlarges the apparent gap, hardest when the
gap is small.

> **RULE 24 — "QUOTE THE RATIO, NOT THE READING" — HAS ITS FOUNDING CASE REFUTED.** The rule may
> still be good practice. **This case does not support it, and rev 48's brief introduced the rule on
> the strength of it.**

**0.43 is kept deliberately.** The correction (0.376) is *also* the green bus's number. The red bus
bounds the gap to **0.25–0.47** and no further, because both red frames are **blown**. Both values sit
inside. The source declares it TRANSFERRED / ARTWORK CONFIRMED DIFFERENT / MAGNITUDE UNVERIFIED and
two rows require it to keep saying so. **§7 item 2 is what closes it.**

---

## §5. THE STARS — and rev 46's stated reason was false

> *"They are actually stars that were not properly represented."*

Rev 45 drew **bunting**; rev 46 retired it at his instruction **and recorded the reason as "No frame
we hold shows them"**. `ref_side.jpg` shows the band plainly at 7×. **Their presence was never the
error — their identity was.** Built as 7 stars in the measured band plus the isolated lower-left mark.

**`STAR_N` is NOT MEASURED**: both red frames are blown, so the band returns as one merged 1499-px
component. And **the clamp reports itself** — 2 of 7 band positions fall outside this decal's own
rectangle (on the vehicle they are painted on the body). *A silent truncation reads as coverage.*

---

## §6. WHAT IS STILL WRONG — WORK THIS LIST IN ORDER

> **THE LOUVRE APERTURES WERE ITEM 1 HERE AND REV 48 THEN BUILT THEM.** This file was written before
> that work and said "closed ribs, not apertures — the real JOB 2". It is **done**: one hole per
> flank, blades spanning it, a dark bay behind, signed modulation **+0.0343 → −0.2559**. The row is
> struck rather than deleted, because a brief that tells you to do something already done is the
> exact failure this project keeps having, and rev 48 caught it in its own handoff. **Do not rebuild
> it. Check `probe_rev48_louv.py` and `verify_clone`'s six louvre rows first.**
>
> What is left of it is one number: **the pressing DEPTH**, which needs `PHOTOS_WANTED_rev48` item 3
> (a raking-light frame). *Do not tune it from rev 48's amplitude figures — built 0.385 against a
> photographed 0.206 is one lighting against another, and the probe prints that ceiling every run.*

1. **THE BUILD IS ONE RAISED PANEL SHORT.** Both red frames show a thin bulb-lined board based on the
   drip rail at the tail, **z 1.78 ± 0.07 m**, tilted 39°, tip ~0.5 m past `X_TAIL` at z ≈ 2.26 m.
   Nothing in the model occupies that station. **`signboard()` will NOT do it** — wrong hinge axis
   (fore-aft, needs lateral), wrong extent (stops 93 mm short of `X_TAIL`), wrong presentation, and
   it was written for a different board in a different frame.
2. **W6, and it gates W3.** Body red G/R 0.455 built vs 0.223 ± 0.066 photographed (3.5 σ); ~half the
   excess is the white cyclorama's own specular (`T1_SPEC=0` moves it 0.455 → 0.347), and softening
   it trades the catalogue-clean background he set as the bar. **He was asked at rev 48 and answered
   a different question. Ask again — it has blocked W3 for three revisions.**
3. **W4, the nose.** 14.3 mm over 0.70 m of half-width — a plane. Method 2, silhouette corner-wrap on
   `ref_workshop.jpg`, is still the live one, and it is the method that does not care about lighting.
   **`bulge = 0.019` IS the only forward bulge constant** — that check is finally done, statically and
   exhaustively, with one qualification: `step = -0.0062` also displaces nose vertices along their own
   normal, but it is a **recess** (the pressed V-swage), not a bulge. *And the shell is subdivided
   before `nose_shape` runs, so the limit surface adds curvature no constant names.*
   **THE TRAP, unchanged:** `V_POW_Z` is a **paint** curve. `verify_clone` locks it at 0.60 for a
   reason.

---

## §7. WHAT ONLY HE CAN GIVE — and item 2 is not the request every prior revision made

Full text in `PHOTOS_WANTED_rev48.md`. The two that matter:

1. **THE TAIL WITH THE ENGINE LID OPEN.** Settles the hinge, the open angle, stay-vs-counterbalance
   and the bay's contents — four items, one frame. **No frame in this project shows it.** It is what
   turns `TRUNK_OPEN_DEG`, `REAR_OPEN_DEG` and the bay lining from pose choices into measurements.
2. **THE DECAL, NOT BLOWN OUT — AND THIS IS THE CORRECTION.** Every prior revision asked for a
   *closer* frame. That was the wrong request. **`ref_side.jpg` already has the resolution** — the
   burst is **99 × 75 px** there, 2.7× the area of `IMG_2073` and 4× `ref_playa_34`. What it lacks is
   **dynamic range**: both red frames are clipped, so the white type never separates from the red
   burst and the star band merges into one blob. **A darker exposure of the same shot** closes
   `LINE_GAP`, the spike count, the star count, the burst colour and "the lettering looks off"
   together.

*(`LEDGER_rev47.md` §203's "`ref_playa_34.png` is the only frame in the whole set that shows this
decal" and rev 48's brief's "`IMG_2073` ← the best frame in the project" are both refuted for this
decal.)*

---

## §8. THE THING THAT OUTRANKS EVERY ITEM ABOVE

**This project measures beautifully and its instruments keep being wrong.** Rev 46 caught five, rev
47 four, **rev 48 caught four more and three of them were its own:**

* **A periodicity bounder** that reported the louvre block at power **0.958** and looked
  authoritative. Blank paint reads up to **0.380**, the block **0.405** — **not separable**. It had
  locked onto the belt line. *Deleted, not re-thresholded: lowering a threshold makes a blind
  estimator quiet, not sighted.*
* **A silhouette anchor** that read the tail cap at **1315** (the **tail lamp**, 22 mm past the
  body's rearmost vertex) and then at **1396** (the **counter shelf**). Both plausible, both wrong.
  Replaced by projecting through the camera dict, which has no such failure mode.
* **`verify.py`'s `_bounds()` was reading STALE `bound_box`es.** `glass_rear` read
  −1.856…−1.850 while its vertices spanned −2.151…−1.850 — **295 mm hidden**. Worse, it made the
  length row **pass for the wrong reason**: the staleness happened to hide exactly the parts that
  needed excluding. Now computed from **vertices**, with the exclusion read from `t1_shell.SWUNG`.
* **A finding, retracted in the revision that found it.** Rev 48 concluded the built louvres read
  with the wrong sign *because* `LOUV_OFF` rides them proud. **`ref_nolita_front34.jpg` shows the
  same real louvres reading BRIGHT.** Sign follows the key light, not the pressing.

**AND THE RECORD ITSELF WAS WRONG IN PLACES NOBODY CHECKS.** `SPEC.md` stopped at **10.117** while
`cal_gen.py`, `t1_core.py` and `script_gen.py` cited **10.118–10.121** as though they existed —
because `LEDGER_rev46.md` §7 said they were "written into the sources", which reads as "written into
SPEC" and was not. `bootstrap.sh`'s header still said the pip branch was **NEVER EXERCISED** while
the brief said it was discharged. `verify_clone.sh` still called the vent slats **DARK GREY**, a
reading retracted a revision earlier — **in the ledger only**.

> **A RETRACTION THAT LANDS IN A LEDGER AND NOT IN THE SOURCE IS HALF A RETRACTION.**
> The machine is what the next context believes. Fix it *there*.

---

## §9. THIS MACHINE

```
cores 4   RAM 15 GB   Blender 4.5.3 via pip install bpy
build  T1_SUB=1  ~25 s        build  T1_SUB=2  ~100 s
cal_gen ~45 s                 render 1600x1100 96 spp  ~5-6 min PER VIEW
```

```bash
/tmp/blender/blender -b -P build.py                          # T1_SUB defaults to 2
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
T1_PREVIEW=side T1_PFX=r49 T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
  /tmp/blender/blender -b -P build.py
```

**Rendering the louvres:** `probe_rev48_louv.py` takes `T1_LOUV_FRAME` to pick which frame in
`out/` it reads, so a BEFORE and an AFTER can be put through the identical instrument. It defaults
to rev 48's pre-aperture render, so a bare run reproduces the figures it was written against.

**14 views, and `hero` IS one of them** — `hero34f`, **`hero`**, `hero34r`, `front34`, `side`,
`front`, `rear`, `detail_f`, `low34`, `topdown`, `playa`, `playa_ref`, `playa_w`, `counter`. *Three
consecutive briefs said "there is no view called `hero`". `studio.py:1268` says otherwise, and it is
the rev-44 delivery frame.*

**Network:** `WebSearch` works. `curl` reaches `raw.githubusercontent.com` and nothing else.

### TWO SHELL TRAPS THAT COST REV 48 TWO CONTAINER RESTARTS

* **`pgrep -f "blender -b -P build.py"` MATCHES ITS OWN SHELL.** `while pgrep -f ...; do :; done`
  never exits, spins a core, and the container is reaped. So does `pkill -f`. **Wait on a PID
  (`while [ -d /proc/$P ]`), not on a pattern.**
* **`T.solid_prism` EXTRUDES CENTRED ON ITS ORIGIN**, not forward from it. Rev 48's bay stood 210 mm
  proud of the tail before the length row caught it.

---

## §10. HOW TO USE YOUR PARALLELISM

> **DO NOT FAN OUT BLENDER.** Cycles already uses all four cores. **Rev 48 accidentally launched two
> render processes and halved both of them for seven minutes before noticing.** Check with
> `ps -eo pcpu,args --sort=-pcpu | head` before launching.

Fan out everything that is **not** a render: measuring frames, cross-checking the record, and
adversarial verifiers instructed to **REFUTE** a finding before it ships.

**AND FINISH WHAT YOU DISPATCH.** Rev 46 closed with a measurement task outstanding and it never
returned — it cost a whole revision. Rev 47 repeated it in miniature. **Rev 48 ran four agents and
all four reported before its ledger was written**, and two of them changed its conclusions: the
louvre agent refuted rev 48's own headline, and the panel verifier caught rev 48 silently re-adopting
an identification the owner had retired twice. **Set an agent on THIS FILE to refute it, first, and
do not close until it reports.**

---

## §11. THE RULES. EVERY ONE WAS EARNED BY A DEFECT.

1. **A claim in prose is not a guard** — and **a claim in a SOURCE COMMENT is not a measurement**
   (rev 48: rev 46 wrote "the model has no rear vents" into `cal_gen.py:339` and three revisions
   believed it).
2. **A constant tuned against another must be EXPRESSED in terms of it — and DERIVED AT RUN TIME.**
   A frozen literal is a lie with an expiry date.
3. **Read each probe's own summary line, never its exit code.**
4. **Never put a figure in an acceptance test unless you watched it print.**
5. **Do not inherit a guard's rationale along with its shape.**
6. **An ordinal fact licenses a SIGN, never a SHAPE.**
7. **A leading question is not evidence, even when the answer is yes.**
8. **A measurement's window is part of the measurement.**
9. **A threshold trace is only valid if the feature's FAR SIDE is resolved.**
10. **A detail you cannot see is not a detail — and a detail you looked at badly is not looked at.**
11. **When a fix cannot be built at any tolerance, suspect the thing it is fixing.**
12. **Add the guard in the same edit as the change.**
13. **Inventory the frames you already hold before asking him for a new one.**
14. **Prefer dimensionless measurements.**
15. **Retract in the same revision you find the error** — in SPEC, **in the source**, and to him.
16. **A PART MEASURED IN ISOLATION FROM WHAT IT IS FITTED TO IS NOT MEASURED** — including from the
    RESOLUTION it is compared at.
17. **MEASURE THE MERGE STATE; NEVER TRANSCRIBE IT.** Stale three revisions running.
18. **A CONTROL THAT IS RIGHT FOR THE WRONG REASON IS NOT A CONTROL** (rev 48: the length row passed
    only because a stale bounding box hid the parts it should have excluded).
19. **A CONTROL IS NOT FINISHED WHEN IT PASSES. IT IS FINISHED WHEN YOU HAVE WATCHED IT FAIL ON THE
    DEFECT** — and **a guard that CRASHES reports nothing** (rev 48).
20. **AN INSTRUMENT THAT HAS NEVER BEEN WRONG HAS NEVER BEEN TESTED.**
21. **HIS REPEAT IS A MEASUREMENT** — and the axis you already measured is not the one he is
    reporting.
22. **CALIBRATE AGAINST A KNOWN DISPLACEMENT, AT THE REAL DATA'S RESOLUTION.**
23. **A HORIZONTAL OVER A HORIZONTAL AT THE SAME ROW NEEDS NO AXIS RATIO.**
24. **QUOTE THE RATIO, NOT THE READING — *founding case REFUTED at rev 48*.** Keep the practice;
    know that the case that produced it was an angle-search artefact, not a bias.
25. **CLEARANCE IS NOT LEGIBILITY.**
26. **NEW, rev 48 — A MEASUREMENT FROM THE WRONG VEHICLE IS NOT A MEASUREMENT.** There are two buses.
    Geometry transfers; paint and artwork do not. **Check which one a figure came off before quoting
    it.**
27. **NEW, rev 48 — A CAP NOBODY LOGS READS AS COVERAGE.** If a routine drops, clamps or truncates
    anything, it must print what it dropped, every run.
28. **NEW, rev 48 — RENDER IT, CROP IT, AND LOOK AT IT.** The trunk lid opened INWARD through a clean
    `VERIFY`, 95 green `verify_clone` rows and a log line that said "OPEN 52.0 deg". **Every real
    finding at rev 46, 47 and 48 came from looking at an image.**

---

## §12. THE STATE OF THE MACHINE AT HANDOFF

```
bootstrap.sh      ALL 10 PASS   (the pip branch is now genuinely discharged, in the source)
verify_clone.sh   ALL 110 PASS  (86 at rev 48's pickup; 24 added, NONE relaxed)
build             T1_SUB=1  VERIFY: 0 fail, 0 warn
                  length 4.056 vs spec 4.055  (+1 mm, on a repaired instrument)
probes            probe_rev48_louv    11 checked, 0 FAILED
                  probe_rev47_gap      3 checked, 0 FAILED   (was 1 FAILED, undetected)
                  probe_rev47_sharp    9 checked, 0 FAILED
                  probe_rev46_vw       5 checked, 0 FAILED
                  probe_rev46_reports  PARTLY RETRACTED -- do not quote
renders           out/r48ship_*.png    both rear bays open, stars on the decal,
                                       louvres cut through and backed
NO DISPATCHED TASK IS OUTSTANDING.  Four ran; four reported; two changed the
conclusions and are recorded as having done so.
```

**`git rev-list --count origin/main..HEAD` before you start and again before you finish. And
`git diff --name-only HEAD...origin/main` — that is where his photographs arrive.**
