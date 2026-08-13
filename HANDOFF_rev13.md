# HANDOFF rev 13

## THE STANDARD — read this first and hold it for the whole session

Donald's words, unchanged and binding:

> The final product should be nearly indistinguishable from the original.
> **Any single measurement off is unacceptable.**
> We are recreating a photo realistic version of **that exact bus.**

Not a 1963 T1. Not a generic taqueria combi. His. The criterion is
**per-measurement, not on average** — a model right in ninety places and wrong in
one is not 99 % done, because he will look straight at the one.

And the reason, which sits above clinical accuracy:

> I really want this to give the person the opportunity to feel like they were on
> playa del carmen all those years ago. I want the owner to remember standing in
> the kombi, in this very picture that was provided.

Standing instruction: **hold everything up next to the actual source photos.**
Every claim below is a measurement against `ref_side.jpg`, `ref_rear34.jpg` or
`ref_workshop.jpg`, with its method and its uncertainty. Nothing here is a
self-assigned score. The Playa hero stays deprioritised; the 3D model is the job,
and resolution, detail and fidelity keep going up.

## Where to start

```bash
git clone tacombi_history_rev9.bundle tacombi && cd tacombi
git pull ../tacombi_rev13_incremental.bundle HEAD
curl -fsSL -o b.tar.xz https://download.blender.org/release/Blender4.5/blender-4.5.3-linux-x64.tar.xz
tar -xf b.tar.xz && mv blender-4.5.3-linux-x64 /tmp/blender
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=2 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=1 /tmp/blender/blender -b --python audit.py
```

**Verify by CONTENT, never by commit hash or count** — both move whenever the
handoff itself is committed. After the pull `git status` must be clean, `SPEC.md`
must contain a `### 10.29`, and `grep -c DOME_DEFICIT verify.py` must be non-zero.

Expect at **both** levels `0 fail, 1 warn`. **The warn has CHANGED and that is
deliberate:**

```
warn  roof crown @ rear axle (dome-corrected) 1.992 vs spec 1.960 (+32 mm)
```

and the dims line now reads
`roof@rear-axle=1.894 (raw resid -66 mm; dome deficit +98 mm still unmodelled)`.
Also `cut roof hole: 56293v` (SUB=1) / **`207383v`** (SUB=2 — corrected; the
figure `207806v` that first shipped in this file was never observed. It was
written from a truncated console tail and the audit-2 context caught it. A
number in an acceptance test that nobody watched print is exactly the failure
this project's rules exist to stop, and it happened anyway), `roof aperture: open,
and solid fore / aft / both sides`, `TYRE_D=0.6650`, 3 open apertures, four shut
lines `100 % open`, band `1.372–1.775`, **bay widths `0.516 0.515 0.516`**,
**181 meshes**, 0 non-manifold edges, `cutters rolled back: none`,
**5 materials constant-rough**.

**Both levels, every time.**

Then read: **the memory files first** (`/areas/tacombi-combi-3d.md`,
`/areas/tacombi-combi-sticker.md`, `/preferences.md`) → `STATE.md` (machine-written
from the mesh; if it and any prose disagree, **it** is right) → `SPEC.md` §10, then
§10.9 through §10.29 → this file → `AUDIT_rev11.md`.

## The branch divergence is RESOLVED

The audit line came in at `2b8d3c1` / 43 commits — one commit further than the
rev-12 handoff said (`869be6f` plus the fascia dimension). Merge base `e92fad4`
confirmed; neither side contained the other. Reconciled deliberately:

| file | outcome |
|---|---|
| `build.py` | auto-merged. Audit's `SCR` panel z1 0.9177 → 0.9896 and rev 12's roof-cutter call are ~350 lines apart. Both verified present by grep AFTER the merge. |
| `t1_mats.py` | auto-merged. The `_NOSE_SEL[0] = None` clear is gone from the ALPHA branch (severity 5 — the nose rendered as black marks). |
| `STATE.md` | only conflict, provenance rows only. Took rev 12's, then regenerated. |
| `AUDIT_rev11.md`, `NEXT_CONTEXT_PROMPT_rev11.md` | taken from the audit line. |

## What rev 13 did

Full detail in **SPEC §10.29**. In order of how much it moves:

1. **The rake is 17.75 mm/m, not 33.0** — rejected at **4.5σ** by a method that
   needs no ground line, no px/m and no vanishing point. Donald authorised
   re-opening a value on his own settled list, on condition it was measured a
   fourth way first. Both hub centres sit at exactly one tyre radius above flat
   ground by construction, so rocker-above-hub at each axle differences into the
   rake: front −0.0004 m, rear +0.0422 m, /2.400 = 0.01775.
2. **§10.9's five-revision contradiction is closed** against the built value —
   but the arch-gap identity is demoted from estimator to **bound** (the two lips
   are different pressings). The rear gap itself re-measures 41.0 ± 3.5 mm,
   exactly the built value, refuting the audit line's own 52 mm at 3σ.
3. **A 100 mm origin error in `REF_MEASUREMENTS`, found independently in two
   dimensions.** 495.8 px is the hub midpoint, and this model's mid-wheelbase is
   x = +0.100. Bays sat 105 mm aft; §10.7's "99 mm tail" contained the same 100.
4. **The bays are EQUAL at 0.5155 m** — §10.5's taper is perspective. Guard
   strengthened: still pins every edge to 1e-6 and now pins the widths together.
5. **`optics-6` is REFUTED — the catcher was never broken.** The old diagnosis
   was measured on the `side` camera, whose optical axis is horizontal, so the
   ground plane is exactly edge-on and never sampled. Measured at 1022 px/m on
   the hero camera the contact profile matches the photograph within ~1σ at every
   station. **Do not add a shadow this vehicle does not cast.**
6. **`gal_ceiling` deleted**, galley lit through the real hole. Every bay mean
   moved toward the photograph and the two flat bays gained real contrast.
7. Bulb pitch 0.135 → 0.0286 (measured twice, blind, two methods). Tail lamp
   `ruby` → `amber`. Roof guard strengthened with a named `DOME_DEFICIT`.
8. **The cream is measured TOO CLEAN, not too weathered** — 1.24 % RMS at 25 mm
   against §10.4's 4.22 % and a direct re-measurement of 7.37 %.

## Four audit dimensions ran; six of ten are now done

`AUDIT_rev11.md` holds proportion, weathering, script, fascia. rev 13 ran
**counter/galley, wheels+contact, tail, roof** as four parallel `Agent` calls on
disjoint files — the pattern that has now worked three times on this 2-core box.
**Do not run `workflows/tacombi-rev11-audit.js` as a Workflow here.** Two
dimensions remain: **optics/glass** and **playa**.

Two specialists refuted their own briefs, which is the point.

## What is still wrong, ranked

1. **The rear arch is a flat-crowned OGEE and 210–280 mm too narrow.** Drop
   ∝ |Δx|^3.9±0.2 where a circle is 2.00; crown flat within 4.7 mm over 337 mm;
   corners at u 648.6 / 868 → **1.026 ± 0.035 m** against a circular 0.747. At
   140 mm off-axle the model drops 27.2 mm where the photograph drops 2.6.
   **Severity 5 twice over. This is the biggest single geometry defect left.**
2. **The tail is 245 ± 15 mm too long.** Rear overhang 0.761–0.804 m by three
   methods against 1.008 built. §10.7's 99 mm is 100 mm origin error plus 145 mm
   scale drift. RULES §4's 194.8 px/m is refuted **in sign**: 225 ± 3 px/m.
3. **The transverse roof section is 3.9× too flat** — crown R 2.45 ± 0.15 m
   against 9.65, gutter-to-crown 0.188 ± 0.015 against 0.083. `DOME_DEFICIT`
   in `verify.py` must be driven to zero when this is built. The lid is also a
   **curved shell** and the model builds it flat.
4. **Tyres do not deflect and they should** — 31.7 ± 4 mm of squash measured.
   Note it does NOT move the rake (0.2 mm/m) but it does mean rocker-above-GROUND
   is 0.300 front / 0.344 rear, so `STATE.md`'s scalar 0.3020 is the front value.
5. **`COUNTERTAN`.** The owner says the top is bare/varnished plywood, so the
   cream-paint ratio is inadmissible by §10.21 — which is why the two references
   bracket rather than agree. Method that needs no same-class partner is written
   out in §10.29; target top/fascia linear ratio (0.796, 0.810, 0.633) ± 0.02.
   Hue is ~16 % too orange and that part does not survive at all.
6. **Bay 1 is 11 DN low** — a distribution problem, not a level one.
7. **The cream needs MORE breakup**, 3.4–6× more. Do not clean it further.
8. Tail lamp oval not round and 2.4× too small; T-handle 468 mm high with the
   sign inverted; engine lid 108 mm too tall; louvre band 105–170 mm too far aft;
   five condiment caddies where the model has two; hubcap VW glyph has a **ring**
   the model lacks and is 29 % undersized; `SCR`/`Señor` needs re-measuring after
   the panel-aspect fix; Calidad's star is baked into the burst texture.
9. **LOGGED, NOT APPLIED: the serving bays may be glazed.** Contradicts a reading
   Donald settled himself. Needs a third method or a new photograph.

## What would unblock the most

**One photograph.** A left-side broadside, cab door shut, nobody within a metre of
the front wheel, square-on from as far back as the space allows. It would settle
the tumblehome, the front arch, the absolute height, the body's own belt line, and
collapse the rake's ±3.4 mm/m band to ±0.6.

## Process notes earned this session

* **An image slope of a fore-aft line is not the rake.** All of the vehicle's own
  horizontal lines converge on one vanishing point, so a raw slope carries the
  perspective term too. Five revisions of argument rested on that confusion.
* **A guard can be strengthened instead of widened.** The roof residual grew when
  the rake was fixed; encoding the separately-measured dome shortfall as a named
  constant that must go to zero keeps the band tight AND makes the open defect
  visible in the guard's own output.
* **Check what a probe can physically SEE.** `optics-6` cost four revisions
  because the camera used to diagnose it has a horizontal optical axis and cannot
  sample the ground plane at all. Both "proving" numbers were the backdrop.
* **The owner can be wrong about his own vehicle and it still pays to ask.** His
  aperture-bulb answer is refuted by measurement — but the counter-top answer
  (plywood) invalidated a whole derivation in one word.

## Delivery

There is **no reachable git remote** — `rev9-bundle-archive` is a read-only
bundle. On his disk for rev 13: `tacombi_rev13_incremental.bundle`,
`tacombi_rev13_tree.tar.gz`, `SPEC_rev13.md`, `STATE_rev13.md`, `HANDOFF_rev13.md`,
`NEXT_CONTEXT_PROMPT_rev13.md`, `AUDIT_rev11.md`.

Environment: 2 CPU cores; a single shell command is killed at 10 minutes and
`nohup`/`setsid`/`disown` all fail. Drive `hero.py --only N` one strip per call,
then `--stitch-only`, then `post.py` once on the stitched frame.
