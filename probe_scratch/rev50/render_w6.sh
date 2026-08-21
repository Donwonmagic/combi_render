#!/bin/bash
# rev 50 W6 -- the two frames the owner asked to be shown side by side.
# SEQUENTIAL.  k=1.0 is the shipped rig (already rendered as r50b_hero34f);
# this renders the k=3.5 arm on the SAME view so the pair is like-for-like.
cd /home/user/combi_render
LOG=probe_scratch/rev50/render_w6.log; : > $LOG
run () {
  V="$1"; PFX="$2"; shift 2
  echo "=== $(date +%H:%M:%S) START $V pfx=$PFX $* ===" >> $LOG
  env "$@" T1_PREVIEW="$V" T1_PFX="$PFX" T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
    /tmp/blender/blender -b -P build.py >> $LOG 2>&1
  RC=$?
  echo "=== $(date +%H:%M:%S) END $V rc=$RC ===" >> $LOG
  [ "$RC" != "0" ] && echo "!!! $V FAILED rc=$RC" >> $LOG
}
run hero34f w6soft T1_SOFTEN=3.5
run side     w6soft T1_SOFTEN=3.5
echo "=== $(date +%H:%M:%S) W6 RENDERS DONE ===" >> $LOG
