from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parent.parent

PYTHON_CPP_SUMMARY = (
    BASE_DIR
    / "results"
    / "comparison_summary.json"
)

HILS_SUMMARY = (
    BASE_DIR
    / "results"
    / "hils"
    / "hils_summary.json"
)

OUTPUT_PATH = (
    BASE_DIR
    / "results"
    / "all_results_summary.json"
)


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    python_cpp = load_json(PYTHON_CPP_SUMMARY)
    hils = load_json(HILS_SUMMARY)

    hils_map = {}

    for item in hils["scenario_results"]:
        hils_map[item["scenario"]] = item["result"]

    comparisons = []

    overall = "PASS"

    for item in python_cpp["comparisons"]:
        scenario = item["scenario"]

        short_name = scenario.split("_")[0] + "_" + scenario.split("_")[1]

        hils_result = hils_map.get(short_name, "NOT_FOUND")

        comparison = {
            "scenario": scenario,
            "python_cpp": item["comparison"],
            "hils": hils_result,
            "overall": "MATCH",
        }

        if (
            item["comparison"] != "MATCH"
            or
            hils_result != "PASS"
        ):
            comparison["overall"] = "MISMATCH"
            overall = "FAIL"

        comparisons.append(comparison)

    summary = {
        "overall": overall,
        "comparisons": comparisons,
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("=" * 60)
    print("All Results Summary")
    print("=" * 60)

    print(json.dumps(summary, indent=2))

    print()
    print(" output:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
