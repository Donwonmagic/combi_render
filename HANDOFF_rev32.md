# HANDOFF — rev 32

**NO GEOMETRY MOVED. NO SHADER MOVED. NO ARTWORK MOVED.** `CREAM`,
`COUNTERTAN`, `COUNTERCREAM`, `RED`, the rake, the roof, the over-rider bar and
all three textures are UNCHANGED. The last geometry change is still rev 30's.

---

## 1. How rev 32 opened

- **Step 0 worked, and this time it needed nothing.** `get_device_info` returned
  `~/Desktop/tacombi_bus_render` already in `connectedFolders` on the first
  call. rev 30 and rev 31 both had to request and were both granted; rev 32 did
  not have to request at all. **KEEP STEP 0** — it costs one call and it has
  now been the difference between a lost hour (rev 28) and lost minutes (rev
  29, 30, 31) four times.
- **The bridge's ~3 MB throughput ceiling reproduced exactly as briefed.** Two
  files needed splitting — the 19.5 MB base bundle (7 parts) and the 8.5 MB
  `rev14_unified` (3 parts); everything rev15–rev31 crossed whole.
  **md5 matched on both sides** for all four checked files.
  **~9 bridge calls in total.**
- **Two failures inside one 19-file batch, both transient.** `rev30` and `rev31`
  returned `upload failed` in a batch that carried the other seventeen; both
  crossed on a single individual retry. One `device_bash` call died on a
  Cloudflare **502** and worked on retry. **No retry loop was entered.**
- **Restore CLEAN and every count exact:** 34 → 59 → *(fetch rev14b)* → 67 → 71
  → 75 → 81 → 87 → 93 → 96 → 101 → 105 → 107 → 115 → 120 → 126 → 130 → 135 →
  148 → **158, clean tree.** No divergent-branches stop.
- **45/45 content greps exact, 10/10 ancestry, 3/3 texture md5s**, all read off
  the console, none typed from memory. Both guards **0 fail / 0 warn at both
  levels on arrival**, every geometry figure identical to rev 31's table.

---

## 2. SPEC 10.86 — the sweep §10.85 did not do

§10.85 corrected REF §9's V-apex anchor in place (`311.5` → `288.8 ± 3 px`) and
wrote *"everything in this file that used 311.5 as the centreline inherits
this."* **It did not chase the consumers.** rev 32 grepped the whole tree.

| carrier | defect | disposition |
|---|---|---|
| `REF_MEASUREMENTS.md` §9 anchor line | — | already corrected by 10.85 |
| `REF_MEASUREMENTS.md` §9 absolute heights | **`V-SWAGE APEX ~0.49 m` consumes BOTH coordinates of 311.5** | WITHDRAWN as a reading, replaced by a bracket |
| `SPEC.md` §10.75 in-place annotation | **read "REFUTED" a whole revision after 10.84 downgraded it, AND on the wrong anchor** | corrected in place |
| `t1_detail.py` above `overrider_bar()` | same two defects, in shipped source | corrected; original kept as the record |
| `probe_orb_post.py:58` | `V_APEX_U = 311.5` | **kept deliberately**, corrected anchor added beside |

**THE ABSOLUTE-HEIGHT CONSUMER.** REF §9's *"49 px above the bumper top **at the
same image x, hence the same depth**"* uses 311.5 twice. The **ROW**: 49 px is
`718 − 669`, and 669 is not the apex row; the arms cross at `v = 701.1` and the
radiused tip sits above that, so the apex is bracketed `669 < v < 701.1` —
**16.9–49 px, ≈0.40–0.49 m above ground. The published 0.49 m is the TOP of a
bracket.** The **COLUMN**, worse: the "same image x" pairing existed *because*
both readings shared 311.5, and the apex is at 288.8.
**NO REPLACEMENT NUMBER IS PUBLISHED** — re-deriving needs the blade's top
boundary at `u = 288.8`, and **the blade and the V-swage are BOTH CREAM**, so a
cream-run scan cannot find it. Gap named, not filled.

**NEGATIVE SWEEP RESULT, worth carrying:** the other three entries in that block
do NOT consume 311.5 (V arms ← flank belt line; headlamp ← the V arm at its own
x; indicator ← the headlamp). And **`422 px/m` is consumed nowhere in the
tree** — named once, in rev 29's carry-forward, only to warn against it.

---

## 3. §10.84's ARM 2 WOULD NOW PASS — and that is a defect finding

§10.84 reported a clean failure: roundel `306.0` vs apex `311.5` = `+5.5 px`
against `±4 px`, **1.38 σ, C4 FAIL**. On the corrected anchor:

    288.8 − 306.0 = −17.2 px  →  5.73 σ on the ±3 px SYSTEMATIC band
                                 and it clears 10.85's ±7 px worst case too.
    THE SIGN ALSO FLIPS.

**IT IS NOT LEANED ON.** Re-reading the arm once its gate might pass shows two
terms it never had:

1. **NO DEPTH-ORDERING TERM** — a column difference is a magnitude, not a
   direction, until you know which feature is nearer.
2. **NO HEIGHT TERM** — the features are ~150 px apart in `v`, and a centreline
   point's column depends on height unless the camera is level and unrolled.

Both were present in rev 31 and invisible then, **because C4 failed and nothing
downstream of it ever ran**. New rule: **A CONTROL THAT FAILS CAN HIDE THE
DEFECTS DOWNSTREAM OF IT.**

`probe_orb_post.py`'s 311.5 is deliberately left so the file reproduces rev 31's
published result — **a probe that cannot reproduce its own published result is
not a record** — with the corrected arm printed beside it.

**§10.83's centreline claim stays UNDECIDED.** The `_RETIRED_VALUES` row is KEPT
for the third time, reason corrected; the offset is **76.7 px**, not 54.0.

---

## 4. The POST — ruled out BEFORE the revision was spent

`probe_orb_xratio.py` (NEW, read-only). The brief asked for the post as a
fraction of the bar's half-width, for the transverse VP to be bounded or
constructed, and for a go/no-go first.

**The construction was the right shape.** Four collinear points in the BUMPER
PLANE carry a projective invariant — no VP, no scale, no depth, no camera model
— and all four are in the same plane, which **repairs §10.84's objection at the
root**. rev 31's owner reading is what guarantees the plane.

**RULING: IT WILL NOT CLOSE, AND ON EXACTLY ONE TERM.**

| control | result |
|---|---|
| **P1** estimator exact on a synthetic map | worst error **3.55e-15** over five planted values |
| **P1b** GRADED UNTIL IT FAILS | 1 px → 1.4 %, 4 px → 6.2 %, **8 px → 14.3 %**, 15 px → 44 %, **29 px → NO REAL ROOT** |
| **P2** roots reciprocal, one physical | product 1.000000000000, 0.6260 / 1.5974 |
| **C3** columns under a five-threshold sweep | post `355.0–376.0` (centre **365.5**), right edge **0.5 px**; hoop **485.0**, **0.0 px** |
| **C4** near/far from the vehicle's own corner | hoop 485.0 > post 365.5; REF §9's "near side" agrees |
| **C5 KILL** far end swept over rev 31's blob | `203→0.578  209→0.616  215→0.666  221→0.739  228+→ORDER BROKEN`. **28 % swing. FIRES.** |

**THE ~29 px IS NOT "THE STATED PRECISION" ON THIS ROUTE; IT IS FATAL TO IT.**

**A SECOND ROUTE WAS MEASURED AND NOT PUBLISHED.** The transverse VP by harmonic
conjugate off the two headlamps — legitimate because **the transverse VP is
shared by every lateral line regardless of height, so it transfers into the
bumper plane without the vehicle's YAW**, which is what killed rev 31's ARM 1.
Near headlamp `u ≈ 419`, far `u ≈ 236`; with the corrected apex that gives
VP `u ≈ 111` and a bumper-plane centreline near `u ≈ 266`. Withheld for three
stated reasons: the far headlamp's dark region runs into the nose's own
silhouette (±5 px there alone moves `f` by 9 %); four row-wise VP estimates off
the V arms scatter over **154 px**; and the bar-symmetry assumption's only check
disagrees at **17 %**, inside the blob's own confounding — neither a refutation
nor a corroboration.

**NO VALUE OF `f` IS PUBLISHED. THE POST STAYS UNBUILT.** It is blocked on ONE
COLUMN and it is a column measurement cannot reach — a superposition is not
resolvable by thresholding it. **That is why rev 32 spends a QUESTION on it and
not a third estimator.**

**§10.75's POINTER IS VINDICATED.** `357–374` was a pointer rev 30 took a number
from; re-measured properly it is **`355–377`, centre 365.5** — right to within
2 px. The number survives; the process defect stands.

---

## 5. The two questions, and what validating them changed

`mark_rev32_q.py` (NEW) → `rev32_q1_barend.png`, `rev32_q2_surfaces.png`.
`probe_rev32_pointer.py` (NEW, read-only) validated Q2 before sending.

**Q1 — where does the over-rider bar end, on the far side?** Five CANDIDATE
LINES at `u = 205 / 212 / 219 / 228 / 240`, at ×9 and again at ×4 beside the two
measured columns. **They are candidate lines — NOT pointers, NOT sampling
windows.** No number is taken from any of them. *"If none of them is right, say
so"* is on the figure, because rev 31's rule stands.

**Q2 — do the bumper top, the rim face and the hub cap carry dust?** §10.82's
named gap, owed since rev 29 and skipped by rev 30 and rev 31. **B1/B2/B3 are
POINTERS.** Photograph beside the current build with the film OFF and the same
build with 0.7313 restored.

**THREE THINGS CHECKED BEFORE ASKING, TWO OF WHICH CHANGED THE QUESTION:**

1. **THE WORK LIST'S OWN DESCRIPTION IS WRONG.** rev 29, rev 30, rev 31 and the
   rev-32 brief all say *"the workshop frame shows all three"*. **It does not.**
   In `ref_workshop.jpg` **both road wheels are bare painted rims with no hub
   cap** — conversion stage. The red VW-logo caps exist only in `ref_side.jpg`.
   B2 and B3 moved frames. **A FEATURE NAMED IN A WORK LIST IS A PROBE TOO.**
2. **THE QUESTION IS WORTH ASKING, MEASURED NOT ASSUMED.** The retired lever
   reaches **0.4500 m²** rim barrel + **0.2100 m²** hub cap + **0.0909 m²**
   `bumper_f` = **0.751 m²** against `T1_body`'s 12.294 — about 6 %, on three
   surfaces at the front of every hero frame.
3. **THE VALIDATOR CAUGHT MY OWN BOX.** rev 29's statistic and rev 29's two
   anchors, **band unchanged**. My first hub-cap box read **8.77×** — closer to
   a PROVEN straddler (13.54×) than to an ANSWERED box (3.14×); it sat on the
   specular highlight. **Moved, not excused.** Then **7 of 8 cap boxes fail**,
   which is a fact about the cap (a dome with the wheel-arch shadow's EDGE
   across its lower half; a quadratic absorbs a gradient, not an edge). All
   eight printed. Final **B1 1.96×, B2 1.81×, B3 2.78×, 10 controls, 0 failed.**

**CEILING, STATED:** rev 29's anchors both live on `ref_rear34.jpg`; two of
these boxes do not, and **there is no answered anchor on `ref_side.jpg` at
all.** Not load-bearing only because these are pointers.

---

## 6. An unsought defect: a control failing since rev 30

`probe_dust_scope.py:249` hard-coded *"audit.py publishes 185"*. rev 30 added
`orb_bar`, taking the count to **186**, and the literal was not swept. **The
probe has been failing one of its own eight controls since rev 30, and neither
rev 30 nor rev 31 ran it.** Found while validating an owner question. The
literal is corrected, not the check loosened. **A CONTROL NOBODY RUNS IS NOT A
CONTROL.** Now **8 checked, 0 FAILED**.

---

## 7. Guards and falsification

| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 0 warn** | **0 fail, 0 warn** |
| audit.py | **0 fail, 0 warn** | **0 fail, 0 warn** |
| roof crown @ rear axle | 1.9835 | 1.9833 |
| arch lips | 0.3722 → 39.7 mm / 0.3732 → 40.7 mm | same |
| rake | 17.75 mm/m | same |
| cut roof hole | 68564v | 252749v |
| objects / meshes | 127 / 186 | 127 / 186 |
| over-rider row | 97.51 mm, dia 24.97 mm | same |

**FALSIFIED IN FIVE ARMS:**

| arm | result |
|---|---|
| control, clean tree | 0 fail, 0 warn |
| `W_DUST_FAC_UP` → 0.7313 in source | **hard `AssertionError` at import** |
| `BAR_RISE` +3 mm | **2 fails** |
| retired phrase into SPEC's **frozen front matter** | **1 fail** |
| `overrider_bar()` deleted from `build.py` | **1 fail** |
| `probe_dust_scope` literal reverted to 185 | **control FIRES** |

**THREE OF MY FIRST ARMS WERE NO-OPS AND I CAUGHT THEM.** Two `sed` patterns
missed their lines; one injected the retired phrase into a **§10 body**, which
`_retired_value_drift` states in its own ceiling it cannot see. All three read
as "0 fail" — **AN ARM THAT DOES NOT APPLY IS INDISTINGUISHABLE FROM A GUARD
THAT DOES NOT FIRE.** Re-run properly; only the real results are published.

**COMMIT BEFORE FALSIFYING was obeyed.** Every arm ran after commit 159, so no
`git checkout` could eat uncommitted work. rev 31 lost a whole SPEC section that
way.

---

## 8. Things rev 33 must not silently undo

- `probe_orb_post.py`'s `V_APEX_U = 311.5` is **deliberate**. Do not "fix" it —
  it is what keeps rev 31's published 1.38 σ reproducible. The corrected value
  lives beside it as `V_APEX_U_R32`.
- The stale text in `SPEC.md` §10.75 and `t1_detail.py` is **kept and annotated,
  not deleted** — it is the record of what rev 30 believed.
- **No value of `f` exists. The post is UNBUILT.** Do not build it from
  anything in `probe_orb_xratio.py`; that file rules a route OUT and publishes
  no position.
- REF §9's V-swage absolute height is a **BRACKET (≈0.40–0.49 m)**, not a
  reading. Do not quote 0.49 m as a measurement.
- `probe_dust_scope.py`'s mesh literal is now **186**. It must move again the
  next time geometry is added, and that is now a known trap.
- Everything rev 31 §6, rev 30 §3 … rev 18 §4 protects still stands in full.
