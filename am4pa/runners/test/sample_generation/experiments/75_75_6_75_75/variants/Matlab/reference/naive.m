function [res, time] = naive(A, B, C, D)
    tic;
    Y = A*B*C*D;    
    time = toc;
    res = {Y};
end