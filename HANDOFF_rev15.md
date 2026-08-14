# HANDOFF — rev 15

> **THE STANDARD, in the owner's words, and it governs every line below.**
> The final product should be nearly indistinguishable from the original.
> **Any single measurement off is unacceptable.** We are recreating a photo
> realistic version of **that exact bus** — not a 1963 T1, not a generic
> taqueria combi. The criterion is PER-MEASUREMENT, not on average.
>
> And above clinical accuracy: *"I really want this to give the person the
> opportunity to feel like they were on Playa del Carmen all those years ago.
> I want the owner to remember standing in the kombi, in this very picture
> that was provided."*

Guards **0 fail / 1 warn at BOTH subdivision levels**, warn unchanged.
Verify by CONTENT, never by hash or commit count — §7 has the checks.

---

## 1. What the owner settled this revision

- **Nolita is re-admitted, FOR GEOMETRY ONLY.** Nolita photographs may now be
  used for shut lines, arch shape, tail face, engine-lid width, lamp count,
  plate position and off-side glazing — the items no supplied photograph
  covers. **Livery, weathering and artwork stay locked to HIS three
  photographs**, and every Nolita-derived number must be tagged as such in
  SPEC so it can be pulled back out.
- **The two blocked sources are skipped for now** (Tacombi's Instagram
  retrospective, the YouTube brand film) — recorded as blocked-not-absent.
- **SPEC §6's pure-white backdrop lock is RETIRED**, on the measured A/B in
  §4 below. `--backdrop headroom` is now the default.

## 2. THE RESTORE DID NOT FAST-FORWARD — read this before restoring anything

The rev-14 line branched from `258730a` and **never contained `f3c53f4`, the
true tip of the rev-13 line.** `git pull` of the rev14b bundle onto the unified
line fails with *"Need to specify how to reconcile divergent branches"* — that
is the symptom, not a config nuisance.

`f3c53f4` touches one file, `post.py`, and set `bloom` default to 0.0 having
measured that no threshold works on a display-referred frame. rev 14 rewrote
`post.py` and **re-measured the identical defect on its own arm A** — corners
255.000, vignette 0.0000 DN, grain sd 0.0000, 100 % of backdrop exactly white —
and shipped it as the baseline. So rev 14's *"byte-identical to rev 13,
hash-verified"* is true against `258730a` and false against the real rev 13.

**ALL SEVEN of rev 14's content checks passed while a whole rev-13 commit was
missing**, because every one greps for a string rev 14 added.

> **NEW STANDING RULE: a restore check that only asserts THIS revision's
> strings cannot detect a lost ANCESTOR. Every check list must also assert
> something the PREVIOUS line added.** §7's list does.

Merged as restoration, not a change: rev 14's `post.py` (a strict superset) with
`f3c53f4`'s measurement preserved verbatim. The remedy was applied only after
being re-measured on a real hero.

## 3. Detail geometry — item 7, applied with its measurement

| item | photograph | built before | after | σ before |
|---|---|---|---|---|
| cream rim / tyre D | 0.660 ± 0.008 | 0.5729 | **0.6611** | **10.9** |
| VW glyph h / ring ⌀ | 0.746 ± 0.027 | 0.5639 | **0.7761** | **6.6** |
| hubcap emblem / cap ⌀ | 0.317 ± 0.017 | 0.1897 | **0.317** | **7.0** |
| T-handle drop / plate H | +1.274 ± 0.025 | **−1.076** (240 mm *above*) | **+1.274** (214 mm below) | — |
| plate outer W / H | 1.962 ± 0.034 | 1.4798 | **1.962** | **14** |
| tail lamp D / plate H | 1.1627 ± 0.0271 | 0.4619 | **1.1627** | 1.90× small |

Method notes that carry forward:

- **The cream rim is the protractor.** The plate-aspect solve first tried
  rectifying by the frame's own vanishing points and **threw that route out** —
  both VPs are only 1.2σ detections and the rear panel is curved. The rim fits
  a circle to 0.35 px sd, so its apparent aspect 1.847 ± 0.055 *is* the flank's
  foreshortening. No px/m anywhere in the chain.
- Rim profiles now **scale onto `T.RIM_R`**, the constant that was dead. The
  tyre bead is remapped so `TYRE_D` stays 0.6650 and the guard holds.
- The glyph's scale is **read back off the built outline** — no fraction is
  written down, so it cannot go stale the way 0.7486 did. The 0.796 target is
  geometrically unreachable without re-authoring `t1_core.vw_bars`' spine: it
  bursts a ring the photograph shows intact.
- The T-handle and the tail lamp are written as **ratios of `PLATE_OUTER_H`**,
  the ruler they were measured against. That is why the brief's 205 mm and the
  measured 279 mm disagreed — same ratio, two different plates.
- **Louvre ends: NOT MEASURABLE, and not invented.** The band resolves at a
  9.0 px pitch, which is exactly the MERGED pitch of the modelled 4.5 px slot
  pitch, and what looks like a blade end is where the yellow folk art begins.

**Not done, reported:** the hubcap RING is still absent (18 px cannot author a
cross-section); `t1_core.vw_bars`' "12.7 mm air gap" docstring is false at every
diameter; the tail-lamp lens hue is a `t1_mats` question and `amber` is SHARED
with the front indicator, so a tail fix needs its own material slot.

## 4. Optics and the galley

**Glass — the brief was REFUTED and no rig change was made.** The inherited
"rear pane CV 1.22" was a **bounding box**, and the pane projects as a tilted
rounded rectangle, so the box caught cream bodywork in all four corners. On the
pane's own projected hull it reads **0.214** against the photograph re-measured
at **0.221–0.293** over four independently placed windows. Positive control:
re-smooth-shading that pane gives **0.833**, so the probe can see a mirror when
there is one — and the mirror was the smooth shading rev 14 already killed. The
rig is 72 % of the pane's *level*, but level is not the defect.

Also measured, and it changes how any dark pane must be read: **with grain off
the seed-to-seed null collapses sd 5.56 → 0.575.** Nearly all residual spread on
a dark pane is the compositor's film grain.

**Galley — the lever's sign was backwards.** Ablating `fill_galley` *raises*
contrast in all three bays: it was a frontal wash at near-normal incidence,
adding level and subtracting structure. One 1.7 m 21 W source became three
per-bay 0.42 m boxes riding `t1_shell.BAYS` at **0.25 / 0.00 / 0.29 W**.

| | bay 1 | bay 2 | bay 3 |
|---|---|---|---|
| before | 24.72 (145.4) | **19.51** (168.2) | 22.55 (181.5) |
| after | 23.63 (147.1) | **23.44** (159.4) | 21.85 (182.5) |
| photograph, re-measured | 33.69 ± 0.99 | **24.16 ± 0.76** | 21.36 ± 1.38 |

Bay 2's gap **4.64 → 0.73**; bay 3 moved *toward* the photograph. The photograph
was re-measured rather than inherited: bay 3 is **21.36, not 18.11** — a
stainless steamer occludes its lower-right corner in both frames.

**Side effect, logged not hidden:** galley-fill power falls 21.0 → 0.54 W and
the forward red flank drops **5.75 %**. That source was carrying ~4 % of the show
flank's key from 1.5 m away. No compensating light was invented.

**The backdrop A/B, on a real hero at 4320×2880:**

| arm | corners | frame exactly (255,255,255) | grain sd |
|---|---|---|---|
| raw, no post | 255.000 | 63.43 % | 0.0000 |
| white + bloom ON (rev 14 default) | 255.000 | **68.10 %** | 0.0000 |
| white + bloom OFF | 248.997 | 0.92 % | 0.4718 |
| **headroom — SHIPPED** | **246.043** | 0.66 % | **0.9415** |

The bloom arm **raises** the exactly-white fraction. It is erasing information,
not adding glare. `bloom` now defaults to **0.0**; `exclude=` remains the
structural fix and is still wired ONLY into `--backdrop headroom`.

## 5. Four solves, four refutations — SPEC 10.31

Every one of items 1, 2 and 3 was written as "solve constant X onto target T".
All three returned *X is not the parameter*, joining rev 13's bloom threshold.

- **`T1_MURAL_SPEC`** — the albedo pass responds exactly linearly (3 points,
  <0.01 % residual) and solving onto (126,60,24) gives **−0.854 / −0.651 /
  −0.024**. All negative. Validated at spec = 0, where the pass reproduces the
  texture's own area mean, B to 0.5 %. The R/G gap is a **region difference**:
  the SPEC crop is a tighter interior with less gold than the painted face.
- **`W_ALBEDO`** — `T1_W_ALB=0` gives **0.342 %** and the shipped 0.260 gives
  **0.339 %**. Identical. Best point in the whole exposed space is 0.810 %
  against a photograph re-measured at **8.890 %** — the cream is **26× too
  uniform**, not 6×. A denoiser-off arm at 384 samples reads 0.320 %, so it is
  neither render noise nor OIDN.
- **`COUNTERTAN`** — ratio (0.9311, 0.8505, 0.7366) against target (0.7960,
  0.8100, 0.6330) ± 0.02 = **6.8σ / 2.0σ / 5.2σ**. Secant gain only 0.33–0.49,
  so closing on albedo demands (0.177, 0.408, 0.094) — not plywood, not any
  wood.

**A real bug fell out of it.** `counter_tan()` runs at step 7 and `build_all()`
at step 9, and `simple()` resolves materials **by name** — so `build_all()`'s
`rough`/`coat`/`spec` for `countertan` were **dead arguments**. Exposed by a
four-arm ablation reading *identical to four decimals including the both-off
arm*. Same family as the dead `RIM_R` and the VW glyph. Fixed.

> **THE CHEAP DIAGNOSTIC THAT SHOULD RUN FIRST from now on:** ablate the
> constant to zero and re-measure. If the ablated arm and the shipped arm agree,
> the constant is not the parameter and no amount of solving will make it one.

**Two new instruments**, both calibrated against the photograph before use:
`shader_solve.py` (plain-sRGB renders decoded to linear; masks RENDERED from
each object's own alpha, never boxed) and `cream_rms.py` (one 25 mm high-pass
applied identically to photograph and render, on patches scanned for class
purity and eroded by 3σ).

## 6. The loft — grounded, not built (`LOFT_GROUND_rev15.md`)

- **Crown R 2.45 ± 0.15 m is REFUTED twice.** It puts the crown at 1.921, which
  is 39 mm below spec 1.960 **and below the roof's own photographed
  silhouette**. **R ≤ 2.06 m.**
- **The model's roof EDGE is 63 ± 20 mm too HIGH** — never measured before. The
  whole −66 mm residual was being blamed on the dome.
- Joint solution that closes: **D = 0.2116 ± 0.035, R = 1.84 ± 0.30, the rear
  station down 63 mm, rake unchanged at 17.75** → crown lands exactly on 1.960
  and `DOME_DEFICIT` → 0.
- Rear arch is a **flat-crowned ogee, confirmed** (superellipse rms 2.67 mm vs a
  circle's 11.4), crown centred on the rear axle to ~1 mm, **width 0.92 ±
  0.03 m** against 0.747 built — refutes rev 13's 1.026 at 3.4σ. The exponent is
  window-dependent (3.50–4.28); a normalised profile table is supplied instead.
- **Tail 235 ± 22 mm too long**; the old "99 mm" refuted at 10σ.
- **Pole mechanism found:** `loft(cap_first/last)` makes a 110-gon and subsurf's
  face point *is* the pole. A verified 27×28 Coons grid cap is specified — but
  `plate_1963` and `englid_handle` are anchored to the artefact surface, so the
  tail re-space and the cap must go in together.

## 7. Restore and verify — BY CONTENT, never by hash or commit count

```bash
git clone tacombi_history_rev9.bundle tacombi && cd tacombi
git pull ../tacombi_rev14_unified.bundle HEAD
git pull ../tacombi_rev14b_incremental.bundle HEAD
git pull ../tacombi_rev15_incremental.bundle HEAD
```

Then all of these must be true:

```bash
git status                                 # clean
grep -c '### 10.33' SPEC.md                # 1  — rev 15, the divergence
grep -c '### 10.30b' SPEC.md               # 1  — rev 14, the pole finding  (ANCESTOR CHECK)
grep -c 'UNTIL THEN BLOOM DEFAULTS OFF' post.py  # 1 — rev 13's f3c53f4     (ANCESTOR CHECK)
grep -c _isTail t1_mats.py                 # non-zero — rev 14's tail gate
grep -c 'BACKDROP = "headroom"' post.py    # 1  — the retired white lock
grep -c T1_CTAN_SP t1_mats.py              # non-zero — the dead-argument fix
ls shader_solve.py cream_rms.py LOFT_GROUND_rev15.md AUDIT_rev11.md AUDIT_rev12.md
```

Two of those are **ancestor checks** and they exist because rev 14's list had
none. Do not drop them.

## 8. Guards — the figures watched printing

```bash
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=2 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=1 /tmp/blender/blender -b --python audit.py
```

| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 1 warn** | **0 fail, 1 warn** |
| warn | roof crown @ rear axle (dome-corrected) **1.992** vs spec 1.960 (**+32 mm**) | **1.993** (**+33 mm**) |
| dims | roof@rear-axle **1.894**, raw resid **−66 mm**, `DOME_DEFICIT` **+98 mm** | 1.895, −65 mm, +98 mm |
| cut roof hole | **56293v** | **207383v** |

Also: `roof aperture: open, and solid fore / aft / both sides`; `TYRE_D=0.6650`;
3 open apertures on +Y; four shut lines `100 % open`; band `1.372–1.775`; bay
widths **`0.516 0.515 0.516`**; **181 meshes**; **0 non-manifold edges**;
**5 materials constant-rough**; 42 distinct materials.
`cutters rolled back | none` is a **STATE.md row**, not a console print.

## 9. The hero

`out/rev15_hero34f.png` — **4320×2880**, up from rev 13's 3600×2400. SUB=2,
56 samples, **18 strips**, worst seam **z = 2.75** against a threshold of 4.
`post.py` run **once** on the stitch, `--backdrop headroom`, bloom off.

Blender is not preinstalled in a fresh container:

```bash
curl -fsSL -o b.tar.xz https://download.blender.org/release/Blender4.5/blender-4.5.3-linux-x64.tar.xz
tar -xf b.tar.xz && mv blender-4.5.3-linux-x64 /tmp/blender
/tmp/blender/4.5/python/bin/python3.11 -m pip install pillow scipy   # NOT bundled
```

That last line matters: `shader_solve.py` and `post.py`'s exact backdrop flood
both need them, and Blender's bundled Python has neither.
