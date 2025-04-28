#!/usr/bin/env bash
umask u+rw,g+rw # give group read/write permissions to all new files
set -e    # stop immediately on error

#  IMPORTANT: you must have MRCATDIR set as global environment variable (in your .bash_profile) for scripts to run
#  MRCATDIR points to your local MrCat-dev directory

studyDir="/users/rushworth/gwr089/scratch/Generalization-Preprocess"
monkey="zach"
session="MI01049P"
sessionDir=$studyDir/$monkey/$session

# ---------------- #
# PREPARE RAW DATA
# ---------------- #

# NOTE: use argument --isrestingstate=1 (defaults to 0) to set up session folders only for resting state data (or only non-resting state data)

# sh $MRCATDIR/pipelines/PreprocFunc_macaque/PrepareRawData.sh --sessdir=$sessionDir --isrestingstate=1
sh $MRCATDIR/pipelines/PreprocFunc_macaque/PrepareRawData.sh --sessdir=$sessionDir
