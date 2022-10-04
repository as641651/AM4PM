# RunnerVariants

Runners are objects that executes an external command (such as calling a python or julia or bash script)

RunnerVariants class calls scripts that does the following:
  1. Call a script that generates code for variant algorithms.
  2. Call a script that executes the variant algorithms and outputs a csv file consisting of time measurements
  3. Call a script that generates another script which defines cretain measurement strategy (such as measuring only a subset of algorithms.)
            
## generate_variants_for_measurements

calls a script that generates variants

## measure_variants

executes a script that measures the variants and generates an output file.txt
The measurement can be done either locally, in the backend interactively or submnitted to a batch system in the backend.

## generate_measurements_script


## clean

remove arguments folder
