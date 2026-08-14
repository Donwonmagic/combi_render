# NEXT CONTEXT PROMPT — rev 18
Please act as my expert. Continue the Señor Tacombi combi build. **Seventeen
revisions sit behind this.** You are picking up mid-stream, not starting.
## Step 1 — read my memory BEFORE you read any code
`/areas/tacombi-combi-3d.md`, then `/areas/tacombi-combi-3d-rev14.md`, then
`/areas/tacombi-combi-3d-rev17.md`, then `/areas/tacombi-combi-sticker.md`,
then `/preferences.md`. Four prior contexts skipped them; one cost half a day
and produced the wrong body type. If you cannot read them, say so explicitly
rather than quietly proceeding.
**`/areas/tacombi-combi-3d-rev17.md` carries a correction to the others:
I have never stood in the bus.** The "remember standing in the kombi" bar is
about the RESTAURANT'S owner, the person this is for. **Do not ask me what the
real vehicle looks like.** Ask me what a PHOTOGRAPH shows — that has paid off
eight times — but measure the surface, never ask about it.
## Step 2 — restore, and verify BY CONTENT (never by hash or commit count)
See §1 below. **Two of the checks are ANCESTOR checks and they are not
optional.** Anything not on my disk does not exist.
## Step 3 — install Blender 4.5.3 and run BOTH guards before proposing anything
```bash
curl -fsSL -o b.tar.xz https://download.blender.org/release/Blender4.5/blender-4.5.3-linux-x64.tar.xz
tar -xf b.tar.xz && mv blender-4.5.3-linux-x64 /tmp/blender
/tmp/blender/4.5/python/bin/python3.11 -m pip install pillow scipy
```
That pip line is required — Blender's bundled Python has neither, and
`shader_solve.py`, `cream_rms.py` and `post.py`'s exact backdrop flood all need
them. Report the guards' ACTUAL output. Both levels, every time.
## Step 4 — read, in this order
`STATE.md` → `SPEC.md` §10, then §10.9 through §10.44 → this file →
`HANDOFF_rev17.md` → `HANDOFF_rev16.md` → `LOFT_GROUND_rev15.md` →
`AUDIT_rev12.md` → `AUDIT_rev11.md` → `SKEPTIC_PASS.md` → `REF_MEASUREMENTS.md`.
`STATE.md` is machine-written by `audit.py` from the mesh built in the same
process. **If it and any prose disagree, it is right** — but see §4, it still
carries one phantom row.
**§10.29 carries two corrections that touch every REF number.** **§10.34–37 are
rev 16's and supersede parts of `LOFT_GROUND_rev15`** — read §10.34's withdrawal
of the roof-silhouette/proud-strip reading before you use that file.
**§10.38–44 are rev 17's**, and **§10.38 invalidates every "the cream is 26×
too uniform" statement anywhere in the repo.**
## Step 5 — ASK ME WHAT THE PHOTOGRAPHS SHOW before you measure from them
This has now paid off eight times. **And my answers are not infallible — ask me
anyway, then measure what I say.** Show me a crop, mark the regions, give me
options. And check your own crop is where you think it is: rev 14's tail-face
box was 120 px off, rev 16 caught its own red-body detector locking onto the
brass counter nosing 30 rows early, and **rev 17 drew two wrong boxes — one for
me and one handed to an agent, which landed on the "Tacombi" lettering.**
**rev 17 extends this rule: A CLASS GATE IS A PROBE TOO, and so is a BRIEF.**
Three of rev 17's four work items came back with their briefs refuted.
## Step 6 — the work
§6 below is the ordered list. **The loft is DONE. The cream is GROUNDED but NOT
BUILT** — rev 18's first job, and it is blocked on one measurement.
## Step 7 — resolution
rev 16 shipped 4800×3200 in 20 strips, worst seam z 1.89. Drive
`hero.py --only N` one strip per call then `--stitch-only`; run `post.py`
**once** on the stitched frame, never per strip. Middle strips take ~6 min each
at 4800×3200 — budget for it.
## How I work
* Ground in the reference → build → adversarial audit → iterate. Never build
  before grounding. Never call it done off self-review.
* Report the measurement against the reference, **with its ceiling** so the
  number means something. Never a self-assigned score.
* Do not tell me anything is ready. Tell me what is fixed, what is still wrong,
  and what you measured.
* Keep visible cadence on long work and send renders as they land.
* Travel between contexts consciously, every time: record every locked decision
  in `SPEC.md` with a change-log entry, commit it, regenerate `STATE.md`, write
  a handoff and a next-context prompt, and put it all on my disk.
## Already settled — do not re-open without new evidence AND a different method
Tyre OD 0.665 m on 16-inch rims. No rear bumper in service; front bumper cream.
ONE roof opening, under the flower-mural lid, strip of roof surviving both
sides, solid roof fore and aft. The cream "La Santa" panel is a DETACHED SIGN.
The counter has a **bare/varnished plywood** top with brass nosing on its outer
edge. Flank RED sRGB (196,49,36), **albedo saturation 0.816 LOCKED**. The
nose-down rake is **17.75 mm/m**. The serving bays are **EQUAL at 0.5155 m**.
`optics-6` CLOSED as refuted — **the vehicle does not float.** `materials-5`
CLOSED as dead. The tail lamp is **round**. The windscreen is a **SPLIT screen,
two panes**. **Nolita photographs are admissible FOR GEOMETRY ONLY** — livery,
weathering and artwork stay locked to my three photographs, and every
Nolita-derived number must be TAGGED in SPEC. **SPEC §6's pure-white backdrop
lock is RETIRED** — `--backdrop headroom` is the default.
Settled rev 16: the transverse roof section (`RT_ALL 0.0949`, `CR_ALL 0.1179`,
**D = 0.2128**); the rear arch as a flat-crowned ogee at **0.920 m** with
`ARCH_R` held; the rear overhang at **0.773 m**; Coons grid end-caps at
**NHALF 57 / NLOOP 112**.
**NEW, rev 17 and now settled:** the cream is **CHALKY SUN-FADE MOTTLE**, not
dirt, brush or dents — so **`W_ALBEDO` is CLOSED for good: a scalar multiply on
albedo cannot change chroma.** `cream_rms.py`'s 8.890 % is **the galley through
bay 3** and is retired. `ref_side.jpg` is the **worst frame in the set** (2.32
bits/px, DC quantiser 4). The hubcap ring is **band/outer D = 0.093 ± 0.012**.
`vw_bars`' air gap **never existed** — the V penetrates the W by 52.0 mm, and
§10.25's premise is wrong.
Never correct this vehicle toward the VW factory catalogue.
## Hard-won rules — every one was learned by breaking it
* Never set a vertical position from the ground line (~70 mm common-mode) — and
  the HUB-referenced chain carries the same disease, ~29 mm.
* A single linear px→metre scale does not hold along the flank.
* **An image slope of a fore-aft line is not a rake** — that cost five revisions.
* A rendered ratio is only an albedo ratio between two surfaces of the **same
  class** under the same light — paint-to-paint, not paint-to-plywood.
* A constant tuned against another constant must be expressed in terms of it.
* **A claim in prose is not a guard.** Grep for the node that does it.
  `vw_bars`' false docstring survived NINE revisions.
* **Check what a guard, a probe, a crop, a CLASS GATE or a BRIEF can physically
  see** — and print the crop box.
* **MEASURE THE PSF BEFORE QUOTING ANYTHING NEAR THE LIMIT.** rev 17: the same
  feature reads 1.05 σ in one frame and 11.6 σ in another, and the naive
  estimator on the blurred frame reads exactly DOUBLE.
* **A negative control turns a number into a measurement — and check the
  control itself.** rev 17's codec-floor control was wrong by 4× because a
  Gaussian blur at σ then a Gaussian high-pass at σ does not leave zero.
* **Before scheduling a solve, ABLATE THE CONSTANT TO ZERO.**
* **A restore check that only greps THIS revision's strings cannot detect a lost
  ANCESTOR.** Always assert something the PREVIOUS line added.
* **Do not put a figure in an acceptance test unless you watched it print** —
  and do not put one in a HANDOFF either. rev 17 declined to change `H_ROOF`
  for exactly this reason.
* **Do not claim byte-identity of a render path.** Two renders of the same frame
  with nothing changed differ by max 40 DN over 12.86 % of pixels. Compare the
  node graph instead.
* When a finding breaks something independently locked, measure it a third way
  before choosing — and if you must apply it, apply it so the lock survives.
* **A specialist that refutes its own brief is working correctly** — and so does
  a context that refutes the prompt it was handed, if it shows the measurement.
* **Watch for the lamppost** — `ref_side.jpg` columns 62–79 have produced four
  separate confident wrong numbers about the front of the vehicle.
* A single shell command is killed at 10 minutes; `nohup`/`setsid`/`disown` all
  fail. This box has 2 CPU cores — spawn 3–4 `Agent`s on **disjoint files**
  rather than running a Workflow. rev 17 ran three concurrently and it worked.
* **Backticks in a `git commit -m` message hit shell command substitution.**
  Write the message to a file and use `git commit -F`.
---
> **THE STANDARD, in the owner's words, and it governs every line below.**
> The final product should be nearly indistinguishable from the original.
> **Any single measurement off is unacceptable.** We are recreating a photo
> realistic version of **that exact bus** — not a 1963 T1, not a generic
> taqueria combi. The criterion is PER-MEASUREMENT, not on average.
>
> And above clinical accuracy: *"I really want this to give the person the
> opportunity to feel like they were on Playa del Carmen all those years ago.
> I want the owner to remember standing in the kombi, in this very picture
> that was provided."* — **that owner is the restaurant's owner, not me.**
---
## 1. Restore and verify — BY CONTENT, never by hash or commit count
```bash
git clone tacombi_history_rev9.bundle tacombi && cd tacombi
git pull --ff-only ../tacombi_rev14_unified.bundle HEAD          # -> 59 commits
git fetch ../tacombi_rev14b_incremental.bundle HEAD:refs/heads/b14   # FETCH, not pull
git pull --ff-only ../tacombi_rev15_incremental.bundle HEAD      # -> 67 commits
git pull --ff-only ../tacombi_rev16_incremental.bundle HEAD      # -> 71 commits
git pull --ff-only ../tacombi_rev17_incremental.bundle HEAD      # -> 75 commits, clean
```
**The rev14b line is a `fetch`, not a `pull`** — it is DIVERGENT from the rev-13
tip, so pulling it merges or errors; fetching it into a branch makes its commits
available and the rev-15 bundle carries the merge that reconciles them.
**If a pull says "Need to specify how to reconcile divergent branches", STOP.**
Then all of these must be true:
```bash
git status                                       # clean
grep -c '### 10.44' SPEC.md                      # 1
grep -c '### 10.37' SPEC.md                      # 1   <-- ANCESTOR CHECK (rev 16)
grep -c 'The threshold is not the parameter' post.py  # 1   <-- ANCESTOR CHECK (rev 13)
grep -c 'A CLASS GATE IS A PROBE TOO' cream_rms.py    # non-zero
grep -c 'CAP_RING_BANDFRAC' t1_detail.py         # non-zero
grep -c 'matte_tap' studio.py                    # non-zero
grep -c '_coons_cap' t1_core.py                  # non-zero
ls HANDOFF_rev17.md LOFT_GROUND_rev15.md AUDIT_rev11.md AUDIT_rev12.md shader_solve.py cream_rms.py
```
Also assert ancestry, which no grep can do:
```bash
for c in f3c53f4 87aeaa6 d519fc6 5087b84 7ce3d03; do
  git merge-base --is-ancestor $c HEAD && echo "$c ok" || echo "$c LOST"; done
```
## 2. Both guards, and the figures I watched print
| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 1 warn** | **0 fail, 1 warn** |
| warn | roof crown @ rear axle **1.983** vs spec 1.960 (**+23 mm**) | **1.983** (**+23 mm**) |
| dome deficit | **+0** | **+0** |
| rear overhang | **0.7730** | **0.7730** |
| dims | L=**4.065** W=1.750 | same |
| cut roof hole | **68088v** | **252335v** |
| objects at `materials:` | **126** | **126** |
Also: `roof aperture: open, and solid fore / aft / both sides`; `TYRE_D=0.6650`;
3 open apertures on +Y; four shut lines `100 % open`; band `1.372–1.775`; bay
widths **`0.516 0.515 0.516`**; **185 meshes** (was 181 — the four hubcap rings);
**0 non-manifold edges**; **5 materials constant-rough**; 42 distinct materials.
`cutters rolled back | none` is a **STATE.md row**, not a console print.
## 3. What rev 17 changed — see `HANDOFF_rev17.md` for the full account
`cream_rms.py` (geometry gate + hard guard + the re-based instrument),
`audit.py` (the re-typed 4.290), `t1_core.py` (the false air-gap docstring, the
V's short arms), `t1_detail.py` (the hubcap ring), `studio.py` (the real matte),
`flank_compare.py` (windows, tarnish, the metric frame).
**Things you must not silently undo:**
- `cream_rms.cream_mask` is kept ONLY so the old wrong result stays
  reproducible. **Use `body_cream_mask`.** The hard guard in `run()` is there to
  stop the 8.890 % being quoted again — do not remove it.
- `codec_floor()` blurs by **4σ** and subtracts the LEAK. Do not "simplify" it
  back to blur-at-σ; that is the bug it exists to avoid, and it is worth 4×.
- `audit.py` now **imports `verify.SPEC["L"]`**. Do not re-type the target.
- `CAP_RING_BANDFRAC` drives the V's arm length in `t1_core.vw_bars`. They are
  deliberately coupled. Changing one moves the other, which is the point.
- `matte_tap` is opt-in via `T1_MATTE=1` and its `BW` / 8-bit / `Raw` settings
  are each load-bearing for a measured reason. See §10.42.
## 4. Still open, and now with numbers
- **THE CREAM MAP IS NOT BUILT, and it is blocked on ONE measurement**: px/m on
  `ref_rear34.jpg`'s cream plane. Three routes failed (aperture band truncated
  by the counter ≥320; tyre truncated by the frame ≥397; **bulb string not
  detected**, peak/mean 3.6, candidates 225–629). Everything else is ready — the
  spectrum is measured (1.72 % at σ 1 to 6.75 % at σ 12, codec removed), the
  character is settled (chalky fade mottle), and the mechanism is identified
  (modulate `FadeVert` spatially + drive roughness; **NOT** albedo breakup).
  **A fourth route worth trying: the `1963` plate, whose outer height is the
  locked `PLATE_OUTER_H = 0.16823`, and which is visible in `ref_rear34.jpg`.**
- **`STATE.md`'s height row is still a phantom** — `3.0169 vs 1.9600 =
  +1056.9 mm OUT` every run, measuring the open lid board standing above the
  roof. Same class as the 4.290 row I fixed. Exclude the lid objects or delete
  the row; a prose note under it is not a guard.
- **`H_ROOF` still 1.960 and the warn stands** (§10.44). To close it, **probe
  the built mesh directly** — do not compose it from tabulated differences, and
  do not adopt 1.981 from prose.
- **`COUNTERTAN` is 6.8σ / 2.0σ / 5.2σ out** with an albedo gain of only
  0.33–0.49. The next test is still one render: hide the fascia from the top's
  diffuse bounce and see whether interreflection moves the denominator with the
  numerator. **Not run in rev 17.**
- **No adversarial audit of the rev-16 loft has ever been run.** It is new
  geometry checked only by its own author, and it is now the largest unexamined
  surface in the repo. **This should be rev 18's second job.** Spawn 3–4
  `Agent`s on disjoint files.
- The **tail lamp's lens hue still shares the `amber` material** with the front
  indicator. Needs a new slot in `t1_mats.py`.
- `flank_compare.py` now FAILS on **`Senor` alone**, 0.504 of its own 0.782
  ceiling, and the texture-alpha control shows that belongs to the panel and the
  `Senor` reconstruction, not the render. Also open from that work: **`SCR` is
  +80 mm aft and 12–24 mm short**, and the projective map and `k_t` disagree by
  **2.3 %** at the rear hub.
- `hero.py` **does not stitch mattes**, so a matte for a stripped hero must come
  from a single-pass render.
- The head-on rear/front elevation is still missing, and **the flat tail-panel
  height is still 1.02 m built against a 0.36–0.72 m bound**. The open-web search
  returned a clean negative at rank 1–4 but recovered ~12 **unverified** image
  URLs it could not look at. **A vision-capable pass over that list is cheap and
  has still not been run.**
- **Parked deliberately:** tyre deflection. **Logged not applied:** the serving
  bays may be glazed.
## 5. FIRST QUESTION FOR THE OWNER
Same frame, and it is now worth MORE than ever: **a head-on rear (or front)
elevation from roof height or above, with the counter and the lids clear of the
section.** It settles the flat tail panel AND the split between `RT` and `CR`.
**But rev 18's cheapest unblock is smaller and does not need him**: a locked
scale on `ref_rear34.jpg`. Try the `1963` plate first.
## 6. Ordered work list for rev 18
1. **Lock px/m on `ref_rear34.jpg`**, then **build the cream fade-mottle map** —
   spatially modulate `FadeVert`, drive roughness with it, measure with
   `cream_rms.rear34_cream`. **Ablate to zero first.**
2. **A fresh adversarial audit of the rev-16 loft AND of rev 17's own changes.**
   3–4 `Agent`s, disjoint files, each told to REFUTE.
3. `COUNTERTAN`'s interreflection test — one render.
4. `STATE.md`'s phantom height row.
5. The tail-lamp material slot; `Senor`'s letterforms.
6. `H_ROOF`, by direct mesh probe.
7. Camera absolutely last — re-framing invalidates every hero-pixel measurement.
**`t1_shell.py`'s import-time assertion exists because a shut line crossing an
arch lip collapsed the shell 205 562 v → 12 v for six revisions.** Respect it.
If a change trips a guard, do not widen the guard.

---
**A NOTE ON THE COMMIT COUNT ABOVE.** It says 75 and it was written *after* the
commit that fixed it, then re-verified from a fresh clone. The first draft of
this file said 73; the restore printed 74; correcting the file made it 75. That
is the fifth revision running this has happened, always during handoff assembly.
**Read the count off the console after the last commit, then re-cut the bundle,
then verify again.** It is still only a regression catcher — verify by content.
