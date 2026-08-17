# NEXT CONTEXT PROMPT — rev 38

Please act as my expert. Continue the Señor Tacombi combi build. **Thirty-seven
revisions sit behind this.** You are picking up mid-stream, not starting.

## Step 0 — CHECK A FOLDER IS CONNECTED BEFORE YOU PLAN ANYTHING

Call `get_device_info`. **In rev 32 through rev 37 `~/Desktop/tacombi_bus_render`
was ALREADY in `connectedFolders` on the first call** — six in a row. It timed
out unanswered in rev 28/29 and was granted on the first request in rev 30/31.
**Do not assume any of those outcomes** — call it, and say plainly what came back.

**THE BRIDGE HAS A THROUGHPUT CEILING, NOT JUST A SIZE ONE.** Only TWO files need
splitting: the 19.5 MB base bundle (7 parts) and the 8.5 MB `rev14_unified`
(3 parts). **Everything rev15–rev37 is under 3 MB and crosses whole.**

**REV 34–37 ALL REUSED REV 33's `_xfer33/` SPLIT PARTS.** They are still on his
disk and their sizes sum **byte-exactly** to both source bundles — check that
before spending `device_bash`. **REV 37 MOVED 33 FILES IN 7 BRIDGE CALLS WITH
ZERO TRANSIENT FAILURES**, one fewer than rev 36. Do not read that as the new
normal: rev 32 had two `upload failed` in one batch and the bridge genuinely
drops. **TRANSIENT FAILURES ARE NOT DROPS. Do not retry in a loop.**

**`device_bash` DOES NOT SEE `/Users/...`** — the mount is
`/sessions/<session-id>/mnt/tacombi_bus_render`. **`device_stage_files` DOES take
the `/Users/...` path. AND YOUR SHELL'S `~` IS `/root`.**

**`hero.py` IS NOT A BLENDER SCRIPT** — it is a plain Python driver. To preview,
drive `build.py`:
```bash
T1_SUB=1 T1_PREVIEW=hero34f T1_FX=0 T1_RX=900 T1_RY=600 T1_SAMP=24 \
  T1_OUT=/tmp/prev T1_PFX=pv blender -b --python build.py
```
**`ref_workshop.jpg`, `ref_side.jpg` and `ref_rear34.jpg` are IN THE REPO.**

## Step 1 — read my memory BEFORE you read any code

`/areas/tacombi-combi-3d.md`, then `-rev14`, `-rev17` … `-rev36`, then
**`/areas/tacombi-combi-3d-rev37.md`** (SEPARATE FILES; each revision's file does
NOT carry the next), then `/areas/tacombi-combi-sticker.md`, then
`/preferences.md`. If you cannot read them, say so explicitly.

**REV 37 PROVED THIS TWICE OVER.** Checking the inherited brief against memory
before opening the code recovered **FOUR of my instructions** that had been lost
from every carrier that crosses contexts — where rev 36 found one. **AND ONE
MEMORY ENTRY WAS A PHANTOM**: memory said the GitHub migration procedure was
written as `MIGRATION_APPENDIX_rev32.md` at commit 159; the file has never
existed in any commit in any ref. **A MEMORY ENTRY IS A CLAIM TOO — GREP IT.**
**CHECK THIS PROMPT AGAINST MEMORY BEFORE TRUSTING ITS WORK LIST.**

**I have never stood in the bus.** The "remember standing in the kombi" bar is
about the RESTAURANT'S owner. **Do not ask me what the real vehicle looks like.**
Ask me what a PHOTOGRAPH shows — that has now paid off twenty-eight times.

## Step 2 — restore, and verify BY CONTENT (never by hash or commit count)

See §1. **TWENTY-FIVE bundle lines now**, and the rev14b line is a `fetch` that
must come BEFORE rev15. rev 20 through rev 37 all restored CLEAN.

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

**THE GUARDS ARE 0 fail / 0 WARN. GEOMETRY MOVED IN REV 37** — the over-rider
assembly was REMOVED. **126 objects, 185 meshes** (rev 30–36 were 127 / 186).
**Every other figure is identical to rev 30–36's.**

**RUN THE PROBES YOU INHERIT, NOT ONLY THE ONES YOU WRITE.** Still **25**
`probe_*.py` — rev 37 wrote none. Under `blender -b --python`:
`probe_ctan_index`, `probe_dust_scope`, `probe_f90`, `probe_rev16`,
**`probe_cross_anatomy` and `probe_shutlines` (transitive)**, and
`probe_rev36_barend`. Everything else under
`/tmp/blender/4.5/python/bin/python3.11` — **including `probe_clean_top` and
`probe_dust_anchor`, whose only `bpy` is in a comment.**

**READ EACH PROBE'S OWN SUMMARY LINE. DO NOT RE-DERIVE IT.** Rev 37's summary
grep **under-read six probes** because it assumed the wording
`CONTROLS: n checked, m FAILED` and `probe_rev36_posts` prints
`ALL 5 CONTROLS PASSED`. Expected: `rev36_barend` **8/0**, `rev36_posts` **5/0**,
`rev35_harmonic` **18/6**, `rev34_levels` **8/4**, `rev34_ruling` **6/4**,
`rev33_barend` **7/4**, `orb_xratio` **6/1**, `rev32_pointer` **10/0**,
`dust_scope` **8/0**, `updust_pointer` **6/0**, `psf_lines` **2 FAILED both
EXPECTED**, `clean_top` and `dust_anchor` **DELIBERATELY LEFT FAILING**.
**Do not "fix" any of these.**

## Step 4 — read, in this order

`STATE.md` → `SPEC.md` §10, then §10.9 through §10.95 → this file →
**`HANDOFF_rev37.md`** → `HANDOFF_rev36.md` → … → `REF_MEASUREMENTS.md`.
`STATE.md` is machine-written; **if it and any prose disagree, it is right — BUT
CHECK ITS PROVENANCE ROWS FIRST**, including the `working tree` row. **If that
says DIRTY, the file is not a record of anything.**

**§§10.91–10.95 ARE REV 37's.** In short: the posts were built and then the whole
over-rider assembly was withdrawn on my decision; four of my instructions were
recovered; a memory entry was a phantom; a `verify.py` substring ban was
mis-scoped; **and I sent EIGHT DEFECT REPORTS off the hero.**

---

# §6. ORDERED WORK LIST FOR REV 38 — MY EIGHT DEFECT REPORTS

**THESE ARE MINE, OFF `rev37_hero34f.png`, AND NOTHING WAS BUILT ON ANY OF THEM.**
Batch 1 verbatim: *"the front nose is shaped inaccurately, it looks more like the
front of an amtrak train than a vw bus, also we need to fix the vw logo, also the
paint job and the headlights are not alligned"*. Batch 2 verbatim: *"the doors
extend lower, around the wheel well, also there seems to be a bar obstructing the
front wheel? also '100% calidad' is off center, and we there are two bars propping
up the art sign on either side, not one"*.

**FIVE OF THE EIGHT CORROBORATE FINDINGS THIS PROJECT ALREADY MEASURED OR CAN
CHECK IN ONE GREP.** Ordered by what each costs to establish:

1. **THE SIGN'S SECOND STRUT — CONFIRMED, BUILD IT FIRST.**
   `t1_shell.signboard()` appends **ONE** `sign_strut`, no loop over sides. I
   report **two, one either side**. A count needs no scale, no px/m and no camera
   model. §10.95.1.

2. **THE DOOR / FRONT-WHEEL BAR — RUN THE ABLATION BEFORE DECIDING ANYTHING.**
   `doorback1` spans x [0.918, 1.824], lower edge **z 0.717**, **52 mm above the
   tyre's crown (0.665)**, across the whole arch; the bar's blunt end in the
   render lands on its rear edge at x 0.918. **THIS IS AN IDENTIFICATION, NOT A
   CONFIRMATION — REV 37's ABLATION WAS ATTEMPTED AND DID NOT RUN** (the harness
   could not resolve the `hero34f` camera, and appending the removal to
   `build.py` executes AFTER the preview render). **Delete `doorback1` /
   `doorback-1`, re-render the crop, and look.** If the bar goes, reports 5 and 6
   are ONE fix. If not, report 6 is a different object and the search restarts.
   `_DOOR_TOP_AUTH` and `DOOR_H` are **AUTHORED, not measured**, and the door's
   LOWER boundary has never been measured — nothing locked stands against me.
   §10.95.2.

3. **THE HEADLAMP / TWO-TONE ALIGNMENT — THE MEASUREMENT ALREADY EXISTS AT
   4.4 σ.** §10.24 item 3: headlamp centre **belt − 0.339 ± 0.025 m**
   photographed against the build's **belt − 0.242**, 97 mm at ~3.9 σ. It was
   parked for want of a second derivation — **and the rev-11 audit supplied two,
   which were never swept back into §10.24**: 83 ± 19 mm at **4.4 σ** by a ratio
   needing no px/m, and a test needing **no scale at all** — *in the photograph
   the indicator aperture lies BELOW the two-tone break; in the build it lies
   ABOVE it.* **THAT IS MY REPORT, IN THE AUDIT'S OWN WORDS.**
   **DO NOT MOVE THE ROUNDEL WITH THE LAMPS** — its height is supported by both
   chains, and §10.24's three findings were applied together once and reverted
   together once. **They are not one change.** **AND MY REPORT IS ABOUT A
   RELATIONSHIP — do not split it into "the paint" and "the headlamps".** §10.94.

4. **THE VW GLYPH.** §10.25 believed it fixed this by coupling glyph to ring. **Its
   premise is FALSE** — SPEC's own later entry records *"no gap but a 52 mm
   interpenetration"*. There was never a 12.7 mm air gap to preserve, so the V and
   W still **fuse into an X**; the rev-10 fix made the glyph smaller, which hid
   the fusion without removing it. Rebuild against the interpenetration. §10.94.

5. **`V_POW`.** Locked at **0.60** (§10.2, `t1_shell.py:1070`). The rev-11 audit
   measured the V-swage arm rising **~2× too fast** — lamp station to body edge
   **0.111 ± 0.015 m photographed against 0.208 built** — implying **0.30–0.48**.
   **MIRROR ANY CHANGE INTO `t1_shell.nose_shape.zV`** or the pressed swage and
   the painted break de-register; §10.2 says they currently register to 0.0 mm.

6. **"100% CALIDAD" OFF CENTRE.** `cal_gen.py:246` places it at an absolute
   **0.180 of texture width**. **DETERMINE TEXTURE-VERSUS-PANEL BEFORE TOUCHING
   EITHER** — §10.20's family, where a lockup looked wrong because the PANEL
   aspect was stale. **DISTINCT from my earlier sticker LEGIBILITY complaint. Do
   not merge them.** §10.95.3.

7. **`probe_clean_top.py` and `probe_dust_anchor.py` — REWRITE OR RETIRE.**
   **FIVE revisions now.** Decide the post-retirement question first. **Do not
   widen a tolerance.**

8. **Camera absolutely last.**

**SHOOT THE HERO AT THE END, AND SHOOT IT EVERY REVISION THAT MOVES GEOMETRY.**
That is rev 37's biggest lesson: `rev30_hero34f.png` was superseded in rev 36 and
never re-shot, so **eight defects sat unseen for seven revisions** and surfaced
the moment one was shot.

---

## §7. THREE INSTRUCTIONS OF MINE STILL OUTSTANDING, IN NO OTHER CARRIER

1. **NOLITA IS RE-ADMITTED FOR GEOMETRY ONLY** (rev 15, §10.32).
   `grep -ic nolita`: **8 in SPEC, 0 in REF_MEASUREMENTS.** Twenty-two revisions,
   **no Nolita frame ever measured** — while `CREAM`, the absolute roof height and
   the off flank's 804.9 mm are all called photograph-blocked. **AN AUTHORISED
   SOURCE CLASS FOR EXACTLY THOSE IS SITTING UNUSED.** Livery, weathering and
   artwork stay locked to my three photographs; every Nolita-derived number must
   be TAGGED so it can be pulled back out.
2. **THE GITHUB MIGRATION** I asked to have executed (rev 31c). Still unfulfilled.
   Its supposed artefact is a phantom (§10.91.2).
3. **REGION 3 — MY ANSWER IS OUTSTANDING.** `rev37_region3.png` asks: *is the pale
   band under the counter's brass nosing the BUS's own painted body, or part of
   the COUNTER?* rev 12 settled it as the body's belt paint; in rev 19 I was shown
   four cream regions and **did not** pick it. **What it closes:** whether
   `countercream` should carry that band, or whether it belongs to `body_paint`'s
   cream and should inherit the flank's weathering, fade and dust. **Shader
   routing, not geometry. Nothing moves until I answer.** §10.92.

## §8. ALREADY SETTLED — do not re-open without new evidence AND a different method

**THE FRONT OVER-RIDER ASSEMBLY IS WITHDRAWN — BAR AND POSTS.** My decision,
rev 37. The front is a plain cream blade plus its two irons. **DO NOT RE-PROPOSE
IT** without a square-on frame of the front or my say-so — **it is ANSWERED, not
open**, and rev 26's "model them" must not be carried as outstanding. `build.py`'s
two calls are **COMMENTED, NOT DELETED**; `overrider_bar()` and
`overrider_posts()` stay defined; §§10.83/10.90/10.91 log **NOT APPLICABLE** and
**stay armed** — proven by two arms, not asserted. Re-enabling is one line.

**This does NOT overturn my rev-26 reading** that the tube is on the bus — that
was a reading of a WORKSHOP photograph and stands as one. It is consistent with
§2.4's own precedent: the rear bumper was removed between the conversion stage
and service, and no in-service frame shows the nose.

Everything else from the rev-37 prompt's settled list stands: REF §9's V-swage
bracket ≈0.40–0.49 m; `422 px/m` consumed nowhere; no recoverable fore-aft VP;
the camera's roll unestablished; **`u 205–208` is a POST, not the bar's far end**;
§10.83's centreline question dissolved because it assumed there was one post
(**SUGGESTIVE, NOT ESTABLISHED — do not promote it**); the near junction is
UNOBSERVED and **zero white alone proves nothing**.

## §9. HARD-WON RULES — every one was learned by breaking it

Every rule in the rev-37 prompt still stands. **NEW in rev 37:**

* **A MEMORY ENTRY IS A CLAIM AND MUST BE GREPPED LIKE ONE.** Memory recovered
  four real instructions and invented one artefact in the same session.
* **A FUNCTION THAT ANSWERS ANYWAY OUTSIDE ITS DOMAIN WILL SUPPLY A DATUM.**
  `_blade_top_at()` fell through two microns past its domain and returned a value
  35 mm low, landing the post on the crown — §10.90's datum error, reproduced.
* **A PENETRATION DEPTH IS NOT A DISTANCE TO AN EXIT SURFACE.** The tell was two
  round numbers: 108.24 mm is `BUMP_PROFILE`'s height, 24.97 mm is `BAR_DIA`.
* **A THRESHOLD CAN CHANGE SIGN UNDERNEATH A TEST AND INVERT IT.** A negative
  weld bound made the guard fire on a floating post. Caught by **reading the
  arm's output**, not by noting it went red — the second time in two revisions.
* **A GUARD YOU WROTE TO FIX A DEFECT CAN CONTAIN THAT DEFECT.** "Footprint
  sampling" selected one vertex because the mesh is sheared. **It was caught only
  because the numbers did not move.**
* **A NAMED EXEMPTION IS A HOLE IN A GUARD — PROVE THE HOLE IS THE SIZE IT
  CLAIMS.** And when a guard fires on something legitimate, **repair its SCOPE,
  never rename the object to dodge it and never delete the coverage.**
* **A WITHDRAWN FEATURE WHOSE GUARD WAS DELETED COMES BACK UNGUARDED.** Keep the
  guard, log NOT APPLICABLE, and **prove it is only dormant** with an arm.
* **DO NOT REPORT A TEST YOU DID NOT GET TO RUN.** rev 37's door ablation is
  labelled an identification, not a confirmation, because it never executed.
* **SHOOT THE HERO EVERY REVISION THAT MOVES GEOMETRY.** Eight defects surfaced
  the moment one was shot after seven revisions without.

## How I work

* Ground in the reference → build → adversarial audit → iterate. Never build
  before grounding. Never call it done off self-review.
* Report the measurement against the reference, **with its ceiling**. Never a
  self-assigned score.
* Do not tell me anything is ready. Tell me what is fixed, what is still wrong,
  and what you measured.
* Keep visible cadence on long work and send renders as they land.
* Travel between contexts consciously, every time.

---

> **THE STANDARD, in the owner's words.** The final product should be nearly
> indistinguishable from the original. **Any single measurement off is
> unacceptable.** The criterion is PER-MEASUREMENT. And above clinical accuracy:
> *"I want the owner to remember standing in the kombi, in this very picture that
> was provided."* — **that owner is the restaurant's owner.**

---

## §10. RESOLUTION

rev 37 shipped **4800×3200 in 20 strips, worst seam z 1.86** (rev 25: 1.91;
threshold 4). Drive `hero.py --only N` one strip per call then `--stitch-only`;
run `post.py` **once** on the stitched frame, never per strip. Middle strips run
**~390–535 s** at this resolution — close to the 10-minute shell cap, so **one
strip per call through the middle**. Edge strips ~70–90 s.
**`hero.py` STRIPS IN ROW SPACE — SEAMS ARE HORIZONTAL.**

## §11. THE COMMIT COUNT AND THE CONTENT FIGURES

Written LAST, after the final commit, from a fresh-clone verification run.
**THIS HAS GONE WRONG IN TWELVE REVISIONS DURING HANDOFF ASSEMBLY.**
**A grep count is invalidated by any later edit to the file it counts.**
**ANCHOR HEADING COUNTS WITH `^`. `grep -c` COUNTS LINES, NOT OCCURRENCES — a
multi-line anchor CANNOT FIRE.**
