import os
import subprocess
import pandas as pd
import shutil


class RunnerVariants:
    def __init__(self, operand_sizes,
                 script_dir,
                 threads=4,
                 backend_manager=None,
                 backend_commands=None):
        """
        This class handles the code generation and execution of the variant codes.
        The generated event data can be obtained as a pandas dataframe.

        Requirements:

        It is assumed that there exists a script file that generates variant codes
        for a given oopoerand sizes. The operand sizes are input as command line args
            e.g. run of script file: python generate.py 10 10 10 10 12

        After running the script file, inside the folder "experiments", which is in
        the same directory as the script file, an "argument folder" is generated,
        which contains the case_table, event_meta_table (i.e, the event table without actual run times)
        ,and a runner script as shown in the expample below:
            e.g. experiment/10_10_10_10_12/
                    case_table.csv
                    event_meta_table.csv
                    runner.jl

        'runner.jl' is the script that runs the experiments and generates a log file 'run_times.txt' (which is the
        event table with actual run times) in the "arguments folder"


        INPUT:

        name: Experiment name
        script_path: Path to the script file that generates variants
        args: operand sizes (or arguments to the script file)

        USECASE:
        If the behavior of the script is as said in the requirements, this class can
        call the scipt file and collects the eventlogs as a pandas dataframe, and
        if needed, can also clean the generated folders.

        """
        self.script_dir = script_dir
        self.operand_sizes = operand_sizes
        self.operands_dir = os.path.join(self.script_dir,
                                         "experiments",
                                         "_".join(self.operand_sizes))

        self.backend_manager = backend_manager
        self.backend_commands = backend_commands
        self.threads = threads

    def generate_variants_for_measurements(self, generation_script):
        """
        generates experiments for a given set of valid arguments
        that can be given as input to the script file.
            e.g. in,  python generate.py 10 10 10 10 12
            ['10','10','10','10','12'] would be the argument list.

        Output: Return code == 0 implies successful completion
        """
        script_path = os.path.join(self.script_dir, generation_script)
        args = self.operand_sizes + ["--threads={}".format(self.threads)]
        if not self.backend_manager:
            call = ["python", script_path] + args
            print(call)
            completed_proccess = subprocess.run(call)
            ret = completed_proccess.returncode
        else:
            cmd = self.backend_commands.build_cmd("python", script_path, " ".join(args))
            # print(cmd)
            stdout, ret = self.backend_manager.run_cmd(cmd)
            print(stdout.readlines())

        return ret

    def measure_variants(self, app, runner_script):
        """
        executes the runner file, which generates run_times.txt
        """
        runner_path = os.path.join(self.operands_dir, runner_script)
        if not self.backend_manager:
            if os.path.exists(self.operands_dir):
                print("Running Experiments locally")
                completed_proccess = subprocess.run([app, runner_path])
                if completed_proccess.returncode == 0:
                    print("Experiments completed locally")
                    return 0  # Ran experiment
        else:
            cmd = self.backend_commands.build_cmd(app, runner_path)
            stdout, ret = self.backend_manager.run_cmd(cmd)
            print(stdout.readlines())
            if ret == 0:
                print("Running experiments in the backend.")
                return 0

        return -1

    def generate_measurements_script(self, measurement_script, competing_variants, run_id, reps):
        pass

    def clean(self):
        """remove arguments folder"""
        if os.path.exists(self.operands_dir):
            shutil.rmtree(self.operands_dir)
        else:
            return -1



