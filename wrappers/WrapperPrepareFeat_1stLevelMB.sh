#!/usr/bin/env bash
umask u+rw,g+rw # give group read/write permissions to all new files
set -e    # stop immediately on error

#  IMPORTANT: you must have MRCATDIR and MATLABBIN set as global environment variables (in your .bash_profile) for scripts to run
#  MRCATDIR points to your local MrCat-dev directory
#  MATLABBIN points to your local Matlab app directory's bin folder (where matlab app is located)

studyDir=/Volumes/NHP/NHP_Proj4/fMRI_data
outDir=/Volumes/NHP/NHP_Proj4/fMRI_data
templateDir=/Volumes/Monkey/structural_new/template_brain
monkey="Winky"
monkeyTemp="WINKY2021"
sessions="MI00485P MI00486P MI00487P MI00488P MI00489P MI00491P MI00493P MI00496P MI00505P MI00510P MI00513P MI00521P MI00527P MI00531P MI00539P"
standImg="$templateDir/ants/image/groupavg_2_brain.nii.gz"

# bad volume rejection parameters
sdThresh=2.5
doRecursive=0

for session in $sessions; do

	sessionDir="$studyDir/$monkey/$session"
	outputDir="$outDir/$monkey/$session"
	#struct2standwarp="$templateDir/ants/transform/$monkeyTemp/structural_to_groupavg_2_warp.nii.gz"

	#sh $MRCATDIR/pipelines/PreprocFunc_macaque/PrepareFeat_1stLevel.sh --sessdir=$sessionDir --outputdir=$outputDir --makefunc2standwarp=1 --standimg=$standImg --struct2standwarp=$struct2standwarp

	# add to space-separated lists for nuisance regressor function below
	sessionList+="$sessionDir "
	outputDirList+="$outputDir "
	
	#echo "end of PrepareFeat_1stLevel"
done

# -------------------------------------------------------------------------------------------------------- #
# Using MCFLIRT to correct hear rotation
# MCFLIRT loads the time-series in its entirity and will default to the middle volume as an initial template image

 #sessions2mcf="MI00487P MI00489P MI00491P MI00493P MI00496P MI00539P"

#for session in $sessions2mcf; do

	#sessionDir=$outDir/$monkey/$session
	#epiDir=$(find $studyDir/$monkey/$session -maxdepth 1 -d -name "ep2d*")
	
	#echo "correcting head rotation"
	#mcflirt -in $sessionDir/f_aligned_brain -out $sessionDir/f_aligned_brain_mcf -spline_final -plots -meanvol

	# here I rename f_aligned to f_aligned_premcf and rename the MCFLIRT output to f_aligned
	# I then save transformation parameters in the transform folder
	# note that you need to modify CreateNuisanceReg to concatenate MCF parameters with motion regressors
	#mv $sessionDir/f_aligned_brain.nii.gz $sessionDir/f_aligned_brain_preMCF.nii.gz
	#mv $sessionDir/f_aligned_brain_mcf.nii.gz $sessionDir/f_aligned_brain.nii.gz
	#mv $sessionDir/f_aligned_brain_mcf.par $studyDir/$monkey/$session/transform/mcfTransParam.par
	#rm $sessionDir/f_aligned_brain_mcf_mean_reg.nii.gz
	
	#echo "head rotation corrected"
#done       

# -------------------------------------------------------------------------------------------------------- #
# create nuisance regressor for all sessions in list (created above)
# (using a list avoids the slow process of repeatedly opening matlab for each session...)
# note: output dirs must exist already (typically created above in PrepareFinalData.sh call)
echo "	creating nuisance regressors for all sessions"
#$MATLABBIN/matlab -nodisplay -nosplash -r "addpath('$MRCATDIR/in_vivo/PreprocFunc_macaque/'); CreateNuisanceReg('$sessionList',$sdThresh,'$outputDirList',$doRecursive); exit"
$MATLABBIN/matlab -nodisplay -nosplash -r "addpath('/Users/nimakhalighinejad/Desktop/PreprocFunc_macaque/'); CreateNuisanceReg('$sessionList',$sdThresh,'$outputDirList',$doRecursive); exit"