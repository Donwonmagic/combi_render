# NEXT CONTEXT PROMPT — rev 51

**Read this whole file before you touch anything.** Then `LEDGER_rev50.md`, then
`SURVEY_rev49_photoreal.md` §6 (still the work list), then `LEDGER_rev49.md` — **which carries three
figures the machine contradicts, annotated in place at rev 50.**

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
./bootstrap.sh          # ALL 10 PASS   -- row 10 is the branch check; believe it over any prose
./verify_clone.sh       # ALL 125 PASS  -- 125, not 122 and not 113.  Needs a CLEAN tree.
```

**THE BRANCH INSTRUCTION HAS NOW BEEN STALE FIVE REVISIONS RUNNING.** Rev 50's designated branch
measured **0 ahead / 0 behind** while the work sat **29 ahead** — and its remote copy had been
**deleted**, so `git fetch --prune` reported `- [deleted]`. HEAD was a strict ancestor; it
fast-forwarded and nothing was lost. **Work from whichever ref that measurement shows is furthest
ahead of `main` with nothing behind it, and believe `bootstrap.sh` row 10 over any sentence.**

**AND DO NOT EDIT SOURCE WHILE A RENDER QUEUE IS RUNNING.** Rev 50 did it twice. The first time it
aborted three baseline renders — and the harness printed `rc=0` for all three, because `rc=$?` came
after the redirect and reported `echo`'s status. **Freeze the tree for the duration of a baseline
queue, and make your runner report Blender's status, not the last command's.**

---

## §2. WHAT HE RULED AT REV 50 — THREE THINGS, AND ONE CLOSES A FIVE-REVISION ARGUMENT

| his words | consequence |
|---|---|
| **W6: "keep the studio rig as it ships"** | **W6 IS CLOSED.** `T1_SOFTEN` stays 1.0. **The body red's G/R gap against the photographed 0.223 ± 0.066 IS NO LONGER A DEFECT** — it is the accepted consequence of a chosen genre. Do not re-open it, do not ablate `T1_SPEC` against it, and **do not read a G/R shortfall on any surface as a paint error.** |
| **the roof strips: "Retire the number"** | The 0.3 m is gone from the record, and `LID_W` is now **derived** from ref_side.jpg's scale-free board aspect instead of typed. |
| **the wipers: "Remove all of it including the spindles"** | Withdrawn entire, commented not deleted. He **overruled** the survey, which proposed keeping the spindles. |

**This also effectively answers C1(a):** the studio is the deliverable and the street photographs are
**dimensional references, not colour targets**. Do not re-litigate the delivery genre without asking.

---

## §3. WHAT REV 50 FIXED

`LID_OPEN_DEG` 104 → **76** (the lid leaned *away* from the counter for six revisions; `sin 76 = sin
104` exactly, so no z dimension moved — confirmed by `STATE.md` coming back bit-identical). The props
re-footed on the show side, with rev 44b's tip fix kept. `LID_W` 1.1100 → **1.2237**, derived, bounded
by the roof's own half-width walked off the body (**≤ 1.2797 m**). The menu header's `'&'` **0.728 →
0.474** of the strip height. The tail lamps' **Ø33.2 mm disc of body red** at each lens centre. A
**live 17.5 mm** defect in `trunk_bay()` from a stale typed `ENGLID_GAP` z-pair. The cab door handle
**58 mm above the belt** → below it. The dead second `def gutter()`. The wipers.

---

## §4. WHAT REV 50 REFUTED — DO NOT REBUILD THESE

* **`SURVEY_rev49` finding 49, `LID_W` = 1.40–1.49 m.** The aperture starts at the hinge and the roof
  reaches only `Yt`, so **W ≤ 1.2797 m**, measured at run time. At 1.45 the hole would run **170 mm
  past the roof edge**, measured by an assert that walks `roof_z` (Yt = 0.7347 at the lid station).
  *(Rev 50 first published 178 mm from the record's Yt = 0.7273; quote the machine's own walk.)* There is now an assert that says so, watched failing.
* **§6 A3's material half, "the wear field clones".** Refuted from the source (`build.py:867` *asserts*
  every mesh carries an identity transform, so Object coords are world coords, and the wheels are
  2.400 m apart in a 143 mm field) **and** by measurement with the control the original never had
  (θ-high-passed polar residual: tyre annulus front-vs-rear **−0.007 / −0.022**, against a
  self-rotated control of 0.002 / 0.010). The 0.675–0.708 was measuring identical **geometry**.
  **The VW glyph is upright in both photographs — do not randomise it.**
* **§6 A18 as graded.** The contact shadow is **live on the direct path** (ratio 0.875) and gated out
  only on the `hero.py` strip path. The live half is survey #37: vignette 0.000, grain 0.0000, 57 % of
  the frame bit-exact white. Split them.
* **Survey finding 6, the tail board's foot.** Stale — fixed at rev 49d. Synthesis item A23 is
  **discharged**; there is no contradiction left. *But its guard's margin is pinned at exactly +4.0 mm
  by construction, so it is a construction-consistency check, not a free-running clearance measurement.*

---

## §5. THE WORK LIST FOR REV 51, IN ORDER

**A2 — THE HUBCAPS ARE FIVE-PETAL FLOWERS AND IT IS THE MOST VISIBLE DEFECT IN EVERY FRAME.**
Mechanism certain and reproduced three ways to 0.2 mm (crossover **r = 0.11973 m**; render m5
**0.051–0.060** on both wheels with every other harmonic ≤ 0.007, against `ref_side.jpg`'s 0.013–0.024
*not separated* from m2 at 0.176; controls: circle 0.0004, synthetic 5-petal 0.0805).
**IT IS BLOCKED ON ONE MEASUREMENT AND REV 50 DID NOT SHIP A GUESS.** Two mechanisms give the identical
image — the cap ~48 mm too far inboard, or the disc not dishing — and **neither depth is measured
anywhere.** Moving the cap the full 49.7 mm puts its apex **60.2 mm proud of the rim flange**, which the
photographs refute; dishing the disc cuts a **55 mm cliff** into a cream annulus they show smooth.
**What settles it:** how proud the dome stands, from an obliquely-seen wheel — `IMG_2073.jpeg` (green,
1400 px, geometry transfers) or `ref_playa_34.png`'s front wheel. Fit both outlines, take the ellipse
axis ratio for the obliquity, invert the cap-centre offset. **Calibrate on a synthetic at known h
first.** If it cannot be recovered, say so — that is a valid result and it turns A2 into a photograph
request. *(A rev-50 agent was dispatched to do exactly this and had not reported; re-issue it.)*

**A6 — THE CURVATURE EDGE-WEAR SPECKLE. The loudest CG tell in the frame, and it survives W6's
closure** because it is texture, not light. 22.4 % coverage where the same material renders 0.01 % on
the shell; the counter fascia at 19.1 % against the photograph's 0.66 %. Both Pointiness gates saturate
to 1.0 on un-subdivided meshes. `T1_CTAN_WEAR=0` already exists and has never been exercised.

**A7 — the rear serving aperture, the ONLY one his ruling leaves open, renders as a black cavity.**
573 mm of undressed box, on an internal control needing no photograph. **And a second hole nobody
named: `gal_end_a` spans y −0.500…+0.400 against an aperture of ±0.520, so 120 mm of the show side sees
past the end wall entirely.**

**A9 — the galley is ~106 mm too far aft**, and the offset is **NOT rigid**: it runs −0.0957…−0.1103 m
because rev 13's translation was per-bay and the retired map's implied bay width is 1.8 % out. **A
single additive constant leaves ±8 mm.** Re-derive each X from `BAYS` as the header already claims.
Separately: `gal_rail` is **165 mm too LONG** (the survey's headline mis-signs it) and 218 mm too far
forward; `gal_caddy_fill`'s X inset has the wrong sign.

**A11's SECTION** — measured at rev 50, not built. `ref_side.jpg` at 7× shows a chrome lever lying in a
dish **pressed into** the skin; the build has a 12 mm **proud** prism that renders as a white blob.

**A19 — both headlamps and both indicators are placed with ZERO rotation**, and `IND_X = 2.0960` is a
bare literal typed twice. Prerequisite for any W4 work.

**A14's other half** — both `lid_rail` objects are **zero-area** (`_rag_grid` called with `x0 == x1`).
The degeneracy is certain; **the rail's WIDTH is not measured anywhere**, so decide what it should be
before building it, or ask.

**A13, A16's rosettes, A12** — the isolated star is built below the burst where both red frames put it
above; every flank rosette is drawn at the diameter of its **gold core**; the built "Señor" does not
resolve as a word. **A12 is an OWNER RULING, not a DO-NOW**: `senor_trace.py:118-131` calls the remedy
*"inventing ink the photograph does not show"*, and its own ceiling admits the continuity was never
proved. Ask him.

**THE PROCESS ROWS, still open:** the open-findings register abandoned at rev 45 (21 rows); the
standing-instructions carrier deleted at rev 44, which took the **die-cut sticker** — named as the
project's *original deliverable* — with it; SPEC §0.2 publishing two rev-4 corrections that were later
refuted; rev 48's refuted "B stays open" still live in `build.py:936-938` and `t1_shell.py:1380-1383`.

---

## §6. THE ARTWORK STATES — THE TABLE IS STILL INCOMPLETE, AND REV 50 ONLY PARTLY FIXED IT

`ref_playa_34.png` = `IMG_3842.png` = `ref_source.jpeg` is **RED, CURRENT ARTWORK — a THIRD TARGET
FRAME.** I confirmed it by looking: scrollwork, rosettes and the Señor Tacombi script are all plainly
there. The rev-49 survey found this (finding 40) and **it never reached §4 of either brief.** It
matters: SPEC §8's colour locks derive from it, and `probe_rev46_reports.py:127` already takes an
artwork reading off it.

**AND THE COUNT MAY STILL BE WRONG.** A rev-50 audit claims the two GREEN frames are **two different
artwork states** — `ref_workshop.jpg` carrying the script only, `IMG_2073.jpeg` carrying script **plus**
scrollwork **plus** a Calidad burst — which would make it **four** states, not three. **I did not verify
that by looking, and it is not confirmed.** Do that before taking any decal reading off a green frame.

Nine distinct frames, five byte-identical duplicate pairs — **re-confirmed by md5 at rev 50**, exactly
as published.

---

## §7. WHAT ONLY HE CAN GIVE — HE HAS SAID NEITHER IS POSSIBLE NOW

Full text in `PHOTOS_WANTED_rev49.md`, **corrected at rev 50**.

1. **THE TAIL BOARD'S FOOTING.** Still the top item, but **its provenance was wrong and is struck**:
   SPEC §10.28's footing sentence belongs to the *detached* "La Santa" sign, not to this board (§6 of
   `LEDGER_rev50.md`). The request stands on the **parallax argument alone** — 33.5 px/m, identical at
   base and tip, so W ≤ 0.59 m with no lower bound — and it closes **two** unknowns, not three.
2. **THE DECAL, DARKER.** Unchanged. Five items, one frame, 60.8 % of the white lettering clipped.
3. **THE NOSE, SQUARE ON.** W4, six revisions.
4. **A RAKING-LIGHT FRAME OF THE REAR QUARTER** — louvre pressing depth, block length and station, and
   the V swage's section at the nose. One frame, four items.
5. **THE OFF SIDE — ANY FRAME AT ALL.**
6. **NEW: an obliquely-seen WHEEL, close.** It would settle A2's fix direction without a guess, and A2
   is the most visible defect in every frame.

---

## §8. THE RULES. Rev 50 added two, and earned both the hard way.

All 33 rev-49 rules stand. **Read `LEDGER_rev50.md` §8 before you build any instrument** — rev 50
caught four instrument defects and **all four were its own**, including two tautological guards written
in the same edits that cite rule 32, an acceptance figure typed without watching it print, and a
harness that reported `rc=0` for renders that had aborted.

> **34. A REQUIREMENT INHERITS ITS OBJECT EXACTLY AS A RETIREMENT DOES.** Rev 49 wrote rule 29 and
> broke it four lines later, in the mirror direction. Before relying on any *"the record requires X"*,
> check which object the sentence is about — and check that the cited line exists.

> **35. A GUARD WRITTEN AGAINST A POSE ENCODES THAT POSE.** Three guards here identify a part's foot or
> free edge by `min(y)`, which is only the foot while the part leans one way; two aborted correct
> builds this revision. Ask the geometry — a foot is the lowest point — never the pose.

---

## §9. THIS MACHINE

```
cores 4   RAM 15 GB   Blender 4.5.3 via pip install bpy   subagent concurrency 2
build  T1_SUB=1 ~20 s        T1_SUB=2 ~100 s        render 1600x1100 96 spp ~5-9 min PER VIEW
```

```bash
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
T1_PREVIEW=side T1_PFX=r51 T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
  /tmp/blender/blender -b -P build.py
T1_SUB=2 /tmp/blender/blender -b -P audit.py                 # rewrites STATE.md -- COMMIT FIRST
python3 lid_gen.py                                           # regenerates tex/lidmural.png
```

**`lid_gen.py` IS NOT CALLED BY `build.py`.** It is run by hand and its output is tracked and
checksummed. Change it and you must regenerate, or the render silently uses the old texture.

**ABLATIONS — every one exists to WATCH A GUARD FAIL:** `T1_LIDDEG=104`, `T1_BAYSTALE=1`,
`T1_LAMPSINK=1`, `T1_LIDASPECT=1.2`, `T1_HANDLEHI=1` (rev 50); `T1_BAREMAT=1`, `T1_TBFOOT=1`,
`T1_BAYPROUD=1`, `T1_NOTAILBOARD=1`, `T1_SOFTEN=k` (rev 49).

**`git rev-list --count origin/main..HEAD` before you start and again before you finish. And
`git diff --name-only HEAD...origin/main` — that is where his photographs arrive. Re-run it EVERY
session, not once.**
