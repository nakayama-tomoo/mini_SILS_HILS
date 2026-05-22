from __future__ import annotations

import json
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def main() -> int:

    repo_root = (
        Path(__file__)
        .resolve()
        .parents[1]
    )

    coverage_matrix = load_json(
        repo_root
        / "traceability"
        / "coverage_matrix.json"
    )

    requirement_dir = (
        repo_root
        / "requirements"
    )

    requirement_files = sorted(
        requirement_dir.glob(
            "REQ-*.md"
        )
    )

    all_passed = True

    coverage_map = {}

    for requirement in (
        coverage_matrix["requirements"]
    ):

        coverage_map[
            requirement["requirement_id"]
        ] = requirement[
            "covered_by"
        ]

    for requirement_file in (
        requirement_files
    ):

        requirement_id = (
            requirement_file.stem
        )

        covered_by = (
            coverage_map.get(
                requirement_id,
                [],
            )
        )

        if not covered_by:

            print(
                "FAIL: uncovered requirement: "
                f"{requirement_id}"
            )

            all_passed = False

        else:

            print(
                "PASS: "
                f"{requirement_id} "
                f"covered by "
                f"{covered_by}"
            )

    if all_passed:

        print(
            "Coverage check: PASS"
        )

        return 0

    print(
        "Coverage check: FAIL"
    )

    return 1


if __name__ == "__main__":
    sys.exit(main())
