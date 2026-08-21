# LEDGER — rev 50

**Everything this revision measured, changed, refuted, retracted and corrected.** Figures here were
watched print unless a line says otherwise. **Where this ledger and the machine disagree, the machine
is right.**

---

## §0. THE OWNER'S RULINGS THIS REVISION — THREE, AND ONE OF THEM CLOSES W6

| his words | verdict | where |
|---|---|---|
| **W6** — *"A — keep the studio rig as it ships"* | **RULING. W6 IS CLOSED.** Three revisions of refused lighting changes end here, and the red's G/R gap stops being a defect. | §2 |
| **the roof strips** — *"Retire the number"* | **RULING.** The 0.3 m goes, and it was the only thing holding `LID_W` at 1.1100. | §3 |
| **the wipers** — *"Remove all of it including the spindles"* | **RULING. BUILT.** He overruled the survey, which proposed keeping the spindles. | §4 |

> **RULE 34 — NEW. A REQUIREMENT INHERITS ITS OBJECT EXACTLY AS A RETIREMENT DOES.**
> Rev 49 wrote rule 29 — *"a retirement inherits the object it was made about, not the station it was
> seen at"* — at `SPEC.md:10238`, and **four lines later at `:10241`** inherited a *requirement* from
> the very object rule 29 exists to separate. §6.

> **RULE 35 — NEW. A GUARD WRITTEN AGAINST A POSE ENCODES THAT POSE.**
> Three separate guards in this project identify a part's *foot* or *free edge* by `min(y)`. That is
> only the foot while the board leans one way. Two of them aborted correct builds this revision. Ask
> the geometry (a foot is the lowest point), never the pose.

---

## §1. THE BRIEF, GRADED — WRONG IN NINE PLACES, AND ONE OF THEM WAS ABOUT WHAT HE IS WAITING ON

An adversarial agent was set on both briefs **before any work started, and this revision did not
close until it reported.** A second agent verified every §6 premise against the tree. Every item was
then re-checked by hand against the machine.

| # | the brief says | the machine says |
|---|---|---|
| 1 | `verify_clone.sh` ends **ALL 113 PASS** | **122** at rev 49's tip. 113 was true at rev **49c** and was never updated when 49e added nine rows. The carried brief's own §12 says 122 — it contradicts itself. |
| 2 | the branch instruction has been stale **four** revisions | **FIVE.** Rev 50's designated branch measured **0 ahead / 0 behind** while the work sat **29 ahead**, and its remote copy had been **deleted**. |
| 3 | "the TAIL BOARD'S FOOTING, which **SPEC 10.28** has required since rev 12" | **WRONG OBJECT.** §10.28's footing sentence is at `SPEC.md:1009`, inside the paragraph headed *"The detached sign"* — which the same section says *"is not part of this vehicle"*. The cited `SPEC.md:937` is a **blank line**. §6 |
| 4 | the dome "costs **29 %** of the brightness" | That is the **cream** (measured −27.9 %). The **RED loses 41.7 %**, and that figure is in neither `LEDGER_rev49` nor the brief. **He had been choosing without it.** §2 |
| 5 | three artwork states; RED CURRENT = `ref_side`, `ref_rear34` | **INCOMPLETE.** `ref_playa_34.png` (= `IMG_3842.png` = `ref_source.jpeg`) plainly carries scrollwork, the Señor Tacombi script and the Calidad burst — it is **RED CURRENT, a third target frame**, and it is in **no class** in either table. The rev-49 survey found this and it never landed. §5 |
| 6 | §6 A3, *"every duplicated part is a bit-identical clone… the wear field clones too"* | **REFUTED TWICE.** §7 |
| 7 | §6 A18, the contact shadow is missing — **blocking** | **Refuted by its own source.** The shadow is live on the direct path at ratio 0.875; the gating is **latent on the `hero.py` strip path only**. The survey grades it *major, downgraded from blocking*. |
| 8 | §6 A1, *effort: small* | **Not small.** It is coupled to `LID_W`, to the prop struts, to **two** guards that become jointly unsatisfiable, and to an owner-settled roof figure. §3 |
| 9 | `LEDGER_rev49` §10, on the required reading list | **three of its four figures contradicted**: 113 PASS (122), 171 objects (231), 19 ahead (29). Annotated in place. |

**And the survey's "130+ ALREADY RIGHT items so you do not re-litigate settled ground" is misleading
as sold**: the survey's own critic disputes **seven** of them as *"asserted, not checked"* and
**refutes one outright**. Neither brief says so.

---

## §2. W6 IS CLOSED, AND THE TRADE HE WAS OFFERED NEVER EXISTED

He was asked a fourth time — **with the two frames side by side, as he required**, and with the cost
measured on those exact frames rather than quoted.

```
window                       k = 1.0     k = 3.5     cost
cream, cab roof              L 154.5     L 111.4     -27.9 %
red flank under the script   L 128.8     L  75.0     -41.7 %
red G/R                      0.6322      0.5437      -0.0884
backdrop, two 200x140 boxes  255.000     255.000     max|diff| 0.000
                             100.00 % at 255 in BOTH
```

*(Windows stated, rule 8. These are `hero34f`, not the side ortho `probe_rev45_paint` reads, so the
**absolute** G/R values are NOT comparable to the published 0.455 / 0.351 — only the direction and the
size of the move are.)*

**HIS RULING: keep the studio.** What that retires is larger than a lighting setting: **the body red's
G/R gap against the photographed 0.223 ± 0.066 is no longer a defect.** It is the accepted consequence
of a chosen lighting genre, and the street photographs are dimensional references, not colour targets.
Do not re-open it, do not ablate `T1_SPEC` against it, and **do not read a G/R shortfall on any surface
as a paint error.** Landed in `studio.py` at the constant, not only here.

---

## §3. THE LID LEANED AWAY FROM THE COUNTER FOR SIX REVISIONS

`LID_OPEN_DEG = 104.0`, and its own comment said *"leaning over the counter"*. `_hinge` puts the free
edge at `LID_Y_HINGE + LID_W·cos a`, so `a > 90` puts it on the **off** side: it landed at **y −0.8135,
87 mm outboard of the off-side roof edge** and 1.63 m from the counter. Raised at `AUDIT_rev43:117`.

**Corrected to 76.0, and the choice of 76 is the point: `sin 76 − sin 104 = 0.0` EXACTLY.** No z
dimension of the lid moves, no bbox row, no roof-cutter extent, no strut length — the lean flips and
nothing else does. Confirmed afterwards by `STATE.md`: **every measured number bit-identical**, only
the provenance moved. 76° is inside both admissible windows: the photographed taper solve (61–78°) and
the roof's own width (68.9–90°).

**AND THE PROPS HAD TO MOVE WITH IT.** With the free edge over the open aperture, rev 45's
foot-outside-the-aperture guard and rev 44b's `lean < 20` guard became **jointly unsatisfiable**. The
foot is now derived from the pose — it goes on whichever surviving roof strip the board leans over,
which is the **show** side, where both RED and GREEN frames show the stay passing **in front of the
painted face**. Rev 44b's actual fix is KEPT: the tip still meets the board at 0.97 of its width, the
bearing edge, which is what the owner asked for. What is undone is only rev 44b's *own-initiative*
move of the foot.

**`SURVEY_rev49` FINDING 49 IS REFUTED ON THIS SHELL'S OWN ARITHMETIC.** It wants `LID_W` = 1.40–1.49 m.
The aperture starts at the hinge and the roof reaches only `Yt`, so **W ≤ 1.2797 m** — measured at run
time by walking `roof_z` outboard, not typed — or the hole runs off the roof. At 1.45 it would end
**178 mm past the roof edge.**

**AND THEN HE RETIRED THE FIGURE THAT WAS HOLDING IT.** `LID_W` is now **derived**:
`W·sin a = (LID_X0 − LID_X1) / 1.713`, from ref_side.jpg's scale-free board aspect → **1.2237 m**
against 1.1100 typed. The build was **10.2 % short on a pure ratio.** Ceiling: the fragile input is the
hand-read bottom edge, so ±0.03 m; the sign cannot turn over.

---

## §4. THE WIPERS ARE GONE, AND HE OVERRULED THE SURVEY ON THE SPINDLES

Their only warrant was SPEC §4's inventory line under the heading **"Stock 1963 T1"** — inferred from
what the model left the factory with, not measured on this bus — while three in-service photographs of
*this vehicle* show the near pane legible from top rail to sill with **no arm and no blade**. At those
frames' 140–215 px/m a 300 mm arm is 42–65 px; the bobble-fringe balls in the same frames are ~2 px and
are unambiguous. Same evidence class as the over-rider bar he withdrew at rev 37.

The survey proposed keeping `wiper_pivot`/`wiper_boss`. **He overruled it** — the cowl stubs are ~3 px
and could equally be washer jets. Commented, not deleted, exactly as the over-rider is.

---

## §5. A LIVE 17.5 mm DEFECT NOBODY HAD NAMED, IN A FUNCTION FIXED TWICE ALREADY

`T.rrect` is *"centred on origin"* by its own docstring, so `ENGLID_GAP` spans **z 0.6200…1.1200**.
The repository publishes **0.6025…1.1025** in **four** places — same height exactly, centre 0.8525
against the built 0.8700 — and **the fourth is live code**: `trunk_bay()` built its lining from the
typed pair, **17.5 mm below the aperture it lines.**

This is the **third** defect found in `trunk_bay()` in two revisions (rev 49 found the missing material
and the inverted 2 mm inset) and all three are the same shape: **a number about another object, typed
instead of derived.** Both extents now come from `ENGLID_GAP` at run time; the three stale publications
are corrected **in the source**, not only here.

Also landed in the source, not only in a ledger: **`verify.py` printed a pose the vehicle no longer
has, into `STATE.md`** — row 1's length line said *"(the open trunk lid projects aft of X_TAIL)"*
unconditionally, and the owner shut that lid at rev 49. It now names what actually projects, read off
the mesh, and the answer is independent proof the parenthesis was wrong:

```
length excludes opened lids: 4.311 with them, 4.065 without
(what projects: counter, counter_nosing, counter_top, tail_board, tail_board_stay,
 tb_bulbflex, tb_bulbs, tb_edge_dark, tb_edge_red)
```

And the **withdrawn 80 mm was still live justification** at `t1_shell.py`'s `tail_board_stay` —
*"this board stands 80 mm clear on the roof"*, against a built 4.0 mm, opening the comment block a
future context reads to decide whether to re-seat that stay. Rev 49d's commit says it withdrew the
figure *"across the record, not just the source"*; this was the site it missed.

---

## §6. RULE 29 FIRED AGAIN, IN THE MIRROR — AND IT WAS ABOUT WHAT HE IS WAITING ON

**SPEC §10.28 does not require a photograph of the TAIL BOARD's footing.** Its footing sentence is at
`SPEC.md:1009`, inside the paragraph headed **"The detached sign"**, of which the same section says
*"**It is not part of this vehicle**"* — that is **"La Santa"**, the ground-standing board. The citation
carried everywhere, `SPEC.md:937`, is a **blank line**.

And the irony is exact: **§10.123 states rule 29 at `SPEC.md:10238` and breaks it at `:10241`.** Rev 49
refused to inherit a *retirement* from that object, correctly, and then inherited a *requirement* from
the same paragraph. From there it reached `PHOTOS_WANTED_rev49.md` §1, `NEXT_CONTEXT_PROMPT_rev50.md`
§7.1, and the owner's own brief, where it is the stated reason the top wanted photograph is top.

**THE REQUEST STANDS; ONLY ITS PROVENANCE IS STRUCK.** The board's width projects only through
parallax — 33.5 px/m, and being a cross product that coefficient is identical at base and tip — which
bounds it at **W ≤ 0.59 m with no lower bound.** That argument is independent and sound. What the frame
closes is **two** unknowns, not three: the 80 mm dissolved at rev 49d. Corrected in all four carriers.

---

## §7. A BLOCKING FINDING REFUTED TWICE — A3'S WEAR FIELD DOES NOT CLONE

The survey's #3-ranked blocking item rests on a front-vs-rear wheel high-pass correlation of
**0.675–0.708** against a +5 px control of **−0.012**, and concludes the wear field clones because
`WEATHER`/`MOTTLE` are fed Object coordinates.

**Refuted from the source:** `build.py:858-859` states, and `:867` *asserts*, that every mesh carries an
identity transform because `D.place()` bakes into vertex data — so **Object coordinates ARE world
coordinates**, and the two wheels sit 2.400 m apart in a field whose largest feature is 143 mm. And
`MOTTLE_OFS` lives only inside `body_paint()`; it never reaches `capred` / `wheelcream` / `tyre`.

**Refuted by measurement, with the control the original never had.** That statistic cannot separate
*"the texture clones"* from *"the geometry is identical"*. The critic tried to control for it by
restricting to the tyre annulus *"which carries no azimuthally-varying geometry"* — **that is exactly
backwards**: geometry with no azimuthal variation is *identical* at both wheels, so it correlates
perfectly and dominates. Resampling each wheel into polar coordinates about its own hub and
high-passing **along θ** removes it:

```
front vs rear wheel, theta high-passed        box 4.5 deg    box 10.5 deg
  tyre annulus (no vent, no glyph)              -0.007         -0.022
  cream rim ring                                -0.161         -0.089
  hubcap dome                                   -0.100         -0.143
CONTROLS
  front vs ITSELF rotated 37 deg                 0.002          0.010
  front vs white noise                          -0.006         -0.012
```

**My first version of that instrument failed its own controls** — subtracting the θ-mean removes only
`m=0`, so all the smooth shading survived and *"front vs itself rotated 37°"* returned **0.629**. Kept
in `probe_scratch/rev50/a3_control.py` as the record of the failure. **A residual is not a high-pass.**

What survives of A3 is narrow, and largely dissolves with A2: the only genuinely azimuthal features on
a wheel are the five rim vents (which the cap should cover) and the VW glyph (which **both** photographs
show upright, so identical is *correct*). **Do not randomise the glyph angle.**

---

## §8. FOUR OF MY OWN INSTRUMENTS WERE WRONG, AND EVERY ONE IS RECORDED AT ITS SITE

Rev 46 caught five, rev 47 four, rev 48 four, rev 49 four. **Rev 50 caught four, and all four were mine.**

* **A tautology in the replacement lean guard.** I derived the bound from the **rod's own** min/max and
  compared the rod to it — rule 32, in the same edit that cites rule 32. The build aborted with
  *"leans 42.2 deg, past the 5.3 deg its own foot and tip allow"*, because with the foot moved to the
  show side `min(v.y)` is the **tip**.
* **A second tautology in the trunk-bay guard.** It asserted `z0 − min(ENGLID_GAP.z) == BAY_INSET`
  **two lines after** setting `z0` to exactly that. Caught by reading it back, not by running it.
* **An acceptance figure I typed without watching it print.** My new `verify_clone` row counted grep
  **mentions**, not call sites — my own comment three lines above quotes the sibling form verbatim —
  so it read 3 against a typed 2. **Rule 4, fired on the person adding the row.**
* **A harness that reported `rc=0` for renders that had aborted.** `echo "END $V rc=$?"` came *after*
  the redirect, so it reported `echo`'s status. Three baseline renders died on a mid-queue source edit
  and the log said they passed. **Rule 3, in my own instrument** — and it cost the `counter` baseline.

**And the m=5 hubcap instrument failed its first controls too**: taking the last *contiguous* red run
from the centre outward terminated every ray on the VW emblem (median radius 8.25 px on a 33 px dome).
My controls did not include a disc with a central hole. Fixed, re-controlled, and only then run.

**AND A PRE-EXISTING GUARD HAD THE SAME SHAPE OF ERROR:** rev 45's foot guard identified the foot as
`min(y)`, true only while the board leaned the wrong way. Rationale kept, shape corrected (rule 5).

---

## §9. WHAT WAS MEASURED, WITH ITS CEILING

* **A2, the hubcap.** The disc crosses in front of the cap at **r = 0.11973 m**, reproduced three
  independent ways to 0.2 mm: by hand from the two authored profiles, from my calibrated m=5 instrument
  on a fresh render (median red radius 32.50 px = 0.11985 m at the side ortho's 271.19 px/m), and by
  eye. The five-fold is unambiguous: render **m5 0.051–0.060** across four thresholds on **both**
  wheels with m2,m3,m4,m6,m7 all ≤ 0.007; `ref_side.jpg` **0.013–0.024** and *not separated* from m2
  (up to 0.176). Controls: perfect circle 0.0004, synthetic 5-petal at +8 % 0.0805.
  **NOT FIXED, and the reason is the finding:** two mechanisms produce the identical image — the cap
  ~48 mm too far inboard, or the disc not dishing — and **neither depth is measured anywhere in the
  repository.** Moving the cap the full 49.7 mm puts its apex **60.2 mm proud of the rim flange**, which
  the photographs refute; dishing the disc instead cuts a **55 mm cliff** into a cream annulus the
  photographs show smooth. Rule 29.3: no finding is attributed to a cause until a control separates it.
  *Ceiling: my m5 normalisation is 2|F_m|/n/mean, twice the survey's convention — my numbers are
  internally comparable and must NOT be compared to its published 0.0399.*
* **A11, the cab door handle.** `z = 1.330` typed three times, uncited, **58 mm above** `Z_BELT_AUTH`,
  so it rendered on the cream. Measured on the **RED target bus in its current artwork** — a door swings
  about a vertical axis, so `ref_side.jpg` is admissible for the station even with the door open.
  Column band x 168..200: break row 438.1, glazing sill row 419.8, handle row 477 with **R−G collapsing
  119.5 → 30.3** (achromatic chrome, not paint and not a shadow). **Quoted as a ratio: 2.126
  band-heights below the belt**, against the green bus's 2.24 — 5 % apart, different vehicle, different
  artwork state. *I nearly published a metric drop and it does not survive:* the band is 0.136 m on the
  survey's render reading and 0.100 m on `Z_SILL − Z_BELT_AUTH`, a **32 % swing** moving the answer
  from 0.219 to 0.289 m. The metric value is therefore derived from the model's own band at run time.
* **A10, the tail lamps.** `small_lamp()`'s profile starts **on the axis**, so the mounting plane and
  the dish's deepest point are the same plane and the 4.0 mm "standoff" buried the lens centre: the skin
  cut the dish at **0.1811 r**, a **Ø33.2 mm disc of body red** at each lamp's middle. Confirmed
  photometrically — the core reads G/R 0.299 / B/R 0.191 against the paint's 0.277 / 0.174 and the lens's
  0.584 / 0.287. **The maximum admissible insertion is zero, and that is not a choice.**
* **A16, the menu header.** `'&'` at **0.728** of the strip height against the file's own declared
  **0.460** — 1.58× — now **0.474**, with the other four words bit-unchanged.

---

## §10. THE STATE OF THE MACHINE

```
bootstrap.sh      ALL 10 PASS
verify_clone.sh   ALL 125 PASS   (122 at pickup; 3 added, 2 re-based, NONE relaxed)
build             T1_SUB=1  VERIFY: 0 fail, 0 warn
                  BBOX L=4.000 W=1.750   223 meshes, 0 bare materials
STATE.md          REGENERATED FROM A CLEAN TREE -- the first in five revisions.
                  Rev 49 wrote rule 33 about exactly this and then regenerated
                  from a tree its own provenance table records as DIRTY.
branch            36 ahead / 0 behind origin/main
renders           out/ is NOT tracked and starts EMPTY.  Re-render before any
                  probe that reads a frame.
```

**GUARDS ADDED THIS REVISION, EVERY ONE WATCHED FAILING ON THE REAL DEFECT:**

| ablation | reproduces |
|---|---|
| `T1_LIDDEG=104` | the mural lid leaning away from the counter |
| `T1_BAYSTALE=1` | the trunk bay lining 17.5 mm below its aperture |
| `T1_LAMPSINK=1` | the tail lamp's 4.0 mm insertion |
| `T1_LIDASPECT=1.2` | a lid width past the roof edge (reports 467.2 mm) |
| `T1_HANDLEHI=1` | the cab handle above the belt |

Rev 49's `T1_BAREMAT`, `T1_TBFOOT` and `T1_BAYPROUD` all still fire.

**DISPATCHED AND REPORTED:** the brief refuter and the premise verifier both returned before this was
written and **both changed the conclusions** — the refuter found the §10.28 mis-attribution and the
A18 mis-grading, the verifier refuted A3's mechanism from the source and proved the tail-board foot
finding stale. A third agent (frame measurement) was dispatched and **had not reported when this was
written**; its brief is recorded in §11 of the handoff so rev 51 can re-issue it.
