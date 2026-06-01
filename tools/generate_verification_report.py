from __future__ import annotations

import json
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent.parent

ALL_RESULTS_PATH = (
    BASE_DIR
    / "results"
    / "all_results_summary.json"
)

REPORT_PATH = (
    BASE_DIR
    / "results"
    / "verification_report.md"
)

REPORTS_DIR_PATH = (
    BASE_DIR
    / "results"
    / "reports"
    / "verification_report.md"
)


def load_all_results() -> dict[str, Any]:
    with ALL_RESULTS_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_scenario_records(
    summary: dict[str, Any],
) -> list[dict[str, Any]]:
    if "scenarios" in summary:
        return summary["scenarios"]

    records = []

    for comparison in summary.get("comparisons", []):
        records.append(
            {
                "id": "N/A",
                "scenario": comparison.get("scenario", ""),
                "version_id": comparison.get("version_id", "unspecified"),
                "python_sils": "N/A",
                "cpp_sils": "N/A",
                "python_cpp": comparison.get("python_cpp", "UNKNOWN"),
                "mini_hils": comparison.get("hils", "UNKNOWN"),
                "overall": comparison.get("overall", "UNKNOWN"),
            }
        )

    return records


def main() -> None:
    summary = load_all_results()
    scenario_records = get_scenario_records(summary)

    overall = summary.get("overall", "UNKNOWN")

    lines: list[str] = []

    lines.append("# Verification Report")
    lines.append("")
    lines.append("## Overall Result")
    lines.append("")
    lines.append(str(overall))
    lines.append("")

    lines.append("## Scenario Results")
    lines.append("")
    lines.append(
        "| ID | Scenario | Version | Python SILS | C++ SILS | Python/C++ | mini HILS | Overall |"
    )
    lines.append(
        "|---|---|---|---|---|---|---|---|"
    )

    for record in scenario_records:
        lines.append(
            "| "
            f"{record.get('id', 'N/A')} | "
            f"{record.get('scenario', '')} | "
            f"{record.get('version_id', 'unspecified')} | "
            f"{record.get('python_sils', 'UNKNOWN')} | "
            f"{record.get('cpp_sils', 'UNKNOWN')} | "
            f"{record.get('python_cpp', 'UNKNOWN')} | "
            f"{record.get('mini_hils', 'UNKNOWN')} | "
            f"{record.get('overall', 'UNKNOWN')} |"
        )

    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append(
        "- `SKIPPED` means the scenario did not target that execution environment."
    )
    lines.append(
        "- SC_05 is currently a Python SILS-only fan_control_v2 validation scenario."
    )
    lines.append(
        "- C++ SILS fan_control_v2 support is deferred until version-aware C++ execution is implemented."
    )
    lines.append("")

    lines.append("## Generated Artifacts")
    lines.append("")
    lines.append("- suite_summary.json")
    lines.append("- comparison_summary.json")
    lines.append("- all_results_summary.json")
    lines.append("- verification_report.md")
    lines.append("- reports/verification_report.md")
    lines.append("")

    report_text = "\n".join(lines)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR_PATH.parent.mkdir(parents=True, exist_ok=True)

    REPORT_PATH.write_text(report_text, encoding="utf-8")
    REPORTS_DIR_PATH.write_text(report_text, encoding="utf-8")

    print("=" * 60)
    print("Verification Report")
    print("=" * 60)
    print(report_text)
    print(f" output: {REPORT_PATH}")
    print(f" output: {REPORTS_DIR_PATH}")


if __name__ == "__main__":
    main()
