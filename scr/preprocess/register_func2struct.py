
import sys, os, yaml
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
sys.path.append(config['paths']['preprocess'])
import preprocessing.func2struct as func2struct

def main(config, monkey: str, session: str, submit: bool, log_dir: str, job_name: str):
    
    assert monkey in ["zach", "zeno"], "Monkey must be either zach or zeno"
    # Get the inputs ------------------------------------------------------------
    episeries = os.path.join(config['paths'][monkey], session, "epi2d", "f_mean.nii.gz")
    assert os.path.exists(episeries), f"EPI series does not exist: {episeries}"
    t1wimg = os.path.join(config['paths'][monkey], "structural", "mprage", "structural_restore.nii.gz")
    assert os.path.exists(t1wimg), f"T1w image does not exist: {t1wimg}"
    t1wmask = os.path.join(config['paths'][monkey], "structural", "mprage", "structural_brain_mask.nii.gz")
    assert os.path.exists(t1wmask), f"T1w mask does not exist: {t1wmask}"

    # Run the prepare function ---------------------------------------------------
    func2struct.run(episeries, t1wimg, t1wmask, submit, log_dir, job_name)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--monkey", type=str, required=True)
    parser.add_argument("--session", nargs="+", type=str, required=False)
    parser.add_argument("--exclude", nargs="+", type=str, required=False)
    parser.add_argument("--task", type=str, required=False)
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--log_dir", type=str, default="logs")
    parser.add_argument("--job_name", type=str, default="func2struct")
    args = parser.parse_args()

    # Run the main function ------------------------------------------------------
    if args.session is None:
        sessions = config[args.monkey]['task' + args.task]
    else:
        sessions = args.session

    if args.exclude is not None:
        sessions = [session for session in sessions if session not in args.exclude]

    for session in sessions:
        job_name = f"f2s_{session}"
        log_dir = os.path.join(config['paths'][args.monkey], session, "logs")
        main(config, args.monkey, session, args.submit, log_dir, job_name)

"""
Examples:

```bash
python scr/preprocess/register_func2struct.py \
    --monkey zach --session MI01051P --submit
```

python scr/preprocess/register_func2struct.py --monkey zach --session MI01140P --submit
    
```bash
python scr/preprocess/register_func2struct.py --monkey zach --submit \
    --session MI01060P MI01062P MI01063P MI01108P MI01111P MI01115P \
        MI01118P MI01130P MI01132P MI01134P MI01136P
```

```bash
python scr/preprocess/register_func2struct.py \
    --monkey zach --task 2 --exclude MI01140P --submit
```

"""

