from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any, Optional

try:
    import yaml
except ImportError as exc:
    raise SystemExit(
        "PyYAML is required. Activate the project virtual environment first."
    ) from exc


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

CPP_RESULTS_DIRS = [
    BASE_DIR
    / "implementations"
    / "python_sils"
    / "cpp"
    / "results",
    BASE_DIR
    / "implementations"
    / "cpp_sils"
    / "results",
]

HILS_SUMMARY_PATH = (
    BASE_DIR
    / "results"
    / "hils"
    / "hils_summary.json"
)

ALL_RESULTS_OUTPUT_PATH = (
    BASE_DIR
    / "results"
    / "all_results_summary.json"
)

COMPARISON_OUTPUT_PATH = (
    BASE_DIR
    / "results"
    / "comparison"
    / "comparison_summary.json"
)


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def normalize_scenario_id(value: str) -> str:
    normalized = value.strip().upper()

    if normalized.startswith("SC_"):
        return normalized

    if normalized.startswith("SC-"):
        return normalized.replace("-", "_")

    match = re.search(r"SC[_-]?(\d+)", normalized)

    if match:
        return f"SC_{match.group(1).zfill(2)}"

    return normalized


def result_status_from_csv(path: Optional[Path]) -> str:
    if path is None or not path.exists():
        return "NOT_FOUND"

    rows = load_csv(path)

    if not rows:
        return "FAIL"

    for row in rows:
        value = (
            row.get("match")
            or row.get("result")
            or row.get("overall")
            or ""
        ).strip().upper()

        if value not in {"PASS", "MATCH"}:
            return "FAIL"

    return "PASS"


def first_value(row: dict[str, str], keys: list[str]) -> str:
    for key in keys:
        value = row.get(key)

        if value is not None:
            return value.strip().upper()

    return ""


def compare_python_cpp_csv(
    python_path: Optional[Path],
    cpp_path: Optional[Path],
) -> str:
    if python_path is None or not python_path.exists():
        return "MISMATCH"

    if cpp_path is None or not cpp_path.exists():
        return "MISMATCH"

    python_rows = load_csv(python_path)
    cpp_rows = load_csv(cpp_path)

    if len(python_rows) != len(cpp_rows):
        return "MISMATCH"

    actual_keys = [
        "actual_fan_state",
        "actual_state",
        "actual_fan_command",
        "actual_command",
        "actual",
    ]

    for python_row, cpp_row in zip(python_rows, cpp_rows):
        python_match = first_value(
            python_row,
            [
                "match",
                "result",
                "overall",
            ],
        )

        cpp_match = first_value(
            cpp_row,
            [
                "match",
                "result",
                "overall",
            ],
        )

        if python_match != cpp_match:
            return "MISMATCH"

        python_actual = first_value(python_row, actual_keys)
        cpp_actual = first_value(cpp_row, actual_keys)

        if python_actual and cpp_actual and python_actual != cpp_actual:
            return "MISMATCH"

    return "MATCH"


def find_python_result(scenario_name: str) -> Optional[Path]:
    path = PYTHON_RESULTS_DIR / f"{scenario_name}_results.csv"

    if path.exists():
        return path

    return None


def find_cpp_result(scenario_name: str) -> Optional[Path]:
    for directory in CPP_RESULTS_DIRS:
        path = directory / f"{scenario_name}_cpp_results.csv"

        if path.exists():
            return path

    return None


def relative_path(path: Optional[Path]) -> Optional[str]:
    if path is None:
        return None

    return str(path.relative_to(BASE_DIR))


def build_hils_result_map(
    hils_summary: dict[str, Any],
) -> dict[str, str]:
    result_map: dict[str, str] = {}

    rows = []

    for key in [
        "scenario_results",
        "scenarios",
        "results",
    ]:
        candidate = hils_summary.get(key)

        if isinstance(candidate, list):
            rows = candidate
            break

    for row in rows:
        if not isinstance(row, dict):
            continue

        result = (
            row.get("result")
            or row.get("overall")
            or row.get("status")
            or "UNKNOWN"
        )

        keys = [
            row.get("scenario_id"),
            row.get("scenario"),
            row.get("id"),
            row.get("name"),
        ]

        for key in keys:
            if not key:
                continue

            key_text = str(key)
            result_map[normalize_scenario_id(key_text)] = str(result)
            result_map[Path(key_text).stem] = str(result)

    return result_map


def scenario_overall(
    targets: list[str],
    python_status: str,
    cpp_status: str,
    python_cpp_status: str,
    hils_status: str,
) -> str:
    checks: list[bool] = []

    if "python_sils" in targets:
        checks.append(python_status == "PASS")

    if "cpp_sils" in targets:
        checks.append(cpp_status == "PASS")

    if "python_sils" in targets and "cpp_sils" in targets:
        checks.append(python_cpp_status == "MATCH")

    if "mini_hils" in targets:
        checks.append(hils_status == "PASS")

    return "PASS" if checks and all(checks) else "FAIL"


def main() -> None:
    scenario_suite = load_yaml(SCENARIO_SUITE_PATH)
    hils_summary = load_json_if_exists(HILS_SUMMARY_PATH)
    hils_map = build_hils_result_map(hils_summary)

    scenario_records = []
    comparison_records = []

    for scenario in scenario_suite["scenarios"]:
        scenario_id = scenario["id"]
        scenario_name = Path(scenario["file"]).stem
        version_id = scenario.get("version_id", "UNKNOWN")
        targets = scenario.get("targets", [])

        python_result_path = find_python_result(scenario_name)
        cpp_result_path = find_cpp_result(scenario_name)

        if "python_sils" in targets:
            python_status = result_status_from_csv(python_result_path)
        else:
            python_status = "SKIPPED"

        if "cpp_sils" in targets:
            cpp_status = result_status_from_csv(cpp_result_path)
        else:
            cpp_status = "SKIPPED"

        if "python_sils" in targets and "cpp_sils" in targets:
            python_cpp_status = compare_python_cpp_csv(
                python_result_path,
                cpp_result_path,
            )
        else:
            python_cpp_status = "SKIPPED"

        if "mini_hils" in targets:
            hils_status = hils_map.get(
                normalize_scenario_id(scenario_id),
                hils_map.get(scenario_name, "NOT_FOUND"),
            )
        else:
            hils_status = "SKIPPED"

        overall = scenario_overall(
            targets,
            python_status,
            cpp_status,
            python_cpp_status,
            hils_status,
        )

        scenario_records.append(
            {
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
        )

        comparison_records.append(
            {
                "scenario": scenario_name,
                "version_id": version_id,
                "comparison": python_cpp_status,
                "python_cpp": python_cpp_status,
                "hils": hils_status,
                "python_result": relative_path(python_result_path),
                "cpp_result": relative_path(cpp_result_path),
                "hils_result": (
                    relative_path(HILS_SUMMARY_PATH)
                    if "mini_hils" in targets and HILS_SUMMARY_PATH.exists()
                    else None
                ),
                "overall": overall,
            }
        )

    passed_scenarios = sum(
        1
        for record in scenario_records
        if record["overall"] == "PASS"
    )

    failed_scenarios = len(scenario_records) - passed_scenarios

    overall = "PASS" if failed_scenarios == 0 else "FAIL"

    summary = {
        "suite": scenario_suite["suite_name"],
        "overall": overall,
        "total_scenarios": len(scenario_records),
        "passed_scenarios": passed_scenarios,
        "failed_scenarios": failed_scenarios,
        "scenarios": scenario_records,
        "comparisons": comparison_records,
    }

    ALL_RESULTS_OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with ALL_RESULTS_OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)
        file.write("\n")

    comparison_summary = {
        "overall": overall,
        "comparisons": comparison_records,
    }

    COMPARISON_OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with COMPARISON_OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(comparison_summary, file, indent=2)
        file.write("\n")

    print("=" * 60)
    print("All Results Summary")
    print("=" * 60)
    print(json.dumps(summary, indent=2))
    print()
    print(" output:", ALL_RESULTS_OUTPUT_PATH)
    print(" output:", COMPARISON_OUTPUT_PATH)

    if overall != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
