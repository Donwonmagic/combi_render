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

**READ `REMAINING_WORK_rev61.md` FIRST — IT IS THE RANKED EXECUTION LIST.** The owner asked for it in
those words: *"a comprehensive list of just what exactly is left, so we know what we need to
execute."* It sorts the register's 83 open rows into **REAL WORK (9) / CEILED-do-not-touch (4) /
the owner's call (3) / process debt (7)**, and its **§I carries 27 open rows that were in no
document at all**, including **F79** (the nose roundel 10–24 % too large, on the owner's top item)
and **F77**. `GAPS_rev60.md` is still worth reading, **but two adversary passes have found NINE
defects in it** — read its ⚠ block before leaning on any figure in it.

**THE OWNER'S REV-58b RANKING IS NOW FULLY WORKED. TWO CLOSED, TWO REFRAMED.**

| # | do | state at close of rev 60 | gate |
|---|---|---|---|
| **A** | **THE DOOR** | **FIXED AT REV 59 and STILL FIXED — but its probe was BROKEN for a revision and nothing reported it (F131).** The rev-60c underbody took C4 and C5 red on a door that had NOT moved; both were instrument defects and both are fixed | `probe_rev59_door.py` **8 checked, 1 FAILED (M3, by design)** — and NEW: `--selftest`, a synthetic step with feet known BY CONSTRUCTION |
| **D** | **THE GROUND SHADOW AND UNDERBODY** | **BUILT AT REV 60; GEOMETRY REPAIRED TWICE SINCE, AND THE FIGURES REV 60 PUBLISHED ARE STALE.** Re-measured at rev 60c: **G4 0.3602 built, 0.5475 ablated**, against a photographed 0.057. The residue is now APPORTIONED — see §2.1 | `probe_rev45_ground.py` **G4 PASSING at 0.3602**; and NEW: `verify.py`'s underbody **proudness** and **slot** rows |
| **C** | **THE EMBLEM — still an X** | **NOT FIXED. CAUSE LOCALISED at rev 60** to the CONSTRUCTION: the V and W are each ONE mitred polyline and they fuse into two diagonals. **Three hypotheses refuted — do not re-try them** | `probe_rev46_vw.py` C6, **watched failing** |
| **B** | **THE NOSE BREAK — 73 mm on the red-bus ruler, but F75's HONEST BRACKET IS 50–80 mm, best single estimate 52 mm** | **NOT FIXED. THE WHOLE REMEDY PROGRAMME IS REFUTED at rev 60** — `V_POW`, `V_RISE` and `V_POW_Z` all fail to move the feature | `probe_rev59_nose.py` M1, **watched failing** |
| **E** | **THE INTERIORS** | **F45 REFUTED AS WRITTEN.** The real defect is CHROMA (F99) and its cause is not separable from one frame | none — and that is a finding |

**THERE IS NOTHING TO PUT TO HIM THIS REVISION, AND THAT IS THE HONEST OUTCOME.** Rev 60 drafted
three owner questions and an independent audit refuted all three: **F99**'s interior warmth was
measured on a DIFFERENT STATE of the vehicle (on the target's own frame the render is within 2 %),
**F100**'s gold surround is that state's too, and **F111**'s glazing was a MISREAD WINDOW — the bays
read OPEN, the cook's bare forearm is at full saturation with no veil over it, and `STATE.md`'s
*"open serving apertures on +Y: 3"* already matches. **Do not spend his one question on any of
them.** *Do not re-ask anything in §4.*

**RANK BY PIXELS OF THE DELIVERY FRAME**, `python3 visibility_budget.py 3840` — **and PASS IT THE
FRAME.** Rev 60 "repaired" it and rev 60c-ii found it had reproduced the defect it fixed (F132): it
took its scale off whichever hero was rendered LAST, in an untracked directory, so the ranking that
decides what counts as WORK depended on `out/` mtimes — 724 px/m against 801 with a different newest
frame. It now names the frame it used on every run. **Every px² figure in `REMAINING_WORK` was
measured at the 801 scale and is ~22 % high; the ORDERS OF MAGNITUDE, which is all that column is
for, are unaffected.**

---

**Now read this whole file before you CHANGE anything.** Then **`REMAINING_WORK_rev61.md`** — the
owner asked for it in those words at rev 60c (*"a comprehensive list of just what exactly is left, so
we know what we need to execute"*) and it is the RANKED EXECUTION LIST: it sorts the register's open
rows into work, ceiled, the owner's call and process debt, and its **§I** carries 27 rows that were in
no document at all. Then `GAPS_rev60.md`, then `CLAUDE.md`,
then `LEDGER_rev60.md` (where every number in §2 comes from), then `OPEN_FINDINGS.md`.

---

## §0.05 THIS BRIEF WAS AUDITED AGAINST THE MACHINE BY AN INDEPENDENT ADVERSARY — AND IT FOUND EIGHTEEN THINGS

**Rule 15/17: an adversary was put on the documents being HANDED ON, not only the ones received.**
It returned **18 findings**, and **the two worst were written in the same session that shipped them**:

* **I broke `probe_rev59_door.py` and every gate stayed green.** Live tree 3 FAILED, `T1_NOUNDER=1`
  1 FAILED. The door never moved — the walks are identical to **under 1.1 px** — but my underbody
  let the tracked walk run **three columns further**, and `feet()` flipped. Two instrument defects
  (an ill-conditioned axis, and a band selected by value with no contiguity test). **F131.**
* **G4's ablated headline `0.5607` was wrong in five documents.** It is **0.5475** — five runs,
  spread 0.0010 — and `probe_rev45_ground.py`'s own header had said so all along. `T1_NOUNDER`
  builds no underbody, so no mesh change can move it, and the brief's justification for striking
  the correct value was invalid on its face. **F130.**

**AND MY OWN TAIL FINDING WAS RETRACTED (F133).** F128 called a "133× spread ratio" decisive; its
two photograph readings came from **different instruments**. Under one consistent painted window the
photograph's spread is the **larger**. The level difference survives (~1.7–2.4×, not 4.7×); the
argument does not.

**THE LESSON, AND IT IS THE PROJECT'S RULE 4 VERBATIM: every instrument built this session was
wrong at least once, and every one produced a plausible number first.**

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

**AND HERE IS THE HONEST DISTANCE.** `verify_clone.sh` ends **ALL 271 PASS** and its own verdict
block says what that is worth: **0 FIDELITY, 271 SELF-CONSISTENCY. Not one of those rows compares
the vehicle to a photograph.**

| gate | state MEASURED at close of rev 60 |
|---|---|
| `flank_compare.py` | **runs, FAILS.** Worst region **`i` at 0.684** against a 0.75 bar; `Senor` **0.721** (re-measured rev 60c-ii). *(The rev-58 table said `Senor` 0.651 and rev 60 found that BOTH stale AND contradicted by this same brief's §9 — re-measured live.)* The deficit is the **artwork alpha and its placement**, not the render (F39) |
| `mottle_measure.py` | **runs, and it is NOT measuring the mottle** — 1.1–2.0 % of it. Rev 56's reading and rev 57's item B are REFUTED |
| `gloss_compare.py` | **runs, FAILS at 0.426** (bar 0.60, re-measured rev 60c-ii on `out/r60c_hero.png`; four heroes in `out/` give 0.425-0.429 and **0.436 reproduces on none of them** -- the brief carried an invented regression). Mask corrected at rev 58 (F59); the model-side lever is now **exhausted** (F60/F62) |
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

## §0.06 THE MACHINE'S VERDICT AT CLOSE OF REV 60c-ii — every one watched print

```
bootstrap.sh          ALL 10 PASS
verify_clone.sh       ALL 271 PASS on a clean tree   <- 0 FIDELITY, 271 SELF-CONSISTENCY
VERIFY (in build)     0 fail, 0 warn at SUB=1 AND SUB=2
  underbody proudness worst -55.8 mm (SUB=2) / -50.1 mm (SUB=1)  INBOARD everywhere
  underbody/shell fit worst intrusion +10.5 mm over 1400 perimeter stations, both signs of y
probe_rev45_ground    5 checked, 0 FAILED.  G4 0.3602 built / 0.5475 ablated / 0.057 photographed
probe_rev59_door      8 checked, 1 FAILED (M3, BY DESIGN);  --selftest 2 checked, 0 FAILED
probe_rev46_vw        C6 FAILS: photograph 7 cream cells, built 6 (4 at the photograph's scale)
probe_rev59_nose      M1 FAILS: 1.187 lamp radii against 1.951-2.121
flank_compare.py      FAILS: worst region `i` 0.684 (bar 0.75), `Senor` 0.721
gloss_compare.py      FAILS: 0.426 (bar 0.60)
textures              7 of 8 tracked >= 3072; tex/emblem.png 1024 and BLOCKED (F115)
audit_brief.py        10 checked, 0 FAILED
audit_adversary.py    24 asked, 0 BROKE   <- six questions REPLACED for rev 61
```

**AND THE STANDING WARNING, WHICH `verify_clone.sh` PRINTS ITSELF.** A green check is not evidence
about the vehicle. **Not one of those 270 rows compares the model to a photograph.** The trunk lid
that opened inwards, the board buried in the roof, the disc of body red in every tail lamp, the
five-petal hubcaps — every one passed this script and was found by **LOOKING AT A CROP**.

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
./verify_clone.sh       # ALL 271 PASS in ~70 s -- and read its verdict block
```

**THE MERGE STATE, MEASURED AT REV 60b CLOSE — AND REV 60 GOT THIS WRONG.**

```
HEAD  claude/new-session-ocymb5   54 ahead / 0 behind origin/main   [rev 60c-ii; MEASURE IT AGAIN]
origin/main                       fbcec2e, still rev 58's PR #18 merge
rev 59's door commit  6275969     NOT on main
rev 60's underbody    0b0bf89     NOT on main
```

**42 commits — the whole of rev 59 AND rev 60 — are MERGED NOWHERE.** They live only on the branch
this file says gets deleted from the remote (five revisions running). The rev-60 brief said
*"0 ahead / 0 behind … rev 59's work was already merged"*, which was false: it had measured
`git diff --name-only HEAD...origin/main`, the **THREE-DOT** form, which is empty whenever main has
nothing HEAD lacks and says **nothing** about the reverse. **That is the seventh consecutive
revision whose prose guessed the merge state.**

**AND `bootstrap.sh` ROW 9 IS STRUCTURALLY BLIND TO IT.** Its loop is
`git rev-list --count HEAD..$b` — it finds branches AHEAD OF HEAD, never HEAD ahead of main. It read
**green** through all 42. `bootstrap.sh` now PRINTS the count every run (it is not a failing row:
being ahead mid-revision is normal, and a row that cries wolf teaches you to ignore the one row that
must never be ignored). **Read that line. Do not infer the merge state from a three-dot diff.**

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
cavity floor / open ground   0.545 -> 0.352 (pan) -> 0.219 (underseal)   photograph 0.057   [STALE]
probe_rev45_ground G4        0.5475 ablated -> 0.2519 built                                   [STALE]

  ^^ BOTH LINES WERE MEASURED ON A BUGGED MESH AND ARE SUPERSEDED.  Re-run at
     rev 60c, after the geometry was repaired:

  G4  ablated (T1_NOUNDER=1)                     0.5475
      BUILT, AS SHIPPED (visible drop 0.090 m)   0.3602   <- the live figure
      built at the ceiling band's top (0.145 m)  0.2581
      photograph ref_side.jpg                    0.057
```

**PARTLY CLOSED WITH ITS CEILING, AND AT REV 60c THE RESIDUE IS APPORTIONED RATHER THAN ASSERTED.**
The third row above is a CONTROL (`T1_UNDER_VIS`, measurement only) that separates the two named
causes, which rev 60 could only name: **the assumed drop owns 0.1021 of the residue, and even at the
most generous drop the photograph is still 0.2011 away — and that remainder is the studio**, F62's
ceiling, which the owner has ruled. **The shipped constant stays 0.090 deliberately**: the
0.137–0.155 m band is a CEILING containing both the metal and the shadowed ground, and setting a
constant to a ceiling would assume the band is all metal. **A low raking shot under the sill is the
new frame that would settle it.**

**AND THE GATE'S OWN SPREAD IS NOW STATED — CORRECTED AT REV 60c-ii, BECAUSE THE FIRST ATTEMPT
POOLED TWO DIFFERENT MESHES AND CALLED THE RESULT INSTRUMENT NOISE.** It quoted *"three runs across
two geometry variants, spread 0.0027"*; a variant is not a repeat, and 0.3585 was measured before the
aft closer moved. Measured properly, on ONE geometry:

```
G4 built     0.3599 / 0.3596 / 0.3610   mean 0.3602   spread 0.0014   <- render noise
G4 ablated   0.5475 / 0.5478 / 0.5477 / 0.5468 / 0.5476
                                        mean 0.5475   spread 0.0010
```

**Quote them as 0.360 ± 0.002 and 0.547 ± 0.001, not to four figures.**

**AND THE 0.2519 THIS BRIEF PUBLISHED WAS SUBSTANTIALLY THE BUG.** The pre-repair pan hung
0.134–0.145 m low, which is essentially the 0.145 row above (0.2581). **Rev 60's "improvement" was
mostly a mesh error that happened to flatter the gate.**

**THE NAME IS ALSO WRONG AND IS FIXED IN SOURCE: `UNDER_DROP` STOPPED MEANING THE VISIBLE DROP.**
Rev 60b silently redefined it as the pan prism's DEPTH, most of it buried (0.124 m now), while the
brief, `GAPS_rev60.md` and `audit_adversary.py`'s ceiling question all went on quoting it against a
ceiling that belongs to the visible drop. **`UNDER_VIS` is the visible drop and is the 0.090.**

**C5 was watched failing before it was watched passing** (rule 3 — re-watched at rev 60c: 0.5475 ablated, 0.3602 built), and `verify.py`'s length
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

## §2.7 WHAT REV 60c DID — AN INDEPENDENT ADVERSARY PUT THE BUG BACK AND NOTHING NOTICED

**THE FINDING THAT MATTERS, and it is about this repository's guards, not about the underbody.**
An independent adversary restored rev 60's *exact* z error on the repaired tree — pan 45 mm low
leaving an open slot, rails 78 % buried — and reported `VERIFY: 0 fail, 0 warn` and
`verify_clone.sh` **ALL PASS**. `grep -n "underpan\|chassis_rail\|under_close\|UNDER_" verify.py`
returned **nothing**. The rev-60b repair guarded the one axis `STATE.md` happened to already print
and left the axis that caused the visible damage unguarded and un-ablatable. **The clone-level row
was worse: it greps `STATE.md` for the four object NAMES, so it passed throughout rev 60 with both
closers 685 mm proud AND the pan 45 mm low** — rule 10, verbatim.

**FOUR MORE DEFECTS IN THE SAME ASSEMBLY, all measured off the mesh, all confirmed independently
before acting** (F116–F125, and every one is in `OPEN_FINDINGS.md` with its number):

| what | measured | now |
|---|---|---|
| aft closer PROUD of the tapering tail | up to **+48 mm**, last 7 mm past the rearmost bodywork in open air | ends at x −1.830; worst **−26.2 mm, inboard everywhere** |
| OPEN SLOT against the shell | **−29.1 mm** at the tail, −2.3 mm at the front | worst intrusion **+10.6 mm** over 1400 perimeter stations |
| rails end blunt in mid-air | **200 mm** short of the pan, square 35 mm face in silhouette | tapered into the pan, ending 100 mm inboard |
| pan floor / rail top | **bit-identical** `0.29599999999999999`, coincident faces over 3.14 m | 10 mm overlap |

**AND `ZB` IS NOT THE SHELL'S UNDERSIDE — that is why rev 60b's slot fix missed the tail by 29 mm.**
`UNDER_TOP` was set "above max(ZB) = 0.397". Ray-cast up at the shell from below and its own bottom
face, authored, is a curve that RISES AT BOTH ENDS, to **0.4391** at x −1.850. **Rev 60b's stated
CAUSE is retracted too**: it blamed the rake shear, but step 8b shears pan and shell alike, and a
shear that is a pure function of x cannot open a gap between two things at the same x.

**THE GUARDS THAT NOW EXIST, and rule 36 says to write down what they cannot see — both do, in
source.** `verify.py` gained **proudness** (per station, against the body's OWN half-width) and
**slot** (against the shell's OWN ray-cast underside). Neither derives its threshold from what it
checks (rule 6): both compare the underbody against the BODY, built by other code.
**Watched failing, all three, which is the only reason they count (rule 3):**

```
T1_UNDER_ZBUG   -> SLOT  -50.5 mm                the defect that was invisible
T1_UNDER_PROUD  -> PROUD +55.4 mm                the PROUDNESS row ONLY
T1_UNDER_YBUG   -> PROUD +724.1 mm, SLOT -335.3, and the old lateral row -496 mm
```

**ALL THREE RE-MEASURED AT REV 60c-ii AT SUB=1, AFTER THE GEOMETRY MOVED.** The brief previously
said `T1_UNDER_PROUD` *"fires the slot row too"* (it does not, since the aft closer's station moved)
and put `T1_UNDER_YBUG` at **+753.8 mm** (it is **+724.1**, because the skin's half-width at the
ramp's new station is different). **Both were true when written and stale when they shipped — which
is the whole reason this brief says measure, do not transcribe.**

**MY OWN NEW GUARD WAS WRONG ON ITS FIRST RUN — rule 4, on schedule.** It sampled a 6 mm vertex slab,
found it EMPTY at x −0.630 because the shell is subdivided, and reported the pan **780 mm proud**
where it is 95 mm inboard. Caught by reading the number, fixed by binning the profile once (F125).

**AND FIVE FIGURES IN THE RECORD WERE WRONG** (F120–F124): item D's headline **G4 0.2519 was
measured on a mesh the repair deleted** and is really **0.3602**; *"919 mm proud"* stood in THREE
source files when 1.560 − 0.875 = **685**; the aft-ramp comment cited `WX(-1.880) = 0.873` when it is
**0.7122** (0.873 is `WX(-1.700)`, 180 mm away) — **and that sentence is what licensed the
proudness**; `UNDER_DROP` silently stopped meaning the visible drop; and `underbody()` cited **SPEC
10.117, which is about PAINT** — SPEC has no underbody section, so the citation is WITHDRAWN rather
than invented (rule 34).

**AND THEN THE ADVERSARY RE-RAN AGAINST THE FIX AND FOUND A −53 mm SLOT STILL LIVE — BEHIND MY OWN
GUARD'S OUTERMOST SAMPLE (F126). THIS IS THE MOST IMPORTANT PARAGRAPH ON THIS PAGE.**
The tail's underside is a **DISH** that turns up violently into the flank. At the pan's outer edge,
authored: **0.4027 at x −1.760, 0.4066 at −1.780, 0.4167 at −1.800, 0.4863 at −1.830** — flat, then
80 mm of climb in 30 mm of x. My slot row sampled five typed y stations **ending at 0.74**, where the
margin reads a comfortable +16.0 mm; at 0.760 it is +3.5 and at 0.778 it is **−20.8**. **It also
never sampled −y at all — the side the entire rev-60 defect lived on.** `STATE.md` published
*"CLOSED everywhere the pan spans"* over a live, symmetric, 53 mm hole. **Rule 8, committed by the
row written to enforce rule 8.**

**AND THE INSTRUMENT HAD TO BE REBUILT TWICE MORE BEFORE IT WAS RIGHT — the second attempt is the
lesson.** Sampling the whole footprint fired at **−357 mm over the WHEEL WELLS** (the body's nearest
downward face there is the inner arch). Capping the gap only MOVED the false positive: x +0.965 read
−148 mm, just inside a 150 mm cap. **Across the notch boundary the gap is a CONTINUUM from 0 to
357 mm, so no threshold can separate the two cases — the threshold was the wrong INSTRUMENT, not a
badly-chosen number.** It now asks the question that actually matters — *"is there a gap you could
SEE?"* — by testing the underbody's **outward-facing perimeter**: the outboard edge where the pan
runs at FULL WIDTH (mesh-derived, so the notched edges drop out because they are narrower, not
because anything was typed), plus both end stations across y. **1400 stations, both signs of y.**

**AND ONE ABLATION SILENTLY STOPPED BEING AN ABLATION (F127).** `T1_UNDER_PROUD` was `xo = -0.120`,
which reproduced rev 60b's −1.880 ramp only while the pan ended at −1.760. When the fix moved the
pan's end the ablation became a −1.820 ramp — **inboard of the skin, exercising nothing** — and it
still looked fine because a different row happened to fire. It is pinned to the absolute station now.
**An ablation must be pinned to what it reproduces, not to an offset from live geometry.**

**THE ONE PIECE OF GENUINELY NEW GROUND: G4's RESIDUE IS NOW APPORTIONED, NOT ASSERTED.** See §2.1.
`T1_UNDER_VIS` is a MEASUREMENT-ONLY control that separates the two causes rev 60 could only name.
**The assumed drop owns 0.1021; the studio owns the remaining 0.2011.** And it explains 0.2519: the
bugged pan hung 0.134–0.145 m low, which is the deep-pan case, **so rev 60's "improvement" was
substantially the bug**.

**`GAPS_rev60.md` HAD NOT BEEN TOUCHED BY ANY REPAIR COMMIT** while §0.0 orders it read FIRST. It is
a carrier, so it is annotated IN PLACE with a ⚠ block naming all four retracted things (F124).

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
python3 probe_rev59_nose.py out/r61_front.png     # M1 FAILS: 1.187 vs 1.951-2.121
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

### §3.4 F93 — THE TEXTURES. **DONE AT REV 60b AND GATED. DO NOT RE-DO IT.**

**This section said "ONE of EIGHT textures meets SPEC §5's 3K floor... the finish line's blocker and
nobody has touched it". That was true at rev 60 and false when it shipped**, and §9 ranked it third
on that basis. Measured at rev 60c-ii: `tex/calidad.png` 3072x2267, `tex/emblem.png` 1024x1024, `tex/lidmural.png` 4096x2476,
`tex/lidsign.png` 4096x2476, `tex/nose.png` 3072x3072, `tex/senor.png` 4096x1738, `tex/swirl.png` 4096x4096, `tex/swirl_b.png` 4096x4096 — **seven of
the eight tracked textures clear 3072, and the eighth is `tex/emblem.png`, which is EXEMPT and cannot be
regenerated at all (F115: `texgen.make_emblem` raises "no usable font").** It is **gated**:
`verify_clone.sh`, grep `every texture meets SPEC sec.5's 3K floor`.

**WHAT IS ACTUALLY LEFT HERE, and it is much smaller:** the owner's own bar is **4K**, and
`tex/calidad.png` and `tex/nose.png` sit at 3072. That is a decision, not a blocker.

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
python3 probe_rev59_nose.py out/r61_front.png               # ITEM B.  M1 FAILS: 1.187 vs 1.951-2.121.
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
**NEW AT REV 60c — THE TWO AXES REV 60b LEFT UNGUARDED, AND THE ONE THAT APPORTIONS G4:**
**`T1_UNDER_ZBUG`** (restores rev 60's z error — pan 45 mm low, rails 78 % buried; `verify.py`'s
underbody SLOT row must REFUSE — **watched at -50.5 mm**), **`T1_UNDER_PROUD`** (restores rev 60b's
aft ramp at its ABSOLUTE station x −1.880 — see F127; the PROUDNESS row must REFUSE — **watched at
+55.4 mm, that row and no other**), **`T1_UNDER_VIS`** (the pan's VISIBLE drop
— **MEASUREMENT ONLY**, it is what apportions G4 in §2.1 and it is not a tuning knob).
**And `T1_UNDER_YBUG` now fires THREE rows — the lateral row at −496 mm, the new proudness row at +724.1 mm, and the slot row at −335.3 mm.**

**NEW AT REV 60 — and `T1_NOUNDER` is the one that arms item D's whole gate:**
**`T1_NOUNDER`** (omits the underbody entirely; `probe_rev45_ground.py`'s **C5 must REFUSE** — watched
failing at G4 0.5475 before it was watched passing at 0.3602), **`T1_UNDERSEAL`**`=0` (puts the pan
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
| ~~next~~ **DONE** | ~~**F93 — the textures.** One of eight meets the floor~~ **CLOSED at rev 60b and GATED — see §3.4. Seven of eight clear 3072; the eighth is exempt (F115). What is left is the owner's 4K bar on two files** | ~~It caps the delivery frame~~ **This row was stale when it shipped and it ranked the item third** |
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
