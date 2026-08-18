# NEXT CONTEXT PROMPT — rev 42

Please act as my expert. Continue the Señor Tacombi combi build. **Forty-one
revisions sit behind this.** You are picking up mid-stream, not starting.

## Step 0 — CHECK A FOLDER IS CONNECTED BEFORE YOU PLAN ANYTHING

Call `get_device_info`. **In rev 32 through rev 41 `~/Desktop/tacombi_bus_render`
was ALREADY in `connectedFolders` on the first call** — ten in a row. It timed
out unanswered in rev 28/29 and was granted on the first request in rev 30/31.
**Do not assume any of those outcomes** — call it, and say plainly what came back.

**AN ABSENCE HAS A TIMESTAMP TOO. REV 41 GOT THIS WRONG AND YOU MUST NOT.**
Rev 41's first recursive listing ran at 12:04 and found **zero** rev-40 files; it
reported rev 40 as having delivered nothing. **They landed at 12:08.** If a
delivery looks missing, say *when* you looked and ask before concluding. Rev 40's
own record said the bridge dropped **at delivery** — that means *in flight*, not
*never*.

**THE BRIDGE DROPPED TWICE IN REV 40** and came back both times on his word.
rev 31/35/36/39's pattern. **Rev 41 saw ZERO drops in 8 calls.** **WAIT IT OUT
AND DO CLOUD-SIDE WORK IN BETWEEN. DO NOT RETRY IN A LOOP.** A 60-second stage
timeout with nothing landed is a transient; the next call returning *"device …
is not connected to the bridge"* is the real drop.

**THE BRIDGE HAS A THROUGHPUT CEILING, NOT JUST A SIZE ONE.** Only TWO files need
splitting: the 19.5 MB base bundle (7 parts) and the 8.5 MB `rev14_unified`
(3 parts). **Everything rev15–rev41 is under 3 MB and crosses whole.**

**REV 34–41 ALL REUSED REV 33's `_xfer33/` SPLIT PARTS.** They are still on his
disk and their sizes sum **byte-exactly** to both source bundles — base parts to
**19,478,840**, r14u parts to **8,519,034**. Check that before spending
`device_bash`. **REV 41 MOVED 36 FILES IN 8 BRIDGE CALLS.**

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

`/areas/tacombi-combi-3d.md`, then `-rev14`, `-rev17` … `-rev40`, then
**`/areas/tacombi-combi-3d-rev41.md`** (SEPARATE FILES; each revision's file does
NOT carry the next), then `/areas/tacombi-combi-sticker.md`, then
`/preferences.md`. If you cannot read them, say so explicitly.

**A MEMORY ENTRY IS A CLAIM TOO — GREP IT.** Rev 37 found memory had invented
`MIGRATION_APPENDIX_rev32.md`, a file that has never existed in any ref; rev 39,
40 and 41 all re-checked and it still has not. Rev 41 also checked the **entire
git history across every ref** — 0 paths.

**CHECK THIS PROMPT AGAINST MEMORY BEFORE TRUSTING ITS WORK LIST.**
**REV 40 REFUSED ITS BRIEF'S ITEM 1 AS A DATUM ERROR. REV 41 GRADED ITS ITEM 1 AS
SOUND AND EXECUTED IT, AND REFUSED ITS ITEM 3 AS A RULER SCOPE ERROR.** Grade
every item before you build it — and notice that grading is not the same as
refusing.

**I have never stood in the bus.** The "remember standing in the kombi" bar is
about the RESTAURANT'S owner. **Do not ask me what the real vehicle looks like.**
Ask me what a PHOTOGRAPH shows — that has now paid off thirty-one times.

## Step 2 — restore, and verify BY CONTENT (never by hash or commit count)

See §11. **TWENTY-NINE bundle lines now**, and the rev14b line is a `fetch` that
must come BEFORE rev15. rev 20 through rev 41 all restored CLEAN.

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

**THE GUARDS ARE 0 fail / 0 WARN. NO GEOMETRY HAS MOVED SINCE REV 38** — rev 39,
40 and 41 are all measurement revisions. **131 objects, 190 meshes.**
**Every figure is identical to rev 38's.**

**RUN THE PROBES YOU INHERIT, NOT ONLY THE ONES YOU WRITE.** **30 now** — rev 41
added `probe_rev41_gate.py`. Under `blender -b --python`: `probe_ctan_index`,
`probe_dust_scope`, `probe_f90`, `probe_rev16`, **`probe_cross_anatomy` and
`probe_shutlines` (transitive)**, `probe_rev36_barend`, **and both rev38 probes**.
Everything else under `/tmp/blender/4.5/python/bin/python3.11` — **including
`probe_clean_top` and `probe_dust_anchor`, whose only `bpy` is in a comment, and
`probe_rev39_flank`, `probe_rev40_datum` and `probe_rev41_gate`.**
**`probe_ctan_index` is the slow one (~7 min); it renders.**

**READ EACH PROBE'S OWN SUMMARY LINE. DO NOT RE-DERIVE IT.** Wordings differ:
`probe_rev36_posts` prints `ALL 5 CONTROLS PASSED`, not `CONTROLS: n checked`.
**A SUMMARY GREP UNDER-READ SIX PROBES IN REV 37 AND AGAIN IN REV 39.**
Expected: **`rev41_gate` 5 checked / 1 FAILED — C4 IS *SUPPOSED* TO FAIL, see
§9**, **`rev40_datum` 4 / 1 — C3 IS *SUPPOSED* TO FAIL**, `rev39_flank` **3/0 and
NO RULING on flatness**, `rev38_wheelbar` **6/0**, `rev38_floorpen` **1/0**,
`rev36_posts` **5/0**, `rev35_harmonic` **18/6**, `rev34_levels` **8/4**,
`rev34_ruling` **6/4**, `rev33_barend` **7/4**, `orb_xratio` **6/1**,
`rev32_pointer` **10/0**, `dust_scope` **8/0**, `updust_pointer` **6/0**,
`psf_lines` **2 FAILED both EXPECTED**, `clean_top` and `dust_anchor`
**DELIBERATELY LEFT FAILING**.
**`probe_rev36_barend` PRINTS "REFUSING TO PRINT A RULING"** and that is CORRECT.
**Do not "fix" any of these.**
Both flank probes and `probe_rev40_datum` and `probe_rev41_gate` need
`out/p_side.png` (see §10).

## Step 4 — read, in this order

`STATE.md` → `SPEC.md` §10, then §10.9 through §10.99 → this file →
**`HANDOFF_rev41.md`** → `HANDOFF_rev40.md` → … → `REF_MEASUREMENTS.md`.
`STATE.md` is machine-written; **if it and any prose disagree, it is right — BUT
CHECK ITS PROVENANCE ROWS FIRST**, including the `working tree` row. **If that
says DIRTY, the file is not a record of anything.** Rev 38 shipped it DIRTY;
rev 39, 40 and 41 all shipped it CLEAN. **Check it anyway.**

---

# §6. ORDERED WORK LIST FOR REV 42

**HIS EIGHT DEFECT REPORTS ARE STILL THE SPINE. TWO ARE CLOSED (6 and 8, rev 38).
DO NOT RE-OPEN EITHER. REPORT 3 IS *NOT* CLOSED AND *NOT* SOLVED** — it is where
rev 38 left it, as SPEC §10.24. **Rev 41 closed one of its ROUTES** (§10.99.6):
the counter fascia was never independent of the flank ruler.

1. **REPORT 5 — THE DOORS EXTEND LOWER, AROUND THE WHEEL WELL.** `doorback1`'s
   bottom is a straight line **52 mm above the tyre crown**, pinned ~10 mm above
   the front arch lip by `t1_shell.py`'s `DOOR_GAP_S` assert. **MEASURE IT OFF
   `ref_workshop.jpg`, NOT `ref_side.jpg`** — the cab door is OPEN 49° there
   (SPEC 10.97.12). The route is a SCALE-FREE RATIO against the arch, whose
   radius `ARCH_R` is locked; that frame carries no admissible px/m on the door
   plane (§10.62). `_DOOR_TOP_AUTH` (1.8140) and `DOOR_H` (1.013467) are
   AUTHORED and live in **`folk_gen.py`, not `t1_shell.py`** — the rev-41 brief
   implied otherwise; grep before you cite. The door's LOWER boundary has never
   been measured. **This is the only untouched item of his that moves geometry,
   so it owes a hero.**
2. **REPORT 3's REMAINING INDEPENDENT ROUTE, and it is buildable.**
   `t1_detail.py` names it and nobody has built it: **the counter top's INNER
   edge, which lies ON the flank plane and needs NO parallax term at all.**
   Unusable in `ref_side.jpg` (the cream ramps from saturation 0.10 to 0.35 with
   no step) but **a clean step in `ref_rear34.jpg` at y 423, x 700**, needing
   only a local vertical scale. **DO NOT re-derive the fascia off the flank
   ruler — that is what rev 41 refused.** §10.99.6.
3. **REPORT 4 — THE VW GLYPH.** §10.25's premise is FALSE: SPEC's own later entry
   records *"no gap but a 52 mm interpenetration"*. There was never a 12.7 mm air
   gap to preserve, so the V and W still **fuse into an X**. §10.94.
4. **REPORT 7 — "100% CALIDAD" OFF CENTRE.** `cal_gen.py:246` places it at an
   absolute **0.180 of texture width** — verified at that exact line in rev 41.
   **DETERMINE TEXTURE-VERSUS-PANEL BEFORE TOUCHING EITHER** (§10.20's family).
   **DISTINCT from my earlier sticker LEGIBILITY complaint. Do not merge them.**
   §10.95.3.
5. **REPORTS 1 & 5 — `V_POW`.** Locked at **0.60** — it is `t1_mats.py:149` and
   `t1_shell.py:1086`'s `V_POW_Z`, **not** `t1_shell.py:1070` as the rev-41 brief
   said. The rev-11 audit implies **0.30–0.48**. **MIRROR ANY CHANGE INTO
   `t1_shell.zV`** or the pressed swage and the painted break de-register.
6. **`probe_clean_top.py` and `probe_dust_anchor.py` — REWRITE OR RETIRE.**
   **NINE revisions now.** Decide the post-retirement question first. **Do not
   widen a tolerance.**
7. **THE UV-OVERLAP AND TEXTURE-RESOLUTION CHECK HAS NEVER BEEN RUN**, in 41
   revisions, against a standing requirement of his (§7 item 14). It moves no
   geometry and needs no photograph. **Cheapest open item in the project.**
8. **A HERO, after anything that moves geometry.** Camera absolutely last.

**SHOOT THE HERO AT THE END, AND SHOOT IT EVERY REVISION THAT MOVES GEOMETRY.
AND RE-RUN THE PROBES TOO.**

---

## §7. INSTRUCTIONS OF MINE STILL OUTSTANDING, IN NO OTHER CARRIER

Grep each before acting — a memory entry is a claim.

1. ~~**DRIVE FIXES OFF THE BROADSIDE RENDER LAID OVER `ref_side.jpg`**~~ —
   **DONE IN REV 39, DATUM CORRECTED IN REV 40, GATE ADJUDICATED IN REV 41.**
   `probe_rev39_flank.py` is the instrument and it is a standing one.
   **RE-RUN IT EVERY REVISION THAT MOVES THE FLANK — but read §10.99 first: its
   Z-LADDER has no power and only its JOINT registration should be quoted.**
2. **"REMEMBER TO HOLD UP NEXT TO THE ACTUAL SOURCE PHOTOS."** A standing check.
   Rev 39/40/41 did it for the show flank. **Still never done for the NOSE, the
   TAIL or the ROOF.**
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
   `grep -c trunk t1_shell.py build.py` is **0 and 0** — re-verified in rev 41.
9. **"CLUTTER ON THE COUNTER"** — a defect I raised more than once, never
   recorded as closed, and rev 11 then dressed the galley with 51 objects.
10. **I STATED THE BUS SITS NOTICEABLY LOWER THAN STOCK.** **NO REVISION HAS
    MEASURED THIS AND NONE MUST BE READ AS HAVING DONE SO** — every flank number
    is relative to the counter fascia or the break by construction and says
    nothing about ride height. Still unadjudicated.
11. **NOLITA IS RE-ADMITTED FOR GEOMETRY ONLY** (rev 15, §10.32).
    `grep -ic nolita`: **9 in SPEC, 0 in REF_MEASUREMENTS.** Twenty-six
    revisions, **no Nolita frame ever measured.** **AN AUTHORISED SOURCE CLASS IS
    SITTING UNUSED.** Every Nolita-derived number must be TAGGED.
12. **THE GITHUB MIGRATION** I asked to have executed (rev 31c). Still
    unfulfilled; its supposed artefact is a phantom, re-checked in rev 41.
    **Running Claude Code LOCALLY was raised alongside it and never decided.**
13. ~~**REGION 3**~~ — **CLOSED BY ME IN REV 40: THE PALE BAND IS THE COUNTER'S
    FRONT FACE.** It supersedes rev 12's "body's own belt paint" and explains my
    rev-19 non-selection. **DO NOT RE-PUT IT.** §10.98.11. **Note rev 41 did NOT
    disturb this — it refused the DEPTH measurement built on top of it, not the
    identification.**
14. **THE STANDARD, IN MY WORDS:** *"we are recreating a photo realistic version
    of that exact bus"* and *"any single measurement off is unacceptable"*. Also:
    4K non-overlapping textures and no floating artifacts — **no revision has
    ever run a UV-overlap or texture-resolution check.** Verified 0 in rev 41.
    **It is §6 item 7 this time. Please actually do it.**

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
against 102.7 ± 6.6 photographed and REF §3a's own 100.0.
**THE COUNTER SLAB IS RIGHT TO 0.0 mm** (rev 41) — built `CNT_ZT − CNT_ZB`
0.1070 m against REF §6's directly measured 22.65 px = 0.107 ± 0.005 m.
**Do not move `CNT_ZT`, `CNT_ZB` or `CNT_NOSE_F` off a flank-plane reading.**
**THE Z-LADDER IN `probe_rev39_flank.py` HAS NO POWER** (rev 41, §10.99).
**Do not re-tune its gate. Do not quote its bands. Its JOINT registration is
sound and is the only part that may be cited.**

## §9. HARD-WON RULES — every one was learned by breaking it

Every rule in the rev-41 prompt still stands. **NEW in rev 41:**

* **A GATE WITHOUT A NULL IS NOT A GATE.** Any acceptance threshold on a
  correlation statistic must be quoted against that statistic's distribution when
  the correspondence is destroyed. `MIN_PROM = 1.08` sat unexamined for two
  revisions against a null that routinely reaches 2–3.
* **WHEN A VERDICT MOVES WITH THE THRESHOLD, PUBLISH THE SWEEP, NOT THE VERDICT.**
  One bar sweep produced FLAT, NO RULING and NOT FLAT from one dataset.
* **A COMMON-MODE AGREEMENT IS NOT A CROSS-CHECK.** Two readings sharing their
  whole scale chain agreeing to 0.7 mm describes their noise, not their accuracy.
* **A SCOPE ERROR HAS TWO HALVES — THE FEATURE AND THE RULER.** Rev 40 fixed the
  feature, republished, and kept the systematic.
* **AN ABSENCE HAS A TIMESTAMP TOO.** Rev 41 reported a delivery as never made,
  four minutes before it arrived. Say when you looked.
* **STATING A CRITERION BEFORE THE RUN IS WORTH IT EVEN WHEN — ESPECIALLY WHEN —
  THE CRITERION FAILS.** Rev 41's G3 was refuted by its own run, and because it
  was written down first, the refutation is evidence rather than embarrassment.
* **GRADING AN ITEM IS NOT REFUSING IT.** Rev 41 graded item 1 as sound and did
  it, and item 3 as unsound and did not. Two revisions of blanket refusal would
  have been as wrong as two revisions of blanket compliance.

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
with `nohup … &` and poll.** `hero.py` STRIPS IN ROW SPACE — SEAMS ARE
HORIZONTAL.

**The flank probes NEED `out/p_side.png`**, which is gitignored, so **produce it
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

### Restore, twenty-nine lines. The rev14b line is a `fetch`, BEFORE rev15.

```bash
git clone tacombi_history_rev9.bundle tacombi && cd tacombi
git pull --ff-only ../tacombi_rev14_unified.bundle HEAD          # -> 59
git fetch ../tacombi_rev14b_incremental.bundle HEAD:refs/heads/b14   # FETCH
git pull --ff-only ../tacombi_rev15_incremental.bundle HEAD      # -> 67
#   ... rev16 71, rev17 75, rev18 81, rev19 87, rev20 93, rev21 96, rev22 101,
#       rev23 105, rev24 107, rev25 115, rev26 120, rev27 126, rev28 130,
#       rev29 135, rev30 148, rev31 158, rev32 166, rev33 173, rev34 182,
#       rev35 187, rev36 191, rev37 203, rev38 207, rev39 211, rev40 215
git pull --ff-only ../tacombi_rev41_incremental.bundle HEAD      # -> SEE BELOW
```
**If a pull says "Need to specify how to reconcile divergent branches", STOP.**
The hero is gitignored and lives only on my disk.

### Content checks — all read off the fresh clone

```bash
git status                                              # clean
grep -c '^### 10.99' SPEC.md                            # 1
grep -c '^#### 10.99' SPEC.md                           # 7
grep -c 'false-answer rate' SPEC.md                     # 1
grep -c 'A GATE WITHOUT A NULL IS NOT A GATE' SPEC.md   # 1   SINGLE-LINE ANCHOR
grep -c 'COMMON-MODE' SPEC.md                           # 3   CASE MATTERS
grep -c '0.9533' SPEC.md                                # 2
grep -c 'T1_R41_NOG4' SPEC.md                           # 1
grep -c 'T1_R41_NOG4' probe_rev41_gate.py               # 3
grep -c 'def gate' probe_rev41_gate.py                  # 1
grep -c 'NULL_OFFS' probe_rev41_gate.py                 # 6
grep -c 'class Band' probe_rev41_gate.py                # 1
grep -c 'CRITERION 1 IS REFUTED' probe_rev41_gate.py    # 1
grep -c 'AN ABSENCE HAS A TIMESTAMP TOO' HANDOFF_rev41.md   # 1
grep -c 'probe_rev41_gate' HANDOFF_rev41.md             # 1
#   inherited, must still hold:
grep -c '^### 10.98' SPEC.md                            # 1
grep -c '^#### 10.98' SPEC.md                           # 13
grep -c '^### 10.97' SPEC.md                            # 1
grep -c '^### 10.96' SPEC.md                            # 1
grep -c "THE COUNTER'S FRONT FACE" SPEC.md              # 3   NOTE THE QUOTES
grep -c 'CNT_NOSE_F' SPEC.md                            # 6
grep -c 'CLOSED BY HIM' SPEC.md                         # 3   CASE MATTERS
grep -c '_assert_same_edge' flank_compare.py            # 4
grep -c 'cab_floor' SPEC.md                             # 4
grep -c 'T1_ABLATE' build.py                            # 5
grep -c 'FLOOR_W' t1_detail.py                          # 5
grep -c '190' probe_dust_scope.py                       # 4
grep -c 'amtrak' SPEC.md                                # 2   HIS WORD
grep -ic 'nolita' SPEC.md                               # 9
grep -c 'TEN flower heads' SPEC.md                      # 1
ls HANDOFF_rev41.md STATE_rev41.md SPEC_rev41.md NEXT_CONTEXT_PROMPT_rev42.md \
   probe_rev41_gate.py
ls probe_*.py | wc -l    # 30
ls rev38_hero34f.png     # MUST FAIL -- heroes are gitignored
```

Ancestry — **rev 41 adds `69fe7d2`, the rev-40 tip (20 now):**
```bash
for c in f3c53f4 87aeaa6 d519fc6 5087b84 7ce3d03 f3cde44 efc1268 456b201 \
         b08e424 e792d73 6f87977 cac32b9 2253399 52e451a 3496cab b6a93ec \
         54fc45d 4843cc3 668614e 69fe7d2; do
  git merge-base --is-ancestor $c HEAD && echo "$c ok" || echo "$c LOST"; done
```

Textures — **all three must match; rev 41 changed NO artwork:**
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

**NO GEOMETRY MOVED IN REV 39, 40 OR 41.** 42 materials, 5 constant-rough, **0
non-manifold**, rake 17.75, L=4.065 W=1.750, arch gaps 39.7 / 40.7 mm, off flank
804.9 mm — every figure identical to rev 38's.

**No hero this revision, and none is owed** — the mesh has not moved since rev 38
shot `rev38_hero34f.png`. **The moment §6 item 1 lands, one IS owed.**

**Two figures are NOT in the repo this revision** — rev 41 shot no render and
produced no marked crop; its output is `probe_rev41_gate.py` and SPEC 10.99.

**FINAL COUNT: 221 commits, clean tree.** *(This line lands in commit 221 itself
— rev 29's pattern, kept since.)*
