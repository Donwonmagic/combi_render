# LEDGER — rev 48

**Everything this revision measured, changed, refuted, retracted and corrected.** Figures here were
watched print unless a line says otherwise. **Where this ledger and the machine disagree, the machine
is right.**

---

## §0. THE OWNER'S REPORTS AND RULINGS THIS REVISION

| his words | verdict | where |
|---|---|---|
| **NEW** *"The geometry appears the same"* | **RULING.** Geometry may be measured from either vehicle. | §5 |
| **NEW** *(chose)* **the RED bus is the target** | **RULING.** Paint and artwork may NOT transfer from the green frames. | §5 |
| **NEW** *"They are actually stars that were not properly represented"* | **RULING, and it corrects rev 46's stated reason.** | §7 |
| **NEW** *"the main bay that should be open is the upper one"* | **BUILT.** The rear hatch opens; the trunk stays open too. | §4 |
| *(rev 47 standing)* *"we're going to need the trunk open like it's in service"* | **BUILT.** And the panel was already free. | §4 |

---

## §1. THE BRIEF, GRADED — IT WAS WRONG SEVEN TIMES

An adversarial agent was set on `NEXT_CONTEXT_PROMPT_rev48.md` before any work started, **and unlike
rev 46 and rev 47 this revision did not close until it reported.** Every item below was then
re-checked by hand against the machine.

| # | the brief says | the machine says |
|---|---|---|
| 1 | check out `claude/combi-render-rev46-t8vhpm` | **STALE, third revision running.** 0 ahead / 1 behind `origin/main`. Obeying it loses rev 47 entirely — 12 commits, two owner uploads. |
| 2 | JOB 2: *"the model has NO rear vents at all"* | **REFUTED against the build.** 20 louvres, built since rev 16. §2 |
| 3 | the grep *"returns … nothing else"* | **140 hits**, incl. `t1_detail.py:2122 # REAR-QUARTER AIR LOUVRES`. |
| 4 | *"There is no view called `hero`"* | **`hero` EXISTS** — `studio.py:1268`, the rev-44 delivery frame. Copied through three briefs. |
| 5 | the `pip install bpy` caveat is *"now discharged"* | `bootstrap.sh`'s header still said **NOT EXERCISED**. Now genuinely discharged, in the source. §8 |
| 6 | *"everything you need to be correct is in `SPEC.md`"* | **SPEC stopped at 10.117.** 10.118–10.121 were cited by three `.py` files and did not exist. §8 |
| 7 | `probe_rev47_gap` *"3 checked, 0 FAILED"* | **3 checked, 1 FAILED.** §6 |

**Two things the brief got right that mattered.** JOB 1's suspicion that the trunk lid was only a
seam — right in outcome, wrong in mechanism (§4). And its §8 insistence that this project's
instruments keep being wrong: **rev 48 killed three of its own.** §3.

---

## §2. JOB 2 IS REFUTED — THE LOUVRES HAVE BEEN BUILT ALL ALONG

Confirmed against the **BUILD**, from a `T1_SUB=2` run, watched print:

```
    louvres1 / louvres-1   560 v each   x -1.5371..-1.2419 (len 0.2952)
                                        z  0.8636.. 1.0699
                                        TEN slot rows, pitch 21.111 mm
```

`LEDGER_rev46.md` §5 ("NEW FINDING — THE MODEL HAS NO REAR VENTS"), `LEDGER_rev47.md` §10c
("nothing replaced them") and this brief's JOB 2 are all wrong.

**How it propagated is the lesson.** Rev 46 was right to retire the painted bunting from the decal.
But those painted lines sat **between the roof and the burst**; the real louvres are on the quarter
panel **half a metre lower**. Rev 46 concluded from retiring the paint that the geometry was absent,
and **wrote that conclusion into `cal_gen.py:339` as a source comment**, where every later context
read it as machine truth. Guarded now, three rows.

**The count is CONFIRMED, not inherited.** 10 slats on `IMG_2073.jpeg` (rows 468–582, cols
1156–1188, de-sheared s = −0.180), pitch **8.106 ± 0.023 px** — confirms rev 47's 8.02 ± 0.42 and
tightens it ~18×. Measured on the green vehicle, which is admissible **because it is geometry**.

**What is actually wrong is that they do not read.** `probe_rev48_louv.py`, **11 checked, 0 FAILED**.
The built block is bounded **by projection** through `studio.views()["side"]`, parsed at run time.

```
    ref_side.jpg   signed modulation  -0.0383   |amp| 0.2059
    the render     signed modulation  +0.0343   |amp| 0.1112
    RATIO   |photographed| / |built|   1.85x
```

**THE RATIO BOUNDS PROMINENCE, NOT DEPTH**, and the probe prints that ceiling every run. See §3.

**Still open, and lighting-independent:** `t1_detail.louvres()` is *"A sweep, not a boolean … the
shell is never touched"* — **closed ribs on an unbroken flank**, where a T1 louvre is an **aperture**.
That is the `bus_model_ref.JPG` fidelity bar, and it is the real JOB 2.

---

## §3. THREE INSTRUMENTS BUILT, WATCHED FAIL, AND THROWN AWAY

* **An automatic periodicity bounder** reported the built block at power **0.958** and looked
  authoritative. Blank painted panel reads up to **0.380**; the block itself **0.405**. **Not
  separable.** It had locked onto the belt line. Deleted, not re-thresholded — lowering the threshold
  makes a blind estimator quiet, not sighted.
* **A silhouette anchor for the projection.** "The rightmost non-white pixel" over z 0.81–1.10 gives
  **1315** — 22 mm past the body's rearmost vertex, because the **tail lamp** protrudes. Moved to
  z 1.20–1.50 it gives **1396**, because the **counter shelf** is there. Replaced by the camera dict.
* **A finding, retracted in the revision that found it** (rule 15). An earlier draft concluded the
  signs disagree *because* `LOUV_OFF` rides the sweep proud, and would have had rev 49 recess it.
  **`ref_nolita_front34.jpg` shows these same real louvres reading BRIGHT.** Sign follows the key
  light, not the pressing.

**And a fourth, in `verify.py`, which had been wrong for longer than this revision.** §4.

---

## §4. JOB 1 — BOTH REAR BAYS OPEN

### 4a. The trunk lid was never a seam

Connected-component analysis of `T1_body` from a real `T1_SUB=2` build gives **six** components, one
of them **7982 v at x −1.873…−1.870, y −0.467…+0.467, z 0.608…1.103** — `gap_prism`'s outline to
3 mm. `build.py:69` had already recorded the count going *"1 → 6 as each gap cutter frees a panel"*.
So: **separate, name, hinge** — not a rebuild — and the fragile `gap_englid` boolean is untouched.

**It swings AFTER the rake shear.** `_hinge()` rotates about a **fore-aft** axis, leaving x alone,
which is why a roof lid can swing before step 8b. A tail lid hinges **laterally** and moves x; swung
first, 8b would shear it at the wrong station.

### 4b. IT OPENED INWARD, AND ONLY A RENDER CAUGHT IT

The sign was inverted against its own docstring. The lid folded **into** the engine bay, carrying the
1963 plate and the T-handle in with it. **`VERIFY: 0 fail, 0 warn`. `verify_clone` ALL 95 PASS. The
log said "separated 2200v … OPEN 52.0 deg".** Every number green; one crop showed it in a second.

`_swing_open()` now guards it — shared by both lids, because a guard written twice gets fixed once —
and **watched fail** (rule 19):

```
    AssertionError: trunk lid opened the WRONG WAY: its free edge moved
    dx +0.3850 dz +0.1878
```

Its own first version was not a guard: it dereferenced a bpy struct after the mesh was mutated and
died with `bpy_prop_collection[-1425949424]: out of range`. **A guard that crashes reports nothing.**

### 4c. The upper bay — his correction

He was asked with **both** rear apertures marked on a straight rear view, marked **by projection**
through the rear camera. He chose **A, the rear window**. B stays open: he called the upper one the
*main* bay, not the only one.

```
    trunk lid  free edge dx -0.3850 m (aft)  dz +0.1878 m (up)
    rear hatch free edge dx -0.2985 m (aft)  dz +0.1865 m (up)
```

`REAR_OPEN_DEG` and `TRUNK_OPEN_DEG` are **POSE CHOICES** and say so; `verify_clone` requires the
declaration. No strut and no counterbalance is built — an invented one would be a claim.

**And SPEC §10.26's row "trunk lid | OPEN, at the tail | `ref_side.jpg`" is REFUTED.** That raised
panel is a thin board, cream-faced, red-bordered, with a **bulb string** along its lower edge. Its
base measures **1.78 ± 0.07 m** above ground — the drip rail — against 0.60–1.10 m for the engine
lid. **~11 σ.** Independently: the project's own locked drip-rail fit predicts v = 293.2 at that
column; the base measures **292**. `LEDGER_rev47.md` §5 was right.

### 4d. `verify.py` WAS READING STALE BOUNDING BOXES

The length row printed the same 4.065 after the hatch opened as before it, which cannot be true of a
pane that swings 0.30 m aft.

```
    glass_rear   bound_box x  -1.8560..-1.8500
                 vertices  x  -2.1510..-1.8501    <-- 295 mm hidden
```

**`ob.bound_box` goes stale after an in-place vertex edit.** `lid_trunk` was not stale — it is a
freshly created mesh — so the defect appears only on parts moved in place.

**Worse, it made the length row pass FOR THE WRONG REASON (rule 18).** The row excluded `lid_*` and
got the right answer only because the stale boxes happened to hide `glass_rear`, `englid_handle`
(aft-most vertex −2.3204) and `plate_1963` (−2.2008), none of which match that prefix. Had Blender
refreshed those boxes it would have gone red on a vehicle that had not moved.

Fixed two ways: `_bounds()` computes from **vertices**, and the exclusion reads `t1_shell.SWUNG`, the
set every swung part registers itself in — not a prefix, not a list.

```
    length excludes opened lids: 4.480 with them, 4.056 without
    spec 4.055  ->  +1 mm   (against +10 mm on the stale instrument)
```

---

## §5. THERE ARE TWO VEHICLES, AND HE HAS RULED ON THEM

| | body G/R | raised lid carries |
|---|---|---|
| `ref_side.jpg` **RED** | 0.204 | flower mural + yellow menu strips |
| `ref_rear34.jpg` **RED** | 0.269 | the mural board, **plus** the "La Santa" cream + red-script board |
| `IMG_2073.jpeg` **GREEN** | 1.378 | tufted damask panel, ornate green frame, bulbs |
| `ref_workshop.jpg` **GREEN** | 1.304 | plain cream — mid-conversion |

0.20 against 1.38 is not a white-balance artefact. **His rulings: the RED bus is the target; geometry
transfers; paint and artwork do not.**

**W5 DISSOLVES.** The brief says *"every frame shows a hand-chalked blackboard"*. **`ref_side.jpg` —
the frame `lid_gen.py` §A measured the mural from at rev 11 — shows the flower mural with yellow menu
strips, exactly as built.** No frame shows a chalked blackboard on the vehicle's own lid. W5 was never
a defect.

**A retraction inside this revision, caught by this revision's own verifier, and it was mine.** SPEC
10.122.5's table first described `ref_rear34.jpg`'s lid as *"mural outer / cream + red script inner"*
— the §10.19/§10.26 identification the owner retired in §10.28 and re-retired in §10.49. §10.49 exists
because §10.38 re-adopted it once already. **This was the third re-adoption.** Corrected and named.

**The build is one raised panel short.** Both red frames show a second: a thin board based on the
drip rail at the tail, z 1.78 m, tilted 39°, tip ~0.5 m past `X_TAIL` at z ≈ 2.26 m, bulb string,
one stay. Nothing in the model occupies that station. `signboard()` would **not** reproduce it —
wrong hinge axis, wrong extent, wrong presentation, and written for a different board in a different
frame.

---

## §6. THE DECAL — AND RULE 24'S FOUNDING CASE IS REFUTED

**`probe_rev47_gap.py` had a frozen literal.** `built_truth = 0.111`, commented *"the build's own
construction value, from cal_gen"*. It was typed, and it was the value for `LINE_GAP = 0.26`.

**The failure pointed the wrong way.** At 0.43 the estimator reads 0.281 against a construction
0.2776 — **1.2 % error, its most accurate operating point.** C1 was failing *because* the instrument
had become right: **it passed when the estimator was 34 % wrong and failed when it was 1 % right.**
Derived at run time now; 3 checked, 0 FAILED, honestly.

**The "+34 % absolute bias" is not a bias.**

```
    LG    0.20   0.26   0.32   0.38   0.43   0.50
    read  0.104  0.149  0.193  0.248  0.281  0.391
    r/t   2.00   1.34   1.13   1.08   1.01   1.13
```

Roughly **affine with a negative intercept**. A ratio rescaling assumes proportionality *through the
origin*. On clean synthetics the estimator reads 0.984 at every gap — there is no fixed bias.

**The mechanism.** The estimator picks its reading angle by **maximising the apparent gap**, and
selects −37.5° on a decal `cal_gen` sets at −19.7°. Skewing two staggered words enlarges the apparent
gap, hardest when the gap is small. **An instrument defect, not a property that divides out.**

> **RULE 24 — "QUOTE THE RATIO, NOT THE READING, the bias divides out" — HAS ITS FOUNDING CASE
> REFUTED.** The rule may still be good practice. This case does not support it.

**And it is the wrong vehicle.** 0.244 was measured on the GREEN bus. A word gap is artwork.

**0.43 is kept anyway, deliberately.** Inverting the curve gives 0.376 — still the green bus's
number. The red bus bounds the gap to **0.25–0.47** and no further: both red frames are **blown**,
and the white type does not separate from the burst at any threshold. Both values sit inside that
band. Recorded in the source as **TRANSFERRED, ARTWORK CONFIRMED DIFFERENT, MAGNITUDE UNVERIFIED**,
with two rows requiring it to keep saying so.

**Three of rev 47's four decal "defects" were measured against the wrong vehicle.** On the RED bus
the build's few long broad spikes and its single left-hand star are **right**; the green bus's many
fine serrations and scattered stars are a different decal — spike depth **0.133 / 0.239** against
**0.044**, a factor no viewing geometry produces.

**And `ref_side.jpg` shows this decal at 99 × 75 px** — 2.7× the area of `IMG_2073`. Both
`LEDGER_rev47.md` §203 ("`ref_playa_34.png` is the only frame … 23 × 39 px") and the brief's "the
best frame in the project" are refuted for this decal.

---

## §7. THE STARS — HIS RULING, AND WHAT IT CORRECTS

> *"They are actually stars that were not properly represented."*

Rev 45 drew **bunting** above the burst. Rev 46 retired it at his instruction **and recorded the
reason as "No frame we hold shows them."** **That reason is false** — `ref_side.jpg` shows the band
plainly at 7×; rev 46 was reading `ref_playa_34.png` at 23 × 39 px, where the marks are sub-pixel.
**Their presence was never the error. Their identity was, and only he could settle it.**

Measured on the target vehicle, window (700,280)–(870,400), mask (R−G) > 26:

```
    the burst      x 733..836  y 306..383   ->  103 x 77 px
    the mark band  x 700..869  y 281..320   ->  169 x 39 px
```

Expressed against the burst (rule 14) and derived from its centre and radius at draw time (rule 2).

**NOT MEASURED, and it is the count.** Both red frames are blown; the band returns as **one connected
1499-px component** at every threshold. `STAR_N = 7` is a pose choice and says so.

**A cap that reports itself.** The measured band runs to ±1.64 RO; the decal's rectangle holds
±1.38 RO. **2 of 7 band positions fall outside the texture** — on the vehicle they are painted on the
body. Clamped, and the number dropped is printed every run. *A silent truncation reads as coverage.*

---

## §8. THE RECORD ITSELF

* **SPEC 10.118–10.121 did not exist.** `LEDGER_rev46.md` §7 said they were *"written into the
  sources"*, which reads as "written into SPEC" and was not. Four load-bearing sections were
  reachable only as comments in three `.py` files, while the brief sends the next context to SPEC for
  everything. **Recovered, with their ceilings and retractions intact.** 10.122 added for this
  revision.
* **`bootstrap.sh`'s header** said the `pip install bpy==4.5.3` branch had **never been exercised**
  while the brief claimed it discharged at rev 47. It has now run on a cold container, ALL 10 PASS,
  watched print — **and the header says so.** A retraction that lands in a ledger and not in the
  source is half a retraction.
* **`verify_clone.sh` still called the vent slats "DARK GREY"** — retracted at rev 47, in the ledger
  only, so the machine went on handing out the retracted reading.

---

## §9. THE STATE OF THE MACHINE

```
bootstrap.sh      ALL 10 PASS   (the pip branch now genuinely discharged)
verify_clone.sh   ALL 101 PASS  (86 at pickup; 15 added, none relaxed)
build             T1_SUB=1, VERIFY: 0 fail, 0 warn
                  length 4.056 vs spec 4.055  (+1 mm, on a fixed instrument)
probes            probe_rev48_louv    11 checked, 0 FAILED
                  probe_rev47_gap      3 checked, 0 FAILED  (was 1 FAILED)
                  probe_rev47_sharp    9 checked, 0 FAILED
                  probe_rev46_vw       5 checked, 0 FAILED
                  probe_rev46_reports  PARTLY RETRACTED -- do not quote
renders           out/r48v_hero34r.png   both rear bays open
branch            claude/combi-render-rev48-ypkd3o
```

**EVERY DISPATCHED TASK RETURNED AND IS RECORDED.** Rev 46 closed with one outstanding and it cost a
whole revision; rev 47 repeated it in miniature. Four agents ran this revision — the brief refuter,
the vent measurement, the LINE_GAP verifier and the raised-panel verifier — **and all four reported
before this was written.** Their findings are §1, §2, §5 and §6.

---

## §10. STILL BLOCKED ON HIM

* **W6 — the paint and the studio.** Body red G/R 0.455 built vs 0.223 ± 0.066 photographed (3.5 σ);
  about half the excess is the white cyclorama's own specular, and softening it trades the clean
  background he set as the bar. **Asked this revision and not yet answered** — he answered the
  vehicle question instead. **It still gates the rest of W3.**
* **The trunk bay's contents.** He chose "fill it as a service bay" and then said *"I trust your
  judgement"*. Nothing is invented yet — see §11.
* **The nose is flat** (W4). 14.3 mm over 0.70 m. Unchanged, still no photographed anchor. Method 2,
  silhouette corner-wrap on `ref_workshop.jpg`, is still the live one.

---

## §11. WHAT THE NEXT REVISION SHOULD DO, IN ORDER

1. **The louvres as APERTURES, not closed ribs.** The lighting-independent half of JOB 2, and the
   `bus_model_ref.JPG` bar. §2.
2. **The trunk bay.** He asked for it dressed as a service bay; this revision built the opening and
   stopped short of inventing contents, because no frame supports any. **Ask him for one frame of the
   open tail** — it settles the bay, the hinge, the open angle and the stay at once.
3. **The second raised panel**, §5 — the build is one short and both red frames show it.
4. **W6**, which gates W3.
5. **One unblown frame of the red bus's decal** — it closes `LINE_GAP` and "the lettering looks off"
   together.
