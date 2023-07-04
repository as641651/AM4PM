using MatrixGenerator
using LinearAlgebra.BLAS
BLAS.set_num_threads({threads})

{variants_includes}
include("operand_generator.jl")

function main()

    matrices = operand_generator()

    io = open("{runner_path}","w")
    write(io, "case:concept:name;concept:name;concept:flops;concept:operation;concept:kernel;timestamp:start;timestamp:end\n")

    n = 2000
    rand(n, n)*rand(n, n) # this seems to help to reduce some startup noise

{runner_code}


end

main()