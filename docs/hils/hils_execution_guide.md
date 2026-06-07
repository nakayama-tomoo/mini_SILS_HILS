# HILS Execution Guide

## Purpose

This document describes how to execute the Mini HILS environment using Raspberry Pi 5 and Arduino.

## Hardware Configuration

### Test Bench

* Raspberry Pi 5
* Arduino DUT (Device Under Test)
* USB Serial connection

### Communication

* Serial Port: `/dev/ttyUSB0`
* Baud Rate: 115200

## HILS Environment Location

```text
/home/pi5admin/mini-sils-hils
```

## Execution Procedure

### Connect to Raspberry Pi 5

```bash
ssh pi5admin@raspberrypi5.local
```

### Move to HILS Source Directory

```bash
cd ~/mini-sils-hils/mini-hils/src
```

### Execute HILS

```bash
python3 run_all_hils.py
```

## Expected Output

Scenario execution:

* SC_01
* SC_02
* SC_03
* SC_04

Expected overall result:

PASS

## Generated Evidence

```text
mini-hils/results/
```

Files:

* sc_01_hils.json
* sc_02_hils.json
* sc_03_hils.json
* sc_04_hils.json
* hils_summary.json

## Notes

This environment is intended for educational Mini HILS validation only.

No vehicle hardware or production ECU is connected.

