cmake_minimum_required(VERSION 3.16)

project(mini_sils_cpp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

enable_testing()

find_package(GTest REQUIRED)

include_directories(include)

add_library(
    fan_control_lib
    src/fan_control.cpp
)

add_executable(
    fan_control_main
    src/main.cpp
)

target_link_libraries(
    fan_control_main
    fan_control_lib
)

add_executable(
    test_fan_control
    tests/test_fan_control.cpp
)

target_link_libraries(
    test_fan_control
    fan_control_lib
    GTest::gtest_main
)

include(GoogleTest)

gtest_discover_tests(test_fan_control)

add_executable(
    run_scenario
    scenarios/run_scenario.cpp
)

target_link_libraries(
    run_scenario
    fan_control_lib
)
