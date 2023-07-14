import os
from unicodedata import east_asian_width
from algorithm_ranking import MeasurementsManager
from ..runners import RunnerVariants
from ..data_integration import DataCollector
from ..data_proccessing import CaseDurationsManager
from ..data_proccessing import FilterOnKPIs

class MeasurementsLinnea(MeasurementsManager):
    def __init__(self,linnea_config, op_sizes,threads=None):
        super().__init__()
        
        self.linnea_config = linnea_config
        self.op_sizes = op_sizes
        self.runner = None
        self.data_collector = None
        self.case_durations_manager = CaseDurationsManager()
        self.h0 = None
        if not threads:
            self.threads = int(self.linnea_config.threads)
        self.threads = int(threads)

        self.init()
        self.measured_once = False

    def init(self):
        if self.linnea_config.backend:
            self.runner = RunnerVariants(self.op_sizes,
                                    self.linnea_config.backend_dir,
                                    threads = self.threads,
                                    backend_manager = self.linnea_config.bm,
                                    backend_commands= self.linnea_config.bm_cmds)
            
            local_operands_dir = os.path.join(self.linnea_config.local_dir,
                                            self.linnea_config.local_bfolder, 
                                            '{}T'.format(self.threads),
                                            self.runner.operands_dir_name)
            if not os.path.exists(local_operands_dir):
                os.makedirs(local_operands_dir)
            
            self.data_collector = DataCollector(local_operands_dir,
                                           self.runner.operands_dir, self.linnea_config.bm)
                
        else:
            self.runner = RunnerVariants(self.op_sizes,
                                    self.linnea_config.local_dir,
                                    threads = self.threads)
            self.data_collector = DataCollector(self.runner.operands_dir)
        
    def generate_variants(self, bGenerate=True):
        if bGenerate:    
            self.runner.generate_variants_for_measurements(self.linnea_config.generation_script)

    def measure_once(self):
        self.runner.measure_variants(app=self.linnea_config.app,
                                        runner_script=self.linnea_config.runner_script)
        self.measured_once = True

    def gather_all_variants(self):
        case_table = self.data_collector.get_case_table()
        self.h0 = case_table['case:concept:name'].tolist()

    def filter_on_flops_rel_duration(self, rel_duration=1.2):
        case_table = self.data_collector.get_case_table()
        if self.measured_once:
            measurements_table = self.data_collector.get_runtimes_table()
            filterKPI = FilterOnKPIs(case_table,measurements_table)
            df = filterKPI.filter_on_flops_and_rel_duration(rel_duration)
            self.h0 = df['case:concept:name'].tolist()
        else:
            print("Run 'measure once'. Returning all variants")
            self.h0 = case_table['case:concept:name'].tolist()

    def filter_on_flops(self, rel_flops=1.2):
        case_table = self.data_collector.get_case_table()
        filterKPI = FilterOnKPIs(case_table)
        df = filterKPI.filter_on_rel_flops(rel_flops=rel_flops)
        self.h0 = df['case:concept:name'].tolist()
        

    ## Depreicated
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
            
        #self.case_durations_manager = CaseDurationsManager()
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
            
        
    def filter_table(self ,df):
        return df[df.apply(lambda x: x['case:concept:name'].split('_')[0] in self.h0, axis=1)]

    def collect_measurements(self, run_id):
        df = self.data_collector.get_runtimes_competing_table(run_id)
        df = self.filter_table(df)
        self.case_durations_manager.add_case_durations(df)
        
    def get_alg_measurements(self):
        d_ = self.case_durations_manager.get_alg_measurements()
        f_ = {alg:d_[alg] for alg in d_.keys() if alg in self.h0 }
        return f_
        