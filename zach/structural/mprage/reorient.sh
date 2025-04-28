#!/bin/bash

echo "Copying from backup to structural_reset.nii.gz"
cp ZACH_20221207_001_100_Arithmetic_Mean_MEAN_MPRAGE.nii.gz structural_reset.nii.gz

echo "Deleting existing orientation information..."
fslorient -deleteorient structural_reset.nii.gz

echo "Setting standard qform code..."
# This sets the interpretation to standard (likely RAS)
fslorient -setqformcode 1 structural_reset.nii.gz
# Optionally add sform code back too for robustness:
# fslorient -setsformcode 1 structural_reset.nii.gz

echo "Flipping Left/Right (X-axis)..."
# Perform the flip on the reset file, save to a new final file
fslswapdim structural_reset.nii.gz -x y z structural_fov.nii.gz

echo "Removing the intermediate files..."
rm structural_reset.nii.gz

echo "Check the orientation of structural_fov.nii.gz in FSLeyes."
echo "Done."
