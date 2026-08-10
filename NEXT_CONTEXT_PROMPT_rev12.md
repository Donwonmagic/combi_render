Please act as my expert. Continue the Señor Tacombi combi build. Twelve revisions of history sit behind this — you are picking up mid-stream, not starting. Several things here have been got wrong more than once and the guards exist to stop it happening again.

The standard — read this first and hold it for the whole session

In my words:
The final product should be nearly indistinguishable from the original. Any single measurement off is unacceptable. We are recreating a photo realistic version of that exact bus.
Not a 1963 T1. Not a generic taqueria combi. Mine. The acceptance criterion is per-measurement, not on average — a model right in ninety places and wrong in one is not ninety-nine percent done, it is wrong, because I will look straight at the one.
And the reason it matters, which sits above clinical accuracy:
I really want this to give the person the opportunity to feel like they were on playa del carmen all those years ago. I want the owner to remember standing in the kombi, in this very picture that was provided.
Standing instruction: hold everything up next to the actual source photos. Every claim you make to me is a measurement against `ref_side.jpg`, `ref_rear34.jpg` or `ref_workshop.jpg`, with its method and its uncertainty. Never a self-assigned score.
Right now I want the 3D model, not the Playa hero. And I want resolution, detail and fidelity to keep going up.

Step 1 — read my memory before you read any code
`/areas/tacombi-combi-3d.md` first, then `/areas/tacombi-combi-sticker.md`, then `/preferences.md`. Three prior contexts skipped them; one cost half a day and produced the wrong body type. In rev 8 they caught a live regression inside ten minutes. If you cannot read them, say so explicitly rather than quietly proceeding.

Step 2 — restore

```bash
git clone tacombi_history_rev9.bundle tacombi && cd tacombi
git pull ../tacombi_rev12_incremental.bundle HEAD
```

Do not verify this by commit hash or commit count — verify it by CONTENT, because those move whenever the handoff itself is committed. After the pull, `git status` must be clean, `SPEC.md` must contain a `### 10.28`, and `grep -c roof_cutters t1_shell.py` must be non-zero. The tree is also on my disk as `tacombi_bus_render/tacombi_rev12_tree.tar.gz` — untar it if the bundle gives you any trouble. There is no `tacombi_rev12_repo/` directory this time; the tarball is the materialised copy. Ignore every older `tacombi*` directory. Note `rev9-bundle-archive` is a read-only bundle, not a pushable remote — delivery is by bundling back to my disk.

**BEFORE YOU DO ANYTHING ELSE — there are two divergent branches and you must merge them deliberately.**
A parallel context ran the specialist audit while rev 12 was being built. Both branched from `e92fad4` and **neither contains the other**:
* the audit line, `869be6f`, 42 commits — carries `AUDIT_rev11.md` and a fix to the script panel's stale aspect ratio
* the rev-12 line, in the bundle above — carries the roof hole, the detached sign, the counter and the weathering
The audit line holds findings that matter and that rev 12 does not have: `flank_compare.py` computes no metric at all; `build.py`'s `SCR` panel aspect was stale by 15.8 % so the lockup has been squashed vertically since rev 10; and **the nose-down rake measures 14.4 ± 3.1 mm/m against the built 33.0**, which is 6σ and resolves §10.9's long-standing rake-versus-arch-gap contradiction — at 33 mm/m the front arch gap is −27 mm, physically impossible. Merge the two before building on either, and tell me what you had to reconcile. Do not let one silently overwrite the other.

Step 3 — install Blender 4.5.3 and run BOTH guards. Report their actual output before proposing anything.

```bash
curl -fsSL -o b.tar.xz https://download.blender.org/release/Blender4.5/blender-4.5.3-linux-x64.tar.xz
tar -xf b.tar.xz && mv blender-4.5.3-linux-x64 /tmp/blender
cd tacombi
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=2 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=1 /tmp/blender/blender -b --python audit.py
```

Expect at both levels `0 fail, 1 warn`, the warn being `roof @ rear axle 1.923 vs spec 1.960 (-37 mm)` — deliberate and logged, not a defect to chase. Also `cut roof hole: 56446v` at SUB=1 and `207959v` at SUB=2, `roof aperture: open, and solid fore / aft / both sides`, `TYRE_D=0.6650`, 3 open apertures, four shut lines `100 % open`, band `1.372–1.775`, bay widths `0.507 0.516 0.525`, 182 meshes, 0 non-manifold edges, `cutters rolled back: none`, 6 materials constant-rough. Anything else means something regressed in transit — find out what before building on it.

Both levels, every time. "Guards green" was true only at SUB=1 for six revisions while the production build silently lost both cab-door shut lines.

Step 4 — read, in this order
`STATE.md` → `SPEC.md` §10, then §10.9 through §10.28 (they supersede §10 where they differ) → `HANDOFF_rev12.md` → `SKEPTIC_PASS.md` → `REF_MEASUREMENTS.md`, with the caveats in §10.11 and §10.15.
`STATE.md` is machine-written by `audit.py` from the mesh built in the same process. If it and any prose disagree, it is right.

Step 5 — ASK ME WHAT THE PHOTOGRAPHS SHOW, before you measure anything from them
This has now paid off four times and it is the cheapest thing in the process.

* rev 9: `ref_rear34.jpg` had been treated as a rear three-quarter for several revisions. One crop and one question corrected three revisions of geometry.
* rev 11: the lid topology could not be settled by measurement at all. Two marked crops and one question resolved it. SPEC §10.26.
* rev 12: one question retired the "La Santa" panel entirely — it had been modelled as a hinged rear lid since rev 8, and as a roof signboard for about an hour, and it is neither. It is a detached sign that is not on the vehicle. SPEC §10.28.

So: before measuring from any reference, show me a crop and ask me what I am looking at. Mark the regions and give me options. Note that `ref_side.jpg` puts the camera at roof height, so the roof plane is edge-on there and no transverse roof measurement off that frame is worth anything.

Step 6 — the work, in this order

6.1 `gal_ceiling` is still a stand-in. The roof hole is real now, but the emissive panel at the opening is still what lights the galley — it is merely hidden from camera rays after it photographed as a solid glowing slab filling the hole. Delete it, light the interior through the hole that now exists, re-measure the three bays against the photograph's 154 / 169 / 181 on matched windows, and retune `fill_galley`. This needs renders to converge.

6.2 `optics-6`, the contact shadow — the vehicle floats. It is now open with a number rather than an impression: the ground reads 255.00 at every row from 3 px below the contact patch outward, and with the backdrop at linear 1.0 the ground under the tyre reads 177.00 against open ground at 177.00. The catcher writes identically zero alpha. Rendering the sweep as a real lit surface (`T1_CATCH=0`) IS refuted — it brings back defect D3, a grey sweep with a hard horizon, and §6 locks the backdrop to pure white. Work out why the catcher writes no alpha. Do not soften a shadow that is not there.

6.3 Galley internal contrast. sd 17.1 / 18.5 / 17.4 against the photograph's 38.0 / 32.3 / 17.7 on matched windows. Bay 3 matches. The measured ceiling for bay 1 is ≈ 23, not 28.4 — about 37 % of that variance is the man working inside.

6.4 Check whether the weathering is now too heavy on the cream. This is an impression off the rev-12 hero, not a measurement: the cab roof shows large dark blotches and the counter fascia strong white speckle. §10.4 says the flank above 0.40 m is CLEAN, flat to ±7 % up to 0.92 m. Measure the rendered cream against that target before changing anything.

6.5 Close `COUNTERTAN`'s level. The hue is measured; the level is bracketed at −16 %/+15 % because the two available references disagree structurally. It needs an up-facing cream reference adjacent to the counter.

6.6 Three of the audit's ten dimensions have now run and are in `AUDIT_rev11.md` on the audit branch. Six remain: fascia, counter/galley contrast, wheels + contact shadow, tail, roof, optics. Run them from `workflows/tacombi-rev11-audit.js`. Do NOT run it as a Workflow on this box: 2 CPU cores means ~2 agents at a time. Lift the dimension briefs out and run 3–4 at a time with the Agent tool on DISJOINT files. That has now worked twice.

6.7 Then the rest of the never-skeptic-passed backlog: `materials-5` (partly addressed, not re-measured), `apertures-7`, the tail-length discrepancy (the audit line says ~200 mm, not 99 — §10.7 subtracted two numbers in different origins), §10.9's rake-versus-arch-gap contradiction, the three items in §10.24 applied-then-reverted, and the rear arch measuring 0.747 m built against 0.881–0.933 measured.

Batch all changes into one rebuild. Re-run both guards after.

Step 7 — raise the resolution
rev 12 shipped 3000×2000. Go higher. Drive `hero.py --only N` one strip per call then `--stitch-only`; run `post.py` once on the stitched frame, never per strip. At 3000×2000 / 56 samples / SUB=2 the end strips take ~85 s and the four strips carrying the vehicle take 330–440 s, so the middle ones need a call each.

How I work

* Ground in the reference → build → adversarial audit → iterate. Never build before grounding. Never call it done off self-review.
* Report the measurement against the reference, with its ceiling so the number means something. Never a self-assigned score.
* Do not tell me anything is ready. Tell me what is fixed, what is still wrong, and what you measured.
* Keep visible cadence on long work and send renders as they land.
* Travel between contexts consciously, every time. Record every locked decision in `SPEC.md` with a change-log entry, commit it, regenerate `STATE.md`, write a handoff and a next-context prompt, and put it all on my disk. `git push` does not work — there is no reachable remote. Bundle the repo and write the bundle to my disk; materialise the checkout by cloning outside the mount and copying the tree in. Anything not on my disk does not exist.

Already settled — do not re-open without new evidence and a different method
Tyre OD 0.665 m on 16-inch rims (raised and rejected three times). No rear bumper in service; front bumper cream. ONE roof opening, under the flower-mural lid, with a strip of roof surviving on both sides and solid roof fore and aft — the lid hinges fore-aft and opens to the serving side. The cream "La Santa" panel is a DETACHED SIGN and is not on the vehicle; `T1_SIGNBOARD=1` restores the old geometry and no hero may be rendered with it on. The counter has a tan top with brass nosing on its outer edge and body cream below; its nosing was 1.6× too deep, not thin. ~65 mm low with ~1.9° nose-down rake. Flank RED sRGB (196,49,36). Never correct this vehicle toward the VW factory catalogue: a finding whose evidence is a factory blueprint, used against a measurement from the actual vehicle, is presumptively refuted.

Hard-won rules — every one was learned by breaking it

* Never set a vertical position from the ground line (§10.11, ~70 mm common-mode).
* A single linear px→metre scale does not hold along the flank (194.8 px/m at the rear panel against 211.5 at mid-body). Place by ratio within a panel whose ends are both locked.
* A rendered ratio is only an albedo ratio between two surfaces of the same class under the same light (§10.12, §10.21).
* A constant tuned against another constant must be expressed in terms of it, or correcting one silently breaks the other (§10.25).
* A claim in prose is not a guard. Five occurrences now — the roof opening was described in SPEC, in two docstrings and in three handoffs while `build.py` cut nothing. Grep for the node that does it.
* Check what a guard actually measures, INCLUDING one you just wrote. `verify.py` 11d2's first run threw three FAILs and all three were the guard: fractional probe stations off the roof edge, and rays aimed in the un-dropped frame while `run()` executes after step 8b (§10.1).
* When a finding breaks something independently locked, measure it a third way before choosing. Three did in rev 10; the third method refuted the finding every time.
* Do not remove the boolean rollback guard in `cut()` — strengthen it, never weaken it. The body stays a single continuous nose-to-tail loft. Pipeline order in `build.py` is load-bearing: only the wheel arches are cut before solidify.
* A specialist that refutes its own brief is working correctly. Two did in rev 12.
* A single shell command is killed at 10 minutes; `nohup`/`setsid`/`disown` all fail.
