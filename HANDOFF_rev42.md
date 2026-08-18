# HANDOFF rev 42

**GEOMETRY MOVED.** For the first time since rev 38. His **defect report 5 —
"the doors extend lower, around the wheel well"** — is built, off two readings
he gave of `ref_workshop.jpg`. Guards **0 fail / 0 warn at both levels on both
tools**; 131 objects, 190 meshes, 42 materials, 5 constant-rough, **0
non-manifold at both levels**. **All 30 inherited probes re-run on the moved
geometry and all 30 reproduce their published tallies.**

And the project's oldest un-instrumented requirement — SPEC §5's *"Decals
3K-4K, **non-overlapping**"* — is measured for the first time in forty-two
revisions.

---

## 1. Arrival

* `get_device_info` called at **13:06:36 UTC**; folder already in
  `connectedFolders` — **eleventh revision running**. Step 0 kept anyway, not
  assumed.
* **AN ABSENCE HAS A TIMESTAMP TOO, and this revision's said so.** The
  recursive listing ran at **13:07:05 UTC** and found all six rev-41 artefacts
  at their recorded sizes. When I looked is stated, per rev 41's own headline
  defect.
* `_xfer33/` parts reused for the **ninth** revision, sizes checked
  byte-exactly first: **19,478,840** and **8,519,034**, both exact.
  **36 files in 3 bridge calls, ZERO drops.**
* Restore CLEAN 34 → 59 → *(fetch rev14b)* → 67 … → 215 → **222**. Rev-41
  bundle md5 `e73db125f50213529c799da73d9be209`, matching its recorded value.
  **30/30 content checks exact, 20/20 ancestry, 3/3 texture md5s, 30 probes,
  hero correctly absent.**
* `STATE.md` provenance checked BEFORE trusting it: `working tree | clean`,
  commit `5f5d3b3` = **commit 216, a reachable ancestor** of HEAD 222, and
  216..222 touches only doc files. The parent-provenance pattern, not
  staleness.
* **`MIGRATION_APPENDIX_rev32.md` is still a phantom** — 0 files in the tree,
  0 paths in the whole git history across every ref. **Sixth check.**

## 2. One correction to the inherited brief, and it is a wording one

The rev-42 prompt lists `probe_rev39_flank` as *"3/0 and NO RULING on
flatness"*. Its controls are 3/0. Its own summary line reads:

> `VERDICT (derived): spread 415 mm exceeds the 30 mm bar -- NOT flat, so the
> offset-versus-scale question is NOT settled here.`

Same substance, different words. Quoted from the probe, not from the brief —
§10.90.10's lesson. Its JOINT registration reproduces **(−1, −4) px = (−5 mm z,
−19 mm x)** exactly, which per §10.99 is the only part of that instrument that
may be cited.

## 3. Item 1 — REPORT 5 IS BUILT.  SPEC 10.100

### 3.1 What was wrong, and why it looked unmeasurable

`DOOR_GAP` cut the cab door's bottom as a **straight chord across the top of
the front wheel arch**, z 0.8000–0.8160 un-dropped, **14.6–30.6 mm ABOVE** the
crown at 0.7854. rev 7 through rev 41 all shipped it.

§10.62 and §10.73 record that **no supplied frame carries both a closed cab
door and an admissible px/m on the door plane**. `ref_side.jpg` has the door
**OPEN 49°**; `ref_workshop.jpg`'s only locked ruler is on the nose plane at a
catalogue 0.180 m, and REF §9 warns lateral scale there varies **>2:1**.
**Rev 42 takes no metric from that frame.**

### 3.2 What was measured — ordinal, so it needs no scale

The cab door's **front shut line** in `ref_workshop.jpg` fits
`x = −0.03467 v + 512.233` over 49 rows and runs **continuously from the belt
to the body's lower edge at v = 712**, which is **~91 px BELOW the arch crown
at v ≈ 621**. The build put it ABOVE. **The sign was wrong, and a sign does not
need a ruler.**

**A CANDIDATE LINE I NEARLY PUBLISHED DID NOT EXIST.** My first marked figure
drew a near-horizontal "door bottom" across x 500–585 at v ≈ 692. Contrast
stretched at 9× with no overlay, that region is FLAT — ridge scores 4–8 against
a noise floor of 3.5–5.5. **The line was my own annotation, read back as
evidence.** Caught before the figure went to him.

### 3.3 His two readings

*[stated, rev 42]*, off one 9× crop with three marks:

* **"the door extends down to the side rocker it looks like"** — his hedge kept
  verbatim.
* **The door's rear lower corner sweeps UP AND OVER the front wheel arch** —
  the arch's front lip is part of the door. **YES.**

rev 36's one-crop-one-mark-one-sentence format, paying again. It settles the
**SHAPE**, not any magnitude, and no magnitude is claimed.

### 3.4 The construction — not one new constant

    z_bot(x) = max( ZB(x)+G , arch_z(X_AXLE_F) + sqrt((ARCH_R+G)^2 - (x-X_AXLE_F)^2) )

The arch is the build's own circle; the rocker is `t1_core.ZB`; and **G is read
off rev 41's own outline** — `DOOR_ARCH_G` = the minimum radial clearance rev
41's smoothed `DOOR_GAP_S` kept from that circle, **0.024426 m**. So the new
outline is **nowhere closer to the arch than the one that has been passing
T1_SUB=2 since rev 23**.

Door bottom now **272.2 mm lower at the rear corner, 387.5 mm lower at the
front corner**.

**THE GUARD FIRED ON MY FIRST ATTEMPT AND WAS RIGHT** — smoothing pulled the
arc to 0.0225 m against rev 41's 0.0244 m. **The guard was not relaxed by
1.9 mm.** The construction solves by **fixed point** for the build clearance
that makes the *smoothed* outline land on rev 41's value: `_G_BUILD`
**0.026278**, smoothed minimum **0.024421** against **0.024426**.

### 3.5 The guard is RE-SCOPED and its new rationale stated

rev 23's rule. The old assert's "10 mm above the CROWN" was a **proxy** for the
real invariant — the outline must not **cross the arch lip**, the condition that
collapsed the shell **205562 v → 12 v at SUB=2 for six revisions**. A door that
wraps the arch violates the proxy and satisfies the invariant. Now a **radial**
clearance, armed at rev 41's own value. Plus a 10 mm absolute floor and a new
assert that the outline stays off the body's lower edge (**26.3 mm**).

### 3.6 What is NOT changed — named, not absorbed

`DOOR_GAP` is **bit-identical** and keeps its second job as the **ART DATUM**:
`folk_gen` parses it for `DOOR_H = 1.013467`, which divides every v-coordinate
of the door art. Re-pointing it moves `DOOR_H` ~390 mm and forces a re-bake —
a second lever, exactly what rev 25 refused. **The art frame is still rev 41's
and that is REV 43's ITEM 1.** Three texture md5s unchanged by construction.

### 3.7 Cost to the guards: nothing

**0 fail / 0 warn at both levels on both tools.** Every inherited figure
identical. **Two figures move and both follow from a longer outline:** cut roof
hole **68564 → 70069 v** (SUB=1) and **252749 → 254428 v** (SUB=2).
Re-baselined and flagged. **The SUB=2 shell did not collapse.**

## 4. Item 7 — THE UV AND TEXTURE CHECK.  SPEC 10.101

Claim checked before acting: `grep -ric "uv overlap|texel densit|
non-overlapping"` over SPEC, REF_MEASUREMENTS and every `.py` returns **one
hit — SPEC:319, the requirement itself.** Never run, confirmed.

`probe_rev42_uv.py`, NEW, READ-ONLY. **5 controls, 1 FAILED (C3), and the
failure is published rather than tuned away.**

* **THE CENSUS IS ALREADY A RESULT.** Seven image nodes; **one meets §5's own
  3K floor**. `nose.png` is **1024×1024**. `lidsign.png` is loaded by a material
  worn by **no object**; `tex/emblem.png` is referenced by nothing at all.
* **THERE IS NO UV LAYOUT ON THE BODY.** `swirl`/`swirl_b` are **BOX**
  projections from object coordinates; 20 of 190 meshes carry a UV layer and
  `T1_body` is not one. "Non-overlapping UVs" is not merely unchecked there —
  it is not well posed. `folk_gen`'s own `XART_LO` comment already records a
  texel collision (*"x = -2.029 is the same texel as x = +1.817"*) and works
  around it by restricting where art is painted.
* **SELF-OVERLAP vs REUSE, and pooling them manufactures a defect.**
  `senor.png` scores **100 % pooled** across `script_L` + `script_R` and
  **0.00 %** per object. Split properly: **TOTAL SELF-OVERLAP 32.5746 m² =
  55.97 %** of 58.2048 m² painted; a further 3.13 % is legitimate reuse.
  **`swirl` 83.04 %, `swirl_b` 48.36 %, `nose` 11.54 %, and EVERY hand-made UV
  layout is 0.00 %.**
* **TEXEL DENSITY**, area weighted medians: calidad 4657, senor 3197, lidmural
  1106, nose 648, swirl_b 531, swirl 532 texels/m. Against the hero's own
  **1180.8 px/m** (derived, and labelled as derived), the three lowest deliver
  **0.45×, 0.45× and 0.55×**.
* **TWO ESTIMATORS WERE KILLED BY CONTROLS BEFORE THIS ONE**, both kept in the
  probe: a point sampler C3 killed (5.34 → 6.10 → 10.98 % as sampling got
  denser — it measured my sample count), and a conservative raster C2 killed at
  **99.95 %** (a flat quad "self-colliding") and C5 killed at **+53.8 %** area.
* **A DEFECT OF MINE CAUGHT BY ARITHMETIC, NOT BY A CONTROL.** The triangle
  cache was keyed without the object list, so the per-object pass printed
  self-overlap of **571.71 %** of the painted area. **A fraction over 100 % is
  impossible** — the only reason it was caught in one read.
* **THE SELECTOR IS PARSED, NOT ASSUMED.** The first cut hard-coded my reading
  of `T1_paint`'s Mix chain. If the split were on the NORMAL rather than the
  POSITION, the solidified shell's inner skin would go to the other tile and
  the compared sets would not be the renderer's. Now evaluated from the graph;
  anything unrecognised RAISES.
* **C3 FAILS AND THE VERDICT SURVIVES ANYWAY, and both are stated.** `TOL_M`
  moves the answer **0.00 pp**; `CELL_K` **8.41 pp**; `C_FOOT` — a parameter I
  introduced — **8.04 pp**, all against a stated 2.0 pp tolerance. The figure is
  good to ±8 pp and no better. **But every value in the whole sweep, 59.06 % to
  67.50 %, lies on the same side of the 10 % bar stated before the run.**

**NOTHING IS REPAIRED HERE.** Fixing it means giving `T1_body` a real UV
layout, which is a re-bake of every flank texture — **coupled to §10.100.6's
re-bake, and neither should be done alone.**

## 5. What rev 42 shipped

* Build files touched: **`t1_shell.py` only.** No shader, no artwork, **3/3
  texture md5s unchanged**.
* New: `probe_rev42_uv.py`. **31 probes now.**
* `probe_rev39_flank`'s JOINT registration still **(−1, −4) px** on the moved
  geometry; `probe_cross_anatomy` still show flank **0.0 mm** / off flank
  **804.9 mm**; `probe_dust_scope` still 8/0.
* **A HERO IS OWED AND WAS SHOT** — the geometry moved. See §11 of the rev-43
  prompt for its figures.

## 6. Open, in the order rev 43 should take them

1. **THE ART FRAME.** `DOOR_H` is still rev 41's; the door is ~390 mm deeper
   than the frame its art was baked into. Coupled to item 2.
2. **THE BODY HAS NO UV LAYOUT.** 55.97 % self-overlap. Same re-bake.
3. **REPORT 3's remaining independent route** — the counter top's INNER edge in
   `ref_rear34.jpg` at y 423, x 700. §10.99.6.
4. Report 4 (the VW glyph, §10.94); Report 7 (Calidad, `cal_gen.py:246`,
   texture-versus-panel first); `V_POW` (`t1_mats.py:149` / `t1_shell.py:1086`).
5. `probe_clean_top` / `probe_dust_anchor` — **TEN revisions**.
6. **`lidsign.png` is worn by no object and `tex/emblem.png` by nothing at
   all** — reported in rev 42, not touched.
