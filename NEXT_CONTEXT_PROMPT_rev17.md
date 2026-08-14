# NEXT CONTEXT PROMPT — rev 17

Please act as my expert. Continue the Señor Tacombi combi build. **Sixteen
revisions sit behind this.** You are picking up mid-stream, not starting.

## Step 1 — read my memory BEFORE you read any code
`/areas/tacombi-combi-3d.md`, then `/areas/tacombi-combi-3d-rev14.md`, then
`/areas/tacombi-combi-sticker.md`, then `/preferences.md`. Three prior contexts
skipped them; one cost half a day and produced the wrong body type. If you
cannot read them, say so explicitly rather than quietly proceeding.

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
`STATE.md` → `SPEC.md` §10, then §10.9 through §10.37 → this file →
`HANDOFF_rev16.md` → `LOFT_GROUND_rev15.md` → `AUDIT_rev12.md` →
`AUDIT_rev11.md` → `SKEPTIC_PASS.md` → `REF_MEASUREMENTS.md`.
`STATE.md` is machine-written by `audit.py` from the mesh built in the same
process. **If it and any prose disagree, it is right.**
**§10.29 carries two corrections that touch every REF number**, and **§10.34–37
are rev 16's and they supersede parts of `LOFT_GROUND_rev15`** — read §10.34's
withdrawal of the roof-silhouette/proud-strip reading before you use that file.

## Step 5 — ASK ME WHAT THE PHOTOGRAPHS SHOW before you measure from them
This has now paid off eight times. **And my answers are not infallible — ask me
anyway, then measure what I say.** Show me a crop, mark the regions, give me
options. And check your own crop is where you think it is: rev 14's tail-face
box was 120 px off, and rev 16 caught its own red-body detector locking onto the
brass counter nosing 30 rows early.

## Step 6 — the work
§6 below is the ordered list. **The loft is DONE.** rev 17 is the shader and
compositing backlog that has been queued behind it since rev 12.

## Step 7 — resolution
rev 15 shipped 4320×2880 in 18 strips, worst seam z 2.75. Drive
`hero.py --only N` one strip per call then `--stitch-only`; run `post.py`
**once** on the stitched frame, never per strip. Middle strips take ~5 min each
at 4320×2880 — budget for it.

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
**NEW, rev 16 and now settled:** the transverse roof section
(`RT_ALL 0.0949`, `CR_ALL 0.1179`, **D = 0.2128**); the rear arch as a
flat-crowned ogee at **0.920 m** with `ARCH_R` held; the rear overhang at
**0.773 m**; Coons grid end-caps at **NHALF 57 / NLOOP 112**.
Never correct this vehicle toward the VW factory catalogue.

## Hard-won rules — every one was learned by breaking it
* Never set a vertical position from the ground line (~70 mm common-mode) — and
  rev 16 found the same common-mode in the HUB-referenced chain, ~29 mm.
* A single linear px→metre scale does not hold along the flank.
* **An image slope of a fore-aft line is not a rake** — that cost five revisions.
* A rendered ratio is only an albedo ratio between two surfaces of the **same
  class** under the same light — paint-to-paint, not paint-to-plywood.
* A constant tuned against another constant must be expressed in terms of it.
* **A claim in prose is not a guard.** Grep for the node that does it.
* **Check what a guard, or a probe, or a crop can physically SEE** — and print
  the crop box.
* **A guard can be strengthened instead of widened.** rev 16 did exactly this:
  the overall-length row can never be a measurement because `X_NOSE` is behind a
  lamppost, so a rear-overhang row was added beside it.
* **A negative control turns a number into a measurement.**
* **Before scheduling a solve, ABLATE THE CONSTANT TO ZERO.**
* **A restore check that only greps THIS revision's strings cannot detect a lost
  ANCESTOR.** Always assert something the PREVIOUS line added.
* **Do not put a figure in an acceptance test unless you watched it print.**
* When a finding breaks something independently locked, measure it a third way
  before choosing — and if you must apply it, apply it so the lock survives.
  **rev 16 is the worked example**: the brief said drop the roof 63 mm, that
  left 2 mm of metal above the serving bays and broke the windscreen anchor, and
  the third method said 41 mm and spent it on the junction instead.
* **A specialist that refutes its own brief is working correctly** — and so does
  a context that refutes the prompt it was handed, if it shows the measurement.
* **Watch for the lamppost** — `ref_side.jpg` columns 62–79 have produced four
  separate confident wrong numbers about the front of the vehicle.
* A single shell command is killed at 10 minutes; `nohup`/`setsid`/`disown` all
  fail. This box has 2 CPU cores — spawn 3–4 `Agent`s on **disjoint files**
  rather than running a Workflow.
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
> that was provided."*
---

## 1. Restore and verify — BY CONTENT, never by hash or commit count
```bash
git clone tacombi_history_rev9.bundle tacombi && cd tacombi
git pull --ff-only ../tacombi_rev14_unified.bundle HEAD          # -> 59 commits
git fetch ../tacombi_rev14b_incremental.bundle HEAD:refs/heads/b14   # FETCH, not pull
git pull --ff-only ../tacombi_rev15_incremental.bundle HEAD      # -> 67 commits
git pull --ff-only ../tacombi_rev16_incremental.bundle HEAD      # -> 69 commits
```
**The rev14b line is a `fetch`, not a `pull`** — it is DIVERGENT from the rev-13
tip, so pulling it merges or errors; fetching it into a branch makes its commits
available and the rev-15 bundle carries the merge that reconciles them.
**If a pull says "Need to specify how to reconcile divergent branches", STOP.**

Then all of these must be true:
```bash
git status                                       # clean
grep -c '### 10.37' SPEC.md                      # 1
grep -c '### 10.33' SPEC.md                      # 1   <-- ANCESTOR CHECK (rev 15)
grep -c 'The threshold is not the parameter' post.py  # 1   <-- ANCESTOR CHECK (rev 13)
grep -c '_coons_cap' t1_core.py                  # non-zero
grep -c 'ARCH_W_REAR' t1_shell.py                # non-zero
grep -c 'def _aft' t1_core.py                    # 1
grep -c 'rear overhang' verify.py                # non-zero
ls shader_solve.py cream_rms.py probe_rev16.py LOFT_GROUND_rev15.md AUDIT_rev11.md AUDIT_rev12.md
```
Also assert ancestry, which no grep can do:
```bash
for c in f3c53f4 87aeaa6 d519fc6 5087b84; do
  git merge-base --is-ancestor $c HEAD && echo "$c ok" || echo "$c LOST"; done
```

## 2. Both guards, and the figures I watched print
| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 1 warn** | **0 fail, 1 warn** |
| warn | roof crown @ rear axle **1.983** vs spec 1.960 (**+23 mm**) | **1.983** (**+23 mm**) |
| dome deficit | **0** | **0** |
| rear overhang | **0.7730** | **0.7730** |
| dims | L=**4.065** W=1.750 | same |
| cut roof hole | **68088v** | **252335v** |

Also: `roof aperture: open, and solid fore / aft / both sides`; `TYRE_D=0.6650`;
3 open apertures on +Y; four shut lines `100 % open`; band `1.372–1.775`; bay
widths **`0.516 0.515 0.516`**; **181 meshes**; **0 non-manifold edges**;
**5 materials constant-rough**; 42 distinct materials.
`cutters rolled back | none` is a **STATE.md row**, not a console print.

## 3. What rev 16 changed — see `HANDOFF_rev16.md` for the full table
The loft, in one rebuild: roof section (`RT_ALL`/`CR_ALL`, D = 0.2128), rear arch
as an ogee at 0.920 m, tail re-spaced to a 0.773 m overhang, Coons grid end-caps
at NHALF 57. `DOME_DEFICIT` → 0. Poles gone, max valence 115 → 6. Two latent
bugs fixed. `SPEC["L"]` re-expressed and a rear-overhang guard added.

**Things rev 16 changed that you must not silently undo:**
- `t1_core._aft()` and `aft_lut()` are the ONLY place the tail re-space lives.
  Re-measuring the overhang means changing `O_NEW` and nothing else. Do not
  re-type aft stations as metres.
- `NHALF = 57` is load-bearing at SUB=2. `T1_NHALF57=0` reproduces the failure.
- `RT_ALL`/`CR_ALL` are a JOINT fit to two measurements. `D` is the finding;
  `R` is a re-expression that moves with `Yt`. Do not quote `R` alone.
- `t1_detail.gutter()` and `bulb_string()` sit at `zt0 + 0.01512`, not at
  `zt − 0.72·rt`. That was re-expressed because `RT_ALL` moved.

## 4. Still open, and now with numbers
- **The crown warn: +23 mm against `SPEC H_ROOF = 1.960`.** `H_ROOF` was NOT
  tuned. REF §1 derived 1.960 from the banned ground line; the belt-anchored
  chain puts the crown at 1.981. **Your call whether to re-derive `H_ROOF`.**
- **The flat tail-panel HEIGHT is still 1.02 m built against a 0.36–0.72 m
  bound.** The counter occludes exactly that band. Needs the head-on rear
  elevation. Not guessed.
- **The arch's aft foot is now 313 mm from the aft skin, against 418 before.**
  Predicted by `LOFT_GROUND` §3.3 and the most likely constraint on any future
  tail change.
- **The cream is 26× too uniform at 25 mm** (0.339 % against a photograph
  re-measured at 8.890 %) and `W_ALBEDO` cannot fix it — its zero-ablation reads
  the same. The fix is a real detail map at the 10–40 mm scale driven into
  albedo AND roughness, measured with `cream_rms.py`, which is calibrated.
- **`COUNTERTAN` is 6.8σ / 2.0σ / 5.2σ out** with an albedo gain of only
  0.33–0.49. Next test, one render: hide the fascia from the top's diffuse
  bounce to see whether interreflection moves the denominator with the numerator.
- **The hero PNG's alpha still carries no information.** `--matte` is plumbed;
  `--backdrop headroom` falls back to the heuristic mask (67.76 % cover) and
  warns every run. A real matte needs a File Output tap in `studio.py`.
- The hubcap RING is absent. `t1_core.vw_bars`' air-gap docstring is false. The
  tail lamp's lens hue needs its own material slot — `amber` is shared with the
  front indicator. `flank_compare.py` still FAILS 3 of 4 with the ink sitting
  +95 mm below the panel top.
- **Parked deliberately:** tyre deflection (real at 23–32 mm, unauthorable in an
  axisymmetric revolve, trips `TYRE_D`). **Logged not applied:** the serving
  bays may be glazed — contradicts a reading he settled himself.

## 5. FIRST QUESTION FOR THE OWNER
Same frame as rev 16 asked for, and it is now worth MORE, not less: **a head-on
rear (or front) elevation from roof height or above, with the counter and lids
clear of the section.** rev 16 built the roof section from two heights plus an
assumed parabola — `D = 0.2128` is measured, but the split between the shoulder
roll `RT` and the crown `CR` is **not determined by any frame we hold**, and
neither is the flat tail panel's height. A head-on elevation settles both
directly and carries no fore-aft perspective term.
The open-web search returned a clean negative at rank 1–4 but recovered ~12
**unverified** direct image URLs it could not look at. **A vision-capable pass
over that specific list is cheap and is the first thing to try.**

## 6. Ordered work list for rev 17 — the backlog the loft was blocking
1. **The cream detail map.** §4's first bullet. A real 10–40 mm map into albedo
   AND roughness, measured with `cream_rms.py`. **Ablate to zero first.**
2. **`COUNTERTAN`'s interreflection test** — one render, fascia hidden from the
   top's diffuse bounce.
3. **The real matte** — File Output tap in `studio.py`; `--matte` is waiting.
4. **Detail geometry left over:** hubcap ring; tail-lamp material slot split
   from `amber`; `flank_compare.py`'s +95 mm ink offset.
5. **Re-run `flank_compare.py` and the galley bay measurements** — both were
   measured against a shell whose tail, arch and roof have all just moved, so
   their windows need re-deriving before their numbers mean anything again.
6. **A fresh adversarial audit of the loft.** It is new geometry and it has only
   been checked by its own author. Spawn 3–4 `Agent`s on disjoint files.
7. Camera absolutely last — re-framing invalidates every hero-pixel measurement.

**`t1_shell.py`'s import-time assertion exists because a shut line crossing an
arch lip collapsed the shell 205 562 v → 12 v for six revisions.** Respect it.
If a change trips a guard, do not widen the guard.
