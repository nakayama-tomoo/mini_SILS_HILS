from pathlib import Path
import argparse
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from mini_sils.result_writer import write_csv, write_json
from mini_sils.scenario_runner import run_fan_control_scenario

def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--scenario",
        type=str,
        help="Single scenario CSV path",
    )

    args = parser.parse_args()

    output_dir = REPO_ROOT / "results" / "fan_control"

    if args.scenario:
        scenario_files = [Path(args.scenario)]
    else:
        scenario_dir = REPO_ROOT / "scenarios" / "fan_control"
        scenario_files = sorted(scenario_dir.glob("*.csv"))


    if not scenario_files:
        raise FileNotFoundError(f"No scenario CSV files found: {scenario_dir}")

    total_cases = 0
    total_pass = 0
    total_fail = 0

    for scenario_path in scenario_files:
        results = run_fan_control_scenario(scenario_path)

        output_path = output_dir / f"{scenario_path.stem}_results.csv"
        write_csv(
            output_path,
            [result.__dict__ for result in results],
        )

        json_output_path = output_dir / f"{scenario_path.stem}_results.json"

        write_json(
            json_output_path,
            [result.__dict__ for result in results],
        )

        passed = sum(1 for result in results if result.match == "PASS")
        failed = sum(1 for result in results if result.match == "FAIL")

        total_cases += len(results)
        total_pass += passed
        total_fail += failed

        print(f"{scenario_path.name}: total={len(results)}, PASS={passed}, FAIL={failed}")
        print(f"  output: {output_path}")

    print("")
    print(f"TOTAL: {total_cases}")
    print(f"PASS : {total_pass}")
    print(f"FAIL : {total_fail}")

    if total_fail > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
