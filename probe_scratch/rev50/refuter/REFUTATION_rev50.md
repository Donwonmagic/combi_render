# REFUTATION — rev 50

*Written by the rev-50 brief refuter. Nothing tracked was modified; nothing was committed; no
Blender was run. Every claim below carries a command, a `file:line`, or a described image.
`out/` is EMPTY (`ls out` → nothing), so no figure quoted off a render was reproducible and every
such figure is marked UNVERIFIABLE rather than confirmed.*

Two documents are graded here: **P** = `probe_scratch/rev50/BRIEF_rev50_verbatim.md` (the operator's
prose), **N** = `NEXT_CONTEXT_PROMPT_rev50.md` (the carried-forward brief, rev 49's authorship).

---

## 1. VERDICT TABLE

| # | claim | source | status | the machine's actual value |
|---|---|---|---|---|
| 1 | `./verify_clone.sh` ends **ALL 113 PASS** — "113 now, not 110" | P §1; N §1 L38-39 | **WRONG** | `ALL 122 PASS`, exit 0. N's own §12 says 122. |
| 2 | `./bootstrap.sh` ends ALL 10 PASS, row 10 green | P §1; N §1 | **CONFIRMED** | `ALL 10 PASS`; row 10 "no branch carries work HEAD does not have" = ok |
| 3 | 122 is legitimate, not an uncounted addition | (my task) | **CONFIRMED** | 110 → 122 = +12. `git diff 40dd87e HEAD -- verify_clone.sh`: **15 `ck` added, 3 removed**. Nothing hidden. |
| 4 | "13 added, 1 re-based, 1 relabelled, NONE relaxed" | N §12 | **WRONG (arithmetic + one relaxation)** | 110+13 = 123 ≠ 122; true net +12. And the `TRUNK_OPEN_DEG declares itself NOT MEASURED` row's grep window was widened `-A 3` → `-A 30`. |
| 5 | Five reference files are byte-identical duplicates of five others | P §3; N §4 | **CONFIRMED** | all five pairs verified by md5, names exactly as published |
| 6 | "NINE distinct frames, not fifteen" | P §3; N §4 | **CONFIRMED (qualified)** | 16 reference image files; 15 vehicle frames (16th is `bus_model_ref.JPG`); −5 byte-dupes = 10; `ref_source.jpeg` ≡ `ref_playa_34.png` → **9**. My NCC 0.9858 (record: 0.9768); controls 0.12/0.17/−0.03. |
| 7 | Rule 13 discharged: "TEN frames, not fifteen" | N §11 rule 13 | **WRONG / STALE** | §4 of the same file corrects it to NINE; rule 13 was not updated |
| 8 | Rev 47's brief named ahead-count 5; real 1 | P §1; N §1 | **CONFIRMED** | `LEDGER_rev47.md:29-36` |
| 9 | Rev 48's named branch 0 ahead / 1 BEHIND | P §1; N §1 | **CONFIRMED** | `LEDGER_rev48.md:29`; `origin/claude/combi-render-rev46-t8vhpm` measures **0 ahead / 1 behind** right now |
| 10 | Rev 49's designated branch 0 ahead while real work sat 15 ahead | P §1; N §1 | **CONFIRMED** | `LEDGER_rev49.md:48-50`; `origin/claude/combi-render-rev48-ypkd3o` measures **15 ahead / 0 behind** right now |
| 11 | Rev 50's branch was 0/0 while work sat 29 ahead | (my task) | **CONFIRMED** | reflog: `claude/combi-render-setup-dkgwme` created at `1c89e9f` (= `origin/main`) 18:04:02, fast-forwarded to `868c72d` 18:05:31. Now 29 ahead / 0 behind. |
| 12 | "The branch instruction has been stale **FOUR** revisions running" | P §1; N §1 | **UNDERSTATED** | with rev 50 it is **FIVE** |
| 13 | Survey: 19 agents = 12 surveys + 5 refuters + 1 critic + 1 synthesis | P §6; N §6 | **CONFIRMED** | 12+5+1+1 = 19, header of `SURVEY_rev49_photoreal.md` |
| 14 | 78 findings, 15 blocking | P §6; N §6 | **CONFIRMED** | exactly 78 `### N. [SEV]` headers numbered 1–78; **15 BLOCKING, 42 MAJOR, 21 MINOR** |
| 15 | "130+ ALREADY RIGHT items" | P §6; N §6 | **CONFIRMED as a count** | 133 bullets in the ALREADY-RIGHT block (L793–952) across 12 sub-headers |
| 16 | ...*"so you do not re-litigate settled ground"* | P §6; N §6 | **MISLEADING** | the survey's own critic disputes **7** of them as "asserted, not checked" (§2.1–2.7) and **refutes one outright** (§2.3). Neither brief says so. |
| 17 | "~5 h, 1632 tool calls, 600+ working crops" | N §6; `LEDGER_rev49:411` | **PARTLY UNVERIFIABLE** | tree holds **526** `rev50_*.png` (592 `rev50_*` files incl. 65 `.py`). No tool-call log exists. |
| 18 | Red CURRENT artwork = `ref_side`, `ref_rear34` | P §3; N §4 | **INCOMPLETE — WRONG** | `ref_playa_34.png` (= `ref_source.jpeg` = `IMG_3842.png`) is the **9th distinct frame** and is RED CURRENT. It is in **no class** in either table. |
| 19 | GREEN = `ref_workshop`, `IMG_2073`, geometry only | P §3; N §4 | **CONFIRMED as vehicles; the STATE count is wrong** | both are green ✓, but they are **two different artwork states** (see §2.6). "THREE artwork states" undercounts. |
| 20 | Four "nolita" frames: plain red, TACOMBI.COM, no scrollwork/script/burst | P §3; N §4 | **CONFIRMED by looking at all four** | see §2.5 |
| 21 | `bus_model_ref.JPG` is a SCHOOL BUS, not this vehicle | P closing | **CONFIRMED** | yellow US school bus, CG render on white, with a graded contact shadow |
| 22 | "the SAME RED BUS in an earlier state" | P §3 | **UNVERIFIABLE** | Nolita = 267 Elizabeth St, New York; target = Playa del Carmen. Nothing in the tree establishes one vehicle, or which is earlier. |
| 23 | W6: the white background difference "was 0.000" | P closing; N §5 | **CONFIRMED AS PUBLISHED, OVER-GENERALISED** | `LEDGER_rev49:169`, `SPEC §10.123.5`. One arm only, and structurally near-guaranteed. `studio.py:826-829` records earlier shadow attempts that **did** leak onto the backdrop. |
| 24 | "growing the source in the axis that matters moves the red by 0.003" | P closing | **NUMBER CONFIRMED, PHRASE INVERTED** | 0.455 → 0.452. The record calls it "the axis that *sets the streak*" and the point is that it does **not** matter. |
| 25 | The dome "costs 29 % of the brightness" | P closing; N §5 | **NUMBER FOUND, MATERIALLY INCOMPLETE** | `SPEC §10.123.5`: cream → **0.706** of base (−29.4 %) **and the red flank → 0.545** (−45.5 %). The brief omits the larger half. The figure appears nowhere in `LEDGER_rev49.md`. |
| 26 | "I had already retired the pure-white backdrop lock myself at rev 15" | P closing; N §5 | **CONFIRMED, retraction only half-landed** | `SPEC.md:324` struck through, "RETIRED, §10.69 — THE OWNER'S DECISION, rev 15 (§10.32)"; §10.32 at `SPEC.md:1674`. But `SPEC.md:1029, :1459, :9140, :9704` still assert the lock as live and use it to refuse the A4/A18 fix. |
| 27 | The top wanted photo changed to the tail board's FOOTING | P closing; N §7 | **CONFIRMED** | `PHOTOS_WANTED_rev49.md:34` is item 1 |
| 28 | The open tail "was item 1 for two revisions" | N §7 | **CONFIRMED** | `PHOTOS_WANTED_rev48.md:9`; `NEXT_CONTEXT_PROMPT_rev49.md:218` |
| 29 | "SPEC 10.28 has required [the footing] since rev 12 and nobody ever asked me for it" | P closing; N §7.1; `PHOTOS_WANTED_rev49:52`; `SPEC.md:10242` | **WRONG — RULE 29 AGAIN** | §10.28's demand is about **the detached "La Santa" sign**, the object the owner retired. Citation `SPEC.md:937` points at a blank line; the sentence is at **`SPEC.md:1008-1009`**. See §2.1. |
| 30 | Rev 48 found its brief wrong seven times | P §4 | **CONFIRMED** | `LEDGER_rev48.md:22-38`, 7 rows |
| 31 | Rev 49 found its brief wrong ten times | P §4 | **CONFIRMED** | `LEDGER_rev49.md:35-46`, 10 rows |
| 32 | Rev 47 measured a decal off the green bus and applied it to the red one | P §3 | **CONFIRMED** | `LEDGER_rev48.md:274-283` |
| 33 | Rev 46 retracted two of its own numbers | P §4 | **SUBSTANTIALLY SUPPORTED, not exactly countable** | one formal RETRACTION (`LEDGER_rev46.md:60`), one refuted hypothesis (`:109`), one partly-retracted probe (`:280-286`) |
| 34 | Rev 48: trunk lid opened inwards through a clean VERIFY and 95 green checks | P closing | **CONFIRMED** | `LEDGER_rev48.md:152` "verify_clone ALL 95 PASS" |
| 35 | A1 `LID_OPEN_DEG = 104.0` tips the lid AWAY from the counter | N §6 A1 | **CONFIRMED FROM CONSTANTS ALONE** | see §3 |
| 36 | A2 `rim()` scales radially by 1.1538 and leaves axial alone | N §6 A2 | **CONFIRMED, arithmetically reproduced** | `RIM_R 0.2198 / 0.1905 = 1.153806`; crossover at r ≈ 0.120 m |
| 37 | A3 "Fix is two lines and `MOTTLE_OFS` already exists" | N §6 A3 | **REMEDY WRONG** | see §2.7 — a shared-material constant cannot decorrelate instances |
| 38 | A4 `FLOOR_W = 1.200`, world 0.05, convex-only Pointiness | N §6 A4 | **CONFIRMED, all three** | `t1_detail.py:1209`; `studio.py:429-430`; `t1_mats.py:903` → `:962` `_mr(PT, 0.520, 0.600, 0, 1, clamp=True)` |
| 39 | A5 "the body's three finish constants have **no derivation**" | N §6 A5 | **WRONG** | `t1_mats.py:1690-1693` states the derivation (rev 8, red 0.37 vs 0.82) |
| 40 | A7 `gal_end_a` stops at −1.300, leaving 573 mm | N §6 A7 | **CONFIRMED EXACTLY** | `t1_detail.py:3089` X0 = −1.3000, `:3101`; `t1_core.py:72` X_TAIL = −1.873 → 573 mm |
| 41 | A8 handle 46.8 mm below the shut line, escutcheon 21.8 mm clear | N §6 A8 | **CONFIRMED — and N is right where the SURVEY is wrong** | see §2.2 |
| 42 | A9 "one additive constant" fixes the galley cluster | N §6 A9 | **UNDER-SCOPED** | three separate survey findings bundled; the 106 mm rests on a ruling that, if overturned, **inverts** |
| 43 | A10 `build.py:564` places the lamp 4.0 mm inside the tail skin | N §6 A10 | **CONFIRMED** | `build.py:564` `loc=(T.X_TAIL + 0.0040, …)` |
| 44 | A11 `z = 1.330` typed twice vs `Z_BELT_AUTH = 1.2720` | N §6 A11 | **CONFIRMED** | `t1_detail.py:1865, :1870`; `t1_mats.py:144`. Photographs agree by eye. |
| 45 | A12 W3's remaining half is topology, "blocked on NOTHING" | N §6 A12 | **RE-SCOPE — it is an owner ruling** | see §3 |
| 46 | A14 both `lid_rail` zero-area; `def gutter()` twice | N §6 A14 | **CONFIRMED** | `t1_shell.py:2123` `((LID_X0, LID_X0), (LID_X1, LID_X1))`; `t1_detail.py:944` and `:1717` |
| 47 | A15 wipers, listed under "DO NOW — unblocked" | N §6 A15 | **CONTRADICTORY — it is C2** | the survey puts wipers only in C, BLOCKED ON AN OWNER RULING |
| 48 | A17 windscreen has no split; `WS_N` hard-zero y | N §6 A17 | **CONFIRMED** | `t1_shell.py:15`, `:22-30` |
| 49 | A18 "THE DELIVERED FRAMES HAVE NO CONTACT SHADOW AT ALL" | N §6 A18 | **WRONG — contradicted by its own source** | see §2.3 |
| 50 | A19 both lamps and indicators placed with zero rotation | N §6 A19 | **CONFIRMED** | `build.py:506`, `:520-521` — no `rot=` |
| 51 | "NO DISPATCHED TASK IS OUTSTANDING" | N §12 | **CONFIRMED** | `LEDGER_rev49.md:411+` records five efforts, five reports |
| 52 | `out/` is not tracked and starts empty | N §9, §12 | **CONFIRMED** | `out/` exists and is empty |

---

## 2. WRONG — each error in full

### 2.1 THE BIGGEST ONE: SPEC §10.28's footing demand belongs to the **retired** sign, not the tail board

**The claim** (P closing; N §7 item 1; `PHOTOS_WANTED_rev49.md:52`; `SPEC.md:10242-10243`;
`LEDGER_rev49.md` §11):

> "the TAIL BOARD'S FOOTING, which **SPEC 10.28 has required since rev 12** and which nobody has ever
> actually asked me for."

**The machine.** Two checks.

1. The citation is bad. `PHOTOS_WANTED_rev49.md:52` cites `SPEC.md:937`. `sed -n '937p' SPEC.md`
   returns a **blank line**. §10.28's heading is at `SPEC.md:959`; the quoted sentence is at
   `SPEC.md:1008-1009`.

2. The object is wrong. `grep -n footing SPEC.md` returns exactly two hits: `:1009` and `:10243`.
   Line 1009 sits inside this paragraph (`SPEC.md:1002-1009`):

   > **The detached sign.** Modelled since rev 8 as `lid_rear`, a second hinged lid over a second
   > opening `build.py` never cut; briefly re-modelled this revision as a roof-mounted signboard;
   > now emitting nothing. **It is not part of this vehicle.** … The owner has revised **this one
   > panel** three times; **if it is revisited, it needs a photograph that shows its footing, not
   > another inference.**

   §10.28's own answer table (`SPEC.md:965-970`) identifies that panel: row 3, *"what the cream
   lettered panel is — first 'a separate signboard, not a cut roof lid', then, unprompted:
   **'I was wrong, I think it is a detached sign'**."* That is the **"La Santa"** board —
   `signboard()` — the object `LEDGER_rev49.md` §8 and `N` §3 correctly separate from the tail board.

**So the demand was made about the object the owner retired.** RULE 29 has fired again, in the
mirror direction: rev 49 correctly refused to inherit a *retirement* from the wrong object, and then
inherited a *requirement* from that same wrong object, from the same paragraph. It is now in four
carriers and has been put to the owner in his own brief.

**Corrected statement.** *"The tail board's footing is the top-ranked wanted photograph. Its
warrant is `PHOTOS_WANTED_rev49.md` §1's own parallax argument — the board's plane contains the
lateral direction, so its width projects only through parallax at 33.5 px/m, identical at base and
tip, giving W ≤ 0.59 m with no lower bound. SPEC §10.28's footing demand is about the retired
'La Santa' detached sign and must not be cited for this board."*

**Ceiling.** I read §10.28 in full and grepped the whole of `SPEC.md` for "footing"; there is no
second §10.28 subsection. What I cannot see: whether some earlier SPEC revision numbered a
tail-board section 10.28 — the citation `SPEC.md:937` may be correct against a superseded file. That
would not change the object.

---

### 2.2 A8's numbers are right and the SURVEY's are wrong — and a source comment is stale by 17.5 mm

`N` §6 A8 says the T-handle is **46.8 mm** below `ENGLID_GAP`'s lower shut line and its escutcheon
top is **21.8 mm** clear. `SURVEY_rev49_photoreal.md` synthesis item 8 instead cites
*"`t1_shell.py:1528` records `ENGLID_GAP`'s z as 0.6025…1.1025; `t1_detail.py:2729` puts the handle
at 0.5732"* and then states **48 mm** — a delta that is not the difference of the two numbers it
cites (0.6025 − 0.5732 = **29.3 mm**).

I resolved it from the constants:

```
t1_shell.py:856-857   ENGLID_GAP = [(u, v + 0.8700) for (u,v) in T.rrect(0.9400, 0.5000, 0.055, 6)]
t1_core.py:545-546    rrect(w,h,r) -> "rounded rectangle outline CENTRED ON ORIGIN"
                      => v in [-0.25, +0.25]  =>  z in [0.6200, 1.1200]
t1_detail.py:2714     ENGLID_HANDLE_DROP = 1.274 * PLATE_OUTER_H
t1_detail.py:2729     z = PLATE_OUTER_CZ - ENGLID_HANDLE_DROP

PLATE_OUTER_H = 0.3300/1.9616 = 0.16823 ; PLATE_OUTER_CZ = 0.78754 ; DROP = 0.21433
handle z              = 0.57322
0.6200 - 0.57322      = 0.04678 m = 46.8 mm        <- N is exact
escutcheon top 0.59822 ; 0.6200 - 0.59822 = 21.8 mm <- N is exact
```

**The defect is `t1_shell.py:1528`**, which publishes *"ENGLID_GAP's z 0.6025..1.1025"* — **17.5 mm
below what the code computes**. It is a comment, not a measurement (rule 1), it is quoted in the
tail-board argument at `t1_shell.py:1524-1532`, and the survey read it as machine truth.

**Corrected statement.** *"`ENGLID_GAP` spans z 0.6200…1.1200, computed. The T-handle sits at
0.57322, i.e. 46.8 mm below the lower shut line, with the top of its escutcheon 21.8 mm clear.
`t1_shell.py:1528`'s '0.6025..1.1025' is stale by 17.5 mm and must be corrected or annotated."*

**Ceiling.** I evaluated `rrect` by reading it, not by importing it under Blender; and I have not
confirmed that `ENGLID_GAP`'s v-datum and the handle's z share a frame beyond both being the
un-dropped geometry frame. The 11 σ tail-board argument that also quotes 0.6025 is unaffected by
17.5 mm.

---

### 2.3 A18's headline is refuted by the survey it cites

`N` §6 A18: **"THE DELIVERED FRAMES HAVE NO CONTACT SHADOW AT ALL"**, graded **blocking**.

The survey's synthesis item 9 — the source of that row — grades it
**"major *(downgraded from blocking: it fires only when `hero.py` is used)*"** and states
**"Latent, not live — every frame now in `out/` is a direct render"**, with this evidence:

> *"ground band just outboard of the near front tyre **223.2** against open ground **255.0** =
> ratio **0.875**, bracketing SPEC 10.116.5's deepened target 0.8729 and nowhere near the
> undeepened 0.9756. So the gain **is live on the direct path** and gated off on the strip path."*

The survey's completeness critic lists exactly this as contradiction **C1**: *"Both are about the
shipped picture. **They cannot both be acted on.**"* `N` §6 A18 acted on one and asserted the
negation of the other, and re-promoted the severity without saying it had been downgraded.

**Two separate findings were merged.** The 57 % / vignette 0.000 / grain 0.0000 half is survey
finding **#37 [MAJOR]** — *"On the direct-render path the vignette delivers 0.000 and the grain
delivers 0.0000 — 57 % of the shipped frame is bit-exact (255,255,255)"* — and that half **is**
about the delivered frames and stands. Split them.

**And do not re-tune against 0.8729.** Survey §2.1: `studio.py:786` sets the target to
*"0.871 — THE WEAKEST PHOTOGRAPHED READING"* out of four (0.3049 / 0.7300 / 0.6950 / 0.8713, mean
0.6503) — I read that comment directly at `studio.py:780-786`. "It matches its declared target" is
a statement about SPEC, not about a photograph.

**Corrected statement.** *"`hero.py:112` forces `T1_FX=0` and `studio.py:762`/`:823` gate the whole
contact-shadow subgraph on it, so the **stitched** path drops the shadow — latent, since every
delivered frame is currently a direct render, on which the shadow measures 0.875. Separately, on
the direct path `bg_white_level`'s 24.87 clips to 255 and the vignette and grain the owner chose at
rev 15 deliver 0.000 / 0.0000."*

**Ceiling.** Both the 0.875 and the 57 % are read off frames that no longer exist in `out/`.
Neither is reproducible until `r49s_hero34f.png` is re-rendered.

---

### 2.4 `verify_clone.sh` is at 122, and the count's provenance is a stale mid-revision figure

```
$ ./verify_clone.sh 2>&1 | tail -3
  ALL 122 PASS.  Content matches the rev-42 measured baseline,
  which is still current at rev 44.
```

Where 113 came from, from git:

| commit | subject | `ck` invocations | printed rows |
|---|---|---|---|
| `40dd87e` | rev 48, last touch | 113 | **110** (`LEDGER_rev48.md:338`) |
| `5adf8e7` | rev 49c | 116 | **113** (`LEDGER_rev49.md:359`) |
| `7b12ca8` | rev 49e, HEAD | 125 | **122** (measured now) |

So **113 was rev 49's mid-revision figure**, published in `LEDGER_rev49.md` §10 and quoted by the
survey's §4. `N` §1 carries it as current and adds *"113, not 110. Four rows added at rev 49"*;
`N` §12, written later, carries the correct 122. **`N` contradicts itself, and `P` copied §1.**

**122 is legitimate.** `git diff 40dd87e HEAD -- verify_clone.sh` shows **15 `ck` lines added and 3
removed** (`build.py opens the trunk lid` → `separates`; `TRUNK_OPEN_DEG declares itself NOT
MEASURED` restated; `mesh objects 221` → `231`) — net **+12**, which is exactly 110 → 122. Nothing
was added without being counted.

Two caveats on `N` §12's wording:
* **"13 added"** does not balance: 110 + 13 = 123.
* **"NONE relaxed"** is not strictly true. One row's search window was widened tenfold:
  `grep -A 3 '^TRUNK_OPEN_DEG'` → `grep -A 30 '^TRUNK_OPEN_DEG'`. The diff documents why (the
  constant's comment block grew) and adds a compensating row, so this is disclosed, not laundered —
  but "NONE relaxed" should read "one window widened, with a compensating row".
* **13 of the 15 new rows are `grep -q` presence tests on source text.** They test that a comment
  exists, not that the bus is right. That is the class the survey's §4 says must be tagged
  `SELF-CONSISTENCY, NOT FIDELITY` and stop counting toward the headline.

---

### 2.5 The three-artwork-state table omits the ninth frame — which is a TARGET frame

Checksums, run now:

```
230a2a90…  IMG_3842.png        = ref_playa_34.png
a00c45b4…  IMG_2054.jpeg       = ref_nolita_flank.jpg
b8e7f7a4…  IMG_2053.jpeg       = ref_nolita_front34b.jpg
ed2c33b0…  IMG_2060.jpeg       = ref_nolita_front34.jpg
f1b6f98c…  IMG_3840.jpeg       = ref_nolita_doorshut.jpg
```

Plus the resized pair, re-measured independently: `ref_source.jpeg` (246×197) against
`ref_playa_34.png` (500×400) resampled to a common size, luma NCC = **0.9858**; controls against
`ref_side` 0.147, `ref_workshop` 0.168, `ref_nolita_front34` 0.117, `ref_rear34` −0.031,
`IMG_2073` −0.032. Same photograph.

Nine distinct vehicle frames. **The tables in `P` §3 and `N` §4 classify eight of them.**

I looked at the ninth. `ref_playa_34.png`: red bus, three-quarter front, **yellow-and-red folk
scrollwork on the flank and the nose**, **"Señor Tacombi" script**, a **red "100 % Calidad" burst**
on the cream upper aft, drip-rail bulbs, red hubcaps with the VW emblem. That is **RED, CURRENT
ARTWORK — the TARGET class**, alongside `ref_side.jpg` and `ref_rear34.jpg`.

This is already in the survey (`SURVEY_rev49_photoreal.md:404`): *"rev 49 §4's three-artwork-state
table classifies only 8 of its own 10 frames; `ref_playa_34.png` and `ref_source.jpeg` appear in NO
class, while `probe_rev46_reports.py:127` takes an ARTWORK measurement of the Calidad decal off
`ref_playa_34.png`."* **The correction did not land in `N` §4, and `P` §3 repeats the omission.**

It matters three ways: `SPEC §8`'s colour locks derive from `ref_source.jpeg`; `probe_rev46_reports`
takes an artwork reading off it (and `N` §12 says that probe is *"PARTLY RETRACTED — do not
quote"*); and `C1(b)` proposes making that very camera the deliverable. **A rule that exists to stop
wrong-artwork measurements does not classify the frame those measurements come from.**

**Corrected table:**

| class | frames |
|---|---|
| **RED, CURRENT — THE TARGET** | `ref_side.jpg`, `ref_rear34.jpg`, **`ref_playa_34.png` (= `ref_source.jpeg` = `IMG_3842.png`)** |
| **RED, EARLIER (Nolita)** | `ref_nolita_flank`, `ref_nolita_front34`, `ref_nolita_front34b`, `ref_nolita_doorshut` |
| **GREEN — geometry only** | `ref_workshop.jpg`, `IMG_2073.jpeg` — *and these are two different states* |
| **NOT THIS VEHICLE** | `bus_model_ref.JPG` — fidelity bar only |

The four Nolita frames were checked by eye and are **exactly as described**: plain red flank, no
scrollwork, no script, no burst; `TACOMBI.COM` on `ref_nolita_flank` and `ref_nolita_doorshut`;
`267 ELIZABETH STREET / NEW YORK` on both; chalkboards on `front34b` and `doorshut`.

---

### 2.6 "THREE ARTWORK STATES" undercounts — the green bus is in two states

Looked at both green frames.

* **`ref_workshop.jpg`** — green bus in a workshop, mid-build. Flank carries the **"Señor Tacombi"
  script only**: no floral scrollwork, no burst. The raised lid's underside is plain cream with
  pressed ribs and a plain orange bulb strip. The near headlamp aperture is a **bare bore, lamp
  removed**.
* **`IMG_2073.jpeg`** — green bus in service. Flank carries the script **plus white floral
  scrollwork with daisies**, **plus a red "100 % Calidad" burst** on the cream upper aft, **plus
  "TACOS" and "BREAKFAST SPECIAL"** lettering. The raised lid has a green scalloped rim and a
  patterned (damask) underside. Headlamp fitted.

The operating rule — *take geometry from green, never paint* — is unaffected and correct. But the
**count** is wrong, and rule 26's rev-49 sharpening ("there are THREE ARTWORK STATES, not two
vehicles") is stated as a fact about the set. There are **at least four** artwork states across two
vehicles. Anyone corroborating a decal reading "in both green frames" is corroborating across a
repaint.

**Corrected statement.** *"Four artwork states across two vehicles: RED CURRENT (3 frames), RED
NOLITA (4 frames), GREEN BARE-SCRIPT (`ref_workshop`), GREEN DRESSED (`IMG_2073`). Geometry
transfers; paint and artwork do not, including between the two green frames."*

**Ceiling.** Read by eye at full resolution. I did not establish that the two green frames are the
same physical vehicle either — only that both are green and their artwork differs.

---

### 2.7 A3's finding is sound; its stated remedy cannot work

`N` §6 A3: *"**Fix is two lines and `MOTTLE_OFS` already exists as a declared no-op at (0,0,0)**."*

The finding is confirmed: `build.py:345-360` places all four wheels with
`D.place(o, loc=(x, s * tr / 2, T.TIRE_R))` and no rotation about the axle; the −Y pair is mirrored
in y (`v.co.y = -v.co.y`), so **front-vs-rear on the same side are true clones**, which is what the
survey measured.

The remedy is wrong:

* `MOTTLE_OFS` is read once (`t1_mats.py:662`, env `T1_MOT_OFS`, default `"0,0,0"`) and applied as
  the **Location of a single Mapping node inside a material node tree** (`t1_mats.py:1424-1431`).
* `simple()` and `_gm()` **return an existing material by name** (`t1_mats.py:702-704`), so all four
  wheels share **one** `tyre` / `wheelcream` / `capred` datablock — and therefore one `MOTTLE_OFS`.
* The field is sampled in **Object** coordinates. Two objects with identical local geometry get
  identical Object coordinates regardless of where they sit in the world; a **constant** offset
  added to that space is the same constant for all of them. It cannot decorrelate instances.
* Rotating each wheel about its axle rotates the Object-space texture **with** the mesh, so it
  changes the geometric phase (vents, emblem) and leaves the wear field cloned.

Decorrelating the texture needs per-instance variation the file does not have: an
`Object Info → Random` input, per-object material copies, or a switch to Generated/world
coordinates. **Budget it as a real change, not two lines.**

**Ceiling.** Read off the node graph and the material factory; no Blender was run. If some call site
overrides the TexCoord node's `object` property per instance I would be wrong — `t1_mats.py:1423`
creates `mtc` with no object override and links `mtc.outputs["Object"]` directly.

---

### 2.8 A5's "no derivation" premise is false, and the fix walks back into rev 8

`t1_mats.py:1690-1693`, immediately above the constants:

> *"(rough .105, coat .75 @ .025) put a mirror clearcoat on the body, which in a white studio laid
> an achromatic white veil over the paint — **that, not the base colour, is why the red measured sat
> 0.37 against the reference's 0.82 and read salmon.** Chalky finish restores the chroma."*

The values 0.02 / 0.300 are a **reaction to a measurement**. That is not the same as being derived,
but "no derivation" as written invites someone to raise the coat weight — re-creating exactly the
mechanism W6 blames, in exactly the studio W6 is measured in, one row below `T1_SPEC = 0` which the
same table marks *"rev 8 made this fix and REVERTED it."*

And the survey **dropped its own stronger claim**: *"I started this as 'the render has no specular
highlight anywhere and the photographs plainly do' and I DROPPED that half"* — C\*/(L\*+16) by L\*
quintile falls −24 % in `ref_rear34.jpg` against −20 % in the render. **The lobe shape already
matches; only the level is off, and the level is W6.**

**Corrected statement.** *"The body's coat weight and coat roughness are un-ablatable literals,
10× out of family with `simple()`'s 0.030, on the vehicle's largest surface. This is an
**ablatability and internal-consistency** defect. Render one arm, record it, propose no value, and
do not ship a change before C1/W6 is answered."*

---

### 2.9 The pure-white lock's retraction only half-landed — and it is refusing this revision's top item

`SPEC.md:324` carries the retirement. Four other passages still assert the lock as **live**, and all
four use it to **refuse the exact fix A4 and A18 now need**:

* `SPEC.md:1029` — *"rendering the sweep as a real lit surface **does** put a shadow down (175.2
  mean / 161.2 min against 255) but … **sec.6 locks the backdrop to pure white**."*
* `SPEC.md:1459` — *"SPEC 6 locks the backdrop to pure white, so retiring that is the owner's call."*
* `SPEC.md:9140` — *"it brings back a 166-grey falloff with a hard horizon line, and **§6 locks the
  backdrop to pure white**."*
* `SPEC.md:9704` — *"`T1_CATCH=0` — refused again… **SPEC §6 locks the backdrop to pure white.**
  Refused, this time with both numbers."*

`N` §8 lists four half-retractions as landed at rev 49. **This is a fifth, it is four passages
deep, and it will refuse A4 a fifth time if it is not annotated first.** Note also what the owner
actually chose at rev 15: not "no white background", but the **headroom** arm,
`BACKDROP_PEAK = 252.0`, *with a designed vignette and grain* (`SPEC.md:324-329`) — the very things
A18/finding #37 says now deliver 0.000.

---

### 2.10 Two more retractions that landed in a ledger and not in the source

**(a) The withdrawn 80 mm is still load-bearing.** `t1_shell.py:1826-1830`:

> *"…that reading belongs to a base at the near-edge height, and **this board stands 80 mm clear on
> the roof (see `tail_board()`)**. Run at the measured ANGLE and stop where the rod MEETS THE ROOF…"*

`LEDGER_rev49.md:268` withdraws the 80 mm; `t1_shell.py:1620` says it "DISSOLVES". The annotation
landed at 1620 and **not** at 1828, where the figure is still used to justify the stay's landing.
The survey found this (`SURVEY:434`: *"The figure is 20× wrong, in the very file the rev-49d commit
says it swept"*) and it was not fixed.

**(b) `verify.py` still calls the trunk lid open.** `verify.py:706-707`:

```python
log("  length excludes opened lids: %.3f with them, %.3f without "
    "(the open trunk lid projects aft of X_TAIL)" % (hi.x - lo.x, L))
```

The owner ruled the lid **SHUT** at rev 49. That hard-coded string is printed into the
machine-written `STATE.md` on every build and is sitting there now. It is the same class as
`N` §8's *"`verify.py` called the 3.0 m bbox top 'the raised signboard'"* — same file, not caught.

---

### 2.11 `STATE.md` was regenerated from a DIRTY tree, and rule 33 was written in the same revision

`STATE.md` provenance block:

```
| generated    | 2026-08-21 08:53:39 UTC |
| git commit   | e19b46f  (rev 49e)      |
| working tree | **DIRTY** — this state is not committed |
```

`git log --oneline e19b46f..HEAD` = **5 commits**. So the file eight `verify_clone` rows read as
their acceptance baseline was written from an **uncommitted** tree, five commits ago.

`N` §11 **rule 33**, written at rev 49: *"A CONTROL THAT READS A STALE BASELINE IS NOT A CONTROL.
`verify_clone`'s 'guard figures, read from the machine-written STATE.md' block was checking the
current build against a **rev-45** baseline written from a tree recorded as **DIRTY** — and passing.
Four revisions. **Regenerate STATE.md before trusting any row that reads it.**"*

The regeneration commit `8ae40a8` is literally titled *"regenerate STATE.md — it was last written at
rev 45, from a DIRTY tree"*, and the file it produced records itself as DIRTY. `N` §12's
*"STATE.md REGENERATED at rev 49e"* is true and incomplete. **Regenerate it from a clean tree before
quoting any of the eight rows that read it.**

Two more things inside `STATE.md` that rev 50 must not blindly "fix":

* `| overall length (ex counter) | 4.5800 | 4.0550 | **+525.0 mm OUT** |` — a red row in the
  machine-written state file while `VERIFY: 0 fail, 0 warn` and `ALL 122 PASS`. Establish whether
  that row excludes the opened mural lid before touching anything.
* **Three published values for the same length.** `STATE.md`: *"4.311 with them, 4.065 without"*.
  `SPEC §10.123.4`: *"4.480 with them, 4.056 without (spec 4.055)"*. `N` §12 and `verify_clone`:
  4.065. Neither the "with" nor the "without" agrees between STATE and SPEC.

---

### 2.12 `LEDGER_rev49.md` §10 — on the required reading list — carries three figures the machine contradicts

| the ledger says | the machine says |
|---|---|
| `verify_clone.sh   ALL 113 PASS` | **122** |
| `171 objects` | **231** (`STATE.md`, and `verify_clone`'s own `mesh objects 231` row) |
| `branch … 19 ahead / 0 behind origin/main` | **29 ahead / 0 behind** |

`P` §2 instructs the next context to read `LEDGER_rev49.md` start to finish. It will pick up all
three. `LEDGER_rev49.md` §11 also repeats the §10.28 mis-attribution of §2.1.

---

### 2.13 Smaller falsifications

* **`N` §11 rule 13** still reads *"TEN frames, not fifteen"* against §4's own correction to NINE.
* **The survey contradicts itself on its own completeness**: the header says *"12 of 12 subsystem
  surveys returned"*; `SURVEY:574` says *"run the ten subsystem surveys that did not return"*. The
  header is the later statement; believe it.
* **`verify_clone.sh`'s trailer** still prints *"Content matches the rev-42 measured baseline, which
  is still current at rev 44"* at rev 50.
* **`P`'s "costs 29 % of the brightness"** drops the word *cream* and drops the red flank's −45.5 %.
  When this is put to the owner as a look decision, both numbers must be on the page.
* **`P`'s "growing the source in the axis that matters moves the red by 0.003"** reads as if the
  lever works. The record's phrase is *"the axis that sets the streak"*, and 0.003 is the evidence
  that it does **not**.
* **`P`'s "NOTHING done to the lights can dirty it"** is over-general. The 0.000 is one arm
  (`T1_CYCALB` 0.76→0.30) on a background that `composite_on_white()` lays as an unconditional
  `AlphaOver` of a literal constant — so it is close to structurally guaranteed for alpha-0 pixels
  and says nothing about matte edges, glass, or the shadow catcher. `studio.py:826-829`'s own
  comment: *"SUBTRACT THE CATCHER'S NOISE FLOOR FIRST, and this is the whole reason the first two
  attempts **leaked onto the backdrop**."* And `SPEC_rev41 §10.78` records a precedent in which
  `T1_CYCALB=0` was a **vacuous arm** because the cyclorama was not in the probe scene at all.

---

## 3. ITEMS TO REFUSE OR RE-SCOPE (from `N` §6)

**REFUSE as written**

* **A18** — the headline "no contact shadow at all" is refuted by its own source (§2.3). Split into
  (i) the latent strip-path gate, severity **major** as the survey graded it, and (ii) survey #37,
  the vignette/grain annihilation on the direct path, which is the live half. Do not re-tune against
  SPEC's 0.8729; that target is the weakest of four photographed readings by its own comment.
* **A12** — listed as **DO NOW, blocked on NOTHING**. It is an owner ruling. The remedy costs
  **IoU 0.913** against the measured mask, and `senor_trace.py:118-131`, quoted in the finding
  itself, says bridging the strokes *"would be inventing ink the photograph does not show."* The
  survey's own ceiling (`SURVEY:977`): *"finding 1 rests on the source's own declaration that its
  breaks are tarnish artefacts, not on my having proved the paint is continuous — I looked for that
  proof in the blue channel and did not get it."* Against a standard of *"any single measurement off
  is unacceptable"*, deliberately degrading a measured match is his call. Put it as multiple choice
  with the two crops. (It is also not in the survey's ranked A-list at all, and at `effort = large`
  it cannot rank at position 12 on the stated formula.)
* **A15 (wipers)** — listed under *"A. DO NOW — unblocked"* and then annotated *"→ C2"*. The survey
  places it **only** in C, blocked on an owner ruling. Removing a built assembly on an inference is
  the class the owner withdrew at rev 37. Ask; do not act.

**RE-SCOPE before building**

* **A3** — finding sound, remedy impossible as stated (§2.7). Not two lines.
* **A5** — "no derivation" is false (§2.8). Re-frame as ablatability; render one arm; ship no value
  before C1/W6.
* **A9** — three survey findings bundled into one "blocking, small" row, and the load-bearing half
  carries a rule-29 hazard the row does not mention: *"the ~106 mm frame error … depends entirely on
  rev 13's ruling that REF's X = (495.8 − u)/211.5 is 100 mm aft; **if that ruling is ever
  overturned, finding 1 inverts** and it is the APERTURES that are 105 mm forward of the fit-out."*
  Separately, the condiment rank (survey #31) *"must be re-converted, not pasted in"*. Verify which
  object the rev-13 ruling was about **first**.
* **A2** — the mechanism is arithmetically certain and I reproduced it from source alone. But the
  **fix direction is contested** and neither brief says so. Survey contradiction **C4**: WHEELS says
  *"the five rim vent holes are correctly NOT scaled by S … do not shrink or grow CAP_R"*; FIDELITY
  BAR says *"the five vent holes are the only places the cap still shows."* Raise the cap dome, or
  lower the disc face? Decide explicitly and record why.
* **A4 / A18 / C4** — before any of them, land the four annotations in §2.9, or the fix will be
  refused a fifth time on a lock the owner retired at rev 15.

**RESTORE — dropped from `N` §6 and they should not have been**

`N` §6.A carries 19 of the survey's 24 A-items and `N` §6.C carries 4 of its 5 C-questions. The five
dropped rows include:

* **Survey A23 — the tail-board foot contradiction, and it says "resolve this BEFORE touching it."**
  Critic contradiction **C2**: ROOF says the foot is buried 63–75 mm inside the roof crown; RECORD
  says the height chain closes at 2.7 mm; *"nobody states whether these measure the foot vertex or
  the chord's base station … rev 50 will otherwise either fix a non-defect or ignore a real one."*
  `N` §3 declares **"THE FOOT IS SOLVED"** without addressing it. Resolve it in one sentence first.
* **Survey A11 — the tyres have no contact patch**, four rigid circles touching at a point,
  *"standing the vehicle ~30 mm too high"* (major, small). Directly bears on A4 and on the fidelity
  bar, which shows a flattened patch and a graded pool.
* **Survey A22 — the contact shadow terminates in a hard ragged rim** (major, small, dimensionless
  measurement, and SPEC 10.116's C3 control structurally cannot see it). Bears on A18.
* **Survey A20** — the louvre cluster.
* **Survey C5** — *"are the serving bays glazed?"*, which the survey says to ask once and close.

**One headline to soften.** `N` §6: *"W4 is real, quantified and CONFIRMED."* What the homography
settles is **non-coplanarity** — 13.24 px rms against a 0.22 px control. The survey's critic **C6**:
*"a lamp whose axis is +X on a flat nose and a lamp whose axis is +X on a crowned nose both render
elliptical from a 3/4. **Crowning the nose without splaying the lamp axes will not fix it.**"*
`N` §6.B3 acknowledges the apportionment is open; the headline should say so too.

**Items I checked and found sound — build them.** A1 (see below), A2 (mechanism), A4, A6, A7, A8,
A10, A11, A14, A17, A19.

**A1, confirmed from constants alone, no render needed:**

```
t1_shell.py:1076-1078   LID_Y_HINGE = -0.5450   # off-side edge of the opening
                        LID_W       =  1.1100   # across, hinge -> free edge
                        LID_OPEN_DEG= 104.0     # "past vertical, leaning over the counter"
STATE.md                open serving apertures on +Y: 3          <- the counter is +Y

free-edge y = -0.545 + 1.110 * cos(theta):
   theta = 104 deg  ->  y = -0.8135     814 mm on the OFF side, AWAY from the counter
   theta =  78 deg  ->  y = -0.3142
   theta =  61 deg  ->  y = -0.0069
```

The source comment is false for the value it annotates. The photographed 61–78° band puts the free
edge at the centreline, not past it toward the counter — so the 26–43° error `N` states is the
*inclination* error, and it is right.

---

## 4. RETRACTIONS / DELIBERATE FAILURES / DO-NOT-TOUCH

**RETRACTED — do not re-derive, do not re-quote**

| what | where | status |
|---|---|---|
| the rev-46 photographed decal-centring target **(+0.0455, +0.0746)** | `LEDGER_rev46.md:60-73` | **WITHDRAWN.** The instrument returned ≈(−0.01, −0.04) for *every* truth value tried. The photographed target is "centred", visual, not numeric. |
| `probe_rev46_reports.py` — R1's photo target | `LEDGER_rev46:280`, `LEDGER_rev48:345`, `N` §12 | **PARTLY RETRACTED — DO NOT QUOTE.** Note it still reads an artwork measurement off `ref_playa_34.png` at `:127`. |
| `LEDGER_rev47`'s decal defects — three of four | `LEDGER_rev48.md:283-287` | **REFUTED — measured on the GREEN bus.** Spike depth 0.133/0.239 (red) vs 0.044 (green). |
| **RULE 24**'s founding case ("quote the ratio, the bias divides out") | `LEDGER_rev48.md:270-272`; `N` §11 rule 24 | **FOUNDING CASE REFUTED.** The rule may still be practice; this case does not support it. |
| `LEDGER_rev47 §203` "ref_playa_34 is the only frame … 23 × 39 px" | `LEDGER_rev48.md:287-289` | **REFUTED.** `ref_side.jpg` shows the burst at 100 × 74–78 px. |
| the rev-49 **"80 mm foot inconsistency"** | `LEDGER_rev49.md:91, :268`; `t1_shell.py:1620` | **WITHDRAWN — but still live at `t1_shell.py:1828` and load-bearing on the stay.** §2.10(a). |
| the rev-49 burst-chroma headline *"of the 3007 burst pixels, ZERO have G ≥ 254"* | `LEDGER_rev49.md` §6 | **WITHDRAWN — an algebraic identity about its own threshold.** Observed max G inside the mask: 198. |
| rev 49's first tail-board **foot guard** | `LEDGER_rev49` §6a; `N` §3, rule 32 | **WITHDRAWN — a tautology** (`z0 = f(x)+0.005` guarded by `z0 < f(x)`). Replaced. |
| `LEDGER_rev45`'s *"about half the excess is the specular response to the white cyclorama"* | `SPEC §10.123.5`; `LEDGER_rev49` §5 | **REFUTED.** |
| `H_ROOF = 1.960` as an accuracy target | `STATE.md` | **RETIRED rev 22, owner's call.** The +23 mm warn is gone because the test was withdrawn, not because the mesh moved. |
| SPEC §1.1's bay taper `0.507 / 0.516 / 0.526` | `STATE.md` | **RETIRED** — it was rev 13's 100 mm origin error. Bays are equal at 0.5155. |
| `ref_source.jpeg` | `SPEC §10.2` | **FORMALLY RETIRED yet load-bearing** (ledger finding 21). Now known to be the same photograph as `ref_playa_34.png` at 4× the area. |
| SPEC §6's **pure-white backdrop lock** | `SPEC.md:324` | **RETIRED rev 15, THE OWNER'S DECISION** — but still asserted live at `:1029, :1459, :9140, :9704`. §2.9. |
| the over-rider **bar and posts** | `STATE.md`; `build.py:400-402` | **WITHDRAWN BY THE OWNER, rev 37.** Calls are **commented, not deleted**, and the guards stay armed. `build.py:401`: *"DO NOT re-add it without his say-so."* |
| W5, the raised sign board | `PHOTOS_WANTED_rev49` | **DISSOLVED rev 48.** *"He should never have been asked."* |

**DELIBERATELY LEFT AS IT IS — do not "fix"**

* **`TRUNK_OPEN_DEG = 0.0` means SHUT and the swing is SKIPPED, not run at zero.** `_swing_open()`
  asserts the free edge travels, so putting a shut lid through it would fire a guard on a correct
  pose. **Do not propose reopening the lower bay** (`N` §2a; owner ruling, rev 49).
* **`LINE_GAP = 0.43` is kept deliberately** though it came off the green bus.
  `LEDGER_rev48.md:274-279`: inverting the curve gives 0.376, still the green bus's number; the red
  bus bounds it to 0.25–0.47 and no further. Recorded as **TRANSFERRED / ARTWORK CONFIRMED DIFFERENT
  / MAGNITUDE UNVERIFIED**, with two verifier rows requiring it to keep saying so.
* **The off-flank apertures — 804.9 mm, graded E, explicitly NOT a correctness claim** (`STATE.md`).
* **The trunk bay's contents — deliberately not invented** (`N` §6.D).
* **Five constant-roughness materials** — amber, glass, lens, reflector, ruby. `STATE.md` argues
  these are the legitimate exemptions (transmissive plus the sealed reflector).
* **`T1_SOFTEN` defaults to 1.0 and NOTHING SHIPS CHANGED.** `P1 = 0.455` at k = 1.0 reproduces
  rev 48 exactly. The k = 3.5 and cyc-0.30 frames are labelled experiments, not shipped.
* **Ablation switches that exist to WATCH A GUARD FAIL** — set them only to reproduce a defect, never
  in a delivery: `T1_BAREMAT=1`, `T1_TBFOOT=1`, `T1_BAYPROUD=1`, `T1_NOTAILBOARD=1`, `T1_SOFTEN=k`.
* **`STATE.md`'s `+525.0 mm OUT` length row** — a red row alongside `0 fail, 0 warn`. Diagnose the
  exclusion before treating it as a regression (§2.11).
* **Honest un-measured rows** — `verify.py:766` records plainly that row 1's length *"cannot carry
  the measurement because `X_NOSE` has never been measured."* Honest, not a defect; the defect the
  survey names is that it still counts toward the headline PASS number.

**DO NOT TOUCH / DO NOT CHASE**

* **`CAP_R = 0.1345`** — *"correct at 0.35 σ and locked … Do not touch"* (`t1_detail.py:165-169`).
  The hubcap flower is the **rim disc's** fault (A2).
* **`bulge = 0.019`** (the only forward-bulge term) and **`V_POW_Z = 0.60`** (a paint curve).
* **`ROUNDEL_Z_AG = 1.0170`**, **`ROUNDEL_D = 0.2800`**, **`IND_DZ = 0.206` / `IND_DY = 0.130`**
  (a "3.8 σ low" reading on the last pair was **retracted as a calibration error**).
* **"The rocker is not modelled" — REFUTED, rule 31.** `t1_core.section()` run B builds a bottom
  roll of radius `RB_ALL` = 0.122 m over the whole main run; `audit.py` publishes
  `rocker to ground 0.3177` into `STATE.md` every build (present now). Grepping for an object name
  is not a test for whether a feature is built.
* **"W4 has a photographed handle at last" — NARROWED.** The observable stands and is quantitative;
  it does **not** unblock the fix.
* **"The engine-lid outline is 65 mm too high" — NARROWED to A8.**
* **The rear bumper** — removed at the conversion, must not return (SPEC 2.4).
* **The Nolita frames** — geometry only. Never take artwork off them (rule 26).
* **`ref_workshop.jpg`** — geometry and clarity only. Never paint, shape or proportion.
* **`bus_model_ref.JPG`** — a fidelity bar only. Take nothing about shape, paint or proportion.
* **Do not fan out Blender.** Renders sequentially, from one script, in the background.
* **Do not edit `bootstrap.sh` or `verify_clone.sh` to make a line pass.** A failing check is a
  finding.
* **Do not ask him again**: the vent slats; the bunting (they are STARS); which vehicle (RED);
  W5; whether the tail board is on the vehicle; which rear bay is open; the tail with the engine lid
  open. And he has answered *"Neither is possible right now"* on the photographs — **record, do not
  queue.**

---

## 5. WHAT I COULD NOT CHECK, AND WHY

1. **Everything that needs a render.** `out/` exists and is **empty**. Every figure in `N` §6 quoted
   off `r49s_hero34f.png`, `r49s_rear.png`, `r49s_counter.png`, `r49board_side.png`,
   `r49base_side.png`, `r49s_low34.png`, `r49s_front.png` or `r49playa_playa_ref.png` is
   unreproducible from this tree — specifically: A7's 14.3 / 184.5 / 126.6 and the 8.8× / 12.9×
   ratios; A3's 0.675 / 0.708 / 0.695 correlations and the −0.012 control; A2's m = 5 harmonics
   0.050–0.056; A6's 22.4 % / 0.01 % / 20.9 %; A18's 57 % and 0.875; A4's 133.1 / 162.5 / p05
   42 / 72; A8's pixel route; the playa 0.2736 vs studio 0.5081. `N` §9's own rule applies:
   **render before quoting any probe that reads a frame.** I confirmed A8's *constants* route
   independently, and A1, A2, A4, A7, A14, A17 and A19 need no render at all.
2. **A1's "87 mm outboard of the roof edge" and "1.63 m from the counter."** I confirmed the
   direction and the 26–43° inclination error from the constants; the two distances need the built
   roof edge and counter face from the mesh.
3. **A13's premise** — that `ref_side.jpg` x 702..713, y 381..391 is "the door edge and the counter
   boxes". I confirmed the citation exists at `cal_gen.py:488`; I did not crop that region.
4. **A6's counter-fascia photographic half.** The survey's own ceiling flags it: it cannot rule out
   in-camera noise reduction in the 2007-era JPEG. Its *internal* control (one material, 0.01 % on
   the shell against 22.4 % on detail meshes) needs no photograph and is the part that survives.
5. **"1632 tool calls."** No log exists in the tree. "600+ working crops" resolves to **526**
   `rev50_*.png` on disk (592 `rev50_*` files including 65 `.py`).
6. **Whether the Nolita bus is physically the same vehicle as the target, and which state is
   earlier.** Nothing in the repository establishes either. The operationally binding half — paint
   and artwork do not transfer — holds regardless.
7. **The exact printed row count at `40dd87e`.** I did not check out an old commit (that would dirty
   the tree). I inferred 110 from `LEDGER_rev48.md:338` plus the `ck` deltas, which agree: 113 `ck`
   → 110 rows then, 125 `ck` → 122 rows now, the same 3-row gap in both eras. I did not trace which
   three `ck` invocations never print.
8. **The three-artwork-state assignment of `IMG_2073` vs `ref_workshop` as one vehicle.** I
   established their artwork differs; I did not establish they are the same green bus.
9. **Whether some superseded `SPEC.md` had a tail-board section numbered 10.28.** The citation
   `SPEC.md:937` is dead against the current file, and the current §10.28 is unambiguously about the
   detached sign. A stale line number would not change the object.

---

## 6. THE THREE THINGS I WOULD PUT FIRST

1. **Strike SPEC §10.28 from the footing request's provenance** (§2.1) — before it is put to the
   owner again. The request itself stands on `PHOTOS_WANTED_rev49` §1's parallax argument.
2. **Classify `ref_playa_34.png` / `ref_source.jpeg` as RED CURRENT in `N` §4 and in the prose**
   (§2.5) — the survey found this and it did not land, and `C1(b)` proposes making that frame the
   deliverable.
3. **Split A18 and stop calling the delivered frames shadowless** (§2.3) — the survey's own critic
   says the two halves cannot both be acted on, and the half that is live is the vignette and grain
   the owner personally chose at rev 15.

---

## 7. ADDENDUM — THE TREE WENT DIRTY DURING THIS AUDIT, AND IT WAS NOT ME

At **18:34:09** — after my `verify_clone.sh` run (18:08:40) and while this file was being written
(18:33:54) — `t1_shell.py` was modified by a **concurrent session**. `git status` shows exactly two
entries: `M t1_shell.py` and `?? probe_scratch/rev50/`. **Every file I wrote is under
`probe_scratch/rev50/refuter/`; I did not touch any tracked file.**

Three consequences for whoever reads this:

1. **The `ALL 122 PASS` in §1 row 1 was measured before that edit**, on a tree whose only
   difference from `HEAD` was the untracked `probe_scratch/rev50/`. `verify_clone.sh` requires a
   clean tree, so it must be re-run after the concurrent work is committed.
2. **The edit is the A1 fix**: `LID_OPEN_DEG` 104.0 → `float(os.environ.get("T1_LIDDEG", 76.0))`,
   plus a foot re-seat for `_roof_edge_y` and an in-source refutation of survey finding 49
   (`LID_W` "too narrow"). It is consistent with everything I measured independently: it states the
   free edge at 104° is `y = -0.8135` and at 76° is `y = -0.2765` — **both reproduce my own numbers
   exactly** — and it gives the roof half-width as `Yt = 0.7273`, which resolves my open item §5.2:
   0.8135 − 0.7273 = **86 mm**, so `N` §6 A1's *"87 mm outboard of the roof edge"* is **CONFIRMED**.
   `sin(76°) ≡ sin(104°)`, so no z dimension, bbox row, cutter extent or strut length moves — that
   claim is exact.
3. **One precision I owe on my own §1 row 35.** What I confirmed is that at 104° the lid's **free
   edge** lands 814 mm on the OFF side, away from the +Y counter, and that the built inclination is
   26–43° outside the photographed 61–78° band. The concurrent edit points out — correctly — that
   the painted **face normal** already pointed toward the counter at 104° (`(dy,dz) = (+0.970,
   +0.242)`, toward the counter and UP) and does so still at 76° (`(+0.970, −0.242)`, toward the
   counter and slightly down, an awning). So `N` §6 A1's phrase *"tips the mural lid AWAY from the
   counter"* is true of the **board's lean and free edge**, not of which way the mural faces. Say
   which, or the next context will look for a mural pointing at the wall and not find one.
