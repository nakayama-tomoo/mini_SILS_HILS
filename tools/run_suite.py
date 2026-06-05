from pathlib import Path
import json
import subprocess
import sys
import yaml


BASE_DIR = Path(__file__).resolve().parent.parent

SCENARIO_SUITE_PATH = (
    BASE_DIR
    / "common"
    / "scenario"
    / "scenario_suite.yaml"
)


def main():
    total_scenarios = 0
    passed_scenarios = 0
    failed_scenarios = 0

    with open(SCENARIO_SUITE_PATH, "r", encoding="utf-8") as f:
        suite = yaml.safe_load(f)

    print("=" * 60)
    print("Scenario Suite Runner")
    print("=" * 60)

    for scenario in suite["scenarios"]:
        version_id = scenario.get("version_id", "fan_control_v1")
        targets = scenario.get("targets", [])

        scenario_path = (
            BASE_DIR
            / "common"
            / "scenario"
            / scenario["file"]
        )

        print(f"[{scenario['id']}]")
        print(f" description : {scenario['description']}")
        print(f" category    : {scenario['category']}")
        print(f" version_id  : {version_id}")
        print(f" targets     : {', '.join(targets)}")
        print(f" scenario    : {scenario_path}")

        if not scenario_path.exists():
            print(" status      : NOT FOUND")
            failed_scenarios += 1
            print()
            continue

        print(" status      : FOUND")

        total_scenarios += 1
        scenario_pass = True

        if "python_sils" in targets:
            command = [
                sys.executable,
                "implementations/python_sils/scripts/run_fan_control_sils.py",
                "--scenario",
                str(scenario_path),
                "--version-id",
                version_id,
            ]

            print(" python cmd  :", " ".join(command))

            result = subprocess.run(command)

            print(" python rc   :", result.returncode)

            if result.returncode != 0:
                scenario_pass = False

        else:
            print(" python cmd  : SKIPPED")

        if "cpp_sils" in targets:
            cpp_command = [
                "./build/run_scenario",
                "--scenario",
                str(scenario_path),
                "--version-id",
                version_id,
            ]

            print(" cpp command :", " ".join(cpp_command))

            cpp_result = subprocess.run(
                cpp_command,
                cwd=BASE_DIR / "implementations" / "cpp_sils",
            )

            print(" cpp rc      :", cpp_result.returncode)

            if cpp_result.returncode != 0:
                scenario_pass = False

        else:
            print(" cpp command : SKIPPED")

        if scenario_pass:
            passed_scenarios += 1
        else:
            failed_scenarios += 1

        print()

    overall = "PASS"

    if failed_scenarios > 0:
        overall = "FAIL"

    summary = {
        "suite": suite["suite_name"],
        "total_scenarios": total_scenarios,
        "passed_scenarios": passed_scenarios,
        "failed_scenarios": failed_scenarios,
        "overall": overall,
    }

    summary_path = (
        BASE_DIR
        / "results"
        / "suite_summary.json"
    )

    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("=" * 60)
    print("Suite Summary")
    print("=" * 60)

    print(json.dumps(summary, indent=2))

    print()
    print(" summary     :", summary_path)

    if failed_scenarios > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
