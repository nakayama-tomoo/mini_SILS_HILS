# Static Analysis Management Policy

## Purpose

This document defines how static analysis findings are managed in the Mini SILS/HILS PoC.

The goal is not to achieve zero findings.

The goal is to:

- understand findings
- classify findings
- make remediation decisions
- retain evidence

## Static Analysis Tools

Current tools:

- Ruff
- Cppcheck

Future tools may be added.

## Classification Categories

### Review Required

Definition:

Findings requiring design or implementation review before remediation.

Examples:

- Ruff E402

Action:

- Review before modification
- Document rationale

### Tool Configuration Issue

Definition:

Findings caused by tool configuration limitations.

Examples:

- missingInclude
- missingIncludeSystem

Action:

- Improve tool configuration when practical
- Do not treat as software defects

### Style Candidate

Definition:

Findings representing maintainability improvements.

Examples:

- useStlAlgorithm
- unusedFunction

Action:

- Fix when cost is reasonable
- Not CI blocking

### Informational

Definition:

Tool informational messages.

Examples:

- toomanyconfigs
- normalCheckLevelMaxBranches
- checkersReport

Action:

- Record only

## CI Gate Policy

Current policy:

- Static analysis findings are reported
- Static analysis findings do not fail CI

Future policy:

- Selected categories may become CI gate candidates

## Evidence Retention

Static analysis evidence shall be retained under:

artifacts/

Classification records shall be retained under:

docs/sqa/static-analysis/

## Change Management

Any remediation decision should be traceable through:

- Git commit
- Pull Request
- CI result
- Documentation

## Review Process

Static analysis findings should be reviewed during:

- Pull Request review
- Periodic quality review
- Release readiness review

## Baseline Concept

Existing findings may be accepted as a baseline.

New findings should be evaluated separately from baseline findings.

The objective is to prevent quality regression while allowing gradual improvement.


