import os

def _create_link(input_file, output_file):
    
    if not os.path.lexists(output_file):
        os.symlink(
            input_file, 
            output_file)
    else:
        print(f"Link already exists. Skipping...")
    
    return output_file

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, required=True)
    parser.add_argument("--output_file", type=str, required=True)
    args = parser.parse_args()
    _create_link(args.input_file, args.output_file)
