# mini-sils-poc

![Python mini SILS CI](https://github.com/nakayama-tomoo/mini-sils-poc/actions/workflows/python-test.yml/badge.svg?branch=main)


This repository is a personal PoC(Proof of Concept) for building a small SILS(Software-in-the-Loop Simulation) environment using fictional and generalized data only.

The first target is a simplified electric radiator fan control logic.

## Target Function

The target function controls a fictional electric radiator fan based on coolant temperature.

Input:

- coolant_temp_c
- previous fan state

Output:

- OFF
- LOW
- HIGH

## Data Policy

This repository does not use company confidential information, customer information, real project information, real vehicle data, real ECU(Electronic Control Unit) data, or real CAN(Controller Area Network) logs.

All scenarios, inputs, expected results, and test cases are fictional.

## Run Tests

Run:

pytest

## Run SILS(Software-in-the-Loop Simulation)

Run:

python scripts/run_fan_control_sils.py

## Current Status

- Python fan control logic implemented
- Unit tests implemented
- Scenario CSV(Comma-Separated Values) tests implemented
- Result CSV(Comma-Separated Values) generation implemented
