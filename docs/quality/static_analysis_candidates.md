# Static Analysis Candidate Selection

## Purpose

This document selects static analysis candidates for future phases of the mini SILS(Software-in-the-Loop Simulation) project.

Phase 12 does not make static analysis a blocking quality gate. The first introduction should be report-only.

## Why static analysis is introduced after functional CI

Functional CI(Continuous Integration) answers:

- Does the code build?
- Do tests pass?
- Does C++ behavior match the Python reference?

Static analysis answers a different question:

- Is the code likely to contain maintainability issues, unsafe constructs, type mistakes, or latent defects that tests did not cover?

For this project, static analysis should complement tests. It should not replace tests or scenario comparison.

## C++ candidate tools

| Priority | Tool | Role | Phase 12 decision |
|---|---|---|---|
| 0 | Compiler warnings | Minimum build hygiene | Keep as a baseline; consider `-Wall -Wextra -Wpedantic` later |
| 1 | Cppcheck | Lightweight C/C++ static analysis, suitable for early embedded-style PoC | First candidate for Phase 13 |
| 2 | clang-tidy | Clang-based C++ linter/static analysis, works well with CMake compile database | Second candidate after Cppcheck |
| 3 | SARIF upload / code scanning | Result visualization and audit-style dashboard | Later phase only |

## C++ introduction plan

Phase 13 candidate flow:

1. Install Cppcheck in CI.
2. Run Cppcheck in report-only mode.
3. Save XML or text report as artifact.
4. Do not fail CI on findings at first.
5. Review findings and decide suppression or rule policy.
6. Consider clang-tidy after CMake compile database is stable.

Suggested first Cppcheck command:

```bash
mkdir -p reports/static
cppcheck --enable=warning,performance,portability \
  --xml --xml-version=2 \
  src 2> reports/static/cppcheck.xml
```

Notes:

- Avoid `--enable=all` as the first step because it can create too much noise.
- Prefer report-only until the baseline is understood.

## Python candidate tools

| Priority | Tool | Role | Phase 12 decision |
|---|---|---|---|
| 1 | Ruff | Python linter and formatter candidate | First candidate for Phase 13 |
| 2 | mypy | Optional static type checker | Second candidate, initially limited to core SILS modules |
| 3 | Pylint | Detailed code smell analysis | Later phase only |
| 4 | Pyright | Static type checker and VS Code learning companion | Later phase or editor-side learning |

## Python introduction plan

Phase 13 candidate flow:

1. Install Ruff in CI.
2. Run `ruff check` in report-only mode first or as a non-blocking local check.
3. Decide whether to add `ruff format --check`.
4. Add mypy only for core SILS modules at first.
5. Expand target directories after baseline issues are understood.

Suggested first Ruff commands:

```bash
mkdir -p reports/static
ruff check . --output-format=github | tee reports/static/ruff-check.txt
ruff format --check . | tee reports/static/ruff-format-check.txt
```

Suggested first mypy command:

```bash
mypy src | tee reports/static/mypy.txt
```

Adjust `src` to match the actual repository layout.

## Phase 12 decision

Static analysis tools are selected, but not yet introduced as blocking quality gates.

Recommended next phase:

- Phase 13-A: Add Ruff report-only.
- Phase 13-B: Add Cppcheck report-only.
- Phase 14 or later: Decide limited gate rules after baseline cleanup.
