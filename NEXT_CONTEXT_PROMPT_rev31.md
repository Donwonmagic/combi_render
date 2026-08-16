# NEXT CONTEXT PROMPT — rev 31

Please act as my expert. Continue the Señor Tacombi combi build. **Thirty
revisions sit behind this.** You are picking up mid-stream, not starting.

## Step 0 — CHECK A FOLDER IS CONNECTED BEFORE YOU PLAN ANYTHING
Call `get_device_info`; if `connectedFolders` is empty, request
`~/Desktop/tacombi_bus_render` immediately and say so plainly. It timed out
unanswered in rev 28 and rev 29; **it was granted on the FIRST request in rev
30.** Do not assume either way — send it and say you have.

**NEW, rev 30 — THE BRIDGE HAS A THROUGHPUT CEILING, NOT JUST A SIZE ONE.**
`device_stage_files` returned `wall-clock timeout` on **every file above
~3 MB**, including the 19.5 MB base bundle **alone, twice**. Small files
crossed fine throughout, so it is not a drop. **The fix that worked:** split
the big bundles into 3 MB parts on his machine with `device_bash`, stage them
**1–2 per call**, and `cat` them back. **md5 matched on both sides** — a
stronger round trip than rev 29 achieved. Budget ~10 extra calls for this.

## Step 1 — read my memory BEFORE you read any code
`/areas/tacombi-combi-3d.md`, then `-rev14`, `-rev17` … `-rev29`, then
**`/areas/tacombi-combi-3d-rev30.md`** (SEPARATE FILES; each revision's file
does NOT carry the next), then `/areas/tacombi-combi-sticker.md`, then
`/preferences.md`. If you cannot read them, say so explicitly.

**I have never stood in the bus.** The "remember standing in the kombi" bar is
about the RESTAURANT'S owner. **Do not ask me what the real vehicle looks
like.** Ask me what a PHOTOGRAPH shows — that has now paid off nineteen times.

## Step 2 — restore, and verify BY CONTENT (never by hash or commit count)
See §1. **EIGHTEEN bundle lines now, and the rev14b line is a `fetch` that must
come BEFORE rev15.** rev 20 through rev 30 all restored CLEAN — do not assume
either way, check.

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

**THE GUARDS ARE 0 fail / 0 WARN.** **GEOMETRY MOVED IN REV 30 — the first
time since rev 23** — and the SHADING moved in rev 29, so
`rev25_hero34f.png` is **STALE TWICE OVER**. Read §10.83.

## Step 4 — read, in this order
`STATE.md` → `SPEC.md` §10, then §10.9 through §10.83 → this file →
**`HANDOFF_rev30.md`** → `HANDOFF_rev29.md` → … → `AUDIT_rev18_loft.md` →
`LOFT_GROUND_rev15.md` → `AUDIT_rev12.md` → `REF_MEASUREMENTS.md`.
`STATE.md` is machine-written; **if it and any prose disagree, it is right.**

**§10.83 IS REV 30's, AND IT IS THE FIRST ENTRY IN SEVEN REVISIONS TO MOVE
GEOMETRY.** It also **CORRECTS §10.75** — that section's "post at the vehicle's
centreline" is REFUTED and marked in place.

## Step 5 — ASK ME WHAT THE PHOTOGRAPHS SHOW before you measure from them
This has now paid off nineteen times. Show me a crop, mark the regions, give me
options, **print the crop box**, and **say plainly whether a box is a POINTER
or a SAMPLING WINDOW** — rev 30's two boxes were the first SAMPLING WINDOWS and
it said so on the figure. Show the photograph **BESIDE a render of the current
build**.

**A CLASS GATE IS A PROBE TOO, and so is a BRIEF, a TARGET, a SUBAGENT'S
FINDING, A CITATION, A GUARD YOU JUST WROTE, AN ESTIMATOR YOU JUST BUILT,
A QUESTION YOU ARE ABOUT TO ASK ME, A THRESHOLD, and — NEW, rev 30 — A
SAMPLING WINDOW and A NULL PATCH.**
rev 30 killed TWO of its own estimators, TWO of its own null patches, its own
first guard (a tautology) and its own first sampling window.

**AND, NEW: DO NOT ASK ME WHAT MEASUREMENT CAN ANSWER.** rev 30's brief made
the blade-column question task one. A line fit answered it, so it was not
asked, and the two questions I did get were the ones only I could answer.

## Step 6 — the work
§6 below is the ordered list. **THE OLDEST UNDONE ITEM IS NOW THE OVER-RIDER
POST, and it is blocked on a LATERAL position REF §9 bars on this panel.**

## Step 7 — resolution
rev 25 shipped 4800×3200 in 20 strips, worst seam z 1.91. Drive
`hero.py --only N` one strip per call then `--stitch-only`; run `post.py`
**once** on the stitched frame, never per strip. Middle strips ~5–7 min each,
edge strips ~1.5 min.

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
Everything in the rev-30 prompt's equivalent section still stands, plus:

**THE FRONT OVER-RIDER BAR IS BUILT (§10.83)**, WORKSHOP-STAGE, on a ratio to
the headlamp aperture measured at the tube's own station. **`BAR_DIA` and
`BAR_RISE` are written as `ratio × APERTURE_M` and must stay that way** — the
anchor is a **CATALOGUE** 0.180 m, SPEC 10.72's struck class.
**The 10.83 verify row's reference is FROZEN IN `verify.py`, not read from
`t1_detail` — the first version was a TAUTOLOGY and read 0 fail on a 3 mm
source change.** Its window is `x > 2.100`, not `x > 2.132`.
**§10.75's "post at the vehicle's centreline" is REFUTED** — the V apex is at
`u = 311.5`, the post's columns are 357–374. **Do not build the post at the
centreline.**
**rev 29's scale-free tube/blade ratio is REFUTED as a fix** (±12.8 %, between
its own two terms). **The trolley does NOT occlude the blade in the tube's
columns** (rail line rms 0.289 px).
**TWO NEW `_RETIRED_VALUES` ROWS**, `14.98` and `post at the vehicle's
centreline`, both watched FIRE.

## Hard-won rules — every one was learned by breaking it
Every rule in the rev-30 prompt still stands. **NEW in rev 30:**
* **A GUARD WHOSE REFERENCE IS THE THING IT GUARDS CAN ONLY CATCH DELETION.**
  Third tautology-inside-a-guard. **Freeze the reference.**
* **A FLATNESS FIGURE YOU DO NOT GATE ON IS NOT A CONTROL.**
* **MEASURE SOMEWHERE ELSE BEFORE YOU BUILD A THIRD ESTIMATOR.** Two died; the
  answer was a BOUND that needed neither.
* **A "CAN'T TELL" IS A RESULT AND IT BINDS.**
* **ASK ONLY WHAT MEASUREMENT CANNOT ANSWER.**

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
```
**If a pull says "Need to specify how to reconcile divergent branches", STOP.**
Content checks — **the first eleven reach the TIP on purpose.** The hero is
gitignored and lives only on my disk.
```bash
git status                                              # clean
grep -c '### 10.83' SPEC.md                             # 1   rev 30
grep -c 'REFUTED, rev 30' SPEC.md                       # 1   rev 30
grep -c 'SPEC 10.83' t1_detail.py                       # 1   rev 30
grep -c '10.83' verify.py                               # 10  rev 30
grep -c 'ORB_RISE_SPEC' verify.py                       # 6   rev 30
grep -c 'BAR_RATIO' t1_detail.py                        # 3   rev 30
grep -c 'overrider_bar' build.py                        # 1   rev 30
grep -c 'STEP_1090' probe_orb_blade.py                  # 4   rev 30
grep -c 'W_h' probe_orb_hoop.py                         # 6   rev 30
grep -c 'SAMPLING WINDOW' mark_rev30_q.py               # 8   rev 30
ls HANDOFF_rev30.md probe_orb_blade.py probe_orb_hoop.py mark_rev30_q.py
grep -c '### 10.82' SPEC.md                             # 1   ANCESTOR rev 29
grep -c 'W_DUST_FAC_UP' probe_dust_scope.py             # 14  ANCESTOR rev 29
grep -c 'ANSWERED' probe_updust_pointer.py              # 7   ANCESTOR rev 29
grep -c '### 10.80' SPEC.md                             # 1   ANCESTOR rev 28
grep -c 'CORE' probe_psf_owner.py                       # 12  ANCESTOR rev 28
grep -c 'SPEC 10.76' t1_mats.py                         # 4   ANCESTOR rev 27
grep -c 'PUBLISHED_CLEAN' probe_ctan_pedestal.py        # 3   ANCESTOR rev 26
grep -c '_ceval' folk_gen.py                            # 19  ANCESTOR rev 25
grep -c '_retired_value_drift' verify.py                # 3   ANCESTOR rev 24
grep -c 'OFF_CROSS_BASELINE' t1_shell.py                # 1   ANCESTOR rev 23
grep -c 'H_ROOF_REGRESSION' verify.py                   # 7   ANCESTOR rev 22
grep -c 'T1_CTAN_NOBOUNCE' shader_solve.py              # 4   ANCESTOR rev 20
grep -c '_BODY' cream_rms.py                            # 4   ANCESTOR rev 19
grep -c '_arch_lip_z' verify.py                         # 2   ANCESTOR rev 18
grep -c 'matte_tap' studio.py                           # 6   ANCESTOR rev 17
grep -c '_coons_cap' t1_core.py                         # 3   ANCESTOR rev 16
grep -c 'The threshold is not the parameter' post.py    # 1   ANCESTOR rev 13
```
**EVERY VALUE ABOVE WAS FILLED FROM A FRESH-CLONE VERIFICATION RUN.** Never
type one from memory — `grep -c` counts LINES, not occurrences, and that has
produced a wrong figure in eleven revisions.
Ancestry — **rev 30 adds `b08e424`, a rev-29 commit (NOT its tip — see §7),
so the loop's newest entry is no longer a rev-19 commit:**
```bash
for c in f3c53f4 87aeaa6 d519fc6 5087b84 7ce3d03 f3cde44 efc1268 456b201 b08e424; do
  git merge-base --is-ancestor $c HEAD && echo "$c ok" || echo "$c LOST"; done
```
Texture md5s — **all three must match:**
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
| objects at `materials:` | **127** *(126 + the over-rider)* | **127** |
| shut line × aperture, SHOW / OFF | **0.0 mm / 804.9 mm** | same |
| `CARGO_GAP` samples | **154** | same |
| bay widths | **0.516 0.515 0.516** | same |
| over-rider row | **97.51 mm above the blade top, dia 24.97 mm** | same |

Also: **186 meshes**; 42 materials; 5 constant-rough; **0 non-manifold**;
band 1.372–1.775.
**EVERY GEOMETRY FIGURE EXCEPT THE COUNTS IS IDENTICAL TO REV 23's.**

## 3. What rev 30 changed — `HANDOFF_rev30.md` has the full account
- **`t1_detail.py`** — NEW `overrider_bar()` and its constants (§10.83).
- **`build.py`** — one line, workshop-stage.
- **`verify.py`** — NEW 10.83 row with a FROZEN reference; two
  `_RETIRED_VALUES` rows, both watched FIRE.
- **`SPEC.md`** — §10.83; §10.75 corrected in place.
- **`probe_orb_blade.py`**, **`probe_orb_hoop.py`**, **`mark_rev30_q.py`** —
  all NEW, all READ-ONLY.
- **NO ARTWORK.** `CREAM`, `COUNTERTAN`, `COUNTERCREAM`, `RED`, the rake, the
  roof and all three textures UNCHANGED.

**Things you must not silently undo — `HANDOFF_rev30.md` §3**, and rev 29's §4
through rev 18's §4 all still stand in full.

## 4. Still open
- **THE OVER-RIDER POST (§10.75, §10.83).** Now the oldest undone item. Its
  columns are 357–374 against the V apex at 311.5, so it is NOT on the
  centreline. **Blocked on a LATERAL position, which REF §9 bars on this panel**
  (scale varies >2:1, a fitted projection model did not close). The only route I
  can see is a projection solve for `ref_workshop.jpg` using the WORKSHOP's own
  architecture — the masonry courses, the roof beams, the columns — with the
  bumper top at 0.348 m as the known height. **Single-view metrology. Untried.**
  Say so before you spend a revision on it.
- **A HERO IS OWED TWICE OVER** — shading moved in rev 29, geometry in rev 30.
- **§10.70's percentages must be RE-RUN** before being quoted again.
- **§10.82's unasked surfaces** — bumper top, rim barrels, hub caps.
- **THE FRONT BUMPER FACE IS UNMEASURED.** **`CREAM`.** **THE ABSOLUTE ROOF
  HEIGHT.** **THE OFF FLANK, 804.9 mm.** `COUNTERTAN` 34.0 % short in B.
- `GAL_SKY` dead lever. `PLATE_W = 0.3300` no provenance.
  `probe_rev16.py:90` prints `xa` vs `xa`.

## 5. FIRST QUESTIONS FOR THE OWNER — NONE OUTSTANDING
Both of rev 30's questions were answered and both changed the work. What would
still move the most is one photograph: **a head-on rear (or front) elevation
from roof height or above, with the counter and the lids clear of the
section** — the only realistic route to closing `CREAM`, the absolute roof
height and the B residual. A clear view of the **off flank** closes 804.9 mm.
**And for the over-rider POST: any frame showing the FRONT of the vehicle
square-on, which would collapse the lateral-scale problem entirely.**

## 6. Ordered work list for rev 31
1. **A HERO — it is OWED TWICE OVER.** Shading moved in rev 29, geometry in
   rev 30. Shoot it first this time; do not let it slip a third revision.
2. **THE OVER-RIDER POST.** Single-view metrology off the workshop
   architecture, or a proof it will not close. **Say which before you start.**
3. **Re-run §10.70's arms** on the post-retirement build before quoting any of
   its percentages, then the scene→top bounce. The harness has **no cyclorama**
   (§10.78) — state that, do not silently fix it.
4. **§10.82's unasked surfaces** — the bumper top, the rim barrels, the hub
   caps. If any frame shows them, ask.
5. Tail-lamp material slot; `Senor`'s letterforms; `SCR`'s +80 mm.
6. Camera absolutely last.

## 7. THE COMMIT COUNT AND THE CONTENT FIGURES
This section is written LAST, after the final commit, and every figure in §1 was
read off a fresh-clone verification run rather than typed from memory. **This has
gone wrong in ELEVEN revisions during handoff assembly.** rev 23 through rev 30
were clean runs.

**FINAL COUNT: 148 commits, clean tree.** *(Written into the commit that makes it true — the count lands in its own commit, rev 29's pattern. It was 144 and then 146 in two earlier drafts of this file and BOTH were stale the moment they were committed; that is the twelfth instance of this trap and the reason this line is the last edit of the revision.)*

**A COUNT TRAP CAUGHT AND NAMED, rev 30.** `STATE_rev29.md` records commit
`b08e424`, and I took that for the rev-29 TIP. It is not: rev 29 committed three
more times after `audit.py` wrote that file, so `b08e424` counts **132** and the
real rev-29 tip is **`82504fd`** at **135**. The rev-30 bundle spans
`b08e424..HEAD`, which is harmless — the extra three commits are already in your
history and the pull still fast-forwards — but the ARITHMETIC was wrong until it
was checked against a clone.
**A PROVENANCE HASH IN A MACHINE-WRITTEN FILE IS THE COMMIT THAT WROTE IT, NOT
THE TIP OF ITS REVISION.**
