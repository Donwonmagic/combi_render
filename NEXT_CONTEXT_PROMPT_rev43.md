# NEXT CONTEXT PROMPT — rev 43
Please act as my expert. Continue the Señor Tacombi combi build. **Forty-two
revisions sit behind this.** You are picking up mid-stream, not starting.
## Step 0 — CHECK A FOLDER IS CONNECTED BEFORE YOU PLAN ANYTHING
Call `get_device_info`. **In rev 32 through rev 42 `~/Desktop/tacombi_bus_render`
was ALREADY in `connectedFolders` on the first call** — eleven in a row. It
timed out unanswered in rev 28/29 and was granted on the first request in
rev 30/31. **Do not assume any of those outcomes** — call it, and say plainly
what came back, WITH ITS TIMESTAMP.
**AN ABSENCE HAS A TIMESTAMP TOO.** Rev 41's first recursive listing ran at
12:04 and found **zero** rev-40 files; it reported rev 40 as having delivered
nothing. **They landed at 12:08.** Rev 42 stated the clock time of every look.
If a delivery looks missing, say *when* you looked and ask before concluding.
**THE BRIDGE DROPPED TWICE IN REV 40** and came back both times on his word;
rev 31/35/36/39's pattern. **Rev 41 and rev 42 saw ZERO drops.**
**WAIT IT OUT AND DO CLOUD-SIDE WORK IN BETWEEN. DO NOT RETRY IN A LOOP.** A
60-second stage timeout with nothing landed is a transient; the next call
returning *"device … is not connected to the bridge"* is the real drop.
**THE BRIDGE HAS A THROUGHPUT CEILING, NOT JUST A SIZE ONE.** Only TWO files need
splitting: the 19.5 MB base bundle (7 parts) and the 8.5 MB `rev14_unified`
(3 parts). **Everything rev15–rev42 is under 3 MB and crosses whole EXCEPT the
hero, which is ~15 MB and crosses whole on its own.**
**REV 34–42 ALL REUSED REV 33's `_xfer33/` SPLIT PARTS.** They are still on his
disk and their sizes sum **byte-exactly** to both source bundles — base parts to
**19,478,840**, r14u parts to **8,519,034**. Check that before spending
`device_bash`. **REV 42 MOVED 36 FILES IN 3 BRIDGE CALLS.**
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
`/areas/tacombi-combi-3d.md`, then `-rev14`, `-rev17` … `-rev41`, then
**`/areas/tacombi-combi-3d-rev42.md`** (SEPARATE FILES; each revision's file does
NOT carry the next), then `/areas/tacombi-combi-sticker.md`, then
`/preferences.md`. If you cannot read them, say so explicitly.
**A MEMORY ENTRY IS A CLAIM TOO — GREP IT.** Rev 37 found memory had invented
`MIGRATION_APPENDIX_rev32.md`, a file that has never existed in any ref; rev 39
through rev 42 all re-checked and it still has not. Rev 41 and rev 42 both
checked the **entire git history across every ref** — 0 paths.
**CHECK THIS PROMPT AGAINST MEMORY BEFORE TRUSTING ITS WORK LIST.**
**REV 40 REFUSED ITS BRIEF'S ITEM 1 AS A DATUM ERROR. REV 41 GRADED ITS ITEM 1 AS
SOUND AND EXECUTED IT, AND REFUSED ITS ITEM 3. REV 42 GRADED ITS ITEMS 1 AND 7
AS SOUND AND DID BOTH, AND CORRECTED ONE WORDING ERROR IN ITS BRIEF.** Grade
every item before you build it — and notice that grading is not the same as
refusing.
**I have never stood in the bus.** The "remember standing in the kombi" bar is
about the RESTAURANT'S owner. **Do not ask me what the real vehicle looks like.**
Ask me what a PHOTOGRAPH shows — that has now paid off thirty-three times, twice
in rev 42 alone.
## Step 2 — restore, and verify BY CONTENT (never by hash or commit count)
See §11. **THIRTY bundle lines now**, and the rev14b line is a `fetch` that
must come BEFORE rev15. rev 20 through rev 42 all restored CLEAN.
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
**THE GUARDS ARE 0 fail / 0 WARN. GEOMETRY MOVED IN REV 42 FOR THE FIRST TIME
SINCE REV 38** — the cab door's lower shut line. **131 objects, 190 meshes, and
every figure is identical to rev 38's EXCEPT the two roof-hole vertex counts,
which are re-baselined at 70069 / 254428.**
**RUN THE PROBES YOU INHERIT, NOT ONLY THE ONES YOU WRITE.** **31 now** — rev 42
added `probe_rev42_uv.py`. Under `blender -b --python`: `probe_ctan_index`,
`probe_dust_scope`, `probe_f90`, `probe_rev16`, **`probe_cross_anatomy` and
`probe_shutlines` (transitive)**, `probe_rev36_barend`, **both rev38 probes, and
`probe_rev42_uv`**. Everything else under
`/tmp/blender/4.5/python/bin/python3.11` — **including `probe_clean_top` and
`probe_dust_anchor`, whose only `bpy` is in a comment, and `probe_rev39_flank`,
`probe_rev40_datum` and `probe_rev41_gate`.**
**`probe_ctan_index` is the slow one (~7 min); it renders. `probe_rev42_uv` is
the OTHER slow one (~9 min); it rasterises every triangle nine times.**
**READ EACH PROBE'S OWN SUMMARY LINE. DO NOT RE-DERIVE IT.** Wordings differ:
`probe_rev36_posts` prints `ALL 5 CONTROLS PASSED`, not `CONTROLS: n checked`.
**A SUMMARY GREP UNDER-READ SIX PROBES IN REV 37 AND AGAIN IN REV 39.**
Expected: **`rev42_uv` 5 checked / 1 FAILED — C3 IS *SUPPOSED* TO FAIL, see
§9**, **`rev41_gate` 5 / 1 — C4 IS *SUPPOSED* TO FAIL**, **`rev40_datum` 4 / 1 —
C3 IS *SUPPOSED* TO FAIL**, `rev39_flank` **3/0**, `rev38_wheelbar` **6/0**,
`rev38_floorpen` **1/0**, `rev36_posts` **5/0**, `rev35_harmonic` **18/6**,
`rev34_levels` **8/4**, `rev34_ruling` **6/4**, `rev33_barend` **7/4**,
`orb_xratio` **6/1**, `rev32_pointer` **10/0**, `dust_scope` **8/0**,
`updust_pointer` **6/0**, `psf_lines` **2 FAILED both EXPECTED**, `clean_top`
and `dust_anchor` **DELIBERATELY LEFT FAILING**.
**`probe_rev36_barend` PRINTS "REFUSING TO PRINT A RULING"** and that is CORRECT.
**`probe_rev39_flank` PRINTS "NOT flat, so the offset-versus-scale question is
NOT settled here" — NOT the phrase "NO RULING".** The rev-42 brief said
otherwise; rev 42 corrected it by reading the probe. **Do not "fix" any of
these.**
Both flank probes and `probe_rev40_datum` and `probe_rev41_gate` need
`out/p_side.png` (see §10).
## Step 4 — read, in this order
`STATE.md` → `SPEC.md` §10, then §10.9 through §10.101 → this file →
**`HANDOFF_rev42.md`** → `HANDOFF_rev41.md` → … → `REF_MEASUREMENTS.md`.
`STATE.md` is machine-written; **if it and any prose disagree, it is right — BUT
CHECK ITS PROVENANCE ROWS FIRST**, including the `working tree` row. **If that
says DIRTY, the file is not a record of anything.** Rev 38 shipped it DIRTY;
rev 39 through rev 42 all shipped it CLEAN. **Check it anyway.**
---
# §6. ORDERED WORK LIST FOR REV 43
**HIS EIGHT DEFECT REPORTS ARE STILL THE SPINE. THREE ARE NOW CLOSED — 6 and 8
in rev 38, and 5 in rev 42. DO NOT RE-OPEN ANY. REPORT 3 IS *NOT* CLOSED AND
*NOT* SOLVED** — it is where rev 38 left it, as SPEC §10.24. Rev 41 closed one
of its ROUTES (§10.99.6).
1. **THE ART FRAME AND THE BODY'S MISSING UV LAYOUT — ONE JOB, AND THEY MUST BE
   DONE TOGETHER.** Rev 42 moved the cab door's bottom **272 mm at the rear
   corner and 388 mm at the front** (SPEC §10.100) and DELIBERATELY left
   `folk_gen`'s art frame at rev 41's `DOOR_H = 1.013467`, because re-pointing
   it forces a texture re-bake and rev 25's rule is one lever at a time.
   Separately, `probe_rev42_uv` measured **55.97 % of painted surface
   self-overlapping**, all of it the BOX projection on `T1_paint` — **the body
   has no UV layout at all** (SPEC §10.101). **BOTH fixes are the same re-bake.**
   Doing either alone burns the bake twice. **This is the largest single piece
   of work left in the project and it needs a plan before a line of code.**
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
   absolute **0.180 of texture width** — re-verified at that exact line in
   rev 42. **DETERMINE TEXTURE-VERSUS-PANEL BEFORE TOUCHING EITHER** (§10.20's
   family). **DISTINCT from my earlier sticker LEGIBILITY complaint. Do not
   merge them.** §10.95.3. Note `calidad.png` is **2400×1771**, below §5's own
   3K floor, and its UV layout is **clean at 0.00 %**.
5. **REPORTS 1 & 5 — `V_POW`.** Locked at **0.60** — it is `t1_mats.py:149` and
   `t1_shell.py:1086`'s `V_POW_Z`, **not** `t1_shell.py:1070`. The rev-11 audit
   implies **0.30–0.48**. **MIRROR ANY CHANGE INTO `t1_shell.zV`** or the pressed
   swage and the painted break de-register. **Report 5's geometry half is now
   CLOSED, but report 1 — the nose shape — is not.**
6. **`probe_clean_top.py` and `probe_dust_anchor.py` — REWRITE OR RETIRE.**
   **TEN revisions now.** Decide the post-retirement question first. **Do not
   widen a tolerance.**
7. **TWO ORPHANS REPORTED IN REV 42 AND NOT TOUCHED:** `lidsign.png` is loaded
   by a material worn by **no object**, and `tex/emblem.png` is referenced by
   **nothing at all**. Cheap, and neither moves geometry.
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
   Rev 42 moved the flank and it still reads **(−1, −4) px**.
2. **"REMEMBER TO HOLD UP NEXT TO THE ACTUAL SOURCE PHOTOS."** A standing check.
   Rev 39/40/41 did it for the show flank; **rev 42 did it for the CAB DOOR off
   `ref_workshop.jpg`. Still never done for the NOSE, the TAIL or the ROOF.**
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
   (214,216,218) against reference per-channel std 16–19. **Rev 42 measured
   `senor.png` at 4096×1738, the ONLY image meeting §5's 3K bar, and its UV
   layout at 0.00 % overlap — so neither resolution nor layout is the problem.**
8. **THE FRONT ROOF LID NEEDS TWO-SIDED ARTWORK** — my settled topology, never
   implemented. `roof_lids()` gives each lid ONE board face. Also mine: **a TRUNK
   LID, separate from the roof lids, and region C is that trunk lid, OPEN.**
   `grep -c trunk t1_shell.py build.py` is **0 and 0** — re-verified in rev 42.
9. **"CLUTTER ON THE COUNTER"** — a defect I raised more than once, never
   recorded as closed, and rev 11 then dressed the galley with 51 objects.
10. **I STATED THE BUS SITS NOTICEABLY LOWER THAN STOCK.** **NO REVISION HAS
    MEASURED THIS AND NONE MUST BE READ AS HAVING DONE SO** — every flank number
    is relative to the counter fascia or the break by construction and says
    nothing about ride height. Still unadjudicated.
11. **NOLITA IS RE-ADMITTED FOR GEOMETRY ONLY** (rev 15, §10.32).
    `grep -ic nolita`: **9 in SPEC, 0 in REF_MEASUREMENTS.** Twenty-seven
    revisions, **no Nolita frame ever measured.** **AN AUTHORISED SOURCE CLASS IS
    SITTING UNUSED.** Every Nolita-derived number must be TAGGED.
12. **THE GITHUB MIGRATION** I asked to have executed (rev 31c). Still
    unfulfilled; its supposed artefact is a phantom, re-checked in rev 42.
    **Running Claude Code LOCALLY was raised alongside it and never decided.**
13. ~~**REGION 3**~~ — **CLOSED BY ME IN REV 40: THE PALE BAND IS THE COUNTER'S
    FRONT FACE.** It supersedes rev 12's "body's own belt paint" and explains my
    rev-19 non-selection. **DO NOT RE-PUT IT.** §10.98.11. **Note rev 41 did NOT
    disturb this — it refused the DEPTH measurement built on top of it.**
14. **THE STANDARD, IN MY WORDS:** *"we are recreating a photo realistic version
    of that exact bus"* and *"any single measurement off is unacceptable"*. Also:
    4K non-overlapping textures and no floating artifacts. ~~**no revision has
    ever run a UV-overlap or texture-resolution check**~~ — **RUN IN REV 42.
    SPEC §10.101. ONE image of seven meets §5's own 3K floor and 55.97 % of the
    painted surface self-overlaps. THE MEASUREMENT EXISTS NOW; THE REPAIR DOES
    NOT.**
## §8. ALREADY SETTLED — do not re-open without new evidence AND a different method
**REPORT 6 IS CLOSED** (`cab_floor`; four wheel houses; both pans `FLOOR_W =
1.200`). **REPORT 8 IS CLOSED** (second `lid_strut`). SPEC 10.96.
**REPORT 5 IS CLOSED FOR ITS GEOMETRY** (rev 42, SPEC 10.100) — the cab door now
wraps the front wheel arch, on HIS two readings of `ref_workshop.jpg`. **Its ART
FRAME is NOT closed and is §6 item 1.**
**THE FRONT OVER-RIDER ASSEMBLY IS WITHDRAWN — BAR AND POSTS.** My decision,
rev 37. **DO NOT RE-PROPOSE IT** without a square-on frame of the front or my
say-so — **it is ANSWERED, not open.** `build.py`'s two calls are **COMMENTED,
NOT DELETED**; the guards stay armed and log NOT APPLICABLE.
**THE MURAL BOARD'S TEN FLOWER HEADS ARE SETTLED BY ME** (rev 39).
**REGION 3 IS SETTLED BY ME** (rev 40) — the counter's front face.
**THE TYRE DIAMETER IS RIGHT** — rev 39 measured 651 ± 13 mm against the locked
665. **Do not re-open it off a visual impression of the overlay.**
**THE MODEL'S BREAK-TO-SILL IS RIGHT TO 2.7 mm** (rev 40).
**THE COUNTER SLAB IS RIGHT TO 0.0 mm** (rev 41). **Do not move `CNT_ZT`,
`CNT_ZB` or `CNT_NOSE_F` off a flank-plane reading.**
**THE Z-LADDER IN `probe_rev39_flank.py` HAS NO POWER** (rev 41, §10.99).
**Do not re-tune its gate. Do not quote its bands. Its JOINT registration is
sound and is the only part that may be cited.**
**THE DOOR OUTLINE'S ARCH CLEARANCE IS ARMED AT REV 41's OWN VALUE** (rev 42,
§10.100.5). It can only be satisfied by being no worse than what shipped. **Do
not re-arm it at a number chosen later.**
## §9. HARD-WON RULES — every one was learned by breaking it
Every rule in the rev-42 prompt still stands. **NEW in rev 42:**
* **AN ORDINAL FACT NEEDS NO RULER, AND THAT IS WHAT MAKES IT ADMISSIBLE WHERE
  A METRIC IS BARRED.** Report 5 sat unbuildable for five revisions because
  §10.62 bars a px/m on the door plane. The finding that broke it was that the
  door's shut line runs BELOW the arch crown and the build put it ABOVE — a
  SIGN, and a sign has no units.
* **A LINE YOU DREW IS NOT EVIDENCE.** My first marked figure produced a "door
  bottom" that, contrast-stretched with no overlay, does not exist: ridge scores
  4–8 against a noise floor of 3.5–5.5. I had read my own annotation back as a
  measurement. Check the unmarked frame.
* **A GUARD FIRING ON YOUR OWN CHANGE IS THE GUARD WORKING.** The arch-clearance
  assert caught my first door outline 1.9 mm too close. Fix the construction.
* **WHEN SMOOTHING MOVES A CURVE, SOLVE FOR THE INPUT THAT PUTS THE OUTPUT WHERE
  YOU WANT IT.** A fixed point, not a hand-tuned offset, so it re-solves itself
  when the resample count changes.
* **A REQUIREMENT NOBODY HAS INSTRUMENTED IS NOT A REQUIREMENT.** §5's
  "non-overlapping" sat in SPEC for thirty-nine revisions with no probe.
* **SWEEP THE PARAMETER YOU ADDED YOURSELF.** `C_FOOT` was mine and it moves the
  answer 8 pp.
* **POOLING TWO OBJECTS THAT SHARE A DECAL MANUFACTURES A DEFECT.** `senor.png`
  reads 100 % pooled and 0.00 % per object.
* **A FRACTION OVER 100 % IS THE CHEAPEST CONTROL THERE IS.** It caught a cache
  key nothing else was watching.
* **C3 CAN FAIL AND THE RULING CAN STILL STAND, IF THE WHOLE SWEEP IS ON ONE
  SIDE OF THE BAR.** State both. Do not let an uncertain figure suppress a
  certain verdict, and do not let a certain verdict launder an uncertain figure.
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
  rev 40 after twenty-one revisions and report 5 in rev 42 after five.**
---
> **THE STANDARD, in the owner's words.** The final product should be nearly
> indistinguishable from the original. **Any single measurement off is
> unacceptable.** The criterion is PER-MEASUREMENT. And above clinical accuracy:
> *"I want the owner to remember standing in the kombi, in this very picture that
> was provided."* — **that owner is the restaurant's owner.**
---
## §10. RESOLUTION AND THE SIDE PROBE
The hero: **4800×3200 in 20 strips**, SUB=2, 56 samples. Drive
`hero.py --only N` one strip per call then `--stitch-only`; run `post.py`
**once** on the stitched frame, never per strip. **TIMINGS RISE MONOTONICALLY
DOWN THE FRAME** — strips 0–2 ~152 s, and the bottom strips run 3–4× that.
**Run the bottom strips with `nohup … &` and poll.** `hero.py` STRIPS IN ROW
SPACE — SEAMS ARE HORIZONTAL.
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
**THIS HAS GONE WRONG IN FIFTEEN REVISIONS DURING HANDOFF ASSEMBLY.**
**A grep count is invalidated by any later edit to the file it counts.**
**ANCHOR HEADING COUNTS WITH `^`. `grep -c` COUNTS LINES, NOT OCCURRENCES.**
**CHECK EVERY ANCHOR'S CASE AND THAT IT DOES NOT WRAP ACROSS A LINE BREAK.**
### Restore, thirty lines. The rev14b line is a `fetch`, BEFORE rev15.
```bash
git clone tacombi_history_rev9.bundle tacombi && cd tacombi
git pull --ff-only ../tacombi_rev14_unified.bundle HEAD          # -> 59
git fetch ../tacombi_rev14b_incremental.bundle HEAD:refs/heads/b14   # FETCH
git pull --ff-only ../tacombi_rev15_incremental.bundle HEAD      # -> 67
#   ... rev16 71, rev17 75, rev18 81, rev19 87, rev20 93, rev21 96, rev22 101,
#       rev23 105, rev24 107, rev25 115, rev26 120, rev27 126, rev28 130,
#       rev29 135, rev30 148, rev31 158, rev32 166, rev33 173, rev34 182,
#       rev35 187, rev36 191, rev37 203, rev38 207, rev39 211, rev40 215,
#       rev41 222
git pull --ff-only ../tacombi_rev42_incremental.bundle HEAD      # -> SEE BELOW
```
**If a pull says "Need to specify how to reconcile divergent branches", STOP.**
The hero is gitignored and lives only on my disk.
### Content checks — all read off the fresh clone
SEE THE TABLE WRITTEN INTO `HANDOFF_rev42.md` §7 AND THE BLOCK BELOW.
