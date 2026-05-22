# Fan Control Mini SILS Specification

## Overview

This document defines the first target function of the mini SILS(Software-in-the-Loop Simulation) PoC(Proof of Concept).

The target is a simplified electric radiator fan control logic using fictional and generalized data only.

This PoC(Proof of Concept) does not represent a real vehicle, real ECU(Electronic Control Unit), real thermal model, or real project specification.

## Purpose

The purpose is to understand the basic SILS(Software-in-the-Loop Simulation) workflow:

- input definition
- control decision
- expected result comparison
- PASS / FAIL judgment
- scenario execution
- result CSV(Comma-Separated Values) generation
- automated testing with pytest

## Target Function

The target function is a simplified electric radiator fan control.

Input:

- coolant_temp_c
- previous fan state

Output:

- fan state: OFF, LOW, or HIGH
- comparison result: PASS or FAIL

## Fan States

The fan state is one of the following:

- OFF
- LOW
- HIGH

The initial fan state is OFF.

## Control Rules

The next fan state is decided from the previous fan state and the current coolant temperature.

| Previous State | Condition | Next State |
|---|---|---|
| OFF | coolant_temp_c < 95 | OFF |
| OFF | 95 <= coolant_temp_c < 105 | LOW |
| OFF | 105 <= coolant_temp_c | HIGH |
| LOW | coolant_temp_c <= 90 | OFF |
| LOW | 90 < coolant_temp_c < 105 | LOW |
| LOW | 105 <= coolant_temp_c | HIGH |
| HIGH | coolant_temp_c <= 90 | OFF |
| HIGH | 90 < coolant_temp_c <= 100 | LOW |
| HIGH | 100 < coolant_temp_c | HIGH |

## Python Interface

The current Python implementation provides the following function:

- decide_fan_state(prev_fan_state, coolant_temp_c)

The function returns the next fan state.

## Scenario CSV Format

Scenario files are stored under:

- scenarios/fan_control/

The scenario CSV(Comma-Separated Values) format is:

| Column | Meaning |
|---|---|
| time_s | fictional time in seconds |
| coolant_temp_c | fictional coolant temperature |
| expected_fan_state | expected fan state |

## Result CSV Format

Result files are generated under:

- results/fan_control/

The result CSV(Comma-Separated Values) format is:

| Column | Meaning |
|---|---|
| time_s | fictional time in seconds |
| coolant_temp_c | fictional coolant temperature |
| expected_fan_state | expected fan state |
| actual_fan_state | actual fan state calculated by the control logic |
| match | PASS or FAIL |

## Unit Tests

The unit tests verify boundary values of the control logic.

The current test file is:

- tests/test_fan_control.py

## Scenario Tests

The scenario tests verify time-series fan state transitions using CSV(Comma-Separated Values) files.

The current test file is:

- tests/test_scenario_runner.py

## Acceptance Criteria

This PoC(Proof of Concept) is accepted when:

- all pytest tests pass
- scenario CSV(Comma-Separated Values) files can be executed
- result CSV(Comma-Separated Values) files are generated
- expected fan states and actual fan states can be compared
- the repository does not contain company confidential information, customer information, real project information, or real vehicle data

## Out of Scope

The following items are out of scope for the initial phase:

- real vehicle behavior
- real ECU(Electronic Control Unit) software
- real thermal model
- real CAN(Controller Area Network) logs
- HILS(Hardware-in-the-Loop Simulation)
- C/C++ implementation
- Docker execution
- AWS(Amazon Web Services)
- Amazon EC2(Elastic Compute Cloud)
- SBOM(Software Bill of Materials)
