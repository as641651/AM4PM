using LinearAlgebra.BLAS
using LinearAlgebra

function recommended(A::Array{Float64,2}, B::Array{Float64,2}, C::Array{Float64,2}, D::Array{Float64,2})
    start::Float64 = 0.0
    finish::Float64 = 0.0
    Benchmarker.cachescrub()
    start = time_ns()

    Y = A*B*C*D;

    finish = time_ns()
    return (tuple(Y), (finish-start)*1e-9)
end