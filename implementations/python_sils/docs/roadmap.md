# Roadmap

## Phase 1: Python-only mini SILS

Goal:

Build a minimal SILS(Software-in-the-Loop Simulation) using Python and fictional fan control scenarios.

Current target:

- simplified electric radiator fan control
- pytest unit tests
- scenario CSV(Comma-Separated Values) execution
- result CSV(Comma-Separated Values) generation
- local Git management

Status:

- implemented
- pytest passed
- scenario execution passed
- result CSV generation confirmed

## Phase 2: GitHub Repository

Goal:

Publish the mini SILS(Software-in-the-Loop Simulation) PoC(Proof of Concept) to a personal GitHub repository.

Planned tasks:

- create personal GitHub repository
- push local main branch
- confirm repository structure on GitHub
- avoid uploading generated result files and private documents

## Phase 3: GitHub Actions CI

Goal:

Run pytest automatically with GitHub Actions CI(Continuous Integration).

Planned tasks:

- add GitHub Actions workflow
- run pytest on push
- confirm CI result
- keep CI configuration simple

## Phase 4: C/C++ Control Logic

Goal:

Add C/C++ implementation of the same fan control logic.

Planned tasks:

- implement fan control logic in C/C++
- add C/C++ unit tests
- compare Python and C/C++ behavior

## Phase 5: Static Analysis and SBOM

Goal:

Add basic quality and traceability activities.

Planned tasks:

- add Python static checks
- add C/C++ static analysis
- generate SBOM(Software Bill of Materials)
- keep outputs as CI(Continuous Integration) artifacts where appropriate

## Phase 6: AWS Execution

Goal:

Run the same mini SILS(Software-in-the-Loop Simulation) on AWS(Amazon Web Services), especially Amazon EC2(Elastic Compute Cloud).

Planned tasks:

- confirm AWS free tier and cost control
- launch minimal Amazon EC2(Elastic Compute Cloud) environment
- run Python mini SILS(Software-in-the-Loop Simulation)
- stop or terminate resources after use

## Phase 7: HILS Expansion

Goal:

Use the same fictional scenarios as a base for future HILS(Hardware-in-the-Loop Simulation).

Candidate equipment:

- Raspberry Pi
- Arduino
- NXP S32K144EVB-Q100

Initial communication should prioritize USB serial or UART(Universal Asynchronous Receiver/Transmitter).

CAN(Controller Area Network) and LIN(Local Interconnect Network) are later topics.

## Phase 3 Result

GitHub Actions CI(Continuous Integration) has been added.

Confirmed results:

- pytest runs on GitHub Actions
- mini SILS(Software-in-the-Loop Simulation) runs on GitHub Actions
- result CSV(Comma-Separated Values) files are uploaded as artifacts
- README.md shows the CI(Continuous Integration) status badge

This phase confirms that the Python-only mini SILS(Software-in-the-Loop Simulation) can be reproduced in a clean CI(Continuous Integration) environment.

## Phase 4 Result (Initial)

A minimal C++ implementation of the fictional fan control logic has been added.

Confirmed results:

- local C++ build succeeded
- fan_control.cpp execution succeeded
- GoogleTest unit tests passed
- UT-01 to UT-10 were implemented in C++

This phase confirms that the same control specification can be implemented both in Python and in C++.

## Phase 4 Result (CMake and CTest)

CMake-based local C++ build and CTest execution have been added.

Confirmed results:

- CMake configure succeeded
- CMake build succeeded
- fan_control_main execution succeeded
- GoogleTest execution succeeded
- CTest execution succeeded

This phase confirms that the same control specification can be implemented, built, and tested in both Python and C++.
