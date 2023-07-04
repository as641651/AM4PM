import pathlib
import os
from re import template
import shutil
from tempfile import tempdir
this_dir = pathlib.Path(__file__).parent.resolve()



def _copy_template(file_name, code_dir):
    shutil.copy(os.path.join(this_dir,'template',file_name), os.path.join(code_dir,file_name))


def expr_init(expr_file, code_dir):
    template_path = os.path.join(this_dir,'template/generate-variants-linnea.py')
    with open(template_path, "r") as file:
        template_string = file.read()

    with open(expr_file, "r") as file:
        expr_string = file.read()

    for s_ in expr_string.split('\n'):
        if 'def' in s_:  
            expr_fn = s_.split('(')[0].split('def')[-1].strip()
            num_params = len(s_.split('(')[-1].split(','))
            break

    d_str = ''
    for i in range(num_params-1):
        d_str += '{}_'
    d_str += '{}/'


    inject = {
        'expression_code':expr_string,
        'num_params':num_params,
        'd_str':d_str,
        'expression_fn': expr_fn
    }

    if not os.path.exists(code_dir):
        os.makedirs(code_dir)

    out_file = os.path.join(code_dir,'generate-variants-linnea.py')

    with open(out_file, "wt", encoding='utf-8') as of:
        of.write(template_string.format(**inject))


    _copy_template("generate_linnea_experiment_code.py", code_dir)
    _copy_template("project_utils.py", code_dir)
    
    template_dir = os.path.join(code_dir,'templates')
    if os.path.exists(template_dir):
        shutil.rmtree(template_dir)
    shutil.copytree(os.path.join(this_dir,'template','templates'), template_dir)
    os.rename(os.path.join(template_dir, 'runner.py'), os.path.join(template_dir, 'runner.jl'))
    os.rename(os.path.join(template_dir, 'slrum_submit.py'), os.path.join(template_dir, 'slrum_submit.sh'))



    

    
    
