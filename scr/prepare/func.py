
import sys, os, yaml
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
sys.path.append(config['paths']['preprocess'])
import preprocessing.prepare as prepare

def main(config, monkey: str, session: str, submit: bool, log_dir: str, job_name: str):
    
    assert monkey in ["zach", "zeno"], "Monkey must be either zach or zeno"
    
    # Get the input ------------------------------------------------------------
    session_dir = os.path.join(config['paths']['reconstructed'], monkey, session)
    input_func = [f for f in os.listdir(session_dir) if "ep2d" in f and "nii.gz" in f][0]
    input_file = os.path.join(session_dir, input_func)
    # Get the output ------------------------------------------------------------
    output_dir = os.path.join(config['paths'][monkey], session, "epi2d")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = os.path.join(output_dir, "f.nii.gz")

    # Run the prepare function ---------------------------------------------------
    prepare.func(input_file, output_file, submit, log_dir, job_name)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--monkey", type=str, required=True)
    parser.add_argument("--session", nargs="+", type=str, required=False)
    parser.add_argument("--task", type=str, required=False)
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--log_dir", type=str, default="logs")
    parser.add_argument("--job_name", type=str, default="func")
    args = parser.parse_args()

    # Run the main function ------------------------------------------------------
    if args.session is None:
        sessions = config[args.monkey]['task' + args.task]
    else:
        sessions = args.session

    for session in sessions:
        jobname = f"fslreorient2std_{session}"
        log_dir = os.path.join(config['paths'][args.monkey], session, "logs")
        main(config, args.monkey, session, args.submit, log_dir, jobname)

"""
Example:
    python scr/prepare/func.py --monkey zach --session MI01049P --submit
    python scr/prepare/func.py --monkey zach --session MI01051P --submit
    
    python scr/prepare/func.py --monkey zach --task 2 --submit
    python scr/prepare/func.py --monkey zach --task 3 --submit
    python scr/prepare/func.py --monkey zach --task 4 --submit
    python scr/prepare/func.py --monkey zach --task 5 --submit
"""
