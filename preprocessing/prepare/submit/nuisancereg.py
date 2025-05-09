import os
from simple_slurm import Slurm
import shlex # Import shlex for safer quoting

# Determine the project root relative to this submission script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Module path (relative to project root, using dots)
module_path = "preprocessing.prepare.dontsb.nuisancereg"

def load_modules():
    module_load_command = "module load fsl" # Adjust if your HPC uses a different command
    return module_load_command

def submit_nuisancereg(sessiondir,sdthr,outputdir,dorecursive,dobadvol,domotioncomp,domelodiccomp,epidir, log_dir="logs", job_name="nuisancereg"):

    # Define log paths relative to project root or use absolute paths
    log_dir = os.path.join(sessiondir, 'logs')
    os.makedirs(log_dir, exist_ok=True) # Ensure log directory exists
    log_basename = f"nuisancereg_{os.path.basename(sessiondir)}"
    output_log = os.path.join(log_dir, f"{log_basename}.out")
    error_log = os.path.join(log_dir, f"{log_basename}.err")

    # Define the necessary module load command for your HPC
    module_load_command = load_modules()

    slurm = Slurm(
        job_name=job_name,
        partition="short",
        time="0:10:00",
        output=output_log, # Use absolute or relative-to-project path
        error=error_log,   # Use absolute or relative-to-project path
        mem='4G',
        cpus_per_task=4
    )

    # Construct the command to execute the module
    # Use shlex.quote for robust handling of paths with spaces/special chars
    command = (
        f"{module_load_command} && " # Load module first
        f"python -m {module_path} "  # Then run python script as module
        f"--sessiondir {shlex.quote(sessiondir)} "
        f"--outputdir {shlex.quote(outputdir)} "
        f"--sdthr {sdthr} "
        f"--dorecursive {dorecursive} "
        f"--dobadvol {dobadvol} "
        f"--domotioncomp {domotioncomp} "
        f"--domelodiccomp {domelodiccomp} "
        f"--epidir {epidir}"
    )

    print(f"\033[92mSubmitting command to Slurm:\033[0m")
    print(f"\t{command}")

    job_id = slurm.sbatch(command)

    print(f"\033[92mSubmitted job with ID: {job_id}\033[0m")
    return job_id
