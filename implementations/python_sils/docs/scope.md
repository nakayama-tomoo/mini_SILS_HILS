# Scope

## Purpose

This document defines the scope of the mini SILS(Software-in-the-Loop Simulation) PoC(Proof of Concept).

The initial goal is to build a small, reproducible SILS(Software-in-the-Loop Simulation) environment on a personal PC using fictional and generalized data only.

## In Scope

The initial scope includes:

- Python-based control logic
- simplified electric radiator fan control
- fictional coolant temperature scenarios
- CSV(Comma-Separated Values) scenario input
- CSV(Comma-Separated Values) result output
- expected vs actual result comparison
- PASS / FAIL judgment
- pytest-based automated tests
- local execution on a personal Mac

## Out of Scope

The initial scope does not include:

- real vehicle data
- real ECU(Electronic Control Unit) software
- real project information
- company confidential information
- customer information
- real CAN(Controller Area Network) logs
- HILS(Hardware-in-the-Loop Simulation)
- Raspberry Pi execution
- Arduino execution
- NXP S32K144EVB-Q100 execution
- C/C++ implementation
- Docker execution
- GitHub Actions CI(Continuous Integration)
- AWS(Amazon Web Services)
- Amazon EC2(Elastic Compute Cloud)
- SBOM(Software Bill of Materials)

These may be considered in later phases using only public, fictional, and generalized data.

## Data Policy

All requirements, scenarios, inputs, expected results, logs, and outputs are fictional.

Do not use:

- company documents
- customer documents
- real project documents
- real test cases
- real defect reports
- real measurement logs
- real CAN(Controller Area Network) data
- real vehicle data

## Current Completion Criteria

The current phase is complete when:

- pytest passes
- SILS(Software-in-the-Loop Simulation) execution script runs successfully
- result CSV(Comma-Separated Values) files are generated
- Git repository is initialized
- initial commit is created
- README.md and docs files explain the purpose, scope, and execution method
