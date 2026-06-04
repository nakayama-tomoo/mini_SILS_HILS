# CI Workflow Responsibility

## Purpose

This document defines the responsibility split between existing GitHub Actions workflows in Phase 12.

The goal is not to add more checks blindly. The goal is to make each CI(Continuous Integration) workflow answer one clear question:

- Does the Python SILS(Software-in-the-Loop Simulation) reference behavior still work?
- Does the C++ SILS build, test, and match the Python reference behavior?
- Are CI artifacts usable as lightweight SQA(Software Quality Assurance) evidence?

## Workflow responsibility table

| Workflow | Primary responsibility | Quality gate | Evidence artifact | Out of scope |
|---|---|---|---|---|
| `python-test.yml` | Validate Python SILS reference implementation | Python tests and Python scenario checks | pytest result, Python scenario result, tool versions, metadata | C++ build, CTest, Python/C++ comparison, static analysis |
| `cpp-sils-ci.yml` | Validate C++ SILS build/test and Python/C++ equivalence | CMake build, CTest, SC_01 to SC_05 suite, Python/C++ comparison | CTest result, C++ scenario result, Python/C++ comparison result, tool versions, metadata | Python lint, Python type check, C++ static analysis |
| future `static-analysis.yml` | Report code maintainability and potential bug findings | Phase 13: report-only; later phase: partial gate | Cppcheck, clang-tidy, Ruff, mypy reports | SILS functional tests, HILS(Hardware-in-the-Loop Simulation) connection |

## `python-test.yml`

### Purpose

`python-test.yml` keeps the Python SILS implementation usable as the reference behavior for the mini SILS project.

### Expected checks

- Install Python dependencies.
- Run Python unit tests.
- Run Python scenario tests if available.
- Store Python-side test evidence as artifact.

### Expected failure meaning

If `python-test.yml` fails, the likely problem is in one of these areas:

- Python SILS implementation
- Python tests
- Python scenario runner
- Python dependency or environment setup

### Not responsible for

- CMake configure/build
- CTest execution
- C++ executable behavior
- Python/C++ comparison
- Static analysis

## `cpp-sils-ci.yml`

### Purpose

`cpp-sils-ci.yml` checks that the C++ SILS implementation can be built, tested, and compared against the Python reference behavior.

### Expected checks

- Configure CMake.
- Build C++ SILS.
- Run CTest.
- Run SC_01 to SC_05 suite for C++ SILS if available.
- Run Python/C++ comparison.
- Store C++ and comparison evidence as artifact.

### Expected failure meaning

| Failing step | Meaning |
|---|---|
| CMake configure | Build definition or dependency issue |
| CMake build | C++ compile/link issue |
| CTest | C++ unit or integration test issue |
| SC_01 to SC_05 suite | C++ scenario behavior issue |
| Python/C++ comparison | C++ behavior differs from Python reference behavior |

### Not responsible for

- Python lint
- Python static type checking
- C++ static analysis
- HILS(Hardware-in-the-Loop Simulation) execution

## Python/C++ comparison ownership

Python/C++ comparison belongs to `cpp-sils-ci.yml`.

Reason:

The comparison answers whether the C++ implementation matches the already-tested Python reference behavior. Therefore, it is part of C++ SILS acceptance, not Python reference validation.

## Phase 12 policy

Static analysis is not a blocking quality gate in Phase 12.

Phase 12 prepares the evidence structure and selects candidate tools. Actual static analysis execution should be introduced later as report-only first.
