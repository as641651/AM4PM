import sys
import os
import shutil

from linnea.algebra.expression import Matrix, Vector, Equal, Times, Inverse, Transpose
from linnea.algebra.equations import Equations
from linnea.algebra.properties import Property

import pathlib
this_dir = pathlib.Path(__file__).parent.resolve()

#from ...utils import generate_linnea_experiment_code
import generate_linnea_experiment_code

import argparse


def matrix_chain_4(m,n,k,l,q):

    A = Matrix("A", (n, m))
    A.set_property(Property.FULL_RANK)

    B = Matrix("B", (m, k))
    B.set_property(Property.FULL_RANK)

    C = Matrix("C", (k, l))
    C.set_property(Property.FULL_RANK)
    
    D = Matrix("D", (l, q))
    D.set_property(Property.FULL_RANK)

    Y = Matrix("Y", (n, q))

    # Y = ABCD
    equations = Equations(Equal(Y, Times(A,B,C,D)))

    return equations



if __name__ == "__main__":

    import linnea.config

    linnea.config.set_output_code_path(".")
    linnea.config.experiment_configuration["repetitions"] = 10
    linnea.config.init()

    from linnea.algorithm_generation.graph.search_graph import SearchGraph

    parser = argparse.ArgumentParser(description='Input: [m,n,k,l,q]')
    parser.add_argument('dims', metavar='N', type=int, nargs='+',
                        help='Dimensions of matrix chain of length 4, Enter atleast 5 integers. ')
    parser.add_argument('--threads', type=int, default=4,
                        help= 'Num threads')

    dims = parser.parse_args()._get_kwargs()[0][1]
    threads = parser.parse_args()._get_kwargs()[1][1]
    if len(dims) != 5:
        raise Exception("Need 5 dimensions")
    m,n,k,l,q = dims
    linnea.config.experiment_configuration["threads"] = str(threads)

    expression_dir = os.path.join(this_dir,'experiments','{}_{}_{}_{}_{}/'.format(m,n,k,l,q))
    if os.path.exists(expression_dir):
        shutil.rmtree(expression_dir)
    os.makedirs(expression_dir)
    linnea.config.set_output_code_path(expression_dir)


    #from input1 import equations

    # import linnea.examples.examples
    # equations = linnea.examples.examples.Example001().eqns

    equations = matrix_chain_4(m,n,k,l,q)
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