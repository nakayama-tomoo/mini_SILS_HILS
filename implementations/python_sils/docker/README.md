# Python SILS Docker

This Dockerfile is for Python SILS only.

## Scope

This image validates the Python SILS package and tests.

It does not build or run C++ SILS.

C++ SILS is located at:

    implementations/cpp_sils/

C++ SILS Docker support may be added separately in a later phase.

## Build

Run from the repository root:

    docker build -t mini-sils-python-sils -f implementations/python_sils/docker/Dockerfile .

## Run

Run from the repository root:

    docker run --rm mini-sils-python-sils

## Notes

The Docker build context is the repository root so that the image can access shared assets such as:

    common/
    implementations/python_sils/

This is aligned with the Mini-SILS-HILS architecture where common scenario assets are shared across environments.
