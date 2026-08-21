#!/bin/bash
# rev 51 baseline queue.  SEQUENTIAL -- Blender is CPU-bound, never fan it out.
# rc is captured from BLENDER, not from the last command in the pipeline.
# (rev 50's harness put `rc=$?` after the redirect and reported echo's status.)
cd /home/user/combi_render
LOG=probe_scratch/rev51/renderq.log
: > "$LOG"
echo "TREE FROZEN AT: $(git rev-parse HEAD)  dirty=$(git status --porcelain | wc -l)" >> "$LOG"
for V in side detail_f low34 counter; do
  echo "=== BEGIN $V  $(date -u +%H:%M:%S) ===" >> "$LOG"
  T1_PREVIEW=$V T1_PFX=r51b T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
    /tmp/blender/blender -b -P build.py >> "$LOG" 2>&1
  rc=$?                                   # <- immediately after blender, nothing between
  echo "=== END $V rc=$rc  $(date -u +%H:%M:%S) ===" >> "$LOG"
  if [ "$rc" -ne 0 ]; then echo "!!! $V ABORTED rc=$rc -- queue continues, frame is INVALID" >> "$LOG"; fi
done
echo "=== QUEUE DONE  $(date -u +%H:%M:%S) ===" >> "$LOG"
ls -la out/ >> "$LOG"
