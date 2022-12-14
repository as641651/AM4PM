from backend_manager import BackendManager, Commands
import os


#should go into am4pa
class LinneaConfig:
    def __init__(self, problem, threads):
        
        self.problem = problem
        self.threads = threads
        #self.op_sizes = op_sizes
        #self.num_ops = len(op_sizes)
        
        self.local_dir = ""
        
        # Backend set up
        self.server = ""
        self.uname = ""
        self.server = ""
        self.backend_dir = None
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
        self.local_dir = local_dir
        
    def setup_backend_details(self, server, uname, init_script, backend_dir):
        self.server = server
        self.uname = uname
        self.init_script = init_script
        self.backend_dir = backend_dir
        self.backend = True
        self.slrum_submit_cmd = "sbatch submit.sh"
        
    def connect_backend(self):
        if self.backend:
            self.bm = BackendManager(server=self.server, uname = self.uname)
            self.bm.connect()
            self.bm_cmds = Commands(source = self.init_script)
        
            
    def sync_local_and_backend(self):
        if self.bm:
            if self.bm.connected:
                self.bm.copy_to_backend(self.local_dir, self.backend_dir)
            
    def check_backend_folder_sync(self):
        if self.bm:
            return self.bm.check_if_file_exists(os.path.join(self.backend_dir,self.generation_script))
        return False
        