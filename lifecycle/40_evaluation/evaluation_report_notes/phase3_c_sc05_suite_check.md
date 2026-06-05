# Phase 3-C SC_05 Scenario Suite Check

## Purpose

This note records Phase 3-C, which adds SC_05 to the common scenario suite.

## Context

SC_05 is a fan_control_v2 validation scenario.

The scenario file is:

    common/scenario/fan_control/sc_05_v2_threshold_validation.csv

Phase 3-A introduced version_id metadata.

Phase 3-B updated the suite runner to handle version_id and targets.

## Change Applied

The following scenario was added to:

    common/scenario/scenario_suite.yaml

Scenario:

    SC_05

Version:

    fan_control_v2

Targets:

    python_sils

## Reason

SC_05 is initially limited to python_sils because C++ SILS version switching for fan_control_v2 is not yet confirmed.

C++ SILS can be added later after version-aware C++ execution is supported.

## Expected Behavior

tools/run_suite.py should execute SC_05 using:

    python_sils

and skip:

    cpp_sils

because cpp_sils is not listed in the SC_05 targets.

## Follow-up

Later phases may update comparison and verification report generation so that SC_05 appears explicitly in integrated comparison and verification reports.

## Correction

During Phase 3-C, SC_05 was accidentally appended twice to:

    common/scenario/scenario_suite.yaml

The duplicate SC_05 entry was removed.

After correction, the scenario suite contains:

    SC_01
    SC_02
    SC_03
    SC_04
    SC_05

SC_05 appears only once.

Expected corrected suite summary:

    total_scenarios: 5
    passed_scenarios: 5
    failed_scenarios: 0
    overall: PASS
