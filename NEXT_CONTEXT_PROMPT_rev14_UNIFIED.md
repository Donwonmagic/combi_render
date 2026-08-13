Please act as my expert. Continue the Señor Tacombi combi build. Thirteen revisions sit behind this and **three parallel contexts have just been unified into one line** — you are picking up mid-stream, not starting, and your first job is to build on a merge rather than to redo it.

## The standard — read this first and hold it for the whole session

In my words:

The final product should be nearly indistinguishable from the original. Any single measurement off is unacceptable. We are recreating a photo realistic version of that exact bus.

Not a 1963 T1. Not a generic taqueria combi. Mine. The acceptance criterion is per-measurement, not on average — a model right in ninety places and wrong in one is not ninety-nine percent done, it is wrong, because I will look straight at the one.

And the reason it matters, which sits above clinical accuracy:

I really want this to give the person the opportunity to feel like they were on playa del carmen all those years ago. I want the owner to remember standing in the kombi, in this very picture that was provided.

Standing instruction: hold everything up next to the actual source photos. Every claim you make to me is a measurement against `ref_side.jpg`, `ref_rear34.jpg` or `ref_workshop.jpg`, with its method and its uncertainty. Never a self-assigned score.

I want the 3D model, not the Playa hero. And I want resolution, detail and fidelity to keep going up.

## Step 1 — read my memory before you read any code

`/areas/tacombi-combi-3d.md` first, then `/areas/tacombi-combi-sticker.md`, then `/preferences.md`. Three prior contexts skipped them; one cost half a day and produced the wrong body type. If you cannot read them, say so explicitly rather than quietly proceeding.

## Step 2 — restore. THERE IS ONE LINE NOW.

```bash
git clone tacombi_history_rev9.bundle tacombi && cd tacombi
git pull ../tacombi_rev14_unified.bundle HEAD
```

**Do not verify by commit hash or count** — those move whenever the handoff itself is committed. Verify by CONTENT: after the pull `git status` must be clean, and all four of these must be true:

```bash
grep -c '### 10.29' SPEC.md          # 1  — rev 13's section
grep -c DOME_DEFICIT verify.py       # non-zero
ls AUDIT_rev11.md AUDIT_rev12.md     # BOTH present
grep -c _COUNTER_PARTS audit.py      # non-zero
```

The tree is also on my disk as `tacombi_rev14_tree.tar.gz`. Ignore every older `tacombi*` directory. `rev9-bundle-archive` is a read-only bundle, not a pushable remote — delivery is by bundling back to my disk. **Anything not on my disk does not exist.**

**THE BRANCH DIVERGENCE IS OVER. Do not go looking for it.** Three lines were merged, deliberately, and each merge is documented in its own commit message:

| line | carried | state |
|---|---|---|
| rev-12 build line | the roof hole, the detached sign, the counter, the weathering | merged |
| audit line (`2b8d3c1`) | `AUDIT_rev11.md` — proportion, weathering, script, fascia; the `SCR` panel-aspect fix; the `_NOSE_SEL` severity-5 fix | merged, both code fixes verified present by grep AFTER the merge |
| audit-2 line (`87aeaa6`) | `AUDIT_rev12.md` — counter/galley, wheels+ground, tail, roof, optics/glass, each with an adversarial verifier | merged, re-cut against rev 13 so it measures the tree it ships with |

**All ten audit dimensions have now run.** Four of them ran twice, in contexts blind to each other. That double coverage is the most valuable thing in the repo and §"What the two audits agree on" below is where you should start.

## Step 3 — install Blender 4.5.3 and run BOTH guards. Report their actual output before proposing anything.

```bash
curl -fsSL -o b.tar.xz https://download.blender.org/release/Blender4.5/blender-4.5.3-linux-x64.tar.xz
tar -xf b.tar.xz && mv blender-4.5.3-linux-x64 /tmp/blender
cd tacombi
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=2 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=1 /tmp/blender/blender -b --python audit.py
```

Expect at both levels `0 fail, 1 warn`. **The warn changed in rev 13 and it is deliberate:**

```
warn  roof crown @ rear axle (dome-corrected) 1.992 vs spec 1.960 (+32 mm)
dims  roof@rear-axle=1.894 (raw resid -66 mm; dome deficit +98 mm still unmodelled)
```

Also `cut roof hole: 56293v` at SUB=1 and **`207383v`** at SUB=2, `roof aperture: open, and solid fore / aft / both sides`, `TYRE_D=0.6650`, 3 open apertures, four shut lines `100 % open`, band `1.372–1.775`, **bay widths `0.516 0.515 0.516`**, **181 meshes**, 0 non-manifold edges, `cutters rolled back: none`, **5 materials constant-rough**.

That SUB=2 figure is worth a sentence. `HANDOFF_rev13.md` first shipped `207806v`, a number nobody ever watched print — it was written from a truncated console tail. The audit-2 context caught it and a clean-tree rebuild gives **207383v**. It is corrected everywhere now. Take the lesson rather than the number: **do not put a figure in an acceptance test unless you saw it print.**

Both levels, every time. "Guards green" was true only at SUB=1 for six revisions while the production build silently lost both cab-door shut lines.

## Step 4 — read, in this order

`STATE.md` → `SPEC.md` §10, then §10.9 through §10.29 → `HANDOFF_rev13.md` → **`AUDIT_rev12.md`** → `AUDIT_rev11.md` → `SKEPTIC_PASS.md` → `REF_MEASUREMENTS.md`.

`STATE.md` is machine-written by `audit.py` from the mesh built in the same process. **If it and any prose disagree, it is right.**

**§10.29 carries two corrections that touch every REF number.** `REF_MEASUREMENTS`'s model-frame column is **100 mm aft of where it says**, because 495.8 px is the hub midpoint and this model's mid-wheelbase is x = +0.100. And `RULES §4`'s 194.8 px/m at the rear panel is refuted **in sign** — it measures 225 ± 3.

## Step 5 — ASK ME WHAT THE PHOTOGRAPHS SHOW, before you measure anything from them

This has now paid off five times and it is the cheapest thing in the process. In rev 13 one word from me — "plywood" — invalidated a whole `COUNTERTAN` derivation that two revisions had been bracketing.

**And my answers are not infallible.** In the same pass my reading that the bulbs around the serving apertures light the galley was refuted by measurement: the aperture trim reads S 0.110–0.152 while the drip-rail festoon in the same rows reads S 0.281–0.317 and 15–40 codes brighter. The surround is a matte white bobble fringe; the only lit string is outside the skin. **That was the right outcome — ask me anyway, then measure what I say.**

Show me a crop, mark the regions, give me options. `ref_side.jpg` puts the camera at roof height, so the roof plane is edge-on there and no transverse roof measurement off that frame is worth anything.

## What the two audits AGREE on — treat these as the firmest facts in the project

Two contexts, blind to each other, different methods:

| finding | audit line / rev 13 | audit-2 line |
|---|---|---|
| **`optics-6` is refuted — the vehicle does not float** | the `side` camera's optical axis is horizontal, so the ground plane at z = 0 is edge-on and never sampled; both "proving" numbers were the backdrop | the same, found separately: an ORTHO camera with view direction (0,−1,0) against a cyclorama that *is* the plane z = 0 |
| **the contact shadow is real** | 0.484 / 0.797 / 0.921 / 0.999 / 1.000 at 0 / 5 / 10 / 15 / 20 mm outboard against a photograph at 0.57 / 0.89 / 0.94 / 0.97 / 1.00 | catcher writes α 0.674–0.930 at 20 mm; control with `is_shadow_catcher=False` gives α ≡ 1.0000, so it is shadow, not coverage |
| **bulb pitch** | 28.6 ± 1.0 mm (FFT) | 28.8 ± 2.0 mm, with a JPEG-artefact control that passes cleanly |
| **the tail is long** | 245 ± 15 mm, three methods | 195–300 mm |
| **the roof section is short and the lid is flat** | crown R 2.45 ± 0.15 m; gutter-to-crown 0.188 ± 0.015 against 0.083 | lid crown 122 ± 16 mm with an internal control (longitudinal edge straight to rms 0.51 px, transverse bows 23 px, same detector) |
| **the rake and the dome are ONE defect** | applied the rake, named the residual `DOME_DEFICIT = 0.098`, measured +32 mm | *predicted* +30 mm before seeing it, and predicted the raw residual would land at −58/−74 (it is −66) |
| **`audit.py` was measuring a prop** | `_bodyish` omits `counter_top` | the same, independently |

**The rake/dome convergence is the single strongest result the project has produced.** One context measured the dome from the drip-rail gutter and from the workshop lid's cut edge; the other measured the lid's crown from its own silhouette; a third route predicted the residual arithmetically before it was observed. They are the same missing 90–120 mm. What is left is a one-parameter fit, not an open question.

## Where they DISAGREE, and how each was resolved

* **The tail lamp's OVAL is REFUTED.** The tail dimension measured AR 1.49 and called it a 1.5:1 upright oval. The adversarial verifier showed AR 1.46–1.60 is exactly what a circle shows at that foreshortening. **rev 13 did not apply the oval** — it changed only the material, `ruby` → `amber`, and audit-2 independently confirms the lens is *warmer* than the paint it sits on. Leave the lamp round.
* **Bay 1's galley contrast: the man in the hatch is wearing a WHITE SHIRT.** Every mask ever offered caught skin only. Properly masked, bay 1's photograph sd is **18.50 ± 2.02** — *below* the ~23 "ceiling" the old finding attacked. **The 38.0 / 32.3 / 17.7 targets rev 13 tuned `fill_galley` against are superseded.** Current numbers, re-measured on the rev-13 tree: render **24.34 / 19.65 / 24.89** against a photograph at **32.23 / 24.28 / 18.11**. So **bay 2 is the real defect** and **bay 3 already runs over** — a further global lift makes bay 3 worse. The remaining work is per-bay.
* **`materials-5` is DEAD.** Bay-pair peak NCC +0.157 / +0.281 / +0.148 against a positive control at +0.517 and the photograph's own bay null at +0.332 / −0.135 / +0.194. Close it.
* **Rear arch width**: 1.026 ± 0.035 m (rev 13's wheels pass) against 0.881–0.933 (audit line). Both reject the built 0.747 by a wide margin; the *profile* finding is the stronger one either way — see below.
* **Rear arch GAP**: the audit line's 52 mm is refuted at 3σ. It measures **41.0 ± 3.5 mm**, exactly the built `ARCH_R − TIRE_R`.

## Step 6 — the work

Order matters and it is not the order of severity. This sequence is the merge of both audits' own ordered lists, deduplicated, and it is chosen so nothing later invalidates something earlier.

**6.1 Metrology and guards first — cheap, and everything downstream is measured through them.**
`audit.py`'s `_bodyish` and `post.py`'s bloom threshold were both fixed in the unified line; confirm they took. `flank_compare.py` still **computes no metric at all** and three of its framing decisions are wrong — give it a real number before you touch the script again, or you cannot tell whether a change helped.

**6.2 Shaders and post — these change every pixel and cost no geometry risk.**
* **All glass reads as a mirror.** Rear pane CV 1.22 against the photograph's 0.24; the interior *is* modelled and lit and is being overwritten; panes are smooth-shaded at 9.4× the render null. `gal_ceiling`'s `visible_glossy` is refuted as the cause (1.87 against a 4.19 null) — it is the rig.
* **Gold folk art is painted across the flat tail face.** Photograph 0.00 % gate-independent in 35 991 px with a 20.94 % positive control; render 14.3–18.1 %. Cause is `t1_mats.py`'s BOX projection — the nose's fix was never done for the tail. **There is still no tail selector.**
* **The mural texture is right and the render is not.** Texture area mean (127,59,23) matches the photograph's (126,60,24) to one code; the render reads (148,92,69), displaced *away* by a near-neutral additive lift. **Fix the shader. Never touch `tex/lidmural.png`.**
* **The cream needs MORE breakup, 3.4–6×** — 1.24 % RMS at 25 mm against §10.4's 4.22 % and 7.37 % measured directly. My "too heavy" impression is refuted for the flank. The cab **roof** is a different node and is not yet measured.
* Sun fade is keyed on `Normal.Z`, so every vertical surface gets exactly zero. `WEATHER` is spliced onto only ten materials.

**6.3 Detail geometry.**
Cream rim ~59 mm small (rim/tyre 0.6612 ± 0.0060 against 0.5729 built, 14.7σ; the implied OD lands 0.1 mm from the dead `RIM_R`, which is referenced by nothing). Hubcap VW glyph has a **ring** the model lacks and is 29 % undersized; the V and W prisms interpenetrate at every diameter. T-handle 205 mm *below* the plate in the photograph, 240 mm *above* it in the build. Plate frame +31 to +66 % too tall. Tail lamps 1.9–2.2× short. Louvre band 105–170 mm too far aft. Five condiment caddies where the model has two. An 18.0 mm red strip exposed above the counter at every station.

**6.4 The loft, jointly — roof crown + rake first, then the rear arch, then the tail LAST.**
* **Roof crown and rake are one fit.** `DOME_DEFICIT` in `verify.py` must be driven to zero as you build the section. Crown R 2.45 ± 0.15 m; the lid is a curved shell and `_lid_panel` builds it flat.
* **The rear arch is a flat-crowned OGEE, not a circle** — drop ∝ |Δx|^3.9±0.2 where a circle is 2.00; crown flat within 4.7 mm over 337 mm; at 140 mm off-axle the model drops 27.2 mm where the photograph drops 2.6. Change the *profile*, not just the radius.
* **The tail, last, as a re-spaced aft station set — never a translation.** It moves the counter, the plate, the lamps and the louvres with it.
* Tyre deflection is real at 23–32 mm but is **deliberately parked**: it cannot be authored in an axisymmetric revolve and it trips `audit.py`'s `TYRE_D` guard.

**6.5 `COUNTERTAN`.** The top is bare/varnished plywood, so no cream-paint ratio is admissible under §10.21 — which is exactly why the two references bracket rather than agree. The method that needs no same-class partner is written out in §10.29: hold `COUNTERCREAM`, measure the gold-line-referenced top/fascia linear ratio in the photograph — **(0.796, 0.810, 0.633) ± 0.02** — and solve `T1_CTAN` onto it in the render, three points. The hue is ~16 % too orange and does not survive at all.

**6.6 The camera absolutely last.** Re-framing invalidates every hero-pixel measurement in both reports.

**LOGGED, NOT APPLIED — do not apply without a third method or a new photograph:** the serving bays may be glazed. It contradicts a reading I settled myself.

Batch all changes into one rebuild. Re-run both guards after.

## Step 7 — raise the resolution

rev 12 shipped 3000×2000; rev 13 went to 3600×2400. Go higher again. Drive `hero.py --only N` one strip per call then `--stitch-only`; run `post.py` **once** on the stitched frame, never per strip.

## Two photographs would unblock more than any amount of measurement

1. **A left-side broadside** — cab door shut, nobody within a metre of the front wheel, square-on from as far back as the space allows. Settles the tumblehome, the front arch, the absolute height, the body's own belt line, and collapses the rake's ±3.4 mm/m band to ±0.6.
2. **A square-on rear elevation, or any rear three-quarter from the OFF side.** Settles the engine lid's width and shut lines, the rear-lamp count, the plate's lateral position, the far half of the tail face, the roof opening's forward station, the hinge count — and whether the off flank carries glazing at all. `glass_bay0/1/2_R` exist and render at 3× the local contrast, and **no photograph shows that side**.

Ask me for them.

## How I work

* Ground in the reference → build → adversarial audit → iterate. Never build before grounding. Never call it done off self-review.
* Report the measurement against the reference, with its ceiling so the number means something. Never a self-assigned score.
* Do not tell me anything is ready. Tell me what is fixed, what is still wrong, and what you measured.
* Keep visible cadence on long work and send renders as they land.
* Travel between contexts consciously, every time. Record every locked decision in `SPEC.md` with a change-log entry, commit it, regenerate `STATE.md`, write a handoff and a next-context prompt, and put it all on my disk.

## Already settled — do not re-open without new evidence and a different method

Tyre OD 0.665 m on 16-inch rims. No rear bumper in service; front bumper cream. ONE roof opening, under the flower-mural lid, with a strip of roof surviving on both sides and solid roof fore and aft — the lid hinges fore-aft and opens to the serving side. The cream "La Santa" panel is a DETACHED SIGN and is not on the vehicle. The counter has a **bare/varnished plywood** top with brass nosing on its outer edge and body cream below. Flank RED sRGB (196,49,36). **The nose-down rake is 17.75 mm/m (1.02°)** — re-derived hub-referenced in rev 13, 4.5σ from the old 33.0; the old value is retired, not open. **The serving bays are EQUAL at 0.5155 m.** **`optics-6` is CLOSED as refuted.** **`materials-5` is CLOSED as dead.** The tail lamp is **round**, not oval. Never correct this vehicle toward the VW factory catalogue.

## Hard-won rules — every one was learned by breaking it

* Never set a vertical position from the ground line (§10.11, ~70 mm common-mode).
* A single linear px→metre scale does not hold along the flank. Place by ratio within a panel whose ends are both locked.
* **An image slope of a fore-aft line is not a rake** — all of the vehicle's own horizontal lines converge on one vanishing point, so a raw slope carries the perspective term too. That confusion cost five revisions.
* A rendered ratio is only an albedo ratio between two surfaces of the same class under the same light — and "same class" means paint-to-paint, not paint-to-plywood.
* A constant tuned against another constant must be expressed in terms of it (§10.25).
* A claim in prose is not a guard. Grep for the node that does it.
* **Check what a guard, or a probe, can physically SEE.** `optics-6` cost four revisions because it was diagnosed on a camera that cannot sample the ground plane at all.
* **A guard can be strengthened instead of widened.** When a residual grows because a second measured defect became visible, encode that defect as a named constant that must go to zero — do not open the band.
* **Do not put a figure in an acceptance test unless you watched it print.** `207806v` shipped in a handoff from a truncated console tail.
* When a finding breaks something independently locked, measure it a third way before choosing.
* Do not remove the boolean rollback guard in `cut()` — strengthen it, never weaken it. Pipeline order in `build.py` is load-bearing: only the wheel arches are cut before solidify.
* **A specialist that refutes its own brief is working correctly.** Several did in rev 13, and the adversarial verifiers overturned their own specialists repeatedly in `AUDIT_rev12.md`. That is the process working, not failing.
* **Watch for the lamppost.** In `ref_side.jpg` a post occupies columns 62–79 and has now produced three separate confident wrong numbers about the front of the vehicle. Check occlusion before trusting any measurement forward of column 90.
* A single shell command is killed at 10 minutes; `nohup`/`setsid`/`disown` all fail. This box has 2 CPU cores — spawn 3–4 `Agent`s on disjoint files rather than running a Workflow.
