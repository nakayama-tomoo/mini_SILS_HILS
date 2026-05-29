```text
.
├── .github
│   └── workflows
│       └── python-test.yml
├── .gitignore
├── common
│   ├── comparison
│   │   └── compare_results.py
│   ├── expected
│   ├── README.md
│   └── scenario
│       ├── fan_control
│       │   ├── sc_01_traffic_warmup_cooldown.csv
│       │   ├── sc_02_around_95deg_fluctuation.csv
│       │   ├── sc_03_rapid_heatup_recovery.csv
│       │   └── sc_04_high_temp_oscillation.csv
│       └── scenario_suite.yaml
├── docs
│   ├── evidence_governance_phase3.md
│   ├── sbom_minimum_policy_phase4.md
│   └── tree_mini_sils_hils_poc_full.md
├── environments
│   ├── arduino_hils.json
│   ├── cpp_sils.json
│   └── python_sils.json
├── evidence
│   ├── dependencies
│   │   ├── python_freeze.txt
│   │   └── README.md
│   ├── evidence_manifest.json
│   └── sbom
│       └── python_environment_sbom.json
├── implementations
│   └── python_sils
│       ├── .dockerignore
│       ├── .github
│       │   └── workflows
│       │       └── python-test.yml
│       ├── .gitignore
│       ├── cpp
│       │   ├── CMakeLists.txt
│       │   ├── include
│       │   │   └── fan_control.hpp
│       │   ├── main
│       │   ├── README.md
│       │   ├── results
│       │   │   ├── .gitkeep
│       │   │   ├── sc_01_traffic_warmup_cooldown_cpp_results.csv
│       │   │   ├── sc_02_around_95deg_fluctuation_cpp_results.csv
│       │   │   ├── sc_03_rapid_heatup_recovery_cpp_results.csv
│       │   │   └── sc_04_high_temp_oscillation_cpp_results.csv
│       │   ├── scenarios
│       │   │   └── run_scenario.cpp
│       │   ├── src
│       │   │   ├── fan_control.cpp
│       │   │   └── main.cpp
│       │   ├── test_fan_control
│       │   └── tests
│       │       └── test_fan_control.cpp
│       ├── docker
│       │   ├── Dockerfile
│       │   └── README.md
│       ├── docs
│       │   ├── ci_evidence.md
│       │   ├── environment.md
│       │   ├── roadmap.md
│       │   ├── scope.md
│       │   └── specs
│       │       └── fan_control_sils_spec.md
│       ├── pyproject.toml
│       ├── README.md
│       ├── results
│       │   ├── .gitkeep
│       │   ├── comparison_summary.json
│       │   └── fan_control
│       │       ├── sc_01_traffic_warmup_cooldown_results.csv
│       │       ├── sc_01_traffic_warmup_cooldown_results.json
│       │       ├── sc_02_around_95deg_fluctuation_results.csv
│       │       ├── sc_02_around_95deg_fluctuation_results.json
│       │       ├── sc_03_rapid_heatup_recovery_results.csv
│       │       ├── sc_03_rapid_heatup_recovery_results.json
│       │       ├── sc_04_high_temp_oscillation_results.csv
│       │       └── sc_04_high_temp_oscillation_results.json
│       ├── scenarios
│       │   └── fan_control
│       │       ├── sc_01_traffic_warmup_cooldown.csv
│       │       ├── sc_02_around_95deg_fluctuation.csv
│       │       ├── sc_03_rapid_heatup_recovery.csv
│       │       ├── sc_04_high_temp_oscillation.csv
│       │       └── sc_05_v2_threshold_validation.csv
│       ├── scripts
│       │   └── run_fan_control_sils.py
│       ├── src
│       │   └── mini_sils
│       │       ├── __init__.py
│       │       ├── fan_control.py
│       │       ├── result_writer.py
│       │       ├── scenario_runner.py
│       │       └── version_loader.py
│       ├── tests
│       │   ├── __init__.py
│       │   ├── test_fan_control.py
│       │   └── test_scenario_runner.py
│       └── tools
│           └── compare_results.py
├── pyproject.toml
├── requirements
│   ├── REQ-FAN-001.md
│   ├── REQ-FAN-002.md
│   └── REQ-FAN-003.md
├── requirements-dev.txt
├── requirements.txt
├── results
│   ├── all_results_summary.json
│   ├── comparison_summary.json
│   ├── hils
│   │   └── hils_summary.json
│   ├── suite_summary.json
│   └── verification_report.md
├── tools
│   ├── check_coverage.py
│   ├── check_evidence_manifest.py
│   ├── check_traceability.py
│   ├── compare_all_results.py
│   ├── compare_python_cpp_results.py
│   ├── generate_coverage_matrix.py
│   ├── generate_evidence_manifest.py
│   ├── generate_verification_report.py
│   ├── generate_version_matrix.py
│   ├── load_scenario_suite.py
│   ├── run_governance_checks.py
│   ├── run_suite.py
│   └── run_v2_validation.py
├── traceability
│   ├── coverage_matrix.json
│   ├── evidence_mapping.json
│   ├── scenario_traceability.json
│   └── version_compatibility_matrix.json
└── versions
    ├── fan_control_v1.json
    └── fan_control_v2.json

41 directories, 100 files
```
