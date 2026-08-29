#!/usr/bin/env bash
# judge_set.sh -- rev 61, F146.
#
# EVERY FIDELITY JUDGEMENT THIS PROJECT MADE FOR SIXTY REVISIONS WAS MADE ON A
# RAW, UN-POST-PROCESSED FRAME, while post.py sat in the tree implementing
# bloom -> chromatic aberration -> vignette -> grain in the correct physical
# order.  ONLY `bloom` defaults to 0.0; ca, vig and grain default to 1.0
# -- post.py's _FLOATS.  This comment said "every per-stage gain" until
# rev 64 and the same wrong sentence was in the brief and in F146 (F189a).
# An independent
# photography panel scored OPTICS 1/10 and SENSOR CHARACTER 2/10 on that
# omission alone and put it at +4 to +6 points of 80.
#
# MEASURED on out/r61f_hero.png (watched print, rule 5):
#     frame exactly (255,255,255)   47.89 %  ->   1.54 %
#     corner value                    255.0  ->  246.4   (a real vignette)
#     high-frequency sigma            0.000  ->   1.317  (real grain)
#
# --backdrop headroom is REQUIRED: post.py's own rev-14 note records that
# without it the backdrop sits on the 255 clip, bloom's mask lifts it, and the
# designed vignette and grain are not rendered at all.
#
# This does NOT change the delivery path (hq_render.py -> stitch.py -> post.py)
# and it does not change what build.py writes.  It produces a SECOND set,
# suffixed _post, which is what a photorealism judgement should be made on.
set -e
cd "$(dirname "$0")"
PFX="${1:-r61f}"
for v in front side hero34f hero34r; do   # rev 71, F248: was "hero", which NO preview list has
                                          # produced since the hero34f/hero34r split -- judge_set.sh
                                          # exited 2 before post-processing the delivery view
    f="out/${PFX}_${v}.png"
    [ -f "$f" ] || { echo "judge_set: NO RENDER $f -- render before judging"; exit 2; }
    python3 post.py "$f" "out/${PFX}_${v}_post.png" \
        --bloom 1.0 --ca 1.0 --vig 1.0 --grain 1.0 --backdrop headroom
done
echo "judge_set: wrote out/${PFX}_*_post.png -- judge photorealism on THESE"
