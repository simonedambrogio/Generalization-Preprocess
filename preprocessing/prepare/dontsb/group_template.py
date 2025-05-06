import os

def dontsb_grouptemplate(
    inputdir, 
    monkeylist, 
    outputdir, 
    refimg, 
    inputsubpath='', 
    suffixbiascorr='_restore', 
    suffixbrain='_brain', 
    suffixmask='_mask',
    niter=6, 
    flgtemplate=1, 
    flgantsreg=1, 
    t1wbase='structural', 
    refmask=None, 
    useniter=None):
    """
    Reorient and resample a structural image to the standard space.
    obligatory:

    --inputdir=<dir>
        This is the group/study directory which contains a folder for each animal, which holds that animal's 
        T1w image and mask. This script assumes: 
          inputdir/animal_1_dir/[T1wImage, T1wMask]
          inputdir/animal_2_dir/[T1wImage, T1wMask] 
          etc.

    --monkeylist=<double quoted variable>
        A variable (in double quotes "") pointing to space-separated string of animal (folder) names> 
        E.g., "$mylist" (where mylist="animal_1_dir animal_2_dir animal_3_dir")
        The double quotes ensure that the full list is passed along!

    --outputdir=<dir>
        The output directory which will store group templates, transforms etc.
        This will be created if does not already exist.

    --refimg=<reference img>
        This points to the desired reference image to be used for the group template.
        This script assumes that there is also a mask for this reference in the place
        (see also refmask argument below).

  optional:

    --inputsubpath=<string> (default: '')
        The sub-path, if any, between top-level monkey dir and actual structural images
        e.g., /studydir/monkey/inputsubpath/structural.nii

    --refmask=<reference brain mask img> (default: "$refimg"_mask)
        The reference brain mask image.

    --niter=<1 to 6> (default: 6)
        The number of iterations to run for group template creation:
          (1) Initially register to reference
          (2) Create group template
          (3) Register to group template
          Repeat steps (2) and (3) [1-6] number of times...

          Note that a group template is provided for each iteration. 

    --useniter=<1 to 6> (default: niter)
        Which iteration to use to create ANTs struct2stand transform 

    --flgtemplate=<0,1> (default: 1)
        run group template script 

    --flgantsreg=<0,1> (default: 1)
        run ANTs struct2stand registration 
        (i.e, if group template already exists)

    --t1wbase=<string> (default: "structural")
        Basename of T1w image that script will look for within each animal directory

    --suffixbiascorr=<string> (default: "_restore")
        A substring that is appended to identify bias-corrected (restored)
        images.

    --suffixbrain=<string> (default: "_brain")
        A substring that is appended to identify brain extracted images.

    --suffixmask=<string> (default: "_mask")
        A substring that is appended to identify binary brain masks.
    """
    
    print(refimg)
    refmask = refimg + suffixmask if refmask is None else refmask
    useniter = niter if useniter is None else useniter
    
    command = f"""
    sh $MRCATDIR/pipelines/PreprocFunc_macaque/group_template/groupTemplate.sh \
        --inputdir={inputdir} \
        --monkeylist={monkeylist} \
        --outputdir={outputdir} \
        --refimg={refimg} \
        --inputsubpath={inputsubpath} \
        --refmask={refmask} \
        --niter={niter} \
        --useniter={useniter} \
        --flgtemplate={flgtemplate} \
        --flgantsreg={flgantsreg} \
        --t1wbase={t1wbase} \
        --suffixbiascorr={suffixbiascorr} \
        --suffixbrain={suffixbrain} \
        --suffixmask={suffixmask}
    """
    os.system(command)
    
    print("done.")

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
    args = parser.parse_args()
    
    # if monkelist is array, convert to string
    if isinstance(args.monkeylist, list):
        args.monkeylist = " ".join(args.monkeylist)
    
    if args.refimg.endswith('.nii.gz'):
        args.refimg = args.refimg.replace('.nii.gz', '')
        
    dontsb_grouptemplate(
        inputdir=args.inputdir, 
        monkeylist=args.monkeylist, 
        outputdir=args.outputdir, 
        refimg=args.refimg, 
        inputsubpath=args.inputsubpath, 
        refmask=args.refmask, 
        niter=args.niter, 
        useniter=args.useniter, 
        flgtemplate=args.flgtemplate, 
        flgantsreg=args.flgantsreg, 
        t1wbase=args.t1wbase, 
        suffixbiascorr=args.suffixbiascorr, 
        suffixbrain=args.suffixbrain, 
        suffixmask=args.suffixmask)
    
    """
    Example:
    python preprocessing/prepare/dontsb/group_template.py \
        --monkeylist zach zeno \
        --inputdir /users/rushworth/gwr089/scratch/Generalization-Preprocess \
        --inputsubpath=structural/mprage \
        --outputdir /users/rushworth/gwr089/scratch/Generalization-Preprocess/template \
        --refimg $MRCATDIR/data/macaque/F99/McLaren
    """