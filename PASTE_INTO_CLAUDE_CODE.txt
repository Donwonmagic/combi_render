# NEXT CONTEXT PROMPT — rev 61

## §0.0 DO THIS FIRST — THE WHOLE DECISION, IN TWENTY LINES

**Before you read another word, put the machine to work. It is CPU-bound and idle right now.**

```bash
cd /home/user/combi_render
./bootstrap.sh                 # the toolchain is NOT on the clone -- this builds it
nohup env T1_SUB=1 T1_PREVIEW=front,side,hero T1_PFX=r61 T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
  /tmp/blender/blender -b -P build.py > /tmp/r61.log 2>&1 &
```

`out/` is untracked and **starts EMPTY** — it did at rev 59 and rev 60, whatever any handoff says.
**`bootstrap.sh` first**: at rev 58, 59 AND 60 `/tmp/blender/blender` did not exist and `bpy` was not
importable, and the script rebuilt both from nothing. Then start the render, then read.
**`grep -c Saved: /tmp/r61.log` must be 3** — a backgrounded runner's exit code is the redirect's.

**READ `GAPS_rev60.md` BEFORE THE WORK LIST.** The owner asked for it by name at rev 60: the whole
render-against-photograph gap review, graded MEASURED / OBSERVED / REFUTED. §6 of that file is the
recommended order and this §0.0 is its short form.

**THE OWNER'S REV-58b RANKING IS NOW FULLY WORKED. TWO CLOSED, TWO REFRAMED.**

| # | do | state at close of rev 60 | gate |
|---|---|---|---|
| **A** | **THE DOOR** | **FIXED AT REV 59.** 0.1 mm | `probe_rev59_door.py` M2 **PASSING** |
| **D** | **THE GROUND SHADOW AND UNDERBODY** | **BUILT AT REV 60, PARTLY CLOSED.** Cavity 0.545 → **0.219** against a photographed 0.057; the residue is the ruled-in studio | `probe_rev45_ground.py` **G4, PASSING at 0.2519** |
| **C** | **THE EMBLEM — still an X** | **NOT FIXED. CAUSE LOCALISED at rev 60** to the CONSTRUCTION: the V and W are each ONE mitred polyline and they fuse into two diagonals. **Three hypotheses refuted — do not re-try them** | `probe_rev46_vw.py` C6, **watched failing** |
| **B** | **THE NOSE BREAK — 73 mm on the red-bus ruler, but F75's HONEST BRACKET IS 50–80 mm, best single estimate 52 mm** | **NOT FIXED. THE WHOLE REMEDY PROGRAMME IS REFUTED at rev 60** — `V_POW`, `V_RISE` and `V_POW_Z` all fail to move the feature | `probe_rev59_nose.py` M1, **watched failing** |
| **E** | **THE INTERIORS** | **F45 REFUTED AS WRITTEN.** The real defect is CHROMA (F99) and its cause is not separable from one frame | none — and that is a finding |

**THE ONE THING TO PUT TO HIM, as multiple choice with the two crops attached:**
**F111 — ARE THE SERVING BAYS GLAZED OR OPEN?** `ref_side.jpg` shows all three carrying glass with
clear reflections; `ref_nolita_doorshut.jpg` shows the same three open. Both are the red target bus;
the panels evidently lift out for service. The model builds them OPEN. **No gate can settle this —
it is a ruling.** *Do not re-ask anything in §4.*

**AND DO NOT ASK HIM THE TWO REV 60 DRAFTED.** **F99** was measured on the doorshut frame, which is
a DIFFERENT STATE of the vehicle — on the target's own frame the render is within 2 % (rule 11), and
**F100**'s "gold surround" is that state's too: in `ref_side.jpg` the surround is the beaded bulb
string the model already builds (F112).

**RANK BY PIXELS OF THE DELIVERY FRAME**, `python3 visibility_budget.py` — **which was repaired at
rev 60 and is worth trusting for the first time**: it had named a frame that cannot exist, so it
always reported a FALLBACK scale, and its table omitted three of the owner's own five items.

---

**Now read this whole file before you CHANGE anything.** Then `GAPS_rev60.md`, then `CLAUDE.md`,
then `LEDGER_rev60.md` (where every number in §2 comes from), then `OPEN_FINDINGS.md`.

---

## §0.05 THIS BRIEF WAS AUDITED AGAINST THE MACHINE — AND WHAT THE AUDIT FOUND

**Rule 17: audit the brief you WRITE, not only the one you receive.** Both halves ran as scripts;
the run is recorded at close of rev 60.

**AND THE REV-60 LESSON IS RULE 36's, EARNED THREE MORE TIMES.** *Ablate the thing you are about to
tune, FIRST.* Rev 58 and rev 59 both proposed inverting nose constants that four renders now show
**do not move the feature at all**. Rev 58 proposed two emblem fixes that make the topology **worse**.
**Every one of those proposals would have been shipped on a plausible argument.**

**AND FOUR OF MY OWN INSTRUMENTS WERE WRONG THIS REVISION, WHICH IS NORMAL HERE (rule 4).** A G4
window that walked up from the wrong contact patch onto the **"Tacombi" lettering** and printed a
believable **0.3134**; a px/m fit that locked onto body red **around a person standing in front of
the wheel**; a red mask that swallowed the **mural lid** and
reported 1.972 m of red on a body 1.5 m tall; and a contiguous-run edge finder cut short by the
**silver script**. **Every one caught by PAINTING THE WINDOW AND LOOKING. None by reasoning.**

---
## §0. THE GOAL, AND HOW FAR OFF IT WE ACTUALLY ARE

**CARRIED FORWARD FROM THE REV-55, 56, 57 AND 58 BRIEFS. It is not mine and it is not to be
dropped — rule 16.**

**PHOTO-REALISTIC PARITY WITH THAT EXACT BUS.** Not "a convincing VW bus" — *that one*, the red
Señor Tacombi combi in the frames on this repo. **Any single measurement off is unacceptable,
per-measurement and not on average.** A model right in ninety places and wrong in one is not 99 %
done, because he will look straight at the one. **At rev 58 he did exactly that, at the emblem,
for the fifth time, while every automated check was green.**

**AND HERE IS THE HONEST DISTANCE.** `verify_clone.sh` ends **ALL 266 PASS** and its own verdict
block says what that is worth: **0 FIDELITY, 266 SELF-CONSISTENCY. Not one of those rows compares
the vehicle to a photograph.**

| gate | state MEASURED at close of rev 60 |
|---|---|
| `flank_compare.py` | **runs, FAILS.** Worst region **`i` at 0.685** against a 0.75 bar; `Senor` **0.720**. *(The rev-58 table said `Senor` 0.651 and rev 60 found that BOTH stale AND contradicted by this same brief's §9 — re-measured live.)* The deficit is the **artwork alpha and its placement**, not the render (F39) |
| `mottle_measure.py` | **runs, and it is NOT measuring the mottle** — 1.1–2.0 % of it. Rev 56's reading and rev 57's item B are REFUTED |
| `gloss_compare.py` | **runs, FAILS at 0.436** (bar 0.60, measured at rev-60 close; it was 0.426 at rev 58). Mask corrected at rev 58 (F59); the model-side lever is now **exhausted** (F60/F62) |
| **`probe_rev46_vw.py`** | **NOW FAILS C6, and that is the point.** photograph 7 cream cells, built 6. It reported 0 FAILED for three revisions while the glyph was an X |
| `cream_rms.py` | `run()` is the LIVE re-based path |
| the badge STROKE WEIGHT | **CEILED-rev57.** Different finding from F63 |
| `visibility_budget.py` | the RANKING, not a gate |
| everything else | self-consistency |

**The frame reads as clay and the cause is the environment, not the shaders** — the surround is a
featureless white cyclorama, so the paint has nothing to reflect. **He was shown that, told the
cost, offered four routes, and ruled "keep studio, fix the model".** **Rev 58 MEASURED that
ceiling** (F62): this flank's specular image is white cyclorama **19.3 m** away. **Do not
re-litigate it.**

### §0.1 THE REFERENCE SET IS COMPLETE, AND IT IS GUARDED FRAME BY FRAME

> *[owner, rev 54]* **"we have all references that we need on repo and I want to make sure that is
> never forgotten."**

**ONE: WHAT WE HOLD IS WHAT WE GET. STOP PARKING WORK BEHIND A PHOTOGRAPH.** `PHOTOS_WANTED_*` is a
wish list, not a gate — carry it (rule 16, and items 1–5 are still not to be re-asked) but **do not
let it license parking an item.** Where a frame genuinely cannot answer, the result is *"it cannot
be recovered from what we hold"* — a real result, stated with its ceiling. **Rev 58 produced two:**
the residual gloss gap (F62) and the photograph's inability to resolve the V/W centre gap at 68 px.

**TWO: THEY CANNOT BE RE-SHOT, SO THEY ARE CHECKSUMMED INDIVIDUALLY.** **18 rows name them one at a
time**, so a loss says *which*:

* **the RED target bus** — `ref_side.jpg`, `ref_rear34.jpg`, `ref_playa_34.png`,
  `ref_nolita_front34.jpg`, `ref_nolita_front34b.jpg`, `ref_nolita_flank.jpg`,
  `ref_nolita_doorshut.jpg`
* **NOT the target, geometry only** — `ref_workshop.jpg` is the **GREEN** vehicle; **`IMG_2073.jpeg` is ALSO
  the GREEN vehicle and was MISFILED under the red bus in this very register until rev 58 measured it**
  (body **G−R +21.7** on the lower flank and **+28.5** on the rear quarter, against `ref_side.jpg`'s **−67.6**);
  `bus_model_ref.JPG`
  is a **SCHOOL BUS**, a fidelity bar only. **Paint and artwork do not transfer between vehicles;
  geometry does (rule 11).**
* **retired** — `ref_source.jpeg`, a 246×197 thumbnail the record itself retired
* **derived/annotated** — `ref_grid.png`, `ref_side_grid.png`, `ref_nose_grid.png`,
  `ref_band_grid.png`, `ref_x6_lanczos.png`
* a **floor of 54** reference-class tracked images, and **the five byte-identical pairs are asserted
  to stay five** — a sixth group means a frame arrived that duplicates one we already hold, which is
  **not corroboration** and has fooled this project before (rule 11).

---

---

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
./bootstrap.sh          # 9 of 10 at rev 60 close.  MEASURE IT ANYWAY
./verify_clone.sh       # ALL 266 PASS in ~70 s -- and read its verdict block
```

**AT PICKUP, REV 60 MEASURED.** HEAD was `claude/new-session-ocymb5`, **0 ahead / 0 behind**
`origin/main`, tree clean, `git diff --name-only HEAD...origin/main` **empty**. Rev 59's work was
already merged. **That is the SIXTH revision running in which the prose guessed the merge state and
the machine corrected it** — the incoming handoff said HEAD was 13 ahead and that rev 58/58b were
unmerged; they were merged through PR #18.

**AND THE TENTH DELETION HAPPENED, ON SCHEDULE.** `fetch --prune` printed
`- [deleted] (none) -> origin/claude/new-session-ocymb5` — **the branch rev 60 was told to develop
on**, deleted before rev 60 had pushed anything, the **FIFTH RUNNING** to hit the current revision's
own branch. It was recreated by the first push. **Expect it at rev 61.**

**AND `out/` WAS EMPTY.** Render before quoting any probe.

**ROW 9 WAS RED AT PICKUP AND IS GREEN AT CLOSE, AND I DO NOT FULLY KNOW WHY — SO MEASURE IT.**
At pickup `bootstrap.sh` ended **9 PASSED, 1 FAILED**:
`STRANDED: origin/claude/bus-model-rev57-yvrlhi(6 commits, 16 files)`. At close it ends
`bootstrap.sh` **ALL 10 PASS**, and an independent loop — `git rev-list --count HEAD..$b` —
finds **no branch ahead of HEAD**. Rev 60 did not merge anything, so the most likely explanation is
that the pickup reading was taken against an incompletely-fetched remote. **THAT IS A GUESS AND IT IS
LABELLED ONE.** Run row 9 yourself and believe the output, not this paragraph — it is the row this
project says must never be ignored, and it has been wrong in both directions now.

**RE-MEASURE BEFORE YOU FINISH, TOO.** `origin/main` moved mid-revision at rev 51 and rev 55.

---

## §2. WHAT REV 60 DID

**Every figure below is in `LEDGER_rev60.md` with its provenance, and the whole gap picture is in
`GAPS_rev60.md`. Nothing here is transcribed.**

### §2.1 ITEM D — THE UNDERBODY, BUILT (F67)

The defect, measured before anything was built: a vertical profile between the wheels showed the
render's body edge followed **immediately** by rising ground — **no cavity at all** — where
`ref_side.jpg` has a **forty-row band at 8.5 DN**. Cause: `body_paint` drives the two-tone off
object-space z, so the shell's bottom face at `ZB` sat below the belt line and was painted **body
red**, sampling (159, 117, 112).

Built: `t1_detail.underbody()` — a notched pan, two chassis rails, an end ramp at each end — on a new
`M["underseal"]`.

```
cavity floor / open ground   0.545 -> 0.352 (pan) -> 0.219 (underseal)   photograph 0.057
probe_rev45_ground G4        0.5475 ablated -> 0.2519 built
```

**PARTLY CLOSED WITH ITS CEILING**: the residue is the white cyclorama filling a 90 mm cavity, the
same ceiling as F62. **`UNDER_DROP` 0.090 m is a STATED ASSUMPTION** under a measured ceiling of
**0.137–0.155 m**, threshold-dependent — corrected in the same revision (rule 13) — the photograph's band contains both the metal and the shadowed ground and cannot separate
them. **A low raking shot under the sill is the new frame that would settle it.**

**C5 was watched failing at 0.5475 before it was watched passing** (rule 3), and `verify.py`'s length
row caught the pan's first aft end protruding **205 mm** past the vehicle's fixed bodywork limit.

### §2.2 ITEM C — THE EMBLEM: THREE REFUTATIONS AND THE CAUSE (F101–F105)

**DO NOT RE-TRY ANY OF THESE:**

```
the 18.9 mm float   T1_VW_CAPMIN=1            cells 6 -> 2
                    + T1_VW_PUREFIT=1         cells 6 -> 4      BOTH WORSE
stroke weight       ink fraction 0.5903 built vs 0.6062 photographed
                    T1_VW_WFRAC 0.1986 -> 0.48   cells 6 at EVERY value
the six constants   T1_VW_CELLSOLVE, 2000 pts  7 cells only at residual 0.2498 (bar 0.045),
                                               and it collapses to 6 at the photograph's own scale
```

**THE CAUSE, and painting the counted cells is the only reason it was found:** the photograph's cream
is **seven long thin SLIVERS**, the build's is **four fat WEDGES**. The V's arms and the W's outer
arms **fuse into two long diagonals crossing at the centre** — the X itself. **The V and the W are
each built as ONE mitred polyline, fused at the apex. That is what has to change.**

**And C6 compares two rasters at different scales** (F105) — photo at 41×69, built at 276 rows. The
built count is stable at 6 from 55 to 552 rows, so the verdict stands, but at the photograph's own
scale the built glyph reads **4**, so **C6 understates the deficit**.

### §2.3 ITEM B — THE NOSE REMEDY PROGRAMME IS REFUTED (F106/F107)

```
V_POW   0.15 / 0.60 / 1.20     ->  1.174 / 1.187 / 1.170 lamp radii   (r60_front)
V_RISE  0.8670 / 0.9800        ->  1.174 / 1.165
V_POW = V_POW_Z, 0.60 / 0.30   ->  1.175 / 1.178
```

**An 8× sweep of `V_POW` moves the break by 0.004 lamp radii.** The switches are **not inert** — the
extreme arms differ over **128 421 pixels** and an inboard column's cream boundary moves
**808 → 900 px**. The change is real, large, and lands at the V's **apex**, where it does nothing for
the lamp. **So rev 58's "`V_POW` needs 0.345 at the lamp" is refuted.**

**A two-constraint analytic solve WAS built and then THROWN AWAY, not reported.** It predicted a
break of **0.604** lamp radii where the machine measures **1.187**. A hand-written copy of a node
graph that the machine contradicts by 42 mm is not a solve, and shipping constants from it would have
been a fabricated fix. **Do not rebuild it: solve against the SHADER, or against renders.**

### §2.4 ITEM E — F45 IS NOT REPRODUCIBLE (F98/F99/F100)

| statistic | render | photograph |
|---|---|---|
| interior ÷ exterior cream | **0.705** | 0.774 |
| relative std in the bay | **0.161** | 0.060 |
| edge density, matched 72×72 | **0.231** | 0.200 |

Two of the three point **the other way**, and the comparison is **CEILED** by a 480×320 JPEG against
a 1600 px render. **What survives is CHROMA as a within-frame ratio: interior÷exterior R/B is 1.201
photographed against 0.864 built, a net 1.39×** (F99). **Three causes fit and one frame cannot
separate them** — a deliberately-neutral `GAL_WHITE`, no warm interior practical, or the surround.
**NOT FIXED deliberately: W6 makes colour his call, and warming a paint constant to absorb what may
be a lighting defect is laundering.**

### §2.5 THE CHEAP ROWS, AND A GUARD I BROKE

* **F85 CLOSED.** `gloss_compare.py` no longer writes into tracked `probe_scratch/`.
* **`visibility_budget.py` WAS NEVER MEASURING.** It named `out/r57_hero.png`, a revision-numbered
  frame that cannot exist on a clone, so it **always** took its except branch and **always** reported
  a FALLBACK scale while printing a table that reads like a measurement (rule 37). **And its table
  omitted three of the owner's own five items** while ranking the CEILED gloss row first.
* **I BROKE A BY-VALUE GUARD AND IT CAUGHT ME.** The first `T1_VPOW` cut took out all three
  `^V_POW = 0.60` rows — the three the rev-60 brief warned about **by name**. The literal is back on
  its own line with the override below it. **An ablation that disarms a by-value guard is a
  regression.**

### §2.6 REFUTED AT REV 60 — INCLUDING TWO OF MY OWN

* *"the interiors are untextured white blocks"* — **NOT REPRODUCIBLE** (F98).
* *"the W's outer arms float, and that is the cause"* — **SYMPTOM** (F101).
* *"the emblem is a stroke-weight problem"* — **NO**, ink fraction 0.5903 vs 0.6062 (F102).
* *"`V_POW` needs 0.345 at the lamp"* — **NO** (F106).
* **MINE:** *"the flank two-tone break sits too low"*, from a side-by-side — **REFUTED BY MY OWN
  MEASUREMENT**: **RETRACTED AGAIN at rev 60b (F110)** — that instrument was on the mural lid and the script. Settled: model 0.8745 m from its own constants against a photographed 0.863 ± 0.014 m, **+12 ± 14 mm, no resolvable gap**.
* **MINE, AND THEN REFUTED AGAIN AT REV 60b (F108):** I refused the wheelbase's 210 px/m in favour
  of **258.6** from "the rear tyre's own width". **There is no tyre in that window** — the tyre and
  the arch shadow above it are contiguous and no threshold separates them. The scale is **211.6 px/m**
  from a circle fit to both cream rims (rear rms 1.11 px over 828 points), and the rear rim images
  ROUND, so there is no foreshortening to justify the refusal either. **The route I refused was the
  right one, and every metric figure I took off that frame carried a 23 % error.**
* **§2b of the rev-52 brief — HIS SETTLED RULINGS — IS UNCHANGED AND STILL BINDING.** W6; the roof
  strips' 0.3 m retired; the wipers withdrawn entire; the lower bay SHUT; the RED bus is the target
  and **paint and artwork do not transfer between vehicles**; the tail board IS on the vehicle; the
  marks above the burst are STARS. **Do not re-open or re-ask any of them.** `playa_env.py` is not on
  the table. **And rev 54's ruling stands: "Keep studio, fix the model".**

---

## §3. THE WORK LIST FOR REV 61

> **`GAPS_rev60.md` §6 is the ranked order and it is the owner's own list worked through. This
> section says HOW.**

### §3.1 ITEM C — THE EMBLEM. His top item, and rev 60 handed you the cause.

```bash
T1_SUB=1 /tmp/blender/blender -b -P probe_rev46_vw.py                 # C6 FAILS: photo 7, built 6
T1_SUB=1 T1_VW_DUMP=1 /tmp/blender/blender -b -P probe_rev46_vw.py    # PAINT the cells. LOOK.
```

**REV 60 PRESCRIBED THE WRONG FIX HERE AND REV 60b CAUGHT IT (F113).** It said *"a construction that
keeps them as separate strokes is the next thing to try"*. **`t1_core.vw_bars`' own docstring says
that construction WAS tried and produced an X** — grep `This was six independent overlapping bars`:
*"rev 8 … six independent overlapping bars … at hero resolution the V and the W merged into an X"*.
And the centre fusion it would open is one the photograph shows CLOSED — grep
`A TOUCH at the centre does match`. **Do not un-fuse the glyph and do not go back to separate
objects.**

**WHAT IS ACTUALLY UNTESTED IS THE ANGULAR SPACING OF THE SIX TERMINALS** (F114). Reach is refuted
(F101), weight is refuted (F102); the measured defect — seven thin SLIVERS photographed against four
fat WEDGES built — is a statement about **where the six stroke ends sit around the ring**, and that
axis has never been swept. The docstring carries the angles it was built from (*"V arm -40.75 deg,
W inner -53.04 deg"*). **Sweep those through C6's cell count, exactly as rev 60 swept `V_POW`
through M1.** If no angular arrangement reaches 7 substantial cells at the photograph's own scale,
**say so with the number**; that is a real result.

### §3.2 ITEM B — THE NOSE. Three candidates, and the ablations are already in the tree.

```bash
python3 probe_rev59_nose.py out/r61_front.png     # M1 FAILS: 1.185 vs 1.951-2.121
```

**Sweep each through M1, exactly as rev 60 swept `V_POW` — one render each:**
1. the hard-coded **0.860** divisor in `body_paint`'s `u = |y| / 0.860`;
2. `tblend`'s **1.858 → 2.012** smoothstep, which is on **X** and clamps to 1 well before the lamp;
3. `HL_DROP` — the other side of the ratio, refuted at rev 58 on a **2σ** conflict, so it needs that
   conflict re-measured before it can be used.

**`T1_VPOW` and `T1_VPOWZ` exist now and must move TOGETHER** or `verify.py` fires
*"V_POW de-registered"* — which is correct behaviour and was watched.

### §3.3 F99's CONTROL — a MEASUREMENT, so it does not need him first

Add a warm interior practical, re-render, re-measure interior÷exterior R/B. If the interior warms
without touching paint, the cause is lighting and `GAL_WHITE` is exonerated. **That separates the
three candidates and it is the only thing that can.**

### §3.4 F93 — THE TEXTURES. Mechanical, ungated, and it CAPS the delivery frame.

**ONE of EIGHT** textures meets SPEC §5's 3K floor. Two are **1024×1024**. A 3840-wide delivery frame
cannot be sharper than the textures in it. **This is the finish line's blocker and nobody has touched it.**

### §3.5 F91 — THE TAIL AND THE ROOF HAVE NEVER BEEN HELD UP AGAINST A PHOTOGRAPH

Two thirds of the owner's own standing bar, never done. `ref_rear34.jpg` exists.

**AND THE REV-60 AUDIT ARGUES THIS SHOULD RUN EARLY, NOT FIFTH.** Every other
item on this list works a defect that is already KNOWN and already gated. This
is the only one that can find an UNKNOWN one, and it is cheap — one render, one
matched-scale crop, one look. Rev 51 did exactly this for the NOSE and it found
**three real defects by eye alone** (flush headlamps, the roundel's short
V-arms, a flat nose) that no gate had ever reported. The tail and the roof have
had no such pass in sixty revisions. **If the goal is parity rather than
closing tickets, an hour here probably buys more than an hour anywhere else on
this page.** Do it before, or alongside, item C — not after.

### §3.6 THE ROWS CARRIED FORWARD, STILL OPEN

* **F45's roof-aperture interior** was never separately measured — F98 covers the galley bays only.
* **F83** the front arch's 4.4 mm departure — **CEILED, and the owner ruled "leave it circular"**.
* **F14** `gal_end_f`'s sight lines — **rev 52, EIGHT revisions un-re-measured**.
* **F10** the galley's ~103 mm — provenance INHERITED, not re-measured since rev 52.
* **F18** the die-cut sticker — the original deliverable, open since rev 44.
* **F42** the 8-bit reader; **F05** the beauty arm, cheap now that F51 is fixed.
* **SPEC §8's colour locks** are graded M off a **retired 246×197 thumbnail**. Re-derivable on
  `ref_playa_34.png` at 4× the area. **Report the values; W6 makes the change his call.**

### §3.7 THE HABITS THAT PAID AT REV 60

**ABLATE THE THING YOU ARE ABOUT TO TUNE, BEFORE YOU TUNE IT.** Four renders killed a remedy
programme two revisions had been building toward. **It is cheaper to disprove a lever than to ship one.**

**PAINT THE WINDOW AND LOOK AT IT.** Four wrong instruments this revision, every one caught this way
and none by reasoning — including one that reported 1.972 m of red on a body 1.5 m tall.

**RUN YOUR INSTRUMENT ON A CASE WHOSE ANSWER YOU KNOW.** The emblem's cell count was compared across
scales and the built glyph reads 4 at the photograph's scale, not 6.

**IF THE MACHINE CONTRADICTS YOUR MODEL, THE MODEL IS THE SUSPECT AND YOU DO NOT PUBLISH IT.** The
nose solve predicted 0.604 where the machine measures 1.187. It was thrown away.

**A GUARD THAT REFUSES YOUR CHANGE MAY BE RIGHT.** `verify.py`'s length row caught a 205 mm
protrusion the eye had already missed once.

---

## §4. WHAT WAS ASKED OF HIM — A CARRIER, NOT A LIST OF BLOCKERS

> **READ §0.1 FIRST.** At rev 54 he ruled that **the reference set on the repo is complete**. This
> section is kept in full because `CLAUDE.md` rule 16 forbids dropping a carrier, and because it
> records what was asked and what was refused — which is why items 1–5 must never be re-asked.
> **But it is no longer a licence to park work.**

**`PHOTOS_WANTED_rev52.md` is the carrier for item 7 (ONE HUBCAP, SQUARE ON AND CLOSE)**. Items
**1–5** keep their full text in `PHOTOS_WANTED_rev49.md`: the tail board's footing; the decal darker;
the nose square on; a raking-light frame of the louvres (**ONE item — the pressing depth**); the off
side, any frame. **He has said 1–5 are not possible now. DO NOT RE-ASK THEM.** Item 6 (an obliquely
seen wheel) was **DISSOLVED at rev 51** — struck, not outstanding.

**CARRIED FROM REV 53, still no carrier outside these briefs:** a frame showing the cream **where it
IS chipped**. Rev 54 and rev 55 both lowered its urgency; the band is 0.27 px at every scale this
project ships, and the gate that would place those chips is not built.

**ANSWERED AT REV 56 AND NOT TO BE RE-ASKED:** `lid_rail`'s width — *"narrow lip, ~as wide as it is
tall"*.

**ASKED AND ANSWERED AT REV 58:** the roughness/chroma trade — **"ship 0.250"** (F60). That is the
only thing put to him, and it was put as multiple choice with the crop attached.

**ASKED AND ANSWERED AT REV 59 — THREE RULINGS, NONE TO BE RE-ASKED.** All three were put as
multiple choice with the crops attached, in one batch:
1. **the stranded rev-57b branch** — ***"Merge it, renumber its IDs."*** Done; F88–F97; row 9 green.
2. **the studio** — ***"Keep studio — ruling stands."*** Put to him WITH F62 and F86 and the
   headlamp crop. **F80's headlamp gap is ceiled to the surround; F86's red/cream level is not.**
3. **the front arch** — ***"Leave it circular."*** **Do not build it and do not mirror it.**

**AND HE VOLUNTEERED TWO INSTRUCTIONS AT REV 58, BOTH BINDING:** the emblem needs a fix (F63, item
A), and **the full delivery render waits until the model is right.**

**STILL WORTH HIS TIME AND NOT ASKED:** **F38** — the built nose ring band sits at the top of its
adopted range (0.10086 against three frame readings at 0.087–0.093), and moving it moves the glyph's
fit radius with it, **which now interacts with F63**; and **F39** — `Senor`'s ink deficit is in the
artwork, which A12 makes his call. **Decide whether to ask. Do not simply carry them.**

---

---

## §5. THE RULES — `CLAUDE.md` CARRIES THE METHOD, NOT THE NUMBERED CANON

The canon (rules 1–33) is printed in `NEXT_CONTEXT_PROMPT_rev50.md` §11. **Rules 34–36 live only in
the rev-51…58 briefs and `LEDGER_rev50.md` §0, so they are carried here too — that is `CLAUDE.md`'s
own rule 16 firing on this file:**

> **34. A REQUIREMENT INHERITS ITS OBJECT EXACTLY AS A RETIREMENT DOES.** Before relying on any
> *"the record requires X"*, check which object the sentence is about — and check the cited line
> exists. **Rev 56 applied it to a CAMERA**: `flank_compare.py`'s header attributes a recovered
> camera position to `ref_side.jpg` that `studio.py` attributes to the PLAYA frame — the same three
> numbers in two places about two photographs (**F26, still open**). **Check it before any future
> work leans on that camera — item B does.**

> **35. A GUARD WRITTEN AGAINST A POSE ENCODES THAT POSE.** Guards that identify a part's foot or
> free edge by `min(y)` are only right while the part leans one way. Ask the geometry.

> **36. A GATE ONLY COUNTS FOR WHAT IT CAN SEE — ABLATE THE THING YOU ARE ABOUT TO TUNE, FIRST.**
> Earned at rev 57 and it cost that revision's item B. **Rev 58 extends it: a gate can be blind to a
> whole AXIS, not just to one constant.** `probe_rev46_vw.py` fits vertical landmarks and reported
> 0 FAILED for three revisions while the glyph was an X, because reach is a radius and every
> landmark it owns is a row (**F64**). **When you build a gate, write down which axes it does NOT
> see.**

> **37. NEW AT REV 58 — AN ABSENT INPUT MUST NEVER READ AS A MEASUREMENT.** `gloss_compare`'s
> missing default frame came back as `MOVED: []`, i.e. *"the estimator moved"*, and pointed the
> reader at the statistic instead of the path (**F58**). A probe that cannot run must say **"NO
> RENDER"** in those words and exit non-zero. **And a check whose input lives in an untracked
> directory passes only in the tree that wrote it.**

> **Rule 29.3:** no finding is attributed to a cause until a control separates it. **Rule 15:** a
> retraction that lands in a ledger and not in the source is half a retraction — **rev 58 retracted
> F47 in `t1_mats.py` itself.**

---

## §6. THIS MACHINE

```
cores 4   RAM 15 GB   Blender 4.5.3 via pip install bpy   subagent concurrency 2
build  T1_SUB=1 ~20 s     render 1600x1100 96 spp ~4.5-5.5 min PER VIEW
mottle_measure.py (albedo arm, 64 spp) ~4.8 min PER RUN -- budget ablations in fives
```

```bash
./bootstrap.sh                                               # THE TOOLCHAIN IS NOT ON THE CLONE
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
T1_PREVIEW=front,side,hero T1_PFX=r61 T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
  /tmp/blender/blender -b -P build.py     # ALL THREE views, ONE build.  It takes a LIST.
T1_RIG=1 ... /tmp/blender/blender -b -P build.py             # rev 58: build the rig WITHOUT a preview
T1_NORIG=1 ...                                               # the ABLATION -- assert_lit must REFUSE
T1_SUB=2 /tmp/blender/blender -b -P audit.py                 # rewrites STATE.md -- COMMIT FIRST
python3 lid_gen.py                                           # regenerates tex/lidmural.png
python3 flank_compare.py out/r61_side.png /tmp/fc.png        # GATE 1.  worst region i 0.685.
python3 gloss_compare.py out/r61_hero.png                    # GATE 3.  FAILS at 0.436 today.
#   ^ F85 is CLOSED at rev 60: the painted tiles go to out/ now, so running the
#     gate no longer dirties the tree.  T1_GL_TILES=track restores the old
#     destination if you deliberately want to refresh the committed tiles.
python3 probe_rev59_door.py out/r61_side.png                # ITEM A.  M2 PASSES, M3 fails BY DESIGN.
python3 probe_rev59_nose.py out/r61_front.png               # ITEM B.  M1 FAILS: 1.185 vs 1.951-2.121.
T1_SUB=1 /tmp/blender/blender -b -P probe_rev45_nose.py     # 8 checked, 0 FAILED -- and read F86.
python3 gloss_compare.py --selftest                          # exposure invariance, NO frame needed
python3 visibility_budget.py 3840                            # THE RANKING.  Run it before choosing.
T1_SUB=1 /tmp/blender/blender -b -P probe_rev46_vw.py        # ITEM C.  C6 FAILS: photo 7, built 6.
T1_SUB=1 T1_VW_SOLVE=1 /tmp/blender/blender -b -P probe_rev46_vw.py   # the solver
T1_SUB=1 T1_GL_WRGH=0.25 T1_GL_PFX=w25 T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
  /tmp/blender/blender -b -P probe_rev58_gloss.py            # ITEM A's roughness arm, changes NO source
python3 cream_rms.py                                         # the LIVE photograph-side cream
T1_SUB=1 T1_MM_ALBEDO=1 T1_MM_SAMP=16 /tmp/blender/blender -b -P mottle_measure.py  # GATE 2
#   ^ 16, NOT the default 64.  Rev 56 measured this statistic stable across 16/32/48.
T1_SUB=1 T1_VW_DUMP=1 /tmp/blender/blender -b -P probe_rev46_vw.py     # PAINT the cells.  LOOK.
T1_SUB=1 T1_VW_RES=1 /tmp/blender/blender -b -P probe_rev46_vw.py      # count vs raster scale (F105)
T1_SUB=1 T1_PG_PAINT=1 /tmp/blender/blender -b -P probe_rev45_ground.py  # ITEM D.  G4 + its PAINTED window
T1_SUB=1 T1_NOUNDER=1 /tmp/blender/blender -b -P probe_rev45_ground.py   # the ABLATION -- C5 must REFUSE
python3 audit_brief.py                                       # rule 17's MECHANICAL half
python3 audit_adversary.py                                   # rule 15's adversary -- REPLACE its questions
```

**`out/` IS NOT TRACKED and starts empty. Render before quoting any probe that reads a frame.**
**A backgrounded runner's exit code is the WRAPPER'S, not Blender's — grep the log for `Saved:`.**
**`probe_rev54_aov.py` and `probe_rev55_truenorm.py` write EXR into `probe_scratch/` — delete them
before committing and keep the PNGs.**
**`mottle_measure.py`'s BEAUTY arm REFUSES (100 % clipped) — but F51 is FIXED now, so wiring it is
cheap (§3.4).**
**`mottle_measure.py` names its output by `MOTTLE_AMP`, so two runs that differ in `MOTTLE_M`
OVERWRITE EACH OTHER'S PNG.**
**EVERY MEASUREMENT THROUGH `shader_solve._render` IS 8-BIT (F42), whatever `color_depth` says.**

**THE DELIVERY FRAME — DO NOT RUN IT UNTIL THE MODEL IS RIGHT (owner, rev 58, and STILL BINDING:
items B, C, D and E are open).**

```bash
T1_SUB=2 /tmp/blender/blender -b -P hq_render.py      # ONE build, 10 bands, WITH MARGIN
python3 stitch.py out/hq_hero_raw.png 0.0000,0.1000=out/hq0_hero.png ...   # DECLARED spans
#   ^^ CHECK ITS EXIT CODE.  It exits 2 on a seam and it MEANS it (F49).
python3 post.py out/hq_hero_raw.png out/hq_hero.png   # optics LAST, never per strip
```

3840×2640, 256 spp, SUB=2, **106.8 min**. `probe_scratch/rev57b_delivery_hq_hero.png` (1600 px) is
the tracked baseline; the full frame is **not** tracked and that is deliberate. The guard is
narrowed **by DIMENSION, not by name** — tracked hero PNGs must be ≤ 1600 px wide.

**ABLATIONS — every one exists to WATCH A GUARD FAIL.**
**NEW AT REV 60 — and `T1_NOUNDER` is the one that arms item D's whole gate:**
**`T1_NOUNDER`** (omits the underbody entirely; `probe_rev45_ground.py`'s **C5 must REFUSE** — watched
failing at G4 0.5475 before it was watched passing at 0.2519), **`T1_UNDERSEAL`**`=0` (puts the pan
back on the cab-interior grey, which is the 0.352-vs-0.219 step), **`T1_VPOW`** / **`T1_VPOWZ`** (the
paint's and the pressed swage's exponents — **move them TOGETHER** or `verify.py` fires *"V_POW
de-registered"*, which is correct and was watched), **`T1_VRISE`** (re-derives `V_APEX0` to hold the
locked identity, so it DE-REGISTERS the swage and is for MEASUREMENT ONLY), **`T1_VW_CAPMIN`** /
**`T1_VW_PUREFIT`** / **`T1_VW_WFRAC`** (the three emblem routes rev 60 REFUTED — see §2.2 and do not
re-open them), **`T1_VW_CELLSOLVE`**(`_N`) (the cell-count search), **`T1_VW_DUMP`**(`_P`) (**paints
what `cream_cells` actually counts** — the only reason the cause was found), **`T1_VW_RES`** (the
count against raster scale, which is how F105 was caught), **`T1_VW_WSWEEP`** (stroke weight against
the photograph's ink fraction), **`T1_GL_TILES=track`** (writes the gloss tiles back into tracked
`probe_scratch/`; the default now writes to `out/`, which is F85's fix), **`T1_PG_PAINT`** (paints
G4's window — **look at it before quoting G4**).
**CARRIED FROM REV 59:** **`T1_DOOR_STALE`** (restores rev 44b's door lobes; the re-based cab-door/front-arch
clearance guard must REFUSE — watched, at 0.0653 R against the photograph's 0.0226 R).
**CARRIED FROM REV 58:** **`T1_NORIG`** (suppresses the rig; `assert_lit` must refuse — watched),
**`T1_RIG`** (build the rig without asking for a preview), **`T1_GC_ABSSPREAD`** (drops the `/p50`;
the exposure selftest must FAIL — watched), **`T1_GC_LOOSEMASK`** (restores the gloss gate's old
ink-contaminated mask), **`T1_GL_WRGH`** (the WEATHER group's roughness — item A's live lever),
**`T1_BODY_RGH`** (the shipped body roughness), **`T1_GL_DARK`** (the dark-card rig-ceiling arm —
it lands IN FRAME, which is the measurement).
Carried: `T1_GL_SPOT` (**refuted as a ceiling measure, F61**), `T1_GL_COATW`/`T1_GL_COATR`
(**refuted as a route, F54**), `T1_MOT_AMP`/`T1_MOT_M`/`T1_MOT_RGH`/`T1_MOT_DET`, `T1_FC_KVQUAD`,
`T1_RAILFLAT`, `T1_CR_LEGACY`, `T1_FC_INKGAIN`, `T1_FC_ZSTRETCH`, `T1_TRUENORM` (**a
DEMONSTRATION, not a fix**), `T1_PTWEAR`, `T1_EDGERAD`, `T1_MM_ALBEDO`, `T1_SOLVE_NODENOISE`,
`T1_TARNCONTAM`, `T1_RAILSTALE`, `T1_ENDSHORT`, `T1_CAPSINK`, `T1_LIDDEG`, `T1_BAYSTALE`,
`T1_LAMPSINK`, `T1_LIDASPECT`, `T1_HANDLEHI`, `T1_BAREMAT`, `T1_TBFOOT`, `T1_BAYPROUD`,
`T1_NOBEVEL`, `T1_BEVEL_SAMPLES`, `T1_FC_OLDDATUM`.

---

## §7. THE STANDARD, IN HIS WORDS

We are recreating a photorealistic version of **that exact bus**, and **any single measurement off is
unacceptable** — per-measurement, not on average. A model right in ninety places and wrong in one is
not 99 % done, because he will look straight at the one. **He did, at rev 58, at the emblem.**

`bus_model_ref.JPG` is a **SCHOOL BUS** and is **NOT the vehicle** — a FIDELITY BAR only. Use
`ref_workshop.jpg` the same way, and remember it has **no headlamps and no hubcaps fitted** and is
the **GREEN** vehicle (§4).

**Ground in the reference, build, adversarially audit, iterate.** Never build before grounding. Never
call it done off self-review. Report the measurement **with its ceiling**, never a self-assigned
score. Do not say anything is ready — say what is fixed, what is still wrong, and what you measured.

**RENDER IT, CROP IT, AND LOOK AT IT, before and after every change.** Every defect this project has
shipped passed `VERIFY: 0 fail, 0 warn` and was found by looking at a crop. **At rev 58 it was found
by rasterising the badge at the photograph's own scale and putting the two side by side.**

**When you need something from him, ask as MULTIPLE CHOICE with the reference material attached — one
crop, one mark, one sentence — and ASK IT WITH THE QUESTION TOOL.**

---

## §8. THE OPEN-FINDINGS REGISTER — `OPEN_FINDINGS.md`

**A register existed once and was ABANDONED AT REV 45 WITH 21 ROWS**, and nobody noticed for eleven
revisions. Rev 56 reinstated it; it carries **117 rows** now (rev 58's '65' stood until rev 60b — §8 is a CARRIER and it went stale for two revisions while the findings it points at doubled).

**IT IS A CARRIER (rule 16). Rows leave it only by being CLOSED with the measurement that closed
them, or RETIRED with the ruling that retired them. Never by being dropped.**

**THE POINT OF THE FILE IS THE PROVENANCE GRADE, NOT THE LIST.** This project's recurring failure is
**re-quoting inherited numbers as though they had been measured**. An `INHERITED` row is a claim.

**GRADE DECAY IS ITSELF A FINDING.** An `INHERITED` row that survives three more revisions without
being re-measured should be re-measured or downgraded.

**REV 58 ADDED EIGHT AND MOVED TWO.** Added: **F58** (the clone-only verifier row), **F59** (the
gate's headroom was a third artwork), **F60** (roughness, the live lever), **F61** (the rig arm
measures fill), **F62** (what the flank reflects, 19.3 m out), **F63** (the glyph is an X), **F64**
(the solver's blind axis), **F65** (three fixes that failed). Moved: **F44** partly closed,
**F51** closed.

**AND ONE CLOSURE FROM AN EARLIER REVISION IS NOW WRONG: F40** (*"the roundel reads as an X"* —
closed twice, at rev 55 and rev 57). **It was closed on a crop; the project's own rasteriser draws
an X.** F63 supersedes it.

**WHAT IS STILL INHERITED AND OLDEST:** **F14** (`gal_end_f`'s 260.0 / 20.0 mm sight lines, **rev
52 — SIX revisions un-re-measured**), F15 (A7's 803 mm, rev 52), F20 (the colour locks, rev 52),
F10 (the galley offset, rev 52), F18 (the die-cut sticker, rev 44 — **the oldest thing in the file**).

---

## §9. THE HORIZON BEYOND REV 61

**Rev 61's own order is §0.0 and `GAPS_rev60.md` §6. This section is the longer arc.** It is a
CARRIER: re-rank it, do not rewrite it, and **say what moved**.

**WHAT MOVED AT REV 60.** **D left the table** — built, gated, partly closed with its ceiling stated.
**E left it too, as a REFUTATION**: F45 is not reproducible and F99 replaced it. **B and C both moved
from "a lead needing a fix" to "the fix family is REFUTED and the cause is localised"** — which is
less satisfying and much more valuable, because two revisions of proposals are now closed off.
**`visibility_budget.py` became trustworthy for the first time.** And **F85 closed**.

**WHAT MOVED AT REV 59.** The **door** closed and was verified. The **nose** got a pose-free
instrument. The **front arch** entered and left in one revision, refuted as a method artefact.

| horizon | the work | why it is in this order |
|---|---|---|
| **next** | **F63 — the emblem's CONSTRUCTION.** His top item, five reports | Rev 60 narrowed it from six constants to one structural fact. Build, do not search |
| **next** | **F107 — the nose's real lever.** Three candidates named | The ablations exist; one render each |
| **next** | **F93 — the textures.** One of eight meets the floor | **It caps the delivery frame.** Mechanical and ungated |
| **near** | **F99's control** — a warm interior practical | Separates three causes; a measurement, not a paint change |
| **near** | **F91 — the tail and the roof against a photograph** | Two thirds of his own bar, never once done |
| **near** | **F01/F39 — `Senor`.** Worst flank region `i` at 0.685 | Small but hard-edged; A12 makes the remedy his call |
| **then** | **F10–F14 — the galley cluster.** F14 is EIGHT revisions inherited | Re-derive each X from `BAYS` |
| **CEILED** | **F44/F60/F62 gloss; F83 the front arch; F67's residue** | All three ceiled to rulings he has already given. **Do not re-litigate** |
| **standing** | **F18 — the die-cut sticker** | The original deliverable. No gate, no ruling, open since rev 44 |

---

## §10. HOW TO GROW THIS HANDOFF WITHOUT BREAKING IT

1. **The set is three files.** `LEDGER_rev<N>.md`, `NEXT_CONTEXT_PROMPT_rev<N+1>.md`, and **`cp` of
   that file over `PASTE_INTO_CLAUDE_CODE.txt` IN THE SAME COMMIT.** `CLAUDE.md` imports the `.txt`
   into every session and a byte-identity row fails if you forget. *(The `HANDOFF_rev*.md` series
   ended at rev 45; do not restart it.)*
2. **`README.md` and `START_HERE.md` name the newest brief BY NUMBER.** Two rows check it.
3. **THE ROW COUNT IS SELF-REFERENTIAL — AND IT IS AUTOMATED, SO STOP HAND-EDITING IT.**
   `python3 audit_brief.py --fix-count` writes the clean-tree total into the brief AND into
   `PASTE_INTO_CLAUDE_CODE.txt`. **Every row you add changes the number the brief must state**, so
   write the count LAST and grep for the bare number afterwards, not just the phrase.
4. **ADD ROWS ANCHORED ON ARITHMETIC OR BEHAVIOUR, NOT ON A GREP.** A grep passes on a comment.
   **Rev 58 broke this and was caught by it in the same session:** a new row meant to forbid a
   revision-numbered default frame matched **its own explanatory comment** and reported the
   explanation as the defect — the **fifth** time a row in that file has done exactly that. It is
   tokenised now. **When you write a row about a string, strip comments first.**
5. **RUN BOTH AUDITS, AS SCRIPTS, AND RECORD WHAT THEY FOUND *IN* THE BRIEF.** `audit_brief.py`
   asks *"is what the file says true?"*; `audit_adversary.py` asks *"what would make it false?"*
   **REPLACE the adversary's questions each revision** — a question that can no longer fail is not
   a control.
6. **NEVER DELETE A CARRIER.** §0, §0.1, §4, §5, §8 and §9 are carriers.
7. **RANK BEFORE YOU CHOOSE** — `python3 visibility_budget.py`. **But the owner outranks it**, and
   at rev 58 he used that. If you work an item the script puts in the bottom half, say why.
8. **NEVER RELAX ONE COPY OF A CHECK.** `audit_brief.py` and `verify_clone.sh` assert some of the
   same things. **Loosen both or neither**, and when a check fails on code you just wrote, suspect
   the code first.
9. **DO NOT LET THE MACHINE IDLE.** Blender is CPU-bound and must not be fanned out. **Run
   `bootstrap.sh` first** — the toolchain was absent at rev 58 — then launch the render, then read.
10. **ROOM TO GROW:** new findings go in `OPEN_FINDINGS.md` with an ID and a grade, not into this
   file's prose. This file points AT the register.
