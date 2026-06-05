from pathlib import Path
import csv
import json


BASE_DIR = Path(__file__).resolve().parent.parent

PYTHON_RESULTS_DIR = (
    BASE_DIR
    / "implementations"
    / "python_sils"
    / "results"
    / "fan_control"
)

CPP_RESULTS_DIR = (
    BASE_DIR
    / "implementations"
    / "python_sils"
    / "cpp"
    / "results"
)

OUTPUT_PATH = (
    BASE_DIR
    / "results"
    / "comparison_summary.json"
)


def load_csv(path):
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    comparisons = []

    python_files = sorted(
        PYTHON_RESULTS_DIR.glob("*_results.csv")
    )

    overall_match = True

    for python_file in python_files:
        scenario_name = python_file.name.replace(
            "_results.csv",
            "",
        )

        cpp_file = (
            CPP_RESULTS_DIR
            / f"{scenario_name}_cpp_results.csv"
        )

        comparison = {
            "scenario": scenario_name,
            "python_result": "FOUND",
            "cpp_result": "FOUND",
            "comparison": "MATCH",
        }

        if not cpp_file.exists():
            comparison["cpp_result"] = "NOT_FOUND"
            comparison["comparison"] = "MISMATCH"

            overall_match = False

            comparisons.append(comparison)
            continue

        python_rows = load_csv(python_file)
        cpp_rows = load_csv(cpp_file)

        if len(python_rows) != len(cpp_rows):
            comparison["comparison"] = "MISMATCH"
            overall_match = False

            comparisons.append(comparison)
            continue

        for py_row, cpp_row in zip(python_rows, cpp_rows):
            if py_row["match"] != cpp_row["match"]:
                comparison["comparison"] = "MISMATCH"
                overall_match = False
                break

        comparisons.append(comparison)

    summary = {
        "overall": "PASS" if overall_match else "FAIL",
        "comparisons": comparisons,
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("=" * 60)
    print("Comparison Summary")
    print("=" * 60)

    print(json.dumps(summary, indent=2))

    print()
    print(" output:", OUTPUT_PATH)

    if not overall_match:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
