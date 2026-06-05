# Verification Report

## Overall Result

PASS

## Scenario Results

| ID | Scenario | Version | Python SILS | C++ SILS | Python/C++ | mini HILS | Overall |
|---|---|---|---|---|---|---|---|
| SC_01 | sc_01_traffic_warmup_cooldown | fan_control_v1 | PASS | PASS | MATCH | PASS | PASS |
| SC_02 | sc_02_around_95deg_fluctuation | fan_control_v1 | PASS | PASS | MATCH | PASS | PASS |
| SC_03 | sc_03_rapid_heatup_recovery | fan_control_v1 | PASS | PASS | MATCH | PASS | PASS |
| SC_04 | sc_04_high_temp_oscillation | fan_control_v1 | PASS | PASS | MATCH | PASS | PASS |
| SC_05 | sc_05_v2_threshold_validation | fan_control_v2 | PASS | PASS | MATCH | SKIPPED | PASS |

## Notes

- `SKIPPED` means the scenario did not target that execution environment.
- SC_05 is a fan_control_v2 validation scenario executed by Python SILS and C++ SILS.
- C++ SILS fan_control_v2 support is implemented via version-aware C++ scenario execution.

## Generated Artifacts

- suite_summary.json
- comparison_summary.json
- all_results_summary.json
- verification_report.md
- reports/verification_report.md
