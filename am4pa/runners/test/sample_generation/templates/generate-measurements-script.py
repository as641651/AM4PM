import os
import argparse
import sys

import pathlib
this_dir = pathlib.Path(__file__).parent.resolve()
sys.path.append(os.path.join(this_dir,"../../../../utils"))
import generate_linnea_experiment_code


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:  no  valid path")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='generate script that measures competing variants ')
    parser.add_argument('--algs', nargs='+', default=[], required=True)
    parser.add_argument('--rep', type=int, default=10, required=True)
    parser.add_argument('--id', type=int, default=0, required=True)
    parser.add_argument('--threads', type=int, default=4, required=True)

    args = parser.parse_args()

    generate_linnea_experiment_code.generate_runner_competing_code(args.algs, args.rep, args.id, args.threads, this_dir)


