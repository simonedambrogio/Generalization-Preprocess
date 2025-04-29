# Generalization-Preprocess

A Python-based pipeline for preprocessing macaque NHP fMRI data, designed for submission to SLURM clusters. This repository provides tools to automate steps outlined in traditional NHP fMRI preprocessing guides, leveraging Python wrappers around core shell scripts from the MrCat toolbox and ANTs.

## Overview

This pipeline facilitates the preprocessing of structural and functional NHP MRI data. It breaks down the process into distinct stages:

1.  **Structural Preparation:** Preprocessing the T1w structural image (FOV cropping, bias correction, brain extraction, registration to reference).
2.  **Functional Reorientation:** Reorienting the functional EPI image to match the FSL standard orientation (MNI152). This is often a preliminary step to ensure consistent orientation before further processing or registration.
3.  **Motion Correction:** Aligning EPI volumes to correct for motion-induced distortions.
4.  **Functional-to-Structural Registration:** Aligning the mean functional image to the preprocessed structural image.

Each stage is implemented as a Python module within the `preprocessing` directory. These modules provide functions that can either execute the underlying shell scripts directly or submit them as jobs to a SLURM cluster. The scripts in the `scr` directory utilize these modules to orchestrate the pipeline for specific datasets.

## Prerequisites

This pipeline relies on several external software packages and a specific environment setup.

**Software:**

*   **Unix-like Environment:** Linux or macOS.
*   **Python:** Version 3.x.
*   **Core Neuroimaging Tools:**
    *   **FSL:** (FMRIB Software Library) - Essential for many neuroimaging operations.
    *   **ANTs:** (Advanced Normalization Tools) - Used for registration steps.
    *   **MrCat Toolbox:** The underlying shell scripts (`struct_macaque.sh`, `Reconstruction_macaque.sh`, `MotionCorrection_macaque.sh`, `RegisterFuncStruct_macaque.sh`, etc.) are assumed to come from this or a similar NHP processing suite. Ensure this is installed and accessible.
    *   **MATLAB:** Required by some underlying scripts. Check the requirements of the specific shell scripts being called.
*   **SLURM Workload Manager:** Access to an HPC cluster running SLURM is required for job submission features.

**Environment Setup:**

Correct environment variable setup is **CRITICAL** for the underlying shell scripts to function correctly when called from Python. Configure these in your shell profile (e.g., `~/.bashrc`, `~/.bash_profile`, `~/.zshrc`):

*   **`$PATH`:** Ensure the `bin` directories for FSL, ANTs, MATLAB (if needed), and potentially MrCat scripts are included in your system's `$PATH`.
*   **`$FSLDIR`:** Points to your FSL installation directory. FSL setup usually handles this.
*   **`$ANTSPATH`:** Points to your ANTs installation directory (containing binaries like `antsRegistration`, `antsApplyTransforms`).
*   **`$MRCATDIR`:** Points to the root directory of the MrCat (or equivalent) toolbox installation. Your Python scripts rely on this to find the shell scripts.
*   **`$MATLABBIN`:** (If MATLAB is required) Points to the `bin` directory of your MATLAB installation.

**Verification:** After setting up environment variables, open a *new* terminal and test that you can run commands like `fslinfo`, `antsRegistration`, and potentially `matlab` directly. Also, verify `$MRCATDIR` is set correctly (`echo $MRCATDIR`).

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd Generalization-Preprocess
    ```
2.  **Install Python dependencies:**
    ```bash
    pip install simple_slurm
    # Add any other dependencies if needed
    ```
3.  **Ensure Prerequisites:** Verify all software prerequisites and environment variables are set up correctly as described above.

## Directory Structure

The pipeline assumes a specific input directory structure, similar to the one described in the NHP guide:

```
<studyDir>/
├── <monkey_name>/             # e.g., zeno
│   ├── structural/
│   │   └── mprage/            # Contains T1w NIfTI files (e.g., structural.nii.gz)
│   ├── <session_name>/        # e.g., MI01049P
│   │   └── ep2d/              # Contains functional EPI NIfTI files (e.g., f.nii.gz)
│   ├── <session_name_2>/
│   │   └── ...
│   └── ...
├── <monkey_name_2>/
│   └── ...
└── ...
```

*   `<studyDir>`: The root directory for the study.
*   `<monkey_name>`: Directory for each individual subject.
*   `structural/mprage/`: Contains the high-resolution T1w image(s). The scripts often expect specific naming conventions (e.g., `structural.nii.gz`, producing `structural_restore.nii.gz`, `structural_restore_brain.nii.gz`).
*   `<session_name>`: Directory for each imaging session.
*   `ep2d/`: Contains the 4D functional EPI timeseries data (e.g., `f.nii.gz`). Assumes one primary EPI series per session folder after initial preparation.

Output files and transformations are typically written back into these directories or into specified output/log directories.

## Workflow and Usage

The preprocessing pipeline is executed step-by-step by calling functions within the `preprocessing` modules. You would typically use scripts within the `scr` directory to call these functions for your specific subjects and sessions.

The core functions generally accept parameters to control execution and job submission:

*   `input_file` / `subjdir` / `episeries`: Path(s) to the relevant input data or directories.
*   `submit`: Boolean flag (or similar mechanism). If `True`, the step is submitted as a SLURM job via the corresponding `preprocessing.*.submit` module. If `False`, it will run directly via the `preprocessing.*.dontsb` module.
*   `log_dir`: Directory to store SLURM output/error logs.
*   `job_name`: Name for the SLURM job.
*   `**kwargs`: Additional optional arguments passed directly to the underlying shell script (e.g., `structimg`, `refspace`, `fovmm`).

**Step 1: Prepare Structural Image**

*   **Module:** `preprocessing.prepare.struct` (likely called by a script in `scr/prepare/`)
*   **Underlying Script:** `struct_macaque.sh` (or similar)
*   **Purpose:** Performs FOV cropping, bias correction, brain extraction, and registration of the T1w image to a reference space (e.g., F99).
*   **Example Call (Conceptual - adapt based on your scripts in `scr`):**
    ```python
    from preprocessing.prepare.submit import struct as submit_struct # Assuming submit variant
    # Or: from preprocessing.prepare.dontsb import struct as dontsb_struct

    submit_struct.submit_struct(
        input_file="/path/to/<studyDir>/<monkey_name>", # Typically the subject dir
        output_file=None, # Output often handled by script, passed via kwargs if needed
        log_dir="path/to/logs/struct",
        job_name="struct_prep_<monkey>",
        # Kwargs for struct_macaque.sh:
        instructions="all", # e.g., 'all', 'robustfov', 'biascorr'
        structimg="/path/to/<studyDir>/<monkey_name>/structural/mprage/structural", # Base name
        refspace="F99",
        refimg="/path/to/MrCat/data/macaque/F99/McLaren"
        # ... other kwargs like fovmm, config ...
    )
    ```

**Step 2: Functional Reorientation**

*   **Module:** `preprocessing.prepare.func` (Or submit/dontsb variants)
*   **Underlying Script/Tool:** `fslreorient2std` (from FSL)
*   **Purpose:** Reorients the functional EPI image to match the FSL standard orientation (MNI152). This is often a preliminary step to ensure consistent orientation before further processing or registration.
*   **Example Call (Conceptual):**
    ```python
    # Assuming similar submit/dontsb structure exists for func reorient
    from preprocessing.prepare.submit import func as submit_func_reorient

    submit_func_reorient.submit_func(
        input_file="/path/to/input/func_image.nii.gz", # e.g., the output of reconstruction
        output_file="/path/to/output/func_reoriented.nii.gz",
        log_dir="path/to/logs/func_reorient",
        job_name="func_reorient_<session>"
        # kwargs are likely not applicable for fslreorient2std via this wrapper
    )
    ```

**Step 3: Motion Correction**

*   **Module:** `preprocessing.motion_correction.run` (Or submit/dontsb variants)
*   **Underlying Script:** `MotionCorrection_macaque.sh` (or similar)
*   **Purpose:** Performs slice-by-slice alignment of the 4D EPI timeseries to a reference volume derived from the series itself, correcting for motion-induced field distortions. Generates motion parameter outputs.
*   **Example Call (Conceptual):**
    ```python
    # Assuming similar submit/dontsb structure exists for motion
    from preprocessing.motion_correction.submit import run as submit_motion

    submit_motion.submit_motion(
        episeries="/path/to/<studyDir>/<monkey_name>/<session_name>/ep2d/f", # Base name of reconstructed EPI
        t1wimg="/path/to/<studyDir>/<monkey_name>/structural/mprage/structural_restore", # Preprocessed T1w
        t1wmask="/path/to/<studyDir>/<monkey_name>/structural/mprage/structural_restore_brain_mask", # T1w Mask
        log_dir="path/to/logs/motion",
        job_name="motion_<session>",
        # Kwargs for MotionCorrection_macaque.sh (if any)
    )
    ```

**Step 4: Functional to Structural Registration**

*   **Module:** `preprocessing.func2struct.run` (Or submit/dontsb variants)
*   **Underlying Script:** `RegisterFuncStruct_macaque.sh` (or similar)
*   **Purpose:** Registers the mean functional image (e.g., `f_mean.nii.gz` created during motion correction) to the subject's preprocessed structural image (T1w). Generates transformation warps.
*   **Example Call (Conceptual):**
    ```python
    # Assuming similar submit/dontsb structure exists for func2struct
    from preprocessing.func2struct.submit import run as submit_f2s

    submit_f2s.submit_f2s(
        episeries="/path/to/<studyDir>/<monkey_name>/<session_name>/ep2d/f_mean", # Mean EPI image
        t1wimg="/path/to/<studyDir>/<monkey_name>/structural/mprage/structural_restore", # Preprocessed T1w
        t1wmask="/path/to/<studyDir>/<monkey_name>/structural/mprage/structural_restore_brain_mask", # T1w Mask
        log_dir="path/to/logs/func2struct",
        job_name="f2s_<session>",
        # Kwargs for RegisterFuncStruct_macaque.sh (if any)
    )
    ```

**Job Monitoring and Logs:**

*   Submitted jobs can be monitored using standard SLURM commands (`squeue`, `sacct`).
*   Output (`.out`) and error (`.err`) logs for each job will be saved in the specified `log_dir`. Check these files carefully, especially if a job fails.

## Important Notes

*   **Manual Checks:** As emphasized in the original NHP guide, **manual quality control is essential** at various stages (e.g., checking structural brain masks, motion correction quality, registration results) using tools like `fsleyes`. This pipeline automates execution, not quality assessment.
*   **Underlying Scripts:** This package primarily wraps existing shell scripts. Understanding the behavior, inputs, and outputs of those original scripts (`struct_macaque.sh`, `MotionCorrection_macaque.sh`, etc.) is crucial for effective use and troubleshooting.
*   **Configuration:** Adapt paths, SLURM parameters (`partition`, `time`, `mem`), and optional arguments (`kwargs`) in the calling scripts (within `scr/` likely) to match your specific data and cluster environment.

