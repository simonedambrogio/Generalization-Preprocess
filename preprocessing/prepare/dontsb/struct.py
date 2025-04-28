import os
import shlex # For safely quoting arguments for the shell
import subprocess # For executing the command

def dontsb_struct(instructions, subjdir, **kwargs):
    """
    Constructs and executes the struct_macaque.sh command.

    Args:
        instructions: The specific step to run (e.g., "robustfov", "all").
        subjdir: Path to the subject directory.
        **kwargs: Optional settings corresponding to struct_macaque.sh arguments
                  (e.g., fovmm="128x128x64", config="/path/to/fnirt.cnf").
                  Keys should match the argument names in the shell script
                  (without the leading '--').

    Bash Help:
        Preprocess macaque structural MRI. Brain extraction, bias correction, and
        reference registration.

        example:
        struct_macaque.sh --subjdir=MAC1 --all
        struct_macaque.sh --subjdir=MAC1 --once
        struct_macaque.sh --subjdir=MAC1 --structImg=struct/struct --betorig --biascorr

        usage: struct_macaque.sh
        instructions:
            [--all] : execute all inctructions, twice: --robustfov --betorig --biascorr
            --betrestore --register --brainmask --biascorr --register --brainmask
            --segment
            [--once] : execute all instructions once: --robustfov --betorig --biascorr
            --betrestore --register --brainmask --segment
            [--robustfov] : robust field-of-view cropping
            [--betorig] : rough brain extraction of the original structural
            [--betrestore] : brain extraction of the restored structural
            [--biascorr] : correct the spatial bias in signal intensity
            [--register] : register to the reference and warp the refMask back
            [--brainmask] : retrieve the brain mask from the reference and polish
            [--segment] : segment the structural image in CSF, GM, and WM compartments
            [--hemimask] : create masks for each hemisphere (left/right)
        settings:
            [--subjdir=<subject dir>] default: <current directory>
            [--structdir=<structural dir>] default: <subjdir>/struct
            [--structimg=<structural image>] default: <structdir>/struct
            the <structdir> can be inferred from <structImg>, if provided
            [--structmask=<structural brain mask>] default: <structimg>_brain_mask
            [--transdir=<transform dir>] default: <subjdir>/transform
            [--scriptdir=<script dir>] default: <parent directory of struct_macaque.sh>
            path to bet_macaque.sh and robustfov_macaque.sh scripts
            [--refdir=<reference dir>] default: <inferred from refimg, or scriptdir>
            path to reference images
            [--fovmm=<XSIZExYSIZExZSIZE> default: 128x128x64
            field-of-view in mm, for robustfov_macaque
            [--config=<fnirt config file> default: <scriptdir>/fnirt_1mm.cnf
            [--refspace=<reference space name>] default: F99, alternative: SL, MNI
            [--refimg=<ref template image>] default: <scriptdir>/<refspace>/McLaren
            [--refmask=<reference brain mask>] default: <refimg>_brain_mask
            [--refweightflirt=<ref weights for flirt>] default <refmask>
            [--refmaskfnirt=<ref brain mask for fnirt>] default <refmask>
            [--flirtoptions]=<extra options for flirt>] default none
    """

    assert instructions in [
        "all", "once", "robustfov", "betorig", "betrestore", "biascorr", "register", "brainmask", "segment", "hemimask"
    ], "Invalid instruction"

    # check if $MRCATDIR is set
    mrcatdir = os.getenv("MRCATDIR")
    if not mrcatdir:
        raise ValueError("MRCATDIR environment variable is not set")

    script_path = os.path.join(mrcatdir, "core", "struct_macaque.sh")
    if not os.path.exists(script_path):
         raise FileNotFoundError(f"struct_macaque.sh not found at {script_path}")

    # Start building the command list for subprocess (safer than one long string)
    command_list = ['sh', script_path]

    
    # Add required/explicit arguments using --key=value format
    command_list.append(f"--subjdir={shlex.quote(subjdir)}")

    # Add optional settings from kwargs
    for key, value in kwargs.items():
        # Convert value to string and quote it for shell safety
        command_list.append(f"--{key}={shlex.quote(str(value))}")

    # Add the instruction argument at the end, prepending --
    command_list.append(f"--{shlex.quote(instructions)}")

    print(f"\nExecuting command:")
    # Join list with spaces for printing, but use the list for execution
    print(" ".join(command_list))
    print("-" * 30) # Separator

    # Execute the command
    try:
        # Using subprocess.run is generally preferred
        # Pass the current environment, ensuring MRCATDIR is available to the shell
        env = os.environ.copy()
        result = subprocess.run(command_list, check=True, capture_output=True, text=True, env=env)
        # print(command_list)
        print("Command STDOUT:")
        print(result.stdout)
        print("-" * 30) # Separator
        if result.stderr:
             print("Command STDERR:")
             print(result.stderr)
             print("-" * 30) # Separator
        print("Command finished successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Error executing command (Exit Code: {e.returncode})")
        print("STDOUT:")
        print(e.stdout)
        print("STDERR:")
        print(e.stderr)
        # Re-raise the error or handle it as needed
        raise e
    except FileNotFoundError:
         print(f"Error: 'sh' command not found or script path incorrect: {script_path}")
         raise # Re-raise

if __name__ == "__main__":
    
    """
    Example usage:
    python -m preprocessing.prepare.dontsb.struct \
        --instructions=all \
        --subjdir=/users/rushworth/gwr089/scratch/Generalization-Preprocess/zeno \
        --structimg=/users/rushworth/gwr089/scratch/Generalization-Preprocess/zeno/structural/mprage/structural_fov \
        --refspace=F99 \
        --refimg=$MRCATDIR/data/macaque/F99/McLaren
    """
    import argparse

    # Use ArgumentParser with add_help=False to handle possible "-h" or "--help" in kwargs
    parser = argparse.ArgumentParser(description="Wrapper for struct_macaque.sh.", add_help=False)
    # Define known arguments
    parser.add_argument("--instructions", type=str, required=True, help="Instructions to run (e.g., all, once, robustfov)")
    parser.add_argument("--subjdir", type=str, required=True, help="Subject directory")

    # Parse known args, leave the rest for kwargs
    args, unknown_args = parser.parse_known_args()

    # Process unknown arguments into a kwargs dictionary
    kwargs = {}
    i = 0
    while i < len(unknown_args):
        arg = unknown_args[i]
        if arg.startswith("--"):
            key_part = arg[2:] # Key part, might contain =value
            value = None

            # Check if the format is --key=value
            if '=' in key_part:
                key, value = key_part.split('=', 1)
            else:
                # Format is --key value or just --key (flag)
                key = key_part
                # Check if the next item is a value
                if i + 1 < len(unknown_args) and not unknown_args[i+1].startswith("--"):
                    value = unknown_args[i+1]
                    i += 1 # Consume the value argument
                # else: it's potentially a boolean flag or malformed, value remains None

            if value is not None:
                 kwargs[key] = value
            else:
                 # Handle boolean flags or arguments without values if necessary.
                 # struct_macaque.sh doesn't seem to use standalone flags other than instructions.
                 # We'll issue a warning for now if a value wasn't found.
                 print(f"Warning: Argument --{key} provided without a value or in unexpected format, skipping.")

        else:
            print(f"Warning: Unexpected argument format: {arg}, skipping.")
        i += 1

    # Call the function with parsed args and kwargs
    dontsb_struct(args.instructions, args.subjdir, **kwargs)