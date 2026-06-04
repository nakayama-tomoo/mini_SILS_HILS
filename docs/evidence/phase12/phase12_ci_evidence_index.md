# Phase 12 CI Evidence Index

## Phase summary

| Item | Value |
|---|---|
| Phase | Phase 12 |
| Theme | CI evidence organization and static analysis preparation |
| Branch | `phase12-ci-evidence-static-analysis-prep` |
| Final CI green commit | `595fc2d0da748fb4f3e611ac839ebd4b43b6d4c7` |
| Final tag | `checkpoint-after-phase12-ci-evidence-static-analysis-prep-20260604` |
| Final CI result | `passed` |
| Final CI run URL | Recorded in `Phase 12 CI execution result` section below. |

## Evidence target

Phase 12 checks the following:

1. Existing CI(Continuous Integration) workflow responsibilities are documented.
2. `python-test.yml` and `cpp-sils-ci.yml` responsibilities are separated.
3. CI artifact naming and evidence structure are defined.
4. C++ static analysis candidates are selected.
5. Python static analysis candidates are selected.

## Workflow evidence

| Workflow | Expected result | Artifact name | Notes |
|---|---|---|---|
| `python-test.yml` | `passed` | `phase12-python-sils-evidence-${{ github.run_id }}-${{ github.run_attempt }}` | Python SILS pytest, governance, Docker execution, and Python-side evidence |
| `cpp-sils-ci.yml` | `passed` | `phase12-cpp-sils-evidence-${{ github.run_id }}-${{ github.run_attempt }}` | C++ build, CTest, scenario execution, Python/C++ comparison, and C++-side evidence |
| `cpp-sils-ci.yml` comparison step | `passed` | Included in `phase12-cpp-sils-evidence-${{ github.run_id }}-${{ github.run_attempt }}` | Python/C++ behavior comparison |

## Scenario evidence

| Scenario | Python result | C++ result | Comparison result | Notes |
|---|---|---|---|---|
| SC_01 | `passed` | `passed` | `matched` | Verified by C++ SILS CI suite and Python/C++ comparison |
| SC_02 | `passed` | `passed` | `matched` | Verified by C++ SILS CI suite and Python/C++ comparison |
| SC_03 | `passed` | `passed` | `matched` | Verified by C++ SILS CI suite and Python/C++ comparison |
| SC_04 | `passed` | `passed` | `matched` | Verified by C++ SILS CI suite and Python/C++ comparison |
| SC_05 | `passed` | `passed` | `matched` | Verified by C++ SILS CI suite and Python/C++ comparison |

## Static analysis preparation result

| Language | First candidate | Second candidate | Phase 12 decision |
|---|---|---|---|
| C++ | Cppcheck | clang-tidy | Candidate selection only. No quality gate in Phase 12. |
| Python | Ruff | mypy | Candidate selection only. No quality gate in Phase 12. |

## Final judgement

## Phase 12 CI execution result

Status: Passed

Branch: phase12-ci-evidence-static-analysis-prep

Final CI commit:
- short hash: 595fc2d
- full hash: 595fc2d0da748fb4f3e611ac839ebd4b43b6d4c7

GitHub Actions results:
- Python side workflow: passed
  - run URL: https://github.com/nakayama-tomoo/mini_SILS_HILS/actions/runs/26946503960
  - artifact: phase12-python-sils-evidence-26946503960-1
- C++ SILS CI: passed
  - run URL: https://github.com/nakayama-tomoo/mini_SILS_HILS/actions/runs/26944534742
  - artifact: phase12-cpp-sils-evidence-26944534742-1

Phase 12 evidence policy confirmed:
- Python SILS CI is responsible for Python pytest, governance checks, Docker execution, and Python-side evidence.
- C++ SILS CI is responsible for C++ build, CTest, suite execution, Python/C++ comparison, and C++-side evidence.
- C++ generated CSV/JSON evidence files are collected when available, but missing optional result files do not fail the CI.
- Functional quality gates remain CMake build, CTest, suite execution, and Python/C++ comparison.
- Static analysis tools are not introduced as CI gates in Phase 12.
