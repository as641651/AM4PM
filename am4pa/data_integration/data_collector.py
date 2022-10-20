import os
import pandas as pd
import glob


class DataCollector:
    def __init__(self, local_data_dir, backend_data_dir=None, backend_manager=None):
        self.local_data_dir = local_data_dir
        self.backend_manager = backend_manager
        self.backend_data_dir = backend_data_dir

    def read_log(self, log_path):
        if os.path.exists(log_path):
            df = pd.read_csv(log_path, sep=';')
            return df
        return -1

    def get_table(self, table_name):
        table_path = os.path.join(self.local_data_dir, table_name)
        if os.path.exists(table_path):
            return self.read_log(table_path)
        elif self.backend_data_dir:
            backend_path = os.path.join(self.backend_data_dir, table_name)
            self.backend_manager.copy_from_backend(backend_path, self.local_data_dir)
            if os.path.exists(table_path):
                return self.read_log(table_path)

        return -1

    def get_case_table(self):
        return self.get_table("case_table.csv")

    def get_meta_table(self):
        """get event table without actual execution times."""
        return self.get_table("event_meta_table.csv")

    def get_runtimes_table(self):
        """get event table with actual execution times."""
        return self.get_table("run_times.csv")

    def get_runtimes_competing_table(self, run_id):
        return self.get_table("run_times_competing_{}.csv".format(run_id))

    def get_ranks(self):
        return self.get_table("ranks.csv")

    def get_mean_ranks(self):
        return self.get_table("mean_ranks.csv")

    def delete_competing_measurements(self):
        files = glob.glob(os.path.join(self.local_data_dir, "*_competing_*.csv"))
        for f in files:
            if os.path.exists(f):
                print("removing ", f)
                os.remove(f)
        if self.backend_manager:
            cmd = "rm -rf {arg_dir}/*_competing_*".format(arg_dir=self.backend_data_dir)
            ret = self.backend_manager.run_cmd(cmd)
            return ret
        return 0

    def delete_ranks(self):
        files = glob.glob(os.path.join(self.local_data_dir, "*ranks.csv"))
        for f in files:
            if os.path.exists(f):
                print("removing ", f)
                os.remove(f)
        if self.backend:
            cmd = "rm -rf {arg_dir}/*ranks.csv".format(arg_dir=self.backend_data_dir)
            ret = self.backend.run_cmd(cmd)
            return ret
        return 0

    def delete_local_data(self):
        files = glob.glob(os.path.join(self.local_data_dir, "*.csv"))
        for f in files:
            if os.path.exists(f):
                print("removing ", f)
                os.remove(f)
        return 0


