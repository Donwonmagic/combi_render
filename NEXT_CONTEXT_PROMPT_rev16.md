# NEXT CONTEXT PROMPT — rev 16

Please act as my expert. Continue the Señor Tacombi combi build. **Fifteen
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
`shader_solve.py` and `post.py`'s exact backdrop flood both need them.
Report the guards' ACTUAL output. Both levels, every time.

## Step 4 — read, in this order

`STATE.md` → `SPEC.md` §10, then §10.9 through §10.33 → this file →
`HANDOFF_rev15.md` → `LOFT_GROUND_rev15.md` → `AUDIT_rev12.md` →
`AUDIT_rev11.md` → `SKEPTIC_PASS.md` → `REF_MEASUREMENTS.md`.

`STATE.md` is machine-written by `audit.py` from the mesh built in the same
process. **If it and any prose disagree, it is right.**

**§10.29 carries two corrections that touch every REF number.**
`REF_MEASUREMENTS`'s model-frame column is **100 mm aft of where it says**, and
`RULES §4`'s 194.8 px/m at the rear panel is refuted **in sign** — it measures
225 ± 3. rev 15 adds a third: **`REF_MEASUREMENTS` §0.2's "parallel, VP at
−98 000" is refuted** — the flank map is projective with `u_vp ≈ −11 140`,
predicting 211.2 px/m mid-body and 226.9 at the tail.

## Step 5 — ASK ME WHAT THE PHOTOGRAPHS SHOW before you measure from them

This has now paid off seven times. **And my answers are not infallible — ask me
anyway, then measure what I say.** Show me a crop, mark the regions, give me
options. And check your own crop is where you think it is: rev 14's tail-face
box was 120 px off and I answered it correctly while the box was wrong.

**FIRST QUESTION FOR ME:** §5 below — the loft is the whole of rev 16 and there
is one photograph that would change how it is done.

## Step 6 — the work

§6 below is the ordered list. **Rev 16 is the loft.** It is one job, it is
scheduled last for a reason, and it must be done jointly.

## Step 7 — resolution

rev 13 shipped 3600×2400; rev 15 went to **4320×2880 in 18 strips**, worst seam
z 2.75. Go higher again if the loft lands. Drive `hero.py --only N` one strip
per call then `--stitch-only`; run `post.py` **once** on the stitched frame,
never per strip. Middle strips take ~5 min each at 4320×2880 — budget for it.

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
two panes**. **Nolita photographs are admissible FOR GEOMETRY ONLY** (settled
rev 15) — livery, weathering and artwork stay locked to my three photographs,
and every Nolita-derived number must be TAGGED in SPEC. **SPEC §6's pure-white
backdrop lock is RETIRED** — `--backdrop headroom` is the default (settled
rev 15). Never correct this vehicle toward the VW factory catalogue.

## Hard-won rules — every one was learned by breaking it

* Never set a vertical position from the ground line (~70 mm common-mode).
* A single linear px→metre scale does not hold along the flank.
* **An image slope of a fore-aft line is not a rake** — that cost five revisions.
* A rendered ratio is only an albedo ratio between two surfaces of the **same
  class** under the same light — paint-to-paint, not paint-to-plywood.
* A constant tuned against another constant must be expressed in terms of it.
* **A claim in prose is not a guard.** Grep for the node that does it.
* **Check what a guard, or a probe, or a crop can physically SEE** — and print
  the crop box. rev 15 measured the cream lid skin *through* the mural board
  because the mask was isolated and the render was not.
* **A guard can be strengthened instead of widened.**
* **A negative control turns a number into a measurement.**
* **NEW, rev 15 — before scheduling a solve, ABLATE THE CONSTANT TO ZERO.** If
  the ablated arm equals the shipped arm, the constant is not the parameter and
  no amount of solving will make it one. This would have saved three revisions
  on `W_ALBEDO`.
* **NEW, rev 15 — a restore check that only greps THIS revision's strings
  cannot detect a lost ANCESTOR.** rev 14's seven checks all passed while a
  whole rev-13 commit was missing. Always assert something the PREVIOUS line
  added.
* **Do not put a figure in an acceptance test unless you watched it print.**
* When a finding breaks something independently locked, measure it a third way
  before choosing — and if you must apply it, apply it so the lock survives.
* **A specialist that refutes its own brief is working correctly.**
* **Watch for the lamppost** — `ref_side.jpg` columns 62–79 have produced three
  separate confident wrong numbers about the front of the vehicle.
* A single shell command is killed at 10 minutes; `nohup`/`setsid`/`disown` all
  fail. This box has 2 CPU cores — spawn 3–4 `Agent`s on **disjoint files**
  rather than running a Workflow. rev 15 ran three at once successfully.

---

> **THE STANDARD, in the owner's words, and it governs every line below.**
> The final product should be nearly indistinguishable from the original.
> **Any single measurement off is unacceptable.** We are recreating a photo
> realistic version of **that exact bus** — not a 1963 T1, not a generic
> taqueria combi. The criterion is PER-MEASUREMENT, not on average: a model
> right in ninety places and wrong in one is not 99 % done, it is wrong,
> because he will look straight at the one.
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
git pull --ff-only ../tacombi_rev15_incremental.bundle HEAD      # -> 66 commits, clean
```

**The middle line is a `fetch`, not a `pull`, and that is the whole point of
10.33.** The rev-14 line is DIVERGENT from the rev-13 tip, so pulling it merges
or errors; fetching it into a branch makes its commits available, and the rev-15
bundle carries the merge that reconciles them. Verified end to end from a fresh
rev9 clone: clean tree, 66 commits, guards 0 fail / 1 warn.

**If a pull says "Need to specify how to reconcile divergent branches", STOP.**
That is not a config nuisance — it is how rev 15 discovered that the rev-14 line
had lost a whole rev-13 commit. Fetch the bundle into a branch and test ancestry
before merging anything.

Then all of these must be true:

```bash
git status                                       # clean
grep -c '### 10.33' SPEC.md                      # 1
grep -c '### 10.30b' SPEC.md                     # 1   <-- ANCESTOR CHECK (rev 14)
grep -c 'The threshold is not the parameter' post.py  # 1   <-- ANCESTOR CHECK (rev 13)
grep -c _isTail t1_mats.py                       # non-zero
grep -c 'BACKDROP = "headroom"' post.py          # 1
grep -c T1_CTAN_SP t1_mats.py                    # non-zero
ls shader_solve.py cream_rms.py LOFT_GROUND_rev15.md AUDIT_rev11.md AUDIT_rev12.md
```

## 2. Both guards, and the figures I watched print

| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 1 warn** | **0 fail, 1 warn** |
| warn | roof crown @ rear axle (dome-corrected) **1.992** vs spec 1.960 (**+32 mm**) | **1.993** (**+33 mm**) |
| dims | roof@rear-axle **1.894**, raw resid **−66 mm**, `DOME_DEFICIT` **+98 mm** | 1.895, −65 mm, +98 mm |
| cut roof hole | **56293v** | **207383v** |

Also: `roof aperture: open, and solid fore / aft / both sides`; `TYRE_D=0.6650`;
3 open apertures on +Y; four shut lines `100 % open`; band `1.372–1.775`; bay
widths **`0.516 0.515 0.516`**; **181 meshes**; **0 non-manifold edges**;
**5 materials constant-rough**; 42 distinct materials.
`cutters rolled back | none` is a **STATE.md row**, not a console print.

## 3. What rev 15 changed — see `HANDOFF_rev15.md` for the full table

Detail geometry applied at 6.6–14σ (rim, glyph, hubcap emblem, T-handle, plate
aspect, tail lamp). Per-bay galley: bay 2's gap 4.64 → 0.73, bay 3 moved toward
the photograph. Glass brief REFUTED, no rig change. Four solves returned "the
constant is not the parameter". One dead-argument bug fixed. Hero at 4320×2880.
Backdrop lock retired by the owner.

**Two things rev 15 changed that you must not silently undo:**

- `post.py` now defaults to `bloom = 0.0` and `BACKDROP = "headroom"`. Both are
  measurements plus an owner decision, not preferences.
- `t1_mats.py`'s `countertan` finish numbers live in `counter_tan()`, not in
  `build_all()`. `simple()` resolves by name and `counter_tan()` runs first.

## 4. Still open, and now with numbers

- **The cream is 26× too uniform at 25 mm** (0.339 % against a photograph
  re-measured at 8.890 %) and `W_ALBEDO` cannot fix it — its zero-ablation reads
  the same. The fix is a real detail map at the 10–40 mm scale driven into
  albedo AND roughness, measured with `cream_rms.py`, which is now calibrated.
- **`COUNTERTAN` is 6.8σ / 2.0σ / 5.2σ out** and albedo has a gain of only
  0.33–0.49. Next test, one render: hide the fascia from the top's diffuse
  bounce to see whether interreflection is moving the denominator with the
  numerator.
- **The hero PNG's alpha still carries no information.** `--matte` is plumbed
  and waiting; `--backdrop headroom` is currently falling back to the heuristic
  mask (67.76 % cover) and warns about it every run. A real matte needs a File
  Output tap in `studio.py`.
- The hubcap RING is absent. `t1_core.vw_bars`' air-gap docstring is false. The
  tail lamp's lens hue needs its own material slot — `amber` is shared with the
  front indicator. `flank_compare.py` still FAILS 3 of 4 with the ink sitting
  +95 mm below the panel top.
- **Parked deliberately:** tyre deflection (real at 23–32 mm, unauthorable in an
  axisymmetric revolve, trips `TYRE_D`). **Logged not applied:** the serving
  bays may be glazed — contradicts a reading he settled himself.

## 5. FIRST QUESTION FOR THE OWNER

`LOFT_GROUND_rev15.md` names the one photograph that would change how rev 16 is
done: **a head-on rear (or front) elevation from roof height or above, with the
counter and lids clear of the section.** It is the only frame that measures the
transverse roof section directly, it gives `Yt` — which the crown radius goes as
the *square* of — it shows the full tail panel whose height rev 15 could not
settle because the counter occludes exactly that band, and being head-on it
carries no fore-aft perspective term at all.

He has now admitted **Nolita photographs for geometry**. Put it to him: does a
Nolita head-on rear elevation exist that he can supply or point at? Everything
in §6 gets more accurate with it, and the crown radius in particular is
currently pinned by one route only.

## 6. Ordered work list for rev 16 — THIS IS THE LOFT, AND IT IS ONE JOB

The loft was scheduled last across four revisions precisely so that nothing
after it would invalidate what came before. It is now first, and it is
everything. Do it in this order, in ONE rebuild, and re-run both guards after.

1. **Roof crown + rake + roof EDGE, jointly.** The system is over-determined and
   rev 15 found it does not currently close. Use the joint solution:
   **D = 0.2116 ± 0.035, R = 1.84 ± 0.30, `ZT_ALL(−1.100)` down 63 mm, rake
   unchanged at 17.75.** **`R = 2.45 ± 0.15` is REFUTED twice — do not use it**
   (it puts the crown 39 mm below spec AND below the roof's own photographed
   silhouette; **R ≤ 2.06 m**). Note the roof EDGE finding is new: the model's
   gutter is 63 ± 20 mm too HIGH and the dome was carrying the blame.
   `DOME_DEFICIT` must reach **0** and the warn must clear.
2. **The rear arch as a flat-crowned ogee.** Confirmed by fit (superellipse rms
   2.67 mm vs a circle's 11.4). Use the normalised profile table in
   `LOFT_GROUND_rev15.md`, **not** the exponent — it is window-dependent
   (3.50–4.28) and 3.9 ± 0.2 is reproduced only at one particular window.
   Width **0.92 ± 0.03 m** against 0.747 built; the crown is centred on the rear
   axle to ~1 mm; `ARCH_R` is already right, the shape is not.
3. **The tail, LAST, as a re-spaced aft station set — never a translation.**
   **235 ± 22 mm too long**, dimensionless and lamppost-free; the old 99 mm is
   refuted at 10σ. Station fractions are tabulated in `LOFT_GROUND_rev15.md`
   against a named datum, deliberately not as metres from an origin whose
   definition has already moved once.
4. **The end-cap poles, IN THE SAME PASS as the tail.** `loft(cap_first/last)`
   makes a 110-gon and subsurf's face point is the pole; the n-gon cap also
   pulls the flat tail face 1.4 mm forward, so the pole stands proud. A verified
   **27×28 Coons grid cap** is specified (max valence 4, 8 valence-3 verts, 0
   non-manifold, +5 828 v) and leaves the boolean order strictly easier. **But
   `plate_1963` and `englid_handle` are anchored at −2.1070 to the artefact
   surface and would end up 1.0 mm inside the skin** — which is why 3 and 4 are
   one step.
5. Only then: the cream detail map (§4), `COUNTERTAN`'s interreflection test,
   the real matte, the hubcap ring, the tail-lamp material slot.
6. Camera absolutely last — re-framing invalidates every hero-pixel measurement.

**`t1_shell.py:286` carries an assertion that exists because a shut line
crossing an arch lip collapsed the shell 205 562 v → 12 v for six revisions.**
Respect it. If a change trips a guard, do not widen the guard.
