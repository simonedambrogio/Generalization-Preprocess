
import sys, os, yaml
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
sys.path.append(config['paths']['preprocess'])
import preprocessing.prepare as prepare

def main(config, monkey: str, session: str, submit: bool, instructions: str, log_dir: str, job_name: str):
    
    assert monkey in ["zach", "zeno"], "Monkey must be either zach or zeno"
    
    # Get the input ------------------------------------------------------------
    session_dir = os.path.join(config['paths']['reconstructed'], monkey, session)
    input_struct = [f for f in os.listdir(session_dir) if "mprage" in f and "nii.gz" in f][0]
    input_file = os.path.join(session_dir, input_struct)
    # Get the output ------------------------------------------------------------
    output_dir = os.path.join(config['paths'][monkey], session, "structural")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Run the prepare function ---------------------------------------------------
    prepare.struct(input_file, submit, instructions, log_dir, job_name)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--monkey", type=str, required=True)
    parser.add_argument("--session", nargs="+", type=str, required=True)
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--instructions", type=str, default="all")
    parser.add_argument("--log_dir", type=str, default="logs")
    parser.add_argument("--job_name", type=str, default="struct")
    args = parser.parse_args()

    # Run the main function ------------------------------------------------------
    for session in args.session:
        jobname = f"struct_{session}"
        log_dir = os.path.join(config['paths'][args.monkey], session, "logs")
        main(config, args.monkey, session, args.submit, 
             args.instructions, log_dir, jobname, 
             refspace="F99", refimg="$MRCATDIR/data/macaque/F99/McLaren")

"""
Example:
    python scr/prepare/struct.py --monkey zach --session MI01049P --submit
    python scr/prepare/struct.py --monkey zach --session MI01051P --submit --instructions all
"""
