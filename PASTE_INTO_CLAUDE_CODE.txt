# NEXT CONTEXT PROMPT — rev 64

## §0.0 DO THIS FIRST — THE WHOLE DECISION, IN TWENTY LINES

**Before you read another word, put the machine to work. It is CPU-bound and idle right now.**

```bash
cd /home/user/combi_render
./bootstrap.sh                 # the toolchain is NOT on the clone -- this builds it
nohup setsid env T1_SUB=1 T1_PREVIEW=front,side,hero,hero34r T1_PFX=r64 T1_RX=1600 T1_RY=1100 \
  T1_SAMP=96 /tmp/blender/blender -b -P build.py > /tmp/r64.log 2>&1 < /dev/null &
```

`out/` is untracked and **starts EMPTY**. **`bootstrap.sh` first**: at rev 58–62
`/tmp/blender/blender` did not exist. Then start the render, then read.
**`grep -c Saved: /tmp/r64.log` must be 4** — a backgrounded runner's exit code is the
redirect's. **USE `setsid`, NOT A BARE `nohup &`**: at rev 63 a harness restart killed a
render queue mid-job after two views, and only that `grep` caught it (F173).

**AND CHECK YOUR CLONE IS THE TIP.** Rev 62's clone arrived **SHALLOW (depth 50) AND
EIGHTEEN REVISIONS STALE**; **rev 63's arrived SHALLOW TOO**. A content check cannot
detect that you are on an old commit of the same repository. **Only `git fetch
--unshallow` and the ahead/behind loop in §1 found it.** Run §1 before you trust anything.

**THEN RUN `./judge_set.sh r64`.** `post.py` implements bloom → CA → vignette → grain,
defaults every gain to **0.0**, and the preview path **never calls it** (F146). Judge
photorealism on the `_post` set, never on the raw one.

**READ `LEDGER_rev63.md` §7 BEFORE YOU PLAN** — it is the list of what rev 63 did NOT do,
said plainly, and it is shorter than what it did.

---
## §0.05 THIS BRIEF WAS AUDITED AGAINST THE MACHINE — AND, AGAIN, WITHOUT AN ADVERSARY

**SAY THIS FIRST: NO INDEPENDENT ADVERSARY AGENT WAS RUN ON THIS DOCUMENT.** Rev 63's
session, like rev 62's, was instructed not to spawn subagents. Rules 15 and 17 were
discharged by their **committed script halves** — `audit_brief.py` and
`audit_adversary.py` — plus the author's own pass. **That is the mechanical half only.**
Rev 61 ran a real adversary and it returned TWENTY findings the author had not seen.
**Assume this brief carries defects of that class and put an agent on it first.**

**WHAT THE AUTHOR CAUGHT IN HIS OWN WORK — FOUR INSTRUMENTS, every one of which printed a
plausible number before it was caught:**

* **A RASTERISER CONTROL THAT ASSERTED AN IMPOSSIBLE AREA.** `svgraster.py`'s first C/S
  test demanded a triangle of area 0.5 and read **0.5828** — and the **CONTROL** was the
  defect: an `S` reflects the previous control point, so at a corner its implied handle
  necessarily leaves the chord. Replaced by an equivalence test with its own kill.
* **A ROW WHOSE CLAIM AND RULER DISAGREED.** `probe_rev63_canon.py`'s C24 said *"AT AN
  IDENTICAL RASTER"* while printing a 276-row figure against the photograph's 41 × 69.
  Rule 38, caught by reading the row against its own sentence.
* **A MASK THAT SELECTED THE RING INSTEAD OF THE STROKES.** `probe_rev63_reach.py`'s first
  window counted **arcs of the ring band's own edge** between cream cells — **10 contacts
  where the mark has 6, and 41 at 552 rows**. Caught by its three-raster row, confirmed by
  painting it. **That is the SIXTH time this project has recorded this exact defect.**
* **A KILL THAT COULD NOT KILL.** The same probe's first kill demanded the contact count
  DROP when the W's arms collapse onto the axis; it went **4 → 5**. `_on_band` projects
  every terminal onto the band circle by construction, so an inboard spine point changes
  its ANGLE, not its reach. Replaced with a synthetic kill: bars that reach read 6,
  retracted to 0.72 they read 0.

**AND TWO OF THE AUTHOR'S OWN PROPOSALS WERE REFUTED BY BUILDING THEM**, which is worth
more than the four above: the canonical vector as a target (F168) and the reach term as
the missing discriminator (F179).

**`verify_clone.sh` WAS RUN ON THE ACTUAL HANDOFF COMMIT, not on the tree later.**

---
## §0.06 THE BIG ONE: A GATE PASSING IS NOT EVIDENCE, AND REV 63 BUILT THE PROOF

**`probe_rev63_shapefit.py` FINDS CONSTANTS THAT SATISFY EVERY GATE THIS PROJECT HAS
STEERED THE OWNER'S TOP ITEM BY, AND RENDER AS A Y-SHAPED TRIDENT WORSE THAN THE X.**

```
                        IoU      cells   elongation   verdict
    shipped (rev 46)   0.4172      6        1.485     reads as an X
    the TRIDENT        0.5363      7        3.322     C6 PASS, C8 PASS, IoU up
    THE PHOTOGRAPH        --       7        3.390
```

**Look at `probe_scratch/rev63_emblem_ba.png` before you believe any number in this
file.** The constants were reverted; nothing of it shipped. **F175.**

**AND THE GATE CONTAINS THE ALARM FOR ITS OWN FAILURE.** At those constants
`probe_rev46_vw.py` prints **`[FAIL] C7 KILL: collapsing the W's arms and troughs onto the
axis moves the cell count 7 -> 7`**. A kill that cannot fail is not a control (rule 3), so
**C6's simultaneous PASS is worthless there**. Nobody had ever driven the gate into the
region where its own kill dies. **READ C7 AS A PRECONDITION ON C6. F176.**

**AND THE LANDMARK RESIDUAL WAS THE ONLY STATISTIC THAT STAYED RED ON THE TRIDENT, AND IT
WAS RIGHT (F177).** One counterexample, so **not** a rehabilitation of L1–L6 — F137 and
F139 stand — but it **inverts the presumption**, and `EMBLEM_HANDOFF.md` §5 item 5's
*"retire them"* should not be taken on the current evidence.

---
## §0.07 THE MACHINE'S VERDICT AT CLOSE OF REV 63 — every one watched print

```
bootstrap.sh            ALL 10 PASS
verify_clone.sh         ALL 298 PASS on a clean tree, AT THE HANDOFF COMMIT
                        <- 0 FIDELITY, 298 SELF-CONSISTENCY.  THIRTEEN rows moved this
                           revision: SIX emblem constants RE-BASED TOGETHER with the
                           cause named, plus SEVEN companion rows
audit.py                VERIFY: 0 fail, 0 warn at T1_SUB=2.  STATE.md REGENERATED --
                        the emblem spine is geometry and 19 verify rows read that file
probe_rev46_vw.py       9 checked, 3 FAILED -- C4, C5, C6.  C7 and C8 now PASS,
                        and C7 passing is what makes C6's reading meaningful (F176)
probe_rev63_canon.py    5 checked 0 FAILED;  --fit  11 checked 0 FAILED
probe_rev63_ablate.py   the construction's CEILING: elongation 6.877 AT 7 CELLS
probe_rev63_reach.py    6 checked, 0 FAILED
probe_rev63_trace.py    T3 FAILS at IoU 0.6504 -- HALF BUILT, and it is item 1 below
audit_brief.py          10 checked, 0 FAILED
audit_adversary.py      36 asked, 0 BROKE
```

**AND THE STANDING WARNING, WHICH `verify_clone.sh` PRINTS ITSELF.** A green check is not
evidence about the vehicle. **Not one of those 285 rows compares the model to a photograph.**

---
## §0. THE GOAL, AND HOW FAR OFF IT WE ACTUALLY ARE

**CARRIED FORWARD FROM THE REV-55…63 BRIEFS. It is not mine and it is not to be dropped —
rule 16.**

**PHOTO-REALISTIC PARITY WITH THAT EXACT BUS.** Not "a convincing VW bus" — *that one*,
the red Señor Tacombi combi in the frames on this repo. **Any single measurement off is
unacceptable, per-measurement and not on average.** A model right in ninety places and
wrong in one is not 99 % done, because he will look straight at the one. **At rev 58 he
did exactly that, at the emblem, for the fifth time. At rev 61 he did it again. At rev 62
he said *"I am sick and tired of not being able to execute a publicly available emblem."***

**AT REV 63 THE EMBLEM WAS CHANGED AND IT NOW READS AS A V OVER A W ON THE NOSE** —
`probe_scratch/rev63_emblem_ba2.png`, BEFORE | AFTER. **THAT IS NOT THE SAME AS RIGHT.**
Held next to the two photographs in `probe_scratch/rev63_vs_real.png`, four things are
still visibly wrong and **none of them is measured against a target**: the glyph does not
fill its ring the way both photographs do, the V is too narrow, the W's outer arms are too
short, and the strokes are thinner than the pressing's.

**AND HERE IS THE HONEST DISTANCE — THE GATE TABLE, WHICH AN ADVERSARY ONCE CAUGHT A BRIEF
DROPPING.** `verify_clone.sh` ends **ALL 298 PASS** and its own verdict block says what
that is worth: **0 FIDELITY, 298 SELF-CONSISTENCY.**

| gate | state MEASURED at close of rev 63 |
|---|---|
| `flank_compare.py` | **runs, FAILS.** Worst region **`i` at 0.686 of its own ceiling**; the `Senor` row now scores a **DELIBERATE DEPARTURE** — see F156, still not re-based |
| `gloss_compare.py` | **runs, FAILS at 0.426** (bar 0.60). The model-side lever is EXHAUSTED (F60/F62) — **but F62's ceiling is DISPUTED on measurements** |
| `probe_rev46_vw.py` | **C4, C5 and C6 FAIL; C7 and C8 PASS.** C8 at elongation 2.39 against 3.39 — *"1.42× too round"*, a pass against a 0.70 bar and NOT a claim of parity |
| `probe_rev59_nose.py` | **M1 PASSES lens-ruled — AND THAT IS NOT CLOSURE (F136).** Bezel-ruled 1.549 / 1.585 against a rim-ruled 1.951–2.121 |
| `mottle_measure.py` | **runs, and it is NOT measuring the mottle** — 1.1–2.0 % of it |
| `probe_rev45_ground.py` | item D's gate, and `T1_NOUNDER`'s only consumer. **G4 0.3602 built / 0.5475 ablated / 0.057 photographed** |
| `probe_rev59_door.py` | `T1_DOOR_STALE`'s gate. **8 checked, 1 FAILED (M3, BY DESIGN)** |
| `cream_rms.py` | `run()` is the LIVE photograph-side cream path |
| `visibility_budget.py` | the RANKING, not a gate — and **pass it the frame** (F132) |
| everything else | self-consistency |

**AND AT REV 61 HE ADDED A STANDARD.** *"I want this 3d model to look like new. Enhanced
from the photo."* That is not the same as WEATHERED, which SPEC §3 locks. **Where the two
collide, say so and put it to him** — do not silently pick one.

### §0.1 THE REFERENCE SET IS COMPLETE, AND IT IS GUARDED FRAME BY FRAME

> *[owner, rev 54]* **"we have all references that we need on repo and I want to make sure
> that is never forgotten."**

**ONE: WHAT WE HOLD IS WHAT WE GET. STOP PARKING WORK BEHIND A PHOTOGRAPH.** Where a frame
genuinely cannot answer, the result is *"it cannot be recovered from what we hold"* — a
real result, stated with its ceiling. **Rev 61 produced four; rev 63 produced one more**:
the six contact angles have no photographed target until the badge's ring is fitted on the
frame (F181).

**TWO: THEY CANNOT BE RE-SHOT, SO THEY ARE CHECKSUMMED INDIVIDUALLY.** 18 rows name them
one at a time:

* **the RED target bus** — `ref_side.jpg`, `ref_rear34.jpg`, `ref_playa_34.png`,
  `ref_nolita_front34.jpg`, `ref_nolita_front34b.jpg`, `ref_nolita_flank.jpg`,
  `ref_nolita_doorshut.jpg`
* **NOT the target, geometry only** — `ref_workshop.jpg` is the **GREEN** vehicle;
  **`IMG_2073.jpeg` is ALSO the GREEN vehicle**; `bus_model_ref.JPG` is a **SCHOOL BUS**,
  a fidelity bar only. **Paint and artwork do not transfer between vehicles; geometry does
  (rule 11)** — *and the useful corollary: the nose roundel's SHAPE is the factory chrome
  PRESSING, which is geometry and DOES transfer; only its colour is artwork (F141). Rev 63
  leaned on exactly this to trace the pressing.*
* **AND RULE 11 APPLIES BETWEEN LIVERY STATES OF THE SAME VEHICLE**, which killed F99, F100
  and F140: `ref_nolita_front34b.jpg` has a chalkboard lid and no folk art.
* **AND IT APPLIES BETWEEN ERAS OF A TRADEMARK** — new at rev 63, F168.
  `vw_canonical_2019.svg` is the mark as REDRAWN IN 2019, and it is **a different object**
  from the 1955–67 pressing: 3 cells / elongation 1.597 against the photographed badge's
  7 / 3.390 at an identical raster. **It is deliberately NOT named `ref_*`.**
* **derived/annotated** — `ref_grid.png`, `ref_side_grid.png`, `ref_nose_grid.png`,
  `ref_band_grid.png`, `ref_x6_lanczos.png` *(the last is a 6× upsample of the RETIRED
  thumbnail — "interpolation, no new information", so it adds nothing)*
* **retired** — `ref_source.jpeg`, a 246×197 thumbnail the record itself retired
* a **floor of 54** reference-class tracked images, and **the five byte-identical pairs are
  asserted to stay five** — a sixth group means a frame arrived that duplicates one we
  hold, which is **not corroboration** and has fooled this project before.

**AND `ref_playa_34.png` IS UNDER-USED.** Rev 61 verified its white balance **neutral** on
the paving (116,119,120) and used it, not `ref_side.jpg`, as the frame to judge paint
against. `ref_side.jpg` and `ref_rear34.jpg` are both globally WARM.

---

## §1 START HERE — MEASURE THE BRANCH, DO NOT TRANSCRIBE IT

```bash
git fetch --all --prune
git rev-parse --is-shallow-repository        # <- rev 62 AND rev 63 both arrived TRUE
for b in $(git branch -r | grep -v HEAD); do
  printf "%-52s ahead %-3s behind %s\n" "$b" \
    "$(git rev-list --count origin/main..$b)" "$(git rev-list --count $b..origin/main)"
done
git diff --name-only HEAD...origin/main        # <- HIS PHOTOGRAPHS ARRIVE HERE
./bootstrap.sh          # read ROW 9, and read the "N ahead / M behind" NOTE line
./verify_clone.sh       # ALL 298 PASS -- and read its verdict block
```

**MEASURED AT REV 63 PICKUP:** the clone was **SHALLOW**, and `fetch --prune` printed
`- [deleted] origin/claude/new-session-i94n44` — **the designated branch, before anything
had been pushed to it, the SEVENTH RUNNING.** It was recreated by the first push. After
`git fetch --unshallow`, HEAD was **0 ahead / 0 behind** `origin/main`, and no branch
carried work HEAD did not have. **EXPECT THE DELETION AT REV 64.**

**AND MEASURE IT AGAIN BEFORE YOU FINISH.** `origin/main` moved mid-revision at rev 51 and
rev 55. **At rev 63's CLOSE, HEAD was 5+ ahead / 0 behind `origin/main`** — the pickup
figure is NOT the close figure, and an adversary once caught a brief shipping only the
pickup one.

---
## §2 THE EMBLEM — **READ `EMBLEM_HANDOFF.md` FIRST. IT IS THE CARRIER FOR THIS ITEM.**

> *[owner, rev 62]* **"I am sick and tired of not being able to execute a publicly
> available emblem."**

**REV 63 CHANGED IT AND IT NOW READS AS A VW.** What shipped: the six spine constants
fitted to `vw_canonical_2019.svg` at IoU 0.7979 (converged, no parameter on a bound), and
the **NOSE's** stroke weight `vw_logo_fit()`'s default **0.1986 → 0.1800**, where the built
ink fraction matches the photograph's **0.606** exactly.

**IT IS NOT RIGHT YET, AND §5b/§5c OF `EMBLEM_HANDOFF.md` SAY EXACTLY WHY.** The four
visible errors are in §0 above. **The method most likely to close it is half built — see
§3 item 1.**

**DO NOT re-try any of these. Every one is measured, not argued:**

```
reach            T1_VW_CAPMIN            cells 6 -> 2                       (F101)
stroke weight    T1_VW_WFRAC alone       moves the WRONG way against C8     (F152)
six-constant cell-count solve            7 cells only at residual 0.2498    (F103)
separate strokes                         rev 8 did it and got an X          (F113)
the V/W kink                             the PHOTOGRAPHS have the same kink (F138)
terminal angles off the badges           residual 0.1800, WORSE than a bad
                                         control at 0.1167                  (F141)
the workshop badge's LANDMARKS           CEILED -- scale confound           (F153)
THE CANONICAL 2019 VECTOR as a TARGET    a DIFFERENT OBJECT, 3 cells /
  (new at rev 63)                        1.597 vs 7 / 3.390 at one ruler    (F168)
A REACH TERM as the discriminator        the trident touches in all SIX     (F179)
  (new at rev 63)
"no spine can satisfy the cell shape"    REFUTED: the construction reaches
  (F137, killed at rev 63)               6.877 at 7 cells                   (F174)
```

---
## §3 THE WORK LIST FOR REV 64

**RANK BY PIXELS OF THE DELIVERY FRAME** — `python3 visibility_budget.py 3840` — **and
PASS IT THE FRAME** (F132). Its ceiling: pixels are not visibility, so use it for ORDERS
OF MAGNITUDE, not to rank neighbours. **And the owner outranks it.**

**WHICH RANKING GOVERNS: THIS ONE.** `REMAINING_WORK_rev61.md` remains a CARRIER and its
§I still holds **27 untriaged rows** — **three revisions running**. `PANEL_rev61.md` is a
carrier too.

1. **PUT AN ADVERSARY ON THIS BRIEF FIRST (rule 15).** Rev 62 and rev 63 both could not.
2. **FINISH `probe_rev63_trace.py` AND PUT THE TRACED PRESSING IN THE MESH.** This is the
   emblem's most likely close and it is **half built**. It traces the real pressing's
   outline off `ref_workshop.jpg` instead of approximating it with seven constants.
   **Its own T3 FAILS at IoU 0.6504 and the diagnosis is already done and in the probe:
   the disagreement is the RING (IoU 0.508), not the glyph (interior IoU 0.78).** It needs
   hole-aware outlines fed to `t1_core`'s existing outline-to-mesh builder — the tracer
   (`trace_outline.py`) already carries `trace_with_holes()` and passes 10 selftest
   shapes. **The traced glyph already scores IoU 0.7129 against the TARGET BUS's own badge
   where the shipped one scores 0.5367.**
3. **LOOK AT THE HUBCAPS.** The spine is shared by five objects (F69) and rev 63 changed
   it. **No side or hero render was inspected after the change.** One render, one crop.
4. **GIVE F181's CONTACT ANGLES A TARGET.** `probe_rev63_angles.py` reads the six angles
   off both photographs but its stroke counts are **unstable across sampling radii
   (5, 5, 7, 9, 6)** — a windowing defect, stated. Fit the badge's ring on the frame and
   the target exists; then the search has a term that can reject a trident.
5. **ASK HIM THE TWO OPEN QUESTIONS** (§4): the print size, and whether the delivery
   render waits for the traced glyph.
6. **F156 — `flank_compare`'s `Senor` row scores a DELIBERATE DEPARTURE.** Re-base the
   reference or annotate the row. **Rev 62 and rev 63 both did neither.**
7. **TEST THE TWO DISPUTED CEILINGS** (specular-event census **0.024 % against 7.07 %**;
   the ground shadow). Recorded, NOT adopted.
8. **THE SURVIVING PANEL ITEMS**, none of which rev 61, 62 or 63 touched: the glass is a
   flat slab (0.5 % sd against the photograph's 12.8 %); the tyres have no tread, no
   sidewall lettering, and are 35 % too light; the tail is modelled as a box where the
   real one is a barrel; every shut line is a 1-px ink stroke with no leading-edge
   highlight; the galley is monochrome; the counter is a floating slab with no fascia.
9. **F143 — TWO LOUDSPEAKERS STAND ON THE ROOF AND ARE UNMODELLED.** Known since
   `AUDIT_rev12.md`, in no live carrier for 51 revisions now.
10. **THE INHERITED CLUSTER** — F14 (**eleven** revisions un-re-measured), F15, F10, F20.
11. **THE DELIVERY PACKAGE IS BUILT BUT NOT RE-RUN AT SIZE.** `deliver.py` shipped a set
    at 2400×1650. **`delivery/READ_ME_FIRST.txt` lists the model's known defects to him**;
    keep that list current or it becomes a lie — **it does not yet mention the rev-63
    emblem change.**

---
## §4 WHAT WAS ASKED OF HIM — A CARRIER, NOT A LIST OF BLOCKERS

> **READ §0.1 FIRST.** At rev 54 he ruled the reference set on the repo is complete. This
> section is kept in full because rule 16 forbids dropping a carrier.

**`PHOTOS_WANTED_rev52.md` is the carrier for item 7 (ONE HUBCAP, SQUARE ON AND CLOSE).**
Items **1–5** keep their full text in `PHOTOS_WANTED_rev49.md`. **He has said 1–5 are not
possible now. DO NOT RE-ASK THEM.** Item 6 was **DISSOLVED at rev 51**.

**HIS SETTLED RULINGS — DO NOT RE-OPEN OR RE-ASK ANY OF THESE.** W6 makes colour his call;
the roof strips' 0.3 m retired; the wipers withdrawn entire; the lower bay SHUT; the RED
bus is the target and paint/artwork do not transfer between vehicles; the tail board IS on
the vehicle; the marks above the burst are STARS; `lid_rail`'s width *"narrow lip, ~as wide
as it is tall"*; the roughness trade *"ship 0.250"*; the stranded rev-57b branch *"merge
it, renumber its IDs"*; the studio *"keep studio — ruling stands"* (twice); the front arch
*"leave it circular"*.

> **AND ONE LINE OF THAT LIST WAS NEVER HIS — CORRECTED BY ASKING HIM, AFTER REV 62.**
> It carried *"`playa_env.py` is not on the table — do not re-propose it"* from rev 52 to rev 63.
> **That entered as a brief's INFERENCE from W6, whose object is the studio RIG, and was applied
> to a SECOND DELIVERABLE — rule 34 exactly.** Put to him as multiple choice with both readings
> quoted, he ruled the Playa hero **"DEPRIORITISED, NOT CANCELLED"** — which is what his own
> rev-43 words said before that carrier was deleted at rev 44 (**F92**).
>
> **WHAT IT LICENSES: NOTHING TO DO NOW.** *"Focus on the 3d model"* stands, *"keep studio"*
> stands, **no revision works the Playa hero until he opens it**, and **nothing re-proposes
> `playa_env.py` as the delivery frame** — which is also why **F57** (that path renders no
> vehicle) stays recorded rather than fixed. What changes is that it is a LIVE agreed second
> deliverable carried in the register, not a closed one, and that *"the emotional bar that sits
> ABOVE clinical accuracy"* is back in the record. **Do not re-ask it; do not act on it either.**

**RULED AT REV 62, STILL BINDING:**

> ***"Bright silver, same as Tacombi."*** — the `Señor` word's finish. **This OVERRIDES
> SPEC §3's WEATHERED LOCK FOR THAT WORD ONLY.** SHIPPED as `script_gen.SENOR_TARNISH =
> 0.0`. `T1_SENOR_TARNISH=1` restores the pre-ruling texture byte for byte. **F157.**

> ***"It is going on different backgrounds for promotional material etc. give me
> everything I might need."*** **BUILT**: `T1_ALPHA=1` renders RGBA with the contact shadow
> in partial alpha (**F159**), and `deliver.py` packages full-frame, trimmed and SEPARATED
> vehicle/shadow layers with a plain-language `delivery/READ_ME_FIRST.txt` (**F160**).
> **It does NOT retire the rev-58 hold on the FULL delivery render.**

> ***"this is just the render to plug into company merch with different backgrounds once i
> determine the model is done"*** — **HE DID NOT AUTHORISE THE BOUNCE CARD; the "keep
> studio" ruling stands.** Consequences in **F155**: the white backdrop is **scaffolding**,
> a clean matte matters, and **the gate is HIM determining the model is done.**

**RULED AT REV 61:** ***"senor Tacombi should be clearer in the render than in that photo.
Well defined. I want this 3d model to look like new. Enhanced from the photo."*** **It
creates a live tension with SPEC §3's WEATHERED lock — surface it, do not silently pick a side.**

**ASKED AT REV 63 AND NOT YET ANSWERED — THESE ARE THE TWO LIVE QUESTIONS:**

1. **WHAT OUTPUT SIZE DOES HE NEED FOR PRINT?** `deliver.py` shipped at 2400×1650 and he
   has never stated a target. If he asks for large format it is one command and a longer
   wait — do not re-derive the pipeline.
2. **DOES THE DELIVERY RENDER WAIT FOR THE TRACED GLYPH (§3 item 2), OR GO NOW AT CURRENT
   FIDELITY?** His rev-58 gate says the full render waits until the model is right; the
   emblem is better than it was and is still not right. **This is his call, not the
   revision's.**

**CARRIED FROM REV 53, AND STILL IN NO OTHER DOCUMENT:** a frame showing the cream **where
it IS chipped**. Rev 54 and rev 55 both lowered its urgency — the band is 0.27 px at every
scale this project ships — but it is **not struck**, and F19 covers the MODELLING of
chipping, not the photograph request.

**AND HE VOLUNTEERED, STILL BINDING:** the emblem needs a fix, and **the full delivery
render waits until the model is right.**

**STILL WORTH HIS TIME AND NOT ASKED:** **F38** — the nose ring band at the top of its
adopted range, which interacts with the emblem; **F39/A3** — `Senor`'s ink deficit; and
**the local bounce card** both panels proposed independently, which is a studio change
under a ruling he has given twice.

---

## §5 THE RULES — `CLAUDE.md` CARRIES THE METHOD, NOT THE NUMBERED CANON

The canon (rules 1–33) is printed in `NEXT_CONTEXT_PROMPT_rev50.md` §11. Rules 34–42 live
only in the briefs and are carried here — that is rule 16 firing on this file:

> **34. A REQUIREMENT INHERITS ITS OBJECT EXACTLY AS A RETIREMENT DOES.** Check which
> object a *"the record requires X"* sentence is about, and check the cited line exists.
> **F26 is still open.**

> **35. A GUARD WRITTEN AGAINST A POSE ENCODES THAT POSE.** Ask the geometry, never the
> pose it happens to be in. **Rev 63 leaned on this deliberately: the contact-count
> statistic locates no terminal and names none, so it survives any spine.**

> **36. A GATE ONLY COUNTS FOR WHAT IT CAN SEE — ABLATE THE THING YOU ARE ABOUT TO TUNE,
> FIRST.** **Rev 63 finally ablated the emblem CONSTRUCTION rather than a constant inside
> it, and the answer overturned F137.**

> **37. AN ABSENT INPUT MUST NEVER READ AS A MEASUREMENT.** A probe that cannot run must
> say **"NO RENDER"** and exit non-zero. **Rev 63's sibling: `svgraster.py` RAISES on an
> unsupported path command rather than silently ignoring it.**

> **38. TWO SIDES OF A RATIO MUST SHARE A RULER, AND IF THEY CANNOT, SAY SO IN THE ROW'S
> OWN NAME.** **Rev 63 caught its own C24 breaking this.**

> **39. A GATE'S TARGET IS AN INSTRUMENT TOO, AND MUST BE SWEPT LIKE ONE.** Three targets
> in one instrument family have been found contaminated or mis-ruled — C6's 7 (F139),
> M1's ruler (F136), C8's window (F151).

> **40. WHEN AN OWNER RULING MAKES THE MODEL DEPART FROM THE REFERENCE, THE GATE THAT
> SCORES AGAINST THAT REFERENCE STOPS MEANING WHAT IT MEANT.** **F156, and rev 62 and rev
> 63 both failed to act on it.**

> **41. NEW AT REV 63 — A GATE PASSING IS NOT EVIDENCE THE THING IS RIGHT. BUILD THE
> COUNTEREXAMPLE.** C6, C8 and IoU all passed on a glyph that rendered as a Y (F175). A
> statistic is a projection; several projections can agree while the object is wrong.
> **The render is the arbiter. Any emblem search must be judged on a rendered crop.**

> **42. NEW AT REV 63 — A CONTROL'S KILL IS A PRECONDITION ON ITS PASS.** If the kill
> cannot go red at a point in parameter space, the control's PASS at that point means
> nothing. **C7 was dead exactly where C6 went green (F176). Read the kill first.**

---

## §6 THIS MACHINE

```
cores 4   RAM 15 GB   Blender 4.5.3 via pip install bpy   subagent concurrency 2
build  T1_SUB=1 ~20 s     render 1600x1100 96 spp ~4.5-5.5 min PER VIEW
```

**`bpy` IS A PIP MODULE HERE**, so `python3 probe_rev46_vw.py` runs in ~1.1 s without the
Blender CLI. That is what made rev 63's **24 000-point ablation** affordable — about
25 ms per glyph build. **Check whether a probe needs `blender -b -P` before you budget
minutes for it.**

```bash
./bootstrap.sh                                               # THE TOOLCHAIN IS NOT ON THE CLONE
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
./judge_set.sh r64                                           # the optics chain (F146)
python3 flank_compare.py out/r64_side.png /tmp/fc.png        # GATE 1
python3 gloss_compare.py out/r64_hero.png                    # GATE 3
python3 probe_rev59_nose.py out/r64_front.png                # READ BOTH RULERS
python3 probe_rev46_vw.py                                    # THE EMBLEM GATE -- read C7 FIRST
python3 probe_rev63_canon.py                                 # the canonical mark, measured
python3 probe_rev63_ablate.py                                # the construction's ceiling
python3 probe_rev63_shapefit.py                              # rebuilds F175's counterexample
python3 probe_rev63_reach.py                                 # contacts with the ring, and angles
python3 probe_rev63_trace.py                                 # HALF BUILT -- T3 fails, item 2
python3 trace_outline.py                                     # the tracer's own selftest
python3 svgraster.py                                         # the rasteriser's own selftest
python3 senor_trace.py                                       # the `S` connectivity guard
python3 cream_rms.py                                         # the LIVE photograph-side cream
python3 visibility_budget.py 3840                            # THE RANKING -- pass it the FRAME
T1_SUB=2 /tmp/blender/blender -b -P audit.py                 # rewrites STATE.md -- COMMIT FIRST
python3 audit_brief.py ; python3 audit_adversary.py          # rules 15 and 17, MECHANICAL half
```

**THE GATES THE ABLATIONS EXIST TO MAKE REFUSE:**

```bash
T1_SUB=1 T1_NOUNDER=1 /tmp/blender/blender -b -P probe_rev45_ground.py  # C5 must REFUSE
T1_SUB=1 T1_PG_PAINT=1 /tmp/blender/blender -b -P probe_rev45_ground.py # paints G4's window
python3 probe_rev59_door.py out/r64_side.png        # M3 fails BY DESIGN
python3 probe_rev61.py emblem --paint               # every mode paints its window
```

**ABLATION SWITCHES — all MEASUREMENT-ONLY:** `T1_VW_WFRAC` (**and note F178: it overrides
the NOSE's weight, `vw_logo_fit()`'s signature default — NOT `CAP_EMBLEM_WFRAC`, which is
the HUBCAP's**), `T1_VW_CAPMIN`, `T1_VW_PUREFIT`, `T1_VW_CELLSOLVE`, `T1_VW_DUMP`,
`T1_VW_RES`, `T1_VW_WSWEEP`, `T1_VNOSE_DIV`, `T1_BULB_STR`, `T1_BULB_BASEV`,
`T1_SENOR_BREAKS`, `T1_SENOR_TARNISH`, `T1_ALPHA`, `T1_NOUNDER`, `T1_UNDER_ZBUG`,
`T1_UNDER_PROUD`, `T1_UNDER_VIS`, `T1_UNDER_YBUG`, `T1_UNDERSEAL`, `T1_VPOW`/`T1_VPOWZ`
(**move them TOGETHER**), `T1_VRISE`, `T1_DOOR_STALE`, `T1_NORIG`, `T1_RIG`, `T1_WORLD`,
`T1_MOT_AMP`, `T1_GL_WRGH`, `T1_BODY_RGH`, `T1_GC_ABSSPREAD`, `T1_GC_LOOSEMASK`,
`T1_GL_TILES`, `T1_PG_PAINT`, `T1_BAREMAT`, `T1_CLAY`.

**FACTS ABOUT THIS MACHINE THAT BITE:**
* **EVERY MEASUREMENT THROUGH `shader_solve._render` IS 8-BIT (F42)**, whatever
  `color_depth` says.
* **`mottle_measure.py` names its output by `MOTTLE_AMP`**, so two runs differing only in
  `MOTTLE_M` **OVERWRITE EACH OTHER'S PNG**.
* **`probe_rev54_aov.py` and `probe_rev55_truenorm.py` write EXR into `probe_scratch/`** —
  delete them before committing and keep the PNGs.
* **`script_gen.py` IS NOT CALLED BY `build.py`.** Change it and regenerate `tex/senor.png`
  by hand, or the render silently uses the old texture.
* **`lid_gen.py` is NOT called by `build.py`** either.
* **`audit.py` rewrites `STATE.md`. COMMIT FIRST** — and regenerate it after ANY geometry
  change. **The emblem spine IS geometry; rev 63 regenerated it.**
* **LAUNCH LONG RENDER QUEUES WITH `setsid`, NOT A BARE `nohup &`** — F173.

**THE DELIVERY CHAIN, WHICH IS NOT THE PREVIEW CHAIN:**
```bash
T1_SUB=2 /tmp/blender/blender -b -P hq_render.py    # ONE build, 10 bands, WITH MARGIN
python3 stitch.py out/hq_hero_raw.png ...           # CHECK ITS EXIT CODE -- 2 on a seam (F49)
python3 post.py out/hq_hero_raw.png out/hq_hero.png # optics LAST, never per strip
```

**THE DELIVERY FRAME — DO NOT RUN IT UNTIL THE MODEL IS RIGHT (owner, rev 58, STILL
BINDING), and see §4's two open questions.**

---

## §7 THE STANDARD, IN HIS WORDS

We are recreating a photorealistic version of **that exact bus**, and **any single
measurement off is unacceptable** — per-measurement, not on average. **Ground in the
reference, build, adversarially audit, iterate.** Never build before grounding. Never call
it done off self-review. Report the measurement **with its ceiling**, never a self-assigned
score. Do not say anything is ready — say what is fixed, what is still wrong, and what you
measured.

**RENDER IT, CROP IT, AND LOOK AT IT, before and after every change.** Every defect this
project has shipped passed `VERIFY: 0 fail, 0 warn` and was found by looking at a crop.
**At rev 63 the single most important finding — that C6, C8 and IoU can all pass on a
glyph that reads as a Y — was found by rendering the winner and looking at it.**

**When you need something from him, ask as MULTIPLE CHOICE with the reference material
attached — one crop, one mark, one sentence — and ASK IT WITH THE QUESTION TOOL.**

---

## §8 THE OPEN-FINDINGS REGISTER — `OPEN_FINDINGS.md`

**IT IS A CARRIER (rule 16). Rows leave it only by being CLOSED with the measurement that
closed them, or RETIRED with the ruling that retired them. Never by being dropped.**

**Rev 63 added F167–F182**, of which **five are refutations** — two of rev 63's own
proposals (F170 amended, F179 refuted) — and one, **F175**, is the counterexample that
undercuts the emblem gate itself.

**THE POINT OF THE FILE IS THE PROVENANCE GRADE, NOT THE LIST.** An `INHERITED` row is a
claim. **GRADE DECAY IS ITSELF A FINDING.**

**STILL INHERITED AND OLDEST:** **F14** (`gal_end_f`'s sight lines, **rev 52 — ELEVEN
revisions un-re-measured**), F15, F20, F10, and **F18** (the die-cut sticker, rev 44 — the
oldest live row and the project's original deliverable).

**AND `REMAINING_WORK_rev61.md` §I IS STILL NOT TRIAGED** — 27 rows, **three revisions**.

---

## §9 THE HORIZON BEYOND REV 64

**CARRIER: re-rank it, do not rewrite it, and say what moved.**

**WHAT MOVED AT REV 63.** The emblem **changed on the nose** for the first time in
eighteen revisions and now reads as a V over a W; the **construction was ablated** and
F137 overturned; a **canonical vector** was obtained and disqualified by rule 11; and the
**gate itself was refuted as sufficient** by a built, rendered counterexample. **What did
NOT move: anything outside the emblem.**

**WHAT MOVED AT REV 62.** The emblem's leading suspect (L6) was killed by ablation; C8's
target was found to have a silent failure mode; `Señor` got an owner ruling, shipped.

| horizon | the work | why |
|---|---|---|
| **next** | **AN ADVERSARY ON THIS BRIEF** | Rev 62 and rev 63 both shipped without one |
| **next** | **FINISH THE TRACED PRESSING (§3 item 2)** | Half built, diagnosis done, and it is the emblem's most likely close |
| **next** | **LOOK AT THE HUBCAPS** | The spine changed under five objects and nobody looked |
| **next** | **THE TWO OPEN OWNER QUESTIONS (§4)** | Print size, and whether delivery waits |
| **near** | **F156 — the `Senor` gate row scores a DEPARTURE** | Three revisions unacted |
| **near** | **Test the two disputed ceilings** | A ceiling attributed to a studio that F155 says gets thrown away |
| **near** | **Glass, tyres, the tail's barrel, the shut lines** | The surviving panel items, none touched |
| **near** | **F143 — the roof loudspeakers** | Unmodelled since rev 12, in no carrier for 51 revisions |
| **then** | **F10–F14 — the galley cluster** | F14 is ELEVEN revisions inherited |
| **CEILED** | **F153 the workshop landmarks; F168 the 2019 vector; F44/F60/F62 gloss; F83 the front arch; F67's residue; F142's roof colour; F148's dark chrome** | **But F62 is DISPUTED — do not quote it without testing it** |
| **standing** | **F18 — the die-cut sticker** | The original deliverable. Open since rev 44 |

---

## §10 HOW TO GROW THIS HANDOFF WITHOUT BREAKING IT

1. **The set is three files.** `LEDGER_rev<N>.md`, `NEXT_CONTEXT_PROMPT_rev<N+1>.md`, and
   **`cp` of that file over `PASTE_INTO_CLAUDE_CODE.txt` IN THE SAME COMMIT.**
2. **`README.md` and `START_HERE.md` name the newest brief BY NUMBER.** Two rows check it.
3. **THE ROW COUNT IS SELF-REFERENTIAL AND AUTOMATED.** `python3 audit_brief.py
   --fix-count`. Write it LAST.
4. **ADD ROWS ANCHORED ON ARITHMETIC OR BEHAVIOUR, NOT ON A GREP.**
5. **RUN BOTH AUDITS AS SCRIPTS AND RECORD WHAT THEY FOUND *IN* THE BRIEF.** **REPLACE the
   adversary's questions each revision** — a question that can no longer fail is not a
   control.
6. **NEVER DELETE A CARRIER.** §0, §0.1, §4, §5, §8 and §9 are carriers.
   **`EMBLEM_HANDOFF.md`, `PANEL_rev61.md` and `REMAINING_WORK_rev61.md` are carriers too.**
7. **RANK BEFORE YOU CHOOSE** — but **the owner outranks the ranking**.
8. **NEVER RELAX ONE COPY OF A CHECK.** Rev 63 moved six emblem rows together and added
   seven companions.
9. **DO NOT LET THE MACHINE IDLE.** Run `bootstrap.sh`, launch the render, then read.
10. **ROOM TO GROW:** new findings go in `OPEN_FINDINGS.md` with an ID and a grade.
