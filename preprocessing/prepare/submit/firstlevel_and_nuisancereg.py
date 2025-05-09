import os
from simple_slurm import Slurm
import shlex # Import shlex for safer quoting

# Determine the project root relative to this submission script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Module path (relative to project root, using dots)
firstlevel_module_path = "preprocessing.prepare.dontsb.firstlevel"
nuisancereg_module_path = "preprocessing.prepare.dontsb.nuisancereg"

def load_modules():
    module_load_command = "module load fsl" # Adjust if your HPC uses a different command
    return module_load_command

def submit_firstlevel_and_nuisancereg(
    sessdir, epidir, transdir, outputdir, standimg, struct2standwarp,
    sdthr, dorecursive, dobadvol, domotioncomp, domelodiccomp,
    log_dir=None, job_name="firstlevel&nuisancereg"):

    # Define log paths relative to project root or use absolute paths
    log_dir = os.path.join(sessdir, 'logs') if log_dir is None else log_dir
    os.makedirs(log_dir, exist_ok=True) # Ensure log directory exists
    output_log = os.path.join(log_dir, job_name + ".out")
    error_log = os.path.join(log_dir, job_name + ".err")

    # Define the necessary module load command for your HPC
    module_load_command = load_modules()

    slurm = Slurm(
        job_name=job_name,
        partition="short",
        time="0:40:00",
        output=output_log, # Use absolute or relative-to-project path
        error=error_log,   # Use absolute or relative-to-project path
        mem='8G',
        cpus_per_task=4
    )

    # Construct the command to execute the module
    # Use shlex.quote for robust handling of paths with spaces/special chars
    command = (
        f"{module_load_command} && "
        # firstlevel
        f"python -m {firstlevel_module_path} "
        f"--sessdir={shlex.quote(sessdir)} "
        f"--epidir={shlex.quote(epidir)} "
        f"--transdir={shlex.quote(transdir)} "
        f"--outputdir={shlex.quote(outputdir)} "
        f"--standimg={shlex.quote(standimg)} "
        f"--struct2standwarp={shlex.quote(struct2standwarp)}"
        f" && "
        # nuisancereg
        f"python -m {nuisancereg_module_path} "
        f"--sessiondir {shlex.quote(sessdir)} "
        f"--outputdir {shlex.quote(outputdir)} "
        f"--sdthr {sdthr} "
        f"--dorecursive {dorecursive} "
        f"--dobadvol {dobadvol} "
        f"--domotioncomp {domotioncomp} "
        f"--domelodiccomp {domelodiccomp} "
        f"--epidir {shlex.quote(epidir)}"
    )

    print(f"\033[92mSubmitting command to Slurm:\033[0m")
    print(f"\t{command}")

    job_id = slurm.sbatch(command)

    print(f"\033[92mSubmitted job with ID: {job_id}\033[0m")
    return job_id