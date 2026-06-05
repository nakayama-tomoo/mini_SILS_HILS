# ADR-003: Scenario Suite Version ID

## Status

Accepted for Mini-SILS-HILS PoC restructuring.

## Context

The Mini-SILS-HILS PoC uses a shared scenario suite:

    common/scenario/scenario_suite.yaml

The same scenario data is intended to be reused across:

    python_sils
    cpp_sils
    mini_hils

A new scenario file exists for fan control v2 validation:

    common/scenario/fan_control/sc_05_v2_threshold_validation.csv

However, the current scenario suite does not explicitly represent which fan control version should be used for each scenario.

This creates ambiguity when adding scenarios that are intended for a specific control version.

## Decision

Add an optional `version_id` field to each scenario entry in:

    common/scenario/scenario_suite.yaml

For existing scenarios, use:

    version_id: fan_control_v1

For the v2 validation scenario, use:

    version_id: fan_control_v2

The initial migration should be phased.

Phase 3-A:

    Add version_id to existing SC_01 through SC_04.
    Do not add SC_05 to the suite yet.

Phase 3-B:

    Update tools/run_suite.py to handle version_id explicitly.
    Update environment target handling if required.

Phase 3-C:

    Add SC_05 to scenario_suite.yaml after version-aware execution is confirmed.

## Consequences

Positive consequences:

- The scenario suite can explicitly express which control version should be used.
- SC_05 can be added without ambiguity.
- Future comparison between v1 and v2 behavior becomes easier.
- Traceability between scenario, version, result, and evidence becomes clearer.

Trade-offs:

- Existing tools must be updated to read version_id.
- C++ SILS may need separate handling if it does not support version switching.
- Reports and comparison tools may need schema updates when SC_05 is added.

## Scope

This decision applies only to the personal Mini-SILS-HILS PoC.

It does not define a company or customer-specific verification process.
