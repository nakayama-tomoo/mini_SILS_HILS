#!/usr/bin/env python3

import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "evidence" / "evidence_manifest.json"


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    sys.exit(1)


def main() -> None:
    if not MANIFEST_PATH.exists():
        fail(f"Evidence manifest not found: {MANIFEST_PATH}")

    try:
        with MANIFEST_PATH.open("r", encoding="utf-8") as f:
            manifest = json.load(f)
    except json.JSONDecodeError as e:
        fail(f"Invalid JSON in evidence manifest: {e}")

    missing_files = []

    if "dependency_evidence" not in manifest:
        fail("dependency_evidence is missing from evidence manifest")

    dependency_evidence = manifest["dependency_evidence"]

    if not isinstance(dependency_evidence, list):
        fail("dependency_evidence must be a list")

    for evidence_item in dependency_evidence:
        evidence_id = evidence_item.get("id", "<missing id>")
        files = evidence_item.get("files", [])

        if not isinstance(files, list):
            fail(f"files must be a list in dependency_evidence item: {evidence_id}")

        for file_item in files:
            path_value = file_item.get("path")

            if not path_value:
                fail(f"Missing path in dependency_evidence item: {evidence_id}")

            evidence_file_path = REPO_ROOT / path_value

            if not evidence_file_path.exists():
                missing_files.append(
                    {
                        "evidence_id": evidence_id,
                        "path": path_value,
                    }
                )

    if missing_files:
        print("[FAIL] Missing evidence files referenced by evidence_manifest.json:")
        for missing in missing_files:
            print(f"  - id: {missing['evidence_id']}, path: {missing['path']}")
        sys.exit(1)

    print("[PASS] Evidence manifest references are valid.")


if __name__ == "__main__":
    main()
