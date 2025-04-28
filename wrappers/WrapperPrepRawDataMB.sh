#!/usr/bin/env bash
umask u+rw,g+rw # give group read/write permissions to all new files
set -e    # stop immediately on error

#  IMPORTANT: you must have MRCATDIR and MATLABBIN set as global environment variables (in your .bash_profile) for scripts to run
#  MRCATDIR points to your local MrCat-dev directory
#  MATLABBIN points to your local Matlab app directory's bin folder (where matlab app is located)

# ---------------- #
# PREPARE RAW DATA
# ---------------- #

studyDir="/Volumes/LaCie"
monkey="Ulrich"
#sessions="MI00485P MI00486P MI00487P MI00488P MI00489P MI00491P MI00493P MI00496P MI00505P MI00510P MI00513P MI00521P MI00527P MI00531P MI00539P"
#sessions="MI00543P MI00546P MI00548P MI00555P MI00559P MI00562P MI00566P MI00570P MI00574P MI00577P MI00581P MI00585P MI00591P MI00593P MI00595P MI00597P"
#sessions="MI00615P MI00616P MI00617P MI00618P MI00619P MI00620P MI00621P MI00622P MI00623P MI00624P MI00625P MI00627P"
#sessions="MI00565P MI00569P MI00573P MI00576P MI00580P MI00584P MI00592P MI00594P MI00596P MI00598P MI00600P MI00601P MI00602P MI00604P MI00605P MI00606P"
sessions="MI00565P MI00569P MI00600P MI00601P MI00602P MI00606P"

prepare=1
orient=0

if [[ $prepare -eq 1 ]] ; then

	for session in $sessions; do

		echo "preprocessing of awake behaving macaque EPI timeseries"
		
		sessionDir=$studyDir/$monkey/$session
		
		epiDir=$(find $sessionDir -maxdepth 1 -type d -name "ep2d_*")
		cp -p $epiDir/*.nii.gz $epiDir/f.nii.gz

		# NOTE: for BATCH preprocessing, this is better run with a separate script (as it may require user input)!
		# NOTE: use argument --isrestingstate=1 (defaults to 0) to set up session folders only for resting state data (or only non-resting state data)

		# sh $MRCATDIR/in_vivo/PreprocFunc_macaque/PrepareRawData.sh --sessdir=$sessionDir --isrestingstate=1
		#sh $MRCATDIR/pipelines/PreprocFunc_macaque/PrepareRawData.sh --sessdir=$sessionDir

	done
fi


if [[ $orient -eq 1 ]] ; then

	for session in $sessions; do

	    echo; echo "    correcting orientation for all images in session"

	    sessionDir=$studyDir/$monkey/$session
	    epiDir=$(find $sessionDir -maxdepth 1 -type d -name "ep2d_*")

	    find $sessionDir -maxdepth 2 -type f -name "*.nii.gz" | while read input; do
	     
	        fslreorient2std $input $epiDir/f
	        
	        echo "      ${input} corrected (and gzipped)"
	    done
	done
fi
