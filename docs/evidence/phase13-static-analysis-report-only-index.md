# Phase 13 Evidence Index: Static Analysis Report Only

## Phase title

【進行中】 Mini SILS ④-E 静的解析report-only導入（Ruff / Cppcheck artifact証跡化）

## Purpose

This phase introduces report-only static analysis for the mini SILS project.

The purpose is to collect static analysis results as CI evidence without enabling quality gates.

## Scope

- Ruff report-only execution for Python code
- Cppcheck report-only execution for C/C++ code
- GitHub Actions artifact upload
- GitHub Actions Job Summary output
- Recording workflow run URL and artifact names

## Out of scope

- Quality gate
- Auto-fix
- Mandatory suppression policy
- MISRA compliance
- clang-tidy
- SBOM
- SQA audit automation
- mini-HILS connection

## Workflow

| Item | Value |
|---|---|
| Workflow file | `.github/workflows/static-analysis-report.yml` |
| Workflow name | `Static Analysis Report Only` |
| Gate status | Disabled |
| Trigger | push to main / pull_request / workflow_dispatch |

## Run record

| Item | Value |
|---|---|
| Date | TBD |
| Branch | TBD |
| Commit SHA | TBD |
| Workflow run URL | TBD |
| Trigger | TBD |

## Artifacts

| Tool | Artifact name | Main files | Result summary |
|---|---|---|---|
| Ruff | `phase13-ruff-static-analysis-report` | `ruff.json`, `ruff-github.txt`, `ruff-summary.md`, `ruff-version.txt` | TBD |
| Cppcheck | `phase13-cppcheck-static-analysis-report` | `cppcheck.xml`, `cppcheck.txt`, `cppcheck-summary.md`, `cppcheck-version.txt` | TBD |

## Gate status

| Tool | Gate enabled? | Notes |
|---|---:|---|
| Ruff | No | Findings are recorded only |
| Cppcheck | No | Findings are recorded only |

## Notes

- This phase records the initial static analysis evidence.
- Findings are not treated as CI failures.
- Rule tuning and suppression handling will be considered in later phases.
- Static analysis results will be used as a baseline candidate in the next phase.
