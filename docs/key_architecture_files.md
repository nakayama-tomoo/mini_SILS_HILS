## common/scenario/scenario_suite.yaml
```yaml
suite_name: fan_control_suite

description: >
  Shared scenario suite for:
  - Python SILS(Software-in-the-Loop Simulation)
  - C++ SILS(Software-in-the-Loop Simulation)
  - mini HILS(Hardware-in-the-Loop Simulation)

owner: Mini_SILS_HILS_Construction

scenarios:
  - id: SC_01
    description: traffic warmup cooldown
    category: normal
    file: fan_control/sc_01_traffic_warmup_cooldown.csv

    targets:
      - python_sils
      - cpp_sils
      - mini_hils

  - id: SC_02
    description: around 95deg fluctuation
    category: boundary
    file: fan_control/sc_02_around_95deg_fluctuation.csv

    targets:
      - python_sils
      - cpp_sils
      - mini_hils

  - id: SC_03
    description: rapid heatup recovery
    category: stress
    file: fan_control/sc_03_rapid_heatup_recovery.csv

    targets:
      - python_sils
      - cpp_sils
      - mini_hils

  - id: SC_04
    description: high temperature oscillation
    category: oscillation
    file: fan_control/sc_04_high_temp_oscillation.csv

    targets:
      - python_sils
      - cpp_sils
      - mini_hils
```

## environments/python_sils.json
```json
{
  "environment_id": "PYTHON_SILS",

  "type": "SILS",

  "implementation": "python_sils",

  "execution_model": {
    "logical_time": true,
    "realtime": false
  },

  "interfaces": {
    "input": "CSV",
    "output": "JSON"
  },

  "platform": {
    "language": "Python",
    "runtime": "CPython"
  }
}
```

## environments/cpp_sils.json
```json
{
  "environment_id": "CPP_SILS",

  "type": "SILS",

  "implementation": "cpp_sils",

  "execution_model": {
    "logical_time": true,
    "realtime": false
  },

  "interfaces": {
    "input": "CSV",
    "output": "JSON"
  },

  "platform": {
    "language": "C++",
    "runtime": "native"
  }
}
```

## environments/arduino_hils.json
```json
{
  "environment_id": "ARDUINO_HILS",

  "type": "HILS",

  "implementation": "arduino_hils",

  "execution_model": {
    "logical_time": false,
    "realtime": true
  },

  "interfaces": {
    "input": "UART",
    "output": "UART"
  },

  "platform": {
    "host": "Raspberry Pi 5",
    "dut": "Arduino UNO"
  }
}
```

## results/verification_report.md
```markdown
# Verification Report

## Overall Result

PASS

## Scenario Results

| Scenario | Python/C++ | HILS | Overall |
|---|---|---|---|
| sc_01_traffic_warmup_cooldown | MATCH | PASS | MATCH |
| sc_02_around_95deg_fluctuation | MATCH | PASS | MATCH |
| sc_03_rapid_heatup_recovery | MATCH | PASS | MATCH |
| sc_04_high_temp_oscillation | MATCH | PASS | MATCH |

## Generated Artifacts

- suite_summary.json
- comparison_summary.json
- all_results_summary.json
- verification_report.md```
