using MatrixGenerator
using LinearAlgebra.BLAS
BLAS.set_num_threads(4)

include("experiments/algorithm1.jl")
include("experiments/algorithm5.jl")
include("experiments/algorithm4.jl")
include("experiments/algorithm0.jl")
include("experiments/algorithm3.jl")
include("experiments/algorithm2.jl")

include("operand_generator.jl")

function main()

    matrices = operand_generator()

    io = open("/Users/aravind/exercise/PyCharmProjects/performance-analyzer/am4pa/am4pa/runner_variants/test/sample_generation/experiments/75_75_6_75_75/run_times.csv","w")
    write(io, "case:concept:name;concept:name;concept:flops;concept:operation;concept:kernel;timestamp:start;timestamp:end\n")

    n = 2000
    rand(n, n)*rand(n, n) # this seems to help to reduce some startup noise

    ret,times = algorithm1(map(MatrixGenerator.unwrap, map(copy, matrices))...)
    write_algorithm1_to_eventlog(io, "algorithm1", times)
    temp = rand(25000) # cache trashing

    ret,times = algorithm5(map(MatrixGenerator.unwrap, map(copy, matrices))...)
    write_algorithm5_to_eventlog(io, "algorithm5", times)
    temp = rand(25000) # cache trashing

    ret,times = algorithm4(map(MatrixGenerator.unwrap, map(copy, matrices))...)
    write_algorithm4_to_eventlog(io, "algorithm4", times)
    temp = rand(25000) # cache trashing

    ret,times = algorithm0(map(MatrixGenerator.unwrap, map(copy, matrices))...)
    write_algorithm0_to_eventlog(io, "algorithm0", times)
    temp = rand(25000) # cache trashing

    ret,times = algorithm3(map(MatrixGenerator.unwrap, map(copy, matrices))...)
    write_algorithm3_to_eventlog(io, "algorithm3", times)
    temp = rand(25000) # cache trashing

    ret,times = algorithm2(map(MatrixGenerator.unwrap, map(copy, matrices))...)
    write_algorithm2_to_eventlog(io, "algorithm2", times)
    temp = rand(25000) # cache trashing




end

main()