import os
import shutil
from .execute_sub_process import ExecuteSubProcess, bcolors


class RunnerVariants(ExecuteSubProcess):
    def __init__(self, operand_sizes,
                 script_dir,
                 threads=4,
                 backend_manager=None,
                 backend_commands=None):
        """
        Runners are objects that executes an external command (such as calling a python or julia or bash script)

        RunnerVariants class calls scripts that does the following:
            1. Call a script that generates code for variant algorithms.
            2. Call a script that executes the variant algorithms and outputs a csv file consisting of time measurements
            3. Call a script that generates another script which defines cretain measurement strategy
            (such as measuring only a subset of algorithms.)

        """
        super().__init__(backend_manager)

        self.script_dir = script_dir
        self.operand_sizes = operand_sizes
        self.operands_dir_name = "_".join(self.operand_sizes)
        self.operands_dir = os.path.join(self.script_dir,
                                         "experiments",
                                         '{}T/'.format(threads),
                                         self.operands_dir_name)

        self.backend_commands = backend_commands
        self.threads = threads
        # In order to check the status of jobs submitted to a bacth system,
        # job name should match with the job name mentioned in the bacth script
        self.job_name = "{}_T{}".format(self.operands_dir_name, self.threads)

    def generate_variants_for_measurements(self, generation_script):
        """calls a script that generates variants"""
        script_path = os.path.join(self.script_dir, generation_script)
        args = self.operand_sizes + ["--threads={}".format(self.threads)]
        msg = "{} run: Generate variants"
        if not self.backend_manager:
            call = ["python", script_path] + args
            ret = self.execute_subprocess_local(call, msg.format("Local"))
            return ret
        else:
            cmd = self.backend_commands.build_cmd("python", script_path, " ".join(args))
            ret = self.execute_subprocess_backend(cmd, msg.format("Backend interactive"))
            return ret

    def measure_variants(self, app, runner_script, submit_cmd=None):
        """
        executes a script that measures the variants and generates an output file.txt
        The measurement can be done either locally, in the backend interactively or submnitted
        to a batch system in the backend.
        """
        runner_path = os.path.join(self.operands_dir, runner_script)
        msg = "{machine} run: " + "Measurements from {script}".format(script=runner_script)
        if not self.backend_manager:
            if os.path.exists(runner_path):
                print("Running Measurements locally")
                call = [app, runner_path]
                ret = self.execute_subprocess_local(call, msg.format(machine="Local"))
                return ret
            else:
                print(bcolors.FAIL + "File not found: " + msg.format(machine="Local") + bcolors.ENDC)
                return -1
        else:
            if not submit_cmd:
                print("Running Measurements Backend interactive")
                cmd = self.backend_commands.build_cmd(app, runner_path)
                ret = self.execute_subprocess_backend(cmd, msg.format(machine="Backend interactive"))
                return ret
            else:
                print("Running Measurements Backend batch")
                cmd = self.backend_commands.submit_job_cmd(submit_cmd, app, runner_path)
                ret = self.execute_subprocess_backend(cmd, msg.format(machine="Backend batch"))
                return ret

    def generate_measurements_script(self, generate_measurement_script, variants, run_id, reps):
        script_path = os.path.join(self.operands_dir, generate_measurement_script)
        cmd_args = "--algs {algs} --rep {rep} --threads {threads} --id {run_id}".format(algs=" ".join(variants),
                                                                                        rep=reps,
                                                                                        threads=self.threads,
                                                                                        run_id=run_id)
        msg = "{machine} run: " + "Generate Measurement script {run_id}".format(run_id=run_id)
        if not self.backend_manager:
            if os.path.exists(script_path):
                call = ["python", script_path] + cmd_args.split()
                ret = self.execute_subprocess_local(call, msg.format(machine="Local"))
                return ret
            else:
                print(bcolors.FAIL + "File not found: " + msg.format(machine="Local") + bcolors.ENDC)
                return -1
        else:
            cmd = self.backend_commands.build_cmd("python", script_path, cmd_args)
            ret = self.execute_subprocess_backend(cmd, msg.format(machine="Backend interactive"))
            return ret

    def clean(self):
        """remove arguments folder"""
        if not self.backend_manager:
            if os.path.exists(self.operands_dir):
                shutil.rmtree(self.operands_dir)
            else:
                print(bcolors.FAIL + "Folder not found: {}".format(self.operands_dir) + bcolors.ENDC)
                return -1
        else:
            cmd = "rm -rf {}".format(self.operands_dir)
            ret = self.execute_subprocess_backend(cmd, msg="Removing directory {}".format(self.operands_dir))
            return ret

