# NEXT CONTEXT PROMPT — rev 34
Please act as my expert. Continue the Señor Tacombi combi build. **Thirty-three
revisions sit behind this.** You are picking up mid-stream, not starting.
## Step 0 — CHECK A FOLDER IS CONNECTED BEFORE YOU PLAN ANYTHING
Call `get_device_info`. **In rev 32 AND rev 33 `~/Desktop/tacombi_bus_render`
was ALREADY in `connectedFolders` on the first call.** It timed out unanswered
in rev 28 and rev 29 and was granted on the first request in rev 30 and rev 31.
**Do not assume any of those outcomes** — call it, and say plainly what came
back.
**THE BRIDGE HAS A THROUGHPUT CEILING, NOT JUST A SIZE ONE — CONFIRMED FOUR
TIMES.** `device_stage_files` times out above ~3 MB. **Only TWO files need
splitting:** the 19.5 MB base bundle (7 parts) and the 8.5 MB `rev14_unified`
(3 parts). **Everything rev15–rev33 is under 3 MB and crosses whole.**
**IN REV 33 ALL 26 FILES CROSSED WITH ZERO TRANSIENT FAILURES — A FIRST.** Do
not read that as the new normal: rev 32 had two `upload failed` in one batch
that both crossed on a single retry, and a `device_bash` 502 that worked on
retry. **TRANSIENT FAILURES ARE NOT DROPS**, and the bridge also genuinely
drops (three times in rev 31, each recovering on its own). Do not retry in a
loop; do cloud-side work and come back.
**`device_bash` DOES NOT SEE `/Users/...`.** The connected folder is mounted at
`/sessions/<session-id>/mnt/tacombi_bus_render`. `pwd` then `ls mnt/` finds it.
rev 33 lost a call to this. **`device_stage_files` DOES take the `/Users/...`
path** — the two tools take different roots and that is not a typo.
**AND YOUR SHELL'S `~` IS `/root`, NOT `/home/claude`.** The `Read` tool needs
the real path. rev 33 lost a call to that too.
**`ref_workshop.jpg`, `ref_side.jpg` and `ref_rear34.jpg` are IN THE REPO**, so
all reference measurement survives an outage.
## Step 1 — read my memory BEFORE you read any code
`/areas/tacombi-combi-3d.md`, then `-rev14`, `-rev17` … `-rev32`, then
**`/areas/tacombi-combi-3d-rev33.md`** (SEPARATE FILES; each revision's file
does NOT carry the next), then `/areas/tacombi-combi-sticker.md`, then
`/preferences.md`. If you cannot read them, say so explicitly.
**I have never stood in the bus.** The "remember standing in the kombi" bar is
about the RESTAURANT'S owner. **Do not ask me what the real vehicle looks
like.** Ask me what a PHOTOGRAPH shows — that has now paid off twenty-four
times.
## Step 2 — restore, and verify BY CONTENT (never by hash or commit count)
See §1. **TWENTY-ONE bundle lines now, and the rev14b line is a `fetch` that
must come BEFORE rev15.** rev 20 through rev 33 all restored CLEAN — do not
assume either way, check.
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
**THE GUARDS ARE 0 fail / 0 WARN.** **NO GEOMETRY MOVED IN REV 31, 32 OR 33** —
the last geometry change is still rev 30's. **THE HERO IS NOT OWED:
`rev30_hero34f.png` IS A RENDER OF THE REV-30 BUILD.** Do not re-shoot it.
**AND RUN THE PROBES YOU INHERIT, NOT ONLY THE ONES YOU WRITE.** rev 32 found
`probe_dust_scope.py` failing one of its own controls since rev 30. **rev 33
found TWO MORE** — and one of them is not merely failing, it is DEGENERATE
(§10.87.2). **Six of the twenty-five probes need `bpy` and must be run under
`blender -b --python`, not the bundled standalone python** — running them the
wrong way gives `ModuleNotFoundError`, which reads like a broken probe and is
not one.
## Step 4 — read, in this order
`STATE.md` → `SPEC.md` §10, then §10.9 through §10.87 → this file →
**`HANDOFF_rev33.md`** → `HANDOFF_rev32.md` → … → `AUDIT_rev18_loft.md` →
`LOFT_GROUND_rev15.md` → `AUDIT_rev12.md` → `REF_MEASUREMENTS.md`.
`STATE.md` is machine-written; **if it and any prose disagree, it is right —
BUT CHECK ITS PROVENANCE ROWS FIRST.** In rev 33 the committed `STATE.md` was
byte-identical to `STATE_rev31.md` and named a rev-31b commit, because rev 32
never re-committed it (§10.87.3). **It also has a `working tree` row; if that
says DIRTY, the file is not a record of anything.**
**§10.87 IS REV 33's. IT MOVES NO GEOMETRY.** It does five things:
1. **CLOSES §10.82's NAMED GAP** on my all-clean answer to Q2.
2. **FINDS TWO INHERITED PROBES DEGENERATE**, one printing a tautology as a
   comparison.
3. **CORRECTS REV 32's Q1 FIGURE**, which quoted a PLANTED SYNTHETIC value as
   a measurement.
4. **TAKES MY Q1/Q1b ANSWERS, CLOSES THE FAR END WITH THEM — and still rules
   the post UNBUILDABLE**, on a fourth column nobody ever measured.
5. **RECORDS `STATE.md`'s staleness BEFORE fixing it.**
## Step 5 — ASK ME WHAT THE PHOTOGRAPHS SHOW before you measure from them
This has now paid off twenty-four times. Show me a crop, mark the regions,
give me options, **print the crop box**, and **say plainly what each mark IS.**
rev 30's two marks were SAMPLING WINDOWS; rev 31's four were POINTERS; rev 32
and rev 33 used CANDIDATE LINES, a third class that is neither — and every
figure said which.
Show the photograph **BESIDE a render of the current build**.
**A CLASS GATE IS A PROBE TOO, and so is a BRIEF, a TARGET, a SUBAGENT'S
FINDING, A CITATION, A GUARD YOU JUST WROTE, AN ESTIMATOR YOU JUST BUILT,
A QUESTION YOU ARE ABOUT TO ASK ME, A THRESHOLD, A SAMPLING WINDOW, A NULL
PATCH, A REFUTATION SOMEONE ELSE ALREADY BANKED, THE AXIS YOUR DETECTOR
SEARCHES ALONG, A LINE IN THE WORK LIST, A FALSIFICATION ARM YOU JUST RAN,
and — NEW, rev 33 — THE ARITHMETIC PRINTED UNDER A FIGURE, and A
PRE-COMMITMENT YOU JUST MADE.**
**DO NOT ASK ME WHAT MEASUREMENT CAN ANSWER.** **AND MY ANSWER MAY NOT BE ONE
OF YOUR OPTIONS.** **NEW AND SHARPER, rev 33: IF I PICK THE FIRST OR LAST
OPTION, YOUR SET PROBABLY DID NOT REACH FAR ENOUGH.** An endpoint answer
leaves the interval OPEN on that side and is the weakest evidence a set can
give that it was wide enough. **Ask a bounded follow-up on that side before you
consume the answer** — rev 33 did, and I closed it.
## Step 6 — the work
§6 below is the ordered list. **THE OLDEST UNDONE ITEM IS STILL THE OVER-RIDER
POST.** rev 33 removed the blocker it inherited and found a NEW one underneath
it. **What blocks it now is ONE COLUMN — the FAR STRUT at u 228** — and unlike
the far end, **it has never been measured, never been graded, and never been
asked about.**
## Step 7 — resolution
rev 25 shipped 4800×3200 in 20 strips, worst seam z 1.91. Drive
`hero.py --only N` one strip per call then `--stitch-only`; run `post.py`
**once** on the stitched frame, never per strip. Middle strips ~5–7 min each,
edge strips ~1.5 min. **`hero.py` STRIPS IN ROW SPACE — SEAMS ARE HORIZONTAL.**
A 900×600 `T1_PREVIEW=hero34f T1_SAMP=24` frame takes **90 s**.
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
Everything in the rev-33 prompt's equivalent section still stands, **with these
changes.**
**§10.82's NAMED GAP IS CLOSED.** *[stated, rev 33]* the bumper top, the rim
face and the hub cap are **ALL CLEAN**. The global `f = 0` gains three surfaces
of support and **THE FILM DOES NOT BECOME LOCAL.** **Do not tune the lever;
§10.82 retired a DERIVATION, not a constant.** Ceiling: two of the three
pointers are on `ref_side.jpg` and **there is no answered anchor on that frame
at all.**
**THE BAR'S FAR END IS SETTLED AT u = 205.** *[stated, rev 33]* candidate line
1, and *[stated, rev 33]* **AT line 1, not left of it.** `f` there is **0.5897**
of the bar's half-width. **This is NOT a build value** — see the next item.
**THE POST IS STILL UNBUILDABLE, AND THE BLOCKER HAS MOVED.** The cross-ratio
consumes FOUR columns. C3 measured two (post 365.5, hoop 485.0), P1b graded one
(the far end), and **the FAR STRUT at u = 228 has never been measured, graded
or asked about** — it is hard-coded in C5 and its own print calls it `(blob)`,
and u 228 is rev 32's candidate line 4, INSIDE the same superposition.
**± 4 px on the strut swings `f` by 11.1 %; the far end's own level is 6.2 % for
the same move. THE UNGRADED COLUMN IS THE MORE SENSITIVE OF THE TWO.**
**THE CROSS-RATIO'S ALGEBRA IS NOT THE PROBLEM** — exact to 3.55e-15 on planted
values. **Do not rebuild it.**
**§10.83's "post at the vehicle's centreline" is STILL UNDECIDED**, fourth
revision running. **The post stays UNBUILT. Do not treat either position as
settled.**
**REF §9's V-SWAGE ABSOLUTE HEIGHT IS A BRACKET, NOT A READING** — ≈0.40–0.49 m,
and the published figure is the TOP of that bracket. Closing it needs the
blade's top boundary at `u = 288.8`, and blade and V-swage are BOTH CREAM.
**REF §9's OTHER THREE ABSOLUTE HEIGHTS DO NOT INHERIT §10.85.** They inherit
the 422 px/m near-side scale and its >2:1 warning. **`422 px/m` is CONSUMED
NOWHERE in the tree.** Sweep done.
**THE TRANSVERSE VP BY HARMONIC CONJUGATE IS NOT REFUTED, IT IS UNPUBLISHED.**
The construction is legitimate — the transverse VP is shared by every lateral
line regardless of height, so it transfers into the bumper plane WITHOUT the
vehicle's yaw. Withheld: the far headlamp runs into the nose's own silhouette
(±5 px moves `f` by 9 %), four row-wise estimates scatter over **154 px**, and
the symmetry assumption's only check disagrees at 17 %.
**A square-on frame of the front still collapses this entirely.**
**THE FRONT OVER-RIDER BAR IS BUILT (§10.83)**, WORKSHOP-STAGE. **`BAR_DIA` and
`BAR_RISE` are written as `ratio × APERTURE_M` and must stay that way.** The
10.83 verify row's reference is **FROZEN IN `verify.py`**, window `x > 2.100`.
**§10.75's POINTER IS VINDICATED** — re-measured `u 355–377`, centre 365.5,
stable to 0.5 px. The number survives; the process defect stands.
**THE VEHICLE HAS NO RECOVERABLE FORE-AFT VANISHING POINT.** Do not fit one.
**THE HERO IS SHOT AND PROVED BY CONTENT.**
## Hard-won rules — every one was learned by breaking it
Every rule in the rev-33 prompt still stands. **NEW in rev 33:**
* **A PROBE OUTLIVES THE WORLD IT WAS WRITTEN IN.** When a lever is retired,
  every probe that DIFFERENCES that lever silently becomes a comparison of a
  value against itself — and it keeps printing, keeps formatting, and keeps
  narrating. **A DEGENERATE COMPARISON IS MORE DANGEROUS THAN A FAILING
  CONTROL, BECAUSE NOTHING ABOUT IT IS RED.**
* **A PRE-COMMITMENT IS A PROBE TOO.** rev 33's named a residual without
  naming which reading of it applied — and the two readings disagree ACROSS
  the decision boundary — **and it was aimed at the wrong term entirely.**
  State which quantity it binds, and check that it is the one the estimator is
  most sensitive to.
* **GRADE EVERY COLUMN AN ESTIMATOR CONSUMES, NOT THE ONE YOU ARE ARGUING
  ABOUT.** P1b graded one of four. Two revisions and three questions went into
  the wrong term.
* **AN ENDPOINT ANSWER IS AN OPEN INTERVAL.** If the owner picks the first or
  last option, the set did not reach far enough. Ask a bounded follow-up.
* **A NUMBER WRITTEN INTO A QUESTION IS A NUMBER NOBODY RE-READS.** Make the
  figure recompute it at draw time, and make it REFUSE TO DRAW if its own
  positive control fails.
* **A DOCUMENTED ESCAPE HATCH IS NOT A FALSIFICATION.** rev 33's arm 4 used
  `T1_W_DUP`, whose own comment says it skips the assert. Read what you are
  bypassing before you call it an arm.
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
```
**If a pull says "Need to specify how to reconcile divergent branches", STOP.**
The hero is gitignored and lives only on my disk.
```bash
git status                                                   # clean
grep -c '^### 10.87' SPEC.md                                 # 1   rev 33
grep -c '^#### 10.87' SPEC.md                                # 6   rev 33
grep -c '10.87' SPEC.md                                      # 7   rev 33
grep -c 'A PROBE OUTLIVES THE WORLD IT WAS WRITTEN IN' SPEC.md    # 1   rev 33
grep -c 'A PRE-COMMITMENT IS A PROBE TOO' SPEC.md            # 1   rev 33
grep -c 'A NUMBER WRITTEN INTO A QUESTION' SPEC.md           # 1   rev 33
grep -c 'STRUT_U' probe_rev33_barend.py                      # 11  rev 33
grep -c 'KILL' probe_rev33_barend.py                         # 11  rev 33
grep -c 'Q1B_LEFT_BOUNDED' probe_rev33_barend.py             # 1   rev 33
grep -c 'blob' probe_rev33_barend.py                         # 4   rev 33
grep -c 'REFUSING TO WRITE' mark_rev33_q1.py                 # 1   rev 33
grep -c 'PLANTED' mark_rev33_q1.py                           # 3   rev 33
grep -c 'CANDIDATE LINES' mark_rev33_q1b.py                  # 4   rev 33
ls HANDOFF_rev33.md STATE_rev33.md probe_rev33_barend.py
ls mark_rev33_q1.py mark_rev33_q1b.py rev33_q1_barend.png rev33_q1b_leftbound.png
grep -c 'UNDECIDED' SPEC.md                                  # 9   MOVED BY 10.87
grep -c '### 10.86' SPEC.md                                  # 1   ANCESTOR rev 32
grep -c '288.8' SPEC.md                                      # 8   ANCESTOR rev 32
grep -c '288.8' REF_MEASUREMENTS.md                          # 4   ANCESTOR rev 32
grep -c 'UNDECIDED' verify.py                                # 3   ANCESTOR rev 32
grep -c 'V_APEX_TOL' probe_orb_post.py                       # 12  ANCESTOR rev 32
grep -c '76.7' verify.py                                     # 2   ANCESTOR rev 32
grep -c 'publishes 186' probe_dust_scope.py                  # 1   ANCESTOR rev 32
grep -c 'NO REAL ROOT' probe_orb_xratio.py                   # 3   ANCESTOR rev 32
grep -c 'broke_at' probe_orb_xratio.py                       # 8   ANCESTOR rev 32
grep -c 'ANSWERED' probe_rev32_pointer.py                    # 12  ANCESTOR rev 32
grep -c 'CANDIDATE LINES' mark_rev32_q.py                    # 3   ANCESTOR rev 32
grep -c 'ORB_RISE_SPEC' verify.py                            # 6   ANCESTOR rev 30
grep -c 'BAR_RATIO' t1_detail.py                             # 3   ANCESTOR rev 30
grep -c 'overrider_bar' build.py                             # 1   ANCESTOR rev 30
grep -c 'W_h' probe_orb_hoop.py                              # 6   ANCESTOR rev 30
grep -c 'CORE' probe_psf_owner.py                            # 12  ANCESTOR rev 28
grep -c 'SPEC 10.76' t1_mats.py                              # 4   ANCESTOR rev 27
grep -c 'PUBLISHED_CLEAN' probe_ctan_pedestal.py             # 3   ANCESTOR rev 26
grep -c '_ceval' folk_gen.py                                 # 19  ANCESTOR rev 25
grep -c '_retired_value_drift' verify.py                     # 3   ANCESTOR rev 24
grep -c 'OFF_CROSS_BASELINE' t1_shell.py                     # 1   ANCESTOR rev 23
grep -c 'H_ROOF_REGRESSION' verify.py                        # 7   ANCESTOR rev 22
grep -c 'T1_CTAN_NOBOUNCE' shader_solve.py                   # 4   ANCESTOR rev 20
grep -c '_BODY' cream_rms.py                                 # 4   ANCESTOR rev 19
grep -c '_arch_lip_z' verify.py                              # 2   ANCESTOR rev 18
grep -c 'matte_tap' studio.py                                # 6   ANCESTOR rev 17
grep -c '_coons_cap' t1_core.py                              # 3   ANCESTOR rev 16
grep -c 'The threshold is not the parameter' post.py         # 1   ANCESTOR rev 13
```
**EVERY VALUE ABOVE WAS FILLED FROM A FRESH-CLONE VERIFICATION RUN.** Never
type one from memory — `grep -c` counts LINES, not occurrences, and that has
produced a wrong figure in eleven revisions.
**AND `grep -c '### 10.87'` IS NOT 1 — IT IS 7.** `#### 10.87.1` CONTAINS
`### 10.87` as a substring, so the h3 and all six h4s match. That is why the
first two rows above are anchored with `^`. **rev 33 hit this within a minute
of writing the section.** A heading count without an anchor is not a heading
count.
**NOTE THE ROW MARKED "MOVED BY 10.87".** rev 32 published `UNDECIDED` in SPEC
as 8; §10.87 added one and it is now 9. *A grep count is invalidated by any
later edit to the file it counts — including a later revision's.*
Ancestry — **rev 33 adds `cac32b9`, the rev-32 TIP:**
```bash
for c in f3c53f4 87aeaa6 d519fc6 5087b84 7ce3d03 f3cde44 efc1268 456b201 b08e424 e792d73 6f87977 cac32b9; do
  git merge-base --is-ancestor $c HEAD && echo "$c ok" || echo "$c LOST"; done
```
Texture md5s — **all three must match, and rev 33 changed NO artwork:**
```bash
md5sum tex/swirl.png tex/swirl_b.png tex/nose.png
# 4ee4e09e...   d201597e...   b31ea156...
```
## 2. Both guards, and the figures I watched print
| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 0 warn** | **0 fail, 0 warn** |
| audit.py | **0 fail, 0 warn** | **0 fail, 0 warn** |
| roof crown @ rear axle | **1.9835** (baseline 1.9835, −0.0 mm) | **1.9833** (−0.2 mm) |
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
band 1.372–1.775. **EVERY GEOMETRY FIGURE IS IDENTICAL TO REV 30's, 31's AND
32's.**
Probe controls on the fresh clone: `probe_rev33_barend.py` **7 checked, 4
FAILED — AND ALL FOUR FAILURES ARE THE RESULT**; `probe_orb_xratio.py` **6
checked, 1 FAILED** (C5, a KILL control); `probe_rev32_pointer.py` **10
checked, 0 FAILED**; `probe_dust_scope.py` **8 checked, 0 FAILED**;
`probe_clean_top.py` **controls FAIL** and `probe_dust_anchor.py` **FAIL** —
**both DELIBERATELY LEFT FAILING** (§10.87.2). **Do not "fix" any of these.**
## 3. What rev 33 changed — `HANDOFF_rev33.md` has the full account
- **`SPEC.md`** — NEW §10.87, six parts.
- **`STATE.md`** — regenerated on the clean rev-33 tree, AFTER §10.87.3
  recorded that it had been stale. **`STATE_rev33.md`** written alongside.
- **`probe_rev33_barend.py`**, **`mark_rev33_q1.py`**, **`mark_rev33_q1b.py`**,
  **`rev33_q1_barend.png`**, **`rev33_q1b_leftbound.png`**,
  **`HANDOFF_rev33.md`** — all NEW, all READ-ONLY.
- **NO GEOMETRY. NO SHADER. NO ARTWORK.** `CREAM`, `COUNTERTAN`,
  `COUNTERCREAM`, `RED`, the rake, the roof, the over-rider bar and all three
  textures UNCHANGED. **`verify.py`, `t1_detail.py`, `t1_mats.py`, `build.py`
  and every other build file are BYTE-UNCHANGED from rev 32.**
**Things you must not silently undo — `HANDOFF_rev33.md` §6**, and rev 32's §8
through rev 18's §4 all still stand in full.
## 4. Still open
- **THE OVER-RIDER POST.** Blocked on **THE FAR STRUT at u = 228** — never
  measured, never graded, never asked about, and **more sensitive than the
  column three questions were spent on.** This is item 1.
- **§10.83's centreline claim is UNDECIDED**, fourth revision running.
- **REF §9's V-SWAGE ABSOLUTE HEIGHT is a bracket, ≈0.40–0.49 m.**
- **§10.70's percentages must be RE-RUN** before being quoted again — and
  §10.87.2 now names the mechanism: they are of the degenerate-comparison
  family. The harness has **no cyclorama** (§10.78) — state that, do not
  silently fix it.
- **`probe_clean_top.py` and `probe_dust_anchor.py` need REWRITING, not
  fixing.** What they compare no longer exists.
- **THE FRONT BUMPER FACE IS UNMEASURED.** **`CREAM`.** **THE ABSOLUTE ROOF
  HEIGHT.** **THE OFF FLANK, 804.9 mm.** `COUNTERTAN` 34.0 % short in B.
- `GAL_SKY` dead lever. `PLATE_W = 0.3300` no provenance.
  `probe_rev16.py:90` prints `xa` vs `xa`.
## 5. FIRST QUESTION FOR THE OWNER — ONE, AND IT IS ITEM 1
**Where does the over-rider bar's FAR STRUT sit?** It is the vertical member
inboard of the bar's far end, and C5 has been assuming `u = 228` with no
support. **Build the figure the way rev 33 built Q1b:** crop `ref_workshop.jpg`
around the strut, CANDIDATE LINES declared as such, the crop box printed, `f`
recomputed under each line at draw time, and **the figure refusing to draw if
its own positive control fails.** **And bracket the answer on BOTH sides this
time** — offer lines above and below 228 so an endpoint answer is not the only
thing the set can return.
What would still move the most is one photograph: **a head-on rear (or front)
elevation from roof height or above, with the counter and the lids clear of the
section** — the only realistic route to closing `CREAM`, the absolute roof
height and the B residual. A clear view of the **off flank** closes 804.9 mm.
**And for the POST: any frame showing the FRONT of the vehicle square-on
collapses the lateral-scale problem entirely and makes the strut question
moot.**
## 6. Ordered work list for rev 34
1. **THE FAR STRUT.** Ask, then feed it into `probe_rev33_barend.py`'s A7.
   **Say before you start whether it will close** — at ±4 px it will not
   (11.1 % on `f`, against a 6.2 % closing level), so **a candidate-line answer
   alone is not enough; you need a bound on BOTH sides.** If it closes, express
   the post as a **FRACTION of the bar's half-width** so it inherits
   `BAR_HALF_Y`'s grade E rather than adding a new lateral choice.
2. **REWRITE `probe_clean_top.py` and `probe_dust_anchor.py`**, or retire them
   with a stated reason. **Do not widen a tolerance.** Decide first what the
   post-retirement question is.
3. **Re-run §10.70's arms** on the post-retirement build before quoting any of
   its percentages, then the scene→top bounce.
4. Tail-lamp material slot; `Senor`'s letterforms; `SCR`'s +80 mm.
5. Camera absolutely last.
## 7. THE COMMIT COUNT AND THE CONTENT FIGURES
This section is written LAST, after the final commit, and every figure in §1
was read off a fresh-clone verification run rather than typed from memory.
**This has gone wrong in ELEVEN revisions during handoff assembly.**
**FINAL COUNT: 173 commits, clean tree.** *(Verified: this line lands in commit
173 itself, which is what makes it true — the count lands in its own commit,
rev 29's pattern, kept since.)*
**THE GREP TRAP FIRED AGAIN, IN A NEW WAY.** rev 31b found its own later
section moving its own earlier counts. rev 32 found seven of rev 31's counts
invalidated by rev 32's edits. **rev 33 found a SUBSTRING collision inside a
single grep:** `grep -c '### 10.87'` returns **7**, not 1, because
`#### 10.87.1` contains the pattern. Anchored with `^` it is 1. **The pattern
was wrong, not the file.**
**AND FOUR OF SIX FALSIFICATION ARMS DID NOTHING ON THE FIRST TRY.** One used
a literal the guard does not watch; one had its `+ 0.003` swallowed into a
comment; one injected into a comment line and then used a **documented escape
hatch** that the assert's own text says it skips; one broke a dict literal so
the script "refused to write" **because it crashed**. **Every one printed
something that looked like success.** All four caught by printing the changed
line before believing the arm — §10.86's rule, and it paid four times in one
revision.
