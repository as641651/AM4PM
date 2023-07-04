from backend_manager import BackendManager, Commands
import os
from .expr_init import expr_init


#should go into am4pa
class LinneaConfig:
    def __init__(self, problem_file, threads):
        
        self.problem_file = problem_file
        self.threads = threads
        #self.op_sizes = op_sizes
        #self.num_ops = len(op_sizes)
        
        self.local_dir = ""
        
        # Backend set up
        self.server = ""
        self.uname = ""
        self.server = ""
        self.backend_dir = None
        self.backend_root = None
        self.backend = False
        self.bm = None
        self.bm_cmds = None
        
        self.generation_script = 'generate-variants-linnea.py'
        self.measurements_script = "generate-measurements-script.py"
        self.local_bfolder = "cluster-data"
        self.slrum_submit_cmd = None
        
        self.app = "julia"
        self.runner_script = "runner.jl"
        self.runner_competing_script = 'runner_competing_{}.jl'
        
    def set_local_directory(self,local_dir):
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        self.local_dir = local_dir
        
    def setup_backend_details(self, server, uname, init_script, backend_root):
        self.server = server
        self.uname = uname
        self.init_script = init_script
        self.backend_root = backend_root
        self.backend_dir = os.path.join(self.backend_root, os.path.basename(self.local_dir))
        self.backend = True
        self.slrum_submit_cmd = "sbatch submit.sh"
        
    def connect_backend(self):
        if self.backend:
            self.bm = BackendManager(server=self.server, uname = self.uname)
            self.bm.connect()
            self.bm_cmds = Commands(source = self.init_script)
        
            
    def sync_local_and_backend(self):
        expr_init(self.problem_file, self.local_dir)
        if self.bm:
            if self.bm.connected:
                self.bm.copy_to_backend(self.local_dir, self.backend_root)
            
    def check_backend_folder_sync(self):
        if self.bm:
            return self.bm.check_if_file_exists(os.path.join(self.backend_dir,self.generation_script))
        return False
        