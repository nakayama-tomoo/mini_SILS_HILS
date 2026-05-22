# Development Environment

## Purpose

This document describes the development environment for the mini SILS(Software-in-the-Loop Simulation) PoC(Proof of Concept).

## Main Development Environment

The main development environment is a personal Mac.

The current local environment uses:

- macOS
- Python
- Python venv
- pytest
- Git
- local terminal
- personal Git repository

## Python Environment

The current Python environment is managed using venv.

Typical setup command:

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'

## Test Execution

Run unit tests and scenario tests with:

pytest

## SILS Execution

Run the mini SILS(Software-in-the-Loop Simulation) scenario execution with:

python scripts/run_fan_control_sils.py

## Git Ignore Policy

The following items are not tracked by Git:

- .venv/
- .pytest_cache/
- generated result CSV(Comma-Separated Values) files
- generated result JSON(JavaScript Object Notation) files
- local private documents

## Equipment Policy

Only personal equipment is used for this PoC(Proof of Concept).

Company-managed devices, customer-related devices, and business project assets are out of scope.

## Future Environment Candidates

The following may be considered in later phases:

- GitHub Actions for CI(Continuous Integration)
- C/C++ compiler
- CMake
- GoogleTest
- Docker
- AWS(Amazon Web Services)
- Amazon EC2(Elastic Compute Cloud)
- Raspberry Pi
- Arduino
- NXP S32K144EVB-Q100

These are not required for the current Python-only phase.
