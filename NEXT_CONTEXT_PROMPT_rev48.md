# NEXT CONTEXT PROMPT — rev 48

**Read this whole file before you touch anything.** It is written for a context that knows nothing
about this project. Everything you need to start is here; everything you need to be *correct* is in
`SPEC.md`, `LEDGER_rev47.md` and `LEDGER_rev46.md`, and this file says where to look.

---

## §0. WHAT HE SAID, AND WHAT IS LEFT

| his words | state |
|---|---|
| "100% calidad off center" | **FIXED** at rev 46, guarded, guard watched fail. |
| "the vw logo wrong" | **FIXED** at rev 46. Residual 0.1167 → 0.0347, at the photograph's noise floor. |
| "señor Tacombi still isn't clearer" | **BLUR FIXED** at rev 47 (edge/stroke 0.0924 → 0.0062). **CONTRAST HALF STILL OPEN and gated on W6.** |
| "the bottom word does not collide with the top one either" | **FIXED at rev 47b**, and only after he repeated it. See §1. |
| "It still does not read as two separate words" | **FIXED** — `LINE_GAP` 0.26 → 0.43, ratio-measured off `IMG_2073.jpeg`. |
| "the nose of the car is too flat" | **CONFIRMED, NOT FIXED, still no photographed anchor.** See §3. |
| "we're going to need the trunk open like it's in service" | **NOT STARTED. YOUR SECOND JOB.** See §2. |
| "I only meant to use that bus as a reference for the level of detail" | **`bus_model_ref.JPG` IS A FIDELITY BAR, NOT A VEHICLE REFERENCE.** See §5. |
| "the lettering looks off as well" | **STILL NOT EVALUABLE** — 4 px letters even in the new frame. |

> **RULE 21 — HIS REPEAT IS A MEASUREMENT, AND AT REV 47 IT FIRED ON THE ASSISTANT.**
> Rev 47 opened the word gap until the two words shared **zero pixels**, measured it, looked at it,
> and shipped it. He looked at the same picture and said it still did not read as two words. **He was
> right.** Zero shared pixels is **clearance**; he was reporting **legibility**. They are different
> quantities and rev 47 substituted one for the other. **When he repeats a report, do not re-measure
> the axis you already measured — find the one you did not.**

---

## §1. START HERE — THE MACHINE, AND PROVING IT

```bash
cd /home/user/combi_render
./bootstrap.sh            # toolchain + tree.  ~1 min warm, ~6 min cold.  ALL 10 PASS
./bootstrap.sh --guards   # ... and both builds and the probes.  ~10 min more.
```

`bootstrap.sh` installs Blender **as `bpy` from PyPI** and writes two shims at `/tmp/blender`. **The
`pip install bpy==4.5.3` branch, which had never been exercised, ran clean on a cold container at
rev 47** — that caveat in its header is now discharged.

If `verify_clone.sh` fails on **`commits >= 227 → got short:114`**, that is a **shallow clone**, and
the script says so in its own output. `git fetch --unshallow`, re-run. **Do not edit the script.**

### THE BRANCH — AND DO NOT TRANSCRIBE AN AHEAD-COUNT

```
branch   claude/combi-render-rev46-t8vhpm
```

**Rev 47's brief told it to check out a branch and expect an ahead-count of 5. Both were stale.** The
five commits had already merged to `main` via PR #5, the real count was **1**, and — the part that
matters — **`main` carried an owner upload the named branch did not have** (`bus_model_ref.JPG`). A
context obeying the instruction literally would have silently lost owner-supplied material.

**So: `git fetch --all` and CHECK the merge state; never trust a number written in prose.** He pushes
photographs straight to `main` from the GitHub web UI, mid-revision, without saying so. **Fetch
`main` at the start of every work session and diff it against your branch.** Rev 47 found two owner
uploads that way, one of which reset an entire work item.

```bash
git fetch --all
git diff --name-only HEAD...origin/main     # <- owner uploads land here
git rev-list --count origin/main..HEAD      # measure it, do not assume it
```

---

## §2. YOUR FIRST TWO JOBS

### JOB 1 — THE TRUNK OPEN, IN SERVICE *(his newest requirement, not started)*

> *"we're going to need the trunk open like it's in service"*

**What is known, and it is not much:**

* `t1_shell.roof_lids()` (line 1241) builds the **roof** lids and they **are** already modelled open
  and served — `audit.py` §87 records `lid_strut0` spanning z 1.8994–3.0169.
* `t1_shell.engine_lid_gap()` (line 994) cuts the **trunk/engine lid** as a **seam in the body**. It
  appears **not** to be an openable part.
* `lid_gen.py` §1 states the settled topology: **"There are two roof lids plus a trunk lid."**

**CONFIRM THAT AGAINST THE BUILD BEFORE YOU BELIEVE IT.** §9 lists a trap where two separate contexts
"fixed" the sign props' inset by reading the source and both were wrong. **Run the build and look.**

**`IMG_2073.jpeg` is the pose reference** — it shows the vehicle in service, roof lids up on visible
struts with lit strip lighting along the lid edge. **It does not show the trunk open.** Hinge side,
open angle, strut vs counterbalance, and what the inner face carries are **all unmeasured**
(`PHOTOS_WANTED_rev47.md` #3).

**The bar is §5's**: this is bodywork with depth that self-shadows, not a painted seam.

### JOB 2 — THE REAR VENT SLATS *(geometry the model does not have at all)*

`grep -rniE 'vent|louvre|louver|slat|intake'` over every source returns the cab quarter-light and the
studio lighting rig **and nothing else**. Rev 46 retired the painted fakes at his instruction and
**nothing replaced them.**

**What rev 47 measured from `IMG_2073.jpeg`, and what it refused to:**

* **Pitch: 8.02 ± 0.42 native px** — regular to 5 %. Real.
* **COUNT: NOT SETTLED, NOT PUBLISHED.** A bounded detector found **6** in a 50-px crop that may not
  span the panel; the eye reads **~10** on the same crop. **Bound the panel first, then count.** Do
  not inherit either number.
* **They are BODY COLOUR, not dark grey.** `LEDGER_rev46.md` §5 read them as dark grey from a frame
  where only the shadow survived. **Corrected at rev 47** — they are the same green as the panel and
  read dark because each pressed slot **self-shadows**. That is *why* they must be geometry.

---

## §3. W4 — the nose is flat, and it STILL has no photographed anchor

Raycast against the built body at z = 1.25, mm behind the centreline crown:

```
    y=0.00   0.10   0.20   0.30   0.40   0.50   0.60   0.70
      0.0   -0.4   -1.6   -3.6   -6.5  -10.2  -12.9  -14.3
```

**14.3 mm over 0.70 m of half-width — a plane.** The only forward bulge in the model is one constant,
`bulge = 0.019` in `t1_shell.nose_shape`. *(Rev 47 did not independently re-verify that it is the
only one — that check is still owed.)*

> **THE TRAP.** Ledger finding 6, *"the nose shape, `V_POW` locked 0.60"*, is a **different axis**.
> `V_POW_Z` drives the **painted** two-tone break line's height. It is a paint curve.
> `verify_clone` locks it at 0.60 for a reason.

**THE MEASUREMENT TASK REV 46 DISPATCHED DOES NOT EXIST. Rev 47 checked exhaustively so you do not
have to** — every commit on every ref, every tracked and untracked file, `/tmp`, and the content of
every `.md`/`.json`/`.py`. Every hit is a restatement of the open problem.

**The pixel budget, measured at rev 47, so nobody re-derives it:**

| frame | nose face | the problem |
|---|---|---|
| `ref_workshop.jpg` 1200×824 | **~240 px** | flat overhead fluorescent — almost no directional falloff. **But its silhouette is the sharpest in the set.** |
| `ref_nolita_front34.jpg` 700×467 | ~165 px | red channel **clipped**, near lamp **blooming** over ~78 px, a child's head occluding the lower quarter |
| everything else | ≤110 px | ~15 mm/px or worse |

**METHOD 2 — silhouette corner-wrap on `ref_workshop.jpg` — IS THE LIVE ONE**, because it is the one
that does not care about lighting. Rev 45's shading-gradient attempt was thrown away because the
render and photograph boxes were not comparable; if you go that route, **choose the render's box by
PROJECTING the same 3-D band through the render camera, never by typing it.**

**Whatever you build, watch a control fail on it:** a rendered flat panel and a rendered domed panel
must give different numbers, **or the estimator is blind.**

---

## §4. THE DECAL — four defects now visible, none yet measurable

`IMG_2073.jpeg` shows the burst at **44 × 61 px** against `ref_playa_34.png`'s 23 × 39. That was
enough for the word gap and **not** enough for these four, all of which were invisible before:

1. **The spikes.** Photograph: **many short, fine, near-uniform needles** on a nearly circular core.
   Build: **~20 long, broad, irregular** spikes. A different character, not a different tuning.
2. **The burst colour.** Photograph: fairly **uniform deep crimson**. Build: a strong
   **RED → ORANGE → YELLOW** gradient.
3. **The stars.** Photograph: **several small magenta stars scattered around the decal**. Build: one.
4. **The type fills too much of the burst** — the photograph leaves a clear red margin all round.

**Do not tune any of these by eye against a 44-px frame.** They are `PHOTOS_WANTED_rev47.md` #2.

---

## §5. THE STANDARD HE SET — and it is a level of detail, not a shape

He uploaded `bus_model_ref.JPG` (an American yellow school bus, a studio 3-D render) and then said:

> *"I only meant to use that bus as a reference for the level of detail"*
> *"Use the clarity in the workshop photo too to inform you"*

**It is a FIDELITY BAR. Nothing about the T1's geometry, paint or proportions may be taken from it.**
What it *does* set is the standard: crisp panel edges, and **small features carried as real geometry
with depth rather than as paint** — its own nose louvres are modelled slots that self-shadow. **That
is the bar for Jobs 1 and 2.** `ref_workshop.jpg` is the photographic half of the same instruction.

---

## §6. THIS MACHINE

```
cores 4   RAM 15 GB   Blender 4.5.3 via pip install bpy
build  T1_SUB=1  ~20 s        build  T1_SUB=2  ~75-100 s   <- the GUARDED case
script_gen.py ~22 s           cal_gen.py ~48 s
render 1600x1100  96 spp  ~3 m 40 s PER VIEW
```

```bash
/tmp/blender/blender -b -P build.py                      # T1_SUB defaults to 2
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py  # -> "VERIFY: 0 fail, 0 warn"
T1_PREVIEW=side T1_PFX=r48 T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
  /tmp/blender/blender -b -P build.py
```

**There is no view called `hero`.** The keys are `hero34f`, `hero34r`, `front34`, `side`, `front`,
`rear`, `detail_f`, `low34`, `topdown`, `playa`, `playa_ref`, `playa_w`, `counter`.

**Network:** `WebSearch` works. `WebFetch` and `curl` are 403 on every domain except
`raw.githubusercontent.com`.

---

## §7. HOW TO USE YOUR PARALLELISM — and he has asked you to use it hard

**He has explicitly asked the next context to use large, complex workflows to finish this vehicle.**
Take that seriously, and take one rule with it that survives every box:

> **DO NOT FAN OUT BLENDER.** Cycles already uses all four cores. Two instances make both slower.

**Fan out everything that is not a render.** Renders go in the background while you analyse in the
foreground; an 8-minute render should never be 8 minutes of idle.

A shape that fits this project, given Jobs 1 and 2 are independent geometry:

* **Phase 1 — understand, in parallel.** One agent maps `t1_shell`'s lid topology against the *built*
  scene; one inventories every frame that shows the rear panel; one re-verifies the claims in §3 and
  §4 of this file against the machine. **They must not render.**
* **Phase 2 — build, serially.** Geometry lands one change at a time, each with `T1_VERIFY=1` and its
  guard **in the same edit**.
* **Phase 3 — verify, adversarially and in parallel.** Every finding goes to verifiers **instructed
  to REFUTE it**, with distinct lenses (does the control fail on the defect? does the estimator track
  a known displacement? is the ratio right for the wrong reason?). A finding that survives three
  hostile readers is worth shipping; one that survives its author is not.

**AND FINISH WHAT YOU DISPATCH.** Rev 46 recorded a revision with a measurement task outstanding and
it never returned — §3 above is what that cost, a whole revision later. **Rev 47 repeated the mistake
in miniature**: it dispatched an adversarial audit of its own brief and closed before it reported.
**If a task has not returned, say so in the ledger and say what you verified by hand instead.**

---

## §8. THE THING THAT OUTRANKS EVERY ITEM ABOVE

**This project measures beautifully and its instruments keep being wrong.** Rev 46 caught five. **Rev
47 caught four more, three of them its own, and every one produced a plausible number:**

* **A calibration harness that broke its own estimator's validity regime.** 60-px bars blurred to
  σ = 20 never reach α 0.9 at the bar's centre, so the whole bar counted as "band" and the estimator
  over-reported by 26 %, then 44 %. **The harness was wrong, not the estimator.** Fixed, and a
  control now **watches the break happen**.
* **"The built strokes are too fat" — a 7.9 σ defect that was not there.** The EDT stroke estimator
  carries a **16.6 % resolution bias** across a 15× gap. At the photograph's own 271 px: built
  0.04317 vs photo 0.04414 ± 0.00090, **1.1 σ.** *(Rev 46 had the identical illusion about the VW
  glyph. It is the third time. Expect it a fourth.)*
* **"42 % of the type sits outside the burst"** — a hole-filling artefact; the type meets the burst
  boundary so its counters are not enclosed regions.
* **A word-gap estimator that reported a 0.75 px cap height at 102°** because it took a two-word
  block's **principal axis** as the reading angle.

> **§10.116.6 — AN INSTRUMENT THAT HAS NEVER BEEN WRONG HAS NEVER BEEN TESTED.**
> **§10.115.4 — A CONTROL IS NOT FINISHED WHEN IT PASSES. IT IS FINISHED WHEN YOU HAVE WATCHED IT
> FAIL ON THE DEFECT.**
> **§10.110.8 — A PART MEASURED IN ISOLATION FROM WHAT IT IS FITTED TO IS NOT MEASURED** — and rev 47
> adds: **including from the RESOLUTION it is compared at.**

**The two cheapest defences, both of which paid at rev 47:**

* **Calibrate against a known answer at the real data's resolution.** Run your estimator on the
  *build*, where the truth is set by construction, downsampled to the *photograph's* size. That is
  how the word gap became quotable.
* **QUOTE THE RATIO, NOT THE READING.** The word-gap estimator has a +34 % absolute bias. It divides
  out of a ratio and does not divide out of a reading. **Photographed ÷ built, on the identical
  instrument, at the identical scale.**

**And: render it, crop it, and LOOK at it, before and after every change.** Every real finding at
rev 46 and rev 47 came from looking at an image. The blur, the colliding words, the vent slats' true
colour and all four new decal defects were invisible in the metrics and obvious on screen.

---

## §9. SETTLED — DO NOT RE-OPEN

* **The paint's *finish*.** §10.104.8 refuses it in writing. W6 is about the **studio**, not the finish.
* **Finding 29** — "the red renders 2× too light" — retracted, a unit error.
* **`T1_CATCH=0`** — refused at rev 12, re-refused at rev 45 with numbers.
* **The rear bumper was removed after the conversion**; the over-rider bar and posts were withdrawn
  by the owner at rev 37. **There is no fourth serving bay.**
* **The sign props' `LID_X1 + 0.16` / `LID_X0 - 0.16` is an INSET.** Two contexts have "fixed" this
  and both were wrong. **Run the build before you believe the source.**
* **The Calidad decal PANEL's placement on the vehicle** (Report 7) — closed at rev 44. The *type's*
  placement within the decal (rev 46) and the *word gap* (rev 47b) are different things.
* **The bunting pennants** — retired at rev 46 at his instruction, guarded by absence three ways.
* **`probe_rev46_reports.py` IS PARTLY RETRACTED** and must be rebuilt before it is quoted. Its R1
  photographed target is withdrawn and its estimator is the blind one; its R2 target line carries a
  transcription error corrected in `LEDGER_rev46.md` §2. **`probe_rev46_vw.py` is the model to copy**
  — it identifies landmarks by structure and carries a kill control that is red by design.

---

## §10. STILL BLOCKED ON HIM

* **W5 — the sign board.** The build paints a flower mural with menu strips; every frame shows a
  hand-chalked **blackboard**. `IMG_2073.jpeg` shows a chalked board on a **post beside** the
  vehicle — evidence about such boards, **not** about the vehicle's own raised lid. **Nobody has ever
  asked him which he wants.** Ask.
* **W6 — the paint and the studio.** Body red G/R 0.455 built vs 0.223 ± 0.066 photographed
  (**3.5 σ**); hubcap red 3.4 σ; cream right to 0.4 σ. **ONE finding, not three.** About half the
  excess is the white cyclorama's own specular (`T1_SPEC=0` moves it 0.455 → 0.347), and softening it
  trades the catalogue-clean white background he supplied as the bar. **His call — and it gates the
  rest of W3**, because the script's remaining contrast shortfall is the ground being 11 % too
  bright, not the ink.

---

## §11. THE RULES. EVERY ONE WAS EARNED BY A DEFECT.

1. **A claim in prose is not a guard** (§10.45).
2. **A constant tuned against another constant must be EXPRESSED in terms of it** (§10.25) — and rev 47
   adds: **expressed is not enough if it is expressed against a FROZEN measurement. Derive it at run
   time.** `TYPE_SHIFT` is now computed from the actual laid-out type.
3. **Read each probe's own summary line, never its exit code.**
4. **Never put a figure in an acceptance test unless you watched it print** (rev 13).
5. **Do not inherit a guard's rationale along with its shape** (rev 23). Rev 47 restated two
   `verify_clone` rows on exactly this ground.
6. **An ordinal fact licenses a SIGN, never a SHAPE** (§10.102.8).
7. **A leading question is not evidence, even when the answer is yes** (§10.102.8).
8. **A measurement's window is part of the measurement** (§10.106.6).
9. **A threshold "lowest X" trace is only valid if the feature's FAR SIDE is resolved** (§10.106.7).
10. **A detail you cannot see is not a detail** (§10.105.7) — **and a detail you looked at badly is
    not looked at** (§10.115.4).
11. **When a fix cannot be built at any tolerance, suspect the thing it is fixing** (§10.102.8).
12. **Add the guard in the same edit as the change.**
13. **Inventory the frames you already hold before asking him for a new one.**
14. **Prefer dimensionless measurements** (§10.106.3).
15. **Retract in the same revision you find the error** — in SPEC, in the ledger, and to him.
16. **A PART MEASURED IN ISOLATION FROM WHAT IT IS FITTED TO IS NOT MEASURED** (§10.110.8).
17. **A REVISION THAT IS NOT MERGED DID NOT HAPPEN** (§10.113.5) — **and an ahead-count written into
    prose has an expiry date. Measure the merge state; never transcribe it** (rev 47).
18. **A RATIO THAT IS RIGHT FOR THE WRONG REASON IS NOT A CONTROL** (§10.111.2).
19. **A CONTROL IS NOT FINISHED WHEN IT PASSES. IT IS FINISHED WHEN YOU HAVE WATCHED IT FAIL ON THE
    DEFECT** (§10.115.4).
20. **AN INSTRUMENT THAT HAS NEVER BEEN WRONG HAS NEVER BEEN TESTED** (§10.116.6).
21. **HIS REPEAT IS A MEASUREMENT** (rev 46) — **and when it repeats, the axis you already measured
    is not the axis he is reporting** (rev 47).
22. **CALIBRATE AGAINST A KNOWN DISPLACEMENT, AT THE REAL DATA'S RESOLUTION** (rev 47).
23. **A HORIZONTAL OVER A HORIZONTAL AT THE SAME ROW NEEDS NO AXIS RATIO** (rev 47).
24. **NEW, rev 48 — QUOTE THE RATIO, NOT THE READING.** When an estimator carries an absolute bias,
    run it on the build *and* the photograph at the same scale and quote photographed ÷ built. The
    bias divides out. This is what made the word gap quotable after two revisions had refused it.
25. **NEW, rev 48 — CLEARANCE IS NOT LEGIBILITY.** Proving that two things do not overlap does not
    prove they read as two things. **Check that the quantity you measured is the quantity he
    reported.**

---

## §12. THE STATE OF THE MACHINE AT HANDOFF

```
bootstrap.sh      ALL 10 PASS   (the pip install bpy branch is now exercised)
verify_clone.sh   ALL 86 PASS   (83 at rev 46; three rows added, three re-based)
build             T1_SUB=1  VERIFY: 0 fail, 0 warn
probes            probe_rev47_sharp   9 checked, 0 FAILED  (C4 KILL; C6, C7 WATCHED-FAIL)
                  probe_rev47_gap     3 checked, 0 FAILED  (C3 KILL, refuses rather than invents)
                  probe_rev46_vw      5 checked, 0 FAILED  (C3 a KILL, red by design)
                  probe_rev46_reports PARTLY RETRACTED -- do not quote
render            out/r47_side.png  1600x1100  96 spp
new frames        IMG_2073.jpeg   1400x933  <- the best frame in the project
                  bus_model_ref.JPG        <- a FIDELITY BAR, not a T1
branch            claude/combi-render-rev46-t8vhpm
```

**A DISPATCHED TASK THAT DID NOT RETURN.** Rev 47 set an adversarial agent on its own brief to refute
it and **closed before it reported**. Its claim list is `LEDGER_rev47.md` §1c — **every row marked ✔
there was verified by hand and stands on its own.** The one row it was to check and rev 47 did **not**
verify independently: **`bulge = 0.019` being the only forward bulge constant in the model.** Check
it before you build on it.

**`git rev-list --count origin/main..HEAD` before you start and again before you finish. And
`git diff --name-only HEAD...origin/main` — that is where his photographs arrive.**
