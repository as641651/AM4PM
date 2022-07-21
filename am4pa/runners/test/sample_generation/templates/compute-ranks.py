import sys
import os
import pathlib
this_dir = pathlib.Path(__file__).parent.resolve()
sys.path.append(os.path.join(this_dir,"../../../../utils"))

from data_collector import DataCollector
from filter_on_kpis import FilterOnKPIs
from runner_competing import RunnerCompeting
from measure_and_rank import measure_and_rank
import argparse

if __name__ == "__main__":

   parser = argparse.ArgumentParser(description='compute ranks ')
   parser.add_argument('--rep_steps', type=int, default=3)
   parser.add_argument('--max_rep', type=int, default=50)
   parser.add_argument('--eps', type=float, default=0.001)
   parser.add_argument('--threads', type=int, default=4)
   parser.add_argument('--algs', nargs='+', default=[])

   if not os.path.exists(os.path.join(this_dir,"run_times.csv")):
       print("PLease run 'julia runner.jl' first")
       exit(-1)

   args = parser.parse_args()
   threads = args.threads
   rep_steps = args.rep_steps
   eps = args.eps
   max_rep = args.max_rep

   dc = DataCollector(this_dir)

   if len(args.algs) > 0:
       algs_seq_h0 = args.algs
   else:
       case_table = dc.get_case_table()
       measurements = dc.get_all_runtimes_table()

       kpi_filter = FilterOnKPIs(case_table, measurements)
       competing_cases = kpi_filter.filter_on_flops_and_rel_duration()
       algs_seq_h0 = kpi_filter.get_alg_seq_sorted_on_duration(competing_cases)

   runner_competing = RunnerCompeting(algs_seq_h0, this_dir,
                                            threads=threads)

   rank_variants, _, mean_ranks = measure_and_rank(runner_competing,
                                                    dc,
                                                    algs_seq_h0,
                                                    rep_steps,
                                                    eps,
                                                    max_rep)


   ranks = rank_variants.calculate_ranks()
   print(ranks)
   print(mean_ranks)

   ranks.to_csv(os.path.join(this_dir,"ranks.csv"), sep=';')
   mean_ranks.to_csv(os.path.join(this_dir,"mean_ranks.csv"), sep=';')
