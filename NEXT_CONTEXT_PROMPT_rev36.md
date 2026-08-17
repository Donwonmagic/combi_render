# NEXT CONTEXT PROMPT — rev 36
Please act as my expert. Continue the Señor Tacombi combi build. **Thirty-five
revisions sit behind this.** You are picking up mid-stream, not starting.
## Step 0 — CHECK A FOLDER IS CONNECTED BEFORE YOU PLAN ANYTHING
Call `get_device_info`. **In rev 32, 33, 34 AND rev 35 `~/Desktop/tacombi_bus_render`
was ALREADY in `connectedFolders` on the first call** — four in a row. It timed
out unanswered in rev 28/29 and was granted on the first request in rev 30/31.
**Do not assume any of those outcomes** — call it, and say plainly what came back.
**THE BRIDGE HAS A THROUGHPUT CEILING, NOT JUST A SIZE ONE — CONFIRMED SIX
TIMES.** `device_stage_files` times out above ~3 MB. **Only TWO files need
splitting:** the 19.5 MB base bundle (7 parts) and the 8.5 MB `rev14_unified`
(3 parts). **Everything rev15–rev35 is under 3 MB and crosses whole**
(rev 35's bundle is 711 KB, the smallest since rev 28).
**REV 34 AND REV 35 BOTH REUSED REV 33's `_xfer33/` SPLIT PARTS** rather than
re-splitting. They are still on his disk and md5-verified on both sides in
rev 35. Check they are there before spending `device_bash` calls.
**REV 33, 34 AND 35 ALL CROSSED WITH ZERO TRANSIENT FAILURES** — rev 35 moved
31 files in **9 bridge calls**. Do not read that as the new normal: rev 32 had
two `upload failed` in one batch that both crossed on a single retry, and a
`device_bash` 502 that worked on retry. **TRANSIENT FAILURES ARE NOT DROPS**,
and the bridge also genuinely drops (three times in rev 31). Do not retry in a
loop; do cloud-side work and come back.
**`device_bash` DOES NOT SEE `/Users/...`.** The mount is
`/sessions/<session-id>/mnt/tacombi_bus_render`. **`device_stage_files` DOES
take the `/Users/...` path** — different roots, not a typo. **AND YOUR SHELL'S
`~` IS `/root`.** Use absolute paths.
**`hero.py` IS NOT A BLENDER SCRIPT.** It is a plain Python driver that invokes
Blender itself; `blender -b --python hero.py` fails with *unrecognized
arguments*. To render a preview, drive `build.py` the way `hero.py` drives a
strip:
```bash
T1_SUB=1 T1_PREVIEW=hero34f T1_FX=0 T1_RX=900 T1_RY=600 T1_SAMP=24 \
  T1_OUT=/tmp/prev T1_PFX=pv blender -b --python build.py
```
**That took 79.3 s in rev 35, not the 71 s every prompt since rev 33 has said.**
`hero.py`'s `BLENDER` constant already points at `/tmp/blender/blender`.
**`ref_workshop.jpg`, `ref_side.jpg` and `ref_rear34.jpg` are IN THE REPO.**
## Step 1 — read my memory BEFORE you read any code
`/areas/tacombi-combi-3d.md`, then `-rev14`, `-rev17` … `-rev34`, then
**`/areas/tacombi-combi-3d-rev35.md`** (SEPARATE FILES; each revision's file
does NOT carry the next), then `/areas/tacombi-combi-sticker.md`, then
`/preferences.md`. If you cannot read them, say so explicitly.
**I have never stood in the bus.** The "remember standing in the kombi" bar is
about the RESTAURANT'S owner. **Do not ask me what the real vehicle looks like.**
Ask me what a PHOTOGRAPH shows — that has now paid off twenty-six times.
**REV 35 ASKED ME NOTHING, and that was correct** — see §5.
## Step 2 — restore, and verify BY CONTENT (never by hash or commit count)
See §1. **TWENTY-THREE bundle lines now, and the rev14b line is a `fetch` that
must come BEFORE rev15.** rev 20 through rev 35 all restored CLEAN.
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
**THE GUARDS ARE 0 fail / 0 WARN.** **NO GEOMETRY MOVED IN REV 31–35** — the
last geometry change is still rev 30's. **THE HERO IS NOT OWED:
`rev30_hero34f.png` IS A RENDER OF THE REV-30 BUILD.** Do not re-shoot it.
**RUN THE PROBES YOU INHERIT, NOT ONLY THE ONES YOU WRITE.** **THERE ARE NOW
23 `probe_*.py` FILES** (rev 35 inherited 22 and wrote 1). rev 32 found one
failing a control since rev 30; rev 33 found two more, one DEGENERATE; rev 34
found the brief's own sentence about them wrong; **rev 35 found its own H4
checking the wrong precondition.**
**SIX PROBES NEED BLENDER — BUT NOT THE SIX A GREP NAMES, AND REV 35 CONFIRMED
THIS BY EXECUTION RATHER THAN BY GREP.** Run under `blender -b --python`:
`probe_ctan_index`, `probe_dust_scope`, `probe_f90`, `probe_rev16`, **plus
`probe_cross_anatomy` and `probe_shutlines`, which import it TRANSITIVELY.**
Everything else under `/tmp/blender/4.5/python/bin/python3.11` — **including
`probe_clean_top` and `probe_dust_anchor`, whose only `bpy` is in a comment.**
**A grep gives two false positives and two false negatives and they CANCEL.**
**`probe_rev35_harmonic.py` runs standalone.**
## Step 4 — read, in this order
`STATE.md` → `SPEC.md` §10, then §10.9 through §10.89 → this file →
**`HANDOFF_rev35.md`** → `HANDOFF_rev34.md` → … → `AUDIT_rev18_loft.md` →
`LOFT_GROUND_rev15.md` → `AUDIT_rev12.md` → `REF_MEASUREMENTS.md`.
`STATE.md` is machine-written; **if it and any prose disagree, it is right —
BUT CHECK ITS PROVENANCE ROWS FIRST.** In rev 33 the committed `STATE.md` was
one revision stale. **rev 35's is current** — regenerated on the clean rev-35
tree at commit `0ecbe4f`, `working tree | clean`, with `STATE_rev35.md`
alongside. **It has a `working tree` row; if that says DIRTY, the file is not
a record of anything.**
**§10.89 IS REV 35's. IT MOVES NO GEOMETRY.** It does five things:
1. **GRADES THE HARMONIC-CONJUGATE ROUTE BEFORE SPENDING A QUESTION** and
   retires it — **on a MISSING FEATURE, not on precision.**
2. **FINDS `u_lamp_far = 236` HAS NO RECORDED DERIVATION ANYWHERE.**
3. **ASKS NOTHING, and proves in arithmetic that a question would close nothing.**
4. **PUBLISHES A REPLACEMENT AND THEN REFUTES IT WITH ITS OWN ADVERSARIAL
   AUDIT**, striking the magnitudes and keeping only the sign.
5. **RECORDS SIX DEFECTS OF MY OWN**, one of which is the revision's own H4.
## Step 5 — ASK ME WHAT THE PHOTOGRAPHS SHOW before you measure from them
This has now paid off twenty-six times. Show me a crop, mark the regions,
give me options, **print the crop box**, and **say plainly what each mark IS.**
rev 30's two marks were SAMPLING WINDOWS; rev 31's four were POINTERS; rev 32,
33, 34 used CANDIDATE LINES; rev 34 added an ORDERING WALL; **rev 35 added a
fifth class, MEASURED COLUMNS + ONE DERIVED MEAN, on a figure whose header
says NOT A QUESTION and which sought no answer.**
Show the photograph **BESIDE a render of the current build.**
**A CLASS GATE IS A PROBE TOO, and so is a BRIEF, a TARGET, a SUBAGENT'S
FINDING, A CITATION, A GUARD YOU JUST WROTE, AN ESTIMATOR YOU JUST BUILT,
A QUESTION YOU ARE ABOUT TO ASK ME, A THRESHOLD, A SAMPLING WINDOW, A NULL
PATCH, A REFUTATION SOMEONE ELSE ALREADY BANKED, THE AXIS YOUR DETECTOR
SEARCHES ALONG, A LINE IN THE WORK LIST, A FALSIFICATION ARM YOU JUST RAN,
THE ARITHMETIC PRINTED UNDER A FIGURE, A PRE-COMMITMENT YOU JUST MADE, THE
UNITS YOUR TOLERANCE IS STATED IN, THE DETECTOR THAT TELLS YOU WHICH FILES A
RULE APPLIES TO, and — NEW, rev 35 — **THE LIST OF PRECONDITIONS YOU THINK A
CONSTRUCTION HAS**, and **A FIGURE YOU HAVE ALREADY SENT ME.**
**DO NOT ASK ME WHAT MEASUREMENT CAN ANSWER.** **AND MY ANSWER MAY NOT BE ONE
OF YOUR OPTIONS.** **IF I PICK THE FIRST OR LAST OPTION, YOUR SET PROBABLY DID
NOT REACH FAR ENOUGH — ask a bounded follow-up before you consume the answer,
BUT CHECK WHETHER THE ENDPOINT IS AGAINST A WALL FIRST.**
## Step 6 — the work
§6 below is the ordered list. **THE POST IS NO LONGER ITEM 1.** Both routes on
this panel are now retired. **Do not open a third estimator on this frame.**
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
Everything in the rev-35 prompt's equivalent section still stands, **with these
changes.**
**THE HARMONIC-CONJUGATE ROUTE IS RETIRED.** Not for precision — **its third
input does not exist.** The construction needs the two lamps AND their
midpoint's image; **there is no feature at the centre of the headlamp line.**
§10.86 substituted the V apex, 0.625 m below that line at an unrecorded depth.
Sweeping the VP over its whole admissible range leaves the midpoint **free over
67.8 px** and `t` over **0.8483 half-widths, 17× the level.**
**BOTH ROUTES ON THIS PANEL ARE NOW RETIRED, EACH ON A PRECONDITION.**
**`u_lamp_far = 236` HAS NO RECORDED DERIVATION.** §10.86's prose and
`HANDOFF_rev32.md` only — not `REF_MEASUREMENTS.md`, not any probe. **It is
LEFT with an EMPTY provenance string in `probe_rev35_harmonic.py`, which is what
makes H5 fail. Do not fill it in from the prose.**
**§10.86's `≈266` IS STALE** — computed with the far bar end at u ≈ 209, which
my answers replaced with u ∈ (205, 208]. At u 205 it is **261.2**.
**§10.83's "post at the vehicle's centreline" MOVES FROM UNDECIDED TO SIGN
ESTABLISHED, MAGNITUDE NOT.** The post is on the **NEAR side of the bar's 3-D
midpoint** — and only under the bar's symmetry about the centreline, whose only
check disagrees at 17 %. **THE MAGNITUDES 0.1464 AND 0.0595 ARE WITHDRAWN, NOT
RE-SCOPED. Do not reinstate them with a caveat.** **THE POST STAYS UNBUILT.**
**THE BAR'S FOUR READ POINTS ARE NOT COLLINEAR IN 3-D.** `u 485` is the HOOP's
outer column and `t1_detail.py`'s arc puts its generating point **53.7 mm below
and 17.5 mm behind** the far reading's line; the post's column was read on rows
676–700 against a bar top edge at v 672.5. **FOUR POINTS, THREE LINES.**
**THE CAMERA'S ROLL IS UNESTABLISHED AND CANNOT BE ESTABLISHED ON THIS FRAME** —
normalising the bar to 205/485 and projecting the build's own headlamp centres
misses by **47 px**, best-in-grid 45 px over 3344 poses. **That reproduces REF
§9's own "a fitted projection model did not close" FROM THE MODEL SIDE.**
**REF §9's V-SWAGE ABSOLUTE HEIGHT IS A BRACKET** ≈0.40–0.49 m. **`422 px/m`
IS CONSUMED NOWHERE.** **THE VEHICLE HAS NO RECOVERABLE FORE-AFT VANISHING
POINT.** **THE FRONT OVER-RIDER BAR IS BUILT, WORKSHOP-STAGE**; `BAR_DIA` and
`BAR_RISE` are `ratio × APERTURE_M` and **`BAR_RISE` IS NOT A LITERAL** — arm
`BAR_RISE_RATIO`. **THE HERO IS SHOT AND PROVED BY CONTENT.**
**A SQUARE-ON FRAME OF THE FRONT still collapses the post entirely, and after
§10.89 it is ALSO the only thing that could bound the camera's roll.**
## Hard-won rules — every one was learned by breaking it
Every rule in the rev-35 prompt still stands. **NEW in rev 35:**
* **CHECKING THE PRECONDITION YOU WERE WARNED ABOUT IS NOT CHECKING THE
  PRECONDITIONS.** §10.88.4 retired the cross-ratio on ORDERING, so rev 35's H4
  checked ordering — and PASSED, printing *"no consumed column sits against a
  precondition wall."* The violated precondition was COLLINEARITY. **Enumerate
  what the construction REQUIRES, not what the last revision found.**
* **A CONSTRUCTION CAN FAIL BECAUSE A FEATURE DOES NOT EXIST**, not because a
  reading is imprecise. Ask what the construction needs an IMAGE OF, and check
  that thing is actually in the frame, before grading anything.
* **A FIGURE YOU HAVE ALREADY SENT IS A PROBE TOO.** When a claim is withdrawn,
  the figure carrying it must be re-issued and the superseded issue named on
  the replacement. Do not let a sent figure outlive its number.
* **A BOUND THAT SAYS "FOR EVERY ADMISSIBLE CAMERA" IS A CLAIM ABOUT CAMERAS**
  and must enumerate what it quietly excludes. rev 35's excluded roll and post
  standoff and said it consumed "no camera model."
* **PRINT A MARGIN IN THE UNITS THE READER CAN CHECK.** rev 35's bound was
  20.5 px of post column at nominal against a post whose own extent is 21 px.
  **In half-widths it looked like a bound; in px it looks like a coincidence.**
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
```
**If a pull says "Need to specify how to reconcile divergent branches", STOP.**
The hero is gitignored and lives only on my disk.
**NOTE THE rev34 LINE.** Every prompt through rev 35 annotated it `-> 181`; it
is **182**, and rev 34's own §7 said so. **rev 35 caught it on the restore run.**
```bash
git status                                                   # clean
grep -c '^### 10.89' SPEC.md                                 # 1   rev 35
grep -c '^#### 10.89' SPEC.md                                # 5   rev 35
grep -c '10.89' SPEC.md                                      # 8   rev 35
grep -c 'CHECKING THE PRECONDITION YOU WERE WARNED ABOUT' SPEC.md  # 1   rev 35
grep -c 'FOUR POINTS, THREE LINES' SPEC.md                   # 1   rev 35
grep -c 'MISSING FEATURE' SPEC.md                            # 1   rev 35
grep -c 'REFUSING TO PRINT A RULING' probe_rev35_harmonic.py # 1   rev 35
grep -c 'WITHDRAWN' probe_rev35_harmonic.py                  # 4   rev 35
grep -c 'COLLINEARITY' probe_rev35_harmonic.py               # 2   rev 35
grep -c 'u_lamp_far' probe_rev35_harmonic.py                 # 16  rev 35
grep -c 'MEASURED COLUMNS' mark_rev35_bound.py               # 2   rev 35
grep -c 'REFUSING TO WRITE' mark_rev35_bound.py              # 2   rev 35
ls HANDOFF_rev35.md STATE_rev35.md probe_rev35_harmonic.py mark_rev35_bound.py rev35_bound.png
grep -c 'UNDECIDED' SPEC.md                                  # 11  MOVED BY 10.89 (was 10)
grep -c '10.88' SPEC.md                                      # 14  MOVED BY 10.89 (was 7)
grep -c '288.8' SPEC.md                                      # 9   MOVED BY 10.89 (was 8)
grep -c '^### 10.88' SPEC.md                                 # 1   ANCESTOR rev 34
grep -c '^#### 10.88' SPEC.md                                # 6   ANCESTOR rev 34
grep -c 'A TOLERANCE STATED IN THE UNITS OF THE MEASUREMENT' SPEC.md   # 1   ANCESTOR rev 34
grep -c 'A DETECTOR WHOSE ERRORS CANCEL' SPEC.md             # 1   ANCESTOR rev 34
grep -c 'DEGENERATED TO THREE' SPEC.md                       # 1   ANCESTOR rev 34
grep -c 'ORDER BROKEN' probe_rev34_ruling.py                 # 2   ANCESTOR rev 34
grep -c 'ORDERING WALL' mark_rev34_strutb.py                 # 4   ANCESTOR rev 34
grep -c 'CANDIDATE LINES' mark_rev34_strut.py                # 8   ANCESTOR rev 34
grep -c 'SYN_' probe_rev34_levels.py                         # 8   ANCESTOR rev 34
grep -c '^### 10.87' SPEC.md                                 # 1   ANCESTOR rev 33
grep -c 'STRUT_U' probe_rev33_barend.py                      # 11  ANCESTOR rev 33
grep -c 'KILL' probe_rev33_barend.py                         # 11  ANCESTOR rev 33
grep -c '### 10.86' SPEC.md                                  # 1   ANCESTOR rev 32
grep -c '288.8' REF_MEASUREMENTS.md                          # 4   ANCESTOR rev 32
grep -c 'UNDECIDED' verify.py                                # 3   ANCESTOR rev 32
grep -c 'V_APEX_TOL' probe_orb_post.py                       # 12  ANCESTOR rev 32
grep -c '76.7' verify.py                                     # 2   ANCESTOR rev 32
grep -c 'ORB_RISE_SPEC' verify.py                            # 6   ANCESTOR rev 30
grep -c 'BAR_RATIO' t1_detail.py                             # 3   ANCESTOR rev 30
grep -c 'overrider_bar' build.py                             # 1   ANCESTOR rev 30
grep -c 'The threshold is not the parameter' post.py         # 1   ANCESTOR rev 13
```
**EVERY VALUE ABOVE WAS FILLED FROM A FRESH-CLONE VERIFICATION RUN.** Never
type one from memory — `grep -c` counts LINES, not occurrences.
**ANCHOR YOUR HEADING COUNTS WITH `^`.** `grep -c '### 10.89'` is **6**, not 1.
**THREE ROWS ARE MARKED "MOVED BY 10.89"** — §10.89 cites §10.88 repeatedly and
mentions UNDECIDED and 288.8. *A grep count is invalidated by any later edit to
the file it counts — including a later revision's.*
Ancestry — **rev 35 adds `52e451a`, the rev-34 TIP:**
```bash
for c in f3c53f4 87aeaa6 d519fc6 5087b84 7ce3d03 f3cde44 efc1268 456b201 b08e424 e792d73 6f87977 cac32b9 2253399 52e451a; do
  git merge-base --is-ancestor $c HEAD && echo "$c ok" || echo "$c LOST"; done
```
Texture md5s — **all three must match, and rev 35 changed NO artwork:**
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
Also: **186 meshes**; 42 materials; 5 constant-rough; **0 non-manifold**;
band 1.372–1.775. **EVERY GEOMETRY FIGURE IS IDENTICAL TO REV 30–34's.**
Probe controls on the fresh clone: `probe_rev35_harmonic.py` **18 checked, 6
FAILED — H3, H5, G1, G3, B2, B3, and ALL SIX ARE THE RESULT**;
`probe_rev34_levels.py` **8 / 4**; `probe_rev34_ruling.py` **6 / 4**;
`probe_rev33_barend.py` **7 / 4**; `probe_orb_xratio.py` **6 / 1**;
`probe_rev32_pointer.py` **10 / 0**; `probe_dust_scope.py` **8 / 0**;
`probe_updust_pointer.py` **6 / 0**; `probe_psf_lines.py` **2 FAILED, both
EXPECTED**; `probe_clean_top.py` and `probe_dust_anchor.py` **DELIBERATELY
LEFT FAILING**. **Do not "fix" any of these.**
## 3. What rev 35 changed — `HANDOFF_rev35.md` has the full account
- **`SPEC.md`** — NEW §10.89, five parts.
- **`STATE.md`** — regenerated on the clean rev-35 tree at `0ecbe4f`,
  `working tree | clean`. **`STATE_rev35.md`** written alongside.
- **`probe_rev35_harmonic.py`**, **`mark_rev35_bound.py`**,
  **`rev35_bound.png`**, **`HANDOFF_rev35.md`** — all NEW, all READ-ONLY.
- **NO GEOMETRY. NO SHADER. NO ARTWORK. NO BUILD FILE TOUCHED AT ALL** —
  rev 35 is the first revision since rev 29 to change nothing outside docs and
  probes, not even a constant.
## 4. Still open
- **THE POST — BOTH ROUTES ON THIS PANEL ARE RETIRED.** Do not open a third
  estimator here. **Only a square-on frame of the FRONT closes it.**
- **`probe_clean_top.py` and `probe_dust_anchor.py` need REWRITING, not
  fixing.** rev 35 did not reach them. **Do not widen a tolerance.**
- **§10.70's percentages must be RE-RUN** before being quoted again. The
  harness has **no cyclorama** (§10.78) — state that, do not silently fix it.
- **REF §9's V-SWAGE ABSOLUTE HEIGHT is a bracket, ≈0.40–0.49 m.**
- **THE FRONT BUMPER FACE IS UNMEASURED. `CREAM`. THE ABSOLUTE ROOF HEIGHT.
  THE OFF FLANK, 804.9 mm.** `COUNTERTAN` 34.0 % short in B.
- `GAL_SKY` dead lever. `PLATE_W = 0.3300` no provenance.
  `probe_rev16.py:90` prints `xa` vs `xa`.
## 5. FIRST QUESTION FOR THE OWNER
**NO QUESTION IS OUTSTANDING WITH ME. REV 35 ASKED ME NOTHING AT ALL** — the
first revision since rev 30 to spend none, and it said why in arithmetic rather
than deferring: the only ungraded column on the panel does not enter the
surviving result, so a reading of it would have bought a column, not an answer.
**Before you ask me anything, say what it can close.**
What would still move the most is one photograph: **a head-on rear (or front)
elevation from roof height or above, with the counter and the lids clear of the
section** — the only realistic route to closing `CREAM`, the absolute roof
height and the B residual. A clear view of the **off flank** closes 804.9 mm.
**And for the POST: any frame showing the FRONT of the vehicle square-on is now
the ONLY thing that closes it — and the only thing that could bound the
camera's roll, which §10.89.3 shows this frame cannot.**
## 6. Ordered work list for rev 36
1. **REWRITE `probe_clean_top.py` AND `probe_dust_anchor.py`**, or retire them
   with a stated reason. Decide first what the post-retirement question is.
   **Do not widen a tolerance.** This has slipped three revisions.
2. **Re-run §10.70's arms** on the post-retirement build before quoting any of
   its percentages, then the scene→top bounce.
3. Tail-lamp material slot; `Senor`'s letterforms; `SCR`'s +80 mm.
4. **THE POST ONLY IF A NEW PHOTOGRAPH ARRIVES.** Not otherwise.
5. Camera absolutely last.
## 7. THE COMMIT COUNT AND THE CONTENT FIGURES
This section is written LAST, after the final commit, and every figure in §1
was read off a fresh-clone verification run rather than typed from memory.
**This has gone wrong in ELEVEN revisions during handoff assembly.**
**FINAL COUNT: 187 commits, clean tree.** *(Verified: this line lands in commit
187 itself, which is what makes it true — rev 29's pattern, kept since.)*
**THE GREP TRAP FIRED AGAIN, THREE TIMES, AND THE FRESH-CLONE RUN CAUGHT ALL
THREE.** §10.89's own text moved three inherited counts: `UNDECIDED` in SPEC
**10 → 11**, `10.88` in SPEC **7 → 14**, `288.8` in SPEC **8 → 9**. Nothing was
wrong when written. Marked "MOVED BY 10.89" above. **Thirteenth revision.**
**AND ONE OF MY SIX FALSIFICATION ARMS DID NOTHING ON THE FIRST TRY.** ARM 5
was aimed at `swing()`'s unreachable path and returned a finite **0.9474**,
because the band I chose missed the singularity by 0.002 px. **Caught by
printing the changed line and reading the number.** Re-armed on an exact binary
coincidence (`365.5 + 119.5 == 485.0`) it prints **`n/a` / UNREACHABLE**.
**Fourth revision running that an arm has failed to apply.**
