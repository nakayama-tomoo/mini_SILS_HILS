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

    evidence_manifest = load_json(
        repo_root
        / "evidence"
        / "evidence_manifest.json"
    )

    matrix = {
        "schema_version": "0.1.0",
        "entries": [],
    }

    for evidence in (
        evidence_manifest["evidence"]
    ):

        version_id = (
            evidence["version_id"]
        )

        scenario_id = (
            evidence["scenario_id"]
        )

        for requirement_id in (
            evidence["requirement_ids"]
        ):

            for environment in (
                evidence["environments"]
            ):

                result = "PASS"

                if (
                    environment
                    == "ARDUINO_HILS"
                ):

                    result = (
                        evidence[
                            "hils_result"
                        ]
                    )

                matrix["entries"].append({

                    "requirement_id":
                        requirement_id,

                    "version_id":
                        version_id,

                    "environment":
                        environment,

                    "scenario_id":
                        scenario_id,

                    "result":
                        result,
                })

    output_path = (
        repo_root
        / "traceability"
        / "version_compatibility_matrix.json"
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            matrix,
            file,
            indent=2,
        )

    print(
        f"Generated: {output_path}"
    )


if __name__ == "__main__":
    main()
