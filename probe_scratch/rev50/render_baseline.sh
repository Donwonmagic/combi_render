#!/bin/bash
# rev 50 baseline renders -- SEQUENTIAL, one Blender at a time.
cd /home/user/combi_render
mkdir -p out probe_scratch/rev50
LOG=probe_scratch/rev50/render_baseline.log
: > $LOG
run () {
  V="$1"; PFX="$2"; RX="$3"; RY="$4"; SAMP="$5"
  echo "=== $(date +%H:%M:%S) START $V pfx=$PFX ${RX}x${RY} ${SAMP}spp ===" >> $LOG
  T1_PREVIEW="$V" T1_PFX="$PFX" T1_RX="$RX" T1_RY="$RY" T1_SAMP="$SAMP" \
    /tmp/blender/blender -b -P build.py >> $LOG 2>&1
  RC=$?
  # rev 50: this said `rc=$?` AFTER the redirect, so it reported the status of
  # `echo`, not of Blender -- three baseline renders aborted on a source edit
  # mid-queue and the log printed rc=0 for all three.  Rule 3, in my own harness.
  echo "=== $(date +%H:%M:%S) END $V rc=$RC ===" >> $LOG
  if [ "$RC" != "0" ]; then echo "!!! $V FAILED rc=$RC" >> $LOG; fi
  ls -la out/ >> $LOG 2>&1
}
# side ortho first: it is the measuring frame for most of the A-list
run side      r50a 1600 1100 96
run hero34f   r50a 1600 1100 96
run hero34r   r50a 1600 1100 96
run rear      r50a 1600 1100 96
run counter   r50a 1600 1100 96
run low34     r50a 1600 1100 96
run front     r50a 1600 1100 96
echo "=== $(date +%H:%M:%S) ALL BASELINE RENDERS DONE ===" >> $LOG
