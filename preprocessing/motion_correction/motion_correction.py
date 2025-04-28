from preprocessing.motion_correction.dontsb.mc import mc_dontsb
from preprocessing.motion_correction.submit.mc import mc_submit

def run(episeries: str, t1wimg: str, t1wmask: str, submit: bool, log_dir="logs", job_name="motion_correction"):
    
    # If episeries, t1wimg, and t1wmask end with .nii.gz, remove the extension
    if episeries.endswith(".nii.gz"):
        episeries = episeries.replace(".nii.gz", "")
    if t1wimg.endswith(".nii.gz"):
        t1wimg = t1wimg.replace(".nii.gz", "")
    if t1wmask.endswith(".nii.gz"):
        t1wmask = t1wmask.replace(".nii.gz", "")
        
    if submit:
        mc_submit(episeries, t1wimg, t1wmask, log_dir, job_name)
    else:
        mc_dontsb(episeries, t1wimg, t1wmask)

