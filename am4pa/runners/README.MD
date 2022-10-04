# RunnerVariants

Runners are objects that executes an external command (such as calling a python or julia or bash script)

RunnerVariants class calls scripts that does the following:
  1. Call a script that generates code for variant algorithms.
  2. Call a script that executes the variant algorithms and outputs a csv file consisting of time measurements
  3. Call a script that generates another script which defines cretain measurement strategy (such as measuring only a subset of algorithms.)
            
