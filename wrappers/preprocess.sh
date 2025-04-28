#!/usr/bin/env bash
umask u+rw,g+rw # give group read/write permissions to all new files
set -e    # stop immediately on error

#  IMPORTANT: you must have MRCATDIR and MATLABBIN set as global environment variables (in your .bash_profile) for scripts to run
#  MRCATDIR points to your local MrCat-dev directory
#  MATLABBIN points to your local Matlab app directory's bin folder (where matlab app is located)

#########################
#
# Wrapper script to preprocess and prepare raw data for FEAT
# Last version 20/11/2017
#
#########################

# initialise
# studyDir="/Volumes/NHP/NHP_Proj4"
# monkey="Ulrich"
# sessions="MI00600P"

echo ""
echo "preprocessing of awake behaving macaque EPI timeseries"

# sessionDir=$studyDir/$monkey/$session
# epiDir=$(find $sessionDir -maxdepth 1 -type d -name "ep2d_*")
prepared_session_dir=/users/rushworth/gwr089/scratch/Generalization-Preprocess/prepared/output/zach/MI01049P
struct_dir=/well/rushworth/projects/nhp/users/simone/struct/zach
# ----------------------------------- #
# MOTION CORRECTION / SLIGN ALIGNMENT
# ----------------------------------- #

# # run the motion correction, start a timer
# SECONDS=0
# echo "starting motion correction"

# # here be magic
# sh $MRCATDIR/pipelines/PreprocFunc_macaque/MotionCorrection_macaque.sh \
#     --episeries=$prepared_session_dir/func_reoriented \
#     --t1wimg=$struct_dir/struct_restore \
#     --t1wmask=$struct_dir/struct_brain_mask

# echo "  seconds elapsed: $SECONDS"
# echo ""

# --------------------------- #
# FUNC TO STRUCT REGISTRATION
# --------------------------- #

# run the EPI to T1w registration, start a timer
SECONDS=0
echo "starting EPI to T1w registration"

# here be more magic
sh $MRCATDIR/pipelines/PreprocFunc_macaque/RegisterFuncStruct_macaque.sh \
    --epiimg=$prepared_session_dir/func_reoriented_ref \
    --t1wimg=$struct_dir/struct_restore \
    --t1wmask=$struct_dir/struct_brain_mask

echo "  seconds elapsed: $SECONDS"
echo ""


echo ""
echo "preprocessing is complete!"

