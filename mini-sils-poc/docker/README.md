# Docker Execution

## Purpose

This Docker environment provides a reproducible execution environment for the mini SILS(Software-in-the-Loop Simulation) PoC(Proof of Concept).

The container includes:

- Python
- pytest
- CMake
- GoogleTest
- CTest

## Build

docker build -t mini-sils-poc -f docker/Dockerfile .

## Run

docker run --rm mini-sils-poc
