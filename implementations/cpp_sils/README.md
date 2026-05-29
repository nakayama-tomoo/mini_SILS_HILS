# C++ fan_control

## Purpose

This directory contains the C++ implementation of the fictional electric radiator fan control logic used in the mini SILS(Software-in-the-Loop Simulation) PoC(Proof of Concept).

The purpose is to compare:

- Python reference implementation
- C++ implementation closer to embedded software development

using the same fictional control rules and boundary conditions.

## Current Contents

- include/fan_control.hpp
- src/fan_control.cpp
- src/main.cpp
- tests/test_fan_control.cpp

## Build Example

Build the sample executable:

g++ -std=c++17 \
    cpp/src/main.cpp \
    cpp/src/fan_control.cpp \
    -Icpp/include \
    -o cpp/main

Run:

./cpp/main

## GoogleTest Example

Build the GoogleTest executable:

g++ -std=c++17 \
    cpp/tests/test_fan_control.cpp \
    cpp/src/fan_control.cpp \
    -Icpp/include \
    -I/opt/homebrew/include \
    -L/opt/homebrew/lib \
    -lgtest \
    -lgtest_main \
    -pthread \
    -o cpp/test_fan_control

Run:

./cpp/test_fan_control

## Current Status

- fan_control C++ implementation completed
- GoogleTest unit tests implemented
- UT-01 to UT-10 passed
- local Mac build confirmed

## CMake Build Example

Configure:

cmake -S cpp -B cpp/build

Build:

cmake --build cpp/build

Run sample executable:

./cpp/build/fan_control_main

Run GoogleTest executable:

./cpp/build/test_fan_control

Run CTest:

cd cpp/build
ctest --output-on-failure
cd ../..
