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
| Date | 2026-06-05 |
| Branch | phase13/static-analysis-report-only |
| Commit SHA | 43a723d |
| Workflow run URL | https://github.com/nakayama-tomoo/mini_SILS_HILS/actions/runs/27010591125 |
| Trigger | pull_request |
| Status | Success |

## Artifacts

| Tool | Artifact name | Main files | Result summary |
|---|---|---|---|
| Ruff | `phase13-ruff-static-analysis-report` | `ruff.json`, `ruff-github.txt`, `ruff-summary.md`, `ruff-version.txt`, `ruff-natural-exit-code.txt`, `ruff-report-only-exit-code.txt` | Report generated. Findings: 4. Natural exit code: 1. Report-only exit code: 0. Gate disabled. |
| Cppcheck | `phase13-cppcheck-static-analysis-report` | `cppcheck.xml`, `cppcheck.txt`, `cppcheck-summary.md`, `cppcheck-version.txt`, `cppcheck-targets.txt`, `cppcheck-xml-exit-code.txt`, `cppcheck-text-exit-code.txt` | Report generated. Findings: 6. Severity: style 6. XML/Text exit code: 0. Gate disabled. |

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
