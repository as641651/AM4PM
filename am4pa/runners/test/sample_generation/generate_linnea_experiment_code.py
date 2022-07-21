import pkg_resources
import os
from re import search
import glob
import shutil
import csv
from datetime import datetime
import time
import random
import project_utils

offset = '    '

def set_up_tables(expression_dir=""):

    ##Case attributes
    case_log = os.path.join(expression_dir, 'case_table.csv')
    case_file = open(case_log, 'w', encoding='UTF8')
    case_csv_writer = csv.writer(case_file, delimiter=';')

    case_header = ['case:concept:name', 'case:flops', 'case:num_kernels']
    case_csv_writer.writerow(case_header)

    ##Event Attributes
    event_meta_log = os.path.join(expression_dir,'event_meta_table.csv')
    event_meta_file = open(event_meta_log, 'w', encoding='UTF8')
    event_meta_csv_writer = csv.writer(event_meta_file, delimiter=';')

    event_meta_header = ['case:concept:name', 'concept:name', 'concept:flops', 'concept:kernel', 'concept:operation', 'timestamp:start']
    event_meta_csv_writer.writerow(event_meta_header)

    return {
        'case_file': case_file,
        'case_csv_writer': case_csv_writer,
        'event_meta_file':event_meta_file,
        'event_meta_csv_writer': event_meta_csv_writer
    }


def write_meta_data(alg_id, kernels, tables, timestamp, variants_path):
    case_csv_writer = tables['case_csv_writer']
    event_meta_csv_writer = tables['event_meta_csv_writer']

    meta_path = os.path.join(variants_path.split("algorithm")[0], "generation_steps/algorithm{}.txt".format(alg_id))
    meta_file = open(meta_path,'r')

    costs = []
    operations = []
    lines = meta_file.readlines()
    for line in lines:
        if search("#", line):
            content = line.split("#")
            costs.append(content[-1].strip())
            operations.append(content[0].strip())
    operations.pop(0)

    case_concept_name = "algorithm{}".format(alg_id)
    dummy_stamp = timestamp + int(alg_id)*100

    case_row = []
    case_row.append(case_concept_name)
    case_row.append(costs.pop(0).split("cost")[-1].strip())
    case_row.append(len(kernels))
    case_csv_writer.writerow(case_row)

    concept_names = []
    #print(alg_id)
    for i in range(len(kernels)):
        #print(kernels[i])
        #print(costs[i])
        concept_name = kernels[i].split("!")[0] + "_" + costs[i]
        dt_dummy = datetime.fromtimestamp(dummy_stamp+i).strftime('%Y-%m-%d %H:%M:%S.%f')
        event_meta_row = [case_concept_name, concept_name, costs[i], kernels[i], operations[i], dt_dummy]
        event_meta_csv_writer.writerow(event_meta_row)
        concept_names.append(concept_name)

    meta_file.close()

    return (concept_names,costs,operations)

def generate_experiment_variant(variant_path, experiment_path, tables, timestamp):

    f1 = open(variant_path, 'r')
    f2 = open(experiment_path, 'w')

    alg_id = variant_path.split("algorithm")[-1].split('.')[0]
    #print(alg_id)

    lines = f1.readlines()

    id = 0
    code = ""
    stamps = []
    kernels = []
    for line in lines:
        if search("!", line):
            if not search("blascopy", line):
                stamp_id = "stime{}".format(id)
                stamps.append(stamp_id)
                kernels.append(line.strip())
                t_string = offset+stamp_id+"= time()\n"
                f2.write(t_string)
                f2.write(line)
                id = id+1
        elif search("return", line):
            stamp_id = "stime{}".format(id)
            stamps.append(stamp_id)
            t_string = offset+stamp_id+"= time()\n"
            f2.write(t_string)

            time_stamp_str = "("
            for i in stamps:
                time_stamp_str += "{},".format(i)
            time_stamp_str += ")\n"
            f2.write(offset+line.strip()+" ,{}".format(time_stamp_str))


        else:
            f2.write(line)

    concept_names,costs,operations = write_meta_data(alg_id, kernels, tables, timestamp, variant_path)

    code = "\n\n"
    code += "function write_algorithm{}_to_eventlog(io, id, stamps)\n".format(alg_id)
    for i in range(len(concept_names)):
        code += offset+"write( io, string(id, " \
                       "\";\", " \
                       "\"{};\", " \
                       "\"{};\", " \
                       "\"{};\", " \
                       "\"{};\", " \
                       "string(stamps[{}]), \";\"," \
                       " string(stamps[{}]), '\n'  ))\n"\
            .format(concept_names[i], costs[i], operations[i], kernels[i],i+1, i+2)

    code += "end"

    f2.write(code)

    f1.close()
    f2.close()





def generate_experiment_code(expression_dir=""):

    tables = set_up_tables(expression_dir)
    timestamp = time.time()

    variants_paths = os.path.join(expression_dir,"variants/Julia/generated/*.jl")
    experiments_dir = os.path.join(expression_dir, "experiments/")

    if os.path.exists(experiments_dir):
        shutil.rmtree(experiments_dir)

    os.mkdir(experiments_dir)

    variants = glob.glob(variants_paths)

    for v in variants:
        exp_path = os.path.join(experiments_dir, v.split("/")[-1])
        #print(v, exp_path)
        generate_experiment_variant(v, exp_path, tables, timestamp)

    tables['case_file'].close()
    tables['event_meta_file'].close()

    #ret,times = algorithm0(map(MatrixGenerator.unwrap, map(copy, matrices))...)
    #write_variant0_to_eventlog(io, "V0", times)


def generate_runner_code(expression_dir="", threads=4, backend_template=None):

    runner_file = os.path.join(expression_dir,"runner.jl")
    backend_submit_file = os.path.join(expression_dir, "submit.sh")

    variants_paths = os.path.join(expression_dir,"variants/Julia/generated/*.jl")
    variants = glob.glob(variants_paths)
    variants_includes = ""
    runner_code = ""
    runner_template = offset+'ret,times = {alg}(map(MatrixGenerator.unwrap, map(copy, matrices))...)\n'
    runner_template += offset+'write_{alg}_to_eventlog(io, "{alg}", times)\n'
    runner_template += offset + 'temp = rand(25000) # cache trashing\n\n'

    for v in variants:
        alg = v.split("/")[-1].split(".jl")[0]
        variants_includes += 'include("experiments/{}.jl")\n'.format(alg)
        runner_code += runner_template.format(alg=alg)

    # print(variants_includes)
    # print(runner_code)

    runner_path = os.path.join(expression_dir,"run_times.csv")
    inject = {
        'variants_includes': variants_includes,
        'runner_code': runner_code,
        'runner_path':runner_path,
        'threads':threads
    }

    project_utils.generate_script_from_template("templates/runner.jl", runner_file,inject)


    if backend_template:
        submit_template = "templates/{}".format(backend_template)
        inject = {
            'job_name': "{}_T{}".format(expression_dir.split('/')[-2], threads),
            'threads': threads,
            'memory': str(int(10240/threads))
        }
        project_utils.generate_script_from_template(submit_template, backend_submit_file, inject)

    project_utils.generate_script_from_template("templates/generate-measurements-script.py",
                                                os.path.join(expression_dir, "generate-measurements-script.py"),
                                                {})

    project_utils.generate_script_from_template("templates/compute-ranks.py",
                                                os.path.join(expression_dir, "compute-ranks.py"),
                                                {})

    operands_src = os.path.join(expression_dir,"variants/Julia/operand_generator.jl")
    operands_dst = os.path.join(expression_dir, "operand_generator.jl")
    shutil.copyfile(operands_src, operands_dst)

    logs_dir = os.path.join(expression_dir, "logs")
    if not os.path.exists(logs_dir):
        os.mkdir(logs_dir)


def generate_runner_competing_code(competing_vars, reps, run_id, threads=4, expression_dir=""):
    variants_path = [os.path.join(expression_dir,
                                  "experiments", "{}.jl".format(alg)) for alg in competing_vars]

    for var_path in variants_path:
        if not os.path.exists(var_path):
            return -1

    variants_includes = ""
    measurements_instance_set = []
    for var in competing_vars:
        variants_includes += 'include("experiments/{}.jl")\n'.format(var)
        measurements_instance_set += [(i, var) for i in range(reps)]
    random.shuffle(measurements_instance_set)

    runner_template = offset + 'ret,times = {alg}(map(MatrixGenerator.unwrap, map(copy, matrices))...)\n'
    runner_template += offset + 'write_{alg}_to_eventlog(io, "{alg}_{run_id}{rep}", times)\n'
    runner_template += offset + 'temp = rand(25000) # cache trashing\n\n'
    runner_code = ""
    for measurement in measurements_instance_set:
        runner_code += runner_template.format(alg=measurement[1], run_id=run_id, rep=measurement[0])

    runner_path = os.path.join(expression_dir, "run_times_competing_{}.csv".format(run_id))
    inject = {
        'variants_includes': variants_includes,
        'runner_code': runner_code,
        'runner_path': os.path.abspath(runner_path),
        'threads':threads
    }

    template_str = pkg_resources.resource_string(__name__, "templates/runner.jl").decode("UTF-8")

    runner_file = os.path.join(expression_dir,"runner_competing_{}.jl".format(run_id))
    with open(runner_file, "wt", encoding='utf-8') as output_file:
        output_file.write(template_str.format(**inject))

    return 1

if __name__ == '__main__':

    expression_dir = "Matrix-Chain-4/variants-linnea/"
    generate_experiment_code(expression_dir)


















