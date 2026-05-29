# Phase 2.5 Legacy C++ Reference Cleanup Note

## Purpose

This note records the remaining legacy C++ references after promoting C++ SILS to a top-level implementation directory.

## Current Architecture

C++ SILS is now located at:

    implementations/cpp_sils/

The previous location was:

    implementations/python_sils/cpp/

## Phase 2 Result

The following checks passed after the move:

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

## Remaining Legacy References

The following files may still contain references to the old nested C++ location:

    implementations/python_sils/docker/Dockerfile
    implementations/python_sils/.dockerignore
    implementations/python_sils/.gitignore
    implementations/python_sils/.github/workflows/python-test.yml

## Policy

These files are not Phase 2 blockers because the active execution path and root GitHub Actions workflow now use:

    implementations/cpp_sils/

However, they should be handled in a later cleanup phase to avoid confusion.

## Recommended Handling

### Dockerfile

Do not modify blindly.

The Python SILS Docker build context may need to be redesigned if it should also build or run C++ SILS.

Candidate options:

    1. Keep Python SILS Dockerfile Python-only.
    2. Create a separate C++ SILS Dockerfile under implementations/cpp_sils/docker/.
    3. Create a top-level integration Dockerfile for multi-environment execution.

### Python SILS .gitignore and .dockerignore

Remove stale cpp/results rules from Python SILS-specific ignore files because C++ SILS no longer lives under implementations/python_sils/cpp/.

### Nested GitHub Actions Workflow

The active workflow should be the root workflow:

    .github/workflows/python-test.yml

The nested workflow under:

    implementations/python_sils/.github/workflows/

should be reviewed and either removed or moved to documentation if it is no longer used.

