import os
from simple_slurm import Slurm
import shlex # Import shlex for safer quoting

# Determine the project root relative to this submission script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Module path (relative to project root, using dots)
module_path = "preprocessing.prepare.dontsb.func"

def load_modules():
    module_load_command = "module load fsl" # Adjust if your HPC uses a different command
    return module_load_command

def submit_func(input_file, output_file, log_dir="logs", job_name="func_prepare"):

    # Ensure paths are absolute before passing to Slurm, especially if chdir is used
    abs_input_file = os.path.abspath(input_file)
    abs_output_file = os.path.abspath(output_file)

    # Define log paths relative to project root or use absolute paths
    os.makedirs(log_dir, exist_ok=True) # Ensure log directory exists
    log_basename = f"func_{os.path.basename(abs_input_file)}"
    output_log = os.path.join(log_dir, f"{log_basename}.out")
    error_log = os.path.join(log_dir, f"{log_basename}.err")

    # Define the necessary module load command for your HPC
    module_load_command = load_modules()

    slurm = Slurm(
        job_name=job_name,
        partition="short",
        time="0:05:00",
        output=output_log, # Use absolute or relative-to-project path
        error=error_log,   # Use absolute or relative-to-project path
        mem='4G'
    )

    # Construct the command to execute the module
    # Use shlex.quote for robust handling of paths with spaces/special chars
    command = (
        f"{module_load_command} && " # Load module first
        f"python -m {module_path} "  # Then run python script as module
        f"--input_file {shlex.quote(abs_input_file)} "
        f"--output_file {shlex.quote(abs_output_file)}"
    )

    print(f"\033[92mSubmitting command to Slurm:\033[0m")
    print(f"\t{command}")

    job_id = slurm.sbatch(command)

    print(f"\033[92mSubmitted job with ID: {job_id}\033[0m")
    return job_id

# Example of how you might call this (outside the function)
# if __name__ == "__main__":
#     input_example = "/path/to/your/input.nii.gz"
#     output_example = "/path/to/your/output_directory"
#     submit_func(input_example, output_example)
