# NEXT CONTEXT PROMPT — rev 37
Please act as my expert. Continue the Señor Tacombi combi build. **Thirty-six
revisions sit behind this.** You are picking up mid-stream, not starting.

## Step 0 — CHECK A FOLDER IS CONNECTED BEFORE YOU PLAN ANYTHING
Call `get_device_info`. **In rev 32 through rev 36 `~/Desktop/tacombi_bus_render`
was ALREADY in `connectedFolders` on the first call** — five in a row. It timed
out unanswered in rev 28/29 and was granted on the first request in rev 30/31.
**Do not assume any of those outcomes** — call it, and say plainly what came back.

**THE BRIDGE HAS A THROUGHPUT CEILING, NOT JUST A SIZE ONE.** `device_stage_files`
times out on large single files. **Only TWO files need splitting:** the 19.5 MB
base bundle (7 parts) and the 8.5 MB `rev14_unified` (3 parts). **Everything
rev15–rev36 is under 3 MB and crosses whole.**
**REV 34, 35 AND 36 ALL REUSED REV 33's `_xfer33/` SPLIT PARTS** rather than
re-splitting. They are still on his disk. Check before spending `device_bash`.
**REV 36 MOVED 32 FILES IN 8 BRIDGE CALLS WITH ZERO TRANSIENT FAILURES** — one
call fewer than rev 35, and **THREE 2.9 MB PARTS IN ONE CALL (8.7 MB) HELD.**
Do not read that as the new normal: rev 32 had two `upload failed` in one batch,
and the bridge genuinely drops (three times in rev 31, once at rev 35's
delivery). **TRANSIENT FAILURES ARE NOT DROPS.** Do not retry in a loop.

**`device_bash` DOES NOT SEE `/Users/...`.** The mount is
`/sessions/<session-id>/mnt/tacombi_bus_render`. **`device_stage_files` DOES
take the `/Users/...` path.** **AND YOUR SHELL'S `~` IS `/root`.**

**`hero.py` IS NOT A BLENDER SCRIPT.** It is a plain Python driver.
To render a preview, drive `build.py`:
```bash
T1_SUB=1 T1_PREVIEW=hero34f T1_FX=0 T1_RX=900 T1_RY=600 T1_SAMP=24 \
  T1_OUT=/tmp/prev T1_PFX=pv blender -b --python build.py
```
**A 1500×1000 / 36-sample nose render took 6 m 50 s in rev 36.** A 900×600 /
24-sample took 79.3 s in rev 35. **`detail_f` FRAMES THE NOSE, NOT THE BUMPER** —
rev 36 wasted a 5-minute render finding that out and wrote
`render_rev36_bumper.py`, which adds a bumper-level camera to a LOCAL COPY of
`studio.views()` and **refuses if the name already exists.** Reuse it.
**`ref_workshop.jpg`, `ref_side.jpg` and `ref_rear34.jpg` are IN THE REPO.**

## Step 1 — read my memory BEFORE you read any code
`/areas/tacombi-combi-3d.md`, then `-rev14`, `-rev17` … `-rev35`, then
**`/areas/tacombi-combi-3d-rev36.md`** (SEPARATE FILES; each revision's file
does NOT carry the next), then `/areas/tacombi-combi-sticker.md`, then
`/preferences.md`. If you cannot read them, say so explicitly.

**REV 36 PROVED WHY THIS STEP IS NOT OPTIONAL.** My own defect report — *"the
upper bar appears to also connect with the main bumper on either end"* — had
been lost from **every carrier that crosses contexts**: not `SPEC.md`, not
`HANDOFF_rev35.md`, not anywhere in the rev-36 prompt, whose §6 item 1 was the
probe rewrite and whose §5 said *"NO QUESTION IS OUTSTANDING."* **Only memory
had it.** Had rev 36 opened the code first it would have rewritten two probes
and never touched the bar. **CHECK THIS PROMPT AGAINST MEMORY BEFORE TRUSTING
ITS WORK LIST.**

**I have never stood in the bus.** The "remember standing in the kombi" bar is
about the RESTAURANT'S owner. **Do not ask me what the real vehicle looks like.**
Ask me what a PHOTOGRAPH shows — that has now paid off twenty-seven times.

## Step 2 — restore, and verify BY CONTENT (never by hash or commit count)
See §1. **TWENTY-FOUR bundle lines now, and the rev14b line is a `fetch` that
must come BEFORE rev15.** rev 20 through rev 36 all restored CLEAN.

## Step 3 — install Blender 4.5.3 and run BOTH guards before proposing anything
```bash
curl -fsSL -o b.tar.xz https://download.blender.org/release/Blender4.5/blender-4.5.3-linux-x64.tar.xz
tar -xf b.tar.xz && mv blender-4.5.3-linux-x64 /tmp/blender
/tmp/blender/4.5/python/bin/python3.11 -m pip install pillow scipy
```
That pip line is required. Guards are `T1_SUB=n T1_VERIFY=1 blender -b
--python build.py` and `T1_SUB=n blender -b --python audit.py`. Report the
guards' ACTUAL output, both levels. **`audit.py` rewrites `STATE.md` every run
— `git checkout STATE.md` after.**

**THE GUARDS ARE 0 fail / 0 WARN.** **GEOMETRY MOVED IN REV 36 — the first time
since rev 30.** **THE HERO IS NOW GENUINELY OWED: `rev30_hero34f.png` IS A
RENDER OF THE REV-30 BUILD AND THE BAR'S ENDS HAVE CHANGED SHAPE SINCE.** It is
SUPERSEDED, not merely stale. Do not quote it as current.

**RUN THE PROBES YOU INHERIT, NOT ONLY THE ONES YOU WRITE.** **THERE ARE NOW
25 `probe_*.py` FILES** (rev 36 inherited 23 and wrote 2). rev 32 found one
failing a control since rev 30; rev 33 found two more; rev 34 found the brief's
own sentence about them wrong; rev 35 found its own H4 checking the wrong
precondition; **rev 36 found FOUR of its own detectors measuring the wrong
thing, and every one was caught by a control rather than by inspection.**

**SIX INHERITED PROBES NEED BLENDER — BUT NOT THE SIX A GREP NAMES.** Run under
`blender -b --python`: `probe_ctan_index`, `probe_dust_scope`, `probe_f90`,
`probe_rev16`, **plus `probe_cross_anatomy` and `probe_shutlines`, which import
it TRANSITIVELY** — **and NEW in rev 36, `probe_rev36_barend`, which imports
`build` directly, making SEVEN.** Everything else under
`/tmp/blender/4.5/python/bin/python3.11` — **including `probe_clean_top` and
`probe_dust_anchor`, whose only `bpy` is in a comment.** **A grep still gives
two false positives and two false negatives.**
**`probe_rev35_harmonic.py` and `probe_rev36_posts.py` run standalone.**

## Step 4 — read, in this order
`STATE.md` → `SPEC.md` §10, then §10.9 through §10.90 → this file →
**`HANDOFF_rev36.md`** → `HANDOFF_rev35.md` → … → `AUDIT_rev18_loft.md` →
`LOFT_GROUND_rev15.md` → `AUDIT_rev12.md` → `REF_MEASUREMENTS.md`.
`STATE.md` is machine-written; **if it and any prose disagree, it is right —
BUT CHECK ITS PROVENANCE ROWS FIRST.** In rev 33 the committed `STATE.md` was
one revision stale. **rev 36's is current** — regenerated on the clean rev-36
tree at commit `7c74e57`, `working tree | clean`, with `STATE_rev36.md`
alongside. **It has a `working tree` row; if that says DIRTY, the file is not
a record of anything.**

**§10.90 IS REV 36's. IT MOVES GEOMETRY.** It does nine things:
1. **OVERTURNS ALL THREE OF REV 35's FIGURES** about the bar's ends. One gap,
   not two; 23.59 mm, not 8.1; the fore-aft gap does not exist.
2. **FINDS TWO DEFECTS THAT WERE NOT THE GAP** — a 61.2° tangent discontinuity,
   and a numerical workaround that had become the shape.
3. **MEASURES THE REAL END SHAPE SCALE-FREE** and publishes both figures WITH
   THE DIRECTION OF THEIR BOUND.
4. **BUILDS IT**, retiring two grade-E constants and deriving two more.
5. **GUARDS IT TWO-SIDED** and falsifies it in four arms.
6. **RECORDS THE OWNER RENAMING A COLUMN CONSUMED SINCE REV 32.**
7. **DISSOLVES §10.83** — two posts, neither on the centreline.
8. **ENUMERATES A THIRD ESTIMATOR'S PRECONDITIONS AND ABANDONS IT BEFORE
   BUILDING IT.**
9. **RECORDS SIX DEFECTS OF MY OWN, PLUS A SEVENTH THAT WAS THE BRIEF'S.**

## Step 5 — ASK ME WHAT THE PHOTOGRAPHS SHOW before you measure from them
This has now paid off twenty-seven times. Show me a crop, mark the regions,
give me options, **print the crop box**, and **say plainly what each mark IS.**
rev 30's two marks were SAMPLING WINDOWS; rev 31's four were POINTERS; rev 32,
33, 34 used CANDIDATE LINES; rev 34 added an ORDERING WALL; rev 35 added
MEASURED COLUMNS + ONE DERIVED MEAN; **rev 36 added TWO more — a COALESCENCE
COLUMN, and an OCCLUSION BAND, which is the first mark in this project that
marks the ABSENCE of legibility rather than something legible.**
Show the photograph **BESIDE a render of the current build.**

**AND REV 36 LEARNED THE HARD WAY THAT A FIGURE CAN BE TOO CLEVER TO ANSWER.**
Its first question figure carried five mark classes, printed crop boxes,
coalescence columns and a priced null — and my answer was *"i don't understand
what is being asked."* **The second attempt was one 7× crop, one red circle, and
one sentence, and it produced the most valuable answer in ten revisions.**
**IF I DO NOT UNDERSTAND THE QUESTION, THE FIGURE IS THE DEFECT, NOT ME.**

**A CLASS GATE IS A PROBE TOO**, and so is a BRIEF, a TARGET, a SUBAGENT'S
FINDING, A CITATION, A GUARD YOU JUST WROTE, AN ESTIMATOR YOU JUST BUILT,
A QUESTION YOU ARE ABOUT TO ASK ME, A THRESHOLD, A SAMPLING WINDOW, A NULL
PATCH, A REFUTATION SOMEONE ELSE ALREADY BANKED, THE AXIS YOUR DETECTOR
SEARCHES ALONG, A LINE IN THE WORK LIST, A FALSIFICATION ARM YOU JUST RAN,
THE ARITHMETIC PRINTED UNDER A FIGURE, A PRE-COMMITMENT YOU JUST MADE, THE
UNITS YOUR TOLERANCE IS STATED IN, THE DETECTOR THAT TELLS YOU WHICH FILES A
RULE APPLIES TO, THE LIST OF PRECONDITIONS YOU THINK A CONSTRUCTION HAS,
A FIGURE YOU HAVE ALREADY SENT ME, and — NEW, rev 36 — **THE DATUM A DERIVATION
LANDS ON**, **THE FAILURE MESSAGE A GUARD PRINTS WHEN IT FIRES**, and **THE
LABEL UNDER WHICH YOU ASKED ME A QUESTION.**

**DO NOT ASK ME WHAT MEASUREMENT CAN ANSWER.** **AND MY ANSWER MAY NOT BE ONE
OF YOUR OPTIONS — IN REV 36 IT WAS NOT, AND THAT ANSWER WAS THE REVISION.**
**IF I PICK THE FIRST OR LAST OPTION, YOUR SET PROBABLY DID NOT REACH FAR
ENOUGH — but CHECK WHETHER THE ENDPOINT IS AGAINST A WALL FIRST.**

## Step 6 — the work
§6 below is the ordered list. **CHECK IT AGAINST MEMORY BEFORE YOU TRUST IT** —
the rev-36 prompt's list had lost my highest-priority item entirely.

## Step 7 — resolution
rev 25 shipped 4800×3200 in 20 strips, worst seam z 1.91. Drive
`hero.py --only N` one strip per call then `--stitch-only`; run `post.py`
**once** on the stitched frame, never per strip. Middle strips ~5–7 min each,
edge strips ~1.5 min. **`hero.py` STRIPS IN ROW SPACE — SEAMS ARE HORIZONTAL.**

## How I work
* Ground in the reference → build → adversarial audit → iterate. Never build
  before grounding. Never call it done off self-review.
* Report the measurement against the reference, **with its ceiling**. Never a
  self-assigned score.
* Do not tell me anything is ready. Tell me what is fixed, what is still wrong,
  and what you measured.
* Keep visible cadence on long work and send renders as they land.
* Travel between contexts consciously, every time.

## Already settled — do not re-open without new evidence AND a different method
Everything in the rev-36 prompt's equivalent section still stands, **with these
changes.**

**THE BAR'S HOOP ENDS NOW MEET THE BUMPER.** 23.59 mm → **0.02 mm**, both ends,
symmetric to 0.002 mm, guarded TWO-SIDED as SPEC 10.90.
**`BAR_END_DROP` AND `BAR_END_BACK` ARE RETIRED.** **`BAR_HALF_Y` IS DERIVED**
(0.574387) **FROM A FROZEN TIP** (`BAR_TIP_Y` = 0.629528, written as the OLD
FORMULA so the equality is provable). **DO NOT TURN `BAR_HALF_Y` BACK INTO A
FREE CONSTANT.**
**`BLADE_TOP_Z` IS NOT THE LANDING DATUM** — it is the blade's CROWN, and the
channel top slopes **2.30 mm** away from it at the tube's station. Landing on it
is a 2.32 mm gap. **`BLADE_TOP_Z` ITSELF MUST STAY PUT** — it anchors `BAR_Z`
and verify.py's over-rider row.
**`BEND_R_RATIO` = 1.35 IS A LOWER BOUND AND `BEND_THETA` = 69° AN UPPER BOUND**,
both image-space. **Do not quote them as 3-D readings.**

**`u 205–208` IS A POST, NOT THE BAR'S FAR END** *[stated, rev 36]*. It was put
to me twice under the wrong label (rev 33 Q1, rev 34 Q1b). **My readings stand;
the label was wrong.** §10.88's retirement of the cross-ratio turned on *"the
strut sits 1.5 px from the bar's far end"* — a statement about a feature that is
not there. **DO NOT RE-CONSUME THAT COLUMN UNDER THE OLD LABEL.**

**THERE ARE TWO POSTS AND NEITHER IS ON THE CENTRELINE.** §10.83's five-revision
question dissolves — **it assumed there was one.** **REPORTED AS SUGGESTIVE, NOT
ESTABLISHED**: 41:1 against the null, and the residual **crosses the band
boundary** between the two available readings of the near post (0.73 band at
362.5, **1.23 at 365.5**). **DO NOT PROMOTE IT.**

**THE BAR'S SPAN IS A LOWER BOUND, NOT A READING** — it continues past the far
post and wraps out of sight. **A THIRD ESTIMATOR WAS ENUMERATED AND ABANDONED
BEFORE IT WAS BUILT**: it needs the centreline's image AT THE BAR'S HEIGHT AND
DEPTH, and `u 288.8` is the V-swage apex at a different height and depth —
**the same missing feature that killed §10.89's route.** **DO NOT OPEN IT.**

**THE NEAR JUNCTION IS UNOBSERVED.** Rows **725–732** at cols 470–510 carry
ZERO white and 50 % dark — a black workshop frame member. **Rev 35 reported "one
continuous white path" there; it read a junction THROUGH an occlusion**, and its
crop stopped at v 730, inside the band. **Its negative control matters: clear
body reads zero white too, so ZERO WHITE ALONE PROVES NOTHING.**

**A SQUARE-ON FRAME OF THE FRONT still collapses the post entirely**, is still
the only thing that could bound the camera's roll, and is now **also the only
thing that could close the bar's span.**
Everything else from the rev-36 prompt's settled list stands unchanged: REF §9's
V-swage bracket ≈0.40–0.49 m; `422 px/m` consumed nowhere; no recoverable
fore-aft VP; the camera's roll unestablished on this frame.

## Hard-won rules — every one was learned by breaking it
Every rule in the rev-36 prompt still stands. **NEW in rev 36:**
* **A DERIVATION IS ONLY AS GOOD AS THE DATUM IT LANDS ON.** The tangency
  algebra was right and the result was 2.32 mm wrong, because `BLADE_TOP_Z` is
  the blade's crown and the tube does not stand at the crown. **ASK WHAT A
  NAMED CONSTANT IS THE MAXIMUM OF BEFORE YOU LAND ANYTHING ON IT.**
* **A GUARD'S FAILURE MESSAGE IS A CLAIM AND MUST BE FALSIFIED LIKE ONE.**
  ARM 3 drove the tube THROUGH the bumper and the guard failed correctly while
  printing *"floats 77.38 mm"* — the opposite of what happened. **CAUGHT BY
  READING THE ARM'S OUTPUT, NOT BY NOTING THAT IT WENT RED.**
* **A NUMERICAL WORKAROUND CAN BECOME THE SHAPE.** The hoop stopped at 0.62 of
  a quarter turn to dodge a singularity in `sweep()`. Six revisions later that
  was the defect I reported. **WHEN A COMMENT GIVES A NUMERICAL REASON FOR A
  GEOMETRIC CONSTANT, THAT CONSTANT IS UNGROUNDED BY DEFINITION.**
* **A CLAIM READ OFF A CONSTANT WHOSE CONSUMER MODIFIES IT IS NOT A
  MEASUREMENT.** Rev 35's "no render needed" is the whole error in four words.
* **A FIGURE THE READER CANNOT PARSE HAS MEASURED NOTHING.** See Step 5.
* **THE LABEL YOU ATTACH TO A COLUMN IS PART OF THE QUESTION.** Two of my
  answers were consumed for four revisions under a name for a feature that is
  not there. **NAME WHAT YOU ARE POINTING AT, AND LET ME CORRECT THE NAME.**

---
> **THE STANDARD, in the owner's words.** The final product should be nearly
> indistinguishable from the original. **Any single measurement off is
> unacceptable.** The criterion is PER-MEASUREMENT. And above clinical
> accuracy: *"I want the owner to remember standing in the kombi, in this very
> picture that was provided."* — **that owner is the restaurant's owner.**
---

## 1. Restore and verify — BY CONTENT, never by hash or commit count
```bash
git clone tacombi_history_rev9.bundle tacombi && cd tacombi
git pull --ff-only ../tacombi_rev14_unified.bundle HEAD          # -> 59
git fetch ../tacombi_rev14b_incremental.bundle HEAD:refs/heads/b14   # FETCH, BEFORE rev15
git pull --ff-only ../tacombi_rev15_incremental.bundle HEAD      # -> 67
git pull --ff-only ../tacombi_rev16_incremental.bundle HEAD      # -> 71
git pull --ff-only ../tacombi_rev17_incremental.bundle HEAD      # -> 75
git pull --ff-only ../tacombi_rev18_incremental.bundle HEAD      # -> 81
git pull --ff-only ../tacombi_rev19_incremental.bundle HEAD      # -> 87
git pull --ff-only ../tacombi_rev20_incremental.bundle HEAD      # -> 93
git pull --ff-only ../tacombi_rev21_incremental.bundle HEAD      # -> 96
git pull --ff-only ../tacombi_rev22_incremental.bundle HEAD      # -> 101
git pull --ff-only ../tacombi_rev23_incremental.bundle HEAD      # -> 105
git pull --ff-only ../tacombi_rev24_incremental.bundle HEAD      # -> 107
git pull --ff-only ../tacombi_rev25_incremental.bundle HEAD      # -> 115
git pull --ff-only ../tacombi_rev26_incremental.bundle HEAD      # -> 120
git pull --ff-only ../tacombi_rev27_incremental.bundle HEAD      # -> 126
git pull --ff-only ../tacombi_rev28_incremental.bundle HEAD      # -> 130
git pull --ff-only ../tacombi_rev29_incremental.bundle HEAD      # -> 135
git pull --ff-only ../tacombi_rev30_incremental.bundle HEAD      # -> 148
git pull --ff-only ../tacombi_rev31_incremental.bundle HEAD      # -> 158
git pull --ff-only ../tacombi_rev32_incremental.bundle HEAD      # -> 166
git pull --ff-only ../tacombi_rev33_incremental.bundle HEAD      # -> 173
git pull --ff-only ../tacombi_rev34_incremental.bundle HEAD      # -> 182
git pull --ff-only ../tacombi_rev35_incremental.bundle HEAD      # -> 187
git pull --ff-only ../tacombi_rev36_incremental.bundle HEAD      # -> 190
```
**If a pull says "Need to specify how to reconcile divergent branches", STOP.**
The hero is gitignored and lives only on my disk.

```bash
git status                                                   # clean
grep -c '^### 10.90' SPEC.md                                 # 1   rev 36
grep -c '^#### 10.90' SPEC.md                                # 9   rev 36
grep -c '10.90' SPEC.md                                      # 14  rev 36
grep -c 'A NUMERICAL WORKAROUND HAD BECOME THE SHAPE' SPEC.md # 1  rev 36
grep -c 'THERE WAS ONE GAP, NOT TWO' SPEC.md                 # 1   rev 36
grep -c 'A THIRD TIME' SPEC.md                               # 1   rev 36
grep -c 'DATUM ERROR' SPEC.md                                # 1   rev 36
grep -c 'SUGGESTIVE, NOT ESTABLISHED' SPEC.md                # 1   rev 36
grep -c 'READING THE ARM' SPEC.md                            # 1   rev 36
grep -c 'OCCLUSION BAND' SPEC.md                             # 1   rev 36
grep -c 'BAR_TIP_Y' t1_detail.py                             # 2   rev 36
grep -c 'BEND_THETA' t1_detail.py                            # 13  rev 36
grep -c '_blade_top_at' t1_detail.py                         # 2   rev 36
grep -c 'DERIVED' t1_detail.py                               # 5   rev 36
grep -c 'BAR_END_DROP' t1_detail.py                          # 2   rev 36  RETIRED -- comments only
grep -c 'SPEC 10.90' verify.py                               # 7   rev 36
grep -c 'ORB_TANGENT_TOL' verify.py                          # 5   rev 36
grep -c 'DRIVEN' verify.py                                   # 3   rev 36
grep -c 'REFUSING TO PRINT A RULING' probe_rev36_barend.py   # 2   rev 36
grep -c 'RETIRED' probe_rev36_barend.py                      # 9   rev 36
grep -c 'FALSIFICATION' probe_rev36_posts.py                 # 2   rev 36
grep -c 'capped' probe_rev36_posts.py                        # 1   rev 36
grep -c 'OCCLUSION BAND' mark_rev36_ends.py                  # 2   rev 36
grep -c 'COALESCENCE' mark_rev36_ends.py                     # 2   rev 36
grep -c 'REFUSING TO WRITE' mark_rev36_ends.py               # 2   rev 36
ls HANDOFF_rev36.md STATE_rev36.md probe_rev36_barend.py probe_rev36_posts.py \
   mark_rev36_ends.py render_rev36_bumper.py rev36_ends.png rev36_ends_plain.png \
   rev36_barend_ab.png
grep -c '10.89' SPEC.md                                      # 9   MOVED BY 10.90 (was 8)
grep -c '10.88' SPEC.md                                      # 15  MOVED BY 10.90 (was 14)
grep -c '288.8' SPEC.md                                      # 12  MOVED BY 10.90 (was 9)
grep -c '^#### 10.89' SPEC.md                                # 5   ANCESTOR rev 35
grep -c 'UNDECIDED' SPEC.md                                  # 11  ANCESTOR rev 35
grep -c 'MISSING FEATURE' SPEC.md                            # 1   ANCESTOR rev 35
grep -c 'FOUR POINTS, THREE LINES' SPEC.md                   # 1   ANCESTOR rev 35
grep -c 'CHECKING THE PRECONDITION YOU WERE WARNED ABOUT' SPEC.md  # 1   ANCESTOR rev 35
grep -c 'u_lamp_far' probe_rev35_harmonic.py                 # 16  ANCESTOR rev 35
grep -c 'ORDERING WALL' mark_rev34_strutb.py                 # 4   ANCESTOR rev 34
grep -c 'CANDIDATE LINES' mark_rev34_strut.py                # 8   ANCESTOR rev 34
grep -c 'SYN_' probe_rev34_levels.py                         # 8   ANCESTOR rev 34
grep -c 'STRUT_U' probe_rev33_barend.py                      # 11  ANCESTOR rev 33
grep -c '288.8' REF_MEASUREMENTS.md                          # 4   ANCESTOR rev 32
grep -c 'UNDECIDED' verify.py                                # 3   ANCESTOR rev 32
grep -c '76.7' verify.py                                     # 2   ANCESTOR rev 32
grep -c 'ORB_RISE_SPEC' verify.py                            # 6   ANCESTOR rev 30
grep -c 'BAR_RATIO' t1_detail.py                             # 3   ANCESTOR rev 30
grep -c 'overrider_bar' build.py                             # 1   ANCESTOR rev 30
grep -c 'The threshold is not the parameter' post.py         # 1   ANCESTOR rev 13
```
**EVERY VALUE ABOVE WAS FILLED FROM A FRESH-CLONE VERIFICATION RUN.** Never
type one from memory — `grep -c` counts LINES, not occurrences.
**ANCHOR YOUR HEADING COUNTS WITH `^`.**
**THREE ROWS ARE MARKED "MOVED BY 10.90".**
*A grep count is invalidated by any later edit to the file it counts.*

Ancestry — **rev 36 adds `3496cab`, the rev-35 TIP:**
```bash
for c in f3c53f4 87aeaa6 d519fc6 5087b84 7ce3d03 f3cde44 efc1268 456b201 b08e424 e792d73 6f87977 cac32b9 2253399 52e451a 3496cab; do
  git merge-base --is-ancestor $c HEAD && echo "$c ok" || echo "$c LOST"; done
```
Texture md5s — **all three must match, and rev 36 changed NO artwork:**
```bash
md5sum tex/swirl.png tex/swirl_b.png tex/nose.png
# 4ee4e09e...   d201597e...   b31ea156...
```

## 2. Both guards, and the figures I watched print
| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 0 warn** | **0 fail, 0 warn** |
| audit.py | **0 fail, 0 warn** | **0 fail, 0 warn** |
| roof crown @ rear axle | **1.9835** | **1.9833** |
| rear arch lip → gap | **0.3722 → 39.7 mm** | same |
| front arch (control) | **0.3732 → 40.7 mm** | same |
| rake | **17.75 mm/m (locked 17.75)** | same |
| dims | L=4.065 W=1.750 | same |
| cut roof hole | **68564v** | **252749v** |
| objects at `materials:` | **127** | **127** |
| shut line × aperture, SHOW / OFF | **0.0 mm / 804.9 mm** | same |
| `CARGO_GAP` samples | **154** | same |
| bay widths | **0.516 0.515 0.516** | same |
| over-rider row | **97.51 mm above the blade top, dia 24.97 mm** | same |
| **over-rider hoop ends (NEW)** | **0.02 / 0.02 mm residual, tol 1.0, TWO-SIDED** | same |

Also: **186 meshes**; 42 materials; 5 constant-rough; **0 non-manifold**;
band 1.372–1.775. **EVERY INHERITED GEOMETRY FIGURE IS IDENTICAL TO REV 30–35's**
— the bar's tip was frozen precisely so this stayed true.

Probe controls on the fresh clone: `probe_rev36_barend.py` **8 / 0**;
`probe_rev36_posts.py` **5 / 0**; `probe_rev35_harmonic.py` **18 checked, 6
FAILED — H3, H5, G1, G3, B2, B3, and ALL SIX ARE THE RESULT**;
`probe_rev34_levels.py` **8 / 4**; `probe_rev34_ruling.py` **6 / 4**;
`probe_rev33_barend.py` **7 / 4**; `probe_orb_xratio.py` **6 / 1**;
`probe_rev32_pointer.py` **10 / 0**; `probe_dust_scope.py` **8 / 0**;
`probe_updust_pointer.py` **6 / 0**; `probe_psf_lines.py` **2 FAILED, both
EXPECTED**; `probe_clean_top.py` and `probe_dust_anchor.py` **DELIBERATELY
LEFT FAILING**. **Do not "fix" any of these.**

## 3. What rev 36 changed — `HANDOFF_rev36.md` has the full account
- **`t1_detail.py`** — BUILD FILE. `overrider_bar()` rewritten; `BAR_END_DROP`
  and `BAR_END_BACK` RETIRED; `BAR_LEG_LEN` and `BAR_HALF_Y` DERIVED;
  `BAR_TIP_Y` FROZEN; `_blade_top_at()` added.
- **`verify.py`** — BUILD FILE. SPEC 10.90's two-sided ray-cast guard.
- **`SPEC.md`** — NEW §10.90, nine parts.
- **`STATE.md`** — regenerated on the clean rev-36 tree at `7c74e57`,
  `working tree | clean`. **`STATE_rev36.md`** alongside.
- **NEW, all read-only**: `probe_rev36_barend.py`, `probe_rev36_posts.py`,
  `mark_rev36_ends.py`, `render_rev36_bumper.py`, `HANDOFF_rev36.md`,
  `rev36_ends.png`, `rev36_ends_plain.png`, `rev36_barend_ab.png`.
- **NO SHADER. NO ARTWORK. `build.py` UNTOUCHED.**

## 4. Still open
- **THE HERO IS OWED.** `rev30_hero34f.png` is SUPERSEDED — the geometry moved.
- **`probe_clean_top.py` and `probe_dust_anchor.py` need REWRITING, not
  fixing.** **FOUR revisions now.** **Do not widen a tolerance.**
- **THE BAR'S SPAN.** Lower bound only. Only a square-on front frame closes it.
- **§10.70's percentages must be RE-RUN** before being quoted again. The
  harness has **no cyclorama** (§10.78) — state that, do not silently fix it.
- **REF §9's V-SWAGE ABSOLUTE HEIGHT is a bracket, ≈0.40–0.49 m.**
- **THE FRONT BUMPER FACE IS UNMEASURED. `CREAM`. THE ABSOLUTE ROOF HEIGHT.
  THE OFF FLANK, 804.9 mm.** `COUNTERTAN` 34.0 % short in B.
- `GAL_SKY` dead lever. `PLATE_W = 0.3300` no provenance.
  `probe_rev16.py:90` prints `xa` vs `xa`.

## 5. FIRST QUESTION FOR THE OWNER
**NO QUESTION IS OUTSTANDING WITH ME.** Rev 36 spent one and I answered it, and
my answer was **none of its four options** — which is what produced §10.90.5
through §10.90.7. **Before you ask me anything, say what it can close.**

What would still move the most is one photograph: **a head-on rear (or front)
elevation from roof height or above, with the counter and the lids clear of the
section** — the only realistic route to closing `CREAM`, the absolute roof
height and the B residual. A clear view of the **off flank** closes 804.9 mm.
**And any frame showing the FRONT of the vehicle square-on now closes THREE
things: the post, the camera's roll, and the bar's span.**

## 6. Ordered work list for rev 37
1. **SHOOT THE HERO.** It is genuinely owed for the first time since rev 30 —
   the geometry moved and `rev30_hero34f.png` no longer depicts this build.
   §7 has the strip procedure. **Do not re-use the rev-30 file as current.**
2. **REWRITE `probe_clean_top.py` AND `probe_dust_anchor.py`**, or retire them
   with a stated reason. Decide first what the post-retirement question is.
   **Do not widen a tolerance.** This has slipped FOUR revisions.
3. **Re-run §10.70's arms** on the post-retirement build before quoting any of
   its percentages, then the scene→top bounce.
4. Tail-lamp material slot; `Senor`'s letterforms; `SCR`'s +80 mm.
5. **THE BAR'S SPAN AND THE POST ONLY IF A NEW PHOTOGRAPH ARRIVES.**
6. Camera absolutely last.

## 7. THE COMMIT COUNT AND THE CONTENT FIGURES
This section is written LAST, after the final commit, and every figure in §1
was read off a fresh-clone verification run rather than typed from memory.
**This has gone wrong in ELEVEN revisions during handoff assembly.**

**FINAL COUNT: 190 commits, clean tree.** *(Verified: this line lands in commit
190 itself, which is what makes it true — rev 29's pattern, kept since.)*

**THE GREP TRAP FIRED AGAIN AND THE VERIFICATION RUN CAUGHT IT — INCLUDING ONE
OF A NEW KIND.** §10.90's own text moved three inherited counts: `10.89`
**8 → 9**, `10.88` **14 → 15**, `288.8` **9 → 12**, all marked above. **AND A
FOURTH, WHICH WAS MINE:** I proposed
`grep -c 'THE SAME MISSING FEATURE, A THIRD TIME'` as a rev-36 anchor and it
returns **0**, because SPEC wraps that sentence across a line break and
**`grep -c` matches LINES.** Replaced with `'A THIRD TIME'`, which is on one
line and returns 1. **A GREP ANCHOR IS A PROBE TOO — AND A MULTI-LINE ONE
CANNOT FIRE.** Fourteenth revision the trap has fired.
