import os
from preprocessing.prepare.dontsb.create_link import _create_link
from fsl.wrappers import fslreorient2std

def dontsb_func(input_file, output_dir):
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("Step 1: Creating link...")
    output_file = os.path.join(output_dir, "func.nii.gz")
    input_file = _create_link(input_file, output_file)
    
    print("Step 2: Reorienting to standard space...")
    output_file = os.path.join(output_dir, "func_reoriented.nii.gz")
    fslreorient2std(input_file, output_file)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, required=True)
    parser.add_argument("--output_dir", type=str, required=True)
    args = parser.parse_args()
    dontsb_func(args.input_file, args.output_dir)
