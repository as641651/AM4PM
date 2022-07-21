function [res, time] = recommended(A, B, C, D)
    tic;
    Y = A*B*C*D;    
    time = toc;
    res = {Y};
end