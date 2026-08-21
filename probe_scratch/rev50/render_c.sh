#!/bin/bash
cd /home/user/combi_render
LOG=probe_scratch/rev50/render_c.log; : > $LOG
run () {
  V="$1"; PFX="$2"
  echo "=== $(date +%H:%M:%S) START $V pfx=$PFX ===" >> $LOG
  T1_PREVIEW="$V" T1_PFX="$PFX" T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
    /tmp/blender/blender -b -P build.py >> $LOG 2>&1
  RC=$?
  echo "=== $(date +%H:%M:%S) END $V rc=$RC ===" >> $LOG
  [ "$RC" != "0" ] && echo "!!! $V FAILED rc=$RC" >> $LOG
}
run hero34f r50c
run front   r50c
run side    r50c
echo "=== $(date +%H:%M:%S) DONE ===" >> $LOG
