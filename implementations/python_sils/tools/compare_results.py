import csv
import json
import sys
from pathlib import Path


def read_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def compare_csv(
    python_csv: Path,
    cpp_csv: Path,
) -> tuple[bool, int]:
    python_rows = read_csv(python_csv)
    cpp_rows = read_csv(cpp_csv)

    if len(python_rows) != len(cpp_rows):
        print("")
        print("Row count mismatch:")
        print(f"  Python: {python_csv}")
        print(f"  C++   : {cpp_csv}")
        return False, 1

    mismatch_count = 0

    for index, (python_row, cpp_row) in enumerate(zip(python_rows, cpp_rows)):
        if python_row != cpp_row:
            mismatch_count += 1

            print("")
            print(f"Mismatch at row {index}")
            print("Python:")
            print(python_row)
            print("C++:")
            print(cpp_row)

    if mismatch_count > 0:
        print("")
        print(f"FAIL: {python_csv.name}")
        return False, mismatch_count

    print(f"PASS: {python_csv.name}")
    return True, 0


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]

    python_result_dir = (
        repo_root
        / "results"
        / "fan_control"
    )

    cpp_result_dir = (
        repo_root
        / "cpp"
        / "results"
    )

    python_csv_files = sorted(
        python_result_dir.glob("*_results.csv")
    )

    if not python_csv_files:
        print("No Python result CSV files found.")
        return 1

    scenario_results = []

    total_scenarios = 0
    passed_scenarios = 0
    failed_scenarios = 0
    total_mismatches = 0

    all_passed = True

    for python_csv in python_csv_files:
        scenario_name = python_csv.name.replace(
            "_results.csv",
            ""
        )

        cpp_csv = (
            cpp_result_dir
            / f"{scenario_name}_cpp_results.csv"
        )

        total_scenarios += 1

        if not cpp_csv.exists():
            print("")
            print(f"Missing C++ result file: {cpp_csv.name}")

            scenario_results.append({
                "scenario": scenario_name,
                "result": "FAIL",
                "mismatch_count": -1,
                "reason": "missing_cpp_result_file",
            })

            failed_scenarios += 1
            all_passed = False
            continue

        result, mismatch_count = compare_csv(
            python_csv,
            cpp_csv,
        )

        scenario_results.append({
            "scenario": scenario_name,
            "result": "PASS" if result else "FAIL",
            "mismatch_count": mismatch_count,
        })

        total_mismatches += mismatch_count

        if result:
            passed_scenarios += 1
        else:
            failed_scenarios += 1

        all_passed = all_passed and result

    summary = {
        "total_scenarios": total_scenarios,
        "passed_scenarios": passed_scenarios,
        "failed_scenarios": failed_scenarios,
        "total_mismatches": total_mismatches,
        "overall_result": "PASS" if all_passed else "FAIL",
        "scenario_results": scenario_results,
    }

    summary_path = (
        repo_root
        / "results"
        / "comparison_summary.json"
    )

    with summary_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            summary,
            file,
            indent=2,
        )

    print("")
    print(f"Summary JSON: {summary_path}")

    if all_passed:
        print("Comparison result: PASS")
        return 0

    print("Comparison result: FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
