#!/usr/bin/env bash
set -e    # stop immediately on error
umask u+rw,g+rw # give group read/write permissions to all new files

studyDir="/users/rushworth/gwr089/scratch/Generalization-Preprocess"
monkey="zach"
session="TEST"
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
sh $MRCATDIR/pipelines/PreprocFunc_macaque/MotionCorrection_CorrectMotionDistortion.sh \
    --from-vol=2 \
    --to-vol=3 \
    --vars=/users/rushworth/gwr089/scratch/Generalization-Preprocess/zach/TEST/epi2d/work/motion_correction_vars.sh

echo "  seconds elapsed: $SECONDS"
echo ""


