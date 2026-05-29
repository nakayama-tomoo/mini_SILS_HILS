# ADR-001: Evaluation Package + Environment + Adapter Architecture

## Status

Accepted for Mini-SILS-HILS PoC restructuring.

## Context

The Mini-SILS-HILS PoC currently contains useful assets for:

- Python SILS(Software-in-the-Loop Simulation)
- C++ SILS(Software-in-the-Loop Simulation)
- mini HILS(Hardware-in-the-Loop Simulation)
- scenario execution
- result comparison
- evidence generation
- traceability
- SBOM(Software Bill of Materials)

However, the current folder structure still has several risks.

Environment IDs are not fully unified.

    python_sils
    cpp_sils
    mini_hils
    arduino_hils
    ARDUINO_HILS

Arduino HILS implementation details may leak into upper-level evaluation logic.

Scenario files exist in multiple locations, which may cause divergence.

Expected behavior, signal definitions, and judge rules are not yet clearly separated as common evaluation assets.

HILS uses UART(Universal Asynchronous Receiver/Transmitter), while SILS uses CSV/JSON-style files. This difference should be handled by Adapter logic.

Result files need to be separated into raw results, normalized results, comparison results, and reports.

## Decision

Adopt the following architecture for the Mini-SILS-HILS PoC.

    Evaluation Package
      + Environment
      + Adapter
      + Common Scenario / Signal / Expected / Judge Assets
      + Normalized Results
      + Evidence

The evaluator should select the following two items.

    1. Evaluation Package
    2. Environment

The differences between Python SILS, C++ SILS, mini HILS, and future vehicle evaluation shall be hidden behind environment definitions and adapters.

## Environment Naming Policy

Use lower snake_case environment IDs at the upper level.

    python_sils
    cpp_sils
    mini_hils

Use implementation names for lower-level details.

    arduino_hils

Therefore, mini HILS should be represented as follows.

    environment_id: mini_hils
    implementation: arduino_hils

This means that Arduino is treated as one implementation of mini HILS, not as the upper-level evaluation environment name.

## Common Asset Policy

The following assets shall be treated as common evaluation assets.

    common/scenario/
    common/signals/
    common/expected/
    common/judge/
    common/evaluation_package/

The `common/scenario/` directory shall be treated as the canonical scenario source.

Implementation-specific directories should not own separate scenario master files.

## Adapter Policy

SILS environments may directly consume CSV scenario files and produce JSON results.

HILS environments may require physical interfaces such as UART.

Therefore, HILS-specific differences shall be represented by adapters.

    CSV scenario
      -> input adapter
      -> UART
      -> DUT(Device Under Test)
      -> UART
      -> output adapter
      -> normalized JSON result

## Result Management Policy

Results shall be separated into the following directories.

    results/raw/
    results/normalized/
    results/comparison/
    results/reports/

Raw results preserve environment-specific outputs.

Normalized results provide common comparison-ready data.

Comparison results and reports are generated from normalized results.

## Relationship to Lifecycle Work Products

This decision supports the following lifecycle structure.

### Requirements Analysis

Define why shared scenarios and environment switching are needed.

### Design

Define Evaluation Package, Environment, Adapter, Signal Dictionary, Judge Rules, and Result Model.

### Implementation

Implement Python SILS, C++ SILS, and mini HILS as replaceable targets.

### Evaluation

Execute scenarios and collect raw and normalized results.

### Verification

Check whether requirements are satisfied using test results and evidence.

### Validation

Check whether the PoC is suitable for personal learning, SQA(Software Quality Assurance) understanding, HILS expansion, and future AWS(Amazon Web Services) execution.

## Consequences

Positive consequences:

- The same scenarios can be reused across Python SILS, C++ SILS, and mini HILS.
- Environment-specific differences are isolated.
- HILS implementation details do not leak into upper-level evaluation logic.
- Traceability from requirements to scenarios, results, and evidence becomes easier.
- The PoC becomes easier to explain as an evaluation architecture set, not just a sample SILS/HILS implementation.

Trade-offs:

- More metadata files are required.
- Tools such as `run_suite.py` may need to be updated to read environment definitions and evaluation packages.
- Existing paths may need migration.
- A phased restructuring is required to avoid breaking current tests and CI(Continuous Integration).

## Scope Constraints

This decision applies only to the personal Mini-SILS-HILS PoC.

Out of scope:

- company confidential information
- customer information
- real vehicle data
- real ECU(Electronic Control Unit) data
- company project artifacts
- customer-specific requirements
- safety-critical physical load testing
- direct connection to real vehicles or company equipment

## Migration Priority

The restructuring should proceed in the following order.

    1. Back up the current repository.
    2. Create a restructuring branch.
    3. Add lifecycle and architecture decision documents.
    4. Add common/signals, common/expected, common/judge, and common/evaluation_package.
    5. Add environments/mini_hils.json.
    6. Add environment capability matrix.
    7. Split results into raw, normalized, comparison, and reports.
    8. Move C++ SILS from implementations/python_sils/cpp to implementations/cpp_sils.
    9. Make common/scenario the canonical scenario source.
    10. Clean up duplicated or nested workflow directories after tests pass.

