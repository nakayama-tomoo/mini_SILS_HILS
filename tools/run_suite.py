from pathlib import Path
import json
import subprocess
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
        scenario_path = (
            BASE_DIR
            / "common"
            / "scenario"
            / scenario["file"]
        )

        print(f"[{scenario['id']}]")
        print(f" description : {scenario['description']}")
        print(f" category    : {scenario['category']}")
        print(f" scenario    : {scenario_path}")

        if scenario_path.exists():
            print(" status      : FOUND")

            command = [
               "python",
               "implementations/python_sils/scripts/run_fan_control_sils.py",
               "--scenario",
               str(scenario_path),
            ]

            cpp_command = [
                "./build/run_scenario",
                "--scenario",
                str(scenario_path),
            ]

            print(" command     :", " ".join(command))

            print(
                " cpp command :",
                " ".join(cpp_command),
            )

            result = subprocess.run(command)

            print(" returncode  :", result.returncode)

            cpp_result = subprocess.run(
                cpp_command,
                cwd=BASE_DIR / "implementations" / "cpp_sils",
            )

            print(
                " cpp returncode :",
                cpp_result.returncode,
            )

            total_scenarios += 1

            if (
                result.returncode == 0
                and
                cpp_result.returncode == 0
            ):
                passed_scenarios += 1
            else:
                failed_scenarios += 1

        else:
            print(" status      : NOT FOUND")

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


if __name__ == "__main__":
    main()
