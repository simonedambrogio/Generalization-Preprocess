#!/bin/bash

monkeylist="zach zeno"

#  study dir with folders named "pugsley", "pringle", etc.
inputdir=/users/rushworth/gwr089/scratch/Generalization-Preprocess

# name of desired output directory (will be created if does not exist)
outputdir=/users/rushworth/gwr089/scratch/Generalization-Preprocess/template

# reference image (McLaren template in F99 space)
refimg=$MRCATDIR/data/macaque/F99/McLaren.nii.gz

sh $MRCATDIR/pipelines/PreprocFunc_macaque/group_template/groupTemplate.sh \
    --monkeylist="$monkeylist" \
    --inputdir=$inputdir \
    --inputsubpath=structural/mprage \
    --outputdir=$outputdir \
    --refimg=$refimg