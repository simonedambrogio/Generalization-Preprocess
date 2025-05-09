import os

def dontsb_nuisancereg(sessiondir,sdthr,outputdir,dorecursive,dobadvol,domotioncomp,domelodiccomp,epidir):
    print(f"\nRunning nuisancereg for {sessiondir}")
    command = f"""
        $MATLABBIN/matlab -nodisplay -nosplash -r "addpath('$MRCATDIR/pipelines/PreprocFunc_macaque/'); CreateNuisanceRegSingle('{sessiondir}',{sdthr},'{outputdir}',{dorecursive},{dobadvol},{domotioncomp},{domelodiccomp},'{epidir}'); exit" 
    """
    os.system(command)
    print(f"done")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--sessiondir", type=str, required=True)
    parser.add_argument("--sdthr", type=float, required=True)
    parser.add_argument("--outputdir", type=str, required=True)
    parser.add_argument("--epidir", type=str, required=True)
    parser.add_argument("--dorecursive", type=int, required=True)
    parser.add_argument("--dobadvol", type=int, required=True)
    parser.add_argument("--domotioncomp", type=int, required=True)
    parser.add_argument("--domelodiccomp", type=int, required=True)
    args = parser.parse_args()
    
    dontsb_nuisancereg(
        sessiondir=args.sessiondir, 
        sdthr=args.sdthr, 
        outputdir=args.outputdir, 
        dorecursive=args.dorecursive, 
        dobadvol=args.dobadvol, 
        domotioncomp=args.domotioncomp, 
        domelodiccomp=args.domelodiccomp, 
        epidir=args.epidir
    )

