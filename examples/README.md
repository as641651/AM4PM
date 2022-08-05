## Runner:

Runners are objects that executes an external command (such as calling a python or julia or bash script). Running the external command outputs a csv file in a format that can be handled by the data_integration sub module. The inputs are the names of the script files that executes the required operation.

The execution of the scripts can either be local, in the backend or submitted to a batch system.

## Input:

Implementation that generates and measures variant codes for an input linear algebra expression. The generated code has timestamps inserted before and after the kernel calls.

# Local Measurements:
### 1. Generate variants for an instance of a linear algebra expression.
An instance refers to an linear algebra expression with a specific operand sizes

```python
operand_sizes = ["75","75","6","75","75"]
script_dir = "sample_generation/"
runner_local = RunnerVariants(operand_sizes, script_dir)
```


Here, generate-variants-linnea.py is a script file that generates variant codes using the Linnea interface

```python
runner_local.generate_variants_for_measurements(generation_script="generate-variants-linnea.py")
```
output1 : here the image of the first output must be added.

### 2. Measure variants
Executing generate-variants-linnea.py creates a subdirectory experiments/75_75_6_75_75/, which consists of the generated code and a number of scripts.

```python
!ls sample_generation/experiments/75_75_6_75_75/
```
output2: an image of the output

runner.jl is a script that executes all the variants once and outputs a file run_times.csv that consists of the run time for each variant.

```python
runner_local.measure_variants(app="julia", runner_script="runner.jl")
```
output3:

```python
!ls sample_generation/experiments/75_75_6_75_75/
```
output4:

generate_measurement_scripts.py is a file that generates a measurement script with a specific identifier (run_id) that repeats a given set of variant for a said (rep) numnber of times. For instance, the resulting script for identifier 0 is runner_competing_0.jl

```python
measurements_script = "generate-measurements-script.py"
variants = ['algorithm0', 'algorithm1']
reps = 3
run_id = 0
```
```python
runner_local.generate_measurements_script(measurements_script, variants, run_id, reps)
```
output5:
