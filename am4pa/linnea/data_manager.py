import os
import pandas as pd
from .linnea_config import LinneaConfig
from .measurements_linnea import MeasurementsLinnea
import json

class DataManagerLinnea:
    def __init__(self,linnea_config:LinneaConfig):
        self.lc = linnea_config
        
        self.config = None
        self.config_file = os.path.join(self.lc.local_dir, 'config.json')
        self.bNew_config = True
        self._get_config()
            
        self.operands_data = None    
        self.operands_file = os.path.join(self.lc.local_dir, 'operands.json')
        if os.path.exists(self.operands_file):
            with open(self.operands_file, 'r') as jf:
                self.operands_data = json.load(jf)
        elif self.lc.backend:
            self._pull_operands_backend()
        else:
            ## TODO:
            self.operands_data = {}
            
        self.mls = {}
        for thread_str,op_list in self.operands_data.items():
            self.mls[thread_str] = {}
            thread = thread_str.split('T')[0]
            for op in op_list:
                self.mls[thread_str][op] = MeasurementsLinnea(self.lc, op.split("_"),thread)
                self.mls[thread_str][op].gather_all_variants()
                
                
        self.measurements_data = None
        self.measurements_file = os.path.join(self.lc.local_dir, 'measurements.json')
        if os.path.exists(self.measurements_file):
            with open(self.measurements_file, 'r') as jf:
                self.measurements_data = json.load(jf)
        elif self.lc.backend:
            self._pull_measurement_ids_backend()
        else:
            ##TODO
            self.measurements_data = {}
            
                    
             
    def _get_config(self):
   
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as jf:
                self.config = json.load(jf)
            self._sanity_check()
            self.bNew_config = False
            
        else:
            self.config = {}
            self.config['problem'] = self.lc.problem_file
            self.config['backend'] = self.lc.backend
            self.config['server'] = self.lc.server
            self.config['uname'] = self.lc.uname
            self.config['local_dir'] = self.lc.local_dir
            
            self.lc.sync_local_and_backend()
            if self.lc.check_backend_folder_sync():
                self.config['backend_dir'] = self.lc.backend_dir
            else:
                self.config['backend_dir'] = 'Unsynced'
                
            self._update_json(self.config,self.config_file)
                
        print(self.config)
        
    def _sanity_check(self):
        
        msg = "This directory contains probelm with"
        
        assert self.config['backend'] == self.lc.backend, msg + " backend connected "
        
        if self.lc.backend:
            assert self.config['uname'] == self.lc.uname, msg + " backend uname {}".format(self.lc.uname)
            assert self.config['server'] == self.lc.server, msg + " backend server {}".format(self.lc.server)
            assert self.config['backend_dir'] == self.lc.backend_dir, msg + " backend dir {}".format(self.lc.backend_dir)
                    

    def _pull_operands_backend(self):
        
        assert self.lc.backend == True, "requires backend"
        
        exp_dir = os.path.join(self.lc.backend_dir, "experiments")
        data = {}
        
        if self.lc.bm.check_if_dir_exists(exp_dir):
            print("Experiments Directory {} exists at backend".format(exp_dir))
            cmd = 'ls {}'.format(exp_dir)
            ret, _ = self.lc.bm.run_cmd(cmd)
            threads = ret.readlines()
            
            for t in threads:
                t_dir = t.strip() 
                data[t_dir] = []
            
                cmd = 'ls {}'.format(os.path.join(exp_dir, t_dir))
                ret, _ = self.lc.bm.run_cmd(cmd)
                ops = ret.readlines()
                for op in ops:
                    data[t_dir].append(op.strip())
               
            self._update_json(data,self.operands_file)
                                     
        self.operands_data = data
        
        
    def _pull_measurement_ids_backend(self):
        
        assert self.lc.backend == True, "requires backend"
        exp_dir = os.path.join(self.lc.backend_dir, "experiments")
        
        data = {}
        if not self.lc.bm.check_if_dir_exists(exp_dir):
            self.measurements_data = data
            return
            
        for thread_str, op_sizes in self.operands_data.items():
            data[thread_str] = {}
            for op in op_sizes:
                
                cmd = 'ls {}/run_times_competing_*'.format(self.mls[thread_str][op].runner.operands_dir)
                ret, _ = self.lc.bm.run_cmd(cmd)
                runs = ret.readlines()
                if runs:
                    data[thread_str][op] = []
                    for run in runs:
                        run_id = run.split('_')[-1].split('.csv')[0]
                        data[thread_str][op].append(run_id)
                    
        
        if data:
            self._update_json(data, self.measurements_file)
            
        self.measurements_data = data
                            
    
    def _update_json(self,data,file_):
        with open(file_,'w') as jf:
            json.dump(data,jf)
    
    def generate_variants(self, thread, op_size):
        thread_str = '{}T'.format(thread)
        if not thread_str in self.mls:
            self.mls[thread_str] = {}
            
        ml = MeasurementsLinnea(self.lc, op_size.split("_"),thread)
        ml.generate_variants()
        if self.lc.bm.check_if_dir_exists(ml.runner.operands_dir):
            if not thread_str in self.operands_data:
                self.operands_data[thread_str] = []
            if not op_size in self.operands_data[thread_str]:
                self.operands_data[thread_str].append(op_size)
                self._update_json(self.operands_data,self.operands_file)
            ml.data_collector.delete_local_data()
            ml.gather_all_variants()
            
            bDirty = False
            if not thread_str in self.measurements_data:
                self.measurements_data[thread_str] = {}
                bDirty = True
            elif op_size in self.measurements_data[thread_str]:
                del self.measurements_data[thread_str][op_size]
                bDirty = True
            if bDirty:
                self._update_json(self.measurements_data,self.measurements_file)
            
            self.mls[thread_str][op_size] = ml
        
    def measure_variants(self, thread,op_size,reps,run_id):
        thread_str = '{}T'.format(thread)
        try:
            ml = self.mls[thread_str][op_size]
            ml.measure(reps,run_id)
            if not op_size in self.measurements_data[thread_str]:
                self.measurements_data[thread_str][op_size] = []
            if not run_id in self.measurements_data[thread_str][op_size]:
                self.measurements_data[thread_str][op_size].append(str(run_id))
                self._update_json(self.measurements_data, self.measurements_file)
            ml.data_collector.delete_local_competing_measurements_by_id(run_id)
        except KeyError:
            print("First Generate variants for the said thread and op_Size")
            
    def delete_measurements(self,thread,op_size,run_id):
        thread_str = '{}T'.format(thread)
        try:
            ml = self.mls[thread_str][op_size]
            ml.data_collector.delete_competing_measurements_by_id(run_id)
            if str(run_id) in self.measurements_data[thread_str][op_size]:
                self.measurements_data[thread_str][op_size].remove(str(run_id))
                self._update_json(self.measurements_data, self.measurements_file)
        except KeyError:
            print("First Generate and measure variants for the said thread and op_Size")
                
        