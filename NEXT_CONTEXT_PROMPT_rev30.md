# NEXT CONTEXT PROMPT — rev 30
Please act as my expert. Continue the Señor Tacombi combi build. **Twenty-nine
revisions sit behind this.** You are picking up mid-stream, not starting.
## Step 0 — CHECK A FOLDER IS CONNECTED BEFORE YOU PLAN ANYTHING
Call `get_device_info`; if `connectedFolders` is empty, request
`~/Desktop/tacombi_bus_render` immediately and say so plainly. **The dialog can
time out** — it timed out unanswered in BOTH rev 28 and rev 29. Re-send it.
Without a folder the eighteen bundle files and all three reference photographs
are unreachable and every item in §6 is blocked.
## Step 1 — read my memory BEFORE you read any code
`/areas/tacombi-combi-3d.md`, then `-rev14`, `-rev17` … `-rev28`, then
**`/areas/tacombi-combi-3d-rev29.md`** (SEPARATE FILES; each revision's file
does NOT carry the next), then `/areas/tacombi-combi-sticker.md`, then
`/preferences.md`. If you cannot read them, say so explicitly.
**I have never stood in the bus.** The "remember standing in the kombi" bar is
about the RESTAURANT'S owner. **Do not ask me what the real vehicle looks
like.** Ask me what a PHOTOGRAPH shows — that has now paid off eighteen times.
## Step 2 — restore, and verify BY CONTENT (never by hash or commit count)
See §1. **SEVENTEEN bundle lines now, and the rev14b line is a `fetch`.**
rev 20 through rev 29 all restored CLEAN — do not assume either way, check.
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
**THE GUARDS ARE 0 fail / 0 WARN.** **NO GEOMETRY HAS MOVED SINCE REV 23, AND
NO ARTWORK SINCE REV 25 — BUT THE SHADING MOVED IN REV 29**, so
`rev25_hero34f.png` is STALE and a hero is OWED. Read §10.82.
## Step 4 — read, in this order
`STATE.md` → `SPEC.md` §10, then §10.9 through §10.82 → this file →
**`HANDOFF_rev29.md`** → `HANDOFF_rev28.md` → `HANDOFF_rev27.md` → …
→ `AUDIT_rev18_loft.md` → `LOFT_GROUND_rev15.md` → `AUDIT_rev12.md` →
`REF_MEASUREMENTS.md`. `STATE.md` is machine-written; **if it and any prose
disagree, it is right.**
**§10.82 IS REV 29's, AND IT RETIRES A CONSTANT FOR THE FIRST TIME IN SIX
REVISIONS.** It also refutes the framing of §10.81 and of `t1_mats.py:366`.
## Step 5 — ASK ME WHAT THE PHOTOGRAPHS SHOW before you measure from them
This has now paid off eighteen times. Show me a crop, mark the regions, give me
options, **print the crop box**, and **say plainly whether a box is a POINTER
or a SAMPLING WINDOW**. Show the photograph **BESIDE a render of the current
build** — that is what made rev 26's and rev 29's questions decisive.
**A CLASS GATE IS A PROBE TOO, and so is a BRIEF, a TARGET, a SUBAGENT'S
FINDING, A CITATION, A GUARD YOU JUST WROTE, AN ESTIMATOR YOU JUST BUILT,
A QUESTION YOU ARE ABOUT TO ASK ME, and — NEW, rev 29 — A THRESHOLD.**
rev 29 refuted THREE of its own thresholds, TWO of its own probe's estimators,
and its OWN first falsification arm.
## Step 6 — the work
§6 below is the ordered list. **THE OLDEST UNDONE ITEM IS STILL THE FRONT
OVER-RIDER, and it is blocked on A SCALE, not on a reading.**
## Step 7 — resolution
rev 25 shipped 4800×3200 in 20 strips, worst seam z 1.91. Drive
`hero.py --only N` one strip per call then `--stitch-only`; run `post.py`
**once** on the stitched frame, never per strip. Middle strips ~5–7 min each,
edge strips ~1.5 min. **`rev25_hero34f.png` NO LONGER PHOTOGRAPHS THE CURRENT
BUILD** — the shading moved in rev 29. **A HERO IS OWED.**
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
Everything in the rev-29 prompt's equivalent section still stands, plus:
**`W_DUST_FAC_UP` IS RETIRED TO 0.0 (§10.82)** on TWO owner readings — the
counter top (rev 28) and the ROOF (rev 29). It was never a counter-top
constant: it is ONE MULTIPLY node in the file's ONE shared `WEATHER` node-tree,
reaching **ELEVEN materials**, and `T1_W_DUP=0` takes **all eleven** to zero.
**86.4 % of the area it filmed was NOT the counter** — the largest surface is
`T1_body` under `T1_paint`, **12.3697 m²** of up-facing area.
**Restoring 0.7313 in source FIRES an assert. Use `T1_W_DUP=0.7313` to render
the retired arm.** **The SPEC 10.76 catcher is RE-BASELINED to
(−0.023400, −0.037000, −0.120500)** — a deliberate re-baseline after a
deliberate change, band UNCHANGED at 2e-3; **do not tighten it and do not
restore the rev-26 figure, which is unreachable by construction.**
**TWO `_RETIRED_VALUES` ROWS**, `0.7313` and `mean coverage 0.548` — the same
retirement in two forms; both watched FIRE.
**THIS DID NOT FIX `COUNTERTAN`** — a clean top is still **34.0 % short in B**.
**§10.70's percentages must be RE-RUN before being quoted again**, because they
were measured on a build that had the film.
**The bumper top, the rim barrels and the hub caps are filmed by the same node
and NOBODY HAS BEEN ASKED about them.** The retirement asserts more than two
readings strictly support. Named, not hidden.
## Hard-won rules — every one was learned by breaking it
Every rule in the rev-29 prompt still stands. **NEW in rev 29:**
* **COMMIT BEFORE FALSIFYING.** A `git checkout <file>` used to undo a
  falsification arm destroyed unrelated uncommitted work **TWICE** — the second
  time twenty minutes after the rule had been written into SPEC itself.
  *Writing a rule down is not the same as having it.*
* **A THRESHOLD IS A PROBE TOO.** Three were wrong before one was right.
* **CALIBRATE AGAINST AN ANSWERED QUESTION.** The strongest control on "can
  this be answered" is a box that WAS answered. rev 29's straddle band has
  **no free parameter** for exactly this reason.
* **A NUMBER COMPUTED ONE WAY IS NOT A NUMBER COMPUTED ANOTHER WAY.**
* **CHECK WHICH SECTION A GUARD CAN SEE** — rev 29's first falsification of its
  own new rows did not fire and **the guard was right.**
* **A PROBE THAT CANNOT DESCRIBE THE SHIPPED BUILD IS NOT A PROBE** — rev 29's
  own probe divided by an assert its own change had made zero.
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
git fetch ../tacombi_rev14b_incremental.bundle HEAD:refs/heads/b14   # FETCH
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
```
**If a pull says "Need to specify how to reconcile divergent branches", STOP.**
Content checks — **the first nine reach the TIP on purpose.** The hero is
gitignored and lives only on my disk.
```bash
git status                                              # clean
grep -c '### 10.82' SPEC.md                             # 1   rev 29
grep -c 'SPEC 10.82' t1_mats.py                         # 8   rev 29
grep -c 'RETIRED, rev 29' t1_mats.py                    # 1   rev 29
grep -c '10.82' verify.py                               # 3   rev 29
grep -c 'W_DUST_FAC_UP' probe_dust_scope.py             # 14  rev 29
grep -c 'Newell' probe_dust_scope.py                    # 4   rev 29
grep -c 'ANSWERED' probe_updust_pointer.py              # 7   rev 29
grep -c 'POINTER' mark_rev29_q.py                       # 4   rev 29
grep -c 'COMMIT BEFORE FALSIFYING' SPEC.md              # 1   rev 29
ls HANDOFF_rev29.md probe_dust_scope.py probe_updust_pointer.py mark_rev29_q.py
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
Ancestry:
```bash
for c in f3c53f4 87aeaa6 d519fc6 5087b84 7ce3d03 f3cde44 efc1268 456b201; do
  git merge-base --is-ancestor $c HEAD && echo "$c ok" || echo "$c LOST"; done
```
**Known limitation, stated rather than hidden:** the ancestry loop's newest
entry is a rev-19 commit, because a hash cannot be written into the file that
contains it without amending, and rev 14 learned not to amend. **The TIP is
covered by the rev-29 content greps instead.**
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
| objects at `materials:` | **126** | **126** |
| shut line × aperture, SHOW / OFF | **0.0 mm / 804.9 mm** | same |
| `CARGO_GAP` samples | **154** | same |
| bay widths | **0.516 0.515 0.516** | same |
Also: **185 meshes**; 42 materials; 5 constant-rough; **0 non-manifold**;
band 1.372–1.775.
**EVERY GEOMETRY FIGURE IS IDENTICAL TO REV 23's.** The SHADING moved.
## 3. What rev 29 changed — `HANDOFF_rev29.md` has the full account
- **`t1_mats.py`** — `W_DUST_FAC_UP` **0.7313 → 0.0** (§10.82); the derivation
  assert RETIRED and replaced with a narrower one that CAN fail; the §10.76
  catcher RE-BASELINED.
- **`verify.py`** — two `_RETIRED_VALUES` rows, both watched FIRE.
- **`SPEC.md`** — §10.82.
- **`probe_dust_scope.py`**, **`probe_updust_pointer.py`**, **`mark_rev29_q.py`**
  — all NEW, all READ-ONLY.
- **NO GEOMETRY. NO ARTWORK.** `CREAM`, `COUNTERTAN`, `COUNTERCREAM`, `RED`,
  the rake, the roof and all three textures UNCHANGED.
**Things you must not silently undo — `HANDOFF_rev29.md` §4**, and rev 28's §4
through rev 18's §4 all still stand in full.
## 4. Still open
- **THE FRONT OVER-RIDER (§10.75, §10.80).** The owner has ruled the tube and
  the post are BOTH ON THE BUS and chose **model them tagged workshop-stage**.
  **NOT ATTEMPTED IN REV 28 OR REV 29.** The PSF blocker is CLEARED
  (σ = 0.5594 ± 0.0280 px). What is left: **a scale on the nose/bumper plane,
  or a proof none is admissible.** **rev 29's one contribution is NEGATIVE and
  worth carrying:** REF §9's **422 px/m** is a LOCAL near-side scale anchored on
  the headlamp aperture at 0.180 m, and REF says in the same breath that
  *lateral scale varies by more than 2:1 across the front panel and a fitted
  projection model did not close.* The tube is at `u 260–286`, the headlamp at
  `u 419`. **The most promising untried route is a SCALE-FREE RATIO at the same
  station** — the tube's vertical thickness against the **bumper blade's face
  height in the same columns** (0.133 m at S = 211.2, 0.123 m at S = 211.5,
  stock T1 ≈ 0.12 m — an 8 % spread that must be carried). **Ask first**: rev 26
  found the foreground trolley occludes the blade's lower edge in 5 of 8
  columns, so the question is WHICH COLUMNS SHOW THE TRUE BLADE BOTTOM.
- **§10.82 did NOT fix `COUNTERTAN`** — still 34.0 % short in B.
- **The residual pedestal** — only the scene→top bounce remains, but
  **§10.70's arms must be RE-RUN on the post-retirement build first.**
- **THE FRONT BUMPER FACE IS UNMEASURED.** **`CREAM`.** **THE ABSOLUTE ROOF
  HEIGHT.** **THE OFF FLANK, 804.9 mm.**
- `GAL_SKY` dead lever. `PLATE_W = 0.3300` no provenance.
  `probe_rev16.py:90` prints `xa` vs `xa`.
## 5. FIRST QUESTIONS FOR THE OWNER — NONE OUTSTANDING
rev 29's question was answered and it changed the work. **No decision is
outstanding.** What would still move the most is one photograph: **a head-on
rear (or front) elevation from roof height or above, with the counter and the
lids clear of the section** — it is the only realistic route to closing
`CREAM`, the absolute roof height, and the B residual. A clear view of the
**off flank** closes 804.9 mm. **And for the over-rider: any frame showing the
FRONT of the vehicle with a feature of known size in the bumper plane.**
## 6. Ordered work list for rev 30
1. **THE FRONT OVER-RIDER (§10.75, §10.80).** Now the oldest and best-posed
   undone item. Ask the blade-column question FIRST, then the scale-free ratio
   **or a proof none is admissible**, then size and build, **every number
   tagged workshop-stage**. **This moves geometry.**
2. **A HERO — it is OWED.** `rev25_hero34f.png` is stale for shading after
   §10.82. If item 1 lands first, shoot once, after it.
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
gone wrong in ELEVEN revisions during handoff assembly.** rev 23 through rev 29
were clean runs.
**FINAL COUNT: 135 commits, clean tree.**
