# NEXT CONTEXT PROMPT — rev 20
Please act as my expert. Continue the Señor Tacombi combi build. **Nineteen
revisions sit behind this.** You are picking up mid-stream, not starting.

## Step 1 — read my memory BEFORE you read any code
`/areas/tacombi-combi-3d.md`, then `/areas/tacombi-combi-3d-rev14.md`, then
`/areas/tacombi-combi-3d-rev17.md`, then `/areas/tacombi-combi-3d-rev18.md`
(**which now carries rev 19 too**), then `/areas/tacombi-combi-sticker.md`,
then `/preferences.md`. Five prior contexts skipped them; one cost half a day
and produced the wrong body type. If you cannot read them, say so explicitly
rather than quietly proceeding.

**I have never stood in the bus.** The "remember standing in the kombi" bar is
about the RESTAURANT'S owner, the person this is for. **Do not ask me what the
real vehicle looks like.** Ask me what a PHOTOGRAPH shows — that has now paid
off ten times, most recently when it retired the entire cream measurement
surface — but measure the surface, never ask about it.

## Step 2 — restore, and verify BY CONTENT (never by hash or commit count)
See §1 below. **SEVEN bundle lines now, and the rev14b line is a `fetch`.**
Anything not on my disk does not exist — **rev 19 opened with rev 18 missing
from my disk entirely, exactly as rev 18 opened with rev 17 missing.** The
ancestry loop caught it that time and the content greps agreed. Read §1's note
before you trust any check.

## Step 3 — install Blender 4.5.3 and run BOTH guards before proposing anything
```bash
curl -fsSL -o b.tar.xz https://download.blender.org/release/Blender4.5/blender-4.5.3-linux-x64.tar.xz
tar -xf b.tar.xz && mv blender-4.5.3-linux-x64 /tmp/blender
/tmp/blender/4.5/python/bin/python3.11 -m pip install pillow scipy
```
That pip line is required. Report the guards' ACTUAL output. Both levels.

## Step 4 — read, in this order
`STATE.md` → `SPEC.md` §10, then §10.9 through §10.52 → this file →
**`HANDOFF_rev19.md`** → `AUDIT_rev18_loft.md` → `HANDOFF_rev18.md` →
`HANDOFF_rev17.md` → `HANDOFF_rev16.md` → `LOFT_GROUND_rev15.md` →
`AUDIT_rev12.md` → `AUDIT_rev11.md` → `SKEPTIC_PASS.md` →
`REF_MEASUREMENTS.md`.
`STATE.md` is machine-written by `audit.py`. **If it and any prose disagree, it
is right — EXCEPT for its arch row, see §4.**

**§10.29 carries two corrections that touch every REF number. §10.34–37 are rev
16's. §10.45–48 are rev 18's and RETIRE claims in §10.34 and §10.37. §10.49–52
are rev 19's and they RETIRE the surface every cream number was measured on,
the character instrument that produced them, and the claim that the cream is
26× too uniform — read them before you use any cream number.**

## Step 5 — ASK ME WHAT THE PHOTOGRAPHS SHOW before you measure from them
This has now paid off ten times. **My answers are not infallible — ask me
anyway, then measure what I say.** Show me a crop, mark the regions, give me
options, and **print the crop box**. rev 14's box was 120 px off; rev 16's
detector locked onto brass nosing 30 rows early; rev 17 drew two wrong boxes,
one on the "Tacombi" lettering; **rev 19's first region-4 box straddled the
dark roof opening and was redrawn before it was sent.**
**A CLASS GATE IS A PROBE TOO, and so is a BRIEF.** Three of rev 17's four work
items came back with their briefs refuted; two of rev 18's four did; **rev 19's
single work item came back with its brief refuted three separate ways.**

## Step 6 — the work
§6 below is the ordered list. **The loft is DONE and AUDITED. The arch is
FIXED. The guards are REAL. The cream is re-grounded on the vehicle and the
map is BUILT, WIRED and MEASURED — and its chroma amplitude is short by a
bounded, identified amount.**

## Step 7 — resolution
rev 16 shipped 4800×3200 in 20 strips, worst seam z 1.89. Drive
`hero.py --only N` one strip per call then `--stitch-only`; run `post.py`
**once** on the stitched frame, never per strip. Middle strips ~6 min each.
**No hero has been rendered since rev 16 — the arch fix, rev 17's hubcap rings
and rev 19's cream mottle are all unphotographed.**

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
ONE roof opening under the flower-mural lid. **The cream "La Santa" panel is a
DETACHED SIGN — confirmed a second time in rev 19, and it is NOT a cream
reference.** The counter has a bare/varnished plywood top with brass nosing.
Flank RED sRGB (196,49,36), **albedo saturation 0.816 LOCKED**. Rake **17.75
mm/m**. Serving bays **EQUAL at 0.5155 m**. `optics-6` CLOSED. `materials-5`
CLOSED. Tail lamp **round**. Windscreen **split, two panes**. Nolita admissible
**FOR GEOMETRY ONLY**, every such number TAGGED. SPEC §6's pure-white backdrop
lock **RETIRED**.
Settled rev 16: `RT_ALL 0.0949`, `CR_ALL 0.1179`, **D = 0.2128**; rear overhang
**0.773**; Coons caps at NHALF 57 / NLOOP 112.
Settled rev 17: **`W_ALBEDO` CLOSED for good**; `ref_side.jpg` is the **worst
frame**; hubcap ring **0.093 ± 0.012**; `vw_bars`' air gap **never existed**.
Settled rev 18: the rear arch **holds its crown**, tyre gap **39.7 mm**;
`LOFT_GROUND` §2.3's **`(0.10, 0.014)` is REFUTED**; px/m on `ref_rear34.jpg`'s
**plate plane** is **344.1 ± 6.7**.
**NEW, rev 19 and now settled:** the cream reference is **`_BODY =
(885, 968, 292, 388)`**, the bus's own paint, gated on **GEOMETRY ONLY**;
the character is **CHALKY SUN-FADE MOTTLE by a DERIVED verdict** that returns
None when unsupported; **"the cream is 26× too uniform" is RETIRED** — dL\* rms
is already 0.322/0.584/0.948 against 0.385/0.493/0.735; the cream's flank plane
is **337 ± 7 px/m**, a BRACKET, **not** the plate's 344.1.
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
* **Check what a guard, a probe, a crop, a CLASS GATE or a BRIEF can physically
  see — including WHICH SURFACE.** Print the crop box.
* **A VERDICT PRINTED AS A CONSTANT STRING IS NOT A MEASUREMENT.** rev 19's
  character instrument printed "CHALKY SUN-FADE MOTTLE" for a box of pure red
  paint at 0.0 % purity with every statistic `nan`.
* **MEASURE THE PSF BEFORE QUOTING ANYTHING NEAR THE LIMIT**, and **sweep the
  threshold rather than picking one**.
* **A negative control turns a number into a measurement — and check the
  control itself.**
* **Before scheduling a solve, ABLATE THE CONSTANT TO ZERO — then check the
  ablation is measuring the right STATISTIC.** rev 19's luminance ablation said
  the mottle map was inert. It was not: the lever is chromatic and the
  estimator was achromatic. **An inert-looking ablation can mean the wrong
  estimator, not a dead constant.**
* **CLIPPING DESTROYS TEXTURE.** Print the clipped fraction on both sides of any
  comparison. rev 19's first cream ratio read 3× because one patch was 10 %
  clipped and the other 0.2 %; the truth is 2.1–2.6×.
* **An ORTHO render has an EXACT px/m** — put the render side on one and all the
  scale uncertainty collapses into one stated bracket on the photograph.
* **Verify a projection before measuring through it.** `X_TAIL` predicted column
  1961.9 against an alpha edge at 1961; the wrong sign missed by 103 px.
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
* **The device bridge may drop mid-transfer and may refuse a 19 MB file.** Split
  on my machine, stage as PARALLEL single-file calls, reassemble, **verify by
  md5 against my disk before using it**. `device_bash` cannot `rm`.

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
git pull --ff-only ../tacombi_rev19_incremental.bundle HEAD      # -> 87, clean
```
**If a pull says "Need to specify how to reconcile divergent branches", STOP.**
```bash
git status                                             # clean
grep -c '### 10.52' SPEC.md                            # 1   rev 19
grep -c '_BODY' cream_rms.py                           # 4   rev 19
grep -c 'FADEV_MOTTLE' t1_mats.py                      # 2   rev 19
grep -c 'FadeRough' t1_mats.py                         # 5   rev 19
grep -c '### 10.48' SPEC.md                            # 1   ANCESTOR rev 18
grep -c '_arch_lip_z' verify.py                        # 2   ANCESTOR rev 18
grep -c '### 10.44' SPEC.md                            # 1   ANCESTOR rev 17
grep -c 'matte_tap' studio.py                          # 6   ANCESTOR rev 17
grep -c '_coons_cap' t1_core.py                        # 3   ANCESTOR rev 16
grep -c 'The threshold is not the parameter' post.py   # 1   ANCESTOR rev 13
ls HANDOFF_rev19.md AUDIT_rev18_loft.md HANDOFF_rev18.md LOFT_GROUND_rev15.md
```
Ancestry — **the last entry is a rev-19 commit, and that is the point**:
```bash
for c in f3c53f4 87aeaa6 d519fc6 5087b84 7ce3d03 f3cde44 efc1268 456b201; do
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
**0.516 0.515 0.516**. Every figure identical to rev 18 — rev 19 is
shader-only. `cutters rolled back | none` is a **STATE.md row**, not a print.

## 3. What rev 19 changed — `HANDOFF_rev19.md` has the full account
`cream_rms.py` (`_LID` retired, `_BODY` added, `spectrum()` and a DERIVED
`character()`), `t1_mats.py` (`FadeRough` group input, `fadev_from`, the
`FADEV_MOTTLE` chain inside `body_paint`, seven `MOTTLE_*` constants,
`T1_FADEV`), `SPEC.md` (§10.49–52 + change log), new `fadev_ablate.py` and
`mottle_measure.py`, `HANDOFF_rev19.md`.
**Things you must not silently undo — see `HANDOFF_rev19.md` §4**, and rev 18's
§4 still stands in full.

## 4. Still open
See `HANDOFF_rev19.md` §5 for the full list. The ones that matter:
- **The mottle map's CHROMA amplitude, and the lever is bounded.** dC\* rms
  render **0.240 / 0.249 / 0.253** (flat) vs photograph **0.744 / 1.015 /
  1.295** (growing). AMP 0.55 → 2.0 moved it 0.240 → 0.241: the fade factor
  clamps at 1.0 and the *modulation* collapses past it. The ceiling is the full
  `W_FADE_SAT = 0.88` swing, ~12 % saturation, which on the render's C\* ≈ 12
  cream cannot reach 1.3. **Give the mottle its own chroma gain so the uniform
  fade keeps 0.88.** Bounded next step, not a sweep.
- **§10.52 — a FOURTH `STATE.md` phantom, deliberately NOT repaired.**
  `audit.py:156` and `:474` still compute `ARCH_R − TIRE_R`, so `STATE.md`
  publishes `| arch radius − tyre radius | 41.0 mm (measured 41) |` against the
  mesh's **39.7 mm**, 68 lines below the real number, with a hand-typed
  "(measured 41)". One line each; it changes `STATE.md`, so it is recorded
  rather than slipped in at the end of a revision.
- **`PLATE_W = 0.3300` has no provenance.** rev 18's §5 says it is "bounded by
  the wheel control at < 0.1754 m" — **that bound is on `PLATE_OUTER_H`.**
- **`H_ROOF = 1.960` is UNSUPPORTED** — direct mesh probe reads **1.9835 ±
  0.0007**. Your call, still not taken, four revisions running.
- **Five shut-line × aperture crossings, one on the show flank.**
  `CARGO_GAP` samples 5.2 % of its own outline; `gap_cargo_mid` never.
- `COUNTERTAN`'s interreflection test — **still not run, four revisions**.
- `SCR` +80 mm aft and 12–24 mm short; `Senor` 0.504 of its 0.782 ceiling.
- The tail-lamp material slot; `probe_rev16.py`'s `xa` vs `xa`; `folk_gen.py`'s
  four stale constants; SPEC §1713's stale `RAKE_DZDX`; the ~12 unverified
  image URLs never looked at.
- **Parked:** tyre deflection. **Logged not applied:** the bays may be glazed.

## 5. FIRST QUESTION FOR THE OWNER
Unchanged: **a head-on rear (or front) elevation from roof height or above,
with the counter and the lids clear of the section.** It settles the flat tail
panel, the `RT`/`CR` split, and would give `H_ROOF` a datum that is not the
ground line §10.11 bans.

## 6. Ordered work list for rev 20
1. **FINISH THE CREAM MAP: give the mottle its own chroma gain.** Target dC\*
   rms **0.744 / 1.015 / 1.295** at σ 5.9 / 11.9 / 23.7 mm, corr(dL\*,dC\*)
   **+0.042 / −0.106 / −0.294**. Do NOT chase dL\* — it is already 0.322 /
   0.584 / 0.948 against 0.385 / 0.493 / 0.735 and runs OVER at coarse scale.
   Ablate, and check the ablation is measuring the right statistic.
2. **§10.52** — repair `audit.py`'s two constants-only arch lines and regenerate
   `STATE.md`.
3. **`H_ROOF`** — put the decision to me with §10.48's finding.
4. `COUNTERTAN`'s interreflection test — one render. Fourth revision on the list.
5. The shut-line × aperture invariant: generalise the `t1_shell` assert to all
   four outlines, and give `CARGO_GAP` samples on its straight runs.
6. The tail-lamp material slot; `Senor`'s letterforms; `SCR`'s +80 mm.
7. **A hero at 4800×3200.** Nothing photographed since rev 16.
8. Camera absolutely last.

---
**A NOTE ON ONE OF THE CONTENT CHECKS.** `grep -c 'FADEV_MOTTLE'` first said
**3** in this file. I had not watched it print. The verification run on a fresh
clone returned **2** — `mot.name` and `mot.label` are set on one line and
`grep -c` counts LINES, not occurrences. Corrected to 2 before this file
shipped. **Seventh instance of the same failure, and the first one caught by a
content check rather than by a commit count.** The rule holds: do not put a
figure in an acceptance test unless you watched it print.

**A NOTE ON THE COMMIT COUNT ABOVE.** It says 87 and it was written *after* the
commit that regenerates `STATE.md`, then corrected once when the FADEV_MOTTLE
fix added a commit, then re-verified from a fresh clone. This has gone wrong in six consecutive
revisions during handoff assembly. **Read the count off the console after the
last commit, then re-cut the bundle, then verify again.** It is still only a
regression catcher — verify by content.
