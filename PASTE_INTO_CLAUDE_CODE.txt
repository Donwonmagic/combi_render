# NEXT CONTEXT PROMPT — rev 67

## §0.0 DO THIS FIRST — THE WHOLE DECISION, IN TWENTY LINES

**Before you read another word, put the machine to work. It is CPU-bound and idle right now.**

```bash
cd /home/user/combi_render
./bootstrap.sh                 # the toolchain is NOT on the clone -- this builds it
nohup setsid env T1_SUB=1 T1_PREVIEW=front,side,hero,hero34r T1_PFX=r67 T1_RX=1600 T1_RY=1100 \
  T1_SAMP=96 /tmp/blender/blender -b -P build.py > /tmp/r67.log 2>&1 < /dev/null &
```

`out/` is untracked and **starts EMPTY**. **`bootstrap.sh` first**: at rev 58–62
`/tmp/blender/blender` did not exist. Then start the render, then read.
**`grep -c Saved: /tmp/r67.log` must be 4** — a backgrounded runner's exit code is the
redirect's. **USE `setsid`, NOT A BARE `nohup &`** (F173).

**AND CHECK YOUR CLONE IS THE TIP.** Rev 62 through **rev 66** all arrived **SHALLOW** —
**nine running**. A content check cannot detect that you are on an old commit of the same
repository. **Only `git fetch --unshallow` and the ahead/behind loop in §1 find it.**

**THEN RUN `./judge_set.sh r67`.** `post.py` implements bloom → CA → vignette → grain and the
preview path **never calls it** (F146). Judge photorealism on the `_post` set, never the raw
one. *(**ONLY `bloom` defaults to 0.0** — `ca`, `vig` and `grain` default to **1.0**; F189a.)*

**READ `LEDGER_rev66.md` §7 AND §4 BEFORE YOU PLAN** — what rev 66 did NOT do, and the three
things it got wrong in its own work.

---
## §0.05 THIS BRIEF WAS AUDITED AGAINST THE MACHINE — AND WHERE IT IS WEAKEST

**HOW IT WAS AUDITED (rule 17).** Every figure in §0.06, §0.07 and §3 was RE-RUN at the
handoff commit, not transcribed. `audit_brief.py` and `audit_adversary.py` were both run and
their results are printed in §0.07.

**AND HERE IS THE LESSON REV 66 ADDS TO REV 65's.** Rev 65 found that the *sentence* naming
the emblem's defect was a string literal — a number that printed without being measured.
**Rev 66 found that two of the three NUMBERS it was being measured AGAINST could not be
reached by any glyph at all.** A literal at least changes when someone edits it. **A wrong
TARGET is invisible: every instrument agrees, every audit passes, and the work goes on for six
revisions.** **Assume this document contains another one.**

**WHERE THIS BRIEF IS WEAKEST:** **§0's inherited gate table** and **§4**, which are the two
longest carriers and are almost entirely inherited text — rev 64 found a seven-revision
misattribution in §4 and rev 65 found the literal. **AND NOW ALSO §2's REFUTED LIST**, which
is 14 rows of inherited "do not re-try this": **rev 66 showed that at least three of those
refutations were scored on gates now known to be mis-targeted.** Start an adversary there.

---
## §0.06 THE BIG ONE: TWO OF THE EMBLEM'S THREE TARGETS WERE UNREACHABLE, AND
## THE REAL DEFECT WAS SITTING IN THE PROBE SINCE REV 46

> *[owner, rev 65]* **"I can't believe that we can't even accomplish a publicly available
> emblem, and we still have work to do on the shape of the nose."**

**C6's TARGET OF 7 CELLS IS THE PHOTOGRAPH'S RIM (F200).** `photo_cells()` labels background
inside a `frac=0.97` disc concentric with the **41×69 CROP BOX**; the photographed ring is not
concentric with that box, so its outer edge falls inside the disc at one point and a crescent
of background was counted as a cream cell.

```
    the photograph's 7 cells, each against the RING'S OWN FILLED OUTLINE
      six at 100.0 % INSIDE          one at 0.0 %, mean r 0.932   <- THE SEVENTH
    disc sweep, photographed RAW count, frac 0.99 -> 0.84
      8, 7, 7, 8, 6, 6, 6            the BUILT count is 6 at EVERY one
    topology: a V fused to a W meets the band at SIX points, and a connected figure
      attached to a disc's boundary at k points cuts it into exactly k regions
    144 builds, all six constants +-50 %, weight 0.12..0.30:  6 in 143, 5 in one.
      NEVER 7.
```

**C4/C5's RESIDUAL WAS 96.4 % ONE BROKEN LANDMARK (F203).** L4 is *"the last 3-run row"*;
when the raster shows only one, that is **L2's row**, so L4 compared the built V's **APEX**
against the photograph's W **TROUGHS**. Built L4 flips between **0.366 and 0.866** with the
raster row count. **Converged, the residual is 0.1001, not 0.4455 — the constants AS THEY STOOD AT REV 65
were 2.8× BETTER than rev 45 (0.2814/0.1001) where C5 reported them 1.6× WORSE
(0.4469/0.2814).** *(Those four figures are all the PRE-rev-66 state, quoted together so
F203 can be checked in isolation. After F202 and F204 the probe prints residual 0.0755
against a rev-45 comparison of 0.2471, a factor of 3.3 — do not mix the two sets.)*

**AND WITH THE INSTRUMENTS CORRECTED THE REAL DEFECT WAS ALREADY IN THE PROBE.** `L6` —
stroke width over ring width **at the same row**, a horizontal over a horizontal so the
viewing angle's cosine cancels — had read **0.1178 against the photograph's 0.1528 since rev
46** and was never acted on, because it lived inside the residual that was 96 % one broken
landmark. **That is the owner's own sentence, *"the strokes are thinner than the pressing's"*,
as a number.** Two statistics sharing no ruler agree to 0.1 %:

```
    L6   crosses the photograph at wfrac 0.2283      <- no axis ratio, no registration
    INK  inboard of the band, crosses at    0.2280   <- built 0.432, photo 0.525 +- 0.055
    SHIPPED: vw_logo_fit's wfrac 0.1800 -> 0.2283.  HUBCAP's 0.2087 UNTOUCHED (F178).
```

**AND THE ARC-CUT TERMINAL IS BUILT AND SHIPPED (F202)** — the route the rev-66 brief called
*"the only one left standing"*. Both cap corners land on the band by construction and the
global extreme does not move (0.8140 → 0.8140). **It did NOT move the cell count, because
F200 shows the count was never the discriminator. The rev-66 brief's stated acceptance for
that item — *"C6 → 7 cells"* — was unreachable when it was written.**

**MEASURED ON THE RENDER, WHICH IS THE ARBITER:** ink inside the band
**0.418 → 0.502 against the photograph's 0.510**. The deficit closes from 18 % to 1.6 %.
**LOOK AT `probe_scratch/rev66_emblem_ba.png` AND `probe_scratch/rev66_photo_before_after.png`
BEFORE YOU PLAN ANYTHING.**

---
## §0.065 AND THEN THE OWNER LOOKED AT IT AND C6's PASS TURNED OUT TO BE A **RASTER** FACT

> *[owner, rev 66, shown the before/after crop]* **"The W's outer arms sit too low"** AND
> **"The strokes still don't reach the ring."**

**HE IS RIGHT, AND THE MEASUREMENT IS C6's OWN — JUST NOT ON C6's RASTER (F205).** Run
`cream_cells(..., interior=True)` on the RENDER instead of on `glyph_only_mask`:

```
    PHOTOGRAPH   6 interior cells        <- every stroke reaches
    RENDER before (rev-65 geometry)  4   <- the V's arms float; cells merge
    RENDER after  (as shipped)       3   <- and the arc cut + heavier stroke made it WORSE
    the FLAT RASTER reads 6 for BOTH, and cannot see any of this
    raw pixels outward along the V's left arm, 115 deg:
      red to r 0.63 | NEUTRAL CREAM (131,131,127) sat +4 from 0.66 to 0.78 | ring red from 0.81
```

**THE GAP IS NOSE CREAM, NOT SHADOW. AND THE MESH DISAGREES WITH THE RENDER:** it puts every
terminal at **0.8400 R** against a band inner edge of 0.8000, and `terminal_reach()` finds
**102 of 108** outline vertices inside the band. **REV 66 DID NOT FIND WHERE THEY DIVERGE.
That is the honest state — a measured contradiction, not a diagnosis, and it is §3 item 2.**

**ONE HYPOTHESIS WAS BUILT, GUARDED AND REFUTED — DO NOT RE-TRY IT (F206).** The roundel's
cream disc and the glyph are draped as separate plates and their front faces looked coincident
to 0.1 mm. A `GLYPH_STANDOFF` was added and a guard written in the same edit; **the guard
refuted the hypothesis — at the original standoff the clearance is already +2.04 mm.** The
apparent coincidence was two DIFFERENT radii inside one wide bin (rule 38, inside a
diagnostic). **The change is reverted; the guard stays, because the comparison was genuinely
missing.**

> **AND THE LESSON, WHICH IS RULE 41 AGAIN AND COST THIS REVISION ITS HEADLINE.** C6 was
> repaired, re-based and made to PASS — **on a raster that does not predict the render on the
> very axis C6 is named for.** A gate can be corrected, guarded, killed, swept, and still be
> measuring the wrong object. **The render is the arbiter. Run the emblem gates on the FRAME
> before you believe them.**

---
## §0.07 THE MACHINE'S VERDICT AT CLOSE OF REV 66 — every one watched print

```
bootstrap.sh              ALL 10 PASS
verify_clone.sh           ALL 329 PASS on a clean tree, AT THE HANDOFF COMMIT
                          <- 0 FIDELITY, 329 SELF-CONSISTENCY.  303 -> 322.
                          ONE row RE-BASED with its cause named (C7's kill, F201) and
                          17 companion rows added.  NO row relaxed.
probe_rev46_vw.py         12 checked, 1 FAILED -- C4 ONLY, at 0.0755 against a bar of
                          0.045.  WAS 9 checked, 3 FAILED (C4, C5, C6).
                          C6 PASSES 6 = 6 -- **ON THE RASTER.  ON THE RENDER THE SAME
                          FUNCTION READS 3 AGAINST THE PHOTOGRAPH'S 6 (F205).**
                          C10, C11, C12 are NEW
THE SAME FUNCTION ON      PHOTOGRAPH 6  |  out/r66_front.png 4  |  out/r66b_front.png 3
THE RENDER (F205)         <- the gate that matters, and it is RED
build.py T1_VERIFY=1      VERIFY: 0 fail, 0 warn at SUB=1
audit.py T1_SUB=2         VERIFY: 0 fail, 0 warn -- STATE.md regenerated at the commit
probe_rev65_unproject.py  10 checked, 0 FAILED
probe_rev64_shear.py      6 checked, 0 FAILED
probe_rev63_trace.py      ALL CONTROLS PASS
probe_rev63_reach.py      ALL CONTROLS PASS
vw_pressing.py            5 checked, 0 FAILED
trace_outline.py          SELFTEST PASS ;  svgraster.py  SELFTEST PASS
flank_compare.py          FAILS -- unchanged
gloss_compare.py          FAILS at 0.441 of the photograph's spread (bar 0.60) -- unchanged
probe_rev59_nose.py       5 checked, 0 FAILED -- AND IT STILL DOES NOT MEASURE THE NOSE'S
                          SECTION, which is what he asked about (F197)
probe_rev59_door.py       8 checked, 1 FAILED (M3, BY DESIGN).  PASS IT THE **side** FRAME --
                          handed a front frame it dies with UnboundLocalError, not a refusal
```

**AND THE STANDING WARNING, WHICH `verify_clone.sh` PRINTS ITSELF.** A green check is not
evidence about the vehicle. **Not one of those 322 rows compares the model to a photograph.**
The three that do are `flank_compare`, `gloss_compare` and `probe_rev46_vw` — **and two of the
three still fail.**

---
## §0. THE GOAL, AND HOW FAR OFF IT WE ACTUALLY ARE

**CARRIED FORWARD FROM THE REV-55…64 BRIEFS. It is not mine and it is not to be dropped —
rule 16.**

**PHOTO-REALISTIC PARITY WITH THAT EXACT BUS.** Not "a convincing VW bus" — *that one*, the
red Señor Tacombi combi in the frames on this repo. **Any single measurement off is
unacceptable, per-measurement and not on average.** A model right in ninety places and wrong
in one is not 99 % done, because he will look straight at the one. **At rev 58 he did exactly
that, at the emblem, for the fifth time. At rev 61 he did it again. At rev 62 he said *"I am
sick and tired of not being able to execute a publicly available emblem."***

**AT REV 63 THE EMBLEM CHANGED AND NOW READS AS A V OVER A W ON THE NOSE. IT IS NOT RIGHT,
AND AT REV 64 AND REV 65 IT DID NOT MOVE. AT REV 66 IT MOVED: the strokes were measured
24 % too thin and are fitted, and the terminal caps are cut on the band's arc. Ink inside
the band, ON THE RENDER, 0.418 → 0.502 against the photograph's 0.510.** Held next to the photographs, four things are still visibly
wrong: the glyph does not fill its ring the way both photographs do, the V is too narrow, the
W's outer arms are too short, and the strokes are thinner than the pressing's. **The W's two
outer arms visibly FLOAT short of the ring — C6 measures it at 18.9 mm and you can see it in
`probe_scratch/rev64_front_emblem.png`.** What is new is that **two of the three gates that
would score a fix are now known not to mean what they were taken to mean** (§0.06).

**AND HERE IS THE HONEST DISTANCE — THE GATE TABLE, WHICH AN ADVERSARY ONCE CAUGHT A BRIEF
DROPPING.** `verify_clone.sh` ends **ALL 329 PASS**: **0 FIDELITY, 329 SELF-CONSISTENCY.**

| gate | state MEASURED at close of rev 64 |
|---|---|
| `flank_compare.py` | **runs, FAILS.** Worst region **`i` at 0.687 of its own ceiling**; the `Senor` row scores a **DELIBERATE DEPARTURE** — F156, **FOUR revisions un-re-based** |
| `gloss_compare.py` | **runs, FAILS at 0.442** (bar 0.60). Model-side lever EXHAUSTED (F60/F62) — **but F62's ceiling is DISPUTED on measurements** |
| `probe_rev46_vw.py` | **RE-MEASURED AT REV 66: 12 checked, 1 FAILED — C4 ONLY, at 0.0755 (bar 0.045).** C5, C6, C7, C8 now PASS; C10/C11/C12 are new. **C6's target was RE-BASED 7 → 6 because SEVEN WAS THE PHOTOGRAPH'S RIM (F200)**, and C4/C5's residual was 96 % one broken landmark (F203). Read §0.06 before quoting any of it |
| `probe_rev64_shear.py` | **NEW. 6 checked, 0 FAILED.** The reason the two above cannot decide the emblem |
| `probe_rev63_trace.py` | **ALL CONTROLS PASS.** The trace is sound; what it traced is a sheared frame (F183) |
| `probe_rev59_nose.py` | **M1 PASSES lens-ruled — AND THAT IS NOT CLOSURE (F136).** Bezel-ruled 1.550 / 1.584 against rim-ruled 1.951–2.121 |
| `mottle_measure.py` | **runs, and it is NOT measuring the mottle** — 1.1–2.0 % of it |
| `probe_rev45_ground.py` | item D's gate, `T1_NOUNDER`'s only consumer. **G4 0.3602 built / 0.5475 ablated / 0.057 photographed** |
| `probe_rev59_door.py` | `T1_DOOR_STALE`'s gate. **8 checked, 1 FAILED (M3, BY DESIGN)** |
| `cream_rms.py` | `run()` is the LIVE photograph-side cream path |
| `visibility_budget.py` | the RANKING, not a gate. **PASS IT A `.png`** — `visibility_budget.py 3840` alone falls back to globbing `out/*hero*.png` by mtime, **which IS F132's defect**, so the command printed in every brief through rev 64 reproduces the bug the sentence beside it warns against (F189) |
| everything else | self-consistency |

**AND AT REV 61 HE ADDED A STANDARD.** *"I want this 3d model to look like new. Enhanced from
the photo."* That is not the same as WEATHERED, which SPEC §3 locks. **Where the two collide,
say so and put it to him** — do not silently pick one.

### §0.1 THE REFERENCE SET IS COMPLETE, AND IT IS GUARDED FRAME BY FRAME

> *[owner, rev 54]* **"we have all references that we need on repo and I want to make sure
> that is never forgotten."**

**ONE: WHAT WE HOLD IS WHAT WE GET. STOP PARKING WORK BEHIND A PHOTOGRAPH.** Where a frame
genuinely cannot answer, the result is *"it cannot be recovered from what we hold"* — a real
result, stated with its ceiling. **Rev 61 produced four; rev 63 one; rev 64 one more**: F185,
the amount of shear in the two badge frames, which cannot be separated from shape until the
ring is fitted as an ellipse.

**TWO: THEY CANNOT BE RE-SHOT, SO THEY ARE CHECKSUMMED INDIVIDUALLY.** **16 `ck "ref …"` rows
name them one at a time** *(the "18" in the rev-63 and rev-64 briefs counted two aggregate
rows that by their own words do not name a frame — F189)*:

* **the RED target bus** — `ref_side.jpg`, `ref_rear34.jpg`, `ref_playa_34.png`,
  `ref_nolita_front34.jpg`, `ref_nolita_front34b.jpg`, `ref_nolita_flank.jpg`,
  `ref_nolita_doorshut.jpg`
* **NOT the target, geometry only** — `ref_workshop.jpg` is the **GREEN** vehicle;
  **`IMG_2073.jpeg` is ALSO the GREEN vehicle**; `bus_model_ref.JPG` is a **SCHOOL BUS**, a
  fidelity bar only. **Paint and artwork do not transfer between vehicles; geometry does
  (rule 11)** — *and the corollary rev 63 leaned on: the nose roundel's SHAPE is the factory
  chrome PRESSING, which is geometry and DOES transfer; only its colour is artwork (F141).*
  **REV 64 ADDS THE LIMIT ON THAT COROLLARY: the shape transfers, but the PROJECTION does
  not. `ref_workshop.jpg` shows the pressing obliquely (mirror IoU 0.4111) and no de-squash
  removes it (F184).**
* **AND RULE 11 APPLIES BETWEEN LIVERY STATES OF THE SAME VEHICLE**, which killed F99, F100
  and F140: `ref_nolita_front34b.jpg` has a chalkboard lid and no folk art.
* **AND IT APPLIES BETWEEN ERAS OF A TRADEMARK** — F168. `vw_canonical_2019.svg` is the mark
  as REDRAWN IN 2019 and is **a different object** from the 1955–67 pressing: 3 cells /
  elongation 1.597 against the photographed badge's 7 / 3.390 at one raster. **It is
  deliberately NOT named `ref_*`.**
* **derived/annotated** — `ref_grid.png`, `ref_side_grid.png`, `ref_nose_grid.png`,
  `ref_band_grid.png`, `ref_x6_lanczos.png` *(a 6× upsample of the RETIRED thumbnail —
  "interpolation, no new information")*
* **retired** — `ref_source.jpeg`, a 246×197 thumbnail the record itself retired
* a **floor of 54** reference-class tracked images, and **the five byte-identical pairs are
  asserted to stay five** — a sixth group means a frame arrived that duplicates one we hold,
  which is **not corroboration** and has fooled this project before.

**AND `ref_playa_34.png` IS UNDER-USED.** Rev 61 verified its white balance **neutral** on the
paving (116,119,120) and used it, not `ref_side.jpg`, to judge paint. `ref_side.jpg` and
`ref_rear34.jpg` are both globally WARM.

---
---
## §1 START HERE — MEASURE THE BRANCH, DO NOT TRANSCRIBE IT

```bash
git fetch --all --prune
git rev-parse --is-shallow-repository        # <- rev 62..66 ALL arrived TRUE
for b in $(git branch -r | grep -v HEAD); do
  printf "%-52s ahead %-3s behind %s\n" "$b" \
    "$(git rev-list --count origin/main..$b)" "$(git rev-list --count $b..origin/main)"
done
git diff --name-only HEAD...origin/main        # <- HIS PHOTOGRAPHS ARRIVE HERE
./bootstrap.sh          # read ROW 9, and read the "N ahead / M behind" NOTE line
./verify_clone.sh       # ALL 329 PASS -- and read its verdict block
```

**MEASURED AT REV 66 PICKUP:** the clone was **SHALLOW** — the **NINTH running**;
`fetch --prune` printed `- [deleted] origin/claude/next-context-prompt-rev66-0rd3kg`, **the
designated branch, before anything had been pushed to it, THE NINTH RUNNING**; HEAD was
**0 ahead / 0 behind** `origin/main`; **row 9 PASSED**; and
`git diff --name-only HEAD...origin/main` was **EMPTY** — no new photographs.
**EXPECT THE BRANCH DELETION AGAIN AT REV 67.**

> **AND THE LESSON THAT COST SEVEN REVISIONS: no sentence about branch state survives the
> hour. `bootstrap.sh` row 9 outranks every sentence, INCLUDING THIS ONE.**

**AND MEASURE IT AGAIN BEFORE YOU FINISH.** `origin/main` moved mid-revision at rev 51 and
rev 55; the pickup figure is NOT the close figure. **AT REV 66's CLOSE, see §8 below.**

---
## §2 THE EMBLEM — **READ `EMBLEM_HANDOFF.md` FIRST, AND READ ITS §5b.2 RETRACTION.**

> *[owner, rev 62]* **"I am sick and tired of not being able to execute a publicly available
> emblem."**

**WHAT IS IN THE TREE AT REV 66's CLOSE:** rev 63's six spine constants (`VW_V_TIP_X 0.3287`,
`VW_APEX_Z 0.0538`, `VW_W_ARM_X 1.1002`, `VW_W_ARM_Z 0.4350`, `VW_W_TROUGH_X 0.3111`,
`VW_W_TROUGH_Z -0.6445`) — **UNCHANGED** — plus **rev 66's two changes: the ARC-CUT TERMINAL
(F202, ON by default, `T1_VW_NOARC=1` ablates it) and the NOSE's stroke weight `wfrac 0.2283`
(F204, was 0.1800).**

**DO NOT re-try any of these. Every one is measured, not argued:**

```
reach            T1_VW_CAPMIN            cells 6 -> 2                       (F101)
stroke weight    T1_VW_WFRAC alone       "moves the WRONG way against C8"   (F152)
                                         *** SUPERSEDED AT REV 66: measured
                                         now, raising it moves elongation
                                         TOWARD the target and L6 ONTO it.
                                         F152 was scored on C8's OLD target
                                         and against a residual that was
                                         96 % broken.  SHIPPED.       (F204) ***
six-constant cell-count solve            7 cells only at residual 0.2498    (F103)
                                         *** AND 7 IS UNREACHABLE (F200) ***
separate strokes                         rev 8 did it and got an X          (F113)
the V/W kink                             the PHOTOGRAPHS have the same kink (F138)
terminal angles off the badges           residual 0.1800, WORSE than a bad
                                         control at 0.1167                  (F141)
the workshop badge's LANDMARKS           CEILED -- scale confound           (F153)
THE CANONICAL 2019 VECTOR as a TARGET    a DIFFERENT OBJECT                 (F168)
A REACH TERM as the discriminator        the trident touches in all SIX     (F179)
"no spine can satisfy the cell shape"    REFUTED: 6.877 at 7 cells          (F174)
TRACING THE PRESSING AND MESHING IT      BUILT, RENDERED, WORSE.
                                         T1_VW_TRACED MUST STAY OFF        (F183)
TUNING AGAINST C6 OR C8 AS THEY STAND    their targets carry the viewing
                                         angle -- a pure shear spans both   (F184)
C8's 3.390 AS A TARGET AT ALL            un-squashed it is 2.63..2.96       (F194)
SEARCHING THE MARK'S VERTICAL BY         renders as horizontal bars         (F195)
  MIRROR IoU
T1_VW_CAPMIN + T1_VW_PUREFIT             6 cells / 2.24.  TRIED, REFUTED    (F199)
QUOTING C6's "0.6638 / 18.9 mm"          IT WAS A STRING LITERAL            (F198)
                                         *** FIXED AT REV 66: C6 now
                                         measures, and C12 is the kill ***
CHASING C6 TO SEVEN CELLS                SEVEN IS THE PHOTOGRAPH'S RIM.
  (new at rev 66)                        The mark makes SIX and the build
                                         ALREADY MAKES SIX                  (F200) ***
```

> **AND A WARNING ABOUT THIS LIST ITSELF, WHICH IS NEW AND IS THE POINT OF §0.05.**
> **Three of the rows above were scored on gates now known to be mis-targeted** — F152 against
> C8's old target and a 96 %-broken residual, F103 and F179 against C6's unreachable 7.
> **A refutation inherits its instrument. Before you accept any row here, check what it was
> measured with.** That is rule 39 applied to the refuted list rather than to a gate.

---
## §3 THE WORK LIST FOR REV 67

> **HIS TWO SENTENCES ARE STILL THE WORK.** *"I can't believe that we can't even accomplish a
> publicly available emblem, and we still have work to do on the shape of the nose."*
> **The emblem MOVED at rev 66 and is not finished. THE NOSE HAS NOT BEEN TOUCHED.**

1. **THE NOSE'S SHAPE — HE ASKED FOR IT BY NAME, TWO REVISIONS AGO, AND THERE IS STILL NO
   INSTRUMENT FOR IT (F197). THIS IS NOW THE TOP ITEM.** `probe_rev59_nose.py` measures the
   lamp break's ELEVATION, not the nose's SECTION. Rev 51 held the nose against the
   photographs and found **a FLAT NOSE** by eye, alongside the roundel's short V-arms; the
   V-arms became the emblem and swallowed fifteen revisions and **the flat nose was never
   worked.** Levers: `t1_shell`'s `V_POW` / `V_POWZ` / `V_RISE` — **move `V_POW` and `V_POWZ`
   TOGETHER** — never fitted to a photographed section. **BUILD THE INSTRUMENT FIRST:**
   extract the nose's silhouette from `ref_nolita_front34.jpg` and `ref_playa_34.png` and
   compare with the mesh's own section. **Then fit. Then render, crop, and LOOK.**
   *(And note the pattern rev 66 proved: build the instrument, and the defect may already be
   sitting in one you have. Check what `probe_rev59_nose.py` ALREADY measures before adding.)*
2. **F205 — THE RENDER CUTS THREE INTERIOR CELLS WHERE THE PHOTOGRAPH CUTS SIX, AND THE
   RASTER CANNOT SEE IT. THIS IS THE EMBLEM'S TOP ITEM AND IT IS ONE OF HIS TWO SENTENCES.**
   Run C6's own `cream_cells(..., interior=True)` on `out/r67_front.png` rather than on
   `glyph_only_mask`: photograph **6**, render **4** (rev-65 geometry) and **3** (as shipped).
   Raw pixels outward along the V's left arm at 115° read red to r 0.63, **neutral cream
   (131,131,127), saturation +4**, from 0.66 to 0.78, then the ring from 0.81 — **cream in the
   gap, not shadow.** Yet the mesh puts every terminal at **0.8400 R** against a band inner
   edge of 0.8000, and `terminal_reach()` finds 102 of 108 outline vertices inside the band.
   **THE MESH AND THE RENDER DISAGREE AND REV 66 DID NOT FIND WHERE.** One hypothesis — the
   cream disc winning the depth test — was built, guarded and **REFUTED** (F206: the clearance
   is already +2.04 mm at the original standoff). **Do not re-try that one.** Start by painting
   `probe_scratch/rev66_render_cells.png` beside a fresh render.
3. **C4 IS THE EMBLEM'S LAST RED ROW — 0.0755 against a bar of 0.045.** With L4 working
   (F203) the solver can see the trough landmark **for the first time**, and `T1_VW_SOLVE=1`
   is sitting there unrun. Errors now: **L1 −0.0307, L3 −0.0239, L4 +0.0634**; L5 and L6 are
   within 0.01. **RE-SOLVE THE SIX CONSTANTS AND THEN RENDER IT** — rule 41, and it has
   refuted a winner in three of the last four revisions.
4. **THE FIT DEPTH IS STILL UNMEASURED — and F205 may or may not be the same defect.** The glyph's
   extreme is fitted **20 % into the band** (`1.0 - 0.8 * _BAND_FRAC` in `vw_logo_fit`).
   Rev 44 warns that fitting to the OUTER radius **buries the arms**. **The answer is between
   and it is a MEASUREMENT, not a guess** — and the ring's own profile
   (`roundel()`: R, R−0.002, R−0.012, R−0.024, R−0.028, R−0.020) says where its visible inner
   lip actually is. Nobody has measured this.
5. **PUT AN ADVERSARY ON THIS BRIEF (rule 15), AND POINT IT AT §2's REFUTED LIST** — see the
   warning under it. Rev 64's adversary found fourteen.
6. **FIX `probe_rev63_shapefit.py`** — its baseline is stale and it reads `CAP_EMBLEM_WFRAC`,
   the HUBCAP's weight, where the nose ships its own (F178's trap). **F204 has now MOVED the
   nose's weight, so that probe is further out of date than it was.**
7. **F156 — `flank_compare`'s `Senor` row scores a DELIBERATE DEPARTURE. SIX revisions
   unacted.** Re-base the reference or annotate the row.
8. **TRIAGE `REMAINING_WORK_rev61.md` §I** — 27 rows, SIX revisions.
9. **THE SURVIVING PANEL ITEMS**, untouched for six revisions: the glass is a flat slab
   (0.5 % sd against the photograph's 12.8 %); **the tyres have no tread, no sidewall
   lettering, and are 35 % too light**; the tail is a box where the real one is a barrel;
   every shut line is a 1-px ink stroke with no leading-edge highlight; the galley is
   monochrome; the counter is a floating slab.
10. **F143 — TWO LOUDSPEAKERS STAND ON THE ROOF AND ARE UNMODELLED.** 54 revisions.
11. **THE INHERITED CLUSTER** — F14 (**fourteen** revisions un-re-measured), F15, F10, F20.
12. **`delivery/READ_ME_FIRST.txt` LISTS THE MODEL'S KNOWN DEFECTS TO HIM.** It does not yet
    mention the rev-63 emblem change, F184, F194, F197, or **rev 66's F200/F202/F204**.

**RANKING NOTE — AND THE RULE IT CARRIES IS NOT DROPPED.**
**RANK BY PIXELS OF THE DELIVERY FRAME** — `python3 visibility_budget.py 3840
out/r67_hero.png` — **and PASS IT A `.png`**, or it globs `out/` by mtime and reproduces F132.
Its ceiling: pixels are not visibility, so use it for ORDERS OF MAGNITUDE. **But he has
overridden the ranking three times in three revisions, and the owner outranks it — which is
why items 1 and 2 are his, not the budget's.**

---
## §4 WHAT WAS ASKED OF HIM — A CARRIER, NOT A LIST OF BLOCKERS

> **READ §0.1 FIRST.** At rev 54 he ruled the reference set on the repo is complete. This
> section is kept in full because rule 16 forbids dropping a carrier.

**`PHOTOS_WANTED_rev52.md` is the carrier for item 7 (ONE HUBCAP, SQUARE ON AND CLOSE).**
Items **1–5** keep their full text in `PHOTOS_WANTED_rev49.md`. **He has said 1–5 are not
possible now. DO NOT RE-ASK THEM.** Item 6 was **DISSOLVED at rev 51**.

**HIS SETTLED RULINGS — DO NOT RE-OPEN OR RE-ASK ANY OF THESE.** W6 makes colour his call;
the roof strips' 0.3 m retired; the wipers withdrawn entire; the lower bay SHUT; the RED bus
is the target and paint/artwork do not transfer between vehicles; the tail board IS on the
vehicle; the marks above the burst are STARS; `lid_rail`'s width *"narrow lip, ~as wide as it
is tall"*; the roughness trade *"ship 0.250"*; the stranded rev-57b branch *"merge it,
renumber its IDs"* — **DISCHARGED AT REV 64, seven revisions late (F188)**; the studio *"keep
studio — ruling stands"* (twice); the front arch *"leave it circular"*.

> **AND ONE LINE OF THAT LIST WAS NEVER HIS — CORRECTED BY ASKING HIM, AFTER REV 62.**
> It carried *"`playa_env.py` is not on the table — do not re-propose it"* from rev 52 to
> rev 64. **That entered as a brief's INFERENCE from W6, whose object is the studio RIG, and
> was applied to a SECOND DELIVERABLE — rule 34 exactly.** Put to him as multiple choice with
> both readings quoted, he ruled the Playa hero **"DEPRIORITISED, NOT CANCELLED"** — which is
> what his own rev-43 words said before that carrier was deleted at rev 44 (**F92**).
> **The correction sat on an UNMERGED BRANCH from rev 57 to rev 64 while every brief kept
> publishing the misattribution (F188).**
>
> **WHAT IT LICENSES: NOTHING TO DO NOW.** *"Focus on the 3d model"* stands, *"keep studio"*
> stands, **no revision works the Playa hero until he opens it**, and **nothing re-proposes
> `playa_env.py` as the delivery frame** — which is also why **F57** stays recorded rather
> than fixed. What changes is that it is a LIVE agreed second deliverable carried in the
> register, and that *"the emotional bar that sits ABOVE clinical accuracy"* is back in the
> record. **Do not re-ask it; do not act on it either.**

**RULED AT REV 66 — BOTH NEW, BOTH BINDING, AND THEY SET THIS REVISION'S WORK LIST.**
Asked as multiple choice with `probe_scratch/rev66_emblem_ba.png` and
`probe_scratch/rev66_photo_before_after.png` attached and the measured ink figures quoted:

> ***"The W's outer arms sit too low"*** AND ***"The strokes still don't reach the ring."***
> — **BOTH, chosen together, as what is STILL wrong with the emblem.** He did **NOT**
> re-report the strokes as too thin, which is the axis rev 66 moved.
> **Each maps onto a measurement this project already held:** the arms are **C4**, still red
> at 0.0755 against a bar of 0.045 with L4 the largest error at **+0.0634**; the reach is
> **F205** — C6's own interior-cell function run on the RENDER gives the photograph **6** cells
> against the render's **4 before and 3 after**, where the raster reads 6 for both.
> **HIS REPEAT IS A MEASUREMENT. This is his SEVENTH report of this emblem.**

> ***The nose's shape — FIRST.*** Asked directly whether rev 67 should do the nose or finish
> the emblem, he chose **the nose**. **F197 IS NOW A RULING, NOT AN INFERENCE**, and §3 item 1
> is his, not the ranking's.

**RULED AT REV 65 — BOTH NEW, BOTH BINDING, AND THEY SET THE WORK LIST:**

> ***"I don't think the bus is ready yet. We need the bus to be ready before investing
> seriously in the render."*** — **HIS THIRD HOLD** (rev 58, rev 64, rev 65), and this one
> was VOLUNTEERED, not asked for. It also settles what the render will be when it comes:
> **MULTIPLE SIZES, MAX RESOLUTION, MAX FIDELITY, ALL IN ONE FOLDER.** **F193.**
> **CONSEQUENCE: F192's "prove the large-format chain" drops BELOW the model defects.**
> Do not spend a revision on the pipeline.

> ***"we still have work to do on the shape of the nose."*** — **A SECOND DEFECT, AND IT IS
> NOT THE EMBLEM.** The emblem sits on the nose; he named the nose's SHAPE separately.
> **It corroborates a finding the record already held and never acted on**: rev 51 held the
> nose against the photographs and found **flush headlamps, the roundel's short V-arms, and
> A FLAT NOSE**. The V-arms became the emblem item; **the flat nose was never worked, and
> there is still no instrument for it.** **F197. It is §3 item 2.**

**RULED AT REV 64 — BOTH STILL BINDING:**

> ***"Keep holding — fix the emblem first."*** — the full delivery render. **His rev-58 gate
> is REAFFIRMED, and this time against a revision that could have shipped.** Asked with the
> crop attached, and with the plain statement that the route rev 63 nominated had been built,
> rendered and refuted. **F191. NO DELIVERY RENDER UNTIL HE SAYS SO.**

> ***"Bigger — large-format print."*** — over the pipeline's 3840×2640 default. **THE EXACT
> DIMENSION IS STILL OPEN**: the option invited him to name the medium and he did not. **Do
> NOT re-ask it cold — ask once you have something to show him.** What is settled: **3840 is
> not the target**, so the banded path must be proven larger. **F192.**
> *(And note what the question corrected: the rev-63 and rev-64 briefs both stated
> `deliver.py` "shipped a set at 2400×1650". **That figure is in no source file and no
> ledger** — `deliver.py` carries no output resolution at all. The premise was withdrawn in
> the asking. F189d.)*

**RULED AT REV 62, STILL BINDING:**

> ***"Bright silver, same as Tacombi."*** — the `Señor` word's finish. **This OVERRIDES SPEC
> §3's WEATHERED LOCK FOR THAT WORD ONLY.** SHIPPED as `script_gen.SENOR_TARNISH = 0.0`.
> `T1_SENOR_TARNISH=1` restores the pre-ruling texture byte for byte. **F157.**

> ***"It is going on different backgrounds for promotional material etc. give me everything I
> might need."*** **BUILT**: `T1_ALPHA=1` renders RGBA with the contact shadow in partial
> alpha (**F159**), and `deliver.py` packages full-frame, trimmed and SEPARATED
> vehicle/shadow layers with a plain-language `delivery/READ_ME_FIRST.txt` (**F160**).
> **It does NOT retire the rev-58 hold, which he has now reaffirmed (F191).**

> ***"this is just the render to plug into company merch with different backgrounds once i
> determine the model is done"*** — **HE DID NOT AUTHORISE THE BOUNCE CARD; "keep studio"
> stands.** Consequences in **F155**: the white backdrop is **scaffolding**, a clean matte
> matters, and **the gate is HIM determining the model is done.**

**RULED AT REV 61:** ***"senor Tacombi should be clearer in the render than in that photo.
Well defined. I want this 3d model to look like new. Enhanced from the photo."*** **It
creates a live tension with SPEC §3's WEATHERED lock — surface it, do not silently pick a
side.**

**CARRIED FROM REV 53, AND STILL IN NO OTHER DOCUMENT:** a frame showing the cream **where it
IS chipped**. Rev 54 and rev 55 both lowered its urgency — the band is 0.27 px at every scale
this project ships — but it is **not struck**, and F19 covers the MODELLING of chipping, not
the photograph request.

**AND HE VOLUNTEERED, STILL BINDING:** the emblem needs a fix, and **the full delivery render
waits until the model is right.**

**STILL WORTH HIS TIME AND NOT ASKED:** **F38** — the nose ring band at the top of its adopted
range, which interacts with the emblem *(and with F185: fitting the ring on the frame gives
this a target too)*; **F39/A3** — `Senor`'s ink deficit; and **the local bounce card** both
panels proposed independently, which is a studio change under a ruling he has given twice.

---
## §5 THE RULES — `CLAUDE.md` CARRIES THE METHOD, NOT THE NUMBERED CANON

The canon (rules 1–33) is printed in `NEXT_CONTEXT_PROMPT_rev50.md` §11. Rules 34–44 live
only in the briefs and are carried here — that is rule 16 firing on this file:

> **34. A REQUIREMENT INHERITS ITS OBJECT EXACTLY AS A RETIREMENT DOES.** Check which object
> a *"the record requires X"* sentence is about, and check the cited line exists. **F26 is
> still open. And rev 64 found rule 34's own textbook case still live in §4 for the
> thirteenth revision — see F188.**

> **35. A GUARD WRITTEN AGAINST A POSE ENCODES THAT POSE.** Ask the geometry, never the pose
> it happens to be in. **Rev 64's sibling: a VERIFY row counted "two mitred prisms per wheel"
> and went red on a glyph built as one object — the row encodes the CONSTRUCTION.**

> **36. A GATE ONLY COUNTS FOR WHAT IT CAN SEE — ABLATE THE THING YOU ARE ABOUT TO TUNE,
> FIRST.** **Rev 64 ablated the FRAME rather than the glyph, and that is what found F184.**

> **37. AN ABSENT INPUT MUST NEVER READ AS A MEASUREMENT.** A probe that cannot run must say
> **"NO RENDER"** and exit non-zero.

> **38. TWO SIDES OF A RATIO MUST SHARE A RULER, AND IF THEY CANNOT, SAY SO IN THE ROW'S OWN
> NAME.** **Rev 64 found this twice in one probe: a 9 % scale error worth 0.30 of IoU (F186),
> and a whole comparison column that broke it toward the conclusion it was used for (F187).**

> **39. A GATE'S TARGET IS AN INSTRUMENT TOO, AND MUST BE SWEPT LIKE ONE.** C6's 7 (F139),
> M1's ruler (F136), C8's window (F151) — **and now C6's AND C8's targets together, which are
> read off images that are not mirror-symmetric (F184). This is rule 39's largest instance.**

> **40. WHEN AN OWNER RULING MAKES THE MODEL DEPART FROM THE REFERENCE, THE GATE THAT SCORES
> AGAINST THAT REFERENCE STOPS MEANING WHAT IT MEANT.** **F156, and rev 62, 63 and 64 all
> failed to act on it.**

> **41. A GATE PASSING IS NOT EVIDENCE THE THING IS RIGHT. BUILD THE COUNTEREXAMPLE.** C6,
> C8 and IoU all passed on a glyph that rendered as a Y (F175). **AND AT REV 64 IT FIRED
> AGAIN, ON THE ITEM IT WAS WRITTEN ABOUT: the traced pressing won on cells, on elongation
> and on IoU, and rendered as a blob (F183). The render is the arbiter.**

> **42. A CONTROL'S KILL IS A PRECONDITION ON ITS PASS.** If the kill cannot go red at a
> point in parameter space, the control's PASS there means nothing. **C7 was dead exactly
> where C6 went green (F176). Read the kill first.**

> **43. NEW AT REV 64 — A PHOTOGRAPH IS A PROJECTION, AND A DE-SQUASH IS NOT AN
> UN-PROJECTION.** Rescaling two axes cannot undo a rotation or a shear. Before taking ANY
> shape statistic off a frame, ask what symmetry the real object has and check the frame
> still has it. **The VW mark is mirror-symmetric; both badge frames read 0.41–0.48 against
> the model's 0.9777 (F184).**

> **44. NEW AT REV 64 — WHEN A GUARD GOES RED ON YOUR OWN NEW WORK, THE GUARD IS THE DEFAULT
> WINNER.** Rev 64 graded its own register row with a word outside the register's vocabulary
> and the grade guard failed it. **The vocabulary was not widened; the row was regraded.**
> Widening a guard to admit your own output is the laundering these guards exist to stop.

---

> **45. NEW AT REV 66 — A TARGET CAN BE UNREACHABLE, AND NOTHING INSIDE THE INSTRUMENT WILL
> SAY SO.** Rule 39 says sweep a gate's target like an instrument. Rev 66 adds the harder
> case: **ask whether the thing you are building could EVER produce that target.** C6 wanted
> 7 cells; a V fused to a W meets the band at six points and therefore cuts the disc into six,
> and 144 perturbed builds produced 7 not once. **Six revisions of work were aimed at a number
> the mark cannot make (F200).** A literal at least changes when someone edits it; a wrong
> target is invisible and every audit passes over it.

> **46. NEW AT REV 66 — A REFUTATION INHERITS ITS INSTRUMENT.** *"Tried, refuted"* is only as
> good as the gate that scored it. **Three rows of §2's do-not-re-try list were scored on
> gates now known to be mis-targeted**, and one of them — the stroke weight, F152's *"moves
> the WRONG way"* — turned out to be the revision's actual fix (F204). **Before you accept a
> refutation, check what it was measured with, and when.**
---
## §6 THIS MACHINE

```
cores 4   RAM 15 GB   Blender 4.5.3 via pip install bpy   subagent concurrency 2
build  T1_SUB=1 ~20 s     render 1600x1100 96 spp ~4.5-5.5 min PER VIEW
```

**`bpy` IS A PIP MODULE HERE**, so `python3 probe_rev46_vw.py` runs in ~1.1 s without the
Blender CLI. **Check whether a probe needs `blender -b -P` before you budget minutes for it.**

> **AND A METHOD REV 66 PROVED, WHICH IS WORTH MORE THAN THE TIME IT SAVED.** The emblem's
> whole search was done in a **pure-2-D replica** with no `bpy` at all, while Blender had all
> four cores for the baseline render. **The replica was validated on a KNOWN ANSWER first** —
> it reproduced the live probe's 6 cells, elongation 2.388, extreme 0.8140 and CAPMIN's
> 2 cells / 1.310 / 0.9250 — and afterwards against the RENDER, whose radial profile it
> matches to 0.02 at every annulus. **Prove the proxy on a known answer, then use it.**

```bash
./bootstrap.sh                                               # THE TOOLCHAIN IS NOT ON THE CLONE
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
./judge_set.sh r67                                           # the optics chain (F146)
python3 flank_compare.py out/r67_side.png /tmp/fc.png        # GATE 1
python3 gloss_compare.py out/r67_hero.png                    # GATE 3
python3 probe_rev59_nose.py out/r67_front.png                # READ BOTH RULERS
python3 probe_rev46_vw.py                    # THE EMBLEM GATE -- C4 is the only red row
python3 probe_rev64_shear.py ; python3 probe_rev65_unproject.py
python3 probe_rev63_trace.py ; python3 vw_pressing.py ; python3 probe_rev63_canon.py
python3 probe_rev63_ablate.py                # the construction's ceiling
python3 probe_rev63_shapefit.py              # F175's counterexample -- BUT SEE SS3 ITEM 5
python3 probe_rev63_reach.py                 # contacts with the ring, and angles
python3 trace_outline.py ; python3 svgraster.py ; python3 senor_trace.py
python3 cream_rms.py                         # the LIVE photograph-side cream
python3 visibility_budget.py 3840 out/r67_hero.png   # PASS IT A .png -- see F132/F189
T1_SUB=2 /tmp/blender/blender -b -P audit.py         # rewrites STATE.md -- COMMIT FIRST
python3 audit_brief.py ; python3 audit_adversary.py  # rules 15/17, MECHANICAL half only
```

**THE GATES THE ABLATIONS EXIST TO MAKE REFUSE:**

```bash
T1_SUB=1 T1_NOUNDER=1 /tmp/blender/blender -b -P probe_rev45_ground.py  # C5 must REFUSE
T1_SUB=1 T1_PG_PAINT=1 /tmp/blender/blender -b -P probe_rev45_ground.py # paints G4's window
python3 probe_rev59_door.py out/r67_side.png        # M3 fails BY DESIGN.  **SIDE FRAME** --
                                                    # a front frame kills it with an
                                                    # UnboundLocalError, not a refusal
python3 probe_rev61.py emblem --paint               # every mode paints its window
T1_VW_NOARC=1 T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py  # rev 65's
                                                    # perpendicular cap, rebuildable (F202)
T1_VW_TRACED=1 T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py  # F183's refutation.
                                                    # IT MUST NOT SHIP
```

**ABLATION SWITCHES — all MEASUREMENT-ONLY:** **`T1_VW_NOARC` (NEW at rev 66 — restores the
PERPENDICULAR terminal cap exactly as it stood at rev 65; the arc cut is what SHIPS)**,
`T1_VW_TRACED` (**REFUTED, F183; two verifier rows hold it OFF**), `T1_VW_WFRAC`
(**F178: it overrides the NOSE's weight, `vw_logo_fit()`'s signature default — NOT
`CAP_EMBLEM_WFRAC`, which is the HUBCAP's. The nose's default is now 0.2283, F204**),
`T1_VW_CAPMIN`, `T1_VW_PUREFIT`, `T1_VW_CELLSOLVE`, `T1_VW_DUMP`, `T1_VW_RES`, `T1_VW_WSWEEP`,
`T1_VW_SOLVE`, `T1_VNOSE_DIV`, `T1_BULB_STR`, `T1_BULB_BASEV`, `T1_SENOR_BREAKS`,
`T1_SENOR_TARNISH`, `T1_ALPHA`, `T1_NOUNDER`, `T1_UNDER_ZBUG`, `T1_UNDER_PROUD`,
`T1_UNDER_VIS`, `T1_UNDER_YBUG`, `T1_UNDERSEAL`, `T1_VPOW`/`T1_VPOWZ` (**move them
TOGETHER**), `T1_VRISE`, `T1_DOOR_STALE`, `T1_NORIG`, `T1_RIG`, `T1_WORLD`, `T1_MOT_AMP`,
`T1_GL_WRGH`, `T1_BODY_RGH`, `T1_GC_ABSSPREAD`, `T1_GC_LOOSEMASK`, `T1_GL_TILES`,
`T1_PG_PAINT`, `T1_BAREMAT`, `T1_CLAY`.

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
* **`vw_pressing.py`'s `trace()` is NOT called by `build.py`** — the outline is a committed
  literal and the selftest is what holds it to the photograph. That is deliberate.
* **`audit.py` rewrites `STATE.md`. COMMIT FIRST** — and regenerate it after ANY geometry
  change. **Rev 66's change moved it by +920 verts / +460 faces and NOTHING ELSE**, which is
  itself the evidence the change was contained.
* **LAUNCH LONG RENDER QUEUES WITH `setsid`, NOT A BARE `nohup &`** — F173.

**THE DELIVERY CHAIN, WHICH IS NOT THE PREVIEW CHAIN:**
```bash
T1_SUB=2 /tmp/blender/blender -b -P hq_render.py    # ONE build, 10 bands, WITH MARGIN
python3 stitch.py out/hq_hero_raw.png ...           # CHECK ITS EXIT CODE -- 2 on a seam (F49)
python3 post.py out/hq_hero_raw.png out/hq_hero.png # optics LAST, never per strip
```

**THE DELIVERY FRAME — DO NOT RUN IT. He REAFFIRMED the hold at rev 64 (F191) and again at
rev 65 (F193). And he needs LARGE FORMAT, which this chain has never been proven at (F192).**

---
## §7 THE STANDARD, IN HIS WORDS

We are recreating a photorealistic version of **that exact bus**, and **any single measurement
off is unacceptable** — per-measurement, not on average. **Ground in the reference, build,
adversarially audit, iterate.** Never build before grounding. Never call it done off
self-review. Report the measurement **with its ceiling**, never a self-assigned score. Do not
say anything is ready — say what is fixed, what is still wrong, and what you measured.

**RENDER IT, CROP IT, AND LOOK AT IT, before and after every change.** Every defect this
project has shipped passed `VERIFY: 0 fail, 0 warn` and was found by looking at a crop.
**At rev 64 the traced pressing won on every statistic the project owns and rendered as an
unrecognisable blob. One crop settled it in ten seconds.**

**When you need something from him, ask as MULTIPLE CHOICE with the reference material
attached — one crop, one mark, one sentence — and ASK IT WITH THE QUESTION TOOL.**
**And CHECK THE PREMISE FIRST: rev 64 came within one step of asking him a question built on
a figure that exists in no source file (F189d).**

---
## §8 THE OPEN-FINDINGS REGISTER — `OPEN_FINDINGS.md`

**IT IS A CARRIER (rule 16). Rows leave it only by being CLOSED with the measurement that
closed them, or RETIRED with the ruling that retired them. Never by being dropped.**

**Rev 66 added F200–F204**, of which **three are defects in this project's OWN instruments**
and **two of those invalidate TARGETS rather than measurements** — a class this register had
never carried before. **F198 and F196 were both re-graded in the same edit (rule 13): F198 is
CLOSED, and F196's premise is withdrawn because the reach figures it quoted were F198's
literal.** Rev 65 added F193–F199; rev 64 added F183–F192.

**THE POINT OF THE FILE IS THE PROVENANCE GRADE, NOT THE LIST.** An `INHERITED` row is a
claim. **GRADE DECAY IS ITSELF A FINDING.** *(The grade vocabulary is
MEASURED / RECOMPUTED / INHERITED / RULED / CEILED / OBSERVED. **Do not widen it** — rule 44.)*

**STILL INHERITED AND OLDEST:** **F14** (`gal_end_f`'s sight lines, **rev 52 — FOURTEEN
revisions un-re-measured**), F15, F20, F10, and **F18** (the die-cut sticker, rev 44 — the
oldest live row and the project's original deliverable).

**AND `REMAINING_WORK_rev61.md` §I IS STILL NOT TRIAGED** — 27 rows, **six revisions**.

---
## §9 THE HORIZON BEYOND REV 67

**CARRIER: re-rank it, do not rewrite it, and say what moved.**

**AND WHAT REV 66 LEARNED LAST, WHICH RE-RANKS THE REST.** C6 was repaired, re-based, killed
and swept until it PASSED — **on a raster that does not predict the render on the axis C6 is
named for.** The owner looked at the frame and named the defect the gate could not see (F205).
**Run the emblem gates on the FRAME before you believe them.**

**WHAT MOVED AT REV 66.** The emblem's **stroke weight** was fitted and shipped, by two
statistics that share no ruler; the **arc-cut terminal** was built and shipped; and **three of
the project's own emblem instruments were found to be reporting things that were not
measurements** — C6 against an unreachable target, C4/C5 against a landmark that was 96 % of
its own residual, and C6's message (F198) repaired with a kill that holds it. **C6 now PASSES.
The emblem gate went from 3 red rows to 1.** **What did NOT move: the NOSE, and everything
outside the emblem.**

**WHAT MOVED AT REV 65.** The badge's ring was fitted as an ellipse, re-basing C8's target;
the reach was measured live off the mesh; the naming sentence was found to be a literal.

| horizon | the work | why |
|---|---|---|
| **next** | **THE NOSE'S SECTION (§3 item 1, F197)** | **He asked for it by name TWO revisions ago and it has not been touched.** It is now the top item |
| **next** | **F205 — THE RENDER CUTS 3 CELLS WHERE THE PHOTOGRAPH CUTS 6 (§3 item 2)** | **The owner's own second sentence, and C6's own statistic says so — on the FRAME, which the raster does not predict.** The mesh says 0.8400 R and the render disagrees; rev 66 did not find where |
| **next** | **C4 — re-solve the six constants (§3 item 3)** | The emblem's last red row, **the owner's first sentence** (*"the W's outer arms sit too low"*), and the solver can see L4 for the first time |
| **next** | **THE TIP/RING GAP (§3 item 3)** | The photograph shows none; nobody has measured the fit depth |
| **next** | **AN ADVERSARY ON THIS BRIEF, AIMED AT §2's REFUTED LIST** | **Three of its rows were scored on gates now known mis-targeted** |
| **near** | **F156 — the `Senor` gate row scores a DEPARTURE** | SIX revisions unacted |
| **near** | **Fix `probe_rev63_shapefit.py`** | Stale baseline AND the hubcap's weight — **and F204 moved the nose's** |
| **near** | **Triage `REMAINING_WORK_rev61.md` §I** | 27 rows, six revisions |
| **near** | **Glass, tyres, the tail's barrel, the shut lines** | Untouched for six revisions |
| **near** | **F143 — the roof loudspeakers** | Unmodelled since rev 12 — 54 revisions |
| **LOWERED** | **F192 — prove the large-format chain** | **He ruled the MODEL comes first (F193).** Do not spend a revision on the pipeline |
| **then** | **F10–F14 — the galley cluster** | F14 is FOURTEEN revisions inherited |
| **CEILED** | **F153; F168; F183 the traced pressing; F195 the rotation search; F44/F60/F62 gloss; F83; F67; F142; F148** | **F62 is DISPUTED — do not quote it without testing it** |
| **standing** | **F18 — the die-cut sticker** | The original deliverable. Open since rev 44 |

---
## §10 HOW TO GROW THIS HANDOFF WITHOUT BREAKING IT

1. **The set is three files.** `LEDGER_rev<N>.md`, `NEXT_CONTEXT_PROMPT_rev<N+1>.md`, and
   **`cp` of that file over `PASTE_INTO_CLAUDE_CODE.txt` IN THE SAME COMMIT.**
2. **`README.md` and `START_HERE.md` name the newest brief BY NUMBER.** Two rows check it.
3. **THE ROW COUNT IS SELF-REFERENTIAL AND AUTOMATED.** `python3 audit_brief.py
   --fix-count`. Write it LAST. *(It reads the CLEAN-TREE total. On a dirty tree
   `verify_clone.sh`'s own row expects `PASS+1`, which undercounts by the number of earlier
   failures — that is an artefact of the dirty tree, not a defect in the count.)*
4. **ADD ROWS ANCHORED ON ARITHMETIC OR BEHAVIOUR, NOT ON A GREP.**
5. **RUN BOTH AUDITS AS SCRIPTS AND RECORD WHAT THEY FOUND *IN* THE BRIEF.** **REPLACE the
   adversary's questions each revision** — a question that can no longer fail is not a control.
6. **NEVER DELETE A CARRIER.** §0, §0.1, §4, §5, §8 and §9 are carriers.
   **`EMBLEM_HANDOFF.md`, `PANEL_rev61.md` and `REMAINING_WORK_rev61.md` are carriers too.**
7. **RANK BEFORE YOU CHOOSE** — but **the owner outranks the ranking**.
8. **NEVER RELAX ONE COPY OF A CHECK.** Rev 64 re-based `probe_rev63_trace.py`'s T3 with the
   cause named and **four** companion rows, one of which is a kill that was watched firing.
9. **DO NOT LET THE MACHINE IDLE.** Run `bootstrap.sh`, launch the render, then read.
10. **ROOM TO GROW:** new findings go in `OPEN_FINDINGS.md` with an ID and a grade.
