from preprocessing.prepare.dontsb.func import dontsb_func
from preprocessing.prepare.submit.func import submit_func

def func(input_file, output_dir, submit=False):
    
    if submit:
        submit_func(input_file, output_dir)
    else:
         dontsb_func(input_file, output_dir)
