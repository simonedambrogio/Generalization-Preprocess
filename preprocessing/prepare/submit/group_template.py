import os
from simple_slurm import Slurm
import shlex # Import shlex for safer quoting

# Determine the project root relative to this submission script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Module path (relative to project root, using dots)
module_path = "preprocessing.prepare.dontsb.group_template"

def load_modules():
    module_load_command = "module load fsl" # Adjust if your HPC uses a different command
    return module_load_command


def submit_grouptemplate(
    inputdir, 
    monkeylist, 
    outputdir, 
    refimg, 
    inputsubpath='', 
    suffixbiascorr='_restore', 
    suffixbrain='_brain', 
    suffixmask='_mask',
    niter=6, 
    flgtemplate=1, 
    flgantsreg=1, 
    t1wbase='structural', 
    refmask=None, 
    useniter=None,
    log_dir="logs", 
    job_name="group_template"):
    """
    Reorient and resample a structural image to the standard space.
    obligatory:

    --inputdir=<dir>
        This is the group/study directory which contains a folder for each animal, which holds that animal's 
        T1w image and mask. This script assumes: 
          inputdir/animal_1_dir/[T1wImage, T1wMask]
          inputdir/animal_2_dir/[T1wImage, T1wMask] 
          etc.

    --monkeylist=<double quoted variable>
        A variable (in double quotes "") pointing to space-separated string of animal (folder) names> 
        E.g., "$mylist" (where mylist="animal_1_dir animal_2_dir animal_3_dir")
        The double quotes ensure that the full list is passed along!

    --outputdir=<dir>
        The output directory which will store group templates, transforms etc.
        This will be created if does not already exist.

    --refimg=<reference img>
        This points to the desired reference image to be used for the group template.
        This script assumes that there is also a mask for this reference in the place
        (see also refmask argument below).

  optional:

    --inputsubpath=<string> (default: '')
        The sub-path, if any, between top-level monkey dir and actual structural images
        e.g., /studydir/monkey/inputsubpath/structural.nii

    --refmask=<reference brain mask img> (default: "$refimg"_mask)
        The reference brain mask image.

    --niter=<1 to 6> (default: 6)
        The number of iterations to run for group template creation:
          (1) Initially register to reference
          (2) Create group template
          (3) Register to group template
          Repeat steps (2) and (3) [1-6] number of times...

          Note that a group template is provided for each iteration. 

    --useniter=<1 to 6> (default: niter)
        Which iteration to use to create ANTs struct2stand transform 

    --flgtemplate=<0,1> (default: 1)
        run group template script 

    --flgantsreg=<0,1> (default: 1)
        run ANTs struct2stand registration 
        (i.e, if group template already exists)

    --t1wbase=<string> (default: "structural")
        Basename of T1w image that script will look for within each animal directory

    --suffixbiascorr=<string> (default: "_restore")
        A substring that is appended to identify bias-corrected (restored)
        images.

    --suffixbrain=<string> (default: "_brain")
        A substring that is appended to identify brain extracted images.

    --suffixmask=<string> (default: "_mask")
        A substring that is appended to identify binary brain masks.
    """
    
    refmask = refimg + suffixmask if refmask is None else refmask
    useniter = niter if useniter is None else useniter
    
    # Define log paths relative to project root or use absolute paths
    log_dir = os.path.join(outputdir, "logs") if log_dir == "logs" else log_dir
    os.makedirs(log_dir, exist_ok=True) # Ensure log directory exists
    log_basename = f"group_template_{os.path.basename(inputdir)}"
    output_log = os.path.join(log_dir, f"{log_basename}.out")
    error_log = os.path.join(log_dir, f"{log_basename}.err")
    

    # Define the necessary module load command for your HPC
    module_load_command = load_modules()

    slurm = Slurm(
        job_name=job_name,
        partition="short",
        time="04:00:00",   # 4 hours
        output=output_log, # Use absolute or relative-to-project path
        error=error_log,   # Use absolute or relative-to-project path
        mem='16G',
        cpus_per_task=4
    )

    # Construct the command to execute the module
    # Use shlex.quote for robust handling of paths with spaces/special chars
    if isinstance(monkeylist, list):
        monkeylist = " ".join(monkeylist)
        
    command = (
        f"{module_load_command} && " # Load module first
        f"python -m {module_path} "  # Then run python script as module
        f"--inputdir {shlex.quote(inputdir)} "
        f"--monkeylist {shlex.quote(monkeylist)} "
        f"--outputdir {shlex.quote(outputdir)} "
        f"--refimg {shlex.quote(refimg)} "
        f"--inputsubpath {shlex.quote(inputsubpath)} "
        f"--refmask {shlex.quote(refmask)} "
        f"--niter {niter} "
        f"--useniter {useniter} "
        f"--flgtemplate {flgtemplate} "
        f"--flgantsreg {flgantsreg} "
        f"--t1wbase {t1wbase} "
        f"--suffixbiascorr {suffixbiascorr} "
        f"--suffixbrain {suffixbrain} "
        f"--suffixmask {suffixmask}"
    )

    print(f"\033[92mSubmitting command to Slurm:\033[0m")
    print(f"\t{command}")

    job_id = slurm.sbatch(command)

    print(f"\033[92mSubmitted job with ID: {job_id}\033[0m")
    return job_id
    
    