#!/bin/bash

#SBATCH --job-name=motion_corr_zach      # Descriptive job name
#SBATCH --output=motion_corr_zach_%j.out # Standard output log (%j expands to job ID)
#SBATCH --error=motion_corr_zach_%j.err  # Standard error log (%j expands to job ID)
#SBATCH --time=96:00:00                  # Estimated Wall clock time (HH:MM:SS)
#SBATCH --partition=long                  # Use the long partition for longer jobs
#SBATCH --cpus-per-task=4                # Request 4 CPUs
#SBATCH --mem=16G                        # Request 16 GB of memory per node

# --- Environment Setup ---
echo "Setting up environment..."
module load fsl

# --- Job Information ---
echo "Job ID: $SLURM_JOB_ID"
echo "Job Name: $SLURM_JOB_NAME"
echo "Running on host: $(hostname)"
echo "Running on node: $SLURMD_NODENAME"
echo "Working directory: $(pwd)"
echo "Allocated CPUs: $SLURM_CPUS_PER_TASK"
echo "Allocated Memory: $SLURM_MEM_PER_NODE MB"

# --- Define Script ---
# Make sure the path to your wrapper script is correct
SCRIPT_TO_RUN="/users/rushworth/gwr089/scratch/Generalization-Preprocess/wrappers/WrapperMotionCorrection_macaque.sh"
echo "Script to run: $SCRIPT_TO_RUN"

# --- Execute Script ---
echo "Starting script execution at $(date)"

# Run the wrapper script
bash "$SCRIPT_TO_RUN"
EXIT_CODE=$? # Capture the exit code of the script

echo "Script finished at $(date) with exit code: $EXIT_CODE"

# Exit the SLURM job with the script's exit code
exit $EXIT_CODE