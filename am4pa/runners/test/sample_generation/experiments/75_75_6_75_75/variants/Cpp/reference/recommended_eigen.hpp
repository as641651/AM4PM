struct recommended_eigen
{
template<typename Type_A, typename Type_B, typename Type_C, typename Type_D>
decltype(auto) operator()(Type_A && A, Type_B && B, Type_C && C, Type_D && D)
{
    auto Y = (A*B*C*D).eval();

    typedef std::remove_reference_t<decltype(Y)> return_t;
    return return_t(Y);                         
}
};