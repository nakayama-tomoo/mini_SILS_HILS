from enum import Enum
from mini_sils.version_loader import load_version

class FanState(str, Enum):
    OFF = "OFF"
    LOW = "LOW"
    HIGH = "HIGH"

def decide_fan_state(
    prev_fan_state: FanState,
    coolant_temp_c: int,
    version_id: str = "fan_control_v1",
) -> FanState:

    version = load_version(version_id)

    thresholds = version["thresholds"]

    low_on_c = thresholds["low_on_c"]
    off_c = thresholds["off_c"]
    high_on_c = thresholds["high_on_c"]
    high_off_c = thresholds["high_off_c"]

    """
    Decide the next electric radiator fan state.

    This logic is fictional and generalized.
    It is not intended to represent a real vehicle cooling system.
    """

    if prev_fan_state == FanState.OFF:
        if coolant_temp_c < low_on_c:
            return FanState.OFF
        if coolant_temp_c < high_on_c:
            return FanState.LOW
        return FanState.HIGH

    if prev_fan_state == FanState.LOW:
        if coolant_temp_c <= off_c:
            return FanState.OFF
        if coolant_temp_c < high_on_c:
            return FanState.LOW
        return FanState.HIGH

    if prev_fan_state == FanState.HIGH:
        if coolant_temp_c <= off_c:
            return FanState.OFF
        if coolant_temp_c <= high_off_c:
            return FanState.LOW
        return FanState.HIGH

    raise ValueError(f"Unsupported fan state: {prev_fan_state}")
