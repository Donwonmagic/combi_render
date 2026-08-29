# LEDGER — rev 70

> **RULE 55 HEADER — `python3 revstats.py`, run at close:**
> **geometry 254 lines · doc 4188 lines · instrument 539 lines · findings closed/refuted 3**
> *(rev 8–20, the era the owner named, ran **721** geometry lines per revision at a doc:geo ratio of
> **1.55**. The doc figure here is inflated by the handoff SPLIT, which moved 81 KB of carriers into a
> new file — that is a one-off, not a trend; see §2.)*
> **THE ZERO-CLOSURE STREAK IS BROKEN. Rev 66, 67, 68, 69 closed 0, 0, 0, 0. Rev 70 closed 3.**

---
## §1 WHAT THIS REVISION DID

Three things, in the order the owner asked for them.

1. **THE DRIFT WAS MEASURED AND THE HANDOFF WAS SPLIT** (§2).
2. **THE BACK OPENING WAS BUILT** — the owner's item 1, `RULED-rev62, NOT BUILT` for seven revisions (§3).
3. **AND THE BRIEF'S OWN INSTRUCTION FOR IT WAS REFUTED IN THE DOING** (§4). That is the result worth
   carrying: the top item was aimed at the wrong quantity, and building to it would have made the
   model worse.

---
## §2 THE SPLIT

> *[owner]* **"I feel that we were way more productive in the first 20 or so handoffs and I fear we
> have drifted since then."**

**He was right and `revstats.py` — new this revision — is the measurement:**

```
    band        geometry/rev   doc/rev   instr/rev   doc:geo   findings closed
    rev  8-20        721         1120         44       1.55
    rev 61-70        209         2923       1145      13.98
    rev 66..69                                                      0, 0, 0, 0
```

Geometry per revision fell **3.4×** while the brief grew **12 KB → 95 KB**. The cause is structural:
**all 54 rules were about not being WRONG and not one was about SHIPPING**, and rule 16 made pruning
the brief impossible, so it could only accumulate.

**DONE:** a **19 KB ACTION brief** plus `HANDOFF_CARRIERS.md` holding every carrier verbatim (14
sections, 81 KB). **Nothing deleted.** Guards **re-pointed to the union, not relaxed**, with four
companion rows that make the split separately testable — all **watched failing**: carriers missing →
red; brief re-bloated to 94,962 B → red; §4 gutted → section count 13 of 14 **and the original
emotional-bar row red**; §0 gutted → the reference-set row red. **Rule 55 added**, with three rows.
`verify_clone.sh` 351 → **358**, none relaxed, none re-based.

---
## §3 THE BACK OPENING — BUILT

**`TB_CHORD` 0.7110 → 0.8250 m.** Two independent frames, two scales, two picks:

```
    ref_side.jpg   RED bus, CURRENT livery, PRIMARY   >= 0.822 m   (mine, ends painted, k_t 215.5)
    IMG_3840.jpeg  the SAME bus, CHALKBOARD livery    >= 0.829 m   (F165, rev 62)
```

Agreeing to **0.9 %** across eight revisions. **Both are LOWER BOUNDS and so is the shipped value** —
the board sits inboard of the flank plane. 0.8250 is the shortest length consistent with both frames.

**THE GATE THIS OBJECT HAD NEVER HAD:** `verify._tail_board_pose`, reading the board's **principal
axis in XZ off the built mesh** and naming that ruler — because **F165's "built 38.4° / 0.732 m" is
the BOUNDING-BOX DIAGONAL** (rule 38). Both arms watched failing (`T1_TB_CHORD=0.7110`,
`T1_TB_TILT=28.0`).

**F244 CLOSED A QUESTION REV 69 HANDED FORWARD:** the large dark rectangle under the board is
`glass_rear` — 72 verts, Transmission 1.00, 5 of 9 rays hit the shell. The rear **window** reading
black into an unlit interior. **F71's branch, not a hole.**

---
## §4 WHAT REV 70 GOT WRONG — IN ITS OWN BRIEF, ABOUT ITS OWN TOP ITEM

**The brief made *"38.0° against a photographed 28.0°, ~10° too steep"* the #1 item. It is REFUTED.**

```
    ref_side.jpg    PRIMARY frame     38.8 deg
    IMG_3840.jpeg   same board        21.0 deg
    BUILT                             38.0 deg   <- matches the PRIMARY frame to 0.8 deg
    F165 published                    28.0 deg   <- matches NEITHER
```

**THE BOARD IS HINGED. Its angle is a POSE, not a dimension** — the two frames are 18° apart because
somebody propped it differently on two different days. **Building to 28.0 would have made the model
worse against the vehicle being recreated.** Rule 35 and rule 11 firing together on the top item.

**AND RULE 8 KILLED THREE WINDOWS ON THE WAY**, each caught by PAINTING and none by reasoning: a
"cream face" mask that selected **the wall** (33.5°); a "bulb string" mask that selected **the red
wall graphics** (24.7°, rms 27.6 px on a 174 px baseline); and the orange face's **principal axis**
(21.7° — a foreshortened wedge's principal axis is not its chord). **Three plausible, publishable
numbers, every one wrong.**

**F163's "dark angled recess" was NOT built and that is a result (rule 12):** it appears only on the
chalkboard frame, on a surface the primary frame does not show, and at 480 px cannot be separated into
geometry, paint or shadow. **It cannot be recovered from what we hold.**

---
## §5 WHAT REV 70 DID NOT DO

* **The emblem** — untouched. The route is established by elimination (F236/F237); the construction is
  not built. **This is now the top item.**
* **The nose** — not re-rendered at delivery size and not looked at.
* **The board's PAINT** — held against `ref_side.jpg` the render's board is a plain white plank with
  pale bulbs where the photograph shows a cream face, a **red** edge stripe, a **navy** stripe and
  **lit** amber bulbs. Every one of those objects exists in the mesh. **Materials and emission, not
  form** — and it is the visible remainder of item 1.
* **C4**, F156, F143, the glass, the tail's barrel, the shut lines — untouched.

---
## §6 THE BRANCH, MEASURED AT CLOSE

`origin/claude/nose-fixture-alignment-r68-rrqyqx` is **ahead of `origin/main` and merged nowhere**.
`bootstrap.sh` prints the number and says row 9 cannot see that axis. **A fresh clone defaults to
`main` and would silently redo this work on a stale tree.** Re-measure at pickup; no sentence about
branch state survives the hour.
