import os
from simple_slurm import Slurm
import shlex # Import shlex for safer quoting

# Determine the project root relative to this submission script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Module path (relative to project root, using dots)
module_path = "preprocessing.prepare.dontsb.firstlevel"

def load_modules():
    module_load_command = "module load fsl" # Adjust if your HPC uses a different command
    return module_load_command

def submit_firstlevel(
    sessdir: str, 
    epidir: str, 
    transdir: str, 
    outputdir: str, 
    standimg: str, 
    struct2standwarp: str,
    log_dir: str = "logs",
    job_name: str = "firstlevel"
):
    log_dir = os.path.join(sessdir, "logs") if log_dir == "logs" else log_dir
    os.makedirs(log_dir, exist_ok=True) # Ensure log directory exists
    log_basename = f"firstlevel_{os.path.basename(sessdir)}"
    output_log = os.path.join(log_dir, f"{log_basename}.out")
    error_log = os.path.join(log_dir, f"{log_basename}.err")
    
    # Create a Slurm job
    slurm = Slurm(
        job_name=job_name,
        partition="short",   
        time="12:00:00",
        cpus_per_task=4,
        mem="32G",
        output=output_log,
        error=error_log
    )
    
    
    module_load_command = load_modules()
    
    command = (
        f"{module_load_command} && "
        f"python -m {module_path} "
        f"--sessdir={shlex.quote(sessdir)} "
        f"--epidir={shlex.quote(epidir)} "
        f"--transdir={shlex.quote(transdir)} "
        f"--outputdir={shlex.quote(outputdir)} "
        f"--standimg={shlex.quote(standimg)} "
        f"--struct2standwarp={shlex.quote(struct2standwarp)}"
    )
    
    
    print(f"\033[92mSubmitting command to Slurm:\033[0m")
    print(f"\t{command}")

    job_id = slurm.sbatch(command)

    print(f"\033[92mSubmitted job with ID: {job_id}\033[0m")
    return job_id
