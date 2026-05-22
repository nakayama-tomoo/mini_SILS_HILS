import csv
from dataclasses import dataclass
from pathlib import Path

from mini_sils.fan_control import FanState, decide_fan_state


@dataclass(frozen=True)
class ScenarioResult:
    time_s: int
    coolant_temp_c: int
    expected_fan_state: str
    actual_fan_state: str
    match: str


def run_fan_control_scenario(
    scenario_path: Path,
    initial_state: FanState = FanState.OFF,
) -> list[ScenarioResult]:
    results: list[ScenarioResult] = []
    prev_fan_state = initial_state

    with scenario_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            time_s = int(row["time_s"])
            coolant_temp_c = int(row["coolant_temp_c"])
            expected_fan_state = FanState(row["expected_fan_state"])

            actual_fan_state = decide_fan_state(
                prev_fan_state=prev_fan_state,
                coolant_temp_c=coolant_temp_c,
            )

            match = "PASS" if actual_fan_state == expected_fan_state else "FAIL"

            results.append(
                ScenarioResult(
                    time_s=time_s,
                    coolant_temp_c=coolant_temp_c,
                    expected_fan_state=expected_fan_state.value,
                    actual_fan_state=actual_fan_state.value,
                    match=match,
                )
            )

            prev_fan_state = actual_fan_state

    return results
