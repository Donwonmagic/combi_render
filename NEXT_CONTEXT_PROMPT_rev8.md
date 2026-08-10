# Prompt for the next context — paste this as the opening message

---

Continue the Señor Tacombi combi build. Eight revisions of history sit behind
this — you are picking up mid-stream, not starting. Several things here have
been got wrong more than once and the guards exist to stop it happening again.

## The goal, and the thing that keeps failing

The most advanced, highest-fidelity 3D model achievable of the Playa del Carmen
Tacombi combi — a 1963 VW Type 2 (T1) converted into a taqueria — delivered as
hero stills at 2400×1600 or better, indistinguishable from a photograph of the
real vehicle. The deliverable is **renders**, not an editable file.

Read this part carefully, because it reframes the brief. In my words:

> I really want this to give the person the opportunity to feel like they were
> on playa del carmen all those years ago. I want the owner to remember standing
> in the kombi, in this very picture that was provided. I want it to be so real
> it evokes emotion.

A white-studio still cannot do that — it removes the place. Deliver **both**: a
white-studio hero as the fidelity benchmark, and a warm Playa hero for the
memory. A `T1_SCENE=playa` rig exists and renders; it has not been art-directed.

**Eight revisions and no hero has ever landed.** Every context so far has spent
its budget on diagnosis and fixes and run out before rendering. `out/` holds
560–700 px probes only. The step order below is designed to break that pattern —
**follow it in order and do not reorder it.**

## Step 1 — read my memory before you read any code

`/areas/tacombi-combi-sticker.md` and `/preferences.md`. Three prior contexts
skipped them or could not see them; one cost half a day and produced the wrong
body type. In rev 8 those two files caught a live regression — a canvas ragtop
retired four revisions earlier that was still shipping — inside ten minutes.
**If you cannot read them, say so explicitly rather than quietly proceeding.**

## Step 2 — restore from the rev 8 bundle, not rev 7 and not a tarball

```bash
git clone tacombi_history_rev8.bundle tacombi
```

`HEAD` should be `a2f7eee`, 23 commits, clean tree. The repo also lives checked
out and current in my `tacombi_bus_render` folder.

## Step 3 — install Blender 4.5.3 and run BOTH guards. Report their actual output before proposing anything.

```bash
curl -fsSL -o b.tar.xz https://download.blender.org/release/Blender4.5/blender-4.5.3-linux-x64.tar.xz
tar -xf b.tar.xz && mv blender-4.5.3-linux-x64 /tmp/blender
cd tacombi
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=2 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=1 /tmp/blender/blender -b --python audit.py
```

Expect at **both** levels `0 fail, 1 warn`, the warn being
`roof @ rear axle 1.923 vs spec 1.960 (-37 mm)` — deliberate and logged, not a
defect to chase. Also `TYRE_D=0.6650`, 3 open apertures, four shut lines
`100 % open`, band `1.372–1.775` un-dropped, bay widths `0.507 0.516 0.525`,
**132 meshes**, 0 non-manifold edges, `cutters rolled back: none`. Anything else
means something regressed in transit — find out what before building on it.

Both levels, every time. "Guards green" was true only at SUB=1 for six revisions
while the production build silently lost both cab-door shut lines.

## Step 4 — read, in this order

`STATE.md` → `SPEC.md` **§10, then §10.9 and §10.10** (rev 8; they supersede §10
where they differ) → `SKEPTIC_PASS.md` → `HANDOFF_rev8.md` → `REF_MEASUREMENTS.md`.

`STATE.md` is machine-written by `audit.py` from the mesh built in the same
process, with the git SHA and a dirty-tree flag. **If it and any prose disagree,
it is right.**

## Step 5 — PROVE THE RENDER PIPELINE NOW, cheaply, before any other work

This is the step every previous context left to the end and never reached. The
strip machinery is committed and has **never been run end to end**.

At **1200×800**, render four strips with `T1_BORDER` `0.00,0.25` / `0.25,0.50` /
`0.50,0.75` / `0.75,1.00` and `T1_FX=0`, stitch them, then run `post.py` **once
on the stitched frame** — never per strip, optics band at the seams. Send me the
result. If the seams show, fix the stitch now, while a test frame costs minutes.

Measured on rev 8's box (**2 cores / 8 GB** — check yours, it varies):
`hero34f` at 700×470 / 20 samples took **32 s**. Scale from that. 2400×1600 at
64 samples is roughly **20 minutes per full frame**, so about 5 minutes per
strip. Budget that time before you spend it on analysis.

Background processes are reaped — `nohup`, `setsid` and `disown` all fail, and
three hero attempts were killed 25–30 s in. **Render synchronously, in strips.**

## Step 6 — finish the art reproduction pass

`SPEC.md` §10.10 is a **standing requirement, a hard bar not a preference**:

> Every painted element on this vehicle must be REPRODUCED from photographs of
> the actual combi. Not approximated. Not invented. Not derived from palette
> statistics.

The bar is that the owner recognises **his own vehicle**. §10.10 tables all eight
painted elements with source crops and current state. I scoped the pass to four;
two are done (mural `lid_gen.py`, paisley `folk_gen.py`), two are not:

**The script — I have already rejected this once.** Of the rev 8 probe I said
*"That script i see on the p9 hero is NOT it."* Crop `ref_side.jpg` at
`(300,470)-(620,570)` and magnify 5× before you write a line. It is fat, rounded,
late-1960s psychedelic display lettering in **silver** — not white, not gold.
"Señor" small and raised upper-left; "Tacombi" large. The capital **T** carries a
long ribbon swash sweeping back over "Señor". The **o, a, c and b have rolled
spiral counters** — an actual spiral wound inside each bowl. Strong thick/thin
contrast, bulbous terminals.

`sign_gen.py` already has `swash_T()`, `spiral()` and `counter_spirals()`. The
machinery exists and the output still does not look like the photograph. Treat
this as a **letterform** job: drive those primitives from control points read off
the crop, or build the glyphs as explicit outlines. **A system font with
flourishes bolted on is what is there now and it is what I rejected.**

Acceptance test, not self-review: render the flank, crop the script to the same
framing as the reference, and show me the two side by side at matched scale. If
the letterform skeleton, the swash path and the spiral counters do not line up,
it is not done.

**The Calidad decal — never started.** Crop `(735,295)-(860,390)`. A spiky
starburst with a red-orange → orange/yellow **gradient**, white **bold italic**
"100%" over "Calidad" set at about −20°, and **two red bunting bars with
triangular pennants above it** that are not modelled at all.

Batch all changes into one rebuild. Re-run both guards after.

## Step 7 — land the hero set properly

Full 2400×1600 or better, in strips, both scenes: the white studio for fidelity
and `T1_SCENE=playa` for the place. Art-direct the Playa rig against
`ref_side.jpg` — it is lit but not directed. Send them as they land.

## Step 8 — adversarially audit, then iterate

Roughly 23 high-value findings from `AUDIT_RECOVERED.md` remain open and have
never been through a skeptic pass. Also open: the tail is 99 mm long (model
−2.108, measured −2.007; loft change, the counter's `X1` moves with it); six
materials still report a constant roughness; and the rake-versus-arch-gap
contradiction in §10.9 is logged, not resolved. Do not stop at good enough.

## What is settled — do not re-derive it

`SPEC.md` §10 + §10.9 + §10.10 is canonical; `REF_MEASUREMENTS.md` holds the
working. Scale, ride height, **rake**, belt line, V-swage, aperture edges, tyre
and rim sizes, louvre block, counter, rear overhang, indicator type, roundel
colour and **lids-open** are measured or locked with stated method and error
bands. If you think one is wrong, re-derive it by a different method and show
both.

Already considered and rejected — do not re-open without new evidence:

- **"The tyre is 0.596–0.606 m, not 0.665."** Raised and rejected three times. It
  comes from taking the ground/shadow line as the tyre edge. 72 rays restricted
  to sectors silhouetted against deep arch shadow; ellipse axis ratio 0.984 kills
  the perspective escape; wheelbase/flange 5.46 ± 0.08 against 5.44 for a 16-inch
  and 5.77 for a 15-inch.
- **"Set `Z_BELT` from sill − 100 mm."** That launders the sill's error into the
  belt. Set each from its own measurement; let the 100 mm fall out as a *check*.
- **"Model the lids closed" / bring back the canvas ragtop.** I locked OPEN on
  2026-08-10. Both in-service photographs show them up; none shows it closed.
- **"Scan SPEC §0.2 for material names to build the retired-material ban list."**
  Tried in rev 8; it flags six *correct* materials, because every bullet reads
  "retired reading — correction" and the names appear on both sides.
- **"Raise the flank saturation to 0.816."** That is the paint's *albedo*
  saturation. No beauty pixel of a dielectric under a white softbox reaches it —
  the specular term is achromatic and additive. §10.9 has the decomposition and
  the falsification test.

## Mistakes already made more than once

**Correcting the vehicle toward the factory catalogue.** This is not a standard
1963 T1. rev 4 "corrected" the tyre to a factory 6.40-15 and zeroed the lowering;
both were wrong and rev 3 had them right. It runs 16-inch rims, ≈0.665 m tyres,
no rear bumper, sits 65 mm low at the reference station with ~1.9° of nose-down
rake, and its roof is cut into hinged lids. **Measure the vehicle, never assume
the catalogue.** A finding whose evidence is a factory blueprint — especially the
Samba one — used against a measurement from the actual vehicle is presumptively
refuted.

**Measuring the belt line aft of the counter.** On the serving flank the visible
cream/red edge is the counter fascia bottom at 1.082 m, not the paint break at
1.207 m. This produced a 6× error.

**Measuring body features on the cab door in `ref_side.jpg`.** That door is open,
swung ~55–60° on its front hinge. And **a man stands directly in front of the
front wheel** in that photograph — every rev 8 attempt to measure the front arch
locked onto his red shirt instead.

**Trusting a guard that works by naming things.** The canvas ragtop shipped for
three revisions after §0.2 retired it, because `verify.py` banned only the
retired materials someone had remembered to type.

## Hard constraints — every one was learned by breaking it

- **Three frames.** Geometry constants are un-dropped; shader constants in
  `t1_mats.py` are dropped / above-ground; `verify.py` runs after the drop
  (§10.1). And since rev 8 **the drop is a function of x** — use
  `t1_core.rake_drop(x)`, never the `RIDE_DROP` scalar, for any frame conversion.
- Pipeline order in `build.py`: subsurf applied before any boolean; wheel arches
  cut while the shell is still a closed solid; every other aperture cut after
  solidify.
- Do not remove the boolean rollback guard in `cut()` — strengthen it, never
  weaken it. The obvious digest does not work: EXACT re-tessellates n-gons even
  on a true no-op, so vertex-count equality is the only clean test.
- A panel-gap outline must not cross the lip of another aperture. The cab-door
  clearance against the front arch is **asserted at import** in `t1_shell` — if
  you change the rake or the arch, that assert is what stops the SUB=2 collapse
  returning.
- The body stays a single continuous nose-to-tail loft.
- Batch all changes into one rebuild — do not render between fixes.

## How I work

- Ground in the reference → build → adversarial audit → iterate. Never build
  before grounding. Never call it done off self-review.
- Report the measurement against the reference. **Never a self-assigned score.**
- Do not tell me anything is ready. Tell me what is fixed, what is still wrong,
  and what you measured.
- Keep visible cadence on long work and **send renders as they land**.
- Record every new locked decision in `SPEC.md` with a change-log entry, commit
  it, regenerate `STATE.md`, and write it back to my disk — the container is
  ephemeral and a restart has already killed one workflow mid-run. **Anything not
  on my disk does not exist.**
