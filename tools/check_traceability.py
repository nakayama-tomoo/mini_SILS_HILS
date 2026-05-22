from __future__ import annotations

import json
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def check_requirement_exists(
    repo_root: Path,
    requirement_id: str,
) -> bool:

    path = (
        repo_root
        / "requirements"
        / f"{requirement_id}.md"
    )

    if not path.exists():
        print(
            f"FAIL: missing requirement: {path}"
        )
        return False

    return True


def main() -> int:

    repo_root = (
        Path(__file__)
        .resolve()
        .parents[1]
    )

    scenario_traceability = load_json(
        repo_root
        / "traceability"
        / "scenario_traceability.json"
    )

    evidence_mapping = load_json(
        repo_root
        / "traceability"
        / "evidence_mapping.json"
    )

    all_passed = True

    scenario_ids = set()

    for scenario in (
        scenario_traceability["scenarios"]
    ):

        scenario_id = (
            scenario["scenario_id"]
        )

        scenario_ids.add(
            scenario_id
        )

        for requirement_id in (
            scenario["requirement_ids"]
        ):

            result = (
                check_requirement_exists(
                    repo_root,
                    requirement_id,
                )
            )

            all_passed = (
                all_passed
                and result
            )

    for evidence in (
        evidence_mapping["evidence"]
    ):

        scenario_id = (
            evidence["scenario_id"]
        )

        if (
            scenario_id
            not in scenario_ids
        ):

            print(
                "FAIL: evidence references "
                f"unknown scenario: "
                f"{scenario_id}"
            )

            all_passed = False

        result_file = (
            repo_root
            / evidence["result_file"]
        )

        if not result_file.exists():

            print(
                "FAIL: missing result file: "
                f"{result_file}"
            )

            all_passed = False

    if all_passed:

        print(
            "Traceability check: PASS"
        )

        return 0

    print(
        "Traceability check: FAIL"
    )

    return 1


if __name__ == "__main__":
    sys.exit(main())
