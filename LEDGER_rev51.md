# LEDGER — rev 51

**Everything this revision measured, changed, refuted, retracted and corrected.** Figures here were
watched print unless a line says otherwise. **Where this ledger and the machine disagree, the machine
is right.**

---

## §0. THE HEADLINE

**Job 1 (A2, the five-petal hubcaps) was reframed before it was measured, and the reframing is the
finding.** The record says two mechanisms produce the identical image and neither depth is measured.
That is a false dilemma. The ~58 mm proudness is **forced by the cap's own authored section under
either fix**, because a hubcap must seat its lip on the wheel:

```
proud = dome_depth - (flange_y - disc_at_lip) = 70.5 - (64.0 - 51.7) = 58.2 mm
```

`hubcap()`'s profile runs `(0.0745, 0.0000)` at the apex to `(0.0040, 0.1370)` at the lip — a **70.5 mm
dome depth**. So there is a **THIRD mechanism nobody named: the dome depth itself.** And `CAP_R =
0.1345`, marked *"LOCKED ... Do not touch"* and treated throughout the record as settling the cap, is a
**RADIUS**, validated against `hubcap D / tyre D` — a ratio of two **diameters**. It says nothing about
depth, and the depth is authored with no citation anywhere in the repository. That is precisely the
"neither depth is measured anywhere" the brief points at, and it belongs to the **cap**, not to its
mounting.

The measurement that settles it converts straight onto the profile: **required dome depth = measured
proudness + 12.3 mm.**

**MEASURED, THEN FIXED, THEN LOOKED AT.** Recovered from photographs by a **shape-free** estimator --
the emblem sits on the axle axis, so its projected offset from the cream-ring ellipse centre in an
obliquely-seen wheel carries h with no dome profile entering:

```
IMG_2073.jpeg      (GREEN, chrome cap)   phi 49.6   49.8 +- 8.7 mm
ref_rear34.jpg     (RED, current)        phi 70.2   62.1 +- 16.0 mm
ref_nolita_front34 (RED, earlier)        phi 58.3   49.4 +- 20.5 mm
weighted                                            52.2, 1sd ~7 mm

as built, 10.5 mm  ->  EXCLUDED at 5.8 sigma
seated,   58.2 mm  ->  CONSISTENT at 0.8 sigma
```

Controls all passed: side ORTHO at phi = 0 returns q = +0.0002 +- 0.0025 (the dome term must vanish);
low34, where the answer is KNOWN to be 10.5 mm, reads back 12.6 +- 9.2; ref_side.jpg at phi = 10.5
correctly returns UNRECOVERABLE. **AND IT REFUTES THE THIRD-MECHANISM HYPOTHESIS ABOVE** -- implied
dome depth 64.5 mm against the authored 70.5, inside 1 sigma. The profile is NOT touched. The brief's
claim that the photographs refute fix (a) is WRONG; they support it.

**AFTER THE FIX, on fresh renders:**

```
m5 harmonic, the survey's OWN instrument, 4 thresholds
  before   0.0487 .. 0.0565      after   0.0005 .. 0.0019      circle control 0.0000
5-fold in the band the vents cleared (r 0.1345-0.1415)
  before   0.1295 / 0.1314       after   0.0055 / 0.0148       photographs 0.0024-0.0150
cap edge / rim radius, from the max red radius
  before   0.5369                after   0.625                 built INTENT 0.6233, photos 0.60-0.65
```

**TWO CEILINGS, STATED.** (1) A residual 5-fold persists on the FRONT wheel in a band moved clear of
both the vents and the cap lip: A5 0.0100 at SNR 5.4, where the rear is clean at 0.0047 / SNR 1.8.
The amplitude is inside the photographs' own range so it is not a visible defect, but it is
statistically distinct and **I have not explained it**. (2) The median visible-red radius reads 35.00
px against a geometric lip at 37.25 px, because the dome's own shading darkens toward the rim and the
red gate loses it before the geometry ends -- the survey predicted exactly this bias. Quote the max,
not the median, for the edge.

---

## §1. THE BRIEF, GRADED — WRONG IN TEN PLACES, IMPRECISE IN SEVEN

An adversarial agent was set on the brief **before any work started, and this revision did not close
until it reported.** Every item below was then re-checked by hand against the machine.

| # | the brief says | the machine says |
|---|---|---|
| 1 | *"bootstrap's row 10 is 'no branch carries work HEAD does not have'. If that row is green you are on the right ref. Believe it over any sentence in this brief"* | **IT IS ROW 9.** Row 10 is `verify_clone.sh`. The machine's own numbered output: `8 clone depth / 9 no branch carries work HEAD does not have / 10 verify_clone.sh`. **I repeated "row 10" in my own first report before counting** — the machine outranks my prose too. The *instruction* is right; only its address is wrong. Propagated from `LEDGER_rev49` through `NEXT_CONTEXT_PROMPT_rev50`. |
| 2 | *"Moving the cap the full **49.7 mm** puts its apex **60.2 mm** proud"* | **NOT A DERIVABLE MOVE.** The three real clearance criteria give **39.2 / 47.7 / 54.9 mm**, landing the apex at 49.7 / 58.2 / 65.4 mm proud. And `10.5 + 39.2 = 49.7` **exactly** — the published "move" is the *proudness resulting from* the 39.2 mm move, with the as-built 10.5 mm added a second time to reach 60.2. §5 A2's own *"the cap ~48 mm too far inboard"* is the 47.7 figure: **two values for one quantity, four lines apart.** |
| 3 | *"vignette 0.000, grain 0.0000 — verify those two constants exist and are zero"* | **NO SUCH CONSTANTS, AND NEITHER IS ZERO.** `studio.py` has `_envf("T1_VIG", 1.0) * 0.055` and `_envf("T1_GRAIN", 1.0) * 0.016`; `post.py`'s `_FLOATS` carries `vig` and `grain` at **1.0** — it is `bloom` that is 0.0. The 0.000s are **measured delivered amplitudes**. The finding is real; the description is not. |
| 4 | *"`T1_CTAN_WEAR=0` already exists and **has never been exercised**"* | **IT HAS.** `probe_ctan_pedestal.py` carries it as arms 3 and 4 under *"Every triple here was READ OFF THE CONSOLE"*, with the radiances stored. **And it is not a clean ablation:** the same file records it as *"wear = 0 (TWO levers: also drops Metallic)"*. Anyone isolating A6's chip mechanism with it measures two changes and attributes them to one. |
| 5 | *"stale FIVE revisions running"* | **SIX, and this session was the sixth** — proved directly from `git reflog`: the rev-51 branch was created at `origin/main`, 0 ahead / 0 behind, while the work sat 39 ahead, and its remote copy had been deleted. |
| 6 | *"the 0.3 m roof-strip figure retired"* | **HALF-LANDED.** §3. |
| 7 | *"§10.123 states rule 29 at `SPEC.md:10238` and breaks it at `:10241`"* | **ROTTED.** Rule 29 is at 10239–10240; `:10241` is blank; the requirement is at 10242–10243 and is **already struck through and WITHDRAWN**. |
| 8 | *"rev 48's refuted 'B stays open' still live at `build.py:936-938` / `t1_shell.py:1380-1383`"* | **TRUE IN SUBSTANCE, STALE LINE NUMBERS** — the text is live at `build.py` ~1010 and `t1_shell.py` ~1499. Cite strings. |
| 9 | the m5 figure set, and `LEDGER_rev50`'s ceiling that its normalisation is *"TWICE the survey's"* | **THERE IS NO CONVENTION CONFLICT.** §2. |
| 10 | `LEDGER_rev50` §10: the un-reported agent's brief *"is recorded in §11 of the handoff"* | **§11 DOES NOT EXIST.** The rev-51 prompt has §1–§9 and there is no rev-50 handoff (last is `HANDOFF_rev45.md`). That brief is gone; job 1 was reconstructed from §5. |

**Imprecise, right in direction:** the identity-transform assert covers every mesh *that exists at step
8b* (step 8c builds nine more; the wheels are step 7, so the A3 refutation is unaffected); the "143 mm
field" appears in no source file and reconstructs as `1 / W_CLUST_SCALE = 142.9 mm`, while the field's
largest feature is `W_N1_SCALE` → 285.7 mm (argument untouched: 2400 ≫ 286); `_lid_w_bound()` does not
*walk* anything, it is closed form; "reproduced three ways to 0.2 mm" is two ways plus *"by eye"*;
A7's "the ONLY aperture his ruling leaves open" — `STATE.md` says `open serving apertures on +Y: 3`;
`IND_X` names a constant that does not exist.

**Confirmed:** ALL 125 / ALL 10; five byte-identical pairs and nine distinct frames; `gal_rail` **165 mm
too LONG** (the brief's correction of the survey's sign is right); the galley offset range
(−0.0957…−0.1103, better than the survey's own); `gal_caddy_fill`'s X sign; the zero-area `lid_rail`;
both rev-50 re-bases carrying genuine companion rows; W6 and the wipers landed in the source.

---

## §2. THE m=5 "CONVENTION CONFLICT" IS NOT ONE — AND BOTH SIDES WERE WRONG

`LEDGER_rev50` §9 states as its own ceiling that its normalisation is *"2|F_m|/n/mean, **twice** the
survey's convention — my numbers ... must NOT be compared to its published 0.0399."* This revision's
adversarial pass went further and called the published figures mutually impossible. **Both are wrong,
for the same reason.** Cross-applying the two normalisations to the two control shapes isolates the
variable completely:

```
survey's HALF-WAVE RECTIFIED petal     survey norm 0.0399     mine 0.0389
a PURE SINUSOID petal                  survey norm 0.0800     mine 0.0800
```

The **normalisations agree to 2.5 %.** It is the **CONTROL SHAPES** that differ 2×:
`probe_scratch/rev50_fidelity-bar_hub5.py` builds its control as `np.clip(np.cos(5*th),0,None)`,
half-wave rectified, whose fundamental is **half its peak** — `2.6/2/32.6 = 0.0399` exactly. A pure
cosine of the same fractional amplitude gives 0.0800. So the render and `ref_side` figures agreeing at
1× across both instruments is **correct, not a contradiction.**

**Settled on the machine, not by argument.** The survey's own instrument, unmodified except for the
frame path, run on a fresh rev-51 render:

```
render rear hub, 4 thresholds   m5 0.0487..0.0565   every other harmonic <= 0.0085
ref_side.jpg rear hub, same 4   m5 0.0124..0.0216   NOT separated from m2 (up to 0.1608)
```

against my own independent instrument's **0.0554 / 0.0553** on the two wheels. Two instruments, one
frame, agreement to 0.001. **My instrument passes a control the original lacked** — a red disc with a
**WHITE CENTRAL HOLE**, which returns identically to a plain disc and so defeats the VW-emblem ray
termination that broke rev 50's first version (median radius 8.25 px on a 33 px dome).

And the crossover reproduces a **fourth** independent way: re-derived analytically from the two
authored profiles, **r = 0.11973 m**, matching the record exactly.

---

## §3. WHAT LANDED IN THE SOURCE

**The 0.3 m retirement only half-landed at rev 50, and the live half would have re-opened three things
the owner closed.** A block above `LID_Y_HINGE` was still publishing, live and unannotated: the roof
spanning `y -0.7273 .. +0.7273`; `W <= 1.2723 m`; *"178 mm PAST the roof edge"*; *"against the owner's
settled 'roughly 0.3 m each side'"*; *"THAT IS AN OWNER QUESTION (rev 50 C3), NOT A CONSTANT TO TUNE"*;
and *"W is left at 1.1100 deliberately"*. Every one is contradicted 80 lines below in the same file.

Measured, not transcribed — watched print from the assert under `T1_LIDASPECT=1.2`:

```
"the roof reaches only y=0.7347 at the lid station, so W <= 1.2797 m"
"LID_W = 1.7469 m runs the roof aperture 467.2 mm PAST the roof edge"
```

so at W = 1.45 the overrun is `1.45 - 1.2797 =` **170.3 mm, not 178**. The 178 comes from the record's
stale `Yt = 0.7273` — **and the same stale 178 was sitting inside the block rev 50 wrote to correct
it.** Both sites now carry the machine's walk. Struck through, not deleted, per the wipers convention.

**The foot guard's comment claimed the opposite of the truth.** It read *"it cannot be satisfied by
construction the way its predecessor was"*. False, and in the same direction as the guard it replaced:
`z0 = _seat + _hang + 0.0040` and the lowest vertex is identically `z0 - _hang`, so `_lo = _seat +
0.0040` whatever `_seat` is, and `_lo < _seat` **cannot fire** in the shipped path. It prints
*"+4.0 mm clear"* every build because 4.0 mm is what was typed two lines up. **Rule 32, third
occurrence on this one guard.** Relabelled in the comment and in its log line as what it is — a
**construction-consistency check** — and kept, because it still catches a `z0` not built from `_seat`,
which is what `T1_TBFOOT=1` substitutes.

---

## §4. SEVEN INSTRUMENTS OF MY OWN WERE WRONG, AND EVERY ONE WAS CAUGHT BY RUNNING IT

* **Two dead measurement windows**, both caught by marking them and looking. A *"cab roof cream"* box
  that was not on the roof at all — it straddled the mural lid and the white background (17.15 % dark /
  14.17 % bright, meaningless). A *"flank cream"* box that included the bulb string, which is why it
  returned **27.68 % bright**. Both withdrawn; neither published as a number. This is the completeness
  critic's own recorded failure, reproduced by me.
* **A third dead window**, same revision, same cause: a *"VW roundel disc"* box on `detail_f` that
  straddled the V and W strokes, so its 13.85 % was measuring **bars, not speckle**. Withdrawn.
  **I have changed my order of operations to mark-and-look BEFORE computing, not after.**
* **A guard I added that failed its own control.** I cross-checked `_seat` against
  `roof_z(x0, TB_Y_CENTRE) - rake_drop` as an "independent analytic route". **It fired on the clean
  build** — mesh `1.7497` vs analytic `1.6391`, **110.6 mm apart**. The instrument is wrong, not the
  build: `x0 = -1.8530` is 20 mm from `X_TAIL`, **inside the tail roll-down**, where `roof_z`'s
  main-run crown formula does not describe the surface (`ZT_ALL` is worse still at 1.6227), and
  `LEDGER_rev49` §6a's own walk agrees with the **mesh**: *"1.7497 at -1.850"*.
  **I did not widen the tolerance to make it pass.** Withdrawn, with the finding recorded at the site,
  because the negative result is worth more than the guard: **at the board's station there is NO
  analytic route to cross-check `_seat` against**, so reading it off the body mesh is not the better
  choice but the only correct one — which is the deeper reason rev 49b went wrong, and a trap for
  anyone who later tidies it into a profile function.
* **The A2 clearance guard's first version fired on a CORRECTLY SEATED cap.** The hubcap profile is
  **not monotonic in r** -- it runs out to the lip and RETURNS along the back face -- so sorting the
  whole list by radius read the return point `(-0.0035, R + 0.0010)` where the front surface belonged,
  reporting -7.1 mm at r = 0.1355. Corrected to the front half only. Once corrected, the ablation
  fires at **r = 0.11974**, matching the analytic crossover 0.11973 to 0.01 mm.
* **A notch-band window that measured the wrong annulus.** I sampled r 0.140-0.160 for the 5-fold null
  and got a null in BOTH frames -- because the notches physically spanned 0.1345-0.1415, outside my
  band. Caught by checking the band against the vent geometry instead of trusting the number.
* **AND A SEVENTH, WHICH IS THE THIRD OF EXACTLY ONE SHAPE.** I predicted that a seated cap would
  displace the emblem from 4.98 px to 15.79 px off the wheel centre in low34, and measured 18.79 ->
  17.67 px, i.e. no change. **The instrument was wrong.** Its "emblem" mask selected 2827 px -- the
  whole upper CREAM RIM RING -- because my "inside the red blob" restriction was a RECTANGLE, and the
  rim ring falls inside that rectangle above the cap. Caught only by PAINTING THE MASK AND LOOKING AT
  IT (`probe_scratch/rev51/MASK_check.png`). **The cross-check is WITHDRAWN**; A2 rests on the three
  confirmations above, not on it.
  **THE PATTERN, NAMED:** three of this revision's seven instrument defects are the same defect --
  a mask or window that selected the wrong pixels. I wrote the rule for myself after the first two
  and then broke it again on the seventh. **NEVER PUBLISH A NUMBER FROM A MASK OR WINDOW YOU HAVE NOT
  PAINTED AND LOOKED AT.** Not "marked and looked at afterwards" -- painted, before the number.
* **A process defect:** I ran `git add -A` on a directory a live dispatched agent owned, staging two of
  its in-progress files, which made `verify_clone` read 124/1 and briefly confused the adversarial
  agent. Not a content failure. Do not `git add -A` a directory an agent is writing.

---

## §5. THE ARTWORK STATES — IT IS **FOUR**, CONFIRMED BY LOOKING

Rev 50 saw the claim and did not verify it. Verified here:

| class | frames | what the artwork carries |
|---|---|---|
| **RED, CURRENT** | `ref_side.jpg`, `ref_rear34.jpg`, `ref_playa_34.png` (= `IMG_3842.png` = `ref_source.jpeg`) | scrollwork, Señor Tacombi script, Calidad burst |
| **RED, EARLIER** | the four *nolita* frames | plain red flank, `TACOMBI.COM`, no scrollwork, no script, no burst |
| **GREEN, IN SERVICE** | `IMG_2073.jpeg` | script in **BLACK**, plus white/blue scrollwork with yellow daisies, plus a **100 % Calidad starburst**, plus orange TACOS / BREAKFAST SPECIAL. Headlamps fitted. |
| **GREEN, CONVERSION** | `ref_workshop.jpg` | script **ONLY**, silver outline. No scrollwork, no daisies, no burst. Headlamps **not fitted**, and `mark_rev32_q.py` records **both road wheels are bare painted rims with NO HUB CAP**. |

**The two green frames corroborate each other on nothing.** And `ref_workshop.jpg` is useless for any
wheel or lamp reading — it has neither fitted.

**A correction to the frame arithmetic:** `ref_playa_34.png = IMG_3842.png = ref_source.jpeg` is written
as an identity chain, but only the first two are byte-identical (md5 `230a2a90df`). `ref_source.jpeg` is
`03631c7ae3` — the **same photograph** at 246×197 (correlation **0.9768**, confirmed by looking), not the
same file. So: **15 files, 5 byte-identical pairs, 10 distinct files, 9 distinct frames.** The count of
9 is right; the `=` is not a byte identity.

---

## §6. A6 — THE BASELINE, WITH ITS CEILING STATED

Windows verified **by eye before any number was computed**:

```
counter fascia, same feature, matched to 800 px/m
  render out/r51b_side.png        dark 17.06 %   bright 3.36 %   p2 -0.139
  ref_side.jpg                    dark  0.62 %   bright 0.00 %   p2 -0.023

the SUBDIVIDED shell, out/r51b_detail_f.png, three windows
  nose cream left of roundel      dark 0.00 %    bright 0.00 %
  nose cream right of roundel     dark 0.00 %    bright 0.00 %
  cab cream above the roundel     dark 0.00 %    bright 0.00 %

CONTROLS   flat cream + 0.5 DN noise   0.00 %      (expect ~0)
           flat cream + 7.6 % chips    6.58 %      (expect ~7.6)
```

**CEILING, stated:** a local-median threshold count is **structurally blind to the large-cell,
low-contrast MOTTLE** that is plainly visible on the same cream in the same crop. These figures are
true for **chips** and say nothing about the mottle. The completeness critic warned of exactly this and
its own attempt failed on straddling windows.

**The mechanism, by string.** `pw = _mr(nt, PT, W_PT_LO, W_PT_HI, ...)` with `W_PT_LO, W_PT_HI = 0.520,
0.600`; Blender's Pointiness is 0.5 on a flat face, so any low-poly convex vertex clears 0.600 and
`pw → 1.0`. `deep` is fed **from `pw`** (`deep = _mr(nt, pw, W_STEEL_LO, W_STEEL_HI, ...)`), so it
saturates too. Both gates, structurally.

**The fix is well-grounded and NOT shipped this revision.** `round_edges()` already splices a Cycles
`ShaderNodeBevel` into every Principled BSDF's Normal input, and a Bevel node **ray-traces a real
radius in world units** — mesh-density independent in exactly the way Pointiness is not. That is the
right edge detector. It is not shipped because validating a shader change needs before/after renders at
6–15 min each and because the obvious ablation is confounded (§1 row 4). **A6 is diagnosed, not fixed.**

---

## §7. HELD UP AGAINST THE SOURCE PHOTOGRAPHS — THE NOSE, FOR THE FIRST TIME

The owner's standing instruction *"REMEMBER TO HOLD UP NEXT TO THE ACTUAL SOURCE PHOTOS"* was carried in
every brief to rev 43 and lost when the standing-instructions section was deleted at rev 44. The record
says it was done for the show flank and the cab door and is *"Still never done for the NOSE, the TAIL
or the ROOF."* Done here for the nose (`probe_scratch/rev51/FIG_nose_vs_photographs.png`).

**Corroborated by eye, all previously only in the survey:** the **headlamps sit flush** where both
photographs show a proud chrome-rimmed lamp standing out of the panel with its own shadow (finding 63 —
the bore is cut at the lens radius while the bezel's widest ring sits 14 mm *behind* the skin); the
roundel's **V-arms stop short** of the ring while the W arms reach (finding 34); the **nose reads flat**
where both photographs show a forward crown (W4 — recorded, still blocked on the grazing frame).

**Right, and not to be re-litigated:** the V two-tone break's shape and station, the roundel's position
and diameter, the headlamp stations, the bumper blade, the overall nose proportion.

**The TAIL and the ROOF halves are still not done.**

---

## §8. THE STATE OF THE MACHINE

```
bootstrap.sh      ALL 10 PASS      (the branch check is ROW 9, not row 10)
verify_clone.sh   ALL 125 PASS     clean tree
build             T1_SUB=1  rc=0,  VERIFY: 0 fail, 0 warn
renders           out/ NOT tracked, starts EMPTY.  Four frames rendered this revision,
                  every one rc=0 CAPTURED FROM BLENDER, not from the last command:
                  r51b_side, r51b_detail_f, r51b_low34, r51b_counter
```

**THE `counter` BASELINE IS BACK** — the frame rev 50 lost to its own `rc=$?`-after-the-redirect bug.
It confirms rev 50's headline fix **by looking, for the first time**: the mural board leans over the
counter as an awning. Nobody had seen it, because rev 50 fixed it and lost the frame that shows it.

**EVERY ABLATION RE-WATCHED FIRING THIS REVISION**, rc=1 on each: `T1_TBFOOT`, `T1_BAYPROUD`,
`T1_BAREMAT`, `T1_LIDDEG=104`, `T1_LIDASPECT=1.2`, `T1_HANDLEHI`, `T1_BAYSTALE`, `T1_LAMPSINK`.

**GUARD GAP, UNCHANGED AND TOTAL:** 128 `ck` rows in `verify_clone.sh` and **not one** mentions a wheel,
hub, cap, rim or vent. `verify.py` has none either. The most visible defect in every frame has zero
verifier coverage.

---

## §9. THE BRANCH — AND IT CHANGED SHAPE MID-SESSION

Stale a **sixth** consecutive revision, in rev 50's exact form: the designated branch's remote copy had
been **deleted** (`fetch --prune` reported `- [deleted]`) and HEAD measured **0 ahead / 0 behind** while
the work sat **39 ahead** on `claude/combi-render-setup-dkgwme`. HEAD was a strict ancestor; it
fast-forwarded and nothing was lost.

**Then `origin/main` moved while this revision was running.** PR #7 merged that branch — all 39 rev-50
commits — into `main`. Caught only because `git rev-list --count origin/main..HEAD` came back **3** when
it should have been 42, i.e. **by re-measuring rather than trusting the count taken at pickup.** Merged
back; content diff against main **empty** (no photographs arrived, nothing lost).

**CONSEQUENCE FOR REV 52:** every historical branch was absorbed by that merge and now reads 0 ahead, so
*"work from whichever ref is furthest ahead"* selects **this branch and nothing else**. The failure that
has been stale for six revisions may not recur in the same shape — **but measure it, do not assume
either way.**
