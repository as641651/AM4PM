cmake_minimum_required(VERSION 3.0)
project(variants)

find_package(LibTests REQUIRED)

add_executable(runner_t4 runner_t4.cpp)
target_link_libraries(runner_t4 PRIVATE libtests)
set_target_properties(runner_t4 PROPERTIES CXX_STANDARD 14)

