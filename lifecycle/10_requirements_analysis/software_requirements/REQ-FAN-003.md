# REQ-FAN-003

## Title

Fan controller shall maintain stable state
within hysteresis ranges.

## Description

The fan controller shall avoid rapid
fan state oscillation by maintaining
the current fan state while coolant
temperature remains within hysteresis ranges.

## Rationale

This requirement prevents unstable
fan chattering behavior.

## Input

- coolant_temp_c
- current_fan_state

## Output

- next_fan_state

## Expected Behavior

- LOW remains LOW
  while 90 < coolant_temp_c < 105

- HIGH remains HIGH
  while coolant_temp_c > 100

## Related Scenarios

- SC-04

## Verification Environments

- python_sils
- cpp_sils
- arduino_hils
