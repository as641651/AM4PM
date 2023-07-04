import sys
import os
import shutil

from linnea.algebra.expression import Matrix, Vector, Equal, Times, Inverse, Transpose
from linnea.algebra.equations import Equations
from linnea.algebra.properties import Property

import pathlib
this_dir = pathlib.Path(__file__).parent.resolve()
#sys.path.append(os.path.join(this_dir,"../../utils"))

#from ...utils import generate_linnea_experiment_code
import generate_linnea_experiment_code

import argparse

def generalized_least_squares(m=2500,n=500):

    b = Vector("b", (n, 1))

    X = Matrix("X", (m, n))
    X.set_property(Property.FULL_RANK)

    M = Matrix("M", (m, m))
    M.set_property(Property.SPD)

    y = Vector("y", (m, 1))

    # b = (X.T*M.inv*X).inv*X.T*M.inv*y
    equations = Equations(Equal(b, Times(Inverse(Times(Transpose(X), Inverse(M), X)), Transpose(X), Inverse(M), y)))

    return equations



if __name__ == "__main__":

    import linnea.config

    linnea.config.set_output_code_path(".")
    linnea.config.experiment_configuration["repetitions"] = 10
    linnea.config.init()

    from linnea.algorithm_generation.graph.search_graph import SearchGraph

    parser = argparse.ArgumentParser(description='Input: the dims')
    parser.add_argument('dims', metavar='N', type=int, nargs='+',
                        help='NA')
    parser.add_argument('--threads', type=int, default=4,
                        help= 'Num threads')

    dims = parser.parse_args()._get_kwargs()[0][1]
    threads = parser.parse_args()._get_kwargs()[1][1]
    if len(dims) != 2:
        raise Exception("Need dimensions")
    linnea.config.experiment_configuration["threads"] = str(threads)


    expression_dir = os.path.join(this_dir,'experiments', '{}T'.format(threads) ,'{}_{}/'.format(*dims))
    if os.path.exists(expression_dir):
        shutil.rmtree(expression_dir)
    os.makedirs(expression_dir)
    linnea.config.set_output_code_path(expression_dir)


    #from input1 import equations

    # import linnea.examples.examples
    # equations = linnea.examples.examples.Example001().eqns

    equations = generalized_least_squares(*dims)
    graph = SearchGraph(equations)
    graph.generate(time_limit=60,
                   merging=True,
                   dead_ends=True,
                   pruning_factor=100.0)

    graph.write_output(code=True,
                       generation_steps=True,
                       output_name="variants",
                       experiment_code=True,
                       algorithms_limit=100,
                       graph=True,
                       no_duplicates=True)


    ## Generate Experiment Code
    generate_linnea_experiment_code.generate_experiment_code(expression_dir)
    generate_linnea_experiment_code.generate_runner_code(expression_dir,
                                                         threads=threads,
                                                         backend_template='slrum_submit.sh')
    ##generate min flops runner code. read case table and find alg with min flops

    print("Generated Variants.")


