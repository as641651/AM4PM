import os
from algorithm_ranking import MeasurementsManager
from ..runners import RunnerVariants
from ..data_integration import DataCollector
from ..data_proccessing import CaseDurationsManager
from ..data_proccessing import FilterOnKPIs

class MeasurementsLinnea(MeasurementsManager):
    def __init__(self,linnea_config, op_sizes):
        super().__init__()
        
        self.linnea_config = linnea_config
        self.op_sizes = op_sizes
        self.runner = None
        self.data_collector = None
        self.case_durations_manager = None
        self.h0 = None
        self.init()

    def init(self):
        if self.linnea_config.backend:
            self.runner = RunnerVariants(self.op_sizes,
                                    self.linnea_config.backend_dir,
                                    threads = self.linnea_config.threads,
                                    backend_manager = self.linnea_config.bm,
                                    backend_commands= self.linnea_config.bm_cmds)
            
            local_operands_dir = os.path.join(self.linnea_config.local_dir,self.linnea_config.local_bfolder,self.runner.operands_dir_name)
            if not os.path.exists(local_operands_dir):
                os.makedirs(local_operands_dir)
            
            self.data_collector = DataCollector(local_operands_dir,
                                           self.runner.operands_dir, self.linnea_config.bm)
                
        else:
            self.runner = RunnerVariants(self.op_sizes,
                                    self.linnea_config.local_dir,
                                    threads = self.linnea_config.threads)
            self.data_collector = DataCollector(self.runner.operands_dir)
        
    def generate_variants(self, bGenerate=True):
        if bGenerate:    
            self.runner.generate_variants_for_measurements(self.linnea_config.generation_script)
        
    def gather_competing_variants(self, bmeasure_once=False, rel_duration=1.2):
        case_table = self.data_collector.get_case_table()
        
        if bmeasure_once:
            self.runner.measure_variants(app=self.linnea_config.app,
                                        runner_script=self.linnea_config.runner_script)
            measurements_table = self.data_collector.get_runtimes_table()
            
            filterKPI = FilterOnKPIs(case_table,measurements_table)
            df = filterKPI.filter_on_flops_and_rel_duration(rel_duration)
            
            self.h0 = df['case:concept:name'].tolist()
        else:
            self.h0 = case_table['case:concept:name'].tolist()
            
        self.case_durations_manager = CaseDurationsManager()
        return self.h0
    
    def measure(self, rep_steps,run_id, bSlrum=False):
        self.runner.generate_measurements_script(self.linnea_config.measurements_script,
                                                self.h0,
                                                run_id,
                                                rep_steps)
        
        if not bSlrum:
            self.runner.measure_variants(app=self.linnea_config.app,
                                    runner_script=self.linnea_config.runner_competing_script.format(run_id))
            
            self.collect_measurements(run_id)
        else:
            self.runner.measure_variants(app=self.linnea_config.app,
                                    runner_script=self.linnea_config.runner_competing_script.format(run_id),
                                        submit_cmd=self.linnea_config.slrum_submit_cmd)
            
        
    def collect_measurements(self, run_id):
        df = self.data_collector.get_runtimes_competing_table(run_id)
        self.case_durations_manager.add_case_durations(df)
        
    def get_alg_measurements(self):
        return self.case_durations_manager.get_alg_measurements()
        