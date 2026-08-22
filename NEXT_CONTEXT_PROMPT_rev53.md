# NEXT CONTEXT PROMPT — rev 53

**Read this whole file before you touch anything.** Then `CLAUDE.md` (method only, loads every
session), then `LEDGER_rev52.md` — which is where every number below comes from — then
`SURVEY_rev49_photoreal.md` §6, still the work list.

---

## §1. START HERE — MEASURE THE BRANCH, DO NOT TRANSCRIBE IT

```bash
cd /home/user/combi_render
git fetch --unshallow 2>/dev/null || true
git fetch --all --prune
for b in $(git branch -r | grep -v HEAD); do
  printf "%-52s ahead %-3s behind %s\n" "$b" \
    "$(git rev-list --count origin/main..$b)" "$(git rev-list --count $b..origin/main)"
done
git diff --name-only HEAD...origin/main        # <- HIS PHOTOGRAPHS ARRIVE HERE
./bootstrap.sh          # ALL 10 PASS  -- THE BRANCH CHECK IS ROW 9
./verify_clone.sh       # ALL 151 PASS -- and read what its verdict block says
```

**THE DESIGNATED BRANCH'S REMOTE COPY WAS DELETED AGAIN AT REV 52** — `fetch --prune` printed
`- [deleted] (none) -> origin/claude/new-session-sdoxpg`, exactly as at rev 51. HEAD measured
**0 ahead / 0 behind** `origin/main` and **no branch carried work HEAD did not have**: rev 51's work
had landed in `main` through **PR #8, which carried 20 commits** (19 on the branch plus the merge —
MEASURED at the rev-52 audit. An earlier draft of this file said *39*, transcribed from the rev-52
brief's statement about a different measurement. That is exactly the mistake this section warns
against, and it was caught by re-measuring, not by re-reading). **Expect this shape again and
measure it; do not transcribe it.**

> **ROW 9, NOT ROW 10** — confirmed again at rev 52 by reading the machine's own output:
> row 8 clone depth, **row 9 "no branch carries work HEAD does not have"**, row 10 `verify_clone.sh`.

**Re-measure before you finish, too.** `origin/main` moved mid-revision at rev 51.

---

## §2. WHAT REV 52 DID — AND THE ONE THING IT IS PROUDEST OF IS A RETRACTION

**THE FIDELITY LANE IS RUNNING. `flank_compare.py` was RUN, not grepped, for the first time since
rev 40.** Everything else follows from that.

### §2.1 `Senor` 0.174 WAS THE INSTRUMENT, NOT THE MODEL — and the brief had it backwards

The rev-52 brief asked for 0.174 (rev 51) to be reconciled with 0.459 (`LEDGER_rev44`/`45`) and said
*"do not assume a typo"*. It is not a typo and it is not a regression. **Four candidates were raised
and each was killed by its own control** — units, the ceiling, `tex/senor.png`'s rev-46/47 rewrite,
and the panel `SCR`. The cause is **a mask selecting the wrong pixels**, found by PAINTING the four
tarnish zones on the render and LOOKING:

```
the "enor" zone lands 16.5 % on top of Tacombi's swash, so endmembers() split
SILVER from {tarnish + red} instead of tarnish from red:
   ink (165,158,160) NEUTRAL  vs the working S zone's (160,108,96)
   50 %-mix threshold  0.2192 -> 0.1086
   the zone rescued +0 px of the 81.7 % of itself that IS tarnish
```

Fitting each zone's endmembers on `zm & ~raw` — pixels the silver rule has **not** already claimed —
gives:

| | before | after | rev 40 |
|---|---|---|---|
| `Senor` of its own ceiling | **0.174** | **0.480** | **0.459** |
| ink area ratio | 0.8751 FAIL | **0.9446 PASS** | — |
| IoU vs ceiling | 0.7350 | 0.7623 | 0.7535 |
| aspect | 2.3689 FAIL | 2.3689 FAIL, unmoved | 2.3622 |

**REFUTED, and it is the brief's own headline: "ONLY THE WORST-REGION NUMBER IS ROBUST" is
backwards.** It was the *least* robust of the four — the one the broken window destroyed — and **two
of the three FAILs were one cause.**

**THE GATE STILL FAILS 2 OF 4.** Current, on `out/r52d_side.png`: `Senor` **0.479**, aspect **2.3689**.

### §2.2 What else landed, all measured, all with ablations watched failing

| item | result |
|---|---|
| **A6** chip gate | `T1_EDGEBEVEL=1` takes the counter fascia from **4.07 % → 0.10 %** dark against `ref_side.jpg`'s **0.00 %**, and a verified SHELL window holds 0.00 → 0.00. **NOT the default: its positive control FAILED** (§3). |
| **A9** `gal_rail` | DERIVED from `BAYS[2]` now: centre −0.3800 → **−0.5980**, length 0.6600 → **0.4949**. **Floating hooks 3 → 1.** |
| **A9** `gal_caddy_fill` | inset sign was inverted by authoring order: **+24.0 mm proud → −24.0 mm inset**. |
| **A7** `gal_end_a` | show-side sight line **120.0 mm → 0.0 mm**, off side 20.0 → 0.0, half-width DERIVED from `REAR_W/2`. |
| **A19** lamps | *"zero rotation"* is now a number: **9.6°** (indicators) and **4.6°** (headlamps) off the nose's own normal. Measured, not fixed. |
| **`lid_rail`** | **0.000000000 m², 18/18 faces degenerate**, both objects. Guarded, **not fixed** (§4.1). |
| carriers | `PHOTOS_WANTED_rev52.md` created for §7 item 7, which had none. `START_HERE.md` / `README.md` pointers fixed. |

**Ablations added, every one watched failing:** `T1_TARNCONTAM`, `T1_EDGEBEVEL`, `T1_RAILSTALE`,
`T1_ENDSHORT`. **`verify_clone.sh` 127 → 151 rows; `verify.py` gained a zero-area sweep.**

### §2.3 THIS FILE WAS AUDITED AGAINST THE MACHINE, AND THE AUDIT FOUND THREE THINGS IN IT

Rule 15 says put something on the incoming brief whose only job is to refute it. That was done to
**this** file before it shipped — every cited file opened, every cited string grepped, every figure
recomputed. It found:

| what the draft said | what the machine says | how it got in |
|---|---|---|
| PR #8 carried **39 commits** | **20** (19 + the merge) | transcribed from the rev-52 brief's statement about a *different* measurement |
| the sixth hook is **51.4 mm** beyond the bay edge | **51.25 mm** | arithmetic published without being re-checked |
| `CAP_EMBLEM_WFRAC` cited with no file | it is in **`t1_detail.py`** | rule 17 — cite a string someone can grep |

**All three are corrected above.** The 51.4 mm also reached `LEDGER_rev52.md` and a commit message;
the ledger is corrected in place and the commit message cannot be, so the correction is recorded
there instead. **Two of the three were transcription, not measurement** — in a file whose own §1
tells you not to transcribe.

**AND THE STEP IS NOW MACHINE-CHECKED, SO IT CANNOT BE FORGOTTEN AGAIN.** Prose did not hold it —
the standing-instructions carrier and the open-findings register were both prose and both were lost.
`CLAUDE.md` gains the method rule, and **two `verify_clone.sh` rows** hold that the rule survives and
that **the highest-numbered brief actually carries its audit result**. Both were watched failing,
including on a newly written brief with no audit section, which is the real failure mode. **If you
write a rev-54 brief without auditing it, `verify_clone.sh` fails and tells you so.**

Verified clean by the same audit: all 14 cited files exist; the rev-50 canon block, and rules 34 and
35 in `LEDGER_rev50.md`, are all still where this file says they are; **all 13 named ablation
switches exist in the source**; `LID_X1 = -1.0700`, `REAR_W = 1.0400`, `GAPW = 0.0055` and
`W_EDGE_90 = 0.29289` all check; the 803 mm reproduces exactly off a live `X_TAIL = -1.8730`; and
`verify_clone.sh` reports **ALL 151 PASS** with the branch check on **row 9** (138 at the audit; the audit and the carry-forward block added the rest).

### §2.4 THE CARRY-FORWARD BLOCK — ELEVEN ROWS THAT NOW GUARD THIS FILE ITSELF

**Read this before you rewrite anything.** `verify_clone.sh` now checks that **the highest-numbered
brief still carries each item this project has actually lost or let go stale.** They were added
after sweeping the whole record — 45 briefs, 39 handoffs, 10 ledgers, 7 photograph lists.

**Measured first, and it changed the design:** `git log --diff-filter=D` over the whole
`LEDGER_*` / `NEXT_CONTEXT_PROMPT_*` / `PHOTOS_WANTED_*` / `HANDOFF_*` series is **EMPTY — no carrier
file has ever been deleted.** Both recorded losses were **content dropped inside a rewritten file**,
so a file-existence guard would have guarded the wrong thing.

| the row | what it guards, and what happened |
|---|---|
| die-cut sticker | rev 44 deleted the standing-instructions carrier and took the **original deliverable** with it. Five revisions undetected. **Still open.** |
| open-findings register | rev 45, 21 rows, went the same way |
| `flank_compare` | unrun rev 40 → rev 52 while the acceptance surface **grepped it for a symbol count instead of running it** |
| `cream_rms` | a second render-vs-photograph gate, **still zero rows of its own, still never run** |
| `PHOTOS_WANTED` | item 7 had **no carrier outside one brief** until rev 52 wrote one |
| canon pointer | rules 1–33 live **only** in `NEXT_CONTEXT_PROMPT_rev50.md` §11 |
| rules 34 / 35 | have never lived anywhere but briefs and `LEDGER_rev50.md` §0 |
| `T1_` ablation sweep | every switch a brief names must exist in the source, so the list cannot go stale unrun |
| README / START_HERE | README pointed at rev 43 for **nine revisions**; START_HERE said *"rev 7"* thirty revisions on |

They test **present/absent, never an exact count**, so re-wording is free and only **dropping** an
item fails. **If you write a rev-54 brief that drops any of these, or that has no audit section,
`verify_clone.sh` fails and names the row.** All eleven were watched failing on the real failure
mode — a rewritten brief with a line removed — and passing when restored.

---

## §3. WHAT IS REFUTED OR DELIBERATELY NOT BUILT — DO NOT REDO THESE

* **"Only the worst-region number is robust."** Backwards. See §2.1.
* **The A6 Bevel gate as the default.** Its **positive control FAILED**: looked at at 8× on the
  counter lip, it does **not move the chips to the edges, it REMOVES them** — no chipping at the lip
  either. `GAPW/2 = 2.75 mm` is **0.75 px at 271.2 px/m**, so the edge band is sub-pixel at every
  scale this project renders, and SPEC §3 locks the finish WEATHERED. **The mechanism is right and
  the scale is not.** Do not simply switch the default on; ground the radius first (§4.2).
* **`gal_end_f` widened to `REAR_W/2`.** NOT done, deliberately: it is the **FORWARD** return and the
  rear window is not what looks at it. Applying that figure there is rule 34 exactly.
* **A7's aft wall extended to the tail station.** Still refuted, still not built. A7 is
  **ILLUMINATION, not dressing** — both rear-3/4 frames still show a dark cavity after the sight
  line was closed.
* **Everything rev 50 and rev 51 refuted still stands.** The cap's dome depth; the m5 "convention
  conflict"; the wear field does not clone; `LID_W ≤ 1.2797 m`.
* **§2b of the rev-52 brief — HIS SETTLED RULINGS — IS UNCHANGED AND STILL BINDING.** W6 (keep the
  studio rig; **a G/R shortfall on any surface is NOT a paint error**); the roof strips' 0.3 m
  retired; the wipers withdrawn entire, commented not deleted; the lower bay SHUT; the RED bus is
  the target and **paint and artwork do not transfer between vehicles**; the tail board IS on the
  vehicle; the marks above the burst are STARS. **Do not re-open or re-ask any of them.**
  `playa_env.py` is not on the table.

---

## §4. THE WORK LIST FOR REV 53

**Item 1 is blocked on a photograph. Items 2–4 are not. If you do one thing, do item 2.**

**1. THE TWO VW BADGES — HIS REPORT AT REV 51, STILL THE TOP JOB, STILL BLOCKED.**
Untouched at rev 52. **PROVENANCE, GRADED: every figure in this item is INHERITED from rev 51 / rev 15
and was NOT re-measured at rev 52.** Treat them as the record's, not as freshly verified. The DIAMETER route on `ref_side.jpg` is **EXHAUSTED** (rev 51 got 0.3474 vs the
built 0.3170 — 9.6 % small but only **1.8 sigma**; re-running gets the same). **The untouched
constant is the STROKE WEIGHT**, `CAP_EMBLEM_WFRAC = 0.2087` **in `t1_detail.py`**, whose own comment says it kept its w/R
from the rev-14 emblem that rev 15 found at 7.0 sigma and resized. **No frame has ever been compared
against it.** Full text, and the four closed routes, in **`PHOTOS_WANTED_rev52.md` item 7**.
**AND THE GUARD GAP ON THIS PART IS STILL TOTAL** — rev 52 added rows for the tarnish window, the
chip gate, the galley and the zero-area sweep, but **still not one row anywhere names a wheel, hub,
cap, rim or vent.** Verified at rev 52: the only apparent hit is "vent" inside "in**vent**ed".

**2. GROUND THE A6 EDGE RADIUS AND FINISH THE JOB. The lever exists; the scale does not.**
Everything is built and measured; what is missing is one number: **how big a chip is in a
photograph.** Measure it on `ref_side.jpg`'s counter fascia (dark coverage there is **0.00 %**, so
measure chips where the photograph HAS them), set the Bevel radius from that rather than from
`GAPW/2`, then re-run the exact comparison in `LEDGER_rev52` §6.3 — the estimator, its two controls
and the painted windows are all recorded there so the numbers are directly comparable.
**And re-watch the positive control:** the fix is only right when the chips **move to the edges**,
not when the statistic falls.

**3. FINISH A9. Two of its four parts are done; the galley is still ~103 mm too far aft.**
**PROVENANCE, GRADED: the per-feature deltas below are INHERITED from the rev-52 brief and were NOT
re-measured at rev 52** — rev 52 measured `gal_rail`, `gal_caddy_fill` and the hooks, nothing else in
A9. Re-measure before relying on them. The offset is **NOT rigid** (−0.09574 at hook u=0.13 to −0.11035 at `gal_appliance` u=0.80, so one
additive constant leaves ±7.3 mm). Re-derive each X from `BAYS`, the way `gal_rail` now is.
*(The brief's ~106 mm and its +0.096..+0.113 range are both wrong; the machine's twelve per-feature
deltas mean 103.0 mm and none reaches 0.113.)*

**4. THE THREE HOLES REV 52 LEFT OPEN, all measured and all cheap to reach:**
* `gal_end_f` sees past by **260.0 mm** on the show side and 20.0 mm on the off side. Needs its own
  sight line established first — do not inherit `REAR_W/2`.
* The **sixth hook at X −0.907 lies 51.25 mm beyond `BAYS[2]`'s own aft edge (−0.855750)**, so it is outside bay 3
  altogether. The six hook stations are typed literals with irregular spacing whose span centre is
  **−0.705** against the rail's measured **−0.598**. **The hook stations and the bay measurement
  disagree and one of them is wrong.**
* A7's real defect: `roof_cutters()`'s aft edge is `LID_X1 = -1.0700`, so **803 mm of roofed body**
  sits between the last light inlet and the tail skin. Unbuilt. *(This one WAS re-derived at rev 52's
  audit and reproduces exactly: `LID_X1 = -1.0700` against a live `X_TAIL = -1.8730` gives 803.0 mm.)*

**5. A13 / A16 / A12** — the isolated star built BELOW the burst where both red frames put it above;
every flank rosette drawn at the diameter of its **gold core**; *A12 is an OWNER RULING, not a
do-now* — `senor_trace.py` calls the remedy *"inventing ink the photograph does not show"*, and
rev 52's §2.1 now shows the residual `Senor` failure belongs to **the reconstruction, not the
render** (its texture-only control reads 0.505 against the render's 0.479).

**6. A11's SECTION, A14** — a chrome lever lying in a dish **pressed into** the skin against a 12 mm
**proud** prism; the `lid_rail` WIDTH (§4.1).

**A CHEAP UNBLOCKED ITEM, STILL NOT DONE:** `SPEC` §8's colour locks are all graded **M** =
*"measured by me from `ref_source.jpeg`"* — a 246×197 thumbnail the record itself calls retired.
They can be re-derived on `ref_playa_34.png` at **4× the area** with no new photograph. **Report the
re-derived values; do not change the constants without his ruling** — W6 makes colour his call.

**THE PROCESS ROWS, still open:** the open-findings register abandoned at rev 45 (21 rows); the
standing-instructions carrier deleted at rev 44, which took the **die-cut sticker — the project's
original deliverable** — with it, still open; SPEC §0.2's two rev-4 corrections later refuted;
rev 48's refuted *"B stays open"* still live in `build.py` and, **split across two lines so a flat
grep misses it**, in `t1_shell.py`; the tail board still has **zero rows in either verifier**.
**AND `cream_rms.py` IS A SECOND DORMANT RENDER-VS-PHOTOGRAPH GATE with zero rows in either
acceptance script. It was NOT run at rev 52.** (`mark_rev45_ba.py` is *not* the same shape — it is a
question-figure generator, not a gate.)

### §4.1 `lid_rail` — MEASURED AT ZERO AREA, GUARDED, AND THE STOP WAS DELIBERATE

Both objects are **0.000000000 m² with 18 of 18 faces degenerate and bbox dx exactly 0.000000** — a
sweep found exactly these two of 223 meshes. The "perimeter rail the skin sits on, standing proud of
the roof" **is in no render this project has ever made**, and nothing caught it because **nothing
ever asked a mesh for its area**.
**It is exempt in `verify.py`, not fixed, because the rail's WIDTH is measured NOWHERE.** `LID_T` is
*"skin + rail thickness"* — a combined THICKNESS, not the member's width in X. **The exemption is
two-sided and cannot outlive the defect**: give the rail a width and the stale arm FAILS until the
exemption is deleted. **This is an owner question.**

### §4.2 THE HABIT THAT PAID AT REV 52, TWICE

**PAINT THE WINDOW AND LOOK AT IT BEFORE IT PRODUCES A NUMBER.** Rev 52 caught **four of its own
windows** this way and all four read a plausible **0.00 %**: two on the **WHITE BACKGROUND**, one on
the **BULB STRING** (rev 51's identical defect), one on the **WINDOW GLASS**.
**NEW TO THE RECORD, and specific to this delivery genre: a white studio background PASSES a
"bright and neutral" cream test.** Exclude it explicitly.
Also caught at rev 52: a guard row asserting `want 1` for a symbol that occurs **3** times, and an
ablation that **did not fire** because `grep 'smp = zm & ~raw'` still matches `~raw_BROKEN` — a
substring guard a suffix defeats. **Anchor the pattern and watch it fail on an APPEND, not only on
a deletion.**

---

## §5. WHAT ONLY HE CAN GIVE

**`PHOTOS_WANTED_rev52.md` is now the carrier for item 7 (ONE HUBCAP, SQUARE ON AND CLOSE)** — it had
none before rev 52 and the rev-52 brief said so. Items **1–5** keep their full text in
`PHOTOS_WANTED_rev49.md`: the tail board's footing; the decal darker; the nose square on; a
raking-light frame of the louvres (**ONE item — the pressing depth**; the "block length, station and
V swage" expansion is a proposal, not the record); the off side, any frame. **He has said 1–5 are not
possible now. DO NOT RE-ASK THEM.** Item 6 (an obliquely-seen wheel) was **DISSOLVED at rev 51** —
struck, not outstanding.

---

## §6. THE RULES — `CLAUDE.md` CARRIES THE METHOD, NOT THE NUMBERED CANON

The canon (rules 1–33) is printed in `NEXT_CONTEXT_PROMPT_rev50.md` §11. **Rules 34 and 35 live only
in the rev-51 brief, `LEDGER_rev50.md` §0 and the rev-52 brief, so they are carried here too — that
is `CLAUDE.md`'s own rule 16 firing on this file:**

> **34. A REQUIREMENT INHERITS ITS OBJECT EXACTLY AS A RETIREMENT DOES.** Before relying on any
> *"the record requires X"*, check which object the sentence is about — and check the cited line
> exists. **Rev 52 applied this deliberately**: `gal_end_f` was left alone because `REAR_W/2` belongs
> to the rear window, which is not what looks at it.

> **35. A GUARD WRITTEN AGAINST A POSE ENCODES THAT POSE.** Guards that identify a part's foot or
> free edge by `min(y)` are only right while the part leans one way. Ask the geometry.

> **Rule 29.3:** no finding is attributed to a cause until a control separates it. **Rule 29:** a
> retirement inherits the object it was made about. **Rule 15:** a retraction that lands in a ledger
> and not in the source is half a retraction.

---

## §7. THIS MACHINE

```
cores 4   RAM 15 GB   Blender 4.5.3 via pip install bpy   subagent concurrency 2
build  T1_SUB=1 ~30 s     render 1600x1100 96 spp ~6-7 min PER VIEW
```

```bash
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
T1_PREVIEW=side T1_PFX=r53 T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
  /tmp/blender/blender -b -P build.py
T1_PREVIEW=hero34r ...                                       # the REAR 3/4 -- A7 lives here
T1_SUB=2 /tmp/blender/blender -b -P audit.py                 # rewrites STATE.md -- COMMIT FIRST
python3 lid_gen.py                                           # regenerates tex/lidmural.png
python3 flank_compare.py out/r53_side.png /tmp/fc.png        # THE FIDELITY GATE.  Exits 1 today.
```

**`out/` IS NOT TRACKED and starts empty. Render before quoting any probe that reads a frame.**
**A backgrounded runner's exit code is the WRAPPER'S, not Blender's — grep the log for `Saved:`.**
Bitten twice at rev 52.

**ABLATIONS — every one exists to WATCH A GUARD FAIL. The four new ones were watched at rev 52:**
`T1_TARNCONTAM=1` (restores the contaminated tarnish window, reproduces `Senor` 0.174 exactly),
`T1_EDGEBEVEL=1` (the ray-traced chip gate), `T1_RAILSTALE=1` (the typed `gal_rail`),
`T1_ENDSHORT=1` (the short `gal_end_a`). Carried from before: `T1_CAPSINK=1`, `T1_LIDDEG=104`,
`T1_BAYSTALE=1`, `T1_LAMPSINK=1`, `T1_LIDASPECT=1.2`, `T1_HANDLEHI=1`, `T1_BAREMAT=1`,
`T1_TBFOOT=1`, `T1_BAYPROUD=1`.

---

## §8. THE STANDARD, IN HIS WORDS

We are recreating a photorealistic version of **that exact bus**, and **any single measurement off is
unacceptable** — per-measurement, not on average. A model right in ninety places and wrong in one is
not 99 % done, because he will look straight at the one.

`bus_model_ref.JPG` is a **SCHOOL BUS** and is **NOT the vehicle** — a FIDELITY BAR only. Use
`ref_workshop.jpg` the same way, and remember it has **no headlamps and no hubcaps fitted**.

**Ground in the reference, build, adversarially audit, iterate.** Never build before grounding. Never
call it done off self-review. Report the measurement **with its ceiling**, never a self-assigned
score. Do not say anything is ready — say what is fixed, what is still wrong, and what you measured.

**RENDER IT, CROP IT, AND LOOK AT IT, before and after every change.** Every defect this project has
shipped passed `VERIFY: 0 fail, 0 warn` and was found by looking at a crop. **Rev 52's whole result
came from looking at one.**

**When you need something from him, ask as MULTIPLE CHOICE with the reference material attached — one
crop, one mark, one sentence — and ASK IT WITH THE QUESTION TOOL.** He has never stood in the bus: do
not ask what the real vehicle looks like, ask what a PHOTOGRAPH shows.

**`git rev-list --count origin/main..HEAD` before you start and again before you finish. And
`git diff --name-only HEAD...origin/main` — that is where his photographs arrive. EVERY session.**
