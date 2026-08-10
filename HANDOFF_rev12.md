# HANDOFF rev 12

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
`ref_workshop.jpg`, with its method. Nothing here is a self-assigned score.

He has deprioritised the Playa hero: *"let's not do playa right now. Lets focus
on the 3d model."* He wants resolution, detail and fidelity to keep going up.

## Where to start

```bash
git clone tacombi_history_rev9.bundle tacombi && cd tacombi
git pull ../tacombi_rev12_incremental.bundle HEAD      # applies straight onto the rev9 clone
curl -fsSL -o b.tar.xz https://download.blender.org/release/Blender4.5/blender-4.5.3-linux-x64.tar.xz
tar -xf b.tar.xz && mv blender-4.5.3-linux-x64 /tmp/blender
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=2 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=1 /tmp/blender/blender -b --python audit.py
```

Expect at **both** levels `0 fail, 1 warn`, the warn being
`roof @ rear axle 1.923 vs spec 1.960 (-37 mm)` — deliberate and logged. Also
`cut roof hole: 56446v` (SUB=1) / `207959v` (SUB=2),
`roof aperture: open, and solid fore / aft / both sides`, `TYRE_D=0.6650`,
3 open apertures, four shut lines `100 % open`, band `1.372–1.775`, bay widths
`0.507 0.516 0.525`, **182 meshes**, **0 non-manifold edges**,
`cutters rolled back: none`, **6 materials constant-rough**.

**Both levels, every time.** "Guards green" was true only at SUB=1 for six
revisions while the production build silently lost both cab-door shut lines.

Then read: **the memory files first** (`/areas/tacombi-combi-3d.md`,
`/areas/tacombi-combi-sticker.md`, `/preferences.md`) → `STATE.md` (machine-written
from the mesh; if it and any prose disagree, **it** is right) → `SPEC.md` §10,
then §10.9 through §10.28 → this file.

## What rev 12 did

**THE ROOF HOLE IS CUT.** This was the top open item since rev 11. `build.py`
issued no roof cutter for eleven revisions, so the lids floated over an unbroken
roof skin and the galley was a sealed 2.8 mm steel box no exterior source could
reach — which is why the black serving bays survived six revisions of
`fill_galley` tuning. `t1_shell.roof_cutters()` now issues one, from step 3,
after solidify. Non-manifold stayed 0 with a 1.11 × 2.03 m hole in the roof.

**Four readings settled with Donald from marked crops, before measuring** — SPEC
§10.28:

| # | his answer |
|---|---|
| roof, fore-aft | **ONE opening only**, under the flower lid; solid roof forward over the cab and aft to the tail |
| roof, across | **a strip on both sides**; the 1.11 m width stands |
| the cream lettered panel | *"I was wrong, I think it is a **detached sign**"* |
| the counter | **tan top, brass nosing on the OUTER EDGE, body cream below** |

**The "La Santa" panel is off the vehicle.** Modelled as `lid_rear` since rev 8
(a second hinged lid implying a second opening that was never cut), briefly
re-modelled this revision as a roof signboard on his first answer, and now
emitting nothing. It never appears in `ref_side.jpg` not because it is folded
flat — which is what I had reasoned — but because it is not on the bus.
Geometry kept behind `T1_SIGNBOARD=1`. **Not the default. Do not render a hero
with it on.** He has revised this one panel three times; if it is revisited it
needs a photograph showing its footing, not another inference.

**Weathering, to §10.4's measured targets.** The dust tide line was re-fitted:
C\*/(L\*+16) on 45 266 red-flank px is flat to ±1.5 % over z = 0.42–0.84 and
leaves the ±7 % band at **h = 0.424 ± 0.020**; the shipped ramp had its knee at
0.350, outside §10.4's 0.40 ± 0.04. The upward-facing deposit was **sharing one
colour and one height ramp with the road film** and delivering ΔC\* +0.58 against
a target of +5.0 — and weighting a *vertical* high panel as though it were an
upward face. Split into two independent deposits; the solve is asserted at
import, not eyeballed. Independent confirmation of §10.4 from `ref_rear34.jpg`:
ΔL\* −8.39 / ΔC\* +3.71 / Δhue −5.20° against §10.4's −8.8 / +5.0 / −6.6.

**Constant-roughness materials 9 → 6.** The three the rev-11 galley dressing
added now carry a roughness field. The six left are transmissive or the sealed
reflector — the only exemptions `STATE.md` allows — plus `gal_sky`, which should
be **deleted** now the aperture is real.

**The counter.** Tan top added (`countertan`, and see the honest caveat below).
The brass nosing was **re-measured and it was 1.6× too DEEP, not thin**: the gold
band is 4.52 ± 0.23 px of a 24.84 px counter edge in `ref_side.jpg`, ratio 0.182,
cross-checked at 0.191 in `ref_rear34.jpg`; the model was showing 31.2 mm where
0.186 of the locked 107 mm slab is 19.9 mm. "Reads thin" was a **contrast**
defect, not a size one — `build.py` painted the whole slab `countercream`, so the
gold had cream above *and* below it where the photograph has tan above.

**`CNT_ZB`'s 40 mm residual is explained.** It is the frame conversion, not the
geometry: `CNT_ZT` was set as 1.189 + 0.065, but since rev 8 the drop is a LINE
and `RIDE_DROP` survives only as its value at `X_DROP_REF` = +0.8636. The counter
runs +0.918 → −2.423, essentially all aft of that station. The 68 mm gap is
0.0330 × (0.8636 − (−1.2000)) exactly. **Not applied** — the re-measurement sits
inside a parallax term pinned only to ±10 mm, and §10.24 exists for findings
applied from one chain that broke something locked.


## BRANCH DIVERGENCE — resolve this before rev 13 builds anything

The specialist audit ran in a parallel context while rev 12 was being built. Both
lines branched from `e92fad4` and **neither contains the other**:

| line | tip | carries |
|---|---|---|
| audit | `869be6f`, 42 commits | `AUDIT_rev11.md`, and a fix to the script panel's stale aspect |
| rev 12 | this bundle | the roof hole, the detached sign, the counter, the weathering |

Findings on the audit line that rev 12 does **not** have, and that matter:

* **`flank_compare.py` computes no metric at all.** The test SPEC calls the
  acceptance test for the flank script prints two crop sizes and writes a stacked
  image. All three of its framing decisions are wrong and two of them cancel, so
  the pair look MORE alike than they are.
* **`build.py`'s `SCR` panel aspect was stale by 15.8 %** — commented "= tex AR",
  true of the rev-9 texture; rev 10 rebuilt the texture and nobody updated the
  constant. The lockup has been squashed vertically since rev 10.
* **The nose-down rake measures 14.4 ± 3.1 mm/m against the built 33.0** — 6σ —
  and it RESOLVES §10.9's rake-versus-arch-gap contradiction rather than deepening
  it: at 33 mm/m the front arch gap is −27 mm, physically impossible; at 14.4 it
  is +17 mm, inside REF §2's independent band. That is the third independent
  method this project's own rules demand.
* Two calibration corrections that move many numbers: the model's origin is not
  mid-wheelbase, so every REF "model-frame" number is 100 mm aft of where it says;
  and the flank's px/m drifts the opposite way from RULES §4 — the tail is NEARER.

Merge deliberately. Do not let either line silently overwrite the other.

## What is still wrong, ranked by what a viewer sees first

1. **The vehicle floats.** `optics-6`, and it is now open *with a number*. The
   old note said the shadow "dies within 11 mm of the tyre", which describes a
   shadow that decays. It does not decay: on a 1400 × 933 side probe the ground
   reads **255.00 at every row from 3 px below the contact patch outward**, and
   with the backdrop forced to linear 1.0 the ground under the tyre reads
   **177.00 against open ground at 177.00** — identical to two decimals. The
   catcher writes identically zero alpha. **The obvious fix is refuted**:
   `T1_CATCH=0` renders the sweep as a real lit surface and does put a shadow
   down (175.2 mean / 161.2 min against 255), but it brings back defect D3 in
   full — a 166 grey sweep with a hard horizon — and §6 locks the backdrop to
   pure white. **Next attempt: ask why the catcher writes no alpha under a
   vehicle that plainly occludes the rig. Do not soften a shadow that isn't there.**
2. **`gal_ceiling` is still a stand-in, now merely hidden.** Cutting the hole
   made it visible: the first 3000 × 2000 hero photographed a solid pale glowing
   slab filling the opening, which read as a closed lid. It is now
   `visible_camera = False` — it still emits, still lights the bays, so the
   measured levels survive. **The real fix is to delete it and light the interior
   through the hole that now exists, then re-measure the three bays and retune
   `fill_galley`.** That needs renders to converge and is the first job.
3. **Galley internal contrast, still short.** On matched windows the render now
   reads bay means 132 / 158 / 172 against the photograph's 154 / 169 / 181, and
   sd **17.1 / 18.5 / 17.4 against 38.0 / 32.3 / 17.7**. Bay 3 matches. Bays 1
   and 2 are flat. Honest ceiling, measured not guessed: splitting the
   photograph's bay 1 at u 0.35 gives a man-free forward third at sd 28.6 against
   35.9 for the whole bay, so ~37 % of that variance is the man working inside
   and no dressing produces it. Reachable target for bay 1 is ≈ 23, not 28.4.
4. **`COUNTERTAN`'s level is bracketed, not measured.** The hue is measured; the
   level is the midpoint of two references that disagree structurally — the
   fascia (same light, wrong orientation, takes red bounce) gives albedo G 0.416,
   the cab roof (right orientation, different surround) gives 0.569. Locked at
   0.493, **−16 %/+15 %**. `T1_CTAN=r,g,b` tests the ends. Closing this needs an
   up-facing cream reference *adjacent to the counter*, which neither photograph
   clearly provides.
5. **The weathering may now be too heavy on the cream.** Not measured — an
   impression off the 3000 × 2000 hero, where the cab roof shows large dark
   blotches and the counter fascia carries strong white speckle. §10.4 says the
   flank above 0.40 m is CLEAN, flat to ±7 % up to 0.92 m. **Measure the rendered
   cream against that before touching anything**; the previous specialist
   deliberately left `W_ALBEDO` and the chip constants alone and gave reasons.
6. Never applied, never skeptic-passed: `materials-5` (partly addressed — the
   emitter footprint was the duplication mechanism and is now the true opening,
   but it has not been re-measured), `apertures-7`, the 99 mm tail-length
   discrepancy, §10.9's rake-versus-arch-gap contradiction, the three findings in
   §10.24 applied-then-reverted, and the rear arch measuring 0.747 m against
   0.952 m off the photograph.
7. **The comprehensive specialist audit still has not run.** `AUDIT_rev11.md` was
   expected from a parallel context this session and did not arrive. The script
   is at `workflows/tacombi-rev11-audit.js`. On this 2-core box, do NOT run it as
   a Workflow — lift the dimension briefs out and run 3–4 at a time with the
   Agent tool **on disjoint files**. That worked well twice now.

## Process notes earned this session

* **The two-sided guard caught its own author.** `verify.py` 11d2 asserts the
  opening is open AND the roof is solid everywhere Donald says it is. Its first
  run threw three FAILs and **all three were guard bugs, not geometry**:
  fractional probe stations landed at |y| = 0.81, off the roof entirely, and the
  rays were aimed in the UN-DROPPED frame while `run()` executes AFTER step 8b.
  Re-derived by ray-casting the built mesh on a 13 × 9 grid; the residual against
  `roof_z` came out as exactly `−rake_drop(x)` at every station, which proves it
  was a frame error. §10.1 exists for this and it still caught me.
* **Ask before measuring — it paid twice more.** One question retired a panel
  that had been modelled three different ways across five revisions.
* **Two specialists on disjoint single files worked well.** One owned
  `t1_mats.py`, one owned `t1_detail.py`, neither ran Blender, all changes
  batched into one rebuild. Both returned measurements with methods and both
  refuted part of their own brief, which is the point.
* **A specialist refuting its brief is a success, not a failure.** The counter
  brief said the nosing reads thin; measurement said 1.6× too deep. The brief
  said two galley shelves were invisible; the ray from `hero34r` reaches them.
  Both were reported rather than quietly complied with.

## Delivery

There is **no reachable git remote** — `rev9-bundle-archive` is a read-only
bundle. Delivery is by bundling to Donald's disk and that is the only thing that
counts. On his disk for rev 12: `tacombi_rev12_incremental.bundle`,
`tacombi_rev12_tree.tar.gz` (the materialised copy — there is no `tacombi_rev12_repo/` this time), `SPEC_rev12.md`,
`STATE_rev12.md`, `HANDOFF_rev12.md`, `NEXT_CONTEXT_PROMPT_rev12.md`,
`rev12_hero_studio.png`.

Environment: 2 CPU cores; a single shell command is killed at 10 minutes and
`nohup`/`setsid`/`disown` all fail. At 3000 × 2000 / 56 samples / SUB=2 the end
strips take ~85 s and the strips carrying the vehicle take **330–440 s** — one
strip per call for the middle four, then `--stitch-only`, then `post.py` once.
