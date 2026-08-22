#!/bin/bash
cd /home/user/combi_render
LOG=probe_scratch/rev51/renderq2.log
: > "$LOG"
echo "TREE FROZEN AT: $(git rev-parse HEAD)  dirty=$(git status --porcelain | wc -l)" >> "$LOG"
for V in side low34; do
  echo "=== BEGIN $V  $(date -u +%H:%M:%S) ===" >> "$LOG"
  T1_PREVIEW=$V T1_PFX=r51c T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
    /tmp/blender/blender -b -P build.py >> "$LOG" 2>&1
  rc=$?
  echo "=== END $V rc=$rc  $(date -u +%H:%M:%S) ===" >> "$LOG"
done
echo "=== QUEUE DONE  $(date -u +%H:%M:%S) ===" >> "$LOG"
