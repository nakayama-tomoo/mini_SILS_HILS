# Phase 3 Evidence and Governance Summary

## Purpose

This document summarizes the current Evidence and Governance structure of the mini SILS/HILS PoC.

The purpose of Phase 3 was not only to execute tests, but also to make the evidence structure visible, reproducible, and checkable by CI.

Current flow:

Requirement
→ Scenario
→ Execution Result
→ Evidence
→ Evidence Manifest
→ Governance Check
→ CI Result
→ GitHub Actions Artifact

## Scope

This activity is a personal PoC.

It does not use company information, customer information, real vehicle data, real ECU data, internal documents, or project-specific confidential data.

All requirements, scenarios, test data, and evidence files are based on fictional and general-purpose examples.

## Phase 3-A: Python Dependency Evidence

Python dependency evidence was added as minimal environment evidence.

Stored files:

- evidence/dependencies/python_freeze.txt
- evidence/dependencies/README.md

Meaning:

- python_freeze.txt records the installed Python packages at the time of evidence generation.
- README.md records how to regenerate the dependency evidence.

This provides a minimal answer to:

Which Python dependency environment was used for this PoC?

## Phase 3-B: Evidence Manifest Connection

The dependency evidence is referenced from:

- evidence/evidence_manifest.json

The added structure is:

- dependency_evidence[]
  - files[]
    - path

Meaning:

The dependency evidence is no longer an isolated file. It is now connected to the main evidence manifest.

## Phase 3-C: GitHub Actions Artifact

The CI workflow uploads the evidence files as a GitHub Actions artifact.

Artifact name:

- evidence-package

The artifact includes evidence-related files such as:

- evidence/
- results/
- traceability/
- environments/

Meaning:

Each CI run can keep the evidence package generated at that point in time.

This is a small but important step toward audit-ready evidence management.

## Phase 3-D: Evidence Manifest Governance Check

A new governance check script was added:

- tools/check_evidence_manifest.py

This script checks whether the files referenced by dependency_evidence[].files[].path actually exist.

The script is executed locally and in GitHub Actions.

Command:

- python tools/check_evidence_manifest.py

Expected result:

- [PASS] Evidence manifest references are valid.

## Checked Items

| Item | Failure condition |
| --- | --- |
| evidence/evidence_manifest.json | File does not exist |
| JSON syntax | JSON is invalid |
| dependency_evidence | Missing or not a list |
| dependency_evidence[].files | Missing or not a list |
| dependency_evidence[].files[].path | Missing, empty, or points to a non-existing file |

## Issues Detected During Implementation

During Phase 3-D, one important issue was found.

When the governance checks were executed, tools/generate_evidence_manifest.py regenerated evidence/evidence_manifest.json.

At first, this regeneration removed the manually added dependency_evidence section.

The issue was:

tools/run_governance_checks.py
→ tools/generate_evidence_manifest.py
→ evidence/evidence_manifest.json is regenerated
→ dependency_evidence is removed

To fix this, tools/generate_evidence_manifest.py was updated so that it generates dependency_evidence as part of the manifest.

As a result, the evidence manifest is now stable after regeneration.

## Current Governance Flow

Run governance checks:

- check_traceability.py
- generate_evidence_manifest.py
- generate_coverage_matrix.py
- check_coverage.py
- generate_version_matrix.py
- run_v2_validation.py

Check evidence manifest references:

- check_evidence_manifest.py

Validate evidence files:

- JSON syntax validation

Upload evidence package:

- GitHub Actions artifact: evidence-package

## Current Evidence/Governance Structure

- requirements/
  - Requirement definitions

- traceability/
  - scenario_traceability.json
  - coverage_matrix.json
  - version_compatibility_matrix.json

- results/
  - comparison_summary.json
  - hils/hils_summary.json

- evidence/
  - evidence_manifest.json
  - dependencies/python_freeze.txt
  - dependencies/README.md

- tools/
  - run_governance_checks.py
  - generate_evidence_manifest.py
  - check_evidence_manifest.py
  - generate_coverage_matrix.py
  - check_coverage.py
  - generate_version_matrix.py
  - run_v2_validation.py

- .github/workflows/
  - python-test.yml

## SQA Meaning

This Phase 3 structure allows the PoC to explain the following:

- Which requirement is being checked?
- Which scenario is linked to the requirement?
- Which execution result was generated?
- Which evidence files were created?
- Which dependency evidence was recorded?
- Are the evidence references still valid?
- Was the check executed by CI?
- Was the evidence package stored as an artifact?

This is still a small PoC, but it has moved from:

Tests pass

to:

Tests pass, evidence is generated, evidence references are checked, and CI stores the evidence package.

## Current Completion Status

| Phase | Status | Result |
| --- | --- | --- |
| Phase 3-A | Done | Python dependency evidence was created |
| Phase 3-B | Done | Dependency evidence was connected to evidence_manifest.json |
| Phase 3-C | Done | Evidence package is uploaded by GitHub Actions |
| Phase 3-D | Done | Evidence manifest references are checked by CI |

## Next Candidate

The natural next step is:

Phase 4: Minimal SBOM support

Possible direction:

python_freeze.txt
→ SBOM-like dependency evidence
→ SBOM file generation
→ SBOM reference from evidence_manifest.json
→ SBOM validation in CI

This should be done as a small incremental extension, not as a full enterprise-level SBOM process.
