# SILS-HILS Comparison Policy

## Purpose

This document defines how SILS (Software-in-the-Loop Simulation) and HILS (Hardware-in-the-Loop Simulation) results are compared in the Mini SILS/HILS PoC.

The objective is not only to verify that SILS and HILS pass independently.

The objective is to verify that equivalent behavior is observed across execution environments.

## Scope

Current comparison targets:

* Python SILS
* C++ SILS
* Arduino HILS

Future targets may include:

* Raspberry Pi DUT
* STM32 DUT
* NXP S32K144EVB-Q100 DUT
* Cloud execution environments

## Comparison Basis

The following items shall be identical:

* Requirement ID
* Scenario ID
* Input sequence
* Expected behavior

## Acceptance Criteria

A scenario is considered equivalent when:

* Expected result matches
* SILS result matches
* HILS result matches

Example:

```text
Expected = HIGH
Python SILS = HIGH
C++ SILS = HIGH
Arduino HILS = HIGH
```

Result:

PASS

## Evidence

Comparison results shall be retained as project evidence.

Evidence may be used for:

* Traceability review
* Regression review
* Governance review
* Future DPG-related studies

## Limitations

This PoC validates logical behavior only.

Real-time characteristics and hardware timing behavior are outside the scope of this phase.

