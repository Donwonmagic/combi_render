# Paste this into the fresh context

Continue the Señor Tacombi combi build. **Eleven revisions of history sit behind
this — you are picking up mid-stream, not starting.** Several things here have been
got wrong more than once and the guards exist to stop it happening again.

## The standard — read this first and hold it for the whole session

In my words:

> The final product should be nearly indistinguishable from the original.
> **Any single measurement off is unacceptable.**
> We are recreating a photo realistic version of **that exact bus.**

Not a 1963 T1. Not a generic taqueria combi. Mine. The acceptance criterion is
per-measurement, not on average — a model right in ninety places and wrong in one is
not ninety-nine percent done, it is wrong, because I will look straight at the one.

And the reason it matters, which sits above clinical accuracy:

> I really want this to give the person the opportunity to feel like they were on
> playa del carmen all those years ago. I want the owner to remember standing in the
> kombi, in this very picture that was provided.

**Standing instruction: hold everything up next to the actual source photos.** Every
claim you make to me is a measurement against `ref_side.jpg`, `ref_rear34.jpg` or
`ref_workshop.jpg`, with its method and its uncertainty. Never a self-assigned score.

Right now I want the **3D model**, not the Playa hero. And I want resolution, detail
and fidelity to keep going up.

## Step 1 — read my memory before you read any code

`/areas/tacombi-combi-3d.md` first, then `/areas/tacombi-combi-sticker.md`, then
`/preferences.md`. Three prior contexts skipped them; one cost half a day and
produced the wrong body type. In rev 8 they caught a live regression inside ten
minutes. If you cannot read them, say so explicitly rather than quietly proceeding.

## Step 2 — restore

```bash
git clone tacombi_history_rev9.bundle tacombi && cd tacombi
git pull ../tacombi_rev11_incremental.bundle HEAD
```

`HEAD` should be `df2cb7f`, 39 commits, clean tree. The same tree is also on my disk
at `tacombi_bus_render/tacombi_rev11_repo/`. Ignore every older `tacombi*` directory.

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
`roof @ rear axle 1.923 vs spec 1.960 (-37 mm)` — deliberate and logged, not a defect
to chase. Also `TYRE_D=0.6650`, 3 open apertures, four shut lines `100 % open`, band
`1.372–1.775`, bay widths `0.507 0.516 0.525`, **182 meshes**, 0 non-manifold edges,
`cutters rolled back: none`. Anything else means something regressed in transit —
find out what before building on it.

Both levels, every time. "Guards green" was true only at SUB=1 for six revisions
while the production build silently lost both cab-door shut lines.

## Step 4 — read, in this order

`STATE.md` → `SPEC.md` §10, then §10.9 through §10.27 (they supersede §10 where they
differ) → `HANDOFF_rev11.md` → `SKEPTIC_PASS.md` → `REF_MEASUREMENTS.md`, with the
caveats in §10.11 and §10.15.

`STATE.md` is machine-written by `audit.py` from the mesh built in the same process.
**If it and any prose disagree, it is right.**

## Step 5 — ASK ME WHAT THE PHOTOGRAPHS SHOW, before you measure anything from them

This has now paid off twice and it is the cheapest thing in the process.

* rev 9: `ref_rear34.jpg` had been treated as a rear three-quarter for several
  revisions. One crop and one question corrected three revisions of geometry.
* rev 11: the lid topology could not be settled by measurement at all — the aspect
  ratios contradicted each other. I looked at two marked crops and said *"the
  separate roof panel that we see in the playa photo is still closed on the side ref
  photo"*, and it resolved instantly. SPEC §10.26.

So: before measuring from any reference, show me a crop and ask me what I am looking
at. Mark the regions and give me options.

## Step 6 — the work

**6.1 Cut the roof hole.** This is the top item and it is real geometry. `build.py`
issues no roof cutter, so the lids float over an unbroken roof skin and the galley is
a sealed steel box — which is why black serving bays survived six revisions of light
tuning. rev 11 stands it in with an emissive panel. SPEC §10.27 has the constraints:
1.11 × 2.03 m, cut **after** solidify, and it changes the roof's manifold state so
the non-manifold count and the shut-line probes must be re-run at both levels.

**6.2 Run the comprehensive specialist audit.** It is written and waiting at
`workflows/tacombi-rev11-audit.js` with a header explaining what to change before
running it. It was deferred in rev 11 — my scheduling call, not a judgement that it
wasn't worth doing — because that container had two cores and it would have taken
hours. **I want it conducted.** If your box is wide, run it as a Workflow. If it is
narrow, take the ten dimension briefs out of it and run them 3–4 at a time with the
Agent tool on disjoint files, which is what rev 11 actually did and it worked well.

**6.3 Weathering.** Nothing on this vehicle is dirty. No road grime, no edge wear on
the arches or the counter lip, no chalking gradient where the sun would put one.
SPEC §3 locks the finish as WEATHERED and §10.4 has measured targets. This uniformity
is now the dominant CG tell. Also: constant-roughness materials regressed 6 → 9 with
the rev-11 galley dressing.

**6.4 The galley's internal contrast.** It has the right level now — bays read
130 / 160 / 167 against a measured 137 / 157 / 175 — but it is flat: bay 1 sd 15.3
against the photograph's 28.4, bay 2 10.2 against 24.7.

**6.5 The counter** reads as a thin plank where the photograph has a deep slab with
a heavy brass nosing.

**6.6** Then the never-skeptic-passed backlog: `optics-6` contact shadow (the vehicle
floats), `materials-5` (three serving bays share one reflection), `apertures-7`, the
99 mm tail-length discrepancy, §10.9's rake-versus-arch-gap contradiction, and the
three items in §10.24 applied-then-reverted and still open.

Batch all changes into one rebuild. Re-run both guards after.

## Step 7 — raise the resolution

I want the heroes bigger and sharper than 2400×1600. Drive `hero.py --only N` one
strip per call then `--stitch-only`; run `post.py` once on the stitched frame, never
per strip.

## How I work

* Ground in the reference → build → adversarial audit → iterate. Never build before
  grounding. Never call it done off self-review.
* Report the measurement against the reference, with its ceiling so the number means
  something. Never a self-assigned score.
* Do not tell me anything is ready. Tell me what is fixed, what is still wrong, and
  what you measured.
* Keep visible cadence on long work and send renders as they land.
* **Travel between contexts consciously, every time.** Record every locked decision
  in `SPEC.md` with a change-log entry, commit it, regenerate `STATE.md`, write a
  handoff and a next-context prompt, and put it all on my disk. `git push` does not
  work — `origin` is a read-only bundle. Bundle the repo and write the bundle to my
  disk; materialise the checkout by cloning outside the mount and copying the tree
  in. **Anything not on my disk does not exist.**

## Already settled — do not re-open without new evidence and a different method

Tyre OD 0.665 m on 16-inch rims (raised and rejected three times). No rear bumper in
service; front bumper cream. Roof cut into hinged lids, modelled OPEN, hinging
**fore-aft** and opening to the serving side — §10.19's "open forward" is refuted
(§10.26). ~65 mm low with ~1.9° nose-down rake. Flank RED sRGB (196,49,36). Never
correct this vehicle toward the VW factory catalogue: a finding whose evidence is a
factory blueprint, used against a measurement from the actual vehicle, is
presumptively refuted.

## Hard-won rules — every one was learned by breaking it

* Never set a vertical position from the ground line (§10.11, ~70 mm common-mode).
* A single linear px→metre scale does not hold along the flank (194.8 px/m at the
  rear panel against 211.5 at mid-body). Place by ratio within a panel whose ends
  are both locked.
* A rendered ratio is only an albedo ratio between two surfaces of the same class
  under the same light (§10.12, §10.21).
* A constant tuned against another constant must be expressed in terms of it, or
  correcting one silently breaks the other (§10.25 — the VW glyph merged into an X
  twice this way).
* **A claim in prose is not a guard.** Four occurrences now. Grep for the node that
  does it.
* **Check what a guard actually measures.** The script's acceptance test scored
  against a reference mask missing 14 % of the ink, and two recorded "generator
  defects" were artefacts of it (§10.20).
* When a finding breaks something independently locked, measure it a third way
  before choosing. Three did in rev 10; the third method refuted the finding every
  time.
* Do not remove the boolean rollback guard in `cut()` — strengthen it, never weaken
  it. The body stays a single continuous nose-to-tail loft. Pipeline order in
  `build.py` is load-bearing.
* A single shell command is killed at 10 minutes; `nohup`/`setsid`/`disown` all fail.
