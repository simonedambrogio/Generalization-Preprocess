#!/usr/bin/env bash
set -e    # stop immediately on error
umask u+rw,g+rw # give group read/write permissions to all new files

studyDir="/users/rushworth/gwr089/scratch/Generalization-Preprocess"
monkey="zach"
session="MI01049P"
sessionDir=$studyDir/$monkey/$session

echo ""
echo "motion correction of awake behaving macaque EPI timeseries"

# ----------------------------------- #
# MOTION CORRECTION / SLIGN ALIGNMENT
# ----------------------------------- #

# run the motion correction, start a timer
SECONDS=0
echo "starting motion correction"

# here be magic
sh $MRCATDIR/pipelines/PreprocFunc_macaque/MotionCorrection_macaque.sh \
    --episeries=$sessionDir/epi2d/f \
    --t1wimg=$studyDir/$monkey/structural/mprage/structural_restore \
    --t1wmask=$studyDir/$monkey/structural/mprage/structural_brain_mask

echo "  seconds elapsed: $SECONDS"
echo ""
