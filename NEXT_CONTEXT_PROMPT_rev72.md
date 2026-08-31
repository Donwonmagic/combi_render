# NEXT CONTEXT PROMPT — rev 72   ·   **ACTION BRIEF**

**SHORT ON PURPOSE, AND SHORTER THAN REV 71's ON PURPOSE.** Rev 71 measured its own drift at
**doc:geo 35.39 (79 geometry lines, 2796 doc lines, 2 findings closed) against a rev-8-20 baseline of
1.55** — run `python3 revstats.py` and read ITS numbers, not this sentence. *(An earlier draft of this
line said 67:1. It was transcribed, not run. Rule 18, inside the file that carries rule 18.)* Every carrier lives in
`HANDOFF_CARRIERS.md`; every finding lives in `OPEN_FINDINGS.md`; every measurement lives in a probe
that RUNS. **This file is only what to do next. DO NOT GROW IT.**

> *[owner]* **"finish the nose render, make the emblem correct (a bare minimum qualification) and fix
> the opening"** … **"I meant to say the back opening."**
> *[owner, rev 71]* **"The ultimate goal is a 3d render from which to build promotional material
> from."** and **"I certainly want physics closed."**

**THE SECOND PAIR RE-RANKS THE FIRST.** Photo-real parity is in SERVICE of a promotional render.
Do not reach for a grade to hide a physical defect — but where the physics IS closed and the residual
is scene, **say so and stop**, because that is what rev 71 proved about the red.

---
## §0 DO THIS FIRST — THE MACHINE IS IDLE WHILE YOU READ

```bash
cd /home/user/combi_render
./bootstrap.sh                 # the toolchain is NOT on the clone -- this builds it
pip install pillow             # bootstrap FAILS 3 of 10 without it, EVERY revision
nohup setsid env T1_SUB=1 T1_PREVIEW=front,side,hero34f,hero34r T1_PFX=r72 T1_RX=1600 T1_RY=1100 \
  T1_SAMP=96 /tmp/blender/blender -b -P build.py > /tmp/r72.log 2>&1 < /dev/null &
```
**`grep -c Saved: /tmp/r72.log` must be 4.** `setsid`, not a bare `nohup &` (F173). **`out/` starts
EMPTY** — re-render before quoting any frame. **DO NOT EDIT SOURCE WHILE THE QUEUE RUNS.**
Then `./judge_set.sh r72` for the `_post` set (fixed at rev 71, F248).

## §0b **BEFORE YOU MEASURE ANYTHING — THIS IS NEW AND IT IS THE REVISION'S BIGGEST GIFT**

```bash
python3 photometry.py          # 9 checked, 0 FAILED -- FIVE of the nine are KILLS
```
**Rev 71 found SIX defects in its OWN instruments and RETRACTED FOUR PUBLISHED CONCLUSIONS.** Every
one violated a rule of reading a pixel: **read linear** (inverse-sRGB does NOT undo AgX — read through
AgX one ratio moved with EXPOSURE and read 3.43× where the truth is nearer 1.7×); **refuse clipped
data** (a relight was measured to "work" three times and every gain was the denominator clipping);
**median not mean** (a 15 % contaminant tail doubles a dark channel's mean); **paint the window and
look** (four windows were wrong). **`photometry.py` enforces all four. Import it. Do not re-derive it.**

> **⚠⚠ AND THE FIFTH, FOUND LAST AND THE LARGEST OF THE FIVE (F263). EVERY FRAME THIS PROJECT RENDERS
> IS 16-BIT AND EVERY MEASUREMENT EVER TAKEN OFF ONE WAS READ AT 8.** `studio.setup_render` sets
> `color_depth = '16'` and all 50 PNGs in `out/` carry IHDR bit-depth 16 — but **PIL has no 16-bit RGB
> path and truncates silently**: `np.asarray(Image.open("out/phys_side.png"))` returns
> `uint8 max 255`. **The lost precision is the READER, not the renderer** — `F42` recorded it as a
> property of the renderer for fifty revisions. **`photometry.read_png()` is a real decoder** (pure
> `zlib`+`numpy`), validated on a live frame: **its top 8 bits agree with PIL on all 5 280 000 pixels,
> max difference 0**, and it returns the other 8. **Use it for anything that reads a dark channel.
> Nothing else in this tree does yet — `flank_compare`, `gloss_compare`, `probe_rev70_tyre`,
> `probe_rev46_vw`, `cream_rms` and every `probe_rev*` still read through PIL. That is a
> project-wide re-measurement waiting to happen, and it is CHEAP.**

---
## §1 THE BRANCH — MEASURE IT, DO NOT TRANSCRIBE IT, **INCLUDING THIS SENTENCE**

```bash
git fetch --all --prune
for b in $(git branch -r | grep -v HEAD); do printf "%-52s ahead %-3s behind %s\n" "$b" \
  "$(git rev-list --count origin/main..$b)" "$(git rev-list --count $b..origin/main)"; done
git diff --name-only HEAD...origin/main        # <- HIS PHOTOGRAPHS ARRIVE HERE
```
**SEVEN CONSECUTIVE REVISIONS OF STALE BRANCH PROSE (F253), rev 71's stale in the OPPOSITE direction
from rev 70's.** A brief cannot carry a true statement about branch state across a boundary. Believe
`bootstrap.sh` row 9 and the loop above, never this paragraph.

---
## §2 RANKED WORK FOR REV 72

**HOW THIS IS RANKED, STATED SO YOU CAN OVERRULE IT.** The owner's three named items are the emblem,
the back opening and the nose. His NEWEST pair — *"the ultimate goal is a 3d render from which to build
promotional material"* and *"I certainly want physics closed"* — **re-ranks within them, not over
them.** So: the item that SHIPS GEOMETRY comes first (rule 55, and rev 71 shipped one constant);
the item that covers the most delivery pixels comes second; the emblem is third **not because it
matters less but because it is currently BLOCKED on an instrument** (see its precondition), and it is
item 9 of 16 at **3.32e4 px²** against the gloss/flank surfaces at **2.89e6 px² — 87× larger**.
**RE-RUN `python3 visibility_budget.py 3840 out/r72_hero34f.png` AND RE-RANK IT YOURSELF.**

### **1. THE BACK OPENING — `REAR_OPEN_DEG = 64.0` HAS NO FRAME, NO SWITCH AND NO GUARD.**
`t1_shell.py` logs *"OPEN 64.0 deg [angle NOT MEASURED -- no frame shows it]"*. Rev 71 projected
`glass_rear` and painted it (F254): the pane lands at u 1018…1251, v 545…619; the dark rectangle is
u 976…1247, v 545…670, so **63 % of it is the pane and 37 % is the OPEN APERTURE with no pane in
front**. **This is the owner's own words and the most shippable item on the list**: measure the angle
from a frame, or state with its ceiling that it cannot be recovered — and give it a switch and a row
either way, so the pose is at least declared. **See `HANDOFF_CARRIERS.md` §0.05 before you touch
`TB_WIDTH`: a full-width board is REFUTED at >2×, the width has an upper bound of 0.59 m and NO lower
bound, and the shipped 0.5500 is an honestly-labelled POSE CHOICE. DO NOT WIDEN IT.**

### **2. THE PHOTOGRAPH GATES, AUDITED THE WAY THE RED WAS — AND NOW ON A REAL RULER.**
`gloss_compare` **0.411** (bar 0.60) and `flank_compare` **0.689** (bar 0.75) have never been read
through `photometry`, and — like everything else in this tree — **they read their frames through PIL,
so they have never seen more than 8 of the 16 bits that are in the file (F263).** Re-read them through
`photometry.read_png` + `load_linear` first; **the re-read is cheap and it may move the numbers before
you tune anything.** The red turned out physically correct with the residual entirely scene; **expect
at least one of these to be the same, and say so if it is.** This is the item that directly serves
*"a render from which to build promotional material"*: it either finds a real defect or clears the
model for grading.

### **3. THE EMBLEM — AND ITS OBJECTIVE NEEDS A LEGIBILITY TERM FIRST.**
**P4 scored the traced pressing HIGHER than shipped on BOTH frames (+0.0060 / +0.0081) and rendered it
is FRAGMENTED INTO DISCONNECTED SHARDS** (`probe_scratch/rev71_trace_ab.png`, F262). **A silhouette IoU
at ~220 px cannot see fragmentation, so a search run against it can walk toward another shattered
mark** (rule 56). Add connectivity / stroke-continuity to the objective and **WATCH IT REJECT THE
TRACED GLYPH** (rule 3) before trusting it.
> **⚠ THE CEILING ON THAT WARNING, STATED SO IT IS NOT OVER-READ: n = 1.** One construction was
> observed to fool the IoU, and it is the one construction in this tree that is a single filled
> outline with holes. **The SHIPPED glyph is six separate strokes with no mechanism to shatter**, and
> P1b's control reads 0.9146 on it. **So this is a PRECONDITION ON A SEARCH, not a bar on touching
> the emblem at all** — moving a constant and LOOKING at the render (which is what rev 71 shipped)
> needs no new term. Do not let this paragraph cost the revision the owner's #1 item.

### **4. THE NOSE — `probe_rev67_nose.py`'s P3 REFUSES on the render** (fit rms 113.92 px = 12 % of
span). This project still has **no render-side reading of the bumper's edge**. Give it a true elevation
frame or re-cut the row. ⚠ **Bare, that probe prints a GREEN summary and exits 0 while its first line
refuses**, and it builds the whole shell in-process (~74 s). Unfixed at rev 71.
**DO NOT ASK HIM THE NOSE AGAIN — both askings are spent (F214/F215). Check the catalogue literature
first (F229, rule 52); the sources are named in `HANDOFF_CARRIERS.md` §0.06.**

### **2b. AND IF YOU DO NOTHING ELSE, CLOSE THE PHYSICS PROPERLY — IT IS FOUR RENDERS.**
The owner asked for it in his own words. F261 has the right ORDERING and inadmissible FIGURES (§3).
Everything needed to redo it honestly now exists: a real 16-bit reader (F263), and **`T1_DIFFB`**, the
inter-reflection switch that was missing and was why F261 could not be reproduced from any committed
script. The four frames, `Raw` and stopped down so nothing clips:

```bash
C="T1_SUB=1 T1_PREVIEW=side T1_RX=1600 T1_RY=1100 T1_SAMP=96 T1_VT=Raw T1_LOOK=None T1_EXP=-2.5"
env $C T1_PFX=f1shipped                                              blender -b -P build.py
env $C T1_PFX=f2nodiffb T1_DIFFB=0                                   blender -b -P build.py
env $C T1_PFX=f3nospec  T1_DIFFB=0 T1_SPEC=0.05                      blender -b -P build.py
env $C T1_PFX=f4flat    T1_DIFFB=0 T1_SPEC=0.05 T1_CYCALB=0.05 T1_BODY_COAT=0.0  blender -b -P build.py
python3 probe_rev71_red.py out/f1shipped_side.png --transform raw    # then the others
```
**≈4 min a frame.** **AND THE EXPOSURE-INVARIANCE TEST IS THE ACCEPTANCE CONDITION, not an extra:**
re-render one config at `T1_EXP=-1.5` and `-3.5` and the ratio must agree to a few parts in a hundred.
**If it drifts, the read is still wrong and no decomposition off it is admissible** — that is exactly
how F261 was caught. **Publish the invariance figure beside the decomposition.**

---
## §3 WHAT REV 71 CLOSED — **DO NOT RE-OPEN ANY OF IT**

| closed | the result |
|---|---|
| **THE RED / F21's "paint or light"** | **DIRECTION ESTABLISHED, MAGNITUDES WITHDRAWN — READ THIS ROW WHOLE (F261, DOWNGRADED BY F263).** The ORDERING is robust and stands: **specular dominates**, the materials present their authored albedos, the world is inert, the weather chain is inert, inter-reflection is small. **It is one physically-correct specular lobe (F0≈0.04) reflecting a bright uniform studio onto a dark saturated albedo, and the reference photograph is the same bus OUTDOORS IN SHADE — a different scene. That is F21 answered: it is LIGHT, and the light is not wrong, it is DIFFERENT.** **⚠ BUT ITS FIGURES ARE NOT ADMISSIBLE.** They were read through PIL from a frame that is 16-bit on disk, so the red's G channel — about **five code levels of 255** at the stated 2.5-stop stop-down — was quantised to nothing. **The invariance test fails: the same ratio at exposures −1.5 / −2.5 / −3.5 reads 1.60 / 1.53 / 1.39, and a ratio of two albedos cannot drift with exposure in true linear. DO NOT QUOTE 1.73× / 1.63× / 0.91× / 0.99×.** **RE-MEASURING IT IS NOW ONE COMMAND** — `photometry.read_png` exists, `T1_DIFFB` is the inter-reflection switch that was missing, and §2b names the four renders. **Closing this properly is the owner's own explicit ask and it is a SHORT job.** |
| **THE RELIGHT (F259/F260)** | **REFUTED.** `T1_SOFTEN=3.5` reads 1.98× against shipped 1.73× — **worse**. Every apparent gain was the cream denominator clipping. The owner's *"relight the studio"* ruling stands as a ruling; the lever does not work. |
| **THE TRACED PRESSING (F262)** | Builds now, **renders shattered**. F183 stands, and `probe_rev69_fitpose.py`'s **P4 message carries the withdrawal in its own text**, so rule 9 reads it there. **F255 is annotated; do not act on F255 without reading F262.** |
| **"FREE ENDPOINTS" (F252)** | 0.0010 **worse** than the current parameterisation. |
| **THE FIT DEPTH (F251/F256)** | Measured, swept, **SHIPPED at 0.86** — both frames' argmax. |
| **`judge_set.sh` (F248)** | Was exiting 2 and never post-processed the delivery view. Fixed. |
| **THE TAIL-BOARD GUARD (F247)** | Recorded a "watched failure" its own bar would have PASSED. Corrected, re-watched at +95.0 mm / 3.2σ. |

---
## §4 THE MACHINE

```bash
./bootstrap.sh                                # ALL 10 PASS -- read ROW 9
./verify_clone.sh                             # read the verdict block AND the row count
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
python3 photometry.py                         # THE MEASUREMENT PROTOCOL -- run it first
python3 probe_rev71_proxy.py                  # must read IoU 1.000000
python3 probe_rev69_fitpose.py                # the emblem.  P1b PASSES; P2 and P4 fail
python3 probe_rev71_emblem.py                 # the fit depth.  T1_REV71_SEARCH=AB adds the searches
python3 probe_rev71_red.py out/r72_side.png   # the red.  READ ITS PROTOCOL NOTE FIRST
python3 probe_rev71_bulbs.py out/r72_side.png # window MISPLACED -- direction only (F250)
python3 flank_compare.py out/r72_side.png /tmp/fc.png ; python3 gloss_compare.py out/r72_hero34f.png
python3 probe_rev70_tyre.py out/r72_side.png ; python3 probe_rev46_vw.py
python3 visibility_budget.py 3840 out/r72_hero34f.png ; python3 revstats.py
T1_SUB=2 /tmp/blender/blender -b -P audit.py            # rewrites STATE.md -- COMMIT FIRST
python3 audit_brief.py ; python3 audit_adversary.py     # rules 15/17, MECHANICAL half only
```
**FACTS THAT BITE:** `bootstrap.sh` fails 3/10 without pillow. The render is **not** run-to-run
deterministic (floor 2.441 % of pixels >8 levels). `lid_gen.py` / `script_gen.py` are **not** called by
`build.py`. `audit.py` rewrites `STATE.md` — commit first. `ck` in `verify_clone.sh` collapses
whitespace, and its greps **cannot tell a comment from an assignment** — rev 71 tripped one with a
comment. **A backgrounded runner's `rc=$?` is the redirect's; in a pipeline it is `tail`'s.**

---
## §5 THE RULES THAT WILL BITE YOU

Full canon (1–57) in `HANDOFF_CARRIERS.md` §5.

1. **RENDER IT, CROP IT, AND LOOK AT IT.** It killed the trace at rev 71 after the instrument endorsed it.
3. **A control is finished when you have WATCHED IT FAIL on the defect.**
5. **NEVER PUT A FIGURE IN AN ACCEPTANCE TEST UNLESS YOU WATCHED IT PRINT.**
6. **A window that selects for the quantity it reports is a tautology.**
8. **YOU MUST NOT PUBLISH A NUMBER FROM A WINDOW YOU HAVE NOT PAINTED AND LOOKED AT.** Four fell at rev 71.
12. **Report the measurement WITH ITS CEILING.** *"It cannot be recovered"* is a real result.
13. **RETRACT IN THE SAME REVISION YOU FIND THE ERROR.** Rev 71 retracted three of its own.
16. **YOU MUST NOT DELETE A CARRIER.**
42. **A CONTROL MUST BE FRAMED THE WAY ITS MEASUREMENT IS FRAMED** (F246).
44. **WHEN A GUARD GOES RED ON YOUR OWN NEW WORK, THE GUARD WINS.** Three did at rev 71; none was relaxed.
**56. AN INSTRUMENT CAN RANK A THING THE EYE REJECTS, AND IT WILL NOT TELL YOU** (F262).
**57. THE FOUR RULES OF READING A PIXEL — `photometry.py` enforces them.**
**58. NEW AT REV 71 — A LIBRARY CAN THROW AWAY HALF YOUR DATA WITHOUT RAISING ANYTHING.** PIL
   truncates a 16-bit RGB PNG to 8 bits silently, and this project rendered 16-bit and measured 8
   for fifty revisions (F263). **Check what your reader actually returned — dtype, max, shape —
   before you trust a number off it**, and prefer a decoder you can control on a known file.
55. **EVERY REVISION SHIPS A VISIBLE CHANGE TO THE VEHICLE, OR SAYS PLAINLY WHY IT COULD NOT.**

**RANK BY PIXELS OF THE DELIVERY FRAME** before you choose — `python3 visibility_budget.py 3840
out/r72_hero34f.png` — **but the owner outranks the ranking.** The ranked list is
`REMAINING_WORK_rev61.md`, triaged into `ROADMAP_rev68.md`.

---
## §6 WHERE EVERYTHING ELSE LIVES

| file | what it holds |
|---|---|
| **`HANDOFF_CARRIERS.md`** | every carrier: the goal, the reference set, §2's refuted emblem routes, §4 the owner's rulings, §5 rules 34–57, the horizon |
| `OPEN_FINDINGS.md` | the register. **F246–F264 are rev 71's.** It outranks prose. **F261 is `PROVENANCE-REFUTED` — read its middle column before quoting it** |
| `STATE.md` | machine-written; outranks every prose description |
| `LEDGER_rev71.md` | what rev 71 did, **and §4, what it got wrong in its own work** |
| `photometry.py` | the measurement protocol, with a selftest |
| `SPEC.md`, `REF_MEASUREMENTS.md`, `SURVEY_rev49_photoreal.md`, `ROADMAP_rev68.md`, `PANEL_rev61.md`, `PHOTOS_WANTED_rev49.md`, `PHOTOS_WANTED_rev52.md`, `EMBLEM_HANDOFF.md` | large; load the one the task needs |

**⚠ IDs THIS BRIEF LEANS ON WITHOUT NAMING, SO A GREP FINDS THEM (rule 16): `F245`** rev 70's chord
retraction, **`F242`** the hatch angle being a POSE not a dimension, **`F134`** the bulbs' null,
**`F240`** the red's earlier branches, **`F21`** paint-or-light, now answered by F261.

---
## §7 HOW TO CLOSE

**HIS STANDARD:** photo-real parity with **that exact bus**, in service of a promotional render. **Any
single measurement off is unacceptable** — per-measurement, not on average. **Never call it done off
self-review. Report the measurement with its ceiling. Do not say anything is ready.**

1. `./bootstrap.sh` and `./verify_clone.sh` all-PASS on a **clean** tree.
2. `python3 revstats.py` — **put its geometry/closure line in the ledger header, and if the revision
   shipped nothing, say so at the top.**
3. Regenerate `STATE.md` (`T1_SUB=2 … audit.py`) — **commit first**.
4. **DISPATCH an adversary at the brief you WROTE (rule 17).** At rev 71 the outgoing adversary
   **reversed the revision's central conclusion** and unblocked the owner's #1 item.
5. **Keep the split, and KEEP THIS FILE SHORT.** `cp` it over `PASTE_INTO_CLAUDE_CODE.txt` in the
   same commit.
