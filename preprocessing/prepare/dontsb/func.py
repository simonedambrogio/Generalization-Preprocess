import os
from fsl.wrappers import fslreorient2std

def dontsb_func(input_file, output_file):
    print("Reorienting to standard space...")
    fslreorient2std(input_file, output_file)
    print("done.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, required=True)
    parser.add_argument("--output_file", type=str, required=True)
    args = parser.parse_args()
    dontsb_func(args.input_file, args.output_file)
