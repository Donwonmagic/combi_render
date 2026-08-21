# PHOTOS WANTED — rev 49

**He was asked at rev 49 and answered: "Neither is possible right now."** So this list is not a
request queue any more — it is a **record of exactly what each frame would unblock**, ranked, so that
when one *does* become possible the next context knows precisely what to do with it and does not
re-derive the case.

**RULE 13 IS DISCHARGED HERE, PROPERLY, FOR THE FIRST TIME.** The reference set is **TEN distinct
vehicle frames, not fifteen** — five files are byte-identical duplicates:

```
IMG_3842.png  = ref_playa_34.png          IMG_2054.jpeg = ref_nolita_flank.jpg
IMG_2053.jpeg = ref_nolita_front34b.jpg   IMG_2060.jpeg = ref_nolita_front34.jpg
IMG_3840.jpeg = ref_nolita_doorshut.jpg
```

**And they are THREE artwork states, not two vehicles** (§8 of the ledger). Do not count a duplicate
as corroboration, and do not take artwork off a Nolita frame.

---

## 1. THE TAIL BOARD'S FOOTING — **NEW, AND IT IS NOW THE TOP ITEM**

**What it settles:** the board's **width across the vehicle**, its **lateral position**, and the
**80 mm inconsistency in its foot** — three unknowns, one frame.

**Why it cannot be settled from what we hold, precisely.** The board's plane contains the lateral
direction, so its width projects **only through parallax**: 33.5 px per metre, and being a cross
product that coefficient is **identical at base and tip, so the projected width cannot taper**. The
observed silhouette *does* taper (19.9 px at the base, 7.2 over the last 40 columns), which means the
thickness also carries the board's own material and its rim band, and at 1024 px they cannot be
separated. That gives a **safe upper bound of W ≤ 0.59 m and no lower bound at all**.

**And the foot does not close.** The near-edge read puts the base on the drip-rail line to 1 px; but a
board based at rail height and spanning laterally is buried by the **80 mm of roof crown over its
inboard span**. Both cannot be true. Rev 49 built it standing clear — the choice that makes the stay's
measured triangle land on the body — and **declared the 80 mm rather than hiding it**.

**`SPEC.md:937` §10.28 has demanded exactly this frame since rev 12** — *"if it is revisited, it needs
a photograph that shows its footing, not another inference"* — **and nobody ever asked him for it.**

*The shot:* the tail from **slightly off the centreline and slightly BELOW the board**, so its
underside and its mounting are visible, with the roof in frame for scale. A frame with the roof lid
**CLOSED** is worth more than one with it open.

---

## 2. THE "100 % CALIDAD" DECAL — SQUARE ON, AND **NOT BLOWN OUT**

**Settles five open items:** the word gap, the spike count and character, the star count, the burst
colour, and *"the lettering looks off as well"*.

**Rev 49 tried to dissolve this request and FAILED ITS OWN CALIBRATION.** The attempt is recorded
because the failure is the evidence:

```
                        synthetic (geometry known)     real ref_side.jpg
  gap/cap, th 0.22-0.38   0.304 ... 0.318               0.167 ... 2.25
  vs ground truth 0.3114  2 % error, FLAT PLATEAU       158 % error, NO PLATEAU
  spread max/min          4.4x                          13.5x
```

Built at `ref_side.jpg`'s exact resolution **and its exact 4:2:2 JPEG subsampling**, the estimator
recovers a known gap to **2 %** with a flat plateau. On the real frame it has **no plateau at all**.
**The photograph, not the method, is the binding constraint.** Rule 22, applied and obeyed.

**The specific defect is DYNAMIC RANGE, not resolution.** `ref_side.jpg` already has the pixels — the
burst is **100 × 78 px**, 2.7× the area of `IMG_2073` and **8.6×** `ref_playa_34`. What it lacks is
range: **60.8 % of the white lettering is clipped**, against 9.0 % in the green frame.

*And chroma subsampling is NOT the limit* — forcing the chroma to true half resolution changes the
recovered component count by one and the type area by eight pixels.

*The shot:* **the same shot as `ref_side.jpg`, one or two stops DARKER.** Phone HDR **off**, tap the
decal, drag exposure **down** until the white lettering stops glowing and each letter's edge is
visible. The rest of the frame may go black. **Same distance, same angle — do NOT step closer.**

---

## 3. THE NOSE, SQUARE ON *(standing since rev 45 — five revisions)*

**Settles:** W4, *"the nose of the car is too flat"* — his own report, **confirmed and unfixed**, at
14.3 mm of bulge over 0.70 m of half-width.

**Why not from what we hold:** the two best frames are `ref_workshop.jpg` (~240 px across the nose
face, but it is the **GREEN** bus under flat overhead fluorescent, so almost no directional falloff —
admissible as **geometry**) and `ref_nolita_front34.jpg` (~165 px, the **red channel clipped**, the
near lamp blooming over ~78 px, a child occluding the lower quarter, **and an earlier artwork state**).
Everything else is ≤ 110 px, i.e. ~15 mm per pixel.

**Method 2 — silhouette corner-wrap on `ref_workshop.jpg` — is still the live one**, and it is the
method that does not care about lighting. **It has never been run.**

---

## 4. A RAKING-LIGHT FRAME OF THE LOUVRES

**Settles:** the **pressing depth**, the one louvre dimension still open. The count (10) and pitch
(21.111 mm) are confirmed; the apertures were cut at rev 48.

**Why not from what we hold:** built amplitude 0.385 against a photographed 0.206 is **one lighting
against another** — the photographed block is in the counter's shade and the rendered one in open key.
The probe prints that ceiling every run. **Do not tune the depth from those figures.**

*The shot:* sun or a lamp **low and along the flank**, six or so slats filling the frame. The shadow
length against the known pitch gives the depth directly.

---

## 5. THE OFF SIDE — ANY FRAME AT ALL

**Settles:** whether the off flank carries a matching louvre array, and the off-side serving
apertures, which are graded **E** and are explicitly **not a correctness claim**.

**Why not from what we hold: every frame in the project is of the serving side. There is no
exception.** Anything at all from the other side would be new information.

---

## DO NOT ASK HIM AGAIN

* **The vent slats** — answered rev 46; geometry and count confirmed rev 48.
* **The bunting** — answered twice: removed rev 46, identified as **STARS** rev 48.
* **Which vehicle** — answered rev 48: the **RED** bus.
* **The raised sign board (W5)** — dissolved rev 48; `ref_side.jpg` shows the flower mural exactly as
  built. He should never have been asked.
* **Whether the tail board is on the vehicle** — **answered rev 49**: *"That was referring to a
  different sign. This one is part of the vehicle."* Its **footing** (item 1) is a different question
  and is still open.
* **Which rear bay is open** — **answered rev 49**: *"Leave the lower bay shut, just have the back
  trunk window open for service."* The engine lid is **SHUT**. Do not propose reopening it, and do not
  ask for a photograph of the open tail: **with the lid shut, nothing in that bay shows.**
* Anything on rev 45's do-not-ask list.
