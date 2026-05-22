from pathlib import Path

import pytest

from mini_sils.scenario_runner import run_fan_control_scenario


@pytest.mark.parametrize(
    "scenario_path",
    sorted(Path("scenarios/fan_control").glob("*.csv")),
)
def test_fan_control_scenario_all_pass(scenario_path: Path) -> None:
    results = run_fan_control_scenario(scenario_path)

    assert len(results) > 0
    assert all(result.match == "PASS" for result in results)
