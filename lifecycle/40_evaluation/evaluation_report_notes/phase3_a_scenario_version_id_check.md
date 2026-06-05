# Phase 3-A Scenario Version ID Check

## Purpose

This note records the first step of Phase 3, which introduces version_id into the scenario suite.

## Context

A v2 validation scenario exists:

    common/scenario/fan_control/sc_05_v2_threshold_validation.csv

However, the scenario suite did not explicitly represent which fan control version should be used for each scenario.

## Change Applied

The following scenario suite file was updated:

    common/scenario/scenario_suite.yaml

Existing scenarios SC_01 through SC_04 now include:

    version_id: fan_control_v1

SC_05 was not added to the suite in Phase 3-A.

## Reason

SC_05 is intended for fan_control_v2 validation.

Before adding SC_05 to the common scenario suite, tools/run_suite.py should be updated to handle version_id and environment targets explicitly.

## Tool Change

tools/load_scenario_suite.py now displays:

    version_id

for each scenario entry.

## Expected Behavior

Existing suite behavior should remain unchanged because SC_01 through SC_04 still use fan_control_v1.

## Follow-up

Phase 3-B should update tools/run_suite.py to use version_id explicitly.

Phase 3-C should add SC_05 to scenario_suite.yaml after version-aware execution is confirmed.
