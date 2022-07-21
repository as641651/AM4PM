#include <generator/generator.hpp>

template<typename Gen>
decltype(auto) operand_generator(Gen && gen)
{
    auto A = gen.generate({75,75}, generator::property::random{});
    auto B = gen.generate({75,6}, generator::property::random{}, generator::shape::not_square{});
    auto C = gen.generate({6,75}, generator::property::random{}, generator::shape::not_square{});
    auto D = gen.generate({75,75}, generator::property::random{});
    return std::make_tuple(A, B, C, D);
}