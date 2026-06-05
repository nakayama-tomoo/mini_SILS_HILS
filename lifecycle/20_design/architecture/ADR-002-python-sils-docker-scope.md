# ADR-002: Python SILS Docker Scope

## Status

Accepted for Mini-SILS-HILS PoC restructuring.

## Context

C++ SILS was promoted from:

    implementations/python_sils/cpp/

to:

    implementations/cpp_sils/

The existing Python SILS Dockerfile still referenced:

    cpp/build/run_scenario

This created a mismatch because C++ SILS is no longer located under the Python SILS implementation directory.

In addition, after Phase 1, the canonical scenario source is:

    common/scenario/

If the Docker build context is limited to:

    implementations/python_sils/

the Docker image cannot access the shared common scenario assets.

## Decision

The Python SILS Dockerfile shall be treated as a Python SILS focused Dockerfile.

It should not build or execute C++ SILS.

The Docker build context should be the repository root so that the image can access:

    common/
    implementations/python_sils/
    pyproject.toml
    requirements files

C++ SILS Docker support should be handled separately in a later phase.

Candidate future options:

    1. Create implementations/cpp_sils/docker/Dockerfile for C++ SILS.
    2. Create a top-level integration Dockerfile for multi-environment execution.
    3. Keep Docker usage limited to Python SILS for the initial PoC.

## Consequences

Positive consequences:

- Python SILS Docker no longer depends on the old nested C++ path.
- The Docker build becomes consistent with the new folder structure.
- C++ SILS remains a separate replaceable implementation target.
- The CI workflow can still validate the Docker image.

Trade-offs:

- Python SILS Docker no longer validates C++ SILS.
- C++ SILS Docker support is deferred to a later phase.
- The Docker build context changes from implementations/python_sils to the repository root.

## Scope

This decision applies only to the personal Mini-SILS-HILS PoC.

It does not define any company, customer, or production Docker policy.
