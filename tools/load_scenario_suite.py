from pathlib import Path
import yaml


SCENARIO_SUITE_PATH = (
    Path(__file__)
    .resolve()
    .parent.parent
    / "common"
    / "scenario"
    / "scenario_suite.yaml"
)


def main():
    with open(SCENARIO_SUITE_PATH, "r", encoding="utf-8") as f:
        suite = yaml.safe_load(f)

    print("=" * 60)
    print(f"Suite Name : {suite['suite_name']}")
    print(f"Owner      : {suite['owner']}")
    print("=" * 60)

    for scenario in suite["scenarios"]:
        print(
            f"{scenario['id']} | "
            f"{scenario['category']} | "
            f"{scenario['description']}"
        )

        print(f"  file: {scenario['file']}")
        print(f"  targets: {', '.join(scenario['targets'])}")
        print()


if __name__ == "__main__":
    main()
