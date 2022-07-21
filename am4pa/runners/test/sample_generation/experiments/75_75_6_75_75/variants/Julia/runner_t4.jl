using Test
using Logging
using MatrixGenerator

using LinearAlgebra.BLAS
BLAS.set_num_threads(4)

include("operand_generator.jl")
include("experiments/algorithm0.jl")
include("reference/naive.jl")
include("reference/recommended.jl")

function main()
    matrices = operand_generator()

    @info("Performing Test run...")
    result_naive = collect(naive(map(copy, matrices)...)[1])
    result_recommended = collect(recommended(map(copy, matrices)...)[1])
    test_result = isapprox(result_naive, result_recommended, rtol=1e-3)
    @test test_result
    result = collect(algorithm0(map(MatrixGenerator.unwrap, map(copy, matrices))...)[1])
    test_result = isapprox(result, result_recommended, rtol=1e-3)
    @test test_result # this somehow avoids too much memory being used                                         
    @info("Test run performed successfully")

    n = 2000
    rand(n, n)*rand(n, n) # this seems to help to reduce some startup noise

    @info("Running Benchmarks...")
    plotter = Benchmarker.Plot("julia_results_variants", ["algorithm"; "threads"]);
    Benchmarker.add_data(plotter, ["algorithm0"; 4], Benchmarker.measure(10, algorithm0, map(MatrixGenerator.unwrap, matrices)...) );
    Benchmarker.add_data(plotter, ["naive_julia"; 4], Benchmarker.measure(10, naive, matrices...) );
    Benchmarker.add_data(plotter, ["recommended_julia"; 4], Benchmarker.measure(10, recommended, matrices...) );
    Benchmarker.finish(plotter);
    @info("Benchmarks complete")
end

main()
