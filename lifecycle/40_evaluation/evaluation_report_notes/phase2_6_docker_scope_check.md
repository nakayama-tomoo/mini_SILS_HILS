# Phase 2.6 Docker Scope Check

## Purpose

This note records the Docker scope cleanup after promoting C++ SILS to a top-level implementation directory.

## Context

C++ SILS is now located at:

    implementations/cpp_sils/

The previous Python SILS Dockerfile referenced the old nested C++ location:

    cpp/build/run_scenario

This was no longer valid after Phase 2.

## Decision Applied

Python SILS Docker is now treated as Python SILS focused.

It does not build or run C++ SILS.

The Docker build context is the repository root:

    .

The Dockerfile remains at:

    implementations/python_sils/docker/Dockerfile

## Docker Build Command

The following command was executed from the repository root:

    docker build -t mini-sils-python-sils -f implementations/python_sils/docker/Dockerfile .

## Docker Run Command

The following command was executed:

    docker run --rm mini-sils-python-sils

## Docker Check Result

Result:

    PASS

Observed result:

    15 passed

## Non-Docker Check Results

The following checks were executed before the Docker verification:

    python3 -m pytest
    python3 tools/run_suite.py
    python3 tools/compare_all_results.py
    python3 tools/generate_verification_report.py
    ctest --test-dir implementations/cpp_sils/build --output-on-failure

Observed results:

    Python tests: 15 passed
    C++ CTest: 10 passed
    Scenario suite: PASS
    Verification report: generated successfully

## CI Update

The root GitHub Actions workflow now uses the repository root as Docker build context.

This allows the Docker image to access shared assets such as:

    common/
    implementations/python_sils/

The Docker image name is:

    mini-sils-python-sils

## Remaining Notes

C++ SILS Docker support is deferred.

Future options include:

    1. Add implementations/cpp_sils/docker/Dockerfile.
    2. Add a top-level integration Dockerfile.
    3. Keep Docker limited to Python SILS for the initial PoC.
