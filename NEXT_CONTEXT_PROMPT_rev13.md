Please act as my expert. Continue the Señor Tacombi combi build. Thirteen revisions of history sit behind this — you are picking up mid-stream, not starting. Several things here have been got wrong more than once and the guards exist to stop it happening again.

The standard — read this first and hold it for the whole session

In my words:

The final product should be nearly indistinguishable from the original. Any single measurement off is unacceptable. We are recreating a photo realistic version of that exact bus.

Not a 1963 T1. Not a generic taqueria combi. Mine. The acceptance criterion is per-measurement, not on average — a model right in ninety places and wrong in one is not ninety-nine percent done, it is wrong, because I will look straight at the one.

And the reason it matters, which sits above clinical accuracy:

I really want this to give the person the opportunity to feel like they were on playa del carmen all those years ago. I want the owner to remember standing in the kombi, in this very picture that was provided.

Standing instruction: hold everything up next to the actual source photos. Every claim you make to me is a measurement against `ref_side.jpg`, `ref_rear34.jpg` or `ref_workshop.jpg`, with its method and its uncertainty. Never a self-assigned score.

Right now I want the 3D model, not the Playa hero. And I want resolution, detail and fidelity to keep going up.

Step 1 — read my memory before you read any code
`/areas/tacombi-combi-3d.md` first, then `/areas/tacombi-combi-sticker.md`, then `/preferences.md`. Three prior contexts skipped them; one cost half a day and produced the wrong body type. If you cannot read them, say so explicitly rather than quietly proceeding.

Step 2 — restore
```bash
git clone tacombi_history_rev9.bundle tacombi && cd tacombi
git pull ../tacombi_rev13_incremental.bundle HEAD
```
Do not verify this by commit hash or commit count — verify it by CONTENT, because those move whenever the handoff itself is committed. After the pull, `git status` must be clean, `SPEC.md` must contain a `### 10.29`, and `grep -c DOME_DEFICIT verify.py` must be non-zero. The tree is also on my disk as `tacombi_bus_render/tacombi_rev13_tree.tar.gz` — untar it if the bundle gives you any trouble. Ignore every older `tacombi*` directory. `rev9-bundle-archive` is a read-only bundle, not a pushable remote — delivery is by bundling back to my disk.

THE TWO DIVERGENT BRANCHES ARE MERGED. rev 13 merged the audit line (`2b8d3c1`, 43 commits, `AUDIT_rev11.md` + the SCR panel-aspect fix) into the rev-12 line. Nothing is outstanding there. Do not go looking for it again.

Step 3 — install Blender 4.5.3 and run BOTH guards. Report their actual output before proposing anything.
```bash
curl -fsSL -o b.tar.xz https://download.blender.org/release/Blender4.5/blender-4.5.3-linux-x64.tar.xz
tar -xf b.tar.xz && mv blender-4.5.3-linux-x64 /tmp/blender
cd tacombi
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=2 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=1 /tmp/blender/blender -b --python audit.py
```
Expect at both levels `0 fail, 1 warn`. THE WARN CHANGED IN REV 13 AND IT IS DELIBERATE: `roof crown @ rear axle (dome-corrected) 1.992 vs spec 1.960 (+32 mm)`, and the dims line reads `roof@rear-axle=1.894 (raw resid -66 mm; dome deficit +98 mm still unmodelled)`. Also `cut roof hole: 56293v` at SUB=1 and `207806v` at SUB=2, `roof aperture: open, and solid fore / aft / both sides`, `TYRE_D=0.6650`, 3 open apertures, four shut lines `100 % open`, band `1.372–1.775`, bay widths `0.516 0.515 0.516`, 181 meshes, 0 non-manifold edges, `cutters rolled back: none`, 5 materials constant-rough. Anything else means something regressed in transit — find out what before building on it.

Both levels, every time. "Guards green" was true only at SUB=1 for six revisions while the production build silently lost both cab-door shut lines.

Step 4 — read, in this order
`STATE.md` → `SPEC.md` §10, then §10.9 through §10.29 (they supersede §10 where they differ) → `HANDOFF_rev13.md` → `AUDIT_rev11.md` → `SKEPTIC_PASS.md` → `REF_MEASUREMENTS.md`, with the caveats in §10.11, §10.15 and §10.29. `STATE.md` is machine-written by `audit.py` from the mesh built in the same process. If it and any prose disagree, it is right.

**§10.29 carries a correction that touches every REF number: `REF_MEASUREMENTS`'s model-frame column is 100 mm aft of where it says, because 495.8 px is the hub midpoint and this model's mid-wheelbase is x = +0.100.** And RULES §4's 194.8 px/m at the rear panel is refuted in sign — it measures 225 ± 3.

Step 5 — ASK ME WHAT THE PHOTOGRAPHS SHOW, before you measure anything from them
This has now paid off five times and it is the cheapest thing in the process. In rev 13 one word from me ("plywood") invalidated a whole derivation of `COUNTERTAN` that two revisions had been bracketing. Note that my answers are not infallible: in the same pass my reading that the aperture bulbs light the galley was refuted by measurement, and that was the right outcome. Show me a crop and ask me what I am looking at; mark the regions and give me options. `ref_side.jpg` puts the camera at roof height, so the roof plane is edge-on there and no transverse roof measurement off that frame is worth anything.

Step 6 — the work, in this order

6.1 **The rear arch.** Biggest geometry defect left, severity 5 twice over. It is a flat-crowned OGEE, not a circle: drop ∝ |Δx|^3.9±0.2 where a circle is 2.00, crown flat within 4.7 mm over 337 mm, and the corners put it at 1.026 ± 0.035 m against a built 0.747. At 140 mm off-axle the model drops 27.2 mm where the photograph drops 2.6. Re-derive once more before applying — it contradicts a locked value — then change the cutter profile, not just its radius.

6.2 **The tail is 245 ± 15 mm too long.** Rear overhang 0.761–0.804 m by three methods against 1.008 built. This is a loft change and it moves the counter, the plate, the lamps and the louvres with it. §10.7's "99 mm" is 100 mm of origin error plus 145 mm of scale drift.

6.3 **The transverse roof section, 3.9× too flat.** Crown R 2.45 ± 0.15 m against 9.65 built; gutter-to-crown 0.188 ± 0.015 against 0.083. `verify.py`'s `DOME_DEFICIT` must be driven to zero as you build it — that is what it is there for. The lid is also a curved shell and `_lid_panel` builds it flat.

6.4 **Tyre deflection**, 31.7 ± 4 mm. It does not move the rake (0.2 mm/m) but it does mean rocker-above-ground is 0.300 front / 0.344 rear.

6.5 **Close `COUNTERTAN`.** The top is bare/varnished plywood, so no cream-paint ratio is admissible (§10.21). The method that needs no same-class partner is written out in §10.29: hold `COUNTERCREAM`, measure the gold-line-referenced top/fascia linear ratio in the photograph — (0.796, 0.810, 0.633) ± 0.02 — and solve `T1_CTAN` onto it in the render, three points. The hue is ~16 % too orange and does not survive at all.

6.6 **The cream needs MORE breakup, not less** — 1.24 % RMS at 25 mm against §10.4's 4.22 % and a direct re-measurement of 7.37 %. My "too heavy" impression is refuted for the flank; the cab ROOF is a different node and is not yet measured.

6.7 **The last two audit dimensions**: optics/glass and playa. Lift the briefs out of `workflows/tacombi-rev11-audit.js` and run them with the Agent tool on disjoint files, 3–4 at a time. Do NOT run it as a Workflow on this box — 2 CPU cores.

6.8 Then the rest: bay 1 is 11 DN low (a distribution problem); tail lamp oval not round and 2.4× too small; T-handle 468 mm high with the sign inverted; engine lid 108 mm too tall; louvre band 105–170 mm too far aft; five caddies where the model has two; the hubcap VW glyph has a ring the model lacks and is 29 % undersized; the V and W prisms interpenetrate at every diameter; `Señor` needs re-measuring after the panel-aspect fix; Calidad's star is baked into the burst texture; `nose.png`'s ink is in the wrong band; `apertures-7`.

**LOGGED, NOT APPLIED — do not apply without a third method or a new photograph:** the serving bays may be glazed. It contradicts a reading I settled myself.

Batch all changes into one rebuild. Re-run both guards after.

Step 7 — raise the resolution
rev 12 shipped 3000×2000; rev 13 went higher. Go higher again. Drive `hero.py --only N` one strip per call then `--stitch-only`; run `post.py` once on the stitched frame, never per strip.

How I work
* Ground in the reference → build → adversarial audit → iterate. Never build before grounding. Never call it done off self-review.
* Report the measurement against the reference, with its ceiling so the number means something. Never a self-assigned score.
* Do not tell me anything is ready. Tell me what is fixed, what is still wrong, and what you measured.
* Keep visible cadence on long work and send renders as they land.
* Travel between contexts consciously, every time. Record every locked decision in `SPEC.md` with a change-log entry, commit it, regenerate `STATE.md`, write a handoff and a next-context prompt, and put it all on my disk. `git push` does not work. Anything not on my disk does not exist.

Already settled — do not re-open without new evidence and a different method
Tyre OD 0.665 m on 16-inch rims. No rear bumper in service; front bumper cream. ONE roof opening, under the flower-mural lid, with a strip of roof surviving on both sides and solid roof fore and aft — the lid hinges fore-aft and opens to the serving side. The cream "La Santa" panel is a DETACHED SIGN and is not on the vehicle. The counter has a bare/varnished plywood top with brass nosing on its outer edge and body cream below. Flank RED sRGB (196,49,36). **The nose-down rake is 17.75 mm/m (1.02°), re-derived hub-referenced in rev 13 and 4.5σ from the old 33.0 — the old value is retired, not open.** The serving bays are EQUAL at 0.5155 m. `optics-6` is CLOSED as refuted — the contact shadow matches the photograph within ~1σ at every station and the vehicle is not floating. Never correct this vehicle toward the VW factory catalogue.

Hard-won rules — every one was learned by breaking it
* Never set a vertical position from the ground line (§10.11, ~70 mm common-mode).
* A single linear px→metre scale does not hold along the flank. Place by ratio within a panel whose ends are both locked.
* **An image slope of a fore-aft line is not a rake** — all of the vehicle's own horizontal lines converge on one vanishing point, so a raw slope carries the perspective term too. That confusion cost five revisions.
* A rendered ratio is only an albedo ratio between two surfaces of the same class under the same light (§10.12, §10.21) — and "same class" means paint-to-paint, not paint-to-plywood.
* A constant tuned against another constant must be expressed in terms of it (§10.25).
* A claim in prose is not a guard. Grep for the node that does it.
* **Check what a guard, or a probe, can physically SEE.** `optics-6` cost four revisions because it was diagnosed on a camera whose optical axis is horizontal and which cannot sample the ground plane at all.
* **A guard can be strengthened instead of widened.** When a residual grows because a second measured defect became visible, encode that defect as a named constant that must go to zero — do not open the band.
* When a finding breaks something independently locked, measure it a third way before choosing.
* Do not remove the boolean rollback guard in `cut()` — strengthen it, never weaken it. Pipeline order in `build.py` is load-bearing: only the wheel arches are cut before solidify.
* A specialist that refutes its own brief is working correctly.
* A single shell command is killed at 10 minutes; `nohup`/`setsid`/`disown` all fail.
