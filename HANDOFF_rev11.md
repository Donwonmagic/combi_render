# HANDOFF rev 11

## THE STANDARD — read this first and hold it for the whole session

Donald's words, unchanged and binding:

> The final product should be nearly indistinguishable from the original.
> **Any single measurement off is unacceptable.**
> We are recreating a photo realistic version of **that exact bus.**

Not a 1963 T1. Not a generic taqueria combi. His. The acceptance criterion is
**per-measurement, not on average** — a model right in ninety places and wrong in
one is not 99 % done, because he will look straight at the one.

And the reason, which sits above clinical accuracy:

> I really want this to give the person the opportunity to feel like they were on
> playa del carmen all those years ago. I want the owner to remember standing in
> the kombi, in this very picture that was provided.

His standing instruction, restated this session: **"remember to hold up next to the
actual source photos."** Every claim below is a measurement against `ref_side.jpg`,
`ref_rear34.jpg` or `ref_workshop.jpg`. Nothing here is a self-assigned score.

## Where to start

```bash
git clone tacombi_history_rev9.bundle tacombi && cd tacombi
git pull ../tacombi_rev11_incremental.bundle HEAD     # -> 9a227cd, 38 commits
curl -fsSL -o b.tar.xz https://download.blender.org/release/Blender4.5/blender-4.5.3-linux-x64.tar.xz
tar -xf b.tar.xz && mv blender-4.5.3-linux-x64 /tmp/blender
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=2 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=1 /tmp/blender/blender -b --python audit.py
```

Expect at **both** levels `0 fail, 1 warn`, the warn being
`roof @ rear axle 1.923 vs spec 1.960 (-37 mm)` — deliberate and logged. Also
`TYRE_D=0.6650`, 3 open apertures, four shut lines `100 % open`, band
`1.372–1.775`, bay widths `0.507 0.516 0.525`, **182 meshes**, 0 non-manifold
edges, `cutters rolled back: none`.

Then read: `STATE.md` (machine-written from the mesh; if it and any prose disagree,
**it** is right) → `SPEC.md` §10, then §10.9 through §10.27 → this file.

**Read the memory files before you read any code**: `/areas/tacombi-combi-sticker.md`
and `/preferences.md`. Three prior contexts skipped them; one cost half a day and
produced the wrong body type.

## THE BIGGEST OPEN ITEM — the roof hole is not cut

`build.py` step 3 issues windscreen, side-glazing, serving-bay, rear-window and
panel-gap cutters. **It issues no ROOF cutter.** The lids float over an unbroken
roof skin, so the galley is a sealed 2.8 mm steel box and no exterior light can
physically reach the interior. That is why the black serving bays survived several
revisions of `fill_galley` tuning — the light had nowhere to enter.

rev 11 stands the opening in with an emissive panel at the plane where the hole
physically is. **That is a stand-in, not the fix.** SPEC §10.27 has the constraints:
the opening is 1.11 × 2.03 m, it must be cut **after** solidify (the pipeline order
in §10.1 is load-bearing — only the wheel arches are cut while the shell is a closed
solid), and it will change the roof's manifold state, so the non-manifold count and
the shut-line probes must be re-run at **both** subdivision levels.

## Cross-file asks from the rev-11 specialists — measured, reported, NOT applied

Each of these was produced by a specialist who did not own the file it lands in.

1. **Two-sided front lid** (`t1_shell.roof_lids`, `build.py:252-253`). `lid_gen.py`
   now writes `lidmural.png` and `lidsign.png` at an **identical** 2048 × 1238,
   aspect 1.6543, because they are two faces of one flat panel. To use them:
   build a second `_lid_face` for the front lid at `off = -(LID_T + 0.0016)`,
   **reverse its polygon winding** or it renders backfacing, and **mirror u** on
   the inward face (or run `T1_LIDSIGN_MIRROR=1` and `lid_gen` writes it
   pre-mirrored — verified working). Do **not** flip v, and do not "fix" u on the
   mural: `_lid_face`'s v=1 is the free edge and its u=0 is at `LID_X0`, both of
   which already match the textures. **Hold this until §10.26's open questions are
   settled** — it is not yet established that the mural and the lettering are two
   faces of the same panel.
2. **Texture-wrap collision** (`t1_mats.py:823` Scale `0.2600 → 0.2280`, `:815`
   Location.x `0.185 → 0.500`). The tile period is 3.846 m against a 4.01 m flank,
   so the lower nose and the rear-most quarter **share texels**. Costs the X −1.95
   bin 6 points of gold. `folk_gen.MAP_LOC`/`MAP_SCALE` must change to match and the
   generator be re-run — it self-checks and warns if they diverge.
3. **`ROUNDEL_D` coupling is done but check its neighbours.** The VW glyph merged
   into an X twice because `vw_logo`'s R and w were absolute constants tuned against
   a ring diameter driven by `ROUNDEL_D` (§10.25). Grep for other constants tuned
   against a constant.
4. **`t1_detail.CNT_ZB`** puts the counter top at 1.240 AG against
   `REF_MEASUREMENTS` §6's measured 1.189–1.205 — a ~40 mm residual, currently
   absorbed by the galley warmer's height. Unresolved.
5. **Two shelves in `galley()` at x −1.500 / −1.780** are behind the solid rear
   corner panel and visible from nowhere.

## The comprehensive audit — DEFERRED, NOT DROPPED

Donald asked for "a complete and comprehensive workflow by a number of expert
specialists". It was written and launched: ten specialists, one per dimension, each
measuring the model and the heroes against the source photographs; then an
adversarial verifier per ranked finding whose instruction is to REFUTE it; then a
synthesis into `AUDIT_rev11.md`.

**It did not run, and that was my scheduling call, not a judgement that it was not
worth doing.** This container has two CPU cores, so the Workflow runner executed
about two agents at a time; two hours in it had started 2 of its 25 agents. I stopped
waiting and redirected to three targeted specialists, which is what produced the
galley, mural and folk-art fixes in this revision. Donald has since said explicitly
that he wants the audit conducted.

The script is preserved at **`workflows/tacombi-rev11-audit.js`** with a header
listing exactly what to update before running it (four of the ten dimension briefs
were written against rev 10 and rev 11 moved them). On a wide box, run it as a
Workflow. On a narrow one, lift the ten dimension briefs out of it and run them 3-4
at a time with the Agent tool on disjoint files — that is what rev 11 did and it
worked well.

## What still does not match, ranked by what a viewer sees first

Every number is display luma or a measured fraction against the named photograph.

1. **The galley has the right level but not the right depth.** Bays now read
   130 / 160 / 167 against a measured 137 / 157 / 175 — within a few per cent. But
   the internal contrast is flat: bay 1 sd **15.3** against the photograph's
   **28.4**, bay 2 **10.2** against **24.7**. Bay 3's distribution does match. Some
   of bay 1's spread is the man working inside and the surfaces he occludes.
2. **Nothing is dirty.** No road grime, no edge wear on the arches or the counter
   lip, no chalking gradient where the sun would put one. SPEC §3 locks the finish
   as WEATHERED and §10.4 has measured targets. This uniformity is now the dominant
   CG tell on the vehicle.
3. **The counter reads as a thin plank** where the photograph has a deep slab with
   a heavy brass nosing.
4. **Constant-roughness materials went 6 → 9** with the galley dressing. A constant
   roughness is the physical definition of the plastic look. Find the three new ones
   and give them a roughness field.
5. **The Playa hero is not converged** and Donald has deprioritised it — "let's not
   do playa right now. Lets focus on the 3d model." Render reads cream 253 / red 193
   / foliage 46 / ground 186 against a measured 241 / 118 / 82 / 108, cream clipping.
   Diagnosis to test when it comes back: a **contrast** mismatch, not a level one —
   the film (AgX + Punchy) is calibrated for the white studio where paper white sits
   at linear 21.0 (§10.8). Sweeping two light scalars trades foliage against ground
   without fixing the range.
6. **No contact shadow** (`optics-6`) — dies within 11 mm of the tyre, so the
   vehicle floats. Never applied.
7. **The rear window renders as a mirror** rather than showing an interior.
8. Open and never skeptic-passed: `materials-5` (three serving bays share one
   reflection, NCC 0.94–0.97), `apertures-7`, the 99 mm tail-length discrepancy, and
   §10.9's unresolved rake-versus-arch-gap contradiction.
9. **The model's rear arch is 0.747 m wide** (`2·ARCH_R`) against
   `analysis/final_numbers.py`'s 0.952 m read off the photograph. Pre-existing.

## SPEC §10.24 — three things applied and reverted, still OPEN

Bumper standoff, indicator lens depth, headlamp vertical position. Each was applied
from a measurement, broke something independently locked, and was reverted rather
than laundered. The third method that refuted them was the **frontal silhouette** of
`ref_side.jpg` scanned row by row for the left-most vehicle column: nose crown at
column 78, bumper face at 82–91, indicator face at 80.

## Process rules that have each been earned by breaking them

* **Ask what a photograph shows before measuring from it.** One question and two
  marked crops settled the roof topology that three revisions of measurement could
  not (§10.26). It also invalidated more work than any other single error when it
  was skipped.
* **A rendered ratio is only an albedo ratio between two surfaces of the same class
  under the same light.** Generalises §10.12; cost one wrong silver in rev 10.
* **A constant tuned against another constant must be expressed in terms of it**,
  or correcting one silently breaks the other (§10.25).
* **A claim in prose is not a guard.** §10.19 said the lids open forward; the code
  had always hinged them fore-aft. Fourth occurrence. Grep for the node that does it.
* **Check what a guard actually measures.** The script's acceptance test scored
  against a reference mask missing 14 % of the ink, and two recorded generator
  defects were artefacts of it (§10.20).
* **When a finding breaks something independently locked, measure it a third way
  before choosing.** Three did in rev 10; the third method refuted the finding
  every time.
* Batch all changes into one rebuild. Never render between fixes. Never run
  `post.py` per strip — once, on the stitched frame.

## Environment notes that cost real time to learn

* **This container has 2 CPU cores.** A `Workflow` runs only ~2 agents concurrently,
  so a 25-agent audit takes many hours and is not practical. Spawning 3–4 agents
  directly with the Agent tool, on **disjoint files**, is far more effective.
* A single shell command is killed at 10 minutes. `nohup`/`setsid`/`disown` all
  fail. Drive `hero.py --only N` one strip per call, then `--stitch-only`.
* There is **no reachable git remote**. `origin` points at the rev-9 bundle, which
  is a read-only archive. Deliver by bundling to his disk — anything not on his disk
  does not exist.
* Playa strips at 2400×1600/56 run ~6 min each; studio strips ~4 min.
