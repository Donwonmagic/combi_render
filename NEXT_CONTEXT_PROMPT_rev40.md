# NEXT CONTEXT PROMPT — rev 40
Please act as my expert. Continue the Señor Tacombi combi build. **Thirty-nine
revisions sit behind this.** You are picking up mid-stream, not starting.

## Step 0 — CHECK A FOLDER IS CONNECTED BEFORE YOU PLAN ANYTHING
Call `get_device_info`. **In rev 32 through rev 39 `~/Desktop/tacombi_bus_render`
was ALREADY in `connectedFolders` on the first call** — eight in a row. It timed
out unanswered in rev 28/29 and was granted on the first request in rev 30/31.
**Do not assume any of those outcomes** — call it, and say plainly what came back.

**THE BRIDGE HAS A THROUGHPUT CEILING, NOT JUST A SIZE ONE.** Only TWO files need
splitting: the 19.5 MB base bundle (7 parts) and the 8.5 MB `rev14_unified`
(3 parts). **Everything rev15–rev39 is under 3 MB and crosses whole.**
**REV 34–39 ALL REUSED REV 33's `_xfer33/` SPLIT PARTS.** They are still on his
disk and their sizes sum **byte-exactly** to both source bundles — base parts to
**19,478,840**, r14u parts to **8,519,034**. Check that before spending
`device_bash`. **REV 39 MOVED 35 FILES IN 8 BRIDGE CALLS WITH ZERO TRANSIENT
FAILURES.** Do not read that as the new normal: rev 32 had two `upload failed`
in one batch and the bridge genuinely drops. **TRANSIENT FAILURES ARE NOT DROPS.
Do not retry in a loop.**

**`device_bash` DOES NOT SEE `/Users/...`** — the mount is
`/sessions/<session-id>/mnt/tacombi_bus_render`. **`device_stage_files` DOES take
the `/Users/...` path. AND YOUR SHELL'S `~` IS `/root`.**

**`hero.py` IS NOT A BLENDER SCRIPT** — it is a plain Python driver. To preview,
drive `build.py`:
```bash
T1_SUB=1 T1_PREVIEW=hero34f T1_FX=0 T1_RX=1600 T1_RY=1067 T1_SAMP=24 \
  T1_OUT=/tmp/prev T1_PFX=pv blender -b --python build.py     # ~225 s
```
**`ref_workshop.jpg`, `ref_side.jpg` and `ref_rear34.jpg` are IN THE REPO.**

## Step 1 — read my memory BEFORE you read any code
`/areas/tacombi-combi-3d.md`, then `-rev14`, `-rev17` … `-rev38`, then
**`/areas/tacombi-combi-3d-rev39.md`** (SEPARATE FILES; each revision's file does
NOT carry the next), then `/areas/tacombi-combi-sticker.md`, then
`/preferences.md`. If you cannot read them, say so explicitly.

**A MEMORY ENTRY IS A CLAIM TOO — GREP IT.** Rev 37 found memory had invented
`MIGRATION_APPENDIX_rev32.md`, a file that has never existed in any ref; rev 39
re-checked and it still has not.
**CHECK THIS PROMPT AGAINST MEMORY BEFORE TRUSTING ITS WORK LIST.**
**REV 39 FOUND THE REV-39 PROMPT'S OWN §6 ITEM 1 NAMED THE WRONG PHOTOGRAPH** —
see §9.

**I have never stood in the bus.** The "remember standing in the kombi" bar is
about the RESTAURANT'S owner. **Do not ask me what the real vehicle looks like.**
Ask me what a PHOTOGRAPH shows — that has now paid off thirty times.

## Step 2 — restore, and verify BY CONTENT (never by hash or commit count)
See §11. **TWENTY-SEVEN bundle lines now**, and the rev14b line is a `fetch` that
must come BEFORE rev15. rev 20 through rev 39 all restored CLEAN.

## Step 3 — install Blender 4.5.3 and run BOTH guards before proposing anything
```bash
curl -fsSL -o b.tar.xz https://download.blender.org/release/Blender4.5/blender-4.5.3-linux-x64.tar.xz
tar -xf b.tar.xz && mv blender-4.5.3-linux-x64 /tmp/blender
/tmp/blender/4.5/python/bin/python3.11 -m pip install pillow scipy
```
That pip line is required. Guards are `T1_SUB=n T1_VERIFY=1 blender -b --python
build.py` and `T1_SUB=n blender -b --python audit.py`. Report the guards' ACTUAL
output, both levels. **`audit.py` rewrites `STATE.md` every run — `git checkout
STATE.md` after.**

**THE GUARDS ARE 0 fail / 0 WARN. NO GEOMETRY MOVED IN REV 39** — it is a
measurement revision. **131 objects, 190 meshes**, exactly as rev 38 shipped.
**Every figure is identical to rev 38's.**

**RUN THE PROBES YOU INHERIT, NOT ONLY THE ONES YOU WRITE.** **28 now** — rev 39
added `probe_rev39_flank.py`. Under `blender -b --python`: `probe_ctan_index`,
`probe_dust_scope`, `probe_f90`, `probe_rev16`, **`probe_cross_anatomy` and
`probe_shutlines` (transitive)**, `probe_rev36_barend`, **and both rev38 probes**.
Everything else under `/tmp/blender/4.5/python/bin/python3.11` — **including
`probe_clean_top` and `probe_dust_anchor`, whose only `bpy` is in a comment, and
`probe_rev39_flank`.**
**READ EACH PROBE'S OWN SUMMARY LINE. DO NOT RE-DERIVE IT.** Wordings differ:
`probe_rev36_posts` prints `ALL 5 CONTROLS PASSED`, not `CONTROLS: n checked`.
**MY OWN SUMMARY GREP UNDER-READ SIX PROBES IN REV 39** — rev 37's trap,
reproduced. Expected: `rev39_flank` **2/0** (and it needs `out/p_side.png`, see
§6), `rev38_wheelbar` **6/0**, `rev38_floorpen` **1/0**, `rev36_posts` **5/0**,
`rev35_harmonic` **18/6**, `rev34_levels` **8/4**, `rev34_ruling` **6/4**,
`rev33_barend` **7/4**, `orb_xratio` **6/1**, `rev32_pointer` **10/0**,
`dust_scope` **8/0**, `updust_pointer` **6/0**, `psf_lines` **2 FAILED both
EXPECTED**, `clean_top` and `dust_anchor` **DELIBERATELY LEFT FAILING**.
**`probe_rev36_barend` PRINTS "REFUSING TO PRINT A RULING"** and that is CORRECT.
**Do not "fix" any of these.**

## Step 4 — read, in this order
`STATE.md` → `SPEC.md` §10, then §10.9 through §10.97 → this file →
**`HANDOFF_rev39.md`** → `HANDOFF_rev38.md` → … → `REF_MEASUREMENTS.md`.
`STATE.md` is machine-written; **if it and any prose disagree, it is right — BUT
CHECK ITS PROVENANCE ROWS FIRST**, including the `working tree` row. **If that
says DIRTY, the file is not a record of anything.** **REV 38 SHIPPED IT DIRTY AND
REV 39's OWN BRIEF SAID IT WAS CLEAN** — rev 39 resolved it by REGENERATING and
diffing (byte-identical but for the four provenance rows) rather than trusting
either. **Rev 39's `STATE.md` reads `working tree | clean`. Check it anyway.**

---
# §6. ORDERED WORK LIST FOR REV 40

**HIS EIGHT DEFECT REPORTS ARE STILL THE SPINE. TWO ARE CLOSED (6 and 8, rev 38).
DO NOT RE-OPEN EITHER.**

1. **REPORT 3 — THE BREAK LINE. 81 ± 7 mm, AND IT IS THE ITEM WITH THE MOST
   EVIDENCE BEHIND IT IN THE PROJECT.** SPEC 10.97.5–6. Rev 39 measured the whole
   flank silhouette against the cream/red two-tone break: **flat in u** (5 bands,
   spread 4 px) and **flat in z** (7 of 10 bands answered, spread 19 mm over
   z 0.10 → 2.00). One rigid offset. **THE BREAK LINE SITS ~81 mm TOO LOW ON THE
   BODY.**
   **MOVE THE BREAK. DO NOT MOVE THE LAMPS AND DO NOT MOVE THE ROUNDEL.** That is
   not caution, it is the whole point: §10.24 was applied and reverted TWICE, and
   what killed it each time was the frontal silhouette of `ref_side.jpg` refuting
   the finding **as applied** — and *as applied* meant moving the headlamps.
   Moving the break instead leaves the roundel untouched **by construction**,
   leaves the lamps untouched so that refutation does not bear on it, and is the
   RELATIONSHIP my report names rather than either half of it.
   **`probe_rev39_flank.py` IS THE GUARD FOR THIS. Re-run it after.** It should
   fall toward zero; if it does not, the change is wrong, not the probe.
2. **THEN `SCR`'s +76.2 mm FORWARD AND +61.9 mm DOWN** — SPEC 10.97.2,
   cross-checked in one run by `SCR`'s own x extents at +83 / +80 mm aft of
   `flank_X(LOCKUP)`, height **31.5 mm short** (rev 17's carried "12–24 mm" is
   superseded). **RE-MEASURE IT AFTER THE BREAK MOVES, NEVER BEFORE** — the break
   is `SCR`'s own vertical datum, and applying both as they stand double-counts.
   §10.29's rule: re-fit jointly, never separately.
3. **REPORT 5 — THE DOORS EXTEND LOWER, AROUND THE WHEEL WELL.** `doorback1`'s
   bottom is a straight line **52 mm above the tyre crown**, pinned 11 mm above
   the front arch lip by `t1_shell:497`'s assert. **MEASURE IT OFF
   `ref_workshop.jpg`, NOT `ref_side.jpg`** — see §9. The route is a SCALE-FREE
   RATIO against the arch, whose radius `ARCH_R` is locked; that frame carries no
   admissible px/m on the door plane (§10.62) so no metre figure may be taken
   from it directly. `_DOOR_TOP_AUTH` (1.8140) and `DOOR_H` (1.013467) are
   AUTHORED, and the door's LOWER boundary has never been measured.
4. **REPORT 4 — THE VW GLYPH.** §10.25's premise is FALSE: SPEC's own later entry
   records *"no gap but a 52 mm interpenetration"*. There was never a 12.7 mm air
   gap to preserve, so the V and W still **fuse into an X**. Rebuild against the
   interpenetration. §10.94.
5. **REPORTS 1 & 5 — `V_POW`.** Locked at **0.60** (§10.2, `t1_shell.py:1070`);
   the rev-11 audit implies **0.30–0.48**. **MIRROR ANY CHANGE INTO
   `t1_shell.nose_shape.zV`** or the pressed swage and the painted break
   de-register. **THIS INTERACTS WITH ITEM 1** — both move the nose's two-tone.
6. **REPORT 7 — "100% CALIDAD" OFF CENTRE.** `cal_gen.py:246` places it at an
   absolute **0.180 of texture width**. **DETERMINE TEXTURE-VERSUS-PANEL BEFORE
   TOUCHING EITHER** (§10.20's family). **DISTINCT from my earlier sticker
   LEGIBILITY complaint. Do not merge them.** §10.95.3.
7. **`probe_clean_top.py` and `probe_dust_anchor.py` — REWRITE OR RETIRE.**
   **SEVEN revisions now.** Decide the post-retirement question first. **Do not
   widen a tolerance.**
8. **A HERO, after anything that moves geometry.** Camera absolutely last.

**SHOOT THE HERO AT THE END, AND SHOOT IT EVERY REVISION THAT MOVES GEOMETRY.
AND RE-RUN THE PROBES TOO.**

---
## §7. INSTRUCTIONS OF MINE STILL OUTSTANDING, IN NO OTHER CARRIER
Grep each before acting — a memory entry is a claim.

1. ~~**DRIVE FIXES OFF THE BROADSIDE RENDER LAID OVER `ref_side.jpg`**~~ —
   **DONE IN REV 39, SPEC 10.97.** `probe_rev39_flank.py` is the instrument and
   it is now a standing one. **RE-RUN IT EVERY REVISION THAT MOVES THE FLANK.**
   It found the 81 mm and validated SPEC 10.35's map at −5 mm.
2. **"REMEMBER TO HOLD UP NEXT TO THE ACTUAL SOURCE PHOTOS."** A standing check.
   Rev 39 did it for the show flank. **Still never done for the NOSE, the TAIL or
   the ROOF.**
3. **THE DIE-CUT VINYL STICKER IS THE ORIGINAL DELIVERABLE AND IS UNBUILT.**
   For children at the restaurant; should spark joy and be something families
   keep. **Style LOCKED by me: cartoon with rendered depth.** **Scene LOCKED by
   me: nothing but the bus, die-cut tight, plus the sun and the papel picado.**
   *[stated, rev 39]* On the papel-picado conflict: **"Leave it open, I'll decide
   when the sticker is actually being built."** **DO NOT RE-PUT IT UNTIL THEN.**
   I also said I like how the wheels were drawn in the earlier cartoon version.
4. **THE PLAYA HERO IS DEPRIORITISED, NOT CANCELLED** — *"let's not do playa
   right now. Lets focus on the 3d model"*. The agreed deliverable is the
   white-studio hero for fidelity **PLUS** a warm low-light Playa hero, and **the
   Playa one carries the emotional bar that sits ABOVE clinical accuracy.**
5. ~~**NINE FLOWER HEADS**~~ — **CLOSED IN REV 39. I ANSWERED TEN.** SPEC
   10.97.11. `lid_gen.py`'s ten is right; my rev-8 count of nine is retired and
   SPEC §0's line is struck. **Do not re-open it.**
6. **ABSOLUTE REPLICATION OF ALL ARTWORK** — mural board, flank paisley, the
   script, the Calidad decal, **the menu strips and cards, the rear-lid
   lettering, the plate surround**. A hard bar. Rev 10 recorded the lettered panel
   reads *"La S——— and no further"* and that **"La Santa" is a RECONSTRUCTION**.
7. **THE SEÑOR TACOMBI SCRIPT — I REJECTED IT TWICE.** Rev 39 has the number at
   last: `flank_compare` puts `Senor` at **0.393 IoU = 0.503 of its own 0.782
   ceiling**, and its texture-only control scores **0.559** in the same box — so
   **the failure is the PANEL and the `Senor` reconstruction, not the render.**
   Also open: **the silver is FLAT** — `tex/senor.png` emits a constant
   (214,216,218) against reference per-channel std 16–19.
8. **THE FRONT ROOF LID NEEDS TWO-SIDED ARTWORK** — my settled topology, never
   implemented. `roof_lids()` gives each lid ONE board face. Also mine: **a TRUNK
   LID, separate from the roof lids, and region C is that trunk lid, OPEN.**
   `grep -c trunk t1_shell.py build.py` is **0 and 0** — verified in rev 39.
9. **"CLUTTER ON THE COUNTER"** — a defect I raised more than once, never
   recorded as closed, and rev 11 then dressed the galley with 51 objects.
10. **I STATED THE BUS SITS NOTICEABLY LOWER THAN STOCK.** **REV 39 DID NOT
    MEASURE THIS AND MUST NOT BE READ AS HAVING DONE SO** — its 81 mm is the body
    against the BREAK LINE, which is a relative measurement by construction and
    says nothing about ride height. Still unadjudicated.
11. **NOLITA IS RE-ADMITTED FOR GEOMETRY ONLY** (rev 15, §10.32).
    `grep -ic nolita`: **9 in SPEC, 0 in REF_MEASUREMENTS.** Twenty-four
    revisions, **no Nolita frame ever measured.** **AN AUTHORISED SOURCE CLASS IS
    SITTING UNUSED.** Every Nolita-derived number must be TAGGED.
12. **THE GITHUB MIGRATION** I asked to have executed (rev 31c). Still
    unfulfilled; its supposed artefact is a phantom, re-checked in rev 39.
    **Running Claude Code LOCALLY was raised alongside it and never decided.**
13. **REGION 3 — MY ANSWER IS OUTSTANDING.** `rev37_region3.png` asks: *is the
    pale band under the counter's brass nosing the BUS's own painted body, or
    part of the COUNTER?* **Shader routing, not geometry. Nothing moves until I
    answer.** §10.92. **NOT RE-PUT IN REV 39.**
14. **THE STANDARD, IN MY WORDS:** *"we are recreating a photo realistic version
    of that exact bus"* and *"any single measurement off is unacceptable"*. Also:
    4K non-overlapping textures and no floating artifacts — **no revision has
    ever run a UV-overlap or texture-resolution check.** Verified 0 in rev 39.

## §8. ALREADY SETTLED — do not re-open without new evidence AND a different method
**REPORT 6 IS CLOSED** (the bar across the front wheel was `cab_floor`; four
wheel houses built, both pans narrowed to `FLOOR_W = 1.200`). **REPORT 8 IS
CLOSED** (second `lid_strut` in `roof_lids()`). SPEC 10.96.
**THE FRONT OVER-RIDER ASSEMBLY IS WITHDRAWN — BAR AND POSTS.** My decision,
rev 37. **DO NOT RE-PROPOSE IT** without a square-on frame of the front or my
say-so — **it is ANSWERED, not open.** `build.py`'s two calls are **COMMENTED,
NOT DELETED**; the guards stay armed and log NOT APPLICABLE.
**THE MURAL BOARD'S TEN FLOWER HEADS ARE SETTLED BY ME** (rev 39).
**THE TYRE DIAMETER IS RIGHT** — rev 39 measured 651 ± 13 mm against the locked
665, inside the ±15 mm floor, at the rear-axle column the calibrated map placed.
**Do not re-open it off a visual impression of the overlay; that is exactly the
false lead rev 39 killed.**
Everything else from the rev-39 prompt's settled list stands.

## §9. HARD-WON RULES — every one was learned by breaking it
Every rule in the rev-39 prompt still stands. **NEW in rev 39:**
* **A PROBE THAT REPORTS THE END OF ITS OWN SEARCH RANGE IS NOT REPORTING A
  PEAK.** Three of ten z bands did, and manufactured a fictional 13 % vertical
  scale error I had already written down. The `or -9` / `_roof_at` shape, third
  instance. State the acceptance criterion BEFORE the run and make the probe
  DECLINE.
* **THE VERDICT MUST BE DERIVED, NOT PRINTED.** The first draft of
  `probe_rev39_flank.py` printed "FLAT IN HEIGHT" unconditionally — §10.50's
  defect, in the file that documents §10.50, written the same hour.
* **THE BRIEF CAN NAME THE WRONG PHOTOGRAPH.** The rev-39 prompt's §6 item 1 sent
  me to `ref_side.jpg` for the cab door's lower cutaway, worrying about the man's
  red shirt. **The door is OPEN 49° in that frame** and SPEC already said so
  twice. The blocker was never the shirt.
* **A CLASS GATE THAT EXCLUDES ITS OWN SUBJECT FAILS SILENTLY-LOOKING.** My
  flower-head detector gated `sat < 0.62` for "pale"; the heads are gold. 0/10 on
  its own positive control.
* **§10.7's RED SHIRT WILL TAKE YOUR DETECTOR.** Fourth instance. Anything
  gated on redness in `ref_side.jpg`'s lower-forward flank will find the man.
* **A LUMINANCE-ONLY GATE CANNOT SEPARATE BLACK RUBBER FROM RED PAINT** — the red
  body's luma is **79**. Two terms, and print the endmembers.
* **AN OVERLAY IS FOR SEEING, NOT FOR MEASURING.** Every impression it gives must
  be measured before it is written down. Mine said the wheels were too big; they
  are right to 14 mm.
* **CHECK A GREP ANCHOR'S CASE AND ITS LINE BREAKS.** Rev 39's first check list
  had one anchor wrapped across a line break (returned 0 — the rev-36 trap) and
  one that differed only in case. Both caught by the fresh-clone run.

## How I work
* Ground in the reference → build → adversarial audit → iterate. Never build
  before grounding. Never call it done off self-review.
* Report the measurement against the reference, **with its ceiling**. Never a
  self-assigned score.
* Do not tell me anything is ready. Tell me what is fixed, what is still wrong,
  and what you measured.
* Keep visible cadence on long work and send renders as they land.
* Travel between contexts consciously, every time.
* **Ask me questions as MULTIPLE CHOICE with reference material** (rev 26) — and
  **if I do not understand the question, the FIGURE is the defect, not me**
  (rev 36). One crop, one mark, one sentence.

---
> **THE STANDARD, in the owner's words.** The final product should be nearly
> indistinguishable from the original. **Any single measurement off is
> unacceptable.** The criterion is PER-MEASUREMENT. And above clinical accuracy:
> *"I want the owner to remember standing in the kombi, in this very picture that
> was provided."* — **that owner is the restaurant's owner.**
---

## §10. RESOLUTION AND THE SIDE PROBE
The hero: rev 38 shipped **4800×3200 in 20 strips**, SUB=2, 56 samples. Drive
`hero.py --only N` one strip per call then `--stitch-only`; run `post.py`
**once** on the stitched frame, never per strip. **TIMINGS RISE MONOTONICALLY
DOWN THE FRAME** — strips 0–2 ~145–157 s, strip 8 ~420 s, strip 15 ~548 s, and
**strip 16 was KILLED at 580 s by the 10-minute shell cap. Run the bottom strips
with `nohup ... &` and poll.** `hero.py` STRIPS IN ROW SPACE — SEAMS ARE
HORIZONTAL.

**`probe_rev39_flank.py` NEEDS `out/p_side.png`**, which is gitignored, so
**produce it first** (≈97 s):
```bash
T1_SUB=1 T1_PREVIEW=side T1_SAMP=24 T1_RX=1400 T1_RY=933 T1_FX=0 \
  T1_PFX=p blender -b --python build.py
```
`T1_FX=0` is load-bearing: every mask in that chain is a chromaticity rule.
**1400 px wide is a FLOOR, not a suggestion** — `flank_compare` documents a
verdict flip across its aspect tolerance at 900 px for no change in the model.

## §11. THE COMMIT COUNT AND THE CONTENT FIGURES
Written LAST, after the final commit. **EVERY VALUE BELOW WAS READ OFF A
FRESH-CLONE VERIFICATION RUN — none was typed from memory.**
**THIS HAS GONE WRONG IN FOURTEEN REVISIONS DURING HANDOFF ASSEMBLY.** Rev 39's
own first check list had **one anchor that returned 0 because it wrapped across a
line break** (the rev-36 trap, reproduced) and **one that differed only in case**.
Both were caught by the fresh-clone run and replaced, not loosened.
**A grep count is invalidated by any later edit to the file it counts.**
**ANCHOR HEADING COUNTS WITH `^`. `grep -c` COUNTS LINES, NOT OCCURRENCES.**

### Restore, twenty-seven lines. The rev14b line is a `fetch`, BEFORE rev15.
```bash
git clone tacombi_history_rev9.bundle tacombi && cd tacombi
git pull --ff-only ../tacombi_rev14_unified.bundle HEAD          # -> 59
git fetch ../tacombi_rev14b_incremental.bundle HEAD:refs/heads/b14   # FETCH
git pull --ff-only ../tacombi_rev15_incremental.bundle HEAD      # -> 67
#   ... rev16 71, rev17 75, rev18 81, rev19 87, rev20 93, rev21 96, rev22 101,
#       rev23 105, rev24 107, rev25 115, rev26 120, rev27 126, rev28 130,
#       rev29 135, rev30 148, rev31 158, rev32 166, rev33 173, rev34 182,
#       rev35 187, rev36 191, rev37 203, rev38 207
git pull --ff-only ../tacombi_rev39_incremental.bundle HEAD      # -> SEE BELOW
```
**If a pull says "Need to specify how to reconcile divergent branches", STOP.**
The hero is gitignored and lives only on my disk. **So are rev 39's two figures**
— they are 8.0 MB and 4.8 MB and would have taken the 16 KB bundle past the
bridge ceiling, so they are on my disk only, as rev 38 did with its A/B.

### Content checks — all read off the fresh clone
```bash
git status                                              # clean
grep -c '^### 10.97' SPEC.md                            # 1
grep -c '^#### 10.97' SPEC.md                           # 14
grep -c '10.97' SPEC.md                                 # 19
grep -c 'flank_compare' SPEC.md                         # 10
grep -c 'ONE RIGID OFFSET' SPEC.md                      # 1   SINGLE-LINE ANCHOR
grep -c 'no headlamp' SPEC.md                           # 1
grep -c 'IS NOT REPORTING A PEAK' SPEC.md               # 1   CASE MATTERS
grep -c 'RED SHIRT' SPEC.md                             # 1
grep -c 'TEN flower heads' SPEC.md                      # 1
grep -c 'nine flower heads' SPEC.md                     # 1   the STRUCK line
grep -c 'T1_R39_NOGATE' probe_rev39_flank.py            # 2
grep -c 'DECLINES' probe_rev39_flank.py                 # 1
grep -c 'DECLINED' probe_rev39_flank.py                 # 1
grep -c 'def best_dy' probe_rev39_flank.py              # 1
grep -c 'NO NEW ESTIMATOR' probe_rev39_flank.py         # 1
grep -c 'the break line is the misplaced' HANDOFF_rev39.md   # 1
grep -c 'MEASUREMENT revision' HANDOFF_rev39.md         # 1
grep -c 'probe_rev39_flank' HANDOFF_rev39.md            # 2
#   inherited, must still hold:
grep -c '^### 10.96' SPEC.md                            # 1
grep -c 'cab_floor' SPEC.md                             # 4
grep -c 'T1_ABLATE' build.py                            # 5
grep -c 'FLOOR_W' t1_detail.py                          # 5
grep -c '190' probe_dust_scope.py                       # 4
grep -c 'amtrak' SPEC.md                                # 2   HIS WORD
grep -ic 'nolita' SPEC.md                               # 9   was 8 in rev 38
ls HANDOFF_rev39.md STATE_rev39.md SPEC_rev39.md NEXT_CONTEXT_PROMPT_rev40.md \
   probe_rev39_flank.py
ls probe_*.py | wc -l    # 28
ls rev39_broadside_overlay.png   # MUST FAIL -- figures are not in the repo
```
Ancestry — **rev 39 adds `4843cc3`, the rev-38 tip (18 now):**
```bash
for c in f3c53f4 87aeaa6 d519fc6 5087b84 7ce3d03 f3cde44 efc1268 456b201 \
         b08e424 e792d73 6f87977 cac32b9 2253399 52e451a 3496cab b6a93ec \
         54fc45d 4843cc3; do
  git merge-base --is-ancestor $c HEAD && echo "$c ok" || echo "$c LOST"; done
```
Textures — **all three must match; rev 39 changed NO artwork:**
```bash
md5sum tex/swirl.png tex/swirl_b.png tex/nose.png
# 4ee4e09e...   d201597e...   b31ea156...
```
### Guards on the fresh clone, watched print
| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 0 warn** | **0 fail, 0 warn** |
| `audit.py` | **0 fail, 0 warn** | **0 fail, 0 warn** |
| roof crown @ rear axle | **1.9835** | **1.9833** |
| cut roof hole | **68564v** | **252749v** |
| objects at `materials:` | **131** | **131** |
| meshes | **190** | **190** |
| bay widths | 0.516 0.515 0.516 | same |
| over-rider rows | **NOT APPLICABLE, stated** | same |
**NO GEOMETRY MOVED IN REV 39.** 42 materials, 5 constant-rough, **0
non-manifold**, rake 17.75, L=4.065 W=1.750, arch gaps 39.7 / 40.7 mm, off flank
804.9 mm — every figure identical to rev 38's.
**No hero this revision, and none is owed** — the mesh has not moved since rev 38
shot `rev38_hero34f.png`. **The moment item 1 lands, one IS owed.**

**FINAL COUNT: 211 commits, clean tree.** *(This line lands in commit 211 itself
— rev 29's pattern, kept since.)*
