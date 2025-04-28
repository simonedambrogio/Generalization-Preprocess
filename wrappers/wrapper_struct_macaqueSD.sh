#!/usr/bin/env bash
set -e    # stop immediately on error
umask u+rw,g+rw # give group read/write permissions to all new files

# A wrapper to preprocess macaque structural images, looping over subjects.
#   1. brain extraction
#   2. bias correction
#   3. reference registration
# These steps are dependent on each other and could therefore be repeated for
# the best results.
#
# Please edit the hard-coded folder definitions and the <subjList>


# retrieve directory of this script
scriptDir="$(cd "$( dirname ${BASH_SOURCE[0]} )" && pwd)"

# find the path to MrCat script library
# [[ -z $MRCATDIR ]] && export MRCATDIR=$(cd $scriptDir/.. && pwd)
# MRCATDIR="$HOME/scratch/MrCat-dev"
# MRCATDIR="$HOME/code/MrCat-dev"

# in this example the subject data is also in the scriptDir
studyDir="/users/rushworth/gwr089/scratch/Generalization-Preprocess"

# space delineated list of subjects
subjList="zeno"

# determine if this script is run locally or on the jalapeno cluster
cmd="echo" # by default: send command to standard output
# [[ $OSTYPE == "linux-gnu" ]] && cmd="fsl_sub -q short.q -N structmac" # when on linux: submit the job to the jalapeno cluster
# [[ $OSTYPE == "darwin"* ]] && cmd="" # when on a Mac: run locally

# loop over subjects
for subj in $subjList ; do

  # preprocess the structural image 
  sh $MRCATDIR/core/struct_macaque.sh \
    --all \
    --subjdir=$studyDir/$subj \
    --structimg=$studyDir/$subj/structural/mprage/structural_fov \
    --refspace=F99 \
    --refimg=$MRCATDIR/data/macaque/F99/McLaren
done


sh /well/rushworth/projects/nhp/softwares/MrCat-win/core/struct_macaque.sh \
    --subjdir=/users/rushworth/gwr089/scratch/Generalization-Preprocess/zeno \
    --structimg=/users/rushworth/gwr089/scratch/Generalization-Preprocess/zeno/structural/mprage/structural_fov \
    --refspace=F99 \
    --refimg=/well/rushworth/projects/nhp/softwares/MrCat-win/data/macaque/F99/McLaren \
    all
