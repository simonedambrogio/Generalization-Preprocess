import os

def main(vars_file: str):
    
    command = f"""
    sh $MRCATDIR/pipelines/PreprocFunc_macaque/MotionCorrection_PrepareRefImg_macaque.sh \
        --vars={vars_file}
    """
    
    os.system(command)

if __name__ == "__main__":
    """ Example usage:
        python motion2.py --vars /users/rushworth/gwr089/scratch/Generalization-Preprocess/zach/TEST/epi2d/work/motion_correction_vars.sh
    """
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--vars-file", type=str, required=True)
    args = parser.parse_args()
    main(args.vars_file)
    
    