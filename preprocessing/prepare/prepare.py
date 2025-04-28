from preprocessing.prepare.dontsb.func import dontsb_func
from preprocessing.prepare.submit.func import submit_func

from preprocessing.prepare.dontsb.struct import dontsb_struct
from preprocessing.prepare.submit.struct import submit_struct

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

