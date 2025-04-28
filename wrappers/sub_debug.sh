#!/bin/bash

#SBATCH --job-name=debug_imagemath
#SBATCH --output=debug_imagemath_%j.out
#SBATCH --error=debug_imagemath_%j.err
#SBATCH --time=00:30:00       # 30 minutes should be enough
#SBATCH --cpus-per-task=1     # CompCorr might not use many cores effectively
#SBATCH --mem=32G             # Request 32 GB memory

echo "Job started on $(hostname) at $(date)"
echo "Memory allocated: $SLURM_MEM_PER_NODE MB"

# --- Environment Setup ---
# Add any 'module load' commands here if needed

# --- Run Debug Script ---
bash /users/rushworth/gwr089/scratch/Generalization-Preprocess/debug_ImageMath_CompCorr.sh
EXIT_CODE=$?

echo "Job finished at $(date) with exit code $EXIT_CODE"
exit $EXIT_CODE