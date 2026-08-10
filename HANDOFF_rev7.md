# HANDOFF — end of the rev 7 context

`HANDOFF.md` (rev-3 era) is **retired**. It claimed "0 fail, 0 warn" over a
state that had one of each and claimed six commits that never existed. Read
this file, then `STATE.md`, and believe `STATE.md` over both.

---

## 0. Read this first, in this order

1. **Donald's memory: `/areas/tacombi-combi-sticker.md` and `/preferences.md`.**
   **⚠ I could not read them.** They do not exist in this container — I searched
   the whole filesystem; this session ran a different harness with no memory
   tool attached. I did **not** rebuild from the thumbnail: I grounded in
   `START_HERE.md`, `SPEC.md`, `REF_MEASUREMENTS.md` and Donald's own
   restatement of the settled decisions in his brief. **If you can read those
   two files, read them before anything else and check nothing in rev 7
   contradicts them.**
2. `STATE.md` — machine-written by `audit.py` from the mesh built in the same
   process. If it and any prose disagree, it is right.
3. `SPEC.md` **rev 7**, especially **§10**, which is the canonical constants
   table and supersedes every value above it.
4. `SKEPTIC_PASS.md` — what survived the adversarial pass over the 13
   criticals, and the six places where acting on the audit's numbers would
   have introduced fresh errors.
5. `REF_MEASUREMENTS.md` — the measurement working. Still authoritative over
   `AUDIT_RECOVERED.md`.

---

## 1. Environment — three things that cost me time

**Paths are not `/home/claude`.** That directory does not exist and cannot be
created. The repo is portable now (`ROOT` derives from `__file__`), so clone it
anywhere. In this container:

```bash
REPO=/sessions/<session>/mnt/tacombi_bus_render/tacombi     # = the mounted Desktop folder
BL=/sessions/<session>/blender/blender
```

The repo lives **inside Donald's mounted folder**, so the git history persists
on his disk. That is deliberate — the container is ephemeral.

**Background processes are reaped.** `nohup`, `setsid` and `disown` all fail:
three attempts at a backgrounded 2400×1600 hero were killed 25–30 s in, with
memory never above 600 MB of 3.9 GB. It is reaping, not OOM. The shell caps a
synchronous call at 10 minutes and a full hero is ~19 minutes, so:

- `T1_BORDER="lo,hi"` renders a horizontal band of the **same full-size frame**
  (`crop_to_border` stays off so framing is identical across strips).
- `post.py` applies bloom / CA / vignette / grain to the **stitched** image in
  numpy. Do not apply them per strip — bloom and vignette band at the seams.
- Render with `T1_FX=0` when stripping, then run `post.py`.

**3.9 GB RAM, 4 cores.** SUB=2 at 2400×1600 with OIDN did not survive; SUB=1 at
that resolution peaked at 594 MB and was fine. Post-solidify the shell density
difference between SUB=1 and SUB=2 is small at hero distance — **render heroes
at SUB=1 and use SUB=2 only as a guard.**

---

## 2. Reproduce the state

```bash
cd $REPO
T1_SUB=1 T1_VERIFY=1 $BL -b --python build.py     # expect 0 fail, 0 warn
T1_SUB=2 T1_VERIFY=1 $BL -b --python build.py     # expect 0 fail, 0 warn
T1_SUB=1 $BL -b --python audit.py                 # rewrites STATE.md
```

**Both levels must be run.** "Guards green" was true only at SUB=1 for six
revisions while the production build silently lost both cab-door shut lines.

Expected at HEAD (`1c5f8e2`): `TYRE_D=0.6650`, 3 open apertures, `lowered
65 mm`, four shut lines `100 % open`, band `1.372–1.775` un-dropped, bay widths
`0.507 0.516 0.525`, 147 meshes, 0 non-manifold edges, `FAILED_CUTS` empty at
both levels.

---

## 3. What rev 7 changed

Nine commits, `dd7f41e` → `1c5f8e2`.

| | |
|---|---|
| **SUB=2 passes for the first time** | both `gap_door` booleans were collapsing the shell 205562 → 12 v and rolling back. Every hero this project ever rendered was of a bus with **no cab-door shut line**. Cause: the gap outline crossed the front wheel-arch lip. Bottom run raised 0.4248 → 0.780 un-dropped. |
| **The `≥ 20 mm clear of roll-over` lore is refuted** | skip the arch cutters and the identical cutter at the identical z succeeds. Replaced by: *a gap outline must not cross another aperture's lip.* SPEC §10.6. |
| **Boolean guard strengthened, never removed** | the 0.6 ratio could not catch a cutter deleting 39 % of the shell, and a no-op passed silently. The obvious digest **does not work** — EXACT re-tessellates on a true no-op. Vertex-count equality is the only clean test. Validated: 2 true positives, **0 false positives** across 44 measured (cutter, level) rows. Four negative controls fire that the old guard passed. |
| **Geometry set from measurement** | `Z_SILL` 1.372, `Z_HEAD` 1.775, `Z_BELT` 1.207 AG, `V_APEX` 0.340 AG, `V_RISE` 0.867, `V_POW` 0.60. The V-swage apex was **476 mm** out, not the 250 the audit claimed, and the audit's own replacement (0.620) was still 224 mm high. Aperture edges, louvres (10/side), counter (was 983 mm short, now wraps the tail), script decal (was 1.3 m aft and half size), roundel, wipers (were buried 30 mm inside the nose skin). |
| **`RED` was a retired reading** | shipped `(0.5250, 0.0395, 0.0072)` = sRGB(192,56,20), hue 12.5°, sat 0.894 — a **deep crimson**, which §0.2 retires *by name*. Its green channel was 3.6× too low; nobody had converted §3's own measured sRGB(196,106,36) back to linear. Now `(0.5520, 0.1441, 0.0176)`. |
| **Folk art was wallpaper** | it ran at the tile's own alpha in its dense regions and dragged the measured flank from sat 0.816 to **0.27**. Capped at `W_ART = 0.30`. |
| **Weathering built to measured targets** | roughness breakup, Pointiness edge wear through primer to bare steel, dust with a tide line at **h = 0.40 m** (the intuitive 0.75 is ~3× too tall and dusts a band the reference shows clean), sun fade entered explicitly as a design value. No subsurface anywhere. |
| **Physical camera** | 36 mm sensor, f/8, focused on the near front arch, logging its measured DoF (`hero34f`: sharp 7.25–16.71 m, hyperfocal 25.4 m). One long raking strip replaces six rectangles. The rig measured **2.6 EV hot**, which is what let AgX desaturate the flank; energies scaled ×0.165. |
| **`audit.py` stopped lying** | it printed a **hardcoded** belt line for six revisions, near enough to the right value that the status report certified the exact dimension that was broken. Also a hardcoded body half-width and body width, and two stacked bugs that printed the *tail* poles as "nose reach". |
| **`STATE.md`** | machine-written from live geometry, with git SHA and a dirty-tree flag. It caught the height defect in §4 within a minute of existing. |

---

## 4. What is still wrong — measured, not guessed

**The vehicle is 89 mm short, and the cause is now known.** `STATE.md` reports
overall height 1.871 against `REF_MEASUREMENTS` §2.3's 1.960. A grounding pass
**refuted** §2.3's inference that the roof-lid frame stands 0.10–0.15 m proud,
at ~13σ, by a camera-free measurement: roof silhouette *minus* drip rail at the
same column reads 36.6 ± 0.6 px on the factory cab roof and 35.4 ± 0.9 px on
the fixed rear roof — the same structure. A 0.10 m curb would read 20–22 px.
Measured proud height is **26 ± 7 mm**, and `ref_workshop.jpg` shows the open
lid is the cut-out roof skin itself on a shallow perimeter rail, not a box.

**The real cause is the unmodelled rake.** Model crown vs photograph:
**+12 mm at the front axle, −29 mm mid-wheelbase, −67 mm at the rear axle** —
a tilt signature, not a missing curb. The drip rail is straight over
x_img 265→846 (rms 0.4 px) at 33 ± 4 mm/m = **1.9° ± 0.25°**, consistent with
the 1.71° ± 0.4° measured elsewhere. §2.3's 1.960 is the **maximum of a sloping
line** taken at its highest station (X ≈ −1.39, i.e. 0.19 m aft of the rear
axle) and it includes the 26 mm strip.

**This is the highest-value next move.** Replace the scalar drop in `build.py`
step 8b with a shear:

```python
# was: v.co.z -= T.RIDE_DROP
v.co.z -= (0.0365 + 0.0330 * v.co.x)     # rake coefficient 0.0330 ± 0.0040
                                         # (0.0302 from the belt, 0.0367 from the drip rail)
```

Wheel placement must follow (`T.TIRE_R + 0.0365 + 0.0330*x`). **Use a shear,
not a rotation** — every reference number is a height-versus-X, and a 1.9°
rotation also shifts x by 63 mm at roof level. Add `+0.0153` to both
`_rag_grid` offsets in `ragtop()` (0.0075 → **0.0228** canvas, 0.0060 →
**0.0213** frame) for the real 26 mm proud lid. Together these reproduce §2.3's
1.960 to 5 mm **with no raised lid box**. Note `RAG_X0 = +1.4800` is
contradicted — the cab roof dome is unbroken to X = +0.964.

Then **`Z_BELT` becomes a line, not a constant**, and `audit.py`'s height row
must become a three-station roof-line check rather than a single scalar.

**Other open items, in the order I would take them:**

1. **Flank saturation is 0.601 against a measured 0.816** (hue is now 25.2°
   against 26.3°, so hue is essentially solved). Not yet diagnosed. Suspects,
   in order: residual folk-art coverage, the AgX Punchy look, and the fact that
   SPEC's target was measured on a sun-lit photograph that carries its own
   camera tone curve — that last one may mean the target itself needs restating
   as a render-space number.
2. **The tail is 99 mm long** — model −2.108, measured −2.007, factory
   arithmetic −2.009. Fixing it is a loft change. The counter's `X1` was set to
   −2.423 to preserve the *measured* 0.316 m overhang relative to the model's
   own tail, so fixing the tail requires moving the counter with it.
3. **A hero set has not landed.** `out/v7_hero34f.png` and `out/v7_side.png` are
   560 px probes, not deliverables. The strip machinery is committed and
   untested end to end — the first strip call was interrupted. Next context
   should run four strips at `T1_BORDER` 0.00/0.25/0.50/0.75, stitch, and run
   `post.py`.
4. `capvw` is 24 objects for 4 hubcaps — the VW glyph is still six independent
   bars, not the two closed mitred prisms `SKEPTIC_PASS.md` §D specifies. The
   ring diameter and height were fixed; the glyph was not.
5. Six materials still carry a constant roughness: `amber, brass, glass, lens,
   reflector, ruby`. Five are legitimately exempt. **`brass` is not** — it was
   defined locally in `t1_detail._brass()` because `t1_mats.build_all()` has no
   brass key. Fold it in.
6. The bulb string renders unlit pearl white; in the reference it is lit and
   reads warm. Needs an emissive material.
7. Menu cards are untextured white; there is no menu artwork in `tex/`.

---

## 5. Claims I considered and rejected — do not re-open without new evidence

**"The tyre is 0.596–0.606 m, not 0.665."** Raised again by the roof grounding
pass, measuring at column 750. **Rejected.** This is the same error
`REF_MEASUREMENTS` §2.2 already resolved: the short reading comes from taking
the **ground/shadow line** as the tyre edge. The verification pass re-measured
using 72 rays restricted to sectors where the tyre silhouettes against **deep
arch shadow**, and independently killed the "it's perspective" escape with an
ellipse axis ratio of 0.984. The wheelbase/flange ratio of 5.46 ± 0.08 matches
a 16-inch rim (5.44) and is 4σ from a 15-inch (5.77). Donald's brief also flags
tyre-and-ride-height "corrections" as a mistake made more than once. **0.665
and the 16-inch rim stand.**

**"Set `Z_BELT` from sill − 100 mm."** The 100 mm is a *restatement* of two
measurements (sill 1.307, break 1.207), not a physical law. Feeding the model's
own sill into it launders the sill's +27 mm error into the belt and the
relationship then *looks* satisfied while both numbers are wrong. Set each from
its own measurement; let the 100 mm fall out as a check.

**The audit's numbers generally.** 0 of 13 criticals were killed but 11 needed
corrected numbers, and six of its proposed fixes would have introduced fresh
errors. Read `SKEPTIC_PASS.md` §E before implementing anything from
`AUDIT_RECOVERED.md`. The 44 major and 32 minor findings have **not** been
through a skeptic pass at all.

---

## 6. Two process notes

`ref_side.jpg`'s **cab door is open**, swung ~55–60° on its front hinge — proved
by foreshortening (103 px where a T1 door is ~0.90 m) and by the door lines
running at image slope +0.065 against every body line at −0.041. This
invalidates the *method* `REF_MEASUREMENTS` §3(a) used for the belt line,
though not its answer, which was re-derived by a ratio taken on the door itself.
**Do not measure body features on the cab door in that photograph.**

There are **three frames**, and getting them wrong moves everything 65 mm:
geometry constants are **un-dropped**; shader constants are **dropped /
above-ground** (a shader reads `Geometry→Position` off the already-dropped
mesh); and `verify.py` runs **after** the drop, which its own header denied
until rev 7. SPEC §10.1.
