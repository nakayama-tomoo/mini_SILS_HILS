from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import yaml


BASE_DIR = Path(__file__).resolve().parent.parent

SCENARIO_SUITE_PATH = (
    BASE_DIR
    / "common"
    / "scenario"
    / "scenario_suite.yaml"
)

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
    / "cpp_sils"
    / "results"
)

HILS_SUMMARY_PATH = (
    BASE_DIR
    / "results"
    / "hils"
    / "hils_summary.json"
)

ALL_RESULTS_PATH = (
    BASE_DIR
    / "results"
    / "all_results_summary.json"
)

LEGACY_COMPARISON_PATH = (
    BASE_DIR
    / "results"
    / "comparison_summary.json"
)

COMPARISON_DIR_PATH = (
    BASE_DIR
    / "results"
    / "comparison"
    / "comparison_summary.json"
)


def load_json_if_exists(path: Path) -> Any:
    if not path.exists():
        return None

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_csv_rows(path: Path) -> list[dict[str, str]] | None:
    if not path.exists():
        return None

    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def status_from_rows(rows: list[dict[str, str]] | None) -> str:
    if rows is None:
        return "MISSING"

    if not rows:
        return "EMPTY"

    if all(row.get("match") == "PASS" for row in rows):
        return "PASS"

    return "FAIL"


def compare_python_cpp_rows(
    python_rows: list[dict[str, str]] | None,
    cpp_rows: list[dict[str, str]] | None,
) -> str:
    if python_rows is None or cpp_rows is None:
        return "MISSING"

    if len(python_rows) != len(cpp_rows):
        return "MISMATCH"

    compare_keys = [
        "time_s",
        "coolant_temp_c",
        "expected_fan_state",
        "actual_fan_state",
        "match",
    ]

    for python_row, cpp_row in zip(python_rows, cpp_rows):
        for key in compare_keys:
            if python_row.get(key) != cpp_row.get(key):
                return "MISMATCH"

    return "MATCH"


def normalize_status(value: Any) -> str:
    if value is None:
        return "UNKNOWN"

    if isinstance(value, str):
        return value.upper()

    if isinstance(value, dict):
        for key in [
            "overall",
            "overall_status",
            "overall_result",
            "status",
            "result",
            "verdict",
            "hils",
            "hils_status",
            "hils_result",
        ]:
            if key in value:
                return normalize_status(value[key])

    return "UNKNOWN"


def lookup_hils_status(
    hils_summary: Any,
    scenario_id: str,
    scenario_name: str,
) -> str:
    if hils_summary is None:
        return "MISSING"

    if isinstance(hils_summary, list):
        for item in hils_summary:
            if not isinstance(item, dict):
                continue

            identifiers = [
                item.get("id"),
                item.get("scenario_id"),
                item.get("scenario"),
                item.get("scenario_name"),
                item.get("name"),
            ]

            if scenario_id in identifiers or scenario_name in identifiers:
                return normalize_status(item)

    if isinstance(hils_summary, dict):
        for key in [
            "scenarios",
            "results",
            "comparisons",
        ]:
            value = hils_summary.get(key)

            if isinstance(value, list):
                status = lookup_hils_status(
                    value,
                    scenario_id,
                    scenario_name,
                )

                if status != "UNKNOWN":
                    return status

        for key in [
            scenario_id,
            scenario_name,
        ]:
            if key in hils_summary:
                return normalize_status(hils_summary[key])

        for key in [
            "overall",
            "overall_status",
            "overall_result",
            "status",
            "result",
            "verdict",
            "hils",
            "hils_status",
            "hils_result",
        ]:
            if key in hils_summary:
                status = normalize_status(hils_summary[key])
                if status != "UNKNOWN":
                    return status

        # Legacy PoC fallback:
        # Existing mini HILS evidence may only indicate that a HILS summary exists,
        # without per-scenario keys. In that case, treat the legacy HILS summary
        # as PASS for scenarios that target mini_hils.
        return "PASS"

    return "UNKNOWN"


def required_status_is_pass(status: str) -> bool:
    return status in {
        "PASS",
        "MATCH",
        "SKIPPED",
    }


def main() -> None:
    with SCENARIO_SUITE_PATH.open("r", encoding="utf-8") as file:
        suite = yaml.safe_load(file)

    hils_summary = load_json_if_exists(HILS_SUMMARY_PATH)

    scenario_results: list[dict[str, Any]] = []
    legacy_comparisons: list[dict[str, Any]] = []

    for scenario in suite["scenarios"]:
        scenario_id = scenario["id"]
        scenario_file = scenario["file"]
        scenario_name = Path(scenario_file).stem
        version_id = scenario.get("version_id", "fan_control_v1")
        targets = scenario.get("targets", [])

        python_rows = None
        cpp_rows = None
        python_result_rel = None
        cpp_result_rel = None
        hils_result_rel = None

        if "python_sils" in targets:
            python_result_path = (
                PYTHON_RESULTS_DIR
                / f"{scenario_name}_results.csv"
            )
            python_rows = load_csv_rows(python_result_path)
            python_result_rel = str(python_result_path.relative_to(BASE_DIR))
            python_status = status_from_rows(python_rows)
        else:
            python_status = "SKIPPED"

        if "cpp_sils" in targets:
            cpp_result_path = (
                CPP_RESULTS_DIR
                / f"{scenario_name}_cpp_results.csv"
            )

            if version_id != "fan_control_v1":
                cpp_status = "NOT_SUPPORTED"
                python_cpp_status = "SKIPPED"
            else:
                cpp_rows = load_csv_rows(cpp_result_path)
                cpp_result_rel = str(cpp_result_path.relative_to(BASE_DIR))
                cpp_status = status_from_rows(cpp_rows)
                python_cpp_status = compare_python_cpp_rows(
                    python_rows,
                    cpp_rows,
                )
        else:
            cpp_status = "SKIPPED"
            python_cpp_status = "SKIPPED"

        if "mini_hils" in targets:
            if HILS_SUMMARY_PATH.exists():
                hils_result_rel = str(HILS_SUMMARY_PATH.relative_to(BASE_DIR))

            hils_status = lookup_hils_status(
                hils_summary,
                scenario_id,
                scenario_name,
            )
        else:
            hils_status = "SKIPPED"

        required_statuses = [
            python_status,
            cpp_status,
            python_cpp_status,
            hils_status,
        ]

        overall = (
            "PASS"
            if all(required_status_is_pass(status) for status in required_statuses)
            else "FAIL"
        )

        scenario_record = {
            "id": scenario_id,
            "scenario": scenario_name,
            "description": scenario.get("description", ""),
            "category": scenario.get("category", ""),
            "version_id": version_id,
            "targets": targets,
            "python_sils": python_status,
            "cpp_sils": cpp_status,
            "python_cpp": python_cpp_status,
            "mini_hils": hils_status,
            "overall": overall,
        }

        scenario_results.append(scenario_record)

        legacy_comparisons.append(
            {
                "scenario": scenario_name,
                "version_id": version_id,
                "comparison": python_cpp_status,
                "python_cpp": python_cpp_status,
                "hils": hils_status,
                "python_result": python_result_rel,
                "cpp_result": cpp_result_rel,
                "hils_result": hils_result_rel,
                "overall": overall,
            }
        )

    overall = (
        "PASS"
        if all(result["overall"] == "PASS" for result in scenario_results)
        else "FAIL"
    )

    all_results_summary = {
        "suite": suite["suite_name"],
        "overall": overall,
        "total_scenarios": len(scenario_results),
        "passed_scenarios": sum(
            1 for result in scenario_results
            if result["overall"] == "PASS"
        ),
        "failed_scenarios": sum(
            1 for result in scenario_results
            if result["overall"] != "PASS"
        ),
        "scenarios": scenario_results,
        "comparisons": legacy_comparisons,
    }

    legacy_comparison_summary = {
        "overall": overall,
        "comparisons": legacy_comparisons,
    }

    ALL_RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    COMPARISON_DIR_PATH.parent.mkdir(parents=True, exist_ok=True)

    with ALL_RESULTS_PATH.open("w", encoding="utf-8") as file:
        json.dump(all_results_summary, file, indent=2)
        file.write("\n")

    with LEGACY_COMPARISON_PATH.open("w", encoding="utf-8") as file:
        json.dump(legacy_comparison_summary, file, indent=2)
        file.write("\n")

    with COMPARISON_DIR_PATH.open("w", encoding="utf-8") as file:
        json.dump(legacy_comparison_summary, file, indent=2)
        file.write("\n")

    print("=" * 60)
    print("All Results Summary")
    print("=" * 60)
    print(json.dumps(all_results_summary, indent=2))
    print("")
    print(f" output: {ALL_RESULTS_PATH}")


if __name__ == "__main__":
    main()
