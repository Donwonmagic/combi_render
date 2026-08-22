# NEXT CONTEXT PROMPT — rev 52

**Read this whole file before you touch anything.** Then `CLAUDE.md` (new at rev 51 — method only,
loads every session), then `LEDGER_rev51.md`, then `SURVEY_rev49_photoreal.md` §6 (still the work
list). `LEDGER_rev49.md` §10 carries three figures the machine contradicts and is annotated in place.

---

## §1. START HERE — MEASURE THE BRANCH, DO NOT TRANSCRIBE IT

```bash
cd /home/user/combi_render
git fetch --unshallow 2>/dev/null || true      # verify_clone fails on a shallow clone
git fetch --all --prune
for b in $(git branch -r | grep -v HEAD); do
  printf "%-52s ahead %-3s behind %s\n" "$b" \
    "$(git rev-list --count origin/main..$b)" "$(git rev-list --count $b..origin/main)"
done
git diff --name-only HEAD...origin/main        # <- HIS PHOTOGRAPHS ARRIVE HERE
./bootstrap.sh          # ALL 10 PASS  -- the BRANCH CHECK IS ROW 9, not row 10
./verify_clone.sh       # ALL 127 PASS -- and read what its verdict block now says
```

**THE BRANCH INSTRUCTION HAS NOW BEEN STALE SIX REVISIONS RUNNING.** At rev 51 the designated
branch's remote copy had been **deleted** (`fetch --prune` printed `- [deleted]`) and HEAD measured
**0 ahead / 0 behind** while the work sat **39 ahead** elsewhere. HEAD was a strict ancestor; it
fast-forwarded and nothing was lost.

**AND THE SHAPE CHANGED MID-REVISION, SO DO NOT ASSUME THE OLD PATTERN.** `origin/main` moved while
rev 51 was running — a pull request merged the rev-50 branch into it — so every historical branch now
measures **0 ahead**. Caught only because `git rev-list --count origin/main..HEAD` came back **3**
when it should have been 42, i.e. **by re-measuring rather than trusting the count taken at pickup**.
Re-measure both at the start AND before you finish.

> **"row 10" IS WRONG AND EVERY BRIEF THROUGH REV 51 SAID IT.** The machine's own numbered output:
> row 8 clone depth, **row 9 "no branch carries work HEAD does not have"**, row 10 `verify_clone.sh`.
> Believe row 9 over any sentence in this file.

---

## §2. HIS REPORT AT REV 51, AND IT IS THE TOP JOB

> **"The vw on the hubcap is not the right scale either, just like the front emblem."**

**REV 51'S OWN FIX MADE IT VISIBLE, AND THAT IS THE INTERESTING PART.** `CAP_EMBLEM_D` is a fraction
of the cap's **full geometric** diameter. The emblem's absolute size never changed — but what is
VISIBLE did, because rev 51 seated a cap that had been buried:

```
emblem absolute diameter                       0.08686 m   (unchanged)
BEFORE the seat: visible red disc 0.2360 m  ->  emblem / visible = 0.3680
AFTER  the seat: visible red disc 0.2748 m  ->  emblem / visible = 0.3161
built ratio to the cap's FULL diameter                       = 0.3170
```

While the cap was buried the visible disc was 16 % too small, which made the emblem read 16 % too
**large** — landing near what the photograph shows. **TWO ERRORS WERE CANCELLING.** Fixing one
exposed the other. Same shape as rev 49's tail board and rev 44's hubcap colour.
**When a fix makes a neighbouring feature look worse, suspect a cancelling pair before the fix.**

---

## §2b. CLOSED BY HIM — DO NOT RE-OPEN, DO NOT RE-ASK

These are settled rulings. A fresh context that re-opens one burns a revision on a question he has
already answered, and he has said so.

| his ruling | what it closes |
|---|---|
| **W6 — *"keep the studio rig as it ships"*** (rev 50) | `T1_SOFTEN` stays 1.0. **The body red's G/R gap against the photographed 0.223 +- 0.066 IS NO LONGER A DEFECT** — it is the accepted cost of a chosen lighting genre. Do not re-open it, do not ablate `T1_SPEC` against it, and **do not read a G/R shortfall on ANY surface as a paint error.** The street photographs are **dimensional references, not colour targets.** |
| **the roof strips — *"Retire the number"*** (rev 50) | The 0.3 m is gone from the record. `LID_W` is DERIVED, not typed. Landed in the source at rev 51 (it had only half-landed). |
| **the wipers — *"Remove all of it including the spindles"*** (rev 50) | Withdrawn entire, **commented not deleted**, and locked by a `verify_clone` row. He **overruled** the survey, which proposed keeping the spindles. Do not re-add them. |
| **the lower bay SHUT, only the rear window open for service** (rev 49) | `TRUNK_OPEN_DEG = 0.0` means SHUT and the swing is **skipped, not run at zero**. Rev 48's contrary inference is refuted; its text is still live in two source comments and should be struck (§5). |
| **the RED bus is the target; geometry transfers between vehicles, PAINT AND ARTWORK DO NOT** | See §6. |
| **the raised board at the tail IS on the vehicle** (rev 49) | The retirement that looked like it applied belongs to the DETACHED "La Santa" ground sign. Rule 29. |
| **the marks above the Calidad burst are STARS**; the flower mural with yellow menu strips is correct as built; the over-rider bar and posts withdrawn (rev 37); the rear bumper removed at the conversion and must not return | — |

**AND THE DELIVERY GENRE IS SETTLED WITH W6:** the white-studio product look IS the deliverable.
`playa_env.py` is a 1695-line dormant subsystem and reviving it as the delivery frame is **not** on
the table — do not re-propose it.

---

## §3. WHAT REV 51 FIXED

**A2, the five-petal hubcaps — MEASURED, then fixed, then rendered and looked at.** How proud the
dome stands, recovered from photographs by a **shape-free** estimator (the emblem sits on the axle
axis, so its projected offset from the cream-ring ellipse centre carries h with no dome profile
entering): weighted **52.2 mm, 1sd ~7**, from three frames at three obliquities. As built **10.5 mm
— EXCLUDED at 5.8 sigma**; seated **58.2 mm — CONSISTENT at 0.8 sigma**. Every control passed,
including the negative one (`ref_side.jpg` at phi 10.5 deg correctly returns UNRECOVERABLE) and a
positive one on a render where the answer was KNOWN (reads 12.6 +- 9.2 against a true 10.5).
`CAP_SEAT_DY` is **derived** from the two profile tables, not typed. After, quoting the ledger's own form and BOTH wheels: m5 across four thresholds
**0.0487..0.0565 -> 0.0005..0.0019** (circle control 0.0000); the vent notch signature
**0.1295 / 0.1314 -> 0.0055 / 0.0148** against photographs at 0.0024-0.0150.
**CEILING, carried:** the FRONT wheel's 0.0148 is inside the photographic range by 0.2 %, and a
residual 5-fold persists there in a band clear of both vents and cap lip — **A5 0.0100 at SNR 5.4**
against the rear's clean 0.0047 / SNR 1.8. **Unexplained.**

Also: the **0.3 m roof-strip retirement landed in the source** (it had only half-landed at rev 50 —
six superseded statements were still live, including *"THAT IS AN OWNER QUESTION (rev 50 C3)"* which
he had already answered); the tail-board foot guard **relabelled** as the construction-consistency
check it actually is; `verify_clone`'s score **split** into FIDELITY vs SELF-CONSISTENCY; a
`CLAUDE.md` written and guarded.

---

## §4. WHAT IS REFUTED — DO NOT REBUILD THESE

* **"the cap's DOME DEPTH is wrong."** Proposed at rev 51 as a third mechanism and **REFUTED by the
  measurement**: implied depth 64.5 mm against the authored 70.5, inside 1 sigma. The authored
  profile is right; only its mounting was wrong. `CAP_R` stays locked — it is a **RADIUS**, validated
  against a ratio of two **DIAMETERS**, and it never bore on depth.
* **"moving the cap outboard is refuted by the photographs."** The rev-51 brief said so. **The
  photographs SUPPORT it.** Fix (a) was correct all along.
* **The rev-50 m5 "convention conflict."** `LEDGER_rev50` §9 states as its own ceiling that its
  normalisation is *"twice the survey's"*, and a rev-51 adversary escalated that to "mutually
  impossible". **Both are wrong.** Cross-applying the two normalisations to the two control shapes:
  they agree to 2.5 %; it is the **CONTROL SHAPES** that differ 2x (the survey's is
  `np.clip(np.cos(5*th),0,None)`, half-wave rectified, whose fundamental is half its peak).
* **Everything rev 50 refuted still stands**: the wear field does NOT clone; `LID_W` is bounded by the
  roof at **W <= 1.2797 m** (the machine's own walk, Yt 0.7347 — *the 178 mm published twice in
  `t1_shell.py` was from the record's stale Yt 0.7273 and is now corrected to 170.3*); the contact
  shadow is live on the direct path; the tail board's foot is fixed.

---

## §5. THE WORK LIST FOR REV 52

**ORDERING, STATED HONESTLY:** item 1 is his most recent report and is **blocked** on a photograph for
its decisive half. **Item 2 is the highest value-per-minute in this file and is NOT blocked — if you
only do one thing, do item 2.** Items 3 onward are unblocked and sequential.

**1. THE TWO VW BADGES — HIS REPORT, AND IT IS ON TWO PARTS.**
Both are built by **one generator**, `T.vw_bars(R, w, ...)`, each passing its own stroke-width
fraction: nose `vw_logo_fit(..., wfrac=0.1986)`, hubcap `CAP_EMBLEM_WFRAC = 0.2087`. **Neither is
measured**, and the hubcap's declares its own provenance: `# w/R as authored (0.0072 / 0.0345),
kept`. **0.0345 was the OLD emblem radius.** rev 14 BUILT it (`0.1897   built (rev 14)   -> 7.0 sigma`); the 7-sigma finding and the correction to 0.3170 are **rev 15's**. The
DIAMETER was fixed and the STROKE RATIO WAS KEPT from the wrong-sized object.
**THE DIAMETER ROUTE ON `ref_side.jpg` IS EXHAUSTED — DO NOT RE-RUN IT.** Rev 51 already did exactly
the calibration this item would otherwise prescribe: a synthetic emblem at KNOWN ratio and KNOWN blur
at that frame's own scale, swept over its declared PSF sigma. It returns a true emblem/cap of
**0.3474** against the built **0.3170** — **9.6 % small, but only 1.8 sigma** against the record's own
declared +- 0.017. **Not enough to change a constant on, and re-running it gets the same 1.8 sigma.**
**THE UNTOUCHED CONSTANT IS THE STROKE WEIGHT**, which no frame has ever been compared against.
**DIAMETER and STROKE WEIGHT are two constants and only the first has ever been compared to a
photograph.** Calibrate on a synthetic emblem at KNOWN size and KNOWN blur before touching a frame.
**KNOWN-CLOSED ROUTES, do not re-try blind:** `ref_workshop.jpg` for the nose stroke width (the rev-49
survey dropped it — *"too oblique to measure a perpendicular width from"*); `IMG_2073.jpeg` by
automated mask (rev 51 tried it; **chrome is hostile to threshold segmentation** — the "cap" mask
selected the painted rim and the "emblem" mask a dark environment reflection).

**2. REVIVE THE FIDELITY LANE. IT ALREADY EXISTS, IT RUNS, AND IT IS RED.**
`flank_compare.py` is a render-vs-photograph gate that exits non-zero. **Last touched at rev 40, with zero LEDGER
mentions since rev 43** — it IS named in the rev-41/42/43 prompts and three times in
`SURVEY_rev49`, so "zero mentions anywhere" is too strong — and its only appearance in the
acceptance surface is
`ck "_assert_same_edge" 4 "$(grep -c ...)"` — *the fidelity test is being grepped for a symbol count
instead of run.*
**`out/` IS NOT TRACKED AND STARTS EMPTY — render one side view first, then run it.** That is the
only Blender this item needs, and the run itself is about fifteen seconds. Rev 51's result, on its
own render:

```
FAIL ink area ratio   0.8753            target 1.000 +/- 0.10
FAIL ink aspect       2.3689 vs 2.2512  target within 5 %
PASS IoU vs ceiling   0.7362            target >= 0.7303
FAIL worst region     0.174 (Senor)     target >= 0.75 of that region's own ceiling
EXIT=1
```

**READ THE INSTRUMENT'S OWN BANDS BEFORE CHASING ANY OF THIS — TWO OF THE THREE FAILS ARE INSIDE
THEM.** The same run prints `ratio render/reference 0.8753 +/- 0.0244 ... read against the render
mask's own coverage band, +15.8 % / -6.7 %`: at the 25 % threshold the ratio is **1.0136, inside the
1.000 +- 0.10 bar**. And the aspect FAIL flips on which vertical calibration is used — the same run
gives **+2.86 %, inside the 5 % bar**, using the map's own scale instead of `k_t`, and `SURVEY_rev49`
says `k_t = 215.5 px/m` **"is known to be wrong somewhere"** with the two calibrated instruments
disagreeing by 2.3 % *with the sign wrong*. **ONLY THE WORST-REGION NUMBER IS ROBUST.**

**"Senor" reads 0.174 of its own measured ceiling.** That is the word he has reported unclear THREE
times, carrying a number the whole time — *though not the same number: `LEDGER_rev44`/`rev45` carry it
as **0.459** of its ceiling in the open-findings register. Reconcile them; do not assume a typo.* Check `cream_rms.py` and `mark_rev45_ba.py` for the same
shape. **This is the highest value-per-minute item in the file.**

**3. A6 — THE CURVATURE EDGE-WEAR SPECKLE.** The loudest CG tell, and it survives W6's closure
because it is texture, not light. Baseline re-measured at rev 51 with windows **verified by eye**:
counter fascia **17.06 %** dark coverage against `ref_side.jpg`'s **0.62 %**; three nose/cab cream
windows on the **subdivided** shell return **0.00 %**. *Honest caveat: that is NOT a single-variable
control — the fascia is `countercream` (WEAR 0.7) and the shell windows are `paint` (WEAR 0.55), on
two different renders. The 1.27x wear ratio cannot explain 17 % vs 0 %, so the Pointiness diagnosis
survives, but two things moved, not one.* Controls: flat cream +
0.5 DN noise 0.00 %, flat cream + 7.6 % known chips 6.58 %.
*Mechanism, by string:* `W_PT_LO, W_PT_HI = 0.520, 0.600` gates the chip mask on Pointiness, which is
0.5 on a flat face, so any low-poly convex vertex clears 0.600 and `pw -> 1.0`; `deep` is fed **from
`pw`**, so it saturates too. **Both gates, structurally.**
*Two things the rev-51 brief got wrong here:* `T1_CTAN_WEAR=0` **HAS** been exercised
(`probe_ctan_pedestal.py` arms 3 and 4, radiances stored), **and it is not a clean ablation** — the
same file records it as *"TWO levers: also drops Metallic"*. You need a lever that moves the chip
gate alone.
*The fix is well-grounded and NOT yet shipped:* `round_edges()` already splices a Cycles
`ShaderNodeBevel` into every Principled BSDF's Normal input, and a Bevel node **ray-traces a real
radius in world units** — mesh-density independent in exactly the way Pointiness is not.
**STATED CEILING on the A6 statistic:** a local-median threshold count is **structurally blind to the
large-cell, low-contrast MOTTLE** visible on the same cream in the same crop. It is true for CHIPS
and says nothing about the mottle.

**4. A7 — the rear serving aperture renders as a black cavity.** The internal control is sound and
needs no photograph: the model's own side bays read median 188.5 / 124.4 against the rear aperture's
26.2.
**BUT THE "573 mm OF UNDRESSED BOX" FRAMING IS REFUTED — BY THE SURVEY'S OWN ADVERSARY, UNDER THE
HEADING "WHAT I BROKE".** `gal_end_a` is `_gbox("gal_end_a", X0 - 0.030, X0, -0.5000, 0.4000, 1.2000,
1.8600)` with `X0 = -1.3000` — a white slab that **covers essentially the whole aperture in
projection** and was placed deliberately. **The defect is ILLUMINATION, not dressing**, and the
prescribed fix (extend the aft wall to the tail station) is wrong: it moves an unlit wall 573 mm
closer without lighting it and deletes depth the photograph does show. **DO NOT BUILD IT.** The
mechanism the same block gives is the real one: `roof_cutters()`'s aft edge is `LID_X1 = -1.0700`, so
**803 mm of roofed body sits between the last light inlet and the tail skin.**
**And a second hole, which stands:** `gal_end_a` spans y -0.500..+0.400 against an aperture of
+-0.520, so **120 mm of the show side sees past the end wall**. *Imprecision to carry:
"the ONLY aperture his ruling leaves open" is wrong — `STATE.md` says `open serving apertures on +Y:
3`. It is the only REAR/service aperture open.*

**5. A9 — the galley is ~103 mm too far aft** *(the survey's §6 headline says ~106 mm and quotes the range as +0.096..+0.113; **both are wrong** — the machine's twelve per-feature deltas run -0.09574..-0.11035, mean 103.0 mm, and no feature reaches 0.113. Correcting the record, not silently.)*, and the offset is **NOT rigid**: -0.09574 (hook u=0.13)
to -0.11035 (`gal_appliance` u=0.80), so a single additive constant leaves **+-7.3 mm**. Re-derive
each X from `BAYS`. Separately `gal_rail` is **165 mm too LONG** (the survey's headline mis-signs it;
its own body says built centre -0.380 length 0.660 against a measured -0.598 / 0.495) and 218 mm too
far forward; `gal_caddy_fill`'s X inset has the wrong sign.

**6. A11's SECTION, A19, A14** — a chrome lever lying in a dish **pressed into** the skin against a
12 mm **proud** prism; both headlamps and both indicators placed with **zero rotation** (there is no
symbol `IND_X` — X alone is a bare literal, typed twice, which is the point); both `lid_rail` objects
**zero-area** via `_rag_grid` called with `x0 == x1`, and the rail's WIDTH is measured nowhere.

**7. A13 / A16 / A12** — the isolated star built BELOW the burst where both red frames put it above;
every flank rosette drawn at the diameter of its **gold core**; the built "Senor" does not resolve as
a word — **and item 2 now gives that one a number.** *A12 is an OWNER RULING, not a do-now:*
`senor_trace.py` calls the remedy *"inventing ink the photograph does not show"*.

**AND THE GUARD GAP ON THE PART JOB 1 TOUCHES IS TOTAL.** Not one `ck` row in `verify_clone.sh`
mentions a wheel, hub, cap, rim or vent, and `verify.py` has none either. Rev 51 changed
`CAP_SEAT_DY` and left `CAP_EMBLEM_D` alone with **zero verifier coverage on either**, and rev 52's
top job changes them again. Add coverage in the same edit as the change (rule 12).

**A CHEAP, UNBLOCKED ITEM NOT ON THE OLD LIST:** `SPEC` §8's colour locks are all graded **M** =
*"Measured by me from `ref_source.jpeg`"* — a 246x197 thumbnail the record itself calls retired. They
can be re-derived on `ref_playa_34.png` at **4x the area, today, with no new photograph**
(`PHOTOS_WANTED_rev49.md` says so and nothing shows it was ever done).

**THE PROCESS ROWS, still open:** the open-findings register abandoned at rev 45 (21 rows); the
standing-instructions carrier deleted at rev 44, which took the **die-cut sticker** — the project's
*original deliverable* — with it; SPEC §0.2 publishing two rev-4 corrections later refuted; rev 48's
refuted *"B stays open"* still live in `build.py` (*"B (the engine lid, above) stays open"*) and
`t1_shell.py` (*"so B"* / *"stays open and A is added"* — **it is split across two lines, so a flat
grep for the phrase misses it**); and **the tail board still has zero rows in either verifier**.

---

## §6. THE ARTWORK STATES — IT IS **FOUR**, CONFIRMED BY LOOKING AT REV 51

| class | frames | what the artwork carries |
|---|---|---|
| **RED, CURRENT** | `ref_side.jpg`, `ref_rear34.jpg`, `ref_playa_34.png` | scrollwork, Senor Tacombi script, Calidad burst |
| **RED, EARLIER** | the four *nolita* frames | plain red flank, `TACOMBI.COM`, no scrollwork, no script, no burst |
| **GREEN, IN SERVICE** | `IMG_2073.jpeg` | script in **BLACK**, plus scrollwork with yellow daisies, a **100 % Calidad burst**, orange TACOS / BREAKFAST SPECIAL. Headlamps fitted. |
| **GREEN, CONVERSION** | `ref_workshop.jpg` | script **ONLY**, silver outline. No scrollwork, no burst. Headlamps **not fitted**, and **both road wheels are bare rims with NO HUBCAP**. |

**The two green frames corroborate each other on NOTHING.** `ref_workshop.jpg` is useless for any
wheel or lamp reading — it has neither fitted.
**AND A CORRECTION TO THE FRAME ARITHMETIC:** `ref_playa_34.png = IMG_3842.png = ref_source.jpeg` is
written as an identity chain but **only the first two are byte-identical**. `ref_source.jpeg` is the
same PHOTOGRAPH at 246x197 (correlation 0.9768), not the same file. *Ceiling, and it is the record's
own: a correlation on a 246x197 thumbnail **cannot distinguish "the same frame" from "two frames one
second apart on a tripod"**. And this correction is NOT new at rev 51 — `PHOTOS_WANTED_rev49.md`
already carried it.* So: **15 files, 5 byte-identical
pairs, 10 distinct FILES, 9 distinct FRAMES.**

---

## §7. WHAT ONLY HE CAN GIVE — HE HAS SAID THE FIRST FIVE ARE NOT POSSIBLE NOW

Full text in `PHOTOS_WANTED_rev49.md` **for items 1–5 only** — that file contains no items 6 or 7,
so **item 7 below has no carrier outside this brief. Put it in `PHOTOS_WANTED_rev52.md`.**
**Do not re-ask 1–5.**

1. **THE TAIL BOARD'S FOOTING** — stands on the parallax bound alone (33.5 px/m, identical at base
   and tip, so W <= 0.59 m with no lower bound). Closes **two** unknowns, not three.
2. **THE DECAL, DARKER.** Five items, one frame, 60.8 % of the white lettering clipped.
3. **THE NOSE, SQUARE ON.** W4, seven revisions.
4. **A RAKING-LIGHT FRAME OF THE LOUVRES — the pressing depth.** *That is what
   `PHOTOS_WANTED_rev49.md` and the rev-50 correction actually say: ONE item. The "block length,
   station and V swage" expansion first appears in the rev-51 brief with no cited derivation — treat
   it as a proposal, not as the record.*
5. **THE OFF SIDE — ANY FRAME AT ALL.**
6. **AN OBLIQUELY-SEEN WHEEL, CLOSE.** *Rev 51 DISSOLVED this one — the dome was recovered from
   frames we already hold. Struck.*
7. **NEW: ONE HUBCAP, SQUARE ON AND CLOSE.** This is what §5 item 1 is blocked on. Every frame we
   hold puts the badge at ~19 px on a red dome or on chrome that defeats segmentation. It settles
   the emblem DIAMETER and the STROKE WEIGHT on the part he has just reported, and the same frame
   would confirm the seated dome's proudness directly.

---

## §8. THE RULES — `CLAUDE.md` CARRIES THE METHOD; THE NUMBERED CANON DOES NOT LIVE THERE

Read it first. It is method only, carries **no measurements** (a `verify_clone` row enforces that,
watched failing both ways), and every rule in it traces to a recorded failure of this project.

**BUT `CLAUDE.md` HOLDS 17 METHOD RULES, NOT THE NUMBERED CANON, AND IT SAYS SO.** The canon (rules
1–33) is printed last in `NEXT_CONTEXT_PROMPT_rev50.md` §11. **Rules 34 and 35 exist ONLY in
`NEXT_CONTEXT_PROMPT_rev51.md` §8 and `LEDGER_rev50.md` §0**, and this brief would be the first to
carry neither — which is `CLAUDE.md`'s own rule 16 (*"YOU MUST NOT DELETE A CARRIER"*) firing on this
file. **Carried here so the chain does not break:**

> **34. A REQUIREMENT INHERITS ITS OBJECT EXACTLY AS A RETIREMENT DOES.** Before relying on any
> *"the record requires X"*, check which object the sentence is about — and check the cited line exists.

> **35. A GUARD WRITTEN AGAINST A POSE ENCODES THAT POSE.** Guards that identify a part's foot or free
> edge by `min(y)` are only right while the part leans one way. Ask the geometry — a foot is the
> lowest point — never the pose.

> **Rule 29.3, cited in §2b and in `LEDGER_rev51`:** no finding is attributed to a cause until a
> control separates it. **Rule 29:** a retirement inherits the object it was made about, not the
> station it was seen at. **Rule 15:** a retraction that lands in a ledger and not in the source is
> half a retraction.

**REV 51 CAUGHT NINE INSTRUMENTS OF ITS OWN, AND FIVE OF THE NINE WERE ONE DEFECT.** A mask or window that
selected the wrong pixels: a "cab roof" window that was on the mural lid and the background; a "flank
cream" window that included the bulb string; a "roundel" window on the V and W strokes; an "emblem"
window on the rim ring; a "cap" window on the painted rim. **Every one caught by PAINTING the
selection and looking; NONE by reasoning about it.** It is now a `YOU MUST` in `CLAUDE.md`.

Also caught: a clearance guard that **fired on a correctly seated cap** (the hubcap profile is not
monotonic in r — it runs to the lip and RETURNS along the back face, so sorting by radius reads the
return where the front belongs); a notch-band window that measured the wrong annulus; a guard row
whose shell was wrong (**`grep -c` EXITS 1 when the count is ZERO**, which is exactly the passing
case, so a `|| echo 99` fallback fires on success); and a free-running seat cross-check that **failed
its own control** — `roof_z` does not describe the surface inside the tail roll-down, and the
tolerance was NOT widened to make it pass; it was withdrawn and the finding recorded at the site.

---

## §9. THIS MACHINE

```
cores 4   RAM 15 GB   Blender 4.5.3 via pip install bpy   subagent concurrency 2
build  T1_SUB=1 ~20 s     render 1600x1100 96 spp ~6-15 min PER VIEW (slower with agents running)
```

```bash
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
T1_PREVIEW=side T1_PFX=r52 T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
  /tmp/blender/blender -b -P build.py
T1_SUB=2 /tmp/blender/blender -b -P audit.py                 # rewrites STATE.md -- COMMIT FIRST
python3 lid_gen.py                                           # regenerates tex/lidmural.png
python3 flank_compare.py out/r52_side.png /tmp/fc.png        # THE FIDELITY GATE.  Exits 1 today.
```

**ABLATIONS — every one exists to WATCH A GUARD FAIL. All re-watched firing at rev 51:**
`T1_CAPSINK=1` (**new** — restores the un-seated cap; fires at r = 0.11974, the analytic crossover to
0.01 mm), `T1_LIDDEG=104`, `T1_BAYSTALE=1`, `T1_LAMPSINK=1`, `T1_LIDASPECT=1.2`, `T1_HANDLEHI=1`,
`T1_BAREMAT=1`, `T1_TBFOOT=1`, `T1_BAYPROUD=1`.

---

## §10. NEW METHOD, GRADED — ADOPTED AND REJECTED, WITH REASONS

Twelve process proposals reached rev 51 from outside. **Recorded so they are not re-proposed.**

| proposal | verdict | why |
|---|---|---|
| Root `CLAUDE.md`, method only, no numbers | **ADOPTED** | There was none. Landed, 118 lines, guarded by two rows watched failing. |
| Split `verify_clone`'s score FIDELITY vs SELF-CONSISTENCY | **ADOPTED** | **0 of 127 rows name a frame and a pixel window.** `SURVEY_rev49` §4 prescribed this during rev 50 — two revisions — and it never reached the machine. |
| Revive the dormant render-vs-photograph gates | **ADOPTED — the one that matters** | `flank_compare.py` runs and is RED. §5 item 2. |
| Promote the rev-50 tail-lamp chroma reading into a runnable fidelity probe | **ADOPT NARROWED** | The instrument is already written in prose in `LEDGER_rev50` — a frame, a window, a target, a control — and left zero rows behind. |
| Add image/fidelity rows to `verify_clone.sh` | **REJECT** | Structurally impossible and the script now says so at the site: no build, no render, no image library, `out/` untracked. |
| **Record pruning / context decay / ledger compaction** | **REJECT WITH PREJUDICE** | This is the repo's worst recorded failure, twice: the standing-instructions carrier deleted at rev 44 took the **die-cut sticker, the original deliverable**, undetected for five revisions; the open-findings register went the same way at rev 45. **Here the audit trail IS the asset.** |
| Autonomy / auto-merge / unreviewed shipping | **REJECT** | Contradicts *"any single measurement off is unacceptable — per-measurement, not on average"* against a measured **four to nine wrong instruments per revision**. |
| More agents / parallel Blender fan-out | **REJECT** | 4 cores, Blender CPU-bound, concurrency 2. Negative value: it slows the live queue. |
| A sixth verification surface (CI, lint, coverage) | **REJECT** | Five exist — `bootstrap.sh`, `verify_clone.sh`, `verify.py`, `audit.py`/`STATE.md`, the ablations — **and all five miss the same thing: pixels.** A sixth that cannot read a pixel is motion, not progress. |
| A separate `RULES_CANON.md` | **REJECT** | A second source of truth for the same rules, free to diverge. `CLAUDE.md` plus a grep line closes it. |
| Hyperframes (HTML/GSAP video) | **REJECT for the modelling work** | It does not model, render or measure. The standard here is per-pixel against still photographs. |
| A published visual defect register (Artifact / design canvas) | **OPEN — worth one hour** | The survey is 464 KB with 78 findings and hundreds of crops in `probe_scratch/`, and he judges by LOOKING. Not started. |

**AND FIX THE INTAKE DOORS, cheaply, in the same commit as anything else:** `START_HERE.md` still
says *"rev 7"*, `cd /home/claude/tacombi`, *"2 CPU cores"* and proposes a `STATE.md` that has existed
for thirty revisions; it mentions `verify_clone`, `bootstrap.sh` and `lid_gen` **zero** times.
`README.md` still points at `NEXT_CONTEXT_PROMPT_rev43.md`. Two pointer lines each.

---

## §11. THE STANDARD, IN HIS WORDS

We are recreating a photorealistic version of **that exact bus**, and **any single measurement off is
unacceptable** — per-measurement, not on average. A model right in ninety places and wrong in one is
not 99 % done, because he will look straight at the one.

`bus_model_ref.JPG` is a **SCHOOL BUS** and is **NOT the vehicle**. It is a FIDELITY BAR only: crisp
edges, small features built as real geometry with depth rather than painted on. Use `ref_workshop.jpg`
the same way. Take nothing about shape, paint or proportion from either.

**Ground in the reference, build, adversarially audit, iterate.** Never build before grounding. Never
call it done off self-review. Report the measurement against the reference **with its ceiling**, never
a self-assigned score. Do not say anything is ready — say what is fixed, what is still wrong, and what
you measured. Keep visible cadence on long work.

**RENDER IT, CROP IT, AND LOOK AT IT, before and after every change.** Every defect this project has
shipped passed `VERIFY: 0 fail, 0 warn` and was found by looking at a crop.

**When you need something from him, ask as MULTIPLE CHOICE with the reference material attached — one
crop, one mark, one sentence — and ASK IT WITH THE QUESTION TOOL.** He has never stood in the bus: do
not ask what the real vehicle looks like, ask what a PHOTOGRAPH shows.

**`git rev-list --count origin/main..HEAD` before you start and again before you finish. And
`git diff --name-only HEAD...origin/main` — that is where his photographs arrive. EVERY session.**
