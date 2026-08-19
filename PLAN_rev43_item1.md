# ITEM 1 — THE ART FRAME AND THE BODY'S MISSING UV LAYOUT
## The written plan the brief requires before a line of code

**Status: PLAN ONLY. No code written, no texture re-baked, no md5 moved.** The brief is explicit
that half a re-bake is the worst state this project can be in — textures moved, the tripwire fired,
and no SPEC §10.10 report to show for it — so nothing starts until the decisions below are settled.

---

## 1. THE PLAN'S FIRST DECISION, ANSWERED FROM THE CODE

The brief states it as the thing to decide before anything else:

> **THE PLAN'S FIRST DECISION IS WHETHER THE NEW UV LAYOUT REPRODUCES THAT AFFINE MAP ON THE
> FLANK — so `folk_gen` survives — OR REPLACES IT, so `folk_gen` is re-authored and every §10.10
> target re-measured.**

**ANSWER: REPRODUCE. And it is not a close call — it is nearly free.**

The mechanism, read from `t1_mats.body_paint` rather than from prose. `TexCoord.Object` feeds a
Mapping node with `Location (0.185, 0.410, 0.263)` and `Scale (0.26, 0.26, 0.26)`, whose output
drives `swirl.png` and `swirl_b.png` at **`projection='BOX'`, `blend=0.10`**. BOX projection picks
the dominant axis of the face normal; on a flank face (normal ±Y) it samples **(x, z)**. So on the
flank the map is:

```
    u = U0 + SGN · 0.26 · x        v = 0.263 + 0.26 · z
    U0 = 1 − MAP_LOC[0] = 0.815, SGN = −1   on the show (+Y) flank
    U0 =     MAP_LOC[0] = 0.185, SGN = +1   on the off  (−Y) flank
```

**That is a pure affine function of world (x, z), and it is exactly what a planar UV projection
computes.** Assigning each flank vertex `uv = (U0 + SGN·0.26·x, 0.263 + 0.26·z)` reproduces the
existing map **identically**, including over the tumblehome and the swage, because BOX already
ignores y on a Y-dominant face. No re-authoring. All 2455 lines of measured composition keep their
meaning, `folk_door.md`'s numbers keep their meaning, and **every §10.10 target stays comparable to
rev 25's published run.**

**Replacing the map would cost everything and buy nothing.** It is rejected.

---

## 2. WHERE THE 56 % ACTUALLY COMES FROM — AND IT CHANGES THE SIZE OF THE JOB

**MEASURE THIS FIRST. IT IS THE CHEAPEST THING IN THE PLAN AND IT MAY HALVE THE WORK.**

`build.py` line 232: `sol = body.modifiers.new("sol", 'SOLIDIFY')` with `sol.thickness = 0.0028`.
The shell is solidified to **2.8 mm**, which gives every outer face an inner twin. The inner twin's
normal is roughly opposite — so on the flank it is **still Y-dominant**, BOX still samples **the same
(x, z)**, and it therefore lands on **exactly the same texels as the outer skin**.

`probe_rev42_uv` splits the two tiles on `sideY = Y > 0.0` — the **sign of POSITION**, not of the
normal. The probe's own note says why: *"if the split were on the NORMAL rather than the POSITION,
the solidified shell's INNER skin would go to the other tile and the compared sets would not be the
ones the renderer uses."* Correct for fidelity to the renderer — **and it means the inner skin is
inside the measured set and is counted in the self-overlap.**

**So an unknown but potentially large share of the headline figure is a 2.8 mm shell that is never
visible in any render.** The per-image figures are consistent with that being a big part but not all
of it: `swirl` **83.04 %**, `swirl_b` **48.36 %** — an inner-skin-only story predicts roughly 50 %
for both, so `swirl` carries an additional ~33 pp of genuine collision from other Y-dominant surfaces.

> **ACTION 0, before any code: re-run the overlap measurement with the inner skin excluded, and
> publish the decomposition — (a) inner-skin duplication, invisible; (b) genuine visible collision.**
> This is a read-only measurement. It costs one probe run and it determines how much of §10.101 is
> a real defect versus an artefact of counting a hidden shell.
> **It also does not let the layout off: even invisible faces must own disjoint UV territory, or the
> next person to make that shell visible inherits the collision.**

---

## 3. THE TWO MECHANISMS ARE NOT THE SAME EDIT — and confusing them is the trap

SPEC §10.101.7: they *"should be done together, and neither should be done alone."* That is the
**schedule**. It is not a statement that they are one change. They are two:

| | the ART FRAME | the UV LAYOUT |
|---|---|---|
| what is wrong | `DOOR_H` is rev 41's; the door is 272.2 mm / 387.5 mm deeper | `T1_body` has no UV layout; BOX projection is multi-valued |
| where | `folk_gen.py`, symbol `DOOR_H` | `t1_mats.py` `body_paint`, plus a UV pass in the build |
| fixed by | re-running `folk_gen` | rewriting `body_paint` and adding UVs |
| does re-running `folk_gen` fix it | **yes** | **no — it changes 0 % of it** |

---

## 4. THE ART FRAME — AND THE OWNER'S ANSWER CREATES A PROBLEM `DOOR_H` CANNOT EXPRESS

Asked whether the paisley reaches the door's own bottom edge, the owner answered **"reaches the
bottom edge"** — the art scales *with* the door.

**But `DOOR_H` is a single scalar multiplier — `h = sv * DOOR_H`, twice in `folk_gen.py`, and there
is no `/ DOOR_H` anywhere.** (SPEC §10.100.6 calls it a *divisor*; the code says otherwise, and
§10.73's own arithmetic — *"−4.200 mm, −0.41 % on every v"*, same sign — agrees with the code. **The
SPEC wording is wrong in two places and should be corrected in the same revision that acts on it.**)

**The door's added depth is NOT uniform: 272.2 mm at the rear corner, 387.5 mm at the front.** A
single scalar cannot map a rectangle onto a non-rectangular outline. So "the art scales with the
door" cannot be executed as `DOOR_H: 1.013467 → ~1.40`. Doing that would be right at one corner and
**115 mm wrong at the other.**

**What follows instead:** the door art's extent must be driven by **the door's own outline** — the
same `z_bot(x)` construction §10.100.4 already builds from `ZB`, `arch_z`, `ARCH_R` and
`DOOR_ARCH_G` — rather than by a scalar height. `folk_gen` already parses `t1_shell` for the door
frame, so it can parse the outline too. That keeps rev 25's rule intact: **one lever, and the lever
is the outline, not a second hand-tuned constant.**

**AND ONE QUESTION REMAINS FOR THE OWNER, because two readings of his answer differ by ~38 %:**
does the art *stretch* to fill the deeper door (every motif ~38 % taller), or does it keep its
drawn scale and *extend further down* (more motifs, same size)? The photograph cannot settle it:
the only frame showing the door's full outline is `ref_nolita_doorshut.jpg`, and **that bus carries
no folk art at all.** This must be asked before the bake, not after.

---

## 5. THE UV LAYOUT — the build steps, in order

1. **UV pass on `T1_body`, after solidify and after the apertures are cut**, so island assignment
   sees final topology. `build.py`'s pipeline order is load-bearing and must not move: *loft →
   subsurf → nose swage → arches → solidify → apertures → gaps*.
2. **Classify faces into groups by normal dominance and position**: show flank (+Y), off flank (−Y),
   inner skin (either side, by shell membership), nose, roof, tail, underside.
3. **Show and off flank: assign `uv = (U0 + SGN·0.26·x, 0.263 + 0.26·z)`** — the contract,
   reproduced exactly. `folk_gen` output is then valid unchanged.
4. **Every other group: assign disjoint territory** outside the painted region, so nothing collides.
   The inner skin gets its own, not "none" — an unassigned island is a collision waiting to happen.
5. **Rewrite `body_paint`** to read `UVMap` instead of `TexCoord.Object` → Mapping → BOX. The Mapping
   node's constants stay as the authored record of where the map came from.
6. **`check_mapping_contract()` must be extended.** It currently regex-reads `t1_mats.py` for the
   Mapping node's Location and Scale and **only WARNS**, never raises. Once the map lives in UVs, it
   must verify the UV assignment instead — and it should **raise**, not warn. A bake against a
   broken contract lands the art at the wrong body station and nothing stops it today.

---

## 6. ACCEPTANCE — what this must report against, and where those targets really live

**The brief says report against "§10.10's own targets". §10.10 CONTAINS NO NUMERIC TARGETS.** It is
a hard bar, an eight-row scope table and a method requirement. The de-facto template is **§10.68,
rev 25's own re-bake report**, and that is what this will report against:

| quantity | rev 25 before → after | rev 43 must publish |
|---|---|---|
| door ink past the true rear shut line | 3 411 → 0 px | ✔ |
| sill LUT max error over the body | 76.222 → 0.000000 mm | ✔ |
| flank density rms, show / off | 3.59 → 3.58 / 3.98 → 3.96 | ✔ |
| zone residuals R1 / R2 | −0.44 → +0.29 / +0.58 → −0.14 | ✔ |
| door gold, target 29.08, spread 28.96–29.19 | 29.09 → 28.90 | ✔ |
| self-overlap, per image and total | — | **new: expect → ~0 %** |
| all eight texture md5s | — | ✔ in the same commit |

Plus: `probe_rev42_uv` re-run, and **the eight md5s in `verify_clone.sh` updated IN THE SAME COMMIT
as the new artwork** — never a separate one, because that is how a tripwire becomes a rubber stamp.

---

## 7. WHAT WOULD MAKE ME STOP

- The owner has not answered the stretch-versus-extend question in §4.
- Action 0's decomposition shows the visible collision is small enough that the re-bake's risk
  exceeds its gain — in which case the **UV layout still ships** (it costs no artwork change) and
  the art frame waits.
- `check_mapping_contract()` cannot be made to raise before the bake runs.

**None of those is a reason to start and stop halfway. All of them are reasons not to start.**
