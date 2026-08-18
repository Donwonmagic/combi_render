# NEXT CONTEXT PROMPT — rev 39
Please act as my expert. Continue the Señor Tacombi combi build. **Thirty-eight
revisions sit behind this.** You are picking up mid-stream, not starting.

## Step 0 — CHECK A FOLDER IS CONNECTED BEFORE YOU PLAN ANYTHING
Call `get_device_info`. **In rev 32 through rev 38 `~/Desktop/tacombi_bus_render`
was ALREADY in `connectedFolders` on the first call** — seven in a row. It timed
out unanswered in rev 28/29 and was granted on the first request in rev 30/31.
**Do not assume any of those outcomes** — call it, and say plainly what came back.
**THE BRIDGE HAS A THROUGHPUT CEILING, NOT JUST A SIZE ONE.** Only TWO files need
splitting: the 19.5 MB base bundle (7 parts) and the 8.5 MB `rev14_unified`
(3 parts). **Everything rev15–rev38 is under 3 MB and crosses whole.**
**REV 34–38 ALL REUSED REV 33's `_xfer33/` SPLIT PARTS.** They are still on his
disk and their sizes sum **byte-exactly** to both source bundles — base parts to
**19,478,840**, r14u parts to **8,519,034**. Check that before spending
`device_bash`. **REV 38 MOVED 34 FILES IN 7 BRIDGE CALLS WITH ZERO TRANSIENT
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
`/areas/tacombi-combi-3d.md`, then `-rev14`, `-rev17` … `-rev37`, then
**`/areas/tacombi-combi-3d-rev38.md`** (SEPARATE FILES; each revision's file does
NOT carry the next), then `/areas/tacombi-combi-sticker.md`, then
`/preferences.md`. If you cannot read them, say so explicitly.
**REV 37 PROVED THIS AND REV 38 PROVED IT AGAIN, HARDER.** Rev 37 recovered four
lost instructions. **REV 38 RAN TWO PARALLEL MEMORY SWEEPS OVER rev11–35 AND THE
STICKER FILE AND RECOVERED A LARGE SET MORE — see §7.** The sticker file is the
single richest source and NO PROMPT HAS EVER ENUMERATED IT.
**A MEMORY ENTRY IS A CLAIM TOO — GREP IT.** Rev 37 found memory had invented
`MIGRATION_APPENDIX_rev32.md`, a file that has never existed in any ref.
**CHECK THIS PROMPT AGAINST MEMORY BEFORE TRUSTING ITS WORK LIST.**
**REV 38's OWN BRIEF NAMED THE WRONG OBJECT IN ITS ITEM 1** — see §9.
**I have never stood in the bus.** The "remember standing in the kombi" bar is
about the RESTAURANT'S owner. **Do not ask me what the real vehicle looks like.**
Ask me what a PHOTOGRAPH shows — that has now paid off twenty-nine times.

## Step 2 — restore, and verify BY CONTENT (never by hash or commit count)
See §11. **TWENTY-SIX bundle lines now**, and the rev14b line is a `fetch` that
must come BEFORE rev15. rev 20 through rev 38 all restored CLEAN.

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
**THE GUARDS ARE 0 fail / 0 WARN. GEOMETRY MOVED IN REV 38** — four wheel houses
and a second lid strut added, both floor pans narrowed. **131 objects, 190
meshes** (rev 37 was 126 / 185; rev 30–36 were 127 / 186).
**Every other figure is identical to rev 30–38's.**
**RUN THE PROBES YOU INHERIT, NOT ONLY THE ONES YOU WRITE.** **27 now** — rev 38
added `probe_rev38_wheelbar.py` and `probe_rev38_floorpen.py`. Under
`blender -b --python`: `probe_ctan_index`, `probe_dust_scope`, `probe_f90`,
`probe_rev16`, **`probe_cross_anatomy` and `probe_shutlines` (transitive)**,
`probe_rev36_barend`, **and both rev38 probes**. Everything else under
`/tmp/blender/4.5/python/bin/python3.11` — **including `probe_clean_top` and
`probe_dust_anchor`, whose only `bpy` is in a comment.**
**READ EACH PROBE'S OWN SUMMARY LINE. DO NOT RE-DERIVE IT.** Wordings differ:
`probe_rev36_posts` prints `ALL 5 CONTROLS PASSED`, not `CONTROLS: n checked`.
Expected: `rev38_wheelbar` **6/0**, `rev38_floorpen` **1/0**, `rev36_posts`
**5/0**, `rev35_harmonic` **18/6**, `rev34_levels` **8/4**, `rev34_ruling`
**6/4**, `rev33_barend` **7/4**, `orb_xratio` **6/1**, `rev32_pointer` **10/0**,
`dust_scope` **8/0** (its literal is now **190**), `updust_pointer` **6/0**,
`psf_lines` **2 FAILED both EXPECTED**, `clean_top` and `dust_anchor`
**DELIBERATELY LEFT FAILING**. **`probe_rev36_barend` PRINTS "REFUSING TO PRINT
A RULING — a positive control is down"** and that is CORRECT: `orb_bar` was
withdrawn in rev 37, so it cannot rule. **Do not "fix" any of these.**

## Step 4 — read, in this order
`STATE.md` → `SPEC.md` §10, then §10.9 through §10.96 → this file →
**`HANDOFF_rev38.md`** → `HANDOFF_rev37.md` → … → `REF_MEASUREMENTS.md`.
`STATE.md` is machine-written; **if it and any prose disagree, it is right — BUT
CHECK ITS PROVENANCE ROWS FIRST**, including the `working tree` row. **If that
says DIRTY, the file is not a record of anything.** In rev 38 its `git commit`
row was commit 201 against a HEAD of 203 — **the documented parent-provenance
pattern, verified by diffing 201..203 and finding only doc files.** Do that diff.

---
# §6. ORDERED WORK LIST FOR REV 39
**HIS EIGHT DEFECT REPORTS ARE STILL THE SPINE. TWO ARE NOW CLOSED.**
Batch 1 verbatim: *"the front nose is shaped inaccurately, it looks more like the
front of an amtrak train than a vw bus, also we need to fix the vw logo, also the
paint job and the headlights are not alligned"*. Batch 2 verbatim: *"the doors
extend lower, around the wheel well, also there seems to be a bar obstructing the
front wheel? also '100% calidad' is off center, and we there are two bars propping
up the art sign on either side, not one"*.

**CLOSED IN REV 38:** report 6 (the bar) and report 8 (the second strut).
**DO NOT RE-OPEN EITHER.** See §8.

1. **REPORT 5 — THE DOORS EXTEND LOWER, AROUND THE WHEEL WELL.**
   **THIS IS NOT THE SAME FIX AS REPORT 6** — rev 38's ablation refuted the
   shared cause, so treat them as independent. `doorback1` spans x [0.918,
   1.824], z **0.717 → 1.755**; its bottom is a STRAIGHT line **52 mm above the
   tyre crown (0.665)**, not following the arch. `_DOOR_TOP_AUTH` (1.8140) and
   `DOOR_H` (1.013467) are **AUTHORED, not measured**, and the door's LOWER
   boundary has never been measured. **Nothing locked stands against me.**
   The real T1 cab door's lower front corner is cut away for the arch — measure
   that off `ref_side.jpg` if the man's red shirt does not occlude it (§10.7
   records that every front-arch attempt has locked onto his shirt). SPEC 10.96.8.
2. **REPORT 3 — THE HEADLAMP / TWO-TONE ALIGNMENT. THE MEASUREMENT ALREADY
   EXISTS AT 4.4 σ.** §10.24 item 3: headlamp centre **belt − 0.339 ± 0.025 m**
   photographed against the build's **belt − 0.242**, 97 mm at ~3.9 σ. Parked
   for want of a second derivation — **and the rev-11 audit supplied two, never
   swept back into §10.24**: 83 ± 19 mm at **4.4 σ** by a ratio needing no px/m,
   and a test needing **no scale at all** — *in the photograph the indicator
   aperture lies BELOW the two-tone break; in the build it lies ABOVE it.*
   **THAT IS MY REPORT, IN THE AUDIT'S OWN WORDS.**
   **DO NOT MOVE THE ROUNDEL WITH THE LAMPS** — its height is supported by both
   chains, and §10.24's three findings were applied together once and reverted
   together once. **They are not one change.** **AND MY REPORT IS ABOUT A
   RELATIONSHIP — do not split it into "the paint" and "the headlamps".** §10.94.
3. **REPORT 4 — THE VW GLYPH.** §10.25 believed it fixed this by coupling glyph
   to ring. **Its premise is FALSE** — SPEC's own later entry records *"no gap
   but a 52 mm interpenetration"*. There was never a 12.7 mm air gap to
   preserve, so the V and W still **fuse into an X**; the rev-10 fix made the
   glyph smaller, which hid the fusion without removing it. Rebuild against the
   interpenetration. §10.94.
4. **REPORTS 1 & 5 — `V_POW`.** Locked at **0.60** (§10.2, `t1_shell.py:1070`).
   The rev-11 audit measured the V-swage arm rising **~2× too fast** — lamp
   station to body edge **0.111 ± 0.015 m photographed against 0.208 built** —
   implying **0.30–0.48**. **MIRROR ANY CHANGE INTO `t1_shell.nose_shape.zV`**
   or the pressed swage and the painted break de-register; §10.2 says they
   currently register to 0.0 mm.
5. **REPORT 7 — "100% CALIDAD" OFF CENTRE.** `cal_gen.py:246` places it at an
   absolute **0.180 of texture width**. **DETERMINE TEXTURE-VERSUS-PANEL BEFORE
   TOUCHING EITHER** — §10.20's family, where a lockup looked wrong because the
   PANEL aspect was stale. **DISTINCT from my earlier sticker LEGIBILITY
   complaint. Do not merge them.** §10.95.3.
6. **`probe_clean_top.py` and `probe_dust_anchor.py` — REWRITE OR RETIRE.**
   **SIX revisions now.** Decide the post-retirement question first. **Do not
   widen a tolerance.**
7. **Camera absolutely last.**
**SHOOT THE HERO AT THE END, AND SHOOT IT EVERY REVISION THAT MOVES GEOMETRY.**
**AND RE-RUN THE PROBES TOO — that is rev 38's addition to the rule, see §9.**

---
## §7. INSTRUCTIONS OF MINE STILL OUTSTANDING, IN NO OTHER CARRIER
Rev 38's memory sweep recovered these. **EVERY ONE IS MINE AND NONE IS IN ANY
PROMPT BEFORE THIS.** Grep each before acting — a memory entry is a claim.
1. **DRIVE FIXES OFF THE BROADSIDE RENDER LAID OVER `ref_side.jpg` AT MATCHED
   SCALE.** My stated method for the model work — that flank carries the script,
   folk art, counter, Calidad decal, belt line, stance and arches. `flank_compare.py`
   exists and was recorded NOT RUN in rev 10 and never mentioned since.
   **This is the instruction that would have caught most of my eight reports
   before I had to make them.**
2. **"REMEMBER TO HOLD UP NEXT TO THE ACTUAL SOURCE PHOTOS."** A standing check,
   restated by me. No whole-vehicle render-vs-photograph comparison since rev 16.
3. **THE DIE-CUT VINYL STICKER IS THE ORIGINAL DELIVERABLE AND IS UNBUILT.**
   For children at the restaurant; should spark joy and be something families
   keep. **Style LOCKED by me: cartoon with rendered depth** — vector line and
   flat colour, shading and occlusion sampled from the 3D asset. **Scene LOCKED
   by me: nothing but the bus, die-cut tight, plus the sun and the papel
   picado.** **CONFLICT NEEDING ME, NOT A MEASUREMENT:** rev 10 established
   *"there is no papel picado in that photograph"*. I also said I like how the
   wheels were drawn in the earlier cartoon version.
4. **THE PLAYA HERO IS DEPRIORITISED, NOT CANCELLED** — *"let's not do playa
   right now. Lets focus on the 3d model"*. The agreed deliverable is the
   white-studio hero for fidelity **PLUS** a warm low-light Playa hero for the
   memory, and **the Playa one carries the emotional bar that sits ABOVE clinical
   accuracy**. Its rig exists; its exposure was recorded NOT converged in rev 10.
5. **NINE FLOWER HEADS ON THE MURAL BOARD — I COUNTED THEM OFF THE PHOTOGRAPH
   MYSELF.** Rev 11 re-measured PETALS (eight, not twelve) and speaks of "6 of 7
   clean heads". **Nothing has ever checked the model's HEAD COUNT against my
   nine.** A count, and counts are the cheapest thing to check.
6. **ABSOLUTE REPLICATION OF ALL ARTWORK** — mural board, flank paisley, the
   script, the Calidad decal, **the menu strips and cards, the rear-lid
   lettering, the plate surround**. A hard bar, not a preference. Rev 10 recorded
   that the lettered panel reads *"La S——— and no further"* and that
   **"La Santa" is a RECONSTRUCTION, not a reading, carried as fact**.
7. **THE SEÑOR TACOMBI SCRIPT — I REJECTED IT TWICE.** *"That script i see on
   the p9 hero is NOT it."* and *"deserves a more finely tuned recreation pass"*.
   Rev 10 raised lockup IoU to 0.942 but recorded the test is **NOT independent**
   (glyphs are swept along the medial axis of the same mask it scores against).
   Also open: **the silver is FLAT** — `tex/senor.png` emits a constant
   (214,216,218) against reference per-channel std 16–19.
8. **THE FRONT ROOF LID NEEDS TWO-SIDED ARTWORK** — my settled topology, never
   implemented. `roof_lids()` gives each lid ONE board face. Also mine: **a
   TRUNK LID, separate from the roof lids, and region C is that trunk lid, OPEN.**
9. **"CLUTTER ON THE COUNTER"** — a defect I raised more than once, never
   recorded as closed, and rev 11 then dressed the galley with 51 objects.
10. **I STATED THE BUS SITS NOTICEABLY LOWER THAN STOCK**; the street-level photo
    reads close to stock. Unadjudicated — the shape of conflict you resolve by
    asking me.
11. **NOLITA IS RE-ADMITTED FOR GEOMETRY ONLY** (rev 15, §10.32).
    `grep -ic nolita`: **8 in SPEC, 0 in REF_MEASUREMENTS.** Twenty-three
    revisions, **no Nolita frame ever measured** — while `CREAM`, the absolute
    roof height and the off flank's 804.9 mm are all called photograph-blocked.
    **AN AUTHORISED SOURCE CLASS IS SITTING UNUSED.** Every Nolita-derived number
    must be TAGGED so it can be pulled back out.
12. **THE GITHUB MIGRATION** I asked to have executed (rev 31c). Still
    unfulfilled; its supposed artefact is a phantom (§10.91.2). **Running Claude
    Code LOCALLY was raised alongside it and never decided.**
13. **REGION 3 — MY ANSWER IS OUTSTANDING.** `rev37_region3.png` asks: *is the
    pale band under the counter's brass nosing the BUS's own painted body, or
    part of the COUNTER?* rev 12 settled it as the body's belt paint; in rev 19 I
    was shown four cream regions and **did not** pick it. **What it closes:**
    whether `countercream` should carry that band, or whether it belongs to
    `body_paint`'s cream and should inherit the flank's weathering, fade and
    dust. **Shader routing, not geometry. Nothing moves until I answer.** §10.92.
14. **THE STANDARD, IN MY WORDS:** *"we are recreating a photo realistic version
    of that exact bus"* and *"any single measurement off is unacceptable"*, and
    I want an earlier render of my own **recovered in its entirety and improved
    from there**. Also: 4K non-overlapping textures and no floating artifacts —
    **no revision has ever run a UV-overlap or texture-resolution check.**

## §8. ALREADY SETTLED — do not re-open without new evidence AND a different method
**REPORT 6 IS CLOSED.** The bar across the front wheel was **`cab_floor`**, seen
through an arch with nothing behind it. Established by ABLATION (the brief's
`doorback1` candidate refuted: 612 px of 1.7 M changed, none of them the bar)
and by RAY-CAST identification (308 rays, first hit). Four wheel houses built,
both floor pans narrowed to `FLOOR_W = 1.200`. **0 interior rays and 0
floor↔wheel face pairs, from 308 and 1156.** SPEC 10.96.
**REPORT 8 IS CLOSED.** Second `lid_strut` built in `roof_lids()`.
**THE FRONT OVER-RIDER ASSEMBLY IS WITHDRAWN — BAR AND POSTS.** My decision,
rev 37. The front is a plain cream blade plus its two irons. **DO NOT RE-PROPOSE
IT** without a square-on frame of the front or my say-so — **it is ANSWERED, not
open**, and rev 26's "model them" must not be carried as outstanding. `build.py`'s
two calls are **COMMENTED, NOT DELETED**; `overrider_bar()` and
`overrider_posts()` stay defined; §§10.83/10.90/10.91 log **NOT APPLICABLE** and
**stay armed**. Re-enabling is one line.
**This does NOT overturn my rev-26 reading** that the tube is on the bus — that
was a reading of a WORKSHOP photograph and stands as one.
Everything else from the rev-38 prompt's settled list stands: REF §9's V-swage
bracket ≈0.40–0.49 m; `422 px/m` consumed nowhere; no recoverable fore-aft VP;
the camera's roll unestablished; **`u 205–208` is a POST, not the bar's far end**;
§10.83's centreline question dissolved because it assumed there was one post
(**SUGGESTIVE, NOT ESTABLISHED**); the near junction is UNOBSERVED and **zero
white alone proves nothing**.

## §9. HARD-WON RULES — every one was learned by breaking it
Every rule in the rev-38 prompt still stands. **NEW in rev 38:**
* **A GUARD TESTS THE PROPERTY YOU THOUGHT TO NAME. ONLY THE RENDER TESTS THE
  PROPERTY YOU DID NOT.** rev 38's first wheel house was a full 360° revolve:
  **0 fail, 0 warn, 0 non-manifold, 0 interior rays, all six probe controls
  PASS** — and the render showed a dark skirt hanging in mid-air below the sill.
  The second had a fixed outboard y and stood up to **90 mm** proud of the skin;
  the guards passed again. **CAUGHT TWICE, BY LOOKING, INSIDE ONE REVISION.**
* **A REVISION THAT MOVES GEOMETRY MUST RE-RUN THE PROBES, NOT ONLY RE-SHOOT THE
  HERO.** rev 37 wrote the hero half and not the probe half, and shipped two
  stale probe figures in its own brief. `probe_dust_scope`'s mesh-count literal
  has now drifted **twice, in both directions** — rev 30 (185→186), rev 37
  (186→185), each unswept, over a comment reading *"A CONTROL NOBODY RUNS IS NOT
  A CONTROL."*
* **A CONTROL THAT FAILS IS A RESULT, NOT A BROKEN INSTRUMENT.** `van_floor` was
  written as the CONTROL for the cab-floor claim and it FAILED — which is the
  only reason anyone learned the defect was systemic and all four wheels were
  penetrated.
* **AN ABLATION THAT REMOVES NOTHING RENDERS AN IDENTICAL FRAME, AND "IDENTICAL"
  READS AS A FINDING.** `T1_ABLATE` RAISES on a name that matches nothing.
* **A TEST APPENDED AFTER THE RENDER IS NOT A TEST.** rev 37's ablation removed
  an object from a scene nobody looked at. The hook must be UPSTREAM.
* **A PROBE THAT ASSERTS A FACT ITS SUBJECT HAS MOVED PAST IS A DEFECT.** Sweep
  your own probes' prose in the same revision that invalidates it.
* **REPAIR A CONTROL'S SCOPE; NEVER RE-AIM THE RAY UNTIL IT HITS THE NAME YOU
  FIRST WROTE DOWN.** And **assert that a control's window lands where you think
  it does** — rev 38's "rear arch" window was on the NOSE.
* **A DETECTOR OUTSIDE ITS DOMAIN PRINTS A CONFIDENT, WELL-FORMATTED, FICTIONAL
  RESULT.** rev 38's first probe draft ran against Blender's DEFAULT STARTUP CUBE.
* **THE BRIEF CAN NAME A FUNCTION THAT NEVER RUNS.** §6 item 1 of the rev-38
  prompt called the second strut "CONFIRMED, BUILD IT FIRST" and attributed it
  to `signboard()`, which is gated behind `T1_SIGNBOARD=1` and appears in no
  shipped frame. **The report was right; the attribution was not.**

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
## §10. RESOLUTION
rev 38 shipped **4800×3200 in 20 strips**, SUB=2, 56 samples. Drive
`hero.py --only N` one strip per call then `--stitch-only`; run `post.py`
**once** on the stitched frame, never per strip.
**TIMINGS MEASURED IN REV 38, AND THEY RISE MONOTONICALLY DOWN THE FRAME:**
strips 0–2 ~145–157 s, strip 5 ~314 s, strip 8 ~420 s, strip 11 ~477 s,
strip 15 ~548 s. **THE LAST FEW STRIPS EXCEED THE 10-MINUTE SHELL CAP** —
strip 16 was killed at 580 s. **Run the bottom strips with `nohup ... &` and
poll**, or they will be truncated. Edge strips at the TOP are the fast ones.
**`hero.py` STRIPS IN ROW SPACE — SEAMS ARE HORIZONTAL.**

## §11. THE COMMIT COUNT AND THE CONTENT FIGURES
Written LAST, after the final commit. **EVERY VALUE BELOW WAS READ OFF A
FRESH-CLONE VERIFICATION RUN — none was typed from memory.**
**THIS HAS GONE WRONG IN THIRTEEN REVISIONS DURING HANDOFF ASSEMBLY.**
**A grep count is invalidated by any later edit to the file it counts.**
**ANCHOR HEADING COUNTS WITH `^`. `grep -c` COUNTS LINES, NOT OCCURRENCES — a
multi-line anchor CANNOT FIRE.**
### Restore, twenty-six lines. The rev14b line is a `fetch`, BEFORE rev15.
```bash
git clone tacombi_history_rev9.bundle tacombi && cd tacombi
git pull --ff-only ../tacombi_rev14_unified.bundle HEAD          # -> 59
git fetch ../tacombi_rev14b_incremental.bundle HEAD:refs/heads/b14   # FETCH
git pull --ff-only ../tacombi_rev15_incremental.bundle HEAD      # -> 67
#   ... rev16 71, rev17 75, rev18 81, rev19 87, rev20 93, rev21 96, rev22 101,
#       rev23 105, rev24 107, rev25 115, rev26 120, rev27 126, rev28 130,
#       rev29 135, rev30 148, rev31 158, rev32 166, rev33 173, rev34 182,
#       rev35 187, rev36 191, rev37 203
git pull --ff-only ../tacombi_rev38_incremental.bundle HEAD      # -> SEE BELOW
```
**If a pull says "Need to specify how to reconcile divergent branches", STOP.**
The hero is gitignored and lives only on my disk.
