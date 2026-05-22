from enum import Enum


class FanState(str, Enum):
    OFF = "OFF"
    LOW = "LOW"
    HIGH = "HIGH"


def decide_fan_state(prev_fan_state: FanState, coolant_temp_c: int) -> FanState:
    """
    Decide the next electric radiator fan state.

    This logic is fictional and generalized.
    It is not intended to represent a real vehicle cooling system.
    """

    if prev_fan_state == FanState.OFF:
        if coolant_temp_c < 95:
            return FanState.OFF
        if coolant_temp_c < 105:
            return FanState.LOW
        return FanState.HIGH

    if prev_fan_state == FanState.LOW:
        if coolant_temp_c <= 90:
            return FanState.OFF
        if coolant_temp_c < 105:
            return FanState.LOW
        return FanState.HIGH

    if prev_fan_state == FanState.HIGH:
        if coolant_temp_c <= 90:
            return FanState.OFF
        if coolant_temp_c <= 100:
            return FanState.LOW
        return FanState.HIGH

    raise ValueError(f"Unsupported fan state: {prev_fan_state}")
