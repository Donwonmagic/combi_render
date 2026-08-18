# NEXT CONTEXT PROMPT — rev 41
Please act as my expert. Continue the Señor Tacombi combi build. **Forty revisions
sit behind this.** You are picking up mid-stream, not starting.

## Step 0 — CHECK A FOLDER IS CONNECTED BEFORE YOU PLAN ANYTHING
Call `get_device_info`. **In rev 32 through rev 40 `~/Desktop/tacombi_bus_render`
was ALREADY in `connectedFolders` on the first call** — nine in a row. It timed
out unanswered in rev 28/29 and was granted on the first request in rev 30/31.
**Do not assume any of those outcomes** — call it, and say plainly what came back.

**THE BRIDGE DROPPED TWICE IN REV 40, mid-restore and again at write-up**, and
came back both times on his word. rev 31/35/36/39's pattern. **WAIT IT OUT AND DO
CLOUD-SIDE WORK IN BETWEEN. DO NOT RETRY IN A LOOP.** A 60-second stage timeout
with nothing landed is a transient; the next call may return
*"device ... is not connected to the bridge"*, which is the real drop.

**THE BRIDGE HAS A THROUGHPUT CEILING, NOT JUST A SIZE ONE.** Only TWO files need
splitting: the 19.5 MB base bundle (7 parts) and the 8.5 MB `rev14_unified`
(3 parts). **Everything rev15–rev40 is under 3 MB and crosses whole.**
**REV 34–40 ALL REUSED REV 33's `_xfer33/` SPLIT PARTS.** They are still on his
disk and their sizes sum **byte-exactly** to both source bundles — base parts to
**19,478,840**, r14u parts to **8,519,034**. Check that before spending
`device_bash`. **REV 40 MOVED 36 FILES IN 8 BRIDGE CALLS** once the bridge was up.

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
`/areas/tacombi-combi-3d.md`, then `-rev14`, `-rev17` ... `-rev39`, then
**`/areas/tacombi-combi-3d-rev40.md`** (SEPARATE FILES; each revision's file does
NOT carry the next), then `/areas/tacombi-combi-sticker.md`, then
`/preferences.md`. If you cannot read them, say so explicitly.

**A MEMORY ENTRY IS A CLAIM TOO — GREP IT.** Rev 37 found memory had invented
`MIGRATION_APPENDIX_rev32.md`, a file that has never existed in any ref; rev 39
and rev 40 both re-checked and it still has not.

**CHECK THIS PROMPT AGAINST MEMORY BEFORE TRUSTING ITS WORK LIST.**
**REV 40 FOUND THE REV-40 PROMPT'S OWN §6 ITEM 1 WAS A DATUM ERROR AND REFUSED TO
EXECUTE IT.** The rev-39 prompt's §6 item 1 named the wrong photograph. **TWO
REVISIONS RUNNING THE BRIEF'S ITEM 1 HAS BEEN WRONG. Grade item 1 before you
build it.**

**I have never stood in the bus.** The "remember standing in the kombi" bar is
about the RESTAURANT'S owner. **Do not ask me what the real vehicle looks like.**
Ask me what a PHOTOGRAPH shows — that has now paid off thirty-one times.

## Step 2 — restore, and verify BY CONTENT (never by hash or commit count)
See §11. **TWENTY-EIGHT bundle lines now**, and the rev14b line is a `fetch` that
must come BEFORE rev15. rev 20 through rev 40 all restored CLEAN.

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
**THE GUARDS ARE 0 fail / 0 WARN. NO GEOMETRY MOVED IN REV 40** — it is an
instrument revision. **131 objects, 190 meshes**, exactly as rev 38 shipped.
**Every figure is identical to rev 38's and rev 39's.**

**RUN THE PROBES YOU INHERIT, NOT ONLY THE ONES YOU WRITE.** **29 now** — rev 40
added `probe_rev40_datum.py`. Under `blender -b --python`: `probe_ctan_index`,
`probe_dust_scope`, `probe_f90`, `probe_rev16`, **`probe_cross_anatomy` and
`probe_shutlines` (transitive)**, `probe_rev36_barend`, **and both rev38 probes**.
Everything else under `/tmp/blender/4.5/python/bin/python3.11` — **including
`probe_clean_top` and `probe_dust_anchor`, whose only `bpy` is in a comment, and
`probe_rev39_flank` and `probe_rev40_datum`.**

**READ EACH PROBE'S OWN SUMMARY LINE. DO NOT RE-DERIVE IT.** Wordings differ:
`probe_rev36_posts` prints `ALL 5 CONTROLS PASSED`, not `CONTROLS: n checked`.
**A SUMMARY GREP UNDER-READ SIX PROBES IN REV 37 AND AGAIN IN REV 39.**
Expected: **`rev40_datum` 4 checked / 1 FAILED — C3 IS *SUPPOSED* TO FAIL, see
§9**, `rev39_flank` **3/0 and NO RULING on flatness, see §6 item 1**,
`rev38_wheelbar` **6/0**, `rev38_floorpen` **1/0**, `rev36_posts` **5/0**,
`rev35_harmonic` **18/6**, `rev34_levels` **8/4**, `rev34_ruling` **6/4**,
`rev33_barend` **7/4**, `orb_xratio` **6/1**, `rev32_pointer` **10/0**,
`dust_scope` **8/0**, `updust_pointer` **6/0**, `psf_lines` **2 FAILED both
EXPECTED**, `clean_top` and `dust_anchor` **DELIBERATELY LEFT FAILING**.
**`probe_rev36_barend` PRINTS "REFUSING TO PRINT A RULING"** and that is CORRECT.
**Do not "fix" any of these.**

Both flank probes need `out/p_side.png` (see §10) and `probe_rev40_datum` needs
it too.

## Step 4 — read, in this order
`STATE.md` → `SPEC.md` §10, then §10.9 through §10.98 → this file →
**`HANDOFF_rev40.md`** → `HANDOFF_rev39.md` → ... → `REF_MEASUREMENTS.md`.
`STATE.md` is machine-written; **if it and any prose disagree, it is right — BUT
CHECK ITS PROVENANCE ROWS FIRST**, including the `working tree` row. **If that
says DIRTY, the file is not a record of anything.** Rev 38 shipped it DIRTY;
rev 39 and rev 40 both shipped it CLEAN. **Check it anyway.**

---
# §6. ORDERED WORK LIST FOR REV 41

**HIS EIGHT DEFECT REPORTS ARE STILL THE SPINE. TWO ARE CLOSED (6 and 8, rev 38).
DO NOT RE-OPEN EITHER. REPORT 3 IS *NOT* CLOSED AND *NOT* SOLVED** — rev 39
thought it had it at 81 mm; rev 40 showed that was a datum error. It is back
where rev 38 left it, as SPEC §10.24.

1. **RE-DERIVE `probe_rev39_flank.py`'s BAND ACCEPTANCE GATE.** On the corrected
   datum, seven z bands cluster at **−5 to −24 mm** and three return
   **±193–222 mm** — **the same three that DECLINED under the rev-39 datum**, and
   +222 mm is the exact figure §10.97.7 says its gate exists to kill.
   **Prominence cannot separate them** (1.20 / 1.30 / 1.55 against a good band's
   1.23). **STATE THE CRITERION BEFORE THE RUN. DO NOT WIDEN ANYTHING, and do not
   pick a number that makes your answer come out** — rev 40 deliberately left the
   ladder saying NO RULING rather than tune it. §10.98.10.
2. **`SCR`: +76.2 mm FORWARD and −33.3 mm, i.e. 33 mm UP.** SPEC 10.98.8. Now
   measured through a datum that is checked two-sided. **The forward term never
   moved** — the datum is a horizontal line and never entered x. Re-measure once
   after any counter change, then apply. §10.29: re-fit jointly, never separately.
3. **THE COUNTER'S PAINTED FASCIA IS 6.5 mm SHORT** — 87.1 mm built
   (`CNT_ZT − CNT_ZB − CNT_NOSE_F × slab`) against **93.6 ± 2.0 mm** (rev 40's
   probe, 5 columns) and **94.3 mm** (`t1_detail`'s own independent 113-column
   half-max run), two photographic readings 0.7 mm apart. §10.98.11.
   **DECIDE WHICH END MOVES**: `CNT_ZB` is REF §3b's MEASURED 1.082 m AG,
   `CNT_ZT` is not independently measured. **Moves geometry, so it owes a hero.**
4. **REPORT 5 — THE DOORS EXTEND LOWER, AROUND THE WHEEL WELL.** `doorback1`'s
   bottom is a straight line **52 mm above the tyre crown**, pinned 11 mm above
   the front arch lip by `t1_shell:497`'s assert. **MEASURE IT OFF
   `ref_workshop.jpg`, NOT `ref_side.jpg`** — the cab door is OPEN 49° there
   (SPEC 10.97.12). The route is a SCALE-FREE RATIO against the arch, whose
   radius `ARCH_R` is locked; that frame carries no admissible px/m on the door
   plane (§10.62). `_DOOR_TOP_AUTH` (1.8140) and `DOOR_H` (1.013467) are
   AUTHORED, and the door's LOWER boundary has never been measured.
5. **REPORT 4 — THE VW GLYPH.** §10.25's premise is FALSE: SPEC's own later entry
   records *"no gap but a 52 mm interpenetration"*. There was never a 12.7 mm air
   gap to preserve, so the V and W still **fuse into an X**. §10.94.
6. **REPORT 7 — "100% CALIDAD" OFF CENTRE.** `cal_gen.py:246` places it at an
   absolute **0.180 of texture width**. **DETERMINE TEXTURE-VERSUS-PANEL BEFORE
   TOUCHING EITHER** (§10.20's family). **DISTINCT from my earlier sticker
   LEGIBILITY complaint. Do not merge them.** §10.95.3.
7. **REPORTS 1 & 5 — `V_POW`.** Locked at **0.60** (§10.2, `t1_shell.py:1070`);
   the rev-11 audit implies **0.30–0.48**. **MIRROR ANY CHANGE INTO
   `t1_shell.nose_shape.zV`** or the pressed swage and the painted break
   de-register.
8. **`probe_clean_top.py` and `probe_dust_anchor.py` — REWRITE OR RETIRE.**
   **EIGHT revisions now.** Decide the post-retirement question first. **Do not
   widen a tolerance.**
9. **A HERO, after anything that moves geometry.** Camera absolutely last.

**SHOOT THE HERO AT THE END, AND SHOOT IT EVERY REVISION THAT MOVES GEOMETRY.
AND RE-RUN THE PROBES TOO.**

---
## §7. INSTRUCTIONS OF MINE STILL OUTSTANDING, IN NO OTHER CARRIER
Grep each before acting — a memory entry is a claim.
1. ~~**DRIVE FIXES OFF THE BROADSIDE RENDER LAID OVER `ref_side.jpg`**~~ —
   **DONE IN REV 39, AND ITS DATUM CORRECTED IN REV 40.**
   `probe_rev39_flank.py` is the instrument and it is a standing one.
   **RE-RUN IT EVERY REVISION THAT MOVES THE FLANK.**
2. **"REMEMBER TO HOLD UP NEXT TO THE ACTUAL SOURCE PHOTOS."** A standing check.
   Rev 39/40 did it for the show flank. **Still never done for the NOSE, the TAIL
   or the ROOF.**
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
   10.97.11. **Do not re-open it.**
6. **ABSOLUTE REPLICATION OF ALL ARTWORK** — mural board, flank paisley, the
   script, the Calidad decal, **the menu strips and cards, the rear-lid
   lettering, the plate surround**. A hard bar. Rev 10 recorded the lettered panel
   reads *"La S——— and no further"* and that **"La Santa" is a RECONSTRUCTION**.
7. **THE SEÑOR TACOMBI SCRIPT — I REJECTED IT TWICE.** On the corrected datum
   `flank_compare` puts `Senor` at **0.459 of its own ceiling**, and its
   texture-only control scores **0.7595 = 0.884** overall — so **the failure is
   the PANEL and the `Senor` reconstruction, not the render.**
   Also open: **the silver is FLAT** — `tex/senor.png` emits a constant
   (214,216,218) against reference per-channel std 16–19.
8. **THE FRONT ROOF LID NEEDS TWO-SIDED ARTWORK** — my settled topology, never
   implemented. `roof_lids()` gives each lid ONE board face. Also mine: **a TRUNK
   LID, separate from the roof lids, and region C is that trunk lid, OPEN.**
   `grep -c trunk t1_shell.py build.py` is **0 and 0** — verified in rev 39.
9. **"CLUTTER ON THE COUNTER"** — a defect I raised more than once, never
   recorded as closed, and rev 11 then dressed the galley with 51 objects.
10. **I STATED THE BUS SITS NOTICEABLY LOWER THAN STOCK.** **NEITHER REV 39 NOR
    REV 40 MEASURED THIS AND NEITHER MUST BE READ AS HAVING DONE SO** — both
    numbers are relative to the counter fascia by construction and say nothing
    about ride height. Still unadjudicated.
11. **NOLITA IS RE-ADMITTED FOR GEOMETRY ONLY** (rev 15, §10.32).
    `grep -ic nolita`: **9 in SPEC, 0 in REF_MEASUREMENTS.** Twenty-five
    revisions, **no Nolita frame ever measured.** **AN AUTHORISED SOURCE CLASS IS
    SITTING UNUSED.** Every Nolita-derived number must be TAGGED.
12. **THE GITHUB MIGRATION** I asked to have executed (rev 31c). Still
    unfulfilled; its supposed artefact is a phantom, re-checked in rev 40.
    **Running Claude Code LOCALLY was raised alongside it and never decided.**
13. ~~**REGION 3**~~ — **CLOSED BY ME IN REV 40: THE PALE BAND IS THE COUNTER'S
    FRONT FACE.** It supersedes rev 12's "body's own belt paint" and explains my
    rev-19 non-selection. **DO NOT RE-PUT IT.** §10.98.11.
14. **THE STANDARD, IN MY WORDS:** *"we are recreating a photo realistic version
    of that exact bus"* and *"any single measurement off is unacceptable"*. Also:
    4K non-overlapping textures and no floating artifacts — **no revision has
    ever run a UV-overlap or texture-resolution check.** Verified 0 in rev 40.

## §8. ALREADY SETTLED — do not re-open without new evidence AND a different method
**REPORT 6 IS CLOSED** (the bar across the front wheel was `cab_floor`; four
wheel houses built, both pans narrowed to `FLOOR_W = 1.200`). **REPORT 8 IS
CLOSED** (second `lid_strut` in `roof_lids()`). SPEC 10.96.
**THE FRONT OVER-RIDER ASSEMBLY IS WITHDRAWN — BAR AND POSTS.** My decision,
rev 37. **DO NOT RE-PROPOSE IT** without a square-on frame of the front or my
say-so — **it is ANSWERED, not open.** `build.py`'s two calls are **COMMENTED,
NOT DELETED**; the guards stay armed and log NOT APPLICABLE.
**THE MURAL BOARD'S TEN FLOWER HEADS ARE SETTLED BY ME** (rev 39).
**REGION 3 IS SETTLED BY ME** (rev 40) — the counter's front face.
**THE TYRE DIAMETER IS RIGHT** — rev 39 measured 651 ± 13 mm against the locked
665. **Do not re-open it off a visual impression of the overlay.**
**THE MODEL'S BREAK-TO-SILL IS RIGHT TO 2.7 mm** (rev 40) — 100.0 mm built
against 102.7 ± 6.6 photographed and REF §3a's own 100.0. **Do not move the
break line without a measurement that does not pass through the counter.**

## §9. HARD-WON RULES — every one was learned by breaking it
Every rule in the rev-40 prompt still stands. **NEW in rev 40:**
* **TWO DATUM LINES ARE NOT ONE DATUM JUST BECAUSE A COMMENT SAYS SO.** Check
  which physical edge each estimator lands on, in each frame, separately.
  §10.45's *a claim in prose is not a guard* — and the prose was inside the
  instrument.
* **DIFFERENT ESTIMATORS FIND DIFFERENT EDGES.** A luminance step and a redness
  step on a cream / gold / beige / red stack are different boundaries. If two
  sides of a differential use different estimators, the difference does not
  cancel — it carries a member's whole height as a systematic.
* **SEQUENTIAL REGISTRATION OF COUPLED AXES IS NOT REGISTRATION.** dx-then-dy
  returned −71 mm where a joint search returns −19 mm.
* **AN ACCEPTANCE GATE CALIBRATED ON ONE DATUM DOES NOT TRANSFER TO ANOTHER.**
  Three bands that correctly DECLINED under one datum sail through under the
  corrected one, returning the exact fictional figure the gate was written to
  kill.
* **NAMING A DEFECT CLASS DOES NOT IMMUNISE YOU AGAINST IT.** Rev 40 committed a
  scope error inside the section documenting scope errors, in the same hour.
* **A PRICED BIAS EARNS ITS KEEP LATER; A LOOSENED ONE CANNOT.** C3's +1.25 px
  was recorded as a number, which is what made it available to test a later
  figure against — and to show it must NOT be applied there, because it is
  referenced to a different edge criterion.
* **WHEN A FINDING IS THE PREVIOUS REVISION'S HEADLINE, FIND A ROUTE THAT SHARES
  NO DATUM WITH IT.** Break-to-sill is body-internal and settled it at −2.7 mm.

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
  (rev 36). One crop, one mark, one sentence. **That format closed region 3 in
  rev 40 after twenty-one revisions.**

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

**Both flank probes NEED `out/p_side.png`**, which is gitignored, so **produce it
first** (≈95 s):
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
**THIS HAS GONE WRONG IN FOURTEEN REVISIONS DURING HANDOFF ASSEMBLY.**
**A grep count is invalidated by any later edit to the file it counts.**
**ANCHOR HEADING COUNTS WITH `^`. `grep -c` COUNTS LINES, NOT OCCURRENCES.**
**CHECK EVERY ANCHOR'S CASE AND THAT IT DOES NOT WRAP ACROSS A LINE BREAK.**

### Restore, twenty-eight lines. The rev14b line is a `fetch`, BEFORE rev15.
```bash
git clone tacombi_history_rev9.bundle tacombi && cd tacombi
git pull --ff-only ../tacombi_rev14_unified.bundle HEAD          # -> 59
git fetch ../tacombi_rev14b_incremental.bundle HEAD:refs/heads/b14   # FETCH
git pull --ff-only ../tacombi_rev15_incremental.bundle HEAD      # -> 67
#   ... rev16 71, rev17 75, rev18 81, rev19 87, rev20 93, rev21 96, rev22 101,
#       rev23 105, rev24 107, rev25 115, rev26 120, rev27 126, rev28 130,
#       rev29 135, rev30 148, rev31 158, rev32 166, rev33 173, rev34 182,
#       rev35 187, rev36 191, rev37 203, rev38 207, rev39 211
git pull --ff-only ../tacombi_rev40_incremental.bundle HEAD      # -> SEE BELOW
```
**If a pull says "Need to specify how to reconcile divergent branches", STOP.**
The hero is gitignored and lives only on my disk.

### Content checks — all read off the fresh clone
**One candidate anchor of mine returned 0 because SPEC wraps it across a line
break — the rev-36 trap, caught before publication and REPLACED, not loosened.**
```bash
git status                                              # clean
grep -c '^### 10.98' SPEC.md                            # 1
grep -c '^#### 10.98' SPEC.md                           # 13
grep -c '10.98' SPEC.md                                 # 21
grep -c "THE COUNTER'S FRONT FACE" SPEC.md              # 3   NOTE THE QUOTES
grep -c 'CNT_NOSE_F' SPEC.md                            # 5
grep -c 'break-to-sill' SPEC.md                         # 2
grep -c 'CLOSED BY HIM' SPEC.md                         # 3   CASE MATTERS
grep -c 'T1_FC_OLDDATUM' SPEC.md                        # 2
grep -c 'T1_FC_OLDDATUM' flank_compare.py               # 3
grep -c '_assert_same_edge' flank_compare.py            # 4
grep -c 'def _assert_same_edge' flank_compare.py        # 1
grep -c 'JOINT registration' probe_rev39_flank.py       # 1   SINGLE-LINE ANCHOR
grep -c 'def _score' probe_rev39_flank.py               # 1
grep -c 'def _authored' probe_rev40_datum.py            # 1
grep -c 'CNT_NOSE_F' probe_rev40_datum.py               # 5
grep -c 'SCOPE' probe_rev40_datum.py                    # 1
grep -c 'STOPPED its own item 1' HANDOFF_rev40.md       # 1
grep -c 'probe_rev40_datum' HANDOFF_rev40.md            # 2
#   inherited, must still hold:
grep -c '^### 10.97' SPEC.md                            # 1
grep -c '^### 10.96' SPEC.md                            # 1
grep -c 'cab_floor' SPEC.md                             # 4
grep -c 'T1_ABLATE' build.py                            # 5
grep -c 'FLOOR_W' t1_detail.py                          # 5
grep -c '190' probe_dust_scope.py                       # 4
grep -c 'amtrak' SPEC.md                                # 2   HIS WORD
grep -ic 'nolita' SPEC.md                               # 9
grep -c 'TEN flower heads' SPEC.md                      # 1
ls HANDOFF_rev40.md STATE_rev40.md SPEC_rev40.md NEXT_CONTEXT_PROMPT_rev41.md \
   probe_rev40_datum.py rev40_datum.png rev40_q_region3.png
ls probe_*.py | wc -l    # 29
ls rev38_hero34f.png     # MUST FAIL -- heroes are gitignored
```
Ancestry — **rev 40 adds `668614e`, the rev-39 tip (19 now):**
```bash
for c in f3c53f4 87aeaa6 d519fc6 5087b84 7ce3d03 f3cde44 efc1268 456b201 \
         b08e424 e792d73 6f87977 cac32b9 2253399 52e451a 3496cab b6a93ec \
         54fc45d 4843cc3 668614e; do
  git merge-base --is-ancestor $c HEAD && echo "$c ok" || echo "$c LOST"; done
```
Textures — **all three must match; rev 40 changed NO artwork:**
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

**NO GEOMETRY MOVED IN REV 40.** 42 materials, 5 constant-rough, **0
non-manifold**, rake 17.75, L=4.065 W=1.750, arch gaps 39.7 / 40.7 mm, off flank
804.9 mm — every figure identical to rev 38's and rev 39's.

**No hero this revision, and none is owed** — the mesh has not moved since rev 38
shot `rev38_hero34f.png`. **The moment item 3 lands, one IS owed.**

**Two figures ARE in the repo this time** (153 KB and 63 KB, well under the bridge
ceiling): `rev40_datum.png` and `rev40_q_region3.png`.

**FINAL COUNT: 215 commits, clean tree.** *(This line lands in commit 215 itself
— rev 29's pattern, kept since.)*
