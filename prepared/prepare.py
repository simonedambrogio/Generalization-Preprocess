import sys, os, yaml
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import preprocessing.prepare as prepare

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

def main(config, monkey, session, submit):
    
    # Get the input ------------------------------------------------------------
    session_dir = os.path.join(config['paths']['reconstructed'], monkey, session)
    input_func = [f for f in os.listdir(session_dir) if "ep2d" in f and "nii.gz" in f][0]
    input_file = os.path.join(session_dir, input_func)
    # Get the output ------------------------------------------------------------
    output_dir = os.path.join(config['paths']['prepared'], monkey, session)

    # Run the prepare function ---------------------------------------------------
    prepare.func(input_file, output_dir, submit)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--monkey", type=str, required=True)
    parser.add_argument("--session", type=str, required=True)
    parser.add_argument("--submit", action="store_true")
    args = parser.parse_args()

    main(config, args.monkey, args.session, args.submit)

"""
python prepared/prepare.py --monkey zach --session MI01049P --submit
"""