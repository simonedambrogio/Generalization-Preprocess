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
    # scripts to run
    parser.add_argument("--firstlevel", action="store_true", default=False)
    parser.add_argument("--nuisancereg", action="store_true", default=False)
    # nuisancereg parameters
    parser.add_argument("--sdthr", type=float, required=False, default=3)
    parser.add_argument("--dorecursive", type=int, required=False, default=1)
    parser.add_argument("--dobadvol", type=int, required=False, default=1)
    parser.add_argument("--domotioncomp", type=int, required=False, default=1)
    parser.add_argument("--domelodiccomp", type=int, required=False, default=1)
    # submssion
    parser.add_argument("--submit", action="store_true", default=False)
    parser.add_argument("--log_dir", type=str, required=False, default="logs")
    parser.add_argument("--job_name", type=str, required=False, default="firstlevel")
    args = parser.parse_args()

    firstlevel_and_nuisancereg = not args.firstlevel and not args.nuisancereg
    
    if args.session is None:
        sessions = config[args.monkey]['task' + args.task]
    else:
        sessions = args.session
        
    standimg = os.path.join(config['paths']['preprocess'], 'template', 'ants', 'image', 'groupavg_2_brain.nii.gz')
    struct2standwarp = os.path.join(config['paths']['preprocess'], 'template', 'ants', 'transform', args.monkey, 'structural_to_groupavg_2_warp.nii.gz')
    

    for session in sessions:
        sessdir = os.path.join(config['paths']['preprocess'], args.monkey, session)
        epidir = os.path.join(sessdir, "epi2d")
        transdir = os.path.join(sessdir, "transform")
        outputdir = os.path.join(sessdir, "proc")
        
        if args.firstlevel:
            job_name = f"{args.monkey}_{session}_preparefirstlevel"
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
        
        if args.nuisancereg:
            job_name = f"{args.monkey}_{session}_preparenuisancereg"
            prepare.nuisancereg(
                sessdir, 
                args.sdthr, 
                outputdir, 
                args.dorecursive, 
                args.dobadvol, 
                args.domotioncomp, 
                args.domelodiccomp, 
                epidir, 
                args.submit, 
                args.log_dir, 
                job_name)
        
        if firstlevel_and_nuisancereg:
            job_name = f"{args.monkey}_{session}_prepare_firstlevel&nuisancereg"
            prepare.firstlevel_and_nuisancereg(
                sessdir, 
                epidir, 
                transdir, 
                outputdir, 
                standimg, 
                struct2standwarp,
                args.sdthr,
                args.dorecursive,
                args.dobadvol,
                args.domotioncomp,
                args.domelodiccomp,
                args.submit,
                args.log_dir,
                job_name)
    """
    Example:
    python scr/prepare/firstlevel.py --monkey zach --session MI01060P --submit
    python scr/prepare/firstlevel.py --monkey zach --task 1 --submit
    
    python scr/prepare/firstlevel.py --monkey zach --session MI01051P --nuisancereg --submit
    python scr/prepare/firstlevel.py --monkey zach --task 1 --nuisancereg --submit
    
    python scr/prepare/firstlevel.py --monkey zach --task 2 --submit
    python scr/prepare/firstlevel.py --monkey zach --task 3 --submit
    """