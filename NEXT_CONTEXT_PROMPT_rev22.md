# NEXT CONTEXT PROMPT — rev 22
Please act as my expert. Continue the Señor Tacombi combi build. **Twenty-one
revisions sit behind this.** You are picking up mid-stream, not starting.
## Step 1 — read my memory BEFORE you read any code
`/areas/tacombi-combi-3d.md`, then `-rev14`, `-rev17`, `-rev18`, `-rev19`,
`-rev20`, then **`/areas/tacombi-combi-3d-rev21.md`** (these are SEPARATE FILES;
each revision's file does NOT carry the next), then
`/areas/tacombi-combi-sticker.md`, then `/preferences.md`. Five prior contexts
skipped them; one cost half a day and produced the wrong body type. If you
cannot read them, say so explicitly rather than quietly proceeding.
**I have never stood in the bus.** The "remember standing in the kombi" bar is
about the RESTAURANT'S owner, the person this is for. **Do not ask me what the
real vehicle looks like.** Ask me what a PHOTOGRAPH shows — that has now paid
off twelve times — but measure the surface, never ask about it.
## Step 2 — restore, and verify BY CONTENT (never by hash or commit count)
See §1 below. **NINE bundle lines now, and the rev14b line is a `fetch`.**
rev 18 opened with rev 17 missing and rev 19 with rev 18 missing; **rev 20 and
rev 21 both opened CLEAN** — do not assume either way, check.
## Step 3 — install Blender 4.5.3 and run BOTH guards before proposing anything
```bash
curl -fsSL -o b.tar.xz https://download.blender.org/release/Blender4.5/blender-4.5.3-linux-x64.tar.xz
tar -xf b.tar.xz && mv blender-4.5.3-linux-x64 /tmp/blender
/tmp/blender/4.5/python/bin/python3.11 -m pip install pillow scipy
```
That pip line is required. Guards are `T1_SUB=n T1_VERIFY=1 blender -b
--python build.py` and `T1_SUB=n blender -b --python audit.py`. Report the
guards' ACTUAL output. Both levels. **`audit.py` rewrites `STATE.md` every run
but only its provenance rows — `git checkout STATE.md` after.**
## Step 4 — read, in this order
`STATE.md` → `SPEC.md` §10, then §10.9 through §10.58 → this file →
**`HANDOFF_rev21.md`** → `HANDOFF_rev20.md` → `HANDOFF_rev19.md` →
`AUDIT_rev18_loft.md` → `HANDOFF_rev18.md` → `HANDOFF_rev17.md` →
`LOFT_GROUND_rev15.md` → `AUDIT_rev12.md` → `AUDIT_rev11.md` →
`REF_MEASUREMENTS.md`.
`STATE.md` is machine-written by `audit.py`. **If it and any prose disagree, it
is right.** It has no known phantoms.
**§10.29 carries two corrections that touch every REF number. §10.45–48 RETIRE
claims in §10.34 and §10.37. §10.53–56 are rev 20's. §10.57–58 are rev 21's and
§10.57 RETIRES rev 20's own account of boxes A and B — read it before you touch
`CREAM` or draw a crop.**
## Step 5 — ASK ME WHAT THE PHOTOGRAPHS SHOW before you measure from them
This has now paid off twelve times. **My answers are not infallible — ask me
anyway, then measure what I say.** Show me a crop, mark the regions, give me
options, and **print the crop box**. rev 14's box was 120 px off; rev 16's
detector locked onto brass nosing; rev 17 drew two wrong boxes; rev 19's first
region-4 box straddled the dark roof opening; rev 20's A and B straddled TWO
MATERIALS; **rev 21's redrawn N1 STILL straddled two materials and I caught it.**
**A CLASS GATE IS A PROBE TOO, and so is a BRIEF, a TARGET, and a SUBAGENT'S
FINDING.** Three of rev 17's four work items came back with their briefs
refuted; two of rev 18's four did; rev 19's single item came back refuted three
ways; rev 20's first item came back with its TARGET refuted; **rev 21 refuted
all FIVE routes to its own headline, and half of a subagent's finding.**
## Step 6 — the work
§6 below is the ordered list. **The loft is DONE and AUDITED. The arch is FIXED.
The guards are REAL. `STATE.md` has no known phantoms. The cream map is BUILT,
WIRED and MEASURED. `CREAM` is UNCHANGED and rev 21 explains why in §10.57.**
## Step 7 — resolution
rev 16 shipped 4800×3200 in 20 strips, worst seam z 1.89. Drive
`hero.py --only N` one strip per call then `--stitch-only`; run `post.py`
**once** on the stitched frame, never per strip. Middle strips ~6 min each.
**NO HERO SINCE REV 16** — the arch fix, rev 17's hubcap rings and rev 19's
cream mottle are all unphotographed. rev 20 held it in case `CREAM` moved.
**`CREAM` did not move and is not going to move without a new photograph, so
the hero is UNBLOCKED. It is item 1.**
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
`W_ALBEDO` **CLOSED for good**. `ref_side.jpg` is the **worst frame**. Hubcap
ring **0.093 ± 0.012**. `vw_bars`' air gap **never existed**. The rear arch
**holds its crown**, tyre gap **39.7 mm**; `LOFT_GROUND` §2.3's **`(0.10, 0.014)`
is REFUTED**. px/m on `ref_rear34.jpg`'s **plate plane** is **344.1 ± 6.7**;
the cream's flank plane is **337 ± 7**, a BRACKET. The shipped mottle arm is
dC\* **0.220/0.227/0.231**; **the cream map's chroma is NOT short**; the BEAUTY
arm of `mottle_measure.py` is **100 % clipped**.
**NEW, rev 21 and now settled:** N2 `(816,836,422,450)` and N3
`(868,890,426,452)` are **white paper napkins**, N3 is **0.00 % clipped**;
**N1 `(784,798,420,448)` STRADDLES two materials — do not use it**; M1
`(844,860,418,452)` is **bare/brushed stainless**; rev 20's **C/D/E are inside
the galley** at 0.22–0.32× the cream's luminance and are **not neutrals**;
`ref_rear34`'s red is **+31 sd** from the locked albedo on §10.12's
neutral-additive invariant, so **no neutral transform relates that frame to the
locked constants**; **`CREAM` UNCHANGED at (206,208,200)**.
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
  before comparing two frames through it.**
* **A RAY-VISIBILITY FLAG IS NOT AN ABLATION.** Remove the ALBEDO.
* **Build the CONTROL first and prove it is a no-op, then run the experiment.**
* **AN ILLUMINANT REFERENCE MUST CARRY SUBSTANTIAL ALBEDO IN ALL THREE
  CHANNELS.** Dividing by a near-zero channel amplifies the additive without
  bound — that is what killed rev 21's route D. *(NEW)*
* **BEFORE DE-ILLUMINATING ANYTHING, TEST WHETHER A NEUTRAL TRANSFORM CAN RELATE
  THE TWO FRAMES AT ALL.** §10.12's (G−B)/(R−B) ratio does it in one line and
  would have saved four of rev 21's five routes. *(NEW)*
* **A SUBAGENT'S FINDING IS A CLAIM, NOT A MEASUREMENT.** Test it before you
  report it. *(NEW)*
* **MEASURE THE PSF BEFORE QUOTING ANYTHING NEAR THE LIMIT**, and **sweep the
  threshold rather than picking one**.
* **A negative control turns a number into a measurement — and check the control
  itself.**
* **Before scheduling a solve, ABLATE THE CONSTANT TO ZERO — then check the
  ablation is measuring the right STATISTIC**, and check the estimator's NOISE
  is smaller than the effect.
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
* **The device bridge may drop mid-transfer.** Try the direct call FIRST — rev 21
  moved NINE bundles (~28 MB) in ONE call — and fall back to `split` + parallel
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
git pull --ff-only ../tacombi_rev20_incremental.bundle HEAD      # -> 93
git pull --ff-only ../tacombi_rev21_incremental.bundle HEAD      # -> see §7
```
**If a pull says "Need to specify how to reconcile divergent branches", STOP.**
Content checks — **the first four reach the TIP on purpose**:
```bash
git status                                             # clean
grep -c '### 10.58' SPEC.md                            # 1   rev 21
grep -c 'ALL THREE CHANNELS' SPEC.md                   # ?   rev 21 - watch it print
grep -c 'STRADDLING' SPEC.md                           # ?   rev 21 - watch it print
ls HANDOFF_rev21.md                                    #     rev 21
grep -c '### 10.56' SPEC.md                            # 1   ANCESTOR rev 20
grep -c 'T1_CTAN_NOBOUNCE' shader_solve.py             # 4   ANCESTOR rev 20
grep -c '_BODY' cream_rms.py                           # 4   ANCESTOR rev 19
grep -c '_arch_lip_z' verify.py                        # 2   ANCESTOR rev 18
grep -c 'matte_tap' studio.py                          # 6   ANCESTOR rev 17
grep -c '_coons_cap' t1_core.py                        # 3   ANCESTOR rev 16
grep -c 'The threshold is not the parameter' post.py   # 1   ANCESTOR rev 13
```
**THE TWO FIGURES MARKED `?` ARE DELIBERATE.** They are filled in from the
fresh-clone verification console in §7, never typed from memory — that failure
has now happened in EIGHT consecutive revisions and been caught twice by this
very rule. See §7.
Ancestry:
```bash
for c in f3c53f4 87aeaa6 d519fc6 5087b84 7ce3d03 f3cde44 efc1268 456b201; do
  git merge-base --is-ancestor $c HEAD && echo "$c ok" || echo "$c LOST"; done
```
**Known limitation, stated rather than hidden:** the ancestry loop's newest
entry is a rev-19 commit, because a hash cannot be written into the file that
contains it without amending, and rev 14 learned not to amend. **The TIP is
covered by the rev-21 content greps instead**, which cannot pass on a tree
missing rev 21. Both halves of rev 18's rule are satisfied, by different
mechanisms.
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
**0.516 0.515 0.516**. Every figure identical to rev 18, 19 and 20 — rev 21
changes SPEC only.
## 3. What rev 21 changed — `HANDOFF_rev21.md` has the full account
`SPEC.md` only: **§10.57** (five routes to the cream albedo, all refuted;
the owner's napkin/steel reading; the new all-three-channels rule) and
**§10.58** (a subagent's claim tested and half refuted), plus the change log.
**No code. No geometry. No constant.**
**Things you must not silently undo — see `HANDOFF_rev21.md` §4**, and rev 20's
§4, rev 19's §4 and rev 18's §4 all still stand in full.
## 4. Still open
See `HANDOFF_rev21.md` §5 for the full list. The ones that matter:
- **`CREAM`** — still open, now with the reason understood. It needs a
  same-light, **same-CLASS**, three-channel reference, or an established neutral
  transform for `ref_rear34`. **Neither exists in the three photographs.** It may
  have to be accepted as bracketed and LABELLED rather than solved.
- **`H_ROOF`** — my call, and I have not given it for FIVE revisions. Ask me
  once, plainly, with the recommendation in `HANDOFF_rev20.md` §5.
- **`COUNTERTAN`'s HUE** — cheap, shader-only, untouched since rev 12, and
  ORTHOGONAL to the pedestal fight: built h 42.3° / sat 0.254 against an
  independent 1266-px read of **28.4° / 0.333**. `T1_CTAN` already exists.
- **`COUNTERTAN`'s ~69 % pedestal** — UNIDENTIFIED. Best lead: the occlusion
  hypothesis; needs an object-index pass.
- **Five shut-line × aperture crossings, one on the show flank.**
- **`folk_gen.py` carries the banned flat px/m at `:1884` AND four stale
  constants** — the folk-art bake frame is built on retired numbers, and §10.10
  makes artwork replication a hard bar.
- SPEC §10.3's table still lists the RETIRED red (196,106,36); §10.9's table
  still lists the retired rake 0.0330. `PLATE_W = 0.3300` has no provenance.
## 5. FIRST QUESTION FOR THE OWNER
1. **`H_ROOF` — I owe you this and have owed it for five revisions.** Ask once,
   plainly, with the rev-20 recommendation. Do not start item 2 without it.
2. Unchanged and still the one photograph that would move the most: **a head-on
   rear (or front) elevation from roof height or above, with the counter and the
   lids clear of the section.** It is now also the only realistic route to
   closing `CREAM`.
## 6. Ordered work list for rev 22
1. **A HERO AT 4800×3200.** Nothing photographed since rev 16 — the arch fix,
   the hubcap rings and the cream mottle are all unseen. `CREAM` is not moving
   without a new photograph, so the reason rev 20 held this **no longer
   applies**. Shoot it first, and send it as it lands.
2. **`H_ROOF`** — implement whichever I choose.
3. **`COUNTERTAN`'s HUE** onto its own cited measurement. One render, one
   constant, orthogonal to the level fight. Hold the LEVEL bracketed.
4. The shut-line × aperture invariant: generalise the `t1_shell` assert to all
   four outlines, both arches and all five apertures, and give `CARGO_GAP`
   samples on its straight runs. **Expect it to FAIL when first armed — five
   crossings are live. That is the guard working; fix the geometry, not the
   threshold.**
5. `folk_gen.py`'s stale constants and its flat px/m.
6. The tail-lamp material slot; `Senor`'s letterforms; `SCR`'s +80 mm.
7. Camera absolutely last.
## 7. THE COMMIT COUNT AND THE CONTENT FIGURES
This section is written LAST, after the final commit, and every figure in §1 was
read off a fresh-clone verification run rather than typed from memory. **This has
gone wrong in EIGHT consecutive revisions during handoff assembly** — a truncated
console tail, a stale hash, five wrong counts, and a `grep -c` that counted
LINES rather than occurrences. The rule holds: **do not put a figure in an
acceptance test unless you watched it print.**
**FILL IN FROM THE VERIFICATION CONSOLE — see §1's two `?` entries.**
