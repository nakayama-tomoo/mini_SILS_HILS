from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:
    raise SystemExit(
        "PyYAML is required. Activate the project virtual environment first."
    ) from exc


TARGET_TO_ENVIRONMENT = {
    "python_sils": "PYTHON_SILS",
    "cpp_sils": "CPP_SILS",
    "mini_hils": "ARDUINO_HILS",
}

TARGET_TO_IMPLEMENTATION = {
    "python_sils": "python_sils",
    "cpp_sils": "cpp_sils",
    "mini_hils": "arduino_hils",
}

SCENARIO_HYPHEN_PATTERN = re.compile(r"^SC-\d+$")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def add_error(errors: list[str], message: str) -> None:
    errors.append(message)


def check_no_hyphen_scenario_id(
    value: str,
    context: str,
    errors: list[str],
) -> None:
    if SCENARIO_HYPHEN_PATTERN.match(value):
        add_error(
            errors,
            f"{context}: old scenario_id format found: {value}",
        )


def build_suite_map(
    suite: dict[str, Any],
    errors: list[str],
) -> dict[str, dict[str, Any]]:
    scenarios = suite.get("scenarios", [])
    suite_map: dict[str, dict[str, Any]] = {}

    for index, scenario in enumerate(scenarios):
        scenario_id = scenario.get("id")
        version_id = scenario.get("version_id")
        targets = scenario.get("targets", [])

        context = f"scenario_suite.yaml scenarios[{index}]"

        if not scenario_id:
            add_error(errors, f"{context}: missing id")
            continue

        check_no_hyphen_scenario_id(
            scenario_id,
            context,
            errors,
        )

        if scenario_id in suite_map:
            add_error(
                errors,
                f"{context}: duplicate scenario id: {scenario_id}",
            )

        if not version_id:
            add_error(
                errors,
                f"{context}: missing version_id for {scenario_id}",
            )

        if not targets:
            add_error(
                errors,
                f"{context}: missing targets for {scenario_id}",
            )

        for target in targets:
            if target not in TARGET_TO_ENVIRONMENT:
                add_error(
                    errors,
                    f"{context}: unknown target '{target}' for {scenario_id}",
                )

        suite_map[scenario_id] = scenario

    return suite_map


def build_scenario_requirement_map(
    traceability: dict[str, Any],
    suite_map: dict[str, dict[str, Any]],
    errors: list[str],
) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}

    for index, scenario in enumerate(traceability.get("scenarios", [])):
        scenario_id = scenario.get("scenario_id")
        requirement_ids = scenario.get("requirement_ids", [])

        context = f"scenario_traceability.json scenarios[{index}]"

        if not scenario_id:
            add_error(errors, f"{context}: missing scenario_id")
            continue

        check_no_hyphen_scenario_id(
            scenario_id,
            context,
            errors,
        )

        if scenario_id not in suite_map:
            add_error(
                errors,
                f"{context}: scenario_id not found in scenario_suite.yaml: {scenario_id}",
            )

        if scenario_id in result:
            add_error(
                errors,
                f"{context}: duplicate scenario_id: {scenario_id}",
            )

        if not requirement_ids:
            add_error(
                errors,
                f"{context}: empty requirement_ids for {scenario_id}",
            )

        result[scenario_id] = requirement_ids

    return result


def build_coverage_map(
    coverage_matrix: dict[str, Any],
    suite_map: dict[str, dict[str, Any]],
    errors: list[str],
) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}

    rows = None

    for key in (
        "coverage",
        "entries",
        "requirements",
        "matrix",
        "coverage_matrix",
    ):
        candidate = coverage_matrix.get(key)

        if isinstance(candidate, list):
            rows = candidate
            break

    if rows is None:
        add_error(
            errors,
            "coverage_matrix.json: no supported coverage row key found; "
            "expected one of coverage, entries, requirements, matrix, coverage_matrix",
        )
        return result

    for index, row in enumerate(rows):
        requirement_id = row.get("requirement_id")
        covered_by = row.get("covered_by", [])

        context = f"coverage_matrix.json row[{index}]"

        if not requirement_id:
            add_error(errors, f"{context}: missing requirement_id")
            continue

        if not covered_by:
            add_error(
                errors,
                f"{context}: empty covered_by for {requirement_id}",
            )

        for scenario_id in covered_by:
            check_no_hyphen_scenario_id(
                scenario_id,
                context,
                errors,
            )

            if scenario_id not in suite_map:
                add_error(
                    errors,
                    f"{context}: scenario_id not found in scenario_suite.yaml: {scenario_id}",
                )

        result[requirement_id] = covered_by

    return result


def validate_coverage_links(
    scenario_requirement_map: dict[str, list[str]],
    coverage_map: dict[str, list[str]],
    errors: list[str],
) -> None:
    for scenario_id, requirement_ids in scenario_requirement_map.items():
        for requirement_id in requirement_ids:
            covered_by = coverage_map.get(requirement_id, [])

            if scenario_id not in covered_by:
                add_error(
                    errors,
                    "coverage_matrix.json: "
                    f"{requirement_id} does not cover {scenario_id}",
                )


def validate_version_compatibility_matrix(
    matrix: dict[str, Any],
    suite_map: dict[str, dict[str, Any]],
    scenario_requirement_map: dict[str, list[str]],
    errors: list[str],
) -> None:
    actual_entries: set[tuple[str, str, str, str]] = set()

    for index, entry in enumerate(matrix.get("entries", [])):
        requirement_id = entry.get("requirement_id")
        version_id = entry.get("version_id")
        environment = entry.get("environment")
        scenario_id = entry.get("scenario_id")

        context = f"version_compatibility_matrix.json entries[{index}]"

        if not scenario_id:
            add_error(errors, f"{context}: missing scenario_id")
            continue

        check_no_hyphen_scenario_id(
            scenario_id,
            context,
            errors,
        )

        if scenario_id not in suite_map:
            add_error(
                errors,
                f"{context}: scenario_id not found in scenario_suite.yaml: {scenario_id}",
            )
            continue

        expected_version_id = suite_map[scenario_id].get("version_id")
        if version_id != expected_version_id:
            add_error(
                errors,
                f"{context}: version_id mismatch for {scenario_id}: "
                f"expected {expected_version_id}, actual {version_id}",
            )

        targets = suite_map[scenario_id].get("targets", [])
        allowed_environments = {
            TARGET_TO_ENVIRONMENT[target]
            for target in targets
            if target in TARGET_TO_ENVIRONMENT
        }

        if environment not in allowed_environments:
            add_error(
                errors,
                f"{context}: environment {environment} is not allowed for {scenario_id}; "
                f"allowed={sorted(allowed_environments)}",
            )

        allowed_requirements = scenario_requirement_map.get(scenario_id, [])

        if requirement_id not in allowed_requirements:
            add_error(
                errors,
                f"{context}: requirement_id {requirement_id} is not linked to {scenario_id}; "
                f"allowed={allowed_requirements}",
            )

        actual_entries.add(
            (
                requirement_id,
                scenario_id,
                version_id,
                environment,
            )
        )

    expected_entries: set[tuple[str, str, str, str]] = set()

    for scenario_id, requirement_ids in scenario_requirement_map.items():
        if scenario_id not in suite_map:
            continue

        version_id = suite_map[scenario_id].get("version_id")
        targets = suite_map[scenario_id].get("targets", [])

        for requirement_id in requirement_ids:
            for target in targets:
                environment = TARGET_TO_ENVIRONMENT.get(target)

                if environment:
                    expected_entries.add(
                        (
                            requirement_id,
                            scenario_id,
                            version_id,
                            environment,
                        )
                    )

    missing_entries = expected_entries - actual_entries
    unexpected_entries = actual_entries - expected_entries

    for entry in sorted(missing_entries):
        add_error(
            errors,
            f"version_compatibility_matrix.json: missing expected entry {entry}",
        )

    for entry in sorted(unexpected_entries):
        add_error(
            errors,
            f"version_compatibility_matrix.json: unexpected entry {entry}",
        )


def validate_evidence_mapping(
    evidence_mapping: dict[str, Any],
    suite_map: dict[str, dict[str, Any]],
    scenario_requirement_map: dict[str, list[str]],
    errors: list[str],
) -> None:
    for index, item in enumerate(evidence_mapping.get("evidence", [])):
        scenario_id = item.get("scenario_id")
        requirement_ids = item.get("requirement_ids", [])

        context = f"evidence_mapping.json evidence[{index}]"

        if not scenario_id:
            add_error(errors, f"{context}: missing scenario_id")
            continue

        check_no_hyphen_scenario_id(
            scenario_id,
            context,
            errors,
        )

        if scenario_id not in suite_map:
            add_error(
                errors,
                f"{context}: scenario_id not found in scenario_suite.yaml: {scenario_id}",
            )

        expected_requirement_ids = scenario_requirement_map.get(scenario_id)

        if expected_requirement_ids is None:
            continue

        if set(requirement_ids) - set(expected_requirement_ids):
            add_error(
                errors,
                f"{context}: requirement_ids contain values not linked to {scenario_id}: "
                f"actual={requirement_ids}, expected_subset_of={expected_requirement_ids}",
            )


def validate_evidence_manifest(
    manifest: dict[str, Any],
    suite_map: dict[str, dict[str, Any]],
    scenario_requirement_map: dict[str, list[str]],
    errors: list[str],
) -> None:
    for index, item in enumerate(manifest.get("evidence", [])):
        scenario_id = item.get("scenario_id")
        version_id = item.get("version_id")
        requirement_ids = item.get("requirement_ids", [])
        implementations = item.get("implementations", [])
        environments = item.get("environments", [])
        hils_result = item.get("hils_result")

        context = f"evidence_manifest.json evidence[{index}]"

        if not scenario_id:
            add_error(errors, f"{context}: missing scenario_id")
            continue

        check_no_hyphen_scenario_id(
            scenario_id,
            context,
            errors,
        )

        if scenario_id not in suite_map:
            add_error(
                errors,
                f"{context}: scenario_id not found in scenario_suite.yaml: {scenario_id}",
            )
            continue

        expected_version_id = suite_map[scenario_id].get("version_id")

        if version_id != expected_version_id:
            add_error(
                errors,
                f"{context}: version_id mismatch for {scenario_id}: "
                f"expected {expected_version_id}, actual {version_id}",
            )

        expected_requirement_ids = scenario_requirement_map.get(scenario_id, [])

        if not requirement_ids:
            add_error(
                errors,
                f"{context}: empty requirement_ids for {scenario_id}",
            )

        if set(requirement_ids) != set(expected_requirement_ids):
            add_error(
                errors,
                f"{context}: requirement_ids mismatch for {scenario_id}: "
                f"expected={expected_requirement_ids}, actual={requirement_ids}",
            )

        targets = suite_map[scenario_id].get("targets", [])

        expected_implementations = [
            TARGET_TO_IMPLEMENTATION[target]
            for target in targets
            if target in TARGET_TO_IMPLEMENTATION
        ]

        expected_environments = [
            TARGET_TO_ENVIRONMENT[target]
            for target in targets
            if target in TARGET_TO_ENVIRONMENT
        ]

        if set(implementations) != set(expected_implementations):
            add_error(
                errors,
                f"{context}: implementations mismatch for {scenario_id}: "
                f"expected={expected_implementations}, actual={implementations}",
            )

        if set(environments) != set(expected_environments):
            add_error(
                errors,
                f"{context}: environments mismatch for {scenario_id}: "
                f"expected={expected_environments}, actual={environments}",
            )

        if "mini_hils" not in targets and hils_result != "SKIPPED":
            add_error(
                errors,
                f"{context}: hils_result should be SKIPPED for non-HILS scenario {scenario_id}; "
                f"actual={hils_result}",
            )


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]

    errors: list[str] = []

    suite = load_yaml(
        repo_root / "common" / "scenario" / "scenario_suite.yaml"
    )

    scenario_traceability = load_json(
        repo_root / "traceability" / "scenario_traceability.json"
    )

    coverage_matrix = load_json(
        repo_root / "traceability" / "coverage_matrix.json"
    )

    version_compatibility_matrix = load_json(
        repo_root / "traceability" / "version_compatibility_matrix.json"
    )

    evidence_mapping = load_json(
        repo_root / "traceability" / "evidence_mapping.json"
    )

    evidence_manifest = load_json(
        repo_root / "evidence" / "evidence_manifest.json"
    )

    suite_map = build_suite_map(
        suite,
        errors,
    )

    scenario_requirement_map = build_scenario_requirement_map(
        scenario_traceability,
        suite_map,
        errors,
    )

    coverage_map = build_coverage_map(
        coverage_matrix,
        suite_map,
        errors,
    )

    validate_coverage_links(
        scenario_requirement_map,
        coverage_map,
        errors,
    )

    validate_version_compatibility_matrix(
        version_compatibility_matrix,
        suite_map,
        scenario_requirement_map,
        errors,
    )

    validate_evidence_mapping(
        evidence_mapping,
        suite_map,
        scenario_requirement_map,
        errors,
    )

    validate_evidence_manifest(
        evidence_manifest,
        suite_map,
        scenario_requirement_map,
        errors,
    )

    if errors:
        print("Traceability consistency: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Traceability consistency: PASS")
    print(f"scenarios checked: {len(suite_map)}")
    print(
        "scenario traceability entries checked: "
        f"{len(scenario_requirement_map)}"
    )
    print(
        "version compatibility entries checked: "
        f"{len(version_compatibility_matrix.get('entries', []))}"
    )
    print(
        "evidence entries checked: "
        f"{len(evidence_manifest.get('evidence', []))}"
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
