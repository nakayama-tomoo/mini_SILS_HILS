from __future__ import annotations

from pathlib import Path

from mini_sils.scenario_runner import (
    run_fan_control_scenario,
)


def main() -> None:

    repo_root = (
        Path(__file__)
        .resolve()
        .parents[1]
    )

    scenario_path = (
        repo_root
        / "implementations"
        / "python_sils"
        / "scenarios"
        / "fan_control"
        / "sc_05_v2_threshold_validation.csv"
    )

    results = run_fan_control_scenario(
        scenario_path=scenario_path,
        version_id="fan_control_v2",
    )

    overall_pass = True

    print("")
    print(
        "=== fan_control_v2 validation ==="
    )
    print("")

    for result in results:

        print(
            f"time={result.time_s}s "
            f"temp={result.coolant_temp_c}C "
            f"expected={result.expected_fan_state} "
            f"actual={result.actual_fan_state} "
            f"result={result.match}"
        )

        if result.match != "PASS":
            overall_pass = False

    print("")

    if overall_pass:

        print(
            "fan_control_v2 validation: PASS"
        )

    else:

        print(
            "fan_control_v2 validation: FAIL"
        )


if __name__ == "__main__":
    main()
