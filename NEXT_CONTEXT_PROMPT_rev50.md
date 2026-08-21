# NEXT CONTEXT PROMPT — rev 50

**Read this whole file before you touch anything.** Everything you need to start is here; everything
you need to be *correct* is in `SPEC.md` (§10.123 is this revision's), `LEDGER_rev49.md`, and
`LEDGER_rev48.md`.

---

## §0. WHAT HE SAID, AND WHAT IS LEFT

| his words | state |
|---|---|
| "100% calidad off center" | **FIXED** rev 46, guarded, guard watched fail. |
| "the vw logo wrong" | **FIXED** rev 46. |
| "señor Tacombi still isn't clearer" | **BLUR FIXED** rev 47. **CONTRAST HALF STILL OPEN.** §5 |
| "It still does not read as two separate words" | **FIXED rev 47b**, magnitude RETRACTED rev 48. Blocked on §7 item 2. |
| "the nose of the car is too flat" | **CONFIRMED, NOT FIXED, SIX REVISIONS.** Still no photographed anchor. §6 |
| "we're going to need the trunk open like it's in service" | **SUPERSEDED BY HIS OWN RULING.** See below. |
| "the main bay that should be open is the upper one" | **REV 48 OVER-READ THIS.** §2 |
| **NEW rev 49** — *"Leave the lower bay shut, just have the back trunk window open for service"* | **RULING. BUILT.** §2 |
| **NEW rev 49** — *"That was referring to a different sign. This one is part of the vehicle."* | **RULING. THE TAIL BOARD IS BUILT.** §3 |
| **NEW rev 49** — W6: chose *"re-light to match your photographs"* | **ANSWERED — then the mechanism turned out not to exist as described. RE-ASK.** §5 |
| **NEW rev 49** — photographs: *"Neither is possible right now"* | **RECORDED. STOP ASKING.** §7 |

> **RULE 29 — NEW, rev 49. A RETIREMENT INHERITS THE OBJECT IT WAS MADE ABOUT, NOT THE STATION IT WAS
> SEEN AT.** `signboard()` was retired from a crop of the **"La Santa"** sign standing on the GROUND
> BEHIND the bus. Four revisions read that as *"the raised panel at the tail is retired"* and applied
> it to a **different object at the same station**. Rev 49 REFUSED a job on the strength of it, and
> **the owner had to correct it.**

> **RULE 30 — NEW, rev 49. A FIXTURE'S FOOT MUST BE CLEAR OF THE BODY IT STANDS ON, AND SOMETHING
> MUST CHECK IT.** Nothing did. The tail board's foot sat **120 mm inside the roof**; the trunk bay's
> lining sat **2.0 mm proud of the tail skin**. Both through `VERIFY: 0 fail, 0 warn`.

---

## §1. START HERE — AND DO NOT TRANSCRIBE A BRANCH NAME OR AN AHEAD-COUNT

```bash
cd /home/user/combi_render
./bootstrap.sh            # ALL 10 PASS
./verify_clone.sh         # ALL 113 PASS   <- 113, not 110.  Four rows added at rev 49.
```

### THE BRANCH INSTRUCTION HAS NOW BEEN STALE **FOUR** REVISIONS RUNNING

Rev 47's brief named a branch with an ahead-count of 5; the real count was 1. Rev 48's named one that
was **0 ahead / 1 behind**. Rev 49's designated branch was created at `origin/main` — **0 ahead** —
while the real work sat 15 ahead on another ref. **Working where rev 49 was placed would have
discarded the whole of rev 48.**

**So this file does not name a branch. It names a MEASUREMENT.**

```bash
git fetch --all --prune
git fetch --unshallow 2>/dev/null || true      # verify_clone fails on a shallow clone
for b in $(git branch -r | grep -v HEAD); do
  printf "%-52s ahead %-3s behind %s\n" "$b" \
    "$(git rev-list --count origin/main..$b)" "$(git rev-list --count $b..origin/main)"
done
git diff --name-only HEAD...origin/main        # <- HIS PHOTOGRAPHS ARRIVE HERE
```

**Work from whichever ref that measurement shows is furthest ahead of `main` with nothing behind it.**
At the time of writing that is `claude/combi-render-rev49-sq1pvc` — **but check, do not believe this
sentence.**

**AND THE MACHINE ALREADY CATCHES THIS.** `bootstrap.sh`'s row 10 reads *"no branch carries work HEAD
does not have"*. It fired correctly at rev 49 and confirmed the correction independently. **If that
row is green you are on the right ref; if it is red, believe it over any prose including this file.**

**If your HEAD is an ANCESTOR of the furthest-ahead ref, fast-forward — nothing is lost and nothing is
merged.** Rev 49 verified that with `git merge-base --is-ancestor` before moving.

---

## §2. WHAT REV 49 BUILT AND WHAT HIS RULINGS CHANGED

### 2a. THE LOWER BAY IS SHUT. ONLY THE REAR WINDOW IS OPEN.

> *"Leave the lower bay shut, just have the back trunk window open for service."*

**This refutes an INFERENCE rev 48 made and shipped.** Rev 48 asked him which of the two rear
apertures should be open and he chose **A, the rear window**. Rev 48 then reasoned *"he called the
upper one the MAIN bay, not the ONLY one"* and kept the lower lid open too. **A choice between two
things is not a licence to keep both.** Rule 6.

`TRUNK_OPEN_DEG = 0.0` means SHUT and the swing is **skipped, not run at zero** — `_swing_open()`
asserts the free edge travels, so a shut lid put through it would fire a guard on a correct pose.
The T-handle and the plate are **no longer carried and no longer join `SWUNG`**. Length **4.065**.

**DO NOT PROPOSE REOPENING IT, and do not ask him for a photograph of the open tail: with the lid
shut, nothing in that bay shows.**

### 2b. AND CLOSING IT EXPOSED A DEFECT INVISIBLE FOR A WHOLE REVISION

```
lid_trunk   x -1.8730 .. -1.8702      the shut lid's outer face, at X_TAIL
trunk_bay   x -1.8750 .. -1.4550      the lining's face, 2.0 mm AFT of it
```

`trunk_bay()` set its origin to `x_skin − 0.002 + BAY_DEPTH*0.5`; `solid_prism` extrudes ±depth/2, so
the aft face landed **2 mm PROUD of the tail skin — the sign of the inset was inverted.** With the lid
open, nothing stood in front of it. With it shut it won the depth test across a closed panel and the
tail rendered with a **dark charcoal rectangle where the red engine lid belongs.** Guarded, and
watched fail on `T1_BAYPROUD=1`.

### 2c. THE TRUNK BAY HAD SHIPPED WITH NO MATERIAL AT ALL

`A()` only **appends** to `ASSIGN`; the loop that consumes it is step 9 at `build.py:846`, **91 lines
above** step 8c's call — the only `A()` in the file that lands after its own consumer. The bay
rendered at Blender's default grey, **1.28× the body red**. Now **0.51×**. `VERIFY` was clean and the
log line printed `len(ASSIGN)` — **appends, not assignments** — so it asserted coverage. Guarded
against the cause, watched fail on `T1_BAREMAT=1`.

---

## §3. THE TAIL BOARD — BUILT, AND WHY REV 49'S REFUSAL WAS WRONG

Rev 49 **refused** the rev-49 brief's job 1 because the source records the owner retiring that panel.
**He corrected it: "That was referring to a different sign. This one is part of the vehicle."**

**There are TWO BOARDS in `ref_rear34.jpg`.**

| | what it is | where it stands |
|---|---|---|
| **"La Santa"** | cream, **red brush script**, red star | on the **GROUND, BEHIND** the bus. This is `signboard()`. Correctly retired. |
| **the tail board** | cream face, **red rim**, amber bulbs, 38° | **ON the vehicle**, at the drip rail at the tail |

**Three pieces of physical evidence, not inference:** the base sits on the drip rail to **1 px** of the
locked fit; its bulb string is **continuous with the drip-rail run** at a pitch indistinguishable from
the vehicle's own `BULB_PITCH`; and **a power cable descends from it into the body.**

**Measured** (every figure with its ceiling in SPEC §10.123.2): base 1.747 ± 0.027 m, tilt
**38.0 ± 2.3° FROM HORIZONTAL** (*say which datum* — from vertical it is 52.0°), chord 0.711 ± 0.028 m,
bulb pitch 28 ± 2 mm, one stay.

**THE FOOT IS SOLVED, AND REV 49's OWN DECLARED 80 mm IS WITHDRAWN.** It was never a conflict between
the photograph and the geometry — the board was at the **wrong station**. The rear roof corner falls
away fast, and exactly one station satisfies both the photographed base height and the roof's own skin:

```
photographed base height           1.747 +- 0.027
roof skin at the solved station    1.7497           ->  2.7 mm
tip lands at                       2.2001
measured tip                       2.184 +- 0.030   ->  16 mm, inside the band
```

The station is **derived from `T1_body`'s own vertices at run time**, not typed, so it follows the
shell. **And the guard rev 49 first wrote for this was a TAUTOLOGY** — `z0 − _crown ≡ +0.005` by
construction — which the photorealism survey caught. The replacement measures the **built board**
against the **built skin**, and caught a further 3.7 mm on its first run.

**STILL NOT MEASURED, and NOT MEASURABLE from anything we hold:** the **width across the vehicle**
(parallax bounds it at **W ≤ 0.59 m with NO lower bound**) and the **fore-aft depth plane** — the
solved station sits 128 mm aft of the near-flank silhouette read, and the stay lands at 72.1° against
a measured 77.5°. **That is ONE unmeasurable quantity showing up twice, not two defects**, and it
closes with §7 item 1.

---

## §4. THREE ARTWORK STATES, NOT TWO VEHICLES — AND FIVE DUPLICATE FILES

**RULE 26 AS WRITTEN IS NOT SUFFICIENT.** "Check which bus" passes a Nolita reading and it is *still* a
wrong-artwork measurement.

| class | frames | carries |
|---|---|---|
| **RED, CURRENT — THE TARGET** | `ref_side.jpg`, `ref_rear34.jpg` | scrollwork, Señor Tacombi script, Calidad burst |
| **RED, AN EARLIER STATE** | the four **Nolita** frames | **plain red flank, `TACOMBI.COM`, `267 ELIZABETH STREET`, a chalkboard. NO scrollwork, NO script, NO burst.** |
| **GREEN — geometry only** | `ref_workshop.jpg`, `IMG_2073.jpeg` | a different decal entirely (spike depth 0.044 vs 0.133/0.239) |

**AND FIVE FILES ARE BYTE-IDENTICAL DUPLICATES.** `IMG_3842.png` = `ref_playa_34.png`;
`IMG_2054` = `ref_nolita_flank`; `IMG_2053` = `ref_nolita_front34b`; `IMG_2060` = `ref_nolita_front34`;
`IMG_3840` = `ref_nolita_doorshut`. **NINE distinct vehicle frames, not fifteen** (see the correction below). Do not count a
duplicate as corroboration.

> **CORRECTED, rev 49e — IT IS NINE, NOT TEN.** The rev-49 discharge was itself incomplete. Checksums
> find byte-identical files; they cannot see a **resized** duplicate. `ref_source.jpeg` (246 × 197) and
> `ref_playa_34.png` (500 × 400) are **the same photograph** — normalised cross-correlation **0.9768**
> after resampling to a common size, which is the JPEG-artefact floor, not a coincidence. So the
> reference set is **NINE distinct vehicle frames**. *Ceiling: correlation on a 246 × 197 thumbnail
> cannot distinguish "the same frame" from "two frames one second apart on a tripod"; the reading is
> that they are the same IMAGE, and 0.9768 will not separate those two hypotheses.*
> **And it matters beyond counting:** SPEC §8's colour locks are derived from `ref_source.jpeg`, a
> 246 × 197 thumbnail the record calls retired. They can be re-derived on `ref_playa_34.png` at **4×
> the area**, today, with no new photograph.


---

## §5. W6 — THE TRADE DID NOT EXIST, THEN THE LEVER DIDN'T EITHER. **ASK HIM AGAIN.**

**He was asked for three revisions to choose between accurate paint and a clean white background.
THERE IS NO SUCH TRADE.** The background is a **compositor constant** laid under a keyed render and
renormalised to 252 DN in post. Measured, base vs `T1_CYCALB=0.30`: **max |difference| 0.000, 100.00 %
at 255.** No lighting change can reach it.

**And he retired the pure-white backdrop lock himself at rev 15** — SPEC §6 carries it struck through,
*"RETIRED, §10.69 — THE OWNER'S DECISION"*. Three revisions refused lighting changes citing it as live.

**THE SWEEP** — `probe_rev45_paint.py`, 4 controls incl. its kill, 0 FAILED every run:

| lever | P1 body red G/R | verdict |
|---|---|---|
| base | **0.455** (3.5 σ) | — |
| `T1_CYCALB` 0.76 → 0.30 | ~0.45 | **DEAD** |
| bigger softbox, **short axis** 3.5× | **0.452** | **DEAD** |
| `T1_SPEC = 0` | 0.347 | **rev 8 made this fix and REVERTED it** |
| both axes 3.5× (12× area) | 0.351 | works — but see below |
| photographed | 0.223 ± 0.066 | albedo already right (0.250) |

**Growing the source in the axis that sets the streak moves the red by 0.003.** So the both-axes gain
is **not softening** — it is the rig growing past the subject until it becomes an **enveloping dome**.
`T1_SOFTEN` does not tune the studio, it **replaces** it, and it costs 29 % of the cream's brightness.

**HE CHOSE "re-light to match your photographs" WITHOUT KNOWING THAT.** `T1_SOFTEN` defaults to **1.0**
and **nothing ships changed**. **Put it to him again with the k=1.0 and k=3.5 frames side by side and
the exposure cost stated** — that is a look decision and it is his.

---

## §6. WHAT IS STILL WRONG — WORK THIS LIST IN ORDER

*Written from a **19-agent coordinated survey** run at the owner's request at the close of rev 49:
twelve subsystem surveys → five adversarial refuters → a completeness critic → one ranked synthesis.
19 agents, 0 errors, ~5 h, 1632 tool calls, 600+ working crops. **78 findings: 15 blocking, 42 major,
21 minor.** The full output is **`SURVEY_rev49_photoreal.md` (464 KB, tracked)** — every finding with
its evidence, its ceiling and its own attempted self-refutation, plus 130+ **ALREADY RIGHT** items so
you do not re-litigate settled ground. **READ IT BEFORE STARTING ITEM 1.**

### THE HEADLINE, IN THE SYNTHESIS'S OWN WORDS

> **THE GEOMETRY IS NOW CLOSER THAN THE PRESENTATION.** The residual shape errors are mostly tens of
> millimetres on parts nobody looks at twice — but four things that have nothing to do with
> measurement are what make every shipped frame read as a render: **the vehicle barely darkens the
> ground it stands on**; **its largest surface delivers chalk where every photograph shows polished
> enamel**; **every duplicated part is a bit-identical clone at the same clock angle carrying the same
> dirt**; and **every specular surface has a white void and six rectangles to reflect.**

**AND TWO SHAPE DEFECTS ARE VISIBLE ACROSS THE ROOM, EACH ONE CONSTANT.**

**W4 AND W6 ARE NOT GOING TO CLOSE THIS REVISION AND THE BRIEF SHOULD STOP IMPLYING OTHERWISE.** A
homography test settles that **no camera at any focal length** can put `ref_workshop.jpg`'s roundel
(axis ratio 0.657) and headlamp aperture (0.92) on one plane — flat-plane best fit **13.24 px rms**
against a **0.22 px** control on the render. **W4 is real, quantified and CONFIRMED**; apportioning it
between panel crown, lamp splay and a proud aperture flange still needs §7 item 3.

---

### A. DO NOW — unblocked, measurable from frames we already hold

Ranked by `(visible impact 1-5) × (post-adversarial confidence) ÷ (effort: small 1, medium 2, large 4)`,
judged on the frames he actually looks at.

| # | item | sev | effort | the ONE measurement that settles it |
|---|---|---|---|---|
| **A1** | **`LID_OPEN_DEG = 104.0` tips the mural lid AWAY from the counter.** Free edge lands 87 mm outboard of the roof edge and 1.63 m from the counter; photographs give α = 61–78°, leaning 12–29° **over** it. Its own comment and SPEC §135 say the opposite. **Raised at `AUDIT_rev43:117` and unfixed for six revisions.** | blocking | small | the scale-free taper: the board's span shrinks **−5.3 ± 0.6 %** top-to-bottom in `ref_side.jpg` (4 windows, rms 0.41–1.69 px). Corroborated with no measurement at all — **the support rod passes IN FRONT of the painted face** in `ref_rear34.jpg` and `IMG_2073` |
| **A2** | **Every hubcap renders a FIVE-PETAL FLOWER, not a dome.** `rim()` scales the disc radially by 1.1538 and leaves its **axial** coordinates alone, so the disc stands proud of the cap from r = 0.120 m out: visible **Ø239 mm** against a built **Ø274 mm**, with the five vent holes the only places the cap still shows. **Found independently by two agents.** | blocking | small | m=5 angular harmonic of the hub radius profile: render **0.050–0.056** (m2,m3,m4,m6,m7 all ≤ 0.008) vs `ref_side.jpg` **0.012–0.022**. Controls: perfect circle **0.0000**, synthetic 5-petal **0.0399**. `CAP_R` is correct — **do not shrink the cap** |
| **A3** | **EVERY DUPLICATED PART IS A BIT-IDENTICAL CLONE.** All four wheels are placed with no rotation about the axle, and `WEATHER`/`MOTTLE` are fed **Object** coordinates, so the wear field clones too. Same class: both headlamps, both indicators, both tail lamps, both hinges, three bay seals, two lid struts. **No dimension owned this — the critic found it.** | blocking | small | front-vs-rear wheel high-pass correlation on `r49board_side.png`: **0.675** whole, **0.708** tyre annulus, **0.695** hubcap. Controls: front vs itself at +5 px **−0.012**; two plain flank patches **+0.000**. **Fix is two lines and `MOTTLE_OFS` already exists as a declared no-op at (0,0,0)** |
| **A4** | **THE VEHICLE REMOVES ALMOST NO LIGHT FROM THE FLOOR IT STANDS ON, and there is nothing under it to remove any.** `van_floor` is `FLOOR_W = 1.200` — **AUTHORED**, 550 mm narrower than the body — with no chassis, exhaust, axle beam or tank. `studio.py:429` sets the world to **0.05 to fight W6**, so a crevice is lit or black with no gradient; `t1_mats.py:903` uses **only the convex half of Pointiness**, so no shut line, drip rail, arch lip or badge junction carries grime. **`optics-6` has been open since REV 12.** | blocking | medium | the crop pair read as images. Numerically, verified windows: fidelity bar under-body mean **133.1**, p05 **42**, 32 % pure white; `r49s_hero34f` **162.5**, p05 **72**, 2.6 % pure white |
| **A5** | **The body's three finish constants have no derivation** — Coat Weight **0.02**, Coat Roughness **0.300** (10× out of family with every other coated material: `cream` 0.030, `bumpercream` 0.030), on the vehicle's **largest** surface, with `t1_mats.py:178` declaring "the body is diffuse-dominated". Delivered cream reads as unpolished chalk with no crown highlight. | major | small | crop pair, render cab roof vs `ref_rear34.jpg` same panel. **Must be A/B'd against W6's G/R in the same run — a clearcoat is exactly the achromatic-veil mechanism W6 blames** |
| **A6** | **The edge-wear system degenerates into an all-over grey speckle on every un-subdivided panel** — **22.4 %** coverage where the *same material* renders **0.01 %** on the shell, because Pointiness saturates to 1.0 on flat detail meshes and **both** gates saturate. Same mechanism gives the counter fascia a chip field at **19.1 %** of area against the photograph's **0.66 %**, and `countertan` still carries **WEAR 0.7** on a surface **the owner ruled CLEAN at rev 28**. | blocking | medium | analytic Monte-Carlo of the chip/core clamp chain predicts 25.4–26.1 %; measured 20.9 %. Downsampling to the photograph's 211.5 px/m leaves it unchanged, so it is **texture, not sharpness**. `T1_CTAN_WEAR=0` already exists |
| **A7** | **The rear serving aperture — the ONLY one his rev-49 ruling leaves open — renders as a black cavity.** `gal_end_a` stops at x = −1.300, leaving **573 mm** of undressed, unlit box to the tail skin. **CONFIRMED by the adversary, and worse than reported.** | blocking | medium | geometrically masked to the strip of true open interior (camera validated to 2 px on the 1963 plate): **median L 14.3, p2 1.5, min 0.0**, against the model's own side bays at **184.5** and **126.6** — **8.8× and 12.9× darker**, not 4.5× |
| **A8** | **The T-handle is mounted on the fixed body, not on the engine lid its docstring and SPEC §4 put it on** — 46.8 mm below `ENGLID_GAP`'s lower shut line, 49.5 mm below the lid panel's own lower edge; even the top of its escutcheon is 21.8 mm clear. **A photograph-free internal contradiction.** | major | small | pixels in `r49s_rear.png`: seam y 962.5, handle y 984 → 21.5 px = 46 mm at the plate's own 463.6 px/m |
| **A9** | **EVERY galley feature and counter-top prop is ~106 mm too far AFT** — the header documents a fraction-of-aperture conversion that **is not the one used**. Plus: three of six S-hooks hang in mid-air; `gal_caddy_fill`'s inset has the **wrong sign**; the condiment rank is **2 boxes where `ref_side.jpg` has 5**. | blocking | small | one additive constant on the X of `galley_dressing()`'s objects |
| **A10** | **The tail skin protrudes through both tail lamps** — a disc of body red at the exact centre of each lens — and the lamps sit **~46 mm too high**: the photograph puts the lens centre **below** the plate's centre, the model puts it **above**. A sign flip. | major | small | `small_lamp()`'s profile starts on the axis; `build.py:564` places it 4.0 mm **inside** the tail skin |
| **A11** | **The cab door handle is on the wrong side of the belt line** — a raised white lozenge **above** the two-tone break where both vehicles carry it below. `z = 1.330` typed twice, uncited, against `Z_BELT_AUTH = 1.2720`. | blocking | small | both reference vehicles, unambiguous by eye |
| **A12** | **W3's remaining half is TOPOLOGY, not contrast** — the built "Señor" does not resolve as a word at the identical measured ink bbox, and **the remedy is already written in `senor_trace.py`**. Four revisions have carried this as a contrast problem gated on W6. | blocking | large | held against the photograph at mask x 5..275, y −12..102 |
| **A13** | **The isolated star is built BELOW the burst from a blob that is not a star.** `cal_gen._stars()` cites "components at x 702..713, y 381..391"; that region of `ref_side.jpg` is **the door edge and the counter boxes**. Both red current frames put the star **above**, and ~2.4× larger. | major | small | threshold-stable in both admissible red frames |
| **A14** | **Both `lid_rail` objects are ZERO-AREA** — `_rag_grid` is called with `x0 == x1`, so the lid's proud perimeter rail **has never rendered**. And **`def gutter()` is defined twice**; the dead first copy still carries the drip-rail constant rev 16 retired. | major | small | read straight off the source |
| **A15** | **The wipers are a stock-part inference and three in-service frames of THIS bus show a bare spindle** — no arm, no blade — while they are among the most conspicuous objects on the face in every render. **Same evidence class as the over-rider bar he withdrew at rev 37.** → **C2** | major | small | `build.py:405`, warranted only by SPEC §4's "Stock 1963 T1" inventory line |
| **A16** | **Every flank rosette is drawn at the diameter of its GOLD CORE**, so the flowers are **half size**; and the **menu-board `&` ships 58 % too tall** because `lid_gen.py:742` rescales each word independently, discarding the cap height the same file states at line 184. | major | medium | measured on the shipped texture against figures the same files declare |
| **A17** | **The windscreen has no split** — both panes are built from one origin plane and one basis, `WS_N` with a hard-zero y component. It is **one flat screen with a 52 mm slot in it** where a T1 has two flat panes vee'd about the centre pillar. The vee **angle** needs B5; the **fact** does not. | major | medium | `t1_shell.py:12-18`, `:22-30`, read straight off the source |
| **A18** | **The delivered frames have NO CONTACT SHADOW AT ALL.** `hero.py:112` sets `T1_FX=0` for every strip and `studio.py:825` gates the **entire** contact-shadow subgraph on that flag; `post.py` has no shadow stage. **SPEC §10.116's work never reaches the images he receives.** And `bg_white_level`'s 24.87 **clips to 255**, annihilating the vignette (0.000) and grain (0.0000) **he chose at rev 15**. | blocking | small | 57 % of the shipped frame is bit-exact (255,255,255) |
| **A19** | **Both headlamps and both indicators are placed with ZERO ROTATION** — translation only, no `rot=` anywhere — so both axes are exactly parallel to the centreline. Wrong even against the model's **own** nose, whose normal at y = 0.545 is 1.2° off +X. And the headlamp **bore is cut at the LENS radius**, so the bore rim silhouettes rather than the bezel, whose widest ring sits 14 mm behind the skin. | major | small | `build.py:506`, `:520-521`; `t1_shell.py:466-475` vs `t1_detail.py:853-859` |

**Also do now, cheap and already diagnosed:** re-publish the **open-findings register** abandoned at
rev 45 (21 open rows, four revisions with no successor); restore the **"§7. INSTRUCTIONS OF MINE STILL
OUTSTANDING, IN NO OTHER CARRIER"** section **deleted at rev 44**, which carried fourteen standing
items in the owner's own voice; strike SPEC §0.2's two rev-4 corrections that were themselves later
refuted; and re-derive SPEC §8's colour locks — **they come off `ref_source.jpeg`, a 246 × 197
thumbnail that is the SAME PHOTOGRAPH as `ref_playa_34.png` at 4× the area.**

### B. BLOCKED ON A PHOTOGRAPH — he has said neither is possible now, so RECORD, do not queue

| | the frame | what it closes |
|---|---|---|
| **B1** | **A darker exposure of `ref_side.jpg`** | the whole decal cluster — word gap, spike count and character, star count, burst colour, "the lettering looks off". **5–7 items, one frame.** 60.8 % of the white lettering is clipped |
| **B2** | **A raking-light frame of the rear quarter** | louvre **pressing depth, block length AND block station** — three estimators were built and **all three failed their own controls** — and, same frame class at the nose, the **V swage's section** (6.2 mm / 16 mm, both invented). **Widen `PHOTOS_WANTED` item 4's scope** |
| **B3** | **One frame from beside the front corner at nose height, looking ACROSS the face** | apportions **W4** between panel crown, lamp splay and a proud aperture flange. **A head-on frame does NOT do it**: head-on, a 15° splay compresses the bezel by 3.4 %, which is 1 px |
| **B4** | **The open rear window's jamb** | its seal, hinge and stay — **the only aperture on the vehicle with none of the three** |
| **B5** | *(cheap, may need no photograph)* a bottom-rail trace on `ref_workshop.jpg` | the windscreen **vee angle** (A17's second half) |
| **B6** | **The tail board's FOOTING** | its **width** and **fore-aft depth plane** — one unmeasurable quantity showing up twice (§3) |

### C. BLOCKED ON AN OWNER RULING — put each as MULTIPLE CHOICE with a crop

**C1 — THE DELIVERY GENRE. THIS IS THE HIGHEST-VALUE QUESTION ON THE PAGE.** Every reference frame is
a 3–6 m phone snapshot; every delivered frame is a **78 mm lens at 15 m** on a white sweep. Far/near
depth ratio: `hero34f` **1.279**; `playa_ref` — the only camera this project ever recovered from a
photograph of this bus — **2.323**. **Forty-nine revisions of colour and level arguments have been
fought across that unacknowledged gap.** Options: (a) keep the studio as the deliverable and formally
close colour arguments across the gap; (b) make `playa_ref` the deliverable; (c) deliver both and
judge **fidelity** only on `playa_ref`, **presentation** only on the studio; (d) drop the heroes to
~7 m / 50 mm.

> **REV 49 RENDERED IT, AND THE RESULT IS THE STRONGEST W6 EVIDENCE THE PROJECT HAS —
> BUT IT IS NOT CONFIRMED, AND THE DIFFERENCE MATTERS.**
>
> ```
> body red G/R, normalised to the cream in the SAME frame
>   PLAYA (diffuse dome, real ground)   0.2736   ->  0.77 sigma
>   STUDIO (the shipped rig)            0.5081   ->  4.32 sigma
>   photographed target                 0.223 +- 0.066
>   the paint's own albedo              0.250
> ```
>
> **In the playa environment the red lands essentially on its own albedo.** Ceiling, stated: those
> are flat-patch windows on two different views and two different rigs, **not**
> `probe_rev45_paint.py`'s projected-and-raycast landmarks. The absolute numbers are NOT comparable to
> the published 0.455; the **direction and the order of the gap** are.
>
> **AND THE CALIBRATED PROBE COULD NOT CONFIRM IT.** `T1_SCENE=playa` + `probe_rev45_paint.py`
> returns:
>
> ```
> [FAIL] C1  cap 0, cream 0, red 0 candidates survived visibility
> P1=nan  P2=nan  P3=+nan        CONTROLS: 4 checked, 3 FAILED
> ```
>
> Every landmark is occluded from `hero34f`'s camera station once the environment exists — the C4
> kill sampled `[28, 33, 0]`, foliage. **The instrument does not transfer.** Rule 3: read its own
> summary line. **W6 IS NOT CLOSED. Do not report it as closed.**
>
> **THIS IS REV 50's CHEAPEST HIGH-VALUE TASK: adapt `probe_rev45_paint.py` to the playa camera** —
> project its landmarks through `playa_ref` rather than `hero34f`, or exclude the environment from the
> visibility raycast — and re-run. Four revisions of argument settle on one number.
>
> **WHICHEVER HE PICKS, THE FRAME IS IN `out/r49playa_playa_ref.png`.** `playa_env.py`
> is **1695 lines**, every mass placed by inverting that camera, **dormant since rev 10, referenced by
> NO verifier and NO dimension.** It is the only frame this project can compare pixel-registered
> against a photograph of its own subject; it **is** the diffuse-dome rig rev 49 concluded is W6's
> only surviving lever; and its ground is a **real lit surface**, so it closes `optics-6` and **A4**
> for free — no `T1_SHADOW` gain, no floor, no `T1_FX` gate.

**C2 — THE WIPERS.** (a) remove arms and blades, keep the spindles — what the photographs show;
(b) keep as built; (c) remove entirely.

**C3 — THE ROOF APERTURE'S SIDE STRIPS.** He settled *"roughly 0.3 m each side"*. The build gives
**0.162 / 0.182 m in plan** and **0.286 / 0.306 m as arc**; it passes only on the second reading, and
the re-expression happened **after** the first failed. (a) he meant arc — close it; (b) he meant plan
— the aperture is ~120 mm too wide each side; (c) retire the number from the verifier.

**C4 — WHAT THE GLASS AND CHROME SEE.** Ten panes, both mirrors, every bezel and the bumper reflect a
compositor fill at world 0.05. (a) add a reflection-only environment, invisible to camera; (b) leave
it; (c) solve it by choosing **C1(b)**.

### D. DECLARED AND HONEST — correctly labelled, NOT defects

`TB_WIDTH` and `TB_Y_CENTRE` (pose choices, guarded, parallax-bounded); `REAR_OPEN_DEG` (no frame
shows it); `LOUV_APERTURE` (INFERRED and says so); `LINE_GAP` (TRANSFERRED / ARTWORK CONFIRMED
DIFFERENT / MAGNITUDE UNVERIFIED); `STAR_N` (both red frames blown); the off-flank apertures (graded
**E**, explicitly not a correctness claim); the trunk bay's contents (deliberately not invented).

### WHAT THE ADVERSARY KILLED — do not chase these

* **"The rocker is not modelled."** **REFUTED.** `t1_core.section()` run B builds a bottom roll of
  radius `RB_ALL` = 0.122 m over the whole main run, and `audit.py` publishes **`rocker to ground
  0.3177`** into `STATE.md` every build. **Grepping for an object NAME is not a test for whether a
  feature is BUILT — a lofted feature has no name.** (Rule 31.)
* **"W4 has a photographed handle at last."** **NARROWED.** The observable stands and is now
  quantitative; it does **not** unblock the fix. It is W4's symptom made measurable, not its magnitude.
* **"The engine-lid outline is 65 mm too high."** **NARROWED** to A8, which is stronger: an internal
  contradiction needing no photograph.

---

## §7. WHAT ONLY HE CAN GIVE — AND HE HAS SAID NEITHER IS POSSIBLE NOW

Full text in `PHOTOS_WANTED_rev49.md`. **He answered at rev 49: "Neither is possible right now." STOP
ASKING** — record what each frame unblocks and work on what the frames we hold can settle.

1. **THE TAIL BOARD'S FOOTING — NEW, AND NOW THE TOP ITEM.** Closes the board's **width**, its
   **lateral position** and the **80 mm foot inconsistency** together. **`SPEC.md:937` §10.28 has
   demanded it since rev 12 and nobody ever asked him for it.**
2. **THE DECAL, DARKER — NOT CLOSER.** Five items. **Rev 49 tried to dissolve this request and failed
   its own calibration**: at `ref_side.jpg`'s exact resolution *and* 4:2:2 subsampling the estimator
   recovers a known gap to **2 % with a flat plateau**, and on the real frame it has **no plateau and
   lands 158 % off**. 60.8 % of the white lettering is clipped. **The photograph, not the method, is
   the binding constraint.**
3. **THE NOSE, SQUARE ON.** W4, six revisions.
4. **A RAKING-LIGHT FRAME OF THE LOUVRES** — the pressing depth.
5. **THE OFF SIDE — ANY FRAME AT ALL.** Every frame in the project is of the serving side.

**~~THE TAIL WITH THE ENGINE LID OPEN~~ — DROPPED.** It was item 1 for two revisions. He has ruled the
lid **shut**; with it shut, nothing in that bay shows.

---

## §8. THE THING THAT OUTRANKS EVERY ITEM ABOVE

**This project measures beautifully and its instruments keep being wrong.** Rev 46 caught five, rev 47
four, rev 48 four (three its own), **rev 49 four, and three were its own:**

* **A TAUTOLOGY PUBLISHED AS A MEASUREMENT.** Rev 49 reported that the decal's type separates from the
  burst on chroma, headlined *"of the 3007 burst pixels, ZERO have G ≥ 254"*. The mask
  `(R−G)/R > 0.22` forces `G < 198.9` **by construction**. Observed max: 198. **An algebraic identity
  about the threshold, presented as a fact about the photograph.**
* **A FOOT BURIED 120 mm INSIDE THE ROOF**, from typing a datum measured at a different station.
* **A MEASUREMENT APPLIED ACROSS DEPTH PLANES** (rule 16) — a near-flank reading used in a centreline
  build, where the source explicitly says the sign flips.
* **AND A SECOND MEASUREMENT REFUTED THE FIX**: re-seated, the stay's own triangle landed 144 mm aft
  of `X_TAIL`, in mid-air.

**AND THE RECORD WAS WRONG IN PLACES NOBODY CHECKS.** `cal_gen.py:385` still said *"the model has NO
REAR VENTS"* — **rule 1's own founding case** — two revisions after rev 48 cut real apertures.
`verify.py` called the 3.0 m bbox top *"the raised signboard"* in two places; it is `lid_main`, and
`signboard()` has been gated off since **rev 12**. SPEC §10.26's table still published *"trunk lid |
OPEN, at the tail"*. All four landed in the source at rev 49.

> **A RETRACTION THAT LANDS IN A LEDGER AND NOT IN THE SOURCE IS HALF A RETRACTION.**

---

## §9. THIS MACHINE

```
cores 4   RAM 15 GB   Blender 4.5.3 via pip install bpy
build  T1_SUB=1  ~20 s        build  T1_SUB=2  ~100 s
cal_gen ~45 s                 render 1600x1100 96 spp  ~5-9 min PER VIEW
```

```bash
/tmp/blender/blender -b -P build.py                          # T1_SUB defaults to 2
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
T1_PREVIEW=side T1_PFX=r50 T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
  /tmp/blender/blender -b -P build.py
```

**`out/` IS NOT TRACKED AND STARTS EMPTY ON A CLONE.** `probe_rev48_louv.py` hard-defaults to
`out/r48b_side.png`; with `out/` empty a bare run prints MISSING and **emits no summary line at all** —
easy to mistake for a pass. **Render before quoting any probe that reads a frame.**

**14 views, and `hero` IS one of them** — `hero34f`, **`hero`** (`studio.py:1268`), `hero34r`,
`front34`, `side`, `front`, `rear`, `detail_f`, `low34`, `topdown`, `playa`, `playa_ref`, `playa_w`,
`counter`. *Three consecutive briefs said "there is no view called `hero`".*

### ABLATION SWITCHES ADDED AT REV 49 — every one exists to WATCH A GUARD FAIL

| var | reproduces |
|---|---|
| `T1_BAREMAT=1` | the trunk bay with no material |
| `T1_TBFOOT=1` | the tail board's foot buried in the roof |
| `T1_BAYPROUD=1` | the bay lining 2 mm proud of the tail skin |
| `T1_SOFTEN=k` | the rig-replacement lighting sweep (default 1.0 = rev-48 rig exactly) |
| `T1_NOTAILBOARD=1` | stands the tail board down |

### SHELL TRAPS THAT HAVE COST REAL TIME

* **`pgrep -f "blender -b -P build.py"` MATCHES ITS OWN SHELL.** Wait on a **PID**
  (`while [ -d /proc/$P ]`), never on a pattern.
* **`read -t N </dev/null` RETURNS INSTANTLY** — rev 49 built a wait loop out of it that reported
  "waited 480 s" after waiting zero. If you need to wait, `python3 -c "import time;time.sleep(n)"`.
* **`T.solid_prism` EXTRUDES CENTRED ON ITS ORIGIN**, not forward from it — and **advancing the origin
  does not protect the inset's SIGN**, which is how rev 48's 2 mm defect shipped.
* **`verify_clone.sh` REQUIRES A CLEAN TREE.** It reports `modified tracked files` and stops. Commit
  first, then verify.

---

## §10. HOW TO USE YOUR PARALLELISM

> **DO NOT FAN OUT BLENDER.** Cycles already uses all four cores. Check
> `ps -eo pcpu,args --sort=-pcpu | head` before launching. **Run renders SEQUENTIALLY from one script
> and analyse in the foreground while they go.**

**Subagent concurrency on this box is capped at 2** (`min(16, cores−2)`). A 19-agent workflow runs in
about ten rounds. Plan for that: prefer **fewer, deeper** agents over many shallow ones, and use
`pipeline()` so verification starts as soon as each survey finishes rather than at a barrier.

**Fan out everything that is NOT a render**, and **instruct verifiers to REFUTE**. Rev 49 ran four
agents plus a 19-agent survey; **three of the four changed its conclusions**, and one of them **killed
its author's own headline finding.** That is what they are for.

**AND FINISH WHAT YOU DISPATCH.** Rev 46 closed with one outstanding and it cost a whole revision.
**Rev 49 dispatched five efforts and all five reported before its ledger was written.**

---

## §11. THE RULES. EVERY ONE WAS EARNED BY A DEFECT.

1. **A claim in prose is not a guard** — and **a claim in a SOURCE COMMENT is not a measurement.**
2. **A constant tuned against another must be EXPRESSED in terms of it — and DERIVED AT RUN TIME.**
3. **Read each probe's own summary line, never its exit code.**
4. **Never put a figure in an acceptance test unless you watched it print.**
5. **Do not inherit a guard's rationale along with its shape.**
6. **An ordinal fact licenses a SIGN, never a SHAPE.** *(Fired again at rev 49: "the MAIN bay" was
   read as a licence to keep both bays open.)*
7. **A leading question is not evidence, even when the answer is yes.**
8. **A measurement's window is part of the measurement.**
9. **A threshold trace is only valid if the feature's FAR SIDE is resolved.**
10. **A detail you cannot see is not a detail — and a detail you looked at badly is not looked at.**
11. **When a fix cannot be built at any tolerance, suspect the thing it is fixing.**
12. **Add the guard in the same edit as the change.**
13. **Inventory the frames you already hold before asking him for a new one.** *(Discharged properly
    for the first time at rev 49: TEN frames, not fifteen.)*
14. **Prefer dimensionless measurements.**
15. **Retract in the same revision you find the error** — in SPEC, **in the source**, and to him.
16. **A PART MEASURED IN ISOLATION FROM WHAT IT IS FITTED TO IS NOT MEASURED** — including from the
    DEPTH PLANE it was read in. *(Fired at rev 49, twice.)*
17. **MEASURE THE MERGE STATE; NEVER TRANSCRIBE IT.** Stale four revisions running.
18. **A CONTROL THAT IS RIGHT FOR THE WRONG REASON IS NOT A CONTROL.**
19. **A CONTROL IS NOT FINISHED WHEN IT PASSES. IT IS FINISHED WHEN YOU HAVE WATCHED IT FAIL ON THE
    DEFECT** — and **a guard that CRASHES reports nothing.**
20. **AN INSTRUMENT THAT HAS NEVER BEEN WRONG HAS NEVER BEEN TESTED.**
21. **HIS REPEAT IS A MEASUREMENT.**
22. **CALIBRATE AGAINST A KNOWN DISPLACEMENT, AT THE REAL DATA'S RESOLUTION.** *(This is what killed
    rev 49's decal finding — and it is the rule working exactly as intended.)*
23. **A HORIZONTAL OVER A HORIZONTAL AT THE SAME ROW NEEDS NO AXIS RATIO.**
24. **QUOTE THE RATIO, NOT THE READING — *founding case REFUTED at rev 48*.**
25. **CLEARANCE IS NOT LEGIBILITY.**
26. **A MEASUREMENT FROM THE WRONG VEHICLE IS NOT A MEASUREMENT** — **and rev 49 sharpened it: there
    are THREE ARTWORK STATES, not two vehicles. Check which STATE, not just which bus.**
27. **A CAP NOBODY LOGS READS AS COVERAGE** — **and rev 49 inverted it: A COUNT THAT LOGS THE WRONG
    QUANTITY READS AS COVERAGE TOO.** `len(ASSIGN)` counts appends, not assignments.
28. **RENDER IT, CROP IT, AND LOOK AT IT.** **Every headline finding at rev 46, 47, 48 and 49 came
    from looking at an image.**
29. **NEW, rev 49 — A RETIREMENT INHERITS THE OBJECT IT WAS MADE ABOUT, NOT THE STATION IT WAS SEEN
    AT.**
30. **NEW, rev 49 — A FIXTURE'S FOOT MUST BE CLEAR OF THE BODY IT STANDS ON, AND SOMETHING MUST CHECK
    IT.**
31. **NEW, rev 49 — GREPPING FOR AN OBJECT NAME IS NOT A TEST FOR WHETHER A FEATURE IS BUILT.**
    Lofted and swept features have no object name. The survey reported "the rocker is not modelled"
    on a `grep` for `name="rocker"`, and rev 49 reproduced the error before the adversary killed it:
    `t1_core.section()` builds it as a bottom roll inside the loft, and **`audit.py` publishes
    `rocker to ground 0.3177` into `STATE.md` on every build.** Ask the mesh, or ask `STATE.md`.
32. **NEW, rev 49 — A GUARD THAT DERIVES ITS THRESHOLD FROM THE SAME EXPRESSION IT CHECKS IS A
    TAUTOLOGY.** `z0 = f(x) + 0.005` guarded by `z0 < f(x)` cannot fire. It passed as "watched fail"
    only because an escape hatch substituted a different `z0` — **it was testing the hatch, not the
    construction.** A guard must compare two INDEPENDENTLY OBTAINED quantities: the built thing
    against the built thing it is fitted to.
33. **NEW, rev 49 — A CONTROL THAT READS A STALE BASELINE IS NOT A CONTROL.** `verify_clone`'s
    "guard figures, read from the machine-written `STATE.md`" block was checking the current build
    against a **rev-45** baseline written from a tree recorded as **DIRTY** — and passing. Four
    revisions. **Regenerate `STATE.md` before trusting any row that reads it.**

---

## §12. THE STATE OF THE MACHINE AT HANDOFF

```
bootstrap.sh      ALL 10 PASS
verify_clone.sh   ALL 122 PASS  (110 at rev 49's pickup; 13 added, 1 re-based, 1 relabelled,
                  NONE relaxed).  STATE.md REGENERATED at rev 49e -- it had not been
                  written since rev 45, from a tree it recorded as DIRTY.
build             T1_SUB=1  VERIFY: 0 fail, 0 warn
                  length 4.065 vs spec 4.055     231 mesh objects, 0 bare materials
probes            probe_rev45_paint   4 checked, 0 FAILED   (P1 0.455 reproduced exactly)
                  probe_rev47_gap     3 checked, 0 FAILED
                  probe_rev47_sharp   9 checked, 0 FAILED
                  probe_rev48_louv    NEEDS out/r48b_side.png -- RENDER IT FIRST
                  probe_rev46_reports PARTLY RETRACTED -- do not quote
renders           out/ is NOT TRACKED and starts EMPTY.  Re-render before any frame-reading probe.
NO DISPATCHED TASK IS OUTSTANDING.  Five efforts ran; five reported; three changed
the conclusions and one killed its author's own headline finding.
```

**`git rev-list --count origin/main..HEAD` before you start and again before you finish. And
`git diff --name-only HEAD...origin/main` — that is where his photographs arrive.**
