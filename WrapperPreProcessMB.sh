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
studyDir="/Volumes/NHP/NHP_Proj4"
monkey="Ulrich"
#WINKY#
#sessions="MI00489P"
#ULTRA#
#sessions="MI00543P MI00546P MI00548P MI00555P MI00559P MI00562P MI00566P MI00570P MI00574P MI00577P MI00581P MI00585P MI00591P MI00593P MI00595P MI00597P"
#ULRICH#
#sessions="MI00565P MI00569P MI00573P MI00576P MI00580P MI00584P"
#VAMPIRE#
sessions="MI00600P"

echo ""
echo "preprocessing of awake behaving macaque EPI timeseries"

for session in $sessions; do

	sessionDir=$studyDir/$monkey/$session
	epiDir=$(find $sessionDir -maxdepth 1 -type d -name "ep2d_*")

	# ----------------------------------- #
	# MOTION CORRECTION / SLIGN ALIGNMENT
	# ----------------------------------- #

	# run the motion correction, start a timer
	SECONDS=0
	echo "starting motion correction"

	# here be magic
	sh $MRCATDIR/pipelines/PreprocFunc_macaque/MotionCorrection_macaque.sh --episeries=$epiDir/f --t1wimg=$studyDir/$monkey/structural/structural_restore --t1wmask=$studyDir/$monkey/structural/structural_brain_mask

	echo "  seconds elapsed: $SECONDS"
	echo ""

	# --------------------------- #
	# FUNC TO STRUCT REGISTRATION
	# --------------------------- #

	# run the EPI to T1w registration, start a timer
	SECONDS=0
	echo "starting EPI to T1w registration"

	# here be more magic
	sh $MRCATDIR/pipelines/PreprocFunc_macaque/RegisterFuncStruct_macaque.sh --epiimg=$epiDir/f_mean --t1wimg=$studyDir/$monkey/structural/structural_restore --t1wmask=$studyDir/$monkey/structural/structural_brain_mask

	echo "  seconds elapsed: $SECONDS"
	echo ""
done

echo ""
echo "preprocessing is complete!"

