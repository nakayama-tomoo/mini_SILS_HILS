from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:
    raise SystemExit(
        "PyYAML is required. Activate the project virtual environment first."
    ) from exc


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return load_json(path)


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def normalize_scenario_id(value: str) -> str:
    normalized = value.strip()

    if normalized.upper().startswith("SC_"):
        return normalized.upper()

    if normalized.upper().startswith("SC-"):
        return normalized.upper().replace("-", "_")

    parts = normalized.split("_")

    if len(parts) >= 2 and parts[0].lower() == "sc":
        return f"SC_{parts[1].zfill(2)}"

    return normalized.upper()


def build_traceability_map(traceability: dict[str, Any]) -> dict[str, list[str]]:
    traceability_map: dict[str, list[str]] = {}

    for scenario in traceability["scenarios"]:
        scenario_id = normalize_scenario_id(scenario["scenario_id"])
        traceability_map[scenario_id] = scenario["requirement_ids"]

    return traceability_map


def build_scenario_metadata(
    all_results_summary: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    metadata: dict[str, dict[str, Any]] = {}

    for scenario in all_results_summary.get("scenarios", []):
        scenario_name = scenario.get("scenario")
        scenario_id = scenario.get("id")

        if not scenario_name or not scenario_id:
            continue

        metadata[scenario_name] = {
            "scenario_id": normalize_scenario_id(scenario_id),
            "version_id": scenario.get("version_id", "UNKNOWN"),
            "targets": scenario.get("targets", []),
        }

    return metadata


def build_suite_metadata(
    scenario_suite: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    metadata: dict[str, dict[str, Any]] = {}

    for scenario in scenario_suite.get("scenarios", []):
        scenario_id = scenario.get("id")
        scenario_file = scenario.get("file")

        if not scenario_id or not scenario_file:
            continue

        scenario_name = Path(scenario_file).stem

        metadata[scenario_name] = {
            "scenario_id": normalize_scenario_id(scenario_id),
            "version_id": scenario.get("version_id", "UNKNOWN"),
            "targets": scenario.get("targets", []),
        }

    return metadata


def build_hils_map(hils_summary: dict[str, Any]) -> dict[str, str]:
    hils_map: dict[str, str] = {}

    for scenario in hils_summary.get("scenario_results", []):
        raw_scenario = scenario.get("scenario")
        result = scenario.get("result", "UNKNOWN")

        if not raw_scenario:
            continue

        normalized_id = normalize_scenario_id(raw_scenario)
        hils_map[normalized_id] = result
        hils_map[raw_scenario.upper()] = result

    return hils_map


def target_to_implementations(targets: list[str]) -> list[str]:
    mapping = {
        "python_sils": "python_sils",
        "cpp_sils": "cpp_sils",
        "mini_hils": "arduino_hils",
    }

    return [
        mapping[target]
        for target in targets
        if target in mapping
    ]


def target_to_environments(targets: list[str]) -> list[str]:
    mapping = {
        "python_sils": "PYTHON_SILS",
        "cpp_sils": "CPP_SILS",
        "mini_hils": "ARDUINO_HILS",
    }

    return [
        mapping[target]
        for target in targets
        if target in mapping
    ]


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]

    comparison_summary = load_json(
        repo_root / "results" / "comparison_summary.json"
    )

    all_results_summary = load_json_if_exists(
        repo_root / "results" / "all_results_summary.json"
    )

    hils_summary = load_json_if_exists(
        repo_root / "results" / "hils" / "hils_summary.json"
    )

    traceability = load_json(
        repo_root / "traceability" / "scenario_traceability.json"
    )

    scenario_suite = load_yaml(
        repo_root / "common" / "scenario" / "scenario_suite.yaml"
    )

    traceability_map = build_traceability_map(traceability)

    scenario_metadata = build_scenario_metadata(all_results_summary)
    scenario_metadata.update(
        build_suite_metadata(scenario_suite)
    )

    hils_map = build_hils_map(hils_summary)

    evidence_entries = []

    for comparison in comparison_summary["comparisons"]:
        scenario_name = comparison["scenario"]

        metadata = scenario_metadata.get(scenario_name, {})

        scenario_id = metadata.get(
            "scenario_id",
            normalize_scenario_id(scenario_name),
        )

        version_id = comparison.get(
            "version_id",
            metadata.get("version_id", "UNKNOWN"),
        )

        targets = metadata.get("targets", [])

        if not targets:
            targets = [
                "python_sils",
                "cpp_sils",
                "mini_hils",
            ]

        requirement_ids = traceability_map.get(
            scenario_id,
            [],
        )

        if "mini_hils" in targets:
            hils_result = hils_map.get(
                scenario_id,
                comparison.get("hils", "NOT_FOUND"),
            )
        else:
            hils_result = "SKIPPED"

        evidence_entries.append(
            {
                "scenario_id": scenario_id,
                "version_id": version_id,
                "requirement_ids": requirement_ids,
                "comparison": comparison.get(
                    "comparison",
                    comparison.get(
                        "python_cpp",
                        comparison.get("overall", "UNKNOWN"),
                    ),
                ),
                "python_result": comparison.get("python_result"),
                "cpp_result": comparison.get("cpp_result"),
                "hils_result": hils_result,
                "implementations": target_to_implementations(targets),
                "environments": target_to_environments(targets),
            }
        )

    dependency_evidence = [
        {
            "evidence_id": "PYTHON-DEPENDENCIES-001",
            "evidence_type": "python_dependency_snapshot",
            "description": "Python dependency evidence generated from the active virtual environment.",
            "files": [
                {
                    "path": "evidence/dependencies/python_freeze.txt",
                    "purpose": "Installed Python package list generated by pip freeze.",
                },
                {
                    "path": "evidence/dependencies/README.md",
                    "purpose": "Procedure for regenerating Python dependency evidence.",
                },
            ],
            "status": "AVAILABLE",
        }
    ]

    manifest = {
        "schema_version": "0.1.0",
        "overall": comparison_summary["overall"],
        "dependency_evidence": dependency_evidence,
        "evidence": evidence_entries,
    }

    output_path = repo_root / "evidence" / "evidence_manifest.json"

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            manifest,
            file,
            indent=2,
        )
        file.write("\n")

    print(f"Generated: {output_path}")


if __name__ == "__main__":
    main()
