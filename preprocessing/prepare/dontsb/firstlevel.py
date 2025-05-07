import os

def dontsb_firstlevel(sessdir: str, epidir: str, transdir: str, outputdir: str, standimg: str, struct2standwarp: str):
    print(f"Running firstlevel for {sessdir}")
    command = f"""
        sh $MRCATDIR/pipelines/PreprocFunc_macaque/PrepareFeat_1stLevel.sh \
            --sessdir={sessdir} \
            --epidir={epidir} \
            --transdir={transdir} \
            --outputdir={outputdir} \
            --makefunc2standwarp=1 \
            --standimg={standimg} \
            --struct2standwarp={struct2standwarp}
    """
    os.system(command)
    print(f"done")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--sessdir", type=str, required=True)
    parser.add_argument("--epidir", type=str, required=True)
    parser.add_argument("--transdir", type=str, required=True)
    parser.add_argument("--outputdir", type=str, required=True)
    parser.add_argument("--standimg", type=str, required=True)
    parser.add_argument("--struct2standwarp", type=str, required=True)
    args = parser.parse_args()
    
    dontsb_firstlevel(
        sessdir=args.sessdir, 
        epidir=args.epidir, 
        transdir=args.transdir, 
        outputdir=args.outputdir, 
        standimg=args.standimg, 
        struct2standwarp=args.struct2standwarp
    )
