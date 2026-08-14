# NEXT CONTEXT PROMPT — rev 21
Please act as my expert. Continue the Señor Tacombi combi build. **Twenty
revisions sit behind this.** You are picking up mid-stream, not starting.

## Step 1 — read my memory BEFORE you read any code
`/areas/tacombi-combi-3d.md`, then `/areas/tacombi-combi-3d-rev14.md`, then
`/areas/tacombi-combi-3d-rev17.md`, then `/areas/tacombi-combi-3d-rev18.md`,
then **`/areas/tacombi-combi-3d-rev19.md`**, then
**`/areas/tacombi-combi-3d-rev20.md`** (these last two are SEPARATE FILES —
rev 18's file does NOT carry rev 19), then `/areas/tacombi-combi-sticker.md`,
then `/preferences.md`. Five prior contexts skipped them; one cost half a day
and produced the wrong body type. If you cannot read them, say so explicitly
rather than quietly proceeding.

**I have never stood in the bus.** The "remember standing in the kombi" bar is
about the RESTAURANT'S owner, the person this is for. **Do not ask me what the
real vehicle looks like.** Ask me what a PHOTOGRAPH shows — that has now paid
off eleven times — but measure the surface, never ask about it.

## Step 2 — restore, and verify BY CONTENT (never by hash or commit count)
See §1 below. **EIGHT bundle lines now, and the rev14b line is a `fetch`.**
Anything not on my disk does not exist. rev 18 opened with rev 17 missing and
rev 19 opened with rev 18 missing; **rev 20 opened CLEAN** — do not assume
either way, check.

## Step 3 — install Blender 4.5.3 and run BOTH guards before proposing anything
```bash
curl -fsSL -o b.tar.xz https://download.blender.org/release/Blender4.5/blender-4.5.3-linux-x64.tar.xz
tar -xf b.tar.xz && mv blender-4.5.3-linux-x64 /tmp/blender
/tmp/blender/4.5/python/bin/python3.11 -m pip install pillow scipy
```
That pip line is required. Guards are `T1_SUB=n T1_VERIFY=1 blender -b
--python build.py` and `T1_SUB=n blender -b --python audit.py`. Report the
guards' ACTUAL output. Both levels.

## Step 4 — read, in this order
`STATE.md` → `SPEC.md` §10, then §10.9 through §10.56 → this file →
**`HANDOFF_rev20.md`** → `HANDOFF_rev19.md` → `AUDIT_rev18_loft.md` →
`HANDOFF_rev18.md` → `HANDOFF_rev17.md` → `LOFT_GROUND_rev15.md` →
`AUDIT_rev12.md` → `AUDIT_rev11.md` → `REF_MEASUREMENTS.md`.

`STATE.md` is machine-written by `audit.py`. **If it and any prose disagree, it
is right — and as of rev 20 its arch row is no longer a phantom.**

**§10.29 carries two corrections that touch every REF number. §10.45–48 are rev
18's and RETIRE claims in §10.34 and §10.37. §10.49–52 are rev 19's. §10.53–56
are rev 20's and they RETIRE the cream map's chroma target, the "26× too
uniform" framing's replacement, and two of my own hypotheses — read them before
you touch the cream or `COUNTERTAN`.**

## Step 5 — ASK ME WHAT THE PHOTOGRAPHS SHOW before you measure from them
This has now paid off eleven times. **My answers are not infallible — ask me
anyway, then measure what I say.** Show me a crop, mark the regions, give me
options, and **print the crop box**. rev 14's box was 120 px off; rev 16's
detector locked onto brass nosing 30 rows early; rev 17 drew two wrong boxes;
rev 19's first region-4 box straddled the dark roof opening; **rev 20's boxes A
and B caught white napkins rather than the steel they were labelled for, and it
said so when it sent them.**

**A CLASS GATE IS A PROBE TOO, and so is a BRIEF, and so is a TARGET.** Three of
rev 17's four work items came back with their briefs refuted; two of rev 18's
four did; rev 19's single work item came back refuted three ways; **rev 20's
first work item came back with its TARGET refuted, and two of my own
hypotheses died to controls I built for them.**

## Step 6 — the work
§6 below is the ordered list. **The loft is DONE and AUDITED. The arch is FIXED.
The guards are REAL. `STATE.md` has no known phantoms. The cream map is BUILT,
WIRED, MEASURED — and its chroma is NOT short; that target was invalid.**

## Step 7 — resolution
rev 16 shipped 4800×3200 in 20 strips, worst seam z 1.89. Drive
`hero.py --only N` one strip per call then `--stitch-only`; run `post.py`
**once** on the stitched frame, never per strip. Middle strips ~6 min each.
**No hero since rev 16 — the arch fix, rev 17's hubcap rings and rev 19's cream
mottle are all unphotographed. rev 20 held it deliberately: if `CREAM` moves
(§10.55) a hero shot now is stale on arrival.**

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
Tyre OD 0.665 m on 16-inch rims. No rear bumper in service; front bumper cream.
ONE roof opening under the flower-mural lid. The cream "La Santa" panel is a
**DETACHED SIGN** and is **NOT a cream reference**. The counter has a
bare/varnished plywood top with brass nosing. Flank RED sRGB (196,49,36),
**albedo saturation 0.816 LOCKED**. Rake **17.75 mm/m**. Serving bays **EQUAL at
0.5155 m**. `optics-6` CLOSED. `materials-5` CLOSED. Tail lamp **round**.
Windscreen **split, two panes**. Nolita admissible **FOR GEOMETRY ONLY**, every
such number TAGGED. SPEC §6's pure-white backdrop lock **RETIRED**.
Settled rev 16: `RT_ALL 0.0949`, `CR_ALL 0.1179`, **D = 0.2128**; rear overhang
**0.773**; Coons caps at NHALF 57 / NLOOP 112.
Settled rev 17: **`W_ALBEDO` CLOSED for good**; `ref_side.jpg` is the **worst
frame**; hubcap ring **0.093 ± 0.012**; `vw_bars`' air gap **never existed**.
Settled rev 18: the rear arch **holds its crown**, tyre gap **39.7 mm**;
`LOFT_GROUND` §2.3's **`(0.10, 0.014)` is REFUTED**; px/m on `ref_rear34.jpg`'s
**plate plane** is **344.1 ± 6.7**.
Settled rev 19: cream reference **`_BODY = (885,968,292,388)`**, GEOMETRY-ONLY
gate; the cream's flank plane is **337 ± 7 px/m**, a BRACKET, not the plate's.
**NEW, rev 20 and now settled:** the shipped mottle arm is dC\* **0.220/0.227/
0.231** (the 0.240/0.249/0.253 everywhere in rev 19 is the **ABLATION** arm);
**the cream map's chroma is NOT short** — normalised it is already at or above
the photograph; the **BEAUTY arm of `mottle_measure.py` is 100 % clipped** and
has always reported zeros; `STATE.md`'s arch row is **measured**, 39.7 mm.
Never correct this vehicle toward the VW factory catalogue.

## Hard-won rules — every one was learned by breaking it
* Never set a vertical position from the ground line (~70 mm common-mode) — the
  HUB-referenced chain has the same disease at ~29 mm.
* A single linear px→metre scale does not hold along the flank; the map is
  projective. **And a scale measured on one plane is not the scale on another.**
* **An image slope of a fore-aft line is not a rake** — that cost five revisions.
* A rendered ratio is only an albedo ratio between two surfaces of the **same
  class** under the same light.
* A constant tuned against another constant must be expressed in terms of it.
* **A claim in prose is not a guard.** Grep for the node that does it.
* **Check what a guard, a probe, a crop, a CLASS GATE, a BRIEF or a TARGET can
  physically see — including WHICH SURFACE.** Print the crop box.
* **A VERDICT PRINTED AS A CONSTANT STRING IS NOT A MEASUREMENT.**
* **A TARGET IS A PROBE TOO — print the BASE LEVEL of any absolute statistic
  before comparing two frames through it.** rev 20's dC\* target was compared
  across a 5.5× base-chroma mismatch and did not bind. *(NEW)*
* **A RAY-VISIBILITY FLAG IS NOT AN ABLATION.** In Cycles a ray that cannot see
  an object passes THROUGH it and hits what is behind, so the flag substitutes
  the background rather than removing the source. Remove the ALBEDO. *(NEW)*
* **Build the CONTROL first and prove it is a no-op, then run the experiment.**
  Both of rev 20's refuted hypotheses died to controls built before them. *(NEW)*
* **MEASURE THE PSF BEFORE QUOTING ANYTHING NEAR THE LIMIT**, and **sweep the
  threshold rather than picking one**.
* **A negative control turns a number into a measurement — and check the control
  itself.**
* **Before scheduling a solve, ABLATE THE CONSTANT TO ZERO — then check the
  ablation is measuring the right STATISTIC**, and check the estimator's NOISE
  is smaller than the effect. rev 20's per-pixel occlusion test had 21.7 % median
  seed-to-seed noise against the effect it was looking for, and was discarded.
* **CLIPPING DESTROYS TEXTURE.** Print the clipped fraction on both sides.
* **An ORTHO render has an EXACT px/m.** **Verify a projection before measuring
  through it.**
* **A restore check that only greps THIS revision's strings cannot detect a lost
  ANCESTOR** — and **AN ANCESTOR CHECK IS ONLY AS GOOD AS THE NEWEST COMMIT IN
  IT. Both checks must reach the tip.**
* **Do not put a figure in an acceptance test — or a HANDOFF — unless you
  watched it print.**
* **If a change trips a guard, THAT IS THE GUARD WORKING. Never widen it.**
* **A probe that cannot answer must return None, not an endpoint.**
* When a finding breaks something independently locked, measure it a third way.
* **Watch for the lamppost** — `ref_side.jpg` columns 62–79 have produced four
  confident wrong numbers about the front of the vehicle.
* A single shell command is killed at 10 minutes. This box has 2 cores — spawn
  3–4 `Agent`s on **disjoint files**, read-only for audits, rather than a
  Workflow.
* **Backticks in `git commit -m` hit shell substitution.** Use `git commit -F`.
* **The device bridge may drop mid-transfer.** Try the direct call FIRST — rev 20
  moved a 19.5 MB bundle in one call — and fall back to `split` + parallel
  single-file calls + **md5 against my disk** only on failure. `device_bash`
  cannot `rm`.

---
> **THE STANDARD, in the owner's words, and it governs every line below.**
> The final product should be nearly indistinguishable from the original.
> **Any single measurement off is unacceptable.** We are recreating a photo
> realistic version of **that exact bus**. The criterion is PER-MEASUREMENT.
>
> And above clinical accuracy: *"I really want this to give the person the
> opportunity to feel like they were on Playa del Carmen all those years ago.
> I want the owner to remember standing in the kombi, in this very picture
> that was provided."* — **that owner is the restaurant's owner, not me.**
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
git pull --ff-only ../tacombi_rev20_incremental.bundle HEAD      # -> see §2
```
**If a pull says "Need to specify how to reconcile divergent branches", STOP.**

Content checks — **the last one reaches the TIP on purpose**, which is what rev
18's rule demands and what the rev-20 prompt failed to do:
```bash
git status                                             # clean
grep -c '### 10.56' SPEC.md                            # 1   rev 20
grep -c 'A TARGET IS A PROBE TOO' SPEC.md              # 1   rev 20
grep -c 'T1_CTAN_NOBOUNCE' shader_solve.py             # 2   rev 20
grep -c 'MOTTLE_OFS' t1_mats.py                        # 3   rev 20
grep -c 'MEASURED on the mesh' audit.py                # 1   rev 20
grep -c '### 10.52' SPEC.md                            # 1   ANCESTOR rev 19
grep -c '_BODY' cream_rms.py                           # 4   ANCESTOR rev 19
grep -c '_arch_lip_z' verify.py                        # 2   ANCESTOR rev 18
grep -c 'matte_tap' studio.py                          # 6   ANCESTOR rev 17
grep -c '_coons_cap' t1_core.py                        # 3   ANCESTOR rev 16
grep -c 'The threshold is not the parameter' post.py   # 1   ANCESTOR rev 13
ls HANDOFF_rev20.md HANDOFF_rev19.md AUDIT_rev18_loft.md LOFT_GROUND_rev15.md
```
**EVERY FIGURE ABOVE WAS READ OFF A FRESH-CLONE VERIFICATION RUN, not typed
from memory.** See §7.

Ancestry:
```bash
for c in f3c53f4 87aeaa6 d519fc6 5087b84 7ce3d03 f3cde44 efc1268 456b201; do
  git merge-base --is-ancestor $c HEAD && echo "$c ok" || echo "$c LOST"; done
```
**Known limitation, stated rather than hidden:** the ancestry loop's newest
entry is a rev-19 commit, because a hash cannot be written into the file that
contains it without amending, and rev 14 learned not to amend. **The TIP is
covered by the content greps instead** — the rev-20 greps above cannot pass on a
tree missing rev 20. Both halves of rev 18's rule are therefore satisfied, by
different mechanisms.

## 2. Both guards, and the figures I watched print
| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 1 warn** | **0 fail, 1 warn** |
| warn | roof crown @ rear axle **1.983** vs 1.960 (**+23 mm**) | **1.983** |
| **rear arch lip above hub** | **0.3722 → gap 39.7 mm** | same |
| **front arch (control)** | **0.3732 → gap 40.7 mm** | same |
| **rake** | **17.75 mm/m (locked 17.75)** | same |
| dome deficit / rear overhang | +0 / 0.7730 | same |
| dims | L=4.065 W=1.750 | same |
| cut roof hole | **68052v** | **252123v** |
| objects at `materials:` | **126** | **126** |

Also: **185 meshes**; 42 materials; 5 constant-rough; **0 non-manifold**; three
open apertures on +Y; four shut lines 100 % open; band 1.372–1.775; bay widths
**0.516 0.515 0.516**. Every figure identical to rev 18 and rev 19 — rev 20
changes a guard, a generated file and measurement levers, not geometry.
`STATE.md:102` now reads **`| rear arch lip → tyre gap (MEASURED on the mesh) |
39.7 mm — SPEC §2 locks 41 ± 8 |`** with the front control at 40.7 mm.

The commit count is in §7, read off the console after the last commit.

## 3. What rev 20 changed — `HANDOFF_rev20.md` has the full account
`audit.py` (§10.52 repaired — `:156` calls `verify._arch_lip_z`, the `STATE.md`
row parsed from verify's own line), `shader_solve.py` (`T1_CTAN_NOBOUNCE`),
`t1_mats.py` (`MOTTLE_OFS`, `T1_CTAN_DUST`, `T1_CTAN_WEAR`, `T1_CTAN_FADE`),
`mottle_measure.py` (the base-level L\*/C\* print), `SPEC.md` (§10.53–56 +
change log), `HANDOFF_rev20.md`.
**Things you must not silently undo — see `HANDOFF_rev20.md` §4**, and rev 19's
§4 and rev 18's §4 still stand in full.

## 4. Still open
See `HANDOFF_rev20.md` §5 for the full list. The ones that matter:
- **`CREAM`'s albedo — the largest open thing in the model.** Locked at sRGB
  (206,208,200), hue 75.0°, sat **0.038**, **G > R**. The bus's own cream in
  `ref_rear34.jpg` reads (216,200,161), hue 41.7°, sat **0.255**, **R > G** —
  opposite channel order, 6.7× the saturation. §10.55 records three routes to
  separating paint from light and every one's weakness. **NOT CHANGED.**
- **`H_ROOF`** — recommendation put to the owner, answer not received. See
  `HANDOFF_rev20.md` §5.
- **`COUNTERTAN`'s pedestal is ~69 % and UNIDENTIFIED.** Dust, wear, fade,
  coat+spec and interreflection all excluded. **Best lead: the occlusion
  hypothesis** — rev 15 fixed exactly this in `solve_mural` and the fix was never
  applied to `solve_ctan`. Needs a high sample count or an object-index pass.
- **Five shut-line × aperture crossings, one on the show flank.** The
  `t1_shell:391` assert still covers **1 of 4 outlines, 1 of 2 arches, 0 of 5
  apertures**; `CARGO_GAP` samples 5.2 % of its own outline; `gap_cargo_mid`
  never. **Untouched by rev 20.**
- `PLATE_W = 0.3300` has no provenance (rev 18's bound is on `PLATE_OUTER_H`).
- The tail-lamp material slot; `probe_rev16.py`'s `xa` vs `xa`; `folk_gen.py`'s
  four stale constants; SPEC §1713's stale `RAKE_DZDX`; `SCR` +80 mm aft and
  12–24 mm short; `Senor` 0.504 of its 0.782 ceiling; the ~12 unverified image
  URLs never looked at.
- **Parked:** tyre deflection. **Logged not applied:** the bays may be glazed.

## 5. FIRST QUESTION FOR THE OWNER
Two, and the first is new and cheap:
1. **In `ref_rear34.jpg`: are boxes A `(792,838,410,458)` and B
   `(846,876,408,456)` white paper napkins, or something tinted? And is C
   `(986,1024,330,378)`, D `(1030,1074,392,424)` or E `(1096,1180,404,436)` bare
   stainless rather than painted or plastic?** A same-light neutral is what
   separates paint from illumination on the `CREAM` lead. Crops were sent in
   rev 20 with every box printed and zoomed insets.
2. Unchanged: **a head-on rear (or front) elevation from roof height or above,
   with the counter and the lids clear of the section.**

## 6. Ordered work list for rev 21
1. **`CREAM`'s albedo** — the moment the owner answers §5.1. De-illuminate the
   cream against a same-light neutral and compare albedo-to-albedo. **Do not
   change a locked constant without it.**
2. **`H_ROOF`** — implement whichever the owner chose.
3. **`COUNTERTAN`'s occlusion hypothesis** — the mask/measured-render mismatch
   rev 15 fixed in `solve_mural`. Needs an object-index pass or a much higher
   sample count; the 48-sample per-pixel test provably cannot see it.
4. The shut-line × aperture invariant: generalise the `t1_shell` assert to all
   four outlines, both arches and all five apertures, and give `CARGO_GAP`
   samples on its straight runs. **Expect it to FAIL when first armed — five
   crossings are live. That is the guard working; fix the geometry, not the
   threshold.**
5. The tail-lamp material slot; `Senor`'s letterforms; `SCR`'s +80 mm.
6. **A hero at 4800×3200.** Nothing photographed since rev 16. Shoot it AFTER
   item 1 closes, or it is stale on arrival.
7. Camera absolutely last.

## 7. THE COMMIT COUNT AND THE CONTENT FIGURES
This section is written LAST, after the final commit, and every figure in §1 was
read off a fresh-clone verification run rather than typed from memory. **This has
gone wrong in seven consecutive revisions during handoff assembly** — a truncated
console tail, a stale hash, five wrong counts, and a `grep -c` that counted
LINES rather than occurrences. The rule holds: **do not put a figure in an
acceptance test unless you watched it print.**

**Final state: see the console figures reproduced in `HANDOFF_rev20.md` §2. The
restore should land on the count printed there; treat it as a regression catcher
only, and verify by content.**
