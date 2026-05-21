from pathlib import Path
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
                "mini-sils-poc/scripts/run_fan_control_sils.py",
            ]

            print(" command     :", " ".join(command))

            result = subprocess.run(command)

            print(" returncode  :", result.returncode)

        else:
            print(" status      : NOT FOUND")

        print()


if __name__ == "__main__":
    main()
