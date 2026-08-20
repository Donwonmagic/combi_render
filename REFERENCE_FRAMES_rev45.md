# THE REFERENCE FRAMES — recovered and named, rev 45

**This file exists because the rev-45 brief's §4 inventory was wrong, and being
wrong about it had already cost a revision's worth of work.**

## §1. WHAT THE BRIEF SAID, AND WHAT WAS ACTUALLY IN THE TREE

`NEXT_CONTEXT_PROMPT_rev45.md` §4 states:

> **Reference photographs (8, all tracked):** `ref_side.jpg` … `ref_rear34.jpg`,
> and the four Nolita frames — `ref_nolita_doorshut.jpg`,
> `ref_nolita_flank.jpg`, `ref_nolita_front34.jpg` (**the clearest roundel in
> the set**), `ref_nolita_front34b.jpg`.

`git ls-files` at the head of `claude/project-improvement-id3a9o`:

```
ref_band_grid.png  ref_grid.png  ref_nolita_doorshut.jpg  ref_nose_grid.png
ref_rear34.jpg     ref_side.jpg  ref_side_grid.png        ref_source.jpeg
ref_workshop.jpg   ref_x6_lanczos.png
```

**One Nolita frame, not four.** `ref_nolita_flank.jpg`, `ref_nolita_front34.jpg`
and `ref_nolita_front34b.jpg` **have never been committed to this repository.**
They existed in the rev-44 working tree — §5's item **W1**, the whole roundel-
placement task, is specified against measurements taken on
`ref_nolita_front34.jpg` — but they were never added, so the clone lost them.

**W1 as written was therefore unexecutable**: its method, its crop boxes and its
"roundel bbox cols 152–192, rows 192–257" all refer to a file that is not here.

## §2. THE OWNER'S UPLOAD IS THE MISSING FRAMES

Commit `f30022b` "Add files via upload" added five images. Four of them are the
missing frames; one is new to this project entirely.

| upload | size | canonical name added rev 45 | how the identification was made |
|---|---|---|---|
| `IMG_2060.jpeg` | 700×467 | **`ref_nolita_front34.jpg`** | **PROVEN.** The rev-45 brief publishes "roundel bbox cols 152–192, rows 192–257 → centre (172.0, 224.5), vertical D 66 px" for this frame. Re-measured on `IMG_2060.jpeg`: emblem mask rows **192–259**, cols **152–192**. The columns match exactly and the rows to 2 px. No other frame in the set has a roundel at those coordinates. |
| `IMG_3840.jpeg` | 480×320 | (already tracked as `ref_nolita_doorshut.jpg`) | **PROVEN.** md5-identical to the tracked file, `f1b6f98c6a…`. |
| `IMG_2054.jpeg` | 450×450 | **`ref_nolita_flank.jpg`** | **PROVEN — see §2a.** Identified by content first; the merge then confirmed it md5-identical to rev 44b's file of that name. |
| `IMG_2053.jpeg` | 550×412 | **`ref_nolita_front34b.jpg`** | **PROVEN — see §2a.** Same. |
| `IMG_3842.png` | 500×400 | **`ref_playa_34.png`** | **NEW TO THIS PROJECT.** Not named anywhere in rev 44's inventory or wanted-list. It is the **PLAYA** truck — folk-art flank, "Señor Tacombi" script, the "100 % Calidad" decal, an **unlit** headlamp in daylight, and the cab door's lower edge over the front wheel. It is the only frame in the whole set that shows the painted livery this model is actually reproducing. |

## §2a. THE TWO "BY CONTENT" IDENTIFICATIONS TURNED OUT TO BE PROVABLE

They were published above as **not proven**, and nothing in rev 45 was allowed
to rest on either. Then rev 45 merged the seventeen stranded rev-44/44b commits
(§4 below) — which carry `ref_nolita_flank.jpg` and `ref_nolita_front34b.jpg`
under exactly those names — and the files are **md5-identical**:

```
ref_nolita_front34.jpg    rev 44b ed2c33b0ec   rev 45 from the upload ed2c33b0ec
ref_nolita_flank.jpg      rev 44b a00c45b431   rev 45 from the upload a00c45b431
ref_nolita_front34b.jpg   rev 44b b8e7f7a44b   rev 45 from the upload b8e7f7a44b
```

Three for three. **This is recorded because the ordering matters**: the
identifications were made and published as unproven, and only then checked. Had
they been checked first the agreement would prove nothing about the method.

The `IMG_*` originals are **kept tracked as well as the canonical copies**, so
the provenance chain is in the repository rather than in this sentence.

## §3. WHAT EACH FRAME IS GOOD FOR — and what it is not

| frame | px | admissible for | NOT admissible for |
|---|---|---|---|
| `ref_side.jpg` | 1024×768 | the flank, the belt, the rocker, paint chroma vs cream | the bezel (grazing incidence, a few px — SPEC 10.111) |
| `ref_source.jpeg` | 246×197 | nothing new; **formally retired** (§10.2) yet load-bearing (ledger 21) | anything |
| `ref_workshop.jpg` | 1200×824 | **the nose emblem, at 92 px vertical — the largest in the set**; letterforms, geometry | the door plane (§10.62, §10.73); the emblem's stroke ANGLES (see below) |
| `ref_rear34.jpg` | 1200×824 | the tail | the flank |
| `ref_nolita_doorshut.jpg` | 480×320 | the whole cab-door outline, square-on | the body's lower edge — rows 278–298 are clipped to pure black (§10.106.7) |
| **`ref_nolita_front34.jpg`** | 700×467 | **the roundel's drawing and placement; the headlamp bezel's chroma; paint chroma** | the red's luminance — the red channel is clipped at 240+ over the nose |
| **`ref_nolita_flank.jpg`** | 450×450 | the cab door's lower edge over the front wheel; the hubcap | metrics needing a scale — no hub-to-hub baseline in frame |
| **`ref_nolita_front34b.jpg`** | 550×412 | the roof sign board and its props; the chalkboard | fine detail |
| **`ref_playa_34.png`** | 500×400 | **the folk art, the script, the Calidad decal, an UNLIT headlamp lens, the door over the arch** | anything needing >1 px precision; it is 500 px for a 4 m vehicle |

### A limit that rev 45 hit and could not get past

`ref_workshop.jpg` is the best emblem frame in the set and it still **cannot
settle the glyph's stroke angles.** De-foreshortening a three-quarter view of a
circle requires the ring's axis ratio, and the two independent fits available
disagree by 10 %:

* SPEC §10.107's published conic — vertical D 91.885 px, horizontal 63.143 →
  ratio **0.687**
* rev 45's own re-fit — a_h 34.14, a_v 44.69 → ratio **0.764**

A 10 % error in the horizontal stretch moves every measured angle by several
degrees, which is the whole size of the discrepancy anyone would be trying to
measure. **So rev 45 did not move the spine**, and `PHOTOS_WANTED_rev45.md`
asks for the one frame that closes it: the nose badge, square on.


## §4. AND THE REASON THEY WENT MISSING IN THE FIRST PLACE

The frames were not lost. **They were never merged.**

`origin/claude/tacombi-combi-rev-44-h4ipmg` carries **seventeen commits above
the point where PR #2 was merged**, and neither `origin/main` nor this branch
had any of them:

```
0437cf3  rev 44: the owner's uploads -- three NEW frames, two duplicates removed
028de7b  rev 44: the new front three-quarter measured -- ORDINAL only
3996ccd  rev 44: THE VW LOGO -- the roundel was mounted 11 mm INSIDE the nose
...
d90014f  rev 44b: his three reports, all confirmed, all measured
```

That is where `ref_nolita_*` was added (`0437cf3`), and it is also where
`SPEC.md` grew §10.102–§10.109, where `cab_fitout`, `door_hinges` and
`cabin_fill` were written, and where §10.100's door wrap was retracted.
**`SPEC.md` on `main` ends at §10.101.**

Rev 45 merged all seventeen. See `LEDGER_rev45.md` §1.
