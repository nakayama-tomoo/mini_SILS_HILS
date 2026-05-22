# REQ-FAN-001

## Title

Fan shall transition from OFF to LOW
when coolant temperature reaches LOW ON threshold.

## Description

When the current fan state is OFF
and coolant temperature is greater than
or equal to 95 degrees Celsius,
the fan controller shall transition
the fan state to LOW.

## Rationale

This requirement represents
the start of radiator cooling fan operation.

## Input

- coolant_temp_c
- current_fan_state

## Output

- next_fan_state

## Threshold

- LOW_ON_THRESHOLD_C = 95

## Expected Behavior

OFF -> LOW

## Related Scenarios

- SC-01
- SC-02

## Verification Environments

- python_sils
- cpp_sils
- arduino_hils
