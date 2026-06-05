# Phase 14 Static Analysis Baseline

## Purpose

This document defines the static analysis baseline for Phase 14.

The purpose of Phase 14 is not to fix all Ruff and Cppcheck findings immediately.
The purpose is to classify the findings detected in Phase 13 and record them as known findings.

## Scope

| Item | Value |
|---|---|
| Phase | Phase 14 |
| Theme | Mini SILS ④-F 静的解析baseline整理 |
| Base checkpoint | checkpoint/phase13-static-analysis-report-only |
| Ruff findings | 4 |
| Cppcheck findings | 6 |
| CI gate status | Not gated |
| Fix policy | No source code fix in Phase 14 unless required for evidence generation |

## Baseline Policy

Phase 14 treats the current Ruff and Cppcheck findings as known findings.

The CI result should continue even if static analysis findings exist.
The findings are recorded as evidence and will be reviewed in later phases.

## Classification Policy

| Classification | Meaning | Phase 14 action |
|---|---|---|
| fix_candidate | 修正候補。将来の品質改善対象 | Phase 14では修正しない |
| acceptable_for_poc | 個人PoC(Proof of Concept)として一時許容 | 理由をnotesに残す |
| needs_investigation | 追加確認が必要 | 後続Phaseで確認する |
| false_positive_candidate | 誤検知の可能性あり | 後続Phaseで抑止または設定変更を検討 |
| design_intent | 設計意図による指摘 | 設計理由をnotesに残す |

## Gate Policy

Static analysis findings are not used as a quality gate in Phase 14.

The current policy is report-only.

Future phases may introduce a quality gate after the baseline is stable.

## Summary

| Tool | Known findings | Treatment | Gate |
|---|---:|---|---|
| Ruff | 4 | Classify and record | Not gated |
| Cppcheck | 6 | Classify as style/design/fix candidate | Not gated |

## Evidence

The following evidence should be stored as CI artifacts.

| Artifact | Content |
|---|---|
| phase14-static-analysis-baseline | Baseline markdown, baseline CSV, generated evidence index |
| Ruff report artifact | Ruff report from static analysis job |
| Cppcheck report artifact | Cppcheck report from static analysis job |

## Notes

No company information, customer information, real project data, real vehicle data, or internal documents are used.
All scenarios and source code are part of a personal PoC.
