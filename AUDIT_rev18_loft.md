# AUDIT rev 18 — the rev-16 loft, adversarially

Four auditors, disjoint files, each instructed to **refute**, all read-only.
Run on HEAD `7ce3d03`, 71 commits, clean tree, Blender 4.5.3.
Both guards re-run before any measuring: **0 fail / 1 warn at BOTH levels**,
warn `roof crown @ rear axle (dome-corrected) 1.983 vs spec 1.960 (+23 mm)`.

| auditor | files | outcome |
|---|---|---|
| A | `t1_core.py` | 8 findings, 7 refutations of its own brief |
| B | `t1_shell.py` | 7 findings, 5 refutations |
| C | `verify.py`, `audit.py`, `STATE.md` | 3 dead guards, 3 STATE phantoms |
| D | `SPEC §10.34–37`, `LOFT_GROUND_rev15`, `HANDOFF_rev16`, `REF_MEASUREMENTS` | 9 findings; refuted two of A's and B's headline statistics |

This is the first adversarial pass over the rev-16 loft. It was new geometry
checked only by its own author.

---

## 0. THE HEADLINE

**The loft's geometry is largely sound. Its measurement infrastructure is not.**

Three `verify` rows cannot fail. Three `STATE.md` rows publish phantoms, one of
them previously unknown. Nine of the eleven headline figures in §10.34–10.37
have no guard at all, and the one arch guard that exists subtracts two source
constants and therefore returns the same answer forever.

Two of the four defects the auditors were briefed to find **do not exist**, and
they were killed by measurement, not by argument. Two more are real, and one of
those is a refuted photograph reading that is currently built into the mesh.

---

## 1. CONFIRMED — dead guards. Severity 5.

### 1.1 `verify` row 11e, engine-lid shut line: returns 1.0000 for every input, and never worked

`verify.py:263-278` counts a sample open if `(not hit) or loc.x > -1.95`.
The rear-most body vertex is **x = −1.8730**. The threshold sits **77.0 mm
behind the entire vehicle**, so every ray that hits the tail at all scores
"got through".

```
BODY vertex bounds x[-1.8730, 2.1270]
28/28 samples counted OPEN; no sample hits anything aft of -1.3697
verify._englid_frac = 1.0000
counterfactuals:  +350 mm z -> 1.0000   -300 mm z -> 1.0000
                  +600 mm z -> 1.0000   y squeezed to 20 % -> 1.0000
```

`t1_shell.engine_lid_gap` cuts at `X_TAIL + ENGLID_CUT_DX = −1.7150` and
*expressed* it in terms of `X_TAIL`; `verify.py` kept the literal `−1.95`.
At the OLD tail station `−2.1080` the threshold was already 158 mm inboard of
the skin — **this row has never carried information at any revision.**

### 1.2 `verify` row 11d, rear window: the ray stops 177 mm short of the tail

`_ray_clear(body, (-2.40, 0, REAR_Z + _frame_dz(X_TAIL)), (1,0,0), 0.35)`
terminates at x = **−2.0500**, forward of nothing. Unbounded, the same ray
first hits at x = **+1.9738** — the windscreen, 4.3738 m away.

```
verify's bounded test = True  (True == "rear window IS cut")
controls aimed at certainly-solid metal:
   0.45 m below the rear window  -> True
   0.70 m below (tail panel)     -> True
   0.15 m above                  -> True
```

Shortfall 177.0 mm today, 58.0 mm at the old tail station. Never reached the
tail either. The rear window genuinely *is* cut; the guard did not establish it.

### 1.3 `verify` row 10, "the bus is lowered": an algebraic identity

`X_DROP_REF = (0.0650 − RAKE_Z0)/RAKE_DZDX`, then
`RIDE_DROP = RAKE_Z0 + RAKE_DZDX·X_DROP_REF`, which cancels to the literal
**0.0650 for any rake**. The row tests `|RIDE_DROP − 0.0650| > 0.005`.

```
RIDE_DROP - 0.0650 = 0.000e+00   (exactly, not "small")
RAKE_Z0 = 0.000 / 0.020 / 0.200 / 0.500  -> guard PASSES in all four
```

The stance could be reset to stock — the exact rev-4 regression this row exists
to catch — and it stays green. The quantities that describe the stance
(`RAKE_Z0 = 47.9 mm`, `rake_drop(X_AXLE_R) = 28.4 mm`) are guarded by nothing.

---

## 2. CONFIRMED — `STATE.md` phantoms. Severity 3–4.

`STATE.md` is declared authoritative over all prose. It publishes three
falsehoods.

| row | prints | truth | mechanism |
|---|---|---|---|
| overall length | `4.0648 vs 4.2900 = −225.2 mm OUT` | `+9.8 mm ok` | `audit.py:319` hardcodes `4.290`; `verify` re-expresses `SPEC["L"] = 4.290 − (O_OLD − O_NEW) = 4.0550`. The 235.0 mm gap **is** `O_OLD − O_NEW`. |
| overall height | `3.0169 vs 1.9600 = +1056.9 mm OUT` | n/a — wrong test | `audit.py:322` takes max z over ALL meshes; `lid_strut0` spans 1.8994–**3.0169**. |
| **roof z at mid-wheelbase** | **`0.3497`** | **1.9625** | **NEW — nobody had found this.** |

**The new one.** `audit.py:_roof_at(x, tol=0.045)` filters `|y| < 0.30`. The
roof opening spans x[−1.0700, 0.9640], y[−0.5450, 0.5650]. At mid-wheelbase the
**entire `|y|<0.30` window is inside the hole**, so the max is taken over
whatever else is in the slice — the rocker.

```
_roof_at(x=+0.100, tol 0.045, |y|<0.30):
   z=0.3497  n=18  argmax=(0.1200, -1.10e-10)   <-- STATE.md prints this as "roof z"
   front axle  mesh 1.9395   mid  mesh 1.9625   rear axle  mesh 1.9835
```

Error **−1612.8 mm**. The selection is non-empty (n = 18), so the `default=nan`
guard never fires. This is precisely the failure mode `audit.py`'s own rev-7
comment describes for `reach()` — *"`or -9` hid the empty selection behind a
plausible number"* — reproduced inside the function written to replace it.

**Contagion nobody flagged:** `H = 3.0169` is the denominator of four console
percentages (rocker, belt line, window sill/head, windscreen pane rise). All are
percentages of a lid strut, low by a factor **0.6497**.

`STATE.md` also carries two hand-authored paragraphs, inside a file whose header
says "Nothing in it is typed by hand", that its own tables now contradict — the
"bay widths are not equal 0.507/0.516/0.526" sentence sits four lines below the
line printing `bay widths 0.516 0.515 0.516`.

---

## 3. CONFIRMED — the rear arch. Severity 4.

### 3.1 The crown is double-counted

`t1_shell.rear_arch_outline` evaluates `z = ARCH_R − h·_arch_drop(t)` with
`_arch_drop(0.0) = 0.060`. But `ARCH_R` **is** the measured crown lip height:
SPEC §10.37 and `t1_shell.py:282-285` both state it is HELD, and
`LOFT_GROUND` §2.6 instructs *"hold the crown height, widen to 0.92 m, and use
the §2.3 profile."* Subtracting a crown drop from the crown is a
double-count.

```
h (crown-to-foot) 0.34850
z at t=0 : 0.35259  ->  20.9 mm below ARCH_R      (h * 0.060 = 20.91 mm)
mesh ray-cast at the rear axle: lip-hub 0.3550 -> tyre gap 22.5 mm
```

**§2.6 is authoritative and unambiguous. The implementation did not misread it —
it implemented §2.3 verbatim and never checked the result against §2.6, whose
text its own header comment quotes.**

### 3.2 But the statistics first reported for it were wrong, and auditor D refuted them

Auditor B reported "lip 20.0 mm low, 3.85σ, tyre gap 20–22 mm". That is the value
**at t = 0 only** — correct arithmetic, wrong feature. The outline's actual
highest point is the notch spike at t ≈ +0.10:

```
outline apex: 368.0 mm above hub at dx +0.048   (0.89 sigma from 372.6 +- 5.2)
tyre gap there: 35.5 mm   (SPEC sec.2 locks 41.0)
axle station:   352.6 mm, gap 20.1 mm
```

So: **20.9 mm low at the axle, apex 4.6 mm low and 46 mm out of place, maximum
tyre gap 35.5 mm against a locked 41.0.** The defect is real; the σ figure
originally attached to it is not.

### 3.3 And the number that "confirms" `ARCH_R` is circular

`LOFT_GROUND` §0.4 sets `k_t` partly by *forcing* the arch-to-tyre gap to
SPEC §10.29's 41.0 ± 3.5 mm, giving `k_t = 80.29/0.3735 = 214.97`. It then
adopts 215.5 and reports **the same 80.29 px** as "0.3726 against the built
ARCH_R = 0.3735 — right to 1 mm". The 0.9 mm agreement is manufactured: it is
80.29 px divided by a scale set so that 80.29 px equals 0.3735. The ±0.0052 is
nothing but `0.3726 × 3.0/215.5`.

**§10.37's "the RADIUS is right" is not an independent confirmation of anything.**

### 3.4 No guard sees any of it

`verify.py:527-529` is `gap = ARCH_R − TIRE_R` — a subtraction of two source
constants, which returns 41.0 mm forever regardless of the mesh. `audit.py:383`
prints the same subtraction under the label "measured 41".
`ARCH_W_REAR`, `_ARCH_PROFILE`, `_arch_drop` and `rear_arch_outline` appear
**0 times** in `verify.py` and **0 times** in `audit.py`.

---

## 4. REFUTED — the `(0.10, 0.014)` notch is not a measurement, and it is in the mesh. Severity 4.

`LOFT_GROUND` §2.3's table — headed *"assumption-free, use this if in doubt"* —
reads `0.014` at Δx/a = +0.10, between neighbours of 0.060 and 0.057.
Transcribed faithfully into `t1_shell.py:299`. Implemented, it puts a **16.0 mm
notch** in the lip and moves the built crown **+46 mm forward of the rear axle**,
against a header comment claiming it is centred to ~1 mm.

Auditor D re-traced it.

```
CROP BOX: cols[640,872) rows[505,604) = 232 x 99, R channel
   spans X = -0.594 m (u 640) to -1.632 m (u 872) via the projective map
   the lamppost is at cols 62-79 -- 561 columns away, it cannot enter this crop
   traced 191 of 232 columns (LOFT_GROUND reports 185 of 232)
```

Reproducing §2.1's method exactly (half-max falling crossing in a ±7-row window)
**does** give the anomaly — a 4.5 px = 20.9 mm spike at u 760–765. Then the raw
pixels:

```
row : u749 u755 u758 u760 u762 u765
520 :  204  130   80   69   61   59      <- a dark band, 5 px ABOVE the lip
524 :  133  114   96   81   76   75
525 :   38   31   23   16   12   15      <- the actual lip edge, SAME ROW throughout
```

The lip edge is at row 524→525 at every one of those columns. The ±7-row window
straddles the dark band, drags the half-max down to 72.5 and locks the estimator
onto the band. Re-anchored on the edge itself:

```
u=749 371.4 mm   u=755 370.9   u=758 371.4   u=760 372.1   u=762 372.3   u=765 372.1
```

**No notch. The lip is flat there.**

And the coincidence is exact. Through §0's map,
`Δx/a = +0.10 → x = −1.1460 → u = 759.53`. §2.1's own text says it rejected
outliers at *"u 657, **758-761**, 844-845"* as dark folk-art specks.

**The `+0.10` entry is the middle of the band §2.1 says it rejected. The 9-wide
median filter announced in §2.1 was never propagated into the §2.3 table.**

Independent internal check, needing no re-trace: §2.4 claims the crown is flat
within **1.2 mm over 164 mm**, a span containing Δx/a = ±0.178. The table's own
values across it span `0.054 × h = 18.8 mm` — **15×** that flatness. Even
discarding +0.10, 0.068 vs 0.060 is 2.8 mm, still 2.3×.

D's own flatness reproduction (9-wide median, de-sloped): 164 mm → **2.3 mm**;
209 mm → 2.9; 313 mm → 6.3, against §2.4's 1.2 / 2.5 / 4.6. §2.4 is optimistic
by ~1.4–1.9×, but its qualitative claim is CONFIRMED and either value kills the
notch.

**Authoritative: §2.4 and §2.1. §2.3's table is wrong, and wrong in a way §2.1
already knew about.**

---

## 5. CONFIRMED — the Δx sign convention is implemented backwards. Severity 3.

SPEC §10.37 and `t1_shell.py:305-307` both assert the table is stated for the
**forward** half at −0.90 and the **aft** half at +0.90. But
`rear_arch_outline` emits `(t·a, …)` and `solid_prism` is passed `u = (1,0,0)`,
and `+x` is forward. So `t = −0.90` lands **aft**.

`LOFT_GROUND` §2.3 never states a convention at all. §4's result fixes it
empirically — the anomalous `+0.10` coincides with the *aft* rejected band —
so **`+Δx` is aft and the code is mirrored**.

At the feet this costs `(0.593 − 0.583)·h = 3.5 mm`. At the notch it costs
**92 mm of fore-aft placement** on the (spurious) feature.

---

## 6. CONFIRMED — five live shut-line × aperture crossings, one on the show flank. Severity 3–4.

The import-time assertion at `t1_shell.py:391` — the one that exists because a
shut line crossing an arch lip collapsed the shell 205 562 v → 12 v for six
revisions — guards **`DOOR_GAP_S` against the front wheel arch only**:
1 of 4 shut-line outlines, 1 of 2 arches, 0 of 5 glazing apertures.

```
cab-door shut  (BOTH flanks) x bay0    151.3 mm inside, max penetration 4.31 mm
cargo-door shut(off flank)   x bay0    403.0 mm inside
cargo-door shut(off flank)   x bay2    403.0 mm inside
cargo mid-split(off flank)   x bay1    403.0 mm inside, 104.7 mm penetration
total shut line running through open apertures: 1209.0 mm
```

403.0 mm is `Z_HEAD − Z_SILL` exactly. Ray-cast confirmation on the **+Y serving
flank**, x 0.890 → 0.960 (`#` metal, `.` open):

```
z_auth 1.380 : .........................#####################################...........####...
z_auth 1.404 : ...........................................................................####...
z_auth 1.523 : .....................................................................########...
```

From z ≈ 1.40 upward the tongue of metal between the cab-door shut line and
serving bay 0 is gone; they are one hole, on the flank the customer sees.

**Provenance stated honestly: `BAY_CX`/`BAY_W` are rev 13, `CARGO_GAP` older.
Rev 16 did not cause this. The guard is what fails to see it.** Nothing
collapses — the measured correlate of the 2005-vertex collapse is skin-slope vs
extrusion axis > 0.51, which happens at a wheel-tub lip; a flank glazing lip is
perpendicular to the cut axis. This is a fidelity defect and a latent boolean
hazard, not a live collapse.

### 6.1 And the guard that would report it samples 5.2 % of its own outline

`CARGO_GAP = rrect(1.360, 1.410, 0.045, seg=6)` produces 28 points and **all 28
lie on the four corner arcs**. The straight runs carry no samples at all.

```
outline length 5.4619 m ; corner-arc length 0.2827 m = 5.2 % of the outline
straight runs carrying ZERO samples: 2 x 1.270 m, 2 x 1.320 m
sample spacing: min 0.0117  max 1.3200  mean 0.1951 m
falsification: CARGO_GAP -250 mm z -> frac 1.0000   (moved a quarter-metre, still "100 % open")
```

`gap_cargo_mid` is not in `CARGO_GAP` at all — verify never samples the
mid-split; its position and its aperture crossing are entirely unguarded.

### 6.2 REFUTED: "100 % open *because* it merged with a hole"

`_slot_frac` is monotone one-sided — a sample inside an aperture passes
trivially, so merge can only *raise* the score. But for the cab door the 100 %
is honest:

```
DOOR_GAP_S on +Y: _slot_frac = 1.0000, samples inside a serving bay: 2
frac over samples NOT inside another aperture: 74/74 = 1.0000
DOOR_GAP_S -200 mm z -> frac 0.4079   (would FAIL at 0.90)
```

The cab-door row **does** discriminate. What is true is structural and worse:
**no node anywhere in `verify.py` asserts that a shut line stays clear of another
aperture.**

---

## 7. REFUTED — "R = 2.45 stays refuted" is computed with two retired constants. Severity 5.

SPEC §10.34, `t1_core.py:445` and `HANDOFF_rev16.md:66` all state R = 2.45
"stays refuted: it needs D = 0.172, not 0.213". The 0.172 comes from
`LOFT_GROUND` §1.3's table row, computed at **`RT_ALL = 0.054`** and
**`Yt = 0.7615`**. Rev 16 changed both — to 0.0949 and 0.7273.

```
Yt (probe formula) = 0.7273    R = Yt^2/(2 CR) = 2.243    D shipped = 0.2128
At rev 16's OWN Yt and RT:   R=2.45 -> D = 0.2029
                             R=2.30 -> D = 0.2099
```

Stated uncertainty on D is **±0.035**. So R = 2.45 sits **0.17σ** from §10.34's
own datum-free measurement of 0.209 — it is not refuted at all, and **R = 2.30
reproduces 0.209 to 0.9 mm**. The section states the mechanism two lines later
("`R` here is a re-expression of `D` and moves with `Yt`") and then does not
re-evaluate the number that moved. Both original grounds are also gone:
§1.3 constraint 1 uses the 257.2 §10.34 could not reproduce, constraint 2 uses
1.960 (§8).

---

## 8. CONFIRMED — `D = 0.2116 "independently measured"` is `1.960 − 1.7485`. Severity 5.

Quoted in six places as an independent corroboration of the shipped 0.2128.
`LOFT_GROUND` §1.3's own text says what it is: *"**Crown = 1.960.** Requires
D = 0.2115."* Watched print: `1.960 − 1.7485 = 0.21150`.

It is a residual of two numbers rev 16 itself declares unusable — 1.960 comes
from `REF_MEASUREMENTS.md:157` (`ground = 668.0`, the datum §10.11 bans, which
§10.34 says in as many words) and 1.7485 from the hub chain §10.34 diagnoses as
29 mm low. **It is "subtracting two numbers in different origins", the sin
§10.35 convicts §10.7 of two paragraphs later.**

Meanwhile §10.34 contains a genuinely clean D and does not use it:
*"drip rail → roof top = 44.92 px = 0.209 m"* — a same-column differential,
datum-free. The change-log and four code comments corroborate against the
contaminated number instead.

### 8.1 `H_ROOF = 1.960` is now unsupported

Its only ground-line-free confirmation was `LOFT_GROUND` §1.2's 1.9621
("**1.960 survives**"). §10.34 withdrew that reading's interpretation and did
not note that it was 1.960's only escape from the banned datum. D re-scanned the
top edge independently:

```
CROP BOX: cols 750..818 step 4, rows[230,300), luminance, half-max RISING edge
   u[755,815]: n=15, 251.31 .. 252.70, mean ~252.0
   SPEC 10.34's "flat at 252.1-253.6"     -> REPRODUCED
   LOFT_GROUND's "proud strip 253.21+-1.2" -> REPRODUCED (inside its own band)
   LOFT_GROUND's "fixed skin 257.2+-1.5"   -> NOT REPRODUCED (5.2 px, ~3.5 sigma)
```

So the **height** 253.21 → 1.9621 m stands; only the proud-strip
*interpretation* is dead, and §10.34's wording is exact about that. But three
further numbers still lean on the withdrawn reading: `D = 0.2116` (§8),
`R ≤ 2.06` (derived from the unreproducible 257.2 — its own parenthetical
"≤ 1.82 m if the proud strip is roof skin after all" is now the operative branch
and nobody wrote that down), and the §10.9 corroboration.

**No `H_ROOF` change is proposed here. It is the owner's call and it must come
from a direct mesh probe, not from prose.**

---

## 9. REFUTED — the overhang is NOT 12.7σ out. The probe's label is wrong. Severity 2.

Auditor A found `t1_core.py:35-38` states the basis of the tail re-space as
`overhang/wheelbase = 0.3412 ± 0.0015` while shipped `O_NEW = 0.773` gives
0.3221 — **12.74σ**. Auditor D refuted it.

`verify.py:371-381` states the distinction correctly and is the best-written
passage in rev 16: *"The image ratio and the world ratio are NOT the same number
and must not be compared to each other — the flank map is projective."* It then
guards the **world** value. And 0.773 is fully sourced:

```
X(u) = 641220.4/(u+11140) - 55.0322
   X(242.84) = +1.3000    X(749.38) = -1.1000     (both LOCKED hubs, reproduced)
   X(922.2)  = -1.87271   ->  O = 0.7727          = shipped O_NEW 0.773
   X(652.4) - X(852.0) = 0.9051 m                 = LOFT_GROUND 2.5's own 0.905
```

**The geometry is right.** What is wrong is that three places juxtapose the
image ratio 0.3412 with a metric 0.4200 without the caveat, and
`probe_rev16.py:104-106` prints 0.3221 next to the label "(photo 0.3412)", which
reads as a 12.7σ failure of a model that is correct. The like-for-like image
comparator for the old tail is **0.4470**, not 0.4200.

---

## 10. CONFIRMED — `probe_rev16.py` is not what its docstring says. Severity 3.

Docstring: *"Every number below is measured on the mesh built in this same
process — not read back out of the source constants."*

- `:44-46` — `D = RT + CR` reads the source LUTs. **This is the line that prints 0.2128.**
- `:48-51` — `Yt`, `R` from `T.WX`, `T.G`, `T.CR_ALL`: source constants.
- `:60` — "aperture top (guarded band)" is the literal `1.775`.
- `:90-91` — prints `xa` against `xa`. **The crown-centring check compares a
  variable to itself and can never disagree** — while the preceding lines
  actually trace the crown off the mesh and would have shown it 46 mm away.
- `:104-106` — the mislabelled overhang ratio of §9.

The false-docstring pattern that survived nine revisions is present again, and
this time the probe is the evidence cited in the SPEC section it was written to
support.

### 10.1 What the mesh actually says about D

Auditor A probed it properly at SUB=2 (bin |y| by z, find the `y = Yts`
crossing, D = apex − crossing; zero bias on the authored polyline by
construction):

**D_mesh = 0.209 ± 0.003** against the tabulated 0.2128.

And auditor D found the two are not even the same quantity: `RT + CR` is
roll-start-to-crown, the photograph measures lip-to-crown, differing by exactly
the 3.62 mm gutter term of §11.

```
D by CONSTANTS  RT+CR                              = 0.21280
D by the PHOTOGRAPH's definition (lip -> roof top) = 0.20918
SPEC 10.34's photo value 0.209 -> agreement is 0.18 mm, not "3 mm"
```

**The model reproduces the photograph's D to 0.2 mm. The "3 mm agreement" was a
units-of-definition error understating the model's own accuracy.**

---

## 11. CONFIRMED — `RT_ALL = 0.0949` cannot be reproduced from its own derivation. Severity 3.

`t1_core.py:441`: *"roll start (gutter lip) authored 1.8027 → RT_ALL = 1.8940 −
zt0"*, which yields **0.0913**, not 0.0949.

```
zt0 = ZT_ALL(-1.100) - RT_ALL(-1.100) = 1.79910     <- the roll start
gutter lip (t1_detail.py:745-746)     = 1.80272     <- zt0 +0.01512 +0.004 -0.0155
1.8940 - 1.8027 = 0.09130      1.8940 - zt0 = 0.09490 = shipped
```

The parenthetical "(gutter lip)" and the term "roll start" name two surfaces
3.62 mm apart. The code is self-consistent; the written derivation is 3.8 %
wrong, and `RT_ALL` is now silently a function of three magic numbers inside
`t1_detail.gutter()` while being written as a bare `0.0949` at two knots.
SPEC §10.34 and `HANDOFF_rev16` state no derivation at all — so the derivation
of a shipped constant exists in exactly one place in this repo and it is wrong.

---

## 12. CONFIRMED — the cap headline mixes subdivision levels. Severity 3.

"valence > 4: 53 → 14" is rev-15 at **SUB=2** against rev-16 at **SUB=1**.

```
rev15 SUB=1: max 115  >4 = 55        rev15 SUB=2: max 110  >4 = 53
rev16 SUB=1: max   6  >4 = 14        rev16 SUB=2: max   6  >4 = 58
```

At the level the model ships at, the count went **53 → 58, up by five.**

**The half that mattered is solid.** The valence-110/115 poles are gone at both
levels, max valence is 6, valence-2 vertices collapsed 863 → 5, and the raw
Coons cap is watertight: 784 quads per cap, `edges!=2 = 0`, non-manifold verts
0, zero coincident vertices, correct outward winding both ends, max valence 4,
min face area 6.712e-05. All 14/58 extraordinary vertices come from the
booleans, not from the caps.

---

## 13. WHAT THE AUDIT REFUTED — rev 16 was right, and it is recorded

- **The `zlo` fix is real and structurally sound.** `zlo`/`zhi` recompute from
  `roof_z` live, so the margin tracks the crown automatically (verified by
  scaling `CR` ×0.5/×1/×2/×4). The historical "worked by luck by 6 mm"
  reproduces at **+6.1 mm** on the checked-out rev-15 source, and "18 mm short"
  reconciles as 20.9 mm minus the 2.8 mm solidify skin. The hole is open on the
  built mesh: **315 of 315 grid points clear**. Bottom margin 31.4 mm at SUB=2,
  ~10× the requirement, and the analytic-vs-mesh discrepancy has the safe sign
  (+1.4 to +7.7 mm) and shrinks with subdivision.
- **`vol 3.651e-01` on the roof cut is the cutter's own volume**, not removed
  material: 2.2569 m² × 0.1618 m matches the printed figure to 4 s.f. The cut's
  real bite is `v-ratio 0.9855` against a 0.95 threshold.
- **`_aft()` is exactly the identity forward of the rear axle** — 4001 samples,
  `delta 0.000e+00`, monotone over [−2.2, 2.2]. Every live station and LUT knot
  passes through it. The tail was genuinely re-spaced, not translated.
- **The n-gon cap's 1.4 mm forward pull of the flat tail face is gone**:
  **+0.014 mm mean** over 11 304 vertices, worst +0.381 mm.
- **`NHALF = 57` was chosen on a real guard result** — the 27×28 arm prints
  `!! BOOLEAN REJECTED gap_englid: zero-area faces 0 -> 2 -- ROLLED BACK`.
- **`ARCH_W_REAR = 0.920`'s aft foot lands at 313.0 mm** against the tail solve's
  independently measured 320 mm.
- **Boolean order**: set difference commutes, so only SOLIDIFY is genuinely
  order-bound (arches before solidify is what makes real wheel tubs). No cutter
  depends on a surface a later cutter modifies.
- **Nine `verify` rows do discriminate**, verified by constructing states where
  they flip: windscreen, door glass, bays, solid panel, roof aperture (the
  strongest row in the file — two-sided, 7 probes), cab-door shut line, track,
  rear overhang, roof crown.
- **The +23 mm warn is a real probe, not a composition.** `_roof_z_at` iterates
  `T1_body` vertices and excludes the lid objects. **1.9835 ± 0.0007 m**,
  probe-vs-analytic agreement 0.03 mm.

Two auditors also caught **themselves**, which is the behaviour we want:
- A's first estimator for D returned **0.1711** — a 42 mm defect that does not
  exist — because it triggered on a piecewise-linear LUT knot sitting 1 mm from
  the roll start. It looked calibrated against the authored polyline. Found,
  discarded, reported.
- A predicted `probe_rev16`'s drip-rail block could never fire, then found the
  `gutter()` it had read at line 405 is **shadowed** by a second definition at
  line 729 that does span the window. *"The rule about checking what a probe can
  see cuts both ways, and it cut me first."*

---

## 14. LOWER SEVERITY, RECORDED

- **`verify.py:499` uses `RIDE_DROP` as a frame conversion at the tail**, against
  t1_core's explicit docstring: threshold 1.8350 as written vs 1.8853
  station-correct. **50.3 mm of guard slack.** Full sweep of all 9 code uses:
  one frame error (this), one tautology (row 10), one dead
  (`audit.py:235` — real frame error, `_ap` assigned and never read, twenty
  lines of dead measurement code), six legitimate (two verified at
  `d = 0.000e+00` and `−5.55e-17`). Lead flagged `audit.py:235` as live; **refuted.**
- **8 of 12 `STATE.md` "Measured dimensions" rows compare a constant to a
  re-typed copy of itself** and print `+0.0 mm ok`. The sill/head rows are
  structurally incapable of moving. Only tyre diameter and overall width are
  live in that table.
- **`verify.py:675` `V_APEX > 0.3960` and `:670` `V_APEX + V_RISE != Z_BELT`
  cannot fail** — both duplicate `t1_mats` import-time asserts that would have
  raised first. `SPEC["H"] = 1.941` is **never read**; twelve lines of frame
  reasoning protect a number nothing tests.
- **`SOLID_PROBE_X`'s comment is stale by 104.2 mm** (rev 13 moved the bays), and
  its aft-most probe is now only **73.0 mm** forward of the rear-most sheet
  metal, down from 308 mm before the tail re-space. Nobody watched that shrink.
- **`_retired_section_drift` detects only a change in bullet count** (16 vs 16).
  Replacing a bullet in place leaves it silent. It is also a warn, not a fail.
- **`verify.py`'s frame comment contradicts itself** — line ~540 says `run()`
  executes BEFORE step 8b; the header, 11d2 and `build.py:590` all say after.
  The code is right; the comment is the class that has produced this bug 3×.
- **Needle slivers survive at SUB=2 and no guard can see them.** `ZERO_AREA =
  1e-12` is an **area** threshold; the shortest edge is **0.36 µm** on a face
  spanning 13.3 mm, aspect ratio 1.9e6, area 9.45e-11. 25 coincident vertex
  pairs < 10 µm. These come from the boolean cutters, not the caps. Rev 16
  improved the class substantially (863 → 5 valence-2); the point is that area
  is the wrong statistic.
- **The shipped 28×28 arm leaves 4 well-formed 0.12 mm triangles** at the
  engine-lid gap. Not slivers (aspect 3.5), but the symmetric cap does not
  eliminate degeneracy there — it converts 2 zero-area faces into 4 tiny ones.
- **`roof_z`'s `min(|y|/Yt, 1.0)` clamp** is the roof cutter's one absolute
  limit and it fails in the *unsafe* direction. Headroom today: `LID_W` could
  grow 162 mm before a corner leaves the crown parabola. Unguarded.
- **`folk_gen.py:220-227` re-types four t1_core constants** under a header saying
  they are read off t1_core: `X_TAIL` **235 mm stale**, `RAKE_DZDX` **15.3 mm/m
  stale** (rev 13 rejected 0.0330 at 4.5σ), `RAKE_Z0` 11.4 mm stale. The file's
  own "MAPPING CONTRACT BROKEN" self-check does not cover these four.
- **Dead-but-present aft constants in `t1_core`**: `X_BUMP_R = −2.140` (tuned
  32 mm behind the OLD tail skin), `BED_STATIONS`, `ZT_BED`/`RT_BED` aft knots
  not re-spaced. All verified unreferenced — `ZT_CAB`/`RT_CAB`'s single external
  reference is inside a `def gutter()` that is shadowed.
- **`verify` row 11f see-through covers 2 of 4 shut lines.** The cargo gap
  **is** see-through at 10 of 28 samples and nothing reports it.

---

## 15. PRECISION SWEEP — figures quoted beyond their method

| figure | ceiling |
|---|---|
| `0.3412 ± 0.0015` | omits the front hub's own 2.40 px fit rms. Propagated: **±0.00204**. The missing term is the largest one. |
| `0.773 ± 0.022` | excludes §3.4's own near-corner-vs-centreline bias, "< 15 mm", never added anywhere. |
| `0.3726 ± 0.0052` | ±0.0052 is only `k_t`'s ±3.0/215.5 — 1.1 px on a 2.32 bit/px JPEG, and `k_t` is partly forced by the quantity being confirmed. |
| `ARCH_W_REAR = 0.920` | §2.5's own preferred projective route gives **0.905**. 15 mm of unlabelled choice. |
| "aft foot to 1.5 mm" | §10.35 gives **both** feet: aft 1.5 mm, forward **16.5 mm**. The change-log quotes the better of two. |
| `D = 0.2128` | the mesh/photograph definition gives **0.2092**. Quoted to 0.1 mm against a stated ±35 mm. |
| "starburst 3.015 → 1.609 (−47 %)" | 4 s.f. on a 32-sample render, but the negative control (1.596 → 1.592) bounds reproducibility at ~0.25 % — **marginally supported.** The one over-precise-looking number that survives. |

---

## 16. GUARD TALLY

Of the **eleven headline figures** in §10.34–10.37:

- **1** has a guard that measures the mesh — the rear overhang
  (`verify.py:365-390`, correctly built, and the one passage that states the
  image-vs-world distinction properly).
- **1** has a guard that subtracts two constants and cannot fail — the
  arch-to-tyre gap.
- **9** have no guard at all: `ARCH_W_REAR` 0.920, the profile table, the crown
  centring, max valence 115→6, valence>4 53→14, `NHALF`/`NLOOP`, the starburst
  3.015→1.609, the 27.7 mm drip-rail differential, `D = 0.2128`.

Of `verify`'s ~20 rows, **four are decoration** and three of those four are
shut-line/aperture rows printing a reassuring "100 %".

---

## 17. WHAT WAS NOT CHECKED, AND WHY

- **SUB=2 for auditor C.** All guard measurements are SUB=1. The project's own
  warning is that guards behave differently at SUB=2.
- **`t1_detail.visibility_fails()`**, imported by verify and added to `fails` —
  not audited.
- **Whether 1.9835 m is *right***. That is photogrammetry on `ref_side.jpg` and
  no auditor would quote a figure it did not derive.
- **§2.4's 0.2 px crown centring.** One pixel is 4.64 mm here; a local parabola
  on a flat crown is ill-conditioned (apex u 741.5, residual sd 3.1 mm).
  Neither confirmed nor refuted, and no centre is quoted. The *code* violates it
  regardless.
- **The front arch's true shape and width.** No measurement exists — a man
  occludes it in `ref_side.jpg`. The cost of leaving it circular, **conditional
  on the two pressings matching**, is: aperture 173 mm too narrow on the chord,
  87 mm per side of wing the circle does not have at all, and at |Δx| = 0.30 m
  the circular lip sits **87 mm** below where an ogee would put it.
- **Re-ordering the booleans** — would require editing `build.py`; read-only brief.
- **Visual consequence of the aperture crossings** — renders barred on a 2-core box.
- **Tangent continuity across the cap junction.** The cap is planar in x and the
  adjacent ring is 4.98 mm forward, so there is a hard crease by construction at
  every revision. Separately: `G` is piecewise-linear, so the flank has C⁰ slope
  breaks at every knot, and the flank→roll junction has a 9.3° tangent break.
  Both pre-date rev 16 and are unchanged by it.

---

## 18. THE ORDERED RESPONSE

Nothing below is applied. This document is diagnosis only.

1. **The three dead guards** (§1). Cheapest, and until they are fixed no future
   "0 fail" means what it says. Express each threshold in terms of the constant
   it shadows — `X_TAIL`, not `−1.95`; the tail station, not `−2.40`.
2. **The three `STATE.md` phantoms** (§2), including the new mid-wheelbase one
   and the four contaminated percentages. `STATE.md` is the file declared
   authoritative; it must stop publishing falsehoods.
3. **The arch double-count and the refuted notch** (§3, §4, §5). These are live
   geometry. Removing the notch and holding the crown are one change, and the
   sign convention must be settled in the same pass or the fix lands mirrored.
4. **A guard for the arch** — one that measures the built lip, not two constants.
5. **The shut-line × aperture invariant** (§6) — generalise the `t1_shell:391`
   assert to all four outlines against all arches and apertures, and give
   `CARGO_GAP` samples on its straight runs.
6. `probe_rev16.py`'s docstring and its `xa` vs `xa` line (§10).
7. The prose corrections: `R = 2.45` un-refuted (§7), `D = 0.2116`'s provenance
   (§8), the derivation of `RT_ALL` (§11), the level-mixed valence count (§12),
   the overhang label (§9).
8. **`H_ROOF`** — unchanged, and now known to rest solely on the banned ground
   line. Direct mesh probe only, and the owner's call.

**If a change trips a guard, do not widen the guard.**
