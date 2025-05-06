import os


def f2s_dontsb(episeries: str, t1wimg: str, t1wmask: str):
    command = f"""
    sh $MRCATDIR/pipelines/PreprocFunc_macaque/RegisterFuncStruct_macaque.sh \
        --epiimg={episeries} \
        --t1wimg={t1wimg} \
        --t1wmask={t1wmask}
    """
    os.system(command)
    print(f"Done.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--episeries", type=str, required=True)
    parser.add_argument("--t1wimg", type=str, required=True)
    parser.add_argument("--t1wmask", type=str, required=True)
    args = parser.parse_args()
    f2s_dontsb(args.episeries, args.t1wimg, args.t1wmask)

"""
sh $MRCATDIR/pipelines/PreprocFunc_macaque/RegisterFuncStruct_macaque.sh \
        --epiimg=/users/rushworth/gwr089/scratch/Generalization-Preprocess/zach/MI01051P/epi2d/f_mean \
        --t1wimg=/users/rushworth/gwr089/scratch/Generalization-Preprocess/zach/structural/mprage/structural_restore \
        --t1wmask=/users/rushworth/gwr089/scratch/Generalization-Preprocess/zach/structural/mprage/structural_brain_mask
"""