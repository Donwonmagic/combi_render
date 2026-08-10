// tacombi-rev11-audit.js -- THE COMPREHENSIVE SPECIALIST AUDIT. DEFERRED, NOT DROPPED.
//
// Donald asked for "a complete and comprehensive workflow by a number of expert
// specialists" and this is it: ten specialists, one per dimension, each measuring
// the model and the current heroes against the source photographs; then an
// ADVERSARIAL verifier per ranked finding whose instruction is to REFUTE it; then
// one synthesis into AUDIT_rev11.md.
//
// WHY IT DID NOT RUN IN rev 11, stated plainly because it was my call and not his:
// this container has TWO CPU CORES, so the Workflow runner executes about two
// agents concurrently. Two hours in, it had started 2 of its 25 agents. I stopped
// waiting on it and redirected to three targeted specialists instead, which is what
// produced the galley, mural and folk-art fixes in rev 11. Donald has said he wants
// the audit conducted, so it is carried forward here rather than lost.
//
// HOW TO RUN IT
//   Workflow({ scriptPath: "<repo>/workflows/tacombi-rev11-audit.js" })
// On a 2-core box budget many hours and let it run unattended -- it is a good
// overnight job. On a wider box it is a normal fan-out.
//
// THE ALTERNATIVE THAT WORKS ON 2 CORES, and what rev 11 actually used: take the
// ten DIMENSIONS briefs below and spawn them 3-4 at a time with the Agent tool on
// DISJOINT files, verifying each batch before the next. Slower to write, far faster
// to finish, and it keeps you in the loop between batches.
//
// BEFORE RUNNING, UPDATE THESE -- they were written against rev 10 and rev 11 moved:
//   * the `playa` dimension: Donald deprioritised it ("let's not do playa right
//     now. Lets focus on the 3d model"). Drop it or replace it with a WEATHERING
//     dimension, which is now the dominant CG tell.
//   * the `roof` dimension's brief still poses the lid topology as unresolved. It
//     is resolved -- SPEC 10.26. Re-point it at what is still open: whether the
//     front lid sits forward of LID_X0, and what the rear lid carries.
//   * the `counter` dimension: the galley was rebuilt in rev 11 and now reads
//     130/160/167 against a measured 137/157/175. Point it at the INTERNAL
//     CONTRAST instead (bay 1 sd 15.3 against the photograph's 28.4).
//   * add the roof cutter (SPEC 10.27) to the `proportion` or `roof` brief.
//
export const meta = {
  name: 'tacombi-rev11-audit',
  description: 'Comprehensive specialist audit of the Tacombi combi render against the source photographs, with adversarial verification',
  phases: [
    { title: 'Audit', detail: 'ten specialists, one per dimension, measuring the model and the rev-10 heroes against the source photographs' },
    { title: 'Verify', detail: 'adversarial re-derivation of every ranked finding by an independent method' },
    { title: 'Synthesise', detail: 'one ranked, deduplicated work list' },
  ],
}

const REPO = '/home/claude/work/tacombi'

const PREAMBLE = `
You are a world-class specialist auditing a hyper-photorealistic 3D reconstruction of ONE
SPECIFIC VEHICLE: the Playa del Carmen "Senor Tacombi" combi, a 1963 VW Type 2 cut open and
converted into a taco stand. Repo: ${REPO}. Blender: /tmp/blender/blender. Python3 with
numpy/scipy/PIL/skimage.

FIRST read /home/claude/work/measure/RULES.md IN FULL. It is binding and it encodes traps that
have each cost this project real work.

THE STANDARD, in the owner's words, and it governs your severity ratings:
  "The final product should be nearly indistinguishable from the original.
   ANY SINGLE MEASUREMENT OFF IS UNACCEPTABLE."
  "We are recreating a photo realistic version of THAT EXACT BUS." Not a 1963 T1. Not a generic
  taqueria combi. His.
The acceptance criterion is PER-MEASUREMENT, not on average. A model right in ninety places and
wrong in one is not 99 per cent done, because the owner will look straight at the one.

SOURCE PHOTOGRAPHS ARE THE ONLY TRUTH:
  ${REPO}/ref_side.jpg      1024x768  left flank in service, nose at image LEFT
  ${REPO}/ref_rear34.jpg    1200x824  REAR three-quarter, same flank. Owner-confirmed: the NEAR
                            end (right of frame, x >= about 930) is the TAIL - engine lid, chrome
                            "1963" plate, oval amber tail lamp, chrome T-handle. The cream panel
                            lettered in red script with a red star (x 555-860, y 5-215) is the
                            UNDERSIDE OF THE LID OVER THE FRONT. The roof lids open FORWARD.
  ${REPO}/ref_workshop.jpg  1200x824  green, mid-conversion. NOTE: headlamps and indicators are
                            NOT FITTED in this frame - every circular feature on that nose is a
                            bare aperture. Different fit-out state; do not mix it with in-service.
  ref_source.jpeg is the RETIRED 246x197 thumbnail. Do not open it. Ever.

CURRENT OUTPUT to audit:
  ${REPO}/out/hero_studio.png   2400x1600 white-studio hero (rev 10)
  ${REPO}/out/hero_playa.png    2400x1600 Playa hero (rev 10)
You may also render your own views. studio.views() has hero34f, hero34r, front34, side, front,
rear, detail_f, low34, topdown, playa, playa_w, playa_ref, counter. Render with:
  cd ${REPO} && python3 hero.py VIEW --res 900x600 --samples 24 --strips 1 --tag YOURTAG --no-post
  (add --scene playa for the Playa rig). A single shell command is KILLED AT 10 MINUTES; keep
  every render small. nohup/setsid/disown all fail here. Do NOT render at hero resolution.
To inspect geometry, write a probe script and run:
  T1_SUB=1 /tmp/blender/blender -b --python /tmp/yourprobe.py
  (a probe that does exec(open("build.py").read()) after chdir to the repo gets the built scene).

READ THESE BEFORE MEASURING: ${REPO}/SPEC.md sections 10 and 10.9 through 10.25 (they supersede
section 10 where they differ), ${REPO}/STATE.md (machine-written from the mesh; if it and any
prose disagree, IT is right), ${REPO}/HANDOFF_rev10.md.

ALREADY SETTLED - do NOT re-open without NEW evidence and a DIFFERENT method:
  * Tyre OD 0.665 m on 16-inch rims. Raised and rejected three times.
  * No rear bumper in service. Front bumper cream.
  * Roof cut into hinged lids, modelled OPEN, opening FORWARD.
  * About 65 mm low at the reference station with about 1.9 deg nose-down rake.
  * Flank RED sRGB (196,49,36), hue 5.0, saturation 0.816.
  * Never correct this vehicle toward the VW factory catalogue. A finding whose evidence is a
    factory blueprint, used against a measurement from the actual vehicle, is presumptively
    REFUTED.
  * geometry-4 (roof transverse dome) was ruled NOT MEASURABLE from the admissible frames.

YOUR OUTPUT IS A LIST OF FINDINGS. For each finding you MUST give:
  - what the PHOTOGRAPH shows, with the pixel region you measured and the number you got
  - what the MODEL does, with the number you measured off the mesh or the render
  - the METHOD, precisely enough to reproduce, and an UNCERTAINTY
  - severity 1-5 where 5 = a viewer looking at the hero sees it immediately
  - where the fix lives (file, and line or function if you can find it)
Never report a self-assigned quality score. If something is NOT MEASURABLE in the available
photographs, say so plainly and mark it - that is a valid and valuable finding. Do not invent a
plausible number. Do not report a difference you have not measured.
`

const FINDINGS_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['dimension', 'summary', 'findings'],
  properties: {
    dimension: { type: 'string' },
    summary: { type: 'string', description: 'two or three sentences: the overall state of this dimension against the photographs' },
    findings: {
      type: 'array',
      maxItems: 14,
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['title', 'photograph_shows', 'model_does', 'method', 'severity', 'fix_location'],
        properties: {
          title: { type: 'string' },
          photograph_shows: { type: 'string' },
          model_does: { type: 'string' },
          method: { type: 'string' },
          uncertainty: { type: 'string' },
          severity: { type: 'integer', minimum: 1, maximum: 5 },
          fix_location: { type: 'string' },
          not_measurable: { type: 'boolean' },
        },
      },
    },
  },
}

const VERDICT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['verdict', 'reasoning'],
  properties: {
    verdict: { type: 'string', enum: ['CONFIRMED', 'REFUTED', 'NOT_MEASURABLE', 'PARTIAL'] },
    reasoning: { type: 'string' },
    independent_method: { type: 'string' },
    corrected_measurement: { type: 'string' },
    revised_severity: { type: 'integer', minimum: 1, maximum: 5 },
    risk_if_applied: { type: 'string', description: 'what this change could break - locked dimensions, guards, pipeline order' },
  },
}

const DIMENSIONS = [
  { key: 'proportion', brief: `PROPORTION, STANCE AND SILHOUETTE.
Compare the model's silhouette against ref_side.jpg by rectifying both to a common frame. Measure:
overall length, height at three stations, wheelbase, front and rear overhang, the rake angle, ride
height, wheel-arch gaps front and rear, the roof line's slope, the belt line's slope, the tumblehome.
Do it by RATIO within extents that are both independently locked, never by a single linear px/m
scale (194.8 px/m at the rear panel against 211.5 at mid-body). SPEC 10.9 logs an UNRESOLVED
contradiction between the rake and the arch gap - resolve it if you can, or state precisely why not.
Also check the 99 mm tail-length discrepancy noted as open (model -2.108, measured -2.007).` },

  { key: 'fascia', brief: `THE FRONT FASCIA. The owner called this out as drifting and it is the region he looks at.
Audit every element against the (60,330)-(330,700) region of ref_side.jpg and ref_workshop.jpg:
the V-swage geometry and where its apex sits, the two-tone break across the nose, the VW roundel
(diameter, height, the V-over-W glyph's proportions and the air gap between V and W), headlamps
(diameter, height, bezel), indicators (type, size, position), the bumper (blade section, standoff,
irons, over-riders), the cab door and its vent wing, wipers, mirrors, the front plate if any.
SPEC 10.24 lists THREE items applied and then reverted - bumper standoff, indicator lens depth,
headlamp vertical position - each because a second method refuted the first. Re-derive each by a
THIRD independent method and say which way it falls. Also audit the FOLK ART on the nose: the
rev-10 render shows scattered comma marks where the photograph shows scrollwork.` },

  { key: 'script', brief: `THE FLANK SCRIPT - and this is the INDEPENDENT test that has never been run.
compare_script.py scores the generated mask against the reference mask, but rev 10 traced the
glyphs FROM that mask, so it is no longer an independent check. Run the real one:
  cd ${REPO} && python3 flank_compare.py out/SIDERENDER.png out/flank_compare.png
It crops the rendered flank by projecting the panel through the ortho camera. Render the side view
yourself first. Then measure, against ref_side.jpg at matched scale: the lockup's position on the
flank, its size as a fraction of the panel, its baseline angle, per-glyph shape, the silver's value
and its mottle, the tarnish distribution, and whether the swash and the spiral counters land where
the photograph puts them. Report IoU AND the things IoU cannot see. Also audit the "100% Calidad"
sunburst decal the same way.` },

  { key: 'roof', brief: `THE ROOF, THE LIDS AND THE SIGNBOARDS.
The lids open FORWARD. There is an UNRESOLVED TOPOLOGY QUESTION and your job is to get as far as
measurement can: the lettered cream panel's apparent aspect in ref_rear34 is at least 1.15 and
foreshortening can only REDUCE an aspect, so its true aspect is at least 1.15; the model's front lid
board is 1.83 and the rear lid board 0.67, so the lettered panel cannot be the rear board. But the
flower board's footprint in ref_side spans bus fraction 0.262-0.738 against the front lid's
0.275-0.750. Both cannot be one face. Test the hypothesis that the flower board is a SEPARATE
signboard standing proud of the front lid whose own underside is the cream lettered panel - look
for its thickness, its shadow on the lid, its support struts, any gap. Also audit: the mural's
flower count, positions and palette; the yellow menu strips and what they say; the bulb string;
the lid struts and stays; the hinge line; the rear lid; and the lettered panel's script.` },

  { key: 'counter', brief: `THE COUNTER, THE SERVING BAYS AND THE GALLEY.
Audit against both in-service photographs: the counter slab (depth, height, the gold/brass nosing,
the cream fascia, how far it wraps past the tail, its end caps), the three serving apertures (widths
0.507/0.516/0.525 are locked - verify their POSITIONS and their surrounds), the decorative trim and
small bulbs around each aperture, the printed menu cards on the pillars, the condiment caddies, and
what is visible INSIDE - the blender, bottles, the plancha, shelving, the galley backdrop. Audit
finding materials-5 is open and never skeptic-passed: the three serving bays share ONE reflection,
NCC 0.94-0.97 between them, which is fatal at hero resolution. Verify it and quantify it in the
rev-10 render. Also: apertures-7 is open.` },

  { key: 'wheels', brief: `WHEELS, TYRES, ARCHES AND THE GROUND CONTACT.
Cream painted steel rims, blackwall tyres, RED domed hubcaps with a cream VW. Measure against both
in-service photographs: rim diameter and width, the flange, the tyre's section and sidewall profile,
the hubcap's diameter as a fraction of the rim and its dome depth, the VW glyph on the hubcap, the
number and position of any bolts or slots, the tyre's tread and shoulder, the arch lip section, the
gap between tyre and arch front and rear. Then audit optics-6, open and never applied: the contact
shadow dies within 11 mm of the tyre, so the vehicle reads as floating - measure the contact shadow
in the rev-10 heroes and say what it should be. Also check whether the wheels are correctly steered
and whether the tyres deform at the contact patch at all.` },

  { key: 'materials', brief: `MATERIALS, PAINT AND WEATHERING.
SPEC 3 locks the finish as WEATHERED - chalky, sun-faded, uneven - and SPEC 10.4 has measured
targets. STATE.md reports SIX materials still carrying a CONSTANT roughness (amber, bulb, glass,
lens, reflector, ruby); a constant roughness is the physical definition of the plastic look. Audit
each against the photographs and say which are legitimate (transmissive, sealed reflector) and which
are not. Then measure, in the photographs and in the rev-10 renders: the paint's value, saturation
and its VARIATION across the body; chalking and fade gradients (are they where the sun would put
them?); dirt and road grime distribution; the cream's condition; edge wear on the arches, the shut
lines and the counter lip; the brass nosing's tarnish; the chrome's condition. Report every place
the render is CLEANER or MORE UNIFORM than the photograph - that is the dominant CG tell on this
vehicle.` },

  { key: 'tail', brief: `THE TAIL AND THE REAR QUARTER.
The near end of ref_rear34.jpg (x at least 930) is the TAIL and it is the best photograph of it that
exists. Audit at 5-14x: the engine lid (its shut line, the recessed panel, the T-handle, the hinge),
the chrome-framed "1963" plate and what is actually legible on it, the oval amber tail lamps with
chrome bezels (size, position, height), the tail apron and how it rolls under to a lip with NO rear
bumper, the rear window, the rear-quarter air-intake louvres painted over in the red (count, pitch,
size, position), the fuel flap, and the folk art on the rear quarter - which is where the heavy
dark-brown outlined curlwork actually lives (2.4 per cent area), unlike the cab door. Also verify
the counter's tail wrap and overhang.` },

  { key: 'optics', brief: `LIGHTING, GLASS, REFLECTIONS AND CAMERA.
Audit the rev-10 heroes as PHOTOGRAPHS. Glass first: the rear window renders as a MIRROR in the
Playa hero rather than showing an interior - diagnose it and say what is wrong in the material or
the scene. Then: the windscreen and cab door glass, their seals, any glazing that should be absent
(the serving apertures are GLASSLESS), reflections that repeat where they should not, the bulb
string's emission and whether the bulbs read lit, specular highlight shape and size against what
the softbox subtends, depth of field and whether it is doing anything, chromatic aberration and
vignette from post.py, and the noise floor. For the white-studio hero specifically: is the backdrop
actually reaching paper white, is there a contact shadow, and does the vehicle sit in the frame the
way a product photographer would place it.` },

  { key: 'playa', brief: `THE PLAYA HERO AGAINST ITS OWN BRIEF.
The owner's bar for this image is EMOTIONAL: he wants a viewer to feel they were on Playa del
Carmen years ago and the owner of the bus to remember standing in it. It is rendered from the
reference photograph's own recovered camera. HANDOFF_rev10 records it as NOT CONVERGED: the render
reads cream 253 / red 193 / foliage 46 / ground 186 in display luma where ref_rear34 reads
241 / 118 / 82 / 108, and the cream is clipping. The stated diagnosis to test is that this is a
CONTRAST mismatch rather than a level one, because the film (AgX + Punchy) is calibrated for the
white studio where paper white sits at linear 21.0 (SPEC 10.8). TEST THAT DIAGNOSIS and give the
fix as a specific change. Then audit the environment against ref_rear34: the vegetation's species,
scale, placement and value; the flowering band; the seating; the ground; and what the photograph
has that the render does not. Remember SKEPTIC B5: NEITHER in-service photograph is in direct sun,
so do not recommend an orange grade, a sun lamp or a dapple gobo. There is no papel picado.` },
]

phase('Audit')
log(`Auditing ${DIMENSIONS.length} dimensions against the source photographs`)

const audits = (await parallel(DIMENSIONS.map(d => () =>
  agent(`${PREAMBLE}\n\nYOUR DIMENSION:\n${d.brief}\n\nWork thoroughly. Open the photographs at 5-14x magnification and LOOK before you measure. Measure with numpy, not by eye. Then report.`,
    { label: `audit:${d.key}`, phase: 'Audit', schema: FINDINGS_SCHEMA })
))).filter(Boolean)

log(`${audits.length} of ${DIMENSIONS.length} audits returned`)

const all = audits.flatMap(a => (a.findings || []).map(f => ({ ...f, dimension: a.dimension || 'unknown' })))
log(`${all.length} raw findings`)

const measurable = all.filter(f => !f.not_measurable)
const unmeasurable = all.filter(f => f.not_measurable)
measurable.sort((a, b) => (b.severity || 0) - (a.severity || 0))
const TO_VERIFY = measurable.slice(0, 14)
log(`verifying the top ${TO_VERIFY.length} by severity; ${unmeasurable.length} marked NOT MEASURABLE pass through unverified`)

phase('Verify')
const verdicts = (await parallel(TO_VERIFY.map((f) => () =>
  agent(`${PREAMBLE}

YOU ARE AN ADVERSARIAL VERIFIER. Another specialist has made the claim below. Your job is to try to
REFUTE it, not to confirm it. Default to REFUTED if you cannot independently reproduce it.

This project has a documented history of findings that were applied and then turned out to be wrong,
each time because the finding's method had a flaw nobody tested:
  * livery-9 said the VW roundel was 9 per cent undersized. It was applied. The roundel went 32 per
    cent OVERSIZE, because the finding's only photographic support was the retired thumbnail.
  * A bumper standoff of "at least 80 mm" was applied and put the blade 63 mm PROUD of the nose
    crown and broke the locked overall length - because the two figures used different datums.
  * A folk-art coverage of "0.0-0.2 per cent" was measured by scanning image columns on a door that
    is swung OPEN 49 degrees, so it sampled the wrong surface. The true figure is 29.1 per cent.
  * A reference ink mask thresholded on saturation silently dropped 14 per cent of the ink, and two
    "generator defects" were artefacts of it.
So: find the flaw if there is one.

THE CLAIM (dimension: ${f.dimension}):
  Title: ${f.title}
  Photograph shows: ${f.photograph_shows}
  Model does: ${f.model_does}
  Method used: ${f.method}
  Uncertainty stated: ${f.uncertainty || 'none stated'}
  Severity claimed: ${f.severity}
  Fix location: ${f.fix_location}

Re-derive it by a DIFFERENT method from the one stated. If the claim rests on a single chain of
inference, find a second chain. If it rests on one photograph, try another. If it uses a datum,
test whether that datum is sound - and remember RULES section 3: no vertical position may come from
a ground line, and section 4: no single linear px/m scale holds along the flank.

Then judge:
  CONFIRMED      - reproduced independently, and applying it is safe
  REFUTED        - your independent method disagrees, or the original method has a flaw you can name
  PARTIAL        - the defect is real but the magnitude or the cause is wrong; give the corrected one
  NOT_MEASURABLE - the photographs available cannot settle it

Also state RISK IF APPLIED: what locked dimension, guard, or pipeline invariant this change could
break. build.py's pipeline order is load-bearing (subsurf before any boolean; wheel arches cut while
the shell is a closed solid; every other aperture cut after solidify), the body must stay a single
continuous nose-to-tail loft, and verify.py must stay at 0 fail at BOTH subdivision levels.`,
    { label: `verify:${(f.title || 'f').slice(0, 34)}`, phase: 'Verify', schema: VERDICT_SCHEMA })
    .then(v => ({ finding: f, verdict: v }))
))).filter(Boolean).filter(x => x.verdict)

const confirmed = verdicts.filter(v => v.verdict.verdict === 'CONFIRMED' || v.verdict.verdict === 'PARTIAL')
const refuted = verdicts.filter(v => v.verdict.verdict === 'REFUTED')
const notmeas = verdicts.filter(v => v.verdict.verdict === 'NOT_MEASURABLE')
log(`verified: ${confirmed.length} stand, ${refuted.length} refuted, ${notmeas.length} not measurable`)

phase('Synthesise')
const report = await agent(`${PREAMBLE}

You are the lead. Ten specialists audited the vehicle and fourteen findings then went through an
adversarial verifier whose instruction was to REFUTE them. Produce the owner-facing review he asked
for: "a comprehensive review of where the product stands now, and what still does not match."

DIMENSION SUMMARIES:
${JSON.stringify(audits.map(a => ({ dimension: a.dimension, summary: a.summary, n: (a.findings || []).length })), null, 1)}

VERIFIED FINDINGS (verdict attached):
${JSON.stringify(confirmed.map(v => ({ ...v.finding, verdict: v.verdict })), null, 1)}

REFUTED (these must NOT be applied - say so and say why, because they will otherwise be re-raised):
${JSON.stringify(refuted.map(v => ({ title: v.finding.title, why: v.verdict.reasoning, method: v.verdict.independent_method })), null, 1)}

NOT MEASURABLE from the available photographs:
${JSON.stringify(notmeas.map(v => ({ title: v.finding.title, why: v.verdict.reasoning })).concat(unmeasurable.map(f => ({ title: f.title, why: f.method }))), null, 1)}

UNVERIFIED lower-severity findings (state them as unverified):
${JSON.stringify(measurable.slice(14).map(f => ({ dimension: f.dimension, title: f.title, severity: f.severity, fix: f.fix_location })), null, 1)}

Write markdown to ${REPO}/AUDIT_rev11.md with:
 1. WHERE IT STANDS - an honest, specific assessment per dimension. No scores. Measurements against
    the photograph, each with its uncertainty.
 2. WHAT DOES NOT MATCH - the confirmed defects, RANKED BY WHAT A VIEWER SEES FIRST at hero scale,
    each with: the measured gap, the fix location, and the risk of applying it.
 3. DO NOT RE-OPEN - the refuted findings with the reason each fell.
 4. NOT MEASURABLE - what would be needed to settle each (usually: a new photograph, and say which).
 5. THE ORDERED WORK LIST for the next build, sequenced so that nothing later invalidates
    something earlier, with the batching rule respected (all geometry changes in ONE rebuild, guards
    re-run at BOTH subdivision levels after).
Be specific and physical. Never a self-assigned quality score. Then return a SHORT summary (under
400 words) of the top defects and the ordered work list.`,
  { label: 'synthesise', phase: 'Synthesise' })

return { audits: audits.length, raw: all.length, verified: verdicts.length, confirmed: confirmed.length, refuted: refuted.length, report }
