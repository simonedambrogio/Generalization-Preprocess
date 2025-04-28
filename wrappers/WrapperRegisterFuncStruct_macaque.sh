#!/usr/bin/env bash
set -e    # stop immediately on error
umask u+rw,g+rw # give group read/write permissions to all new files

studyDir="/users/rushworth/gwr089/scratch/Generalization-Preprocess"
monkey="zach"
session="MI01049P"
sessionDir=$studyDir/$monkey/$session

echo ""
echo "EPI to T1w registration"

# --------------------------- #
# FUNC TO STRUCT REGISTRATION
# --------------------------- #

# run the EPI to T1w registration, start a timer
SECONDS=0
echo "starting EPI to T1w registration"

# here be more magic
sh $MRCATDIR/pipelines/PreprocFunc_macaque/RegisterFuncStruct_macaque.sh \
    --epiimg=$sessionDir/epi2d/f_mean \
    --t1wimg=$studyDir/$monkey/structural/mprage/structural_restore \
    --t1wmask=$studyDir/$monkey/structural/mprage/structural_brain_mask

echo "  seconds elapsed: $SECONDS"
echo ""