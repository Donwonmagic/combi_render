# Prompt for the next context

Paste this as the opening message.

---

Continue the Señor Tacombi combi build. This is a running project with **eight**
revisions of history behind it — you are picking up mid-stream, not starting.
Several things here have been got wrong more than once and the guards exist to
stop it happening again.

## Goal

The most advanced, highest-fidelity 3D model achievable of the Playa del Carmen
Tacombi combi — a 1963 VW Type 2 (T1) converted into a taqueria — delivered as
hero stills at 2400×1600 or better. The bar is indistinguishable from a
photograph of the real vehicle. Deliverable is renders, not an editable file.

**And read this part carefully, because it reframes the brief.** In my words:

> I really want this to give the person the opportunity to feel like they were
> on playa del carmen all those years ago. I want the owner to remember standing
> in the kombi, in this very picture that was provided. I want it to be so real
> it evokes emotion.

A white-studio still cannot do that — it removes the place. Deliver **both**: the
white-studio hero as the fidelity benchmark, and a warm Playa hero for the
memory. A `T1_SCENE=playa` rig already exists and renders; it has not been
art-directed.

**No hero has landed yet, in eight revisions.** `out/` holds probes only.

## Do these in order. Do not skip step 1.

**1. Read my memory before you read any code.** `/areas/tacombi-combi-sticker.md`
and `/preferences.md`. Three prior contexts skipped or could not read them; one
cost half a day and produced the wrong body type, and in rev 8 those files
caught a live regression (a retired canvas ragtop still shipping) inside ten
minutes. If you cannot read them, say so explicitly rather than quietly
proceeding.

**2. Restore from the rev 8 bundle**, not rev 7 and not a tarball:

```bash
git clone tacombi_history_rev8.bundle tacombi
```

HEAD should be `c9d9ebc` or later. The repo also lives checked out and clean in my
`tacombi_bus_render` folder.

**3. Install Blender 4.5.3 and run BOTH guards. Report their actual output
before proposing anything.**

```bash
curl -fsSL -o b.tar.xz https://download.blender.org/release/Blender4.5/blender-4.5.3-linux-x64.tar.xz
tar -xf b.tar.xz && mv blender-4.5.3-linux-x64 /tmp/blender
cd tacombi
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=2 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=1 /tmp/blender/blender -b --python audit.py
```

Expect at **both** levels `0 fail, 1 warn`, the warn being
`roof @ rear axle 1.923 vs spec 1.960 (-37 mm)` — deliberate and logged. Also
`TYRE_D=0.6650`, 3 open apertures, four shut lines `100 % open`, band
`1.372–1.775` un-dropped, bay widths `0.507 0.516 0.525`, **132 meshes**,
0 non-manifold edges, `cutters rolled back: none`. Anything else means something
regressed in transit — find out what before building on top of it.

Both levels, every time. "Guards green" was true only at SUB=1 for six revisions
while the production build silently lost both cab-door shut lines.

**4. Read, in this order:** `STATE.md` → `SPEC.md` **§10 then §10.9** (§10.9 is
rev 8 and supersedes §10 where they differ) → `SKEPTIC_PASS.md` →
`HANDOFF_rev8.md` → `REF_MEASUREMENTS.md`.

`STATE.md` is machine-written by `audit.py` from the mesh built in the same
process, with the git SHA and a dirty-tree flag. If it and any prose disagree,
**it is right.**

## Standing requirement — absolute replication of all artwork

`SPEC.md` §10.10, and it is in my memory file. A hard bar, not a preference:

> Every painted element on this vehicle must be REPRODUCED from photographs of
> the actual combi. Not approximated. Not invented. Not derived from palette
> statistics.

The bar is that the owner recognises **his own vehicle**. §10.10 has the table
of every element, its source crop and its current state.

## Your first task — finish the art reproduction pass

I scoped it to four pieces: the mural, the paisley, the "Señor Tacombi" script,
and the "100% Calidad" decal. **The mural and the paisley are done. The script
and the Calidad are not, and I have already rejected the script once** — of the
rev 8 probe I said "That script i see on the p9 hero is NOT it."

- **Script.** Fat rounded late-1960s psychedelic display lettering in **silver**.
  "Señor" small and raised upper-left, "Tacombi" large. The capital T carries a
  long ribbon swash running back over "Señor". The o, a, c and b have rolled
  **spiral counters**. Strong thick/thin contrast, bulbous terminals. Crop
  `ref_side.jpg` at `(300,470)-(620,570)` and magnify 5×. `sign_gen.py` already
  has `swash_T()`, `spiral()` and `counter_spirals()` — the machinery exists and
  the output still does not look like the photograph. Treat it as a letterform
  job. A system font with flourishes bolted on is what is there now and it is
  what I rejected.
- **Calidad.** Crop `(735,295)-(860,390)`. Spiky starburst with a red-orange →
  orange/yellow **gradient**, white **bold italic** "100%" over "Calidad" at
  about −20°, and **two red bunting bars with triangular pennants above it** that
  are not modelled at all.

## Then, in this order

1. **Land the hero set.** Both scenes. The strip machinery
   (`T1_BORDER="lo,hi"` in `studio.render_set`) is committed and still **untested
   end to end** after two contexts. Four strips at 0.00/0.25/0.50/0.75 with
   `T1_FX=0`, stitch, then `post.py` **once on the stitched frame** — optics per
   strip band at the seams.
2. Art-direct the Playa rig against `ref_side.jpg`. It is lit but not directed.
3. The tail is 99 mm long (model −2.108, measured −2.007). Loft change; the
   counter's `X1` moves with it.
4. Resolve or re-log the rake-versus-arch-gap contradiction (`SPEC.md` §10.9).
5. Re-audit adversarially and iterate. ~23 high-value findings from
   `AUDIT_RECOVERED.md` remain open and have never been through a skeptic pass.
   Do not stop at good enough.

## What is settled — do not re-derive it

`SPEC.md` §10 + §10.9 is the canonical constants table; `REF_MEASUREMENTS.md`
holds the working. Scale, ride height, **rake**, belt line, V-swage, aperture
edges, tyre and rim sizes, louvre block, counter, rear overhang, indicator type,
roundel colour and **lids-open** are measured or locked with stated method. If
you think one is wrong, re-derive it by a different method and show both.

Claims already considered and rejected — do not re-open without new evidence:

- **"The tyre is 0.596–0.606 m, not 0.665."** Raised and rejected three times. It
  comes from taking the ground/shadow line as the tyre edge. 72 rays restricted
  to sectors silhouetted against deep arch shadow, ellipse axis ratio 0.984,
  wheelbase/flange 5.46 ± 0.08 against 5.44 for a 16-inch and 5.77 for a 15-inch.
- **"Set `Z_BELT` from sill − 100 mm."** That launders the sill's error into the
  belt. Set each from its own measurement; let the 100 mm fall out as a check.
- **"Model the lids closed" / restore the canvas ragtop.** I locked OPEN on
  2026-08-10. Both in-service photographs show them up; none shows it closed.
- **"Scan SPEC §0.2 for material names to build the retired-material ban list."**
  Tried in rev 8; it flags six *correct* materials, because every bullet reads
  "retired reading — correction" and the names appear on both sides.
- **"Raise the flank saturation to 0.816."** That is the paint's *albedo*
  saturation. No beauty pixel of a dielectric under a white softbox reaches it —
  the specular term is achromatic and additive. `SPEC.md` §10.9 has the
  decomposition and the falsification test.

## Mistakes already made more than once

**Correcting the vehicle toward the factory catalogue.** This is not a standard
1963 T1. rev 4 "corrected" the tyre to a factory 6.40-15 and zeroed the lowering;
both were wrong and rev 3 had them right. It runs 16-inch rims, ≈0.665 m tyres,
no rear bumper, sits 65 mm low at the reference station with ~1.9° of nose-down
rake, and its roof is cut into hinged lids. Measure the vehicle, never assume the
catalogue. A finding whose evidence is a factory blueprint — especially the
Samba one — used against a measurement from the actual vehicle is presumptively
refuted.

**Measuring the belt line aft of the counter.** On the serving flank the visible
cream/red edge is the counter fascia bottom at 1.082 m, not the paint break at
1.207 m. This produced a 6× error.

**Measuring body features on the cab door in `ref_side.jpg`.** That door is open,
swung ~55–60° on its front hinge. Also: **a man stands in front of the front
wheel** in that photograph — every rev 8 attempt to measure the front arch locked
onto his red shirt instead.

**Trusting a guard that names things.** The canvas ragtop shipped for three
revisions after §0.2 retired it, because `verify.py` banned only the retired
materials someone remembered to type.

## Hard constraints — every one was learned by breaking it

- **Three frames.** Geometry constants are un-dropped; shader constants in
  `t1_mats.py` are dropped / above-ground; `verify.py` runs after the drop.
  `SPEC` §10.1. And since rev 8 **the drop is a function of x** — use
  `t1_core.rake_drop(x)`, never the `RIDE_DROP` scalar, for any frame conversion.
- Pipeline order in `build.py`: subsurf applied before any boolean; wheel arches
  cut while the shell is still a closed solid; every other aperture cut after
  solidify.
- Do not remove the boolean rollback guard in `cut()` — strengthen it, never
  weaken it. The obvious digest does not work: EXACT re-tessellates n-gons even
  on a true no-op, so vertex-count equality is the only clean test.
- A panel-gap outline must not cross the lip of another aperture. The cab-door
  clearance against the front arch is now **asserted at import** in `t1_shell` —
  if you change the rake or the arch, that assert is what stops the SUB=2
  collapse coming back.
- The body stays a single continuous nose-to-tail loft.
- Background processes are reaped — `nohup`, `setsid` and `disown` all fail.
  Render synchronously in strips.
- Batch all changes into one rebuild — do not render between fixes.

## How I work

- Ground in the reference → build → adversarial audit → iterate. Never build
  before grounding. Never call it done off self-review.
- Report the measurement against the reference. Never a self-assigned score.
- Do not tell me anything is ready. Tell me what is fixed, what is still wrong,
  and what you measured.
- Keep visible cadence on long work and send renders as they land.
- Record every new locked decision in `SPEC.md` with a change-log entry, commit
  it, regenerate `STATE.md`, and write it back to my disk — the container is
  ephemeral and a restart has already killed one workflow mid-run. **Anything
  not on my disk does not exist.**
