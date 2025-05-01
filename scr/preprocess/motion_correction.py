
import sys, os, yaml
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
sys.path.append(config['paths']['preprocess'])
import preprocessing.motion_correction as motion_correction

def main(config, monkey: str, session: str, submit: bool, log_dir: str, job_name: str):
    
    assert monkey in ["zach", "zeno"], "Monkey must be either zach or zeno"
    
    # Get the inputs ------------------------------------------------------------
    episeries = os.path.join(config['paths'][monkey], session, "epi2d", "f.nii.gz")
    t1wimg = os.path.join(config['paths'][monkey], "structural", "mprage", "structural_restore.nii.gz")
    t1wmask = os.path.join(config['paths'][monkey], "structural", "mprage", "structural_brain_mask.nii.gz")

    # Run the prepare function ---------------------------------------------------
    motion_correction.run(episeries, t1wimg, t1wmask, submit, log_dir, job_name)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--monkey", type=str, required=True)
    parser.add_argument("--session", nargs="+", type=str, required=False)
    parser.add_argument("--task", type=str, required=False)
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--log_dir", type=str, default="logs")
    parser.add_argument("--job_name", type=str, default="motion_correction")
    args = parser.parse_args()

    # Run the main function ------------------------------------------------------
    if args.session is None:
        sessions = config[args.monkey]['task' + args.task]
    else:
        sessions = args.session

    for session in sessions:
        job_name = f"mc_{session}"
        log_dir = os.path.join(config['paths'][args.monkey], session, "logs")
        main(config, args.monkey, session, args.submit, log_dir, job_name)

"""
Example:
    python scr/preprocess/motion_correction.py --monkey zach --session MI01049P --submit
    python scr/preprocess/motion_correction.py --monkey zach --session MI01051P --submit
    
    python scr/preprocess/motion_correction.py --monkey zach --submit \
        --session MI01063P MI01111P MI01130P MI01132P MI01134P MI01136P
    
    python scr/preprocess/motion_correction.py --monkey zach --task 2 --submit
"""

