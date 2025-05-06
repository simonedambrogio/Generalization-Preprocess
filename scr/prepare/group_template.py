
import sys, yaml
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
sys.path.append(config['paths']['preprocess'])
import preprocessing.prepare as prepare

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()    
    # required ------------------------------------------------------------
    parser.add_argument("--inputdir", type=str, required=True)
    parser.add_argument("--monkeylist", nargs="+", type=str, required=True)
    parser.add_argument("--outputdir", type=str, required=True)
    parser.add_argument("--refimg", type=str, required=True)
    # optional ------------------------------------------------------------
    parser.add_argument("--inputsubpath", type=str, required=False, default='')
    parser.add_argument("--refmask", type=str, required=False, default=None)
    parser.add_argument("--niter", type=int, required=False, default=6)
    parser.add_argument("--useniter", type=int, required=False, default=None)
    parser.add_argument("--flgtemplate", type=int, required=False, default=1)
    parser.add_argument("--flgantsreg", type=int, required=False, default=1)
    parser.add_argument("--t1wbase", type=str, required=False, default='structural')
    parser.add_argument("--suffixbiascorr", type=str, required=False, default='_restore')
    parser.add_argument("--suffixbrain", type=str, required=False, default='_brain')
    parser.add_argument("--suffixmask", type=str, required=False, default='_mask')
    # run ------------------------------------------------------------
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--log_dir", type=str, default="logs")
    parser.add_argument("--job_name", type=str, default="group_template")
    args = parser.parse_args()
    
    prepare.group_template(
        inputdir=args.inputdir, 
        monkeylist=args.monkeylist, 
        outputdir=args.outputdir, 
        refimg=args.refimg, 
        submit=args.submit,
        inputsubpath=args.inputsubpath, 
        suffixbiascorr=args.suffixbiascorr, 
        suffixbrain=args.suffixbrain, 
        suffixmask=args.suffixmask,
        niter=args.niter, 
        flgtemplate=args.flgtemplate, 
        flgantsreg=args.flgantsreg, 
        t1wbase=args.t1wbase, 
        refmask=args.refmask, 
        useniter=args.useniter,
        log_dir=args.log_dir, 
        job_name=args.job_name)
    """
    Example:
    python scr/prepare/group_template.py \
        --monkeylist zach zeno \
        --inputdir /users/rushworth/gwr089/scratch/Generalization-Preprocess \
        --inputsubpath=structural/mprage \
        --outputdir /users/rushworth/gwr089/scratch/Generalization-Preprocess/template \
        --refimg $MRCATDIR/data/macaque/F99/McLaren \
        --submit
    """