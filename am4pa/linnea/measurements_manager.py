from .data_manager import DataManagerLinnea
from .operands_sampler import OperandsSamplerBase


class MeasurementsMaganer:
    def __init__(self,data_manager:DataManagerLinnea, operands_sampler:OperandsSamplerBase,thread_str):
        self.dml = data_manager
        self.ops = operands_sampler
        self.thread_str = thread_str
        self.threads = int(self.thread_str.split('T')[0])
        
    
    def generate_basic_variants(self):
        op_list = self.ops.get_operands_basics()
        self._generate_variants(op_list)
        
 
    def generate_variants_sampler(self,n):    
        op_list = []
        for i in range(n):
            op_list.append(self.ops.sample())
        self._generate_variants(op_list)
            
    
    def _generate_variants(self,op_list):
        for op in op_list:
            op_str = self.get_op_string(op)
            if not self.thread_str in self.dml.operands_data:
                self.dml.generate_variants(self.threads,op_str)
            elif not op_str in self.dml.operands_data[self.thread_str]:
                self.dml.generate_variants(self.threads,op_str)
    
    def measure_variants(self,reps,run_id,bSlrum):
        
        op_strs = self.dml.operands_data[self.thread_str]
        
        if self.thread_str in self.dml.measurements_data:    
            md = self.dml.measurements_data[self.thread_str]
        else:
            md = {}
        
        for op_str in op_strs:
            bMeasure = False
            if not op_str in md:
                bMeasure = True
            elif str(run_id) not in md[op_str]:
                bMeasure = True
            
            if bMeasure:
                self.dml.measure_variants(self.threads,op_str,reps,run_id,bSlrum)

    def check_completed_slrum_jobs(self):
        self.dml.check_completed_slrum_jobs()
        
        
    def get_op_string(self, op):
        return '_'.join(map(str,op))
    