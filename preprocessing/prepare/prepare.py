from preprocessing.prepare.dontsb.func import dontsb_func
from preprocessing.prepare.submit.func import submit_func

from preprocessing.prepare.dontsb.struct import dontsb_struct
from preprocessing.prepare.submit.struct import submit_struct

from preprocessing.prepare.dontsb.group_template import dontsb_grouptemplate
from preprocessing.prepare.submit.group_template import submit_grouptemplate

from preprocessing.prepare.dontsb.firstlevel import dontsb_firstlevel
from preprocessing.prepare.submit.firstlevel import submit_firstlevel

def func(input_file, output_file, submit, log_dir="logs", job_name="func_prepare"):
    
    if submit:
        submit_func(input_file, output_file, log_dir, job_name)
    else:
        dontsb_func(input_file, output_file)

def struct(input_file, submit, instructions="all", log_dir="logs", job_name="struct_prepare", **kwargs):
    if submit:
        submit_struct(input_file, instructions, log_dir, job_name, **kwargs)
    else:
        dontsb_struct(input_file, instructions)

def group_template(
    inputdir, 
    monkeylist, 
    outputdir, 
    refimg, 
    submit,
    inputsubpath='', 
    suffixbiascorr='_restore', 
    suffixbrain='_brain', 
    suffixmask='_mask',
    niter=6, 
    flgtemplate=1, 
    flgantsreg=1, 
    t1wbase='structural', 
    refmask=None, 
    useniter=None,
    log_dir="logs", 
    job_name="group_template"):
    if submit:
        submit_grouptemplate(
            inputdir, 
            monkeylist, 
            outputdir, 
            refimg, 
            inputsubpath, 
            suffixbiascorr, 
            suffixbrain, 
            suffixmask, 
            niter, 
            flgtemplate, 
            flgantsreg, 
            t1wbase, 
            refmask, 
            useniter, 
            log_dir, 
            job_name)
    else:
        dontsb_grouptemplate(inputdir, 
            inputdir, 
            monkeylist, 
            outputdir, 
            refimg, 
            inputsubpath, 
            suffixbiascorr, 
            suffixbrain, 
            suffixmask, 
            niter, 
            flgtemplate, 
            flgantsreg, 
            t1wbase, 
            refmask, 
            useniter)

def firstlevel(sessdir, epidir, transdir, outputdir, standimg, struct2standwarp, submit, log_dir="logs", job_name="firstlevel"):
    if submit:
        submit_firstlevel(sessdir, epidir, transdir, outputdir, standimg, struct2standwarp, log_dir, job_name)
    else:
        dontsb_firstlevel(sessdir, epidir, transdir, outputdir, standimg, struct2standwarp)
