import sys, yaml, os
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
sys.path.append(config['paths']['preprocess'])
import preprocessing.prepare as prepare

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--monkey", type=str, required=True)
    parser.add_argument("--session", nargs='+', type=str, required=False)
    parser.add_argument("--task", type=str, required=False)
    parser.add_argument("--submit", action="store_true", default=False)
    parser.add_argument("--log_dir", type=str, required=False, default="logs")
    parser.add_argument("--job_name", type=str, required=False, default="firstlevel")
    args = parser.parse_args()

    if args.session is None:
        sessions = config[args.monkey]['task' + args.task]
    else:
        sessions = args.session
        
    standimg = os.path.join(config['paths']['preprocess'], 'template', 'ants', 'image', 'groupavg_2_brain.nii.gz')
    struct2standwarp = os.path.join(config['paths']['preprocess'], 'template', 'ants', 'transform', args.monkey, 'structural_to_groupavg_2_warp.nii.gz')
    

    for session in sessions:
        job_name = f"{args.monkey}_{session}_preparefirstlevel"
        sessdir = os.path.join(config['paths']['preprocess'], args.monkey, session)
        epidir = os.path.join(sessdir, "epi2d")
        transdir = os.path.join(sessdir, "transform")
        outputdir = os.path.join(sessdir, "proc")
        prepare.firstlevel(
            sessdir, 
            epidir, 
            transdir, 
            outputdir, 
            standimg, 
            struct2standwarp, 
            args.submit, 
            args.log_dir, 
            job_name)
    
    """
    Example:
    python scr/prepare/firstlevel.py \
        --monkey zach \
        --session MI01060P \
        --submit
        
    python scr/prepare/firstlevel.py --monkey zach --task 1 --submit
    """