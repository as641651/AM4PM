function [out] = operand_generator()
    import MatrixGenerator.*;
    out{ 1 } = generate([75,75], Shape.General(), Properties.Random([-1, 1]));
    out{ 2 } = generate([75,6], Shape.General(), Properties.Random([-1, 1]));
    out{ 3 } = generate([6,75], Shape.General(), Properties.Random([-1, 1]));
    out{ 4 } = generate([75,75], Shape.General(), Properties.Random([-1, 1]));
end