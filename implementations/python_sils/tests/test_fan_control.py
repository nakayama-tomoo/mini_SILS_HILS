import pytest

from mini_sils.fan_control import FanState, decide_fan_state


@pytest.mark.parametrize(
    "prev_fan_state,coolant_temp_c,expected_fan_state",
    [
        (FanState.OFF, 94, FanState.OFF),
        (FanState.OFF, 95, FanState.LOW),
        (FanState.OFF, 105, FanState.HIGH),
        (FanState.LOW, 91, FanState.LOW),
        (FanState.LOW, 90, FanState.OFF),
        (FanState.LOW, 105, FanState.HIGH),
        (FanState.HIGH, 101, FanState.HIGH),
        (FanState.HIGH, 100, FanState.LOW),
        (FanState.HIGH, 90, FanState.OFF),
        (FanState.OFF, 120, FanState.HIGH),
    ],
)
def test_decide_fan_state(
    prev_fan_state: FanState,
    coolant_temp_c: int,
    expected_fan_state: FanState,
) -> None:
    actual = decide_fan_state(prev_fan_state, coolant_temp_c)

    assert actual == expected_fan_state
