import subprocess

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class ExecuteSubProcess:
    def __init__(self, backend_manager=None):
        self.backend_manager = backend_manager

    def process_return_codes_from_subprocesses(self, ret, msg=""):
        """return code 0: successful execution of the subprocess
        return code -1: Unsuccessful execution of the subprocess
        Subprocess error code is the return code from the subprocess"""
        if ret == 0:
            print(bcolors.OKGREEN + "Success: {}".format(msg) + bcolors.ENDC)
            return 0
        else:
            print(bcolors.FAIL + "Error: {}\nSub process error code: {}".format(msg, ret) + bcolors.ENDC)
            return -1

    def execute_subprocess_local(self, call, msg=""):
        """call a python sub process"""
        print(call)
        completed_proccess = subprocess.run(call)
        ret = completed_proccess.returncode
        return self.process_return_codes_from_subprocesses(ret, msg)

    def execute_subprocess_backend(self, cmd, msg=""):
        """submit a backend command to a backend manager"""
        if self.backend_manager:
            stdout, ret = self.backend_manager.run_cmd(cmd)
            print(stdout.readlines())
            return self.process_return_codes_from_subprocesses(ret, msg)
        else:
            print(bcolors.FAIL + "No backend manager" + bcolors.ENDC)
            return -1
