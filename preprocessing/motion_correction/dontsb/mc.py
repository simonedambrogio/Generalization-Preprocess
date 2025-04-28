import os

def mc_dontsb(episeries: str, t1wimg: str, t1wmask: str):
    command = f"""
    sh $MRCATDIR/pipelines/PreprocFunc_macaque/MotionCorrection_macaque.sh \
        --episeries={episeries} \
        --t1wimg={t1wimg} \
        --t1wmask={t1wmask}
    """
    os.system(command)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--episeries", type=str, required=True)
    parser.add_argument("--t1wimg", type=str, required=True)
    parser.add_argument("--t1wmask", type=str, required=True)
    args = parser.parse_args()
    mc_dontsb(args.episeries, args.t1wimg, args.t1wmask)