from pathlib import Path

import pytest

from mini_sils.scenario_runner import (
    run_fan_control_scenario,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]
COMMON_SCENARIO_DIR = PROJECT_ROOT / "common" / "scenario" / "fan_control"


SCENARIO_VERSION_MATRIX = [
    (
        COMMON_SCENARIO_DIR / "sc_01_traffic_warmup_cooldown.csv",
        "fan_control_v1",
    ),
    (
        COMMON_SCENARIO_DIR / "sc_02_around_95deg_fluctuation.csv",
        "fan_control_v1",
    ),
    (
        COMMON_SCENARIO_DIR / "sc_03_rapid_heatup_recovery.csv",
        "fan_control_v1",
    ),
    (
        COMMON_SCENARIO_DIR / "sc_04_high_temp_oscillation.csv",
        "fan_control_v1",
    ),
    (
        COMMON_SCENARIO_DIR / "sc_05_v2_threshold_validation.csv",
        "fan_control_v2",
    ),
]


@pytest.mark.parametrize(
    ("scenario_path", "version_id"),
    SCENARIO_VERSION_MATRIX,
)
def test_fan_control_scenario_all_pass(
    scenario_path: Path,
    version_id: str,
) -> None:

    results = run_fan_control_scenario(
        scenario_path=scenario_path,
        version_id=version_id,
    )

    assert len(results) > 0

    assert all(
        result.match == "PASS"
        for result in results
    )
