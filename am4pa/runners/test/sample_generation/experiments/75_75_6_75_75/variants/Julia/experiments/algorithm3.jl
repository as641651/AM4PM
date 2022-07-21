using LinearAlgebra.BLAS
using LinearAlgebra

function algorithm3(ml0::Array{Float64,2}, ml1::Array{Float64,2}, ml2::Array{Float64,2}, ml3::Array{Float64,2})
    start::Float64 = 0.0
    finish::Float64 = 0.0
    Benchmarker.cachescrub()
    start = time_ns()

    # cost: 9.79e+05 FLOPs
    # A: ml0, full, B: ml1, full, C: ml2, full, D: ml3, full
    ml4 = Array{Float64}(undef, 6, 75)
    # tmp3 = (C D)
    gemm!('N', 'N', 1.0, ml2, ml3, 0.0, ml4)

    # A: ml0, full, B: ml1, full, tmp3: ml4, full
    ml5 = Array{Float64}(undef, 75, 75)
    # tmp5 = (B tmp3)
    gemm!('N', 'N', 1.0, ml1, ml4, 0.0, ml5)

    # A: ml0, full, tmp5: ml5, full
    ml6 = Array{Float64}(undef, 75, 75)
    # tmp6 = (A tmp5)
    gemm!('N', 'N', 1.0, ml0, ml5, 0.0, ml6)

    # tmp6: ml6, full
    # Y = tmp6

    finish = time_ns()
    return (tuple(ml6), (finish-start)*1e-9)
end