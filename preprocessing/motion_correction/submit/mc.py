import os
from simple_slurm import Slurm
import shlex # Import shlex for safer quoting

# Determine the project root relative to this submission script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Module path (relative to project root, using dots)
module_path = "preprocessing.motion_correction.dontsb.mc"

def load_modules():
    module_load_command = "module load fsl" # Adjust if your HPC uses a different command
    return module_load_command

def mc_submit(episeries: str, t1wimg: str, t1wmask: str, log_dir="logs", job_name="motion_correction"):

    # Ensure paths are absolute before passing to Slurm, especially if chdir is used
    abs_episeries = os.path.abspath(episeries)
    abs_t1wimg = os.path.abspath(t1wimg)
    abs_t1wmask = os.path.abspath(t1wmask)

    # Define log paths relative to project root or use absolute paths
    os.makedirs(log_dir, exist_ok=True) # Ensure log directory exists
    log_basename = f"mc_{os.path.basename(abs_episeries)}"
    output_log = os.path.join(log_dir, f"{log_basename}.out")
    error_log = os.path.join(log_dir, f"{log_basename}.err")

    # Define the necessary module load command for your HPC
    module_load_command = load_modules()

    slurm = Slurm(
        job_name=job_name,
        partition="long",
        time="96:00:00",
        output=output_log, # Use absolute or relative-to-project path
        error=error_log,   # Use absolute or relative-to-project path
        mem='64G',
        cpus_per_task=4
    )

    # Construct the command to execute the module
    # Use shlex.quote for robust handling of paths with spaces/special chars
    command = (
        f"{module_load_command} && " # Load module first
        f"python -m {module_path} "  # Then run python script as module
        f"--episeries {shlex.quote(abs_episeries)} "
        f"--t1wimg {shlex.quote(abs_t1wimg)} "
        f"--t1wmask {shlex.quote(abs_t1wmask)}"
    )

    print(f"\033[92mSubmitting command to Slurm:\033[0m")
    print(f"\t{command}")

    job_id = slurm.sbatch(command)

    print(f"\033[92mSubmitted job with ID: {job_id}\033[0m")
    return job_id
