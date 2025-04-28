import os

def main(episeries: str, t1wimg: str, t1wmask: str):
    
    command = f"""
    sh $MRCATDIR/pipelines/PreprocFunc_macaque/MotionCorrection_CreateRefImg_macaque.sh \
        --episeries={episeries} \
        --t1wimg={t1wimg} \
        --t1wmask={t1wmask}
    """
    
    os.system(command)

if __name__ == "__main__":
    """ Example usage:
        python motion1.py --episeries=/users/rushworth/gwr089/scratch/Generalization-Preprocess/zach/TEST/epi2d/f \
            --t1wimg=/users/rushworth/gwr089/scratch/Generalization-Preprocess/zach/structural/structural_restore \
            --t1wmask=/users/rushworth/gwr089/scratch/Generalization-Preprocess/zach/structural/structural_brain_mask
    """
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--episeries", type=str, required=True)
    parser.add_argument("--t1wimg", type=str, required=True)
    parser.add_argument("--t1wmask", type=str, required=True)
    args = parser.parse_args()
    main(**vars(args))
    
    