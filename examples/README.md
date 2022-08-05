## Runner:

Runners are objects that executes an external command (such as calling a python or julia or bash script). Running the external command outputs a csv file in a format that can be handled by the data_integration sub module. The inputs are the names of the script files that executes the required operation.

The execution of the scripts can either be local, in the backend or submitted to a batch system.

## Input:

Implementation that generates and measures variant codes for an input linear algebra expression. The generated code has timestamps inserted before and after the kernel calls.

# Local Measurements:
## Generate variants for an instance of a linear algebra expression.

```python
operand_sizes = ["75","75","6","75","75"]
script_dir = "sample_generation/"
runner_local = RunnerVariants(operand_sizes, script_dir)
```
