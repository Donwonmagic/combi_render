# NEXT CONTEXT PROMPT — rev 19
Please act as my expert. Continue the Señor Tacombi combi build. **Eighteen
revisions sit behind this.** You are picking up mid-stream, not starting.

## Step 1 — read my memory BEFORE you read any code
`/areas/tacombi-combi-3d.md`, then `/areas/tacombi-combi-3d-rev14.md`, then
`/areas/tacombi-combi-3d-rev17.md` (**which now carries rev 18 too**), then
`/areas/tacombi-combi-sticker.md`, then `/preferences.md`. Four prior contexts
skipped them; one cost half a day and produced the wrong body type. If you
cannot read them, say so explicitly rather than quietly proceeding.

**`/areas/tacombi-combi-3d-rev17.md` carries a correction to the others:
I have never stood in the bus.** The "remember standing in the kombi" bar is
about the RESTAURANT'S owner, the person this is for. **Do not ask me what the
real vehicle looks like.** Ask me what a PHOTOGRAPH shows — that has now paid
off nine times — but measure the surface, never ask about it.

## Step 2 — restore, and verify BY CONTENT (never by hash or commit count)
See §1 below. **SIX bundle lines now, and the rev14b line is a `fetch`.**
Anything not on my disk does not exist — **rev 18 opened with rev 17 missing
from my disk entirely**, and the ancestry loop it was handed passed 5 of 5
anyway. Read §1's note on that before you trust any check.

## Step 3 — install Blender 4.5.3 and run BOTH guards before proposing anything
```bash
curl -fsSL -o b.tar.xz https://download.blender.org/release/Blender4.5/blender-4.5.3-linux-x64.tar.xz
tar -xf b.tar.xz && mv blender-4.5.3-linux-x64 /tmp/blender
/tmp/blender/4.5/python/bin/python3.11 -m pip install pillow scipy
```
That pip line is required. Report the guards' ACTUAL output. Both levels.

## Step 4 — read, in this order
`STATE.md` → `SPEC.md` §10, then §10.9 through §10.48 → this file →
**`AUDIT_rev18_loft.md`** → `HANDOFF_rev18.md` → `HANDOFF_rev17.md` →
`HANDOFF_rev16.md` → `LOFT_GROUND_rev15.md` → `AUDIT_rev12.md` →
`AUDIT_rev11.md` → `SKEPTIC_PASS.md` → `REF_MEASUREMENTS.md`.

`STATE.md` is machine-written by `audit.py`. **If it and any prose disagree, it
is right** — and as of rev 18 its three phantom rows are gone, so that
instruction finally means something.

**§10.29 carries two corrections that touch every REF number. §10.34–37 are rev
16's and supersede parts of `LOFT_GROUND_rev15` — read §10.34's withdrawal
first. §10.38 invalidates every "the cream is 26× too uniform" statement.
§10.45–48 are rev 18's and they RETIRE claims in §10.34, §10.37 and
`LOFT_GROUND` §2.3 — read them before you use any arch or roof number.**

## Step 5 — ASK ME WHAT THE PHOTOGRAPHS SHOW before you measure from them
This has now paid off nine times — most recently "empty chrome license plate
frame", which unblocked px/m. **My answers are not infallible — ask me anyway,
then measure what I say.** Show me a crop, mark the regions, give me options,
and **print the crop box**. rev 14's box was 120 px off; rev 16's detector
locked onto brass nosing 30 rows early; rev 17 drew two wrong boxes, one of
which landed on the "Tacombi" lettering.
**A CLASS GATE IS A PROBE TOO, and so is a BRIEF.** Three of rev 17's four work
items came back with their briefs refuted; **two of rev 18's four did.**

## Step 6 — the work
§6 below is the ordered list. **The loft is DONE and now AUDITED. The arch is
FIXED. The guards are REAL.** The cream map is grounded, unblocked, and still
not built — that is rev 19's first job.

## Step 7 — resolution
rev 16 shipped 4800×3200 in 20 strips, worst seam z 1.89. Drive
`hero.py --only N` one strip per call then `--stitch-only`; run `post.py`
**once** on the stitched frame, never per strip. Middle strips ~6 min each.
**No hero has been rendered since rev 16 — the arch fix and rev 17's hubcap
rings are both unphotographed.**

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
DETACHED SIGN. The counter has a bare/varnished plywood top with brass nosing.
Flank RED sRGB (196,49,36), **albedo saturation 0.816 LOCKED**. Rake **17.75
mm/m**. Serving bays **EQUAL at 0.5155 m**. `optics-6` CLOSED — the vehicle
does not float. `materials-5` CLOSED. Tail lamp **round**. Windscreen **split,
two panes**. Nolita admissible **FOR GEOMETRY ONLY**, every such number TAGGED.
SPEC §6's pure-white backdrop lock **RETIRED**.
Settled rev 16: transverse roof section `RT_ALL 0.0949`, `CR_ALL 0.1179`,
**D = 0.2128**; rear overhang **0.773**; Coons caps at NHALF 57 / NLOOP 112.
Settled rev 17: the cream is **CHALKY SUN-FADE MOTTLE**; **`W_ALBEDO` CLOSED for
good**; `cream_rms.py`'s 8.890 % retired; `ref_side.jpg` is the **worst frame**;
hubcap ring **0.093 ± 0.012**; `vw_bars`' air gap **never existed**.
**NEW, rev 18 and now settled:** the rear arch **holds its crown** and the tyre
gap measures **39.7 mm** on the mesh; `LOFT_GROUND` §2.3's **`(0.10, 0.014)` is
REFUTED** and the profile's Δx is **aft-positive**; px/m on `ref_rear34.jpg`'s
plate plane is **344.1 ± 6.7**.
Never correct this vehicle toward the VW factory catalogue.

## Hard-won rules — every one was learned by breaking it
* Never set a vertical position from the ground line (~70 mm common-mode) — the
  HUB-referenced chain has the same disease at ~29 mm.
* A single linear px→metre scale does not hold along the flank; the map is
  projective. **And a scale measured on one plane is not the scale on another —
  rev 18's 344.1 px/m is the PLATE plane.**
* **An image slope of a fore-aft line is not a rake** — that cost five revisions.
* A rendered ratio is only an albedo ratio between two surfaces of the **same
  class** under the same light.
* A constant tuned against another constant must be expressed in terms of it.
* **A claim in prose is not a guard.** Grep for the node that does it.
* **Check what a guard, a probe, a crop, a CLASS GATE or a BRIEF can physically
  see** — and print the crop box.
* **MEASURE THE PSF BEFORE QUOTING ANYTHING NEAR THE LIMIT**, and **sweep the
  threshold rather than picking one** — rev 18's plate edge is 5.3 px wide and
  the level choice moves the answer 2.18 %.
* **A negative control turns a number into a measurement — and check the control
  itself.**
* **Before scheduling a solve, ABLATE THE CONSTANT TO ZERO.**
* **A restore check that only greps THIS revision's strings cannot detect a lost
  ANCESTOR** — and **AN ANCESTOR CHECK IS ONLY AS GOOD AS THE NEWEST COMMIT IN
  IT.** rev 18's loop passed 5/5 on a tree missing all of rev 17, because its
  newest entry was the rev-16 tip. **Both checks must reach the tip.**
* **Do not put a figure in an acceptance test — or a HANDOFF — unless you
  watched it print.**
* **Do not claim byte-identity of a render path.** Compare the node graph.
* **If a change trips a guard, THAT IS THE GUARD WORKING. Never widen it.**
  rev 18 took `0 fail` to `1 fail` on purpose and then fixed the geometry.
* **A probe that cannot answer must return None, not an endpoint.** Two separate
  phantoms in this repo came from a probe answering anyway.
* When a finding breaks something independently locked, measure it a third way.
* **Watch for the lamppost** — `ref_side.jpg` columns 62–79 have produced four
  confident wrong numbers about the front of the vehicle.
* A single shell command is killed at 10 minutes. This box has 2 cores — spawn
  3–4 `Agent`s on **disjoint files**, read-only for audits, rather than a
  Workflow. rev 17 ran three; **rev 18 ran four**.
* **Backticks in `git commit -m` hit shell substitution.** Use `git commit -F`.
* **The device bridge may move only ~1 MB per call, one file per call.** Split
  large files on my machine, stage as PARALLEL single-file calls, reassemble,
  verify by md5. `device_bash` cannot `rm`.

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
git pull --ff-only ../tacombi_rev18_incremental.bundle HEAD      # -> 81, clean
```
**If a pull says "Need to specify how to reconcile divergent branches", STOP.**
```bash
git status                                             # clean
grep -c '### 10.48' SPEC.md                            # 1   rev 18
grep -c '_arch_lip_z' verify.py                        # 2   rev 18
grep -c '_ARCH_DMIN' t1_shell.py                       # 2   rev 18
grep -c '_ROOF_FLOOR' audit.py                         # 4   rev 18
grep -c '### 10.44' SPEC.md                            # 1   ANCESTOR rev 17
grep -c 'A CLASS GATE IS A PROBE TOO' cream_rms.py     # 1   ANCESTOR rev 17
grep -c 'matte_tap' studio.py                          # 6   ANCESTOR rev 17
grep -c '### 10.37' SPEC.md                            # 1   ANCESTOR rev 16
grep -c '_coons_cap' t1_core.py                        # 3   ANCESTOR rev 16
grep -c 'The threshold is not the parameter' post.py   # 1   ANCESTOR rev 13
ls AUDIT_rev18_loft.md HANDOFF_rev18.md HANDOFF_rev17.md LOFT_GROUND_rev15.md
```
Ancestry — **the last entry is a rev-18 commit, and that is the point**:
```bash
for c in f3c53f4 87aeaa6 d519fc6 5087b84 7ce3d03 f3cde44 efc1268; do
  git merge-base --is-ancestor $c HEAD && echo "$c ok" || echo "$c LOST"; done
```

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
**0.516 0.515 0.516**. `cutters rolled back | none` is a **STATE.md row**, not a
console print.

## 3. What rev 18 changed — `HANDOFF_rev18.md` has the full account
`verify.py` (three dead rows repaired + `_arch_lip_z` + the rake guard),
`t1_shell.py` (the arch: crown re-base, the refuted notch, the mirrored sign),
`audit.py` (three `STATE.md` phantoms + two hand-typed paragraphs),
`SPEC.md` (§10.45–48 + change log), `AUDIT_rev18_loft.md` (new).

**Things you must not silently undo — see `HANDOFF_rev18.md` §4.** Chiefly:
`_arch_lip_z` returns `None` and never an endpoint; `_ARCH_D` is an EXPRESSION
of `_ARCH_D0`, not a second table; `_arch_drop` negates `t` on purpose; the
engine-lid and rear-window thresholds are offsets from `X_TAIL`; `H` excludes
`lid_*` by name prefix; the height row deliberately has **no target**.

## 4. Still open
See `HANDOFF_rev18.md` §5 for the full list with numbers. The ones that matter:
- **The cream map is UNBLOCKED and STILL NOT BUILT.** px/m is locked at 344.1 ±
  6.7 **on the plate plane** — the cream patches are on other planes and the
  depth correction must be STATED, not assumed. Mechanism: modulate `FadeVert`
  spatially and drive roughness. **NOT albedo breakup. Ablate to zero first.**
- **`PLATE_W = 0.3300` has no provenance anywhere in the repo.** Every scale
  built on `PLATE_OUTER_H` inherits it. Bounded by the wheel control at
  < 0.1754 m, not measured.
- **`H_ROOF = 1.960` is UNSUPPORTED** — its only ground-line-free confirmation
  was withdrawn by §10.34 without anyone noticing that. Direct mesh probe reads
  **1.9835 ± 0.0007**. Your call, still not taken.
- **"R = 2.45 stays refuted" is false**, and **`D = 0.2116` is `1.960 − 1.7485`**.
- **Five shut-line × aperture crossings, one on the show flank.** Pre-dates rev
  16. `CARGO_GAP` samples 5.2 % of its own outline; `gap_cargo_mid` never.
- `COUNTERTAN`'s interreflection test — **still not run, two revisions running**.
- The rear-window "+0.15 m above" control still passes after the repair.
- `SCR` +80 mm aft and 12–24 mm short; `Senor` 0.504 of its 0.782 ceiling.
- The tail-lamp material slot; `probe_rev16.py`'s false docstring and its
  `xa` vs `xa` line; `folk_gen.py`'s four stale constants; SPEC §1713's stale
  `RAKE_DZDX`; the ~12 unverified image URLs never looked at.
- **Parked:** tyre deflection. **Logged not applied:** the bays may be glazed.

## 5. FIRST QUESTION FOR THE OWNER
Unchanged, and now worth more than ever: **a head-on rear (or front) elevation
from roof height or above, with the counter and the lids clear of the section.**
It settles the flat tail panel, the `RT`/`CR` split, and — newly — it would give
`H_ROOF` a datum that is not the ground line §10.11 bans.

## 6. Ordered work list for rev 19
1. **BUILD THE CREAM FADE-MOTTLE MAP.** Spatially modulate `FadeVert`, drive
   roughness with it, measure with `cream_rms.rear34_cream`. **Ablate to zero
   first.** State the plane your px/m applies to and correct for depth.
2. **`H_ROOF`** — direct mesh probe, then put the decision to me with §10.48's
   finding that 1.960 lost its only clean support.
3. `COUNTERTAN`'s interreflection test — one render. Third revision on the list.
4. The shut-line × aperture invariant: generalise the `t1_shell:391` assert to
   all four outlines against all arches and apertures, and give `CARGO_GAP`
   samples on its straight runs.
5. The tail-lamp material slot; `Senor`'s letterforms; `SCR`'s +80 mm.
6. **A hero at 4800×3200.** Nothing has been photographed since rev 16 — the
   arch fix and the hubcap rings are both unrendered.
7. Camera absolutely last — re-framing invalidates every hero-pixel measurement.

**`t1_shell.py`'s import-time assertion exists because a shut line crossing an
arch lip collapsed the shell 205 562 v → 12 v for six revisions.** Respect it.
**If a change trips a guard, do not widen the guard** — rev 18 deliberately
took `0 fail` to `1 fail` to expose the arch, then fixed the geometry.

---
**A NOTE ON THE COMMIT COUNT ABOVE.** It says 81 and it was written *after* the
commit that fixed it, then re-verified from a fresh clone. This has gone wrong
in five consecutive revisions during handoff assembly. **Read the count off the
console after the last commit, then re-cut the bundle, then verify again.** It
is still only a regression catcher — verify by content.
