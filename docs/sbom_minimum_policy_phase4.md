# Phase 4-A SBOM Minimum Policy

## Purpose

This document defines the minimum SBOM policy for Phase 4 of the mini SILS/HILS PoC.

SBOM means Software Bill of Materials.

The purpose of this phase is not to build a full enterprise-level SBOM process.

The purpose is to make Python dependency evidence easier to process by tools and easier to connect with future SQA audit automation.

## Background

In Phase 3, the PoC established a basic evidence and governance structure.

The current structure can explain:

- Which evidence files exist
- Which evidence files are referenced from evidence_manifest.json
- Whether referenced evidence files actually exist
- Whether CI can check the evidence structure
- Whether evidence files are stored as GitHub Actions artifacts

Phase 4 extends this structure by adding minimal SBOM-like evidence.

## Current Input Evidence

The current dependency evidence file is:

- evidence/dependencies/python_freeze.txt

This file records Python packages installed in the local or CI environment.

It is useful as human-readable dependency evidence.

However, it is not ideal for automated checking because it is plain text.

## Problem

The current dependency evidence answers:

Which Python packages were installed?

However, it does not yet clearly answer:

- Can dependency evidence be parsed as structured data?
- Can each dependency be handled as a component?
- Can the dependency evidence be referenced as a specific evidence type?
- Can future governance checks validate the dependency evidence format?
- Can future SQA automation compare dependency evidence between runs?

## Minimum Direction

In Phase 4, the PoC will create a minimal SBOM-like JSON file from python_freeze.txt.

The initial output file will be:

- evidence/sbom/python_sbom_minimal.json

The initial format will be a PoC-specific JSON format.

It is not intended to be full SPDX or CycloneDX compliance.

## Initial Minimal SBOM Structure

The first minimal SBOM JSON structure will be:

```json
{
  "schema_version": "0.1.0",
  "sbom_type": "python_dependency_minimal",
  "source": "evidence/dependencies/python_freeze.txt",
  "components": [
    {
      "name": "example-package",
      "version": "1.0.0"
    }
  ]
}
```

## Scope

In scope:

- Python dependencies recorded in evidence/dependencies/python_freeze.txt
- Minimal JSON generation
- Component name
- Component version
- Source evidence file path
- Future reference from evidence/evidence_manifest.json
- Future CI validation for file existence and JSON syntax

Out of scope for the initial phase:

- Full SPDX compliance
- Full CycloneDX compliance
- Vulnerability scanning
- License policy judgement
- License approval workflow
- Transitive dependency analysis beyond pip freeze output
- Package supplier verification
- Cryptographic signing
- Production-grade software supply chain compliance
- Company information
- Customer information
- Real vehicle data
- Real ECU data
- Internal documents
- Customer-specific requirements

## Initial Acceptance Criteria

Phase 4-A is complete when this policy document is committed to the repository.

Phase 4-B will be complete when:

- evidence/sbom/python_sbom_minimal.json is generated
- The file contains valid JSON
- The file contains a components array
- Each component has a name and version when the package line includes version information

Phase 4-C will be complete when:

- evidence/evidence_manifest.json references the SBOM evidence file

Phase 4-D will be complete when:

- CI checks that the SBOM file exists
- CI checks that the SBOM file is valid JSON
- CI checks that the SBOM reference in evidence_manifest.json is not broken

## Relationship with Existing Evidence

The relationship between existing dependency evidence and the minimal SBOM is:

```text
evidence/dependencies/python_freeze.txt
→ tools/generate_python_sbom_minimal.py
→ evidence/sbom/python_sbom_minimal.json
→ evidence/evidence_manifest.json
→ tools/check_evidence_manifest.py
→ GitHub Actions
→ evidence-package artifact
```

## SQA Meaning

From an SQA perspective, this phase changes dependency evidence from:

Plain text dependency record

to:

Structured dependency evidence that can be checked by tools

This is a small but important step toward future audit automation.

The PoC will be able to explain:

- Which dependency evidence was used as input
- Which SBOM-like evidence was generated
- Which components were recorded
- Whether the generated SBOM file exists
- Whether the generated SBOM file is valid JSON
- Whether the SBOM evidence is connected to the evidence manifest
- Whether CI checked the evidence structure

## Known Limitations

The minimal SBOM file will not fully describe the complete software supply chain.

Known limitations:

- It only reflects Python packages visible in python_freeze.txt
- It does not identify package suppliers
- It does not judge license acceptability
- It does not check vulnerabilities
- It does not include C/C++ compiler details
- It does not include OS packages
- It does not include GitHub Actions runner system libraries
- It does not include hardware firmware
- It does not prove that the dependencies are safe

These limitations are acceptable for the current personal PoC.

## Future Extension Candidates

Future phases may add:

- SPDX output
- CycloneDX output
- Vulnerability scan results
- License summary
- Dependency difference checks between CI runs
- SBOM reference from GitHub Releases
- SBOM comparison between SILS and HILS
- Integration with PR, CI result, test result, and evidence manifest
- SQA audit automation using structured evidence
