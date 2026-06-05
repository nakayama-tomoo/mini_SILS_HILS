# Phase 3-B Version-Aware Runner Check

## Purpose

This note records Phase 3-B, which updates execution tools to handle scenario version_id metadata.

## Context

Phase 3-A added version_id metadata to:

    common/scenario/scenario_suite.yaml

Existing scenarios SC_01 through SC_04 use:

    version_id: fan_control_v1

SC_05 is still not added to the suite in Phase 3-B.

## Changes Applied

### Python SILS Runner

The following script now accepts:

    --version-id

Script:

    implementations/python_sils/scripts/run_fan_control_sils.py

The version_id is passed to:

    run_fan_control_scenario

### Suite Runner

The following tool now reads version_id and targets from scenario_suite.yaml:

    tools/run_suite.py

It passes version_id to Python SILS.

It executes C++ SILS only for:

    version_id: fan_control_v1

### V2 Validation Tool

The following tool now uses the canonical common scenario path:

    tools/run_v2_validation.py

The scenario path is:

    common/scenario/fan_control/sc_05_v2_threshold_validation.csv

## Expected Behavior

Existing SC_01 through SC_04 behavior should remain PASS.

SC_05 is not yet part of the scenario suite.

## Follow-up

Phase 3-C should add SC_05 to scenario_suite.yaml with:

    version_id: fan_control_v2

and initially target:

    python_sils

C++ SILS should be added to SC_05 only after C++ version switching is supported.
