import os

def main(vars_file: str, from_vol: int, to_vol: int):
    
    command = f"""
    sh $MRCATDIR/pipelines/PreprocFunc_macaque/MotionCorrection_CorrectMotionDistortion.sh \
        --vars={vars_file} \
        --from-vol={from_vol} \
        --to-vol={to_vol}
    """
    
    os.system(command)

if __name__ == "__main__":
    """ Example usage:
        python motion3.py --vars /users/rushworth/gwr089/scratch/Generalization-Preprocess/zach/TEST/epi2d/work/motion_correction_vars.sh \
            --from-vol 0 \
            --to-vol 1
    """
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--vars-file", type=str, required=True)
    parser.add_argument("--from-vol", type=int, required=True)
    parser.add_argument("--to-vol", type=int, required=True)
    args = parser.parse_args()
    main(args.vars_file, args.from_vol, args.to_vol)
    
    