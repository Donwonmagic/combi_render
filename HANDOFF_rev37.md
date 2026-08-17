# HANDOFF rev 37

**203 commits, clean tree. Guards 0 fail / 0 warn at BOTH levels on BOTH tools.**
**126 objects, 185 meshes, 42 materials, 5 constant-rough, 0 non-manifold.**

---

## THE ONE-LINE SUMMARY

The owner **withdrew the entire front over-rider assembly** — the bar (rev 30),
its hoop ends (rev 36) and the posts built this revision. **The front is a plain
cream blade plus its two irons.** The revision's lasting yield is elsewhere:
**four of his own instructions were recovered from memory after being lost from
every carrier that crosses contexts**, one memory entry was proved to be a
phantom, and a `verify.py` substring ban that had never fired in the project's
history was found mis-scoped and repaired.

---

## 1. WHAT CHANGED

| file | change |
|---|---|
| `build.py` | **BUILD FILE.** `overrider_bar()` and `overrider_posts()` calls **COMMENTED, NOT DELETED** (SPEC 10.93, 10.91.8) |
| `t1_detail.py` | **BUILD FILE.** `IRON_Y`/`IRON_W`/`IRON_H` hoisted (values unchanged, verified inert); `overrider_posts()` + its constants added — **defined but not called** |
| `verify.py` | **BUILD FILE.** `BANNED_EXEMPT` + its own control; SPEC 10.91's post guard; §§10.83/10.90/10.91 now log **NOT APPLICABLE** when the assembly is absent, **and stay armed** |
| `SPEC.md` | NEW **§10.91** (eight parts), **§10.92**, **§10.93** |
| `STATE.md` | regenerated on the clean rev-37 tree at `d0db75a`, `working tree \| clean`. `STATE_rev37.md` alongside |
| NEW, read-only | `mark_rev37_region3.py`, `rev37_region3.png`, `HANDOFF_rev37.md` |
| hero | `rev37_hero34f.png` — **gitignored, on his disk only** |

**NO SHADER. NO ARTWORK. Textures unchanged (3/3 md5s).**

---

## 2. THE FIGURES, WATCHED PRINT

| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 0 warn** | **0 fail, 0 warn** |
| `audit.py` | **0 fail, 0 warn** | **0 fail, 0 warn** |
| roof crown @ rear axle | **1.9835** | **1.9833** |
| rear arch lip → gap | 0.3722 → 39.7 mm | same |
| front arch (control) | 0.3732 → 40.7 mm | same |
| rake | 17.75 mm/m (locked 17.75) | same |
| dims | L=4.065 W=1.750 | same |
| cut roof hole | **68564v** | **252749v** |
| objects at `materials:` | **126** *(was 127)* | **126** |
| shut line × aperture | 0.0 mm / 804.9 mm | same |
| `CARGO_GAP` samples | 154 | same |
| bay widths | 0.516 0.515 0.516 | same |
| over-rider rows | **NOT APPLICABLE, stated** | same |

**EVERY BODY FIGURE IS IDENTICAL TO REV 30–36's.** The only deltas are
127 → **126** objects and 186 → **185** meshes, both the removed bar.

**HERO: `rev37_hero34f.png`, 4800×3200, SUB=2, 56 samples, 20 strips, worst seam
z = 1.86** (rev 25 shipped 1.91; threshold 4). `post.py` run **once** on the
stitched frame. It depicts the plain blade.

---

## 3. THE HEADLINE: FOUR OF HIS INSTRUCTIONS HAD BEEN LOST

rev 36 found that his own defect report survived only in memory. **rev 37 found
four more, at four times the scale.** Each was verified against the tree:

| # | instruction | rev | state after rev 37 |
|---|---|---|---|
| 1 | "model them" — bar **and post** | 26 | **ANSWERED** — built, then he withdrew the whole assembly |
| 2 | **Nolita re-admitted FOR GEOMETRY ONLY** | 15 | **STILL UNUSED.** `grep -ic nolita`: 8 in SPEC, **0 in REF_MEASUREMENTS** |
| 3 | **execute the GitHub migration** | 31c | **STILL UNFULFILLED** |
| 4 | region 3 not selected as bus cream | 19 | **RE-PUT to him, §10.92. Awaiting his answer** |

**ITEMS 2 AND 3 ARE THE LIVE ONES AND NEITHER IS IN ANY WORK LIST BUT THIS.**
Item 2 matters most: the brief calls `CREAM`, the absolute roof height and the
off flank's 804.9 mm **photograph-blocked**, while an **authorised source class
for exactly those** has sat unused for 21 revisions.

**A MEMORY ENTRY IS A CLAIM TOO.** Memory said the migration procedure was
written as `MIGRATION_APPENDIX_rev32.md` at commit 159. **Both halves false** —
the file has never existed in any commit in any ref, and commit 159 is SPEC
10.86. Memory recovered four real instructions and invented one artefact; the
recovery is trustworthy *because* each was greped.

---

## 4. THE WITHDRAWAL, AND WHY IT IS NOT A REVERSAL OF HIS REV-26 READING

He chose the post as rev 37's work, then reversed mid-revision — *"I want to
change my decision back, sorry. I want to stick to the original bumper."* Asked
how far back that reached (deliberately, since the bar and hoop ends are older
work and one came from his own defect report), he chose the **widest of three
scopes: remove the bar entirely.**

**HIS REV-26 READING STANDS.** It was a reading of a **workshop** photograph and
remains one. What changed is the scope decision layered on it — always his — and
it is **consistent with SPEC 2.4's own precedent**: `ref_workshop.jpg` is the
**conversion** stage, the rear bumper was removed between that stage and service,
and **no in-service frame shows the nose.** The WORKSHOP-STAGE tag existed
precisely so this could be pulled back out.

**IT COSTS NOTHING THAT WAS EVER MEASURED**: the bar's scale was CATALOGUE-
anchored (§10.72's struck class), its standoff a CHOICE, its lateral extent grade
E, the posts' station a STRUCTURAL INFERENCE.

**GUARDS KEPT ARMED, PROVEN BY TWO ARMS RATHER THAN ASSERTED:**

| arm | result |
|---|---|
| re-enable the bar | §10.83 and §10.90 rows **come back alive**, 127 objects |
| re-enable it with `BAR_LEG_LEN` × 0.8 | §10.90 **FAILS** — *"floats 12.36 mm above the bumper"*, both ends |

**Re-enabling is one commented line and needs no edit to `verify.py`.**

---

## 5. FOUR DETECTOR DEFECTS OF MY OWN, ALL IN THE POST GUARD

Recorded in full in §10.91.6. All caught by the guard or by an arm's output,
**none by inspection**:

1. **The landing datum was the CROWN** — §10.90's own datum error reproduced, via
   a `_blade_top_at()` **fall-through two microns outside its domain**. A helper
   that answers anyway outside its domain supplied a datum.
2. **"Footprint sampling" that sampled ONE vertex**, because step 8b shears the
   mesh and a cap is not planar in z. **The fix for the single-vertex defect WAS
   the single-vertex defect**, caught only because the numbers did not move.
3. **An "overlap" that was the member's own thickness** — 108.24 mm is
   `BUMP_PROFILE`'s height, 24.97 mm is `BAR_DIA`. A penetration depth is not a
   distance to an exit surface.
4. **A threshold that changed sign underneath the test.** ARM 4b drove
   `POST_WELD_MAX` to −5.00 mm; a negative weld bound **inverts** the test and it
   fired on a floating post. **§10.90's ARM-3 defect one level up**, caught the
   same way — by reading the arm's output, not noting it went red.

**AND ARM 4 IS A NON-ARM, PUBLISHED AS ONE.** Landing on the crown gives 0 fail,
because a flat-bottomed post on a sloping channel touches somewhere either way.
**THE GUARD BOUNDS THE JOINT TO WITHIN `BUMP_PROFILE`'s 2.30 mm SLOPE BUT DOES
NOT FIX WHERE IN THAT BAND THE BOTTOM SITS.** Fifth revision running in which an
arm turned out not to be one.

**AND THE LOG LINE WAS ASSERTING ITS OWN DATUM** — *"landed on
`_blade_top_at(axis)`, NOT on the crown"* was FALSE under ARM 4 while the guard
passed. It now **prints** the measured offset.

---

## 6. THE `BANNED` REPAIR — LIVE REGARDLESS OF ANY POST

`verify.py`'s `BANNED` contains `"post"`, a prophylactic ban on pickup-era
geometry. `git grep` over **every commit in every ref**: no object has ever been
built in this tree whose name contains "post". **It had never fired on anything
until it fired on a member the owner had asked for.**

Neither renaming the object (dodging) nor dropping `"post"` (deleting coverage).
`BANNED_EXEMPT` matches **WHOLE lowercase names, never substrings**, and carries
**its own two-sided control**, run every build: four planted near-misses must
still be caught, and every exempt name must be one `BANNED` actually matches.
**A NAMED EXEMPTION IS A HOLE IN A GUARD, SO PROVE THE HOLE IS THE SIZE IT
CLAIMS.** Falsified in two arms (6 and 7).

---

## 7. THE ONE QUESTION OUTSTANDING

**§10.92, REGION 3 — awaiting his answer.** `rev37_region3.png`: one 7× crop of
`ref_side.jpg` (u 556–700, v 396–448), **one red circle**, one sentence — *is the
pale band under the brass nosing the BUS's own painted body, or part of the
COUNTER?*

rev 12 settled it as the body's belt paint; in rev 19 he was shown four candidate
cream regions and **did not** pick this one. **What it closes:** whether
`countercream` should carry that band at all — if it is the body it belongs to
`body_paint`'s cream and inherits the flank's weathering, fade and dust, none of
which the counter applies. **Shader routing, not geometry. Nothing moves until he
answers.**

---

## 8. WHAT I DID NOT DO

- **`probe_clean_top.py` / `probe_dust_anchor.py` were NOT rewritten.** **FIFTH
  revision now.** They remain deliberately failing.
- §10.70's arms not re-run; tail-lamp slot, `Senor` letterforms, `SCR`'s +80 mm
  untouched.
- **Nolita never opened** — the largest unspent lever in the project.
- All 25 inherited probes were **run**, and every control count matches the
  brief. **Do not "fix" any of them.** My own summary grep **under-read six**
  before I read their logs — §10.90.10's lesson, on me, within ten minutes.

---

## 9. LATE IN THE REVISION HE SENT EIGHT DEFECT REPORTS OFF THE HERO

**This is the most valuable input since rev 35, and it arrived only because the
hero was shot.** `rev30_hero34f.png` was superseded in rev 36 and never re-shot,
so these eight sat unseen for seven revisions.

**Batch 1 (SPEC 10.94), verbatim:** *"the front nose is shaped inaccurately, it
looks more like the front of an amtrak train than a vw bus, also we need to fix
the vw logo, also the paint job and the headlights are not alligned"*

**THREE OF THESE CORROBORATE FINDINGS THIS PROJECT MEASURED AND NEVER APPLIED.**
Every mapping verified by grep against SPEC and the build files:

| his report | existing finding | status before he spoke |
|---|---|---|
| paint / headlamps not aligned | §10.24 item 3 — headlamp centre belt − 0.339 ± 0.025 m photographed vs **belt − 0.242** built, **97 mm at ~3.9 σ** | **OPEN SINCE REV 10** |
| the vw logo | §10.25's premise is **FALSE** — "no gap but a **52 mm interpenetration**" | fix made the glyph smaller, hiding the fusion |
| nose shape | `V_POW` locked **0.60**; audit implies **0.30–0.48** (arm rises ~2× too fast) | measured, never applied |

**§10.24's STATED BLOCKER WAS DISCHARGED AND THE ENTRY NEVER LEARNED OF IT.** It
said the headlamp claim "deserves a second derivation first". The rev-11 audit
gave two: **83 ± 19 mm at 4.4 σ** by a ratio needing no px/m, and a test needing
**no scale at all** — *in the photograph the indicator aperture lies BELOW the
two-tone break; in the build it lies ABOVE it.* **That sentence is his report.**

**TRAP: DO NOT MOVE THE ROUNDEL WITH THE LAMPS.** Its height is supported by both
chains. And **report 3 is ONE report about a RELATIONSHIP** — do not split it.

**Batch 2 (SPEC 10.95), verbatim:** *"the doors extend lower, around the wheel
well, also there seems to be a bar obstructing the front wheel? also '100%
calidad' is off center, and we there are two bars propping up the art sign on
either side, not one"*

- **THE SIGN'S STRUTS — CONFIRMED, COST ONE GREP.** `t1_shell.signboard()`
  appends **ONE** strut, no loop over sides. He reports two. **Build this first:
  a count needs no scale, no px/m, no camera model.**
- **THE DOOR AND THE "BAR" ARE PROBABLY ONE DEFECT.** `doorback1` spans
  x [0.918, 1.824] with its lower edge at **z 0.717**, **52 mm above the tyre's
  crown (0.665)**, across the whole arch; the bar's blunt end in the render lands
  on `doorback1`'s rear edge at x 0.918. **LABELLED AS A WELL-EVIDENCED
  IDENTIFICATION, NOT A CONFIRMED ONE — THE ABLATION WAS ATTEMPTED AND DID NOT
  RUN** (camera unresolved; appending to `build.py` would have executed after the
  preview render). **No ablation result is reported because none was obtained.**
  `_DOOR_TOP_AUTH`/`DOOR_H` are AUTHORED and the door's LOWER boundary has never
  been measured, so nothing locked stands against him.
- **"100% Calidad"** — `cal_gen.py:246` places it at an absolute 0.180 of texture
  width. **Texture-versus-panel NOT determined; do not guess** (§10.20's family).
  **Distinct from his earlier sticker LEGIBILITY complaint — do not merge them.**

**NOTHING WAS BUILT ON ANY OF THE EIGHT.** §10.95.4 has the ordered list.

**THE LESSON, AND IT IS THE REVISION'S BIGGEST: SHOOT THE HERO ON EVERY REVISION
THAT MOVES GEOMETRY.** Eight defects surfaced the moment one was shot.
