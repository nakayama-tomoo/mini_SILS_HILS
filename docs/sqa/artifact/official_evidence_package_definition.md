# Official Evidence Package Definition

## Purpose

Define the minimum evidence package retained by CI and uploaded to AWS S3.

## Required Evidence

### Verification

- verification_report.md

### Traceability

- coverage_matrix.json

### Evidence Management

- evidence_manifest.json

### SILS Comparison

- comparison_summary.json

### Execution Metadata

- metadata.json

## Future Candidates

- SBOM
- Static Analysis Reports
- HILS Results

## Ownership

Python SILS CI:
- evidence_manifest.json
- coverage_matrix.json

C++ SILS CI:
- comparison_summary.json

Future Evidence Workflow:
- verification_report.md

AWS Upload Workflow:
- store approved evidence package

