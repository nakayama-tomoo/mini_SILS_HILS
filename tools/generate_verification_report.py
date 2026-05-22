from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_PATH = (
    BASE_DIR
    / "results"
    / "all_results_summary.json"
)

OUTPUT_PATH = (
    BASE_DIR
    / "results"
    / "verification_report.md"
)


def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        summary = json.load(f)

    lines = []

    lines.append("# Verification Report")
    lines.append("")

    lines.append("## Overall Result")
    lines.append("")

    lines.append(summary["overall"])
    lines.append("")

    lines.append("## Scenario Results")
    lines.append("")

    lines.append("| Scenario | Python/C++ | HILS | Overall |")
    lines.append("|---|---|---|---|")

    for item in summary["comparisons"]:
        lines.append(
            f"| {item['scenario']} "
            f"| {item['python_cpp']} "
            f"| {item['hils']} "
            f"| {item['overall']} |"
        )

    lines.append("")
    lines.append("## Generated Artifacts")
    lines.append("")

    lines.append("- suite_summary.json")
    lines.append("- comparison_summary.json")
    lines.append("- all_results_summary.json")
    lines.append("- verification_report.md")

    report = "\n".join(lines)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(report)

    print("=" * 60)
    print("Verification Report")
    print("=" * 60)

    print(report)

    print()
    print(" output:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
