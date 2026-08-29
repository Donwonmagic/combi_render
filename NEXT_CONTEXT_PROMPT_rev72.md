# NEXT CONTEXT PROMPT — rev 72   ·   **ACTION BRIEF**

**SHORT ON PURPOSE. Read it end to end before you touch anything; it fits.**
**Every carrier — refuted routes, owner rulings, the rules canon, the gate tables — is in
`HANDOFF_CARRIERS.md`, complete. Nothing was deleted. DO NOT RE-MERGE THEM.**

> *[owner, rev 69]* **"It is important that we finish the nose render, make the emblem correct
> (a bare minimum qualification) and fix the opening."** … **"I meant to say the back opening."**
> and ***"It's been weeks, and a lot of compute, this is unacceptable."***

> **⚠ REV 71 SHIPPED NO VISIBLE CHANGE TO THE VEHICLE AND SAYS SO AT THE TOP OF ITS LEDGER
> (rule 55). NOT ONE CONSTANT MOVED — `STATE.md` differs from rev 70 ONLY in its provenance
> block.** It spent itself proving that **the ruler for the owner's top item is broken (F246)**,
> and it did **not** ship a candidate that measured +0.024 on that ruler. **That was the right
> call and it is also the whole cost of the revision. Rev 72 must SHIP.**

---
## §0 DO THIS FIRST — THE MACHINE IS IDLE WHILE YOU READ

```bash
cd /home/user/combi_render
./bootstrap.sh                 # the toolchain is NOT on the clone -- this builds it
pip install pillow             # bootstrap FAILS 3 of 10 without it, EVERY revision
nohup setsid env T1_SUB=1 T1_PREVIEW=front,side,hero34f,hero34r T1_PFX=r72 T1_RX=1600 T1_RY=1100 \
  T1_SAMP=96 /tmp/blender/blender -b -P build.py > /tmp/r72.log 2>&1 < /dev/null &
```

**`grep -c Saved: /tmp/r72.log` must be 4.** **USE `setsid`, NOT A BARE `nohup &`** (F173).
**`out/` is untracked and starts EMPTY** — re-render before quoting any figure from a frame.
**DO NOT EDIT SOURCE WHILE THE QUEUE RUNS.**

**⚠ THE PREVIEW PATH NEVER CALLS `post.py` (F146).** Run `./judge_set.sh r72` and judge on the
`_post` set. **It was BROKEN until rev 71 — it looped over a `hero` no preview list produces, so
it exited 2 and never post-processed `hero34f`, the delivery view (F248). It now exits 0 and
writes four frames. If you change `T1_PREVIEW`, change its loop in the same edit.**

---
## §1 THE BRANCH — MEASURE IT, DO NOT TRANSCRIBE IT, **INCLUDING THIS SENTENCE**

```bash
git fetch --all --prune
git rev-parse --is-shallow-repository
for b in $(git branch -r | grep -v HEAD); do
  printf "%-52s ahead %-3s behind %s\n" "$b" \
    "$(git rev-list --count origin/main..$b)" "$(git rev-list --count $b..origin/main)"; done
git diff --name-only HEAD...origin/main        # <- HIS PHOTOGRAPHS ARRIVE HERE
```

> **AT REV 71's PICKUP the rev-71 brief's §5 warning was FALSE IN EVERY CLAUSE (F253)** — the
> branch it said was stranded had been merged by PR #27, `origin/main == HEAD`, and `main` DID
> carry the carriers it said were missing. **That is SEVEN consecutive revisions of stale branch
> prose, and rev 71's was stale in the OPPOSITE direction from rev 70's.**
> **A brief cannot carry a true statement about branch state across a revision boundary. Only the
> loop can. Believe `bootstrap.sh` row 9 and the output above, never this paragraph.**

---
## §2 ITEM 2 — THE EMBLEM · **ITS RULER IS BROKEN. FIX THE RULER FIRST. F246.**

**DO NOT MOVE ANY EMBLEM CONSTANT UNTIL P1b PASSES.** `python3 probe_rev69_fitpose.py` and read
its rows:

```
    the SAME search, SAME model, SAME known 37 deg / 0.62 / shear / perspective view
        P1  framed as the probe frames it   (uncropped)     IoU 0.9882
        P1b framed as photo_mark frames EVERY real target        0.4988   <- REFUSES
    the MARK itself, ref_workshop.jpg                             0.7345
```

**`photo_mark` bbox-crops every photograph; P1's control is the raw `warp` output; `fit()` searches
NO TRANSLATION while its docstring asserts both masks are already bbox-centred — false for a crop.
THE CONTROL SCORES 0.25 BELOW ITS OWN SPECIMEN.** So **`0.9882 − 0.7345 = 0.2537` IS NOT A SHAPE
DEFICIT**, and **F237's "4.4 % of the deficit" is a ratio against a number that is not what it
claims.** *(F237's direction survives: the levers ARE nearly inert, re-measured +0.0124.)*

**THE REPAIR IS SPECIFIED AND HALF-MEASURED. FINISH IT.** Two translation terms lift the mark
**0.7345 → 0.8324** and **0.6553 → 0.7944** on two independent frames — **but lift the CONTROL only
0.4988 → 0.5403**, still far below its 0.90 bar. **Necessary, not sufficient.** Rev 71 therefore
did **not** change `fit()`. **Rev 72's first emblem job: a pose search whose P1b PASSES.** Candidates
not yet tried: a full 8-DOF homography solved rather than coordinate-descended; registering on
centroids or second moments before the search; or scoring on an uncropped common frame so the
control and the measurement share a framing.

**⚠ DO NOT FIT TO AN ANGLE** — `probe_rev69_angles.py`'s control A1 **FAILS at 36.30° rms**.
**⚠ FIT ON ONE FRAME, SCORE ON THE OTHER.** **⚠ `IMG_2073`'s box: use the RE-CUT
`(283,537)–(357,662)`** — the shipped `(288,542)–(352,640)` discards ~14 % of the ink (2527 → 2926
on-px, reproduced at rev 71). **TWO live files hard-code it: `probe_rev69_fitpose.py`'s `FRAMES`
and `audit_adversary.py`. Re-cut one only and the guard silently checks the clipped window.**

**AND TWO ROUTES ARE NOW CLOSED — DO NOT RE-TRY THEM (F251, F252):**
* **THE FIT DEPTH IS MEASURED AND WAS ALREADY RIGHT.** Swept 0.70–1.00; the shipped **0.84** is
  within one sweep step of the argmax on **both** frames. `probe_rev71_emblem.py`, 3/0.
  **⚠ It lives in `t1_detail.vw_logo_fit`, NOT `t1_core.py` where the rev-71 brief cited it.**
* **THE "FREE ENDPOINTS" CONSTRUCTION BUYS 0.0009.** The rev-71 brief's own prescription, run in
  the proven proxy: current params re-searched **0.7469** (but **0.5689** on the independent frame
  — overfit); free endpoints **0.7478**; a 1400-start global search **0.7586 / 0.6698**. Every
  basin plateaus near **0.75**. **Rule 54's OBSERVATION stands — the strokes radiate where the
  photograph's are near-parallel — but its PRESCRIPTION is refuted.**
  **REPRODUCE THEM, DO NOT TRANSCRIBE THEM:** `T1_REV71_SEARCH=AB python3 probe_rev71_emblem.py`
  (~40 s) prints (A) and (B); `=ABC` adds the global search (~9 min).

**USE THE PROXY.** `probe_rev71_proxy.py` is a 2-D replica of the emblem raster **PROVEN
BIT-IDENTICAL to the bpy build** (IoU **1.000000**, 41255 px each, 276 rows) at **~0.01 s an
evaluation against ~2 s**. Run its `prove()` before trusting anything from it (rule 3).

**READ `HANDOFF_CARRIERS.md` §2 — SEVENTEEN REFUTED ROWS — BEFORE TRYING ANYTHING HERE.**
**AND F180 IS STILL STALE AND STILL UNCLOSED** — it says FOUR ring contacts; `probe_rev63_reach.py`
reports **SIX**, at a different set of angles (16/66/114/163/248/292 against F180's 62/118/212/328).
**This is its fourth carry. Close it or retire it.**

---
## §3 ITEM 1 — THE BACK OPENING · **TWO THINGS ARE LIVE AND ONE IS NOT WHAT THE LAST BRIEF SAID**

**(a) `glass_rear` IS HINGED OPEN 64° ON AN ANGLE ITS OWN SOURCE MARKS NOT MEASURED — AND THE
REV-71 BRIEF RULED THIS "SETTLED, DO NOT RE-OPEN".** A dispatched adversary found it and **rev 71
did not act on it.** `t1_shell.py` carries `REAR_OPEN_DEG = 64.0` and logs *"rear hatch:
glass_rear hinged … OPEN 64.0 deg [angle NOT MEASURED -- no frame shows it]"*. **F244's quoted bbox
`x −2.151…−1.850` is 301 mm; the CLOSED pane is 6 mm thick — so that bbox is the pane AFTER being
swung out, and F244's own words *"an aperture with a fully transmissive pane IN IT"* do not describe
the built object.** Its *"4 of 9 rays miss"* is equally consistent with *"there is a hole and the
pane hangs open beside it"*. **The owner said "the back opening". There is an actual 64° opening at
the back of this model on an unmeasured angle. PROJECT `glass_rear` AND THE APERTURE INTO
`out/r72_hero34r.png`, PAINT THEM, AND LOOK, before accepting F244** — which F244's own ceiling
already says was never done.

**(b) THE BULBS: F134 IS ANSWERED AND BOTH ITS LEVERS ARE MEASURED INERT (F249). DO NOT RE-SWEEP
THEM.**

```
    bead cores, ONE rule both sides            PHOTOGRAPH  sat 0.1839  V 0.9201  <- a LOWER bound
    T1_BULB_STR=0                                              0.0251     0.8516
    SHIPPED  str 9.0 / basev 1.0                               0.0417     0.9487
    str 3.0 / basev 0.05  THE PAIRING NEVER TRIED, best        0.0572     0.8770
```

**The null — *"the emission contributes nothing"* — is REFUTED: ablating it moves the bead.** But at
strength 9 the bead sits at **V 0.95**, where the view transform's path-to-white removes the chroma,
and a **20× darker envelope buys 0.0077**. **The best configuration is still 3.2× too neutral and
was NOT SHIPPED because it does not READ — rendered, cropped and looked at (rule 1).**
**WHAT IS LEFT: the emission COLOUR (not switchable) and the view transform — F240's surviving
branch.** `probe_rev71_bulbs.py` is the gate; **B2 watched failing at 4.4×**, B3 is an ablation kill.

**(c) THE STRIPES ARE NOT A MATERIALS PROBLEM — THE REV-71 BRIEF'S DIAGNOSIS WAS WRONG-CAUSED.**
`tail_board_edge` builds both bands on `ey = TB_Y_CENTRE - TB_WIDTH*0.5`, the **far** long edge, and
`studio.py`'s `side` camera is **orthographic** with its view direction **in the board's own plane**,
so the far edge projects onto the near one: measured on `out/r71_side.png`, **0 red pixels and 0 dark
pixels**. They are **occluded, not mis-shaded** — and **the red DOES read on `hero34r`**. Do not tune
`capred` against the side frame.

**⚠ THE CHORD CONFLICT IS STILL OPEN AND STILL MUST NOT BE AVERAGED:** two-height closure **0.710**,
calibrated read **0.790**, F165 **0.829**. The first two are both from `ref_side.jpg` and disagree by
**11 %**. **DO NOT re-derive `TB_CHORD` from a flat px/m** (`ref_side.jpg` is PROJECTIVE — use
`flank_X`/`flank_kv`). **DO NOT move the angle to F165's 28.0** — unreconciled, not refuted, and the
guard goes red there.

**AND THE GUARD'S OWN RECORD WAS WRONG UNTIL REV 71 (F247):** it recorded *"WATCHED FAILING … 86.3 mm,
2.9 sigma"* against a bar of **90.0 mm** — **that figure PASSES.** Cause: `2.2703` is the BUILD LOG's
**spine** tip; the row reads the **MESH** max, **2.2790**, 8.7 mm higher — a ruler mismatch inside the
docstring that warns about ruler mismatches. **Re-watched: `T1_TB_CHORD=0.8250` → +95.0 mm, 3.2σ,
`VERIFY: 1 fail`.** The retraction stands, but by **4.9 mm on a 90 mm bar**, not by 2.9σ.

---
## §4 ITEM 3 — THE NOSE · **RENDERED AND LOOKED AT AT REV 71. THE RENDER-SIDE ROW REFUSES.**

```bash
T1_SUB=1 T1_PREVIEW=front T1_PFX=r72 T1_RX=3200 T1_RY=2200 T1_SAMP=128 \
  /tmp/blender/blender -b -P build.py      # then CROP THE NOSE AND LOOK AT IT
python3 probe_rev67_nose.py out/r72_front.png    # PASS IT A FRAME
python3 probe_rev59_nose.py out/r72_front.png    # READ BOTH RULERS
```

**`probe_rev67_nose.py` on rev 71's frame: 5 checked, 1 FAILED — P3 REFUSES**, fit rms **113.92 px
= 12 % of span**, *"the clip RESCUED it"*. **So this project still has NO render-side reading of the
bumper's top edge**, and P3 has never once run to a number. Either give it a frame it can trace
(a true elevation rather than the preview's `front`) or re-cut the row.

> **⚠ AND `probe_rev67_nose.py` BARE PRINTS A GREEN SUMMARY AND EXITS 0** while its own first line
> refuses — *"NO FRAME GIVEN … the render row is ABSENT, not passed"* — 60 lines above the summary
> rule 9 tells you to read. **It also builds the whole shell in-process (~74 s), so it is NOT a
> ~1 s probe and must not run during the render queue.** Unfixed at rev 71; recorded.

**AND WHAT LOOKING FOUND, HANDED ON RATHER THAN ASSERTED (rule 37):** on the 1600×1100 nose crop
the **V's two arm tips end in mid-air with a visible gap to the ring band and a notch cut into each
tip.** That is the owner's *"the strokes still don't reach the ring"* (F205) **visible at this
resolution**, which sits against F233's *"substantially a preview-resolution artefact"*. **Measure it
before naming it.**

> **⚠ CEILINGS.** `verify._bumper_bow`'s own docstring: *"a 28 % error in the one constant it exists
> to police would PASS"*, *"NOT A FIDELITY CLAIM"*. F231: the bow's magnitude **cannot be recovered
> from the frames we hold**; F223's bracket **B ∈ [16, 76] mm contains the shipped 19.6**.
> **DO NOT ASK HIM THE NOSE AGAIN — both askings are spent.** Check the catalogue literature first
> (F229, rule 52); sources named in `HANDOFF_CARRIERS.md` §0.06.

---
## §5 THE MACHINE

```
cores 4   RAM 15 GB   Blender 4.5.3 via pip install bpy   subagent concurrency 2
build T1_SUB=1 ~20 s      render 1600x1100 96 spp ~4.5-6 min PER VIEW
```

```bash
./bootstrap.sh                                # ALL 10 PASS -- read ROW 9 and its NOTE
./verify_clone.sh                             # ALL 358+ PASS -- read its verdict block
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py    # -> "VERIFY: 0 fail, 0 warn"
./judge_set.sh r72                            # the optics chain -- FIXED at rev 71 (F248)
python3 probe_rev71_proxy.py                  # PROVE THE PROXY FIRST -- must read IoU 1.000000
python3 probe_rev71_emblem.py                 # the fit depth, CLOSED -- 3 checked, 0 FAILED
python3 probe_rev69_fitpose.py                # THE EMBLEM -- P1b REFUSES AND IS MEANT TO (F246)
python3 probe_rev71_bulbs.py out/r72_side.png # the bulbs -- B2 watched failing; bare, exit 3
  # and its KILL:  T1_BULB_ABLATED_FRAME=<a side frame rendered with T1_BULB_STR=0>
python3 flank_compare.py out/r72_side.png /tmp/fc.png   # photograph gate -- NAME THE FRAME
python3 gloss_compare.py out/r72_hero34f.png
python3 probe_rev70_tyre.py out/r72_side.png            # PASS IT A FRAME
python3 probe_rev46_vw.py                               # C4 is the only red row
python3 visibility_budget.py 3840 out/r72_hero34f.png   # PASS IT A .png
python3 revstats.py                                     # THE DRIFT DETECTOR -- run it at close
T1_SUB=2 /tmp/blender/blender -b -P audit.py            # rewrites STATE.md -- COMMIT FIRST
python3 audit_brief.py ; python3 audit_adversary.py     # rules 15/17, MECHANICAL half only
```

**FACTS THAT BITE:** `bootstrap.sh` fails 3/10 without `pip install pillow`. Every measurement
through `shader_solve._render` is 8-bit. **The render is NOT run-to-run deterministic** — floor at
1600×1100/96 spp is **2.441 % of pixels >8 levels, worst channel 40**; render the control twice
(rule 49). `lid_gen.py` and `script_gen.py` are **not** called by `build.py`. `audit.py` rewrites
`STATE.md` — commit first. **`ck` in `verify_clone.sh` collapses whitespace.** **A backgrounded
runner's `rc=$?` is the redirect's — and in a pipeline it is `tail`'s, which bit rev 71 once.**

**⚠ `probe_rev46_vw.py`'s C6 passes 6 = 6 — ON THE RASTER. On the RENDER the same function reads 3
against the photograph's 6 (F205).** Run the emblem gates on the FRAME.

---
## §6 THE RULES THAT WILL BITE YOU

Full canon (1–55) in `HANDOFF_CARRIERS.md` §5 and `NEXT_CONTEXT_PROMPT_rev50.md` §11.

1. **RENDER IT, CROP IT, AND LOOK AT IT** — before and after every change. **Rev 71's only reason
   for not shipping the bulb change was looking at it.**
3. **A control is finished when you have WATCHED IT FAIL on the defect.**
5. **NEVER PUT A FIGURE IN AN ACCEPTANCE TEST UNLESS YOU WATCHED IT PRINT.** **F247 is this rule
   failing inside rev 70's own fix — a recorded "watched failure" its own bar would have passed.**
6. **A guard that derives its threshold from the expression it checks is a tautology** — and so is a
   window that selects for the quantity it reports (F250).
8. **YOU MUST NOT PUBLISH A NUMBER FROM A MASK OR WINDOW YOU HAVE NOT PAINTED AND LOOKED AT.**
   **Rev 71 killed TWO of its own windows this way, one of them the same class rev 70 recorded.**
12. **Report the measurement WITH ITS CEILING.** *"It cannot be recovered from what we hold"* is a
    real result.
16. **YOU MUST NOT DELETE A CARRIER.**
18. **CITE STRINGS, NOT LINE NUMBERS — AND CITE THE FILE THE STRING IS IN** (F251).
38. **TWO SIDES OF A RATIO MUST SHARE A RULER** — including a comment and the row it describes (F247).
42. **A CONTROL'S KILL IS A PRECONDITION ON ITS PASS** — **and a control must be framed the way its
    measurement is framed. That is F246 and it is this revision's result.**
44. **WHEN A GUARD GOES RED ON YOUR OWN NEW WORK, THE GUARD WINS.**
55. **EVERY REVISION SHIPS A VISIBLE CHANGE TO THE VEHICLE, OR SAYS PLAINLY WHY IT COULD NOT.**
    **Rev 71 could not, and says so. Rev 72 must.**

---
## §7 WHERE EVERYTHING ELSE LIVES

| file | what it holds |
|---|---|
| **`HANDOFF_CARRIERS.md`** | every carrier: §0 goal + gate table, §0.1 the reference set, §2's seventeen refuted emblem routes, §4 the owner's rulings, §5 rules 34–55, §6 machine notes, §9 the horizon, §10 how to write the next handoff |
| `OPEN_FINDINGS.md` | **253 rows.** The register outranks prose. **F246–F253 are rev 71's** |
| `STATE.md` | machine-written; outranks every prose description |
| `LEDGER_rev71.md` | what rev 71 did, **and §4, what it got wrong in its own work** |
| `EMBLEM_HANDOFF.md` | the emblem's carrier — **its §3 is a STALE second copy of the refuted list** |

---
## §8 HOW TO CLOSE

**THE OWNER'S STANDARD, IN HIS WORDS:** photo-realistic parity with **that exact bus**. **Any single
measurement off is unacceptable** — per-measurement, not on average. **Never call it done off
self-review. Report the measurement with its ceiling, never a self-assigned score. Do not say
anything is ready** — say what is fixed, what is still wrong, and what you measured.

1. `./bootstrap.sh` and `./verify_clone.sh` both all-PASS on a **clean** tree.
2. `python3 revstats.py` — **put its geometry/closure line in the ledger header.** If the revision
   shipped nothing, **say so at the top, not in a footnote** (rev 71 did).
3. Regenerate `STATE.md` (`T1_SUB=2 … audit.py`) — **commit first**.
4. **DISPATCH an adversary at the brief you WROTE (rule 17), not only the one you received.**
   Rev 71's incoming adversary returned **13 defects and its top three changed the revision's plan.**
5. **Keep the split.** Action brief short; carriers in `HANDOFF_CARRIERS.md`; `cp` the brief over
   `PASTE_INTO_CLAUDE_CODE.txt` **in the same commit**.
