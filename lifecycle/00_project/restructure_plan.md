# Mini-SILS-HILS Restructuring Plan

## Purpose

This restructuring changes the Mini-SILS-HILS PoC from an implementation-centered structure to a lifecycle-aware evaluation architecture.

The target architecture supports:

- requirements analysis
- design
- implementation
- evaluation
- verification
- validation
- traceability
- evidence management

## Main Architecture Direction

The evaluator selects the following combination.

    Evaluation Package + Environment

The system absorbs environment-specific differences through the following structure.

    Environment Definition + Adapter

## Priority Items

### 1. Unify Environment IDs

Use the following upper-level environment IDs.

    python_sils
    cpp_sils
    mini_hils

### 2. Treat arduino_hils as an Implementation Name

`arduino_hils` should be treated as the implementation name.

Upper-level evaluation should use `mini_hils`.

    environment_id: mini_hils
    implementation: arduino_hils

### 3. Make common/scenario the Canonical Scenario Source

The canonical scenario source should be:

    common/scenario/

Implementation-specific directories should not own independent scenario master files.

### 4. Add Common Evaluation Assets

Add the following directories.

    common/signals/
    common/expected/
    common/judge/
    common/evaluation_package/

These directories define shared evaluation assets independent from Python SILS, C++ SILS, and mini HILS.

### 5. Explicitly Model HILS UART Differences as Adapter Behavior

HILS uses UART(Universal Asynchronous Receiver/Transmitter), while SILS may use CSV and JSON files directly.

This difference should be hidden behind adapters.

    CSV scenario
      -> input adapter
      -> UART
      -> DUT(Device Under Test)
      -> UART
      -> output adapter
      -> normalized JSON result

### 6. Split Results

Split results into the following directories.

    results/raw/
    results/normalized/
    results/comparison/
    results/reports/

### 7. Add Lifecycle Work Products

Add lifecycle work products for:

- requirements analysis
- design
- implementation mapping
- evaluation
- verification
- validation

## Safety Policy

This is a personal PoC.

Do not use:

- company data
- customer data
- real vehicle data
- confidential documents
- customer-specific requirements
- company project source code
- actual ECU logs
- real vehicle connection

For hardware work:

- do not connect Raspberry Pi GPIO to 5V signals directly
- do not use unsafe external power wiring
- do not control high-current loads
- do not connect to real vehicles or company equipment

## Work Phases

### Phase 0: Backup

- Commit current state.
- Create a Git tag.
- Create a full repository backup using rsync.
- Create folder-level snapshots for major directories.

### Phase 1: Additive Restructuring

Add new folders and metadata files without deleting existing assets.

### Phase 2: Tool Compatibility Check

Run applicable checks.

    python3 -m pytest
    python3 tools/run_suite.py
    python3 tools/compare_all_results.py
    python3 tools/generate_verification_report.py

Use only applicable commands if some tools are not available or not yet connected.

### Phase 3: Move Implementation Folders

Move C++ SILS to the following directory.

    implementations/cpp_sils/

Current source candidate:

    implementations/python_sils/cpp/

Use `git mv` when moving tracked files.

### Phase 4: Canonical Scenario Cleanup

Make the following directory the canonical scenario source.

    common/scenario/

Remove duplicated scenario copies only after tools are updated and tests pass.

### Phase 5: Report and Evidence Cleanup

Align verification reports, evidence manifests, and traceability files with the new structure.

## Recommended Execution Order

Use the following order.

    0. Back up the current repository.
    1. Create a restructuring branch.
    2. Add ADR-001.
    3. Add restructure_plan.md.
    4. Add lifecycle directories.
    5. Add common/signals, common/expected, common/judge, and common/evaluation_package.
    6. Add environments/mini_hils.json.
    7. Add results/raw, results/normalized, results/comparison, and results/reports.
    8. Run tests and existing tools.
    9. Move C++ SILS.
    10. Make common/scenario the canonical scenario source.
    11. Remove duplicated files after confirmation.

## Important Rule

Do not delete files at the beginning.

Use this order.

    Add
    Check
    Run tests
    Move
    Check again
    Delete at the end

