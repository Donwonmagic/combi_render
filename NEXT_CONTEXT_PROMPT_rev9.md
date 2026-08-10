Continue the Señor Tacombi combi build. Nine revisions of history sit behind this — you are picking up mid-stream, not starting. Several things here have been got wrong more than once and the guards exist to stop it happening again.

# The standard — read this first and hold it for the whole session

In my words:

> **The final product should be nearly indistinguishable from the original. Any single measurement off is unacceptable.**

> **We are recreating a photo realistic version of that exact bus.**

Not a 1963 T1. Not a generic taqueria combi. **Mine.** The acceptance criterion is per-measurement, not on average — a model right in ninety places and wrong in one is not ninety-nine percent done, it is wrong, because I will look straight at the one.

And the reason it matters, which sits above clinical accuracy:

> I really want this to give the person the opportunity to feel like they were on playa del carmen all those years ago. I want the owner to remember standing in the kombi, in this very picture that was provided. I want it to be so real it evokes emotion.

Deliverable: hero stills at 2400×1600 or better — a white-studio hero as the fidelity benchmark and a warm Playa hero for the memory. Renders, not an editable file.

# What changed in rev 9 — the pattern of failure is broken, don't re-break it

**Both heroes landed.** For eight revisions no hero ever rendered; every context spent its budget on diagnosis and ran out. `out/hero_studio.png` and `out/hero_playa.png` are 2400×1600 / 64 samples / six overlapping strips, seams measured clean. The render pipeline is proven. **Do not spend this context re-proving it.**

**The strip machinery had a real seam and it is fixed.** Run as previously prescribed — four *abutting* strips — it seams measurably. Use `hero.py`, which overlaps by 48 px and copies only owned rows. SPEC §10.14 has the numbers.

**A single shell command here is killed at 10 minutes.** That is why `hero.py` takes `--only N` and `--stitch-only`. Drive one strip per call, then stitch. `nohup`/`setsid`/`disown` all still fail.

# Step 1 — read my memory before you read any code

`/areas/tacombi-combi-sticker.md` and `/preferences.md`. Three prior contexts skipped them or could not see them; one cost half a day and produced the wrong body type. In rev 8 they caught a live regression inside ten minutes; in rev 9 the "front paint not true to reality" line in the first file was the thread that led to the flank-hue finding. If you cannot read them, say so explicitly rather than quietly proceeding.

# Step 2 — restore from the rev 9 bundle

```bash
git clone tacombi_history_rev9.bundle tacombi
```

`HEAD` should be `146df01`, **33 commits**, clean tree. The same repo is also checked out and current on my disk at `tacombi_bus_render/tacombi_rev9_repo/`.

Ignore the older `tacombi_bus_render/tacombi/` directory — it is at `c21bb34`, fifteen commits behind, with 17 uncommitted files that are all superseded by commits in the bundle.

# Step 3 — install Blender 4.5.3 and run BOTH guards. Report their actual output before proposing anything.

```bash
curl -fsSL -o b.tar.xz https://download.blender.org/release/Blender4.5/blender-4.5.3-linux-x64.tar.xz
tar -xf b.tar.xz && mv blender-4.5.3-linux-x64 /tmp/blender
cd tacombi
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=2 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=1 /tmp/blender/blender -b --python audit.py
```

Expect at both levels `0 fail, 1 warn`, the warn being `roof @ rear axle 1.923 vs spec 1.960 (-37 mm)` — deliberate and logged, not a defect to chase. Also `TYRE_D=0.6650`, 3 open apertures, four shut lines `100 % open`, band `1.372–1.775` un-dropped, bay widths `0.507 0.516 0.525`, 132 meshes, 0 non-manifold edges, `cutters rolled back: none`. Anything else means something regressed in transit — find out what before building on it.

Both levels, every time. "Guards green" was true only at SUB=1 for six revisions while the production build silently lost both cab-door shut lines.

# Step 4 — read, in this order

`STATE.md` → `SPEC.md` §10, then §10.9 through §10.18 (they supersede §10 where they differ) → `SKEPTIC_PASS.md` → `HANDOFF_rev9.md` → `REF_MEASUREMENTS.md`, **with the caveat in §10.11 and §10.15**.

`STATE.md` is machine-written by `audit.py` from the mesh built in the same process, with the git SHA and a dirty-tree flag. If it and any prose disagree, it is right.

# Step 5 — ASK ME WHAT THE PHOTOGRAPHS SHOW, before you measure anything from them

This is new and it is the most important instruction in this prompt.

In rev 9 I looked at a crop and said: *"That is also the front end of the bus open towards the front. What we are looking at is the inside of the front panel."* `ref_rear34.jpg` had been named and treated as a **rear** three-quarter for several revisions. It is the **front**, with the roof opening forward.

Three revisions of geometry rested on an assumption nobody had ever put to me. The check cost one crop and one question.

So: before measuring from any reference, show me a crop and ask me what I am looking at. Everything currently derived from `ref_rear34.jpg` is suspect — including the flank paisley that SPEC §10.10 marks **done**, the "1963" plate surround, the lettered panel, and the modelled lid topology. SPEC §10.15.

# Step 6 — the work, in this order

## 6.1 The side script — a finely tuned recreation pass

My words: *"the Señor Tacombi text is better but I think deserves a more finely tuned recreation pass. There are a lot of features that are missed or improperly displayed in what I see."*

rev 9 replaced the rejected font-plus-flourishes with real letterforms in `script_gen.py`, built from control points read off `ref_side.jpg` at 6–14× in that photograph's own pixel frame. Whole-lockup IoU **0.511** against a measured ceiling of 0.77–0.81. **Do not restart it** — the measurement infrastructure is the asset.

Missed entirely, and probably more important than any outline:

* **The silver is flat.** Reference ink has per-channel std 16–19 and luma spanning 85–135 at p5–p95 — silver leaf, mottled and unevenly tarnished. `tex/senor.png` emits a constant `(214,216,218)` with all shape in alpha.
* **No keyline or drop shadow** — but read SPEC §10.16 first: they are **not measurable** in `ref_side.jpg`. Do not add one because SPEC §3 asserts it.
* **Uniform stroke weight and one-radius terminals**, where the reference has thick/thin modulation within each glyph and bulbous terminals.

Per-glyph, worst first: `Señor` 0.089 (not fitted; the number is meaningless), `b` 0.41, `a` 0.45, `i` 0.50, `m` 0.54, `o` 0.61, `c` 0.62, swash 0.62, `T` 0.68. The lockup also runs 8 % heavy — thin globally before chasing outlines.

Acceptance test, not self-review: `python3 flank_compare.py out/<side render>.png out/flank_compare.png` crops the rendered flank by projecting the panel through the ortho camera, and `compare_script.py` gives per-glyph IoU plus the overlay. Show me both.

## 6.2 The front fascia — it is drifting

My words: *"the front fascia is starting to drift."* SPEC §10.18 has six items. It did not drift because anything changed; it drifted because the rest of the vehicle advanced through rev 8 and rev 9 and the front stood still on findings that were logged and never applied.

The new one is the worst: **the cab-door and lower-nose folk art is far too faint and sparse.** `ref_side.jpg` at (60,330)-(330,700) shows bold graphic scrollwork covering most of the door — large yellow acanthus, heavy dark-brown outlined curlwork, rows of white rosettes with dark centres, high contrast against the red. The model is pale, thin and widely spaced.

That also contradicts §10.9's measured "0.0–0.2 % gold coverage from X +1.47 to −0.40". That band *is* the cab door, and the door is swung open ~55–60° in that frame, so a coverage scan indexed by body x read the wrong surface. **Re-measure the near-nose density lobes.**

The other four are unapplied audit findings: bezels read gold/brass but the model assigns `chrome` (`materials-6`); VW roundel 9 % undersized and 32 mm high (`livery-9`); transverse roof dome absent, +83 mm/side too wide at z 1.53 (`geometry-4`); indicators wrong type and 20 mm inboard (`inventory-9`). Plus the front bumper reads thin — unmeasured.

## 6.3 The Playa hero does not meet its own brief

It is seam-clean and correctly exposed and it reads as an empty pale plain. `ref_rear34.jpg` shows what is actually there: **dense green palm foliage, close behind the vehicle**, flowers along the lid edge, warm shade. rev 9 fixed three rig defects (§10.13) and added a dapple gobo and ground haze; there is still **no vegetation at all**. That is the single biggest gap between the render and the memory.

Do not orange-grade it. SKEPTIC §B5 is explicit that neither in-service photograph is in direct sun.

## 6.4 The lettered panel and the lid mural

`lid_gen.py:291` draws "La Santa" horizontally in a system serif. The photograph shows **red brush script rising diagonally with a red star over the S**. And the mural is far sparser and darker than the photograph, despite being marked done.

Batch all changes into one rebuild. Re-run both guards after.

# Step 7 — land the hero set again

Full 2400×1600 or better, both scenes, using `hero.py --only N` one strip per call then `--stitch-only`. Send them as they land.

# Step 8 — adversarially audit, then iterate

~23 high-value `AUDIT_RECOVERED.md` findings remain open and have never been through a skeptic pass. Highest impact at hero scale: `materials-5` (three serving bays share one reflection, NCC 0.94–0.97), `materials-14` (both flanks carry the same folk art, mirrored — fatal on a two-angle set), `geometry-4`, `optics-6` (contact shadow dies within 11 mm of the tyre), `apertures-7`. Also open: the tail is 99 mm long (model −2.108, measured −2.007; the counter's `X1` moves with it); six materials still report a constant roughness; the rake-versus-arch-gap contradiction in §10.9 is logged, not resolved. Do not stop at good enough.

# What is settled — do not re-derive it

`SPEC.md` §10 + §10.9 through §10.18 is canonical; `REF_MEASUREMENTS.md` holds the working, subject to §10.11 and §10.15. Scale, ride height, rake, belt line, V-swage, aperture edges, tyre and rim sizes, louvre block, counter, rear overhang, indicator type, roundel colour and lids-open are measured or locked with stated method and error bands. If you think one is wrong, re-derive it by a different method and show both.

## Already considered and rejected — do not re-open without new evidence

* "The tyre is 0.596–0.606 m, not 0.665." Raised and rejected three times. 72 rays restricted to sectors silhouetted against deep arch shadow; ellipse axis ratio 0.984 kills the perspective escape; wheelbase/flange 5.46 ± 0.08 against 5.44 for a 16-inch.
* "Set `Z_BELT` from sill − 100 mm." That launders the sill's error into the belt.
* "Model the lids closed" / bring back the canvas ragtop. Locked OPEN 2026-08-10.
* "Scan SPEC §0.2 for material names to build the retired-material ban list." It flags six correct materials.
* **"Raise the flank saturation to 0.816."** That is the paint's albedo saturation; no beauty pixel of a dielectric under a white softbox reaches it. rev 9 changed the **hue** and left the saturation exactly where §10.9 put it — §10.12 is not a re-opening of this.

## New in rev 9 — three methods that are now refuted

* **Never set a vertical position from REF §0.3's ground line** (§10.11). It carries ~70 mm of common-mode error: the script, the Calidad decal and the belt paint break all land low from it by the same sign and magnitude. Use the belt, or a vertical *extent* in which the offset cancels.
* **A single linear pixel→metre scale does not hold across the flank.** The rear panel measures 194.8 px/m against 211.5 px/m at mid-body. Place aft features by ratio within a panel whose ends are both locked.
* **Do not render `T1_SCENE=playa` with `transparent=True`** (§10.13). It composites the world away and you get a blown white sky.

# Mistakes already made more than once

**Correcting the vehicle toward the factory catalogue.** rev 4 "corrected" the tyre to a factory 6.40-15 and zeroed the lowering; both were wrong. It runs 16-inch rims, ≈0.665 m tyres, no rear bumper, sits 65 mm low at the reference station with ~1.9° of nose-down rake, and its roof is cut into hinged lids. Measure the vehicle, never assume the catalogue. A finding whose evidence is a factory blueprint used against a measurement from the actual vehicle is presumptively refuted.

**Measuring the belt line aft of the counter.** On the serving flank the visible cream/red edge is the counter fascia bottom at 1.082 m, not the paint break at 1.207 m. This produced a 6× error.

**Measuring body features on the cab door in `ref_side.jpg`.** That door is open, swung ~55–60° on its front hinge — and this is what corrupted §10.9's near-nose folk-art density. A man also stands directly in front of the front wheel in that photograph.

**Trusting a guard that works by naming things.** The canvas ragtop shipped for three revisions after §0.2 retired it because `verify.py` banned only the retired materials someone had remembered to type.

**A claim in prose is not a guard.** `studio.playa()`'s docstring promised dappled palm shade since rev 8 and no code produced it; the vehicle sat in flat light for a whole revision. `audit.py` printed a fabricated belt line for six. If a rig says it does something, grep for the node that does it.

**Assuming what a photograph shows.** See Step 5. This is the newest and it invalidated more work than any of the others.

# Hard constraints — every one was learned by breaking it

* Three frames. Geometry constants are un-dropped; shader constants in `t1_mats.py` are dropped / above-ground; `verify.py` runs after the drop (§10.1). Since rev 8 the drop is a function of x — use `t1_core.rake_drop(x)`, never the `RIDE_DROP` scalar.
* Pipeline order in `build.py`: subsurf applied before any boolean; wheel arches cut while the shell is still a closed solid; every other aperture cut after solidify.
* Do not remove the boolean rollback guard in `cut()` — strengthen it, never weaken it. EXACT re-tessellates n-gons even on a true no-op, so vertex-count equality is the only clean test.
* A panel-gap outline must not cross the lip of another aperture. The cab-door clearance against the front arch is asserted at import in `t1_shell`.
* The body stays a single continuous nose-to-tail loft.
* Batch all changes into one rebuild — do not render between fixes.
* Never run `post.py` per strip. Once, on the stitched frame.

# How I work

* Ground in the reference → build → adversarial audit → iterate. Never build before grounding. Never call it done off self-review.
* Report the measurement against the reference, with its ceiling so the number means something. Never a self-assigned score.
* Do not tell me anything is ready. Tell me what is fixed, what is still wrong, and what you measured.
* Keep visible cadence on long work and send renders as they land.
* Record every new locked decision in `SPEC.md` with a change-log entry, commit it, regenerate `STATE.md`, and write it back to my disk. Note: `git push` does not work here — there is no reachable remote, and the connected folder blocks `unlink` so git cannot even hold a lock file inside it. Bundle the repo, write the bundle to my disk, and materialise the checkout by cloning outside the mount and copying the tree in. Anything not on my disk does not exist.
