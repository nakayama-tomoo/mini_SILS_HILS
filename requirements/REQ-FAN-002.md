# REQ-FAN-002

## Title

Fan shall transition from LOW to HIGH
when coolant temperature reaches HIGH ON threshold.

## Description

When the current fan state is LOW
and coolant temperature is greater than
or equal to 105 degrees Celsius,
the fan controller shall transition
the fan state to HIGH.

## Rationale

This requirement represents
high temperature cooling escalation.

## Input

- coolant_temp_c
- current_fan_state

## Output

- next_fan_state

## Threshold

- HIGH_ON_THRESHOLD_C = 105

## Expected Behavior

LOW -> HIGH

## Related Scenarios

- SC-03
- SC-04

## Verification Environments

- python_sils
- cpp_sils
- arduino_hils
