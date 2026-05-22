from __future__ import annotations

import json
from pathlib import Path


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def main() -> None:

    repo_root = (
        Path(__file__)
        .resolve()
        .parents[1]
    )

    traceability = load_json(
        repo_root
        / "traceability"
        / "scenario_traceability.json"
    )

    requirement_map = {}

    for scenario in (
        traceability["scenarios"]
    ):

        scenario_id = (
            scenario["scenario_id"]
        )

        for requirement_id in (
            scenario["requirement_ids"]
        ):

            if (
                requirement_id
                not in requirement_map
            ):

                requirement_map[
                    requirement_id
                ] = []

            requirement_map[
                requirement_id
            ].append(
                scenario_id
            )

    coverage_matrix = {

        "schema_version":
            "0.1.0",

        "requirements": [],
    }

    for requirement_id in sorted(
        requirement_map.keys()
    ):

        coverage_matrix[
            "requirements"
        ].append({

            "requirement_id":
                requirement_id,

            "covered_by":
                sorted(
                    requirement_map[
                        requirement_id
                    ]
                ),
        })

    output_path = (
        repo_root
        / "traceability"
        / "coverage_matrix.json"
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            coverage_matrix,
            file,
            indent=2,
        )

    print(
        f"Generated: {output_path}"
    )


if __name__ == "__main__":
    main()
